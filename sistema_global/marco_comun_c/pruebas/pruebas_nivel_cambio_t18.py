"""Pruebas de T-18 (V0.51): el operador cambia el nivel de autonomía de una cartera sin reiniciar (§6). Bajar es inmediato;
subir es de un nivel en uno, en dos pasos con enfriamiento, con canal admitido y segundo factor, sin kill-switch y tras un
periodo mínimo sin incidentes en el nivel actual (criterios de promoción, O-39). Datos SIMULADOS.

Uso: python3 pruebas/pruebas_nivel_cambio_t18.py
"""
import copy
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import migraciones as mg  # noqa: E402
import persistencia as pe  # noqa: E402
from orquestador import CONFIG_DEFECTO, INCIDENTES_PROMOCION, PRIORIDAD_AVISO  # noqa: E402
from pruebas_control_f import CART, informe_f, registrar_foto  # noqa: E402
from ejecucion_g import conciliar  # noqa: E402
from pruebas_ejecucion_g import broker  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, hasta, nuevo  # noqa: E402

AP = {"canal": "CONSOLA", "segundo_factor": True}
MS = "Tres meses sin incidentes en L1: subo la táctica a L2"
MB = "Mercado nervioso esta semana: bajo la táctica a L1"
LISTA = {k: True for k in ("causa_corregida", "conciliacion_limpia", "datos_frescos", "protecciones_verificadas")}


def t(dias=0, minutos=0):
    return (datetime.fromisoformat(AHORA) + timedelta(days=dias, minutes=minutos)).astimezone(timezone.utc).isoformat()


def cfg(tactica="L1", trading="L1", **extra):
    return {"nivel_autonomia": {"TRADING": trading, "TACTICA": tactica, "LARGO_PLAZO": "L1"}, **extra}


def huella(o):
    return (copy.deepcopy(o.cfg), o.huella_config, len(o.limites["entradas"]), len(o.avisos))


def datos(o, ahora):
    """Lo que G haría a diario: una foto de cartera fresca y una conciliación limpia en ese instante."""
    registrar_foto(o, {**CART, "fecha_hora": ahora})
    conciliar(o, broker(), ahora)


def cn(o, *args):
    """cambiar_nivel; para una subida (con aprobación), antes deja datos frescos como los dejaría G."""
    if len(args) == 6:
        datos(o, args[4])
    return o.cambiar_nivel(*args)


def subir(o, nivel="L2", dia=31, cartera="TACTICA", motivo=MS, ap=AP):
    """Solicita y confirma la subida (los dos pasos); devuelve (primera, segunda)."""
    r1 = cn(o, cartera, nivel, "OPERADOR", motivo, t(dia), ap)
    r2 = cn(o, cartera, nivel, "OPERADOR", motivo, t(dia, 30), ap)
    return r1, r2


def main():
    h = Arnes()
    # ------------------------------------------------------------------------------------------- configuración
    h.chk("config_CFG_0100_y_promocion_por_defecto", CONFIG_DEFECTO["version_config"] == "CFG-0.10.0"
          and CONFIG_DEFECTO["promocion_nivel"] == {"periodo_min_dias": 30})
    h.chk("O39_es_ALTA_e_incidentes_declarados", PRIORIDAD_AVISO["O-39"] == "ALTA" and INCIDENTES_PROMOCION == ("O-03", "O-18", "O-25"))
    for nombre, v in (("negativo", {"periodo_min_dias": -1}), ("mas_de_un_anio", {"periodo_min_dias": 366}), ("texto", {"periodo_min_dias": "30"}),
                      ("bool", {"periodo_min_dias": True}), ("nan", {"periodo_min_dias": float("nan")}), ("clave_de_mas", {"periodo_min_dias": 30, "x": 1}),
                      ("vacio", {}), ("no_dict", 30), ("cero", {"periodo_min_dias": 0})):
        try:
            nuevo(cfg(promocion_nivel=v))
            h.chk(f"promocion_{nombre}_rechazada", False)
        except ValueError:
            h.chk(f"promocion_{nombre}_rechazada", True)
    h.chk("esquema_del_codigo_registrado", pe.esquema_actual() == mg.ESQUEMA_V0_51 and mg.ESQUEMA_V0_51 in mg.ESQUEMAS)

    # ------------------------------------------------------------------------------------------- rechazos sin efecto
    o = nuevo(cfg("L2"))
    antes = huella(o)
    for nombre, args, cod in (("actor_no_operador", ("TACTICA", "L1", "ORQUESTADOR", MB, t(1)), "O-05"),
                              ("cartera_desconocida", ("OTRA", "L1", "OPERADOR", MB, t(1)), "O-01"),
                              ("nivel_desconocido", ("TACTICA", "L9", "OPERADOR", MB, t(1)), "O-01"),
                              ("nivel_con_espacio", ("TACTICA", "L1 ", "OPERADOR", MB, t(1)), "O-01"),
                              ("nivel_lista", ("TACTICA", ["L1"], "OPERADOR", MB, t(1)), "O-01"),
                              ("motivo_corto", ("TACTICA", "L1", "OPERADOR", "bajo", t(1)), "O-15"),
                              ("mismo_nivel", ("TACTICA", "L2", "OPERADOR", MB, t(1)), "O-02")):
        r = cn(o, *args)
        h.chk(f"rechazo_{nombre}_{cod}", not r["ok"] and r["codigo"] == cod, r)
    h.chk("los_rechazos_no_cambian_nada", huella(o) == antes)

    # ------------------------------------------------------------------------------------------- bajar
    o = nuevo(cfg("L3"))
    h0 = o.huella_config
    r = cn(o, "TACTICA", "L1", "OPERADOR", MB, t(1))
    x = o.limites["entradas"][-1]
    h.chk("bajar_es_inmediato_y_puede_saltar_niveles", r["ok"] and r["aplicado"] and o.cfg["nivel_autonomia"]["TACTICA"] == "L1" and o.nivel("TACTICA") == "L1", r)
    h.chk("bajar_anota_NIVEL_con_la_huella_nueva", x["tipo"] == "NIVEL" and x["antes"] == "L3" and x["nivel"] == "L1" and x["cartera"] == "TACTICA"
          and x["huella_config"] == o.huella_config != h0 and x["canal"] is None)
    h.chk("y_la_configuracion_sigue_integra", o.config_integra() and o.integridad() == [])
    av = o.avisos[-1]
    h.chk("bajar_avisa_O39_ALTA_de_la_cartera", av["codigo"] == "O-39" and av["prioridad"] == "ALTA" and av["carteras"] == ["TACTICA"])
    h.chk("la_configuracion_publicada_lleva_el_nivel", o.configuracion()["orquestador"]["nivel_autonomia"]["TACTICA"] == "L1"
          and o.configuracion()["huella"] == o.huella_config)
    h.chk("se_puede_bajar_a_L0", cn(o, "TACTICA", "L0", "OPERADOR", MB, t(2))["ok"] and o.nivel("TACTICA") == "L0")
    o = nuevo(cfg("L2"))
    o.activar_kill_switch("prueba de kill", "OPERADOR", t(1))
    h.chk("bajar_vale_con_kill_switch_y_sin_aprobacion", cn(o, "TACTICA", "L1", "OPERADOR", MB, t(1, 5))["ok"])

    # bajar anula la autorización de la matriz de autonomía (aunque luego se vuelva a subir)
    o = nuevo(cfg("L2", matriz_autonomia={"TACTICA": True}))
    hasta(o, "PROPUESTA")
    h.chk("la_matriz_autoriza_en_L2", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["ok"])
    e = o.expedientes["EXP-0001"]
    h.chk("y_la_autorizacion_vale", o.autorizacion_vigente(e))
    cn(o, "TACTICA", "L1", "OPERADOR", MB, t(0, 5))
    h.chk("bajar_la_anula", not o.autorizacion_vigente(e))
    o.cfg["nivel_autonomia"]["TACTICA"] = "L2"   # aun si el nivel volviera a L2 (aquí, a mano y solo para mirarlo)
    h.chk("y_volver_a_L2_no_la_revive", not o.autorizacion_vigente(e))

    # ------------------------------------------------------------------------------------------- subir: el camino feliz
    o = nuevo(cfg("L1"))
    h0 = o.huella_config
    r1 = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31), AP)
    h.chk("subir_primero_solicita_O28", r1["ok"] and r1["codigo"] == "O-28" and r1["aplicado"] is False and o.nivel("TACTICA") == "L1"
          and o.limites["entradas"][-1]["tipo"] == "SOLICITUD_NIVEL" and o.huella_config == h0 and o.config_integra(), r1)
    r2 = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31, 30), AP)
    h.chk("y_tras_el_enfriamiento_aplica", r2["ok"] and r2["aplicado"] and o.nivel("TACTICA") == "L2" and o.huella_config != h0, r2)
    x = o.limites["entradas"][-1]
    h.chk("subir_anota_NIVEL_con_canal", x["tipo"] == "NIVEL" and x["antes"] == "L1" and x["nivel"] == "L2" and x["canal"] == "CONSOLA"
          and x["huella_config"] == o.huella_config)
    h.chk("subir_avisa_O39", o.avisos[-1]["codigo"] == "O-39" and "subido" in o.avisos[-1]["motivo"])
    h.chk("y_todo_integro", o.config_integra() and o.integridad() == [])
    h.chk("una_tercera_llamada_igual_es_O02", cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31, 31), AP)["codigo"] == "O-02")

    o = nuevo(cfg("L1"))
    cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31), AP)
    antes = huella(o)
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31, 10), AP)
    h.chk("confirmar_en_el_enfriamiento_O28_sin_efecto", not r["ok"] and r["codigo"] == "O-28" and huella(o) == antes, r)
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31, 46), AP)   # 30 de enfriamiento + 15 de caducidad: ya caducó
    h.chk("confirmar_caducado_vuelve_a_solicitar", r["ok"] and r["aplicado"] is False and o.nivel("TACTICA") == "L1", r)
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS + " (otro motivo)", t(31, 80), AP)
    h.chk("confirmar_con_otro_motivo_vuelve_a_solicitar", r["ok"] and r["aplicado"] is False and o.nivel("TACTICA") == "L1", r)
    o = nuevo(cfg("L1"))
    cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31), AP)
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31, 45), AP)   # justo al caducar: aún vale
    h.chk("confirmar_en_el_ultimo_instante_vale", r["ok"] and r["aplicado"], r)
    o = nuevo(cfg("L1", trading="L1"))
    cn(o, "TRADING", "L2", "OPERADOR", MS, t(31), AP)
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31, 30), AP)
    h.chk("la_solicitud_de_otra_cartera_no_sirve", r["ok"] and r["aplicado"] is False and o.nivel("TACTICA") == "L1", r)

    # ------------------------------------------------------------------------------------------- subir: rechazos
    o = nuevo(cfg("L1"))
    antes = huella(o)
    for nombre, args, cod in (("dos_niveles_de_golpe", ("TACTICA", "L3", "OPERADOR", MS, t(31), AP), "O-39"),
                              ("sin_aprobacion", ("TACTICA", "L2", "OPERADOR", MS, t(31)), "O-05"),
                              ("canal_chat", ("TACTICA", "L2", "OPERADOR", MS, t(31), {"canal": "CHAT", "segundo_factor": True}), "O-05"),
                              ("sin_segundo_factor", ("TACTICA", "L2", "OPERADOR", MS, t(31), {"canal": "CONSOLA", "segundo_factor": False}), "O-05"),
                              ("segundo_factor_texto", ("TACTICA", "L2", "OPERADOR", MS, t(31), {"canal": "CONSOLA", "segundo_factor": "sí"}), "O-05"),
                              ("aprobacion_con_clave_de_mas", ("TACTICA", "L2", "OPERADOR", MS, t(31), {**AP, "x": 1}), "O-05")):
        r = cn(o, *args)
        h.chk(f"subir_rechazo_{nombre}_{cod}", not r["ok"] and r["codigo"] == cod, r)
    h.chk("los_rechazos_de_subida_no_cambian_nada", huella(o) == antes)
    o = nuevo(cfg("L1"))
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(29, 23 * 60), AP)
    h.chk("antes_del_periodo_minimo_O39", not r["ok"] and r["codigo"] == "O-39" and "periodo mínimo" in r["motivo"], r)
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(30), AP)
    h.chk("al_cumplir_el_periodo_se_puede_solicitar", r["ok"] and r["codigo"] == "O-28", r)
    o = nuevo(cfg("L1"), sellos=())
    o.ultimo_ahora = None
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(400), AP)
    h.chk("sin_nada_anotado_no_se_promociona", not r["ok"] and r["codigo"] == "O-39", r)

    o = nuevo(cfg("L1"))
    o.activar_kill_switch("prueba de kill", "OPERADOR", t(31))
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31, 1), AP)
    h.chk("subir_con_kill_switch_activo_O26", not r["ok"] and r["codigo"] == "O-26", r)
    for av in list(o.avisos):
        o.acusar_aviso(av["id"], "OPERADOR", t(31, 2))
    conciliar(o, broker(), t(31, 3))
    h.chk("rearmado", o.rearmar_kill_switch(LISTA, "OPERADOR", t(31, 3))["ok"])
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(50), AP)
    h.chk("un_kill_en_el_periodo_impide_subir_O39", not r["ok"] and r["codigo"] == "O-39" and "kill-switch" in r["motivo"], r)
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(62), AP)
    h.chk("r05_un_kill_fuera_de_la_ventana_ya_no_bloquea", r["ok"] and r["codigo"] == "O-28", r)

    # cada criterio de promoción, por separado
    def tras(prep, nombre, ini="L1", nivel="L2", cartera="TACTICA", trading="L1", espera=31):
        o = nuevo(cfg(ini, trading=trading))
        prep(o)
        r = cn(o, cartera, nivel, "OPERADOR", MS, t(espera), AP)
        h.chk(f"criterio_{nombre}_O39", not r["ok"] and r["codigo"] == "O-39" and r.get("criterios"), r)
        return o, r

    tras(lambda o: registrar_foto(o, {**CART, "fecha_hora": t(10), "perdida_dia_eur": 2000.0}), "limite_alcanzado_en_el_periodo")
    tras(lambda o: o.reportar_discrepancia([{"tipo": "POSICION", "ref": "TACTICA", "detalle": "x"}], "G", t(10)), "conciliacion_O18_de_la_cartera")
    tras(lambda o: o.reportar_discrepancia([{"tipo": "POSICION", "ref": "NADA-QUE-SE-SEPA", "detalle": "x"}], "G", t(10)), "conciliacion_sin_atribuir")

    def degrada_y_restablece(o):
        o.degradar("TACTICA", "dato viejo", "G", t(10))
        for av in [a for a in o.avisos if a["acuse"] is None]:
            o.acusar_aviso(av["id"], "OPERADOR", t(10, 1))
        assert o.restablecer_nivel("TACTICA", "OPERADOR", t(10, 2))["ok"]
    tras(degrada_y_restablece, "degradacion_en_el_periodo_aunque_restablecida", ini="L2", nivel="L3")
    tras(lambda o: o.degradar("TACTICA", "dato viejo", "G", t(31)), "cartera_degradada_ahora", ini="L2", nivel="L3", espera=32)

    def toca(o):
        o.expedientes["EXP-0001"]["historial"][0]["motivo"] = "tocado por fuera"
    o = nuevo(cfg("L1"))
    hasta(o, "PROPUESTA")
    toca(o)
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31), AP)
    h.chk("criterio_integridad_O39", not r["ok"] and r["codigo"] == "O-39" and "integridad" in r["motivo"], r)

    # lo de otra cartera no impide subir esta
    o = nuevo(cfg("L1", trading="L2"))
    o.degradar("TRADING", "dato viejo", "G", t(10))
    o.reportar_discrepancia([{"tipo": "POSICION", "ref": "TRADING", "detalle": "x"}], "G", t(10, 1))
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31), AP)
    h.chk("la_degradacion_y_la_discrepancia_de_otra_cartera_no_cuentan", r["ok"] and r["codigo"] == "O-28", r)
    # y lo de antes del periodo tampoco (el periodo empieza en el último cambio de nivel de la cartera)
    o = nuevo(cfg("L2"))
    o.reportar_discrepancia([{"tipo": "POSICION", "ref": "TACTICA", "detalle": "x"}], "G", t(1))
    cn(o, "TACTICA", "L1", "OPERADOR", MB, t(2))
    for av in list(o.avisos):
        o.acusar_aviso(av["id"], "OPERADOR", t(2, 1))
    h.chk("bajar_no_quita_la_degradacion_pero_se_restablece", "TACTICA" in o.degradadas and o.restablecer_nivel("TACTICA", "OPERADOR", t(2, 2))["ok"])
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(20), AP)
    h.chk("tras_bajar_el_periodo_empieza_de_nuevo", not r["ok"] and r["codigo"] == "O-39" and "periodo mínimo" in r["motivo"], r)
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(32), AP)
    h.chk("y_lo_anterior_al_cambio_no_cuenta", r["ok"] and r["codigo"] == "O-28", r)

    # lo que pasa entre la solicitud y la confirmación
    for nombre, entre, cod in (("alcance_del_limite", lambda o: registrar_foto(o, {**CART, "fecha_hora": t(31, 5), "perdida_dia_eur": 2000.0}), "O-39"),
                               ("kill_switch", lambda o: o.activar_kill_switch("prueba", "OPERADOR", t(31, 5)), "O-26"),
                               ("discrepancia", lambda o: o.reportar_discrepancia([{"tipo": "P", "ref": "TACTICA", "detalle": "x"}], "G", t(31, 5)), "O-39")):
        o = nuevo(cfg("L1"))
        cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31), AP)
        entre(o)
        r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31, 30), AP)
        h.chk(f"entre_solicitud_y_confirmacion_{nombre}_{cod}", not r["ok"] and r["codigo"] == cod and o.nivel("TACTICA") == "L1", r)
    o = nuevo(cfg("L1"))
    cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31), AP)
    cn(o, "TACTICA", "L0", "OPERADOR", MB, t(31, 5))
    h.chk("bajar_anula_la_solicitud_pendiente", o._nivel_pendiente("TACTICA") is None
          and cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31, 30), AP)["codigo"] == "O-39")

    # ------------------------------------------------------------------------------------------- regresiones de la revisión de V0.51
    o = nuevo(cfg("L1"))
    o.degradar("TACTICA", "sin precio fresco", "H", t(10))
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31), AP)
    h.chk("r01_una_degradacion_en_L1_impide_subir", not r["ok"] and r["codigo"] == "O-39" and "se degradó" in r["motivo"], r)
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(41), AP)
    h.chk("r01_y_fuera_de_la_ventana_ya_no", r["ok"] and r["codigo"] == "O-28", r)
    o = nuevo(cfg("L1"))
    r = o.cambiar_nivel("TACTICA", "L2", "OPERADOR", MS, t(31), AP)
    h.chk("r02_sin_foto_ni_conciliacion_no_se_sube", not r["ok"] and r["codigo"] == "O-39" and "foto" in r["motivo"] and "conciliación" in r["motivo"], r)
    o = nuevo(cfg("L1"))
    datos(o, t(31))
    r = o.cambiar_nivel("TACTICA", "L2", "OPERADOR", MS, t(31, 24 * 60), AP)
    h.chk("r02_una_foto_vieja_no_vale", not r["ok"] and r["codigo"] == "O-39" and "foto" in r["motivo"], r)
    o = nuevo(cfg("L2"))
    registrar_foto(o, {**CART, "fecha_hora": t(10), "perdida_dia_eur": 2000.0})
    cn(o, "TACTICA", "L1", "OPERADOR", MB, t(10, 60))
    registrar_foto(o, {**CART, "fecha_hora": t(10, 120), "perdida_dia_eur": 3000.0})
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(40, 90), AP)
    h.chk("r03_el_alcance_del_mismo_dia_cuenta_aunque_se_anotara_antes", not r["ok"] and r["codigo"] == "O-39" and "límite de pérdida" in r["motivo"], r)
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(42), AP)
    h.chk("r03_y_al_dia_siguiente_de_la_ventana_ya_no", r["ok"] and r["codigo"] == "O-28", r)
    o = nuevo(cfg("L1"))
    o.reportar_discrepancia([{"tipo": "POSICION", "ref": "TACTICA", "detalle": "x"}], "G", t(1))
    cn(o, "TACTICA", "L0", "OPERADOR", MB, t(2))
    r = cn(o, "TACTICA", "L1", "OPERADOR", MS, t(33), AP)
    h.chk("r04_una_discrepancia_sin_acusar_impide_subir_aunque_sea_antigua", not r["ok"] and r["codigo"] == "O-39" and "sin acusar" in r["motivo"], r)
    for av in list(o.avisos):
        o.acusar_aviso(av["id"], "OPERADOR", t(33, 1))
    r = cn(o, "TACTICA", "L1", "OPERADOR", MS, t(33, 2), AP)
    h.chk("r04_acusada_y_fuera_de_la_ventana_ya_no", r["ok"] and r["codigo"] == "O-28", r)
    o = nuevo(cfg("L0"))
    o.reportar_discrepancia([{"tipo": "POSICION", "ref": "TACTICA", "detalle": "x"}], "G", t(1))
    for av in list(o.avisos):
        o.acusar_aviso(av["id"], "OPERADOR", t(1, 1))
    r = cn(o, "TACTICA", "L1", "OPERADOR", MS, t(400), AP)
    h.chk("r05_un_incidente_antiguo_y_acusado_no_bloquea_para_siempre", r["ok"] and r["codigo"] == "O-28", r)
    o = nuevo(cfg("L1", aprobacion={**CONFIG_DEFECTO["aprobacion"], "canales": ["CONSOLA", "MOVIL"]}))
    cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31), AP)
    r = cn(o, "TACTICA", "L2", "OPERADOR", MS, t(31, 30), {"canal": "MOVIL", "segundo_factor": True})
    h.chk("la_confirmacion_por_otro_canal_vuelve_a_solicitar", r["ok"] and r["aplicado"] is False and o.nivel("TACTICA") == "L1", r)
    h.chk("ninguna_migracion_puede_tocar_el_nivel", "cfg.nivel_autonomia" in mg.PROHIBIDAS)
    h.chk("los_incidentes_de_promocion_van_en_la_huella", o.configuracion()["constantes"]["incidentes_promocion"] == list(INCIDENTES_PROMOCION))

    # ------------------------------------------------------------------------------------------- integridad y persistencia
    o = nuevo(cfg("L1"))
    subir(o)
    o.limites["entradas"][-1]["nivel"] = "L3"
    h.chk("tocar_la_entrada_NIVEL_rompe_la_configuracion", not o.config_integra())
    o = nuevo(cfg("L1"))
    subir(o)
    o.cfg["nivel_autonomia"]["TACTICA"] = "L3"
    h.chk("tocar_el_nivel_por_fuera_rompe_la_configuracion", not o.config_integra()
          and cn(o, "TACTICA", "L1", "OPERADOR", MB, t(32))["codigo"] == "O-13")
    h.chk("r06_y_activa_el_kill_switch_como_en_el_resto", o.kill is not None and any(x["codigo"] == "O-26" for x in o.avisos))
    o = nuevo(cfg("L1"))
    subir(o)
    cn(o, "TACTICA", "L3", "OPERADOR", MS, t(62), AP)   # solicitud pendiente
    texto = pe.volcar(o, t(62, 1))
    r = pe.cargar(texto)
    o2 = r.get("orquestador")
    h.chk("se_guarda_y_se_carga", r["ok"] and o2.nivel("TACTICA") == "L2" and o2.config_integra() and o2.integridad() == [], r.get("motivo"))
    r = cn(o2, "TACTICA", "L3", "OPERADOR", MS, t(62, 30), AP)
    h.chk("y_la_solicitud_pendiente_se_confirma_tras_cargar", r["ok"] and r["aplicado"] and o2.nivel("TACTICA") == "L3", r)

    # ------------------------------------------------------------------------------------------- migración de un estado de V0.50
    viejo = (AQUI / "estados" / "estado_V0_50.json").read_text(encoding="ascii")
    d = json.loads(viejo)
    h.chk("el_estado_de_V0_50_es_genuino", d["esquema"] == mg.ESQUEMA_V0_50 and "promocion_nivel" not in d["estado"]["cfg"]
          and d["estado"]["cfg"]["version_config"] == "CFG-0.9.0")
    h.chk("con_este_codigo_no_se_carga_PE08", pe.cargar(viejo)["codigo"] == "PE-08")
    r = mg.migrar(viejo, "2026-11-07T10:00:00+00:00", "Paso el estado guardado al código de V0.51")
    o2 = r.get("orquestador")
    h.chk("MIG003_lo_migra", r["ok"] and r["migraciones"] == ["MIG-003"] and o2.cfg["promocion_nivel"] == {"periodo_min_dias": 30}
          and o2.cfg["version_config"] == "CFG-0.10.0" and o2.integridad() == [] and o2.config_integra(), r.get("motivo"))
    h.chk("MIG003_no_cambia_el_nivel_de_nadie", o2.cfg["nivel_autonomia"] == d["estado"]["cfg"]["nivel_autonomia"])
    h.chk("MIG003_declara_lo_que_cambia", [m for m in mg.MIGRACIONES if m.id == "MIG-003"][0].cambia == frozenset({"cfg.promocion_nivel"}))
    h.chk("y_tras_migrar_se_puede_bajar", cn(o2, "TACTICA", "L0", "OPERADOR", MB, "2026-11-07T10:05:00+00:00")["ok"] and o2.config_integra())
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO NIVEL CAMBIO T-18:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
