"""H — vigilancia de posiciones (código de referencia V0.1).

H mira cada posición abierta contra los datos de mercado y contra el intermediario, y cuando una condición de salida
declarada de antemano se cumple, pide a G que cierre. Determinista, sin LLM. H no decide nada nuevo: solo aplica
las condiciones que la propuesta ya fijó. Ante un dato ausente o viejo no cierra: avisa.
Reglas: H-01 stop ejecutado por el intermediario; H-02 condición de salida cumplida; H-03 dato ausente o viejo;
H-04 cierre pendiente (CERRANDO) que se reintenta; H-05 stop cumplido sin que el intermediario lo ejecutara;
H-06 métrica no soportada; H-07 diferencias de conciliación; H-08 posición REDUCIENDO (no se vigila por precio);
H-09 instante sospechoso (no se hace nada).
"""
from __future__ import annotations

import math

import math as _m

from orquestador import NIVELES
from ejecucion_g import _aviso, _instante, cerrar, conciliar, revisar_entrada
from orquestador import OPERADORES
from validar_sobre import _dt

MAX_EDAD_MIN = 15   # [PROPUESTO]
SALTO_MAX_H = 72    # [PROPUESTO] más allá, el instante recibido se considera sospechoso


def _valor_cumplido(c, pm):
    """El valor con el que se declara cumplida la condición de un stop que el intermediario ya ejecutó: el precio real si la
    cumple y, si no (relleno mejor, redondeo, dato ausente), el umbral mismo o el valor más próximo que la cumple."""
    from orquestador import OPERADORES as OP
    u = c["umbral"]
    for v in (pm, u, _m.nextafter(u, -_m.inf), _m.nextafter(u, _m.inf)):
        if _num(v) and OP[c["operador"]](v, u):
            return v
    return u


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _dato_fresco(d, ahora, max_edad_min):
    try:
        if not (isinstance(d, dict) and _num(d.get("precio")) and d["precio"] > 0):
            return False
        edad = (_dt(ahora) - _dt(d["hora"])).total_seconds() / 60
        return 0 <= edad <= max_edad_min
    except Exception:   # noqa: BLE001
        return False


def vigilar(o, broker, datos, ahora, max_edad_min=MAX_EDAD_MIN):
    """datos: {instrumento: {"precio": número, "hora": ISO con zona}}. Devuelve las acciones y avisos de esta pasada."""
    try:
        if o.ultimo_ahora and (_dt(ahora) - _dt(o.ultimo_ahora)).total_seconds() > SALTO_MAX_H * 3600:
            return {"acciones": [{"posicion": None, "regla": "H-09", "ok": False, "codigo": "H-09"}], "no_evaluadas": [], "conciliacion_ok": False,
                    "motivo": "el instante recibido salta demasiado respecto al último que vio el Orquestador; no se hace nada"}
        ahora = _instante(o, ahora)
    except Exception:   # noqa: BLE001
        return {"acciones": [{"posicion": None, "regla": "H-09", "ok": False, "codigo": "H-09"}], "no_evaluadas": [], "conciliacion_ok": False,
                "motivo": "instante ilegible"}
    acciones, no_eval, hechos = [], [], set()
    # Órdenes de entrada vivas: si se ejecutaron se protegen y se reportan; si vencieron se cancelan (H-11)
    for eid in sorted(o.expedientes):
        x = o.expedientes[eid]
        if x["estado"] == "AUTORIZADA" and (x.get("orden_entrada") or {}).get("estado") in ("ENVIADA", "PARCIAL", "EJECUTADA"):
            r = revisar_entrada(o, eid, broker, ahora)
            acciones.append({"expediente": eid, "posicion": None, "regla": "H-11", "ok": r["ok"], "codigo": r["codigo"]})
    # Primera pasada: hechos consumados (cierres pendientes y stops que el intermediario ya ejecutó).
    for pid in sorted(o.posiciones):
        p = o.posiciones[pid]
        if p["estado"] == "CERRADA":
            continue
        if p["estado"] == "CERRANDO":
            r = cerrar(o, pid, broker, ahora)
            acciones.append({"posicion": pid, "regla": "H-04", "ok": r["ok"], "codigo": r["codigo"]})
            hechos.add(pid)
            continue
        try:
            ejec = [c for x in p["protecciones"] if (c := broker.consultar(x)) and c["estado"] in ("EJECUTADA", "PARCIAL")]
        except Exception:   # noqa: BLE001
            ejec = []
        if ejec:   # el intermediario ya ejecutó el stop: solo falta confirmar el cierre
            stop = next(c for c in o.posiciones[pid]["condiciones_salida"]["condiciones"] if c["tipo"] == "STOP")
            cond = {"id": stop["id"], "valor_observado": _valor_cumplido(stop, ejec[0]["precio_medio"]), "stop_ejecutado_orden_id": ejec[0]["orden_id"]}
            r = cerrar(o, pid, broker, ahora, condicion=cond)
            acciones.append({"posicion": pid, "regla": "H-01", "ok": r["ok"], "codigo": r["codigo"]})
            hechos.add(pid)
    # Conciliar antes de cualquier decisión: una diferencia degrada la cartera y el cierre automático ya no se hace
    conc = conciliar(o, broker, ahora)
    for pid in sorted(o.posiciones):
        p = o.posiciones[pid]
        if p["estado"] == "CERRADA" or pid in hechos:
            continue
        if p["estado"] == "REDUCIENDO":   # la reducción no está implementada: no se vigila por precio
            acciones.append({"posicion": pid, "regla": "H-08", "ok": False, "codigo": "H-08"})
            continue
        d = datos.get(p["instrumento"]) if isinstance(datos, dict) else None
        if not _dato_fresco(d, ahora, max_edad_min):
            o.degradar(p["cartera"], f"sin precio fresco de {p['instrumento']}", "H", _instante(o, ahora))
            reg = _aviso(o, [{"tipo": "DATO_VIEJO", "ref": pid, "detalle": f"sin precio fresco de {p['instrumento']}; no se vigila la posición"}], ahora)
            acciones.append({"posicion": pid, "regla": "H-03", "ok": False, "codigo": "H-03", "aviso_registrado": reg})
            continue
        for c in p["condiciones_salida"]["condiciones"]:
            if c["metrica"] != "precio":
                no_eval.append({"posicion": pid, "condicion": c["id"], "regla": "H-06"})
                continue
            if OPERADORES[c["operador"]](d["precio"], c["umbral"]):
                if NIVELES[o.nivel(p["cartera"])] < 2:   # L0/L1: H prepara el cierre y lo confirma el operador
                    txt = f"CIERRE PREPARADO: {c['id']} ({c['tipo']}) cumplida; confirme el cierre"
                    if not any(x["texto"] == txt for x in p["propuestas"]):
                        o.proponer_sobre_posicion(pid, txt, "H", _instante(o, ahora))
                    acciones.append({"posicion": pid, "regla": "H-10", "condicion": c["id"], "ok": False, "codigo": "H-10"})
                    break
                r = cerrar(o, pid, broker, ahora, condicion={"id": c["id"], "valor_observado": d["precio"]})
                acciones.append({"posicion": pid, "regla": "H-05" if c["tipo"] == "STOP" else "H-02", "condicion": c["id"],
                                 "ok": r["ok"], "codigo": r["codigo"]})
                break
    if not conc["ok"]:
        acciones.append({"posicion": None, "regla": "H-07", "ok": False, "codigo": "H-07", "diferencias": [d["tipo"] for d in conc["diferencias"]]})
    return {"acciones": acciones, "no_evaluadas": no_eval, "conciliacion_ok": conc["ok"]}
