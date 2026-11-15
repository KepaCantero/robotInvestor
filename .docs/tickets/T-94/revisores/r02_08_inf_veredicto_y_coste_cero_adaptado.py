"""QA r02 de T-94 · Adaptación de r01_08: ante el cierre infinito se espera BancoError (fallo cerrado) y la clave
del coste por selección es «por_seleccion_resuelta»; el coste cero se comprueba con precios finitos.

r01 · Un solo cierre infinito da un veredicto firme; coste estimado 0 sale como «sin dato».

Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r02_08_inf_veredicto_y_coste_cero_adaptado.py [<carpeta de banco_medida.py>]"""
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
try:   # r02: el banco 0.3.0 se detiene ante el cierre infinito; antes daba un veredicto firme
    bm.evaluar(tit, precios, U, fin)
    ok(False, "un cierre infinito en la cesta no detiene el banco")
except bm.BancoError as e:
    ok(True, f"un cierre infinito en la cesta → BancoError: {e}")
# El coste: la clave «coste_por_seleccion_resuelta» pasó a «por_seleccion_resuelta»["coste_estimado"]; precios finitos.
precios["Z"] = serie([100, 90, 81])
et, er = bm.evaluar(tit, precios, U, fin), bm.evaluar(ref, precios, U, fin)
inf = bm.construir_informe({"titular": et, "azar": er}, {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0,
                                                       "coste_estimado": 0.0}, 200, 1, None, "h")
ps = inf["coste"]["por_seleccion_resuelta"]
print(f"   coste estimado 0,0 → por selección resuelta = {ps}")
ok(ps is not None and ps["coste_estimado"] == 0.0, "coste estimado 0,0 con selecciones resueltas → 0,0 por selección (no «sin dato»)")
md = bm.informe_md(inf, "t")
ok("por selección resuelta" in md.lower() and f"coste estimado {ps['coste_estimado']}" in md,
   "el informe.md muestra el coste por selección resuelta (lo pide el diseño)")
print(f"\n{len(fallos)} fallo(s)")
sys.exit(1 if fallos else 0)
