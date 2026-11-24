"""QA r01 de T-188 (Claude). Ataques a las lecciones de producto de PB-11 y PB-62.

Ejecutar desde la raíz del repositorio con la venv:
    python -m pytest -q -p no:cacheprovider .docs/tickets/T-188/revisores/r01_01_lecciones_producto.py
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

EJ = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJ / "tests"))
sys.path.insert(0, str(EJ))

from conftest import AS_OF, config_pruebas, nuevo_bloque  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.guias import validar_leccion, AGENTES_DE_CONTROL  # noqa: E402


@pytest.fixture(scope="module")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def _decision(tmp_path, universo, min_calibrar=1, dias_decision=0, dos_ciclos=False):
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(evaluacion={"min_calibrar": min_calibrar}))
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    a, d = r["paquete"]["clases"]["RV"]["opciones"][:2]
    cuando = str((pd.Timestamp(AS_OF) + pd.Timedelta(days=dias_decision)).date())
    b.decision({"decisiones": [{"opp_id": a["opp_id"], "decision": "ENVIADA_A_BLOQUE_B"},
                               {"opp_id": d["opp_id"], "decision": "DESCARTADA"}]}, cuando)
    fin = pd.Timestamp(AS_OF) + pd.Timedelta(days=35)
    b.fijar_fecha(fin)
    b.evaluador.ciclo(fin)
    if dos_ciclos:
        b.evaluador.ciclo(fin + pd.Timedelta(days=7))
    return b, fin


def _lecs(b, tema):
    return [e for e in b.almacen.leer("F6") if e.get("tipo_entrada") == "LEC" and (e.get("ambito") or {}).get("tema") == tema]


def _recurrencia(tmp_path, universo, runs):
    b = nuevo_bloque(tmp_path, universo)
    for run in runs:
        b.consultas.enviar({"tipo": "DATO_O_DOCUMENTO", "modo": "NO_BLOQUEANTE", "run_id": run,
                            "preguntas": [{"texto": "¿Qué documento?", "supuesto_declarado": "El anterior"}]}, AS_OF)
    return b


# --- H-01: la lección no cumple F6 4.4 y no llega a nadie ---------------------------------------------------------
def test_h01_leccion_decision_cumple_f6_44(tmp_path, universo):
    b, _ = _decision(tmp_path, universo)
    (lec,) = _lecs(b, "DECISION_BROKER")
    assert validar_leccion(lec, b.cfg) == []


def test_h01_leccion_decision_llega_a_sus_agentes(tmp_path, universo):
    b, fin = _decision(tmp_path, universo)
    (lec,) = _lecs(b, "DECISION_BROKER")
    vigentes = b.evaluador.lecciones_vigentes(fin)
    assert lec["id"] in [l["id"] for l in vigentes]
    dadas = b.guias.lecciones_para("AG-17", vigentes, fin, "RUN-QA")
    assert lec["id"] in [l["id"] for l in dadas]


def test_h01_leccion_recurrente_cumple_f6_44_y_llega(tmp_path, universo):
    b = _recurrencia(tmp_path, universo, [f"RUN-2026-000{i}" for i in range(3)])
    (lec,) = _lecs(b, "CONSULTA_RECURRENTE")
    assert validar_leccion(lec, b.cfg) == []
    dadas = b.guias.lecciones_para("AG-01", b.evaluador.lecciones_vigentes(AS_OF), AS_OF, "RUN-QA")
    assert lec["id"] in [l["id"] for l in dadas]


def test_h01_ninguna_incidencia_material_por_la_leccion(tmp_path, universo):
    b, fin = _decision(tmp_path, universo)
    (lec,) = _lecs(b, "DECISION_BROKER")
    b.guias.lecciones_para("AG-17", b.evaluador.lecciones_vigentes(fin), fin, "RUN-QA")
    assert not [e for e in b.almacen.leer("HA") if e.get("leccion_id") == lec["id"]]


# --- T-161/T-171: ningún agente de control recibe las PRODUCTO (debe seguir cumpliéndose) --------------------------
def test_control_no_recibe_producto(tmp_path, universo):
    b, fin = _decision(tmp_path, universo)
    vig = b.evaluador.lecciones_vigentes(fin)
    for ag in AGENTES_DE_CONTROL:
        assert not [l for l in b.guias.lecciones_para(ag, vig, fin, "RUN-QA") if l["tipo"] == "PRODUCTO"], ag


# --- H-02: «cuando haya muestra» sin prueba ------------------------------------------------------------------------
def test_h02_sin_muestra_no_hay_leccion(tmp_path, universo):
    b, _ = _decision(tmp_path, universo, min_calibrar=2)   # una opción por grupo < 2
    assert _lecs(b, "DECISION_BROKER") == []


def test_h02_decision_posterior_al_dato_no_cuenta(tmp_path, universo):
    b, _ = _decision(tmp_path, universo, dias_decision=34)   # tras el dato y antes del C5
    assert _lecs(b, "DECISION_BROKER") == []


def test_h02_idempotente(tmp_path, universo):
    b, _ = _decision(tmp_path, universo, dos_ciclos=True)
    assert len(_lecs(b, "DECISION_BROKER")) == 1


# --- H-03: «tres análisis» distintos sin prueba que lo mate --------------------------------------------------------
def test_h03_tres_consultas_del_mismo_analisis_no_crean_leccion(tmp_path, universo):
    b = _recurrencia(tmp_path, universo, ["RUN-2026-0001"] * 3)
    assert _lecs(b, "CONSULTA_RECURRENTE") == []


def test_h03_consultas_sin_run_no_crean_leccion(tmp_path, universo):
    b = _recurrencia(tmp_path, universo, [None] * 3)
    assert _lecs(b, "CONSULTA_RECURRENTE") == []
