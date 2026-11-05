"""Genera, guarda y ejecuta los casos de prueba de CT-G-01 (encargo) y de la comprobación
sobre -> encargo. Datos SIMULADOS. Cada inválido rompe exactamente una regla.

Uso: python3 pruebas/pruebas_encargo.py     (escribe en pruebas/encargos/ y ejecuta)
"""
import copy
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from validar_encargo import validar_encargo, sobre_responde_a_encargo  # noqa: E402
from generar_casos import validos as sobres_validos  # noqa: E402
from validar_sobre import validar, cargar_json  # noqa: E402
from pruebas_k import construir as construir_sello_k, CAL  # noqa: E402
from k_calidad import hash_del_sello  # noqa: E402
from datetime import date  # noqa: E402

_s1 = construir_sello_k()[1]["sello"]                                              # corte 2026-11-05
_s2 = construir_sello_k(hasta=date(2026, 11, 6), solicitada="2026-11-06")[1]["sello"]   # corte 2026-11-06
assert _s1["sello_id"] == "K-20261105-001" and _s2["sello_id"] == "K-20261106-001"
_s0 = construir_sello_k(hasta=date(2026, 11, 4), solicitada="2026-11-04")[1]["sello"]   # corte 2026-11-04
_s3 = construir_sello_k(hasta=date(2026, 11, 3), solicitada="2026-11-03")[1]["sello"]   # corte 2026-11-03
_sf = construir_sello_k(hasta=date(2026, 12, 24), solicitada="2026-12-24",
                        ctx={"ahora": "2026-12-28T09:00:00+00:00", "secuencia": 1})[1]["sello"]   # víspera de festivo
_slp = construir_sello_k(cartera="LARGO_PLAZO")[1]["sello"]
SELLOS = {x["sello_id"]: x for x in (_s0, _s1, _s2, _s3, _sf)}
ESPERADAS_EXTRA = {"inv_E04_corte_no_vigente": {"E-04", "E-16"}, "inv_E04_corte_antiguo": {"E-04", "E-16"}}

CTX = {
    "ahora": "2026-11-06T09:00:00+00:00",
    "fecha_corte_vigente": "2026-11-05",
    "perfiles_activos": ["C-DIV", "C-RV", "C-CRI"],
    "apalancamiento_permitido": False,
    "sellos": SELLOS,
    "calendario": CAL,
}


def encargo_div():
    return {
        "event_id": "EV-ENC-0001", "correlation_id": "COR-0001", "expediente_id": "EXP-0001",
        "producer": "GESTOR_TACTICA", "consumer": "C-DIV", "tipo_mensaje": "CT-G-01",
        "version_esquema": "0.1.0",
        "emitido_en": "2026-11-05T12:00:00+00:00", "valid_until": "2026-11-08T12:00:00+00:00",
        "data_refs": ["PAQ-B-0001", "K-20261105-001"],
        "payload": {
            "pregunta": "¿Conviene una posición larga en EUR/USD a 3 meses?",
            "decision_informada": "ABRIR_POSICION", "cartera_destino": "TACTICA",
            "candidato": {"perfil": "C-DIV", "instrumento": "EUR/USD",
                          "via_acceso": "Futuro de divisas, vencimiento trimestral",
                          "paquete_b_ref": "PAQ-B-0001"},
            "nivel_analisis": "N3", "fecha_corte": "2026-11-05", "sello_corte_ref": "K-20261105-001",
            "mandato": {"benchmark_ref": "BENCH-EFECTIVO", "horizonte_dias": {"min": 14, "max": 90},
                        "apalancamiento_max": 0, "tamano_max_pct_cartera": 5,
                        "instrumentos_permitidos": ["EUR/USD", "GBP/USD"], "exclusiones": []},
            "presupuesto": {"coste_max_eur": 5.0, "tiempo_max_min": 30,
                            "entrega_antes_de": "2026-11-05T20:00:00+00:00"},
            "prioridad": "NORMAL"},
        "resultado_politica": {"controles": ["SC-6"], "resultado": "APROBADO", "version_politica": "POL-0.1"},
    }


def encargo_rv():
    e = encargo_div()
    e["event_id"] = "EV-ENC-0002"; e["correlation_id"] = "COR-0002"; e["expediente_id"] = "EXP-0002"
    e["producer"] = "BROKER"; e["consumer"] = "C-RV"
    p = e["payload"]
    p["pregunta"] = "¿Encaja un ETF de acciones europeas en la cartera de largo plazo?"
    p["decision_informada"] = "ABRIR_POSICION"; p["cartera_destino"] = "LARGO_PLAZO"
    p["candidato"].update(perfil="C-RV", instrumento="ETF acciones Europa",
                          via_acceso="ETF cotizado en bolsa europea", paquete_b_ref="PAQ-B-0002")
    p["nivel_analisis"] = "N2"
    p["mandato"].update(horizonte_dias={"min": 1095, "max": 3650},
                        instrumentos_permitidos=["ETF acciones Europa"], tamano_max_pct_cartera=8)
    e["data_refs"] = ["PAQ-B-0002", "K-20261105-001"]
    return e


def invalidos():
    out = {}
    d = encargo_div

    def caso(nombre, fn, ctx=None, base=d):
        e = base(); fn(e); out[nombre] = (e, ctx or {})

    P = lambda e: e["payload"]
    caso("inv_E01_version_desconocida", lambda e: e.update(version_esquema="9.9.9"))
    caso("inv_E01_sin_zona", lambda e: e.update(emitido_en="2026-11-05T12:00:00"))
    caso("inv_E01_falta_campo", lambda e: P(e).pop("pregunta"))
    caso("inv_E01_producer_desconocido", lambda e: e.update(producer="CUALQUIERA"))
    caso("inv_E01_tamano_cero", lambda e: P(e)["mandato"].update(tamano_max_pct_cartera=0))
    caso("inv_E02_destinatario_distinto", lambda e: e.update(consumer="C-RV"))
    caso("inv_E02_perfil_no_construido", lambda e: (e.update(consumer="C-MP"), P(e)["candidato"].update(perfil="C-MP")))
    caso("inv_E03_caducado", lambda e: (e.update(valid_until="2026-11-05T13:00:00+00:00"),
         P(e)["presupuesto"].update(entrega_antes_de="2026-11-05T12:30:00+00:00")))
    caso("inv_E03_vigencia_excesiva", lambda e: e.update(valid_until="2036-11-05T12:00:00+00:00"))
    caso("inv_E04_corte_no_vigente", lambda e: (P(e).update(fecha_corte="2026-11-04", sello_corte_ref="K-20261104-001"),
                                       e.update(data_refs=["PAQ-B-0001", "K-20261104-001"])),
         ctx={})
    caso("inv_E04_corte_antiguo", lambda e: (P(e).update(fecha_corte="2026-11-03", sello_corte_ref="K-20261103-001"),
                                       e.update(data_refs=["PAQ-B-0001", "K-20261103-001"])),
         ctx={"fecha_corte_vigente": "2026-11-03"})
    caso("inv_E05_horizonte_invertido", lambda e: P(e)["mandato"].update(horizonte_dias={"min": 90, "max": 20}))
    caso("inv_E05_fuera_de_rango_cartera", lambda e: P(e)["mandato"].update(horizonte_dias={"min": 2, "max": 90}))
    caso("inv_E06_apalancamiento", lambda e: P(e)["mandato"].update(apalancamiento_max=5))
    caso("inv_E07_tamano_excesivo", lambda e: P(e)["mandato"].update(tamano_max_pct_cartera=50))
    caso("inv_E08_entrega_antes_de_emitir", lambda e: P(e)["presupuesto"].update(entrega_antes_de="2026-11-05T11:00:00+00:00"))
    caso("inv_E08_entrega_tras_vigencia", lambda e: P(e)["presupuesto"].update(entrega_antes_de="2026-11-20T12:00:00+00:00"))
    caso("inv_E08_presupuesto_insuficiente", lambda e: None,
         ctx={"presupuesto_minimo": {"N3": {"coste_eur": 50.0, "tiempo_min": 30}}})
    caso("inv_E08_supera_tope_encargo", lambda e: None, ctx={"coste_max_eur": 1.0})
    caso("inv_E09_abrir_con_n1", lambda e: P(e).update(nivel_analisis="N1"))
    caso("inv_E09_descartar_con_n3", lambda e: P(e).update(decision_informada="DESCARTAR"))
    caso("inv_E10_instrumento_no_permitido", lambda e: P(e)["mandato"].update(instrumentos_permitidos=["GBP/USD"]))
    caso("inv_E10_instrumento_excluido", lambda e: P(e)["mandato"].update(exclusiones=["EUR/USD"]))
    caso("inv_E11_gestor_ajeno", lambda e: e.update(producer="GESTOR_TRADING"))
    caso("inv_E12_falta_paquete_b", lambda e: e.update(data_refs=["K-20261105-001"]))
    caso("inv_E12_falta_sello", lambda e: e.update(data_refs=["PAQ-B-0001"]))
    caso("inv_E10_exclusion_en_minusculas", lambda e: P(e)["mandato"].update(exclusiones=["eur/usd"]))
    caso("inv_E12_misma_referencia", lambda e: (P(e)["candidato"].update(paquete_b_ref="K-20261105-001"),
         e.update(data_refs=["K-20261105-001"])))
    caso("inv_E16_sello_inexistente", lambda e: None, ctx={"sellos": {}})
    caso("inv_E16_sello_anulado", lambda e: None, ctx={"sellos": {"K-20261105-001": {**_s1, "estado": "ANULADO"}}})
    caso("inv_E16_sello_de_otro_corte", lambda e: None, ctx={"sellos": {"K-20261105-001": {**_s1, "fecha_corte": "2026-11-04"}}})
    caso("inv_E16_sello_con_hash_alterado", lambda e: None, ctx={"sellos": {"K-20261105-001": {**_s1, "version_ajustes": "AJ-9"}}})
    caso("inv_E16_id_del_sello_distinto_de_su_clave", lambda e: None, ctx={"sellos": {"K-20261105-001": _s2}})
    caso("inv_E16_sello_emitido_para_largo_plazo", lambda e: None, ctx={"sellos": {"K-20261105-001": {**_slp, "sello_id": "K-20261105-001"}}})
    caso("inv_E16_sello_no_es_objeto", lambda e: None, ctx={"sellos": {"K-20261105-001": "x"}})
    caso("inv_E16_sello_no_verificable_con_calendario", lambda e: None,
         ctx={"sellos": {"K-20261105-001": {**_s1, "mercados": [{"mercado": "OTRO", "version_calendario": "C"}]}}})
    caso("inv_E01_contexto_sin_calendario", lambda e: None, ctx={"calendario": None})
    caso("inv_E01_contexto_sin_sellos", lambda e: None, ctx={"sellos": None})
    caso("inv_E13_cerrar_sin_posicion", lambda e: P(e).update(decision_informada="CERRAR"))
    caso("inv_E13_abrir_con_posicion", lambda e: P(e).update(posicion_id="POS-0001"))
    caso("inv_E14_politica_rechazada", lambda e: e["resultado_politica"].update(resultado="RECHAZADO"))
    caso("inv_E15_tiempo_no_cabe", lambda e: P(e)["presupuesto"].update(tiempo_max_min=600))
    caso("inv_E06_permiso_como_texto", lambda e: P(e)["mandato"].update(apalancamiento_max=5),
         ctx={"apalancamiento_permitido": "false"})
    caso("inv_E01_contexto_ahora_numerico", lambda e: None, ctx={"ahora": 123})
    caso("inv_E01_contexto_horizonte_parcial", lambda e: None, ctx={"horizonte_dias": {"TACTICA": 5}})
    caso("inv_E01_coste_demasiado_grande", lambda e: P(e)["presupuesto"].update(coste_max_eur=1e300))
    return out


def respuestas():
    """(nombre, mutación del sobre, ctx extra del sobre, esperadas). Los sobres mutados siguen siendo
    válidos para su propio validador; así se comprueba el cruce y no el validador del sobre."""
    I = lambda s: s["payload"]["identificacion"]
    rv = None  # se rellena en main con el sobre de renta variable
    return [
        ("res_R01_otra_peticion", lambda s: s.update(correlation_id="COR-9999"), {}, {"R-01"}),
        ("res_R02_otro_candidato", lambda s: s.update(expediente_id="EXP-9999"), {}, {"R-02"}),
        ("res_R04_otro_corte", lambda s: I(s).update(fecha_corte="2026-11-04"), {"fecha_corte_encargo": "2026-11-04"}, {"R-04"}),
        ("res_R05_otro_nivel", lambda s: I(s).update(nivel_analisis="N2"), {}, {"R-05"}),
        ("res_R06_cartera_incompatible", lambda s: I(s).update(cartera_compatible=["LARGO_PLAZO"]), {}, {"R-06"}),
        ("res_R07_fuera_de_plazo", lambda s: s.update(emitido_en="2026-11-05T21:00:00+00:00"), {}, {"R-07"}),
        ("res_R08_mas_apalancamiento", lambda s: s["payload"]["capital"]["apalancamiento"].update(valor=3),
         {"apalancamiento_permitido": True}, {"R-08"}),
        ("res_R09_otro_instrumento", lambda s: I(s).update(instrumento="GBP/USD"), {}, {"R-09"}),
        ("res_R11_sobre_sin_sello", lambda s: s.update(data_refs=["SRC-EURUSD", "EVID-0001"]), {}, {"R-11"}),
        ("res_R12_fuente_ajena_al_sello", lambda s: s.update(data_refs=["K-20261105-001", "SRC-OTRA", "EVID-0001"]), {}, {"R-12"}),
        ("res_R11_otro_sello_ademas", lambda s: s.update(data_refs=["K-20261105-001", "K-20261104-001", "SRC-EURUSD"]), {}, {"R-11"}),
        ("res_R12_prefijo_en_minusculas", lambda s: s.update(data_refs=["K-20261105-001", "src-noexiste"]), {}, {"R-12"}),
        ("res_R12_prefijo_con_espacio", lambda s: s.update(data_refs=["K-20261105-001", " SRC-FANTASMA"]), {}, {"R-12"}),
        ("res_R12_tipo_desconocido", lambda s: s.update(data_refs=["K-20261105-001", "SRC-EURUSD", "EXT-NOEXISTE"]), {}, {"R-12"}),
        ("res_R12_ninguna_fuente", lambda s: s.update(data_refs=["K-20261105-001", "EVID-0001"]), {}, {"R-12"}),
        ("res_R10_sobre_anterior_al_encargo", lambda s: s.update(emitido_en="2026-11-05T11:00:00+00:00"), {}, {"R-10"}),
    ]


def main():
    (AQUI / "encargos" / "validos").mkdir(parents=True, exist_ok=True)
    (AQUI / "encargos" / "invalidos").mkdir(parents=True, exist_ok=True)
    for viejo in list((AQUI / "encargos" / "validos").glob("*.json")) + list((AQUI / "encargos" / "invalidos").glob("*.json")):
        viejo.unlink()
    ok = True
    validos = {"valido_div_tactica_n3.json": encargo_div(), "valido_rv_largo_plazo_n2.json": encargo_rv()}
    for n, e in validos.items():
        (AQUI / "encargos" / "validos" / n).write_text(json.dumps(e, ensure_ascii=False, indent=2), encoding="utf-8")
        fallos = validar_encargo(e, CTX)
        print(("OK   " if not fallos else "FALLA"), n, "" if not fallos else fallos)
        ok &= not fallos
    for n, (e, extra) in invalidos().items():
        (AQUI / "encargos" / "invalidos" / f"{n}.json").write_text(
            json.dumps({"ctx_extra": extra, "mensaje": e}, ensure_ascii=False, indent=2), encoding="utf-8")
        esperada = re.search(r"inv_(E\d+)", n).group(1).replace("E", "E-")
        reglas = {x["regla"] for x in validar_encargo(e, {**CTX, **extra})}
        bien = reglas == ESPERADAS_EXTRA.get(n, {esperada})
        print(("OK   " if bien else "FALLA"), n, f"esperada={esperada} obtenida={sorted(reglas)}")
        ok &= bien
    # sobre -> encargo: el sobre válido de C-DIV responde al encargo válido de C-DIV
    sobre = cargar_json((AQUI / "validos" / "valido_div_n3.json").read_text(encoding="utf-8"))
    sctx = cargar_json((AQUI / "contexto.json").read_text(encoding="utf-8"))
    assert not validar(sobre, sctx), "el sobre base debe ser válido"
    r = sobre_responde_a_encargo(encargo_div(), sobre, CTX, sctx)
    print(("OK   " if not r else "FALLA"), "respuesta_valida_div", "" if not r else r)
    ok &= not r
    for n, mut, extra, esperadas in respuestas():
        s2 = copy.deepcopy(sobre); mut(s2)
        obt = {x["regla"] for x in sobre_responde_a_encargo(encargo_div(), s2, CTX, {**sctx, **extra})}
        bien = obt == esperadas
        print(("OK   " if bien else "FALLA"), n, f"esperadas={sorted(esperadas)} obtenidas={sorted(obt)}")
        ok &= bien
    # perfil distinto: el sobre de renta variable no responde al encargo de divisas
    rv = sobres_validos()["valido_rv_n3_discrepa.json"]
    obt = {x["regla"] for x in sobre_responde_a_encargo(encargo_div(), rv, CTX, sctx)}
    esperadas = {"R-03", "R-09"}
    print(("OK   " if obt == esperadas else "FALLA"), "res_R03_otro_perfil", f"esperadas={sorted(esperadas)} obtenidas={sorted(obt)}")
    ok &= obt == esperadas
    # R-12: una fuente que K marcó NO_DISPONIBLE no puede citarse
    caida = {**_s1, "fuentes": [dict(x, estado="NO_DISPONIBLE") if x["fuente_id"] == "SRC-EURUSD" else x for x in _s1["fuentes"]]}
    for x in caida["fuentes"]:
        if x["estado"] == "NO_DISPONIBLE":
            for k in ("version_conjunto", "ultima_observacion", "antiguedad_dias_habiles", "hash"):
                x.pop(k, None)
    caida["hash_sello"] = hash_del_sello(caida)
    obt = {x["regla"] for x in sobre_responde_a_encargo(encargo_div(), sobre, {**CTX, "sellos": {**SELLOS, "K-20261105-001": caida}}, sctx)}
    print(("OK   " if obt == {"R-12"} else "FALLA"), "res_R12_fuente_no_disponible", f"obtenidas={sorted(obt)}")
    ok &= obt == {"R-12"}
    # R-00: entradas defectuosas no lanzan excepciones
    for nombre, enc, sob in (("res_R00_encargo_invalido", {"x": 1}, sobre), ("res_R00_sobre_nulo", encargo_div(), None),
                              ("res_R00_ambos_listas", [], [])):
        obt = {x["regla"] for x in sobre_responde_a_encargo(enc, sob, CTX, sctx)}
        print(("OK   " if obt == {"R-00"} else "FALLA"), nombre, f"obtenidas={sorted(obt)}")
        ok &= obt == {"R-00"}
    # válido en fin de semana: corte del viernes, encargo del viernes, hoy lunes
    e = encargo_div()
    e["emitido_en"] = "2026-11-06T12:00:00+00:00"; e["valid_until"] = "2026-11-10T12:00:00+00:00"
    e["payload"]["fecha_corte"] = "2026-11-06"; e["payload"]["presupuesto"]["entrega_antes_de"] = "2026-11-06T20:00:00+00:00"
    e["payload"]["sello_corte_ref"] = "K-20261106-001"; e["data_refs"] = ["PAQ-B-0001", "K-20261106-001"]
    fallos = validar_encargo(e, {**CTX, "ahora": "2026-11-09T09:00:00+00:00", "fecha_corte_vigente": "2026-11-06"})
    print(("OK   " if not fallos else "FALLA"), "valido_corte_viernes_ejecutado_lunes", "" if not fallos else fallos)
    ok &= not fallos
    # víspera de festivo: corte jueves 24-dic, hoy lunes 28 (el 25 es festivo): 1 día hábil, no 2
    e = encargo_div()
    e["emitido_en"] = "2026-12-28T08:30:00+00:00"; e["valid_until"] = "2026-12-31T12:00:00+00:00"
    e["payload"]["fecha_corte"] = "2026-12-24"; e["payload"]["presupuesto"]["entrega_antes_de"] = "2026-12-28T20:00:00+00:00"
    e["payload"]["sello_corte_ref"] = "K-20261224-001"; e["data_refs"] = ["PAQ-B-0001", "K-20261224-001"]
    cf = {**CTX, "ahora": "2026-12-28T09:00:00+00:00", "fecha_corte_vigente": "2026-12-24"}
    fallos = validar_encargo(e, cf)
    print(("OK   " if not fallos else "FALLA"), "valido_corte_antes_de_festivo", "" if not fallos else fallos)
    ok &= not fallos
    cf_sin = {**cf, "calendario": {**CAL, "mercados": {"FX": {"anios": [2026, 2027], "festivos": []}}}}
    fallos = {x["regla"] for x in validar_encargo(e, cf_sin)}
    print(("OK   " if fallos else "FALLA"), "control_sin_festivo_en_calendario_falla", sorted(fallos))
    ok &= bool(fallos)
    # anidamiento extremo: no debe lanzar excepciones (RecursionError) ni en el encargo ni en el sobre
    prof = []
    for _ in range(100000):
        prof = [prof]
    e = encargo_div(); e["payload"]["extra"] = prof
    try:
        r1 = validar_encargo(e, CTX)
        so = copy.deepcopy(sobre); so["payload"]["extra"] = prof
        r2 = validar(so, sctx)
        r3 = sobre_responde_a_encargo(e, so, CTX, sctx)
        bien = bool(r1) and bool(r2) and bool(r3)
    except Exception as ex:   # noqa: BLE001
        bien = False; print(type(ex).__name__)
    print(("OK   " if bien else "FALLA"), "anidamiento_extremo_no_lanza")
    ok &= bien
    print("\nRESULTADO CT-G-01:", "TODAS LAS PRUEBAS PASAN" if ok else "HAY FALLOS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
