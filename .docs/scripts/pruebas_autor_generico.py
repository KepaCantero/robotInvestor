"""Pruebas del autor genérico de los commits (operador, 24-11-2026: «Usa un autor genérico»).

`common.sh` (requiere_autor_generico, que llaman commit.sh y commit_limpio.sh antes del gate) y `cola_astra.py` aceptan solo
los pares de AUTORES_GENERICOS; un nombre o un correo personal, juntos o por separado, en el entorno o en .env, se rechaza.
Uso: python -m pytest -q .docs/scripts/pruebas_autor_generico.py (lo ejecuta pruebas_scripts.sh).
"""
import importlib.util
import os
import re
import subprocess
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent
RAIZ = SCRIPTS.parents[1]
GENERICOS = ["Astra <astra@users.noreply.github.com>", "Claude <noreply@anthropic.com>"]
PERSONAL = ("Persona Prueba", "persona@equipo-" + "local.invalid")   # ficticio, partido en dos cadenas


def _cola(tmp_path, monkeypatch, env, dotenv=None):
    spec = importlib.util.spec_from_file_location("cola_astra_prueba", SCRIPTS / "cola_astra.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if dotenv is not None:
        (tmp_path / ".env").write_text(dotenv, encoding="utf-8")
    monkeypatch.setattr(m, "RAIZ", tmp_path)
    monkeypatch.setattr(m, "git", lambda *a: {"config user.name": PERSONAL[0], "config user.email": PERSONAL[1]}[" ".join(a)])
    for k in ("GIT_AUTOR_NOMBRE", "GIT_AUTOR_EMAIL"):
        monkeypatch.delenv(k, raising=False)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    return m


def _bash(env):
    entorno = {k: v for k, v in os.environ.items() if not k.startswith("GIT_AUTOR_")}
    entorno.update(env)
    orden = f'source "{SCRIPTS}/common.sh"; requiere_autor_generico && echo AUTOR_OK'
    return subprocess.run(["bash", "-c", orden], capture_output=True, text=True, env=entorno, check=False, cwd=RAIZ)


def test_las_dos_listas_son_la_misma():
    """common.sh y cola_astra.py tienen la misma lista cerrada (si una cambia, la otra también)."""
    texto = (SCRIPTS / "common.sh").read_text(encoding="utf-8")
    sh = re.findall(r'"([^"]+ <[^>]+>)"', re.search(r"AUTORES_GENERICOS=\(([^)]*)\)", texto).group(1))
    py = (SCRIPTS / "cola_astra.py").read_text(encoding="utf-8")
    pyl = re.findall(r'"([^"]+ <[^>]+>)"', re.search(r"AUTORES_GENERICOS = \(([^)]*)\)", py).group(1))
    assert sh == pyl == GENERICOS


@pytest.mark.parametrize("autor", GENERICOS)
def test_un_autor_generico_vale(autor, tmp_path, monkeypatch):
    nombre, correo = autor[:-1].split(" <")
    env = {"GIT_AUTOR_NOMBRE": nombre, "GIT_AUTOR_EMAIL": correo}
    assert _cola(tmp_path, monkeypatch, env).autor_efectivo() in GENERICOS
    r = _bash(env)
    assert r.returncode == 0 and "AUTOR_OK" in r.stdout


@pytest.mark.parametrize("env", [
    {"GIT_AUTOR_NOMBRE": PERSONAL[0], "GIT_AUTOR_EMAIL": PERSONAL[1]},
    {"GIT_AUTOR_NOMBRE": "Astra", "GIT_AUTOR_EMAIL": PERSONAL[1]},
    {"GIT_AUTOR_NOMBRE": PERSONAL[0], "GIT_AUTOR_EMAIL": "astra@users.noreply.github.com"},
    {"GIT_AUTOR_NOMBRE": "astra", "GIT_AUTOR_EMAIL": "astra@users.noreply.github.com"},   # sin variantes: la lista es exacta
], ids=["los_dos_personales", "correo_personal", "nombre_personal", "mayusculas"])
def test_un_autor_personal_se_rechaza_y_no_se_repite_en_el_mensaje(env, tmp_path, monkeypatch):
    assert _cola(tmp_path, monkeypatch, env).autor_efectivo() not in GENERICOS
    r = _bash(env)
    assert r.returncode != 0 and "AUTOR_OK" not in r.stdout
    assert "no es genérico" in r.stderr and PERSONAL[0] not in r.stderr and PERSONAL[1] not in r.stderr


def test_sin_variables_cuenta_el_git_config(tmp_path, monkeypatch):
    """Sin GIT_AUTOR_* manda el git config (el de la prueba es personal) y se rechaza."""
    assert _cola(tmp_path, monkeypatch, {}).autor_efectivo() == f"{PERSONAL[0]} <{PERSONAL[1]}>"


def test_un_autor_personal_en_env_se_rechaza(tmp_path, monkeypatch):
    """El .env manda sobre un git config genérico: Astra puede tener el git config bien y el .env mal."""
    m = _cola(tmp_path, monkeypatch, {}, dotenv=f"GIT_AUTOR_NOMBRE={PERSONAL[0]}\nGIT_AUTOR_EMAIL='{PERSONAL[1]}'\n")
    monkeypatch.setattr(m, "git", lambda *a: {"config user.name": "Astra",
                                               "config user.email": "astra@users.noreply.github.com"}[" ".join(a)])
    assert m.autor_efectivo() == f"{PERSONAL[0]} <{PERSONAL[1]}>"


def test_el_entorno_manda_sobre_env(tmp_path, monkeypatch):
    m = _cola(tmp_path, monkeypatch, {"GIT_AUTOR_NOMBRE": "Astra", "GIT_AUTOR_EMAIL": "astra@users.noreply.github.com"},
              dotenv=f"GIT_AUTOR_NOMBRE={PERSONAL[0]}\nGIT_AUTOR_EMAIL={PERSONAL[1]}\n")
    assert m.autor_efectivo() == GENERICOS[0]


def test_los_scripts_de_commit_lo_comprueban_antes_del_gate():
    for nombre in ("commit.sh", "commit_limpio.sh"):
        lineas = (SCRIPTS / nombre).read_text(encoding="utf-8").splitlines()
        i_src = next(i for i, l in enumerate(lineas) if l.startswith("source ") and "common.sh" in l)
        i_aut = next(i for i, l in enumerate(lineas) if l.startswith("requiere_autor_generico"))
        i_gate = next(i for i, l in enumerate(lineas) if "check_all" in l or "pruebas_scripts" in l)
        assert i_src < i_aut < i_gate, nombre


def test_la_cola_da_error_con_un_autor_personal(tmp_path, monkeypatch, capsys):
    """Con una cola propia en tmp_path, no la real (T-194, QA r01 H-06)."""
    m = _cola(tmp_path, monkeypatch, {"GIT_AUTOR_NOMBRE": PERSONAL[0], "GIT_AUTOR_EMAIL": PERSONAL[1]})
    cola = tmp_path / ".docs/tickets/_relevo/cola_astra.md"
    cola.parent.mkdir(parents=True)
    cola.write_text("| # | Tarea | Tipo | Encargo o ticket | Entregable | Estado | Commit | Nota |\n"
                    "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
                    "| C-01 | Tarea | REVISION | encargo | «no/existe.md» | PENDIENTE | | |\n", encoding="utf-8")
    monkeypatch.setattr(m, "COLA", cola)
    falso = {"config user.name": PERSONAL[0], "config user.email": PERSONAL[1]}
    monkeypatch.setattr(m, "git", lambda *a: falso.get(" ".join(a), ""))
    monkeypatch.setattr(m.sys, "argv", ["cola_astra.py"])
    assert m.main() == 1
    salida = capsys.readouterr().out
    assert "autor de los commits no genérico" in salida and PERSONAL[0] not in salida
