"""Pruebas de la vía de acceso y la fecha de revisión ligadas a la propuesta (T-35). Datos SIMULADOS.

Comprueba: la propuesta declara la vía de acceso del sobre (O-21 si es otra: un futuro analizado no se opera como
contado) y una fecha de revisión futura que no pasa de la del sobre; la posición las guarda en su estado de control;
G envía la vía con la orden; la pantalla de aprobación las muestra; H pone la posición EN_REVISION al llegar la fecha
(H-14) y el operador la confirma fijando la siguiente.

Uso: python3 pruebas/pruebas_revision.py
"""
import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from ejecucion_g import cerrar, conciliar, ejecutar, reducir  # noqa: E402
from vigilancia import vigilar  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_ejecucion_g import autorizado  # noqa: E402
from pruebas_orquestador import AHORA, ENTRADA, INV, OBJ, SALIDA, STOP, Arnes, dim, elegir_si_hace_falta, hasta, nuevo  # noqa: E402

EID, PID = "EXP-0001", "POS-EXP-0001"
VIA = "Futuro de divisas, vencimiento trimestral"
SAL_PRONTO = {"condiciones": [STOP, OBJ, INV], "fecha": "2026-11-07"}   # revisión al día siguiente de AHORA
D1 = "2026-11-07T09:00:00+00:00"
D1B = "2026-11-07T09:05:00+00:00"
D2 = "2026-11-08T09:00:00+00:00"


def datos(precio, hora):
    return {"EURUSD": {"precio": precio, "hora": hora}}


def proponer(entrada=None, salida=None):
    o = nuevo()
    hasta(o, "COMPARADA", salida=salida if salida and isinstance(salida, dict) and "condiciones" in salida else None)
    elegir_si_hace_falta(o, EID)
    ent = entrada if entrada is not None else ENTRADA
    sal = salida if salida is not None else SALIDA
    try:
        d = dim(o, EID, None, None)
    except Exception:   # noqa: BLE001
        d = None
    return o, o.proponer(EID, ent, sal, "GESTOR_TACTICA", AHORA, d)


def abierta(salida=None):
    o, b = autorizado(salida=salida)
    r = ejecutar(o, EID, b, AHORA)
    assert r["ok"], r
    return o, b


def main():
    h = Arnes()
    # ------------------------------------------------------------ vía de acceso en la propuesta
    o, r = proponer()
    h.chk("propuesta_con_la_via_del_sobre", r["ok"] and o.expedientes[EID]["propuesta"]["entrada"]["via_acceso"] == VIA, r)
    for nombre, via, codigo in (("contado_en_vez_de_futuro", "Contado (spot) en intermediario", "O-21"),
                                ("etf_en_vez_de_futuro", "ETF cotizado en bolsa europea", "O-21"),
                                ("sin_via", None, "O-01"), ("via_vacia", "   ", "O-01"), ("via_no_texto", 7, "O-01"),
                                ("via_enorme_distinta", "x" * 201, "O-21")):
        ent = {**ENTRADA, "via_acceso": via}
        if via is None:
            ent.pop("via_acceso")
        o, r = proponer(entrada=ent)
        h.chk(f"via_{nombre}_{codigo.replace('-', '')}", r["codigo"] == codigo and o.expedientes[EID]["estado"] == "COMPARADA", r)
    o, r = proponer(entrada={**ENTRADA, "via_acceso": "futuro de divisas,   VENCIMIENTO trimestral"})
    h.chk("via_sin_distinguir_mayusculas_ni_espacios", r["ok"], r)

    # ------------------------------------------------------------ fecha de revisión en la propuesta
    for nombre, fecha, codigo in (("sin_fecha", None, "O-01"), ("formato_ajeno", "05/12/2026", "O-01"), ("fecha_imposible", "2026-02-30", "O-01"),
                                  ("no_texto", 20261205, "O-01"), ("hoy", "2026-11-06", "O-10"), ("pasada", "2026-11-01", "O-10"),
                                  ("despues_del_sobre", "2026-12-06", "O-21")):
        sal = {**SALIDA, "fecha": fecha}
        if fecha is None:
            sal.pop("fecha")
        o, r = proponer(salida=sal)
        h.chk(f"fecha_{nombre}_{codigo.replace('-', '')}", r["codigo"] == codigo and o.expedientes[EID]["estado"] == "COMPARADA", r)
    o, r = proponer(salida={**SALIDA, "fecha": "2026-12-05"})
    h.chk("fecha_igual_a_la_del_sobre_vale", r["ok"], r)
    o, r = proponer(salida={**SALIDA, "fecha": "2026-11-20"})
    h.chk("fecha_mas_prudente_vale", r["ok"], r)

    # ------------------------------------------------------------ pantalla, orden de G y posición
    o, b = autorizado()
    p = o.pantallas.get(EID) or {}
    h.chk("la_pantalla_muestra_via_y_fecha", p.get("via_acceso") == VIA and p.get("fecha_revision") == "2026-12-05", p)
    r = ejecutar(o, EID, b, AHORA)
    orden = b.consultar("ORD-EXP-0001-E-1")
    h.chk("G_envia_la_via_con_la_orden", r["ok"] and orden["via_acceso"] == VIA, orden)
    pos = o.posiciones[PID]
    h.chk("la_posicion_guarda_via_y_fecha", pos["via_acceso"] == VIA and pos["fecha_revision"] == "2026-12-05" and o.integridad() == [], pos)
    for campo, valor in (("via_acceso", "Contado"), ("fecha_revision", "2027-12-31")):
        o2, b2 = abierta()
        o2.posiciones[PID][campo] = valor
        h.chk(f"alterar_{campo}_de_la_posicion_se_detecta", o2.integridad() == ["POS:" + PID]
              and vigilar(o2, b2, datos(1.10, "2026-11-06T09:05:00+00:00"), "2026-11-06T09:05:00+00:00")["acciones"][0]["regla"] == "H-13")

    # ------------------------------------------------------------ H-14: llega la fecha de revisión
    o, b = abierta(salida=SAL_PRONTO)
    r = vigilar(o, b, datos(1.10, "2026-11-06T23:00:00+00:00"), "2026-11-06T23:00:00+00:00")
    h.chk("antes_de_la_fecha_nada", r["acciones"] == [] and o.posiciones[PID]["estado"] == "ABIERTA", r)
    antes = copy.deepcopy(b.ordenes)
    r = vigilar(o, b, datos(1.10, D1), D1)
    pos = o.posiciones[PID]
    h.chk("H14_llega_la_fecha_pasa_a_EN_REVISION", [a["regla"] for a in r["acciones"]] == ["H-14"] and r["acciones"][0]["ok"] and pos["estado"] == "EN_REVISION"
          and b.ordenes == antes and any(x["texto"].startswith("REVISIÓN: llegó la fecha de revisión 2026-11-07") for x in pos["propuestas"]), r)
    r = vigilar(o, b, datos(1.10, D1B), D1B)
    h.chk("H14_no_se_repite", r["acciones"] == [] and len([x for x in o.posiciones[PID]["propuestas"] if x["texto"].startswith("REVISIÓN")]) == 1, r)
    h.chk("en_revision_concilia_limpio", conciliar(o, b, D1B)["ok"])
    # el operador confirma: exige fecha nueva y futura
    h.rechaza("confirmar_sin_fecha_nueva_O15", o, lambda: o.posicion_transicion(PID, "ABIERTA", "OPERADOR", D1B, motivo="la tesis sigue"), "O-15")
    h.rechaza("confirmar_con_fecha_pasada_O10", o, lambda: o.posicion_transicion(PID, "ABIERTA", "OPERADOR", D1B, motivo="la tesis sigue", fecha_revision="2026-11-07"), "O-10")
    h.rechaza("confirmar_con_fecha_mal_escrita_O01", o, lambda: o.posicion_transicion(PID, "ABIERTA", "OPERADOR", D1B, motivo="la tesis sigue", fecha_revision="mañana"), "O-01")
    h.rechaza("confirmar_con_fecha_imposible_O01", o, lambda: o.posicion_transicion(PID, "ABIERTA", "OPERADOR", D1B, motivo="la tesis sigue", fecha_revision="2026-13-01"), "O-01")
    h.rechaza("confirmar_sin_motivo_O15", o, lambda: o.posicion_transicion(PID, "ABIERTA", "OPERADOR", D1B, fecha_revision="2026-12-01"), "O-15")
    h.rechaza("G_no_confirma_la_tesis_O05", o, lambda: o.posicion_transicion(PID, "ABIERTA", "G", D1B, motivo="x", fecha_revision="2026-12-01"), "O-05")
    r = o.posicion_transicion(PID, "ABIERTA", "OPERADOR", D1B, motivo="la tesis sigue en pie", fecha_revision="2026-11-08")
    h.chk("confirmar_con_fecha_nueva", r["ok"] and o.posiciones[PID]["estado"] == "ABIERTA" and o.posiciones[PID]["fecha_revision"] == "2026-11-08"
          and o.integridad() == [], r)
    r = vigilar(o, b, datos(1.10, "2026-11-07T10:00:00+00:00"), "2026-11-07T10:00:00+00:00")
    h.chk("antes_de_la_fecha_nueva_nada", r["acciones"] == [], r)
    r = vigilar(o, b, datos(1.10, D2), D2)
    h.chk("H14_con_la_fecha_nueva", [a["regla"] for a in r["acciones"]] == ["H-14"] and o.posiciones[PID]["estado"] == "EN_REVISION", r)
    # la fecha solo se renueva al confirmar la tesis
    o, b = abierta()
    h.rechaza("fecha_fuera_de_la_confirmacion_O01", o, lambda: o.posicion_transicion(PID, "EN_REVISION", "H", AHORA, fecha_revision="2026-12-01"), "O-01")
    o.posicion_transicion(PID, "EN_REVISION", "H", AHORA)
    h.chk("revision_por_otra_causa_se_confirma_sin_fecha", o.posicion_transicion(PID, "ABIERTA", "OPERADOR", AHORA, motivo="ok")["ok"]
          and o.posiciones[PID]["fecha_revision"] == "2026-12-05")

    # ------------------------------------------------------------ en revisión H sigue vigilando
    o, b = abierta(salida=SAL_PRONTO)
    r = vigilar(o, b, datos(1.15, D1), D1)   # llega la fecha y a la vez se cumple el objetivo (cartera en L2)
    h.chk("en_revision_el_objetivo_cierra", [a["regla"] for a in r["acciones"]] == ["H-14", "H-02"] and o.posiciones[PID]["estado"] == "CERRADA"
          and b.posiciones() == [], r)
    o, b = abierta(salida=SAL_PRONTO)
    vigilar(o, b, datos(1.10, D1), D1)
    r = reducir(o, PID, b, D1B, cantidad=40.0, actor="OPERADOR", motivo="reducir mientras reviso")
    h.chk("reducir_en_revision_no_la_confirma", r["ok"] and o.posiciones[PID]["estado"] == "EN_REVISION", r)
    r = cerrar(o, PID, b, D1B, actor="OPERADOR", motivo="la tesis ya no vale")
    h.chk("cerrar_desde_la_revision", r["ok"] and o.posiciones[PID]["estado"] == "CERRADA" and b.posiciones() == [], r)

    # ------------------------------------------------------------ revisión independiente (regresiones)
    from ejecucion_g import BrokerSimulado, declarar_manual
    from pruebas_ejecucion_g import HORA_DATOS, broker
    from pruebas_manual import a_mano, cambia, sin, reg as reg_manual
    from pruebas_orquestador import anotar_entrada, autorizar_op
    T1M = "2026-11-06T09:05:00+00:00"
    CONTADO = "Contado (spot) en intermediario"
    # 1. CT-G-14 por otra vía
    o, b = autorizado()
    a_mano(b, "EURUSD", "COMPRA", 100.0, "MAN-ORD-1", stop=("MAN-STOP-1", 1.05), via=CONTADO)
    r = declarar_manual(o, reg_manual(), b, T1M)
    h.chk("1_manual_ejecutado_por_otra_via_G10", r["codigo"] == "G-10" and not o.posiciones, r)
    r = declarar_manual(o, reg_manual(via_acceso=CONTADO), b, T1M)
    h.chk("1_manual_declarado_por_otra_via_RM05", r["codigo"] == "O-01" and "RM-05" in r.get("reglas", []) and not o.posiciones, r)
    sin_via = reg_manual()
    sin_via = sin(sin_via, "via_acceso")
    r = o.registrar_manual(sin_via, T1M)
    h.chk("1_manual_sin_via_RM05", "RM-05" in r.get("reglas", []), r)
    o, b = autorizado()
    a_mano(b, "EURUSD", "COMPRA", 100.0, "MAN-ORD-1", stop=("MAN-STOP-1", 1.05))
    r = declarar_manual(o, reg_manual(), b, T1M)
    h.chk("1_manual_por_la_via_analizada_abre", r["ok"] and o.posiciones[PID]["via_acceso"] == VIA, r)
    cierre = reg_manual(event_id="EV-MAN-0002", vinculo={"tipo": "POSICION", "id": PID}, lado="VENTA", ref_intermediario="MAN-CIERRE-1", via_acceso=CONTADO)
    cierre = sin(cierre, "proteccion_ref")
    h.chk("1_cerrar_a_mano_por_otra_via_RM05", "RM-05" in o.registrar_manual(cierre, "2026-11-06T09:10:00+00:00").get("reglas", []))
    # 2. CT-G-14 sobre un expediente alterado: O-13 y kill-switch
    o, b = autorizado(b=broker(precio=1.12))
    r = ejecutar(o, EID, b, AHORA)
    o.expedientes[EID]["orden_entrada"]["estado"] = "CANCELADA"
    r = o.registrar_manual(reg_manual(), T1M)
    h.chk("2_manual_con_la_orden_de_entrada_alterada_O13_y_kill", r["codigo"] == "O-13" and o.kill is not None and not o.posiciones
          and o.integridad() == ["EXP:" + EID], r)
    o, b = autorizado()
    o.expedientes[EID]["control_f"]["cantidad_aprobada"] = 150.0
    r = o.registrar_manual(reg_manual(cantidad=120.0), T1M)
    h.chk("2_manual_con_F_alterado_O13", r["codigo"] == "O-13" and o.kill is not None and not o.posiciones, r)
    # 3. G comprueba la vía con la que ejecutó el intermediario y la lleva en todas sus órdenes
    class OtraVia(BrokerSimulado):
        def enviar(self, x):
            if x.get("tipo") == "LIMITE":
                x = {**x, "via_acceso": CONTADO}
            return super().enviar(x)
    o, b = autorizado(b=OtraVia(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0}))
    r = ejecutar(o, EID, b, AHORA)
    h.chk("3_entrada_por_otra_via_se_deshace_G03", r["codigo"] == "G-03" and not o.posiciones and b.posiciones() == [], r)
    o, b = abierta()
    reducir(o, PID, b, "2026-11-06T09:05:00+00:00", cantidad=40.0, actor="OPERADOR", motivo="x")
    cerrar(o, PID, b, "2026-11-06T09:06:00+00:00", actor="OPERADOR", motivo="x")
    vias = {k: r_["orden"].get("via_acceso") for k, r_ in b.ordenes.items()}
    h.chk("3_todas_las_ordenes_de_G_llevan_la_via", set(vias.values()) == {VIA}, vias)
    o, b = abierta()
    b.ordenes["ORD-EXP-0001-S-1"]["orden"]["via_acceso"] = CONTADO
    c = conciliar(o, b, "2026-11-06T09:05:00+00:00")
    h.chk("3_stop_por_otra_via_es_discrepancia", not c["ok"] and any(d["tipo"] == "PROTECCION" for d in c["diferencias"]), c)
    # 4. la fecha de revisión también se comprueba al autorizar y al ejecutar
    o = nuevo()
    hasta(o, "PROPUESTA", salida=SAL_PRONTO)
    r = autorizar_op(o, EID, informe_f(o, EID, 1), D1)
    h.chk("4_autorizar_con_la_fecha_llegada_O10", r["codigo"] == "O-10" and "fecha de revisión" in r["motivo"], r)
    o = nuevo()
    hasta(o, "AUTORIZADA", salida=SAL_PRONTO)
    anotar_entrada(o, EID, "ORD-1", 100.0, AHORA)
    r = o.ejecutar(EID, {"orden_id": "ORD-1", "cantidad": 100.0, "precio": 1.1, "conciliada": True, "proteccion_orden_ids": ["ORD-1-STOP"],
                         "ejecutada_en": D1}, "G", D1)
    h.chk("4_ejecutar_con_la_fecha_llegada_O10", r["codigo"] == "O-10" and "fecha de revisión" in r["motivo"] and not o.posiciones, r)
    # 5 y 6. quién confirma la tesis y hasta cuándo
    o, b = abierta(salida=SAL_PRONTO)
    vigilar(o, b, datos(1.10, D1), D1)
    h.rechaza("5_gestor_de_otra_cartera_no_confirma_O05", o, lambda: o.posicion_transicion(PID, "ABIERTA", "GESTOR_TRADING", D1B, motivo="x", fecha_revision="2026-12-01"), "O-05")
    h.rechaza("6_fecha_nueva_demasiado_lejos_O06", o, lambda: o.posicion_transicion(PID, "ABIERTA", "OPERADOR", D1B, motivo="x", fecha_revision="9999-12-31"), "O-06")
    r = o.posicion_transicion(PID, "ABIERTA", "GESTOR_TACTICA", D1B, motivo="la tesis sigue", fecha_revision="2026-12-01")
    h.chk("5_el_gestor_de_la_cartera_confirma", r["ok"], r)
    h.chk("7_las_condiciones_de_salida_llevan_la_fecha_nueva", o.posiciones[PID]["condiciones_salida"]["fecha"] == "2026-12-01" == o.posiciones[PID]["fecha_revision"]
          and o.integridad() == [])
    # nota: la vigencia del sobre y el informe del Contradictor van en la cadena
    o = nuevo()
    hasta(o, "PROPUESTA")
    o.expedientes[EID]["sobre"]["valid_until"] = "2027-12-31T00:00:00+00:00"
    h.chk("nota_alargar_la_vigencia_del_sobre_se_detecta", o.integridad() == ["EXP:" + EID])

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO REVISION:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
