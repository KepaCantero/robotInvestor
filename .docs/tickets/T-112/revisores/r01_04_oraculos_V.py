"""QA r01 de T-112 · oráculos independientes del grupo V (valoración), por Motor.servir.

- DER-OPT-001: BSM y Black-76 cerrados propios, griegas por diferencias finitas, volatilidad implícita por bisección
  propia en casos extremos, CRR americano con un árbol propio de 2 000 pasos y cotas de no arbitraje.
- FIR-PRICE-001: bono con calendario propio (dateutil), precio, corrido, rendimiento, y duración y convexidad como
  derivadas numéricas del precio.
- FIR-CURVE-001: NSS por mínimos cuadrados con 300 arranques propios: el Motor no debe quedar en un mínimo peor.
- ACC-VAL-001: DCF de Gordon recalculado a mano desde los datos (WACC, FCFF, VT, EV, DCF inverso y sensibilidad).
"""
import math
import sys
import time
import warnings
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import numpy as np  # noqa: E402
from dateutil.relativedelta import relativedelta  # noqa: E402
from scipy import optimize, stats  # noqa: E402

warnings.simplefilter("ignore")
K = C.Contador("r01_04 oráculos V")
m = C.motor()


# ============================================================ DER-OPT-001
def bs(S, Kk, T, r, q, s, call):
    d1 = (math.log(S / Kk) + (r - q + s * s / 2) * T) / (s * math.sqrt(T))
    d2 = d1 - s * math.sqrt(T)
    if call:
        return S * math.exp(-q * T) * stats.norm.cdf(d1) - Kk * math.exp(-r * T) * stats.norm.cdf(d2)
    return Kk * math.exp(-r * T) * stats.norm.cdf(-d2) - S * math.exp(-q * T) * stats.norm.cdf(-d1)


def arbol(S, Kk, T, r, q, s, call, N):
    dt = T / N
    u = math.exp(s * math.sqrt(dt))
    d = 1 / u
    p = (math.exp((r - q) * dt) - d) / (u - d)
    disc = math.exp(-r * dt)
    pr = S * u ** np.arange(N, -N - 1, -2)
    v = np.maximum(pr - Kk, 0) if call else np.maximum(Kk - pr, 0)
    for i in range(N - 1, -1, -1):
        pr = S * u ** np.arange(i, -i - 1, -2)
        v = np.maximum(disc * (p * v[:-1] + (1 - p) * v[1:]), (pr - Kk) if call else (Kk - pr))
    return float(v[0])


print("DER-OPT-001")
rng = np.random.default_rng(5)
contratos = []
for i in range(25):
    S, Kk = 100.0, float(rng.uniform(50, 160))
    T, r, q, sg = float(rng.uniform(0.02, 3)), float(rng.uniform(-1, 8)), float(rng.uniform(0, 5)), float(rng.uniform(5, 120))
    contratos.append({"S": S, "K": Kk, "T": T, "r": r, "q": q, "estilo": "europea", "sigma": sg, "tipo": "call" if i % 2 else "put"})
r_ = C.servir(m, "DER-OPT-001", {"contratos": contratos})
if K.comprobar("DER-OPT 25 europeas aleatorias: servida", r_["estado"].startswith("SERVED"), str(r_)[:300]):
    malp, malg = [], []
    for c, f in zip(contratos, r_["resultado"]["contratos"]):
        a = (c["S"], c["K"], c["T"], c["r"] / 100, c["q"] / 100, c["sigma"] / 100, c["tipo"] == "call")
        pr = bs(*a)
        if abs(pr - f["precio"]) > 1e-9 * max(1, pr):
            malp.append((c, pr, f["precio"]))
        h = 1e-4
        dS = (bs(a[0] + h, *a[1:]) - bs(a[0] - h, *a[1:])) / (2 * h)
        gS = (bs(a[0] + h, *a[1:]) - 2 * pr + bs(a[0] - h, *a[1:])) / h ** 2
        vg = (bs(*a[:5], a[5] + 1e-5, a[6]) - bs(*a[:5], a[5] - 1e-5, a[6])) / 2e-5 / 100
        th = -(bs(a[0], a[1], a[2] + 1e-6, *a[3:]) - bs(a[0], a[1], a[2] - 1e-6, *a[3:])) / 2e-6 / 365
        rh = (bs(*a[:3], a[3] + 1e-6, *a[4:]) - bs(*a[:3], a[3] - 1e-6, *a[4:])) / 2e-6 / 100
        ok = (abs(dS - f["delta"]) < 1e-6 and abs(gS - f["gamma"]) < 1e-4 and abs(vg - f["vega"]) < 1e-6
              and abs(th - f["theta_dia"]) < 1e-6 and abs(rh - f["rho"]) < 1e-6)
        if not ok:
            malg.append((c, [dS, gS, vg, th, rh], [f["delta"], f["gamma"], f["vega"], f["theta_dia"], f["rho"]]))
    K.comprobar("  precios BSM = fórmula cerrada propia", not malp, str(malp[:2]))
    K.comprobar("  Δ, Γ, vega/punto, θ/día (365) y ρ/punto = diferencias finitas", not malg, str(malg[:2]))
# Volatilidad implícita: ida y vuelta en casos difíciles (OTM profundo, vencimiento corto, vol alta)
casos = [(100, 160, 0.05, 2, 0, 35, "call"), (100, 60, 0.1, 1, 0, 80, "put"), (100, 100, 5, 3, 2, 150, "call"),
         (100, 99, 0.01, 0, 0, 12, "put"), (50, 120, 2, 4, 1, 60, "call"), (100, 100, 1, 5, 0, 1.5, "call")]
for S, Kk, T, r, q, sg, tipo in casos:
    pr = bs(S, Kk, T, r / 100, q / 100, sg / 100, tipo == "call")
    res = C.servir(m, "DER-OPT-001", {"contratos": [{"S": S, "K": Kk, "T": T, "r": r, "q": q, "estilo": "europea", "precio": pr, "tipo": tipo}]})
    if res["estado"].startswith("SERVED"):
        iv = res["resultado"]["contratos"][0]["iv_pct"]
        K.comprobar(f"  IV ida y vuelta {tipo} K={Kk} T={T} σ={sg} %: {iv:.10f}", abs(iv - sg) < 1e-5,
                    f"precio {pr}")
    else:
        K.comprobar(f"  IV ida y vuelta {tipo} K={Kk} T={T} σ={sg} %: rechazada", False, str(res)[:200])
# Black-76
res = C.servir(m, "DER-OPT-001", {"contratos": [{"S": 80, "K": 85, "T": 0.5, "r": 4, "estilo": "europea", "sigma": 30, "tipo": "call",
                                                 "subyacente": "futuro"}]})
if K.comprobar("Black-76: servida", res["estado"].startswith("SERVED"), str(res)[:300]):
    f = res["resultado"]["contratos"][0]
    d1 = (math.log(80 / 85) + 0.045 * 0.5) / (0.3 * math.sqrt(0.5))
    b76 = math.exp(-0.04 * 0.5) * (80 * stats.norm.cdf(d1) - 85 * stats.norm.cdf(d1 - 0.3 * math.sqrt(0.5)))
    K.comprobar("  precio Black-76 = e^{−rT}[F·N(d₁) − K·N(d₂)]", abs(f["precio"] - b76) < 1e-10, f"{f['precio']} vs {b76}")
    K.comprobar("  ρ de Black-76 = −T·C/100", abs(f["rho"] + 0.5 * b76 / 100) < 1e-10)
# Americanas
t0 = time.time()
for (S, Kk, T, r, q, sg, tipo) in [(100, 100, 1, 5, 0, 20, "put"), (100, 110, 0.75, 3, 4, 30, "call"), (90, 100, 2, 6, 0, 25, "put")]:
    res = C.servir(m, "DER-OPT-001", {"contratos": [{"S": S, "K": Kk, "T": T, "r": r, "q": q, "estilo": "americana", "sigma": sg, "tipo": tipo}]})
    if not K.comprobar(f"americana {tipo} K={Kk}: servida", res["estado"].startswith("SERVED"), str(res)[:300]):
        continue
    f = res["resultado"]["contratos"][0]
    ref = (arbol(S, Kk, T, r / 100, q / 100, sg / 100, tipo == "call", 2000) + arbol(S, Kk, T, r / 100, q / 100, sg / 100, tipo == "call", 2001)) / 2
    p500 = (arbol(S, Kk, T, r / 100, q / 100, sg / 100, tipo == "call", 500) + arbol(S, Kk, T, r / 100, q / 100, sg / 100, tipo == "call", 501)) / 2
    K.comprobar(f"  CRR(500/501) = árbol propio exacto", abs(f["precio"] - p500) < 1e-10, f"{f['precio']} vs {p500}")
    K.comprobar(f"  CRR(500/501) a ≤ 2e-3 del árbol de 2 000 pasos ({ref:.5f})", abs(f["precio"] - ref) < 2e-3, f"{f['precio']}")
print(f"   americanas: {time.time() - t0:.1f} s")
for pr, tipo, msg in [(4.0, "put", "put europea por debajo de la cota inferior"), (101.0, "call", "call por encima de S·e^{−qT}")]:
    res = C.servir(m, "DER-OPT-001", {"contratos": [{"S": 100, "K": 110, "T": 1, "r": 5, "q": 0, "estilo": "europea", "precio": pr, "tipo": tipo}]})
    K.comprobar(f"rechazo por no arbitraje: {msg}", res["estado"] == "RECHAZADO", str(res)[:200])

# ============================================================ FIR-PRICE-001
print("FIR-PRICE-001")


def calendario(liq, venc, f):
    meses = 12 // f
    fs = [venc]
    k = 1
    while fs[-1] > liq:
        fs.append(venc - relativedelta(months=meses * k))
        k += 1
    return fs[::-1]


def d30e(a, b):
    return 360 * (b.year - a.year) + 30 * (b.month - a.month) + min(b.day, 30) - min(a.day, 30)


def bono_propio(cup, f, liq, venc, conv, y):
    fs = calendario(liq, venc, f)
    prev, sig = fs[0], fs[1]
    a = (liq - prev).days / (sig - prev).days if conv == "ACT/ACT-ICMA" else d30e(prev, liq) / (360 / f)
    cf = [cup / f] * (len(fs) - 1)
    cf[-1] += 100

    def P(yy):
        return sum(c / (1 + yy / 100 / f) ** (1 - a + k) for k, c in enumerate(cf))
    return P, cup / f * a


rng = np.random.default_rng(9)
for i in range(12):
    f = [1, 2, 4, 12][i % 4]
    conv = "ACT/ACT-ICMA" if i % 3 else "30E/360"
    liq = date(2026, 1, 1) + relativedelta(days=int(rng.integers(0, 700)))
    venc = date(2027, 1, 31) + relativedelta(months=int(rng.integers(6, 360)))
    if i == 5:
        venc = date(2036, 2, 29)      # fin de mes en año bisiesto
    cup, y = float(np.round(rng.uniform(0, 9), 3)), float(np.round(rng.uniform(-0.5, 12), 4))
    P, ai = bono_propio(cup, f, liq, venc, conv, y)
    res = C.servir(m, "FIR-PRICE-001", {"cupon": cup, "frecuencia": f, "liquidacion": str(liq), "vencimiento": str(venc), "convencion": conv,
                                        "rendimiento": y})
    if not K.comprobar(f"bono {i} f={f} {conv} {liq}→{venc} c={cup} y={y}: servido", res["estado"].startswith("SERVED"), str(res)[:300]):
        continue
    R = res["resultado"]
    sucio = P(y)
    dP = (P(y + 1e-4) - P(y - 1e-4)) / 2e-6
    d2P = (P(y + 1e-3) - 2 * sucio + P(y - 1e-3)) / 1e-10
    K.comprobar(f"  [{i}] precio sucio y corrido", abs(R["precio_sucio"] - sucio) < 1e-9 and abs(R["cupon_corrido"] - ai) < 1e-12,
                f"{R['precio_sucio']} vs {sucio}; {R['cupon_corrido']} vs {ai}")
    K.comprobar(f"  [{i}] D_mod = −P'/P y DV01", abs(R["d_mod"] + dP / sucio) < 1e-6 and abs(R["dv01"] + dP / 1e4) < 1e-7,
                f"{R['d_mod']} vs {-dP / sucio}")
    K.comprobar(f"  [{i}] D_mac = D_mod·(1 + y/f)", abs(R["d_macaulay"] - R["d_mod"] * (1 + y / 100 / f)) < 1e-10)
    K.comprobar(f"  [{i}] convexidad = P''/P (1e-3 rel.)", abs(R["convexidad"] - d2P / sucio) < 1e-3 * max(1, R["convexidad"]),
                f"{R['convexidad']} vs {d2P / sucio}")
    res2 = C.servir(m, "FIR-PRICE-001", {"cupon": cup, "frecuencia": f, "liquidacion": str(liq), "vencimiento": str(venc), "convencion": conv,
                                         "precio_limpio": R["precio_limpio"]})
    K.comprobar(f"  [{i}] precio → rendimiento devuelve y a 1e-8", res2["estado"].startswith("SERVED") and abs(res2["resultado"]["ytm_pct"] - y) < 1e-8,
                str(res2.get("resultado", res2))[:200])

# ============================================================ FIR-CURVE-001
print("FIR-CURVE-001")


def nss(t, b, lam):
    x1 = t / lam[0]
    y = b[0] + b[1] * (1 - np.exp(-x1)) / x1 + b[2] * ((1 - np.exp(-x1)) / x1 - np.exp(-x1))
    if len(lam) > 1:
        x2 = t / lam[1]
        y = y + b[3] * ((1 - np.exp(-x2)) / x2 - np.exp(-x2))
    return y


tau = np.array([0.25, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 20, 30])
for sem in (1, 2, 3):
    rng = np.random.default_rng(sem)
    y = nss(tau, [3.5, -1.5, 2.0, -2.5], [1.2, 6.0]) + rng.normal(0, 0.03, len(tau))
    t0 = time.time()
    res = C.servir(m, "FIR-CURVE-001", {"curva": {"fecha": "2026-11-13", "plazos": tau.tolist(), "rendimientos": y.tolist()}})
    dt = time.time() - t0
    if not K.comprobar(f"curva con ruido {sem}: servida ({dt:.1f} s)", res["estado"].startswith("SERVED"), str(res)[:300]):
        continue
    R = res["resultado"]
    pa = R["parametros"]
    bm, lm = [pa["beta0"], pa["beta1"], pa["beta2"], pa["beta3"]], [pa["lambda1"], pa["lambda2"]]
    sse_m = float(np.sum((nss(tau, bm, lm) - y) ** 2))
    K.comprobar(f"  [{sem}] RMSE publicado = el de sus parámetros", abs(math.sqrt(sse_m / len(tau)) * 100 - R["rmse_pb"]) < 1e-8)
    rng2 = np.random.default_rng(1000 + sem)
    mejor = math.inf
    for _ in range(300):
        x0 = np.r_[rng2.uniform(0.5, 6), rng2.uniform(-5, 5, 3), np.log(rng2.uniform(0.1, 30, 2))]
        try:
            o = optimize.least_squares(lambda x: nss(tau, x[:4], np.exp(x[4:])) - y, x0, method="lm", max_nfev=5000)
        except Exception:  # noqa: BLE001
            continue
        if o.x[0] > 0 and np.all(np.isfinite(o.x)):
            mejor = min(mejor, 2 * o.cost)
    K.comprobar(f"  [{sem}] 300 arranques propios no encuentran un mínimo mejor (SSE {sse_m:.6g} frente a {mejor:.6g})",
                sse_m <= mejor * (1 + 1e-6) + 1e-12)

# ============================================================ ACC-VAL-001
print("ACC-VAL-001")
from bloque_a.motor import servicio  # noqa: E402

base = servicio.CASOS_CONTROL["ACC-VAL-001"][0]["datos"][0]["valores"]
import copy  # noqa: E402

for nombre, cambio, params in [("caso base", {}, {}), ("deuda 900, β 0,7, g exp. 6 %", {"deuda_neta": 900.0, "beta": {"valor": 0.7, "fuente": "x"},
                                "crecimiento_explicito": {"valor": 6.0, "fuente": "x"}}, {"anios_explicitos": 8, "g_terminal": 2.0})]:
    v = copy.deepcopy(base)
    v.update(cambio)
    res = C.servir(m, "ACC-VAL-001", v, params)
    if not K.comprobar(f"ACC-VAL {nombre}: servida", res["estado"].startswith("SERVED"), str(res)[:300]):
        continue
    R = res["resultado"]
    ult = v["ejercicios"][-1]
    t = v["tasa_impositiva_legal"] / 100
    fcff0 = ult["ebit"] * (1 - t) + ult["amortizaciones"] - ult["capex"] - ult["variacion_circulante"]
    ke = v["rf"]["valor"] + v["beta"]["valor"] * v["prm"]["valor"]
    E, D = v["capitalizacion"]["valor"], v["deuda_neta"]
    w = (E * ke + D * v["coste_deuda_pct"] * (1 - t)) / (E + D) / 100
    g, gt, n = v["crecimiento_explicito"]["valor"] / 100, params.get("g_terminal", min(v["rf"]["valor"], 4)) / 100, params.get("anios_explicitos", 5)
    fl = [fcff0 * (1 + g) ** k for k in range(1, n + 1)]
    vp = sum(x / (1 + w) ** k for k, x in enumerate(fl, 1))
    vt = fl[-1] * (1 + gt) / (w - gt)
    ev = vp + vt / (1 + w) ** n
    K.comprobar(f"  WACC {w * 100:.6f} %, EV {ev:.6f} y valor del agregado = EV − deuda",
                abs(R["wacc_pct"] - w * 100) < 1e-10 and abs(R["ev"] - ev) < 1e-8 * ev and abs(R["valor_agregado"] - (ev - D)) < 1e-8 * ev,
                f"{R['wacc_pct']} {R['ev']} {R['valor_agregado']}")
    K.comprobar("  peso del VT", abs(R["peso_valor_terminal_pct"] - 100 * vt / (1 + w) ** n / ev) < 1e-9)

    def ev_g(gg):
        fl_ = [fcff0 * (1 + gg) ** k for k in range(1, n + 1)]
        return sum(x / (1 + w) ** k for k, x in enumerate(fl_, 1)) + fl_[-1] * (1 + gt) / (w - gt) / (1 + w) ** n

    gi = optimize.brentq(lambda gg: ev_g(gg) - (E + D), -0.9, 1.0, xtol=1e-14)
    K.comprobar(f"  DCF inverso: g implícito {gi * 100:.6f} %", abs(R["dcf_inverso"]["crecimiento_implicito_pct"] - gi * 100) < 1e-6,
                f"{R['dcf_inverso']['crecimiento_implicito_pct']}")
    sens = R["sensibilidad"]["valor_agregado"]
    w2 = w + 0.01

    def ev_wg(ww, gg_t):
        fl_ = [fcff0 * (1 + g) ** k for k in range(1, n + 1)]
        return sum(x / (1 + ww) ** k for k, x in enumerate(fl_, 1)) + fl_[-1] * (1 + gg_t) / (ww - gg_t) / (1 + ww) ** n

    K.comprobar("  sensibilidad: WACC + 1 pp y g − 0,5 pp", abs(sens[2][0] - (ev_wg(w2, gt - 0.005) - D)) < 1e-8 * ev, f"{sens[2][0]} vs {ev_wg(w2, gt - 0.005) - D}")
sys.exit(K.fin())
