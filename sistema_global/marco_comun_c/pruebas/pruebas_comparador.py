"""Pruebas de D (comparador). Datos SIMULADOS, a partir de los sobres válidos de ejemplo.

Uso: python3 pruebas/pruebas_comparador.py
"""
import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from comparador import comparar_candidatos  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, sobre  # noqa: E402


def cand(n, esperado=(10.0, 0.5, -5.0), conf=0.6, instrumento=None, clase="Q", direccion="LARGO", ev=(0.5, 0.3, 0.2), exclu=None, estado="ESTIMADO"):
    s = copy.deepcopy(sobre(n))
    p = s["payload"]
    p["identificacion"]["instrumento"] = f"PAR{n}" if instrumento is None else instrumento
    p["identificacion"]["clase_comparabilidad"] = clase
    p["identificacion"]["direccion"] = direccion
    p["capa3"]["confianza"] = conf
    p["capa3"]["tope_confianza"] = max(conf, p["capa3"]["tope_confianza"])
    p["evidencia"]["proporcion"] = {"VERIFICADO": ev[0], "ESTIMADO": ev[1], "SUPUESTO": ev[2]}
    p["capa2"]["estado"] = estado
    p["capa2"]["escenarios"] = [{"nombre": "base", "probabilidad": 0.5, "rentabilidad_neta_pct": esperado[0], "horizonte_dias": 30},
                                {"nombre": "neutro", "probabilidad": 0.3, "rentabilidad_neta_pct": esperado[1], "horizonte_dias": 30},
                                {"nombre": "adverso", "probabilidad": 0.2, "rentabilidad_neta_pct": esperado[2], "horizonte_dias": 30}]
    if exclu:
        p["exclusiones_duras"][exclu[0]] = exclu[1]
    return {"expediente_id": f"EXP-{n:04d}", "sobre": s}


def main():
    h = Arnes()
    a, b = cand(1), cand(2, esperado=(3.0, 0.5, -4.0))
    r = comparar_candidatos([a, b], AHORA)
    g = r["grupos"]["Q"]
    h.chk("ordena_por_puntuacion", r["ok"] and [x["expediente_id"] for x in g["ranking"]] == ["EXP-0001", "EXP-0002"] and g["decision"] == "CLARA" and g["primero"] == "EXP-0001", r)
    r2 = comparar_candidatos([b, a], AHORA)
    h.chk("el_orden_de_entrada_no_cambia_el_resultado", r == r2)
    h.chk("determinista_y_no_muta", comparar_candidatos([a, b], AHORA) == r and a == cand(1))
    # puntuación a mano: esperado = .5*10 + .3*.5 + .2*-5 = 4.15 ; riesgo 5 ; conf .6 ; ev = .5 + .15 + .05 = .7
    h.chk("puntuacion_calculada_a_mano", abs(g["ranking"][0]["puntuacion"] - 4.15 / 5 * 0.6 * 0.7) < 1e-12, g["ranking"][0])
    # ajustada
    r = comparar_candidatos([cand(1), cand(2, instrumento="OTRO")], AHORA)
    h.chk("candidatos_casi_iguales_AJUSTADA_sin_primero", r["grupos"]["Q"]["decision"] == "AJUSTADA" and r["grupos"]["Q"]["primero"] is None, r)
    h.chk("empate_exacto_desempata_por_id_y_es_AJUSTADA", [x["expediente_id"] for x in r["grupos"]["Q"]["ranking"]] == ["EXP-0001", "EXP-0002"])
    # exclusiones
    for nombre, c, motivo in (("exclusion_bloqueada", cand(3, exclu=("sanciones", "BLOQUEADO")), "EXCLUSION_DURA"),
                              ("exclusion_desconocida", cand(3, exclu=("acceso", "DESCONOCIDO")), "EXCLUSION_DURA"),
                              ("sin_estimar", cand(3, estado="NO_ESTIMABLE"), "SIN_ESCENARIOS")):
        r = comparar_candidatos([a, b, c], AHORA)
        h.chk(nombre + "_se_excluye_y_el_resto_se_compara", r["ok"] and {"expediente_id": "EXP-0003", "motivo": motivo} in r["excluidos"] and len(r["grupos"]["Q"]["ranking"]) == 2, r)
    c = cand(3); c["sobre"]["payload"]["capa2"]["escenarios"][0]["probabilidad"] = 0.9
    h.chk("probabilidades_que_no_suman_uno_excluye", {"expediente_id": "EXP-0003", "motivo": "SIN_ESCENARIOS"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    c = cand(3); c["sobre"]["payload"]["capa2"]["escenarios"][0]["rentabilidad_neta_pct"] = float("nan")
    h.chk("nan_en_escenarios_excluye", {"expediente_id": "EXP-0003", "motivo": "SIN_ESCENARIOS"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    c = cand(3); c["sobre"]["valid_until"] = "2026-11-06T08:00:00+00:00"
    h.chk("sobre_caducado_excluye", {"expediente_id": "EXP-0003", "motivo": "CADUCADO"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    c = cand(3); c["sobre"]["emitido_en"] = "2026-11-07T08:00:00+00:00"
    h.chk("sobre_del_futuro_excluye", {"expediente_id": "EXP-0003", "motivo": "CADUCADO"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    c = cand(3); del c["sobre"]["payload"]["capa3"]
    h.chk("campo_ausente_excluye_sin_lanzar", {"expediente_id": "EXP-0003", "motivo": "FORMA"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    c = cand(3, ev=(0.9, 0.9, 0.9))
    h.chk("evidencia_que_no_suma_uno_excluye", {"expediente_id": "EXP-0003", "motivo": "FORMA"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    c = cand(3, conf=1.5)
    h.chk("confianza_fuera_de_rango_excluye", {"expediente_id": "EXP-0003", "motivo": "FORMA"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    # duplicados
    r = comparar_candidatos([a, b, cand(1, instrumento="X")], AHORA)
    h.chk("expediente_repetido_se_excluye_los_dos", sum(1 for x in r["excluidos"] if x["motivo"] == "DUPLICADO") == 2 and r["codigo"] == "D-03", r)
    r = comparar_candidatos([a, b, cand(3, instrumento=a["sobre"]["payload"]["identificacion"]["instrumento"])], AHORA)
    h.chk("mismo_instrumento_y_sentido_no_son_alternativas", any(x["motivo"] == "DUPLICADO" for x in r["excluidos"]), r)
    r = comparar_candidatos([a, b, cand(3, instrumento=a["sobre"]["payload"]["identificacion"]["instrumento"], direccion="CORTO")], AHORA)
    h.chk("mismo_instrumento_en_sentido_contrario_si_se_compara", len(r["grupos"]["Q"]["ranking"]) == 3, r)
    # clases
    r = comparar_candidatos([a, b, cand(3, clase="S"), cand(4, clase="S", esperado=(3.0, 0.0, -2.0))], AHORA)
    h.chk("no_mezcla_clases", set(r["grupos"]) == {"Q", "S"} and all(len(v["ranking"]) == 2 for v in r["grupos"].values()), r)
    r = comparar_candidatos([a, cand(3, clase="S")], AHORA)
    h.chk("una_sola_en_cada_clase_D03", r["codigo"] == "D-03" and not r["ok"], r)
    # retorno no positivo: no hay nada que ordenar
    r = comparar_candidatos([cand(1, esperado=(-1.0, -2.0, -8.0)), cand(2, esperado=(-1.0, -2.0, -3.0))], AHORA)
    h.chk("retorno_negativo_no_se_ordena_D03", r["codigo"] == "D-03" and all(x["motivo"] == "SIN_RETORNO_POSITIVO" for x in r["excluidos"]), r)
    r = comparar_candidatos([cand(5, esperado=(-1.0, -1.0, -2.0)), cand(6, esperado=(-2.0, -2.0, -10.0)), a, b], AHORA)
    h.chk("los_perdedores_no_entran_en_el_ranking", r["ok"] and [x["expediente_id"] for x in r["grupos"]["Q"]["ranking"]] == ["EXP-0001", "EXP-0002"]
          and {"expediente_id": "EXP-0005", "motivo": "SIN_RETORNO_POSITIVO"} in r["excluidos"] and {"expediente_id": "EXP-0006", "motivo": "SIN_RETORNO_POSITIVO"} in r["excluidos"], r)
    # revisión independiente
    import itertools
    x1, x2 = cand(1, instrumento="X"), cand(2, instrumento="X", esperado=(5.0, 0.0, -5.0))
    c3, c4 = cand(3), cand(4, esperado=(2.0, 0.0, -4.0))
    res = {str(comparar_candidatos(list(pm), AHORA)) for pm in itertools.permutations([x1, x2, c3, c4])}
    h.chk("duplicado_por_instrumento_no_depende_del_orden", len(res) == 1, len(res))
    r = comparar_candidatos([x1, x2, c3, c4], AHORA)
    h.chk("del_duplicado_se_queda_el_mejor", {"expediente_id": "EXP-0002", "motivo": "DUPLICADO"} in r["excluidos"], r)
    r = comparar_candidatos([cand(1, instrumento="X"), cand(2, instrumento="X", clase="S"), cand(3), cand(4, clase="S")], AHORA)
    h.chk("mismo_instrumento_en_otra_clase_no_es_duplicado", not any(x["motivo"] == "DUPLICADO" for x in r["excluidos"]), r)
    r = comparar_candidatos([cand(1, instrumento="BTC"), cand(2, instrumento="btc "), cand(3)], AHORA)
    h.chk("instrumento_normalizado_para_detectar_duplicados", any(x["motivo"] == "DUPLICADO" for x in r["excluidos"]), r)
    for nombre, inst in (("vacio", ""), ("solo_espacios", "  ")):
        h.chk("instrumento_" + nombre + "_excluye", {"expediente_id": "EXP-0003", "motivo": "FORMA"} in comparar_candidatos([a, b, cand(3, instrumento=inst)], AHORA)["excluidos"])
    c = cand(3); c["sobre"]["payload"]["capa2"]["escenarios"] = [
        {"nombre": "a", "probabilidad": 0.5000005, "rentabilidad_neta_pct": 1.7e308, "horizonte_dias": 1}, {"nombre": "b", "probabilidad": 0.5, "rentabilidad_neta_pct": 1.7e308, "horizonte_dias": 1}]
    h.chk("desborde_a_infinito_excluye", {"expediente_id": "EXP-0003", "motivo": "SIN_ESCENARIOS"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    c = cand(3, conf=0.0)
    r = comparar_candidatos([a, b, c], AHORA)
    h.chk("confianza_cero_no_da_nan", all(x["puntuacion"] == x["puntuacion"] for x in r["grupos"]["Q"]["ranking"]), r)
    pm = {str(comparar_candidatos(list(p), AHORA)) for p in itertools.permutations([a, b, cand(3, conf=0.0)])}
    h.chk("con_confianza_cero_el_resultado_no_depende_del_orden", len(pm) == 1)
    c = cand(3); c["sobre"]["payload"]["evidencia"]["proporcion"] = {"VERIFICADO": 1.0, "ESTIMADO": 1.0, "SUPUESTO": 0.0, "X": -1.0}
    h.chk("clave_extra_en_evidencia_excluye", {"expediente_id": "EXP-0003", "motivo": "FORMA"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    for nombre, ex in (("falta_una", {"sanciones": "OK"}), ("clave_extra", {"sanciones": "OK", "invertibilidad": "OK", "acceso": "OK", "x": "OK"})):
        c = cand(3); c["sobre"]["payload"]["exclusiones_duras"] = ex
        h.chk("exclusiones_" + nombre + "_excluye", {"expediente_id": "EXP-0003", "motivo": "FORMA"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    c = cand(3); c["sobre"]["payload"]["capa2"]["escenarios"].append({"nombre": "cola", "probabilidad": 0.0, "rentabilidad_neta_pct": -100.0, "horizonte_dias": 30})
    r = comparar_candidatos([a, b, c], AHORA)
    h.chk("escenario_de_probabilidad_cero_no_cuenta_como_riesgo", r["ok"] and next(x for x in r["grupos"]["Q"]["ranking"] if x["expediente_id"] == "EXP-0003")["peor_escenario_pct"] == -5.0, r)
    c = cand(3); c["sobre"]["payload"]["capa2"]["escenarios"][0]["rentabilidad_neta_pct"] = 1e9
    h.chk("rentabilidad_absurda_excluye", {"expediente_id": "EXP-0003", "motivo": "SIN_ESCENARIOS"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    c = cand(3); c["sobre"]["payload"]["capa2"]["escenarios"] = [{"nombre": "unico", "probabilidad": 1.0, "rentabilidad_neta_pct": 9.0, "horizonte_dias": 30}]
    h.chk("un_solo_escenario_excluye", {"expediente_id": "EXP-0003", "motivo": "SIN_ESCENARIOS"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    c = cand(3); c["sobre"]["payload"]["capa2"]["escenarios"][0]["horizonte_dias"] = 0
    h.chk("horizonte_invalido_excluye", {"expediente_id": "EXP-0003", "motivo": "SIN_ESCENARIOS"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    c = cand(3); c["sobre"]["expediente_id"] = "OTRO-9999"
    h.chk("id_del_sobre_distinto_del_del_envoltorio_excluye", {"expediente_id": "EXP-0003", "motivo": "FORMA"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    c = cand(3); c["sobre"]["resultado_politica"]["resultado"] = "RECHAZADO"
    h.chk("politica_rechazada_excluye", {"expediente_id": "EXP-0003", "motivo": "EXCLUSION_DURA"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    c = cand(3); c["sobre"]["payload"]["capa3"]["tope_confianza"] = 0.1
    h.chk("confianza_sobre_el_tope_excluye", {"expediente_id": "EXP-0003", "motivo": "FORMA"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    c = cand(3); c["sobre"]["valid_until"] = AHORA
    h.chk("valid_until_igual_a_ahora_es_caducado", {"expediente_id": "EXP-0003", "motivo": "CADUCADO"} in comparar_candidatos([a, b, c], AHORA)["excluidos"])
    h.chk("ahora_en_formato_laxo_D01", comparar_candidatos([a, b], "2026-11-06T10+00:00")["codigo"] == "D-01")
    class Veneno(dict):
        def __getitem__(self, k):
            raise RuntimeError("veneno")
    r = comparar_candidatos([a, b, Veneno({"expediente_id": "E9", "sobre": {}})], AHORA)
    h.chk("un_candidato_envenenado_no_anula_a_los_demas", r["codigo"] == "OK" and len(r["grupos"]["Q"]["ranking"]) == 2 and {"expediente_id": None, "motivo": "FORMA"} in r["excluidos"], r)
    # entrada inválida
    for nombre, args in (("una_sola", ([a], AHORA)), ("no_lista", ("x", AHORA)), ("sin_sobre", ([{"expediente_id": "E"}, a], AHORA)),
                         ("ahora_ilegible", ([a, b], "ayer")), ("ahora_none", ([a, b], None)), ("campos_extra", ([{**a, "x": 1}, b], AHORA))):
        r = comparar_candidatos(*args)
        h.chk("entrada_" + nombre + "_D01", r["codigo"] == "D-01" and not r["ok"] and r["grupos"] == {}, r)
    h.chk("candidato_basura_no_lanza", comparar_candidatos([a, b, {"expediente_id": 5, "sobre": None}] if False else [a, b, {"expediente_id": "E9", "sobre": 5}], AHORA)["ok"])
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO D:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
