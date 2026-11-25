"""QA r03 de T-204 (copia corregida de r02_01: en la r02 la etiqueta del fichero se cambiaba antes de revisar el último
trozo del fichero anterior, así que cada caso salía con el nombre del fichero siguiente). Revisa la limpieza de `.docs/` ya aplicada (commit ba651950) a partir de su diff.
Para cada línea quitada o cambiada en `.docs/` comprueba que:
- no lleva la marca T-204 ni es de un encargo a Astra (`encargo_revision_astra*`);
- no es evidencia medida (N/N, «N de N en verde», «pasadas», 12/12, «12 de 12», ×3, «passed», cuotas, recuentos de mypy, pytest o ruff, «doce controles»);
- no cambia ninguna cita «…» ni ninguna orden entre `…` con espacios, ni nada dentro de un bloque de código;
- lo que quita nombra el Forex (nunca solo A o B), y lo que queda no sigue contando «tres» ni rompe la concordancia.
Uso (desde la raíz): python3 -I r03_01_limpieza_aplicada.py [antes] [después]   (por defecto 253f33fd y ba651950)."""
import difflib
import re
import subprocess
import sys

antes, despues = (sys.argv[1:3] + ["253f33fd", "ba651950"][len(sys.argv[1:3]):])
diff = subprocess.run(["git", "-c", "core.quotepath=off", "diff", "-U0", antes, despues, "--", ".docs",
                       ":!.docs/scripts", ":!.docs/tickets/T-204"], capture_output=True, text=True, check=True).stdout
EVID = re.compile(r"\b\d+/\d+\b|\d+ de \d+ en verde|12 de 12|×3|pasadas|\bpassed\b|cuota|\bmypy\b[^.]*\d|\bpytest\b[^.]*\d|\bruff\b[^.]*\d|doce controles")
COM = re.compile(r"«[^»]*»")


def ordenes(t):
    """Los trozos entre `…` (impares al partir por la comilla) que llevan un espacio: órdenes literales."""
    p = t.split("`")
    return [p[k] for k in range(1, len(p) - 1, 2) if re.search(r"\s", p[k])]

casos, fich, menos, mas, n = [], None, [], [], 0


def revisar():
    global n
    for i, a in enumerate(menos):
        n += 1
        b = mas[i] if i < len(mas) and len(mas) == len(menos) else None
        if "T-204" in a:
            casos.append(f"{fich}: toca una línea con T-204: {a[:150]}")
        if "encargo_revision_astra" in fich:
            casos.append(f"{fich}: toca un encargo a Astra: {a[:150]}")
        if a.lstrip().startswith("```"):
            casos.append(f"{fich}: toca una valla de código: {a[:150]}")
        if b is None:
            quitado = a
        else:                                    # por palabras: en líneas largas, por caracteres el alineado se pierde
            pa, pb = a.split(" "), b.split(" ")
            quitado = " ".join(" ".join(pa[i1:i2]) for op, i1, i2, _, _ in
                               difflib.SequenceMatcher(None, pa, pb, autojunk=False).get_opcodes() if op in ("delete", "replace"))
        if EVID.search(a) and (b is None or EVID.findall(a) != EVID.findall(b)):
            casos.append(f"{fich}: cambia evidencia medida: {a[:200]}")
        if b is not None and COM.findall(a) != COM.findall(b):
            casos.append(f"{fich}: cambia una cita «…»: {a[:200]}")
        if b is not None and ordenes(a) != ordenes(b):
            casos.append(f"{fich}: cambia una orden entre `…`: {a[:200]}")
        if b is not None and re.search(r"\btres (suites|ejecutores|bloques)\b", b):
            casos.append(f"{fich}: la línea nueva sigue contando tres: {b[:200]}")
        if b is not None and re.search(r"suite de B no se tocan", b):
            casos.append(f"{fich}: concordancia rota: {b[:200]}")
        if not re.search(r"(?i)forex|\bfx\b", quitado):
            casos.append(f"{fich}: quita texto sin el Forex: {quitado[:120]!r} en {a[:150]}")
    if len(mas) > len(menos):
        casos.append(f"{fich}: añade líneas: {mas[len(menos):]}")


for l in diff.split("\n") + ["@@ fin"]:   # split("\n"): una línea con U+2028 (T-103) no se parte
    if l.startswith("+++ b/"):
        if menos or mas:                     # el último trozo del fichero anterior, con su nombre
            revisar()
        menos, mas = [], []
        fich = l[6:]
    elif l.startswith("@@"):
        if menos or mas:
            revisar()
        menos, mas = [], []
    elif l.startswith("-") and not l.startswith("---"):
        menos.append(l[1:])
    elif l.startswith("+") and not l.startswith("+++"):
        mas.append(l[1:])
print(f"{n} líneas revisadas; {len(casos)} casos")
for c in casos:
    print("  " + c)
sys.exit(1 if casos else 0)
