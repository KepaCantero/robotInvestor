"""T-106 · Motor Fase 1: fichas TCV del Catálogo V5.0 (TCV-SLOPE-001, TCV-BEI-001, TCV-CDS-001, TCV-VIXTS-001,
TCV-TP-001). Casos de control de «Verificación», reglas de rechazo, determinismo, claves de «Salidas» y valores
calculados a mano con datos sintéticos."""
import copy
import json
import math

import numpy as np
import pandas as pd
import pytest

from bloque_a.motor import fichas_tcv as tcv
from bloque_a.motor.operaciones import ErrorFicha


def _ent(valores, series_rol=None):
    return {"valores": copy.deepcopy(valores), "series": {}, "series_rol": series_rol or {}}


def _correr(ficha, valores, params=None, series_rol=None):
    return tcv.FICHAS[ficha]["fn"](_ent(valores, series_rol), params or {})


def _valores_caso(caso):
    v = {}
    for d in caso["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    return v


CASOS = [(f, c) for f, casos in tcv.CASOS_CONTROL.items() for c in casos]

# ----------------------------------------------------------------------------- datos base por ficha
CURVA_SLOPE = [1.0, 1.5, 2.0, 3.0, 4.0, 4.5]          # nodos 0,25 · 1 · 2 · 5 · 10 · 30 años
BASE = {
    "TCV-SLOPE-001": (tcv.sintetico_slope(lambda t, i: CURVA_SLOPE[[0.25, 1, 2, 5, 10, 30].index(t)]), {}),
    "TCV-BEI-001": ({"curva_nominal": {"plazos": [1, 2, 5, 10, 20], "rendimientos": [3.0, 3.2, 3.6, 4.1, 4.3]},
                     "curva_real": {"plazos": [1, 2, 5, 10, 20], "rendimientos": [1.2, 1.1, 1.3, 1.6, 1.7],
                                    "indice_referencia": "IPC"},
                     "encuestas": {"fecha": "2024-06-01", "fuente": "encuesta sintética",
                                   "horizontes": {"2": 2.0, "5": 2.1, "10": 2.2, "5y5y": 2.3}}},
                    {"ajuste_estacional": False}),
    "TCV-CDS-001": (tcv.sintetico_cds([100.0 + 20 * math.sin(i * 0.1) for i in range(269)] + [150.0], 0.02), {}),
    "TCV-VIXTS-001": (tcv.sintetico_vixts(15.0, [16.0, 18.0], [20, 40]), {}),
    "TCV-TP-001": (tcv.sintetico_acm()[0], {"n_factores": 3}),
}

# Claves de «Salidas» de cada ficha
SALIDAS = {
    "TCV-SLOPE-001": ["pendiente_pb", "valor_razonable_pb", "ic_valor_razonable_pb", "residuo_pb", "z",
                      "pendiente_forward_pb", "carry_neutral_dv01_pb", "regimen"],
    "TCV-BEI-001": ["breakevens_pct", "forward_5y5y_pct", "base_swap_bono_pb", "brecha_encuestas_pb", "percentiles",
                    "carry_inflacion_pb"],
    "TCV-CDS-001": ["diferencial_pb", "lambda_pct_anual", "perdida_esperada_pb", "prima_pb", "ratio_diferencial_perdida",
                    "percentil", "base_pb", "pendiente_pb", "carry_pb_anual", "dv01"],
    "TCV-VIXTS-001": ["curva_puntos", "estado", "ratios", "roll_puntos_dia", "roll_pct_mensual", "percentil_pendiente",
                      "rentabilidades_por_estado", "es_corta_pct"],
    "TCV-TP-001": ["prima_pb", "rendimiento_neutral_pct", "percentiles", "descomposicion_cambios_pb", "serie"],
}


# ============================================================================= registro y casos de control
def test_registro_de_las_cinco_fichas():
    assert set(tcv.FICHAS) == set(tcv.PARAMETROS_POR_DEFECTO) == set(tcv.CASOS_CONTROL) == set(SALIDAS)
    for meta in tcv.FICHAS.values():
        assert meta["modulo"] == "MC-09" and meta["version"] == "1.0"
        assert meta["cifra"] in ("DETERMINISTA", "ESTADISTICA") and meta["ri"] and meta["tol"] > 0
        assert callable(meta["fn"])
    assert tcv.FICHAS["TCV-TP-001"]["tol"] == 1e-6 and tcv.FICHAS["TCV-BEI-001"]["tol"] == 1e-10


@pytest.mark.parametrize("ficha,caso", CASOS, ids=[f"{f}:{c['nombre']}" for f, c in CASOS])
def test_casos_de_control(ficha, caso):
    res, lim = _correr(ficha, _valores_caso(caso), caso["parametros"])
    assert caso["comprobar"](res)
    json.dumps(res, allow_nan=False)          # JSON-serializable y sin NaN
    assert all(isinstance(x, str) for x in lim)


@pytest.mark.parametrize("ficha", sorted(tcv.FICHAS))
def test_al_menos_dos_casos_de_control_por_ficha(ficha):
    assert len(tcv.CASOS_CONTROL[ficha]) >= 2


@pytest.mark.parametrize("ficha", sorted(BASE))
def test_determinismo(ficha):
    v, p = BASE[ficha]
    a = json.dumps(_correr(ficha, v, p), sort_keys=True, allow_nan=False)
    b = json.dumps(_correr(ficha, v, p), sort_keys=True, allow_nan=False)
    assert a == b


@pytest.mark.parametrize("ficha", sorted(BASE))
def test_claves_de_salida(ficha):
    v, p = BASE[ficha]
    res, lim = _correr(ficha, v, p)
    destino = res["tramos"]["2s10s"] if ficha == "TCV-SLOPE-001" else res
    for k in SALIDAS[ficha]:
        assert k in destino, k
    # las advertencias obligatorias de la ficha («Supuestos y limitaciones») se entregan siempre
    assert all(a in lim for a in tcv.ADVERTENCIAS[ficha])


@pytest.mark.parametrize("ficha", sorted(BASE))
def test_no_modifica_la_entrada(ficha):
    v, p = BASE[ficha]
    ent = _ent(v)
    antes = json.dumps(ent["valores"], sort_keys=True)
    tcv.FICHAS[ficha]["fn"](ent, dict(p))
    assert json.dumps(ent["valores"], sort_keys=True) == antes


# ============================================================================= TCV-SLOPE-001
def test_slope_valores_a_mano():
    res, _ = _correr("TCV-SLOPE-001", BASE["TCV-SLOPE-001"][0])
    t = res["tramos"]["2s10s"]
    assert t["pendiente_pb"] == pytest.approx(200.0, rel=1e-12)
    # FIR-CARRY-001 en ambos tramos, Δt = 3 meses, financiación = y(0,25) = 1 %:
    # tramo 2: carry/D = (2 % − 1 %)·0,25·1,02/2 = 0,1275 %; rolldown/D = 2 % − y(1,75) = 2 % − 1,875 % = 0,125 %
    # tramo 10: carry/D = (4 % − 1 %)·0,25·1,04/10 = 0,078 %; rolldown/D = 4 % − y(9,75) = 4 % − 3,95 % = 0,05 %
    c = t["carry_neutral_dv01_pb"]
    assert c["carry_pb"] == pytest.approx(12.75 - 7.8, rel=1e-10)
    assert c["rolldown_pb"] == pytest.approx(12.5 - 5.0, rel=1e-10)
    assert c["total_pb"] == pytest.approx(4.95 + 7.5, rel=1e-10)
    # pendiente forward a 3 meses: f(0,25; 2,25) y f(0,25; 10,25) con capitalización anual
    y = lambda x: np.interp(x, [0.25, 1, 2, 5, 10, 30], CURVA_SLOPE) / 100
    fa = ((1 + y(2.25)) ** 2.25 / (1 + y(0.25)) ** 0.25) ** (1 / 2) - 1
    fb = ((1 + y(10.25)) ** 10.25 / (1 + y(0.25)) ** 0.25) ** (1 / 10) - 1
    assert t["pendiente_forward_pb"]["3m"] == pytest.approx((fb - fa) * 1e4, rel=1e-12)
    assert t["punto_muerto_pb"]["3m"] == pytest.approx(t["pendiente_forward_pb"]["3m"] - 200.0, rel=1e-12)
    assert set(t["pendiente_forward_pb"]) == {"3m", "6m"}


def _slope_lineal(ruido=None):
    """Pendiente = 50 + 10·regresor₁ (+ ruido) pb; el resto de regresores no entra."""
    v = tcv.sintetico_slope(lambda t, i: 2.0)
    r1 = v["regresores"]["cambio_esperado_tipo_oficial_1a"]["serie"]
    for i, fila in enumerate(v["historia_curva"]["rendimientos"]):
        extra = (ruido(i) if ruido else 0.0)
        fila[4] = 2.0 + (50 + 10 * r1[i] + extra) / 100     # nodo de 10 años
        fila[5] = fila[4]
    return v, r1


def test_slope_regresion_recupera_coeficientes():
    v, r1 = _slope_lineal()
    res, _ = _correr("TCV-SLOPE-001", v)
    t = res["tramos"]["2s10s"]
    co = t["regresion"]["coeficientes"]
    assert co["constante"] == pytest.approx(50, abs=1e-8)
    assert co["cambio_esperado_tipo_oficial_1a"] == pytest.approx(10, abs=1e-8)
    assert co["prima_plazo"] == pytest.approx(0, abs=1e-8)
    assert t["valor_razonable_pb"] == pytest.approx(50 + 10 * r1[-1], abs=1e-8)
    assert t["residuo_pb"] == pytest.approx(0, abs=1e-8)
    lo, hi = t["ic_valor_razonable_pb"]
    assert lo <= t["valor_razonable_pb"] <= hi and t["nivel_ic"] == pytest.approx(0.95)


def test_slope_hac_coincide_con_statsmodels():
    sm = pytest.importorskip("statsmodels.api")
    v, _ = _slope_lineal(lambda i: 5 * math.sin(i * 1.7) + 3 * math.cos(i * 0.21))
    res, _ = _correr("TCV-SLOPE-001", v)
    t = res["tramos"]["2s10s"]
    L = t["regresion"]["rezagos_hac"]
    n = len(v["historia_curva"]["fechas"])
    assert L == math.floor(4 * ((n - 1) / 100) ** (2 / 9))       # regla de ACC-FACT-001
    y = np.array([(f[4] - f[2]) * 100 for f in v["historia_curva"]["rendimientos"]])[:-1]
    X = np.column_stack([np.ones(n - 1)] + [np.array(r["serie"][:-1]) for r in v["regresores"].values()])
    ajuste = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": L, "use_correction": False})
    assert list(t["regresion"]["coeficientes"].values()) == pytest.approx(list(ajuste.params), rel=1e-8)
    assert list(t["regresion"]["errores_hac"].values()) == pytest.approx(list(ajuste.bse), rel=1e-8)
    s = math.sqrt(float(np.sum(ajuste.resid ** 2)) / (n - 1 - X.shape[1]))
    assert t["z"] == pytest.approx(t["residuo_pb"] / s, rel=1e-8)


def test_slope_regimen_y_tramo_3m10y():
    v = tcv.sintetico_slope(lambda t, i: 2.0 + (0.002 * i if t >= 10 else -0.001 * i))   # sube el largo, baja el corto
    res, _ = _correr("TCV-SLOPE-001", v, {"tramos": ["2s10s", "3m10y"]})
    assert res["tramos"]["2s10s"]["regimen"]["regimen"] == "empinamiento bajista"
    assert res["tramos"]["2s10s"]["regimen"]["cambio_pendiente_pb"] > 0
    assert res["tramos"]["3m10y"]["pendiente_pb"] == pytest.approx(res["tramos"]["2s10s"]["pendiente_pb"], rel=1e-12)
    v2 = tcv.sintetico_slope(lambda t, i: 3.0 - (0.003 * i if t <= 2 else 0.001 * i))
    res2, _ = _correr("TCV-SLOPE-001", v2)
    assert res2["tramos"]["2s10s"]["regimen"]["regimen"] == "empinamiento alcista"


def test_slope_forward_sin_extrapolar_se_declara():
    res, lim = _correr("TCV-SLOPE-001", BASE["TCV-SLOPE-001"][0], {"tramos": "5s30s"})
    t = res["tramos"]["5s30s"]
    assert t["pendiente_pb"] == pytest.approx(150.0)
    assert t["pendiente_forward_pb"] == {"3m": None, "6m": None}
    assert any("no se extrapola" in x for x in lim)


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v["historia_curva"].update(plazos=v["historia_curva"]["plazos"][:5],
                                          rendimientos=[f[:5] for f in v["historia_curva"]["rendimientos"]]), "nodos"),
    (lambda v: v["historia_curva"].update(fechas=v["historia_curva"]["fechas"][-200:],
                                          rendimientos=v["historia_curva"]["rendimientos"][-200:]), "años"),
    (lambda v: v["regresores"].pop("prima_plazo"), "prima_plazo"),
    (lambda v: v["regresores"]["prima_plazo"].pop("conocible_desde"), "conocible_desde"),
    (lambda v: v["regresores"]["prima_plazo"].pop("fuente"), "fuente"),
    (lambda v: v["regresores"]["prima_plazo"]["conocible_desde"].__setitem__(10, "2030-01-01"), "fuga"),
    (lambda v: v.pop("historia_curva"), "historia_curva"),
])
def test_slope_rechazos(cambio, motivo):
    v = copy.deepcopy(BASE["TCV-SLOPE-001"][0])
    cambio(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _correr("TCV-SLOPE-001", v)


def test_slope_rechazo_por_tramo():
    with pytest.raises(ErrorFicha, match="tramo no reconocido"):
        _correr("TCV-SLOPE-001", BASE["TCV-SLOPE-001"][0], {"tramos": "dos-diez"})
    with pytest.raises(ErrorFicha, match="fuera de la curva"):
        _correr("TCV-SLOPE-001", BASE["TCV-SLOPE-001"][0], {"tramos": "10s40s"})


def test_slope_historia_entre_5_y_10_anios_con_limitacion():
    _, lim = _correr("TCV-SLOPE-001", BASE["TCV-SLOPE-001"][0])
    assert any("< 10 de la entrada mínima" in x for x in lim)


# ============================================================================= TCV-BEI-001
def test_bei_valores_a_mano():
    v, p = BASE["TCV-BEI-001"]
    v = copy.deepcopy(v)
    v["swaps_inflacion"] = {"plazos": [1, 2, 5, 10], "tasas": [2.0, 2.15, 2.4, 2.55], "indice_referencia": "IPC"}
    v["inflacion_devengada"] = {"tasa": 3.1, "horizonte_meses": 3, "fuente": "previsión sintética"}
    res, _ = _correr("TCV-BEI-001", v, p)
    assert res["breakevens_pct"] == pytest.approx({"2": 2.1, "5": 2.3, "10": 2.5}, rel=1e-12)
    f = ((1.025 ** 10 / 1.023 ** 5) ** (1 / 5) - 1) * 100
    assert res["forward_5y5y_pct"] == pytest.approx(f, rel=1e-12)
    assert res["base_swap_bono_pb"] == pytest.approx({"2": 5.0, "5": 10.0, "10": 5.0}, rel=1e-9)
    assert res["brecha_encuestas_pb"]["10"] == pytest.approx(30.0, rel=1e-9)
    assert res["brecha_encuestas_pb"]["5y5y"] == pytest.approx((f - 2.3) * 100, rel=1e-9)
    assert res["carry_inflacion_pb"] == pytest.approx((3.1 - 2.1) * 100 * 0.25, rel=1e-9)


def test_bei_ajuste_estacional_por_nodo():
    v, _ = BASE["TCV-BEI-001"]
    v = copy.deepcopy(v)
    v["curva_real"]["plazos"] = [0.5, 1.5, 5, 10, 20]
    v["curva_nominal"]["plazos"] = [0.5, 1.5, 5, 10, 20]
    fac = [1.0] * 12
    fac[8] = 1.01                                  # septiembre estacionalmente alto
    v["estacionalidad"] = {"factores": fac, "mes_liquidacion": 6, "retardo_indexacion_meses": 3}
    res, _ = _correr("TCV-BEI-001", v, {"plazos": [1.5, 5]})
    # nodo de 1,5 años: liquidación en junio − 3 = marzo; vencimiento 18 meses después − 3 = septiembre
    sesgo = math.log(1.01) / 1.5 * 100
    assert res["breakevens_pct"]["1.5"] == pytest.approx(3.2 - 1.1 - sesgo, rel=1e-12)
    assert res["breakevens_pct"]["5"] == pytest.approx(2.3, rel=1e-12)
    assert "real 1.5" in res["ajuste_estacional_aplicado"] and "real 0.5" in res["ajuste_estacional_aplicado"]


def test_bei_historia_por_series_rol_y_percentil():
    v, p = BASE["TCV-BEI-001"]
    idx = pd.date_range("2013-01-04", periods=600, freq="W-FRI")
    s = pd.Series([2.0 + 0.5 * math.sin(i * 0.05) for i in range(600)], index=idx)
    res, _lim = _correr("TCV-BEI-001", v, p, {"breakeven_10": s})
    h = s.to_numpy()
    assert res["percentiles"]["10"]["percentil"] == pytest.approx(float(np.mean(h <= 2.5)))
    assert res["percentiles"]["10"]["anios"] > 10


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v["curva_real"].update(plazos=[2, 5], rendimientos=[1.1, 1.3]), "< 3 vencimientos"),
    (lambda v: v.update(swaps_inflacion={"plazos": [1, 2, 5], "tasas": [2, 2, 2], "indice_referencia": "HICP"}),
     "índices de referencia distintos"),
    (lambda v: v.pop("encuestas"), "encuestas"),
    (lambda v: v["encuestas"].pop("fecha"), "fecha"),
    (lambda v: v["curva_real"].pop("indice_referencia"), "indice_referencia"),
    (lambda v: v.pop("curva_real"), "curva_real"),
    (lambda v: v.pop("curva_nominal"), "curva_nominal"),
])
def test_bei_rechazos(cambio, motivo):
    v = copy.deepcopy(BASE["TCV-BEI-001"][0])
    cambio(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _correr("TCV-BEI-001", v, BASE["TCV-BEI-001"][1])


def test_bei_conversion_declarada_permite_indices_distintos():
    v = copy.deepcopy(BASE["TCV-BEI-001"][0])
    v["swaps_inflacion"] = {"plazos": [1, 2, 5, 10], "tasas": [2, 2, 2, 2], "indice_referencia": "HICP"}
    v["conversion_indice"] = "HICP→IPC con cuña media declarada por el solicitante"
    res, _ = _correr("TCV-BEI-001", v, BASE["TCV-BEI-001"][1])
    assert res["base_swap_bono_pb"]["10"] == pytest.approx(-50.0)


def test_bei_estacionalidad_obligatoria_a_corto():
    with pytest.raises(ErrorFicha, match="estacionalidad"):
        _correr("TCV-BEI-001", BASE["TCV-BEI-001"][0], {"ajuste_estacional": True})


# ============================================================================= TCV-CDS-001
def test_cds_valores_a_mano():
    v = copy.deepcopy(BASE["TCV-CDS-001"][0])
    v["contado"]["diferencial_pb"] = 130.0
    v["curva_diferenciales"] = {"plazos": [3, 5, 7, 10], "diferenciales_pb": [110.0, 150.0, 170.0, 190.0]}
    v["vencimiento_anios"] = 5
    v["tipo_libre"] = 3.0
    res, _ = _correr("TCV-CDS-001", v)
    assert res["diferencial_pb"] == 150.0 and res["recuperacion"] == 0.40
    assert res["lambda_pct_anual"] == pytest.approx(2.5, rel=1e-12)            # 150 pb / (1 − 0,4)
    assert res["perdida_esperada_pb"] == pytest.approx(120.0, rel=1e-12)       # 2 % · 0,6
    assert res["prima_pb"] == pytest.approx(30.0, rel=1e-10)
    assert res["ratio_diferencial_perdida"] == pytest.approx(1.25, rel=1e-12)
    assert res["base_pb"] == pytest.approx(20.0)
    assert res["pendiente_pb"] == pytest.approx(40.0)
    k = math.log(1.03) + 0.025
    rpv01 = lambda t: (1 - math.exp(-k * t)) / k
    assert res["duracion_con_riesgo"] == pytest.approx(rpv01(5), rel=1e-12)
    assert res["dv01"] == pytest.approx(rpv01(5) / 1e4, rel=1e-12)
    assert res["carry_pb_anual"] == pytest.approx(150 + rpv01(4) * (150 - 130), rel=1e-12)
    assert res["percentil"] == 1.0


def test_cds_pd_por_rating_y_fase_del_ciclo():
    v = copy.deepcopy(BASE["TCV-CDS-001"][0])
    v["impagos"] = {"fuente": "tabla sintética", "rating_medio": "BBB",
                    "tasas_por_rating": {"BBB": {"2008": 0.03, "2009": 0.05, "2015": 0.01}}, "anios": [2008, 2009]}
    res, _ = _correr("TCV-CDS-001", v)
    assert res["pd_anual"] == pytest.approx(0.04)
    assert res["perdida_esperada_pb"] == pytest.approx(240.0)


def test_cds_por_series_rol():
    v = copy.deepcopy(BASE["TCV-CDS-001"][0])
    v.pop("historia")
    idx = pd.date_range("2016-01-01", periods=1600, freq="B")
    s = pd.Series([90.0 + 10 * math.sin(i * 0.01) for i in range(1600)], index=idx)
    res, lim = _correr("TCV-CDS-001", v, series_rol={"diferencial_indice": s})
    assert res["diferencial_pb"] == pytest.approx(float(s.iloc[-1]))
    assert any("percentil con limitación" in x for x in lim)


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v["indice"].pop("serie"), "serie y versión"),
    (lambda v: v["indice"].pop("version"), "serie y versión"),
    (lambda v: v["historia"].update(fechas=v["historia"]["fechas"][-200:],
                                    diferenciales_pb=v["historia"]["diferenciales_pb"][-200:]), "< 5"),
    (lambda v: v["indice"].update(segmento="HY"), "HY sin «recuperacion»"),
    (lambda v: v["impagos"].pop("fuente"), "fuente"),
    (lambda v: v.pop("impagos"), "impagos"),
    (lambda v: v.pop("contado"), "contado"),
    (lambda v: v["contado"].update(medida="precio"), "OAS o Z"),
    (lambda v: v["indice"].update(cotizacion="precio"), "conversión"),
])
def test_cds_rechazos(cambio, motivo):
    v = copy.deepcopy(BASE["TCV-CDS-001"][0])
    cambio(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _correr("TCV-CDS-001", v)


def test_cds_hy_con_recuperacion_declarada():
    v = copy.deepcopy(BASE["TCV-CDS-001"][0])
    v["indice"]["segmento"] = "HY"
    res, _ = _correr("TCV-CDS-001", v, {"recuperacion": 0.3})
    assert res["recuperacion"] == 0.3
    assert res["perdida_esperada_pb"] == pytest.approx(0.02 * 0.7 * 1e4)


# ============================================================================= TCV-VIXTS-001
def test_vixts_valores_a_mano():
    v = copy.deepcopy(BASE["TCV-VIXTS-001"][0])
    v["indices_plazo"] = {"VIX3M": 17.5}
    res, _ = _correr("TCV-VIXTS-001", v)
    assert res["estado"] == "contango"
    assert res["roll_puntos_dia"] == pytest.approx(0.05)                        # (16 − 15)/20
    assert res["roll_pct_mensual"] == pytest.approx(1 / 16 * 30 / 20 * 100)     # mes = 30 días (vencimiento constante)
    assert res["futuro_vencimiento_constante"] == pytest.approx(17.0)           # mitad entre 20 y 40 días
    assert res["pesos_interpolacion"] == pytest.approx({"F1": 0.5, "F2": 0.5})
    assert res["rentabilidad_esperada_larga_pct"] == pytest.approx((15 / 17 - 1) * 100)
    assert res["rentabilidad_esperada_corta_pct"] == pytest.approx(-(15 / 17 - 1) * 100)
    assert res["ratios"] == pytest.approx({"F1/spot": 16 / 15, "F2/F1": 18 / 16, "spot/VIX3M": 15 / 17.5})
    h = v["historia"]
    pend = np.array(h["f2"]) - np.array(h["f1"])
    assert res["percentil_pendiente"] == pytest.approx(float(np.mean(pend <= 2.0)))
    ok = (np.array(h["f2"]) > np.array(h["f1"])) & (np.array(h["f1"]) > np.array(h["spot"]))
    assert res["frecuencia_contango"] == pytest.approx(float(np.mean(ok)))


def test_vixts_backwardation_y_mixta():
    res, _ = _correr("TCV-VIXTS-001", tcv.sintetico_vixts(30.0, [26.0, 24.0], [10, 40]))
    assert res["estado"] == "backwardation" and res["roll_puntos_dia"] == pytest.approx(-0.4)
    res, _ = _correr("TCV-VIXTS-001", tcv.sintetico_vixts(20.0, [21.0, 20.5], [10, 40]))
    assert res["estado"] == "mixta"


def test_vixts_rentabilidades_por_estado_y_es():
    v = tcv.sintetico_vixts(15.0, [16.0, 18.0], [20, 40], n=300)          # 300 semanas ≥ 250 (RISK-VAR-001)
    n = len(v["historia"]["fechas"])
    r = [math.sin(i * 0.9) * 2 for i in range(n)]
    v["historia"]["rent_larga"] = r
    v["historia"]["fuente_rentabilidades"] = "índice sintético a 30 días"
    res, _lim = _correr("TCV-VIXTS-001", v)
    corta = -np.array(r)
    q = np.quantile(corta, 1 - 0.975)
    assert res["es_corta_pct"] == pytest.approx(float(-np.mean(corta[corta <= q])))
    h = v["historia"]
    est = ["contango" if (b > a > s) else ("backwardation" if (b < a < s) else "otros")
           for s, a, b in zip(h["spot"], h["f1"], h["f2"])]
    m = [r[i + 1] for i in range(n - 1) if est[i] == "contango"]
    assert res["rentabilidades_por_estado"]["contango"]["larga_pct"] == pytest.approx(float(np.mean(m)))
    assert res["rentabilidades_por_estado"]["contango"]["n"] == len(m)
    # con menos de 250 observaciones (RISK-VAR-001) el ES no se calcula y se declara
    corto = copy.deepcopy(BASE["TCV-VIXTS-001"][0])
    corto["historia"]["rent_larga"] = r[:len(corto["historia"]["fechas"])]
    corto["historia"]["fuente_rentabilidades"] = "índice sintético a 30 días"
    res2, lim2 = _correr("TCV-VIXTS-001", corto)
    assert res2["es_corta_pct"] is None and any("RISK-VAR-001" in x for x in lim2)


def test_vixts_por_series_rol():
    v = copy.deepcopy(BASE["TCV-VIXTS-001"][0])
    h = v.pop("historia")
    idx = pd.to_datetime(h["fechas"])
    roles = {"indice_spot": pd.Series(h["spot"], index=idx), "futuro_1": pd.Series(h["f1"], index=idx),
             "futuro_2": pd.Series(h["f2"], index=idx)}
    res, _ = _correr("TCV-VIXTS-001", v, series_rol=roles)
    ref, _ = _correr("TCV-VIXTS-001", BASE["TCV-VIXTS-001"][0])
    assert res["percentil_pendiente"] == ref["percentil_pendiente"]


def test_vixts_sin_vencimientos_que_rodeen_30_dias():
    res, lim = _correr("TCV-VIXTS-001", tcv.sintetico_vixts(15.0, [16.0, 17.0], [35, 60]))
    assert res["futuro_vencimiento_constante"] is None and any("no se extrapola" in x for x in lim)


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v["futuros"].update(dias=[20], precios=[16.0]), "< 2 vencimientos"),
    (lambda v: v.pop("futuros"), "futuros"),
    (lambda v: v.pop("historia"), "historia"),
    (lambda v: v["historia"].update({k: v["historia"][k][-100:] for k in ("fechas", "spot", "f1", "f2")}), "< 3"),
    (lambda v: v["futuros"].update(dias=[40, 20]), "crecientes"),
    (lambda v: v.pop("spot"), "spot"),
])
def test_vixts_rechazos(cambio, motivo):
    v = copy.deepcopy(BASE["TCV-VIXTS-001"][0])
    cambio(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _correr("TCV-VIXTS-001", v)


# ============================================================================= TCV-TP-001
def test_tp_acm_identidad_ajuste_y_recuperacion():
    v, verdad = tcv.sintetico_acm()
    res, _lim = _correr("TCV-TP-001", v, {"n_factores": 3})
    for c in ("2", "5", "10"):
        assert res["prima_pb"][c] / 100 + res["rendimiento_neutral_pct"][c] == pytest.approx(
            res["rendimiento_ajustado_pct"][c], abs=1e-12)
        assert res["prima_pb"][c] == pytest.approx(verdad[c], abs=1e-6)
        assert res["rendimiento_ajustado_pct"][c] == pytest.approx(res["rendimiento_observado_pct"][c], abs=1e-9)
        d = res["descomposicion_cambios_pb"][c]
        assert d["cambio_ajustado_pb"] == pytest.approx(d["senda_esperada_pb"] + d["prima_pb"], abs=1e-9)
        assert res["serie"]["prima_pb"][c][-1] == res["prima_pb"][c]
    assert res["error_ajuste_pb"]["rmse"] < 5 and res["error_ajuste_pb"]["max_abs"] < 5
    assert res["percentiles"]["10"]["n"] == 241 and res["percentiles"]["10"]["anios"] == pytest.approx(20.0)


def test_tp_acm_rejilla_gruesa_ajuste_menor_de_5_pb():
    v, _verdad = tcv.sintetico_acm(plazos=[1, 3, 6, 12, 24, 36, 60, 84, 120])
    res, _ = _correr("TCV-TP-001", v, {"n_factores": 3})
    assert res["error_ajuste_pb"]["rmse"] < 5
    for c in ("2", "5", "10"):
        assert res["prima_pb"][c] / 100 + res["rendimiento_neutral_pct"][c] == pytest.approx(
            res["rendimiento_ajustado_pct"][c], abs=1e-12)


def test_tp_acm_no_verificado_falla_cerrado():
    v, _ = tcv.sintetico_acm(plazos=[1, 3, 6, 12, 24, 36, 60, 84, 120])
    filas = v["curva"]["rendimientos"]
    for i, fila in enumerate(filas):                          # ruido de ±1 % en el nodo de 3 años
        fila[5] += math.sin(i * 2.1 + 0.3)
    with pytest.raises(ErrorFicha, match="ACM no verificado"):
        _correr("TCV-TP-001", v, {"n_factores": 3})


def test_tp_segunda_via_publicada():
    v, verdad = tcv.sintetico_acm()
    fechas = v["curva"]["fechas"]
    v["serie_publicada"] = {"fuente": "serie ACM publicada (sintética)", "fechas": fechas,
                            "primas_pb": {"10": [verdad["10"] + 3.0] * len(fechas)}}
    res, _ = _correr("TCV-TP-001", v, {"n_factores": 3})
    assert res["segunda_via"]["metodo"] == "publicado"
    assert res["segunda_via"]["diferencia_pb"]["10"] == pytest.approx(-3.0, abs=1e-6)


def test_tp_metodo_publicado_a_mano():
    fechas = pd.date_range("2010-01-01", periods=181, freq="MS").strftime("%Y-%m-%d").tolist()
    primas = [10.0 + i * 0.5 for i in range(181)]
    rends = [3.0 + i * 0.01 for i in range(181)]
    v = {"serie_publicada": {"fuente": "Kim-Wright (sintética)", "fechas": fechas, "primas_pb": {"10": primas},
                             "rendimientos_pct": {"10": rends}}}
    res, lim = _correr("TCV-TP-001", v, {"metodo": "publicado"})
    assert res["prima_pb"]["10"] == 100.0 and res["percentiles"]["10"]["percentil"] == 1.0
    assert res["rendimiento_neutral_pct"]["10"] == pytest.approx(4.8 - 1.0)
    d = res["descomposicion_cambios_pb"]["10"]
    assert d["cambio_ajustado_pb"] == pytest.approx(1.0) and d["prima_pb"] == pytest.approx(0.5)
    assert d["senda_esperada_pb"] == pytest.approx(0.5)
    assert any("< 20" in x for x in lim)
    idx = pd.to_datetime(fechas)
    res2, _ = _correr("TCV-TP-001", {"serie_publicada": {"fuente": "Kim-Wright"}}, {"metodo": "publicado"},
                      {"prima_publicada_10": pd.Series(primas, index=idx)})
    assert res2["prima_pb"]["10"] == 100.0


@pytest.mark.parametrize("cambio,params,motivo", [
    (lambda v: v["curva"].update(fechas=v["curva"]["fechas"][-100:], rendimientos=v["curva"]["rendimientos"][-100:]),
     {"n_factores": 3}, "< 10"),
    (lambda v: None, {"n_factores": 2}, "fuera del rango"),
    (lambda v: None, {"n_factores": 6}, "fuera del rango"),
    (lambda v: v["curva"]["fechas"].__setitem__(5, "2000-05-15"), {"n_factores": 3}, "mensual"),
    (lambda v: v["curva"].update(plazos_meses=v["curva"]["plazos_meses"][1:],
                                 rendimientos=[f[1:] for f in v["curva"]["rendimientos"]]), {"n_factores": 3}, "1"),
    (lambda v: v["curva"].update(plazos_meses=v["curva"]["plazos_meses"][:60],
                                 rendimientos=[f[:60] for f in v["curva"]["rendimientos"]]), {"n_factores": 3},
     "10 años"),
    (lambda v: v.pop("curva"), {"n_factores": 3}, "curva"),
    (lambda v: None, {"metodo": "otro"}, "no reconocido"),
    (lambda v: None, {"metodo": "publicado"}, "serie_publicada"),
    (lambda v: None, {"metodo": "encuesta"}, "encuesta"),
    (lambda v: None, {}, "factores independientes"),
])
def test_tp_rechazos(cambio, params, motivo):
    v = copy.deepcopy(BASE["TCV-TP-001"][0])
    cambio(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _correr("TCV-TP-001", v, params)


def test_tp_publicado_menor_de_10_anios_rechazado():
    fechas = pd.date_range("2018-01-01", periods=60, freq="MS").strftime("%Y-%m-%d").tolist()
    v = {"serie_publicada": {"fuente": "ACM", "fechas": fechas, "primas_pb": {"10": [1.0] * 60}}}
    with pytest.raises(ErrorFicha, match="< 10"):
        _correr("TCV-TP-001", v, {"metodo": "publicado"})


# ============================================================================= QA r01 (H-02, H-11): falla cerrado
RAROS = [None, "x", [], {}, float("nan"), float("inf"), float("-inf"), 0, -1, 1e300, True, -1e-300, [1, 2], {"a": 1},
         1 + 2j, 20261110]


def _hojas(x, ruta=()):
    if isinstance(x, dict):
        for k in sorted(x, key=str):
            yield ruta + (k,)
            yield from _hojas(x[k], ruta + (k,))
    elif isinstance(x, list):
        for i in (sorted({0, len(x) // 2, len(x) - 1}) if len(x) > 3 else range(len(x))):
            yield ruta + (i,)
            yield from _hojas(x[i], ruta + (i,))


def _poner(x, ruta, valor):
    y = copy.deepcopy(x)
    d = y
    for r in ruta[:-1]:
        d = d[r]
    d[ruta[-1]] = valor
    return y


def _todos_finitos(x):
    if isinstance(x, dict):
        return all(_todos_finitos(v) for v in x.values())
    if isinstance(x, list):
        return all(_todos_finitos(v) for v in x)
    if isinstance(x, float):
        return math.isfinite(x)
    return True


def _mutaciones(ficha):
    v, p = BASE[ficha]
    if ficha == "TCV-TP-001":                       # rejilla gruesa: misma cobertura, mucho más rápida
        v = tcv.sintetico_acm(plazos=[1, 3, 6, 12, 24, 36, 60, 84, 120])[0]
    rutas = list(_hojas(v))
    for i, ruta in enumerate(rutas):
        for raro in RAROS[i % len(RAROS):] + RAROS[:i % len(RAROS)][:4]:
            yield ruta, raro, v, p
    for k in list(tcv.PARAMETROS_POR_DEFECTO[ficha]):
        for raro in RAROS:
            yield ("__param__", k), raro, v, p


@pytest.mark.parametrize("ficha", sorted(BASE))
def test_mutaciones_de_datos_solo_dan_error_ficha_y_cifras_finitas(ficha):
    """Regresión de H-02: ninguna mutación de una hoja o de un parámetro lanza otra excepción ni sirve no finitos."""
    vistos = 0
    for ruta, raro, v, p in _mutaciones(ficha):
        if ruta[0] == "__param__":
            valores, params = v, {**p, ruta[1]: raro}
        else:
            valores, params = _poner(v, ruta, raro), p
        try:
            res, _lim = _correr(ficha, valores, params)
        except ErrorFicha:
            continue
        vistos += 1
        assert _todos_finitos(res), (ruta, raro)
        json.dumps(res, allow_nan=False)
    assert vistos > 0


@pytest.mark.parametrize("ficha", sorted(BASE))
@pytest.mark.parametrize("ent", [None, [], "x", {"valores": [1]}, {"valores": {}, "series_rol": [1]}])
def test_entrada_que_no_es_objeto(ficha, ent):
    with pytest.raises(ErrorFicha):
        tcv.FICHAS[ficha]["fn"](ent, {})


@pytest.mark.parametrize("ficha", sorted(BASE))
def test_umbrales_de_la_ficha_no_se_cambian_por_parametro(ficha):
    clave = next(iter(tcv.UMBRALES[ficha]))
    v, p = BASE[ficha]
    with pytest.raises(ErrorFicha, match="umbrales fijos"):
        _correr(ficha, v, {**p, clave: tcv.UMBRALES[ficha][clave]})


@pytest.mark.parametrize("fecha", [20261110, 20261110.0, "20261110", True, "10/11/2026", "2026-13-01"])
def test_fechas_numericas_o_no_iso_se_rechazan(fecha):
    v = copy.deepcopy(BASE["TCV-SLOPE-001"][0])
    v["regresores"]["prima_plazo"]["conocible_desde"][0] = fecha
    with pytest.raises(ErrorFicha, match="fecha no válida"):
        _correr("TCV-SLOPE-001", v)


def test_serie_de_rol_con_indice_numerico_se_rechaza():
    v = copy.deepcopy(BASE["TCV-CDS-001"][0])
    v.pop("historia")
    s = pd.Series([90.0] * 1600, index=range(20000101, 20001601 + 20000000)[:1600])
    with pytest.raises(ErrorFicha, match="índice de fechas"):
        _correr("TCV-CDS-001", v, series_rol={"diferencial_indice": s})


@pytest.mark.parametrize("plazos", [[1, 3, 6, 12, 24, 60, 120, 120_000_000], [1, 3, 6, 12, 24, 60, 240],
                                    [1, 3, 6, 12, 24, 60, 119]])
def test_tp_plazos_fuera_de_1_a_10_anios_se_rechazan_sin_colgarse(plazos):
    v = {"curva": {"fechas": tcv._fechas_mensuales(2000, 130), "plazos_meses": plazos,
                   "rendimientos": [[3.0] * len(plazos)] * 130}}
    with pytest.raises(ErrorFicha, match="120 meses"):
        _correr("TCV-TP-001", v, {"n_factores": 3})


def test_tp_filas_de_distinta_longitud_se_rechazan():
    v = copy.deepcopy(BASE["TCV-TP-001"][0])
    v["curva"]["rendimientos"][7] = v["curva"]["rendimientos"][7][:-1]
    with pytest.raises(ErrorFicha, match="cada fila"):
        _correr("TCV-TP-001", v, {"n_factores": 3})


def test_cds_eco_del_indice_validado():
    v = copy.deepcopy(BASE["TCV-CDS-001"][0])
    v["indice"]["serie"] = float("inf")
    with pytest.raises(ErrorFicha, match="indice.serie"):
        _correr("TCV-CDS-001", v)
    v["indice"]["serie"] = 41
    v["indice"]["segmento"] = "XX"
    with pytest.raises(ErrorFicha, match="segmento"):
        _correr("TCV-CDS-001", v)


def test_parametros_fuera_de_rango():
    v, _ = BASE["TCV-SLOPE-001"]
    with pytest.raises(ErrorFicha, match="horizonte_carry"):
        _correr("TCV-SLOPE-001", v, {"horizonte_carry": 13})     # FIR-CARRY-001: delta_t en 1–12 meses
    with pytest.raises(ErrorFicha, match="nivel_es"):
        _correr("TCV-VIXTS-001", BASE["TCV-VIXTS-001"][0], {"nivel_es": 0.5})   # RISK-VAR-001: 0,90–0,99
    with pytest.raises(ErrorFicha, match="ajuste_estacional"):
        _correr("TCV-BEI-001", BASE["TCV-BEI-001"][0], {"ajuste_estacional": "no"})
