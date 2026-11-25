"""Ejecutar con la venv del repositorio. Cada mutante vive en una copia temporal."""
import ast
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

raiz = Path(__file__).resolve().parents[3]
ej = Path("bloque_a/11_Ejecutor")
pruebas = ["tests/test_t191_degradado.py", "tests/test_t159_extremo_a_extremo.py::test_pb52_con_ht09_caido_nunca_hay_apto_por_defecto_ni_entrega"]
# Reutiliza los operadores publicados por Claude sin ejecutar el programa durante la lectura.
revisor = raiz / ".docs/tickets/T-191/revisores/r01_mutantes.py"
tabla = next(n.value for n in ast.parse(revisor.read_text()).body
             if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "MUT" for t in n.targets))
_, revisados = ast.literal_eval(tabla)["T-191"]
mutaciones = [(ruta, antes, despues) for nombre, ruta, antes, despues in revisados if nombre != "captura cualquier excepción"]
mutaciones.extend([
    ("bloque_a/sintesis.py", "except ht09.HerramientaNoDisponible as exc:", "except Exception as exc:"),
    ("bloque_a/sintesis.py", "except ht09.HerramientaNoDisponible as exc:", "except ImportError as exc:"),
    ("bloque_a/sintesis.py", 'return {"dictamen": "BLOQUEADO", "modo": "G3_MANUAL"', 'return {"dictamen": "APTO", "modo": "G3_MANUAL"'),
])



def correr(carpeta):
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", *pruebas], cwd=carpeta / ej, text=True,
                          capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


with tempfile.TemporaryDirectory() as tmp:
    copia = Path(tmp)
    shutil.copytree(raiz / "bloque_a", copia / "bloque_a", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    base = correr(copia)
    if base.returncode:
        raise SystemExit(base.stdout + base.stderr)
    for ruta, antes, despues in mutaciones:
        archivo = copia / ej / ruta
        original = archivo.read_text()
        assert original.count(antes) == 1, antes
        archivo.write_text(original.replace(antes, despues))
        resultado = correr(copia)
        archivo.write_text(original)
        if resultado.returncode != 1 or " failed" not in resultado.stdout:
            raise SystemExit(f"Mutante sin fallo de prueba demostrado: {antes}\n{resultado.stdout}")
        print("Detectado:", antes, flush=True)
