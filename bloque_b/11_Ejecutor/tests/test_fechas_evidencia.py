"""T-64: visibilidad y cierre se comprueban por separado, al final del día local."""
import json
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from bloque_b.fechas_evidencia import fechas_de_fuente
from bloque_b.orquestacion import Coordinador
from conftest import peticion_redes

from bloque_b import mock_respuestas as mr

CORTE = "2025-03-20"
FECHAS = {"fecha_fenomeno": "2025-03-17", "fecha_publicacion": "2025-03-18", "conocible_desde": "2025-03-18"}


@pytest.mark.parametrize(("cambios", "visible"), [
    ({}, True), ({"fecha_fenomeno": None}, False), ({"fecha_publicacion": ""}, False),
    ({"conocible_desde": "sin fecha"}, False), ({"conocible_desde": "2025-03-25"}, False),
    ({"fecha_fenomeno": "2025-03-19"}, False), ({"conocible_desde": "2025-03-10"}, False),
    ({"conocible_desde": "2025-03-20T23:00:00Z"}, False),
    ({"conocible_desde": "2025-03-20T22:59:59Z"}, True),
    ({"fecha_publicacion": "2025-03-18T12:00:00"}, False),
])
def test_visibilidad(cambios, visible):
    assert bool(fechas_de_fuente({"fechas": FECHAS | cambios}, CORTE, ZoneInfo("Europe/Madrid"))) is visible


@pytest.mark.parametrize(("observacion", "incidente", "cierra"), [
    ("2025-02-28", "2025-03-10", False), ("2025-03-10", "2025-03-10", False),
    ("2025-03-17", "2025-03-10", True), ("2025-03-17", None, False),
])
def test_desde_nota_hasta_encargo(hacer_entorno, rapido, monkeypatch, observacion, incidente, cierra):
    texto = "Medición fechada de los retrasos de transformadores."

    def dimension(m, c, r):
        informe = mr._informe_dimensional(m, c, r)
        for dim in informe["dim_informes"]:
            nota = dim["notas"][0]
            nota.update(afirmacion=texto, fechas=FECHAS | {"fecha_fenomeno": observacion})
        return informe

    def critico(m, c, r):
        informe = mr._refutacion(m, c, r)
        informe["objeciones"] = [{"objeto": "ESLABON", "eslabon_id": "ESL-03", "fuerza": "fuerte",
                                  "argumento": "Retraso comunicado.", "fecha_incidente": incidente}]
        return informe

    def director(m, c, r):
        ref = next(k for k, v in m["referencias_disponibles"].items() if v["descripcion"] == texto)
        obj, = m["objeciones"]
        return {"respuestas": {obj["obj_id"]: {"respuesta": "La medición confirma la recuperación.",
                                               "resuelta": True, "evidencia_nueva": [ref]}}}

    monkeypatch.setitem(mr._TAREAS, ("*", "informe_dimensional"), dimension)
    monkeypatch.setitem(mr._TAREAS, ("AG-B14", "refutacion"), critico)
    monkeypatch.setitem(mr._TAREAS, ("AG-B02", "respuestas_objeciones"), director)
    res = Coordinador(hacer_entorno(rapido, as_of=CORTE)).recibir(peticion_redes())
    p = json.loads(Path(res["entregables"]["paquete_json"]).read_text())
    obj, = p["refutacion"]["objeciones"]
    assert obj["resuelta"] is cierra
    assert obj["x_fecha_incidente"] == incidente
    cajas = [e for grupo in p["paquete_para_bloque_C"].values() for e in grupo if e["eslabon_id"] == "ESL-03"]
    assert cajas
    for caja in cajas:
        aviso, = caja["objeciones_y_respuestas"]
        assert aviso["x_resuelta"] is cierra
        assert aviso["x_fecha_incidente"] == incidente
        ref, = aviso["x_evidencia_respuesta"]
        assert aviso["x_fechas_evidencia"][ref] == FECHAS | {"fecha_fenomeno": observacion}
        if not cierra:
            assert aviso["x_motivo_abierta"] == obj["x_motivo_abierta"]


def test_reanudar_cierre_heredado_sin_fechas(hacer_entorno):
    res = Coordinador(hacer_entorno()).ejecutar({"pet_id": "PET-B-2025-0001", "run_id": "RUN-B-2025-0001",
        "siguiente": "F9", "refutacion": {"objeciones": [{"fuerza": "fuerte", "resuelta": True}]}})
    assert res["estado_peticion"] == "BLOQUEADO_AUDITORIA"
    assert "entregables" not in res
