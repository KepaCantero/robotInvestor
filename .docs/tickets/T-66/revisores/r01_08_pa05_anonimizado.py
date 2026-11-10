"""T-66 · QA r01 · PA-05 con anonimización (backtest con modelo real): la evidencia citada con símbolos anonimizados
debe seguir siendo verificable al volver a los símbolos reales, y llegar anonimizada al Contradictor."""
import json

from r01_comun import AS_OF, Gancho, bloque, comprobar, fin, opciones_f3

vistos = {"disp": [], "contr": []}


def g(agente, msg, datos):
    if agente == "AG-11" and "contrarreplicas" in msg:
        vistos["contr"].append(json.dumps(msg["contrarreplicas"], ensure_ascii=False))
        return {"resultados": [{"objecion_id": x["objecion_id"], "resuelta": True, "motivo": "QA"} for x in msg["contrarreplicas"]]}
    if agente == "AG-11":
        for x in datos["resultados"]:
            x["objeciones"] = [o for o in x["objeciones"] if o["fuerza"] != "fuerte"] + [
                {"id": f"OBJ-{x['ref']}-09", "tipo": "evidencia_insuficiente", "fuerza": "fuerte", "argumento": "Forzada por QA",
                 "evidencia": "-", "que_la_resolveria": "Dos fuentes"}]
        return datos
    if msg.get("fase") == "RESPUESTA_OBJECIONES":
        vistos["disp"] += [e for o in msg["objeciones"] for e in (o.get("evidencia_disponible") or [])]
        return {"respuestas": [{"objecion_id": o["objecion_id"], "respuesta": "Resuelta con la evidencia citada", "resuelta": True,
                                "evidencia_citada": list(o.get("evidencia_disponible") or [])[:2]} for o in msg["objeciones"]]}
    return datos


b = bloque(cliente=Gancho(g, conocimiento_previo=True))
comprobar("backtest con modelo real: anonimizado", b.anon is not None)
b.ciclo(AS_OF, alcance={"clases": ["RV"]})
reales = set(b.universo["simbolo"]) if hasattr(b, "universo") else set()
fuga = [e for e in vistos["disp"] if any(f"HT-01:{s}" == e for s in reales)]
comprobar("la evidencia disponible llega anonimizada al Analista", not fuga, f"{len(fuga)} ids con símbolo real, p. ej. {fuga[:2]}")
fuga_c = [s for s in reales if any(f'"HT-01:{s}"' in c for c in vistos["contr"])]
comprobar("la contrarréplica llega anonimizada al Contradictor", not fuga_c, f"símbolos reales vistos {fuga_c[:3]}")
fuertes = [o for x in opciones_f3(b) for o in (x.get("objeciones_internas") or []) if o["fuerza"] == "fuerte"]
comprobar("con anonimización, la evidencia citada se verifica y la fuerte se resuelve en contrarréplica",
          bool(vistos["contr"]) and fuertes and all(o["resuelta"] and o.get("evidencia_citada") for o in fuertes),
          f"contrarréplicas {len(vistos['contr'])}; fuertes resueltas {sum(1 for o in fuertes if o['resuelta'])}/{len(fuertes)}; "
          f"evidencia en F3 {[o.get('evidencia_citada') for o in fuertes][:2]}")
fin()
