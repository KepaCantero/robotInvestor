"""T-178 · PB-19, agente de instancia única saturado (Plan de pruebas V3.0; prompt del Orquestador V5.0, 5.3 punto 5).

Con un agente de instancia única saturado: ninguna ORD-, su cola reordenada por prioridad, el aviso al Coordinador sobre
plazos (vía HA) si está en el camino de la entrega y una propuesta de tipo 3 si la saturación se repite (INC-T178-01).
"""
import datetime as dt
import threading

import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.carga import CLAVE_P3, avisos_plazos, registrar_carga
from bloque_a.configuracion import parametro
from bloque_a.guias import BATERIA_REGRESION
from bloque_a.herramientas.ht08_monitor import CAMINO_ENTREGA, Monitor
from conftest import AS_OF, nuevo_bloque

CON_ESTADO = ("AG-01", "AG-02", "AG-18", "AG-19", "AG-20")


def _seis_ct05():
    """Seis órdenes CT-05 para AG-02 en orden de llegada (la preparación de PB-19), con prioridades mezcladas."""
    return [{"ref": "MSG-1", "prioridad": "ALTA", "tipo": "SEGUIMIENTO", "fecha_objetivo": "2026-06-05"},   # C6: al final
            {"ref": "MSG-2", "prioridad": "NORMAL", "tipo": "PERIODICO", "fecha_objetivo": "2026-06-12"},
            {"ref": "MSG-3", "prioridad": "BAJA", "tipo": "AD_HOC", "fecha_objetivo": "2026-06-01"},
            {"ref": "MSG-4", "prioridad": "ALTA", "tipo": "AD_HOC", "fecha_objetivo": "2026-06-19"},
            {"ref": "MSG-5", "prioridad": "NORMAL", "tipo": "AD_HOC", "fecha_objetivo": "2026-06-10"},
            {"ref": "MSG-6", "tipo": "PERIODICO"}]                       # sin prioridad (NORMAL) ni fecha: tras las NORMAL


ORDEN_ESPERADO = ["MSG-4", "MSG-5", "MSG-2", "MSG-6", "MSG-3", "MSG-1"]


def _cars(entradas, agente):
    return [e for e in entradas if e["tipo_entrada"] == "CAR" and e["agente"] == agente]


# ---------------------------------------------------------------- CA-1, CA-2 · sin ORD- y cola reordenada
def test_pb19_seis_ct05_sin_ord_y_la_cola_queda_reordenada_por_prioridad():
    m = Monitor(umbral_cola=3)
    m.encolar("AG-02", ordenes=_seis_ct05())
    assert m.cola["AG-02"] == 6
    salida = m.evaluar_instancias()
    assert not [o for o in salida if o["tipo_entrada"] == "ORD"] and m.instancias["AG-02"] == 1
    [car] = _cars(salida, "AG-02")
    assert [c["ref"] for c in car["cola_reordenada"]] == ORDEN_ESPERADO
    assert [c["posicion"] for c in car["cola_reordenada"]] == [1, 2, 3, 4, 5, 6]
    assert car["cola_reordenada"][3]["prioridad"] == "NORMAL" and car["cola_reordenada"][3]["fecha_objetivo"] is None
    assert car["reordenada"] is True and car["orden_cambiado"] is True and car["saturado"] is True
    assert (car["cola"], car["instancias"], car["umbral_cola"], car["sin_detalle"]) == (6, 1, 3, 0)
    assert [p["ref"] for p in m.pendientes["AG-02"]] == ORDEN_ESPERADO          # el monitor atiende en ese orden


def test_pb19_el_orden_es_estable_y_una_cola_ya_ordenada_no_cambia():
    m = Monitor(umbral_cola=3)
    m.encolar("AG-02", ordenes=[{"ref": f"MSG-{i}", "prioridad": "NORMAL", "fecha_objetivo": "2026-06-12"} for i in range(5)])
    [car] = m.evaluar_instancias()
    assert [c["ref"] for c in car["cola_reordenada"]] == [f"MSG-{i}" for i in range(5)]       # empate: orden de llegada
    assert car["orden_cambiado"] is False


def test_pb19_la_cola_sin_detalle_se_cuenta_y_el_ct01_baja_tras_la_c6_no():
    """Lo que solo se encoló como número va en `sin_detalle`; una ALTA de C6 va detrás de una BAJA de C1–C3 (R5, 6)."""
    m = Monitor(umbral_cola=3)
    m.encolar("AG-02", 3)
    m.encolar("AG-02", ordenes=[{"ref": "C6", "prioridad": "ALTA", "tipo": "SEGUIMIENTO"}, {"ref": "C2", "prioridad": "BAJA"}])
    [car] = m.evaluar_instancias()
    assert car["cola"] == 5 and car["sin_detalle"] == 3 and [c["ref"] for c in car["cola_reordenada"]] == ["C2", "C6"]


def test_pb19_sin_saturacion_no_hay_car_ni_reordenacion():
    m = Monitor(umbral_cola=3)
    ordenes = _seis_ct05()[:3]
    m.encolar("AG-02", ordenes=ordenes)
    assert m.evaluar_instancias() == []
    assert [p["ref"] for p in m.pendientes["AG-02"]] == ["MSG-1", "MSG-2", "MSG-3"]


# ---------------------------------------------------------------- CA-3 · aviso al Coordinador
def test_pb19_aviso_al_coordinador_solo_de_los_agentes_del_camino_de_la_entrega():
    m = Monitor(umbral_cola=3)
    for ag in CON_ESTADO:
        m.encolar(ag, ordenes=[{**o, "ref": f"{ag}-{o['ref']}"} for o in _seis_ct05()])
    cars = {e["agente"]: e for e in m.evaluar_instancias()}
    assert set(cars) == set(CON_ESTADO) and all(e["tipo_entrada"] == "CAR" for e in cars.values())
    assert CAMINO_ENTREGA == {"AG-01", "AG-02", "AG-18"}
    for ag in ("AG-01", "AG-02", "AG-18"):
        av = cars[ag]["aviso_coordinador"]
        assert cars[ag]["afecta_plazos"] is True and av["destinatario"] == "AG-01" and av["en_espera_sobre_umbral"] == 3
        assert [o["ref"] for o in av["ordenes"]] == [f"{ag}-{r}" for r in ORDEN_ESPERADO]
        assert av["ordenes"][0]["fecha_objetivo"] == "2026-06-19"
    for ag in ("AG-19", "AG-20"):                 # asíncrono (R17) y en segundo plano (C4, C5): no retrasan una entrega
        assert cars[ag]["afecta_plazos"] is False and "aviso_coordinador" not in cars[ag]


def test_pb19_el_coordinador_lee_su_aviso_en_ha(tmp_path):
    al = Almacen(tmp_path)
    m = Monitor(umbral_cola=3)
    m.encolar("AG-02", ordenes=_seis_ct05())
    m.encolar("AG-20", 6)
    escritas = registrar_carga(al, m.evaluar_instancias(), "RUN-2026-0001")
    avisos = avisos_plazos(al, "RUN-2026-0001")
    assert [a["agente"] for a in avisos] == ["AG-02"] and avisos[0]["id"] == _cars(escritas, "AG-02")[0]["id"]
    assert avisos[0]["id"].startswith("CAR-") and avisos[0]["_autor"] == "AG-18"
    assert avisos_plazos(al, "RUN-2026-0002") == [] and len(avisos_plazos(al)) == 1


# ---------------------------------------------------------------- CA-4 · propuesta de tipo 3 si se repite
def _saturar(al, run_id, agente="AG-02"):
    m = Monitor(umbral_cola=3)
    m.encolar(agente, ordenes=_seis_ct05())
    return _cars(registrar_carga(al, m.evaluar_instancias(), run_id), agente)[0]


def _p3(al):
    return [e for e in al.leer("HA") if e["tipo_entrada"] == "P3"]


def test_pb19_la_primera_saturacion_no_propone_y_la_segunda_en_otro_run_si(tmp_path):
    al = Almacen(tmp_path)
    car1 = _saturar(al, "RUN-2026-0001")
    assert "p3_id" not in car1 and _p3(al) == []
    car2 = _saturar(al, "RUN-2026-0002")
    [p3] = _p3(al)
    assert car2["p3_id"] == p3["id"] and p3["id"].startswith("P3-ORQ-")
    assert (p3["origen"], p3["estado"], p3["clave"], p3["agente_saturado"]) == ("ORQ", "PENDING_OPERATOR", CLAVE_P3, "AG-02")
    assert p3["evidencia"]["car"] == [car1["id"]] and p3["evidencia"]["runs"] == ["RUN-2026-0001"]     # solo CAR- ya escritos
    assert p3["evidencia"]["run_actual"] == "RUN-2026-0002" and p3["evidencia"]["cola"] == 6
    assert p3["pruebas_regresion"] == list(BATERIA_REGRESION) + ["PB-19"] and p3["plan_reversion"] and p3["impacto"]
    seq = {e["id"]: e["_seq"] for e in al.leer("HA")}
    assert seq[p3["id"]] < seq[car2["id"]]                         # la P3- se escribe antes que el CAR- que la cita


def test_pb19_dos_lecturas_del_mismo_run_no_son_una_repeticion(tmp_path):
    al = Almacen(tmp_path)
    _saturar(al, "RUN-2026-0001")
    car = _saturar(al, "RUN-2026-0001")
    assert "p3_id" not in car and _p3(al) == []


def test_pb19_la_propuesta_abierta_no_se_duplica_y_tras_rechazarla_hace_falta_otra_repeticion(tmp_path):
    al = Almacen(tmp_path)
    _saturar(al, "RUN-2026-0001")
    pid = _saturar(al, "RUN-2026-0002")["p3_id"]
    assert _saturar(al, "RUN-2026-0003")["p3_id"] == pid and len(_p3(al)) == 1           # abierta: se cita, no se duplica
    al.escribir("HA", "AG-18", {"tipo_entrada": "P3", "id": pid, "estado": "APROBADA"})
    assert _saturar(al, "RUN-2026-0004")["p3_id"] == pid                                  # aprobada sin aplicar: sigue abierta
    al.escribir("HA", "AG-18", {"tipo_entrada": "P3", "id": pid, "estado": "RECHAZADA", "decision_operador": {"texto": "no"}})
    car5 = _saturar(al, "RUN-2026-0005")
    assert "p3_id" not in car5 and len({e["id"] for e in _p3(al)}) == 1                   # la primera tras la decisión
    car6 = _saturar(al, "RUN-2026-0006")
    nuevas = [e for e in _p3(al) if e["id"] != pid]
    assert [e["id"] for e in nuevas] == [car6["p3_id"]] and nuevas[0]["evidencia"]["car"] == [car5["id"]]


def test_pb19_la_repeticion_es_por_agente_y_cuenta_los_car_anteriores_a_t178(tmp_path):
    al = Almacen(tmp_path)
    al.escribir("HA", "AG-18", {"tipo_entrada": "CAR", "id": al.nuevo_id("CAR"), "agente": "AG-20", "cola": 6, "instancias": 1,
                                "run_id": "RUN-2026-0001"})                                # CAR- de antes, sin `saturado`
    assert "p3_id" not in _saturar(al, "RUN-2026-0002", "AG-02")                           # otro agente no cuenta
    car = _saturar(al, "RUN-2026-0002", "AG-20")
    [p3] = _p3(al)
    assert car["p3_id"] == p3["id"] and p3["agente_saturado"] == "AG-20" and p3["evidencia"]["afecta_plazos"] is False


# ---------------------------------------------------------------- CA-5 · falla cerrado
@pytest.mark.parametrize("ordenes", [
    [{"ref": "MSG-1", "prioridad": "ALTA"}, {"ref": "MSG-2", "prioridad": "URGENTE"}],
    [{"ref": "MSG-1", "prioridad": "ALTA"}, {"prioridad": "BAJA"}],
    [{"ref": "MSG-1", "prioridad": "ALTA"}, {"ref": "MSG-1", "prioridad": "BAJA"}],
    [{"ref": "MSG-1", "prioridad": "alta"}],
    # r02 (QA r01, H-03): fecha objetivo que no es AAAA-MM-DD (o no es una fecha real)
    [{"ref": "MSG-1", "fecha_objetivo": "2026-06-12"}, {"ref": "MSG-2", "fecha_objetivo": "2026-6-5"}],
    [{"ref": "MSG-1", "fecha_objetivo": "05/06/2026"}],
    [{"ref": "MSG-1", "fecha_objetivo": float("nan")}],
    [{"ref": "MSG-1", "fecha_objetivo": 20260605}],
    [{"ref": "MSG-1", "fecha_objetivo": "2026-02-30"}],
    [{"ref": "MSG-1", "fecha_objetivo": "2026-06-05T10:00"}],
    # r02 (QA r01, H-04): tipo fuera de la lista cerrada
    [{"ref": "MSG-1", "prioridad": "ALTA", "tipo": "seguimiento"}, {"ref": "MSG-2", "prioridad": "BAJA"}],
    [{"ref": "MSG-1", "tipo": "C6"}],
])
def test_pb19_una_orden_invalida_se_rechaza_sin_tocar_la_cola(ordenes):
    m = Monitor(umbral_cola=3)
    with pytest.raises(ValueError):
        m.encolar("AG-02", ordenes=ordenes)
    assert m.cola["AG-02"] == 0 and m.pendientes["AG-02"] == []


def test_pb19_una_orden_ya_en_la_cola_se_rechaza_y_retirar_la_saca():
    m = Monitor(umbral_cola=3)
    m.encolar("AG-02", ordenes=_seis_ct05())
    with pytest.raises(ValueError):
        m.encolar("AG-02", ordenes=[{"ref": "MSG-9", "prioridad": "ALTA"}, {"ref": "MSG-3", "prioridad": "ALTA"}])
    assert m.cola["AG-02"] == 6 and len(m.pendientes["AG-02"]) == 6
    m.retirar("AG-02", "MSG-3")
    assert m.cola["AG-02"] == 5 and "MSG-3" not in [p["ref"] for p in m.pendientes["AG-02"]]
    with pytest.raises(KeyError):
        m.retirar("AG-02", "MSG-3")
    assert m.cola["AG-02"] == 5


def test_pb19_un_agente_con_estado_nunca_recibe_ord_ni_con_umbral_cero():
    m = Monitor(umbral_cola=0)
    for ag in CON_ESTADO:
        m.encolar(ag, 1)
    salida = m.evaluar_instancias()
    assert sorted(e["agente"] for e in salida) == sorted(CON_ESTADO) and {e["tipo_entrada"] for e in salida} == {"CAR"}
    assert all(m.instancias[ag] == 1 for ag in CON_ESTADO)


# ---------------------------------------------------------------- integración · dos ciclos del Bloque
def test_pb19_dos_ciclos_con_el_analizador_saturado_reordenan_avisan_y_proponen_tipo_3(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    assert b.monitor.umbral_cola == int(parametro(b.cfg, "paralelismo.umbral_cola"))       # el umbral del Anexo A
    b.monitor.encolar("AG-02", ordenes=_seis_ct05())
    r1 = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    ha1 = [e for e in b.almacen.leer("HA") if e.get("run_id") == r1["run_id"]]
    assert not [e for e in ha1 if e["tipo_entrada"] == "ORD" and e.get("agente") == "AG-02"]
    [car1] = _cars(ha1, "AG-02")
    assert [c["ref"] for c in car1["cola_reordenada"]] == ORDEN_ESPERADO and "p3_id" not in car1
    assert [a["id"] for a in avisos_plazos(b.almacen, r1["run_id"])] == [car1["id"]]
    assert not [e for e in b.almacen.leer("HA") if e["tipo_entrada"] == "P3" and e.get("clave") == CLAVE_P3]
    r2 = b.ciclo(str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date()), alcance={"clases": ["RV"]})
    [car2] = _cars([e for e in b.almacen.leer("HA") if e.get("run_id") == r2["run_id"]], "AG-02")
    [p3] = [e for e in b.almacen.leer("HA") if e["tipo_entrada"] == "P3" and e.get("clave") == CLAVE_P3]
    assert car2["p3_id"] == p3["id"] and p3["estado"] == "PENDING_OPERATOR" and p3["run_id"] == r2["run_id"]
    assert p3["evidencia"]["car"] == [car1["id"]] and p3["evidencia"]["run_actual"] == r2["run_id"]


# ---------------------------------------------------------------- r02 · hallazgos de la QA r01
def test_r02_h03_una_fecha_date_se_guarda_en_iso_y_ordena_por_fecha():
    m = Monitor(umbral_cola=0)
    m.encolar("AG-02", ordenes=[{"ref": "A", "fecha_objetivo": "2026-06-12"}, {"ref": "B", "fecha_objetivo": dt.date(2026, 6, 1)},
                                {"ref": "C", "fecha_objetivo": pd.Timestamp("2026-06-05 10:00")}])
    [car] = m.evaluar_instancias()
    assert [(c["ref"], c["fecha_objetivo"]) for c in car["cola_reordenada"]] == [
        ("B", "2026-06-01"), ("C", "2026-06-05"), ("A", "2026-06-12")]


def test_r02_h04_los_tipos_de_la_lista_cerrada_se_admiten():
    m = Monitor(umbral_cola=0)
    m.encolar("AG-02", ordenes=[{"ref": t, "tipo": t} for t in ("SEGUIMIENTO", "AD_HOC", "PROFUNDIZACION", "PERIODICO")])
    [car] = m.evaluar_instancias()
    assert [c["ref"] for c in car["cola_reordenada"]] == ["AD_HOC", "PROFUNDIZACION", "PERIODICO", "SEGUIMIENTO"]


def test_r02_h01_dos_runs_concurrentes_no_duplican_la_p3(tmp_path):
    """Dos `Almacen` sobre la misma carpeta (dos procesos) saturan a la vez tras una saturación previa; sin la transacción,
    los dos leen HA antes de que ninguno escriba y salen dos P3-."""
    _saturar(Almacen(tmp_path), "RUN-2026-0000")
    a, b = Almacen(tmp_path), Almacen(tmp_path)
    barrera = threading.Barrier(2, timeout=3)
    for al in (a, b):
        def estado(archivo, *args, _o=al.estado, **kw):
            r = _o(archivo, *args, **kw)
            if archivo == "HA":
                try:
                    barrera.wait()
                except threading.BrokenBarrierError:
                    pass
            return r
        al.estado = estado
    hilos = [threading.Thread(target=_saturar, args=(al, run)) for al, run in ((a, "RUN-2026-0001"), (b, "RUN-2026-0002"))]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    final = Almacen(tmp_path)
    assert len({e["id"] for e in _p3(final)}) == 1
    cars = [e for e in final.leer("HA") if e["tipo_entrada"] == "CAR"]
    assert len(cars) == 3 and {c.get("p3_id") for c in cars[1:]} == {_p3(final)[0]["id"]}


@pytest.mark.parametrize("estado", ["Rechazada", None, "EN_ESTUDIO", "rechazada"])
def test_r02_h02_un_estado_fuera_del_enum_no_cierra_la_propuesta(tmp_path, estado):
    al = Almacen(tmp_path)
    _saturar(al, "RUN-2026-0001")
    pid = _saturar(al, "RUN-2026-0002")["p3_id"]
    al.escribir("HA", "AG-18", {"tipo_entrada": "P3", "id": pid, "estado": estado})
    assert _saturar(al, "RUN-2026-0003")["p3_id"] == pid and _saturar(al, "RUN-2026-0004")["p3_id"] == pid
    assert len({e["id"] for e in _p3(al)}) == 1


def test_r02_h02_aplicada_cierra_la_propuesta_como_rechazada(tmp_path):
    al = Almacen(tmp_path)
    _saturar(al, "RUN-2026-0001")
    pid = _saturar(al, "RUN-2026-0002")["p3_id"]
    al.escribir("HA", "AG-18", {"tipo_entrada": "P3", "id": pid, "estado": "APLICADA"})
    assert "p3_id" not in _saturar(al, "RUN-2026-0003")
    nueva = _saturar(al, "RUN-2026-0004")["p3_id"]
    assert nueva != pid and len({e["id"] for e in _p3(al)}) == 2


def test_r02_h05_si_el_car_falla_la_p3_no_cita_nada_inexistente_y_sigue_abierta(tmp_path):
    al = Almacen(tmp_path)
    _saturar(al, "RUN-2026-0001")
    orig = al.escribir
    def escribir(archivo, autor, e):
        if e.get("tipo_entrada") == "CAR":
            raise OSError("disco lleno (simulado)")
        return orig(archivo, autor, e)
    al.escribir = escribir
    with pytest.raises(OSError):
        _saturar(al, "RUN-2026-0002")
    al.escribir = orig
    ha = al.leer("HA")
    ids = {e["id"] for e in ha}
    [p3] = _p3(al)
    assert p3["evidencia"]["car"] and all(c in ids for c in p3["evidencia"]["car"])
    car3 = _saturar(al, "RUN-2026-0003")
    assert car3["p3_id"] == p3["id"] and len({e["id"] for e in _p3(al)}) == 1


def test_r02_h06_fin_no_baja_la_cola_por_debajo_del_detalle():
    m = Monitor(umbral_cola=0)
    m.encolar("AG-02", 2)
    m.encolar("AG-02", ordenes=_seis_ct05())
    for _ in range(4):
        m.fin("AG-02", m.inicio("AG-02"))
    assert m.cola["AG-02"] == 6 and m.completados["AG-02"] == 4      # las dos sin detalle salen; las seis con detalle no
    [car] = m.evaluar_instancias()
    assert car["cola"] == len(car["cola_reordenada"]) == 6 and car["aviso_coordinador"]["en_espera_sobre_umbral"] == 6
    m.retirar("AG-02", "MSG-4")
    m.fin("AG-02", m.inicio("AG-02"))
    assert m.cola["AG-02"] == 5
