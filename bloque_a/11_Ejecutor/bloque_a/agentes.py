"""Envoltorio por agente: system prompt íntegro (cacheado), modelo configurable, mensaje JSON del contrato,
salida JSON validada con jsonschema, un reintento de reparación y, si persiste el fallo, estado PARCIAL con
registro en HA. Contabiliza tokens y UC por llamada y reutiliza resultados idénticos (HT-06)."""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from typing import Any

import jsonschema

from .configuracion import max_tokens_de, modelo_de, parametro
from .contratos import ESQUEMAS, contiene_credenciales
from .herramientas.ht06_indice import CacheResultados, clave_hash
from .llm import (
    LLMClient,
    ReplayClient,
    Uso,
    con_guarda,
    contenido_sensible,
    herramienta_busqueda_web,
    respuesta_segura,
)
from .prompts import NOMBRES, CatalogoPrompts, mensaje_usuario


@dataclass
class ResultadoAgente:
    agente: str
    datos: dict | None
    estado: str                       # COMPLETO | PARCIAL | SIN_PRESUPUESTO (T-146: la primera petición no cabía; no salió)
    uc: float = 0.0
    intentos: int = 0
    errores: list[str] = field(default_factory=list)
    cache_hit: bool = False
    uso: Uso = field(default_factory=Uso)


def extraer_json(texto: str) -> Any:
    """El JSON de una respuesta. T-146 r02 (QA r01, H-05): uno demasiado anidado para leerlo (`RecursionError`) es un JSON
    no válido (`ValueError`), como cualquier otro: la llamada pide su reparación o queda PARCIAL, y el ciclo sigue."""
    t = texto.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t)
        t = re.sub(r"\n?```\s*$", "", t)
    try:
        try:
            return json.loads(t)
        except json.JSONDecodeError:
            i, j = t.find("{"), t.rfind("}")
            if i >= 0 and j > i:
                return json.loads(t[i:j + 1])
            raise
    except RecursionError:
        raise ValueError("JSON demasiado anidado para leerlo") from None


def errores_esquema(datos: Any, esquema: dict) -> list[str]:
    v = jsonschema.Draft202012Validator(esquema)
    return [f"{'/'.join(map(str, e.absolute_path)) or '(raíz)'}: {e.message}"[:300]
            for e in sorted(v.iter_errors(datos), key=lambda e: list(e.absolute_path))][:15]


class Agentes:
    """Fábrica/ejecutor de llamadas a los agentes AG-01..AG-25."""

    def __init__(self, cfg: dict, cliente: LLMClient, almacen, contabilidad, monitor=None, cache: CacheResultados | None = None) -> None:
        self.cfg = cfg
        self.cliente = cliente
        self.clientes: dict[str, LLMClient] = {}   # T-101 (V6, idea 8): cliente propio de un agente (Contradictor de otro proveedor)
        self.almacen = almacen
        self.contabilidad = contabilidad
        self.monitor = monitor
        self.prompts = CatalogoPrompts(cfg)
        self._avisados: set = set()
        llm = cfg.get("llm") or {}
        self.cache = cache if (cache is not None and llm.get("cache_resultados", True)) else None

    def verificar_prompts(self, agentes, run_id: str | None = None) -> dict[str, str]:
        """Carga (en el hilo principal) los prompts de los agentes indicados y registra una sola vez los que trabajan
        en modo degradado con el marco común. Devuelve {agente: archivo sustituto}."""
        for ag in agentes:
            self.prompts.texto(ag)
            if ag in self.prompts.sustituidos and ag not in self._avisados:
                self._avisados.add(ag)
                self.almacen.incidencia("OTRO", f"System prompt específico de {ag} ({NOMBRES[ag]}) no encontrado: se usa "
                                        f"«{self.prompts.sustituidos[ag]}» (modo degradado)", ag, severidad="Operativa",
                                        tratamiento="análisis con el marco común de los Analistas; revisar 02_System_prompts",
                                        run_id=run_id)
        return {ag: self.prompts.sustituidos[ag] for ag in agentes if ag in self.prompts.sustituidos}

    def herramientas_para(self, agente: str, permitir_web: bool) -> list[dict] | None:
        bw = self.cfg.get("busqueda_web") or {}
        if (permitir_web and self.cfg.get("modo") == "vivo" and bw.get("habilitada_en_vivo")
                and agente in (bw.get("agentes") or [])):
            return [herramienta_busqueda_web(bw.get("tipo_herramienta", "web_search_20260318"), parametro(self.cfg, "busqueda_web.max_usos_por_llamada"))]
        return None

    def invocar(self, agente: str, contrato: str, mensaje: dict, esquema_clave: str, instrucciones: str,
                contexto: dict, run_id: str | None = None, clase: str | None = None, fase: str | None = None,
                permitir_web: bool = False, guarda=None) -> ResultadoAgente:
        """`guarda` (T-146, `consumo.ReservaLlamada`): cada petición reserva su peor caso antes de salir (el primer intento,
        cada reparación y, en el cliente real, cada continuación); la que no cabe no sale."""
        esquema = ESQUEMAS[esquema_clave]
        llm = self.cfg.get("llm") or {}
        modelo = modelo_de(self.cfg, agente)
        system = self.prompts.system(agente, llm.get("cache_prompts", True), llm.get("cache_ttl", "1h"))
        if agente in self.prompts.sustituidos and agente not in self._avisados:
            self._avisados.add(agente)
            self.almacen.incidencia("OTRO", f"System prompt específico de {agente} ({NOMBRES[agente]}) no encontrado: se usa "
                                    f"«{self.prompts.sustituidos[agente]}» (modo degradado)", agente, severidad="Operativa",
                                    tratamiento="análisis con el marco común de los Analistas; revisar 02_System_prompts", run_id=run_id)
        texto_u = mensaje_usuario(contrato, mensaje, contexto, instrucciones, esquema)
        herramientas = self.herramientas_para(agente, permitir_web)
        if contenido_sensible([mensaje, contexto, system, texto_u]):
            self.almacen.incidencia("OTRO", "Encargo bloqueado por R8", agente, severidad="Operativa", run_id=run_id)
            return ResultadoAgente(agente, None, "PARCIAL", errores=["encargo bloqueado por R8"])
        max_tokens = max_tokens_de(self.cfg, agente)
        cliente = self.clientes.get(agente, self.cliente)
        clave = clave_hash(cliente.identidad_cache(), agente, modelo, system, texto_u, herramientas,
                           esquema, max_tokens) if self.cache else None
        # Replay debe consultar siempre su cinta (o grabar la respuesta de la base).
        if self.cache is not None and clave and not isinstance(cliente, ReplayClient):
            previo = self.cache.obtener(clave)
            if previo is not None and not contenido_sensible(previo) and not errores_esquema(previo, esquema):
                self.contabilidad.registrar(run_id, agente, modelo, Uso(), clase, fase, cache_hit=True)
                return ResultadoAgente(agente, previo, "COMPLETO", 0.0, 0, [], True)
        mensajes = [{"role": "user", "content": texto_u}]
        errores: list[str] = []
        uc_total = 0.0
        uso_total = Uso()
        reintentos = int(parametro(self.cfg, "llm.reintento_reparacion"))
        t0 = self.monitor.inicio(agente) if self.monitor else None
        if self.monitor:
            self.monitor.encolar(agente)
        try:
            for intento in range(reintentos + 1):
                mt = max_tokens
                if guarda is not None:
                    mt = guarda.reservar(system, mensajes, herramientas, max_tokens)
                    if mt is None:
                        if intento == 0:   # no ha salido ninguna petición: la fase se cierra declarada (Bloque._invocar)
                            return ResultadoAgente(agente, None, "SIN_PRESUPUESTO", errores=[guarda.negada])
                        errores = [guarda.negada]
                        break
                t_llamada = time.perf_counter()
                with con_guarda(guarda):
                    r = cliente.generar(agente=agente, modelo=modelo, system=system, mensajes=mensajes,
                                        max_tokens=mt, herramientas=herramientas, esquema=esquema)
                latencia = time.perf_counter() - t_llamada
                if guarda is not None:
                    guarda.pagar_resto(r.uso)
                r = respuesta_segura(r)
                uso_total.sumar(r.uso)
                uc_total += self.contabilidad.registrar(run_id, agente, modelo, r.uso, clase, fase, intento=intento + 1,
                                                        latencia_s=latencia)
                if r.rechazo or r.stop_reason in ("refusal", "pause_turn", "error_proveedor", "contenido_sensible", "presupuesto_agotado"):
                    errores = [f"turno no utilizable ({r.stop_reason})"]
                    break
                try:
                    datos = extraer_json(r.texto)
                    errores = errores_esquema(datos, esquema)
                    if r.truncada or r.stop_reason == "max_tokens":
                        errores.append("respuesta truncada por max_tokens")
                except (json.JSONDecodeError, ValueError, RecursionError) as e:   # T-146 r02 (H-05): también si no se puede
                    datos, errores = None, [f"JSON no válido: {e}"[:200]]       # validar por lo anidado (falla cerrado)
                try:
                    con_credenciales = datos is not None and bool(contiene_credenciales(datos))
                except RecursionError:   # T-146 r02 (H-05): demasiado anidado para comprobarlo: falla cerrado
                    con_credenciales = True
                if con_credenciales:
                    errores = ["respuesta bloqueada por R8"]
                    break
                if not errores:
                    if self.cache is not None and clave:
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
        self.almacen.incidencia("OTRO", f"Salida no conforme de {agente} ({NOMBRES[agente]}) tras {intento + 1} intento(s): "
                                + "; ".join(errores)[:500], agente, severidad="Operativa",
                                tratamiento="estado PARCIAL declarado; la fase continúa con alcance reducido", run_id=run_id)
        return ResultadoAgente(agente, None, "PARCIAL", uc_total, intento + 1, errores, False, uso_total)
