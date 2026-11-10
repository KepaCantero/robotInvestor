"""QA r01 · sonda 05: integridad de lo nuevo. ¿Detecta integridad() cualquier toque al rastro SC-5 (también borrarlo o recortarlo),
a los campos nuevos de un expediente DIRECTA (por C, D y E) y a los campos nuevos puestos en un expediente que no es DIRECTA?"""
import copy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, chk, descartado_por_operador, enc_directa, fin, hasta, nuevo  # noqa: E402

MOT = "solo hay un candidato en la cartera: lo pidió el operador"
o = nuevo()
descartado_por_operador(o, 1)
hasta(o, "VALIDADA", 3)
CB = {"consulta_id": "CON-0001", "correlation_id": "COR-CON-0001", "tipo": "COMPARAR", "bloque": "D", "cartera": "TACTICA",
      "analisis": ["EV-SOB-0001", "EV-SOB-0003"], "pregunta": "¿Cuál de estos análisis rinde más que el benchmark?"}
assert o.consultar(CB, "BROKER", AHORA)["ok"]
assert o.consultar({**CB, "consulta_id": "CON-0002", "tipo": "ANALIZAR", "bloque": "C", "analisis": ["EV-SOB-0001"]}, "BROKER", AHORA)["ok"]
assert o.descartar("EXP-0003", "el operador lo aparta", "OPERADOR", AHORA)["ok"]
assert o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001", consulta_id="CON-0001")["ok"]
assert o.abrir_directa("EXP-DE-03", "COR-DE-03", "TACTICA", "E", "BROKER", AHORA, analisis="EV-SOB-0003", motivo=MOT)["ok"] is False   # DD-01 está vivo
assert o.abrir_directa("EXP-DC-05", "COR-EXP-DC-05", "TACTICA", "C", "BROKER", AHORA, encargo=enc_directa("EXP-DC-05", 5), consulta_id="CON-0002")["ok"]
assert o.integridad() == [], o.integridad()
print("rastro SC-5:", [(x["tipo"], x["consulta_id"]) for x in o.consultas["entradas"]])


def toca(nombre, f, se_espera):
    o2 = copy.deepcopy(o)
    f(o2)
    i = o2.integridad()
    chk(nombre, (se_espera in i) if se_espera else True, i)
    return o2, i


# rastro SC-5
toca("SC5_cambiar_pregunta", lambda x: x.consultas["entradas"][0]["consulta"].__setitem__("pregunta", "otra pregunta distinta de la buena"), "CONSULTAS")
toca("SC5_cambiar_estado", lambda x: x.consultas.__setitem__("estado", "OTRO"), "CONSULTAS")
toca("SC5_quitar_una_entrada_del_medio", lambda x: (x.consultas["entradas"].pop(1), x.consultas["historial"].pop(1)), "CONSULTAS")
o2, i = toca("SC5_recortar_la_ultima_entrada_y_su_anotacion", lambda x: (x.consultas["entradas"].pop(), x.consultas["historial"].pop()), None)
chk("SC5_recortar_la_cola_se_detecta_en_integridad", "CONSULTAS" in i, f"integridad()={i}; cabezas SC5 cambia: "
    f"{o.cabezas()['SC5'][:12]} -> {o2.cabezas().get('SC5', '')[:12]}")
o2, i = toca("SC5_borrar_todo_el_rastro", lambda x: setattr(x, "consultas", {"historial": [], "estado": "VIGENTE", "entradas": []}), None)
chk("SC5_borrar_todo_el_rastro_se_detecta_en_integridad", "CONSULTAS" in i or any("EXP-DD-01" in k for k in i),
    f"integridad()={i}; EXP-DD-01.consulta_ref={o2.expedientes['EXP-DD-01']['consulta_ref']} apunta a una consulta que ya no existe")

# campos nuevos de los DIRECTA
for eid in ("EXP-DD-01", "EXP-DC-05"):
    for campo, v in (("bloque_entrada", "E"), ("analisis_ref", "EV-SOB-0003"), ("consulta_ref", None), ("consulta_ref", "CON-0003"),
                     ("via_entrada", "SISTEMATICA"), ("encargo_actual", "EV-ENC-0003")):
        if o.expedientes[eid].get(campo) == v:
            continue   # no es un cambio
        toca(f"{eid}_{campo}={v}", lambda x, eid=eid, campo=campo, v=v: x.expedientes[eid].__setitem__(campo, v), "EXP:" + eid)
    toca(f"{eid}_borrar_bloque_entrada", lambda x, eid=eid: x.expedientes[eid].pop("bloque_entrada"), "EXP:" + eid)
toca("DD_sobre_copiado_cambiar_documento", lambda x: x.expedientes["EXP-DD-01"]["sobre"]["documento"]["payload"]["identificacion"].__setitem__("direccion", "CORTO"),
     "EXP:EXP-DD-01")
toca("DD_contradictor_copiado", lambda x: x.expedientes["EXP-DD-01"].__setitem__("contradictor", {"veredicto": "SIN_OBJECION"}), "EXP:EXP-DD-01")
toca("DD_quitar_la_anotacion_de_reutilizacion", lambda x: x.expedientes["EXP-DD-01"]["historial"].pop(1), "EXP:EXP-DD-01")

# campos nuevos puestos en un expediente que NO es DIRECTA (no entran en su identidad)
for campo, v in (("bloque_entrada", "D"), ("analisis_ref", "EV-SOB-0003"), ("consulta_ref", "CON-0001")):
    o2, i = toca(f"no_DIRECTA_{campo}_añadido", lambda x, campo=campo, v=v: x.expedientes["EXP-0001"].__setitem__(campo, v), None)
    print(f"   no DIRECTA + {campo}: integridad()={i}")

# consultar() mira el rastro antes de comprobarlo: con una consulta tocada, la misma consulta repetida da O-02 «duplicado»
o2 = copy.deepcopy(o)
o2.consultas["entradas"][0]["consulta"]["pregunta"] = "pregunta cambiada a mano, distinta"
r = o2.consultar({**CB, "pregunta": "pregunta cambiada a mano, distinta"}, "BROKER", AHORA)
chk("consultar_con_rastro_tocado_da_O13_y_kill", r["codigo"] == "O-13" and o2.kill is not None, (r, o2.kill))
o2 = copy.deepcopy(o)
o2.consultas["entradas"][0] = {"basura": 1}
r = o2.consultar({**CB, "consulta_id": "CON-0009"}, "BROKER", AHORA)
chk("consultar_con_rastro_ilegible_da_O13_y_kill", r["codigo"] == "O-13" and o2.kill is not None, (r, o2.kill))
sys.exit(fin())
