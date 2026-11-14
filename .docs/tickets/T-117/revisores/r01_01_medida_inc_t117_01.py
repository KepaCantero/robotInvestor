"""QA r01 de T-117 · Repite por cuenta propia la medida de INC-T117-01.

Señal compuesta de los doce tipos de activo con `Bloque.senales_clase` (datos de ejemplo, MockClient) en una muestra de
fechas propia (viernes cada 3 semanas desde el 15-08-2025; la del implementador era cada 4 desde el 04-07-2025). Por tipo: ámbitos por fecha con señal ≥ 0,75 y ≥ 0,65, con y sin la concordancia
de dos familias. Uso, desde bloque_a/11_Ejecutor:  python <este fichero> [n_fechas [inicio [frecuencia]]]   (17 2025-07-04 4W-FRI repite la muestra del implementador)
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "tests")]
import pandas as pd
from bloque_a.configuracion import CLASES
from conftest import config_pruebas
from test_t101_v6 import _bloque

N = int(sys.argv[1]) if len(sys.argv) > 1 else 15
INICIO = sys.argv[2] if len(sys.argv) > 2 else "2025-08-15"
FREC = sys.argv[3] if len(sys.argv) > 3 else "3W-FRI"
FECHAS = [str(d.date()) for d in pd.date_range(INICIO, periods=N, freq=FREC)]
res = {c: {"universo": [], "075": [], "065": [], "065_fam2": [], "075_fam2": [], "neutra": 0, "con_tendencia": 0} for c in CLASES}
with tempfile.TemporaryDirectory() as tmp:
    for i, fecha in enumerate(FECHAS):
        b = _bloque(Path(tmp) / str(i), config_pruebas(diseno="v6"))
        b.fijar_fecha(fecha)
        for c in CLASES:
            try:
                tabla = b.senales_clase(c, pd.Timestamp(fecha), "RUN-2026-0001")[0]
            except Exception as e:  # noqa: BLE001
                print(f"{fecha} {c}: {type(e).__name__}: {e}"[:160]); continue
            sen = [(t.get("senal_compuesta"), t.get("familias_concordantes"), t.get("tendencia_26s")) for t in tabla.values()]
            sen = [x for x in sen if x[0] is not None]
            r = res[c]
            r["universo"].append(len(sen))
            r["075"].append(sum(s >= 0.75 for s, _, _ in sen)); r["065"].append(sum(s >= 0.65 for s, _, _ in sen))
            r["075_fam2"].append(sum(s >= 0.75 and f >= 2 for s, f, _ in sen)); r["065_fam2"].append(sum(s >= 0.65 and f >= 2 for s, f, _ in sen))
            r["neutra"] += sum(t == "sin tendencia" for _, _, t in sen); r["con_tendencia"] += sum(t is not None for _, _, t in sen)
m = lambda v: round(sum(v) / len(v), 2) if v else None
print(f"fechas ({len(FECHAS)}): {FECHAS[0]} … {FECHAS[-1]}")
print("tipo  ámbitos  ≥0,75  ≥0,75+2fam  ≥0,65  ≥0,65+2fam  tendencia neutra")
for c in CLASES:
    r = res[c]
    print(f"{c:<5} {m(r['universo']):>6}  {m(r['075']):>5}  {m(r['075_fam2']):>10}  {m(r['065']):>5}  {m(r['065_fam2']):>10}  "
          f"{(r['neutra'] / r['con_tendencia'] if r['con_tendencia'] else float('nan')):>6.0%}")
json.dump({c: {k: (m(v) if isinstance(v, list) else v) for k, v in r.items()} for c, r in res.items()}, sys.stdout); print()
