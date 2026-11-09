"""Comparación equiponderada con grupos admisibles del mismo tamaño."""
import itertools
import math
import random
from collections import Counter

from .herramientas import ht03


def universo_azar(seleccion, correlaciones=None):
    """Congela los candidatos que HT-03 admitió, antes de conocer sus rentabilidades."""
    candidatos = {}
    reglas = ht03.PARAMETROS_POR_DEFECTO["diversidad"]
    for lista in ("top_n", "alternativas", "resto_secundarios"):
        for c in seleccion[lista]:
            candidatos[c["cand_id"]] = {k: c.get(k) for k in ("subcluster", "emisor", "indice_replicado", "tesis_captura")}
    incompatibles = []
    for par, corr in (correlaciones or {}).items():
        a, b = par.split("|")
        if (a in candidatos and b in candidatos and corr > reglas["correlacion_duplicado"]
                and (candidatos[a]["tesis_captura"] or "_") == (candidatos[b]["tesis_captura"] or "_")):
            incompatibles.append([a, b])
    return {"candidatos": candidatos, "incompatibles": incompatibles, "n_previsto": seleccion["top_n_previsto"]}


def comparar_azar(universo, filas, tipo, intentos, semilla):
    resultado = {"azar_metodo": None, "azar_grupos_examinados": 0, "azar_grupos_validos": 0,
                 "azar_pct_superado": None, "azar_pct_empate": None, "azar_estado": "sin_seleccion"}
    seleccion = [f for f in filas if f.get("en_top_n")]
    if not seleccion or not universo:
        return resultado
    candidatos = universo["candidatos"]
    ids = sorted(candidatos)
    elegidos = [f["cand_id"] for f in seleccion]
    rentas = {f["cand_id"]: f["rent_fwd"] for f in filas}
    if not set(elegidos).issubset(ids) or any(rentas.get(i) is None or not math.isfinite(rentas[i]) for i in ids):
        resultado["azar_estado"] = "universo_incompleto"
        return resultado
    reglas = ht03.PARAMETROS_POR_DEFECTO["diversidad"]
    max_sub = max(1, math.floor(reglas["max_frac_subcluster"] * universo["n_previsto"]))
    incompatibles = {frozenset(par) for par in universo["incompatibles"]}
    n = len(elegidos)
    exacto = math.comb(len(ids), n) <= intentos
    rng = random.Random(semilla)
    grupos = itertools.combinations(ids, n) if exacto else (rng.sample(ids, n) for _ in range(intentos))
    objetivo = math.fsum(rentas[i] for i in elegidos) / n
    peores = empates = validos = examinados = 0
    for grupo in grupos:
        examinados += 1
        if any(par.issubset(grupo) for par in incompatibles):
            continue
        miembros = [candidatos[i] for i in grupo]
        indices = [c["indice_replicado"] for c in miembros if c["indice_replicado"]]
        if len(indices) != len(set(indices)):
            continue
        sub = Counter(c["subcluster"] for c in miembros if c["subcluster"])
        if max(sub.values(), default=0) > max_sub:
            continue
        if tipo == "RF":
            emisores = Counter(c["emisor"] for c in miembros if c["emisor"])
            if max(emisores.values(), default=0) > reglas["max_emisiones_por_emisor_RF"]:
                continue
        media = math.fsum(rentas[i] for i in grupo) / n
        validos += 1
        empates += media == objetivo
        peores += media < objetivo
    resultado.update(azar_metodo="exacto" if exacto else "muestreo", azar_grupos_examinados=examinados,
                     azar_grupos_validos=validos, azar_estado="ok" if validos else "sin_grupos_validos")
    if validos:
        resultado.update(azar_pct_superado=100 * peores / validos, azar_pct_empate=100 * empates / validos)
    return resultado
