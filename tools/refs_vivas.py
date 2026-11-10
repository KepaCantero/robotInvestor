#!/usr/bin/env python3
"""Refs vivas: toda ruta de archivo citada en NUESTROS documentos (CLAUDE.md,
prompts/, docs/) debe existir. Mecaniza la lección de robotTrading: los planes
por fases se ponen rancios — aquí un doc que cite algo inexistente falla el gate.

Solo comprueba rutas con formato de fichero (contienen / y una extensión) que
empiecen por las raíces conocidas del repo. El corpus canónico no se toca.

T-65 (QA de T-53, H-11): los informes de las carpetas `revisores/` de los tickets
se revisan como los demás documentos (antes quedaban todos fuera). Para que una
cita correcta no cuente como rota:
- una orden con argumentos (`.docs/scripts/gate.sh --completo`) se comprueba por
  su primera palabra, si es un script (.sh o .py);
- el sufijo de líneas (`archivo.py:10-20`) se quita;
- una ruta del paquete Python de un bloque (`bloque_a/orquestacion.py`, que vive en
  `bloque_a/11_Ejecutor/bloque_a/`) cuenta como viva.
La prueba está en `.docs/scripts/prueba_refs_vivas.py`.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RAICES_VALIDAS = ("bloque_a/", "bloque_a_forex/", "bloque_b/", "docs/", "prompts/", "tools/", "sistema_global/",
                  ".docs/", ".agents/", ".claude/", "AGENTS.md", "CLAUDE.md")
BLOQUES = ("bloque_a", "bloque_a_forex", "bloque_b")
PAT_RUTA = re.compile(r"`([^`\n]+?)`")
PAT_LINEAS = re.compile(r":\d+(?:-\d+)?$")


def documentos(raiz: Path) -> list[Path]:
    return ([raiz / "CLAUDE.md", raiz / "AGENTS.md"] + sorted((raiz / "prompts").glob("*.md"))
            + sorted((raiz / "docs").glob("*.md"))
            + sorted(p for p in (raiz / ".docs").rglob("*.md") if ".logs" not in p.parts)
            + sorted((raiz / ".agents" / "skills").rglob("*.md")))


def planificados(raiz: Path) -> set:
    """Entregables FUTUROS citados en prompts de fases (se quitan de la lista al aterrizar la fase que los crea — mismo
    ratchet que las cuotas)."""
    allow = raiz / "tools" / "refs_allowlist.txt"
    if not allow.exists():
        return set()
    return {l.split("#")[0].strip() for l in allow.read_text().splitlines() if l.split("#")[0].strip()}


def normalizar_cita(cita: str) -> str:
    """La ruta que nombra una cita, sin sufijo de líneas. Si es una orden con argumentos (la primera palabra es un script
    .sh o .py), la primera palabra; los nombres de archivo con espacios se conservan enteros."""
    r = cita.strip()
    partes = r.split()
    if len(partes) > 1 and partes[0].endswith((".sh", ".py")):
        r = partes[0]
    return PAT_LINEAS.sub("", r).strip("/")


def existe(raiz: Path, r: str) -> bool:
    if (raiz / r).exists():
        return True
    # Ruta de un paquete Python de bloque: `bloque_x/…` dentro de `bloque_x/11_Ejecutor/`
    primero = r.split("/", 1)[0]
    return primero in BLOQUES and (raiz / primero / "11_Ejecutor" / r).exists()


def comprobar(raiz: Path) -> list[str]:
    plan = planificados(raiz)
    rotas = []
    for doc in documentos(raiz):
        if not doc.exists():
            continue
        for m in PAT_RUTA.finditer(doc.read_text(encoding="utf-8")):
            bruta = m.group(1).strip()
            # Abreviaturas (…), placeholders (<bloque>, T-NN, AAAA-MM) y referencias a símbolos (::)
            # no son rutas verificables.
            if "…" in bruta or "<" in bruta or ">" in bruta or "::" in bruta or "T-NN" in bruta or "AAAA" in bruta:
                continue
            r = normalizar_cita(bruta)
            if not r.startswith(RAICES_VALIDAS):
                continue
            if r in plan or bruta.strip("/") in plan:
                continue
            if not existe(raiz, r):
                rotas.append(f"{doc.relative_to(raiz)} cita ruta inexistente: {r}")
    return rotas


def main() -> int:
    rotas = comprobar(RAIZ)
    if rotas:
        for r in rotas:
            print(f"  ROTA: {r}")
        print(f"FALLO: {len(rotas)} referencias a archivos que no existen (¿plan rancio?).")
        return 1
    print("Refs vivas: todas las rutas citadas en CLAUDE.md/prompts/docs existen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
