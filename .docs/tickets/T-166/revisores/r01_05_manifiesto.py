"""QA r01 de T-166 · diff del manifiesto del corpus contra la base (develop a9210c0).

Uso (desde la raíz de la copia): python3 -I .docs/tickets/T-166/revisores/r01_05_manifiesto.py [BASE]
Comprueba: cada ruta del histórico tiene el hash que su original tenía en la base; nada fuera de alcance cambia; los hashes
del manifiesto nuevo son los de los archivos en disco.
"""
import hashlib
import subprocess
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
BASE = sys.argv[1] if len(sys.argv) > 1 else "a9210c0"
ALCANCE = ("bloque_a/01_Gobernanza/", "bloque_a/02_System_prompts/", "bloque_a/03_Funciones/", "bloque_a/05_Archivos_operativos/",
           "bloque_a/99_Historico_V5.2/", "bloque_a/README - Índice de la entrega")


def leer(texto):
    d = {}
    for linea in texto.splitlines():
        if linea.strip():
            h, ruta = linea.split("  ", 1)
            d[unicodedata.normalize("NFC", ruta)] = h
    return d


antes = leer(subprocess.run(["git", "-C", str(RAIZ), "show", f"{BASE}:tools/corpus_manifest.txt"], capture_output=True, text=True, check=True).stdout)
ahora = leer((RAIZ / "tools/corpus_manifest.txt").read_text(encoding="utf-8"))
fallos = []
quitadas = sorted(set(antes) - set(ahora))
puestas = sorted(set(ahora) - set(antes))
cambiadas = sorted(r for r in set(antes) & set(ahora) if antes[r] != ahora[r])
for r in quitadas + puestas + cambiadas:
    if not r.startswith(ALCANCE):
        fallos.append(f"fuera de alcance: {r}")
for r in puestas:
    if r.startswith("bloque_a/99_Historico_V5.2/"):
        orig = r.replace("99_Historico_V5.2/", "", 1)
        if antes.get(orig) != ahora[r]:
            fallos.append(f"histórico con otro hash que su original de la base: {r}")
for r, h in ahora.items():
    p = RAIZ / r
    if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != h:
        fallos.append(f"hash en disco distinto: {r}")
print(f"base {len(antes)} · ahora {len(ahora)} · quitadas {len(quitadas)} · puestas {len(puestas)} · cambiadas {len(cambiadas)}")
for x in ("marco_comun_c", "constitucion", "bloque_a_forex/", "bloque_b/"):
    print(x, "tocado:", any(x in r.lower() for r in quitadas + puestas + cambiadas))
print("fallos:", fallos or "ninguno")
sys.exit(1 if fallos else 0)
