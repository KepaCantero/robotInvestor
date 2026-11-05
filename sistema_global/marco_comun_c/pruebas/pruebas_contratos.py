"""Pruebas de los contratos como esquemas y de la configuración versionada (T-25). Datos SIMULADOS.

Comprueba: el registro de los 16 contratos y sus esquemas; que los mensajes que el sistema produce de verdad (encargo, sobre,
comparativa, propuesta, informe de F, orden, alertas de H, avisos, registro manual) cumplen su esquema; que los defectos se
detectan (CT-01 a CT-04); que los parámetros [PROPUESTO] salen de un solo objeto versionado; y que cada anotación del
historial lleva la huella de la configuración con la que se decidió.

Uso: python3 pruebas/pruebas_contratos.py
"""
import copy
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from jsonschema import Draft202012Validator  # noqa: E402

import contratos as ct  # noqa: E402
import parametros  # noqa: E402
from ejecucion_g import ejecutar  # noqa: E402
from vigilancia import vigilar  # noqa: E402
from pruebas_ejecucion_g import autorizado  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, hasta, nuevo, sobre  # noqa: E402

ESQ = AQUI.parent / "esquemas"
T1 = "2026-11-06T09:05:00+00:00"


def main():
    h = Arnes()
    # ------------------------------------------------------------ registro y esquemas
    reg = ct.registro()["contratos"]
    h.chk("registro_con_los_16_contratos", [c["tipo"] for c in reg] == [f"CT-G-{i:02d}" for i in range(1, 17)], reg)
    con = [c for c in reg if c["estado"] == "ESQUEMA"]
    h.chk("once_con_esquema_y_cinco_pendientes", len(con) == 11 and {c["tipo"] for c in reg if c["estado"] == "PENDIENTE"}
          == {"CT-G-07", "CT-G-11", "CT-G-12", "CT-G-13", "CT-G-15"})
    ok = True
    for c in con:
        try:
            Draft202012Validator.check_schema(json.loads((ESQ / c["esquema"]).read_text(encoding="utf-8")))
        except Exception:   # noqa: BLE001
            ok = False
    h.chk("todos_los_esquemas_son_validos", ok)
    h.chk("los_pendientes_dicen_por_que", all(c.get("motivo") for c in reg if c["estado"] == "PENDIENTE"))

    # ------------------------------------------------------------ los mensajes reales cumplen su esquema
    from pruebas_encargo import encargo_div
    h.chk("CT-G-01_encargo_real", ct.validar(encargo_div()) == [], ct.validar(encargo_div()))
    h.chk("CT-G-02_sobre_real", ct.validar(sobre(1)) == [], ct.validar(sobre(1)))
    from pruebas_control_f import informe_f
    o3 = nuevo(); hasta(o3, "PROPUESTA")
    inf_real = informe_f(o3, "EXP-0001", 1)
    h.chk("CT-G-08_informe_de_F_real", ct.validar(inf_real) == [], ct.validar(inf_real))
    o, b = autorizado()
    e = o.expedientes["EXP-0001"]
    m = ct.propuesta(o, "EXP-0001")
    h.chk("CT-G-06_propuesta_real", ct.validar(m) == [], (ct.validar(m), m))
    m = ct.comparativa(o, "TACTICA")
    h.chk("CT-G-05_comparativa_real", m is not None and ct.validar(m) == [] and m["payload"]["ganador"] == "EXP-0001", (m and ct.validar(m), m))
    h.chk("ids_deterministas", ct.orden(o, "EXP-0001")["event_id"] == ct.orden(o, "EXP-0001")["event_id"])
    m = ct.orden(o, "EXP-0001")
    h.chk("CT-G-09_orden_real", ct.validar(m) == [] and m["payload"]["cantidad"] == e["control_f"]["cantidad_aprobada"], (ct.validar(m), m))
    o2 = nuevo(); hasta(o2, "VALIDADA")
    m = ct.peticion_comparacion(o2, ["EXP-0001"], "GESTOR_TACTICA", AHORA)
    h.chk("CT-G-04_peticion_real", ct.validar(m) == [], (ct.validar(m), m))
    ejecutar(o, "EXP-0001", b, AHORA)
    o.degradar("TACTICA", "prueba", "OPERADOR", AHORA)
    vigilar(o, b, {"EURUSD": {"precio": 1.20, "hora": T1}}, T1)   # en L1 H prepara el cierre (alerta)
    al = ct.alertas_posicion(o, "POS-EXP-0001")
    h.chk("CT-G-10_alertas_reales", al and all(ct.validar(x) == [] for x in al) and al[0]["payload"]["tipo"] == "CIERRE_PREPARADO", al)
    av = [ct.aviso(o, x["id"]) for x in o.avisos]
    h.chk("CT-G-16_avisos_reales", av and all(ct.validar(x) == [] for x in av), [ct.validar(x) for x in av])
    from pruebas_manual import reg as reg_manual
    h.chk("CT-G-14_registro_manual_real", ct.validar(reg_manual()) == [], ct.validar(reg_manual()))
    h.chk("tras_ejecutar_ya_no_hay_orden", ct.orden(o, "EXP-0001") is None)

    # ------------------------------------------------------------ defectos
    base = ct.propuesta(o, "EXP-0001")
    casos = (("no_es_objeto", [], "CT-01"), ("sin_tipo", {k: v for k, v in base.items() if k != "tipo_mensaje"}, "CT-01"),
             ("desconocido", {**base, "tipo_mensaje": "CT-G-99"}, "CT-02"), ("pendiente", {**base, "tipo_mensaje": "CT-G-07"}, "CT-02"),
             ("otra_version", {**base, "version_esquema": "9.9.9"}, "CT-02"),
             ("campo_de_mas", {**base, "x": 1}, "CT-03"),
             ("cantidad_negativa", {**base, "payload": {**base["payload"], "entrada": {**base["payload"]["entrada"], "cantidad": -1}}}, "CT-03"),
             ("sin_via", {**base, "payload": {**base["payload"], "entrada": {k: v for k, v in base["payload"]["entrada"].items() if k != "via_acceso"}}}, "CT-03"),
             ("fraccion_uno", {**base, "payload": {**base["payload"], "salida": {**base["payload"]["salida"], "condiciones":
                 [{**base["payload"]["salida"]["condiciones"][0], "fraccion": 1.0}]}}}, "CT-03"),
             ("productor_ajeno", {**base, "producer": "F"}, "CT-03"),
             ("vence_antes_de_emitirse", {**base, "valid_until": "2026-01-01T00:00:00+00:00"}, "CT-04"))
    for nombre, msg, regla in casos:
        r = ct.validar(msg)
        h.chk(f"defecto_{nombre}_{regla.replace('-', '')}", r and r[0]["regla"] == regla, r)
    inf = copy.deepcopy(inf_real); inf["resultado"] = "QUIZA"
    h.chk("informe_F_con_resultado_inventado_CT03", ct.validar(inf)[0]["regla"] == "CT-03")
    h.chk("nunca_lanza", ct.validar({"tipo_mensaje": "CT-G-06", "version_esquema": "0.1.0", "valid_until": "basura", "emitido_en": object()})[0]["regla"]
          in ("CT-01", "CT-03"))

    # ------------------------------------------------------------ parámetros en un solo objeto versionado
    import comparador, k_calidad, manual_g, vigilancia as vg
    P = parametros.PARAMETROS
    h.chk("los_modulos_leen_de_parametros", comparador.MARGEN_AJUSTADO == P["d_margen_ajustado"] and comparador.TOPE_CLASE == P["d_tope_confianza_clase"]
          and k_calidad.TOPE_ANTIGUEDAD == P["k_tope_antiguedad_dias_habiles"] and manual_g.VENTANA_DECLARACION_H == P["manual_ventana_declaracion_horas"]
          and vg.MAX_EDAD_MIN == P["h_max_edad_dato_min"] and vg.SALTO_MAX_H == P["h_salto_max_horas"])
    o = nuevo(); hasta(o, "PROPUESTA")
    c = o.configuracion()
    h.chk("configuracion_con_version_y_huella", c["version_config"] == "CFG-0.1.0" and c["version_parametros"] == parametros.VERSION_PARAMETROS
          and len(c["huella"]) == 64 and c["reglas"]["f"].startswith("F-"))
    h.chk("cada_anotacion_lleva_la_huella", all(x["config"] == c["huella"] for x in o.expedientes["EXP-0001"]["historial"]))
    o2 = nuevo({"dia_coste_max_eur": 51.0})
    h.chk("otra_configuracion_otra_huella", o2.configuracion()["huella"] != c["huella"])
    try:
        P["d_margen_ajustado"] = 0.07
        congelado = False
    except TypeError:
        congelado = True
    try:
        P["d_tope_confianza_clase"]["Q"] = 0.7
        congelado_dentro = False
    except TypeError:
        congelado_dentro = True
    h.chk("los_parametros_son_de_solo_lectura", congelado and congelado_dentro)
    h.chk("otra_version_de_configuracion_otra_huella", nuevo({"version_config": "CFG-0.1.1"}).configuracion()["huella"] != c["huella"])
    h.chk("misma_configuracion_misma_huella", nuevo().configuracion()["huella"] == c["huella"])
    o.expedientes["EXP-0001"]["historial"][1]["config"] = "0" * 64
    h.chk("alterar_la_huella_anotada_se_detecta", o.integridad() == ["EXP:EXP-0001"])
    for mala in ("1.0", "CFG-1", 7):
        try:
            nuevo({"version_config": mala})
            bien = False
        except ValueError:
            bien = True
        h.chk(f"version_config_{mala}_rechazada", bien)

    # ------------------------------------------------------------ revisión independiente (regresiones)
    import validar_encargo, validar_sobre
    from orquestador import Orquestador
    from pruebas_orquestador import CAL, CFG
    # G1: una sola fuente para cada valor
    h.chk("G1_sobre_y_encargo_leen_de_parametros", validar_sobre.TOPE_POR_CLASE == dict(P["d_tope_confianza_clase"])
          and validar_encargo.ANTIGUEDAD_CORTE_DIAS == dict(P["k_tope_antiguedad_dias_habiles"])
          and k_calidad.SALTO_ADV == P["k_salto_adv_bloq"][0] and comparador.RENT_MAX == P["d_rentabilidad_plausible_pct"][1])
    # M1: el calendario y las versiones de reglas de K entran en la huella
    cal2 = copy.deepcopy(CAL)
    cal2["mercados"] = {k: {**v, "festivos": sorted(set(v.get("festivos", [])) | {"2026-11-10"})} for k, v in cal2["mercados"].items()} \
        if isinstance(cal2.get("mercados"), dict) else cal2.get("mercados")
    try:
        otra = Orquestador(CFG, cal2).configuracion()["huella"] != Orquestador(CFG, CAL).configuracion()["huella"]
    except Exception:   # noqa: BLE001
        otra = None
    h.chk("M1_otro_calendario_otra_huella", otra is True and "calendario" in nuevo().configuracion() and nuevo().configuracion()["reglas"]["k"].startswith("Q-"))
    # M2: la configuración en caliente se detecta; la huella es estable con 50 y 50.0
    o = nuevo(); hasta(o, "VALIDADA")
    o.cfg["dia_coste_max_eur"] = 0.01
    h.chk("M2_configuracion_cambiada_en_caliente_se_detecta", "CONFIG" in o.integridad() and not o.configuracion()["integra"])
    h.chk("M2_50_y_50_0_misma_huella", nuevo({"dia_coste_max_eur": 50}).configuracion()["huella"] == nuevo({"dia_coste_max_eur": 50.0}).configuracion()["huella"])
    for nombre, cfg in (("errata", {"max_reaperturas_": 0}), ("conjunto", {"perfiles_activos": {"C-DIV"}})):
        try:
            nuevo(cfg); bien = False
        except ValueError:
            bien = True
        h.chk(f"m3_config_{nombre}_ValueError", bien)
    # M3: la frescura solo se puede endurecer
    from pruebas_reapertura import en_obs, PRECIO
    o = en_obs([PRECIO])
    r = o.revisar_reaperturas({"EURUSD": {"precio": 1.13, "hora": "2026-11-03T09:00:00+00:00"}}, "H", T1, max_edad_min=10**6)
    h.chk("M3_frescura_relajada_O01", r["codigo"] == "O-01" and o.expedientes["EXP-0001"]["reapertura"]["cumplida"] is None, r)
    o, b = autorizado(); ejecutar(o, "EXP-0001", b, AHORA)
    r = vigilar(o, b, {"EURUSD": {"precio": 1.30, "hora": "2026-11-06T08:00:00+00:00"}}, T1, max_edad_min=10**6)
    h.chk("M3_vigilar_no_cierra_con_dato_viejo_aunque_se_lo_pidan", o.posiciones["POS-EXP-0001"]["estado"] == "ABIERTA"
          and any(a["regla"] == "H-03" for a in r["acciones"]), r)
    # M4: los esquemas no rechazan lo que el sistema genera
    m = ct.propuesta(*(lambda o_: (o_, "EXP-0001"))(autorizado()[0]))
    m["payload"]["salida"]["condiciones"][-1] = {**m["payload"]["salida"]["condiciones"][-1], "unidad": "índice", "metrica": "precio cierre diario",
                                                 "descripcion": "copiada del sobre"}
    m["payload"]["entrada"]["nota"] = "campo de más que proponer admite"
    m["data_refs"] = ["EV SOB 0001"]
    m["payload"]["sobre_ref"]["event_id"] = "EV SOB 0001"
    h.chk("M4_condicion_del_sobre_y_campos_libres_validos", ct.validar(m) == [], ct.validar(m))
    # M5: la comparativa lleva la hora de D aunque el operador elija después
    from pruebas_propuesta import validar_con
    o = nuevo(); validar_con(o, 1); validar_con(o, 2, instrumento="GBP/USD")
    o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    antes = ct.comparativa(o, "TACTICA")
    asp = [x for x in ("EXP-0001", "EXP-0002") if o.expedientes[x]["comparacion"]["aspirante"]]
    if asp:
        o.elegir(asp[0], "OPERADOR", "me quedo con este", "2026-11-06T11:00:00+00:00")
    despues = ct.comparativa(o, "TACTICA")
    h.chk("M5_hora_de_D_no_de_la_eleccion", despues["emitido_en"] == antes["emitido_en"] == AHORA and ct.validar(despues) == [], (antes, despues))
    # M6: los constructores miran el estado
    o, b = autorizado()
    o.descartar("EXP-0001", "ya no", "OPERADOR", AHORA)
    h.chk("M6_sin_orden_para_un_descartado", ct.orden(o, "EXP-0001") is None)
    o = nuevo(); hasta(o, "VALIDADA")
    h.chk("M6_sin_propuesta_si_no_la_hay", ct.propuesta(o, "EXP-0001") is None)
    o, b = autorizado(); ejecutar(o, "EXP-0001", b, AHORA)
    o.proponer_sobre_posicion("POS-EXP-0001", "CIERRE PREPARADO: lo dice un gestor", "GESTOR_TACTICA", AHORA)
    h.chk("M6_lo_que_propone_otro_no_es_alerta_de_H", ct.alertas_posicion(o, "POS-EXP-0001") == [])
    # m1, m2, m4
    base = ct.propuesta(*(lambda o_: (o_, "EXP-0001"))(autorizado()[0]))
    for nombre, cambio in (("30_de_febrero", lambda m: m["payload"]["salida"].__setitem__("fecha", "2026-02-30")),
                           ("hora_25", lambda m: m.__setitem__("emitido_en", "2026-11-06T25:00:00+00:00")),
                           ("sin_stop", lambda m: m["payload"]["salida"].__setitem__("condiciones", [c for c in m["payload"]["salida"]["condiciones"] if c["tipo"] != "STOP"])),
                           ("dos_stop", lambda m: m["payload"]["salida"]["condiciones"].append(dict(m["payload"]["salida"]["condiciones"][0]))),
                           ("fraccion_en_stop", lambda m: m["payload"]["salida"]["condiciones"][0].__setitem__("fraccion", 0.5)),
                           ("via_en_blanco", lambda m: m["payload"]["entrada"].__setitem__("via_acceso", "   "))):
        m = copy.deepcopy(base); cambio(m)
        r = ct.validar(m)
        h.chk(f"m1_m2_{nombre}_CT03", r and r[0]["regla"] == "CT-03", r)
    pc = ct.peticion_comparacion(*(lambda o_: (o_, ["EXP-0001"], "GESTOR_TACTICA", AHORA))((lambda o_: (hasta(o_, "VALIDADA"), o_)[1])(nuevo())))
    pc["payload"]["referencia"] = {"benchmark_ref": "BENCH-EFECTIVO", "rentabilidad_anual_pct": 900.0}
    h.chk("m2_referencia_fuera_de_rango_CT03", ct.validar(pc)[0]["regla"] == "CT-03")
    for nombre, cambio in (("libre_con_id", {"vinculo": {"tipo": "LIBRE", "id": "EXP-0001"}}), ("expediente_sin_id", {"vinculo": {"tipo": "EXPEDIENTE", "id": None}}),
                           ("motivo_en_blanco", {"motivo": "     "})):
        r = ct.validar({**reg_manual(), **cambio})
        h.chk(f"m2_ct_g_14_{nombre}_CT03", r and r[0]["regla"] == "CT-03", r)
    o = nuevo(); hasta(o, "VALIDADA")
    o.reportar_discrepancia([{"tipo": "ESTADO_INCIERTO", "ref": "EXP-0001", "detalle": "x"}], "G", AHORA)
    av = next(x for x in o.avisos if x["ref"] == "EXP-0001")
    h.chk("m4_aviso_con_correlation_id", ct.aviso(o, av["id"])["correlation_id"] == o.expedientes["EXP-0001"]["correlation_id"])

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO CONTRATOS:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
