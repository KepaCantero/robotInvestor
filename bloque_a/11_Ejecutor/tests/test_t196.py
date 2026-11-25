"""T-196 · PB-08, ráfaga de peticiones sin límite (Plan de pruebas V3.0; R5, 7.1, 7.2 y 7.6 del Documento 0 V5.3; prompt del
Coordinador V5.0, 6.1 y 6.3).

Cola de peticiones del Coordinador (`bloque_a/cola_peticiones.py`): todas registradas en F5, ninguna rechazada por número,
servicio por prioridad con envejecimiento, consultas N0 por el carril rápido y presupuesto proporcional por nivel
(INC-T196-01). Los números salen de la configuración (`cola_peticiones`, `presupuesto_uc`): las pruebas los leen de ahí.
"""
import json
import math
import os
import threading
import time

import pandas as pd
import pytest
from bloque_a.cola_peticiones import (
    NIVELES,
    PeticionInvalida,
    objetivo_n0,
    p90,
    presupuesto_por_clase,
)
from bloque_a.configuracion import cargar_config, parametro
from bloque_a.herramientas.ht08_monitor import PRIORIDADES
from conftest import AS_OF, DATOS, nuevo_bloque

from bloque_a import respuesta_final

ZONA = "Europe/Madrid"
T0 = pd.Timestamp(f"{AS_OF}T09:00", tz=ZONA)
PREGUNTA_N0 = "¿Qué opciones hay en el último informe?"
PREGUNTA_ANALITICA = "¿Qué opinas de las divisas frente a la renta fija?"   # el mock la escala (ANALITICA, N2)


def _ct01(prioridad="NORMAL", clases=("DIV",), **kw):
    return {"tipo": kw.pop("tipo", "AD_HOC"), "alcance": {"clases": list(clases)}, "horizontes": ["H2"], "prioridad": prioridad,
            **kw}


def _cfg(b, ruta):
    return parametro(b.cfg, ruta)


def _f5(b, tipo):
    return [e for e in b.almacen.estado("F5").values() if e.get("tipo_entrada") == tipo]


def _pets(b):
    return {e["id"]: e for e in _f5(b, "PETICION")}


class _CicloFalso:
    """Sustituye a `Bloque.ciclo` para medir el orden de servicio de muchas peticiones sin analizar nada."""

    def __init__(self):
        self.llamadas = []

    def __call__(self, as_of, **kw):
        self.llamadas.append(kw)
        return {"run_id": f"RUN-FALSO-{len(self.llamadas)}", "estado": "COMPLETO"}


@pytest.fixture
def b(tmp_path, universo):
    return nuevo_bloque(tmp_path, universo)


# ------------------------------------------------------------------ CA-1, CA-3, CA-4, CA-5 · la ráfaga del plan
def test_pb08_rafaga_del_plan_65_registradas_n0_sin_esperar_y_servicio_por_prioridad(b, monkeypatch):
    b.ciclo(AS_OF, alcance={"clases": ["DIV"]})          # «ciclo periódico en curso»: memoria para las N0
    runs_antes = len(_f5(b, "RUN"))
    prioridades = ["ALTA"] * 5 + ["NORMAL"] * 15 + ["BAJA"] * 5
    orden_ct01 = [prioridades[(7 * i) % 25] for i in range(25)]          # mezcladas (7 es primo con 25)
    assert sorted(orden_ct01) == sorted(prioridades)
    mensajes = [("CT-01", p) for p in orden_ct01] + [("CT-03", "N0" if i % 4 else "ANALITICA") for i in range(40)]
    mensajes = [mensajes[(11 * i) % 65] for i in range(65)]               # intercaladas en 10 minutos
    paso = pd.Timedelta(minutes=10) / 65
    acuses, consultas, tiempos_n0, llegada = [], [], [], []
    for i, (contrato, x) in enumerate(mensajes):
        t = T0 + i * paso
        if contrato == "CT-01":
            r = b.cola.recibir(_ct01(x), t)
            acuses.append(r)
            llegada.append((r["pet_id"], x))
        else:
            t_ini = time.perf_counter()
            q = b.consulta(PREGUNTA_N0 if x == "N0" else PREGUNTA_ANALITICA, as_of=AS_OF, encolar_escalado=True, instante=t)
            if q["ruta"] == "N0":
                tiempos_n0.append(time.perf_counter() - t_ini)
            else:
                llegada.append((q["peticion_cola"], "NORMAL"))
            consultas.append(q)
    # CA-1: las 65 registradas (25 PET- de CT-01, 40 QRY- y una PET- por cada escalado)
    pets, qrys = _pets(b), {e["id"]: e for e in _f5(b, "QRY")}
    escaladas = [q for q in consultas if q["ruta"] == "ANALITICA"]
    assert len([p for p in pets.values() if p["origen"] == "CT-01"]) == 25 and len(qrys) == 40
    assert {q["query_id"] for q in consultas} == set(qrys)
    assert len(escaladas) == 10 and {q["peticion_cola"] for q in escaladas} == {p["id"] for p in pets.values() if p["origen"] == "CT-03"}
    # CA-2: ninguna rechazada; todas en cola
    assert {p["estado"] for p in pets.values()} == {"ENCOLADA"}
    # CA-3: acuse con plazo para cada CT-01; respuesta N0 o provisional con plazo para cada CT-03
    for r in acuses:
        assert r["acuse"]["asignado"] == r["pet_id"] and r["acuse"]["cola"]["plazo_estimado"].startswith("En cola: posición ")
        assert r["acuse"]["nivel"] == "N2" and r["acuse"]["presupuesto_uc"] == _cfg(b, "presupuesto_uc.N2")
    for q in consultas:
        if q["ruta"] == "N0":
            assert q["escalado"] is None and q["referencias"] and q["respuesta"]
        else:
            assert q["escalado"]["run_id"] is None and q["escalado"]["plazo_estimado"].startswith("En cola: posición ")
            assert q["respuesta_final"] is None and q["cola"]["plazo_estimado"] == q["escalado"]["plazo_estimado"]
    # CA-5: las N0 respondidas al recibirse, sin lanzar ningún análisis, y p90 bajo el objetivo (P-21)
    assert len(tiempos_n0) == 30 and len(_f5(b, "RUN")) == runs_antes
    assert p90(tiempos_n0) < objetivo_n0(b.cfg)
    # CA-4: servicio por prioridad (sin espera de una hora, el envejecimiento es 0) y, a igualdad, por llegada
    falso = _CicloFalso()
    monkeypatch.setattr(b, "ciclo", falso)
    servidas = b.cola.atender(T0 + pd.Timedelta(minutes=10))
    base = _cfg(b, "cola_peticiones.prioridad_base")
    esperado = [pid for pid, _ in sorted(llegada, key=lambda x: -base[x[1]])]      # sort estable: llegada a igualdad
    assert [s["pet_id"] for s in servidas] == esperado
    assert [s["orden_servicio"] for s in servidas] == list(range(1, 36))
    assert [c["disparador"]["pet_id"] for c in falso.llamadas] == esperado
    assert {p["estado"] for p in _pets(b).values()} == {"ATENDIDA"}
    # CA-3: cada consulta escalada recibe una sola final al atenderse
    finales = {e["id"]: e for e in _f5(b, "QRY") if e.get("respuesta_final")}
    assert set(finales) == {q["query_id"] for q in escaladas}
    assert all(f["respuesta_final"]["escalado"]["run_id"].startswith("RUN-FALSO-") for f in finales.values())
    assert respuesta_final.enviar_pendientes(b, AS_OF) == []


# ------------------------------------------------------------------ CA-2 · sin límite de número; idempotencia
def test_200_peticiones_en_cola_sin_rechazo_y_un_msg_id_repetido_no_duplica(b):
    for i in range(200):
        r = b.cola.recibir(_ct01("NORMAL"), T0 + pd.Timedelta(seconds=i))
    assert r["cola"]["posicion"] == 200 and r["cola"]["en_cola"] == 200 and r["estado"] == "ENCOLADA"
    assert r["cola"]["uc_por_delante"] == pytest.approx(199 * _cfg(b, "presupuesto_uc.N2"))
    assert len(_pets(b)) == 200 and {p["estado"] for p in _pets(b).values()} == {"ENCOLADA"}
    ct01 = {**_ct01("BAJA"), "msg_id": "MSG-BRK-2026-000001"}
    r1 = b.cola.recibir(ct01, T0 + pd.Timedelta(minutes=5))
    r2 = b.cola.recibir(ct01, T0 + pd.Timedelta(minutes=6))
    assert r2["pet_id"] == r1["pet_id"] and r2["acuse"]["repetido"] is True and r1["acuse"]["repetido"] is False
    assert len(_pets(b)) == 201


# ------------------------------------------------------------------ CA-4 · prioridad efectiva
def test_prioridad_efectiva_base_envejecimiento_y_su_maximo(b):
    pid = b.cola.recibir(_ct01("BAJA"), T0)["pet_id"]
    pet = _pets(b)[pid]
    base, por_hora, maximo = (_cfg(b, "cola_peticiones.prioridad_base.BAJA"), _cfg(b, "cola_peticiones.envejecimiento_por_hora"),
                              _cfg(b, "cola_peticiones.envejecimiento_max"))
    for horas, env in [(0, 0), (0.99, 0), (1, por_hora), (2.5, 2 * por_hora), (maximo / por_hora, maximo), (1000, maximo)]:
        p = b.cola.prioridad(pet, T0 + pd.Timedelta(hours=horas))
        assert (p["base"], p["envejecimiento"], p["urgencia"], p["efectiva"]) == (base, env, 0, base + env), horas


def test_una_baja_que_espera_alcanza_a_una_normal_recien_llegada(b):
    base = _cfg(b, "cola_peticiones.prioridad_base")
    horas = math.ceil((base["NORMAL"] - base["BAJA"]) / _cfg(b, "cola_peticiones.envejecimiento_por_hora"))   # 10 h
    assert horas <= _cfg(b, "cola_peticiones.envejecimiento_max")
    baja = b.cola.recibir(_ct01("BAJA"), T0)["pet_id"]
    normal = b.cola.recibir(_ct01("NORMAL"), T0 + pd.Timedelta(hours=horas) - pd.Timedelta(minutes=30))["pet_id"]   # sin envejecer
    antes = T0 + pd.Timedelta(hours=horas) - pd.Timedelta(minutes=1)      # la BAJA aún no ha alcanzado
    assert [p["id"] for p in b.cola.orden(antes)] == [normal, baja]
    alcanza = T0 + pd.Timedelta(hours=horas)                               # empate: mismo nivel; la BAJA llegó antes
    assert [p["id"] for p in b.cola.orden(alcanza)] == [baja, normal]
    assert b.cola.orden(alcanza)[0]["_prioridad"]["efectiva"] == b.cola.orden(alcanza)[1]["_prioridad"]["efectiva"]


def test_la_urgencia_por_fecha_objetivo_cercana_adelanta_la_peticion(b):
    margen = _cfg(b, "cola_peticiones.urgencia_margen_h")
    lejos = b.cola.recibir(_ct01("NORMAL", fecha_objetivo="2026-06-20T07:00"), T0)["pet_id"]
    sin = b.cola.recibir(_ct01("NORMAL"), T0 + pd.Timedelta(minutes=1))["pet_id"]
    fo = (T0 + pd.Timedelta(hours=margen) + pd.Timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M")
    cerca = b.cola.recibir(_ct01("NORMAL", fecha_objetivo=fo), T0 + pd.Timedelta(minutes=2))["pet_id"]
    assert [p["id"] for p in b.cola.orden(T0 + pd.Timedelta(minutes=5))] == [lejos, sin, cerca]    # margen > urgencia_margen_h
    t = T0 + pd.Timedelta(hours=1)                                                                  # margen 1 h 30 < 2 h
    orden = b.cola.orden(t)
    assert [p["id"] for p in orden] == [cerca, lejos, sin]
    assert orden[0]["_prioridad"]["urgencia"] == _cfg(b, "cola_peticiones.urgencia_puntos")
    vencida = b.cola.orden(T0 + pd.Timedelta(hours=10))[0]                                         # pasada la fecha, sigue urgente
    assert vencida["id"] == cerca and vencida["_prioridad"]["urgencia"] > 0
    en_el_margen = T0 + pd.Timedelta(minutes=30)                                                    # margen justo de 2 h: no
    assert b.cola.prioridad(_pets(b)[cerca], en_el_margen)["urgencia"] == 0
    assert b.cola.prioridad(_pets(b)[cerca], en_el_margen + pd.Timedelta(seconds=1))["urgencia"] > 0


def test_desempate_por_nivel_menor_y_despues_por_llegada(b):
    n3 = b.cola.recibir(_ct01("NORMAL", nivel_forzado="N3"), T0)["pet_id"]
    n2a = b.cola.recibir(_ct01("NORMAL"), T0 + pd.Timedelta(seconds=1))["pet_id"]
    n1 = b.cola.recibir(_ct01("NORMAL", nivel_forzado="N1"), T0 + pd.Timedelta(seconds=2))["pet_id"]
    n2b = b.cola.recibir(_ct01("NORMAL"), T0 + pd.Timedelta(seconds=3))["pet_id"]
    alta = b.cola.recibir(_ct01("ALTA", nivel_forzado="N3"), T0 + pd.Timedelta(seconds=4))["pet_id"]
    assert [p["id"] for p in b.cola.orden(T0 + pd.Timedelta(minutes=1))] == [alta, n1, n2a, n2b, n3]


# ------------------------------------------------------------------ CA-6 · presupuesto proporcional por nivel
def test_presupuesto_proporcional_por_nivel_igual_que_el_ciclo(b):
    clases = ["DIV", "RF"]
    casos = [(_ct01("NORMAL", clases, nivel_forzado="N1"), "N1"), (_ct01("NORMAL", clases), "N2"),
             (_ct01("NORMAL", clases, tipo="PROFUNDIZACION"), "N3")]
    tope = _cfg(b, "presupuesto_uc.ciclo_semanal_max")
    for i, (ct01, nivel) in enumerate(casos):
        r = b.cola.recibir(ct01, T0 + pd.Timedelta(seconds=i))
        pet = _pets(b)[r["pet_id"]]
        assert pet["nivel"] == nivel == r["acuse"]["nivel"]
        por_tipo = _cfg(b, f"presupuesto_uc.{nivel}")
        esperado = {c: por_tipo / len(clases) for c in clases} if nivel == "N3" else {c: por_tipo for c in clases}
        assert pet["presupuesto_por_clase"] == esperado and pet["presupuesto_uc"] == sum(esperado.values())
        reparto = b._reparto(pet["tipo"], clases, {c: nivel for c in clases}, None, tope)
        assert {c: reparto[c] for c in clases} == pet["presupuesto_por_clase"]
    assert presupuesto_por_clase(b.cfg, "PERIODICO", ["DIV"], {"DIV": "N3"}) == {"DIV": _cfg(b, "presupuesto_uc.N3")}


# ------------------------------------------------------------------ CA-3, CA-6, CA-7 · servicio real con el ciclo simulado
def test_servicio_real_de_un_ct01_y_de_una_consulta_escalada_con_su_final(b):
    baja = b.cola.recibir(_ct01("BAJA", nivel_forzado="N1"), T0)["pet_id"]
    q = b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, encolar_escalado=True, instante=T0 + pd.Timedelta(minutes=1))
    assert q["ruta"] == "ANALITICA" and q["peticion_cola"] in _pets(b)
    assert respuesta_final.enviar_pendientes(b, AS_OF) == []                     # en cola: ninguna final todavía
    servidas = b.cola.atender(T0 + pd.Timedelta(minutes=2))
    assert [s["pet_id"] for s in servidas] == [q["peticion_cola"], baja]          # NORMAL antes que BAJA
    f5 = b.almacen.estado("F5")
    for s in servidas:
        pet, run = f5[s["pet_id"]], f5[s["run_id"]]
        assert pet["estado"] == "ATENDIDA" and pet["run_id"] == s["run_id"] and run["tipo_entrada"] == "RUN"
        assert pet["estado_run"] == run["estado"] == s["estado_run"]                 # r02 (H-08)
        assert run["disparador"]["pet_id"] == s["pet_id"] and run["disparador"]["origen"] == pet["origen"]
        assert set(run["nivel_por_clase"].values()) == {pet["nivel"]} and set(run["nivel_por_clase"]) == set(pet["clases"])
        assert [h["tipo"] for h in pet["_historial"]] == ["PETICION"] * 3
    final = servidas[0]["respuesta_final"]
    assert final["repetido"] is False and final["run_id"] == servidas[0]["run_id"]
    assert final["escalado"]["run_id"] == servidas[0]["run_id"] and final["respuesta_final"]["provisional_msg_id"] == q["msg_id"]
    respuesta_final.validar({k: final[k] for k in respuesta_final.ESQUEMA["required"]}, final["estado"])   # jsonschema
    assert f5[q["query_id"]]["respuesta_final"]["msg_id"] == final["msg_id"]
    assert b.cola.atender(T0 + pd.Timedelta(minutes=3)) == []                    # la cola queda vacía


def test_la_final_pendiente_de_una_consulta_atendida_otro_dia_cita_su_run(b, monkeypatch):
    """Si la final no sale al atender (corte justo después), `enviar_pendientes` la envía con la fecha en que se atendió: la
    del RUN-, no la de la consulta (que no vería el RUN- en F5)."""
    import bloque_a.cola_peticiones as cp
    q = b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, encolar_escalado=True, instante=T0)

    class _Corte:
        @staticmethod
        def enviar(*a, **k):
            raise RuntimeError("corte antes de la final")
    monkeypatch.setattr(cp, "respuesta_final", _Corte)
    with pytest.raises(RuntimeError):
        b.cola.atender(T0 + pd.Timedelta(days=1))
    monkeypatch.undo()
    pet = _pets(b)[q["peticion_cola"]]
    assert pet["estado"] == "ATENDIDA" and pet["run_id"]
    [final] = respuesta_final.enviar_pendientes(b)
    assert final["run_id"] == pet["run_id"] and final["escalado"]["run_id"] == pet["run_id"]
    assert final["respuesta_final"]["resultado_analisis"] != "SIN_ENTREGA" or "no consta" not in final["respuesta"]


# ------------------------------------------------------------------ CA-7 · fallo del ciclo
@pytest.mark.parametrize("error", [RuntimeError, KeyboardInterrupt])   # r02 (H-08): también lo que no es Exception
def test_un_ciclo_que_falla_deja_fallida_incidencia_y_el_resto_encolado(b, monkeypatch, error):
    q = b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, encolar_escalado=True, instante=T0)
    otra = b.cola.recibir(_ct01("BAJA"), T0 + pd.Timedelta(minutes=1))["pet_id"]

    def _falla(as_of, **kw):   # r02 (H-08): el ciclo ya había escrito su RUN- cuando falla
        b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "RUN", "id": "RUN-2026-0999", "disparador": kw["disparador"]})
        raise error("datos con texto sensible")
    monkeypatch.setattr(b, "ciclo", _falla)
    with pytest.raises(error):
        b.cola.atender(T0 + pd.Timedelta(minutes=2))
    pets = _pets(b)
    assert pets[q["peticion_cola"]]["estado"] == "FALLIDA" and pets[q["peticion_cola"]]["error"] == error.__name__
    assert pets[q["peticion_cola"]]["run_id"] == "RUN-2026-0999"
    assert pets[otra]["estado"] == "ENCOLADA"
    inc = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and q["peticion_cola"] in e.get("detalle", "")]
    assert len(inc) == 1 and inc[0]["tipo"] == "HERRAMIENTA" and "sensible" not in json.dumps(inc, ensure_ascii=False)
    qry = b.almacen.estado("F5")[q["query_id"]]
    assert qry["escalado"]["estado_run"] == "FALLIDO" and qry["fallo_analisis"] == error.__name__
    assert qry["escalado"]["run_id"] == "RUN-2026-0999"
    [final] = respuesta_final.enviar_pendientes(b, AS_OF)                         # la final FALLIDO sale después
    assert final["respuesta_final"]["resultado_analisis"] == "FALLIDO" and final["estado"] == "SIN_RESULTADO"


# ------------------------------------------------------------------ CA-7 · concurrencia de las tomas
def test_dos_bloques_y_varios_hilos_nunca_toman_la_misma_peticion(tmp_path, universo):
    b1 = nuevo_bloque(tmp_path, universo)
    ids = [b1.cola.recibir(_ct01(PRIORIDADES[i % 3]), T0 + pd.Timedelta(seconds=i))["pet_id"] for i in range(12)]
    b2 = nuevo_bloque(tmp_path, universo)                                         # otra instancia sobre el mismo almacén
    tomadas, errores = [], []

    def _trabajo(bloque):
        try:
            while (p := bloque.cola.tomar(T0 + pd.Timedelta(minutes=1))) is not None:
                tomadas.append(p["id"])
        except Exception as e:   # noqa: BLE001 — la prueba cuenta cualquier error del hilo
            errores.append(e)
    hilos = [threading.Thread(target=_trabajo, args=(bb,)) for bb in (b1, b2, b1, b2)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    assert not errores and sorted(tomadas) == sorted(ids) and len(set(tomadas)) == 12
    assert {p["estado"] for p in _pets(b1).values()} == {"EN_CURSO"}


# ------------------------------------------------------------------ CA-8 · falla cerrado
INVALIDOS = [
    {"prioridad": "URGENTE"}, {"prioridad": None}, {"tipo": "SEGUIMIENTO"}, {"nivel_forzado": "N0"}, {"nivel_forzado": "N4"},
    {"fecha_objetivo": "2026-06-08"}, {"fecha_objetivo": "2026-02-30T10:00"}, {"fecha_objetivo": "mañana"},
    {"fecha_objetivo": 20260608}, {"alcance": ["DIV"]},
]


@pytest.mark.parametrize("cambio", INVALIDOS, ids=lambda c: json.dumps(c, ensure_ascii=False))
def test_un_ct01_invalido_se_rechaza_sin_escribir_nada(b, cambio):
    antes = (len(b.almacen.leer("F5")), b.mensajeria.registro[:])
    with pytest.raises(PeticionInvalida):
        b.cola.recibir({**_ct01(), **cambio}, T0)
    assert (len(b.almacen.leer("F5")), b.mensajeria.registro) == antes


@pytest.mark.parametrize("instante", ["2026-06-05", None, "ayer", 5, pd.NaT, "2026-06-05T25:00",
                                      "2026-03-29T02:30", "2026-10-25T02:30"])                     # r02 (H-05): cambio de hora
def test_un_instante_invalido_se_rechaza(b, instante):
    with pytest.raises(PeticionInvalida):
        b.cola.recibir(_ct01(), instante)
    with pytest.raises(PeticionInvalida):
        b.cola.atender(instante)
    assert _f5(b, "PETICION") == []


def test_un_instante_anterior_a_una_recepcion_no_ordena_ni_sirve(b):
    """r02 (H-01): antes de su recepción la petición aún no ha llegado: no se ve ni se sirve (no es un error de la cola); la
    prioridad de esa petición en ese instante sí se rechaza."""
    pid = b.cola.recibir(_ct01(), T0)["pet_id"]
    antes = T0 - pd.Timedelta(seconds=1)
    assert b.cola.orden(antes) == [] and b.cola.atender(antes) == []
    with pytest.raises(PeticionInvalida):
        b.cola.prioridad(_pets(b)[pid], antes)
    assert {p["estado"] for p in _pets(b).values()} == {"ENCOLADA"}


@pytest.mark.parametrize("maximo", [0, -1, True, "2", 1.5])
def test_maximo_invalido_se_rechaza(b, maximo):
    b.cola.recibir(_ct01(), T0)
    with pytest.raises(PeticionInvalida):
        b.cola.atender(T0, maximo)
    assert {p["estado"] for p in _pets(b).values()} == {"ENCOLADA"}


def test_maximo_limita_las_servidas(b, monkeypatch):
    for i in range(3):
        b.cola.recibir(_ct01(), T0 + pd.Timedelta(seconds=i))
    monkeypatch.setattr(b, "ciclo", _CicloFalso())
    assert len(b.cola.atender(T0 + pd.Timedelta(minutes=1), 2)) == 2
    assert sorted(p["estado"] for p in _pets(b).values()) == ["ATENDIDA", "ATENDIDA", "ENCOLADA"]


def test_consulta_en_cola_con_urgencia_desconocida_o_sin_escalado_se_rechaza_sin_escribir(b):
    n, registro = len(b.almacen.leer("F5")), b.mensajeria.registro[:]
    with pytest.raises(PeticionInvalida):
        b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, urgencia="MUY_URGENTE", encolar_escalado=True, instante=T0)
    assert b.mensajeria.registro == registro          # antes de crear el CT-03 y de llamar al modelo
    with pytest.raises(PeticionInvalida):
        b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, encolar_escalado=True, ejecutar_escalado=False, instante=T0)
    assert len(b.almacen.leer("F5")) == n


def test_la_final_de_una_consulta_en_cola_no_sale_y_sin_pet_si(b):
    q = b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, encolar_escalado=True, instante=T0)
    with pytest.raises(respuesta_final.RespuestaFinalInvalida):
        respuesta_final.enviar(b, q["query_id"], None, AS_OF)
    assert respuesta_final.enviar_pendientes(b, AS_OF) == [] and not b.almacen.estado("F5")[q["query_id"]].get("respuesta_final")
    assert b.cola.tomar(T0) is not None                                           # EN_CURSO: tampoco sale
    assert respuesta_final.enviar_pendientes(b, AS_OF) == []
    assert respuesta_final.consulta_en_cola(b.almacen, {"peticion_cola": "PET-2026-9999"}) is False   # sin PET-: no en cola
    assert respuesta_final.consulta_en_cola(b.almacen, {}) is False


def test_la_consulta_urgente_escala_con_prioridad_alta(b):
    mapa = _cfg(b, "cola_peticiones.prioridad_consulta")
    q = b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, urgencia="INMEDIATA", encolar_escalado=True, instante=T0)
    pet = _pets(b)[q["peticion_cola"]]
    assert pet["prioridad"] == mapa["INMEDIATA"] and pet["origen"] == "CT-03" and pet["qry_id"] == q["query_id"]
    assert pet["nivel"] in NIVELES and pet["nivel"] == q["escalado"]["nivel"]


# ------------------------------------------------------------------ CA-9 · regresión: lo de siempre no cambia
def test_por_defecto_la_consulta_y_la_peticion_siguen_atendiendose_en_el_momento(b):
    q = b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, ejecutar_escalado=False)
    assert q["escalado"]["plazo_estimado"] == "mismo día (ejecución síncrona del ejecutor)" and "peticion_cola" not in q
    assert q["respuesta_final"]["respuesta_final"]["resultado_analisis"] == "NO_EJECUTADO"
    assert _f5(b, "PETICION") == [] and "peticion_cola" not in b.almacen.estado("F5")[q["query_id"]]


def test_la_configuracion_por_defecto_tiene_los_numeros_de_la_cola():
    cfg = cargar_config()
    assert set(parametro(cfg, "cola_peticiones.prioridad_base")) == set(PRIORIDADES)
    assert objetivo_n0(cfg) == 120                       # Anexo A, P-21: «< 2 minutos»
    assert set(parametro(cfg, "cola_peticiones.prioridad_consulta")) == {"INMEDIATA", "NORMAL"}


def test_p90_por_rango_mas_proximo():
    assert p90(list(range(1, 11))) == 9 and p90([5]) == 5 and p90([3, 1, 2]) == 3
    with pytest.raises(ValueError):
        p90([])


# ------------------------------------------------------------------ CLI
def test_cli_encola_y_atiende(tmp_path, capsys):
    from bloque_a.cli import main as cli_main
    sal = tmp_path / "sal"
    pet = tmp_path / "pet.json"
    pet.write_text(json.dumps(_ct01("ALTA")), encoding="utf-8")
    comun = ["--datos", str(DATOS), "--estado", str(sal / "estado"), "--salida", str(sal)]
    assert cli_main([*comun, "peticion", "--json", str(pet), "--encolar", "--instante", f"{AS_OF}T09:00"]) == 0
    r = json.loads(capsys.readouterr().out)
    assert r["estado"] == "ENCOLADA" and r["acuse"]["cola"]["posicion"] == 1
    assert cli_main([*comun, "atender-cola", "--instante", f"{AS_OF}T09:05", "--maximo", "1"]) == 0
    salida = json.loads(capsys.readouterr().out)
    [s] = salida["servidas"]
    assert s["pet_id"] == r["pet_id"] and s["run_id"].startswith("RUN-") and salida["huerfanas"] == []


# ------------------------------------------------------------------ r02 (QA r01)
@pytest.mark.parametrize("con_reloj", [False, True])
def test_atender_no_se_corta_si_llega_una_peticion_durante_el_servicio(b, monkeypatch, con_reloj):
    """H-01: con un instante fijo, la que llega después no se ve todavía (queda ENCOLADA) y las demás se sirven; con un reloj,
    cada toma usa un instante nuevo y la nueva se sirve en la misma pasada."""
    antes = [b.cola.recibir(_ct01(), T0 + pd.Timedelta(seconds=i))["pet_id"] for i in range(3)]
    t_serv = T0 + pd.Timedelta(minutes=1)
    nuevas = []

    def _lento(as_of, **kw):
        if not nuevas:   # otro proceso recibe un CT-01 mientras se analiza la primera
            nuevas.append(b.cola.recibir(_ct01("ALTA"), t_serv + pd.Timedelta(minutes=5))["pet_id"])
        return {"run_id": f"RUN-FALSO-{kw['disparador']['pet_id']}", "estado": "COMPLETO"}
    monkeypatch.setattr(b, "ciclo", _lento)
    ahora = iter([t_serv, t_serv] + [t_serv + pd.Timedelta(minutes=10)] * 10)   # validación, 1.ª toma, las siguientes
    servidas = b.cola.atender((lambda: next(ahora)) if con_reloj else t_serv)
    pets = _pets(b)
    assert {pets[p]["estado"] for p in antes} == {"ATENDIDA"}
    if con_reloj:
        assert [s["pet_id"] for s in servidas] == [antes[0], nuevas[0], *antes[1:]]   # la ALTA nueva, en la toma siguiente
    else:
        assert len(servidas) == 3 and pets[nuevas[0]]["estado"] == "ENCOLADA"
        b.cola.atender(t_serv + pd.Timedelta(minutes=6))                           # se sirve en la pasada siguiente
        assert _pets(b)[nuevas[0]]["estado"] == "ATENDIDA"


def test_un_ct01_con_instante_anterior_a_otra_peticion_se_encola(b):
    """H-02 (A1): una entrega fuera de orden no se rechaza, y su msg_id del Broker no queda bloqueado."""
    primera = b.cola.recibir(_ct01(), T0 + pd.Timedelta(seconds=2))["pet_id"]
    ct01 = {**_ct01("ALTA"), "msg_id": "MSG-BRK-2026-000777"}
    r = b.cola.recibir(ct01, T0 + pd.Timedelta(seconds=1))
    assert r["estado"] == "ENCOLADA" and r["cola"]["posicion"] == 1 and r["cola"]["en_cola"] == 1   # la otra aún no había llegado
    r2 = b.cola.recibir(ct01, T0 + pd.Timedelta(seconds=3))
    assert r2["pet_id"] == r["pet_id"] and r2["acuse"]["repetido"] is True
    assert [p["id"] for p in b.cola.orden(T0 + pd.Timedelta(seconds=5))] == [r["pet_id"], primera]


def test_la_consulta_encolada_no_pierde_su_peticion_si_entra_otra_mientras_responde(b, monkeypatch):
    """H-02 (A3): otro CT-01, con un instante posterior, registrado mientras la consulta escribe su provisional."""
    original = respuesta_final.registrar_provisional

    def _con_carrera(*a, **k):
        r = original(*a, **k)
        b.cola.recibir(_ct01("BAJA"), T0 + pd.Timedelta(seconds=30))
        return r
    monkeypatch.setattr(respuesta_final, "registrar_provisional", _con_carrera)
    q = b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, encolar_escalado=True, instante=T0)
    monkeypatch.undo()
    assert q["peticion_cola"] in _pets(b) and _pets(b)[q["peticion_cola"]]["estado"] == "ENCOLADA"
    monkeypatch.setattr(b, "ciclo", _CicloFalso())
    servidas = b.cola.atender(T0 + pd.Timedelta(minutes=1))
    assert servidas[0]["pet_id"] == q["peticion_cola"] and servidas[0]["respuesta_final"]["repetido"] is False


def test_un_instante_con_nanosegundos_se_trunca_y_el_msg_id_no_queda_bloqueado(b):
    """H-04 (A5): los nanosegundos se truncan a microsegundos antes de reservar nada; la `recibida` guardada se vuelve a leer
    y el reintento con el mismo msg_id recupera la misma petición."""
    ct01 = {**_ct01(), "msg_id": "MSG-BRK-2026-000888"}
    r = b.cola.recibir(ct01, pd.Timestamp("2026-06-05T09:00:00.123456789", tz=ZONA))
    pet = _pets(b)[r["pet_id"]]
    assert pet["recibida"] == "2026-06-05T09:00:00.123456+02:00" and b.cola.orden(T0 + pd.Timedelta(minutes=1))[0]["id"] == pet["id"]
    r2 = b.cola.recibir(ct01, T0 + pd.Timedelta(minutes=1))
    assert r2["pet_id"] == r["pet_id"] and r2["acuse"]["repetido"] is True


def test_un_ct01_sin_clases_activas_se_rechaza_sin_escribir(b):
    """H-07 (A8): sin ninguna clase activa no hay presupuesto proporcional; se rechaza antes de crear el mensaje."""
    antes = (len(b.almacen.leer("F5")), b.mensajeria.registro[:])
    for clases in (("XXX",), ("XXX", "ZZZ")):
        with pytest.raises(PeticionInvalida):
            b.cola.recibir(_ct01(clases=clases), T0)
    assert (len(b.almacen.leer("F5")), b.mensajeria.registro) == antes
    r = b.cola.recibir(_ct01(clases=("XXX", "DIV")), T0)
    assert r["clases"] == ["DIV"] and r["presupuesto_uc"] == _cfg(b, "presupuesto_uc.N2")


def test_un_ct01_periodico_se_encola_como_ad_hoc(b):
    """H-09 (R2): como `Bloque.peticion`, un CT-01 PERIODICO es un AD_HOC (y el N3 se reparte entre sus tipos)."""
    r = b.cola.recibir(_ct01("NORMAL", ("DIV", "RF"), tipo="PERIODICO", nivel_forzado="N3"), T0)
    pet = _pets(b)[r["pet_id"]]
    assert pet["tipo"] == "AD_HOC"
    assert pet["presupuesto_por_clase"] == {c: _cfg(b, "presupuesto_uc.N3") / 2 for c in ("DIV", "RF")}


def test_la_consulta_encolada_es_del_dia_de_su_instante(b):
    """H-09 (R9): con `as_of` de otro día, la QRY- y la PET- son del día del instante de recepción."""
    otro = pd.Timestamp(AS_OF) - pd.Timedelta(days=3)
    q = b.consulta(PREGUNTA_ANALITICA, as_of=otro, encolar_escalado=True, instante=T0)
    f5 = b.almacen.estado("F5")
    assert f5[q["query_id"]]["_historial"][0]["fecha"] == AS_OF
    assert f5[q["peticion_cola"]]["_historial"][0]["fecha"] == AS_OF and f5[q["peticion_cola"]]["recibida"] == T0.isoformat()


def test_cli_consulta_encolada_y_su_final_al_atender(tmp_path, capsys):
    """H-09 (R10): `consulta --encolar-escalado --instante` encola el análisis con ese instante; `atender-cola` envía la final."""
    from bloque_a.cli import main as cli_main
    sal = tmp_path / "sal"
    comun = ["--datos", str(DATOS), "--estado", str(sal / "estado"), "--salida", str(sal)]
    assert cli_main([*comun, "consulta", PREGUNTA_ANALITICA, "--encolar-escalado", "--instante", f"{AS_OF}T09:00"]) == 0
    q = json.loads(capsys.readouterr().out)
    assert q["ruta"] == "ANALITICA" and q["peticion_cola"].startswith("PET-") and q["respuesta_final"] is None
    assert cli_main([*comun, "atender-cola", "--instante", f"{AS_OF}T09:05"]) == 0
    [s] = json.loads(capsys.readouterr().out)["servidas"]
    assert s["pet_id"] == q["peticion_cola"] and s["respuesta_final"]["respuesta_final"]["provisional_msg_id"] == q["msg_id"]
    from bloque_a.almacen import Almacen
    assert Almacen(sal / "estado").estado("F5")[q["peticion_cola"]]["recibida"] == f"{AS_OF}T09:00:00+02:00"


def test_tomar_y_servir_y_lo_tomado_sin_servir_es_huerfano(b, monkeypatch):
    """H-06 (A6): lo tomado se sirve con `servir`; si no se sirve, `atender` avisa (una incidencia, una sola vez)."""
    monkeypatch.setattr(b, "ciclo", _CicloFalso())
    uno = b.cola.recibir(_ct01(), T0)["pet_id"]
    dos = b.cola.recibir(_ct01(), T0 + pd.Timedelta(seconds=1))["pet_id"]
    pet = b.cola.tomar(T0 + pd.Timedelta(minutes=1))
    assert pet["id"] == uno and b.cola.servir(pet, T0 + pd.Timedelta(minutes=1))["pet_id"] == uno
    with pytest.raises(PeticionInvalida):                                         # ya no está EN_CURSO
        b.cola.servir(pet, T0 + pd.Timedelta(minutes=1))
    b.cola.tomar(T0 + pd.Timedelta(minutes=2))                                     # tomada y no servida
    for _ in range(2):
        assert b.cola.atender(T0 + pd.Timedelta(minutes=3)) == [] and b.cola.huerfanas() == [dos]
    inc = [e for e in b.almacen.leer("HA") if e.get("peticion_huerfana") == dos]
    assert len(inc) == 1 and inc[0]["severidad"] == "Operativa"


_HIJO = """
import os, signal, sys
sys.path.insert(0, "tests")
import pandas as pd
from conftest import nuevo_bloque
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import cargar_universo
b = nuevo_bloque(sys.argv[1], cargar_universo(RUTA_UNIVERSO_EJEMPLO))
b.cola._tomar(pd.Timestamp(sys.argv[2]), 1, en_marcha=True)   # empieza a servirla…
os.kill(os.getpid(), signal.SIGKILL)                           # …y el proceso muere en pleno ciclo
"""


def test_peticion_en_curso_de_un_proceso_muerto_deja_una_incidencia_y_se_reconcilia(tmp_path, universo):
    """H-03 (A7): una PET- EN_CURSO de un proceso muerto deja una incidencia Operativa (una sola vez, sin tocarla); tras
    `reconciliar`, FALLIDA y la final FALLIDO de su consulta."""
    import subprocess
    import sys
    from pathlib import Path
    b = nuevo_bloque(tmp_path, universo)
    q = b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, encolar_escalado=True, instante=T0)
    pid = q["peticion_cola"]
    with pytest.raises(PeticionInvalida):                                          # ENCOLADA: no es huérfana
        b.cola.reconciliar(pid, "prueba", T0)
    r = subprocess.run([sys.executable, "-c", _HIJO, str(tmp_path), (T0 + pd.Timedelta(minutes=1)).isoformat()],
                       cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, check=False)
    assert r.returncode != 0
    b2 = nuevo_bloque(tmp_path, universo)
    assert b2.almacen.estado("F5")[pid]["estado"] == "EN_CURSO" and b2.almacen.estado("F5")[pid]["pid"] != os.getpid()
    assert respuesta_final.enviar_pendientes(b2, AS_OF) == []                       # la final no sale sola…
    assert [e["peticion_huerfana"] for e in b2.almacen.leer("HA") if e.get("peticion_huerfana")] == [pid]   # …pero avisa
    assert b2.cola.atender(T0 + pd.Timedelta(days=3)) == []                         # …ni se sirve otra vez
    inc = [e for e in b2.almacen.leer("HA") if e.get("peticion_huerfana") == pid]
    assert len(inc) == 1 and inc[0]["severidad"] == "Operativa" and b2.almacen.estado("F5")[pid]["estado"] == "EN_CURSO"
    with pytest.raises(PeticionInvalida):
        b2.cola.reconciliar(pid, "  ", T0 + pd.Timedelta(days=3))
    b3 = nuevo_bloque(tmp_path, universo)                     # el operador, en otra sesión: el reloj del bloque, sin fijar
    rec = b3.cola.reconciliar(pid, "proceso caído; revisado F5", T0 + pd.Timedelta(days=3))
    assert rec["estado"] == "FALLIDA" and b3.almacen.estado("F5")[pid]["error"] == "PROCESO_TERMINADO"
    assert rec["respuesta_final"]["respuesta_final"]["resultado_analisis"] == "FALLIDO"
    assert b3.cola.huerfanas() == [] and respuesta_final.enviar_pendientes(b3) == []          # una sola final


def test_recepciones_concurrentes_dan_posiciones_distintas(tmp_path, universo):
    """R7 del revisor: la posición del plazo y la escritura de la PET- van en una transacción; cuatro instancias del almacén
    que reciben a la vez (con el mismo instante) nunca comunican la misma posición."""
    bloques = [nuevo_bloque(tmp_path, universo) for _ in range(4)]
    for bb in bloques:   # la tabla de acuses se crea antes (su ALTER TABLE inicial no es concurrente; fuera de T-196)
        bb.mensajeria._acuses().close()
    posiciones, errores = [], []

    def _recibe(bb):
        try:
            for _ in range(12):
                posiciones.append(bb.cola.recibir(_ct01(), T0)["cola"]["posicion"])
        except Exception as e:   # noqa: BLE001 — la prueba cuenta cualquier error del hilo
            errores.append(e)
    hilos = [threading.Thread(target=_recibe, args=(bb,)) for bb in bloques]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    assert not errores and sorted(posiciones) == list(range(1, 49))


# ------------------------------------------------------------------ r03 (QA r02)
def test_una_peticion_en_servicio_no_es_huerfana_hasta_quedar_atendida(b, monkeypatch):
    """N-01 (B1): entre el fin del ciclo y la ATENDIDA, otro hilo no la ve como huérfana ni puede reconciliarla."""
    q = b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, encolar_escalado=True, instante=T0)
    pid = q["peticion_cola"]
    monkeypatch.setattr(b, "ciclo", _CicloFalso())
    vistas = {}
    original = b.cola._escalado

    def _con_otro_hilo(*a, **k):
        def _otro():
            vistas["huerfanas"] = b.cola.huerfanas()
            try:
                b.cola.reconciliar(pid, "prueba", T0 + pd.Timedelta(minutes=2))
                vistas["reconciliar"] = "aceptada"
            except PeticionInvalida:
                vistas["reconciliar"] = "rechazada"
        h = threading.Thread(target=_otro)
        h.start()
        h.join()
        return original(*a, **k)
    monkeypatch.setattr(b.cola, "_escalado", _con_otro_hilo)
    [s] = b.cola.atender(T0 + pd.Timedelta(minutes=1))
    assert vistas == {"huerfanas": [], "reconciliar": "rechazada"}
    qry = b.almacen.estado("F5")[q["query_id"]]
    assert _pets(b)[pid]["estado"] == "ATENDIDA" and qry["escalado"]["estado_run"] == "COMPLETO"
    assert s["respuesta_final"]["respuesta_final"]["resultado_analisis"] != "FALLIDO"
    assert not [e for e in b.almacen.leer("HA") if e.get("peticion_huerfana") == pid]
    assert b.cola.huerfanas() == []                                                 # y al terminar, tampoco


@pytest.mark.parametrize("minutos, atendidas", [
    ((10, 10, 0.5, 11), 1),   # retrocede por debajo del primer instante (B5)
    ((10, 10, 12, 11), 2),    # cierre (M-01): sube y baja sin pasar por debajo del primero; cuenta la toma anterior
])
def test_atender_con_un_reloj_que_retrocede_falla_cerrado(b, monkeypatch, minutos, atendidas):
    """N-02 (B5): si el reloj devuelve un instante anterior al de la toma anterior, `atender` lanza y no toma nada más."""
    for i in range(3):
        b.cola.recibir(_ct01(), T0 + pd.Timedelta(minutes=i))
    monkeypatch.setattr(b, "ciclo", _CicloFalso())
    tiempos = iter([T0 + pd.Timedelta(minutes=m) for m in minutos])
    with pytest.raises(PeticionInvalida):
        b.cola.atender(lambda: next(tiempos))
    assert sorted(p["estado"] for p in _pets(b).values()) == ["ATENDIDA"] * atendidas + ["ENCOLADA"] * (3 - atendidas)


def _en_curso_ajena(b, pet_id, **proceso):
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "PETICION", "id": pet_id, "estado": "EN_CURSO", **proceso})


def _pid_muerto():
    import subprocess
    import sys
    p = subprocess.run([sys.executable, "-c", "import os; print(os.getpid())"], capture_output=True, text=True, check=True)
    return int(p.stdout)


def test_una_en_curso_de_otra_maquina_no_es_huerfana(b):
    """N-04 (Q2): con otro `host` no se puede saber si su proceso vive: no es huérfana ni se reconcilia."""
    from bloque_a.interfaz_broker import _proceso
    pid = b.cola.recibir(_ct01(), T0)["pet_id"]
    _en_curso_ajena(b, pid, host=_proceso()["host"] + "-otra", pid=_pid_muerto())
    assert b.cola.huerfanas() == []
    with pytest.raises(PeticionInvalida):
        b.cola.reconciliar(pid, "prueba", T0 + pd.Timedelta(minutes=1))


def test_servir_una_en_curso_de_otro_proceso_se_rechaza(b):
    """N-04 (Q8): `servir` solo sirve lo que tomó este proceso."""
    from bloque_a.interfaz_broker import _proceso
    pid = b.cola.recibir(_ct01(), T0)["pet_id"]
    _en_curso_ajena(b, pid, host=_proceso()["host"], pid=_pid_muerto())
    with pytest.raises(PeticionInvalida):
        b.cola.servir({**_pets(b)[pid], "id": pid}, T0 + pd.Timedelta(minutes=1))
    assert _pets(b)[pid]["estado"] == "EN_CURSO"


def test_lo_que_escribe_atender_es_del_dia_de_la_toma(b, monkeypatch):
    """N-04 (Q10): recibida un día y atendida al siguiente, la toma y la ATENDIDA llevan la fecha del día de la toma."""
    pid = b.cola.recibir(_ct01(), T0)["pet_id"]
    monkeypatch.setattr(b, "ciclo", _CicloFalso())   # no fija la fecha: lo hace `atender`
    manana = T0 + pd.Timedelta(days=1)
    b.cola.atender(manana)
    fechas = [(e["estado"], e["_fecha"]) for e in b.almacen.leer("F5") if e.get("id") == pid]
    assert fechas == [("ENCOLADA", AS_OF), ("EN_CURSO", str(manana.date())), ("ATENDIDA", str(manana.date()))]


_HIJO_VIVO = """
import sys, time
sys.path.insert(0, "tests")
import pandas as pd
from conftest import nuevo_bloque
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import cargar_universo
b = nuevo_bloque(sys.argv[1], cargar_universo(RUTA_UNIVERSO_EJEMPLO))
b.cola._tomar(pd.Timestamp(sys.argv[2]), 1, en_marcha=True)
print("tomada", flush=True)
time.sleep(120)
"""


def test_una_en_curso_de_un_proceso_vivo_no_es_huerfana(tmp_path, universo):
    """N-04 (Q11, como B3): mientras el proceso que la tomó vive, no es huérfana y `reconciliar` se rechaza."""
    import subprocess
    import sys
    from pathlib import Path
    b = nuevo_bloque(tmp_path, universo)
    pid = b.cola.recibir(_ct01(), T0)["pet_id"]
    hijo = subprocess.Popen([sys.executable, "-c", _HIJO_VIVO, str(tmp_path), (T0 + pd.Timedelta(minutes=1)).isoformat()],
                            cwd=Path(__file__).resolve().parents[1], stdout=subprocess.PIPE, text=True)
    try:
        assert hijo.stdout.readline().strip() == "tomada"
        assert _pets(b)[pid]["estado"] == "EN_CURSO" and _pets(b)[pid]["pid"] == hijo.pid
        assert b.cola.huerfanas() == []
        with pytest.raises(PeticionInvalida):
            b.cola.reconciliar(pid, "prueba", T0 + pd.Timedelta(minutes=2))
    finally:
        hijo.kill()
        hijo.wait()
    assert b.cola.huerfanas() == [pid]                                               # muerto, sí lo es
