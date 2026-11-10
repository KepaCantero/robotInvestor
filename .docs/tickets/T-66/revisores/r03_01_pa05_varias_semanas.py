"""T-66 · QA r03 · PA-05 a lo largo de varias semanas: ¿se relaja sola la regla de Contrarias?

1 · Alta frágil (fuerte resuelta con evidencia y contrarréplica) y 5 semanas de arrastre seguidas: ¿sigue «especulativo» y
    «tesis frágil» cada semana, también cuando se reemiten pronósticos vencidos?
2 · Una vigente frágil vuelve a ser finalista (N2): el veredicto sale de la refutación nueva; con una fuerte nueva sin
    evidencia no se publica, y con la refutación caída tampoco.
3 · Una fuerte se reabre en el arrastre (registro de formato anterior) y después el Analista la responde bien.
4 · Determinismo: el escenario 1 dos veces en carpetas distintas.

Uso: PYTHONPATH=<ejecutor de A>:<revisores r01> python r03_01_pa05_varias_semanas.py   (imprime OK / HALLAZGO / INFO)
"""
import copy
import json
import tempfile

import pandas as pd
from r01_comun import Gancho, bloque, comprobar, fin

CLASE = "RV"
SEMANAS = ["2026-06-05", "2026-06-12", "2026-06-19", "2026-06-26", "2026-07-03", "2026-07-10"]


def hacer_gancho(estado):
    """estado["modo"]: alta (fuerte con evidencia y confirmación) · arrastre (sin finalistas) · sin_evidencia (fuerte que el
    Analista da por resuelta sin citar nada) · sin_refutacion (AG-11 no devuelve nada) · normal (simulado sin tocar)."""

    def g(agente, msg, datos):
        m = estado["modo"]
        if agente == "AG-11" and not msg.get("contrarreplicas"):
            if m == "sin_refutacion":
                return {"resultados": [], "autoevaluacion": "-"}
            if m in ("alta", "sin_evidencia"):
                for x in datos["resultados"]:
                    x["objeciones"] = [o for o in x["objeciones"] if o["fuerza"] != "fuerte"] + [
                        {"id": f"OBJ-{x['ref']}-09", "tipo": "evidencia_insuficiente", "fuerza": "fuerte", "argumento": "QA r03",
                         "evidencia": "-", "que_la_resolveria": "Dos fuentes independientes"}]
            return datos
        if msg.get("fase") == "RESPUESTA_OBJECIONES" and m in ("alta", "sin_evidencia"):
            return {"respuestas": [{"objecion_id": o["objecion_id"], "respuesta": "Resuelta con la serie HT-01 y el cálculo del Motor",
                                    "resuelta": True,
                                    **({"evidencia_citada": list(o.get("evidencia_disponible") or [])[:2]} if m == "alta" else {})}
                                   for o in msg["objeciones"]]}
        if m == "arrastre" and isinstance(datos, dict) and "finalistas" in datos:
            datos["finalistas"] = []
        return datos
    return g


def foto(b, r):
    """Lo que se publica y lo que queda en F3 de las opciones de la clase."""
    f3 = b.almacen.estado("F3")
    pub = {o["opp_id"]: o for o in r["paquete"]["clases"][CLASE]["opciones"]}
    return {"nivel": r["nivel_por_clase"].get(CLASE), "estado": r["estado"],
            "publicadas": {k: o["confianza"] for k, o in pub.items()},
            "f3": {k: {"estado": v.get("estado"), "veredicto": v.get("veredicto_refutacion"), "version": v.get("version"),
                       "fuertes": [(o.get("objecion_id"), o.get("resuelta"), bool(o.get("evidencia_citada")), "contrarreplica" in o,
                                    o.get("reabierta_por") is not None)
                                   for o in v.get("objeciones_internas") or [] if o.get("fuerza") == "fuerte"]}
                   for k, v in f3.items() if v.get("clase") == CLASE}}


def fuerte_mal_resuelta(fs):
    """Una fuerte resuelta sin evidencia citada o sin contrarréplica."""
    return [x for x in fs if x[1] and not (x[2] and x[3])]


def escenario_1(tmp=None):
    est = {"modo": "alta"}
    b = bloque(cliente=Gancho(hacer_gancho(est)), tmp=tmp)
    fotos = []
    for i, s in enumerate(SEMANAS):
        est["modo"] = "alta" if i == 0 else "arrastre"
        r = b.ciclo(s, alcance={"clases": [CLASE]})
        fotos.append(foto(b, r))
    reemitidos = [p for p in b.almacen.leer("F4") if p.get("version_de")]
    return b, fotos, reemitidos


# ---------------------------------------------------------------- 1 · arrastre de varias semanas
b1, fotos, reemitidos = escenario_1()
altas = set(fotos[0]["publicadas"])
print("    semana 1:", fotos[0]["nivel"], fotos[0]["publicadas"])
for s, ft in zip(SEMANAS[1:], fotos[1:]):
    print(f"    {s}: nivel {ft['nivel']}, publicadas {ft['publicadas']}, veredictos {sorted({v['veredicto'] for k, v in ft['f3'].items() if k in altas})}")
comprobar("1 · semana 1: las frágiles salen «especulativo»", bool(altas) and set(fotos[0]["publicadas"].values()) == {"especulativo"},
          str(fotos[0]["publicadas"]))
malas = [(s, k, c) for s, ft in zip(SEMANAS, fotos) for k, c in ft["publicadas"].items() if k in altas and c != "especulativo"]
comprobar("1 · 5 semanas de arrastre: ninguna frágil vuelve a «probable»", not malas, f"relajadas {malas[:4]}")
ver = [(s, k, ft["f3"][k]["veredicto"]) for s, ft in zip(SEMANAS, fotos) for k in ft["publicadas"] if k in altas and ft["f3"][k]["veredicto"] != "tesis frágil"]
comprobar("1 · el veredicto «tesis frágil» se conserva en cada versión de F3", not ver, f"distintos {ver[:4]}")
siguen = [len([k for k in ft["publicadas"] if k in altas]) for ft in fotos]
comprobar("1 · las frágiles bien resueltas no se reabren por error (siguen publicándose)", min(siguen) == len(altas), f"publicadas por semana {siguen}")
mal = [(s, k) for s, ft in zip(SEMANAS, fotos) for k in ft["publicadas"] if fuerte_mal_resuelta(ft["f3"][k]["fuertes"])]
comprobar("1 · ninguna publicada con una fuerte resuelta sin evidencia o sin contrarréplica", not mal, str(mal[:4]))
opp_reem = {p["opp_id"] for p in reemitidos}
comprobar("1 · hay pronósticos vencidos reemitidos en el arrastre (el camino se ejerce)", bool(opp_reem & altas),
          f"{len(reemitidos)} reemitidos, de {sorted(opp_reem)}", hallazgo=False)
reem_pub = [(s, k, c) for s, ft in zip(SEMANAS, fotos) for k, c in ft["publicadas"].items() if k in opp_reem and c != "especulativo"]
comprobar("1 · con pronósticos reemitidos, la opción sigue «especulativo»", not reem_pub, str(reem_pub[:4]))

# ---------------------------------------------------------------- 4 · determinismo
_, fotos_b, reem_b = escenario_1(tempfile.mkdtemp(prefix="r03_det_"))
comprobar("4 · determinismo: mismas publicaciones, veredictos, objeciones y reemisiones en dos carpetas",
          json.dumps(fotos, sort_keys=True) == json.dumps(fotos_b, sort_keys=True)
          and [p["prg_id"] for p in reemitidos] == [p["prg_id"] for p in reem_b])

# ---------------------------------------------------------------- 2 · una vigente frágil vuelve a ser finalista
for modo, espera_pub in (("normal", None), ("sin_evidencia", False), ("sin_refutacion", False)):
    est = {"modo": "alta"}
    b = bloque(cliente=Gancho(hacer_gancho(est)))
    r1 = b.ciclo(SEMANAS[0], alcance={"clases": [CLASE]})
    a = set(foto(b, r1)["publicadas"])
    est["modo"] = "arrastre"
    for sem in SEMANAS[1:3]:                     # 12-06 y 19-06 son N1: arrastre
        b.ciclo(sem, alcance={"clases": [CLASE]})
    est["modo"] = modo
    r2 = b.ciclo(SEMANAS[3], alcance={"clases": [CLASE]})   # 26-06 es N2: las frágiles vuelven a ser finalistas
    ft = foto(b, r2)
    comprobar(f"2 · «{modo}»: la semana de la re-finalista es N2 (el camino se ejerce)", ft["nivel"] == "N2", ft["nivel"], hallazgo=False)
    if modo == "normal":
        # el veredicto se recalcula por la regla sobre las objeciones NUEVAS (no se hereda ni se pierde)
        regla = {k: b._veredicto_refutacion({"_objeciones": b.almacen.estado("F3")[k]["objeciones_internas"]}) for k in a}
        dist = {k: (ft["f3"][k]["veredicto"], regla[k]) for k in a if ft["f3"][k]["veredicto"] != regla[k]}
        comprobar("2 · re-finalista con refutación nueva: veredicto en F3 = regla sobre las objeciones nuevas", not dist,
                  f"nivel {ft['nivel']}; {dist}")
        conf = {k: (ft["publicadas"].get(k), ft["f3"][k]["veredicto"]) for k in a}
        mal = {k: v for k, v in conf.items() if v[0] == "probable" and v[1] == "tesis frágil"}
        comprobar("2 · re-finalista: una frágil por la regla nueva nunca sale «probable»", not mal, f"{conf}")
        viejas = [k for k in a if any(x[0].endswith("-09") and x[1] for x in ft["f3"][k]["fuertes"])]
        comprobar("2 · re-finalista: no hereda la fuerte resuelta de la semana anterior", not viejas, str(viejas), hallazgo=False)
    else:
        pub = set(ft["publicadas"]) & a
        estados = {k: ft["f3"][k]["estado"] for k in a}
        comprobar(f"2 · re-finalista con «{modo}»: no se publica ninguna de las antiguas frágiles", not pub,
                  f"nivel {ft['nivel']}; publicadas {sorted(pub)}; estados F3 {estados}")
        sigue_vig = [k for k, e in estados.items() if e in ("PROPUESTA", "VIGENTE")]
        comprobar(f"2 · re-finalista con «{modo}»: ninguna queda VIGENTE en F3", not sigue_vig, str(estados))

# ---------------------------------------------------------------- 3 · fuerte reabierta y luego bien respondida
est = {"modo": "alta"}
b = bloque(cliente=Gancho(hacer_gancho(est)))
r1 = b.ciclo(SEMANAS[0], alcance={"clases": [CLASE]})
a = sorted(foto(b, r1)["publicadas"])
v = copy.deepcopy(b.almacen.estado("F3")[a[0]])
for o in v["objeciones_internas"]:
    if o["fuerza"] == "fuerte":
        o.pop("evidencia_citada", None)
        o.pop("contrarreplica", None)
v.pop("veredicto_refutacion", None)
v["version"] += 1
v["tipo_entrada"] = "ACTUALIZACION"
b.almacen.escribir("F3", "AG-02", v)          # registro de formato anterior a PA-05, escrito por la vía normal
est["modo"] = "arrastre"
r2 = b.ciclo(SEMANAS[1], alcance={"clases": [CLASE]})
f2 = foto(b, r2)
comprobar("3 · semana 2 (arrastre): la opción con la fuerte de formato anterior no se publica", a[0] not in f2["publicadas"],
          f"publicadas {f2['publicadas']}; F3 {f2['f3'][a[0]]}")
comprobar("3 · semana 2: queda CERRADA, con la fuerte reabierta y «tesis refutada»",
          f2["f3"][a[0]]["estado"] == "CERRADA" and any(x[4] and x[1] is False for x in f2["f3"][a[0]]["fuertes"]),
          str(f2["f3"][a[0]]), hallazgo=False)
comprobar("3 · semana 2: las otras dos siguen frágiles y especulativas", all(f2["publicadas"].get(k) == "especulativo" for k in a[1:]),
          str(f2["publicadas"]))
b.ciclo(SEMANAS[2], alcance={"clases": [CLASE]})   # 19-06, N1: arrastre
est["modo"] = "alta"
r3 = b.ciclo(SEMANAS[3], alcance={"clases": [CLASE]})   # 26-06, N2: el Analista la vuelve a proponer y responde bien
comprobar("3 · la semana de la respuesta buena es N2", r3["nivel_por_clase"].get(CLASE) == "N2", str(r3["nivel_por_clase"]), hallazgo=False)
f3_ = foto(b, r3)
proxy = b.almacen.estado("F3")[a[0]]["simbolo_seguimiento"]
nuevas = [k for k, x in b.almacen.estado("F3").items() if x.get("simbolo_seguimiento") == proxy and k in f3_["publicadas"]]
print(f"    semana 4: publicadas {f3_['publicadas']}; opción de {proxy} publicada como {nuevas}")
mal = [k for k in f3_["publicadas"] if fuerte_mal_resuelta(f3_["f3"][k]["fuertes"]) or any(x[4] and x[1] for x in f3_["f3"][k]["fuertes"])]
comprobar("3 · semana 4 (bien respondida): nada publicado con una fuerte mal resuelta ni con la reabierta dada por resuelta", not mal, str(mal))
comprobar("3 · semana 4: lo publicado con fuerte resuelta sale «especulativo»",
          all(c == "especulativo" for k, c in f3_["publicadas"].items() if f3_["f3"][k]["fuertes"]), str(f3_["publicadas"]))
comprobar("3 · semana 4: la reabierta no revive con su opp_id cerrado", a[0] not in f3_["publicadas"], f"{a[0]} → {nuevas}", hallazgo=False)
print("    integridad:", b.almacen.verificar_integridad() if hasattr(b.almacen, "verificar_integridad") else "-")
_ = pd
fin()
