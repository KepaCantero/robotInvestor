"""T-125 r03 · Hallazgos de la QA r02: `variable` (H-09), fechas solo ISO 8601 (H-10), umbral 1 y 1.0 (H-11), dirección
que no es texto (H-12) y `run_id` en la entrada de RC de la FUE- (H-13)."""
import pytest
from bloque_a.evaluador import (
    _fecha_de_calendario,
    motivo_pronostico_fuente_no_registrable,
    variable_resoluble,
)
from test_t125_r02 import (  # ayudantes de la r02
    AS_OF,
    FUENTE_A,
    _bloque,
    _clm,
    _cuentan,
    _pf,
    _sembrar,
    _valor,
)


class _Refs:
    def por_id(self, ref_id):
        return {"archivo": "F9"} if ref_id.startswith("REF-RF-") else None


PF = {"ref_id": "REF-RF-0001", "variable": "cierre", "serie_ht01": "SPY", "fecha_objetivo": "2026-09-30",
      "umbral_o_rango": 100.0, "direccion": "por_encima", "probabilidad": 0.7, "fecha_emision": "2026-06-01"}


def _motivo(**cambios):
    pf = dict(PF, **cambios)
    return motivo_pronostico_fuente_no_registrable(pf, "REF-RF-0001", "2026-06-05", _Refs(), ["nivel", "cierre", "precio"])


def test_h09_variable_obligatoria_y_resoluble():
    assert _motivo() is None and _motivo(variable="Precio") is None
    pf = dict(PF)
    del pf["variable"]
    assert motivo_pronostico_fuente_no_registrable(pf, "REF-RF-0001", "2026-06-05", _Refs(), ["cierre"]) is not None
    for v in ("rentabilidad_12m", "", None, 3, ["cierre"]):
        assert _motivo(variable=v) is not None, v
    assert not variable_resoluble("rentabilidad", ["cierre"]) and variable_resoluble(" CIERRE ", ["cierre"])


@pytest.mark.parametrize("fecha", ["now", "today", "July 1 2026", "20260701", "1/7/2026", "2026/07/01", "01-07-2026", " "])
def test_h10_fechas_no_iso_no_se_leen(fecha):
    with pytest.raises(ValueError):
        _fecha_de_calendario(fecha)
    assert _motivo(fecha_objetivo=fecha) is not None


@pytest.mark.parametrize("fecha,dia", [("2026-07-01", "2026-07-01"), ("2026-07-01T10:30", "2026-07-01"),
                                      ("2026-07-01T23:30:00+05:00", "2026-07-01"), ("2026-07-01T00:10:00Z", "2026-07-01")])
def test_h10_las_iso_se_leen(fecha, dia):
    assert str(_fecha_de_calendario(fecha).date()) == dia


def test_h09_el_evaluador_no_cuenta_una_variable_no_resoluble(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    f = "2025-03-03"
    v = _valor(b, f)
    assert _cuentan(b, _pf(FUENTE_A, f, v - 1), clm_id="CLM-2025-0901")
    pf = _pf(FUENTE_A, "2025-03-04", v - 1)
    pf["variable"] = "rentabilidad_12m"
    _clm(b, "CLM-2025-0902", pf)
    pf2 = _pf(FUENTE_A, "2025-03-05", v - 1)
    del pf2["variable"]
    _clm(b, "CLM-2025-0903", pf2)
    assert [p["clm_id"] for p in b.evaluador.pronosticos_de_fuentes(AS_OF)] == ["CLM-2025-0901"]


def test_h11_umbral_entero_y_decimal_son_el_mismo_pronostico(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    f = "2025-03-03"
    v = float(int(_valor(b, f)))
    _clm(b, "CLM-2025-0911", _pf(FUENTE_A, f, v))
    _clm(b, "CLM-2025-0912", _pf(FUENTE_A, f, int(v)))
    assert len(b.evaluador.pronosticos_de_fuentes(AS_OF)) == 1


def test_h12_una_direccion_que_no_es_texto_no_tumba_la_fiabilidad(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    f = "2025-03-03"
    v = _valor(b, f)
    _clm(b, "CLM-2025-0921", _pf(FUENTE_A, f, v - 1))
    _clm(b, "CLM-2025-0922", _pf(FUENTE_A, "2025-03-04", v - 1, direccion=["por_encima"]))
    _clm(b, "CLM-2025-0923", _pf(FUENTE_A, "2025-03-05", v - 1, direccion={"a": 1}))
    assert [p["clm_id"] for p in b.evaluador.pronosticos_de_fuentes(AS_OF)] == ["CLM-2025-0921"]


def test_h13_la_entrada_de_rc_de_la_fue_lleva_run_id(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 6, 2)
    fue = b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0099")
    assert fue and fue[0]["ref_id"] == FUENTE_A
    rc = [e for e in b.almacen.leer("RC") if fue[0]["calc_id"] in (e.get("calc_id"), e.get("id"))]
    assert rc and all(e.get("run_id") == "RUN-2026-0099" for e in rc)
