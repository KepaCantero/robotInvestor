"""F7: el paquete JSON se escribe en la carpeta de entregables ANTES de validar esquema y coherencia; si esa validación
bloquea la entrega, el archivo queda en disco con «estado_g3» APTO/APTO_CON_ADVERTENCIAS."""
import tempfile, pathlib, json
from bloque_a import redaccion
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
redaccion.coherencia = lambda rutas, js: ["incoherencia simulada entre entregables"]   # simula un fallo de G3-ENT-07
tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
b = Bloque(cargar_config(extra={"modo": "vivo"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
           cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "ent")
r = b.ciclo("2026-06-05", alcance={"clases": ["RV"]})
print("entrega:", r.get("entrega"), "| g3_entregables:", r["g3_entregables"]["dictamen"], r["g3_entregables"]["bloqueos"])
for p in sorted((tmp / "ent").rglob("*")):
    if p.is_file():
        extra = ""
        if p.suffix == ".json":
            extra = " estado_g3=" + str(json.loads(p.read_text(encoding="utf-8")).get("estado_g3"))
        print("  en disco:", p.relative_to(tmp), extra)
print("paquete en memoria estado_g3:", r["paquete"].get("estado_g3"))
