"""QA r01 de T-94 · Un solo cierre infinito da un veredicto firme; coste estimado 0 sale como «sin dato».

Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r01_08_inf_veredicto_y_coste_cero.py [<carpeta de banco_medida.py>]"""
import sys
from pathlib import Path

import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

fallos = []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


def serie(v):
    return pd.Series([float(x) for x in v], index=pd.date_range("2026-01-01", periods=len(v), freq="D"))


U = pd.DataFrame({"simbolo": ["X", "Y", "Z", "P", "Q"], "clase": ["C1", "C1", "C1", "C2", "C2"]})
precios = {"X": serie([100, 110, 121]), "Y": serie([100, 100, 100]), "Z": serie([100, 90, float("inf")]),
           "P": serie([100, 101, 102]), "Q": serie([100, 99, 98])}
fin = lambda ini, h: pd.Timestamp(ini) + pd.Timedelta(days=2)  # noqa: E731
tit = [{"fecha_asof": "2026-01-01", "clase": "C1", "simbolo": "X", "direccion": "LARGO", "horizonte": "H"},
       {"fecha_asof": "2026-01-01", "clase": "C2", "simbolo": "P", "direccion": "LARGO", "horizonte": "H"}]
ref = [dict(tit[1]), dict(tit[1], simbolo="Q")]
et, er = bm.evaluar(tit, precios, U, fin), bm.evaluar(ref, precios, U, fin)
inf = bm.construir_informe({"titular": et, "azar": er}, {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0,
                                                       "coste_estimado": 0.0}, 200, 1, None, "h")
c = inf["comparaciones"]["titular_vs_azar"]
print(f"   un cierre infinito en Z (cesta de C1) → titular {inf['contendientes']['titular']['media']}, comparación {c}")
ok(c["veredicto"] in ("sin datos", "todavía no se sabe") and c["diferencia"] is not None and abs(c["diferencia"]) != float("inf"),
   "un dato infinito no produce un veredicto firme («mejor/peor») ni una diferencia infinita")
print(f"   coste estimado 0,0 → coste por selección resuelta = {inf['coste']['coste_por_seleccion_resuelta']}")
ok(inf["coste"]["coste_por_seleccion_resuelta"] == 0.0, "coste estimado 0,0 con selecciones resueltas → 0,0 por selección (no «sin dato»)")
md = bm.informe_md(inf, "t")
ok("por selección resuelta" in md and "coste" in md.lower() and str(inf["coste"]["coste_por_seleccion_resuelta"]) in md,
   "el informe.md muestra el coste por selección resuelta (lo pide el diseño)")
print(f"\n{len(fallos)} fallo(s)")
sys.exit(1 if fallos else 0)
