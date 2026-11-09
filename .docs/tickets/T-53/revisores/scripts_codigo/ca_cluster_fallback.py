"""ML-CLUS-001 rechazado → cada indicador en su propio clúster: la regla de diversidad (9.6.3) queda desactivada y
«apuestas_independientes» se sobrestima, sin limitación declarada en el paquete."""
import tempfile, pathlib
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
def corrida(rechazar):
    tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
    b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
               cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
    if rechazar:
        real = b.motor.servir
        b.motor.servir = lambda pet, *a, **k: ({"estado": "RECHAZADO", "motivo": "simulado"} if pet["operacion"] == "ML-CLUS-001" else real(pet, *a, **k))
    r = b.ciclo("2026-06-05", alcance={"clases": ["RV", "IDX"]})
    p = r["paquete"]
    return p["apuestas_independientes"], sum(len(d["opciones"]) for d in p["clases"].values()), [x for x in p["limitaciones"] if "clúster" in x.lower() or "ML-CLUS" in x]
print("normal     (apuestas, opciones, limitaciones):", corrida(False))
print("ML-CLUS KO (apuestas, opciones, limitaciones):", corrida(True))
