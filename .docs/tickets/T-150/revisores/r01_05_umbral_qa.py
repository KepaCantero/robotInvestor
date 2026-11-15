"""QA r01 de T-150 (revisor) · el umbral del desplazamiento de la hipótesis truncada (H-02 de esta ronda).

Uso, desde la raíz de la copia:  .venv/bin/python -I .docs/tickets/T-150/revisores/r01_05_umbral_qa.py [--semillas N]
Compara `motor/frontera_b.py` con el umbral de hoy (q/p ≤ `tolerancia_clon`) y con el mutante X01 de
`r01_04_mutantes_qa.py` (q/p ≤ 2·`tolerancia_clon`), construido en memoria: copias truncadas a 0,01 de series a 0,6 y
0,8 (q/p de 1,2 a 1,7 %) y series distintas en ese mismo tramo. Solo informa (OBS): termina con 0. Sin red ni coste."""
import argparse
import importlib.util
import sys
import types
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[4]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJ))
ap = argparse.ArgumentParser()
ap.add_argument("--semillas", type=int, default=100)
a = ap.parse_args()
import bloque_a.motor.operaciones  # noqa: E402,F401
from bloque_a.motor import fichas_mon_idx as fm  # noqa: E402
from bloque_a.motor import frontera_b as fb  # noqa: E402

fuente = Path(fb.__file__).read_text(encoding="utf-8")
assert fuente.count("    desplaza = 2 * rel <= tol\n") == 1
fx = types.ModuleType("bloque_a.motor.frontera_b_x01")
fx.__package__ = "bloque_a.motor"
fx.__file__ = fb.__file__
exec(compile(fuente.replace("    desplaza = 2 * rel <= tol\n", "    desplaza = rel <= tol\n"), "frontera_b_x01", "exec"),  # noqa: S102
     fx.__dict__)
assert importlib.util is not None
F = pd.bdate_range("2025-06-02", periods=320)
AN = np.asarray((F - F[0]).days, dtype=float) / fm.DIAS_ANIO
T, N = len(F), a.semillas


def juntas(m, x, y):
    g = m._etiquetas_series_copiadas(np.vstack([x, y]), AN, fb.FRONTERA_B["tolerancia_clon"], 1.0)
    return bool(g[0] == g[1])


def tr(x, q):
    return np.floor(x / q) * q


def rd(x, q):
    return np.round(x / q) * q


for nivel in (0.6, 0.8):
    hoy = x01 = 0
    for s in range(N):
        x = nivel * np.exp(np.cumsum(np.random.default_rng(500 + s).normal(0.0005, 0.01, T)))
        hoy += not juntas(fb, x, tr(x, 0.01))
        x01 += not juntas(fx, x, tr(x, 0.01))
    print(f"OBS      copia truncada a 0,01 de una serie a {nivel}: sin agrupar {hoy} de {N} con el 1 %, {x01} con el 2 %")
    for rho in (0.999, 0.9999):
        for o1, o2, nm in ((rd, rd, "r/r"), (tr, tr, "t/t"), (rd, tr, "r/t")):
            hoy = x01 = 0
            for s in range(N):
                r = np.random.default_rng(s)
                m = r.normal(0.0003, 0.01, T)
                e = r.normal(0, 0.01 * np.sqrt(2 * (1 - rho)), T)
                x, y = o1(nivel * np.cumprod(1 + m), 0.01), o2(nivel * np.cumprod(1 + m + e), 0.01)
                hoy += juntas(fb, x, y)
                x01 += juntas(fx, x, y)
            print(f"OBS      distintas a {nivel}, ρ {rho}, {nm}: agrupadas {hoy} de {N} con el 1 %, {x01} con el 2 %", flush=True)
hoy = x01 = 0
for s in range(N):
    r = np.random.default_rng(7000 + s)
    x = np.ones(T)
    x[r.random(T) < 0.3] = 1.01
    y = np.round(1.01 ** (np.arange(T) / 252) * (1 + r.normal(0, 0.002, T)), 2)
    hoy += juntas(fb, x, y)
    x01 += juntas(fx, x, y)
print(f"OBS      monetario a 1,00 frente a otro a 2 decimales: agrupadas {hoy} de {N} con el 1 %, {x01} con el 2 %")
