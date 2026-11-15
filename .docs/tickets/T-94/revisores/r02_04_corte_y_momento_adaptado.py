"""QA r02 de T-94 · Adaptación de r01_04: el punto 5 (NaN en el corte) acepta que momento se detenga con BancoError;
el resto, igual que r01.

r01 · Fecha de corte (fuga de datos futuros) y «mismo número de selecciones» en las referencias.

1. Momento: alterar el cierre del día siguiente al corte (y todos los posteriores) no cambia la selección; alterar el del
   propio día de corte sí puede cambiarla (prueba de que la frontera está donde se dice).
2. Momento con historia corta (< ventana): ¿se detiene o devuelve menos selecciones en silencio?
3. Azar con más selecciones del titular que miembros en la clase: ¿se detiene o recorta en silencio?
4. Evaluador: cambiar precios posteriores a la fecha de resolución no cambia el exceso; cambiar precios anteriores a la
   fecha de corte tampoco.
5. Momento con NaN dentro de la ventana: ¿orden estable y con sentido?
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r02_04_corte_y_momento_adaptado.py [<carpeta de banco_medida.py>]"""
import sys
from pathlib import Path

import numpy as np
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


fechas = pd.bdate_range("2025-01-01", periods=200)
rng = np.random.default_rng(3)
sims = [f"M{i}" for i in range(5)]
U = pd.DataFrame({"simbolo": sims, "clase": ["C"] * 5})
precios = {s: pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(fechas)))), index=fechas) for s in sims}
corte = fechas[120]
pl = [{"fecha_asof": corte.strftime("%Y-%m-%d"), "clase": "C", "simbolo": "?", "direccion": d, "horizonte": "H"}
      for d in ("LARGO", "LARGO", "CORTO")]
base = [x["simbolo"] for x in bm.momento(pl, U, precios, 63)]

# 1. frontera exacta
for desplaz in (1, 2, 50):
    alt = {k: v.copy() for k, v in precios.items()}
    for k in alt:
        alt[k].iloc[120 + desplaz:] = alt[k].iloc[120 + desplaz:] * (1000 if k == base[-1] else 0.001)
    ok([x["simbolo"] for x in bm.momento(pl, U, alt, 63)] == base, f"momento: alterar desde el corte+{desplaz} sesiones no cambia la selección")
alt = {k: v.copy() for k, v in precios.items()}
alt[base[-1]].iloc[120] *= 10   # el cierre del propio día de corte sí cuenta
ok([x["simbolo"] for x in bm.momento(pl, U, alt, 63)] != base, "momento: el cierre del día de corte sí entra (la frontera es <= corte)")

# 2. historia corta: menos sesiones que la ventana
pl_temprano = [dict(p, fecha_asof=fechas[30].strftime("%Y-%m-%d")) for p in pl]
try:
    out = bm.momento(pl_temprano, U, precios, 63)
    print(f"   momento con 31 sesiones de historia y ventana 63: {len(out)} selecciones de {len(pl_temprano)}")
    ok(len(out) == len(pl_temprano), "momento con historia corta: mismo número de selecciones que el titular (o se detiene)")
except bm.BancoError as e:
    ok(True, f"momento con historia corta → BancoError: {e}")

# 2b. Un solo miembro con historia corta: ¿cuenta para la clase?
alt = dict(precios)
alt["M0"] = precios["M0"].iloc[100:]   # empieza tarde
out = bm.momento(pl, U, alt, 63)
ok(len(out) == 3, "momento: un miembro sin historia suficiente no reduce el número de selecciones")

# 3. azar con más filas que miembros
pl6 = [dict(pl[0]) for _ in range(7)]
try:
    out = bm.azar(pl6, U, 7)
    print(f"   azar con 7 filas del titular y 5 miembros: {len(out)} selecciones")
    ok(len(out) == len(pl6), "azar: mismo número de selecciones que el titular (o se detiene con motivo)")
except bm.BancoError as e:
    ok(True, f"azar con más filas que miembros → BancoError: {e}")

# 4. evaluador: precios fuera de [corte, resolución] no influyen
fin = lambda ini, h: pd.Timestamp(ini) + pd.Timedelta(days=30)
sel = [{"fecha_asof": corte.strftime("%Y-%m-%d"), "clase": "C", "simbolo": "M1", "direccion": "LARGO", "horizonte": "H"}]
e0 = bm.evaluar(sel, precios, U, fin)[0]["exceso"]
fin_ts = fin(corte, "H")
alt = {k: v.where(v.index <= fin_ts, v * 7) for k, v in precios.items()}
ok(bm.evaluar(sel, alt, U, fin)[0]["exceso"] == e0, "evaluador: precios posteriores a la resolución no cambian el exceso")
alt = {k: v.where(v.index >= corte, v * 7) for k, v in precios.items()}
ok(bm.evaluar(sel, alt, U, fin)[0]["exceso"] == e0, "evaluador: precios anteriores al corte no cambian el exceso")

# 5. NaN dentro de la ventana de momento
alt = {k: v.copy() for k, v in precios.items()}
alt["M2"].iloc[120] = np.nan
try:   # r02: el banco 0.3.0 se detiene ante el NaN; antes lo ordenaba por accidente
    out = bm.momento(pl, U, alt, 63)
except bm.BancoError as e:
    out = None
    ok(True, f"momento con un NaN en el cierre de corte de M2 → BancoError: {e}")
if out is not None:
    print(f"   momento con un NaN en el cierre de corte de M2: {[x['simbolo'] for x in out]}")
    puntos_nan = alt["M2"].loc[:corte]
    ok(not np.isnan(puntos_nan.iloc[-1] / puntos_nan.iloc[-64] - 1) or "M2" not in [x["simbolo"] for x in out],
       "momento: un símbolo con NaN en el corte no se elige por accidente del orden")

print(f"\n{len(fallos)} fallo(s)")
for f in fallos:
    print(" -", f)
sys.exit(1 if fallos else 0)
