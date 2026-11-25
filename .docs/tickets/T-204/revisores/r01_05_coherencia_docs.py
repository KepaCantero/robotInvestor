"""QA r01 de T-204: coherencia de los documentos vivos con el estado real tras quitar el Forex.
- `docs/AVANCE.md` no da por hecha una versión de la Constitución que no es la de su cabecera;
- las líneas base que citan la skill `ri-probar` y `CLAUDE.md` son las de `tools/cuotas.txt`;
- el número de hallazgos de `.secrets.baseline` que cita `CLAUDE.md` es el del fichero;
- `.pre-commit-config.yaml` no cita un número de gates distinto del gate (10).
Uso (desde la raíz): python3 -I .docs/tickets/T-204/revisores/r01_05_coherencia_docs.py. Sale con 1 si hay casos."""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
leer = lambda r: (RAIZ / r).read_text(encoding="utf-8")  # noqa: E731
casos = []
const = re.search(r"— (V\d+\.\d+)", leer("sistema_global/constitucion/Constitucion_Global.md").splitlines()[0]).group(1)
for v in re.findall(r"Constitución pasa a la (V\d+\.\d+)", leer("docs/AVANCE.md")):
    if v != const:
        casos.append(f"docs/AVANCE.md dice que la Constitución pasa a la {v}; su cabecera dice {const}")
cuotas = dict(l.split("=", 1) for l in leer("tools/cuotas.txt").splitlines() if l and not l.startswith("#"))
base = {"A": cuotas["pytest_bloque_a"], "B": cuotas["pytest_bloque_b"]}
for ruta in (".agents/skills/ri-probar/SKILL.md", "CLAUDE.md"):
    for b, n in re.findall(r"\b([AB]) ≥ (\d+)", leer(ruta)):
        if n != base[b]:
            casos.append(f"{ruta} dice {b} ≥ {n}; tools/cuotas.txt dice {base[b]}")
n_base = sum(len(v) for v in json.loads(leer(".secrets.baseline"))["results"].values())
for n in re.findall(r"\.secrets\.baseline` \((\d+) hallazgos", leer("CLAUDE.md")):
    if int(n) != n_base:
        casos.append(f"CLAUDE.md cita {n} hallazgos en .secrets.baseline; el fichero tiene {n_base}")
for n in re.findall(r"\((\d+) gates\)", leer(".pre-commit-config.yaml")):
    if n != "10":
        casos.append(f".pre-commit-config.yaml dice {n} gates; el gate tiene 10")
print(f"{len(casos)} casos")
for c in casos:
    print("  " + c)
sys.exit(1 if casos else 0)
