"""QA r03 de T-94 · Adaptación de r02_06_apuesta_repetida.py al banco de la ronda r03 (sin tocar el original).
Cambios, y por qué: min_efectivas=5 en vez de 1 en el punto 7 (cota MIN_EFECTIVAS_MIN, H-19); el punto solo cuenta fechas efectivas.

Original:
QA r02 de T-94 · La regla de la «apuesta repetida» (H-01) en sus bordes.

1. Borde de la ventana: una apuesta igual en la fecha exacta de fin de la anterior cuenta (la ventana ya cerró); un día
   antes, no. Con horas en la fecha de corte.
2. Orden: barajar las filas de entrada no cambia qué filas cuentan ni sus excesos (salvo empates de fecha y clave).
   Empate: misma fecha y misma clave con horizontes distintos → ¿depende del orden de entrada?
3. Mezcla de direcciones: LARGO y CORTO del mismo activo con ventanas solapadas cuentan las dos (son apuestas contrarias).
4. Mezcla de clases: el mismo símbolo en dos clases del universo.
5. NEUTRAL no abre ni cierra ventanas.
6. Una apuesta sin resolver (su ventana pasa del final de los datos, p. ej. H5) bloquea las siguientes de la misma clave.
7. El número de fechas efectivas cuenta fechas de corte, no la forma de escribirlas («2026-01-05» y «2026-01-05 00:00:00»).
8. Un horizonte que no está en la configuración: ¿BancoError con motivo?
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r02_06_apuesta_repetida.py [<carpeta de banco_medida.py>]
«FALLO» marca lo que contradice el plan o la regla; «NOTA» lo que es una decisión de diseño que conviene declarar."""
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

fallos, notas = [], []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


def nota(msg):
    print("NOTA  " + msg)
    notas.append(msg)


FECHAS = pd.bdate_range("2026-01-01", "2026-12-31")
rng = np.random.default_rng(4)
SIMS = ["A", "B", "C", "D"]
P = {s: pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(FECHAS)))), index=FECHAS) for s in SIMS}
U = pd.DataFrame({"simbolo": SIMS, "clase": ["K"] * 4})
HORIZ = {"H1": pd.Timedelta(days=7), "H2": pd.Timedelta(days=28), "H5": pd.Timedelta(days=3650)}


def fin(ini, h):
    if h not in HORIZ:
        raise KeyError(h)
    return pd.Timestamp(ini).normalize() + HORIZ[h]


def sel(f, s, d="LARGO", h="H2", c="K"):
    return {"fecha_asof": f, "clase": c, "simbolo": s, "direccion": d, "horizonte": h}


def rep(r):
    return [x["repetida"] for x in r]


# 1. Borde
r = bm.evaluar([sel("2026-01-05", "A"), sel("2026-02-02", "A")], P, U, fin)   # fin de la primera = 2026-02-02
ok(rep(r) == [False, False], f"misma apuesta el día exacto de fin de la anterior: cuenta (ventana cerrada) → {rep(r)}")
r = bm.evaluar([sel("2026-01-05", "A"), sel("2026-02-01", "A")], P, U, fin)
ok(rep(r) == [False, True], f"un día antes del fin: repetida → {rep(r)}")
r = bm.evaluar([sel("2026-01-05 16:00", "A"), sel("2026-02-02 09:30", "A")], P, U, fin)
ok(rep(r) == [False, False], f"con horas: la del día de fin (09:30) cuenta → {rep(r)}")
r = bm.evaluar([sel("2026-01-05", "A"), sel("2026-01-05", "A")], P, U, fin)
ok(rep(r) == [False, True], f"fila duplicada en la misma fecha: la segunda es repetida → {rep(r)}")

# 2. Orden
base = [sel(f.strftime("%Y-%m-%d"), s, d, h) for f in pd.date_range("2026-01-05", periods=20, freq="7D")
        for s, d, h in (("A", "LARGO", "H2"), ("B", "CORTO", "H1"), ("C", "LARGO", "H2"))]
ref = {(x["fecha_asof"], x["simbolo"]): (x["repetida"], x["exceso"]) for x in bm.evaluar(base, P, U, fin)}
iguales = True
for k in range(20):
    b = base[:]
    random.Random(k).shuffle(b)
    out = bm.evaluar(b, P, U, fin)
    iguales &= [(x["fecha_asof"], x["simbolo"]) for x in out] == [(x["fecha_asof"], x["simbolo"]) for x in b]
    iguales &= {(x["fecha_asof"], x["simbolo"]): (x["repetida"], x["exceso"]) for x in out} == ref
ok(iguales, "barajar la entrada (20 órdenes) no cambia qué cuenta ni el exceso, y la salida sigue el orden de entrada")
e1 = bm.evaluar([sel("2026-01-05", "A", h="H1"), sel("2026-01-05", "A", h="H2")], P, U, fin)
e2 = bm.evaluar([sel("2026-01-05", "A", h="H2"), sel("2026-01-05", "A", h="H1")], P, U, fin)
c1 = next(x for x in e1 if not x["repetida"])
c2 = next(x for x in e2 if not x["repetida"])
print(f"   empate (misma fecha y clave, H1 y H2): cuenta {c1['horizonte']} ({c1['exceso']:+.4f}) o {c2['horizonte']} ({c2['exceso']:+.4f}) según el orden")
ok(c1["horizonte"] == c2["horizonte"], "con un empate de fecha y clave, la fila que cuenta no depende del orden de entrada")

# 3. Direcciones
r = bm.evaluar([sel("2026-01-05", "A"), sel("2026-01-12", "A", d="CORTO"), sel("2026-01-19", "A")], P, U, fin)
print(f"   LARGO, CORTO, LARGO del mismo activo con ventanas solapadas: repetidas {rep(r)}")
ok(rep(r) == [False, False, True], "LARGO y CORTO son apuestas distintas; el segundo LARGO, con el primero abierto, es repetido")
nota("LARGO y CORTO del mismo activo con ventanas solapadas cuentan los dos: sus excesos casi se anulan y suman dos "
     "observaciones; con una cesta de dos activos, LARGO de uno y CORTO del otro son la misma apuesta con claves distintas (r02_02, escenario P)")

# 4. Clases: el mismo símbolo en dos clases del universo
U2 = pd.DataFrame({"simbolo": ["A", "B", "C", "A"], "clase": ["K", "K", "K", "M"]})
try:
    r = bm.evaluar([sel("2026-01-05", "A", c="K")], P, U2, fin)
    ok(False, f"universo con A en dos clases (K y M): se evalúa sin aviso → {r[0].get('motivo') or r[0]['exceso']}")
except bm.BancoError as e:
    print(f"   universo con A en dos clases → BancoError: {e}")
    ok("dos clases" in str(e) or "duplic" in str(e) or "repet" in str(e),
       "universo con un símbolo en dos clases: el motivo dice que está duplicado (no «no es de la clase K»)")
U3 = pd.DataFrame({"simbolo": ["A", "B", "C", "A"], "clase": ["K"] * 4})
try:
    a = bm.azar([sel("2026-01-05", "?"), sel("2026-01-05", "?"), sel("2026-01-05", "?"), sel("2026-01-05", "?")], U3, 3)
    ok(len({x["simbolo"] for x in a}) == len(a), f"universo con A dos veces en K: azar «sin repetir activo» → {[x['simbolo'] for x in a]}")
except bm.BancoError as e:
    ok(True, f"universo con A dos veces en K → BancoError: {e}")

# 5. NEUTRAL
r = bm.evaluar([sel("2026-01-05", "A"), sel("2026-01-12", "A", d="NEUTRAL"), sel("2026-01-19", "A")], P, U, fin)
ok(rep(r) == [False, False, True] and not r[1]["resuelta"], f"NEUTRAL no se puntúa ni cierra la ventana → {rep(r)}")

# 6. Apuesta sin resolver que bloquea
r = bm.evaluar([sel("2026-01-05", "A", h="H5"), sel("2026-01-12", "A", h="H2")], P, U, fin)
print(f"   H5 sin resolver seguida de H2 resoluble: resueltas {[x['resuelta'] for x in r]}, repetidas {rep(r)}")
if r[1]["repetida"]:
    nota("una apuesta que no puede resolverse (H5, o ventana más allá de los datos) deja «repetidas» las siguientes de la misma "
         "clave durante toda su ventana: ninguna cuenta; la clave no incluye el horizonte")

# 7. Fechas efectivas y forma de escribir la fecha
ev = [{"resuelta": True, "exceso": 0.01 * (i % 3), "fecha_asof": f} for i, f in
      enumerate(["2026-01-05", "2026-01-05 00:00:00", "2026-01-05T00:00:00"] * 4)]
inf = bm.construir_informe({"titular": ev, "azar": ev}, {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0,
                                                       "coste_estimado": None}, 200, 1, None, "h", min_efectivas=5)
print(f"   la misma fecha de corte escrita de tres formas: efectivas {inf['contendientes']['titular']['efectivas']}")
ok(inf["contendientes"]["titular"]["efectivas"] == 1, "una misma fecha de corte escrita de tres formas cuenta como una fecha efectiva")
r = bm.evaluar([sel("2026-01-05", "A"), sel("2026-01-05 00:00:00", "B")], P, U, fin)
print(f"   evaluar deja fecha_asof tal cual: {[x['fecha_asof'] for x in r]}")

# 8. Horizonte desconocido
try:
    bm.evaluar([sel("2026-01-05", "A", h="H9")], P, U, fin)
    ok(False, "horizonte desconocido aceptado")
except bm.BancoError as e:
    ok(True, f"horizonte desconocido → BancoError: {e}")
except Exception as e:  # noqa: BLE001
    ok(False, f"horizonte desconocido → {type(e).__name__}: {e} (no BancoError con motivo)")
try:
    bm.evaluar([{k: v for k, v in sel("2026-01-05", "A").items() if k != "horizonte"}], P, U, fin)
    ok(False, "selección sin horizonte aceptada")
except bm.BancoError as e:
    ok(True, f"selección sin horizonte → BancoError: {e}")
except Exception as e:  # noqa: BLE001
    ok(False, f"selección sin horizonte → {type(e).__name__}: {e} (no BancoError con motivo)")

print(f"\n{len(fallos)} fallo(s), {len(notas)} nota(s)")
for f in fallos:
    print(" -", f)
sys.exit(1 if fallos else 0)
