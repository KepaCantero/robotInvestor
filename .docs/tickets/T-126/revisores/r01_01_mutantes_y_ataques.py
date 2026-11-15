"""QA r01 de T-126 (revisor sin contexto): ¿las pruebas de PB-26 y PB-48 afirman lo que dicen?

Uso:  python .docs/tickets/T-126/revisores/r01_01_mutantes_y_ataques.py <copia desechable de bloque_a, con «_mut» en la ruta>
1) Mutantes sobre F7 (en la copia) y sobre el ejecutor, contra `tests/test_t126_pb26_pb48.py`.
2) Ataque: en el ciclo de `test_pb48_una_guia_…`, ¿alguna entrada de HT-03 está en banda marginal? (si no, el paso 2 del
   plan, «una selección con opción en banda marginal», no se ejerce).
"""
import re
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "_mut" in str(COPIA) and (COPIA / "11_Ejecutor" / "bloque_a").is_dir()
F7 = next((COPIA / "05_Archivos_operativos").glob("Documentación para el Analizador de Tendencias de Inversión - V*.md"))
PRUEBAS = ["tests/test_t126_pb26_pb48.py"]


def bloques(texto):
    """Fichas «#### ID · Q nn (N) — …» con su sección «## TX-nn»: lista de (inicio, fin, id, seccion)."""
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
        m = re.match(r"^#### (\S+) · Q", ln)
        if m:
            actual = (i, m.group(1), seccion)
    return lineas, [(a, f, i, s) for a, i, s, f in out]


def mover_ultima_de_ta01_al_principio_de_ta02(texto):
    lineas, bs = bloques(texto)
    ta01 = [b for b in bs if b[3] == "TA-01"]
    ini, fin, _, _ = ta01[-1]
    bloque = lineas[ini:fin]
    resto = lineas[:ini] + lineas[fin:]
    j = next(k for k, ln in enumerate(resto) if ln.startswith("## TA-02"))
    return "".join(resto[:j + 1] + ["\n"] + bloque + resto[j + 1:])


def tematica_inventada(texto):
    i = texto.index("#### ANA-DOC-0061 ")
    j = texto.index("- **Temática:** TA-01", i)
    return texto[:j] + "- **Temática:** TA-99" + texto[j + len("- **Temática:** TA-01"):]


ORQ = "11_Ejecutor/bloque_a/orquestacion.py"
HT03 = "11_Ejecutor/bloque_a/herramientas/referencia/ht03_puntuaciones.py"
MUTANTES = [
    ("J1", "F7: una ficha sube de Q y rompe el orden de su temática", F7,
     lambda t: t.replace("#### ANA-DOC-0039 · Q 92 (A)", "#### ANA-DOC-0039 · Q 96 (A)", 1)),
    ("J2", "F7: nivel incoherente con Q", F7, lambda t: t.replace("#### ANA-DOC-0061 · Q 95 (A)", "#### ANA-DOC-0061 · Q 95 (B)", 1)),
    ("J3", "F7: temática que no está en el Anexo D", F7, tematica_inventada),
    ("J4", "F7: una ficha de TA-01 queda dentro de la sección TA-02 (su campo sigue diciendo TA-01)", F7,
     mover_ultima_de_ta01_al_principio_de_ta02),
    ("J5", "HT-03 no recibe nunca la segunda pasada del Analista (el ciclo la omite)", COPIA / ORQ,
     lambda t: t.replace('"dimensiones": f["dimensiones"], "segunda_pasada": f.get("segunda_pasada") or {},\n                                  "anterior"',
                         '"dimensiones": f["dimensiones"], "segunda_pasada": {},\n                                  "anterior"', 1)),
    ("J6", "control: HT-03 ignora la banda marginal (PS8)", COPIA / HT03,
     lambda t: t.replace('    for bm in res["banda_marginal"]:\n        if not bm.get("resuelta"):',
                         '    for bm in res["banda_marginal"]:\n        if False:', 1)),
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
    print(f"{mid} | {que} | {'MUERTO · ' + r.stdout.strip().splitlines()[-1] if r.returncode else 'VIVO'}", flush=True)

# 2) ¿hay banda marginal en el ciclo de la prueba de PB-48?
codigo = r'''
import sys; sys.path.insert(0, "tests")
import tempfile
from pathlib import Path
from conftest import AS_OF, RUTA_UNIVERSO_EJEMPLO, cargar_universo, nuevo_bloque
from bloque_a.herramientas import ht03
import test_t126_pb26_pb48 as t
b = nuevo_bloque(Path(tempfile.mkdtemp(dir=sys.argv[1])), cargar_universo(RUTA_UNIVERSO_EJEMPLO))
b.fijar_fecha(AS_OF)
t._lecciones_que_relajan(b)
res = []
orig = ht03.evaluar_opcion
def anotar(op, *a, **k):
    r = orig(op, *a, **k)
    res.append((op["opp_id"], bool(op.get("segunda_pasada")), [m["codigo"] for m in r["motivos_no_elegible"]], len(r.get("banda_marginal") or [])))
    return r
ht03.evaluar_opcion = anotar
b.ciclo(AS_OF, alcance={"clases": ["RV"]})
marg = [x for x in res if "PS8_BANDA_MARGINAL" in x[2]]
print("entradas HT-03:", len(res), "· con segunda pasada:", sum(1 for x in res if x[1]), "· con algún total en banda marginal:",
      sum(1 for x in res if x[3]), "· en banda marginal sin resolver:", len(marg))
'''
r = subprocess.run([sys.executable, "-c", codigo, str(COPIA.parent)], cwd=COPIA / "11_Ejecutor", capture_output=True, text=True)
print("A1 banda marginal en el ciclo de PB-48 |", (r.stdout or r.stderr).strip().splitlines()[-1])
