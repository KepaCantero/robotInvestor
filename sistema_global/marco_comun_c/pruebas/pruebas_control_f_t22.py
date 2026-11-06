"""Pruebas de T-22: los controles de la §8 que le faltaban a F (F-13 a F-23), el contexto que le da el Orquestador (CF-09),
la cotización del intermediario que registra G y CT-G-08 0.3.0. Datos SIMULADOS.

Uso: python3 pruebas/pruebas_control_f_t22.py
"""
import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import contratos as ct  # noqa: E402
from control_f import POLITICA_DEFECTO, VERSION_ESQUEMA, VERSION_REGLAS, construir_informe, controlar, politica_valida, validar_informe_f  # noqa: E402
from dimensionado import dimensionar  # noqa: E402
from ejecucion_g import BrokerSimulado, cotizar as cotizar_g  # noqa: E402
from pruebas_control_f import AHORA_F, CART, informe_f, solicitud  # noqa: E402
from pruebas_orquestador import AHORA, ENTRADA, Arnes, autorizar_op, hasta, nuevo  # noqa: E402

P = POLITICA_DEFECTO
CTX = {"mandato": {"version": "MAN-0.1.0", "instrumentos_permitidos": None, "exclusiones": [], "apalancamiento_max": 1.0, "horizonte_max_dias": 365},
       "fecha_revision": "2026-11-20",
       "exclusiones_duras": {"sanciones": "OK", "invertibilidad": "OK", "acceso": "OK"},
       "evidencia": {"proporcion_verificado": 0.2, "fecha_corte": "2026-11-05", "valid_until": "2026-11-08T18:00:00+00:00"},
       "eventos": [],
       "autonomia": {"nivel": "L1", "kill_switch": False},
       "actividad": {"importe_dia_eur": 0.0, "ordenes_ultima_hora": 0, "perdida_semana_eur": 0.0},
       "precio_intermediario": {"valor": 1.10, "fecha_hora": "2026-11-06T08:55:00+00:00"}}


def cx(**cambios):
    """El contexto base con cambios en sus apartados («mandato__exclusiones»: el campo exclusiones de mandato)."""
    c = copy.deepcopy(CTX)
    for k, v in cambios.items():
        if "__" in k:
            a, b = k.split("__")
            c[a][b] = v
        else:
            c[k] = v
    return c


def f(sol=None, cart=None, pol=None, ahora=AHORA_F, ctx=None):
    return controlar(solicitud(**(sol or {})), {**CART, **(cart or {})}, pol or P, ahora, CTX if ctx is None else ctx)


def regla(r, nombre):
    return [c for c in r["controles"] if c["regla"] == nombre]


def veta(r, nombre):
    return r["resultado"] == "VETADO" and any(c["resultado"] == "VETA" for c in regla(r, nombre))


def main():
    h = Arnes()
    r = f()
    h.chk("base_aprobada_con_todas_las_reglas", r["resultado"] == "APROBADO" and {c["regla"] for c in r["controles"]} >= {f"F-{i:02d}" for i in range(1, 24)}, r)
    h.chk("version_reglas_F030", VERSION_REGLAS == "F-0.3.0" and VERSION_ESQUEMA == "0.3.0")

    # ------------------------------------------------------------------ límites nominales en euros (F-13 a F-17)
    r = f(sol={"cantidad": 5000.0}, pol={**P, "importe_max_orden_eur": 2200.0})
    h.chk("F13_importe_por_orden_reduce", r["resultado"] == "REDUCIDO" and abs(r["cantidad_aprobada"] - 2000.0) < 1e-5
          and regla(r, "F-13")[0]["resultado"] == "REDUCE", r)
    r = f(sol={"cantidad": 5000.0}, ctx=cx(actividad__importe_dia_eur=49000.0))
    h.chk("F14_importe_del_dia_reduce_a_lo_que_queda", r["resultado"] == "REDUCIDO" and abs(r["cantidad_aprobada"] - 1000.0 / 1.10) < 1e-5
          and regla(r, "F-14")[0]["resultado"] == "REDUCE", r)
    r = f(ctx=cx(actividad__importe_dia_eur=50000.0))
    h.chk("F14_dia_agotado_veta_por_valor_minimo", r["resultado"] == "VETADO" and veta(r, "F-11"), r)
    r = f(sol={"cantidad": 5000.0}, cart={"posiciones": [{"instrumento": "EURGBP", "activo_base": "EUR", "valor_eur": 29000.0}]},
          pol={**P, "concentracion_max_pct": 100.0, "exposicion_max_pct": 100.0})
    h.chk("F15_importe_por_activo_reduce", r["resultado"] == "REDUCIDO" and abs(r["cantidad_aprobada"] - 1000.0 / 1.10) < 1e-5
          and regla(r, "F-15")[0]["resultado"] == "REDUCE", r)
    r = f(cart={"perdida_dia_eur": 2500.0}, pol={**P, "perdida_dia_max_pct": 5.0})
    h.chk("F16_perdida_del_dia_en_euros_veta", veta(r, "F-16") and not veta(r, "F-08"), r)
    r = f(ctx=cx(actividad__perdida_semana_eur=5000.0))
    h.chk("F16_perdida_de_la_semana_veta", veta(r, "F-16"), r)
    r = f(ctx=cx(actividad__ordenes_ultima_hora=10))
    h.chk("F17_ordenes_por_hora_veta", veta(r, "F-17") and f(ctx=cx(actividad__ordenes_ultima_hora=9))["resultado"] == "APROBADO", r)

    # ------------------------------------------------------------------ controles previos (F-18 a F-23)
    for nombre, ctx, s in (("no_permitido", cx(mandato__instrumentos_permitidos=["GBPUSD"]), None),
                           ("excluido_con_otra_grafia", cx(mandato__exclusiones=["eur/usd"]), None),
                           ("apalancamiento", cx(), {"apalancamiento": 2.0}),
                           ("revision_mas_alla_del_horizonte", cx(mandato__horizonte_max_dias=10), None),
                           ("revision_ya_pasada", cx(fecha_revision="2026-11-06"), None)):
        r = f(ctx=ctx, sol=s, pol={**P, "apalancamiento_max": 3.0})
        h.chk(f"F18_mandato_{nombre}", veta(r, "F-18"), r["controles"])
    h.chk("F18_permitido_con_otra_grafia", f(ctx=cx(mandato__instrumentos_permitidos=["EUR/USD"]))["resultado"] == "APROBADO")
    r = f(ctx=cx(exclusiones_duras={"sanciones": "OK", "invertibilidad": "DESCONOCIDO", "acceso": "OK"}))
    h.chk("F19_exclusion_dura_no_OK_veta", veta(r, "F-19") and "invertibilidad" in regla(r, "F-19")[0]["motivo"], r)
    for nombre, ctx in (("pocas_verificadas", cx(evidencia__proporcion_verificado=0.01)),
                        ("corte_viejo", cx(evidencia__fecha_corte="2026-11-01")),
                        ("corte_futuro", cx(evidencia__fecha_corte="2026-11-07")),
                        ("sobre_vencido", cx(evidencia__valid_until="2026-11-06T08:00:00+00:00"))):
        h.chk(f"F20_evidencia_{nombre}", veta(f(ctx=ctx), "F-20"))
    r = f(ctx=cx(eventos=[{"fecha": "2026-11-07", "tipo": "BANCO_CENTRAL"}]))
    h.chk("F21_banco_central_en_la_ventana_veta", veta(r, "F-21") and "BANCO_CENTRAL" in regla(r, "F-21")[0]["motivo"], r)
    h.chk("F21_evento_fuera_de_la_ventana_no", f(ctx=cx(eventos=[{"fecha": "2026-11-09", "tipo": "BANCO_CENTRAL"}]))["resultado"] == "APROBADO")
    h.chk("F21_evento_no_restringido_no", f(ctx=cx(eventos=[{"fecha": "2026-11-06", "tipo": "DIVIDENDO"}]))["resultado"] == "APROBADO")
    h.chk("F21_calendario_ilegible_veta", veta(f(ctx=cx(eventos=None)), "F-21"))
    cart_tarde = {"fecha_hora": "2026-11-06T20:00:00+00:00"}
    tarde = cx(precio_intermediario={"valor": 1.10, "fecha_hora": "2026-11-06T20:00:00+00:00"})
    h.chk("F21_viernes_por_la_tarde_veta", veta(f(ahora="2026-11-06T20:05:00+00:00", cart=cart_tarde, ctx=tarde), "F-21"))
    h.chk("F21_viernes_antes_del_corte_no", f(ahora="2026-11-06T19:55:00+00:00", cart={"fecha_hora": "2026-11-06T19:50:00+00:00"},
                                              ctx=cx(precio_intermediario={"valor": 1.10, "fecha_hora": "2026-11-06T19:50:00+00:00"}))["resultado"] == "APROBADO")
    sab = cx(precio_intermediario={"valor": 1.10, "fecha_hora": "2026-11-07T10:00:00+00:00"}, evidencia__fecha_corte="2026-11-06",
             evidencia__valid_until="2026-11-09T00:00:00+00:00")
    h.chk("F21_sabado_veta", veta(f(ahora="2026-11-07T10:05:00+00:00", cart={"fecha_hora": "2026-11-07T10:00:00+00:00"}, ctx=sab), "F-21"))
    h.chk("F22_kill_switch_veta", veta(f(ctx=cx(autonomia__kill_switch=True)), "F-22"))
    h.chk("F22_nivel_desconocido_veta", veta(f(ctx=cx(autonomia__nivel="L9")), "F-22"))
    h.chk("F22_L0_y_L2_no_vetan", all(f(ctx=cx(autonomia__nivel=n))["resultado"] == "APROBADO" for n in ("L0", "L2")))
    h.chk("F23_sin_precio_del_intermediario_veta", veta(f(ctx=cx(precio_intermediario=None)), "F-23"))
    h.chk("F23_precio_viejo_veta", veta(f(ctx=cx(precio_intermediario={"valor": 1.10, "fecha_hora": "2026-11-06T08:30:00+00:00"})), "F-23"))
    h.chk("F23_precio_del_futuro_veta", veta(f(ctx=cx(precio_intermediario={"valor": 1.10, "fecha_hora": "2026-11-06T09:05:00+00:00"})), "F-23"))
    r = f(ctx=cx(precio_intermediario={"valor": 1.07, "fecha_hora": "2026-11-06T08:55:00+00:00"}))
    h.chk("F23_limite_lejos_del_mercado_veta", veta(r, "F-23") and abs(regla(r, "F-23")[0]["valor"] - (1.10 / 1.07 - 1) * 100) < 1e-9, r)
    h.chk("F23_dentro_de_la_deriva_no", f(ctx=cx(precio_intermediario={"valor": 1.09, "fecha_hora": "2026-11-06T08:55:00+00:00"}))["resultado"] == "APROBADO")

    # ------------------------------------------------------------------ forma, sin contexto, política
    for nombre, ctx in (("clave_de_mas", {**CTX, "x": 1}), ("mandato_sin_version", cx(mandato__version="")),
                        ("actividad_negativa", cx(actividad__importe_dia_eur=-1.0)), ("autorizaciones_no_entero", cx(actividad__ordenes_ultima_hora=1.5)),
                        ("evento_mal_formado", cx(eventos=[{"fecha": "mañana", "tipo": "BANCO_CENTRAL"}])), ("precio_cero", cx(precio_intermediario={"valor": 0, "fecha_hora": AHORA_F})),
                        ("no_objeto", [])):
        r = f(ctx=ctx)
        h.chk(f"contexto_mal_formado_{nombre}_F01", r["resultado"] == "VETADO" and r["controles"][0]["regla"] == "F-01", r["controles"][:1])
    r = controlar(solicitud(), CART, P, AHORA_F)
    h.chk("sin_contexto_solo_las_reglas_de_cantidad_uso_de_E", r["resultado"] == "APROBADO" and not regla(r, "F-18") and regla(r, "F-13") and regla(r, "F-15"), r)
    h.chk("politica_nueva_valida", politica_valida(P))
    for nombre, pol in (("ordenes_no_entero", {**P, "ordenes_max_hora": 2.5}), ("evidencia_mayor_que_1", {**P, "evidencia_verificada_min": 1.5}),
                        ("orden_mayor_que_dia", {**P, "importe_max_orden_eur": 60000.0}), ("dia_mayor_que_semana", {**P, "perdida_dia_max_eur": 6000.0}),
                        ("falta_una_clave", {k: v for k, v in P.items() if k != "importe_max_dia_eur"})):
        h.chk(f"politica_invalida_{nombre}", not politica_valida(pol))
    sol_e = {k: v for k, v in solicitud().items() if k != "cantidad"}
    e = dimensionar({**sol_e, "stop_precio": 1.0999}, {**CART, "capital_eur": 1e9}, P, AHORA_F, paso=1.0)
    h.chk("E_respeta_el_importe_por_orden", e["ok"] and e["limitada_por"] == "F-13" and e["valor_eur"] <= P["importe_max_orden_eur"], e)

    # ------------------------------------------------------------------ Orquestador: contexto, CF-09 y cotización de G
    o = nuevo(); hasta(o, "PROPUESTA")
    inf = informe_f(o)
    c = o.contexto_f("EXP-0001", inf["emitido_en"])
    h.chk("contexto_del_orquestador", inf["payload"]["entradas"]["contexto"] == c and c["mandato"]["version"] == o.mandato("TACTICA")["mandato"]["version"]
          and c["exclusiones_duras"] == {"sanciones": "OK", "invertibilidad": "OK", "acceso": "OK"} and c["autonomia"]["kill_switch"] is False
          and c["precio_intermediario"]["valor"] == ENTRADA["limite"], c)
    h.chk("informe_valido_en_contratos_030", ct.validar(inf) == [], ct.validar(inf))

    def vf(o_, i):
        x = o_.expedientes["EXP-0001"]
        return sorted({z["regla"] for z in validar_informe_f(i, {"ahora": AHORA, "expediente_id": "EXP-0001", "correlation_id": x["correlation_id"],
                                                                 "divisa_cotizacion": "USD", "propuesta": x["propuesta"], "cartera_destino": x["cartera_destino"],
                                                                 "politica": o_.cfg["politica_f"], "contexto": o_._contexto_de_informe("EXP-0001", i)})})
    h.chk("CF09_informe_valido", vf(o, inf) == [], vf(o, inf))
    falso = construir_informe("EV-F-0090", "EXP-0001", o.expedientes["EXP-0001"]["correlation_id"], o.expedientes["EXP-0001"]["propuesta"],
                              inf["payload"]["entradas"]["solicitud"], inf["payload"]["entradas"]["cartera"], inf["payload"]["entradas"]["politica"],
                              inf["emitido_en"], inf["valid_until"], contexto=cx(eventos=[], fecha_revision=c["fecha_revision"]))
    h.chk("CF09_contexto_escrito_por_quien_emite", vf(o, falso) == ["CF-09"], vf(o, falso))
    h.rechaza("CF09_autorizar_con_contexto_ajeno_O01", o, lambda: autorizar_op(o, "EXP-0001", falso, AHORA), "O-01")
    sin = construir_informe("EV-F-0091", "EXP-0001", o.expedientes["EXP-0001"]["correlation_id"], o.expedientes["EXP-0001"]["propuesta"],
                            inf["payload"]["entradas"]["solicitud"], inf["payload"]["entradas"]["cartera"], inf["payload"]["entradas"]["politica"],
                            inf["emitido_en"], inf["valid_until"])
    h.chk("sin_contexto_el_informe_no_vale_CF01", "CF-01" in vf(o, sin) and sin["resultado_politica"]["resultado"] == "VETADO", vf(o, sin))
    o2 = nuevo(); hasta(o2, "PROPUESTA")
    h.chk("sin_cotizacion_el_contexto_no_tiene_precio", o2.contexto_f("EXP-0001", AHORA)["precio_intermediario"] is None)
    i2 = informe_f(o2)
    assert o2.registrar_cotizacion({"instrumento": "EURUSD", "valor": 1.12, "fecha_hora": "2026-11-06T08:58:00+00:00"}, "G", "2026-11-06T09:10:00+00:00")["ok"]
    h.chk("una_cotizacion_registrada_despues_no_cambia_el_contexto_de_un_informe_anterior", vf(o2, i2) == []
          and o2.contexto_f("EXP-0001", "2026-11-06T09:10:00+00:00")["precio_intermediario"]["valor"] == 1.12, vf(o2, i2))
    h.rechaza("cotizacion_solo_de_G_O05", o2, lambda: o2.registrar_cotizacion({"instrumento": "EURUSD", "valor": 1.1, "fecha_hora": AHORA}, "BROKER", "2026-11-06T09:10:00+00:00"), "O-05")
    h.rechaza("cotizacion_mal_formada_O01", o2, lambda: o2.registrar_cotizacion({"instrumento": "EURUSD", "valor": -1, "fecha_hora": AHORA}, "G", "2026-11-06T09:10:00+00:00"), "O-01")
    T2 = "2026-11-06T09:10:00+00:00"
    h.rechaza("cotizacion_del_futuro_O10", o2, lambda: o2.registrar_cotizacion({"instrumento": "EURUSD", "valor": 1.1, "fecha_hora": "2026-11-06T09:30:00+00:00"}, "G", T2), "O-10")
    h.rechaza("cotizacion_anterior_a_la_ultima_O10", o2, lambda: o2.registrar_cotizacion({"instrumento": "EUR/USD", "valor": 1.1, "fecha_hora": "2026-11-06T08:00:00+00:00"}, "G", T2), "O-10")
    o3 = nuevo(); hasta(o3, "PROPUESTA")
    b = BrokerSimulado(100000.0, {"EURUSD": 1.0950}, "2026-11-06T08:59:00+00:00")
    r = cotizar_g(o3, b, "EURUSD", AHORA)
    h.chk("G_cotiza_el_precio_del_intermediario", r["ok"] and o3.contexto_f("EXP-0001", AHORA)["precio_intermediario"] == {"valor": 1.095, "fecha_hora": "2026-11-06T08:59:00+00:00"}, r)
    b.caido = True
    h.chk("G_sin_conexion_no_cotiza", cotizar_g(o3, b, "EURUSD", AHORA)["codigo"] == "O-01")
    h.chk("G_instrumento_sin_precio_no_cotiza", cotizar_g(o3, BrokerSimulado(1.0, {}, AHORA), "GBPUSD", AHORA)["codigo"] == "O-01")

    # actividad: importe autorizado hoy, autorizaciones de la última hora y pérdida de la semana
    o4 = nuevo(); hasta(o4, "PROPUESTA")
    assert autorizar_op(o4, "EXP-0001", informe_f(o4), AHORA)["ok"]
    from validar_sobre import _dt
    act = o4._actividad(None, _dt(AHORA))
    q = o4.expedientes["EXP-0001"]["control_f"]["cantidad_aprobada"]
    h.chk("actividad_cuenta_la_autorizacion", abs(act["importe_dia_eur"] - q * ENTRADA["limite"] * 1.0) < 1e-6 and act["ordenes_ultima_hora"] == 1, act)
    act2 = o4._actividad(None, _dt("2026-11-06T10:30:00+00:00"))
    h.chk("pasada_la_hora_no_cuenta_pero_el_dia_si", act2["ordenes_ultima_hora"] == 0 and act2["importe_dia_eur"] == act["importe_dia_eur"], act2)
    h.chk("otro_dia_no_cuenta", o4._actividad(None, _dt("2026-11-07T09:00:00+00:00"))["importe_dia_eur"] == 0.0)
    o5 = nuevo()
    for dia, perd in (("2026-11-06T09:30:00+00:00", 1000.0), ("2026-11-06T09:40:00+00:00", 400.0), ("2026-11-07T09:30:00+00:00", 1500.0),
                      ("2026-11-09T09:30:00+00:00", 700.0)):
        assert o5.registrar_cartera({**CART, "fecha_hora": dia, "perdida_dia_eur": perd}, "G", dia, cuenta="SIM-1")["ok"], dia
    h.chk("perdida_semana_suma_la_mayor_de_cada_dia", o5._actividad(None, _dt("2026-11-09T10:00:00+00:00"))["perdida_semana_eur"] == 3200.0)
    h.chk("perdida_semana_olvida_lo_de_hace_ocho_dias", o5._actividad(None, _dt("2026-11-13T10:00:00+00:00"))["perdida_semana_eur"] == 2200.0
          and o5._actividad(None, _dt("2026-11-14T10:00:00+00:00"))["perdida_semana_eur"] == 700.0)

    # integración: un veto de contexto llega al operador como veto de F
    o6 = nuevo(); hasta(o6, "PROPUESTA")
    v = informe_f(o6, pol=None)
    h.chk("integracion_aprobado", v["resultado_politica"]["resultado"] == "APROBADO", v["resultado_politica"]["motivo"])
    o7 = nuevo({"politica_f": {**P, "evidencia_verificada_min": 0.5}}); hasta(o7, "PROPUESTA")
    v = informe_f(o7)
    h.chk("integracion_evidencia_insuficiente_veta_F20", v["resultado_politica"]["resultado"] == "VETADO" and v["resultado_politica"]["motivo"].startswith("veta F-20"),
          v["resultado_politica"]["motivo"])
    h.rechaza("integracion_vetado_O06", o7, lambda: autorizar_op(o7, "EXP-0001", v, AHORA), "O-06", mutacion_permitida=True)
    o8 = nuevo({"politica_f": {**P, "importe_max_orden_eur": 50.0, "valor_min_eur": 10.0}}); hasta(o8, "PROPUESTA", entrada={**ENTRADA, "cantidad": 40.0})
    v = informe_f(o8)
    h.chk("integracion_E_y_F_respetan_el_importe_por_orden", v["resultado_politica"]["resultado"] == "APROBADO"
          and v["payload"]["cantidad_aprobada"] * ENTRADA["limite"] <= 50.0, v["resultado_politica"])

    # ------------------------------------------------------------------ regresiones de la revisión independiente de T-22
    from control_f import aplanar_informe
    pol150 = {**P, "importe_max_orden_eur": 150.0, "importe_max_dia_eur": 150.0}
    o = nuevo({"politica_f": pol150}); hasta(o, "AUTORIZADA"); hasta(o, "PROPUESTA", n=3)   # 110 € ya autorizados hoy
    inf = informe_f(o, "EXP-0003", 3)
    p = o.pantalla_aprobacion("EXP-0003", inf, AHORA, anular_veto={"motivo": "Oportunidad revisada a mano: anulo el veto de valor mínimo"})
    q = p["ok"] and p["pantalla"]["cantidad"]
    h.chk("r01_la_anulacion_tambien_la_acota_el_importe_del_dia", p["ok"] and 110.0 + q * 1.10 <= 150.0 + 1e-9, p)
    o = nuevo({"politica_f": pol150}); hasta(o, "PROPUESTA"); hasta(o, "PROPUESTA", n=3)
    assert autorizar_op(o, "EXP-0001", informe_f(o, "EXP-0001", 1), "2026-11-06T09:10:00+00:00")["ok"]
    atrasado = informe_f(o, "EXP-0003", 3, emitido_en="2026-11-06T09:05:00+00:00")
    r = autorizar_op(o, "EXP-0003", atrasado, "2026-11-06T09:15:00+00:00")
    h.chk("r02_un_informe_anterior_a_otra_autorizacion_no_vale_O10", r["codigo"] == "O-10" and "EXP-0001" in r["motivo"], r)
    o = nuevo(); hasta(o, "PROPUESTA")
    ayer = informe_f(o, cartera={"fecha_hora": "2026-11-06T23:30:00+00:00"}, emitido_en="2026-11-06T23:40:00+00:00", valid_until="2026-11-07T09:00:00+00:00")
    r = autorizar_op(o, "EXP-0001", ayer, "2026-11-07T00:05:00+00:00")
    h.chk("r02_un_informe_de_otro_dia_no_vale_O10", r["codigo"] == "O-10", r)
    o = nuevo()
    assert o.registrar_cartera({**CART, "fecha_hora": "2026-11-06T09:30:00+00:00", "perdida_dia_eur": 4000.0}, "G", "2026-11-06T09:30:00+00:00", cuenta="SIM-1")["ok"]
    from datetime import datetime, timedelta
    t0 = datetime.fromisoformat("2026-11-07T08:00:00+00:00")
    for i in range(205):
        t = (t0 + timedelta(minutes=i)).isoformat()
        assert o.registrar_cartera({**CART, "fecha_hora": t, "perdida_dia_eur": 1500.0}, "G", t, cuenta="SIM-1")["ok"]
    h.chk("r03_la_perdida_de_la_semana_no_se_pierde_al_podar_las_fotos", len(o.fotos) == 200
          and o._actividad(None, _dt("2026-11-07T12:00:00+00:00"))["perdida_semana_eur"] == 5500.0)
    o = nuevo(); hasta(o, "AUTORIZADA")
    r = o.orden_entrada("EXP-0001", "ORD-1", "ENVIADA", 0.0, "G", "2026-11-07T08:00:00+00:00")
    h.chk("r04_al_enviar_F_vuelve_a_mirar_fin_de_semana_y_precio_O06", r["codigo"] == "O-06" and "F-21" in r["reglas"] and "F-23" in r["reglas"], r)
    o = nuevo(); hasta(o, "AUTORIZADA")
    n = 0
    while n < 20 and o.orden_entrada("EXP-0001", f"ORD-{n}", "ENVIADA", 0.0, "G", AHORA)["ok"]:
        o.orden_entrada("EXP-0001", f"ORD-{n}", "RECHAZADA", 0.0, "G", AHORA)
        n += 1
    h.chk("r05_F17_cuenta_las_ordenes_enviadas_reintentos_incluidos", n == P["ordenes_max_hora"]
          and o._actividad("EXP-0002", _dt(AHORA))["ordenes_ultima_hora"] == n, n)
    r = f(sol={"cantidad": 5000.0}, cart={"posiciones": [{"instrumento": "EURGBP", "activo_base": "eur", "valor_eur": 29000.0}]},
          pol={**P, "concentracion_max_pct": 100.0, "exposicion_max_pct": 100.0})
    h.chk("r06_F15_y_F07_reconocen_el_activo_con_otra_grafia", regla(r, "F-15")[0]["resultado"] == "REDUCE" and abs(r["cantidad_aprobada"] - 1000.0 / 1.10) < 1e-5, r)
    o = nuevo(); o._ahora(AHORA)
    h.chk("r07_cotizar_con_instante_ilegible_no_lanza", cotizar_g(o, BrokerSimulado(1.0, {"EURUSD": 1.1}, AHORA), "EURUSD", "ayer")["codigo"] == "O-01")
    o = nuevo({"nivel_autonomia": {"TACTICA": "L2"}}); hasta(o, "PROPUESTA")
    inf = informe_f(o)
    o._degradar("TACTICA", "prueba", AHORA)
    h.chk("r08_una_degradacion_no_invalida_el_informe_de_F", o.nivel("TACTICA") == "L1" and autorizar_op(o, "EXP-0001", inf, AHORA)["ok"])

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO F T-22:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
