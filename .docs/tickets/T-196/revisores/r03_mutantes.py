"""QA r03 de T-196 (revisor): mutantes propios de las correcciones de la r03. Uso (desde bloque_a/11_Ejecutor):
../../.venv/bin/python ../../.docs/tickets/T-196/revisores/r03_mutantes.py . [P1 …]"""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
TIEMPO = 900
COLA, RF, ORQ, CLI = "bloque_a/cola_peticiones.py", "bloque_a/respuesta_final.py", "bloque_a/orquestacion.py", "bloque_a/cli.py"
M = [
 ("P1 el retroceso solo se mide contra el primer instante", COLA, "            previo = t\n", ""),
 ("P2 un instante igual al anterior cuenta como retroceso", COLA, "            if t < previo:", "            if t <= previo:"),
]
vivos = []
SOLO = sys.argv[2:]
M = [m for m in M if not SOLO or m[0].split()[0] in SOLO]
for nombre, f, a, b in M:
    p = EJ / f
    orig = p.read_text(encoding="utf-8")
    assert orig.count(a) == 1, (nombre, orig.count(a))
    p.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t196.py"],
                           cwd=EJ, capture_output=True, text=True, check=False, timeout=TIEMPO)
        muerto = r.returncode != 0
    except subprocess.TimeoutExpired:
        muerto = True
    finally:
        p.write_text(orig, encoding="utf-8")
    print(f"{nombre}: {'MUERTO' if muerto else 'VIVO'}", flush=True)
    if not muerto:
        vivos.append(nombre)
print(f"{len(M) - len(vivos)} muertos, {len(vivos)} vivos: {vivos}")
sys.exit(1 if vivos else 0)
