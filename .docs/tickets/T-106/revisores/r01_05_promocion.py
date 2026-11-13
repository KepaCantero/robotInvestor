"""QA r01 de T-106 · Reproduce la promoción del Catálogo desde el Catálogo anterior al commit y comprueba el re-congelado.

1. En una raíz temporal: el Catálogo del commit padre + el script de promoción del commit + el ejecutor del commit.
   `--aplicar` debe dar, byte a byte, el Catálogo commiteado. Una segunda pasada no debe cambiar nada (idempotencia).
2. La huella del Catálogo padre es la que tenía el manifiesto antes; la del commiteado, la de ahora; y el manifiesto solo
   cambia en esa línea.
3. La copia .docx no se ha tocado.

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r01_05_promocion.py [RAIZ] [COMMIT]
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
RAIZ = Path(args[0] if args else C.raiz_por_defecto()).resolve()
COMMIT = args[1] if len(args) > 1 else "7064f60"
REL = "bloque_a/04_Motor_conocimiento_y_catalogo/Catálogo de cálculos del Motor - V5.0.md"


def git(*a: str) -> bytes:
    return subprocess.run(["git", "-C", str(RAIZ), *a], capture_output=True, check=True).stdout


padre, ahora = git("show", f"{COMMIT}^:{REL}"), git("show", f"{COMMIT}:{REL}")
tmp = Path(tempfile.mkdtemp(prefix="qa_t106_prom_"))
(tmp / ".docs" / "scripts").mkdir(parents=True)
(tmp / ".docs" / "scripts" / "promover_fichas_catalogo.py").write_bytes(git("show", f"{COMMIT}:.docs/scripts/promover_fichas_catalogo.py"))
(tmp / "bloque_a").mkdir()
(tmp / "bloque_a" / "11_Ejecutor").symlink_to(RAIZ / "bloque_a" / "11_Ejecutor")
cat = tmp / REL
cat.parent.mkdir(parents=True)
cat.write_bytes(padre)
py = str(RAIZ / ".venv" / "bin" / "python")
r1 = subprocess.run([py, "-I", "-B", str(tmp / ".docs/scripts/promover_fichas_catalogo.py"), "--aplicar"], capture_output=True,
                    text=True, cwd=tmp, timeout=600)
print(r1.stdout[-600:], r1.stderr[-400:])
C.informe("la promoción desde el Catálogo padre sale con código 0 y promueve 21", r1.returncode == 0 and "Promovidas: 21" in r1.stdout)
C.informe("el Catálogo promovido es byte a byte el commiteado", cat.read_bytes() == ahora,
          f"{hashlib.sha256(cat.read_bytes()).hexdigest()[:16]} vs {hashlib.sha256(ahora).hexdigest()[:16]}")
r2 = subprocess.run([py, "-I", "-B", str(tmp / ".docs/scripts/promover_fichas_catalogo.py"), "--aplicar"], capture_output=True,
                    text=True, cwd=tmp, timeout=600)
C.informe("segunda pasada idempotente (0 promovidas, archivo igual)", "Promovidas: 0" in r2.stdout and cat.read_bytes() == ahora)
shutil.rmtree(tmp, ignore_errors=True)

man_padre = git("show", f"{COMMIT}^:tools/corpus_manifest.txt").decode()
man_ahora = git("show", f"{COMMIT}:tools/corpus_manifest.txt").decode()
C.informe("manifiesto padre = huella del Catálogo padre", hashlib.sha256(padre).hexdigest() in man_padre)
C.informe("manifiesto del commit = huella del Catálogo commiteado", hashlib.sha256(ahora).hexdigest() in man_ahora)
dif = [(a, b) for a, b in zip(man_padre.splitlines(), man_ahora.splitlines()) if a != b]
C.informe("el manifiesto solo cambia en la línea del Catálogo", len(dif) == 1 and REL in dif[0][1]
          and len(man_padre.splitlines()) == len(man_ahora.splitlines()), str(len(dif)))
docx = git("diff", "--name-only", f"{COMMIT}^", COMMIT, "--", "*.docx").decode().strip()
C.informe("ningún .docx tocado", not docx, docx)
sys.exit(C.resumen())
