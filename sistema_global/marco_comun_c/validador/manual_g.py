"""CT-G-14 — registro de ejecución manual (operador → G). Código de referencia V0.1, determinista, sin LLM.

En L1 el operador ejecuta él mismo la orden que el robot preparó, o hace algo fuera del sistema. Lo declara con
un registro CT-G-14. Lo declarado no cuenta como discrepancia en la conciliación; lo no declarado sí
(Constitución §6 y §8). Reglas RM-01 a RM-09:

RM-01 forma: campos, tipos y valores cerrados.
RM-02 emisor: solo el operador.
RM-03 instantes: ejecutado_en <= emitido_en <= ahora, y no más antiguo que la ventana de declaración.
RM-04 vínculo inexistente o en un estado que no admite el registro.
RM-05 no coincide con lo que vincula (cartera, instrumento, activo base o sentido).
RM-06 cantidad: supera lo aprobado por F (expediente) o no es la de la posición (cierre total).
RM-07 un registro que abre posición exige su orden de protección declarada.
RM-08 instrumento no admitido en esa cartera (lista de la configuración, si la hay).
RM-09 precio de una entrada fuera de la tolerancia del límite autorizado.
RM-10 operación LIBRE en un instrumento con posición abierta o expediente AUTORIZADA: debe vincularse a ellos.
"""
from __future__ import annotations

import math
import re
from datetime import timedelta

from validar_sobre import _dt

CONTRATO, VERSION = "CT-G-14", "0.1.0"
ID = re.compile(r"^[A-Za-z0-9._:/-]{1,64}\Z")
FH = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z")
CARTERAS = ("TRADING", "TACTICA", "LARGO_PLAZO")
CAMPOS = {"contrato", "version", "event_id", "producer", "emitido_en", "ejecutado_en", "cartera", "instrumento", "activo_base",
          "lado", "cantidad", "precio", "ref_intermediario", "motivo", "vinculo", "proteccion_ref", "comision_eur"}
OBLIGATORIOS = CAMPOS - {"proteccion_ref", "comision_eur"}
VENTANA_DECLARACION_H = 72   # [PROPUESTO] lo no declarado en 72 h es discrepancia; un registro más antiguo se rechaza


def _num(x, minimo=None, estricto=True):
    if not (isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)):
        return False
    return minimo is None or (x > minimo if estricto else x >= minimo)


def _f(regla, mensaje):
    return {"regla": regla, "mensaje": mensaje}


def validar_manual(reg, ctx):
    """ctx: {"ahora", "expediente": dict|None, "posicion": dict|None, "tolerancia_precio": número,
    "instrumentos_permitidos": {cartera: [..]} opcional}. Devuelve la lista de fallos (vacía = válido)."""
    if not isinstance(reg, dict):
        return [_f("RM-01", "el registro no es un objeto")]
    fallos = []
    extra, falta = set(reg) - CAMPOS, OBLIGATORIOS - set(reg)
    if extra or falta:
        return [_f("RM-01", f"campos de más {sorted(extra)} o de menos {sorted(falta)}")]
    v = reg["vinculo"]
    forma = (reg["contrato"] == CONTRATO and reg["version"] == VERSION
             and all(isinstance(reg[k], str) and ID.match(reg[k]) for k in ("event_id", "ref_intermediario", "instrumento", "activo_base"))
             and all(isinstance(reg[k], str) and FH.match(reg[k]) for k in ("emitido_en", "ejecutado_en"))
             and reg["cartera"] in CARTERAS and reg["lado"] in ("COMPRA", "VENTA")
             and _num(reg["cantidad"], 0) and _num(reg["precio"], 0)
             and isinstance(reg["motivo"], str) and 3 <= len(reg["motivo"].strip()) <= 500
             and isinstance(v, dict) and set(v) == {"tipo", "id"} and v["tipo"] in ("EXPEDIENTE", "POSICION", "LIBRE")
             and (v["id"] is None if v["tipo"] == "LIBRE" else isinstance(v["id"], str) and ID.match(v["id"]))
             and ("proteccion_ref" not in reg or isinstance(reg["proteccion_ref"], str) and ID.match(reg["proteccion_ref"]))
             and ("comision_eur" not in reg or _num(reg["comision_eur"], 0, estricto=False)))
    if not forma:
        return [_f("RM-01", "forma inválida: contrato, versión, identificadores, instantes, valores cerrados o números")]
    if reg["producer"] != "OPERADOR":
        fallos.append(_f("RM-02", "solo el operador declara ejecuciones manuales"))
    ahora = ctx["ahora"]
    ej, em = _dt(reg["ejecutado_en"]), _dt(reg["emitido_en"])
    if not (ej <= em <= _dt(ahora)) or _dt(ahora) - ej > timedelta(hours=VENTANA_DECLARACION_H):
        fallos.append(_f("RM-03", f"instantes incoherentes o declaración fuera de la ventana de {VENTANA_DECLARACION_H} h"))
    elif ctx.get("no_antes_de") and ej < _dt(ctx["no_antes_de"]):
        fallos.append(_f("RM-03", "la ejecución es anterior a la autorización del expediente o a la apertura de la posición"))
    if reg.get("proteccion_ref") == reg["ref_intermediario"]:
        fallos.append(_f("RM-01", "la orden ejecutada y la de protección no pueden ser la misma"))
    perm = (ctx.get("instrumentos_permitidos") or {}).get(reg["cartera"])
    if perm is not None and reg["instrumento"] not in perm:
        fallos.append(_f("RM-08", "instrumento no admitido en esa cartera"))
    if v["tipo"] == "EXPEDIENTE":
        e = ctx.get("expediente")
        if e is None or e.get("estado") != "AUTORIZADA":
            return fallos + [_f("RM-04", "el expediente no existe o no está AUTORIZADA")]
        ent = e["propuesta"]["entrada"]
        stop = next(c for c in e["propuesta"]["salida"]["condiciones"] if c["tipo"] == "STOP")
        lado = "COMPRA" if stop["operador"] in ("<", "<=") else "VENTA"
        if (reg["cartera"], reg["instrumento"], reg["activo_base"], reg["lado"]) != (e["cartera_destino"], ent["instrumento"], ent["activo_base"], lado):
            fallos.append(_f("RM-05", "cartera, instrumento, activo base o sentido distintos de la propuesta autorizada"))
        if reg["cantidad"] > e["control_f"]["cantidad_aprobada"]:
            fallos.append(_f("RM-06", "la cantidad supera la aprobada por F"))
        if "proteccion_ref" not in reg:
            fallos.append(_f("RM-07", "una entrada exige declarar su orden de protección en el intermediario"))
        if abs(reg["precio"] - ent["limite"]) > ctx["tolerancia_precio"] * abs(ent["limite"]):
            fallos.append(_f("RM-09", "el precio se aleja del límite autorizado más de la tolerancia"))
    elif v["tipo"] == "POSICION":
        p = ctx.get("posicion")
        if p is None or p.get("estado") not in ("ABIERTA", "EN_REVISION", "REDUCIENDO"):
            return fallos + [_f("RM-04", "la posición no existe o no está ABIERTA, EN_REVISION ni REDUCIENDO")]
        lado = "VENTA" if p["direccion"] == "LARGO" else "COMPRA"
        if (reg["cartera"], reg["instrumento"], reg["activo_base"], reg["lado"]) != (p["cartera"], p["instrumento"], p["activo_base"], lado):
            fallos.append(_f("RM-05", "cartera, instrumento, activo base o sentido no cierran esa posición"))
        red = p.get("reduccion") if p.get("estado") == "REDUCIENDO" else None
        if red:   # a media reducción queda entre lo que la reducción deja y lo que había; G comprueba que el intermediario queda plano
            if not (red["objetivo_restante"] - 1e-6 <= reg["cantidad"] <= p["cantidad"] + 1e-6):
                fallos.append(_f("RM-06", "a media reducción el cierre manual debe ser de lo que queda en el intermediario"))
        elif abs(reg["cantidad"] - p["cantidad"]) > 1e-6:
            fallos.append(_f("RM-06", "el cierre manual debe ser total (una reducción parcial la hace G con reducir; declararla a mano no está implementado)"))
    else:
        if "proteccion_ref" in reg:
            fallos.append(_f("RM-01", "un registro LIBRE no lleva orden de protección"))
        if ctx.get("instrumento_ocupado"):
            fallos.append(_f("RM-10", "hay una posición abierta o un expediente autorizado en ese instrumento: vincule el registro a ellos"))
    return fallos


def neto_libre(manuales, instrumento):
    """Cantidad neta (con signo) de las operaciones LIBRES declaradas en un instrumento."""
    return sum((r["cantidad"] if r["lado"] == "COMPRA" else -r["cantidad"]) for r in manuales
               if r["vinculo"]["tipo"] == "LIBRE" and r["instrumento"] == instrumento)
