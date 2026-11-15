"""QA r01 de T-149 (revisor) · regla de niveles de IDX-CONC-001 con las rejillas de `REJILLAS_PRECIO`.

Uso, desde la raíz de la copia:
  .venv/bin/python -I .docs/tickets/T-149/revisores/r01_01_rejillas_qa.py [--modulo <frontera_b.py de otra versión>]
                                                                          [--sin-coste]
Sin red. Tres partes:
  A. copias de una misma serie que el ticket no prueba (otras rejillas de la lista, escalas, divisas, el borde del 90 %,
     cifras significativas en otras décadas, precios diminutos, dos copias sin el original, truncar en vez de redondear,
     tablas de pasos por tramo de precio): se espera que se agrupen y que IDX-CONC-001 no sirva la amplitud;
  B. series distintas (índices muy correlados, valores poco líquidos con precios repetidos, series que cruzan una
     década, series casi constantes): se espera que no se agrupen;
  C. coste y memoria de `_etiquetas_series_copiadas` con n = 2000 y T = 2520 (la prueba de T-144), y orden de las series.
Lo que cae en un límite declarado (INC-T127-01, «Ronda T-149») se imprime como OBS y no cuenta. Termina con 1 si hay
algún hallazgo. Con `--modulo` mide otra versión (p. ej. la de antes de T-149: `git show HEAD~1:<ruta> > x.py`)."""
import argparse
import importlib.util
import resource
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[4]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJ))
ap = argparse.ArgumentParser()
ap.add_argument("--modulo")
ap.add_argument("--sin-coste", action="store_true")
ap.add_argument("--medir-coste", help=argparse.SUPPRESS)   # interno: n,T en un proceso aparte
a = ap.parse_args()
if a.modulo:
    import bloque_a.motor.operaciones  # noqa: F401
    spec = importlib.util.spec_from_file_location("bloque_a.motor.frontera_b_qa", a.modulo)
    fb = importlib.util.module_from_spec(spec)
    fb.__package__ = "bloque_a.motor"
    spec.loader.exec_module(fb)
else:
    from bloque_a.motor import frontera_b as fb
from bloque_a.motor import fichas_mon_idx as fm

if a.medir_coste:   # proceso hijo: tiempo y memoria máxima de una llamada
    n, T = (int(v) for v in a.medir_coste.split(","))
    rng = np.random.default_rng(3)
    p = 50 * np.exp(np.cumsum(rng.normal(0.0003, 0.012, (n, T)), axis=1))
    p = np.round(p, 2)
    anios = np.arange(T) / 252.0
    t0 = time.perf_counter()
    g = fb._etiquetas_series_copiadas(p, anios, fb.FRONTERA_B["tolerancia_clon"], 1.0)
    dt = time.perf_counter() - t0
    print(f"{dt:.2f} {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} {len(set(g.tolist()))}")
    sys.exit(0)

FECHAS = pd.bdate_range("2025-06-02", periods=320)
hallazgos = 0


def paseo(semilla, nivel=50.0, sd=0.01, n=len(FECHAS)):
    rng = np.random.default_rng(semilla)
    return pd.Series(nivel * np.exp(np.cumsum(rng.normal(0.0005, sd, n))), index=FECHAS[:n])


def rej(s, paso):
    return (s / paso).round() * paso


def es_copia(*series):
    t = pd.DataFrame({f"s{i}": s for i, s in enumerate(series)}).sort_index()
    g = fb._etiquetas_series_copiadas(t.to_numpy(dtype=float).T, np.asarray((t.index - t.index[0]).days, dtype=float) / fm.DIAS_ANIO,
                                      fb.FRONTERA_B["tolerancia_clon"], 1.0)
    return g


def agrupadas(x, y, *otras):
    g = es_copia(x, y, *otras)
    return bool(g[0] == g[1])


def amplitud(series):
    v = {"composicion": fm._composicion(10, igual=False)}
    res, _ = fm.FICHAS["IDX-CONC-001"]["fn"]({"valores": v, "series": series, "series_rol": {}}, {"top_n": 5})
    return res["amplitud"]


def caso(nombre, ok, detalle="", declarado=False):
    global hallazgos
    etiqueta = "OK      " if ok else ("OBS     " if declarado else "HALLAZGO")
    hallazgos += (not ok) and not declarado
    print(f"{etiqueta} {nombre}" + (f" · {detalle}" if detalle else ""), flush=True)


def sig(s, k):
    return s.apply(lambda v: float(f"{v:.{k}g}"))


def con_sueltos(copia, original, k, semilla=0):
    """`k` precios de `copia` sustituidos por los de `original` (sin redondear), en fechas al azar."""
    idx = np.random.default_rng(semilla).choice(len(copia), k, replace=False)
    c = copia.copy()
    c.iloc[idx] = original.iloc[idx]
    return c


def tramos(s, corte, fino, grueso):
    """Tabla de pasos por tramo de precio (como las de MiFID II): `fino` por debajo de `corte` y `grueso` por encima."""
    return pd.Series(np.where(s < corte, rej(s, fino), rej(s, grueso)), index=s.index)


# ---------------------------------------------------------------- A. copias (se esperan agrupadas y sin amplitud)
A = paseo(7, 50.0)                    # 36,6 … 50,2
ANCHA = paseo(21, 8.0, sd=0.03)       # cruza décadas
print(f"A: {A.min():.2f}…{A.max():.2f}; ANCHA: {ANCHA.min():.2f}…{ANCHA.max():.2f}")
VIAS = {   # nombre: (original, copia, declarado)
    "0,5 a 50": (A, rej(A, 0.5), False),
    "0,2 a 50": (A, rej(A, 0.2), False),
    "2,5 a 500": (A, rej(A * 10, 2.5), False),
    "250 a 50 000": (A, rej(A * 1000, 250.0), False),
    "500 a 50 000": (A, rej(A * 1000, 500.0), False),
    "0,0025 a 0,5": (A, rej(A / 100, 0.0025), False),
    "1/64 a 100": (A, rej(A * 2, 1 / 64), False),
    "1/256 a 100": (A, rej(A * 2, 1 / 256), False),
    "0,05 con un cambio de divisa fijo (×1,0837)": (A, rej(A * 1.0837, 0.05), False),
    "0,05 con el 9 % de precios sin redondear": (A, con_sueltos(rej(A, 0.05), A, 29), False),
    "0,05 con el 10 % exacto sin redondear (borde)": (A, con_sueltos(rej(A, 0.05), A, 32), False),
    "0,05 con el 11 % sin redondear (fuera del 90 %)": (A, con_sueltos(rej(A, 0.05), A, 36), True),
    "dos copias sin el original: 0,05 y 1/8": (rej(A, 0.05), rej(A, 0.125), False),
    "dos copias sin el original: 0,25 y 2 decimales": (rej(A, 0.25), A.round(2), False),
    "3 cifras significativas cruzando 10 (A/4)": (A / 4, sig(A / 4, 3), False),
    "4 cifras significativas cruzando 1000 (A·22)": (A * 22, sig(A * 22, 4), False),
    "4 cifras significativas cruzando dos décadas": (ANCHA, sig(ANCHA, 4), False),
    "2 decimales con una serie que cruza dos décadas": (ANCHA, ANCHA.round(2), False),
    "precios diminutos (~1e-5) a 8 decimales": (A * 3e-7, (A * 3e-7).round(8), False),
    "0,0005 a 0,5 (céntimos de céntimo)": (A / 100, rej(A / 100, 0.0005), False),
    "0,0005 a 0,005 (paso del 10 % del precio)": (A / 10000, rej(A / 10000, 0.0005), True),
    "0,05 con una sesión ausente y un precio suelto": (A, con_sueltos(rej(A, 0.05), A, 1).drop(A.index[200]), False),
    # tablas de pasos por tramo de precio: cambia la resolución dentro de una década (límite declarado, por el tiempo)
    "tabla por tramos: 0,01 bajo 45 y 0,05 encima": (A, tramos(A, 45.0, 0.01, 0.05), True),
    "tabla por tramos: 0,01 bajo 40 y 0,05 encima": (A, tramos(A, 40.0, 0.01, 0.05), True),
    # truncar (redondeo hacia abajo) en vez de redondear: el error llega a un paso entero, no a medio
    "0,05 truncado (hacia abajo)": (A, np.floor(A / 0.05) * 0.05, False),
    "2 decimales truncado": (A, np.floor(A * 100) / 100, False),
}
for nombre, (x, copia, declarado) in VIAS.items():
    ag = agrupadas(x, copia)
    amp = amplitud({"C00": x, "SECRETA": copia})
    caso(f"A {nombre}: agrupada y sin amplitud", ag and amp is None,
         f"agrupada={ag} amplitud={'null' if amp is None else 'servida'}", declarado)

# una serie de precio muy alto en el índice no cambia lo de las demás (la década de partida es la del mayor precio)
G = es_copia(A, rej(A, 0.05), paseo(3, 2e6), paseo(4, 0.02))
caso("A una serie de 2e6 y otra de 0,02 junto a la copia de 0,05", G[0] == G[1] and len(set(G.tolist())) == 3, f"grupos={G.tolist()}")

# ---------------------------------------------------------------- B. series distintas (se esperan separadas)
SEM = 100


def contar(fn):
    return sum(bool(fn(np.random.default_rng(7000 + s))) for s in range(SEM))


def par_indices(rng, nivel, paso, ruido=0.0011, n=len(FECHAS)):
    m = rng.normal(0.0003, 0.011, n)
    x = pd.Series(nivel * np.cumprod(1 + m), index=FECHAS[:n])
    y = pd.Series(nivel * np.cumprod(1 + m + rng.normal(0, ruido, n)), index=FECHAS[:n])
    return (x, y) if paso is None else (rej(x, paso), rej(y, paso))


for nivel, paso in ((100.0, 0.05), (100.0, 0.25), (50.0, 0.125), (100.0, 1 / 32), (12.0, 0.05), (200.0, 0.5), (1000.0, 5.0)):
    k = contar(lambda r: agrupadas(*par_indices(r, nivel, paso)))
    caso(f"B dos índices ρ≈0,995 a {nivel:g} en {paso:g} (paso {paso / nivel:.2%} del precio)", k == 0, f"{k} de {SEM} agrupados")


def iliquidos(rng, nivel=100.0, quietos=0.8, sd=0.002):
    """Dos bonos distintos poco líquidos: el precio solo cambia un 20 % de las sesiones, a 2 decimales."""
    out = []
    comun = rng.normal(0.0001, sd, len(FECHAS))
    for _ in range(2):
        r = comun + rng.normal(0, sd, len(FECHAS))
        r[rng.random(len(FECHAS)) < quietos] = 0.0
        out.append(pd.Series(nivel * np.cumprod(1 + r), index=FECHAS).round(2))
    return out


k = contar(lambda r: agrupadas(*iliquidos(r)))
caso("B dos bonos distintos poco líquidos a 100 (80 % de sesiones quietas, 2 decimales)", k == 0, f"{k} de {SEM}")
k = contar(lambda r: agrupadas(*iliquidos(r, nivel=10.0, quietos=0.9, sd=0.004)))
caso("B dos valores distintos poco líquidos a 10 (90 % quietas, 2 decimales)", k == 0, f"{k} de {SEM}")


def cruzan_100(rng):
    m = rng.normal(0.0, 0.006, len(FECHAS))
    x = pd.Series(99.0 * np.cumprod(1 + m), index=FECHAS)
    y = pd.Series(99.0 * np.cumprod(1 + m + rng.normal(0, 0.0011, len(FECHAS))), index=FECHAS)
    return sig(x, 4), sig(y, 4)


k = contar(lambda r: agrupadas(*cruzan_100(r)))
caso("B dos índices ρ≈0,995 a 4 cifras significativas alrededor de 100", k == 0, f"{k} de {SEM}")


def casi_constantes(rng):
    """Un fondo monetario a 1,00 casi siempre (2 decimales) y otro distinto a 4 decimales que crece un 1 %/año."""
    x = np.ones(len(FECHAS))
    x[rng.random(len(FECHAS)) < 0.08] = 1.01
    y = 1.0 * (1 + 0.01) ** (np.arange(len(FECHAS)) / 252) * (1 + rng.normal(0, 0.0002, len(FECHAS)))
    return pd.Series(x, index=FECHAS), pd.Series(y, index=FECHAS).round(4)


k = contar(lambda r: agrupadas(*casi_constantes(r)))
caso("B un monetario casi siempre a 1,00 y otro que crece un 1 %/año (4 decimales)", k == 0, f"{k} de {SEM}",
     declarado=True)   # paso de 1 frente a 1,00: el límite de los pasos grandes frente al precio (T-144)

# ---------------------------------------------------------------- C. orden, coste y memoria
B_ = paseo(11, 80.0)
o1 = amplitud({"C00": A, "C01": B_, "C02": rej(A, 0.25), "C03": sig(A * 2.3, 4)})
o2 = amplitud({"C03": sig(A * 2.3, 4), "C02": rej(A, 0.25), "C01": B_, "C00": A})
caso("C el orden de las series no cambia el resultado", o1 == o2)
if not a.sin_coste:
    cmd = [sys.executable, "-I", __file__, "--medir-coste", "2000,2520"] + (["--modulo", a.modulo] if a.modulo else [])
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    dt, mb, grupos = r.stdout.split()
    print(f"INFO     C n = 2000, T = 2520 a 2 decimales: {dt} s, memoria máxima {mb} MB, {grupos} grupos", flush=True)
    caso("C n = 2000, T = 2520 dentro de la cota de la prueba (60 s)", float(dt) < 60, f"{dt} s")

print(f"\n{hallazgos} hallazgos")
sys.exit(1 if hallazgos else 0)
