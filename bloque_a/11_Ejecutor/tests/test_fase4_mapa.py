"""T-116 · Fase 4: el mapa verificado del Plan de pruebas V3.0 (`mapa_plan_pruebas.json`) sigue al día.

No ejecuta las pruebas citadas (eso lo hace `.docs/scripts/evidencias_plan_a.py --ejecutar`): comprueba que el mapa coincide
con el plan y que cada prueba citada existe en su fichero.
"""
import ast
import copy
import importlib.util
from pathlib import Path

import pytest

BLOQUE = Path(__file__).resolve().parents[2]
RUTA_SCRIPT = BLOQUE.parent / ".docs" / "scripts" / "evidencias_plan_a.py"


@pytest.fixture(scope="module")
def ev():
    spec = importlib.util.spec_from_file_location("evidencias_plan_a", RUTA_SCRIPT)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope="module")
def nodos(ev):
    """Identificadores de las funciones de prueba de las dos carpetas, leídos de los ficheros (sin ejecutar pytest)."""
    hallados = set()
    for carpeta in ev.CARPETAS:
        for fichero in sorted((BLOQUE / carpeta / "tests").glob("test_*.py")):
            arbol = ast.parse(fichero.read_text(encoding="utf-8"))
            for nodo in arbol.body:
                if isinstance(nodo, ast.FunctionDef) and nodo.name.startswith("test"):
                    hallados.add(f"{carpeta}/tests/{fichero.name}::{nodo.name}")
                elif isinstance(nodo, ast.ClassDef):
                    hallados |= {f"{carpeta}/tests/{fichero.name}::{nodo.name}::{m.name}" for m in nodo.body
                                 if isinstance(m, ast.FunctionDef) and m.name.startswith("test")}
    return hallados


def test_ca1_el_mapa_tiene_las_67_pruebas_del_plan(ev):
    plan, mapa = ev.leer_plan(), ev.leer_mapa()
    assert sorted(plan) == sorted(mapa) == [f"PB-{n:02d}" for n in range(1, 68)]
    assert all(p["titulo"] and p["criterio"] for p in plan.values())
    assert all(set(fila) == set(ev.CAMPOS) for fila in mapa.values())


def test_ca2_el_mapa_no_tiene_problemas_y_cada_prueba_citada_existe(ev, nodos):
    assert ev.comprobar(ev.leer_plan(), ev.leer_mapa(), nodos) == []
    citadas = {n for fila in ev.leer_mapa().values() for n in fila["pruebas"]}
    assert len(citadas) >= 80 and citadas <= nodos


def test_ca5_una_fila_sin_pruebas_nunca_resulta_superada(ev):
    mapa = ev.leer_mapa()
    todas_pasan = {n: "SUPERADA" for fila in mapa.values() for n in fila["pruebas"]}
    for pb, fila in mapa.items():
        resultado = ev.resultado_fila(fila, todas_pasan)
        if fila["cobertura"] == "AUTOMATICA":
            assert resultado == "Superada", pb
        elif fila["cobertura"] == "PARCIAL":
            assert resultado == "Superada en parte" and fila["no_comprueba"], pb
        else:
            assert not fila["pruebas"] and resultado == ev.SIN_PRUEBAS[fila["cobertura"]] and "uperada" not in resultado, pb
    con_pruebas = next(fila for fila in mapa.values() if len(fila["pruebas"]) > 1)
    assert ev.resultado_fila(con_pruebas, {}) == "No ejecutada"
    assert ev.resultado_fila(con_pruebas, {**todas_pasan, con_pruebas["pruebas"][0]: "FALLA"}) == "FALLA"
    assert ev.resultado_fila(con_pruebas, {**todas_pasan, con_pruebas["pruebas"][-1]: "NO EJECUTADA"}) == "No ejecutada"


@pytest.mark.parametrize("cambio, fragmento", [
    (lambda m: m["PB-01"]["pruebas"].append("11_Ejecutor/tests/test_integracion.py::test_que_no_existe"), "PB-01: la prueba citada no existe"),
    (lambda m: m.pop("PB-40"), "PB-40: está en el plan y falta en el mapa"),
    (lambda m: m.__setitem__("PB-99", copy.deepcopy(m["PB-01"])), "PB-99: está en el mapa y no en el plan"),
    (lambda m: m["PB-02"].__setitem__("no_comprueba", " "), "PB-02: PARCIAL sin decir qué queda sin comprobar"),
    (lambda m: m["PB-04"].__setitem__("no_comprueba", ""), "PB-04: PENDIENTE_API sin decir qué queda sin comprobar"),
    (lambda m: m["PB-01"].__setitem__("comprueba", ""), "PB-01: falta decir qué comprueban sus pruebas"),
    (lambda m: m["PB-01"].__setitem__("pruebas", []), "PB-01: AUTOMATICA con 0 pruebas citadas"),
    (lambda m: m["PB-04"].__setitem__("pruebas", list(m["PB-01"]["pruebas"])), "PB-04: PENDIENTE_API con 2 pruebas citadas"),
    (lambda m: m["PB-01"].__setitem__("cobertura", "SUPERADA"), "PB-01: cobertura desconocida 'SUPERADA'"),
    (lambda m: m["PB-01"]["pruebas"].append(m["PB-01"]["pruebas"][0]), "PB-01: pruebas repetidas"),
    (lambda m: m["PB-01"].pop("comprueba"), "PB-01: campos"),
])
def test_ca6_un_mapa_estropeado_se_detecta(ev, nodos, cambio, fragmento):
    mapa = copy.deepcopy(ev.leer_mapa())
    cambio(mapa)
    problemas = ev.comprobar(ev.leer_plan(), mapa, nodos)
    assert any(p.startswith(fragmento) for p in problemas), problemas


def test_las_ordenes_para_repetir_una_fila_van_por_carpeta(ev):
    mapa = ev.leer_mapa()
    ordenes = ev.orden(mapa["PB-12"])
    assert len(ordenes) == 2 and ordenes[0].startswith("(cd bloque_a/11_Ejecutor && ") and ordenes[1].startswith("(cd bloque_a/10_Herramientas && ")
    assert all("'tests/test_" in o and "11_Ejecutor/tests" not in o.split("&&")[1] for o in ordenes)
    assert ev.orden(mapa["PB-04"]) == []


def test_el_documento_tiene_una_fila_por_prueba_del_plan(ev):
    plan, mapa = ev.leer_plan(), ev.leer_mapa()
    todas_pasan = {n: "SUPERADA" for fila in mapa.values() for n in fila["pruebas"]}
    doc = ev.documento(plan, mapa, todas_pasan, "2026-11-13", "abc1234")
    tabla = [linea for linea in doc.splitlines() if linea.startswith("| PB-")]
    assert len(tabla) == 67 and "| **Total** | **67** |" in doc
    assert sum("| Superada |" in linea for linea in tabla) == sum(f["cobertura"] == "AUTOMATICA" for f in mapa.values())
    assert doc.count("### PB-") == sum(bool(f["pruebas"]) for f in mapa.values())
    sin_ejecutar = ev.documento(plan, mapa, {}, "2026-11-13", "abc1234")
    assert "| Superada" not in sin_ejecutar and "| No ejecutada |" in sin_ejecutar
