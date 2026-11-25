"""Ejecutar con la venv del repositorio. Cada mutante vive en una copia temporal."""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

raiz = Path(__file__).resolve().parents[3]
ej = Path("bloque_a/11_Ejecutor")
prueba = "tests/test_t181_fuentes.py"
mutaciones = [
    ('rev.get("hash") != r["hash"]', "False"),
    ('if clave not in alertas:', 'if True:'),
    ('if dia <= fecha}', 'if True}'),
    ('mantiene = op.get("ps1") is True and bloque._ps1(raices)', 'mantiene = True'),
    ('datos.get("archived_snapshots") == {}', 'True'),
    ('copia["hash"] != ficha.campo("Hash de contenido")', 'False'),
    ('if ruta.read_text(encoding="utf-8") != original:', 'if False:'),
    ('q = sum(puntos)', 'q = sum(puntos) - 1'),
]


def correr(carpeta):
    return subprocess.run([sys.executable, "-m", "pytest", "-q", prueba], cwd=carpeta / ej, text=True,
                          capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


with tempfile.TemporaryDirectory() as tmp:
    copia = Path(tmp)
    shutil.copytree(raiz / "bloque_a", copia / "bloque_a", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    base = correr(copia)
    if base.returncode:
        raise SystemExit(base.stdout + base.stderr)
    archivo = copia / ej / "bloque_a/mantenimiento_fuentes.py"
    original = archivo.read_text()
    for antes, despues in mutaciones:
        assert original.count(antes) == 1, antes
        archivo.write_text(original.replace(antes, despues))
        resultado = correr(copia)
        if resultado.returncode != 1 or " failed" not in resultado.stdout:
            raise SystemExit(f"Mutante sin fallo de prueba demostrado: {antes}\n{resultado.stdout}")
        print("Detectado:", antes, flush=True)
