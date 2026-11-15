"""QA r01 de T-144 (revisor) · copias de una serie que la regla de niveles no ve y series distintas que agrupa.

Uso, desde la raíz de la copia:  .venv/bin/python -I .docs/tickets/T-144/revisores/r01_01_copias_otras_rejillas.py
Sin red. Para cada vía de copia se espera amplitud `null` en IDX-CONC-001 (la copia se agrupa); para cada par de series
distintas, que no se agrupen. Además: precios inválidos y orden de las series. Termina con 1 si hay algún hallazgo.

La regla de niveles saca el error de redondeo de cada serie de su «paso de precio», la mayor potencia de 10 de la que
todos sus precios son múltiplos. Una serie en una rejilla que no es una potencia de 10 (pasos de 0,05 o de 0,25, octavos o
treintaidosavos, como algunos mercados y bonos) tiene un error de redondeo mayor que la mitad de ese paso decimal."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "bloque_a" / "11_Ejecutor"))
from bloque_a.motor import fichas_mon_idx as fm
from bloque_a.motor import frontera_b as fb
from bloque_a.motor.operaciones import ErrorFicha

FECHAS = pd.bdate_range("2025-06-02", periods=320)
hallazgos = 0


def paseo(semilla, nivel=100.0, sd=0.01):
    rng = np.random.default_rng(semilla)
    return pd.Series(nivel * np.exp(np.cumsum(rng.normal(0.0005, sd, len(FECHAS)))), index=FECHAS)


def a_rejilla(s, paso):
    return (s / paso).round() * paso


def es_copia(x, y):
    t = pd.DataFrame({"x": x, "y": y}).sort_index()
    g = fb._etiquetas_series_copiadas(t.to_numpy(dtype=float).T, np.asarray((t.index - t.index[0]).days, dtype=float) / fm.DIAS_ANIO,
                                      fb.FRONTERA_B["tolerancia_clon"], 1.0)
    return bool(g[0] == g[1])


def amplitud(series):
    v = {"composicion": fm._composicion(10, igual=False)}
    res, _ = fm.FICHAS["IDX-CONC-001"]["fn"]({"valores": v, "series": series, "series_rol": {}}, {"top_n": 5})
    return res["amplitud"]


def caso(nombre, ok, detalle=""):
    global hallazgos
    hallazgos += not ok
    print(f"{'OK      ' if ok else 'HALLAZGO'} {nombre}" + (f" · {detalle}" if detalle else ""))


# ---------------------------------------------------------------- A. copias en otras rejillas (se esperan agrupadas)
A = paseo(7, 50.0)
VIAS = {
    "paso de 0,05 (rejilla de algunas bolsas)": a_rejilla(A, 0.05),
    "paso de 0,25": a_rejilla(A, 0.25),
    "octavos (1/8)": a_rejilla(A, 1 / 8),
    "treintaidosavos (1/32, bonos)": a_rejilla(A * 2, 1 / 32),
    "dos decimales con un solo precio sin redondear": pd.concat([A.round(2).iloc[:-1], A.iloc[-1:]]),
    "cifras significativas (4)": A.apply(lambda v: float(f"{v:.4g}")),
}
for nombre, copia in VIAS.items():
    sep = es_copia(A, copia)
    amp = amplitud({"C00": A, "SECRETA": copia})
    caso(f"A copia {nombre}: agrupada y sin amplitud", sep and amp is None, f"agrupada={sep} amplitud={'null' if amp is None else 'servida'}")

# ---------------------------------------------------------------- B. series distintas, nunca agrupadas (100 semillas)
cuentas = {"dos índices ρ≈0,995 en rejilla de 0,05": 0, "dos acciones distintas de ~1 € a 2 decimales": 0}
for s in range(100):
    rng = np.random.default_rng(5000 + s)
    m = rng.normal(0.0003, 0.011, len(FECHAS))
    x = pd.Series(100 * np.cumprod(1 + m), index=FECHAS)
    y = pd.Series(100 * np.cumprod(1 + m + rng.normal(0, 0.0011, len(FECHAS))), index=FECHAS)
    cuentas["dos índices ρ≈0,995 en rejilla de 0,05"] += es_copia(a_rejilla(x, 0.05), a_rejilla(y, 0.05))
    p = pd.Series(1.0 * np.cumprod(1 + m), index=FECHAS).round(2)
    q = pd.Series(1.0 * np.cumprod(1 + m + rng.normal(0, 0.004, len(FECHAS))), index=FECHAS).round(2)
    cuentas["dos acciones distintas de ~1 € a 2 decimales"] += es_copia(p, q)
for nombre, n in cuentas.items():
    # la segunda es un límite declarado (paso grande frente al precio: falla cerrado); se informa, no cuenta
    declarado = "~1 €" in nombre
    print(f"{'OBS     ' if declarado else ('OK      ' if n == 0 else 'HALLAZGO')} B {nombre}: {n} de 100 agrupadas")
    hallazgos += (not declarado) and n > 0

# ---------------------------------------------------------------- C. precios inválidos y orden
for nombre, valor in (("cero", 0.0), ("negativo", -1.0), ("infinito", np.inf), ("-infinito", -np.inf)):
    s = A.copy()
    s.iloc[100] = valor
    try:
        amplitud({"C00": A, "MALA": s})
        caso(f"C precio {nombre} rechazado", False, "se aceptó")
    except ErrorFicha:
        caso(f"C precio {nombre} rechazado", True)
B_ = paseo(11, 80.0)
orden1 = amplitud({"C00": A, "C01": B_, "C02": a_rejilla(A, 0.05)})
orden2 = amplitud({"C02": a_rejilla(A, 0.05), "C01": B_, "C00": A})
caso("C el orden de las series no cambia el resultado", orden1 == orden2)

print(f"\n{hallazgos} hallazgos")
sys.exit(1 if hallazgos else 0)
