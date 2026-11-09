"""T-62: la misma objeción al sector o a un eslabón, hasta el encargo a C."""
import json
from pathlib import Path

import jsonschema
import pytest
from bloque_b.orquestacion import Coordinador
from conftest import peticion_redes

from bloque_b import mock_respuestas as mr


@pytest.mark.parametrize(("objeto", "eid", "cerrada"), [
    ("TESIS", None, False), ("ESLABON", "ESL-03", False),
    ("TESIS", "ESL-03", False), ("ESLABON", "ESL-03", True),
    ("ESLABON", "ESL-99", False), ("ESLABON", None, False), ("ESLABON", [], False),
])
def test_retraso_transformadores(hacer_entorno, rapido, monkeypatch, objeto, eid, cerrada):
    esquema = next((Path(__file__).resolve().parents[2] / "06_Plantillas_entregables").glob("Esquema*.json"))
    argumento = "Los plazos de entrega de los transformadores se han duplicado."

    def critico(m, c, r):
        informe = mr._refutacion(m, c, r)
        o = {"objeto": objeto, "fuerza": "fuerte", "argumento": argumento}
        if eid is not None:
            o["eslabon_id"] = eid
        informe["objeciones"] = [o]
        return informe

    def director(m, c, r):
        return {"respuestas": {o["obj_id"]: {"respuesta": "Contraste de plazos.", "resuelta": cerrada,
                                                "evidencia_nueva": list(m["referencias_disponibles"])[:1]}
                               for o in m["objeciones"]}}

    monkeypatch.setitem(mr._TAREAS, ("AG-B14", "refutacion"), critico)
    monkeypatch.setitem(mr._TAREAS, ("AG-B02", "respuestas_objeciones"), director)
    res = Coordinador(hacer_entorno(rapido, as_of="2025-01-31")).recibir(peticion_redes())
    if objeto == "ESLABON" and eid != "ESL-03":
        assert res["estado_peticion"] == "BLOQUEADO_AUDITORIA"
        assert not res.get("entregables")
        return
    assert res["estado_peticion"] == "ENTREGADA", res
    p = json.loads(Path(res["entregables"]["paquete_json"]).read_text())
    jsonschema.validate(p, json.loads(esquema.read_text()))
    if eid is None:
        assert p["veredicto"]["valor"] == "VIGILAR"
        assert p["puertas_ambito"]["PA5"] == "BLOQUEA"
        cajas = [e for grupo in p["paquete_para_bloque_C"].values() for e in grupo]
        assert cajas
        for e in cajas:
            aviso, = e["contexto_ambito"]["x_objeciones_tesis_abiertas"]
            assert aviso["argumento"] == argumento and aviso["objeto"] == "TESIS"
        return
    assert p["veredicto"]["valor"] == "INVERTIR_ESCALONADO"
    assert p["puertas_ambito"]["PA5"] == "OK"
    obj, = p["refutacion"]["objeciones"]
    assert (obj["objeto"], obj["x_eslabon_id"], obj["resuelta"]) == ("CADENA", eid, cerrada)
    afectados = set(obj["x_candidatos_afectados"])
    for grupo in p["candidatos_por_tipo"].values():
        for candidato in grupo.get("top_n", []):
            expuesto = candidato["eslabon_id"] == eid or eid in candidato["eslabones_secundarios"]
            assert expuesto == (candidato["cand_id"] in afectados)
            assert candidato["puertas"]["PC5"] == ("LIMITA" if expuesto and not cerrada else "OK")
    vistos = set()
    for encargos in p["paquete_para_bloque_C"].values():
        for enc in encargos:
            avisos = [o for o in enc["objeciones_y_respuestas"] if o["obj_id"] == obj["obj_id"]]
            assert bool(avisos) == (enc["cand_id"] in afectados)
            if enc["eslabon_id"] == eid:
                assert avisos
            if avisos:
                assert avisos[0]["resumen"] == argumento
                assert avisos[0]["x_eslabon_id"] == eid
                assert avisos[0]["x_resuelta"] is cerrada
                assert avisos[0]["x_evidencia_respuesta"] == obj["x_evidencia_respuesta"]
                if not cerrada:
                    assert enc["veredicto_candidato"] == "SECUNDARIO"
            vistos.add(bool(avisos))
    assert vistos == {True, False}


def test_alcance_secundario_y_opciones_adicionales(hacer_entorno, rapido, monkeypatch):
    # Un top reducido deja instrumentos adicionales en las tablas por cobertura.
    rapido["top_n"]["N2"] = [1, 0]
    asignar = mr._asignar

    def asignar_secundarios(mensaje):
        asignaciones = asignar(mensaje)
        for opcion in asignaciones.values():
            if mensaje.get("tipo_activo") == "RF":
                opcion["eslabon_id"] = "ESL-03"
            if opcion["eslabon_id"] != "ESL-02":
                opcion["eslabones_secundarios"] = ["ESL-02"]
        return asignaciones

    def critico(m, c, r):
        assert "cables" in m["eslabones"]["ESL-02"].lower()
        return {**mr._refutacion(m, c, r), "objeciones": [
            {"objeto": "ESLABON", "eslabon_id": "ESL-02", "fuerza": "fuerte",
             "argumento": "Retrasos de fabricación de cables."}]}

    monkeypatch.setattr(mr, "_asignar", asignar_secundarios)
    monkeypatch.setitem(mr._TAREAS, ("AG-B14", "refutacion"), critico)
    monkeypatch.setitem(mr._TAREAS, ("AG-B02", "respuestas_objeciones"), lambda *args: {"respuestas": {}})
    res = Coordinador(hacer_entorno(rapido, as_of="2025-01-31")).recibir(peticion_redes())
    assert res["estado_peticion"] == "ENTREGADA", res
    p = json.loads(Path(res["entregables"]["paquete_json"]).read_text())
    cajas = [e for grupo in p["paquete_para_bloque_C"].values() for e in grupo]
    assert any(e["origen_seleccion"] == "MEJORES_POR_ESLABON" for e in cajas)
    assert any(e["eslabon_id"] != "ESL-02" for e in cajas)
    for e in cajas:
        assert e["veredicto_candidato"] == "SECUNDARIO"
        aviso, = e["objeciones_y_respuestas"]
        assert aviso["x_eslabon_id"] == "ESL-02" and not aviso["x_resuelta"]
