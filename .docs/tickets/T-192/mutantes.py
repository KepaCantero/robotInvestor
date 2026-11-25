"""Comprueba los catorce operadores de QA y los dos propios en copias temporales."""
import importlib.util
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ruta = Path(__file__).parent / "revisores/r01_mutantes_revisor.py"
spec = importlib.util.spec_from_file_location("mutantes_claude", ruta)
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)

actualizados = {
    "M13": ('if p < parametro(evaluador.cfg, "evaluacion.recalibracion_rk.p_reversion"):', 'if False:'),
    "M14": ('if n_pares >= parametro(evaluador.cfg, "evaluacion.min_calibrar") and medias:', 'if medias:'),
}
casos = [(nombre, archivo, *actualizados.get(nombre.split()[0], (antes, despues)))
         for nombre, archivo, antes, despues in qa.MUTANTES]
casos.extend([
    ("C01 ignora la fecha de la tasa base", qa.EV, 'fuga_base = max(fechas_base) > str(f0.date())', 'fuga_base = False'),
    ("C02 confirma como reversión", qa.SO, 'estado = "CONFIRMADO"', 'estado = "REVERTIDO"'),
])


def comprobar(caso):
    # El ejecutor r01 considera cualquier retorno distinto de cero como muerte. Aquí se requiere un fallo de aserción.
    nombre, ruta, antes, despues = caso
    import os
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        ej = Path(tmp) / qa.EJ
        shutil.copytree(qa.RAIZ / "bloque_a", Path(tmp) / "bloque_a",
                        ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
        archivo = ej / ruta
        original = archivo.read_text()
        if original.count(antes) != 1:
            return nombre, "NO APLICA"
        archivo.write_text(original.replace(antes, despues))
        res = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *qa.PRUEBAS],
                             cwd=ej, text=True, capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        return nombre, "MUERTO" if res.returncode == 1 and " failed" in res.stdout else "REVISAR"


if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "pytest", "-q", *qa.PRUEBAS], cwd=qa.RAIZ / qa.EJ, check=True)
    with ThreadPoolExecutor(3) as pool:
        estados = list(pool.map(comprobar, casos))
    for nombre, estado in estados:
        print(f"{estado}: {nombre}")
    sys.exit(int(any(estado != "MUERTO" for _, estado in estados)))
