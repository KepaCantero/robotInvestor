"""QA r01 de T-173: tasa de degradaciones falsas de una celda SIN pérdida (pronóstico y referencia con el mismo Brier
esperado) con la regla implementada: DM-HLN h = 1, p unilateral <= 0,10, n >= 30, evaluada en cada C5 semanal con los
datos acumulados (un PRG por semana), durante 13 semanas (un trimestre) y 52 (un año). Usa la DM del propio Motor."""
import sys
import numpy as np
sys.path.insert(0, "bloque_a/11_Ejecutor")
from bloque_a.motor.evaluacion import diebold_mariano_hln  # noqa: E402

rng = np.random.default_rng(173)
SIMS, ALFA, NMIN = 2000, 0.10, 30
res = {13: 0, 52: 0, "una_mirada": 0}
for _ in range(SIMS):
    T = NMIN + 52
    q = rng.uniform(0.3, 0.7, T); o = (rng.random(T) < q).astype(float)
    p = np.clip(q + rng.normal(0, np.sqrt(0.4 ** 2 / 12), T), 0.01, 0.99)   # E[(p-o)^2] ≈ E[(0,5-o)^2]
    d = (0.5 - o) ** 2 - (p - o) ** 2
    hits = [diebold_mariano_hln(d[:n], np.zeros(n), 1)["p_unilateral"] <= ALFA for n in range(NMIN, T + 1)]
    res["una_mirada"] += hits[0]; res[13] += any(hits[:13]); res[52] += any(hits[:52])
print({k: round(v / SIMS, 3) for k, v in res.items()})
