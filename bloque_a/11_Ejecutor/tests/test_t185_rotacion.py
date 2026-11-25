import hashlib
import json
from pathlib import Path

import jsonschema
import pytest
from bloque_a.configuracion import parametro
from conftest import AS_OF, config_pruebas, nuevo_bloque

EJ = Path(__file__).resolve().parents[1]
SEGUNDO = "2026-06-12"


def _n1(tmp_path, universo, fraccion=0.2, primero=True):
    cfg = config_pruebas(presupuesto_uc={"rotacion_exploratoria": fraccion})
    b = nuevo_bloque(tmp_path, universo, cfg=cfg)
    _espiar(b)
    if primero:
        b.ciclo(AS_OF, alcance={"clases": ["RF"]})
    r = b.ciclo(SEGUNDO, tipo="AD_HOC", alcance={"clases": ["RF"]}, nivel_forzado="N1")
    return b, r


def _espiar(b):
    b._qa_msgs = []
    crear = b.mensajeria.crear

    def crear_y_anotar(*args, **kwargs):
        msg = crear(*args, **kwargs)
        b._qa_msgs.append(json.loads(json.dumps(msg, default=str)))
        return msg
    b.mensajeria.crear = crear_y_anotar


def _ct06(b, run_id):
    out = [m for m in b._qa_msgs if m["contrato"] == "CT-06" and m.get("run_id") == run_id and m.get("tipo_mensaje") == "ENCARGO"]
    assert out, "sin CT-06 de ese run"
    return out


# --- H-01: el valor de la bolsa de cribado de N1 no lo comprueba ninguna prueba --------------------------------------
def test_rotacion_presupuestada_en_f5(tmp_path, universo):
    b, r = _n1(tmp_path, universo)
    plan = b.almacen.estado("F5")[r["run_id"]]["cribado_n1"]["RF"]
    esperado = parametro(b.cfg, "presupuesto_uc.N1") * parametro(b.cfg, "presupuesto_uc.reparto_fases.cribado")
    assert plan["uc_cribado"] == pytest.approx(esperado) == 1.75
    assert plan["uc_rotacion"] == pytest.approx(0.35)
    assert plan["uc_vigentes"] == pytest.approx(1.40)
    assert plan["simbolos"]


def test_h01_reparto_del_ct06_es_el_de_f5(tmp_path, universo):
    b, r = _n1(tmp_path, universo)
    plan = b.almacen.estado("F5")[r["run_id"]]["cribado_n1"]["RF"]
    (msg,) = _ct06(b, r["run_id"])
    cuerpo = msg.get("cuerpo", msg)
    assert cuerpo["reparto_cribado"] == plan
    assert cuerpo["reparto_cribado"]["simbolos"] == cuerpo["rotacion_exploratoria"]


# --- H-02: fracción nula, fuera de rango o con tipo inesperado: sin pruebas ------------------------------------------
def test_h02_fraccion_nula_no_explora(tmp_path, universo):
    b, r = _n1(tmp_path, universo, fraccion=0)
    plan = b.almacen.estado("F5")[r["run_id"]]["cribado_n1"]["RF"]
    assert plan["uc_rotacion"] == 0 and plan["simbolos"] == []
    for m in _ct06(b, r["run_id"]):
        cuerpo = m.get("cuerpo", m)
        assert cuerpo["rotacion_exploratoria"] == []


@pytest.mark.parametrize("malo", [1.5, -0.1, True, "0.2", None, float("nan")])
def test_h02_fraccion_invalida_falla_cerrado(tmp_path, universo, malo):
    cfg = config_pruebas(presupuesto_uc={"rotacion_exploratoria": malo})
    bloque = nuevo_bloque(tmp_path, universo, cfg=cfg)
    def huellas():
        return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in bloque.almacen.carpeta.rglob("*") if p.is_file()}
    antes = huellas()
    with pytest.raises(ValueError, match="Fracción de rotación"):
        bloque.ciclo(AS_OF, alcance={"clases": ["RF"]}, nivel_forzado="N2")
    assert huellas() == antes


# --- CT-06: el esquema derivado del Anexo B admite el campo nuevo y los ejemplos no cambian --------------------------
def test_esquema_derivado_admite_reparto(tmp_path, universo):
    esquemas = json.loads((EJ / "tests/goldens/anexo_b_esquemas.json").read_text())
    b, r = _n1(tmp_path, universo)
    for m in _ct06(b, r["run_id"]):
        cuerpo = m.get("cuerpo", m)
        assert "reparto_cribado" in cuerpo
        jsonschema.validate(cuerpo, esquemas["CT-06.ENCARGO"])


def test_n2_no_lleva_reparto(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    _espiar(b)
    r = b.ciclo(AS_OF, alcance={"clases": ["RF"]})
    assert r["nivel_por_clase"]["RF"] in ("N2", "N3")
    assert all("reparto_cribado" not in m.get("cuerpo", m) for m in _ct06(b, r["run_id"]))
    assert b.almacen.estado("F5")[r["run_id"]]["cribado_n1"] == {}


def test_mapa_declara_limite_de_la_rotacion():
    limite = json.loads((EJ / "tests/mapa_plan_pruebas.json").read_text())["PB-13"]["no_comprueba"]
    assert "INC-T185-01" in limite and "rotacion_exploratoria_celdas" in limite
