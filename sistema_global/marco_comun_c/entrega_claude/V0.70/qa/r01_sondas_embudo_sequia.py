"""QA r01 de T-75 (V0.70): sondas del revisor contra embudo(), sequia(), la alarma O-40 de barrer() e informe_embudo().

Cada sonda imprime OBS (lo que se observa, para el informe) y HALLAZGO o OK. No cambia el código ni las pruebas.
Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.70/qa/r01_sondas_embudo_sequia.py
"""
import copy
import sys
from datetime import datetime, timedelta
from pathlib import Path

MARCO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
from consola import informe_embudo, panel  # noqa: E402
from orquestador import Orquestador  # noqa: E402
from pruebas_k import CAL  # noqa: E402
from pruebas_orquestador import (AHORA, CFG, S1, encargo, hasta, informe_ctr, obj_ctr, registrar_motor,  # noqa: E402
                                 sobre, sobre_para)

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


def lectura_pura(o, fn):
    antes = copy.deepcopy(o.__dict__)
    fn()
    return antes == o.__dict__


# ---------------------------------------------------------------------------------------------- 1. vía DIRECTA
def s01_directa_D_reutiliza():
    """Un único análisis (EV-SOB-0001) validado en EXP-0001, descartado por el operador y reutilizado dos veces por D."""
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    assert o.descartar("EXP-0001", "el operador lo aparta por ahora", "OPERADOR", AHORA)["ok"]
    r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
    assert r["ok"], r
    em1 = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    assert o.descartar("EXP-DD-01", "el operador aparta también este", "OPERADOR", AHORA)["ok"]
    r2 = o.abrir_directa("EXP-DD-02", "COR-DD-02", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
    em2 = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    sobres = {(x.get("sobre") or {}).get("event_id") for x in o.expedientes.values()} - {None}
    ver("s01_directa_D_un_analisis_cuenta_como_varias_validadas",
        em2["validadas"] == len(sobres),
        f"análisis distintos={len(sobres)}; validadas tras 1 reutilización={em1['validadas']}, tras 2ª ({r2['ok']})={em2['validadas']}; "
        f"entran={em2['entran']} por_capa={em2['por_capa']}")
    return o


def s02_directa_E():
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    assert o.descartar("EXP-0001", "el operador lo aparta por ahora", "OPERADOR", AHORA)["ok"]
    r = o.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "E", "BROKER", AHORA, analisis="EV-SOB-0001",
                        motivo="candidato único: no hay otro análisis vigente en la cartera")
    em = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    x = [z for z in em["oportunidades"] if z["expediente_id"] == "EXP-DE-01"]
    ver("s02_directa_E_nace_COMPARADA_y_su_capa_es_COMPARADA", r["ok"] and x and x[0]["capa"] == "COMPARADA",
        f"abrir={r['codigo']} capa={x[0]['capa'] if x else None} validadas={em['validadas']} (EXP-0001 y EXP-DE-01 con el mismo sobre)")


# ---------------------------------------------------------------------------------------------- 2. reaperturas y observación
def s03_observar_reabrir_revalidar():
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    precio = {"tipo": "PRECIO", "instrumento": "EURUSD", "operador": ">=", "umbral": 1.12}
    assert o.observar("EXP-0001", [precio], "esperar a que se den las condiciones", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.reabrir("EXP-0001", "cambió el contexto", "OPERADOR", AHORA)["ok"]
    enc = encargo(1); enc["event_id"] = "EV-ENC-0101"
    r = o.emitir_encargo("EXP-0001", enc, "GESTOR_TACTICA", AHORA)
    s = sobre_para(1, None); s["event_id"] = "EV-SOB-0001-R"
    r2 = o.entregar_sobre("EXP-0001", s, AHORA) if r["ok"] else r
    em = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    pasos = [(z["desde"], z["hasta"]) for z in o.expedientes["EXP-0001"]["historial"]]
    ver("s03_reabierto_y_revalidado_cuenta_dos_veces",
        em["validadas"] == 1,
        f"reencargo={r['codigo']} sobre={r2['codigo']} validadas={em['validadas']} para 1 oportunidad; salidas={len(em['salidas'])}; "
        f"historial={pasos}")


def s04_observacion_vencida_dos_salidas():
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    precio = {"tipo": "PRECIO", "instrumento": "EURUSD", "operador": ">=", "umbral": 9.0}
    assert o.observar("EXP-0001", [precio], "esperar a que se den las condiciones", "GESTOR_TACTICA", AHORA)["ok"]
    r = o.barrer(mas(AHORA, days=32))
    em = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, days=32))
    sal = [(z["expediente_id"], z["desde"], z["hasta"], z["actor"]) for z in em["salidas"]]
    ver("s04_una_oportunidad_que_sale_una_vez_cuenta_una_salida", len(sal) == 1,
        f"barrer={r['codigo']} salidas={sal}")


# ---------------------------------------------------------------------------------------------- 3. objeción crítica y bloqueados
def s05_objecion_critica():
    o = antiguo({"exige_contradictor_en": ["N3"]})
    assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
    crit = informe_ctr(sobre(1), veredicto="OBJECION_CRITICA", objeciones=[obj_ctr(1, "CRITICA", ["SRC-EURUSD"], "LOGICA")])
    r = o.entregar_sobre("EXP-0001", sobre(1), AHORA, informe=crit)
    em0 = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    r2 = o.levantar_objecion("EXP-0001", "asumo la objeción", "OPERADOR", mas(AHORA, minutes=2))
    em1 = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=3))
    cap = em0["oportunidades"][0]
    ver("s05_objecion_critica_retenida_no_cuenta_y_levantada_cuenta_una",
        r["codigo"] == "O-17" and em0["validadas"] == 0 and cap["capa"] == "EN_ANALISIS" and r2["ok"] and em1["validadas"] == 1,
        f"retenida: validadas={em0['validadas']} capa={cap['capa']} motivo={cap['motivo']!r}; levantada: validadas={em1['validadas']}")


def s06_bloqueado_O32():
    o = antiguo()
    assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
    s = sobre(1); s["payload"]["exclusiones_duras"]["sanciones"] = "BLOQUEADO"
    r = o.entregar_sobre("EXP-0001", s, AHORA)
    em = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    sq = o.sequia(mas(AHORA, minutes=1))
    ver("s06_bloqueado_sale_por_el_Orquestador_y_no_cuenta_como_validada",
        r["codigo"] == "O-32" and em["validadas"] == 0 and em["salidas"][0]["actor"] == "ORQUESTADOR" and not sq["activa"],
        f"sobre={r['codigo']} validadas={em['validadas']} salida={em['salidas'][0]['desde']}->{em['salidas'][0]['hasta']} por {em['salidas'][0]['actor']}; sequia={sq['activa']}")


# ---------------------------------------------------------------------------------------------- 4. caducidad y bordes
def s07_caducidad_y_bordes():
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    o.barrer("2026-11-10T00:00:00+00:00")   # el sobre de prueba vence el 9: caduca
    est = o.expedientes["EXP-0001"]["estado"]
    e_ex = o.embudo(AHORA, AHORA)   # periodo de un instante, justo el de la validación
    e_semana1 = o.embudo(mas(AHORA, days=-7), AHORA)
    e_semana2 = o.embudo(AHORA, mas(AHORA, days=7))
    dobles = e_semana1["entran"] + e_semana2["entran"]
    ver("s07_semanas_consecutivas_no_cuentan_dos_veces_lo_del_borde", dobles == 1,
        f"estado={est}; [t,t]: entran={e_ex['entran']} validadas={e_ex['validadas']}; semana [t-7,t] entran={e_semana1['entran']} "
        f"y [t,t+7] entran={e_semana2['entran']} (una sola oportunidad); validadas {e_semana1['validadas']}+{e_semana2['validadas']}")
    # borde exacto del plazo de sequía
    s60 = o.sequia(mas(AHORA, days=60))
    s60b = o.sequia((datetime.fromisoformat(AHORA) + timedelta(days=60, microseconds=1)).isoformat())
    ver("s07b_borde_exacto_del_plazo", s60["activa"] and not s60b["activa"],
        f"a los 60 días exactos activa={s60['activa']}; 1 µs después activa={s60b['activa']} ({s60b['motivo']})")


def s08_joven_en_el_borde():
    o = Orquestador(dict(CFG), CAL)
    assert o.registrar_sello(S1, AHORA)["ok"]
    registrar_motor(o, S1["sello_id"])
    hasta(o, "VALIDADA", 1)
    primero = o._primer_instante().isoformat()
    sj = o.sequia(mas(primero, days=60))
    sj2 = o.sequia(mas(primero, days=59, hours=23))
    ver("s08_sistema_de_60_dias_exactos_si_juzga_y_uno_mas_joven_no", sj["activa"] and not sj2["activa"],
        f"primer instante={primero}; a 60 d: {sj['activa']} ({sj['motivo']}); a 59 d 23 h: {sj2['activa']} ({sj2['motivo']})")


# ---------------------------------------------------------------------------------------------- 5. alarma: una por plazo, silenciar, forzar
def s09_alarma_cada_plazo_y_acuse():
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    t1 = mas(AHORA, hours=1)
    o.barrer(t1)
    n1 = len(o40(o))
    for d in range(1, 60):
        o.barrer(mas(t1, days=d))
    n2 = len(o40(o))
    ver("s09_una_sola_alarma_en_60_barridos_diarios", n1 == 1 and n2 == 1, f"tras el primero={n1}; tras 59 días más={n2}")


def s10_aviso_igual_sin_acusar_se_traga_y_cambios_miente():
    """Un O-40 de un plazo anterior sin acusar, con el mismo texto que el del plazo nuevo: _aviso() no lo añade (ya hay uno igual
    sin acusar) pero barrer() devuelve el cambio («sequia») en cada barrido. Se fabrica el O-40 anterior con el texto que daría
    el plazo nuevo para no depender de las fechas fijas de los datos de prueba."""
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    t = mas(AHORA, hours=1)
    sq = o.sequia(t)
    em = sq["embudo"]
    texto = (f"en {sq['dias']} días ninguna oportunidad se invirtió habiendo {sq['validadas']} que pasaron el análisis; "
             f"embudo del periodo: entran {em['entran']}, por capa {em['por_capa']}, salidas {len(em['salidas'])}")
    o._aviso("O-40", texto, mas(T0, minutes=1))   # el de hace un plazo, sin acusar
    n0 = len(o40(o))
    r1 = o.barrer(t)
    r2 = o.barrer(mas(t, hours=1))
    c1 = [c for c in r1["cambios"] if c[0] == "sequia"]
    c2 = [c for c in r2["cambios"] if c[0] == "sequia"]
    ver("s10_barrer_no_anuncia_una_alarma_que_no_dio", not (len(o40(o)) == n0 and (c1 or c2)),
        f"O-40 antes={n0} después={len(o40(o))}; cambios 'sequia' barrido1={c1} barrido2={c2}")


def s11_inversion_silencia_todas_las_carteras():
    """Una EJECUTADA en una cartera apaga la alarma de las demás (lectura literal de «ninguna oportunidad»)."""
    o = antiguo()
    hasta(o, "EJECUTADA", 1)   # TACTICA invierte
    sq = o.sequia(mas(AHORA, hours=1))
    por_cartera = {x["cartera"] for x in sq["embudo"]["oportunidades"]}
    ver("s11_observacion_el_embudo_no_separa_carteras", True,
        f"carteras en el embudo={sorted(por_cartera)}; claves={sorted(sq['embudo'])}; activa={sq['activa']}")


# ---------------------------------------------------------------------------------------------- 6. robustez y solo lectura
def s12_entradas_raras():
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    raros = [None, 0, 1.5, float("nan"), "ayer", "2026-11-06T09:00:00", "2026-13-01T00:00:00+00:00", datetime(2026, 11, 6),
             "0001-01-01T00:00:00+00:00", "9999-12-31T23:59:59+00:00", "2026-11-06T09:00:00Z", b"2026", [], {}]
    malos = []
    for x in raros:
        for nombre, fn in (("sequia", lambda x=x: o.sequia(x)), ("embudo_d", lambda x=x: o.embudo(x, AHORA)),
                           ("embudo_h", lambda x=x: o.embudo(AHORA, x)), ("informe", lambda x=x: informe_embudo(o, x))):
            try:
                r = fn()
                if nombre == "sequia" and r["activa"] and x not in ("9999-12-31T23:59:59+00:00", "2026-11-06T09:00:00Z"):   # dos instantes legibles
                    malos.append((nombre, repr(x), "activa"))
            except Exception as ex:   # noqa: BLE001
                malos.append((nombre, repr(x), type(ex).__name__))
    for d in (0, -1, float("nan"), float("inf"), "60", None, True, 10 ** 12, 1.5):
        for nombre, fn in (("sequia_dias", lambda d=d: o.sequia(mas(AHORA, hours=1), d)),
                           ("informe_dias", lambda d=d: informe_embudo(o, mas(AHORA, hours=1), d))):
            try:
                fn()
            except Exception as ex:   # noqa: BLE001
                malos.append((nombre, repr(d), type(ex).__name__))
    zf = o.sequia("2026-11-06T10:00:00Z")
    ver("s12_nada_lanza_ni_dispara_con_entradas_raras", not malos,
        f"fallos={malos}; con 'Z' activa={zf['activa']}; informe dias=True -> {informe_embudo(o, mas(AHORA, hours=1), True).get('dias')!r}; "
        f"informe dias=0 -> ok={informe_embudo(o, mas(AHORA, hours=1), 0)['ok']}")


def s13_solo_leen():
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    ok = all(lectura_pura(o, f) for f in (lambda: o.sequia(mas(AHORA, days=1)), lambda: o.embudo(T0, mas(AHORA, days=1)),
                                          lambda: informe_embudo(o, mas(AHORA, days=1)), lambda: o.sequia("x"),
                                          lambda: informe_embudo(o, mas(AHORA, days=1), -3)))
    ver("s13_embudo_sequia_e_informe_no_mueven_nada_ni_el_reloj", ok, f"ultimo_ahora={o.ultimo_ahora}")


def s14_panel_no_cambia():
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    p0 = panel(o, mas(AHORA, hours=1))
    o.barrer(mas(AHORA, hours=1))
    p1 = panel(o, mas(AHORA, hours=1))
    qs = [c["que"] for c in p1["comprobaciones"]]
    av = [c for c in p1["comprobaciones"] if c["que"] == "avisos"]
    ver("s14_el_panel_no_gana_comprobaciones_y_la_sequia_llega_por_su_aviso", [c["que"] for c in p0["comprobaciones"]] == qs,
        f"comprobaciones={qs}; avisos antes={[c for c in p0['comprobaciones'] if c['que']=='avisos']} después={av}")


def s15_determinismo_y_persistencia():
    import persistencia as pe
    def flujo():
        o = antiguo()
        hasta(o, "VALIDADA", 1)
        o.barrer(mas(AHORA, hours=1))
        return o
    a, b = flujo(), flujo()
    ta = pe.volcar(a, mas(AHORA, hours=1)); tb = pe.volcar(b, mas(AHORA, hours=1))
    r = pe.cargar(ta)
    c = r.get("orquestador")
    sa = a.sequia(mas(AHORA, hours=2)); sc = c.sequia(mas(AHORA, hours=2)) if c else None
    c.barrer(mas(AHORA, hours=2)) if c else None
    ver("s15_mismo_flujo_mismo_estado_y_cargado_no_repite_la_alarma", ta == tb and c is not None and sa == sc and len(o40(c)) == 1,
        f"volcados iguales={ta == tb}; cargar={r.get('codigo')}; sequia igual={sa == sc}; O-40 tras barrer cargado={len(o40(c)) if c else None}")


def s16_diario_reproduce():
    import tempfile
    import diario as di
    with tempfile.TemporaryDirectory() as d:
        o = antiguo()
        hasta(o, "VALIDADA", 1)
        re, rd = str(Path(d) / "e.json"), str(Path(d) / "d.log")
        r = di.crear(o, re, rd, AHORA)
        D = r.get("diario")
        rb = D.barrer(mas(AHORA, hours=1)) if D else None
        inf = informe_embudo(D, mas(AHORA, hours=1)) if D else None
        r2 = di.abrir(re, rd)
        o2 = r2.get("orquestador") or (r2.get("diario")._o if r2.get("diario") else None)
        ver("s16_el_diario_reproduce_la_alarma_e_informe_por_el_diario", rb and rb["ok"] and o2 is not None and len(o40(o2)) == 1
            and inf["ok"], f"crear={r.get('codigo')} barrer={rb and rb['codigo']} abrir={r2.get('codigo')} "
            f"O-40 reproducidos={len(o40(o2)) if o2 else None}; informe por el diario ok={inf and inf['ok']}")


def s17_veto_de_F_no_aparece_en_el_embudo():
    """F veta la propuesta (F-09) y el operador no anula: el expediente sigue en PROPUESTA y acaba CADUCADA por el reloj. ¿Dice el
    embudo que la capa que lo paró fue F?"""
    from pruebas_operador_t50 import vetado
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    inf = vetado(o)
    r = o.autorizar("EXP-0001", "OPERADOR", inf, AHORA)
    em = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    x = [z for z in em["oportunidades"] if z["expediente_id"] == "EXP-0001"][0]
    o.barrer("2026-11-09T00:00:00+00:00")   # la ventana de entrada de la propuesta (8-11 12:00) ya pasó
    em2 = o.embudo(mas(AHORA, minutes=-1), "2026-11-09T00:00:00+00:00")
    sal = [(z["desde"], z["hasta"], z["actor"], z["motivo"]) for z in em2["salidas"] if z["expediente_id"] == "EXP-0001"]
    texto = repr(em) + repr(em2)
    ver("s17_el_embudo_dice_que_F_vetó", "F-09" in texto or "vet" in texto.lower(),
        f"autorizar={r['codigo']} ({r['motivo']}); capa tras el veto={x['capa']} actor={x['actor']} motivo={x['motivo']!r}; "
        f"salida final={sal}")


def s18_tope_del_reloj():
    import reloj as rl
    res = {}
    for c in (rl.TOPE_SIN_CONTRASTE_S, rl.TOPE_SIN_CONTRASTE_S + 1e-6, True, "604800", float("nan"), -1, 0):
        try:
            r = rl.Reloj(lambda: 1.8e9, lambda: 1.0, max_sin_contraste_s=c)
            res[repr(c)] = r.max_sin_contraste_s
        except ValueError:
            res[repr(c)] = "rechazado"
    ok = (res[repr(rl.TOPE_SIN_CONTRASTE_S)] == rl.TOPE_SIN_CONTRASTE_S and res[repr(rl.TOPE_SIN_CONTRASTE_S + 1e-6)] == "rechazado"
          and res[repr(float("nan"))] == "rechazado" and res["-1"] == "rechazado" and res["0"] == "rechazado")
    ver("s18_el_tope_del_contraste_es_cerrado_y_sin_huecos", ok and rl.MAX_SIN_CONTRASTE_S <= rl.TOPE_SIN_CONTRASTE_S, res)


def s19_barridos_diarios_pierden_la_sequia():
    """Inversión a las 09:00 y un candidato validado a las 10:00; después nada se invierte. Del 10:00 del día 0 al 10:00 del día
    60 hay un plazo de 60 días sin inversiones con un candidato que pasó el análisis. La ventana deslizante solo lo ve entre las
    09:00 y las 10:00 del día 60: un barrido diario a las 08:00 nunca lo ve."""
    def caso(hora_barrido):
        o = antiguo()
        hasta(o, "EJECUTADA", 1)   # EXP-0001 se invierte a las 09:00 (EXP-0002 es su rival de la comparación)
        t1 = mas(AHORA, hours=1)
        hasta(o, "VALIDADA", 5, ahora=t1)   # un candidato nuevo a las 10:00
        dia0 = datetime.fromisoformat(AHORA).replace(hour=hora_barrido)
        for d in range(1, 91):
            o.barrer((dia0 + timedelta(days=d)).isoformat())
        return len(o40(o)), o.expedientes["EXP-0005"]["estado"]
    n8, est = caso(8)
    n9 = None
    o = antiguo()
    hasta(o, "EJECUTADA", 1)
    hasta(o, "VALIDADA", 5, ahora=mas(AHORA, hours=1))
    sq = o.sequia(mas(AHORA, days=60, minutes=30))
    ver("s19_con_barridos_diarios_la_sequia_se_ve", n8 >= 1,
        f"barridos diarios a las 08:00 durante 90 días: O-40={n8} (EXP-0005 {est}); la sequía solo se ve entre las 09:00 y las 10:00 "
        f"del día 60: sequia(día 60, 09:30) activa={sq['activa']}")


def main():
    for f in (s19_barridos_diarios_pierden_la_sequia, s17_veto_de_F_no_aparece_en_el_embudo, s18_tope_del_reloj,s01_directa_D_reutiliza, s02_directa_E, s03_observar_reabrir_revalidar, s04_observacion_vencida_dos_salidas,
              s05_objecion_critica, s06_bloqueado_O32, s07_caducidad_y_bordes, s08_joven_en_el_borde, s09_alarma_cada_plazo_y_acuse,
              s10_aviso_igual_sin_acusar_se_traga_y_cambios_miente, s11_inversion_silencia_todas_las_carteras, s12_entradas_raras,
              s13_solo_leen, s14_panel_no_cambia, s15_determinismo_y_persistencia, s16_diario_reproduce):
        try:
            f()
        except Exception as ex:   # noqa: BLE001
            print("ERROR   ", f.__name__, "::", type(ex).__name__, ex)
            hallazgos.append(f.__name__ + " (error de la sonda)")
    print(f"\n{len(oks)} OK, {len(hallazgos)} a revisar: {hallazgos}")


if __name__ == "__main__":
    main()
