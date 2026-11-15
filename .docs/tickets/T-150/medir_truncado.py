"""T-150 · Copias truncadas hacia abajo y falsos positivos de la regla de niveles de IDX-CONC-001 (H-05 de la QA r01 de T-149).

Uso, desde la raíz de la copia:
  .venv/bin/python -I .docs/tickets/T-150/medir_truncado.py [--semillas 300] [--modulo <frontera_b.py de otra versión>]
Con `--modulo` mide otra versión del fichero (p. ej. la de antes: `git show HEAD:<ruta> > /tmp/x.py`). Sin red. Imprime,
por caso y en cada rejilla y nivel:
  - copias no agrupadas: la serie truncada (⌊p/q⌋·q) frente a la original sin redondear, frente a la misma redondeada a
    otra rejilla y frente a otra truncada a otra rejilla, y la serie a cifras significativas truncada (se espera 0);
  - falsos positivos: pares de series distintas (dos índices con ρ ≈ 0,995, un índice y su rentabilidad total) con una o
    las dos truncadas, que se toman por copias (se espera 0).
Los fondos frente a su índice con un error de seguimiento pequeño no se miden aquí: con rejillas gruesas ya se toman por
copias redondeados (límite declarado en INC-T127-01, rondas T-144 y T-149; `.docs/tickets/T-149/medir_copias.py`)."""
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
    spec = importlib.util.spec_from_file_location("bloque_a.motor.frontera_b_medida", a.modulo)
    fb = importlib.util.module_from_spec(spec)
    fb.__package__ = "bloque_a.motor"
    spec.loader.exec_module(fb)
else:
    from bloque_a.motor import frontera_b as fb
from bloque_a.motor import fichas_mon_idx as fm

FECHAS = pd.bdate_range("2025-06-02", periods=320)
ANIOS = np.asarray((FECHAS - FECHAS[0]).days, dtype=float) / fm.DIAS_ANIO
REJILLAS = {100.0: (0.01, 0.05, 0.25, 1 / 8, 1 / 32), 12.0: (0.01, 0.05, 1 / 32), 2.0: (0.001, 0.01)}


def juntas(x, y):
    g = fb._etiquetas_series_copiadas(np.vstack([x, y]), ANIOS, fb.FRONTERA_B["tolerancia_clon"], 1.0)
    return bool(g[0] == g[1])


def trunc(x, q):
    return np.floor(x / q + 1e-9) * q


def red(x, q):
    return np.round(x / q) * q


def sig_trunc(x, k):
    e = np.floor(np.log10(x)) - (k - 1)
    return np.floor(x / 10.0 ** e + 1e-9) * 10.0 ** e


def paseo(rng, nivel, sd=0.011):
    return nivel * np.cumprod(1 + rng.normal(0.0003, sd, len(FECHAS)))


print(f"{a.semillas} semillas · copias no agrupadas (se espera 0)")
for nivel, rejillas in REJILLAS.items():
    for q in rejillas:
        cuenta = {"truncada / original": 0, "truncada / redondeada 2 dec.": 0, "truncada / truncada 0,001": 0}
        for s in range(a.semillas):
            x = paseo(np.random.default_rng(9000 + s), nivel)
            t = trunc(x, q)
            cuenta["truncada / original"] += not juntas(x, t)
            cuenta["truncada / redondeada 2 dec."] += not juntas(red(x, 0.01), t) if q != 0.01 else 0
            cuenta["truncada / truncada 0,001"] += not juntas(trunc(x, 0.001), t) if q != 0.001 else 0
        print(f"  nivel {nivel:5g}  {q:<8g} " + "  ".join(f"{k}: {v:3d}" for k, v in cuenta.items()), flush=True)
k = sum(not juntas(x, sig_trunc(x, 4)) for x in (paseo(np.random.default_rng(9500 + s), 99.0, 0.006) for s in range(a.semillas)))
print(f"  4 cifras significativas truncadas alrededor de 100: {k}")

print(f"{a.semillas} semillas · falsos positivos con series truncadas (se espera 0)")
for nivel, rejillas in REJILLAS.items():
    for q in rejillas:
        cuenta = {"índices, una truncada": 0, "índices, las dos": 0, "rent. total, una truncada": 0}
        for s in range(a.semillas):
            rng = np.random.default_rng(7000 + s)
            m = rng.normal(0.0003, 0.011, len(FECHAS))
            x = nivel * np.cumprod(1 + m)
            y = nivel * np.cumprod(1 + m + rng.normal(0, 0.0011, len(FECHAS)))
            rt = x * (1 + 0.02) ** ANIOS
            cuenta["índices, una truncada"] += juntas(red(x, q), trunc(y, q))
            cuenta["índices, las dos"] += juntas(trunc(x, q), trunc(y, q))
            cuenta["rent. total, una truncada"] += juntas(red(x, q), trunc(rt, q))
        print(f"  nivel {nivel:5g}  {q:<8g} " + "  ".join(f"{k}: {v:3d}" for k, v in cuenta.items()), flush=True)
