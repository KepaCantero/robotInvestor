"""Revisión de Claude (antes de T-92) de la rama de Astra: ¿el filtro R8 nuevo (contenido_sensible) bloquea prompts legítimos del corpus? Uso: python -I r01_02… <11_Ejecutor> <raíz bloque_a>"""
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from bloque_a.llm import contenido_sensible
from bloque_a.contratos import RE_SECRETO
n = 0
for p in sorted(Path(sys.argv[2]).rglob("*.md")):
    t = p.read_text(encoding="utf-8", errors="replace")
    if contenido_sensible(t):
        n += 1
        m = RE_SECRETO.search(t + '"')
        print("BLOQUEA", p.relative_to(sys.argv[2]), repr(t[max(0, m.start()-40):m.end()+20]))
print("ficheros que el filtro bloquearía:", n)
