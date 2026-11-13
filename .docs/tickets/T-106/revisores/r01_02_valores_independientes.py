"""QA r01 de T-106 · Recalcula con otra implementación (numpy/scipy/statsmodels, escrita por el revisor a partir de la ficha)
los resultados de las fichas, con datos distintos de los de los casos de control.

Cubre: MON-YLD (conversiones y cubierto), MON-EXP (bootstrap de la senda y nodos que no reproduce), IDX-ERP (Grinold-Kroner),
IDX-CONC (HHI, N_ef, top-n, HHI sectorial), DER-VRP (réplica VIX), DER-SKEW (SVI y deltas 25Δ), DER-ROLL (carry y roll),
TCV-TP (ACM con statsmodels sobre otra curva afín, con innovaciones gaussianas y prima verdadera conocida).

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r01_02_valores_independientes.py [RAIZ]
"""
from __future__ import annotations

import math
import sys
import warnings
from pathlib import Path

import numpy as np
from scipy import optimize
from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

M = C.preparar(sys.argv[1] if len(sys.argv) > 1 else None)
S = M["servicio"]
warnings.simplefilter("ignore")


def fn(ficha):
    return S.IMPLEMENTADAS[ficha]["fn"]


def cerca(a, b, tol):
    return a is not None and b is not None and abs(float(a) - float(b)) <= tol


# ------------------------------------------------------------------ MON-YLD-001
seg = [{"segmento": "letras", "divisa": "EUR", "plazo_meses": 6, "dias": 182, "fecha": "2026-11-10",
        "convencion": "descuento_360", "valor": 0.0241},
       {"segmento": "pagares", "divisa": "EUR", "plazo_meses": 6, "dias": 182, "fecha": "2026-11-10",
        "convencion": "simple_360", "valor": 0.0275},
       {"segmento": "tbill", "divisa": "USD", "plazo_meses": 6, "dias": 182, "fecha": "2026-11-10",
        "convencion": "simple_360", "valor": 0.0420}]
r, _ = fn("MON-YLD-001")({"valores": {"segmentos": seg, "cobertura": {"divisa_destino": "EUR", "segmentos": {
    "tbill · USD · 6m": {"spot": 1.08, "forward": 1.0965}}}}, "series": {}, "series_rol": {}}, {"cobertura": True})
t = 182
P = 1 - 0.0241 * t / 360
fila = r["tabla"]["letras · EUR · 6m"]
C.informe("MON-YLD descuento → precio", cerca(fila["precio"], P, 1e-14))
C.informe("MON-YLD descuento → simple Act/365 = (1/P − 1)·365/t", cerca(fila["simple_365"], (1 / P - 1) * 365 / t, 1e-14))
C.informe("MON-YLD descuento → TAE = (1/P)^(365/t) − 1", cerca(fila["tae"], (1 / P) ** (365 / t) - 1, 1e-14))
C.informe("MON-YLD descuento → MMY Act/360", cerca(fila["simple_360"], (1 / P - 1) * 360 / t, 1e-14))
i = 0.0275
fp = r["tabla"]["pagares · EUR · 6m"]
C.informe("MON-YLD simple i → TAE = (1 + i·t/base)^(365/t) − 1", cerca(fp["tae"], (1 + i * t / 360) ** (365 / t) - 1, 1e-14))
C.informe("MON-YLD MMY Act/360 ↔ Act/365 (= i·365/360)", cerca(fp["simple_365"], i * 365 / 360, 1e-14))
dif = ((1 + i * t / 360) ** (365 / t) - 1 - ((1 / P) ** (365 / t) - 1)) * 1e4
C.informe("MON-YLD diferencial pagarés − letras en pb (TAE)", cerca(r["diferenciales_pb"].get("letras − pagares · EUR · 6m",
          -r["diferenciales_pb"].get("pagares − letras · EUR · 6m", 0)), -dif, 1e-9), str(r["diferenciales_pb"]))
bruto = (1 + 0.042 * t / 360) * 1.08 / 1.0965
cub = r["rendimiento_cubierto"]["tbill · USD · 6m"]
C.informe("MON-YLD cubierto = (1 + i·t/base)·(S/F) − 1, TAE", cerca(cub["rendimiento_periodo"], bruto - 1, 1e-14)
          and cerca(cub["tae"], bruto ** (365 / t) - 1, 1e-14))

# ------------------------------------------------------------------ MON-EXP-001
# Curva OIS (Act/360) con la senda escalonada de la ficha; bootstrap propio: un tramo de tipo a un día por reunión.
fecha = np.datetime64("2026-11-12")
reun = [np.datetime64(x) for x in ("2026-12-17", "2027-02-04", "2027-04-29", "2027-07-22", "2027-10-28")]
cortes = [0] + [int((m - fecha).astype(int)) for m in reun]
oficial, dif_est = 0.0200, 0.0008
r0 = oficial - dif_est
senda_verdad = [r0, r0 - 0.0025, r0 - 0.0050, r0 - 0.0050, r0 - 0.0075, r0 - 0.0075]   # una bajada, otra, pausa…
dias_nodo = [cortes[1] + 10, cortes[2] + 10, cortes[3] + 10, cortes[4] + 10, cortes[5] + 30]


def factor(d):
    lg = 0.0
    for k in range(len(cortes)):
        a = cortes[k]
        b = cortes[k + 1] if k + 1 < len(cortes) else 10 ** 9
        if a >= d:
            break
        lg += (min(b, d) - a) * math.log1p(senda_verdad[k] / 360)
    return math.exp(lg)


curva = [{"dias": d, "tipo": (factor(d) - 1) * 360 / d} for d in dias_nodo]
v = {"fecha": "2026-11-12", "base_curva": 360, "curva": curva, "tipo_oficial": oficial, "diferencial_estable": dif_est,
     "reuniones": [str(m) for m in reun]}
r, lim = fn("MON-EXP-001")({"valores": v, "series": {}, "series_rol": {}}, {})
obt = [s["tipo_mercado_implicito"] for s in r["senda"]]
C.informe("MON-EXP recupera la senda escalonada (bootstrap propio)", np.allclose(obt, senda_verdad[1:], atol=1e-12),
          f"{np.round(np.array(obt) * 1e4, 4)} vs {np.round(np.array(senda_verdad[1:]) * 1e4, 4)} pb")
mov = [s["movimientos_en_reunion"] for s in r["senda"]]
C.informe("MON-EXP movimientos por reunión = Δ/25 pb", np.allclose(mov, [-1, -1, 0, -1, 0], atol=1e-9), str(np.round(mov, 6)))
# Curva plana COTIZADA (todos los nodos al tipo vigente, como la daría una pantalla OIS): ¿probabilidad 0?
plana = {**v, "curva": [{"dias": d, "tipo": r0} for d in dias_nodo]}
rp, _ = fn("MON-EXP-001")({"valores": plana, "series": {}, "series_rol": {}}, {})
movp = [s["movimientos_en_reunion"] for s in rp["senda"]]
C.informe("MON-EXP curva OIS cotizada plana al tipo vigente ⇒ movimientos 0 (lectura literal de la Verificación)",
          max(abs(x) for x in movp) < 1e-6, f"movimientos = {np.round(movp, 4)} (cambio acumulado "
          f"{np.round([s['cambio_vs_vigente_pb'] for s in rp['senda']], 2)} pb)")
# Ruido de cotización realista (redondeo de las cotizaciones OIS a 0,1 pb) sobre la curva exacta anterior
ruido = {**v, "curva": [{"dias": n["dias"], "tipo": round(n["tipo"], 5)} for n in curva]}
rr_, _ = fn("MON-EXP-001")({"valores": ruido, "series": {}, "series_rol": {}}, {})
err = max(abs(s["tipo_mercado_implicito"] - t) for s, t in zip(rr_["senda"], senda_verdad[1:])) * 1e4
C.informe("MON-EXP estable ante el redondeo de las cotizaciones a 0,1 pb (error de la senda < 1 pb)", err < 1,
          f"error máx. de la senda {err:.2f} pb; movimientos {np.round([s['movimientos_en_reunion'] for s in rr_['senda']], 2)}")
# Nodos redundantes del caso de control «la senda reproduce los forwards de entrada»
caso = S.CASOS_CONTROL["MON-EXP-001"][1]
rc, _ = fn("MON-EXP-001")(C.entrada(caso), dict(caso["parametros"]))
red = rc["verificacion"]["nodos_redundantes"]
peor = max((abs(x["tipo_nodo"] - x["tipo_senda"]) * 1e4 for x in red), default=0.0)
C.informe("MON-EXP caso de control: la senda reproduce TODOS los nodos de entrada (también los que no fijan tramo)",
          peor < 1e-6, f"{len(red)} nodo(s) redundante(s) no reproducido(s); desajuste máx. {peor:.3f} pb; "
          f"error_reproduccion_nodos_max (solo los usados) = {rc['verificacion']['error_reproduccion_nodos_max']:.2e}")

# ------------------------------------------------------------------ IDX-ERP-001
caso = S.CASOS_CONTROL["IDX-ERP-001"][1]
ent = C.entrada(caso)
ent["valores"].update({"rentabilidad_dividendo": 0.021, "recompras_netas": 0.012, "multiplo_actual": 31.0,
                       "rf": {"valor": 0.027, "plazo_anios": 7, "divisa": "EUR"}})
r, _ = fn("IDX-ERP-001")(ent, {"lambda_reversion": 0.3, "N": 7})
hist = np.array([h["valor"] for h in ent["valores"]["historia_multiplo"]])
med = float(np.median(hist))
m_obj = 31.0 + 0.3 * (med - 31.0)
er = 0.021 + 0.012 + 0.015 + 0.02 + ((m_obj / 31.0) ** (1 / 7) - 1)
C.informe("IDX-ERP Grinold-Kroner a mano (λ = 0,3, N = 7)", cerca(r["er_nominal"]["IDX-SINT"], er, 1e-14),
          f"{r['er_nominal']['IDX-SINT']:.10f} vs {er:.10f}")
C.informe("IDX-ERP real = nominal − π^e y prima = E[R] − r_f", cerca(r["er_real"]["IDX-SINT"], er - 0.02, 1e-14)
          and cerca(r["prima_rf"]["IDX-SINT"], er - 0.027, 1e-14))
# λ = 1: el múltiplo vuelve entero a la mediana
ent["valores"]["rf"] = {"valor": 0.027, "plazo_anios": 10, "divisa": "EUR"}
r1, _ = fn("IDX-ERP-001")(ent, {"lambda_reversion": 1.0, "N": 10})
C.informe("IDX-ERP λ = 1 ⇒ %Δ múltiplo = (mediana/actual)^(1/N) − 1",
          cerca(r1["bloques"]["IDX-SINT"]["cambio_valoracion"], (med / 31.0) ** 0.1 - 1, 1e-14))

# ------------------------------------------------------------------ IDX-CONC-001
rng = np.random.default_rng(7)
w = rng.dirichlet(np.ones(37) * 0.4)
w = w / w.sum()
comp = {"fecha": "2026-10-31", "componentes": [{"id": f"C{j}", "peso": float(x), "sector": f"S{j % 5}"} for j, x in enumerate(w)]}
r, _ = fn("IDX-CONC-001")({"valores": {"composicion": comp}, "series": {}, "series_rol": {}}, {"top_n": 7})
hhi = float(np.sum(w ** 2))
sect = np.array([w[np.arange(37) % 5 == s].sum() for s in range(5)])
C.informe("IDX-CONC HHI = Σw² y N_ef = 1/HHI", cerca(r["hhi"], hhi, 1e-14) and cerca(r["n_ef"], 1 / hhi, 1e-10))
C.informe("IDX-CONC peso de los 7 mayores", cerca(r["peso_top_n"], float(np.sort(w)[::-1][:7].sum()), 1e-14))
C.informe("IDX-CONC HHI sectorial", cerca(r["hhi_sectorial"], float(np.sum(sect ** 2)), 1e-14))
# Pesos realistas publicados en % con 2 decimales (suman 100,00 % ± redondeo): ¿se aceptan?
wp = np.round(w * 100, 2)
wp[-1] += round(100 - wp.sum(), 2)
comp2 = {"fecha": "2026-10-31", "componentes": [{"id": f"C{j}", "peso": float(x) / 100} for j, x in enumerate(wp)]}
try:
    fn("IDX-CONC-001")({"valores": {"composicion": comp2}, "series": {}, "series_rol": {}}, {})
    ok, det = True, f"suma = {sum(float(x) / 100 for x in wp)!r}"
except M["ErrorFicha"] as e:
    ok, det = False, str(e)[:140]
C.informe("IDX-CONC acepta pesos publicados al 0,01 % que suman 100 % (suma en coma flotante)", ok, det)

# ------------------------------------------------------------------ DER-VRP-001 (réplica libre de modelo)
caso = S.CASOS_CONTROL["DER-VRP-001"][2]
ent = C.entrada(caso)
sig, F0, rr, dias = 0.31, 102.0, 0.035, 30
T = dias / 365
K = np.arange(40.0, 200.0, 2.5)


def black(F, K_, s, T_, call):
    d1 = (math.log(F / K_) + 0.5 * s * s * T_) / (s * math.sqrt(T_))
    d2 = d1 - s * math.sqrt(T_)
    return F * norm.cdf(d1) - K_ * norm.cdf(d2) if call else K_ * norm.cdf(-d2) - F * norm.cdf(-d1)


k0 = float(K[K <= F0][-1])
Q = [math.exp(-rr * T) * (black(F0, k, sig, T, k > k0) if k != k0 else (black(F0, k, sig, T, True) + black(F0, k, sig, T, False)) / 2)
     for k in K]
dK = np.gradient(K)
dK[0], dK[-1] = K[1] - K[0], K[-1] - K[-2]
var_vix = 2 / T * np.sum(dK / K ** 2 * math.exp(rr * T) * np.array(Q)) - (F0 / k0 - 1) ** 2 / T
ent["valores"]["cesta_opciones"] = {"strikes": [float(x) for x in K], "q": [float(x) for x in Q], "forward": F0,
                                    "tipo_interes": rr, "dias": dias}
r, _ = fn("DER-VRP-001")(ent, {"prevision_rv": "realizada_pasada"})
C.informe("DER-VRP réplica = fórmula VIX (implementación propia)",
          cerca(r["replica"]["sigma_imp_replica_pct"], math.sqrt(var_vix) * 100, 1e-10),
          f"{r['replica']['sigma_imp_replica_pct']:.8f} vs {math.sqrt(var_vix) * 100:.8f}")
C.informe("DER-VRP réplica ≈ σ de la sonrisa plana (banda de discretización 0,5 puntos)",
          abs(r["replica"]["sigma_imp_replica_pct"] - sig * 100) < 0.5, f"{r['replica']['sigma_imp_replica_pct']:.4f} vs {sig * 100}")

# ------------------------------------------------------------------ DER-SKEW-001 (SVI y deltas)
x_true = np.array([0.012, 0.09, -0.55, 0.03, 0.22])
Tm = 0.25
kk = np.linspace(-0.6, 0.45, 23)
a, b, rho, m_, s_ = x_true
w_true = a + b * (rho * (kk - m_) + np.sqrt((kk - m_) ** 2 + s_ ** 2))
vol = np.sqrt(w_true / Tm)
caso = S.CASOS_CONTROL["DER-SKEW-001"][1]
ent = C.entrada(caso)
ent["valores"]["superficie"] = {"strikes": [float(100 * math.exp(z)) for z in kk], "vols": [float(z) for z in vol],
                                "forward": 100.0, "spot": 100.0, "tipo_interes": 0.0}
r, _ = fn("DER-SKEW-001")(ent, {})
svi = r["svi"]
C.informe("DER-SKEW SVI recupera (a, b, ρ, m, σ) de una sonrisa SVI exacta",
          np.allclose([svi["a"], svi["b"], svi["rho"], svi["m"], svi["sigma"]], x_true, atol=1e-6),
          str(np.round([svi["a"], svi["b"], svi["rho"], svi["m"], svi["sigma"]], 6)))


def vol_svi(k):
    return math.sqrt((a + b * (rho * (k - m_) + math.sqrt((k - m_) ** 2 + s_ ** 2))) / Tm)


def k_de_delta(dc):
    return optimize.brentq(lambda k: norm.cdf((-k + 0.5 * vol_svi(k) ** 2 * Tm) / (vol_svi(k) * math.sqrt(Tm))) - dc, -0.6, 0.45)


sp, sc = vol_svi(k_de_delta(0.75)), vol_svi(k_de_delta(0.25))
C.informe("DER-SKEW RR 25Δ por SVI = σ(Δc = 0,75) − σ(Δc = 0,25) (raíz propia, delta forward sin prima)",
          cerca(svi["rr_puntos"], (sp - sc) * 100, 1e-6), f"{svi['rr_puntos']:.6f} vs {(sp - sc) * 100:.6f}")
C.informe("DER-SKEW BF 25Δ por SVI", cerca(svi["bf_puntos"], ((sp + sc) / 2 - vol_svi(0.0)) * 100, 1e-6))
C.informe("DER-SKEW RR por interpolación en delta próxima a la de SVI (< 0,3 puntos)",
          abs(r["rr_puntos"] - (sp - sc) * 100) < 0.3, f"deltas {r['rr_puntos']:.4f} vs SVI {(sp - sc) * 100:.4f}")
dsig = b * (rho + (0 - m_) / math.sqrt(m_ ** 2 + s_ ** 2)) / (2 * math.sqrt(vol_svi(0) ** 2 * Tm * Tm))
C.informe("DER-SKEW pendiente dσ/dk en k = 0", cerca(svi["pendiente_vol_k0"], dsig, 1e-6), f"{svi['pendiente_vol_k0']} vs {dsig}")

# ------------------------------------------------------------------ DER-ROLL-001
Sx, rf, q = 1.0850, 0.041, 0.027     # divisa: F = S·e^{(i_cot − i_base)T}
dias = [45.0, 136.0, 227.0]
Fs = [Sx * math.exp((rf - q) * d / 365) * (1 + 0.0004 * j) for j, d in enumerate(dias)]
r, _ = fn("DER-ROLL-001")({"valores": {"tipo_activo": "divisa", "spot": Sx, "tipo_financiacion": rf, "tipo_base": q,
                                       "futuros": [{"precio": f, "dias": d} for f, d in zip(Fs, dias)]},
                           "series": {}, "series_rol": {}}, {})
carry = [math.log(f / Sx) / (d / 365) for f, d in zip(Fs, dias)]
C.informe("DER-ROLL carry = ln(F/S)/T por vencimiento", all(cerca(x["carry_implicito_pct"], c * 100, 1e-10)
                                                           for x, c in zip(r["vencimientos"], carry)))
C.informe("DER-ROLL roll = (F₁/F₂ − 1)·365/(d₂ − d₁)", cerca(r["roll_yield_pct"], (Fs[0] / Fs[1] - 1) * 365 / 91 * 100, 1e-10))
C.informe("DER-ROLL desviación frente al teórico en pb", cerca(r["desviacion_vs_teorico_pb"], (carry[0] - (rf - q)) * 1e4, 1e-8))
r3, _ = fn("DER-ROLL-001")({"valores": {"tipo_activo": "divisa", "spot": Sx, "tipo_financiacion": rf, "tipo_base": q,
                                        "futuros": [{"precio": f, "dias": d} for f, d in zip(Fs, dias)]},
                            "series": {}, "series_rol": {}}, {"anualizacion": 360})
C.informe("DER-ROLL anualización 360", cerca(r3["roll_yield_pct"], (Fs[0] / Fs[1] - 1) * 360 / 91 * 100, 1e-10)
          and cerca(r3["carry_implicito_pct"], math.log(Fs[0] / Sx) / (45 / 360) * 100, 1e-10))

# ------------------------------------------------------------------ TCV-TP-001 (ACM independiente)
from statsmodels.tsa.api import VAR  # noqa: E402

rng = np.random.default_rng(11)
k, n_m, plazos = 3, 300, list(range(1, 121))
Phi = np.array([[0.985, 0.01, 0.0], [0.0, 0.93, 0.02], [0.0, 0.0, 0.85]])
Sig_chol = np.diag([1.2e-4, 1e-4, 0.8e-4])   # convexidad moderada: el Σ estimado y el verdadero difieren poco
X = np.zeros((n_m, k))
for tt in range(1, n_m):
    X[tt] = Phi @ X[tt - 1] + Sig_chol @ rng.standard_normal(k)
d0, d1 = 0.025 / 12, np.array([1.0, 0.6, -0.3])
lam0_true, lam1_true = np.array([-2e-5, 1e-5, 0.0]), np.array([[0.02, 0.0, 0.0], [0.0, 0.03, 0.0], [0.0, 0.0, 0.01]])
SigT = Sig_chol @ Sig_chol.T


def recursiones(mu_, Phi_, Sig_, l0, l1, nmax):
    A, B = np.zeros(nmax + 1), np.zeros((nmax + 1, k))
    for n in range(1, nmax + 1):
        A[n] = A[n - 1] + B[n - 1] @ (mu_ - l0) + 0.5 * B[n - 1] @ Sig_ @ B[n - 1] - d0
        B[n] = B[n - 1] @ (Phi_ - l1) - d1
    return A, B


A, B = recursiones(np.zeros(k), Phi, SigT, lam0_true, lam1_true, 120)
Ylog = np.column_stack([-(A[n] + X @ B[n]) / n for n in plazos])
Ypct = np.expm1(Ylog * 12) * 100
fechas = [f"{2000 + j // 12}-{j % 12 + 1:02d}-01" for j in range(n_m)]
r, lim = fn("TCV-TP-001")({"valores": {"curva": {"fechas": fechas, "plazos_meses": plazos,
                                                  "rendimientos": Ypct.tolist()}}, "series": {}, "series_rol": {}},
                          {"n_factores": 3})
# ACM propio: PCA (SVD), VAR(1) con statsmodels, regresión de excesos, λ, recursiones.
Yc = Ylog - Ylog.mean(0)
U, Sv, Vt = np.linalg.svd(Yc, full_matrices=False)
W = Vt[:k].T
Xh = Yc @ W
var = VAR(Xh).fit(1, trend="c")
mu_h, Phi_h = var.params[0], var.params[1:].T
Vh = var.resid
Sig_h = Vh.T @ Vh / (n_m - 1)
dd = np.linalg.lstsq(np.column_stack([np.ones(n_m), Xh]), Ylog[:, 0], rcond=None)[0]
rr_ = Ylog[:, 0]
mats = list(range(2, 121))
RX = np.column_stack([-(n - 1) * Ylog[1:, n - 2] + n * Ylog[:-1, n - 1] - rr_[:-1] for n in mats])
Z = np.column_stack([np.ones(n_m - 1), Vh, Xh[:-1]])
cf = np.linalg.lstsq(Z, RX, rcond=None)[0]
a_, beta_, Cm = cf[0], cf[1:1 + k], cf[1 + k:].T
E = RX - Z @ cf
s2 = float((E ** 2).sum() / E.size)
Bs = np.array([np.outer(beta_[:, j], beta_[:, j]).ravel() for j in range(len(mats))])
pinv = np.linalg.pinv(beta_.T)
l1h = pinv @ Cm
l0h = pinv @ (a_ + 0.5 * (Bs @ Sig_h.ravel() + s2))


def rec2(l0, l1, nmax=120):
    A_, B_ = np.zeros(nmax + 1), np.zeros((nmax + 1, k))
    A_[1], B_[1] = -dd[0], -dd[1:]
    for n in range(2, nmax + 1):
        A_[n] = A_[n - 1] + B_[n - 1] @ (mu_h - l0) + 0.5 * (B_[n - 1] @ Sig_h @ B_[n - 1] + s2) - dd[0]
        B_[n] = B_[n - 1] @ (Phi_h - l1) - dd[1:]
    return A_, B_


Aa, Ba = rec2(l0h, l1h)
An_, Bn_ = rec2(np.zeros(k), np.zeros((k, k)))
for anios, n in ((2, 24), (5, 60), (10, 120)):
    tp_prop = (np.expm1(-(Aa[n] + Xh[-1] @ Ba[n]) / n * 12) - np.expm1(-(An_[n] + Xh[-1] @ Bn_[n]) / n * 12)) * 1e4
    tp_ver = (np.expm1(Ylog[-1, n - 1] * 12) - np.expm1(-(recursiones(np.zeros(k), Phi, SigT, np.zeros(k), np.zeros((k, k)), 120)[0][n]
                                                             + X[-1] @ recursiones(np.zeros(k), Phi, SigT, np.zeros(k),
                                                                                    np.zeros((k, k)), 120)[1][n]) / n * 12)) * 1e4
    C.informe(f"TCV-TP prima a {anios} años = ACM propio (statsmodels)", cerca(r["prima_pb"][str(anios)], tp_prop, 1e-6),
              f"{r['prima_pb'][str(anios)]:.6f} vs {tp_prop:.6f} pb (verdad del generador {tp_ver:.2f} pb)")
    # Informativo: con 25 años de muestra el VAR infraestima la persistencia (la ficha lo advierte), así que la prima
    # estimada se aparta de la del generador en el plazo largo; no es un fallo de la implementación.
    print(f"      (informativo) prima a {anios} años: ACM {r['prima_pb'][str(anios)]:.2f} pb · generador {tp_ver:.2f} pb")
C.informe("TCV-TP error de ajuste < 5 pb en la curva afín propia", r["error_ajuste_pb"]["rmse"] < 5, str(r["error_ajuste_pb"]))
sys.exit(C.resumen())
