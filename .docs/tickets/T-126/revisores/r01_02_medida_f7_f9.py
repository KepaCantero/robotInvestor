"""QA r01 de T-126: medida de F7, F8 y F9 entregados (solo lectura): fichas fuera de la sección `## TX-nn` en la que están,
empates de Q dentro de cada temática y sentido del desempate por año («a igualdad, por fecha más reciente», Doc. 0), fichas D.

Uso, desde `bloque_a/11_Ejecutor`:  python ../../.docs/tickets/T-126/revisores/r01_02_medida_f7_f9.py
"""
import itertools
import re
from collections import Counter
from pathlib import Path

from bloque_a.configuracion import cargar_config
from bloque_a.herramientas import ht02
from bloque_a.referencias import Referencias

r = Referencias(cargar_config())
for k in ("F7", "F8", "F9"):
    fs = r.fichas[k]
    lineas = Path(r.rutas[k]).read_text(encoding="utf-8").splitlines()
    inicio = {f.linea_inicio: f.id for f in ht02.leer_fichas(lineas)}
    seccion, de = None, {}
    for i, ln in enumerate(lineas):
        m = re.match(r"^## (T[AMF]-\d{2})\b", ln)
        if m:
            seccion = m.group(1)
        if i in inicio:
            de[inicio[i]] = seccion
    fuera = [(f["ref_id"], f["tematica"], de.get(f["ref_id"])) for f in fs if f["tematica"] != de.get(f["ref_id"])]
    c, al_reves = Counter(), []
    for a, b in itertools.pairwise(fs):
        if a["tematica"] == b["tematica"] and a["q"] == b["q"]:
            if a["anio"] is None or b["anio"] is None:
                c["sin año"] += 1
            elif b["anio"] < a["anio"]:
                c["más reciente primero"] += 1
            elif b["anio"] == a["anio"]:
                c["mismo año"] += 1
            else:
                c["al revés"] += 1
                al_reves.append((a["ref_id"], a["anio"], b["ref_id"], b["anio"], a["q"]))
    print(f"{k}: {len(fs)} fichas · fuera de su sección {len(fuera)} {fuera[:3]} · empates {dict(c)} {al_reves} · "
          f"nivel D {sum(1 for f in fs if f['nivel'] == 'D')}")
