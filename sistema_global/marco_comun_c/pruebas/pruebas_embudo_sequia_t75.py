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
          and "60 días" in av[0]["motivo"] and "entran 2" in av[0]["motivo"] and av[0]["prioridad"] == "MEDIA", (r, av))
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
    h.chk("con_una_inversion_en_el_plazo_no_hay_sequia", not sq["activa"] and sq["invertidas"] == 1 and not o40(o3), sq)

    o4 = antiguo()
    sq = o4.sequia(mas(AHORA, hours=1))
    h.chk("sin_candidatos_que_pasaran_el_analisis_no_hay_sequia", not sq["activa"] and sq["validadas"] == 0
          and sq["motivo"] == "ningún candidato pasó el análisis", sq)

    sq = o.sequia(mas(AHORA, days=61))   # la validación ya cae fuera del plazo
    h.chk("lo_validado_fuera_del_plazo_no_cuenta", not sq["activa"] and sq["validadas"] == 0, sq)
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
