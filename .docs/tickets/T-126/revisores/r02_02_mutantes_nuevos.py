"""QA r02 de T-126 (revisor sin contexto): mutantes nuevos contra las pruebas de la r01 y la r02 (`test_t126_pb26_pb48.py` y
`test_t126_r02.py`), para las cláusulas que la r02 dice afirmar y que J1–J6 no tocaban.

- J7: F7, dos fichas contiguas con la misma Q y año distinto se intercambian (el desempate por fecha queda al revés).
- J8: F9, la última ficha de TF-01 se mueve dentro de la sección TF-02 (J4, pero en F9).
- J9: el ciclo deja de registrar la segunda pasada en F3 (sí llega a HT-03).
- J10: F8, un nivel A pasa a B con la misma Q (nivel incoherente en F8).

Uso:  python .docs/tickets/T-126/revisores/r02_02_mutantes_nuevos.py <copia desechable de bloque_a, con «_mut» en la ruta>
"""
import re
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "_mut" in str(COPIA) and (COPIA / "11_Ejecutor" / "bloque_a").is_dir()
OPER = COPIA / "05_Archivos_operativos"
F7 = next(OPER.glob("Documentación para el Analizador de Tendencias de Inversión - V*.md"))
F8 = next(OPER.glob("Documentación para el Motor de Cálculo Avanzado - V*.md"))
F9 = next(OPER.glob("Registro de Fuentes para el Analizador de Tendencias de Inversión - V*.md"))
ORQ = COPIA / "11_Ejecutor/bloque_a/orquestacion.py"
PRUEBAS = ["tests/test_t126_pb26_pb48.py", "tests/test_t126_r02.py"]
RE_FICHA = re.compile(r"^#### (\S+) · Q (\d+) \(([A-D])\)")


def bloques(texto):
    """(inicio, fin, id, q, año, sección) de cada ficha «#### ID · Q nn (N)» (fin = siguiente «## » o «#### »)."""
    lineas = texto.splitlines(keepends=True)
    out, seccion, actual = [], None, None
    for i, ln in enumerate(lineas):
        if ln.startswith("## ") or ln.startswith("#### "):
            if actual:
                out.append((*actual, i))
                actual = None
        m = re.match(r"^## (T[AMF]-\d{2})\b", ln)
        if m:
            seccion = m.group(1)
        m = RE_FICHA.match(ln)
        if m:
            actual = [i, m.group(1), int(m.group(2)), None, seccion]
        a = re.match(r"^- \*\*Año:\*\* ((?:19|20)\d{2})\b", ln)
        if a and actual:
            actual[3] = int(a.group(1))
    if actual:
        out.append((*actual, len(lineas)))
    return lineas, [(ini, fin, fid, q, anio, sec) for ini, fid, q, anio, sec, fin in out]


def intercambiar_empate(texto):
    lineas, bs = bloques(texto)
    for x, y in zip(bs, bs[1:]):
        if x[5] == y[5] and x[3] == y[3] and x[4] and y[4] and x[4] > y[4] and x[1] == y[0]:
            print(f"   J7: {x[2]} ({x[4]}) ↔ {y[2]} ({y[4]}), Q {x[3]}, {x[5]}")
            return "".join(lineas[:x[0]] + lineas[y[0]:y[1]] + lineas[x[0]:x[1]] + lineas[y[1]:])
    raise SystemExit("J7: no hay dos fichas contiguas empatadas con año")


def mover_ultima_de_tf01(texto):
    lineas, bs = bloques(texto)
    ini, fin = [b for b in bs if b[5] == "TF-01"][-1][:2]
    bloque, resto = lineas[ini:fin], lineas[:ini] + lineas[fin:]
    j = next(k for k, ln in enumerate(resto) if ln.startswith("## TF-02"))
    return "".join(resto[:j + 1] + ["\n"] + bloque + resto[j + 1:])


def nivel_a_b(texto):
    lineas = texto.splitlines(keepends=True)
    i = next(k for k, ln in enumerate(lineas) if RE_FICHA.match(ln) and " (A)" in ln)
    lineas[i] = lineas[i].replace(" (A)", " (B)", 1)
    return "".join(lineas)


MUTANTES = [
    ("J7", "F7: desempate por fecha al revés (dos fichas contiguas empatadas se intercambian)", F7, intercambiar_empate),
    ("J8", "F9: la última ficha de TF-01 queda dentro de la sección TF-02", F9, mover_ultima_de_tf01),
    ("J9", "el ciclo deja de registrar la segunda pasada en F3", ORQ,
     lambda t: t.replace('"dimensiones": f["dimensiones"], "segunda_pasada": f.get("segunda_pasada"), "saturacion_narrativa"',
                         '"dimensiones": f["dimensiones"], "segunda_pasada": None, "saturacion_narrativa"', 1)),
    ("J10", "F8: un nivel A pasa a B con la misma Q", F8, nivel_a_b),
]
for mid, que, ruta, cambio in MUTANTES:
    original = ruta.read_text(encoding="utf-8")
    mutado = cambio(original)
    assert mutado != original, f"{mid}: el mutante no cambia nada"
    ruta.write_text(mutado, encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *PRUEBAS], cwd=COPIA / "11_Ejecutor",
                           capture_output=True, text=True)
    finally:
        ruta.write_text(original, encoding="utf-8")
    assert r.returncode in (0, 1), r.stdout[-1500:] + r.stderr[-1500:]
    fallan = sorted({ln.split("::")[1].split(" ")[0] for ln in r.stdout.splitlines() if ln.startswith("FAILED")})
    print(f"{mid} | {que} | {'MUERTO · ' + r.stdout.strip().splitlines()[-1] + ' · ' + ', '.join(fallan) if r.returncode else 'VIVO'}", flush=True)
