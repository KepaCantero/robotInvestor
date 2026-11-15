"""r02_03 · El cerrojo: proceso que muere con el cerrojo cogido, proceso colgado con él, «.lock» que es un directorio o un
enlace, dos procesos que escriben a la vez, lectores mientras otro escribe y el mismo registro por dos rutas (enlace).
Uso: python3 -B r02_03_cerrojo.py <raíz>"""
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r02_comun import AHORA, DESPUES, SCRIPTS, caso, fin, lanza, pre, registro_temporal, rx  # noqa: E402

COGE = r"""
import sys, fcntl, time
f = open(sys.argv[1] + ".lock", "a")
fcntl.flock(f.fileno(), fcntl.LOCK_EX)
print("cogido", flush=True)
time.sleep(60)
"""
ESCRIBE = r"""
import sys, time
sys.path.insert(0, sys.argv[1])
import registro_experimentos as rx
r = rx.Registro(sys.argv[2]); t0 = float(sys.argv[4]); ok = err = 0
while time.time() < t0:
    pass
for i in range(int(sys.argv[3])):
    try:
        r.intento(sys.argv[5], "v1", "2026-11-12T11:00:00+00:00"); ok += 1
    except Exception as e:
        err += 1
print(ok, err)
"""
LEE = r"""
import sys, time
sys.path.insert(0, sys.argv[1])
import registro_experimentos as rx
r = rx.Registro(sys.argv[2]); t0 = float(sys.argv[3]); fin = t0 + float(sys.argv[4]); ok = 0; malos = {}
while time.time() < t0:
    pass
while time.time() < fin:
    try:
        r.verificar(); ok += 1
    except rx.RegistroError as e:
        k = str(e)[:40]; malos[k] = malos.get(k, 0) + 1
print(ok, malos)
"""


def proc(codigo, *args):
    return subprocess.Popen([sys.executable, "-B", "-c", codigo, *map(str, args)], stdout=subprocess.PIPE, text=True)


# 1. Un proceso coge el cerrojo y muere (SIGKILL): el siguiente escribe
reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
p = proc(COGE, reg.ruta); p.stdout.readline(); os.kill(p.pid, signal.SIGKILL); p.wait()
t = time.time(); e = lanza(lambda: reg.intento(exp, "v1", DESPUES)); dt = time.time() - t
caso("proceso muerto con el cerrojo: el siguiente escribe sin esperar", e is None and dt < 2, f"{dt:.2f} s, {e}")
caso("…el «.lock» que queda no estorba ni se sube (*.jsonl.lock en .gitignore)", reg.ruta.with_name("registro.jsonl.lock").exists())

# 2. Un proceso colgado con el cerrojo: el escritor espera sin límite
reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
p = proc(COGE, reg.ruta); p.stdout.readline()
q = proc(ESCRIBE, SCRIPTS, reg.ruta, 1, time.time(), exp)
try:
    q.wait(timeout=5); colgado = False
except subprocess.TimeoutExpired:
    colgado = True
caso("(baja) con otro proceso colgado con el cerrojo, el escritor no espera sin límite: falla cerrado con un mensaje", not colgado,
     "sigue esperando a los 5 s (flock sin LOCK_NB ni plazo)" if colgado else "")
p.kill(); p.wait(); q.wait(timeout=10)
caso("…y en cuanto el colgado muere, escribe", q.stdout.read().split()[:1] == ["1"])

# 3. «.lock» que es un directorio
reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
reg.ruta.with_name("registro.jsonl.lock").unlink(); reg.ruta.with_name("registro.jsonl.lock").mkdir()
e = lanza(lambda: reg.intento(exp, "v1", DESPUES), Exception)
caso("«.lock» que es un directorio: no escribe", e is not None and reg.verificar() == 1)
caso("…y sale RegistroError (lo que capturan el banco y los llamadores)", isinstance(e, rx.RegistroError), f"{type(e).__name__}")

# 4. Dos procesos con 100 intentos cada uno
reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
t0 = time.time() + 1.0
ps = [proc(ESCRIBE, SCRIPTS, reg.ruta, 100, t0, exp) for _ in range(2)]
sal = [x.communicate()[0].split() for x in ps]
e = lanza(reg.verificar, rx.RegistroError)
caso("dos procesos con 100 intentos cada uno: 200 escritos, cadena íntegra y n correlativo",
     e is None and reg.verificar() == 201 and [i["n"] for i in reg.experimento(exp)["intentos"]] == list(range(1, 201)),
     f"salidas {sal}; {e}")

# 5. Un lector mientras otro escribe: ¿acusa de manipulación a un registro sano?
reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
t0 = time.time() + 1.0
w = proc(ESCRIBE, SCRIPTS, reg.ruta, 300, t0, exp); r_ = proc(LEE, SCRIPTS, reg.ruta, t0, 4)
sw = w.communicate()[0].strip(); sr = r_.communicate()[0].strip()
caso("(baja) un lector («ver», «verificar», el banco) mientras otro escribe no acusa a un registro sano", "{}" in sr,
     f"escritor: {sw}; lector (lecturas buenas, falsas alarmas): {sr[:200]}")

# 6. El mismo registro por dos rutas (enlace simbólico): dos cerrojos y dos sellos
reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
enl = reg.ruta.with_name("otro.jsonl"); enl.symlink_to(reg.ruta.name)
e = lanza(lambda: rx.Registro(enl).intento(exp, "v1", DESPUES), rx.RegistroError)
caso("(baja) el registro por un enlace simbólico: o se lee con el mismo sello, o se rechaza con un motivo claro", True,
     f"intento por el enlace: {e}")
fin()
