"""QA r01 de T-119 · oráculos independientes (1 de 2): FIR-CRED, FX-BEER, CMD-REAL, REI-LEV, CHR-ONCHAIN y CHR-TOKEN.

Datos propios no degenerados (numpy, semilla fija) servidos por `Motor.servir`; lo esperado se calcula aquí por otra vía:
 - FIR-CRED-001: sistema de Merton con `scipy.optimize.fsolve` sobre (V, σ_V) (no las dos raíces anidadas del código);
   diferencial por la identidad B = V − E (valor de la deuda), no por N(d₂) + …; PD real con μ; Bharath-Shumway; T ≠ 1.
 - FX-BEER-001: DOLS con `statsmodels` OLS + HAC (Bartlett, sin corrección); Johansen con `VECM(deterministic="ci")`;
   vida media con OLS de statsmodels; IC del desalineamiento a mano.
 - CMD-REAL-001: `scipy.stats.theilslopes`, percentil y percentil ponderado de la curva de costes a mano.
 - REI-LEV-001, CHR-TOKEN-001: bucles a mano. CHR-ONCHAIN-001: `pandas.rolling`.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.api as sm  # noqa: E402
from scipy import optimize, stats  # noqa: E402
from statsmodels.tsa.vector_ar.vecm import VECM  # noqa: E402

K = C.Contador("r01_02 oráculos A")
m = C.motor()
rng = np.random.default_rng(20261114)
N = stats.norm.cdf


def ok(r):
    if r["estado"] == "RECHAZADO":
        print("   RECHAZADO:", r["detalle"][:300])
        return False
    return True


# ------------------------------------------------------------------ FIR-CRED-001
print("FIR-CRED-001")
n = 17
E = rng.uniform(20, 900, n)
sE = rng.uniform(0.15, 0.9, n)
corto = rng.uniform(0, 300, n)
largo = rng.uniform(5, 800, n)
mu = rng.uniform(-0.05, 0.15, n)
r_, T = 0.037, 1.0


def valores_fc(T_=None):
    return {"fecha": "2026-06-30", "segmento": {"nombre": "seg", "financiero": False, "cobertura": 0.7}, "r": r_,
            "diferencial_indice_pb": 233.0,
            "componentes": [{"id": f"X{i}", "capitalizacion": float(E[i]), "volatilidad_acciones": float(sE[i]),
                             "deuda_corto": float(corto[i]), "deuda_largo": float(largo[i]), "mu_historico": float(mu[i])}
                            for i in range(n)], "pd_historica_rating_pct": 1.1}


def merton_fsolve(E_, sE_, D, r, T_):
    def sistema(x):
        V, s = math.exp(x[0]), math.exp(x[1])
        d1 = (math.log(V / D) + (r + s * s / 2) * T_) / (s * math.sqrt(T_))
        d2 = d1 - s * math.sqrt(T_)
        return [(V * N(d1) - D * math.exp(-r * T_) * N(d2)) / E_ - 1, N(d1) * s * V / (E_ * sE_) - 1]
    sol, _, ier, _ = optimize.fsolve(sistema, [math.log(E_ + D), math.log(sE_ * E_ / (E_ + D))], full_output=True, xtol=1e-14)
    assert max(abs(x) for x in sistema(sol)) < 1e-10, (ier, sistema(sol))
    return math.exp(sol[0]), math.exp(sol[1])


def esperado_fc(T_, metodo="iterativo"):
    dd, pdn, ddr, pdr, dif = [], [], [], [], []
    for i in range(n):
        D = corto[i] + 0.5 * largo[i]
        if metodo == "iterativo":
            V, s = merton_fsolve(E[i], sE[i], D, r_, T_)
        else:
            V = E[i] + D
            s = E[i] / V * sE[i] + D / V * (0.05 + 0.25 * sE[i])
        d2 = (math.log(V / D) + (r_ - s * s / 2) * T_) / (s * math.sqrt(T_))
        d1 = d2 + s * math.sqrt(T_)
        dr = (math.log(V / D) + (mu[i] - s * s / 2) * T_) / (s * math.sqrt(T_))
        dd.append(d2), pdn.append(N(-d2)), ddr.append(dr), pdr.append(N(-dr))
        # valor de la deuda = V − opción de compra (con el V y σ_V dados); en el iterativo, B = V − E
        call = V * N(d1) - D * math.exp(-r_ * T_) * N(d2)
        B = V - call
        dif.append(-math.log(B / (D * math.exp(-r_ * T_))) / T_)
    w = (corto + largo) / (corto + largo).sum()
    return {k: np.array(x) for k, x in (("dd", dd), ("pd", pdn), ("ddr", ddr), ("pdr", pdr), ("dif", dif))}, w


for T_, metodo in ((1, "iterativo"), (3.5, "iterativo"), (1, "ingenuo"), (0.25, "iterativo")):
    r = C.servir(m, "FIR-CRED-001", valores_fc(), {"T": T_, "metodo": metodo})
    if not K.comprobar(f"servido T={T_} {metodo}", ok(r)):
        continue
    x, e, w = r["resultado"], *esperado_fc(T_, metodo)
    et = f"T={T_} {metodo}"
    for bloque, kd, kp in (("neutral_al_riesgo", "dd", "pd"), ("real", "ddr", "pdr")):
        b = x[bloque]
        K.cerca(f"{et} {bloque} DD mediana", b["dd"]["mediana"], np.median(e[kd]), 1e-7)
        K.cerca(f"{et} {bloque} DD q25", b["dd"]["q25"], np.quantile(e[kd], 0.25), 1e-7)
        K.cerca(f"{et} {bloque} DD q75", b["dd"]["q75"], np.quantile(e[kd], 0.75), 1e-7)
        K.cerca(f"{et} {bloque} DD media ponderada por deuda", b["dd"]["media_ponderada_deuda"], w @ e[kd], 1e-7)
        K.cerca(f"{et} {bloque} PD mediana %", b["pd_pct"]["mediana"], np.median(e[kp]) * 100, 1e-7)
        K.cerca(f"{et} {bloque} PD q75 %", b["pd_pct"]["q75"], np.quantile(e[kp], 0.75) * 100, 1e-7)
        K.cerca(f"{et} {bloque} PD media ponderada %", b["pd_pct"]["media_ponderada_deuda"], w @ e[kp] * 100, 1e-7)
        K.cerca(f"{et} {bloque} proporción DD<2 %", b["proporcion_dd_menor_2_pct"], np.mean(e[kd] < 2) * 100, 1e-9)
    K.cerca(f"{et} diferencial implícito (pb) por B = V − E", x["diferencial_implicito_pb"], w @ e["dif"] * 1e4, 1e-7)
    K.cerca(f"{et} brecha observado − implícito", x["brecha_observado_implicito_pb"], 233.0 - w @ e["dif"] * 1e4, 1e-6)
    K.cerca(f"{et} ref. ingenua: PD real ponderada − histórica", x["referencia_ingenua"]["diferencia_pd_pct"],
            w @ e["pdr"] * 100 - 1.1, 1e-6)
r = C.servir(m, "FIR-CRED-001", valores_fc(), {"mu": "r"})
x = r["resultado"]
K.comprobar("mu = r: sin bloque real y la referencia usa la PD neutral", x["real"] is None and abs(
    x["referencia_ingenua"]["diferencia_pd_pct"] - (x["neutral_al_riesgo"]["pd_pct"]["media_ponderada_deuda"] - 1.1)) < 1e-9)

# ------------------------------------------------------------------ FX-BEER-001
print("FX-BEER-001")
nq = 104
fechas = pd.date_range("1998-03-31", periods=nq, freq="QE")
Xf = np.cumsum(rng.normal(0, [0.02, 0.015, 0.03, 0.01], (nq, 4)), axis=0)
u = np.zeros(nq)
for t in range(1, nq):
    u[t] = 0.75 * u[t - 1] + rng.normal(0, 0.02)
dXf = np.diff(Xf, axis=0, prepend=Xf[:1])
q = 4.5 + Xf @ np.array([0.6, -0.4, 0.25, 1.5]) + u + 0.3 * dXf[:, 0]      # endogeneidad a corto plazo
nombres = ["terminos_intercambio", "diferencial_productividad", "piin_pib", "diferencial_tipos_reales"]
vb = {"vintage": "2024-03-01", "serie": [{"fecha": str(f.date()), "reer": float(math.exp(q[i])),
                                           **{nb: float(Xf[i, j]) for j, nb in enumerate(nombres)}}
                                          for i, f in enumerate(fechas)]}
for k in (2, 1, 4):
    r = C.servir(m, "FX-BEER-001", vb, {"retardos": k})
    if not K.comprobar(f"DOLS k={k} servido", ok(r)):
        continue
    x = r["resultado"]
    df = pd.DataFrame(Xf, columns=nombres)
    reg = {"const": 1.0, **{nb: df[nb] for nb in nombres}}
    for j in range(-k, k + 1):
        for nb in nombres:
            reg[f"d_{nb}_{j}"] = df[nb].diff().shift(-j)          # Δx_{t+j}
    Z = pd.DataFrame(reg).dropna()
    yy = pd.Series(q)[Z.index]
    L = math.floor(4 * (len(Z) / 100) ** (2 / 9))
    fit = sm.OLS(yy, Z).fit(cov_type="HAC", cov_kwds={"maxlags": L, "use_correction": False})
    K.comprobar(f"k={k} n de estimación {x['n_estimacion']} = {len(Z)}", x["n_estimacion"] == len(Z))
    for nb in nombres:
        K.cerca(f"k={k} β {nb}", x["coeficientes"][nb]["beta"], fit.params[nb], 1e-7)
        K.cerca(f"k={k} ee HAC {nb}", x["coeficientes"][nb]["ee"], fit.bse[nb], 1e-6)
        K.cerca(f"k={k} t {nb}", x["coeficientes"][nb]["t"], fit.tvalues[nb], 1e-6)
    b = fit.params[nombres].to_numpy()
    sc = q - Xf @ b
    z = sc - sc.mean()
    K.cerca(f"k={k} constante", x["constante"], sc.mean(), 1e-8)
    K.cerca(f"k={k} desalineamiento %", x["desalineamiento_pct"], (math.exp(z[-1]) - 1) * 100, 1e-7)
    K.cerca(f"k={k} equilibrio", x["equilibrio"], math.exp(q[-1] - z[-1]), 1e-8)
    d = Xf[-1] - Xf.mean(axis=0)
    V = fit.cov_params().loc[nombres, nombres].to_numpy()
    ee = math.sqrt(d @ V @ d)
    zc = stats.norm.ppf(1 - (1 - x["nivel_ic"]) / 2)
    K.cerca(f"k={k} IC inferior", x["ic_desalineamiento_pct"][0], (math.exp(z[-1] - zc * ee) - 1) * 100, 1e-6)
    K.cerca(f"k={k} IC superior", x["ic_desalineamiento_pct"][1], (math.exp(z[-1] + zc * ee) - 1) * 100, 1e-6)
    ar = sm.OLS(np.diff(z), sm.add_constant(z[:-1])).fit()
    rho = 1 + ar.params[1]
    K.cerca(f"k={k} velocidad de corrección", x["velocidad_correccion_trimestral"], ar.params[1], 1e-7)
    K.cerca(f"k={k} vida media (años)", x["vida_media_anios"], math.log(0.5) / math.log(rho) / 4, 1e-7)
    K.cerca(f"k={k} PPA %", x["segunda_via_ppa"]["desalineamiento_pct"], (math.exp(q[-1] - q.mean()) - 1) * 100, 1e-8)
    K.comprobar(f"k={k} residuo de media nula", abs(x["verificacion"]["media_desalineamiento"]) < 1e-12
                and abs(x["verificacion"]["media_residuo_regresion"]) < 1e-10)
print(f"   nivel_ic usado: {x['nivel_ic']}; cointegración: {x['cointegracion']}")
from statsmodels.tsa.stattools import adfuller  # noqa: E402
tau = adfuller(z, maxlag=math.floor(4 * (nq / 100) ** (2 / 9)), regression="n", autolag="AIC")[0]
K.cerca("ADF de los residuos (statsmodels, sin constante, AIC)", x["cointegracion"]["estadistico"], tau, 1e-6)
for k in (2, 1):
    r = C.servir(m, "FX-BEER-001", vb, {"metodo": "Johansen", "retardos": k})
    if not K.comprobar(f"Johansen k={k} servido", ok(r)):
        continue
    x = r["resultado"]
    Y = np.column_stack([q, Xf])
    vf = VECM(Y, k_ar_diff=k, coint_rank=1, deterministic="ci").fit()
    b = -vf.beta[1:5, 0] / vf.beta[0, 0]
    for j, nb in enumerate(nombres):
        K.cerca(f"Johansen k={k} β {nb} (VECM ci)", x["coeficientes"][nb]["beta"], b[j], 1e-6)
    sc = q - Xf @ b
    K.cerca(f"Johansen k={k} desalineamiento %", x["desalineamiento_pct"], (math.exp(sc[-1] - sc.mean()) - 1) * 100, 1e-6)
    from statsmodels.tsa.vector_ar.vecm import coint_johansen  # noqa: E402
    print(f"   traza servida {x['cointegracion']['estadistico']:.4f}, crítico {x['cointegracion']['critico']} (MHM 1999, caso 2, "
          f"5 variables, 5 %: 76,97); IC: {x['ic_desalineamiento_pct']}")
    K.comprobar(f"Johansen k={k}: crítico de la traza = 76,97 (caso 2, p − r = 5)", abs(x["cointegracion"]["critico"] - 76.97) < 0.01)
    K.comprobar(f"Johansen k={k}: sin IC, declarado en limitaciones", x["ic_desalineamiento_pct"] is None
                and any("IC" in s for s in r["limitaciones"]))

# ------------------------------------------------------------------ CMD-REAL-001
print("CMD-REAL-001")
nm = 400
fm = pd.date_range("1992-01-31", periods=nm, freq="ME")
ipc = 100 * np.exp(np.cumsum(rng.normal(0.002, 0.003, nm)))
precio = 40 * np.exp(np.cumsum(rng.normal(0.003, 0.06, nm)))
tramos = [{"coste": float(c), "produccion": float(p_)} for c, p_ in zip(rng.uniform(10, 90, 37), rng.uniform(1, 50, 37))]
vc = {"moneda": "USD", "ipc_moneda": "USD", "serie": [{"fecha": str(f.date()), "precio": float(precio[i]), "ipc": float(ipc[i])}
                                                       for i, f in enumerate(fm)],
      "curva_costes": {"fecha": "2019-05-17", "fuente": "x", "tramos": tramos}}
for pc in (0.9, 0.5, 1.0, 0.013):
    r = C.servir(m, "CMD-REAL-001", vc, {"percentil_coste": pc})
    if not K.comprobar(f"percentil_coste={pc} servido", ok(r)):
        continue
    x = r["resultado"]
    real = precio * ipc[-1] / ipc
    K.cerca("precio real actual = nominal", x["precio_real_actual"], precio[-1], 1e-12)
    K.cerca("percentil", x["percentil"], sum(1 for v_ in real if v_ <= real[-1]) / nm, 1e-12)
    K.cerca("media real (RI-MH)", x["media_real"], real.mean(), 1e-12)
    K.cerca("z", x["z"], (real[-1] - real.mean()) / real.std(ddof=1), 1e-10)
    sl = stats.theilslopes(np.log(real), np.arange(nm), 0.95)
    K.cerca("tendencia real % anual (Theil-Sen de scipy)", x["tendencia_real_pct_anual"], (math.exp(12 * sl[0]) - 1) * 100, 1e-9)
    orden = sorted(tramos, key=lambda t: t["coste"])
    tot, ac, cm = sum(t["produccion"] for t in orden), 0.0, None
    for t in orden:
        ac += t["produccion"]
        if ac >= pc * tot * (1 - 1e-12):
            cm = t["coste"]
            break
    i_cc = list(fm.to_period("M")).index(pd.Period("2019-05", "M"))
    K.cerca(f"pc={pc} coste marginal nominal", x["coste_marginal"]["coste_nominal"], cm, 1e-12)
    K.cerca(f"pc={pc} precio/coste (coste a moneda constante)", x["precio_sobre_coste"], precio[-1] / (cm * ipc[-1] / ipc[i_cc]), 1e-11)
print(f"   IC de la tendencia servido {x['ic_tendencia_pct_anual']}; scipy (otra convención de IC) "
      f"{[(math.exp(12 * s) - 1) * 100 for s in sl[2:]]}; p {x['tendencia_p_valor']}")
tau_k = stats.kendalltau(np.arange(nm), np.log(real))
print(f"   p de Kendall (scipy, exacto/asintótico con empates): {tau_k.pvalue}")

# ------------------------------------------------------------------ REI-LEV-001
print("REI-LEV-001")
nc = 9
comps = []
for i in range(nc):
    imp = rng.uniform(10, 200, 5)
    fechas_v = ["2026-07-01", "2027-06-30", "2028-06-30", "2028-07-01", "2031-01-15"]
    comps.append({"id": f"R{i}", "gav": float(rng.uniform(800, 3000)), "deuda": float(imp.sum()), "caja": float(rng.uniform(0, 80)),
                  "ebitda": float(rng.uniform(30, 150)), "gastos_financieros": float(rng.uniform(5, 40)),
                  "ffo": float(rng.uniform(-5, 90)),
                  "vencimientos": [{"fecha": f, "importe": float(x_), "coste": float(rng.uniform(0.005, 0.07))}
                                   for f, x_ in zip(fechas_v, imp)],
                  **({"covenants": {"ltv_max": float(rng.uniform(0.2, 0.65)), "icr_min": float(rng.uniform(1.5, 6))}} if i % 3 else {})})
vr = {"fecha": "2026-06-30", "moneda": "EUR", "coste_refinanciacion": {"swap": 0.029, "margen": 0.021}, "componentes": comps}
for par in ({}, {"margen": 0.035, "caidas_valor": [-0.3, -0.05, -0.15]}):
    r = C.servir(m, "REI-LEV-001", vr, par)
    if not K.comprobar(f"servido {par}", ok(r)):
        continue
    x = r["resultado"]
    marg = par.get("margen", 0.021)
    caidas = par.get("caidas_valor", [-0.1, -0.2])
    G = sum(c["gav"] for c in comps)
    Dn = sum(c["deuda"] - c["caja"] for c in comps)
    Dt = sum(c["deuda"] for c in comps)
    hz = pd.Timestamp("2028-06-30")
    v24 = sum(v_["importe"] for c in comps for v_ in c["vencimientos"] if pd.Timestamp(v_["fecha"]) <= hz)
    extra = sum(v_["importe"] * (0.029 + marg - v_["coste"]) for c in comps for v_ in c["vencimientos"] if pd.Timestamp(v_["fecha"]) <= hz)
    K.cerca("LTV %", x["ltv_pct"], Dn / G * 100, 1e-12)
    K.cerca("ICR", x["icr_veces"], sum(c["ebitda"] for c in comps) / sum(c["gastos_financieros"] for c in comps), 1e-12)
    K.cerca("deuda neta/EBITDA", x["deuda_neta_sobre_ebitda_veces"], Dn / sum(c["ebitda"] for c in comps), 1e-12)
    K.cerca("vencimientos 24 m % (3 de 5 tramos: el del 2028-06-30 entra, el del 2028-07-01 no)", x["vencimientos_24m_pct"], v24 / Dt * 100, 1e-12)
    K.cerca("impacto en FFO %", x["impacto_ffo_pct"], -extra / sum(c["ffo"] for c in comps) * 100, 1e-11)
    for c_ in caidas:
        K.cerca(f"LTV estresado {c_}", x["ltv_estresado_pct"][f"{c_:g}"], Dn / (G * (1 + c_)) * 100, 1e-12)
    ltvs = [(c["deuda"] - c["caja"]) / c["gav"] * 100 for c in comps]
    K.cerca("dispersión LTV: mediana", x["dispersion"]["ltv_pct"]["mediana"], np.median(ltvs), 1e-12)
    K.cerca("dispersión LTV: q25", x["dispersion"]["ltv_pct"]["q25"], np.percentile(ltvs, 25), 1e-12)
    cc = [c for c in comps if "covenants" in c]
    hl = [c["covenants"]["ltv_max"] * 100 - (c["deuda"] - c["caja"]) / c["gav"] * 100 for c in cc]
    hi = [c["ebitda"] / c["gastos_financieros"] - c["covenants"]["icr_min"] for c in cc]
    K.cerca("holgura LTV (pp) mediana", x["covenants"]["holgura_ltv_pp"]["mediana"], np.median(hl), 1e-10)
    K.cerca("holgura ICR mediana", x["covenants"]["holgura_icr_veces"]["mediana"], np.median(hi), 1e-10)
    K.cerca("% en incumplimiento", x["covenants"]["en_incumplimiento_pct"], np.mean([a < 0 or b < 0 for a, b in zip(hl, hi)]) * 100, 1e-12)
    for c_ in caidas:
        e_ = np.mean([(c["deuda"] - c["caja"]) / (c["gav"] * (1 + c_)) > c["covenants"]["ltv_max"] for c in cc]) * 100
        K.cerca(f"% que incumple el LTV con caída {c_}", x["covenants"]["en_incumplimiento_ltv_estresado_pct"][f"{c_:g}"], e_, 1e-12)
    rompe = [((c["deuda"] - c["caja"]) / c["gav"] / c["covenants"]["ltv_max"] - 1) * 100 for c in cc]
    K.cerca("caída de valor que agota el LTV (mediana)", x["covenants"]["caida_valor_que_agota_ltv_pct"]["mediana"], np.median(rompe), 1e-10)

# ------------------------------------------------------------------ CHR-ONCHAIN-001
print("CHR-ONCHAIN-001")
nd = 1700
fd = pd.date_range("2021-01-01", periods=nd, freq="D")
cm_ = 5e11 * np.exp(np.cumsum(rng.normal(0.0005, 0.03, nd)))
cr_ = pd.Series(cm_).ewm(span=300).mean().to_numpy() * rng.uniform(0.9, 1.1, nd)
vol = cm_ / rng.uniform(20, 120, nd)
vo = {"fuente": {"nombre": "F", "metodologia": "m", "filtros": "f"},
      "serie": [{"fecha": str(f.date()), "capitalizacion": float(cm_[i]), "capitalizacion_realizada": float(cr_[i]),
                 "volumen_ajustado": float(vol[i])} for i, f in enumerate(fd)]}
for w in (90, 1, 365, 7):
    r = C.servir(m, "CHR-ONCHAIN-001", vo, {"media_nvt": w})
    if not K.comprobar(f"media_nvt={w} servido", ok(r)):
        continue
    x = r["resultado"]
    s = pd.DataFrame({"cm": cm_, "cr": cr_, "vol": vol})
    mv = s.cm / s.cr
    zz = (s.cm - s.cr) / s.cm.std()                       # pandas: ddof = 1
    nvt = s.cm / s.vol
    sen = (s.cm / s.vol.rolling(w).mean()).dropna()
    K.cerca("MVRV", x["mvrv"], mv.iloc[-1], 1e-12)
    K.cerca("MVRV-Z", x["mvrv_z"], zz.iloc[-1], 1e-11)
    K.cerca("NVT", x["nvt"], nvt.iloc[-1], 1e-12)
    K.cerca(f"señal NVT ({w} d)", x["senal_nvt"], sen.iloc[-1], 1e-10)
    for nb, ser in (("mvrv", mv), ("mvrv_z", zz), ("nvt", nvt), ("senal_nvt", sen)):
        K.cerca(f"percentil {nb} (w={w})", x["percentiles"][nb], (ser <= ser.iloc[-1]).mean(), 1e-12)

# ------------------------------------------------------------------ CHR-TOKEN-001
print("CHR-TOKEN-001")
toks = []
for i in range(7):
    circ = float(rng.uniform(1e6, 1e9))
    total = circ * float(rng.uniform(1.2, 3))
    maxima = None if i == 2 else total * float(rng.uniform(1, 2))
    bloqueada = total - circ
    cant = bloqueada * rng.dirichlet(np.ones(6)) * 0.9
    fs_ = ["2026-06-29", "2026-06-30", "2026-07-01", "2026-07-30", "2026-07-31", "2026-09-28"]   # +30 d = 30-jul; +90 d = 28-sep
    toks.append({"id": f"T{i}", "precio": float(rng.uniform(0.01, 300)), "oferta_circulante": circ, "oferta_total": total,
                 "oferta_maxima": maxima, "emision_anual": float(circ * rng.uniform(0, 0.1)), "quema_anual": float(circ * rng.uniform(0, 0.12)),
                 "calendario": {"fuente": "doc", "desbloqueos": [{"fecha": f, "cantidad": float(c)} for f, c in zip(fs_, cant)]},
                 **({"staking_nominal": float(rng.uniform(0, 0.2))} if i % 2 else {}),
                 **({"concentracion_10_mayores": float(rng.uniform(0.1, 0.9))} if i < 5 else {})})
vt = {"fecha": "2026-06-30", "fuente": "agregador", "ambito": "sector", "tokens": toks}
r = C.servir(m, "CHR-TOKEN-001", vt, {"ventanas_desbloqueo": [90, 30, 31, 7]})
if K.comprobar("servido", ok(r)):
    x = r["resultado"]
    CM = sum(t["precio"] * t["oferta_circulante"] for t in toks)
    K.cerca("FDV/CM", x["fdv_sobre_capitalizacion_veces"], sum(t["precio"] * (t["oferta_maxima"] or t["oferta_total"]) for t in toks) / CM, 1e-12)
    K.cerca("inflación neta % = Σ precio·(emisión − quema)/Σ CM", x["inflacion_neta_pct_anual"],
            sum(t["precio"] * (t["emision_anual"] - t["quema_anual"]) for t in toks) / CM * 100, 1e-10)
    f0 = pd.Timestamp("2026-06-30")
    for w in (7, 30, 31, 90):
        e_ = sum(t["precio"] * d_["cantidad"] for t in toks for d_ in t["calendario"]["desbloqueos"]
                 if f0 < pd.Timestamp(d_["fecha"]) <= f0 + pd.Timedelta(days=w)) / CM * 100
        K.cerca(f"desbloqueos a {w} d %", x["desbloqueos_pct"][str(w)], e_, 1e-10)
    st = [(t["precio"] * t["oferta_circulante"], t["staking_nominal"] - (t["emision_anual"] - t["quema_anual"]) / t["oferta_circulante"])
          for t in toks if "staking_nominal" in t]
    K.cerca("rendimiento real de staking %", x["rendimiento_real_staking_pct"], sum(a * b for a, b in st) / sum(a for a, _ in st) * 100, 1e-10)
    K.cerca("cobertura staking %", x["cobertura_staking_pct"], sum(a for a, _ in st) / CM * 100, 1e-12)
    co = [(t["precio"] * t["oferta_circulante"], t["concentracion_10_mayores"]) for t in toks if "concentracion_10_mayores" in t]
    K.cerca("concentración %", x["concentracion_10_mayores_pct"], sum(a * b for a, b in co) / sum(a for a, _ in co) * 100, 1e-10)
    K.comprobar("2 desbloqueos pasados declarados por token (14)", any("14 desbloqueos" in s for s in r["limitaciones"]), str(r["limitaciones"])[:200])
sys.exit(K.fin())
