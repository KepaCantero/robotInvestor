"""QA r02 de T-204: dos ataques a lo nuevo de la r02.
1. refs-vivas: una asignación de entorno (`PYTHONPATH=bloque_a_forex/11_Ejecutor pytest -q`) en un documento vivo debe
   hacer fallar el gate, como en la r01 (la r02 solo parte por «=» las palabras que empiezan por «-»).
2. `test_h02` de `pruebas_gate_bloques.py` no debe fallar cuando la Constitución pase legítimamente a otra versión (V0.8,
   la de la enmienda 5): se cambia la cabecera en el propio worktree, se ejecuta la prueba y se restaura.
Uso (desde la raíz): .venv/bin/python .docs/tickets/T-204/revisores/r02_03_ataques_r02.py. Sale con 1 si algo falla."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
malos = 0
for cita in ("PYTHONPATH=bloque_a_forex/11_Ejecutor pytest -q", "env PYTHONPATH=bloque_a_forex/11_Ejecutor python3 -m pytest"):
    with tempfile.TemporaryDirectory() as t:
        raiz = Path(t) / "repo"
        (raiz / "tools").mkdir(parents=True)
        (raiz / "docs").mkdir()
        shutil.copy(RAIZ / "tools" / "refs_vivas.py", raiz / "tools" / "refs_vivas.py")
        (raiz / "CLAUDE.md").write_text("Protocolo.\n", encoding="utf-8")
        (raiz / "docs" / "x.md").write_text(f"Ejecuta `{cita}`.\n", encoding="utf-8")
        rc = subprocess.run([sys.executable, "-I", str(raiz / "tools" / "refs_vivas.py")], capture_output=True, check=False).returncode
    ok = rc == 1
    malos += not ok
    print(f"{'OK   ' if ok else 'FALLO'} refs-vivas con `{cita}`: salida {rc}, esperada 1")
c = RAIZ / "sistema_global" / "constitucion" / "Constitucion_Global.md"
orig = c.read_text(encoding="utf-8")
c.write_text(orig.replace("— V0.7", "— V0.8", 1), encoding="utf-8")
try:
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-k", "h02",
                        ".docs/scripts/pruebas_gate_bloques.py"], cwd=RAIZ, capture_output=True, text=True, check=False)
finally:
    c.write_text(orig, encoding="utf-8")
ok = r.returncode == 0
malos += not ok
print(f"{'OK   ' if ok else 'FALLO'} test_h02 con la Constitución en una V0.8 legítima: {r.stdout.strip().splitlines()[-1]}")
sys.exit(1 if malos else 0)
