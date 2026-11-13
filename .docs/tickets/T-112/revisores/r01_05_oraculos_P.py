"""QA r01 de T-112 · oráculos independientes del grupo P (inmobiliario, materias primas, cripto y alternativos).

- ALT-DESMOOTH-001: GLM frente al MA(k) por máxima verosimilitud exacta de statsmodels (ARIMA) normalizado a Σθ = 1;
  Geltner frente a un AR(1) por MCO de statsmodels; beta de Dimson frente a OLS de statsmodels; MDD propio.
- REI-NAV-001: primas, pesos por capitalización, dispersión ponderada y NAV ajustado recalculados con 5 componentes.
- CMD-RETDEC-001: descomposición spot + roll + colateral recalculada desde los índices.
- CHR-FUND-001: financiación anualizada (periodos por año) ponderada por interés abierto y base anualizada.
"""
import copy
import math
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

warnings.simplefilter("ignore")
K = C.Contador("r01_05 oráculos P")
m = C.motor()
from bloque_a.motor import servicio  # noqa: E402

# ============================================================ ALT-DESMOOTH-001
print("ALT-DESMOOTH-001")
import statsmodels.api as sm  # noqa: E402
from statsmodels.tsa.arima.model import ARIMA  # noqa: E402

fechas = [d.date().isoformat() for d in pd.date_range("1996-03-31", periods=120, freq="QE")]
for sem, th_true in ((1, [0.6, 0.3, 0.1]), (2, [0.5, 0.35, 0.15])):
    rng = np.random.default_rng(sem)
    real = 0.02 + 0.06 * rng.standard_normal(122)
    merc = 0.015 + 0.08 * rng.standard_normal(122)
    real = real + 0.5 * (merc - 0.015)
    obs = np.array([sum(th_true[j] * real[t - j] for j in range(3)) for t in range(2, 122)])
    mk = merc[2:]
    val = {"rentabilidades": [{"fecha": f, "r": float(x)} for f, x in zip(fechas, obs)],
           "mercado": [{"fecha": f, "r": float(x)} for f, x in zip(fechas, mk)]}
    r = C.servir(m, "ALT-DESMOOTH-001", val, {"metodo": "GLM", "k": 2})
    if not K.comprobar(f"GLM datos {sem}: servida", r["estado"].startswith("SERVED"), str(r)[:300]):
        continue
    R = r["resultado"]
    x = obs - obs.mean()
    # θ de GLM: MV exacta del MA(2) con θ_j ≥ 0 y Σθ = 1. Oráculo: la log-verosimilitud exacta de statsmodels
    # (ARIMA, filtro de Kalman) maximizada en una rejilla fina del simplex y refinada; el Motor no debe quedar por debajo.
    mod_ = ARIMA(x, order=(0, 0, 2), trend="n")
    from scipy import optimize as _opt

    def ll_theta(t12):
        t0 = 1 - t12[0] - t12[1]
        if t0 <= 0 or min(t12) < 0:
            return -1e18
        psi_ = [t12[0] / t0, t12[1] / t0]
        o_ = _opt.minimize_scalar(lambda ls: -mod_.loglike(np.r_[psi_, math.exp(ls)]), bounds=(-15, 0), method="bounded",
                                  options={"xatol": 1e-10})
        return -o_.fun

    rejilla = [(a_, b_) for a_ in np.linspace(0, 0.95, 39) for b_ in np.linspace(0, 0.95, 39) if a_ + b_ < 0.97]
    t_best = max(rejilla, key=ll_theta)
    ref_ = _opt.minimize(lambda t: -ll_theta(t), t_best, method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-11})
    cand = [ref_.x, np.array(t_best)] + [np.array(c_) for c_ in ((ref_.x[0], 0.0), (0.0, ref_.x[1]))]
    ll_or = max(ll_theta(np.clip(c_, 0, 1)) for c_ in cand)
    ll_mo = ll_theta(np.array(R["theta"][1:]))
    K.comprobar(f"  [{sem}] θ de GLM: el máximo propio con restricciones no mejora al Motor (1e-6)", ll_or <= ll_mo + 1e-6,
                f"oráculo {ll_or} vs Motor {ll_mo}; θ Motor {R['theta']}")
    th = np.array(R["theta"])
    rr = obs.copy()
    for t in range(2, len(obs)):
        rr[t] = (obs[t] - th[1] * rr[t - 1] - th[2] * rr[t - 2]) / th[0]
    K.comprobar(f"  [{sem}] serie desuavizada = filtro propio", np.allclose([z["r"] for z in R["serie_desuavizada"]], rr[2:], atol=1e-12))
    K.comprobar(f"  [{sem}] volatilidad anual = σ·√4 (ddof 1)", abs(R["volatilidad_desuavizada_pct"] - np.std(rr[2:], ddof=1) * 200) < 1e-9)
    w = np.r_[1, np.cumprod(1 + rr[2:])]
    K.comprobar(f"  [{sem}] MDD desuavizado", abs(R["mdd_desuavizado_pct"] - 100 * np.max(1 - w / np.maximum.accumulate(w))) < 1e-9)
    y = rr[2:][2:]
    X = sm.add_constant(np.column_stack([mk[2:][2:], mk[2:][1:-1], mk[2:][:-2]]))
    bd = sm.OLS(y, X).fit().params[1:].sum()
    K.comprobar(f"  [{sem}] beta de Dimson (L = k = 2) = OLS de statsmodels", abs(R["beta_dimson"]["desuavizada"] - bd) < 1e-9,
                f"{R['beta_dimson']} vs {bd}")
    r = C.servir(m, "ALT-DESMOOTH-001", val)
    if K.comprobar(f"Geltner datos {sem}: servida", r["estado"].startswith("SERVED"), str(r)[:300]):
        R = r["resultado"]
        phi = sm.OLS(obs[1:], sm.add_constant(obs[:-1])).fit().params[1]
        K.comprobar(f"  [{sem}] φ = AR(1) MCO con constante (statsmodels)", abs(R["phi"] - phi) < 1e-12, f"{R['phi']} vs {phi}")
        g = (obs[1:] - phi * obs[:-1]) / (1 - phi)
        K.comprobar(f"  [{sem}] serie de Geltner", np.allclose([z["r"] for z in R["serie_desuavizada"]], g, atol=1e-12))

# ============================================================ REI-NAV-001
print("REI-NAV-001")
rng = np.random.default_rng(3)
comps = []
for i in range(5):
    acc = float(rng.uniform(5e7, 3e8))
    gav = float(rng.uniform(1e9, 6e9))
    dn, op = gav * float(rng.uniform(0.2, 0.45)), gav * float(rng.uniform(0.02, 0.08))
    nav = gav - dn - op
    comps.append({"id": f"C{i}", "fecha_precio": "2026-09-30", "precio": float(nav / acc * rng.uniform(0.7, 1.2)), "acciones": acc,
                  "nav_por_accion": nav / acc, "fecha_nav": "2026-06-30", "variante_nav": "EPRA NTA", "gav": gav, "deuda_neta": dn,
                  "otros_pasivos": op, "cap_rate_tasacion": float(rng.uniform(0.04, 0.06))})
hist = servicio.CASOS_CONTROL["REI-NAV-001"][2]["datos"][0]["valores"]["historia_prima"]
r = C.servir(m, "REI-NAV-001", {"componentes": comps, "historia_prima": hist}, {"cap_objetivo": 0.0525})
if K.comprobar("REI-NAV 5 componentes: servida", r["estado"].startswith("SERVED"), str(r)[:300]):
    R = r["resultado"]
    cap = np.array([c["precio"] * c["acciones"] for c in comps])
    pr = np.array([c["precio"] / c["nav_por_accion"] - 1 for c in comps]) * 100
    w = cap / cap.sum()
    agg = float(w @ pr)
    disp = math.sqrt(float(w @ (pr - agg) ** 2))
    K.comprobar("  prima agregada ponderada por capitalización", abs(R["prima_agregada_pct"] - agg) < 1e-10, f"{R['prima_agregada_pct']} vs {agg}")
    K.comprobar("  dispersión ponderada", abs(R["dispersion_pct"] - disp) < 1e-10, f"{R['dispersion_pct']} vs {disp}")
    adj = sum(c["gav"] * c["cap_rate_tasacion"] / 0.0525 - c["deuda_neta"] - c["otros_pasivos"] for c in comps)
    tot = sum(c["nav_por_accion"] * c["acciones"] for c in comps)
    K.comprobar("  NAV ajustado agregado y variación", abs(R["nav_ajustado"]["nav_ajustado_total"] / adj - 1) < 1e-12
                and abs(R["nav_ajustado"]["variacion_pct"] - 100 * (adj / tot - 1)) < 1e-9)

# ============================================================ CMD-RETDEC-001
print("CMD-RETDEC-001")
caso = copy.deepcopy(servicio.CASOS_CONTROL["CMD-RETDEC-001"][0]["datos"][0]["valores"])
ix = caso["indices"]
rng = np.random.default_rng(4)
n = 37
ix["fechas"] = [d.date().isoformat() for d in pd.date_range("2022-01-31", periods=n, freq="ME")]
sp = 100 * np.cumprod(np.r_[1, 1 + 0.03 * rng.standard_normal(n - 1)])
ex = 250 * np.cumprod(np.r_[1, (sp[1:] / sp[:-1]) - 0.004 + 0.002 * rng.standard_normal(n - 1)])
col = 0.02 + 0.01 * rng.uniform(size=n)
tot = 400 * np.cumprod(np.r_[1, (ex[1:] / ex[:-1]) + col[:-1] / 12])
ix.update({"spot": sp.tolist(), "exceso": ex.tolist(), "total": tot.tolist()})
caso["tipo_colateral"] = col.tolist()
r = C.servir(m, "CMD-RETDEC-001", caso)
if K.comprobar("CMD-RETDEC 36 meses: servida", r["estado"].startswith("SERVED"), str(r)[:300]):
    R = r["resultado"]
    rs, re_, rt = sp[1:] / sp[:-1] - 1, ex[1:] / ex[:-1] - 1, tot[1:] / tot[:-1] - 1
    a = R["acumulados"]
    K.comprobar("  spot, roll y colateral por periodo sumados", np.allclose([a["spot"], a["roll"], a["colateral"], a["total"]],
                [rs.sum(), (re_ - rs).sum(), (rt - re_).sum(), rt.sum()], atol=1e-12), str(a))
    K.comprobar("  % anual = acumulado / años", abs(R["total_pct_anual"] - 100 * rt.sum() / 3) < 1e-9, str(R["total_pct_anual"]))
    K.comprobar("  total compuesto", abs(R["total_compuesto_pct_anual"] - 100 * ((tot[-1] / tot[0]) ** (1 / 3) - 1)) < 1e-9,
                str(R["total_compuesto_pct_anual"]))

# ============================================================ CHR-FUND-001
print("CHR-FUND-001")
c = copy.deepcopy(servicio.CASOS_CONTROL["CHR-FUND-001"][1]["datos"][0]["valores"])
r = C.servir(m, "CHR-FUND-001", c)
if K.comprobar("CHR-FUND: servida", r["estado"].startswith("SERVED"), str(r)[:300]):
    R = r["resultado"]
    tasas, oi = {}, {}
    for nom, pl in c["plataformas"].items():
        u = pl["historia"][-1]
        tasas[nom] = u["tasa"] * (24 / pl["periodo_horas"]) * 365 * 100 if "tasa" in u else None
        oi[nom] = u.get("interes_abierto")
    if all(v is not None for v in tasas.values()) and all(v is not None for v in oi.values()):
        w = np.array([oi[k] for k in tasas]) / sum(oi.values())
        agg = float(w @ np.array(list(tasas.values())))
        K.comprobar("  financiación por plataforma = tasa × (24/h) × 365", all(abs(R["financiacion_por_plataforma_pct_anual"][k] - v) < 1e-9 for k, v in tasas.items()),
                    f"{R['financiacion_por_plataforma_pct_anual']} vs {tasas}")
        K.comprobar("  ponderada por interés abierto", abs(R["financiacion_pct_anual"] - agg) < 1e-9, f"{R['financiacion_pct_anual']} vs {agg}")
    else:
        print("   (formato de la historia distinto del supuesto:", list(c["plataformas"]["P1"]["historia"][-1]), ")")
    fu, spt = c["futuro"][-1], c["spot"][-1]
    if isinstance(fu, dict) and isinstance(spt, dict):
        print("   futuro:", {k: fu[k] for k in fu if k != "precio"} | {"precio": fu.get("precio")}, "spot:", spt)
        base = (fu["precio"] / spt["precio"] - 1) * 365 / R["dias_vencimiento"] * 100
        K.comprobar("  base = (F/S − 1)·365/días", abs(R["base_pct_anual"] - base) < 1e-9, f"{R['base_pct_anual']} vs {base}")
sys.exit(K.fin())
