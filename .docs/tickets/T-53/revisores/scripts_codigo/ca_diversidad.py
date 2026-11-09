"""9.6.3: con tres elegibles del mismo clúster y la mejor alternativa de otro clúster a > 10 puntos, HT-03 publica las tres."""
from bloque_a.herramientas.referencia import ht03_puntuaciones as h
def ev(oid, rk, cl):
    return {"opp_id": oid, "vigente": False, "elegible": True, "cluster": cl, "riesgo_cola": 1,
            "puntuaciones": {"RK": rk, "E": 70}, "motivos_no_elegible": []}
r = h.seleccionar_top3([ev("A", 80, "CL-1"), ev("B", 79, "CL-1"), ev("C", 78, "CL-1"), ev("D", 60, "CL-2")], h.PARAMETROS_POR_DEFECTO)
print("top3:", [(t["opp_id"], t["cluster"]) for t in r["top3"]], "| diversidad:", r["diversidad"])
