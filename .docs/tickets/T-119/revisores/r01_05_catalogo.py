"""QA r01 de T-119 · Catálogo, corpus y despacho (CA-2 y CA-6).

 1. §4: 81 filas, 81 IMPLEMENTADO, 0 Documentado; 10 con la etiqueta T-119, y son las 10 P2. Cada sección de esas 10 dice
    IMPLEMENTADO (T-119). §1.3: 81 = 14 + 67; ninguna en DOCUMENTADO.
 2. Diff del Catálogo frente al padre (`08862e8`): 21 líneas, solo la columna de madurez de 10 filas, 10 líneas de
    «Prioridad y madurez» y el §1.3.
 3. Manifiesto del corpus: la huella sha256 del Catálogo es la del manifiesto; 695 huellas; solo cambia esa línea.
 4. CA-2: servible = código ∩ IMPLEMENTADO: 80 manejadores servibles por CT-09 + AUD-REX-001 por CT-10; ficha ajena ⇒
    OPERACION_SIN_FICHA; con un Catálogo que devuelve una P2 a «Documentado» (copia desechable) ⇒ METODO_NO_IMPLEMENTADO.
 5. `promover_fichas_catalogo.py --aplicar --etiqueta "ejecutor, casos de control registrados (T-119)"` sobre el Catálogo
    del padre, en una copia desechable: resultado idéntico byte a byte al de la copia revisada.
Uso: r01_05_catalogo.py [ejecutor] --desechable <carpeta vacía donde copiar>
"""
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

eje = C.preparar(sys.argv)
from bloque_a.motor import servicio  # noqa: E402

K = C.Contador("r01_05 Catálogo, corpus y despacho")
RAIZ = C.RAIZ_REPO
PADRE = "08862e8"
REL = "bloque_a/04_Motor_conocimiento_y_catalogo/Catálogo de cálculos del Motor - V5.0.md"
cat = (RAIZ / REL).read_text(encoding="utf-8")
filas = re.findall(r"^\| ([A-Z]+(?:-[A-Z0-9]+)+-\d{3}) \|.*\| (P\d) \| ([^|]+?) \|\s*$", cat, re.MULTILINE)
K.comprobar(f"§4: 81 filas ({len(filas)}), sin repetidas", len(filas) == 81 and len({f for f, _, _ in filas}) == 81)
impl = [f for f, _, m_ in filas if m_.startswith("IMPLEMENTADO")]
K.comprobar(f"§4: 81 IMPLEMENTADO ({len(impl)}) y ninguna Documentado/VALIDADO", len(impl) == 81)
t119 = sorted(f for f, _, m_ in filas if "T-119" in m_)
K.comprobar("§4: las de la etiqueta T-119 son las 10 P2 y siguen siendo P2", t119 == sorted(C.P2) and all(p == "P2" for f, p, _ in filas if f in C.P2))
for f in C.P2:
    sec = cat[cat.index(f"\n### {f} ·"):]
    sec = sec[:sec.index("\n### ", 1)] if "\n### " in sec[1:] else sec
    K.comprobar(f"sección de {f}: IMPLEMENTADO (T-119)", "**Prioridad y madurez.** P2 · IMPLEMENTADO (ejecutor, casos de control registrados (T-119))." in sec)
K.comprobar("ninguna sección dice DOCUMENTADO en «Prioridad y madurez»", not re.search(r"\*\*Prioridad y madurez\.\*\* P\d · DOCUMENTADO", cat))
l13 = next(x for x in cat.split("\n") if x.startswith("Estado actual de las"))
print("   §1.3:", l13)
K.comprobar("§1.3: 81 = 14 + 67, ninguna en DOCUMENTADO", "81 **IMPLEMENTADO** (14 del ejecutor V1.0 con pruebas unitarias y 67 con casos" in l13
            and "ninguna queda en **DOCUMENTADO**" in l13)
etiquetas = {}
for _, _, m_ in filas:
    etiquetas[m_] = etiquetas.get(m_, 0) + 1
print("   madurez por etiqueta:", etiquetas)
K.comprobar("14 + 67 cuadra con las etiquetas de la tabla (67 con «casos de control registrados»)",
            sum(n for e, n in etiquetas.items() if "casos de control registrados" in e) == 67)

d = subprocess.run(["git", "-C", str(RAIZ), "diff", PADRE, "--", REL], capture_output=True, text=True).stdout
menos = [x[1:] for x in d.split("\n") if x.startswith("-") and not x.startswith("---")]
mas = [x[1:] for x in d.split("\n") if x.startswith("+") and not x.startswith("+++")]
K.comprobar(f"diff frente a {PADRE}: 21 líneas cambiadas ({len(menos)}/{len(mas)})", len(menos) == 21 and len(mas) == 21)
solo_madurez = True
for a, b in zip(sorted(menos), sorted(mas)):
    if a.startswith("| "):
        solo_madurez &= a.rsplit("|", 2)[0] == b.rsplit("|", 2)[0] and a.rsplit("|", 2)[1].strip() == "Documentado"
K.comprobar("diff: en las filas solo cambia la última columna (Documentado → IMPLEMENTADO (T-119))", solo_madurez)
K.comprobar("diff: 10 líneas «P2 · DOCUMENTADO.» y el §1.3", sum(x == "**Prioridad y madurez.** P2 · DOCUMENTADO." for x in menos) == 10
            and sum(x.startswith("Estado actual") for x in menos) == 1 and sum(x.startswith("| ") for x in menos) == 10)

man = (RAIZ / "tools/corpus_manifest.txt").read_text(encoding="utf-8").strip().split("\n")
huella = hashlib.sha256((RAIZ / REL).read_bytes()).hexdigest()
K.comprobar(f"manifiesto: {len(man)} huellas (695) y la del Catálogo coincide ({huella[:12]})", len(man) == 695 and f"{huella}  {REL}" in man)
dm = subprocess.run(["git", "-C", str(RAIZ), "diff", PADRE, "--numstat", "--", "tools/corpus_manifest.txt"], capture_output=True, text=True).stdout
K.comprobar(f"manifiesto: una sola línea cambiada ({dm.split()[:2]})", dm.split()[:2] == ["1", "1"])

mad = servicio.madurez_catalogo()
sirve = sorted(f for f in servicio.FICHAS_CATALOGO if servicio.servible(f))
K.comprobar(f"CA-2: 80 manejadores ({len(servicio.IMPLEMENTADAS)}) y 80 servibles ({len(sirve)}); el que falta es AUD-REX-001",
            len(servicio.IMPLEMENTADAS) == 80 and len(sirve) == 80 and set(servicio.FICHAS_CATALOGO) - set(sirve) == {"AUD-REX-001"}
            and "AUD-REX-001" in servicio.SERVICIOS_CT10)
K.comprobar("CA-2: servible = código ∩ IMPLEMENTADO en el Catálogo", set(sirve) == {f for f in servicio.IMPLEMENTADAS if (mad.get(f) or "").startswith("IMPLEMENTADO")})
K.comprobar("DOCUMENTADAS_CON_CODIGO vacío; las 10 en ESTRICTAS y sin semilla", not servicio.DOCUMENTADAS_CON_CODIGO
            and set(C.P2) <= servicio.ESTRICTAS and not set(C.P2) & servicio.ACEPTA_SEMILLA)
m = C.motor()
r = C.servir(m, "ZZZ-NADA-001", {}, {})
K.comprobar("ficha ajena ⇒ OPERACION_SIN_FICHA", r["estado"] == "RECHAZADO" and r["motivo"] == "OPERACION_SIN_FICHA")
r = C.servir(m, "AUD-REX-001", {}, {})
K.comprobar("AUD-REX-001 por CT-09 ⇒ rechazo", r["estado"] == "RECHAZADO")

if "--desechable" in sys.argv:
    des = Path(sys.argv[sys.argv.index("--desechable") + 1]).resolve()
    des.mkdir(parents=True, exist_ok=True)
    for sub in ("bloque_a", ".docs/scripts"):
        shutil.copytree(RAIZ / sub, des / sub, ignore=shutil.ignore_patterns("*.docx", "__pycache__", ".pytest_cache", "*.pdf"), dirs_exist_ok=True)
    viejo = subprocess.run(["git", "-C", str(RAIZ), "show", f"{PADRE}:{REL}"], capture_output=True).stdout
    (des / REL).write_bytes(viejo)
    # con el Catálogo del padre, las 10 P2 no se sirven (manda el Catálogo)
    cod = ("import sys; sys.path.insert(0, sys.argv[1]); sys.path.insert(0, sys.argv[2]); import r01_comun as C; from bloque_a.motor import servicio; "
           "m = C.motor(); v, p = C.caso('PRV-PME-001', 0); r = C.servir(m, 'PRV-PME-001', v, p); print(r['estado'], r.get('motivo'), len([f for f in servicio.FICHAS_CATALOGO if servicio.servible(f)]))")
    pr = subprocess.run([sys.executable, "-c", cod, str(des / "bloque_a/11_Ejecutor"), str(Path(__file__).resolve().parent)], capture_output=True, text=True)
    print("   con el Catálogo del padre:", pr.stdout.strip(), pr.stderr[-300:])
    K.comprobar("Catálogo del padre (10 P2 en Documentado) ⇒ METODO_NO_IMPLEMENTADO y 70 servibles", pr.stdout.strip() == "RECHAZADO METODO_NO_IMPLEMENTADO 70")
    pr = subprocess.run([sys.executable, str(des / ".docs/scripts/promover_fichas_catalogo.py"), "--aplicar", "--etiqueta",
                         "ejecutor, casos de control registrados (T-119)"], capture_output=True, text=True, cwd=des)
    cola = [x for x in pr.stdout.split("\n") if x.startswith(("Promovidas", "NO SUPERA"))]
    print("   promover:", cola, pr.stderr[-300:])
    K.comprobar("promover: 10 promovidas y ninguna que no supere", any(x.startswith("Promovidas: 10 · No superan: []") for x in cola))
    K.comprobar("promover: el Catálogo resultante es idéntico byte a byte al revisado", (des / REL).read_bytes() == (RAIZ / REL).read_bytes())
    shutil.rmtree(des)
sys.exit(K.fin())
