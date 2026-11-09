"""Continuidad HT-03: una vigente 'sustituida' queda fuera aunque haya hueco y entre una nueva peor."""
from bloque_a.herramientas.referencia import ht03_puntuaciones as h
P = h.PARAMETROS_POR_DEFECTO
def ev(oid, rk, E=70, vig=False, cl=None):
    return {"opp_id": oid, "vigente": vig, "elegible": True, "cluster": cl, "riesgo_cola": 1,
            "puntuaciones": {"RK": rk, "E": E}, "motivos_no_elegible": []}
evs = [ev("OPP-N1", 85), ev("OPP-N2", 62), ev("OPP-V1", 70, vig=True)]
r = h.seleccionar_top3(evs, P)
print("top3:", [(t["opp_id"], t["RK"]) for t in r["top3"]])
print("decisiones:", r["decisiones"])
print("menos_de_tres:", r["menos_de_tres_motivo"] and r["menos_de_tres_motivo"]["texto"])
