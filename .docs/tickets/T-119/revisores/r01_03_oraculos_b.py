"""QA r01 de T-119 · oráculos independientes (2 de 2): PRV-PME, PRV-CF, ALT-HF y ALT-AUC.

 - PRV-PME-001: KS-PME con bucles; TIR resolviendo el VAN con `scipy.optimize.newton` en tiempo continuo (δ = ln(1+r));
   alfa directo resolviendo Σ FV_i·e^{−a·t_i} = 0 en a (definición de Gredil, Griffiths y Stucke), no vía ln(1 + TIR);
   PME+ por su definición (la inversión en el índice con distribuciones λ·D acaba con el mismo NAV) y su TIR.
 - PRV-CF-001: múltiplos y curva J a mano; TIR con varias raíces y sin raíz; Takahashi-Alexander con una recurrencia
   escrita desde el artículo (RC_t, RD_t = max(Y, (t/L)^B), NAV_t).
 - ALT-HF-001: Geltner + OLS HAC de `statsmodels` (Bartlett, L = ⌊4(T/100)^{2/9}⌋, sin corrección); coherencia con
   ACC-FACT-001 servida por el Motor con los mismos datos.
 - ALT-AUC-001: ventas repetidas (BMN) y hedónico con `statsmodels` OLS sobre datos propios con ruido, piezas con 2 y 3
   ventas y pares en el mismo año.
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
from scipy import optimize  # noqa: E402

K = C.Contador("r01_03 oráculos B")
m = C.motor()
rng = np.random.default_rng(119)


def ok(r):
    if r["estado"] == "RECHAZADO":
        print("   RECHAZADO:", r["detalle"][:300])
        return False
    return True


def tir_continua(t, f):
    """TIR anual por otra vía: raíz en δ del VAN continuo Σ f·e^{−δ t}, con Newton desde varios arranques."""
    def van(d):
        return float(np.sum(f * np.exp(-d * t)))
    for d0 in (0.05, 0.3, -0.2, 1.0):
        try:
            d = optimize.newton(van, d0, tol=1e-15, maxiter=500)
            if abs(van(d)) < 1e-9 * np.abs(f).sum():
                return math.exp(d) - 1
        except RuntimeError:
            pass
    return None


# ------------------------------------------------------------------ PRV-PME-001
print("PRV-PME-001")
fechas = pd.to_datetime(["2012-02-17", "2012-11-03", "2013-06-30", "2014-01-10", "2015-08-21", "2016-03-05", "2017-12-29",
                         "2019-04-11", "2020-09-30", "2021-06-15"])
Cc = np.array([30.0, 25, 20, 15, 5, 3, 0, 0, 2, 0])
Dd = np.array([0.0, 0, 1, 4, 12, 20, 35, 30, 18, 22])
f_nav, nav = pd.Timestamp("2022-03-31"), 17.5
niv_f = 100 * np.exp(np.cumsum(rng.normal(0.06, 0.15, len(fechas))))
niv_nav = float(niv_f[-1] * 1.07)
vp = {"moneda": "EUR", "flujos": [{"fecha": str(f.date()), "aportacion": float(c), "distribucion": float(d)}
                                  for f, c, d in zip(fechas, Cc, Dd)],
      "nav_final": {"fecha": "2022-03-31", "valor": nav},
      "indice": {"nombre": "I", "moneda": "EUR", "rentabilidad_total": True, "riesgo_comparable": "sí",
                 "niveles": [{"fecha": str(f.date()), "nivel": float(x)} for f, x in zip(fechas, niv_f)]
                 + [{"fecha": "2022-03-31", "nivel": niv_nav}, {"fecha": "2015-01-01", "nivel": 55.0}]}}
r = C.servir(m, "PRV-PME-001", vp, {"metodo": "PME+"})
if K.comprobar("servido", ok(r)):
    x = r["resultado"]
    num = den = 0.0
    for f, c, d, i_ in zip(fechas, Cc, Dd, niv_f):
        num += d * niv_nav / i_
        den += c * niv_nav / i_
    K.cerca("KS-PME", x["ks_pme_veces"], (num + nav) / den, 1e-12)
    K.cerca("TVPI", x["tvpi_veces"], (Dd.sum() + nav) / Cc.sum(), 1e-12)
    K.cerca("DPI", x["dpi_veces"], Dd.sum() / Cc.sum(), 1e-12)
    t = np.array([(f - fechas[0]).days / 365 for f in list(fechas) + [f_nav]])
    neto = np.append(Dd - Cc, nav)
    K.cerca("TIR % (Newton en tiempo continuo)", x["tir_pct"], tir_continua(t, neto) * 100, 1e-9)
    fv = np.append((Dd - Cc) * niv_nav / niv_f, nav)
    a = optimize.brentq(lambda a_: float(np.sum(fv * np.exp(-a_ * t))), -2, 2, xtol=1e-15)
    K.cerca("alfa directo % anual (raíz en a de Σ FV·e^{−a t})", x["alfa_directo_pct_anual"], a * 100, 1e-9)
    lam = x["pme_plus"]["lambda"]
    final_indice = sum((c - lam * d) * niv_nav / i_ for c, d, i_ in zip(Cc, Dd, niv_f))
    K.cerca("PME+: con λ, la inversión en el índice acaba con el NAV del fondo", final_indice, nav, 1e-10)
    tir_i = tir_continua(t, np.append(lam * Dd - Cc, nav))
    K.cerca("PME+: TIR del índice %", x["pme_plus"]["tir_indice_pct"], tir_i * 100, 1e-9)
    K.cerca("PME+: diferencial de TIR", x["pme_plus"]["diferencial_tir_pct"], x["tir_pct"] - tir_i * 100, 1e-9)
    K.comprobar("KS-PME > 1 ⇔ alfa directo > 0 (coherencia de signo)", (x["ks_pme_veces"] > 1) == (x["alfa_directo_pct_anual"] > 0))
# NAV en la misma fecha que el último flujo
vp2 = {**vp, "nav_final": {"fecha": "2021-06-15", "valor": nav}}
r = C.servir(m, "PRV-PME-001", vp2, {})
if K.comprobar("NAV el día del último flujo: servido", ok(r)):
    x = r["resultado"]
    f_ = niv_f[-1] / niv_f
    K.cerca("KS-PME (NAV el día del último flujo)", x["ks_pme_veces"], ((Dd * f_).sum() + nav) / (Cc * f_).sum(), 1e-12)
    t2 = np.array([(f - fechas[0]).days / 365 for f in fechas])
    n2 = (Dd - Cc).copy()
    n2[-1] += nav
    K.cerca("TIR (NAV sumado al último flujo)", x["tir_pct"], tir_continua(t2, n2) * 100, 1e-9)
    K.comprobar("sin PME+ si no se pide", x["pme_plus"] is None)

# ------------------------------------------------------------------ PRV-CF-001
print("PRV-CF-001")
vcf = {"compromiso": 120.0, "flujos": vp["flujos"], "navs": [{"fecha": "2018-12-31", "valor": 60.0}, {"fecha": "2022-03-31", "valor": nav}],
       "vida_anios": 15, "referencia_cosecha": {"tvpi_mediana": 1.6, "tir_mediana": 0.11}}
tasas, bow, g = [0.25, 0.3, 0.4, 0.5, 0.5, 0.6], 3.2, 0.11
r = C.servir(m, "PRV-CF-001", vcf, {"tasas_aportacion": tasas, "bow": bow, "crecimiento": g})
if K.comprobar("servido", ok(r)):
    x = r["resultado"]
    K.cerca("TIR %", x["tir_pct"], tir_continua(t, neto) * 100, 1e-9)
    K.cerca("TVPI", x["tvpi_veces"], (Dd.sum() + nav) / Cc.sum(), 1e-12)
    K.cerca("DPI", x["dpi_veces"], Dd.sum() / Cc.sum(), 1e-12)
    K.cerca("RVPI", x["rvpi_veces"], nav / Cc.sum(), 1e-12)
    ac = 0.0
    curva = []
    for c, d in zip(Cc, Dd):
        ac += d - c
        curva.append(ac)
    K.comprobar("curva J punto a punto", all(abs(a["flujo_neto_acumulado"] - b) < 1e-9 for a, b in zip(x["curva_j"]["serie"], curva)))
    K.cerca("curva J: mínimo sobre compromiso", x["curva_j"]["minimo_sobre_compromiso"], min(curva) / 120, 1e-12)
    K.comprobar("curva J: fecha del mínimo", x["curva_j"]["fecha_minimo"] == str(fechas[int(np.argmin(curva))].date()))
    # Takahashi y Alexander (2002): edad = años completos desde el primer flujo hasta el NAV
    edad = int((f_nav - fechas[0]).days // 365)
    pic, nv, esperado = Cc.sum(), nav, []
    for anio in range(edad + 1, 15 + 1):
        rc = tasas[anio - 1] if anio <= len(tasas) else tasas[-1]
        c_t = rc * max(120.0 - pic, 0.0)
        rd = max(0.0, (anio / 15) ** bow)
        d_t = rd * nv * (1 + g)
        nv = nv * (1 + g) + c_t - d_t
        pic += c_t
        esperado.append((anio, c_t, d_t, nv))
    pr = x["proyeccion"]
    K.comprobar(f"proyección: edad {pr['edad_anios']} = {edad}, {len(pr['serie'])} años", pr["edad_anios"] == edad and len(pr["serie"]) == len(esperado))
    K.comprobar("proyección T-A año a año (aportación, distribución, NAV)",
                all(s["anio_vida"] == e[0] and abs(s["aportacion"] - e[1]) < 1e-9 and abs(s["distribucion"] - e[2]) < 1e-9
                    and abs(s["nav"] - e[3]) < 1e-9 for s, e in zip(pr["serie"], esperado)))
    K.cerca("proyección: el último año se distribuye todo el NAV (RD = 1): queda solo la aportación de ese año",
            pr["serie"][-1]["nav"], pr["serie"][-1]["aportacion"], 1e-9)
    d_fin = Dd.sum() + sum(e[2] for e in esperado)
    K.cerca("proyección: TVPI final", pr["tvpi_final_veces"], (d_fin + esperado[-1][3]) / pic, 1e-10)
    K.cerca("referencia: TVPI − mediana", x["referencia_ingenua"]["diferencia_tvpi"], (Dd.sum() + nav) / Cc.sum() - 1.6, 1e-10)
    K.cerca("referencia: TIR − mediana (pp)", x["referencia_ingenua"]["diferencia_tir_pct"], x["tir_pct"] - 11.0, 1e-10)

print("   TIR con varias raíces y sin raíz")


def cf(flujos, navv, fecha_nav):
    return {"compromiso": 1000.0, "flujos": [{"fecha": f, "aportacion": float(a), "distribucion": float(d)} for f, a, d in flujos],
            "navs": [{"fecha": fecha_nav, "valor": navv}]}


# −100, +230, −132 a 0, 1 y 2 años (365 d): raíces exactas 10 % y 20 %
r = C.servir(m, "PRV-CF-001", cf([("2021-01-01", 100, 0), ("2022-01-01", 0, 230), ("2023-01-01", 132, 0)], 0.0, "2023-01-01"), {})
x = r["resultado"]
print(f"     dos raíces (10 % y 20 %): tir_pct = {x['tir_pct']}; limitaciones: {[s for s in r['limitaciones'] if 'TIR' in s]}")
K.comprobar("dos raíces (10 % y 20 %): avisa de múltiples soluciones", any("múltiples" in s for s in r["limitaciones"]))
K.comprobar("dos raíces: no afirma que no hay TIR cuando hay dos", not any("sin TIR" in s for s in r["limitaciones"]),
            str([s for s in r["limitaciones"] if "TIR" in s]))
# −100, +230, −133: sin raíz real
r = C.servir(m, "PRV-CF-001", cf([("2021-01-01", 100, 0), ("2022-01-01", 0, 230), ("2023-01-01", 133, 0)], 0.0, "2023-01-01"), {})
K.comprobar("sin raíz real: TIR null y declarado", r["resultado"]["tir_pct"] is None and any("sin TIR" in s for s in r["limitaciones"]))
# tres cambios de signo con tres raíces en el rango: 5 %, 15 % y 40 % (coeficientes del polinomio en 1/(1+r))
raices = np.array([1 / 1.05, 1 / 1.15, 1 / 1.40])
pol = np.poly(raices)[::-1] * 1000          # a0 + a1 v + a2 v² + a3 v³
fl = [(f"{2020 + i}-01-01", max(-a, 0.0), max(a, 0.0)) for i, a in enumerate(pol)]
fl = [(f"2021-01-0{1}", fl[0][1], fl[0][2]), ("2022-01-01", fl[1][1], fl[1][2]), ("2023-01-01", fl[2][1], fl[2][2])]
r = C.servir(m, "PRV-CF-001", cf(fl, float(pol[3]) if pol[3] > 0 else 0.0, "2024-01-01") if pol[3] > 0 else
             cf(fl + [("2024-01-01", -pol[3], 0.0)], 0.0, "2024-01-01"), {})
x = r["resultado"]
print(f"     tres raíces (5, 15 y 40 %): tir_pct = {x['tir_pct']}; {[s for s in r['limitaciones'] if 'TIR' in s]}")
K.comprobar("tres raíces: la servida es una de ellas y se avisa", x["tir_pct"] is not None and min(abs(x["tir_pct"] - e) for e in (5, 15, 40)) < 1e-6
            and any("múltiples" in s for s in r["limitaciones"]))
# sólo aportaciones
r = C.servir(m, "PRV-CF-001", cf([("2021-01-01", 100, 0), ("2022-01-01", 50, 0)], 0.0, "2022-06-01"), {})
K.comprobar("sin cambio de signo: TIR null y declarado", r["resultado"]["tir_pct"] is None and any("sin cambio de signo" in s for s in r["limitaciones"]))
# TIR fuera del rango (pérdida casi total en poco tiempo y ganancia enorme)
r = C.servir(m, "PRV-CF-001", cf([("2021-01-01", 100, 0)], 1e-4, "2022-01-01"), {})
print(f"     pérdida del 99,9999 % en un año: tir_pct = {r['resultado']['tir_pct']}; {[s for s in r['limitaciones'] if 'TIR' in s]}")
r = C.servir(m, "PRV-CF-001", cf([("2021-01-01", 100, 0)], 5000.0, "2022-01-01"), {})
print(f"     ×50 en un año (TIR 4 900 %): tir_pct = {r['resultado']['tir_pct']}; {[s for s in r['limitaciones'] if 'TIR' in s]}")
r = C.servir(m, "PRV-CF-001", cf([("2021-01-01", 100, 0)], 130.0, "2021-01-31"), {})
print(f"     +30 % en 30 días (TIR anual ≈ {(1.3 ** (365 / 30) - 1) * 100:.0f} %): tir_pct = {r['resultado']['tir_pct']}; "
      f"{[s for s in r['limitaciones'] if 'TIR' in s]}")

# ------------------------------------------------------------------ ALT-HF-001
print("ALT-HF-001")
nmes = 97
fm = pd.date_range("2016-01-31", periods=nmes, freq="ME")
FH = ["MKT", "SMB", "BONO10A", "CREDITO", "PTFSBD", "PTFSFX", "PTFSCOM"]
Fm = rng.normal(0.3, [4, 2.5, 1.5, 1.0, 15, 18, 14], (nmes, 7))
verd = 0.35 + Fm @ np.array([0.4, 0.2, -0.1, 0.5, 0.02, 0.03, -0.01]) + rng.normal(0, 1.2, nmes)
obs = np.empty(nmes)
obs[0] = verd[0]
for i in range(1, nmes):
    obs[i] = 0.55 * verd[i] + 0.45 * obs[i - 1]                     # suavizado
rf = rng.uniform(0.0, 0.4, nmes)
vh = {"serie": [{"fecha": str(f.date()), "r": float(obs[i]), "rf": float(rf[i]), **{nb: float(Fm[i, j]) for j, nb in enumerate(FH)}}
                for i, f in enumerate(fm)]}
for des in (True, False):
    r = C.servir(m, "ALT-HF-001", vh, {"desuavizar": des})
    if not K.comprobar(f"desuavizar={des} servido", ok(r)):
        continue
    x = r["resultado"]
    if des:
        phi = sm.OLS(obs[1:], sm.add_constant(obs[:-1])).fit().params[1]
        K.cerca("φ del AR(1) (OLS de statsmodels)", x["desuavizado"]["phi"], phi, 1e-10)
        y = (obs[1:] - phi * obs[:-1]) / (1 - phi) - rf[1:]
        XX = Fm[1:]
    else:
        y, XX = obs - rf, Fm
    L = math.floor(4 * (len(y) / 100) ** (2 / 9))
    fit = sm.OLS(y, sm.add_constant(XX)).fit(cov_type="HAC", cov_kwds={"maxlags": L, "use_correction": False})
    K.cerca(f"des={des} α del periodo %", x["alfa_periodo_pct"], fit.params[0], 1e-9)
    K.cerca(f"des={des} α anual % (compuesto)", x["alfa_anual_pct"], ((1 + fit.params[0] / 100) ** 12 - 1) * 100, 1e-9)
    K.cerca(f"des={des} t(α) Newey-West", x["t_alfa"], fit.tvalues[0], 1e-7)
    for j, nb in enumerate(FH):
        K.cerca(f"des={des} β {nb}", x["betas"][nb]["beta"], fit.params[j + 1], 1e-9)
        K.cerca(f"des={des} t {nb}", x["betas"][nb]["t"], fit.tvalues[j + 1], 1e-7)
    K.cerca(f"des={des} R²", x["r2"], fit.rsquared, 1e-10)
    K.comprobar(f"des={des} n de la regresión", x["n"] == len(y) and x["rezagos_nw"] == L)
    K.cerca(f"des={des} cartera pasiva de factores (media)", x["referencia_ingenua"]["rentabilidad_media_periodo_pct"],
            float(fit.params[1:] @ XX.mean(axis=0)), 1e-9)
# coherencia con ACC-FACT-001 servida por el Motor con los mismos datos (factores de ACC-FACT: FF5 + UMD)
from bloque_a.motor import servicio  # noqa: E402
va, pa = C.caso("ACC-FACT-001", 0)
print("   claves de ACC-FACT-001:", sorted(va), pa, "factores:", sorted(va["factores"]))
nf = sorted(va["factores"])
nobs = len(va["fechas"])
Fa = rng.normal(0.2, 3, (nobs, len(nf)))
ra = 0.2 + Fa @ rng.normal(0.3, 0.3, len(nf)) + rng.normal(0, 1, nobs)
rfa = rng.uniform(0, 0.3, nobs)
va2 = {**va, "rendimientos": [float(v) for v in ra], "rf": [float(v) for v in rfa], "factores": {nb: [float(v) for v in Fa[:, j]] for j, nb in enumerate(nf)}}
va2.pop("en_exceso", None)
ra_ = C.servir(m, "ACC-FACT-001", va2, pa)
vh2 = {"serie": [{"fecha": va["fechas"][i], "r": float(ra[i]), "rf": float(rfa[i]), **{nb: float(Fa[i, j]) for j, nb in enumerate(nf)}}
                 for i in range(nobs)]}
nf_acc = list(ra_["resultado"]["factores"]) if ok(ra_) else nf      # los que ACC-FACT-001 usa de verdad (FF5 + UMD)
rh_ = C.servir(m, "ALT-HF-001", {"serie": [{k: v_ for k, v_ in f.items() if k in ("fecha", "r", "rf", *nf_acc)} for f in vh2["serie"]]},
               {"factores": nf_acc, "desuavizar": False})
if K.comprobar("ACC-FACT-001 y ALT-HF-001 servidas con los mismos datos", ok(ra_) and ok(rh_)):
    a, h = ra_["resultado"], rh_["resultado"]
    print("   claves ACC-FACT:", sorted(a)[:12])
    K.cerca("coherencia: α del periodo", h["alfa_periodo_pct"], a["alfa_periodo_pct"], 1e-12)
    K.cerca("coherencia: t(α)", h["t_alfa"], a["t_alfa"], 1e-12)
    K.cerca("coherencia: R²", h["r2"], a["r2"], 1e-12)
    K.comprobar("coherencia: betas", all(abs(h["betas"][nb]["beta"] - a["betas"][nb]["beta"]) < 1e-12 for nb in nf_acc))

# ------------------------------------------------------------------ ALT-AUC-001
print("ALT-AUC-001")
P, a0 = 13, 2008
beta_v = np.concatenate([[0], np.cumsum(rng.normal(0.06, 0.12, P - 1))])
trans = []
piezas = 420
for i in range(piezas):
    nv = 3 if i % 4 == 0 else 2
    calidad, tam = rng.normal(0, 1), rng.uniform(0, 3)
    base = 5 + 0.8 * calidad + 0.3 * tam
    anios = sorted(rng.choice(P, nv, replace=(i % 17 == 0)))          # algunas con dos ventas el mismo año
    for k, a in enumerate(anios):
        lp = base + beta_v[a] + rng.normal(0, 0.25)
        trans.append({"id_pieza": f"Z{i}", "fecha": f"{a0 + a}-{1 + (i + k) % 12:02d}-{1 + (i * 7 + k) % 27:02d}",
                      "precio": float(math.exp(lp)), "caracteristicas": {"calidad": float(calidad), "tam": float(tam)}})
# ventas únicas para el hedónico
for i in range(150):
    calidad, tam, a = rng.normal(0, 1), rng.uniform(0, 3), int(rng.integers(P))
    trans.append({"id_pieza": f"U{i}", "fecha": f"{a0 + a}-06-15", "precio": float(math.exp(5 + 0.8 * calidad + 0.3 * tam + beta_v[a] + rng.normal(0, 0.25))),
                  "caracteristicas": {"calidad": float(calidad), "tam": float(tam)}})
orden = rng.permutation(len(trans))
trans = [trans[i] for i in orden]                                     # desordenadas
vau = {"categoria": "arte", "transacciones": trans, "referencia": {"inflacion_anual": 0.025, "rv_global_anual": 0.08}}
df = pd.DataFrame([{"id": t["id_pieza"], "f": pd.Timestamp(t["fecha"]), "lp": math.log(t["precio"]), **t["caracteristicas"]} for t in trans])
df["per"] = df.f.dt.year - a0
# pares consecutivos por pieza
filas, yv = [], []
desc = 0
for _, g_ in df.sort_values(["id", "f"], kind="stable").groupby("id", sort=False):
    g_ = g_.reset_index(drop=True)
    for j in range(1, len(g_)):
        if g_.per[j] == g_.per[j - 1]:
            desc += 1
            continue
        fila = np.zeros(P)
        fila[g_.per[j]] += 1
        fila[g_.per[j - 1]] -= 1
        filas.append(fila[1:])
        yv.append(g_.lp[j] - g_.lp[j - 1])
Mx, yv = np.array(filas), np.array(yv)
fit_vr = sm.OLS(yv, Mx).fit()
ind_vr = 100 * np.exp(np.concatenate([[0], fit_vr.params]))
dum = pd.get_dummies(df.per, prefix="p", drop_first=True).astype(float)
fit_he = sm.OLS(df.lp, sm.add_constant(pd.concat([df[["calidad", "tam"]], dum], axis=1))).fit()
ind_he = 100 * np.exp(np.concatenate([[0], fit_he.params[3:].to_numpy()]))
for metodo, ind, fit in (("ventas_repetidas", ind_vr, fit_vr), ("hedonico", ind_he, fit_he)):
    r = C.servir(m, "ALT-AUC-001", vau, {"metodo": metodo, "comisiones": 0.2})
    if not K.comprobar(f"{metodo} servido", ok(r)):
        continue
    x = r["resultado"]
    K.comprobar(f"{metodo}: pares {x['n_pares']} = {len(yv)} y descartados {x['pares_descartados_mismo_periodo']} = {desc}",
                x["n_pares"] == len(yv) and x["pares_descartados_mismo_periodo"] == desc)
    K.comprobar(f"{metodo}: índice periodo a periodo (statsmodels)", len(x["indice"]) == P and all(
        abs(a["indice"] - b) < 1e-7 * b and a["periodo"] == a0 + i for i, (a, b) in enumerate(zip(x["indice"], ind))),
        str([(a["indice"], b) for a, b in zip(x["indice"], ind)][:3]))
    bruta = ((ind[-1] / ind[0]) ** (1 / (P - 1)) - 1) * 100
    K.cerca(f"{metodo}: rentabilidad anual bruta %", x["rentabilidad_anual_bruta_pct"], bruta, 1e-8)
    K.cerca(f"{metodo}: neta % (una compraventa al 20 %)", x["rentabilidad_anual_neta_pct"], ((ind[-1] / ind[0] * 0.8) ** (1 / (P - 1)) - 1) * 100, 1e-8)
    K.cerca(f"{metodo}: volatilidad %", x["volatilidad_pct"], np.std(ind[1:] / ind[:-1] - 1, ddof=1) * 100, 1e-8)
    K.cerca(f"{metodo}: desviación residual % (√(SSR/gl))", x["dispersion"]["desviacion_residual_pct"], math.sqrt(fit.mse_resid) * 100, 1e-8)
    K.cerca(f"{metodo}: real anual %", x["referencia_ingenua"]["rentabilidad_real_anual_pct"], ((1 + bruta / 100) / 1.025 - 1) * 100, 1e-8)
    K.cerca(f"{metodo}: exceso sobre RV global", x["referencia_ingenua"]["exceso_sobre_rv_global_pct"], bruta - 8.0, 1e-8)
    otro = ind_he if metodo == "ventas_repetidas" else ind_vr
    K.cerca(f"{metodo}: segunda vía (el otro método)", x["segunda_via"]["rentabilidad_anual_bruta_pct"], ((otro[-1] / otro[0]) ** (1 / (P - 1)) - 1) * 100, 1e-8)
    K.comprobar(f"{metodo}: base 100", x["indice"][0]["indice"] == 100.0)
print(f"   índice verdadero final {100 * math.exp(beta_v[-1]):.1f}; VR {ind_vr[-1]:.1f}; hedónico {ind_he[-1]:.1f}")
sys.exit(K.fin())
