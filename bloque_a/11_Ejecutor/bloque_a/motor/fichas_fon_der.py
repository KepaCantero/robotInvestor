"""Fichas FON (PERF-ETF) y DER (PERF-DER) del Catálogo de cálculos del Motor V5.0 (T-106, Motor Fase 1).

Fichas: FON-DISC-001, FON-FLOW-001, FON-TD-001, FON-LEV-001 (sección 16 del Catálogo) y DER-VRP-001,
DER-SKEW-001, DER-TERM-001, DER-ROLL-001 (sección 17). DER-OPT-001 no está aquí.

Convenciones (sección 3 del Catálogo): rendimientos simples; anualización 252 sesiones con capitalización
compuesta; recuento de días Real/365 salvo convención de mercado; cuantiles de tipo 7 (lineales, los de NumPy
por defecto); redondeo solo al final (aquí no se redondea: lo hace la entrega). Tasas, volatilidades y
rentabilidades de ENTRADA van en tanto por uno (0,20 = 20 %); las SALIDAS llevan la unidad en el nombre de la
clave (``_pct``, ``_pp``, ``_pb``, ``_puntos``) y en ``unidades``. «Puntos» de volatilidad = σ·100; «puntos»
de varianza = (σ·100)². Los percentiles son la fracción (0–1) de la historia menor o igual que el valor
(misma convención que ``operaciones.posicion_historica``); los z-scores usan la desviación muestral (n − 1)
y valen ``None`` si la historia no varía (nunca 0 por defecto).

Interfaz de cada manejador: ``f(ent, params) -> (resultado, limitaciones)`` con
``ent = {"valores": {...}, "series": {...}, "series_rol": {rol: pd.Series}}``. Todo es determinista (sin
aleatoriedad) y falla cerrado: entradas insuficientes o incoherentes ⇒ ``ErrorFicha`` con el motivo.
"""
from __future__ import annotations

import itertools
import math
from collections.abc import Callable
from typing import Any

import numpy as np
import pandas as pd
from scipy import optimize, stats

from . import operaciones as op
from .operaciones import ErrorFicha

# --------------------------------------------------------------------------------------------- convenciones
SESIONES_ANIO = 252          # §3.1: anualización en 252 sesiones
DIAS_ANIO = 365              # §3.1: recuento Real/365
MESES_ANIO = 12              # calendario
A_PCT = 100.0                # tanto por uno → %
A_PB = 10000.0               # tanto por uno → puntos básicos
LAMBDA_EWMA = 0.94           # §3.3: RI-EWMA (λ = 0,94)

# --------------------------------------------------------------------------------------------- parámetros
# Valores por defecto tal como los da el campo «Parámetros» de cada ficha (y, donde se indica, el «Método»).
PARAMETROS_POR_DEFECTO: dict[str, dict[str, Any]] = {
    # FON-DISC-001 «Parámetros»: ventana_media (52 semanas; 26–260); ventana_larga (5 años); kappa (0,5; 0–1);
    # agregacion (mediana).
    "FON-DISC-001": {"ventana_media": 52, "ventana_larga": 5, "kappa": 0.5, "agregacion": "mediana"},
    # FON-FLOW-001 «Parámetros»: ventanas (1, 3, 12 meses); ventana_z (36 meses); taxonomia (la del proveedor,
    # declarada: sin valor por defecto). «Método» (iii) autocorrelación de orden 1–3; (v) señal contraria
    # opcional con percentil > 95 o < 5.
    "FON-FLOW-001": {"ventanas": [1, 3, 12], "ventana_z": 36, "taxonomia": None,
                     "ordenes_autocorrelacion": [1, 2, 3], "senal_contraria": False,
                     "percentiles_contrarios": [0.05, 0.95]},
    # FON-TD-001 «Parámetros»: frecuencia (diaria para TE; anual para TD); variante_indice (neta);
    # agregacion (mediana).
    "FON-TD-001": {"frecuencia": "diaria", "variante_indice": "neta", "agregacion": "mediana"},
    # FON-LEV-001 «Parámetros»: L (2; −3 a 3); horizonte (20–250 sesiones, sin valor por defecto);
    # rejilla_sigma (10–80 %); n_trayectorias (10 000, solo para la simulación, que no se sirve aquí).
    # L se exige declarado en los datos (rechazo «sin L declarado»): el 2 de la ficha no se aplica en silencio.
    "FON-LEV-001": {"L": 2, "horizonte": None, "rejilla_sigma": [0.10, 0.80], "n_trayectorias": 10000},
    # DER-VRP-001 «Parámetros»: plazo (30 días; 7–90); prevision_rv (HAR; GARCH; realizada pasada);
    # ventana_percentil (5 años). nivel_es: la ficha no lo fija; se toma el nivel por defecto de RISK-VAR-001
    # (0,975), la ficha del Catálogo para el ES.
    "DER-VRP-001": {"plazo": 30, "prevision_rv": "HAR", "ventana_percentil": 5, "nivel_es": 0.975},
    # DER-SKEW-001 «Parámetros»: delta (25; 10–25); vencimiento (3 meses; 1–12); metodo (deltas; SVI).
    # «Método» (iv): protección estándar = put al 90 % a 3 meses.
    "DER-SKEW-001": {"delta": 25, "vencimiento": 3, "metodo": "deltas",
                     "proteccion_moneyness": 0.90, "proteccion_meses": 3},
    # DER-TERM-001 «Parámetros»: vencimientos (1, 3, 6, 12 meses); interpolacion (varianza_total).
    # «Método» (ii): pendiente = σ(3m) − σ(1m); inversión si σ(1m)/σ(3m) > 1.
    "DER-TERM-001": {"vencimientos": [1, 3, 6, 12], "interpolacion": "varianza_total", "pendiente_meses": [1, 3]},
    # DER-ROLL-001 «Parámetros»: anualizacion (365; 360 en mercados monetarios); pares (1–2).
    "DER-ROLL-001": {"anualizacion": 365, "pares": [1, 2]},
}

# Rangos admitidos de los parámetros (campo «Parámetros» de la ficha; FON-DISC ventana_larga: «3–5 años» del Método).
RANGOS: dict[str, dict[str, tuple[float, float]]] = {
    "FON-DISC-001": {"ventana_media": (26, 260), "ventana_larga": (3, 5), "kappa": (0, 1)},
    "FON-LEV-001": {"L": (-3, 3), "horizonte": (20, 250), "rejilla_sigma": (0.10, 0.80)},
    "DER-VRP-001": {"plazo": (7, 90)},
    "DER-SKEW-001": {"delta": (10, 25), "vencimiento": (1, 12)},
}

# Mínimos de «Entradas mínimas» y de «Aclaración y rechazo» de cada ficha.
MINIMOS: dict[str, dict[str, Any]] = {
    # ≥ 5 miembros; ≥ 3 años (≥ 5 recomendados); NAV ≥ semanal; NAV de antigüedad ≤ 6 meses (≤ 12 en privados).
    "FON-DISC-001": {"miembros": 5, "anios": 3, "anios_recomendados": 5, "semanas_nav": 1,
                     "meses_nav": 6, "meses_nav_privados": 12},
    # Mensual ≥ 3 años o semanal ≥ 1 año; rechazo con < 12 meses.
    "FON-FLOW-001": {"anios_mensual": 3, "anios_semanal": 1, "meses_rechazo": 12},
    # ≥ 5 miembros; ≥ 3 años.
    "FON-TD-001": {"miembros": 5, "anios": 3},
    # Rentabilidades diarias del índice ≥ 1 año.
    "FON-LEV-001": {"anios": 1},
    # ≥ 3 años (≥ 5 recomendados); rechazo con < 2 años; superficie con ≥ 5 precios de ejercicio.
    "DER-VRP-001": {"anios": 3, "anios_recomendados": 5, "anios_rechazo": 2, "strikes": 5},
    # ≥ 5 precios de ejercicio; diaria ≥ 2 años; percentil frente a ≥ 3 años.
    "DER-SKEW-001": {"strikes": 5, "anios": 2, "anios_percentil": 3},
    # ≥ 3 vencimientos; diaria ≥ 2 años; percentil ≥ 3 años.
    "DER-TERM-001": {"vencimientos": 3, "anios": 2, "anios_percentil": 3},
    # ≥ 2 vencimientos; percentil frente a ≥ 5 años.
    "DER-ROLL-001": {"vencimientos": 2, "anios_percentil": 5},
}


# =========================================================================================== utilidades
def _p(ficha: str, params: dict | None) -> dict[str, Any]:
    """Parámetros efectivos: los de la petición encima de los de la ficha (idempotente si ya vienen fusionados)."""
    p = dict(PARAMETROS_POR_DEFECTO[ficha])
    p.update(params or {})
    return p


def _rango(ficha: str, nombre: str, valor: float) -> None:
    lo, hi = RANGOS[ficha][nombre]
    if not lo <= valor <= hi:
        raise ErrorFicha(f"{ficha}: parámetro {nombre}={valor} fuera del rango admitido [{lo}, {hi}]")


def _num(d: dict, clave: str, ficha: str, *, positivo: bool = False, ctx: str = "") -> float:
    if not isinstance(d, dict) or d.get(clave) is None:
        raise ErrorFicha(f"{ficha}: falta «{clave}»{ctx}")
    try:
        x = float(d[clave])
    except (TypeError, ValueError) as e:
        raise ErrorFicha(f"{ficha}: «{clave}» no es numérico{ctx}") from e
    if not math.isfinite(x):
        raise ErrorFicha(f"{ficha}: «{clave}» no es finito{ctx}")
    if positivo and x <= 0:
        raise ErrorFicha(f"{ficha}: «{clave}» debe ser positivo{ctx}")
    return x


def _vector(d: dict, clave: str, ficha: str, *, positivo: bool = False, ctx: str = "") -> np.ndarray:
    if not isinstance(d, dict) or d.get(clave) is None:
        raise ErrorFicha(f"{ficha}: falta «{clave}»{ctx}")
    try:
        a = np.asarray(d[clave], dtype=float)
    except (TypeError, ValueError) as e:
        raise ErrorFicha(f"{ficha}: «{clave}» no es una lista numérica{ctx}") from e
    if a.ndim != 1 or a.size == 0:
        raise ErrorFicha(f"{ficha}: «{clave}» debe ser una lista no vacía{ctx}")
    if not np.all(np.isfinite(a)):
        raise ErrorFicha(f"{ficha}: «{clave}» tiene huecos o valores no finitos (no se rellenan){ctx}")
    if positivo and np.any(a <= 0):
        raise ErrorFicha(f"{ficha}: «{clave}» debe ser estrictamente positivo{ctx}")
    return a


def _fecha(x: Any, ficha: str, clave: str) -> pd.Timestamp:
    try:
        t = pd.Timestamp(x)
    except (TypeError, ValueError) as e:
        raise ErrorFicha(f"{ficha}: «{clave}» no es una fecha válida") from e
    if t is pd.NaT:
        raise ErrorFicha(f"{ficha}: «{clave}» no es una fecha válida")
    return t


def _fechas(d: dict, clave: str, ficha: str) -> pd.DatetimeIndex:
    if not isinstance(d, dict) or not d.get(clave):
        raise ErrorFicha(f"{ficha}: faltan las fechas «{clave}»")
    try:
        f = pd.DatetimeIndex(pd.to_datetime(list(d[clave])))
    except (TypeError, ValueError) as e:
        raise ErrorFicha(f"{ficha}: «{clave}» contiene fechas no válidas") from e
    if f.hasnans or not f.is_monotonic_increasing or not f.is_unique:
        raise ErrorFicha(f"{ficha}: «{clave}» debe ser estrictamente creciente y sin huecos de fecha")
    return f


def _posicion(valor: float, historia: np.ndarray, tol: float) -> dict[str, Any]:
    """Posición frente a la historia: percentil (fracción ≤ valor) y z-score (desviación n − 1).

    Si la desviación no supera la tolerancia de la ficha (relativa a la escala de la historia), la historia no
    varía y el z-score no está definido: ``None`` (el ruido de redondeo no se convierte en señal).
    """
    h = np.asarray(historia, dtype=float)
    media = float(np.mean(h))
    sd = float(np.std(h, ddof=1)) if h.size > 1 else float("nan")
    escala = max(float(np.max(np.abs(h))), abs(valor))
    definido = math.isfinite(sd) and sd > tol * escala
    return {"n": int(h.size), "media": media, "desviacion": sd if math.isfinite(sd) else None,
            "z": float((valor - media) / sd) if definido else None,
            "percentil": float(np.mean(h <= valor))}


def _cuantil(a: np.ndarray, q: float) -> float:
    return float(np.quantile(a, q))   # tipo 7 (interpolación lineal), §3 del Catálogo


def _autocorrelacion(x: np.ndarray, k: int) -> float | None:
    d = x - float(np.mean(x))
    den = float(np.sum(d * d))
    if den == 0 or k >= x.size:
        return None
    return float(np.sum(d[k:] * d[:-k]) / den)


def _ar1(x: np.ndarray, tol: float) -> tuple[float | None, float | None]:
    """AR(1) por MCO: x_t = a + φ·x_{t−1}; vida media = ln(½)/ln(φ) en periodos (solo con 0 < φ < 1).

    Una serie que no varía más allá de la tolerancia de la ficha no identifica φ: ``(None, None)``.
    """
    xl, y = x[:-1], x[1:]
    if xl.size < 3 or float(np.ptp(x)) <= tol * float(np.max(np.abs(x))):
        return None, None
    coef, *_ = np.linalg.lstsq(np.column_stack([np.ones_like(xl), xl]), y, rcond=None)
    phi = float(coef[1])
    return phi, (math.log(0.5) / math.log(phi) if 0 < phi < 1 else None)


def _pendiente_mco(y: np.ndarray) -> float:
    x = np.arange(y.size, dtype=float)
    coef, *_ = np.linalg.lstsq(np.column_stack([np.ones_like(x), x]), y, rcond=None)
    return float(coef[1])


def _black(F: float, K: float, sigma: float, T: float, call: bool) -> float:
    """Precio de Black sin descontar (medida forward)."""
    sd = sigma * math.sqrt(T)
    d1 = (math.log(F / K) + 0.5 * sd * sd) / sd
    d2 = d1 - sd
    if call:
        return float(F * stats.norm.cdf(d1) - K * stats.norm.cdf(d2))
    return float(K * stats.norm.cdf(-d2) - F * stats.norm.cdf(-d1))


def _delta_call_forward(k: float, sigma: float, T: float) -> float:
    """Delta forward de la call sin prima: N(d1), con k = ln(K/F)."""
    sd = sigma * math.sqrt(T)
    return float(stats.norm.cdf((-k + 0.5 * sd * sd) / sd))


def _clave_mes(x: Any) -> str:
    return f"{float(x):g}"


def _diaria_por_fechas(f: pd.DatetimeIndex) -> bool:
    """Datos diarios: la separación mediana entre observaciones es de un día."""
    return bool(f.size > 1 and pd.Series(f).diff().dropna().median() == pd.Timedelta(days=1))


# =========================================================================================== FON-DISC-001
def f_fon_disc(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """FON-DISC-001 · Descuento de fondos cerrados frente a su media (MC-09).

    ``valores``: ``fechas`` (lista ISO, común, NAV al menos semanal, ≥ 3 años); ``miembros`` =
    {id: {"precio": [...], "nav": [...] (alineados con ``fechas``), "fecha_nav": fecha del último NAV publicado,
    "capitalizacion": escalar o lista (opcional; segunda vía ponderada), "subcategoria" (opcional),
    "privado" (bool, opcional; también ``activos_privados`` a nivel de categoría), "ajuste_nav_declarado"
    (texto, si el NAV supera la antigüedad máxima)}}; opcionales ``rentabilidad_nav_supuesta`` (tanto por uno a H)
    y ``catalizadores`` (lista declarada, paso v). Sin rol de series: las entradas son por miembro y en línea.
    """
    F = "FON-DISC-001"
    p, m, v = _p(F, params), MINIMOS[F], ent.get("valores") or {}
    for n in ("ventana_media", "ventana_larga", "kappa"):
        _rango(F, n, float(p[n]))
    if p["agregacion"] not in ("mediana", "media_ponderada"):
        raise ErrorFicha(f"{F}: agregacion «{p['agregacion']}» no admitida (mediana | media_ponderada)")
    fechas = _fechas(v, "fechas", F)
    miembros = v.get("miembros")
    if not isinstance(miembros, dict) or len(miembros) < m["miembros"]:
        raise ErrorFicha(f"{F}: rechazo con < {m['miembros']} miembros")
    corte = fechas[-1]
    if fechas[0] > corte - pd.DateOffset(years=m["anios"]):
        raise ErrorFicha(f"{F}: historia de precio y NAV inferior a {m['anios']} años")
    paso = pd.Series(fechas).diff().dropna().median()
    if paso > pd.Timedelta(weeks=m["semanas_nav"]):
        raise ErrorFicha(f"{F}: NAV con frecuencia inferior a la semanal (separación mediana {paso})")
    lim: list[str] = [("NAV retrasados (privados, inmobiliario) sesgan el descuento; descuentos persistentes por "
                      "comisiones, apalancamiento, fiscalidad o iliquidez; la reversión no está garantizada y el "
                      "descuento puede ampliarse en crisis de liquidez")]
    if fechas[0] > corte - pd.DateOffset(years=m["anios_recomendados"]):
        lim.append(f"historia inferior a los {m['anios_recomendados']} años recomendados")
    nombres = sorted(miembros)
    filas, pesos, subcat = [], [], []
    for nom in nombres:
        mb, ctx = miembros[nom], f" (miembro {nom})"
        if not isinstance(mb, dict):
            raise ErrorFicha(f"{F}: miembro {nom} mal formado")
        pr = _vector(mb, "precio", F, positivo=True, ctx=ctx)
        nav = _vector(mb, "nav", F, positivo=True, ctx=ctx)
        if pr.size != fechas.size or nav.size != fechas.size:
            raise ErrorFicha(f"{F}: precio y NAV deben estar alineados con «fechas»{ctx}")
        if not mb.get("fecha_nav"):
            raise ErrorFicha(f"{F}: rechazo sin fecha de NAV{ctx}")
        fnav = _fecha(mb["fecha_nav"], F, "fecha_nav")
        if fnav > corte:
            raise ErrorFicha(f"{F}: fecha de NAV posterior a la fecha de corte{ctx}")
        privado = bool(mb.get("privado", v.get("activos_privados", False)))
        meses = m["meses_nav_privados"] if privado else m["meses_nav"]
        if fnav < corte - pd.DateOffset(months=meses):
            if not mb.get("ajuste_nav_declarado"):
                raise ErrorFicha(f"{F}: rechazo con NAV de antigüedad > {meses} meses sin ajuste declarado{ctx}")
            lim.append(f"miembro {nom}: NAV de {fnav.date()} (> {meses} meses); ajuste declarado: "
                       f"{mb['ajuste_nav_declarado']}")
        filas.append(pr / nav - 1)
        if mb.get("capitalizacion") is not None:
            try:
                c = np.asarray(mb["capitalizacion"], dtype=float)
            except (TypeError, ValueError) as e:
                raise ErrorFicha(f"{F}: capitalización no numérica{ctx}") from e
            c = np.full(fechas.size, float(c)) if c.ndim == 0 else c
            if c.size != fechas.size or not np.all(np.isfinite(c)) or np.any(c <= 0):
                raise ErrorFicha(f"{F}: capitalización no válida o no alineada{ctx}")
            pesos.append(c)
        subcat.append(str(mb.get("subcategoria") or "(sin subcategoría)"))
    D = np.vstack(filas)                                   # miembros × fechas
    mediana = np.median(D, axis=0)
    ponderada = None
    if len(pesos) == len(nombres):
        W = np.vstack(pesos)
        ponderada = np.sum(D * W, axis=0) / np.sum(W, axis=0)
    elif p["agregacion"] == "media_ponderada":
        raise ErrorFicha(f"{F}: agregacion media_ponderada sin capitalización de todos los miembros")
    else:
        lim.append("sin capitalización de todos los miembros: no hay segunda vía (media ponderada)")
    agregado = ponderada if p["agregacion"] == "media_ponderada" and ponderada is not None else mediana
    d = float(agregado[-1])
    m_media = fechas > corte - pd.Timedelta(weeks=float(p["ventana_media"]))
    meses_larga = round(float(p["ventana_larga"]) * MESES_ANIO)
    m_larga = fechas > corte - pd.DateOffset(months=meses_larga)
    if fechas[0] > corte - pd.DateOffset(months=meses_larga):
        lim.append(f"ventana_larga de {p['ventana_larga']} años mayor que la historia: se usa la disponible")
    tol = FICHAS[F]["tol"]
    pos_media, pos_larga = _posicion(d, agregado[m_media], tol), _posicion(d, agregado[m_larga], tol)
    kappa = float(p["kappa"])
    normalizacion: dict[str, Any] = {}
    for clave, pos in (("ventana_media", pos_media), ("ventana_larga", pos_larga)):
        d_obj = d + kappa * (pos["media"] - d)
        normalizacion[clave] = {"descuento_objetivo_pct": d_obj * A_PCT,
                                "rentabilidad_normalizacion_pct": ((1 + d_obj) / (1 + d) - 1) * A_PCT}
    r_nav = v.get("rentabilidad_nav_supuesta")
    if r_nav is not None:
        r_nav = _num(v, "rentabilidad_nav_supuesta", F)
        for blo in normalizacion.values():   # identidad exacta: P_H/P_0 = (1 + d_obj)/(1 + d) · NAV_H/NAV_0
            blo["rentabilidad_total_supuesta_pct"] = (
                (1 + blo["rentabilidad_normalizacion_pct"] / A_PCT) * (1 + r_nav) - 1) * A_PCT
    else:
        lim.append("sin rentabilidad supuesta del NAV: solo se entrega la rentabilidad por normalización")
    phi, vida = _ar1(agregado, tol)
    vida_meses = vida * paso.days * MESES_ANIO / DIAS_ANIO if vida is not None else None
    if vida is None:
        lim.append("AR(1) del descuento agregado sin reversión (φ fuera de (0, 1) o serie constante): vida media no definida")
    ult = D[:, -1]
    desglose: dict[str, Any] = {}
    for s in sorted(set(subcat)):
        idx = [i for i, x in enumerate(subcat) if x == s]
        desglose[s] = {"n": len(idx), "descuento_mediana_pct": float(np.median(ult[idx])) * A_PCT}
    catal = v.get("catalizadores")
    if catal is None:
        lim.append("catalizadores agregados (paso v) no declarados")
    res = {
        "fecha_corte": str(corte.date()), "n_miembros": len(nombres), "agregacion": p["agregacion"],
        "descuento_agregado_pct": d * A_PCT,
        "descuento_mediana_pct": float(mediana[-1]) * A_PCT,
        "descuento_media_ponderada_pct": float(ponderada[-1]) * A_PCT if ponderada is not None else None,
        "z_scores": {"ventana_media": pos_media["z"], "ventana_larga": pos_larga["z"]},
        "medias_pct": {"ventana_media": pos_media["media"] * A_PCT, "ventana_larga": pos_larga["media"] * A_PCT},
        "percentil": pos_larga["percentil"],
        "dispersion_pp": {"desviacion": float(np.std(ult, ddof=1)) * A_PCT, "rango": float(np.ptp(ult)) * A_PCT},
        "phi_ar1": phi, "vida_media_meses": vida_meses,
        "rentabilidad_normalizacion_pct": normalizacion["ventana_media"]["rentabilidad_normalizacion_pct"],
        "normalizacion": normalizacion, "kappa": kappa,
        "desglose_subcategoria": desglose, "catalizadores": catal,
        "verificacion": {
            "minimo_miembros_pct": float(np.min(ult)) * A_PCT, "maximo_miembros_pct": float(np.max(ult)) * A_PCT,
            "agregado_entre_min_y_max": bool(np.min(ult) <= d <= np.max(ult)),
            "segunda_via_ponderada_menos_mediana_pp":
                (float(ponderada[-1]) - float(mediana[-1])) * A_PCT if ponderada is not None else None},
        "referencias_ingenuas": {"RI_MH_descuento_pct": pos_larga["media"] * A_PCT, "RI_PA_descuento_pct": d * A_PCT},
        "unidades": {"descuento": "%", "dispersion": "pp", "vida_media": "meses", "rentabilidad": "% a H"},
    }
    return res, lim


# =========================================================================================== FON-FLOW-001
def f_fon_flow(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """FON-FLOW-001 · Flujos por categoría de vehículos (MC-02).

    ``valores``: ``taxonomia`` (texto, fija y declarada; también vale en parámetros), ``frecuencia``
    ("mensual" | "semanal"), ``fechas`` (cierres regulares, sin huecos), ``categorias`` =
    {cat: {"aum": [...] (alineado con ``fechas``), "rentabilidad": [...] y/o "flujo": [...] (longitud
    len(fechas) − 1: el elemento i es el periodo (fechas[i], fechas[i+1]]), "gestion": "indexada" | "activa"
    (opcional)}}; opcional ``flujo_total_publicado`` (longitud len(fechas) − 1). Sin rol de series.
    """
    F = "FON-FLOW-001"
    p, m, v = _p(F, params), MINIMOS[F], ent.get("valores") or {}
    taxonomia = v.get("taxonomia") or p.get("taxonomia")
    if not taxonomia:
        raise ErrorFicha(f"{F}: rechazo sin taxonomía fija declarada")
    frec = v.get("frecuencia")
    if frec not in ("mensual", "semanal"):
        raise ErrorFicha(f"{F}: «frecuencia» debe declararse como mensual o semanal")
    fechas = _fechas(v, "fechas", F)
    if fechas.size < 2:
        raise ErrorFicha(f"{F}: se necesitan al menos dos cierres")
    if frec == "mensual":
        idx_mes = fechas.year * MESES_ANIO + fechas.month
        regular = bool(np.all(np.diff(np.asarray(idx_mes)) == 1))
    else:
        regular = bool(np.all(np.diff(fechas.values) == pd.Timedelta(weeks=1).to_timedelta64()))
    if not regular:
        raise ErrorFicha(f"{F}: las fechas no siguen la frecuencia {frec} declarada (huecos o duplicados)")
    corte = fechas[-1]
    if fechas[0] > corte - pd.DateOffset(months=m["meses_rechazo"]):
        raise ErrorFicha(f"{F}: rechazo con < {m['meses_rechazo']} meses de historia")
    anios = m["anios_mensual"] if frec == "mensual" else m["anios_semanal"]
    if fechas[0] > corte - pd.DateOffset(years=anios):
        raise ErrorFicha(f"{F}: frecuencia {frec} exige ≥ {anios} años de historia")
    cats = v.get("categorias")
    if not isinstance(cats, dict) or not cats:
        raise ErrorFicha(f"{F}: faltan las categorías")
    lim: list[str] = [("los flujos de vehículos cotizados incluyen creaciones y reembolsos de intermediarios y "
                      "coberturas; los flujos persiguen rentabilidades pasadas; la relación flujo–rentabilidad "
                      "futura es débil y cambiante")]
    if len(cats) < 2:
        lim.append("una sola categoría: el rango entre categorías no es informativo")
    ff = fechas[1:]
    nombres = sorted(cats)
    flujos: dict[str, np.ndarray] = {}
    aum_prev: dict[str, np.ndarray] = {}
    residuos_aum: dict[str, float | None] = {}
    agregado_via_aum = np.zeros(ff.size)
    todas_con_rent = True
    for c in nombres:
        cd, ctx = cats[c], f" (categoría {c})"
        if not isinstance(cd, dict):
            raise ErrorFicha(f"{F}: categoría {c} mal formada")
        aum = _vector(cd, "aum", F, positivo=True, ctx=ctx)
        if aum.size != fechas.size:
            raise ErrorFicha(f"{F}: «aum» no alineado con «fechas»{ctx}")
        r = _vector(cd, "rentabilidad", F, ctx=ctx) if cd.get("rentabilidad") is not None else None
        if r is not None and r.size != ff.size:
            raise ErrorFicha(f"{F}: «rentabilidad» debe tener len(fechas) − 1 elementos{ctx}")
        if cd.get("flujo") is not None:
            fl = _vector(cd, "flujo", F, ctx=ctx)
            if fl.size != ff.size:
                raise ErrorFicha(f"{F}: «flujo» debe tener len(fechas) − 1 elementos{ctx}")
            residuos_aum[c] = (float(np.max(np.abs(aum[1:] - aum[:-1] * (1 + r) - fl))) if r is not None else None)
            if r is None:
                lim.append(f"categoría {c}: flujos publicados sin rentabilidad: identidad de AUM no verificable")
        elif r is not None:
            fl = aum[1:] - aum[:-1] * (1 + r)          # paso (i)
            residuos_aum[c] = float(np.max(np.abs(aum[1:] - aum[:-1] * (1 + r) - fl)))
        else:
            raise ErrorFicha(f"{F}: faltan rentabilidad o flujos publicados{ctx}")
        if r is None:
            todas_con_rent = False
        else:
            agregado_via_aum = agregado_via_aum + aum[1:] - aum[:-1] * (1 + r)
        flujos[c], aum_prev[c] = fl, aum[:-1]
    ventanas = [int(k) for k in p["ventanas"]]
    vz = int(p["ventana_z"])
    if fechas[0] > corte - pd.DateOffset(months=vz):
        lim.append(f"historia menor que ventana_z ({vz} meses): z-score sobre la historia disponible")
    lo, hi = (float(x) for x in p["percentiles_contrarios"])
    tabla: dict[str, Any] = {}
    for c in nombres:
        fl, ap = flujos[c], aum_prev[c]
        rel = fl / ap                                    # paso (ii)
        acum: dict[str, Any] = {}
        for k in ventanas:
            mk = ff > corte - pd.DateOffset(months=k)
            i0 = int(np.argmax(mk))
            mon = float(np.sum(fl[mk]))
            acum[str(k)] = {"moneda": mon, "pct_aum": mon / float(ap[i0]) * A_PCT}
        mz = ff > corte - pd.DateOffset(months=vz)
        pos = _posicion(float(rel[-1]), rel[mz], FICHAS[F]["tol"])
        senal = None
        if p["senal_contraria"]:
            senal = ("ENTRADAS_EXTREMAS" if pos["percentil"] > hi else
                     "SALIDAS_EXTREMAS" if pos["percentil"] < lo else "NINGUNA")
        tabla[c] = {"flujo_ultimo": float(fl[-1]), "flujo_relativo_ultimo_pct": float(rel[-1]) * A_PCT,
                    "acumulados": acum, "z_score": pos["z"], "percentil": pos["percentil"],
                    "autocorrelaciones": {str(k): _autocorrelacion(rel, int(k)) for k in p["ordenes_autocorrelacion"]},
                    "gestion": cats[c].get("gestion"), "senal_contraria": senal}
    for k in ventanas:   # paso (iv): rango 1 = mayor flujo relativo acumulado (empates por nombre)
        orden = sorted(nombres, key=lambda c: (-tabla[c]["acumulados"][str(k)]["pct_aum"], c))
        for i, c in enumerate(orden, start=1):
            tabla[c].setdefault("rango", {})[str(k)] = i
    por_gestion: dict[str, Any] = {}
    for g in sorted({str(tabla[c]["gestion"]) for c in nombres if tabla[c]["gestion"]}):
        miembros_g = [c for c in nombres if str(tabla[c]["gestion"]) == g]
        por_gestion[g] = {}
        for k in ventanas:
            mk = ff > corte - pd.DateOffset(months=k)
            i0 = int(np.argmax(mk))
            mon = float(sum(np.sum(flujos[c][mk]) for c in miembros_g))
            base = float(sum(aum_prev[c][i0] for c in miembros_g))
            por_gestion[g][str(k)] = {"moneda": mon, "pct_aum": mon / base * A_PCT}
    total = np.sum(np.vstack([flujos[c] for c in nombres]), axis=0)
    if todas_con_rent:
        dif_total: float | None = float(np.max(np.abs(total - agregado_via_aum)))
    elif v.get("flujo_total_publicado") is not None:
        pub = _vector(v, "flujo_total_publicado", F)
        if pub.size != ff.size:
            raise ErrorFicha(f"{F}: «flujo_total_publicado» debe tener len(fechas) − 1 elementos")
        dif_total = float(np.max(np.abs(total - pub)))
    else:
        dif_total = None
        lim.append("sin rentabilidades ni flujo total publicado: la suma por categorías no tiene segunda vía")
    if p["senal_contraria"]:
        lim.append("señal contraria (paso v): hipótesis declarada, no regla")
    res = {
        "taxonomia": taxonomia, "frecuencia": frec, "fecha_corte": str(corte.date()),
        "categorias": tabla, "fechas_flujo": [str(x.date()) for x in ff],
        "flujo_total": [float(x) for x in total],
        "serie_flujos_acumulados": {c: [float(x) for x in np.cumsum(flujos[c])] for c in nombres},
        "por_gestion": por_gestion,
        "verificacion": {"suma_categorias_vs_total_max_abs": dif_total, "identidad_aum_residuo_max_abs": residuos_aum},
        "referencias_ingenuas": {"flujo_nulo": 0.0,
                                 "RI_PA_flujo_relativo_pct": {c: tabla[c]["flujo_relativo_ultimo_pct"] for c in nombres}},
        "unidades": {"flujo": "moneda", "flujo_relativo": "% de AUM", "acumulados": "moneda y % de AUM"},
    }
    return res, lim


# =========================================================================================== FON-TD-001
_COMPONENTES_TD = ("prestamo_valores", "diferencial_retencion", "efecto_replicacion", "efecto_caja")


def f_fon_td(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """FON-TD-001 · Diferencia de seguimiento agregada por categoría (MC-01; MC-09 invitado).

    ``valores``: ``rentabilidades_indice`` (diarias, totales, en la variante declarada), ``variante_indice``
    (obligatoria: si falta se pide aclaración), ``miembros`` = {id: {"rentabilidades": [...] (diarias, alineadas),
    "gastos_corrientes" (anual), "replicacion" (texto), "domicilio" (opcional), y componentes anuales opcionales
    con su signo: "prestamo_valores", "diferencial_retencion", "efecto_replicacion", "efecto_caja"}}.
    Años = bloques de 252 sesiones contados desde el final (el bloque incompleto inicial se descarta). Sin rol
    de series. La salida es la categoría o el segmento, nunca un ranking de vehículos.
    """
    F = "FON-TD-001"
    p, m, v = _p(F, params), MINIMOS[F], ent.get("valores") or {}
    variante = v.get("variante_indice")
    if not variante:
        raise ErrorFicha(f"{F}: ACLARACION_REQUERIDA: la variante del índice no se declara")
    if str(variante) != str(p["variante_indice"]):
        raise ErrorFicha(f"{F}: variante del índice declarada «{variante}» distinta de la del parámetro "
                         f"«{p['variante_indice']}»: TD espuria")
    if v.get("frecuencia", "diaria") != p["frecuencia"]:
        raise ErrorFicha(f"{F}: las rentabilidades deben ser {p['frecuencia']}s")
    miembros = v.get("miembros")
    if not isinstance(miembros, dict) or len(miembros) < m["miembros"]:
        raise ErrorFicha(f"{F}: rechazo con < {m['miembros']} miembros")
    ri = _vector(v, "rentabilidades_indice", F)
    n_bloques = ri.size // SESIONES_ANIO
    if n_bloques < m["anios"]:
        raise ErrorFicha(f"{F}: se necesitan ≥ {m['anios']} años ({m['anios'] * SESIONES_ANIO} sesiones) de rentabilidades")
    ini = ri.size - n_bloques * SESIONES_ANIO
    lim: list[str] = [("una variante del índice equivocada genera TD espuria; diferencias de hora de valoración; "
                      "con pocos miembros el agregado es frágil; salida por categoría o segmento, nunca ranking")]
    nombres = sorted(miembros)
    td, te, gastos, bloques = [], [], [], []
    comps: dict[str, list[float]] = {c: [] for c in _COMPONENTES_TD}
    for nom in nombres:
        mb, ctx = miembros[nom], f" (miembro {nom})"
        if not isinstance(mb, dict):
            raise ErrorFicha(f"{F}: miembro {nom} mal formado")
        rv = _vector(mb, "rentabilidades", F, ctx=ctx)
        if rv.size != ri.size:
            raise ErrorFicha(f"{F}: rentabilidades no alineadas con el índice{ctx}")
        gastos.append(_num(mb, "gastos_corrientes", F, ctx=ctx))
        if not mb.get("replicacion"):
            raise ErrorFicha(f"{F}: falta el método de replicación{ctx}")
        tdb = []
        for j in range(n_bloques):
            sl = slice(ini + j * SESIONES_ANIO, ini + (j + 1) * SESIONES_ANIO)
            tdb.append(float(np.prod(1 + rv[sl]) - np.prod(1 + ri[sl])))
        bloques.append(tdb)
        td.append(float(np.mean(tdb)))
        te.append(float(np.std(rv[ini:] - ri[ini:], ddof=1)) * math.sqrt(SESIONES_ANIO))
        for c in _COMPONENTES_TD:
            if mb.get(c) is not None:
                comps[c].append(_num(mb, c, F, ctx=ctx))
    td_a, te_a = np.asarray(td), np.asarray(te)
    td_med = float(np.median(td_a))
    descomp: dict[str, float] = {"gastos_corrientes": -float(np.mean(gastos)) * A_PB}
    for c in _COMPONENTES_TD:
        if len(comps[c]) == len(nombres):
            descomp[c] = float(np.mean(comps[c])) * A_PB
        else:
            lim.append(f"componente «{c}» no aportado por todos los miembros: queda en el residuo")
    td_media = float(np.mean(td_a)) * A_PB
    descomp["residuo"] = td_media - sum(descomp.values())
    mediana_bloques = np.median(np.asarray(bloques), axis=0)
    segmentos: dict[str, Any] = {}
    for attr in ("replicacion", "domicilio"):
        grupos: dict[str, list[int]] = {}
        for i, nom in enumerate(nombres):
            if miembros[nom].get(attr):
                grupos.setdefault(str(miembros[nom][attr]), []).append(i)
        if not grupos:
            continue
        segmentos[attr] = {}
        for g in sorted(grupos):
            med = float(np.median(td_a[grupos[g]]))
            segmentos[attr][g] = {"n": len(grupos[g]), "td_mediana_pb": med * A_PB,
                                  "diferencia_vs_categoria_pb": (med - td_med) * A_PB}
            if len(grupos[g]) < m["miembros"]:
                lim.append(f"segmento {attr}={g} con {len(grupos[g])} miembros (< {m['miembros']}): agregado frágil")
    res = {
        "n_miembros": len(nombres), "variante_indice": variante, "anios_completos": n_bloques,
        "td_mediana_pb": td_med * A_PB,
        "td_cuartiles_pb": {"q1": _cuantil(td_a, 0.25) * A_PB, "q3": _cuantil(td_a, 0.75) * A_PB},
        "td_dispersion_iqr_pb": (_cuantil(td_a, 0.75) - _cuantil(td_a, 0.25)) * A_PB,
        "te_mediano_pct": float(np.median(te_a)) * A_PCT,
        "te_cuartiles_pct": {"q1": _cuantil(te_a, 0.25) * A_PCT, "q3": _cuantil(te_a, 0.75) * A_PCT},
        "td_media_pb": td_media, "descomposicion_pb": descomp,
        "td_mediana_por_anio_pb": [float(x) * A_PB for x in mediana_bloques],
        "tendencia_pb_por_anio": _pendiente_mco(mediana_bloques) * A_PB,
        "segmentos": segmentos,
        "referencia_ingenua_td_pb": -float(np.mean(gastos)) * A_PB,
        "verificacion": {"descomposicion_mas_residuo_menos_td_pb": sum(descomp.values()) - td_media},
        "unidades": {"td": "pb anuales", "te": "% anual", "descomposicion": "pb", "tendencia": "pb por año"},
    }
    return res, lim


# =========================================================================================== FON-LEV-001
def _rend_diarios(ent: dict, F: str, rol: str, clave: str) -> tuple[np.ndarray, str]:
    """Rentabilidades diarias desde ``series_rol[rol]`` (precios) o ``valores[clave]`` (rentabilidades)."""
    v = ent.get("valores") or {}
    s = (ent.get("series_rol") or {}).get(rol)
    if s is not None:
        s = s.dropna().astype(float)
        if not isinstance(s.index, pd.DatetimeIndex) or not _diaria_por_fechas(s.index):
            raise ErrorFicha(f"{F}: rechazo sin datos diarios (serie «{rol}»)")
        if np.any(s.values <= 0):
            raise ErrorFicha(f"{F}: precios no positivos en la serie «{rol}»")
        return np.asarray(s.pct_change().dropna().values, dtype=float), f"serie de rol «{rol}»"
    r = _vector(v, clave, F)
    if v.get("fechas") is not None:
        f = _fechas(v, "fechas", F)
        if f.size != r.size or not _diaria_por_fechas(f):
            raise ErrorFicha(f"{F}: rechazo sin datos diarios (fechas no diarias o no alineadas)")
    elif v.get("frecuencia") != "diaria":
        raise ErrorFicha(f"{F}: rechazo sin datos diarios (declare «fechas» o frecuencia «diaria»)")
    return r, f"valores «{clave}»"


def _rl_formula(L: float, R: float, var_T: float, coste: float) -> float:
    """Paso (i): R_L ≈ (1 + R)^L · exp(−½(L² − L)σ²T) − 1 − costes (var_T = σ²·T)."""
    return float((1 + R) ** L * math.exp(-0.5 * (L * L - L) * var_T) - 1 - coste)


def f_fon_lev(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """FON-LEV-001 · Decaimiento por volatilidad de vehículos apalancados e inversos (MC-09; MC-05 invitado).

    ``valores``: ``L`` (obligatorio), ``horizonte`` (sesiones; también vale en parámetros), ``tipo_financiacion``
    (anual), ``gastos_medios`` (anual de la categoría) y ``rentabilidades_indice`` diarias con ``fechas`` o
    ``frecuencia: "diaria"``; o bien la serie de precios del índice en ``series_rol["indice"]``.
    Opcionales: ``sigma`` (anual, con ``fuente_sigma``; si no, la realizada de la historia), ``rendimiento_indice``
    (R del índice a T, escenario; si no, la realizada en las últimas ``horizonte`` sesiones) y
    ``rejilla_rendimiento`` (lista de R para la rejilla). La simulación SIM-MC-001/VOL-GARCH-001 no se sirve.
    """
    F = "FON-LEV-001"
    p, m, v = _p(F, params), MINIMOS[F], ent.get("valores") or {}
    if v.get("L") is None:
        raise ErrorFicha(f"{F}: rechazo sin L declarado")
    L = _num(v, "L", F)
    _rango(F, "L", L)
    h_src = v.get("horizonte") if v.get("horizonte") is not None else p.get("horizonte")
    if h_src is None:
        raise ErrorFicha(f"{F}: falta el horizonte (sesiones)")
    h_f = _num({"horizonte": h_src}, "horizonte", F, positivo=True)
    h = int(h_f)
    if h != h_f:
        raise ErrorFicha(f"{F}: el horizonte debe ser un número entero de sesiones")
    _rango(F, "horizonte", h)
    rf = _num(v, "tipo_financiacion", F)
    g = _num(v, "gastos_medios", F)
    r, fuente_r = _rend_diarios(ent, F, "indice", "rentabilidades_indice")
    if r.size < m["anios"] * SESIONES_ANIO:
        raise ErrorFicha(f"{F}: se necesitan ≥ {m['anios']} año(s) de rentabilidades diarias del índice")
    if np.any(1 + L * r <= 0):
        lim_extra = ["algún día con L·r ≤ −100 %: el vehículo se habría liquidado"]
    else:
        lim_extra = []
    rejilla_s = [float(x) for x in p["rejilla_sigma"]]
    for s in rejilla_s:
        _rango(F, "rejilla_sigma", s)
    lim: list[str] = [("rebalanceo diario exacto al cierre; saltos y huecos amplifican el arrastre; la fórmula es "
                       "exacta solo bajo movimiento browniano geométrico; describe la estructura de la categoría, "
                       "no vehículos concretos"),
                      ("segunda vía por simulación (SIM-MC-001 en régimen VOL-GARCH-001) no servida: requiere el "
                       "módulo invitado MC-05 y semilla; percentiles simulados no entregados")] + lim_extra
    if v.get("sigma") is not None:
        sigma, fuente_s = _num(v, "sigma", F, positivo=True), str(v.get("fuente_sigma") or "declarada")
    else:
        sigma = float(np.std(r, ddof=1)) * math.sqrt(SESIONES_ANIO)
        fuente_s = f"realizada ({r.size} sesiones, {fuente_r})"
    if v.get("rendimiento_indice") is not None:
        R, fuente_R = _num(v, "rendimiento_indice", F), "declarado (escenario)"
    else:
        R, fuente_R = float(np.prod(1 + r[-h:]) - 1), f"realizado en las últimas {h} sesiones"
        lim.append("R del índice tomado de la historia reciente: escenario descriptivo, no previsión")
    if 1 + R <= 0:
        raise ErrorFicha(f"{F}: rendimiento del índice ≤ −100 %")
    T = h / SESIONES_ANIO
    A = 0.5 * (L * L - L) * T
    coste = ((L - 1) * rf + g) * T
    arrastre = A * sigma * sigma                                  # paso (ii)
    rl = _rl_formula(L, R, sigma * sigma * T, coste)
    # Paso (iii): umbral de σ en el que R_L = L·R (con costes); por encima, el arrastre domina la tendencia.
    umbral, estado = None, "SIN_ARRASTRE"
    if A > 0:
        ratio = (1 + L * R + coste) / (1 + R) ** L
        if ratio <= 0:
            estado = "NO_DEFINIDO"
        else:
            s2 = -math.log(ratio) / A
            if s2 < 0:
                estado = "DOMINA_CON_CUALQUIER_SIGMA"
            else:
                umbral, estado = math.sqrt(s2), "UMBRAL"
    elif A < 0:
        estado = "CONVEXIDAD_FAVORABLE"
    sigmas = sorted(set(rejilla_s + [sigma]))
    rs = [float(x) for x in v["rejilla_rendimiento"]] if v.get("rejilla_rendimiento") is not None else [R]
    if v.get("rejilla_rendimiento") is None:
        lim.append("rejilla con un solo R del índice (no se declaró «rejilla_rendimiento»)")
    rejilla = []
    for s in sigmas:
        for x in rs:
            if 1 + x <= 0:
                raise ErrorFicha(f"{F}: rendimiento de la rejilla ≤ −100 %")
            y = _rl_formula(L, x, s * s * T, coste)
            rejilla.append({"sigma_pct": s * A_PCT, "R_indice_pct": x * A_PCT, "R_L_pct": y * A_PCT,
                            "L_por_R_pct": L * x * A_PCT, "diferencia_pp": (y - L * x) * A_PCT})
    # Paso (iv), segunda vía determinista: reconstrucción exacta con rebalanceo diario en ventanas de h sesiones.
    if r.size < h:
        raise ErrorFicha(f"{F}: historia menor que el horizonte")
    c_dia = ((L - 1) * rf + g) / SESIONES_ANIO
    disc, exactas, formulas = [], [], []
    for i in range(r.size - h + 1):
        w = r[i:i + h]
        ex = float(np.prod(1 + L * w - c_dia) - 1)
        Rw = float(np.prod(1 + w) - 1)
        fo = _rl_formula(L, Rw, float(np.var(w, ddof=1)) * SESIONES_ANIO * T, coste)
        exactas.append(ex)
        formulas.append(fo)
        disc.append(ex - fo)
    da = np.abs(np.asarray(disc))
    res = {
        "L": L, "horizonte_sesiones": h, "T_anios": T,
        "sigma_anual_pct": sigma * A_PCT, "fuente_sigma": fuente_s,
        "rendimiento_indice_T_pct": R * A_PCT, "fuente_rendimiento": fuente_R,
        "arrastre_pct": arrastre * A_PCT,
        "R_L_formula_pct": rl * A_PCT, "L_por_R_indice_pct": L * R * A_PCT,
        "R_L_menos_L_por_R_pp": (rl - L * R) * A_PCT,
        "coste_financiacion_y_gastos_pct": coste * A_PCT,
        "umbral_sigma_pct": umbral * A_PCT if umbral is not None else None, "estado_umbral": estado,
        "rejilla": rejilla,
        "reconstruccion": {"ventanas": len(disc), "R_L_exacta_ultima_pct": exactas[-1] * A_PCT,
                           "R_L_formula_ultima_pct": formulas[-1] * A_PCT,
                           "discrepancia_ultima_pp": disc[-1] * A_PCT,
                           "discrepancia_abs_mediana_pp": float(np.median(da)) * A_PCT,
                           "discrepancia_abs_max_pp": float(np.max(da)) * A_PCT},
        "percentiles_simulados": None,
        "referencia_ingenua_pct": L * R * A_PCT,
        "unidades": {"arrastre": "% a T", "diferencias": "pp", "sigma": "% anual"},
    }
    return res, lim


# =========================================================================================== DER-VRP-001
def _replica_varianza(cesta: dict, F_: str, n_min: int, plazo: float) -> float:
    """Paso (i): σ²_imp = (2/T)·Σ(ΔKᵢ/Kᵢ²)·e^{rT}·Q(Kᵢ) − (1/T)·(F/K₀ − 1)² (réplica libre de modelo)."""
    K = _vector(cesta, "strikes", F_, positivo=True, ctx=" (cesta_opciones)")
    Q = _vector(cesta, "q", F_, ctx=" (cesta_opciones)")
    if K.size < n_min:
        raise ErrorFicha(f"{F_}: réplica con < {n_min} precios de ejercicio")
    if Q.size != K.size or np.any(Q < 0) or np.any(np.diff(K) <= 0):
        raise ErrorFicha(f"{F_}: cesta de opciones no válida (strikes crecientes y Q ≥ 0 alineados)")
    fwd = _num(cesta, "forward", F_, positivo=True, ctx=" (cesta_opciones)")
    r = _num(cesta, "tipo_interes", F_, ctx=" (cesta_opciones)")
    dias = _num(cesta, "dias", F_, positivo=True, ctx=" (cesta_opciones)")
    if dias != plazo:
        raise ErrorFicha(f"{F_}: rechazo con plazos no alineados (cesta a {dias} días, plazo {plazo})")
    T = dias / DIAS_ANIO
    bajo = K[K <= fwd]
    if bajo.size == 0:
        raise ErrorFicha(f"{F_}: ningún precio de ejercicio ≤ forward (K₀ no definido)")
    k0 = float(bajo[-1])
    dK = np.empty_like(K)
    dK[1:-1] = (K[2:] - K[:-2]) / 2
    dK[0], dK[-1] = K[1] - K[0], K[-1] - K[-2]
    var = 2 / T * float(np.sum(dK / K ** 2 * math.exp(r * T) * Q)) - (fwd / k0 - 1) ** 2 / T
    if var <= 0:
        raise ErrorFicha(f"{F_}: réplica con varianza no positiva")
    return var


def f_der_vrp(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """DER-VRP-001 · Prima de varianza implícita-realizada (MC-09; MC-02 invitado).

    ``valores``: ``vol_implicita`` (diaria, anual, tanto por uno, a ``plazo_dias_vol_implicita`` días) y
    ``precios_subyacente`` (diarios, alineados con la volatilidad); o las series ``series_rol["subyacente"]``
    (precios) y ``series_rol["vol_implicita"]`` (se alinean por fecha). Opcional ``cesta_opciones`` =
    {"strikes", "q" (Q(Kᵢ): put fuera de dinero si K < K₀, call si K > K₀, media en K₀), "forward",
    "tipo_interes", "dias"} para la réplica libre de modelo de hoy (segunda vía frente al índice publicado).
    Realizada: Σr²·252/n con rendimientos simples; la posterior a h = plazo·252/365 sesiones (21 a 30 días) solo
    entra en la historia, nunca en la señal actual.
    """
    F = "DER-VRP-001"
    p, m, v = _p(F, params), MINIMOS[F], ent.get("valores") or {}
    plazo = float(p["plazo"])
    _rango(F, "plazo", plazo)
    sr = ent.get("series_rol") or {}
    if sr.get("subyacente") is not None and sr.get("vol_implicita") is not None:
        al = pd.concat([sr["subyacente"], sr["vol_implicita"]], axis=1, join="inner").dropna().astype(float)
        precios, iv = al.iloc[:, 0].to_numpy(), al.iloc[:, 1].to_numpy()
    else:
        precios = _vector(v, "precios_subyacente", F, positivo=True)
        iv = _vector(v, "vol_implicita", F, positivo=True)
        if precios.size != iv.size:
            raise ErrorFicha(f"{F}: rechazo con plazos no alineados (precios y volatilidad de distinta longitud)")
    if np.any(precios <= 0) or np.any(iv <= 0):
        raise ErrorFicha(f"{F}: precios y volatilidades deben ser positivos")
    if _num(v, "plazo_dias_vol_implicita", F, positivo=True) != plazo:
        raise ErrorFicha(f"{F}: rechazo con plazos no alineados (implícita a {v['plazo_dias_vol_implicita']} días, "
                         f"plazo {plazo:g})")
    r = precios[1:] / precios[:-1] - 1
    iv = iv[1:]
    n = r.size
    if n < m["anios_rechazo"] * SESIONES_ANIO:
        raise ErrorFicha(f"{F}: rechazo con < {m['anios_rechazo']} años de historia")
    if n < m["anios"] * SESIONES_ANIO:
        raise ErrorFicha(f"{F}: entradas mínimas: ≥ {m['anios']} años de volatilidad implícita diaria")
    h = round(plazo * SESIONES_ANIO / DIAS_ANIO)
    lim: list[str] = [("VRP positiva en promedio con pérdidas extremas en crisis (asimetría negativa); la realizada "
                       "posterior usa datos futuros y nunca entra en la señal actual; los índices publicados tienen "
                       "metodología propia"),
                      "ES de la venta de varianza sobre ventanas solapadas (observaciones dependientes)"]
    rv_d = r * r * SESIONES_ANIO
    cs = np.concatenate([[0.0], np.cumsum(rv_d)])
    t_hist = np.arange(0, n - h)                         # t con realizada posterior conocida en la fecha de corte
    rv_post = (cs[t_hist + 1 + h] - cs[t_hist + 1]) / h
    var_imp = iv * iv
    vrp_post = var_imp[t_hist] - rv_post
    metodo = p["prevision_rv"]
    if metodo == "HAR":
        lw, lm = 5, 22   # HAR-RV de Corsi (2009): componentes diaria, semanal (5) y mensual (22)
        filas = np.arange(lm - 1, n)

        def _x(t: np.ndarray) -> np.ndarray:
            return np.column_stack([np.ones(t.size), rv_d[t], (cs[t + 1] - cs[t + 1 - lw]) / lw,
                                    (cs[t + 1] - cs[t + 1 - lm]) / lm])
        entreno = filas[filas < n - h]
        coef, *_ = np.linalg.lstsq(_x(entreno), rv_post[entreno], rcond=None)
        e_rv = float((_x(np.array([n - 1])) @ coef)[0])
        if e_rv <= 0:
            raise ErrorFicha(f"{F}: previsión HAR de la varianza realizada no positiva; use otra prevision_rv")
    elif metodo == "GARCH":
        try:
            g = op.garch11(pd.Series(precios), horizonte=h)
        except NotImplementedError as e:
            raise ErrorFicha(f"{F}: prevision_rv GARCH requiere el paquete opcional «arch»") from e
        e_rv = float(np.mean(np.square(g["vol_prevista_anual"])))
    elif metodo == "realizada_pasada":
        e_rv = float(np.mean(rv_d[-h:]))
    else:
        raise ErrorFicha(f"{F}: prevision_rv «{metodo}» no admitida (HAR | GARCH | realizada_pasada)")
    vrp_var = float(var_imp[-1]) - e_rv
    vrp_vol = float(iv[-1]) - math.sqrt(e_rv)
    nw = int(float(p["ventana_percentil"]) * SESIONES_ANIO)
    if n < m["anios_recomendados"] * SESIONES_ANIO:
        lim.append(f"historia inferior a los {m['anios_recomendados']} años recomendados: percentiles orientativos")
    hist_vrp, hist_iv = vrp_post[-nw:], iv[-nw:]
    tol = FICHAS[F]["tol"]
    pos_vrp, pos_iv = _posicion(vrp_var, hist_vrp, tol), _posicion(float(iv[-1]), hist_iv, tol)
    rel = vrp_post[-nw:] / var_imp[t_hist][-nw:]          # rentabilidad de vender varianza por unidad de σ²_imp
    nivel = float(p["nivel_es"])
    q = _cuantil(rel, 1 - nivel)
    es = -float(np.mean(rel[rel <= q])) * A_PCT
    replica = None
    if v.get("cesta_opciones") is not None:
        var_rep = _replica_varianza(v["cesta_opciones"], F, m["strikes"], plazo)
        replica = {"sigma_imp_replica_pct": math.sqrt(var_rep) * A_PCT,
                   "diferencia_replica_menos_publicado_puntos": (math.sqrt(var_rep) - float(iv[-1])) * A_PCT}
    else:
        lim.append("sin cesta de opciones: no hay segunda vía (réplica frente a índice publicado)")
    res = {
        "plazo_dias": plazo, "sesiones_plazo": h, "prevision_rv": metodo,
        "sigma_imp_pct": float(iv[-1]) * A_PCT, "varianza_imp_puntos": float(var_imp[-1]) * A_PB,
        "sigma_real_esperada_pct": math.sqrt(e_rv) * A_PCT,
        "sigma_real_posterior_ultima_pct": math.sqrt(float(rv_post[-1])) * A_PCT,
        "vrp_ex_ante": {"varianza_puntos": vrp_var * A_PB, "volatilidad_puntos": vrp_vol * A_PCT},
        "vrp_ex_post_ultima": {"varianza_puntos": float(vrp_post[-1]) * A_PB,
                               "volatilidad_puntos": (float(iv[t_hist[-1]]) - math.sqrt(float(rv_post[-1]))) * A_PCT},
        "percentiles": {"vrp_ex_ante_en_historia_ex_post": pos_vrp["percentil"], "z_vrp": pos_vrp["z"],
                        "sigma_imp": pos_iv["percentil"], "z_sigma_imp": pos_iv["z"], "n_historia": pos_vrp["n"]},
        "frecuencia_vrp_positiva_pct": float(np.mean(hist_vrp > 0)) * A_PCT,
        "es_venta_varianza_pct": es, "nivel_es": nivel,
        "replica": replica,
        "referencias_ingenuas": {"RI_MH_vrp_varianza_puntos": float(np.mean(hist_vrp)) * A_PB,
                                 "RI_EWMA_sigma_real_pct": op.ewma_vol(r, LAMBDA_EWMA, SESIONES_ANIO) * A_PCT},
        "verificacion": {"signo_coherente_varianza_volatilidad": bool(np.sign(vrp_var) == np.sign(vrp_vol))},
        "unidades": {"sigma": "% anual", "varianza": "puntos (σ·100)²", "vrp_volatilidad": "puntos",
                     "es": "% de σ²_imp (pérdida positiva)"},
    }
    return res, lim


# =========================================================================================== DER-SKEW-001
def _svi(x: np.ndarray, k: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    a, b, rho, mm, s = x
    raiz = np.sqrt((k - mm) ** 2 + s * s)
    w = a + b * (rho * (k - mm) + raiz)
    w1 = b * (rho + (k - mm) / raiz)
    w2 = b * s * s / raiz ** 3
    return w, w1, w2


def _svi_g(x: np.ndarray, k: np.ndarray) -> np.ndarray:
    """Condición de no arbitraje de mariposa de Gatheral: g(k) ≥ 0 y w(k) > 0."""
    w, w1, w2 = _svi(x, k)
    return (1 - k * w1 / (2 * w)) ** 2 - w1 * w1 / 4 * (1 / w + 1 / 4) + w2 / 2


def _vols_25d(k: np.ndarray, vol: np.ndarray, T: float, delta: float, F_: str) -> tuple[float, float, float]:
    """σ de la put y la call a la delta dada y σ ATM (k = 0) por interpolación lineal; sin extrapolar."""
    dc = np.array([_delta_call_forward(float(a), float(b), T) for a, b in zip(k, vol)])
    if np.any(np.diff(dc) >= 0):
        raise ErrorFicha(f"{F_}: deltas no monótonas en el precio de ejercicio: no se puede interpolar en delta")
    xs, ys = dc[::-1], vol[::-1]
    for objetivo in (delta, 1 - delta):
        if not xs[0] <= objetivo <= xs[-1]:
            raise ErrorFicha(f"{F_}: la delta {objetivo:g} cae fuera de la superficie cotizada (no se extrapola)")
    if not k[0] <= 0 <= k[-1]:
        raise ErrorFicha(f"{F_}: la superficie no cubre el ATM (k = 0); no se extrapola")
    return (float(np.interp(1 - delta, xs, ys)), float(np.interp(delta, xs, ys)), float(np.interp(0.0, k, vol)))


def f_der_skew(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """DER-SKEW-001 · Sesgo de la volatilidad implícita (MC-09).

    ``valores``: ``vencimiento_meses`` (debe coincidir con el parámetro); una de dos entradas:
    ``superficie`` = {"strikes", "vols" (anuales, tanto por uno), "forward", "spot" y "tipo_interes" (opcionales,
    para el coste de protección)} con ≥ 5 precios de ejercicio, o cotizaciones a la delta del parámetro
    (``delta`` declarada y ``vol_put``/``vol_call``/``vol_atm``, o ``rr``/``bf``/``vol_atm``). Historia diaria
    obligatoria ``historia_rr`` (≥ 2 años) y opcionales ``historia_bf``, ``historia_pendiente``,
    ``historia_coste_proteccion`` (mismas unidades: tanto por uno). Opcional ``asimetria_publicada`` (índice de
    sesgo publicado). Convenciones: delta forward sin prima; RR = σ_put − σ_call; ATM = forward (k = 0).
    """
    F = "DER-SKEW-001"
    p, m, v = _p(F, params), MINIMOS[F], ent.get("valores") or {}
    _rango(F, "delta", float(p["delta"]))
    _rango(F, "vencimiento", float(p["vencimiento"]))
    if p["metodo"] not in ("deltas", "SVI"):
        raise ErrorFicha(f"{F}: metodo «{p['metodo']}» no admitido (deltas | SVI)")
    if _num(v, "vencimiento_meses", F, positivo=True) != float(p["vencimiento"]):
        raise ErrorFicha(f"{F}: vencimiento de los datos no declarado o distinto del parámetro ({p['vencimiento']} meses)")
    delta = float(p["delta"]) / A_PCT
    T = float(p["vencimiento"]) / MESES_ANIO
    tol = FICHAS[F]["tol"]
    hist_rr = _vector(v, "historia_rr", F)
    if hist_rr.size < m["anios"] * SESIONES_ANIO:
        raise ErrorFicha(f"{F}: se necesita historia diaria ≥ {m['anios']} años")
    lim: list[str] = [("el sesgo depende de la convención de delta (aquí forward sin prima); las probabilidades "
                      "neutrales al riesgo no son reales; los cambios de nivel alteran el sesgo (use la normalizada)")]
    if hist_rr.size < m["anios_percentil"] * SESIONES_ANIO:
        lim.append(f"historia < {m['anios_percentil']} años: percentiles orientativos")
    sup = v.get("superficie")
    svi: dict[str, Any] | None = None
    bkm: float | None = None
    coste: float | None = None
    if sup is not None:
        K = _vector(sup, "strikes", F, positivo=True, ctx=" (superficie)")
        if K.size < m["strikes"]:
            raise ErrorFicha(f"{F}: rechazo con < {m['strikes']} precios de ejercicio")
        vol = _vector(sup, "vols", F, positivo=True, ctx=" (superficie)")
        fwd = _num(sup, "forward", F, positivo=True, ctx=" (superficie)")
        if vol.size != K.size or np.any(np.diff(K) <= 0):
            raise ErrorFicha(f"{F}: superficie no válida (strikes crecientes y vols alineadas)")
        C = np.array([_black(fwd, float(a), float(b), T, True) for a, b in zip(K, vol)])
        pend_c = np.diff(C) / np.diff(K)
        if np.any(pend_c > tol) or np.any(np.diff(pend_c) < -tol):
            raise ErrorFicha(f"{F}: rechazo: superficie con arbitraje (precios de call no decrecientes o no convexos); "
                             "no se corrige")
        k = np.log(K / fwd)
        s_put, s_call, s_atm = _vols_25d(k, vol, T, delta, F)
        rr_deltas = s_put - s_call
        if any(v.get(x) is not None for x in ("vol_put", "vol_call", "rr", "bf")):
            lim.append("cotizaciones RR/BF ignoradas: se usa la superficie")
        # (ii) SVI por mínimos cuadrados sobre la varianza total, con arranque derivado de los datos.
        w_obs = vol * vol * T
        x0 = np.array([float(np.min(w_obs)), float(np.ptp(w_obs) / np.ptp(k)), 0.0,
                       float(k[int(np.argmin(w_obs))]), float(np.std(k))])
        ajuste = optimize.least_squares(lambda x: _svi(x, k)[0] - w_obs, x0,
                                        bounds=([-np.inf, 0, -1, -np.inf, 0], [np.inf, np.inf, 1, np.inf, np.inf]))
        xs = ajuste.x
        nodos = np.sort(np.concatenate([k, (k[1:] + k[:-1]) / 2]))
        w_n = _svi(xs, nodos)[0]
        sin_arb = bool(np.all(w_n > 0) and np.all(_svi_g(xs, nodos) >= -tol))
        w0, w10, _ = _svi(xs, np.array([0.0]))
        svi = {"a": float(xs[0]), "b": float(xs[1]), "rho": float(xs[2]), "m": float(xs[3]), "sigma": float(xs[4]),
               "rmse_varianza_total": float(np.sqrt(np.mean(ajuste.fun ** 2))),
               "sin_arbitraje_mariposa": sin_arb,
               "pendiente_vol_k0": float(w10[0] / (2 * math.sqrt(float(w0[0]) * T))) if w0[0] > 0 else None}
        if sin_arb:
            def _vol_svi(kk: float) -> float:
                return math.sqrt(float(_svi(xs, np.array([kk]))[0][0]) / T)

            def _raiz(objetivo: float) -> float:
                fun = lambda kk: _delta_call_forward(kk, _vol_svi(kk), T) - objetivo
                if fun(float(k[0])) * fun(float(k[-1])) > 0:
                    raise ErrorFicha(f"{F}: SVI: delta {objetivo:g} fuera del rango cotizado (no se extrapola)")
                return float(optimize.brentq(fun, float(k[0]), float(k[-1])))
            sp, sc, sa = _vol_svi(_raiz(1 - delta)), _vol_svi(_raiz(delta)), _vol_svi(0.0)
            svi.update({"sigma_put_pct": sp * A_PCT, "sigma_call_pct": sc * A_PCT, "sigma_atm_pct": sa * A_PCT,
                        "rr_puntos": (sp - sc) * A_PCT, "bf_puntos": ((sp + sc) / 2 - sa) * A_PCT})
        elif p["metodo"] == "SVI":
            raise ErrorFicha(f"{F}: rechazo: el ajuste SVI presenta arbitraje de mariposa no corregible")
        else:
            lim.append("ajuste SVI con arbitraje de mariposa: segunda vía no disponible")
        if p["metodo"] == "SVI":
            s_put, s_call, s_atm = (svi["sigma_put_pct"] / A_PCT, svi["sigma_call_pct"] / A_PCT,
                                    svi["sigma_atm_pct"] / A_PCT)
        # (iii) Asimetría neutral al riesgo (Bakshi-Kapadia-Madan) en medida forward, sobre los strikes cotizados.
        Q = np.array([_black(fwd, float(a), float(b), T, bool(a >= fwd)) for a, b in zip(K, vol)])
        lk = k

        def _int(f2: np.ndarray) -> float:
            y = f2 * Q
            return float(np.sum((y[1:] + y[:-1]) / 2 * np.diff(K)))
        mu = -_int(1 / K ** 2)
        V = _int((2 - 2 * lk) / K ** 2)
        W = _int((6 * lk - 3 * lk ** 2) / K ** 2)
        den = V - mu * mu
        bkm = float((W - 3 * mu * V + 2 * mu ** 3) / den ** 1.5) if den > 0 else None
        lim.append("asimetría BKM integrada solo sobre los strikes cotizados (truncamiento y discretización)")
        # (iv) Coste de la protección estándar (put al 90 % a 3 meses), en % del nocional.
        if float(p["vencimiento"]) != float(p["proteccion_meses"]):
            lim.append("vencimiento distinto del de la protección estándar: coste de protección no calculado")
        elif sup.get("spot") is None or sup.get("tipo_interes") is None:
            lim.append("sin spot o tipo de interés en la superficie: coste de protección no calculado")
        else:
            S = _num(sup, "spot", F, positivo=True, ctx=" (superficie)")
            rr_ = _num(sup, "tipo_interes", F, ctx=" (superficie)")
            Kp = float(p["proteccion_moneyness"]) * S
            kp = math.log(Kp / fwd)
            if k[0] <= kp <= k[-1]:
                sp_ = float(np.interp(kp, k, vol))
                coste = math.exp(-rr_ * T) * _black(fwd, Kp, sp_, T, False) / S
            else:
                lim.append("el strike de la protección cae fuera de la superficie: no se extrapola")
    else:
        if _num(v, "delta", F, positivo=True) != float(p["delta"]):
            raise ErrorFicha(f"{F}: cotizaciones sin delta declarada o distinta del parámetro ({p['delta']})")
        if p["metodo"] == "SVI":
            raise ErrorFicha(f"{F}: metodo SVI exige superficie con ≥ {m['strikes']} precios de ejercicio")
        s_atm = _num(v, "vol_atm", F, positivo=True)
        if v.get("vol_put") is not None and v.get("vol_call") is not None:
            s_put, s_call = _num(v, "vol_put", F, positivo=True), _num(v, "vol_call", F, positivo=True)
        elif v.get("rr") is not None and v.get("bf") is not None:
            rr_q, bf_q = _num(v, "rr", F), _num(v, "bf", F)
            s_put, s_call = s_atm + bf_q + rr_q / 2, s_atm + bf_q - rr_q / 2
        else:
            raise ErrorFicha(f"{F}: rechazo: ni superficie con ≥ {m['strikes']} precios de ejercicio ni cotizaciones RR/BF")
        lim.append("sin superficie: sin SVI, asimetría neutral al riesgo ni coste de protección calculados")
    rr = s_put - s_call
    bf = (s_put + s_call) / 2 - s_atm
    pend = rr / s_atm
    percent: dict[str, Any] = {"rr": _posicion(rr, hist_rr, tol)}
    for clave, valor in (("bf", bf), ("pendiente_normalizada", pend), ("coste_proteccion", coste)):
        hk = f"historia_{clave}"
        if v.get(hk) is not None and valor is not None:
            percent[clave] = _posicion(valor, _vector(v, hk, F), tol)
    segunda = None
    if svi is not None and "rr_puntos" in svi:
        segunda = {"rr_deltas_puntos": rr_deltas * A_PCT, "rr_svi_puntos": svi["rr_puntos"],
                   "rr_deltas_menos_svi_puntos": rr_deltas * A_PCT - svi["rr_puntos"]}
    res = {
        "vencimiento_meses": float(p["vencimiento"]), "delta": float(p["delta"]), "metodo": p["metodo"],
        "convencion_delta": "forward sin prima", "convencion_rr": "σ_put − σ_call",
        "sigma_put_pct": s_put * A_PCT, "sigma_call_pct": s_call * A_PCT, "sigma_atm_pct": s_atm * A_PCT,
        "rr_puntos": rr * A_PCT, "bf_puntos": bf * A_PCT, "pendiente_normalizada": pend,
        "svi": svi, "segunda_via": segunda,
        "asimetria_neutral_riesgo": bkm, "asimetria_publicada": v.get("asimetria_publicada"),
        "coste_proteccion_pct": coste * A_PCT if coste is not None else None,
        "percentiles": {c: {"percentil": x["percentil"], "z": x["z"], "n": x["n"]} for c, x in percent.items()},
        "referencias_ingenuas": {"RI_MH_rr_puntos": float(np.mean(hist_rr)) * A_PCT,
                                 "RI_PA_rr_puntos": float(hist_rr[-1]) * A_PCT},
        "unidades": {"sigma": "% anual", "rr_bf": "puntos de volatilidad", "pendiente_normalizada": "adimensional",
                     "coste_proteccion": "% del nocional"},
    }
    return res, lim


# =========================================================================================== DER-TERM-001
def f_der_term(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """DER-TERM-001 · Estructura de plazos de la volatilidad implícita (MC-09).

    ``valores``: ``vencimientos_meses`` (≥ 3, crecientes) y ``vol_atm`` (anuales, tanto por uno, alineadas);
    ``calendario_eventos`` (lista obligatoria, puede ir vacía si se declara que no hay eventos) con
    {"nombre", "vencimiento_meses" (uno de los cotizados, que contiene el evento), "sigma_base" (de vencimientos
    que lo excluyen, supuesto declarado), "fuente_sigma_base"}; ``historia_vol_1m`` e ``historia_vol_3m``
    (diarias, alineadas, ≥ 2 años). Interpolación lineal en T de la varianza total w = σ²·T; no se extrapola.
    """
    F = "DER-TERM-001"
    p, m, v = _p(F, params), MINIMOS[F], ent.get("valores") or {}
    if p["interpolacion"] != "varianza_total":
        raise ErrorFicha(f"{F}: interpolacion «{p['interpolacion']}» no admitida (varianza_total)")
    meses = _vector(v, "vencimientos_meses", F, positivo=True)
    vol = _vector(v, "vol_atm", F, positivo=True)
    if meses.size < m["vencimientos"]:
        raise ErrorFicha(f"{F}: rechazo con < {m['vencimientos']} vencimientos")
    if vol.size != meses.size or np.any(np.diff(meses) <= 0):
        raise ErrorFicha(f"{F}: vencimientos crecientes y volatilidades alineadas")
    if v.get("calendario_eventos") is None:
        raise ErrorFicha(f"{F}: falta el calendario de eventos (lista vacía si no hay)")
    h1, h3 = _vector(v, "historia_vol_1m", F, positivo=True), _vector(v, "historia_vol_3m", F, positivo=True)
    if h1.size != h3.size:
        raise ErrorFicha(f"{F}: historias de 1 y 3 meses no alineadas")
    if h1.size < m["anios"] * SESIONES_ANIO:
        raise ErrorFicha(f"{F}: se necesita historia diaria ≥ {m['anios']} años")
    tol = FICHAS[F]["tol"]
    T = meses / MESES_ANIO
    w = vol * vol * T
    if np.any(np.diff(w) < -tol * w[:-1]):
        raise ErrorFicha(f"{F}: rechazo: varianza total decreciente (arbitraje de calendario); no hay corrección declarada")
    lim: list[str] = ["el movimiento del evento depende de la varianza base supuesta"]
    if h1.size < m["anios_percentil"] * SESIONES_ANIO:
        lim.append(f"historia < {m['anios_percentil']} años: percentiles orientativos")

    def sigma_en(mes: float) -> float | None:
        t = mes / MESES_ANIO
        if not T[0] <= t <= T[-1]:
            return None
        return math.sqrt(float(np.interp(t, T, w)) / t)
    curva = {}
    for mes in p["vencimientos"]:
        s = sigma_en(float(mes))
        curva[_clave_mes(mes)] = s * A_PCT if s is not None else None
        if s is None:
            lim.append(f"vencimiento de {mes} meses fuera del rango cotizado: no se extrapola")
    m1, m3 = (float(x) for x in p["pendiente_meses"])
    s1, s3 = sigma_en(m1), sigma_en(m3)
    if s1 is None or s3 is None:
        raise ErrorFicha(f"{F}: la pendiente exige cotizaciones que cubran {m1:g} y {m3:g} meses (no se extrapola)")
    pend = s3 - s1
    ratio = s1 / s3
    estado = "INVERTIDA" if ratio > 1 else "PLANA" if ratio == 1 else "NORMAL"
    fwd = []
    grid = [float(x) for x in p["vencimientos"] if curva[_clave_mes(x)] is not None]
    for a, b in itertools.pairwise(grid):
        ta, tb = a / MESES_ANIO, b / MESES_ANIO
        sa, sb = sigma_en(a), sigma_en(b)
        if sa is None or sb is None:
            raise ErrorFicha(f"{F}: vencimiento fuera del rango cotizado")
        fwd.append({"desde_meses": a, "hasta_meses": b,
                    "sigma_fwd_pct": math.sqrt((sb * sb * tb - sa * sa * ta) / (tb - ta)) * A_PCT})
    eventos = []
    for e in v["calendario_eventos"]:
        if not isinstance(e, dict):
            raise ErrorFicha(f"{F}: evento mal formado")
        mc = _num(e, "vencimiento_meses", F, positivo=True, ctx=" (evento)")
        if mc not in {float(x) for x in meses}:
            raise ErrorFicha(f"{F}: el vencimiento del evento debe ser uno de los cotizados")
        sb_ = _num(e, "sigma_base", F, positivo=True, ctx=" (evento: supuesto declarado)")
        s_con = float(vol[int(np.where(meses == mc)[0][0])])
        tc = mc / MESES_ANIO
        var_e = s_con * s_con * tc - sb_ * sb_ * tc
        if var_e < 0:
            lim.append(f"evento {e.get('nombre')}: varianza del evento negativa con la σ_base declarada")
        eventos.append({"nombre": e.get("nombre"), "fecha": e.get("fecha"), "vencimiento_meses": mc,
                        "sigma_base_pct": sb_ * A_PCT, "fuente_sigma_base": e.get("fuente_sigma_base"),
                        "varianza_evento": var_e,
                        "movimiento_descontado_pct": math.sqrt(var_e) * A_PCT if var_e >= 0 else None})
    hist_p = h3 - h1
    pos = _posicion(pend, hist_p, tol)
    inv = (h1 / h3) > 1
    rachas, cur = [], 0
    for x in inv:
        if x:
            cur += 1
        elif cur:
            rachas.append(cur)
            cur = 0
    if cur:
        rachas.append(cur)
    res = {
        "sigma_por_vencimiento_pct": curva,
        "pendiente_puntos": pend * A_PCT, "ratio_1m_3m": ratio, "estado": estado,
        "sigma_fwd": fwd, "eventos": eventos,
        "percentiles": {"pendiente": pos["percentil"], "z_pendiente": pos["z"], "n": pos["n"]},
        "inversiones_historicas": {"frecuencia_pct": float(np.mean(inv)) * A_PCT, "episodios": len(rachas),
                                   "duracion_media_sesiones": float(np.mean(rachas)) if rachas else None,
                                   "duracion_max_sesiones": max(rachas) if rachas else None,
                                   "racha_actual_sesiones": int(cur)},
        "verificacion": {"varianza_total_monotona": bool(np.all(np.diff(w) >= -tol * w[:-1])),
                         "varianza_total": [float(x) for x in w]},
        "referencias_ingenuas": {"RI_MH_pendiente_puntos": float(np.mean(hist_p)) * A_PCT,
                                 "RI_PA_pendiente_puntos": pend * A_PCT},
        "unidades": {"sigma": "% anual", "pendiente": "puntos de volatilidad", "movimiento": "%"},
    }
    return res, lim


# =========================================================================================== DER-ROLL-001
def f_der_roll(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """DER-ROLL-001 · Carry y roll de futuros financieros (MC-09).

    ``valores``: ``tipo_activo`` ("indice" | "divisa" | "bono"), ``tipo_financiacion`` (anual, continuo;
    en divisas, el tipo de la moneda cotizada; en bonos, el repo), ``futuros`` = [{"precio", "dias"} …] (≥ 2,
    días hasta el vencimiento) y ``spot`` (o la serie ``series_rol["spot"]``, de la que se toma el último cierre).
    Índices: ``rendimiento_dividendo`` (q). Divisas: ``tipo_base``. Bonos: ``precio_entregable``,
    ``factor_conversion`` y ``rendimiento_entregable`` (spot efectivo = precio/factor). Opcionales:
    ``historia_carry`` e ``historia_roll`` (diarias, tanto por uno anual) y ``periodo`` = {"spot_ini", "spot_fin",
    "futuro_ini", "futuro_fin", "tipo_colateral", "dias"} para la descomposición.
    """
    F = "DER-ROLL-001"
    p, m, v = _p(F, params), MINIMOS[F], ent.get("valores") or {}
    anual = float(p["anualizacion"])
    if anual not in (float(DIAS_ANIO), 360.0):
        raise ErrorFicha(f"{F}: anualizacion {anual:g} no admitida (365 | 360)")
    if v.get("tipo_financiacion") is None:
        raise ErrorFicha(f"{F}: rechazo sin tipo de financiación")
    r = _num(v, "tipo_financiacion", F)
    fut = v.get("futuros")
    if not isinstance(fut, list) or len(fut) < m["vencimientos"]:
        raise ErrorFicha(f"{F}: rechazo con < {m['vencimientos']} vencimientos")
    pares_fd = sorted((_num(x, "dias", F, positivo=True, ctx=" (futuro)"), _num(x, "precio", F, positivo=True, ctx=" (futuro)"))
                      for x in fut)
    dias = np.array([x[0] for x in pares_fd])
    Fp = np.array([x[1] for x in pares_fd])
    if np.any(np.diff(dias) <= 0):
        raise ErrorFicha(f"{F}: vencimientos repetidos")
    tipo = v.get("tipo_activo")
    lim: list[str] = ["márgenes y liquidación diaria; el carry no es previsión"]
    if tipo == "bono":
        S = (_num(v, "precio_entregable", F, positivo=True) / _num(v, "factor_conversion", F, positivo=True))
        teorico = _num(v, "rendimiento_entregable", F) - r
        lim.append("bonos: cupón corrido y opción de entrega no modelados (spot efectivo = precio del entregable / factor)")
    else:
        sr = (ent.get("series_rol") or {}).get("spot")
        S = float(sr.dropna().iloc[-1]) if sr is not None and v.get("spot") is None else _num(v, "spot", F, positivo=True)
        if tipo == "indice":
            teorico = r - _num(v, "rendimiento_dividendo", F)
            lim.append("dividendos esperados inciertos")
        elif tipo == "divisa":
            teorico = r - _num(v, "tipo_base", F)
        else:
            raise ErrorFicha(f"{F}: tipo_activo «{tipo}» no admitido (indice | divisa | bono)")
    T = dias / anual
    carry = np.log(Fp / S) / T
    tabla = []
    for i in range(Fp.size):
        fila = {"dias": float(dias[i]), "precio": float(Fp[i]), "base_puntos": float(Fp[i] - S),
                "base_pct": float(Fp[i] / S - 1) * A_PCT, "carry_implicito_pct": float(carry[i]) * A_PCT,
                "desviacion_vs_teorico_pb": float(carry[i] - teorico) * A_PB}
        if tipo == "indice":
            fila["dividendo_implicito_pct"] = float(r - carry[i]) * A_PCT
        elif tipo == "bono":
            fila["repo_implicito_pct"] = float(teorico + r - carry[i]) * A_PCT   # rendimiento del entregable − carry
        tabla.append(fila)
    pares = [int(x) for x in p["pares"]]
    if len(pares) != 2 or not (1 <= pares[0] < pares[1] <= Fp.size):
        raise ErrorFicha(f"{F}: pares {pares} no válidos para {Fp.size} vencimientos")
    i, j = pares[0] - 1, pares[1] - 1
    roll = float((Fp[i] / Fp[j] - 1) * anual / (dias[j] - dias[i]))
    percent: dict[str, Any] = {}
    for clave, valor in (("carry", float(carry[0])), ("roll", roll)):
        if v.get(f"historia_{clave}") is not None:
            hst = _vector(v, f"historia_{clave}", F)
            percent[clave] = _posicion(valor, hst, FICHAS[F]["tol"])
            if hst.size < m["anios_percentil"] * SESIONES_ANIO:
                lim.append(f"historia de {clave} < {m['anios_percentil']} años: percentil orientativo")
        else:
            percent[clave] = None
            lim.append(f"sin historia de {clave}: percentil no calculado")
    descomp = None
    if v.get("periodo") is not None:
        pr = v["periodo"]
        s0, s1 = _num(pr, "spot_ini", F, positivo=True), _num(pr, "spot_fin", F, positivo=True)
        f0, f1 = _num(pr, "futuro_ini", F, positivo=True), _num(pr, "futuro_fin", F, positivo=True)
        col = _num(pr, "tipo_colateral", F) * _num(pr, "dias", F, positivo=True) / anual
        spot_r, fut_r = s1 / s0 - 1, f1 / f0 - 1
        descomp = {"spot_pct": spot_r * A_PCT, "roll_pct": (fut_r - spot_r) * A_PCT, "colateral_pct": col * A_PCT,
                   "total_pct": (fut_r + col) * A_PCT,
                   "suma_componentes_menos_total_pp": ((spot_r + (fut_r - spot_r) + col) - (fut_r + col)) * A_PCT}
    else:
        lim.append("sin «periodo»: descomposición spot + roll + colateral no calculada")
    res = {
        "tipo_activo": tipo, "spot": S, "anualizacion": anual, "vencimientos": tabla,
        "carry_implicito_pct": float(carry[0]) * A_PCT, "carry_teorico_pct": teorico * A_PCT,
        "desviacion_vs_teorico_pb": float(carry[0] - teorico) * A_PB,
        "roll_yield_pct": roll * A_PCT, "par_roll": pares,
        "percentiles": {c: ({"percentil": x["percentil"], "z": x["z"], "n": x["n"]} if x else None)
                        for c, x in percent.items()},
        "descomposicion": descomp,
        "referencias_ingenuas": {"RI_MH_carry_pct": percent["carry"]["media"] * A_PCT if percent["carry"] else None,
                                 "carry_teorico_pct": teorico * A_PCT},
        "unidades": {"base": "puntos y %", "carry": "% anual", "roll": "% anual", "desviacion": "pb",
                     "descomposicion": "% del periodo"},
    }
    return res, lim


# =========================================================================================== registro
FICHAS: dict[str, dict[str, Any]] = {
    "FON-DISC-001": {"fn": f_fon_disc, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA",
                     "ri": "RI-MH (media del descuento) y RI-PA (descuento sin cambio)", "tol": 1e-10},
    "FON-FLOW-001": {"fn": f_fon_flow, "modulo": "MC-02", "version": "1.0", "cifra": "ESTADISTICA",
                     "ri": "Flujo nulo y RI-PA del flujo relativo", "tol": 1e-10},
    "FON-TD-001": {"fn": f_fon_td, "modulo": "MC-01", "version": "1.0", "cifra": "ESTADISTICA",
                   "ri": "TD = −gastos corrientes medios de la categoría", "tol": 1e-10},
    "FON-LEV-001": {"fn": f_fon_lev, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA",
                    "ri": "L × rentabilidad del índice", "tol": 1e-10},
    "DER-VRP-001": {"fn": f_der_vrp, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA",
                    "ri": "RI-MH de la VRP; RI-EWMA para la realizada esperada", "tol": 1e-8},
    "DER-SKEW-001": {"fn": f_der_skew, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA",
                     "ri": "RI-MH y RI-PA del sesgo", "tol": 1e-8},
    "DER-TERM-001": {"fn": f_der_term, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA",
                     "ri": "RI-MH y RI-PA de la pendiente", "tol": 1e-10},
    "DER-ROLL-001": {"fn": f_der_roll, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA",
                     "ri": "RI-MH del carry y carry teórico", "tol": 1e-10},
}


# =========================================================================================== casos de control
# Datos sintéticos deterministas (sin aleatoriedad): las cifras de estos generadores son DATOS de control, no
# parámetros del método.
def _fechas_semanales(n: int) -> list[str]:
    return [str(x.date()) for x in pd.date_range("2020-01-03", periods=n, freq="W-FRI")]


def _ctl_disc(iguales: bool, constante: bool = False) -> dict:
    fechas = _fechas_semanales(3 * 52 + 2)
    t = np.arange(len(fechas))
    miembros = {}
    for i in range(5):
        nav = 100 + t * 0.1
        d = -0.10 + 0.02 * i if constante else -0.08 + 0.01 * i + 0.03 * np.sin(t / 9 + i)
        precio = nav if iguales else nav * (1 + d)
        miembros[f"M{i + 1}"] = {"precio": [float(x) for x in np.broadcast_to(precio, t.shape)],
                                 "nav": [float(x) for x in nav], "fecha_nav": fechas[-1], "capitalizacion": 1000.0}
    return {"fechas": fechas, "miembros": miembros}


def _ctl_flow(publicados: bool) -> dict:
    fechas = [str(x.date()) for x in pd.date_range("2021-01-31", periods=37, freq="ME")]
    t = np.arange(36)
    cats: dict[str, Any] = {}
    for i, nombre in enumerate(("RV_indexada", "RF_activa", "MP_indexada")):
        r = 0.005 + 0.02 * np.sin(t / 4 + i)
        fl = 10 * np.cos(t / 5 + i)
        aum = [1000.0 + 100 * i]
        for k in range(36):
            aum.append(aum[-1] * (1 + r[k]) + fl[k])
        cd: dict[str, Any] = {"aum": aum, "rentabilidad": [float(x) for x in r],
                              "gestion": "indexada" if "indexada" in nombre else "activa"}
        if publicados:
            cd["flujo"] = [float(x) for x in fl]
        cats[nombre] = cd
    return {"taxonomia": "proveedor X, clase de activo", "frecuencia": "mensual", "fechas": fechas, "categorias": cats}


def _ctl_rend_indice(n: int) -> np.ndarray:
    t = np.arange(n)
    return 0.0003 + 0.01 * np.sin(t * 0.7)


def _ctl_td(identicos: bool) -> dict:
    ri = _ctl_rend_indice(3 * SESIONES_ANIO)
    miembros = {}
    for i in range(5):
        ter = 0.001 * (i + 1)
        rv = ri if identicos else ri - ter / SESIONES_ANIO + 0.0001 * np.cos(np.arange(ri.size) + i)
        mb: dict[str, Any] = {"rentabilidades": [float(x) for x in rv], "gastos_corrientes": 0.0 if identicos else ter,
                              "replicacion": "fisica" if i % 2 else "sintetica"}
        if not identicos:
            mb.update({"prestamo_valores": 0.0002, "diferencial_retencion": 0.0001})
        miembros[f"V{i + 1}"] = mb
    return {"rentabilidades_indice": [float(x) for x in ri], "variante_indice": "neta", "miembros": miembros}


def _ctl_lev(L: float) -> dict:
    n = SESIONES_ANIO
    r = np.where(np.arange(n) % 2 == 0, 0.01, -0.01)
    fechas = [str(x.date()) for x in pd.bdate_range("2023-01-02", periods=n)]
    return {"L": L, "horizonte": 100, "tipo_financiacion": 0.0, "gastos_medios": 0.0,
            "rentabilidades_indice": [float(x) for x in r], "fechas": fechas}


_CTL_CESTA = (50.0, 151.0, 1.0, 100.0)   # strikes de la cesta de control: desde, hasta, paso; forward


def _ctl_vrp(factor: float, cesta: bool = False) -> dict:
    n = 3 * SESIONES_ANIO + 1
    a = 0.01
    r = np.where(np.arange(n - 1) % 2 == 0, a, -a)
    precios = np.concatenate([[100.0], 100 * np.cumprod(1 + r)])
    iv = np.full(n, factor * a * math.sqrt(SESIONES_ANIO))
    v: dict[str, Any] = {"precios_subyacente": [float(x) for x in precios], "vol_implicita": [float(x) for x in iv],
                         "plazo_dias_vol_implicita": 30}
    if cesta:
        desde, hasta, paso, fwd = _CTL_CESTA
        T, s = 30 / DIAS_ANIO, float(iv[-1])
        K = np.arange(desde, hasta, paso)
        q = [_black(fwd, k, s, T, bool(k > fwd)) if k != fwd else (_black(fwd, k, s, T, True) + _black(fwd, k, s, T, False)) / 2
             for k in K]
        v["cesta_opciones"] = {"strikes": [float(x) for x in K], "q": q, "forward": fwd, "tipo_interes": 0.0, "dias": 30}
    return v


def _ctl_skew_hist() -> list[float]:
    return [float(0.03 + 0.01 * math.sin(i / 20)) for i in range(3 * SESIONES_ANIO)]


def _ctl_skew_svi() -> dict:
    T = 0.25
    x = np.array([0.008, 0.06, -0.4, 0.0, 0.15])
    K = 100 * np.exp(np.linspace(-0.4, 0.4, 17))
    k = np.log(K / 100)
    vol = np.sqrt(_svi(x, k)[0] / T)
    return {"vencimiento_meses": 3, "historia_rr": _ctl_skew_hist(),
            "superficie": {"strikes": [float(z) for z in K], "vols": [float(z) for z in vol], "forward": 100.0,
                           "spot": 100.0, "tipo_interes": 0.0}}


def _ctl_term(plana: bool) -> dict:
    vols = [0.20, 0.20, 0.20, 0.20] if plana else [0.25, 0.22, 0.21, 0.205]
    n = 3 * SESIONES_ANIO
    return {"vencimientos_meses": [1, 3, 6, 12], "vol_atm": vols, "calendario_eventos": [],
            "historia_vol_1m": [float(0.20 + 0.03 * math.sin(i / 15)) for i in range(n)],
            "historia_vol_3m": [0.21] * n}


def _ctl_roll(plana: bool) -> dict:
    S, r, q = 4000.0, 0.03, 0.01
    dias = [30.0, 120.0]
    precios = [S, S] if plana else [S * math.exp((r - q) * d / DIAS_ANIO) for d in dias]
    return {"tipo_activo": "indice", "spot": S, "tipo_financiacion": r, "rendimiento_dividendo": q,
            "futuros": [{"precio": precios[0], "dias": dias[0]}, {"precio": precios[1], "dias": dias[1]}],
            "periodo": {"spot_ini": 4000.0, "spot_fin": 4100.0, "futuro_ini": 4010.0, "futuro_fin": 4105.0,
                        "tipo_colateral": 0.03, "dias": 30}}


_Caso = dict[str, Any]
CASOS_CONTROL: dict[str, list[_Caso]] = {
    "FON-DISC-001": [
        {"nombre": "P = NAV ⇒ d = 0", "datos": [{"valores": _ctl_disc(iguales=True)}], "parametros": {},
         "comprobar": lambda r: abs(r["descuento_agregado_pct"]) <= 1e-10 and abs(r["verificacion"]["maximo_miembros_pct"]) <= 1e-10},
        {"nombre": "agregado entre el mínimo y el máximo de los miembros", "datos": [{"valores": _ctl_disc(iguales=False)}],
         "parametros": {},
         "comprobar": lambda r: r["verificacion"]["agregado_entre_min_y_max"]
         and r["verificacion"]["minimo_miembros_pct"] <= r["descuento_media_ponderada_pct"] <= r["verificacion"]["maximo_miembros_pct"]},
        {"nombre": "segunda vía: media ponderada frente a mediana (pesos iguales y simétricos ⇒ coinciden)",
         "datos": [{"valores": _ctl_disc(iguales=False, constante=True)}], "parametros": {},
         "comprobar": lambda r: abs(r["verificacion"]["segunda_via_ponderada_menos_mediana_pp"]) <= 1e-10
         and abs(r["descuento_agregado_pct"] + 6.0) <= 1e-10},
    ],
    "FON-FLOW-001": [
        {"nombre": "suma de flujos de las categorías = flujo total", "datos": [{"valores": _ctl_flow(False)}],
         "parametros": {},
         "comprobar": lambda r: r["verificacion"]["suma_categorias_vs_total_max_abs"] <= 1e-10 * max(abs(x) for x in r["flujo_total"])},
        {"nombre": "identidad de AUM con flujos publicados", "datos": [{"valores": _ctl_flow(True)}], "parametros": {},
         "comprobar": lambda r: all(x is not None and x <= 1e-10 for x in r["verificacion"]["identidad_aum_residuo_max_abs"].values())},
    ],
    "FON-TD-001": [
        {"nombre": "vehículo idéntico al índice ⇒ TD = 0 y TE = 0", "datos": [{"valores": _ctl_td(True)}],
         "parametros": {}, "comprobar": lambda r: r["td_mediana_pb"] == 0 and r["te_mediano_pct"] == 0},
        {"nombre": "componentes de la descomposición + residuo = TD", "datos": [{"valores": _ctl_td(False)}],
         "parametros": {},
         "comprobar": lambda r: abs(r["verificacion"]["descomposicion_mas_residuo_menos_td_pb"]) <= 1e-10 * max(1.0, abs(r["td_media_pb"]))},
    ],
    "FON-LEV-001": [
        {"nombre": "L = 1 ⇒ arrastre 0", "datos": [{"valores": _ctl_lev(1.0)}], "parametros": {},
         "comprobar": lambda r: r["arrastre_pct"] == 0},
        {"nombre": "reconstrucción diaria frente a fórmula dentro de la banda (discrepancia < arrastre) en serie sintética",
         "datos": [{"valores": _ctl_lev(2.0)}], "parametros": {},
         "comprobar": lambda r: abs(r["reconstruccion"]["discrepancia_ultima_pp"]) < r["arrastre_pct"]
         and r["reconstruccion"]["discrepancia_abs_max_pp"] < r["arrastre_pct"]},
    ],
    "DER-VRP-001": [
        {"nombre": "σ_imp = σ_real ⇒ VRP = 0", "datos": [{"valores": _ctl_vrp(1.0)}],
         "parametros": {"prevision_rv": "realizada_pasada"},
         "comprobar": lambda r: abs(r["vrp_ex_ante"]["varianza_puntos"]) <= 1e-8 * r["varianza_imp_puntos"]
         and abs(r["vrp_ex_post_ultima"]["varianza_puntos"]) <= 1e-8 * r["varianza_imp_puntos"]},
        {"nombre": "signo coherente entre VRP en varianza y en volatilidad", "datos": [{"valores": _ctl_vrp(1.3)}],
         "parametros": {},
         "comprobar": lambda r: r["vrp_ex_ante"]["varianza_puntos"] > 0 and r["vrp_ex_ante"]["volatilidad_puntos"] > 0
         and r["verificacion"]["signo_coherente_varianza_volatilidad"]},
        {"nombre": "segunda vía: índice publicado frente a réplica (cesta densa de una sonrisa plana)",
         "datos": [{"valores": _ctl_vrp(1.0, cesta=True)}], "parametros": {"prevision_rv": "realizada_pasada"},
         # Banda de discretización de la cesta: error relativo de la réplica < paso relativo de los strikes (ΔK/F).
         "comprobar": lambda r: r["replica"] is not None and abs(r["replica"]["diferencia_replica_menos_publicado_puntos"])
         / r["sigma_imp_pct"] < _CTL_CESTA[2] / _CTL_CESTA[3]},
    ],
    "DER-SKEW-001": [
        {"nombre": "sonrisa simétrica ⇒ RR = 0",
         "datos": [{"valores": {"vencimiento_meses": 3, "delta": 25, "vol_put": 0.22, "vol_call": 0.22, "vol_atm": 0.20,
                                "historia_rr": _ctl_skew_hist()}}], "parametros": {},
         "comprobar": lambda r: r["rr_puntos"] == 0 and r["pendiente_normalizada"] == 0},
        {"nombre": "SVI sin arbitraje de mariposa", "datos": [{"valores": _ctl_skew_svi()}], "parametros": {},
         "comprobar": lambda r: r["svi"]["sin_arbitraje_mariposa"] and r["svi"]["rmse_varianza_total"] <= 1e-8},
        {"nombre": "segunda vía: deltas frente a SVI", "datos": [{"valores": _ctl_skew_svi()}], "parametros": {},
         "comprobar": lambda r: r["segunda_via"] is not None
         and abs(r["segunda_via"]["rr_deltas_menos_svi_puntos"]) < abs(r["rr_puntos"])},
    ],
    "DER-TERM-001": [
        {"nombre": "curva plana ⇒ σ_fwd = σ", "datos": [{"valores": _ctl_term(True)}], "parametros": {},
         "comprobar": lambda r: all(abs(x["sigma_fwd_pct"] - 20.0) <= 1e-10 * 20.0 for x in r["sigma_fwd"])},
        {"nombre": "varianza total w monótona", "datos": [{"valores": _ctl_term(False)}], "parametros": {},
         "comprobar": lambda r: r["verificacion"]["varianza_total_monotona"]
         and all(b >= a for a, b in zip(r["verificacion"]["varianza_total"][:-1], r["verificacion"]["varianza_total"][1:]))},
    ],
    "DER-ROLL-001": [
        {"nombre": "F = S·e^{(r − q)T} ⇒ carry implícito = r − q", "datos": [{"valores": _ctl_roll(False)}],
         "parametros": {},
         "comprobar": lambda r: all(abs(f["carry_implicito_pct"] - 2.0) <= 1e-10 * 2.0 for f in r["vencimientos"])},
        {"nombre": "curva plana ⇒ roll 0", "datos": [{"valores": _ctl_roll(True)}], "parametros": {},
         "comprobar": lambda r: r["roll_yield_pct"] == 0},
        {"nombre": "suma de componentes = total", "datos": [{"valores": _ctl_roll(False)}], "parametros": {},
         "comprobar": lambda r: abs(r["descomposicion"]["suma_componentes_menos_total_pp"]) <= 1e-10},
    ],
}


def ejecutar_caso(ficha: str, caso: _Caso) -> tuple[dict, list[str]]:
    """Ejecuta un caso de control con la misma forma de entrada que usa el Motor."""
    ent: dict[str, Any] = {"valores": {}, "series": {}, "series_rol": {}}
    for d in caso["datos"]:
        ent["valores"].update(d.get("valores") or {})
    fn: Callable[[dict, dict], tuple[dict, list[str]]] = FICHAS[ficha]["fn"]
    return fn(ent, _p(ficha, caso.get("parametros")))
