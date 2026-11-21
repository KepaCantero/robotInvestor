import pytest
from conftest import AS_OF, nuevo_bloque

from bloque_a import sintesis


@pytest.mark.parametrize("fallo", [1, 2])
def test_ciclo_bloqueado_y_registrado(tmp_path, universo, monkeypatch, fallo):
    b = nuevo_bloque(tmp_path, universo)
    original = sintesis.ht09_validar
    llamadas = []
    def control(*args):
        llamadas.append(True)
        if len(llamadas) == fallo:
            raise RuntimeError("Verificador no disponible")
        return original(*args)
    monkeypatch.setattr(sintesis, "ht09_validar", control)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["estado"] == "PARCIAL" and r["entrega"] == "BLOQUEADA"
    assert b.almacen.estado("F5")[r["run_id"]]["entrega"] == "BLOQUEADA"
    assert any(m["contrato"] == "CT-14" and m["receptor"] == "AG-18" for m in b.mensajeria.registro)
    assert any(e.get("tipo_control") == "G3_MANUAL" and e["dictamen_efectivo"] == "BLOQUEADO" for e in b.almacen.leer("HA"))
    assert not b.almacen.leer("F4")
