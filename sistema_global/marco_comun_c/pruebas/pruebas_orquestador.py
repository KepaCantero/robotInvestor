"""Pruebas del Orquestador V0.1 (máquina de estados). Datos SIMULADOS.
Cada rechazo debe dar el código esperado y dejar el estado intacto (salvo los hechos que se
registran a propósito: avisos y estado de encargos caducados/anulados).

Uso: python3 pruebas/pruebas_orquestador.py
"""
import copy
import sys
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from orquestador import Orquestador  # noqa: E402
from pruebas_encargo import encargo_div, SELLOS as SELLOS_ENC  # noqa: E402
from pruebas_k import CAL, CTX as CTX_K, construir as construir_k  # noqa: E402
from generar_casos import validos as sobres_validos  # noqa: E402
from pruebas_contradictor import informe as informe_ctr, obj as obj_ctr  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402

CFG = {"perfiles_activos": ["C-DIV", "C-RV", "C-CRI"], "apalancamiento_permitido": False,
       "clases_ratificadas": {"C-DIV": "Q", "C-RV": "Q", "C-CRI": "K", "C-RF": "S"},
       "nivel_autonomia": {"TRADING": "L2", "TACTICA": "L2", "LARGO_PLAZO": "L2"}}   # las pruebas de mecánica usan L2; los niveles tienen su propio bloque
AHORA = "2026-11-06T09:00:00+00:00"
A2 = "2026-11-08T13:00:00+00:00"
S1 = SELLOS_ENC["K-20261105-001"]
S2 = SELLOS_ENC["K-20261106-001"]
STOP = {"id": "STOP-1", "tipo": "STOP", "metrica": "precio", "operador": "<=", "umbral": 1.05, "unidad": "USD"}
OBJ = {"id": "OBJ-1", "tipo": "OBJETIVO", "metrica": "precio", "operador": ">=", "umbral": 1.14, "unidad": "USD"}
INV = {"id": "INV-1", "tipo": "INVALIDEZ", "metrica": "precio_cierre", "operador": "<", "umbral": 1.05, "unidad": "EUR"}   # la del sobre
ENTRADA = {"limite": 1.10, "ventana_hasta": "2026-11-08T12:00:00+00:00", "instrumento": "EURUSD", "activo_base": "EUR",
           "apalancamiento": 1.0, "cantidad": 100.0}
SALIDA = {"condiciones": [STOP, OBJ, INV], "fecha": "2026-12-05"}
CART_E = {"fecha_hora": "2026-11-06T08:50:00+00:00", "capital_eur": 100000.0, "perdida_dia_eur": 0.0, "posiciones": [],
          "tipos_cambio_eur": {"USD": 1.0}}


def dim(o, eid="EXP-0001", entrada=None, salida=None, cartera=None, ahora=AHORA, paso=1.0):
    """El cálculo de E que acompaña a una propuesta (las mismas entradas que el Orquestador repite)."""
    ent, sal = entrada or ENTRADA, salida or SALIDA
    st = [c for c in sal["condiciones"] if c.get("tipo") == "STOP"][0]
    sol = {"instrumento": ent["instrumento"], "activo_base": ent["activo_base"], "divisa_cotizacion": o.divisa(ent["instrumento"]), "direccion": "LARGO" if st["operador"] in ("<", "<=") else "CORTO",
           "precio_entrada": ent["limite"], "stop_precio": st["umbral"], "apalancamiento": ent["apalancamiento"],
           "cartera": o.expedientes[eid]["cartera_destino"] if eid in o.expedientes else "TACTICA"}
    from pruebas_control_f import registrar_foto
    cart = registrar_foto(o, copy.deepcopy(cartera or CART_E))
    return {"solicitud": sol, "cartera": cart, "riesgo_objetivo_pct": None, "paso": paso, "ahora": ahora}


def autorizar_op(o, eid, informe, ahora=AHORA, importe=None, canal="CONSOLA", segundo_factor=True):
    """Lo que hace el operador: pide la pantalla con las cifras de F y la aprueba tecleando el importe."""
    p = o.pantalla_aprobacion(eid, informe, ahora)
    if not p["ok"]:
        return p
    pa = p["pantalla"]
    return o.autorizar(eid, "OPERADOR", informe, ahora, {"pantalla_hash": pa["hash"], "importe_tecleado": pa["importe"] if importe is None else importe,
                                                         "canal": canal, "segundo_factor": segundo_factor})


def anotar_entrada(o, eid, oid, cantidad, ahora=AHORA):
    """Lo que G hace antes de reportar una ejecución: anotar la orden de entrada enviada y ejecutada."""
    assert o.orden_entrada(eid, oid, "ENVIADA", 0.0, "G", ahora)["ok"]
    r = o.orden_entrada(eid, oid, "EJECUTADA", cantidad, "G", ahora)
    assert r["ok"], r


def elegir_si_hace_falta(o, eid, ahora=AHORA):
    c = o.expedientes[eid].get("comparacion") or {}
    if not c.get("ganador"):
        r = o.elegir(eid, "OPERADOR", "elección de prueba", ahora)
        assert r["ok"], r


def nuevo(cfg=None, sellos=(S1,)):
    o = Orquestador({**CFG, **(cfg or {})}, CAL)
    for s in sellos:
        assert o.registrar_sello(s, AHORA)["ok"], "sello base"
    return o


def encargo(n=1, corte="2026-11-05", sello="K-20261105-001", producer="GESTOR_TACTICA"):
    e = encargo_div()
    e["event_id"] = f"EV-ENC-{n:04d}"; e["correlation_id"] = f"COR-{n:04d}"; e["expediente_id"] = f"EXP-{n:04d}"
    e["producer"] = producer
    e["payload"]["fecha_corte"] = corte; e["payload"]["sello_corte_ref"] = sello
    e["data_refs"] = [f"PAQ-B-{n:04d}", sello]; e["payload"]["candidato"]["paquete_b_ref"] = f"PAQ-B-{n:04d}"
    if corte == "2026-11-06":
        e["emitido_en"] = "2026-11-06T08:30:00+00:00"; e["valid_until"] = "2026-11-09T12:00:00+00:00"
        e["payload"]["presupuesto"]["entrega_antes_de"] = "2026-11-06T20:00:00+00:00"
    return e


def sobre(n=1, corte="2026-11-05", sello="K-20261105-001"):
    s = copy.deepcopy(sobres_validos()["valido_div_n3.json"])
    s["event_id"] = f"EV-SOB-{n:04d}"; s["correlation_id"] = f"COR-{n:04d}"; s["expediente_id"] = f"EXP-{n:04d}"
    s["payload"]["identificacion"]["fecha_corte"] = corte
    s["data_refs"] = [sello, "SRC-EURUSD", f"EVID-{n:04d}"]
    if corte == "2026-11-06":
        s["emitido_en"] = "2026-11-06T10:00:00+00:00"; s["valid_until"] = "2026-11-09T18:00:00+00:00"
    return s


def sobre_para(n, salida):
    """Un sobre coherente con unas condiciones de salida dadas (dirección, stop, objetivo e invalidez)."""
    s = sobre(n)
    if salida is None:
        return s
    p = s["payload"]
    st = [c for c in salida["condiciones"] if c.get("tipo") == "STOP"][0]
    p["identificacion"]["direccion"] = "LARGO" if st["operador"] in ("<", "<=") else "CORTO"
    p["entrada_salida"]["stop"]["valor"] = st["umbral"]
    objs = [c for c in salida["condiciones"] if c.get("tipo") == "OBJETIVO"]
    if objs:
        p["entrada_salida"]["objetivo"]["valor"] = objs[0]["umbral"]
    invs = [c for c in salida["condiciones"] if c.get("tipo") == "INVALIDEZ"]
    if invs:
        p["tesis"]["condiciones_invalidez"] = [{"id": c["id"], "descripcion": "invalidez de prueba", "metrica": c["metrica"], "operador": c["operador"],
                                               "umbral": c["umbral"], "unidad": c["unidad"]} for c in invs]
    return s


def hasta(o, estado, n=1, ahora=AHORA, entrada=None, salida=None, cartera_e=None):
    """Lleva el expediente EXP-000n hasta `estado` por el camino feliz (sin cambiar el reloj)."""
    if estado == "DESDE_CERO":
        return
    assert o.detectar(f"EXP-{n:04d}", f"COR-{n:04d}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", ahora)["ok"]
    if estado == "DETECTADA":
        return
    assert o.emitir_encargo(f"EXP-{n:04d}", encargo(n), "GESTOR_TACTICA", ahora)["ok"]
    if estado == "EN_ANALISIS":
        return
    r = o.entregar_sobre(f"EXP-{n:04d}", sobre_para(n, salida), ahora)
    assert r["ok"], r
    if estado == "VALIDADA":
        return
    # la comparación necesita dos candidatos de la misma cartera con el mismo corte
    assert o.detectar(f"EXP-{n + 1:04d}", f"COR-{n + 1:04d}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", ahora)["ok"]
    assert o.emitir_encargo(f"EXP-{n + 1:04d}", encargo(n + 1), "GESTOR_TACTICA", ahora)["ok"]
    assert o.entregar_sobre(f"EXP-{n + 1:04d}", sobre(n + 1), ahora)["ok"]
    for k, x in list(o.expedientes.items()):   # los perdedores de comparaciones anteriores se descartan antes de comparar de nuevo
        if k not in (f"EXP-{n:04d}", f"EXP-{n + 1:04d}") and x["estado"] in ("VALIDADA", "COMPARADA"):
            assert o.descartar(k, "descartado antes de la comparación siguiente", "GESTOR_TACTICA", ahora)["ok"]
    r = o.comparar([f"EXP-{n:04d}", f"EXP-{n + 1:04d}"], "D", ahora)
    assert r["ok"], r
    if estado == "COMPARADA":
        return
    elegir_si_hace_falta(o, f"EXP-{n:04d}", ahora)
    r = o.proponer(f"EXP-{n:04d}", entrada or ENTRADA, salida or SALIDA, "GESTOR_TACTICA", ahora, dim(o, f"EXP-{n:04d}", entrada, salida, cartera=cartera_e, ahora=ahora))
    assert r["ok"], r
    if estado == "PROPUESTA":
        return
    assert autorizar_op(o, f"EXP-{n:04d}", informe_f(o, f"EXP-{n:04d}", n), ahora)["ok"]
    if estado == "AUTORIZADA":
        return
    anotar_entrada(o, f"EXP-{n:04d}", "ORD-1", 100.0, ahora)
    r = o.ejecutar(f"EXP-{n:04d}", {"orden_id": "ORD-1", "cantidad": 100.0, "precio": 1.1, "conciliada": True,
                                    "proteccion_orden_ids": ["ORD-1-STOP"]}, "G", ahora)
    assert r["ok"], r


class Arnes:
    def __init__(self):
        self.ok = True
        self.n = 0

    def chk(self, nombre, cond, detalle=""):
        self.n += 1
        print(("OK   " if cond else "FALLA"), nombre, "" if cond else detalle)
        self.ok &= bool(cond)

    def rechaza(self, nombre, o, fn, codigo, mutacion_permitida=False, ok_esperado=False):
        antes = copy.deepcopy({k: v for k, v in o.__dict__.items() if k not in ("avisos", "ultimo_ahora")})
        r = fn()
        despues = {k: v for k, v in o.__dict__.items() if k not in ("avisos", "ultimo_ahora")}
        bien = r["codigo"] == codigo and r["ok"] is ok_esperado and (mutacion_permitida or antes == despues)
        self.chk(nombre, bien, f"esperado={codigo} ok={ok_esperado} obtenido={r['codigo']} ok={r['ok']} {r['motivo']!r} "
                 f"{'(estado cambió)' if antes != despues else ''}")
        return r


def main():
    h = Arnes()
    R = h.rechaza
    # ---------------------------------------------------------------- camino feliz
    o = nuevo()
    hasta(o, "EJECUTADA")
    e = o.expedientes["EXP-0001"]
    h.chk("feliz_expediente_ejecutado", e["estado"] == "EJECUTADA" and e["posicion_id"] == "POS-EXP-0001")
    h.chk("feliz_posicion_abierta_con_protecciones", o.posiciones["POS-EXP-0001"]["estado"] == "ABIERTA" and o.posiciones["POS-EXP-0001"]["protecciones"])
    h.chk("feliz_historial_completo", [x["hasta"] for x in e["historial"]] ==
          ["DETECTADA", "EN_ANALISIS", "VALIDADA", "COMPARADA", "PROPUESTA", "AUTORIZADA", "AUTORIZADA", "AUTORIZADA", "EJECUTADA"])   # orden ENVIADA y EJECUTADA
    h.chk("feliz_historial_integro", o._historial_ok(e))
    R("terminal_ejecutada_no_se_mueve", o, lambda: o.descartar("EXP-0001", "x", "BROKER", AHORA), "O-14")

    # ---------------------------------------------------------------- sellos
    o = Orquestador(CFG, CAL)
    R("sello_alterado_O01", o, lambda: o.registrar_sello({**S1, "version_ajustes": "AJ-9"}, AHORA), "O-01")
    R("sello_anulado_O01", o, lambda: o.registrar_sello({**S1, "estado": "ANULADO"}, AHORA), "O-01")
    o0 = Orquestador(CFG, CAL)
    R("sello_del_futuro_O01", o0, lambda: o0.registrar_sello(S1, "2026-11-05T01:00:00+00:00"), "O-01")
    R("sello_no_objeto_O01", o, lambda: o.registrar_sello([], AHORA), "O-01")
    R("sello_reemplaza_desconocido_O12", o, lambda: o.registrar_sello(
        construir_k(ctx={**CTX_K, "secuencia": 2, "reemplaza_a": "K-20261104-001"})[1]["sello"], AHORA), "O-12")
    h.chk("sello_registro_ok", o.registrar_sello(S1, AHORA)["ok"])
    R("sello_duplicado_O02", o, lambda: o.registrar_sello(S1, AHORA), "O-02", ok_esperado=True)
    otro = construir_k(mut=lambda e: e["ajustes"].update(version="AJ-OTRO"))[1]["sello"]
    R("sello_mismo_id_otro_contenido_O03", o, lambda: o.registrar_sello(otro, AHORA), "O-03")
    R("ahora_mal_formado_O00_y_estado_intacto", o, lambda: o.registrar_sello(S1, "ayer"), "O-00")

    # ---------------------------------------------------------------- detectar
    o = nuevo()
    R("detectar_actor_C_O05", o, lambda: o.detectar("EXP-1", "COR-1", "DISCRECIONAL", "TACTICA", "C", AHORA), "O-05")
    R("detectar_gestor_ajeno_O05", o, lambda: o.detectar("EXP-1", "COR-1", "DISCRECIONAL", "TRADING", "GESTOR_TACTICA", AHORA), "O-05")
    R("detectar_id_con_espacio_O01", o, lambda: o.detectar("EXP 1", "COR-1", "DISCRECIONAL", "TACTICA", "BROKER", AHORA), "O-01")
    R("detectar_via_mala_O01", o, lambda: o.detectar("EXP-1", "COR-1", "OTRA", "TACTICA", "BROKER", AHORA), "O-01")
    hasta(o, "DETECTADA")
    R("detectar_duplicado_O03", o, lambda: o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA), "O-03")

    # ---------------------------------------------------------------- emitir encargo
    R("encargo_expediente_inexistente_O12", o, lambda: o.emitir_encargo("EXP-9999", encargo(1), "BROKER", AHORA), "O-12")
    R("encargo_actor_C_O05", o, lambda: o.emitir_encargo("EXP-0001", encargo(1), "C", AHORA), "O-05")
    R("encargo_emisor_distinto_O05", o, lambda: o.emitir_encargo("EXP-0001", encargo(1, producer="GESTOR_TRADING"), "GESTOR_TACTICA", AHORA), "O-05")
    R("encargo_de_otro_expediente_O12", o, lambda: o.emitir_encargo("EXP-0001", encargo(2), "GESTOR_TACTICA", AHORA), "O-12")
    R("encargo_no_objeto_O01", o, lambda: o.emitir_encargo("EXP-0001", [], "BROKER", AHORA), "O-01")
    malo = encargo(1); malo["payload"]["nivel_analisis"] = "N0"
    r = R("encargo_invalido_O01", o, lambda: o.emitir_encargo("EXP-0001", malo, "GESTOR_TACTICA", AHORA), "O-01")
    h.chk("encargo_invalido_cita_E09", "E-09" in r.get("reglas", []), r.get("reglas"))
    otra_cartera = encargo(1); otra_cartera["payload"]["cartera_destino"] = "LARGO_PLAZO"; otra_cartera["producer"] = "BROKER"
    R("encargo_de_otra_cartera_O12", o, lambda: o.emitir_encargo("EXP-0001", otra_cartera, "BROKER", AHORA), "O-12")
    sin = Orquestador(CFG, CAL); sin.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    R("encargo_sin_ningun_sello_O06", sin, lambda: sin.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA), "O-06")
    assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
    R("encargo_duplicado_O02", o, lambda: o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA), "O-02", ok_esperado=True)
    cambiado = encargo(1); cambiado["payload"]["pregunta"] = "otra pregunta distinta"
    R("encargo_mismo_event_id_otro_contenido_O03", o, lambda: o.emitir_encargo("EXP-0001", cambiado, "GESTOR_TACTICA", AHORA), "O-03", mutacion_permitida=True)
    h.chk("conflicto_O03_deja_aviso", any(a["codigo"] == "O-03" for a in o.avisos))
    segundo = encargo(1); segundo["event_id"] = "EV-ENC-0099"
    R("encargo_con_otro_en_curso_O06", o, lambda: o.emitir_encargo("EXP-0001", segundo, "GESTOR_TACTICA", AHORA), "O-06")

    # ---------------------------------------------------------------- presupuestos y bucles
    o = nuevo({"dia_coste_max_eur": 4.0})
    hasta(o, "DETECTADA")
    R("presupuesto_diario_insuficiente_O08", o, lambda: o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA), "O-08")
    o = nuevo()
    hasta(o, "EN_ANALISIS")
    R("gasto_inexistente_O12", o, lambda: o.registrar_gasto("EV-X", 1, 1, AHORA), "O-12")
    R("gasto_negativo_O01", o, lambda: o.registrar_gasto("EV-ENC-0001", -1, 1, AHORA), "O-01")
    R("gasto_nan_O01", o, lambda: o.registrar_gasto("EV-ENC-0001", float("nan"), 1, AHORA), "O-01")
    r = o.registrar_gasto("EV-ENC-0001", 1.0, 5, AHORA)
    h.chk("gasto_dentro_del_presupuesto", r["ok"] and r["alertas"] == [] and o.encargos["EV-ENC-0001"]["estado"] == "EN_CURSO")
    r = o.registrar_gasto("EV-ENC-0001", 10.0, 5, AHORA)
    h.chk("gasto_excede_encargo_O07", r["ok"] and r["alertas"] == ["O-07"] and o.encargos["EV-ENC-0001"]["estado"] == "INCOMPLETO")
    R("encargo_incompleto_no_se_valida_O07", o, lambda: o.entregar_sobre("EXP-0001", sobre(1), AHORA), "O-07")
    c0 = o.encargos["EV-ENC-0001"]["coste"]
    r = o.registrar_gasto("EV-ENC-0001", 1, 1, AHORA)
    h.chk("gasto_sobre_encargo_cerrado_se_registra", r["ok"] and o.encargos["EV-ENC-0001"]["coste"] == c0 + 1 and o.encargos["EV-ENC-0001"]["estado"] == "INCOMPLETO", r)
    o = nuevo({"max_reintentos": 1})
    hasta(o, "EN_ANALISIS")
    o.registrar_gasto("EV-ENC-0001", 99.0, 1, AHORA)
    reint = encargo(1); reint["event_id"] = "EV-ENC-0010"
    R("bucle_O09", o, lambda: o.emitir_encargo("EXP-0001", reint, "GESTOR_TACTICA", AHORA), "O-09")
    h.chk("bucle_deja_aviso", any(a["codigo"] == "O-09" for a in o.avisos))
    o = nuevo()
    hasta(o, "EN_ANALISIS")
    o.registrar_gasto("EV-ENC-0001", 99.0, 1, AHORA)   # incompleto, y el día queda agotado
    h.chk("dia_agotado_deja_aviso", any(a["codigo"] == "O-08" for a in o.avisos))
    reint = encargo(1); reint["event_id"] = "EV-ENC-0010"
    R("dia_agotado_bloquea_encargos_nuevos_O08", o, lambda: o.emitir_encargo("EXP-0001", reint, "GESTOR_TACTICA", AHORA), "O-08")
    o = nuevo({"dia_coste_max_eur": 1000.0})
    hasta(o, "EN_ANALISIS")
    o.registrar_gasto("EV-ENC-0001", 99.0, 1, AHORA)
    reint = encargo(1); reint["event_id"] = "EV-ENC-0010"
    r = o.emitir_encargo("EXP-0001", reint, "GESTOR_TACTICA", AHORA)
    h.chk("reintento_tras_incompleto_ok", r["ok"] and o.expedientes["EXP-0001"]["sin_avance"] == 2, r)

    # ---------------------------------------------------------------- entregar sobre
    o = nuevo()
    hasta(o, "DETECTADA")
    R("sobre_sin_encargo_O04", o, lambda: o.entregar_sobre("EXP-0001", sobre(1), AHORA), "O-04")
    o = nuevo(); hasta(o, "EN_ANALISIS")
    R("sobre_no_objeto_O01", o, lambda: o.entregar_sobre("EXP-0001", [], AHORA), "O-01")
    malo = sobre(1); malo["payload"]["identificacion"]["nivel_analisis"] = "N2"
    r = R("sobre_que_no_responde_O01", o, lambda: o.entregar_sobre("EXP-0001", malo, AHORA), "O-01")
    sin_src = sobre(1); sin_src["data_refs"] = ["K-20261105-001", "EVID-0001"]
    r = R("sobre_sin_fuentes_R12_O01", o, lambda: o.entregar_sobre("EXP-0001", sin_src, AHORA), "O-01")
    h.chk("sobre_sin_fuentes_cita_R12", "R-12" in r.get("reglas", []), r.get("reglas"))
    R("sobre_con_encargo_caducado_O10", o, lambda: o.entregar_sobre("EXP-0001", sobre(1), "2026-11-09T09:00:00+00:00"), "O-10", mutacion_permitida=True)
    R("sobre_tras_caducar_el_encargo_sigue_O10", o, lambda: o.entregar_sobre("EXP-0001", sobre(1), "2026-11-09T10:00:00+00:00"), "O-10")
    h.chk("encargo_pasa_a_CADUCADO", o.encargos["EV-ENC-0001"]["estado"] == "CADUCADO")
    o = nuevo(); hasta(o, "EN_ANALISIS")
    assert o.entregar_sobre("EXP-0001", sobre(1), AHORA)["ok"]
    R("sobre_identico_reenviado_es_duplicado_O02", o, lambda: o.entregar_sobre("EXP-0001", sobre(1), AHORA), "O-02", ok_esperado=True)
    otro = sobre(1); otro["event_id"] = "EV-SOB-0099"
    R("sobre_en_expediente_ya_validado_O04", o, lambda: o.entregar_sobre("EXP-0001", otro, AHORA), "O-04")
    o = nuevo({"exige_contradictor_en": ["N3"]})
    o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)
    R("sobre_N3_sin_contradictor_O06", o, lambda: o.entregar_sobre("EXP-0001", sobre(1), AHORA), "O-06")
    R("sobre_N3_informe_invalido_O01", o, lambda: o.entregar_sobre("EXP-0001", sobre(1), AHORA, informe={"event_id": "EV-CTR-0001"}), "O-01")
    inf = informe_ctr(sobre(1))
    h.chk("sobre_N3_con_contradictor_ok", o.entregar_sobre("EXP-0001", sobre(1), AHORA, informe=inf)["ok"]
          and o.expedientes["EXP-0001"]["contradictor"]["veredicto"] == "SIN_OBJECIONES_RELEVANTES")
    # informe reutilizado en otro expediente
    o.detectar("EXP-0002", "COR-0002", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    o.emitir_encargo("EXP-0002", encargo(2), "GESTOR_TACTICA", AHORA)
    R("informe_reutilizado_en_otro_expediente_O03", o, lambda: o.entregar_sobre("EXP-0002", sobre(2), AHORA, informe=inf), "O-03")
    # objeción mayor: pasa con aviso; crítica: retiene hasta que el operador la levante
    o = nuevo({"exige_contradictor_en": ["N3"]}); hasta_enc = o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA); o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)
    mayor = informe_ctr(sobre(1), veredicto="OBJECION_MAYOR", objeciones=[obj_ctr(1, "MAYOR", ["EVID-0001"])])
    h.chk("objecion_mayor_pasa_con_aviso", o.entregar_sobre("EXP-0001", sobre(1), AHORA, informe=mayor)["ok"] and any(a["codigo"] == "O-17" for a in o.avisos))
    o = nuevo({"exige_contradictor_en": ["N3"]}); o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA); o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)
    crit = informe_ctr(sobre(1), veredicto="OBJECION_CRITICA", objeciones=[obj_ctr(1, "CRITICA", ["SRC-EURUSD"], "LOGICA")])
    R("objecion_critica_retiene_O17", o, lambda: o.entregar_sobre("EXP-0001", sobre(1), AHORA, informe=crit), "O-17", mutacion_permitida=True)
    h.chk("critica_deja_expediente_en_analisis", o.expedientes["EXP-0001"]["estado"] == "EN_ANALISIS" and o.expedientes["EXP-0001"]["sobre"] is None)
    R("critica_reenvio_sigue_rechazado_O17", o, lambda: o.entregar_sobre("EXP-0001", sobre(1), AHORA, informe=crit), "O-17")
    R("critica_no_se_esquiva_con_observar_O17", o, lambda: o.observar("EXP-0001", ["x"], "m", "BROKER", AHORA), "O-17")
    R("critica_no_se_esquiva_con_reencargo_O17", o, lambda: o.emitir_encargo("EXP-0001", {**encargo(1), "event_id": "EV-ENC-0101"}, "GESTOR_TACTICA", AHORA), "O-17")
    R("levantar_critica_actor_ajeno_O05", o, lambda: o.levantar_objecion("EXP-0001", "ok", "C", AHORA), "O-05")
    R("levantar_critica_sin_motivo_O15", o, lambda: o.levantar_objecion("EXP-0001", " ", "OPERADOR", AHORA), "O-15")
    R("levantar_sin_critica_pendiente_O04", o, lambda: o.levantar_objecion("EXP-0099", "ok", "OPERADOR", AHORA), "O-12")
    h.chk("levantar_critica_ok", o.levantar_objecion("EXP-0001", "he revisado la objeción y la asumo", "OPERADOR", AHORA)["ok"]
          and o.expedientes["EXP-0001"]["estado"] == "VALIDADA" and o.expedientes["EXP-0001"]["contradictor"]["veredicto"] == "OBJECION_CRITICA")
    R("levantar_dos_veces_O04", o, lambda: o.levantar_objecion("EXP-0001", "otra vez", "OPERADOR", AHORA), "O-04")
    o = nuevo({"exige_contradictor_en": ["N3"]}); o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA); o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)
    o.entregar_sobre("EXP-0001", sobre(1), AHORA, informe=crit)
    R("levantar_con_sobre_vencido_O10", o, lambda: o.levantar_objecion("EXP-0001", "ok", "OPERADOR", "2026-11-09T00:00:00+00:00"), "O-10")
    # informe caducado antes que el sobre: el sobre vale solo mientras valga el informe
    o = nuevo({"exige_contradictor_en": ["N3"]}); o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA); o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)
    o.entregar_sobre("EXP-0001", sobre(1), AHORA, informe=informe_ctr(sobre(1)))
    r = o.barrer("2026-11-08T12:30:00+00:00")
    h.chk("informe_vencido_caduca_el_expediente", o.expedientes["EXP-0001"]["estado"] == "CADUCADA", r)
    for nombre, cfg in (("minuscula", ["n3"]), ("nivel_inexistente", ["N4"]), ("no_texto", [None]), ("anidada", [["N3"]])):
        try:
            Orquestador({**CFG, "exige_contradictor_en": cfg}, CAL)
            h.chk("config_contradictor_invalida_" + nombre, False, "arrancó")
        except ValueError:
            h.chk("config_contradictor_invalida_" + nombre, True)
    h.chk("critica_se_puede_descartar", o.descartar("EXP-0001", "la objeción es válida", "OPERADOR", "2026-11-09T00:00:00+00:00")["ok"])
    # duplicado y conflicto de sobre
    o = nuevo(); hasta(o, "EN_ANALISIS")
    s = sobre(1)
    o.eventos[s["event_id"]] = {"hash": "otro-hash", "expediente_id": "EXP-0001"}
    R("sobre_mismo_event_id_otro_contenido_O03", o, lambda: o.entregar_sobre("EXP-0001", s, AHORA), "O-03", mutacion_permitida=True)
    o = nuevo(); hasta(o, "EN_ANALISIS")
    o.eventos[s["event_id"]] = {"hash": __import__("orquestador")._hash(s), "expediente_id": "EXP-0001"}
    R("sobre_duplicado_O02", o, lambda: o.entregar_sobre("EXP-0001", s, AHORA), "O-02", ok_esperado=True)

    # ---------------------------------------------------------------- anulación del sello
    o = nuevo(); hasta(o, "EN_ANALISIS")
    nuevo_sello = construir_k(ctx={**CTX_K, "secuencia": 2, "reemplaza_a": "K-20261105-001"})[1]["sello"]
    h.chk("sello_de_reemplazo_registra", o.registrar_sello(nuevo_sello, AHORA)["ok"])
    h.chk("sello_anterior_anulado", o.sellos["K-20261105-001"]["estado"] == "ANULADO")
    h.chk("encargo_del_sello_anulado_pasa_a_ANULADO", o.encargos["EV-ENC-0001"]["estado"] == "ANULADO")
    R("entrega_sobre_encargo_anulado_O06", o, lambda: o.entregar_sobre("EXP-0001", sobre(1), AHORA), "O-06")
    r = o.emitir_encargo("EXP-0001", {**encargo(1, sello="K-20261105-002"), "event_id": "EV-ENC-0020"}, "GESTOR_TACTICA", AHORA)
    h.chk("reintento_con_el_sello_nuevo_ok", r["ok"], r)

    # ---------------------------------------------------------------- comparar
    o = nuevo(); hasta(o, "VALIDADA")
    o.detectar("EXP-0002", "COR-0002", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    o.emitir_encargo("EXP-0002", encargo(2), "GESTOR_TACTICA", AHORA)
    o.entregar_sobre("EXP-0002", sobre(2), AHORA)
    R("comparar_dejando_fuera_un_candidato_O24", o, lambda: o.comparar(["EXP-0001"], "D", AHORA), "O-24")
    R("comparar_lista_vacia_O01", o, lambda: o.comparar([], "D", AHORA), "O-01")
    R("comparar_actor_Broker_O05", o, lambda: o.comparar(["EXP-0001", "EXP-0002"], "BROKER", AHORA), "O-05")
    R("comparar_repetidos_O01", o, lambda: o.comparar(["EXP-0001", "EXP-0001"], "D", AHORA), "O-01")
    R("comparar_inexistente_O12", o, lambda: o.comparar(["EXP-0001", "EXP-0077"], "D", AHORA), "O-12")
    R("comparar_con_sobre_caducado_O10", o, lambda: o.comparar(["EXP-0001", "EXP-0002"], "D", "2026-11-09T09:00:00+00:00"), "O-10")
    # corte distinto
    o = nuevo(sellos=(S1,)); hasta(o, "VALIDADA")
    assert o.registrar_sello(S2, AHORA)["ok"]
    o.detectar("EXP-0002", "COR-0002", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    r = o.emitir_encargo("EXP-0002", encargo(2, corte="2026-11-06", sello="K-20261106-001"), "GESTOR_TACTICA", AHORA)
    assert r["ok"], r
    r = o.entregar_sobre("EXP-0002", sobre(2, corte="2026-11-06", sello="K-20261106-001"), "2026-11-06T10:30:00+00:00")
    assert r["ok"], r
    r = R("comparar_cortes_distintos_O11", o, lambda: o.comparar(["EXP-0001", "EXP-0002"], "D", "2026-11-06T10:30:00+00:00"), "O-11")
    h.chk("O11_indica_que_datos_actualizar", r.get("actualizar") == ["EXP-0001"], r.get("actualizar"))
    o.cfg["umbral_corte_comun_dias_habiles"] = 1
    h.chk("comparar_con_umbral_configurado_ok", o.comparar(["EXP-0001", "EXP-0002"], "D", "2026-11-06T10:30:00+00:00")["ok"])

    # ---------------------------------------------------------------- proponer / autorizar / ejecutar
    o = nuevo(); hasta(o, "COMPARADA")
    R("proponer_actor_C_O05", o, lambda: o.proponer("EXP-0001", ENTRADA, SALIDA, "C", AHORA), "O-05")
    R("proponer_sin_stop_O01", o, lambda: o.proponer("EXP-0001", ENTRADA, {"condiciones": [OBJ]}, "BROKER", AHORA), "O-01")
    R("proponer_condicion_cualitativa_O01", o, lambda: o.proponer("EXP-0001", ENTRADA, {"condiciones": [STOP, {"id": "X", "metrica": "m", "operador": "<", "umbral": "bajo"}]}, "BROKER", AHORA), "O-01")
    R("proponer_ids_repetidos_O01", o, lambda: o.proponer("EXP-0001", ENTRADA, {"condiciones": [STOP, STOP]}, "BROKER", AHORA), "O-01")
    R("proponer_ventana_vencida_O10", o, lambda: o.proponer("EXP-0001", {**ENTRADA, "ventana_hasta": "2026-11-06T08:00:00+00:00"}, SALIDA, "BROKER", AHORA), "O-10")
    R("proponer_limite_no_numerico_O01", o, lambda: o.proponer("EXP-0001", {**ENTRADA, "limite": "alto"}, SALIDA, "BROKER", AHORA), "O-01")
    o = nuevo(); hasta(o, "PROPUESTA")
    F = informe_f(o)
    R("autorizar_actor_G_O05", o, lambda: o.autorizar("EXP-0001", "G", F, AHORA), "O-05")
    R("autorizar_matriz_sin_permiso_O05", o, lambda: o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", F, AHORA), "O-05")
    R("autorizar_sin_control_F_O01", o, lambda: autorizar_op(o, "EXP-0001", None, AHORA), "O-01")
    R("autorizar_vetado_por_F_O06", o, lambda: autorizar_op(o, "EXP-0001", informe_f(o, n=2, cartera={"perdida_dia_eur": 5000.0}), AHORA), "O-06", mutacion_permitida=True)
    R("autorizar_propuesta_caducada_O10", o, lambda: autorizar_op(o, "EXP-0001", F, "2026-11-08T13:00:00+00:00"), "O-10")
    o = nuevo({"matriz_autonomia": {"TACTICA": True}}); hasta(o, "PROPUESTA")
    h.chk("autorizar_matriz_con_permiso_ok", o.autorizar("EXP-0001", "MATRIZ_AUTONOMIA", F, AHORA)["ok"])
    o = nuevo(); hasta(o, "AUTORIZADA")
    ORD = {"orden_id": "ORD-1", "cantidad": 100.0, "precio": 1.1, "conciliada": True, "proteccion_orden_ids": ["ORD-1-STOP"]}
    R("ejecutar_actor_Broker_O05", o, lambda: o.ejecutar("EXP-0001", ORD, "BROKER", AHORA), "O-05")
    R("ejecutar_sin_conciliar_O06", o, lambda: o.ejecutar("EXP-0001", {**ORD, "conciliada": False}, "G", AHORA), "O-06")
    R("ejecutar_conciliada_como_texto_O06", o, lambda: o.ejecutar("EXP-0001", {**ORD, "conciliada": "true"}, "G", AHORA), "O-06")
    R("ejecutar_sin_proteccion_O06", o, lambda: o.ejecutar("EXP-0001", {**ORD, "proteccion_orden_ids": []}, "G", AHORA), "O-06")
    R("ejecutar_cantidad_cero_O06", o, lambda: o.ejecutar("EXP-0001", {**ORD, "cantidad": 0}, "G", AHORA), "O-06")
    R("ejecutar_ventana_vencida_O10", o, lambda: o.ejecutar("EXP-0001", ORD, "G", "2026-11-08T13:00:00+00:00"), "O-10")
    R("transicion_saltada_O04", o, lambda: o.proponer("EXP-0001", ENTRADA, SALIDA, "BROKER", A2), "O-04")

    # ---------------------------------------------------------------- observación, descarte, caducidad
    o = nuevo(); hasta(o, "VALIDADA")
    R("observar_sin_condiciones_O15", o, lambda: o.observar("EXP-0001", [], "esperar", "BROKER", AHORA), "O-15")
    R("observar_sin_motivo_O15", o, lambda: o.observar("EXP-0001", ["EURUSD > 1.12"], " ", "BROKER", AHORA), "O-15")
    R("observar_actor_C_O05", o, lambda: o.observar("EXP-0001", ["EURUSD > 1.12"], "esperar", "C", AHORA), "O-05")
    h.chk("observar_ok", o.observar("EXP-0001", ["EURUSD > 1.12"], "esperar un nivel", "BROKER", AHORA)["ok"] and o.expedientes["EXP-0001"]["estado"] == "EN_OBSERVACION")
    R("descartar_sin_motivo_O15", o, lambda: o.descartar("EXP-0001", "", "BROKER", AHORA), "O-15")
    R("descartar_actor_D_O05", o, lambda: o.descartar("EXP-0001", "no", "D", AHORA), "O-05")
    h.chk("descartar_ok", o.descartar("EXP-0001", "ya no interesa", "OPERADOR", AHORA)["ok"])
    R("descartada_es_terminal_O14", o, lambda: o.observar("EXP-0001", ["x"], "y", "BROKER", AHORA), "O-14")
    o = nuevo(); hasta(o, "PROPUESTA")
    r = o.barrer("2026-11-08T13:00:00+00:00")
    h.chk("barrer_caduca_propuesta_vencida", ("expediente", "EXP-0001", "CADUCADA") in [tuple(c) for c in r["cambios"]] and o.expedientes["EXP-0001"]["estado"] == "CADUCADA", r)
    R("caducada_no_se_ejecuta_O04", o, lambda: o.ejecutar("EXP-0001", ORD, "G", A2), "O-04")
    h.chk("caducada_se_puede_descartar", o.descartar("EXP-0001", "venció", "BROKER", A2)["ok"])
    o = nuevo(); hasta(o, "EN_ANALISIS")
    r = o.barrer("2026-11-06T21:00:00+00:00")
    h.chk("barrer_avisa_encargo_sin_entrega", o.encargos["EV-ENC-0001"]["estado"] == "EN_CURSO" and any(a["codigo"] == "O-10" for a in o.avisos), r)
    r = o.barrer("2026-11-09T13:00:00+00:00")
    h.chk("barrer_caduca_encargo_tras_valid_until", o.encargos["EV-ENC-0001"]["estado"] == "CADUCADO", r)
    o = nuevo(); hasta(o, "VALIDADA")

    # ---------------------------------------------------------------- integridad del historial
    o = nuevo(); hasta(o, "EN_ANALISIS")
    o.expedientes["EXP-0001"]["historial"][0]["motivo"] = "manipulado"
    R("historial_alterado_O13", o, lambda: o.entregar_sobre("EXP-0001", sobre(1), AHORA), "O-13", mutacion_permitida=True)
    h.chk("un_incidente_de_integridad_activa_el_kill", o.kill is not None and o.kill["actor"] == "ORQUESTADOR" and "integridad" in o.kill["motivo"])
    o = nuevo(); hasta(o, "EN_ANALISIS")
    del o.expedientes["EXP-0001"]["historial"][0]
    R("historial_truncado_O13", o, lambda: o.descartar("EXP-0001", "x", "BROKER", AHORA), "O-13", mutacion_permitida=True)

    # ---------------------------------------------------------------- posiciones
    o = nuevo(); hasta(o, "EJECUTADA")
    P = "POS-EXP-0001"
    R("posicion_inexistente_O12", o, lambda: o.posicion_transicion("POS-X", "EN_REVISION", "H", AHORA), "O-12")
    R("posicion_transicion_inexistente_O04", o, lambda: o.posicion_transicion(P, "CERRADA", "G", AHORA), "O-04")
    R("posicion_H_no_vende_O05", o, lambda: o.posicion_transicion(P, "CERRANDO", "H", AHORA, condicion={"id": "STOP-1", "valor_observado": 1.0}), "O-05")
    R("posicion_cierre_automatico_sin_condicion_O06", o, lambda: o.posicion_transicion(P, "CERRANDO", "F", AHORA), "O-06")
    R("posicion_condicion_no_declarada_O06", o, lambda: o.posicion_transicion(P, "CERRANDO", "F", AHORA, condicion={"id": "INVENTADA", "valor_observado": 1.0}), "O-06")
    R("posicion_condicion_no_se_cumple_O06", o, lambda: o.posicion_transicion(P, "CERRANDO", "F", AHORA, condicion={"id": "STOP-1", "valor_observado": 1.2}), "O-06")
    R("posicion_valor_no_numerico_O06", o, lambda: o.posicion_transicion(P, "CERRANDO", "F", AHORA, condicion={"id": "STOP-1", "valor_observado": "1.0"}), "O-06")
    R("posicion_operador_manual_sin_motivo_O15", o, lambda: o.posicion_transicion(P, "CERRANDO", "OPERADOR", AHORA), "O-15")
    r = o.proponer_sobre_posicion(P, "la tesis parece debilitada por una noticia", "H", AHORA)
    h.chk("H_propone_sin_cambiar_estado", r["ok"] and o.posiciones[P]["estado"] == "ABIERTA" and len(o.posiciones[P]["propuestas"]) == 1)
    R("propuesta_sin_texto_O15", o, lambda: o.proponer_sobre_posicion(P, "", "H", AHORA), "O-15")
    h.chk("H_pone_en_revision", o.posicion_transicion(P, "EN_REVISION", "H", AHORA)["ok"])
    R("confirmar_tesis_sin_motivo_O15", o, lambda: o.posicion_transicion(P, "ABIERTA", "BROKER", AHORA), "O-15")
    h.chk("confirmar_tesis_ok", o.posicion_transicion(P, "ABIERTA", "BROKER", AHORA, motivo="la tesis se mantiene")["ok"])
    R("stop_no_reduce_automaticamente_O06", o, lambda: o.posicion_transicion(P, "REDUCIENDO", "F", AHORA, condicion={"id": "STOP-1", "valor_observado": 1.04}), "O-06")
    h.chk("operador_reduce_con_cantidad_y_motivo", o.posicion_transicion(P, "REDUCIENDO", "OPERADOR", AHORA, motivo="reducir riesgo", cantidad=60.0)["ok"])
    ORD2 = {"orden_id": "ORD-2", "conciliada": True}
    R("reduccion_sin_orden_conciliada_O06", o, lambda: o.posicion_transicion(P, "ABIERTA", "G", AHORA, restante=40.0, orden={"orden_id": "ORD-2", "conciliada": False}), "O-06")
    R("reduccion_total_no_puede_volver_a_abierta_O06", o, lambda: o.posicion_transicion(P, "ABIERTA", "G", AHORA, restante=0, orden=ORD2), "O-06")
    R("reduccion_parcial_no_puede_cerrar_O06", o, lambda: o.posicion_transicion(P, "CERRADA", "G", AHORA, restante=40.0, orden=ORD2), "O-06")
    R("restante_mayor_que_la_cantidad_O06", o, lambda: o.posicion_transicion(P, "ABIERTA", "G", AHORA, restante=500.0, orden=ORD2), "O-06")
    R("reduccion_sin_stop_redimensionado_O06", o, lambda: o.posicion_transicion(P, "ABIERTA", "G", AHORA, restante=40.0, orden=ORD2), "O-06")
    h.chk("reduccion_parcial_vuelve_a_abierta", o.posicion_transicion(P, "ABIERTA", "G", AHORA, restante=40.0, orden=ORD2, protecciones=["ORD-S2"])["ok"]
          and o.posiciones[P]["cantidad"] == 40.0 and o.posiciones[P]["protecciones"] == ["ORD-S2"])
    h.chk("objetivo_numerico_cierra", o.posicion_transicion(P, "CERRANDO", "ORQUESTADOR", AHORA, condicion={"id": "OBJ-1", "valor_observado": 1.16})["ok"])
    R("cerrando_no_admite_restante_O06", o, lambda: o.posicion_transicion(P, "CERRADA", "G", AHORA, restante=10.0, orden=ORD2), "O-06")
    h.chk("cierre_conciliado", o.posicion_transicion(P, "CERRADA", "G", AHORA, restante=0, orden={"orden_id": "ORD-3", "conciliada": True})["ok"])
    R("posicion_cerrada_es_terminal_O14", o, lambda: o.posicion_transicion(P, "EN_REVISION", "H", AHORA), "O-14")
    o = nuevo(); hasta(o, "EJECUTADA")
    R("reclasificar_sin_operador_O05", o, lambda: o.reclasificar(P, "LARGO_PLAZO", "BROKER", "x", AHORA), "O-05")
    R("reclasificar_sin_motivo_O15", o, lambda: o.reclasificar(P, "LARGO_PLAZO", "OPERADOR", "", AHORA), "O-15")
    h.chk("reclasificar_con_operador_ok", o.reclasificar(P, "LARGO_PLAZO", "OPERADOR", "decisión del operador", AHORA)["ok"] and o.posiciones[P]["cartera"] == "LARGO_PLAZO")
    o.posiciones[P]["historial"][0]["actor"] = "otro"
    R("historial_de_posicion_alterado_O13", o, lambda: o.posicion_transicion(P, "EN_REVISION", "H", AHORA), "O-13")
    o = nuevo(); hasta(o, "EJECUTADA")
    h.chk("operador_manual_con_motivo_cierra", o.posicion_transicion(P, "CERRANDO", "OPERADOR", AHORA, motivo="decisión propia")["ok"])

    # ---------------------------------------------------------------- robustez
    o = nuevo()
    for nombre, fn in (("detectar_basura", lambda: o.detectar(None, [], {}, 5, "BROKER", AHORA)),
                       ("emitir_basura", lambda: o.emitir_encargo({}, None, "BROKER", AHORA)),
                       ("gasto_basura", lambda: o.registrar_gasto([], {}, None, AHORA)),
                       ("comparar_basura", lambda: o.comparar("x", "D", AHORA)),
                       ("barrer_ahora_basura", lambda: o.barrer(123))):
        try:
            r = fn()
            h.chk("sin_excepciones_" + nombre, r["ok"] is False and r["codigo"].startswith("O-"), r)
        except Exception as ex:   # noqa: BLE001
            h.chk("sin_excepciones_" + nombre, False, f"lanzó {type(ex).__name__}")
    prof = []
    for _ in range(100000):
        prof = [prof]
    o = nuevo(); o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    e = encargo(1); e["payload"]["extra"] = prof
    try:
        r = o.emitir_encargo("EXP-0001", e, "GESTOR_TACTICA", AHORA)
        h.chk("sin_excepciones_anidamiento_extremo", r["ok"] is False and r["codigo"] in ("O-00", "O-01"), r)
        h.chk("anidamiento_extremo_deja_estado_intacto", o.expedientes["EXP-0001"]["estado"] == "DETECTADA" and not o.encargos)
    except Exception as ex:   # noqa: BLE001
        h.chk("sin_excepciones_anidamiento_extremo", False, type(ex).__name__)


    # ---------------------------------------------------------------- correcciones tras la revisión independiente
    for nombre, cfg in (("perfiles_vacios", {"perfiles_activos": []}), ("max_reintentos_cero", {"max_reintentos": 0}),
                        ("tope_negativo", {"dia_coste_max_eur": -1}), ("apalancamiento_texto", {"apalancamiento_permitido": "no"}),
                        ("matriz_no_bool", {"matriz_autonomia": {"TACTICA": "si"}})):
        try:
            Orquestador({**CFG, **cfg}, CAL)
            h.chk("config_invalida_" + nombre, False, "arrancó")
        except ValueError:
            h.chk("config_invalida_" + nombre, True)
    o = nuevo(); hasta(o, "DETECTADA")
    R("reloj_retrocede_O16", o, lambda: o.barrer("2026-11-06T08:00:00+00:00"), "O-16")
    h.chk("reloj_igual_o_posterior_ok", o.barrer(AHORA)["ok"])
    o = nuevo(); hasta(o, "AUTORIZADA")
    o.expedientes["EXP-0001"]["propuesta"]["entrada"]["limite"] = 9.9
    R("propuesta_alterada_sin_tocar_historial_O13", o, lambda: o.ejecutar("EXP-0001", {"orden_id": "ORD-1", "cantidad": 1.0, "precio": 9.9, "conciliada": True, "proteccion_orden_ids": ["P"]}, "G", AHORA), "O-13", mutacion_permitida=True)
    o = nuevo(); hasta(o, "AUTORIZADA")
    R("ejecutar_precio_fuera_de_tolerancia_O06", o, lambda: o.ejecutar("EXP-0001", {"orden_id": "ORD-1", "cantidad": 1.0, "precio": 1.50, "conciliada": True, "proteccion_orden_ids": ["P"]}, "G", AHORA), "O-06")
    o = nuevo(); hasta(o, "EJECUTADA")
    o.detectar("EXP-0007", "COR-0007", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    h.chk("orden_usada_queda_registrada", "ORD-1" in o.ordenes_usadas and "ORD-1-STOP" in o.ordenes_usadas)
    o = nuevo(); hasta(o, "PROPUESTA")
    # reemplazo de sello: cascada a expedientes
    s2 = construir_k(ctx={**CTX_K, "secuencia": 2, "reemplaza_a": "K-20261105-001"})
    o = nuevo(); hasta(o, "COMPARADA")
    if s2[0] is not None or True:
        r2 = o.registrar_sello(s2[1]["sello"], AHORA)
        h.chk("reemplazo_de_sello_caduca_expedientes", r2["ok"] and o.expedientes["EXP-0001"]["estado"] == "CADUCADA"
              and o.expedientes["EXP-0002"]["estado"] == "CADUCADA", r2)
    # gasto: la reserva de un encargo vivo cuenta el día siguiente
    o = nuevo({"dia_coste_max_eur": 7.0}); hasta(o, "EN_ANALISIS")
    o.detectar("EXP-0002", "COR-0002", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    R("reserva_viva_cuenta_O08", o, lambda: o.emitir_encargo("EXP-0002", encargo(2), "GESTOR_TACTICA", AHORA), "O-08")
    # idempotencia entre expedientes
    o = nuevo(); hasta(o, "EN_ANALISIS")
    o.detectar("EXP-0002", "COR-0002", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
    R("mismo_encargo_en_otro_expediente_O12", o, lambda: o.emitir_encargo("EXP-0002", encargo(1), "GESTOR_TACTICA", AHORA), "O-12")
    # actor no textual
    R("actor_no_textual_O01", o, lambda: o.descartar("EXP-0002", "x", ["BROKER"], AHORA), "O-01")
    # cabezas
    cab = o.cabezas()
    h.chk("cabezas_cubre_expedientes", set(cab) >= {"EXP:EXP-0001", "EXP:EXP-0002"} and all(len(v) == 64 for v in cab.values()))

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO ORQUESTADOR:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
