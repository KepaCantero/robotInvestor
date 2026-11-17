"""Ronda de cierre de la QA de T-175 (revisor): H-04 por el camino real de HA (`redaccion.detalles_g3v`) y efecto de
`sintesis.bloqueos_delante` en `g3_met13_tecnico` (T-165): mismo dictamen, misma lista de bloqueos y mismo conjunto de incidencias.

    cd bloque_a/11_Ejecutor && ../../.venv/bin/python ../../.docs/tickets/T-175/revisores/r03_01_cierre_orden.py
"""
import copy
import sys
import tempfile

sys.path.insert(0, ".")
sys.path.insert(0, "tests")
from conftest import AS_OF, RUTA_UNIVERSO_EJEMPLO, cargar_universo, nuevo_bloque  # noqa: E402

from bloque_a import redaccion as red  # noqa: E402
from bloque_a import sintesis as sint  # noqa: E402
from bloque_a.herramientas import ht09  # noqa: E402

b = nuevo_bloque(tempfile.mkdtemp(), cargar_universo(RUTA_UNIVERSO_EJEMPLO))
alts = {"RV": [{"opp_id": f"OPP-2026-09{i:02d}", "retirados": ["nombre"]} for i in range(6)]}


def res_con(incid, resultado):
    return {"dictamen": "APTO", "resumen": {}, "comprobaciones": [
        {"id": "C01", "nombre": "x", "resultado": "ADVERTENCIA", "incidencias": [{"severidad": "ADVERTENCIA", "detalle": "c01"}]},
        {"id": ht09.ID_MET13, "nombre": ht09.NOMBRE_MET13, "resultado": resultado, "datos": {"fichas_citadas": []}, "incidencias": incid}]}


# 1) detalles_g3v sobre una lista SIN ordenar (como si nadie hubiera llamado a bloqueos_delante)
c = {"incidencias": [{"severidad": "ADVERTENCIA", "detalle": f"a{i}"} for i in range(6)] + [{"severidad": "BLOQUEO", "detalle": "B1"},
                                                                                           {"severidad": "BLOQUEO", "detalle": "B2"}]}
d = red.detalles_g3v(c)
print(("OK  " if d[:2] == ["B1", "B2"] and d[2:] == ["a0", "a1", "a2"] else "MAL ") + f"detalles_g3v sin ordenar antes: {d}")
# 2) g3_met13_tecnico: con y sin bloqueos_delante, mismo dictamen, motivo, bloqueos y multiconjunto de incidencias
for previo in ([], [{"severidad": "ADVERTENCIA", "ruta": "x", "detalle": "adv F6"}],
               [{"severidad": "BLOQUEO", "ruta": "informe_visual", "detalle": "bloq visual"}]):
    base = res_con(copy.deepcopy(previo), "BLOQUEO" if any(i["severidad"] == "BLOQUEO" for i in previo) else
                   ("ADVERTENCIA" if previo else "OK"))
    sint.advertir_alternativas_retiradas(base, alts)
    a, z = copy.deepcopy(base), copy.deepcopy(base)
    ra = sint.g3_met13_tecnico(b, a, "El método ST-DESC-001 está validado.")
    orig = sint.bloqueos_delante
    sint.bloqueos_delante = lambda comp: None          # T-165 sin el cambio de la ronda de cierre
    try:
        rz = sint.g3_met13_tecnico(b, z, "El método ST-DESC-001 está validado.")
    finally:
        sint.bloqueos_delante = orig
    ma, mz = a["comprobaciones"][1], z["comprobaciones"][1]
    clave = lambda i: (i["severidad"], i.get("ruta"), i["detalle"])  # noqa: E731
    igual = (ra == rz and a["dictamen"] == z["dictamen"] and a.get("motivo") == z.get("motivo") and a["resumen"] == z["resumen"]
             and [x["resultado"] for x in a["comprobaciones"]] == [x["resultado"] for x in z["comprobaciones"]]
             and sorted(map(clave, ma["incidencias"])) == sorted(map(clave, mz["incidencias"])))
    hay_b = any("BLOQUEO" == i["severidad"] for i in ma["incidencias"])
    print(("OK  " if igual else "MAL ") + f"previo={[i['detalle'] for i in previo]} · dictamen {a['dictamen']} · mismo resultado con y sin"
          f" bloqueos_delante: {igual} · BLOQUEO en los 5 de HA: {any(x in ('bloq visual',) or 'validado' in x for x in red.detalles_g3v(ma)) if hay_b else '—'}")
