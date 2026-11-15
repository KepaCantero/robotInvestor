"""Utilidades comunes de los scripts de ataque r05 (QA r05 de T-99, registro 0.5.0). Reutiliza `r04_comun.py` y `r03_comun.py`
(sin tocarlos) y añade lo que cambia en la 0.5.0: el sello, el cerrojo y el turno viven en la carpeta de git del repositorio
(`git rev-parse --git-path ri-registro`) cuando el registro está en uno. Nunca escriben en el registro del repositorio: todo va a
carpetas temporales nuevas (los clones del proyecto, también), y `fin()` comprueba que no existe «.docs/experimentos» ni en la
raíz revisada ni en el repositorio principal.

Uso: python3 -B r05_NN_….py <raíz del repositorio o del worktree> [...]
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r04_comun import (AHORA, DESPUES, ENTORNO_GIT, PY, RAIZ, REL, SCRIPTS, borrar, caso, cli, cronometro,  # noqa: E402,F401
                       detecta, escribir_lineas, experimento_completo, fin, git, lanza, lineas, pre, recadenar,
                       rehacer_sello, remoto_y_clon, repo_proyecto, rx, subir, tmpdir)


def carpeta_local(repo):
    """Dónde pone la 0.5.0 el sello, el cerrojo y el turno de un registro que está en `repo`."""
    p = Path(git(repo, "rev-parse", "--git-path", "ri-registro"))
    return p if p.is_absolute() else Path(repo) / p


def clon_del_proyecto(origen, prefijo="r05_t99_proyecto_"):
    """Un clon nuevo del repositorio del proyecto (con su historia real, superficial o no) en una carpeta temporal."""
    d = tmpdir(prefijo)
    d.rmdir()
    subprocess.run(["git", "clone", "-q", "--no-local", str(origen), str(d)], check=True, capture_output=True, env=ENTORNO_GIT)
    git(d, "config", "commit.gpgsign", "false")
    git(d, "checkout", "-q", "-B", "develop")
    return d


def adoptable(reg, exp):
    r = reg.resumen(exp)
    return r["adoptable"], r


def cuantas(reg):
    return len(lineas(reg.ruta)) if reg.ruta.exists() else 0


def sello_json(reg):
    return json.loads(reg.sello.read_text(encoding="utf-8"))
