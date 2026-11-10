"""T-66 · QA r01 · PA-05: contrarréplica que falla, ids no pedidos o repetidos, evidencia inventada o de otra opción.

Regla del plan (README de T-66 e INC-T66-02): una objeción fuerte queda resuelta SOLO si la respuesta del Analista cita
evidencia verificable Y el Contradictor lo confirma en una contrarréplica. Sin contrarréplica, sigue abierta.
"""
from r01_comun import AS_OF, Gancho, bloque, comprobar, fin, opciones_f3

CLASE = "RV"


def fuertes(b):
    return [(x["opp_id"], o) for x in opciones_f3(b) for o in (x.get("objeciones_internas") or []) if o["fuerza"] == "fuerte"]


def resueltas_sin_evidencia(b):
    return [(oid, o["objecion_id"]) for oid, o in fuertes(b) if o["resuelta"] and not o.get("evidencia_citada")]


def contradictor_con_fuerte(datos, id_fijo=None):
    for x in datos["resultados"]:
        x["objeciones"] = [o for o in x["objeciones"] if o["fuerza"] != "fuerte"] + [
            {"id": id_fijo or f"OBJ-{x['ref']}-09", "tipo": "evidencia_insuficiente", "fuerza": "fuerte",
             "argumento": "Forzada por QA", "evidencia": "-", "que_la_resolveria": "Dos fuentes independientes"}]
    return datos


def escenario(gancho_contr, gancho_analista, id_fijo=None):
    estado = {"refs": [], "contrarreplicas": []}

    def g(agente, msg, datos):
        if agente == "AG-11" and "contrarreplicas" in msg:
            estado["contrarreplicas"].append(msg["contrarreplicas"])
            return gancho_contr(msg, datos)
        if agente == "AG-11":
            estado["refs"] = [p["ref"] for p in msg["peticiones"]]
            return contradictor_con_fuerte(datos, id_fijo)
        if msg.get("fase") == "RESPUESTA_OBJECIONES":
            return gancho_analista(msg, datos, estado)
        return datos
    b = bloque(cliente=Gancho(g))
    r = b.ciclo(AS_OF, alcance={"clases": [CLASE]})
    return b, r, estado


# 1 · La contrarréplica devuelve un JSON no conforme (dos veces: también la reparación) → la fuerte sigue abierta
def analista_cita_2(msg, datos, estado):
    return {"respuestas": [{"objecion_id": o["objecion_id"], "respuesta": "Resuelta", "resuelta": True,
                            "evidencia_citada": list(o.get("evidencia_disponible") or [])[:2]} for o in msg["objeciones"]]}


b, r, est = escenario(lambda m, d: "esto no es JSON", analista_cita_2)
comprobar("contrarréplica no conforme: ninguna fuerte resuelta", bool(fuertes(b)) and not any(o["resuelta"] for _, o in fuertes(b)),
          f"{len(fuertes(b))} fuertes, contrarréplicas enviadas {len(est['contrarreplicas'])}")
comprobar("contrarréplica no conforme: nada publicado de la clase", not r["paquete"]["clases"][CLASE]["opciones"])

# 2 · La contrarréplica lanza una excepción del proveedor
try:
    def explota(m, d):
        raise RuntimeError("proveedor caído")
    b, r, est = escenario(explota, analista_cita_2)
    comprobar("contrarréplica con excepción: el ciclo sigue y la fuerte queda abierta",
              not any(o["resuelta"] for _, o in fuertes(b)), f"estado {r['estado']}")
except RuntimeError as e:
    comprobar("contrarréplica con excepción: la excepción sube y el ciclo no termina", False,
              f"{e} (comportamiento común a todos los agentes de A, anterior a T-66)", hallazgo=False)

# 3 · Evidencia inventada → no hay contrarréplica y sigue abierta
def analista_inventa(msg, datos, estado):
    return {"respuestas": [{"objecion_id": o["objecion_id"], "respuesta": "Resuelta", "resuelta": True,
                            "evidencia_citada": ["CALC-9999-INVENTADO", "HT-01:NO-EXISTE", "REF-ZZZ-999"]} for o in msg["objeciones"]]}


b, r, est = escenario(lambda m, d: {"resultados": [{"objecion_id": x["objecion_id"], "resuelta": True} for x in m["contrarreplicas"]]},
                      analista_inventa)
comprobar("evidencia inventada: no se pide contrarréplica", est["contrarreplicas"] == [])
comprobar("evidencia inventada: ninguna fuerte resuelta", not any(o["resuelta"] for _, o in fuertes(b)))

# 4 · Evidencia de OTRA opción → se filtra (solo cuenta la verificable de la propia finalista)
def analista_cita_de_otra(msg, datos, estado):
    por_ref = {o["ref"]: list(o.get("evidencia_disponible") or []) for o in msg["objeciones"]}
    refs = sorted(por_ref)
    out = []
    for o in msg["objeciones"]:
        otra = next((r for r in refs if r != o["ref"]), o["ref"])
        ajena = [e for e in por_ref[otra] if e not in por_ref[o["ref"]]][:2]
        out.append({"objecion_id": o["objecion_id"], "respuesta": "Resuelta", "resuelta": True, "evidencia_citada": ajena})
    return {"respuestas": out}


b, r, est = escenario(lambda m, d: {"resultados": [{"objecion_id": x["objecion_id"], "resuelta": True} for x in m["contrarreplicas"]]},
                      analista_cita_de_otra)
citas = [e["id"] for lote in est["contrarreplicas"] for x in lote for e in x["evidencia_citada"]]
comprobar("evidencia de otra opción: filtrada (no llega a la contrarréplica ni resuelve)",
          not any(o["resuelta"] for _, o in fuertes(b)), f"ids que llegaron a la contrarréplica: {citas[:4]}")

# 5 · La contrarréplica «resuelve» ids que NO se le pidieron (objeción con resuelta=false y sin evidencia del Analista)
def analista_solo_la_primera(msg, datos, estado):
    out = []
    for k, o in enumerate(msg["objeciones"]):
        if o["fuerza"] != "fuerte":   # las moderadas se responden (así G2 depende solo de la fuerte)
            out.append({"objecion_id": o["objecion_id"], "respuesta": "Respondida con los datos HT-01", "resuelta": True})
            continue
        if not any(x.get("evidencia_citada") for x in out):   # la primera fuerte: cita evidencia; las demás: «no resuelta», sin evidencia
            out.append({"objecion_id": o["objecion_id"], "respuesta": "Resuelta con la evidencia citada", "resuelta": True,
                        "evidencia_citada": list(o.get("evidencia_disponible") or [])[:2]})
        else:
            out.append({"objecion_id": o["objecion_id"], "respuesta": "No la puedo resolver", "resuelta": False, "evidencia_citada": []})
    return {"respuestas": out}


def contr_resuelve_todo(m, d, estado_ref=[]):
    pedidos = [x["objecion_id"] for x in m["contrarreplicas"]]
    extra = [f"OBJ-{r}-09" for r in ESTADO["refs"]]
    return {"resultados": [{"objecion_id": i, "resuelta": True, "motivo": "QA"} for i in dict.fromkeys(pedidos + extra + ["OBJ-DESCONOCIDA"])]}


ESTADO = {"refs": []}


def g_refs(agente, msg, datos):
    return datos


b, r, est = None, None, None


def escenario5():
    global ESTADO
    estado = {"refs": [], "contrarreplicas": []}
    ESTADO = estado

    def g(agente, msg, datos):
        if agente == "AG-11" and "contrarreplicas" in msg:
            estado["contrarreplicas"].append([x["objecion_id"] for x in msg["contrarreplicas"]])
            return contr_resuelve_todo(msg, datos)
        if agente == "AG-11":
            estado["refs"] = [p["ref"] for p in msg["peticiones"]]
            return contradictor_con_fuerte(datos)
        if msg.get("fase") == "RESPUESTA_OBJECIONES":
            return analista_solo_la_primera(msg, datos, estado)
        return datos
    bb = bloque(cliente=Gancho(g))
    rr = bb.ciclo(AS_OF, alcance={"clases": [CLASE]})
    return bb, rr, estado


b, r, est = escenario5()
for x in opciones_f3(b):
    for o in x.get("objeciones_internas") or []:
        if o["fuerza"] == "fuerte":
            print(f"    {x['opp_id']} {o['objecion_id']} resuelta={o['resuelta']} evidencia={o.get('evidencia_citada')} "
                  f"respuesta={o.get('respuesta')!r} contrarreplica={o.get('contrarreplica')!r} elegible={x.get('elegible')}")
pedidas = {i for lote in est["contrarreplicas"] for i in lote}
indebidas = [(oid, o["objecion_id"]) for oid, o in fuertes(b) if o["resuelta"] and o["objecion_id"] not in pedidas]
publicadas = [o["opp_id"] for o in r["paquete"]["clases"][CLASE]["opciones"]]
comprobar("contrarréplica con ids no pedidos: no resuelve objeciones que no se le enviaron", not indebidas,
          f"pedidas a la contrarréplica {sorted(pedidas)}; resueltas sin pedirse {indebidas}; publicadas {publicadas}")
comprobar("ninguna fuerte resuelta sin evidencia citada por el Analista", not resueltas_sin_evidencia(b),
          f"{resueltas_sin_evidencia(b)}; entrega {r.get('entrega', 'ENTREGADA')} (estado {r['estado']}; F3 {sorted({v.get('estado') for v in b.almacen.estado('F3').values()})})")

# 6 · Ids de objeción repetidos entre opciones (el modelo usa «OBJ-01» para todas): la evidencia y la confirmación de UNA
#     opción no pueden resolver las fuertes de las demás
def analista_ids_repetidos(msg, datos, estado):
    fuertes_msg = [o for o in msg["objeciones"] if o["fuerza"] == "fuerte"]
    propias = {o["ref"]: set(o.get("evidencia_disponible") or []) for o in fuertes_msg}
    a = fuertes_msg[0]
    unica = [e for e in (a.get("evidencia_disponible") or []) if not any(e in v for r, v in propias.items() if r != a["ref"])][:2]
    estado["unica"] = (a["ref"], unica)
    out = [{"objecion_id": o["objecion_id"], "respuesta": "Respondida con los datos HT-01", "resuelta": True}
           for o in msg["objeciones"] if o["fuerza"] != "fuerte"]
    out.append({"objecion_id": a["objecion_id"], "respuesta": "Resuelta con la evidencia citada de esta opción", "resuelta": True,
                "evidencia_citada": unica})
    return {"respuestas": out}


def contradictor_ids_repetidos(datos):
    for x in datos["resultados"]:
        x["objeciones"] = [{"id": "OBJ-01", "tipo": "explicacion_alternativa", "fuerza": "moderada", "argumento": "Rebote técnico",
                            "evidencia": "-", "que_la_resolveria": "Confirmación"},
                           {"id": "OBJ-02", "tipo": "evidencia_insuficiente", "fuerza": "fuerte", "argumento": "Forzada por QA",
                            "evidencia": "-", "que_la_resolveria": "Dos fuentes independientes"}]
    return datos


est6 = {"contrarreplicas": []}


def g6(agente, msg, datos):
    if agente == "AG-11" and "contrarreplicas" in msg:
        est6["contrarreplicas"].append([(x["ref"], x["objecion_id"]) for x in msg["contrarreplicas"]])
        return {"resultados": [{"objecion_id": x["objecion_id"], "resuelta": True, "motivo": "QA"} for x in msg["contrarreplicas"]]}
    if agente == "AG-11":
        return contradictor_ids_repetidos(datos)
    if msg.get("fase") == "RESPUESTA_OBJECIONES":
        return analista_ids_repetidos(msg, datos, est6)
    return datos


b = bloque(cliente=Gancho(g6))
r = b.ciclo(AS_OF, alcance={"clases": [CLASE]})
f3 = b.almacen.estado("F3")
pub = [(o["opp_id"], f3.get(o["opp_id"], {}).get("proxy") or "?") for o in r["paquete"]["clases"][CLASE]["opciones"]]
sin_ev = [(oid, o["objecion_id"]) for oid, o in fuertes(b) if o["resuelta"] and not o.get("evidencia_citada")]
print(f"    evidencia única citada: {est6.get('unica')}; contrarréplicas pedidas {est6['contrarreplicas']}")
comprobar("ids repetidos entre opciones: la confirmación de una opción no resuelve las fuertes de las demás", not sin_ev,
          f"resueltas sin evidencia {sin_ev}; entrega {r.get('entrega', 'ENTREGADA')} (estado {r['estado']}; F3 {sorted({v.get('estado') for v in b.almacen.estado('F3').values()})}); publicadas {[p for p, _ in pub]}")

# 7 · El Contradictor falla en la refutación: ninguna elegible; ¿queda el veredicto por regla registrado?
def g7(agente, msg, datos):
    if agente == "AG-11":
        return "no conforme"
    return datos


b = bloque(cliente=Gancho(g7))
r = b.ciclo(AS_OF, alcance={"clases": [CLASE]})
comprobar("sin refutación: nada elegible en N2", not r["paquete"]["clases"][CLASE]["opciones"])
ver = {x.get("veredicto_refutacion") for x in opciones_f3(b)}
comprobar("sin refutación: veredicto por regla registrado en F3", ver != {None}, f"veredictos en F3: {ver}", hallazgo=False)

fin()
