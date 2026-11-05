"""Pruebas de T-27: el sobre CT-G-02 0.2.0 en el Orquestador y en D (entrada numérica, candidato bloqueado, capa 2 SUPUESTO,
versión retirada). Las reglas del validador (V-13, V-16, V-21 a V-25) las cubren los casos de pruebas/validos e invalidos."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

import contratos as ct  # noqa: E402
from comparador import comparar_candidatos  # noqa: E402
from validar_sobre import bloqueos, validar  # noqa: E402
from pruebas_orquestador import (AHORA, COND_OBS, ENTRADA, INV, OBJ, SALIDA, STOP, Arnes, dim, elegir_si_hace_falta, encargo,  # noqa: E402
                                 nuevo, sobre, sobre_para)
from validar_sobre import _dt, proporcion_real  # noqa: E402
import json  # noqa: E402

CTX = json.loads((AQUI / "contexto.json").read_text(encoding="utf-8"))


def estado(o):
    return copy.deepcopy((o.expedientes, o.encargos, o.eventos, o.avisos, o.ultimo_ahora))


def en_analisis(o, n):
    eid = f"EXP-{n:04d}"
    assert o.detectar(eid, f"COR-{n:04d}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.emitir_encargo(eid, encargo(n), "GESTOR_TACTICA", AHORA)["ok"]
    return eid


def comparada_con(mod=None, salida=None):
    """EXP-0001 (con su sobre retocado por `mod`) y EXP-0002 comparados; EXP-0001 elegido si hace falta."""
    o = nuevo()
    s1 = sobre_para(1, salida)
    if mod:
        mod(s1["payload"])
    en_analisis(o, 1)
    r = o.entregar_sobre("EXP-0001", s1, AHORA)
    assert r["ok"], r
    en_analisis(o, 2)
    assert o.entregar_sobre("EXP-0002", sobre(2), AHORA)["ok"]
    assert o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)["ok"]
    elegir_si_hace_falta(o, "EXP-0001", AHORA)
    return o


def proponer(o, entrada=None, salida=None):
    entrada, salida = entrada or ENTRADA, salida or SALIDA
    return o.proponer("EXP-0001", entrada, salida, "GESTOR_TACTICA", AHORA, dim(o, "EXP-0001", entrada, salida))


def main():
    h = Arnes()

    # ---------------------------------------------------------------- candidato bloqueado (O-32)
    o = nuevo()
    eid = en_analisis(o, 1)
    s = sobre(1)
    s["payload"]["exclusiones_duras"]["sanciones"] = "BLOQUEADO"
    h.chk("bloqueado_es_sobre_valido", validar(s, CTX) == [] and bloqueos(s) == ["sanciones"], validar(s, CTX))
    r = o.entregar_sobre(eid, s, AHORA)
    e = o.expedientes[eid]
    h.chk("bloqueado_se_recibe_y_descarta_O32", r["ok"] and r["codigo"] == "O-32" and e["estado"] == "DESCARTADA"
          and e["sobre"] is None and e["exclusion"]["bloqueos"] == ["sanciones"], r)
    h.chk("bloqueado_no_pasa_por_validada", not any(x["hasta"] == "VALIDADA" for x in e["historial"])
          and e["historial"][-1]["actor"] == "ORQUESTADOR")
    av = [x for x in o.avisos if x["codigo"] == "O-32"]
    h.chk("bloqueado_avisa_al_operador_con_su_cartera", len(av) == 1 and av[0]["ref"] == eid and av[0]["carteras"] == ["TACTICA"]
          and "sanciones" in av[0]["motivo"], av)
    h.chk("bloqueado_encargo_entregado", o.encargos[e["encargo_actual"]]["estado"] == "ENTREGADO")
    h.chk("bloqueado_integridad", o.integridad() == [], o.integridad())
    h.chk("bloqueado_reenvio_duplicado", o.entregar_sobre(eid, s, AHORA)["codigo"] in ("O-02", "O-14"))
    otro = encargo(1); otro["event_id"] = "EV-ENC-OTRO"
    r = o.emitir_encargo(eid, otro, "GESTOR_TACTICA", AHORA)
    h.chk("bloqueado_no_se_reabre_O14", r["codigo"] == "O-14", r)
    # no compite ni queda de testigo: dos candidatos más se comparan sin él
    en_analisis(o, 2); assert o.entregar_sobre("EXP-0002", sobre(2), AHORA)["ok"]
    en_analisis(o, 3); assert o.entregar_sobre("EXP-0003", sobre(3), AHORA)["ok"]
    r = o.comparar(["EXP-0002", "EXP-0003"], "D", AHORA)
    h.chk("bloqueado_no_es_testigo", r["ok"] and not o._testigos("TACTICA", __import__("validar_sobre")._dt(AHORA), {"EXP-0002", "EXP-0003"}), r)
    h.chk("bloqueado_no_entra_en_comparar", o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)["ok"] is False)
    # otras exclusiones y varias a la vez
    for campo in ("invertibilidad", "acceso"):
        o2 = nuevo(); en_analisis(o2, 1); s2 = sobre(1); s2["payload"]["exclusiones_duras"][campo] = "BLOQUEADO"
        h.chk(f"bloqueado_por_{campo}_O32", o2.entregar_sobre("EXP-0001", s2, AHORA)["codigo"] == "O-32")
    o2 = nuevo(); en_analisis(o2, 1); s2 = sobre(1); s2["payload"]["exclusiones_duras"].update(sanciones="BLOQUEADO", acceso="BLOQUEADO")
    r = o2.entregar_sobre("EXP-0001", s2, AHORA)
    h.chk("bloqueado_por_dos_motivos", r["codigo"] == "O-32" and o2.expedientes["EXP-0001"]["exclusion"]["bloqueos"] == ["acceso", "sanciones"])
    # un bloqueo con otra cosa mal sigue siendo un sobre inválido (no se cuela como informe)
    o2 = nuevo(); en_analisis(o2, 1); s2 = sobre(1); s2["payload"]["exclusiones_duras"]["sanciones"] = "BLOQUEADO"
    s2["payload"]["capa3"]["confianza"] = 0.99
    antes = estado(o2)
    r = o2.entregar_sobre("EXP-0001", s2, AHORA)
    h.chk("bloqueado_e_invalido_O01_sin_cambios", r["codigo"] == "O-01" and estado(o2)[:4] == antes[:4], r)
    o2 = nuevo(); en_analisis(o2, 1); s2 = sobre(1); s2["payload"]["exclusiones_duras"].update(sanciones="BLOQUEADO", acceso="DESCONOCIDO")
    r = o2.entregar_sobre("EXP-0001", s2, AHORA)
    h.chk("bloqueado_y_desconocido_V16", r["codigo"] == "O-01" and "V-16" in r["motivo"], r)
    # D lo excluye aunque se lo pasen directamente
    d1, d2 = sobre(1), sobre(2)
    d2["payload"]["identificacion"]["instrumento"] = "GBP/USD"
    d1["payload"]["exclusiones_duras"]["sanciones"] = "BLOQUEADO"
    rd = comparar_candidatos([{"expediente_id": "EXP-0001", "sobre": d1}, {"expediente_id": "EXP-0002", "sobre": d2}], AHORA)
    h.chk("D_excluye_bloqueado", {"expediente_id": "EXP-0001", "motivo": "EXCLUSION_DURA"} in rd["excluidos"], rd.get("excluidos"))
    h.chk("bloqueos_nunca_lanza", bloqueos(None) == [] and bloqueos({}) == [] and bloqueos({"payload": {"exclusiones_duras": []}}) == [])

    # ---------------------------------------------------------------- entrada numérica en la propuesta (O-21)
    o = comparada_con()
    h.chk("propuesta_con_limite_igual_al_del_sobre_OK", proponer(comparada_con(), {**ENTRADA, "limite": 1.12})["ok"])
    r = proponer(o, {**ENTRADA, "limite": 1.13})
    h.chk("largo_limite_mas_caro_que_el_sobre_O21", r["codigo"] == "O-21" and "peor que el analizado" in r["motivo"], r)
    h.chk("largo_limite_mas_barato_OK", proponer(comparada_con(), {**ENTRADA, "limite": 1.09})["ok"])
    o = comparada_con(mod=lambda p: p["entrada_salida"]["entrada"].update(ventana_hasta="2026-11-07T12:00:00+00:00"))
    r = proponer(o, {**ENTRADA, "ventana_hasta": "2026-11-07T18:00:00+00:00"})
    h.chk("ventana_mas_larga_que_la_del_sobre_O21", r["codigo"] == "O-21" and "ventana de entrada pasa de la analizada" in r["motivo"], r)
    o = comparada_con(mod=lambda p: p["entrada_salida"]["entrada"].update(ventana_hasta="2026-11-07T12:00:00+00:00"))
    h.chk("ventana_dentro_de_la_del_sobre_OK", proponer(o, {**ENTRADA, "ventana_hasta": "2026-11-07T11:00:00+00:00"})["ok"])
    corto = {**SALIDA, "condiciones": [{**STOP, "operador": ">=", "umbral": 1.15}, {**OBJ, "operador": "<=", "umbral": 1.00},
                                       {**INV, "operador": ">", "umbral": 1.15}]}
    o = comparada_con(salida=corto)
    lim_sobre = o.expedientes["EXP-0001"]["sobre"]["documento"]["payload"]["entrada_salida"]["entrada"]["limite"]["valor"]
    r = proponer(o, {**ENTRADA, "limite": round(lim_sobre - 0.0005, 6)}, corto)
    h.chk("corto_limite_mas_barato_que_el_sobre_O21", r["codigo"] == "O-21" and "peor que el analizado" in r["motivo"], r)
    o = comparada_con(salida=corto)
    h.chk("corto_limite_igual_OK", proponer(o, {**ENTRADA, "limite": lim_sobre}, corto)["ok"])
    # el sobre guardado manda: si alguien lo toca, O-13 antes que nada
    o = comparada_con()
    o.expedientes["EXP-0001"]["sobre"]["documento"]["payload"]["entrada_salida"]["entrada"]["limite"]["valor"] = 9.0
    h.chk("limite_del_sobre_guardado_alterado_O13", proponer(o, {**ENTRADA, "limite": 1.13})["codigo"] == "O-13")

    # ---------------------------------------------------------------- capa 2 SUPUESTO: se acepta y D no la ordena
    o = nuevo(); en_analisis(o, 1)
    s = sobre(1); s["payload"]["capa2"]["estado"] = "SUPUESTO"
    h.chk("capa2_supuesto_con_escenarios_se_valida", o.entregar_sobre("EXP-0001", s, AHORA)["ok"] and o.expedientes["EXP-0001"]["estado"] == "VALIDADA")
    d2 = sobre(2); d2["payload"]["identificacion"]["instrumento"] = "GBP/USD"
    rd = comparar_candidatos([{"expediente_id": "EXP-0001", "sobre": s}, {"expediente_id": "EXP-0002", "sobre": d2}], AHORA)
    h.chk("D_no_ordena_capa2_supuesto", {"expediente_id": "EXP-0001", "motivo": "ESCENARIOS_SUPUESTO"} in rd["excluidos"], rd.get("excluidos"))
    # D ordena igual con horizonte común declarado: la puntuación no depende de los campos nuevos
    a, b = sobre(1), sobre(1)
    b["payload"]["capa2"]["distribucion"] = {"p05": -10.0, "p50": 0.0, "p95": 10.0}
    b["payload"]["entrada_salida"]["entrada"]["descripcion"] = "otra descripción"
    ra = comparar_candidatos([{"expediente_id": "EXP-0001", "sobre": a}], AHORA)
    rb = comparar_candidatos([{"expediente_id": "EXP-0001", "sobre": b}], AHORA)
    h.chk("D_misma_puntuacion", ra["grupos"] == rb["grupos"] and ra["decision_global"] == rb["decision_global"], (ra, rb))

    # ---------------------------------------------------------------- versión retirada
    viejo = sobre(1)
    viejo["version_esquema"] = "0.1.0"
    viejo["payload"]["entrada_salida"]["entrada"] = "Límite en 1,12 hasta el 8 de noviembre"
    for k in ("horizonte_dias", "distribucion"):
        viejo["payload"]["capa2"].pop(k)
    f = validar(viejo, CTX)
    h.chk("sobre_010_V01_retirada", [x["regla"] for x in f] == ["V-01"] and "retirada" in f[0]["mensaje"], f)
    o = nuevo(); en_analisis(o, 1); antes = estado(o)
    r = o.entregar_sobre("EXP-0001", viejo, AHORA)
    h.chk("sobre_010_O01_sin_cambios", r["codigo"] == "O-01" and estado(o)[:4] == antes[:4], r)
    h.chk("contratos_010_CT02_y_historico", ct.validar(viejo)[0]["regla"] == "CT-02" and ct.validar(viejo, historico=True) == [],
          (ct.validar(viejo), ct.validar(viejo, historico=True)))
    h.chk("contratos_020_valido", ct.validar(sobre(1)) == [], ct.validar(sobre(1)))
    reg = {c["tipo"]: c for c in ct.registro()["contratos"]}["CT-G-02"]
    h.chk("registro_02_en_020_con_010_retirada", reg["version"] == "0.2.0" and [v["estado"] for v in reg["versiones"]] == ["VIGENTE", "RETIRADA"])


    # ================================================================ regresiones de la revisión independiente
    # R1: un candidato que fue testigo y luego queda bloqueado deja de serlo (no le quita la victoria a nadie)
    o = nuevo(); en_analisis(o, 1)
    assert o.entregar_sobre("EXP-0001", sobre(1), AHORA)["ok"]
    assert o.observar("EXP-0001", COND_OBS, "esperar", "GESTOR_TACTICA", AHORA)["ok"]
    h.chk("R1_antes_del_bloqueo_es_testigo", [x["expediente_id"] for x in o._testigos("TACTICA", _dt(AHORA), set())] == ["EXP-0001"])
    assert o.reabrir("EXP-0001", "re-analizar", "OPERADOR", AHORA)["ok"]
    enc = encargo(1); enc["event_id"] = "EV-ENC-0001-B"
    assert o.emitir_encargo("EXP-0001", enc, "GESTOR_TACTICA", AHORA)["ok"]
    s = sobre(1); s["event_id"] = "EV-SOB-0001-B"; s["payload"]["exclusiones_duras"]["sanciones"] = "BLOQUEADO"
    h.chk("R1_bloqueo_tras_reabrir_O32", o.entregar_sobre("EXP-0001", s, AHORA)["codigo"] == "O-32")
    h.chk("R1_bloqueado_deja_de_ser_testigo", o._testigos("TACTICA", _dt(AHORA), set()) == [])
    en_analisis(o, 2); assert o.entregar_sobre("EXP-0002", sobre(2), AHORA)["ok"]
    en_analisis(o, 3); assert o.entregar_sobre("EXP-0003", sobre(3), AHORA)["ok"]
    r = o.comparar(["EXP-0002", "EXP-0003"], "D", AHORA)
    h.chk("R1_comparar_sin_O30_por_el_bloqueado", r["ok"] and r.get("apartado_mejor") is None and r["codigo"] != "O-30", r)
    h.chk("R1_integridad", o.integridad() == [], o.integridad())
    # R2: la ventana de entrada acota la vida del candidato
    s = sobre(1); s["payload"]["entrada_salida"]["entrada"]["ventana_hasta"] = "2026-11-06T08:00:00+00:00"
    h.chk("R2_ventana_ya_cerrada_V24", [x["regla"] for x in validar(s, CTX)] == ["V-24"], validar(s, CTX))
    o = nuevo(); en_analisis(o, 1)
    s = sobre(1); s["payload"]["entrada_salida"]["entrada"]["ventana_hasta"] = "2026-11-06T12:00:00+00:00"
    assert o.entregar_sobre("EXP-0001", s, AHORA)["ok"]
    h.chk("R2_vigencia_util_es_la_ventana", o.expedientes["EXP-0001"]["sobre"]["valid_until"] == "2026-11-06T12:00:00+00:00")
    o.barrer("2026-11-06T12:30:00+00:00")
    h.chk("R2_barrer_lo_caduca_al_cerrar_la_ventana", o.expedientes["EXP-0001"]["estado"] == "CADUCADA", o.expedientes["EXP-0001"]["estado"])
    d1, d2 = sobre(1), sobre(2)
    d1["payload"]["entrada_salida"]["entrada"]["ventana_hasta"] = "2026-11-06T08:00:00+00:00"
    d2["payload"]["identificacion"]["instrumento"] = "GBP/USD"
    rd = comparar_candidatos([{"expediente_id": "EXP-0001", "sobre": d1}, {"expediente_id": "EXP-0002", "sobre": d2}], AHORA)
    h.chk("R2_D_no_ordena_con_la_ventana_cerrada", {"expediente_id": "EXP-0001", "motivo": "CADUCADO"} in rd["excluidos"], rd.get("excluidos"))
    # R3: unidades
    s = sobre(1); s["payload"]["entrada_salida"]["objetivo"].update(valor=5.0, unidad="%")
    h.chk("R3_objetivo_en_porcentaje_V22", "V-22" in {x["regla"] for x in validar(s, CTX)})
    def en_eur(p):
        for k in ("stop", "objetivo"):
            p["entrada_salida"][k]["unidad"] = "EUR"
        p["entrada_salida"]["entrada"]["limite"]["unidad"] = "EUR"
    r = proponer(comparada_con(mod=en_eur))
    h.chk("R3_sobre_en_otra_divisa_que_la_de_cotizacion_O21", r["codigo"] == "O-21" and "divisa de cotización" in r["motivo"], r)
    r = proponer(comparada_con(), salida={**SALIDA, "condiciones": [{**STOP, "unidad": "EUR"}, OBJ, INV]})
    h.chk("R3_stop_de_la_propuesta_en_otra_divisa_O21", r["codigo"] == "O-21" and "divisa de cotización" in r["motivo"], r)
    # R4: un candidato bloqueado se informa también en N0 y N1 (antes R-13 tropezaba con la capa 2 que falta)
    for nivel in ("N0", "N1"):
        o = nuevo()
        assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
        enc = encargo(1); enc["payload"]["nivel_analisis"] = nivel; enc["payload"]["decision_informada"] = "EXPLORAR"
        assert o.emitir_encargo("EXP-0001", enc, "GESTOR_TACTICA", AHORA)["ok"]
        s = sobre(1); p = s["payload"]; p["identificacion"]["nivel_analisis"] = nivel
        for k in ("capa2", "capa3") + (("tesis", "entrada_salida", "liquidez", "costes", "capital", "estres_historico", "factores", "referencias")
                                         if nivel == "N0" else ()):
            p.pop(k)
        p["exclusiones_duras"]["sanciones"] = "BLOQUEADO"
        real = proporcion_real(p)
        p["evidencia"]["proporcion"] = {k: round(v, 4) for k, v in real.items()} if sum(real.values()) else {"VERIFICADO": 0, "ESTIMADO": 0, "SUPUESTO": 1.0}
        r = o.entregar_sobre("EXP-0001", s, AHORA)
        h.chk(f"R4_bloqueado_en_{nivel}_O32", r["codigo"] == "O-32" and o.integridad() == [], r)
    # R5: horizonte no entero
    s = sobre(1); s["payload"]["capa2"]["horizonte_dias"] = 90.0
    for x in s["payload"]["capa2"]["escenarios"]:
        x["horizonte_dias"] = 90.0
    h.chk("R5_horizonte_90_0_V25", [x["regla"] for x in validar(s, CTX)] == ["V-25"], validar(s, CTX))
    # R6: D no interpreta una versión retirada aunque se la pasen directamente
    rd = comparar_candidatos([{"expediente_id": "EXP-0001", "sobre": {**sobre(1), "version_esquema": "0.1.0"}}], AHORA)
    h.chk("R6_D_excluye_version_retirada", {"expediente_id": "EXP-0001", "motivo": "FORMA"} in rd["excluidos"], rd.get("excluidos"))
    # R7: la exclusión guardada está en la cadena
    o = nuevo(); en_analisis(o, 1)
    s = sobre(1); s["payload"]["exclusiones_duras"]["sanciones"] = "BLOQUEADO"
    assert o.entregar_sobre("EXP-0001", s, AHORA)["codigo"] == "O-32"
    for nombre, cambio in (("otra", {"event_id": "OTRO", "hash": "0" * 64, "bloqueos": []}), ("sin_bloqueos", None)):
        o2 = copy.deepcopy(o)
        if cambio is None:
            o2.expedientes["EXP-0001"].pop("exclusion")
        else:
            o2.expedientes["EXP-0001"]["exclusion"] = cambio
        h.chk(f"R7_exclusion_alterada_{nombre}_se_detecta", o2.integridad() != [], o2.integridad())
    o2 = nuevo(); en_analisis(o2, 1); assert o2.entregar_sobre("EXP-0001", sobre(1), AHORA)["ok"]
    o2.expedientes["EXP-0001"]["exclusion"] = {"event_id": "X", "hash": "0" * 64, "bloqueos": ["sanciones"]}
    h.chk("R7_exclusion_inventada_se_detecta", o2.integridad() != [])

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO SOBRE T-27:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
