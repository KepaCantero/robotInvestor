"""T-61 · QA de Claude, ronda r02: ataques a comparacion_azar (rama astra/bloque-b-backtesting-cobertura-y-azar).
Uso: PYTHONPATH=<ruta a bloque_b/11_Ejecutor> python3 r02_ataques_azar.py"""
import math
from fractions import Fraction

from bloque_b import comparacion_azar as ca
from bloque_b.herramientas import ht03

fallos = []


def comprobar(nombre, cond):
    print(("OK   " if cond else "FALLA") + " " + nombre)
    if not cond:
        fallos.append(nombre)


def cand(i, sub=None, emisor=None, indice=None):
    return {"cand_id": f"C{i}", "subcluster": sub, "emisor": emisor, "indice_replicado": indice, "tesis_captura": None}


def seleccion(n_cands, top, n_previsto=None, **kw):
    cs = [cand(i, **kw) for i in range(n_cands)]
    return {"top_n": cs[:top], "alternativas": cs[top:], "resto_secundarios": [], "top_n_previsto": n_previsto or top}


def filas(n_cands, top, rentas):
    return [{"cand_id": f"C{i}", "en_top_n": i < top, "rent_fwd": rentas[i]} for i in range(n_cands)]


# 1. Sin selección o sin universo: no inventa nada
u = ca.universo_azar(seleccion(6, 2))
comprobar("sin elegidos → sin_seleccion", ca.comparar_azar(u, filas(6, 0, [0.1] * 6), "RV", 100, "s")["azar_estado"] == "sin_seleccion")
comprobar("sin universo → sin_seleccion", ca.comparar_azar(None, filas(6, 2, [0.1] * 6), "RV", 100, "s")["azar_estado"] == "sin_seleccion")

# 2. Un candidato admitido sin precio, NaN o infinito: universo incompleto (no compara con un grupo sesgado)
for malo in (None, float("nan"), float("inf")):
    r = [0.1, 0.2, 0.0, malo, 0.05, 0.03]
    comprobar(f"renta {malo} en el universo → universo_incompleto",
              ca.comparar_azar(u, filas(6, 2, r), "RV", 100, "s")["azar_estado"] == "universo_incompleto")

# 3. Un elegido que no está en el universo → universo_incompleto
fs = filas(6, 2, [0.1] * 6) + [{"cand_id": "X", "en_top_n": True, "rent_fwd": 0.5}]
comprobar("elegido ajeno al universo → universo_incompleto", ca.comparar_azar(u, fs, "RV", 100, "s")["azar_estado"] == "universo_incompleto")

# 4. Enumeración exacta: C(6,2)=15 grupos; la selección es la mejor → supera a 14 y empata con ella misma
r = [0.9, 0.8, 0.1, 0.2, 0.3, 0.4]
res = ca.comparar_azar(u, filas(6, 2, r), "RV", 1000, "s")
comprobar("exacto: 15 grupos examinados y válidos", res["azar_metodo"] == "exacto" and res["azar_grupos_examinados"] == 15 and res["azar_grupos_validos"] == 15)
comprobar("exacto: supera al 14/15 y empata 1/15", math.isclose(res["azar_pct_superado"], 100 * 14 / 15) and math.isclose(res["azar_pct_empate"], 100 / 15))

# 5. Muestreo: misma semilla, mismo resultado; la semilla de texto no depende de PYTHONHASHSEED
u20 = ca.universo_azar(seleccion(20, 5))
r20 = [((i * 37) % 11) / 10 for i in range(20)]
a = ca.comparar_azar(u20, filas(20, 5, r20), "RV", 50, "clave|2024-01-31|RV|H3")
b = ca.comparar_azar(u20, filas(20, 5, r20), "RV", 50, "clave|2024-01-31|RV|H3")
comprobar("muestreo determinista con la misma semilla", a == b and a["azar_metodo"] == "muestreo" and a["azar_grupos_examinados"] == 50)

# 6. Diversidad: dos del mismo índice replicado no forman grupo válido
sel = seleccion(4, 2)
sel["alternativas"][0]["indice_replicado"] = "IDX"
sel["alternativas"][1]["indice_replicado"] = "IDX"
res = ca.comparar_azar(ca.universo_azar(sel), filas(4, 2, [0.4, 0.3, 0.2, 0.1]), "RV", 100, "s")
comprobar("mismo índice replicado: 5 de 6 grupos válidos", res["azar_grupos_validos"] == 5)

# 7. RF: no más de max_emisiones_por_emisor_RF del mismo emisor (2) en un grupo de 3
dv = ht03.PARAMETROS_POR_DEFECTO["diversidad"]
selrf = seleccion(5, 3, emisor="E1")
res = ca.comparar_azar(ca.universo_azar(selrf), filas(5, 3, [0.1] * 5), "RF", 100, "s")
comprobar(f"RF: todos del mismo emisor y grupos de 3 > {dv['max_emisiones_por_emisor_RF']} → sin_grupos_validos",
          res["azar_estado"] == "sin_grupos_validos" and res["azar_pct_superado"] is None)

# 8. Hallazgo: el límite de subclúster se aplica aunque el ámbito sea un subclúster (HT-03 no lo aplica entonces)
selsub = seleccion(6, 3, sub="S1")   # todos del mismo subclúster, como en un ámbito que ES un subclúster
res = ca.comparar_azar(ca.universo_azar(selsub), filas(6, 3, [0.1] * 6), "RV", 100, "s")
comprobar("ámbito-subclúster: la comparación se queda sin grupos aunque HT-03 sí selecciona (esperado: hallazgo H-06)",
          res["azar_estado"] == "sin_grupos_validos")

# 9. Pesos racionales en la réplica: calcular_S sigue devolviendo un número serializable
comp = {k: 50 for k in ht03.PARAMETROS_POR_DEFECTO["pesos"]["RV"]} if "RV" in ht03.PARAMETROS_POR_DEFECTO["pesos"] else None
if comp:
    pesos = {k: Fraction("0.25") for k in comp}
    s = ht03.calcular_S(comp, "RV", pesos)["S"]
    comprobar(f"calcular_S con pesos Fraction devuelve {type(s).__name__}", isinstance(s, (int, float)))
else:
    print("·    sin pesos RV en los parámetros por defecto; omitido el punto 9")

print(f"\n{len(fallos)} fallos")
raise SystemExit(1 if fallos else 0)
