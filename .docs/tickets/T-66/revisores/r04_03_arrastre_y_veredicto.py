"""T-66 · QA r04 · normalización del arrastre (`_objeciones_arrastre`) y veredicto «más estricto» (corrección de H-17).

1 · Las objeciones escritas por el código (fuerte bien resuelta, moderada respondida, débil) pasan por el arrastre sin cambios,
    y la normalización es idempotente. Una contrarréplica confirmada sin `motivo` (se guarda "") no reabre la fuerte.
2 · Tres semanas de arrastre de una frágil bien resuelta: sigue publicada, «especulativo», sin `reabierta_por`.
3 · «Más estricto» no bloquea para siempre: una vigente frágil que vuelve a ser finalista (N2) y se refuta con éxito (sin fuertes
    ni moderadas suficientes) pasa a «tesis robusta»; y en el arrastre siguiente sigue robusta (no revive el «frágil» antiguo).
4 · Veredicto guardado de tipo raro (lista, dict, número): sin excepción y gana la regla.

Uso: PYTHONPATH=<ejecutor de A>:<revisores r01> python r04_03_arrastre_y_veredicto.py   (imprime OK / HALLAZGO / INFO)
"""
import copy

from r01_comun import Gancho, bloque, comprobar, fin
from bloque_a.orquestacion import Bloque

CLASE = "RV"
SEM = ["2026-06-05", "2026-06-12", "2026-06-19", "2026-06-26", "2026-07-03"]
estado = {"modo": "alta"}


def g(agente, msg, datos):
    m = estado["modo"]
    if agente == "AG-11" and msg.get("contrarreplicas"):
        if m == "sin_motivo":
            return {"resultados": [{"objecion_id": x["objecion_id"], "resuelta": True} for x in msg["contrarreplicas"]]}
        return datos
    if agente == "AG-11":
        for x in datos["resultados"]:
            if m == "limpia":      # refutación con éxito: solo una débil
                x["objeciones"] = [{"id": "D", "tipo": "otro", "fuerza": "debil", "argumento": "Menor", "evidencia": "-", "que_la_resolveria": "-"}]
                x["veredicto_global"] = "tesis robusta"
            else:
                x["objeciones"] = [o for o in x["objeciones"] if o["fuerza"] != "fuerte"] + [
                    {"id": "Z", "tipo": "evidencia_insuficiente", "fuerza": "fuerte", "argumento": "QA r04", "evidencia": "-",
                     "que_la_resolveria": "Dos fuentes"},
                    {"id": "W", "tipo": "otro", "fuerza": "debil", "argumento": "Menor", "evidencia": "-", "que_la_resolveria": "-"}]
        return datos
    if msg.get("fase") == "RESPUESTA_OBJECIONES":
        return {"respuestas": [{"objecion_id": o["objecion_id"], "respuesta": "Resuelta con la evidencia citada", "resuelta": True,
                                "evidencia_citada": list(o.get("evidencia_disponible") or [])[:2]} for o in msg["objeciones"]]}
    if m == "arrastre" and isinstance(datos, dict) and "finalistas" in datos:
        datos["finalistas"] = []
    return datos


def foto(b, r):
    f3 = {v["opp_id"]: v for v in b.almacen.estado("F3").values()}
    pub = {o["opp_id"]: o["confianza"] for o in r["paquete"]["clases"][CLASE]["opciones"]}
    return f3, pub


# 1 · objeciones del código, sin cambios e idempotentes
for modo in ("alta", "sin_motivo"):
    estado["modo"] = modo
    b = bloque(cliente=Gancho(g))
    r = b.ciclo(SEM[0], alcance={"clases": [CLASE]})
    f3, pub = foto(b, r)
    objs = [o for v in f3.values() if v["opp_id"] in pub for o in v["objeciones_internas"]]
    norm = Bloque._objeciones_arrastre(copy.deepcopy(objs))
    comprobar(f"1 · «{modo}»: las objeciones escritas por el código pasan el arrastre sin cambios",
              bool(objs) and norm == objs, f"{len(objs)} objeciones de {len(pub)} publicadas; fuerzas {sorted({o['fuerza'] for o in objs})}; "
                                          f"contrarréplicas {sorted({repr(o.get('contrarreplica')) for o in objs if o['fuerza'] == 'fuerte'})}")
    comprobar(f"1 · «{modo}»: normalizar dos veces da lo mismo", Bloque._objeciones_arrastre(norm) == norm)

# 2 · tres semanas de arrastre
estado["modo"] = "alta"
b = bloque(cliente=Gancho(g))
r = b.ciclo(SEM[0], alcance={"clases": [CLASE]})
f3, pub0 = foto(b, r)
print("    semana 1:", pub0, {k: f3[k]["veredicto_refutacion"] for k in pub0})
estado["modo"] = "arrastre"
for s in SEM[1:4]:
    b.cliente = Gancho(g)
    r = b.ciclo(s, alcance={"clases": [CLASE]})
    f3, pub = foto(b, r)
    reab = [o for k in pub0 for o in f3[k]["objeciones_internas"] if o.get("reabierta_por")]
    comprobar(f"2 · {s} ({r['nivel_por_clase'].get(CLASE)}): las frágiles bien resueltas siguen publicadas, «especulativo», sin reabrir",
              set(pub) == set(pub0) and all(c == "especulativo" for c in pub.values()) and not reab
              and all(f3[k]["veredicto_refutacion"] == "tesis frágil" for k in pub0), f"{pub}; reabiertas {len(reab)}")

# 3 · vigente frágil que se vuelve a refutar con éxito
estado["modo"] = "limpia"
b.cliente = Gancho(g)
r = b.ciclo(SEM[4], alcance={"clases": [CLASE]}, nivel_forzado="N2")
f3, pub = foto(b, r)
mismos = [k for k in pub0 if k in pub]
print(f"    {SEM[4]} (N2 forzado, refutación limpia): {pub}; veredictos {[(k, f3[k]['veredicto_refutacion']) for k in pub0 if k in f3]}")
comprobar("3 · la re-finalista refutada con éxito pasa a «tesis robusta» (el «frágil» guardado no la bloquea)",
          bool(mismos) and all(f3[k]["veredicto_refutacion"] == "tesis robusta" for k in mismos)
          and all(pub[k] != "especulativo" for k in mismos), f"mismas opp_id publicadas {mismos}")
estado["modo"] = "arrastre"
b.cliente = Gancho(g)
r = b.ciclo("2026-07-10", alcance={"clases": [CLASE]})
f3, pub = foto(b, r)
comprobar("3 · en el arrastre siguiente sigue «tesis robusta» y no vuelve a «especulativo»",
          bool(mismos) and all(f3[k]["veredicto_refutacion"] == "tesis robusta" and pub.get(k) not in (None, "especulativo") for k in mismos),
          f"{r['nivel_por_clase'].get(CLASE)}; {pub}")

# 4 · veredicto guardado de tipo raro
for raro in (["tesis refutada"], {"v": 1}, 3, "Tesis Refutada", "tesis refutada "):
    try:
        v = Bloque._veredicto_mas_estricto(raro, "tesis frágil")
        comprobar(f"4 · veredicto guardado {raro!r}: sin excepción y gana la regla", v == "tesis frágil", repr(v))
    except Exception as ex:  # noqa: BLE001
        comprobar(f"4 · veredicto guardado {raro!r}: sin excepción", False, f"{type(ex).__name__}: {ex}")
fin()
