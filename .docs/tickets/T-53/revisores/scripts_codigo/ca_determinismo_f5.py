import tempfile, pathlib, json
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
def corrida():
    tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
    b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
               cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
    b.ciclo("2026-06-05")
    return [json.loads(l) for l in (tmp / "e" / "F5_historial_analisis.jsonl").read_text().splitlines()]
def dif(x, y, ruta=""):
    if type(x) != type(y): return [ruta]
    if isinstance(x, dict):
        return [r for k in sorted(set(x) | set(y)) for r in dif(x.get(k), y.get(k), f"{ruta}.{k}")]
    if isinstance(x, list):
        return [ruta + "[len]"] if len(x) != len(y) else [r for i, (a, b) in enumerate(zip(x, y)) for r in dif(a, b, f"{ruta}[{i}]")]
    return [] if x == y else [f"{ruta}: {str(x)[:60]} != {str(y)[:60]}"]
a, b = corrida(), corrida()
for i, (x, y) in enumerate(zip(a, b)):
    d = [r for r in dif(x, y) if not r.startswith(("._hash", "._hash"))]
    if d: print(i, x.get("tipo_entrada"), d[:6])
