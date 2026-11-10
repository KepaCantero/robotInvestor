"""El LEEME del marco común de C frente al disco: la lista de «Cómo se ejecuta» y las comprobaciones que cita cada batería (nació como r01 de la QA de T-79).

- La lista de «Cómo se ejecuta» coincide con pruebas/ejecutar_pruebas.py + pruebas/pruebas_*.py.
- Cada batería se ejecuta (python -I) y se cuentan sus líneas «OK »/«FALLA »; el número se compara con el que cita el LEEME
  en la fila de la tabla («| `pruebas/x.py` | N comprobaciones») y en el punto «Comprobado en …» (`pruebas/x.py`, N comprobaciones).

Uso: .venv/bin/python -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c (necesita jsonschema: con el python del sistema las baterías no arrancan y todo sale como diferencia) [bateria1.py ...]
"""
import re
import subprocess
import sys
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve()
SOLO = set(sys.argv[2:])
leeme = (MARCO / "LEEME.md").read_text(encoding="utf-8")
sec = leeme.split("## Cómo se ejecuta", 1)[1].split("```")[1]
lista = sorted(set(re.findall(r"^python3 (pruebas/(?:pruebas_\w+|ejecutar_pruebas)\.py)", sec, re.M)))
disco = sorted(str(p.relative_to(MARCO)) for p in [MARCO / "pruebas/ejecutar_pruebas.py", *(MARCO / "pruebas").glob("pruebas_*.py")])
fallos = []
if lista != disco:
    fallos.append(f"lista de ejecución distinta del disco: solo LEEME {sorted(set(lista)-set(disco))}, solo disco {sorted(set(disco)-set(lista))}")
print(f"lista de ejecución: {len(lista)} órdenes; disco: {len(disco)} baterías")

for rel in disco:
    nombre = Path(rel).name
    if SOLO and nombre not in SOLO:
        continue
    citas = set()
    for m in re.finditer(r"^\| `" + re.escape(rel) + r"` \| (\d+) comprobaciones", leeme, re.M):
        citas.add(("tabla", int(m.group(1))))
    for m in re.finditer(r"\(`" + re.escape(rel) + r"`, (\d+) comprobaciones", leeme):
        citas.add(("comprobado", int(m.group(1))))
    if not citas:
        continue
    r = subprocess.run([sys.executable, "-I", nombre], cwd=MARCO / "pruebas", capture_output=True, text=True, timeout=300)
    n = sum(1 for l in r.stdout.splitlines() if re.match(r"^(OK|FALLA)\s", l))
    malas = sorted(c for c in citas if c[1] != n)
    estado = "OK" if not malas else "DISTINTO"
    print(f"{estado:9} {nombre}: ejecuta {n}; LEEME cita {sorted(citas)}")
    if malas:
        fallos.append(f"{nombre}: ejecuta {n} comprobaciones y el LEEME cita {malas}")
print()
print("\n".join(fallos) if fallos else "sin diferencias")
print(f"RESULTADO r01 LEEME: {'HAY DIFERENCIAS' if fallos else 'SIN DIFERENCIAS'} ({len(fallos)})")
