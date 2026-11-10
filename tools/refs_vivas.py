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
  su primera palabra, si es un script (.sh o .py), y por cada argumento que empiece
  por una raíz conocida (QA r01 de T-65, H-06);
- el sufijo de líneas (`archivo.py:10-20`) se quita;
- una ruta del paquete Python de un bloque (`bloque_a/orquestacion.py`, que vive en
  `bloque_a/11_Ejecutor/bloque_a/`) cuenta como viva.
QA r02 de T-65 (H-15), en una orden:
- un intérprete delante (`python3`, `bash`, `sh`, `.venv/bin/python`) se salta: se
  comprueba el script que ejecuta; las comillas de un argumento se quitan;
- un argumento con comodín (`*`, `?`, `[`) vale si casa con algún archivo (glob), y
  falla si no casa con ninguno;
- el argumento que sigue a una opción de salida (`-o`, `--salida`, `--output`, `--out`,
  también con `=`) es un archivo que la orden va a crear: no se comprueba.
Cualquier otro archivo que aún no existe y se cita a propósito (una salida futura
fuera de una orden, un entregable de una fase) va en `tools/refs_allowlist.txt`.
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
INTERPRETES = ("python", "python3", "bash", "sh", ".venv/bin/python", "../../.venv/bin/python")
OPCIONES_SALIDA = ("-o", "--salida", "--output", "--out")
COMODINES = ("*", "?", "[")


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


def rutas_de_cita(cita: str) -> list[str]:
    """Las rutas que nombra una cita, sin sufijo de líneas. Si es una orden con argumentos (la primera palabra es un script
    .sh o .py), el script y cada argumento con forma de ruta del repo; si no, la cita entera (los nombres de archivo con
    espacios se conservan enteros)."""
    r = cita.strip()
    partes = [x.strip("'\"") for x in r.split()]
    interprete = len(partes) > 1 and partes[0] in INTERPRETES
    if interprete:
        partes = partes[1:]
    if partes and partes[0].endswith((".sh", ".py")) and (len(partes) > 1 or interprete):
        candidatas = [partes[0]]
        salida = False
        for a in partes[1:]:
            if salida:                       # archivo que la orden va a crear
                salida = False
                continue
            if a in OPCIONES_SALIDA:
                salida = True
                continue
            if "=" in a and a.split("=", 1)[0] in OPCIONES_SALIDA:
                continue
            if PAT_LINEAS.sub("", a).strip("/").startswith(RAICES_VALIDAS):
                candidatas.append(a)
    elif interprete:
        candidatas = [partes[0]]
    else:
        candidatas = [r]
    return [PAT_LINEAS.sub("", c).strip("/") for c in candidatas]


def normalizar_cita(cita: str) -> str:
    """La ruta principal de una cita (la primera de `rutas_de_cita`)."""
    return rutas_de_cita(cita)[0]


def existe(raiz: Path, r: str) -> bool:
    if any(c in r for c in COMODINES):   # QA r02 de T-65, H-15: un comodín vale si casa con algún archivo
        return any(raiz.glob(r)) or (r.split("/", 1)[0] in BLOQUES and any((raiz / r.split("/", 1)[0] / "11_Ejecutor").glob(r)))
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
            for r in rutas_de_cita(bruta):
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
