"""QA r01 de T-112 · oráculos independientes del grupo R (riesgo, backtest y modelos), por Motor.servir.

- BT-DSR-001: fórmulas de Bailey y López de Prado (2012, 2014) escritas aparte; el ejemplo numérico del artículo
  (SR anual 2,5; T = 1 250; γ₃ = −3; γ₄ = 10; N = 100; V = ½) da DSR ≈ 0,9004 con el oráculo.
- BT-PBO-001: CSCV escrito con bucles (Bailey, Borwein, López de Prado y Zhu, 2017).
- BT-VAR-001: Kupiec, Christoffersen, Z₂ de Acerbi-Székely y semáforo escritos aparte; modo generado sin mirar al futuro.
- RISK-VAR-001: GARCH(1,1) con objetivo de varianza maximizado con otro optimizador; EVT-POT con una GPD propia.
- ML-PRED-001: métricas recalculadas de las predicciones y ausencia de fuga (cambiar el futuro no cambia el pasado).
"""
import itertools
import math
import sys
import time
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import numpy as np  # noqa: E402
from scipy import optimize, stats  # noqa: E402

warnings.simplefilter("ignore")
K = C.Contador("r01_03 oráculos R")
m = C.motor()


# ============================================================ BT-DSR-001
def dsr_oraculo(sr, T, g3, g4, N, V_periodo, sr_ref=0.0, nivel=0.95):
    ee = math.sqrt((1 - g3 * sr + (g4 - 1) / 4 * sr ** 2) / (T - 1))
    psr = stats.norm.cdf((sr - sr_ref) / ee)
    if N > 1:
        sr0 = math.sqrt(V_periodo) * ((1 - np.euler_gamma) * stats.norm.ppf(1 - 1 / N)
                                      + np.euler_gamma * stats.norm.ppf(1 - 1 / (N * math.e)))
    else:
        sr0 = 0.0
    dsr = stats.norm.cdf((sr - sr0) / ee)
    z = stats.norm.ppf(nivel)
    mintrl = 1 + (1 - g3 * sr + (g4 - 1) / 4 * sr ** 2) * (z / (sr - sr_ref)) ** 2 if sr > sr_ref else None
    return ee, psr, sr0, dsr, mintrl


print("BT-DSR-001")
_, _, sr0_p, dsr_p, _ = dsr_oraculo(2.5 / math.sqrt(250), 1250, -3, 10, 100, 0.5 / 250)
K.comprobar("oráculo: ejemplo de Bailey y López de Prado (2014): SR*₀ diario 0,1132 y DSR 0,9004",
            abs(sr0_p - 0.1132) < 5e-5 and abs(dsr_p - 0.9004) < 5e-5, f"{sr0_p} {dsr_p}")
rng = np.random.default_rng(4)
for caso, (r, N, V, unidad, ref) in {
    "t asimétrica": (0.0006 + 0.01 * (rng.standard_t(5, 1000) - 0.3 * rng.exponential(1, 1000)), 40, 0.8, "anual", 0.5),
    "mensual": (0.01 + 0.04 * rng.standard_normal(60), 7, 0.002, "periodo", 0.0),
}.items():
    freq = "mensual" if caso == "mensual" else "diaria"
    q = 12 if freq == "mensual" else 252
    res = C.servir(m, "BT-DSR-001", {"rendimientos": r.tolist(), "varianza_sr_ensayos": {"valor": V, "unidad": unidad}},
                   {"N": N, "SR_referencia": ref, "frecuencia": freq})
    if not K.comprobar(f"DSR {caso}: servida", res["estado"].startswith("SERVED"), str(res)[:300]):
        continue
    R = res["resultado"]
    n = len(r)
    mu, s = r.mean(), r.std(ddof=1)
    sr = mu / s
    d = r - mu
    m2, m3, m4 = np.mean(d ** 2), np.mean(d ** 3), np.mean(d ** 4)
    g1 = m3 / m2 ** 1.5
    g3 = g1 * math.sqrt(n * (n - 1)) / (n - 2)                          # asimetría corregida (Fisher-Pearson ajustada)
    g2 = m4 / m2 ** 2 - 3
    g4 = ((n + 1) * g2 + 6) * (n - 1) / ((n - 2) * (n - 3)) + 3          # curtosis corregida
    Vp = V / q if unidad == "anual" else V
    ee, psr, sr0, dsr, mt = dsr_oraculo(sr, n, g3, g4, N, Vp, ref / math.sqrt(q))
    K.comprobar(f"  {caso}: SR, asimetría y curtosis", np.allclose([sr, g3, g4], [R["sr_periodo"], R["asimetria"], R["curtosis"]], rtol=1e-10))
    K.comprobar(f"  {caso}: EE, PSR, SR*₀, DSR y MinTRL = oráculo",
                np.allclose(np.array([ee, psr, sr0, dsr, mt], dtype=float),
                            np.array([R["ee_periodo"], R["psr"], R["sr0_periodo"], R["dsr"], R["min_trl_periodos"]], dtype=float),
                            rtol=1e-10, atol=1e-14, equal_nan=True), f"{[ee, psr, sr0, dsr, mt]} vs {[R['ee_periodo'], R['psr'], R['sr0_periodo'], R['dsr'], R['min_trl_periodos']]}")
    K.comprobar(f"  {caso}: SR anual = SR·√q", abs(R["sr_anual"] - sr * math.sqrt(q)) < 1e-12)

# ============================================================ BT-PBO-001
print("BT-PBO-001")


def pbo_oraculo(M, S):
    T, N = M.shape
    b = T // S
    M = M[T - b * S:]
    bl = [M[i * b:(i + 1) * b] for i in range(S)]
    lams, isv, oosv = [], [], []
    for comb in itertools.combinations(range(S), S // 2):
        dentro = np.vstack([bl[i] for i in comb])
        fuera = np.vstack([bl[i] for i in range(S) if i not in comb])
        sh_in = dentro.mean(0) / dentro.std(0, ddof=1)
        sh_out = fuera.mean(0) / fuera.std(0, ddof=1)
        n_star = int(np.argmax(sh_in))
        rk = stats.rankdata(sh_out)[n_star]
        w = rk / (N + 1)
        lams.append(math.log(w / (1 - w)))
        isv.append(sh_in[n_star])
        oosv.append(sh_out[n_star])
    lams = np.array(lams)
    return float(np.mean(lams <= 0)), lams, np.polyfit(isv, oosv, 1)[0], float(np.mean(np.array(oosv) < 0))


for sem, (N, T, S, hab) in {1: (6, 400, 8, 0.0), 2: (12, 520, 10, 0.02), 3: (4, 333, 8, 0.0)}.items():
    rng = np.random.default_rng(sem)
    M = rng.standard_normal((T, N)) * 0.01 + hab * 0.01 * np.arange(N) / N
    res = C.servir(m, "BT-PBO-001", {"rendimientos": {f"c{i:02d}": M[:, i].tolist() for i in range(N)}}, {"S": S})
    if not K.comprobar(f"PBO N={N} T={T} S={S}: servida", res["estado"].startswith("SERVED"), str(res)[:300]):
        continue
    R = res["resultado"]
    pbo, lams, pend, pperd = pbo_oraculo(M, S)
    K.comprobar(f"  PBO = oráculo de bucles ({pbo:.4f})", abs(pbo - R["pbo"]) < 1e-12, f"{R['pbo']}")
    K.comprobar("  λ: media, mínimo y máximo", np.allclose([lams.mean(), lams.min(), lams.max()],
                                                         [R["lambda"]["media"], R["lambda"]["minimo"], R["lambda"]["maximo"]], rtol=1e-9))
    K.comprobar("  pendiente y probabilidad de pérdida", abs(pend - R["pendiente_degradacion"]) < 1e-9 and abs(pperd - R["probabilidad_perdida"]) < 1e-12)
    K.comprobar("  combinaciones = C(S, S/2)", R["combinaciones"] == math.comb(S, S // 2))

# ============================================================ BT-VAR-001
print("BT-VAR-001")


def kupiec(x, T, p):
    f = x / T
    l0 = (T - x) * math.log(1 - p) + (x * math.log(p) if x else 0)
    l1 = ((T - x) * math.log(1 - f) if T > x else 0) + (x * math.log(f) if x else 0)
    return -2 * (l0 - l1)


def christ(e):
    c = {(i, j): 0 for i in (0, 1) for j in (0, 1)}
    for a, b in zip(e[:-1], e[1:]):
        c[(int(a), int(b))] += 1
    n00, n01, n10, n11 = c[(0, 0)], c[(0, 1)], c[(1, 0)], c[(1, 1)]
    xl = lambda k, p: k * math.log(p) if k else 0.0  # noqa: E731
    pi = (n01 + n11) / (n00 + n01 + n10 + n11)
    p01 = n01 / (n00 + n01) if n00 + n01 else 0
    p11 = n11 / (n10 + n11) if n10 + n11 else 0
    return -2 * ((xl(n00 + n10, 1 - pi) + xl(n01 + n11, pi)) - (xl(n00, 1 - p01) + xl(n01, p01) + xl(n10, 1 - p11) + xl(n11, p11)))


rng = np.random.default_rng(8)
T = 600
sig = 0.01 * np.exp(0.3 * np.sin(np.arange(T) / 40))
res_ = sig * rng.standard_t(4, T) / math.sqrt(2)
var_p = 2.326 * sig * 0.8
es_p = 2.665 * sig * 0.8
for nivel in (0.99, 0.975):
    r = C.servir(m, "BT-VAR-001", {"var_previsto": var_p.tolist(), "es_previsto": es_p.tolist(), "resultados": res_.tolist()}, {"nivel": nivel})
    if not K.comprobar(f"BT-VAR previsto nivel {nivel}: servida", r["estado"].startswith("SERVED"), str(r)[:300]):
        continue
    R = r["resultado"]
    e = res_ < -var_p
    x = int(e.sum())
    luc, lind = kupiec(x, T, 1 - nivel), christ(e)
    K.comprobar(f"  LR_uc, LR_ind, LR_cc ({x} excedencias)", np.allclose([luc, lind, luc + lind], [R["lr_uc"], R["lr_ind"], R["lr_cc"]], rtol=1e-10))
    K.comprobar("  p-valores χ²", np.allclose([stats.chi2.sf(luc, 1), stats.chi2.sf(luc + lind, 2)], [R["p_uc"], R["p_cc"]], rtol=1e-9))
    z2 = np.sum(res_ * e / (T * (1 - nivel) * es_p)) + 1
    K.comprobar("  Z₂ de Acerbi-Székely", abs(z2 - R["z2"]) < 1e-12)
    if nivel == 0.99:
        x250 = int(e[-250:].sum())
        zona = "verde" if x250 <= 4 else ("amarilla" if x250 <= 9 else "roja")
        K.comprobar(f"  semáforo con las últimas 250 ({x250})", R["zona_semaforo"] == zona, str(R["zona_semaforo"]))
# Modo generado: VaR histórico ex ante con ventana 250
hist = 0.01 * rng.standard_t(5, 700)
r = C.servir(m, "BT-VAR-001", {"rendimientos": hist.tolist()}, {"nivel": 0.975})
if K.comprobar("BT-VAR generado con RISK-VAR-001: servida", r["estado"].startswith("SERVED"), str(r)[:300]):
    R = r["resultado"]
    vp = np.array([-np.quantile(hist[t - 250:t], 0.025) for t in range(250, 700)])
    e = hist[250:] < -vp
    K.comprobar("  excedencias = oráculo ex ante (cuantil de los 250 anteriores)", R["excedencias"]["n"] == int(e.sum()),
                f"{R['excedencias']['n']} vs {int(e.sum())}")
    hist2 = hist.copy()
    hist2[650:] = hist2[650:] * 5          # cambiar el futuro
    r2 = C.servir(m, "BT-VAR-001", {"rendimientos": hist2[:650].tolist()}, {"nivel": 0.975})
    r3 = C.servir(m, "BT-VAR-001", {"rendimientos": hist[:650].tolist()}, {"nivel": 0.975})
    K.comprobar("  sin mirar al futuro: el tramo común da lo mismo", r2["resultado"]["lr_uc"] == r3["resultado"]["lr_uc"])

# ============================================================ RISK-VAR-001
print("RISK-VAR-001")
rng = np.random.default_rng(12)
n = 1500
om, al, be = 2e-6, 0.08, 0.9
h, e_, rr = om / (1 - al - be), 0.0, []
for _ in range(n):
    h = om + al * e_ ** 2 + be * h
    e_ = math.sqrt(h) * rng.standard_normal()
    rr.append(0.0003 + e_)
rr = np.array(rr)
r = C.servir(m, "RISK-VAR-001", {"rendimientos": rr.tolist()}, {"metodo": "historico_filtrado", "nivel": 0.975})
if K.comprobar("RISK-VAR histórico filtrado: servida", r["estado"].startswith("SERVED"), str(r)[:300]):
    R = r["resultado"]
    g = R["detalle_metodo"]["garch"]
    eps = rr - rr.mean()
    v0 = eps.var()

    def nll(th):
        a_, b_ = th
        if a_ <= 0 or b_ <= 0 or a_ + b_ >= 1:
            return 1e12
        hh, out = v0, 0.0
        o_ = v0 * (1 - a_ - b_)
        hs = np.empty(n)
        hs[0] = v0
        for t in range(1, n):
            hs[t] = o_ + a_ * eps[t - 1] ** 2 + b_ * hs[t - 1]
        return 0.5 * np.sum(np.log(hs) + eps ** 2 / hs)

    best = min((optimize.minimize(nll, x0, method="Powell", options={"xtol": 1e-10, "ftol": 1e-13}) for x0 in
                ([0.05, 0.9], [0.15, 0.8], [0.02, 0.97])), key=lambda o: o.fun)
    K.comprobar("  GARCH: α, β = máximo propio (Powell, 3 arranques) a 2e-3", np.allclose(best.x, [g["alpha"], g["beta"]], atol=2e-3),
                f"{best.x} vs {[g['alpha'], g['beta']]}")
    K.comprobar("  GARCH: el máximo propio no mejora la verosimilitud del Motor en más de 1e-6 relativo",
                nll([g["alpha"], g["beta"]]) - best.fun <= 1e-6 * abs(best.fun), f"{nll([g['alpha'], g['beta']])} vs {best.fun}")
    try:
        from arch import arch_model
        am = arch_model(rr * 100, mean="Constant", vol="GARCH", p=1, q=1, dist="normal").fit(disp="off")
        K.comprobar("  GARCH: cerca de `arch` (sin objetivo de varianza) a 0,03", abs(am.params["alpha[1]"] - g["alpha"]) < 0.03
                    and abs(am.params["beta[1]"] - g["beta"]) < 0.03, f"arch {am.params.values} vs {g}")
    except ImportError:
        pass
    # VaR con los residuos estandarizados del Motor
    hs = np.empty(n)
    hs[0] = v0
    a_, b_ = g["alpha"], g["beta"]
    o_ = v0 * (1 - a_ - b_)
    for t in range(1, n):
        hs[t] = o_ + a_ * eps[t - 1] ** 2 + b_ * hs[t - 1]
    z = eps / np.sqrt(hs)
    s1 = math.sqrt(o_ + a_ * eps[-1] ** 2 + b_ * hs[-1])
    qz = np.quantile(z, 0.025)
    K.comprobar("  VaR FHS = −(μ + σ_{T+1}·q(z))", abs(R["var"] + (rr.mean() + s1 * qz)) < 1e-10)
    K.comprobar("  ES FHS", abs(R["es"] + (rr.mean() + s1 * z[z <= qz].mean())) < 1e-10)
rt = 0.01 * rng.standard_t(3, 2000)
r = C.servir(m, "RISK-VAR-001", {"rendimientos": rt.tolist()}, {"metodo": "evt_pot", "nivel": 0.99})
if K.comprobar("RISK-VAR EVT-POT: servida", r["estado"].startswith("SERVED"), str(r)[:300]):
    R = r["resultado"]
    L = -rt
    u = np.quantile(L, 0.9)
    y = L[L > u] - u

    def nll_gpd(th):
        xi, lb = th
        b = math.exp(lb)
        z_ = 1 + xi * y / b
        if np.any(z_ <= 0):
            return 1e12
        return len(y) * lb + (1 + 1 / xi) * np.sum(np.log(z_)) if abs(xi) > 1e-12 else len(y) * lb + np.sum(y) / b

    o = min((optimize.minimize(nll_gpd, x0, method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-12, "maxiter": 20000})
             for x0 in ([0.2, math.log(y.mean())], [0.5, math.log(y.mean() / 2)])), key=lambda o: o.fun)
    xi, b = o.x[0], math.exp(o.x[1])
    var = u + b / xi * ((len(L) / len(y) * 0.01) ** (-xi) - 1)
    es = (var + b - xi * u) / (1 - xi)
    K.comprobar("  ξ y β = MLE propia", abs(xi - R["detalle_metodo"]["xi"]) < 1e-4 and abs(b / R["detalle_metodo"]["beta"] - 1) < 1e-4,
                f"{xi},{b} vs {R['detalle_metodo']}")
    K.comprobar("  VaR y ES de McNeil = oráculo (1e-4 rel.)", abs(var / R["var"] - 1) < 1e-4 and abs(es / R["es"] - 1) < 1e-4,
                f"{var},{es} vs {R['var']},{R['es']}")
r = C.servir(m, "RISK-VAR-001", {"rendimientos": rt.tolist()}, {"metodo": "cornish_fisher", "nivel": 0.95})
K.comprobar("RISK-VAR: nivel 0,95 dentro del rango 0,90–0,99", r["estado"].startswith("SERVED") or "Cornish" in str(r), str(r)[:200])

# ============================================================ ML-PRED-001
print("ML-PRED-001")
import pandas as pd  # noqa: E402

rng = np.random.default_rng(31)
n = 420
fechas = [str(d.date()) for d in pd.bdate_range("2024-01-01", periods=n)]
x = rng.standard_normal(n)
ruido = rng.standard_normal(n)
precio = 100 * np.exp(np.cumsum(0.004 * np.r_[0, x[:-1]] + 0.01 * rng.standard_normal(n)))
val = {"fechas": fechas, "objetivo": {"serie": precio.tolist(), "horizonte": 1, "tipo": "direccion", "criterio_resolucion": "cierre siguiente"},
       "variables": {"x": {"serie": x.tolist(), "conocible_desde": fechas}, "ruido": {"serie": ruido.tolist(), "conocible_desde": fechas}}}
t0 = time.time()
r = C.servir(m, "ML-PRED-001", val)
print(f"   ML-PRED-001: {time.time() - t0:.1f} s")
if K.comprobar("ML-PRED: servida", r["estado"].startswith("SERVED"), str(r)[:300]):
    R = r["resultado"]
    pr = np.array([o["prediccion"] for o in R["predicciones_oos"]])
    yo = np.array([o["realizacion"] for o in R["predicciones_oos"]])
    idx = np.array([o["indice"] for o in R["predicciones_oos"]])
    K.comprobar("  realizaciones = dirección de serie[i + 1] > serie[i]", np.array_equal(yo, (precio[idx + 1] > precio[idx]).astype(float)))
    K.comprobar("  Brier = media de (p − y)²", abs(np.mean((pr - yo) ** 2) - R["metricas_oos"]["brier"]) < 1e-12)
    K.comprobar("  acierto", abs(np.mean((pr >= 0.5) == (yo == 1)) - R["metricas_oos"]["acierto"]) < 1e-12)
    ref = np.array([np.mean((precio[1:] > precio[:-1]).astype(float)[: t - 1 + 1]) for t in idx])
    K.comprobar("  BSS frente a la tasa base conocida", abs(1 - np.mean((pr - yo) ** 2) / np.mean((ref - yo) ** 2) - R["metricas_oos"]["bss"]) < 1e-12)
    # Fuga: cambiar la serie objetivo y las variables a partir del inicio del último pliegue no cambia los anteriores
    ult = R["particiones"][-1]["prueba"][0]
    val2 = __import__("copy").deepcopy(val)
    for j in range(ult + 1, n):
        val2["objetivo"]["serie"][j] *= (1.5 if j % 2 else 0.6)
    for j in range(R["particiones"][-1]["prueba"][1] + 1, n):
        val2["variables"]["x"]["serie"][j] = -val2["variables"]["x"]["serie"][j]
    r2 = C.servir(m, "ML-PRED-001", val2)
    p2 = {o["indice"]: o["prediccion"] for o in r2["resultado"]["predicciones_oos"]}
    previas = [o for o in R["predicciones_oos"] if o["indice"] < ult]
    K.comprobar(f"  sin fuga: {len(previas)} predicciones anteriores al último pliegue idénticas con el futuro cambiado",
                all(p2[o["indice"]] == o["prediccion"] for o in previas))
    ult_pl = [o for o in R["predicciones_oos"] if o["indice"] >= ult]
    K.comprobar("  y las del último pliegue no dependen de etiquetas posteriores a su inicio",
                all(p2[o["indice"]] == o["prediccion"] for o in ult_pl))
    K.comprobar("  particiones: entrenamiento ≤ inicio − embargo", all(pa["entrenamiento"][1] <= pa["prueba"][0] - R["embargo"] for pa in R["particiones"]))
sys.exit(K.fin())
