"""Utilidades comunes de los scripts de ataque r03 (QA r03 de T-99, registro 0.3.0). No escriben nunca en el registro del
repositorio: todo va a carpetas temporales nuevas de /tmp (fuera de cualquier repositorio git, salvo los repositorios
temporales que crean a propósito). Al terminar, `fin()` comprueba que no existe «.docs/experimentos» ni en la raíz que se
revisa ni en el repositorio principal.

Uso: python3 -B r03_NN_….py <raíz del repositorio o del worktree>
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

RAIZ = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[4]
SCRIPTS = RAIZ / ".docs" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import registro_experimentos as rx  # noqa: E402

CARPETAS_PROHIBIDAS = (RAIZ / ".docs" / "experimentos", Path("/home/user/robotinvestor/.docs/experimentos"))
AHORA = "2026-11-12T10:00:00+00:00"
DESPUES = "2026-11-12T11:00:00+00:00"
_resultados = []
_ya_existian = {p for p in CARPETAS_PROHIBIDAS if p.exists()}


def pre(**cambios):
    d = {"hipotesis": "Quitar la segunda pasada no empeora la calidad", "objeto": "RECORTE",
         "metrica": "exceso frente a la cesta de la clase", "datos": "backtest simulado",
         "desde": "2026-03-06", "hasta": "2026-05-29", "semilla": 7,
         "criterio_exito": "rango del 90 % por encima de cero", "max_variantes": 2}
    d.update(cambios)
    return d


def tmpdir(prefijo="r03_t99_"):
    return Path(tempfile.mkdtemp(prefix=prefijo))


def caso(nombre, esperado_ok, detalle=""):
    """esperado_ok=True: se comporta como pide el plan (o como declara el implementador); False: hallazgo."""
    _resultados.append((nombre, esperado_ok))
    print(f"[{'OK' if esperado_ok else 'HALLAZGO'}] {nombre}" + (f" · {detalle}" if detalle else ""), flush=True)


def lanza(f, *exc):
    try:
        f()
    except exc or (Exception,) as e:
        return e
    return None


def lineas(ruta):
    return Path(ruta).read_text(encoding="utf-8").split("\n")[:-1]


def escribir_lineas(ruta, ls):
    Path(ruta).write_text("".join(x + "\n" for x in ls), encoding="utf-8")


def rehacer_sello(reg):
    """El atacante (declarado) que rehace el sello para que case con lo que deja en el registro."""
    ls = lineas(reg.ruta)
    ult = json.loads(ls[-1]) if ls else {"_seq": 0, "_hash": "0" * 64}
    reg.sello.write_text(json.dumps({"seq": ult["_seq"], "hash": ult["_hash"]}) + "\n", encoding="utf-8")


def recadenar(objs):
    prev, out = "0" * 64, []
    for i, e in enumerate(objs, 1):
        e = {k: v for k, v in e.items() if k != "_hash"}
        e["_seq"], e["_hash_prev"] = i, prev
        e["_hash"] = rx.huella(e)
        prev = e["_hash"]
        out.append(rx._linea(e))
    return out


ENTORNO_GIT = {**os.environ, "GIT_AUTHOR_NAME": "qa", "GIT_AUTHOR_EMAIL": "qa@ejemplo.invalid", "GIT_COMMITTER_NAME": "qa",
               "GIT_COMMITTER_EMAIL": "qa@ejemplo.invalid"}


def git(carpeta, *args, check=True):
    p = subprocess.run(["git", "-C", str(carpeta), *args], capture_output=True, text=True, env=ENTORNO_GIT)
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {p.stderr.strip()}")
    return p.stdout.strip()


def repo_temporal(prefijo="r03_t99_git_"):
    d = tmpdir(prefijo)
    git(d, "init", "-q", "-b", "develop")
    git(d, "config", "commit.gpgsign", "false")
    return d


def experimento_completo(reg, veredicto="peor", variante="v1", exp=None, ahora=AHORA, despues=DESPUES):
    """Prerregistro (si no se da exp), un intento y su resultado. Devuelve el exp_id."""
    if exp is None:
        exp = reg.prerregistrar(pre(), "qa", ahora=ahora)["exp_id"]
    n = reg.intento(exp, variante, ahora=despues)["n"]
    reg.resultado(exp, n, veredicto, ahora=despues)
    return exp


def subir(repo, *rutas, mensaje="registro"):
    git(repo, "add", *[str(r) for r in rutas])
    git(repo, "commit", "-q", "-m", mensaje)


def cronometro():
    t = time.monotonic()
    return lambda: time.monotonic() - t


def fin():
    for p in CARPETAS_PROHIBIDAS:
        assert p in _ya_existian or not p.exists(), f"un script de ataque escribió en {p}"
    ok = sum(1 for _, x in _resultados if x)
    print(f"\n{ok}/{len(_resultados)} como pide el plan; {len(_resultados) - ok} hallazgo(s)")


def borrar(*ps):
    for p in ps:
        shutil.rmtree(p, ignore_errors=True)
