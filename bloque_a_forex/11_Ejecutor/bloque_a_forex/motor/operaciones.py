"""Operaciones numéricas del Motor (fichas del Catálogo de cálculos del Motor - Bloque A Forex V1.0).

Convenciones (sección 3.1 del Catálogo): rendimientos simples por defecto (logarítmicos donde la ficha
lo pide), anualización 252 sesiones, cuantiles de tipo 7, redondeo solo al final. Pares en notación BASE/COTIZADA
(precio = unidades de cotizada por unidad de base) y dirección referida a la base (convención M17 del Catálogo).
"""
from __future__ import annotations

import math
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy import stats
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform


class ErrorFicha(ValueError):
    """Entrada insuficiente o no válida para la ficha (se traduce en RECHAZADO)."""


def _arr(x) -> np.ndarray:
    a = np.asarray(x, dtype=float)
    return a[~np.isnan(a)]


# ------------------------------------------------------------------ ST-DESC-001
def descriptiva(x: Sequence[float], cuantiles=(0.05, 0.25, 0.5, 0.75, 0.95)) -> Dict:
    a = _arr(x)
    n = len(a)
    if n < 5:
        raise ErrorFicha("ST-DESC-001: se necesitan al menos 5 observaciones")
    med = float(np.median(a))
    mad = float(np.median(np.abs(a - med)))
    desv = float(np.std(a, ddof=1))
    q = {str(c): float(np.quantile(a, c)) for c in cuantiles}  # tipo 7 (lineal)
    k = max(int(0.1 * n), 0)
    recortada = float(np.mean(np.sort(a)[k:n - k])) if n - 2 * k > 0 else float(np.mean(a))
    robusta = 1.4826 * mad if mad > 0 else desv
    atipicos = int(np.sum(np.abs(a - med) > 3 * robusta)) if robusta > 0 else 0
    return {"n": n, "media": float(np.mean(a)), "mediana": med, "media_recortada_10": recortada, "desviacion": desv,
            "iqr": float(np.quantile(a, 0.75) - np.quantile(a, 0.25)),
            "mad": mad, "asimetria": float(stats.skew(a, bias=False)) if n > 2 else None,
            "curtosis_exceso": float(stats.kurtosis(a, bias=False)) if n > 3 else None,
            "cuantiles": q, "atipicos_3_robustas": atipicos}


def posicion_historica(valor: float, historia: Sequence[float]) -> Dict:
    """z-score y percentil histórico del valor frente a su historia (ST-DESC-001, posición)."""
    h = _arr(historia)
    if len(h) < 5:
        raise ErrorFicha("Posición histórica: historia insuficiente (< 5)")
    sd = float(np.std(h, ddof=1))
    return {"z": float((valor - np.mean(h)) / sd) if sd > 0 else 0.0,
            "percentil": float(np.mean(h <= valor)), "media": float(np.mean(h)), "n": int(len(h))}


# ------------------------------------------------------------------ FIN-CAGR-001
def cagr(v_ini: float, v_fin: float, anios: float) -> float:
    if v_ini <= 0 or anios <= 0:
        raise ErrorFicha("FIN-CAGR-001: valor inicial y años deben ser positivos")
    return (v_fin / v_ini) ** (1.0 / anios) - 1.0


def real(nominal: float, inflacion: float) -> float:
    return (1 + nominal) / (1 + inflacion) - 1


def rentabilidades(precios: pd.Series, log: bool = False) -> pd.Series:
    p = precios.astype(float)
    return (np.log(p).diff() if log else p.pct_change()).dropna()


def rentabilidad_periodo(precios: pd.Series, sesiones: int) -> Optional[float]:
    if len(precios) <= sesiones:
        return None
    return float(precios.iloc[-1] / precios.iloc[-1 - sesiones] - 1)


# ------------------------------------------------------------------ FX-MOM-001 (12-1, TSMOM y rango transversal)
def momentum_12_1(precios: pd.Series, retro: int = 12, salto: int = 1, sesiones_mes: int = 21) -> Dict:
    n_necesario = retro * sesiones_mes + 1
    if len(precios) < n_necesario:
        raise ErrorFicha(f"FX-MOM-001: se necesitan al menos {retro + 1} meses de precios")
    p = precios.astype(float).values
    fin = -1 - salto * sesiones_mes
    ini = -1 - retro * sesiones_mes
    mom = p[fin] / p[ini] - 1
    r12 = p[-1] / p[ini] - 1
    rend = np.diff(np.log(p[-253:]))
    vol = float(np.std(rend, ddof=1) * math.sqrt(252)) if len(rend) > 2 else None
    return {"momentum": float(mom), "rent_12m": float(r12), "senal_tsmom": int(np.sign(r12)),
            "volatilidad_anual": vol, "rent_1m": float(p[-1] / p[-1 - sesiones_mes] - 1),
            "rent_3m": float(p[-1] / p[-1 - 3 * sesiones_mes] - 1)}


def rango_transversal(valores: Dict[str, float]) -> Dict[str, Dict]:
    """Percentil y z-score transversal dentro del universo del segmento."""
    claves = [k for k, v in valores.items() if v is not None and not np.isnan(v)]
    if not claves:
        return {}
    arr = np.array([valores[k] for k in claves])
    sd = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
    out = {}
    for k in claves:
        v = valores[k]
        out[k] = {"percentil": float(np.mean(arr <= v)), "z": float((v - arr.mean()) / sd) if sd > 0 else 0.0}
    return out


# ------------------------------------------------------------------ FX-VOL-001 / RI-EWMA / VOL-GARCH-001
def volatilidad(precios: pd.Series, ventana: int = 20, anual: int = 252) -> Dict:
    r = rentabilidades(precios, log=True)
    if len(r) < 30:
        raise ErrorFicha("FX-VOL-001: se necesitan al menos 30 observaciones")
    v = float(r.iloc[-ventana:].std(ddof=1) * math.sqrt(anual))
    v_alt = float(r.iloc[-2 * ventana:].std(ddof=1) * math.sqrt(anual))
    return {"volatilidad_anual": v, "ventana": ventana, "segunda_via_ventana_doble": v_alt,
            "ewma_anual": ewma_vol(r.values, 0.94, anual)}


def ewma_vol(rend: Sequence[float], lam: float = 0.94, anual: int = 252) -> float:
    r = _arr(rend)
    if len(r) < 2:
        raise ErrorFicha("EWMA: rendimientos insuficientes")
    var = float(np.var(r[: min(30, len(r))], ddof=1)) if len(r) > 2 else float(r[0] ** 2)
    for x in r:
        var = lam * var + (1 - lam) * x * x
    return float(math.sqrt(var * anual))


def garch11(precios: pd.Series, horizonte: int = 10, anual: int = 252) -> Dict:
    try:
        from arch import arch_model
    except ImportError as e:
        raise NotImplementedError("VOL-GARCH-001 requiere el paquete opcional «arch»") from e
    r = rentabilidades(precios, log=True) * 100
    if len(r) < 250:
        raise ErrorFicha("VOL-GARCH-001: se necesitan al menos 250 rendimientos")
    am = arch_model(r.values, vol="GARCH", p=1, q=1, dist="t", mean="Constant", rescale=False)
    res = am.fit(disp="off", options={"maxiter": 500})
    om, al, be = float(res.params["omega"]), float(res.params["alpha[1]"]), float(res.params["beta[1]"])
    pers = al + be
    prev = res.forecast(horizon=horizonte, reindex=False).variance.values[-1]
    return {"omega": om, "alpha": al, "beta": be, "persistencia": pers,
            "vida_media_sesiones": float(math.log(0.5) / math.log(pers)) if 0 < pers < 1 else None,
            "vol_largo_plazo_anual": float(math.sqrt(om / (1 - pers) * anual) / 100) if pers < 1 else None,
            "vol_condicional_anual": float(res.conditional_volatility[-1] * math.sqrt(anual) / 100),
            "vol_prevista_anual": [float(math.sqrt(v * anual) / 100) for v in prev],
            "integrado": bool(pers >= 1), "ewma_anual": ewma_vol(r.values / 100, 0.94, anual)}


# ------------------------------------------------------------------ RISK-DD-001
def drawdowns(precios: pd.Series) -> Dict:
    p = precios.astype(float).values
    pico = np.maximum.accumulate(p)
    dd = 1 - p / pico
    i_fondo = int(np.argmax(dd))
    i_pico = int(np.argmax(p[: i_fondo + 1])) if i_fondo > 0 else 0
    rec = np.where(p[i_fondo:] >= pico[i_fondo])[0]
    duracion = int((rec[0] if len(rec) else len(p) - 1 - i_fondo) + (i_fondo - i_pico))
    peores = np.sort(dd)[-max(int(0.05 * len(dd)), 1):]
    return {"mdd": float(dd.max()), "duracion_sesiones": duracion, "recuperado": bool(len(rec)),
            "cdar_95": float(peores.mean()), "drawdown_actual": float(dd[-1])}


UMBRALES_VOL_FX = (0.05, 0.09, 0.14, 0.20)
REGIMENES_SUELO = ("TIPO_FIJO", "CAJA_CONVERSION", "CONTROLES")


def escala_riesgo(precios: pd.Series, anual: int = 252, liquidez_limitada: bool = False, suelo_regimen: bool = False,
                  sentido: int = 1, umbrales: Sequence[float] = UMBRALES_VOL_FX, umbral_mdd: float = 0.25,
                  dias_liquidacion: Optional[float] = None) -> Dict:
    """RISK-DD-001 v2.0: base por volatilidad anualizada con umbrales cambiarios (< 5 % ⇒ 1; 5–9 % ⇒ 2; 9–14 % ⇒ 3;
    14–20 % ⇒ 4; ≥ 20 % ⇒ 5); +1 por colas (ES 97,5 % a 10 sesiones > 2,5·σ·√10 o asimetría semanal < −0,5 en la
    dirección de la exposición), +1 por liquidez limitada (NDF, controles, profundidad baja) y +1 por caída máxima
    > 25 %; suelo 4 para un tipo fijo con riesgo de ruptura o una divisa con controles; tope 5.
    `sentido` = −1 evalúa la exposición bajista (serie invertida)."""
    if len(precios) < 252:
        raise ErrorFicha("RISK-DD-001: se necesita al menos 1 año de datos")
    p = precios.astype(float)
    if sentido < 0:
        p = 1.0 / p
    r = rentabilidades(p, log=True)
    sd = float(r.std(ddof=1))
    vol = sd * math.sqrt(anual)
    u1, u2, u3, u4 = umbrales
    base = 1 if vol < u1 else 2 if vol < u2 else 3 if vol < u3 else 4 if vol < u4 else 5
    r10 = r.rolling(10).sum().dropna().values
    cola = np.sort(r10)[: max(int(math.ceil(0.025 * len(r10))), 1)]
    es975 = float(-cola.mean()) if len(cola) else 0.0
    sem = np.log(p.resample("W-FRI").last().dropna()).diff().dropna()
    asim = float(stats.skew(sem.values, bias=False)) if len(sem) > 10 else None
    dd = drawdowns(p)
    motivos = [f"volatilidad anualizada {vol:.1%} ⇒ base {base}"]
    ajustes = 0
    if es975 > 2.5 * sd * math.sqrt(10) or (asim is not None and asim < -0.5):
        ajustes += 1
        motivos.append("+1 colas (ES 97,5 % a 10 sesiones > 2,5·σ·√10 o asimetría semanal < −0,5)")
    if liquidez_limitada or (dias_liquidacion is not None and dias_liquidacion > 5):
        ajustes += 1
        motivos.append("+1 liquidez limitada (NDF, controles o profundidad baja)")
    if dd["mdd"] > umbral_mdd:
        ajustes += 1
        motivos.append(f"+1 caída máxima histórica > {umbral_mdd:.0%}")
    nivel = min(base + ajustes, 5)
    if suelo_regimen and nivel < 4:
        nivel = 4
        motivos.append("suelo 4 de régimen (tipo fijo con riesgo de ruptura o divisa con controles; nota 2 del Anexo A)")
    calmar = None
    anios = len(p) / anual
    if dd["mdd"] > 0 and anios > 0:
        calmar = float(((p.iloc[-1] / p.iloc[0]) ** (1 / anios) - 1) / dd["mdd"])
    lim = [] if len(p) >= 3 * anual else ["menos de 3 años de datos: el MDD puede subestimar el de largo plazo"]
    return {"riesgo_1a5": nivel, "base_volatilidad": base, "ajustes": ajustes, "suelo_regimen": bool(suelo_regimen),
            "volatilidad_anual": vol, "es975_10s": es975, "asimetria_semanal": asim, **dd, "calmar": calmar,
            "motivo": "; ".join(motivos), "limitaciones": lim}


# ------------------------------------------------------------------ FX-TREND-001
def _var_s(x: np.ndarray) -> float:
    n = len(x)
    _, cuentas = np.unique(x, return_counts=True)
    t = cuentas[cuentas > 1]
    return (n * (n - 1) * (2 * n + 5) - np.sum(t * (t - 1) * (2 * t + 5))) / 18.0


def mann_kendall(serie: Sequence[float], alpha: float = 0.05, corregir_autocorrelacion: bool = True) -> Dict:
    x = _arr(serie)
    n = len(x)
    if n < 10:
        raise ErrorFicha("FX-TREND-001: se necesitan al menos 10 observaciones")
    i, j = np.triu_indices(n, 1)
    s = float(np.sum(np.sign(x[j] - x[i])))
    var_s = _var_s(x)
    pendientes = (x[j] - x[i]) / (j - i)
    sen = float(np.median(pendientes))
    factor = 1.0
    if corregir_autocorrelacion and n >= 12:
        # Hamed y Rao (1998): autocorrelación de los rangos de la serie sin tendencia de Sen
        resid = x - sen * np.arange(n)
        rk = stats.rankdata(resid)
        rk = rk - rk.mean()
        den = np.sum(rk * rk)
        z_crit = stats.norm.ppf(1 - alpha / 2)
        acum = 0.0
        for k in range(1, n - 1):
            rho = float(np.sum(rk[:-k] * rk[k:]) / den) if den > 0 else 0.0
            if abs(rho) > z_crit / math.sqrt(n):
                acum += (n - k) * (n - k - 1) * (n - k - 2) * rho
        factor = max(1 + 2.0 / (n * (n - 1) * (n - 2)) * acum, 1e-6)
    var_c = var_s * factor
    z = (s - np.sign(s)) / math.sqrt(var_c) if s != 0 and var_c > 0 else 0.0
    p = float(2 * (1 - stats.norm.cdf(abs(z))))
    # IC de la pendiente de Sen (Gilbert, 1987)
    ps = np.sort(pendientes)
    c = stats.norm.ppf(1 - alpha / 2) * math.sqrt(var_s)
    m1, m2 = int(round((len(ps) - c) / 2)) - 1, int(round((len(ps) + c) / 2))
    m1, m2 = max(m1, 0), min(m2, len(ps) - 1)
    mitad = n // 2
    acel = None
    if n >= 20:
        acel = float(np.median(np.diff(x[mitad:])) - np.median(np.diff(x[:mitad])))
    mco = float(np.polyfit(np.arange(n), x, 1)[0])
    return {"S": s, "var_S": var_s, "factor_hamed_rao": factor, "Z": float(z), "p_valor": p,
            "tau": float(s / (n * (n - 1) / 2)), "pendiente_sen": sen, "ic_pendiente": [float(ps[m1]), float(ps[m2])],
            "direccion": "creciente" if (p < alpha and s > 0) else "decreciente" if (p < alpha and s < 0) else "sin tendencia",
            "aceleracion": acel, "segunda_via_pendiente_mco": mco, "n": n}


# ------------------------------------------------------------------ FX-CORR-001 / ML-CLUS-001
def correlaciones(rend: pd.DataFrame, cola_q: float = 0.05) -> Dict:
    r = rend.dropna()
    if len(r) < 60:
        raise ErrorFicha("FX-CORR-001: se necesitan al menos 60 observaciones comunes")
    pear = r.corr(method="pearson")
    spear = r.corr(method="spearman")
    colas = {}
    cols = list(r.columns)
    u = r.rank(pct=True)
    for a in range(len(cols)):
        for b in range(a + 1, len(cols)):
            ca, cb = u[cols[a]], u[cols[b]]
            den = float((ca <= cola_q).sum())
            colas[f"{cols[a]}|{cols[b]}"] = float(((ca <= cola_q) & (cb <= cola_q)).sum() / den) if den else None
    return {"pearson": pear.round(10).to_dict(), "spearman": spear.round(10).to_dict(), "cola_inferior": colas, "n": len(r)}


def clusteres(rend: pd.DataFrame, umbral_rho: float = 0.7) -> Dict:
    r = rend.dropna()
    cols = list(r.columns)
    if len(cols) == 0:
        return {"asignacion": {}, "n_clusteres": 0, "n_efectivo": 0.0}
    if len(cols) == 1:
        return {"asignacion": {cols[0]: 1}, "n_clusteres": 1, "n_efectivo": 1.0, "matriz": {cols[0]: {cols[0]: 1.0}}}
    if len(r) < 20:
        raise ErrorFicha("ML-CLUS-001: series no alineables o demasiado cortas")
    c = r.corr().fillna(0).to_numpy(copy=True)
    np.fill_diagonal(c, 1.0)
    d = np.sqrt(np.clip(2 * (1 - c), 0, None))
    np.fill_diagonal(d, 0.0)
    z = linkage(squareform(d, checks=False), method="average")
    etiquetas = fcluster(z, t=math.sqrt(2 * (1 - umbral_rho)), criterion="distance")
    # renumeración estable por orden de aparición
    mapa, asign = {}, {}
    for col, e in zip(cols, etiquetas):
        mapa.setdefault(int(e), len(mapa) + 1)
        asign[col] = mapa[int(e)]
    lam = np.clip(np.linalg.eigvalsh(c), 0, None)
    n_ef = float(lam.sum() ** 2 / np.sum(lam ** 2)) if np.sum(lam ** 2) > 0 else float(len(cols))
    return {"asignacion": asign, "n_clusteres": len(mapa), "n_efectivo": n_ef, "umbral_rho": umbral_rho,
            "matriz": pd.DataFrame(c, index=cols, columns=cols).round(6).to_dict()}


# ------------------------------------------------------------------ FX-CARRY-001 (núcleo v1.1 y v2.0)
def carry_divisas(tipo_base: float, tipo_cotizada: float, spot_ini: float, spot_fin: float, anios: float) -> Dict:
    """Núcleo v1.1. Par BASE/COTIZADA, posición larga en la base; tipos en tanto por uno anual.
    Rentabilidad total = variación cambiaria + carry·años (identidad aditiva)."""
    diferencial = tipo_base - tipo_cotizada
    var_spot = spot_fin / spot_ini - 1
    carry = diferencial * anios
    return {"diferencial_anual": diferencial, "carry_periodo": carry, "variacion_cambiaria": var_spot,
            "rentabilidad_total": var_spot + carry, "referencia_ingenua_RI_PA": carry}


def signo_carry(carry_pct: Optional[float], umbral_pct: float = 0.25) -> str:
    if carry_pct is None:
        return "no aplicable"
    return "a favor" if carry_pct > umbral_pct else "en contra" if carry_pct < -umbral_pct else "neutro"


def carry_exposicion(tipo_base: float, tipo_cotizada: float, direccion: str = "ALCISTA_BASE",
                     vol_anual: Optional[float] = None, inflacion_base: Optional[float] = None,
                     inflacion_cotizada: Optional[float] = None, horizonte_anios: float = 0.25) -> Dict:
    """v2.0, pasos (ii)–(v): carry anual de la exposición con su signo respecto de la dirección, carry ajustado por
    volatilidad, carry real y equilibrio (movimiento adverso del contado que lo anula en el horizonte)."""
    if direccion not in ("ALCISTA_BASE", "BAJISTA_BASE"):
        raise ErrorFicha("FX-CARRY-001: dirección ambigua (ALCISTA_BASE o BAJISTA_BASE)")
    dif = tipo_base - tipo_cotizada
    carry = dif if direccion == "ALCISTA_BASE" else -dif
    out = {"diferencial_anual": dif, "carry_anual": carry, "carry_anual_pct": 100 * carry,
           "signo": signo_carry(100 * carry), "carry_ajustado_vol": carry_ajustado_vol(carry, vol_anual),
           "equilibrio_pct": 100 * carry * horizonte_anios,
           "equilibrio_sigmas": (carry * horizonte_anios / (vol_anual * math.sqrt(horizonte_anios))) if vol_anual else None}
    if inflacion_base is not None and inflacion_cotizada is not None:
        real_dif = (tipo_base - inflacion_base) - (tipo_cotizada - inflacion_cotizada)
        out["carry_real_anual"] = real_dif if direccion == "ALCISTA_BASE" else -real_dif
    return out


def carry_ajustado_vol(diferencial_anual: float, vol_anual: Optional[float]) -> Optional[float]:
    return diferencial_anual / vol_anual if vol_anual and vol_anual > 0 else None


# ------------------------------------------------------------------ FX-FWD-001
def forward_teorico(spot: float, tipo_base: float, tipo_cotizada: float, dias: float, base_dias_base: int = 360,
                    base_dias_cotizada: int = 360, escala_pip: float = 1e-4) -> Dict:
    """Forward por paridad cubierta F = S·(1 + i_c·d/B_c)/(1 + i_b·d/B_b), puntos forward y carry implícito anualizado
    de una posición larga en la base −(F − S)/S·(1/τ)."""
    if spot <= 0 or dias <= 0:
        raise ErrorFicha("FX-FWD-001: contado y plazo deben ser positivos")
    tb, tc = dias / base_dias_base, dias / base_dias_cotizada
    f = spot * (1 + tipo_cotizada * tc) / (1 + tipo_base * tb)
    tau = dias / 365.0
    return {"forward": f, "puntos_pips": (f - spot) / escala_pip, "cambio_forward": f / spot - 1,
            "carry_implicito_anual": -(f - spot) / spot / tau, "plazo_dias": dias}


def rendimiento_implicito_base(spot: float, forward: float, tipo_cotizada: float, dias: float,
                               base_dias_base: int = 360, base_dias_cotizada: int = 360) -> float:
    """i_b implícito = [(S/F)·(1 + i_c·τ_c) − 1]/τ_b (FX-FWD-001, paso iii)."""
    tb, tc = dias / base_dias_base, dias / base_dias_cotizada
    return ((spot / forward) * (1 + tipo_cotizada * tc) - 1) / tb


# ------------------------------------------------------------------ FX-PPP-001 (PPA relativa, versión sencilla)
def ppa_relativa(spot: pd.Series, precios_base: pd.Series, precios_cotizada: pd.Series) -> Dict:
    """S_PPA,t = S_0·(P_c,t/P_c,0)/(P_b,t/P_b,0) con base = media de largo plazo del tipo real; desviación
    100·ln(S/S_PPA) (positiva = base cara) y persistencia AR(1) por MCO del tipo real con vida media."""
    al = pd.concat([spot, precios_base, precios_cotizada], axis=1, join="inner").dropna()
    if len(al) < 24:
        raise ErrorFicha("FX-PPP-001: se necesitan al menos 24 observaciones alineadas")
    s, pb, pc = (al.iloc[:, k].astype(float) for k in range(3))
    q = np.log(s) + np.log(pb) - np.log(pc)                 # tipo de cambio real en log (precio relativo de la base)
    desv = 100 * (q - q.mean())
    s_ppa = float(np.exp(np.log(s.iloc[-1]) - (q.iloc[-1] - q.mean())))
    x, y = q.values[:-1] - q.mean(), q.values[1:] - q.mean()
    rho = float(np.dot(x, y) / np.dot(x, x)) if np.dot(x, x) > 0 else None
    vida = float(math.log(0.5) / math.log(rho)) if rho is not None and 0 < rho < 1 else None
    return {"desviacion_pct": float(desv.iloc[-1]), "valor_ppa": s_ppa, "rho_ar1": rho, "vida_media_periodos": vida,
            "n": int(len(al)), "base": "media de largo plazo del tipo real"}


# ------------------------------------------------------------------ RI-PA / RI-FWD probabilísticas y FX-RW-001
def prob_paseo_aleatorio(spot: float, umbral: Optional[float], vol_anual: Optional[float], anios: float,
                         sube: bool = True, centro: Optional[float] = None) -> float:
    """RI-PA probabilística: p = 0,5 para «sube/baja» frente al contado; para un umbral, ln S_T ~ N(ln S_t, σ²·τ)
    (lognormal sin deriva con la volatilidad conocida en t). Con `centro` = forward se obtiene RI-FWD."""
    c = spot if centro is None else centro
    k = spot if umbral is None else umbral
    if centro is None and (umbral is None or umbral == spot):
        return 0.5
    if not vol_anual or vol_anual <= 0 or anios <= 0:
        return 0.5 if c == k else (1.0 if (c > k) == sube else 0.0)
    z = (math.log(c) - math.log(k)) / (vol_anual * math.sqrt(anios))
    p_sube = float(stats.norm.cdf(z))
    return p_sube if sube else 1.0 - p_sube


def evaluar_frente_rw(p: Sequence[float], o: Sequence[int], p_fwd: Optional[Sequence[float]] = None) -> Dict:
    """FX-RW-001 (versión sencilla): Brier del pronóstico, de RI-PA (0,5) y de RI-FWD; BSS frente a RI-PA y RI-FWD
    y acierto direccional frente al 50 %."""
    pa, oa = np.asarray(p, float), np.asarray(o, float)
    if len(pa) == 0 or len(pa) != len(oa):
        raise ErrorFicha("FX-RW-001: pronósticos y realizaciones deben tener la misma longitud (> 0)")
    b = float(np.mean((pa - oa) ** 2))
    b_pa = float(np.mean((0.5 - oa) ** 2))
    out = {"n": int(len(pa)), "brier": b, "brier_RI_PA": b_pa, "bss_RI_PA": 1 - b / b_pa if b_pa > 0 else None,
           "acierto": float(np.mean((pa >= 0.5) == (oa == 1))),
           "p_binomial_acierto": float(stats.binomtest(int(np.sum((pa >= 0.5) == (oa == 1))), len(pa), 0.5,
                                                         alternative="greater").pvalue)}
    if p_fwd is not None:
        pf = np.asarray(p_fwd, float)
        b_f = float(np.mean((pf - oa) ** 2))
        out.update({"brier_RI_FWD": b_f, "bss_RI_FWD": 1 - b / b_f if b_f > 0 else None})
    return out


# ------------------------------------------------------------------ SCORE-RK-001 (reimplementación independiente)
def _redondeo_5(x: Fraction) -> int:
    base = (x / 5)
    ent = math.floor(base)
    resto = base - ent
    return int(5 * (ent + (1 if resto > Fraction(1, 2) else 0)))


def puntuacion_total(dims: Dict, pesos: Dict, tope_valoracion: Optional[int] = None) -> Optional[int]:
    """Media ponderada con NA (redistribución) y NE (= 0), máximo 2 NA/NE, redondeo a 5 (empates abajo)."""
    na_ne = sum(1 for k in pesos if str(dims.get(k, "NE")).upper() in ("NA", "NE"))
    if na_ne > 2:
        raise ErrorFicha("SCORE-RK-001: más de dos NA/NE")
    num, den = Fraction(0), Fraction(0)
    for k, w in pesos.items():
        v = dims.get(k, "NE")
        if isinstance(v, str) and v.upper() == "NA":
            continue
        val = 0 if isinstance(v, str) else v
        if k == "valoracion" and tope_valoracion is not None:
            val = min(val, tope_valoracion)
        num += Fraction(w) * Fraction(val)
        den += Fraction(w)
    return _redondeo_5(num / den) if den else None


def clave_rk(A: int, E: int, T: Optional[int], pesos=(0.45, 0.35, 0.20)) -> int:
    wa, we, wt = (Fraction(str(w)) for w in pesos)
    if T is None:
        x = (wa * A + we * E) / (wa + we)
    else:
        x = wa * A + we * E + wt * T
    ent = math.floor(x)
    return int(ent + (1 if x - ent > Fraction(1, 2) else 0))
