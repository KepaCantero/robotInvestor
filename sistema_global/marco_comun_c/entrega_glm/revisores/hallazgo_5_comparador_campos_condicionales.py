"""Hallazgo 5 — comparador.py (`_leer`): dos campos que D usa se leen con tratamiento favorable si faltan.

La cabecera de D promete: «lee solo los campos que usa y falla cerrado si falta alguno». Todos los
campos que falta -> FORMA, menos dos que se leen de forma condicional:
- `entrada_salida.entrada` (o `entrada_salida` entera): si falta, se salta el control de ventana
  («CADUCADO» cuando la ventana de entrada se cerró) y el de la pérdida hasta el stop; un LARGO se
  ordena igualmente (solo se le aplica el riesgo del 100 %).
- `resultado_politica`: si falta, no se puede ver un sobre RECHAZADO y el candidato se ordena; con el
  campo presente, el mismo sobre se excluye por EXCLUSION_DURA.

Uso: python3 hallazgo_5_comparador_campos_condicionales.py   (desde la carpeta marcoC)
Imprime FALLA si el defecto existe y OK si está corregido (exigir esos campos y excluir con FORMA).
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/
sys.path.insert(0, str(RAIZ / "validador"))
sys.path.insert(0, str(RAIZ / "pruebas"))

import copy

from comparador import comparar_candidatos
from pruebas_comparador import cand
from pruebas_orquestador import AHORA

def sitio(eid, r):
    """'ranking', el motivo de exclusión o 'D-01'."""
    if not r.get("ok"):
        return "D-01"
    if any(d["expediente_id"] == eid for g in r["grupos"].values() for d in g["ranking"]):
        return "ranking"
    mot = [e["motivo"] for e in r["excluidos"] if e["expediente_id"] == eid]
    return f"excluido:{mot or '?'}"

mal = []

# 1) testigos: el mismo candidato con los campos presentes se excluye por lo que toca
c = cand(3)
c["sobre"]["payload"]["entrada_salida"]["entrada"]["ventana_hasta"] = "2026-11-06T08:00:00+00:00"  # ventana cerrada (ahora es 09:00)
r = comparar_candidatos([copy.deepcopy(cand(1)), copy.deepcopy(c)], AHORA)
if sitio("EXP-0003", r) != "excluido:['CADUCADO']":
    mal.append(f"testigo roto: ventana de entrada cerrada -> {sitio('EXP-0003', r)}")
c = cand(4, esperado=(3.0, 0.5, -4.0))
c["sobre"]["resultado_politica"]["resultado"] = "RECHAZADO"
r = comparar_candidatos([copy.deepcopy(cand(1)), copy.deepcopy(c)], AHORA)
if sitio("EXP-0004", r) != "excluido:['EXCLUSION_DURA']":
    mal.append(f"testigo roto: sobre rechazado -> {sitio('EXP-0004', r)}")

# 2) sin `entrada` se salta el control de ventana: el mismo sobre con la ventana cerrada se ordena
#    (valid_until sigue en el futuro, así que la única regla que lo excluye es la de la ventana)
c = cand(3)
c["sobre"]["payload"]["entrada_salida"]["entrada"]["ventana_hasta"] = "2026-11-06T08:00:00+00:00"
del c["sobre"]["payload"]["entrada_salida"]["entrada"]
r = comparar_candidatos([copy.deepcopy(cand(1)), copy.deepcopy(c)], AHORA)
if sitio("EXP-0003", r) == "ranking":
    mal.append("sin 'entrada' el sobre con la ventana de entrada cerrada se ordena (control saltado)")

# 3) sin `resultado_politica` un RECHAZADO se ordena
c = cand(5, esperado=(3.0, 0.5, -4.0))
c["sobre"]["resultado_politica"]["resultado"] = "RECHAZADO"
del c["sobre"]["resultado_politica"]
r = comparar_candidatos([copy.deepcopy(cand(1)), copy.deepcopy(c)], AHORA)
if sitio("EXP-0005", r) == "ranking":
    mal.append("sin 'resultado_politica' un sobre RECHAZADO se ordena")

print("FALLA " + ("; ".join(mal)) if mal else "OK")
sys.exit(1 if mal else 0)
