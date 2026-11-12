"""Pruebas de T-76 (V0.71): cartera sombra pasiva (Constitución V0.6, §9 punto 9, D-22, D-27 y D-30). Datos SIMULADOS.

Uso: python3 pruebas/pruebas_sombra_t76.py
"""
import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import persistencia as pe  # noqa: E402
import sombra as sb  # noqa: E402
from validar_sobre import _dt  # noqa: E402
from orquestador import PRIORIDAD_AVISO  # noqa: E402
from parametros import PARAMETROS  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, hasta, nuevo  # noqa: E402

NAN, INF = float("nan"), float("inf")


def meses_desde(n):
    """El mes AAAA-MM que cae n meses después de noviembre de 2026, y un instante del mes siguiente (el mes ya terminó: QA r01, H-02)."""
    a, m = 2026 + (10 + n) // 12, (10 + n) % 12 + 1
    a2, m2 = 2026 + (11 + n) // 12, (11 + n) % 12 + 1
    return f"{a:04d}-{m:02d}", f"{a2:04d}-{m2:02d}-01T12:00:00+00:00"


def o41(o):
    return [x for x in o.avisos if x["codigo"] == "O-41"]


def main():
    h = Arnes()
    R = h.rechaza
    h.chk("los_numeros_son_los_de_la_constitucion", PARAMETROS["i_meses_juicio_sombra"] == 24 and PARAMETROS["i_indice_sombra"]
          and PARAMETROS["i_coste_anual_sombra_pct"] == 0.20 and PRIORIDAD_AVISO["O-41"] == "ALTA")

    # ------------------------------------------------------------------ inicio y movimientos
    o = nuevo()
    hasta(o, "EN_ANALISIS", 1)   # un encargo con su gasto: los costes de análisis que la sombra resta al robot
    assert o.registrar_gasto("EV-ENC-0001", 2.5, 10.0, AHORA)["ok"]
    R("antes_de_iniciar_no_hay_movimientos", o, lambda: o.movimiento_sombra("APORTE", 1000.0, 110.0, "OPERADOR", AHORA, ref="MOV-043"), "O-06")
    R("antes_de_iniciar_no_se_compara", o, lambda: o.comparar_sombra("2026-12", 10000.0, 100.0, 100.0, 100.0, 0.0, "I", AHORA), "O-06")
    R("solo_el_operador_la_inicia", o, lambda: o.iniciar_sombra(10000.0, 100.0, "BROKER", AHORA), "O-05")
    for nombre, imp, pr in (("importe_nan", NAN, 100.0), ("importe_cero", 0.0, 100.0), ("importe_negativo", -1.0, 100.0),
                            ("precio_infinito", 10000.0, INF), ("importe_bool", True, 100.0), ("precio_texto", 10000.0, "100")):
        R(f"inicio_con_{nombre}_no", o, lambda imp=imp, pr=pr: o.iniciar_sombra(imp, pr, "OPERADOR", AHORA), "O-01")
    r = o.iniciar_sombra(10000.0, 100.0, "OPERADOR", AHORA)
    h.chk("el_primer_dia_compra_el_indice_con_el_mismo_capital", r["ok"] and r["unidades"] == 100.0
          and o.sombra["entradas"][0]["indice"] == PARAMETROS["i_indice_sombra"], r)
    R("una_sola_vez", o, lambda: o.iniciar_sombra(5000.0, 100.0, "OPERADOR", AHORA), "O-02")
    r = o.movimiento_sombra("APORTE", 1100.0, 110.0, "OPERADOR", AHORA, ref="MOV-053")
    h.chk("un_aporte_se_replica_al_precio_de_ese_momento", r["ok"] and abs(sb.estado_sombra(o.sombra["entradas"], 110.0, _dt(AHORA))["unidades"] - 110.0) < 1e-9, r)
    r = o.movimiento_sombra("RETIRADA", 550.0, 110.0, "G", AHORA, ref="MOV-055")
    h.chk("G_tambien_registra_una_retirada", r["ok"] and abs(sb.estado_sombra(o.sombra["entradas"], 110.0, _dt(AHORA))["unidades"] - 105.0) < 1e-9, r)
    R("una_retirada_mayor_que_la_sombra_no", o, lambda: o.movimiento_sombra("RETIRADA", 1e6, 110.0, "OPERADOR", AHORA, ref="MOV-057"), "O-06")
    R("tipo_de_movimiento_invalido", o, lambda: o.movimiento_sombra("DIVIDENDO", 10.0, 110.0, "OPERADOR", AHORA, ref="MOV-058"), "O-01")
    R("otro_actor_no_registra_movimientos", o, lambda: o.movimiento_sombra("APORTE", 10.0, 110.0, "BROKER", AHORA, ref="MOV-059"), "O-05")
    h.chk("registro_integro_y_anclado", o.sombra_ok() and o.integridad() == [] and "SOMBRA" in o.cabezas())

    # ------------------------------------------------------------------ la comparación mensual
    mes1, t1 = meses_desde(1)
    R("la_compara_I", o, lambda: o.comparar_sombra(mes1, 11000.0, 120.0, 100.0, 101.0, 0.0, "OPERADOR", t1), "O-05")
    R("no_el_mes_del_inicio", o, lambda: o.comparar_sombra("2026-11", 11000.0, 120.0, 100.0, 101.0, 0.0, "I", t1), "O-01")
    R("no_saltarse_un_mes", o, lambda: o.comparar_sombra(meses_desde(2)[0], 11000.0, 120.0, 100.0, 101.0, 0.0, "I", meses_desde(2)[1]), "O-01")
    R("no_un_mes_del_futuro", o, lambda: o.comparar_sombra(mes1, 11000.0, 120.0, 100.0, 101.0, 0.0, "I", AHORA), "O-01")
    for nombre, args in (("valor_nan", (NAN, 120.0, 100.0, 101.0, 0.0)), ("precio_cero", (11000.0, 0.0, 100.0, 101.0, 0.0)),
                         ("inflacion_negativa", (11000.0, 120.0, -100.0, 101.0, 0.0)), ("impuestos_negativos", (11000.0, 120.0, 100.0, 101.0, -1.0)),
                         ("mes_ilegible", None)):
        if args is None:
            R(f"comparar_con_{nombre}_no", o, lambda: o.comparar_sombra("2026-13", 11000.0, 120.0, 100.0, 101.0, 0.0, "I", t1), "O-01")
        else:
            R(f"comparar_con_{nombre}_no", o, lambda args=args: o.comparar_sombra(mes1, *args, "I", t1), "O-01")

    # los costes de análisis son los que anotó el Orquestador
    r = o.comparar_sombra(mes1, 13000.0, 120.0, 100.0, 105.0, 50.0, "I", t1)
    c = o.sombra["entradas"][-1]
    est = c["sombra"]
    bruto = 105.0 * 120.0
    h.chk("la_sombra_vale_sus_unidades_al_precio_neta_de_su_coste", abs(est["valor_bruto_eur"] - bruto) < 1e-6
          and 0 < est["coste_eur"] < bruto * 0.002 and abs(est["valor_eur"] - (bruto - est["coste_eur"])) < 1e-6, est)
    res = r.get("resultado") or {}
    h.chk("el_robot_va_neto_de_costes_de_analisis_e_impuestos", r["ok"] and c["costes_analisis_eur"] == 2.5
          and abs(res["robot_neto_eur"] - (13000.0 - 2.5 - 50.0)) < 1e-9, r)
    h.chk("y_tambien_en_terminos_reales", abs(res["robot_neto_real_eur"] - res["robot_neto_eur"] / 1.05) < 1e-6
          and abs(res["sombra_real_eur"] - est["valor_eur"] / 1.05) < 1e-6 and abs(res["inflacion_acumulada"] - 0.05) < 1e-12, res)
    h.chk("antes_del_plazo_no_se_juzga", r["veredicto"] == "EN_PLAZO" and not o41(o), r)
    R("un_mes_una_vez", o, lambda: o.comparar_sombra(mes1, 13000.0, 120.0, 100.0, 105.0, 50.0, "I", t1), "O-02", ok_esperado=False)

    # ------------------------------------------------------------------ el juicio a los 24 meses
    def hasta_el_mes(o, n, robot):
        for k in range(1 + len([x for x in o.sombra["entradas"] if x["tipo"] == "COMPARACION"]), n + 1):
            mes, t = meses_desde(k)
            r = o.comparar_sombra(mes, robot, 120.0, 100.0, 110.0, 0.0, "I", t)
            assert r["ok"], (k, r)
        return r
    o2 = copy.deepcopy(o)
    r = hasta_el_mes(o2, 23, 9000.0)
    h.chk("a_los_23_meses_sigue_en_plazo_aunque_pierda", r["veredicto"] == "EN_PLAZO" and not o41(o2), r)
    r = hasta_el_mes(o2, 24, 9000.0)
    h.chk("a_los_24_si_no_la_supera_propone_gestion_pasiva", r["veredicto"] == "PROPONER_PASIVA" and len(o41(o2)) == 1
          and o41(o2)[0]["prioridad"] == "ALTA" and "decide el operador" in o41(o2)[0]["motivo"], (r, o41(o2)))
    r = hasta_el_mes(o2, 26, 9000.0)
    h.chk("O41_una_vez_al_pasar_a_no_superarla_no_cada_mes_H08", r["veredicto"] == "PROPONER_PASIVA" and len(o41(o2)) == 1, o41(o2))
    o3 = copy.deepcopy(o)
    r = hasta_el_mes(o3, 24, 20000.0)
    h.chk("si_la_supera_en_real_no_hay_aviso", r["veredicto"] == "SUPERA" and not o41(o3), r)
    h.chk("informe_de_la_sombra", o3.informe_sombra()["comparaciones"] == 24 and o3.informe_sombra()["ultima"]["veredicto"] == "SUPERA"
          and nuevo().informe_sombra() is None)

    # ------------------------------------------------------------------ integridad y persistencia
    for nombre, toque in (("una_comparacion", lambda L: L["entradas"][-1]["resultado"].__setitem__("supera", True)),
                          ("el_inicio", lambda L: L["entradas"][0].__setitem__("importe_eur", 1.0)),
                          ("un_segundo_inicio", lambda L: L["entradas"].append(dict(L["entradas"][0])))):
        o4 = copy.deepcopy(o2)
        toque(o4.sombra)
        h.chk(f"tocar_{nombre}_se_detecta", "SOMBRA" in o4.integridad() and not o4.sombra_ok())
    o4 = copy.deepcopy(o2)
    o4.sombra["entradas"][-1]["veredicto"] = "SUPERA"
    mes, t = meses_desde(27)
    r = o4.comparar_sombra(mes, 9000.0, 120.0, 100.0, 110.0, 0.0, "I", "2030-01-01T12:00:00+00:00")
    h.chk("con_el_registro_tocado_no_se_compara_y_salta_el_kill", r["codigo"] == "O-13" and o4.kill is not None, r)
    t_ = pe.volcar(o2, meses_desde(24)[1])
    rc = pe.cargar(t_)
    h.chk("guardar_y_cargar_conserva_la_sombra", rc["ok"] and rc["orquestador"].sombra == o2.sombra and rc["orquestador"].integridad() == [],
          rc.get("motivo"))

    # ------------------------------------------------------------------ el cálculo, solo
    h.chk("estado_ilegible_es_None", sb.estado_sombra([{"tipo": "INICIO"}], 100.0, _dt(AHORA)) is None
          and sb.estado_sombra([{"tipo": "INICIO", "importe_eur": 1.0, "precio_indice": 0.0, "ahora": AHORA}], 1.0, _dt(AHORA)) is None)

    # ------------------------------------------------------------------ regresiones de la QA r01
    ini = {"tipo": "INICIO", "importe_eur": 10000.0, "precio_indice": 100.0, "ahora": "2026-01-01T00:00:00+00:00"}
    apo = {"tipo": "APORTE", "importe_eur": 1e6, "precio_indice": 100.0, "ahora": "2026-12-31T00:00:00+00:00"}
    est = sb.estado_sombra([ini, apo], 100.0, _dt("2027-01-01T00:00:00+00:00"))
    h.chk("un_aporte_de_la_vispera_paga_un_dia_de_coste_H01", est and est["coste_eur"] < 10000.0 * 0.0021 + 1e6 * 0.002 / 365 * 1.5, est)
    ret = {"tipo": "RETIRADA", "importe_eur": 5000.0, "precio_indice": 100.0, "ahora": "2026-12-31T00:00:00+00:00"}
    e1 = sb.estado_sombra([ini], 100.0, _dt("2026-12-31T00:00:00+00:00"))
    e2 = sb.estado_sombra([ini, ret], 100.0, _dt("2026-12-31T00:00:00+00:00"))
    h.chk("una_retirada_no_borra_el_coste_devengado_H01", e1 and e2 and abs((e1["valor_eur"] - e2["valor_eur"]) - 5000.0) < 1e-6
          and e2["coste_eur"] > 0, (e1, e2))
    h.chk("retirar_mas_de_lo_que_hay_con_precios_enormes_no_H06",
          sb.estado_sombra([{**ini, "precio_indice": 1e12}, {**ret, "importe_eur": 2e4, "precio_indice": 1e12}], 1e12, _dt("2026-12-31T00:00:00+00:00")) is None)
    o8 = nuevo()   # T-100 (QA r03, H-18): con un inicio válido, para que la prueba llegue a comparar (el de antes ya lo rechaza H-11)
    assert o8.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
    m1, t1_ = meses_desde(1)
    n8 = len(o8.sombra["entradas"])
    r = o8.comparar_sombra(m1, 1e308, 100.0, 1e10, 1e-300, 0.0, "I", t1_)
    h.chk("resultados_no_finitos_no_se_anotan_H03", r["codigo"] == "O-01" and len(o8.sombra["entradas"]) == n8
          and pe.volcar(o8, t1_) is not None, r)
    o9 = nuevo()
    assert o9.iniciar_sombra(10000.0, 100.0, "OPERADOR", AHORA)["ok"]
    mes, t = meses_desde(1)
    R("no_se_compara_un_mes_sin_terminar_H02", o9, lambda: o9.comparar_sombra(mes, 10000.0, 100.0, 100.0, 100.0, 0.0, "I", "2026-12-31T23:00:00+00:00"), "O-01")
    assert o9.comparar_sombra(mes, 10000.0, 100.0, 100.0, 100.0, 0.0, "I", t)["ok"]
    mes2, t2 = meses_desde(2)
    R("el_indice_de_precios_del_inicio_no_cambia_H07", o9, lambda: o9.comparar_sombra(mes2, 10000.0, 100.0, 90.0, 100.0, 0.0, "I", t2), "O-01")
    r = o9.barrer(meses_desde(3)[1])
    h.chk("si_I_deja_de_comparar_barrer_lo_avisa_H04", [x for x in o9.avisos if x["codigo"] == "O-42"] and ("sombra_pendiente", mes2, 1) in r["cambios"], r)   # V0.75 (QA r02, H-13): con cuántos faltan
    o9.barrer(meses_desde(3)[1])
    h.chk("y_no_lo_repite_cada_barrido", len([x for x in o9.avisos if x["codigo"] == "O-42"]) == 1)
    o10 = copy.deepcopy(o9)
    o10.sombra["entradas"][0]["importe_eur"] = 1.0
    r = o10.comparar_sombra(mes2, 10000.0, 100.0, 100.0, 100.0, 0.0, "I", meses_desde(4)[1])
    h.chk("con_el_registro_tocado_comparar_da_O13_antes_de_leerlo_H05", r["codigo"] == "O-13" and o10.kill is not None, r)
    h.chk("comparar_con_inflacion_imposible_es_None", sb.comparar(1.0, 0.0, 0.0, {"valor_eur": 1.0, "aportado_neto_eur": 1.0}, 0.0, 1.0) is None)
    h.chk("veredicto_en_el_borde", sb.veredicto(23, {"supera": False}) == "EN_PLAZO" and sb.veredicto(24, {"supera": False}) == "PROPONER_PASIVA"
          and sb.veredicto(24, {"supera": True}) == "SUPERA")
    h.chk("meses_entre", sb.meses_entre("2026-11", "2028-11") == 24 and sb.meses_entre("2026-12", "2027-01") == 1)

    # ------------------------------------------------------------------ QA r02 de T-76 (ronda r03)
    def veinticuatro(robot_ultimo, mov):
        """Meses 1 a 23 comparados a tiempo; tras el cierre del 24, un movimiento; después I compara el 24 (sondas J5 y J5c)."""
        o_ = nuevo()
        assert o_.iniciar_sombra(100000.0, 100.0, "OPERADOR", AHORA)["ok"]
        for k in range(1, 24):
            m_, t_ = meses_desde(k)
            assert o_.comparar_sombra(m_, 100000.0, 100.0, 100.0, 100.0, 0.0, "I", t_)["ok"], k
        m24, t24 = meses_desde(24)
        assert o_.movimiento_sombra(mov, 50000.0, 100.0, "OPERADOR", "2028-12-02T09:00:00+00:00", ref="MOV-179")["ok"]
        return o_, o_.comparar_sombra(m24, robot_ultimo, 100.0, 100.0, 100.0, 0.0, "I", "2028-12-03T09:00:00+00:00")
    o_, r = veinticuatro(99000.0, "RETIRADA")
    h.chk("una_retirada_tras_el_cierre_no_cambia_el_juicio_H10", r["ok"] and r["veredicto"] == "PROPONER_PASIVA" and o41(o_), r)
    o_, r = veinticuatro(101000.0, "APORTE")
    h.chk("un_aporte_tras_el_cierre_no_cambia_el_juicio_H10", r["ok"] and r["veredicto"] == "SUPERA" and not o41(o_), r)
    o12 = nuevo()
    R("inicio_con_unidades_no_finitas_no_H11", o12, lambda: o12.iniciar_sombra(1e200, 1e-200, "OPERADOR", AHORA), "O-01")
    assert o12.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
    r = o12.movimiento_sombra("APORTE", 1e300, 1e-300, "OPERADOR", AHORA, ref="MOV-188")
    h.chk("un_movimiento_no_finito_no_se_confunde_con_una_retirada_mayor_H11", r["codigo"] == "O-01" and "finito" in r["motivo"], r)
    for nombre, toque in (("sin_ahora", lambda x: x.sombra["entradas"][0].pop("ahora")), ("entradas_vaciadas", lambda x: x.sombra["entradas"].clear())):
        for op in ("iniciar", "movimiento"):
            o13 = nuevo()
            assert o13.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
            toque(o13)
            r = (o13.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA) if op == "iniciar"
                 else o13.movimiento_sombra("APORTE", 10.0, 100.0, "OPERADOR", AHORA, ref="MOV-196"))
            h.chk(f"registro_tocado_{nombre}_{op}_es_O13_H12", r["codigo"] == "O-13" and o13.kill is not None, r)
    o14 = nuevo()
    assert o14.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
    o14.sombra["entradas"][0]["importe_eur"] = 1.0
    o14.barrer(meses_desde(2)[1])
    h.chk("barrer_avisa_de_un_registro_de_la_sombra_roto_H12", any(x["codigo"] == "O-13" and "sombra" in x["motivo"] for x in o14.avisos), o14.avisos[-3:])
    # H-13: plazo de gracia, cuántos faltan y el mes de juicio en ALTA
    o15 = nuevo()
    assert o15.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]   # el 6-11-2026: el primer mes que se compara es 2026-12
    gracia = PARAMETROS["i_dias_gracia_comparacion_sombra"]
    h.chk("antes_del_plazo_de_gracia_no_hay_O42_H13", o15.comparacion_sombra_pendiente("2027-01-01T00:00:00+00:00") is None
          and o15.comparacion_sombra_pendiente(f"2027-01-{gracia:02d}T23:59:59.999999+00:00") is None)
    h.chk("y_justo_al_acabar_el_plazo_si_H13", o15.comparacion_sombra_pendiente(f"2027-01-{gracia + 1:02d}T00:00:00+00:00") == "2026-12")
    d = o15.comparaciones_sombra_pendientes("2027-04-10T00:00:00+00:00")
    h.chk("dice_cuantos_meses_faltan_H13", d == {"primero": "2026-12", "faltan": 4, "juicio": False}, d)
    o15.barrer("2027-04-10T00:00:00+00:00")
    h.chk("y_el_aviso_lo_dice_H13", any(x["codigo"] == "O-42" and "4 mes(es)" in x["motivo"] for x in o15.avisos))
    o16 = nuevo()
    assert o16.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
    for k in range(1, 24):
        m_, t_ = meses_desde(k)
        assert o16.comparar_sombra(m_, 1000.0, 100.0, 100.0, 100.0, 0.0, "I", t_)["ok"]
    o16.barrer("2028-12-10T00:00:00+00:00")
    h.chk("falta_el_mes_de_juicio_es_O44_en_ALTA_H13", any(x["codigo"] == "O-44" and x["prioridad"] == "ALTA" for x in o16.avisos)
          and not any(x["codigo"] == "O-42" for x in o16.avisos), [x["codigo"] for x in o16.avisos])
    # H-14: los cuatro mutantes que sobrevivían
    o17 = nuevo()
    assert o17.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-12-01T00:30:00+01:00")["ok"]   # en UTC aún es noviembre
    h.chk("el_mes_de_inicio_es_el_de_UTC_en_el_borde_H14", o17.comparar_sombra("2026-12", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-01-02T00:00:00+00:00")["ok"])
    o18 = nuevo()
    assert o18.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-12-01T00:30:00+01:00")["ok"]
    R("y_no_se_puede_empezar_por_el_mes_siguiente_H14", o18,
      lambda: o18.comparar_sombra("2027-01", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-02-02T00:00:00+00:00"), "O-01")
    h.chk("pendiente_no_salta_el_ultimo_instante_del_mes_H14", o15.comparacion_sombra_pendiente("2026-12-31T23:59:59.999999+00:00") is None)
    mini = [{"tipo": "INICIO", "importe_eur": 1e-7, "precio_indice": 100.0, "ahora": AHORA}]
    h.chk("la_tolerancia_es_relativa_con_unidades_diminutas_H14",
          sb.estado_sombra(mini + [{"tipo": "RETIRADA", "importe_eur": 2e-7, "precio_indice": 100.0, "ahora": AHORA}], 100.0, _dt(AHORA)) is None
          and sb.estado_sombra(mini + [{"tipo": "RETIRADA", "importe_eur": 1e-7, "precio_indice": 100.0, "ahora": AHORA}], 100.0, _dt(AHORA)) is not None)
    h.chk("estado_sombra_con_un_resultado_infinito_es_None_H14",
          sb.estado_sombra([{"tipo": "INICIO", "importe_eur": 1e308, "precio_indice": 1e-10, "ahora": AHORA}], 100.0, _dt(AHORA)) is None)

    # ------------------------------------------------------------------ QA r03 de T-76 (T-100, marco V0.76)
    from datetime import datetime, timedelta, timezone
    coste = PARAMETROS["i_coste_anual_sombra_pct"]

    def cierre(mes):
        a_, m_ = map(int, mes.split("-"))
        return datetime(a_ + m_ // 12, m_ % 12 + 1, 1, tzinfo=timezone.utc) - timedelta(microseconds=1)

    def referencia(movs, precio, t_fin):
        """Cálculo independiente del código: un fondo con valor liquidativo (1 - coste)^(años desde el inicio); cada aporte compra
        participaciones y cada retirada las vende a ese valor; la sombra vale participaciones · precio · valor liquidativo."""
        t0 = _dt(movs[0][3])
        vl = lambda t: (1 - coste / 100.0) ** ((t - t0).total_seconds() / (365 * 86400.0))  # noqa: E731
        part = sum((-1 if tp == "RETIRADA" else 1) * imp / (pr * vl(_dt(t))) for tp, imp, pr, t in movs)
        return part * precio * vl(t_fin)

    # H-17: la referencia del movimiento en el intermediario; el mismo movimiento cuenta una vez
    o20 = nuevo()
    assert o20.iniciar_sombra(100000.0, 100.0, "OPERADOR", AHORA)["ok"]
    t_ap = "2026-12-10T10:00:00+00:00"
    r1 = o20.movimiento_sombra("APORTE", 50000.0, 100.0, "G", t_ap, ref="INT-0001")
    r2 = o20.movimiento_sombra("APORTE", 50000.0, 101.0, "OPERADOR", "2026-12-10T11:00:00+00:00", ref="INT-0001")
    r3 = o20.movimiento_sombra("APORTE", 50000.0, 100.0, "G", "2026-12-10T12:00:00+00:00", ref="INT-0001")
    aportes = [x for x in o20.sombra["entradas"] if x["tipo"] == "APORTE"]
    h.chk("el_mismo_movimiento_declarado_dos_veces_cuenta_una_H17", r1["codigo"] == "OK" and r2["codigo"] == r3["codigo"] == "O-02"
          and r2["ok"] and len(aportes) == 1 and aportes[0]["precio_indice"] == 100.0 and aportes[0]["ref"] == "INT-0001",
          (r1["codigo"], r2["codigo"], r3["codigo"], len(aportes)))
    for k in range(1, 25):
        m_, t_ = meses_desde(k)
        r = o20.comparar_sombra(m_, 150750.0, 100.0, 100.0, 100.0, 0.0, "I", t_)
    h.chk("y_un_aporte_repetido_no_da_la_vuelta_al_juicio_H17", r["ok"] and r["veredicto"] == "SUPERA" and not o41(o20), r)
    o21 = nuevo()
    assert o21.iniciar_sombra(100000.0, 100.0, "OPERADOR", AHORA)["ok"]
    assert o21.movimiento_sombra("APORTE", 50000.0, 100.0, "G", t_ap, ref="INT-0001")["ok"]
    for nombre, args in (("otro_importe", ("APORTE", 40000.0)), ("otro_tipo", ("RETIRADA", 50000.0))):
        o_ = copy.deepcopy(o21)
        n_ = len(o_.sombra["entradas"])
        r = o_.movimiento_sombra(*args, 100.0, "OPERADOR", "2026-12-10T11:00:00+00:00", ref="INT-0001")
        h.chk(f"la_misma_referencia_con_{nombre}_es_O03_con_kill_switch_H17", r["codigo"] == "O-03" and not r["ok"]
              and o_.kill is not None and len(o_.sombra["entradas"]) == n_ and any(x["codigo"] == "O-03" for x in o_.avisos), r)
    for nombre, ref in (("sin_referencia", None), ("referencia_vacia", ""), ("referencia_en_blanco", "  "), ("referencia_no_texto", 7)):
        R(f"movimiento_{nombre}_no_H17", o21, lambda ref=ref: o21.movimiento_sombra("APORTE", 10.0, 100.0, "OPERADOR", t_ap, ref=ref), "O-01")
    h.chk("otra_referencia_es_otro_movimiento_H17", o21.movimiento_sombra("APORTE", 50000.0, 100.0, "G", t_ap, ref="INT-0002")["ok"]
          and len([x for x in o21.sombra["entradas"] if x["tipo"] == "APORTE"]) == 2)
    o22 = nuevo()   # una entrada sin referencia, como las de un estado de la V0.75: se conserva y no se compara con nada
    assert o22.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
    o22._anota_sombra({"tipo": "APORTE", "importe_eur": 10.0, "precio_indice": 100.0, "ahora": AHORA}, "OPERADOR", AHORA)
    h.chk("las_entradas_sin_referencia_de_la_V075_se_conservan_H17", o22.sombra_ok()
          and o22.movimiento_sombra("APORTE", 10.0, 100.0, "OPERADOR", AHORA, ref="INT-0003")["codigo"] == "OK"
          and len(o22.sombra["entradas"]) == 3)
    # H-19: con el registro roto, barrer() para (kill-switch) y no calcula lo pendiente
    for nombre, toque in (("importe_del_inicio", lambda x: x.sombra["entradas"][0].__setitem__("importe_eur", 1.0)),
                          ("inicio_retrasado", lambda x: x.sombra["entradas"][0].__setitem__("ahora", "2020-01-01T00:00:00+00:00"))):
        o_ = nuevo()
        assert o_.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
        toque(o_)
        o_.barrer("2027-03-10T00:00:00+00:00")
        cods = [x["codigo"] for x in o_.avisos]
        h.chk(f"barrer_con_el_registro_roto_{nombre}_para_y_no_calcula_lo_pendiente_H19", "O-13" in cods and o_.kill is not None
              and "O-42" not in cods and "O-44" not in cods, cods)
    # H-18: regresiones para los mutantes que sobrevivían (sondas A1, A2, A3, A8, A12 y F9 del revisor)
    o23 = nuevo()   # A1: el último microsegundo del mes entra; el primer instante del siguiente, no; valor contra la referencia
    assert o23.iniciar_sombra(100000.0, 100.0, "OPERADOR", AHORA)["ok"]
    movs = [("INICIO", 100000.0, 100.0, AHORA), ("APORTE", 10000.0, 101.0, "2026-12-31T23:59:59.999999+00:00")]
    assert o23.movimiento_sombra(*movs[1][:3], "OPERADOR", movs[1][3], ref="INT-A1-1")["ok"]
    assert o23.movimiento_sombra("APORTE", 3000.0, 102.0, "OPERADOR", "2027-01-01T00:00:00+00:00", ref="INT-A1-2")["ok"]
    assert o23.comparar_sombra("2026-12", 110000.0, 103.0, 100.0, 100.0, 0.0, "I", "2027-01-02T06:00:00+00:00")["ok"]
    est = o23.sombra["entradas"][-1]["sombra"]
    h.chk("el_ultimo_microsegundo_del_mes_entra_y_el_primer_instante_del_siguiente_no_H18", est["aportado_neto_eur"] == 110000.0
          and abs(est["valor_eur"] - referencia(movs, 103.0, cierre("2026-12"))) < 1e-6, est)
    o24 = nuevo()   # A2: los costes de análisis hasta el cierre del mes, ni un instante después
    hasta(o24, "EN_ANALISIS", 1)
    assert o24.registrar_gasto("EV-ENC-0001", 1.0, 1.0, AHORA)["ok"]
    assert o24.iniciar_sombra(100000.0, 100.0, "OPERADOR", "2026-11-06T12:00:00+00:00")["ok"]
    assert o24.registrar_gasto("EV-ENC-0001", 3.0, 1.0, "2026-12-31T23:59:59.999999+00:00")["ok"]
    assert o24.registrar_gasto("EV-ENC-0001", 7.0, 1.0, "2027-01-01T00:00:00+00:00")["ok"]
    assert o24.comparar_sombra("2026-12", 100000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-01-03T06:00:00+00:00")["ok"]
    c12 = o24.sombra["entradas"][-1]["costes_analisis_eur"]
    assert o24.comparar_sombra("2027-01", 100000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-02-03T06:00:00+00:00")["ok"]
    h.chk("los_costes_de_analisis_cuentan_hasta_el_cierre_H18", c12 == 4.0 and o24.sombra["entradas"][-1]["costes_analisis_eur"] == 11.0, c12)
    o25 = nuevo()   # A3: comparar 29 días tarde no devenga más coste; y el coste es el de la referencia (año de 365 días)
    assert o25.iniciar_sombra(1e6, 100.0, "OPERADOR", AHORA)["ok"]
    assert o25.comparar_sombra("2026-12", 1e6, 100.0, 100.0, 100.0, 0.0, "I", "2027-01-30T06:00:00+00:00")["ok"]
    v25 = o25.sombra["entradas"][-1]["sombra"]["valor_eur"]
    h.chk("el_coste_se_devenga_hasta_el_cierre_aunque_I_compare_tarde_H18",
          abs(v25 - referencia([("INICIO", 1e6, 100.0, AHORA)], 100.0, cierre("2026-12"))) < 1e-6, v25)
    gracia = PARAMETROS["i_dias_gracia_comparacion_sombra"]
    o26 = nuevo()   # A8: O-44 en cuanto vence la gracia del mes de juicio, aunque falten meses anteriores
    assert o26.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
    for k in range(1, 21):
        m_, t_ = meses_desde(k)
        assert o26.comparar_sombra(m_, 1000.0, 100.0, 100.0, 100.0, 0.0, "I", t_)["ok"]
    d_antes = o26.comparaciones_sombra_pendientes(f"2028-12-{gracia:02d}T23:59:59+00:00")
    d_juicio = o26.comparaciones_sombra_pendientes(f"2028-12-{gracia + 1:02d}T00:00:00+00:00")
    h.chk("el_juicio_se_mira_en_el_ultimo_mes_pendiente_no_en_el_primero_H18",
          d_antes == {"primero": "2028-08", "faltan": 3, "juicio": False} and d_juicio == {"primero": "2028-08", "faltan": 4, "juicio": True},
          (d_antes, d_juicio))
    o27 = nuevo()   # A12: lo pendiente cuenta desde el mes de inicio en UTC
    assert o27.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-12-01T00:30:00+01:00")["ok"]
    d = o27.comparaciones_sombra_pendientes(f"2027-01-{gracia + 1:02d}T00:00:00+00:00")
    h.chk("lo_pendiente_cuenta_desde_el_mes_de_inicio_en_UTC_H18", d == {"primero": "2026-12", "faltan": 1, "juicio": False}, d)
    o28 = nuevo()   # F9: una comparación que no da números finitos se rechaza sin tocar nada
    assert o28.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
    R("comparacion_con_precio_enorme_no_finita_no_H18", o28,
      lambda: o28.comparar_sombra("2026-12", 1000.0, 1e308, 1.0, 1.0, 0.0, "I", "2027-01-02T00:00:00+00:00"), "O-01")
    h.chk("comparar_sin_resultado_finito_es_None_H18",
          sb.comparar(1e308, 0.0, 0.0, {"valor_eur": 1.0, "aportado_neto_eur": 1.0}, 1e10, 1e-300) is None)
    o29 = nuevo()   # empate en el mes de juicio: no la supera, se propone la gestión pasiva (juicio en real, con «>»)
    assert o29.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
    for k in range(1, 24):
        m_, t_ = meses_desde(k)
        assert o29.comparar_sombra(m_, 1000.0, 100.0, 100.0, 100.0, 0.0, "I", t_)["ok"]
    m24, t24 = meses_desde(24)
    igual = sb.estado_sombra(o29.sombra["entradas"], 100.0, cierre(m24))["valor_eur"]
    r = o29.comparar_sombra(m24, igual, 100.0, 100.0, 100.0, 0.0, "I", t24)
    h.chk("con_el_robot_igual_a_la_sombra_se_propone_la_pasiva_H18", r["ok"] and r["veredicto"] == "PROPONER_PASIVA", r)

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO SOMBRA T-76:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
