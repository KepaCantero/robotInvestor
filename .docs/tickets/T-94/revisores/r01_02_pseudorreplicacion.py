"""QA r01 de T-94 · ¿Afirma el banco más de lo que mide? Tasa de falsos «mejor/peor» sin habilidad alguna.

Mundo nulo: precios en paseo aleatorio, sin ninguna señal. Un «titular» sin habilidad elige al azar y, como hace el
Bloque A en el ejemplo (35 de 39 filas de senales.csv son VIGENTE: la misma oportunidad repetida cada semana),
repite la misma elección todas las semanas con horizonte H3 (6 meses), de modo que las ventanas se solapan.
Las referencias son las del banco (`azar`). Con un rango del 90 % honesto, el banco debería decir «mejor» o «peor»
alrededor del 10 % de las veces. Escenarios:
  A) control iid: elección nueva cada semana, horizonte de 5 días (sin solape) → ~10 % esperado;
  B) como A en el ejemplo: 3 oportunidades fijas repetidas 13 semanas, horizonte 6 meses.
  C) muestra mínima: una selección por lado.
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r01_02_pseudorreplicacion.py [<carpeta de banco_medida.py>] [n_sim]"""
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
NSIM = int(sys.argv[2]) if len(sys.argv) > 2 else 200
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

SIMBOLOS = [f"S{i}" for i in range(6)]
UNIVERSO = pd.DataFrame({"simbolo": SIMBOLOS, "clase": ["C"] * 6})
FECHAS = pd.bdate_range("2024-01-01", "2026-12-31")
CORTES = [d.strftime("%Y-%m-%d") for d in pd.date_range("2025-03-07", periods=13, freq="7D")]


def mundo(seed):
    rng = np.random.default_rng(seed)
    return {s: pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(FECHAS)))), index=FECHAS) for s in SIMBOLOS}


def simular(escenario, seed):
    precios = mundo(seed)
    r = random.Random(seed)
    if escenario == "A":
        plantilla = [{"fecha_asof": c, "clase": "C", "simbolo": s, "direccion": "LARGO", "horizonte": "H1"}
                     for c in CORTES for s in r.sample(SIMBOLOS, 3)]
        fin = lambda ini, h: ini + pd.Timedelta(days=5)
    elif escenario == "B":
        fijos = r.sample(SIMBOLOS, 3)
        plantilla = [{"fecha_asof": c, "clase": "C", "simbolo": s, "direccion": "LARGO", "horizonte": "H3"}
                     for c in CORTES for s in fijos]
        fin = lambda ini, h: ini + pd.DateOffset(months=6)
    else:
        plantilla = [{"fecha_asof": CORTES[0], "clase": "C", "simbolo": r.choice(SIMBOLOS), "direccion": "LARGO", "horizonte": "H3"}]
        fin = lambda ini, h: ini + pd.DateOffset(months=6)
    tit = bm.evaluar(plantilla, precios, UNIVERSO, fin)
    az = bm.evaluar(bm.azar(plantilla, UNIVERSO, seed), precios, UNIVERSO, fin)
    d = bm.diferencia([f["exceso"] for f in tit if f["resuelta"]], [f["exceso"] for f in az if f["resuelta"]], 500, seed)
    return d["veredicto"]


fallos = []
for esc, techo in (("A", 0.16), ("B", 0.16), ("C", 0.16)):
    vs = [simular(esc, 10_000 + k) for k in range(NSIM)]
    tasa = sum(v in ("mejor", "peor") for v in vs) / len(vs)
    estado = "OK   " if tasa <= techo else "FALLO"
    print(f"{estado} escenario {esc}: falsos «mejor/peor» sin habilidad = {tasa:.1%} (nominal 10 %, techo de la prueba {techo:.0%})")
    if tasa > techo:
        fallos.append(esc)
print(f"\n{len(fallos)} escenario(s) por encima del techo: {fallos}")
sys.exit(1 if fallos else 0)
