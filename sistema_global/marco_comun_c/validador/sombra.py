"""Cartera sombra pasiva (T-76, V0.71; Constitución V0.6, §9 punto 9, D-22, D-27 y D-30). Determinista, sin red.

Desde el primer día corre en simulado un plan pasivo simple (un índice mundial) con los mismos aportes y retiradas que la cartera
real. Cada mes se compara el robot con la sombra después de costes de análisis (los de los modelos incluidos), comisiones e
impuestos, y también en términos reales (después de inflación). Si tras 24 meses el robot no la supera, se propone pasar a
gestión pasiva y decide el operador.

Este módulo solo calcula (funciones puras); el registro encadenado y los avisos viven en el Orquestador. Convenciones:
- El valor del robot es el de su cartera según G (las comisiones ya van dentro: son lo que cobró el intermediario).
- Los costes de análisis son los que el Orquestador anotó (`gasto_dia`) desde el inicio de la sombra.
- Los impuestos los estima quien compara (SC-9 aún no existe): se declaran y se restan.
- La sombra paga su propio coste anual (`i_coste_anual_sombra_pct`, el de un fondo indexado), prorrateado por días.
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


def estado_sombra(entradas, precio_indice, dias_desde_inicio, coste_anual_pct=PARAMETROS["i_coste_anual_sombra_pct"]):
    """Unidades del índice y aportado neto tras las entradas INICIO y APORTE/RETIRADA, y el valor de la sombra al precio dado,
    neto de su coste anual prorrateado. Devuelve None si las entradas no se pueden leer o una retirada deja unidades negativas."""
    try:
        unidades, neto = 0.0, 0.0
        for x in entradas:
            if x["tipo"] == "INICIO":
                unidades += x["importe_eur"] / x["precio_indice"]
                neto += x["importe_eur"]
            elif x["tipo"] in TIPOS_MOVIMIENTO:
                signo = 1 if x["tipo"] == "APORTE" else -1
                unidades += signo * x["importe_eur"] / x["precio_indice"]
                neto += signo * x["importe_eur"]
                if unidades < -1e-9:
                    return None
        bruto = unidades * precio_indice
        coste = bruto * (coste_anual_pct / 100.0) * max(0.0, dias_desde_inicio) / 365.0
        return {"unidades": unidades, "aportado_neto_eur": neto, "valor_bruto_eur": bruto, "coste_eur": coste, "valor_eur": bruto - coste}
    except (KeyError, TypeError, ZeroDivisionError, ValueError, OverflowError):
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
        return {"robot_neto_eur": robot, "sombra_eur": sombra["valor_eur"], "exceso_eur": robot - sombra["valor_eur"],
                "robot_neto_real_eur": robot_real, "sombra_real_eur": sombra_real, "exceso_real_eur": robot_real - sombra_real,
                "exceso_sobre_aportado": (robot - sombra["valor_eur"]) / base if base > 0 else None,
                "inflacion_acumulada": f - 1.0, "supera": robot_real > sombra_real}
    except (KeyError, TypeError, ZeroDivisionError, ValueError, OverflowError):
        return None


def veredicto(meses, comparacion, meses_juicio=PARAMETROS["i_meses_juicio_sombra"]):
    """EN_PLAZO antes de los meses de juicio; después, SUPERA o PROPONER_PASIVA (en términos reales, D-30). Decide el operador."""
    if meses < meses_juicio:
        return "EN_PLAZO"
    return "SUPERA" if comparacion["supera"] else "PROPONER_PASIVA"
