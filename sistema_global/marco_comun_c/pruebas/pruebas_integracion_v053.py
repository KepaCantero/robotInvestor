"""Pruebas de la integración de V0.53: las piezas de GLM (V0.37 a V0.41: robustez de validadores, tope de LIBRES T-33, pantalla
de F, cortacircuito T-40 y reducción parcial a mano T-44) sobre la línea V0.52 (T-03, T-18, T-43). Prueba lo que nace de juntarlas:
la migración MIG-004 de los estados guardados, T-52 (rearmar exige integridad), y que lo de GLM cuenta en la promoción de nivel
(T-18) y convive con la reducción ajustada al paso (T-43). Datos SIMULADOS.

Uso: python3 pruebas/pruebas_integracion_v053.py
"""
import json
import math
import sys
from datetime import datetime, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import migraciones as mg  # noqa: E402
import persistencia as pe  # noqa: E402
from control_f import POLITICA_DEFECTO  # noqa: E402
from ejecucion_g import conciliar, declarar_manual, reducir  # noqa: E402
from orquestador import CONFIG_DEFECTO  # noqa: E402
from pruebas_control_f import CART, registrar_foto  # noqa: E402
from pruebas_ejecucion_g import broker  # noqa: E402
from pruebas_manual import PID, T1, a_mano, libre  # noqa: E402
from pruebas_manual_t44 import abierta_min, arma_parcial, rparcial  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, hasta, nuevo  # noqa: E402

AP = {"canal": "CONSOLA", "segundo_factor": True}
MS = "Un mes estable en L1: subo la táctica a L2"
LISTA = {k: True for k in ("causa_corregida", "conciliacion_limpia", "datos_frescos", "protecciones_verificadas")}


def t(dias=0, minutos=0):
    return (datetime.fromisoformat(AHORA) + timedelta(days=dias, minutes=minutos)).isoformat()


def datos(o, ahora, b=None):
    registrar_foto(o, {**CART, "fecha_hora": ahora})
    conciliar(o, b or broker(), ahora)


def sube(o, ahora, b=None):
    datos(o, ahora, b)
    return o.cambiar_nivel("TACTICA", "L2", "OPERADOR", MS, ahora, AP)


def main():
    h = Arnes()
    # ------------------------------------------------------------------------------------------- configuración y esquema
    h.chk("CFG_0110_integra_las_dos_lineas", CONFIG_DEFECTO["version_config"] == "CFG-0.11.0"
          and CONFIG_DEFECTO["libres_tope_dia_eur"] == {"TRADING": 2000.0, "TACTICA": 2000.0, "LARGO_PLAZO": 2000.0}
          and CONFIG_DEFECTO["promocion_nivel"] == {"periodo_min_dias": 30} and "umbral_l2_eur" in CONFIG_DEFECTO)
    # V0.67: el esquema del código pasa a V0.67 (MIG-005, sin cambios en el estado); V0.53 sigue registrado y MIG-004 en la cadena
    mig004 = next((m for m in mg.MIGRACIONES if m.id == "MIG-004"), None)
    h.chk("esquema_V0_53_registrado_y_MIG004_en_la_cadena", mg.ESQUEMA_V0_53 in mg.ESQUEMAS and mig004 is not None
          and mig004.esquema_desde == mg.ESQUEMA_V0_51 and mig004.esquema_hasta == mg.ESQUEMA_V0_53)
    mig005 = next((m for m in mg.MIGRACIONES if m.id == "MIG-005"), None)
    h.chk("v067_esquema_registrado_y_MIG005_sin_cambios", mg.ESQUEMA_V0_67 in mg.ESQUEMAS and mig005 is not None
          and mig005.esquema_desde == mg.ESQUEMA_V0_53 and mig005.esquema_hasta == mg.ESQUEMA_V0_67 and mig005.aplicar is mg._sin_cambios
          and mig005.cambia == frozenset())
    # V0.68 (T-80): el esquema del código pasa a V0.68 (MIG-006: el rastro SC-5 de las consultas, vacío)
    mig006 = next((m for m in mg.MIGRACIONES if m.id == "MIG-006"), None)
    h.chk("v068_esquema_registrado_y_MIG006_con_el_rastro_vacio", mg.ESQUEMA_V0_68 in mg.ESQUEMAS and mig006 is not None
          and mig006.esquema_desde == mg.ESQUEMA_V0_67 and mig006.esquema_hasta == mg.ESQUEMA_V0_68
          and mig006.cambia == frozenset() and mg._v068({})["consultas"] == {"historial": [], "estado": "VIGENTE", "entradas": []})
    # V0.70 (T-75): el esquema del código pasa a V0.70 (MIG-007, sin cambios en el estado: aviso O-40 y parámetros nuevos)
    mig007 = next((m for m in mg.MIGRACIONES if m.id == "MIG-007"), None)
    h.chk("v070_esquema_registrado_y_MIG007_sin_cambios", mg.ESQUEMA_V0_70 in mg.ESQUEMAS and mig007 is not None
          and mig007.esquema_desde == mg.ESQUEMA_V0_68 and mig007.esquema_hasta == mg.ESQUEMA_V0_70
          and mig007.aplicar is mg._sin_cambios and mig007.cambia == frozenset())
    # V0.71 (T-76): el esquema del código pasa a V0.71 (MIG-008: el registro de la cartera sombra, vacío)
    h.chk("v071_esquema_actual_y_MIG008_con_la_sombra_vacia", pe.esquema_actual() == mg.ESQUEMA_V0_71 and mg.ESQUEMA_V0_71 in mg.ESQUEMAS
          and mg.MIGRACIONES[-1].id == "MIG-008" and mg.MIGRACIONES[-1].esquema_desde == mg.ESQUEMA_V0_70
          and mg.MIGRACIONES[-1].cambia == frozenset() and mg._v071({})["sombra"] == {"historial": [], "estado": "VIGENTE", "entradas": []})

    # ------------------------------------------------------------------------------------------- MIG-004
    viejo = (AQUI / "estados" / "estado_V0_52.json").read_text(encoding="ascii")
    d = json.loads(viejo)
    h.chk("el_estado_de_V0_52_es_genuino", d["esquema"] == mg.ESQUEMA_V0_51 and "libres_tope_dia_eur" not in d["estado"]["cfg"]
          and "libres" not in d["estado"] and d["estado"]["cfg"]["version_config"] == "CFG-0.10.0")
    h.chk("con_este_codigo_no_se_carga_PE08", pe.cargar(viejo)["codigo"] == "PE-08")
    r = mg.migrar(viejo, "2026-11-08T10:00:00+00:00", "Paso el estado guardado al código de V0.53")
    o2 = r.get("orquestador")
    h.chk("MIG004_lo_migra", r["ok"] and r["migraciones"] == ["MIG-004", "MIG-005", "MIG-006", "MIG-007", "MIG-008"] and o2.cfg["libres_tope_dia_eur"] == CONFIG_DEFECTO["libres_tope_dia_eur"]
          and o2.libres == [] and o2.cortacircuitos == [] and o2.cfg["version_config"] == "CFG-0.11.0"
          and o2.integridad() == [] and o2.config_integra(), r.get("motivo"))
    h.chk("MIG004_no_cambia_el_nivel_de_nadie_ni_lo_demas", o2.cfg["nivel_autonomia"] == d["estado"]["cfg"]["nivel_autonomia"]
          and o2.cfg["promocion_nivel"] == d["estado"]["cfg"]["promocion_nivel"] and len(o2.expedientes) == len(d["estado"]["expedientes"]))
    h.chk("MIG004_declara_lo_que_cambia", [m for m in mg.MIGRACIONES if m.id == "MIG-004"][0].cambia == frozenset({"cfg.libres_tope_dia_eur", "libres"}))
    v50 = (AQUI / "estados" / "estado_V0_50.json").read_text(encoding="ascii")
    r = mg.migrar(v50, "2026-11-08T10:00:00+00:00", "Paso el estado guardado al código de V0.53")
    h.chk("desde_V0_50_la_cadena_es_MIG003_a_MIG008", r["ok"] and r["migraciones"] == ["MIG-003", "MIG-004", "MIG-005", "MIG-006", "MIG-007", "MIG-008"] and r["orquestador"].integridad() == [], r.get("motivo"))
    d2 = json.loads(viejo)
    d2["estado"]["cfg"]["version_config"] = "CFG-7.7.7"
    h.chk("una_version_de_configuracion_propia_no_se_pisa", mg._v053(d2["estado"])["cfg"]["version_config"] == "CFG-7.7.7")

    # ------------------------------------------------------------------------------------------- T-52: rearmar exige integridad
    o = nuevo()
    hasta(o, "PROPUESTA")
    o.activar_kill_switch("prueba de T-52", "OPERADOR", t(0, 10))
    for av in list(o.avisos):
        o.acusar_aviso(av["id"], "OPERADOR", t(0, 11))
    conciliar(o, broker(), t(0, 12))
    o.expedientes["EXP-0001"]["historial"][0]["motivo"] = "tocado por fuera"
    r = o.rearmar_kill_switch(LISTA, "OPERADOR", t(0, 13))
    h.chk("T52_sin_integridad_no_se_rearma_O13", not r["ok"] and r["codigo"] == "O-13" and "EXP" in r["motivo"] and o.kill is not None, r)
    o = nuevo()
    hasta(o, "PROPUESTA")
    o.activar_kill_switch("prueba de T-52", "OPERADOR", t(0, 10))
    for av in list(o.avisos):
        o.acusar_aviso(av["id"], "OPERADOR", t(0, 11))
    conciliar(o, broker(), t(0, 12))
    h.chk("T52_con_integridad_si", o.rearmar_kill_switch(LISTA, "OPERADOR", t(0, 13))["ok"] and o.kill is None)

    # ------------------------------------------------------------------------------------------- lo de GLM cuenta para subir de nivel
    o = nuevo({"nivel_autonomia": {"TRADING": "L1", "TACTICA": "L1", "LARGO_PLAZO": "L1"}})
    registrar_foto(o, {**CART, "fecha_hora": t(10), "perdida_dia_eur": 2600.0})   # salta el cortacircuito (T-40, 2500 EUR)
    h.chk("el_cortacircuito_activa_el_kill_switch", o.kill is not None and o.kill["motivo"].startswith("cortacircuito"))
    r = sube(o, t(31))
    h.chk("con_el_cortacircuito_activo_no_se_sube_O26", not r["ok"] and r["codigo"] == "O-26", r)
    registrar_foto(o, {**CART, "fecha_hora": t(31, 1), "perdida_dia_eur": 0.0})
    for av in list(o.avisos):
        o.acusar_aviso(av["id"], "OPERADOR", t(31, 2))
    conciliar(o, broker(), t(31, 3))
    h.chk("rearmado_tras_bajar_la_perdida", o.rearmar_kill_switch(LISTA, "OPERADOR", t(31, 4))["ok"])
    r = sube(o, t(32))
    h.chk("un_cortacircuito_en_la_ventana_impide_subir_O39", not r["ok"] and r["codigo"] == "O-39" and "kill-switch" in r["motivo"], r)
    r = sube(o, t(62))
    h.chk("y_fuera_de_la_ventana_ya_no", r["ok"] and r["codigo"] == "O-28", r)

    o = nuevo({"nivel_autonomia": {"TRADING": "L1", "TACTICA": "L1", "LARGO_PLAZO": "L1"},
               "libres_tope_dia_eur": {"TRADING": 2000.0, "TACTICA": 50.0, "LARGO_PLAZO": 2000.0}})
    registrar_foto(o, {**CART, "fecha_hora": T1})
    bl = broker()
    a_mano(bl, "GBPUSD", "COMPRA", 50.0, "MAN-GBP-1")   # lo que hizo el operador en el intermediario
    r = o.registrar_manual(libre(), T1)   # una LIBRE de la táctica por encima de su tope: O-37 y degrada (en L1, sin bajar)
    h.chk("una_LIBRE_sobre_el_tope_avisa_O37", r["ok"] and r.get("tope_libres_superado") is True and any(x["codigo"] == "O-37" for x in o.avisos), r)
    h.chk("y_queda_como_degradacion_aunque_la_cartera_este_en_L1", "TACTICA" in o.ultimas_degradaciones)
    for av in list(o.avisos):
        o.acusar_aviso(av["id"], "OPERADOR", t(1))
    r = sube(o, t(30), bl)   # la ventana de 30 días acaba de empezar con el registro de la LIBRE
    h.chk("una_LIBRE_sobre_el_tope_en_la_ventana_impide_subir_O39", not r["ok"] and r["codigo"] == "O-39" and "degradó" in r["motivo"], r)
    r = sube(o, t(31), bl)
    h.chk("y_un_dia_despues_de_salir_de_la_ventana_ya_no", r["ok"] and r["codigo"] == "O-28", r)

    # ------------------------------------------------------------------------------------------- T-44 (a mano) con T-43 (por G)
    o, b = abierta_min()
    arma_parcial(o, b)   # el operador vende 40 de 100 a mano y deja un stop por 60
    r = declarar_manual(o, rparcial(), b, T1)
    p = o.posiciones[PID]
    h.chk("T44_la_parcial_a_mano_queda_en_60", r["ok"] and p["cantidad"] == 60.0 and p["reducciones"][-1].get("manual") is True, r)
    h.chk("y_concilia_limpio", conciliar(o, b, T1)["ok"])
    b.mover_precio("EURUSD", 1.10, T1)
    v = o.cantidad_reduccion(PID, T1, cantidad=20.0)
    h.chk("T43_despues_reduce_por_G_ajustado_al_paso", v["ok"] and v["cantidad"] == 20.0 and v["restante"] == 40.0, v)
    v = o.cantidad_reduccion(PID, T1, cantidad=45.0)   # quedarían 15 x 1,10 = 16,50 EUR < 20 EUR (mínimo de F de la batería T-44)
    h.chk("T43_y_respeta_el_minimo_de_F_sobre_lo_que_dejo_la_parcial", not v["ok"] and "ciérrela entera" in v["motivo"], v)
    r = reducir(o, PID, b, T1, cantidad=20.0, actor="OPERADOR", motivo="reduzco otra parte por G tras la parcial a mano")
    h.chk("T43_la_reduccion_por_G_tras_la_manual_concilia", r["ok"] and o.posiciones[PID]["cantidad"] == 40.0 and conciliar(o, b, T1)["ok"]
          and o.integridad() == [], r)
    # ------------------------------------------------------------------------------------------- revisión de GLM (g02)
    from comparador import comparar_candidatos
    from pruebas_comparador import cand
    r = comparar_candidatos([cand(1, instrumento="ΑΒΓ"), cand(2, esperado=(3.0, 0.5, -4.0), instrumento="ΔΕΖ")], AHORA)
    rank = [x for g in r.get("grupos", {}).values() for x in g["ranking"]]
    h.chk("g02_D_no_toma_por_el_mismo_dos_instrumentos_sin_identidad", not any(x["motivo"] == "DUPLICADO" for x in r.get("excluidos", []))
          and not rank and all(x["motivo"] == "FORMA" for x in r.get("excluidos", [])) and len(r.get("excluidos", [])) == 2, r)
    # ------------------------------------------------------------------------------------------- revisión de la integración (h01-h06)
    import os
    import tempfile
    from ejecucion_g import BrokerSimulado
    from pruebas_ejecucion_g import HORA_DATOS
    from pruebas_manual import T2, abierta_l1
    from pruebas_manual_t44 import coloca_stop
    from vigilancia import vigilar
    # h01: la posición que cerró su stop retirado no reaparece como huérfana cuando el instrumento vuelve a tener cantidad
    o, b = abierta_min()
    arma_parcial(o, b)
    assert o.registrar_manual(rparcial(event_id="EV-R-H01"), T1)["ok"]
    b.mover_precio("EURUSD", 1.04, T2)
    vigilar(o, b, {"EURUSD": {"precio": 1.04, "hora": T2}}, T2)
    T3 = "2026-11-06T09:15:00+00:00"
    registrar_foto(o, {**CART, "fecha_hora": T3})
    a_mano(b, "EURUSD", "COMPRA", 10.0, "MAN-EUR-L1")
    r = o.registrar_manual(libre(event_id="EV-R-H01-L", instrumento="EURUSD", activo_base="EUR", cantidad=10.0, precio=1.04,
                                 ref_intermediario="MAN-EUR-L1", emitido_en=T3, ejecutado_en=T3), T3)
    c = conciliar(o, b, T3)
    h.chk("h01_la_cerrada_por_su_stop_retirado_no_reaparece_huerfana", o.posiciones[PID]["estado"] == "CERRADA" and r["ok"] and c["ok"], c)

    # h02: un stop retirado que vende más de lo que queda no explica un cierre (aunque luego el neto quede a cero)
    class Real(BrokerSimulado):
        def _fill(self, orden, q, precio):
            vivos = {k for k, x in self.ordenes.items() if x["estado"] == "ACEPTADA" and x["orden"]["tipo"] == "STOP" and not x["orden"].get("solo_reduccion")}
            super()._fill(orden, q, precio)
            for k in vivos:
                if self.ordenes[k]["estado"] == "CANCELADA":
                    self.ordenes[k]["estado"] = "ACEPTADA"
    o, b = abierta_min(b=Real(100000.0, {"EURUSD": 1.10}, HORA_DATOS))
    arma_parcial(o, b)
    assert declarar_manual(o, rparcial(), b, T1)["ok"]
    a_mano(b, "EURUSD", "VENTA", 20.0, "MAN-RED-2")
    assert coloca_stop(b, "MAN-STOP-3", 40.0, precio=1.03)["estado"] == "ACEPTADA"
    assert o.registrar_manual(rparcial(event_id="EV-R-H02", cantidad=20.0, ref_intermediario="MAN-RED-2", proteccion_ref="MAN-STOP-3"), T1)["ok"]
    b.mover_precio("EURUSD", 1.04, T1)   # salta MAN-STOP-2 (60) sobre 40
    a_mano(b, "EURUSD", "COMPRA", 20.0, "MAN-OCULTA")   # el operador lo aplana sin declararlo
    rv = vigilar(o, b, {"EURUSD": {"precio": 1.04, "hora": T2}}, T2)
    c = conciliar(o, b, T2)
    h.chk("h02_un_stop_retirado_mayor_no_explica_el_cierre", o.posiciones[PID]["estado"] != "CERRADA" and not c["ok"]
          and any(d["tipo"] == "PROTECCION_HUERFANA" for d in c["diferencias"]), (rv["acciones"], c))

    # h03: MIG-004 reconstruye las LIBRES ya declaradas: siguen contando en F-14 y en su tope
    texto = (AQUI / "estados" / "estado_V0_52_con_libre.json").read_text(encoding="ascii")
    r = mg.migrar(texto, T1, "Paso el estado guardado al código de V0.53")
    o2 = r["orquestador"]
    o3, b3 = abierta_l1()
    a_mano(b3, "GBPUSD", "COMPRA", 50.0, "MAN-GBP-1")
    assert o3.registrar_manual(libre(), T1)["ok"]
    from validar_sobre import _dt as _dts
    a2, a3 = o2._actividad(None, _dts(T2)), o3._actividad(None, _dts(T2))
    h.chk("h03_MIG004_reconstruye_las_LIBRES_declaradas", r["ok"] and o2.integridad() == [] and len(o2.libres) == len(o3.libres) == 1
          and a2["importe_dia_eur"] == a3["importe_dia_eur"] and o2.libres[0]["importe_eur"] == o3.libres[0]["importe_eur"], (o2.libres, o3.libres))

    # h04: una semana de pérdidas que desborda se satura: el cortacircuito salta y el estado se guarda
    o = nuevo()
    cta = o.cfg["cuenta_intermediario"]
    o.registrar_cartera({**CART, "fecha_hora": "2026-11-06T09:30:00+00:00", "perdida_dia_eur": 1e308}, "G", "2026-11-06T09:30:00+00:00", cuenta=cta)
    o.registrar_cartera({**CART, "fecha_hora": "2026-11-07T09:30:00+00:00", "perdida_dia_eur": 1e308}, "G", "2026-11-07T09:30:00+00:00", cuenta=cta)
    d = tempfile.mkdtemp(prefix="v053-")
    g = pe.guardar(o, os.path.join(d, "estado.json"), "2026-11-07T09:31:00+00:00")
    h.chk("h04_la_semana_desbordada_se_satura_y_se_guarda", g["ok"] and o.kill is not None
          and all(math.isfinite(x["perdida_semana_eur"]) for x in o.cortacircuitos), g)

    # h06: un O-37 sin acusar impide subir de nivel (aunque la cartera estuviera en L1 y no hubiera O-19)
    o = nuevo({"nivel_autonomia": {"TRADING": "L1", "TACTICA": "L1", "LARGO_PLAZO": "L1"},
               "libres_tope_dia_eur": {"TRADING": 2000.0, "TACTICA": 50.0, "LARGO_PLAZO": 2000.0}})
    registrar_foto(o, {**CART, "fecha_hora": T1})
    bl = broker()
    a_mano(bl, "GBPUSD", "COMPRA", 50.0, "MAN-GBP-1")
    assert o.registrar_manual(libre(), T1)["tope_libres_superado"]
    for av in list(o.avisos):
        if av["codigo"] != "O-37":
            o.acusar_aviso(av["id"], "OPERADOR", t(1))
    r = sube(o, t(32), bl)
    h.chk("h06_un_O37_sin_acusar_impide_subir", not r["ok"] and r["codigo"] == "O-39" and "O-37" in r["motivo"], r)
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO INTEGRACION V0.53:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
