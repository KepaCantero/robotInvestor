#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HT-08 · Monitor de tiempo, colas y consumo (implementación de referencia).

Bloque B · Robot Investor · V2.0 (actualizado V2.1, 03/11/2026) · Subordinada al Documento 0 del Bloque B, óptima V2.1
(secciones 4.4, 7.2, 7.4 F0, 7.10, 9.9, 10.3 y Anexo A).

Funciones:

  * **Modelo de tiempos** (Anexo A): estimación por nodo del grafo del plan —dimensión × profundidad, selección ×
    tamaño de universo, refutación, auditoría con su bucle esperado, redacción— con camino crítico (F2 en paralelo
    por especialista; F4 y F5 en paralelo; F5 en paralelo por tipo de activo). Devuelve p50 y p80 de minutos y de
    UC y el desglose por fase. p80 = p50 × factor de dispersión. Factores de calibración por fase que el Evaluador
    reestima con el historial de F1 (`recalibrar`), dentro de bandas.
  * **Puerta de tiempo previa** (PT30, antes de F1): p80 > 30 min, o p80 > límite de un PERS.
  * **Puerta en ejecución**: proyección = consumido + p80 restante (escalado por la desviación observada);
    PT30 si no hay autorización por encima de 30 min y la proyección supera 30; PTA si supera el tiempo autorizado
    más el margen (máximo de +10 % y +5 min).
  * **Opciones** de CT-B-05: continuar, versión ≤ 30 min (recortes que no tocan los controles de integridad, R23),
    dividir en fases, avanzar hasta la puerta PV2 (`HASTA_PV2`, V2.1), cancelar; y recomendación del bloque.
  * **Capas** (V2.1, 7.10): estimación por capa (0–4) y acumulada a partir del desglose por fase (F2 y F3 se reparten
    entre las capas 2 y 3 con las fracciones declaradas en `REPARTO_CAPAS`); la puerta usa siempre el acumulado.
  * **Política de autorización automática** (F10): reglas POL- con condición y acción, tope absoluto (240 min por
    defecto; nunca más de 480).
  * **Estado de una autorización pendiente**: recordatorio a las 24 h y CADUCADA a los 7 días.
  * **Puntos de control** reanudables: guardado JSON con huella SHA-256 y verificación al cargar.
  * **Cronómetro** por fase y agente, consumo en UC y órdenes de instancias (R29: cola > 3 o respuesta > 2× objetivo).

Solo biblioteca estándar. CLI: `python3 ht08_monitor_tiempo.py plan.json` (estimación y puerta previa).
Estado de madurez (R26): implementada (referencia), pruebas unitarias superadas; integrada en el ejecutor.
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import math
import statistics
import sys
import threading
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

VERSION = "2.1"
UMBRAL_PT30_MIN = 30.0
TOPE_AUTOMATICO_MIN = 240.0
TOPE_AUTOMATICO_MAX_MIN = 480.0
N3_POR_DEFECTO_MIN = 240.0
FASES = ("F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10")
OPCIONES = ("CONTINUAR", "VERSION_30_MIN", "DIVIDIR_EN_FASES", "HASTA_PV2", "CANCELAR")
# Reparto de cada fase entre capas (7.3, 7.10). F2: dimensiones líderes (capa 2) y resto (capa 3); F3: integración
# provisional (capa 2) y consolidada (capa 3). Concreción declarada de HT-08; la calibra el Evaluador por capa.
REPARTO_CAPAS = {"F0": {0: 1.0}, "F1": {1: 1.0}, "F2": {2: 0.5, 3: 0.5}, "F3": {2: 0.4, 3: 0.6}, "F5": {3: 1.0},
                 "F4": {4: 1.0}, "F6": {4: 1.0}, "F7": {4: 1.0}, "F8": {4: 1.0}, "F9": {4: 1.0}, "F10": {4: 1.0}}
ESPECIALISTA_DIM = {"D1": "AG-B03", "D2": "AG-B04", "D3": "AG-B05", "D4": "AG-B03", "D5": "AG-B06", "D6": "AG-B07",
                    "D7": "AG-B08", "D8": "AG-B09", "D9": "AG-B09", "D10": "AG-B10", "D11": "AG-B11", "D12": "AG-B11"}

MODELO_POR_DEFECTO: Dict[str, Any] = {
    "F0": {"base": 1.0},
    "F1": {"base": 1.0, "por_tipo": 0.3},
    "F2": {"profundidad": {"P0": 0.0, "P1": 0.8, "P2": 1.6, "P3": 2.8}, "integracion": 0.8, "director_factor": 0.3,
           "emergentes": 1.2, "desglose_cadena": 0.4},
    "F3": {"base": 1.5},
    "F4": {"base": 2.5, "N1": 1.0},
    "F5": {"base": 1.0, "por_activo": 0.02, "por_finalista": 0.2},
    "F6": {"base": 1.5, "por_finalista": 0.1, "N1": 0.8},
    "F7": {"base": 1.5},
    "F8": {"g3": 0.5, "auditoria": 2.5, "vuelta": 1.0, "vueltas_esperadas": 0.5,
           "muestreo": {"N0": 0.1, "N1": 0.3, "N2": 1.0, "N3": 1.0, "PERS": 1.0}},
    "F9": {"base": 2.0},
    "F10": {"base": 0.5},
    # Factor global por nivel (N1 reutiliza la Biblioteca y profundiza menos; N3 hace segunda ronda de búsqueda en
    # las dimensiones críticas y usa el plan de cálculo EXT)
    "factor_nivel": {"N0": 0.1, "N1": 0.5, "N2": 1.0, "N3": 1.6, "PERS": 1.0},
    "dispersion_p80": 1.2,
    "factores": {f: 1.0 for f in FASES},
    "uc": {"llamada": 1.0, "calculo_STD": 1.0, "calculo_EXT": 2.0, "calculo_MIN": 0.3},
    "banda_factores": (0.5, 3.0),
    "muestra_minima_recalibrar": 20,
}


class ErrorEntrada(ValueError):
    pass


def _modelo(extra: Optional[Dict]) -> Dict:
    m = copy.deepcopy(MODELO_POR_DEFECTO)

    def fus(a, b):
        for k, v in (b or {}).items():
            if isinstance(v, dict) and isinstance(a.get(k), dict):
                fus(a[k], v)
            else:
                a[k] = v
    fus(m, extra or {})
    return m


# ==============================================================================================================
# Modelo de tiempos
# ==============================================================================================================
def estimar(plan: Dict, modelo: Optional[Dict] = None, fases: Optional[Sequence[str]] = None) -> Dict:
    """Estimación p50/p80 (minutos y UC) del grafo del plan.

    `plan`: nivel; profundidad {D1..D12: P0–P3}; especialistas_activos [AG-B03…]; tipos_activo [..];
    universo_por_tipo {tipo: n}; top_n (por tipo); refutacion (bool); plan_calculo (MIN|STD|EXT);
    `fases`: subconjunto a estimar (para lo que falta en una reanudación)."""
    m = _modelo(modelo)
    nivel = plan.get("nivel", "N2")
    prof = plan.get("profundidad") or {}
    activos = set(plan.get("especialistas_activos") or [])
    tipos = list(plan.get("tipos_activo") or [])
    universo = plan.get("universo_por_tipo") or {}
    top_n = int(plan.get("top_n") or (3 if nivel == "N1" else 10 if nivel == "N3" else 5))
    fin = 2 * top_n
    f = m["factores"]
    d: Dict[str, float] = {}
    llamadas: Dict[str, float] = {}
    d["F0"] = m["F0"]["base"]
    llamadas["F0"] = 2
    d["F1"] = m["F1"]["base"] + m["F1"]["por_tipo"] * len(tipos)
    llamadas["F1"] = 1 + len(tipos) * 0.2
    por_esp: Dict[str, float] = {}
    director = 0.0
    for dim, p in prof.items():
        t = m["F2"]["profundidad"].get(p, 0.0)
        ag = ESPECIALISTA_DIM.get(dim)
        if ag in activos:
            por_esp[ag] = por_esp.get(ag, 0.0) + t
        else:
            director += t * m["F2"]["director_factor"]
    if "AG-B24" in activos:          # V2.1: radar de emergentes (capa 3, en paralelo con los especialistas)
        por_esp["AG-B24"] = m["F2"]["emergentes"]
    if "AG-B03" in activos and prof.get("D4") in ("P2", "P3"):
        por_esp["AG-B03"] = por_esp.get("AG-B03", 0.0) + m["F2"]["desglose_cadena"]
    d["F2"] = (max(por_esp.values()) if por_esp else 0.0) + m["F2"]["integracion"] + director
    llamadas["F2"] = len(por_esp) + 1
    d["F3"] = m["F3"]["base"]
    llamadas["F3"] = 1
    d["F4"] = m["F4"]["N1"] if nivel == "N1" else m["F4"]["base"]
    llamadas["F4"] = 1
    tiempos_tipo = [m["F5"]["base"] + m["F5"]["por_activo"] * float(universo.get(t, 40)) + m["F5"]["por_finalista"] * fin
                    for t in tipos]
    d["F5"] = max(tiempos_tipo) if tiempos_tipo else 0.0
    llamadas["F5"] = len(tipos)
    refut = plan.get("refutacion", nivel in ("N2", "N3"))
    d["F6"] = (m["F6"]["base"] + m["F6"]["por_finalista"] * fin * max(1, len(tipos))) if refut else m["F6"]["N1"]
    llamadas["F6"] = 3 if refut else 1
    d["F7"] = m["F7"]["base"]
    llamadas["F7"] = 1
    pm = m["F8"]["muestreo"].get(nivel, 1.0)
    d["F8"] = m["F8"]["g3"] + pm * (m["F8"]["auditoria"] + m["F8"]["vuelta"] * m["F8"]["vueltas_esperadas"])
    llamadas["F8"] = pm * (1 + m["F8"]["vueltas_esperadas"])
    d["F9"] = m["F9"]["base"]
    llamadas["F9"] = 1
    d["F10"] = m["F10"]["base"]
    llamadas["F10"] = 0
    fn = m["factor_nivel"].get(nivel, 1.0)
    d = {k: round(v * f.get(k, 1.0) * (fn if k not in ("F8", "F10") else 1.0), 3) for k, v in d.items()}
    sel = list(fases) if fases is not None else list(FASES)
    # Camino crítico: F4 ∥ F5
    total = 0.0
    for k in sel:
        if k == "F4" and "F5" in sel:
            total += max(d["F4"], d["F5"])
        elif k == "F5" and "F4" in sel:
            continue
        else:
            total += d[k]
    plan_calc = plan.get("plan_calculo", "EXT" if nivel == "N3" else "STD")
    uc_calc = m["uc"].get(f"calculo_{plan_calc}", 1.0) * (len(tipos) + 2)
    uc = sum(llamadas[k] for k in sel) * m["uc"]["llamada"] + (uc_calc if ("F4" in sel or "F5" in sel) else 0)
    disp = m["dispersion_p80"]
    capas = por_capa({k: d[k] for k in sel})
    hasta_pv2 = sum(v for c, v in capas.items() if int(c) <= 2)
    return {"herramienta": "HT-08", "version": VERSION, "minutos_p50": round(total, 1), "minutos_p80": round(total * disp, 1),
            "uc_p50": round(uc, 1), "uc_p80": round(uc * disp, 1), "desglose_por_fase": {k: d[k] for k in sel},
            "desglose_por_capa": capas, "desglose_por_capa_p80": {c: round(v * disp, 2) for c, v in capas.items()},
            "minutos_p80_hasta_pv2": round(hasta_pv2 * disp, 1),
            "camino_critico": "F4 ∥ F5; F2 en paralelo por especialista; F5 en paralelo por tipo de activo"}


def por_capa(desglose_por_fase: Dict[str, float], fracciones: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    """Minutos por capa (claves «0»…«4») desde el desglose por fase (7.10). `fracciones` (fase → fracción pendiente)
    permite estimar el resto de una fase repartida (p. ej., F2 con la capa 2 ya hecha → {"F2": 0.5})."""
    out: Dict[str, float] = {}
    for f, v in (desglose_por_fase or {}).items():
        rep = REPARTO_CAPAS.get(f, {4: 1.0})
        for c, w in rep.items():
            out[str(c)] = out.get(str(c), 0.0) + float(v) * w
    return {k: round(v, 2) for k, v in sorted(out.items())}


# ==============================================================================================================
# Puertas de tiempo
# ==============================================================================================================
def margen_pta(autorizado_min: float) -> float:
    """Margen de la PTA: +10 % o +5 min, lo que sea mayor (Anexo A)."""
    return max(0.10 * autorizado_min, 5.0)


def tiempo_autorizado_inicial(nivel: str, limite_min: Optional[float] = None, n3_expreso: bool = False,
                              umbral: float = UMBRAL_PT30_MIN) -> float:
    """Tiempo autorizado de partida: un N3 solicitado expresamente viene autorizado hasta el tiempo indicado
    (o 240 min por defecto); un PERS hasta su límite; el resto, hasta el umbral de 30 min."""
    if nivel == "N3" and n3_expreso:
        return float(limite_min or N3_POR_DEFECTO_MIN)
    if nivel == "PERS" and limite_min:
        return float(limite_min)
    return float(umbral)


def puerta_previa(estimacion: Dict, nivel: str, limite_min: Optional[float] = None, n3_expreso: bool = False,
                  umbral: float = UMBRAL_PT30_MIN) -> Dict:
    """PT30 antes de iniciar F1 (9.9). La justificación se genera siempre (R20), aunque no se dispare."""
    p80 = float(estimacion["minutos_p80"])
    autorizado = tiempo_autorizado_inicial(nivel, limite_min, n3_expreso, umbral)
    if nivel == "N3" and n3_expreso:
        dispara = p80 > autorizado
        puerta = "PTA" if dispara else None
        motivo = (f"N3 expreso autorizado hasta {autorizado:g} min; p80 {p80:g} min"
                  + (" lo supera" if dispara else " cabe en lo autorizado"))
    elif nivel == "PERS" and limite_min:
        dispara = p80 > float(limite_min)
        puerta = "PT30" if dispara else None
        motivo = f"PERS con límite {limite_min:g} min; p80 {p80:g} min" + (" lo supera" if dispara else "")
    else:
        dispara = p80 > umbral
        puerta = "PT30" if dispara else None
        motivo = f"p80 {p80:g} min {'>' if dispara else '≤'} {umbral:g} min"
    return {"dispara": dispara, "puerta": puerta, "momento": "PREVIO_F0", "minutos_autorizados": autorizado,
            "motivo": motivo}


def proyectar(consumido_min: float, estimado_hecho_p50: float, restante: Dict, modelo: Optional[Dict] = None,
              ratio_limites: Sequence[float] = (0.8, 2.5)) -> Dict:
    """Proyección del tiempo total: consumido + p80 restante × ratio observado (real/estimado de lo hecho)."""
    m = _modelo(modelo)
    ratio = consumido_min / estimado_hecho_p50 if estimado_hecho_p50 > 0 else 1.0
    ratio = min(max(ratio, ratio_limites[0]), ratio_limites[1])
    rest_p50 = float(restante["minutos_p50"]) * ratio
    return {"ratio_observado": round(ratio, 3), "restante_p50": round(rest_p50, 1),
            "restante_p80": round(rest_p50 * m["dispersion_p80"], 1),
            "total_p50": round(consumido_min + rest_p50, 1),
            "total_p80": round(consumido_min + rest_p50 * m["dispersion_p80"], 1)}


def evaluar_en_ejecucion(consumido_min: float, proyeccion_total_p80: float, autorizado_min: float,
                         umbral: float = UMBRAL_PT30_MIN) -> Dict:
    """PT30 en ejecución (análisis estimado por debajo de 30) o PTA (supera lo autorizado + margen)."""
    if autorizado_min <= umbral:
        dispara = proyeccion_total_p80 > umbral
        return {"dispara": dispara, "puerta": "PT30" if dispara else None, "momento": "EN_EJECUCION",
                "umbral": umbral, "proyeccion_p80": proyeccion_total_p80, "consumido": consumido_min}
    lim = autorizado_min + margen_pta(autorizado_min)
    dispara = proyeccion_total_p80 > lim
    return {"dispara": dispara, "puerta": "PTA" if dispara else None, "momento": "EN_EJECUCION",
            "umbral": autorizado_min, "umbral_con_margen": round(lim, 1), "proyeccion_p80": proyeccion_total_p80,
            "consumido": consumido_min}


# ==============================================================================================================
# Opciones de CT-B-05 y recomendación
# ==============================================================================================================
_BAJAR = {"P3": "P2", "P2": "P1", "P1": "P1", "P0": "P0"}


def version_recortada(plan: Dict, objetivo_min: float = UMBRAL_PT30_MIN, modelo: Optional[Dict] = None,
                      consumido_min: float = 0.0, fases_restantes: Optional[Sequence[str]] = None) -> Dict:
    """Opción (b): recortes sucesivos hasta que consumido + p80 restante ≤ objetivo. Nunca recorta los controles de
    integridad (G3, auditoría previa en N2/N3, D9 ≥ P2 y D12 ≥ P1)."""
    p = copy.deepcopy(plan)
    recortes: List[str] = []
    E_max, veredicto_max = 100, "INVERTIR"

    def total():
        return consumido_min + estimar(p, modelo, fases_restantes)["minutos_p80"]
    pasos: List[Callable[[], Optional[str]]] = []
    # 1) dimensiones P3 a P2 (salvo D9), por peso ascendente
    for dim in sorted((p.get("profundidad") or {}), key=lambda x: (p.get("pesos") or {}).get(x, 0)):
        if p["profundidad"][dim] == "P3" and dim != "D9":
            def f(dim=dim):
                p["profundidad"][dim] = "P2"
                return f"{dim} a P2"
            pasos.append(f)
    # 2) top-N a 3
    def topn():
        if int(p.get("top_n") or 5) > 3:
            p["top_n"] = 3
            return "top-N 3"
        return None
    pasos.append(topn)
    # 3) tipos de activo secundarios
    def tipos():
        t = list(p.get("tipos_activo") or [])
        if len(t) > 1:
            omit = t[1:]
            p["tipos_activo"] = t[:1]
            return "tipos " + ", ".join(omit) + " omitidos"
        return None
    pasos.append(tipos)
    # 4) dimensiones P2 a P1 (salvo D9 y D12)
    for dim in sorted((p.get("profundidad") or {}), key=lambda x: (p.get("pesos") or {}).get(x, 0)):
        if dim not in ("D9", "D12"):
            def g(dim=dim):
                if p["profundidad"][dim] == "P2":
                    p["profundidad"][dim] = "P1"
                    return f"{dim} a P1"
                return None
            pasos.append(g)
    # 5) refutación limitada a la tesis
    def refut():
        if p.get("refutacion", True):
            p["refutacion_limitada"] = True
            p["refutacion"] = False
            return "refutación limitada a la tesis (autorrefutación de candidatos)"
        return None
    pasos.append(refut)
    for paso in pasos:
        if total() <= objetivo_min:
            break
        r = paso()
        if r:
            recortes.append(r)
    alcanza = total() <= objetivo_min
    n_p3 = sum(1 for r in recortes if r.endswith("a P2"))
    n_p1 = sum(1 for r in recortes if r.endswith("a P1"))
    if n_p1:
        E_max = 55
    elif n_p3:
        E_max = 65
    if any(r.startswith("refutación") for r in recortes) or E_max < 60:
        veredicto_max = "VIGILAR"
    elif n_p3:
        veredicto_max = "INVERTIR_ESCALONADO"
    est = estimar(p, modelo, fases_restantes)
    return {"opcion": "VERSION_30_MIN", "que_se_recorta": recortes, "alcanza_objetivo": alcanza,
            "minutos_p80": round(consumido_min + est["minutos_p80"], 1), "uc_p80": est["uc_p80"],
            "efecto_previsible": {"E_max": E_max, "veredicto_max": veredicto_max},
            "controles_no_recortados": ["G3 (HT-09)", "auditoría previa en N2/N3", "D9 ≥ P2", "D12 ≥ P1", "PA1–PA8",
                                        "PC1–PC8"],
            "plan_modificado": p}


def opciones(plan: Dict, estimacion: Dict, consumido_min: float = 0.0, modelo: Optional[Dict] = None,
             relevancia: str = "MEDIA", fases_restantes: Optional[Sequence[str]] = None, pv2_pendiente: bool = False) -> Dict:
    """Opciones de CT-B-05 (9.9) y recomendación. `pv2_pendiente`: PV2 aún no evaluada (añade `HASTA_PV2`)."""
    p80 = consumido_min + float(estimacion["minutos_p80"])
    ops: List[Dict] = [{"opcion": "CONTINUAR", "minutos_p80": round(p80, 1), "uc_p80": estimacion.get("uc_p80")}]
    # V2.1: el recorte apunta al 90 % del umbral para absorber la desviación observada que escala la proyección
    vr = version_recortada(plan, 0.9 * UMBRAL_PT30_MIN, modelo, consumido_min, fases_restantes)
    ops.append({k: v for k, v in vr.items() if k != "plan_modificado"})
    resto = list(fases_restantes) if fases_restantes is not None else list(FASES)
    f1 = [f for f in resto if f != "F5"]
    f2 = [f for f in ("F5", "F6", "F7", "F8", "F9", "F10") if f in resto or "F5" in resto]
    e1 = estimar(plan, modelo, f1)["minutos_p80"]
    e2 = estimar(plan, modelo, f2)["minutos_p80"] if "F5" in resto else 0.0
    if "F5" in resto:
        ops.append({"opcion": "DIVIDIR_EN_FASES", "fases": [
            {"fase": 1, "contenido": "ámbito y veredicto (sin selección de candidatos)", "minutos_p80": round(consumido_min + e1, 1)},
            {"fase": 2, "contenido": "selección de candidatos, refutación de finalistas y entregables", "minutos_p80": round(e2, 1)}]})
    if pv2_pendiente:
        est_r = estimar(plan, modelo, resto)
        ops.append({"opcion": "HASTA_PV2", "minutos_p80": round(consumido_min + est_r["minutos_p80_hasta_pv2"], 1),
                    "que_se_decide_despues": "capas 3 y 4 con el resultado de PV2 (si no se supera, informe de parada sin más consumo)"})
    ops.append({"opcion": "CANCELAR", "se_entrega": "resumen N0 de lo hecho"})
    if pv2_pendiente and p80 > 60 and relevancia != "ALTA" and consumido_min + estimar(plan, modelo, resto)["minutos_p80_hasta_pv2"] <= UMBRAL_PT30_MIN:
        return {"opciones": ops, "recomendacion_bloque": {"opcion": "HASTA_PV2", "motivo": "las capas 0–2 caben en 30 min y PV2 decide si merece la pena el resto"},
                "plan_recortado": vr["plan_modificado"]}
    if p80 > 120 and "F5" in resto:
        rec, mot = "DIVIDIR_EN_FASES", "la estimación supera 120 min: un entregable intermedio reduce el riesgo de espera"
    elif relevancia == "ALTA" or p80 <= 1.5 * UMBRAL_PT30_MIN:
        rec, mot = "CONTINUAR", ("relevancia ALTA: el tiempo adicional reduce incertidumbres que pueden cambiar el veredicto"
                                 if relevancia == "ALTA" else "el exceso es moderado y el recorte reduciría E")
    elif vr["alcanza_objetivo"] and vr["efecto_previsible"]["veredicto_max"] != "VIGILAR":
        rec, mot = "VERSION_30_MIN", "el recorte cabe en 30 min sin rebajar el veredicto máximo a VIGILAR"
    else:
        rec, mot = ("DIVIDIR_EN_FASES", "el recorte rebajaría el veredicto máximo; mejor por fases") if "F5" in resto \
            else ("CONTINUAR", "quedan pocas fases")
    return {"opciones": ops, "recomendacion_bloque": {"opcion": rec, "motivo": mot}, "plan_recortado": vr["plan_modificado"]}


# ==============================================================================================================
# Política de autorización automática
# ==============================================================================================================
def aplicar_politica(reglas: Sequence[Dict], contexto: Dict, minutos_necesarios: float,
                     tope_min: float = TOPE_AUTOMATICO_MIN) -> Dict:
    """Primera regla cuya condición se cumple. Condición: claves relevancia, nivel (lista o valor), origen,
    siguiente_paso_A, puerta, minutos_max (p80 ≤ valor) y minutos_p80_min (p80 ≥ valor); None = cualquiera.
    Acciones: AUTORIZAR_HASTA (minutos), ELEGIR_OPCION (opcion),
    NO_AUTORIZAR. Por encima del tope absoluto la decisión es siempre manual."""
    tope = min(float(tope_min), TOPE_AUTOMATICO_MAX_MIN)
    for r in reglas or []:
        cond = r.get("condicion") or {}
        ok = True
        for k, v in cond.items():
            if v is None or v == [] or v == {}:
                continue
            real = contexto.get(k)
            if isinstance(v, (list, tuple)):
                ok = real in v
            elif k == "minutos_max":
                ok = minutos_necesarios <= float(v)
            elif k == "minutos_p80_min":       # la regla aplica si el p80 necesario alcanza este valor (Runbook 3.3, POL-3)
                ok = minutos_necesarios >= float(v)
            else:
                ok = real == v
            if not ok:
                break
        if not ok:
            continue
        accion = r.get("accion")
        if accion == "AUTORIZAR_HASTA":
            lim = min(float(r.get("minutos") or 0), tope)
            if minutos_necesarios <= lim:
                return {"regla_id": r.get("regla_id"), "resultado": "AUTORIZA", "opcion": "CONTINUAR",
                        "minutos_autorizados": round(minutos_necesarios, 1), "limite_regla": lim}
            continue
        if accion == "ELEGIR_OPCION":
            op = r.get("opcion")
            if op not in OPCIONES:
                raise ErrorEntrada(f"Opción de política desconocida {op}")
            if op == "CONTINUAR" and minutos_necesarios > tope:
                continue
            return {"regla_id": r.get("regla_id"), "resultado": "AUTORIZA", "opcion": op,
                    "minutos_autorizados": round(min(minutos_necesarios, tope), 1)}
        if accion == "NO_AUTORIZAR":
            return {"regla_id": r.get("regla_id"), "resultado": "NO_CUBRE", "opcion": None}
    return {"regla_id": None, "resultado": "NO_CUBRE", "opcion": None,
            "nota": "ninguna regla cubre el caso o se supera el tope absoluto: decisión manual del Broker"}


def estado_autorizacion(solicitada: str, ahora: str, recordatorio_h: float = 24, caducidad_dias: float = 7) -> str:
    """PENDIENTE, RECORDATORIO (≥ 24 h) o CADUCADA (≥ 7 días)."""
    t0 = dt.datetime.fromisoformat(solicitada)
    t1 = dt.datetime.fromisoformat(ahora)
    if t0.tzinfo is None and t1.tzinfo is not None:
        t0 = t0.replace(tzinfo=t1.tzinfo)
    if t1.tzinfo is None and t0.tzinfo is not None:
        t1 = t1.replace(tzinfo=t0.tzinfo)
    h = (t1 - t0).total_seconds() / 3600
    if h >= caducidad_dias * 24:
        return "CADUCADA"
    if h >= recordatorio_h:
        return "RECORDATORIO"
    return "PENDIENTE"


# ==============================================================================================================
# Puntos de control
# ==============================================================================================================
def _huella(datos: Dict) -> str:
    return hashlib.sha256(json.dumps(datos, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")).hexdigest()


def guardar_punto_control(carpeta, checkpoint_id: str, datos: Dict) -> Path:
    """Guarda un punto de control seguro (todo lo producido ya registrado) con huella de integridad."""
    c = Path(carpeta)
    c.mkdir(parents=True, exist_ok=True)
    cuerpo = {"checkpoint_id": checkpoint_id, "version": VERSION, "datos": datos}
    cuerpo["huella"] = _huella({k: v for k, v in cuerpo.items() if k != "huella"})
    ruta = c / f"{checkpoint_id}.json"
    tmp = ruta.with_suffix(".tmp")
    tmp.write_text(json.dumps(cuerpo, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    tmp.replace(ruta)   # escritura atómica: nunca un punto de control a medias
    return ruta


def cargar_punto_control(ruta) -> Dict:
    cuerpo = json.loads(Path(ruta).read_text(encoding="utf-8"))
    h = cuerpo.get("huella")
    if h != _huella({k: v for k, v in cuerpo.items() if k != "huella"}):
        raise ErrorEntrada(f"Punto de control {ruta} alterado (huella no coincide)")
    return cuerpo["datos"]


# ==============================================================================================================
# Recalibración del modelo (Evaluador)
# ==============================================================================================================
def recalibrar(historial: Sequence[Dict], modelo: Optional[Dict] = None) -> Dict:
    """`historial`: [{fase, estimado_p50, real}]. Factor por fase = mediana(real/estimado) × factor vigente si hay
    ≥ muestra mínima; recortado a la banda. Devuelve factores nuevos y error medio por fase."""
    m = _modelo(modelo)
    lo, hi = m["banda_factores"]
    out = dict(m["factores"])
    informe = {}
    for f in FASES:
        filas = [h for h in historial if h.get("fase") == f and float(h.get("estimado_p50") or 0) > 0]
        if len(filas) < m["muestra_minima_recalibrar"]:
            informe[f] = {"n": len(filas), "aplicado": False}
            continue
        ratios = [float(h["real"]) / float(h["estimado_p50"]) for h in filas]
        nuevo = min(max(out.get(f, 1.0) * statistics.median(ratios), lo), hi)
        informe[f] = {"n": len(filas), "aplicado": True, "factor_anterior": out.get(f, 1.0), "factor_nuevo": round(nuevo, 3),
                      "error_medio_abs_min": round(statistics.mean(abs(float(h["real"]) - float(h["estimado_p50"])) for h in filas), 2)}
        out[f] = round(nuevo, 3)
    return {"factores": out, "informe": informe}


# ==============================================================================================================
# Cronómetro, consumo y colas
# ==============================================================================================================
class Cronometro:
    """Cronometraje por fase y agente. `reloj` devuelve minutos (real o simulado)."""

    def __init__(self, reloj: Callable[[], float], consumido_previo: float = 0.0) -> None:
        self.reloj = reloj
        self.base = consumido_previo
        self.t0 = reloj()
        self.fases: Dict[str, float] = {}
        self.agentes: Dict[str, float] = {}
        self.uc: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._abiertas: Dict[str, float] = {}

    def consumido(self) -> float:
        return round(self.base + self.reloj() - self.t0, 3)

    def abrir(self, fase: str) -> None:
        self._abiertas[fase] = self.reloj()

    def cerrar(self, fase: str, uc: float = 0.0) -> float:
        t = self.reloj() - self._abiertas.pop(fase, self.reloj())
        with self._lock:
            self.fases[fase] = round(self.fases.get(fase, 0.0) + t, 3)
            self.uc[fase] = round(self.uc.get(fase, 0.0) + uc, 3)
        return t

    def agente(self, agente: str, minutos: float) -> None:
        with self._lock:
            self.agentes[agente] = round(self.agentes.get(agente, 0.0) + minutos, 3)

    def resumen(self) -> Dict:
        return {"consumido_min": self.consumido(), "por_fase_min": dict(self.fases), "por_agente_min": dict(self.agentes),
                "uc_por_fase": dict(self.uc), "uc_total": round(sum(self.uc.values()), 2)}


def ordenes_instancias(colas: Dict[str, int], tiempos_respuesta: Optional[Dict[str, float]] = None,
                       objetivos: Optional[Dict[str, float]] = None, umbral_cola: int = 3,
                       instancia_unica: Sequence[str] = ("AG-B01", "AG-B21", "AG-B22", "AG-B23")) -> List[Dict]:
    """R29: abrir instancia si la cola > umbral o la respuesta > 2× objetivo (solo agentes sin estado)."""
    out = []
    for ag, q in colas.items():
        lento = bool(tiempos_respuesta and objetivos and ag in objetivos
                     and tiempos_respuesta.get(ag, 0) > 2 * objetivos[ag])
        if q > umbral_cola or lento:
            if ag in instancia_unica:
                out.append({"agente": ag, "accion": "REORDENAR", "motivo": "instancia única con cola"})
            else:
                out.append({"agente": ag, "accion": "ABRIR", "motivo": "cola > umbral" if q > umbral_cola else
                            "respuesta > 2× objetivo", "instancias_adicionales": max(1, math.ceil(q / umbral_cola) - 1)})
    return out


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="HT-08 · Estimación de tiempo y puerta de 30 minutos (Bloque B)")
    ap.add_argument("plan", help="JSON con el plan (nivel, profundidad, especialistas_activos, tipos_activo, …)")
    ap.add_argument("--limite", type=float, help="Límite PERS o tiempo de un N3 expreso (min)")
    ap.add_argument("--n3-expreso", action="store_true")
    a = ap.parse_args(argv)
    try:
        plan = json.load(open(a.plan, encoding="utf-8"))
        est = estimar(plan, plan.get("modelo"))
        pp = puerta_previa(est, plan.get("nivel", "N2"), a.limite, a.n3_expreso)
        res = {"estimacion": est, "puerta_previa": pp}
        if pp["dispara"]:
            res["opciones"] = {k: v for k, v in opciones(plan, est).items() if k != "plan_recortado"}
    except (ErrorEntrada, KeyError, json.JSONDecodeError) as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 3
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 1 if pp["dispara"] else 0


if __name__ == "__main__":
    sys.exit(main())
