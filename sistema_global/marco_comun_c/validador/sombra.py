"""Cartera sombra pasiva (T-76, V0.71; Constitución V0.6, §9 punto 9, D-22, D-27 y D-30). Determinista, sin red.

Desde el primer día corre en simulado un plan pasivo simple (un índice mundial) con los mismos aportes y retiradas que la cartera
real. Cada mes se compara el robot con la sombra después de costes de análisis (los de los modelos incluidos), comisiones e
impuestos, y también en términos reales (después de inflación). Si tras 24 meses el robot no la supera, se propone pasar a
gestión pasiva y decide el operador.

Este módulo solo calcula (funciones puras); el registro encadenado y los avisos viven en el Orquestador. Convenciones:
- El valor del robot es el de su cartera según G (las comisiones ya van dentro: son lo que cobró el intermediario).
- Los costes de análisis son los que el Orquestador anotó (`gasto_dia`) desde el inicio de la sombra.
- Los impuestos los estima quien compara (SC-9 aún no existe): se declaran y se restan.
- La sombra paga su propio coste anual (`i_coste_anual_sombra_pct`, el de un fondo indexado), devengado por tramos entre
  movimientos como el gasto corriente de un fondo. No paga impuestos ni comisiones de compra: es el plan pasivo de referencia.
- En real, robot y sombra se dividen por la misma inflación: el veredicto en real coincide siempre con el nominal; la cifra real
  es la que se informa (D-30). El índice de precios lo fija el operador (propuesto: el IPCA de la zona euro, P-25) y lo da K.
- Términos reales: los dos valores se dividen por la inflación acumulada (índice de precios del mes / índice al inicio).
- Como los dos reciben los mismos movimientos, se comparan los valores, no las rentabilidades (no hace falta una tasa
  ponderada por dinero). Se da también el exceso en euros y en proporción de lo aportado neto.
"""
from __future__ import annotations

import math
import re

from parametros import PARAMETROS

MES = re.compile(r"^\d{4}-(0[1-9]|1[0-2])\Z")
TIPOS_MOVIMIENTO = ("APORTE", "RETIRADA")


def num_pos(x, cero=False):
    """Un número finito positivo (o cero si cero=True); False para bool, textos, NaN e infinitos."""
    return (isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and (x >= 0 if cero else x > 0))


def meses_entre(mes0, mes1):
    """Meses naturales de mes0 a mes1 (AAAA-MM)."""
    a0, m0 = map(int, mes0.split("-"))
    a1, m1 = map(int, mes1.split("-"))
    return (a1 - a0) * 12 + (m1 - m0)


def _factor_coste(dias, coste_anual_pct):
    """Lo que queda de una unidad tras `dias` de coste anual (como el gasto corriente de un fondo, que se descuenta del valor
    liquidativo cada día): (1 - coste) elevado a dias/365."""
    return (1.0 - coste_anual_pct / 100.0) ** (max(0.0, dias) / 365.0)


def estado_sombra(entradas, precio_indice, hasta, coste_anual_pct=PARAMETROS["i_coste_anual_sombra_pct"]):
    """Unidades del índice y aportado neto tras las entradas INICIO y APORTE/RETIRADA, valoradas al precio dado en el instante
    `hasta` (datetime). T-76 (QA r01, H-01): el coste de la sombra se devenga por tramos entre movimientos, descontando unidades
    como hace un fondo; un aporte reciente paga solo desde que llegó y una retirada no borra lo ya devengado. Devuelve None si
    las entradas no se pueden leer, si una retirada es mayor que lo que hay o si algún resultado no es un número finito (H-03 y
    H-06: la comparación de la retirada es relativa a lo que hay, no una tolerancia absoluta)."""
    try:
        from validar_sobre import _dt
        unidades, sin_coste, neto, t_prev = 0.0, 0.0, 0.0, None
        for x in entradas:
            if x["tipo"] not in ("INICIO",) + TIPOS_MOVIMIENTO:
                continue
            t = _dt(x["ahora"])
            if t_prev is not None:
                unidades *= _factor_coste((t - t_prev).total_seconds() / 86400.0, coste_anual_pct)
            t_prev = t
            u = x["importe_eur"] / x["precio_indice"]
            if x["tipo"] == "RETIRADA":
                if u > unidades * (1 + 1e-12):
                    return None
                unidades, sin_coste, neto = max(0.0, unidades - u), sin_coste - u, neto - x["importe_eur"]
            else:
                unidades, sin_coste, neto = unidades + u, sin_coste + u, neto + x["importe_eur"]
        if t_prev is None:
            return None
        unidades *= _factor_coste((hasta - t_prev).total_seconds() / 86400.0, coste_anual_pct)
        bruto = sin_coste * precio_indice
        valor = unidades * precio_indice
        out = {"unidades": unidades, "aportado_neto_eur": neto, "valor_bruto_eur": bruto, "coste_eur": bruto - valor, "valor_eur": valor}
        return out if all(math.isfinite(v) for v in out.values()) else None
    except (KeyError, TypeError, ZeroDivisionError, ValueError, OverflowError, AttributeError):
        return None


def comparar(robot_valor_eur, costes_analisis_eur, impuestos_eur, sombra, inflacion_inicio, inflacion_mes):
    """El robot (neto de costes de análisis e impuestos) frente a la sombra, en nominal y en real. None si algo no se lee."""
    try:
        robot = robot_valor_eur - costes_analisis_eur - impuestos_eur
        f = inflacion_mes / inflacion_inicio
        if not (math.isfinite(f) and f > 0):
            return None
        robot_real, sombra_real = robot / f, sombra["valor_eur"] / f
        base = sombra["aportado_neto_eur"]
        out = {"robot_neto_eur": robot, "sombra_eur": sombra["valor_eur"], "exceso_eur": robot - sombra["valor_eur"],
               "robot_neto_real_eur": robot_real, "sombra_real_eur": sombra_real, "exceso_real_eur": robot_real - sombra_real,
               "exceso_sobre_aportado": (robot - sombra["valor_eur"]) / base if base > 0 else None,
               "inflacion_acumulada": f - 1.0, "supera": robot_real > sombra_real}
        # H-03: un resultado no finito no se anota (después el estado no se podría guardar)
        return out if all(v is None or isinstance(v, bool) or math.isfinite(v) for v in out.values()) else None
    except (KeyError, TypeError, ZeroDivisionError, ValueError, OverflowError):
        return None


def veredicto(meses, comparacion, meses_juicio=PARAMETROS["i_meses_juicio_sombra"]):
    """EN_PLAZO antes de los meses de juicio; después, SUPERA o PROPONER_PASIVA (en términos reales, D-30). Decide el operador."""
    if meses < meses_juicio:
        return "EN_PLAZO"
    return "SUPERA" if comparacion["supera"] else "PROPONER_PASIVA"
