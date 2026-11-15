"""QA r01 de T-150 (revisor) · IDX-CONC-001 con copias truncadas (H-05): copias que se escapan y series distintas que
se agrupan por error, frente a la versión de antes (T-149) y con el coste de n = 2000.

Uso, desde la raíz de la copia:
  .venv/bin/python -I .docs/tickets/T-150/revisores/r01_01_truncadas_qa.py <frontera_b.py de antes> [--semillas N] [--sin-coste]
El de antes se saca con `git show ac12d5a:bloque_a/11_Ejecutor/bloque_a/motor/frontera_b.py > <fichero>`.
Partes:
  E. copias (truncadas a muchos pasos y niveles, a otra escala, sin el original, con una sesión ausente y precios
     sueltos, cruzando una potencia de 10): tienen que agruparse; lo que no se agrupa y está declarado en INC-T127-01
     (paso entero > 1 % del precio, redondeo hacia arriba, tablas por tramo) es OBS;
  F. series distintas (monetarios a 4 decimales, índices con ρ de 0,9999 y 0,99999, bonos casi iguales, casi planas,
     índice frente a su rentabilidad total, monetario a 1,00 frente a otro que crece): la versión nueva no agrupa más
     pares que la de antes (lo que ya agrupaba la de antes es un límite declarado de las rondas T-144 y T-149);
  C. coste de n = 2000, T = 2520 (tiempo y memoria máxima, en un proceso aparte).
Termina con 1 si hay algún hallazgo. Sin red ni coste."""
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
ap.add_argument("viejo")
ap.add_argument("--semillas", type=int, default=60)
ap.add_argument("--sin-coste", action="store_true")
ap.add_argument("--medir-coste", help=argparse.SUPPRESS)
a = ap.parse_args()
import bloque_a.motor.operaciones  # noqa: E402,F401
from bloque_a.motor import fichas_mon_idx as fm  # noqa: E402
from bloque_a.motor import frontera_b as fb  # noqa: E402


def _cargar(ruta):
    spec = importlib.util.spec_from_file_location("bloque_a.motor.frontera_b_qa150", ruta)
    m = importlib.util.module_from_spec(spec)
    m.__package__ = "bloque_a.motor"
    spec.loader.exec_module(m)
    return m


fv = _cargar(a.viejo)
if a.medir_coste:   # proceso hijo
    n, T = (int(v) for v in a.medir_coste.split(","))
    rng = np.random.default_rng(1)
    P = np.round(100 * np.exp(np.cumsum(rng.normal(0, 0.01, (n, T)), axis=1)), 2)
    anios = np.arange(T) / 252
    t0 = time.time()
    fb._etiquetas_series_copiadas(P, anios, fb.FRONTERA_B["tolerancia_clon"], 1.0)
    print(f"{time.time() - t0:.1f} {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f}")
    sys.exit(0)

F = pd.bdate_range("2025-06-02", periods=320)
AN = np.asarray((F - F[0]).days, dtype=float) / fm.DIAS_ANIO
T = len(F)
TOL = fb.FRONTERA_B["tolerancia_clon"]
N = a.semillas
hallazgos = 0


def caso(nombre, ok, detalle="", obs=False):
    global hallazgos
    hallazgos += (not ok) and not obs
    print(f"{'OK      ' if ok else ('OBS     ' if obs else 'HALLAZGO')} {nombre}" + (f" · {detalle}" if detalle else ""), flush=True)


def juntas(m, x, y):
    g = m._etiquetas_series_copiadas(np.vstack([x, y]), AN, TOL, 1.0)
    return bool(g[0] == g[1])


def paseo(s, nivel=50.0, sd=0.01):
    return nivel * np.exp(np.cumsum(np.random.default_rng(s).normal(0.0005, sd, T)))


def tr(x, q):
    return np.floor(x / q) * q


def rd(x, q):
    return np.round(x / q) * q


def amplitud(x, y):
    series = {"C00": pd.Series(x, index=F), "C01": pd.Series(y, index=F)}
    res, _ = fm.FICHAS["IDX-CONC-001"]["fn"]({"valores": {"composicion": fm._composicion(10, igual=False)}, "series": series,
                                               "series_rol": {}}, {"top_n": 5})
    return res["amplitud"]


# ---------------------------------------------------------------- E. copias que tienen que agruparse
def sig_tr(x, k):
    e = np.floor(np.log10(x)) - (k - 1)
    return np.floor(x / 10.0 ** e) * 10.0 ** e


def con_huecos(x, s):
    y = x.copy()
    r = np.random.default_rng(s)
    y[r.random(T) < 0.02] = np.nan                       # sesiones ausentes
    sueltos = r.random(T) < 0.05                         # precios sueltos sin redondear (por debajo del 10 %)
    y[sueltos] = x[sueltos] * (1 + r.normal(0, 1e-6, sueltos.sum()))
    return y


COPIAS = [   # (nombre, generador(semilla) -> (x, copia), declarado)
    ("0,01 truncado a 1,5", lambda s: (paseo(s, 1.5), tr(paseo(s, 1.5), 0.01)), False),
    ("0,01 truncado a 5", lambda s: (paseo(s, 5.0), tr(paseo(s, 5.0), 0.01)), False),
    ("0,05 truncado a 20", lambda s: (paseo(s, 20.0), tr(paseo(s, 20.0), 0.05)), False),
    ("0,1 truncado a 100", lambda s: (paseo(s, 100.0), tr(paseo(s, 100.0), 0.1)), False),
    ("1 truncado a 1000 y a 10000", lambda s: (paseo(s, 1e4), tr(paseo(s, 1e4), 1.0)), False),
    ("0,0001 truncado a 1 (monetario a 4 decimales)", lambda s: (paseo(s, 1.0), tr(paseo(s, 1.0), 1e-4)), False),
    ("1/32 truncado a 30", lambda s: (paseo(s, 30.0), tr(paseo(s, 30.0), 1 / 32)), False),
    ("1/256 truncado a 60", lambda s: (paseo(s, 60.0), tr(paseo(s, 60.0), 1 / 256)), False),
    ("redondeada a 0,01 frente a truncada a 0,05", lambda s: (rd(paseo(s), 0.01), tr(paseo(s), 0.05)), False),
    ("dos truncadas a escalas distintas (×1,1 a 0,01 y a 0,05)", lambda s: (tr(paseo(s) * 1.1, 0.01), tr(paseo(s), 0.05)), False),
    ("truncada de la redondeada con el error de la coma flotante (⌊100·p⌋/100)",
     lambda s: (rd(paseo(s), 0.01), np.floor(rd(paseo(s), 0.01) * 100) / 100), False),
    ("truncada con sesiones ausentes y un 5 % de precios sueltos", lambda s: (paseo(s), con_huecos(tr(paseo(s), 0.05), s)), False),
    ("4 cifras significativas truncadas cruzando 10", lambda s: (paseo(s, 9.9, 0.006), sig_tr(paseo(s, 9.9, 0.006), 4)), False),
    ("4 cifras significativas truncadas cruzando 1000", lambda s: (paseo(s, 990.0, 0.006), sig_tr(paseo(s, 990.0, 0.006), 4)), False),
    ("[declarado] 0,01 truncado a 0,8 (paso entero > 1 % del precio)", lambda s: (paseo(s, 0.8), tr(paseo(s, 0.8), 0.01)), True),
    ("[declarado] redondeada hacia arriba a 0,05", lambda s: (paseo(s), np.ceil(paseo(s) / 0.05) * 0.05), True),
    ("[sin declarar] redondeada a 0,05 la primera mitad y truncada después (cambio de método)",
     lambda s: (paseo(s), np.where(np.arange(T) < T // 2, rd(paseo(s), 0.05), tr(paseo(s), 0.05))), None),
]
for nombre, gen, declarado in COPIAS:
    fuera = fuera_v = 0
    for s in range(100, 100 + N):
        x, c = gen(s)
        fuera += not juntas(fb, x, c)
        fuera_v += not juntas(fv, x, c)
    detalle = f"sin agrupar {fuera} de {N} (antes de T-150: {fuera_v})"
    if declarado is None:
        caso(f"E {nombre}", fuera == 0, detalle + "; no está en INC-T127-01 (es de la familia de «cambia de resolución»)", obs=True)
    else:
        caso(f"E {nombre}", fuera == 0, detalle + ("; límite declarado (INC-T127-01, ronda T-150)" if declarado else ""),
             obs=declarado)
# la ficha entera: la copia truncada no deja la amplitud servida
x = paseo(7)
caso("E IDX-CONC-001 no sirve la amplitud con una copia truncada a 0,05", amplitud(x, tr(x, 0.05)) is None)


# ---------------------------------------------------------------- F. series distintas: no más agrupadas que antes
def mon(r, sd, q, o1, o2):
    base = np.exp(0.03 * np.arange(T) / 252)
    return o1(base * np.exp(np.cumsum(r.normal(0, sd, T))), q), o2(base * np.exp(np.cumsum(r.normal(0, sd, T))), q)


def corr(r, nivel, rho, q, o1, o2):
    m = r.normal(0.0003, 0.01, T)
    e = r.normal(0, 0.01 * np.sqrt(2 * (1 - rho)), T)
    return o1(nivel * np.cumprod(1 + m), q), o2(nivel * np.cumprod(1 + m + e), q)


def bono(r, q, o1, o2):
    b = 100 + np.cumsum(r.normal(0, 0.02, T))
    return o1(b * (1 + r.normal(0, 2e-5, T)), q), o2(b * (1 + r.normal(0, 2e-5, T)), q)


def plana(r, q, o1, o2):
    x = 10 * np.exp(np.cumsum(r.normal(0, 0.001, T)))
    return o1(x, q), o2(x * np.exp(np.cumsum(r.normal(0, 0.0002, T))), q)


def rt(r, div, q, o1, o2):
    x = 100 * np.cumprod(1 + r.normal(0.0003, 0.01, T))
    return o1(x, q), o2(x * (1 + div) ** AN, q)


def monetario_100(r, o2):
    x = np.ones(T)
    x[r.random(T) < 0.08] = 1.01
    y = 1.01 ** (np.arange(T) / 252) * (1 + r.normal(0, 0.0002, T))
    return x, o2(y, 1e-4)


FAMILIAS = []
for o1, o2, nm in ((rd, rd, "r/r"), (tr, tr, "t/t"), (rd, tr, "r/t")):
    for sd, q in ((1e-5, 1e-4), (1e-4, 1e-4), (1e-4, 1e-3)):
        FAMILIAS.append((f"monetarios ~1 sd {sd} a {q} {nm}", lambda r, sd=sd, q=q, o1=o1, o2=o2: mon(r, sd, q, o1, o2)))
    for nivel, q in ((10, 0.01), (100, 0.01), (100, 0.05), (1000, 0.1), (5, 0.001)):
        for rho in (0.9999, 0.99999):
            FAMILIAS.append((f"índices ρ {rho} a {nivel} en {q} {nm}",
                             lambda r, nivel=nivel, rho=rho, q=q, o1=o1, o2=o2: corr(r, nivel, rho, q, o1, o2)))
    for q in (0.001, 0.01):
        FAMILIAS.append((f"bonos ~100 casi iguales en {q} {nm}", lambda r, q=q, o1=o1, o2=o2: bono(r, q, o1, o2)))
    FAMILIAS.append((f"casi planas ~10 en 0,01 {nm}", lambda r, o1=o1, o2=o2: plana(r, 0.01, o1, o2)))
    for div in (0.002, 0.005):
        FAMILIAS.append((f"índice y su rentabilidad total ({div}) en 0,01 {nm}", lambda r, div=div, o1=o1, o2=o2: rt(r, div, 0.01, o1, o2)))
FAMILIAS.append(("monetario a 1,00 frente a otro que crece a 4 decimales, redondeado", lambda r: monetario_100(r, rd)))
FAMILIAS.append(("monetario a 1,00 frente a otro que crece a 4 decimales, truncado", lambda r: monetario_100(r, tr)))
peores, indistinguibles = [], []
for nombre, gen in FAMILIAS:
    nuevo = viejo = 0
    for s in range(N):
        x, y = gen(np.random.default_rng(20000 + s))
        nuevo += juntas(fb, x, y)
        viejo += juntas(fv, x, y)
    if nuevo > viejo:   # si antes ya se agrupaba una buena parte, a esa resolución no se distinguen (límite de T-149)
        (peores if viejo < N // 4 else indistinguibles).append(f"{nombre}: {nuevo} frente a {viejo}")
    print(f"         F {nombre:66} agrupadas {nuevo:3} de {N} (antes {viejo})", flush=True)
caso(f"F series distintas: la hipótesis truncada no agrupa más pares que antes ({len(FAMILIAS)} familias, {N} semillas)",
     not peores, "; ".join(peores[:4]))
caso("F familias que ya se agrupaban antes en buena parte (diferencias por debajo del redondeo: INC-T127-01, ronda T-149)",
     not indistinguibles, "; ".join(indistinguibles[:4]), obs=True)

# ---------------------------------------------------------------- C. coste
if not a.sin_coste:
    cmd = [sys.executable, "-I", __file__, a.viejo, "--medir-coste", "2000,2520"]
    r = subprocess.run(cmd, capture_output=True, text=True, check=False)
    seg, mb = (float(v) for v in r.stdout.split())
    caso("C n = 2000, T = 2520 por debajo de la cota de la prueba (60 s)", seg < 60, f"{seg:.1f} s, {mb:.0f} MB de memoria máxima")

print(f"\n{hallazgos} hallazgos")
sys.exit(1 if hallazgos else 0)
