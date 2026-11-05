"""Pruebas de T-24 (aprobación del operador con importe tecleado, §6), del kill-switch (§8, §11) y de la escalada de avisos."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validador"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ejecucion_g import cerrar, conciliar, ejecutar, kill_switch  # noqa: E402
from vigilancia import vigilar  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_ejecucion_g import autorizado, broker  # noqa: E402
from pruebas_orquestador import AHORA, CAL, CFG, Arnes, autorizar_op, hasta, nuevo  # noqa: E402

EID, PID = "EXP-0001", "POS-EXP-0001"
T = lambda m: f"2026-11-06T{9 + m // 60:02d}:{m % 60:02d}:00+00:00"   # noqa: E731 - minutos tras las 09:00
L2 = {"nivel_autonomia": {"TRADING": "L2", "TACTICA": "L2", "LARGO_PLAZO": "L2"}}


def propuesta(cfg=None):
    o = nuevo(cfg)
    hasta(o, "PROPUESTA")
    return o


def aprob(p, **kw):
    a = {"pantalla_hash": p["hash"], "importe_tecleado": p["importe"], "canal": "CONSOLA", "segundo_factor": True}
    a.update(kw)
    return a


def main():
    h = Arnes()
    # ---------------------------------------------------------------- pantalla y aprobación
    o = propuesta(); F = informe_f(o)
    r = o.pantalla_aprobacion(EID, F, AHORA)
    p = r["pantalla"]
    h.chk("pantalla_solo_con_cifras_de_F", r["ok"] and p["importe"] == 110.0 and p["riesgo"] == 5.0 and p["cantidad"] == 100.0
          and p["resultado_f"] == "APROBADO" and p["motivos_enfriamiento"] == [] and not any(k in p for k in ("texto", "resumen", "tesis")), p)
    for nombre, ap, cod in (("sin_aprobacion_O27", None, "O-27"), ("importe_mal_tecleado_O27", aprob(p, importe_tecleado=111.0), "O-27"),
                            ("importe_texto_O27", aprob(p, importe_tecleado="110"), "O-27"), ("hash_de_otra_pantalla_O27", aprob(p, pantalla_hash="x" * 64), "O-27"),
                            ("canal_chat_O05", aprob(p, canal="CHAT"), "O-05"), ("sin_segundo_factor_O05", aprob(p, segundo_factor=False), "O-05"),
                            ("campos_de_mas_O27", {**aprob(p), "extra": 1}, "O-27")):
        r = o.autorizar(EID, "OPERADOR", F, AHORA, ap)
        h.chk(nombre, r["codigo"] == cod and o.expedientes[EID]["estado"] == "PROPUESTA", r)
    h.chk("caducada_no_se_actua_O10", o.autorizar(EID, "OPERADOR", F, T(16), aprob(p))["codigo"] == "O-10")
    o = propuesta(); F = informe_f(o); p = o.pantalla_aprobacion(EID, F, AHORA)["pantalla"]
    Fb = informe_f(o, cartera={"perdida_dia_eur": 500.0})   # mismo event_id, otro contenido
    h.chk("mismo_id_de_informe_otro_contenido_O27", Fb["event_id"] == F["event_id"] and o.autorizar(EID, "OPERADOR", Fb, AHORA, aprob(p))["codigo"] == "O-27")
    h.chk("pantalla_solo_la_pide_el_operador_O05", o.pantalla_aprobacion(EID, F, AHORA, actor="BROKER")["codigo"] == "O-05")
    F2 = informe_f(o, n=7)
    h.chk("pantalla_de_otro_informe_O27", o.autorizar(EID, "OPERADOR", F2, AHORA, aprob(p))["codigo"] == "O-27")
    o.pantallas[EID]["importe"] = 1.0   # alguien toca la pantalla guardada
    h.chk("pantalla_alterada_O27", o.autorizar(EID, "OPERADOR", F, AHORA, aprob(p, importe_tecleado=1.0))["codigo"] == "O-27")
    o = propuesta(); F = informe_f(o); p = o.pantalla_aprobacion(EID, F, AHORA)["pantalla"]
    r = o.autorizar(EID, "OPERADOR", F, T(5), aprob(p))
    h.chk("aprobacion_correcta", r["ok"] and o.pantallas[EID]["usada"] and o.expedientes[EID]["control_f"]["aprobacion"]["importe"] == 110.0
          and o.integridad() == [], r)
    o2 = copy.deepcopy(o)
    o2.expedientes[EID]["control_f"]["aprobacion"]["importe"] = 5.0
    h.chk("aprobacion_guardada_alterada_se_detecta", o2.integridad() == [f"EXP:{EID}"])
    o = propuesta(); F = informe_f(o); p = o.pantalla_aprobacion(EID, F, AHORA)["pantalla"]
    o.pantallas[EID]["usada"] = True
    h.chk("aprobacion_ya_usada_O03", o.autorizar(EID, "OPERADOR", F, AHORA, aprob(p))["codigo"] == "O-03")
    # enfriamiento
    o = propuesta(); F = informe_f(o, cartera={"perdida_dia_eur": 100.0})
    p = o.pantalla_aprobacion(EID, F, AHORA)["pantalla"]
    h.chk("perdida_del_dia_activa_enfriamiento", p["motivos_enfriamiento"] == ["pérdida en el día"] and p["enfriamiento_hasta"] == "2026-11-06T09:30:00+00:00", p)
    h.chk("en_enfriamiento_O28", o.autorizar(EID, "OPERADOR", F, T(10), aprob(p))["codigo"] == "O-28")
    h.chk("tras_el_enfriamiento_si", o.autorizar(EID, "OPERADOR", F, T(31), aprob(p))["ok"])
    from orquestador import CONFIG_DEFECTO
    ap_cfg = {**CONFIG_DEFECTO["aprobacion"], "horario_utc": ["10:00", "21:00"]}
    o = propuesta({"aprobacion": ap_cfg}); F = informe_f(o)
    p = o.pantalla_aprobacion(EID, F, AHORA)["pantalla"]
    h.chk("fuera_de_horario_activa_enfriamiento", p["motivos_enfriamiento"] == ["fuera de horario"]
          and o.autorizar(EID, "OPERADOR", F, AHORA, aprob(p))["codigo"] == "O-28", p)
    ap_cfg2 = {**CONFIG_DEFECTO["aprobacion"], "horario_utc": ["07:00", "09:05"]}
    o = propuesta({"aprobacion": ap_cfg2}); F = informe_f(o)
    p = o.pantalla_aprobacion(EID, F, T(4))["pantalla"]   # 09:04, dentro de horario
    h.chk("aprobar_ya_fuera_de_horario_exige_enfriamiento_O28", p["motivos_enfriamiento"] == [] and o.autorizar(EID, "OPERADOR", F, T(10), aprob(p))["codigo"] == "O-28")
    ap_cfg3 = {**CONFIG_DEFECTO["aprobacion"], "horario_utc": ["22:00", "10:00"]}   # cruza la medianoche: las 09:00 están dentro
    o = propuesta({"aprobacion": ap_cfg3}); F = informe_f(o)
    h.chk("horario_que_cruza_la_medianoche", o.pantalla_aprobacion(EID, F, AHORA)["pantalla"]["motivos_enfriamiento"] == [])
    o = propuesta({"matriz_autonomia": {"TACTICA": True}, **L2})
    h.chk("la_matriz_no_necesita_pantalla", o.autorizar(EID, "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["ok"]
          and o.expedientes[EID]["control_f"]["aprobacion"] is None)
    from orquestador import Orquestador
    for nombre, c in (("canal_chat", {"aprobacion": {**CONFIG_DEFECTO["aprobacion"], "canales": ["CHAT"]}}),
                      ("hora_mala", {"aprobacion": {**CONFIG_DEFECTO["aprobacion"], "horario_utc": ["25:00", "21:00"]}}),
                      ("avisos_por_chat", {"avisos": {**CONFIG_DEFECTO["avisos"], "canal_alta": "chat"}}),
                      ("escalar_cero", {"avisos": {**CONFIG_DEFECTO["avisos"], "escalar_tras": 0}}),
                      ("kill_negativo", {"kill_switch": {"periodo_min_l1_horas": -1}}),
                      ("escalado_igual_que_alta", {"avisos": {**CONFIG_DEFECTO["avisos"], "canal_escalado": "CONSOLA"}}),
                      ("horario_vacio", {"aprobacion": {**CONFIG_DEFECTO["aprobacion"], "horario_utc": ["09:00", "09:00"]}})):
        try:
            Orquestador({**CFG, **c}, CAL); h.chk(f"config_{nombre}_se_rechaza", False)
        except ValueError:
            h.chk(f"config_{nombre}_se_rechaza", True)
    # ---------------------------------------------------------------- kill-switch
    o = nuevo(L2)
    h.chk("kill_solo_operador_orquestador_o_vigilante_O05", o.activar_kill_switch("x", "G", AHORA)["codigo"] == "O-05")
    h.chk("kill_sin_motivo_O15", o.activar_kill_switch(" ", "OPERADOR", AHORA)["codigo"] == "O-15")
    o, b = autorizado(b=broker(precio=1.12), o=nuevo(L2))
    assert ejecutar(o, EID, b, AHORA)["codigo"] == "G-11"
    r = kill_switch(o, b, T(1), "prueba manual")
    h.chk("kill_cancela_las_entradas_vivas", r["ok"] and r["entradas"] == {EID: "G-02"} and b.consultar("ORD-EXP-0001-E-1")["estado"] == "CANCELADA"
          and o.expedientes[EID]["orden_entrada"]["estado"] == "CANCELADA", r)
    h.chk("kill_pasa_todo_a_L1_y_avisa", all(o.nivel(c) == "L1" for c in ("TRADING", "TACTICA", "LARGO_PLAZO"))
          and any(x["codigo"] == "O-26" and x["prioridad"] == "ALTA" and x["canal"] == "CONSOLA" for x in o.avisos))
    h.chk("kill_bloquea_nuevas_entradas", ejecutar(o, EID, b, T(2))["codigo"] == "G-06" and len(b.ordenes) == 1)
    o2 = propuesta(); o2.activar_kill_switch("x", "OPERADOR", AHORA)
    h.chk("kill_bloquea_aprobaciones_O26", autorizar_op(o2, EID, informe_f(o2))["codigo"] == "O-26")
    h.chk("kill_dos_veces_O02", o2.activar_kill_switch("y", "VIGILANTE", AHORA)["codigo"] == "O-02")
    o, b = autorizado(o=nuevo(L2)); ejecutar(o, EID, b, AHORA)
    kill_switch(o, b, T(1), "prueba")
    h.chk("kill_no_toca_protecciones_ni_posiciones", b.consultar("ORD-EXP-0001-S-1")["estado"] == "ACEPTADA" and o.posiciones[PID]["estado"] == "ABIERTA"
          and len(b.posiciones()) == 1)
    h.chk("con_kill_se_puede_cerrar", cerrar(o, PID, b, T(2), actor="OPERADOR", motivo="cierro con el kill-switch activo")["ok"])
    # rearme
    lista = {k: True for k in ("causa_corregida", "conciliacion_limpia", "datos_frescos", "protecciones_verificadas")}
    h.chk("rearmar_solo_operador_O05", o.rearmar_kill_switch(lista, "ORQUESTADOR", T(3))["codigo"] == "O-05")
    h.chk("rearmar_lista_incompleta_O06", o.rearmar_kill_switch({**lista, "datos_frescos": False}, "OPERADOR", T(3))["codigo"] == "O-06")
    h.chk("rearmar_con_avisos_altos_sin_acusar_O06", o.rearmar_kill_switch(lista, "OPERADOR", T(3))["codigo"] == "O-06")
    for av in list(o.avisos):
        o.acusar_aviso(av["id"], "OPERADOR", T(3))
    h.chk("rearmar_sin_conciliacion_limpia_posterior_O06", o.rearmar_kill_switch(lista, "OPERADOR", T(3))["codigo"] == "O-06")
    h.chk("conciliacion_limpia", conciliar(o, b, T(4))["ok"])
    h.chk("rearmar_ok", o.rearmar_kill_switch(lista, "OPERADOR", T(4))["ok"] and o.kill is None and len(o.rearmes) == 1)
    h.chk("rearmar_sin_kill_O12", o.rearmar_kill_switch(lista, "OPERADOR", T(4))["codigo"] == "O-12")
    h.chk("tras_el_rearme_sigue_en_L1_O26", o.restablecer_nivel("TACTICA", "OPERADOR", T(5))["codigo"] == "O-26" and o.nivel("TACTICA") == "L1")
    h.chk("tras_el_periodo_minimo_se_restablece", o.restablecer_nivel("TACTICA", "OPERADOR", "2026-11-07T09:10:00+00:00")["ok"] and o.nivel("TACTICA") == "L2")
    # rearme con una entrada que no se pudo cancelar; y lo aprobado antes del kill no se envía tras el rearme
    o, b = autorizado(b=broker(precio=1.12), o=nuevo(L2))
    ejecutar(o, EID, b, AHORA)
    b.caido = True
    r = kill_switch(o, b, T(1), "prueba")
    h.chk("kill_sin_conexion_no_cancela_y_lo_dice", not r["ok"] and r["entradas"] == {EID: "G-01"}, r)
    b.caido = False
    for av in list(o.avisos):
        o.acusar_aviso(av["id"], "OPERADOR", T(2))
    conciliar(o, b, T(2))
    h.chk("rearmar_con_entrada_viva_O06", o.rearmar_kill_switch(lista, "OPERADOR", T(3))["codigo"] == "O-06" and "EXP-0001" in o.rearmar_kill_switch(lista, "OPERADOR", T(3))["motivo"])
    from ejecucion_g import revisar_entrada
    revisar_entrada(o, EID, b, T(4))   # ahora sí se cancela
    conciliar(o, b, T(4))
    for av in list(o.avisos):
        o.acusar_aviso(av["id"], "OPERADOR", T(4))
    h.chk("rearmar_tras_cancelar", o.rearmar_kill_switch(lista, "OPERADOR", T(5))["ok"])
    r = ejecutar(o, EID, b, T(6))
    h.chk("lo_aprobado_antes_del_kill_no_se_envia_tras_el_rearme", r["codigo"] == "G-06" and "kill" in r["motivo"] and len(b.ordenes) == 1, r)
    # desencadenantes automáticos
    o, b = autorizado(o=nuevo(L2)); ejecutar(o, EID, b, AHORA)
    b.pos["EURUSD"]["cantidad"] = 150.0
    conciliar(o, b, T(1))
    h.chk("discrepancia_sin_explicar_activa_el_kill", o.kill is not None and o.kill["actor"] == "ORQUESTADOR" and "CANTIDAD" in o.kill["motivo"])
    o, b = autorizado(b=broker(precio=1.12), o=nuevo(L2)); ejecutar(o, EID, b, AHORA)
    b.pos["GBPUSD"] = {"cantidad": 10.0, "activo_base": "GBP"}
    conciliar(o, b, T(1))
    h.chk("el_kill_automatico_cancela_en_el_acto_las_entradas", o.kill is not None and b.consultar("ORD-EXP-0001-E-1")["estado"] == "CANCELADA")
    o, b = autorizado(o=nuevo(L2)); ejecutar(o, EID, b, AHORA)
    b.mover_precio("EURUSD", 1.04, T(1))
    c = conciliar(o, b, T(1))
    h.chk("stop_ejecutado_pendiente_de_H_no_es_falso_positivo", c["ok"] and [x["tipo"] for x in c["explicadas"]] == ["STOP_EJECUTADO"] and o.kill is None, c)
    o, b = autorizado(o=nuevo(L2)); ejecutar(o, EID, b, AHORA)
    vigilar(o, b, {"EURUSD": {"precio": 1.10, "hora": "2026-11-06T07:00:00+00:00"}}, T(1))
    h.chk("dato_viejo_degrada_pero_no_activa_el_kill", o.kill is None and "TACTICA" in o.degradadas)
    o, b = autorizado(b=broker(precio=1.12), o=nuevo(L2))
    ejecutar(o, EID, b, AHORA)
    o.activar_kill_switch("vigilante sin latido", "VIGILANTE", T(1))
    v = vigilar(o, b, {"EURUSD": {"precio": 1.12, "hora": T(2)}}, T(2))
    h.chk("con_kill_la_vigilancia_cancela_lo_que_quede_vivo", v["acciones"][0]["codigo"] == "G-02" and b.consultar("ORD-EXP-0001-E-1")["estado"] == "CANCELADA", v)
    # ---------------------------------------------------------------- avisos: reiteración y escalada
    o = nuevo(); o.activar_kill_switch("x", "OPERADOR", AHORA)
    av = next(x for x in o.avisos if x["codigo"] == "O-26")
    o.barrer(T(10))
    h.chk("antes_de_15_min_no_se_reitera", av["reiteraciones"] == [])
    for m in (16, 32, 48):
        o.barrer(T(m))
    av = next(x for x in o.avisos if x["codigo"] == "O-26")
    h.chk("se_reitera_y_escala_tras_tres", len(av["reiteraciones"]) == 3 and av["escalado"], av)
    o.acusar_aviso(av["id"], "OPERADOR", T(50))
    o.barrer(T(70))
    h.chk("acusado_deja_de_reiterarse", len(next(x for x in o.avisos if x["codigo"] == "O-26")["reiteraciones"]) == 3)
    o = nuevo(); o.activar_kill_switch("x", "OPERADOR", AHORA)
    o.barrer(T(180))   # un solo barrido tres horas después
    av = next(x for x in o.avisos if x["codigo"] == "O-26")
    h.chk("barrido_tardio_escala_igual_y_cambia_de_canal", av["escalado"] and av["canal"] == "ESCALADO", av)
    o = nuevo(); o._aviso("O-20", "media", AHORA)
    o.barrer(T(60))
    h.chk("los_de_prioridad_media_no_se_reiteran", o.avisos[0]["reiteraciones"] == [])
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO APROBACION:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
