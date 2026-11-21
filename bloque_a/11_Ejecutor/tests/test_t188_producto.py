import pandas as pd
from conftest import AS_OF, config_pruebas, nuevo_bloque


def test_comparacion_por_decision(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(evaluacion={"min_calibrar": 1}))
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    a, d = r["paquete"]["clases"]["RV"]["opciones"][:2]
    b.decision({"decisiones": [{"opp_id": a["opp_id"], "decision": "ENVIADA_A_BLOQUE_B"},
                               {"opp_id": d["opp_id"], "decision": "DESCARTADA"}]}, AS_OF)
    fin = pd.Timestamp(AS_OF) + pd.Timedelta(days=35)
    b.fijar_fecha(fin)
    b.evaluador.ciclo(fin)
    lecs = [e for e in b.almacen.leer("F6") if e.get("ambito", {}).get("tema") == "DECISION_BROKER"]
    assert len(lecs) == 1 and lecs[0]["tipo"] == "PRODUCTO" and lecs[0]["n"] >= 2
    assert "descartadas" in lecs[0]["observacion"]


def test_recurrencia_entre_analisis(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    for i in range(3):
        b.consultas.enviar({"tipo": "DATO_O_DOCUMENTO", "modo": "NO_BLOQUEANTE", "run_id": f"RUN-2026-000{i}",
                            "preguntas": [{"texto": "¿Qué documento?", "supuesto_declarado": "El anterior"}]}, AS_OF)
    lecs = [e for e in b.almacen.leer("F6") if e.get("tipo") == "PRODUCTO"]
    assert len(lecs) == 1 and "CT-01" in lecs[0]["recomendacion"] and len(lecs[0]["evidencia"]) == 3
