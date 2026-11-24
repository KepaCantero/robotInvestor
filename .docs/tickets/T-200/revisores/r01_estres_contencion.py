"""QA r01 de T-200: ¿puede BEGIN IMMEDIATE dar «database is locked» en el uso normal con la máquina cargada?
Ocho procesos usan a la vez EL MISMO almacén ya creado (la tabla de acuses existe y está migrada): cada uno alterna
procesar_una_vez (mensajes distintos) y estado_reserva, mientras otros procesos queman CPU. Se cuentan los fallos.
Uso: python r01_estres_contencion.py <bloque_a/11_Ejecutor> [iteraciones] [quemadores]"""
import subprocess
import sys
import tempfile
import time
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
ITER = int(sys.argv[2]) if len(sys.argv) > 2 else 150
QUEMA = int(sys.argv[3]) if len(sys.argv) > 3 else 6
PROC = 8
TRAB = r"""
import sys, time
sys.path.insert(0, sys.argv[1])
from bloque_a.almacen import Almacen
from bloque_a.contratos import Mensajeria
ms = Mensajeria(Almacen(sys.argv[2]))
fallos, peor = 0, 0.0
for i in range(int(sys.argv[3])):
    t = time.perf_counter()
    try:
        m = ms.crear("CT-03", "BROKER", "AG-01", {"pregunta": f"saldo {sys.argv[4]} {i}"})
        ms.procesar_una_vez(m, lambda _: {"ok": 1})
        ms.estado_reserva(m["msg_id"])
    except Exception as e:
        fallos += 1
        print("fallo", type(e).__name__, e, file=sys.stderr)
    peor = max(peor, time.perf_counter() - t)
print(fallos, round(peor, 3))
"""
with tempfile.TemporaryDirectory() as d:
    sys.path.insert(0, str(EJ))
    from bloque_a.almacen import Almacen
    from bloque_a.contratos import Mensajeria
    Mensajeria(Almacen(d)).estado_reserva("MSG-X")   # tabla creada y migrada
    quem = [subprocess.Popen([sys.executable, "-c", "while True: pass"]) for _ in range(QUEMA)]
    t0 = time.time()
    try:
        ps = [subprocess.Popen([sys.executable, "-c", TRAB, str(EJ), d, str(ITER), str(i)], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True) for i in range(PROC)]
        res = [p.communicate() for p in ps]
    finally:
        for q in quem:
            q.kill()
    fallos = sum(int(o.split()[0]) for o, _ in res)
    peor = max(float(o.split()[1]) for o, _ in res)
    errores = {l for _, e in res for l in e.splitlines() if l.startswith("fallo")}
    print(f"procesos={PROC} iteraciones={ITER} quemadores={QUEMA} segundos={time.time() - t0:.1f} "
          f"fallos={fallos} peor_iteracion={peor}s errores={sorted(errores)[:3]}")
    sys.exit(1 if fallos else 0)
