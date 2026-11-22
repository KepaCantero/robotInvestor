import pytest
from bloque_a.contratos import DatosSensibles
from conftest import AS_OF, nuevo_bloque


def test_ct04_rechaza_lista_global_incompatible(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    antes = b.f10("2026-06-08").get("P-03")
    b.decision({"configuracion": {"clases_activas": ["ALT"], "horizontes": ["H1"]}}, AS_OF)
    assert b.f10("2026-06-08").get("P-03") == antes
    assert b.f10("2026-06-08")["P-02"] == ["ALT"]


def test_seguridad_solo_etiquetas(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    with pytest.raises(DatosSensibles):
        b.decision({"valoracion_informe": {"nota": "ES91 2100 " + "0418 4502 0005 1332",
                                           "api_key": "valor-" + "ficticio"}}, AS_OF)
    inc = b.almacen.leer("HA")[-1]
    assert set(inc["tipos_dato"]) == {"IBAN", "CLAVE_API"}


def test_aut_con_valor_ganado(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["MP"]}, presupuesto_override={"MP": 6.0})
    aut = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "AUT" and e.get("bolsa") == "MP"]
    assert {e["decision"] for e in aut} == {"AUTORIZADA", "DENEGADA"}
    assert r["presupuesto"]["MP"]["consumido"] > 0
    for e in aut:
        if e["ev"] and e["ac"]:
            assert e["cpi"] == pytest.approx(e["ev"] / e["ac"])
            assert e["eac"] == pytest.approx(e["ac"] + (e["bac"] - e["ev"]) / e["cpi"])
        else:
            assert e["eac"] is None
