"""QA de la ronda de cierre de T-161 (H-17) · Lo que la lista blanca `CAMPOS_DE_CICLO_DE_VIDA` y la entrada de alta tienen que
cumplir además de las pruebas del ticket: una entrada anterior al alta, otra con otro `tipo_entrada`, una que repite los
mismos valores, una que solo cambia `estado` o `caducidad`, y que el agente nunca recibe el `l` consolidado.

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-161/revisores/r05_01_cierre.py
"""
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tests"))
from conftest import AS_OF, nuevo_bloque  # noqa: E402

from bloque_a import guias as G  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402

CONTROL = tuple(sorted(G.AGENTES_DE_CONTROL))
TODOS = CONTROL + ("AG-02", "AG-03", "AG-17")
MALA = "Omite la segunda pasada en banda marginal"


@pytest.fixture(scope="module")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


@pytest.fixture
def b(tmp_path, universo):
    x = nuevo_bloque(tmp_path, universo)
    x.fijar_fecha(AS_OF)
    return x


def predictiva(b, lid=None):
    if lid:   # con un id dado (para sembrar entradas antes del alta)
        lec = {"tipo_entrada": "LEC", "id": lid, "fecha": AS_OF, "ambito": {"clase": "RV", "horizonte": "H2"}, "nivel": "B",
               "tipo": "PREDICTIVA", "observacion": "Acierto 38% en 26 pronósticos de RV×H2.", "evidencia": ["M"],
               "recomendacion": "Rebajar un nivel la banda verbal.", "fuerza": "recurrente", "n": 26, "caducidad": "2027-01-01",
               "estado": "VIGENTE", "origen": "DETERMINISTA"}
        b.almacen.escribir("F6", "AG-20", lec)
        return lec
    return b.evaluador._nueva_leccion(pd.Timestamp(AS_OF), {"clase": "RV", "horizonte": "H2"}, "PREDICTIVA",
                                      "Acierto 38% en 26 pronósticos de RV×H2.", "Rebajar un nivel la banda verbal.",
                                      "recurrente", ["M"], 26)


def dadas(b, run="RUN-X"):
    vig = b.evaluador.lecciones_vigentes(AS_OF)
    return {a: b.guias.lecciones_para(a, vig, AS_OF, run) for a in TODOS}


def test_entrada_anterior_al_alta_sin_tipo_entrada_cuenta_como_alteracion(b):
    b.almacen.escribir("F6", "AG-20", {"id": "LEC-SEMBRADA-1", "fuerza": MALA})
    predictiva(b, "LEC-SEMBRADA-1")
    # el alta pisa fuerza en el consolidado; la entrada anterior difiere del alta: alteración, a nadie
    assert all(v == [] for v in dadas(b).values())


def test_entrada_con_otro_tipo_entrada_y_el_mismo_id(b):
    lec = predictiva(b)
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "RES", "id": lec["id"], "observacion": MALA})
    d = dadas(b)
    assert all(MALA.lower() not in json.dumps(v, ensure_ascii=False).lower() for v in d.values())


def test_repetir_los_mismos_valores_no_es_alteracion(b):
    lec = predictiva(b)
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "LEC", "id": lec["id"], "observacion": lec["observacion"],
                                       "fuerza": lec["fuerza"]})
    assert all([x["id"] for x in dadas(b)[a]] == [lec["id"]] for a in CONTROL)


@pytest.mark.parametrize("cambio", [{"estado": "VIGENTE"}, {"caducidad": "2027-03-01"}, {"estado": "RETIRADA"},
                                    {"caducidad": "2020-01-01"}])
def test_solo_ciclo_de_vida(b, cambio):
    lec = predictiva(b)
    b.almacen.escribir("F6", "AG-20", {"id": lec["id"], **cambio})
    d = dadas(b)
    vigente = cambio.get("estado", "VIGENTE") == "VIGENTE" and cambio.get("caducidad", "2099") >= AS_OF
    assert all(([x["id"] for x in d[a]] == [lec["id"]]) == vigente for a in CONTROL)
    assert all(x == {k: lec[k] for k in G.CAMPOS_PARA_EL_AGENTE} for a in CONTROL for x in d[a])


@pytest.mark.parametrize("campo", ["n", "evidencia", "nivel", "nota_nueva"])
def test_cualquier_otro_campo_deja_la_leccion_sin_dar(b, campo):
    lec = predictiva(b)
    b.almacen.escribir("F6", "AG-20", {"id": lec["id"], campo: MALA})
    assert all(v == [] for v in dadas(b).values())
