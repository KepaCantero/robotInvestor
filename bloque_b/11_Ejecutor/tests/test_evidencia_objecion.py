"""T-63 · El cierre de una objeción fuerte debe viajar con su referencia."""
import json
from pathlib import Path

import pytest
from bloque_b.orquestacion import Coordinador
from conftest import peticion_redes

from bloque_b import mock_respuestas as mr


@pytest.mark.parametrize("caso", ["sin_cita", "inventada", "otra_peticion", "registrada"])
def test_cierre_fuerte_requiere_fuente_en_la_caja(hacer_entorno, rapido, monkeypatch, caso):
    ent = hacer_entorno(rapido, as_of="2025-01-31")
    ajena = ent.alm.nuevo_id("DAT-B")
    ent.alm.escribir("F2", "AG-B15", {"tipo_entrada": "DAT", "id": ajena, "pet_id": "PET-B-2024-0001",
                                      "descripcion": "Dato de otra petición."})
    cita = []

    def critico(m, c, r):
        informe = mr._refutacion(m, c, r)
        informe["objeciones"] = [{"objeto": "TESIS", "fuerza": "fuerte", "fecha_incidente": "2025-01-10", "argumento": "Han aumentado los retrasos."}]
        return informe

    def director(m, c, r):
        respuesta = {"resuelta": True, "respuesta": "Los plazos han vuelto al nivel anterior."}
        if caso == "registrada":
            cita.append(next(iter(m["referencias_disponibles"])))
            respuesta["evidencia_nueva"] = cita
        elif caso == "otra_peticion":
            assert ajena not in m.get("referencias_disponibles", {})
            respuesta["evidencia_nueva"] = [ajena]
        elif caso == "inventada":
            respuesta["evidencia_nueva"] = ["EVD-B-9999-9999"]
        obj, = m["objeciones"]
        return {"respuestas": {obj["obj_id"]: respuesta}}

    monkeypatch.setitem(mr._TAREAS, ("AG-B14", "refutacion"), critico)
    monkeypatch.setitem(mr._TAREAS, ("AG-B02", "respuestas_objeciones"), director)
    res = Coordinador(ent).recibir(peticion_redes())
    paquete = json.loads(Path(res["entregables"]["paquete_json"]).read_text())
    confirmado = caso == "registrada"
    assert paquete["veredicto"]["valor"] == ("INVERTIR_ESCALONADO" if confirmado else "VIGILAR")
    obs, = paquete["refutacion"]["objeciones"]
    assert obs["resuelta"] is confirmado
    assert obs["x_evidencia_respuesta"] == cita
    informe = Path(res["entregables"]["informe_tecnico"]).read_text()
    linea = next(linea for linea in informe.splitlines() if obs["argumento"] in linea and obs["obj_id"] in linea)
    assert (cita[0] if confirmado else obs["x_motivo_abierta"]) in linea
    cajas = [e for grupo in paquete["paquete_para_bloque_C"].values() for e in grupo]
    assert cajas
    campo = "x_objeciones_tesis_resueltas" if confirmado else "x_objeciones_tesis_abiertas"
    for caja in cajas:
        aviso, = caja["contexto_ambito"][campo]
        assert aviso["x_evidencia_respuesta"] == cita
        assert aviso["resuelta"] is confirmado


@pytest.mark.parametrize(("citas", "texto", "cierra"), [
    ([], "Resuelto", False), ("DAT-B-2025-0001", "Resuelto", False),
    (["DAT-B-2025-0001", {}], "Resuelto", False),
    (["DAT-B-2025-0001"], "  ", False), (["DAT-B-2025-0001"], {}, False),
    (["DAT-B-2025-0001", "DAT-B-2025-0001"], "Comprobación documentada.", True),
])
def test_fronteras_de_la_respuesta(citas, texto, cierra):
    obj = {"obj_id": "OBJ-1", "fuerza": "fuerte", "x_fecha_incidente": "2025-01-10", "resuelta": False}
    Coordinador._aplicar_respuestas([obj], {"OBJ-1": {"resuelta": True, "respuesta": texto, "evidencia_nueva": citas}},
                                   {"DAT-B-2025-0001": {"fecha_fenomeno": "2025-01-14", "fecha_publicacion": "2025-01-15", "conocible_desde": "2025-01-15"}})
    assert obj["resuelta"] is cierra
    if cierra:
        assert obj["x_evidencia_respuesta"] == ["DAT-B-2025-0001"]
