"""Pruebas de T-40 (V0.39): cortacircuito global por pérdida (parte del T-40; el vigilante con latido queda para la Fase 3).

Lo que demuestra: al registrar una foto de cartera válida, si la pérdida del día de la foto o la pérdida de la semana (la suma
de los siete días que acaban en la fecha UTC de la foto, el mismo criterio que F-16) llega a su límite —incluido el caso igual—,
el Orquestador activa solo el kill-switch (§8 y §11) con actor ORQUESTADOR y motivo «cortacircuito global: …», emite el aviso
O-38 de prioridad ALTA con las dos cifras y sus límites, anota el disparo una vez por día UTC de la foto en `self.cortacircuitos`
y acepta el registro igual, con `cortacircuito: True/False`; una foto mal formada o rechazada no dispara nada; si el kill ya
estaba activo (manual u otra causa) el motivo no se pisa y el O-38 sale igual; el rearme se rechaza con O-35 mientras la última
foto siga en o por encima de alguno de los dos límites, y sale con la lista del §11 cuando baja o cambia el día; el kill del
cortacircuito no liquida nada (lo hace el kill-switch de siempre) y G cancela las entradas vivas como con los demás kills.
Las regresiones r01 y r02 fijan los hallazgos de la revisión independiente: la suma de la semana es plana (un desbordamiento
da infinito y el cortacircuito salta con él, sin lanzar) y el O-35 del rearme solo vale para el kill del cortacircuito
(actor ORQUESTADOR y su prefijo), no para un kill manual cuyo motivo empiece por «cortacircuito».

Uso: python3 pruebas/pruebas_cortacircuito_t40.py
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

from orquestador import PRIORIDAD_AVISO  # noqa: E402
from control_f import POLITICA_DEFECTO  # noqa: E402
from pruebas_control_f import CART, informe_f  # noqa: E402
from pruebas_ejecucion_g import autorizado, broker  # noqa: E402
from ejecucion_g import ejecutar, revisar_entrada  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, autorizar_op, hasta, nuevo  # noqa: E402

EID = "EXP-0001"
L2 = {"nivel_autonomia": {"TRADING": "L2", "TACTICA": "L2", "LARGO_PLAZO": "L2"}}
LISTA = ("causa_corregida", "conciliacion_limpia", "datos_frescos", "protecciones_verificadas")


def avisos(o, codigo):
    return [x for x in o.avisos if x["codigo"] == codigo]


def foto(o, t, perdida, ahora=None):
    """Lo que hace G: registra una foto con la pérdida dada a la hora t (su registro va un poco después, sin retroceder el reloj)."""
    return o.registrar_cartera({**CART, "fecha_hora": t, "perdida_dia_eur": perdida}, "G", ahora or t, cuenta=o.cfg["cuenta_intermediario"])


def main():
    h = Arnes()

    # ------------------------------------------------------------------ el límite justo del día
    o = nuevo(L2)
    hasta(o, "PROPUESTA")
    r = foto(o, "2026-11-06T09:01:00+00:00", 2499.99, "2026-11-06T09:01:30+00:00")   # bajo el límite de 2.500 EUR
    h.chk("bajo_el_limite_no_salta", r["ok"] and r["cortacircuito"] is False and o.kill is None
          and o.cortacircuitos == [] and avisos(o, "O-38") == [] and o.nivel("TACTICA") == "L2", r)
    r = foto(o, "2026-11-06T09:03:00+00:00", 2500.0, "2026-11-06T09:03:30+00:00")   # justo el límite: igual también salta
    h.chk("en_el_limite_igual_salta", r["ok"] and r["cortacircuito"] is True and o.kill is not None
          and o.kill["actor"] == "ORQUESTADOR"
          and o.kill["motivo"] == "cortacircuito global: pérdida del día 2500.00 EUR (límite 2500.00 EUR)"
          and o.nivel("TRADING") == "L1" and o.nivel("TACTICA") == "L1" and o.nivel("LARGO_PLAZO") == "L1", (r, o.kill))
    o26, o38 = avisos(o, "O-26"), avisos(o, "O-38")
    h.chk("el_aviso_O26_y_el_O38", len(o26) == 1 and len(o38) == 1 and o38[0]["prioridad"] == "ALTA"
          and o38[0]["ref"] == "CORTACIRCUITO" and "cortacircuito" in o26[0]["motivo"], (o26, o38))
    h.chk("el_aviso_O38_lleva_las_dos_cifras_y_sus_limites",
          o38[0]["motivo"] == "cortacircuito global por pérdida: día 2500.00 EUR (límite 2500.00 EUR), "
                              "semana 2500.00 EUR (límite 5000.00 EUR)", o38)
    h.chk("la_fila_del_dia_en_cortacircuitos", o.cortacircuitos == [{"dia": "2026-11-06", "perdida_dia_eur": 2500.0,
                                                                     "perdida_semana_eur": 2500.0, "ahora": "2026-11-06T09:03:30+00:00"}],
          o.cortacircuitos)
    inf = informe_f(o, cartera={**CART, "fecha_hora": "2026-11-06T09:04:00+00:00"})
    ra = autorizar_op(o, EID, inf, "2026-11-06T09:05:00+00:00")
    h.chk("autorizar_con_el_kill_del_cortacircuito_O26", ra["codigo"] == "O-26" and "kill" in ra["motivo"]
          and o.expedientes[EID]["estado"] == "PROPUESTA", ra)

    # ------------------------------------------------------------------ la semana repartida en varios días
    o = nuevo(L2, sellos=())   # sin sellos: el reloj arranca libre, para fotos de días anteriores a las 09:00
    foto(o, "2026-11-04T09:00:00+00:00", 1800.0)
    foto(o, "2026-11-05T09:00:00+00:00", 1800.0)
    r = foto(o, "2026-11-06T09:00:00+00:00", 1800.0)   # ningún día llega a 2.500; la semana llega a 5.400
    h.chk("la_semana_repartida_en_varios_dias_salta", r["ok"] and r["cortacircuito"] is True and o.kill is not None
          and o.kill["motivo"] == "cortacircuito global: pérdida de la semana 5400.00 EUR (límite 5000.00 EUR)"
          and o.cortacircuitos == [{"dia": "2026-11-06", "perdida_dia_eur": 1800.0, "perdida_semana_eur": 5400.0,
                                    "ahora": "2026-11-06T09:00:00+00:00"}], (r, o.kill, o.cortacircuitos))
    o = nuevo(L2, sellos=())
    foto(o, "2026-11-04T09:00:00+00:00", 2400.0)
    foto(o, "2026-11-05T09:00:00+00:00", 2400.0)
    r = foto(o, "2026-11-06T09:00:00+00:00", 2500.0)   # día y semana en el límite a la vez: el motivo cita el del día
    h.chk("con_dia_y_semana_en_el_limite_el_motivo_cita_el_del_dia",
          r["cortacircuito"] is True and o.kill["motivo"] == "cortacircuito global: pérdida del día 2500.00 EUR (límite 2500.00 EUR)"
          and o.cortacircuitos[0]["perdida_semana_eur"] == 7300.0, o.kill)
    # la fecha de la fila es la fecha UTC de la foto, aunque la foto venga con otra zona horaria
    o = nuevo(L2, sellos=())
    foto(o, "2026-11-04T09:00:00+00:00", 1900.0)
    foto(o, "2026-11-05T09:00:00+00:00", 1900.0)
    r = foto(o, "2026-11-07T00:30:00+01:00", 1900.0, "2026-11-06T23:30:00+00:00")   # son las 23:30 UTC del día 6
    h.chk("la_fila_lleva_el_dia_utc_de_la_foto", r["cortacircuito"] is True and len(o.cortacircuitos) == 1
          and o.cortacircuitos[0]["dia"] == "2026-11-06" and o.cortacircuitos[0]["perdida_semana_eur"] == 5700.0, o.cortacircuitos)

    # ------------------------------------------------------------------ una vez por día UTC de la foto
    o = nuevo(L2)
    r1 = foto(o, "2026-11-06T09:01:00+00:00", 2500.0, "2026-11-06T09:01:30+00:00")
    r2 = foto(o, "2026-11-06T09:03:00+00:00", 2600.0, "2026-11-06T09:03:30+00:00")   # la misma pérdida, el mismo día
    h.chk("una_segunda_foto_del_mismo_dia_no_repite_O38", r2["ok"] and r2["cortacircuito"] is True
          and len(avisos(o, "O-38")) == 1 and len(o.cortacircuitos) == 1
          and o.kill["motivo"] == "cortacircuito global: pérdida del día 2500.00 EUR (límite 2500.00 EUR)", (r1, r2, o.kill))
    r3 = foto(o, "2026-11-07T09:00:00+00:00", 2500.0)   # al día siguiente, en el límite otra vez: aviso y fila nuevos
    h.chk("al_dia_siguiente_vuelve_a_avisar_y_anotar", r3["ok"] and r3["cortacircuito"] is True
          and len(avisos(o, "O-38")) == 2 and len(avisos(o, "O-26")) == 1 and len(o.cortacircuitos) == 2
          and o.cortacircuitos[1] == {"dia": "2026-11-07", "perdida_dia_eur": 2500.0, "perdida_semana_eur": 5100.0,
                                      "ahora": "2026-11-07T09:00:00+00:00"}
          and o.kill["motivo"] == "cortacircuito global: pérdida del día 2500.00 EUR (límite 2500.00 EUR)", (r3, o.cortacircuitos, o.kill))

    # ------------------------------------------------------------------ una foto rechazada no dispara nada
    o = nuevo(L2)
    r = o.registrar_cartera({**CART, "de_mas": 1}, "G", AHORA, cuenta=o.cfg["cuenta_intermediario"])
    h.chk("foto_mal_formada_no_dispara", r["codigo"] == "O-01" and o.kill is None and o.cortacircuitos == []
          and avisos(o, "O-38") == [], r)
    r = o.registrar_cartera({**CART, "perdida_dia_eur": float("nan")}, "G", AHORA, cuenta=o.cfg["cuenta_intermediario"])
    h.chk("foto_con_perdida_nan_no_dispara", r["codigo"] == "O-01" and o.kill is None and o.cortacircuitos == [], r)
    r = o.registrar_cartera({**CART, "perdida_dia_eur": 2500.0}, "G", AHORA, cuenta="OTRA-CUENTA")
    h.chk("foto_rechazada_por_cuenta_no_dispara_aunque_vaya_en_el_limite", r["codigo"] == "O-29" and o.kill is None
          and o.cortacircuitos == [] and avisos(o, "O-38") == [], r)
    r = o.registrar_cartera({**CART, "fecha_hora": "2026-11-06T09:30:00+00:00", "perdida_dia_eur": 2500.0}, "G", AHORA,
                            cuenta=o.cfg["cuenta_intermediario"])   # del futuro
    h.chk("foto_del_futuro_no_dispara", r["codigo"] == "O-10" and o.kill is None and o.cortacircuitos == [], r)

    # ------------------------------------------------------------------ el rearme (flujo de la §11)
    o = nuevo(L2)
    hasta(o, "PROPUESTA")
    foto(o, "2026-11-06T09:01:00+00:00", 2500.0, "2026-11-06T09:01:30+00:00")
    lista = {k: True for k in o.LISTA_REHABILITACION}
    h.chk("rearme_sin_acusar_y_sin_conciliar_O06", o.rearmar_kill_switch(lista, "OPERADOR", "2026-11-06T09:02:00+00:00")["codigo"] == "O-06")
    for av in o.avisos:
        o.acusar_aviso(av["id"], "OPERADOR", "2026-11-06T09:02:30+00:00")
    o.registrar_conciliacion(True, "G", "2026-11-06T09:02:40+00:00")
    r = o.rearmar_kill_switch(lista, "OPERADOR", "2026-11-06T09:03:00+00:00")
    h.chk("rearme_con_la_perdida_en_el_limite_O35", r["codigo"] == "O-35"
          and r["motivo"] == "la pérdida sigue en el límite: no se rearma hasta que baje o cambie el día"
          and o.kill is not None and len(o.rearmes) == 0, r)
    r = foto(o, "2026-11-06T09:03:30+00:00", 1000.0, "2026-11-06T09:04:00+00:00")   # la pérdida del día baja
    h.chk("foto_nueva_por_debajo_y_rearme_ok", r["ok"] and r["cortacircuito"] is False
          and o.rearmar_kill_switch(lista, "OPERADOR", "2026-11-06T09:05:00+00:00")["ok"]
          and o.kill is None and len(o.rearmes) == 1 and o.nivel("TACTICA") == "L1", o.rearmes)
    r = foto(o, "2026-11-06T09:06:00+00:00", 2500.0, "2026-11-06T09:06:30+00:00")   # la pérdida vuelve al límite el mismo día
    h.chk("defecto_01_tras_un_rearme_el_cortacircuito_vuelve_a_saltar_el_mismo_dia", r["ok"] and r["cortacircuito"] is True
          and o.kill is not None and o.kill["motivo"].startswith("cortacircuito") and len(avisos(o, "O-26")) == 2
          and len(avisos(o, "O-38")) == 2 and len(o.cortacircuitos) == 2   # V0.53 (g03): cada activación deja su aviso y su fila
          and o.nivel("TACTICA") == "L1", (r, o.kill, o.cortacircuitos))
    o = nuevo(L2)   # al día siguiente, con la semana aún cargada por ayer pero bajo el tope semanal
    hasta(o, "PROPUESTA")
    foto(o, "2026-11-06T09:01:00+00:00", 2500.0, "2026-11-06T09:01:30+00:00")
    for av in o.avisos:
        o.acusar_aviso(av["id"], "OPERADOR", "2026-11-06T09:02:00+00:00")
    o.registrar_conciliacion(True, "G", "2026-11-06T09:02:10+00:00")
    foto(o, "2026-11-07T09:00:00+00:00", 0.0)
    h.chk("al_dia_siguiente_con_la_semana_cargada_se_rearma", o.rearmar_kill_switch(lista, "OPERADOR", "2026-11-07T09:05:00+00:00")["ok"]
          and o.kill is None, o.rearmes)

    # ------------------------------------------------------------------ un kill manual no se pisa
    o = nuevo(L2)
    o.activar_kill_switch("corte manual del operador", "OPERADOR", "2026-11-06T09:00:30+00:00")
    r = foto(o, "2026-11-06T09:01:00+00:00", 2500.0, "2026-11-06T09:01:30+00:00")
    h.chk("kill_manual_no_se_pisa_y_O38_sale", r["ok"] and r["cortacircuito"] is True
          and o.kill["motivo"] == "corte manual del operador" and o.kill["actor"] == "OPERADOR"
          and len(avisos(o, "O-38")) == 1 and len(o.cortacircuitos) == 1, (r, o.kill))
    for av in o.avisos:
        o.acusar_aviso(av["id"], "OPERADOR", "2026-11-06T09:02:00+00:00")
    o.registrar_conciliacion(True, "G", "2026-11-06T09:02:30+00:00")
    h.chk("el_rearme_de_un_kill_que_no_es_cortacircuito_no_exige_foto_baja",
          o.rearmar_kill_switch({k: True for k in o.LISTA_REHABILITACION}, "OPERADOR", "2026-11-06T09:03:00+00:00")["ok"], o.rearmes)

    # ------------------------------------------------------------------ no liquida nada y G cancela las entradas vivas
    o, b = autorizado(b=broker(precio=1.12), o=nuevo(L2))   # orden de entrada viva (el precio del intermediario está fuera del límite)
    ejecutar(o, EID, b, "2026-11-06T09:01:00+00:00")   # G envía la orden al intermediario: queda viva, pendiente de ejecutar
    r = o.registrar_cartera({**o.cartera_f(), "fecha_hora": "2026-11-06T09:02:00+00:00", "perdida_dia_eur": 2500.0},
                            "G", "2026-11-06T09:02:30+00:00", cuenta=o.cfg["cuenta_intermediario"])
    h.chk("el_cortacircuito_no_liquida_nada", r["ok"] and r["cortacircuito"] is True and o.kill is not None
          and o.kill["motivo"].startswith("cortacircuito")
          and b.consultar("ORD-EXP-0001-E-1")["estado"] == "ACEPTADA"   # el cortacircuito por sí solo no toca el intermediario
          and o.expedientes[EID]["orden_entrada"]["estado"] == "ENVIADA", (r, o.kill))
    rr = revisar_entrada(o, EID, b, "2026-11-06T09:03:00+00:00")   # G, en su siguiente paso: la cartera quedó degradada por el kill
    h.chk("y_g_cancela_la_entrada_viva_como_con_los_demas_kills", rr["codigo"] == "G-02"
          and b.consultar("ORD-EXP-0001-E-1")["estado"] == "CANCELADA"
          and o.expedientes[EID]["orden_entrada"]["estado"] == "CANCELADA" and o.nivel("TACTICA") == "L1", rr)

    # ------------------------------------------------------------------ el aviso nuevo y su prioridad
    h.chk("O38_es_un_aviso_de_prioridad_ALTA", PRIORIDAD_AVISO["O-38"] == "ALTA")

    # ------------------------------------------------------------------ regresiones de la revisión independiente
    o = nuevo(L2, sellos=())   # r01: la semana que desborda no mata el registro ni deja al cortacircuito sin disparar
    r1 = foto(o, "2026-11-05T09:00:00+00:00", 1e308)   # finita y válida: en el límite del día, salta
    r2 = foto(o, "2026-11-06T09:00:00+00:00", 1e308)   # la semana real (2e308) desborda: fsum lanzaba OverflowError y el registro moría con O-00
    o2 = nuevo({**L2, "politica_f": {**POLITICA_DEFECTO, "perdida_dia_max_eur": 1.7e308, "perdida_semana_max_eur": 1.75e308}}, sellos=())
    foto(o2, "2026-11-05T09:00:00+00:00", 9.9e307)   # bajo el límite del día: se acepta sin salto
    r3 = foto(o2, "2026-11-06T09:00:00+00:00", 9.9e307)   # la semana real (1.98e308) supera el límite semanal: el cortacircuito debe saltar
    h.chk("r01_la_semana_desbordada_no_mata_el_registro_y_el_cortacircuito_dispara",
          r1["ok"] and r1["cortacircuito"] is True and o.kill is not None
          and r2["ok"] and r2["cortacircuito"] is True and o.kill["motivo"].startswith("cortacircuito")
          and len(avisos(o, "O-38")) == 2 and len(o.cortacircuitos) == 2
          and o.cortacircuitos[1]["perdida_semana_eur"] == sys.float_info.max   # V0.53 (h04): saturada, finita y guardable
          and r3["ok"] and r3["cortacircuito"] is True and o2.kill is not None
          and o2.kill["motivo"].startswith("cortacircuito global: pérdida de la semana"), (r1, r2, r3, o.cortacircuitos, o2.kill))
    o = nuevo(L2)   # r02: un kill MANUAL cuyo motivo empieza por «cortacircuito» no es un kill del cortacircuito
    o.activar_kill_switch("cortacircuito manual: parada preventiva del operador", "OPERADOR", "2026-11-06T09:00:00+00:00")
    r = foto(o, "2026-11-06T09:01:00+00:00", 2500.0, "2026-11-06T09:01:30+00:00")   # el O-38 sale; el kill manual no se pisa
    for av in o.avisos:
        o.acusar_aviso(av["id"], "OPERADOR", "2026-11-06T09:02:00+00:00")
    o.registrar_conciliacion(True, "G", "2026-11-06T09:02:30+00:00")
    es_manual = o.kill is not None and o.kill["actor"] == "OPERADOR"   # el kill sigue siendo el manual antes del rearme
    rr = o.rearmar_kill_switch({k: True for k in o.LISTA_REHABILITACION}, "OPERADOR", "2026-11-06T09:03:00+00:00")
    h.chk("r02_el_rearme_de_un_kill_manual_con_prefijo_cortacircuito_no_exige_foto_baja",
          r["ok"] and r["cortacircuito"] is True and es_manual and rr["ok"] and o.kill is None,
          (r, rr))

    # V0.53 (revisión de la integración, g05 M3): el rearme también se rechaza si la pérdida de la SEMANA sigue en el límite
    from ejecucion_g import conciliar as _concilia
    o = nuevo()
    foto(o, "2026-11-06T09:00:00+00:00", 2400.0)
    foto(o, "2026-11-07T09:00:00+00:00", 2400.0)
    r = foto(o, "2026-11-08T09:00:00+00:00", 300.0)   # semana 5100 EUR >= 5000 EUR: salta por la semana, no por el día
    foto(o, "2026-11-08T09:01:00+00:00", 0.0)
    for x in list(o.avisos):
        o.acusar_aviso(x["id"], "OPERADOR", "2026-11-08T09:02:00+00:00")
    _concilia(o, broker(), "2026-11-08T09:03:00+00:00")
    rr = o.rearmar_kill_switch({k: True for k in o.LISTA_REHABILITACION}, "OPERADOR", "2026-11-08T09:04:00+00:00")
    h.chk("r03_no_se_rearma_con_la_perdida_de_la_semana_aun_en_el_limite_O35", r["cortacircuito"] is True and not rr["ok"]
          and rr["codigo"] == "O-35" and o.kill is not None, (r, rr))
    # V0.53 (g03): un segundo disparo el mismo día tras un rearme deja también su aviso O-38 y su fila
    o = nuevo()
    foto(o, "2026-11-06T09:00:00+00:00", 2600.0)
    foto(o, "2026-11-06T09:01:00+00:00", 0.0)
    for x in list(o.avisos):
        o.acusar_aviso(x["id"], "OPERADOR", "2026-11-06T09:02:00+00:00")
    _concilia(o, broker(), "2026-11-06T09:03:00+00:00")
    rr = o.rearmar_kill_switch({k: True for k in o.LISTA_REHABILITACION}, "OPERADOR", "2026-11-06T09:04:00+00:00")
    r = foto(o, "2026-11-06T09:05:00+00:00", 2600.0)
    h.chk("r04_un_segundo_disparo_el_mismo_dia_deja_aviso_y_fila", rr["ok"] and r["cortacircuito"] is True and o.kill is not None
          and len(o.cortacircuitos) == 2 and len(avisos(o, "O-38")) == 2, (rr, o.cortacircuitos))

    print(f"RESULTADO CORTACIRCUITO: {'TODAS LAS PRUEBAS PASAN' if h.ok else 'HAY FALLOS'} ({h.n} comprobaciones)")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
