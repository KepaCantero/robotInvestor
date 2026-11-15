"""T-149 · Falsos positivos y copias de la regla de niveles de IDX-CONC-001 (`frontera_b._etiquetas_series_copiadas`).

Uso, desde la raíz de la copia:
  .venv/bin/python -I .docs/tickets/T-149/medir_copias.py [--semillas 300] [--modulo <frontera_b.py de otra versión>]
Con `--modulo` mide otra versión del fichero (p. ej. la de HEAD, sacada con `git show HEAD:<ruta> > /tmp/x.py`), para
comparar antes y después. Sin red. Imprime, por caso, cuántos pares de series distintas se toman por copias (falsos
positivos) y cuántas copias de la misma serie no se agrupan (se espera 0 en las dos columnas salvo los límites
declarados en INC-T128-01)."""
import argparse
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "bloque_a" / "11_Ejecutor"))
ap = argparse.ArgumentParser()
ap.add_argument("--semillas", type=int, default=300)
ap.add_argument("--modulo")
a = ap.parse_args()
if a.modulo:
    import bloque_a.motor.operaciones  # noqa: F401  (el import relativo del fichero copiado)
    spec = importlib.util.spec_from_file_location("bloque_a.motor.frontera_b_medida", a.modulo,
                                                  submodule_search_locations=None)
    fb = importlib.util.module_from_spec(spec)
    fb.__package__ = "bloque_a.motor"
    spec.loader.exec_module(fb)
else:
    from bloque_a.motor import frontera_b as fb

FECHAS = pd.bdate_range("2025-06-02", periods=320)
ANIOS = np.asarray((FECHAS - FECHAS[0]).days, dtype=float) / 365.25


def copia(x, y):
    g = fb._etiquetas_series_copiadas(np.vstack([x, y]), ANIOS, fb.FRONTERA_B["tolerancia_clon"], 1.0)
    return bool(g[0] == g[1])


def rejilla(s, paso):
    return s if paso is None else np.round(s / paso) * paso


PASOS = {"sin redondear": None, "0,001": 0.001, "0,01": 0.01, "0,05": 0.05, "0,25": 0.25, "1/8": 0.125, "1/32": 1 / 32}
fp: dict[tuple[str, str, float], int] = {}
fn: dict[tuple[str, float], int] = {}
for nivel in (100.0, 12.0, 2.0):
    for s in range(a.semillas):
        rng = np.random.default_rng(1000 + s)
        m = rng.normal(0.0003, 0.011, len(FECHAS))
        base = nivel * np.cumprod(1 + m)
        otras = {"índices ρ≈0,995": nivel * np.cumprod(1 + m + rng.normal(0, 0.0011, len(FECHAS))),
                 "rentabilidad total 2 %": nivel * np.cumprod(1 + m + 0.02 / 252),
                 "fondo TE 0,1 %": nivel * np.cumprod(1 + m + rng.normal(0, 0.001 / np.sqrt(252), len(FECHAS))),
                 "fondo TE 0,01 %": nivel * np.cumprod(1 + m + rng.normal(0, 0.0001 / np.sqrt(252), len(FECHAS)))}
        for np_, paso in PASOS.items():
            if paso is not None and paso / nivel > 0.02:
                continue   # paso del 2 % del precio o más: fuera de la resolución que la regla puede distinguir
            for caso, y in otras.items():
                fp[(caso, np_, nivel)] = fp.get((caso, np_, nivel), 0) + copia(rejilla(base, paso), rejilla(y, paso))
            # la misma serie, redondeada a la rejilla y con un precio suelto sin redondear
            c = rejilla(base, paso).copy()
            c[-1] = base[-1]
            fn[(np_, nivel)] = fn.get((np_, nivel), 0) + (not copia(base, c))
print(f"{a.semillas} semillas · falsos positivos (pares distintos tomados por copias)")
for (caso, np_, nivel), k in sorted(fp.items(), key=lambda t: (t[0][0], t[0][2], t[0][1])):
    print(f"  {caso:24} nivel {nivel:5.0f}  {np_:14} {k:4d}")
print("copias no agrupadas (la serie en la rejilla con un precio sin redondear)")
for (np_, nivel), k in sorted(fn.items(), key=lambda t: (t[0][1], t[0][0])):
    print(f"  nivel {nivel:5.0f}  {np_:14} {k:4d}")
