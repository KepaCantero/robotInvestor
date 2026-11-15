"""r04_05 · El cerrojo con turno de la 0.4.0 (H-02, H-21, H-29): lectores y escritores mezclados, un proceso que muere con el
turno, un proceso colgado con el turno (espera máxima), y un lector sin permiso de escritura en la carpeta del registro.
Uso: .venv/bin/python -B r04_05_turno.py <raíz>   (el último caso necesita ser root para cambiar de usuario)"""
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r04_comun import AHORA, SCRIPTS, borrar, caso, cronometro, fin, lanza, pre, rx, tmpdir  # noqa: E402

tmps = []
PY = sys.executable


def hijo(codigo):
    return subprocess.Popen([PY, "-I", "-c", f"import sys; sys.path.insert(0, {str(SCRIPTS)!r})\n" + codigo],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


# 1. Tres escritores (30 intentos cada uno) y tres lectores en bucle, a la vez
d = tmpdir("r04_t99_"); tmps.append(d)
ruta = d / "registro.jsonl"
exp = rx.Registro(ruta).prerregistrar(pre(max_variantes=1000), "qa", ahora=AHORA)["exp_id"]
escritor = f"""
import registro_experimentos as rx
r = rx.Registro({str(ruta)!r}); malos = 0
for k in range(30):
    try:
        r.intento({exp!r}, "v%d" % k)
    except rx.RegistroError as e:
        malos += 1; print("ERR", e)
print("FIN", malos)
"""
lector = f"""
import time, registro_experimentos as rx
r = rx.Registro({str(ruta)!r}); buenas = malas = 0; t = time.monotonic()
while time.monotonic() - t < 8:
    try:
        r.verificar(); buenas += 1
    except rx.RegistroError as e:
        malas += 1; print("ERR", e)
print("FIN", buenas, malas)
"""
ps = [hijo(escritor) for _ in range(3)] + [hijo(lector) for _ in range(3)]
salidas = [p.communicate(timeout=300)[0].strip().splitlines()[-1] for p in ps]
n = lanza(rx.Registro(ruta).verificar)
ns = [x["n"] for x in rx.Registro(ruta).anotaciones() if x["tipo"] == "INTENTO"] if n is None else []
caso("3 escritores × 30 y 3 lectores a la vez: 90 intentos, cadena íntegra, n correlativo, ningún error",
     n is None and ns == list(range(1, 91)) and all(s.split()[0] == "FIN" and s.split()[-1] == "0" for s in salidas),
     f"salidas {salidas}; {n or len(ns)}")

# 2. Un proceso que coge el turno y muere (kill -9): el escritor entra enseguida
d = tmpdir("r04_t99_"); tmps.append(d)
ruta = d / "registro.jsonl"
exp = rx.Registro(ruta).prerregistrar(pre(), "qa", ahora=AHORA)["exp_id"]
turno = ruta.with_name(ruta.name + ".turno")
p = hijo(f"import fcntl, time\nf = open({str(turno)!r}, 'a'); fcntl.flock(f, fcntl.LOCK_EX); print('cogido', flush=True); time.sleep(600)")
p.stdout.readline()
os.kill(p.pid, signal.SIGKILL); p.wait()
t = cronometro()
e = lanza(lambda: rx.Registro(ruta).intento(exp, "v1"), rx.RegistroError)
caso("el que tenía el turno muere con kill -9: el escritor escribe sin esperar", e is None and t() < 2, f"{t():.2f} s; {e}")

# 3. Un proceso colgado con el turno: escritor y lector fallan cerrado hacia los 30 s, sin escribir nada
p = hijo(f"import fcntl, time\nf = open({str(turno)!r}, 'a'); fcntl.flock(f, fcntl.LOCK_EX); print('cogido', flush=True); time.sleep(600)")
p.stdout.readline()
antes = ruta.read_bytes()
t = cronometro()
e = lanza(lambda: rx.Registro(ruta).intento(exp, "v1"), rx.RegistroError)
te = t()
t = cronometro()
el = lanza(lambda: rx.Registro(ruta).verificar(), rx.RegistroError)
tl = t()
p.kill(); p.wait()
caso("turno cogido por un proceso colgado: el escritor falla cerrado a los ~30 s y no escribe",
     e is not None and 29 < te < 35 and ruta.read_bytes() == antes, f"{te:.1f} s; {e}")
caso("…y el lector también falla cerrado a los ~30 s (no se queda colgado)", el is not None and 29 < tl < 35, f"{tl:.1f} s; {el}")

# 4. Un escritor que espera a un lector colgado retiene el turno: otro escritor espera hasta 30 s al turno y otros 30 al cerrojo?
lock = ruta.with_name(ruta.name + ".lock")
p = hijo(f"import fcntl, time\nf = open({str(lock)!r}, 'a'); fcntl.flock(f, fcntl.LOCK_SH); print('cogido', flush=True); time.sleep(600)")
p.stdout.readline()
a = hijo(f"import time, registro_experimentos as rx\nt = time.monotonic()\ntry:\n    rx.Registro({str(ruta)!r}).intento({exp!r}, 'v1')\n"
         "    print('ESCRIBIÓ', round(time.monotonic() - t, 1))\nexcept rx.RegistroError as e:\n    print('FALLA', round(time.monotonic() - t, 1))")
time.sleep(1)
b = hijo(f"import time, registro_experimentos as rx\nt = time.monotonic()\ntry:\n    rx.Registro({str(ruta)!r}).intento({exp!r}, 'v1')\n"
         "    print('ESCRIBIÓ', round(time.monotonic() - t, 1))\nexcept rx.RegistroError as e:\n    print('FALLA', round(time.monotonic() - t, 1))")
time.sleep(5)
p.kill(); p.wait()   # el lector colgado muere a los ~6 s: A entra; B, que esperaba el turno, entra detrás
sa, sb = a.communicate(timeout=120)[0].strip(), b.communicate(timeout=120)[0].strip()
caso("lector colgado 6 s: el escritor A entra al morir y el B, que esperaba el turno detrás de A, también",
     sa.startswith("ESCRIBIÓ") and sb.startswith("ESCRIBIÓ"), f"A: {sa}; B: {sb}")

# 5. Un lector sin permiso de escritura en la carpeta (un registro de solo lectura): ¿puede leer?
d = tmpdir("r04_t99_ro_"); tmps.append(d)
ruta = d / "registro.jsonl"
rx.Registro(ruta).prerregistrar(pre(), "qa", ahora=AHORA)
for f in (".lock", ".turno"):
    Path(str(ruta) + f).unlink(missing_ok=True)
os.chmod(d, 0o755)
for f in d.iterdir():
    os.chmod(f, 0o644)
if os.geteuid() == 0:
    mod = tmpdir("r04_t99_mod_"); tmps.append(mod); os.chmod(mod, 0o755)   # copia legible por «nobody» del módulo revisado
    (mod / "registro_experimentos.py").write_bytes((SCRIPTS / "registro_experimentos.py").read_bytes())
    os.chmod(mod / "registro_experimentos.py", 0o644)
    codigo = (f"import os, sys; os.setgid(65534); os.setuid(65534); sys.path.insert(0, {str(mod)!r})\n"
              f"import registro_experimentos as rx\ntry:\n    print('LEE', rx.Registro({str(ruta)!r}, ancla_git=False).verificar())\n"
              "except Exception as e:\n    print('FALLA', type(e).__name__, e)")
    r = subprocess.run([PY, "-I", "-c", codigo], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    caso("(baja) un usuario que solo puede leer la carpeta del registro puede verificarlo", out.startswith("LEE"), out[:160])
else:
    print("[SIN COMPROBAR] lector sin permiso de escritura: hace falta ser root para cambiar de usuario")

for t_ in tmps:
    borrar(t_)
fin()
