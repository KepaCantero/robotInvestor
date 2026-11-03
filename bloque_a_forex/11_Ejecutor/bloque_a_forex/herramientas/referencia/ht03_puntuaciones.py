#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HT-03 · Calculadora determinista de puntuaciones y ranking (implementación de referencia).

Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026 · Subordinado
al Documento 0 del Bloque A Forex V1.0 (secciones 2.6, 9.1, 9.2, 9.6 y Anexo A).

Calcula T, E, M, P y A a partir de sus dimensiones (0–100 en múltiplos de 10,
o «NA»/«NE»), la clave de ordenación RK, la banda marginal, los cambios que
exigen justificación, la elegibilidad para el top-3 y la selección del top-3
por segmento de divisas (los seis segmentos de 2.6: G10N, G10M, EMAS, EMLA,
EMEA, ESTR). Entrada y salida JSON. Aritmética exacta (fracciones).

Reglas implementadas:
  * Total = media ponderada de las dimensiones; «NA» se excluye y su peso se
    redistribuye proporcionalmente entre las restantes; «NE» puntúa 0 y
    conserva su peso; máximo dos NA/NE por puntuación (si hay más, la
    puntuación no es calculable y la opción no es elegible).
  * Redondeo del total al múltiplo de 5 más próximo; los empates (x,5 exacto)
    se resuelven hacia abajo.
  * P incluye como dimensión el total T (40 %); es la única dimensión que no
    tiene por qué ser múltiplo de 10.
  * A FX (atractivo de la oportunidad cambiaria, 9.1 y Anexo A): asimetría 30,
    valoración y desviación del equilibrio 20, carry 15, catalizadores 15,
    momento y posicionamiento 10, convertibilidad y profundidad 10. No puntúa
    instrumentos concretos ni sus costes (frontera con el Bloque B, R21).
  * Tope por saturación narrativa: la dimensión «valoracion» de A no supera 40.
  * T puede ser «NA» en bloque (oportunidad táctica): entonces se exige A ≥ 65
    y RK redistribuye el peso de T entre A y E (regla NA).
  * RK = 0,45·A + 0,35·E + 0,20·T sobre los totales ya redondeados; RK se
    redondea al entero (empates hacia abajo).
  * Banda marginal: total a ≤ 5 puntos de un umbral (elegibilidad y GC2). Si
    se aporta «segunda_pasada» se usa el menor de los dos valores; si no, la
    opción queda no elegible por PS8 (cálculo decisivo sin segunda pasada).
  * Cada opción declara su segmento («segmento» o, por compatibilidad, «clase»)
    entre los seis códigos; el top-3 se selecciona por segmento y la salida
    sigue el orden de la tabla 2.6.
  * Diversidad dentro del segmento (9.6.3): como máximo dos opciones del mismo
    clúster de exposición y una misma divisa con la misma dirección (LARGO o
    CORTO) en no más de dos opciones. La opción que rompería la regla cede su
    puesto a la siguiente elegible que la cumpla si su RK está a ≤ 10 puntos;
    si no hay ninguna, el hueco queda vacío y se explica (R14). La exposición
    de cada opción se toma de «exposiciones» [{divisa, lado}], de «composicion»
    [{divisa, peso, lado}] o, en su defecto, de «par» BASE/COTIZADA y
    «direccion» (ALCISTA_BASE: base LARGO y cotizada CORTO; BAJISTA_BASE: al
    revés).

Solo biblioteca estándar. Estado de madurez (R22): implementada (referencia),
pruebas unitarias superadas; pendiente de integración.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from fractions import Fraction
from typing import Any, Dict, List, Optional, Sequence, Tuple

VERSION = "FX-1.0"

# Los seis segmentos de divisas (Documento 0 Forex V1.0, 2.6), en el orden canónico de la tabla.
SEGMENTOS = ("G10N", "G10M", "EMAS", "EMLA", "EMEA", "ESTR")
# Dimensiones de A que no existen en el Bloque A Forex (A del Bloque A general) y su equivalente FX.
DIMENSIONES_A_RETIRADAS = {"liquidez_accesibilidad": "convertibilidad", "costes_implementacion": "convertibilidad",
                           "invertibilidad": "convertibilidad", "momento": "momento_posicionamiento"}
LADOS = ("LARGO", "CORTO")

PARAMETROS_POR_DEFECTO: Dict[str, Any] = {
    "pesos": {
        "T": {"magnitud": 20, "alcance": 15, "velocidad": 15, "duracion": 10, "difusion": 10,
              "posicion_cadena_valor": 10, "capacidad_transformadora": 10, "claridad_causal": 10},
        "E": {"calidad_raices": 25, "cobertura_variables": 15, "calidad_metodologica": 15, "trazabilidad": 15,
              "actualidad": 10, "discrepancias_resueltas": 10, "objeciones_respondidas": 10},
        "M": {"adopcion": 20, "escalado": 15, "indicadores_disponibles": 15, "persistencia": 15,
              "estabilidad_impulsores": 15, "hitos_claros": 20},
        "P": {"T": 40, "novedad": 20, "incertidumbre_reducible": 20, "coste_eficiencia": 20},
        "A": {"asimetria": 30, "valoracion": 20, "carry": 15, "catalizadores": 15, "momento_posicionamiento": 10,
              "convertibilidad": 10},
    },
    "pesos_rk": {"A": 0.45, "E": 0.35, "T": 0.20},
    "umbrales": {"E": 60, "A": 55, "T": 50, "A_si_T_NA": 65, "GC2_E": 50},
    "banda_marginal": 5,
    "cambio_material": 15,
    "tope_valoracion_saturacion": 40,
    "max_na_ne": 2,
    "max_opciones_por_segmento": 3,
    "max_por_cluster": 2,
    "max_divisa_misma_direccion": 2,
    "diversidad_margen_rk": 10,
    "continuidad_margen_rk": 10,
    "empate_rk": 2,
    "segmentos": list(SEGMENTOS),
    "puertas_obligatorias": ["G1", "G2", "G3", "G4", "PS1", "PS2", "PS3", "PS4", "PS5", "PS6", "PS7", "PS8"],
}

ORDEN_PUNTUACIONES = ["T", "E", "M", "A", "P"]  # P depende de T


class ErrorEntrada(ValueError):
    pass


# ---------------------------------------------------------------------------
# Utilidades numéricas
# ---------------------------------------------------------------------------
def redondear_abajo_en_empate(valor: Fraction, paso: int) -> int:
    """Redondea al múltiplo de `paso` más próximo; en empate exacto, hacia abajo."""
    q = Fraction(valor) / paso
    base = q.numerator // q.denominator
    resto = q - base
    if resto > Fraction(1, 2):
        base += 1
    return int(base * paso)


def _frac(x) -> Fraction:
    return Fraction(str(x)) if isinstance(x, float) else Fraction(x)


def fusionar_parametros(extra: Optional[Dict]) -> Dict:
    p = copy.deepcopy(PARAMETROS_POR_DEFECTO)
    if not extra:
        return p
    for k, v in extra.items():
        if isinstance(v, dict) and isinstance(p.get(k), dict):
            for k2, v2 in v.items():
                if isinstance(v2, dict) and isinstance(p[k].get(k2), dict):
                    p[k][k2] = dict(v2)  # un juego de pesos se sustituye entero
                else:
                    p[k][k2] = v2
        else:
            p[k] = v
    return p


# ---------------------------------------------------------------------------
# Cálculo de una puntuación
# ---------------------------------------------------------------------------
def calcular_puntuacion(nombre: str, dims: Dict[str, Any], pesos: Dict[str, int], max_na_ne: int = 2,
                        tope: Optional[Dict[str, int]] = None, derivadas: Tuple[str, ...] = ()) -> Dict:
    """Devuelve {'total', 'media_exacta', 'desglose', 'na', 'ne', 'notas'} o lanza ErrorEntrada."""
    if not isinstance(dims, dict):
        raise ErrorEntrada(f"{nombre}: las dimensiones deben ser un objeto")
    desconocidas = sorted(set(dims) - set(pesos))
    faltan = sorted(set(pesos) - set(dims))
    if desconocidas:
        retiradas = [d for d in desconocidas if nombre == "A" and d in DIMENSIONES_A_RETIRADAS]
        if retiradas:
            equivalentes = sorted({DIMENSIONES_A_RETIRADAS[d] for d in retiradas})
            raise ErrorEntrada(f"{nombre}: dimensiones {retiradas} no existen en la A FX (9.1 y Anexo A del Bloque A Forex); "
                               f"usar {equivalentes}")
        raise ErrorEntrada(f"{nombre}: dimensiones desconocidas {desconocidas}")
    if faltan:
        raise ErrorEntrada(f"{nombre}: faltan dimensiones {faltan} (usar 'NA' o 'NE' de forma explícita)")
    na, ne, notas = [], [], []
    valores: Dict[str, Optional[Fraction]] = {}
    for d, v in dims.items():
        if isinstance(v, str) and v.strip().upper() in ("NA", "NE"):
            (na if v.strip().upper() == "NA" else ne).append(d)
            valores[d] = None if v.strip().upper() == "NA" else Fraction(0)
            continue
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ErrorEntrada(f"{nombre}.{d}: valor no válido {v!r}")
        fv = _frac(v)
        if fv < 0 or fv > 100:
            raise ErrorEntrada(f"{nombre}.{d}: fuera de rango 0–100 ({v})")
        if d not in derivadas and fv % 10 != 0:
            raise ErrorEntrada(f"{nombre}.{d}: debe ser múltiplo de 10 ({v})")
        if tope and d in tope and fv > tope[d]:
            notas.append(f"{d} limitada a {tope[d]} por saturación narrativa (valor declarado {v})")
            fv = Fraction(tope[d])
        valores[d] = fv
    if len(na) + len(ne) > max_na_ne:
        raise ErrorEntrada(f"{nombre}: {len(na) + len(ne)} dimensiones NA/NE (máximo {max_na_ne}); puntuación no calculable")
    peso_aplicable = sum(Fraction(pesos[d]) for d in pesos if d not in na)
    if peso_aplicable == 0:
        raise ErrorEntrada(f"{nombre}: ningún peso aplicable")
    suma = sum(Fraction(pesos[d]) * valores[d] for d in pesos if d not in na)
    media = suma / peso_aplicable
    desglose = {}
    for d in pesos:
        pe = Fraction(0) if d in na else Fraction(pesos[d]) / peso_aplicable * 100
        desglose[d] = {"valor": ("NA" if d in na else ("NE" if d in ne else _num(valores[d]))),
                       "peso_nominal": pesos[d], "peso_efectivo": round(float(pe), 4)}
    if na:
        notas.append(f"NA en {na}: peso redistribuido proporcionalmente entre {len(pesos) - len(na)} dimensiones")
    if ne:
        notas.append(f"NE en {ne}: puntúan 0 y conservan su peso")
    return {"total": redondear_abajo_en_empate(media, 5), "media_exacta": round(float(media), 4),
            "desglose": desglose, "na": na, "ne": ne, "notas": notas}


def _num(f: Fraction):
    return int(f) if f.denominator == 1 else float(f)


def calcular_rk(T: Optional[int], E: int, A: int, pesos_rk: Dict[str, float]) -> Tuple[int, float]:
    componentes = {"A": A, "E": E, "T": T}
    aplicable = {k: _frac(w) for k, w in pesos_rk.items() if componentes.get(k) is not None}
    total_peso = sum(aplicable.values())
    exacto = sum(w * componentes[k] for k, w in aplicable.items()) / total_peso
    return redondear_abajo_en_empate(exacto, 1), round(float(exacto), 4)


# ---------------------------------------------------------------------------
# Opción completa
# ---------------------------------------------------------------------------
def _umbrales_de(nombre: str, T_na: bool, u: Dict) -> List[Tuple[str, int]]:
    if nombre == "E":
        return [("elegibilidad E", u["E"]), ("GC2 E provisional", u["GC2_E"])]
    if nombre == "A":
        return [("elegibilidad A", u["A_si_T_NA"] if T_na else u["A"])]
    if nombre == "T" and not T_na:
        return [("elegibilidad T", u["T"])]
    return []


def exposiciones_de(op: Dict) -> List[Dict[str, str]]:
    """Exposición por divisa de una opción: lista ordenada y sin duplicados de {divisa, lado}.

    Prioridad: «exposiciones» explícitas; «composicion» [{divisa, peso, lado}]; «par» BASE/COTIZADA con
    «direccion» ALCISTA_BASE (base LARGO, cotizada CORTO) o BAJISTA_BASE (base CORTO, cotizada LARGO).
    En cestas, bloques y estrategias la dirección está en la composición; una opción de VOLATILIDAD (dirección nula y
    `vista_volatilidad`) no tiene exposición direccional."""
    vistos, out = set(), []

    def _add(div, lado):
        div, lado = str(div or "").strip().upper(), str(lado or "").strip().upper()
        if len(div) == 3 and lado in LADOS and (div, lado) not in vistos:
            vistos.add((div, lado))
            out.append({"divisa": div, "lado": lado})
    for e in op.get("exposiciones") or []:
        if isinstance(e, dict):
            _add(e.get("divisa"), e.get("lado"))
    if not out:
        for c in op.get("composicion") or []:
            if isinstance(c, dict):
                _add(c.get("divisa"), c.get("lado"))
    if not out and isinstance(op.get("par"), str) and "/" in op["par"]:
        base, cot = op["par"].split("/", 1)
        d = str(op.get("direccion") or "").upper()
        if d == "ALCISTA_BASE":
            _add(base, "LARGO"), _add(cot, "CORTO")
        elif d == "BAJISTA_BASE":
            _add(base, "CORTO"), _add(cot, "LARGO")
    return out


def evaluar_opcion(op: Dict, params: Optional[Dict] = None) -> Dict:
    p = params or PARAMETROS_POR_DEFECTO
    seg = op.get("segmento") or op.get("clase")
    res: Dict[str, Any] = {
        "opp_id": op.get("opp_id"), "segmento": seg, "clase": seg, "cluster": op.get("cluster"),
        "exposiciones": exposiciones_de(op),
        "vigente": bool(op.get("vigente", False)), "riesgo_cola": op.get("riesgo_cola"),
        "puntuaciones": {}, "desglose": {}, "banda_marginal": [], "exige_justificacion": [],
        "errores": [], "advertencias": [], "elegible": False, "motivos_no_elegible": [],
    }
    dims = op.get("dimensiones") or {}
    segunda = op.get("segunda_pasada") or {}
    T_na = isinstance(dims.get("T"), str) and dims.get("T").strip().upper() == "NA"
    tope = {"valoracion": p["tope_valoracion_saturacion"]} if op.get("saturacion_narrativa") else None
    totales: Dict[str, Optional[int]] = {}
    for nombre in ORDEN_PUNTUACIONES:
        if nombre == "T" and T_na:
            totales["T"] = None
            res["puntuaciones"]["T"] = "NA"
            res["desglose"]["T"] = {"notas": ["T no aplicable (oportunidad táctica sin tendencia estructural)"]}
            continue
        d = dims.get(nombre)
        if d is None:
            res["errores"].append(f"Falta la puntuación {nombre}")
            totales[nombre] = None
            continue
        d = dict(d)
        derivadas: Tuple[str, ...] = ()
        if nombre == "P":
            derivadas = ("T",)
            if "T" not in d:
                d["T"] = "NA" if totales.get("T") is None else totales["T"]
        try:
            r = calcular_puntuacion(nombre, d, p["pesos"][nombre], p["max_na_ne"],
                                    tope if nombre == "A" else None, derivadas)
        except ErrorEntrada as e:
            res["errores"].append(str(e))
            totales[nombre] = None
            continue
        total = r["total"]
        # Banda marginal
        cercanos = [(etq, u) for etq, u in _umbrales_de(nombre, T_na, p["umbrales"]) if abs(total - u) <= p["banda_marginal"]]
        if cercanos:
            entrada_bm = {"puntuacion": nombre, "total_primera_pasada": total,
                          "umbrales": [{"umbral": etq, "valor": u, "distancia": total - u} for etq, u in cercanos]}
            if nombre in segunda:
                d2 = dict(segunda[nombre])
                if nombre == "P" and "T" not in d2:
                    d2["T"] = d["T"]
                try:
                    r2 = calcular_puntuacion(nombre, d2, p["pesos"][nombre], p["max_na_ne"],
                                             tope if nombre == "A" else None, derivadas)
                    entrada_bm["total_segunda_pasada"] = r2["total"]
                    if r2["total"] < total:
                        r = r2
                        total = r2["total"]
                    entrada_bm["total_usado"] = total
                    entrada_bm["resuelta"] = True
                except ErrorEntrada as e:
                    res["errores"].append(f"segunda pasada: {e}")
                    entrada_bm["resuelta"] = False
            else:
                entrada_bm["resuelta"] = False
            res["banda_marginal"].append(entrada_bm)
        totales[nombre] = total
        res["puntuaciones"][nombre] = total
        res["desglose"][nombre] = r
    # P se recalcula si T cambió tras segunda pasada (P usa el T final)
    if totales.get("T") is not None and "P" in res["desglose"] and isinstance(res["desglose"]["P"], dict):
        tp = res["desglose"]["P"].get("desglose", {}).get("T", {}).get("valor")
        if tp != totales["T"] and "T" not in (dims.get("P") or {}):
            d = dict(dims["P"]); d["T"] = totales["T"]
            r = calcular_puntuacion("P", d, p["pesos"]["P"], p["max_na_ne"], None, ("T",))
            res["desglose"]["P"] = r
            res["puntuaciones"]["P"] = totales["P"] = r["total"]
    # RK
    if totales.get("A") is not None and totales.get("E") is not None:
        rk, rk_exacto = calcular_rk(totales.get("T"), totales["E"], totales["A"], p["pesos_rk"])
        res["puntuaciones"]["RK"] = rk
        res["desglose"]["RK"] = {"exacto": rk_exacto, "pesos": p["pesos_rk"],
                                 "notas": (["T NA: pesos de RK redistribuidos entre A y E"] if T_na else [])}
    # Cambios materiales
    anterior = op.get("anterior") or {}
    for k, v in anterior.items():
        actual = res["puntuaciones"].get(k)
        if isinstance(actual, int) and isinstance(v, (int, float)) and abs(actual - v) >= p["cambio_material"]:
            res["exige_justificacion"].append({"puntuacion": k, "anterior": v, "actual": actual,
                                               "cambio": actual - v})
    res["elegible"], res["motivos_no_elegible"] = _elegibilidad(op, res, totales, T_na, p)
    return res


def _elegibilidad(op: Dict, res: Dict, tot: Dict, T_na: bool, p: Dict) -> Tuple[bool, List[Dict]]:
    m: List[Dict] = []
    u = p["umbrales"]
    if res["errores"]:
        m.append({"codigo": "ERROR_CALCULO", "detalle": "; ".join(res["errores"])})
    E, A, T = tot.get("E"), tot.get("A"), tot.get("T")
    if E is not None and E < u["E"]:
        m.append({"codigo": "E_BAJO", "detalle": f"E={E} < {u['E']}", "falta": u["E"] - E})
    if T_na:
        if A is not None and A < u["A_si_T_NA"]:
            m.append({"codigo": "A_BAJO", "detalle": f"A={A} < {u['A_si_T_NA']} (T NA)", "falta": u["A_si_T_NA"] - A})
    else:
        if A is not None and A < u["A"]:
            m.append({"codigo": "A_BAJO", "detalle": f"A={A} < {u['A']}", "falta": u["A"] - A})
        if T is not None and T < u["T"]:
            m.append({"codigo": "T_BAJO", "detalle": f"T={T} < {u['T']}", "falta": u["T"] - T})
    puertas = op.get("puertas") or {}
    for g in p["puertas_obligatorias"]:
        if g not in puertas:
            m.append({"codigo": "PUERTA_SIN_DATO", "detalle": f"{g} sin resultado declarado", "puerta": g})
        elif puertas[g] is not True:
            m.append({"codigo": "PUERTA_NO_SUPERADA", "detalle": f"{g} no superada", "puerta": g})
    for bm in res["banda_marginal"]:
        if not bm.get("resuelta"):
            m.append({"codigo": "PS8_BANDA_MARGINAL", "puntuacion": bm["puntuacion"],
                      "detalle": f"{bm['puntuacion']}={bm['total_primera_pasada']} en banda marginal sin segunda pasada independiente"})
    fuertes = int(op.get("objeciones_fuertes_abiertas") or 0)
    if fuertes > 0:
        m.append({"codigo": "OBJECION_FUERTE", "detalle": f"{fuertes} objeción(es) fuerte(s) sin resolver"})
    return (not m), m


# ---------------------------------------------------------------------------
# Selección del top-3 por segmento de divisas (9.6)
# ---------------------------------------------------------------------------
def _cola(o: Dict) -> float:
    c = o.get("riesgo_cola")
    return float(c) if isinstance(c, (int, float)) else float("inf")


def ordenar(elegibles: List[Dict], empate: int = 2) -> List[Dict]:
    """Orden por RK; dentro de ±empate puntos prevalece mayor E y después menor riesgo de cola."""
    lst = sorted(elegibles, key=lambda o: (-o["puntuaciones"]["RK"], -o["puntuaciones"]["E"], _cola(o), str(o["opp_id"])))
    clave2 = lambda o: (-o["puntuaciones"]["E"], _cola(o), str(o["opp_id"]))  # noqa: E731
    cambiado = True
    while cambiado:
        cambiado = False
        for i in range(len(lst) - 1):
            a, b = lst[i], lst[i + 1]
            if abs(a["puntuaciones"]["RK"] - b["puntuaciones"]["RK"]) <= empate and clave2(b) < clave2(a):
                lst[i], lst[i + 1] = b, a
                cambiado = True
    return lst


def _que_tendria_que_ocurrir(motivos: List[Dict]) -> List[str]:
    out = []
    for m in motivos:
        c = m["codigo"]
        if c in ("E_BAJO", "A_BAJO", "T_BAJO"):
            out.append(f"{c[0]} debería subir al menos {m['falta']} puntos ({m['detalle']})")
        elif c == "PUERTA_NO_SUPERADA":
            out.append(f"Superar la puerta {m['puerta']}")
        elif c == "PUERTA_SIN_DATO":
            out.append(f"Evaluar la puerta {m['puerta']}")
        elif c == "PS8_BANDA_MARGINAL":
            out.append(f"Segunda pasada independiente de {m['puntuacion']} y cálculo verificado")
        elif c == "OBJECION_FUERTE":
            out.append("Resolver las objeciones fuertes con evidencia")
        else:
            out.append(m["detalle"])
    return out


def _infracciones(o: Dict, seleccion: List[Dict], p: Dict) -> List[str]:
    """Reglas de diversidad del segmento (9.6.3) que rompería añadir `o` a la selección."""
    out = []
    cl = o.get("cluster")
    if cl is not None and sum(1 for x in seleccion if x.get("cluster") == cl) >= p["max_por_cluster"]:
        out.append(f"más de {p['max_por_cluster']} opciones del clúster «{cl}»")
    for e in o.get("exposiciones") or []:
        n = sum(1 for x in seleccion for f in (x.get("exposiciones") or []) if f["divisa"] == e["divisa"] and f["lado"] == e["lado"])
        if n >= p["max_divisa_misma_direccion"]:
            out.append(f"{e['divisa']} {e['lado']} en más de {p['max_divisa_misma_direccion']} opciones del segmento")
    return out


def seleccionar_top3(evaluadas: List[Dict], params: Optional[Dict] = None, candidatas_analizadas: Optional[int] = None) -> Dict:
    p = params or PARAMETROS_POR_DEFECTO
    maxn = p.get("max_opciones_por_segmento", p.get("max_opciones_por_clase", 3))
    elegibles = [o for o in evaluadas if o["elegible"]]
    no_elegibles = [o for o in evaluadas if not o["elegible"]]
    orden = ordenar(elegibles, p["empate_rk"])
    pos = {o["opp_id"]: i for i, o in enumerate(orden)}
    decisiones: List[Dict] = []

    # Continuidad (9.6.4)
    nuevas = [o for o in orden if not o["vigente"]]
    mejor_nueva = nuevas[0]["puntuaciones"]["RK"] if nuevas else None
    mantenidas, sustituidas = [], []
    for v in [o for o in orden if o["vigente"]]:
        if mejor_nueva is None or v["puntuaciones"]["RK"] >= mejor_nueva - p["continuidad_margen_rk"]:
            mantenidas.append(v)
        else:
            sustituidas.append(v)
            decisiones.append({"opp_id": v["opp_id"], "decision": "SUSTITUIDA",
                               "motivo": f"Vigente con RK {v['puntuaciones']['RK']}, más de {p['continuidad_margen_rk']} puntos por debajo de la mejor alternativa nueva ({nuevas[0]['opp_id']}, RK {mejor_nueva})"})
    for v in [o for o in no_elegibles if o["vigente"]]:
        decisiones.append({"opp_id": v["opp_id"], "decision": "VIGENTE_NO_ELEGIBLE",
                           "motivo": "Deja de ser elegible: " + "; ".join(m["detalle"] for m in v["motivos_no_elegible"])})
    # Orden de consideración: vigentes mantenidas (continuidad) y después las nuevas por RK
    cola = sorted(mantenidas, key=lambda o: pos[o["opp_id"]]) + nuevas

    # Diversidad (9.6.3): ≤ 2 por clúster y una divisa con la misma dirección en ≤ 2 opciones del segmento.
    # La opción que rompería la regla cede su puesto a la siguiente elegible que la cumpla con RK a ≤ 10 puntos.
    seleccion: List[Dict] = []
    cedidas: List[Dict] = []
    for o in cola:
        if len(seleccion) >= maxn:
            break
        inf = _infracciones(o, seleccion, p)
        if inf:
            cedidas.append({"opp_id": o["opp_id"], "RK": o["puntuaciones"]["RK"], "infracciones": inf})
            continue
        if cedidas and o["puntuaciones"]["RK"] < min(c["RK"] for c in cedidas) - p["diversidad_margen_rk"]:
            break   # ninguna alternativa diversa a ≤ 10 puntos: el hueco queda vacío (R14)
        seleccion.append(o)
    seleccion.sort(key=lambda o: pos[o["opp_id"]])
    ids_sel = {o["opp_id"] for o in seleccion}
    entran = [o["opp_id"] for o in seleccion if cedidas and pos[o["opp_id"]] > min(pos[c["opp_id"]] for c in cedidas)]
    diversidad: Dict[str, Any] = {"aplicada": bool(cedidas)}
    for c in cedidas:
        motivo = (f"{c['opp_id']} (RK {c['RK']}) rompería la diversidad del segmento: {'; '.join(c['infracciones'])} (9.6.3)")
        decisiones.append({"opp_id": c["opp_id"], "decision": "CEDE_POR_DIVERSIDAD", "motivo": motivo})
    if cedidas:
        diversidad.update({"sale": [c["opp_id"] for c in cedidas], "entra": entran,
                           "motivo": "; ".join(d["motivo"] for d in decisiones if d["decision"] == "CEDE_POR_DIVERSIDAD")})
        if len(seleccion) < maxn:
            diversidad["hueco_vacio"] = True
            diversidad["motivo"] += (f"; no hay alternativa elegible que cumpla la diversidad con RK a ≤ {p['diversidad_margen_rk']} "
                                     "puntos: el hueco queda vacío (R14)")
    sin_cluster = [o["opp_id"] for o in seleccion if o.get("cluster") is None]
    ids_mant = {o["opp_id"] for o in mantenidas}
    decisiones = [d for d in decisiones if d["opp_id"] not in ids_sel]

    def _motivo_sel(o: Dict) -> str:
        if o["opp_id"] in entran:
            return "Entra por diversidad del segmento (9.6.3)"
        if o["opp_id"] in ids_mant:
            return f"Continuidad: vigente y elegible, a ≤ {p['continuidad_margen_rk']} puntos de la mejor alternativa nueva (9.6.4)"
        return f"Orden por RK ({o['puntuaciones']['RK']}) con desempate por E y riesgo de cola (9.6.2)"

    top = [{"rango": i + 1, "opp_id": o["opp_id"], "RK": o["puntuaciones"]["RK"], "E": o["puntuaciones"]["E"],
            "cluster": o.get("cluster"), "exposiciones": o.get("exposiciones") or [], "vigente": o["vigente"],
            "motivo": _motivo_sel(o)}
           for i, o in enumerate(seleccion)]
    for o in orden:
        if o["opp_id"] not in ids_sel and not any(d["opp_id"] == o["opp_id"] for d in decisiones):
            decisiones.append({"opp_id": o["opp_id"], "decision": "ALTERNATIVA",
                               "motivo": f"Elegible fuera del top-{maxn} por RK ({o['puntuaciones']['RK']})"})
    for o in no_elegibles:
        if not o["vigente"]:
            decisiones.append({"opp_id": o["opp_id"], "decision": "NO_ELEGIBLE",
                               "motivo": "; ".join(m["detalle"] for m in o["motivos_no_elegible"])})
    menos = None
    if len(seleccion) < maxn:
        n_cand = candidatas_analizadas if candidatas_analizadas is not None else len(evaluadas)
        menos = {
            "candidatas_analizadas": n_cand, "finalistas_evaluadas": len(evaluadas), "elegibles": len(elegibles),
            "no_llegaron": [{"opp_id": o["opp_id"], "motivos": [m["detalle"] for m in o["motivos_no_elegible"]],
                             "que_tendria_que_ocurrir": _que_tendria_que_ocurrir(o["motivos_no_elegible"])}
                            for o in no_elegibles],
            "texto": (f"Se proponen {len(seleccion)} opción(es): de {n_cand} candidatas analizadas, "
                      f"{len(evaluadas)} finalistas evaluadas y {len(elegibles)} elegibles (R14)."
                      + (f" {len(cedidas)} elegible(s) cedieron su puesto por diversidad del segmento (9.6.3)." if cedidas else "")),
        }
    return {"top3": top, "decisiones": decisiones, "diversidad": diversidad,
            "sin_cluster": sin_cluster, "menos_de_tres_motivo": menos}


def procesar(entrada: Dict) -> Dict:
    params = fusionar_parametros(entrada.get("parametros"))
    opciones = entrada.get("opciones")
    if not isinstance(opciones, list):
        raise ErrorEntrada("La entrada debe contener la lista 'opciones'")
    validos = tuple(params.get("segmentos") or SEGMENTOS)
    vistos = set()
    normalizadas = []
    for o in opciones:
        seg = o.get("segmento") or o.get("clase")
        if not o.get("opp_id") or not seg:
            raise ErrorEntrada("Cada opción necesita 'opp_id' y 'segmento' (o 'clase')")
        if o.get("segmento") and o.get("clase") and o["segmento"] != o["clase"]:
            raise ErrorEntrada(f"{o['opp_id']}: 'segmento' {o['segmento']} distinto de 'clase' {o['clase']}")
        if seg not in validos:
            raise ErrorEntrada(f"{o['opp_id']}: segmento desconocido {seg!r} (válidos: {', '.join(validos)})")
        if o["opp_id"] in vistos:
            raise ErrorEntrada(f"opp_id duplicado: {o['opp_id']}")
        vistos.add(o["opp_id"])
        normalizadas.append({**o, "segmento": seg, "clase": seg})
    cand = entrada.get("candidatas_analizadas") or {}
    desconocidos = sorted(set(cand) - set(validos))
    if desconocidos:
        raise ErrorEntrada(f"candidatas_analizadas: segmentos desconocidos {desconocidos}")
    evaluadas = [evaluar_opcion(o, params) for o in normalizadas]
    por_seg: Dict[str, List[Dict]] = {}
    for e in evaluadas:
        por_seg.setdefault(e["segmento"], []).append(e)
    orden = [t for t in validos if t in por_seg or t in cand]
    seleccion = {t: seleccionar_top3(por_seg.get(t, []), params, cand.get(t)) for t in orden}
    return {"herramienta": "HT-03", "version": VERSION, "parametros": params,
            "opciones": evaluadas, "seleccion": seleccion}


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="HT-03 · Puntuaciones T/E/M/P/A (A FX), RK, elegibilidad y top-3 por segmento de divisas")
    ap.add_argument("entrada", help="JSON de entrada ('-' para stdin)")
    ap.add_argument("--salida", help="JSON de salida (por defecto, stdout)")
    a = ap.parse_args(argv)
    try:
        fh = sys.stdin if a.entrada == "-" else open(a.entrada, encoding="utf-8")
        with fh:
            entrada = json.load(fh)
        res = procesar(entrada)
    except (OSError, json.JSONDecodeError, ErrorEntrada) as e:
        print(json.dumps({"herramienta": "HT-03", "error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2
    texto = json.dumps(res, ensure_ascii=False, indent=2)
    if a.salida:
        with open(a.salida, "w", encoding="utf-8") as fh:
            fh.write(texto + "\n")
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
