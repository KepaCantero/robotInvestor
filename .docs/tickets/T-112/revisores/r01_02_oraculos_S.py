"""QA r01 de T-112 · oráculos independientes del grupo S (estadística y series), por Motor.servir.

- FX-REGIME-001 (Markov switching por EM propio) frente a statsmodels MarkovRegression y un filtro de Hamilton propio.
- FX-COINT-001 (ADF, Engle-Granger y Johansen escritos a mano) frente a statsmodels adfuller, coint y VECM («ci»).
- REG-HMM-001 (HMM multivariante por EM propio) frente a un forward propio y un Baum-Welch propio con otros arranques.
- ST-INF-001 frente a scipy y statsmodels multipletests (Holm y BH).
"""
import math
import sys
import time
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

warnings.simplefilter("ignore")
K = C.Contador("r01_02 oráculos S")
m = C.motor()


# ============================================================ FX-REGIME-001
def serie_regimen(n, semilla, s=(0.01, 0.03), p=(0.97, 0.95), mu=0.0005):
    rng = np.random.default_rng(semilla)
    z, est = [], 0
    for _ in range(n):
        est = est if rng.uniform() < p[est] else 1 - est
        z.append(mu + s[est] * rng.standard_normal())
    return np.array(z)


def hamilton(y, pi0, A, mu, sd):
    filt, ll, pred = np.empty((len(y), len(pi0))), 0.0, pi0.copy()
    for t, x in enumerate(y):
        a = pred * stats.norm.pdf(x, mu, sd)
        c = a.sum()
        ll += math.log(c)
        filt[t] = a / c
        pred = filt[t] @ A
    return filt, ll


print("FX-REGIME-001")
from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression  # noqa: E402

for sem in (7, 21):
    y = serie_regimen(500, sem)
    r = C.servir(m, "FX-REGIME-001", {"serie": y.tolist()})
    if not K.comprobar(f"FX-REGIME semilla datos {sem}: servida", r["estado"].startswith("SERVED"), str(r)[:300]):
        continue
    R = r["resultado"]
    A = np.array(R["matriz_transicion"])
    mu = np.array([e["media"] for e in R["estados"]])
    sd = np.array([e["desviacion"] for e in R["estados"]])
    pi0 = np.array([e["probabilidad_inicial"] for e in R["estados"]])
    filt, ll = hamilton(y, pi0, A, mu, sd)
    K.comprobar(f"  [{sem}] loglik = filtro de Hamilton propio con sus parámetros", abs(ll - R["loglik"]) < 1e-6,
                f"{ll} vs {R['loglik']}")
    K.comprobar(f"  [{sem}] filtradas = filtro propio", np.max(np.abs(filt - np.array(R["serie"]["filtradas"]))) < 1e-8)
    # statsmodels con la probabilidad inicial del Motor: su máximo no debe superar el del Motor
    mod = MarkovRegression(y, k_regimes=2, trend="c", switching_trend=False, switching_variance=True)
    mod.initialize_known(pi0)
    # parámetros de statsmodels: p[0->0], p[1->0], const, sigma2.0, sigma2.1 (columna = estado de origen)
    start = np.array([A[0, 0], A[1, 0], mu[0], sd[0] ** 2, sd[1] ** 2])
    # statsmodels pone la probabilidad inicial un periodo antes de la primera observación; el Motor, en la primera
    # observación (pi0 estimada por EM). Se comparan los óptimos con la convención del Motor: se maximiza la loglik propia
    # (pi0 libre) desde el óptimo de statsmodels y desde el del Motor; ninguna debe mejorar al Motor.
    mejor = -np.inf
    for rep in range(6):
        try:
            res = mod.fit(start_params=None if rep else start, search_reps=20 if rep else 0, disp=False, maxiter=500)
            if res.llf > mejor:
                mejor, pr = res.llf, res.params
        except Exception as e:  # noqa: BLE001
            print("   statsmodels falla:", e)
    from scipy import optimize

    def nll(th):
        p00, p11 = 1 / (1 + np.exp(-th[0])), 1 / (1 + np.exp(-th[1]))
        s1, s2 = np.exp(th[3]), np.exp(th[4])
        q = 1 / (1 + np.exp(-th[5]))
        A_ = np.array([[p00, 1 - p00], [1 - p11, p11]])
        return -hamilton(y, np.array([q, 1 - q]), A_, np.array([th[2], th[2]]), np.array([s1, s2]))[1]

    def theta(A_, mu_, sd_, q):
        lg = lambda x: math.log(min(max(x, 1e-9), 1 - 1e-9) / (1 - min(max(x, 1e-9), 1 - 1e-9)))  # noqa: E731
        return np.array([lg(A_[0, 0]), lg(A_[1, 1]), mu_, math.log(sd_[0]), math.log(sd_[1]), lg(q)])

    sig_sm = np.sqrt(pr[3:5])
    o = np.argsort(sig_sm)
    P_sm = np.array([[pr[0], 1 - pr[0]], [pr[1], 1 - pr[1]]])[np.ix_(o, o)]
    arranques = [theta(A, mu[0], sd, pi0[0]), theta(P_sm, pr[2], sig_sm[o], 0.5)]
    mejores = []
    for th0 in arranques:
        op_ = optimize.minimize(nll, th0, method="Nelder-Mead", options={"maxiter": 20000, "xatol": 1e-10, "fatol": 1e-12})
        mejores.append(-op_.fun)
    K.comprobar(f"  [{sem}] máximo propio (pi0 libre) desde el Motor y desde statsmodels no mejora al Motor (+1e-5)",
                max(mejores) <= R["loglik"] + 1e-5, f"propio {mejores} vs motor {R['loglik']}; statsmodels {mejor}")
    K.comprobar(f"  [{sem}] el óptimo de statsmodels (su convención) queda a menos de 0,05 del Motor", abs(mejor - R["loglik"]) < 0.05,
                f"sm {mejor} vs motor {R['loglik']}")
    # Parámetros frente a statsmodels (estados ordenados por varianza)
    K.comprobar(f"  [{sem}] desviaciones ≈ statsmodels (5 % rel., otra convención inicial)", np.allclose(sig_sm[o], sd, rtol=5e-2),
                f"{sig_sm[o]} vs {sd}")
    K.comprobar(f"  [{sem}] transición ≈ statsmodels (0,01)", np.allclose(P_sm, A, atol=1e-2), f"{P_sm} vs {A}")
    dur = [1 / (1 - A[i, i]) for i in range(2)]
    K.comprobar(f"  [{sem}] duraciones = 1/(1 − p_ii)", np.allclose(dur, R["duraciones_esperadas"], rtol=1e-12))
    pi = np.linalg.solve(np.array([[A[0, 0] - 1, A[1, 0]], [1, 1]]), [0, 1])
    K.comprobar(f"  [{sem}] distribución estacionaria", np.allclose(pi, R["distribucion_estacionaria"], atol=1e-10))
    # BIC de un régimen
    bic1 = -2 * np.sum(stats.norm.logpdf(y, y.mean(), y.std())) + 2 * math.log(len(y))
    K.comprobar(f"  [{sem}] BIC de un régimen", abs(bic1 - R["referencia_ingenua"]["bic"]) < 1e-6)
    # Régimen actual: argmax de la última filtrada si ≥ umbral
    u = R["probabilidades_filtradas_actuales"]
    kmax = max(u, key=u.get)
    K.comprobar(f"  [{sem}] régimen actual coherente con el umbral",
                R["regimen_actual"] == (kmax if u[kmax] >= R["umbral"] else "indeterminado"))

# ============================================================ FX-COINT-001
print("FX-COINT-001")
from statsmodels.tsa.stattools import adfuller, coint  # noqa: E402
from statsmodels.tsa.vector_ar.vecm import VECM  # noqa: E402

for sem in (3, 11):
    rng = np.random.default_rng(sem)
    n = 400
    x = np.cumsum(rng.standard_normal(n)) + 50
    u_ = np.zeros(n)
    for t in range(1, n):
        u_[t] = 0.6 * u_[t - 1] + rng.standard_normal()
    yv = 1.5 * x + 3 + u_
    z = np.cumsum(rng.standard_normal(n)) + 20
    r = C.servir(m, "FX-COINT-001", {"series": {"y": yv.tolist(), "x": x.tolist(), "z": z.tolist()}})
    if not K.comprobar(f"FX-COINT datos {sem} (3 series): servida", r["estado"].startswith("SERVED"), str(r)[:300]):
        continue
    R = r["resultado"]
    L = R["rezago_maximo"]
    Y = np.column_stack([yv, x, z])
    for j, c in enumerate(["y", "x", "z"]):
        a0 = adfuller(Y[:, j], maxlag=L, regression="c", autolag="AIC")
        a1 = adfuller(np.diff(Y[:, j]), maxlag=L, regression="c", autolag="AIC")
        K.comprobar(f"  [{sem}] ADF nivel {c} = statsmodels", abs(a0[0] - R["integracion"][c]["adf_nivel"]["tau"]) < 1e-8,
                    f"{a0[0]} vs {R['integracion'][c]['adf_nivel']['tau']} (rez {a0[2]} vs {R['integracion'][c]['adf_nivel']['rezagos']})")
        K.comprobar(f"  [{sem}] ADF diferencia {c} = statsmodels",
                    abs(a1[0] - R["integracion"][c]["adf_diferencia"]["tau"]) < 1e-8,
                    f"{a1[0]} vs {R['integracion'][c]['adf_diferencia']['tau']}")
    eg = coint(Y[:, 0], Y[:, 1:], trend="c", maxlag=L, autolag="aic")
    K.comprobar(f"  [{sem}] Engle-Granger τ = statsmodels coint", abs(eg[0] - R["engle_granger"]["adf_residuos"]["tau"]) < 1e-8,
                f"{eg[0]} vs {R['engle_granger']['adf_residuos']['tau']}")
    # Johansen caso 2 (constante restringida): VECM «ci» de statsmodels con el mismo orden
    kd = R["johansen"]["orden_var"] - 1
    lls = {}
    for rk in (1, 2):
        lls[rk] = VECM(Y, k_ar_diff=kd, coint_rank=rk, deterministic="ci").fit().llf
    lam = np.array(R["johansen"]["autovalores"])
    T = len(Y) - 1 - kd
    tr = [t["estadistico"] for t in R["johansen"]["traza"]]
    K.comprobar(f"  [{sem}] traza(1) − traza(2) = 2·(llf₂ − llf₁) del VECM «ci»", abs((tr[1] - tr[2]) - 2 * (lls[2] - lls[1])) < 1e-6,
                f"{tr[1] - tr[2]} vs {2 * (lls[2] - lls[1])}")
    K.comprobar(f"  [{sem}] traza = −T·Σ ln(1 − λ)", all(abs(tr[r_] + T * np.sum(np.log(1 - lam[r_:]))) < 1e-8 for r_ in range(3)))
    v1 = VECM(Y, k_ar_diff=kd, coint_rank=1, deterministic="ci").fit()
    beta = v1.beta[:, 0] / v1.beta[0, 0]
    const = float(v1.det_coef_coint[0, 0]) / v1.beta[0, 0]
    vec = R["vector_normalizado"]
    K.comprobar(f"  [{sem}] vector normalizado = VECM «ci» de statsmodels", np.allclose([vec["y"], vec["x"], vec["z"]], beta, atol=1e-8),
                f"{[vec['y'], vec['x'], vec['z']]} vs {beta}")
    K.comprobar(f"  [{sem}] constante del vector = VECM", abs(vec["constante"] - const) < 1e-6, f"{vec['constante']} vs {const}")
    alfa = v1.alpha[:, 0] * v1.beta[0, 0]
    va = R["velocidad_ajuste"]
    K.comprobar(f"  [{sem}] velocidad de ajuste = α del VECM", np.allclose([va["y"], va["x"], va["z"]], alfa, atol=1e-8),
                f"{[va['y'], va['x'], va['z']]} vs {alfa}")
    K.comprobar(f"  [{sem}] rango 1 detectado (y, x cointegradas; z aparte)", R["johansen"]["rango"] == 1, str(R["johansen"]["traza"]))

# ============================================================ REG-HMM-001
print("REG-HMM-001")


def datos_hmm(n, semilla):
    rng = np.random.default_rng(semilla)
    est, X = 0, []
    for _ in range(n):
        est = est if rng.uniform() < (0.97 if est == 0 else 0.93) else 1 - est
        mu = (0.3, -0.2) if est == 0 else (-1.2, 1.5)
        X.append([mu[0] + rng.standard_normal() * (0.8 if est == 0 else 1.4), mu[1] + rng.standard_normal() * 0.7])
    return np.array(X)


def forward(Z, pi0, A, mus, covs):
    ll, pred, filt = 0.0, pi0.copy(), []
    for x in Z:
        dens = np.array([stats.multivariate_normal.pdf(x, mus[k], covs[k]) for k in range(len(pi0))])
        a = pred * dens
        c = a.sum()
        ll += math.log(c)
        filt.append(a / c)
        pred = filt[-1] @ A
    return np.array(filt), ll


def baum_welch(Z, k, semilla, arranques=10, it=400):
    rng = np.random.default_rng(semilla)
    n, d = Z.shape
    mejor = -np.inf
    for _ in range(arranques):
        mus = Z[rng.choice(n, k, replace=False)]
        covs = np.array([np.cov(Z.T) for _ in range(k)])
        A = np.full((k, k), 0.1 / (k - 1))
        np.fill_diagonal(A, 0.9)
        pi0 = np.full(k, 1 / k)
        prev = -np.inf
        for _ in range(it):
            B = np.column_stack([stats.multivariate_normal.pdf(Z, mus[j], covs[j]) for j in range(k)])
            al, c = np.zeros((n, k)), np.zeros(n)
            al[0] = pi0 * B[0]
            c[0] = al[0].sum()
            al[0] /= c[0]
            for t in range(1, n):
                al[t] = (al[t - 1] @ A) * B[t]
                c[t] = al[t].sum()
                al[t] /= c[t]
            be = np.ones((n, k))
            for t in range(n - 2, -1, -1):
                be[t] = (A @ (B[t + 1] * be[t + 1])) / c[t + 1]
            g = al * be
            g /= g.sum(1, keepdims=True)
            xi = al[:-1, :, None] * A[None] * (B[1:] * be[1:])[:, None, :] / c[1:, None, None]
            pi0 = g[0]
            A = xi.sum(0) / xi.sum(0).sum(1, keepdims=True)
            for j in range(k):
                w = g[:, j]
                mus[j] = w @ Z / w.sum()
                dz = Z - mus[j]
                covs[j] = np.diag((w @ dz ** 2) / w.sum())
            ll = np.log(c).sum()
            if abs(ll - prev) < 1e-10:
                break
            prev = ll
        mejor = max(mejor, ll)
    return mejor


X = datos_hmm(300, 5)
fechas = [str(d.date()) for d in __import__("pandas").date_range("2019-01-04", periods=300, freq="W-FRI")]
t0 = time.time()
r = C.servir(m, "REG-HMM-001", {"variables": {"a": X[:, 0].tolist(), "b": X[:, 1].tolist()}, "fechas": fechas},
             {"n_estados": 2})
print(f"   REG-HMM-001 k = 2: {time.time() - t0:.1f} s")
if K.comprobar("REG-HMM k = 2 servida", r["estado"].startswith("SERVED"), str(r)[:300]):
    R = r["resultado"]
    Z = (X - X.mean(0)) / X.std(0, ddof=1)
    A = np.array(R["matriz_transicion"])
    pi0 = np.array([e["probabilidad_inicial"] for e in R["estados"]])
    mus = np.array([[e["medias_estandarizadas"]["a"], e["medias_estandarizadas"]["b"]] for e in R["estados"]])
    covs = np.array([np.diag(e["covarianza_estandarizada"]) for e in R["estados"]])
    filt, ll = forward(Z, pi0, A, mus, covs)
    K.comprobar("  loglik = forward propio con sus parámetros", abs(ll - R["loglik"]) < 1e-6, f"{ll} vs {R['loglik']}")
    K.comprobar("  filtradas = forward propio", np.max(np.abs(filt - np.array(R["serie_filtradas"]["probabilidades"]))) < 1e-8)
    ll_bw = baum_welch(Z, 2, 99)
    K.comprobar("  Baum-Welch propio (10 arranques) no supera al Motor (+1e-4)", ll_bw <= R["loglik"] + 1e-4, f"{ll_bw} vs {R['loglik']}")
    K.comprobar("  medias desestandarizadas = μ·sd + media",
                np.allclose([[e["medias"]["a"], e["medias"]["b"]] for e in R["estados"]], mus * X.std(0, ddof=1) + X.mean(0)))
    K.comprobar("  estados ordenados por la media de la primera variable", mus[0, 0] <= mus[1, 0])
t0 = time.time()
r = C.servir(m, "REG-HMM-001", {"variables": {"a": X[:, 0].tolist(), "b": X[:, 1].tolist()}, "fechas": fechas})
dt = time.time() - t0
print(f"   REG-HMM-001 BIC (2–4 estados), doble pasada del Motor: {dt:.1f} s")
if K.comprobar("REG-HMM BIC servida", r["estado"].startswith("SERVED"), str(r)[:300]):
    R = r["resultado"]
    d, n = 2, 300
    ok = True
    for k_, b in R["bic"].items():
        k_ = int(k_)
        npar = (k_ - 1) + k_ * (k_ - 1) + 2 * k_ * d
        ok &= b > 0 and math.isfinite(b) and npar > 0
    K.comprobar("  BIC elige 2 estados en datos de 2 estados", R["n_estados"] == 2, str(R["bic"]))

# ============================================================ ST-INF-001
print("ST-INF-001")
from statsmodels.stats.multitest import multipletests  # noqa: E402

rng = np.random.default_rng(1)
cs = [{"nombre": f"c{i}", "muestra": (rng.standard_normal(25) + d).tolist(), "mu0": 0.0} for i, d in enumerate((0.0, 0.3, 0.6, 0.1, 0.9))]
for corr, met in (("holm", "holm"), ("bh", "fdr_bh")):
    r = C.servir(m, "ST-INF-001", {"contrastes": cs}, {"tipo_contraste": "t_una_muestra", "correccion": corr})
    if not K.comprobar(f"ST-INF t una muestra + {corr}: servida", r["estado"].startswith("SERVED"), str(r)[:300]):
        continue
    R = r["resultado"]
    pv = [stats.ttest_1samp(c["muestra"], 0.0).pvalue for c in cs]
    filas = [R["contrastes"][c["nombre"]] for c in cs]
    pm = [f["p_valor"] for f in filas]
    K.comprobar(f"  p-valores = scipy ({corr})", np.allclose(pm, pv, rtol=1e-10), f"{pm} vs {pv}")
    adj = multipletests(pv, alpha=0.05, method=met)[1]
    pa = [f.get("p_ajustado") for f in filas]
    K.comprobar(f"  p ajustados = statsmodels {met}", np.allclose(pa, adj, rtol=1e-10), f"{pa} vs {adj}")
a, b = rng.standard_normal(30).tolist(), (rng.standard_normal(40) * 2 + 0.5).tolist()
r = C.servir(m, "ST-INF-001", {"contrastes": [{"nombre": "w", "muestra_a": a, "muestra_b": b}]}, {"tipo_contraste": "t_welch"})
if K.comprobar("ST-INF Welch servida", r["estado"].startswith("SERVED"), str(r)[:300]):
    f0 = r["resultado"]["contrastes"]["w"]
    K.comprobar("  Welch p = scipy", abs(f0["p_valor"] - stats.ttest_ind(a, b, equal_var=False).pvalue) < 1e-10, str(f0)[:300])
sys.exit(K.fin())
