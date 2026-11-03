"""Invocación de los 24 agentes: system prompt íntegro + interfaz, mensaje de usuario con el contrato, cliente LLM
(simulado, Anthropic o de repetición), extracción y validación de la respuesta JSON con un reintento de reparación,
registro de consumo (tokens → UC) y de incidencias. Un agente que no responde conforme deja el resultado PARCIAL:
el orquestador degrada de forma declarada (nunca inventa)."""
from __future__ import annotations

import json
import threading
import time
from dataclasses import asdict
from typing import Dict, List, Optional

from .configuracion import max_tokens_de, modelo_de
from .contratos import extraer_json, sanear, validar_minimo
from .llm import LLMClient, Uso, herramienta_busqueda_web
from .prompts import CatalogoPrompts, mensaje_usuario


def uc_de_uso(u: Uso, cfg: Dict) -> float:
    c = cfg.get("uc") or {}
    entrada = u.entrada + u.cache_escritura + float(c.get("peso_lectura_cache", 0.1)) * u.cache_lectura
    return round(0.5 * entrada / float(c.get("tokens_entrada", 8000)) + 0.5 * u.salida / float(c.get("tokens_salida", 1500)), 4)


class Invocador:
    def __init__(self, cfg: Dict, cliente: LLMClient, prompts: CatalogoPrompts, almacen=None, modo: str = "vivo") -> None:
        self.cfg = cfg
        self.cliente = cliente
        self.prompts = prompts
        self.alm = almacen
        self.modo = modo
        self._lock = threading.Lock()
        self.registro: List[Dict] = []           # una fila por llamada (consumo.csv)
        self.uc_total = 0.0
        self.incidencias_r12: List[str] = []

    def llamar(self, agente: str, contrato: str, tarea: str, mensaje: Dict, instrucciones: str, requeridos: Dict[str, str],
               contexto: Optional[Dict] = None, run_id: Optional[str] = None, busqueda: bool = False) -> Dict:
        ctx = dict(contexto or {})
        ctx.setdefault("modo", self.modo)
        msg = sanear(dict(mensaje, tarea=tarea), self.incidencias_r12)
        esquema = {"type": "object", "required": list(requeridos),
                   "properties": {k: {"type": v} for k, v in requeridos.items()}}
        texto = mensaje_usuario(contrato, msg, ctx, instrucciones, esquema)
        system = self.prompts.system(agente, (self.cfg.get("llm") or {}).get("cache_ttl", "1h"))
        herramientas = None
        bw = (self.cfg.get("llm") or {}).get("busqueda_web") or {}
        if busqueda and self.modo == "vivo" and bw.get("activa_en_vivo") and agente in (bw.get("agentes") or []) \
                and self.cliente.nombre == "anthropic":
            herramientas = [herramienta_busqueda_web(bw.get("tipo", "web_search_20260318"), bw.get("max_usos", 5))]
        mensajes = [{"role": "user", "content": texto}]
        uso = Uso()
        datos: Optional[Dict] = None
        errores: List[str] = []
        t0 = time.perf_counter()
        for intento in range(2):
            r = self.cliente.generar(agente=agente, modelo=modelo_de(self.cfg, agente), system=system, mensajes=mensajes,
                                     max_tokens=max_tokens_de(self.cfg, agente), herramientas=herramientas)
            uso.sumar(r.uso)
            datos = extraer_json(r.texto)
            ok, errores = validar_minimo(datos, esquema) if datos is not None else (False, ["respuesta no es JSON"])
            if ok:
                break
            mensajes = mensajes + [{"role": "assistant", "content": r.texto[:4000]},
                                   {"role": "user", "content": "Tu respuesta no cumple el esquema (" + "; ".join(errores)
                                    + "). Devuelve SOLO el objeto JSON corregido."}]
            datos = None
        uc = uc_de_uso(uso, self.cfg)
        with self._lock:
            self.uc_total += uc
            self.registro.append({"run_id": run_id, "agente": agente, "contrato": contrato, "tarea": tarea, **asdict(uso),
                                  "uc": uc, "segundos": round(time.perf_counter() - t0, 3), "conforme": datos is not None})
        if datos is None:
            if self.alm is not None:
                self.alm.incidencia("RESPUESTA_NO_CONFORME", f"{agente} ({contrato}, {tarea}): {'; '.join(errores)[:300]}",
                                    agente, severidad="Operativa", run_id=run_id)
            return {"estado": "PARCIAL", "_no_conforme": True}
        datos.setdefault("estado", "COMPLETO")
        return datos

    def consumo(self, run_id: Optional[str] = None) -> Dict:
        filas = [r for r in self.registro if run_id is None or r["run_id"] == run_id]
        tot = {k: sum(r[k] for r in filas) for k in ("entrada", "salida", "cache_escritura", "cache_lectura", "busquedas_web")}
        tot["uc"] = round(sum(r["uc"] for r in filas), 3)
        tot["llamadas"] = len(filas)
        return tot
