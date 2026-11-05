"""Contratos CT-G como esquemas (T-25): validación de cualquier mensaje por su tipo y versión, y construcción de los mensajes
que el sistema produce a partir del estado real del Orquestador.

Reglas: CT-01 forma (no es un objeto o le falta tipo y versión); CT-02 contrato pendiente o versión sin esquema;
CT-03 no cumple el esquema (ruta y motivo); CT-04 la envoltura no es coherente (valid_until anterior a emitido_en).
Nunca lanza excepciones.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import date
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator

from validar_sobre import _dt

ESQUEMAS = Path(__file__).resolve().parent.parent / "esquemas"


def _hash(x) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


@lru_cache(maxsize=1)
def registro():
    return json.loads((ESQUEMAS / "registro_contratos.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=32)
def _validador(fichero):
    return Draft202012Validator(json.loads((ESQUEMAS / fichero).read_text(encoding="utf-8")))


def _f(regla, ruta, mensaje):
    return {"regla": regla, "ruta": ruta, "mensaje": mensaje}


def validar(msg) -> list[dict]:
    try:
        return _validar(msg)
    except Exception as e:   # noqa: BLE001 - un mensaje mal formado nunca rompe al que valida
        return [_f("CT-01", "(interno)", f"{type(e).__name__}")]


def _validar(msg):
    if not isinstance(msg, dict):
        return [_f("CT-01", "", "el mensaje no es un objeto")]
    tipo = msg.get("tipo_mensaje", msg.get("contrato"))
    version = msg.get("version_esquema", msg.get("version"))
    if not (isinstance(tipo, str) and isinstance(version, str)):
        return [_f("CT-01", "tipo_mensaje", "falta el tipo de mensaje o su versión")]
    c = next((x for x in registro()["contratos"] if x["tipo"] == tipo), None)
    if c is None:
        return [_f("CT-02", "tipo_mensaje", f"contrato desconocido: {tipo}")]
    if c["estado"] != "ESQUEMA":
        return [_f("CT-02", "tipo_mensaje", f"{tipo} está pendiente: {c['motivo']}")]
    if c["version"] != version:
        return [_f("CT-02", "version_esquema", f"{tipo} no tiene esquema para la versión {version} (vigente {c['version']})")]
    fallos = [_f("CT-03", "/".join(str(p) for p in e.absolute_path), e.message[:200])
              for e in sorted(_validador(c["esquema"]).iter_errors(msg), key=lambda e: [str(p) for p in e.absolute_path])]
    fallos += _fechas_imposibles(msg, "")   # el esquema solo mira los dígitos: 30 de febrero o 25:61 no son fechas
    if not fallos and msg.get("valid_until") and _dt(msg["valid_until"]) < _dt(msg["emitido_en"]):
        fallos.append(_f("CT-04", "valid_until", "vence antes de emitirse"))
    return fallos


_FH = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z")
_FE = re.compile(r"^\d{4}-\d{2}-\d{2}\Z")


def _fechas_imposibles(x, ruta):
    out = []
    if isinstance(x, dict):
        for k, v in x.items():
            out += _fechas_imposibles(v, f"{ruta}/{k}" if ruta else str(k))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            out += _fechas_imposibles(v, f"{ruta}/{i}")
    elif isinstance(x, str) and (_FH.match(x) or _FE.match(x)):
        try:
            _dt(x) if _FH.match(x) else date.fromisoformat(x)
        except (ValueError, OverflowError):
            out.append(_f("CT-03", ruta, f"fecha imposible: {x!r}"))
    return out


# ------------------------------------------------------------------ mensajes a partir del estado del Orquestador
def _env(tipo, producer, consumer, emitido_en, payload, correlation_id=None, expediente_id=None, valid_until=None, data_refs=()):
    m = {"event_id": None, "correlation_id": correlation_id, "expediente_id": expediente_id, "producer": producer, "consumer": consumer,
         "tipo_mensaje": tipo, "version_esquema": "0.1.0", "emitido_en": emitido_en, "valid_until": valid_until,
         "data_refs": list(data_refs), "payload": payload}
    m["event_id"] = f"{tipo}-{_hash(m)[:16]}"   # determinista: el mismo contenido da el mismo id
    return m


def peticion_comparacion(o, expediente_ids, actor, ahora):
    """CT-G-04: lo que se pide comparar (con los testigos que el Orquestador añadirá, T-36)."""
    exps = [o.expedientes[x] for x in expediente_ids]
    cartera = exps[0]["cartera_destino"]
    testigos = [x["expediente_id"] for x in o._testigos(cartera, _dt(ahora), set(expediente_ids))]
    vence = min((x["sobre"]["valid_until"] for x in exps if x.get("sobre")), key=_dt, default=ahora)   # vale lo que vale el primer sobre
    return _env("CT-G-04", actor, "D", ahora, {"cartera": cartera, "expedientes": list(expediente_ids),
                                                  "referencia": copy.deepcopy(o.cfg["referencias"][cartera]), "testigos": testigos},
                valid_until=vence, data_refs=[x["sobre"]["event_id"] for x in exps if x.get("sobre")])


def comparativa(o, cartera, consumer="ORQUESTADOR"):
    """CT-G-05: la comparación vigente de la cartera, tal como la anotó el Orquestador."""
    cid = o.ultima_comparacion.get(cartera)
    exps = sorted((x for x in o.expedientes.values() if (x.get("comparacion") or {}).get("id") == cid and x.get("sobre")),
                  key=lambda x: x["expediente_id"])
    if not exps:
        return None
    c0 = exps[0]["comparacion"]
    cand = [{"expediente_id": x["expediente_id"], "ganador": x["comparacion"]["ganador"], "aspirante": x["comparacion"]["aspirante"],
             "excluido": x["comparacion"]["excluido"], "decision": x["comparacion"]["decision"], "sensible": x["comparacion"]["sensible"],
             "elegido_por_operador": x["comparacion"]["elegido_por_operador"] is not None, "detalle_d": x["comparacion"]["detalle_d"]}
            for x in exps]
    ultima = max((h for x in exps for h in x["historial"] if h["ref"] == cid and h["hasta"] == "COMPARADA" and h["actor"] == "D"),
                 key=lambda h: _dt(h["ahora"]))   # la hora de D, no la de una elección posterior del operador
    vence = min((x["sobre"]["valid_until"] for x in exps), key=_dt)
    return _env("CT-G-05", "D", consumer, ultima["ahora"],
                {"comparacion_id": cid, "cartera": cartera, "codigo_d": c0["codigo_d"], "decision_global": c0["decision_global"],
                 "referencia": c0["referencia"], "candidatos": cand, "testigos": c0.get("testigos", []),
                 "apartado_mejor": c0.get("apartado_mejor"), "ganador": next((x["expediente_id"] for x in exps if x["comparacion"]["ganador"]), None)},
                valid_until=vence, data_refs=[x["sobre"]["event_id"] for x in exps])


def propuesta(o, expediente_id):
    """CT-G-06: la propuesta registrada del expediente."""
    e = o.expedientes[expediente_id]
    p = e["propuesta"]
    if not p or e["estado"] not in ("PROPUESTA", "AUTORIZADA", "EJECUTADA"):
        return None   # solo una propuesta en vigor
    h = next(x for x in reversed(e["historial"]) if x["hasta"] == "PROPUESTA")
    return _env("CT-G-06", h["actor"], "E", h["ahora"],
                {"cartera": e["cartera_destino"], "entrada": copy.deepcopy(p["entrada"]), "salida": copy.deepcopy(p["salida"]),
                 "cantidad_e": p["cantidad_e"], "sobre_ref": {"event_id": e["sobre"]["event_id"], "hash": e["sobre"]["hash"]},
                 "comparacion_id": e["comparacion"]["id"]},
                correlation_id=e["correlation_id"], expediente_id=expediente_id, valid_until=p["entrada"]["ventana_hasta"],
                data_refs=[e["sobre"]["event_id"]])


def orden(o, expediente_id):
    """CT-G-09: la orden que G debe enviar por un expediente AUTORIZADA, con su protección."""
    e = o.expedientes[expediente_id]
    if e["estado"] != "AUTORIZADA" or not e.get("control_f"):
        return None   # solo hay orden para un expediente autorizado y aún sin ejecutar
    en, cf = e["propuesta"]["entrada"], e["control_f"]
    st = next(c for c in e["propuesta"]["salida"]["condiciones"] if c["tipo"] == "STOP")
    largo = st["operador"] in ("<", "<=")
    h = next(x for x in reversed(e["historial"]) if x["hasta"] == "AUTORIZADA" and x["desde"] != "AUTORIZADA")
    hasta = min(_dt(en["ventana_hasta"]), _dt(e["sobre"]["valid_until"]), _dt(cf["valid_until"])).isoformat()
    return _env("CT-G-09", "ORQUESTADOR", "G", h["ahora"],
                {"cartera": e["cartera_destino"], "instrumento": en["instrumento"], "activo_base": en["activo_base"], "via_acceso": en["via_acceso"],
                 "lado": "COMPRA" if largo else "VENTA", "tipo": "LIMITE", "cantidad": cf["cantidad_aprobada"], "precio_limite": en["limite"],
                 "valida_hasta": hasta, "proteccion": {"tipo": "STOP", "precio": st["umbral"], "solo_reduccion": True},
                 "control_f_ref": {"event_id": cf["event_id"], "hash": _hash(cf)}, "autorizada_por": h["actor"]},
                correlation_id=e["correlation_id"], expediente_id=expediente_id, valid_until=hasta, data_refs=[cf["event_id"]])


def alertas_posicion(o, posicion_id):
    """CT-G-10: las alertas que H dejó sobre una posición (cierre o reducción preparados, revisión)."""
    p = o.posiciones[posicion_id]
    e = o.expedientes.get(p["expediente_id"], {})
    out = []
    for x in p["propuestas"]:
        if x["actor"] != "H":
            continue   # CT-G-10 es de H; lo que proponga otro no se presenta como alerta de H
        t = x["texto"]
        tipo = ("CIERRE_PREPARADO" if t.startswith("CIERRE PREPARADO") else "REDUCCION_PREPARADA" if t.startswith("REDUCCIÓN PREPARADA")
                else "REVISION" if t.startswith("REVISIÓN") else "OTRA")
        out.append(_env("CT-G-10", "H", f"GESTOR_{p['cartera']}", x["ahora"],
                        {"posicion_id": posicion_id, "cartera": p["cartera"], "estado_posicion": p["estado"], "tipo": tipo, "texto": t},
                        correlation_id=e.get("correlation_id"), expediente_id=p["expediente_id"], valid_until=x["ahora"]))
    return out


def aviso(o, aviso_id):
    """CT-G-16: un aviso del Orquestador al operador."""
    a = next(x for x in o.avisos if x["id"] == aviso_id)
    return _env("CT-G-16", "ORQUESTADOR", "OPERADOR", a["ahora"],
                {"aviso_id": a["id"], "codigo": a["codigo"], "prioridad": a["prioridad"], "motivo": a["motivo"], "ref": a["ref"],
                 "carteras": a.get("carteras"), "canal": a["canal"], "acuse": a["acuse"], "reiteraciones": len(a["reiteraciones"]),
                 "escalado": a["escalado"]},
                correlation_id=o.expedientes[a["ref"]]["correlation_id"] if a["ref"] in o.expedientes else None,
                expediente_id=a["ref"] if a["ref"] in o.expedientes else None)
