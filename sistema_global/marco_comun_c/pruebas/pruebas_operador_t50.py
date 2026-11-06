"""Pruebas de T-50: controles sobre el operador (Constitución §6.2 y §6.3).
El operador puede anular un veto de F (solo los anulables, con motivo, enfriamiento, canal y segundo factor, y dentro del límite
mensual) y ajustar el límite de pérdida del día (bajarlo siempre; subirlo nunca el mismo día en que se alcanzó). Datos SIMULADOS."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

import contratos as ct  # noqa: E402
from control_f import aplanar_informe  # noqa: E402
from orquestador import Orquestador, VETOS_ANULABLES  # noqa: E402
from pruebas_control_f import CART, informe_f, registrar_foto  # noqa: E402
from validar_sobre import _dt  # noqa: E402
from ejecucion_g import ejecutar  # noqa: E402
from pruebas_ejecucion_g import broker  # noqa: E402
from pruebas_orquestador import AHORA, CAL, CFG, Arnes, autorizar_op, hasta, nuevo  # noqa: E402

T_ESPERA = "2026-11-06T09:31:00+00:00"   # pasado el enfriamiento (30 min [PROPUESTO])
T_TARDE = "2026-11-06T12:00:00+00:00"
T_MANANA = "2026-11-07T08:00:00+00:00"
MOTIVO = "Oportunidad revisada a mano: el tope de posiciones se cumple al cerrar otra hoy"
POS10 = [{"instrumento": f"XAU{i}", "activo_base": f"X{i:02d}", "valor_eur": 100.0} for i in range(10)]   # F-09: 10 posiciones
OK2F = {"canal": "CONSOLA", "segundo_factor": True}


def aprobacion(p, **kw):
    return {"pantalla_hash": p["hash"], "importe_tecleado": p["importe"], "canal": "CONSOLA", "segundo_factor": True, **kw}


def vetado(o, eid="EXP-0001", n=1, **cart):
    return informe_f(o, eid, n, cartera={"posiciones": POS10, **cart})


def anular(o, inf, eid="EXP-0001", motivo=MOTIVO, t1=AHORA, t2=T_ESPERA):
    r = o.pantalla_aprobacion(eid, inf, t1, anular_veto={"motivo": motivo})
    if not r["ok"]:
        return r
    return o.autorizar(eid, "OPERADOR", inf, t2, aprobacion(r["pantalla"]))


def main():
    h = Arnes()

    # ================================================================ §6.2 anulación de veto
    o = nuevo(); hasta(o, "PROPUESTA")
    inf = vetado(o)
    cf = aplanar_informe(inf)
    h.chk("F_veta_por_F09", cf["resultado"] == "VETADO" and [c["regla"] for c in cf["controles"] if c["resultado"] == "VETA"] == ["F-09"])
    r = o.pantalla_aprobacion("EXP-0001", inf, AHORA, anular_veto={"motivo": "porque sí"})
    h.chk("anular_exige_motivo_O15", r["codigo"] == "O-15", r)
    for nombre, av in (("sin_dict", "motivo largo de sobra para pasar"), ("clave_extra", {"motivo": MOTIVO, "cantidad": 500}),
                       ("motivo_no_texto", {"motivo": 12345678901234567})):
        h.chk(f"anular_mal_formado_{nombre}_O15", o.pantalla_aprobacion("EXP-0001", inf, AHORA, anular_veto=av)["codigo"] == "O-15")
    r = o.pantalla_aprobacion("EXP-0001", inf, AHORA, anular_veto={"motivo": MOTIVO})
    p = r["pantalla"]
    h.chk("pantalla_de_anulacion", r["ok"] and p["anulacion"] == {"motivo": MOTIVO, "vetos": ["F-09"]} and p["resultado_f"] == "VETADO"
          and p["cantidad"] == 100.0 and "anulación de veto" in p["motivos_enfriamiento"], r)
    h.chk("pantalla_sin_consumir_el_informe", inf["event_id"] not in o.eventos)
    r = o.autorizar("EXP-0001", "OPERADOR", inf, AHORA, aprobacion(p))
    h.chk("anular_siempre_espera_O28", r["codigo"] == "O-28", r)
    r = o.autorizar("EXP-0001", "OPERADOR", inf, T_ESPERA, aprobacion(p, segundo_factor=False))
    h.chk("anular_exige_segundo_factor", r["codigo"] == "O-05", r)
    r = o.autorizar("EXP-0001", "OPERADOR", inf, T_ESPERA, aprobacion(p, importe_tecleado=p["importe"] + 1))
    h.chk("anular_exige_importe_tecleado", r["codigo"] == "O-27", r)
    h.chk("rechazos_no_autorizan", o.expedientes["EXP-0001"]["estado"] == "PROPUESTA" and o.anulaciones_mes(T_ESPERA) == 0)
    r = o.autorizar("EXP-0001", "OPERADOR", inf, T_ESPERA, aprobacion(p))
    e = o.expedientes["EXP-0001"]
    h.chk("anulacion_autoriza", r["ok"] and e["estado"] == "AUTORIZADA" and e["control_f"]["anulacion"] == {"motivo": MOTIVO, "vetos": ["F-09"]}
          and e["control_f"]["cantidad_aprobada"] == 100.0 and e["control_f"]["resultado"] == "VETADO", r)
    h.chk("anulacion_en_la_cadena", e["historial"][-1]["motivo"].startswith("ANULACIÓN DE VETO (F-09") and MOTIVO[:40] in e["historial"][-1]["motivo"]
          and o.integridad() == [], o.integridad())
    h.chk("anulacion_avisa_O34", any(a["codigo"] == "O-34" and a["ref"] == "EXP-0001" for a in o.avisos))
    h.chk("anulacion_cuenta_en_el_mes", o.anulaciones_mes(T_ESPERA) == 1 and o.anulaciones_mes("2026-12-01T00:00:00+00:00") == 0)
    orden = ct.orden(o, "EXP-0001")
    h.chk("orden_con_la_cantidad_anulada", orden["payload"]["cantidad"] == 100.0 and ct.validar(orden) == [], ct.validar(orden))
    h.chk("pantalla_de_un_solo_uso", o.autorizar("EXP-0001", "OPERADOR", inf, T_ESPERA, aprobacion(p))["ok"] is False)
    e2 = copy.deepcopy(e)
    e["historial"][-1]["motivo"] = "control F: VETADO (0.0)"   # borrar la huella de la anulación para que no cuente
    h.chk("ocultar_una_anulacion_se_detecta", o.integridad() != [])
    o.expedientes["EXP-0001"] = e2

    # la cantidad de la anulación no pasa de los topes de F (la solicitada recortada por F-03, F-04, F-06 y F-07)
    o = nuevo(); hasta(o, "PROPUESTA")
    cf = aplanar_informe(vetado(o))
    for c in cf["controles"]:
        if c["regla"] == "F-04":
            c["resultado"], c["limite"] = "REDUCE", 40.1234567
    q, vetos, err = o._comprobar_anulacion(cf, {"motivo": MOTIVO}, _dt(AHORA))
    h.chk("anulacion_acotada_por_los_topes", err is None and q == 40.123456 and vetos == ["F-09"], (q, err))
    for c in cf["controles"]:
        if c["regla"] == "F-04":
            c["limite"] = 0.0
    h.chk("topes_a_cero_no_dejan_anular_O34", o._comprobar_anulacion(cf, {"motivo": MOTIVO}, _dt(AHORA))[2]["codigo"] == "O-34")

    # vetos que no se anulan
    for nombre, cart, regla in (("perdida_del_dia_F08", {"perdida_dia_eur": 2500.0, "posiciones": []}, "F-08"),
                                ("F08_y_F09_juntos", {"perdida_dia_eur": 2500.0}, "F-08")):
        o = nuevo(); hasta(o, "PROPUESTA")
        inf = informe_f(o, cartera={"posiciones": POS10, **cart})
        r = o.pantalla_aprobacion("EXP-0001", inf, AHORA, anular_veto={"motivo": MOTIVO})
        h.chk(f"no_anulable_{nombre}_O34", r["codigo"] == "O-34" and regla in r["motivo"], r)
    h.chk("anulables_declarados", VETOS_ANULABLES == ("F-09", "F-11"))
    o = nuevo(); hasta(o, "PROPUESTA")
    inf = informe_f(o)
    r = o.pantalla_aprobacion("EXP-0001", inf, AHORA, anular_veto={"motivo": MOTIVO})
    h.chk("sin_veto_no_hay_que_anular_O01", r["codigo"] == "O-01", r)
    h.chk("y_la_aprobacion_normal_sigue", autorizar_op(o, "EXP-0001", inf, AHORA)["ok"] and o.expedientes["EXP-0001"]["control_f"]["anulacion"] is None)

    # sin pedir la anulación, el veto consume el informe como antes
    o = nuevo(); hasta(o, "PROPUESTA")
    inf = vetado(o)
    h.chk("veto_sin_anular_O06", o.pantalla_aprobacion("EXP-0001", inf, AHORA)["codigo"] == "O-06")
    h.chk("ese_informe_ya_no_se_anula_O03", o.pantalla_aprobacion("EXP-0001", inf, AHORA, anular_veto={"motivo": MOTIVO})["codigo"] == "O-03")
    # la matriz de autonomía no anula
    o = nuevo({"nivel_autonomia": {"TACTICA": "L2"}, "matriz_autonomia": {"TACTICA": True}}); hasta(o, "PROPUESTA")
    inf = vetado(o)
    h.chk("la_matriz_no_anula", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", inf, AHORA)["codigo"] == "O-06")

    # límite mensual
    o = nuevo({"anulaciones_veto_mes": 0}); hasta(o, "PROPUESTA")
    r = o.pantalla_aprobacion("EXP-0001", vetado(o), AHORA, anular_veto={"motivo": MOTIVO})
    h.chk("limite_cero_O34", r["codigo"] == "O-34" and "mensual" in r["motivo"], r)
    o = nuevo({"anulaciones_veto_mes": 1}); hasta(o, "PROPUESTA")
    inf1 = vetado(o)
    p1 = o.pantalla_aprobacion("EXP-0001", inf1, AHORA, anular_veto={"motivo": MOTIVO})
    hasta(o, "PROPUESTA", n=3, ahora=AHORA)
    inf3 = vetado(o, "EXP-0003", 3)
    p3 = o.pantalla_aprobacion("EXP-0003", inf3, AHORA, anular_veto={"motivo": MOTIVO})
    h.chk("dos_pantallas_con_el_cupo_libre", p1["ok"] and p3["ok"], (p1, p3))
    r1 = o.autorizar("EXP-0001", "OPERADOR", inf1, T_ESPERA, aprobacion(p1["pantalla"]))
    err = o._comprobar_anulacion(aplanar_informe(inf3), {"motivo": MOTIVO}, _dt(T_ESPERA))[2]   # lo que autorizar vuelve a comprobar
    h.chk("el_cupo_se_recomprueba_al_autorizar", r1["ok"] and err["codigo"] == "O-34" and "mensual" in err["motivo"], (r1, err))

    # ================================================================ §6.3 límite de pérdida del día
    o = nuevo()
    h.chk("registro_de_limites_inicial", o.limites["entradas"][0]["tipo"] == "INICIO" and o.integridad() == [] and "LIM" in o.cabezas())
    for nombre, args, cod in (("actor_no_operador", (1.5, "GESTOR_TACTICA", MOTIVO, AHORA), "O-05"),
                              ("motivo_corto", (1.5, "OPERADOR", "bajar", AHORA), "O-15"),
                              ("cero", (0, "OPERADOR", MOTIVO, AHORA), "O-01"), ("negativo", (-1, "OPERADOR", MOTIVO, AHORA), "O-01"),
                              ("mas_de_100", (101, "OPERADOR", MOTIVO, AHORA), "O-01"), ("texto", ("1.5", "OPERADOR", MOTIVO, AHORA), "O-01"),
                              ("nan", (float("nan"), "OPERADOR", MOTIVO, AHORA), "O-01"), ("bool", (True, "OPERADOR", MOTIVO, AHORA), "O-01"),
                              ("el_mismo", (2.0, "OPERADOR", MOTIVO, AHORA), "O-02")):
        antes = (copy.deepcopy(o.cfg), copy.deepcopy(o.limites), o.huella_config)
        r = o.ajustar_limite_perdida(*args)
        h.chk(f"ajuste_{nombre}_{cod}", r["codigo"] == cod and (o.cfg, o.limites, o.huella_config) == antes, r)
    hasta(o, "PROPUESTA")
    inf_viejo = informe_f(o)
    huella0 = o.huella_config
    r = o.ajustar_limite_perdida(1.5, "OPERADOR", "Bajo el límite tras una semana de volatilidad alta", AHORA)
    h.chk("bajar_vale_sin_segundo_factor", r["ok"] and o.cfg["politica_f"]["perdida_dia_max_pct"] == 1.5 and o.huella_config != huella0
          and o.integridad() == [] and o.limites["entradas"][-1]["tipo"] == "CAMBIO", r)
    h.chk("cambio_avisa_O35", any(a["codigo"] == "O-35" for a in o.avisos))
    r = o.pantalla_aprobacion("EXP-0001", inf_viejo, AHORA)
    h.chk("informe_con_la_politica_vieja_ya_no_vale", r["codigo"] == "O-01" and "CF-07" in r["motivo"], r)
    h.chk("y_uno_nuevo_si", autorizar_op(o, "EXP-0001", informe_f(o, n=2), AHORA)["ok"])
    M2 = "Vuelvo al límite anterior tras revisar la cartera"
    r = o.ajustar_limite_perdida(2.0, "OPERADOR", M2, AHORA)
    h.chk("subir_exige_canal_y_segundo_factor_O05", r["codigo"] == "O-05", r)
    r = o.ajustar_limite_perdida(2.0, "OPERADOR", M2, AHORA, {"canal": "CHAT", "segundo_factor": True})
    h.chk("subir_desde_el_chat_O05", r["codigo"] == "O-05", r)
    r = o.ajustar_limite_perdida(2.5, "OPERADOR", M2, AHORA, OK2F)
    h.chk("R_M4_no_sube_por_encima_del_inicial_O35", r["codigo"] == "O-35" and "J" in r["motivo"], r)
    r = o.ajustar_limite_perdida(2.0, "OPERADOR", M2, AHORA, OK2F)
    h.chk("R_M4_subir_primero_se_solicita", r["ok"] and r["codigo"] == "O-28" and r["aplicado"] is False
          and o.cfg["politica_f"]["perdida_dia_max_pct"] == 1.5 and o.limites["entradas"][-1]["tipo"] == "SOLICITUD" and o.integridad() == [], r)
    r = o.ajustar_limite_perdida(2.0, "OPERADOR", M2, "2026-11-06T09:20:00+00:00", OK2F)
    h.chk("R_M4_confirmar_antes_del_enfriamiento_O28", r["ok"] is False and r["codigo"] == "O-28", r)
    r = o.ajustar_limite_perdida(2.0, "OPERADOR", M2, T_ESPERA, OK2F)
    h.chk("R_M4_confirmar_pasado_el_enfriamiento", r["ok"] and r["aplicado"] and o.cfg["politica_f"]["perdida_dia_max_pct"] == 2.0
          and o.integridad() == [] and o.version_politica() == "POL-2", r)
    o = nuevo()
    registrar_foto(o, CART)
    assert o.ajustar_limite_perdida(1.0, "OPERADOR", "Bajo el límite durante la semana de resultados", AHORA)["ok"]
    assert o.ajustar_limite_perdida(2.0, "OPERADOR", M2, AHORA, OK2F)["codigo"] == "O-28"
    r = o.ajustar_limite_perdida(2.0, "OPERADOR", "Otro motivo distinto del solicitado", T_ESPERA, OK2F)
    h.chk("R_M4_otro_motivo_es_otra_solicitud", r["codigo"] == "O-28" and r["aplicado"] is False and o.cfg["politica_f"]["perdida_dia_max_pct"] == 1.0, r)
    r = o.ajustar_limite_perdida(2.0, "OPERADOR", M2, "2026-11-06T09:31:00+00:00", OK2F)
    h.chk("R_M4_la_solicitud_anterior_se_sustituyo", r["codigo"] == "O-28" and r["aplicado"] is False, r)
    o = nuevo()
    h.chk("R_M4_sin_foto_reciente_no_sube_O35", o.ajustar_limite_perdida(1.0, "OPERADOR", MOTIVO, AHORA)["ok"]
          and o.ajustar_limite_perdida(2.0, "OPERADOR", M2, AHORA, OK2F)["codigo"] == "O-35")

    # alcanzado: no se sube en 24 horas (cubre el mismo día en cualquier zona horaria)
    o = nuevo()
    registrar_foto(o, {**CART, "perdida_dia_eur": 2000.0})   # 2 % de 100.000: el límite justo
    h.chk("alcance_anotado", [x["tipo"] for x in o.limites["entradas"]] == ["INICIO", "ALCANZADO"] and o.limites["entradas"][-1]["dia"] == "2026-11-06"
          and any(a["codigo"] == "O-35" for a in o.avisos) and o.integridad() == [])
    registrar_foto(o, {**CART, "fecha_hora": "2026-11-06T09:10:00+00:00", "perdida_dia_eur": 2600.0})
    h.chk("alcance_una_vez_por_dia", [x["tipo"] for x in o.limites["entradas"]].count("ALCANZADO") == 1)
    h.chk("bajar_el_dia_alcanzado_si", o.ajustar_limite_perdida(1.0, "OPERADOR", "Reduzco el límite después de la pérdida", T_TARDE)["ok"])
    registrar_foto(o, {**CART, "fecha_hora": "2026-11-06T11:58:00+00:00", "perdida_dia_eur": 500.0})
    r = o.ajustar_limite_perdida(2.0, "OPERADOR", "Quiero seguir operando hoy con más margen", "2026-11-06T12:01:00+00:00", OK2F)
    h.chk("subir_el_dia_alcanzado_O35", r["codigo"] == "O-35" and o.cfg["politica_f"]["perdida_dia_max_pct"] == 1.0, r)
    registrar_foto(o, {**CART, "fecha_hora": "2026-11-07T12:25:00+00:00", "perdida_dia_eur": 0.0})
    M3 = "Recupero el límite del día anterior"
    r1 = o.ajustar_limite_perdida(2.0, "OPERADOR", M3, "2026-11-07T12:30:00+00:00", OK2F)
    r2 = o.ajustar_limite_perdida(2.0, "OPERADOR", M3, "2026-11-07T13:01:00+00:00", OK2F)
    h.chk("subir_pasadas_24_horas", r1["codigo"] == "O-28" and r2["ok"] and r2["aplicado"] and o.integridad() == [], (r1, r2))
    # R-M1: bajar por debajo de la pérdida es alcanzarlo, aunque una foto posterior muestre menos pérdida
    o = nuevo()
    registrar_foto(o, {**CART, "perdida_dia_eur": 1600.0})   # 1,6 %: no alcanza el 2 %
    assert o.ajustar_limite_perdida(1.5, "OPERADOR", "Bajo el límite por prudencia esta mañana", AHORA)["ok"]
    h.chk("R_M1_bajar_bajo_la_perdida_anota_alcance", o.limites["entradas"][-1]["tipo"] == "ALCANZADO" and o.limites["entradas"][-1]["limite_pct"] == 1.5)
    registrar_foto(o, {**CART, "fecha_hora": "2026-11-06T11:55:00+00:00", "perdida_dia_eur": 1400.0})
    r = o.ajustar_limite_perdida(2.0, "OPERADOR", "Lo vuelvo a subir para seguir operando", T_TARDE, OK2F)
    h.chk("R_M1_bajar_y_subir_con_la_perdida_encima_O35", r["codigo"] == "O-35", r)
    # R-M2: una foto tomada con el límite bajo y registrada tras subirlo se juzga con el más bajo que rigió
    o = nuevo()
    assert o.ajustar_limite_perdida(1.5, "OPERADOR", "Bajo el límite por prudencia esta mañana", AHORA)["ok"]
    registrar_foto(o, {**CART, "fecha_hora": "2026-11-06T09:05:00+00:00", "perdida_dia_eur": 1000.0})
    assert o.ajustar_limite_perdida(2.0, "OPERADOR", M2, "2026-11-06T09:06:00+00:00", OK2F)["codigo"] == "O-28"
    assert o.ajustar_limite_perdida(2.0, "OPERADOR", M2, "2026-11-06T09:40:00+00:00", OK2F)["aplicado"]
    o.registrar_cartera({**CART, "fecha_hora": "2026-11-06T09:39:00+00:00", "perdida_dia_eur": 1600.0}, "G", "2026-11-06T09:41:00+00:00",
                        cuenta=o.cfg["cuenta_intermediario"])
    h.chk("R_M2_foto_tomada_con_el_limite_bajo", o.limites["entradas"][-1]["tipo"] == "ALCANZADO" and o.limites["entradas"][-1]["limite_pct"] == 1.5,
          o.limites["entradas"][-1])
    # R-m1: el día de la foto en otra zona horaria no abre un hueco: son 24 horas
    o = nuevo()
    o.registrar_cartera({**CART, "fecha_hora": "2026-11-07T00:30:00+01:00", "perdida_dia_eur": 2500.0}, "G", "2026-11-06T23:35:00+00:00",
                        cuenta=o.cfg["cuenta_intermediario"])
    assert o.ajustar_limite_perdida(1.0, "OPERADOR", "Bajo el límite tras la pérdida de anoche", "2026-11-06T23:40:00+00:00")["ok"]
    o.registrar_cartera({**CART, "fecha_hora": "2026-11-07T01:05:00+01:00", "perdida_dia_eur": 0.0}, "G", "2026-11-07T00:08:00+00:00",
                        cuenta=o.cfg["cuenta_intermediario"])
    r = o.ajustar_limite_perdida(2.0, "OPERADOR", M2, "2026-11-07T01:10:00+01:00", OK2F)
    h.chk("R_m1_otra_zona_horaria_O35", r["codigo"] == "O-35", r)
    # kill-switch
    o = nuevo()
    o.activar_kill_switch("prueba de kill-switch", "OPERADOR", AHORA)
    h.chk("kill_switch_no_deja_subir_O26", o.ajustar_limite_perdida(3.0, "OPERADOR", MOTIVO, AHORA, OK2F)["codigo"] == "O-26")
    h.chk("kill_switch_deja_bajar", o.ajustar_limite_perdida(1.0, "OPERADOR", MOTIVO, AHORA)["ok"])

    # R-M3: bajar el límite deja sin valor lo autorizado antes (G no envía la entrada)
    o = nuevo(); hasta(o, "PROPUESTA")
    assert autorizar_op(o, "EXP-0001", informe_f(o), AHORA)["ok"]
    assert o.ajustar_limite_perdida(1.5, "OPERADOR", "Bajo el límite antes de que entre la orden", "2026-11-06T09:02:00+00:00")["ok"]
    b = broker()
    r = ejecutar(o, "EXP-0001", b, "2026-11-06T09:03:00+00:00")
    h.chk("R_M3_autorizacion_anterior_a_bajar_no_se_envia", r["codigo"] == "G-06" and b.ordenes == {}, r)
    h.chk("R_M3_ni_se_anota_la_entrada", o.orden_entrada("EXP-0001", "ORD-X-1", "ENVIADA", 0.0, "G", "2026-11-06T09:03:00+00:00")["codigo"] == "O-05")

    # R-G1: una anulación autorizada se ejecuta (G y el Orquestador aceptan que F vuelva a vetar solo por lo anulado)
    o = nuevo(); hasta(o, "PROPUESTA")
    inf = vetado(o)
    assert anular(o, inf)["ok"]
    b = broker()
    r = ejecutar(o, "EXP-0001", b, T_ESPERA)
    h.chk("R_G1_la_anulacion_se_ejecuta", r["ok"] and o.posiciones["POS-EXP-0001"]["cantidad"] == 100.0 and o.integridad() == [], r)
    h.chk("R_G1_sin_deshacer_en_el_intermediario", all(x["orden"]["tipo"] != "MERCADO" for x in b.ordenes.values()))

    # integridad del límite: cambiarlo por fuera se detecta, aunque se recalcule la huella
    o = nuevo()
    o.cfg["politica_f"]["perdida_dia_max_pct"] = 5.0
    h.chk("cambio_por_fuera_CONFIG", "CONFIG" in o.integridad())
    o.huella_config = o._huella_actual() if hasattr(o, "_huella_actual") else __import__("orquestador")._hash(
        __import__("orquestador")._canon(o._configuracion_completa()))
    h.chk("cambio_por_fuera_con_huella_recalculada_CONFIG", "CONFIG" in o.integridad())
    h.chk("y_no_se_ajusta_O13", o.ajustar_limite_perdida(1.0, "OPERADOR", MOTIVO, AHORA)["codigo"] == "O-13")
    o = nuevo()
    registrar_foto(o, {**CART, "perdida_dia_eur": 2000.0})
    o.limites["entradas"][-1]["dia"] = "2026-11-05"   # disimular el alcance de hoy
    h.chk("alterar_el_registro_de_limites_CONFIG", "CONFIG" in o.integridad())
    o = nuevo()
    del o.limites["entradas"][-1]
    h.chk("borrar_del_registro_CONFIG", "CONFIG" in o.integridad())
    o = nuevo()
    o.limites.pop("entradas")
    try:
        h.chk("R_m4_registro_mal_formado_es_CONFIG_sin_excepcion", "CONFIG" in o.integridad())
    except Exception as ex:   # noqa: BLE001
        h.chk("R_m4_registro_mal_formado_es_CONFIG_sin_excepcion", False, type(ex).__name__)
    c = nuevo().configuracion()
    h.chk("R_m3_constantes_en_la_huella", c["constantes"]["vetos_anulables"] == ["F-09", "F-11"] and c["constantes"]["limite_perdida"] == "perdida_dia_max_pct")

    # ================================================================ configuración
    for nombre, v in (("negativo", -1), ("mas_de_10", 11), ("decimal", 1.5), ("bool", True), ("texto", "2")):
        try:
            Orquestador({**CFG, "anulaciones_veto_mes": v}, CAL)
            h.chk(f"config_anulaciones_{nombre}_se_rechaza", False)
        except ValueError:
            h.chk(f"config_anulaciones_{nombre}_se_rechaza", True)
    c = nuevo().configuracion()
    h.chk("config_040", c["version_config"] == "CFG-0.4.0" and c["orquestador"]["anulaciones_veto_mes"] == 2)

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO OPERADOR T-50:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
