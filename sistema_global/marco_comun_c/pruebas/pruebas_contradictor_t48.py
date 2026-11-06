"""Pruebas de T-48: el informe del Contradictor CT-G-03 0.2.0 (autoría y diversidad, escenarios de fallo, objeciones ligadas a
ellos) y el Contradictor exigido por defecto en N2 y N3."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

import contratos as ct  # noqa: E402
from orquestador import CONFIG_DEFECTO, Orquestador  # noqa: E402
from validar_contradictor import diversidad, validar_informe  # noqa: E402
from validar_sobre import proporcion_real  # noqa: E402
from pruebas_contradictor import AUTORIA, ESC, informe, obj  # noqa: E402
from pruebas_orquestador import AHORA, CAL, CFG, ENTRADA, S1, SALIDA, Arnes, dim, elegir_si_hace_falta, encargo, sobre  # noqa: E402

DEFECTO = {k: v for k, v in CFG.items() if k not in ("exige_contradictor_en", "contradictor_desactivado_motivo")}   # la configuración real: Contradictor en N2 y N3
C_DIV = {"modelo": "modelo-analista-1", "proveedor": "proveedor-a"}


def orq(**extra):
    o = Orquestador({**DEFECTO, **extra}, CAL)
    assert o.registrar_sello(S1, AHORA)["ok"]
    from pruebas_orquestador import registrar_motor   # T-26: los sobres citan artefactos del Motor
    registrar_motor(o)
    return o


def en_analisis(o, n=1, nivel=None):
    eid = f"EXP-{n:04d}"
    assert o.detectar(eid, f"COR-{n:04d}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    enc = encargo(n)
    if nivel:
        enc["payload"]["nivel_analisis"] = nivel
        enc["payload"]["decision_informada"] = "EXPLORAR"
    assert o.emitir_encargo(eid, enc, "GESTOR_TACTICA", AHORA)["ok"]
    return eid


def estado(o):
    return copy.deepcopy((o.expedientes, o.encargos, o.eventos, o.avisos))


def main():
    h = Arnes()
    S = sobre(1)
    ctx = {"ahora": AHORA, "sobre": S}

    def reglas(inf, c=None):
        return sorted({x["regla"] for x in validar_informe(inf, c or ctx)})

    def caso(nombre, inf, esperadas, c=None):
        r = reglas(inf, c)
        h.chk(nombre, r == esperadas, (r, validar_informe(inf, c or ctx)[:2]))

    # ---------------------------------------------------------------- validador: lo válido
    caso("valido_por_defecto", informe(S), [])
    caso("valido_mayor_con_escenario", informe(S, veredicto="OBJECION_MAYOR", objeciones=[obj(1, "MAYOR", ["EVID-0001"])]), [])
    caso("valido_mismo_modelo_con_motivo", informe(S, autoria={**AUTORIA, "diversidad": "MISMO_MODELO", "motivo_mismo_modelo": "no hay otro proveedor contratado"}), [])
    perdida = {**ESC, "id": "EF-2", "consecuencia": "PERDIDA", "perdida_pct": -12.5}
    caso("valido_escenario_de_perdida", informe(S, escenarios=[ESC, perdida]), [])
    caso("valido_objecion_menor_con_escenario", informe(S, objeciones=[obj(1, esc=["EF-1"])]), [])
    caso("valido_autoria_coherente_con_c", informe(S), [], c={**ctx, "autoria_c": C_DIV})
    caso("valido_otro_modelo_mismo_proveedor", informe(S, autoria={**AUTORIA, "proveedor": "PROVEEDOR.A", "diversidad": "OTRO_MODELO"}), [],
         c={**ctx, "autoria_c": C_DIV})
    # ---------------------------------------------------------------- C-11 autoría
    caso("C11_mismo_modelo_sin_motivo_lo_ve_el_esquema", informe(S, autoria={**AUTORIA, "diversidad": "MISMO_MODELO"}), ["C-01"])
    caso("C11_motivo_sin_ser_mismo_modelo_lo_ve_el_esquema", informe(S, autoria={**AUTORIA, "motivo_mismo_modelo": "x y z"}), ["C-01"])
    caso("C11_dice_otro_proveedor_y_es_el_mismo", informe(S, autoria={**AUTORIA, "proveedor": "proveedor-a"}), ["C-11"], c={**ctx, "autoria_c": C_DIV})
    caso("C11_dice_otro_modelo_y_es_el_mismo", informe(S, autoria={"modelo": "Modelo-Analista-1", "proveedor": "proveedor-a", "diversidad": "OTRO_MODELO"}),
         ["C-11"], c={**ctx, "autoria_c": C_DIV})
    caso("C11_dice_mismo_modelo_y_no_lo_es", informe(S, autoria={**AUTORIA, "diversidad": "MISMO_MODELO", "motivo_mismo_modelo": "por si acaso"}),
         ["C-11"], c={**ctx, "autoria_c": C_DIV})
    caso("C01_autoria_sin_proveedor", informe(S, autoria={"modelo": "m", "diversidad": "OTRO_PROVEEDOR"}), ["C-01"])
    caso("C01_proveedor_en_blanco", informe(S, autoria={**AUTORIA, "proveedor": "   "}), ["C-01"])
    caso("C01_diversidad_inventada", informe(S, autoria={**AUTORIA, "diversidad": "DIVERSO"}), ["C-01"])
    h.chk("diversidad_sin_autoria_de_c_es_desconocida", diversidad(AUTORIA, None) is None and diversidad(AUTORIA, {"modelo": "x"}) is None)
    # ---------------------------------------------------------------- C-12 escenarios de fallo
    caso("C01_sin_escenarios", informe(S, escenarios=[]), ["C-01"])
    caso("C12_ids_repetidos", informe(S, escenarios=[ESC, ESC]), ["C-12"])
    caso("C12_perdida_sin_porcentaje_lo_ve_el_esquema", informe(S, escenarios=[{**ESC, "consecuencia": "PERDIDA"}]), ["C-01"])
    caso("C12_perdida_cero_lo_ve_el_esquema", informe(S, escenarios=[{**ESC, "consecuencia": "PERDIDA", "perdida_pct": 0}]), ["C-01"])
    caso("C12_perdida_imposible_lo_ve_el_esquema", informe(S, escenarios=[{**ESC, "consecuencia": "PERDIDA", "perdida_pct": -150}]), ["C-01"])
    caso("C12_invalida_con_porcentaje_lo_ve_el_esquema", informe(S, escenarios=[{**ESC, "perdida_pct": -5}]), ["C-01"])
    caso("C12_evidencia_ajena", informe(S, escenarios=[{**ESC, "evid_refs": ["EVID-9999"]}]), ["C-12"])
    caso("C01_escenario_sin_evidencia", informe(S, escenarios=[{**ESC, "evid_refs": []}]), ["C-01"])
    caso("C01_disparador_sin_unidad", informe(S, escenarios=[{**ESC, "disparador": {k: v for k, v in ESC["disparador"].items() if k != "unidad"}}]), ["C-01"])
    caso("C01_disparador_no_numerico", informe(S, escenarios=[{**ESC, "disparador": {**ESC["disparador"], "umbral": "bajo"}}]), ["C-01"])
    # ---------------------------------------------------------------- C-13 objeciones ligadas
    caso("C13_mayor_sin_escenario", informe(S, veredicto="OBJECION_MAYOR", objeciones=[obj(1, "MAYOR", ["EVID-0001"], esc=[])]), ["C-13"])
    caso("C13_critica_sin_escenario", informe(S, veredicto="OBJECION_CRITICA", objeciones=[obj(1, "CRITICA", ["EVID-0001"], esc=[])]), ["C-13"])
    caso("C13_escenario_inexistente", informe(S, objeciones=[obj(1, esc=["EF-9"])]), ["C-13"])
    caso("C06_el_veredicto_sigue_siendo_el_de_las_objeciones", informe(S, veredicto="OBJECION_CRITICA", objeciones=[obj(1, "MAYOR", ["EVID-0001"])]), ["C-06"])
    # ---------------------------------------------------------------- versión retirada
    viejo = informe(S)
    viejo["version_esquema"] = "0.1.0"
    for k in ("autoria", "escenarios_fallo"):
        viejo["payload"].pop(k)
    for x in viejo["payload"]["objeciones"]:
        x.pop("escenarios")
    f = validar_informe(viejo, ctx)
    h.chk("C01_version_retirada", [x["regla"] for x in f] == ["C-01"] and "retirada" in f[0]["mensaje"], f)
    h.chk("contratos_03_retirada_CT02_e_historico", ct.validar(viejo)[0]["regla"] == "CT-02" and ct.validar(viejo, historico=True) == []
          and ct.validar(informe(S)) == [], (ct.validar(viejo), ct.validar(informe(S))))
    reg = {c["tipo"]: c for c in ct.registro()["contratos"]}["CT-G-03"]
    h.chk("registro_03_en_020_con_010_retirada", reg["version"] == "0.2.0" and [v["estado"] for v in reg["versiones"]] == ["VIGENTE", "RETIRADA"])
    h.chk("validar_nunca_lanza", all(validar_informe(x, ctx) for x in (None, [], {}, {**informe(S), "payload": None},
                                                                      {**informe(S), "payload": {**informe(S)["payload"], "escenarios_fallo": None}})))

    # ---------------------------------------------------------------- Orquestador con la configuración por defecto
    h.chk("por_defecto_exige_n2_y_n3", CONFIG_DEFECTO["exige_contradictor_en"] == ["N2", "N3"] and CONFIG_DEFECTO["version_config"] >= "CFG-0.2.0")
    o = orq()
    eid = en_analisis(o)
    antes = estado(o)
    r = o.entregar_sobre(eid, sobre(1), AHORA)
    h.chk("n3_sin_informe_O06", r["codigo"] == "O-06" and "Contradictor" in r["motivo"] and estado(o) == antes, r)
    o = orq(autoria_c={"C-DIV": C_DIV})
    eid = en_analisis(o)
    s = sobre(1)
    r = o.entregar_sobre(eid, s, AHORA, informe(s))
    h.chk("n3_con_informe_diverso_VALIDADA_sin_aviso", r["ok"] and o.expedientes[eid]["estado"] == "VALIDADA"
          and not [a for a in o.avisos if a["codigo"] == "O-33"], r)
    o = orq()
    eid = en_analisis(o)
    s = sobre(1)
    r = o.entregar_sobre(eid, s, AHORA, informe(s))
    av = [a for a in o.avisos if a["codigo"] == "O-33"]
    h.chk("sin_autoria_de_c_se_acepta_con_aviso_O33", r["ok"] and len(av) == 1 and "no se puede comprobar" in av[0]["motivo"]
          and av[0]["carteras"] == ["TACTICA"] and av[0]["prioridad"] == "MEDIA", (r, av))
    o = orq(autoria_c={"C-DIV": C_DIV})
    eid = en_analisis(o)
    s = sobre(1)
    mismo = {**C_DIV, "diversidad": "MISMO_MODELO", "motivo_mismo_modelo": "un solo proveedor contratado"}
    r = o.entregar_sobre(eid, s, AHORA, informe(s, autoria=mismo))
    av = [a for a in o.avisos if a["codigo"] == "O-33"]
    h.chk("mismo_modelo_se_acepta_con_aviso_O33", r["ok"] and len(av) == 1 and "mismo modelo" in av[0]["motivo"], (r, av))
    o = orq(autoria_c={"C-DIV": C_DIV})
    eid = en_analisis(o)
    s = sobre(1)
    antes = estado(o)
    r = o.entregar_sobre(eid, s, AHORA, informe(s, autoria={**C_DIV, "diversidad": "OTRO_PROVEEDOR"}))
    h.chk("diversidad_falsa_O01_C11_sin_cambios", r["codigo"] == "O-01" and "C-11" in r.get("reglas", []) and estado(o) == antes, r)
    antes = estado(o)
    r = o.entregar_sobre(eid, s, AHORA, viejo)
    h.chk("informe_010_O01_sin_cambios", r["codigo"] == "O-01" and "C-01" in r.get("reglas", []) and estado(o) == antes, r)
    s2 = sobre(1)
    r = o.entregar_sobre(eid, s2, AHORA, informe(s2, veredicto="OBJECION_CRITICA", objeciones=[obj(1, "CRITICA", ["EVID-0001"])]))
    h.chk("critica_ligada_a_escenario_retiene_O17", r["codigo"] == "O-17" and o.expedientes[eid]["retenido"] is not None, r)
    # N1 sigue siendo opcional con la configuración por defecto
    o = orq()
    eid = en_analisis(o, nivel="N1")
    s = sobre(1)
    p = s["payload"]
    p["identificacion"]["nivel_analisis"] = "N1"
    for k in ("capa2", "capa3", "estres_historico", "factores"):
        p.pop(k)
    p["evidencia"]["proporcion"] = {k: round(v, 4) for k, v in proporcion_real(p).items()}
    p["evidencia"]["proporcion"]["ESTIMADO"] = round(p["evidencia"]["proporcion"]["ESTIMADO"] + 1 - sum(p["evidencia"]["proporcion"].values()), 4)
    r = o.entregar_sobre(eid, s, AHORA)
    h.chk("n1_sin_informe_se_acepta", r["ok"] and o.expedientes[eid]["estado"] == "VALIDADA", r)
    # configuración
    for nombre, valor in (("no_dict", []), ("sin_proveedor", {"C-DIV": {"modelo": "m"}}), ("en_blanco", {"C-DIV": {"modelo": " ", "proveedor": "p"}}),
                          ("clave_de_mas", {"C-DIV": {**C_DIV, "x": 1}})):
        try:
            Orquestador({**DEFECTO, "autoria_c": valor}, CAL)
            h.chk(f"config_autoria_c_{nombre}_se_rechaza", False)
        except ValueError:
            h.chk(f"config_autoria_c_{nombre}_se_rechaza", True)
    h.chk("autoria_c_en_la_huella", orq().configuracion()["huella"] != orq(autoria_c={"C-DIV": C_DIV}).configuracion()["huella"])


    # ================================================================ regresiones de la revisión independiente
    # R1: el mismo modelo servido por otro proveedor no aporta diversidad
    revendido = {"modelo": "modelo-analista-1", "proveedor": "nube-revendedora"}
    h.chk("R1_mismo_modelo_otro_proveedor_es_MISMO_MODELO", diversidad(revendido, C_DIV) == "MISMO_MODELO")
    caso("R1_declararlo_otro_proveedor_C11", informe(S, autoria={**revendido, "diversidad": "OTRO_PROVEEDOR"}), ["C-11"], c={**ctx, "autoria_c": C_DIV})
    o = orq(autoria_c={"C-DIV": C_DIV}); eid = en_analisis(o); s = sobre(1)
    r = o.entregar_sobre(eid, s, AHORA, informe(s, autoria={**revendido, "diversidad": "MISMO_MODELO", "motivo_mismo_modelo": "mismo modelo en otra nube"}))
    h.chk("R1_declarado_honesto_se_acepta_con_O33", r["ok"] and any(a["codigo"] == "O-33" and "mismo modelo" in a["motivo"] for a in o.avisos), r)
    # R2: la grafía no fabrica diversidad y un MISMO_MODELO honesto con otra grafía se acepta
    for nombre, prov in (("punto", "proveedor.a"), ("mayusculas", "PROVEEDOR-A"), ("dos_puntos", "proveedor:a")):
        caso(f"R2_grafia_{nombre}_no_es_otro_proveedor", informe(S, autoria={"modelo": "otro-modelo", "proveedor": prov, "diversidad": "OTRO_PROVEEDOR"}),
             ["C-11"], c={**ctx, "autoria_c": C_DIV})
    caso("R2_caracter_invisible_C01", informe(S, autoria={**AUTORIA, "proveedor": "proveedor\u200ba"}), ["C-01"])
    caso("R2_ancho_completo_C01", informe(S, autoria={**AUTORIA, "proveedor": "\uff30roveedor-a"}), ["C-01"])
    caso("R2_mismo_modelo_honesto_con_otra_grafia", informe(S, autoria={"modelo": "Modelo.Analista.1", "proveedor": "PROVEEDOR-A", "diversidad": "MISMO_MODELO",
                                                                        "motivo_mismo_modelo": "solo hay un proveedor"}), [], c={**ctx, "autoria_c": C_DIV})
    caso("R2_contradictor_distinto_del_configurado_C11", informe(S), ["C-11"],
         c={**ctx, "autoria_contradictor": {"modelo": "modelo-contradictor-2", "proveedor": "proveedor-b"}})
    caso("R2_contradictor_configurado_con_otra_grafia", informe(S), [],
         c={**ctx, "autoria_contradictor": {"modelo": "MODELO.CONTRADICTOR.1", "proveedor": "Proveedor-B"}})
    o = orq(autoria_c={"C-DIV": C_DIV}, autoria_contradictor={"modelo": "otro", "proveedor": "otro"}); eid = en_analisis(o); s = sobre(1); antes = estado(o)
    r = o.entregar_sobre(eid, s, AHORA, informe(s))
    h.chk("R2_orquestador_exige_el_contradictor_configurado", r["codigo"] == "O-01" and "C-11" in r.get("reglas", []) and estado(o) == antes, r)
    # R3: el esquema dice lo mismo que Python
    for nombre, esc, aut in (("perdida_500", {**ESC, "consecuencia": "PERDIDA", "perdida_pct": 500}, None),
                             ("perdida_menos_1000", {**ESC, "consecuencia": "PERDIDA", "perdida_pct": -1000}, None),
                             ("perdida_0", {**ESC, "consecuencia": "PERDIDA", "perdida_pct": 0}, None),
                             ("invalida_con_pct", {**ESC, "perdida_pct": -5}, None),
                             ("mismo_modelo_sin_motivo", ESC, {**AUTORIA, "diversidad": "MISMO_MODELO"})):
        i = informe(S, escenarios=[esc], autoria=aut)
        h.chk(f"R3_esquema_rechaza_{nombre}", ct.validar(i) and ct.validar(i)[0]["regla"] == "CT-03" and reglas(i) == ["C-01"], (ct.validar(i), reglas(i)))
    # R4 y R5: configuración mal formada o con erratas no arranca (ValueError)
    for nombre, extra in (("exige_none", {"exige_contradictor_en": None}), ("exige_numero", {"exige_contradictor_en": 3}),
                          ("autoria_c_perfil_inexistente", {"autoria_c": {"C-Div": C_DIV}}),
                          ("autoria_contradictor_mal", {"autoria_contradictor": {"modelo": "m"}}),
                          ("sin_n2_n3_y_sin_motivo", {"exige_contradictor_en": ["N3"]}),
                          ("motivo_sin_desactivar", {"contradictor_desactivado_motivo": "no hace falta"}),
                          ("motivo_vacio", {"exige_contradictor_en": [], "contradictor_desactivado_motivo": "  "})):
        try:
            Orquestador({**DEFECTO, **extra}, CAL)
            h.chk(f"R4_config_{nombre}_ValueError", False)
        except ValueError:
            h.chk(f"R4_config_{nombre}_ValueError", True)
        except Exception as ex:   # noqa: BLE001
            h.chk(f"R4_config_{nombre}_ValueError", False, type(ex).__name__)
    # R6: desactivarlo exige motivo y queda en el historial de cada expediente
    o = orq(exige_contradictor_en=[], contradictor_desactivado_motivo="periodo de pruebas en L0")
    eid = en_analisis(o)
    r = o.entregar_sobre(eid, sobre(1), AHORA)
    h.chk("R6_sin_contradictor_queda_en_el_historial", r["ok"] and "sin Contradictor (desactivado: periodo de pruebas en L0)" in o.expedientes[eid]["historial"][-1]["motivo"], r)
    h.chk("R6_motivo_en_la_huella", orq(exige_contradictor_en=[], contradictor_desactivado_motivo="uno").configuracion()["huella"]
          != orq(exige_contradictor_en=[], contradictor_desactivado_motivo="otro").configuracion()["huella"])
    # R7: la autoría queda en el expediente y en la cadena
    o = orq(autoria_c={"C-DIV": C_DIV}); eid = en_analisis(o); s = sobre(1)
    assert o.entregar_sobre(eid, s, AHORA, informe(s))["ok"]
    c = o.expedientes[eid]["contradictor"]
    h.chk("R7_autoria_guardada", c["autoria"]["modelo"] == AUTORIA["modelo"] and c["diversidad"] == "OTRO_PROVEEDOR" and o.integridad() == [], c)
    o2 = copy.deepcopy(o); o2.expedientes[eid]["contradictor"]["autoria"]["modelo"] = "modelo-analista-1"
    h.chk("R7_autoria_alterada_se_detecta", o2.integridad() != [])
    o = orq(); eid = en_analisis(o); s = sobre(1)
    assert o.entregar_sobre(eid, s, AHORA, informe(s))["ok"]
    h.chk("R7_diversidad_no_comprobable_queda_anotada", o.expedientes[eid]["contradictor"]["diversidad"] == "NO_COMPROBABLE")
    # R8 y R9: documentación y registro
    leeme = (AQUI.parent / "LEEME.md").read_text(encoding="utf-8")
    h.chk("R9_leeme_no_sobrescribe_el_esquema_retirado", "generar_esquema_contradictor.py > esquemas/ct-g-03_0.1.0.schema.json" not in leeme
          and "generar_esquema_contradictor.py > esquemas/ct-g-03_0.2.0.schema.json" in leeme)
    h.chk("R8_registro_REG030", ct.registro()["version_registro"] >= "REG-0.3.0")
    # extremo a extremo con la configuración por defecto: dos candidatos con informe, comparación y propuesta
    o = orq(autoria_c={"C-DIV": C_DIV})
    for n in (1, 2):
        eid = en_analisis(o, n); s = sobre(n)
        assert o.entregar_sobre(eid, s, AHORA, informe(s, n=n))["ok"]
    r = o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    elegir_si_hace_falta(o, "EXP-0001", AHORA)
    rp = o.proponer("EXP-0001", ENTRADA, SALIDA, "GESTOR_TACTICA", AHORA, dim(o, "EXP-0001"))
    h.chk("extremo_con_contradictor_por_defecto_llega_a_propuesta", r["ok"] and rp["ok"] and o.integridad() == [], (r, rp))

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO CONTRADICTOR T-48:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
