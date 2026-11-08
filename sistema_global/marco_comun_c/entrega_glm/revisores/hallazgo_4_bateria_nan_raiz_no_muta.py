"""Hallazgo 4 — pruebas_robustez.py (bloques CF y RM): falso «mutó la entrada» cuando la raíz queda en NaN.

El generador de la batería puede sustituir el objeto entero (camino raíz, operación «valor») por un
valor del veneno; si el valor es NaN, el objeto mutado es un NaN suelto y la comprobación «no muta la
entrada», que compara `m != foto`, da cierto aunque `validar_manual`/`validar_informe_f` no hayan
tocado nada (nan != nan). La batería cuenta entonces una mutación inexistente y
`RM_no_muta_la_entrada_en_300_mutaciones` / `CF_validar_no_muta_el_informe_en_300_mutaciones` fallan:
sale en ~1 de cada 2 semillas (RM) y ~1 de cada 16 (CF); con la oficial (20261107) no sale, por eso la
batería entrega en verde. Aquí se barre la batería real, semilla por semilla.

Uso: python3 hallazgo_4_bateria_nan_raiz_no_muta.py   (desde la carpeta marcoC)
Imprime FALLA si el defecto existe y OK si está corregido (comparación que trate NaN == NaN, o que no
compare con != la raíz escalar).
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/

CODIGO = """
import sys
sys.path.insert(0, "{raiz}/validador"); sys.path.insert(0, "{raiz}/pruebas")
import pruebas_robustez as pr
pr.SEMILLA = {semilla}
rc = pr.main()
sys.exit(rc)
"""

def bateria(semilla):
    """Ejecuta la batería real con una semilla y devuelve las comprobaciones en FALLA (o 'CRASH')."""
    r = subprocess.run([sys.executable, "-B", "-c", CODIGO.format(raiz=RAIZ, semilla=semilla)],
                       capture_output=True, text=True, cwd=str(RAIZ))
    if r.returncode not in (0, 1) or "Traceback" in r.stderr:
        return ["CRASH: " + (r.stderr.strip().splitlines() or ["?"])[-1][:120]]
    return [l.split()[1] for l in r.stdout.splitlines() if l.startswith("FALLA")]

OBJETIVO = ("RM_no_muta_la_entrada_en_300_mutaciones", "CF_validar_no_muta_el_informe_en_300_mutaciones")

mal = []
visto = None
crashes = 0
for semilla in range(1, 31):
    fallas = bateria(semilla)
    crashes += sum(1 for f in fallas if f.startswith("CRASH"))
    malas = [f for f in fallas if f in OBJETIVO]
    if malas:
        visto = (semilla, malas)
        break

if visto is not None:
    semilla, malas = visto
    mal.append(f"la batería real, con la semilla {semilla}, da FALLA en {', '.join(malas)} sin que ningún "
               f"validador mute nada: el generador puede dejar la raíz del objeto en NaN (jugada legal) y "
               f"la comprobación compara con `m != foto`, que es cierto para nan != nan")
elif crashes >= 30:
    mal.append("las 30 ejecuciones se quedaron en CRASH (no se pudo llegar a la comprobación)")

print("FALLA " + ("; ".join(mal)) if mal else "OK")
sys.exit(1 if mal else 0)
