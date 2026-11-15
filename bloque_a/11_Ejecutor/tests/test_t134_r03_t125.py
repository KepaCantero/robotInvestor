"""T-134 · Hallazgos de la QA r03 de T-125: enteros enormes (H-14, H-15), cifras no ASCII y zona sin hora en las fechas
(H-16), `variables_nivel` sin validar (H-17) y dos conexiones del ciclo sin prueba (H-18)."""
import pytest
from bloque_a.almacen import Almacen
from bloque_a.evaluador import (
    Evaluador,
    _fecha_de_calendario,
    motivo_pronostico_fuente_no_registrable,
)
from conftest import AS_OF, config_pruebas, nuevo_bloque
from test_t125_r02 import (
    FUENTE_A,
    _analista_con_pronosticos,
    _bloque,
    _clm,
    _pf,
    _valor,
    _vivo,
)

ENORME = 10 ** 400


class _Refs:
    def por_id(self, ref_id):
        return {"archivo": "F9"} if ref_id.startswith("REF-RF-") else None


PF = {"ref_id": "REF-RF-0001", "variable": "cierre", "serie_ht01": "SPY", "fecha_objetivo": "2026-09-30",
      "umbral_o_rango": 100.0, "direccion": "por_encima", "probabilidad": 0.7, "fecha_emision": "2026-06-01"}


def _motivo(**cambios):
    return motivo_pronostico_fuente_no_registrable(dict(PF, **cambios), "REF-RF-0001", "2026-06-05", _Refs(), ["cierre"])


@pytest.mark.parametrize("cambio", [{"umbral_o_rango": ENORME}, {"umbral_o_rango": -ENORME},
                                    {"direccion": "dentro", "umbral_o_rango": [1, ENORME]}, {"probabilidad": ENORME}])
def test_h14_un_entero_enorme_no_lanza_y_no_se_registra(cambio):
    assert _motivo(**cambio) is not None


def test_h15_un_entero_enorme_en_f2_no_hace_perder_la_fue_de_las_demas(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    f = "2025-03-03"
    v = _valor(b, f)
    _clm(b, "CLM-2025-0931", _pf(FUENTE_A, f, v - 1))
    _clm(b, "CLM-2025-0932", _pf(FUENTE_A, "2025-03-04", ENORME))
    _clm(b, "CLM-2025-0933", _pf(FUENTE_A, "2025-03-05", [1, ENORME], direccion="dentro"))
    assert [p["clm_id"] for p in b.evaluador.pronosticos_de_fuentes(AS_OF)] == ["CLM-2025-0931"]


@pytest.mark.parametrize("fecha", ["２０２６-０７-０１", "٢٠٢٦-٠٧-٠١", "२०२६-०७-०१", "2026-07-01-05:00", "2026-07-01Z"])
def test_h16_cifras_no_ascii_y_zona_sin_hora(fecha):
    with pytest.raises(ValueError):
        _fecha_de_calendario(fecha)


@pytest.mark.parametrize("fecha", ["2026-07-01", "2026-07-01T10:30Z", "2026-07-01T10:30:00+05:00", "2026-07-01 10:30:00+0500"])
def test_h16_las_iso_validas_se_siguen_leyendo(fecha):
    assert str(_fecha_de_calendario(fecha).date()) == "2026-07-01"


@pytest.mark.parametrize("valor", ["cierre", 3, [], [""], ["cierre", 4]])
def test_h17_variables_nivel_mal_formada_falla_al_crear_el_evaluador(tmp_path, valor):
    cfg = config_pruebas(fiabilidad_fuentes={"variables_nivel": valor})
    with pytest.raises(ValueError, match="variables_nivel"):
        Evaluador(Almacen(tmp_path), None, None, cfg, None)


def test_h17_sin_variables_nivel_falla_cerrado(tmp_path):
    with pytest.raises(KeyError, match="variables_nivel"):   # una clave nula es una clave ausente (regla de `parametro`)
        Evaluador(Almacen(tmp_path), None, None, config_pruebas(fiabilidad_fuentes={"variables_nivel": None}), None)


def test_h18_el_c5_pasa_el_run_id_a_la_fiabilidad(tmp_path, universo, monkeypatch):
    _analista_con_pronosticos(monkeypatch)
    b = _vivo(tmp_path, universo)
    b.ciclo("2026-04-03", alcance={"clases": ["RV"]})
    r2 = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    fue = r2["evaluacion"]["fiabilidad_fuentes"]
    assert fue
    rc = [e for e in b.almacen.leer("RC") if fue[0]["calc_id"] in (e.get("calc_id"), e.get("id"))]
    assert rc and all(e.get("run_id") == r2["run_id"] for e in rc)


def test_h18_el_alta_en_f2_usa_la_lista_de_la_configuracion(tmp_path, universo, monkeypatch):
    # con «cierre» fuera de la lista, los bloques del Analista simulado (variable «cierre») no entran en F2
    _analista_con_pronosticos(monkeypatch)
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(modo="vivo", fiabilidad_fuentes={"variables_nivel": ["nivel"]}))
    b.ciclo("2026-04-03", alcance={"clases": ["RV"]})
    f2 = [c for c in b.almacen.estado("F2", clave="clm_id").values() if c.get("tipo_entrada") == "CLM"]
    assert not [c for c in f2 if isinstance(c.get("pronostico_fuente"), dict)]
    assert any("no resoluble con el cierre" in e.get("detalle", "") for e in b.almacen.leer("HA"))
