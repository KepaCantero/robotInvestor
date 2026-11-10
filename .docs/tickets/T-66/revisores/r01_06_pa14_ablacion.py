"""T-66 · QA r01 · PA-14: ablación con 0 candidatos, con el Analista caído, y coherencia de la variante «sin objeciones»."""
from r01_comun import AS_OF, Gancho, bloque, comprobar, fin, ultimo_run

from bloque_a import mock_respuestas as mr


def g_vacio(agente, msg, datos):
    if agente in mr.ANALISTAS_MOCK and msg.get("fase") not in ("RESPUESTA_OBJECIONES",) and isinstance(datos, dict) and "finalistas" in datos:
        datos["finalistas"] = []
        if "cribado" in datos:
            datos["cribado"] = []
    return datos


def g_caido(agente, msg, datos):
    if agente in mr.ANALISTAS_MOCK:
        return "no conforme"
    return datos


for nombre, g in (("0 candidatos", g_vacio), ("Analista caído", g_caido)):
    try:
        b = bloque(cliente=Gancho(g))
        r = b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
        abl = (ultimo_run(b).get("ablacion") or {}).get("DIV")
        ok = abl is None or (abl["top3"] == [] and abl["sin_objeciones"]["top3"] == [] and abl["sin_objeciones"]["cambia_decision"] is False)
        comprobar(f"ablación con {nombre}: no falla y no inventa decisiones", ok, f"estado {r['estado']}; ablación {abl}")
    except Exception as e:   # noqa: BLE001
        comprobar(f"ablación con {nombre}: no falla y no inventa decisiones", False, f"{type(e).__name__}: {e}"[:160])

# Variante «sin objeciones»: ¿quita también el efecto de las objeciones en la dimensión E (objeciones_respondidas)?
b = bloque()
orig = b._ablacion
capt = {}


def esp(an, candidatos, entradas, sel, n):
    capt["entradas"] = entradas
    return orig(an, candidatos, entradas, sel, n)


b._ablacion = esp
b.ciclo(AS_OF, alcance={"clases": ["RV"]})
ent = capt.get("entradas") or []
con_efecto = [e["opp_id"] for e in ent if isinstance((e["dimensiones"].get("E") or {}).get("objeciones_respondidas"), int)
              and e["dimensiones"]["E"]["objeciones_respondidas"] < 100]
comprobar("«sin objeciones» neutraliza también objeciones_respondidas en E", not con_efecto,
          f"{len(con_efecto)} de {len(ent)} entradas conservan E.objeciones_respondidas < 100 en la variante", hallazgo=False)
fin()
