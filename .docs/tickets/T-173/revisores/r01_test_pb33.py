"""QA r01 de T-173: el PB-33 ORIGINAL (develop 80751da) con la degradación DM neutralizada debe seguir pasando sobre wip/t173
(el comportamiento de PB-33 no cambia; solo se le suma la degradación). Y con la DM activa, la vista H3 de RV desaparece.
Uso (desde bloque_a/11_Ejecutor): PYTHONPATH=. pytest -q -p no:cacheprovider ../../.docs/tickets/T-173/revisores/r01_test_pb33.py"""
import subprocess
import sys
import types
from pathlib import Path

from bloque_a.evaluador import Evaluador

sys.path.insert(0, str(Path.cwd() / "tests"))
_src = subprocess.run(["git", "show", "80751da:bloque_a/11_Ejecutor/tests/test_fase4_huecos.py"], capture_output=True,
                      text=True, check=True).stdout   # la prueba tal como estaba en develop
orig = types.ModuleType("pb33_original")
orig.__file__ = str(Path.cwd() / "tests" / "test_fase4_huecos.py")
exec(compile(_src, orig.__file__, "exec"), orig.__dict__)
from conftest import universo  # noqa: E402,F401


def test_pb33_original_con_dm_neutralizada(tmp_path, universo, monkeypatch):  # noqa: F811
    monkeypatch.setattr(Evaluador, "aplicar_degradacion_dm", lambda self, *a, **k: [])
    orig.test_pb33_tras_la_revocacion_hay_alerta_de_sobreconfianza_y_el_run_siguiente_no_publica_probabilidad(tmp_path, universo)
