"""QA r01 de T-171 · Integración: lo que pasa el detector (ataques de `r01_01_reservado_revisor.py`) no llega a ningún agente de
control. Una guía con esos ítems a un control no se emite, ni siquiera con la simulación del fallo del emisor; a un Analista
se emite y, en un ciclo, no llega a AG-11, AG-18, AG-19 ni AG-20 (ni como lección). Una lección de AG-20 con un ataque de
lecciones que pasa el detector llega a los demás y a ningún control.

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -s -p no:cacheprovider ../../.docs/tickets/T-171/revisores/r01_02_integracion.py
"""
import copy
import importlib.util
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
from bloque_a.contratos import MensajeInvalido  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402

_spec = importlib.util.spec_from_file_location("r01_01", Path(__file__).resolve().parent / "r01_01_reservado_revisor.py")
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)
CONTROL = tuple(sorted(G.AGENTES_DE_CONTROL))
PASAN = [t for _, t in R.ATAQUES if G.conflicto_para({**R.BASE, "que_cambia": t}, "AG-03") is None]
LEC_PASAN = [(o, r) for _, o, r in R.LECCIONES_ATAQUE
             if G.conflicto_de_leccion({"tipo": "OPERATIVA", "ambito": {}, "observacion": o, "recomendacion": r}) is None]


@pytest.fixture(scope="module")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


@pytest.fixture
def b(tmp_path, universo):
    x = nuevo_bloque(tmp_path, universo)
    x.fijar_fecha(AS_OF)
    return x


def items(textos):
    return [{**R.BASE, "que_cambia": t} for t in textos]


def test_hay_ataques_que_pasan():
    print(f"pasan {len(PASAN)} ítems y {len(LEC_PASAN)} lecciones del juego reservado")
    assert PASAN and LEC_PASAN


@pytest.mark.parametrize("agente", CONTROL)
@pytest.mark.parametrize("simular", [False, True])
def test_una_guia_con_lo_que_pasa_no_se_emite_a_un_control(b, agente, simular):
    """Sin la simulación, el emisor la rechaza; con ella (PB-48, solo con el cliente simulado), el receptor no la aplica."""
    if simular:
        b.guias.emitir(agente, items(PASAN[:3]), as_of=AS_OF, simular_fallo_del_emisor=True)
    else:
        with pytest.raises(MensajeInvalido):
            b.guias.emitir(agente, items(PASAN[:3]), as_of=AS_OF)
    assert b.guias.para(agente, AS_OF, "RUN-1") == []


def test_en_un_ciclo_lo_que_pasa_solo_llega_al_analista(b, monkeypatch):
    b.guias.emitir("AG-03", items(PASAN[:6]), as_of=AS_OF)
    vistos = []
    inv = b.agentes.invocar

    def invocar(agente, contrato, mensaje, esquema, instrucciones, contexto, *a, **kw):
        vistos.append((agente, copy.deepcopy(contexto)))
        return inv(agente, contrato, mensaje, esquema, instrucciones, contexto, *a, **kw)
    monkeypatch.setattr(b.agentes, "invocar", invocar)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    marca = G._normalizar(PASAN[0])[:25]
    con = sorted({a for a, c in vistos if marca in G._normalizar(json.dumps(c, ensure_ascii=False))})
    print("el texto de la guía aparece en el contexto de:", con, "; invocados:", sorted({a for a, _ in vistos}))
    assert "AG-03" in con and not set(con) & set(CONTROL)


def test_una_leccion_que_pasa_el_detector_no_llega_a_un_control(b):
    for o, r in LEC_PASAN:
        b.evaluador._nueva_leccion(pd.Timestamp(AS_OF), {}, "OPERATIVA", o, r, "anecdotica", ["RUN"], 1, origen="AG-20")
    vig = b.evaluador.lecciones_vigentes(AS_OF)
    assert len(b.guias.lecciones_para("AG-03", vig, AS_OF, "RUN-X")) == min(len(LEC_PASAN), len(vig))
    assert all(b.guias.lecciones_para(a, vig, AS_OF, "RUN-X") == [] for a in CONTROL)
