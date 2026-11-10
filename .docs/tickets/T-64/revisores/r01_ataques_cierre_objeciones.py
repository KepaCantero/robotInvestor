"""QA de Claude sobre T-62, T-63 y T-64 (ramas de Astra): ataques al cierre de objeciones fuertes de B."""
import json
from pathlib import Path

import pytest
from bloque_b.orquestacion import Coordinador
from conftest import peticion_redes

from bloque_b import mock_respuestas as mr

CORTE = "2025-03-20"
FECHAS = {"fecha_fenomeno": "2025-03-17", "fecha_publicacion": "2025-03-18", "conocible_desde": "2025-03-18"}
TEXTO = "Medición fechada de los retrasos de transformadores."


def _montar(monkeypatch, *, fechas=FECHAS, incidente="2025-03-10", objeto="ESLABON", eid="ESL-03", citas=None, resuelta=True,
            fuerza="fuerte", extra_nota=None):
    vistas = {}

    def dimension(m, c, r):
        informe = mr._informe_dimensional(m, c, r)
        for dim in informe["dim_informes"]:
            dim["notas"][0].update(afirmacion=TEXTO, fechas=dict(fechas))
            if extra_nota:
                dim["notas"].append(dict(extra_nota))
        return informe

    def critico(m, c, r):
        informe = mr._refutacion(m, c, r)
        o = {"objeto": objeto, "fuerza": fuerza, "argumento": "Retraso comunicado.", "fecha_incidente": incidente}
        if eid is not None:
            o["eslabon_id"] = eid
        if objeto == "CANDIDATO":
            o["objeto"] = m["finalistas"][0]["cand_id"]
        informe["objeciones"] = [o]
        return informe

    def responder(m, c, r, clave):
        vistas["refs"] = dict(m["referencias_disponibles"])
        buena = next((k for k, v in m["referencias_disponibles"].items() if v["descripcion"] == TEXTO), None)
        ev = citas(buena, m["referencias_disponibles"]) if callable(citas) else [buena]
        return {clave: {o["obj_id"]: {"respuesta": "La medición confirma la recuperación.", "resuelta": resuelta,
                                      "evidencia_nueva": ev} for o in m["objeciones"]}}

    monkeypatch.setitem(mr._TAREAS, ("*", "informe_dimensional"), dimension)
    monkeypatch.setitem(mr._TAREAS, ("AG-B14", "refutacion"), critico)
    monkeypatch.setitem(mr._TAREAS, ("AG-B02", "respuestas_objeciones"), lambda m, c, r: responder(m, c, r, "respuestas"))
    monkeypatch.setitem(mr._TAREAS, ("AG-B12", "respuestas_objeciones"), lambda m, c, r: responder(m, c, r, "respuestas_objeciones"))
    return vistas


def _correr(hacer_entorno, rapido):
    res = Coordinador(hacer_entorno(rapido, as_of=CORTE)).recibir(peticion_redes())
    if not res.get("entregables"):
        return res, None
    return res, json.loads(Path(res["entregables"]["paquete_json"]).read_text())


def _fuertes(p):
    return [o for o in p["refutacion"]["objeciones"] if o["fuerza"] == "fuerte"]


def test_a01_control_cierra(hacer_entorno, rapido, monkeypatch):
    _montar(monkeypatch)
    _, p = _correr(hacer_entorno, rapido)
    assert all(o["resuelta"] for o in _fuertes(p))


@pytest.mark.parametrize("citas", [
    lambda b, refs: [b, "EVD-B-9999-9999"],          # una buena y una inventada
    lambda b, refs: b,                                # cadena en lugar de lista
    lambda b, refs: [],                               # lista vacía
    lambda b, refs: [{"id": b}],                      # cita mal formada
])
def test_a02_citas_invalidas_no_cierran(hacer_entorno, rapido, monkeypatch, citas):
    _montar(monkeypatch, citas=citas)
    _, p = _correr(hacer_entorno, rapido)
    assert _fuertes(p) and not any(o["resuelta"] for o in _fuertes(p))


def test_a03_cita_duplicada_cierra_una_vez(hacer_entorno, rapido, monkeypatch):
    _montar(monkeypatch, citas=lambda b, refs: [b, b])
    _, p = _correr(hacer_entorno, rapido)
    o, = _fuertes(p)
    assert o["resuelta"] and len(o["x_evidencia_respuesta"]) == 1


@pytest.mark.parametrize("resuelta", ["true", 1, None])
def test_a04_resuelta_no_booleana_no_cierra(hacer_entorno, rapido, monkeypatch, resuelta):
    _montar(monkeypatch, resuelta=resuelta)
    _, p = _correr(hacer_entorno, rapido)
    assert not any(o["resuelta"] for o in _fuertes(p))


@pytest.mark.parametrize("incidente", ["2025-03-10T10:00:00", "2025-12-31", "ayer", 20250310])
def test_a05_fecha_de_incidente_rara_o_futura_no_cierra(hacer_entorno, rapido, monkeypatch, incidente):
    _montar(monkeypatch, incidente=incidente)
    _, p = _correr(hacer_entorno, rapido)
    assert not any(o["resuelta"] for o in _fuertes(p))


def test_a06_fuente_futura_no_se_ofrece_y_no_cierra(hacer_entorno, rapido, monkeypatch):
    vistas = _montar(monkeypatch, fechas=FECHAS | {"conocible_desde": "2025-04-01"})
    res, p = _correr(hacer_entorno, rapido)
    assert TEXTO not in [v["descripcion"] for v in vistas.get("refs", {}).values()]
    assert not any(o["resuelta"] for o in _fuertes(p))


def test_a07_la_nota_con_fecha_futura_se_declara(hacer_entorno, rapido, monkeypatch):
    """La nota con fechas imposibles se descarta: ¿queda declarado en alguna limitación o incidencia?"""
    _montar(monkeypatch, fechas=FECHAS | {"conocible_desde": "2025-04-01"})
    res, p = _correr(hacer_entorno, rapido)
    texto = json.dumps(p, ensure_ascii=False)
    assert TEXTO not in texto
    assert any("fecha" in x.lower() for x in p.get("limitaciones", [])), "nota descartada en silencio"


def test_a08_objecion_fuerte_a_un_candidato_usa_la_misma_regla(hacer_entorno, rapido, monkeypatch):
    _montar(monkeypatch, objeto="CANDIDATO", eid=None, incidente=None)
    _, p = _correr(hacer_entorno, rapido)
    o, = _fuertes(p)
    assert o["resuelta"] is False and "incidente" in o["x_motivo_abierta"]


def test_a09_eslabon_desconocido_bloquea_la_peticion_entera(hacer_entorno, rapido, monkeypatch):
    _montar(monkeypatch, eid="ESL-99")
    res, p = _correr(hacer_entorno, rapido)
    assert res["estado_peticion"] == "BLOQUEADO_AUDITORIA" and p is None


def test_a10_moderada_sin_cita_sigue_su_regla(hacer_entorno, rapido, monkeypatch):
    _montar(monkeypatch, fuerza="moderada", citas=lambda b, refs: [])
    _, p = _correr(hacer_entorno, rapido)
    mods = [o for o in p["refutacion"]["objeciones"] if o["fuerza"] == "moderada"]
    assert mods and all(o["resuelta"] for o in mods) and not any("x_motivo_abierta" in o for o in mods)


def test_a11_eslabon_abierto_marca_a_los_expuestos_y_baja_su_prioridad(hacer_entorno, rapido, monkeypatch):
    _montar(monkeypatch, resuelta=False)
    _, p = _correr(hacer_entorno, rapido)
    o, = _fuertes(p)
    afectados = set(o["x_candidatos_afectados"])
    cajas = [e for g in p["paquete_para_bloque_C"].values() for e in g if e.get("cand_id") in afectados]
    assert afectados and cajas
    assert all(any(a.get("x_eslabon_id") == "ESL-03" and a.get("x_resuelta") is False for a in c["objeciones_y_respuestas"]) for c in cajas)

