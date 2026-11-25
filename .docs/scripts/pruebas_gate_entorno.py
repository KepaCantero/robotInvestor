"""Pruebas de la comprobación del entorno en los gates de mypy de `tools/check_all.sh` (T-202, QA r01, H-03).

Las cuotas de mypy dependen de los stubs fijados en `tools/requisitos_entorno.txt`: con un `.venv` sin ellos, mypy cuenta
menos y el gate pasaría en verde código que en rojo con los stubs. Por eso, antes de mypy, el gate ejecuta
`preparar_entorno.sh --comprobar` y, si falla, cada gate de mypy sale ✗ con su motivo, sin ejecutar mypy, y el total no cambia.

Cada prueba copia `check_all.sh`, `cuotas.txt`, el fichero de versiones real y `preparar_entorno.sh` (con `common.sh`) a una
raíz temporal con un `.venv` falso: `python` responde a lo que preguntan el script del entorno y los gates, y `ruff`, `mypy`
y `pytest` dan una salida fija y apuntan sus llamadas. No crean entornos ni usan la red.
Uso: .venv/bin/python -m pytest -q .docs/scripts/pruebas_gate_entorno.py"""
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

AQUI = Path(__file__).resolve().parent
RAIZ_REAL = AQUI.parent.parent
PYTHON_FALSO = """#!/usr/bin/env bash
if [[ "$1" == "-c" ]]; then echo "3.12"; exit 0; fi          # versión del .venv y gate yaml-configs
if [[ "$1 $2 $3" == "-m pip --version" ]]; then echo "pip 24.0"; exit 0; fi
if [[ "$1 $2 $3" == "-m pip freeze" ]]; then cat "$(dirname "$0")/freeze.txt"; exit 0; fi
if [[ "$1" == "-I" ]]; then shift; exec python3 -I "$@"; fi  # la comparación de preparar_entorno.sh, de verdad
exit 0                                                         # tools/*.py: corpus, nfc, secrets, refs-vivas
"""
APUNTA = """#!/usr/bin/env bash
echo "$(basename "$0") $*" >> "$(dirname "$0")/llamadas.log"
"""


def _pins() -> list[str]:
    texto = (RAIZ_REAL / "tools" / "requisitos_entorno.txt").read_text(encoding="utf-8")
    return [x for x in texto.splitlines() if x.strip() and not x.startswith("#")]


def _paquetes() -> list[str]:
    """Los paquetes que mide el gate, leídos del propio script (el número cambia si se quita un bloque)."""
    m = re.search(r"^PAQUETES=\(([^)]*)\)", (RAIZ_REAL / "tools" / "check_all.sh").read_text(encoding="utf-8"), re.M)
    assert m, "check_all.sh sin PAQUETES=(…)"
    return m.group(1).split()


@pytest.fixture
def raiz(tmp_path):
    for f in ("tools/check_all.sh", "tools/cuotas.txt", "tools/requisitos_entorno.txt",
              ".docs/scripts/preparar_entorno.sh", ".docs/scripts/common.sh"):
        (tmp_path / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(RAIZ_REAL / f, tmp_path / f)
    bin_ = tmp_path / ".venv" / "bin"
    bin_.mkdir(parents=True)
    programas = {"python": PYTHON_FALSO, "ruff": APUNTA, "mypy": APUNTA,
                 "pytest": APUNTA + 'echo "9999 passed in 1.00s"\n'}
    for nombre, texto in programas.items():
        (bin_ / nombre).write_text(texto, encoding="utf-8")
        (bin_ / nombre).chmod(0o755)
    (bin_ / "freeze.txt").write_text("\n".join(_pins()) + "\n", encoding="utf-8")
    return tmp_path


def gate(raiz: Path) -> tuple[int, str, list[str]]:
    env = {k: v for k, v in os.environ.items() if k not in ("VIRTUAL_ENV", "PYTHON_ENTORNO")}
    r = subprocess.run(["bash", str(raiz / "tools" / "check_all.sh")], cwd=raiz, capture_output=True, text=True,
                       env=env, check=False)
    salida = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr)
    log = raiz / ".venv" / "bin" / "llamadas.log"
    return r.returncode, salida, log.read_text(encoding="utf-8").splitlines() if log.exists() else []


def _total(salida: str) -> int:
    m = re.search(r"Gates ejecutados: (\d+)", salida)
    assert m, salida[-2000:]
    return int(m.group(1))


def test_con_el_entorno_conforme_mypy_se_ejecuta_y_pasa(raiz):
    codigo, salida, llamadas = gate(raiz)
    paquetes = _paquetes()
    assert codigo == 0, salida[-2000:]
    for paq in paquetes:
        assert f"✓ mypy {paq}" in salida
    assert len([x for x in llamadas if x.startswith("mypy ")]) == len(paquetes)
    assert "no coincide con tools/requisitos_entorno.txt" not in salida


@pytest.mark.parametrize("quitar", ["scipy-stubs", "types-PyYAML", "types-jsonschema"])
def test_sin_un_stub_fijado_los_gates_de_mypy_fallan_sin_ejecutarlo(raiz, quitar):
    _, salida_buena, _ = gate(raiz)
    (raiz / ".venv" / "bin" / "llamadas.log").unlink()
    freeze = [x for x in _pins() if not x.startswith(quitar + "==")]
    assert len(freeze) == len(_pins()) - 1
    (raiz / ".venv" / "bin" / "freeze.txt").write_text("\n".join(freeze) + "\n", encoding="utf-8")
    codigo, salida, llamadas = gate(raiz)
    paquetes = _paquetes()
    assert codigo == 1
    for paq in paquetes:
        assert (f"✗ mypy {paq}: el .venv no coincide con tools/requisitos_entorno.txt (stubs incluidos): "
                "ejecuta .docs/scripts/preparar_entorno.sh") in salida
        assert f"✓ mypy {paq}" not in salida
    assert f"falta {quitar.lower()}==" in salida                      # la salida de --comprobar dice qué falta
    assert not [x for x in llamadas if x.startswith("mypy ")]           # mypy no se ejecuta
    assert re.search(rf"Fallaron: {len(paquetes)}\b", salida)
    assert _total(salida) == _total(salida_buena)                       # el total de gates no cambia
    assert "✓ ruff (hallazgos)" in salida and "✓ pytest bloque_a" in salida   # los demás gates, igual


def test_un_paquete_sin_fijar_tambien_hace_fallar_mypy(raiz):
    (raiz / ".venv" / "bin" / "freeze.txt").write_text("\n".join(_pins() + ["pandas-stubs==3.1.0.261029"]) + "\n",
                                                       encoding="utf-8")
    codigo, salida, llamadas = gate(raiz)
    assert codigo == 1 and "pandas-stubs==3.1.0.261029 está instalado y no está fijado" in salida
    assert not [x for x in llamadas if x.startswith("mypy ")]
