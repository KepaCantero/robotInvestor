"""Ejecutar con la venv del repositorio. Cada mutante vive en una copia temporal."""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

raiz = Path(__file__).resolve().parents[3]
ej = Path("bloque_a/11_Ejecutor")
prueba = "tests/test_t193_ingesta.py"
mutaciones = [['bloque_a/herramientas/ht08_monitor.py', 'if lenta or q > self.umbral_cola:', 'if q > self.umbral_cola:'], ['bloque_a/herramientas/ht08_monitor.py', 'if self._lecturas_vacias[ag] >= 2:', 'if self._lecturas_vacias[ag] >= 3:']]


def correr(carpeta):
    return subprocess.run([sys.executable, "-m", "pytest", "-q", prueba], cwd=carpeta / ej, text=True,
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
