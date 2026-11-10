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
from orquestador import PRIORIDAD_AVISO  # noqa: E402
from parametros import PARAMETROS  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, hasta, nuevo  # noqa: E402

NAN, INF = float("nan"), float("inf")


def meses_desde(n):
    """El mes AAAA-MM que cae n meses después de noviembre de 2026, y un instante dentro de él."""
    a, m = 2026 + (10 + n) // 12, (10 + n) % 12 + 1
    mes = f"{a:04d}-{m:02d}"
    return mes, f"{mes}-28T12:00:00+00:00"


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
    R("antes_de_iniciar_no_hay_movimientos", o, lambda: o.movimiento_sombra("APORTE", 1000.0, 110.0, "OPERADOR", AHORA), "O-06")
    R("antes_de_iniciar_no_se_compara", o, lambda: o.comparar_sombra("2026-12", 10000.0, 100.0, 100.0, 100.0, 0.0, "I", AHORA), "O-06")
    R("solo_el_operador_la_inicia", o, lambda: o.iniciar_sombra(10000.0, 100.0, "BROKER", AHORA), "O-05")
    for nombre, imp, pr in (("importe_nan", NAN, 100.0), ("importe_cero", 0.0, 100.0), ("importe_negativo", -1.0, 100.0),
                            ("precio_infinito", 10000.0, INF), ("importe_bool", True, 100.0), ("precio_texto", 10000.0, "100")):
        R(f"inicio_con_{nombre}_no", o, lambda imp=imp, pr=pr: o.iniciar_sombra(imp, pr, "OPERADOR", AHORA), "O-01")
    r = o.iniciar_sombra(10000.0, 100.0, "OPERADOR", AHORA)
    h.chk("el_primer_dia_compra_el_indice_con_el_mismo_capital", r["ok"] and r["unidades"] == 100.0
          and o.sombra["entradas"][0]["indice"] == PARAMETROS["i_indice_sombra"], r)
    R("una_sola_vez", o, lambda: o.iniciar_sombra(5000.0, 100.0, "OPERADOR", AHORA), "O-02")
    r = o.movimiento_sombra("APORTE", 1100.0, 110.0, "OPERADOR", AHORA)
    h.chk("un_aporte_se_replica_al_precio_de_ese_momento", r["ok"] and abs(sb.estado_sombra(o.sombra["entradas"], 110.0, 0)["unidades"] - 110.0) < 1e-9, r)
    r = o.movimiento_sombra("RETIRADA", 550.0, 110.0, "G", AHORA)
    h.chk("G_tambien_registra_una_retirada", r["ok"] and abs(sb.estado_sombra(o.sombra["entradas"], 110.0, 0)["unidades"] - 105.0) < 1e-9, r)
    R("una_retirada_mayor_que_la_sombra_no", o, lambda: o.movimiento_sombra("RETIRADA", 1e6, 110.0, "OPERADOR", AHORA), "O-06")
    R("tipo_de_movimiento_invalido", o, lambda: o.movimiento_sombra("DIVIDENDO", 10.0, 110.0, "OPERADOR", AHORA), "O-01")
    R("otro_actor_no_registra_movimientos", o, lambda: o.movimiento_sombra("APORTE", 10.0, 110.0, "BROKER", AHORA), "O-05")
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
    mes, t = meses_desde(25)
    r = o4.comparar_sombra(mes, 9000.0, 120.0, 100.0, 110.0, 0.0, "I", t)
    h.chk("con_el_registro_tocado_no_se_compara_y_salta_el_kill", r["codigo"] == "O-13" and o4.kill is not None, r)
    t_ = pe.volcar(o2, meses_desde(24)[1])
    rc = pe.cargar(t_)
    h.chk("guardar_y_cargar_conserva_la_sombra", rc["ok"] and rc["orquestador"].sombra == o2.sombra and rc["orquestador"].integridad() == [],
          rc.get("motivo"))

    # ------------------------------------------------------------------ el cálculo, solo
    h.chk("estado_ilegible_es_None", sb.estado_sombra([{"tipo": "INICIO"}], 100.0, 0) is None
          and sb.estado_sombra([{"tipo": "INICIO", "importe_eur": 1.0, "precio_indice": 0.0}], 1.0, 0) is None)
    h.chk("comparar_con_inflacion_imposible_es_None", sb.comparar(1.0, 0.0, 0.0, {"valor_eur": 1.0, "aportado_neto_eur": 1.0}, 0.0, 1.0) is None)
    h.chk("veredicto_en_el_borde", sb.veredicto(23, {"supera": False}) == "EN_PLAZO" and sb.veredicto(24, {"supera": False}) == "PROPONER_PASIVA"
          and sb.veredicto(24, {"supera": True}) == "SUPERA")
    h.chk("meses_entre", sb.meses_entre("2026-11", "2028-11") == 24 and sb.meses_entre("2026-12", "2027-01") == 1)

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO SOMBRA T-76:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
