"""QA r01 de T-135 · IDX-CONC-001: copias en la amplitud (T-128 H-05).

 C. Vías de copia de un valor: exacta, a escala, recortada, con desfase de fechas, con una sesión ausente, redondeada
    (GBX → GBP con 2 decimales; conversión a otra divisa con 4 decimales) y muchas copias de un valor más otro.
 K. La concentración (peso de los n mayores, HHI, N_ef, HHI sectorial) no cambia y se comprueba a mano.
 F. Falsos positivos de «copia»: índice de precios frente a su índice de rentabilidad total, dos índices de un mismo
    mercado muy correlados, un fondo frente a su índice con un error de seguimiento pequeño, dos series planas.
 P. La petición no cambia la regla (claves no declaradas, umbrales fijos).
 R. Orden, NaN/0 por la vía `ent["series"]` y coste con índices grandes.
Uso: python -I .docs/tickets/T-135/revisores/r01_01_copias_idx_conc.py bloque_a/11_Ejecutor
Imprime «ok» o «HALLAZGO»; los hallazgos no hacen fallar el script (código de salida 0), lo resume la última línea.
"""
import copy
import sys
import time
from pathlib import Path

EJE = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJE))
import numpy as np
import pandas as pd
from bloque_a.motor import fichas_mon_idx as fm
from bloque_a.motor import frontera_b as fb
from bloque_a.motor.operaciones import ErrorFicha

FECHAS = pd.bdate_range("2025-06-02", periods=320)
ok, hallazgos = 0, []


def comprobar(nombre, cond, detalle=""):
    global ok
    if cond:
        ok += 1
        print(f"  ok        {nombre}")
    else:
        hallazgos.append(nombre)
        print(f"  HALLAZGO  {nombre} · {detalle}")


def correr(series, p=None, comp=None):
    v = {"composicion": comp or fm._composicion(10, igual=False)}
    ent = {"valores": copy.deepcopy(v), "series": series, "series_rol": {}}
    return fm.FICHAS["IDX-CONC-001"]["fn"](ent, dict(p or {"top_n": 5}))


def paseo(semilla, deriva=0.0, sd=0.01, nivel=100.0, fechas=FECHAS):
    rng = np.random.default_rng(semilla)
    return pd.Series(nivel * np.exp(np.cumsum(rng.normal(deriva, sd, len(fechas)))), index=fechas)


def a_mano(series):
    sobre = [float(s.iloc[-1] > s.iloc[-200:].mean()) for s in series]
    return sum(sobre) / len(sobre)


def amplitud(series):
    try:
        res, lim = correr(series)
    except ErrorFicha as e:
        return "R", str(e)[:120], []
    return ("S", res["amplitud"], lim)


# ------------------------------------------------------------------ C: vías de copia
print("[C] un valor A y una copia suya")
A = paseo(7, 0.0005, nivel=1234.5)
B = paseo(8, -0.0005)
vias = {
    "exacta": A.copy(),
    "a escala ×0,01": A * 0.01,
    "a escala ×37": A * 37,
    "recortada (desde la sesión 40, más de 1 año) ×2": A.iloc[40:] * 2,
}
for nombre, c in vias.items():
    st, amp, lim = amplitud({"C00": A, "SECRETA": c})
    comprobar(f"C: A + copia {nombre}: amplitud null sin identificadores",
              st == "S" and amp is None and not any("SECRETA" in x or "C00" in x for x in lim), f"{st} {amp}")

# vías que la regla declara como límite o que pueden darse sin querer
print("    vías fuera de la regla (se registra lo que da la ficha):")
desfase = pd.Series(A.to_numpy(), index=FECHAS + pd.offsets.BDay(1))
una_menos = A.drop(A.index[150])
gbp = (A / 100).round(2)                 # la misma acción en libras con 2 decimales (cotiza en peniques)
divisa = (A * 1.0837).round(4)           # convertida a otra divisa a un cambio fijo, 4 decimales
A50 = paseo(7, 0.0005, nivel=50.0)       # la misma acción de dos proveedores: uno con 2 decimales, otro con 6
otras_prov = {"proveedor con 2 decimales (A a ~50)": A50.round(2), "proveedor con 3 decimales (A a ~50)": A50.round(3)}
otras = {"desfase de 1 sesión": desfase, "una sesión ausente": una_menos, "GBX→GBP redondeada a 2 decimales": gbp,
         "a otra divisa (cambio fijo) con 4 decimales": divisa}
fugas = {}
for nombre, c in otras.items():
    st, amp, lim = amplitud({"C00": A, "SECRETA": c})
    rev = None
    if st == "S" and amp is not None:
        rev = amp["porcentaje_sobre_media"] in (0.0, 1.0)
    fugas[nombre] = (st, None if amp is None else amp.get("porcentaje_sobre_media"), rev)
    print(f"    {nombre}: {st} · amplitud {'null' if amp is None else {k: amp[k] for k in ('porcentaje_sobre_media', 'linea_avance_retroceso')}}"
          f" · A sobre su media {a_mano([A]):.0f}")
comprobar("C: una sesión ausente en la copia (fuentes con festivos distintos) no la saca de su grupo",
          fugas["una sesión ausente"][1] is None, str(fugas["una sesión ausente"]))
comprobar("C: la copia en libras redondeada a 2 decimales (GBX/GBP) es una copia a escala",
          fugas["GBX→GBP redondeada a 2 decimales"][1] is None, str(fugas["GBX→GBP redondeada a 2 decimales"]))
comprobar("C: la copia a otra divisa a cambio fijo con 4 decimales es una copia a escala",
          fugas["a otra divisa (cambio fijo) con 4 decimales"][1] is None,
          str(fugas["a otra divisa (cambio fijo) con 4 decimales"]))
for nombre, c in otras_prov.items():
    st, amp, lim = amplitud({"C00": A50.round(6), "SECRETA": c})
    print(f"    {nombre}: {st} · amplitud {'null' if amp is None else amp['porcentaje_sobre_media']}")
    comprobar(f"C: {nombre} frente a 6 decimales es una copia", st == "S" and amp is None, f"{st} {amp}")
print(f"    (desfase de 1 sesión: {fugas['desfase de 1 sesión']}: «muestreada en otras fechas», límite declarado)")

# cuántas sesiones redondeadas bastan para romper el grupo: la tolerancia es por rentabilidad
r = A.pct_change().dropna()
rg = gbp.pct_change().dropna()
fuera = int((np.abs(r - rg) > 0.01 * np.maximum(np.abs(r), np.abs(rg))).sum())
print(f"    GBP con 2 decimales: {fuera} de {len(r)} sesiones con la rentabilidad a más del 1 % relativo de la de A")

print("[C] muchas copias de un valor más otro")
for k_, esperado in ((19, "servida"), (20, "null"), (60, "null")):
    series = {"B": B, **{f"K{j:02d}": A * (1 + j) for j in range(k_)}}
    st, amp, lim = amplitud(series)
    comprobar(f"C: {k_} copias de A + B: amplitud {esperado}",
              st == "S" and ((amp is not None) if esperado == "servida" else (amp is None)), f"{st} {amp}")
Bs = next(paseo(s_, 0.002) for s_ in range(100, 200) if a_mano([paseo(s_, 0.002)]) != a_mano([A]))
st, amp, lim = amplitud({"B": Bs, "K0": A, "K1": A * 2})
st2, amp2, _ = amplitud({"B": Bs, "K0": A})
if st == "S" and amp is not None:
    p_ = amp["porcentaje_sobre_media"]
    print(f"    2 copias de A + B: servida · porcentaje {p_:.4f} = (2·A + B)/3 con A = {a_mano([A]):.0f}, B = {a_mano([Bs]):.0f}: "
          f"despeja A y B; con A y B solos: {amp2['porcentaje_sobre_media']:.2f} (no dice cuál)")
# 19 copias recortadas y a escala distinta, cada una ≥ 1 año
series = {"B": B, **{f"K{j:02d}": A.iloc[j:] * (1 + j) for j in range(20)}}
st, amp, lim = amplitud(series)
comprobar("C: 20 copias recortadas cada una desde otra sesión + B: amplitud null", st == "S" and amp is None, f"{st} {amp}")
# cadena de casi copias: cada una a < 1 % de la anterior, la última a más del 1 % de A
rA = A.pct_change().fillna(0).to_numpy()
cadena = {"B": B, "A": A}
for j in range(1, 30):
    rj = rA * (1 + 0.009 * j)
    cadena[f"K{j:02d}"] = pd.Series(100 * np.cumprod(1 + rj), index=FECHAS)
st, amp, lim = amplitud(cadena)
comprobar("C: cadena de 29 casi copias (cierre transitivo) + B: amplitud null", st == "S" and amp is None, f"{st} {amp}")

# ------------------------------------------------------------------ K: la concentración
print("[K] concentración")
comp = fm._composicion(10, igual=False)
pesos = {c["id"]: c["peso"] for c in comp["componentes"]}
hhi = sum(w * w for w in pesos.values())
sect = {}
for c in comp["componentes"]:
    sect[c["sector"]] = sect.get(c["sector"], 0) + c["peso"]
top5 = sum(sorted(pesos.values(), reverse=True)[:5])
claves = ("peso_top_n", "hhi", "n_ef", "hhi_sectorial", "n_componentes")
ref = {"peso_top_n": top5, "hhi": hhi, "n_ef": 1 / hhi, "hhi_sectorial": sum(w * w for w in sect.values()), "n_componentes": 10}
for nombre, series in (("sin precios", {}), ("A + copia", {"C00": A, "C01": A * 2}), ("A + B", {"C00": A, "C01": B}),
                       ("20 copias + B", {"B": B, **{f"K{j:02d}": A * (1 + j) for j in range(20)}})):
    res, _ = correr(series)
    comprobar(f"K: {nombre}: peso de los 5 mayores, HHI, N_ef, HHI sectorial y n a mano",
              all(abs(res[c] - ref[c]) < 1e-12 for c in claves), str({c: res[c] for c in claves}))
igual = fm._composicion(8, igual=True)
res, _ = correr({"C00": A, "C01": A * 3}, comp=igual)
comprobar("K: equiponderado de 8 ⇒ N_ef = 8 (Verificación de la ficha), con copias en los precios",
          abs(res["n_ef"] - 8) < 1e-10)

# ------------------------------------------------------------------ F: falsos positivos
print("[F] falsos positivos de «copia» con series distintas pero muy correladas")


def es_copia(x, y):
    tabla = pd.DataFrame({"x": x, "y": y}).sort_index()
    g = fb._etiquetas_series_copiadas(tabla.to_numpy(dtype=float).T,
                                      np.asarray((tabla.index - tabla.index[0]).days, dtype=float) / fm.DIAS_ANIO,
                                      fb.FRONTERA_B["tolerancia_clon"], 1.0)
    return g[0] == g[1]


n_sem = 300
cuentas = {"precio vs rentabilidad total (div. 2 %/año)": 0, "dos índices de un mercado (ρ ≈ 0,995)": 0,
           "fondo vs índice (TE 0,1 %/año)": 0, "fondo vs índice (TE 0,01 %/año)": 0}
for s in range(n_sem):
    rng = np.random.default_rng(1000 + s)
    m = rng.normal(0.0003, 0.011, len(FECHAS))
    precio = pd.Series(100 * np.cumprod(1 + m), index=FECHAS)
    rt = pd.Series(100 * np.cumprod(1 + m + 0.02 / 252), index=FECHAS)
    otro = pd.Series(100 * np.cumprod(1 + m + rng.normal(0, 0.0011, len(FECHAS))), index=FECHAS)
    f1 = pd.Series(100 * np.cumprod(1 + m + rng.normal(0, 0.001 / np.sqrt(252), len(FECHAS))), index=FECHAS)
    f2 = pd.Series(100 * np.cumprod(1 + m + rng.normal(0, 0.0001 / np.sqrt(252), len(FECHAS))), index=FECHAS)
    cuentas["precio vs rentabilidad total (div. 2 %/año)"] += es_copia(precio, rt)
    cuentas["dos índices de un mercado (ρ ≈ 0,995)"] += es_copia(precio, otro)
    cuentas["fondo vs índice (TE 0,1 %/año)"] += es_copia(precio, f1)
    cuentas["fondo vs índice (TE 0,01 %/año)"] += es_copia(precio, f2)
for k_, c in cuentas.items():
    print(f"    {k_}: {c}/{n_sem} tomados por copia")
comprobar("F: dos índices de un mismo mercado (ρ ≈ 0,995) nunca son copia",
          cuentas["dos índices de un mercado (ρ ≈ 0,995)"] == 0)
comprobar("F: índice de precios y su rentabilidad total nunca son copia",
          cuentas["precio vs rentabilidad total (div. 2 %/año)"] == 0)
plano1 = pd.Series(10.0, index=FECHAS)
plano2 = pd.Series(250.0, index=FECHAS)
print(f"    dos series planas de valores distintos (sin cotizar un año): copia = {es_copia(plano1, plano2)} (degenerado)")
# un valor con sus días sin variación (iliquidez) y otro con los mismos días planos y el resto distinto
ili1 = A.copy()
ili2 = B.copy()
comprobar("F: dos valores distintos con muchos días sin variación no son copia", not es_copia(ili1.round(0), ili2.round(0)))

# ------------------------------------------------------------------ P: la petición
print("[P] la petición")
for clave, valor in (("tolerancia_clon", 1.0), ("peso_maximo_componente", 1.0), ("componentes_minimos", 1),
                     ("IDX_CONC_COMPONENTES_MINIMOS", 1), ("coincidencias_informativas_minimas", 0), ("foo", "bar")):
    try:
        res, lim = correr({"C00": A, "C01": A * 2}, {"top_n": 5, clave: valor})
        comprobar(f"P: «{clave}» en la petición no sirve la amplitud de A + copia", res["amplitud"] is None)
    except ErrorFicha as e:
        comprobar(f"P: «{clave}» en la petición se rechaza", True, str(e))
for clave, valor in (("anios_precios_min", 0), ("top_n_rango", [1, 50]), ("ventana_percentil_min_anios", 0)):
    try:
        correr({"C00": A, "C01": A * 2}, {"top_n": 5, clave: valor})
        comprobar(f"P: «{clave}» (umbral) se rechaza", False, "se aceptó")
    except ErrorFicha as e:
        comprobar(f"P: «{clave}» (umbral) se rechaza", "umbrales fijos" in str(e), str(e)[:100])
# media_amplitud (parámetro declarado) no reabre la fuga: con 1 sesión la media es el último precio
for m in (1, 2, 199, 2520):
    try:
        res, _ = correr({"C00": A, "C01": A * 2}, {"top_n": 5, "media_amplitud": m})
        comprobar(f"P: media_amplitud = {m} con A + copia: amplitud null", res["amplitud"] is None)
    except ErrorFicha as e:
        comprobar(f"P: media_amplitud = {m}: rechazo", True, str(e)[:80])

# ------------------------------------------------------------------ R: orden, valores raros, coste
print("[R] orden, valores raros y coste")
s1 = {"B": B, "C00": A, "C01": A * 2, "D": paseo(9)}
s2 = dict(reversed(list(s1.items())))
r1, l1 = correr(s1)
r2, l2 = correr(s2)
comprobar("R: el orden de las series no cambia la entrega", r1 == r2 and l1 == l2)
r3, _ = correr({"ZZ": B, "AA": A, "MM": A * 2, "D": paseo(9)})
comprobar("R: renombrar las series no cambia la entrega", r1["amplitud"] == r3["amplitud"])
for nombre, s in (("con un 0", A.where(A.index != A.index[100], 0.0)), ("con inf", A.where(A.index != A.index[100], np.inf)),
                  ("negativa", -A)):
    try:
        res, lim = correr({"C00": s, "C01": B})
        print(f"    serie {nombre} por ent['series']: servida · amplitud {res['amplitud']}")
    except (ErrorFicha, ValueError, ZeroDivisionError) as e:
        print(f"    serie {nombre} por ent['series']: rechazo/errores · {type(e).__name__}: {str(e)[:80]}")
# vía valores["precios"] con un 0
try:
    v = {"composicion": fm._composicion(10, igual=False),
         "precios": {"C00": [{"fecha": str(d.date()), "precio": 0.0 if i == 100 else float(x)} for i, (d, x) in enumerate(A.items())],
                     "C01": [{"fecha": str(d.date()), "precio": float(x)} for d, x in B.items()]}}
    fm.FICHAS["IDX-CONC-001"]["fn"]({"valores": v, "series": {}, "series_rol": {}}, {"top_n": 5})
    comprobar("R: un precio 0 en valores[precios] se rechaza", False, "servido")
except ErrorFicha as e:
    comprobar("R: un precio 0 en valores[precios] se rechaza", True, str(e)[:80])

fechas_largas = pd.bdate_range("2016-11-01", periods=2520)
for n, tardia in ((100, False), (500, False), (500, True), (1000, True)):
    rng = np.random.default_rng(n)
    m = rng.normal(0, 0.01, len(fechas_largas))
    series = {}
    for i in range(n):
        x = pd.Series(100 * np.exp(np.cumsum(m + rng.normal(0, 0.01, len(fechas_largas)))), index=fechas_largas)
        series[f"S{i:04d}"] = x
    if tardia:   # una salida a bolsa reciente (1 año y medio) y una exclusión antigua sin fechas comunes con ella
        series["S0000"] = series["S0000"].iloc[-380:]
        series["S0001"] = series["S0001"].iloc[:300]
    comp = {"fecha": "2026-10-31", "componentes": [{"id": k, "peso": 1 / n, "sector": "X"} for k in series]}
    t0 = time.perf_counter()
    res, _ = correr(series, comp=comp)
    dt = time.perf_counter() - t0
    print(f"    n = {n}, T = 2520{', con salida y exclusión' if tardia else ''}: {dt:.1f} s · amplitud servida "
          f"{res['amplitud'] is not None}")
    if n == 1000:
        comprobar("R: un índice de 1000 valores con 10 años y una salida y una exclusión sin fechas comunes en < 60 s",
                  dt < 60, f"{dt:.0f} s")

print(f"\n== r01_01 T-135 IDX-CONC copias: {ok} ok · {len(hallazgos)} hallazgo(s): {'; '.join(hallazgos) or 'ninguno'}")
