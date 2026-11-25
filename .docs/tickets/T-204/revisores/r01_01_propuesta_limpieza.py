"""QA r01 de T-204: revisa la propuesta de limpieza de `.docs/` (limpiar_docs.py) sin aplicarla.
Para cada línea que cambiaría, comprueba:
- que no cambian las citas entre «…» (órdenes y palabras literales) ni los trozos entre `…` (órdenes);
- que lo que se quita no nombra A ni B (bloque_a/, bloque_b/, «Bloque A», «Bloque B», «A 58», «B 174»…), salvo
  que el trozo quitado también nombre el Forex;
- que no borra ni reescribe líneas marcadas con T-204 (la huella deliberada del ticket).
Uso: python3 -I r01_01_propuesta_limpieza.py <salida de limpiar_docs.py>. Sale con 1 si hay casos que revisar."""
import difflib
import re
import sys

txt = open(sys.argv[1], encoding="utf-8").read().split("\n")
doc, casos, n = None, [], 0
RE_COMILLAS, RE_COD = re.compile(r"«[^»]*»"), re.compile(r"`[^`]*`")
RE_AB = re.compile(r"bloque_a/|bloque_b|Bloque A(?! Forex)|Bloque B|\bA \d|\bB \d|\bB:|\bA:")
i = 0
while i < len(txt):
    l = txt[i]
    if l.startswith("== "):
        doc = l[3:]
    elif ": BORRADA: " in l:
        n += 1
        cuerpo = l.split(": BORRADA: ", 1)[1]
        if "T-204" in cuerpo:
            casos.append(f"{doc}: borra una línea marcada con T-204: {cuerpo[:160]}")
        if RE_COMILLAS.search(cuerpo):
            casos.append(f"{doc}: borra una línea con cita literal «…»: {cuerpo[:160]}")
    elif ": ANTES: " in l and i + 1 < len(txt) and ": AHORA: " in txt[i + 1]:
        n += 1
        a, b = l.split(": ANTES: ", 1)[1], txt[i + 1].split(": AHORA: ", 1)[1]
        if "T-204" in a:
            casos.append(f"{doc}: reescribe una línea marcada con T-204: {a[:160]}")
        if RE_COMILLAS.findall(a) != RE_COMILLAS.findall(b):
            casos.append(f"{doc}: cambia una cita «…»: {a[:200]}")
        if RE_COD.findall(a) != RE_COD.findall(b):
            quit_ = [x for x in RE_COD.findall(a) if x not in RE_COD.findall(b)]
            if any(" " in x for x in quit_):
                casos.append(f"{doc}: cambia una orden entre `…`: {quit_}")
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        for op, i1, i2, _, _ in sm.get_opcodes():
            if op in ("delete", "replace"):
                quitado = a[i1:i2]
                if RE_AB.search(quitado) and not re.search(r"(?i)forex|FX", quitado):
                    casos.append(f"{doc}: quita texto de A o B sin Forex: «{quitado}» en: {a[:160]}")
        i += 1
    i += 1
print(f"{n} cambios revisados; {len(casos)} casos")
for c in casos:
    print("  " + c)
sys.exit(1 if casos else 0)
