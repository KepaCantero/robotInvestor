"""Pruebas de T-11 (la cartera de E y F es una foto que G toma del intermediario) y T-10 (conversión a euros en F)."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validador"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from control_f import POLITICA_DEFECTO, construir_informe, controlar, divisa_cotizada  # noqa: E402
from dimensionado import dimensionar  # noqa: E402
from ejecucion_g import BrokerSimulado, cartera_para_f, foto_cartera  # noqa: E402
from pruebas_control_f import solicitud  # noqa: E402
from pruebas_orquestador import AHORA, CAL, CFG, ENTRADA, SALIDA, Arnes, autorizar_op, dim, hasta, nuevo  # noqa: E402

HORA = "2026-11-06T08:50:00+00:00"
EID = "EXP-0001"


def cart(**kw):
    c = {"fecha_hora": HORA, "capital_eur": 100000.0, "perdida_dia_eur": 0.0, "posiciones": [], "tipos_cambio_eur": {"USD": 1 / 1.10}}
    c.update(kw)
    return c


def tope(r, regla):
    return next(x["limite"] for x in r["controles"] if x["regla"] == regla)


def main():
    h = Arnes()
    # ---------------------------------------------------------------- T-10: F valora en euros
    r = controlar(solicitud(cantidad=20000.0), cart(), POLITICA_DEFECTO, AHORA)
    h.chk("eurusd_el_tope_de_tamano_es_en_euros", abs(tope(r, "F-04") - 10000.0) < 1e-6 and abs(r["cantidad_aprobada"] - 10000.0) < 1e-5, r["controles"])
    h.chk("eurusd_el_riesgo_es_en_euros", abs(tope(r, "F-03") - 1000.0 / (0.05 / 1.10)) < 1e-6)
    jpy = solicitud(instrumento="USDJPY", activo_base="USD", divisa_cotizacion="JPY", precio_entrada=150.0, stop_precio=148.0, cantidad=1e6)
    r = controlar(jpy, cart(tipos_cambio_eur={"JPY": 0.006}), POLITICA_DEFECTO, AHORA)
    h.chk("usdjpy_sin_el_error_de_dos_ordenes_de_magnitud", abs(tope(r, "F-04") - 10000.0 / 0.9) < 1e-6 and abs(tope(r, "F-03") - 1000.0 / 0.012) < 1e-6, r["controles"])
    r = controlar(jpy, cart(), POLITICA_DEFECTO, AHORA)
    h.chk("sin_tipo_de_cambio_F12_veta", r["resultado"] == "VETADO" and any(x["regla"] == "F-12" and x["resultado"] == "VETA" for x in r["controles"]), r)
    r = controlar(solicitud(divisa_cotizacion="usd"), cart(), POLITICA_DEFECTO, AHORA)
    h.chk("divisa_mal_escrita_F01", r["resultado"] == "VETADO" and r["controles"][0]["regla"] == "F-01")
    r = controlar(solicitud(), cart(tipos_cambio_eur={"USD": -1.0}), POLITICA_DEFECTO, AHORA)
    h.chk("tipo_de_cambio_negativo_F01", r["resultado"] == "VETADO" and r["controles"][0]["regla"] == "F-01")
    r = controlar(solicitud(), {k: v for k, v in cart().items() if k != "tipos_cambio_eur"}, POLITICA_DEFECTO, AHORA)
    h.chk("cartera_sin_tipos_F01", r["resultado"] == "VETADO" and r["controles"][0]["regla"] == "F-01")
    r = controlar(solicitud(instrumento="EURGBP", divisa_cotizacion="EUR", precio_entrada=1.0, stop_precio=0.95, cantidad=1e6), cart(), POLITICA_DEFECTO, AHORA)
    h.chk("cotizado_en_euros_no_necesita_tipo", r["resultado"] == "REDUCIDO" and abs(tope(r, "F-04") - 10000.0) < 1e-6, r)
    sol_e = {k: v for k, v in solicitud().items() if k != "cantidad"}
    e = dimensionar(sol_e, cart(), POLITICA_DEFECTO, AHORA, paso=1.0)
    h.chk("E_tambien_en_euros", e["ok"] and e["cantidad"] == 10000.0 and abs(e["valor_eur"] - 10000.0) < 1e-6, e)
    e = dimensionar({**sol_e, "divisa_cotizacion": "JPY"}, cart(), POLITICA_DEFECTO, AHORA, paso=1.0)
    h.chk("E_sin_tipo_de_cambio_E03", e["codigo"] == "E-03", e)
    h.chk("divisa_de_un_par", divisa_cotizada("EUR/USD") == "USD" and divisa_cotizada("usdjpy") == "JPY")
    h.chk("divisa_desconocida_None", divisa_cotizada("SAN.MC") is None and divisa_cotizada("SAN.MC", {"SAN.MC": "EUR"}) == "EUR")
    # ---------------------------------------------------------------- G: la foto de cartera
    b = BrokerSimulado(100000.0, {"EURUSD": 1.10}, HORA)
    b.enviar({"orden_id": "X-1", "tipo": "MERCADO", "lado": "COMPRA", "instrumento": "EURUSD", "activo_base": "EUR", "cantidad": 100.0})
    f = cartera_para_f(b)
    h.chk("G_valora_las_posiciones_en_euros", abs(f["posiciones"][0]["valor_eur"] - 100.0) < 1e-9 and abs(f["tipos_cambio_eur"]["USD"] - 1 / 1.10) < 1e-12, f)
    b2 = BrokerSimulado(100000.0, {"GBPJPY": 190.0}, HORA)
    b2.enviar({"orden_id": "X-1", "tipo": "MERCADO", "lado": "COMPRA", "instrumento": "GBPJPY", "activo_base": "GBP", "cantidad": 10.0})
    try:
        cartera_para_f(b2); h.chk("sin_tipo_para_valorar_una_posicion_falla", False)
    except ValueError:
        h.chk("sin_tipo_para_valorar_una_posicion_falla", True)
    o = nuevo()
    h.chk("foto_sin_tipos_no_se_registra", foto_cartera(o, b2, AHORA) is None and o.fotos == {})
    b.caido = True
    h.chk("foto_con_el_intermediario_caido_no_se_registra", foto_cartera(o, b, AHORA) is None)
    b.caido = False
    ft = foto_cartera(o, b, AHORA)
    h.chk("foto_registrada", ft is not None and len(o.fotos) == 1)
    h.chk("registrar_solo_G_O05", o.registrar_cartera(cart(), "H", AHORA, cuenta="SIM-1")["codigo"] == "O-05")
    h.chk("foto_mal_formada_O01", o.registrar_cartera({**cart(), "extra": 1}, "G", AHORA, cuenta="SIM-1")["codigo"] == "O-01")
    h.chk("foto_del_futuro_O10", o.registrar_cartera(cart(fecha_hora="2026-11-06T09:30:00+00:00"), "G", AHORA, cuenta="SIM-1")["codigo"] == "O-10")
    h.chk("foto_vieja_O10", o.registrar_cartera(cart(fecha_hora="2026-11-06T07:00:00+00:00"), "G", AHORA, cuenta="SIM-1")["codigo"] == "O-10")
    for i in range(205):
        o.registrar_cartera(cart(capital_eur=1000.0 + i), "G", AHORA, cuenta="SIM-1")
    h.chk("solo_se_guardan_las_fotos_recientes", len(o.fotos) == 200)
    # ---------------------------------------------------------------- el Orquestador exige la foto
    o = nuevo(); hasta(o, "COMPARADA")
    d = dim(o)
    d["cartera"] = {**d["cartera"], "capital_eur": 1e7}   # cartera inventada por quien llama: no la registró G
    r = o.proponer(EID, ENTRADA, SALIDA, "GESTOR_TACTICA", AHORA, d)
    h.chk("E_con_cartera_no_registrada_O29", r["codigo"] == "O-29", r)
    o = nuevo(); hasta(o, "PROPUESTA")
    e_ = o.expedientes[EID]
    sol = {**solicitud(), "cantidad": e_["propuesta"]["entrada"]["cantidad"]}
    c55 = cart(tipos_cambio_eur={"USD": 1.0}, fecha_hora="2026-11-06T08:55:00+00:00")   # foto que G no ha registrado
    inf = construir_informe("EV-F-0009", EID, e_["correlation_id"], e_["propuesta"], sol, c55,
                            o.cfg["politica_f"], AHORA, "2026-11-07T09:00:00+00:00")
    r = autorizar_op(o, EID, inf)
    h.chk("F_con_cartera_no_registrada_O29", r["codigo"] == "O-29", r)
    o.registrar_cartera(c55, "G", AHORA, cuenta="SIM-1")
    r = autorizar_op(o, EID, inf)
    h.chk("registrada_por_G_se_autoriza", r["ok"], r)
    o = nuevo(); hasta(o, "PROPUESTA")
    e_ = o.expedientes[EID]
    inf = construir_informe("EV-F-0010", EID, e_["correlation_id"], e_["propuesta"], {**sol, "divisa_cotizacion": "EUR"},
                            cart(tipos_cambio_eur={"USD": 1.0}), o.cfg["politica_f"], AHORA, "2026-11-07T09:00:00+00:00")
    o.registrar_cartera(cart(tipos_cambio_eur={"USD": 1.0}), "G", AHORA, cuenta="SIM-1")
    r = autorizar_op(o, EID, inf)
    h.chk("informe_con_otra_divisa_CF05", r["codigo"] == "O-01" and "CF-05" in r.get("reglas", []), r)
    # pantalla en euros con tipos reales
    o = nuevo(); hasta(o, "PROPUESTA")
    e_ = o.expedientes[EID]
    cr = cart()
    inf = construir_informe("EV-F-0011", EID, e_["correlation_id"], e_["propuesta"], {**sol, "cantidad": e_["propuesta"]["entrada"]["cantidad"]}, cr,
                            o.cfg["politica_f"], AHORA, "2026-11-07T09:00:00+00:00")
    o.registrar_cartera(cr, "G", AHORA, cuenta="SIM-1")
    # E se calculó con tipo neutro y F con tipo real: capitales iguales, así que se acepta; la pantalla muestra euros
    p = o.pantalla_aprobacion(EID, inf, AHORA)
    h.chk("pantalla_en_euros", p["ok"] and p["pantalla"]["unidad_importe"] == "EUR" and abs(p["pantalla"]["importe"] - 100.0) < 0.006
          and p["pantalla"]["divisa_cotizacion"] == "USD", p)
    # configuración
    from orquestador import Orquestador
    try:
        Orquestador({**CFG, "divisas_cotizacion": {"SAN.MC": "eur"}}, CAL); h.chk("config_divisa_mal_escrita_se_rechaza", False)
    except ValueError:
        h.chk("config_divisa_mal_escrita_se_rechaza", True)
    o = nuevo({"divisas_cotizacion": {"SAN.MC": "EUR"}})
    h.chk("divisa_configurada", o.divisa("SAN.MC") == "EUR" and o.divisa("EURUSD") == "USD" and o.divisa("XYZ") is None)
    o = nuevo(); hasta(o, "COMPARADA")
    r = o.proponer(EID, {**ENTRADA, "instrumento": "SAN.MC"}, SALIDA, "GESTOR_TACTICA", AHORA, dim(o))
    h.chk("instrumento_sin_divisa_conocida_no_se_propone", r["codigo"] == "O-01" and "divisa" in r["motivo"], r)
    # ---------------------------------------------------------------- revisión independiente
    o = nuevo()
    h.chk("tipo_absurdo_no_se_registra_O29", o.registrar_cartera(cart(tipos_cambio_eur={"USD": 1e-9}), "G", AHORA, cuenta="SIM-1")["codigo"] == "O-29")
    h.chk("tipo_sin_rango_no_se_registra_O29", o.registrar_cartera(cart(tipos_cambio_eur={"XAU": 3000.0}), "G", AHORA, cuenta="SIM-1")["codigo"] == "O-29")
    h.chk("foto_de_otra_cuenta_O29", o.registrar_cartera(cart(), "G", AHORA, cuenta="OTRA")["codigo"] == "O-29")
    h.chk("foto_sin_cuenta_O29", o.registrar_cartera(cart(), "G", AHORA)["codigo"] == "O-29")
    h.chk("posiciones_mal_formadas_O01", o.registrar_cartera(cart(posiciones=[1, "x"]), "G", AHORA, cuenta="SIM-1")["codigo"] == "O-01")
    assert o.registrar_cartera(cart(fecha_hora="2026-11-06T08:59:00+00:00"), "G", AHORA, cuenta="SIM-1")["ok"]
    h.chk("foto_anterior_a_la_ultima_O10", o.registrar_cartera(cart(), "G", AHORA, cuenta="SIM-1")["codigo"] == "O-10")
    # solo vale la última foto: una vieja sin la pérdida del día ya no sirve
    o = nuevo(); hasta(o, "PROPUESTA")
    e_ = o.expedientes[EID]
    vieja = cart(tipos_cambio_eur={"USD": 1.0}, fecha_hora="2026-11-06T08:52:00+00:00")
    nueva = cart(tipos_cambio_eur={"USD": 1.0}, fecha_hora="2026-11-06T08:58:00+00:00", perdida_dia_eur=5000.0)
    o.registrar_cartera(vieja, "G", AHORA, cuenta="SIM-1"); o.registrar_cartera(nueva, "G", AHORA, cuenta="SIM-1")
    inf = construir_informe("EV-F-0030", EID, e_["correlation_id"], e_["propuesta"], sol, vieja, o.cfg["politica_f"], AHORA, "2026-11-07T09:00:00+00:00")
    h.chk("una_foto_que_no_es_la_ultima_O29", autorizar_op(o, EID, inf)["codigo"] == "O-29")
    # el tipo de un par con el euro debe cuadrar con su precio
    o = nuevo(); hasta(o, "COMPARADA")
    d = dim(o)
    r = o.registrar_cartera(cart(tipos_cambio_eur={"USD": 1.35}, fecha_hora="2026-11-06T08:55:00+00:00"), "G", AHORA, cuenta="SIM-1")   # en rango, pero 1,35 x 1,10 = 1,49
    h.chk("tipo_que_no_cuadra_con_K_no_se_registra_O29", r["codigo"] == "O-29" and "K" in r["motivo"], r)   # T-42: ya al registrar la foto
    o2 = nuevo({"tolerancia_tipo_k_rel": 0.5}); hasta(o2, "COMPARADA")   # sin el contraste de K, lo para la propuesta
    d2 = dim(o2)
    assert o2.registrar_cartera(cart(tipos_cambio_eur={"USD": 1.35}, fecha_hora="2026-11-06T08:55:00+00:00"), "G", AHORA, cuenta="SIM-1")["ok"]
    d2 = {**d2, "cartera": o2.cartera_f()}
    h.chk("tipo_que_no_cuadra_con_el_par_O29", o2.proponer(EID, ENTRADA, SALIDA, "GESTOR_TACTICA", AHORA, d2)["codigo"] == "O-29")
    h.chk("seis_letras_que_no_son_un_par", divisa_cotizada("ABCJPY") is None and divisa_cotizada("EUREKA") is None and divisa_cotizada("EUR-USD") == "USD")
    # conversión en cada tope (que las pruebas con tipo neutro no veían)
    c5 = cart(tipos_cambio_eur={"USD": 0.5}, posiciones=[{"instrumento": "EURGBP", "activo_base": "EUR", "valor_eur": 15000.0}])
    r = controlar(solicitud(cantidad=1e6), c5, POLITICA_DEFECTO, AHORA)
    h.chk("F06_y_F07_en_euros", abs(tope(r, "F-07") - 5000.0 / 0.55) < 1e-6 and abs(tope(r, "F-06") - 85000.0 / 0.55) < 1e-6, r["controles"])
    r = controlar(solicitud(cantidad=150.0), cart(tipos_cambio_eur={"USD": 0.5}), POLITICA_DEFECTO, AHORA)
    h.chk("F11_valor_minimo_en_euros", r["resultado"] == "VETADO" and any(x["regla"] == "F-11" and x["resultado"] == "VETA" for x in r["controles"]), r["controles"])
    e = dimensionar(sol_e, cart(tipos_cambio_eur={"USD": 0.5}), POLITICA_DEFECTO, AHORA, riesgo_objetivo_pct=0.1, paso=1.0)
    h.chk("E_riesgo_objetivo_en_euros", e["ok"] and e["cantidad"] == 4000.0 and abs(e["riesgo_eur"] - 100.0) < 1e-6, e)
    o = nuevo(); hasta(o, "PROPUESTA")
    e_ = o.expedientes[EID]
    o.registrar_cartera(cr, "G", AHORA, cuenta="SIM-1")
    inf = construir_informe("EV-F-0031", EID, e_["correlation_id"], e_["propuesta"], {**sol, "cantidad": e_["propuesta"]["entrada"]["cantidad"]}, cr,
                            o.cfg["politica_f"], AHORA, "2026-11-07T09:00:00+00:00")
    p = o.pantalla_aprobacion(EID, inf, AHORA)["pantalla"]
    h.chk("pantalla_riesgo_en_euros", abs(p["riesgo"] - round(100.0 * 0.05 / 1.10, 2)) < 1e-9, p)
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO CARTERA:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
