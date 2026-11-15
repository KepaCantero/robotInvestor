"""T-94 r03 · Simulación nula con fechas suficientes: 620 cortes semanales, horizonte de 8 semanas, 24 activos en 4
subsectores con factor común. Sin habilidad, el banco debe dar veredicto firme ~10 % de las veces.
Uso (desde la raíz): .venv/bin/python -B .docs/tickets/T-94/nula_r03.py [n_sim]  (unos 3 s por mundo)"""
import random
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, ".docs/scripts")
import banco_medida as bm

SEM = pd.date_range("2015-01-02", periods=700, freq="7D")
CORTES = list(SEM[30:650])
H = 8
FIN = lambda ini, h: pd.Timestamp(ini) + pd.Timedelta(weeks=H)
SUB = {f"S{i:02d}": i // 6 for i in range(24)}
U = pd.DataFrame({"simbolo": list(SUB), "clase": ["C"] * 24})
C0 = {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0, "coste_estimado": None}
def sim(seed, tema):
    rng, r = np.random.default_rng(seed), random.Random(seed)
    f = rng.normal(0, 0.02, size=(4, len(SEM)))
    p = {s: pd.Series(100*np.exp(np.cumsum(f[g] + rng.normal(0, 0.03, len(SEM)))), index=SEM) for s, g in SUB.items()}
    t = r.randrange(4)
    cands = [s for s in SUB if SUB[s] == t] if tema else list(SUB)
    pl = [{"fecha_asof": c.strftime("%Y-%m-%d"), "clase": "C", "simbolo": r.choice(cands), "direccion": "LARGO", "horizonte": "H"} for c in CORTES]
    inf = bm.construir_informe({"titular": bm.evaluar(pl, p, U, FIN), "azar": bm.evaluar(bm.azar(pl, U, seed), p, U, FIN)}, C0, 500, seed, None, "h")
    c = inf["comparaciones"]["titular_vs_azar"]
    return c["veredicto"] in ("mejor", "peor"), c["efectivas"]
for tema in (False, True):
    res = [sim(2000 + k, tema) for k in range(int(sys.argv[1]) if len(sys.argv) > 1 else 200)]
    print("tema" if tema else "sin tema", sum(x for x, _ in res) / len(res), "efectivas", res[0][1])
