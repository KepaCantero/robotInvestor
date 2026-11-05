"""Pruebas de CT-G-14 (registro de ejecución manual) y de la conciliación con diferencias explicadas (T-19)."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validador"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ejecucion_g import BrokerSimulado, conciliar, declarar_manual, ejecutar  # noqa: E402
from manual_g import envolver_manual, validar_manual  # noqa: E402
from vigilancia import vigilar  # noqa: E402
from pruebas_ejecucion_g import autorizado, broker  # noqa: E402
from pruebas_orquestador import autorizar_op, AHORA, Arnes, hasta, nuevo  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402

T1 = "2026-11-06T09:05:00+00:00"
T2 = "2026-11-06T09:10:00+00:00"
L1 = {"nivel_autonomia": {"TACTICA": "L1"}}
PID = "POS-EXP-0001"
VIA = "Futuro de divisas, vencimiento trimestral"


class NoCancela(BrokerSimulado):
    """Como un intermediario real: un stop sin posición debajo no se cancela solo."""
    def _fill(self, o, q, p):
        d = q if o["lado"] == "COMPRA" else -q
        cur = self.pos.get(o["instrumento"], {"cantidad": 0.0, "activo_base": o["activo_base"]})
        cur["cantidad"] += d
        if abs(cur["cantidad"]) <= 1e-6:
            self.pos.pop(o["instrumento"], None)
        else:
            self.pos[o["instrumento"]] = cur


ENV = ("event_id", "correlation_id", "expediente_id", "producer", "consumer", "tipo_mensaje", "version_esquema", "emitido_en", "valid_until", "data_refs")


def ct14(campos):
    """CT-G-14 0.2.0 a partir de los campos planos de una prueba. La identidad del caso se deduce del vínculo como lo haría la
    consola (EXP-n -> COR-n; POS-EXP-n -> EXP-n); un campo de la envoltura dado en `campos` la sustituye tal cual."""
    f = dict(campos)
    v = f.get("vinculo")
    vid = v.get("id") if isinstance(v, dict) else None
    eid = (vid[4:] if vid.startswith("POS-") else vid) if isinstance(vid, str) else None
    cid = "COR-" + eid.split("-")[-1] if eid else None
    env = {k: f.pop(k) for k in ENV if k in f}
    m = envolver_manual(f, env.pop("event_id", "EV-MAN-0001"), env.pop("emitido_en", T1), expediente_id=eid, correlation_id=cid)
    m.update(env)
    return m


def plano(m):
    """Campos planos de un CT-G-14 de prueba (para derivar variantes)."""
    return {**{k: m[k] for k in ENV if k in m and k not in ("data_refs", "tipo_mensaje", "version_esquema", "consumer", "valid_until",
                                                             "correlation_id", "expediente_id")}, **m["payload"]}


def cambia(m, **kw):
    """El mismo registro con otros campos (re-envuelto: data_refs e identidad se recalculan salvo que se den)."""
    return ct14({**plano(m), **kw})


def sin(m, *claves):
    return ct14({k: v for k, v in plano(m).items() if k not in claves})


def reg(**kw):
    r = {"event_id": "EV-MAN-0001", "producer": "OPERADOR",
         "emitido_en": T1, "ejecutado_en": AHORA, "cartera": "TACTICA", "instrumento": "EURUSD", "activo_base": "EUR",
         "lado": "COMPRA", "cantidad": 100.0, "precio": 1.10, "ref_intermediario": "MAN-ORD-1",
         "motivo": "ejecutado a mano en la plataforma", "vinculo": {"tipo": "EXPEDIENTE", "id": "EXP-0001"}, "proteccion_ref": "MAN-STOP-1",
         "via_acceso": VIA}
    r.update(kw)
    return ct14(r)


def libre(**kw):
    r = plano(reg(vinculo={"tipo": "LIBRE", "id": None}, instrumento="GBPUSD", activo_base="GBP", cantidad=50.0, precio=1.30,
                  event_id="EV-MAN-0010", ref_intermediario="MAN-GBP-1"))
    r.pop("proteccion_ref")
    r.update(kw)
    return ct14(r)


def a_mano(b, ins, lado, q, oid, stop=None, via=None):
    """El operador opera directamente en el intermediario, sin pasar por G (por la vía analizada, salvo que se diga otra)."""
    b.precios.setdefault(ins, 1.30)
    via = via or VIA
    r = b.enviar({"orden_id": oid, "tipo": "MERCADO", "lado": lado, "instrumento": ins, "activo_base": ins[:3], "cantidad": q, "via_acceso": via})
    if stop:
        b.enviar({"orden_id": stop[0], "tipo": "STOP", "lado": "VENTA" if lado == "COMPRA" else "COMPRA", "instrumento": ins,
                  "activo_base": ins[:3], "cantidad": q, "precio": stop[1], "via_acceso": via})
    return r


def estado(o):
    return copy.deepcopy((o.posiciones, o.manuales, o.eventos, o.expedientes, o.ordenes_usadas))


def main():
    h = Arnes()
    ctx = {"ahora": T1, "expediente": None, "posicion": None, "tolerancia_precio": 0.05}
    # ---------------------------------------------------------------- validador puro
    h.chk("libre_valido", validar_manual(libre(), ctx) == [])
    def regla(nombre, r, esperada, c=ctx):
        f = validar_manual(r, c)
        h.chk(nombre, {x["regla"] for x in f} == {esperada}, f)
    regla("no_objeto_RM01", "x", "RM-01")
    regla("campo_de_mas_RM01", {**libre(), "extra": 1}, "RM-01")
    falta = libre(); falta["payload"].pop("motivo")
    regla("campo_de_menos_RM01", falta, "RM-01")
    regla("contrato_otro_RM01", libre(tipo_mensaje="CT-G-08"), "RM-01")
    regla("version_retirada_RM01", libre(version_esquema="0.1.0"), "RM-01")
    regla("lado_invalido_RM01", libre(lado="LARGO"), "RM-01")
    regla("cantidad_cero_RM01", libre(cantidad=0), "RM-01")
    regla("cantidad_nan_RM01", libre(cantidad=float("nan")), "RM-01")
    regla("cantidad_booleana_RM01", libre(cantidad=True), "RM-01")
    regla("precio_negativo_RM01", libre(precio=-1.0), "RM-01")
    regla("motivo_vacio_RM01", libre(motivo="  "), "RM-01")
    regla("cartera_inventada_RM01", libre(cartera="OTRA"), "RM-01")
    regla("libre_con_id_RM01", libre(vinculo={"tipo": "LIBRE", "id": "EXP-0001"}), "RM-01")
    regla("libre_con_proteccion_RM01", libre(proteccion_ref="S-1"), "RM-01")
    regla("comision_negativa_RM01", libre(comision_eur=-0.5), "RM-01")
    h.chk("comision_cero_valida", validar_manual(libre(comision_eur=0.0), ctx) == [])
    regla("instante_sin_zona_RM01", libre(emitido_en="2026-11-06T09:05:00"), "RM-01")
    regla("emisor_G_RM02", libre(producer="G"), "RM-02")
    regla("ejecutado_despues_de_emitido_RM03", libre(ejecutado_en=T2), "RM-03")
    regla("emitido_en_el_futuro_RM03", libre(emitido_en=T2), "RM-03", {**ctx, "ahora": T1})
    regla("declaracion_tardia_RM03", libre(ejecutado_en="2026-11-02T09:00:00+00:00"), "RM-03")
    regla("instrumento_no_admitido_RM08", libre(), "RM-08", {**ctx, "instrumentos_permitidos": {"TACTICA": ["EURUSD"]}})
    h.chk("instrumento_admitido_ok", validar_manual(libre(), {**ctx, "instrumentos_permitidos": {"TACTICA": ["GBPUSD"]}}) == [])

    # ---------------------------------------------------------------- vínculo a expediente: abre la posición
    o, b = autorizado(o=nuevo(L1))
    a_mano(b, "EURUSD", "COMPRA", 100.0, "MAN-ORD-1", stop=("MAN-STOP-1", 1.05))
    c0 = conciliar(o, b, T1)
    h.chk("sin_declarar_es_discrepancia", not c0["ok"] and [d["tipo"] for d in c0["diferencias"]] == ["POSICION_DESCONOCIDA"], c0)
    for av in list(o.avisos):
        o.acusar_aviso(av["id"], "OPERADOR", T1)
    r = o.registrar_manual(reg(), T1)
    h.chk("expediente_manual_abre_posicion", r["ok"] and r["posicion_id"] == PID and o.posiciones[PID]["estado"] == "ABIERTA"
          and o.posiciones[PID]["origen"] == "MANUAL" and o.expedientes["EXP-0001"]["estado"] == "EJECUTADA", r)
    h.chk("historial_dice_quien_y_como", o.posiciones[PID]["historial"][0]["actor"] == "OPERADOR"
          and "CT-G-14" in o.posiciones[PID]["historial"][0]["motivo"] and o.integridad() == [])
    c1 = conciliar(o, b, T1)
    h.chk("declarado_concilia_limpio", c1["ok"] and c1["diferencias"] == [], c1)
    h.chk("duplicado_identico_O02", o.registrar_manual(reg(), T1)["codigo"] == "O-02")
    h.chk("mismo_event_id_otro_contenido_O03", o.registrar_manual(reg(cantidad=50.0), T1)["codigo"] == "O-03")
    h.chk("orden_ya_registrada_O03", o.registrar_manual(libre(ref_intermediario="MAN-ORD-1"), T1)["codigo"] == "O-03")
    h.chk("proteccion_ya_registrada_O03", o.registrar_manual(libre(event_id="EV-MAN-0011", ref_intermediario="MAN-STOP-1"), T1)["codigo"] == "O-03")
    # H vigila la posición manual igual que las demás
    r = vigilar(o, b, {"EURUSD": {"precio": 1.30, "hora": T2}}, T2)
    h.chk("H_vigila_la_posicion_manual", [a["regla"] for a in r["acciones"]] == ["H-10"] and r["conciliacion_ok"], r)

    def rechazo(nombre, r_, esperada, prep=None, cfg=L1):
        o_, b_ = autorizado(o=nuevo(cfg))
        if prep:
            prep(o_)
        antes = estado(o_)
        res = o_.registrar_manual(r_, T1)
        h.chk(nombre, res["codigo"] == "O-01" and esperada in res.get("reglas", []) and estado(o_) == antes, res)
    rechazo("expediente_sentido_contrario_RM05", reg(lado="VENTA"), "RM-05")
    rechazo("expediente_otro_instrumento_RM05", reg(instrumento="GBPUSD"), "RM-05")
    rechazo("expediente_otra_cartera_RM05", reg(cartera="TRADING"), "RM-05")
    rechazo("expediente_mas_de_lo_aprobado_RM06", reg(cantidad=1e6), "RM-06")
    sin_prot = sin(reg(), "proteccion_ref")
    rechazo("expediente_sin_proteccion_RM07", sin_prot, "RM-07")
    rechazo("expediente_precio_lejos_RM09", reg(precio=1.30), "RM-09")
    rechazo("expediente_inexistente_RM04", reg(vinculo={"tipo": "EXPEDIENTE", "id": "EXP-9999"}), "RM-04")
    rechazo("producer_no_operador_RM02", reg(producer="G"), "RM-02")
    o, b = nuevo(L1), broker(); hasta(o, "PROPUESTA")
    res = o.registrar_manual(reg(), T1)
    h.chk("expediente_no_autorizado_RM04", res["codigo"] == "O-01" and "RM-04" in res["reglas"] and o.posiciones == {}, res)
    o, b = autorizado(o=nuevo(L1))
    res = o.registrar_manual(reg(cantidad=100.0, precio=1.10), "2026-11-08T13:00:00+00:00")
    h.chk("ventana_vencida_O10", res["codigo"] == "O-10" and o.posiciones == {}, res)
    o, b = autorizado(o=nuevo(L1))
    h.chk("reloj_hacia_atras_O16", o.registrar_manual(reg(), T1)["ok"] and o.registrar_manual(libre(), AHORA)["codigo"] == "O-16")
    # autorización automática + cartera degradada: el operador sí puede ejecutar a mano
    o = nuevo({"matriz_autonomia": {"TACTICA": True}, "nivel_autonomia": {"TACTICA": "L2"}}); hasta(o, "PROPUESTA")
    b = broker()
    from ejecucion_g import cartera_para_f
    o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o, "EXP-0001", n=1, cartera=cartera_para_f(b)), AHORA)
    o.degradar("TACTICA", "prueba", "G", AHORA)
    h.chk("degradada_G_no_ejecuta_pero_el_operador_a_mano_si", not ejecutar(o, "EXP-0001", b, AHORA)["ok"] and o.registrar_manual(reg(), T1)["ok"])

    # ---------------------------------------------------------------- vínculo a posición: la cierra
    o, b = autorizado(o=nuevo(L1)); ejecutar(o, "EXP-0001", b, AHORA)
    a_mano(b, "EURUSD", "VENTA", 100.0, "MAN-CIERRE-1")
    cierre = reg(event_id="EV-MAN-0002", vinculo={"tipo": "POSICION", "id": PID}, lado="VENTA", ref_intermediario="MAN-CIERRE-1")
    cierre = sin(cierre, "proteccion_ref")
    r = o.registrar_manual(cierre, T1)
    h.chk("posicion_manual_se_cierra", r["ok"] and o.posiciones[PID]["estado"] == "CERRADA" and o.posiciones[PID]["cantidad"] == 0
          and [x["hasta"] for x in o.posiciones[PID]["historial"]][-2:] == ["CERRANDO", "CERRADA"], r)
    c = conciliar(o, b, T1)
    h.chk("cierre_manual_concilia_limpio", c["ok"], c)
    h.chk("posicion_cerrada_no_admite_otro_cierre_RM04", "RM-04" in o.registrar_manual(cambia(cierre, event_id="EV-MAN-0003", ref_intermediario="MAN-CIERRE-2"), T1).get("reglas", []))
    o, b = autorizado(o=nuevo(L1)); ejecutar(o, "EXP-0001", b, AHORA)
    antes = estado(o)
    h.chk("cierre_parcial_RM06", "RM-06" in o.registrar_manual(cambia(cierre, cantidad=40.0), T1).get("reglas", []) and estado(o) == antes)
    h.chk("cierre_en_el_mismo_sentido_RM05", "RM-05" in o.registrar_manual(cambia(cierre, lado="COMPRA"), T1).get("reglas", []))
    h.chk("cierre_de_posicion_inexistente_RM04", "RM-04" in o.registrar_manual(cambia(cierre, vinculo={"tipo": "POSICION", "id": "POS-X"}), T1).get("reglas", []))
    h.chk("cierre_con_orden_usada_por_G_O03", o.registrar_manual(cambia(cierre, ref_intermediario="ORD-EXP-0001-S-1"), T1)["codigo"] == "O-03")

    # ---------------------------------------------------------------- operaciones LIBRES y diferencias explicadas
    o, b = abierta_l1({"nivel_autonomia": {"TACTICA": "L2"}})
    a_mano(b, "GBPUSD", "COMPRA", 50.0, "MAN-GBP-1")
    c = conciliar(o, b, T1)
    h.chk("libre_sin_declarar_degrada", not c["ok"] and "TACTICA" in o.degradadas and "POSICION_DESCONOCIDA" in [d["tipo"] for d in c["diferencias"]], c)
    h.chk("libre_declarado_se_acepta", o.registrar_manual(libre(), T1)["ok"] and len(o.manuales) == 1)
    c = conciliar(o, b, T1)
    h.chk("libre_declarado_es_explicada", c["ok"] and [x["tipo"] for x in c["explicadas"]] == ["MANUAL_DECLARADA"], c)
    a_mano(b, "GBPUSD", "VENTA", 50.0, "MAN-GBP-2")
    c = conciliar(o, b, T2)
    h.chk("libre_cerrado_sin_declarar_no_cuadra", not c["ok"] and [d["tipo"] for d in c["diferencias"]] == ["MANUAL_NO_CUADRA"], c)
    o.registrar_manual(libre(event_id="EV-MAN-0012", ref_intermediario="MAN-GBP-2", lado="VENTA", emitido_en=T2, ejecutado_en=T1), T2)
    c = conciliar(o, b, T2)
    h.chk("libre_compensado_concilia_limpio", c["ok"] and c["explicadas"] == [], c)
    # libre sobre el mismo instrumento que una posición del sistema
    o, b = abierta_l1()
    a_mano(b, "EURUSD", "COMPRA", 30.0, "MAN-EUR-1")
    h.chk("libre_en_instrumento_con_posicion_es_cantidad", [d["tipo"] for d in conciliar(o, b, T1)["diferencias"]] == ["CANTIDAD"])
    r = o.registrar_manual(libre(instrumento="EURUSD", activo_base="EUR", cantidad=30.0, precio=1.10, ref_intermediario="MAN-EUR-1"), T1)
    h.chk("libre_en_instrumento_con_posicion_RM10", r["codigo"] == "O-01" and "RM-10" in r["reglas"] and o.manuales == [], r)
    h.chk("y_la_discrepancia_sigue", [d["tipo"] for d in conciliar(o, b, T1)["diferencias"]] == ["CANTIDAD"])

    # tolerancia de redondeo
    o, b = abierta_l1({"tolerancia_conciliacion_rel": 0.005, "nivel_autonomia": {"TACTICA": "L2"}})
    b.pos["EURUSD"]["cantidad"] = 100.3
    c = conciliar(o, b, T1)
    h.chk("redondeo_dentro_de_tolerancia_es_explicada", c["ok"] and [x["tipo"] for x in c["explicadas"]] == ["REDONDEO"] and o.nivel("TACTICA") == "L2"
          and not o.degradadas and o.avisos == [], c)
    b.pos["EURUSD"]["cantidad"] = 101.0
    h.chk("fuera_de_tolerancia_es_discrepancia", [d["tipo"] for d in conciliar(o, b, T1)["diferencias"]] == ["CANTIDAD"])
    o, b = abierta_l1()
    b.pos["EURUSD"]["cantidad"] = 100.3
    h.chk("tolerancia_por_defecto_cero", [d["tipo"] for d in conciliar(o, b, T1)["diferencias"]] == ["CANTIDAD"])
    b.pos["EURUSD"]["cantidad"] = -100.0
    h.chk("sentido_contrario_sigue_detectandose", [d["tipo"] for d in conciliar(o, b, T1)["diferencias"]] == ["SENTIDO_O_ACTIVO"])
    # --- hallazgos de la revisión independiente
    o, b = abierta_l1()
    r = o.registrar_manual(libre(instrumento="EURUSD", activo_base="EUR", lado="VENTA", cantidad=100.0, precio=1.10, ref_intermediario="MAN-X"), T1)
    h.chk("libre_que_compensaria_una_posicion_RM10", "RM-10" in r.get("reglas", []))
    o, b = autorizado(o=nuevo(L1))
    r = o.registrar_manual(libre(instrumento="EURUSD", activo_base="EUR", cantidad=5000.0, precio=1.10, ref_intermediario="MAN-X"), T1)
    h.chk("libre_en_instrumento_de_expediente_autorizado_RM10", "RM-10" in r.get("reglas", []), r)
    o2, b2 = autorizado(o=nuevo(L1)); ejecutar(o2, "EXP-0001", b2, AHORA)
    hasta(o2, "PROPUESTA", n=3)   # otra comparación (EXP-0003 frente a EXP-0004), elegida y propuesta
    from ejecucion_g import cartera_para_f as _cpf
    ra = autorizar_op(o2, "EXP-0003", informe_f(o2, "EXP-0003", n=3, cartera=_cpf(b2)), AHORA)
    h.chk("segundo_expediente_autorizado", ra["ok"], ra)
    r = o2.registrar_manual(reg(event_id="EV-MAN-0020", vinculo={"tipo": "EXPEDIENTE", "id": "EXP-0003"}, ref_intermediario="MAN-2", proteccion_ref="MAN-S-2"), T1)
    h.chk("segunda_posicion_en_el_mismo_instrumento_O06", r["codigo"] == "O-06" and len(o2.posiciones) == 1, r)
    o, b = nuevo(L1), broker()
    h.chk("libre_dos_veces_la_misma_orden_O03", o.registrar_manual(libre(), T1)["ok"]
          and o.registrar_manual(libre(event_id="EV-MAN-0099"), T1)["codigo"] == "O-03")
    h.chk("libre_deja_aviso_O20", any(x["codigo"] == "O-20" for x in o.avisos))
    o, b = autorizado(o=nuevo(L1))
    r = o.registrar_manual(reg(proteccion_ref="MAN-ORD-1"), T1)
    h.chk("orden_y_proteccion_iguales_RM01", "RM-01" in r.get("reglas", []), r)
    r = o.registrar_manual(reg(ejecutado_en="2026-11-06T03:00:00+00:00"), T1)
    h.chk("ejecucion_anterior_a_la_autorizacion_RM03", "RM-03" in r.get("reglas", []), r)
    o, b = abierta_l1()
    r = o.registrar_manual(cambia(cierre, event_id="EV-MAN-0030", ejecutado_en="2026-11-06T08:00:00+00:00"), T1)
    h.chk("cierre_anterior_a_la_apertura_RM03", "RM-03" in r.get("reglas", []), r)
    o, b = nuevo({"tolerancia_conciliacion_rel": 0.01}), broker()
    b.pos["GBPUSD"] = {"cantidad": 0.45, "activo_base": "GBP"}
    h.chk("tolerancia_no_tapa_una_posicion_desconocida", [d["tipo"] for d in conciliar(o, b, T1)["diferencias"]] == ["POSICION_DESCONOCIDA"])
    o, b = abierta_l1({"tolerancia_conciliacion_rel": 0.01})
    b.pos["EURUSD"]["cantidad"] = -50.0
    h.chk("sentido_contrario_no_espejo", [d["tipo"] for d in conciliar(o, b, T1)["diferencias"]] == ["SENTIDO_O_ACTIVO"])
    o, b = nuevo(L1), broker()
    a_mano(b, "GBPUSD", "COMPRA", 50.0, "MAN-GBP-1")
    o.registrar_manual(libre(activo_base="XXX"), T1)
    h.chk("libre_con_activo_base_falso", "SENTIDO_O_ACTIVO" in [d["tipo"] for d in conciliar(o, b, T1)["diferencias"]])

    # --- declarar_manual: G contrasta con el intermediario
    o, b = autorizado(o=nuevo(L1))
    a_mano(b, "EURUSD", "COMPRA", 100.0, "MAN-ORD-1", stop=("MAN-STOP-1", 1.05))
    h.chk("G_orden_inventada_G10", declarar_manual(o, reg(ref_intermediario="NO-EXISTE"), b, T1)["codigo"] == "G-10" and o.posiciones == {})
    h.chk("G_precio_distinto_G10", declarar_manual(o, reg(precio=1.11), b, T1)["codigo"] == "G-10")
    h.chk("G_cantidad_distinta_G10", declarar_manual(o, reg(cantidad=90.0), b, T1)["codigo"] == "G-10")
    h.chk("G_proteccion_inexistente_G10", declarar_manual(o, reg(proteccion_ref="NADA"), b, T1)["codigo"] == "G-10")
    r = declarar_manual(o, reg(), b, T1)
    h.chk("G_declaracion_que_cuadra_abre", r["ok"] and o.posiciones[PID]["origen"] == "MANUAL" and conciliar(o, b, T1)["ok"], r)
    o, b = autorizado(o=nuevo(L1))
    a_mano(b, "EURUSD", "COMPRA", 100.0, "MAN-ORD-1", stop=("MAN-STOP-1", 1.00))
    h.chk("G_stop_a_otro_precio_G10", declarar_manual(o, reg(), b, T1)["codigo"] == "G-10")
    o, b = autorizado(o=nuevo(L1))
    a_mano(b, "EURUSD", "COMPRA", 100.0, "MAN-ORD-1", stop=("MAN-STOP-1", 1.05))
    b.caido = True
    h.chk("G_sin_conexion_G01", declarar_manual(o, reg(), b, T1)["codigo"] == "G-01" and o.posiciones == {})
    # cierre manual con un intermediario que NO cancela solo los stops
    o, b = autorizado(o=nuevo(L1), b=NoCancela(100000.0, {"EURUSD": 1.10}, "2026-11-06T08:59:00+00:00", tipos_cambio={"USD": 1.0})); ejecutar(o, "EXP-0001", b, AHORA)
    a_mano(b, "EURUSD", "VENTA", 100.0, "MAN-CIERRE-1")
    h.chk("el_stop_seguiria_vivo", b.consultar("ORD-EXP-0001-S-1")["estado"] == "ACEPTADA")
    r = declarar_manual(o, cierre, b, T1)
    h.chk("G_cierre_manual_cancela_el_stop", r["ok"] and b.consultar("ORD-EXP-0001-S-1")["estado"] == "CANCELADA"
          and o.posiciones[PID]["estado"] == "CERRADA" and conciliar(o, b, T1)["ok"], r)
    o, b = abierta_l1()
    b.mover_precio("EURUSD", 1.04, T1)
    r = declarar_manual(o, cambia(cierre, ref_intermediario="ORD-EXP-0001-S-1", precio=1.04), b, T1)
    # desde T-47 el Orquestador lo rechaza antes de consultar al intermediario: el stop es una orden ya registrada (O-03)
    h.chk("G_stop_ya_ejecutado_no_es_cierre_manual_O03", r["codigo"] == "O-03" and o.posiciones[PID]["estado"] == "ABIERTA", r)
    o, b = abierta_l1()
    a_mano(b, "EURUSD", "VENTA", 40.0, "MAN-CIERRE-1")
    r = declarar_manual(o, cambia(cierre, cantidad=40.0), b, T1)
    h.chk("G_cierre_que_no_deja_plano_G10", r["codigo"] in ("G-10", "O-01") and o.posiciones[PID]["estado"] == "ABIERTA", r)
    h.chk("G_registro_no_objeto_G10", declarar_manual(o, None, b, T1)["codigo"] == "G-10")

    # configuración
    from orquestador import Orquestador
    from pruebas_orquestador import CAL, CFG
    for nombre, cfg in (("tolerancia_negativa", {"tolerancia_conciliacion_rel": -1}), ("tolerancia_texto", {"tolerancia_conciliacion_rel": "0"}),
                        ("tolerancia_por_encima_del_tope", {"tolerancia_conciliacion_rel": 0.02}),
                        ("permitidos_no_dict", {"instrumentos_permitidos": ["EURUSD"]}), ("permitidos_cartera_mala", {"instrumentos_permitidos": {"X": ["EURUSD"]}})):
        try:
            Orquestador({**CFG, **cfg}, CAL); h.chk(f"config_{nombre}_se_rechaza", False)
        except ValueError:
            h.chk(f"config_{nombre}_se_rechaza", True)
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO CT-G-14:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


def abierta_l1(extra=None):
    o, b = autorizado(o=nuevo({**L1, **(extra or {})}))
    assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]
    return o, b


if __name__ == "__main__":
    sys.exit(main())
