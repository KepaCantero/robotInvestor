"""QA r02 de T-75 (V0.73): sondas del revisor contra las correcciones de H-01..H-08 y las regresiones que pueden abrir.

Cada sonda imprime OK o HALLAZGO con lo observado. No cambia el código ni las pruebas.
Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.70/qa/r02_sondas_embudo_sequia.py
"""
import copy
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

MARCO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
import contratos as ct  # noqa: E402
import diario as di  # noqa: E402
import persistencia as pe  # noqa: E402
from consola import cola_aprobaciones, informe_embudo  # noqa: E402
from orquestador import MOTIVO_VETO_F, Orquestador  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_k import CAL  # noqa: E402
from pruebas_operador_t50 import MOTIVO, T_ESPERA, aprobacion, vetado  # noqa: E402
from pruebas_orquestador import AHORA, CFG, S1, autorizar_op, hasta, registrar_motor  # noqa: E402

T0 = "2026-09-01T09:00:00+00:00"
hallazgos, oks = [], []


def mas(t, **kw):
    return (datetime.fromisoformat(t) + timedelta(**kw)).isoformat()


def antiguo(cfg=None):
    o = Orquestador({**CFG, **(cfg or {})}, CAL)
    assert o.degradar("TRADING", "arranque de prueba: el operador deja TRADING en L1", "OPERADOR", T0)["ok"]
    assert o.registrar_sello(S1, AHORA)["ok"]
    registrar_motor(o, S1["sello_id"])
    return o


def ver(nombre, cond_ok, obs):
    print(("OK      " if cond_ok else "HALLAZGO"), nombre, "::", obs)
    (oks if cond_ok else hallazgos).append(nombre)


def o40(o):
    return [x for x in o.avisos if x["codigo"] == "O-40"]


def fila(em, eid):
    return next((x for x in em["oportunidades"] if x["expediente_id"] == eid), None)


def vetos(o, eid="EXP-0001"):
    return [h for h in o.expedientes[eid]["historial"] if h["desde"] == h["hasta"] == "PROPUESTA" and h["actor"] == "F"]


# ============================================================================== 1. H-08: sequía con barridos de cualquier ritmo
def base_s19():
    o = antiguo()
    hasta(o, "EJECUTADA", 1)                            # inversión a las 09:00 del día 0
    hasta(o, "VALIDADA", 5, ahora=mas(AHORA, hours=1))  # candidato a las 10:00, que nadie invierte
    return o


def p01_barridos_a_cualquier_hora():
    """Un barrido diario a cada hora del día (0..23) durante 130 días: dos alarmas (una por plazo) para todas las horas."""
    malas = {}
    d0 = datetime.fromisoformat(AHORA).replace(hour=0)
    for hora in range(0, 24, 1):
        o = base_s19()
        for d in range(1, 131):
            o.barrer((d0 + timedelta(days=d, hours=hora)).isoformat())
        n = len(o40(o))
        if n != 2:
            malas[hora] = n
    ver("p01_barrido_diario_a_cualquier_hora_da_una_alarma_por_plazo", not malas, f"horas con un número de O-40 distinto de 2: {malas}")


def p02_barridos_espaciados():
    """Ritmos: cada hora (3 días alrededor del borde), semanal, cada 59, 60 y 61 días, e irregular."""
    res = {}
    for nombre, pasos in (("semanal", [timedelta(days=7 * k) for k in range(1, 19)]),
                          ("cada_59d", [timedelta(days=59 * k) for k in range(1, 3)]),
                          ("cada_60d", [timedelta(days=60 * k) for k in range(1, 3)]),
                          ("cada_61d", [timedelta(days=61 * k) for k in range(1, 3)]),
                          ("irregular", [timedelta(days=d, hours=h) for d, h in ((3, 5), (17, 1), (44, 23), (61, 2), (62, 0), (99, 7), (121, 22))])):
        o = base_s19()
        for p in pasos:
            o.barrer((datetime.fromisoformat(AHORA) + p).isoformat())
        res[nombre] = len(o40(o))
    o = base_s19()
    for hh in range(0, 72):
        o.barrer(mas(AHORA, days=59, hours=hh))
    res["horario_en_el_borde"] = len(o40(o))
    t_aviso = o40(o)[0]["ahora"] if o40(o) else None
    esperado = {"semanal": 2, "cada_59d": 1, "cada_60d": 2, "cada_61d": 2, "irregular": 2, "horario_en_el_borde": 1}
    ver("p02_barridos_espaciados_y_horarios", res == esperado and t_aviso == mas(AHORA, days=60),
        f"O-40 por ritmo={res} (esperado {esperado}); primer aviso horario en {t_aviso}")


def p03_borde_exacto():
    o = base_s19()
    t = mas(AHORA, days=60)
    a, b = o.sequia(mas(t, microseconds=-1)), o.sequia(t)
    o2 = Orquestador(CFG, CAL)   # sin inversiones nunca: el primer instante es AHORA (sello, Motor y validación)
    assert o2.registrar_sello(S1, AHORA)["ok"]
    registrar_motor(o2, S1["sello_id"])
    hasta(o2, "VALIDADA", 1)
    c, d, e = o2.sequia(mas(AHORA, days=60, microseconds=-2)), o2.sequia(mas(AHORA, days=60, microseconds=-1)), o2.sequia(mas(AHORA, days=60))
    ver("p03_borde_exacto_de_60_dias", not a["activa"] and b["activa"] and not c["activa"] and not d["activa"] and e["activa"],
        f"con inversión: 60d-1µs={a['activa']} 60d={b['activa']}; sin inversiones: 60d-2µs={c['activa']} 60d-1µs={d['activa']} "
        f"({d['motivo']}) 60d={e['activa']}")
    return d["activa"]


def p04_sin_inversiones_nunca_y_otras_carteras():
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    n = []
    for d in range(1, 131):
        o.barrer(mas(T0, days=d, hours=-3))
    n.append(len(o40(o)))
    # inversión en TACTICA; candidato validado en TACTICA después: alarma; con la inversión en otra cartera (documentado como límite)
    o2 = base_s19()
    sq = o2.sequia(mas(AHORA, days=61))
    ver("p04_sin_inversiones_nunca_salta_y_se_repite", n == [2] and sq["activa"] and sq["validadas"] == 1,
        f"sin inversiones, 130 barridos diarios: O-40={n}; con inversión previa y candidato posterior: activa={sq['activa']} validadas={sq['validadas']}")


def p05_directa_E_tras_la_inversion():
    """Un análisis validado antes de la última inversión y reutilizado después por la vía DIRECTA. Por D nace VALIDADA y cuenta como
    candidato; por E nace COMPARADA. ¿Cuentan igual para la sequía?"""
    out = {}
    for via in ("D", "E"):
        o = antiguo()
        hasta(o, "EJECUTADA", 1)   # se invierte EXP-0001 a AHORA; su rival EXP-0002 (sobre EV-SOB-0002) queda validado y comparado
        assert o.descartar("EXP-0002", "el operador lo aparta por ahora", "OPERADOR", mas(AHORA, minutes=1))["ok"]
        kw = {"motivo": "candidato único: no hay otro análisis vigente en la cartera"} if via == "E" else {}
        r = o.abrir_directa(f"EXP-D{via}-01", f"COR-D{via}-01", "TACTICA", via, "BROKER", mas(AHORA, minutes=2), analisis="EV-SOB-0002", **kw)
        sq = o.sequia(mas(AHORA, days=61))
        out[via] = (r["codigo"], o.expedientes.get(f"EXP-D{via}-01", {}).get("estado"), sq["validadas"], sq["activa"])
    ver("p05_directa_por_D_y_por_E_cuentan_igual_en_la_sequia", out["D"][2] == out["E"][2], f"(abrir, estado, validadas, activa)={out}")


# ============================================================================== 2. H-01: el veto de F por todas sus entradas
def p06_veto_por_la_pantalla_del_operador():
    """El camino del operador es pedir la pantalla (autorizar_op de las pruebas, y la cola de la consola): con un informe que veta,
    pantalla_aprobacion da O-06 y consume el informe. ¿Queda anotado el veto?"""
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    cola = [x["tipo"] for x in cola_aprobaciones(o, AHORA) if x["ref"] == "EXP-0001"]
    inf = vetado(o)
    r = o.pantalla_aprobacion("EXP-0001", inf, AHORA)
    r2 = o.autorizar("EXP-0001", "OPERADOR", inf, AHORA)   # ya no se anota: el informe está usado
    em = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    o.barrer(mas(AHORA, days=3))
    em2 = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, days=3))
    sal = [(x["hasta"], x["bloqueo_previo"]) for x in em2["salidas"] if x["expediente_id"] == "EXP-0001"]
    ver("p06_veto_visto_en_la_pantalla_del_operador_queda_en_el_embudo", fila(em, "EXP-0001")["bloqueo"] is not None,
        f"cola={cola}; pantalla={r['codigo']} ({r['motivo']}); autorizar después={r2['codigo']}; anotaciones de veto={len(vetos(o))}; "
        f"fila={ {k: fila(em, 'EXP-0001')[k] for k in ('capa', 'actor', 'motivo', 'bloqueo')} }; salida={sal}")


def p07_veto_por_la_matriz():
    o = antiguo({"nivel_autonomia": {"TACTICA": "L2"}, "matriz_autonomia": {"TACTICA": True}})
    hasta(o, "PROPUESTA", 1)
    r = o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", vetado(o), AHORA)
    em = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    f = fila(em, "EXP-0001")
    ver("p07_veto_en_la_autorizacion_automatica_queda_anotado", r["codigo"] == "O-06" and f["bloqueo"] and o.integridad() == [],
        f"autorizar={r['codigo']}; fila capa={f['capa']} actor={f['actor']} bloqueo={f['bloqueo']!r}; integridad={o.integridad()}")


def p08_propuesta_CT_G_06_tras_el_veto():
    """contratos.propuesta toma la última anotación que llega a PROPUESTA como emisor e instante de la propuesta."""
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    m0 = ct.propuesta(o, "EXP-0001")
    r = o.autorizar("EXP-0001", "OPERADOR", vetado(o), mas(AHORA, minutes=5))
    m1 = ct.propuesta(o, "EXP-0001")
    ver("p08_la_propuesta_CT_G_06_sigue_valida_e_igual_tras_el_veto", ct.validar(m1) == [] and m1["event_id"] == m0["event_id"],
        f"autorizar={r['codigo']}; antes producer={m0['producer']} emitido={m0['emitido_en']} validar={ct.validar(m0)}; "
        f"después producer={m1['producer']} emitido={m1['emitido_en']} event_id igual={m1['event_id'] == m0['event_id']} "
        f"validar={[(x['regla'], x['mensaje'][:60]) for x in ct.validar(m1)]}")


def p09_tras_el_veto_otro_informe_autoriza_ejecuta_y_cuadra():
    from ejecucion_g import ejecutar
    from pruebas_ejecucion_g import broker
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    assert o.autorizar("EXP-0001", "OPERADOR", vetado(o), AHORA)["codigo"] == "O-06"
    inf2 = informe_f(o, "EXP-0001", 2)
    r = autorizar_op(o, "EXP-0001", inf2, AHORA)
    e = o.expedientes["EXP-0001"]
    po = o._propuesta_ok(e)
    ordn = ct.orden(o, "EXP-0001")
    b = broker()
    rx = ejecutar(o, "EXP-0001", b, AHORA)
    em = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    ver("p09_tras_el_veto_otro_informe_de_F_autoriza_y_ejecuta", r["ok"] and po and ordn and ct.validar(ordn) == [] and o.integridad() == []
        and e["estado"] == "EJECUTADA",
        f"autorizar_op={r['codigo']}; _propuesta_ok={po}; orden válida={ordn is not None and ct.validar(ordn) == []}; ejecutar={rx.get('codigo') if isinstance(rx, dict) else rx}; "
        f"estado={e['estado']}; integridad={o.integridad()}; fila={ {k: fila(em, 'EXP-0001')[k] for k in ('capa', 'bloqueo')} }")


def p10_anulacion_T50_tras_un_veto_anotado():
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    assert o.autorizar("EXP-0001", "OPERADOR", vetado(o), AHORA)["codigo"] == "O-06"
    inf2 = vetado(o, n=2)
    p = o.pantalla_aprobacion("EXP-0001", inf2, AHORA, anular_veto={"motivo": MOTIVO})
    r = o.autorizar("EXP-0001", "OPERADOR", inf2, T_ESPERA, aprobacion(p["pantalla"])) if p["ok"] else p
    e = o.expedientes["EXP-0001"]
    ver("p10_la_anulacion_de_veto_sigue_funcionando_tras_un_veto_anotado", r["ok"] and e["estado"] == "AUTORIZADA" and o.anulaciones_mes(T_ESPERA) == 1
        and o.integridad() == [] and len(vetos(o)) == 1,
        f"pantalla={p['codigo']} autorizar={r['codigo']} estado={e['estado']} anulaciones={o.anulaciones_mes(T_ESPERA)} vetos anotados={len(vetos(o))}")


def p11_idempotencia_y_varios_vetos():
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    inf = vetado(o)
    r1 = o.autorizar("EXP-0001", "OPERADOR", inf, AHORA)
    r2 = o.autorizar("EXP-0001", "OPERADOR", inf, AHORA)
    n1 = len(vetos(o))
    inf2 = vetado(o, n=2)
    o.autorizar("EXP-0001", "OPERADOR", inf2, AHORA)
    em = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    ver("p11_el_mismo_informe_no_se_anota_dos_veces", n1 == 1 and len(vetos(o)) == 2 and em["por_capa"].get("PROPUESTA") == 1 and not em["salidas"],
        f"r1={r1['codigo']} r2={r2['codigo']} ({r2.get('motivo')}); vetos tras el mismo informe={n1}, tras otro={len(vetos(o))}; por_capa={em['por_capa']}")


def p12_persistencia_y_diario_con_el_veto():
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    inf = vetado(o)
    o.autorizar("EXP-0001", "OPERADOR", inf, AHORA)
    t = pe.volcar(o, mas(AHORA, minutes=1))
    r = pe.cargar(t)
    c = r.get("orquestador")
    ok_pe = c is not None and c.integridad() == [] and c.expedientes == o.expedientes
    with tempfile.TemporaryDirectory() as d:
        o2 = antiguo()
        hasta(o2, "PROPUESTA", 1)
        inf2 = vetado(o2)   # registra la foto de G y la cotización antes de abrir el diario (por fuera daría DI-06)
        re_, rd = str(Path(d) / "e.json"), str(Path(d) / "d.log")
        D = di.crear(o2, re_, rd, AHORA)["diario"]
        ra = D.autorizar("EXP-0001", "OPERADOR", inf2, AHORA)
        h1 = copy.deepcopy(o2.expedientes["EXP-0001"]["historial"])
        r2 = di.abrir(re_, rd)
        o3 = r2.get("orquestador") or (r2.get("diario")._o if r2.get("diario") else None)
        ok_di = o3 is not None and o3.expedientes["EXP-0001"]["historial"] == h1 and o3.integridad() == [] and len(vetos(o3)) == 1
    ver("p12_persistencia_y_diario_reproducen_el_veto", ok_pe and ok_di and ra["codigo"] == "O-06",
        f"cargar={r.get('codigo')} igual={ok_pe}; diario autorizar={ra['codigo']} abrir={r2.get('codigo')} historial reproducido={ok_di}")


def p13_veto_con_hora_posterior_al_reloj():
    """La llamada rechazada no adelanta ultimo_ahora (@_seguro), pero ahora deja una anotación con su instante: una operación
    posterior con una hora anterior se admite y el historial queda desordenado en el tiempo."""
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    u0 = o.ultimo_ahora
    r = o.autorizar("EXP-0001", "OPERADOR", vetado(o), mas(AHORA, minutes=30))
    u1 = o.ultimo_ahora
    rb = o.descartar("EXP-0001", "el gestor lo descarta tras el veto", "GESTOR_TACTICA", mas(AHORA, minutes=10))
    hs = [h["ahora"] for h in o.expedientes["EXP-0001"]["historial"]]
    mono = all(datetime.fromisoformat(a) <= datetime.fromisoformat(b) for a, b in zip(hs, hs[1:]))
    ver("p13_la_anotacion_del_veto_no_queda_por_delante_del_reloj", r["codigo"] == "O-06" and (u1 != u0 or mono),
        f"autorizar={r['codigo']}; ultimo_ahora antes={u0} después={u1}; descartar a una hora anterior al veto={rb['codigo']}; "
        f"instantes del historial={hs[-3:]} monótonos={mono}")


def p14_testigos_y_salida_no_operador():
    """Un candidato vetado (en PROPUESTA) que su gestor descarta: ¿cambia _salida_no_operador o los testigos por la anotación?"""
    res = []
    for con_veto in (False, True):
        o = antiguo()
        hasta(o, "PROPUESTA", 1)
        if con_veto:
            o.autorizar("EXP-0001", "OPERADOR", vetado(o), AHORA)
        r = o.descartar("EXP-0001", "el gestor lo descarta tras el veto", "GESTOR_TACTICA", AHORA)
        x = o.expedientes["EXP-0001"]
        s = o._salida_no_operador(x)
        res.append((r["codigo"], s and (s["desde"], s["hasta"], s["actor"]), [t["expediente_id"] for t in o._testigos("TACTICA", datetime.fromisoformat(AHORA), set())]))
    ver("p14_el_veto_no_cambia_testigos_ni_salidas", res[0] == res[1], f"sin veto={res[0]}; con veto={res[1]}")


# ============================================================================== 3. H-03 / H-04: cuentas y periodo
def p15_revalidado_cuenta_una_vez():
    """Docstring de embudo(): «un análisis cuenta una vez: un DIRECTA que reutiliza el de otro no suma, y un expediente
    revalidado tampoco». La s03 de la r01 (observar, reabrir, encargar de nuevo y validar) da 2."""
    from pruebas_orquestador import encargo, sobre_para
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    assert o.observar("EXP-0001", [{"tipo": "PRECIO", "instrumento": "EURUSD", "operador": ">=", "umbral": 1.12}], "esperar condiciones", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.reabrir("EXP-0001", "cambió el contexto", "OPERADOR", AHORA)["ok"]
    enc = encargo(1); enc["event_id"] = "EV-ENC-0101"
    assert o.emitir_encargo("EXP-0001", enc, "GESTOR_TACTICA", AHORA)["ok"]
    s = sobre_para(1, None); s["event_id"] = "EV-SOB-0001-R"
    assert o.entregar_sobre("EXP-0001", s, AHORA)["ok"]
    em = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    ver("p15_un_expediente_revalidado_cuenta_como_dice_el_docstring", em["validadas"] == 1,
        f"validadas={em['validadas']} (dos sobres distintos para una oportunidad); salidas={len(em['salidas'])} salen={em['salen']}")


def p16_periodo_semiabierto():
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    t = AHORA
    a = o.embudo(mas(t, days=-7), t)
    b = o.embudo(t, mas(t, days=7))
    c = o.embudo(t, t)
    d = o.embudo(mas(t, microseconds=-1), t)
    ver("p16_periodo_desde_hasta_abierto_por_la_izquierda", a["entran"] == 1 and b["entran"] == 0 and c["entran"] == 0 and d["entran"] == 1
        and a["validadas"] + b["validadas"] == 1,
        f"(t-7d,t]: entran={a['entran']} validadas={a['validadas']}; (t,t+7d]: {b['entran']}/{b['validadas']}; (t,t]: {c['entran']}; (t-1µs,t]: {d['entran']}")


def p17_informe_y_texto_del_aviso():
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    hasta(o, "VALIDADA", 3)
    t = mas(AHORA, days=1)   # el sistema arrancó en T0 (más de 60 días antes) y nunca invirtió
    r = o.barrer(t)
    av = o40(o)
    inf = informe_embudo(o, t)
    malos = [d for d in (0, -1, True, False, 2.5, "7", None, float("nan")) if informe_embudo(o, AHORA, d)["ok"] is not False]
    ver("p17_aviso_con_candidatos_e_informe_robusto", len(av) == 1 and "2 candidato(s)" in av[0]["motivo"] and inf["ok"] and inf["sequia"]["activa"] and not malos
        and ("sequia", o.sequia(t)["desde"], 2) in r["cambios"],
        f"aviso={av[0]['motivo'] if av else None!r}; informe ok={inf['ok']}; días no rechazados={malos}")


def main():
    for f in (p01_barridos_a_cualquier_hora, p02_barridos_espaciados, p03_borde_exacto, p04_sin_inversiones_nunca_y_otras_carteras,
              p05_directa_E_tras_la_inversion, p06_veto_por_la_pantalla_del_operador, p07_veto_por_la_matriz, p08_propuesta_CT_G_06_tras_el_veto,
              p09_tras_el_veto_otro_informe_autoriza_ejecuta_y_cuadra, p10_anulacion_T50_tras_un_veto_anotado, p11_idempotencia_y_varios_vetos,
              p12_persistencia_y_diario_con_el_veto, p13_veto_con_hora_posterior_al_reloj, p14_testigos_y_salida_no_operador,
              p15_revalidado_cuenta_una_vez, p16_periodo_semiabierto, p17_informe_y_texto_del_aviso):
        try:
            f()
        except Exception as ex:   # noqa: BLE001
            import traceback
            print("ERROR   ", f.__name__, "::", type(ex).__name__, ex, traceback.format_exc().splitlines()[-3])
            hallazgos.append(f.__name__ + " (error de la sonda)")
    print(f"\n{len(oks)} OK, {len(hallazgos)} a revisar: {hallazgos}")


if __name__ == "__main__":
    main()
