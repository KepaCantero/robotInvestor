"""Pruebas de N mínimo (consola del operador) y del acuse de avisos. Datos SIMULADOS.

Uso: python3 pruebas/pruebas_consola.py
"""
import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from consola import avisos_pendientes, cola_aprobaciones, panel  # noqa: E402
from pruebas_orquestador import (AHORA, S1, S2, Arnes, CAL, CFG, Orquestador, encargo, hasta, informe_ctr, nuevo,  # noqa: E402
                                 obj_ctr, sobre)


def niv(o, ahora=AHORA):
    return panel(o, ahora)["nivel"]


def comp(o, que, ahora=AHORA):
    return next(x for x in panel(o, ahora)["comprobaciones"] if x["que"] == que)["nivel"]


def main():
    h = Arnes()
    R = lambda *a, **k: h.rechaza(*a, **k)  # noqa: E731
    # panel
    o = Orquestador(CFG, CAL)
    h.chk("sin_sellos_es_rojo", niv(o) == "ROJO" and comp(o, "datos") == "ROJO")
    o = nuevo()
    h.chk("estado_limpio_es_verde", niv(o) == "VERDE", panel(o, AHORA))
    antes = copy.deepcopy(o.__dict__)
    panel(o, AHORA); cola_aprobaciones(o, AHORA); avisos_pendientes(o)
    h.chk("consola_no_modifica_nada", antes == o.__dict__)
    h.chk("panel_basura_es_rojo_sin_excepcion", panel(o, "no-es-fecha")["nivel"] == "ROJO" and panel(None, AHORA)["nivel"] == "ROJO")
    # avisos
    o = nuevo(); hasta(o, "EN_ANALISIS")
    o.registrar_gasto("EV-ENC-0001", 99.0, 1, AHORA)   # O-07 (media) y O-08 (alta)
    pend = avisos_pendientes(o)
    h.chk("avisos_ordenados_alta_primero", [x["prioridad"] for x in pend][0] == "ALTA" and len(pend) == 2, pend)
    h.chk("aviso_alto_sin_acusar_es_rojo", comp(o, "avisos") == "ROJO" and comp(o, "presupuesto") == "ROJO")
    R("acusar_actor_ajeno_O05", o, lambda: o.acusar_aviso(pend[0]["id"], "BROKER", AHORA), "O-05")
    R("acusar_inexistente_O12", o, lambda: o.acusar_aviso("AV-99999", "OPERADOR", AHORA), "O-12")
    R("acusar_no_texto_O12", o, lambda: o.acusar_aviso(["AV-00001"], "OPERADOR", AHORA), "O-12")
    for x in pend:
        assert o.acusar_aviso(x["id"], "OPERADOR", AHORA)["ok"]
    h.chk("acusar_deja_constancia_y_no_borra", len(o.avisos) == 2 and all(x["acuse"] for x in o.avisos) and avisos_pendientes(o) == [])
    R("acusar_dos_veces_O02", o, lambda: o.acusar_aviso(pend[0]["id"], "OPERADOR", AHORA), "O-02", ok_esperado=True)
    h.chk("avisos_acusados_dejan_avisos_verde", comp(o, "avisos") == "VERDE")
    # aviso de prioridad media -> ámbar
    o = nuevo(); hasta(o, "EN_ANALISIS")
    o.registrar_gasto("EV-ENC-0001", 6.0, 1, AHORA)    # supera el encargo (5): O-07 media
    h.chk("aviso_medio_es_ambar", comp(o, "avisos") == "AMBAR" and niv(o) == "AMBAR", panel(o, AHORA))
    # cola de aprobaciones y urgencia
    o = nuevo(); hasta(o, "PROPUESTA")
    cola = cola_aprobaciones(o, AHORA)
    h.chk("propuesta_en_cola", [x["tipo"] for x in cola] == ["AUTORIZAR"] and cola[0]["ref"] == "EXP-0001", cola)
    h.chk("propuesta_lejana_es_verde", comp(o, "decisiones") == "VERDE")
    h.chk("propuesta_que_vence_pronto_es_ambar", comp(o, "decisiones", "2026-11-08T08:00:00+00:00") == "AMBAR")
    h.chk("propuesta_vencida_marcada", cola_aprobaciones(o, "2026-11-09T00:00:00+00:00")[0]["vencida"] is True)
    # objeción crítica -> rojo
    o = nuevo({"exige_contradictor_en": ["N3"]}); o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)
    crit = informe_ctr(sobre(1), veredicto="OBJECION_CRITICA", objeciones=[obj_ctr(1, "CRITICA", ["SRC-EURUSD"], "LOGICA")])
    o.entregar_sobre("EXP-0001", sobre(1), AHORA, informe=crit)
    h.chk("objecion_critica_en_cola_y_rojo", [x["tipo"] for x in cola_aprobaciones(o, AHORA)] == ["OBJECION_CRITICA"] and comp(o, "decisiones") == "ROJO")
    o.levantar_objecion("EXP-0001", "asumo la objeción", "OPERADOR", AHORA)
    h.chk("levantada_sale_de_la_cola", cola_aprobaciones(o, AHORA) == [])
    # posición en revisión
    o = nuevo(); hasta(o, "EJECUTADA")
    o.posicion_transicion("POS-EXP-0001", "EN_REVISION", "H", AHORA)
    h.chk("posicion_en_revision_en_cola", [x["tipo"] for x in cola_aprobaciones(o, AHORA)] == ["REVISAR_POSICION"])
    # integridad rota -> rojo
    o = nuevo(); hasta(o, "DETECTADA")
    o.expedientes["EXP-0001"]["historial"][0]["actor"] = "otro"
    h.chk("historial_roto_es_rojo", comp(o, "integridad") == "ROJO" and niv(o) == "ROJO")
    # sello caducado por antigüedad -> ámbar
    o = nuevo()
    h.chk("unico_sello_caducado_es_rojo", comp(o, "datos", "2026-12-20T09:00:00+00:00") == "ROJO")
    o = nuevo(sellos=(S1, S2))
    h.chk("un_sello_caducado_y_otro_vigente_es_ambar", comp(o, "datos", "2026-11-09T09:00:00+00:00") == "AMBAR", panel(o, "2026-11-09T09:00:00+00:00"))
    # presupuesto cercano al tope -> ámbar
    o = nuevo({"dia_coste_max_eur": 6.0}); hasta(o, "EN_ANALISIS")
    h.chk("presupuesto_comprometido_es_ambar", comp(o, "presupuesto") == "AMBAR", panel(o, AHORA))
    # --- correcciones tras la revisión independiente
    o = nuevo(); hasta(o, "EN_ANALISIS"); o.registrar_gasto("EV-ENC-0001", 99.0, 1, AHORA)
    p = avisos_pendientes(o); p[0]["acuse"] = {"actor": "X"}
    h.chk("avisos_pendientes_son_copias", len(avisos_pendientes(o)) == 2 and comp(o, "avisos") == "ROJO")
    o = nuevo(); hasta(o, "PROPUESTA"); o.expedientes["EXP-0001"]["propuesta"]["entrada"]["limite"] = 9.9
    h.chk("propuesta_alterada_es_rojo", comp(o, "integridad") == "ROJO" and "EXP:EXP-0001" in o.integridad())
    o = nuevo(); hasta(o, "EJECUTADA"); o.detectar("POS-EXP-0001", "COR-9", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    o.expedientes["POS-EXP-0001"]["historial"][0]["actor"] = "x"
    h.chk("colision_de_ids_no_oculta_historial_roto", comp(o, "integridad") == "ROJO" and o.integridad() == ["EXP:POS-EXP-0001"], o.integridad())
    h.chk("cabezas_no_colisionan", {"EXP:POS-EXP-0001", "POS:POS-EXP-0001"} <= set(o.cabezas()))
    o = nuevo(); hasta(o, "DETECTADA")
    r = o.acusar_aviso("AV-00001", "BROKER", "2099-01-01T00:00:00Z")
    h.chk("llamada_rechazada_no_adelanta_el_reloj", not r["ok"] and o.detectar("EXP-0005", "COR-5", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"])
    o = nuevo(); r = o.detectar("EXP-0001", "COR-1", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", "2099-01-01T00:00:00Z"); r2 = o.detectar("EXP-0002", "x", "MAL", "TACTICA", "GESTOR_TACTICA", "2098-01-01T00:00:00Z")
    h.chk("rechazo_por_datos_no_adelanta_el_reloj", not r2["ok"] and o.ultimo_ahora == "2099-01-01T00:00:00Z")
    o = nuevo(); o.detectar("EXP-0001", "COR-1", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    o.detectar("EXP-0002", "x", "MAL", "TACTICA", "GESTOR_TACTICA", "2099-01-01T00:00:00Z")
    h.chk("detectar_rechazado_deja_reloj", o.ultimo_ahora == AHORA)
    o = nuevo()
    h.chk("todos_los_sellos_caducados_es_rojo", comp(o, "datos", "2027-06-20T09:00:00+00:00") == "ROJO")
    o = nuevo(); hasta(o, "PROPUESTA"); o.barrer("2026-11-08T12:30:00+00:00")
    h.chk("caducar_por_barrer_deja_aviso", any(a["codigo"] == "O-10" and a["ref"] == "EXP-0001" for a in o.avisos))
    o = nuevo(); hasta(o, "EN_ANALISIS"); o.registrar_gasto("EV-ENC-0001", 6.0, 1, AHORA)
    for x in list(avisos_pendientes(o)):
        o.acusar_aviso(x["id"], "OPERADOR", AHORA)
    h.chk("encargo_incompleto_en_cola_y_ambar", [x["tipo"] for x in cola_aprobaciones(o, AHORA)] == ["REEMITIR_O_DESCARTAR"] and comp(o, "decisiones") == "AMBAR")
    o = nuevo(); hasta(o, "PROPUESTA")
    o.expedientes["EXP-0002"]["propuesta"] = copy.deepcopy(o.expedientes["EXP-0001"]["propuesta"]) if "EXP-0002" in o.expedientes else None
    a1 = copy.deepcopy(o.expedientes["EXP-0001"]); a1["propuesta"]["entrada"]["ventana_hasta"] = "2026-11-08T12:00:00+05:00"
    o.expedientes["EXP-0003"] = a1; o.expedientes["EXP-0003"]["expediente_id"] = "EXP-0003"
    orden = [x["ref"] for x in cola_aprobaciones(o, AHORA) if x["tipo"] == "AUTORIZAR"]
    h.chk("cola_ordena_por_instante_no_por_texto", orden[0] == "EXP-0003", orden)
    o = nuevo(); hasta(o, "EN_ANALISIS")
    for _ in range(3):
        o.barrer("2026-11-06T21:00:00+00:00")
    for _ in range(3):
        o.registrar_gasto("EV-ENC-0001", 99.0, 1, "2026-11-06T21:00:00+00:00")
    h.chk("avisos_iguales_no_se_multiplican", sorted(a["codigo"] for a in o.avisos).count("O-10") == 1 and sorted(a["codigo"] for a in o.avisos).count("O-08") == 1, [a["codigo"] for a in o.avisos])
    o = nuevo(); hasta(o, "EJECUTADA"); o.posicion_transicion("POS-EXP-0001", "EN_REVISION", "H", AHORA)
    h.chk("posicion_en_revision_es_ambar", comp(o, "decisiones") == "AMBAR")
    o = nuevo()
    for mala in (None, "2026-11-06T09:00:00", 123):
        try:
            r = cola_aprobaciones(o, mala)
            h.chk(f"cola_no_lanza_{mala!r}", r and r[0]["tipo"] == "ERROR")
        except Exception as ex:   # noqa: BLE001
            h.chk(f"cola_no_lanza_{mala!r}", False, type(ex).__name__)
    o = nuevo(); hasta(o, "PROPUESTA"); o.ultimo_ahora = "2026-11-08T11:00:00+00:00"
    h.chk("panel_no_usa_reloj_anterior_al_del_orquestador", comp(o, "decisiones", "2026-11-06T09:00:00+00:00") == "AMBAR")
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO CONSOLA:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
