"""r02 · CA-04: BLOQUEANTE que pausa todo el alcance. ¿Qué entrega el run? ¿Estado, limitaciones, G3, entregables?
Y una BLOQUEANTE sin clases en un ciclo de 2 tipos."""
import tempfile, pathlib, json
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
           cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
q = {"tipo": "ACLARACION_ALCANCE", "modo": "BLOQUEANTE", "clases": ["CRI"],
     "preguntas": [{"texto": "¿Incluimos stablecoins?", "supuesto_declarado": "No", "efecto_si_falso": "cambia el ámbito"}]}
b.consultas.enviar(q, "2026-06-05")
r = b.ciclo("2026-06-05", alcance={"clases": ["CRI"]})
print("estado:", r["estado"], "| g3:", r["g3"].get("dictamen"), "| clases en paquete:", list(r["paquete"]["clases"]))
print("limitaciones pausado:", [x for x in r["paquete"]["limitaciones"] if "pausado" in x])
print("entregables:", json.dumps(r.get("entregables"), default=str)[:400])
print("archivos:", sorted(str(p.relative_to(tmp)) for p in (tmp / "s").rglob("*") if p.is_file())[:10])
# sin clases, ciclo de 2 tipos
tmp2 = pathlib.Path(tempfile.mkdtemp(dir="."))
b2 = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
            cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp2 / "e", tmp2 / "s")
b2.consultas.enviar(dict(q, clases=[]), "2026-06-05")
r2 = b2.ciclo("2026-06-05", alcance={"clases": ["RV", "RF"]})
print("sin clases -> estado:", r2["estado"], "| clases en paquete:", list(r2["paquete"]["clases"]),
      "| pausado:", [x for x in r2["paquete"]["limitaciones"] if "pausado" in x])
print("entrega:", r.get("entrega"), "| g3_entregables:", json.dumps(r.get("g3_entregables"), default=str, ensure_ascii=False)[:900])
