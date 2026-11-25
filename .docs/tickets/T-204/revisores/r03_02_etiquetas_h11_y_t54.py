"""QA r03 de T-204:
1. los tickets que INC-T204-03 dice corregidos en la r03 (H-11) son los que cambió el commit de esa corrección (80d152ec);
2. la fila T-54 de la deuda, si cita la redacción antigua de D-20 («A Forex y B Forex fuera»), la anota como la Constitución
   anota D-20 y el cambio 17 (enmienda 6, D-48).
Uso (desde la raíz): python3 -I .docs/tickets/T-204/revisores/r03_02_etiquetas_h11_y_t54.py [commit]. Sale con 1 si hay casos."""
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
commit = sys.argv[1] if len(sys.argv) > 1 else "80d152ec"
casos = []
cambiados = subprocess.run(["git", "diff", "--name-only", f"{commit}~1", commit, "--", ".docs/tickets"], cwd=RAIZ,
                           capture_output=True, text=True, check=True).stdout.split()
reales = {re.match(r"\.docs/tickets/(T-\d+)/", f).group(1) for f in cambiados if not f.startswith(".docs/tickets/T-204/")}
inc = (RAIZ / "docs" / "incidencias.md").read_text(encoding="utf-8")
t = inc[inc.index("**INC-T204-03"):]
t = t[:t.find("\n**INC-", 1)]
seccion = t[t.find("Lo que se corrigió después"):]
seccion = seccion[:seccion.find("\nLas pruebas de")]
citados = set(re.findall(r"\bT-\d+\b", seccion)) - {"T-204"}
if citados != reales:
    casos.append(f"INC-T204-03 cita {sorted(citados)} como corregidos en la r03; {commit} cambió {sorted(reales)}")
deuda = (RAIZ / "sistema_global" / "seguimiento" / "Deuda_tecnica_y_pendientes_del_operador.md").read_text(encoding="utf-8")
fila = next(l for l in deuda.splitlines() if l.startswith("| T-54 |"))
if re.search(r"A Forex y B Forex fuera", fila) and "enmienda 6" not in fila:
    casos.append("la fila T-54 cita la redacción antigua de D-20 sin anotar la enmienda 6 (D-48)")
print(f"{len(casos)} casos")
for c in casos:
    print("  " + c)
sys.exit(1 if casos else 0)
