"""Pruebas de T-47: CT-G-08 y CT-G-14 en la versión 0.2.0 con la envoltura común; la 0.1.0 queda retirada."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

import contratos as ct  # noqa: E402
from control_f import aplanar_informe, construir_informe, controlar, motivo_de, validar_informe_f  # noqa: E402
from ejecucion_g import BrokerSimulado, conciliar, declarar_manual  # noqa: E402
from manual_g import aplanar_manual, envolver_manual, validar_manual  # noqa: E402
from pruebas_control_f import informe_f, pon  # noqa: E402
from pruebas_ejecucion_g import HORA_DATOS, autorizado  # noqa: E402
from pruebas_manual import L1, PID, T1, a_mano, cambia, estado, libre, plano, reg, sin  # noqa: E402
from pruebas_orquestador import AHORA, ENTRADA, Arnes, autorizar_op, hasta, nuevo  # noqa: E402


def a_010_f(inf):
    """El mismo informe en la forma plana retirada (0.1.0)."""
    p = aplanar_informe(inf)
    p.pop("motivo")
    return {**p, "version_esquema": "0.1.0"}


def a_010_m(m):
    """El mismo registro manual en la forma retirada (0.1.0: contrato/version, sin envoltura)."""
    return {"contrato": "CT-G-14", "version": "0.1.0", "event_id": m["event_id"], "producer": m["producer"], "emitido_en": m["emitido_en"],
            **m["payload"]}


class Vigilado(BrokerSimulado):
    """Cuenta las consultas: un mensaje mal envuelto no debe llegar al intermediario."""
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.consultas = 0

    def consultar(self, orden_id):
        self.consultas += 1
        return super().consultar(orden_id)


def vigilado():
    return Vigilado(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0})


def main():
    h = Arnes()

    def vfm(o, inf, e="EXP-0001"):
        x = o.expedientes[e]
        return validar_informe_f(inf, {"ahora": AHORA, "expediente_id": e, "correlation_id": x["correlation_id"], "divisa_cotizacion": "USD",
                                       "propuesta": x["propuesta"], "cartera_destino": x["cartera_destino"], "politica": o.cfg["politica_f"]})

    def vf(o, inf, e="EXP-0001"):
        return sorted({f["regla"] for f in vfm(o, inf, e)})

    # ================================================================ CT-G-08 0.2.0
    o = nuevo(); hasta(o, "PROPUESTA")
    inf = informe_f(o)
    h.chk("f_envoltura_comun", set(inf) == {"event_id", "correlation_id", "expediente_id", "producer", "consumer", "tipo_mensaje", "version_esquema",
                                            "emitido_en", "valid_until", "data_refs", "payload", "resultado_politica"}
          and inf["version_esquema"] == "0.2.0" and inf["data_refs"] == [], sorted(inf))
    h.chk("f_valida_en_contratos_y_en_F", ct.validar(inf) == [] and vf(o, inf) == [], (ct.validar(inf), vf(o, inf)))
    h.chk("f_payload_y_politica", set(inf["payload"]) == {"propuesta_ref", "entradas", "cantidad_aprobada"}
          and set(inf["resultado_politica"]) == {"version_politica", "resultado", "motivo", "controles"})
    # mismo resultado que las reglas, para aprobado, reducido y vetado
    for nombre, cart, esperado in (("aprobado", None, "APROBADO"),
                                   ("reducido", {"posiciones": [{"instrumento": "EURGBP", "activo_base": "EUR", "valor_eur": 15000.0}]}, "REDUCIDO"),
                                   ("vetado", {"perdida_dia_eur": 5000.0}, "VETADO")):
        o2 = nuevo(); hasta(o2, "PROPUESTA", entrada={**ENTRADA, "cantidad": 9090.0})
        i = informe_f(o2, cartera=cart)
        en = i["payload"]["entradas"]
        r = controlar(en["solicitud"], en["cartera"], en["politica"], i["emitido_en"])
        p = aplanar_informe(i)
        h.chk(f"f_mismo_resultado_{nombre}", r["resultado"] == esperado and (p["resultado"], p["cantidad_aprobada"], p["controles"])
              == (r["resultado"], r["cantidad_aprobada"], r["controles"]) and p["motivo"] == motivo_de(r["resultado"], r["controles"]), (r, p))
        h.chk(f"f_motivo_{nombre}", {"APROBADO": p["motivo"] == "todos los controles en OK",
                                     "REDUCIDO": p["motivo"].startswith("reduce F-"),
                                     "VETADO": p["motivo"].startswith("veta F-08")}[esperado], p["motivo"])
    # defectos de la envoltura: CF-01 (y CT-03 donde el esquema lo ve)

    def mut(fn):
        i = copy.deepcopy(inf)
        fn(i)
        return i
    for nombre, fn, cf, ctr in (
            ("data_refs_no_vacio", lambda i: i["data_refs"].append("EV-X"), "CF-01", "CT-03"),
            ("clave_de_mas_en_payload", lambda i: i["payload"].update(x=1), "CF-01", "CT-03"),
            ("clave_de_mas_en_politica", lambda i: i["resultado_politica"].update(x=1), "CF-01", "CT-03"),
            ("sin_resultado_politica", lambda i: i.pop("resultado_politica"), "CF-01", "CT-03"),
            ("payload_no_objeto", lambda i: i.update(payload=[]), "CF-01", "CT-03"),
            ("version_politica_ajena", lambda i: pon(i, version_politica="F-9.9.9"), "CF-01", None),
            ("motivo_inventado", lambda i: pon(i, motivo="porque sí"), "CF-04", None),
            ("controles_en_payload", lambda i: i["payload"].update(controles=i["resultado_politica"]["controles"]), "CF-01", "CT-03"),
            ("consumer_ajeno", lambda i: i.update(consumer="G"), "CF-01", "CT-03")):
        m = mut(fn)
        r = vf(o, m)
        c = ct.validar(m)
        h.chk(f"f_{nombre}_{cf.replace('-', '')}", cf in r and (ctr is None or (c and c[0]["regla"] == ctr)), (r, c))
    # la 0.1.0 plana está retirada
    viejo = a_010_f(inf)
    h.chk("f_010_CF01_version", vf(o, viejo) == ["CF-01"] and "versión" in vfm(o, viejo)[0]["mensaje"], vfm(o, viejo))
    h.chk("f_010_contratos_CT02_retirada", ct.validar(viejo)[0]["regla"] == "CT-02" and "retirada" in ct.validar(viejo)[0]["mensaje"])
    h.chk("f_010_se_lee_como_historico", ct.validar(viejo, historico=True) == [], ct.validar(viejo, historico=True))
    h.chk("f_020_tambien_en_historico", ct.validar(inf, historico=True) == [])
    h.rechaza("f_autorizar_con_010_O01", o, lambda: autorizar_op(o, "EXP-0001", viejo, AHORA), "O-01")
    h.rechaza("f_pantalla_con_010_O01", o, lambda: o.pantalla_aprobacion("EXP-0001", viejo, AHORA), "O-01")
    # el hash es del mensaje completo: una pantalla de otro mensaje con el mismo event_id no vale
    o3 = nuevo(); hasta(o3, "PROPUESTA")
    a = informe_f(o3)
    b = informe_f(o3, valid_until="2026-11-07T08:00:00+00:00")   # mismo event_id, otra envoltura, aún válido
    p = o3.pantalla_aprobacion("EXP-0001", a, AHORA)["pantalla"]
    h.chk("f_otra_envoltura_valida_por_si_misma", vf(o3, b) == [])
    r = o3.autorizar("EXP-0001", "OPERADOR", b, AHORA, {"pantalla_hash": p["hash"], "importe_tecleado": p["importe"], "canal": "CONSOLA", "segundo_factor": True})
    h.chk("f_pantalla_de_otro_mensaje_O27", r["codigo"] == "O-27" and o3.expedientes["EXP-0001"]["estado"] == "PROPUESTA", r)
    r = o3.autorizar("EXP-0001", "OPERADOR", a, AHORA, {"pantalla_hash": p["hash"], "importe_tecleado": p["importe"], "canal": "CONSOLA", "segundo_factor": True})
    cf = o3.expedientes["EXP-0001"]["control_f"]
    h.chk("f_autoriza_y_guarda_la_forma_interna", r["ok"] and set(cf) == {"resultado", "cantidad_aprobada", "event_id", "emitido_en", "valid_until",
                                                                       "entradas", "aprobacion"}
          and cf["cantidad_aprobada"] == a["payload"]["cantidad_aprobada"] and o3.integridad() == [], (r, sorted(cf)))
    h.chk("f_mismo_event_id_otra_envoltura_O03", autorizar_op(o3, "EXP-0001", b, AHORA)["codigo"] in ("O-03", "O-04"))
    h.chk("f_orden_CT_G_09_valida", ct.validar(ct.orden(o3, "EXP-0001")) == [])
    # nunca lanza
    prof = []
    for _ in range(50000):
        prof = [prof]
    raros = (None, [], "x", {}, {**inf, "payload": None}, {**inf, "resultado_politica": "x"}, {**inf, "data_refs": None},
             {**inf, "payload": {"propuesta_ref": prof, "entradas": prof, "cantidad_aprobada": prof}})
    try:
        h.chk("f_aplanar_nunca_lanza", all(aplanar_informe(x) is None for x in raros[:-1]))
        h.chk("f_validar_nunca_lanza", all(vf(o, x) and vf(o, x)[0] == "CF-01" for x in raros), [vf(o, x) for x in raros])
    except Exception as ex:   # noqa: BLE001
        h.chk("f_nunca_lanza", False, type(ex).__name__)

    # ================================================================ CT-G-14 0.2.0
    m = reg()
    h.chk("m_envoltura_comun", set(m) == {"event_id", "correlation_id", "expediente_id", "producer", "consumer", "tipo_mensaje", "version_esquema",
                                          "emitido_en", "valid_until", "data_refs", "payload"}
          and m["consumer"] == "G" and m["valid_until"] is None and m["data_refs"] == ["MAN-ORD-1", "MAN-STOP-1"]
          and (m["expediente_id"], m["correlation_id"]) == ("EXP-0001", "COR-0001"), m)
    h.chk("m_valida_en_contratos", ct.validar(m) == [] and ct.validar(libre()) == [], (ct.validar(m), ct.validar(libre())))
    h.chk("m_libre_sin_identidad", (libre()["expediente_id"], libre()["correlation_id"]) == (None, None) and libre()["data_refs"] == ["MAN-GBP-1"])
    ctx = {"ahora": T1, "expediente": None, "posicion": None, "tolerancia_precio": 0.05}
    for nombre, x, regla, ctr in (
            ("consumer_ajeno", {**m, "consumer": "ORQUESTADOR"}, "RM-01", "CT-03"),
            ("con_vigencia", {**m, "valid_until": "2026-11-07T00:00:00+00:00"}, "RM-01", "CT-03"),
            ("data_refs_desordenados", {**m, "data_refs": ["MAN-STOP-1", "MAN-ORD-1"]}, "RM-01", None),
            ("data_refs_sin_proteccion", {**m, "data_refs": ["MAN-ORD-1"]}, "RM-01", None),
            ("data_refs_ajenos", {**m, "data_refs": ["MAN-ORD-1", "OTRA"]}, "RM-01", None),
            ("campo_de_mas_en_payload", {**m, "payload": {**m["payload"], "x": 1}}, "RM-01", "CT-03"),
            ("campo_de_operacion_fuera_del_payload", {**m, "cantidad": 1.0}, "RM-01", "CT-03"),
            ("version_desconocida", {**m, "version_esquema": "0.3.0"}, "RM-01", "CT-02")):
        r = {f["regla"] for f in validar_manual(x, ctx)}
        c = ct.validar(x)
        h.chk(f"m_{nombre}_{regla.replace('-', '')}", r == {regla} and (ctr is None or (c and c[0]["regla"] == ctr)), (r, c))
    viejo = a_010_m(m)
    h.chk("m_010_RM01", [f["regla"] for f in validar_manual(viejo, ctx)] == ["RM-01"] and "retirada" in validar_manual(viejo, ctx)[0]["mensaje"])
    h.chk("m_010_contratos_CT02_y_historico", ct.validar(viejo)[0]["regla"] == "CT-02" and ct.validar(viejo, historico=True) == [],
          (ct.validar(viejo), ct.validar(viejo, historico=True)))
    h.chk("m_esquema_vinculado_sin_identidad_CT03", ct.validar({**m, "expediente_id": None, "correlation_id": None})[0]["regla"] == "CT-03")
    h.chk("m_esquema_libre_con_identidad_CT03", ct.validar({**libre(), "expediente_id": "EXP-0001", "correlation_id": "COR-0001"})[0]["regla"] == "CT-03")
    # RM-11 en el Orquestador
    for nombre, x in (("otra_correlacion", {**m, "correlation_id": "COR-0009"}), ("otro_expediente", {**m, "expediente_id": "EXP-0009"}),
                      ("libre_con_identidad", {**libre(), "expediente_id": "EXP-0001", "correlation_id": "COR-0001"}),
                      ("vinculado_sin_identidad", {**m, "expediente_id": None, "correlation_id": None})):
        o, b = autorizado(o=nuevo(L1))
        antes = estado(o)
        r = o.registrar_manual(x, T1)
        h.chk(f"m_{nombre}_RM11", r["codigo"] == "O-01" and "RM-11" in r.get("reglas", []) and estado(o) == antes, r)
    h.chk("m_RM11_sin_contexto_falla_cerrado", "RM-11" in {f["regla"] for f in validar_manual(m, {**ctx, "expediente": autorizado()[0].expedientes["EXP-0001"]})})
    # camino real: la consola construye el mensaje con contratos.registro_manual
    o, b = autorizado(o=nuevo(L1), b=vigilado())
    a_mano(b, "EURUSD", "COMPRA", 100.0, "MAN-ORD-1", stop=("MAN-STOP-1", 1.05))
    x = ct.registro_manual(o, reg()["payload"], "EV-MAN-0100", T1)
    h.chk("m_consola_deduce_identidad", (x["expediente_id"], x["correlation_id"]) == ("EXP-0001", o.expedientes["EXP-0001"]["correlation_id"])
          and ct.validar(x) == [], x)
    r = declarar_manual(o, x, b, T1)
    h.chk("m_consola_registro_aceptado", r["ok"] and o.posiciones[PID]["estado"] == "ABIERTA" and conciliar(o, b, T1)["ok"], r)
    h.chk("m_manuales_guarda_la_forma_plana", o.manuales and set(o.manuales[-1]) >= {"vinculo", "instrumento", "cantidad", "lado", "event_id",
                                                                                     "expediente_id", "correlation_id"}
          and "payload" not in o.manuales[-1], o.manuales)
    h.chk("m_mismo_event_id_otra_envoltura_O03", o.registrar_manual({**x, "emitido_en": "2026-11-06T09:04:00+00:00"}, T1)["codigo"] == "O-03")
    # cierre por posición: la identidad es la del expediente de la posición
    b.precios["EURUSD"] = 1.12
    for s in [k for k, v in b.ordenes.items() if v["estado"] == "ACEPTADA"]:
        b.cancelar(s)
    a_mano(b, "EURUSD", "VENTA", 100.0, "MAN-CIERRE-1")
    campos = sin(cambia(reg(), vinculo={"tipo": "POSICION", "id": PID}, lado="VENTA", ref_intermediario="MAN-CIERRE-1", precio=1.12, ejecutado_en=T1), "proteccion_ref")["payload"]
    y = ct.registro_manual(o, campos, "EV-MAN-0101", T1)
    h.chk("m_consola_posicion_identidad_del_expediente", (y["expediente_id"], y["correlation_id"]) == ("EXP-0001", "COR-0001") and y["data_refs"] == ["MAN-CIERRE-1"], y)
    r = declarar_manual(o, y, b, T1)
    h.chk("m_cierre_por_posicion_aceptado", r["ok"] and o.posiciones[PID]["estado"] == "CERRADA", r)
    h.chk("m_consola_vinculo_inexistente_sin_identidad", ct.registro_manual(o, {**campos, "vinculo": {"tipo": "POSICION", "id": "POS-X"}}, "EV-X", T1)["expediente_id"] is None)
    # G no consulta al intermediario por un mensaje mal envuelto
    o, b = autorizado(o=nuevo(L1), b=vigilado())
    a_mano(b, "EURUSD", "COMPRA", 100.0, "MAN-ORD-1", stop=("MAN-STOP-1", 1.05))
    for nombre, x in (("010", a_010_m(reg())), ("data_refs", {**reg(), "data_refs": []}), ("consumer", {**reg(), "consumer": "H"})):
        n0, antes = b.consultas, estado(o)
        r = declarar_manual(o, x, b, T1)
        h.chk(f"m_G_mal_envuelto_{nombre}_O01_sin_consultar", r["codigo"] == "O-01" and "RM-01" in r.get("reglas", []) and b.consultas == n0
              and estado(o) == antes, r)
    h.chk("m_G_bien_envuelto_si_consulta", declarar_manual(o, reg(), b, T1)["ok"] and b.consultas > 0)
    # nunca lanza
    raros = (None, [], {}, {**reg(), "payload": None}, {**reg(), "payload": {"vinculo": prof}}, {**reg(), "data_refs": None},
             {**reg(), "payload": {**reg()["payload"], "ref_intermediario": prof}})
    try:
        h.chk("m_aplanar_nunca_lanza", all(aplanar_manual(x) is None for x in raros[:-1]))
        h.chk("m_validar_nunca_lanza", all(validar_manual(x, ctx) and validar_manual(x, ctx)[0]["regla"] == "RM-01" for x in raros))
    except Exception as ex:   # noqa: BLE001
        h.chk("m_nunca_lanza", False, type(ex).__name__)
    h.chk("m_consola_campos_de_envoltura_en_payload_RM01", "RM-01" in {f["regla"] for f in validar_manual(
        ct.registro_manual(o, {**reg()["payload"], "event_id": "X"}, "EV-MAN-0200", T1), ctx)})
    h.chk("m_envolver_es_puro", envolver_manual({"ref_intermediario": "A"}, "E", T1) == envolver_manual({"ref_intermediario": "A"}, "E", T1))

    # ================================================================ regresiones de la revisión independiente
    # R1: G no consulta ni cancela el stop por un CT-G-14 que el Orquestador va a rechazar (RM-11, RM-02, RM-01)
    def abierta_a_mano():
        o_, b_ = autorizado(o=nuevo(L1), b=vigilado())
        a_mano(b_, "EURUSD", "COMPRA", 100.0, "MAN-ORD-1", stop=("MAN-STOP-1", 1.05))
        assert declarar_manual(o_, reg(), b_, T1)["ok"]
        a_mano(b_, "EURUSD", "VENTA", 100.0, "MAN-CIERRE-1")   # cierra a mano; el stop sigue en el intermediario
        return o_, b_
    cierre = sin(cambia(reg(), event_id="EV-MAN-0002", vinculo={"tipo": "POSICION", "id": PID}, lado="VENTA", ref_intermediario="MAN-CIERRE-1",
                        ejecutado_en=T1, precio=1.10), "proteccion_ref")
    for nombre, x, regla in (("correlacion_falsa", {**cierre, "correlation_id": "COR-0009"}, "RM-11"),
                             ("emisor_broker", {**cierre, "producer": "BROKER"}, "RM-02"),
                             ("motivo_en_blanco", cambia(cierre, motivo="   "), "RM-01"),
                             ("vinculo_con_clave_de_mas", cambia(cierre, vinculo={"tipo": "POSICION", "id": PID, "x": 1}), "RM-01"),
                             ("fecha_imposible", cambia(cierre, ejecutado_en="2026-02-30T09:00:00+00:00"), "RM-01")):
        o, b = abierta_a_mano()
        n0, stop0, antes = b.consultas, copy.deepcopy(b.ordenes.get("MAN-STOP-1")), estado(o)
        r = declarar_manual(o, x, b, T1)
        h.chk(f"R1_{nombre}_no_toca_el_intermediario_{regla.replace('-', '')}",
              r["codigo"] == "O-01" and regla in r.get("reglas", []) and b.consultas == n0 and b.ordenes.get("MAN-STOP-1") == stop0
              and estado(o) == antes and o.posiciones[PID]["estado"] == "ABIERTA", (r, b.consultas - n0))
    o, b = abierta_a_mano()
    r = declarar_manual(o, cierre, b, T1)
    h.chk("R1_el_cierre_correcto_si_cancela_y_cierra", r["ok"] and o.posiciones[PID]["estado"] == "CERRADA"
          and b.ordenes["MAN-STOP-1"]["estado"] != "ACEPTADA", r)
    # comprobar_manual no tiene efectos (ni reloj, ni eventos, ni kill)
    o, b = abierta_a_mano()
    antes = (estado(o), o.ultimo_ahora, o.kill)
    for x in (cierre, {**cierre, "correlation_id": "COR-0009"}, reg(), a_010_m(cierre), None, {**cierre, "payload": None}):
        o.comprobar_manual(x, "2026-11-06T10:00:00+00:00")
    h.chk("R1_comprobar_manual_sin_efectos", (estado(o), o.ultimo_ahora, o.kill) == antes)
    h.chk("R1_comprobar_manual_dice_lo_mismo", o.comprobar_manual(cierre, T1) is None
          and o.comprobar_manual({**cierre, "correlation_id": "COR-0009"}, T1)["codigo"] == "O-01"
          and o.comprobar_manual(reg(), T1)["codigo"] == "O-03"
          and o.comprobar_manual(cierre, "2026-11-01T00:00:00+00:00")["codigo"] == "O-00")
    # R2: validar_manual no lanza con fechas que solo tienen la forma
    for nombre, campo, valor in (("30_febrero", "ejecutado_en", "2026-02-30T09:00:00+00:00"), ("hora_25", "ejecutado_en", "2026-11-06T25:00:00+00:00"),
                                 ("desfase_25", "emitido_en", "2026-11-06T09:05:00+25:00")):
        try:
            f = validar_manual(cambia(libre(), **{campo: valor}), ctx)
            h.chk(f"R2_{nombre}_RM01_sin_lanzar", [x["regla"] for x in f] == ["RM-01"], f)
        except Exception as ex:   # noqa: BLE001
            h.chk(f"R2_{nombre}_RM01_sin_lanzar", False, type(ex).__name__)
    o, b = autorizado(o=nuevo(L1))
    r = o.registrar_manual(cambia(reg(), ejecutado_en="2026-02-30T09:00:00+00:00"), T1)
    h.chk("R2_orquestador_O01_no_O00", r["codigo"] == "O-01" and r.get("reglas") == ["RM-01"], r)
    h.chk("R2_contexto_roto_RM01_sin_lanzar", [x["regla"] for x in validar_manual(reg(), {"ahora": T1, "expediente": {"estado": "AUTORIZADA"}})] == ["RM-01"])
    # R3: la consola no lanza con campos mal formados (deja la identidad nula y el Orquestador rechaza)
    o, b = autorizado(o=nuevo(L1))
    for nombre, campos in (("vinculo_texto", {**reg()["payload"], "vinculo": "EXP-0001"}), ("vinculo_lista", {**reg()["payload"], "vinculo": []}),
                           ("id_lista", {**reg()["payload"], "vinculo": {"tipo": "EXPEDIENTE", "id": ["EXP-0001"]}}), ("campos_lista", []),
                           ("campos_nulos", None)):
        try:
            x = ct.registro_manual(o, campos, "EV-MAN-0300", T1)
            r = o.registrar_manual(x, T1)
            h.chk(f"R3_consola_{nombre}_sin_lanzar_y_rechazado", x["expediente_id"] is None and r["codigo"] == "O-01", r)
        except Exception as ex:   # noqa: BLE001
            h.chk(f"R3_consola_{nombre}_sin_lanzar_y_rechazado", False, type(ex).__name__)
    # R4: el motivo tiene una sola definición (Python y esquema dicen lo mismo)
    from manual_g import motivo_ok
    for i, mot in enumerate(("a\nb\nc", "a" * 500, "a" * 499 + " ", "a" * 501, "  ab  ", "ok\n", "abc", "   ", "a b", "ab", " \t x y z \n", "é€ñ")):
        x = cambia(libre(), motivo=mot)
        py = not any(f["regla"] == "RM-01" for f in validar_manual(x, ctx))
        es = ct.validar(x) == []
        h.chk(f"R4_motivo_{i}_misma_regla", py == es == motivo_ok(mot), (repr(mot[:12]), py, es))

    # ================================================================ registro
    reg_c = {c["tipo"]: c for c in ct.registro()["contratos"]}
    con = [c for c in reg_c.values() if c["estado"] == "ESQUEMA"]
    h.chk("registro_todos_con_envoltura_completa", all(c["envoltura"] == "COMPLETA" for c in con), {c["tipo"]: c["envoltura"] for c in con})
    h.chk("registro_una_vigente_por_contrato", all(sum(v["estado"] == "VIGENTE" for v in c["versiones"]) == 1
                                                   and next(v for v in c["versiones"] if v["estado"] == "VIGENTE")["version"] == c["version"] for c in con))
    h.chk("registro_08_y_14_en_020_con_la_010_retirada", all(reg_c[t]["version"] == "0.2.0" and [v["estado"] for v in reg_c[t]["versiones"]] == ["VIGENTE", "RETIRADA"]
                                                              for t in ("CT-G-08", "CT-G-14")))
    h.chk("registro_version_REG030", ct.registro()["version_registro"] == "REG-0.3.0")   # T-48 cambió CT-G-03

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO ENVOLTURA:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
