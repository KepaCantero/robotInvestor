"""QA r02 de T-106 · Oráculos independientes, escritos por el revisor a partir de la ficha del Catálogo (no del código),
para las fichas que la r01 no recalculó y para MON-EXP-001, que la r02 rehízo:

  - MON-EXP-001 (método nuevo): senda escalonada exacta con nodos en las reuniones y con nodos fuera de ellas
    (sistema sobredeterminado); forwards entre reuniones recalculados aparte; curva redondeada sin y con
    `precision_cotizacion` (si se sirve, el error real de la senda debe quedar dentro de la cota que se declara);
    curva suave no escalonada (no debe inventar movimientos); tira de futuros; cambio acumulado a 6 y 12 meses.
  - FON-DISC-001: d = P/NAV − 1, mediana, z a 52 semanas, normalización con κ, AR(1) y vida media en meses.
  - FON-FLOW-001: flujo por la identidad de AUM, flujo relativo, acumulados, z a 36 meses, autocorrelaciones (statsmodels),
    rango y suma por categorías.
  - DER-TERM-001: varianza total interpolada, pendiente, ratio, σ_fwd y movimiento de un evento.
  - TCV-SLOPE-001: pendiente 2s10s, regresión MCO con HAC de Newey-West (statsmodels, sin corrección), IC, pendiente
    forward a 3 y 6 meses y carry + rolldown neutral en DV01.
  - TCV-VIXTS-001: estado, roll, futuro a 30 días, rentabilidad esperada, percentil, frecuencia de contango y ES.

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r02_02_oraculos.py [RAIZ]
"""
from __future__ import annotations

import math
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

M = C.preparar(sys.argv[1] if len(sys.argv) > 1 else None)
S, EF = M["servicio"], M["ErrorFicha"]
warnings.simplefilter("ignore")
from scipy.stats import norm  # noqa: E402
from statsmodels.regression.linear_model import OLS  # noqa: E402
from statsmodels.tsa.stattools import acf  # noqa: E402


def llamar(ficha, valores, params=None, roles=None):
    try:
        r, lim = S.IMPLEMENTADAS[ficha]["fn"]({"valores": valores, "series": {}, "series_rol": roles or {}}, dict(params or {}))
        return r, lim, None
    except EF as e:
        return None, None, str(e)


def cerca(a, b, tol):
    return a is not None and b is not None and abs(float(a) - float(b)) <= tol


rng = np.random.default_rng(20261113)

# ====================================================================== MON-EXP-001
BASE = 360.0
FECHA = pd.Timestamp("2026-11-12")
REUN = ["2026-12-17", "2027-02-04", "2027-04-29", "2027-07-22", "2027-10-28"]
CORTES = [0] + [(pd.Timestamp(m) - FECHA).days for m in REUN]
OFICIAL, DIF = 0.0200, 0.0008
R0 = OFICIAL - DIF
VERDAD = [R0, R0 - 0.0025, R0 - 0.0050, R0 - 0.0050, R0 - 0.0025, R0 - 0.0050]   # bajada, bajada, pausa, subida, bajada


def log_factor(d, senda=VERDAD):
    lg = 0.0
    for k, a in enumerate(CORTES):
        b = CORTES[k + 1] if k + 1 < len(CORTES) else 10 ** 9
        if a >= d:
            break
        lg += (min(b, d) - a) * math.log1p(senda[k] / BASE)
    return lg


def curva(dias, senda=VERDAD, redondeo=None):
    out = []
    for d in dias:
        t = math.expm1(log_factor(d, senda)) * BASE / d
        out.append({"dias": d, "tipo": round(t, redondeo) if redondeo else t})
    return out


def exp_valores(cv, **extra):
    return {"fecha": str(FECHA.date()), "base_curva": BASE, "curva": cv, "tipo_oficial": OFICIAL,
            "diferencial_estable": DIF, "reuniones": list(REUN), **extra}


def fwd_entre(cv, d1, d2):
    """Oráculo: tipo a un día constante entre d1 y d2 a partir de los factores de la curva (d1 = 0 ⇒ factor 1)."""
    tab = {n["dias"]: math.log1p(n["tipo"] * n["dias"] / BASE) for n in cv}
    l1 = tab.get(d1, 0.0) if d1 else 0.0
    return math.expm1((tab[d2] - l1) / (d2 - d1)) * BASE


# (a) nodos en las fechas de reunión (sistema justo pero alineado: cada tramo es un forward entre puntos conocidos)
d_fin = CORTES[-1] + 60
nodos_a = CORTES[1:] + [d_fin]
cv = curva(nodos_a)
r, lim, err = llamar("MON-EXP-001", exp_valores(cv))
if err:
    C.informe("MON-EXP (a) nodos en las reuniones: se sirve", False, err[:200])
else:
    obt = [s["tipo_mercado_implicito"] for s in r["senda"]]
    orac = [fwd_entre(cv, CORTES[k], (CORTES + [d_fin])[k + 1]) for k in range(1, len(CORTES))]
    C.informe("MON-EXP (a) tramos = forwards entre reuniones (oráculo propio) = senda verdadera",
              np.allclose(obt, orac, atol=1e-12, rtol=0) and np.allclose(obt, VERDAD[1:], atol=1e-12, rtol=0),
              f"máx |obt − oráculo| = {max(abs(a - b) for a, b in zip(obt, orac)):.2e}")
    mov = [s["movimientos_en_reunion"] for s in r["senda"]]
    acu = [s["movimientos_acumulados"] for s in r["senda"]]
    C.informe("MON-EXP (a) movimientos por reunión [−1, −1, 0, +1, −1] y acumulados [−1, −2, −2, −1, −2]",
              np.allclose(mov, [-1, -1, 0, 1, -1], atol=1e-8) and np.allclose(acu, [-1, -2, -2, -1, -2], atol=1e-8),
              f"{np.round(mov, 9)} · {np.round(acu, 9)}")
    probs_ok = all(abs(sum(s["probabilidades"]["movimientos"].values()) - 1) < 1e-12 for s in r["senda"])
    C.informe("MON-EXP (a) probabilidades binarias suman 1", probs_ok)
    d6 = (FECHA + pd.DateOffset(months=6) - FECHA).days
    d12 = (FECHA + pd.DateOffset(months=12) - FECHA).days
    vig = lambda d: VERDAD[max(k for k in range(len(VERDAD)) if CORTES[k] <= d)]  # noqa: E731
    C.informe("MON-EXP (a) cambio acumulado a 6 y 12 meses = tipo vigente ese día − r0 (pb)",
              cerca(r["cambio_acumulado_pb"]["6m"], (vig(d6) - R0) * 1e4, 1e-8)
              and cerca(r["cambio_acumulado_pb"]["12m"], (vig(d12) - R0) * 1e4, 1e-8), str(r["cambio_acumulado_pb"]))

# (b) nodos fuera de las reuniones, sobredeterminado (dos por tramo)
nodos_b = sorted({c + 12 for c in CORTES[1:]} | {c + 30 for c in CORTES[1:]} | {20})
r, lim, err = llamar("MON-EXP-001", exp_valores(curva(nodos_b)))
C.informe("MON-EXP (b) nodos fuera de las reuniones (sobredeterminado, exacto): recupera la senda",
          err is None and np.allclose([s["tipo_mercado_implicito"] for s in r["senda"]], VERDAD[1:], atol=1e-12, rtol=0),
          err[:160] if err else "")

# (c) la misma curva redondeada a 0,1 pb (5 decimales), sin declarar la precisión: no se reproduce ⇒ rechazo
cv_red = curva(nodos_b, redondeo=5)
r, lim, err = llamar("MON-EXP-001", exp_valores(cv_red))
C.informe("MON-EXP (c) curva redondeada a 0,1 pb sin precisión declarada: rechazo (no inventa)", err is not None,
          (err or "SERVIDA")[:160])

# (d) con precision_cotizacion = 0,05 pb (medio dígito): si se sirve, el error real ≤ la cota declarada
for prec, etiqueta in ((5e-6, "0,05 pb"), (5e-5, "0,5 pb")):
    for nodos, nom in ((nodos_b, "nodos a +12 y +30 días"), (sorted({c + 3 for c in CORTES[1:]} | {c + 40 for c in CORTES[1:]} | {20}), "nodos a +3 y +40 días")):
        cvr = curva(nodos, redondeo=5 if prec == 5e-6 else 4)
        r, lim, err = llamar("MON-EXP-001", exp_valores(cvr, precision_cotizacion=prec))
        if err:
            C.informe(f"MON-EXP (d) {nom}, precisión {etiqueta}: rechazada con motivo", "identificada" in err or "reproducir" in err
                      or "contrastar" in err, err[:150])
            continue
        errs = [abs(s["tipo_mercado_implicito"] - t) * 1e4 for s, t in zip(r["senda"], VERDAD[1:])]
        cotas = [s["incertidumbre_redondeo_pb"] for s in r["senda"]]
        C.informe(f"MON-EXP (d) {nom}, precisión {etiqueta}: error real de cada tramo ≤ cota declarada (y < Δ)",
                  all(e <= c * (1 + 1e-9) + 1e-9 for e, c in zip(errs, cotas)) and max(errs) < 25,
                  f"errores {np.round(errs, 3)} pb · cotas {np.round(cotas, 3)} pb")

# (e) curva suave no escalonada (OIS lineal 1,92 % → 1,60 % en 12 meses), sobredeterminada: no debe servir movimientos
suave = [{"dias": d, "tipo": 0.0192 + (0.0160 - 0.0192) * d / 365} for d in (20, 60, 90, 120, 180, 240, 300, 365, 420)]
r, lim, err = llamar("MON-EXP-001", exp_valores(suave))
C.informe("MON-EXP (e) curva suave no escalonada, exacta: rechazo (no admite una senda escalonada)", err is not None,
          (err or f"SERVIDA: movimientos {[round(s['movimientos_en_reunion'], 2) for s in r['senda']]}")[:180])
r, lim, err = llamar("MON-EXP-001", exp_valores(suave, precision_cotizacion=1e-4))
if err:
    C.informe("MON-EXP (e') curva suave con precisión declarada de 1 pb: rechazo", True, err[:150])
else:
    mov = [s["movimientos_en_reunion"] for s in r["senda"]]
    C.informe("MON-EXP (e') curva suave con precisión declarada de 1 pb: si se sirve, movimientos acotados (|m| ≤ 2)",
              max(abs(m) for m in mov) <= 2, f"movimientos {np.round(mov, 2)}")

# (f) tira de futuros contigua (tipo = 100 − precio) que replica la senda; tramos = forwards de los contratos
tramos = list(zip(CORTES, CORTES[1:] + [d_fin]))
futs = []
for (a, b), t in zip(tramos, VERDAD):
    ini, fin = FECHA + pd.Timedelta(days=a), FECHA + pd.Timedelta(days=b)
    tipo_simple = math.expm1((b - a) * math.log1p(t / BASE)) * BASE / (b - a)
    futs.append({"inicio": str(ini.date()), "fin": str(fin.date()), "precio": 100 - 100 * tipo_simple})
vf = exp_valores(None)
vf.pop("curva")
vf["futuros"] = futs
r, lim, err = llamar("MON-EXP-001", vf, {"convexidad": False})
C.informe("MON-EXP (f) tira de futuros alineada con las reuniones: recupera la senda",
          err is None and np.allclose([s["tipo_mercado_implicito"] for s in r["senda"]], VERDAD[1:], atol=1e-11, rtol=0),
          (err or "")[:160])

# ====================================================================== FON-DISC-001
fechas = pd.date_range("2021-11-05", periods=4 * 52 + 1, freq="7D")
n = len(fechas)
miembros = {}
D = []
for i in range(6):
    nav = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))
    dsc = -0.08 + 0.03 * np.sin(np.arange(n) / 15 + i) + rng.normal(0, 0.005, n)
    pr = nav * (1 + dsc)
    miembros[f"F{i}"] = {"precio": pr.tolist(), "nav": nav.tolist(), "fecha_nav": str(fechas[-1].date())}
    D.append(pr / nav - 1)
D = np.vstack(D)
v = {"fechas": [str(x.date()) for x in fechas], "miembros": miembros, "rentabilidad_nav_supuesta": 0.04,
     "catalizadores": ["recompras"]}
r, lim, err = llamar("FON-DISC-001", v, {"kappa": 0.3})
if err:
    C.informe("FON-DISC se sirve con datos válidos", False, err)
else:
    agg = np.median(D, axis=0)
    d = agg[-1]
    m52 = fechas > fechas[-1] - pd.Timedelta(weeks=52)
    h = agg[m52]
    z = (d - h.mean()) / h.std(ddof=1)
    dobj = d + 0.3 * (h.mean() - d)
    rn = ((1 + dobj) / (1 + d) - 1) * 100
    C.informe("FON-DISC descuento agregado = mediana(P/NAV − 1)", cerca(r["descuento_agregado_pct"], d * 100, 1e-12))
    C.informe("FON-DISC z frente a 52 semanas", cerca(r["z_scores"]["ventana_media"], z, 1e-9), f"{r['z_scores']['ventana_media']} vs {z}")
    C.informe("FON-DISC normalización con κ = 0,3: (1 + d_obj)/(1 + d) − 1", cerca(r["rentabilidad_normalizacion_pct"], rn, 1e-10))
    C.informe("FON-DISC total con NAV supuesto = (1 + rn)(1 + r_NAV) − 1",
              cerca(r["normalizacion"]["ventana_media"]["rentabilidad_total_supuesta_pct"], ((1 + rn / 100) * 1.04 - 1) * 100, 1e-10))
    phi = np.polyfit(agg[:-1], agg[1:], 1)[0]
    vida = math.log(0.5) / math.log(phi) * 7 * 12 / 365
    C.informe("FON-DISC AR(1) y vida media en meses", cerca(r["phi_ar1"], phi, 1e-9) and cerca(r["vida_media_meses"], vida, 1e-7),
              f"φ {r['phi_ar1']:.6f} vs {phi:.6f}; vida {r['vida_media_meses']:.4f} vs {vida:.4f}")
    C.informe("FON-DISC agregado entre el mínimo y el máximo de los miembros", min(D[:, -1]) <= d <= max(D[:, -1])
              and r["verificacion"]["agregado_entre_min_y_max"])

# ====================================================================== FON-FLOW-001
fm = pd.date_range("2021-10-31", periods=49, freq="ME")
cats, FL, AP = {}, {}, {}
for c in ("acciones", "bonos", "mixtos"):
    aum = [1000.0 * (1 + rng.random())]
    rent = rng.normal(0.005, 0.02, len(fm) - 1)
    flu = rng.normal(5, 20, len(fm) - 1)
    for k in range(len(fm) - 1):
        aum.append(aum[-1] * (1 + rent[k]) + flu[k])
    aum = np.array(aum)
    cats[c] = {"aum": aum.tolist(), "rentabilidad": rent.tolist(), "gestion": "indexada" if c != "mixtos" else "activa"}
    FL[c], AP[c] = aum[1:] - aum[:-1] * (1 + rent), aum[:-1]
v = {"taxonomia": "propia QA", "frecuencia": "mensual", "fechas": [str(x.date()) for x in fm], "categorias": cats}
r, lim, err = llamar("FON-FLOW-001", v)
if err:
    C.informe("FON-FLOW se sirve con datos válidos", False, err)
else:
    ok_f = ok_z = ok_a = ok_ac = True
    for c in cats:
        t = r["categorias"][c]
        rel = FL[c] / AP[c]
        ok_f &= cerca(t["flujo_ultimo"], FL[c][-1], 1e-8) and cerca(t["flujo_relativo_ultimo_pct"], rel[-1] * 100, 1e-10)
        h = rel[-36:]
        ok_z &= cerca(t["z_score"], (rel[-1] - h.mean()) / h.std(ddof=1), 1e-9)
        ac = acf(rel, nlags=3, fft=False)
        ok_a &= all(cerca(t["autocorrelaciones"][str(k)], ac[k], 1e-10) for k in (1, 2, 3))
        ok_ac &= cerca(t["acumulados"]["3"]["moneda"], FL[c][-3:].sum(), 1e-8) and \
            cerca(t["acumulados"]["3"]["pct_aum"], FL[c][-3:].sum() / AP[c][-3] * 100, 1e-10) and \
            cerca(t["acumulados"]["12"]["pct_aum"], FL[c][-12:].sum() / AP[c][-12] * 100, 1e-10)
    C.informe("FON-FLOW flujo = AUM_t − AUM_{t−1}(1 + r_t) y flujo relativo", ok_f)
    C.informe("FON-FLOW z del flujo relativo frente a 36 meses", ok_z)
    C.informe("FON-FLOW autocorrelaciones de orden 1–3 = acf de statsmodels", ok_a)
    C.informe("FON-FLOW acumulados a 3 y 12 meses (moneda y % del AUM al inicio de la ventana)", ok_ac)
    tot = sum(FL.values())
    C.informe("FON-FLOW suma de categorías = flujo total", np.allclose(r["flujo_total"], tot, atol=1e-8))
    orden = sorted(cats, key=lambda c: -FL[c][-12:].sum() / AP[c][-12])
    C.informe("FON-FLOW rango a 12 meses (1 = mayor flujo relativo)", [r["categorias"][c]["rango"]["12"] for c in orden] == [1, 2, 3])

# ====================================================================== DER-TERM-001
mv = np.array([1.0, 2.0, 3.0, 6.0, 12.0])
vol = np.array([0.24, 0.215, 0.21, 0.205, 0.20])
nh = 3 * 252
h1 = 0.18 + 0.03 * np.sin(np.arange(nh) / 40)
h3 = 0.19 + 0.01 * np.cos(np.arange(nh) / 50)
v = {"vencimientos_meses": mv.tolist(), "vol_atm": vol.tolist(), "historia_vol_1m": h1.tolist(), "historia_vol_3m": h3.tolist(),
     "calendario_eventos": [{"nombre": "elecciones", "vencimiento_meses": 2.0, "sigma_base": 0.20, "fuente_sigma_base": "QA"}]}
r, lim, err = llamar("DER-TERM-001", v)
if err:
    C.informe("DER-TERM se sirve con datos válidos", False, err)
else:
    T = mv / 12
    w = vol ** 2 * T
    sig = lambda m: math.sqrt(np.interp(m / 12, T, w) / (m / 12))  # noqa: E731
    C.informe("DER-TERM σ por vencimiento por varianza total lineal en T",
              all(cerca(r["sigma_por_vencimiento_pct"][f"{m:g}"], sig(m) * 100, 1e-12) for m in (1, 3, 6, 12)))
    C.informe("DER-TERM pendiente σ(3m) − σ(1m), ratio y estado INVERTIDA",
              cerca(r["pendiente_puntos"], (sig(3) - sig(1)) * 100, 1e-12) and cerca(r["ratio_1m_3m"], sig(1) / sig(3), 1e-12)
              and r["estado"] == "INVERTIDA")
    f36 = math.sqrt((sig(6) ** 2 * 0.5 - sig(3) ** 2 * 0.25) / 0.25) * 100
    C.informe("DER-TERM σ_fwd 3m→6m", cerca(r["sigma_fwd"][1]["sigma_fwd_pct"], f36, 1e-10), f"{r['sigma_fwd'][1]} vs {f36}")
    ve = 0.215 ** 2 * 2 / 12 - 0.20 ** 2 * 2 / 12
    C.informe("DER-TERM movimiento del evento = √(σ²_con·T − σ²_base·T)",
              cerca(r["eventos"][0]["movimiento_descontado_pct"], math.sqrt(ve) * 100, 1e-12))
    C.informe("DER-TERM frecuencia histórica de inversiones", cerca(r["inversiones_historicas"]["frecuencia_pct"],
              float(np.mean(h1 / h3 > 1)) * 100, 1e-12))

# ====================================================================== TCV-SLOPE-001
fw = pd.date_range("2014-01-03", periods=12 * 52, freq="7D")
pl = np.array([0.25, 1, 2, 3, 5, 7, 10, 20])
nf = len(fw)
nivel = 2 + np.cumsum(rng.normal(0, 0.03, nf))
pend_v = 1 + np.cumsum(rng.normal(0, 0.02, nf))
X1 = rng.normal(0, 1, nf)
X2 = np.cumsum(rng.normal(0, 0.1, nf))
pend_v = pend_v + 0.3 * X1
Rm = np.array([[nv + pv * (1 - math.exp(-t / 3)) for t in pl] for nv, pv in zip(nivel, pend_v)])
regs = {nom: {"serie": s.tolist(), "conocible_desde": [str(x.date()) for x in fw], "fuente": "QA"}
        for nom, s in (("x1", X1), ("x2", X2))}
v = {"historia_curva": {"fechas": [str(x.date()) for x in fw], "plazos": pl.tolist(), "rendimientos": Rm.tolist()},
     "regresores": regs}
r, lim, err = llamar("TCV-SLOPE-001", v, {"regresores": ["x1", "x2"]})
if err:
    C.informe("TCV-SLOPE se sirve con datos válidos", False, err)
else:
    t = r["tramos"]["2s10s"]
    ya = np.array([np.interp(2, pl, f) for f in Rm])
    yb = np.array([np.interp(10, pl, f) for f in Rm])
    pend = (yb - ya) * 100
    Xr = np.column_stack([np.ones(nf), X1, X2])
    nest = nf - 1
    L = math.floor(4 * (nest / 100) ** (2 / 9))
    mod = OLS(pend[:-1], Xr[:-1]).fit(cov_type="HAC", cov_kwds={"maxlags": L, "use_correction": False})
    raz = float(Xr[-1] @ mod.params)
    ee = math.sqrt(float(Xr[-1] @ mod.cov_params() @ Xr[-1]))
    C.informe("TCV-SLOPE pendiente 2s10s (pb)", cerca(t["pendiente_pb"], pend[-1], 1e-9))
    C.informe("TCV-SLOPE coeficientes MCO = statsmodels", np.allclose(list(t["regresion"]["coeficientes"].values()), mod.params, atol=1e-9))
    C.informe("TCV-SLOPE errores HAC (Newey-West, Bartlett, L = ⌊4(T/100)^(2/9)⌋) = statsmodels",
              np.allclose(list(t["regresion"]["errores_hac"].values()), mod.bse, rtol=1e-8) and t["regresion"]["rezagos_hac"] == L,
              f"{list(t['regresion']['errores_hac'].values())} vs {list(mod.bse)}")
    q = norm.ppf(0.975)
    C.informe("TCV-SLOPE valor razonable e IC al 95 %", cerca(t["valor_razonable_pb"], raz, 1e-8)
              and np.allclose(t["ic_valor_razonable_pb"], [raz - q * ee, raz + q * ee], atol=1e-8))
    act = Rm[-1] / 100
    yi = lambda x: np.interp(x, pl, Rm[-1]) / 100  # noqa: E731
    ok = True
    for hm in (3, 6):
        h = hm / 12
        fa = ((1 + yi(h + 2)) ** (h + 2) / (1 + yi(h)) ** h) ** (1 / 2) - 1
        fb = ((1 + yi(h + 10)) ** (h + 10) / (1 + yi(h)) ** h) ** (1 / 10) - 1
        ok &= cerca(t["pendiente_forward_pb"][f"{hm}m"], (fb - fa) * 1e4, 1e-8)
    C.informe("TCV-SLOPE pendiente forward a 3 y 6 meses", ok, str(t["pendiente_forward_pb"]))
    dt = 0.25
    fin = yi(dt)
    leg = {}
    for tau in (2, 10):
        y = yi(tau)
        dm = tau / (1 + y)
        leg[tau] = ((y - fin) * dt / dm, -dm * (yi(tau - dt) - y) / dm)
    c_ = (leg[2][0] - leg[10][0]) * 1e4
    rd = (leg[2][1] - leg[10][1]) * 1e4
    cn = t["carry_neutral_dv01_pb"]
    C.informe("TCV-SLOPE carry y rolldown neutrales en DV01 (FIR-CARRY-001 en ambos tramos)",
              cn is not None and cerca(cn["carry_pb"], c_, 1e-9) and cerca(cn["rolldown_pb"], rd, 1e-9), str(cn))

# ====================================================================== TCV-VIXTS-001
fv = pd.date_range("2020-01-02", periods=4 * 252, freq="B")
nv = len(fv)
hs = 18 + 4 * np.sin(np.arange(nv) / 30) + rng.normal(0, 0.5, nv)
hf1 = hs + 1 + rng.normal(0, 1, nv)
hf2 = hf1 + 0.8 + rng.normal(0, 1, nv)
hr = rng.normal(-0.3, 3, nv)
v = {"spot": 16.0, "futuros": {"dias": [18, 46, 74], "precios": [17.2, 18.4, 19.1]},
     "historia": {"fechas": [str(x.date()) for x in fv], "spot": hs.tolist(), "f1": hf1.tolist(), "f2": hf2.tolist(),
                  "rent_larga": hr.tolist(), "fuente_rentabilidades": "QA"}}
r, lim, err = llamar("TCV-VIXTS-001", v)
if err:
    C.informe("TCV-VIXTS se sirve con datos válidos", False, err)
else:
    w = (46 - 30) / (46 - 18)
    fcm = w * 17.2 + (1 - w) * 18.4
    C.informe("TCV-VIXTS estado contango y roll (F₁ − spot)/días", r["estado"] == "contango" and cerca(r["roll_puntos_dia"], 1.2 / 18, 1e-14))
    C.informe("TCV-VIXTS futuro a 30 días interpolado y rentabilidad esperada larga (spot/F30 − 1)",
              cerca(r["futuro_vencimiento_constante"], fcm, 1e-12) and cerca(r["rentabilidad_esperada_larga_pct"], (16 / fcm - 1) * 100, 1e-12))
    sel = np.array([(fv[-1] - x).days / 365.25 <= 5 for x in fv])
    ph = (hf2 - hf1)[sel]
    C.informe("TCV-VIXTS percentil de la pendiente y frecuencia de contango",
              cerca(r["percentil_pendiente"], float(np.mean(ph <= 1.2)), 1e-12)
              and cerca(r["frecuencia_contango"], float(np.mean(((hf2 > hf1) & (hf1 > hs))[sel])), 1e-12))
    corta = -hr
    qq = np.quantile(corta, 0.025)
    C.informe("TCV-VIXTS ES al 97,5 % de la exposición corta (método histórico)",
              cerca(r["es_corta_pct"], -corta[corta <= qq].mean(), 1e-12), f"{r['es_corta_pct']} vs {-corta[corta <= qq].mean()}")

sys.exit(C.resumen())
