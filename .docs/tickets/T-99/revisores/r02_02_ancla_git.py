"""r02_02 · El ancla en git: fichero sin subir, subido y truncado, recalculado, truncado Y subido, renombrado, otra rama,
HEAD sin el fichero, repositorio sin commits, git ausente, objeto de git dañado, y un clon nuevo (el otro agente) con el
sello sin subir o atrasado. Todo en repositorios temporales nuevos de /tmp.
Uso: python3 -B r02_02_ancla_git.py <raíz>"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r02_comun import (AHORA, DESPUES, SCRIPTS, caso, escribir, fin, git, lanza, lineas, pre, recadenar,  # noqa: E402
                       repo_temporal, rx, tmpdir)


def en_repo(commit=True, con_sello=True):
    d = repo_temporal()
    reg = rx.Registro(d / "exp" / "registro.jsonl")
    exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
    reg.intento(exp, "v1", DESPUES); reg.resultado(exp, 1, "peor", ahora=DESPUES)
    reg.intento(exp, "v2", DESPUES); reg.resultado(exp, 2, "fallido", ahora=DESPUES)
    if commit:
        git(d, "add", "exp/registro.jsonl", *(["exp/registro.jsonl.sello"] if con_sello else []))
        git(d, "commit", "-q", "-m", "registro")
    return d, reg, exp


def err(reg):
    return lanza(reg.verificar, rx.RegistroError)


# 1. Sin subir: no hay ancla (declarado)
d, reg, exp = en_repo(commit=False); escribir(reg, lineas(reg)[:-2])
caso("(regla declarada) sin subir a git, truncar y rehacer el sello no se detecta", err(reg) is None)

# 2. Subido: truncar y rehacer el sello se detecta
d, reg, exp = en_repo(); escribir(reg, lineas(reg)[:-2])
caso("subido: truncar las dos últimas y rehacer el sello se detecta", err(reg) is not None, str(err(reg))[:90])
d, reg, exp = en_repo(); objs = [json.loads(x) for x in lineas(reg)]; objs[2]["veredicto"] = "mejor"; escribir(reg, recadenar(objs))
caso("subido: cambiar un veredicto y recalcular cadena y sello se detecta", err(reg) is not None)
d, reg, exp = en_repo(); reg.intento(exp, "v1", DESPUES)
caso("subido y luego anotado (crece): se lee", err(reg) is None)

# 3. Truncar Y subir el truncado (commit) con el sello rehecho
d, reg, exp = en_repo(); escribir(reg, lineas(reg)[:-2]); git(d, "commit", "-q", "-am", "quito el intento fallido")
caso("truncar, rehacer el sello y hacer commit: se detecta (el ancla mira solo HEAD, no la historia)", err(reg) is not None,
     f"verificar: {reg.verificar() if err(reg) is None else err(reg)} anotaciones; "
     f"git log del registro: {git(d, 'log', '--oneline', '--', 'exp/registro.jsonl').count(chr(10)) + 1} commits")
d, reg, exp = en_repo(); objs = [json.loads(x) for x in lineas(reg)]; objs[2]["veredicto"] = "mejor"
escribir(reg, recadenar(objs)); git(d, "commit", "-q", "-am", "veredicto")
caso("cambiar un veredicto, recalcular y hacer commit: se detecta", err(reg) is not None,
     f"adoptable ahora = {reg.adoptable(exp) if err(reg) is None else '-'}")

# 4. HEAD sin el fichero (git rm --cached + commit), y truncado después
d, reg, exp = en_repo(); git(d, "rm", "-q", "--cached", "exp/registro.jsonl", "exp/registro.jsonl.sello")
git(d, "commit", "-q", "-m", "fuera"); escribir(reg, lineas(reg)[:-2])
caso("sacar el registro de HEAD con un commit y truncarlo: se detecta", err(reg) is not None)

# 5. Renombrado con git mv (subido) y truncado
d, reg, exp = en_repo(); git(d, "mv", "exp/registro.jsonl", "exp/nuevo.jsonl"); git(d, "mv", "exp/registro.jsonl.sello", "exp/nuevo.jsonl.sello")
git(d, "commit", "-q", "-m", "renombro"); r2 = rx.Registro(d / "exp" / "nuevo.jsonl"); escribir(r2, lineas(r2)[:-2])
caso("renombrado con commit y truncado: se detecta", err(r2) is not None)
d, reg, exp = en_repo(); shutil.copy(reg.ruta, d / "exp" / "copia.jsonl"); shutil.copy(reg.sello, d / "exp" / "copia.jsonl.sello")
r3 = rx.Registro(d / "exp" / "copia.jsonl"); escribir(r3, lineas(r3)[:-2])
caso("(regla declarada) una copia sin subir con otro nombre no tiene ancla", err(r3) is None)

# 6. Otra rama: lo anotado en una rama y truncado en otra
d, reg, exp = en_repo(); git(d, "checkout", "-q", "-b", "otra"); reg.intento(exp, "v1", DESPUES)
git(d, "commit", "-q", "-am", "anoto en otra"); git(d, "checkout", "-q", "main")
caso("volver a main tras anotar en otra rama: el registro de main se lee", err(reg) is None)
git(d, "checkout", "-q", "otra"); escribir(reg, lineas(reg)[:-1])
caso("en la otra rama, truncar lo subido en ella: se detecta", err(reg) is not None)

# 7. Repositorio sin commits y git ausente
d = repo_temporal(); reg = rx.Registro(d / "registro.jsonl"); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
caso("repositorio sin commits: se escribe y se lee (sin ancla)", err(reg) is None)
d, reg, exp = en_repo(); escribir(reg, lineas(reg)[:-2])
hijo = ("import sys; sys.path.insert(0, sys.argv[1]); import registro_experimentos as rx\n"
        "try:\n    print('LEE', rx.Registro(sys.argv[2]).verificar())\nexcept rx.RegistroError as e:\n    print('ERROR', e)")
p = subprocess.run([sys.executable, "-B", "-c", hijo, str(SCRIPTS), str(reg.ruta)], capture_output=True, text=True,
                   env={**os.environ, "PATH": str(tmpdir())})
caso("sin git en el PATH, un registro subido y truncado no se da por bueno (el ancla no se apaga en silencio)",
     p.stdout.startswith("ERROR"), p.stdout.strip() or p.stderr.strip()[-120:])
p = subprocess.run([sys.executable, "-B", "-c", hijo, str(SCRIPTS), str(reg.ruta)], capture_output=True, text=True,
                   env={**os.environ, "GIT_DIR": str(tmpdir())})
caso("con GIT_DIR apuntando a otra carpeta, el ancla no se apaga en silencio", p.stdout.startswith("ERROR"), p.stdout.strip())

# 8. Objeto de git dañado: el blob del registro en HEAD ya no se puede leer
d, reg, exp = en_repo(); blob = git(d, "rev-parse", "HEAD:exp/registro.jsonl")
(d / ".git" / "objects" / blob[:2] / blob[2:]).unlink(); escribir(reg, lineas(reg)[:-2])
caso("blob del registro en HEAD dañado y registro truncado: no se da por bueno (falla cerrado)", err(reg) is not None,
     f"verificar = {reg.verificar() if err(reg) is None else err(reg)}: «git show» falla y se toma como «no está en HEAD»")

# 9. Un clon nuevo (el otro agente): con el sello subido, sin él, o con el sello atrasado
d, reg, exp = en_repo()
c = tmpdir("r02_t99_clon_") / "c"; git(c.parent, "clone", "-q", str(d), str(c))
caso("clon nuevo con registro y sello subidos: se lee", err(rx.Registro(c / "exp" / "registro.jsonl")) is None)
d, reg, exp = en_repo(con_sello=False)
c = tmpdir("r02_t99_clon_") / "c"; git(c.parent, "clone", "-q", str(d), str(c))
e = err(rx.Registro(c / "exp" / "registro.jsonl"))
caso("subir el registro sin su sello: nada lo impide y el clon del otro agente queda bloqueado", e is None, f"en el clon: {e}")
d, reg, exp = en_repo(); reg.intento(exp, "v1", DESPUES); git(d, "add", "exp/registro.jsonl"); git(d, "commit", "-q", "-m", "solo el registro")
c = tmpdir("r02_t99_clon_") / "c"; git(c.parent, "clone", "-q", str(d), str(c))
e = err(rx.Registro(c / "exp" / "registro.jsonl"))
caso("subir el registro con el sello atrasado: el clon queda bloqueado («no casa con su sello»)", e is None, f"en el clon: {str(e)[:90]}")
fin()
