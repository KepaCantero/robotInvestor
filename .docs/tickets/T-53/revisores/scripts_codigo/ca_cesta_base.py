import tempfile, pathlib
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
for c in ("DIV", "FON"):
    r = b.ciclo("2026-06-05", alcance={"clases": [c]})
    print(c, [o["opp_id"] for o in r["paquete"]["clases"][c]["opciones"]], r["gc0"][c]["motivos"][:2], r["paquete"]["clases"][c]["menos_de_tres_motivo"])
