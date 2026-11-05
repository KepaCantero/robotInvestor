"""Pruebas de la degradación por cartera y por sello caducado (T-29). Datos SIMULADOS.

Comprueba: una discrepancia degrada solo la cartera de su posición, expediente o instrumento; lo que no se puede atribuir y el
kill-switch degradan todas; restablecer una cartera exige acusar solo los avisos que le afectan; un sello caducado con
candidatos en juego degrada su cartera en el barrido; la matriz no autoriza con un sello que ya no está vigente.

Uso: python3 pruebas/pruebas_degradacion.py
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from ejecucion_g import ejecutar  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_ejecucion_g import autorizado  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, hasta, nuevo  # noqa: E402
from pruebas_propuesta import validar_con  # noqa: E402

TODAS = {"TRADING", "TACTICA", "LARGO_PLAZO"}
LUNES = "2026-11-09T09:00:00+00:00"   # el sello del jueves 5 ya no vale para TACTICA (1 día hábil); sí para LARGO_PLAZO (5)


def broker_alto():
    from pruebas_ejecucion_g import broker
    return broker(precio=1.12)   # por encima del límite: la orden de entrada queda viva


def dif(tipo, ref):
    return [{"tipo": tipo, "ref": ref, "detalle": "prueba"}]


def acusar(o, cartera, ahora=AHORA):
    for x in o.avisos:
        if x["acuse"] is None and x["codigo"] in ("O-18", "O-19") and (not o._carteras_de(x["ref"]) or cartera in o._carteras_de(x["ref"])):
            assert o.acusar_aviso(x["id"], "OPERADOR", ahora)["ok"]


def main():
    h = Arnes()
    # ------------------------------------------------------------ atribución de una discrepancia
    o, b = autorizado()
    ejecutar(o, "EXP-0001", b, AHORA)
    pid = "POS-EXP-0001"
    for nombre, ref, esperadas in (("posicion", pid, {"TACTICA"}), ("expediente", "EXP-0001", {"TACTICA"}),
                                   ("instrumento_con_posicion", "EURUSD", {"TACTICA"}), ("instrumento_escrito_de_otra_forma", "EUR/USD", {"TACTICA"}),
                                   ("cartera", "TACTICA", {"TACTICA"}), ("sin_referencia", None, TODAS),
                                   ("instrumento_desconocido", "XAUUSD", TODAS), ("basura", 7, TODAS)):
        o.degradadas.clear()
        r = o.reportar_discrepancia(dif("ESTADO_INCIERTO", ref), "G", AHORA)
        h.chk(f"discrepancia_por_{nombre}", r["ok"] and set(o.degradadas) == esperadas, (r, sorted(o.degradadas)))
    o.degradadas.clear()
    o.reportar_discrepancia(dif("ESTADO_INCIERTO", pid) + dif("SIN_CONEXION", None), "G", AHORA)
    h.chk("si_una_no_se_puede_atribuir_todas", set(o.degradadas) == TODAS)
    o.degradadas.clear()
    o.reportar_discrepancia(dif("CANTIDAD", pid), "G", AHORA)
    h.chk("discrepancia_grave_kill_y_todas", o.kill is not None and set(o.degradadas) == TODAS)

    # ------------------------------------------------------------ restablecer: solo los avisos de esa cartera
    o = nuevo()
    o.detectar("EXP-0011", "COR-0011", "DISCRECIONAL", "TRADING", "GESTOR_TRADING", AHORA)
    o.detectar("EXP-0012", "COR-0012", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    o.reportar_discrepancia(dif("ESTADO_INCIERTO", "EXP-0011"), "G", AHORA)
    o.reportar_discrepancia(dif("ESTADO_INCIERTO", "EXP-0012"), "G", AHORA)
    h.chk("cada_discrepancia_degrada_su_cartera", set(o.degradadas) == {"TRADING", "TACTICA"} and o.nivel("LARGO_PLAZO") == "L2")
    r = o.restablecer_nivel("TACTICA", "OPERADOR", AHORA)
    h.chk("sin_acusar_no_se_restablece_O06", r["codigo"] == "O-06", r)
    acusar(o, "TACTICA")
    r = o.restablecer_nivel("TACTICA", "OPERADOR", AHORA)
    h.chk("acusados_los_suyos_se_restablece_aunque_otra_tenga_pendientes", r["ok"] and o.nivel("TACTICA") == "L2" and o.nivel("TRADING") == "L1", r)
    h.chk("la_otra_sigue_esperando_sus_acuses", o.restablecer_nivel("TRADING", "OPERADOR", AHORA)["codigo"] == "O-06")
    o.reportar_discrepancia(dif("SIN_CONEXION", None), "G", AHORA)
    h.chk("aviso_sin_atribuir_bloquea_a_todas", o.restablecer_nivel("TACTICA", "OPERADOR", AHORA)["codigo"] == "O-06")

    # ------------------------------------------------------------ H: dato viejo solo en su cartera (ya existía)
    from vigilancia import vigilar
    o, b = autorizado()
    ejecutar(o, "EXP-0001", b, AHORA)
    vigilar(o, b, {}, "2026-11-06T09:05:00+00:00")
    h.chk("dato_viejo_degrada_solo_su_cartera", set(o.degradadas) == {"TACTICA"})

    # ------------------------------------------------------------ sello caducado con candidatos en juego
    o = nuevo()
    validar_con(o, 1, valid_until="2026-11-10T18:00:00+00:00")
    r = o.barrer("2026-11-06T12:00:00+00:00")
    h.chk("sello_vigente_no_degrada", r["ok"] and not o.degradadas, (r, o.degradadas))
    r = o.barrer(LUNES)
    h.chk("sello_caducado_con_candidato_en_juego_degrada_su_cartera", set(o.degradadas) == {"TACTICA"}
          and any(c[0] == "degradada" and c[1] == "TACTICA" for c in r["cambios"])
          and any(x["codigo"] == "O-19" and x["ref"] == "TACTICA" for x in o.avisos), (r, o.degradadas))
    o = nuevo()
    r = o.barrer(LUNES)
    h.chk("sello_caducado_sin_candidatos_no_degrada", not o.degradadas, r)
    o = nuevo()
    validar_con(o, 1, valid_until="2026-11-10T18:00:00+00:00")
    o.descartar("EXP-0001", "ya no", "OPERADOR", AHORA)
    o.barrer(LUNES)
    h.chk("candidato_descartado_no_cuenta", not o.degradadas)

    # ------------------------------------------------------------ la matriz no autoriza con un sello que ya no vale
    cfg = {"matriz_autonomia": {"TACTICA": True}}
    o = nuevo(cfg)
    hasta(o, "PROPUESTA")
    inf = informe_f(o, "EXP-0001", 1)
    import copy
    o2 = copy.deepcopy(o)
    r = o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", inf, AHORA)
    h.chk("control_la_matriz_autoriza_con_sello_vigente", r["ok"], r)
    from validar_sobre import _dt
    e = o2.expedientes["EXP-0001"]
    h.chk("el_sello_del_jueves_no_vale_el_lunes_para_TACTICA", not o2._sello_vigente_para(e, _dt(LUNES)) and o2._sello_vigente_para(e, _dt(AHORA)))
    # el lunes la propuesta y el informe ya habrían vencido; se prueba la regla en el instante en que el sello deja de valer
    import orquestador as orq
    original = orq.estado_sello
    orq.estado_sello = lambda s, f, c, cal: "CADUCADO"   # el sello deja de estar vigente (K lo marcaría así al día siguiente)
    try:
        r = o2.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", inf, AHORA)
    finally:
        orq.estado_sello = original
    h.chk("la_matriz_no_autoriza_con_sello_caducado_O10", r["codigo"] == "O-10" and "sello" in r["motivo"] and o2.expedientes["EXP-0001"]["estado"] == "PROPUESTA", r)
    h.chk("y_la_cartera_queda_degradada", o2.nivel("TACTICA") == "L1")
    orq.estado_sello = lambda s, f, c, cal: "CADUCADO"
    try:
        from pruebas_orquestador import autorizar_op
        r = autorizar_op(o2, "EXP-0001", inf, AHORA)
    finally:
        orq.estado_sello = original
    h.chk("el_operador_si_puede_autorizar_sabiendolo", r["ok"], r)

    # ------------------------------------------------------------ revisión independiente (regresiones)
    from ejecucion_g import BrokerSimulado, conciliar
    from pruebas_ejecucion_g import HORA_DATOS
    # G1: una orden de entrada viva con el sello caducado también degrada, y la ejecución automática se frena
    o, b = autorizado(b=broker_alto())
    r0 = ejecutar(o, "EXP-0001", b, AHORA)   # la orden límite queda viva (G-11)
    orq.estado_sello = lambda s_, f, c, cal: "CADUCADO"
    try:
        r = o.barrer("2026-11-06T09:30:00+00:00")
    finally:
        orq.estado_sello = original
    h.chk("G1_entrada_viva_con_sello_caducado_degrada", r0["codigo"] == "G-11" and o.nivel("TACTICA") == "L1", (r0, r, o.degradadas))
    # G2: no poder conciliar se informa y degrada; lo ya encontrado conserva su gravedad
    o, b = autorizado()
    ejecutar(o, "EXP-0001", b, AHORA)
    b.caido = True
    c = conciliar(o, b, "2026-11-06T09:05:00+00:00")
    h.chk("G2_sin_conexion_degrada_todas_y_avisa", not c["ok"] and set(o.degradadas) == TODAS and any("SIN_CONEXION" in x["motivo"] for x in o.avisos), c)
    class FallaTarde(BrokerSimulado):
        armado = False
        def consultar(self, oid):
            if self.armado and "-C-" in oid:   # falla después de revisar los stops
                raise TimeoutError("lento")
            return super().consultar(oid)
    o, b = autorizado(b=FallaTarde(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0}))
    ejecutar(o, "EXP-0001", b, AHORA)
    b.cancelar("ORD-EXP-0001-S-1")   # la posición se queda sin stop y luego la conciliación falla a medias
    b.armado = True
    c = conciliar(o, b, "2026-11-06T09:05:00+00:00")
    h.chk("G2_lo_hallado_antes_del_fallo_cuenta_kill", any(d["tipo"] == "PROTECCION" for d in c["diferencias"]) and o.kill is not None, c)
    # G3: ids que se hacen pasar por otra cosa
    o = nuevo()
    for i in ("TRADING", "POS-EXP-0001", "POS-X"):
        h.chk(f"G3_no_se_crea_un_expediente_llamado_{i}", o.detectar(i, "COR-1", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["codigo"] == "O-01")
    o = nuevo()
    o.detectar("EXP-0011", "COR-0011", "DISCRECIONAL", "TRADING", "GESTOR_TRADING", AHORA)
    o.expedientes["TACTICA"] = o.expedientes["EXP-0011"]   # aunque existiera por otra vía, una referencia ambigua degrada todas
    o.reportar_discrepancia(dif("ESTADO_INCIERTO", "TACTICA"), "G", AHORA)
    h.chk("G3_referencia_ambigua_degrada_todas", set(o.degradadas) == TODAS)
    # M1: el sello que K da por vigente para LARGO_PLAZO no la degrada
    o = nuevo()
    o.detectar("EXP-0021", "COR-0021", "DISCRECIONAL", "LARGO_PLAZO", "GESTOR_LARGO_PLAZO", AHORA)
    from validar_sobre import _dt as _dt1
    x = o.expedientes["EXP-0021"]
    x["encargo_actual"] = None
    o.sellos[next(iter(o.sellos))]["estado"] = "CADUCADO"   # lo marcó así barrer, por la antigüedad de su cartera (TACTICA)
    o.encargos["ENC-LP"] = {"sello_ref": next(iter(o.sellos))}
    x["encargo_actual"] = "ENC-LP"
    h.chk("M1_vigente_para_LARGO_PLAZO_aunque_caducara_para_TACTICA", o._sello_vigente_para(x, _dt1(LUNES)))
    # M2: no se reclasifica una posición con avisos de su cartera sin acusar
    o, b = autorizado()
    ejecutar(o, "EXP-0001", b, AHORA)
    o.reportar_discrepancia(dif("ORDEN_VIVA", "POS-EXP-0001"), "G", AHORA)
    r = o.reclasificar("POS-EXP-0001", "TRADING", "OPERADOR", "cambio de mandato", AHORA)
    h.chk("M2_reclasificar_con_la_cartera_degradada_O06", r["codigo"] == "O-06" and o.posiciones["POS-EXP-0001"]["cartera"] == "TACTICA", r)
    av = next(x for x in o.avisos if x["codigo"] == "O-18")
    h.chk("M2_el_aviso_guarda_su_cartera", av["carteras"] == ["TACTICA"], av)
    # M3: una posición alterada no decide qué cartera se degrada
    for valor in ("LARGO_PLAZO", "CARTERA-X"):
        o, b = autorizado()
        ejecutar(o, "EXP-0001", b, AHORA)
        o.posiciones["POS-EXP-0001"]["cartera"] = valor
        o.reportar_discrepancia(dif("ESTADO_INCIERTO", "POS-EXP-0001"), "G", AHORA)
        h.chk(f"M3_posicion_alterada_a_{valor}_degrada_todas", set(o.degradadas) == TODAS)
    o, b = autorizado()
    ejecutar(o, "EXP-0001", b, AHORA)
    o.posiciones["POS-EXP-0001"]["cartera"] = "LARGO_PLAZO"
    vigilar(o, b, {"EURUSD": {"precio": 1.10, "hora": "2026-11-06T09:05:00+00:00"}}, "2026-11-06T09:05:00+00:00")
    h.chk("M3_integridad_rota_activa_el_kill_switch", o.kill is not None and "INTEGRIDAD" in o.kill["motivo"])
    # m1: no se acusa ni se restablece antes de la degradación
    o = nuevo()
    o.detectar("EXP-0031", "COR-0031", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    o.reportar_discrepancia(dif("ESTADO_INCIERTO", "EXP-0031"), "G", "2026-11-06T12:00:00+00:00")
    o.ultimo_ahora = AHORA   # como tras un rechazo que degradó con un instante posterior
    av = next(x for x in o.avisos if x["codigo"] == "O-19")
    h.chk("m1_acuse_anterior_al_aviso_O16", o.acusar_aviso(av["id"], "OPERADOR", "2026-11-06T10:00:00+00:00")["codigo"] == "O-16")
    h.chk("m1_restablecer_anterior_a_la_degradacion_O16", o.restablecer_nivel("TACTICA", "OPERADOR", "2026-11-06T10:00:00+00:00")["codigo"] in ("O-16", "O-06"))

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO DEGRADACION:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
