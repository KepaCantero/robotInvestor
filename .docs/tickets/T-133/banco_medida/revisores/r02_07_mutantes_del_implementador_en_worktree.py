"""T-133 QA r02 · Los mutantes de `mutantes.py` (del implementador) ejecutados en un WORKTREE.

`mutantes.py` copia `.docs/scripts` a un temporal sin `bloque_a`; desde 0.5.0 `banco_medida.py` lee al importarse la
configuración de A (`_minimo_de_a`), así que en esa copia la importación falla con NameError y TODOS los mutantes «mueren»
sin que se ejecute una prueba. Este script toma su lista de mutantes tal cual y los ejecuta en un worktree completo (con
`bloque_a`), como r01_04 y r02_06, sin la prueba de integración (igual que `mutantes.py`).
Uso: .venv/bin/python -B r02_07_mutantes_del_implementador_en_worktree.py <worktree>"""
import importlib.util
import subprocess
import sys
from pathlib import Path

ARBOL_PRINCIPAL = Path(__file__).resolve().parents[5]
if len(sys.argv) < 2:
    sys.exit("uso: r02_07_mutantes_del_implementador_en_worktree.py <worktree>")
W = Path(sys.argv[1]).resolve()
if W == ARBOL_PRINCIPAL:
    sys.exit("me niego a mutar el árbol principal: pásame un worktree")
spec = importlib.util.spec_from_file_location("mutantes_impl", Path(__file__).resolve().parents[1] / "mutantes.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
F = W / ".docs" / "scripts" / "banco_medida.py"
ORIGINAL = F.read_text(encoding="utf-8")


def pytest() -> int:
    return subprocess.run([str(W / ".venv" / "bin" / "python"), "-B", "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "-k",
                           "not integracion", ".docs/scripts/pruebas_banco_medida.py"], cwd=W, capture_output=True, text=True,
                          timeout=900, check=False).returncode


if pytest() != 0:
    sys.exit("la suite no pasa sin mutar en el worktree: nada que medir")
vivos = []
try:
    for nombre, (viejo, nuevo) in mod.MUTANTES.items():
        if ORIGINAL.count(viejo) != 1:
            print(f"SIN PATRÓN  {nombre}", flush=True)
            vivos.append(nombre + " (sin patrón)")
            continue
        F.write_text(ORIGINAL.replace(viejo, nuevo), encoding="utf-8")
        muere = pytest() != 0
        print(("muere " if muere else "VIVE  ") + nombre, flush=True)
        if not muere:
            vivos.append(nombre)
finally:
    F.write_text(ORIGINAL, encoding="utf-8")
estado = subprocess.run(["git", "status", "--short"], cwd=W, capture_output=True, text=True, check=False).stdout
print(f"\n{len(mod.MUTANTES)} mutantes, {len(vivos)} vivos: {vivos}")
print(f"git status del worktree: {estado.strip() or 'vacío'}")
