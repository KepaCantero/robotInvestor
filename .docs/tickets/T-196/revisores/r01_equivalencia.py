"""QA r01 de T-196: un CT-01 servido por la cola (instante con hora y zona) frente al mismo CT-01 por `Bloque.peticion` (fecha).
El RUN- y sus entregables deben coincidir salvo identificadores, sellos de tiempo y el `disparador`.
Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-196/revisores/r01_equivalencia.py"""
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "tests"))
import pandas as pd  # noqa: E402
from conftest import AS_OF, nuevo_bloque  # noqa: E402

from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402

UNI = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
CT01 = {"tipo": "AD_HOC", "alcance": {"clases": ["DIV", "RF"]}, "horizontes": ["H2"], "prioridad": "NORMAL"}
T = pd.Timestamp(f"{AS_OF}T23:30", tz="Europe/Madrid")   # tarde: si la hora se colara en los datos, se vería


def limpio(x):
    s = json.dumps(x, sort_keys=True, ensure_ascii=False, default=str)
    s = re.sub(r"(RUN|MSG|PET|QRY|INC|OPP|PRG|TND|CLM|CALC|ENT|EH5|HIT|CAR|SEG)-[A-Z0-9-]*\d", "ID", s)
    s = re.sub(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?([+-]\d{2}:\d{2}|Z)?", "TS", s)
    return json.loads(s)


b1 = nuevo_bloque(tempfile.mkdtemp(), UNI)
r1 = b1.peticion(dict(CT01), AS_OF)
b2 = nuevo_bloque(tempfile.mkdtemp(), UNI)
b2.cola.recibir(dict(CT01), T)
[s] = b2.cola.atender(T + pd.Timedelta(minutes=10))
run1 = {k: v for k, v in b1.almacen.estado("F5")[r1["run_id"]].items() if not k.startswith("_") and k != "disparador"}
run2 = {k: v for k, v in b2.almacen.estado("F5")[s["run_id"]].items() if not k.startswith("_") and k != "disparador"}
dif = sorted(k for k in set(run1) | set(run2) if limpio(run1.get(k)) != limpio(run2.get(k)))
print("RUN- campos distintos:", dif)
for k in dif:
    print(" ", k, "| peticion:", str(run1.get(k))[:160], "| cola:", str(run2.get(k))[:160])
for a in ("F3", "F4"):
    e1 = [limpio({k: v for k, v in e.items() if not k.startswith("_")}) for e in b1.almacen.leer(a)]
    e2 = [limpio({k: v for k, v in e.items() if not k.startswith("_")}) for e in b2.almacen.leer(a)]
    print(a, "iguales" if e1 == e2 else f"DISTINTOS ({len(e1)} frente a {len(e2)})")
print("VEREDICTO:", "OK" if not dif else "REVISAR")
