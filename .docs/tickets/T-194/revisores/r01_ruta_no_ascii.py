"""T-194 · QA r01 · H-07: un entregable con una ruta no ASCII y cambios sin commit no avisa, porque
`git status --porcelain` la entrecomilla y escapa (core.quotePath) y la comparación con la ruta de la fila falla.
Reutiliza el repositorio de prueba de `pruebas_cola_astra.py`. Uso, desde la raíz:
  .venv/bin/python -I .docs/tickets/T-194/revisores/r01_ruta_no_ascii.py      (1 = el defecto sigue)
"""
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / ".docs/scripts"))
import pruebas_cola_astra as p  # noqa: E402

p.FILAS[3] = ("C-04", "REVISION", "`.docs/diseño/bloque_d/revisión.md`")
with tempfile.TemporaryDirectory() as tmp:
    r = p.Repo(Path(tmp) / "repo")
    r.escribir(".docs/diseño/bloque_d/revisión.md", "BORRADOR\n")
    r.escribir(".docs/diseño/bloque_d/revisión.md", "BORRADOR, más\n", commit=False)
    rc, out = r.correr()
    ok = "C-04: el entregable tiene cambios sin commit" in out
    print("OK   avisa con una ruta no ASCII" if ok else "FALLA (H-07) no avisa con una ruta no ASCII:\n" + out)
    sys.exit(0 if ok else 1)
