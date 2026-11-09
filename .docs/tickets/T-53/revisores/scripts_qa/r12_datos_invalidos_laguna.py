"""r12 · CA-02 + CA-06: un CSV con un solo cierre no numérico hace que el símbolo se excluya del ciclo. ¿Con qué motivo
se declara? ¿Queda incidencia en HA? (la serie tiene datos; lo que tiene es un valor inválido)."""
import pathlib, shutil, tempfile
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
datos = tmp / "datos"; shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", datos)
p = datos / "EURUSD=X.csv"; lin = p.read_text().splitlines()
k = next(i for i, l in enumerate(lin) if l.startswith("2023-03-01"))
c = lin[k].split(","); c[4] = "n.d."; lin[k] = ",".join(c); p.write_text("\n".join(lin) + "\n")
b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(datos), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
r = b.ciclo("2026-06-05", alcance={"clases": ["DIV"]})
print("limitaciones DIV:", [x for x in r["paquete"]["limitaciones"] if "Divisas" in x])
print("incidencias HA con EURUSD:", [(e.get("tipo"), e.get("detalle")[:80]) for e in b.almacen.leer("HA") if "EURUSD" in str(e.get("detalle"))][:3])
