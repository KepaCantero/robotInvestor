"""r03_03 · El cerrojo con lectores y espera máxima del registro 0.3.0 (H-21): un lector colgado bloquea al escritor, lectores
continuos lo matan de hambre, un lector que muere, y dos nombres (enlace simbólico) para el mismo registro.
Uso: .venv/bin/python -B r03_03_cerrojo_lectores.py <raíz>   (tarda alrededor de un minuto y medio)"""
import fcntl
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r03_comun import (AHORA, DESPUES, RAIZ, borrar, caso, cronometro, experimento_completo, fin, git, lanza, pre,  # noqa: E402
                       repo_temporal, rx, subir, tmpdir)

tmps = []
PY = sys.executable
SCR = str(RAIZ / ".docs" / "scripts")


def lector_colgado(ruta, segundos):
    """Un proceso que lee el registro con el cerrojo compartido y se queda colgado con él (como un «ver» en un terminal
    suspendido con Ctrl-Z)."""
    cod = (f"import fcntl,time; f=open({str(ruta) + '.lock'!r},'a'); fcntl.flock(f.fileno(), fcntl.LOCK_SH); "
           f"print('cogido', flush=True); time.sleep({segundos})")
    p = subprocess.Popen([PY, "-I", "-c", cod], stdout=subprocess.PIPE, text=True)
    assert p.stdout.readline().strip() == "cogido"
    return p


# 1. Un lector colgado: el escritor espera y falla cerrado a los CERROJO_ESPERA_S, sin escribir
d = tmpdir(); tmps.append(d)
reg = rx.Registro(d / "registro.jsonl")
exp = experimento_completo(reg)
p = lector_colgado(reg.ruta, 120)
antes = reg.ruta.read_bytes()
t = cronometro()
e = lanza(lambda: reg.intento(exp, "v1", ahora=DESPUES))
s = t()
caso(f"un lector colgado con el cerrojo: el escritor falla cerrado hacia los {rx.CERROJO_ESPERA_S} s sin escribir",
     isinstance(e, rx.RegistroError) and reg.ruta.read_bytes() == antes and rx.CERROJO_ESPERA_S <= s < rx.CERROJO_ESPERA_S + 5,
     f"{s:.1f} s; {e}")
p.kill(); p.wait()
t = cronometro()
e = lanza(lambda: reg.intento(exp, "v1", ahora=DESPUES))
caso("…y en cuanto el lector muere (kill -9), el escritor escribe sin esperar", e is None and t() < 1, f"{t():.2f} s; {e}")

# 2. Lectores continuos (cuatro «ver» en bucle) sobre un registro con ancla en git: ¿el escritor entra?
repo = repo_temporal(); tmps.append(repo)
ruta = repo / ".docs" / "experimentos" / "registro_claude.jsonl"
r0 = rx.Registro(ruta, ancla_git=False)
exp = r0.prerregistrar(pre(max_variantes=1000), "qa", ahora=AHORA)["exp_id"]
subir(repo, ruta, Path(str(ruta) + ".sello"))
for k in range(1, 61):
    r0.intento(exp, f"v{k}", ahora=DESPUES); r0.resultado(exp, k, "peor", ahora=DESPUES)
    subir(repo, ruta, Path(str(ruta) + ".sello"), mensaje=f"intento {k}")
bucle = (f"import sys,time; sys.path.insert(0,{SCR!r}); import registro_experimentos as rx; r=rx.Registro({str(ruta)!r}); "
         "t=time.monotonic()\nwhile time.monotonic()-t<45: r.verificar()")
lectores = [subprocess.Popen([PY, "-I", "-c", bucle]) for _ in range(4)]
time.sleep(1)
reg = rx.Registro(ruta)
t = cronometro()
e = lanza(lambda: reg.intento(exp, "v61", ahora=DESPUES))
s = t()
for q in lectores:
    q.kill(); q.wait()
caso("cuatro lectores en bucle no dejan sin escribir al escritor (no hay hambre de escritores)", e is None,
     f"{s:.1f} s; {e if e else 'escribió'}")

# 3. Dos nombres para el mismo registro (enlace simbólico): cerrojos y sellos distintos
d = tmpdir(); tmps.append(d)
real = d / "registro.jsonl"
reg = rx.Registro(real)
exp = reg.prerregistrar(pre(max_variantes=1000), "qa", ahora=AHORA)["exp_id"]
alias = d / "alias.jsonl"
alias.symlink_to(real)
escritor = (f"import sys; sys.path.insert(0,{SCR!r}); import registro_experimentos as rx; r=rx.Registro(sys.argv[1])\n"
            f"for i in range(40):\n    r.intento({exp!r}, 'v'+sys.argv[2]+str(i), ahora={DESPUES!r})")
ps = [subprocess.Popen([PY, "-I", "-c", escritor, str(x), y], stderr=subprocess.PIPE, text=True)
      for x, y in ((real, "a"), (alias, "b"))]
errs = [q.communicate()[1].strip().splitlines()[-1:] for q in ps]
e1, e2 = lanza(rx.Registro(real).verificar), lanza(rx.Registro(alias).verificar)
caso("dos procesos que escriben el mismo registro por dos nombres (enlace simbólico): el registro real no se rompe y el "
     "alias falla cerrado (sin sello propio)", e1 is None and (e2 is None or isinstance(e2, rx.RegistroError)), f"real: {e1 or 'íntegro'}; alias: {e2 or 'íntegro'}; errores: {errs}"[:300])

for t_ in tmps:
    borrar(t_)
fin()
