"""Alcance de una objeción fuerte a un finalista en el recorrido completo."""
import json
from pathlib import Path

from bloque_b.orquestacion import Coordinador
from conftest import peticion_redes

from bloque_b import mock_respuestas as mr


def test_objecion_individual_conserva_el_contexto_y_afecta_solo_al_finalista(hacer_entorno, rapido, monkeypatch):
    def refutar(mensaje, contexto, azar):
        informe = mr._refutacion(mensaje, contexto, azar)
        for objecion in informe["objeciones"]:
            if objecion["objeto"] != "TESIS":
                objecion.update(fuerza="fuerte", argumento="El fabricante perdió un contrato importante.")
        return informe

    monkeypatch.setitem(mr._TAREAS, ("AG-B14", "refutacion"), refutar)
    paquetes = []
    for resuelta in (True, False):
        def responder(mensaje, contexto, azar, resuelta=resuelta):
            objetados = {o["objeto"] for o in mensaje["objeciones"]}
            assert {c["cand_id"] for c in mensaje["finalistas"]} == objetados
            assert all(c["nombre"] and c["tipo"] for c in mensaje["finalistas"])
            return {"respuestas_objeciones": {
                o["obj_id"]: {"respuesta": "Contraste simulado del contrato.", "resuelta": resuelta,
                              "evidencia_nueva": list(mensaje["referencias_disponibles"])[:1]}
                for o in mensaje["objeciones"]
            }}

        monkeypatch.setitem(mr._TAREAS, ("AG-B12", "respuestas_objeciones"), responder)
        res = Coordinador(hacer_entorno(rapido, as_of="2025-01-31")).recibir(peticion_redes())
        assert res["estado_peticion"] == "ENTREGADA"
        paquetes.append(json.loads(Path(res["entregables"]["paquete_json"]).read_text(encoding="utf-8")))

    control, abierta = paquetes
    assert control["veredicto"]["valor"] == abierta["veredicto"]["valor"] == "INVERTIR_ESCALONADO"
    assert control["puertas_ambito"]["PA5"] == abierta["puertas_ambito"]["PA5"] == "OK"
    objetivo, = [o["objeto"] for o in abierta["refutacion"]["objeciones"] if o["fuerza"] == "fuerte"]

    def finalistas(paquete):
        return {c["cand_id"]: c for grupo in paquete["candidatos_por_tipo"].values() for c in grupo.get("top_n", [])}

    antes, despues = map(finalistas, paquetes)
    assert antes.keys() == despues.keys()
    assert antes[objetivo]["puertas"]["PC5"] == "OK"
    assert despues[objetivo]["puertas"]["PC5"] == "LIMITA"
    caja = next(e for grupo in control["paquete_para_bloque_C"].values() for e in grupo if e["cand_id"] == objetivo)
    assert any(o.get("x_evidencia_respuesta") and o["x_resuelta"] for o in caja["objeciones_y_respuestas"])
    assert despues[objetivo]["veredicto"] == "SECUNDARIO"
    for cid in antes.keys() - {objetivo}:
        assert despues[cid]["puertas"] == antes[cid]["puertas"]
        assert despues[cid]["veredicto"] == antes[cid]["veredicto"]


def test_el_seleccionador_no_puede_cerrar_una_objecion_de_la_tesis(hacer_entorno, rapido, monkeypatch):
    pendientes = {}

    def refutar(mensaje, contexto, azar):
        informe = mr._refutacion(mensaje, contexto, azar)
        informe["objeciones"][0]["fuerza"] = "fuerte"
        return informe

    def director(mensaje, contexto, azar):
        for o in mensaje["objeciones"]:
            pendientes[o["obj_id"]] = {"respuesta": "Falta verificar la demanda.", "resuelta": False}
        return {"respuestas": pendientes}

    def seleccionador(mensaje, contexto, azar):
        respuestas = mr._seleccion(mensaje, contexto, azar)["respuestas_objeciones"]
        for identificador in pendientes:
            respuestas[identificador] = {"respuesta": "Cierre ajeno al encargo.", "resuelta": True}
        return {"respuestas_objeciones": respuestas}

    monkeypatch.setitem(mr._TAREAS, ("AG-B14", "refutacion"), refutar)
    monkeypatch.setitem(mr._TAREAS, ("AG-B02", "respuestas_objeciones"), director)
    monkeypatch.setitem(mr._TAREAS, ("AG-B12", "respuestas_objeciones"), seleccionador)
    res = Coordinador(hacer_entorno(rapido, as_of="2025-01-31")).recibir(peticion_redes())
    paquete = json.loads(Path(res["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    assert paquete["veredicto"]["valor"] == "VIGILAR"
    for o in paquete["refutacion"]["objeciones"]:
        if o["obj_id"] in pendientes:
            assert o["estado_contraste"] == "incertidumbre_abierta"
            assert o["respuesta"] == "Falta verificar la demanda."
        elif o["fuerza"] == "debil":
            assert o["estado_contraste"] == "aceptada"
        else:
            assert o["estado_contraste"] == "resuelta"


def test_refutacion_con_un_solo_matiz(hacer_entorno, rapido, monkeypatch):
    def refutar(mensaje, contexto, azar):
        informe = mr._refutacion(mensaje, contexto, azar)
        informe["objeciones"] = [o for o in informe["objeciones"] if o["fuerza"] == "debil"]
        return informe

    monkeypatch.setitem(mr._TAREAS, ("AG-B14", "refutacion"), refutar)
    res = Coordinador(hacer_entorno(rapido, as_of="2025-01-31")).recibir(peticion_redes())
    paquete = json.loads(Path(res["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    matiz, = paquete["refutacion"]["objeciones"]
    assert matiz["estado_contraste"] == "aceptada"
    assert matiz["resuelta"] is True
