"""T-152 (QA r01 de T-150, H-02) · el umbral del desplazamiento de la hipótesis truncada de IDX-CONC-001, del 1 al 10 %.

Uso, desde la raíz del repositorio:  .venv/bin/python -I .docs/tickets/T-152/medir_umbral.py [--semillas N]

`motor/frontera_b.py` desplaza la cota de un precio a la hipótesis truncada solo si su paso entero no pasa de un umbral:
q/p ≤ `tolerancia_clon` (1 %) en T-150; q/p ≤ 2·`tolerancia_clon` (2 %) desde la decisión del operador del 16-11-2026,
tomada con esta medida (INC-T127-01, ronda T-152). Este script construye en memoria el mismo
módulo con el umbral al 1, 2, 5 y 10 % y mide, en tres tramos de q/p (paso 0,01 con precios entre 0,55 y 0,95, entre
0,42 y 0,55, entre 0,22 y 0,42 y entre 0,11 y 0,19, sin cruzar de década):
- copias truncadas frente a la original (cuántas NO se agrupan: lo que se pierde);
- series distintas que se siguen de cerca (ρ 0,999 y 0,9999 de sus rentabilidades diarias), las dos redondeadas, las
  dos truncadas o una y una (cuántas SÍ se agrupan: falsos positivos; IDX-CONC-001 deja de servir la amplitud);
- y, fuera de los tramos, el monetario casi siempre a 1,00 frente a otro que crece a 2 decimales (QA r01 de T-150).
Solo informa: termina con 0. Sin red ni coste. Semillas fijas: el resultado se repite."""
import argparse
import sys
import types
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "bloque_a" / "11_Ejecutor"))
import bloque_a.motor.operaciones  # noqa: F401  (carga el registro de fichas, como el Motor)
from bloque_a.motor import fichas_mon_idx as fm
from bloque_a.motor import frontera_b as fb

LINEA = "    desplaza = rel <= tol\n"   # q/p ≤ 2·`tolerancia_clon` desde la decisión del operador (16-11-2026)
UMBRALES = (0.01, 0.02, 0.05, 0.10)
TRAMOS = ((0.55, 0.95), (0.42, 0.55), (0.22, 0.42), (0.11, 0.19))
PASO = 0.01
F = pd.bdate_range("2025-06-02", periods=320)
AN = np.asarray((F - F[0]).days, dtype=float) / fm.DIAS_ANIO


def modulo(umbral: float):
    fuente = Path(fb.__file__).read_text(encoding="utf-8")
    assert fuente.count(LINEA) == 1, "la línea del umbral ha cambiado: actualiza este script"
    m = types.ModuleType(f"bloque_a.motor.frontera_b_u{umbral}")
    m.__package__, m.__file__ = "bloque_a.motor", fb.__file__
    exec(compile(fuente.replace(LINEA, f"    desplaza = 2 * rel <= {umbral!r}\n"), m.__name__, "exec"), m.__dict__)  # noqa: S102
    return m


def juntas(m, x, y) -> bool:
    g = m._etiquetas_series_copiadas(np.vstack([x, y]), AN, fb.FRONTERA_B["tolerancia_clon"], 1.0)
    return bool(g[0] == g[1])


def camino(lo: float, hi: float, rng) -> np.ndarray:
    """Un paseo aleatorio llevado al tramo [lo, hi]: cambia de precio sin salir del tramo de q/p."""
    u = np.cumsum(rng.normal(0, 0.03, len(F)))
    return lo + (hi - lo) * (u - u.min()) / (u.max() - u.min())


def tr(x, q):
    return np.floor(x / q) * q


def rd(x, q):
    return np.round(x / q) * q


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--semillas", type=int, default=100)
    n = ap.parse_args().semillas
    mods = {u: modulo(u) for u in UMBRALES}
    cab = " | ".join(f"{u:.0%}" for u in UMBRALES)
    print(f"| Caso | q/p | {cab} |\n| --- | --- | {' | '.join('---' for _ in UMBRALES)} |")
    for lo, hi in TRAMOS:
        qp = f"{PASO / hi:.1%} a {PASO / lo:.1%}"
        cuenta = dict.fromkeys(UMBRALES, 0)
        for s in range(n):
            x = camino(lo, hi, np.random.default_rng(1000 + s))
            for u in UMBRALES:
                cuenta[u] += not juntas(mods[u], x, tr(x, PASO))
        print(f"| copia truncada sin agrupar | {qp} | {' | '.join(f'{cuenta[u]} de {n}' for u in UMBRALES)} |", flush=True)
        for rho in (0.999, 0.9999):
            for o1, o2, nombre in ((rd, rd, "r/r"), (tr, tr, "t/t"), (rd, tr, "r/t")):
                cuenta = dict.fromkeys(UMBRALES, 0)
                for s in range(n):
                    r = np.random.default_rng(2000 + s)
                    x = camino(lo, hi, r)
                    y = x * np.exp(np.cumsum(r.normal(0, 0.01 * np.sqrt(2 * (1 - rho)), len(F))))
                    for u in UMBRALES:
                        cuenta[u] += juntas(mods[u], o1(x, PASO), o2(y, PASO))
                print(f"| distintas, ρ {rho}, {nombre}, agrupadas | {qp} | "
                      f"{' | '.join(f'{cuenta[u]} de {n}' for u in UMBRALES)} |", flush=True)
    cuenta = dict.fromkeys(UMBRALES, 0)
    for s in range(n):
        r = np.random.default_rng(7000 + s)
        x = np.ones(len(F))
        x[r.random(len(F)) < 0.3] = 1.01
        y = np.round(1.01 ** (np.arange(len(F)) / 252) * (1 + r.normal(0, 0.002, len(F))), 2)
        for u in UMBRALES:
            cuenta[u] += juntas(mods[u], x, y)
    print(f"| monetario a 1,00 frente a otro a 2 decimales, agrupados | 1 % a 100 % | "
          f"{' | '.join(f'{cuenta[u]} de {n}' for u in UMBRALES)} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
