"""Pruebas de T-75 y T-89 (V0.70): contrapesos de la abstención de la Constitución V0.6 (D-22) — embudo visible en N y alarma de
sequía a los 60 días (D-27, P-17) — y tope del tiempo sin contrastar del reloj (QA de T-72, H-03). Datos SIMULADOS.

Uso: python3 pruebas/pruebas_embudo_sequia_t75.py
"""
import copy
import sys
from datetime import datetime, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import reloj as rl  # noqa: E402
from consola import informe_embudo  # noqa: E402
from orquestador import PRIORIDAD_AVISO, Orquestador  # noqa: E402
from parametros import PARAMETROS  # noqa: E402
from pruebas_k import CAL  # noqa: E402
from pruebas_orquestador import AHORA, CFG, S1, Arnes, hasta, registrar_motor  # noqa: E402

T0 = "2026-09-01T09:00:00+00:00"   # el sistema arranca más de 60 días antes de AHORA


def mas(t, **kw):
    return (datetime.fromisoformat(t) + timedelta(**kw)).isoformat()


def antiguo():
    """Un Orquestador que lleva funcionando desde T0 (su primera anotación es de entonces) y con el sello y el Motor de AHORA."""
    o = Orquestador(dict(CFG), CAL)
    assert o.degradar("TRADING", "arranque de prueba: el operador deja TRADING en L1", "OPERADOR", T0)["ok"]
    assert o.registrar_sello(S1, AHORA)["ok"]
    registrar_motor(o, S1["sello_id"])
    return o


def o40(o):
    return [x for x in o.avisos if x["codigo"] == "O-40"]


def main():
    h = Arnes()
    h.chk("los_numeros_son_los_ratificados", PARAMETROS["o_dias_sequia"] == 60 and PARAMETROS["n_dias_embudo"] == 7
          and PRIORIDAD_AVISO["O-40"] == "MEDIA")

    # ------------------------------------------------------------------ alarma de sequía
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    hasta(o, "VALIDADA", 3)
    assert o.descartar("EXP-0003", "el operador lo descarta: no le convence", "OPERADOR", AHORA)["ok"]
    sq = o.sequia(mas(AHORA, hours=1))
    h.chk("sin_inversiones_y_con_candidatos_validados_hay_sequia", sq["activa"] and sq["validadas"] == 2 and sq["invertidas"] == 0
          and sq["dias"] == 60, sq)
    r = o.barrer(mas(AHORA, hours=1))
    av = o40(o)
    h.chk("barrer_avisa_al_operador_con_el_embudo", r["ok"] and ("sequia", sq["desde"], 2) in r["cambios"] and len(av) == 1
          and "(plazo 60)" in av[0]["motivo"] and "entran 2" in av[0]["motivo"] and av[0]["prioridad"] == "MEDIA", (r, av))
    o.barrer(mas(AHORA, hours=2))
    h.chk("una_sola_alarma_por_plazo_aunque_se_acuse", len(o40(o)) == 1)
    assert o.acusar_aviso(av[0]["id"], "OPERADOR", mas(AHORA, hours=3))["ok"]
    o.barrer(mas(AHORA, hours=4))
    h.chk("acusarla_no_la_repite_dentro_del_plazo", len(o40(o)) == 1)

    o2 = Orquestador(dict(CFG), CAL)   # un sistema más joven que el plazo
    assert o2.registrar_sello(S1, AHORA)["ok"]
    registrar_motor(o2, S1["sello_id"])
    hasta(o2, "VALIDADA", 1)
    sq = o2.sequia(mas(AHORA, hours=1))
    o2.barrer(mas(AHORA, hours=1))
    h.chk("un_sistema_mas_joven_que_el_plazo_no_juzga_sequia", not sq["activa"] and sq["motivo"] == "el sistema lleva menos del plazo"
          and not o40(o2), sq)

    o3 = antiguo()
    hasta(o3, "EJECUTADA", 1)
    sq = o3.sequia(mas(AHORA, hours=1))
    o3.barrer(mas(AHORA, hours=1))
    h.chk("con_una_inversion_en_el_plazo_no_hay_sequia", not sq["activa"] and "desde la última inversión" in sq["motivo"] and not o40(o3), sq)

    o4 = antiguo()
    sq = o4.sequia(mas(AHORA, hours=1))
    h.chk("sin_candidatos_que_pasaran_el_analisis_no_hay_sequia", not sq["activa"] and sq["validadas"] == 0
          and sq["motivo"] == "ningún candidato pasó el análisis", sq)

    sq = o.sequia(mas(AHORA, days=61))   # QA r01, H-08: la sequía sigue mientras no se invierta (antes la ventana deslizante la perdía)
    h.chk("la_sequia_sigue_hasta_la_siguiente_inversion_H08", sq["activa"] and sq["validadas"] == 2, sq)
    sq = o3.sequia(mas(AHORA, days=61))
    h.chk("lo_validado_antes_de_la_ultima_inversion_no_cuenta", not sq["activa"] and sq["validadas"] == 0, sq)

    # QA r01, H-08: inversión a las 09:00, validación a las 10:00 y barridos diarios a las 08:00 durante 90 días: un aviso
    o5 = antiguo()
    hasta(o5, "EJECUTADA", 1)   # se invierte a AHORA (09:00)
    hasta(o5, "VALIDADA", 5, ahora=mas(AHORA, hours=1))   # un candidato validado a las 10:00, que nadie invierte
    for d in range(1, 91):
        o5.barrer(mas(AHORA, days=d, hours=-1))
    h.chk("con_barridos_diarios_la_alarma_salta_H08", len(o40(o5)) == 1, [x["ahora"] for x in o40(o5)])
    for d in range(91, 125):
        o5.barrer(mas(AHORA, days=d, hours=-1))
    h.chk("y_se_repite_una_vez_por_plazo_mientras_dure", len(o40(o5)) == 2, [x["ahora"] for x in o40(o5)])
    h.chk("plazo_ilegible_no_juzga_H07", o.sequia(mas(AHORA, days=61), dias=0)["activa"] is False
          and o.sequia(mas(AHORA, days=61), dias=True)["activa"] is False and o.sequia(mas(AHORA, days=61), dias=2.5)["activa"] is False)
    h.chk("sequia_con_instante_ilegible_no_salta_ni_lanza", o.sequia("ayer")["activa"] is False and o.sequia(None)["activa"] is False)
    antes = copy.deepcopy(o.__dict__)
    o.sequia(mas(AHORA, hours=5))
    o.embudo(AHORA, mas(AHORA, hours=5))
    h.chk("sequia_y_embudo_solo_leen", antes == o.__dict__)

    # ------------------------------------------------------------------ embudo visible
    em = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, hours=1))
    capas = {x["expediente_id"]: (x["capa"], x["actor"]) for x in em["oportunidades"]}
    h.chk("el_embudo_dice_cuantas_entran_y_en_que_capa_cae_cada_una", em["entran"] == 2
          and em["por_capa"] == {"DESCARTADA": 1, "VALIDADA": 1} and capas["EXP-0003"] == ("DESCARTADA", "OPERADOR"), em)
    h.chk("y_por_que_salen", [(x["expediente_id"], x["hasta"], x["actor"], x["motivo"]) for x in em["salidas"]]
          == [("EXP-0003", "DESCARTADA", "OPERADOR", "el operador lo descarta: no le convence")], em["salidas"])
    h.chk("y_cuantas_pasaron_el_analisis_y_se_invirtieron", em["validadas"] == 2 and em["invertidas"] == 0, em)
    em2 = o.embudo(mas(AHORA, hours=10), mas(AHORA, hours=11))
    h.chk("lo_anterior_al_periodo_no_entra", em2["entran"] == 0 and em2["salidas"] == [] and em2["validadas"] == 0, em2)
    h.chk("embudo_al_reves_o_ilegible_es_None", o.embudo(mas(AHORA, hours=1), AHORA) is None and o.embudo("x", AHORA) is None)
    em3 = o3.embudo(mas(AHORA, minutes=-1), mas(AHORA, hours=1))
    h.chk("una_inversion_cuenta_en_el_embudo", em3["invertidas"] == 1 and em3["por_capa"].get("EJECUTADA") == 1, em3)

    inf = informe_embudo(o, mas(AHORA, hours=1))
    h.chk("N_muestra_el_embudo_semanal_y_la_sequia", inf["ok"] and inf["dias"] == 7 and inf["embudo"]["entran"] == 2
          and inf["sequia"]["activa"] is True, inf)
    h.chk("informe_ilegible_no_lanza", informe_embudo(o, "ayer")["ok"] is False and informe_embudo(None, AHORA)["ok"] is False)
    h.chk("informe_con_dias_ilegibles_no_vale_H07", all(informe_embudo(o, AHORA, d)["ok"] is False for d in (0, -1, True, 2.5, "7")))

    # QA r01, H-01: el embudo dice que F paró la oportunidad, también cuando después caduca
    from pruebas_operador_t50 import vetado
    o6 = antiguo()
    hasta(o6, "PROPUESTA", 1)
    r = o6.autorizar("EXP-0001", "OPERADOR", vetado(o6), AHORA)
    em = o6.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    fila = next(x for x in em["oportunidades"] if x["expediente_id"] == "EXP-0001")
    h.chk("el_veto_de_F_queda_anotado_y_el_embudo_lo_dice_H01", r["codigo"] == "O-06" and fila["capa"] == "PROPUESTA"
          and fila["actor"] == "F" and "F-09" in fila["motivo"] and fila["bloqueo"] == fila["motivo"] and o6.integridad() == [], (r, fila))
    o6.barrer(mas(AHORA, days=3))
    em = o6.embudo(mas(AHORA, minutes=-1), mas(AHORA, days=3))
    sal = [x for x in em["salidas"] if x["expediente_id"] == "EXP-0001"]
    h.chk("y_su_caducidad_lleva_el_veto_como_causa_previa_H01", sal and sal[-1]["hasta"] == "CADUCADA" and "F-09" in (sal[-1]["bloqueo_previo"] or ""), sal)

    # QA r01, H-03 y H-04: se cuentan candidatos y oportunidades, no pasos; los bordes no se cuentan dos veces
    o7 = antiguo()
    hasta(o7, "VALIDADA", 1)
    assert o7.observar("EXP-0001", [{"tipo": "FECHA", "fecha": "2026-11-20"}], "el operador lo aparta", "OPERADOR", AHORA)["ok"]
    assert o7.descartar("EXP-0001", "el operador lo descarta del todo", "OPERADOR", AHORA)["ok"]
    for k in (1, 2):
        assert o7.abrir_directa(f"EXP-DD-0{k}", f"COR-DD-0{k}", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")["ok"] if k == 1 else True
    em = o7.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    h.chk("un_analisis_reutilizado_cuenta_una_vez_H03", em["validadas"] == 1, em)
    h.chk("una_oportunidad_que_sale_dos_veces_cuenta_una_H04", em["salen"] == 1 and len(em["salidas"]) == 2, em)
    w1 = o7.embudo(mas(AHORA, minutes=-1), AHORA)
    w2 = o7.embudo(AHORA, mas(AHORA, minutes=1))
    h.chk("dos_periodos_seguidos_no_cuentan_dos_veces_el_borde_H04", w1["entran"] + w2["entran"] == em["entran"]
          and w1["validadas"] + w2["validadas"] == em["validadas"], (w1["entran"], w2["entran"], em["entran"]))

    # ------------------------------------------------------------------ QA r02 de T-75 (ronda r03)
    import contratos as ct
    from pruebas_orquestador import nuevo
    # H-09: el veto que ve el operador en la pantalla (el camino normal) también se anota
    o8 = antiguo()
    hasta(o8, "PROPUESTA", 1)
    inf8 = vetado(o8)
    r = o8.pantalla_aprobacion("EXP-0001", inf8, AHORA)
    em = o8.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    fila = next(x for x in em["oportunidades"] if x["expediente_id"] == "EXP-0001")
    h.chk("el_veto_visto_en_la_pantalla_queda_anotado_H09", r["codigo"] == "O-06" and fila["actor"] == "F" and "F-09" in fila["motivo"]
          and fila["bloqueo"] == fila["motivo"] and o8.integridad() == [], (r, fila))
    h.chk("y_el_informe_no_se_puede_volver_a_usar_H09", o8.autorizar("EXP-0001", "OPERADOR", inf8, mas(AHORA, minutes=1))["codigo"] == "O-03")
    o8.barrer(mas(AHORA, days=3))
    sal = [x for x in o8.embudo(mas(AHORA, minutes=-1), mas(AHORA, days=3))["salidas"] if x["expediente_id"] == "EXP-0001"]
    h.chk("y_la_caducidad_lleva_el_veto_como_causa_previa_H09", sal and "F-09" in (sal[-1]["bloqueo_previo"] or ""), sal)
    # H-10: la propuesta CT-G-06 en vigor no cambia por el veto: la emite su gestor y sigue siendo válida
    o9 = antiguo()
    hasta(o9, "PROPUESTA", 1)
    p1 = ct.propuesta(o9, "EXP-0001")
    r = o9.autorizar("EXP-0001", "OPERADOR", vetado(o9), mas(AHORA, minutes=5))
    p2 = ct.propuesta(o9, "EXP-0001")
    h.chk("la_propuesta_tras_el_veto_es_la_misma_y_valida_H10", r["codigo"] == "O-06" and p2 == p1 and p2["producer"] != "F"
          and ct.validar(p2) == [], (r, p2 and p2["producer"]))
    # H-11: una llamada rechazada que deja una anotación no deja anotar nada antes de ella
    o10 = antiguo()
    hasta(o10, "PROPUESTA", 1)
    assert o10.autorizar("EXP-0001", "OPERADOR", vetado(o10), mas(AHORA, minutes=30))["codigo"] == "O-06"
    r = o10.descartar("EXP-0001", "el gestor lo descarta antes del veto", "GESTOR_TACTICA", mas(AHORA, minutes=10))
    horas = [x["ahora"] for x in o10.expedientes["EXP-0001"]["historial"]]
    h.chk("tras_el_veto_no_se_anota_nada_anterior_H11", not r["ok"] and r["codigo"] == "O-16"
          and horas == sorted(horas, key=lambda t: datetime.fromisoformat(t)), (r, horas))
    h.chk("y_despues_del_veto_si_se_puede_descartar_H11",
          o10.descartar("EXP-0001", "el gestor lo descarta tras el veto", "GESTOR_TACTICA", mas(AHORA, minutes=31))["ok"])
    # H-14: un sistema más joven que el plazo no juzga, hasta el microsegundo
    o11 = nuevo()
    hasta(o11, "VALIDADA", 1)
    primero = o11._primer_instante().isoformat()
    antes, justo = o11.sequia(mas(primero, days=60, microseconds=-1)), o11.sequia(mas(primero, days=60))
    h.chk("la_edad_se_mide_desde_el_primer_instante_real_H14", antes["activa"] is False and justo["activa"] is True, (antes["motivo"], justo["motivo"]))

    # ------------------------------------------------------------------ QA r03 de T-75 (T-100, marco V0.76)
    from pruebas_orquestador import encargo, sobre_para
    # H-15 (sonda n01): un análisis nuevo anterior al periodo también borra el veto anterior
    o12 = antiguo()
    hasta(o12, "PROPUESTA", 1)
    assert o12.pantalla_aprobacion("EXP-0001", vetado(o12), AHORA)["codigo"] == "O-06"
    t1, t2, t3, t4 = (mas(AHORA, minutes=m) for m in (1, 2, 3, 10))
    assert o12.observar("EXP-0001", [{"tipo": "PRECIO", "instrumento": "EURUSD", "operador": ">=", "umbral": 1.12}], "esperar", "GESTOR_TACTICA", t1)["ok"]
    assert o12.reabrir("EXP-0001", "cambió el contexto", "OPERADOR", t2)["ok"]
    enc = encargo(1); enc["event_id"] = "EV-ENC-0101"
    assert o12.emitir_encargo("EXP-0001", enc, "GESTOR_TACTICA", t2)["ok"]
    s = sobre_para(1, None); s["event_id"] = "EV-SOB-0001-R"
    assert o12.entregar_sobre("EXP-0001", s, t3)["ok"]
    assert o12.descartar("EXP-0001", "el operador lo descarta tras el nuevo análisis", "OPERADOR", t4)["ok"]
    previo = [[x["bloqueo_previo"] for x in o12.embudo(d, t4)["salidas"] if x["hasta"] == "DESCARTADA"][-1]
              for d in (mas(AHORA, minutes=-1), mas(AHORA, minutes=5))]
    h.chk("tras_un_analisis_nuevo_el_veto_no_es_la_causa_mire_el_periodo_que_mire_H15", previo == [None, None], previo)
    # H-17 (sonda q03): tras el veto visto en la pantalla, nada anterior entra; un rechazo que no anota no adelanta el reloj
    o13 = antiguo()
    hasta(o13, "PROPUESTA", 1)
    r = o13.pantalla_aprobacion("EXP-0001", vetado(o13), mas(AHORA, minutes=30))
    h.chk("tras_el_veto_de_la_pantalla_el_reloj_se_queda_en_el_veto_H17", r["codigo"] == "O-06" and o13.ultimo_ahora == mas(AHORA, minutes=30), r)
    R = h.rechaza
    R("y_nada_anterior_al_veto_de_la_pantalla_entra_H17", o13,
      lambda: o13.descartar("EXP-0001", "antes del veto", "GESTOR_TACTICA", mas(AHORA, minutes=10)), "O-16")
    rx = o13.autorizar("EXP-0001", "OPERADOR", {}, mas(AHORA, minutes=50))
    h.chk("un_rechazo_que_no_anota_sigue_sin_adelantar_el_reloj_H17", rx["codigo"] == "O-01" and o13.ultimo_ahora == mas(AHORA, minutes=30), rx)

    # ------------------------------------------------------------------ T-89: tope del tiempo sin contrastar
    for c in (rl.TOPE_SIN_CONTRASTE_S * 2, 1e12, 1e308):
        try:
            rl.Reloj(lambda: 1.8e9, lambda: 1.0, max_sin_contraste_s=c)
            aceptado = True
        except ValueError:
            aceptado = False
        h.chk(f"contraste_de_{c:g}_s_se_rechaza_H03", not aceptado)
    r = rl.Reloj(lambda: 1.8e9, lambda: 1.0, max_sin_contraste_s=rl.TOPE_SIN_CONTRASTE_S)
    h.chk("el_tope_exacto_se_admite", r.max_sin_contraste_s == rl.TOPE_SIN_CONTRASTE_S == 7 * 24 * 3600.0)
    r._tol = (r._tol[0], r._tol[1], 1e12)
    h.chk("y_por_encima_del_tope_en_lo_privado_no_vale", r.max_sin_contraste_s != r.max_sin_contraste_s)   # NaN

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO EMBUDO Y SEQUÍA T-75:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
