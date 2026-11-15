"""QA r03 de T-94 · Adaptación de r02_05_remuestreo_oraculo.py al banco de la ronda r03 (sin tocar el original).
Cambios, y por qué: el recuento propio de fechas efectivas (punto 4) aplica ahora la regla de fechas sin solape (H-13), escrita de nuevo
aquí con un recorrido propio y no con la función del banco; en el punto 6, `remuestreos=1` y `nivel=0,01` tienen que
dar BancoError (cotas de un veredicto, H-19) y, como control, el nivel mínimo admitido (0,80) no pasa del 25 % de
veredictos firmes sin habilidad (nominal 20 %).

Original:
QA r02 de T-94 · Remuestreo por fechas de corte y fechas efectivas frente a un oráculo propio.

1. Oráculo independiente del remuestreo por conglomerados (otro generador, 20.000 remuestreos, implementación con bucles):
   con grupos de tamaños muy distintos, el rango de `resumen(..., grupos=)` y de `diferencia(..., grupos_a=, grupos_b=)`
   coincide con el del oráculo (tolerancia: 0,25 errores típicos del oráculo).
2. La media del informe es la media de las observaciones (no la de las medias por fecha): se declara qué se estima.
3. Cobertura del rango por grupos con conglomerados correlados dentro (efecto aleatorio por fecha): ~90 %.
4. Fechas efectivas: número de fechas distintas entre las selecciones RESUELTAS y puntuadas, por lado (no las repetidas,
   NEUTRAL ni sin resolver), con un recuento propio desde `evaluar`.
5. Mínimo de fechas efectivas: 10 y 10 da veredicto; 9 y 10, y 10 y 9, no (los dos lados).
6. Remuestreos y nivel extremos que el banco admite: `remuestreos=1` y `nivel=0,01` (veredicto firme con un rango de
   anchura cero o casi).
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r02_05_remuestreo_oraculo.py [<carpeta de banco_medida.py>]"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

fallos = []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


def oraculo_medias(x, g, B, seed):
    """Conglomerados enteros con reemplazo; la media es la de todas las observaciones de los conglomerados elegidos."""
    r = np.random.default_rng(seed)
    por = {}
    for v, k in zip(x, g):
        por.setdefault(k, []).append(v)
    grupos = list(por.values())
    out = np.empty(B)
    for b in range(B):
        elegidos = r.integers(0, len(grupos), len(grupos))
        tot = cnt = 0.0
        for e in elegidos:
            tot += sum(grupos[e])
            cnt += len(grupos[e])
        out[b] = tot / cnt
    return out


# 1. Oráculo
rng = np.random.default_rng(11)
tam = rng.integers(1, 9, size=25)                     # 25 fechas con 1 a 8 selecciones cada una
g = [f"2026-{1 + i // 28:02d}-{1 + i % 28:02d}" for i, n in enumerate(tam) for _ in range(n)]
efecto = {k: rng.normal(0, 0.03) for k in set(g)}
x = [0.005 + efecto[k] + rng.normal(0, 0.02) for k in g]
r = bm.resumen(x, 4000, 3, nivel=0.9, grupos=g)
m = oraculo_medias(x, g, 20000, 99)
olo, ohi = np.quantile(m, [0.05, 0.95])
se = m.std()
print(f"   resumen por fechas: banco {r['rango']}  oráculo [{olo:.6f}, {ohi:.6f}]  (n {r['n']}, efectivas {r['efectivas']})")
ok(abs(r["rango"][0] - olo) < 0.25 * se and abs(r["rango"][1] - ohi) < 0.25 * se, "resumen: rango por fechas = oráculo")
ok(r["efectivas"] == 25 and r["n"] == len(x), "resumen: efectivas = 25 fechas, n = observaciones")
ok(abs(r["media"] - float(np.mean(x))) < 1e-6, "resumen: la media es la de las observaciones")
medias_fecha = float(np.mean([np.mean([v for v, k in zip(x, g) if k == f]) for f in sorted(set(g))]))
print(f"   media de observaciones {np.mean(x):+.5f} frente a media de las medias por fecha {medias_fecha:+.5f} (pesa más una fecha con más selecciones)")

tam2 = rng.integers(1, 5, size=18)
g2 = [f"2025-{1 + i // 28:02d}-{1 + i % 28:02d}" for i, n in enumerate(tam2) for _ in range(n)]
y = [rng.normal(-0.002, 0.03) for _ in g2]
d = bm.diferencia(x, y, 4000, 5, 0.9, 10, g, g2)
dd = oraculo_medias(x, g, 20000, 7) - oraculo_medias(y, g2, 20000, 8)
olo, ohi = np.quantile(dd, [0.05, 0.95])
print(f"   diferencia por fechas: banco {d['rango']}  oráculo [{olo:.6f}, {ohi:.6f}]  efectivas {d['efectivas']}")
ok(abs(d["rango"][0] - olo) < 0.25 * dd.std() and abs(d["rango"][1] - ohi) < 0.25 * dd.std(), "diferencia: rango por fechas = oráculo")
ok(d["efectivas"] == [25, 18], "diferencia: efectivas por lado = fechas distintas de cada lado")

# 3. Cobertura con efecto por fecha
dentro = 0
N = 300
for k in range(N):
    rr = np.random.default_rng(5000 + k)
    gg = [f"d{i}" for i in range(30) for _ in range(4)]
    ef = {kk: rr.normal(0, 1.0) for kk in set(gg)}
    z = [ef[kk] + rr.normal(0, 1.0) for kk in gg]
    lo, hi = bm.resumen(z, 1000, k, grupos=gg)["rango"]
    dentro += lo <= 0.0 <= hi
print(f"   cobertura con 30 fechas de 4 selecciones correladas: {dentro / N:.3f}")
ok(0.84 <= dentro / N <= 0.95, "cobertura del rango por fechas entre 84 % y 95 % con correlación dentro de la fecha")

# 4. Fechas efectivas desde evaluar, con un recuento propio
fechas = pd.bdate_range("2026-01-01", "2026-12-31")
pr = np.random.default_rng(2)
sims = ["A", "B", "C", "D", "E"]
P = {s: pd.Series(100 * np.exp(np.cumsum(pr.normal(0, 0.01, len(fechas)))), index=fechas) for s in sims}
P["E"] = P["E"].loc[:"2026-06-30"]                      # E deja de cotizar: sus ventanas posteriores no se resuelven
U = pd.DataFrame({"simbolo": sims, "clase": ["K"] * 5})
fin = lambda ini, h: pd.Timestamp(ini) + pd.Timedelta(days=28)   # noqa: E731
cortes = [d.strftime("%Y-%m-%d") for d in pd.date_range("2026-01-05", periods=40, freq="7D")]
sel = []
for i, c in enumerate(cortes):
    sel.append({"fecha_asof": c, "clase": "K", "simbolo": sims[i % 5], "direccion": ["LARGO", "CORTO", "NEUTRAL"][i % 3], "horizonte": "H"})
    sel.append({"fecha_asof": c, "clase": "K", "simbolo": "A", "direccion": "LARGO", "horizonte": "H"})   # A LARGO cada semana
ev = bm.evaluar(sel, P, U, fin)
abiertas, propias = {}, set()
for s in sorted(sel, key=lambda s: pd.Timestamp(s["fecha_asof"])):   # recuento propio (orden estable por fecha)
    ini, k = pd.Timestamp(s["fecha_asof"]), (s["clase"], s["simbolo"], s["direccion"])
    if s["direccion"] == "NEUTRAL" or (k in abiertas and abiertas[k] > ini):
        continue
    abiertas[k] = fin(ini, "H")
    serie = P[s["simbolo"]]
    if serie.index.max() >= abiertas[k] and fechas.max() >= abiertas[k]:
        propias.add(s["fecha_asof"])
inf = bm.construir_informe({"titular": ev, "azar": ev}, {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0,
                                                       "coste_estimado": None}, 200, 1, None, "h")
print(f"   fechas efectivas: banco {inf['contendientes']['titular']['efectivas']}, recuento propio {len(propias)}; "
      f"repetidas {inf['contendientes']['titular']['repetidas']}, resueltas {inf['contendientes']['titular']['resueltas']}")
finales = {}
for s in sel:   # ventana más larga de cada fecha (todas las filas: también NEUTRAL, repetidas y sin resolver)
    finales[s["fecha_asof"]] = max(finales.get(s["fecha_asof"], fin(s["fecha_asof"], "H")), fin(s["fecha_asof"], "H"))
muestra, hasta = set(), pd.Timestamp.min
for c in sorted(finales):
    if pd.Timestamp(c) >= hasta:
        muestra.add(c)
        hasta = finales[c]
propias_r03 = {c for c in propias if c in muestra}
# Cuidado: una fecha de la muestra puede tener su apuesta de A «repetida» (abierta en una fecha fuera de la muestra)
print(f"   muestra propia sin solape: {len(muestra)} fechas; con alguna selección resuelta y puntuada: {len(propias_r03)}")
ok(inf["contendientes"]["titular"]["efectivas"] == len(propias_r03), "fechas efectivas = recuento propio (sin solape, resueltas y puntuadas)")
ok(sorted(muestra) == inf["fechas_en_muestra"], "fechas de la muestra = recuento propio sin solape")

# 5. Mínimo por lado
def lado(n):
    return [0.05] * (2 * n), [f"f{i // 2}" for i in range(2 * n)]


for na, nb, firme in ((10, 10, True), (9, 10, False), (10, 9, False), (10, 30, True)):
    xa, ga = lado(na)
    xb, gb = lado(nb)
    xb = [-v for v in xb]
    v = bm.diferencia(xa, xb, 300, 1, grupos_a=ga, grupos_b=gb)["veredicto"]
    ok((v == "mejor") == firme, f"mínimo de 10 fechas: {na} frente a {nb} → «{v}»")

# 6. Parámetros extremos admitidos
xa = list(np.random.default_rng(8).normal(0.0, 0.05, 40))
xb = list(np.random.default_rng(9).normal(0.0, 0.05, 40))
ga = gb = [f"f{i}" for i in range(40)]
for kw in ({"remuestreos": 1}, {"nivel": 0.01}, {"nivel": 0.995}, {"min_efectivas": 4}):
    args = dict(remuestreos=300, semilla=1, nivel=0.9, min_efectivas=10) | kw
    try:
        d1 = bm.diferencia(xa, xb, args["remuestreos"], args["semilla"], args["nivel"], args["min_efectivas"], ga, gb)
        ok(False, f"{kw} aceptado en diferencia: «{d1['veredicto']}»")
    except bm.BancoError as e:
        ok(True, f"{kw} → BancoError: {e}")
firmes = sum(bm.diferencia(list(np.random.default_rng(100 + k).normal(0, 0.05, 40)), list(np.random.default_rng(900 + k).normal(0, 0.05, 40)),
                           300, k, 0.80, 10, ga, gb)["veredicto"] in ("mejor", "peor") for k in range(200))
print(f"   nivel=0,80 (la cota) sin habilidad: {firmes / 2:.1f} % de veredictos firmes (nominal 20 %)")
ok(firmes / 2 <= 25, "con el nivel mínimo admitido (0,80), los veredictos firmes sin habilidad no pasan del 25 %")

print(f"\n{len(fallos)} fallo(s)")
for f in fallos:
    print(" -", f)
sys.exit(1 if fallos else 0)
