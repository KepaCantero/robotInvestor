"""T-203 · cuota de ruff del Bloque A: lo que no es una sustitución literal no cambia nada.

1. HT-02, HT-03 y HT-07 (`bloque_a/herramientas/ht02.py`, `ht03.py`, `ht07.py`): desde el rebase sobre T-201 los
   envoltorios son los de T-201 (con `TYPE_CHECKING`) y T-203 ya no los cambia. La prueba se queda como guarda de
   equivalencia: en un intérprete nuevo, sin la carpeta de referencia en `sys.path`, cada módulo carga y reexporta
   exactamente lo mismo que la referencia (los mismos objetos), con `modulo`, `DIR_REFERENCIA` y `TYPE_CHECKING`.
2. `motor/operaciones.py` y `mock_respuestas.py` (UP006, UP045, UP035): `Dict`, `List`, `Optional` y
   `typing.Sequence` pasan a `dict`, `list`, `X | None` y `collections.abc.Sequence` solo en anotaciones, que
   siguen sin evaluarse al definir la función (`from __future__ import annotations`) y que, si alguien las
   evalúa, se resuelven todas con Python 3.12.
"""
import inspect
import json
import subprocess
import sys
import typing

import pytest
from bloque_a.motor import operaciones
from conftest import RAIZ

from bloque_a import mock_respuestas

SONDA = """
import json, sys
ref_dir = sys.argv[1]
sys.path[:] = [p for p in sys.path if p.rstrip("/") != ref_dir]
import importlib
mod = importlib.import_module("bloque_a.herramientas." + sys.argv[2])
ref = sys.modules[sys.argv[3]]
publicos = sorted(n for n in vars(ref) if not n.startswith("_"))
print(json.dumps({
    "nombres": sorted(n for n in vars(mod) if not n.startswith("__")),
    "publicos": publicos,
    "mismos_objetos": all(getattr(mod, n) is getattr(ref, n) for n in publicos),
    "modulo_es_ref": mod.modulo is ref and mod._ref is ref,
    "fichero_ref": ref.__file__,
    "dir_referencia": str(mod.DIR_REFERENCIA),
    "ref_en_path": ref_dir in sys.path,
}))
"""


@pytest.mark.parametrize("corto,referencia", [("ht02", "ht02_verificador_enlaces"), ("ht03", "ht03_puntuaciones"),
                                              ("ht07", "ht07_legibilidad")])
def test_reexportacion_de_referencia_sin_cambios(corto, referencia):
    ref_dir = RAIZ / "bloque_a" / "herramientas" / "referencia"
    r = subprocess.run([sys.executable, "-c", SONDA, str(ref_dir), corto, referencia], cwd=RAIZ,
                       capture_output=True, text=True, check=True, env={"PYTHONPATH": str(RAIZ), "PATH": ""})
    d = json.loads(r.stdout)
    assert d["publicos"], "la referencia no exporta nada"
    assert d["nombres"] == sorted([*d["publicos"], "DIR_REFERENCIA", "TYPE_CHECKING", "_ref", "modulo"])
    assert d["mismos_objetos"] and d["modulo_es_ref"] and d["ref_en_path"]
    assert d["fichero_ref"] == str(ref_dir / f"{referencia}.py") and d["dir_referencia"] == str(ref_dir)


@pytest.mark.parametrize("modulo", [operaciones, mock_respuestas], ids=["operaciones", "mock_respuestas"])
def test_anotaciones_sin_evaluar_y_resolubles(modulo):
    funciones = [f for _, f in inspect.getmembers(modulo, inspect.isfunction) if f.__module__ == modulo.__name__]
    assert len(funciones) > 5
    anotadas = 0
    for f in funciones:
        crudas = f.__annotations__
        assert all(isinstance(v, str) for v in crudas.values()), f.__name__   # aplazadas: nada se evalúa al definir
        resueltas = typing.get_type_hints(f)
        assert set(resueltas) == set(crudas), f.__name__
        anotadas += bool(crudas)
    assert anotadas > 5
    for nombre in ("Dict", "List", "Optional", "Tuple"):
        assert not hasattr(modulo, nombre)            # nadie los toma de aquí (se comprobó con grep en T-203)
