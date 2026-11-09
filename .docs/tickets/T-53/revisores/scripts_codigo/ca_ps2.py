"""PS2 (Anexo A: H1 ≤ 1 día): el ejecutor admite 3 días en H1 (+2 escrito a mano), también entre semana."""
import tempfile, pathlib
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
           cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
f = {"senales": {"fecha_dato": "2026-06-07", "riesgo_1a5": 3}, "_refutacion": {}, "_objeciones": [], "_ps1": True}
print("as_of miércoles 2026-06-10, dato del domingo 07 (3 días), H1 -> PS2 =", b._puertas(f, "N2", "2026-06-10", ["H1"])["PS2"])
