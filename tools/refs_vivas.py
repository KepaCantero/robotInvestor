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
- un intérprete delante (`python3`, `bash`, `sh`, `.venv/bin/python`) se salta, con
  sus opciones (`-I`, `-u`, `-X valor`…; QA r03 de T-65, H-22): se comprueba el script
  que ejecuta; la orden se parte con `shlex`, así que un argumento entre comillas con
  espacios es uno solo;
- un argumento con comodín (`*`, `?`, `[`) vale si casa con algún archivo (glob), y
  falla si no casa con ninguno;
- el argumento que sigue a una opción de salida (`-o`, `--salida`, `--output`, `--out`,
  también con `=`) es un archivo que la orden va a crear: no se comprueba.
Cualquier otro archivo que aún no existe y se cita a propósito (una salida futura
fuera de una orden, un entregable de una fase) va en `tools/refs_allowlist.txt`.
T-204 (orden del operador del 25-11-2026): un bloque eliminado del repositorio (`RETIRADOS`)
no vuelve a la lista de permitidas. Una cita suya (también la carpeta sola, o abreviada
con «…») es una ruta muerta salvo en dos casos:
- en los registros de `.docs/` (tickets, diario, memoria y diseño), que no se reescriben
  (regla 1 de `.docs/README.md`);
- en una línea que la marca con el ticket que retiró el bloque (p. ej. «eliminado el
  25-11-2026, T-204»).
La prueba está en `.docs/scripts/prueba_refs_vivas.py`.
"""
import re
import shlex
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RAICES_VALIDAS = ("bloque_a/", "bloque_b/", "docs/", "prompts/", "tools/", "sistema_global/",
                  ".docs/", ".agents/", ".claude/", "AGENTS.md", "CLAUDE.md")
BLOQUES = ("bloque_a", "bloque_b")
# Bloques eliminados del repositorio → el ticket que los retiró, que es también la marca que acepta una cita suya.
RETIRADOS = {"bloque_a_forex": "T-204"}
# Registros de .docs/ que no se reescriben: una cita a un bloque retirado se queda como estaba.
REGISTROS = (".docs/tickets/", ".docs/diario/", ".docs/memoria/", ".docs/diseno/")
PAT_RUTA = re.compile(r"`([^`\n]+?)`")
PAT_LINEAS = re.compile(r":\d+(?:-\d+)?$")
# Intérpretes (con o sin ruta y versión: python3, python3.12, .venv/bin/python3, bash, sh) y lanzadores de pruebas
RE_INTERPRETE = re.compile(r"(?:[\w./-]*/)?(?:python(?:\d+(?:\.\d+)?)?|bash|sh)")
RE_LANZADOR = re.compile(r"(?:[\w./-]*/)?pytest")
OPCIONES_SALIDA = ("-o", "--salida", "--output", "--out")
COMODINES = ("*", "?", "[")
OPCIONES_CON_VALOR = ("-X", "-W")
RE_ASIGNACION = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")


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


def _args_con_ruta(args: list[str]) -> list[str]:
    """Argumentos con forma de ruta del repo, sin el archivo que sigue a una opción de salida (lo crea la orden)."""
    out, salida = [], False
    for a in args:
        if salida:
            salida = False
            continue
        if a in OPCIONES_SALIDA:
            salida = True
            continue
        if "=" in a and a.split("=", 1)[0] in OPCIONES_SALIDA:
            continue
        if PAT_LINEAS.sub("", a).strip("/").startswith(RAICES_VALIDAS):
            out.append(a)
    return out


def rutas_de_cita(cita: str) -> list[str]:
    """Las rutas que nombra una cita, sin sufijo de líneas. Si es una orden (un script .sh o .py con argumentos, o un
    intérprete con sus opciones), el script y cada argumento con forma de ruta del repo; si no, la cita entera (los nombres
    de archivo con espacios se conservan enteros)."""
    r = cita.strip()
    try:
        partes = shlex.split(r)
    except ValueError:                       # comillas sin cerrar: se parte por espacios
        partes = [x.strip("'\"") for x in r.split()]
    if len(partes) > 1 and RE_LANZADOR.fullmatch(partes[0]):   # pytest: todos sus argumentos con forma de ruta
        return [PAT_LINEAS.sub("", c).strip("/") for c in _args_con_ruta(partes[1:])]
    interprete = len(partes) > 1 and bool(RE_INTERPRETE.fullmatch(partes[0]))
    if interprete:
        partes = partes[1:]
        while partes and partes[0].startswith("-") and partes[0] not in ("-m", "-c"):   # opciones del intérprete
            partes = partes[2:] if partes[0] in OPCIONES_CON_VALOR else partes[1:]
        if partes and partes[0] == "-c":     # código en línea: nada que comprobar
            return []
        if partes and partes[0] == "-m":     # un módulo: solo sus argumentos con forma de ruta
            candidatas = _args_con_ruta(partes[2:])
        else:
            candidatas = partes[:1] + _args_con_ruta(partes[1:])
    elif len(partes) > 1 and partes[0].endswith((".sh", ".py")):
        candidatas = [partes[0]] + _args_con_ruta(partes[1:])
    else:
        candidatas = [r]
    return [PAT_LINEAS.sub("", c).strip("/") for c in candidatas]


def normalizar_cita(cita: str) -> str:
    """La ruta principal de una cita (la primera de `rutas_de_cita`; la cita entera si no nombra ninguna)."""
    rutas = rutas_de_cita(cita)
    return rutas[0] if rutas else cita.strip()


def existe(raiz: Path, r: str) -> bool:
    if ".." in Path(r).parts:            # nunca fuera del repositorio
        return False
    if (raiz / r).exists():              # también un nombre con corchetes literales
        return True
    if any(c in r for c in COMODINES):   # QA r02 de T-65, H-15: un comodín vale si casa con algún archivo
        return any(raiz.glob(r)) or (r.split("/", 1)[0] in BLOQUES and any((raiz / r.split("/", 1)[0] / "11_Ejecutor").glob(r)))
    if (raiz / r).exists():
        return True
    # Ruta de un paquete Python de bloque: `bloque_x/…` dentro de `bloque_x/11_Ejecutor/`
    primero = r.split("/", 1)[0]
    return primero in BLOQUES and (raiz / primero / "11_Ejecutor" / r).exists()


def marcada(linea: str, marca: str) -> bool:
    """La línea lleva la marca como palabra: «T-204», no «T-2040» ni «XT-204» (QA r01 de T-204, H-06)."""
    return re.search(rf"(?<![\w-]){re.escape(marca)}(?!\d)", linea) is not None


def bloque_retirado(cita: str) -> str | None:
    """El bloque retirado que nombra una cita, o None: la cita entera o cualquiera de sus palabras (una orden con
    argumentos, `--opcion=ruta`), con o sin `./`, comillas o sufijo de líneas."""
    try:
        partes = shlex.split(cita)
    except ValueError:                       # comillas sin cerrar: se parte por espacios
        partes = cita.split()
    for r in [cita.strip()] + partes:
        r = r.strip().strip("'\"")
        # `--opcion=ruta` o `NOMBRE=ruta` (una asignación de entorno): la ruta es lo que sigue al «=» (QA r01 y r02 de T-204,
        # H-06 y H-12); un nombre de archivo con «=» (`bloque_a_forex/a=b.md`) no se parte
        if r.startswith("-") or RE_ASIGNACION.match(r):
            r = r.split("=", 1)[-1]
        r = PAT_LINEAS.sub("", r)
        primero = r.removeprefix("./").split("/", 1)[0]
        if primero in RETIRADOS:
            return primero
    return None


def comprobar(raiz: Path) -> list[str]:
    plan = planificados(raiz)
    rotas = []
    for doc in documentos(raiz):
        if not doc.exists():
            continue
        rel = doc.relative_to(raiz).as_posix()
        texto = doc.read_text(encoding="utf-8")
        for m in PAT_RUTA.finditer(texto):
            bruta = m.group(1).strip()
            retirado = bloque_retirado(bruta)
            if retirado is not None:          # T-204: antes que cualquier otro filtro (también «…» o una carpeta sola)
                fin = texto.find("\n", m.end())
                linea = texto[texto.rfind("\n", 0, m.start()) + 1:fin if fin != -1 else len(texto)]
                if not rel.startswith(REGISTROS) and not marcada(linea, RETIRADOS[retirado]):
                    rotas.append(f"{rel} cita el bloque retirado {retirado} ({RETIRADOS[retirado]}) sin marcarlo: {bruta}")
            # Las demás rutas de la cita se comprueban como siempre; las del bloque retirado ya no son de una raíz válida.
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
