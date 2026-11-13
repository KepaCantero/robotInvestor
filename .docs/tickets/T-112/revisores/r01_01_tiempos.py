"""QA r01 de T-112 · tiempos por ficha: cada caso de control de las 35 fichas servido por Motor.servir (doble pasada
incluida), y los casos lentos que declara el análisis (REG-HMM-001 con BIC, FIR-CURVE-001). Imprime la tabla ordenada."""
import copy
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
from bloque_a.motor import servicio  # noqa: E402

m = C.motor()
filas = []
for f in sorted(servicio.FASE2):
    peor, estados = 0.0, set()
    for caso in servicio.CASOS_CONTROL[f]:
        t0 = time.time()
        r = m.servir({"operacion": f, "datos": copy.deepcopy(caso.get("datos") or []), "parametros": dict(caso.get("parametros") or {}),
                      "fecha_corte": None, "semilla": caso.get("semilla")}, "AG-18")
        dt = time.time() - t0
        peor = max(peor, dt)
        estados.add(r["estado"])
    filas.append((peor, f, len(servicio.CASOS_CONTROL[f]), sorted(estados)))
for peor, f, n, est in sorted(filas, reverse=True):
    print(f"{f:18s} casos {n}  peor {peor:7.2f} s  {est}")
fallos = [f for _, f, _, est in filas if any(e not in ("SERVED", "SERVED_WITH_LIMITATIONS") for e in est)]
print("casos de control no servidos por CT-09:", fallos)
