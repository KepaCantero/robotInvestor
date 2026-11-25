"""Pruebas de `.docs/scripts/preparar_entorno.sh` (T-96 y T-137) con un `.venv` falso: no crean entornos ni usan la red.

El script calcula la raíz desde su propia carpeta, así que cada prueba lo copia (con `common.sh`) a una raíz temporal con su
`tools/requisitos_entorno.txt` y un `.venv/bin/python` falso que responde a lo que el script le pregunta.
Uso: .venv/bin/python -m pytest -q .docs/scripts/pruebas_preparar_entorno.py"""
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

AQUI = Path(__file__).resolve().parent
PYTHON_FALSO = """#!/usr/bin/env bash
echo "$*" >> "$(dirname "$0")/llamadas.log"
if [[ "$1" == "-c" ]]; then echo "${VERSION_FALSA:-3.12}"; exit 0; fi
if [[ "$1 $2 $3" == "-m pip --version" ]]; then [[ -n "${SIN_PIP:-}" ]] && exit 1; echo "pip 24.0"; exit 0; fi
if [[ "$1 $2 $3" == "-m pip freeze" ]]; then cat "$(dirname "$0")/freeze.txt"; exit 0; fi
if [[ "$1 $2 $3" == "-m pip install" ]]; then exit 0; fi
if [[ "$1" == "-I" ]]; then shift; exec python3 -I "$@"; fi
exec python3 "$@"
"""


@pytest.fixture
def raiz(tmp_path):
    (tmp_path / ".docs" / "scripts").mkdir(parents=True)
    for f in ("preparar_entorno.sh", "common.sh"):
        shutil.copy(AQUI / f, tmp_path / ".docs" / "scripts" / f)
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "requisitos_entorno.txt").write_text("# versiones\narch==8.0.0\nnumpy==2.1.0\n", encoding="utf-8")
    bin_ = tmp_path / ".venv" / "bin"
    bin_.mkdir(parents=True)
    (bin_ / "python").write_text(PYTHON_FALSO, encoding="utf-8")
    (bin_ / "python").chmod(0o755)
    (bin_ / "freeze.txt").write_text("arch==8.0.0\nnumpy==2.1.0\n", encoding="utf-8")
    return tmp_path


def correr(raiz, *args, **entorno):
    env = {k: v for k, v in os.environ.items() if k not in ("VERSION_FALSA", "SIN_PIP", "PYTHON_ENTORNO")}
    env.update(entorno)
    r = subprocess.run(["bash", str(raiz / ".docs" / "scripts" / "preparar_entorno.sh"), *args], capture_output=True,
                       text=True, env=env, check=False)
    return r.returncode, r.stdout + r.stderr


def test_conforme(raiz):
    codigo, salida = correr(raiz, "--comprobar")
    assert codigo == 0 and "entorno conforme: 2 paquetes" in salida


def test_h01_un_venv_sin_pip_se_detecta_y_dice_como_salir(raiz):
    codigo, salida = correr(raiz, "--comprobar", SIN_PIP="1")
    assert codigo != 0 and "a medias" in salida and "rm -rf .venv" in salida


def test_h02_otro_python_se_rechaza_antes_de_instalar(raiz):
    codigo, salida = correr(raiz, VERSION_FALSA="3.13")
    llamadas = (raiz / ".venv" / "bin" / "llamadas.log").read_text(encoding="utf-8")
    assert codigo != 0 and "usa Python 3.13" in salida and "pip install" not in llamadas


def test_h03_un_paquete_sin_fijar_es_un_error(raiz):
    (raiz / ".venv" / "bin" / "freeze.txt").write_text("arch==8.0.0\nnumpy==2.1.0\nsix==1.16.0\n", encoding="utf-8")
    codigo, salida = correr(raiz, "--comprobar")
    assert codigo != 0 and "six==1.16.0 está instalado y no está fijado" in salida


@pytest.mark.parametrize("linea,ok,motivo", [("arch==8.0.0  # nota", True, ""), ("arch===8.0.0", False, "versión exacta"),
                                            ("arch==8.0.0\narch==9.0.0", False, "repetido"), ("arch>=8", False, "versión exacta")])
def test_h05_el_fichero_se_lee_como_pip(raiz, linea, ok, motivo):
    (raiz / "tools" / "requisitos_entorno.txt").write_text(f"{linea}\nnumpy==2.1.0\n", encoding="utf-8")
    codigo, salida = correr(raiz, "--comprobar")
    assert (codigo == 0) == ok and motivo in salida


def test_h06_argumentos_de_mas_y_python_por_nombre(raiz, tmp_path_factory):
    codigo, salida = correr(raiz, "--comprobar", "--otra")
    assert codigo != 0 and "uso:" in salida
    shutil.rmtree(raiz / ".venv")
    carpeta = tmp_path_factory.mktemp("bin")
    (carpeta / "python3.11falso").write_text("#!/usr/bin/env bash\necho 3.11\n", encoding="utf-8")
    (carpeta / "python3.11falso").chmod(0o755)
    codigo, salida = correr(raiz, PYTHON_ENTORNO="python3.11falso", PATH=f"{carpeta}:{os.environ['PATH']}")
    assert codigo != 0 and "es Python 3.11" in salida and not (raiz / ".venv").exists()


def norma(nombre):
    """El nombre de un paquete como lo compara pip (PEP 503)."""
    return re.sub(r"[-_.]+", "-", nombre).lower()


def test_t202_el_script_instala_cada_stub_de_tipos_fijado(raiz):
    """T-202: cada stub de tipos fijado en el fichero real (types-*, *-stubs) está en la orden de instalación del script.
    Si se fijara uno sin instalarlo, --comprobar fallaría en un entorno nuevo («falta …») y mypy mediría otra cosa."""
    real = (AQUI.parent.parent / "tools" / "requisitos_entorno.txt").read_text(encoding="utf-8")
    pins = [x for x in real.splitlines() if x.strip() and not x.startswith("#")]
    nombres = {norma(x.split("==")[0].strip()) for x in pins}
    stubs = {n for n in nombres if n.startswith("types-") or n.endswith("-stubs")}
    assert {"types-pyyaml", "types-jsonschema", "scipy-stubs"} <= stubs
    (raiz / "tools" / "requisitos_entorno.txt").write_text(real, encoding="utf-8")
    (raiz / ".venv" / "bin" / "freeze.txt").write_text("\n".join(pins) + "\n", encoding="utf-8")
    codigo, salida = correr(raiz)
    assert codigo == 0 and f"entorno conforme: {len(pins)} paquetes" in salida
    llamadas = (raiz / ".venv" / "bin" / "llamadas.log").read_text(encoding="utf-8").splitlines()
    orden = next(x for x in llamadas if x.startswith("-m pip install"))
    assert "-c tools/requisitos_entorno.txt" in orden
    assert stubs <= {norma(x) for x in orden.split()}
