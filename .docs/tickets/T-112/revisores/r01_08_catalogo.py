"""QA r01 de T-112 · promoción en el Catálogo y corpus congelado.

Argumentos: <ejecutor> (como los demás r01_*) y, opcional, la raíz del árbol del padre del commit para el diff.
Comprueba: la tabla del §4 (81 filas), la madurez de cada ficha en su sección, el recuento del §1.3, que el Motor sirve
exactamente lo que tiene código e IMPLEMENTADO (más AUD-REX-001 por CT-10), que el commit solo cambia la madurez y el
§1.3, y que el manifiesto del corpus coincide con el disco.
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

eje = C.preparar(sys.argv)
from bloque_a.motor import servicio  # noqa: E402

K = C.Contador("r01_08 Catálogo y corpus")
raiz = eje.parents[1]
cat = raiz / "bloque_a" / "04_Motor_conocimiento_y_catalogo" / "Catálogo de cálculos del Motor - V5.0.md"
txt = cat.read_text(encoding="utf-8")
i, j = txt.find("\n## 4."), txt.find("\n## 5.")
filas = re.findall(r"^\| ([A-Z]+(?:-[A-Z0-9]+)+-\d{3}) \|.*\| (P\d) \| ([^|]+?) \|\s*$", txt[i:j], re.MULTILINE)
K.comprobar("§4: 81 filas de fichas, sin repetidas", len(filas) == 81 and len({f for f, _, _ in filas}) == 81, str(len(filas)))
tabla = {f: (p, e.strip()) for f, p, e in filas}
impl = {f for f, (_, e) in tabla.items() if e.startswith("IMPLEMENTADO")}
doc = {f for f, (_, e) in tabla.items() if e.startswith("Documentado") or e.startswith("DOCUMENTADO")}
otros = {f: e for f, (_, e) in tabla.items() if f not in impl | doc}
K.comprobar("§4: 71 IMPLEMENTADO y 10 DOCUMENTADO, ninguna en otro estado", (len(impl), len(doc), otros) == (71, 10, {}),
            f"{len(impl)} {len(doc)} {otros}")
t112 = {f for f, (_, e) in tabla.items() if "T-112" in e}
K.comprobar("§4: 36 promovidas con la etiqueta T-112 = las 35 fichas de la Fase 2 + AUD-REX-001",
            t112 == set(servicio.FASE2) | {"AUD-REX-001"}, str(sorted(t112 ^ (set(servicio.FASE2) | {"AUD-REX-001"}))))
K.comprobar("las 10 DOCUMENTADO son P2 y no tienen código", all(tabla[f][0] == "P2" and f not in servicio.IMPLEMENTADAS for f in doc),
            str(sorted((f, tabla[f][0], f in servicio.IMPLEMENTADAS) for f in doc)))
K.comprobar("ninguna P0/P1 queda sin promover", all(tabla[f][0] == "P2" for f in doc))
# Madurez en la sección de cada ficha
mal = []
for f, (p, e) in tabla.items():
    m = re.search(rf"^### {re.escape(f)} · .*?$(.*?)(?=^### |^## )", txt, re.MULTILINE | re.DOTALL)
    if not m:
        mal.append((f, "sin sección"))
        continue
    pm = re.search(r"^\*\*Prioridad y madurez\.\*\* (P\d) · ([^\n]+?)\.?[ \t]*$", m.group(1), re.MULTILINE)
    if not pm or pm.group(1) != p or pm.group(2).strip().rstrip(".").lower() != e.rstrip(".").lower():   # «Documentado» de las P2: sin cambios
        mal.append((f, pm.group(0)[:120] if pm else None, e))
K.comprobar("la madurez y la prioridad de cada sección coinciden con su fila del §4", not mal, str(mal[:5]))
# §1.3
m13 = re.search(r"Estado actual de las 81 fichas: (\d+) \*\*IMPLEMENTADO\*\* \(14 del ejecutor V1\.0 [^)]*?y (\d+) con casos de control[^)]*\); (\d+) \*\*DOCUMENTADO\*\*", txt)
K.comprobar("§1.3: 71 IMPLEMENTADO (14 + 57) y 10 DOCUMENTADO", bool(m13) and m13.groups() == ("71", "57", "10"), m13.group(0)[:200] if m13 else "no encontrado")
con_casos = set(servicio.CASOS_CONTROL) | servicio.SERVICIOS_CT10
K.comprobar("57 fichas con casos de control en el ejecutor", len(con_casos) == 57, str(len(con_casos)))
v14 = impl - con_casos
K.comprobar("las 14 restantes son las del ejecutor V1.0 (sin casos de control, con código)", len(v14) == 14 and v14 <= set(servicio.IMPLEMENTADAS),
            str(sorted(v14)))
# CA-2: lo que sirve el Motor
serv = {f for f in servicio.IMPLEMENTADAS if servicio.servible(f, raiz / "bloque_a")}
esperado = (set(servicio.IMPLEMENTADAS) & impl) - ({"VOL-GARCH-001"} if not servicio.garch_disponible() else set())
K.comprobar("CA-2: el Motor sirve exactamente lo que tiene código e IMPLEMENTADO", serv == esperado, str(sorted(serv ^ esperado)))
K.comprobar("AUD-REX-001: IMPLEMENTADO, sin manejador CT-09 y con casos por CT-10", "AUD-REX-001" in impl and "AUD-REX-001" not in servicio.IMPLEMENTADAS)
K.comprobar("DOCUMENTADAS_CON_CODIGO vacío", not servicio.DOCUMENTADAS_CON_CODIGO)
# Diff del commit: solo madurez y §1.3
if len(sys.argv) > 2:
    rel = cat.relative_to(raiz)
    d = subprocess.run(["git", "-C", str(raiz), "diff", "efd1bb3~1", "efd1bb3", "--", str(rel)], capture_output=True, text=True).stdout
    cambios = [x for x in d.splitlines() if x[:1] in "+-" and not x.startswith(("+++", "---"))]
    raros = [x for x in cambios if not (x.startswith(("-**Prioridad y madurez.**", "+**Prioridad y madurez.**", "-Estado actual de las 81", "+Estado actual de las 81"))
                                        or re.match(r"^[-+]\| [A-Z]+(-[A-Z0-9]+)+-\d{3} \|", x))]
    K.comprobar(f"el commit solo toca filas del §4, líneas de madurez y el §1.3 ({len(cambios)} líneas)", not raros, str(raros[:3]))
    # las filas cambian solo en la última columna
    menos = {re.match(r"^-\| (\S+) \|", x).group(1): x[1:].rsplit("|", 2)[0] for x in cambios if x.startswith("-| ")}
    mas = {re.match(r"^\+\| (\S+) \|", x).group(1): x[1:].rsplit("|", 2)[0] for x in cambios if x.startswith("+| ")}
    K.comprobar("en las filas solo cambia la columna de madurez", menos == mas and len(mas) == 36, f"{len(mas)}")
# Corpus congelado
man = (raiz / "tools" / "corpus_manifest.txt").read_text(encoding="utf-8").splitlines()
malos, n = [], 0
for linea in man:
    if not linea.strip() or linea.startswith("#"):
        continue
    partes = linea.split(None, 1) if "  " not in linea else linea.split("  ", 1)
    h, ruta = partes[0], partes[1].strip()
    p = raiz / ruta
    n += 1
    if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != h:
        malos.append(ruta)
K.comprobar(f"manifiesto del corpus: {n} archivos con su huella", not malos and n == 695, f"{n} {malos[:3]}")
sys.exit(K.fin())
