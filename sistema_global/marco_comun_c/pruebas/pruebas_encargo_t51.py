"""Pruebas de T-51: el encargo CT-G-01 0.2.0 cita el mandato de SC-1 (versión y huella) en lugar de llevarlo dentro, y solo
puede estrecharlo. El Orquestador guarda los mandatos (SC-1) y los ofrece con mandato(cartera). Datos SIMULADOS."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

import contratos as ct  # noqa: E402
import mandatos as sc1  # noqa: E402
from orquestador import Orquestador  # noqa: E402
from validar_encargo import sobre_responde_a_encargo, validar_encargo  # noqa: E402
from validar_sobre import cargar_json  # noqa: E402
from pruebas_encargo import CTX, MANDATOS, encargo_div  # noqa: E402
from pruebas_orquestador import AHORA, CAL, CFG, Arnes, encargo, nuevo, sobre  # noqa: E402

MT = MANDATOS["TACTICA"]


def con(**cambio):
    return {**MANDATOS, "TACTICA": {**MT, **cambio}}


def detectado(o, n=1):
    assert o.detectar(f"EXP-{n:04d}", f"COR-{n:04d}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]


def main():
    h = Arnes()

    # ---------------------------------------------------------------- SC-1 en el Orquestador
    o = nuevo()
    m = o.mandato("TACTICA")
    h.chk("mandato_de_SC1", m["mandato"] == MT and m["referencia"] == sc1.referencia(MT) and m["version_sc1"] == sc1.VERSION_SC1)
    h.chk("mandato_es_una_copia", (m["mandato"].update(tamano_max_pct_cartera=99) or True) and o.mandato("TACTICA")["mandato"] == MT)
    h.chk("mandato_de_cartera_desconocida", o.mandato("OTRA") is None and o.mandato(None) is None)
    h.chk("config_050_con_mandatos", o.configuracion()["version_config"] >= "CFG-0.5.0" and o.configuracion()["orquestador"]["mandatos"] == MANDATOS)
    h.chk("los_mandatos_en_la_huella", nuevo().configuracion()["huella"] != nuevo({"mandatos": con(tamano_max_pct_cartera=8.0)}).configuracion()["huella"])
    malos = (("falta_cartera", {k: v for k, v in MANDATOS.items() if k != "TRADING"}),
             ("clave_extra", con(objetivo="crecer")), ("version_mal_formada", con(version="v1")),
             ("horizonte_fuera_de_la_cartera", con(horizonte_dias={"min": 2, "max": 90})),
             ("horizonte_invertido", con(horizonte_dias={"min": 90, "max": 20})),
             ("apalancamiento_sin_permiso", con(apalancamiento_max=2)), ("tamano_cero", con(tamano_max_pct_cartera=0)),
             ("tamano_texto", con(tamano_max_pct_cartera="5")), ("instrumentos_lista_vacia", con(instrumentos_permitidos=[])),
             ("instrumentos_repetidos", con(instrumentos_permitidos=["EUR/USD", "eur/usd"])),
             ("exclusion_no_texto", con(exclusiones=[7])), ("benchmark_distinto_de_la_referencia", con(benchmark_ref="BENCH-OTRO")))
    for nombre, mands in malos:
        try:
            Orquestador({**CFG, "mandatos": mands}, CAL)
            h.chk(f"config_mandato_{nombre}_se_rechaza", False)
        except ValueError:
            h.chk(f"config_mandato_{nombre}_se_rechaza", True)
    try:
        Orquestador({**CFG, "instrumentos_permitidos": {"TACTICA": ["EURUSD"]}}, CAL)
        h.chk("instrumentos_permitidos_ya_no_es_configuracion", False)
    except ValueError:
        h.chk("instrumentos_permitidos_ya_no_es_configuracion", True)
    h.chk("apalancamiento_con_permiso_se_acepta", Orquestador({**CFG, "apalancamiento_permitido": True, "mandatos": con(apalancamiento_max=2)}, CAL) is not None)

    # ---------------------------------------------------------------- el encargo cita el mandato vigente
    o = nuevo(); detectado(o)
    h.chk("encargo_con_el_mandato_vigente", o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"])
    for nombre, mut in (("sin_referencia", lambda p: p.pop("mandato_ref")),
                        ("de_otra_cartera", lambda p: p.update(mandato_ref=sc1.referencia(MANDATOS["TRADING"]))),
                        ("de_otra_version", lambda p: p["mandato_ref"].update(version="MAN-0.2.0")),
                        ("mandato_dentro_como_010", lambda p: (p.pop("mandato_ref"), p.update(mandato={"benchmark_ref": "BENCH-EFECTIVO"})))):
        o = nuevo(); detectado(o)
        e = encargo(1); mut(e["payload"])
        h.chk(f"encargo_{nombre}_O24", o.emitir_encargo("EXP-0001", e, "GESTOR_TACTICA", AHORA)["codigo"] == "O-24")
    o = nuevo({"mandatos": con(tamano_max_pct_cartera=8.0)}); detectado(o)
    h.chk("SC1_cambiado_el_encargo_viejo_no_vale_O24", o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["codigo"] == "O-24")
    e = encargo(1); e["payload"]["mandato_ref"] = o.mandato("TACTICA")["referencia"]
    h.chk("y_con_el_mandato_nuevo_si", o.emitir_encargo("EXP-0001", e, "GESTOR_TACTICA", AHORA)["ok"])
    # el mandato de SC-1 limita los instrumentos; el encargo no puede ampliarlos
    o = nuevo({"mandatos": con(instrumentos_permitidos=["GBP/USD"])}); detectado(o)
    e = encargo(1); e["payload"]["mandato_ref"] = o.mandato("TACTICA")["referencia"]
    r = o.emitir_encargo("EXP-0001", e, "GESTOR_TACTICA", AHORA)
    h.chk("instrumento_fuera_del_mandato_E10", r["codigo"] == "O-01" and "E-10" in r["reglas"], r)
    e["payload"]["restricciones"]["instrumentos_permitidos"] = ["EUR/USD"]
    r = o.emitir_encargo("EXP-0001", e, "GESTOR_TACTICA", AHORA)
    h.chk("el_encargo_no_amplia_instrumentos_E01", r["codigo"] == "O-01" and "E-01" in r["reglas"], r)
    o = nuevo({"mandatos": con(exclusiones=["EUR/USD"])}); detectado(o)
    e = encargo(1); e["payload"]["mandato_ref"] = o.mandato("TACTICA")["referencia"]
    r = o.emitir_encargo("EXP-0001", e, "GESTOR_TACTICA", AHORA)
    h.chk("instrumento_excluido_por_el_mandato_E10", r["codigo"] == "O-01" and "E-10" in r["reglas"], r)
    e = encargo(1); del e["payload"]["restricciones"]
    o = nuevo(); detectado(o)
    h.chk("sin_restricciones_vale_el_mandato_entero", o.emitir_encargo("EXP-0001", e, "GESTOR_TACTICA", AHORA)["ok"])
    e = encargo(1); e["payload"]["prioridad"] = "ALTA"
    h.chk("prioridad_ya_no_es_un_campo_E01", {x["regla"] for x in validar_encargo(e, CTX)} == {"E-01"})

    # ---------------------------------------------------------------- el sobre se cruza con el mandato de SC-1 (y sus restricciones)
    o = nuevo(); detectado(o)
    e = encargo(1); e["payload"]["restricciones"]["horizonte_dias"] = {"min": 14, "max": 60}
    assert o.emitir_encargo("EXP-0001", e, "GESTOR_TACTICA", AHORA)["ok"]
    r = o.entregar_sobre("EXP-0001", sobre(1), AHORA)
    h.chk("R13_horizonte_de_la_restriccion", r["codigo"] == "O-01" and "R-13" in r["motivo"], r)
    sob = cargar_json((AQUI / "validos" / "valido_div_n3.json").read_text(encoding="utf-8"))
    sctx = cargar_json((AQUI / "contexto.json").read_text(encoding="utf-8"))
    h.chk("sobre_responde_con_el_mandato_de_SC1", sobre_responde_a_encargo(encargo_div(), sob, CTX, sctx) == [])
    obt = {x["regla"] for x in sobre_responde_a_encargo(encargo_div(), sob, {**CTX, "mandatos": con(tamano_max_pct_cartera=8.0)}, sctx)}
    h.chk("mandato_cambiado_antes_del_sobre_R00", obt == {"R-00"}, obt)
    s2 = copy.deepcopy(sob); s2["payload"]["capital"]["apalancamiento"]["valor"] = 2
    m2 = con(apalancamiento_max=3)
    e2 = encargo_div(); e2["payload"]["mandato_ref"] = sc1.referencia(m2["TACTICA"])
    obt = {x["regla"] for x in sobre_responde_a_encargo(e2, s2, {**CTX, "mandatos": m2, "apalancamiento_permitido": True},
                                                        {**sctx, "apalancamiento_permitido": True})}
    h.chk("R08_con_el_apalancamiento_del_mandato_dentro", obt == set(), obt)
    obt = {x["regla"] for x in sobre_responde_a_encargo(encargo_div(), s2, CTX, {**sctx, "apalancamiento_permitido": True})}
    h.chk("R08_por_encima_del_mandato", obt == {"R-08"}, obt)

    # ---------------------------------------------------------------- registro de contratos
    reg = {c["tipo"]: c for c in ct.registro()["contratos"]}["CT-G-01"]
    h.chk("registro_01_en_020_con_010_retirada", reg["version"] == "0.2.0" and [v["estado"] for v in reg["versiones"]] == ["VIGENTE", "RETIRADA"]
          and ct.registro()["version_registro"] >= "REG-0.5.0")
    h.chk("CT_G_01_020_valida", ct.validar(encargo_div()) == [])
    viejo = encargo_div(); p = viejo["payload"]
    viejo["version_esquema"] = "0.1.0"; p.pop("mandato_ref"); p.pop("restricciones"); p["prioridad"] = "NORMAL"
    p["mandato"] = {"benchmark_ref": "BENCH-EFECTIVO", "horizonte_dias": {"min": 14, "max": 90}, "apalancamiento_max": 1,
                    "tamano_max_pct_cartera": 5, "instrumentos_permitidos": ["EUR/USD"], "exclusiones": []}
    h.chk("CT_G_01_010_retirada_CT02", [x["regla"] for x in ct.validar(viejo)] == ["CT-02"] and ct.validar(viejo, historico=True) == [])
    h.chk("validar_encargo_rechaza_la_010", [x["regla"] for x in validar_encargo(viejo, CTX)] == ["E-01"])

    # ================================================================ regresiones de la revisión independiente
    import pruebas_orquestador as po
    from pruebas_manual import libre, T1
    _enc = po.encargo

    def con_sc1(mands, restr=None):
        """Los encargos de las pruebas citan el mandato `mands` de TACTICA (y opcionalmente lo estrechan)."""
        def enc(*a, **k):
            x = _enc(*a, **k)
            x["payload"]["mandato_ref"] = sc1.referencia(mands["TACTICA"])
            x["payload"]["restricciones"].update(restr or {})
            return x
        po.encargo = enc
        return po.nuevo({"mandatos": mands})

    # H1: una exclusión no se esquiva cambiando el separador o con espacios invisibles (identidad única de instrumento)
    m = con(exclusiones=["EURUSD"])
    for grafia in ("EUR/USD", "EUR-USD", "eur.usd", "EUR  USD", "EUR\u00a0USD", "EUR\u200bUSD", "ＥＵＲ／ＵＳＤ"):
        e = encargo_div(); e["payload"]["mandato_ref"] = sc1.referencia(m["TACTICA"]); e["payload"]["candidato"]["instrumento"] = grafia
        h.chk(f"H1_exclusion_con_grafia_{grafia.encode('unicode_escape').decode()}_E10",
              "E-10" in {x["regla"] for x in validar_encargo(e, {**CTX, "mandatos": m})})
    for nombre, lista in (("repetidos_por_identidad", ["EUR/USD", "EURUSD"]), ("identidad_vacia", ["//"])):
        try:
            Orquestador({**CFG, "mandatos": con(instrumentos_permitidos=lista)}, CAL)
            h.chk(f"H1_lista_{nombre}_se_rechaza", False)
        except ValueError:
            h.chk(f"H1_lista_{nombre}_se_rechaza", True)
    # H2: el tamaño máximo del mandato (y el del encargo) limitan la propuesta
    o = con_sc1(con(tamano_max_pct_cartera=2.0), {"tamano_max_pct_cartera": 1.0})
    try:
        po.hasta(o, "PROPUESTA", entrada={**po.ENTRADA, "cantidad": 8000.0})
        h.chk("H2_tamano_del_encargo_limita_O23", False)
    except AssertionError as ex:
        h.chk("H2_tamano_del_encargo_limita_O23", "O-23" in str(ex) and "tamaño máximo del mandato (1.0 %" in str(ex), str(ex)[:200])
    o = con_sc1(con(tamano_max_pct_cartera=2.0))
    po.hasta(o, "PROPUESTA", entrada={**po.ENTRADA, "cantidad": 1500.0})   # 1.650 EUR de 100.000: 1,65 % < 2 %
    h.chk("H2_dentro_del_tamano_del_mandato_se_propone", o.expedientes["EXP-0001"]["estado"] == "PROPUESTA")
    # H3: el apalancamiento del mandato manda aunque el sistema y F lo permitan
    from control_f import POLITICA_DEFECTO
    po.encargo = _enc
    o2 = po.nuevo({"apalancamiento_permitido": True, "politica_f": {**POLITICA_DEFECTO, "apalancamiento_max": 3.0}})
    po.hasta(o2, "COMPARADA")
    po.elegir_si_hace_falta(o2, "EXP-0001")
    ent = {**po.ENTRADA, "apalancamiento": 3.0}
    r = o2.proponer("EXP-0001", ent, po.SALIDA, "GESTOR_TACTICA", AHORA, po.dim(o2, "EXP-0001", ent, None))
    h.chk("H3_apalancamiento_por_encima_del_mandato_O06", r["codigo"] == "O-06" and "mandato" in r["motivo"], r)
    # H4: un CT-G-14 LIBRE no opera un instrumento excluido por el mandato (con cualquier grafía)
    o = po.nuevo({"mandatos": con(exclusiones=["GBP/USD"])})
    r = o.registrar_manual(libre(), T1)
    h.chk("H4_ctg14_en_instrumento_excluido_RM08", r["codigo"] == "O-01" and r.get("reglas") == ["RM-08"] and o.manuales == [], r)
    # H7: RM-08 usa la identidad única: un permitido «GBP/USD» admite «GBPUSD»
    o = po.nuevo({"mandatos": con(instrumentos_permitidos=["GBP/USD"])})
    h.chk("H7_permitido_con_otra_grafia_se_admite", o.registrar_manual(libre(), T1)["ok"])
    # H5: un mandato alterado en caliente es un incidente (O-13 y kill-switch), también antes que O-24
    o = po.nuevo(); detectado(o)
    o.cfg["mandatos"]["TACTICA"]["tamano_max_pct_cartera"] = 50.0
    r = o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)
    h.chk("H5_encargar_con_mandato_alterado_O13_kill", r["codigo"] == "O-13" and o.kill is not None, r)
    o = po.nuevo(); po.hasta(o, "VALIDADA"); po.hasta(o, "VALIDADA", n=2)
    o.cfg["mandatos"]["TACTICA"]["tamano_max_pct_cartera"] = 50.0
    r = o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    h.chk("H5_comparar_con_mandato_alterado_O13_kill", r["codigo"] == "O-13" and o.kill is not None, r)
    o = po.nuevo({"mandatos": con(instrumentos_permitidos=["GBP/USD"])})
    o.cfg["mandatos"]["TACTICA"]["exclusiones"] = ["X"]
    h.chk("H5_manual_con_mandato_alterado_O13", o.comprobar_manual(libre(), T1)["codigo"] == "O-13"
          and o.registrar_manual(libre(), T1)["codigo"] == "O-13" and o.kill is not None)
    # H6: 10 y 10.0 son el mismo mandato (misma huella que la configuración)
    h.chk("H6_huella_canonica", sc1.huella(con(tamano_max_pct_cartera=10)["TACTICA"]) == sc1.huella(con(tamano_max_pct_cartera=10.0)["TACTICA"]))
    po.encargo = _enc

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO ENCARGO T-51:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
