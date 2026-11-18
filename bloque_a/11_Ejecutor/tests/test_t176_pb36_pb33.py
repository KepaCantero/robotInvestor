"""T-176 · PB-36 (recalibración fuera de bandas: umbral E en P-09 y P-05 con banda PENDIENTE_OPERADOR, P3- a la cola de tipo 3
de HA por CT-19, F10 intacto) y PB-33 (sección «Novedades» de F6 con la revocación del certificado y la alerta de
sobreconfianza). Siguen los pasos del Plan de pruebas V3.0 con el cliente simulado."""
import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.evaluador import ESTIMADORES_TRIMESTRALES, Evaluador
from conftest import AS_OF, config_pruebas, nuevo_bloque
from test_fase4_huecos import _pb33_revision_y_run

# T-176 r02 (QA r01, H-05): §6 del Plan de pruebas V3.0 (batería de regresión, literal) y las específicas de R18 (§5)
BATERIA_Y_R18 = ["PB-01", "PB-02", "PB-06", "PB-08", "PB-13", "PB-18", "PB-20", "PB-21", "PB-22", "PB-23", "PB-30", "PB-31",
                 "PB-36", "PB-37", "PB-39", "PB-49", "PB-10", "PB-34", "PB-35", "PB-50"]
UMBRAL_OPTIMO = 48            # Preparación de PB-36: el umbral E óptimo sería 48 (−12 frente al inicial, 60)


def _historia_umbral_e(almacen, optimo=UMBRAL_OPTIMO, n=60, desde="2026-01-05", base=9000):
    """PRG resueltos (sin la A de su opción, para que la recalibración de RK no intervenga) cuya opción acierta si y solo si
    su E es ≥ `optimo`: la E va de 40 a 79."""
    for i in range(n):
        pid = f"PRG-2026-{base + i:04d}"
        e = 40 + (i % 40)
        fr = str((pd.Timestamp(desde) + pd.offsets.BDay(i)).date())
        almacen.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "clase": "RV", "horizonte": "H3", "prob_interna": 0.65,
                                         "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True, "sentido": "POSITIVO",
                                         "fecha_emision": "2025-12-01", "estado": "ABIERTO", "fecha_resolucion": fr,
                                         "puntuaciones_opcion": {"E": e}})
        almacen.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                                         "resolucion": {"resultado_binario": int(e >= optimo), "valor_observado": 0.01,
                                                        "comprobacion_fuga": "SUPERADA", "fecha_resuelto": fr}})


def _f10_de(b, *ids):
    return {i: [e for e in b.almacen.leer("F10") if e.get("param_id") == i] for i in ids}


def _p3_f6(b):
    return {k: v for k, v in b.almacen.estado("F6", clave="id").items() if v.get("tipo_entrada") == "P3"}


def _p05_sembrado(objetivo=10):
    """Preparación de PB-36, segundo caso: evidencia de que P-05 (candidatas máximas, 8) debería cambiar."""
    return lambda self, as_of: {"objetivo": objetivo, "parametro": "P-05", "evidencia": "sembrada (plan PB-36)"}


# ---------------------------------------------------------------- PB-36 · criterio completo, con el ciclo simulado
def test_pb36_umbral_e_y_p05_fuera_de_banda_a_la_cola_de_ha_con_f10_intacto(tmp_path, universo, monkeypatch):
    monkeypatch.setitem(ESTIMADORES_TRIMESTRALES, ("P-05", None), _p05_sembrado())
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha("2026-05-01")
    _historia_umbral_e(b.almacen)
    b.fijar_fecha(AS_OF)
    f10_antes = _f10_de(b, "P-09", "P-05")
    vigente_e = b.f10()["P-09"]["E"]
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})                                   # 1) revisión trimestral (C5) y el RUN-
    rev = r["evaluacion"]["revision_trimestral"]
    assert rev["id"] == "RTR-2026-T2" and rev["parametros"]["P-09·E"]["evidencia"]["objetivo"] == UMBRAL_OPTIMO
    p3 = _p3_f6(b)
    p09 = p3[rev["parametros"]["P-09·E"]["resultado"]]
    p05 = p3[rev["parametros"]["P-05"]["resultado"]]
    assert (p09["motivo"], p09["de"], p09["a"], p09["acumulado_vs_inicial"]) == ("fuera de banda", vigente_e, 48.0, -12.0)
    assert p09["banda"] == {"estado": "DEFINIDA", "trimestral": 5.0, "total": 10.0}
    assert (p05["motivo"], p05["banda"], p05["de"], p05["a"]) == ("sin banda", {"estado": "PENDIENTE_OPERADOR"}, 8.0, 10.0)
    for p in (p09, p05):                                                             # esquema F6 4.7
        assert p["id"].startswith("P3-EVAL-") and p["estado"] == "ENVIADA" and p["evidencia"] and p["impacto_esperado"]
        assert p["pruebas_regresion"] == BATERIA_Y_R18 and p["plan_reversion"]   # H-05 de la QA r01
    assert p09["evidencia"]["indice_youden"] == pytest.approx(1.0) and p09["evidencia"]["n"] == 60
    # Ningún cambio en F10 para ambos (sin CFG- ni valor nuevo), y HT-03 sigue con 60
    assert _f10_de(b, "P-09", "P-05") == f10_antes and b.f10()["P-09"]["E"] == vigente_e and "P-05" not in b.f10()
    assert not [a for a in b.almacen.estado("F6", clave="id").values() if a.get("tipo_entrada") == "AJU"
                and a.get("parametro") in ("P-09", "P-05")]
    # Enviada vía CT-19 al Orquestador, que la registra en HA como PENDING_OPERATOR
    ct19 = {m["msg_id"]: m for m in b.mensajeria.registro if m["contrato"] == "CT-19" and m["receptor"] == "AG-18"}
    ha = b.almacen.estado("HA")
    for p in (p09, p05):
        assert p["elevada_via"] in ct19 and ct19[p["elevada_via"]]["emisor"] == "AG-20"
        cola = ha[p["id"]]
        assert (cola["tipo_entrada"], cola["origen"], cola["estado"], cola["recibida_via"]) == ("P3", "EVAL", "PENDING_OPERATOR",
                                                                                               p["elevada_via"])
        assert cola["evidencia"] == p["evidencia"] and cola["plan_reversion"] == p["plan_reversion"]
        assert [h["autor"] for h in cola["_historial"]] == ["AG-18"]
    assert all(b.almacen.verificar_integridad().values())


def test_pb36_un_segundo_ciclo_no_duplica_la_elevacion_ni_la_revision(tmp_path, universo, monkeypatch):
    monkeypatch.setitem(ESTIMADORES_TRIMESTRALES, ("P-05", None), _p05_sembrado())
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha("2026-05-01")
    _historia_umbral_e(b.almacen)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    p3, ha = set(_p3_f6(b)), [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "P3"]
    n_ct19 = len([m for m in b.mensajeria.registro if m["contrato"] == "CT-19" and m["receptor"] == "AG-18"])
    r2 = b.ciclo(str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date()), alcance={"clases": ["RV"]})   # mismo trimestre
    assert r2["evaluacion"]["revision_trimestral"] is None                            # una revisión por trimestre (F10, regla 7)
    assert set(_p3_f6(b)) == p3 and len(p3) == 2
    assert [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "P3"] == ha
    assert len([m for m in b.mensajeria.registro if m["contrato"] == "CT-19" and m["receptor"] == "AG-18"]) == n_ct19 == 2


def test_p3_de_p11_tambien_se_eleva(tmp_path, universo):
    """La P3- de los pesos de RK fuera de banda (anterior a T-176) también llega a la cola de tipo 3."""
    from test_t66_evaluacion import _celda_recalibrable
    rr = {"paso": 0.05, "banda_trimestral": 0.05, "banda_total": 0.02, "dif_ic_min": 0.10, "meses_sombra": 3}
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(evaluacion={"recalibracion_rk": rr}))
    b.reloj.fijar("2026-01-02")
    _celda_recalibrable(b.almacen, contaminados=0)
    b.fijar_fecha("2026-01-02")
    p3 = b.evaluador.recalibrar("2026-01-02")
    assert p3["tipo_entrada"] == "P3" and p3["motivo"] == "fuera de banda"
    assert b.elevar_propuestas_tipo3("2026-01-02", "RUN-2026-0001") == [p3["id"]]
    assert b.almacen.estado("HA")[p3["id"]]["estado"] == "PENDING_OPERATOR"
    assert b.elevar_propuestas_tipo3("2026-01-02", "RUN-2026-0001") == []           # idempotente
    # H-02 de la QA r01: el plan de reversión (esquema F6 4.7) en F6 y en la cola de HA; H-05: la batería de regresión
    assert p3["plan_reversion"] and b.almacen.estado("HA")[p3["id"]]["plan_reversion"] == p3["plan_reversion"]
    assert p3["pruebas_regresion"] == BATERIA_Y_R18 and (p3["parametro"], p3["trimestre"]) == ("P-11", "2026-T1")


# ---------------------------------------------------------------- T-176 r02 · regresiones de la QA r01
def test_r02_h01_recalibrar_dos_semanas_deja_una_p3_de_p11_en_f6_y_en_ha(tmp_path, universo):
    from test_t66_evaluacion import _celda_recalibrable
    rr = {"paso": 0.05, "banda_trimestral": 0.05, "banda_total": 0.02, "dif_ic_min": 0.10, "meses_sombra": 3}
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(evaluacion={"recalibracion_rk": rr}))
    b.reloj.fijar("2026-01-02")
    _celda_recalibrable(b.almacen, contaminados=0)
    ids = []
    for fecha in ("2026-01-02", "2026-01-09"):
        b.fijar_fecha(fecha)
        ids.append(b.evaluador.recalibrar(fecha)["id"])
        b.elevar_propuestas_tipo3(fecha, "RUN-2026-0001")
    assert ids[0] == ids[1]
    assert len([x for x in b.almacen.estado("F6", clave="id").values() if x.get("tipo_entrada") == "P3"]) == 1
    assert [k for k, v in b.almacen.estado("HA").items() if v.get("tipo_entrada") == "P3"] == [ids[0]]


def test_r02_h03_una_p3_abierta_del_parametro_bloquea_cualquier_otro_objetivo(tmp_path):
    e = _evaluador(tmp_path)
    primera = e.proponer_ajuste("P-09", "E", 48, {}, "2026-06-05")                   # 2026-T2
    e.almacen.reloj.fijar("2026-07-06")
    segunda = e.proponer_ajuste("P-09", "E", 47, {}, "2026-07-06")                   # 2026-T3, la primera sigue ENVIADA
    assert segunda == primera
    assert e.proponer_ajuste("P-09", "E", 57, {}, "2026-07-06") == primera           # tampoco un AJU- dentro de banda
    assert [x["id"] for x in e.almacen.leer("F6") if x.get("tipo_entrada") in ("P3", "AJU")] == [primera["id"]]
    otro = e.proponer_ajuste("P-09", "A", 40, {}, "2026-07-06")                       # otro componente: sí
    assert otro["id"] != primera["id"]


def test_r02_h03_la_revision_registra_la_p3_abierta(tmp_path):
    e = _evaluador(tmp_path)
    abierta = e.proponer_ajuste("P-09", "E", 70, {}, "2026-06-05")
    _historia_umbral_e(e.almacen)
    rev = e.revision_trimestral("2026-06-05")
    assert rev["parametros"]["P-09·E"]["resultado"] == abierta["id"]
    assert len([x for x in e.almacen.leer("F6") if x.get("tipo_entrada") == "P3"]) == 1


def _a_la_vez(n, fn):
    import threading
    barrera, fallos = threading.Barrier(n), []

    def correr(i):
        barrera.wait()
        try:
            fn(i)
        except Exception as ex:  # noqa: BLE001
            fallos.append(repr(ex))
    hilos = [threading.Thread(target=correr, args=(i,)) for i in range(n)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    return fallos


def test_r02_h04_propuestas_y_revisiones_concurrentes_no_se_duplican(tmp_path):
    evs = [_evaluador(tmp_path / "p") for _ in range(8)]
    assert _a_la_vez(8, lambda i: evs[i].proponer_ajuste("P-09", "E", 48, {}, "2026-06-05")) == []
    assert len({x["id"] for x in Almacen(tmp_path / "p").leer("F6") if x.get("tipo_entrada") == "P3"}) == 1
    base = Almacen(tmp_path / "r")
    base.reloj.fijar("2026-05-01")
    _historia_umbral_e(base)
    revs = [_evaluador(tmp_path / "r") for _ in range(4)]
    assert _a_la_vez(4, lambda i: revs[i].revision_trimestral("2026-06-05", "RUN-X")) == []
    f6 = Almacen(tmp_path / "r").leer("F6")
    assert [x.get("tipo_entrada") for x in f6].count("RTR") == 1 and [x.get("tipo_entrada") for x in f6].count("P3") == 1


def test_r02_h04_elevaciones_concurrentes_dejan_una_entrada_en_ha(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    p3 = b.evaluador.proponer_ajuste("P-09", "E", 48, {}, AS_OF)
    otros = [nuevo_bloque(tmp_path, universo) for _ in range(3)]
    for o in otros:
        o.fijar_fecha(AS_OF)
    assert _a_la_vez(3, lambda i: otros[i].elevar_propuestas_tipo3(AS_OF, "RUN-2026-0001")) == []
    assert [e["id"] for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "P3"] == [p3["id"]]
    assert len([e for e in b.almacen.leer("F6") if e.get("id") == p3["id"] and e.get("elevada_via")]) == 1


def test_r02_h06_una_p3_con_elevada_via_pero_fuera_de_ha_se_eleva(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    p3 = b.evaluador.proponer_ajuste("P-05", None, 10, {}, AS_OF)
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "P3", "id": p3["id"], "elevada_via": "MSG-2026-999999"})   # no existe
    assert p3["id"] not in b.almacen.estado("HA")
    assert b.elevar_propuestas_tipo3(AS_OF, "RUN-2026-0001") == [p3["id"]]
    assert b.almacen.estado("HA")[p3["id"]]["estado"] == "PENDING_OPERATOR"
    assert b.elevar_propuestas_tipo3(AS_OF, "RUN-2026-0001") == []


# ---------------------------------------------------------------- PB-36 · proponer_ajuste: dentro de banda, límites y fallo cerrado
def _evaluador(tmp_path, **extra):
    a = Almacen(tmp_path)
    a.reloj.fijar("2026-04-06")
    return Evaluador(a, None, None, config_pruebas(**extra), None)


@pytest.mark.parametrize("objetivo, tipo", [(55, "AJU"), (65, "AJU"), (54, "P3"), (66, "P3")])
def test_proponer_ajuste_banda_trimestral_de_p09_en_el_limite(tmp_path, objetivo, tipo):
    e = _evaluador(tmp_path)
    r = e.proponer_ajuste("P-09", "E", objetivo, {"prueba": True}, "2026-04-06")
    assert r["tipo_entrada"] == tipo
    if tipo == "AJU":
        assert (r["estado"], r["aplicado_en_produccion"], r["banda"]) == ("PROPUESTO", False, {"trimestral": 5.0, "total": 10.0})
        assert e.ajuste_en_sombra("2026-04-06") is None                              # no es la sombra de los pesos de RK
    else:
        assert r["motivo"] == "fuera de banda"
    assert not e.almacen.leer("F10")


def test_proponer_ajuste_dentro_de_banda_suma_lo_del_trimestre_y_el_total_frente_al_inicial(tmp_path):
    e = _evaluador(tmp_path)
    primero = e.proponer_ajuste("P-09", "E", 57, {}, "2026-04-06")                  # −3 frente al vigente (60)
    assert primero["tipo_entrada"] == "AJU" and e.proponer_ajuste("P-09", "E", 57, {}, "2026-04-06") == primero   # no se repite
    assert e.proponer_ajuste("P-09", "E", 58, {}, "2026-04-06")["tipo_entrada"] == "AJU"      # −2: 3 + 2 = 5, en el límite
    assert e.proponer_ajuste("P-09", "E", 59, {}, "2026-04-06")["motivo"] == "fuera de banda"  # −1: 3 + 2 + 1 = 6 > 5
    assert len([x for x in e.almacen.leer("F6") if x.get("tipo_entrada") == "AJU"]) == 2
    otro = _evaluador(tmp_path / "t3")                                                # otro trimestre, total frente al inicial
    assert otro.proponer_ajuste("P-09", "A", 50, {}, "2026-04-06")["tipo_entrada"] == "AJU"   # A: 55 → 50, −5
    assert not e.almacen.leer("F10") and not otro.almacen.leer("F10")


def test_proponer_ajuste_rechaza_no_calibrable_y_sin_banda_es_tipo_3(tmp_path):
    e = _evaluador(tmp_path, evaluacion={"bandas_f10": {"P-09": {"estado": "DEFINIDA", "trimestral": 5, "total": 10}}})
    with pytest.raises(ValueError, match="no es CALIBRABLE"):
        e.proponer_ajuste("P-04", None, 4, {}, "2026-04-06")                         # opciones máximas: OPERADOR
    with pytest.raises(ValueError, match="no numérico"):
        e.proponer_ajuste("P-09", "E", float("nan"), {}, "2026-04-06")
    r = e.proponer_ajuste("P-06", None, 6, {}, "2026-04-06")                         # CALIBRABLE sin banda en la configuración
    assert (r["tipo_entrada"], r["motivo"], r["banda"]) == ("P3", "sin banda", {"estado": "PENDIENTE_OPERADOR"})
    assert e.proponer_ajuste("P-09", "E", 60, {}, "2026-04-06") is None             # igual al vigente
    with pytest.raises(KeyError):
        e.proponer_ajuste("P-24", None, 0.75, {}, "2026-04-06")                      # sin valor en F10 ni en la configuración
    assert not e.almacen.leer("F10")


# ---------------------------------------------------------------- PB-36 · evidencia del umbral E
def test_evidencia_umbral_e_youden_y_muestra_insuficiente(tmp_path):
    e = _evaluador(tmp_path)
    _historia_umbral_e(e.almacen, n=29)
    ev29 = e.evidencia_umbral_e("2026-06-05")
    assert ev29["objetivo"] is None and "29 < 30" in ev29["motivo"]
    assert e.revision_trimestral("2026-06-05") == {"id": None, "trimestre": "2026-T2", "parametros": {
        "P-09·E": {"parametro": "P-09", "componente": "E", "evidencia": ev29, "resultado": "SIN_EVIDENCIA"}}}
    assert "RTR-2026-T2" not in e.almacen.estado("F6", clave="id")                  # sin evidencia, el C5 siguiente la repite
    _historia_umbral_e(e.almacen, n=60, optimo=52, base=8000)
    assert e.evidencia_umbral_e("2026-06-05")["objetivo"] is not None


def test_evidencia_umbral_e_empate_elige_el_mas_cercano_al_vigente_y_j_nulo_no_propone(tmp_path):
    e = _evaluador(tmp_path)
    for i in range(40):                                  # la E no separa nada: J ≤ 0 en todo umbral
        pid = f"PRG-2026-{i + 1:04d}"
        e.almacen.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "clase": "RV", "horizonte": "H3", "prob_interna": 0.65,
                                           "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True, "sentido": "POSITIVO",
                                           "fecha_emision": "2026-01-02", "estado": "ABIERTO", "fecha_resolucion": "2026-03-02",
                                           "puntuaciones_opcion": {"E": 61 + (i % 2)}})
        e.almacen.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                                           "resolucion": {"resultado_binario": (i // 2) % 2, "valor_observado": 0.0,
                                                          "comprobacion_fuga": "SUPERADA", "fecha_resuelto": "2026-03-02"}})
    r = e.evidencia_umbral_e("2026-06-05")
    assert r["objetivo"] is None and "J ≤ 0" in r["motivo"]


# ---------------------------------------------------------------- PB-33 · sección «Novedades» de F6
def test_pb33_novedades_de_la_semana_con_la_revocacion_y_la_leccion(tmp_path, universo):
    b, r = _pb33_revision_y_run(tmp_path, universo)
    nov = r["evaluacion"]["novedades"]
    semana = pd.Timestamp(AS_OF).isocalendar()
    assert nov["id"] == f"NOV-{semana.year}-W{semana.week:02d}" and nov["id"] in b.almacen.estado("F6", clave="id")
    rev = [x for x in nov["revocaciones"] if x["id"] == "CERT-2025-0001"]
    assert len(rev) == 1 and rev[0]["estado"] == "REVOCADO" and rev[0]["fecha"] == AS_OF and "deterioro" in rev[0]["motivo"]
    alerta = next(l for l in r["evaluacion"]["lecciones_nuevas"] if l["tipo"] == "CALIBRACION")
    assert alerta["id"] in [x["id"] for x in nov["lecciones"]]                        # la alerta de sobreconfianza, por id
    assert "CERT-2025-0001" not in [x["id"] for x in nov["altas"]]                    # el alta es de antes de esta semana


def test_novedades_semana_siguiente_solo_lo_nuevo_y_misma_semana_rehace(tmp_path):
    a = Almacen(tmp_path)
    a.reloj.fijar("2026-06-01")
    e = Evaluador(a, None, None, config_pruebas(), None)
    a.escribir("F6", "AG-20", {"tipo_entrada": "CERT", "id": "CERT-2026-0001", "estado": "VIGENTE", "celda": {"clase": "RV"}})
    a.escribir("F6", "AG-20", {"tipo_entrada": "LEC", "id": "LEC-2026-0001", "estado": "VIGENTE", "tipo": "PREDICTIVA"})
    a.escribir("F6", "AG-20", {"tipo_entrada": "MET", "id": "MET-2026-06-01"})                 # no es novedad
    n1 = e.publicar_novedades("2026-06-01")
    assert [x["id"] for x in n1["altas"]] == ["CERT-2026-0001"] and [x["id"] for x in n1["lecciones"]] == ["LEC-2026-0001"]
    a.reloj.fijar("2026-06-03")                                                       # la misma semana: se rehace entera
    a.escribir("F6", "AG-20", {"tipo_entrada": "AJU", "id": "AJU-2026-0001", "parametro": "P-11", "estado": "EN_SOMBRA"})
    n1b = e.publicar_novedades("2026-06-03")
    assert n1b["id"] == n1["id"] and [x["id"] for x in n1b["ajustes"]] == ["AJU-2026-0001"] and n1b["altas"] == n1["altas"]
    assert a.estado("F6", clave="id")[n1["id"]]["ajustes"] == n1b["ajustes"]
    assert e.publicar_novedades("2026-06-03")["ajustes"] == n1b["ajustes"]           # sin duplicados
    a.reloj.fijar("2026-06-08")                                                       # semana siguiente
    assert e.publicar_novedades("2026-06-08") is None                                  # nada nuevo: no se publica
    a.escribir("F6", "AG-20", {"tipo_entrada": "CERT_REVOCACION", "id": "CERT-2026-0001", "estado": "REVOCADO",
                               "motivo_cambio": "deterioro", "fecha": "2026-06-08"})
    a.escribir("F6", "AG-20", {"tipo_entrada": "LEC", "id": "LEC-2026-0001", "estado": "CADUCADA"})   # cambio, no lección nueva
    a.escribir("F6", "AG-20", {"tipo_entrada": "AJU", "id": "AJU-2026-0001", "estado": "CONFIRMADO"})  # cambio de estado, no ajuste nuevo
    n2 = e.publicar_novedades("2026-06-08")
    assert n2["id"] != n1["id"] and [x["id"] for x in n2["revocaciones"]] == ["CERT-2026-0001"]
    assert n2["altas"] == n2["ajustes"] == n2["lecciones"] == []


def test_r03_h07_seis_recalibraciones_a_la_vez_dejan_una_sola_p3_de_p11(tmp_path):
    """QA r02, H-07: la deduplicación de la P3- de P-11 (H-01) comprueba y escribe en una sola transacción."""
    from test_t66_evaluacion import _celda_recalibrable
    rr = {"paso": 0.05, "banda_trimestral": 0.05, "banda_total": 0.02, "dif_ic_min": 0.10, "meses_sombra": 3}
    base = Almacen(tmp_path)
    base.reloj.fijar("2026-01-02")
    _celda_recalibrable(base, contaminados=0)
    evs = [_evaluador(tmp_path, evaluacion={"recalibracion_rk": rr}) for _ in range(6)]
    for e in evs:
        e.almacen.reloj.fijar("2026-01-02")
    assert _a_la_vez(6, lambda i: evs[i].recalibrar("2026-01-02")) == []
    assert len({x["id"] for x in Almacen(tmp_path).leer("F6") if x.get("tipo_entrada") == "P3"}) == 1
