"""estrangular.py FRACCION -- orden...: ejecuta la orden y la deja correr solo FRACCION del tiempo (SIGSTOP/SIGCONT en
ciclos de 100 ms), como una máquina con mucha más carga que núcleos. El tiempo de CPU del proceso no cambia; el de reloj sí."""
import os, signal, subprocess, sys, time
frac = float(sys.argv[1]); orden = sys.argv[sys.argv.index("--") + 1:]
p = subprocess.Popen(orden, start_new_session=True)
ciclo = 0.1
try:
    while p.poll() is None:
        time.sleep(ciclo * frac)
        try: os.killpg(p.pid, signal.SIGSTOP)
        except ProcessLookupError: break
        time.sleep(ciclo * (1 - frac))
        try: os.killpg(p.pid, signal.SIGCONT)
        except ProcessLookupError: break
finally:
    try: os.killpg(p.pid, signal.SIGCONT)
    except ProcessLookupError: pass
sys.exit(p.wait())
