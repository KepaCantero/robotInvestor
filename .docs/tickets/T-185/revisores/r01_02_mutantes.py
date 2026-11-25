"""QA r01 de T-185 (Claude): mutantes propios de lo esencial. Cada mutante vive en una copia temporal de bloque_a/;
el repositorio no se toca. Uso (venv del repositorio): python .docs/tickets/T-185/revisores/r01_02_mutantes.py
Un mutante VIVO (las pruebas del ticket y las vecinas siguen en verde) que cambia el comportamiento es un hallazgo."""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

raiz = Path(__file__).resolve().parents[4]
ej = Path("bloque_a/11_Ejecutor")
pruebas = ["tests/test_t185_rotacion.py", "tests/test_t65_resto_t53.py::test_cs10_celdas_de_rotacion_exploratoria_de_la_configuracion",
           "tests/test_integracion.py::test_gc0_negativo_arrastre_verificado"]
MUT = [
    ("M1 bolsa de cribado = presupuesto entero", "bloque_a/orquestacion.py",
     'uc_cribado = presupuesto.asignado[clase] * parametro(self.cfg, "presupuesto_uc.reparto_fases.cribado")',
     'uc_cribado = presupuesto.asignado[clase]'),
    ("M2 sin validación de la fracción", "bloque_a/orquestacion.py",
     'if isinstance(fraccion, bool) or not isinstance(fraccion, (int, float)) or not 0 <= fraccion <= 1:',
     'if False:'),
    ("M3 fracción nula sigue explorando", "bloque_a/orquestacion.py",
     '            if not uc_rotacion:\n                rot = []\n', ''),
    ("M4 F5 y CT-06 con símbolos distintos", "bloque_a/orquestacion.py",
     '"uc_vigentes": uc_cribado - uc_rotacion, "simbolos": rot}', '"uc_vigentes": uc_cribado - uc_rotacion, "simbolos": rot[:1]}'),
]


def correr(carpeta):
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *pruebas], cwd=carpeta / ej, text=True,
                          capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


with tempfile.TemporaryDirectory() as tmp:
    copia = Path(tmp)
    shutil.copytree(raiz / "bloque_a", copia / "bloque_a", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    base = correr(copia)
    if base.returncode:
        raise SystemExit(base.stdout[-3000:] + base.stderr[-3000:])
    for nombre, ruta, antes, despues in MUT:
        archivo = copia / ej / ruta
        original = archivo.read_text()
        assert original.count(antes) == 1, nombre
        archivo.write_text(original.replace(antes, despues))
        r = correr(copia)
        archivo.write_text(original)
        print(("MUERTO " if r.returncode else "VIVO   ") + nombre, flush=True)
