"""T-187 · PB-51 del plan de pruebas: conocimiento específico en los system prompts (revisión documental).

La revisión la hace `.docs/scripts/revision_prompts_pb51.py` (sin red y determinista; sus datos, en `.docs/tickets/T-187/`)
y el contraste de la muestra, cuatro revisores independientes (`.docs/tickets/T-187/veredictos/`). Esta prueba ata el
resultado al corpus actual: si cambian los prompts, el Documento 0, la configuración o los veredictos, el informe guardado
deja de coincidir y la prueba falla hasta que se repita la revisión. Criterios `[PROPUESTO]` en INC-T187-01 y
INC-T187-02 (`docs/incidencias.md`).
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

BLOQUE = Path(__file__).resolve().parents[2]
RAIZ = BLOQUE.parent
SCRIPTS = RAIZ / ".docs" / "scripts"
TICKET = RAIZ / ".docs" / "tickets" / "T-187"
MAPA = BLOQUE / "11_Ejecutor" / "tests" / "mapa_plan_pruebas.json"


@pytest.fixture(scope="module")
def rp():
    spec = importlib.util.spec_from_file_location("revision_prompts_pb51", SCRIPTS / "revision_prompts_pb51.py")
    assert spec and spec.loader
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["revision_prompts_pb51"] = modulo        # las dataclass lo buscan ahí
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope="module")
def revision(rp):
    revs, anexo, _ = rp.revisar(RAIZ)
    return revs, anexo


def test_pb51_el_informe_y_la_muestra_guardados_son_los_del_corpus_y_los_veredictos_actuales(rp):
    assert rp.principal(["--raiz", str(RAIZ), "--salida", str(TICKET), "--comprobar"]) == 0


def test_pb51_paso_1_todos_los_prompts_con_las_secciones_del_anexo_g(revision):
    revs, anexo = revision
    prompts = [r for r in revs if not r.plantilla]
    assert len(anexo) == 12 and len(prompts) == 35
    assert all(r.estructura["completa"] for r in prompts)


def test_pb51_paso_2_seccion_10_por_areas_con_formulas_y_referencias_sin_doi_invalidos(revision):
    revs, _ = revision
    for r in (r for r in revs if not r.plantilla):
        filas = [f for f in r.recuento if not f["excluida"]]
        assert [f for f in r.recuento if not f["subarea"].endswith(".0")], r.agente
        assert sum(f["formulas"] for f in filas) > 0 and sum(f["referencias"] for f in filas) > 0, r.agente
    assert all(d["estructura_valida"] for r in revs for d in r.identificadores["doi"])


def test_pb51_paso_3_al_menos_95_por_ciento_de_las_verificables_correctas(rp, revision):
    revs, _ = revision
    c = rp.leer_contraste(TICKET / "veredictos", rp.afirmaciones(revs))
    assert c["n"] == 350 and c["supera"] and 100 * c["correctas"] >= rp.UMBRAL_CORRECTAS * c["verificables"]
    guardada = json.loads((TICKET / "muestra_afirmaciones.json").read_text(encoding="utf-8"))
    assert [a["id"] for a in guardada["afirmaciones"]] == [a["id"] for a in rp.afirmaciones(revs)]


def test_pb51_tamanos_dentro_de_las_orientaciones_escritas(revision):
    revs, _ = revision
    con_tope = [r for r in revs if not r.plantilla and r.tamano["dentro"] is not None]
    assert len(con_tope) == 14 and all(r.tamano["dentro"] for r in con_tope)


def test_pb51_fila_del_mapa_superada_en_parte():
    """QA r01, H-01: con 9 ERRONEA (el resultado esperado dice «ninguna») y 21 papeles sin orientación de tamaño, PB-51
    no comprueba todo el criterio del plan: «Superada en parte», con las dos cosas en «No comprueba»."""
    fila = json.loads(MAPA.read_text(encoding="utf-8"))["PB-51"]
    assert fila["cobertura"] == "PARCIAL"
    nc = fila["no_comprueba"]
    for frase in ("ninguna afirmación técnica errónea", "INC-T187-03", "21 papeles", "afirmaciones técnicas por prompt"):
        assert frase in nc, frase
    assert nc.index("ninguna afirmación técnica errónea") < nc.index("21 papeles")
    assert "(10 por prompt)" not in fila["comprueba"]
