"""Revisión de Claude (antes de T-92) de la rama de Astra: falsos positivos del patrón sk-… de RE_SECRETO (sin límite de palabra) en las referencias que se envían a los agentes,
y efecto en Agentes.llamar: el encargo queda bloqueado por R8 (PARCIAL) sin llamar al modelo.
Uso: python -I r01_03… <11_Ejecutor de la rama> <raíz bloque_a de la rama>"""
import re, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from bloque_a.contratos import RE_SECRETO
from bloque_a.llm import contenido_sensible
total = 0
for p in sorted((Path(sys.argv[2]) / "05_Archivos_operativos").glob("*.md")):
    lineas = [l for l in p.read_text(encoding="utf-8").splitlines() if RE_SECRETO.search(l + '"')]
    if lineas:
        total += len(lineas)
        ids = sorted({m for l in lineas for m in re.findall(r"\b(?:RF|FU|TM|REF)-\d+\b", l)})
        print(f"{p.name}: {len(lineas)} líneas; ids citados en ellas: {ids[:12]}")
        print("   ej.:", RE_SECRETO.search(lineas[0] + '"').group(0)[:60])
print("líneas del corpus operativo que el filtro R8 toma por secreto:", total)
for texto in ("Fuente: https://johnhcochrane.com/research-all/the-risk-and-return-of-venture-capital",
              "La pregunta es si el risk-adjusted-return-of-the-portfolio mejora", "disk-encryption-at-rest-for-the-database"):
    print(repr(texto[:50]), "→ sensible" if contenido_sensible(texto) else "→ limpio")
