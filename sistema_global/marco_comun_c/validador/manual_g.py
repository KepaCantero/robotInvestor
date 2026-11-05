"""CT-G-14 — registro de ejecución manual (operador → G). Código de referencia V0.1, determinista, sin LLM.

En L1 el operador ejecuta él mismo la orden que el robot preparó, o hace algo fuera del sistema. Lo declara con
un registro CT-G-14. Lo declarado no cuenta como discrepancia en la conciliación; lo no declarado sí
(Constitución §6 y §8). Reglas RM-01 a RM-09:

RM-01 forma: campos, tipos y valores cerrados.
RM-02 emisor: solo el operador.
RM-03 instantes: ejecutado_en <= emitido_en <= ahora, y no más antiguo que la ventana de declaración.
RM-04 vínculo inexistente o en un estado que no admite el registro.
RM-05 no coincide con lo que vincula (cartera, instrumento, activo base, sentido o vía de acceso).
RM-06 cantidad: supera lo aprobado por F (expediente) o no es la de la posición (cierre total).
RM-07 un registro que abre posición exige su orden de protección declarada.
RM-08 instrumento no admitido en esa cartera (lista de la configuración, si la hay).
RM-09 precio de una entrada fuera de la tolerancia del límite autorizado.
RM-10 operación LIBRE en un instrumento con posición abierta o expediente AUTORIZADA: debe vincularse a ellos.
RM-11 la identidad de la envoltura (expediente_id, correlation_id) no es la del vínculo (T-47).

Desde T-47 el mensaje es CT-G-14 0.2.0 con la envoltura común: producer OPERADOR, consumer G, valid_until nulo (un hecho
declarado no caduca; la ventana la aplica RM-03), data_refs = las órdenes del intermediario que lo prueban, y en payload los
campos de la operación. `aplanar_manual` lo pasa a la forma plana que usan el Orquestador, G y la conciliación. La 0.1.0
(contrato/version, sin envoltura) está retirada: RM-01.
"""
from __future__ import annotations

import math
import re
from datetime import timedelta

from validar_sobre import _dt

CONTRATO, VERSION = "CT-G-14", "0.2.0"
ID = re.compile(r"^[A-Za-z0-9._:/-]{1,64}\Z")
FH = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})\Z")
CARTERAS = ("TRADING", "TACTICA", "LARGO_PLAZO")
ENVOLTURA = ("event_id", "correlation_id", "expediente_id", "producer", "consumer", "tipo_mensaje", "version_esquema", "emitido_en",
             "valid_until", "data_refs", "payload")
PAYLOAD = {"ejecutado_en", "cartera", "instrumento", "activo_base", "lado", "cantidad", "precio", "ref_intermediario", "motivo", "vinculo",
           "proteccion_ref", "comision_eur", "via_acceso"}
PAYLOAD_OBLIGATORIOS = PAYLOAD - {"proteccion_ref", "comision_eur", "via_acceso"}   # la vía es obligatoria salvo en una operación LIBRE (RM-05)
# forma interna plana (la que guarda el Orquestador en `manuales`); no es un mensaje
CAMPOS = PAYLOAD | {"tipo_mensaje", "version_esquema", "event_id", "correlation_id", "expediente_id", "producer", "consumer", "emitido_en"}
OBLIGATORIOS = CAMPOS - {"proteccion_ref", "comision_eur", "via_acceso"}
from parametros import PARAMETROS as _P   # noqa: E402
VENTANA_DECLARACION_H = _P["manual_ventana_declaracion_horas"]   # [PROPUESTO] lo no declarado en 72 h es discrepancia; un registro más antiguo se rechaza


def _num(x, minimo=None, estricto=True):
    if not (isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)):
        return False
    return minimo is None or (x > minimo if estricto else x >= minimo)


def via_norm(x):
    """Identidad de una vía de acceso: sin distinguir mayúsculas ni espacios repetidos (la misma que el Orquestador y R-14)."""
    return " ".join(x.split()).casefold() if isinstance(x, str) and x.strip() else None


def _f(regla, mensaje):
    return {"regla": regla, "mensaje": mensaje}


def envolver_manual(campos, event_id, emitido_en, expediente_id=None, correlation_id=None, producer="OPERADOR"):
    """CT-G-14 0.2.0 a partir de los campos de la operación (los del payload). Lo usa la consola del operador
    (contratos.registro_manual deduce la identidad del vínculo con el estado del Orquestador)."""
    pl = dict(campos)
    refs = [pl.get("ref_intermediario")] + ([pl["proteccion_ref"]] if "proteccion_ref" in pl else [])
    return {"event_id": event_id, "correlation_id": correlation_id, "expediente_id": expediente_id, "producer": producer, "consumer": "G",
            "tipo_mensaje": CONTRATO, "version_esquema": VERSION, "emitido_en": emitido_en, "valid_until": None, "data_refs": refs, "payload": pl}


def _envoltura_ok(reg):
    pl = reg.get("payload")
    return (set(reg) == set(ENVOLTURA) and reg["tipo_mensaje"] == CONTRATO and reg["version_esquema"] == VERSION
            and reg["consumer"] == "G" and reg["valid_until"] is None
            and all(reg[k] is None or isinstance(reg[k], str) and ID.match(reg[k]) for k in ("correlation_id", "expediente_id"))
            and isinstance(pl, dict) and not (set(pl) - PAYLOAD) and not (PAYLOAD_OBLIGATORIOS - set(pl))
            and isinstance(reg["data_refs"], list)
            and reg["data_refs"] == [pl["ref_intermediario"]] + ([pl["proteccion_ref"]] if "proteccion_ref" in pl else []))


def aplanar_manual(reg):
    """Del mensaje CT-G-14 0.2.0 a la forma interna plana. None si no tiene exactamente la forma de la envoltura (no lanza)."""
    try:
        if not (isinstance(reg, dict) and _envoltura_ok(reg)):
            return None
        return {**{k: reg[k] for k in ENVOLTURA if k not in ("payload", "data_refs", "valid_until")}, **reg["payload"]}
    except (TypeError, KeyError, AttributeError, ValueError, RecursionError):
        return None


MOTIVO = re.compile(r"\S[\s\S]*\S[\s\S]*\S")   # al menos 3 caracteres que no son espacio; la misma regla que el esquema
MOTIVO_MAX = 500


def motivo_ok(m):
    return isinstance(m, str) and len(m) <= MOTIVO_MAX and MOTIVO.search(m) is not None


def _fh(x):
    """Instante con el formato y además real (no 30 de febrero ni desfase +25:00)."""
    if not (isinstance(x, str) and FH.match(x)):
        return False
    try:
        _dt(x)
        return True
    except (ValueError, OverflowError):
        return False


def validar_manual(reg, ctx):
    """Nunca lanza: cualquier fallo de cálculo es RM-01 (falla cerrado)."""
    try:
        return _validar_manual(reg, ctx)
    except Exception as e:   # noqa: BLE001
        return [_f("RM-01", f"entrada o contexto mal formado: {type(e).__name__}")]


def _validar_manual(reg, ctx):
    """reg: el mensaje CT-G-14 0.2.0. ctx: {"ahora", "expediente": dict|None, "posicion": dict|None, "tolerancia_precio": número,
    "instrumentos_permitidos": {cartera: [..]} opcional, "identidad": (expediente_id, correlation_id) que corresponde al vínculo}.
    Devuelve la lista de fallos (vacía = válido)."""
    if not isinstance(reg, dict):
        return [_f("RM-01", "el registro no es un objeto")]
    if reg.get("version_esquema", reg.get("version")) != VERSION:
        return [_f("RM-01", f"versión de CT-G-14 no admitida (vigente {VERSION}; la 0.1.0 sin envoltura común está retirada)")]
    plano = aplanar_manual(reg)
    if plano is None:
        return [_f("RM-01", "envoltura inválida: campos, consumer G, valid_until nulo, payload o data_refs (las órdenes del payload)")]
    fallos = _validar_plano(plano, ctx)
    if not any(x["regla"] == "RM-01" for x in fallos):
        v = plano["vinculo"]
        esperada = (None, None) if v["tipo"] == "LIBRE" else ctx.get("identidad")
        if esperada is None:
            mal = not any(x["regla"] == "RM-04" for x in fallos)   # sin vínculo que exista no hay identidad que comparar (ya es RM-04)
        else:
            mal = (plano["expediente_id"], plano["correlation_id"]) != tuple(esperada)
        if mal:
            fallos.append(_f("RM-11", "la envoltura no identifica el caso del vínculo (expediente_id y correlation_id; nulos si es LIBRE)"))
    return fallos


def _validar_plano(reg, ctx):
    fallos = []
    v = reg["vinculo"]
    forma = (all(isinstance(reg[k], str) and ID.match(reg[k]) for k in ("event_id", "ref_intermediario", "instrumento", "activo_base"))
             and all(_fh(reg[k]) for k in ("emitido_en", "ejecutado_en"))
             and reg["cartera"] in CARTERAS and reg["lado"] in ("COMPRA", "VENTA")
             and _num(reg["cantidad"], 0) and _num(reg["precio"], 0)
             and motivo_ok(reg["motivo"])
             and isinstance(v, dict) and set(v) == {"tipo", "id"} and v["tipo"] in ("EXPEDIENTE", "POSICION", "LIBRE")
             and (v["id"] is None if v["tipo"] == "LIBRE" else isinstance(v["id"], str) and ID.match(v["id"]))
             and ("proteccion_ref" not in reg or isinstance(reg["proteccion_ref"], str) and ID.match(reg["proteccion_ref"]))
             and ("comision_eur" not in reg or _num(reg["comision_eur"], 0, estricto=False))
             and ("via_acceso" not in reg or isinstance(reg["via_acceso"], str) and reg["via_acceso"].strip()))
    if not forma:
        return [_f("RM-01", "forma inválida: identificadores, instantes, valores cerrados o números")]
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
        if via_norm(reg.get("via_acceso")) != via_norm(ent.get("via_acceso")):
            fallos.append(_f("RM-05", "la vía de acceso no es la de la propuesta autorizada (un futuro analizado no se opera como contado)"))
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
        if via_norm(reg.get("via_acceso")) != via_norm(p.get("via_acceso")):
            fallos.append(_f("RM-05", "la vía de acceso no es la de la posición"))
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
