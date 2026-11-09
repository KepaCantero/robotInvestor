"""Determinismo: dos ejecuciones idénticas del mismo ciclo simulado (12 tipos, hilos=4) ¿producen el mismo estado?"""
import tempfile, pathlib, hashlib, sys
from bloque_a.configuracion import cargar_config, RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
def corrida():
    tmp = pathlib.Path(tempfile.mkdtemp(dir="."))
    b = Bloque(cargar_config(extra={"modo": "backtest"}), ProveedorCSV(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"),
               cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "e", tmp / "s")
    b.ciclo("2026-06-05")
    return {p.name: p.read_bytes() for p in sorted((tmp / "e").glob("*.jsonl"))}, b.mensajeria.registro
a, ra = corrida(); bb, rb = corrida()
for k in sorted(set(a) | set(bb)):
    print(f"{k:40s}", "IGUAL" if a.get(k) == bb.get(k) else "DISTINTO")
ia = [(m["msg_id"], m["contrato"], m["receptor"]) for m in ra]; ib = [(m["msg_id"], m["contrato"], m["receptor"]) for m in rb]
print("secuencia de mensajes (msg_id→contrato/receptor) igual:", ia == ib)
if ia != ib:
    d = [(x, y) for x, y in zip(ia, ib) if x != y][:3]; print("  primeras diferencias:", d)
