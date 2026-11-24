"""QA r01 de T-199 (revisor): aplica un mutante de `mutantes.py` y ejecuta contra él los nodos de prueba que se le den.
Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-199/revisores/r01_03_mutantes_contra.py M13 nodo [nodo…]
Restaura siempre el fichero. Imprime MUERTO / VIVO y la primera línea «E» de pytest."""
import importlib.util
import subprocess
import sys
from pathlib import Path

nombre, nodos = sys.argv[1], sys.argv[2:]
sys.argv = [sys.argv[0], "."]
spec = importlib.util.spec_from_file_location("mut199", Path(__file__).parents[1] / "mutantes.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
(_, f, cambios, _), = [m for m in mod.M if m[0].split()[0] == nombre]
p = Path(f)
orig = p.read_text(encoding="utf-8")
mut = orig
for a, b in cambios:
    assert mut.count(a) == 1
    mut = mut.replace(a, b)
p.write_text(mut, encoding="utf-8")
try:
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "--rootdir=.", *nodos],
                       capture_output=True, text=True, check=False, timeout=1200)
except subprocess.TimeoutExpired:
    r = subprocess.CompletedProcess([], 1, "E   (más de 20 min: cuelgue)", "")
finally:
    p.write_text(orig, encoding="utf-8")
e = next((ln.strip() for ln in r.stdout.splitlines() if ln.lstrip().startswith("E ")), "")
print(f"{nombre}: {'VIVO' if r.returncode == 0 else 'MUERTO'} {e[:200]}")
