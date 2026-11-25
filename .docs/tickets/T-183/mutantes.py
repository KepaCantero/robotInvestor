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

raiz = Path(__file__).resolve().parents[3]
ej = Path("bloque_a/11_Ejecutor")
pruebas = ["tests/test_t183_raices.py"]
mutaciones = [
    ('M1 incluye retiradas/cuarentena', 'bloque_a/sintesis.py', 'and e.get("estado_verificacion") in ("VERIFICADA", "PENDIENTE")', 'and True'),
    ('M2 ignora origen documental', 'bloque_a/sintesis.py', 'origen = e.get("origen_documental") or e["ref_id"]', 'origen = e["ref_id"]'),
    ('M3 aplica PS1 de la opción a cada CLM', 'bloque_a/orquestacion.py', 'cuenta, ps1 = len(propias), self._ps1(propias)', 'cuenta, ps1 = len(propias), any(self._ps1(sint.raices_de_evidencias(e for otra in f["_evidencias"] for e in sint.evidencias_raiz(clms[otra], por_id).values())) for f in finales if cid in f["_evidencias"])'),
    ('M4 acepta contrarias', 'bloque_a/sintesis.py', ' and e.get("direccion") == "FAVORABLE"):', '):'),
    ('M5 cuenta referencias en la opción', 'bloque_a/orquestacion.py', 'f["_raices"] = sint.raices_de_evidencias(respaldos.values())', 'f["_raices"] = {e["ref_id"]: (e["nivel_fuente"], e["tipo_fuente"]) for e in respaldos.values()}'),
    ('M6 ignora primaria A', 'bloque_a/procedencia.py', 'or any(n == "A" and t == "PRIMARIA" for n, t in raices.values())', 'or False'),
    ('M7 ignora fecha F2', 'bloque_a/sintesis.py', 'f2 = bloque.almacen.estado("F2", paquete["fecha"], clave="clm_id")', 'f2 = bloque.almacen.estado("F2", clave="clm_id")'),
    ('M8 G3 siempre OK', 'bloque_a/sintesis.py', '"nombre": "Raíces independientes", "resultado": estado', '"nombre": "Raíces independientes", "resultado": "OK"'),
    ('M9 admite derivada como soporte raíz', 'bloque_a/procedencia.py', 'if origen != fuente:', 'if False:'),
    ('M10 omite similitud', 'bloque_a/procedencia.py', 'if trios and cid in clms:', 'if False:'),
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
        muerto = r.returncode == 1 and " failed" in r.stdout
        print("MUERTO" if muerto else "VIVO  ", nombre, flush=True)
