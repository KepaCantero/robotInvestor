"""T-133 QA r01 · Simulación nula por la ruta NUEVA de `ejecutar_a` (muestra elegida antes de evaluar, H-24).

Las simulaciones nulas de T-94 (`nula_r03.py`, `revisores/r03_09_nula_propia.py`) llaman a `construir_informe` con lo que
devuelve `evaluar` sobre TODAS las fechas: no pasan por el cambio de T-133, que en `ejecutar_a` elige primero la muestra con
el titular y vuelve a evaluar solo dentro de ella. Este script pasa por `ejecutar_a` (con `titular_a` sustituido por un
titular sin habilidad y `--sin-registro`) con el patrón de A: una oportunidad NUEVA que sigue VIGENTE 26 semanas, dos
apuestas a la vez con inicios escalonados, horizonte de 13 semanas y cortes semanales.

Escenarios (24 activos de una clase, precios semanales, factor común y ruido propio):
- P0: sin deriva propia persistente (paseo aleatorio): la referencia de la calibración;
- P1 / P2: cada activo tiene una deriva propia constante en su mundo (0,2 % y 0,4 % semanal de desviación): una apuesta que
  sigue abierta en dos fechas de la muestra aporta dos observaciones correladas de la misma deriva.
Sin habilidad (el titular elige el activo al azar al abrir cada apuesta), el veredicto firme frente a azar debería rondar el
10 % nominal y no pasar del 15 % (techo de CA-3).

Uso: .venv/bin/python -B r01_03_nula_patron_a.py <carpeta de banco_medida.py> [mundos] [escenarios]
"""
import argparse
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[4] / "scripts"
MUNDOS = int(sys.argv[2]) if len(sys.argv) > 2 else 200
ESCENARIOS = sys.argv[3] if len(sys.argv) > 3 else "012"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

N_ACT, SEMANAS, HIST = 24, 560, 40
SEM = pd.date_range("2012-01-06", periods=SEMANAS, freq="7D")
CORTES = list(SEM[HIST:SEMANAS - 14])
SIMS = [f"S{i:02d}" for i in range(N_ACT)]
TMP = Path(tempfile.mkdtemp(prefix="r01_t133_nula_"))
DERIVA = {"0": 0.0, "1": 0.002, "2": 0.004}


def mundo(k: int, sigma_mu: float):
    rng = np.random.default_rng(10_000 + k)
    factor = rng.normal(0, 0.02, SEMANAS)
    mu = rng.normal(0, sigma_mu, N_ACT)
    carpeta = TMP / f"m{k}"
    shutil.rmtree(carpeta, ignore_errors=True)
    carpeta.mkdir()
    fechas = SEM.strftime("%Y-%m-%d")
    for i, s in enumerate(SIMS):
        r = factor + mu[i] + rng.normal(0, 0.03, SEMANAS)
        cierre = 100 * np.exp(np.cumsum(r))
        (carpeta / f"{s}.csv").write_text("fecha,cierre\n" + "".join(f"{d},{c:.6f}\n" for d, c in zip(fechas, cierre)),
                                          encoding="utf-8")
    universo = TMP / f"u{k}.csv"
    universo.write_text("simbolo,clase\n" + "".join(f"{s},C\n" for s in SIMS), encoding="utf-8")
    # Titular sin habilidad con el patrón de A: dos apuestas abiertas, cada una 26 semanas, inicios escalonados 13 semanas
    eleccion = np.random.default_rng(20_000 + k)
    sel, actual = [], [None, None]
    for w, c in enumerate(CORTES):
        for j in (0, 1):
            if (w + 13 * j) % 26 == 0 or actual[j] is None:
                libres = [s for s in SIMS if s != actual[1 - j]]
                actual[j] = libres[int(eleccion.integers(len(libres)))]
            sel.append({"fecha_asof": c.strftime("%Y-%m-%d"), "clase": "C", "simbolo": actual[j], "direccion": "LARGO",
                        "horizonte": "H3"})
    return carpeta, universo, sel


def ejecutar(k: int, sigma_mu: float) -> dict:
    datos, universo, sel = mundo(k, sigma_mu)

    def titular(*a, **kw):
        return {"selecciones": sel, "consumo": {"llamadas": 1, "tokens_entrada": 1, "tokens_salida": 1, "coste_estimado": None},
                "datos": datos, "universo": universo, "fecha_fin": lambda ini, h: ini + pd.Timedelta(weeks=13),
                "advertencias": [], "excluidos_contaminacion": 0}

    bm.titular_a = titular
    ns = argparse.Namespace(desde=CORTES[0].strftime("%Y-%m-%d"), hasta=CORTES[-1].strftime("%Y-%m-%d"),
                            salida=str(TMP / f"s{k}"), cliente="mock", frecuencia=None, clases=None, semilla=7,
                            remuestreos=500, ventana=13, nivel=0.90, min_efectivas=10, registro=None, experimento=None,
                            max_variantes=1, datos=str(datos), universo=str(universo))
    inf = bm.ejecutar_a(ns)
    shutil.rmtree(TMP / f"s{k}", ignore_errors=True)
    shutil.rmtree(datos, ignore_errors=True)
    return inf


for esc in ESCENARIOS:
    firmes_azar = mejor_azar = 0
    ef = []
    for k in range(MUNDOS):
        inf = ejecutar(k, DERIVA[esc])
        c = inf["comparaciones"]["titular_vs_azar"]
        firmes_azar += c["veredicto"] in ("mejor", "peor")
        mejor_azar += c["veredicto"] == "mejor"
        ef.append(c["efectivas"][0])
    tasa = firmes_azar / MUNDOS
    print(f"P{esc} (deriva propia {DERIVA[esc]:.3f}/semana, {MUNDOS} mundos): firmes frente a azar {tasa * 100:.1f} % "
          f"(«mejor» {mejor_azar / MUNDOS * 100:.1f} %); fechas efectivas del titular {min(ef)}–{max(ef)}; "
          f"selecciones en la muestra {inf['plantilla']}; {'OK' if tasa <= 0.15 else 'POR ENCIMA DEL TECHO DE 15 %'}",
          flush=True)
shutil.rmtree(TMP, ignore_errors=True)
