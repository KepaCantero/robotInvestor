"""CT-23 BLOQUEANTE: si afecta a TODOS los tipos del alcance (o no declara clases), no se pausa nada."""
import tempfile, pathlib, json
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
cfg = cargar_config(extra={"modo": "backtest"})
b = Bloque(cfg, ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
q = {"tipo": "ACLARACION_ALCANCE", "modo": "BLOQUEANTE", "clases": ["CRI"],
     "preguntas": [{"texto": "¿Incluimos stablecoins?", "supuesto_declarado": "No", "efecto_si_falso": "cambia el ámbito"}]}
print("consulta:", b.consultas.enviar(q, "2026-06-05"))
print("clases_pausadas(['CRI']):", b.consultas.clases_pausadas("2026-06-05", ["CRI"]))
r = b.ciclo("2026-06-05", alcance={"clases": ["CRI"]})
print("clases analizadas:", list(r["paquete"]["clases"]), "| opciones CRI:", [o["opp_id"] for o in r["paquete"]["clases"]["CRI"]["opciones"]])
print("limitaciones con 'pausado':", [x for x in r["paquete"]["limitaciones"] if "pausado" in x])
q2 = dict(q, clases=[])
c2 = b.consultas.enviar(q2, "2026-06-05")
print("BLOQUEANTE sin clases -> pausadas en RV,RF:", b.consultas.clases_pausadas("2026-06-05", ["RV", "RF"]))
