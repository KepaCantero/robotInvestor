"""Utilidades comunes de los scripts de ataque r04 (QA r04 de T-99, registro 0.4.0). Reutiliza `r03_comun.py` (sin tocarlo) y
añade lo que cambia en la 0.4.0: los repositorios temporales llevan el `.gitignore` del proyecto (el sello, el cerrojo y el
turno son locales y no se suben) y `subir()` solo sube el registro. Nunca escriben en el registro del repositorio: todo va a
carpetas temporales nuevas, y `fin()` comprueba que no existe «.docs/experimentos» ni en la raíz revisada ni en el principal.

Uso: python3 -B r04_NN_….py <raíz del repositorio o del worktree>
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r03_comun import (AHORA, DESPUES, ENTORNO_GIT, RAIZ, SCRIPTS, borrar, caso, cronometro, escribir_lineas,  # noqa: E402,F401
                       experimento_completo, fin, git, lanza, lineas, pre, recadenar, rehacer_sello, rx, tmpdir)

REL = Path(".docs/experimentos/registro_claude.jsonl")
PY = sys.executable


def repo_proyecto(prefijo="r04_t99_git_"):
    """Repositorio temporal en develop con el .gitignore del proyecto ya subido."""
    d = tmpdir(prefijo)
    git(d, "init", "-q", "-b", "develop")
    git(d, "config", "commit.gpgsign", "false")
    (d / ".gitignore").write_bytes((RAIZ / ".gitignore").read_bytes())
    git(d, "add", ".gitignore")
    git(d, "commit", "-q", "-m", "inicio")
    return d


def subir(repo, rel=REL, mensaje="registro"):
    git(repo, "add", str(rel))
    git(repo, "commit", "-q", "-m", mensaje)


def remoto_y_clon(repo):
    """Un remoto desnudo con lo de `repo` y un segundo clon (otra máquina del mismo agente)."""
    remoto = tmpdir("r04_t99_remoto_")
    git(remoto, "init", "-q", "--bare", "-b", "develop")
    git(repo, "remote", "add", "origin", str(remoto))
    git(repo, "push", "-q", "origin", "develop")
    clon = tmpdir("r04_t99_clon_")
    clon.rmdir()
    git(clon.parent, "clone", "-q", "-b", "develop", str(remoto), str(clon))
    git(clon, "config", "commit.gpgsign", "false")
    return remoto, clon


def detecta(reg):
    """(True, motivo) si leer el registro falla cerrado; (False, «verificar = n») si lo acepta."""
    e = lanza(reg.verificar, rx.RegistroError)
    return e is not None, (str(e)[:120] if e else f"verificar = {reg.verificar()}")


def cli(*args, env=None, cwd=None):
    """La línea de órdenes del registro de la raíz revisada, con RI_AGENTE y demás según `env`."""
    import os
    entorno = {k: v for k, v in os.environ.items() if k != "RI_AGENTE"}
    entorno.update(env or {})
    p = subprocess.run([PY, "-B", str(SCRIPTS / "registro_experimentos.py"), *args], capture_output=True, text=True,
                       env=entorno, cwd=cwd)
    return p.returncode, (p.stdout + p.stderr).strip()


def sello(reg):
    return json.loads(reg.sello.read_text(encoding="utf-8"))
