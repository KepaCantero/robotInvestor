"""Envoltorio por agente: system prompt íntegro (cacheado), modelo configurable, mensaje JSON del contrato,
salida JSON validada con jsonschema, un reintento de reparación y, si persiste el fallo, estado PARCIAL con
registro en HA. Contabiliza tokens y UC por llamada y reutiliza resultados idénticos (HT-06)."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import jsonschema

from .configuracion import max_tokens_de, modelo_de
from .contratos import ESQUEMAS, contiene_credenciales
from .herramientas.ht06_indice import CacheResultados, clave_hash
from .llm import LLMClient, Uso, herramienta_busqueda_web
from .prompts import NOMBRES, CatalogoPrompts, mensaje_usuario


@dataclass
class ResultadoAgente:
    agente: str
    datos: Optional[Dict]
    estado: str                       # COMPLETO | PARCIAL
    uc: float = 0.0
    intentos: int = 0
    errores: List[str] = field(default_factory=list)
    cache_hit: bool = False
    uso: Uso = field(default_factory=Uso)


def extraer_json(texto: str) -> Any:
    t = texto.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t)
        t = re.sub(r"\n?```\s*$", "", t)
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        i, j = t.find("{"), t.rfind("}")
        if i >= 0 and j > i:
            return json.loads(t[i:j + 1])
        raise


def errores_esquema(datos: Any, esquema: Dict) -> List[str]:
    v = jsonschema.Draft202012Validator(esquema)
    return [f"{'/'.join(map(str, e.absolute_path)) or '(raíz)'}: {e.message}"[:300]
            for e in sorted(v.iter_errors(datos), key=lambda e: list(e.absolute_path))][:15]


class Agentes:
    """Fábrica/ejecutor de llamadas a los 21 agentes del Bloque A Forex (AG-01..AG-21)."""

    def __init__(self, cfg: Dict, cliente: LLMClient, almacen, contabilidad, monitor=None, cache: Optional[CacheResultados] = None) -> None:
        self.cfg = cfg
        self.cliente = cliente
        self.almacen = almacen
        self.contabilidad = contabilidad
        self.monitor = monitor
        self.prompts = CatalogoPrompts(cfg)
        self._avisados: set = set()
        llm = cfg.get("llm") or {}
        self.cache = cache if (cache is not None and llm.get("cache_resultados", True)) else None

    def verificar_prompts(self, agentes, run_id: Optional[str] = None) -> Dict[str, str]:
        """Carga (en el hilo principal) los prompts de los agentes indicados y registra una sola vez los que trabajan
        en modo degradado con el marco común. Devuelve {agente: archivo sustituto}."""
        for ag in agentes:
            self.prompts.texto(ag)
            if ag in self.prompts.sustituidos and ag not in self._avisados:
                self._avisados.add(ag)
                self.almacen.incidencia("OTRO", f"System prompt Forex de {ag} ({NOMBRES[ag]}) no encontrado: se usa "
                                        f"«{self.prompts.sustituidos[ag]}» (modo degradado)", ag, severidad="Operativa",
                                        tratamiento="análisis con el marco común de los Analistas de segmento o con el prompt del Bloque A general (transición); revisar 02_System_prompts",
                                        run_id=run_id)
        return {ag: self.prompts.sustituidos[ag] for ag in agentes if ag in self.prompts.sustituidos}

    def herramientas_para(self, agente: str, permitir_web: bool) -> Optional[List[Dict]]:
        bw = self.cfg.get("busqueda_web") or {}
        if (permitir_web and self.cfg.get("modo") == "vivo" and bw.get("habilitada_en_vivo")
                and agente in (bw.get("agentes") or [])):
            return [herramienta_busqueda_web(bw.get("tipo_herramienta", "web_search_20260318"), bw.get("max_usos_por_llamada", 5))]
        return None

    def invocar(self, agente: str, contrato: str, mensaje: Dict, esquema_clave: str, instrucciones: str,
                contexto: Dict, run_id: Optional[str] = None, segmento: Optional[str] = None, fase: Optional[str] = None,
                permitir_web: bool = False) -> ResultadoAgente:
        esquema = ESQUEMAS[esquema_clave]
        llm = self.cfg.get("llm") or {}
        modelo = modelo_de(self.cfg, agente)
        system = self.prompts.system(agente, llm.get("cache_prompts", True), llm.get("cache_ttl", "1h"))
        if agente in self.prompts.sustituidos and agente not in self._avisados:
            self._avisados.add(agente)
            self.almacen.incidencia("OTRO", f"System prompt Forex de {agente} ({NOMBRES[agente]}) no encontrado: se usa "
                                    f"«{self.prompts.sustituidos[agente]}» (modo degradado)", agente, severidad="Operativa",
                                    tratamiento="análisis con el marco común de los Analistas de segmento o con el prompt del Bloque A general (transición); revisar 02_System_prompts", run_id=run_id)
        texto_u = mensaje_usuario(contrato, mensaje, contexto, instrucciones, esquema)
        herramientas = self.herramientas_para(agente, permitir_web)
        clave = clave_hash(agente, modelo, texto_u, herramientas) if self.cache else None
        if clave:
            previo = self.cache.obtener(clave)
            if previo is not None:
                self.contabilidad.registrar(run_id, agente, modelo, Uso(), segmento, fase, cache_hit=True)
                return ResultadoAgente(agente, previo, "COMPLETO", 0.0, 0, [], True)
        mensajes = [{"role": "user", "content": texto_u}]
        errores: List[str] = []
        uc_total = 0.0
        uso_total = Uso()
        reintentos = int(llm.get("reintento_reparacion", 1))
        t0 = self.monitor.inicio(agente) if self.monitor else None
        if self.monitor:
            self.monitor.encolar(agente)
        try:
            for intento in range(reintentos + 1):
                r = self.cliente.generar(agente=agente, modelo=modelo, system=system, mensajes=mensajes,
                                         max_tokens=max_tokens_de(self.cfg, agente), herramientas=herramientas, esquema=esquema)
                uso_total.sumar(r.uso)
                uc_total += self.contabilidad.registrar(run_id, agente, modelo, r.uso, segmento, fase)
                try:
                    datos = extraer_json(r.texto)
                    errores = errores_esquema(datos, esquema)
                    if r.truncada:
                        errores.append("respuesta truncada por max_tokens")
                except (json.JSONDecodeError, ValueError) as e:
                    datos, errores = None, [f"JSON no válido: {e}"[:200]]
                if datos is not None and contiene_credenciales(datos):
                    errores.append("la respuesta contiene un patrón de credencial (R8)")
                if not errores:
                    if clave:
                        self.cache.guardar(clave, datos)
                    return ResultadoAgente(agente, datos, "COMPLETO", uc_total, intento + 1, [], False, uso_total)
                if intento < reintentos:
                    mensajes = mensajes + [
                        {"role": "assistant", "content": r.texto or "(vacío)"},
                        {"role": "user", "content": "Tu respuesta no cumple el formato exigido. Errores:\n- "
                         + "\n- ".join(errores) + "\nDevuelve SOLO el objeto JSON completo y corregido."}]
        finally:
            if self.monitor:
                self.monitor.fin(agente, t0)
        self.almacen.incidencia("OTRO", f"Salida no conforme de {agente} ({NOMBRES[agente]}) tras {reintentos} reparación(es): "
                                + "; ".join(errores)[:500], agente, severidad="Operativa",
                                tratamiento="estado PARCIAL declarado; la fase continúa con alcance reducido", run_id=run_id)
        return ResultadoAgente(agente, None, "PARCIAL", uc_total, reintentos + 1, errores, False, uso_total)
