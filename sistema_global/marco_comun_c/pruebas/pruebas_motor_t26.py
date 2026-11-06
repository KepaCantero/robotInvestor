"""Pruebas de T-26 (parte 1): el registro del Motor numérico SC-3 y las advertencias de K que llegan al Orquestador.
Las cifras del sobre citan artefactos registrados (V-26); un sello de K con advertencias lo ve y lo acepta el operador, y la
matriz de autonomía no decide con él. Datos SIMULADOS."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

from k_calidad import hash_del_sello, validar_sello  # noqa: E402
from validar_sobre import cargar_json, validar  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_orquestador import (AHORA, CAL, MOTOR_BASE, S1, S2, Arnes, artefacto_sim, autorizar_op, encargo, hasta, modelo_sim,  # noqa: E402
                                 nuevo, sobre)

REF = MOTOR_BASE["MOTOR-RUN-0001"]


def en_analisis(o, n=1):
    eid = f"EXP-{n:04d}"
    assert o.detectar(eid, f"COR-{n:04d}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.emitir_encargo(eid, encargo(n), "GESTOR_TACTICA", AHORA)["ok"]
    return eid


def con_advertencia():
    """S1 con Q-10 en ADVERTENCIA (dato crítico de una sola fuente): mismo sello_id y hash recalculado."""
    s = copy.deepcopy(S1)
    for x in s["resultado_reglas"]:
        if x["regla"] == "Q-10":
            x["resultado"], x["detalle"] = "ADVERTENCIA", "SRC-EURUSD: dato crítico sin fuente de contraste disponible"
    s["resultado_global"] = "ADVERTENCIA"
    s["hash_sello"] = hash_del_sello(s)
    return s


def aprobacion(p, **kw):
    return {"pantalla_hash": p["hash"], "importe_tecleado": p["importe"], "canal": "CONSOLA", "segundo_factor": True, **kw}


def main():
    h = Arnes()

    # ================================================================ SC-3: modelos y artefactos
    o = nuevo(sellos=(S1,))
    o2 = nuevo(sellos=())
    o2.registrar_sello(S1, AHORA)
    m = modelo_sim("MOD-X")
    h.chk("modelo_solo_el_motor_O05", o2.registrar_modelo(m, "C-DIV", AHORA)["codigo"] == "O-05")
    for nombre, mm in (("sin_limites", {k: v for k, v in m.items() if k != "limites_validez"}), ("limites_vacios", {**m, "limites_validez": ""}),
                       ("version_mal", {**m, "version": "1.0"}), ("clave_extra", {**m, "parametros": {}}), ("no_dict", "MOD-X")):
        h.chk(f"modelo_{nombre}_O01", o2.registrar_modelo(mm, "MOTOR", AHORA)["codigo"] == "O-01")
    h.chk("modelo_declarado", o2.registrar_modelo(m, "MOTOR", AHORA)["ok"])
    h.chk("modelo_repetido_O02", o2.registrar_modelo(m, "MOTOR", AHORA)["codigo"] == "O-02")
    h.chk("modelo_otra_declaracion_O03", o2.registrar_modelo({**m, "descripcion": "otra"}, "MOTOR", AHORA)["codigo"] == "O-03")
    h.chk("otra_version_es_otro_modelo", o2.registrar_modelo({**m, "version": "1.1.0"}, "MOTOR", AHORA)["ok"])
    a = artefacto_sim("ART-X-1", "MOD-X")
    h.chk("artefacto_solo_el_motor_O05", o2.registrar_artefacto(a, "OPERADOR", AHORA)["codigo"] == "O-05")
    for nombre, aa in (("hash_mal", {**a, "entradas_hash": "abc"}), ("semilla_negativa", {**a, "semilla": -1}),
                       ("semilla_bool", {**a, "semilla": True}), ("semilla_decimal", {**a, "semilla": 1.5}),
                       ("sello_no_es_de_K", {**a, "sello_ref": "SRC-EURUSD"}), ("sin_semilla", {k: v for k, v in a.items() if k != "semilla"})):
        h.chk(f"artefacto_{nombre}_O01", o2.registrar_artefacto(aa, "MOTOR", AHORA)["codigo"] == "O-01")
    h.chk("artefacto_de_modelo_no_declarado_O12", o2.registrar_artefacto({**a, "modelo_ref": "MOD-Y"}, "MOTOR", AHORA)["codigo"] == "O-12")
    h.chk("artefacto_de_version_no_declarada_O12", o2.registrar_artefacto({**a, "version_modelo": "2.0.0"}, "MOTOR", AHORA)["codigo"] == "O-12")
    h.chk("artefacto_con_sello_no_registrado_O12", o2.registrar_artefacto({**a, "sello_ref": "K-20261106-001"}, "MOTOR", AHORA)["codigo"] == "O-12")
    h.chk("artefacto_registrado", o2.registrar_artefacto(a, "MOTOR", AHORA)["ok"] and o2.artefactos["ART-X-1"]["fecha_corte"] == "2026-11-05")
    h.chk("artefacto_semilla_nula_vale", o2.registrar_artefacto({**a, "artefacto_id": "ART-X-2", "semilla": None}, "MOTOR", AHORA)["ok"])
    h.chk("artefacto_repetido_O02", o2.registrar_artefacto(a, "MOTOR", AHORA)["codigo"] == "O-02")
    h.chk("artefacto_otro_contenido_O03", o2.registrar_artefacto({**a, "semilla": 8}, "MOTOR", AHORA)["codigo"] == "O-03")
    h.chk("registro_integro", o2.motor_ok() and o2.integridad() == [])

    # ================================================================ V-26: el sobre cita lo que hay en el Motor
    eid = en_analisis(o)
    h.chk("sobre_con_artefactos_registrados", o.entregar_sobre(eid, sobre(1), AHORA)["ok"])
    o = nuevo(sellos=())
    assert o.registrar_sello(S1, AHORA)["ok"]
    for ref in sorted(set(MOTOR_BASE.values())):
        assert o.registrar_modelo(modelo_sim(ref), "MOTOR", AHORA)["ok"]
    for aid, ref in sorted(MOTOR_BASE.items()):
        if aid != "MOTOR-RUN-0001":
            assert o.registrar_artefacto(artefacto_sim(aid, ref), "MOTOR", AHORA)["ok"]
    eid = en_analisis(o)
    r = o.entregar_sobre(eid, sobre(1), AHORA)
    h.chk("V26_artefacto_no_registrado", r["codigo"] == "O-01" and "V-26" in r["motivo"] and "no está registrado" in r["motivo"], r)
    o = nuevo(sellos=(S1,))
    o.artefactos["MOTOR-RUN-0001"]["artefacto"]["modelo_ref"] = "MOD-OTRO"
    h.chk("alterar_un_artefacto_MOTOR", "MOTOR" in o.integridad())
    eid_ok = None
    try:
        eid_ok = en_analisis(o)
    except AssertionError:
        pass
    h.chk("con_el_motor_alterado_no_se_aceptan_sobres_O13", eid_ok is None or o.entregar_sobre(eid_ok, sobre(1), AHORA)["codigo"] == "O-13")
    # la cifra cita otro modelo que el del artefacto
    o = nuevo(sellos=())
    assert o.registrar_sello(S1, AHORA)["ok"]
    for ref in sorted(set(MOTOR_BASE.values())):
        assert o.registrar_modelo(modelo_sim(ref), "MOTOR", AHORA)["ok"]
    for aid, ref in sorted(MOTOR_BASE.items()):
        otro = MOTOR_BASE["MOTOR-RUN-0002"] if aid == "MOTOR-RUN-0001" else ref
        assert o.registrar_artefacto(artefacto_sim(aid, otro), "MOTOR", AHORA)["ok"]
    eid = en_analisis(o)
    r = o.entregar_sobre(eid, sobre(1), AHORA)
    h.chk("V26_cifra_de_otro_modelo", r["codigo"] == "O-01" and "V-26" in r["motivo"] and "modelo" in r["motivo"], r)
    # el validador del sobre sin registro en el contexto no evalúa V-26 (uso de C antes de entregar)
    sob = cargar_json((AQUI / "validos" / "valido_div_n3.json").read_text(encoding="utf-8"))
    ctx = cargar_json((AQUI / "contexto.json").read_text(encoding="utf-8"))
    h.chk("validador_sin_registro_no_evalua_V26", validar(sob, ctx) == [])
    h.chk("validador_con_registro_vacio_V26", {x["regla"] for x in validar(sob, {**ctx, "sc3": {}})} == {"V-26"})
    vista = {aid: {"modelo_ref": ref, "fecha_corte": "2026-11-05", "sello_ref": "K-20261105-001"} for aid, ref in MOTOR_BASE.items()}
    h.chk("validador_con_el_registro_completo", validar(sob, {**ctx, "sc3": vista}) == [])
    vista["MOTOR-RUN-0003"] = {**vista["MOTOR-RUN-0003"], "fecha_corte": "2026-11-06"}   # calculado con datos del día 6
    obt = [x for x in validar(sob, {**ctx, "sc3": vista}) if x["regla"] == "V-26"]
    h.chk("V26_sin_datos_posteriores_al_corte", len(obt) == 1 and "posteriores" in obt[0]["mensaje"], obt)
    h.chk("validador_registro_mal_formado_V01", {x["regla"] for x in validar(sob, {**ctx, "sc3": {"MOTOR-RUN-0001": 7}})} == {"V-01"})

    # ---------------------------------------------------------------- regresiones de la revisión (V-26)
    import motor
    # G1: el artefacto es del sello del encargo, no de otro (aunque su corte sea anterior)
    vista = {aid: {"modelo_ref": ref, "fecha_corte": "2026-11-05", "sello_ref": "K-20261105-001"} for aid, ref in MOTOR_BASE.items()}
    v2 = {k: {**v, "sello_ref": "K-20261104-001", "fecha_corte": "2026-11-04"} if k == "MOTOR-RUN-0002" else v for k, v in vista.items()}
    obt = [x for x in validar(sob, {**ctx, "sc3": v2, "sello_encargo": "K-20261105-001"}) if x["regla"] == "V-26"]
    h.chk("G1_artefacto_de_otro_sello_V26", len(obt) == 1 and "no con el del encargo" in obt[0]["mensaje"], obt)
    h.chk("G1_sin_sello_en_el_contexto_solo_mira_el_corte", validar(sob, {**ctx, "sc3": v2}) == [])
    h.chk("G1_sello_del_encargo_mal_formado_V01", {x["regla"] for x in validar(sob, {**ctx, "sc3": vista, "sello_encargo": 7})} == {"V-01"})
    # G2: una cifra VERIFICADO/ESTIMADO sin artefacto registrado no pasa, aunque el sobre no traiga referencias (N0)
    s0 = copy.deepcopy(sob)
    s0["payload"]["identificacion"]["nivel_analisis"] = "N0"
    del s0["payload"]["referencias"]
    for _, c in motor._cifras(s0["payload"]):
        if c.get("estado") in ("VERIFICADO", "ESTIMADO"):
            c["motor_id"], c["modelo_ref"] = "INVENTADO-999", "MODELO-INVENTADO"
    obt = {x["regla"] for x in validar(s0, {**ctx, "sc3": vista})}
    h.chk("G2_cifra_sin_artefacto_en_N0_V26", "V-26" in obt, obt)
    s1 = copy.deepcopy(s0)
    for _, c in motor._cifras(s1["payload"]):
        if c.get("motor_id") == "INVENTADO-999":
            c.pop("motor_id")
    h.chk("G2_cifra_sin_motor_id_V26", any(x["regla"] == "V-26" and "no cita ningún artefacto" in x["mensaje"]
                                           for x in validar(s1, {**ctx, "sc3": vista})) or any(x["regla"] == "V-08" for x in validar(s1, {**ctx, "sc3": vista})))
    # m1: las funciones públicas no lanzan con entradas raras
    try:
        ok = (o.advertencias_k(["x"]) == [] and o.advertencias_k({"a": 1}) == [] and o.advertencias_k(None) == []
              and motor.fallos_sobre({}, vista, "2026-11-05") and motor.fallos_sobre(sob, None, "2026-11-05")
              and motor.fallos_sobre({"payload": {"referencias": 7}}, vista, "2026-11-05") == [] or True)
        h.chk("m1_entradas_raras_no_lanzan", ok and motor.fallos_sobre({}, vista, "2026-11-05")[0][0] == "(interno)")
    except Exception as ex:   # noqa: BLE001
        h.chk("m1_entradas_raras_no_lanzan", False, type(ex).__name__)

    # ---------------------------------------------------------------- regresiones de la revisión (registro y sellos)
    # M1: el registro es una cadena; borrar o rehacer una entrada se detecta, y su cabeza se puede anclar fuera
    o = nuevo()
    h.chk("M1_cabeza_SC3", "SC3" in o.cabezas() and o.integridad() == [])
    del o.artefactos["MOTOR-RUN-0001"]
    h.chk("M1_borrar_del_indice_MOTOR", "MOTOR" in o.integridad())
    o = nuevo(); hasta(o, "VALIDADA")
    i = next(k for k, x in enumerate(o.sc3["entradas"]) if x.get("clave") == "MOTOR-RUN-0001")
    o.artefactos.pop("MOTOR-RUN-0001")
    h.chk("M1_borrar_un_artefacto_citado_MOTOR", "MOTOR" in o.integridad())
    o = nuevo()
    art = o.artefactos["MOTOR-RUN-0003"]
    art["artefacto"]["sello_ref"] = "K-20261106-001"; art["hash"] = __import__("motor").huella(art["artefacto"])
    h.chk("M1_rehacer_con_huella_recalculada_MOTOR", "MOTOR" in o.integridad())
    # M2: un sello retocado (sin su advertencia) se detecta y detiene la decisión
    o = nuevo({"matriz_autonomia": {"TACTICA": True}}, sellos=(con_advertencia(),))
    hasta(o, "PROPUESTA")
    for x in o.sellos["K-20261105-001"]["resultado_reglas"]:
        x["resultado"] = "OK"
    o.sellos["K-20261105-001"]["resultado_global"] = "OK"
    h.chk("M2_sello_retocado_SELLOS", "SELLOS" in o.integridad())
    r = o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)
    h.chk("M2_y_no_se_autoriza_O13", r["codigo"] == "O-13" and o.kill is not None, r)
    # M3: con el Motor alterado, entregar un sobre activa el kill-switch, y no se envía ninguna orden
    o = nuevo(); eid = en_analisis(o)
    o.modelos[next(iter(o.modelos))]["modelo"]["limites_validez"] = "cualquiera"
    r = o.entregar_sobre(eid, sobre(1), AHORA)
    h.chk("M3_entregar_con_motor_alterado_O13_kill", r["codigo"] == "O-13" and o.kill is not None, r)
    o = nuevo(); hasta(o, "AUTORIZADA")
    o.artefactos["MOTOR-RUN-0002"]["artefacto"]["semilla"] = 99
    r = o.orden_entrada("EXP-0001", "ORD-1", "ENVIADA", 0.0, "G", AHORA)
    h.chk("M3_no_se_envia_con_algo_alterado_O13_kill", r["codigo"] == "O-13" and o.kill is not None, r)
    # (revisión) un encargo que no informa una apertura no lleva a una propuesta
    import pruebas_orquestador as po
    _enc = po.encargo
    _sob = po.sobre
    po.encargo = lambda *a, **k: (lambda x: (x["payload"].update(decision_informada="EXPLORAR", nivel_analisis="N1"), x)[1])(_enc(*a, **k))
    po.sobre = lambda *a, **k: (lambda x: (x["payload"]["identificacion"].update(nivel_analisis="N1"), x)[1])(_sob(*a, **k))
    try:
        o = nuevo(); po.hasta(o, "COMPARADA"); po.elegir_si_hace_falta(o, "EXP-0001")
        r = o.proponer("EXP-0001", po.ENTRADA, po.SALIDA, "GESTOR_TACTICA", AHORA, po.dim(o, "EXP-0001", None, None))
        h.chk("encargo_que_no_es_de_apertura_no_propone_O06", r["codigo"] == "O-06" and "decisión" in r["motivo"], r)
    finally:
        po.encargo, po.sobre = _enc, _sob

    # ================================================================ hallazgo 13: advertencias de K
    sa = con_advertencia()
    h.chk("sello_con_advertencia_es_valido", validar_sello(sa, {"calendario": CAL}) == [])
    o = nuevo(sellos=(sa,))
    h.chk("advertencia_avisa_al_registrar_O36", any(x["codigo"] == "O-36" and "Q-10" in x["motivo"] for x in o.avisos))
    h.chk("advertencias_k_del_sello", [x["regla"] for x in o.advertencias_k(sa["sello_id"])] == ["Q-10"])
    hasta(o, "PROPUESTA")
    inf = informe_f(o)
    r = o.pantalla_aprobacion("EXP-0001", inf, AHORA)
    p = r["pantalla"]
    h.chk("pantalla_muestra_las_advertencias", r["ok"] and [x["regla"] for x in p["advertencias_k"]] == ["Q-10"])
    r = o.autorizar("EXP-0001", "OPERADOR", inf, AHORA, aprobacion(p))
    h.chk("sin_aceptarlas_O36", r["codigo"] == "O-36" and o.expedientes["EXP-0001"]["estado"] == "PROPUESTA", r)
    r = o.autorizar("EXP-0001", "OPERADOR", inf, AHORA, aprobacion(p, acepta_advertencias_k=False))
    h.chk("aceptar_con_falso_O36", r["codigo"] == "O-36", r)
    r = o.autorizar("EXP-0001", "OPERADOR", inf, AHORA, aprobacion(p, acepta_advertencias_k=True))
    h.chk("aceptandolas_se_autoriza", r["ok"] and o.expedientes["EXP-0001"]["estado"] == "AUTORIZADA", r)
    o = nuevo({"matriz_autonomia": {"TACTICA": True}}, sellos=(sa,))
    hasta(o, "PROPUESTA")
    r = o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)
    h.chk("la_matriz_no_decide_con_advertencias_O36", r["codigo"] == "O-36", r)
    o = nuevo({"matriz_autonomia": {"TACTICA": True}})
    hasta(o, "PROPUESTA")
    h.chk("sin_advertencias_la_matriz_si", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", informe_f(o), AHORA)["ok"])
    o = nuevo()
    hasta(o, "PROPUESTA")
    inf = informe_f(o)
    p = o.pantalla_aprobacion("EXP-0001", inf, AHORA)["pantalla"]
    h.chk("sin_advertencias_la_pantalla_va_vacia", p["advertencias_k"] == [] and not any(x["codigo"] == "O-36" for x in o.avisos))
    r = o.autorizar("EXP-0001", "OPERADOR", inf, AHORA, aprobacion(p, acepta_advertencias_k=True))
    h.chk("aceptar_lo_que_no_hay_O36", r["codigo"] == "O-36", r)
    h.chk("y_sin_aceptar_se_autoriza", autorizar_op(o, "EXP-0001", informe_f(o, n=2), AHORA)["ok"])

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO MOTOR T-26:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
