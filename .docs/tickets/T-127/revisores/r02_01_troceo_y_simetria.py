"""QA r02 de T-127 (y T-128) · frontera con el Bloque B (1.6): ¿se obtiene la cifra de UN emisor, sociedad o token con
UNA sola petición después de la ronda r02 (copias a escala por sus cifras y dominancia de la aportación)?

Vías nuevas (ninguna necesita calcular fuera la cifra de un relleno; solo los datos del propio emisor):
 T. troceo: un emisor partido en k «componentes» con repartos distintos de cada importe (la suma de las partes es el
    emisor). Las cifras de cada parte difieren más del 1 %, ninguna parte domina, y un cociente de sumas da exactamente
    la cifra del emisor entero: REI-LEV-001 (S1 en 3 partes), CHR-TOKEN-001 (TKA, que solo no se admite, en 2 partes como
    «sector»), REI-FFO-001 (X en 2 partes; T-128).
 S. simetría: copias de un emisor con una perturbación simétrica de sus datos, mayor que la tolerancia de clon (2 % a
    10 %): la media ponderada vuelve a la cifra del emisor. Exacto en REI-NAV-001 (T-128: el NAV por acción de A entre
    1,04 y 0,96 con el mismo peso); en FIR-CRED-001 (Merton, no lineal) a segundo orden (σ_E·(1 ± δ), 10 componentes).
 C. compensación: dos rellenos con deuda neta +X y −X; la aportación se mide en valor absoluto, así que S1 no domina,
    y LTV agregado · ΣGAV / GAV de S1 es exactamente su LTV (INC-T127-01 r02 dice «un error de al menos un 5 %»; declara
    aparte las compensaciones).
Cada comprobación es «la entrega NO es la cifra del emisor» (a 1e-9; en S de FIR-CRED, a 1e-3 relativo).
Uso: .venv/bin/python -I .docs/tickets/T-127/revisores/r02_01_troceo_y_simetria.py [ejecutor]
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
from bloque_a.motor import fichas_p2 as P  # noqa: E402

K = C.Contador("r02_01 T-127/T-128 troceo, simetría y compensación")
m = C.motor()
fugas = []


def servir(f, valores, parametros=None, i=0):
    p = C.peticion(f, i)
    p["datos"][0]["valores"] = valores
    if parametros is not None:
        p["parametros"] = parametros
    r, exc, _ = C.servir_contando(m, p)
    if exc is not None:
        return "X", str(exc), []
    if str(r["estado"]).startswith("SERVED"):
        return "S", r["resultado"], r.get("limitaciones") or []
    return "R", r["detalle"], []


def cerca(a, b, tol=1e-9):
    return a is not None and b is not None and abs(a - b) <= tol * max(1.0, abs(b))


def caso(nombre, st, r, pares, tol=1e-9):
    """pares: [(etiqueta, entregado(r), cifra del emisor)]. Fuga si se sirve y todas coinciden."""
    if st != "S":
        print(f"    {nombre}: {st} {str(r)[:170]}")
        K.comprobar(f"{nombre}: no entrega la cifra del emisor", True)
        return
    txt = " · ".join(f"{e} {f(r) if f(r) is None else round(f(r), 9)} (emisor {round(x, 9)})" for e, f, x in pares)
    print(f"    {nombre}: SERVIDO · {txt}")
    fuga = all(cerca(f(r), x, tol) for _, f, x in pares)
    if fuga:
        fugas.append(f"{nombre}: {', '.join(e for e, _, _ in pares)}")
    K.comprobar(f"{nombre}: no entrega la cifra del emisor", not fuga)


# ------------------------------------------------------------------ REI-LEV-001: S1 troceado en 3
print("[REI-LEV-001] T: S1 del caso de control en 3 partes (repartos distintos de cada importe)")
v0 = C.valores("REI-LEV-001")
S1 = v0["componentes"][0]
rep = {"gav": (0.5, 0.3, 0.2), "deuda": (0.3, 0.4, 0.3), "caja": (0.5, 0.25, 0.25), "ebitda": (0.4, 0.4, 0.2),
       "gastos_financieros": (0.25, 0.35, 0.4), "ffo": (0.5, 0.3, 0.2)}
venc = [(60.0, 30.0, 36.0), (40.0, 50.0, 78.0), (20.0, 20.0, 86.0)]     # por parte: 120, 100 y 200 de S1 repartidos
partes = []
for k in range(3):
    c = copy.deepcopy(S1)
    c["id"] = f"S1-parte{k}"
    for q, s in rep.items():
        c[q] = S1[q] * s[k]
    c["vencimientos"] = [{**vto, "importe": venc[k][j]} for j, vto in enumerate(S1["vencimientos"])]
    partes.append(c)
assert all(abs(sum(v["importe"] for v in c["vencimientos"]) - c["deuda"]) < 1e-9 for c in partes)
v = copy.deepcopy(v0)
v["componentes"] = partes
ltv = (S1["deuda"] - S1["caja"]) / S1["gav"] * 100
icr = S1["ebitda"] / S1["gastos_financieros"]
dne = (S1["deuda"] - S1["caja"]) / S1["ebitda"]
coste = v0["coste_refinanciacion"]["swap"] + v0["coste_refinanciacion"]["margen"]
lim24 = "2028-06-30"
prox = [x for x in S1["vencimientos"] if x["fecha"] <= lim24]
v24 = sum(x["importe"] for x in prox) / S1["deuda"] * 100
imp = -sum(x["importe"] * (coste - x["coste"]) for x in prox) / S1["ffo"] * 100
st, r, lim = servir("REI-LEV-001", v)
caso("REI-LEV-001 T3 (S1 troceado)", st, r, [("LTV", lambda r: r["ltv_pct"], ltv), ("ICR", lambda r: r["icr_veces"], icr),
                                            ("DN/EBITDA", lambda r: r["deuda_neta_sobre_ebitda_veces"], dne),
                                            ("venc. 24m", lambda r: r["vencimientos_24m_pct"], v24),
                                            ("impacto FFO", lambda r: r["impacto_ffo_pct"], imp)])

# C: S1 + dos rellenos que se compensan en la deuda neta (+400 y −400)
print("[REI-LEV-001] C: S1 + relleno de deuda neta +400 + relleno de deuda neta −400 (caja > deuda)")
F1 = copy.deepcopy(S1) | {"id": "F1", "gav": 1500.0, "deuda": 410.0, "caja": 10.0, "ebitda": 90.0, "gastos_financieros": 15.0,
                          "ffo": 50.0}
F1["vencimientos"] = [{"fecha": "2030-12-31", "importe": 410.0, "coste": 0.03}]
F2 = copy.deepcopy(S1) | {"id": "F2", "gav": 1200.0, "deuda": 10.0, "caja": 410.0, "ebitda": 70.0, "gastos_financieros": 9.0,
                          "ffo": 40.0}
F2["vencimientos"] = [{"fecha": "2030-12-31", "importe": 10.0, "coste": 0.03}]
for f_ in (F1, F2):
    f_.pop("covenants", None)
v = copy.deepcopy(v0)
v["componentes"] = [copy.deepcopy(S1), F1, F2]
st, r, lim = servir("REI-LEV-001", v)
gtot = S1["gav"] + F1["gav"] + F2["gav"]
caso("REI-LEV-001 C (compensación)", st, r, [("LTV·ΣGAV/GAV_S1", lambda r: r["ltv_pct"] * gtot / S1["gav"], ltv)])

# ------------------------------------------------------------------ CHR-TOKEN-001: TKA troceado en 2 «tokens» de un sector
print("\n[CHR-TOKEN-001] T: TKA (solo, se rechaza: no es una red de `redes_propias`) troceado en 2 tokens de un «sector»")
v0 = C.valores("CHR-TOKEN-001", 1)
TKA = v0["tokens"][0]
solo = copy.deepcopy(v0) | {"tokens": [copy.deepcopy(TKA)], "ambito": "red TKA", "ambito_es_red": True}
st, r, _ = servir("CHR-TOKEN-001", solo, {}, 1)
print(f"    TKA solo como red: {st} {str(r)[:120]}")
K.comprobar("CHR-TOKEN-001: TKA solo se rechaza (control)", st == "R")
a, b = copy.deepcopy(TKA), copy.deepcopy(TKA)
a |= {"id": "TKA-1", "oferta_circulante": 2.4e8, "oferta_total": 3.5e8, "oferta_maxima": 3.8e8, "emision_anual": 1.5e7,
      "quema_anual": 1.0e7, "concentracion_10_mayores": 0.35 * 1.03}
b |= {"id": "TKA-2", "oferta_circulante": 3.6e8, "oferta_total": 5.5e8, "oferta_maxima": 6.2e8, "emision_anual": 3.0e7,
      "quema_anual": 0.5e7, "concentracion_10_mayores": 0.35 * (1 - 0.03 * 0.4 / 0.6)}
fut = [d for d in TKA["calendario"]["desbloqueos"] if d["fecha"] > v0["fecha"]]
pas = [d for d in TKA["calendario"]["desbloqueos"] if d["fecha"] <= v0["fecha"]]
cant_a = (1e7, 4e7, 4e7)
a["calendario"] = {**TKA["calendario"], "desbloqueos": pas + [{**d, "cantidad": q} for d, q in zip(fut, cant_a)]}
b["calendario"] = {**TKA["calendario"], "desbloqueos": [{**d, "cantidad": d["cantidad"] - q} for d, q in zip(fut, cant_a)]}
for q in ("oferta_circulante", "oferta_total", "oferta_maxima", "emision_anual", "quema_anual"):
    assert abs(a[q] + b[q] - TKA[q]) < 1e-3, q
v = copy.deepcopy(v0)
v["tokens"] = [a, b]
cm = TKA["precio"] * TKA["oferta_circulante"]
infl = (TKA["emision_anual"] - TKA["quema_anual"]) / TKA["oferta_circulante"] * 100


def desb(w):
    import pandas as pd
    lim_ = pd.Timestamp(v0["fecha"]) + pd.Timedelta(days=w)
    return sum(d["cantidad"] for d in fut if pd.Timestamp(d["fecha"]) <= lim_) / TKA["oferta_circulante"] * 100


st, r, lim = servir("CHR-TOKEN-001", v, {}, 1)
caso("CHR-TOKEN-001 T2 (TKA troceado)", st, r,
     [("FDV/CM", lambda r: r["fdv_sobre_capitalizacion_veces"], TKA["oferta_maxima"] / TKA["oferta_circulante"]),
      ("inflación", lambda r: r["inflacion_neta_pct_anual"], infl),
      ("desb. 30", lambda r: r["desbloqueos_pct"]["30"], desb(30)), ("desb. 90", lambda r: r["desbloqueos_pct"]["90"], desb(90)),
      ("staking real", lambda r: r["rendimiento_real_staking_pct"], TKA["staking_nominal"] * 100 - infl),
      ("concentración", lambda r: r["concentracion_10_mayores_pct"], TKA["concentracion_10_mayores"] * 100),
      ("capitalización", lambda r: r["capitalizacion_circulante"], cm)])

# ------------------------------------------------------------------ REI-NAV-001 (T-128): A con su NAV por acción simétrico
print("\n[REI-NAV-001] S: la sociedad A en 2 partes con el mismo peso y NAV por acción 20/1,04 y 20/0,96")
v0 = C.valores("REI-NAV-001", 2)
A = v0["componentes"][0]
partes = []
for k, d in enumerate((0.04, -0.04)):
    c = copy.deepcopy(A)
    c["id"] = f"A-parte{k}"
    c["acciones"] = A["acciones"] / 2
    c["nav_por_accion"] = A["nav_por_accion"] / (1 + d)
    c["deuda_neta"] = A["deuda_neta"] / 2
    c["otros_pasivos"] = A["otros_pasivos"] / 2
    c["gav"] = c["nav_por_accion"] * c["acciones"] + c["deuda_neta"] + c["otros_pasivos"]
    partes.append(c)
v = copy.deepcopy(v0)
v["componentes"] = partes
st, r, lim = servir("REI-NAV-001", v, None, 2)
primaA = (A["precio"] / A["nav_por_accion"] - 1) * 100
caso("REI-NAV-001 S2 (A simétrica)", st, r, [("prima agregada", lambda r: r["prima_agregada_pct"], primaA)])
if st == "S":
    print(f"      además: percentil {r.get('percentil')} · z {r.get('z')} (los de la prima de A frente a la historia)")

# ------------------------------------------------------------------ REI-FFO-001 (T-128): X troceada en 2
print("\n[REI-FFO-001] T: la sociedad X en 2 partes (acciones 40/60 y repartos distintos de cada importe)")
v0 = C.valores("REI-FFO-001", 1)
X = v0["componentes"][0]
sh = {"beneficio_neto": 0.2, "amortizaciones_inmobiliarias": 0.5, "plusvalias": 0.5, "capex_mantenimiento": 0.4,
      "ajuste_rentas_lineales": 0.5, "dividendo": 0.45, "rentas": 0.4}
p1, p2 = copy.deepcopy(X), copy.deepcopy(X)
p1["id"], p2["id"] = "X-1", "X-2"
p1["acciones"], p2["acciones"] = X["acciones"] * 0.4, X["acciones"] * 0.6
for e1, e2, e in zip(p1["ejercicios"], p2["ejercicios"], X["ejercicios"]):
    for q, s in sh.items():
        if e.get(q) is not None:
            e1[q], e2[q] = e[q] * s, e[q] * (1 - s)
ult = max(X["ejercicios"], key=lambda e: e["ejercicio"])
ffo = ult["beneficio_neto"] + ult["amortizaciones_inmobiliarias"] - ult["plusvalias"]
affo = ffo - ult["capex_mantenimiento"] - ult["ajuste_rentas_lineales"]
capX = X["precio"] * X["acciones"]
v = copy.deepcopy(v0)
v["componentes"] = [p1, p2]
v.pop("historia_multiplos", None)
st, r, lim = servir("REI-FFO-001", v, None, 1)
caso("REI-FFO-001 T2 (X troceada)", st, r, [("P/FFO", lambda r: r["p_ffo"], capX / ffo), ("P/AFFO", lambda r: r["p_affo"], capX / affo),
                                           ("cobertura", lambda r: r["cobertura_agregada"], affo / ult["dividendo"])])

# ------------------------------------------------------------------ FIR-CRED-001: C11 con σ_E simétrica (no lineal)
print("\n[FIR-CRED-001] S: 10 copias de C11 con σ_E·(1 ± δ), δ = 2, 4, 6, 8 y 10 % (mismos importes)")
v0 = C.valores("FIR-CRED-001", 1)
cifras = [P._fc_directo(V, sV, D) for V, sV, D, _ in P._FC_ACTIVOS]
ix = max(range(len(cifras)), key=lambda i: cifras[i]["pd"])
x0, cx = cifras[ix], v0["componentes"][ix]
comps = []
for k, d in enumerate((0.02, 0.04, 0.06, 0.08, 0.10)):
    for sg in (1, -1):
        c = copy.deepcopy(cx)
        c["id"] = f"S{k}{'+' if sg > 0 else '-'}"
        c["volatilidad_acciones"] = cx["volatilidad_acciones"] * (1 + sg * d)
        comps.append(c)
v = copy.deepcopy(v0)
v["componentes"] = comps
st, r, lim = servir("FIR-CRED-001", v, {})
if st == "S":
    n_ = r["neutral_al_riesgo"]
    e_dd = abs(n_["dd"]["media_ponderada_deuda"] / x0["dd"] - 1)
    e_med = abs(n_["dd"]["mediana"] / x0["dd"] - 1)
    e_pd = abs(n_["pd_pct"]["mediana"] / (x0["pd"] * 100) - 1)
    print(f"    SERVIDO · DD media {n_['dd']['media_ponderada_deuda']:.6f}, mediana {n_['dd']['mediana']:.6f} (C11 {x0['dd']:.6f}; "
          f"error {e_dd:.1e} y {e_med:.1e}) · PD mediana {n_['pd_pct']['mediana']:.6f} % (C11 {x0['pd'] * 100:.6f} %; error {e_pd:.1e})")
    fuga = e_dd < 1e-2 and e_med < 1e-2   # INC-T127-01: «dos o más cifras significativas» es la cifra
    if fuga:
        fugas.append("FIR-CRED-001 S10: DD media y mediana de C11 a < 1 % (dos cifras significativas o más, el criterio de INC-T127-01)")
    K.comprobar("FIR-CRED-001 S10: no entrega la DD de C11 con dos cifras significativas o más", not fuga)
else:
    print(f"    {st} {str(r)[:170]}")
    K.comprobar("FIR-CRED-001 S10: no entrega la DD de C11 con dos cifras significativas o más", True)

print("\n== vías que dan la cifra de un solo emisor, sociedad o token con una petición:")
for f in fugas:
    print("   ", f)
sys.exit(K.fin())
