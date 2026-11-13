"""T-117 · GC1 del diseño V6: umbral por tipo de activo y concordancia de familias de la señal compuesta (Anexo A)."""
import pytest
from bloque_a.configuracion import CLASES, cargar_config, parametro
from conftest import AS_OF, config_pruebas
from test_t101_v6 import _bloque

from bloque_a import diseno_v6 as v6


def _cfg(**gc1):
    return config_pruebas(diseno="v6", v6={"gc1": gc1} if gc1 else {})


def _amb(simbolo, senal, familias=None, **otras):
    senales = {"senal_compuesta": senal, **otras}
    if familias is not None:
        senales["familias_concordantes"] = familias
    return {"simbolo": simbolo, "senales": senales}


UNIVERSO = [_amb("A", 0.80, 3), _amb("B", 0.70, 2), _amb("C", 0.66, 1), _amb("D", 0.60, 2), _amb("E", 0.90, 1), _amb("F", 0.68)]


def _marcas(b, clase, universo=UNIVERSO):
    filtrado, reg = v6.gc1(b, clase, universo, [], AS_OF)
    return {u["simbolo"]: u["gc1"] for u in filtrado}, reg


# ---------------------------------------------------------------- valores por defecto
def test_los_valores_por_defecto_son_los_decididos():
    cfg = cargar_config()
    assert parametro(cfg, "v6.gc1.senal_por_perfil") == {c: "senal_compuesta" for c in CLASES}
    assert parametro(cfg, "v6.gc1.umbral_por_perfil") == {"RF": 0.65, "MON": 0.65, "TCV": 0.65}
    assert parametro(cfg, "v6.gc1.familias_min") == 2
    assert parametro(cfg, "seleccion.umbral_senal_gc1") == 0.75 and cfg["diseno"] == "v5"   # el Anexo A y el diseño por defecto no cambian


# ---------------------------------------------------------------- umbral por tipo
def test_el_umbral_del_tipo_manda_y_los_demas_usan_el_general(tmp_path):
    b = _bloque(tmp_path, _cfg(exploracion_celdas=0))
    rf, reg_rf = _marcas(b, "RF")
    rv, reg_rv = _marcas(b, "RV")
    assert reg_rf["umbral"] == 0.65 and reg_rv["umbral"] == 0.75 and reg_rf["familias_min"] == reg_rv["familias_min"] == 2
    assert reg_rf["pasan"] == ["A", "B", "F"]            # C y E llegan al umbral con una sola familia; D no llega
    assert reg_rv["pasan"] == ["A"]                      # con 0,75, B y F no llegan
    assert rf == {"A": "PASA", "B": "PASA", "F": "PASA"} and rv == {"A": "PASA"}
    motivos = {d["simbolo"]: d["motivo"] for d in reg_rf["descartes"]}
    assert motivos == {"C": "1 familias concordantes < 2", "E": "1 familias concordantes < 2", "D": "senal_compuesta 0.60 < 0.65"}


@pytest.mark.parametrize("clase, umbral", [(c, 0.65 if c in ("RF", "MON", "TCV") else 0.75) for c in CLASES])
def test_cada_tipo_usa_su_umbral(tmp_path, clase, umbral):
    b = _bloque(tmp_path, _cfg())
    assert v6.gc1(b, clase, UNIVERSO, [], AS_OF)[1]["umbral"] == umbral


def test_el_borde_del_umbral_pasa_y_un_pelo_menos_no(tmp_path):
    b = _bloque(tmp_path, _cfg(exploracion_celdas=0))
    _, reg = _marcas(b, "RF", [_amb("JUSTO", 0.65, 2), _amb("CASI", 0.6499, 3)])
    assert reg["pasan"] == ["JUSTO"] and reg["descartes"][0]["simbolo"] == "CASI"


def test_para_volver_al_umbral_general_en_un_tipo_se_le_pone_ese_valor(tmp_path):
    """La configuración se fusiona por claves: un diccionario vacío no borra los valores por defecto."""
    b = _bloque(tmp_path, _cfg(umbral_por_perfil={}, exploracion_celdas=0))
    assert _marcas(b, "RF")[1]["umbral"] == 0.65
    b = _bloque(tmp_path / "b", _cfg(umbral_por_perfil={"RF": 0.75}, exploracion_celdas=0))
    assert _marcas(b, "RF")[1]["umbral"] == 0.75 and _marcas(b, "RF")[1]["pasan"] == ["A"]
    assert _marcas(b, "MON")[1]["umbral"] == 0.65


# ---------------------------------------------------------------- concordancia de familias
def test_sin_el_recuento_de_familias_no_se_descarta_por_ello(tmp_path):
    b = _bloque(tmp_path, _cfg(exploracion_celdas=0))
    _, reg = _marcas(b, "RV", [_amb("SIN", 0.9), _amb("NULO", 0.9, None, familias_concordantes=None), _amb("CERO", 0.9, 0)])
    assert reg["pasan"] == ["NULO", "SIN"] and [d["simbolo"] for d in reg["descartes"]] == ["CERO"]


def test_con_familias_min_cero_no_se_exige_concordancia(tmp_path):
    b = _bloque(tmp_path, _cfg(familias_min=0, exploracion_celdas=0))
    _, reg = _marcas(b, "RF")
    assert reg["pasan"] == ["A", "B", "C", "E", "F"] and reg["familias_min"] == 0


def test_la_concordancia_solo_se_exige_cuando_manda_la_senal_compuesta(tmp_path):
    b = _bloque(tmp_path, _cfg(senal_por_perfil={"DIV": "pct_momentum_clase"}, exploracion_celdas=0))
    uni = [_amb("A", 0.1, 0, pct_momentum_clase=0.9), _amb("B", 0.9, 3, pct_momentum_clase=0.2)]
    _, reg = _marcas(b, "DIV", uni)
    assert reg["clave_senal"] == "pct_momentum_clase" and reg["familias_min"] == 0 and reg["pasan"] == ["A"]


def test_con_tres_familias_y_075_la_concordancia_no_cambia_nada():
    """Con las tres familias en [0, 1], una media de 0,75 o más obliga a que dos lleguen a 0,6: 0,75 × 3 = 2,25 > 1 + 0,6 + 0,6."""
    pasos = [i / 20 for i in range(21)]
    for a in pasos:
        for b_ in pasos:
            for c in pasos:
                if (a + b_ + c) / 3 >= 0.75:
                    assert sum(x >= 0.6 for x in (a, b_, c)) >= 2


def test_un_descartado_por_familias_puede_llegar_como_exploracion(tmp_path):
    b = _bloque(tmp_path, _cfg(exploracion_celdas=6))
    marcas, reg = _marcas(b, "RF")
    assert {s for s, m in marcas.items() if m == "EXPLORACION"} == {"C", "D", "E"} and reg["descartes"] == []


# ---------------------------------------------------------------- la configuración inválida se rechaza al crear el Bloque
@pytest.mark.parametrize("gc1", [
    {"umbral_por_perfil": {"XX": 0.5}}, {"umbral_por_perfil": {"RF": 0}}, {"umbral_por_perfil": {"RF": 1.01}},
    {"umbral_por_perfil": {"RF": -0.1}}, {"umbral_por_perfil": {"RF": "0.6"}}, {"umbral_por_perfil": {"RF": True}},
    {"umbral_por_perfil": {"RF": float("nan")}}, {"umbral_por_perfil": {"RF": float("inf")}}, {"umbral_por_perfil": [0.6]},
    {"umbral_por_perfil": {"RF": None}}, {"familias_min": -1}, {"familias_min": 4}, {"familias_min": 1.5}, {"familias_min": True},
    {"familias_min": "2"},
])
def test_una_configuracion_invalida_se_rechaza(tmp_path, gc1):
    with pytest.raises(ValueError, match="v6.gc1"):
        _bloque(tmp_path, _cfg(**gc1))


@pytest.mark.parametrize("gc1", [{"umbral_por_perfil": {"RF": 1}}, {"umbral_por_perfil": {"RF": 0.01, "ALT": 1.0}}, {"familias_min": 0},
                                 {"familias_min": 3}, {"umbral_por_perfil": None}])
def test_una_configuracion_valida_se_acepta(tmp_path, gc1):
    assert _bloque(tmp_path, _cfg(**gc1))


def test_en_el_diseno_v5_nada_cambia(tmp_path):
    b = _bloque(tmp_path, config_pruebas())
    assert not b.v6 and parametro(b.cfg, "seleccion.umbral_senal_gc1") == 0.75


# ---------------------------------------------------------------- en un ciclo
def test_en_un_ciclo_el_registro_de_gc1_lleva_el_umbral_de_cada_tipo(tmp_path):
    b = _bloque(tmp_path, config_pruebas(diseno="v6"))
    b.ciclo(AS_OF, alcance={"clases": ["RF", "RV"]})
    cob = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "COBERTURA"][-1]["clases"]
    assert cob["RF"]["gc1"]["umbral"] == 0.65 and cob["RV"]["gc1"]["umbral"] == 0.75
    for clase in ("RF", "RV"):
        g = cob[clase]["gc1"]
        assert g["clave_senal"] == "senal_compuesta" and g["familias_min"] == 2
