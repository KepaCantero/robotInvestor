"""QA r03 de T-94 · Simulación nula propia con fechas suficientes (calibración del veredicto tras H-13).

Diseño distinto del de r01_02 y r02_02: precios DIARIOS (sesiones hábiles) con colas pesadas (t de Student con 3 grados de
libertad) y saltos, dos clases con volatilidades distintas (RV: 12 activos en 3 subsectores con factor común; DIV: 6 activos),
cortes semanales y ventanas de 4 semanas (las fechas sin solape son 1 de cada 4). El titular no tiene habilidad: cada
semana elige en RV 3 activos de un subsector al azar (un tema) y en DIV 1 activo con dirección al azar. Las referencias son
las del banco (`azar` y `momento`, con la ventana de 63 sesiones), y todo pasa por `evaluar` y `construir_informe`.

Escenarios:
  S  48 semanas → 12 fechas sin solape (justo por encima del mínimo de 10).
  L  160 semanas → 40 fechas sin solape.
  C  24 semanas → 6 fechas con `min_efectivas=5` (la cota más baja que admite el banco).
  R  como S, pero el factor de cada subsector tiene una deriva persistente (AR(1) diario, vida media de unas 60 sesiones) y el
     titular se queda con el mismo tema 12 semanas: ventanas que no se solapan, pero no independientes.
  M  como S, con dos horizontes mezclados (RV a 4 semanas y DIV a 2): la ventana más larga manda.
Mide el porcentaje de mundos con veredicto firme («mejor» o «peor») frente a cada referencia. Nominal: 10 % (nivel 0,90).
Techo de esta prueba: 15 % (el de la QA r02) para S, L y M; R y C se publican como sensibilidad.
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r03_09_nula_propia.py [<carpeta de banco_medida.py>] [mundos] [escenarios]"""
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
MUNDOS = int(sys.argv[2]) if len(sys.argv) > 2 else 200
ESCENARIOS = sys.argv[3] if len(sys.argv) > 3 else "SLCRM"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm  # noqa: E402

RV = [f"R{s}{k}" for s in range(3) for k in range(4)]
DIV = [f"D{k}" for k in range(6)]
U = pd.DataFrame({"simbolo": RV + DIV, "clase": ["RV"] * len(RV) + ["DIV"] * len(DIV)})
CONSUMO = {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0, "coste_estimado": None}
SEMANAS = {"S": 48, "L": 160, "C": 24, "R": 48, "M": 48}


def precios(rng, n, persistente):
    t = lambda size: rng.standard_t(3, size=size) / np.sqrt(3.0)   # noqa: E731  (varianza 1)
    out = {}
    factores = []
    for _ in range(3):
        f = 0.008 * t(n)
        if persistente:
            deriva = np.zeros(n)
            for i in range(1, n):
                deriva[i] = 0.9885 * deriva[i - 1] + 0.00005 * rng.normal()
            f = f + deriva
        factores.append(f)
    for s in RV:
        r = factores[int(s[1])] + 0.012 * t(n) + (rng.random(n) < 0.004) * rng.normal(0, 0.06, n)
        out[s] = r
    for s in DIV:
        out[s] = 0.005 * t(n)
    return out


def mundo(args):
    k, esc = args
    rng = np.random.default_rng(10_000 + k)
    semanas = SEMANAS[esc]
    fechas = pd.bdate_range("2023-06-01", periods=110 + 5 * semanas + 40)
    rets = precios(rng, len(fechas), esc == "R")
    P = {s: pd.Series(100 * np.exp(np.cumsum(r)), index=fechas) for s, r in rets.items()}
    cortes = pd.date_range(fechas[100], periods=semanas, freq="7D")
    if esc == "M":
        fin = lambda ini, h: pd.Timestamp(ini) + pd.Timedelta(weeks=4 if h == "H4" else 2)   # noqa: E731
    else:
        fin = lambda ini, h: pd.Timestamp(ini) + pd.Timedelta(weeks=4)   # noqa: E731
    pl, tema = [], None
    for i, c in enumerate(cortes):
        d = c.strftime("%Y-%m-%d")
        if tema is None or esc != "R" or i % 12 == 0:
            tema = int(rng.integers(3))
        for s in rng.choice([x for x in RV if int(x[1]) == tema], size=3, replace=False):
            pl.append({"fecha_asof": d, "clase": "RV", "simbolo": str(s), "direccion": "LARGO", "horizonte": "H4"})
        pl.append({"fecha_asof": d, "clase": "DIV", "simbolo": str(rng.choice(DIV)),
                   "direccion": str(rng.choice(["LARGO", "CORTO"])), "horizonte": "H2" if esc == "M" else "H4"})
    min_ef = 5 if esc == "C" else 10
    cont = {"titular": bm.evaluar(pl, P, U, fin), "azar": bm.evaluar(bm.azar(pl, U, 1000 + k), P, U, fin),
            "momento": bm.evaluar(bm.momento(pl, U, P, 63), P, U, fin)}
    inf = bm.construir_informe(cont, CONSUMO, 2000, k, None, "h", 0.90, min_ef)
    c = inf["comparaciones"]
    return (c["titular_vs_azar"]["veredicto"], c["titular_vs_momento"]["veredicto"], c["titular_vs_azar"]["efectivas"],
            bm.veredicto_conjunto(c))


if __name__ == "__main__":
    fallos = []
    with Pool(3) as pool:
        for esc in ESCENARIOS:
            res = pool.map(mundo, [(k, esc) for k in range(MUNDOS)])
            firmes_a = sum(r[0] in ("mejor", "peor") for r in res) / len(res) * 100
            firmes_m = sum(r[1] in ("mejor", "peor") for r in res) / len(res) * 100
            mejor_conj = sum(r[3] == "mejor" for r in res) / len(res) * 100
            sin_ver = sum("todavía" in r[0] for r in res)
            ef = sorted(min(r[2]) for r in res)
            techo = 15.0
            marca = "OK   " if (esc in "RC" or max(firmes_a, firmes_m) <= techo) else "FALLO "
            linea = (f"escenario {esc}: firmes frente a azar {firmes_a:.1f} %, frente a momento {firmes_m:.1f} %; «mejor» conjunto "
                     f"{mejor_conj:.1f} %; fechas efectivas (mín. por lado) mediana {ef[len(ef) // 2]}, rango {ef[0]}–{ef[-1]}; "
                     f"{len(res)} mundos")
            print(marca + linea, flush=True)
            if marca.startswith("FALLO"):
                fallos.append(linea)
    print(f"\n{len(fallos)} escenario(s) por encima del techo de {15} %")
    for f in fallos:
        print(" -", f)
    sys.exit(1 if fallos else 0)
