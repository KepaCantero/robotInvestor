"""QA r01 de T-157 · recuento independiente de las cifras del informe del verificador de IDs.

Cuenta con código propio (sin importar el verificador) las fichas del Catálogo y sus clases, los CT de §6.1 frente a
`CANALES`, las reglas de §1, las puertas de §9.3, el mapa F → archivo por el H1, las citas de CT/R/F/PS fuera de rango,
las menciones a otra versión del Catálogo (con un patrón más ancho que el del verificador) y las referencias de (e), y lo
compara con el JSON que se le pasa. Sale 0 si todo cuadra, 1 si algo difiere.

Uso (desde bloque_a/11_Ejecutor):
    ../../.venv/bin/python ../../.docs/tickets/T-157/revisores/r01_01_cifras.py <informe.json>
"""
import json
import re
import sys
from pathlib import Path

EJ = Path.cwd()
sys.path.insert(0, str(EJ))
RAIZ = EJ.parent
from bloque_a import contratos  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

informe = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
fallos: list[str] = []


def igual(que, mio, suyo):
    estado = "OK " if mio == suyo else "MAL"
    if mio != suyo:
        fallos.append(que)
    print(f"[{estado}] {que}: mío={mio!r} informe={suyo!r}")


def corpus():
    for p in sorted(RAIZ.rglob("*.md")):
        partes = p.relative_to(RAIZ).parts
        if partes[0] == "11_Ejecutor" or any(x.startswith("99_Historico") for x in partes):
            continue
        yield p.relative_to(RAIZ).as_posix(), p.read_text(encoding="utf-8")


DOCS = dict(corpus())
doc0 = [k for k in DOCS if k.startswith("01_Gobernanza/Documento 0")]
assert len(doc0) == 1, doc0
D0 = DOCS[doc0[0]]
cat = [k for k in DOCS if k.startswith("04_Motor_conocimiento_y_catalogo/Catálogo de cálculos")]
assert len(cat) == 1
CAT = DOCS[cat[0]]


def seccion(texto, inicio, fin):
    a = texto.index(inicio)
    b = texto.index(fin, a + 1)
    return texto[a:b]


# ---- fichas
cab = re.findall(r"^### (\S+) · ", CAT, re.M)
igual("encabezados ### ID", len(cab), informe["fichas"]["encabezados"])
s4 = seccion(CAT, "\n## 4. ", "\n## 5. ")
indice = {}
for linea in s4.splitlines():
    c = [x.strip() for x in linea.strip().strip("|").split("|")]
    if len(c) == 7 and re.fullmatch(r"[A-Z0-9-]+-\d{3}", c[0]):
        indice[c[0]] = c[6]
igual("filas del índice §4", len(indice), informe["fichas"]["en_indice"])
igual("mismo conjunto índice/encabezados", sorted(indice), sorted(set(cab)))
cod = set(servicio.FICHAS_CATALOGO)
man = set(servicio.IMPLEMENTADAS) | set(servicio.SERVICIOS_CT10)
clases = {"IMPLEMENTADO": 0, "SOLO_CATALOGO": 0, "SOLO_CODIGO": 0, "ID_DISTINTO": 0}
for f in set(cab):
    clases["IMPLEMENTADO" if f in man else "SOLO_CATALOGO"] += 1
clases["SOLO_CODIGO"] = len((cod | man) - set(cab))   # sin emparejar: si hubiera, serían SOLO_CODIGO o ID_DISTINTO
igual("clases de fichas", clases, informe["fichas"]["conteo_clases"])
igual("madurez citable en las 81", sum(v.startswith(("IMPLEMENTADO", "VALIDADO")) for v in indice.values()), len(indice))
total = re.search(r"^Total: (\d+) fichas", CAT, re.M)
igual("Total declarado", int(total.group(1)) if total else None, informe["fichas"]["total_declarado"])
nuevas = 0
seccion_actual = ""
for linea in CAT.splitlines():
    if linea.startswith("## "):
        seccion_actual = linea
    elif re.match(r"^### \S+ · ", linea) and "V5.0" in seccion_actual:
        nuevas += 1
igual("fichas en secciones V5.0", nuevas, informe["fichas"]["nuevas_en_version"])

# ---- CT
s61 = seccion(D0, "\n### 6.1 ", "\n### 6.2 ")
ct = re.findall(r"^\| (CT-\d+) \|", s61, re.M)
igual("CT en §6.1", len(ct), len(informe["contratos"]["definidos_doc0"]))
igual("CT en CANALES", len(contratos.CANALES), len(informe["contratos"]["definidos_codigo"]))
igual("§6.1 == CANALES", sorted(ct), sorted(contratos.CANALES))
citas_ct = {m for t in DOCS.values() for m in re.findall(r"(?<![\w-])CT-\d+(?![\w-])", t)}
igual("CT citados fuera de §6.1", sorted(citas_ct - set(ct)), [])
# CT con letra (otros bloques) citados: informativo
print("     CT de otros bloques citados:", sorted({m for t in DOCS.values() for m in re.findall(r"(?<![\w-])CT-[A-Z]+-\d+", t)})[:10])

# ---- R
s1 = seccion(D0, "\n## 1. ", "\n## 2. ")
r = re.findall(r"^\| (R\d+) \|", s1, re.M)
igual("R en §1", r, [f"R{i}" for i in range(1, 28)])
citas_r = {}
for k, t in DOCS.items():
    for n, linea in enumerate(t.splitlines(), 1):
        for m in re.findall(r"(?<![\w-])R(\d+)(?![\w-])", linea):
            if int(m) > 27 or int(m) == 0:
                citas_r.setdefault(f"R{m}", []).append((k[:60], n))
print("     R fuera de R1–R27 citadas (mío):", {k: v[:3] for k, v in citas_r.items()})

# ---- PS
s93 = seccion(D0, "\n### 9.3 ", "\n### 9.4 ")
ps = re.findall(r"^\| (PS\d+) ", s93, re.M)
igual("PS en §9.3", ps, informe["puertas"]["definidas"])
citas_ps = {m for t in DOCS.values() for m in re.findall(r"(?<![\w-])PS\d+(?![\w-])", t)}
igual("PS citadas fuera de §9.3", sorted(citas_ps - set(ps)), [])

# ---- F: mapa por H1
s51 = seccion(D0, "\n### 5.1 ", "\n### 5.2 ")
inv = re.findall(r"^\| ([A-Z]+\d*) \| ", s51, re.M)
inv = [x for x in inv if x != "Código"]
mapa = {}
for k, t in DOCS.items():
    if k.startswith("05_Archivos_operativos/"):
        h1 = next(x for x in t.splitlines() if x.startswith("# "))
        # dos formas de H1: «Archivo operativo F7 — Nombre» y «Esquema de archivo operativo — F1 Nombre»
        m = (re.match(r"# Archivo operativo ([A-Z]+\d*) — ", h1)
             or re.match(r"# Esquema de archivo operativo — ([A-Z]+\d*) ", h1))
        assert m, h1
        mapa[m.group(1)] = k
suyo = {f["codigo"]: f["archivo"] for f in informe["archivos"]["mapa"]}
igual("mapa F → archivo por H1", {k: mapa.get(k) for k in inv}, {k: suyo.get(k) for k in inv})
igual("F1–F11 todos con archivo", sorted([k for k in inv if re.fullmatch(r"F\d+", k) and k in mapa], key=lambda x: int(x[1:])),
      [f"F{i}" for i in range(1, 12)])

# ---- menciones a otra versión del Catálogo (patrón ancho, sin distinguir mayúsculas)
anchas = []
for k, t in DOCS.items():
    for n, linea in enumerate(t.splitlines(), 1):
        if re.search(r"cat[aá]logo[^|\n]{0,40}?\bV?4\.0\b|catalog_version\W{0,6}4\.0", linea, re.I):
            anchas.append((k, n))
suyas = [(u["archivo"], u["linea"]) for h in informe["hallazgos"] if h["codigo"] == "MENCION_OTRA_VERSION"
         for u in h["ubicaciones"]]
igual("menciones a V4.0 del Catálogo (patrón ancho)", sorted(anchas), sorted(suyas))

# ---- referencias de (e)
definidas = set()
for k, t in DOCS.items():
    if k.startswith("05_Archivos_operativos/"):
        definidas |= set(re.findall(r"^#{2,6} ((?:RF|TA|TM|TF|ANA-DOC|DOC-MOT)-\d+)", t, re.M))
        definidas |= set(re.findall(r"^\| ((?:RF|TA|TM|TF|ANA-DOC|DOC-MOT)-\d+) \|", t, re.M))
citadas = {}
for k, t in DOCS.items():
    if k.startswith(("02_System_prompts/", "03_Funciones/")):
        for n, linea in enumerate(t.splitlines(), 1):
            for m in re.findall(r"(?<![\w-])((?:RF|TA|TM|TF|ANA-DOC|DOC-MOT)-\d+)(?![\w-])", linea):
                citadas.setdefault(m, []).append((k[:60], n))
igual("referencias citadas sin entrada ni fila", sorted(set(citadas) - definidas), ["RF-0123", "RF-1"])

print()
print("FALLOS:", fallos if fallos else "ninguno")
sys.exit(1 if fallos else 0)
