"""r01_02 · Escrituras concurrentes desde dos procesos sobre el mismo registro, y la fusión de dos ramas de git que anotan
a la vez (Claude y Astra trabajan en máquinas distintas sobre el mismo registro del repositorio).
Uso: python3 r01_02_concurrencia.py <raíz>"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, DESPUES, RAIZ, caso, fin, lanza, pre, registro_temporal, rx  # noqa: E402

HIJO = r"""
import sys, time
sys.path.insert(0, sys.argv[1])
import registro_experimentos as rx
r = rx.Registro(sys.argv[2])
t0 = float(sys.argv[4])
while time.time() < t0:
    pass
ok = err = 0
for i in range(int(sys.argv[3])):
    try:
        r.intento("EXP-2026-0001", "v1", "2026-11-12T11:00:00+00:00"); ok += 1
    except Exception as e:
        err += 1
print(ok, err)
"""

import time  # noqa: E402

for ronda in range(3):
    reg = registro_temporal()
    reg.prerregistrar(pre(), "qa", AHORA)
    t0 = time.time() + 1.0
    ps = [subprocess.Popen([sys.executable, "-c", HIJO, str(RAIZ / ".docs" / "scripts"), str(reg.ruta), "60", str(t0)],
                           stdout=subprocess.PIPE, text=True) for _ in range(2)]
    salidas = [p.communicate()[0].split() for p in ps]
    err = lanza(reg.verificar, rx.RegistroError)
    escritas = sum(int(s[0]) for s in salidas)
    caso(f"ronda {ronda + 1}: dos procesos anotando a la vez dejan la cadena íntegra", err is None,
         f"intentos dados por buenos {escritas}, rechazados {sum(int(s[1]) for s in salidas)}; verificar: {err}")

# Dos prerregistros simultáneos: ¿el mismo EXP-…?
HIJO2 = r"""
import sys, time, json
sys.path.insert(0, sys.argv[1])
import registro_experimentos as rx
r = rx.Registro(sys.argv[2])
d = json.loads(sys.argv[3]); t0 = float(sys.argv[4])
while time.time() < t0:
    pass
try:
    print(r.prerregistrar(d, "qa", "2026-11-12T10:00:00+00:00")["exp_id"])
except Exception as e:
    print("ERR", e)
"""
dup = 0
for ronda in range(10):
    reg = registro_temporal()
    t0 = time.time() + 0.5
    ps = [subprocess.Popen([sys.executable, "-c", HIJO2, str(RAIZ / ".docs" / "scripts"), str(reg.ruta), json.dumps(pre()), str(t0)],
                           stdout=subprocess.PIPE, text=True) for _ in range(2)]
    out = [p.communicate()[0].strip() for p in ps]
    if out[0] == out[1] and not out[0].startswith("ERR"):
        dup += 1
caso("dos prerregistros simultáneos nunca reciben los dos el mismo EXP-… dado por bueno", dup == 0,
     f"{dup}/10 rondas con el mismo identificador devuelto a los dos")

# Fusión de dos ramas que anotan cada una un intento (git): lo que pasa al hacer rebase con el registro en el repositorio
with tempfile.TemporaryDirectory(prefix="r01_t99_git_") as d:
    d = Path(d)
    g = lambda *a: subprocess.run(["git", "-C", str(d), *a], capture_output=True, text=True)  # noqa: E731
    g("init", "-q", "-b", "develop"); g("config", "user.email", "qa@example.invalid"); g("config", "user.name", "qa")
    reg = rx.Registro(d / "registro.jsonl")
    exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
    g("add", "."); g("commit", "-qm", "base")
    g("checkout", "-qb", "astra"); reg.intento(exp, "v-astra", DESPUES); g("commit", "-qam", "astra")
    g("checkout", "-q", "develop"); reg.intento(exp, "v-claude", DESPUES); g("commit", "-qam", "claude")
    m = g("merge", "-q", "astra", "-m", "fusion")
    conflicto = m.returncode != 0
    if conflicto:   # resolución «natural»: quedarse con las dos líneas
        txt = (d / "registro.jsonl").read_text(encoding="utf-8")
        limpio = [x for x in txt.splitlines() if not x.startswith(("<<<<<<<", "=======", ">>>>>>>"))]
        (d / "registro.jsonl").write_text("\n".join(limpio) + "\n", encoding="utf-8")
    err = lanza(reg.verificar, rx.RegistroError)
    caso("dos ramas que anotan a la vez y se fusionan conservando las dos líneas dejan un registro usable", err is None,
         f"conflicto de git: {conflicto}; verificar tras la fusión: {err}")
fin()
