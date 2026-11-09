"""RI-TB con referencia CESTA: un miembro del universo sin datos hasta as_of (alta posterior) hace caer el ciclo entero."""
import tempfile, pathlib, shutil, traceback
import pandas as pd
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
datos = tmp / "datos"; shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", datos)
fechas = pd.bdate_range("2026-09-01", "2026-10-30")       # par que empieza a cotizar después de as_of
(datos / "USDNEW=X.csv").write_text("fecha,cierre\n" + "\n".join(f"{d.date()},1.0{i % 9}" for i, d in enumerate(fechas)) + "\n")
uni = pathlib.Path(RUTA_UNIVERSO_EJEMPLO).read_text(encoding="utf-8").rstrip("\n") + \
      "\nUSDNEW=X,DIV,Dólar frente a nueva divisa,ESTRATEGIA,GLB,G10,USD,SOLO EJEMPLO,Pares,Par nuevo,Otros cruces,USD/NEW,\n"
(tmp / "u.csv").write_text(uni, encoding="utf-8")
b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(datos), cargar_universo(tmp / "u.csv"), MockClient(), tmp / "e", tmp / "s")
try:
    r = b.ciclo("2026-06-05", alcance={"clases": ["DIV"]})
    print("ciclo OK; opciones DIV:", [o["opp_id"] for o in r["paquete"]["clases"]["DIV"]["opciones"]], "| estado:", r["estado"], "| limitaciones:", [x for x in r["paquete"]["limitaciones"] if "Divisas" in x or "DIV" in x])
except Exception as e:
    tb = traceback.extract_tb(e.__traceback__)
    print("ciclo ABORTADO:", type(e).__name__, e, "| en", [f"{pathlib.Path(t.filename).name}:{t.lineno}" for t in tb][-4:])
d = r["paquete"]["clases"]["DIV"]
print("embudo:", d["embudo"], "| menos_de_tres:", d["menos_de_tres_motivo"][:300])
print("RC rechazos:", [(e["operacion"] if isinstance(e.get("operacion"), str) else e.get("operacion", {}).get("method_id"), e.get("estado"), str(e.get("motivo") or e.get("limitaciones"))[:120]) for e in b.almacen.leer("RC") if e.get("estado") not in ("SERVED",)][:6])
