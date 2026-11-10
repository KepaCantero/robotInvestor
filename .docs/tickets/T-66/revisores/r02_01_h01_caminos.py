"""T-66 · QA r02 · H-01: caminos que quedan para resolver una objeción fuerte sin evidencia ni confirmación concreta.

Invariante que se comprueba en cada escenario (README de T-66, PA-05): toda fuerte con `resuelta = true` en F3
  (a) tiene `evidencia_citada` no vacía y verificable para SU opción (fuente o CALC de la opción, o una referencia), y
  (b) se envió a la contrarréplica con el ref de SU opción y el Contradictor devolvió para ese id `resuelta: true`
      (sin otra entrada contradictoria para el mismo id).

Uso: PYTHONPATH=<ejecutor de A>:<revisores r01>:<revisores r02> python r02_01_h01_caminos.py
"""
import copy
import tempfile
from pathlib import Path

import pandas as pd

from r01_comun import AS_OF, Gancho, bloque, cfg, comprobar, fin, opciones_f3
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
from r01_comun import DATOS

CLASE = "RV"


def fuerte_extra(datos, ids=None, n=1):
    """Añade n fuertes a cada opción de la refutación; `ids` fija el id del modelo (p. ej. repetido)."""
    for x in datos["resultados"]:
        x["objeciones"] = [o for o in x["objeciones"] if o["fuerza"] != "fuerte"] + [
            {"id": (ids or f"OBJ-{x['ref']}-9{k}"), "tipo": "evidencia_insuficiente", "fuerza": "fuerte",
             "argumento": f"Forzada por QA {k}", "evidencia": "-", "que_la_resolveria": "Dos fuentes independientes"}
            for k in range(n)]
    return datos


def correr(analista, contr, refut=fuerte_extra, clases=(CLASE,), b=None, as_of=AS_OF):
    est = {"enviadas": [], "respuestas_contr": [], "pendientes": []}

    def g(agente, msg, datos):
        if agente == "AG-11" and msg.get("contrarreplicas"):
            est["enviadas"] += [(x["ref"], x["objecion_id"]) for x in msg["contrarreplicas"]]
            out = contr(msg, datos)
            if isinstance(out, dict):
                est["respuestas_contr"] += [x for x in out.get("resultados", []) if isinstance(x, dict)]
            return out
        if agente == "AG-11":
            return refut(datos)
        if msg.get("fase") == "RESPUESTA_OBJECIONES":
            est["pendientes"] += msg["objeciones"]
            return analista(msg, datos)
        return datos
    b = b or bloque(cliente=Gancho(g))
    r = b.ciclo(as_of, alcance={"clases": list(clases)})
    return b, r, est


def violaciones(b, est):
    """Fuertes resueltas que no cumplen (a) y (b)."""
    enviadas = set(est["enviadas"])
    por_id: dict = {}
    for x in est["respuestas_contr"]:
        por_id.setdefault(str(x.get("objecion_id")), []).append(x.get("resuelta"))
    malas = []
    for v in opciones_f3(b):
        for o in v.get("objeciones_internas") or []:
            if o["fuerza"] != "fuerte" or not o["resuelta"]:
                continue
            ok_a = bool(o.get("evidencia_citada"))
            ok_b = (v.get("simbolo_seguimiento"), o["objecion_id"]) in enviadas and por_id.get(o["objecion_id"]) \
                and all(r is True for r in por_id[o["objecion_id"]])
            if not (ok_a and ok_b):
                malas.append((v["opp_id"], v.get("simbolo_seguimiento"), o["objecion_id"], o.get("evidencia_citada"),
                              por_id.get(o["objecion_id"])))
    return malas


def confirma_lo_enviado(m, d):
    return {"resultados": [{"objecion_id": x["objecion_id"], "resuelta": True, "motivo": "QA"} for x in m["contrarreplicas"]]}


def n_fuertes(b, resuelta=None):
    return sum(1 for v in opciones_f3(b) for o in v.get("objeciones_internas") or []
               if o["fuerza"] == "fuerte" and (resuelta is None or o["resuelta"] is resuelta))


# 1 · El Analista responde con ids de OTRA opción, citando la evidencia de la opción propia
def analista_ids_cruzados(msg, datos):
    fu = [o for o in msg["objeciones"] if o["fuerza"] == "fuerte"]
    out = [{"objecion_id": o["objecion_id"], "respuesta": "Respondida", "resuelta": True} for o in msg["objeciones"] if o["fuerza"] != "fuerte"]
    for i, o in enumerate(fu):
        otra = fu[(i + 1) % len(fu)]
        out.append({"objecion_id": otra["objecion_id"], "respuesta": "Resuelta (id ajeno)", "resuelta": True,
                    "evidencia_citada": [e for e in (o.get("evidencia_disponible") or []) if not e.startswith("REF-")][:2]})
    return {"respuestas": out}


b, r, est = correr(analista_ids_cruzados, confirma_lo_enviado)
v = violaciones(b, est)
comprobar("ids de otra opción en la respuesta del Analista: ninguna fuerte resuelta sin (a)+(b)", not v,
          f"fuertes {n_fuertes(b)}, resueltas {n_fuertes(b, True)}, contrarréplicas {est['enviadas']}; violaciones {v}")

# 2 · Ids del modelo duplicados DENTRO de una opción (dos fuertes con «OBJ-01»): el Analista cita evidencia solo para una
def analista_solo_una_por_opcion(msg, datos):
    out, hechas = [], set()
    for o in msg["objeciones"]:
        if o["fuerza"] != "fuerte":
            out.append({"objecion_id": o["objecion_id"], "respuesta": "Respondida", "resuelta": True})
        elif o["ref"] not in hechas:
            hechas.add(o["ref"])
            out.append({"objecion_id": o["objecion_id"], "respuesta": "Resuelta", "resuelta": True,
                        "evidencia_citada": list(o.get("evidencia_disponible") or [])[:2]})
        else:
            out.append({"objecion_id": o["objecion_id"], "respuesta": "No la puedo resolver", "resuelta": False})
    return {"respuestas": out}


b, r, est = correr(analista_solo_una_por_opcion, confirma_lo_enviado, refut=lambda d: fuerte_extra(d, ids="OBJ-01", n=2))
ids = [o["objecion_id"] for v_ in opciones_f3(b) for o in v_.get("objeciones_internas") or []]
comprobar("ids del modelo duplicados en una opción: el código los distingue", len(ids) == len(set(ids)), f"{len(ids)} ids, {len(set(ids))} distintos")
opc = {v_["opp_id"]: [o["resuelta"] for o in v_.get("objeciones_internas") or [] if o["fuerza"] == "fuerte"] for v_ in opciones_f3(b)}
comprobar("ids del modelo duplicados en una opción: solo se resuelve la que tiene evidencia y confirmación",
          not violaciones(b, est) and all(sum(x) <= 1 for x in opc.values()), f"por opción {opc}")
pub = r["paquete"]["clases"][CLASE]["opciones"]
comprobar("ids del modelo duplicados en una opción: no se publica ninguna con una fuerte abierta", not pub, f"publicadas {[o['opp_id'] for o in pub]}")

# 2b · El Analista contesta con el id DEL MODELO (no el del código)
def analista_id_modelo(msg, datos):
    return {"respuestas": [{"objecion_id": "OBJ-01", "respuesta": "Resuelta", "resuelta": True,
                            "evidencia_citada": list(o.get("evidencia_disponible") or [])[:2]} for o in msg["objeciones"]]}


b, r, est = correr(analista_id_modelo, confirma_lo_enviado, refut=lambda d: fuerte_extra(d, ids="OBJ-01", n=1))
comprobar("el Analista responde con el id del modelo: no resuelve nada", n_fuertes(b, True) == 0 and not violaciones(b, est),
          f"resueltas {n_fuertes(b, True)}; contrarréplicas {est['enviadas']}")

# 3 · Contrarréplica con ids inventados, variantes de un id enviado y entradas raras
def analista_cita_una(msg, datos):
    """Cita evidencia solo para la PRIMERA fuerte del lote; las demás, sin resolver."""
    out, primera = [], None
    for o in msg["objeciones"]:
        if o["fuerza"] == "fuerte" and primera is None:
            primera = o["objecion_id"]
            out.append({"objecion_id": o["objecion_id"], "respuesta": "Resuelta", "resuelta": True,
                        "evidencia_citada": list(o.get("evidencia_disponible") or [])[:2]})
        else:
            out.append({"objecion_id": o["objecion_id"], "respuesta": "Respondida" if o["fuerza"] != "fuerte" else "No",
                        "resuelta": o["fuerza"] != "fuerte"})
    return {"respuestas": out}


def contr_ruido(m, d):
    env = [x["objecion_id"] for x in m["contrarreplicas"]]
    # ids con el formato del código que NO se enviaron (predecibles), variantes de mayúsculas y espacios del enviado
    refs = sorted({x["ref"] for x in m["contrarreplicas"]})
    inventados = [f"OBJ-{rf}-{nn:02d}" for rf in refs for nn in range(1, 6)] + [e.lower() for e in env] + [f" {e} " for e in env]
    return {"resultados": [{"objecion_id": i, "resuelta": True, "motivo": "QA"} for i in dict.fromkeys(inventados) if i not in env]
            + [{"objecion_id": e, "resuelta": False, "motivo": "QA: no basta"} for e in env]}


b, r, est = correr(analista_cita_una, contr_ruido, refut=lambda d: fuerte_extra(d, n=2))
comprobar("contrarréplica con ids inventados o variantes: no resuelve nada", n_fuertes(b, True) == 0,
          f"fuertes {n_fuertes(b)}, resueltas {n_fuertes(b, True)}; enviadas {est['enviadas']}")
comprobar("contrarréplica con ids inventados: nada publicado", not r["paquete"]["clases"][CLASE]["opciones"])


def contr_entradas_raras(m, d):
    return {"resultados": ["x", 5, None, {"objecion_id": ["OBJ"]}, {"resuelta": True},
                           {"objecion_id": m["contrarreplicas"][0]["objecion_id"], "resuelta": "true"}]}


b, r, est = correr(analista_cita_una, contr_entradas_raras)
comprobar("contrarréplica con entradas de tipo inesperado: el ciclo termina y la fuerte sigue abierta",
          n_fuertes(b, True) == 0, f"estado {r['estado']}; resueltas {n_fuertes(b, True)}")

# 4 · La contrarréplica se contradice para el MISMO id (dos entradas): falla cerrado si alguna dice que no
for orden in ((True, False), (False, True)):
    def contr_dup(m, d, orden=orden):
        return {"resultados": [{"objecion_id": x["objecion_id"], "resuelta": v, "motivo": f"QA {v}"}
                               for x in m["contrarreplicas"] for v in orden]}
    b, r, est = correr(analista_cita_una, contr_dup)
    comprobar(f"contrarréplica con el mismo id dos veces {orden}: la fuerte sigue abierta (falla cerrado)",
              n_fuertes(b, True) == 0, f"resueltas {n_fuertes(b, True)}; violaciones {violaciones(b, est)}")

# 5 · Dos tipos de activo con el mismo proxy (mismo símbolo en RV y en INM): los ids de una clase no resuelven la otra
tmp = Path(tempfile.mkdtemp(prefix="r02_"))
uni = pd.read_csv(RUTA_UNIVERSO_EJEMPLO)
fila = uni[uni["simbolo"] == "XLU"].copy() if (uni["simbolo"] == "XLU").any() else uni[uni["clase"] == "RV"].head(1).copy()
sym = str(fila["simbolo"].iloc[0])
fila["clase"] = "INM"
ruta = tmp / "universo_dup.csv"
pd.concat([uni, fila]).to_csv(ruta, index=False)
try:
    universo = cargar_universo(ruta)
    dup_ok = (universo["simbolo"] == sym).sum() == 2
except Exception as e:  # noqa: BLE001
    universo, dup_ok = None, False
    comprobar("dos tipos con el mismo proxy: el universo lo rechaza al cargar (camino cerrado)", True, f"{type(e).__name__}: {e}")
if universo is not None:
    def analista_sym(msg, datos):
        out = []
        for o in msg["objeciones"]:
            if o["fuerza"] == "fuerte" and o["ref"] == sym and msg["clase"] == "RV":
                out.append({"objecion_id": o["objecion_id"], "respuesta": "Resuelta", "resuelta": True,
                            "evidencia_citada": list(o.get("evidencia_disponible") or [])[:2]})
            else:
                out.append({"objecion_id": o["objecion_id"], "respuesta": "Respondida" if o["fuerza"] != "fuerte" else "No",
                            "resuelta": o["fuerza"] != "fuerte"})
        return {"respuestas": out}
    est5 = {"enviadas": [], "respuestas_contr": []}
    contr_vistos = []

    def g5(agente, msg, datos):
        if agente == "AG-11" and msg.get("contrarreplicas"):
            contr_vistos.append([(x["ref"], x["objecion_id"]) for x in msg["contrarreplicas"]])
            ids_ = [x["objecion_id"] for x in msg["contrarreplicas"]]
            return {"resultados": [{"objecion_id": i, "resuelta": True, "motivo": "QA"} for i in ids_]}
        if agente == "AG-11":
            return fuerte_extra(datos)
        if msg.get("fase") == "RESPUESTA_OBJECIONES":
            return analista_sym(msg, datos)
        if msg.get("fase") == "CRIBADO_E_INVESTIGACION" and isinstance(datos, dict) and msg.get("clase") in ("RV", "INM"):
            # que ambos tipos propongan el símbolo compartido como finalista
            fins = datos.get("finalistas") or []
            if fins and not any((f.get("indicador_seguimiento") or {}).get("simbolo") == sym or f.get("proxy") == sym for f in fins):
                f0 = copy.deepcopy(fins[0])
                f0["proxy"] = sym
                f0["indicador_seguimiento"] = {**(f0.get("indicador_seguimiento") or {}), "simbolo": sym}
                datos["finalistas"] = [f0] + fins
        return datos
    tmp2 = Path(tempfile.mkdtemp(prefix="r02_"))
    b5 = Bloque(cfg(), ProveedorCSV(DATOS), universo, Gancho(g5), tmp2 / "estado", tmp2 / "ent")
    r5 = b5.ciclo(AS_OF, alcance={"clases": ["RV", "INM"]})
    por_clase = {}
    for v_ in opciones_f3(b5):
        if v_.get("simbolo_seguimiento") == sym:
            por_clase[v_["clase"]] = [(o["objecion_id"], o["resuelta"], bool(o.get("evidencia_citada")))
                                      for o in v_.get("objeciones_internas") or [] if o["fuerza"] == "fuerte"]
    inm_mal = [x for x in por_clase.get("INM", []) if x[1] and not x[2]]
    comprobar(f"dos tipos con el mismo proxy ({sym} en RV e INM): la resolución de RV no resuelve la fuerte de INM",
              not inm_mal, f"universo duplicado cargado={dup_ok}; fuertes por clase {por_clase}; contrarréplicas {contr_vistos}")
    pub5 = {c: [o["opp_id"] for o in r5["paquete"]["clases"].get(c, {}).get("opciones", [])] for c in ("RV", "INM")}
    print(f"    publicadas {pub5}; estado {r5['estado']}")

# 6 · Determinismo de los ids asignados por el código
b1, r1, _ = correr(analista_cita_una, confirma_lo_enviado, refut=lambda d: fuerte_extra(d, ids="OBJ-01", n=2))
b2, r2, _ = correr(analista_cita_una, confirma_lo_enviado, refut=lambda d: fuerte_extra(d, ids="OBJ-01", n=2))
o1 = [(v_["opp_id"], o["objecion_id"], o["resuelta"]) for v_ in opciones_f3(b1) for o in v_.get("objeciones_internas") or []]
o2 = [(v_["opp_id"], o["objecion_id"], o["resuelta"]) for v_ in opciones_f3(b2) for o in v_.get("objeciones_internas") or []]
comprobar("determinismo: mismos ids y misma resolución en dos ejecuciones", o1 == o2 and bool(o1), f"{len(o1)} objeciones")

fin()
