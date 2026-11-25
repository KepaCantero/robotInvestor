"""QA r01 de T-188 (Claude): mutantes propios de lo esencial. Cada mutante vive en una copia temporal de bloque_a/;
el repositorio no se toca. Uso (venv del repositorio): python .docs/tickets/T-188/revisores/r01_02_mutantes.py
Un mutante VIVO (las pruebas del ticket siguen en verde) que cambia el comportamiento es un hallazgo."""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

raiz = Path(__file__).resolve().parents[4]
ej = Path("bloque_a/11_Ejecutor")
pruebas = ["tests/test_t188_producto.py", "tests/test_v51.py::test_consulta_validaciones_agrupacion_y_entrante",
           "tests/test_fase4_huecos.py::test_pb11_la_opcion_descartada_se_resuelve_y_cuenta_en_el_historial"]
MUT = [
    ("M1 muestra ignorada", "bloque_a/evaluador.py",
     '< parametro(self.cfg, "evaluacion.min_calibrar"):\n                return None\n            resumen = []',
     '< 0:\n                return None\n            resumen = []'),
    ("M2 decisión a cualquier fecha", "bloque_a/evaluador.py",
     'if p["fecha_emision"] <= x["fecha"] < limite), {})', 'if True), {})'),
    ("M3 análisis = consultas", "bloque_a/interfaz_broker.py",
     'por_run = {c["run_id"]: c["cns_id"] for c in iguales if c.get("run_id")}',
     'por_run = {c["cns_id"]: c["cns_id"] for c in iguales}'),
    ("M4 primera decisión y no la última", "bloque_a/evaluador.py",
     'next((x for x in reversed(decisiones.get(p.get("opp_id"), []))', 'next((x for x in (decisiones.get(p.get("opp_id"), []))'),
    ("M5 grupos intercambiados en el texto", "bloque_a/evaluador.py",
     'etiqueta = "enviadas" if nombre == "ENVIADA_A_BLOQUE_B" else "descartadas"',
     'etiqueta = "descartadas" if nombre == "ENVIADA_A_BLOQUE_B" else "enviadas"'),
    ("M6 cuenta fallos como aciertos", "bloque_a/evaluador.py",
     'total = sum(p["resolucion"]["resultado_binario"] for p in grupo)', 'total = len(grupo)'),
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
