"""Pruebas de T-80 (V0.68): vía de entrada DIRECTA y modo CONSULTA en el Orquestador (Constitución V0.6, D-28, §2 y §4.1
regla 6). Datos SIMULADOS.

- Por C el expediente nace EN_ANALISIS con un encargo CT-G-01 completo; sin él, o con uno que no vale, no nace.
- Por D nace VALIDADA reutilizando un análisis vigente del registro (el sobre validado de otro expediente). Sin análisis
  reutilizable, un encargo de nivel bajo a C lo hace nacer EN_ANALISIS; sin encargo, no nace.
- Por E nace COMPARADA con un candidato único y el motivo de no comparar: la comparación es la de D frente al benchmark de la
  cartera. Con otros candidatos vigentes en la cartera se devuelve a D.
- F y G nunca son punto de entrada. Las transiciones hacia delante son las de siempre (hasta EJECUTADA).
- Una consulta no abre expediente ni mueve ninguno: deja su rastro, encadenado, en SC-5; después puede abrir uno DIRECTA.
- Todo queda en la cadena del historial: tocar el bloque de entrada, el análisis reutilizado o el rastro SC-5 se detecta.

Uso: python3 pruebas/pruebas_via_directa_t80.py
"""
import copy
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import persistencia as pe  # noqa: E402
import diario as di  # noqa: E402
from orquestador import BLOQUES_DIRECTA, NIVEL_BAJO, _identidad, _hash  # noqa: E402
from pruebas_orquestador import (AHORA, ENTRADA, SALIDA, Arnes, anotar_entrada, autorizar_op, dim, encargo,  # noqa: E402
                                 hasta, nuevo, sobre_para)
from pruebas_control_f import informe_f  # noqa: E402

TARDE = "2026-11-10T09:00:00+00:00"   # después del valid_until de los sobres de prueba


def enc_directa(eid, n, nivel=None):
    """Encargo CT-G-01 del Broker para el expediente DIRECTA eid (los mismos datos que encargo(n), con sus identificadores)."""
    e = encargo(n, producer="BROKER")
    e["expediente_id"], e["correlation_id"], e["event_id"] = eid, f"COR-{eid}", f"EV-ENC-{eid}"
    if nivel:
        e["payload"]["nivel_analisis"] = nivel
        if nivel in ("N0", "N1"):
            e["payload"]["decision_informada"] = "EXPLORAR"
    return e


def sobre_directa(eid, n):
    s = sobre_para(n, None)
    s["expediente_id"], s["correlation_id"], s["event_id"] = eid, f"COR-{eid}", f"EV-SOB-{eid}"
    return s


def descartado_por_operador(o, n=1):
    """EXP-000n validado y descartado por el operador: su análisis queda vigente en el registro y se puede reutilizar."""
    hasta(o, "VALIDADA", n)
    assert o.descartar(f"EXP-{n:04d}", "el operador lo aparta por ahora", "OPERADOR", AHORA)["ok"]


def consulta(cid="CON-0001", tipo="COMPARAR", bloque="D", cartera="TACTICA", analisis=("EV-SOB-0001",), pregunta="¿Cuál de estos análisis rinde más que el benchmark?"):
    return {"consulta_id": cid, "correlation_id": f"COR-{cid}", "tipo": tipo, "bloque": bloque, "cartera": cartera,
            "analisis": list(analisis), "pregunta": pregunta}


def sin_avisos(o):
    return {k: v for k, v in copy.deepcopy(o.__dict__).items() if k not in ("avisos", "ultimo_ahora")}


def main():
    h = Arnes()
    R = h.rechaza

    # ------------------------------------------------------------------ entrada por C
    o = nuevo()
    r = o.abrir_directa("EXP-DC-01", "COR-EXP-DC-01", "TACTICA", "C", "BROKER", AHORA, encargo=enc_directa("EXP-DC-01", 1))
    e = o.expedientes.get("EXP-DC-01")
    h.chk("C_nace_EN_ANALISIS", r["ok"] and r["nace_en"] == "EN_ANALISIS" and e["estado"] == "EN_ANALISIS" and r["encargo"] == "EV-ENC-EXP-DC-01", r)
    h.chk("C_su_primera_anotacion_es_el_nacimiento_con_la_identidad",
          [(x["desde"], x["hasta"], x["motivo"]) for x in e["historial"]] == [(None, "EN_ANALISIS", "encargo emitido")]
          and e["historial"][0]["datos"] == _hash(_identidad(e)) and e["via_entrada"] == "DIRECTA" and e["bloque_entrada"] == "C")
    h.chk("C_expediente_integro", o.integridad() == [] and o._todo_ok(e))
    r = o.entregar_sobre("EXP-DC-01", sobre_directa("EXP-DC-01", 1), AHORA)
    h.chk("C_sigue_las_transiciones_de_siempre_VALIDADA", r["ok"] and e["estado"] == "VALIDADA", r)
    r = o.comparar(["EXP-DC-01"], "D", AHORA)
    h.chk("C_candidato_unico_se_compara_con_el_benchmark", r["ok"] and e["estado"] == "COMPARADA", r)
    r = o.proponer("EXP-DC-01", ENTRADA, SALIDA, "BROKER", AHORA, dim(o, "EXP-DC-01"))
    h.chk("C_PROPUESTA_por_E", r["ok"] and e["estado"] == "PROPUESTA", r)
    r = autorizar_op(o, "EXP-DC-01", informe_f(o, "EXP-DC-01", 41), AHORA)
    h.chk("C_AUTORIZADA_por_F_y_el_operador", r["ok"] and e["estado"] == "AUTORIZADA", r)
    anotar_entrada(o, "EXP-DC-01", "ORD-DC-1", 100.0, AHORA)
    r = o.ejecutar("EXP-DC-01", {"orden_id": "ORD-DC-1", "cantidad": 100.0, "precio": 1.1, "conciliada": True,
                                 "proteccion_orden_ids": ["ORD-DC-1-STOP"]}, "G", AHORA)
    h.chk("C_EJECUTADA_por_G_y_nace_la_posicion", r["ok"] and e["estado"] == "EJECUTADA" and o.posiciones[e["posicion_id"]]["estado"] == "ABIERTA"
          and o.integridad() == [], r)

    o = nuevo()
    R("C_sin_encargo_no_nace", o, lambda: o.abrir_directa("EXP-DC-02", "COR-2", "TACTICA", "C", "BROKER", AHORA), "O-01")
    mal = enc_directa("EXP-DC-02", 2)
    del mal["payload"]["presupuesto"]
    R("C_con_un_encargo_incompleto_no_nace", o, lambda: o.abrir_directa("EXP-DC-02", "COR-EXP-DC-02", "TACTICA", "C", "BROKER", AHORA, encargo=mal), "O-01")
    R("C_encargo_de_otro_expediente_no_nace", o, lambda: o.abrir_directa("EXP-DC-03", "COR-EXP-DC-03", "TACTICA", "C", "BROKER", AHORA,
                                                                          encargo=enc_directa("EXP-DC-02", 2)), "O-12")
    R("C_no_reutiliza_analisis", o, lambda: o.abrir_directa("EXP-DC-02", "COR-EXP-DC-02", "TACTICA", "C", "BROKER", AHORA,
                                                             encargo=enc_directa("EXP-DC-02", 2), analisis="EV-SOB-0001"), "O-01")
    h.chk("C_lo_rechazado_no_deja_expediente", "EXP-DC-02" not in o.expedientes and "EXP-DC-03" not in o.expedientes and not o.encargos)
    o = nuevo({"dia_coste_max_eur": 0.5})
    R("C_el_presupuesto_del_dia_es_el_mismo", o, lambda: o.abrir_directa("EXP-DC-04", "COR-EXP-DC-04", "TACTICA", "C", "BROKER", AHORA,
                                                                          encargo=enc_directa("EXP-DC-04", 4)), "O-08")

    # ------------------------------------------------------------------ entrada por D
    o = nuevo()
    descartado_por_operador(o, 1)
    r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
    e = o.expedientes.get("EXP-DD-01")
    h.chk("D_nace_VALIDADA_reutilizando_el_analisis", r["ok"] and r["nace_en"] == "VALIDADA" and r["reutiliza"] == "EXP-0001"
          and e["estado"] == "VALIDADA" and e["sobre"] == o.expedientes["EXP-0001"]["sobre"] and e["analisis_ref"] == "EV-SOB-0001", r)
    h.chk("D_historial_nacimiento_y_reutilizacion", [(x["desde"], x["hasta"], x["actor"]) for x in e["historial"]]
          == [(None, "VALIDADA", "BROKER"), ("VALIDADA", "VALIDADA", "ORQUESTADOR")]
          and e["historial"][1]["ref"] == o.expedientes["EXP-0001"]["encargo_actual"] == e["encargo_actual"])
    h.chk("D_expediente_integro", o.integridad() == [])
    h.chk("D_no_encarga_nada_ni_gasta", len(o.encargos) == 1 and o.gasto_dia == {})
    r = o.comparar(["EXP-DD-01"], "D", AHORA)
    h.chk("D_sigue_a_COMPARADA", r["ok"] and e["estado"] == "COMPARADA", r)
    r = o.proponer("EXP-DD-01", ENTRADA, SALIDA, "BROKER", AHORA, dim(o, "EXP-DD-01"))
    h.chk("D_sigue_a_PROPUESTA", r["ok"] and e["estado"] == "PROPUESTA" and o.integridad() == [], r)
    r = autorizar_op(o, "EXP-DD-01", informe_f(o, "EXP-DD-01", 42), AHORA)
    anotar_entrada(o, "EXP-DD-01", "ORD-DD-1", 100.0, AHORA)
    r2 = o.ejecutar("EXP-DD-01", {"orden_id": "ORD-DD-1", "cantidad": 100.0, "precio": 1.1, "conciliada": True,
                                  "proteccion_orden_ids": ["ORD-DD-1-STOP"]}, "G", AHORA)
    h.chk("D_sigue_a_AUTORIZADA_y_EJECUTADA", r["ok"] and r2["ok"] and e["estado"] == "EJECUTADA" and o.integridad() == [], (r, r2))
    R("D_el_mismo_analisis_no_se_reutiliza_dos_veces_ni_invertido", o,
      lambda: o.abrir_directa("EXP-DD-02", "COR-DD-02", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001"), "O-06")

    o = nuevo()
    hasta(o, "VALIDADA", 1)
    r = R("D_un_analisis_en_juego_no_se_reutiliza", o, lambda: o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA,
                                                                                analisis="EV-SOB-0001"), "O-06")
    h.chk("D_sin_analisis_reutilizable_pide_encargo_de_nivel_bajo", r.get("encargar") == NIVEL_BAJO == "N2", r)
    assert o.observar("EXP-0001", [{"tipo": "FECHA", "fecha": "2026-11-20"}], "el gestor lo deja para más adelante", "GESTOR_TACTICA", AHORA)["ok"]
    R("D_lo_apartado_por_el_gestor_no_vuelve_por_la_via_DIRECTA", o,
      lambda: o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001"), "O-06")
    assert o.ratificar_apartado("EXP-0001", "el operador lo hace suyo", "OPERADOR", AHORA)["ok"]
    r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
    h.chk("D_ratificado_por_el_operador_si_se_reutiliza", r["ok"] and o.expedientes["EXP-DD-01"]["estado"] == "VALIDADA", r)
    R("D_de_otra_cartera_no", o, lambda: o.abrir_directa("EXP-DD-03", "COR-DD-03", "TRADING", "D", "BROKER", AHORA, analisis="EV-SOB-0001"), "O-12")
    R("D_analisis_desconocido", o, lambda: o.abrir_directa("EXP-DD-03", "COR-DD-03", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-9999"), "O-12")
    R("D_sin_analisis_ni_encargo", o, lambda: o.abrir_directa("EXP-DD-03", "COR-DD-03", "TACTICA", "D", "BROKER", AHORA), "O-06")
    R("D_no_lleva_motivo_de_no_comparar", o, lambda: o.abrir_directa("EXP-DD-03", "COR-DD-03", "TACTICA", "D", "BROKER", AHORA,
                                                                      analisis="EV-SOB-0001", motivo="un motivo que no es de D"), "O-01")
    o = nuevo()
    descartado_por_operador(o, 1)
    R("D_analisis_caducado", o, lambda: o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", TARDE, analisis="EV-SOB-0001"), "O-10")

    # D sin análisis: lo que falta se encarga a C con nivel bajo
    o = nuevo()
    R("D_lo_que_falta_no_se_encarga_con_nivel_alto", o, lambda: o.abrir_directa("EXP-DD-05", "COR-EXP-DD-05", "TACTICA", "D", "BROKER", AHORA,
                                                                                 encargo=enc_directa("EXP-DD-05", 5)), "O-06")
    r = o.abrir_directa("EXP-DD-05", "COR-EXP-DD-05", "TACTICA", "D", "BROKER", AHORA, encargo=enc_directa("EXP-DD-05", 5, nivel="N2"))
    e = o.expedientes.get("EXP-DD-05")
    h.chk("D_sin_analisis_con_encargo_de_nivel_bajo_nace_EN_ANALISIS", r["ok"] and r["nace_en"] == "EN_ANALISIS" and e["bloque_entrada"] == "D"
          and e["analisis_ref"] is None and o.encargos["EV-ENC-EXP-DD-05"]["nivel"] == "N2" and o.integridad() == [], r)
    s5 = sobre_directa("EXP-DD-05", 5)
    s5["payload"]["identificacion"]["nivel_analisis"] = "N2"
    r = o.entregar_sobre("EXP-DD-05", s5, AHORA)
    r2 = o.comparar(["EXP-DD-05"], "D", AHORA) if r["ok"] else r
    r3 = o.proponer("EXP-DD-05", ENTRADA, SALIDA, "BROKER", AHORA, dim(o, "EXP-DD-05")) if r2["ok"] else r2
    h.chk("D_el_nivel_bajo_puede_acabar_en_una_orden_H04", r3["ok"] and e["estado"] == "PROPUESTA", (r, r2, r3))
    R("D_con_analisis_y_encargo_a_la_vez_no_H06", o, lambda: o.abrir_directa("EXP-DD-06", "COR-EXP-DD-06", "TACTICA", "D", "BROKER", AHORA,
                                                                              analisis="EV-SOB-0001", encargo=enc_directa("EXP-DD-06", 6, nivel="N2")), "O-01")

    # QA r01, H-01: el origen se volvió a encargar después de validar: su sobre ya no es el de su encargo actual
    o = nuevo()
    hasta(o, "VALIDADA", 1)
    assert o.observar("EXP-0001", [{"tipo": "FECHA", "fecha": "2026-11-20"}], "el operador lo deja para más adelante", "OPERADOR", AHORA)["ok"]
    assert o.reabrir("EXP-0001", "el operador quiere un análisis nuevo", "OPERADOR", AHORA)["ok"]
    e2 = encargo(1)
    e2["event_id"] = "EV-ENC-0001-B"
    assert o.emitir_encargo("EXP-0001", e2, "GESTOR_TACTICA", AHORA)["ok"]
    assert o.observar("EXP-0001", [{"tipo": "FECHA", "fecha": "2026-11-20"}], "el operador lo aparta otra vez", "OPERADOR", AHORA)["ok"]
    R("D_no_reutiliza_un_sobre_cuyo_origen_se_volvio_a_encargar_H01", o,
      lambda: o.abrir_directa("EXP-DD-07", "COR-DD-07", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001"), "O-06")
    h.chk("registro_lo_marca_no_reutilizable_H01", [x["reutilizable"] for x in o.analisis_vigentes(AHORA)] == [False])

    # QA r01, H-03: una propuesta caducada no vuelve por la vía DIRECTA (§4.1, regla 4)
    o = nuevo()
    hasta(o, "PROPUESTA", 1)
    A2 = "2026-11-08T13:00:00+00:00"   # pasó la ventana de la propuesta (12:00), no la vigencia del sobre (18:00)
    assert o.barrer(A2)["ok"] and o.expedientes["EXP-0001"]["estado"] == "CADUCADA"
    R("una_propuesta_caducada_no_vuelve_por_la_via_DIRECTA_H03", o,
      lambda: o.abrir_directa("EXP-DD-08", "COR-DD-08", "TACTICA", "D", "BROKER", A2, analisis="EV-SOB-0001"), "O-06")
    for quien in ("OPERADOR", "BROKER"):   # QA r02, H-09: ni pasándola antes a DESCARTADA
        o2 = copy.deepcopy(o)
        assert o2.descartar("EXP-0001", "la propuesta caducó y se descarta (regla 4)", quien, A2)["ok"]
        r = R(f"una_propuesta_caducada_y_descartada_por_{quien}_no_vuelve_H09", o2,
              lambda o2=o2: o2.abrir_directa("EXP-DD-08", "COR-DD-08", "TACTICA", "D", "BROKER", A2, analisis="EV-SOB-0001"), "O-06")
        h.chk(f"el_motivo_dice_que_caduco_H12_{quien}", "caducó" in r["motivo"], r)

    # ------------------------------------------------------------------ entrada por E
    o = nuevo()
    descartado_por_operador(o, 1)
    MOT = "solo hay un candidato en la cartera: lo pidió el operador"
    R("E_sin_motivo_de_no_comparar", o, lambda: o.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "E", "BROKER", AHORA, analisis="EV-SOB-0001"), "O-15")
    R("E_no_encarga", o, lambda: o.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "E", "BROKER", AHORA, analisis="EV-SOB-0001", motivo=MOT,
                                                  encargo=enc_directa("EXP-DE-01", 7)), "O-01")
    R("E_sin_analisis", o, lambda: o.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "E", "BROKER", AHORA, motivo=MOT), "O-06")
    r = o.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "E", "BROKER", AHORA, analisis="EV-SOB-0001", motivo=MOT)
    e = o.expedientes.get("EXP-DE-01")
    c = (e or {}).get("comparacion") or {}
    h.chk("E_nace_COMPARADA_frente_al_benchmark", r["ok"] and r["nace_en"] == "COMPARADA" and e["estado"] == "COMPARADA"
          and c.get("motivo_no_comparar") == MOT and c.get("referencia") is not None and c.get("testigos") == []
          and o.ultima_comparacion["TACTICA"] == c.get("id"), r)
    h.chk("E_historial_con_la_comparacion_de_D", [(x["hasta"], x["actor"]) for x in e["historial"]]
          == [("VALIDADA", "BROKER"), ("VALIDADA", "ORQUESTADOR"), ("COMPARADA", "D")] and "benchmark" in e["historial"][-1]["motivo"])
    h.chk("E_expediente_integro", o.integridad() == [])
    r = o.proponer("EXP-DE-01", ENTRADA, SALIDA, "BROKER", AHORA, dim(o, "EXP-DE-01")) if c.get("ganador") else {"ok": False, "motivo": c}
    h.chk("E_sigue_a_PROPUESTA_y_el_dinero_sale_por_F_y_G", r["ok"] and e["estado"] == "PROPUESTA", r)

    o = nuevo()
    descartado_por_operador(o, 1)
    hasta(o, "VALIDADA", 3)   # otro candidato vigente en la cartera
    r = R("E_con_otros_candidatos_se_devuelve_a_D", o, lambda: o.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "E", "BROKER", AHORA,
                                                                                analisis="EV-SOB-0001", motivo=MOT), "O-22")
    h.chk("E_devuelto_dice_a_donde_y_con_quien", r.get("devolver_a") == "D" and r.get("faltan") == ["EXP-0003"] and "EXP-DE-01" not in o.expedientes, r)
    r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
    r2 = o.comparar(["EXP-DD-01", "EXP-0003"], "D", AHORA)
    h.chk("E_devuelto_a_D_compara_con_todos", r["ok"] and r2["ok"] and o.expedientes["EXP-DD-01"]["estado"] == "COMPARADA", (r, r2))

    # ------------------------------------------------------------------ quién y por dónde
    o = nuevo()
    descartado_por_operador(o, 1)
    for b in ("F", "G", "A", "B", "X", None):
        R(f"bloque_{b}_no_es_entrada", o, lambda b=b: o.abrir_directa("EXP-X-01", "COR-X-01", "TACTICA", b, "BROKER", AHORA, analisis="EV-SOB-0001"), "O-01")
    R("solo_el_Broker_entra_por_la_via_DIRECTA", o, lambda: o.abrir_directa("EXP-X-01", "COR-X-01", "TACTICA", "D", "GESTOR_TACTICA", AHORA,
                                                                             analisis="EV-SOB-0001"), "O-05")
    R("ni_el_operador_sin_el_Broker", o, lambda: o.abrir_directa("EXP-X-01", "COR-X-01", "TACTICA", "D", "OPERADOR", AHORA, analisis="EV-SOB-0001"), "O-05")
    R("expediente_que_ya_existe", o, lambda: o.abrir_directa("EXP-0001", "COR-X-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001"), "O-03")
    R("cartera_invalida", o, lambda: o.abrir_directa("EXP-X-01", "COR-X-01", "OTRA", "D", "BROKER", AHORA, analisis="EV-SOB-0001"), "O-01")
    R("id_de_posicion_no", o, lambda: o.abrir_directa("POS-X", "COR-X-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001"), "O-01")
    R("detectar_no_abre_DIRECTA", o, lambda: o.detectar("EXP-X-01", "COR-X-01", "DIRECTA", "TACTICA", "BROKER", AHORA), "O-01")
    h.chk("BLOQUES_DIRECTA_son_C_D_y_E", BLOQUES_DIRECTA == {"C": "EN_ANALISIS", "D": "VALIDADA", "E": "COMPARADA"})

    # ------------------------------------------------------------------ integridad de lo nuevo
    o = nuevo()
    descartado_por_operador(o, 1)
    assert o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")["ok"]
    for campo, valor in (("bloque_entrada", "C"), ("analisis_ref", "EV-SOB-0002"), ("consulta_ref", "CON-9"), ("via_entrada", "DISCRECIONAL"),
                         ("encargo_actual", "EV-ENC-OTRO")):
        o2 = copy.deepcopy(o)
        o2.expedientes["EXP-DD-01"][campo] = valor
        h.chk(f"tocar_{campo}_se_detecta", "EXP:EXP-DD-01" in o2.integridad())
    o2 = copy.deepcopy(o)
    o2.expedientes["EXP-DD-01"]["sobre"]["valid_until"] = "2027-01-01T00:00:00+00:00"
    h.chk("alargar_el_sobre_reutilizado_se_detecta", "EXP:EXP-DD-01" in o2.integridad())
    o2 = copy.deepcopy(o)
    o2.expedientes["EXP-DD-01"]["historial"][1]["motivo"] = "otra cosa"
    h.chk("tocar_la_anotacion_de_reutilizacion_se_detecta", "EXP:EXP-DD-01" in o2.integridad())
    for campo in ("bloque_entrada", "analisis_ref", "consulta_ref"):   # QA r01, H-07: en un expediente que no es DIRECTA
        o2 = copy.deepcopy(o)
        o2.expedientes["EXP-0001"][campo] = "D" if campo == "bloque_entrada" else "EV-SOB-0001"
        h.chk(f"un_{campo}_en_un_expediente_no_DIRECTA_se_detecta_H07", "EXP:EXP-0001" in o2.integridad())

    # ------------------------------------------------------------------ modo CONSULTA
    o = nuevo()
    hasta(o, "VALIDADA", 1)
    hasta(o, "VALIDADA", 3)
    antes = sin_avisos(o)
    r = o.consultar(consulta(analisis=("EV-SOB-0001", "EV-SOB-0003")), "BROKER", AHORA)
    despues = sin_avisos(o)
    h.chk("consulta_COMPARAR_la_hace_D_y_da_resultado", r["ok"] and r["resultado"]["decision_global"] == "INVERTIR"
          and r["resultado"]["referencia"] is not None and r["resultado"]["ganador"] == "EV-SOB-0001"
          and r["resultado"]["excluidos"] == {"EV-SOB-0003": "DUPLICADO"}, r)   # el mismo instrumento y sentido: D se queda con uno
    h.chk("consulta_no_abre_expediente_ni_mueve_ninguno", antes["expedientes"] == despues["expedientes"]
          and antes["ultima_comparacion"] == despues["ultima_comparacion"] and antes["encargos"] == despues["encargos"])
    h.chk("consulta_deja_su_rastro_en_SC5", len(o.consultas["entradas"]) == 1 and o.consultas["entradas"][0]["tipo"] == "CONSULTA"
          and o.consultas["entradas"][0]["resultado"] == r["resultado"] and o.consultas_ok() and "SC5" in o.cabezas() and o.integridad() == [])
    R("consulta_repetida_es_idempotente", o, lambda: o.consultar(consulta(analisis=("EV-SOB-0001", "EV-SOB-0003")), "BROKER", AHORA), "O-02",
      ok_esperado=True)
    R("consulta_id_repetido_con_otro_contenido", o, lambda: o.consultar(consulta(analisis=("EV-SOB-0001",)), "BROKER", AHORA), "O-03")
    r = o.consultar(consulta("CON-0002", tipo="ANALIZAR", bloque="C", cartera=None, analisis=(), pregunta="¿Qué tal pinta el yen este trimestre?"),
                    "BROKER", AHORA)
    h.chk("consulta_ANALIZAR_sin_analisis_solo_deja_rastro", r["ok"] and r["resultado"] is None and len(o.consultas["entradas"]) == 2, r)
    for nombre, cons, cod in (("tipo_invalido", consulta("CON-X", tipo="INVERTIR"), "O-01"),
                              ("en_F_no", consulta("CON-X", tipo="PROYECTAR", bloque="F"), "O-01"),
                              ("en_G_no", consulta("CON-X", tipo="PROYECTAR", bloque="G"), "O-01"),
                              ("COMPARAR_fuera_de_D", consulta("CON-X", bloque="E"), "O-01"),
                              ("COMPARAR_sin_cartera", consulta("CON-X", cartera=None), "O-01"),
                              ("COMPARAR_sin_analisis", consulta("CON-X", analisis=()), "O-01"),
                              ("analisis_repetidos", consulta("CON-X", analisis=("EV-SOB-0001", "EV-SOB-0001")), "O-01"),
                              ("analisis_desconocido", consulta("CON-X", analisis=("EV-SOB-9999",)), "O-12"),
                              ("analisis_de_otra_cartera", consulta("CON-X", cartera="TRADING"), "O-12"),
                              ("sin_pregunta", consulta("CON-X", pregunta="¿y?"), "O-15"),
                              ("campos_de_mas", {**consulta("CON-X"), "invertir": True}, "O-01")):
        R(f"consulta_{nombre}", o, lambda cons=cons: o.consultar(cons, "BROKER", AHORA), cod)
    R("consulta_solo_la_hace_el_Broker", o, lambda: o.consultar(consulta("CON-X"), "GESTOR_TACTICA", AHORA), "O-05")
    R("consulta_de_un_analisis_caducado", o, lambda: o.consultar(consulta("CON-X"), "BROKER", TARDE), "O-10")

    # de la consulta a la decisión: abre un expediente DIRECTA reutilizando sus análisis
    assert o.descartar("EXP-0001", "el operador lo aparta por ahora", "OPERADOR", AHORA)["ok"]
    R("de_consulta_desconocida_no", o, lambda: o.abrir_directa("EXP-DQ-01", "COR-DQ-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001",
                                                                consulta_id="CON-9999"), "O-12")
    R("de_consulta_con_un_analisis_que_no_es_suyo", o, lambda: o.abrir_directa("EXP-DQ-01", "COR-DQ-01", "TACTICA", "D", "BROKER", AHORA,
                                                                               analisis="EV-SOB-0001", consulta_id="CON-0002"), "O-12")
    r = o.abrir_directa("EXP-DQ-01", "COR-DQ-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001", consulta_id="CON-0001")
    h.chk("de_la_consulta_a_un_expediente_DIRECTA", r["ok"] and o.expedientes["EXP-DQ-01"]["consulta_ref"] == "CON-0001"
          and o.consultas["entradas"][-1] == {"tipo": "APERTURA", "consulta_id": "CON-0001", "expediente_id": "EXP-DQ-01", "bloque": "D"}
          and o.integridad() == [], r)

    # el rastro SC-5 tocado: integridad y kill-switch en el siguiente punto de decisión
    o2 = copy.deepcopy(o)
    o2.consultas["entradas"][0]["resultado"] = None
    h.chk("tocar_el_rastro_SC5_se_detecta", "CONSULTAS" in o2.integridad() and not o2.consultas_ok())
    for nombre, recorte in (("vaciarlo", 0), ("recortar_la_apertura", -1), ("recortar_la_consulta_y_la_apertura", 1)):   # QA r01, H-02
        o3 = copy.deepcopy(o)
        L = o3.consultas
        L["historial"], L["entradas"] = L["historial"][:recorte], L["entradas"][:recorte]
        if not L["historial"]:
            L["estado"] = "VIGENTE"
        h.chk(f"SC5_{nombre}_con_un_expediente_que_lo_cita_se_detecta_H02", "CONSULTAS" in o3.integridad(), L)
    o3 = copy.deepcopy(o)
    o3.consultas["entradas"][0]["consulta"]["pregunta"] = "otra pregunta escrita a mano"
    r = o3.consultar(consulta(analisis=("EV-SOB-0001", "EV-SOB-0003")), "BROKER", AHORA)
    h.chk("consultar_con_el_rastro_tocado_da_O13_y_kill_H05", r["codigo"] == "O-13" and o3.kill is not None, r)
    r = o2.comparar(["EXP-DQ-01", "EXP-0003"], "D", AHORA)
    h.chk("con_el_rastro_SC5_tocado_no_se_compara_y_salta_el_kill", r["codigo"] == "O-13" and o2.kill is not None, r)

    # ------------------------------------------------------------------ registro de análisis vigentes (solo lee)
    reg = o.analisis_vigentes(AHORA, "TACTICA")
    fila = {x["analisis"]: x for x in reg}
    h.chk("registro_lista_los_analisis_vigentes_de_la_cartera", set(fila) == {"EV-SOB-0001", "EV-SOB-0003"}
          and fila["EV-SOB-0001"]["en"] == ["EXP-0001", "EXP-DQ-01"] and fila["EV-SOB-0001"]["reutilizable"] is False
          and fila["EV-SOB-0003"]["reutilizable"] is False and "en juego" in fila["EV-SOB-0003"]["motivo"], reg)
    h.chk("registro_no_mueve_el_reloj", o.analisis_vigentes(TARDE) == [] and o.ultimo_ahora == AHORA)
    h.chk("registro_ilegible_es_lista_vacia", o.analisis_vigentes("ayer") == [] and o.analisis_vigentes(None) == [])
    h.chk("registro_de_otra_cartera_vacio", o.analisis_vigentes(AHORA, "TRADING") == [])

    # ------------------------------------------------------------------ persistencia y diario
    t = pe.volcar(o, AHORA)
    rc = pe.cargar(t)
    h.chk("persistencia_conserva_los_DIRECTA_y_el_rastro", rc["ok"] and rc["orquestador"].integridad() == []
          and rc["orquestador"].consultas == o.consultas and pe.volcar(rc["orquestador"], AHORA) == t, rc.get("motivo"))
    with tempfile.TemporaryDirectory() as d:
        o = nuevo()
        descartado_por_operador(o, 1)
        rd = di.crear(o, Path(d) / "estado.json", Path(d) / "diario.jsonl", AHORA)
        dd = rd["diario"]
        r1 = dd.consultar(consulta(), "BROKER", AHORA)
        r2 = dd.abrir_directa("EXP-DQ-01", "COR-DQ-01", "TACTICA", "E", "BROKER", AHORA, analisis="EV-SOB-0001",
                              motivo="candidato único: viene de la consulta CON-0001", consulta_id="CON-0001")
        ra = di.abrir(Path(d) / "estado.json", Path(d) / "diario.jsonl")
        o3 = ra["diario"]._o if ra.get("ok") else None
        h.chk("diario_anota_y_reproduce_consultar_y_abrir_directa", r1["ok"] and r2["ok"] and o3 is not None
              and pe.volcar(o3, AHORA) == pe.volcar(dd._o, AHORA) and o3.expedientes["EXP-DQ-01"]["estado"] == "COMPARADA", (r1, r2, ra.get("motivo")))

    # ------------------------------------------------------------------ la pasada PC3-01 de la V0.68
    raiz = AQUI.parent
    p = subprocess.run([sys.executable, "-I", str(raiz / "entrega_claude" / "V0.68" / "scripts" / "pc3_01_via_directa.py")],
                       capture_output=True, text=True, timeout=120)
    h.chk("PC3_01_CUMPLE", p.returncode == 0 and p.stdout.startswith("CUMPLE"), p.stdout + p.stderr)

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO VÍA DIRECTA T-80:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
