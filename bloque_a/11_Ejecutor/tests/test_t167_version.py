"""T-167: la versión del paquete del ejecutor coincide con la de su README (INC-001)."""

import re
import tomllib
from pathlib import Path

import bloque_a

RAIZ = Path(__file__).resolve().parents[1]


def _version_readme() -> str:
    cabecera = (RAIZ / "README.md").read_text(encoding="utf-8").splitlines()[0]
    m = re.search(r"\(V(\d+)\.(\d+)\)", cabecera)
    assert m, f"el README no declara la versión del ejecutor en su título: {cabecera!r}"
    return f"{m.group(1)}.{m.group(2)}.0"


def test_pyproject_dice_la_version_del_readme():
    datos = tomllib.loads((RAIZ / "pyproject.toml").read_text(encoding="utf-8"))
    assert datos["project"]["version"] == _version_readme()


def test_el_modulo_dice_la_misma_version_que_el_pyproject():
    datos = tomllib.loads((RAIZ / "pyproject.toml").read_text(encoding="utf-8"))
    assert bloque_a.__version__ == datos["project"]["version"]
