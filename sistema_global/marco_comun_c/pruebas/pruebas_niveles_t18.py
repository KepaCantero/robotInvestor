"""Pruebas de T-18 (V0.50): nivel L3 solo en horario supervisado y umbral de tamaño de la matriz de autonomía en L2 (§6).
Datos SIMULADOS.

Uso: python3 pruebas/pruebas_niveles_t18.py
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import migraciones as mg  # noqa: E402
import persistencia as pe  # noqa: E402
from control_f import NIVELES as NIVELES_F  # noqa: E402
from ejecucion_g import ejecutar  # noqa: E402
from orquestador import CONFIG_DEFECTO, NIVELES, Orquestador  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_ejecucion_g import autorizado  # noqa: E402
from pruebas_orquestador import AHORA, CAL, CFG, Arnes, autorizar_op, hasta, nuevo  # noqa: E402
from vigilancia import vigilar  # noqa: E402

T_FUERA = "2026-11-06T09:01:00+00:00"
M = "Paso el estado guardado al código de V0.50"


def cfg(nivel="L2", umbral=None, horario=None, matriz=True):
    c = {"nivel_autonomia": {"TACTICA": nivel}, "matriz_autonomia": {"TACTICA": matriz}}
    if umbral is not None:
        c["umbral_l2_eur"] = {"TRADING": 5000.0, "TACTICA": umbral, "LARGO_PLAZO": 5000.0}
    if horario is not None:
        c["aprobacion"] = {**CONFIG_DEFECTO["aprobacion"], "horario_utc": horario}
    return c


def propuesta(**kw):
    o = nuevo(cfg(**kw))
    hasta(o, "PROPUESTA")
    return o


def importe(o):
    e = o.expedientes["EXP-0001"]
    return o._importe_eur(e, e["propuesta"]["entrada"]["cantidad"], {"solicitud": {"divisa_cotizacion": "USD"}, "cartera": o.cartera_f()})


def dt(s):
    return datetime.fromisoformat(s).astimezone(timezone.utc)


def main():
    h = Arnes()
    # ------------------------------------------------------------------------------------------- configuración
    h.chk("L3_existe_y_F_lo_acepta", NIVELES["L3"] == 3 and "L3" in NIVELES_F)
    h.chk("version_CFG_0100_y_umbral_por_defecto", CONFIG_DEFECTO["version_config"] == "CFG-0.10.0"
          and CONFIG_DEFECTO["umbral_l2_eur"] == {"TRADING": 5000.0, "TACTICA": 5000.0, "LARGO_PLAZO": 5000.0})
    for nombre, u in (("falta_cartera", {"TRADING": 1.0, "TACTICA": 1.0}), ("cartera_de_mas", {"TRADING": 1.0, "TACTICA": 1.0, "LARGO_PLAZO": 1.0, "X": 1.0}),
                      ("negativo", {"TRADING": -1.0, "TACTICA": 1.0, "LARGO_PLAZO": 1.0}), ("nan", {"TRADING": float("nan"), "TACTICA": 1.0, "LARGO_PLAZO": 1.0}),
                      ("texto", {"TRADING": "1", "TACTICA": 1.0, "LARGO_PLAZO": 1.0}), ("no_dict", 5.0)):
        try:
            Orquestador({**CFG, "umbral_l2_eur": u}, CAL)
            h.chk(f"umbral_{nombre}_se_rechaza", False)
        except ValueError:
            h.chk(f"umbral_{nombre}_se_rechaza", True)
    h.chk("nivel_L3_en_la_configuracion_se_acepta", nuevo(cfg("L3")).nivel("TACTICA") == "L3")
    # ------------------------------------------------------------------------------------------- nivel efectivo
    o = nuevo(cfg("L3", horario=["07:00", "21:00"]))
    h.chk("L3_dentro_del_horario", o.nivel_en("TACTICA", dt("2026-11-06T10:00:00+00:00")) == "L3")
    h.chk("L3_fuera_del_horario_es_L2", o.nivel_en("TACTICA", dt("2026-11-06T22:00:00+00:00")) == "L2")
    o = nuevo(cfg("L3", horario=["22:00", "06:00"]))
    h.chk("horario_que_cruza_la_medianoche", o.nivel_en("TACTICA", dt("2026-11-06T23:30:00+00:00")) == "L3"
          and o.nivel_en("TACTICA", dt("2026-11-06T12:00:00+00:00")) == "L2")
    o = nuevo(cfg("L2"))
    h.chk("L2_no_cambia_con_el_horario", o.nivel_en("TACTICA", dt("2026-11-06T23:00:00+00:00")) == "L2")
    o = nuevo(cfg("L3"))
    o.degradar("TACTICA", "dato viejo en la prueba", "G", AHORA)
    h.chk("L3_degradada_es_L1", o.nivel("TACTICA") == "L1" and o.nivel_en("TACTICA", dt(AHORA)) == "L1")

    # ------------------------------------------------------------------------------------------- matriz y umbral
    o = propuesta()
    imp = importe(o)
    h.chk("el_importe_de_la_propuesta_se_valora", imp is not None and imp > 0, imp)
    o = propuesta(umbral=imp * 2)
    h.chk("L2_por_debajo_del_umbral_autoriza_la_matriz", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["ok"])
    o = propuesta(umbral=round(imp, 2) + 0.01)
    h.chk("L2_en_el_umbral_autoriza", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["ok"])
    o = propuesta(umbral=imp / 2)
    r = o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)
    h.chk("L2_por_encima_del_umbral_O05_y_no_cambia_nada", r["codigo"] == "O-05" and "umbral" in r["motivo"]
          and o.expedientes["EXP-0001"]["estado"] == "PROPUESTA" and "EV-F-0001" not in o.eventos, r)
    h.chk("y_el_operador_si_puede", autorizar_op(o, "EXP-0001", informe_f(o, n=2), AHORA)["ok"])
    o = propuesta(umbral=0.0)
    h.chk("umbral_cero_nada_automatico_en_L2", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["codigo"] == "O-05")
    o = propuesta(nivel="L3", umbral=imp / 2)
    h.chk("L3_en_horario_autoriza_por_encima_del_umbral", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["ok"])
    o = propuesta(nivel="L3", umbral=imp / 2, horario=["10:00", "20:00"])
    r = o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)
    h.chk("L3_fuera_de_horario_por_encima_O05", r["codigo"] == "O-05" and "fuera del horario" in r["motivo"], r)
    o = propuesta(nivel="L3", umbral=imp * 2, horario=["10:00", "20:00"])
    h.chk("L3_fuera_de_horario_por_debajo_autoriza_como_L2", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["ok"])
    o = propuesta(nivel="L3", umbral=imp / 2, matriz=False)
    h.chk("L3_sin_la_matriz_activada_no_autoriza", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["codigo"] == "O-05")
    o = propuesta(nivel="L1", umbral=imp * 2)
    h.chk("L1_sigue_sin_matriz", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["codigo"] == "O-05")
    o = propuesta(nivel="L3", umbral=imp / 2)
    o.degradar("TACTICA", "intermediario caído en la prueba", "G", AHORA)
    h.chk("L3_degradada_no_autoriza", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["codigo"] == "O-05")
    o = propuesta(umbral=imp * 2)
    e = o.expedientes["EXP-0001"]
    h.chk("sin_poder_valorar_en_euros_O05", o._matriz_permite(e, 10.0, {"solicitud": {"divisa_cotizacion": "XXX"}, "cartera": {}}, dt(AHORA))["codigo"] == "O-05")

    # ------------------------------------------------------------------------------------------- al enviar la orden de entrada
    o = propuesta(nivel="L3", umbral=imp / 2, horario=["08:00", "09:01"])
    h.chk("L3_autoriza_a_las_9_en_horario", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["ok"])
    r = o.orden_entrada("EXP-0001", "ORD-T18-1", "ENVIADA", 0.0, "G", T_FUERA)
    h.chk("enviar_fuera_de_horario_por_encima_O05", r["codigo"] == "O-05" and "al enviar" in r["motivo"]
          and o.expedientes["EXP-0001"].get("orden_entrada") is None, r)
    o = propuesta(nivel="L3", umbral=imp * 2, horario=["08:00", "09:01"])
    o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)
    h.chk("enviar_fuera_de_horario_por_debajo_vale", o.orden_entrada("EXP-0001", "ORD-T18-2", "ENVIADA", 0.0, "G", T_FUERA)["ok"])
    o = propuesta(umbral=imp / 2)
    autorizar_op(o, "EXP-0001", informe_f(o), AHORA)
    h.chk("lo_que_autoriza_el_operador_no_mira_el_umbral_al_enviar", o.orden_entrada("EXP-0001", "ORD-T18-3", "ENVIADA", 0.0, "G", T_FUERA)["ok"])
    o, b = autorizado(o=nuevo(cfg("L3", umbral=imp * 2)))
    h.chk("G_ejecuta_en_L3", ejecutar(o, "EXP-0001", b, AHORA)["ok"])

    # ------------------------------------------------------------------------------------------- revisión de V0.50
    from ejecucion_g import cartera_para_f
    from pruebas_ejecucion_g import broker
    # r01: una entrada de L3 por encima del umbral enviada en horario y aún viva se cancela fuera de horario y no abre posición
    o = nuevo(cfg("L3", umbral=imp / 2, horario=["08:00", "09:05"]))
    hasta(o, "PROPUESTA")
    b = broker(precio=1.102)   # por encima del límite de compra: la orden queda viva
    o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o, cartera=cartera_para_f(b)), AHORA)
    ejecutar(o, "EXP-0001", b, "2026-11-06T09:02:00+00:00")
    e = o.expedientes["EXP-0001"]
    h.chk("r01_vigente_en_horario_y_no_fuera", o.autorizacion_vigente(e, dt("2026-11-06T09:03:00+00:00"))
          and not o.autorizacion_vigente(e, dt("2026-11-06T22:00:00+00:00")))
    T22 = "2026-11-06T22:00:00+00:00"
    b.mover_precio("EURUSD", 1.099, T22)
    vigilar(o, b, {"EURUSD": {"precio": 1.099, "hora": T22}}, T22)
    h.chk("r01_fuera_de_horario_la_orden_viva_se_cancela_y_no_abre", "POS-EXP-0001" not in o.posiciones
          or o.posiciones["POS-EXP-0001"]["estado"] != "ABIERTA", o.posiciones.get("POS-EXP-0001", {}).get("estado"))
    # r02: una degradación posterior anula la autorización automática aunque luego se restablezca
    o = propuesta(nivel="L3", umbral=imp / 2)
    o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)
    o.degradar("TACTICA", "dato viejo en la prueba r02", "H", "2026-11-06T09:00:30+00:00")
    for x in o.avisos:
        if x["acuse"] is None:
            o.acusar_aviso(x["id"], "OPERADOR", "2026-11-06T09:00:40+00:00")
    rr = o.restablecer_nivel("TACTICA", "OPERADOR", "2026-11-06T09:00:50+00:00")
    h.chk("r02_restablecer_no_revive_la_autorizacion", rr["ok"] and not o.autorizacion_vigente(o.expedientes["EXP-0001"])
          and o.orden_entrada("EXP-0001", "ORD-R02", "ENVIADA", 0.0, "G", "2026-11-06T09:01:00+00:00")["codigo"] == "O-05", rr)
    # r03: MIG-002 declara la clave que escribe
    h.chk("r03_MIG002_declara_umbral_l2_eur", [m for m in mg.MIGRACIONES if m.id == "MIG-002"][0].cambia == frozenset({"cfg.umbral_l2_eur"}))
    # r04: el último minuto del horario ya no cuenta (horario [desde, hasta))
    o = nuevo(cfg("L3", horario=["07:00", "09:00"]))
    h.chk("r04_horario_semiabierto_al_segundo", o.nivel_en("TACTICA", dt("2026-11-06T08:59:59+00:00")) == "L3"
          and o.nivel_en("TACTICA", dt("2026-11-06T09:00:00+00:00")) == "L2" and o.nivel_en("TACTICA", dt("2026-11-06T07:00:00+00:00")) == "L3")
    # r05: pruebas que sí detectan errores plausibles: tipo de cambio distinto de 1, cantidad reducida por F, importe exacto, contexto
    o = propuesta(umbral=10 ** 6)
    e = o.expedientes["EXP-0001"]
    ent = {"solicitud": {"divisa_cotizacion": "USD"}, "cartera": {**o.cartera_f(), "tipos_cambio_eur": {"USD": 0.9}}}
    v = o._importe_eur(e, 100.0, ent)
    h.chk("r05_el_tipo_de_cambio_se_aplica_bien", v is not None and abs(v - 100.0 * e["propuesta"]["entrada"]["limite"] * 0.9) < 1e-9, v)
    exacto = o._importe_eur(e, e["propuesta"]["entrada"]["cantidad"], {"solicitud": {"divisa_cotizacion": "USD"}, "cartera": o.cartera_f()})
    o = propuesta(umbral=exacto)
    h.chk("r05_importe_exactamente_igual_al_umbral_autoriza", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["ok"])
    from control_f import POLITICA_DEFECTO
    # otro expediente ya autorizado hoy deja poco hueco en el límite del día: F reduce (F-14) y la matriz valora lo aprobado
    pol = {**POLITICA_DEFECTO, "importe_max_orden_eur": 1.5 * exacto, "importe_max_dia_eur": 1.5 * exacto, "valor_min_eur": 10.0}
    o = nuevo({**cfg(umbral=exacto * 0.6), "politica_f": pol})
    hasta(o, "AUTORIZADA")
    hasta(o, "PROPUESTA", n=3)
    r = o.autorizar("EXP-0003", "MATRIZ_AUTONOMIA", informe_f(o, "EXP-0003", n=5), AHORA)
    h.chk("r05_con_F_reduciendo_se_valora_la_cantidad_aprobada", r["ok"] and o.expedientes["EXP-0003"]["control_f"]["resultado"] == "REDUCIDO", r)
    o = propuesta(nivel="L3")
    h.chk("r05_F_recibe_L3_en_el_contexto", o.contexto_f("EXP-0001", AHORA)["autonomia"]["nivel"] == "L3")
    # r06: mensajes al día
    o = propuesta(nivel="L3", umbral=imp / 2)
    o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)
    o.degradar("TACTICA", "dato viejo en la prueba r06", "H", "2026-11-06T09:00:30+00:00")
    r = o.orden_entrada("EXP-0001", "ORD-R06", "ENVIADA", 0.0, "G", "2026-11-06T09:01:00+00:00")
    h.chk("r06_el_mensaje_ya_no_habla_solo_de_L2", r["codigo"] == "O-05" and "degradada después" in r["motivo"], r)

    # ------------------------------------------------------------------------------------------- H y G en L3
    o, b = autorizado(o=nuevo(cfg("L3")))
    ejecutar(o, "EXP-0001", b, AHORA)
    pid = "POS-EXP-0001"
    st = [c for c in o.posiciones[pid]["condiciones_salida"]["condiciones"] if c["tipo"] == "OBJETIVO" and c.get("fraccion") is None][0]
    precio = st["umbral"] + 0.01
    b.mover_precio("EURUSD", precio, "2026-11-06T09:05:00+00:00")
    r = vigilar(o, b, {"EURUSD": {"precio": precio, "hora": "2026-11-06T09:05:00+00:00"}}, "2026-11-06T09:05:00+00:00")
    h.chk("H_cierra_solo_en_L3_como_en_L2", any(a["regla"] == "H-02" for a in r["acciones"]) and o.posiciones[pid]["estado"] == "CERRADA", r["acciones"])
    h.chk("F_recibe_L3_en_el_contexto", nuevo(cfg("L3")).cfg["nivel_autonomia"]["TACTICA"] == "L3")

    # ------------------------------------------------------------------------------------------- migración de un estado de V0.45
    viejo = (AQUI / "estados" / "estado_V0_45.json").read_text(encoding="ascii")
    d = json.loads(viejo)
    h.chk("el_estado_de_V0_45_es_genuino", d["esquema"] == mg.ESQUEMA_V0_45 and "umbral_l2_eur" not in d["estado"]["cfg"]
          and d["estado"]["cfg"]["version_config"] == "CFG-0.7.0")
    h.chk("con_este_codigo_no_se_carga_PE08", pe.cargar(viejo)["codigo"] == "PE-08")
    r = mg.migrar(viejo, "2026-11-07T10:00:00+00:00", M)
    o2 = r.get("orquestador")
    h.chk("MIG002_y_MIG003_lo_migran", r["ok"] and r["migraciones"] == ["MIG-002", "MIG-003"] and o2.cfg["umbral_l2_eur"] == CONFIG_DEFECTO["umbral_l2_eur"]
          and o2.cfg["promocion_nivel"] == CONFIG_DEFECTO["promocion_nivel"]
          and o2.cfg["version_config"] == "CFG-0.10.0" and o2.integridad() == [], r.get("motivo"))
    h.chk("la_huella_de_configuracion_cambia_y_queda_anotada", o2.limites["entradas"][-1]["huella_antes"] != o2.huella_config)
    h.chk("y_la_autorizacion_anterior_deja_de_valer", not o2.autorizacion_vigente(o2.expedientes["EXP-0001"]))
    h.chk("el_nivel_de_cada_cartera_no_cambia", o2.cfg["nivel_autonomia"] == d["estado"]["cfg"]["nivel_autonomia"])
    h.chk("y_se_vuelve_a_cargar", pe.cargar(r["texto"])["ok"])

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO NIVELES T-18:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
