"""Hallazgo 3 — pruebas_robustez.py: la exención «contexto entero a None es el uso de E» no se aplica en
los bucles aleatorios (dos manifestaciones).

El generador de la batería puede sustituir el objeto entero (camino raíz, operación «valor») por None.
Con el CONTEXTO eso es el uso de E sin contexto, y la batería lo reconoce en otros dos sitios — el
barrido sistemático excluye contexto=None («El contexto entero a None no va: es el uso de E sin
contexto») y la comprobación fija `F_sin_contexto_es_el_uso_de_E_...por_diseno` exige APROBADO—. Pero
los bucles aleatorios no lo eximen:
  (a) bloque F: la mutación se clasifica como «de forma» (dict -> none) y exige F-01, así que
      `F_forma_del_contexto_veta_F01_en_N_casos` falla (~1 de cada 7 semillas);
  (b) bloque construir_informe: el informe sale VETADO «falta el contexto» (correcto: un CT-G-08 sin
      contexto no vale, CF-01) y la coherencia lo compara con `controlar(..., None)`, que es el uso de E
      y da APROBADO (también correcto) -> `F_informe_coherente_con_controlar_en_200_mutaciones` falla.
      (Esta segunda manifestación estaba oculta por el hallazgo 6: con la cartera mutilada, ambos lados
      daban VETADO.)

Uso: python3 hallazgo_3_bateria_contexto_none.py   (desde la carpeta marcoC)
Imprime FALLA si el defecto existe y OK si está corregido (los bucles eximen contexto->None como el
barrido sistemático).
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/

CODIGO = """
import sys
sys.path.insert(0, r"{raiz}/validador")
sys.path.insert(0, r"{raiz}/pruebas")
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

OBJETIVO = ("F_forma_del_contexto_veta_F01", "F_informe_coherente_con_controlar_en_200_mutaciones")

mal = []
visto = None
crashes = 0
for semilla in range(1, 31):
    fallas = bateria(semilla)
    crashes += sum(1 for f in fallas if f.startswith("CRASH"))
    malas = [f for f in fallas if f.startswith(OBJETIVO)]
    if malas:
        visto = (semilla, malas)
        break

if visto is not None:
    semilla, malas = visto
    mal.append(f"la batería real, con la semilla {semilla}, da FALLA en {', '.join(malas)} sin que ningún "
               f"validador incumpla nada: la mutación raíz contexto->None es el uso de E (APROBADO por "
               f"diseño, como afirman el barrido sistemático y la comprobación fija de la misma batería; "
               f"y un informe CT-G-08 sin contexto se veta «falta el contexto», no se compara con el uso de E)")
elif crashes >= 30:
    mal.append("las 30 ejecuciones se quedaron en CRASH (no se pudo llegar a la comprobación)")

print("FALLA " + ("; ".join(mal)) if mal else "OK")
sys.exit(1 if mal else 0)
