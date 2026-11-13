"""T-112 · Motor Fase 2, grupo S (estadística y series): ST-INF-001, FX-BRK-001, FX-STL-001, FX-REGIME-001, REG-HMM-001,
FX-COINT-001, BIB-MET-001 y TEM-DIFF-001 del Catálogo V5.0.

Por ficha: casos de control de su «Verificación», rechazos de «Aclaración y rechazo» y de «Entradas mínimas», dominio de
cada parámetro, umbrales fijos, determinismo de dos pasadas, entradas hostiles y al menos un oráculo independiente (el
resultado recalculado por otra vía, sin llamar al código de la ficha)."""
import collections
import copy
import json
import math

import numpy as np
import pandas as pd
import pytest
from bloque_a.motor import fichas_series as S
from bloque_a.motor.operaciones import ErrorFicha
from scipy import optimize, stats

FICHAS = sorted(S.FICHAS)


def _ent(valores, series=None):
    return {"valores": copy.deepcopy(valores), "series": series or {}, "series_rol": {}}


def _correr(ficha, valores, params=None, series=None):
    return S.FICHAS[ficha]["fn"](_ent(valores, series), params or {})


def _valores_caso(caso):
    v = {}
    for d in caso["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    return v


def _rechaza(ficha, valores, params=None, texto=None, series=None):
    with pytest.raises(ErrorFicha) as e:
        _correr(ficha, valores, params, series)
    if texto:
        assert texto in str(e.value), str(e.value)
    return str(e.value)


def _serie_fechas(valores, inicio="2015-01-02", freq="W-FRI"):
    return pd.Series(list(valores), index=pd.date_range(inicio, periods=len(valores), freq=freq))


# Entrada base de cada ficha (rápida) para determinismo, umbrales y hostiles
BASE = {
    "ST-INF-001": ({"contrastes": [{"nombre": "a", "muestra": [0.3, 1.2, -0.4, 0.8, 1.9, 0.1]},
                                   {"nombre": "b", "muestra": [2.0, 1.5, 2.2, 1.1, 2.8, 1.7]}]},
                   {"tipo_contraste": "t_una_muestra"}),
    "FX-BRK-001": ({"serie": list(S._Y_NIVEL)}, {}),
    "FX-STL-001": ({"serie": list(S._Y_STL_RUIDO)}, {"periodo": 12}),
    "FX-REGIME-001": ({"serie": list(S._X_REGIME)}, {}),
    "REG-HMM-001": ({"variables": S._HMM_VARIABLES, "fechas": S._HMM_FECHAS}, {"n_estados": 2}),
    "FX-COINT-001": ({"series": S._PAR}, {}),
    "BIB-MET-001": ({"fichas": S._FICHAS_BIB}, {}),
    "TEM-DIFF-001": ({"adopcion": S._LOG, "anios": S._ANIOS}, {"B": 40}),
}


# ============================================================================= registro
def test_registro_de_las_ocho_fichas():
    esperadas = {"ST-INF-001", "FX-BRK-001", "FX-STL-001", "FX-REGIME-001", "REG-HMM-001", "FX-COINT-001", "BIB-MET-001",
                 "TEM-DIFF-001"}
    assert set(S.FICHAS) == set(S.PARAMETROS_POR_DEFECTO) == set(S.UMBRALES) == set(S.ADVERTENCIAS) \
        == set(S.CASOS_CONTROL) == esperadas
    for f, meta in S.FICHAS.items():
        assert set(meta) == {"fn", "modulo", "version", "cifra", "ri", "tol"} and callable(meta["fn"])
        assert meta["cifra"] in ("DETERMINISTA", "ESTADISTICA") and meta["ri"] and meta["tol"] > 0
        assert len(S.CASOS_CONTROL[f]) >= 2, f
        assert not set(S.PARAMETROS_POR_DEFECTO[f]) & set(S.UMBRALES[f]), f
    # Tolerancias y versiones del campo «Tolerancias y semilla» e «Identificación» de cada ficha
    assert {f: S.FICHAS[f]["tol"] for f in FICHAS} == {
        "BIB-MET-001": 1e-10, "FX-BRK-001": 1e-6, "FX-COINT-001": 1e-6, "FX-REGIME-001": 1e-6, "FX-STL-001": 1e-6,
        "REG-HMM-001": 1e-6, "ST-INF-001": 1e-8, "TEM-DIFF-001": 1e-6}
    assert S.FICHAS["REG-HMM-001"]["version"] == S.FICHAS["TEM-DIFF-001"]["version"] == "1.0"
    assert S.FICHAS["FX-COINT-001"]["modulo"] == "MC-03" and S.FICHAS["TEM-DIFF-001"]["modulo"] == "MC-04"
    assert S.FICHAS["BIB-MET-001"]["cifra"] == "DETERMINISTA"


def test_parametros_por_defecto_de_cada_ficha():
    P = S.PARAMETROS_POR_DEFECTO
    assert P["FX-BRK-001"] == {"max_rupturas": 1, "tipo_cambio": "auto", "nivel": 0.05, "recorte": 0.15}
    assert P["FX-REGIME-001"]["n_estados"] == 2 and P["FX-REGIME-001"]["umbral"] == 0.5
    assert P["FX-REGIME-001"]["varianzas_distintas"] is True and P["FX-REGIME-001"]["medias_distintas"] is False
    assert P["REG-HMM-001"]["n_estados"] == "BIC" and P["REG-HMM-001"]["arranques"] == 20
    assert P["REG-HMM-001"]["covarianza"] == "diagonal"
    assert P["FX-COINT-001"] == {"metodo": "Johansen", "max_rezagos": "AIC", "nivel": 0.05}
    assert P["TEM-DIFF-001"]["arranques"] == 20 and P["TEM-DIFF-001"]["B"] == 1000
    assert P["ST-INF-001"]["tipo_contraste"] is None and P["ST-INF-001"]["alternativa"] == "bilateral"
    assert P["BIB-MET-001"] == {"granularidad": "mensual", "categorias": "todas"}
    assert P["FX-STL-001"] == {"esquema": "auto", "periodo": None, "robusto": True}


# ============================================================================= casos de control
CASOS = [(f, c) for f, casos in S.CASOS_CONTROL.items() for c in casos]


@pytest.mark.parametrize("ficha,caso", CASOS, ids=[f"{f}:{c['nombre'][:60]}" for f, c in CASOS])
def test_casos_de_control(ficha, caso):
    res, lim = _correr(ficha, _valores_caso(caso), dict(caso["parametros"]))
    assert caso["comprobar"](res)
    json.dumps(res, allow_nan=False)
    assert res["advertencias"] == S.ADVERTENCIAS[ficha]
    assert all(isinstance(x, str) for x in lim) and not set(lim) & set(S.ADVERTENCIAS[ficha])


def test_los_casos_de_control_pueden_fallar():
    """Cada comprobación falla con el resultado de otro caso o con una cifra alterada (no es trivialmente cierta)."""
    for ficha, casos in S.CASOS_CONTROL.items():
        for caso in casos:
            res, _ = _correr(ficha, _valores_caso(caso), dict(caso["parametros"]))
            assert caso["comprobar"](res)
            alterado = json.loads(json.dumps(res))

            def perturbar(x):
                if isinstance(x, dict):
                    return {k: perturbar(v) for k, v in x.items()}
                if isinstance(x, list):
                    return [perturbar(v) for v in x]
                if isinstance(x, bool) or x is None:
                    return (not x) if isinstance(x, bool) else x
                if isinstance(x, (int, float)):
                    return x * 1.01 + 0.37
                return x + "·" if isinstance(x, str) else x

            alterado = perturbar(alterado)
            try:
                ok = caso["comprobar"](alterado)
            except (KeyError, TypeError, IndexError, ValueError, AttributeError, ZeroDivisionError):
                ok = False
            assert not ok, f"{ficha}: «{caso['nombre']}» no detecta un resultado alterado"


# ============================================================================= determinismo y advertencias
@pytest.mark.parametrize("ficha", FICHAS)
def test_determinismo_dos_pasadas(ficha):
    v, p = BASE[ficha]
    r1, l1 = _correr(ficha, v, dict(p))
    r2, l2 = _correr(ficha, v, dict(p))
    assert json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True) and l1 == l2


@pytest.mark.parametrize("ficha", ["FX-REGIME-001", "REG-HMM-001", "TEM-DIFF-001"])
def test_la_semilla_se_declara_y_cambia_el_azar(ficha):
    v, p = BASE[ficha]
    r1, _ = _correr(ficha, v, {**p, "semilla": 5})
    r2, _ = _correr(ficha, v, {**p, "semilla": 5})
    assert r1 == r2 and r1["semilla"] == 5
    r3, _ = _correr(ficha, v, {**p, "semilla": 6})
    assert r3["semilla"] == 6


@pytest.mark.parametrize("ficha", FICHAS)
def test_advertencias_en_el_resultado_y_no_en_limitaciones(ficha):
    v, p = BASE[ficha]
    r, lim = _correr(ficha, v, dict(p))
    assert r["advertencias"] == S.ADVERTENCIAS[ficha]
    assert not set(lim) & set(S.ADVERTENCIAS[ficha])


# ============================================================================= umbrales fijos y dominio
UMBRALES = [(f, k) for f in FICHAS for k in S.UMBRALES[f]]


@pytest.mark.parametrize("ficha,umbral", UMBRALES, ids=[f"{f}:{k}" for f, k in UMBRALES])
def test_un_umbral_de_la_ficha_en_la_peticion_se_rechaza(ficha, umbral):
    v, p = BASE[ficha]
    _rechaza(ficha, v, {**p, umbral: S.UMBRALES[ficha][umbral]}, "umbrales fijos")


@pytest.mark.parametrize("ficha", FICHAS)
def test_un_parametro_desconocido_se_rechaza(ficha):
    v, p = BASE[ficha]
    _rechaza(ficha, v, {**p, "parametro_inventado": 1}, "desconocidos")


@pytest.mark.parametrize("ficha", FICHAS)
def test_clase_del_servicio_no_es_un_parametro_desconocido(ficha):
    v, p = BASE[ficha]
    if ficha in ("FX-REGIME-001", "REG-HMM-001", "TEM-DIFF-001"):
        S._parametros(ficha, {**p, "clase": "RV"})      # la validación basta: el cálculo ya se prueba aparte
    else:
        _correr(ficha, v, {**p, "clase": "RV"})


DOMINIO = [
    ("ST-INF-001", {"nivel": 0}), ("ST-INF-001", {"nivel": 1}), ("ST-INF-001", {"nivel": -0.1}),
    ("ST-INF-001", {"nivel": "0.05"}), ("ST-INF-001", {"nivel": True}), ("ST-INF-001", {"alternativa": "dos"}),
    ("ST-INF-001", {"correccion": "ninguna"}), ("ST-INF-001", {"tipo_contraste": "z"}),
    ("ST-INF-001", {"efecto_potencia": 0}), ("ST-INF-001", {"efecto_potencia": -1}),
    ("ST-INF-001", {"efecto_potencia": 0.5, "potencia_objetivo": 1}),
    ("ST-INF-001", {"potencia_objetivo": 0.8}),
    ("FX-BRK-001", {"max_rupturas": 0}), ("FX-BRK-001", {"max_rupturas": 6}), ("FX-BRK-001", {"max_rupturas": 1.5}),
    ("FX-BRK-001", {"nivel": 1}), ("FX-BRK-001", {"recorte": 0}), ("FX-BRK-001", {"recorte": 0.6}),
    ("FX-BRK-001", {"max_rupturas": 3, "recorte": 0.3}), ("FX-BRK-001", {"tipo_cambio": "otro"}),
    ("FX-STL-001", {"periodo": 1}), ("FX-STL-001", {"periodo": 2.5}), ("FX-STL-001", {"periodo": "12"}),
    ("FX-STL-001", {"robusto": "si"}), ("FX-STL-001", {"esquema": "log"}),
    ("FX-REGIME-001", {"n_estados": 1}), ("FX-REGIME-001", {"n_estados": 4}), ("FX-REGIME-001", {"n_estados": 2.5}),
    ("FX-REGIME-001", {"umbral": 0.2}), ("FX-REGIME-001", {"umbral": 0.8}),
    ("FX-REGIME-001", {"varianzas_distintas": "true"}), ("FX-REGIME-001", {"semilla": -1}),
    ("FX-REGIME-001", {"semilla": 1.5}), ("FX-REGIME-001", {"varianzas_distintas": False, "medias_distintas": False}),
    ("REG-HMM-001", {"n_estados": 1}), ("REG-HMM-001", {"n_estados": 5}), ("REG-HMM-001", {"n_estados": "AIC"}),
    ("REG-HMM-001", {"covarianza": "esferica"}), ("REG-HMM-001", {"arranques": 19}), ("REG-HMM-001", {"semilla": -1}),
    ("FX-COINT-001", {"metodo": "VAR"}), ("FX-COINT-001", {"max_rezagos": -1}), ("FX-COINT-001", {"max_rezagos": 1.5}),
    ("FX-COINT-001", {"max_rezagos": "BIC"}), ("FX-COINT-001", {"nivel": 0.07}), ("FX-COINT-001", {"nivel": "0.05"}),
    ("BIB-MET-001", {"granularidad": "semanal"}), ("BIB-MET-001", {"categorias": []}),
    ("BIB-MET-001", {"categorias": "TM-01"}), ("BIB-MET-001", {"categorias": [1]}),
    ("TEM-DIFF-001", {"modelo": "lineal"}), ("TEM-DIFF-001", {"m": 0}), ("TEM-DIFF-001", {"m": -5}),
    ("TEM-DIFF-001", {"m": []}), ("TEM-DIFF-001", {"m": [120, -1]}), ("TEM-DIFF-001", {"arranques": 0}),
    ("TEM-DIFF-001", {"B": 0}), ("TEM-DIFF-001", {"horizonte": 0}), ("TEM-DIFF-001", {"horizonte": 31}),
    ("TEM-DIFF-001", {"semilla": -2}), ("TEM-DIFF-001", {"m": "100"}),
]


@pytest.mark.parametrize("ficha,params", DOMINIO, ids=[f"{f}:{p}" for f, p in DOMINIO])
def test_dominio_de_cada_parametro(ficha, params):
    v, p = BASE[ficha]
    _rechaza(ficha, v, {**p, **params})


def test_parametros_dentro_del_dominio_se_aceptan():
    assert _correr("FX-BRK-001", {"serie": list(S._Y_NIVEL)}, {"nivel": 0.1, "recorte": 0.1})[0]["n_rupturas"] == 1
    r, _ = _correr("FX-COINT-001", {"series": S._PAR}, {"nivel": 0.01, "max_rezagos": 2})
    assert r["nivel"] == 0.01 and r["rezago_maximo"] == 2
    r, _ = _correr("ST-INF-001", BASE["ST-INF-001"][0], {"tipo_contraste": "t_una_muestra", "alternativa": "mayor"})
    assert r["contrastes"]["a"]["ic"]["superior"] is None
    r, _ = _correr("BIB-MET-001", {"fichas": S._FICHAS_BIB}, {"granularidad": "trimestral", "categorias": ["TM-01"]})
    assert r["total"] == 8 and set(r["por_tematica"]) == {"TM-01"}


# ============================================================================= entradas hostiles
HOSTILES = [None, 5, "texto", [1, 2]]


@pytest.mark.parametrize("ficha", FICHAS)
@pytest.mark.parametrize("ent", HOSTILES, ids=["None", "int", "str", "lista"])
def test_entrada_que_no_es_un_objeto(ficha, ent):
    with pytest.raises(ErrorFicha):
        S.FICHAS[ficha]["fn"](ent, {})


@pytest.mark.parametrize("ficha", FICHAS)
def test_valores_vacios_y_parametros_que_no_son_objeto(ficha):
    p = BASE[ficha][1]
    _rechaza(ficha, {}, dict(p))
    with pytest.raises(ErrorFicha):
        S.FICHAS[ficha]["fn"](_ent(BASE[ficha][0]), [1, 2])
    with pytest.raises(ErrorFicha):
        S.FICHAS[ficha]["fn"]({"valores": [1, 2]}, dict(p))


def _envenenar(v, malo):
    """Sustituye el primer número de cada lista de números de los datos por `malo`."""
    if isinstance(v, dict):
        return {k: _envenenar(x, malo) for k, x in v.items()}
    if isinstance(v, list) and v and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v):
        return [malo] + v[1:]
    if isinstance(v, list):
        return [_envenenar(x, malo) for x in v]
    return v


@pytest.mark.parametrize("ficha", [f for f in FICHAS if f != "BIB-MET-001"])
@pytest.mark.parametrize("malo", [float("nan"), float("inf"), -float("inf"), "1.0", None, True],
                         ids=["nan", "inf", "-inf", "str", "None", "bool"])
def test_numeros_hostiles_en_los_datos(ficha, malo):
    v, p = BASE[ficha]
    _rechaza(ficha, _envenenar(copy.deepcopy(v), malo), dict(p))


@pytest.mark.parametrize("campo,malo", [("fecha", "2025-13-01"), ("fecha", 20250101), ("tematica", ""), ("fuente", None),
                                        ("titulo", 5), ("hash", ["x"])])
def test_bib_met_conjunto_corrupto(campo, malo):
    fichas = copy.deepcopy(S._FICHAS_BIB)
    fichas[3][campo] = malo
    _rechaza("BIB-MET-001", {"fichas": fichas}, {})


@pytest.mark.parametrize("ficha,valores", [
    ("FX-BRK-001", {"serie": "1,2,3"}), ("FX-BRK-001", {"serie": {"a": 1}}),
    ("FX-STL-001", {"serie": list(S._Y_STL_RUIDO), "fechas": ["2020-01-01"] * 72}),
    ("FX-STL-001", {"serie": list(S._Y_STL_RUIDO), "fechas": [20200101 + i for i in range(72)]}),
    ("FX-COINT-001", {"series": [[1, 2], [3, 4]]}), ("FX-COINT-001", {"series": {"y": S._PAR["y"], "x": S._PAR["x"][:-1]}}),
    ("REG-HMM-001", {"variables": [1, 2, 3], "frecuencia": "semanal"}),
    ("REG-HMM-001", {"variables": {"a": S._HMM_VARIABLES["rendimiento"], "b": S._HMM_VARIABLES["volatilidad"][:-1]},
                     "frecuencia": "semanal"}),
    ("TEM-DIFF-001", {"adopcion": S._LOG, "anios": S._ANIOS[:-1]}), ("TEM-DIFF-001", {"adopcion": S._LOG, "fechas": [1] * 12}),
    ("ST-INF-001", {"contrastes": {"a": [1, 2]}}), ("ST-INF-001", {"contrastes": [[1, 2, 3]]}),
    ("BIB-MET-001", {"fichas": "nada"}), ("BIB-MET-001", {"fichas": [1, 2]}),
])
def test_estructuras_mal_formadas(ficha, valores):
    _rechaza(ficha, valores, dict(BASE[ficha][1]))


@pytest.mark.parametrize("ficha", ["FX-BRK-001", "FX-STL-001", "FX-REGIME-001"])
def test_serie_de_ht01_con_huecos_o_sin_fechas(ficha):
    p = BASE[ficha][1]
    s = _serie_fechas(BASE[ficha][0]["serie"])
    s.iloc[5] = np.nan
    _rechaza(ficha, {}, dict(p), "huecos", series={"X": s})
    _rechaza(ficha, {}, dict(p), series={"X": pd.Series([1.0, 2.0, 3.0])})
    _rechaza(ficha, {}, dict(p), series={"X": s.fillna(1.0), "Y": s.fillna(1.0)})


# ============================================================================= ST-INF-001
def test_st_inf_rechazos():
    F = "ST-INF-001"
    _rechaza(F, {"contrastes": [{"muestra": [1, 2, 3]}]}, {}, "no declarado")
    _rechaza(F, {"contrastes": [{"muestra": [1.0]}]}, {"tipo_contraste": "t_una_muestra"}, "no sostienen")
    _rechaza(F, {"contrastes": [{"muestra": [2.0, 2.0, 2.0]}]}, {"tipo_contraste": "t_una_muestra"}, "dispersión nula")
    _rechaza(F, {"contrastes": []}, {"tipo_contraste": "t_una_muestra"}, "vacía")
    _rechaza(F, {"contrastes": [{"nombre": "x", "muestra": [1, 2]}, {"nombre": "x", "muestra": [1, 3]}]},
             {"tipo_contraste": "t_una_muestra"}, "repetidos")
    _rechaza(F, {"contrastes": [{"muestra_a": [1, 2, 3], "muestra_b": [1, 2]}]}, {"tipo_contraste": "t_pareado"},
             "distinta longitud")
    _rechaza(F, {"contrastes": [{"muestra": [0.0, 0.0, 0.0]}]}, {"tipo_contraste": "wilcoxon"}, "no nulas")
    _rechaza(F, {"contrastes": [{"muestra_a": [1, 1], "muestra_b": [1, 1]}]}, {"tipo_contraste": "mann_whitney"},
             "empatadas")
    _rechaza(F, {"contrastes": [{"muestra_a": [1, 1], "muestra_b": [2, 2]}]}, {"tipo_contraste": "t_welch"},
             "dispersión nula")
    _rechaza(F, {"contrastes": [{"estadisticos": {"media": 1, "desviacion": -1, "n": 5}}]},
             {"tipo_contraste": "t_una_muestra"})
    _rechaza(F, {"contrastes": [{"estadisticos": {"media": 1, "desviacion": 1, "n": 1}}]},
             {"tipo_contraste": "t_una_muestra"})
    _rechaza(F, {"contrastes": [{"muestra": [1, 2, 3]}]}, {"tipo_contraste": "t_welch"}, "faltan")
    _rechaza(F, {}, {"tipo_contraste": "t_una_muestra"}, "faltan")


def test_st_inf_oraculo_welch_y_pareado_por_scipy():
    a, b = [5.1, 4.9, 6.2, 5.8, 6.0, 5.5, 4.7], [4.0, 4.4, 5.1, 3.9, 4.6]
    r, _ = _correr("ST-INF-001", {"contrastes": [{"nombre": "w", "muestra_a": a, "muestra_b": b}]}, {"tipo_contraste": "t_welch"})
    ref = stats.ttest_ind(a, b, equal_var=False)
    c = r["contrastes"]["w"]
    assert math.isclose(c["estadistico"], ref.statistic, rel_tol=1e-12) and math.isclose(c["p_valor"], ref.pvalue, rel_tol=1e-10)
    v1, v2 = np.var(a, ddof=1) / len(a), np.var(b, ddof=1) / len(b)
    gl = (v1 + v2) ** 2 / (v1 ** 2 / (len(a) - 1) + v2 ** 2 / (len(b) - 1))
    assert math.isclose(c["gl"], gl, rel_tol=1e-12)
    ci = ref.confidence_interval(0.95)
    assert math.isclose(c["ic"]["inferior"], ci.low, rel_tol=1e-10) and math.isclose(c["ic"]["superior"], ci.high, rel_tol=1e-10)
    # pareado = una muestra de las diferencias
    x, y = [1.0, 2.5, 3.1, 4.8, 5.0], [0.8, 2.0, 3.5, 4.1, 4.2]
    r, _ = _correr("ST-INF-001", {"contrastes": [{"nombre": "p", "muestra_a": x, "muestra_b": y}]}, {"tipo_contraste": "t_pareado"})
    assert math.isclose(r["contrastes"]["p"]["p_valor"], stats.ttest_rel(x, y).pvalue, rel_tol=1e-10)
    # estadísticos suficientes = muestra
    m = [0.3, 1.2, -0.4, 0.8, 1.9, 0.1]
    r1, _ = _correr("ST-INF-001", {"contrastes": [{"nombre": "e", "estadisticos": {"media": float(np.mean(m)),
                                                                                  "desviacion": float(np.std(m, ddof=1)),
                                                                                  "n": 6}}]},
                    {"tipo_contraste": "t_una_muestra"})
    r2, _ = _correr("ST-INF-001", {"contrastes": [{"nombre": "e", "muestra": m}]}, {"tipo_contraste": "t_una_muestra"})
    assert math.isclose(r1["contrastes"]["e"]["p_valor"], r2["contrastes"]["e"]["p_valor"], rel_tol=1e-12)


def test_st_inf_oraculo_wilcoxon_exacto():
    # n = 5 diferencias positivas: W+ = 15 y P(W+ = 15) = 1/2⁵ ⇒ p bilateral = 2/32
    r, lim = _correr("ST-INF-001", {"contrastes": [{"nombre": "w", "muestra": [0.5, 1.1, 0.3, 2.0, 0.9]}]},
                     {"tipo_contraste": "wilcoxon"})
    c = r["contrastes"]["w"]
    assert c["estadistico"] == 15 and math.isclose(c["p_valor"], 2 / 32, rel_tol=1e-12) and c["efecto"]["valor"] == 1.0
    assert c["ic"] is None and any("sin IC" in x for x in lim)


def test_st_inf_oraculo_potencia_y_n_minimo():
    # Valores clásicos (Cohen 1988): d = 0,5, α = 0,05 bilateral, potencia 0,8 ⇒ n = 34 (una muestra) y 64 por grupo.
    r, _ = _correr("ST-INF-001", {"contrastes": [{"nombre": "a", "muestra": [0.3, 1.2, -0.4, 0.8, 1.9, 0.1]}]},
                   {"tipo_contraste": "t_una_muestra", "efecto_potencia": 0.5, "potencia_objetivo": 0.8})
    assert r["contrastes"]["a"]["potencia"]["n_minimo"] == 34
    r, _ = _correr("ST-INF-001", {"contrastes": [{"nombre": "w", "muestra_a": [1, 2, 3, 4], "muestra_b": [2, 3, 4, 6]}]},
                   {"tipo_contraste": "t_welch", "efecto_potencia": 0.5, "potencia_objetivo": 0.8})
    assert r["contrastes"]["w"]["potencia"]["n_minimo"] == 64
    # Potencia a n = 6 por simulación (semilla fija): coincide con la no centrada dentro del error Monte Carlo
    rng = np.random.default_rng(1)
    sims = rng.standard_normal((40000, 6)) + 0.5
    t = sims.mean(1) / (sims.std(1, ddof=1) / math.sqrt(6))
    pot_mc = float(np.mean(np.abs(t) > stats.t.ppf(0.975, 5)))
    r6, _ = _correr("ST-INF-001", {"contrastes": [{"nombre": "a", "muestra": [0.3, 1.2, -0.4, 0.8, 1.9, 0.1]}]},
                    {"tipo_contraste": "t_una_muestra", "efecto_potencia": 0.5})
    assert abs(r6["contrastes"]["a"]["potencia"]["potencia"] - pot_mc) < 0.01


def test_st_inf_limitacion_de_normalidad_y_series_ht01():
    sesgada = [0.1, 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 8.0, 0.1, 0.1, 0.1]
    _, lim = _correr("ST-INF-001", {"contrastes": [{"nombre": "s", "muestra": sesgada}]}, {"tipo_contraste": "t_una_muestra"})
    assert any("normalidad rechazada" in x for x in lim)
    s = _serie_fechas(100 * np.cumprod(1 + 0.01 + 0.001 * S.ruido_weyl(60)), freq="B")
    r, lim = _correr("ST-INF-001", {}, {"tipo_contraste": "t_una_muestra"}, series={"X": s})
    rend = s.to_numpy()[1:] / s.to_numpy()[:-1] - 1
    assert math.isclose(r["contrastes"]["X"]["p_valor"], stats.ttest_1samp(rend, 0).pvalue, rel_tol=1e-10)


# ============================================================================= FX-BRK-001
def test_fx_brk_rechazos():
    F = "FX-BRK-001"
    _rechaza(F, {"serie": list(S._Y_NIVEL[:29])}, {}, "< 30")
    _rechaza(F, {"serie": list(S._Y_NIVEL[:45])}, {"max_rupturas": 2}, "< 50")
    _rechaza(F, {"serie": [1.0] * 40}, {}, "constante")
    assert _correr(F, {"serie": list(S._Y_NIVEL[:30])}, {})[0]["n"] == 30


def test_fx_brk_oraculo_cuantiles_de_bai_1997():
    # Bai (1997), tabla de la distribución de argmax de W(s) − |s|/2: 7,687 (90 %) y 11,033 (95 %)
    assert math.isclose(S._cuantil_bai(0.90), 7.687, abs_tol=2e-3)
    assert math.isclose(S._cuantil_bai(0.95), 11.033, abs_tol=2e-3)


def test_fx_brk_oraculo_bic_cusum_e_ic_recalculados():
    y = S._Y_NIVEL
    n = len(y)
    r, _ = _correr("FX-BRK-001", {"serie": list(y)}, {"tipo_cambio": "nivel"})
    k = 60
    ssr1 = float(np.sum((y[:k] - y[:k].mean()) ** 2) + np.sum((y[k:] - y[k:].mean()) ** 2))
    ssr0 = float(np.sum((y - y.mean()) ** 2))
    assert math.isclose(r["bic"]["nivel"]["1"], n * math.log(ssr1 / n) + 4 * math.log(n), rel_tol=1e-10)
    assert math.isclose(r["bic"]["nivel"]["0"], n * math.log(ssr0 / n) + 2 * math.log(n), rel_tol=1e-10)
    cs = np.cumsum(y - y.mean()) / (np.std(y, ddof=1) * math.sqrt(n))
    assert math.isclose(r["cusum"]["estadistico"], float(np.max(np.abs(cs[:-1]))), rel_tol=1e-12)
    # IC de Bai: k ± (⌊c·σ²/δ²⌋ + 1) con σ² de los residuos de los dos segmentos
    delta = y[k:].mean() - y[:k].mean()
    s2 = ssr1 / (n - 2)
    a = math.floor(11.033 * s2 / delta ** 2) + 1
    assert r["rupturas"][0]["ic"]["inferior"] == k - a and r["rupturas"][0]["ic"]["superior"] == k + a


def test_fx_brk_fechas_y_serie_de_ht01():
    s = _serie_fechas(S._Y_NIVEL, "2020-01-03")
    r, _ = _correr("FX-BRK-001", {}, {}, series={"X": s})
    assert r["rupturas"][0]["fecha"] == s.index[60].date().isoformat() and r["origen"] == "HT-01"
    fechas = [d.date().isoformat() for d in s.index]
    r2, _ = _correr("FX-BRK-001", {"serie": list(S._Y_NIVEL), "fechas": fechas}, {})
    assert r2["rupturas"] == r["rupturas"]


# ============================================================================= FX-STL-001
def test_fx_stl_rechazos_y_limitacion():
    F = "FX-STL-001"
    _rechaza(F, {"serie": list(S._Y_STL_RUIDO[:23])}, {"periodo": 12}, "< 2")
    _rechaza(F, {"serie": list(S._Y_STL_RUIDO - 20)}, {"periodo": 12, "esquema": "multiplicativo"}, "no positivos")
    _rechaza(F, {"serie": list(S._Y_STL_RUIDO)}, {}, "periodo")
    irregulares = [d.date().isoformat() for d in pd.date_range("2020-01-01", periods=71, freq="MS")] + ["2026-12-31"]
    _rechaza(F, {"serie": list(S._Y_STL_RUIDO), "fechas": irregulares}, {}, "irregular")
    _, lim = _correr(F, {"serie": list(S._Y_STL_RUIDO[:30])}, {"periodo": 12})
    assert any("recomendados" in x for x in lim)


def test_fx_stl_periodo_deducido_de_las_fechas():
    mensuales = [d.date().isoformat() for d in pd.date_range("2018-01-01", periods=72, freq="MS")]
    r, _ = _correr("FX-STL-001", {"serie": list(S._Y_STL_RUIDO), "fechas": mensuales}, {})
    assert r["periodo"] == 12
    trimestrales = [d.date().isoformat() for d in pd.date_range("2008-01-01", periods=72, freq="QS")]
    assert _correr("FX-STL-001", {"serie": list(S._Y_STL_RUIDO), "fechas": trimestrales}, {})[0]["periodo"] == 4


def test_fx_stl_oraculo_loess_por_minimos_cuadrados_ponderados():
    """El LOESS local lineal coincide con np.polyfit ponderado con pesos tricúbicos en cada punto."""
    rng = np.random.default_rng(3)
    y = np.cumsum(rng.standard_normal(40))
    q = 9
    x = np.arange(40.0)
    for x0 in (0.0, 7.0, 39.0, -1.0, 40.0):
        d = np.abs(x - x0)
        h = np.sort(d)[q - 1]
        w = np.where(d / h < 1, (1 - (d / h) ** 3) ** 3, 0)
        sel = w > 0
        b = np.polyfit(x[sel], y[sel], 1, w=np.sqrt(w[sel]))
        assert math.isclose(float(S._loess(y, q, None, np.array([x0]))[0]), float(np.polyval(b, x0)), rel_tol=1e-9,
                            abs_tol=1e-9)


def test_fx_stl_oraculo_anova_estacional_y_criterio_de_esquema():
    r, _ = _correr("FX-STL-001", {"serie": list(S._Y_STL_RUIDO)}, {"periodo": 12, "esquema": "aditivo"})
    sr = np.array(r["estacional"]) + np.array(r["resto"])
    grupos = [sr[np.arange(72) % 12 == j] for j in range(12)]
    gm = sr.mean()
    ssb = sum(len(g) * (g.mean() - gm) ** 2 for g in grupos)
    ssw = sum(float(np.sum((g - g.mean()) ** 2)) for g in grupos)
    F = (ssb / 11) / (ssw / (72 - 12))
    assert math.isclose(r["diagnostico_estacional"]["F_estable"], F, rel_tol=1e-10)
    assert r["diagnostico_estacional"]["p_valor"] < 0.05
    r2, _ = _correr("FX-STL-001", {"serie": list(S._Y_STL_MULT)}, {"periodo": 12})
    c = r2["criterio_esquema"]
    assert c["varianza_resto_log"] < c["varianza_relativa_resto_aditivo"] and r2["esquema"] == "multiplicativo"
    ajust = np.array(r2["ajustada"]) * np.array(r2["estacional"])
    assert np.allclose(ajust, S._Y_STL_MULT, rtol=1e-12)


def test_fx_stl_robusto_resiste_un_atipico():
    y = S._Y_STL_EXACTA.copy()
    y[30] += 50
    r_rob, _ = _correr("FX-STL-001", {"serie": list(y)}, {"periodo": 12, "esquema": "aditivo"})
    r_sim, _ = _correr("FX-STL-001", {"serie": list(y)}, {"periodo": 12, "esquema": "aditivo", "robusto": False})
    err = [float(np.max(np.abs(np.array(r["estacional"]) - S._PATRON[S._T_STL % 12]))) for r in (r_rob, r_sim)]
    assert err[0] < err[1] and r_rob["diagnostico_estacional"]["observaciones_con_peso_cero"] >= 1


# ============================================================================= FX-REGIME-001
def test_fx_regime_rechazos_y_limitacion():
    F = "FX-REGIME-001"
    _rechaza(F, {"serie": list(S._X_REGIME[:99])}, {}, "< 100")
    _rechaza(F, {"serie": [0.5] * 120}, {}, "constante")
    _, lim = _correr(F, {"serie": list(S._X_REGIME[:150])}, {})
    assert any("recomendadas" in x for x in lim)


def _hamilton(x, pi0, A, mu, sd):
    """Filtro de Hamilton escrito aparte (bucle escalar, densidad normal a mano)."""
    k = len(pi0)
    pred, ll, filt = list(pi0), 0.0, []
    for xt in x:
        a = [pred[i] * math.exp(-0.5 * ((xt - mu[i]) / sd[i]) ** 2) / (sd[i] * math.sqrt(2 * math.pi)) for i in range(k)]
        c = sum(a)
        ll += math.log(c)
        f = [ai / c for ai in a]
        filt.append(f)
        pred = [sum(f[i] * A[i][j] for i in range(k)) for j in range(k)]
    return np.array(filt), ll


def test_fx_regime_oraculo_filtro_de_hamilton_y_maximo_local():
    x = S._X_REGIME
    r, _ = _correr("FX-REGIME-001", {"serie": list(x)}, {})
    e = r["estados"]
    pi0 = [s["probabilidad_inicial"] for s in e]
    mu = [s["media"] for s in e]
    sd = [s["desviacion"] for s in e]
    filt, ll = _hamilton(x, pi0, r["matriz_transicion"], mu, sd)
    assert np.max(np.abs(filt - np.array(r["serie"]["filtradas"]))) < 1e-10 and math.isclose(ll, r["loglik"], rel_tol=1e-10)
    # máximo local: perturbar cada desviación o la persistencia baja la verosimilitud
    for i in range(2):
        for fac in (0.98, 1.02):
            sd2 = list(sd)
            sd2[i] *= fac
            assert _hamilton(x, pi0, r["matriz_transicion"], mu, sd2)[1] < ll
    A2 = np.array(r["matriz_transicion"])
    A2[0] = [A2[0, 0] - 0.01, A2[0, 1] + 0.01]
    assert _hamilton(x, pi0, A2, mu, sd)[1] < ll
    # clasificación de los regímenes verdaderos por la filtrada (el generador alterna σ = 1 y σ = 3 cada 50)
    acierto = float(np.mean(np.argmax(np.array(r["serie"]["filtradas"]), 1) == S._REG_VERDAD))
    assert acierto > 0.85
    assert r["regimen_actual"] in ("estado_1", "estado_2", "indeterminado")
    dur = [1 / (1 - r["matriz_transicion"][i][i]) for i in range(2)]
    assert np.allclose(dur, r["duraciones_esperadas"], rtol=1e-12)


def test_fx_regime_medias_distintas_y_rendimientos_de_ht01():
    n = 200
    x = np.where((np.arange(n) // 40) % 2 == 0, -1.0, 1.0) + 0.3 * S.ruido_gaussiano(n, 9)
    r, _ = _correr("FX-REGIME-001", {"serie": list(x)}, {"medias_distintas": True, "varianzas_distintas": False})
    assert r["estados"][0]["media"] < 0 < r["estados"][1]["media"]
    assert r["estados"][0]["desviacion"] == r["estados"][1]["desviacion"] and r["etiquetado"] == "por media creciente"
    precios = _serie_fechas(100 * np.cumprod(1 + 0.01 * S._X_REGIME[:150]), freq="B")
    r2, _ = _correr("FX-REGIME-001", {}, {}, series={"X": precios})
    assert r2["n"] == 149 and r2["origen"].startswith("HT-01")


# ============================================================================= REG-HMM-001
def test_reg_hmm_rechazos():
    F = "REG-HMM-001"
    v = S._HMM_VARIABLES
    _rechaza(F, {"variables": {k: x[:259] for k, x in v.items()}, "fechas": S._HMM_FECHAS[:259]}, {"n_estados": 2}, "< 260")
    mens = [d.date().isoformat() for d in pd.date_range("2010-01-31", periods=119, freq="ME")]
    _rechaza(F, {"variables": {k: x[:119] for k, x in v.items()}, "fechas": mens}, {"n_estados": 2}, "< 120")
    _rechaza(F, {"variables": v}, {"n_estados": 2}, "frecuencia")
    _rechaza(F, {"variables": v, "frecuencia": "diaria"}, {"n_estados": 2}, "frecuencia")
    _rechaza(F, {"variables": v, "fechas": S._HMM_FECHAS, "frecuencia": "mensual"}, {"n_estados": 2}, "no coinciden")
    _rechaza(F, {"variables": {"a": [1.0] * 300, "b": v["volatilidad"]}, "frecuencia": "semanal"}, {"n_estados": 2},
             "constante")
    _rechaza(F, {"fechas": S._HMM_FECHAS}, {"n_estados": 2}, "variables")
    r, lim = _correr(F, {"variables": v, "frecuencia": "semanal"}, {"n_estados": 2})
    assert r["frecuencia"] == "semanal" and any("no comprobada" in x for x in lim)


def test_reg_hmm_oraculo_filtro_y_estacionaria():
    r, _ = _correr("REG-HMM-001", {"variables": S._HMM_VARIABLES, "fechas": S._HMM_FECHAS}, {"n_estados": 2})
    X = np.column_stack([S._HMM_VARIABLES[c] for c in r["variables"]])
    Z = (X - X.mean(0)) / X.std(0, ddof=1)
    A = np.array(r["matriz_transicion"])
    pred = np.array([s["probabilidad_inicial"] for s in r["estados"]])
    ll, filt = 0.0, []
    for z in Z:
        dens = []
        for s in r["estados"]:
            mu = np.array([s["medias_estandarizadas"][c] for c in r["variables"]])
            var = np.array(s["covarianza_estandarizada"])
            dens.append(float(np.prod(np.exp(-0.5 * (z - mu) ** 2 / var) / np.sqrt(2 * math.pi * var))))
        a = pred * np.array(dens)
        ll += math.log(a.sum())
        filt.append(a / a.sum())
        pred = filt[-1] @ A
    assert np.max(np.abs(np.array(filt) - np.array(r["serie_filtradas"]["probabilidades"]))) < 1e-10
    assert math.isclose(ll, r["loglik"], rel_tol=1e-10)
    pi = np.array(list(r["referencia_ingenua"]["incondicional"].values()))
    assert np.allclose(pi @ A, pi, atol=1e-12) and math.isclose(pi.sum(), 1)
    # medias por estado en unidades originales = estandarizadas·σ + μ
    for s in r["estados"]:
        for j, c in enumerate(r["variables"]):
            assert math.isclose(s["medias"][c], s["medias_estandarizadas"][c] * X[:, j].std(ddof=1) + X[:, j].mean(),
                                rel_tol=1e-12)


def test_reg_hmm_seleccion_por_bic():
    r, _ = _correr("REG-HMM-001", {"variables": S._HMM_VARIABLES, "fechas": S._HMM_FECHAS}, {})
    assert r["criterio"] == "BIC" and set(r["bic"]) <= {"2", "3", "4"}
    assert r["n_estados"] == int(min(r["bic"], key=lambda k: r["bic"][k]))
    assert r["n_estados"] == 2      # el generador tiene dos regímenes


# ============================================================================= FX-COINT-001
def test_fx_coint_rechazos_y_limitaciones():
    F = "FX-COINT-001"
    _rechaza(F, {"series": {k: v[:49] for k, v in S._PAR.items()}}, {}, "< 50")
    _rechaza(F, {"series": {"y": S._PAR["y"]}}, {}, "al menos dos")
    _rechaza(F, {"series": {f"s{i}": S._PAR["x"] for i in range(6)}}, {}, "> 5")
    _rechaza(F, {"series": {"y": S._PAR["y"], "x": [1.0] * 300}}, {}, "constante")
    _rechaza(F, {}, {}, "faltan")
    estacionaria = {"y": list(S.ruido_gaussiano(300, 21)), "x": list(S.ruido_gaussiano(300, 22))}
    _, lim = _correr(F, {"series": estacionaria}, {})
    assert any("no son I(1)" in x for x in lim)


def _johansen_por_correlaciones_canonicas(Y):
    """Autovalores de Johansen (caso 2, sin rezagos) como correlaciones canónicas² entre ΔY_t y (Y_{t−1}, 1)."""
    R0 = np.diff(Y, axis=0)
    R1 = np.column_stack([Y[:-1], np.ones(len(Y) - 1)])
    q0, _ = np.linalg.qr(R0)
    q1, _ = np.linalg.qr(R1)
    sv = np.linalg.svd(q0.T @ q1, compute_uv=False)
    return np.sort(sv ** 2)[::-1][: Y.shape[1]]


def test_fx_coint_oraculo_johansen_y_engle_granger():
    Y = np.column_stack([S._PAR["y"], S._PAR["x"]])
    r, _ = _correr("FX-COINT-001", {"series": S._PAR}, {"max_rezagos": 0})
    assert r["johansen"]["orden_var"] == 1
    assert np.allclose(r["johansen"]["autovalores"], _johansen_por_correlaciones_canonicas(Y), rtol=1e-9)
    b = np.polyfit(Y[:, 1], Y[:, 0], 1)
    assert math.isclose(r["engle_granger"]["vector"][1], -b[0], rel_tol=1e-10)
    assert math.isclose(r["engle_granger"]["constante"], -b[1], rel_tol=1e-10)
    z = Y[:, 0] - np.polyval(b, Y[:, 1])
    dz, zl = np.diff(z), z[:-1]
    rho = float(zl @ dz / (zl @ zl))
    s2 = float(np.sum((dz - rho * zl) ** 2) / (len(dz) - 1))
    assert math.isclose(r["engle_granger"]["adf_residuos"]["tau"], rho / math.sqrt(s2 / float(zl @ zl)), rel_tol=1e-9)
    assert r["engle_granger"]["adf_residuos"]["rezagos"] == 0


def test_fx_coint_oraculo_valores_criticos_por_simulacion():
    """Las tablas de valores críticos (INC-T112-01) coinciden con una simulación Monte Carlo de la distribución nula."""
    rng = np.random.default_rng(5)
    T, R = 500, 3000
    for q in (1, 2):
        e = rng.standard_normal((R, T + 1, q))
        Y = np.cumsum(e, axis=1)
        R0 = np.diff(Y, axis=1)
        R1 = np.concatenate([Y[:, :-1], np.ones((R, T, 1))], axis=2)
        S00 = np.einsum("rti,rtj->rij", R0, R0) / T
        S11 = np.einsum("rti,rtj->rij", R1, R1) / T
        S01 = np.einsum("rti,rtj->rij", R0, R1) / T
        M = np.linalg.solve(S11, np.swapaxes(S01, 1, 2) @ np.linalg.solve(S00, S01))
        lam = np.clip(np.sort(np.linalg.eigvals(M).real, axis=1)[:, ::-1][:, :q], 0, 1 - 1e-15)
        traza = -T * np.log(1 - lam).sum(1)
        assert abs(np.quantile(traza, 0.95) / S._CRIT_TRAZA[q][1] - 1) < 0.06, q
    Y = np.cumsum(rng.standard_normal((R, T, 2)), axis=1)
    X = np.concatenate([np.ones((R, T, 1)), Y[:, :, 1:]], axis=2)
    b = np.linalg.solve(np.einsum("rti,rtj->rij", X, X), np.einsum("rti,rt->ri", X, Y[:, :, 0])[..., None])[..., 0]
    z = Y[:, :, 0] - np.einsum("rti,ri->rt", X, b)
    dz, zl = z[:, 1:] - z[:, :-1], z[:, :-1]
    rho = (zl * dz).sum(1) / (zl ** 2).sum(1)
    s2 = ((dz - rho[:, None] * zl) ** 2).sum(1) / (T - 2)
    tau = rho / np.sqrt(s2 / (zl ** 2).sum(1))
    assert abs(np.quantile(tau, 0.05) / S._CRIT_TAU[2][1] - 1) < 0.05


def test_fx_coint_series_de_ht01_alineadas():
    a = _serie_fechas(S._PAR["y"], "2020-01-03", "B")
    b = _serie_fechas(S._PAR["x"], "2020-01-03", "B").iloc[5:]
    r, _ = _correr("FX-COINT-001", {}, {}, series={"y": a, "x": b})
    assert r["n"] == 295 and r["desviacion_equilibrio"]["fechas"][0] == b.index[0].date().isoformat()


# ============================================================================= BIB-MET-001
def test_bib_met_rechazos():
    F = "BIB-MET-001"
    _rechaza(F, {"fichas": []}, {}, "vacío")
    _rechaza(F, {}, {}, "vacío")
    dup = copy.deepcopy(S._FICHAS_BIB)
    dup[1]["id"] = dup[0]["id"]
    _rechaza(F, {"fichas": dup}, {}, "repetidos")
    _rechaza(F, {"fichas": S._FICHAS_BIB}, {"categorias": ["TM-99"]}, "ninguna")
    _rechaza(F, {"fichas": S._FICHAS_BIB, "referencia": []}, {}, "referencia")


def test_bib_met_oraculo_recuento_aparte():
    fichas = S._FICHAS_BIB
    r, _ = _correr("BIB-MET-001", {"fichas": fichas}, {"granularidad": "anual"})
    assert r["por_periodo"] == dict(sorted(collections.Counter(f["fecha"][:4] for f in fichas).items()))
    assert r["por_fuente"] == dict(sorted(collections.Counter(f["fuente"] for f in fichas).items()))
    cuotas = np.array(list(collections.Counter(f["fuente"] for f in fichas).values())) / len(fichas)
    assert math.isclose(r["hhi_fuentes"], float(np.sum(cuotas ** 2)), rel_tol=1e-12)
    # crecimiento anual 2024 → 2025: 12 → 12 ⇒ 0
    assert r["crecimiento_cagr"] == 0.0
    r2, _ = _correr("BIB-MET-001", {"fichas": fichas}, {"granularidad": "trimestral"})
    assert list(r2["por_periodo"]) == [f"{a}-T{t}" for a in (2024, 2025) for t in (1, 2, 3, 4)]
    assert all(v == 3 for v in r2["por_periodo"].values())


def test_bib_met_periodos_vacios_y_duplicados_por_titulo():
    fichas = [{"id": "1", "fecha": "2025-01-05", "tematica": "T", "fuente": "A", "titulo": "Ñandú: «crecimiento»"},
              {"id": "2", "fecha": "2025-04-05", "tematica": "T", "fuente": "A", "titulo": "nandu crecimiento"},
              {"id": "3", "fecha": "2025-04-06", "tematica": "U", "fuente": "B"}]
    r, _ = _correr("BIB-MET-001", {"fichas": fichas}, {})
    assert r["por_periodo"] == {"2025-01": 1, "2025-02": 0, "2025-03": 0, "2025-04": 2}
    assert r["duplicados"]["grupos"] == [["1", "2"]] and r["verificacion"]["cuadra"]
    assert math.isclose(r["crecimiento_cagr"], (2 / 1) ** (12 / 3) - 1, rel_tol=1e-12)
    r1, lim1 = _correr("BIB-MET-001", {"fichas": fichas[:1]}, {})
    assert r1["crecimiento_cagr"] is None and lim1


# ============================================================================= TEM-DIFF-001
def test_tem_diff_rechazos():
    F = "TEM-DIFF-001"
    _rechaza(F, {"adopcion": S._LOG[:7], "anios": S._ANIOS[:7]}, {"B": 10}, "< 8")
    _rechaza(F, {"adopcion": [float(i) for i in range(12)], "anios": S._ANIOS}, {"B": 10}, "aceleración")
    _rechaza(F, {"adopcion": [-1.0] + S._LOG[1:], "anios": S._ANIOS}, {"B": 10}, "negativa")
    _rechaza(F, {"adopcion": S._LOG, "anios": S._ANIOS[::-1]}, {"B": 10}, "creciente")
    _rechaza(F, {"adopcion": S._LOG, "anios": S._ANIOS}, {"B": 10, "m": 50}, "inferior")
    _rechaza(F, {"adopcion": S._LOG, "anios": S._ANIOS}, {"B": 10, "m": [150, 50]}, "inferior")
    _rechaza(F, {"adopcion": S._LOG, "anios": S._ANIOS, "lanzamiento": 2010}, {"B": 10}, "anterior")
    _rechaza(F, {"adopcion": S._LOG}, {"B": 10}, "anios")
    _rechaza(F, {"anios": S._ANIOS}, {"B": 10}, "adopcion")


def test_tem_diff_oraculo_curve_fit_aic_y_bandas():
    rng = np.random.default_rng(4)
    y = np.array(S._LOG) * (1 + rng.normal(0, 0.03, 12))
    t = np.array(S._ANIOS, dtype=float)
    r, lim = _correr("TEM-DIFF-001", {"adopcion": list(y), "anios": S._ANIOS}, {"B": 200, "modelo": "logistica"})
    th, _ = optimize.curve_fit(lambda x, m, k, t0: m / (1 + np.exp(-k * (x - t0))), t, y, p0=[100, 0.8, 2016])
    for c, v in zip(("m", "k", "t0"), th, strict=True):
        assert math.isclose(r["parametros"][c], v, rel_tol=1e-5), c
    ssr = float(np.sum((y - th[0] / (1 + np.exp(-th[1] * (t - th[2])))) ** 2))
    assert math.isclose(r["aic"]["logistica"], 12 * math.log(ssr / 12) + 6, rel_tol=1e-6)
    pv = r["prevision"]
    assert pv["anios"] == [2022.0, 2023.0, 2024.0, 2025.0, 2026.0]
    assert all(a <= b <= c for a, b, c in zip(pv["p10"], pv["p50"], pv["p90"], strict=True))
    assert all(lo <= c <= hi for lo, c, hi in zip(pv["p10"], pv["central"], pv["p90"], strict=True))
    assert r["replicas_bootstrap"] == 200 and any("techo m estimado" in x for x in lim)
    cuota = r["trayectoria"]["ajustada"][-1] / r["parametros"]["m"]
    assert math.isclose(r["cuota_actual"], cuota, rel_tol=1e-12)


def test_tem_diff_escenarios_de_techo_y_referencia_ingenua():
    r, _ = _correr("TEM-DIFF-001", {"adopcion": S._LOG, "anios": S._ANIOS}, {"B": 20, "m": [110.0, 150.0]})
    assert [e["m"] for e in r["escenarios_m"]] == [110.0, 150.0]
    assert all(math.isclose(e["parametros"]["m"], e["m"]) for e in r["escenarios_m"])
    ing = r["referencia_ingenua"]
    y = S._LOG
    assert math.isclose(ing["lineal_reciente"], y[-1] + (y[-1] - y[-2]) * 5, rel_tol=1e-12)
    tasa = (y[-1] / y[0]) ** (1 / 11) - 1
    assert math.isclose(ing["crecimiento_constante"], y[-1] * (1 + tasa) ** 5, rel_tol=1e-10)


def test_tem_diff_fechas_iso_y_fase_madurez_con_techo_fijado():
    fechas = [f"{a}-07-02" for a in S._ANIOS]
    r, _ = _correr("TEM-DIFF-001", {"adopcion": S._LOG, "fechas": fechas}, {"B": 20, "m": 100, "modelo": "logistica"})
    # la fecha a 2 de julio desplaza medio año la escala decimal: t₀ = 2016,5 en años enteros ≈ 2017,0 en fechas
    assert r["m_fijado"] and r["fase"] == "madurez" and abs(r["inflexion_anio"] - 2017.0) < 0.05
    assert r["inflexion_fecha"][:7] in ("2016-12", "2017-01")


def test_tem_diff_b_por_defecto_es_1000():
    r, _ = _correr("TEM-DIFF-001", {"adopcion": S._LOG, "anios": S._ANIOS}, {"modelo": "logistica"})
    assert r["replicas_bootstrap"] == 1000


@pytest.mark.parametrize("ficha,valores,params", [
    ("ST-INF-001", {"contrastes": [{"muestra": [1e308, -1e308, 1e308]}]}, {"tipo_contraste": "t_una_muestra"}),
    ("FX-BRK-001", {"serie": [1e300 * (i % 2) for i in range(40)]}, {}),
])
def test_desbordamiento_no_sirve_cifras_no_finitas(ficha, valores, params):
    """Datos finitos cuyo cálculo desborda: la ficha rechaza (nunca entrega NaN ni inf)."""
    _rechaza(ficha, valores, params)


def test_fx_brk_recorte_impide_segmentos_cortos():
    """Un salto en t = 6 (dentro del 15 % del borde): ningún segmento queda por debajo de ⌈0,15·n⌉ = 18 observaciones."""
    y = np.where(np.arange(120) < 6, 4.0, 0.0) + S.ruido_weyl(120)
    r, _ = _correr("FX-BRK-001", {"serie": list(y)}, {"tipo_cambio": "nivel"})
    assert all(s["n"] >= 18 for s in r["segmentos"]) and r["rupturas"][0]["indice"] == 18
    r2, _ = _correr("FX-BRK-001", {"serie": list(y)}, {"tipo_cambio": "nivel", "recorte": 0.05})
    assert r2["rupturas"][0]["indice"] == 6


def test_fx_brk_oraculo_ic_de_bai_con_salto_pequeno():
    """δ = 0,6 con ruido uniforme: la anchura ⌊c·σ²/δ²⌋ + 1 no es trivial (c = 11,033 al 95 %, Bai 1997)."""
    y = S._Y_NIVEL_DEBIL
    n = len(y)
    r, _ = _correr("FX-BRK-001", {"serie": list(y)}, {"tipo_cambio": "nivel"})
    k = r["rupturas"][0]["indice"]
    delta = y[k:].mean() - y[:k].mean()
    s2 = float(np.sum((y[:k] - y[:k].mean()) ** 2) + np.sum((y[k:] - y[k:].mean()) ** 2)) / (n - 2)
    a = math.floor(11.033 * s2 / delta ** 2) + 1
    assert a >= 3
    assert r["rupturas"][0]["ic"]["inferior"] == k - a and r["rupturas"][0]["ic"]["superior"] == k + a


def test_fx_stl_serie_ajustada_aditiva():
    r, _ = _correr("FX-STL-001", {"serie": list(S._Y_STL_RUIDO)}, {"periodo": 12, "esquema": "aditivo"})
    assert np.allclose(np.array(r["ajustada"]), S._Y_STL_RUIDO - np.array(r["estacional"]), rtol=0, atol=1e-12)


def test_fx_stl_paso_bajo_exacto_en_serie_periodica_pura():
    """Nivel constante + patrón: el paso bajo (MA p, MA p, MA 3, LOESS) da el nivel exacto en la primera vuelta, así que
    la estacional suma 0 en cada ciclo y la tendencia es el nivel (sin robustez, a precisión de máquina)."""
    y = 10 + S._PATRON[np.arange(60) % 12]
    r, _ = _correr("FX-STL-001", {"serie": list(y)}, {"periodo": 12, "esquema": "aditivo", "robusto": False})
    est = np.array(r["estacional"]).reshape(5, 12)
    assert np.max(np.abs(est.sum(1))) < 1e-10 and np.max(np.abs(np.array(r["tendencia"]) - 10)) < 1e-11


def test_fx_regime_oraculo_estacionariedad_de_la_verosimilitud():
    """En el máximo de verosimilitud la derivada respecto de cada parámetro libre es nula: diferencias centradas con el
    filtro de Hamilton escrito aparte (log σᵢ y el reparto de cada fila de la transición)."""
    x = S._X_REGIME
    r, _ = _correr("FX-REGIME-001", {"serie": list(x)}, {})
    e = r["estados"]
    pi0 = [s["probabilidad_inicial"] for s in e]
    mu = [s["media"] for s in e]
    sd = [s["desviacion"] for s in e]
    A = np.array(r["matriz_transicion"])
    h = 1e-4
    for i in range(2):
        arriba, abajo = list(sd), list(sd)
        arriba[i] *= math.exp(h)
        abajo[i] *= math.exp(-h)
        der = (_hamilton(x, pi0, A, mu, arriba)[1] - _hamilton(x, pi0, A, mu, abajo)[1]) / (2 * h)
        assert abs(der) < 0.05, (i, der)
        Aa, Ab = A.copy(), A.copy()
        Aa[i] = [A[i, 0] + h * (1 - 2 * i), A[i, 1] - h * (1 - 2 * i)]
        Ab[i] = [A[i, 0] - h * (1 - 2 * i), A[i, 1] + h * (1 - 2 * i)]
        der_a = (_hamilton(x, pi0, Aa, mu, sd)[1] - _hamilton(x, pi0, Ab, mu, sd)[1]) / (2 * h)
        assert abs(der_a) * min(A[i, 0], A[i, 1]) < 0.05, (i, der_a)


def test_reg_hmm_oraculo_estacionariedad_con_covarianza_completa():
    """Escalar la covarianza de un estado por e^{±h} no mejora la verosimilitud (derivada nula en el máximo)."""
    v = S._HMM_VARIABLES
    r, _ = _correr("REG-HMM-001", {"variables": v, "fechas": S._HMM_FECHAS}, {"n_estados": 2, "covarianza": "completa"})
    X = np.column_stack([v[c] for c in r["variables"]])
    Z = (X - X.mean(0)) / X.std(0, ddof=1)
    A = np.array(r["matriz_transicion"])

    def ll(covs):
        pred, tot = np.array([s["probabilidad_inicial"] for s in r["estados"]]), 0.0
        for z in Z:
            dens = np.array([stats.multivariate_normal.pdf(z, [s["medias_estandarizadas"][c] for c in r["variables"]], C)
                             for s, C in zip(r["estados"], covs, strict=True)])
            a = pred * dens
            tot += math.log(a.sum())
            pred = (a / a.sum()) @ A
        return tot

    covs = [np.array(s["covarianza_estandarizada"]) for s in r["estados"]]
    assert math.isclose(ll(covs), r["loglik"], rel_tol=1e-10)
    h = 1e-4
    for i in range(2):
        arriba = [C * math.exp(h) if j == i else C for j, C in enumerate(covs)]
        abajo = [C * math.exp(-h) if j == i else C for j, C in enumerate(covs)]
        assert abs((ll(arriba) - ll(abajo)) / (2 * h)) < 0.05


def test_fx_coint_valores_criticos_y_decisiones_por_fila():
    # paseos con semilla 38: traza(r = 0) = 13,2, entre la mitad del valor crítico y el valor crítico (no rechaza)
    cerca = {"y": list(np.cumsum(S.ruido_gaussiano(300, 38))), "x": list(np.cumsum(S.ruido_gaussiano(300, 138)))}
    for datos in (S._PAR, S._INDEP, cerca):
        r, _ = _correr("FX-COINT-001", {"series": datos}, {})
        # MacKinnon (2010), N = 2, 5 %: −3,33613; MacKinnon, Haug y Michelis (1999), caso 2, 5 %: 20,2618 y 9,1645
        assert r["engle_granger"]["adf_residuos"]["critico"] == -3.33613
        assert [f["critico"] for f in r["johansen"]["traza"]] == [20.2618, 9.1645]
        assert all(f["rechaza"] == (f["estadistico"] > f["critico"]) for f in r["johansen"]["traza"])
        rango = next((f["r"] for f in r["johansen"]["traza"] if not f["rechaza"]), 2)
        assert r["johansen"]["rango"] == rango
        assert r["engle_granger"]["adf_residuos"]["rechaza"] == (r["engle_granger"]["adf_residuos"]["tau"] < -3.33613)
        assert all(x["adf_nivel"]["critico"] == -2.86154 for x in r["integracion"].values())
    assert 20.2618 / 2 < r["johansen"]["traza"][0]["estadistico"] < 20.2618 and r["johansen"]["rango"] == 0


def test_fx_coint_oraculo_velocidad_de_ajuste_por_mco():
    """Con el vector fijado, α de Johansen = MCO de ΔY_t sobre z_{t−1} = β'(Y_{t−1}, 1) (caso 2 sin rezagos)."""
    r, _ = _correr("FX-COINT-001", {"series": S._PAR}, {"max_rezagos": 0})
    Y = np.column_stack([S._PAR["y"], S._PAR["x"]])
    b = r["vector_normalizado"]
    z = Y[:, 0] * b["y"] + Y[:, 1] * b["x"] + b["constante"]
    dY = np.diff(Y, axis=0)
    for j, c in enumerate(("y", "x")):
        alfa = float(z[:-1] @ dY[:, j] / (z[:-1] @ z[:-1]))
        assert math.isclose(r["velocidad_ajuste"][c], alfa, rel_tol=1e-8, abs_tol=1e-12)


def test_tem_diff_fases_por_umbral():
    assert S._fase(0.159, [0.16, 0.50]) == "introduccion" and S._fase(0.16, [0.16, 0.50]) == "crecimiento"
    assert S._fase(0.50, [0.16, 0.50]) == "crecimiento" and S._fase(0.501, [0.16, 0.50]) == "madurez"
    y = [100 / (1 + math.exp(-0.5 * (a - 2022))) for a in S._ANIOS]
    r, _ = _correr("TEM-DIFF-001", {"adopcion": y, "anios": S._ANIOS}, {"B": 20, "modelo": "logistica", "m": 100})
    assert 0.16 < r["cuota_actual"] < 0.5 and r["fase"] == "crecimiento"
