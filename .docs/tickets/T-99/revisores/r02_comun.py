"""Utilidades comunes de los scripts de ataque r02 (QA r02 de T-99). No escriben nunca en el registro del repositorio:
todo va a carpetas temporales nuevas de /tmp (fuera de cualquier repositorio git, salvo los que crea r02_02 a propósito).

Uso: python3 -B r02_NN_….py <raíz del repositorio o del worktree>
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[4]
SCRIPTS = RAIZ / ".docs" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import registro_experimentos as rx  # noqa: E402

REGISTRO_REPO = RAIZ / ".docs" / "experimentos" / "registro.jsonl"
REGISTRO_PRINCIPAL = Path("/home/user/robotinvestor/.docs/experimentos/registro.jsonl")
AHORA = "2026-11-12T10:00:00+00:00"
DESPUES = "2026-11-12T11:00:00+00:00"
ANTES = "2026-11-12T09:00:00+00:00"
_resultados = []


def pre(**cambios):
    d = {"hipotesis": "Quitar la segunda pasada no empeora la calidad", "objeto": "RECORTE",
         "metrica": "exceso frente a la cesta de la clase", "datos": "backtest simulado",
         "desde": "2026-03-06", "hasta": "2026-05-29", "semilla": 7,
         "criterio_exito": "rango del 90 % por encima de cero", "max_variantes": 2}
    d.update(cambios)
    return d


def tmpdir(prefijo="r02_t99_"):
    return Path(tempfile.mkdtemp(prefix=prefijo))


def registro_temporal(ancla_git=True):
    return rx.Registro(tmpdir() / "registro.jsonl", ancla_git=ancla_git)


def caso(nombre, esperado_ok, detalle=""):
    """esperado_ok=True: se comporta como pide el plan (o como declara el implementador); False: hallazgo."""
    _resultados.append((nombre, esperado_ok))
    print(f"[{'OK' if esperado_ok else 'HALLAZGO'}] {nombre}" + (f" · {detalle}" if detalle else ""))


def lanza(f, *exc):
    try:
        f()
    except exc or (Exception,) as e:
        return e
    return None


def leer(p):
    return Path(p).read_bytes()


def lineas(reg):
    return reg.ruta.read_text(encoding="utf-8").split("\n")[:-1]


def escribir(reg, ls, sello=True):
    """Reescribe el registro con esas líneas y, si sello=True, rehace también el sello (el atacante que lo sabe)."""
    reg.ruta.write_text("".join(x + "\n" for x in ls), encoding="utf-8")
    if sello:
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


def git(carpeta, *args, check=True):
    env = {**os.environ, "GIT_AUTHOR_NAME": "qa", "GIT_AUTHOR_EMAIL": "qa@ejemplo.invalid", "GIT_COMMITTER_NAME": "qa",
           "GIT_COMMITTER_EMAIL": "qa@ejemplo.invalid"}
    p = subprocess.run(["git", "-C", str(carpeta), *args], capture_output=True, text=True, env=env)
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {p.stderr.strip()}")
    return p.stdout.strip()


def repo_temporal():
    d = tmpdir("r02_t99_git_")
    git(d, "init", "-q", "-b", "main")
    return d


def fin():
    for p in (REGISTRO_REPO, REGISTRO_PRINCIPAL):
        assert not p.exists(), f"un script de ataque escribió en {p}"
    ok = sum(1 for _, x in _resultados if x)
    print(f"\n{ok}/{len(_resultados)} como pide el plan; {len(_resultados) - ok} hallazgo(s)")
