"""T-66 · QA r04 · qué cuenta como «evidencia citada verificable» tras la corrección de H-15 (solo la de la propia opción).

A · Las REF- que aporta AG-14 en las piezas de la opción siguen siendo citables y resuelven con la confirmación (no regresión).
B · Las piezas del Analista llevan una `fuente` de texto libre (esquema FINALISTA): ¿puede el Analista meter como fuente de
    una afirmación suya una REF- posterior a as_of (backtest), una REF- de otro tema, un id inventado o el HT-01 de otro
    símbolo, y después citarla para resolver una fuerte?
C · AG-14 devuelve una REF- registrada que no estaba entre sus candidatas y es posterior a as_of en backtest: ¿entra como pieza
    (y, por tanto, como evidencia citable)? El comentario del código dice «solo referencias registradas y anteriores a as_of».
D · Lo mismo que A con el cliente con conocimiento previo (anonimización de PA-09).

Uso: PYTHONPATH=<ejecutor de A>:<revisores r01> python r04_01_evidencia_citable.py   (imprime OK / HALLAZGO / INFO)
"""
from r01_comun import Gancho, bloque, comprobar, fin
from bloque_a.referencias import TEMATICAS_CLASE

CLASE = "RV"
cap: dict = {}


def fuertes_f3(b):
    return [o for v in b.almacen.estado("F3").values() for o in (v.get("objeciones_internas") or []) if o["fuerza"] == "fuerte"]


def fabrica(citar, afirmacion_extra=None, ag14=None, todas_peticion=True):
    """citar(objecion, ag14_refs) -> lista de ids que cita el Analista."""
    def g(agente, msg, datos):
        if agente == "AG-14":
            if ag14:
                datos = ag14(msg, datos)
            cap.setdefault("ag14", []).extend(r["ref_id"] for r in datos.get("referencias", []))
            return datos
        if agente == "AG-11" and msg.get("contrarreplicas"):
            cap.setdefault("cr", []).extend(msg["contrarreplicas"])
            return datos                                   # el simulado confirma si ve ≥ 2 ids distintos
        if agente == "AG-11":
            for x in datos["resultados"]:
                x["objeciones"] = [o for o in x["objeciones"] if o["fuerza"] != "fuerte"] + [
                    {"id": "Z", "tipo": "evidencia_insuficiente", "fuerza": "fuerte", "argumento": "QA r04", "evidencia": "-",
                     "que_la_resolveria": "Dos fuentes"}]
            return datos
        if msg.get("fase") == "RESPUESTA_OBJECIONES":
            cap.setdefault("disp", {}).update({o["objecion_id"]: o.get("evidencia_disponible") for o in msg["objeciones"]})
            return {"respuestas": [{"objecion_id": o["objecion_id"], "respuesta": "Resuelta con la evidencia citada", "resuelta": True,
                                    "evidencia_citada": citar(o, cap.get("ag14", []))} for o in msg["objeciones"]]}
        if isinstance(datos, dict) and datos.get("finalistas"):
            if todas_peticion and msg.get("referencias_disponibles"):
                f0 = datos["finalistas"][0]
                f0["peticiones_conocimiento"] = [{"tipo": "CT-08", "pregunta": "¿Persistencia del impulso?", "objetivo": "confirmar",
                                                  "para": f0["indicador_seguimiento"]["simbolo"]}]
            if afirmacion_extra:
                for f in datos["finalistas"]:
                    f["afirmaciones"] = list(f["afirmaciones"]) + afirmacion_extra(f)
        return datos
    return g


# ================================================================ A · REF- de AG-14 citables
cap.clear()
b = bloque(cliente=Gancho(fabrica(lambda o, ag14: [r for r in ag14 if r in (o.get("evidencia_disponible") or [])][:2])))
r = b.ciclo("2026-06-05", alcance={"clases": [CLASE]})
ag14 = list(dict.fromkeys(cap.get("ag14", [])))
con_ag14 = [o for o in fuertes_f3(b) if len(o.get("evidencia_citada") or []) == 2]   # la opción que pidió a AG-14
print(f"    AG-14 aportó {ag14}; fuertes que citan sus REF- {[(o['objecion_id'], o['evidencia_citada'], o['resuelta']) for o in con_ag14]}")
comprobar("A · las REF- de AG-14 aparecen en la evidencia disponible de la opción que las pidió",
          any(set(ag14[:2]) <= set(d or []) for d in cap.get("disp", {}).values()), f"{len(ag14)} REF- de AG-14")
comprobar("A · citar dos REF- de AG-14 de la propia opción llega a la contrarréplica y, confirmada, resuelve la fuerte",
          bool(con_ag14) and all(o["resuelta"] and set(o["evidencia_citada"]) <= set(ag14) for o in con_ag14),
          f"contrarréplicas {[(x['objecion_id'], [e['tipo'] for e in x['evidencia_citada']]) for x in cap.get('cr', [])]}")
comprobar("A · el contenido de esas REF- llega a la contrarréplica (no un id vacío)",
          all(e.get("afirmacion") for x in cap.get("cr", []) for e in x["evidencia_citada"]))

# ================================================================ B · fuentes libres en las afirmaciones del Analista
AS_OF_BT = "2024-03-01"
fichas = b.referencias.fichas
tem = set(TEMATICAS_CLASE[CLASE])
futura = next(r for a in ("F7", "F8") for r in fichas[a] if (r["anio"] or 0) > 2024)
otro_tema = next(r for a in ("F7", "F8") for r in fichas[a] if r["tematica"] not in tem and (r["anio"] or 9999) <= 2024)
casos = {
    "REF- posterior a as_of (backtest)": f"REF-{futura['ref_id']}",
    "REF- de otro tema": f"REF-{otro_tema['ref_id']}",
    "id inventado": "REF-INVENTADA-0001",
    "HT-01 de otro símbolo": "HT-01:SPY",
}
for nombre, eid in casos.items():
    cap.clear()

    def extra(f, eid=eid):
        return [{"afirmacion": f"Dato que respalda la tesis de {f['indicador_seguimiento']['simbolo']}", "fuente": eid, "direccion": "favorable"}]

    def citar(o, _ag14, eid=eid):
        return [eid] + [e for e in (o.get("evidencia_disponible") or []) if e.startswith("HT-01:")][:1]

    bb = bloque(cliente=Gancho(fabrica(citar, afirmacion_extra=extra, todas_peticion=False)))
    rr = bb.ciclo(AS_OF_BT, alcance={"clases": [CLASE]})
    fu = fuertes_f3(bb)
    acept = [o for o in fu if eid in (o.get("evidencia_citada") or [])]
    res = [o for o in acept if o["resuelta"]]
    pub = [(o["opp_id"], o["confianza"]) for o in rr["paquete"]["clases"][CLASE]["opciones"]]
    comprobar(f"B · {nombre} puesto por el Analista como fuente de su afirmación no es evidencia citable",
              not acept, f"{eid}: aceptada en {len(acept)}/{len(fu)} fuertes, {len(res)} resueltas con ella; publicadas {pub}")

# ================================================================ C · AG-14 con una REF- futura no ofrecida
cap.clear()


def ag14_futura(msg, datos):
    datos["referencias"] = [{"ref_id": f"REF-{futura['ref_id']}", "afirmacion": "Estudio posterior que confirma la tesis",
                             "direccion": "favorable", "motivo": "QA r04"}] + datos.get("referencias", [])[:1]
    return datos


bc = bloque(cliente=Gancho(fabrica(lambda o, ag14: [f"REF-{futura['ref_id']}"] + [e for e in (o.get("evidencia_disponible") or [])
                                                                              if e.startswith("HT-01:")][:1], ag14=ag14_futura)))
rc = bc.ciclo(AS_OF_BT, alcance={"clases": [CLASE]})
cand_ofrecidas = bc.referencias.para_clase(CLASE, AS_OF_BT, "backtest", max_n=8, archivos=("F7",))["referencias"]
fu = fuertes_f3(bc)
acept = [o for o in fu if f"REF-{futura['ref_id']}" in (o.get("evidencia_citada") or [])]
comprobar("C · en backtest, una REF- posterior a as_of devuelta por AG-14 (no estaba entre sus candidatas) no entra como pieza citable",
          not acept, f"REF-{futura['ref_id']} ({futura['anio']}); ofrecida a AG-14: "
                     f"{any(x['ref_id'] == 'REF-' + futura['ref_id'] for x in cand_ofrecidas)}; aceptada en {len(acept)}/{len(fu)} fuertes, "
                     f"{sum(1 for o in acept if o['resuelta'])} resueltas")

# ================================================================ D · con anonimización (conocimiento previo)
cap.clear()
bd = bloque(cliente=Gancho(fabrica(lambda o, ag14: [r for r in ag14 if r in (o.get("evidencia_disponible") or [])][:2]),
                           conocimiento_previo=True))
bd.ciclo(AS_OF_BT, alcance={"clases": [CLASE]})
con = [o for o in fuertes_f3(bd) if len(o.get("evidencia_citada") or []) == 2]
comprobar("D · con anonimización, las REF- de AG-14 siguen siendo citables y resuelven con la confirmación",
          bool(con) and all(o["resuelta"] for o in con), f"anonimizado {bool(bd.anon)}; {[(o['objecion_id'], o['evidencia_citada'], o['resuelta']) for o in con]}",
          hallazgo=True)
fin()
