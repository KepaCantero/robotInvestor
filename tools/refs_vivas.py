#!/usr/bin/env python3
"""Refs vivas: toda ruta de archivo citada en NUESTROS documentos (CLAUDE.md,
prompts/, docs/) debe existir. Mecaniza la lección de robotTrading: los planes
por fases se ponen rancios — aquí un doc que cite algo inexistente falla el gate.

Solo comprueba rutas con formato de fichero (contienen / y una extensión) que
empiecen por las raíces conocidas del repo. El corpus canónico no se toca.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOCS_NUESTROS = ([RAIZ / "CLAUDE.md", RAIZ / "AGENTS.md"] + sorted((RAIZ / "prompts").glob("*.md"))
                 + sorted((RAIZ / "docs").glob("*.md")) + sorted((RAIZ / ".docs").rglob("*.md"))
                 + sorted((RAIZ / ".agents" / "skills").rglob("*.md")))
RAICES_VALIDAS = ("bloque_a/", "bloque_a_forex/", "bloque_b/", "docs/", "prompts/", "tools/", "sistema_global/",
                  ".docs/", ".agents/", ".claude/", "AGENTS.md", "CLAUDE.md")
PAT_RUTA = re.compile(r"`([^`\n]+?)`")
# Entregables FUTUROS citados en prompts de fases (se quitan de aquí al aterrizar
# la fase que los crea — mismo ratchet que las cuotas).
_allow = Path(__file__).parent / "refs_allowlist.txt"
PLANIFICADOS = set()
if _allow.exists():
    PLANIFICADOS = {l.split("#")[0].strip() for l in _allow.read_text().splitlines()
                    if l.split("#")[0].strip()}


def main() -> int:
    rotas = []
    for doc in DOCS_NUESTROS:
        if not doc.exists():
            continue
        for m in PAT_RUTA.finditer(doc.read_text(encoding="utf-8")):
            r = m.group(1).strip().strip("/")
            # Abreviaturas (…), placeholders (<bloque>, T-NN, AAAA-MM) y referencias a símbolos (::)
            # no son rutas verificables.
            if "…" in r or "<" in r or ">" in r or "::" in r or "T-NN" in r or "AAAA" in r:
                continue
            if not r.startswith(RAICES_VALIDAS):
                continue
            if r in PLANIFICADOS:
                continue
            if not (RAIZ / r).exists():
                rotas.append(f"{doc.relative_to(RAIZ)} cita ruta inexistente: {r}")
    if rotas:
        for r in rotas:
            print(f"  ROTA: {r}")
        print(f"FALLO: {len(rotas)} referencias a archivos que no existen (¿plan rancio?).")
        return 1
    print("Refs vivas: todas las rutas citadas en CLAUDE.md/prompts/docs existen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
