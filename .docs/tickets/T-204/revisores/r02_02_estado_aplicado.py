"""QA r02 de T-204: tras aplicar la enmienda 6 y la limpieza (r02b), ningún documento vivo sigue diciendo que están
pendientes o propuestas (que el permiso lo bloqueara al principio es historia y puede quedarse), ni que la Constitución vigente es la V0.6.
Uso (desde la raíz): python3 -I .docs/tickets/T-204/revisores/r02_02_estado_aplicado.py. Sale con 1 si hay casos."""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
leer = lambda r: (RAIZ / r).read_text(encoding="utf-8")  # noqa: E731
casos = []
const = re.search(r"— (V\d+\.\d+)", leer("sistema_global/constitucion/Constitucion_Global.md").splitlines()[0]).group(1)
PEND = re.compile(r"(?i)lista para aplicar|sin aplicar|no se ha tocado|queda como estaba|solo propone|"
                  r"Pendiente del operador|La decisión es del operador|Si se aplica|no se pudo aplicar")
inc = leer("docs/incidencias.md")
for i in ("INC-T204-01", "INC-T204-03"):
    t = inc[inc.index(f"**{i}"):]
    t = t[:t.find("\n**INC-", 1)]
    if "RESUELTO" in t.split("\n", 1)[0]:
        for m in PEND.finditer(t):
            casos.append(f"docs/incidencias.md {i} (RESUELTO) aún dice «{m.group(0)}»")
fila = next(l for l in leer("sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md").splitlines()
            if l.startswith("| T-204 |"))
for m in PEND.finditer(fila):
    casos.append(f"fila T-204 de la deuda aún dice «{m.group(0)}»")
mem = leer(".docs/memoria/compartida/2026-11-25_bloque-a-forex-eliminado.md")
for m in PEND.finditer(mem):
    casos.append(f"memoria 2026-11-25_bloque-a-forex-eliminado aún dice «{m.group(0)}»")
rd = leer(".docs/tickets/T-204/README.md").split("## Registro")[0]   # el registro es historia
for m in PEND.finditer(rd):
    casos.append(f"README de T-204 aún dice «{m.group(0)}»")
for v in re.findall(r"Constitución global \((V\d+\.\d+) desde", leer("sistema_global/README.md")):
    if v != const:
        casos.append(f"sistema_global/README.md presenta la {v} como vigente; la Constitución está en la {const}")
print(f"{len(casos)} casos")
for c in casos:
    print("  " + c)
sys.exit(1 if casos else 0)
