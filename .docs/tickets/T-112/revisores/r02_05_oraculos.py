"""QA r02 de T-112 · oráculos independientes nuevos (los de la r01 no se repiten), con datos no degenerados propios.

Cada cifra esperada se calcula aquí por otra vía (integración numérica, scipy, statsmodels, fuerza bruta o la fórmula de
la ficha del Catálogo escrita a mano), sin llamar al código de la ficha. Por Motor.servir.
 S: FX-BRK-001 (ruptura por fuerza bruta de la SSR).
 R: DEC-VOI-001 (EVPI y EVSI por cuadratura), RISK-VAR-001 (normal, Cornish-Fisher e histórico a mano), SIM-MC-001 (paseo
    aleatorio frente a la solución lognormal), ML-CAL-001 (métricas a mano).
 V: ACC-ERP-001 (r implícita con g₅ ≠ g_L por brentq), ACC-FACT-001 (OLS con Newey-West de statsmodels), FX-PPA-001
    (sentido económico de la senda), FIR-SPREAD-001.
 P: REI-CAP-001, CMD-INV-001, CHR-FLOW-001, REI-FFO-001.
Uso: .venv/bin/python -I r02_05_oraculos.py
"""
import copy
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(["x"])
import numpy as np  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402
from scipy import integrate, optimize, stats  # noqa: E402

K = C.Contador("r02_05 oráculos")
m = C.motor()


def servir(f, i=0, cambio=None, **par):
    c = servicio.CASOS_CONTROL[f][i]
    d = copy.deepcopy(c.get("datos") or [])
    p = dict(c.get("parametros") or {})
    p.update(par)
    if cambio:
        cambio(d[0]["valores"])
    r = m.servir({"operacion": f, "datos": d, "parametros": p}, "AG-18")
    if r["estado"] == "RECHAZADO":
        print("   RECHAZADO", f, r["detalle"][:200])
        return None
    return r["resultado"]


def cerca(a, b, tol=1e-6):
    return a is not None and b is not None and abs(a - b) <= tol * max(1.0, abs(b))


def alguna(a, candidatos, tol=1e-6):
    """Convenciones que la ficha no fija (ddof, definición del percentil): vale cualquiera de las candidatas; se dice cuál."""
    for nombre, b in candidatos.items():
        if cerca(a, b, tol):
            return nombre
    return None


# ================================================================ R · DEC-VOI-001
print("DEC-VOI-001")
for lo, hi, sigma in ((52.0, 66.0, 3.0), (55.0, 63.0, 1.5), (40.0, 75.0, 8.0)):
    u = 60.0

    def dv(v, lo=lo, hi=hi, sigma=sigma):
        v["rango_plausible"]["inferior"], v["rango_plausible"]["superior"] = lo, hi
        v["verosimilitud"] = {"desviacion": sigma}
    r = servir("DEC-VOI-001", 0, dv)
    d = next(x for x in r["decisiones"] if x["umbral"] == u)
    media = (lo + hi) / 2
    evpi = integrate.quad(lambda s: max(s - u, 0) / (hi - lo), lo, hi, points=[u])[0] - max(media - u, 0)

    def post(x):
        a, b = (lo - x) / sigma, (hi - x) / sigma
        return stats.truncnorm.mean(a, b, loc=x, scale=sigma)

    def fx(x):
        return (stats.norm.cdf((hi - x) / sigma) - stats.norm.cdf((lo - x) / sigma)) / (hi - lo)
    xs = np.linspace(lo - 10 * sigma, hi + 10 * sigma, 200001)
    pm = np.array([post(x) for x in xs[::20]])
    evsi = float(np.trapezoid(np.maximum(pm - u, 0) * np.array([fx(x) for x in xs[::20]]), xs[::20])) - max(media - u, 0)
    K.comprobar(f"EVPI uniforme [{lo}, {hi}] por cuadratura", cerca(d["evpi"], evpi, 1e-8), f"{d['evpi']} ≠ {evpi}")
    K.comprobar(f"EVSI con σ = {sigma} por cuadratura de la media a posteriori", cerca(d["evsi"], evsi, 1e-4), f"{d['evsi']} ≠ {evsi}")
    K.comprobar("  EVPI ≥ EVSI ≥ 0", d["evpi"] >= d["evsi"] >= 0)

# ================================================================ R · RISK-VAR-001
print("RISK-VAR-001")
rng = np.random.default_rng(20261113)
x = rng.standard_t(5, 800) * 0.01 + 0.0003
h, nivel = 5, 0.95


def rv(v):
    v["rendimientos"] = [float(a) for a in x]


mu, sd = x.mean(), x.std(ddof=1)
z = stats.norm.ppf(nivel)
r = servir("RISK-VAR-001", 0, rv, metodo="normal", horizonte=h, nivel=nivel)
K.comprobar("normal: VaR = (−μ + z·σ)·√h", cerca(r["var"], (-mu + z * sd) * math.sqrt(h)), f"{r['var']}")
K.comprobar("normal: ES = (−μ + σ·φ(z)/(1 − nivel))·√h", cerca(r["es"], (-mu + sd * stats.norm.pdf(z) / (1 - nivel)) * math.sqrt(h)), f"{r['es']}")
r = servir("RISK-VAR-001", 0, rv, metodo="cornish_fisher", horizonte=h, nivel=nivel)
S_, K_ = stats.skew(x), stats.kurtosis(x)
S1, K1 = stats.skew(x, bias=False), stats.kurtosis(x, bias=False)
zq = -z


def cf(s, k):
    w = zq + (zq ** 2 - 1) * s / 6 + (zq ** 3 - 3 * zq) * k / 24 - (2 * zq ** 3 - 5 * zq) * s ** 2 / 36
    return -(mu + sd * w) * math.sqrt(h)


conv = alguna(r["var"], {"momentos poblacionales": cf(S_, K_), "momentos insesgados": cf(S1, K1)})
K.comprobar(f"Cornish-Fisher: VaR con la expansión de cuarto orden ({conv})", conv is not None, f"{r['var']} ≠ {cf(S_, K_)} / {cf(S1, K1)}")
r = servir("RISK-VAR-001", 0, rv, metodo="historico", horizonte=h, nivel=nivel)
xs_ = np.sort(x)
k = int(round(len(x) * (1 - nivel)))
cands = {"estadístico de orden n(1−nivel)": -xs_[k - 1] * math.sqrt(h), "np.quantile lineal": -np.quantile(x, 1 - nivel) * math.sqrt(h),
         "orden inferior": -np.quantile(x, 1 - nivel, method="lower") * math.sqrt(h),
         "orden superior": -np.quantile(x, 1 - nivel, method="higher") * math.sqrt(h)}
conv = alguna(r["var"], cands)
K.comprobar(f"histórico: VaR = −cuantil empírico·√h ({conv})", conv is not None, f"{r['var']} frente a {cands}")
q = -r["var"] / math.sqrt(h)
K.comprobar("histórico: ES = −media de los rendimientos ≤ cuantil, ·√h", cerca(r["es"], -x[x <= q + 1e-15].mean() * math.sqrt(h)), f"{r['es']}")
K.comprobar("ES ≥ VaR", r["es"] >= r["var"])

# ================================================================ R · SIM-MC-001
print("SIM-MC-001")
mu_, sg_, s0, hh, n = 0.0005, 0.02, 250.0, 40, 40000


def mc(v):
    v["dinamica"].update({"mu": mu_, "sigma": sg_, "valor_inicial": s0})


r = servir("SIM-MC-001", 0, mc, n_trayectorias=n, horizonte=hh, semilla=777, cuantiles=[0.01, 0.25, 0.5, 0.9], umbrales=[230.0])
if r:
    ml, vl = hh * mu_, hh * sg_ ** 2
    d = r["distribucion"]
    for qq in (0.01, 0.25, 0.5, 0.9):
        an = s0 * math.exp(ml + math.sqrt(vl) * stats.norm.ppf(qq))
        dens = stats.lognorm.pdf(an, s=math.sqrt(vl), scale=s0 * math.exp(ml))
        ee = math.sqrt(qq * (1 - qq) / n) / dens
        K.comprobar(f"paseo aleatorio: cuantil {qq} a menos de 4 EE del lognormal", abs(d["cuantiles"][str(qq)] - an) <= 4 * ee,
                    f"{d['cuantiles'][str(qq)]} frente a {an} (EE {ee:.4f})")
    em = s0 * math.exp(ml + vl / 2)
    es_ = em * math.sqrt((math.exp(vl) - 1) / n)
    K.comprobar("paseo aleatorio: media a menos de 4 EE de S₀·exp(hμ + hσ²/2)", abs(d["media"] - em) <= 4 * es_, f"{d['media']} frente a {em}")
    pu = stats.norm.cdf((math.log(230.0 / s0) - ml) / math.sqrt(vl))
    pr = d["probabilidades_umbral"]
    print("   probabilidades_umbral:", pr, "· P(S < 230) analítica:", round(pu, 5))
    val = next(iter(pr.values())) if isinstance(pr, dict) and pr else None
    val = val if isinstance(val, float) else (next((v for v in val.values() if isinstance(v, float)), None) if isinstance(val, dict) else None)
    K.comprobar("paseo aleatorio: probabilidad del umbral a menos de 4 EE (P por debajo o por encima)",
                val is not None and min(abs(val - pu), abs(val - (1 - pu))) <= 4 * math.sqrt(pu * (1 - pu) / n), f"{pr}")

# ================================================================ R · ML-CAL-001
print("ML-CAL-001")
rng = np.random.default_rng(99)
nn = 80
y = rng.normal(0, 1, nn)
f_ = y * 0.6 + rng.normal(0, 0.5, nn)
ref = rng.normal(0, 0.3, nn)
inf_, sup_ = f_ - 0.9, f_ + 0.9


def cal(v):
    hz = v["horizontes"]["H2"]
    hz.update({"realizaciones": list(map(float, y)), "predicciones": list(map(float, f_)), "referencia": list(map(float, ref)),
               "intervalos": {"inferior": list(map(float, inf_)), "superior": list(map(float, sup_)), "nivel": 0.9}})


r = servir("ML-CAL-001", 0, cal)
if r:
    hz = r["horizontes"]["H2"]
    K.comprobar("MAE", cerca(hz["mae"], np.abs(f_ - y).mean(), 1e-10))
    K.comprobar("RMSE", cerca(hz["rmse"], math.sqrt(((f_ - y) ** 2).mean()), 1e-10))
    conv = alguna(hz["sesgo"], {"realización − predicción": (y - f_).mean(), "predicción − realización": (f_ - y).mean()}, 1e-10)
    K.comprobar(f"sesgo = media del error (signo que la ficha no fija: {conv})", conv is not None, f"{hz['sesgo']}")
    K.comprobar("R²_OOS = 1 − SSE/SSE_ref", cerca(hz["comparacion_referencia"]["r2_oos"], 1 - ((f_ - y) ** 2).sum() / ((ref - y) ** 2).sum(), 1e-10))
    K.comprobar("cobertura de los intervalos", cerca(hz["cobertura_intervalos"]["cobertura"], ((y >= inf_) & (y <= sup_)).mean(), 1e-12))
    ic = hz["mejora_frente_referencia"]["ic"]
    K.comprobar("IC de la mejora contiene la mejora media", ic[0] <= hz["mejora_frente_referencia"]["mejora_media"] <= ic[1], str(ic))

# ================================================================ V · ACC-ERP-001
print("ACC-ERP-001")
for g5, gL, rec in ((7.0, None, True), (7.0, 3.5, False), (1.0, 3.2, True)):
    def erp(v, g5=g5):
        v["g5"]["valor"] = g5
    par = {} if gL is None else {"g_L": gL}
    r = servir("ACC-ERP-001", 0, erp, incluir_recompras=rec, **par)
    v0 = servicio.CASOS_CONTROL["ACC-ERP-001"][0]["datos"][0]["valores"]
    F = v0["dividendos_12m"] + (v0["recompras_netas_12m"] if rec else 0)
    g, gl = g5 / 100, (gL if gL is not None else v0["rf_nominal_10a"]["valor"]) / 100

    def vp(rr):
        return sum(F * (1 + g) ** t / (1 + rr) ** t for t in range(1, 6)) + F * (1 + g) ** 5 * (1 + gl) / ((rr - gl) * (1 + rr) ** 5)
    rr = optimize.brentq(lambda q: vp(q) - v0["nivel"], gl + 1e-9, 1.0, xtol=1e-14)
    K.comprobar(f"r implícita con g₅ = {g5}, g_L = {gL}, recompras {rec} (brentq)", r is not None and cerca(r["r_implicita_pct"], rr * 100, 1e-7),
                f"{r and r['r_implicita_pct']} ≠ {rr * 100}")
    if r:
        K.comprobar("  PRM = r − r_f", cerca(r["prm_pp"], rr * 100 - v0["rf_nominal_10a"]["valor"], 1e-7))
        K.comprobar("  ECY = 100/CAPE − real", cerca(r["ecy_pp"], 100 / v0["cape"]["valor"] - v0["rf_real_10a"]["valor"], 1e-9))
        K.comprobar("  simple = E₁/P − real", cerca(r["version_simple_pp"], 100 * v0["beneficio_adelantado"] / v0["nivel"] - v0["rf_real_10a"]["valor"], 1e-9))

# ================================================================ V · ACC-FACT-001
print("ACC-FACT-001")
import statsmodels.api as sm  # noqa: E402

rng = np.random.default_rng(4)
T = 96
nombres = ["MKT", "SMB", "HML", "RMW", "CMA", "UMD"]
Fm = rng.normal(0.4, 3.0, (T, 6))
e = np.zeros(T)
for t in range(1, T):
    e[t] = 0.5 * e[t - 1] + rng.normal(0, 1.5)
yv = 0.25 + Fm @ np.array([1.1, 0.3, -0.2, 0.15, 0.05, -0.4]) + e
import pandas as pd  # noqa: E402

fechas = [str(d.date()) for d in pd.date_range("2015-01-31", periods=T, freq="ME")]


def fact(v):
    v["fechas"], v["rendimientos"] = fechas, list(map(float, yv))
    v["factores"] = {k: list(map(float, Fm[:, i])) for i, k in enumerate(nombres)}


r = servir("ACC-FACT-001", 0, fact)
if r:
    L = math.floor(4 * (T / 100) ** (2 / 9))
    X = sm.add_constant(Fm)
    a = sm.OLS(yv, X).fit(cov_type="HAC", cov_kwds={"maxlags": L, "use_correction": True})
    b = sm.OLS(yv, X).fit(cov_type="HAC", cov_kwds={"maxlags": L, "use_correction": False})
    K.comprobar("rezagos Newey-West = ⌊4(T/100)^(2/9)⌋", r["rezagos_nw"] == L, f"{r['rezagos_nw']} ≠ {L}")
    K.comprobar("betas = OLS de statsmodels", all(cerca(r["betas"][k]["beta"], a.params[i + 1], 1e-9) for i, k in enumerate(nombres)))
    K.comprobar("α anual compuesto (§3.1 del Catálogo): (1 + α)^12 − 1", cerca(r["alfa_anual_pct"], 100 * ((1 + a.params[0] / 100) ** 12 - 1), 1e-9),
                f"{r['alfa_anual_pct']} ≠ {100 * ((1 + a.params[0] / 100) ** 12 - 1)}")
    conv = alguna(r["t_alfa"], {"HAC con corrección de muestra": a.tvalues[0], "HAC sin corrección": b.tvalues[0]}, 1e-7)
    K.comprobar(f"t de α = Newey-West de statsmodels ({conv})", conv is not None, f"{r['t_alfa']} frente a {a.tvalues[0]} / {b.tvalues[0]}")
    ts = a.tvalues if conv and "con" in conv else b.tvalues
    K.comprobar("t de las betas = Newey-West de statsmodels", all(cerca(r["betas"][k]["t"], ts[i + 1], 1e-7) for i, k in enumerate(nombres)))
    K.comprobar("R²", cerca(r["r2"], a.rsquared, 1e-10))
    c = sm.OLS(yv, sm.add_constant(Fm[:, :1])).fit()
    K.comprobar("segunda vía CAPM: beta", cerca(r["segunda_via_capm"]["beta_mkt"], c.params[1], 1e-9))
    ult = r["betas_moviles"][-1]
    w = sm.OLS(yv[-36:], X[-36:]).fit()
    K.comprobar("betas móviles: última ventana de 36", all(cerca(ult["betas"][k], w.params[i + 1], 1e-8) for i, k in enumerate(nombres)), str(ult)[:200])
    tot = sum(v for v in r["contribuciones_varianza_pct"].values())
    K.comprobar("contribuciones a la varianza suman 100", cerca(tot, 100.0, 1e-8), f"{tot}")

# ================================================================ V · FX-PPA-001
print("FX-PPA-001")
nT = 48
pb = 100 * 1.001 ** np.arange(nT)          # inflación de la moneda base (EUR): 0,1 % mensual
pc = 100 * 1.004 ** np.arange(nT)          # inflación de la cotizada (USD): 0,4 % mensual
s = 1.10 * np.ones(nT)                     # EUR/USD (USD por EUR) plano
fe = [str(d.date()) for d in pd.date_range("2001-01-31", periods=nT, freq="ME")]


def ppa(v):
    v["fechas"], v["tipo_cambio"] = fe, list(map(float, s))
    v["indices"]["base"]["valores"], v["indices"]["cotizada"]["valores"] = list(map(float, pb)), list(map(float, pc))


r = servir("FX-PPA-001", 0, ppa)
if r:
    senda = 1.10 * (pc[-1] / pc[0]) / (pb[-1] / pb[0])   # PPA relativa: la divisa con más inflación (USD) se deprecia ⇒ más USD por EUR
    K.comprobar("senda PPA = cambio base × (P cotizada / P base), en unidades de cotizada por base", cerca(r["senda_ppa_final"], senda, 1e-9),
                f"{r['senda_ppa_final']} frente a {senda} (invertida daría {1.10 * (pb[-1] / pb[0]) / (pc[-1] / pc[0])})")
    K.comprobar("desviación final = 100·ln(s/senda)", cerca(r["desviacion_final_pct"], 100 * math.log(1.10 / senda), 1e-8), f"{r['desviacion_final_pct']}")
    K.comprobar("inflaciones acumuladas", cerca(r["inflacion_acumulada_pct"]["base"], 100 * (pb[-1] / pb[0] - 1), 1e-8)
                and cerca(r["inflacion_acumulada_pct"]["cotizada"], 100 * (pc[-1] / pc[0] - 1), 1e-8), str(r["inflacion_acumulada_pct"]))

# ================================================================ V · FIR-SPREAD-001
print("FIR-SPREAD-001")
c0 = servicio.CASOS_CONTROL["FIR-SPREAD-001"][0]["datos"][0]["valores"]
nh = len(c0["historia"]["fechas"])
rng = np.random.default_rng(8)
dif = np.abs(rng.normal(150, 40, nh)) + 20


def spr(v):
    v["historia"]["diferenciales_pb"] = list(map(float, dif))


r = servir("FIR-SPREAD-001", 0, spr, recuperacion=0.35)
if r:
    act = dif[-1]
    K.comprobar("diferencial actual = último de la historia", cerca(r["diferencial_pb"], act, 1e-12))
    conv = alguna(r["percentil"], {"≤ sobre n": (dif <= act).mean(), "< sobre n": (dif < act).mean(),
                                   "rango medio": ((dif < act).sum() + 0.5 * (dif == act).sum()) / nh,
                                   "≤ sin el actual": (dif[:-1] <= act).mean(), "< sobre n−1": (dif[:-1] < act).mean()}, 1e-9)
    K.comprobar(f"percentil del diferencial ({conv})", conv is not None, f"{r['percentil']}")
    conv = alguna(r["z"], {"ddof 1": (act - dif.mean()) / dif.std(ddof=1), "ddof 0": (act - dif.mean()) / dif.std()}, 1e-9)
    K.comprobar(f"z-score ({conv})", conv is not None, f"{r['z']}")
    pdm = sum(x["pd_anual"] * x["peso"] for x in c0["impagos"]["por_rating"].values())
    K.comprobar("exceso = s − PD·(1 − R) en pb", cerca(r["exceso_perdida_esperada_pb"], act - pdm * (1 - 0.35) * 1e4, 1e-9), f"{r['exceso_perdida_esperada_pb']}")
    K.comprobar("ampliación de equilibrio = s / duración del diferencial", cerca(r["ampliacion_equilibrio_pb"], act / c0["duracion_diferencial"], 1e-9))

# ================================================================ P · REI-CAP-001
print("REI-CAP-001")
c0 = servicio.CASOS_CONTROL["REI-CAP-001"][0]["datos"][0]["valores"]
rng = np.random.default_rng(3)
caps = 0.045 + rng.normal(0, 0.006, len(c0["historia"]))
sob = 0.03 + rng.normal(0, 0.008, len(c0["historia"]))


def cap(v):
    v["noi"]["valor"] = 61.3e6
    v["valor_tasacion"] = 1.19e9
    v["valor_mercado_implicito"] = {"capitalizacion": 5.4e8, "deuda_neta": 7.1e8}
    v["soberano_10a"]["rendimiento"] = 0.0275
    for i, hrow in enumerate(v["historia"]):
        hrow["cap_rate"], hrow["soberano_10a"] = float(caps[i]), float(sob[i])
    v["equilibrio"] = {"r": 0.081, "g_noi": 0.022}


r = servir("REI-CAP-001", 0, cap)
if r:
    ct, cm = 61.3e6 / 1.19e9, 61.3e6 / (5.4e8 + 7.1e8)
    K.comprobar("cap de tasación = NOI / valor", cerca(r["cap_rate_tasacion_pct"], 100 * ct, 1e-10))
    K.comprobar("cap de mercado = NOI / (capitalización + deuda neta)", cerca(r["cap_rate_mercado_pct"], 100 * cm, 1e-10))
    K.comprobar("diferencial = cap de tasación − soberano (pb)", cerca(r["diferencial_pb"], 1e4 * (ct - 0.0275), 1e-9))
    hd = 1e4 * (caps - sob)
    act = 1e4 * (ct - 0.0275)
    conv = alguna(r["percentil"], {"≤ sobre n": (hd <= act).mean(), "< sobre n": (hd < act).mean()}, 1e-9)
    K.comprobar(f"percentil del diferencial frente a la historia ({conv})", conv is not None, f"{r['percentil']} / {(hd <= act).mean()}")
    conv = alguna(r["z"], {"ddof 1": (act - hd.mean()) / hd.std(ddof=1), "ddof 0": (act - hd.mean()) / hd.std()}, 1e-9)
    K.comprobar(f"z ({conv})", conv is not None, f"{r['z']}")
    K.comprobar("cap de equilibrio = r − g", cerca(r["cap_equilibrio_pct"], 100 * (0.081 - 0.022), 1e-10))
    K.comprobar("brecha = cap de tasación − equilibrio (pb)", cerca(r["brecha_equilibrio_pb"], 1e4 * (ct - 0.059), 1e-8), f"{r['brecha_equilibrio_pb']}")

# ================================================================ P · CMD-INV-001
print("CMD-INV-001")
c0 = servicio.CASOS_CONTROL["CMD-INV-001"][0]["datos"][0]["valores"]
nobs = len(c0["inventarios"]["observaciones"])
rng = np.random.default_rng(12)
inv = 300 + 30 * np.sin(2 * np.pi * np.arange(nobs) / 12) + rng.normal(0, 12, nobs)


def cinv(v):
    for i, o in enumerate(v["inventarios"]["observaciones"]):
        o["valor"] = float(inv[i])


r = servir("CMD-INV-001", 0, cinv)
if r:
    prev = inv[nobs - 1 - 12 * np.arange(1, 6)]
    K.comprobar("media estacional = media del mismo mes de los 5 años anteriores", cerca(r["media_estacional"], prev.mean(), 1e-10), f"{r['media_estacional']} / {prev.mean()}")
    K.comprobar("desviación = inventario − media estacional", cerca(r["desviacion"], inv[-1] - prev.mean(), 1e-10))
    K.comprobar("desviación %", cerca(r["desviacion_pct"], 100 * (inv[-1] / prev.mean() - 1), 1e-9))
    conv = alguna(r["z"], {"ddof 1": (inv[-1] - prev.mean()) / prev.std(ddof=1), "ddof 0": (inv[-1] - prev.mean()) / prev.std()}, 1e-9)
    K.comprobar(f"z estacional ({conv})", conv is not None, f"{r['z']}")
    K.comprobar("días de cobertura = inventario / demanda diaria", cerca(r["dias_cobertura"], inv[-1] / c0["demanda_diaria"]["valor"], 1e-10))
    var_t = np.array([inv[nobs - 1 - 12 * k] - inv[nobs - 2 - 12 * k] for k in range(1, 6)])
    K.comprobar("sorpresa = variación − variación estacional típica", cerca(r["sorpresa"]["sorpresa"], (inv[-1] - inv[-2]) - var_t.mean(), 1e-9),
                f"{r['sorpresa']}")

# ================================================================ P · CHR-FLOW-001
print("CHR-FLOW-001")
c0 = servicio.CASOS_CONTROL["CHR-FLOW-001"][0]["datos"][0]["valores"]
fl = np.array([o["flujo"] for o in c0["flujos_etf"]])
pat = np.array([o["patrimonio"] for o in c0["flujos_etf"]])
r = servir("CHR-FLOW-001", 0)
if r:
    for w in (5, 20):
        K.comprobar(f"flujo acumulado a {w} días = suma de los últimos {w}", cerca(r["flujos"][str(w)]["moneda"], fl[-w:].sum(), 1e-12))
        conv = alguna(r["flujos"][str(w)]["pct_patrimonio"], {"sobre el patrimonio anterior a la ventana": 100 * fl[-w:].sum() / pat[-w - 1],
                                                              "sobre el último patrimonio": 100 * fl[-w:].sum() / pat[-1],
                                                              "sobre el primero de la ventana": 100 * fl[-w:].sum() / pat[-w]}, 1e-9)
        K.comprobar(f"  % de patrimonio ({conv})", conv is not None, f"{r['flujos'][str(w)]['pct_patrimonio']}")
        nz = r["flujos"][str(w)]["n_z"]
        rel = np.array([fl[j - w + 1: j + 1].sum() / pat[j - w] for j in range(w, len(fl))])   # % del patrimonio previo a cada ventana
        hist = rel[-nz:]
        cz = {"relativo, con el actual, ddof 1": (rel[-1] - hist.mean()) / hist.std(ddof=1),
              "relativo, con el actual, ddof 0": (rel[-1] - hist.mean()) / hist.std()}
        conv = alguna(r["flujos"][str(w)]["z"], cz, 1e-9)
        K.comprobar(f"  z-score a 1 año del acumulado relativo a {w} días ({conv})", conv is not None, f"{r['flujos'][str(w)]['z']} frente a {cz}")
        import datetime as _dt
        f_ult = _dt.date.fromisoformat(str(c0["flujos_etf"][-1]["fecha"])[:10])
        f_ini = _dt.date.fromisoformat(str(c0["flujos_etf"][-nz]["fecha"])[:10])
        f_ant = _dt.date.fromisoformat(str(c0["flujos_etf"][-nz - 1]["fecha"])[:10])
        K.comprobar("  la ventana del z es el último año natural de sesiones", f_ini > f_ult.replace(year=f_ult.year - 1) >= f_ant,
                    f"{f_ant} / {f_ini} / {f_ult}")

# ================================================================ P · REI-FFO-001
print("REI-FFO-001")
c0 = servicio.CASOS_CONTROL["REI-FFO-001"][0]["datos"][0]["valores"]
r = servir("REI-FFO-001", 0)
if r:
    ffo = affo = capi = div = 0.0
    for comp in c0["componentes"]:
        e_ = comp["ejercicios"][-1]
        f1 = e_["beneficio_neto"] + e_["amortizaciones_inmobiliarias"] - e_["plusvalias"]
        ffo += f1
        affo += f1 - e_["capex_mantenimiento"] - e_["ajuste_rentas_lineales"]
        capi += comp["precio"] * comp["acciones"]
        div += e_["dividendo"]
    K.comprobar("FFO = BN + amortizaciones − plusvalías (agregado)", cerca(r["ffo_agregado"], ffo, 1e-12))
    K.comprobar("AFFO = FFO − CAPEX − ajuste de rentas", cerca(r["affo_agregado"], affo, 1e-12))
    K.comprobar("P/FFO = capitalización / FFO", cerca(r["p_ffo"], capi / ffo, 1e-10))
    K.comprobar("cobertura agregada = AFFO / dividendo", cerca(r["cobertura_agregada"], affo / div, 1e-10))

# ================================================================ S · FX-BRK-001
print("FX-BRK-001")
rng = np.random.default_rng(31)
nB = 150
yb = np.where(np.arange(nB) < 97, 1.0, 2.2) + rng.normal(0, 0.5, nB)
r = servir("FX-BRK-001", 0, lambda v: v.__setitem__("serie", list(map(float, yb))), tipo_cambio="nivel")
if r:
    rec = math.ceil(0.15 * nB)
    ssr = {k: ((yb[:k] - yb[:k].mean()) ** 2).sum() + ((yb[k:] - yb[k:].mean()) ** 2).sum() for k in range(rec, nB - rec + 1)}
    kb = min(ssr, key=ssr.get)
    ru = r["rupturas"][0] if r["rupturas"] else None
    K.comprobar("ruptura de nivel = mínimo de la SSR por fuerza bruta", ru is not None and ru["indice"] == kb, f"{ru and ru['indice']} ≠ {kb}")
    if ru:
        K.comprobar("salto = diferencia de medias de los segmentos", cerca(ru["cambio"]["salto"], yb[kb:].mean() - yb[:kb].mean(), 1e-10))
        k_par = 1
        bic0 = nB * math.log(((yb - yb.mean()) ** 2).sum() / nB)
        bic1 = nB * math.log(ssr[kb] / nB)
        print(f"   BIC publicado: {r['bic']['nivel']} · n·ln(SSR/n): 0 rupturas {bic0:.6f}, 1 ruptura {bic1:.6f} (sin la penalización)")
        K.comprobar("mejora de BIC coherente: BIC(1) − BIC(0) = n·ln(SSR₁/SSR₀) + penalización positiva y finita",
                    0 < (r["bic"]["nivel"]["1"] - r["bic"]["nivel"]["0"]) - (bic1 - bic0) < 10 * math.log(nB),
                    f"{(r['bic']['nivel']['1'] - r['bic']['nivel']['0']) - (bic1 - bic0)}")
sys.exit(K.fin())
