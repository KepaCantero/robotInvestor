"""T-173 r02 (QA r01, H-03): tasa de degradaciones falsas con la regla de la r02, frente a la de la r01.

Celda SIN pérdida (pronóstico y referencia con el mismo Brier esperado, el modelo de `revisores/r01_tasa_falsa.py`), un PRG
resuelto por semana (un conglomerado PA-03 por PRG, así que n_eff = n), DM-HLN h = 1 con la p unilateral de «pierde»:
- r01: una mirada en cada C5 semanal desde n = 30, α = 0,10 por celda, sin Holm;
- r02: una mirada por revisión mensual (cada 4 semanas) desde n = 30, y Holm entre las celdas de la misma revisión.
Familia: `M` celdas H1–H4 en «Sí», todas sin pérdida. Se dan la tasa por celda y la de la familia (alguna celda degradada).
Cierre de la QA r02 (H-06, decisión por delegación del operador del 17-11-2026, opción b): la familia de Holm es fija, las
`FAMILIA` celdas H1–H4 en «Sí» del bloque (32 en la tabla 8.3), y las que no tienen muestra cuentan como no rechazables.
Se mide también la potencia (probabilidad de degradar) de una celda que SÍ pierde, con α entero y con la familia fija.
Uso (desde la raíz): .venv/bin/python .docs/tickets/T-173/r02_tasa_falsa.py"""
import sys

import numpy as np

sys.path.insert(0, "bloque_a/11_Ejecutor")
from bloque_a.motor.evaluacion import diebold_mariano_hln, holm  # noqa: E402

rng = np.random.default_rng(173)
SIMS, ALFA, NMIN, M, SEMANAS, FAMILIA = 1000, 0.10, 30, 12, 52, 32


def p_celda(T):
    q = rng.uniform(0.3, 0.7, T); o = (rng.random(T) < q).astype(float)
    p = np.clip(q + rng.normal(0, np.sqrt(0.4 ** 2 / 12), T), 0.01, 0.99)   # E[(p-o)^2] ≈ E[(0,5-o)^2]
    d = (0.5 - o) ** 2 - (p - o) ** 2
    return [diebold_mariano_hln(d[:n], np.zeros(n), 1)["p_unilateral"] for n in range(NMIN, T + 1)]   # p por semana


def tasas(miradas, con_holm, familia=None):
    """`miradas`: índices de semana (desde n = 30) en que se revisa. Devuelve por celda (trimestre, año) y por familia."""
    celda_t = celda_a = fam_rev = fam_a = 0
    revisiones = 0
    for _ in range(SIMS):
        P = np.array([p_celda(NMIN + SEMANAS) for _ in range(M)])   # M × semanas
        deg = np.zeros((M, len(miradas)), bool)
        for j, w in enumerate(miradas):
            ps = {str(i): P[i, w] for i in range(M)}
            if familia:                                     # familia fija: el resto de celdas, sin muestra (p ausente)
                ps.update({f"x{j}": None for j in range(familia - M)})
            u = holm(ps, ALFA) if con_holm else {k: ALFA for k in ps}
            deg[:, j] = [ps[str(i)] <= u[str(i)] for i in range(M)]
            fam_rev += deg[:, j].any(); revisiones += 1
        trimestre = [j for j, w in enumerate(miradas) if w < 13]
        celda_t += deg[0, trimestre].any(); celda_a += deg[0].any(); fam_a += deg.any()
    return {"celda_trimestre": round(celda_t / SIMS, 3), "celda_anio": round(celda_a / SIMS, 3),
            "familia_por_revision": round(fam_rev / revisiones, 3), "familia_anio": round(fam_a / SIMS, 3)}


def potencia(sigma, umbral, miradas, sims=SIMS):
    """Una celda que pierde: el pronóstico es la probabilidad verdadera con un ruido N(0, sigma) (más error que la referencia de
    0,5 cuando sigma² > 0,4²/12). Probabilidad de que se degrade en la primera mirada, en un trimestre y en un año."""
    r = {"primera": 0, "trimestre": 0, "anio": 0}
    for _ in range(sims):
        T = NMIN + SEMANAS
        q = rng.uniform(0.3, 0.7, T); o = (rng.random(T) < q).astype(float)
        p = np.clip(q + rng.normal(0, sigma, T), 0.01, 0.99)
        d = (0.5 - o) ** 2 - (p - o) ** 2
        hits = [diebold_mariano_hln(d[:NMIN + w], np.zeros(NMIN + w), 1)["p_unilateral"] <= umbral for w in miradas]
        r["primera"] += hits[0]; r["trimestre"] += any(h for w, h in zip(miradas, hits) if w < 13); r["anio"] += any(hits)
    return {k: round(v / sims, 3) for k, v in r.items()}


semanal = list(range(SEMANAS))
mensual = list(range(0, SEMANAS, 4))
print(f"{SIMS} simulaciones, {M} celdas sin pérdida, α = {ALFA}, n ≥ {NMIN}, {SEMANAS} semanas")
print("r01 (cada C5, sin Holm):    ", tasas(semanal, False))
print("solo mensual, sin Holm:     ", tasas(mensual, False))
print("r02 (mensual y con Holm):   ", tasas(mensual, True))
print(f"cierre (mensual, Holm con la familia fija de {FAMILIA}): ", tasas(mensual, True, FAMILIA))
M = 1
print(f"una celda, mensual, α entero (r02):            ", tasas(mensual, True))
print(f"una celda, mensual, familia fija de {FAMILIA} (cierre):", tasas(mensual, True, FAMILIA))
for sigma in (0.18, 0.25):
    print(f"potencia, σ = {sigma}: α = {ALFA}:", potencia(sigma, ALFA, mensual), f"· α/{FAMILIA}:", potencia(sigma, ALFA / FAMILIA, mensual))
