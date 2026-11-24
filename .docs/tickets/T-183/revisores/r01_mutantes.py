"""QA r01 de T-183 (Claude): mutantes propios de lo esencial. Cada mutante vive en una copia temporal de bloque_a.

    .venv/bin/python .docs/tickets/T-183/revisores/r01_mutantes.py

Pruebas que deben matarlos: las del ticket y las vecinas que tocan PS1 y F2.
Imprime MUERTO o VIVO por mutante; un VIVO que cambia el comportamiento es hallazgo (H-05 del qa.md).
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

raiz = Path(__file__).resolve().parents[4]
ej = Path("bloque_a/11_Ejecutor")
pruebas = ["tests/test_t183_raices.py", "tests/test_t181_fuentes.py", "tests/test_t182_procedencia.py",
           "tests/test_t65_qa_r01.py"]
O, S = "bloque_a/orquestacion.py", "bloque_a/sintesis.py"
mutaciones = [
    ("M1 raíces cuentan con la fuente retirada o en cuarentena", S,
     'and e.get("estado_verificacion") in ("VERIFICADA", "PENDIENTE")', 'and True'),
    ("M2 raíces por ref_id, no por origen documental", S,
     'origen = e.get("origen_documental") or e["ref_id"]', 'origen = e["ref_id"]'),
    ("M3 ps1_cumple de la CLM = PS1 de la opción", O,
     'clm["ps1_cumple"] = self._ps1(propias)', 'clm["ps1_cumple"] = f["_ps1"]'),
    ("M4 raíces cuentan evidencia contraria", S,
     ' and e.get("direccion") == "FAVORABLE"):', '):'),
    ("M5 raíz de la opción por fuente", O,
     'f["_raices"][evd.get("origen_documental", raiz)]', 'f["_raices"][fuente]'),
    ("M6 PS1 sin la excepción de la primaria de nivel A", O,
     'or any(n == "A" and t == "PRIMARIA" for n, t in raices.values())', 'or False'),
    ("M7 G3-DAT-09 lee F2 sin fecha", S,
     'f2 = bloque.almacen.estado("F2", paquete["fecha"], clave="clm_id")', 'f2 = bloque.almacen.estado("F2", clave="clm_id")'),
    ("M8 G3-DAT-09 nunca bloquea", S,
     '"resultado": "BLOQUEO" if incidencias else "OK",\n            "incidencias": incidencias}',
     '"resultado": "OK",\n            "incidencias": incidencias}'),
    ("M9 derivada enlazada aunque el soporte no sea RAIZ", O,
     'and por_id[eid].get("grado_independencia") == "RAIZ"}', '}'),
]


def correr(carpeta):
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *pruebas], cwd=carpeta / ej,
                          text=True, capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


with tempfile.TemporaryDirectory() as tmp:
    copia = Path(tmp)
    shutil.copytree(raiz / "bloque_a", copia / "bloque_a", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    base = correr(copia)
    if base.returncode:
        raise SystemExit(base.stdout[-3000:] + base.stderr[-3000:])
    for nombre, ruta, antes, despues in mutaciones:
        archivo = copia / ej / ruta
        original = archivo.read_text()
        assert original.count(antes) == 1, (nombre, original.count(antes))
        archivo.write_text(original.replace(antes, despues))
        r = correr(copia)
        archivo.write_text(original)
        print("MUERTO" if r.returncode else "VIVO  ", nombre, flush=True)
