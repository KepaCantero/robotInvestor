import json
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.guias import AGENTES_DE_CONTROL, validar_leccion
from conftest import AS_OF, config_pruebas, nuevo_bloque


def test_comparacion_por_decision(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(evaluacion={"min_calibrar": 1}))
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    a, d = r["paquete"]["clases"]["RV"]["opciones"][:2]
    b.decision({"decisiones": [{"opp_id": a["opp_id"], "decision": "DESCARTADA"}]}, AS_OF)
    b.decision({"decisiones": [{"opp_id": a["opp_id"], "decision": "ENVIADA_A_BLOQUE_B"},
                               {"opp_id": d["opp_id"], "decision": "DESCARTADA"}]}, AS_OF)
    fin = pd.Timestamp(AS_OF) + pd.Timedelta(days=35)
    b.fijar_fecha(fin)
    b.evaluador.ciclo(fin)
    lec, = [e for e in b.almacen.leer("F6") if e.get("tipo") == "PRODUCTO"]
    pronosticos = b.evaluador.resueltos(fin, solo_informe=True)
    enviados = [p for p in pronosticos if p["opp_id"] == a["opp_id"]]
    descartados = [p for p in pronosticos if p["opp_id"] == d["opp_id"]]
    assert enviados and descartados
    assert lec["observacion"] == ". ".join(
        f"{nombre}: {sum(p['resolucion']['resultado_binario'] for p in grupo)}/{len(grupo)} pronósticos con acierto"
        for nombre, grupo in (("enviadas", enviados), ("descartadas", descartados))
    )
    assert set(lec["evidencia"]) == {p["prg_id"] for p in enviados + descartados}
    assert lec["n"] == len(enviados + descartados)
    _comprobar_entrega(b, lec, {"AG-02", "AG-17"}, fin)


def _comprobar_entrega(b, lec, destinos, fecha):
    assert validar_leccion(lec, b.cfg) == []
    vigentes = b.evaluador.lecciones_vigentes(fecha)
    for agente in destinos | set(AGENTES_DE_CONTROL):
        visibles = b.guias.lecciones_para(agente, vigentes, fecha, "RUN-QA")
        assert (lec["id"] in {v["id"] for v in visibles}) == (agente in destinos)
    assert not [e for e in b.almacen.leer("HA") if e.get("leccion_id") == lec["id"]]


def test_recurrencia_entre_analisis(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    for i in range(3):
        b.consultas.enviar({"tipo": "DATO_O_DOCUMENTO", "modo": "NO_BLOQUEANTE", "run_id": f"RUN-2026-000{i}",
                            "preguntas": [{"texto": "¿Qué documento?", "supuesto_declarado": "El anterior"}]}, AS_OF)
    lecs = [e for e in b.almacen.leer("F6") if e.get("tipo") == "PRODUCTO"]
    assert len(lecs) == 1 and "CT-01" in lecs[0]["recomendacion"] and len(lecs[0]["evidencia"]) == 3
    _comprobar_entrega(b, lecs[0], {"AG-01", "AG-17"}, AS_OF)


@pytest.mark.parametrize(("minimo", "dias", "esperadas"), [(2, 0, 0), (1, 34, 0), (1, 0, 1)])
def test_muestra_temporal_e_idempotencia(tmp_path, universo, minimo, dias, esperadas):
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(evaluacion={"min_calibrar": minimo}))
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    a, d = r["paquete"]["clases"]["RV"]["opciones"][:2]
    fecha = pd.Timestamp(AS_OF) + pd.Timedelta(days=dias)
    b.decision({"decisiones": [{"opp_id": a["opp_id"], "decision": "ENVIADA_A_BLOQUE_B"},
                               {"opp_id": d["opp_id"], "decision": "DESCARTADA"}]}, fecha)
    for dias_en_el_futuro in (35, 42):
        fin = pd.Timestamp(AS_OF) + pd.Timedelta(days=dias_en_el_futuro)
        b.fijar_fecha(fin)
        b.evaluador.ciclo(fin)
    assert sum(e.get("tipo") == "PRODUCTO" for e in b.almacen.leer("F6")) == esperadas


@pytest.mark.parametrize(("runs", "dias"), [([None]*3, [0]*3), (["RUN-1"]*3, [0]*3),
                                            (["RUN-1","RUN-2","RUN-3"], [0, 56, 57])])
def test_recurrencia_exige_analisis_distintos_dentro_de_la_ventana(tmp_path, universo, runs, dias):
    b = nuevo_bloque(tmp_path, universo)
    for run, delta in zip(runs, dias):
        fecha = pd.Timestamp(AS_OF) + pd.Timedelta(days=delta)
        b.fijar_fecha(fecha)
        b.consultas.enviar({"tipo": "DATO_O_DOCUMENTO", "modo": "NO_BLOQUEANTE", "run_id": run,
                            "preguntas": [{"texto": "¿Qué documento?", "supuesto_declarado": "El anterior"}]}, fecha)
    assert not any(e.get("tipo") == "PRODUCTO" for e in b.almacen.leer("F6"))


def test_mapa_distingue_decisiones_y_consultas():
    mapa = json.loads((Path(__file__).parent / "mapa_plan_pruebas.json").read_text())
    assert "min_calibrar" in mapa["PB-11"]["comprueba"]
    assert "CT-01" in mapa["PB-62"]["comprueba"]
    assert "modelo" in mapa["PB-62"]["no_comprueba"]


def test_minimo_por_grupo_con_configuracion_de_entrega(tmp_path, universo):
    from bloque_a.configuracion import cargar_config, parametro

    b = nuevo_bloque(tmp_path, universo, cfg=cargar_config())
    b.fijar_fecha(AS_OF)
    minimo = parametro(b.cfg, "evaluacion.min_calibrar")
    for i in range(minimo):
        for decision, acierto in (("ENVIADA_A_BLOQUE_B", 1), ("DESCARTADA", 0)):
            oid = f"OPP-{decision}-{i}"
            b.almacen.escribir("F3", "AG-02", {"opp_id": oid, "tipo_entrada": "DECISION_BROKER",
                              "decision_broker": {"decision": decision, "fecha": AS_OF}})
            b.almacen.escribir("F4", "AG-10", {"prg_id": f"PRG-{oid}", "opp_id": oid, "tipo_entrada": "ALTA",
                              "estado": "ABIERTO", "en_informe": True, "fecha_emision": AS_OF, "fecha_resolucion": "2026-06-15"})
    fecha = b.fijar_fecha("2026-06-15")
    for i in range(minimo):
        for decision, acierto in (("ENVIADA_A_BLOQUE_B", 1), ("DESCARTADA", 0)):
            b.almacen.escribir("F4", "AG-20", {"prg_id": f"PRG-OPP-{decision}-{i}", "estado": "RESUELTO",
                              "tipo_entrada": "RESOLUCION", "resolucion": {"fecha_dato": "2026-06-15",
                              "resultado_binario": acierto, "comprobacion_fuga": "SUPERADA"}})
        if i == minimo - 2:
            assert b.evaluador.comparar_decisiones_broker(fecha) is None
    lec = b.evaluador.comparar_decisiones_broker(fecha)
    assert lec["n"] == 2 * minimo
    assert lec["observacion"] == f"enviadas: {minimo}/{minimo} pronósticos con acierto. descartadas: 0/{minimo} pronósticos con acierto"
    _comprobar_entrega(b, lec, {"AG-02", "AG-17"}, fecha)
