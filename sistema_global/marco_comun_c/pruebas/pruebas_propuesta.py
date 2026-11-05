"""Pruebas de T-20: la propuesta ligada al sobre (O-21), al resultado de D (O-22) y a la cantidad de E (O-23)."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "validador"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pruebas_orquestador import AHORA, CART_E, ENTRADA, INV, OBJ, SALIDA, STOP, Arnes, dim, hasta, nuevo  # noqa: E402

PROP = "GESTOR_TACTICA"


def validar_con(o, n, instrumento="EUR/USD", escenarios=None, mod=None, valid_until=None):
    """Lleva EXP-000n a VALIDADA con un sobre a medida."""
    from pruebas_orquestador import encargo, sobre
    eid = f"EXP-{n:04d}"
    enc, sob = encargo(n), sobre(n)
    enc["payload"]["mandato"]["instrumentos_permitidos"] = ["EUR/USD", "GBP/USD", "USD/JPY"]
    enc["payload"]["candidato"]["instrumento"] = instrumento
    sob["payload"]["identificacion"]["instrumento"] = instrumento
    if escenarios:
        sob["payload"]["capa2"]["escenarios"] = [{"nombre": k, "probabilidad": p, "rentabilidad_neta_pct": v, "horizonte_dias": 90}
                                                 for k, p, v in zip(("base", "adverso", "favorable"), (0.5, 0.3, 0.2), escenarios)]
    if valid_until:
        sob["valid_until"] = valid_until
        en = sob["payload"]["entrada_salida"]["entrada"]   # V-24: la ventana de entrada no pasa de la vigencia
        en["ventana_hasta"] = valid_until
    if mod:
        mod(sob["payload"])
        from validar_sobre import proporcion_real
        sob["payload"]["evidencia"]["proporcion"] = {k: round(v, 4) for k, v in proporcion_real(sob["payload"]).items()}
    assert o.detectar(eid, f"COR-{n:04d}", "DISCRECIONAL", "TACTICA", PROP, AHORA)["ok"]
    r = o.emitir_encargo(eid, enc, PROP, AHORA); assert r["ok"], r
    r = o.entregar_sobre(eid, sob, AHORA); assert r["ok"], r


def comparada(cfg=None, elegir=True):
    o = nuevo(cfg)
    hasta(o, "COMPARADA")
    if elegir:
        assert o.elegir("EXP-0001", "OPERADOR", "único candidato útil", AHORA)["ok"]
    return o


def elegir_si(o, eid="EXP-0001"):
    if not o.expedientes[eid]["comparacion"]["ganador"]:
        assert o.elegir(eid, "OPERADOR", "prueba", AHORA)["ok"]


def main():
    h = Arnes()

    def prop(nombre, esperado, entrada=None, salida=None, d="auto", o=None, ahora=AHORA):
        o = o or comparada()
        ent, sal = entrada or ENTRADA, salida or SALIDA
        dd = dim(o, "EXP-0001", ent, sal) if d == "auto" else d
        if isinstance(dd, dict) and isinstance(dd.get("cartera"), dict):   # la foto la habría registrado G
            from pruebas_control_f import registrar_foto
            dd = {**dd, "cartera": registrar_foto(o, dd["cartera"])}
        antes = copy.deepcopy(o.expedientes["EXP-0001"])
        r = o.proponer("EXP-0001", ent, sal, PROP, ahora, dd)
        ok = r["codigo"] == esperado and (r["ok"] or o.expedientes["EXP-0001"] == antes)
        h.chk(nombre, ok, r)
        return o, r

    # ---------------------------------------------------------------- D (O-22) y elegir
    o = comparada(elegir=False)
    c1, c2 = o.expedientes["EXP-0001"]["comparacion"], o.expedientes["EXP-0002"]["comparacion"]
    h.chk("D_lo_calcula_el_orquestador", c1["ganador"] and c1["decision"] == "CLARA" and c1["decision_global"] == "INVERTIR"
          and c2["excluido"] == "DUPLICADO" and not c2["ganador"], (c1, c2))
    r = o.proponer("EXP-0002", ENTRADA, SALIDA, PROP, AHORA, dim(o, "EXP-0002"))
    h.chk("el_que_no_gana_no_se_propone_O22", r["codigo"] == "O-22", r)
    h.chk("elegir_otro_habiendo_ganador_O22", o.elegir("EXP-0002", "OPERADOR", "y este", AHORA)["codigo"] == "O-22")
    o2 = nuevo(); hasta(o2, "VALIDADA")
    h.chk("elegir_no_comparado_O04", o2.elegir("EXP-0001", "OPERADOR", "x", AHORA)["codigo"] == "O-04")
    # sin ganador (decisión ajustada): elegir
    o5 = nuevo()
    validar_con(o5, 1); validar_con(o5, 2, instrumento="GBP/USD")
    o5.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    prop("ajustada_sin_eleccion_O22", "O-22", o=o5)
    h.chk("elegir_solo_el_operador_O05", o5.elegir("EXP-0001", "BROKER", "x", AHORA)["codigo"] == "O-05")
    h.chk("elegir_sin_motivo_O15", o5.elegir("EXP-0001", "OPERADOR", " ", AHORA)["codigo"] == "O-15")
    h.chk("elegir_ok", o5.elegir("EXP-0001", "OPERADOR", "me quedo con este", AHORA)["ok"]
          and o5.expedientes["EXP-0001"]["comparacion"]["elegido_por_operador"]["motivo"] == "me quedo con este")
    h.chk("elegir_otro_de_la_misma_comparacion_O22", o5.elegir("EXP-0002", "OPERADOR", "y este", AHORA)["codigo"] == "O-22")
    h.chk("elegir_deja_rastro_integro", o5.integridad() == [] and o5.expedientes["EXP-0001"]["historial"][-1]["motivo"].startswith("elegido"))
    # alterar a mano el resultado de D se detecta (está en la cadena de hashes)
    o3 = nuevo(); hasta(o3, "COMPARADA")
    o3.expedientes["EXP-0002"]["comparacion"]["ganador"] = True
    h.chk("comparacion_alterada_O13", o3.elegir("EXP-0002", "OPERADOR", "x", AHORA)["codigo"] == "O-13" and o3.integridad() == ["EXP:EXP-0002"])
    # exclusión dura real: sin retorno esperado positivo
    o3 = nuevo()
    validar_con(o3, 1, escenarios=(-1.0, -4.0, 1.0)); validar_con(o3, 2, instrumento="GBP/USD")
    o3.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    h.chk("exclusion_dura_no_se_elige_O22", o3.expedientes["EXP-0001"]["comparacion"]["excluido"] == "SIN_RETORNO_POSITIVO"
          and o3.elegir("EXP-0001", "OPERADOR", "x", AHORA)["codigo"] == "O-22")
    # decisión ajustada: solo se elige entre los empatados con el primero
    o4 = nuevo()
    validar_con(o4, 1); validar_con(o4, 2, instrumento="GBP/USD"); validar_con(o4, 3, instrumento="USD/JPY", escenarios=(1.0, -4.0, 4.0))
    o4.comparar(["EXP-0001", "EXP-0002", "EXP-0003"], "D", AHORA)
    h.chk("ajustada_sin_ganador", o4.expedientes["EXP-0001"]["comparacion"]["decision"] == "AJUSTADA"
          and not any(o4.expedientes[x]["comparacion"]["ganador"] for x in ("EXP-0001", "EXP-0002", "EXP-0003")))
    h.chk("ajustada_el_rezagado_no_se_elige_O22", o4.elegir("EXP-0003", "OPERADOR", "x", AHORA)["codigo"] == "O-22")
    h.chk("ajustada_un_empatado_si_se_elige", o4.elegir("EXP-0002", "OPERADOR", "prefiero GBP", AHORA)["ok"])
    prop("elegido_se_propone_OK", "OK")

    # ---------------------------------------------------------------- sobre (O-21)
    prop("instrumento_con_barra_es_el_mismo_OK", "OK", entrada={**ENTRADA, "instrumento": "EUR/USD"})
    prop("otro_instrumento_O21", "O-21", entrada={**ENTRADA, "instrumento": "GBPUSD", "activo_base": "GBP"})
    corto = {"condiciones": [{**STOP, "operador": ">=", "umbral": 1.15}, INV], "fecha": "2026-12-05"}
    prop("direccion_contraria_O21", "O-21", salida=corto)
    prop("stop_mas_holgado_O21", "O-21", salida={**SALIDA, "condiciones": [{**STOP, "umbral": 1.00}, OBJ, INV]})
    prop("stop_mas_prudente_OK", "OK", salida={**SALIDA, "condiciones": [{**STOP, "umbral": 1.07}, OBJ, INV]})
    prop("stop_por_encima_del_limite_O21", "O-21", salida={**SALIDA, "condiciones": [{**STOP, "umbral": 1.12}, OBJ, INV]})
    prop("objetivo_mas_ambicioso_O21", "O-21", salida={**SALIDA, "condiciones": [STOP, {**OBJ, "umbral": 1.20}, INV]})
    prop("objetivo_mas_modesto_OK", "OK", salida={**SALIDA, "condiciones": [STOP, {**OBJ, "umbral": 1.12}, INV]})
    prop("objetivo_del_lado_de_la_perdida_O21", "O-21", salida={**SALIDA, "condiciones": [STOP, {**OBJ, "umbral": 1.08}, INV]})
    prop("sin_objetivo_OK", "OK", salida={**SALIDA, "condiciones": [STOP, INV]})
    prop("falta_la_invalidez_del_sobre_O21", "O-21", salida={**SALIDA, "condiciones": [STOP, OBJ]})
    prop("invalidez_con_otro_umbral_O21", "O-21", salida={**SALIDA, "condiciones": [STOP, OBJ, {**INV, "umbral": 1.00}]})
    prop("ventana_mas_alla_del_sobre_O21", "O-21", entrada={**ENTRADA, "ventana_hasta": "2026-11-09T12:00:00+00:00"})
    o = comparada({"apalancamiento_permitido": True})
    prop("apalancamiento_mayor_que_el_del_sobre_O21", "O-21", entrada={**ENTRADA, "apalancamiento": 2.0}, o=o)
    prop("activo_base_distinto_de_la_divisa_base_O01", "O-01", entrada={**ENTRADA, "activo_base": "ZZZ"})
    prop("condicion_de_tipo_desconocido_O01", "O-01", salida={**SALIDA, "condiciones": [STOP, INV, {**OBJ, "tipo": "TP", "umbral": 9.0}]})
    sin_tipo = {k: v for k, v in OBJ.items() if k != "tipo"}
    prop("condicion_sin_tipo_O01", "O-01", salida={**SALIDA, "condiciones": [STOP, INV, {**sin_tipo, "id": "X-1", "umbral": 0}]})
    prop("invalidez_con_otra_unidad_O21", "O-21", salida={**SALIDA, "condiciones": [STOP, OBJ, {**INV, "unidad": "JPY"}]})
    prop("invalidez_con_otro_tipo_O21", "O-21", salida={**SALIDA, "condiciones": [STOP, OBJ, {**INV, "tipo": "OBJETIVO", "metrica": "precio", "operador": ">=", "umbral": 1.13}]})
    for nombre, cambio in (("stop_no_estimable", {"valor": None, "estado": "NO_ESTIMABLE"}), ("stop_en_porcentaje", {"valor": 1.05, "unidad": "%"})):
        o = nuevo()
        def mod(p, c=cambio):
            p["entrada_salida"]["stop"].update(c)
            p["entrada_salida"]["entrada"]["limite"]["unidad"] = p["entrada_salida"]["stop"]["unidad"]   # V-24: el límite va en la unidad del stop
            p["entrada_salida"]["objetivo"]["unidad"] = p["entrada_salida"]["stop"]["unidad"]   # V-22: y el objetivo también
        validar_con(o, 1, mod=mod); validar_con(o, 2, instrumento="GBP/USD")
        o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
        elegir_si(o)
        prop(f"sobre_con_{nombre}_O21", "O-21", o=o)
    o = comparada()
    from orquestador import _hash
    doc = o.expedientes["EXP-0001"]["sobre"]["documento"]
    doc["payload"]["entrada_salida"]["stop"]["valor"] = 0.50
    o.expedientes["EXP-0001"]["sobre"]["hash"] = _hash(doc)   # y además recalcula el hash guardado junto al sobre
    prop("sobre_alterado_con_hash_recalculado_O13", "O-13", salida={**SALIDA, "condiciones": [{**STOP, "umbral": 0.60}, OBJ, INV]}, o=o)
    o = comparada()
    doc = o.expedientes["EXP-0001"]["sobre"]["documento"]
    doc["payload"]["entrada_salida"]["stop"]["valor"] = 0.90   # alguien toca el sobre guardado para colar un stop holgado
    prop("sobre_guardado_alterado_O13", "O-13", salida={**SALIDA, "condiciones": [{**STOP, "umbral": 0.95}, OBJ, INV]}, o=o)

    # ---------------------------------------------------------------- E (O-23)
    prop("sin_calculo_de_E_O23", "O-23", d=None)
    o = comparada()
    d = dim(o)
    prop("calculo_de_E_con_campos_de_mas_O23", "O-23", d={**d, "extra": 1}, o=o)
    prop("solicitud_de_E_con_otro_stop_O23", "O-23", d={**d, "solicitud": {**d["solicitud"], "stop_precio": 1.00}})
    prop("solicitud_de_E_con_otra_cartera_O23", "O-23", d={**d, "solicitud": {**d["solicitud"], "cartera": "TRADING"}})
    prop("solicitud_de_E_con_otro_limite_O23", "O-23", d={**d, "solicitud": {**d["solicitud"], "precio_entrada": 1.09}})
    prop("calculo_de_E_futuro_O23", "O-23", d={**d, "ahora": "2026-11-06T10:00:00+00:00"})
    prop("calculo_de_E_viejo_O23", "O-23", d={**d, "ahora": "2026-11-06T07:00:00+00:00"})
    prop("calculo_de_E_con_fecha_imposible_O23", "O-23", d={**d, "ahora": "2026-02-30T09:00:00+00:00"})
    prop("cantidad_mayor_que_E_O23", "O-23", entrada={**ENTRADA, "cantidad": 9091.0})
    prop("cantidad_igual_a_E_OK", "OK", entrada={**ENTRADA, "cantidad": 9090.0})
    prop("cantidad_menor_que_E_OK", "OK", entrada={**ENTRADA, "cantidad": 10.0})
    prop("E_sin_hueco_en_la_cartera_O23", "O-23", d={**d, "cartera": {**CART_E, "perdida_dia_eur": 1e9}})
    prop("E_con_riesgo_por_encima_de_la_politica_O23", "O-23", d={**d, "riesgo_objetivo_pct": 50.0})
    o = comparada()
    r = o.proponer("EXP-0001", ENTRADA, SALIDA, PROP, AHORA, dim(o))
    h.chk("la_propuesta_guarda_la_cantidad_de_E", r["ok"] and o.expedientes["EXP-0001"]["propuesta"]["cantidad_e"] == 9090.0 and o.integridad() == [], r)
    # ---------------------------------------------------------------- un ganador claro de D se propone sin elegir
    from pruebas_extremo import candidatos
    o = nuevo(); candidatos(o)
    r = o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    h.chk("ganador_claro_de_D", r["ganador"] == "EXP-0001" and o.expedientes["EXP-0002"]["comparacion"]["ganador"] is False, r)
    prop("ganador_claro_se_propone_sin_eleccion_OK", "OK", o=o)
    # ---------------------------------------------------------------- T-21 y T-34 en el Orquestador
    from comparador import REFERENCIA_EFECTIVO
    def refs(**kw):
        r = {c: dict(REFERENCIA_EFECTIVO) for c in ("TRADING", "TACTICA", "LARGO_PLAZO")}
        r["TACTICA"].update(kw)
        return {"referencias": r}
    o = nuevo(); validar_con(o, 1)
    r = o.comparar(["EXP-0001"], "D", AHORA)
    h.chk("un_solo_candidato_llega_a_COMPARADA_y_gana", r["ok"] and r["ganador"] == "EXP-0001" and r["decision_global"] == "INVERTIR", r)
    prop("un_solo_candidato_se_propone_sin_eleccion_OK", "OK", o=o)
    o = nuevo(refs(rentabilidad_anual_pct=50.0)); validar_con(o, 1); validar_con(o, 2, instrumento="GBP/USD")
    r = o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    c = o.expedientes["EXP-0001"]["comparacion"]
    h.chk("referencia_exigente_D_se_abstiene", r["ok"] and r["decision_global"] == "ABSTENERSE" and r["ganador"] is None
          and c["excluido"] == "NO_SUPERA_REFERENCIA" and c["referencia"]["rentabilidad_anual_pct"] == 50.0, r)
    h.chk("abstencion_no_se_elige_O22", o.elegir("EXP-0001", "OPERADOR", "quiero invertir igualmente", AHORA)["codigo"] == "O-22")
    prop("abstencion_no_se_propone_O22", "O-22", o=o)
    o = nuevo(refs(benchmark_ref="BENCH-OTRO"))
    from pruebas_orquestador import encargo
    o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", PROP, AHORA)
    h.chk("mandato_con_otra_referencia_se_rechaza_al_encargar_O24", o.emitir_encargo("EXP-0001", encargo(1), PROP, AHORA)["codigo"] == "O-24")
    o = nuevo(); validar_con(o, 1); validar_con(o, 2, instrumento="GBP/USD", escenarios=(1.0, -4.0, 4.0))
    r = o.comparar(["EXP-0001"], "D", AHORA)
    h.chk("dejar_fuera_un_candidato_O24", r["codigo"] == "O-24" and r["faltan"] == ["EXP-0002"], r)
    # revisión independiente de T-21/T-34
    o = nuevo(); o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", PROP, AHORA)
    from pruebas_orquestador import sobre as _sobre
    o.emitir_encargo("EXP-0001", encargo(1), PROP, AHORA)
    s1 = _sobre(1)
    for x in s1["payload"]["capa2"]["escenarios"]:
        x["horizonte_dias"] = 1   # por debajo del mínimo del mandato (14 días): rebajaría el listón
    s1["payload"]["capa2"]["horizonte_dias"] = 1   # V-25: horizonte común
    r = o.entregar_sobre("EXP-0001", s1, AHORA)
    h.chk("horizonte_fuera_del_mandato_R13", r["codigo"] == "O-01" and "R-13" in r["motivo"], r)
    o = nuevo(); validar_con(o, 1)
    h.chk("primera_tanda_solo", o.comparar(["EXP-0001"], "D", AHORA)["ganador"] == "EXP-0001")
    validar_con(o, 2, instrumento="GBP/USD", escenarios=(3.0, -4.0, 6.0))   # llega después y es mejor
    prop("candidato_nuevo_obliga_a_recomparar_O22", "O-22", o=o)
    h.chk("la_segunda_tanda_sola_no_vale_O24", o.comparar(["EXP-0002"], "D", AHORA)["codigo"] == "O-24")
    r = o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    h.chk("se_vuelve_a_comparar_con_todos", r["ok"] and r["ganador"] == "EXP-0002" and not o.expedientes["EXP-0001"]["comparacion"]["ganador"], r)
    prop("el_antiguo_ganador_ya_no_se_propone_O22", "O-22", o=o)
    h.chk("la_comparacion_guarda_el_detalle_de_D", o.expedientes["EXP-0001"]["comparacion"]["detalle_d"]["dominado_por"] == ["EXP-0002"]
          and o.expedientes["EXP-0002"]["comparacion"]["detalle_d"]["exceso_sobre_referencia_pct"] > 0 and o.integridad() == [])
    o = nuevo()
    validar_con(o, 1); validar_con(o, 2, instrumento="GBP/USD"); validar_con(o, 3)   # 3: mismo instrumento que 1, duplicado
    o.comparar(["EXP-0001", "EXP-0002", "EXP-0003"], "D", AHORA)
    h.chk("duplicado_no_se_elige_en_ajustada_O22", o.expedientes["EXP-0003"]["comparacion"]["excluido"] == "DUPLICADO"
          and o.elegir("EXP-0003", "OPERADOR", "x", AHORA)["codigo"] == "O-22")
    o = nuevo(); validar_con(o, 1); validar_con(o, 2, instrumento="GBP/USD", valid_until="2026-11-06T10:00:00+00:00")   # vence antes
    r = o.comparar(["EXP-0001"], "D", "2026-11-06T11:00:00+00:00")
    h.chk("un_candidato_caducado_no_bloquea_a_los_demas", r["ok"] and r["ganador"] == "EXP-0001", r)
    from orquestador import Orquestador
    from pruebas_orquestador import CAL, CFG
    for nombre, cfg in (("referencia_absurda", refs(rentabilidad_anual_pct=500.0)), ("referencia_sin_cartera", {"referencias": {"TACTICA": REFERENCIA_EFECTIVO}})):
        try:
            Orquestador({**CFG, **cfg}, CAL); h.chk(f"config_{nombre}_se_rechaza", False)
        except ValueError:
            h.chk(f"config_{nombre}_se_rechaza", True)
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO PROPUESTA:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
