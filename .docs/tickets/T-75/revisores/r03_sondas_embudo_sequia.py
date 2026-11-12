"""QA r03 de T-75 (V0.75): sondas del revisor contra las correcciones de H-09..H-14 y las regresiones que pueden abrir.

Cada sonda imprime OK o HALLAZGO con lo observado. No cambia el código ni las pruebas. Datos SIMULADOS.
Uso (desde la raíz del repositorio):
    .venv/bin/python -I .docs/tickets/T-75/revisores/r03_sondas_embudo_sequia.py [ruta del marco]
Por defecto, el marco es sistema_global/marco_comun_c del mismo árbol.
"""
import copy
import inspect
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
MARCO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else RAIZ / "sistema_global" / "marco_comun_c"
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
from pruebas_orquestador import AHORA, CFG, S1, autorizar_op, encargo, hasta, nuevo, registrar_motor, sobre_para  # noqa: E402

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


def fila(em, eid="EXP-0001"):
    return next((x for x in em["oportunidades"] if x["expediente_id"] == eid), None)


def vetos(o, eid="EXP-0001"):
    return [h for h in o.expedientes[eid]["historial"] if h["desde"] == h["hasta"] == "PROPUESTA" and h["actor"] == "F"]


def horas(o, eid="EXP-0001"):
    return [x["ahora"] for x in o.expedientes[eid]["historial"]]


def ordenado(hs):
    return hs == sorted(hs, key=datetime.fromisoformat)


# ============================================================================== 1. H-09 a H-14, otra vez
def q01_H09_veto_por_la_pantalla():
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    inf = vetado(o)
    cola = [x.get("accion") for x in cola_aprobaciones(o, AHORA) if x.get("expediente_id") == "EXP-0001"]
    r = o.pantalla_aprobacion("EXP-0001", inf, AHORA)
    f = fila(o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1)))
    r2 = o.pantalla_aprobacion("EXP-0001", inf, mas(AHORA, minutes=1))   # el mismo informe otra vez: no se anota dos veces
    r3 = o.autorizar("EXP-0001", "OPERADOR", inf, mas(AHORA, minutes=2))
    o.barrer(mas(AHORA, days=3))
    sal = [x for x in o.embudo(mas(AHORA, minutes=-1), mas(AHORA, days=3))["salidas"] if x["expediente_id"] == "EXP-0001"]
    ok = (r["codigo"] == "O-06" and "reloj_firme" not in r and f and f["actor"] == "F" and "F-09" in (f["bloqueo"] or "")
          and r2["codigo"] == "O-03" and r3["codigo"] == "O-03" and len(vetos(o)) == 1 and sal and sal[-1]["hasta"] == "CADUCADA"
          and "F-09" in (sal[-1]["bloqueo_previo"] or "") and o.integridad() == [])
    ver("q01_H09_el_veto_visto_en_la_pantalla_queda_anotado_una_vez", ok,
        f"cola={cola}; pantalla={r['codigo']} claves={sorted(r)}; fila={f and (f['capa'], f['actor'], f['bloqueo'])}; "
        f"2ª pantalla={r2['codigo']}; autorizar={r3['codigo']}; vetos={len(vetos(o))}; salida={sal and (sal[-1]['hasta'], sal[-1]['bloqueo_previo'])}")


def q02_H10_propuesta_igual_tras_vetos():
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    p0 = ct.propuesta(o, "EXP-0001")
    r1 = o.pantalla_aprobacion("EXP-0001", vetado(o), mas(AHORA, minutes=1))
    p1 = ct.propuesta(o, "EXP-0001")
    r2 = o.autorizar("EXP-0001", "OPERADOR", vetado(o, n=2), mas(AHORA, minutes=3))   # otro informe que veta
    p2 = ct.propuesta(o, "EXP-0001")
    ok = (r1["codigo"] == "O-06" and r2["codigo"] == "O-06" and len(vetos(o)) == 2 and p0 == p1 == p2 and ct.validar(p2) == []
          and p2["producer"] == "GESTOR_TACTICA")
    ver("q02_H10_la_CT_G_06_es_la_misma_y_valida_tras_uno_o_dos_vetos", ok,
        f"pantalla={r1['codigo']} autorizar={r2['codigo']} ({r2['motivo'][:60]}); vetos={len(vetos(o))}; iguales={p0 == p1 == p2}; "
        f"producer={p2['producer']}; validar={ct.validar(p2)}")


def q03_H11_reloj_firme_tras_el_veto():
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    r = o.pantalla_aprobacion("EXP-0001", vetado(o), mas(AHORA, minutes=30))
    u = o.ultimo_ahora
    rd = o.descartar("EXP-0001", "antes del veto", "GESTOR_TACTICA", mas(AHORA, minutes=10))
    rb = o.barrer(mas(AHORA, minutes=20))
    # un rechazo que NO anota sigue sin adelantar el reloj (la corrección no debe extenderse a otros rechazos)
    rx = o.autorizar("EXP-0001", "OPERADOR", {}, mas(AHORA, minutes=50))   # sin informe de F: O-01
    u2 = o.ultimo_ahora
    rok = o.descartar("EXP-0001", "tras el veto y antes del rechazo", "GESTOR_TACTICA", mas(AHORA, minutes=40))
    ok = (r["codigo"] == "O-06" and u == mas(AHORA, minutes=30) and rd["codigo"] == "O-16" and rb["codigo"] == "O-16"
          and rx["codigo"] == "O-01" and u2 == u and rok["ok"] and ordenado(horas(o)))
    ver("q03_H11_tras_el_veto_de_la_pantalla_nada_anterior_entra_y_otros_rechazos_no_adelantan_el_reloj", ok,
        f"pantalla={r['codigo']} reloj={u}; descartar 09:10={rd['codigo']}; barrer 09:20={rb['codigo']}; rechazo O-01 a 09:50 deja el reloj en "
        f"{u2}; descartar 09:40={rok['codigo']}; historial ordenado={ordenado(horas(o))}")


def q04_H14_borde_de_la_edad_por_barrer():
    o = nuevo()
    hasta(o, "VALIDADA", 1)
    primero = o._primer_instante().isoformat()
    s1, s2 = o.sequia(mas(primero, days=60, microseconds=-1)), o.sequia(mas(primero, days=60))
    o.barrer(mas(primero, days=60, microseconds=-1))
    n1 = len(o40(o))
    o.barrer(mas(primero, days=60))
    n2 = len(o40(o))
    ver("q04_H14_sin_inversiones_la_edad_es_exacta_tambien_en_barrer", not s1["activa"] and s2["activa"] and n1 == 0 and n2 == 1,
        f"60d-1µs: {s1['activa']} ({s1['motivo']}), O-40={n1}; 60d: {s2['activa']}, O-40={n2}; desde={s2['desde']}")


def q05_H13_revalidado_y_docstring():
    from orquestador import Orquestador as Oq
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    assert o.observar("EXP-0001", [{"tipo": "PRECIO", "instrumento": "EURUSD", "operador": ">=", "umbral": 1.12}], "esperar", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.reabrir("EXP-0001", "cambió el contexto", "OPERADOR", AHORA)["ok"]
    enc = encargo(1); enc["event_id"] = "EV-ENC-0101"
    assert o.emitir_encargo("EXP-0001", enc, "GESTOR_TACTICA", AHORA)["ok"]
    s = sobre_para(1, None); s["event_id"] = "EV-SOB-0001-R"
    assert o.entregar_sobre("EXP-0001", s, AHORA)["ok"]
    em = o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
    doc = inspect.getdoc(Oq.embudo) or ""
    ver("q05_H13_un_revalidado_con_otro_sobre_suma_y_el_docstring_lo_dice", em["validadas"] == 2 and "revalidado con otro sobre sí suma" in doc,
        f"validadas={em['validadas']}; docstring lo dice={'revalidado con otro sobre sí suma' in doc}")


# ============================================================================== 2. ataques nuevos
def n01_veto_rancio_tras_un_reanalisis_anterior_al_periodo():
    """Veto, observación, reapertura y nuevo análisis ANTES del periodo; dentro del periodo, el operador lo descarta. El veto ya no
    es la causa (el embudo la borra con un análisis nuevo), pero el reinicio solo se hace con anotaciones dentro del periodo."""
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    assert o.pantalla_aprobacion("EXP-0001", vetado(o), AHORA)["codigo"] == "O-06"
    t1, t2, t3 = mas(AHORA, minutes=1), mas(AHORA, minutes=2), mas(AHORA, minutes=3)
    assert o.observar("EXP-0001", [{"tipo": "PRECIO", "instrumento": "EURUSD", "operador": ">=", "umbral": 1.12}], "esperar", "GESTOR_TACTICA", t1)["ok"]
    assert o.reabrir("EXP-0001", "cambió el contexto", "OPERADOR", t2)["ok"]
    enc = encargo(1); enc["event_id"] = "EV-ENC-0101"
    assert o.emitir_encargo("EXP-0001", enc, "GESTOR_TACTICA", t2)["ok"]
    s = sobre_para(1, None); s["event_id"] = "EV-SOB-0001-R"
    assert o.entregar_sobre("EXP-0001", s, t3)["ok"]
    t4 = mas(AHORA, minutes=10)
    assert o.descartar("EXP-0001", "el operador lo descarta tras el nuevo análisis", "OPERADOR", t4)["ok"]
    largo = [x for x in o.embudo(mas(AHORA, minutes=-1), t4)["salidas"] if x["hasta"] == "DESCARTADA"]
    corto = [x for x in o.embudo(mas(AHORA, minutes=5), t4)["salidas"] if x["hasta"] == "DESCARTADA"]
    bl, bc = largo[-1]["bloqueo_previo"], corto[-1]["bloqueo_previo"]
    ver("n01_la_causa_previa_de_una_salida_no_depende_de_donde_empiece_el_periodo", bl == bc,
        f"periodo que incluye el reanálisis: bloqueo_previo={bl!r}; periodo que empieza después del reanálisis: bloqueo_previo={bc!r}")


def n02_persistencia_y_diario_del_veto_por_la_pantalla():
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    o.pantalla_aprobacion("EXP-0001", vetado(o), mas(AHORA, minutes=30))
    c = pe.cargar(pe.volcar(o, mas(AHORA, minutes=30))).get("orquestador")
    rc = c.descartar("EXP-0001", "antes del veto", "GESTOR_TACTICA", mas(AHORA, minutes=10)) if c else {"codigo": None}
    ok_pe = c is not None and c.ultimo_ahora == o.ultimo_ahora and rc["codigo"] == "O-16" and len(vetos(c)) == 1
    with tempfile.TemporaryDirectory() as d:
        o2 = antiguo()
        hasta(o2, "PROPUESTA", 1)
        inf2 = vetado(o2)
        re_, rd = str(Path(d) / "e.json"), str(Path(d) / "d.log")
        D = di.crear(o2, re_, rd, AHORA)["diario"]
        rp = D.pantalla_aprobacion("EXP-0001", inf2, mas(AHORA, minutes=30))
        rr = D.descartar("EXP-0001", "antes del veto", "GESTOR_TACTICA", mas(AHORA, minutes=10))
        h1, u1 = copy.deepcopy(o2.expedientes["EXP-0001"]["historial"]), o2.ultimo_ahora
        r2 = di.abrir(re_, rd)
        o3 = r2["diario"].orquestador if r2.get("diario") is not None else r2.get("orquestador")
        ok_di = (r2.get("ok") and o3 is not None and o3.expedientes["EXP-0001"]["historial"] == h1 and o3.ultimo_ahora == u1
                 and rp["codigo"] == "O-06" and "reloj_firme" not in rp and rr["codigo"] == "O-16")
    ver("n02_guardar_cargar_y_el_diario_conservan_el_veto_de_la_pantalla_y_el_reloj", ok_pe and ok_di,
        f"cargado: reloj igual={c and c.ultimo_ahora == o.ultimo_ahora}, descartar anterior={rc['codigo']}; diario: pantalla={rp['codigo']} "
        f"descartar anterior={rr['codigo']} abrir={r2.get('codigo')} historial y reloj reproducidos={ok_di}")


def n03_anulacion_fallida_no_anota_ni_consume():
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    inf = vetado(o)
    u0 = o.ultimo_ahora
    r = o.pantalla_aprobacion("EXP-0001", inf, mas(AHORA, minutes=1), anular_veto={"motivo": ""})   # sin motivo: se rechaza
    ok1 = not r["ok"] and len(vetos(o)) == 0 and inf["event_id"] not in o.eventos and o.ultimo_ahora == u0
    r2 = o.pantalla_aprobacion("EXP-0001", inf, mas(AHORA, minutes=2))   # después, la pantalla normal sí lo anota
    ver("n03_una_anulacion_rechazada_no_anota_ni_consume_y_la_pantalla_luego_si", ok1 and r2["codigo"] == "O-06" and len(vetos(o)) == 1,
        f"anulación sin motivo={r['codigo']} ({r['motivo'][:50]}); vetos={len(vetos(o))}; reloj intacto={o.ultimo_ahora}; pantalla después={r2['codigo']}")


def n04_estado_manipulado_del_veto():
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    o.pantalla_aprobacion("EXP-0001", vetado(o), AHORA)
    res = {}
    for campo, valor in (("motivo", "vetado por F: F-99"), ("actor", "OPERADOR"), ("ahora", "2026-11-06T08:00:00+00:00"), ("motivo", None)):
        c = copy.deepcopy(o)
        next(h for h in reversed(c.expedientes["EXP-0001"]["historial"]) if h["desde"] == h["hasta"] == "PROPUESTA")[campo] = valor
        em = c.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=1))
        res[f"{campo}={valor!r}"[:30]] = ("EXP:EXP-0001" in c.integridad(), em is not None)
    ver("n04_tocar_la_anotacion_del_veto_lo_detecta_integridad_y_el_embudo_no_lanza", all(a for a, _ in res.values()),
        f"(detectado, embudo no lanza)={res}")


def n05_veto_y_anulacion_despues_en_el_embudo():
    """Tras un veto anotado, el operador lo anula con otro informe y se invierte: la fila dice EJECUTADA y conserva el veto como
    bloqueo (es información, no un error); la sequía se apaga."""
    from pruebas_operador_t50 import anular
    o = antiguo()
    hasta(o, "PROPUESTA", 1)
    o.pantalla_aprobacion("EXP-0001", vetado(o), AHORA)
    ra = anular(o, vetado(o, n=2), t1=mas(AHORA, minutes=1), t2=mas(AHORA, minutes=32))
    f = fila(o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=40)))
    ver("n05_veto_anotado_y_anulado_despues_autoriza", ra["ok"] and f["capa"] == "AUTORIZADA" and len(vetos(o)) == 1 and o.integridad() == [],
        f"anulación={ra['codigo']} ({ra['motivo'][:50]}); fila={(f['capa'], f['actor'], f['bloqueo'])}")


def n06_entradas_raras_en_sequia_e_informe():
    o = antiguo()
    hasta(o, "VALIDADA", 1)
    fallos = []
    for dias in (10 ** 9, 2 ** 63, -0, 1):
        try:
            s = o.sequia(mas(AHORA, days=61), dias=dias)
            if dias >= 10 ** 9 and s["activa"]:
                fallos.append((dias, "activa"))
        except Exception as ex:   # noqa: BLE001
            fallos.append((dias, type(ex).__name__))
    for dias in (10 ** 9, 2 ** 63):
        try:
            r = informe_embudo(o, mas(AHORA, days=61), dias)
            if r.get("ok") is not False and r.get("embudo") is None:
                fallos.append(("informe", dias, r))
        except Exception as ex:   # noqa: BLE001
            fallos.append(("informe", dias, type(ex).__name__))
    antes = copy.deepcopy(o.__dict__)
    informe_embudo(o, mas(AHORA, days=61))
    o.sequia(mas(AHORA, days=61))
    ver("n06_plazos_enormes_no_lanzan_ni_disparan_y_todo_solo_lee", not fallos and antes == o.__dict__, f"fallos={fallos}")


def n07_veto_por_la_matriz_y_por_el_operador_en_el_mismo_expediente():
    """Dos vetos (dos informes) por dos rutas: dos anotaciones, la última es la causa; la CT-G-06 no cambia y el historial va en orden."""
    o = antiguo({"matriz_autonomia": {"TACTICA": True}})
    hasta(o, "PROPUESTA", 1)
    p0 = ct.propuesta(o, "EXP-0001")
    r1 = o.pantalla_aprobacion("EXP-0001", vetado(o), AHORA)
    r2 = o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", vetado(o, n=2), mas(AHORA, minutes=5))
    f = fila(o.embudo(mas(AHORA, minutes=-1), mas(AHORA, minutes=6)))
    ok = (r1["codigo"] == "O-06" and ct.propuesta(o, "EXP-0001") == p0 and ordenado(horas(o)) and o.integridad() == []
          and (r2["codigo"] != "O-06" or len(vetos(o)) == 2))
    ver("n07_dos_vetos_por_dos_rutas", ok, f"pantalla={r1['codigo']} matriz={r2['codigo']} ({r2['motivo'][:50]}); vetos={len(vetos(o))}; "
        f"fila={(f['capa'], f['actor'], f['bloqueo'])}")


def n08_documentacion():
    t89 = next((ln for ln in (RAIZ / "sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md").read_text(encoding="utf-8").splitlines()
                if ln.startswith("| T-89 |")), "")
    ver("n08_la_fila_T_89_de_la_deuda_dice_el_estado_actual_de_T_75", "DETENIDO" not in t89,
        f"fila T-89: «…{t89[-150:]}»")


def main():
    for f in (q01_H09_veto_por_la_pantalla, q02_H10_propuesta_igual_tras_vetos, q03_H11_reloj_firme_tras_el_veto, q04_H14_borde_de_la_edad_por_barrer,
              q05_H13_revalidado_y_docstring, n01_veto_rancio_tras_un_reanalisis_anterior_al_periodo,
              n02_persistencia_y_diario_del_veto_por_la_pantalla, n03_anulacion_fallida_no_anota_ni_consume, n04_estado_manipulado_del_veto,
              n05_veto_y_anulacion_despues_en_el_embudo, n06_entradas_raras_en_sequia_e_informe,
              n07_veto_por_la_matriz_y_por_el_operador_en_el_mismo_expediente, n08_documentacion):
        try:
            f()
        except Exception as ex:   # noqa: BLE001
            ver(f.__name__, False, f"la sonda lanzó {type(ex).__name__}: {str(ex)[:200]}")
    print(f"\n{len(oks)} OK, {len(hallazgos)} HALLAZGO: {hallazgos}")


if __name__ == "__main__":
    main()
