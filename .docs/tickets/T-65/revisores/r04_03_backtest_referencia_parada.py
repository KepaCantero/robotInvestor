"""r04_03 · QA T-65 r04 · H-16 en un backtest: la referencia (ACWI, de RV y de IDX) deja de publicarse a mitad.

Uso (desde bloque_a/11_Ejecutor):  ../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r04_03_backtest_referencia_parada.py

Backtest semanal del 2026-03-06 al 2026-05-01 (RV, IDX y DIV; cliente simulado) con ACWI parada el 2026-03-27 y la
resolución final del backtest. Esperado (H-16): (1) ningún ciclo posterior a la parada + `referencias.antiguedad_maxima_dias`
emite PRG frente a ACWI, y lo declara; (2) ningún PRG frente a ACWI queda RESUELTO sin dato de ACWI posterior a su emisión
(rentabilidad 0); (3) los que no se pueden resolver quedan NO_RESOLUBLE, no ABIERTO para siempre; (4) DIV no cambia.
"""
import collections
import pathlib
import shutil
import sys
import tempfile
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path.cwd()))
from bloque_a.backtest import ejecutar_backtest  # noqa: E402
from bloque_a.configuracion import DIR_EJECUTOR, RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402

PARADA = "2026-03-27"
hall = 0
tmp = pathlib.Path(tempfile.mkdtemp(prefix="r04_03_"))
datos = tmp / "datos"
shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", datos)
df = pd.read_csv(datos / "ACWI.csv")
df[df["fecha"] <= PARADA].to_csv(datos / "ACWI.csv", index=False)
cfg = cargar_config(extra={"perfiles": {"activos": ["RV", "IDX", "DIV"]},
                           "evaluacion": {"bootstrap_replicas": 200, "simulaciones_ece": 200}})
res = ejecutar_backtest(cfg, "2026-03-06", "2026-05-01", str(datos), str(RUTA_UNIVERSO_EJEMPLO), str(tmp / "s"),
                        clases=["RV", "IDX", "DIV"])
from bloque_a.almacen import Almacen  # noqa: E402

al = Almacen(tmp / "s" / "estado")
f4 = al.estado("F4")
acwi = pd.read_csv(datos / "ACWI.csv", parse_dates=["fecha"]).set_index("fecha")["cierre"]
emis = collections.Counter()
malos, estados = [], collections.Counter()
for p in f4.values():
    if p.get("referencia_indice") != "ACWI" or p.get("prob_interna") is None:
        continue
    emis[p["fecha_emision"]] += 1
    estados[p.get("estado")] += 1
    if p.get("estado") == "RESUELTO":
        f0, f1 = pd.Timestamp(p["fecha_emision"]), pd.Timestamp(p["fecha_resolucion"])
        d0, d1 = acwi[acwi.index <= f0].index.max(), acwi[acwi.index <= f1].index.max()
        r = p.get("resolucion") or {}
        if d1 <= d0 or r.get("rent_referencia") == 0.0:
            malos.append((p["prg_id"], p["horizonte"], str(f0.date()), str(f1.date()), str(d1.date()), r.get("rent_referencia")))
tardias = sorted(f for f in emis if (pd.Timestamp(f) - pd.Timestamp(PARADA)).days > 7)
print(f"PRG frente a ACWI por fecha de emisión: {dict(sorted(emis.items()))}")
print(f"Estados de esos PRG al final: {dict(estados)}")
if tardias:
    hall += 1
    print(f"HALLAZGO  emisiones con ACWI parada más de 7 días: {tardias}")
else:
    print("OK        ninguna emisión con ACWI parada más de 7 días")
if malos:
    hall += 1
    print(f"HALLAZGO  {len(malos)} PRG RESUELTOS sin dato de ACWI posterior a la emisión, p. ej. {malos[:3]}")
else:
    print("OK        ningún PRG frente a ACWI resuelto sin dato de ACWI posterior a la emisión")
if estados.get("ABIERTO"):
    print(f"INFO      {estados['ABIERTO']} PRG frente a ACWI siguen ABIERTO al final del backtest")
print(f"runs: {[(r['as_of'], r['estado']) for r in res.get('runs', [])] if isinstance(res, dict) else res}")
print(f"HALLAZGOS: {hall}")
