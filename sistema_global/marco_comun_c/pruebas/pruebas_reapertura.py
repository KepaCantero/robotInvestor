"""Pruebas de las condiciones de reapertura vigiladas (T-46). Datos SIMULADOS.

Comprueba: `observar` exige condiciones comprobables (PRECIO, FECHA, SELLO_NUEVO); H y el barrido las vigilan y avisan (O-31,
H-15); solo se re-encarga con una condición cumplida o con `reabrir` del operador; límite de reaperturas; la observación vence
sola y el expediente queda descartado; todo va en la cadena de hashes.

Uso: python3 pruebas/pruebas_reapertura.py
"""
import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from ejecucion_g import BrokerSimulado  # noqa: E402
from vigilancia import vigilar  # noqa: E402
from pruebas_orquestador import AHORA, S2, Arnes, encargo, hasta, nuevo  # noqa: E402

EID = "EXP-0001"
PRECIO = {"tipo": "PRECIO", "instrumento": "EURUSD", "operador": ">=", "umbral": 1.12}
FECHA = {"tipo": "FECHA", "fecha": "2026-11-10"}
T1 = "2026-11-06T09:05:00+00:00"


def en_obs(conds, actor="GESTOR_TACTICA", estado="VALIDADA"):
    o = nuevo()
    hasta(o, estado)
    r = o.observar(EID, conds, "esperar a que se den las condiciones", actor, AHORA)
    assert r["ok"], r
    return o


def reencargo(o, n, ahora=AHORA):
    enc = encargo(1)
    enc["event_id"] = f"EV-ENC-01{n:02d}"
    return o.emitir_encargo(EID, enc, "GESTOR_TACTICA", ahora)


def precio(p, hora=T1):
    return {"EURUSD": {"precio": p, "hora": hora}}


def main():
    h = Arnes()
    # ------------------------------------------------------------ condiciones comprobables
    o = nuevo()
    hasta(o, "VALIDADA")
    for nombre, conds, codigo in (("texto_libre", ["EURUSD > 1.12"], "O-01"), ("vacias", [], "O-15"), ("no_lista", "x", "O-15"),
                                  ("tipo_raro", [{"tipo": "VOLATILIDAD"}], "O-01"),
                                  ("precio_sin_umbral", [{"tipo": "PRECIO", "instrumento": "EURUSD", "operador": ">"}], "O-01"),
                                  ("precio_operador_raro", [{**PRECIO, "operador": "=>"}], "O-01"),
                                  ("precio_umbral_negativo", [{**PRECIO, "umbral": -1}], "O-01"),
                                  ("precio_campo_de_mas", [{**PRECIO, "x": 1}], "O-01"),
                                  ("fecha_hoy", [{"tipo": "FECHA", "fecha": "2026-11-06"}], "O-01"),
                                  ("fecha_imposible", [{"tipo": "FECHA", "fecha": "2026-02-30"}], "O-01"),
                                  ("sello_con_campos", [{"tipo": "SELLO_NUEVO", "x": 1}], "O-01"),
                                  ("demasiadas", [FECHA] * 11, "O-01")):
        h.rechaza(f"observar_{nombre}_{codigo.replace('-', '')}", o, lambda c=conds: o.observar(EID, c, "esperar", "GESTOR_TACTICA", AHORA), codigo)
    r = o.observar(EID, [PRECIO, FECHA, {"tipo": "SELLO_NUEVO"}], "esperar", "GESTOR_TACTICA", AHORA)
    h.chk("observar_con_condiciones_comprobables", r["ok"] and r["vence"] == "2026-12-06" and o.expedientes[EID]["reapertura"]["cumplida"] is None, r)

    # ------------------------------------------------------------ sin condición cumplida no se re-encarga
    o = en_obs([PRECIO])
    antes = copy.deepcopy(o.expedientes[EID])
    r = reencargo(o, 1)
    h.chk("reencargar_sin_condicion_cumplida_O06", r["codigo"] == "O-06" and o.expedientes[EID]["estado"] == "EN_OBSERVACION", r)

    # ------------------------------------------------------------ PRECIO: lo vigila H
    for nombre, d, cumple in (("no_llega", precio(1.11), False), ("viejo", precio(1.13, "2026-11-06T08:00:00+00:00"), False),
                              ("futuro", precio(1.13, "2026-11-06T10:00:00+00:00"), False), ("otro_instrumento", {"GBPUSD": {"precio": 2.0, "hora": T1}}, False),
                              ("basura", {"EURUSD": {"precio": "x", "hora": "ayer"}}, False), ("se_cumple", precio(1.12), True)):
        o = en_obs([PRECIO])
        r = o.revisar_reaperturas(d, "H", T1)
        h.chk(f"precio_{nombre}", r["ok"] and (r["cumplidas"] == [EID]) == cumple and (o.expedientes[EID]["reapertura"]["cumplida"] is not None) == cumple, r)
    o = en_obs([PRECIO])
    h.rechaza("solo_H_o_el_orquestador_vigilan_O05", o, lambda: o.revisar_reaperturas(precio(1.13), "GESTOR_TACTICA", T1), "O-05")
    b = BrokerSimulado(100000.0, {"EURUSD": 1.13}, "2026-11-06T09:00:00+00:00", tipos_cambio={"USD": 1.0})
    r = vigilar(o, b, precio(1.13), T1)
    av = [x for x in o.avisos if x["codigo"] == "O-31"]
    h.chk("H15_vigilar_marca_la_reapertura_y_avisa", any(a["regla"] == "H-15" and a["expediente"] == EID for a in r["acciones"])
          and len(av) == 1 and av[0]["carteras"] == ["TACTICA"] and o.integridad() == [], (r, av))
    r = vigilar(o, b, precio(1.13, "2026-11-06T09:06:00+00:00"), "2026-11-06T09:06:00+00:00")
    h.chk("H15_no_se_repite", not any(a["regla"] == "H-15" for a in r["acciones"]), r)
    r = reencargo(o, 1, "2026-11-06T09:06:00+00:00")
    h.chk("con_la_condicion_cumplida_se_reencarga", r["ok"] and o.expedientes[EID]["estado"] == "EN_ANALISIS", r)

    # ------------------------------------------------------------ FECHA y SELLO_NUEVO: los comprueba el barrido o el propio re-encargo
    o = en_obs([FECHA])
    r = o.barrer("2026-11-10T08:00:00+00:00")
    h.chk("fecha_la_marca_el_barrido", ("reapertura", EID, "CUMPLIDA") in r["cambios"], r)
    o = en_obs([FECHA])
    h.chk("fecha_antes_de_llegar_no", reencargo(o, 1, "2026-11-09T08:00:00+00:00")["codigo"] == "O-06")
    o = en_obs([FECHA])
    r = reencargo(o, 1, "2026-11-10T08:00:00+00:00")
    # pasa la reapertura y lo siguiente que falla es el encargo de prueba, ya caducado ese día (E-03); un encargo rechazado no deja la
    # condición marcada (si no, un rechazo con una hora adelantada permitiría reabrir antes de tiempo)
    h.chk("fecha_llegada_se_comprueba_al_reencargar", r["codigo"] == "O-01" and "E-03" in r.get("reglas", [])
          and o.expedientes[EID]["reapertura"]["cumplida"] is None and o.integridad() == [], r)
    o = en_obs([{"tipo": "SELLO_NUEVO"}])
    h.chk("sello_nuevo_sin_sello_no", reencargo(o, 1)["codigo"] == "O-06")
    assert o.registrar_sello(S2, "2026-11-06T09:10:00+00:00")["ok"]
    r = o.barrer("2026-11-06T09:11:00+00:00")
    h.chk("sello_nuevo_con_corte_posterior_se_cumple", ("reapertura", EID, "CUMPLIDA") in r["cambios"]
          and o.expedientes[EID]["reapertura"]["cumplida"]["valor"] == "2026-11-06", r)

    # ------------------------------------------------------------ límite de reaperturas
    o = nuevo({"max_reaperturas": 1})
    hasta(o, "VALIDADA")
    o.observar(EID, [PRECIO], "uno", "GESTOR_TACTICA", AHORA)
    o.revisar_reaperturas(precio(1.13), "H", T1)
    h.chk("primera_reapertura_vale", reencargo(o, 1, T1)["ok"])
    o.observar(EID, [PRECIO], "dos", "GESTOR_TACTICA", T1)
    o.revisar_reaperturas(precio(1.13, "2026-11-06T09:06:00+00:00"), "H", "2026-11-06T09:06:00+00:00")
    r = reencargo(o, 2, "2026-11-06T09:06:00+00:00")
    h.chk("pasado_el_limite_O06", r["codigo"] == "O-06" and "solo el operador" in r["motivo"], r)
    h.chk("el_operador_reabre_aun_pasado_el_limite", o.reabrir(EID, "merece otra mirada", "OPERADOR", "2026-11-06T09:07:00+00:00")["ok"]
          and reencargo(o, 2, "2026-11-06T09:07:00+00:00")["ok"])

    # ------------------------------------------------------------ reabrir (operador)
    o = en_obs([PRECIO])
    h.rechaza("reabrir_solo_el_operador_O05", o, lambda: o.reabrir(EID, "x", "GESTOR_TACTICA", AHORA), "O-05")
    h.rechaza("reabrir_sin_motivo_O15", o, lambda: o.reabrir(EID, " ", "OPERADOR", AHORA), "O-15")
    o2 = nuevo(); hasta(o2, "VALIDADA")
    h.rechaza("reabrir_lo_que_no_esta_en_observacion_O04", o2, lambda: o2.reabrir(EID, "x", "OPERADOR", AHORA), "O-04")
    h.chk("reabrir_y_reencargar", o.reabrir(EID, "cambió el contexto", "OPERADOR", AHORA)["ok"] and reencargo(o, 1)["ok"])

    # ------------------------------------------------------------ la observación vence
    o = en_obs([PRECIO])
    h.chk("reencargar_tras_vencer_O10", reencargo(o, 1, "2026-12-07T09:00:00+00:00")["codigo"] == "O-10")
    o = en_obs([PRECIO])
    r = o.barrer("2026-12-07T09:00:00+00:00")
    x = o.expedientes[EID]
    h.chk("el_barrido_descarta_la_observacion_vencida", x["estado"] == "DESCARTADA" and x["historial"][-1]["actor"] == "ORQUESTADOR"
          and any(a["codigo"] == "O-31" and "venció" in a["motivo"] for a in o.avisos), r)
    o = en_obs([PRECIO])
    r = o.barrer("2026-12-06T23:00:00+00:00")
    h.chk("el_dia_que_vence_aun_vale", o.expedientes[EID]["estado"] == "EN_OBSERVACION", r)

    # ------------------------------------------------------------ integridad
    for nombre, mut in (("marcar_cumplida", lambda x: x["reapertura"].__setitem__("cumplida", {"condicion": 0, "valor": 9, "ahora": AHORA, "por": "H"})),
                        ("alargar_el_vencimiento", lambda x: x["reapertura"].__setitem__("vence", "2099-01-01")),
                        ("cambiar_la_condicion", lambda x: x["reapertura"]["condiciones"][0].__setitem__("umbral", 0.5)),
                        ("borrar_la_reapertura", lambda x: x.__setitem__("reapertura", None))):
        o = en_obs([PRECIO])
        mut(o.expedientes[EID])
        r = reencargo(o, 1)
        h.chk(f"alterar_{nombre}_O13", r["codigo"] == "O-13" and o.integridad() == ["EXP:" + EID] and o.expedientes[EID]["estado"] == "EN_OBSERVACION", r)
    o = en_obs([PRECIO])
    o.expedientes[EID]["reapertura"]["vence"] = "2099-01-01"
    r = o.revisar_reaperturas(precio(1.13), "H", T1)
    h.chk("H_no_marca_un_expediente_alterado", r["cumplidas"] == [], r)

    # ------------------------------------------------------------ revisión independiente (regresiones)
    # G1: ratificar un apartado en observación no rompe la integridad
    o = en_obs([PRECIO])
    r = o.ratificar_apartado(EID, "de acuerdo con apartarlo", "OPERADOR", T1)
    h.chk("G1_ratificar_en_observacion_mantiene_la_integridad", r["ok"] and o.integridad() == [] and o.kill is None
          and o.revisar_reaperturas(precio(1.13), "H", T1)["cumplidas"] == [EID], r)
    # G2: un encargo rechazado (con la hora adelantada) no deja la condición marcada
    o = en_obs([FECHA])
    r = o.emitir_encargo(EID, {"event_id": "X-1"}, "GESTOR_TACTICA", "2026-11-10T08:00:00+00:00")
    h.chk("G2_encargo_rechazado_no_marca_la_condicion", r["codigo"] == "O-12" and o.expedientes[EID]["reapertura"]["cumplida"] is None, r)
    h.chk("G2_y_no_se_reencarga_antes_de_la_fecha", reencargo(o, 1, "2026-11-06T09:30:00+00:00")["codigo"] == "O-06")
    # M1: SELLO_NUEVO se mide contra el corte más reciente (también el del encargo en curso)
    o = en_obs([{"tipo": "SELLO_NUEVO"}])
    o.registrar_sello(S2, "2026-11-06T09:10:00+00:00")
    h.chk("M1_corte_previo_es_el_del_analisis", o.expedientes[EID]["reapertura"]["corte_previo"] == "2026-11-05")
    o2 = nuevo(); hasta(o2, "EN_ANALISIS")
    o2.observar(EID, [{"tipo": "SELLO_NUEVO"}], "esperar datos", "GESTOR_TACTICA", AHORA)
    h.chk("M1_desde_EN_ANALISIS_el_corte_del_encargo", o2.expedientes[EID]["reapertura"]["corte_previo"] == "2026-11-05")
    # M2: SELLO_NUEVO solo con un sello vigente para la cartera del expediente
    o = en_obs([{"tipo": "SELLO_NUEVO"}])
    o.registrar_sello(S2, "2026-11-06T09:10:00+00:00")
    r = o.barrer("2026-11-11T09:00:00+00:00")   # el 11-11 el sello del 11-06 ya no vale para TACTICA
    h.chk("M2_sello_caducado_para_la_cartera_no_cumple", o.expedientes[EID]["reapertura"]["cumplida"] is None, r)
    # A, B, C, D: vencimiento y límite
    o = en_obs([PRECIO])
    r = o.revisar_reaperturas(precio(1.13, "2026-12-07T09:00:00+00:00"), "H", "2026-12-07T09:00:00+00:00")
    h.chk("A_vencida_no_se_marca", r["cumplidas"] == [] and not [x for x in o.avisos if x["codigo"] == "O-31"], r)
    o = nuevo({"max_reaperturas": 0}); hasta(o, "VALIDADA")
    o.observar(EID, [PRECIO], "x", "GESTOR_TACTICA", AHORA)
    o.revisar_reaperturas(precio(1.13), "H", T1)
    av = [x for x in o.avisos if x["codigo"] == "O-31"]
    h.chk("B_el_aviso_dice_que_solo_el_operador_puede", len(av) == 1 and "solo el operador" in av[0]["motivo"], av)
    o = en_obs([PRECIO])
    h.rechaza("C_reabrir_vencida_O10", o, lambda: o.reabrir(EID, "x", "OPERADOR", "2026-12-07T09:00:00+00:00"), "O-10")
    o = nuevo(); hasta(o, "VALIDADA")
    h.rechaza("D_fecha_posterior_al_vencimiento_O01", o, lambda: o.observar(EID, [{"tipo": "FECHA", "fecha": "2027-06-01"}], "x", "GESTOR_TACTICA", AHORA), "O-01")
    # E: el instrumento con otra grafía
    o = en_obs([{**PRECIO, "instrumento": "EUR/USD"}])
    h.chk("E_instrumento_con_barra_se_cumple_con_EURUSD", o.revisar_reaperturas(precio(1.13), "H", T1)["cumplidas"] == [EID])
    # F: el encargo que quedó en curso al observar se anula al reabrir
    o = nuevo(); hasta(o, "EN_ANALISIS")
    viejo = o.expedientes[EID]["encargo_actual"]
    o.observar(EID, [PRECIO], "esperar", "GESTOR_TACTICA", AHORA)
    o.reabrir(EID, "ya", "OPERADOR", AHORA)
    r = reencargo(o, 1)
    h.chk("F_el_encargo_viejo_queda_anulado", r["ok"] and o.encargos[viejo]["estado"] == "ANULADO", r)
    # frescura: la de H
    o = en_obs([PRECIO])
    r = o.revisar_reaperturas(precio(1.13, "2026-11-06T08:55:00+00:00"), "H", T1, max_edad_min=5)
    h.chk("frescura_la_misma_que_H", r["cumplidas"] == [], r)
    # G: lo que reabre el operador no cuenta para el límite
    o = nuevo({"max_reaperturas": 1}); hasta(o, "VALIDADA")
    o.observar(EID, [PRECIO], "uno", "GESTOR_TACTICA", AHORA)
    o.reabrir(EID, "lo reabro yo", "OPERADOR", AHORA)
    reencargo(o, 1, T1)
    o.observar(EID, [PRECIO], "dos", "GESTOR_TACTICA", T1)
    o.revisar_reaperturas(precio(1.13, "2026-11-06T09:06:00+00:00"), "H", "2026-11-06T09:06:00+00:00")
    h.chk("G_la_reapertura_del_operador_no_cuenta", reencargo(o, 2, "2026-11-06T09:06:00+00:00")["ok"])

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO REAPERTURA:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
