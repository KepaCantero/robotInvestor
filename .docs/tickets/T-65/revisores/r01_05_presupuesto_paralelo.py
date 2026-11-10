"""r01_05 · QA T-65 · CA-15: ¿el consumo por tipo de F5 (presupuesto.consumido) depende del orden de los hilos?

Uso:  <python> r01_05_presupuesto_paralelo.py <dir_11_Ejecutor> [repeticiones]
Repite el mismo ciclo (12 tipos, 4 hilos, carpetas nuevas) y compara presupuesto, participantes y msg_id de F5 y HA.
"""
import json
import sys
import tempfile
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
EJ = Path(sys.argv[1]).resolve()
N = int(sys.argv[2]) if len(sys.argv) > 2 else 4
sys.path.insert(0, str(EJ))
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

todos = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]
vistos = []
for i in range(N):
    tmp = Path(tempfile.mkdtemp(prefix="r01_05_"))
    cfg = cargar_config(extra={"modo": "backtest", "perfiles": {"activos": todos}, "paralelismo": {"hilos_analistas": 4}})
    b = Bloque(cfg, ProveedorCSV(EJ / "ejemplos" / "datos_sinteticos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(),
               tmp / "e", tmp / "s")
    r = b.ciclo("2026-06-05")
    run = next(x for x in b.almacen.leer("F5") if x.get("tipo_entrada") == "RUN" and x.get("id") == r["run_id"])
    msgs = [m["msg_id"] for m in b.mensajeria.registro] if hasattr(b.mensajeria, "registro") else []
    vistos.append({"presupuesto": json.dumps(run["presupuesto"], sort_keys=True),
                   "participantes": json.dumps(run.get("participantes")),
                   "consumo": json.dumps(run.get("consumo"), sort_keys=True),
                   "msg_ids": json.dumps(sorted(msgs)),
                   "paquete": json.dumps(r["paquete"]["clases"], sort_keys=True, default=str)})
for k in vistos[0]:
    distintos = len({v[k] for v in vistos})
    print(f"{k:14s}: {distintos} valor(es) distinto(s) en {N} ejecuciones")
if len({v["presupuesto"] for v in vistos}) > 1:
    a, b2 = json.loads(vistos[0]["presupuesto"]), json.loads(next(v["presupuesto"] for v in vistos if v["presupuesto"] != vistos[0]["presupuesto"]))
    for c in sorted(a):
        if a[c] != b2.get(c):
            print(f"   {c}: {a[c]} vs {b2.get(c)}")
