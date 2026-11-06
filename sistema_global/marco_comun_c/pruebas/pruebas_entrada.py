"""Pruebas de T-23: orden de entrada viva durante la ventana, parciales y estados de orden (Constitución §4.2)."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validador"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ejecucion_g import BrokerSimulado, cartera_para_f, conciliar, ejecutar, revisar_entrada  # noqa: E402
from vigilancia import vigilar  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_ejecucion_g import autorizado, broker  # noqa: E402
from pruebas_orquestador import AHORA, ENTRADA, SALIDA, Arnes, dim, hasta, nuevo  # noqa: E402

T1 = "2026-11-06T10:00:00+00:00"
T2 = "2026-11-06T11:00:00+00:00"
DESPUES_DE_F = "2026-11-07T10:00:00+00:00"   # el informe de F vence el 7 a las 09:00: fin de la vida de la orden
EID, OID, PID = "EXP-0001", "ORD-EXP-0001-E-1", "POS-EXP-0001"


def viva(**kw):
    """Autorizada con el precio por encima del límite (1,10): la orden de entrada queda viva."""
    o, b = autorizado(b=broker(precio=1.12, **kw))
    r = ejecutar(o, EID, b, AHORA)
    assert r["codigo"] == "G-11", r
    return o, b


def main():
    h = Arnes()
    # ---------------------------------------------------------------- viva y se ejecuta después
    o, b = viva()
    oe = o.expedientes[EID]["orden_entrada"]
    h.chk("queda_viva_y_anotada_ENVIADA", oe["estado"] == "ENVIADA" and b.consultar(OID)["estado"] == "ACEPTADA"
          and o.expedientes[EID]["estado"] == "AUTORIZADA" and o.posiciones == {}, oe)
    h.chk("reejecutar_revisa_y_no_envia_otra", ejecutar(o, EID, b, AHORA)["codigo"] == "G-11" and len(b.ordenes) == 1)
    h.chk("revisar_sin_novedad_sigue_viva_G11", revisar_entrada(o, EID, b, T1)["codigo"] == "G-11")
    b.mover_precio("EURUSD", 1.09, T1)
    v = vigilar(o, b, {"EURUSD": {"precio": 1.09, "hora": T1}}, T1)
    h.chk("H11_la_ejecucion_posterior_abre_y_protege", [a["regla"] for a in v["acciones"]][:1] == ["H-11"] and v["acciones"][0]["ok"]
          and o.posiciones[PID]["estado"] == "ABIERTA" and b.consultar("ORD-EXP-0001-S-1")["estado"] == "ACEPTADA" and v["conciliacion_ok"], v)
    oe = o.expedientes[EID]["orden_entrada"]
    h.chk("estados_de_la_orden_ENVIADA_EJECUTADA_CONCILIADA", [x["estado"] for x in oe["historial"]] == ["ENVIADA", "EJECUTADA", "CONCILIADA"]
          and o.integridad() == [], oe)
    # ---------------------------------------------------------------- ejecutada dentro de plazo, conocida después
    o, b = viva()
    b.mover_precio("EURUSD", 1.09, T1)
    r = revisar_entrada(o, EID, b, DESPUES_DE_F)
    h.chk("ejecutada_a_tiempo_y_revisada_tarde_se_acepta", r["ok"] and o.posiciones[PID]["estado"] == "ABIERTA", r)
    # ---------------------------------------------------------------- vence sin ejecutarse
    o, b = viva()
    late = "2026-11-08T13:00:00+00:00"
    br = o.barrer(late)
    h.chk("barrer_no_caduca_con_la_orden_viva_O25", o.expedientes[EID]["estado"] == "AUTORIZADA"
          and any(x["codigo"] == "O-25" for x in o.avisos) and ("aviso_entrada_viva", EID, "AUTORIZADA") in br["cambios"], br)
    h.chk("descartar_con_la_orden_viva_O25", o.descartar(EID, "ya no interesa", "OPERADOR", late)["codigo"] == "O-25")
    r = revisar_entrada(o, EID, b, late)
    h.chk("al_vencer_G_la_cancela_G02", r["codigo"] == "G-02" and b.consultar(OID)["estado"] == "CANCELADA"
          and o.expedientes[EID]["orden_entrada"]["estado"] == "CANCELADA", r)
    o.barrer(late)
    h.chk("y_entonces_el_expediente_caduca", o.expedientes[EID]["estado"] == "CADUCADA" and o.integridad() == [])
    h.chk("la_conciliacion_queda_limpia", conciliar(o, b, late)["ok"])
    # ---------------------------------------------------------------- parcial
    o, b = autorizado(b=broker(fraccion_fill=0.95))
    r = ejecutar(o, EID, b, AHORA)
    h.chk("parcial_inmediata_protege_lo_ejecutado", r["ok"] and r["cantidad"] == 95.0 and o.posiciones[PID]["cantidad"] == 95.0
          and b.consultar("ORD-EXP-0001-S-1")["cantidad"] == 95.0, r)
    h.chk("parcial_el_resto_se_cancela", b.consultar(OID)["estado"] == "CANCELADA" and b.consultar(OID)["cantidad_ejecutada"] == 95.0
          and [x["estado"] for x in o.expedientes[EID]["orden_entrada"]["historial"]] == ["ENVIADA", "PARCIAL", "CONCILIADA"])
    h.chk("parcial_concilia_limpio", conciliar(o, b, AHORA)["ok"])
    o, b = viva(fraccion_fill=0.95)
    b.mover_precio("EURUSD", 1.09, T1)
    r = revisar_entrada(o, EID, b, T1)
    h.chk("parcial_de_una_orden_viva", r["ok"] and o.posiciones[PID]["cantidad"] == 95.0 and b.consultar(OID)["estado"] == "CANCELADA", r)
    o, b = autorizado(b=broker(fraccion_fill=0.4))   # 40 x 1,10 = 44 €, por debajo del valor mínimo de F (100 €)
    r = ejecutar(o, EID, b, AHORA)
    h.chk("parcial_por_debajo_del_minimo_de_F_se_deshace_G05", r["codigo"] == "G-05" and r.get("cerrada") and b.posiciones() == [] and o.posiciones == {}, r)
    # ---------------------------------------------------------------- otros caminos
    o, b = autorizado(b=broker(precio=1.12))
    assert o.orden_entrada(EID, "ORD-PERDIDA", "ENVIADA", 0.0, "G", AHORA)["ok"]   # se anotó y el envío se perdió
    r = revisar_entrada(o, EID, b, T1)
    h.chk("orden_que_nunca_llego_se_anota_RECHAZADA", r["codigo"] == "G-02" and o.expedientes[EID]["orden_entrada"]["estado"] == "RECHAZADA", r)
    b.avanzar_reloj(T1)   # T-22: el precio que G da a F al reenviar es el del intermediario a esa hora
    h.chk("tras_rechazo_se_puede_reintentar", ejecutar(o, EID, b, T1)["codigo"] == "G-11"
          and o.expedientes[EID]["orden_entrada"]["anteriores"][0]["orden_id"] == "ORD-PERDIDA")
    o, b = viva()
    o.orden_entrada(EID, OID, "CANCELADA", 0.0, "G", T1)   # un G defectuoso la da por cancelada sin cancelarla
    c = conciliar(o, b, T1)
    h.chk("entrada_huerfana_se_detecta", "ENTRADA_HUERFANA" in [d["tipo"] for d in c["diferencias"]], c)
    o, b = viva()
    from pruebas_manual import reg
    h.chk("manual_con_orden_viva_O25", o.registrar_manual(reg(), T1)["codigo"] == "O-25")
    b.caido = True
    h.chk("revisar_sin_conexion_G01_y_sigue_viva", revisar_entrada(o, EID, b, T1)["codigo"] == "G-01"
          and o.expedientes[EID]["orden_entrada"]["estado"] == "ENVIADA")
    # nivel: autorización automática y cartera degradada -> no se envía nada
    o = nuevo({"matriz_autonomia": {"TACTICA": True}, "nivel_autonomia": {"TACTICA": "L2"}}); hasta(o, "PROPUESTA")
    b = broker()
    o.autorizar(EID, "MATRIZ_AUTONOMIA", informe_f(o, EID, n=1, cartera=cartera_para_f(b)), AHORA)
    o.degradar("TACTICA", "prueba", "G", AHORA)
    r = ejecutar(o, EID, b, AHORA)
    h.chk("degradada_no_se_envia_nada", r["codigo"] == "G-06" and b.ordenes == {}, r)
    # ---------------------------------------------------------------- revisión independiente de T-23
    from pruebas_ejecucion_g import CaeAlEnviarStop
    o, b = autorizado(b=CaeAlEnviarStop(100000.0, {"EURUSD": 1.12}, "2026-11-06T08:50:00+00:00", tipos_cambio={"USD": 1.0}))
    assert ejecutar(o, EID, b, AHORA)["codigo"] == "G-11"
    b.mover_precio("EURUSD", 1.09, T1)
    r = revisar_entrada(o, EID, b, T1)
    h.chk("cae_al_poner_el_stop_tras_ejecucion_tardia_G08", r["codigo"] == "G-08" and o.expedientes[EID]["orden_entrada"]["estado"] == "EJECUTADA"
          and any(x["codigo"] == "O-18" for x in o.avisos), r)
    b.caido, b.armado = False, False
    v = vigilar(o, b, {"EURUSD": {"precio": 1.09, "hora": DESPUES_DE_F}}, DESPUES_DE_F)
    h.chk("la_proteccion_se_reanuda_aunque_haya_vencido_el_plazo", v["acciones"][0]["regla"] == "H-11" and v["acciones"][0]["ok"]
          and o.posiciones[PID]["estado"] == "ABIERTA" and b.consultar("ORD-EXP-0001-S-1")["estado"] == "ACEPTADA"
          and o.posiciones[PID]["ejecutada_en"] == T1, v)
    o, b = autorizado(b=broker(fraccion_fill=0.4))
    r1, r2_, r3 = ejecutar(o, EID, b, AHORA), ejecutar(o, EID, b, AHORA), ejecutar(o, EID, b, AHORA)
    h.chk("reintentos_tras_deshacer_nunca_dejan_posicion", [x["codigo"] for x in (r1, r2_, r3)] == ["G-05"] * 3 and b.posiciones() == []
          and [x["estado"] for x in o.expedientes[EID]["orden_entrada"]["anteriores"]] == ["DESHECHA", "DESHECHA"], (r1, r2_, r3))
    o = nuevo({"matriz_autonomia": {"TACTICA": True}, "nivel_autonomia": {"TACTICA": "L2"}}); hasta(o, "PROPUESTA")
    b = broker(precio=1.12)
    o.autorizar(EID, "MATRIZ_AUTONOMIA", informe_f(o, EID, n=1, cartera=cartera_para_f(b)), AHORA)
    assert ejecutar(o, EID, b, AHORA)["codigo"] == "G-11"
    o.degradar("TACTICA", "prueba", "G", T1)
    r = revisar_entrada(o, EID, b, T1)
    h.chk("degradar_cancela_la_orden_viva", r["codigo"] == "G-02" and b.consultar(OID)["estado"] == "CANCELADA", r)
    o = nuevo({"nivel_autonomia": {"TACTICA": "L2"}}); hasta(o, "AUTORIZADA")
    b = broker(precio=1.12); assert ejecutar(o, EID, b, AHORA)["codigo"] == "G-11"
    b.mover_precio("EURUSD", 1.09, T1)
    c = conciliar(o, b, T1)
    h.chk("conciliar_antes_de_revisar_no_degrada", c["ok"] and [x["tipo"] for x in c["explicadas"]] == ["ENTRADA_EN_CURSO"] and not o.degradadas, c)
    o, b = viva()
    b.avanzar_reloj("2026-11-07T09:30:00+00:00")
    h.chk("la_orden_caduca_en_el_intermediario_aunque_G_no_vuelva", b.consultar(OID)["estado"] == "CANCELADA")
    h.chk("y_G_lo_anota_al_volver", revisar_entrada(o, EID, b, "2026-11-07T09:30:00+00:00")["codigo"] == "G-02"
          and o.expedientes[EID]["orden_entrada"]["estado"] == "CANCELADA")
    o, b = viva()
    from ejecucion_g import cancelar_entrada
    r = cancelar_entrada(o, EID, b, T1)
    h.chk("cancelar_a_peticion", r["codigo"] == "G-02" and b.consultar(OID)["estado"] == "CANCELADA" and o.descartar(EID, "ya no", "OPERADOR", T1)["ok"], r)

    class PierdeElEnvio(BrokerSimulado):
        perdido = None

        def enviar(self, o_):
            if o_.get("tipo") == "LIMITE" and self.perdido is None:
                self.perdido = o_
                raise __import__("ejecucion_g").ConexionPerdida("se perdió el envío")
            return super().enviar(o_)
    o, b = autorizado(b=PierdeElEnvio(100000.0, {"EURUSD": 1.12}, "2026-11-06T08:50:00+00:00", tipos_cambio={"USD": 1.0}))
    h.chk("envio_perdido_G08", ejecutar(o, EID, b, AHORA)["codigo"] == "G-08")
    h.chk("envio_perdido_se_anota_rechazado", revisar_entrada(o, EID, b, T1)["codigo"] == "G-02" and o.expedientes[EID]["orden_entrada"]["estado"] == "RECHAZADA")
    BrokerSimulado.enviar(b, b.perdido)   # la orden perdida llega tarde al intermediario
    b.avanzar_reloj(T1)
    r = ejecutar(o, EID, b, T1)
    h.chk("el_reintento_usa_otro_id_y_cancela_el_perdido", r["codigo"] == "G-11" and b.consultar(OID)["estado"] == "CANCELADA"
          and o.expedientes[EID]["orden_entrada"]["orden_id"] == "ORD-EXP-0001-E-2", r)
    o, b = autorizado()
    assert o.orden_entrada(EID, "A-1", "ENVIADA", 0.0, "G", AHORA)["ok"]
    h.chk("cancelada_con_cantidad_O01", o.orden_entrada(EID, "A-1", "CANCELADA", 60.0, "G", AHORA)["codigo"] == "O-01")
    assert o.orden_entrada(EID, "A-1", "EJECUTADA", 100.0, "G", AHORA)["ok"]
    h.chk("nuevo_intento_sin_deshacer_O03", o.orden_entrada(EID, "A-2", "ENVIADA", 0.0, "G", AHORA)["codigo"] == "O-03")
    h.chk("deshecha_con_otra_cantidad_O01", o.orden_entrada(EID, "A-1", "DESHECHA", 50.0, "G", AHORA)["codigo"] == "O-01")
    assert o.orden_entrada(EID, "A-1", "DESHECHA", 100.0, "G", AHORA)["ok"]
    h.chk("reusar_el_id_deshecho_se_rechaza", o.orden_entrada(EID, "A-1", "ENVIADA", 0.0, "G", AHORA)["codigo"] in ("O-03", "O-04"))
    assert o.orden_entrada(EID, "A-2", "ENVIADA", 0.0, "G", AHORA)["ok"] and o.orden_entrada(EID, "A-2", "CANCELADA", 0.0, "G", AHORA)["ok"]
    h.chk("reusar_un_id_de_anteriores_O03", o.orden_entrada(EID, "A-1", "ENVIADA", 0.0, "G", AHORA)["codigo"] == "O-03")
    # ---------------------------------------------------------------- Orquestador.orden_entrada
    o, b = autorizado()
    h.chk("solo_G_anota_O05", o.orden_entrada(EID, "X-1", "ENVIADA", 0.0, "H", AHORA)["codigo"] == "O-05")
    h.chk("enviada_con_cantidad_O01", o.orden_entrada(EID, "X-1", "ENVIADA", 5.0, "G", AHORA)["codigo"] == "O-01")
    h.chk("ejecutada_sin_enviar_O04", o.orden_entrada(EID, "X-1", "EJECUTADA", 5.0, "G", AHORA)["codigo"] == "O-04")
    assert o.orden_entrada(EID, "X-1", "ENVIADA", 0.0, "G", AHORA)["ok"]
    h.chk("duplicado_O02", o.orden_entrada(EID, "X-1", "ENVIADA", 0.0, "G", AHORA)["codigo"] == "O-02")
    h.chk("otra_orden_mientras_vive_O03", o.orden_entrada(EID, "X-2", "ENVIADA", 0.0, "G", AHORA)["codigo"] == "O-03")
    h.chk("mas_de_lo_aprobado_O01", o.orden_entrada(EID, "X-1", "EJECUTADA", 1e9, "G", AHORA)["codigo"] == "O-01")
    h.chk("ejecutada_con_cero_O01", o.orden_entrada(EID, "X-1", "EJECUTADA", 0.0, "G", AHORA)["codigo"] == "O-01")
    assert o.orden_entrada(EID, "X-1", "EJECUTADA", 100.0, "G", AHORA)["ok"]
    h.chk("de_ejecutada_a_cancelada_O04", o.orden_entrada(EID, "X-1", "CANCELADA", 100.0, "G", AHORA)["codigo"] == "O-04")
    ORD = {"orden_id": "X-1", "cantidad": 100.0, "precio": 1.1, "conciliada": True, "proteccion_orden_ids": ["X-1-S"]}
    h.chk("ejecucion_con_otra_cantidad_O06", o.ejecutar(EID, {**ORD, "cantidad": 90.0}, "G", AHORA)["codigo"] == "O-06")
    h.chk("ejecucion_con_otra_orden_O06", o.ejecutar(EID, {**ORD, "orden_id": "X-9"}, "G", AHORA)["codigo"] == "O-06")
    h.chk("ejecutada_en_futuro_O01", o.ejecutar(EID, {**ORD, "ejecutada_en": T2}, "G", AHORA)["codigo"] == "O-01")
    h.chk("ejecutada_antes_de_enviar_O01", o.ejecutar(EID, {**ORD, "ejecutada_en": "2026-11-06T08:00:00+00:00"}, "G", AHORA)["codigo"] == "O-01")
    o2 = copy.deepcopy(o)
    o2.expedientes[EID]["orden_entrada"]["cantidad_ejecutada"] = 50.0   # alteración a mano
    h.chk("orden_alterada_O13", o2.ejecutar(EID, {**ORD, "cantidad": 50.0}, "G", AHORA)["codigo"] == "O-13" and o2.integridad() == [f"EXP:{EID}"])
    h.chk("la_que_corresponde_se_acepta", o.ejecutar(EID, ORD, "G", AHORA)["ok"] and o.expedientes[EID]["orden_entrada"]["estado"] == "CONCILIADA"
          and o.integridad() == [])
    # resto_parcial
    o = nuevo(); hasta(o, "COMPARADA")
    r = o.proponer(EID, {**ENTRADA, "resto_parcial": "CONTINUAR"}, SALIDA, "GESTOR_TACTICA", AHORA, dim(o))
    h.chk("resto_parcial_continuar_no_admitido_O01", r["codigo"] == "O-01", r)
    h.chk("resto_parcial_cancelar_OK", o.proponer(EID, {**ENTRADA, "resto_parcial": "CANCELAR"}, SALIDA, "GESTOR_TACTICA", AHORA, dim(o))["ok"])
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO ENTRADA:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
