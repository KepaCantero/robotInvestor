"""Pruebas de la reducción parcial declarada a mano (T-44: CT-G-14 vinculado a una POSICION con cantidad por debajo
de la de la posición). Datos SIMULADOS.

Comprueba: el caso bueno por G y por el Orquestador (cantidad nueva, protecciones, protecciones_anteriores,
reducciones, el stop viejo cancelado en el intermediario, la conciliación limpia y la integridad); los rechazos del
validador puro (RM-06/RM-07/RM-12) y de G (G-10); una posición REDUCIENDO que sigue con la regla de antes; el
registro duplicado (O-03); dos reducciones manuales seguidas; el cierre total manual posterior por lo que queda; una
pasada de H vigilando la posición con el stop nuevo sin incidencias; y las regresiones de la revisión independiente:
los contrastes de cantidad de la parcial son ABSOLUTOS (un desfase de 3e-5 se rechaza con G-10 y uno dentro de la
banda de 1e-6 cuadra con la conciliación inmediata) y la conciliación ve los stops retirados (un stop viejo vivo tras
un registro directo no queda invisible: PROTECCION_HUERFANA; retirado antes, como manda el patrón de T-12, concilia limpio).

La política de F de esta batería baja valor_min_eur a 20.0 [solo para la prueba; el oficial es 100.0]: con la
posición de prueba (100 EURUSD a 1,10 = 110 EUR) y el mínimo oficial no cabría ninguna reducción parcial.

Uso: python3 pruebas/pruebas_manual_t44.py
"""
import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

from control_f import POLITICA_DEFECTO  # noqa: E402
from ejecucion_g import TOL, BrokerSimulado, declarar_manual, conciliar, ejecutar  # noqa: E402
from manual_g import validar_manual  # noqa: E402
from vigilancia import vigilar  # noqa: E402
from pruebas_ejecucion_g import HORA_DATOS, autorizado  # noqa: E402
from pruebas_manual import PID, T1, T2, VIA, abierta_l1, a_mano, cambia, reg, sin, estado  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, nuevo  # noqa: E402

VMIN = 20.0   # [solo prueba] el valor_min_eur de la política de F para esta batería
L1_MIN = {"nivel_autonomia": {"TACTICA": "L1"}, "politica_f": {**POLITICA_DEFECTO, "valor_min_eur": VMIN}}
STOP_VIEJO = "ORD-EXP-0001-S-1"   # el stop de la entrada de G (solo reducción), a 1.05


def abierta_min(b=None):
    """Posición abierta en L1 (100 EURUSD a 1,10, stop 1.05) con el mínimo de F de la batería, en el broker dado."""
    o, b = autorizado(o=nuevo(dict(L1_MIN)), b=b)
    assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]
    return o, b


def coloca_stop(b, oid, cantidad, precio=1.05, lado="VENTA", ins="EURUSD", via=VIA):
    """Lo que hace el operador a mano: coloca el stop nuevo por lo que queda (antes de declarar la reducción).
    No exige que el intermediario la acepte: los stops malos de estas pruebas pueden ir rechazados."""
    return b.enviar({"orden_id": oid, "tipo": "STOP", "lado": lado, "instrumento": ins, "activo_base": ins[:3],
                     "cantidad": cantidad, "precio": precio, "via_acceso": via})


def rparcial(**kw):
    """CT-G-14 0.2.0 de la reducción parcial buena: vende 40 de 100, con el stop nuevo MAN-STOP-2 por los 60 que quedan."""
    r = {"event_id": "EV-T44-0001", "producer": "OPERADOR", "emitido_en": T1, "ejecutado_en": AHORA, "cartera": "TACTICA",
         "instrumento": "EURUSD", "activo_base": "EUR", "lado": "VENTA", "cantidad": 40.0, "precio": 1.10,
         "ref_intermediario": "MAN-RED-1", "proteccion_ref": "MAN-STOP-2", "motivo": "vendo una parte a mano y dejo stop por lo que queda",
         "vinculo": {"tipo": "POSICION", "id": PID}, "via_acceso": VIA}
    r.update(kw)
    return reg(**r)


def arma_parcial(o, b, q=40.0, oid="MAN-RED-1", sid="MAN-STOP-2", precio_stop=1.05):
    """El operador vende `q` a mano y coloca el stop nuevo por lo que queda."""
    a_mano(b, "EURUSD", "VENTA", q, oid)
    assert coloca_stop(b, sid, 100.0 - q, precio=precio_stop)["estado"] == "ACEPTADA"


class CancelaEnFalso(BrokerSimulado):
    """Un intermediario que responde a la cancelación sin ejecutarla: el stop sigue vivo y lo dice así."""
    def cancelar(self, oid):
        super().cancelar(oid)
        c = self.ordenes.get(oid)
        if c is not None and c["estado"] != "EJECUTADA":
            c["estado"] = "ACEPTADA"
        return self._res(c) if c else None


def main():
    h = Arnes()

    # ---------------------------------------------------------------- validador puro (manual_g)
    o, b = abierta_min()
    p = o.posiciones[PID]
    ctx = {"ahora": T1, "expediente": None, "posicion": copy.deepcopy(p), "tolerancia_precio": 0.05,
           "valor_min_restante_eur": VMIN, "identidad": ("EXP-0001", "COR-0001")}   # fx USD = 1.0 en la foto de G
    h.chk("validador_parcial_valida", validar_manual(rparcial(), ctx) == [])
    h.chk("validador_parcial_sin_stop_RM07", {x["regla"] for x in validar_manual(sin(rparcial(), "proteccion_ref"), ctx)} == {"RM-07"})
    h.chk("validador_parcial_resto_bajo_el_minimo_RM12", {x["regla"] for x in validar_manual(rparcial(cantidad=90.0), ctx)} == {"RM-12"})
    sin_min = {k: v for k, v in ctx.items() if k != "valor_min_restante_eur"}
    h.chk("validador_parcial_sin_minimo_en_ctx_RM12", {x["regla"] for x in validar_manual(rparcial(), sin_min)} == {"RM-12"})
    h.chk("validador_mas_de_lo_que_hay_RM06", {x["regla"] for x in validar_manual(rparcial(cantidad=150.0), ctx)} == {"RM-06"})
    h.chk("validador_parcial_precio_cero_RM01", {x["regla"] for x in validar_manual(rparcial(precio=0.0), ctx)} == {"RM-01"})
    h.chk("validador_parcial_precio_que_desborda_RM12", {x["regla"] for x in validar_manual(rparcial(precio=1e308), ctx)} == {"RM-12"})
    reg90 = rparcial(cantidad=90.0)
    reg0, pos0 = copy.deepcopy(reg90), copy.deepcopy(ctx["posicion"])
    validar_manual(reg90, ctx)
    h.chk("validador_no_muta_registro_ni_posicion", reg90 == reg0 and ctx["posicion"] == pos0)
    p_red = {**copy.deepcopy(p), "estado": "REDUCIENDO", "cantidad": 60.0, "reduccion": {"objetivo_restante": 50.0}}
    f = validar_manual(rparcial(cantidad=30.0), {**ctx, "posicion": p_red})
    h.chk("validador_reduriendo_sigue_la_regla_de_antes_RM06", {x["regla"] for x in f} == {"RM-06"} and "a media reducción" in f[0]["mensaje"], f)

    # ---------------------------------------------------------------- camino bueno por G (declarar_manual)
    o, b = abierta_min()
    arma_parcial(o, b)
    res = declarar_manual(o, rparcial(), b, T1)
    p = o.posiciones[PID]
    h.chk("G_parcial_ok", res["ok"] and res["posicion_id"] == PID and p["estado"] == "ABIERTA" and p["cantidad"] == 60.0, res)
    h.chk("parcial_protecciones_actualizadas", p["protecciones"] == ["MAN-STOP-2"] and p["protecciones_anteriores"] == [STOP_VIEJO], p)
    red = p["reducciones"][-1]
    h.chk("parcial_reduccion_anotada", len(p["reducciones"]) == 1 and red["n"] == 1 and red["cantidad"] == 40.0 and red["desde"] == 100.0
          and red["restante"] == 60.0 and red["manual"] is True and red["orden_id"] == "MAN-RED-1"
          and "terminada_en" in red and red["motivo"].startswith("vendo una parte"), red)
    h.chk("parcial_stop_viejo_cancelado_y_nuevo_vivo", b.consultar(STOP_VIEJO)["estado"] == "CANCELADA"
          and b.consultar("MAN-STOP-2")["estado"] == "ACEPTADA" and b.consultar("MAN-STOP-2")["cantidad"] == 60.0
          and b.consultar("MAN-STOP-2")["precio"] == 1.05)
    h.chk("parcial_ordenes_usadas", "MAN-RED-1" in o.ordenes_usadas and "MAN-STOP-2" in o.ordenes_usadas)
    ult = p["historial"][-1]
    h.chk("parcial_historial_e_integridad", ult["actor"] == "OPERADOR" and "reducción parcial manual" in ult["motivo"]
          and ult["ref"] == "MAN-RED-1" and ult["desde"] == ult["hasta"] == "ABIERTA"
          and o.integridad() == [] and o.posicion_integra(PID), ult)
    c = conciliar(o, b, T1)
    h.chk("parcial_concilia_limpio", c["ok"] and c["diferencias"] == [], c)
    v = vigilar(o, b, {"EURUSD": {"precio": 1.10, "hora": T2}}, T2)
    h.chk("H_vigila_con_el_stop_nuevo", v["conciliacion_ok"] and v["acciones"] == [] and o.posiciones[PID]["estado"] == "ABIERTA", v)
    h.chk("parcial_duplicada_O03", o.registrar_manual(rparcial(event_id="EV-T44-0002"), T2)["codigo"] == "O-03")

    # ---------------------------------------------------------------- camino bueno por el Orquestador (sin G)
    o, b = abierta_min()
    arma_parcial(o, b)
    res = o.registrar_manual(rparcial(), T1)
    h.chk("orquestador_parcial_ok", res["ok"] and o.posiciones[PID]["cantidad"] == 60.0
          and o.posiciones[PID]["protecciones"] == ["MAN-STOP-2"] and o.integridad() == [], res)
    # revisión T-44 (hallazgo 2): por el camino directo el Orquestador no toca el intermediario (límite de T-32),
    # pero la conciliación ya ve los stops retirados (protecciones_anteriores): un stop viejo vivo no puede quedar
    # invisible; y si el operador lo retiró antes, como manda el patrón de T-12, la conciliación queda limpia.
    o, b = abierta_min()
    arma_parcial(o, b)
    res = o.registrar_manual(rparcial(event_id="EV-T44-0010"), T1)
    c = conciliar(o, b, T1)
    h.chk("directo_stop_viejo_vivo_lo_ve_la_conciliacion", res["ok"]
          and b.consultar(STOP_VIEJO)["estado"] == "ACEPTADA" and not c["ok"]
          and [d["tipo"] for d in c["diferencias"]] == ["PROTECCION_HUERFANA"]
          and STOP_VIEJO in c["diferencias"][0]["detalle"], (res, c))
    o, b = abierta_min()
    arma_parcial(o, b)
    assert b.cancelar(STOP_VIEJO)["estado"] == "CANCELADA"   # el operador retira el viejo antes de declarar (T-12)
    res = o.registrar_manual(rparcial(event_id="EV-T44-0011"), T1)
    c = conciliar(o, b, T1)
    h.chk("directo_con_el_viejo_retirado_concilia_limpio", res["ok"] and c["ok"] and c["diferencias"] == []
          and o.posiciones[PID]["cantidad"] == 60.0 and o.integridad() == [], (res, c))

    # ---------------------------------------------------------------- rechazos del Orquestador: O-01 y estado intacto
    def rechazo(nombre, r_, regla, prep=None):
        o_, b_ = abierta_min()
        if prep:
            prep(o_, b_)
        antes = estado(o_)
        out = o_.registrar_manual(r_, T1)
        h.chk(nombre, out["codigo"] == "O-01" and regla in out.get("reglas", []) and estado(o_) == antes, out)
        return o_, b_

    rechazo("parcial_sin_stop_RM07", sin(rparcial(), "proteccion_ref"), "RM-07")
    rechazo("parcial_resto_bajo_el_minimo_RM12", rparcial(cantidad=90.0), "RM-12")
    rechazo("parcial_mas_que_la_posicion_RM06", rparcial(cantidad=150.0), "RM-06")
    rechazo("parcial_sin_tipo_de_cambio_RM12", rparcial(), "RM-12", prep=lambda o_, b_: setattr(o_, "ultima_foto", None))
    rechazo("parcial_precio_cero_RM01", rparcial(precio=0.0), "RM-01")
    rechazo("parcial_precio_que_desborda_RM12", rparcial(precio=1e308), "RM-12")
    o, b = abierta_min()
    h.chk("reduriendo_sigue_la_regla_de_antes_RM06", o.posicion_transicion(PID, "REDUCIENDO", "OPERADOR", T1, motivo="reducir riesgo", cantidad=40.0)["ok"]
          and o.registrar_manual(rparcial(event_id="EV-T44-0008"), T1)["codigo"] == "O-01"
          and "RM-06" in o.registrar_manual(rparcial(event_id="EV-T44-0008"), T1).get("reglas", [])
          and o.posiciones[PID]["estado"] == "REDUCIENDO")
    # la posición se queda en su estado: una parcial sobre EN_REVISION sigue EN_REVISION
    o, b = abierta_min()
    assert o.posicion_transicion(PID, "EN_REVISION", "H", T1, motivo="revisión de prueba")["ok"]
    arma_parcial(o, b)
    res = o.registrar_manual(rparcial(event_id="EV-T44-0009"), T1)
    h.chk("parcial_en_EN_REVISION_se_queda", res["ok"] and o.posiciones[PID]["estado"] == "EN_REVISION"
          and o.posiciones[PID]["cantidad"] == 60.0 and o.integridad() == [], res)

    # ---------------------------------------------------------------- rechazos de G: G-10, nada registrado ni tocado
    # el stop nuevo por otra cantidad, a otro precio, del lado equivocado o de otro instrumento: G-10
    o, b = abierta_min()
    a_mano(b, "EURUSD", "VENTA", 40.0, "MAN-RED-1")
    coloca_stop(b, "MAN-STOP-MAL-1", 50.0)   # por 50, no por lo que queda (60)
    h.chk("G_stop_por_otra_cantidad_G10", declarar_manual(o, rparcial(proteccion_ref="MAN-STOP-MAL-1"), b, T1)["codigo"] == "G-10"
          and o.posiciones[PID]["cantidad"] == 100.0)
    o, b = abierta_min()
    a_mano(b, "EURUSD", "VENTA", 40.0, "MAN-RED-1")
    coloca_stop(b, "MAN-STOP-MAL-2", 60.0, precio=1.00)   # a otro precio que el stop de la posición (1.05)
    h.chk("G_stop_a_otro_precio_G10", declarar_manual(o, rparcial(proteccion_ref="MAN-STOP-MAL-2"), b, T1)["codigo"] == "G-10"
          and o.posiciones[PID]["cantidad"] == 100.0)
    o, b = abierta_min()
    a_mano(b, "EURUSD", "VENTA", 40.0, "MAN-RED-1")
    coloca_stop(b, "MAN-STOP-MAL-3", 60.0, lado="COMPRA")   # del lado equivocado: el intermediario ni lo acepta
    h.chk("G_stop_del_lado_equivocado_G10", declarar_manual(o, rparcial(proteccion_ref="MAN-STOP-MAL-3"), b, T1)["codigo"] == "G-10"
          and o.posiciones[PID]["cantidad"] == 100.0)
    o, b = abierta_min()
    a_mano(b, "EURUSD", "VENTA", 40.0, "MAN-RED-1")
    coloca_stop(b, "MAN-STOP-MAL-4", 60.0, ins="GBPUSD")   # de otro instrumento
    h.chk("G_stop_de_otro_instrumento_G10", declarar_manual(o, rparcial(proteccion_ref="MAN-STOP-MAL-4"), b, T1)["codigo"] == "G-10"
          and o.posiciones[PID]["cantidad"] == 100.0)
    o, b = abierta_min()
    arma_parcial(o, b)
    h.chk("G_stop_inexistente_G10", declarar_manual(o, rparcial(proteccion_ref="MAN-NO-ESTA"), b, T1)["codigo"] == "G-10"
          and o.posiciones[PID]["cantidad"] == 100.0)
    # el neto del intermediario no cuadra: vendió 30 pero declara una parcial de 40
    o, b = abierta_min()
    a_mano(b, "EURUSD", "VENTA", 30.0, "MAN-RED-1")
    coloca_stop(b, "MAN-STOP-2", 60.0)
    h.chk("G_neto_no_cuadra_G10", declarar_manual(o, rparcial(cantidad=40.0), b, T1)["codigo"] == "G-10"
          and o.posiciones[PID]["cantidad"] == 100.0)
    # revisión T-44 (hallazgo 1): lo declarado se contrasta en ABSOLUTO (TOL, la misma medida de la conciliación,
    # de TOL_Q del Orquestador y del control de protección): un desfase de 3e-5 que la banda relativa admitía se
    # rechaza con G-10 y no se registra ni se toca nada, sea el stop por lo declarado o por lo que queda de verdad
    o, b = abierta_min()
    a_mano(b, "EURUSD", "VENTA", 40.0, "MAN-RED-1")
    coloca_stop(b, "MAN-STOP-2", 59.99997)   # el stop, por lo declarado
    h.chk("G_desfase_lo_declarado_G10", declarar_manual(o, rparcial(cantidad=40.00003), b, T1)["codigo"] == "G-10"
          and o.posiciones[PID]["cantidad"] == 100.0 and o.posiciones[PID]["protecciones"] == [STOP_VIEJO]
          and o.integridad() == [])
    o, b = abierta_min()
    a_mano(b, "EURUSD", "VENTA", 40.0, "MAN-RED-1")
    coloca_stop(b, "MAN-STOP-2", 60.0)   # el stop, por lo que queda de verdad
    h.chk("G_desfase_lo_real_G10", declarar_manual(o, rparcial(cantidad=40.00003), b, T1)["codigo"] == "G-10"
          and o.posiciones[PID]["cantidad"] == 100.0 and o.integridad() == [])
    o, b = abierta_min()
    qb = 40.0 + 5e-7   # dentro de la banda absoluta (5e-7 <= TOL): G la acepta y la conciliación inmediata queda limpia
    a_mano(b, "EURUSD", "VENTA", qb, "MAN-RED-1")
    coloca_stop(b, "MAN-STOP-2", 100.0 - qb)
    res = declarar_manual(o, rparcial(cantidad=qb), b, T1)
    c = conciliar(o, b, T1)
    h.chk("G_desfase_dentro_de_la_banda_consistente", res["ok"] and abs(o.posiciones[PID]["cantidad"] - (100.0 - qb)) <= TOL
          and c["ok"] and c["diferencias"] == [] and o.integridad() == [], (res, c))
    # el intermediario no cancela de verdad el stop viejo: G-10 y no se registra nada
    b2 = CancelaEnFalso(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0})
    o, b2 = abierta_min(b2)
    arma_parcial(o, b2)
    antes = estado(o)
    r = declarar_manual(o, rparcial(), b2, T1)
    h.chk("G_no_cancela_el_stop_viejo_G10", r["codigo"] == "G-10" and estado(o) == antes
          and b2.consultar(STOP_VIEJO)["estado"] == "ACEPTADA" and o.posiciones[PID]["cantidad"] == 100.0, r)

    # ---------------------------------------------------------------- comprobar_manual (sin efectos)
    o, b = abierta_min()
    arma_parcial(o, b)
    antes = estado(o)
    h.chk("comprobar_manual_parcial_sin_efectos", o.comprobar_manual(rparcial(), T1) is None and estado(o) == antes)
    mal = o.comprobar_manual(sin(rparcial(), "proteccion_ref"), T1)
    h.chk("comprobar_manual_parcial_mala_RM07", isinstance(mal, dict) and mal["codigo"] == "O-01" and "RM-07" in mal["motivo"], mal)

    # ---------------------------------------------------------------- secuencias
    # dos reducciones manuales seguidas
    o, b = abierta_min()
    arma_parcial(o, b)
    assert declarar_manual(o, rparcial(), b, T1)["ok"]
    a_mano(b, "EURUSD", "VENTA", 20.0, "MAN-RED-2")
    coloca_stop(b, "MAN-STOP-3", 40.0)
    res = declarar_manual(o, rparcial(event_id="EV-T44-0003", cantidad=20.0, ref_intermediario="MAN-RED-2",
                                      proteccion_ref="MAN-STOP-3"), b, T2)
    p = o.posiciones[PID]
    h.chk("dos_parciales_seguidas", res["ok"] and p["cantidad"] == 40.0 and p["protecciones"] == ["MAN-STOP-3"]
          and p["protecciones_anteriores"] == [STOP_VIEJO, "MAN-STOP-2"] and len(p["reducciones"]) == 2
          and p["reducciones"][1]["n"] == 2 and p["reducciones"][1]["desde"] == 60.0 and p["reducciones"][1]["restante"] == 40.0
          and b.consultar("MAN-STOP-2")["estado"] == "CANCELADA" and o.integridad() == [], res)
    c = conciliar(o, b, T2)
    h.chk("dos_parciales_concilian_limpio", c["ok"] and c["diferencias"] == [], c)
    # tras una parcial, el cierre total manual por lo que queda funciona
    a_mano(b, "EURUSD", "VENTA", 40.0, "MAN-CIERRE-9")
    cierre = sin(rparcial(event_id="EV-T44-0004", cantidad=40.0, ref_intermediario="MAN-CIERRE-9",
                          motivo="cierro lo que queda"), "proteccion_ref")
    res = declarar_manual(o, cierre, b, T2)
    h.chk("tras_parcial_el_cierre_total_funciona", res["ok"] and o.posiciones[PID]["estado"] == "CERRADA"
          and o.posiciones[PID]["cantidad"] == 0 and o.integridad() == [] and conciliar(o, b, T2)["ok"], res)

    # ---------------------------------------------------------------- posición CORTO: la parcial es simétrica
    # (la sonda de la revisión propia destapó aquí el defecto del neto con signo: fijado como comprobación)
    STOP_C = {"id": "STOP-1", "tipo": "STOP", "metrica": "precio", "operador": ">=", "umbral": 1.15, "unidad": "USD"}
    OBJ_C = {"id": "OBJ-1", "tipo": "OBJETIVO", "metrica": "precio", "operador": "<=", "umbral": 1.05, "unidad": "USD"}
    INV_C = {"id": "INV-1", "tipo": "INVALIDEZ", "metrica": "precio_cierre", "operador": ">", "umbral": 1.15, "unidad": "USD"}
    SAL_C = {"condiciones": [STOP_C, OBJ_C, INV_C], "fecha": "2026-12-05"}
    o, b = autorizado(o=nuevo(dict(L1_MIN)), salida=SAL_C)
    assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]
    p = o.posiciones[PID]
    lim = p["precio_entrada"]
    assert p["direccion"] == "CORTO" and p["stop_precio"] == 1.15, p
    a_mano(b, "EURUSD", "COMPRA", 40.0, "MAN-RED-1")   # el operador compra una parte del corto a mano
    coloca_stop(b, "MAN-STOP-2", 60.0, precio=1.15, lado="COMPRA")
    rec = reg(event_id="EV-T44-CORTO", vinculo={"tipo": "POSICION", "id": PID}, lado="COMPRA", cantidad=40.0, precio=lim,
              ref_intermediario="MAN-RED-1", proteccion_ref="MAN-STOP-2", motivo="compro una parte del corto a mano")
    res = declarar_manual(o, rec, b, T1)
    h.chk("parcial_en_corto_ok", res["ok"] and p["cantidad"] == 60.0 and p["estado"] == "ABIERTA"
          and p["protecciones"] == ["MAN-STOP-2"] and p["reducciones"][-1]["manual"] is True
          and p["reducciones"][-1]["restante"] == 60.0, res)
    h.chk("parcial_en_corto_stop_y_conciliacion", b.consultar("ORD-EXP-0001-S-1")["estado"] == "CANCELADA"
          and b.consultar("MAN-STOP-2")["estado"] == "ACEPTADA" and conciliar(o, b, T1)["ok"] and o.integridad() == [])
    o2, b2 = autorizado(o=nuevo(dict(L1_MIN)), salida=SAL_C)
    assert ejecutar(o2, "EXP-0001", b2, AHORA)["ok"]
    rec2 = cambia(rec, event_id="EV-T44-CORTO-2", cantidad=90.0)   # el mismo mínimo vale en un corto: RM-12
    out = o2.registrar_manual(rec2, T1)
    h.chk("parcial_en_corto_resto_minimo_RM12", out["codigo"] == "O-01" and "RM-12" in out.get("reglas", []), out)

    # V0.53 (revisión de la integración, g05 M2): un stop retirado a medias (PARCIAL) o ejecutado sin cerrar la posición sale en la
    # conciliación; uno ejecutado que dejó la posición a cero es el stop de la posición y H lo confirma (g01)
    for nombre, est_viejo, ejecutada in (("parcial", "PARCIAL", 30.0), ("ejecutado_sin_cerrar", "EJECUTADA", 30.0)):
        o, b = abierta_min()
        arma_parcial(o, b)
        assert o.registrar_manual(rparcial(event_id=f"EV-T44-M2-{nombre}"), T1)["ok"]
        b.ordenes[STOP_VIEJO]["estado"] = est_viejo   # el intermediario informa del stop viejo así (sin tocar la posición)
        b.ordenes[STOP_VIEJO]["ejecutada"] = ejecutada
        c = conciliar(o, b, T1)
        h.chk(f"r03_stop_retirado_{nombre}_PROTECCION_HUERFANA", any(d["tipo"] == "PROTECCION_HUERFANA" and STOP_VIEJO in d["detalle"]
                                                                       for d in c["diferencias"]), c)
    o, b = abierta_min()
    arma_parcial(o, b)
    assert o.registrar_manual(rparcial(event_id="EV-T44-G01"), T1)["ok"]   # camino directo sin retirar el stop viejo
    b.mover_precio("EURUSD", 1.04, T2)   # salta el stop viejo (solo reducción) y deja la posición a cero
    rv = vigilar(o, b, {"EURUSD": {"precio": 1.04, "hora": T2}}, T2)
    h.chk("r04_el_stop_retirado_que_salta_y_cierra_lo_confirma_H", o.posiciones[PID]["estado"] == "CERRADA"
          and any(a["regla"] == "H-01" and a["ok"] for a in rv["acciones"]) and conciliar(o, b, T2)["ok"], rv["acciones"])
    # V0.53 (g04): el mínimo de F se convierte a la divisa de cotización dividiendo por el tipo (EUR por USD)
    from pruebas_control_f import CART, registrar_foto
    o, b = abierta_min()
    registrar_foto(o, {**CART, "fecha_hora": AHORA, "tipos_cambio_eur": {"USD": 0.8}})   # 20 EUR = 25 USD
    h.chk("r05_minimo_convertido_a_la_divisa_de_cotizacion", abs(o._valor_min_restante("EURUSD") - VMIN / 0.8) <= 1e-9)
    arma_parcial(o, b, q=80.0)   # quedarían 20 x 1,10 = 22 USD: más que 20 pero menos que 25
    out = o.registrar_manual(rparcial(event_id="EV-T44-FX", cantidad=80.0), T1)
    h.chk("r05_con_otro_tipo_el_resto_se_mide_en_su_divisa_RM12", out["codigo"] == "O-01" and "RM-12" in out.get("reglas", []), out)

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO MANUAL T-44:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
