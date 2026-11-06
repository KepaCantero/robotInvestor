"""Pruebas de T-17: D descuenta costes, verifica el riesgo y la confianza declarados y compara horizontes distintos en la misma
unidad. La puntuación ya no premia lo que el productor declare. Datos SIMULADOS."""
from __future__ import annotations

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

from comparador import COSTE_SUELO_IV, FACTOR_SIN_DOBLE, RIESGO_SIN_STOP_LARGO, TOPE_CLASE, comparar_candidatos  # noqa: E402
from parametros import VERSION_PARAMETROS  # noqa: E402
from pruebas_comparador import cand  # noqa: E402
from pruebas_orquestador import AHORA, Arnes  # noqa: E402


def uno(c):
    r = comparar_candidatos([c], AHORA)
    if not r["grupos"]:
        return None, r
    return next(iter(r["grupos"].values()))["ranking"][0], r


def con_horizonte(c, h, esperado=None):
    for e in c["sobre"]["payload"]["capa2"]["escenarios"]:
        e["horizonte_dias"] = h
    c["sobre"]["payload"]["capa2"]["horizonte_dias"] = h
    if esperado:
        for e, v in zip(c["sobre"]["payload"]["capa2"]["escenarios"], esperado):
            e["rentabilidad_neta_pct"] = v
        c["sobre"]["payload"]["capa2"]["distribucion"] = {"p05": esperado[2], "p50": esperado[1], "p95": esperado[0]}
    return c


def con_stop(c, limite, stop):
    es = c["sobre"]["payload"]["entrada_salida"]
    es["entrada"]["limite"]["valor"] = limite
    es["stop"] = {"valor": stop, "unidad": "USD", "estado": "SUPUESTO"}
    return c


def sin_stop(c):
    c["sobre"]["payload"]["entrada_salida"]["stop"] = {"valor": None, "unidad": "USD", "estado": "NO_ESTIMABLE"}
    return c


def main():
    h = Arnes()
    base, _ = uno(cand(1))
    h.chk("base_sin_ajustes", base["ajustes"] == [] and base["coste_descontado_pct"] == 0 and base["riesgo_pct"] == 5.0, base)

    # ---------------------------------------------------------------- (1) costes
    c = cand(1)
    for k in ("entrada", "salida"):
        c["sobre"]["payload"]["costes"][k] = {"valor": None, "unidad": "pb", "estado": "NO_ESTIMABLE"}
    d, _ = uno(c)
    h.chk("coste_no_estimado_se_descuenta_el_suelo", d["ajustes"] == ["COSTE_SUELO"] and abs(d["coste_descontado_pct"] - COSTE_SUELO_IV["Q"] / 100) < 1e-12
          and abs(d["retorno_esperado_pct"] - (base["retorno_esperado_pct"] - 0.02)) < 1e-12 and abs(d["peor_escenario_pct"] - (-5.02)) < 1e-12, d)
    c = cand(1)
    c["sobre"]["payload"]["costes"]["entrada"]["valor"] = 0
    c["sobre"]["payload"]["costes"]["salida"]["valor"] = 0.5
    d, _ = uno(c)
    h.chk("coste_declarado_bajo_el_suelo_se_completa", abs(d["coste_descontado_pct"] - 0.015) < 1e-12 and "COSTE_SUELO" in d["ajustes"], d)
    c = cand(1)
    for k in ("entrada", "salida"):
        c["sobre"]["payload"]["costes"][k]["unidad"] = "EUR"   # en otra unidad no se puede sumar: cuenta como no declarado
    d, _ = uno(c)
    h.chk("coste_en_otra_unidad_no_cuenta", "COSTE_SUELO" in d["ajustes"] and abs(d["coste_descontado_pct"] - 0.02) < 1e-12, d)
    c = cand(1, clase="K", conf=0.3)
    d, _ = uno(c)
    h.chk("suelo_de_la_clase_K", abs(d["coste_descontado_pct"] - (COSTE_SUELO_IV["K"] - 4) / 100) < 1e-12, d)
    c = con_horizonte(cand(1), 365, (0.22, 0.05, -0.05))   # a un año: exceso 0,115 % > 0,10 % antes de costes; 0,095 % después
    for k in ("entrada", "salida"):
        c["sobre"]["payload"]["costes"][k] = {"valor": None, "unidad": "pb", "estado": "NO_ESTIMABLE"}
    c["sobre"]["payload"]["costes"]["mantenimiento_anual"]["valor"] = 0
    d, r = uno(c)
    h.chk("tras_costes_no_supera_la_referencia", d is None and r["excluidos"][0]["motivo"] == "NO_SUPERA_REFERENCIA", r)

    # ---------------------------------------------------------------- (2) riesgo verificado
    c = con_stop(cand(1), 1.10, 1.00)   # 9,09 % hasta el stop, más 4 pb de ida y vuelta
    d, _ = uno(c)
    h.chk("riesgo_hasta_el_stop", "RIESGO_STOP" in d["ajustes"] and abs(d["riesgo_pct"] - (0.1 / 1.10 * 100 + 0.04)) < 1e-9 and d["puntuacion"] < base["puntuacion"], d)
    c = con_stop(cand(1, direccion="CORTO"), 1.10, 1.21)
    d, _ = uno(c)
    h.chk("riesgo_hasta_el_stop_en_corto", "RIESGO_STOP" in d["ajustes"] and abs(d["riesgo_pct"] - (11 / 1.10 + 0.04)) < 1e-9, d)
    c = con_stop(cand(1), 1.10, 1.09)   # stop más cerca que el peor escenario: manda el escenario
    d, _ = uno(c)
    h.chk("stop_cercano_no_cambia_el_riesgo", "RIESGO_STOP" not in d["ajustes"] and d["riesgo_pct"] == 5.0, d)
    c = cand(1)
    c["sobre"]["payload"]["capa2"]["distribucion"]["p05"] = -8.0
    d, _ = uno(c)
    h.chk("riesgo_p05_declarado", d["ajustes"] == ["RIESGO_P05"] and d["riesgo_pct"] == 8.0, d)
    # el productor que declara un adverso muy suave con el stop lejos ya no gana al honesto
    honesto = con_stop(cand(1, esperado=(10.0, 0.5, -9.0)), 1.10, 1.00)
    listo = con_stop(cand(2, esperado=(10.0, 0.5, -0.5)), 1.10, 1.00)
    listo["sobre"]["payload"]["capa2"]["distribucion"]["p05"] = -0.5
    r = comparar_candidatos([honesto, listo], AHORA)
    rk = {x["expediente_id"]: x for x in r["grupos"]["Q"]["ranking"]}
    h.chk("adverso_suave_no_abarata_el_riesgo", rk["EXP-0002"]["riesgo_pct"] == rk["EXP-0001"]["riesgo_pct"], rk)

    # ---------------------------------------------------------------- (3) horizontes en la misma unidad
    corto = con_horizonte(cand(1), 30, (4.0, 1.0, -2.0))      # 2,1 % en 30 días con un 2 % de riesgo
    largo = con_horizonte(cand(2), 365, (12.0, 4.0, -6.0))    # 6 % en un año con un 6 % de riesgo: sin normalizar, gana el largo
    dc, _ = uno(corto)
    dl, _ = uno(largo)
    k = 365 / 30
    h.chk("exceso_anualizado_y_riesgo_por_raiz", abs(dc["exceso_anual_pct"] - dc["exceso_sobre_referencia_pct"] * k) < 1e-9
          and abs(dc["riesgo_anual_pct"] - dc["riesgo_pct"] * k ** 0.5) < 1e-9 and abs(dl["exceso_anual_pct"] - dl["exceso_sobre_referencia_pct"]) < 1e-9)
    r = comparar_candidatos([corto, largo], AHORA)
    g = r["grupos"]["Q"]
    sin_norm = {x["expediente_id"]: x["exceso_sobre_referencia_pct"] / max(1.0, x["riesgo_pct"]) for x in g["ranking"]}
    con_norm_primero = g["ranking"][0]["expediente_id"]
    h.chk("si_la_normalizacion_decide_es_AJUSTADA", (max(sin_norm, key=sin_norm.get) != con_norm_primero) == (g["decision"] == "AJUSTADA")
          and (g["decision"] == "AJUSTADA") == g["sensible"], g)
    h.chk("y_en_este_caso_lo_es", g["decision"] == "AJUSTADA" and g["primero"] is None and set(g["aspirantes"]) == {"EXP-0001", "EXP-0002"}
          and max(sin_norm, key=sin_norm.get) == "EXP-0002", g)
    mismo = con_horizonte(cand(1), 90), con_horizonte(cand(2, esperado=(5.0, 0.5, -5.0)), 90)
    r = comparar_candidatos(list(mismo), AHORA)
    h.chk("mismo_horizonte_decision_clara", r["grupos"]["Q"]["decision"] == "CLARA" and r["grupos"]["Q"]["primero"] == "EXP-0001", r["grupos"]["Q"])

    # ---------------------------------------------------------------- (4) confianza verificada
    alta, _ = uno(cand(1, conf=0.8))
    c = cand(1, conf=0.8)
    c["sobre"]["payload"]["capa3"]["doble_analisis"] = {"realizado": True, "discrepa": True}
    d, _ = uno(c)
    tope_v = FACTOR_SIN_DOBLE * TOPE_CLASE["Q"]
    h.chk("discrepa_topa_la_confianza", d["ajustes"] == ["CONFIANZA_DISCREPA"] and abs(d["confianza_verificada"] - tope_v) < 1e-12
          and abs(d["puntuacion"] - alta["puntuacion"] * tope_v / 0.8) < 1e-9 and d["confianza"] == 0.8, d)
    c = cand(1, conf=0.8)
    c["sobre"]["payload"]["capa3"]["doble_analisis"] = {"realizado": False, "discrepa": False}
    d2, _ = uno(c)
    h.chk("sin_doble_analisis_tambien_se_topa", d2["ajustes"] == ["CONFIANZA_SIN_DOBLE"] and d2["confianza_verificada"] == d["confianza_verificada"], d2)
    c = cand(1)   # 0,6 = 0,75 × 0,8: ya está en el tope verificado, no cambia aunque discrepe (no se castiga dos veces)
    c["sobre"]["payload"]["capa3"]["doble_analisis"] = {"realizado": True, "discrepa": True}
    h.chk("discrepa_no_castiga_dos_veces", uno(c)[0]["confianza_verificada"] == 0.6 and uno(c)[0]["ajustes"] == [])
    c = cand(1)
    c["sobre"]["payload"]["capa3"]["doble_analisis"] = {"realizado": True, "discrepa": False}
    h.chk("sin_discrepancia_no_cambia", uno(c)[0]["confianza_verificada"] == 0.6)

    # ---------------------------------------------------------------- dominancia y parámetros
    a = con_horizonte(cand(1), 90)
    b = con_horizonte(cand(2, esperado=(10.0, 0.5, -5.0)), 90)
    b["sobre"]["payload"]["capa2"]["distribucion"]["p05"] = -7.0   # mismo exceso, más riesgo verificado
    r = comparar_candidatos([a, b], AHORA)
    rk = {x["expediente_id"]: x for x in r["grupos"]["Q"]["ranking"]}
    h.chk("domina_con_el_riesgo_verificado", rk["EXP-0002"]["dominado_por"] == ["EXP-0001"], rk["EXP-0002"]["dominado_por"])
    h.chk("parametros_versionados", VERSION_PARAMETROS == "PAR-0.3.0")

    # ---------------------------------------------------------------- regresiones de la revisión independiente de T-17
    con, _ = uno(con_stop(cand(1, esperado=(3.0, 0.5, -2.0)), 1.12, 1.05))
    sin, _ = uno(sin_stop(cand(1, esperado=(3.0, 0.5, -2.0))))
    h.chk("r01_sin_stop_un_largo_cuenta_con_perderlo_todo", sin["riesgo_pct"] == RIESGO_SIN_STOP_LARGO and "RIESGO_SIN_STOP" in sin["ajustes"]
          and sin["puntuacion"] < con["puntuacion"], (sin, con))
    d, r = uno(sin_stop(cand(1, direccion="CORTO")))
    h.chk("r01_sin_stop_un_corto_no_se_ordena", d is None and r["excluidos"] == [{"expediente_id": "EXP-0001", "motivo": "SIN_STOP"}], r)
    d, _ = uno(con_stop(cand(1, direccion="NEUTRAL", esperado=(10.0, 0.5, -4.0)), 1.12, 1.30))
    h.chk("r02_neutral_cuenta_el_stop", "RIESGO_STOP" in d["ajustes"] and abs(d["riesgo_pct"] - (0.18 / 1.12 * 100 + 0.04)) < 1e-9, d)
    c = cand(1)
    c["sobre"]["payload"]["capa2"]["distribucion"]["p05"] = -8.0
    for k in ("entrada", "salida"):
        c["sobre"]["payload"]["costes"][k] = {"valor": None, "unidad": "pb", "estado": "NO_ESTIMABLE"}
    d, _ = uno(c)
    h.chk("r03_el_p05_paga_el_coste", abs(d["riesgo_pct"] - 8.02) < 1e-12, d)
    largo, rl = uno(con_horizonte(cand(1), 3650, (2.0, 0.0, -1.7)))
    corto, rc = uno(con_horizonte(cand(2), 1, (0.5, 0.0, -0.36)))
    h.chk("r04_el_minimo_para_no_abstenerse_es_anual", largo is None and rl["excluidos"][0]["motivo"] == "NO_SUPERA_REFERENCIA"
          and corto is not None and rc["decision_global"] == "INVERTIR", (rl, rc))
    e1 = con_horizonte(sin_stop(cand(1, esperado=(1.0, 0.3, 0.3))), 1)
    e2 = con_horizonte(sin_stop(cand(2, esperado=(1.0, 0.3, 0.3))), 365)
    for e in (e1, e2):
        e["sobre"]["payload"]["capa2"]["distribucion"]["p05"] = 0.2
        e["sobre"]["payload"]["entrada_salida"]["stop"] = {"valor": 1.12 * 0.9999, "unidad": "USD", "estado": "SUPUESTO"}   # riesgo casi nulo
        e["sobre"]["payload"]["entrada_salida"]["entrada"]["limite"]["valor"] = 1.12
    r = comparar_candidatos([e1, e2], AHORA)
    rk = {x["expediente_id"]: x for x in r["grupos"]["Q"]["ranking"]}
    h.chk("r05_el_suelo_de_riesgo_va_antes_de_anualizar", abs(rk["EXP-0001"]["puntuacion"] / rk["EXP-0002"]["puntuacion"] - 365 ** 0.5) < 1e-6, rk)

    def par(n_corto, n_largo):
        c = con_horizonte(cand(n_corto, esperado=(3.0, 0.5, -2.0)), 30)
        l_ = con_horizonte(cand(n_largo, esperado=(3.0, 0.5, -2.0)), 90)
        g = comparar_candidatos([c, l_], AHORA)["grupos"]["Q"]
        return g["decision"], g["sensible"], sorted(g["aspirantes"])
    h.chk("r06_la_decision_no_depende_del_id", par(1, 2) == par(2, 1) and par(1, 2)[0] == "AJUSTADA", (par(1, 2), par(2, 1)))
    a = con_horizonte(cand(1, esperado=(3.6, -1.5, -1.5)), 30)
    b = con_horizonte(cand(2, esperado=(26.0, -6.0, -6.0)), 365)
    for x, pr in ((a, (0.5, 0.25, 0.25)), (b, (0.5, 0.25, 0.25))):
        for e, q in zip(x["sobre"]["payload"]["capa2"]["escenarios"], pr):
            e["probabilidad"] = q
    g = comparar_candidatos([a, b], AHORA)["grupos"]["Q"]
    h.chk("r07_un_dominado_nunca_es_aspirante", not any(x["dominado_por"] and x["expediente_id"] in g["aspirantes"] for x in g["ranking"])
          and g["ranking"][0]["dominado_por"] == [], g)
    c = cand(1)
    c["sobre"]["payload"]["costes"]["entrada"]["valor"] = 4
    c["sobre"]["payload"]["costes"]["salida"] = {"valor": None, "unidad": "pb", "estado": "NO_ESTIMABLE"}
    d, _ = uno(c)
    h.chk("r09_una_entrada_cara_no_tapa_la_salida", "COSTE_SUELO" in d["ajustes"] and abs(d["coste_descontado_pct"] - COSTE_SUELO_IV["Q"] / 200) < 1e-12, d)
    from pruebas_sobre_t27 import comparada_con
    det = comparada_con().expedientes["EXP-0001"]["comparacion"]["detalle_d"]
    h.chk("r10_el_expediente_guarda_lo_verificado_por_D", all(k in det for k in ("ajustes", "riesgo_pct", "exceso_anual_pct", "riesgo_anual_pct",
                                                                                "coste_descontado_pct", "confianza_verificada")), det)
    h.chk("no_muta_la_entrada", (lambda x: (comparar_candidatos([x], AHORA), x)[1] == cand(1))(cand(1)))

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO D T-17:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
