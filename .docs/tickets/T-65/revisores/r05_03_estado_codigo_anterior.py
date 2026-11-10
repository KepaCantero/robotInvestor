"""r05_03 · QA T-65 r05 · Pronósticos emitidos (y resueltos) con el código anterior que sigue el código nuevo.

Uso, en dos fases y con el mismo directorio de trabajo <dir>:
  1. desde bloque_a/11_Ejecutor de una copia con el código ANTERIOR (HEAD sin las correcciones de la r04):
       ../../.venv/bin/python <ruta>/r05_03_estado_codigo_anterior.py emitir <dir>
  2. desde bloque_a/11_Ejecutor con el código NUEVO:
       ../../.venv/bin/python <ruta>/r05_03_estado_codigo_anterior.py seguir <dir>

Fase 1: datos con DBC (referencia de MP) parada el 2026-04-17; ciclos del 2026-04-17 y del 2026-04-24 con H1 (MP, DIV).
El código anterior resuelve los H1 del 17 el día 24 con `rent_referencia` 0 (H-24). Fase 2: ciclos del 2026-05-01 y
2026-05-08 con el código nuevo sobre el mismo estado. Esperado: integridad intacta, ningún fallo, los ABIERTO del 24 con
DBC parada no se resuelven, y se informa de los RESUELTOS con 0 heredados (el código nuevo no los toca, R11).
"""
import json
import pathlib
import shutil
import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path.cwd()))
from bloque_a.configuracion import DIR_EJECUTOR, RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

fase, base = sys.argv[1], pathlib.Path(sys.argv[2])
cfg = cargar_config(extra={"modo": "backtest", "perfiles": {"activos": ["MP", "DIV"]}})
print(f"código: {DIR_EJECUTOR}")
if fase == "emitir":
    base.mkdir(parents=True, exist_ok=True)
    shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", base / "datos")
    df = pd.read_csv(base / "datos" / "DBC.csv")
    df[df["fecha"] <= "2026-04-17"].to_csv(base / "datos" / "DBC.csv", index=False)
fechas = ["2026-04-17", "2026-04-24"] if fase == "emitir" else ["2026-05-01", "2026-05-08"]
b = Bloque(cfg, ProveedorCSV(base / "datos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), base / "e", base / "s")
for f in fechas:
    r = b.ciclo(f, alcance={"clases": ["MP", "DIV"]}, horizontes=["H1"])
    print(f"ciclo {f}: estado={r['estado']} limitaciones={len(r['paquete'].get('limitaciones') or [])}")
integ = b.almacen.verificar_integridad()
f4 = b.almacen.estado("F4", fechas[-1])
filas = []
for p in sorted(f4.values(), key=lambda x: x["prg_id"]):
    if p.get("prob_interna") is None:
        continue
    r = p.get("resolucion") or {}
    filas.append((p["prg_id"], p["clase"], p["horizonte"], p["fecha_emision"], p.get("referencia_indice"), p.get("estado"),
                  r.get("rent_referencia"), r.get("fecha_resuelto"), "fecha_dato_referencia" in r))
for x in filas:
    print("  ", x)
cero = [x for x in filas if x[5] == "RESUELTO" and x[6] == 0.0]
print(f"integridad: {'OK' if all(integ.values()) else integ}")
print(f"RESUELTOS con rent_referencia 0: {len(cero)} (resueltos el {sorted({x[7] for x in cero})})")
if fase == "seguir":
    nuevos_malos = [x for x in cero if x[7] in fechas]
    print(f"{'HALLAZGO' if nuevos_malos or not all(integ.values()) else 'OK':9} con el código nuevo: {len(nuevos_malos)} resueltos con 0; "
          f"integridad {'intacta' if all(integ.values()) else 'rota'}")
    print(f"{'INFO':9} heredados del código anterior (resueltos con 0 y sin las fechas por serie): "
          f"{len([x for x in cero if x[7] not in fechas])}")
(base / f"{fase}.json").write_text(json.dumps(filas, default=str))
