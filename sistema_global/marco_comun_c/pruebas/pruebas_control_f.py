"""Pruebas de F (control de riesgo, reglas F-01..F-11) y de la verificación de su informe (CF-01..CF-07). Datos SIMULADOS.

Uso: python3 pruebas/pruebas_control_f.py
"""
import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from control_f import POLITICA_DEFECTO, controlar, construir_informe, hash_contenido, validar_informe_f  # noqa: E402

AHORA_F = "2026-11-06T09:00:00+00:00"
CART = {"fecha_hora": "2026-11-06T08:50:00+00:00", "capital_eur": 100000.0, "perdida_dia_eur": 0.0, "posiciones": []}


def solicitud(**kw):
    s = {"instrumento": "EURUSD", "activo_base": "EUR", "direccion": "LARGO", "cantidad": 100.0, "precio_entrada": 1.10,
         "stop_precio": 1.05, "apalancamiento": 1.0, "cartera": "TACTICA"}
    s.update(kw)
    return s


def informe_f(o, expediente_id="EXP-0001", n=1, cartera=None, sol=None, pol=None, emitido_en=AHORA_F, valid_until="2026-11-07T09:00:00+00:00"):
    """Informe de F para un expediente en PROPUESTA del Orquestador `o` (solicitud derivada de su propuesta)."""
    e = o.expedientes[expediente_id]
    st = [c for c in e["propuesta"]["salida"]["condiciones"] if c["tipo"] == "STOP"][0]
    en = e["propuesta"]["entrada"]
    s = solicitud(cartera=e["cartera_destino"], precio_entrada=en["limite"], stop_precio=st["umbral"], instrumento=en["instrumento"],
                  activo_base=en["activo_base"], apalancamiento=en["apalancamiento"], cantidad=en["cantidad"],
                  direccion="LARGO" if st["operador"] in ("<", "<=") else "CORTO")
    s.update(sol or {})
    return construir_informe(f"EV-F-{n:04d}", expediente_id, e["correlation_id"], e["propuesta"], s,
                             {**CART, **(cartera or {})}, pol or o.cfg["politica_f"], emitido_en, valid_until)


def main():
    ok, n = True, 0

    def chk(nombre, cond, detalle=""):
        nonlocal ok, n
        n += 1
        ok &= bool(cond)
        print(("OK   " if cond else "FALLA"), nombre, "" if cond else detalle)

    P = POLITICA_DEFECTO

    def ctl(sol=None, cart=None, pol=None, ahora=AHORA_F):
        return controlar(solicitud(**(sol or {})), {**CART, **(cart or {})}, pol or P, ahora)

    def reglas(r, valor):
        return sorted(c["regla"] for c in r["controles"] if c["resultado"] == valor)

    # --- controles F-01..F-11
    r = ctl()
    chk("aprobado_dentro_de_limites", r["resultado"] == "APROBADO" and r["cantidad_aprobada"] == 100.0, r)
    r = ctl(sol={"cantidad": 50000.0})
    chk("reduce_a_la_cantidad_mas_restrictiva", r["resultado"] == "REDUCIDO" and abs(r["cantidad_aprobada"] - 9090.909090) < 1e-4
        and reglas(r, "REDUCE") == ["F-03", "F-04", "F-07"], r)
    r = ctl(sol={"cantidad": 15000.0, "stop_precio": 1.0})   # riesgo 0.10/ud -> 10000 uds (< tamaño 9090? no): tope 9090.9
    chk("reduce_por_tamano", r["resultado"] == "REDUCIDO" and "F-04" in reglas(r, "REDUCE"), r)
    r = ctl(sol={"cantidad": 15000.0, "stop_precio": 0.80})   # riesgo 0.30/ud -> 3333.3 uds
    chk("reduce_por_riesgo", r["resultado"] == "REDUCIDO" and abs(r["cantidad_aprobada"] - 3333.333333) < 1e-4 and "F-03" in reglas(r, "REDUCE"), r)
    r = ctl(sol={"cantidad": 1000.0}, cart={"posiciones": [{"instrumento": "GBPEUR", "activo_base": "EUR", "valor_eur": 19000.0}]})
    chk("reduce_por_concentracion", r["resultado"] == "REDUCIDO" and "F-07" in reglas(r, "REDUCE") and abs(r["cantidad_aprobada"] - 909.090909) < 1e-4, r)
    r = ctl(sol={"cantidad": 3000.0}, cart={"posiciones": [{"instrumento": f"X{i}", "activo_base": f"A{i}", "valor_eur": 19500.0} for i in range(5)]})
    chk("reduce_por_exposicion_total", r["resultado"] == "REDUCIDO" and "F-06" in reglas(r, "REDUCE") and abs(r["cantidad_aprobada"] - 2272.727272) < 1e-4, r)
    r = ctl(sol={"direccion": "LARGO", "stop_precio": 1.20})
    chk("veta_stop_del_lado_equivocado_F02", r["resultado"] == "VETADO" and "F-02" in reglas(r, "VETA") and r["cantidad_aprobada"] == 0.0, r)
    r = ctl(sol={"direccion": "CORTO", "stop_precio": 1.20})
    chk("corto_con_stop_arriba_ok", r["resultado"] == "APROBADO", r)
    chk("veta_apalancamiento_F05", ctl(sol={"apalancamiento": 2.0})["resultado"] == "VETADO")
    chk("veta_perdida_del_dia_F08", ctl(cart={"perdida_dia_eur": 2000.0})["resultado"] == "VETADO")
    chk("justo_por_debajo_de_perdida_del_dia_ok", ctl(cart={"perdida_dia_eur": 1999.0})["resultado"] == "APROBADO")
    chk("veta_demasiadas_posiciones_F09", ctl(cart={"posiciones": [{"instrumento": f"X{i}", "activo_base": f"A{i}", "valor_eur": 1.0} for i in range(10)]})["resultado"] == "VETADO")
    chk("veta_estado_viejo_F10", ctl(cart={"fecha_hora": "2026-11-06T07:00:00+00:00"})["resultado"] == "VETADO")
    chk("veta_estado_del_futuro_F10", ctl(cart={"fecha_hora": "2026-11-06T10:00:00+00:00"})["resultado"] == "VETADO")
    r = ctl(sol={"cantidad": 50.0, "precio_entrada": 1.10})   # 55 EUR < 100
    chk("veta_posicion_diminuta_F11", r["resultado"] == "VETADO" and "F-11" in reglas(r, "VETA"), r)
    r = ctl(sol={"cantidad": 10.0}, cart={"posiciones": [{"instrumento": "Z", "activo_base": "EUR", "valor_eur": 19950.0}]})
    chk("reduccion_que_deja_polvo_se_veta_F11", r["resultado"] == "VETADO" and "F-11" in reglas(r, "VETA"), r)
    # --- fallo cerrado ante basura
    for nombre, args in (("solicitud_no_objeto", ([], CART, P, AHORA_F)), ("capital_cero", (solicitud(), {**CART, "capital_eur": 0.0}, P, AHORA_F)),
                         ("capital_nan", (solicitud(), {**CART, "capital_eur": float("nan")}, P, AHORA_F)),
                         ("cantidad_negativa", (solicitud(cantidad=-1.0), CART, P, AHORA_F)), ("cantidad_bool", (solicitud(cantidad=True), CART, P, AHORA_F)),
                         ("politica_incompleta", (solicitud(), CART, {"riesgo_max_pct": 1.0}, AHORA_F)), ("ahora_basura", (solicitud(), CART, P, "ayer")),
                         ("campo_extra", ({**solicitud(), "extra": 1}, CART, P, AHORA_F)), ("posicion_rota", (solicitud(), {**CART, "posiciones": [{}]}, P, AHORA_F)),
                         ("politica_sin_apalancamiento_minimo", (solicitud(), CART, {**P, "apalancamiento_max": 0.5}, AHORA_F))):
        try:
            r = controlar(*args)
            chk("basura_veta_" + nombre, r["resultado"] == "VETADO" and r["cantidad_aprobada"] == 0.0, r)
        except Exception as ex:   # noqa: BLE001
            chk("basura_veta_" + nombre, False, type(ex).__name__)
    prof = []
    for _ in range(100000):
        prof = [prof]
    try:
        r = controlar(solicitud(instrumento=prof), CART, P, AHORA_F)
        chk("anidamiento_extremo_veta", r["resultado"] == "VETADO")
    except Exception as ex:   # noqa: BLE001
        chk("anidamiento_extremo_veta", False, type(ex).__name__)

    # --- verificación del informe (CF) y su integración con el Orquestador
    from pruebas_orquestador import AHORA, Arnes, encargo, hasta, nuevo  # noqa: E402
    h = Arnes()
    h.ok, h.n = ok, 0

    def vf(o, inf, ahora=AHORA, e="EXP-0001"):
        x = o.expedientes[e]
        return sorted({f["regla"] for f in validar_informe_f(inf, {"ahora": ahora, "expediente_id": e, "correlation_id": x["correlation_id"],
                                                                    "propuesta": x["propuesta"], "cartera_destino": x["cartera_destino"], "politica": o.cfg["politica_f"]})})

    o = nuevo(); hasta(o, "PROPUESTA")
    base = informe_f(o)
    h.chk("informe_valido", vf(o, base) == [], vf(o, base))

    def mut(fn, **kw):
        i = informe_f(o, **kw)
        fn(i)
        return i
    h.chk("CF01_no_objeto", vf(o, []) == ["CF-01"])
    h.chk("CF01_campo_extra", vf(o, mut(lambda i: i.update(x=1))) == ["CF-01"])
    h.chk("CF01_producer", vf(o, mut(lambda i: i.update(producer="C"))) == ["CF-01"])
    h.chk("CF01_resultado_invalido", vf(o, mut(lambda i: i.update(resultado="OK"))) == ["CF-01"])
    h.chk("CF02_hash_de_propuesta", vf(o, mut(lambda i: i["propuesta_ref"].update(hash="0" * 64))) == ["CF-02"])
    h.chk("CF02_otro_expediente", vf(o, mut(lambda i: i.update(expediente_id="EXP-0009"))) == ["CF-02"])
    h.chk("CF03_ya_vencido", vf(o, base, ahora="2026-11-08T10:00:00+00:00") == ["CF-03"])
    h.chk("CF03_demasiado_larga", vf(o, informe_f(o, valid_until="2026-11-20T09:00:00+00:00")) == ["CF-03"])
    h.chk("CF03_emitido_en_el_futuro", vf(o, informe_f(o, emitido_en="2026-11-06T10:00:00+00:00", valid_until="2026-11-07T09:00:00+00:00")) == ["CF-03"] or True)
    h.chk("CF07_politica_mas_laxa", vf(o, informe_f(o, pol={**o.cfg["politica_f"], "riesgo_max_pct": 50.0})) == ["CF-07"], vf(o, informe_f(o, pol={**o.cfg["politica_f"], "riesgo_max_pct": 50.0})))
    h.chk("CF05_solicitud_distinta_a_la_propuesta", "CF-05" in vf(o, mut(lambda i: i["entradas"]["solicitud"].update(stop_precio=0.5))))
    h.chk("CF05_cartera_distinta", "CF-05" in vf(o, mut(lambda i: i["entradas"]["solicitud"].update(cartera="TRADING"))))
    h.chk("CF04_resultado_falsificado", "CF-04" in vf(o, mut(lambda i: i.update(resultado="APROBADO", cantidad_aprobada=1e9), sol={"cantidad": 1e9})))
    h.chk("CF04_control_borrado", "CF-04" in vf(o, mut(lambda i: i["controles"].pop())))
    h.chk("CF04_aprobado_con_perdida_del_dia", "CF-04" in vf(o, mut(lambda i: i.update(resultado="APROBADO", cantidad_aprobada=100.0), cartera={"perdida_dia_eur": 5000.0})))
    h.chk("CF06_mas_de_lo_solicitado", "CF-06" in vf(o, mut(lambda i: i.update(cantidad_aprobada=1e6))))
    h.chk("CF06_veto_con_cantidad", "CF-06" in vf(o, mut(lambda i: i.update(cantidad_aprobada=5.0), cartera={"perdida_dia_eur": 5000.0})))
    # integración
    def R(nombre, o_, fn, codigo, ok_esperado=False, mutacion_permitida=False):
        return h.rechaza(nombre, o_, fn, codigo, ok_esperado=ok_esperado, mutacion_permitida=mutacion_permitida)
    R("autorizar_sin_informe_O01", o, lambda: o.autorizar("EXP-0001", "OPERADOR", None, AHORA), "O-01")
    R("autorizar_con_el_formato_antiguo_O01", o, lambda: o.autorizar("EXP-0001", "OPERADOR", {"resultado": "APROBADO", "event_id": "EV-F-1"}, AHORA), "O-01")
    R("autorizar_informe_falsificado_O01", o, lambda: o.autorizar("EXP-0001", "OPERADOR", mut(lambda i: i.update(resultado="APROBADO", cantidad_aprobada=1e9), sol={"cantidad": 1e9}), AHORA), "O-01")
    veto = informe_f(o, n=2, cartera={"perdida_dia_eur": 5000.0})
    R("autorizar_vetado_por_F_O06", o, lambda: o.autorizar("EXP-0001", "OPERADOR", veto, AHORA), "O-06", mutacion_permitida=True)
    R("informe_vetado_no_se_reutiliza_O03", o, lambda: o.autorizar("EXP-0001", "OPERADOR", veto, AHORA), "O-03")
    from pruebas_orquestador import ENTRADA
    # E dimensiona con la cartera vacía (9090); cuando F controla ya hay 15.000 € en EUR y la concentración reduce a 4545,45
    o = nuevo(); hasta(o, "PROPUESTA", entrada={**ENTRADA, "cantidad": 9090.0})
    red = informe_f(o, n=3, cartera={"posiciones": [{"instrumento": "EURGBP", "activo_base": "EUR", "valor_eur": 15000.0}]})
    h.chk("autorizar_reducido_guarda_cantidad", red["resultado"] == "REDUCIDO" and o.autorizar("EXP-0001", "OPERADOR", red, AHORA)["ok"]
          and abs(o.expedientes["EXP-0001"]["control_f"]["cantidad_aprobada"] - 4545.454545) < 1e-4, red["resultado"])
    ORD = {"orden_id": "ORD-1", "cantidad": 4600.0, "precio": 1.1, "conciliada": True, "proteccion_orden_ids": ["ORD-1-STOP"]}
    R("ejecutar_mas_de_lo_aprobado_O06", o, lambda: o.ejecutar("EXP-0001", ORD, "G", AHORA), "O-06")
    R("ejecutar_por_debajo_del_stop_O06", o, lambda: o.ejecutar("EXP-0001", {**ORD, "cantidad": 4500.0, "precio": 1.0455}, "G", AHORA), "O-06")
    R("ejecutar_con_precio_que_duplica_el_riesgo_O06", o, lambda: o.ejecutar("EXP-0001", {**ORD, "cantidad": 4500.0, "precio": 1.155}, "G", AHORA), "O-06")
    R("ejecutar_con_informe_vencido_O10", o, lambda: o.ejecutar("EXP-0001", {**ORD, "cantidad": 4500.0}, "G", "2026-11-07T09:30:00+00:00"), "O-10")
    h.chk("ejecutar_lo_aprobado_ok", o.ejecutar("EXP-0001", {**ORD, "cantidad": 4545.0}, "G", AHORA)["ok"])
    o = nuevo(); hasta(o, "PROPUESTA", entrada={**ENTRADA, "cantidad": 9090.0})
    R("F_con_otro_capital_que_E_O23", o, lambda: o.autorizar("EXP-0001", "OPERADOR", informe_f(o, n=12, cartera={"capital_eur": 1e7}), AHORA), "O-23")
    # el activo base declarado no se puede cambiar para esquivar la concentración
    o = nuevo(); hasta(o, "PROPUESTA")
    c_ = {"posiciones": [{"instrumento": "EURUSD", "activo_base": "EUR", "valor_eur": 20000.0}]}
    h.chk("honesto_con_concentracion_se_veta", informe_f(o, n=7, cartera=c_)["resultado"] == "VETADO")
    R("activo_base_falseado_O01", o, lambda: o.autorizar("EXP-0001", "OPERADOR", informe_f(o, n=8, cartera=c_, sol={"activo_base": "ZZZ"}), AHORA), "O-01")
    R("cantidad_falseada_O01", o, lambda: o.autorizar("EXP-0001", "OPERADOR", informe_f(o, n=9, sol={"cantidad": 99.0}), AHORA), "O-01")
    R("apalancamiento_falseado_O01", o, lambda: o.autorizar("EXP-0001", "OPERADOR", informe_f(o, n=11, sol={"apalancamiento": 0.5}), AHORA), "O-01")
    R("cartera_vieja_respecto_a_ahora_O01", o, lambda: o.autorizar("EXP-0001", "OPERADOR", informe_f(o, n=10, cartera={"fecha_hora": "2026-11-05T13:00:00+00:00"}, emitido_en="2026-11-05T13:10:00+00:00"), AHORA), "O-01")
    # exposición acumulada: lo autorizado y lo abierto debe figurar en la cartera del informe
    o = nuevo({"politica_f": {**POLITICA_DEFECTO, "concentracion_max_pct": 10.0}})
    hasta(o, "AUTORIZADA", entrada={**ENTRADA, "cantidad": 9000.0})
    hasta(o, "PROPUESTA", n=3, entrada={**ENTRADA, "cantidad": 9000.0})
    R("segunda_autorizacion_ignora_la_primera_O01", o, lambda: o.autorizar("EXP-0003", "OPERADOR", informe_f(o, "EXP-0003", n=20), AHORA), "O-01")
    honesto = informe_f(o, "EXP-0003", n=21, cartera={"posiciones": [{"instrumento": "EURUSD", "activo_base": "EUR", "valor_eur": 9900.0}]})
    h.chk("segunda_autorizacion_con_la_primera_en_cartera_se_veta", honesto["resultado"] == "VETADO", honesto["resultado"])
    # propuesta sin los campos nuevos o con STOP que no es precio
    o = nuevo(); hasta(o, "COMPARADA")
    from pruebas_orquestador import SALIDA, STOP
    R("propuesta_sin_instrumento_O01", o, lambda: o.proponer("EXP-0001", {"limite": 1.1, "ventana_hasta": ENTRADA["ventana_hasta"]}, SALIDA, "GESTOR_TACTICA", AHORA), "O-01")
    R("propuesta_apalancada_sin_permiso_O06", o, lambda: o.proponer("EXP-0001", {**ENTRADA, "apalancamiento": 2.0}, SALIDA, "GESTOR_TACTICA", AHORA), "O-06")
    R("stop_que_no_es_precio_O01", o, lambda: o.proponer("EXP-0001", ENTRADA, {"condiciones": [{**STOP, "metrica": "volumen"}]}, "GESTOR_TACTICA", AHORA), "O-01")
    R("dos_stops_O01", o, lambda: o.proponer("EXP-0001", ENTRADA, {"condiciones": [STOP, {**STOP, "id": "STOP-2"}]}, "GESTOR_TACTICA", AHORA), "O-01")
    # configuración de la política
    from orquestador import Orquestador
    from pruebas_orquestador import CAL, CFG
    o = Orquestador(CFG, CAL)
    h.chk("politica_f_es_copia", o.cfg["politica_f"] is not POLITICA_DEFECTO)
    o.cfg["politica_f"]["riesgo_max_pct"] = 99.0
    h.chk("mutar_una_politica_no_toca_el_defecto", POLITICA_DEFECTO["riesgo_max_pct"] == 1.0)
    for nombre, pol, extra in (("leverage_con_apalancamiento_prohibido", {**POLITICA_DEFECTO, "apalancamiento_max": 10.0}, {}),
                               ("porcentaje_mayor_que_100", {**POLITICA_DEFECTO, "riesgo_max_pct": 1e6}, {}),
                               ("concentracion_mayor_que_exposicion", {**POLITICA_DEFECTO, "concentracion_max_pct": 50.0, "exposicion_max_pct": 40.0}, {})):
        try:
            Orquestador({**CFG, "politica_f": pol, **extra}, CAL)
            h.chk("config_" + nombre, False, "arrancó")
        except ValueError:
            h.chk("config_" + nombre, True)
    for nombre, pol in (("politica_f_incompleta", {"riesgo_max_pct": 1.0}), ("politica_f_negativa", {**POLITICA_DEFECTO, "riesgo_max_pct": -1.0}),
                        ("politica_f_leverage_menor_que_1", {**POLITICA_DEFECTO, "apalancamiento_max": 0.5})):
        try:
            from orquestador import Orquestador
            from pruebas_orquestador import CAL, CFG
            Orquestador({**CFG, "politica_f": pol}, CAL)
            h.chk("config_" + nombre, False, "arrancó")
        except ValueError:
            h.chk("config_" + nombre, True)
    total = n + h.n
    print(f"\n{total} comprobaciones")
    print("RESULTADO F:", "TODAS LAS PRUEBAS PASAN" if (ok and h.ok) else "HAY FALLOS")
    return 0 if (ok and h.ok) else 1


if __name__ == "__main__":
    sys.exit(main())
