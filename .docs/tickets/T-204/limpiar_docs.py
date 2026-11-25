"""T-204: quita de `.docs/` lo dedicado al Bloque A Forex (ampliación del operador del 25-11-2026: «Elimina el bloque A Forex
definitivamente»; «Haz esas tres cosas. Te doy mi consentimiento»).

Reglas (las mismas que `analisis-tecnico.md`, «.docs/»):
- una línea, fila o viñeta que habla solo del Forex se borra (`BORRAR`);
- en una frase mixta se quita solo el trozo del Forex (`REESCRIBIR`, en orden);
- la evidencia literal se conserva: órdenes dentro de bloques de código y de `…` (ruff con los tres ejecutores, PYTHONPATH,
  búsquedas), scripts y logs de `revisores/`; cambiarlas daría por ejecutado algo que no se ejecutó;
- r02 (QA r01, H-03): tampoco se tocan
  - una línea que lleve la marca T-204 (la huella deliberada del ticket, p. ej. la fila de `.docs/knowledge/01_…`);
  - una línea con resultados de un gate o de una suite (12/12, «12 de 12», ×3, «passed», cuotas o recuentos de mypy, pytest
    y ruff, «doce controles»): reescribirla daría un gate de dos bloques que nadie ejecutó;
  - las instrucciones de los encargos (`.docs/diseno/*/encargo_revision_astra*.md`);
  - la viñeta del A Forex en la lista de entregas de la historia, que cuenta «tres entregas»;
  - una frase cuya reescritura cambiaría una cita literal entre «…»;
  - r03 (QA r02, H-11): también la evidencia con «N/N», «N de N en verde», «pasadas» o «tres suites», «tres ejecutores» o
    «tres bloques»;
  - cierre de la QA r03 (H-14): mypy, pytest y ruff con cualquier mayúscula, y un recuento «A-Forex N, B N» o «FX N, B N»;
- `.docs/scripts/` y el propio ticket T-204 no se tocan aquí.
Uso: .venv/bin/python .docs/tickets/T-204/limpiar_docs.py [--aplicar]   (sin opciones, solo dice qué cambiaría)."""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
FUERA = (".docs/scripts/", ".docs/tickets/T-204/")
RE_MARCA = re.compile(r"(?<![\w-])T-204(?!\d)")
RE_EVIDENCIA = re.compile(r"\b\d+/12\b|\b\d+ de 12\b|\b\d+ pasan\b|×[23]|\bpassed\b|(?i:\bcuotas?\b)|(?i:\bmypy\b|\bpytest\b|\bruff\b)"
                          r"|(?i:\b(?:doce|12) controles\b)"
                          # r03 (QA r02, H-11): «8/8», «N de N en verde», «pasadas», «las tres suites/ejecutores/bloques»
                          r"|\b\d+/\d+\b|\b\d+ de \d+ en verde\b|\bpasadas\b|\btres (?:suites|ejecutores|bloques)\b"
                          # cierre de la QA r03 (H-14): «Pytest:»/«Mypy:» con mayúscula y un recuento «A-Forex 174, B 159»
                          # que sigue en otra línea a su «mypy»
                          r"|\b(?:A-Forex|FX) \d+, B \d+")
RE_ENCARGO = re.compile(r"\.docs/.+/encargo_revision_astra[^/]*\.md")   # instrucciones de un encargo, donde estén
F = r"A[- ]Forex"
BORRAR = [re.compile(p) for p in (
    r"\| `?bloque_a_forex/?(11_Ejecutor)?`? \|.*",
    r"\| `pytest -q bloque_a_forex/11_Ejecutor` \|.*",
    r"\| (Bloque )?A[- ]Forex, en el gate \|.*",
    r"\| pytest bloque_a_forex \|.*",
    r"\s*- A-Forex: 68;",
    r"\s*- mypy A-Forex 174( / 174)?;",
    r"\s*- (El|el) Bloque A Forex (queda para T-115\.|\(regla 8\): su réplica es T-115;)",
    r"- A-Forex;",
    r"\| `git diff --stat HEAD -- bloque_a_forex` \|.*",
    r"- El Bloque A Forex tiene su propia copia de `RE_SECRETO` y no se toca .*",
    r"- \*\*El Bloque A Forex\*\* es una prueba del Bloque A centrada solo en divisas\..*",
    r"- Tareas de protección o de integración del Forex \(por ejemplo T-115\) no se hacen sin orden\.",
)]
REESCRIBIR = [(re.compile(a), b) for a, b in (
    (r"A Forex y B Forex (fueron pruebas y )?quedan fuera", lambda m: "B Forex " + ("fue una prueba y " if m.group(1) else "") + "queda fuera"),
    (r"- pytest A-Forex y B: no se ejecutaron, porque no se tocaron\.", "- pytest B: no se ejecutó, porque no se tocó."),
    (r" · A-Forex \d+(?= ·)", ""), (r", A-Forex \d+ \(\d+\)", ""), (r"en A-Forex y en B", "en B"),
    (r"`bloque_a/11_Ejecutor/tests`, `bloque_a_forex/11_Ejecutor/tests` y ", "`bloque_a/11_Ejecutor/tests` y "),
    # Tablas con tres recuentos en orden A · A-Forex · B
    (r"\| Bloque A Forex y Bloque B \| 68 · 141 \| 68 · 141 \(no se tocan\) \|", "| Bloque B | 141 | 141 (no se toca) |"),
    (r"\| A-Forex y B \| 68 y 176 \| no se tocan ni se ejecutaron \|", "| B | 176 | no se toca ni se ejecuta |"),
    (r"\| A-Forex · B, en el gate \| 68 · 176 \| 68 · 176 \|", "| B, en el gate | 176 | 176 |"),
    (r"\| `bloque_a_forex`, `bloque_b` \| 68 y 174 \|", "| `bloque_b` | 174 |"),
    (r"\| (Bloques A, A Forex y B|pytest A · A-Forex · B(?: \(gate completo\))?) \| (\d+) · 68 · (\d+) \|", r"| \1 | \2 · \3 |"),
    (r"\| (\d+) · 68 · (\d+)( \([^)]*\))? \|", r"| \1 · \2\3 |"),
    (r"(mypy|pytest) bloque_a · bloque_a_forex · bloque_b \| ✓ \((\d+) · \d+ · (\d+)\)", r"\1 bloque_a · bloque_b | ✓ (\2 · \3)"),
    (r"(mypy|pytest) bloque_a · bloque_a_forex · bloque_b \| ✓ (\d+) · 68 · (\d+) passed", r"\1 bloque_a · bloque_b | ✓ \2 · \3 passed"),
    (r"\| mypy \(bloque_a, bloque_a_forex, bloque_b\) \|", "| mypy (bloque_a, bloque_b) |"),
    (r"\| Bloque A Forex, Bloque B \|", "| Bloque B |"), (r"\| Bloque A-Forex, Bloque B \|", "| Bloque B |"),
    (r"\| A-Forex, B \| sin tocar \| sin tocar", "| B | sin tocar | sin tocar"),
    (r"\| Bloques A, A-Forex, B \|", "| Bloques A, B |"),
    (r"\| Suites de A, A-Forex y B, `check_all.sh` \|", "| Suites de A y B, `check_all.sh` |"),
    (r"\| A-Forex 174/174, ", "| "), (r", A-Forex 174/174", ""),
    (r"\| pytest \| A ([\d.]+), A-Forex 68, B", r"| pytest | A \1, B"),
    # Recuentos y cuotas dentro de una frase
    (rf", {F} \*{{0,2}}\d[\d ]*\*{{0,2}}(?:/\d+| ≥ \d+)? y ", " y "),
    (rf", {F} \*{{0,2}}\d[\d ]*\*{{0,2}}(?:/\d+| ≥ \d+)?(?=[,;)\].]| \|)", ""),
    (r", FX \d+ y ", " y "), (r", FX \d+(?=[,;)])", ""), (r" · FX \d+(?= ·)", ""),
    (r"mypy (\d+) ?/ ?174 ?/ ?(\d+)", r"mypy \1/\2"), (r"\((\d+), 174, (\d+)\)", r"(\1, \2)"),
    (r"(\d+) · 174 · (\d+)", r"\1 · \2"), (r"ruff \(A \+ A-Forex \+ B, como el gate\)", "ruff (como el gate de entonces)"),
    (r", 68 de A Forex y 141 de B", " y 141 de B"), (r"\. A Forex: 68\. B:", ". B:"), (r", Forex 174, B", ", B"),
    (r"A 58, Forex 68, B 142", "A 58, B 142"), (r"; 58 de A y 68 de Forex", "; 58 de A"), (r", 58 de A y 68 de Forex", " y 58 de A"),
    (r"\(A 58, A Forex 68, B 141\)", "(A 58, B 141)"), (r", las 68 de Forex y las 174 del Bloque B", " y las 174 del Bloque B"),
    (r"A pasó 58 pruebas, Forex 68 y B", "A pasó 58 pruebas y B"),
    # Enumeraciones de bloques
    (r"(?i)los bloques A, A[- ]Forex y B", lambda m: m.group(0)[:-len("A, A-Forex y B")] + "A y B"),
    (r"A, A[- ]Forex y B", "A y B"), (r"A, A-Forex, B", "A, B"), (r"A \+ A-Forex \+ B", "A + B"),
    (r"los bloques A Forex y B \(un bloque por sesión; el Forex, además, no se integra: decisión del 13-11-2026\)",
     "el Bloque B (un bloque por sesión)"),
    (r"ni de A-Forex ni de B", "ni de B"), (r", A-Forex \d+ ≤ \d+", ""), (r"mypy FX \d+, ", ""), (r"`bloque_b/`, `bloque_a_forex/`,", "`bloque_b/`,"),
    (r" / FX \d+", ""), (r", FX \d+/\d+ y ", " y "), (r", mypy A-Forex \d+ > \d+", ""), (r"A, A-Forex ni B", "A ni B"),
    (r"ni de A-Forex ni de B", "ni de B"), (r"`bloque_a`, `bloque_a_forex` y `bloque_b`", "`bloque_a` y `bloque_b`"),
    (r"de A-Forex y de B", "de B"), (r"(?:las suites|la suite) de A-Forex y (?:(?:la )?de )?B", "la suite de B"),
    (r"ni A-Forex ni B", "ni B"), (r"A-Forex y B no se tocan", "B no se toca"), (r"A-Forex y B no tienen ninguna", "B no tiene ninguna"),
    (r"A-Forex y B: nada", "B: nada"), (r"A-Forex y B no cambian", "B no cambia"), (r"A-Forex y B dentro de cuota", "A y B dentro de cuota"),
    (r"A-Forex, B", "B"), (r"A-Forex y B", "B"), (r"A Forex y B", "B"), (r"Bloque A Forex y Bloque B", "Bloque B"),
    (r"A-Forex · B", "B"), (r"A, A-Forex y B", "A y B"),
    (r"`bloque_a/`, `bloque_a_forex/`, `bloque_b/`", "`bloque_a/`, `bloque_b/`"), (r"`bloque_a_forex/`, `bloque_b/`", "`bloque_b/`"),
    (r"`bloque_a_forex/` ni `bloque_b/`", "`bloque_b/`"), (r"`bloque_a`, `bloque_b`, `bloque_a_forex`,", "`bloque_a`, `bloque_b`,"),
    (r"`bloque_a`, `bloque_a_forex`, `bloque_b`", "`bloque_a`, `bloque_b`"), (r"`bloque_a_forex`, `bloque_b`", "`bloque_b`"),
    (r"`bloque_a/`, `bloque_a_forex/` ni `bloque_b/`", "`bloque_a/` ni `bloque_b/`"),
    # Frases sueltas
    (r" INC-002 \(A-Forex\) sigue abierta\.", ""), (r"; el Forex es solo una prueba con divisas \(T-115 aplazada\)", ""),
    (r" y otros dos en A-Forex", ""), (r", y A-Forex 1\.0\.0 con README «V1\.0, actualizado V1\.1»", ""),
    (r"; A-Forex 1\.0\.0 con README «V1\.0, actualizado V1\.1»", ""), (r"; A-Forex intacto", ""),
    (r"; T-115 \(Forex\) aplaz\w*", ""), (r"; los goldens del Bloque A Forex \(T-115\)", ""),
    (r" \(el Forex tiene su propia copia de `RE_SECRETO` y no se toca\)", ""),
    (r"; el Forex conserva el patrón antiguo", ""), (r" \*\*O-1\*\* el mismo patrón antiguo sigue en el Forex \(declarado en «No entra»\)\.", ""),
    (r"; el Bloque A Forex, que tiene el mismo patrón \(un bloque por tarea; además no se integra\)", ""),
    (r" Forex y B tienen sus propios patrones, sin cambios\.", " B tiene sus propios patrones, sin cambios."),
    (r"(T-104 \(Bloque A\) y T-105 \()A-Forex y B\)", r"\1B)"), (r"H-53 \(A-Forex y B, fila T-105\)", "H-53 (B, fila T-105)"),
    (r"T-105 es de A-Forex y B", "T-105 es de B"), (r"; mypy de A-Forex 174, sin tocar", ""),
    (r"; el Forex es solo una prueba con d[^|]*?(?= \|)", ""),
    (r"\*\*No entra:\*\* A-Forex \(INC-002\), que no es del Bloque A; ", "**No entra:** "),
    (r"No entra: A-Forex y B \(", "No entra: B ("),
    (r"etiquetas: \[bloque_a, documento_0, contratos, forex\]", "etiquetas: [bloque_a, documento_0, contratos]"),
    (r"No se dijo nada del Bloque B ni del Forex frente a sus Documentos 0\.", "No se dijo nada del Bloque B frente a su Documento 0."),
)]


def _documentos() -> list[Path]:
    return sorted(p for p in (RAIZ / ".docs").rglob("*") if p.is_file() and p.suffix in (".md", ".txt")
                  and not p.relative_to(RAIZ).as_posix().startswith(FUERA) and "revisores" not in p.parts
                  and ".logs" not in p.parts and not RE_ENCARGO.fullmatch(p.relative_to(RAIZ).as_posix()))


def limpiar(texto: str) -> tuple[str, list[str]]:
    salida, cambios, en_codigo = [], [], False
    for n, linea in enumerate(texto.split("\n"), 1):
        if linea.lstrip().startswith("```"):
            en_codigo = not en_codigo
        if en_codigo or not re.search(r"(?i)forex|\bFX \d", linea) or RE_MARCA.search(linea) or RE_EVIDENCIA.search(linea):
            salida.append(linea)
            continue
        if any(p.fullmatch(linea) for p in BORRAR):
            cambios.append(f"{n}: BORRADA: {linea}")
            continue
        nueva, borrar = linea, False
        for patron, sustituto in REESCRIBIR:
            if sustituto is None:
                if patron.search(nueva):
                    borrar = True
                continue
            # las órdenes literales entre `…` (las que llevan un espacio) se apartan y se reponen intactas
            partes, guardadas = nueva.split("`"), []
            for k in range(1, len(partes) - 1, 2):            # los trozos impares están entre `…` (si se cierran)
                if re.search(r"\s", partes[k]):
                    guardadas.append(partes[k])
                    partes[k] = f"\x00{len(guardadas) - 1}\x00"
            nueva = "`".join(partes)
            nueva = patron.sub(sustituto, nueva)
            for i, g in enumerate(guardadas):
                nueva = nueva.replace(f"\x00{i}\x00", g, 1)
        if borrar:
            cambios.append(f"{n}: BORRADA: {linea}")
            continue
        if re.findall(r"«[^»]*»", nueva) != re.findall(r"«[^»]*»", linea):   # una cita «…» literal no se recorta (r02)
            nueva = linea
        if nueva != linea:
            cambios.append(f"{n}: ANTES: {linea}\n{n}: AHORA: {nueva}")
        salida.append(nueva)
    return "\n".join(salida), cambios


def main() -> int:
    aplicar = "--aplicar" in sys.argv
    total = 0
    for doc in _documentos():
        texto = doc.read_text(encoding="utf-8")
        nuevo, cambios = limpiar(texto)
        if cambios:
            total += len(cambios)
            print(f"== {doc.relative_to(RAIZ)}")
            print("\n".join(cambios))
            if aplicar:
                doc.write_text(nuevo, encoding="utf-8")
    print(f"{total} líneas {'cambiadas' if aplicar else 'que cambiarían'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
