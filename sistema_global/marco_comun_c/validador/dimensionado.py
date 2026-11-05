"""E — dimensionado de posición (código de referencia V0.1).

Dado el precio de entrada, el stop y el estado de la cartera, calcula la cantidad que arriesga el porcentaje objetivo
del capital sin superar ninguno de los topes de F, redondeada hacia abajo a un múltiplo del paso del instrumento.
Determinista, sin LLM. Los topes se obtienen de F (no se reescriben): lo que E propone, F lo aprueba salvo que algo
cambie. Códigos: OK; E-01 entrada inválida; E-02 el stop no protege; E-03 F vetaría la solicitud (por fondo); E-04 no hay cantidad
viable (por debajo del paso o del valor mínimo). `limitada_por` dice qué regla fijó la cantidad.
"""
from __future__ import annotations

import math
from fractions import Fraction

from control_f import controlar, politica_valida

def _num(x, estricto=True):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and (x > 0 if estricto else x >= 0)


def _r(ok, codigo, motivo, **extra):
    return {"ok": ok, "codigo": codigo, "motivo": motivo, "cantidad": 0.0, **extra}


def dimensionar(sol, cart, pol, ahora, riesgo_objetivo_pct=None, paso=1e-6):
    """sol: instrumento, activo_base, direccion, precio_entrada, stop_precio, apalancamiento, cartera (sin cantidad).
    Nunca lanza excepciones: cualquier fallo es E-01 con cantidad 0."""
    try:
        return _dimensionar(sol, cart, pol, ahora, riesgo_objetivo_pct, paso)
    except Exception as ex:   # noqa: BLE001
        return _r(False, "E-01", f"error de cálculo: {type(ex).__name__}")


def _dimensionar(sol, cart, pol, ahora, objetivo, paso):
    campos = {"instrumento", "activo_base", "direccion", "precio_entrada", "stop_precio", "apalancamiento", "cartera"}
    if not (isinstance(sol, dict) and set(sol) == campos):
        return _r(False, "E-01", "la solicitud debe llevar exactamente los campos exigidos y no una cantidad")
    if not politica_valida(pol):
        return _r(False, "E-01", "política inválida")
    if not (_num(sol["precio_entrada"]) and _num(sol["stop_precio"]) and _num(paso)):
        return _r(False, "E-01", "precios o paso inválidos")
    if objetivo is None:
        objetivo = pol["riesgo_max_pct"]
    if not (_num(objetivo) and objetivo <= pol["riesgo_max_pct"]):
        return _r(False, "E-01", "el riesgo objetivo debe ser positivo y no superar el máximo de la política")
    ent, stop = sol["precio_entrada"], sol["stop_precio"]
    if not (stop < ent if sol["direccion"] == "LARGO" else stop > ent if sol["direccion"] == "CORTO" else False):
        return _r(False, "E-02", "el stop debe estar del lado de la pérdida y la dirección ser LARGO o CORTO")
    # una cantidad de sonda mayor que cualquier tope: F-04, F-06 y F-07 no pueden pasar de capital/precio
    f = controlar({**sol, "cantidad": 10 * cart["capital_eur"] / ent}, cart, pol, ahora)
    if f["resultado"] == "VETADO":
        vetos = [c for c in f["controles"] if c["resultado"] == "VETA"]
        if any(c["regla"] == "F-01" for c in vetos):   # defecto de forma (cartera, fecha, política...), no un veto de fondo
            return _r(False, "E-01", "entrada rechazada por forma: " + (vetos[0]["motivo"] or "F-01"))
        if [c["regla"] for c in vetos] == ["F-11"]:   # solo el valor mínimo: no hay hueco, no es un veto de fondo
            return _r(False, "E-04", "no queda hueco en la cartera para una posición de valor mínimo", reglas=["F-11"])
        return _r(False, "E-03", "F vetaría la solicitud: " + ", ".join(c["regla"] for c in vetos) + (f" ({vetos[0]['motivo']})" if vetos and vetos[0]["motivo"] else ""),
                  reglas=[c["regla"] for c in vetos])
    topes = {c["regla"]: c["limite"] for c in f["controles"] if c["resultado"] == "REDUCE"}
    q_riesgo = objetivo / 100 * cart["capital_eur"] / abs(ent - stop)
    regla, q = min([("RIESGO_OBJETIVO", q_riesgo)] + sorted(topes.items()), key=lambda kv: kv[1])
    k = math.floor(q / paso * (1 + 1e-12))   # el ruido de la coma flotante no debe costar un paso; la comprobación exacta de abajo manda
    bajada = max(1, math.ceil(2e-6 / paso))   # F recorta a 1e-6: si una cantidad en el borde no pasa, se baja de paso en paso
    riesgo_max = Fraction(objetivo) / 100 * Fraction(cart["capital_eur"]) * (1 + Fraction(1, 10**14))   # tolerancia: ruido de la coma flotante de los precios
    dist = abs(Fraction(ent) - Fraction(stop))
    v = None
    for _ in range(25):
        if k <= 0:
            break
        q = k * paso
        if paso >= 1e-9:
            q = round(q, 12)
        if Fraction(q) * dist <= riesgo_max:   # aritmética exacta: nunca se supera el riesgo objetivo
            v = controlar({**sol, "cantidad": q}, cart, pol, ahora)
            if v["resultado"] == "APROBADO":
                break
        v = None
        k -= bajada
    if v is None:
        return _r(False, "E-04", "no hay una cantidad viable por encima del paso y del valor mínimo", limitada_por=regla)
    return {"ok": True, "codigo": "OK", "motivo": "", "cantidad": q, "limitada_por": regla, "valor_eur": q * ent,
            "riesgo_eur": q * abs(ent - stop), "riesgo_pct": q * abs(ent - stop) / cart["capital_eur"] * 100}
