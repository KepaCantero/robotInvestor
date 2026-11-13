"""T-112 · Motor Fase 2, grupo V (valoración de RV, RF, FX y DER): ACC-VAL-001, ACC-ERP-001, ACC-FACT-001,
FIR-PRICE-001, FIR-CURVE-001, FIR-CARRY-001, FIR-SPREAD-001, FX-MOM-001, FX-PPA-001 y DER-OPT-001.

Casos de control de la «Verificación» (y que pueden fallar), rechazos de «Aclaración y rechazo» y de «Entradas mínimas»,
dominio de cada parámetro, umbrales fijos, determinismo, entradas hostiles y, por ficha, al menos un oráculo
independiente: el resultado se recalcula aquí por otra vía, sin llamar al código de la ficha."""
import copy
import json
import math
from datetime import date
from itertools import pairwise
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from bloque_a.motor import fichas_tcv
from bloque_a.motor import fichas_valoracion as V
from bloque_a.motor.operaciones import ErrorFicha
from scipy import optimize

FICHAS = ["ACC-VAL-001", "ACC-ERP-001", "ACC-FACT-001", "FIR-PRICE-001", "FIR-CURVE-001", "FIR-CARRY-001",
          "FIR-SPREAD-001", "FX-MOM-001", "FX-PPA-001", "DER-OPT-001"]


def _ent(valores, series=None):
    return {"valores": copy.deepcopy(valores), "series": series or {}, "series_rol": {}}


def _correr(ficha, valores, params=None, series=None):
    return V.FICHAS[ficha]["fn"](_ent(valores, series), copy.deepcopy(params or {}))


def _valores_caso(caso):
    v = {}
    for d in caso["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    return v


def _caso(ficha, i=0):
    c = V.CASOS_CONTROL[ficha][i]
    return _valores_caso(c), dict(c["parametros"])


CASOS = [(f, c) for f, casos in V.CASOS_CONTROL.items() for c in casos]

# Datos base por ficha (rápidos): FIR-CURVE con λ de Diebold-Li (MCO) para no repetir los 20 arranques en cada prueba.
BASE = {f: _caso(f) for f in FICHAS}
BASE["FIR-CURVE-001"] = _caso("FIR-CURVE-001", 2)


def _error(ficha, valores, params=None, match=None, series=None):
    with pytest.raises(ErrorFicha, match=match):
        _correr(ficha, valores, params, series)


# ============================================================================= registro y casos de control
def test_registro_de_las_diez_fichas():
    for d in (V.FICHAS, V.PARAMETROS_POR_DEFECTO, V.UMBRALES, V.ADVERTENCIAS, V.CASOS_CONTROL):
        assert set(d) == set(FICHAS)
    for f, meta in V.FICHAS.items():
        assert set(meta) == {"fn", "modulo", "version", "cifra", "ri", "tol"} and callable(meta["fn"])
        assert meta["cifra"] in ("DETERMINISTA", "ESTADISTICA") and meta["ri"] and meta["tol"] > 0
        assert meta["modulo"] == ("MC-03" if f == "FX-PPA-001" else "MC-09")
        assert meta["version"] == ("1.1" if f == "FX-PPA-001" else "1.0")
        assert V.ADVERTENCIAS[f] and len(V.CASOS_CONTROL[f]) >= 2
    # tolerancias de la ficha («Tolerancias y semilla»)
    assert V.FICHAS["FIR-PRICE-001"]["tol"] == 1e-10 and V.FICHAS["ACC-ERP-001"]["tol"] == 1e-6
    assert V.FICHAS["FIR-CURVE-001"]["tol"] == 1e-6 and V.FICHAS["DER-OPT-001"]["tol"] == 1e-8


@pytest.mark.parametrize("ficha,caso", CASOS, ids=[f"{f}:{c['nombre'][:60]}" for f, c in CASOS])
def test_casos_de_control(ficha, caso):
    res, lim = _correr(ficha, _valores_caso(caso), caso["parametros"])
    assert caso["comprobar"](res)
    json.dumps(res, allow_nan=False)
    assert all(isinstance(x, str) for x in lim)
    assert res["advertencias"][:len(V.ADVERTENCIAS[ficha])] == V.ADVERTENCIAS[ficha]


def _perturbar(x, cuenta):
    """Mueve cada número del resultado de forma no uniforme (alterna signo y escala) para que ninguna identidad sobreviva
    por invariancia de escala."""
    if isinstance(x, dict):
        return {k: _perturbar(v, cuenta) for k, v in x.items()}
    if isinstance(x, list):
        return [_perturbar(v, cuenta) for v in x]
    if isinstance(x, float) and not isinstance(x, bool):
        cuenta[0] += 1
        return x + (-1) ** cuenta[0] * 1e-3 * (1 + abs(x)) * (1 + cuenta[0] % 3)
    return x


@pytest.mark.parametrize("ficha,caso", CASOS, ids=[f"{f}:{c['nombre'][:60]}" for f, c in CASOS])
def test_cada_caso_de_control_puede_fallar(ficha, caso):
    res, _ = _correr(ficha, _valores_caso(caso), caso["parametros"])
    assert not caso["comprobar"](_perturbar(res, [0]))


# ============================================================================= umbrales fijos, dominio y determinismo
@pytest.mark.parametrize("ficha,umbral", [(f, u) for f in FICHAS for u in V.UMBRALES[f]])
def test_ningun_umbral_se_cambia_desde_la_peticion(ficha, umbral):
    v, p = BASE[ficha]
    _error(ficha, v, {**p, umbral: V.UMBRALES[ficha][umbral]}, "umbrales fijos")


@pytest.mark.parametrize("ficha", FICHAS)
def test_un_parametro_no_declarado_se_rechaza_y_clase_se_ignora(ficha):
    v, p = BASE[ficha]
    _error(ficha, v, {**p, "parametro_inventado": 1}, "no declarados")
    r1, _ = _correr(ficha, v, {**p, "clase": "ACC"})
    r2, _ = _correr(ficha, v, p)
    assert r1 == r2


DOMINIO_MALO = [
    ("ACC-VAL-001", "anios_explicitos", 2), ("ACC-VAL-001", "anios_explicitos", 11), ("ACC-VAL-001", "anios_explicitos", 5.5),
    ("ACC-VAL-001", "anios_explicitos", "5"), ("ACC-VAL-001", "g_terminal", -0.1), ("ACC-VAL-001", "g_terminal", 3.5),
    ("ACC-VAL-001", "PRM", 2.9), ("ACC-VAL-001", "PRM", 7.1), ("ACC-VAL-001", "tasa_impositiva", 100),
    ("ACC-VAL-001", "tasa_impositiva", -1), ("ACC-VAL-001", "enfoque", "APV"),
    ("ACC-ERP-001", "g_L", 2.9), ("ACC-ERP-001", "g_L", 4.1), ("ACC-ERP-001", "g_L", "4"),
    ("ACC-ERP-001", "incluir_recompras", "sí"), ("ACC-ERP-001", "ventana_percentil", 9),
    ("ACC-FACT-001", "modelo", "FF6"), ("ACC-FACT-001", "adicionales", ["XYZ"]), ("ACC-FACT-001", "adicionales", ["QMJ", "QMJ"]),
    ("ACC-FACT-001", "adicionales", "QMJ"), ("ACC-FACT-001", "frecuencia", "diaria"), ("ACC-FACT-001", "ventana_movil", 0),
    ("ACC-FACT-001", "ventana_movil", 2.5),
    ("FIR-PRICE-001", "convencion", "ACT/360"), ("FIR-PRICE-001", "delta_y", 0.5), ("FIR-PRICE-001", "delta_y", 26),
    ("FIR-CURVE-001", "modelo", "spline"), ("FIR-CURVE-001", "lambda", "fijo"), ("FIR-CURVE-001", "arranques", 19),
    ("FIR-CURVE-001", "arranques", 201), ("FIR-CURVE-001", "arranques", 20.5), ("FIR-CURVE-001", "semilla", -1),
    ("FIR-CURVE-001", "semilla", 1.5),
    ("FIR-CARRY-001", "delta_t", 0.5), ("FIR-CARRY-001", "delta_t", 13), ("FIR-CARRY-001", "delta_t", True),
    ("FIR-SPREAD-001", "ventana", 9), ("FIR-SPREAD-001", "recuperacion", 0.1), ("FIR-SPREAD-001", "recuperacion", 0.7),
    ("FIR-SPREAD-001", "ajuste_composicion", 1),
    ("FX-MOM-001", "retrospecciones", [0]), ("FX-MOM-001", "retrospecciones", [13]), ("FX-MOM-001", "retrospecciones", [3, 3]),
    ("FX-MOM-001", "retrospecciones", []), ("FX-MOM-001", "volatilidad", "garch"),
    ("FX-PPA-001", "ventana", 23), ("FX-PPA-001", "base", "media"), ("FX-PPA-001", "suavizado", 0),
    ("DER-OPT-001", "modelo", "Heston"), ("DER-OPT-001", "pasos", 1), ("DER-OPT-001", "pasos", 5001),
    ("DER-OPT-001", "tol_iv", 0), ("DER-OPT-001", "tol_iv", 1e-5), ("DER-OPT-001", "densidad", "no"),
    # QA r01 de T-112, H-01: cotas superiores de los parámetros de tamaño
    ("ACC-ERP-001", "ventana_percentil", 101), ("ACC-FACT-001", "ventana_movil", 1201), ("FIR-CURVE-001", "arranques", 101),
    ("FIR-SPREAD-001", "ventana", 101), ("FX-PPA-001", "ventana", 1201), ("FX-PPA-001", "suavizado", 1201),
    ("DER-OPT-001", "pasos", 1001),
]


@pytest.mark.parametrize("ficha,param,valor", DOMINIO_MALO)
def test_dominio_de_cada_parametro(ficha, param, valor):
    v, p = BASE[ficha]
    if ficha == "FX-PPA-001" and param == "suavizado":
        v = V.sintetico_ppa(36, 0.002, 0.002)
    _error(ficha, v, {**p, param: valor}, "rango|admitid|entero|true o false|lista|repetid|número|declarad|elementos")


DOMINIO_BUENO: list[tuple[str, dict]] = [
    ("ACC-VAL-001", {"anios_explicitos": 10}), ("ACC-VAL-001", {"g_terminal": 2.0, "PRM": 7}),
    ("ACC-VAL-001", {"tasa_impositiva": 30, "enfoque": "FCFE"}), ("ACC-ERP-001", {"g_L": 3.0}),
    ("ACC-ERP-001", {"incluir_recompras": False, "ventana_percentil": 10}),
    ("ACC-FACT-001", {"modelo": "FF3", "adicionales": ["QMJ", "BAB"], "ventana_movil": 24}),
    ("FIR-PRICE-001", {"delta_y": 1}), ("FIR-PRICE-001", {"delta_y": 25}),
    ("FIR-CARRY-001", {"delta_t": 1}), ("FIR-CARRY-001", {"delta_t": 12}),
    ("FIR-SPREAD-001", {"ventana": 10, "recuperacion": 0.2}), ("FIR-SPREAD-001", {"recuperacion": 0.6, "ajuste_composicion": True}),
    ("FX-MOM-001", {"retrospecciones": [12, 6, 1], "volatilidad": "realizada"}),
    ("FX-PPA-001", {"ventana": 24, "base": "media_largo_plazo", "suavizado": 3}),
    ("DER-OPT-001", {"modelo": "CRR", "pasos": 50, "tol_iv": 1e-6}), ("DER-OPT-001", {"modelo": "Black-76"}),
    # QA r01 de T-112, H-01: las cotas superiores se admiten
    ("ACC-ERP-001", {"ventana_percentil": 100}), ("ACC-FACT-001", {"ventana_movil": 1200}), ("FIR-SPREAD-001", {"ventana": 100}),
    ("FX-PPA-001", {"ventana": 1200}), ("DER-OPT-001", {"pasos": 1000}), ("DER-OPT-001", {"modelo": "CRR", "pasos": 2}),
]


@pytest.mark.parametrize("ficha,params", DOMINIO_BUENO, ids=[f"{f}:{sorted(map(str, p))}" for f, p in DOMINIO_BUENO])
def test_parametros_dentro_de_su_dominio_se_sirven(ficha, params):
    v, p = BASE[ficha]
    if ficha == "DER-OPT-001" and params.get("modelo") == "Black-76":
        v = {"contratos": [{**{k: x for k, x in V._OPT_REF.items() if k != "q"}, "tipo": "call"}]}
    res, _ = _correr(ficha, v, {**p, **params})
    json.dumps(res, allow_nan=False)


@pytest.mark.parametrize("ficha", FICHAS)
def test_determinismo_dos_pasadas(ficha):
    v, p = BASE[ficha]
    a, la = _correr(ficha, v, p)
    b, lb = _correr(ficha, v, p)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True) and la == lb


def test_determinismo_nss_con_arranques_y_semilla():
    v, _ = _caso("FIR-CURVE-001", 0)
    a, _ = _correr("FIR-CURVE-001", v, {"semilla": 7})
    b, _ = _correr("FIR-CURVE-001", v, {"semilla": 7})
    assert a == b and a["semilla"] == 7 and a["arranques"] == 20


# ============================================================================= entradas hostiles
@pytest.mark.parametrize("ficha", FICHAS)
@pytest.mark.parametrize("ent", [None, [], "x", {"valores": []}, {"valores": "x"}, {"valores": {}, "series": []},
                                 {"valores": {}, "series_rol": 5}, {"valores": {}}])
def test_entradas_mal_formadas(ficha, ent):
    with pytest.raises(ErrorFicha):
        V.FICHAS[ficha]["fn"](ent, {})


@pytest.mark.parametrize("ficha", FICHAS)
@pytest.mark.parametrize("params", ["x", [1], 5])
def test_parametros_que_no_son_un_objeto(ficha, params):
    v, _ = BASE[ficha]
    with pytest.raises(ErrorFicha):
        V.FICHAS[ficha]["fn"](_ent(v), params)


# Ruta de un número de cada ficha en sus datos base: se sustituye por valores hostiles.
RUTAS = {
    "ACC-VAL-001": ["deuda_neta"], "ACC-ERP-001": ["nivel"], "ACC-FACT-001": ["rendimientos", 5],
    "FIR-PRICE-001": ["cupon"], "FIR-CURVE-001": ["curva", "rendimientos", 2], "FIR-CARRY-001": ["financiacion"],
    "FIR-SPREAD-001": ["historia", "diferenciales_pb", 10], "FX-MOM-001": ["pares", "EURUSD", "spot", "valores", 30],
    "FX-PPA-001": ["tipo_cambio", 4], "DER-OPT-001": ["contratos", 0, "S"],
}


@pytest.mark.parametrize("ficha", FICHAS)
@pytest.mark.parametrize("malo", [float("nan"), float("inf"), -float("inf"), "1.0", None, True, [1.0], {"v": 1}])
def test_numeros_hostiles(ficha, malo):
    v, p = copy.deepcopy(BASE[ficha])
    d = v
    for k in RUTAS[ficha][:-1]:
        d = d[k]
    d[RUTAS[ficha][-1]] = malo
    _error(ficha, v, p)


@pytest.mark.parametrize("ficha", FICHAS)
def test_vacios(ficha):
    _error(ficha, {}, {})
    if len(RUTAS[ficha]) < 2:
        return
    v, p = copy.deepcopy(BASE[ficha])
    d = v
    for k in RUTAS[ficha][:-2]:
        d = d[k]
    d[RUTAS[ficha][-2]] = [] if isinstance(d[RUTAS[ficha][-2]], list) else {}
    _error(ficha, v, p)


def test_la_envoltura_rechaza_un_resultado_no_finito_y_traduce_excepciones():
    envuelta = V._cerrado("ACC-VAL-001")(lambda e, p: ({"x": float("nan"), "y": [1.0, float("inf")]}, []))
    with pytest.raises(ErrorFicha, match="no finito"):
        envuelta({"valores": {}}, {})
    for exc in (ZeroDivisionError("x"), OverflowError("x"), KeyError("x"), IndexError("x"), TypeError("x"),
                np.linalg.LinAlgError("x")):
        def revienta(e, p, exc=exc):
            raise exc
        with pytest.raises(ErrorFicha, match=type(exc).__name__):
            V._cerrado("DER-OPT-001")(revienta)({"valores": {}}, {})


def test_las_advertencias_van_en_el_resultado_y_no_como_limitaciones():
    for f in FICHAS:
        v, p = BASE[f]
        r, lim = _correr(f, v, p)
        assert set(V.ADVERTENCIAS[f]) <= set(r["advertencias"]) and not set(V.ADVERTENCIAS[f]) & set(lim)


# ============================================================================= FIR-PRICE-001
def _bono(**k):
    return V._bono_datos(**{"cupon": 4.0, "f": 2, "liq": "2026-11-13", "venc": "2034-05-15", "conv": "ACT/ACT-ICMA",
                            **k})


def test_fir_price_oraculo_anualidad_y_duracion_cerrada():
    """Bono anual en fecha de cupón: precio por la fórmula de la anualidad y D_mac por la fórmula cerrada."""
    c, y, n = 0.06, 0.045, 12
    v = V._bono_datos(c * 100, 1, "2026-06-01", f"{2026 + n}-06-01", "30E/360", rendimiento=y * 100)
    r, _ = _correr("FIR-PRICE-001", v)
    precio = 100 * c * (1 - (1 + y) ** -n) / y + 100 * (1 + y) ** -n
    d_mac = (1 + y) / y - (1 + y + n * (c - y)) / (c * ((1 + y) ** n - 1) + y)
    assert r["precio_limpio"] == pytest.approx(precio, rel=1e-12)
    assert r["d_macaulay"] == pytest.approx(d_mac, rel=1e-12)
    assert r["d_mod"] == pytest.approx(d_mac / (1 + y), rel=1e-12)
    assert r["dv01"] == pytest.approx(d_mac / (1 + y) * precio / 1e4, rel=1e-12)
    conv = sum(t * (t + 1) * 100 * (c + (t == n)) / (1 + y) ** (t + 2) for t in range(1, n + 1)) / precio
    assert r["convexidad"] == pytest.approx(conv, rel=1e-12)


def test_fir_price_oraculo_cupon_corrido_y_tir_fuera_de_fecha():
    """ACT/ACT ICMA y 30E/360 a mano; TIR con Brent sobre un precio escrito aquí."""
    liq, prev, sig = date(2026, 11, 13), date(2026, 5, 15), date(2026, 11, 15)
    v = _bono(precio_limpio=98.4)
    r, _ = _correr("FIR-PRICE-001", v)
    a = (liq - prev).days / (sig - prev).days
    assert r["cupon_corrido"] == pytest.approx(2.0 * a, rel=1e-14)
    sucio = 98.4 + 2.0 * a
    n = 16   # 15-11-2026 … 15-05-2034

    def precio(y):
        return sum((2.0 + 100 * (k == n - 1)) / (1 + y / 2) ** (1 - a + k) for k in range(n))
    ytm = optimize.brentq(lambda y: precio(y) - sucio, -0.5, 1, xtol=1e-15)
    assert r["ytm_pct"] == pytest.approx(ytm * 100, rel=1e-9)
    r30, _ = _correr("FIR-PRICE-001", _bono(precio_limpio=98.4, conv="30E/360"))
    assert r30["cupon_corrido"] == pytest.approx(2.0 * (360 * 0 + 30 * 6 + (13 - 15)) / 180, rel=1e-14)
    assert r["fecha_peor"] == "2034-05-15" and r["flujos"] == n


def test_fir_price_30e_360_con_dia_31_a_mano():
    """30E/360 (ICMA): el 31 cuenta como 30. Del 31-08 al 15-10: 30·2 + (15 − 30) = 45 días de 180."""
    v = V._bono_datos(5.0, 2, "2026-10-15", "2031-08-31", "30E/360", precio_limpio=101.0)
    r, _ = _correr("FIR-PRICE-001", v)
    assert r["cupon_corrido"] == pytest.approx(2.5 * 45 / 180, rel=1e-14)
    a = 45 / 180
    precio = sum((2.5 + 100 * (k == 9)) / (1 + r["ytm_pct"] / 200) ** (1 - a + k) for k in range(10))
    assert precio == pytest.approx(101.0 + 2.5 * a, rel=1e-10)


def test_fir_price_rescates_ytw_y_efectivas():
    v = _bono(cupon=6.0, precio_limpio=104.0, rescates=[{"fecha": "2028-05-15", "precio": 100.0},
                                                         {"fecha": "2030-05-15", "precio": 101.0}])
    r, lim = _correr("FIR-PRICE-001", v)
    assert r["ytw_pct"] < r["ytm_pct"] and r["fecha_peor"] == "2028-05-15"
    assert r["efectivas"]["duracion"] < r["d_mod"] and any("precio al peor" in x for x in lim)
    # con la TIR del peor escenario se reproduce el precio (bono truncado escrito aquí)
    a = (date(2026, 11, 13) - date(2026, 5, 15)).days / (date(2026, 11, 15) - date(2026, 5, 15)).days
    precio = sum((3.0 + 100 * (k == 3)) / (1 + r["ytw_pct"] / 200) ** (1 - a + k) for k in range(4))
    assert precio == pytest.approx(104.0 + 3.0 * a, rel=1e-10)


def test_fir_price_ligado_inflacion_y_breakeven():
    v = _bono(cupon=0.5, rendimiento=0.8, ligado_inflacion=True,
              rendimiento_nominal_comparable={"valor": 3.1, "fuente": "bono nominal sintético"})
    r, _ = _correr("FIR-PRICE-001", v)
    assert r["duracion_real"] == r["d_mod"] and r["breakeven_pb"] == pytest.approx(230.0, rel=1e-12)
    r2, lim = _correr("FIR-PRICE-001", _bono(cupon=0.5, rendimiento=0.8, ligado_inflacion=True))
    assert r2["breakeven_pb"] is None and any("breakeven" in x for x in lim)
    _error("FIR-PRICE-001", _bono(rendimiento=3, rendimiento_nominal_comparable={"valor": 3.1, "fuente": "x"}), {},
           "ligado a inflación")


@pytest.mark.parametrize("cambio,motivo", [
    ({"convencion": None}, "falta la convención"), ({"estructura": "flotante"}, "no modelables"),
    ({"frecuencia": 3}, "no modelable"), ({"rendimiento": 4.0}, "uno de los dos"), ({"precio_limpio": None}, "uno de los dos"),
    ({"vencimiento": "2026-11-13"}, "posterior"), ({"cupon": -1}, "mínimo"), ({"precio_limpio": 0}, "mínimo"),
    ({"rescates": [{"fecha": "2028-01-01", "precio": 100}]}, "fecha de cupón"), ({"liquidacion": 20261113}, "fecha"),
])
def test_fir_price_rechazos(cambio, motivo):
    v = {**_bono(precio_limpio=98.0), **cambio}
    v = {k: x for k, x in v.items() if x is not None}
    _error("FIR-PRICE-001", v, {}, motivo)


def test_fir_price_convencion_en_parametros_y_conflicto():
    v = {k: x for k, x in _bono(precio_limpio=98.0).items() if k != "convencion"}
    r, _ = _correr("FIR-PRICE-001", v, {"convencion": "30E/360"})
    assert r["convencion"] == "30E/360"
    _error("FIR-PRICE-001", _bono(precio_limpio=98.0), {"convencion": "30E/360"}, "distintas")
    con_rescates = {k: x for k, x in _bono(rendimiento=4.0, rescates=[{"fecha": "2030-05-15", "precio": 100}]).items()}
    _error("FIR-PRICE-001", con_rescates, {}, "precio limpio")


# ============================================================================= FIR-CURVE-001
def _nss_a_mano(t, b, lam):
    def l1(x):
        return 1.0 if x == 0 else (1 - math.exp(-x)) / x
    y = b[0] + b[1] * l1(t / lam[0]) + b[2] * (l1(t / lam[0]) - math.exp(-t / lam[0]))
    if len(lam) > 1:
        y += b[3] * (l1(t / lam[1]) - math.exp(-t / lam[1]))
    return y


def test_fir_curve_oraculo_curva_rmse_y_forward_a_mano():
    pl = V._PLAZOS_NSS
    y = [_nss_a_mano(t, [4.2, -1.7, 1.1, -0.6], [1.2, 7.0]) + 0.01 * math.sin(3 * i) for i, t in enumerate(pl)]
    r, _ = _correr("FIR-CURVE-001", {"curva": {"fecha": "2026-11-13", "plazos": pl, "rendimientos": y}})
    b = [r["parametros"][f"beta{i}"] for i in range(4)]
    lam = [r["parametros"]["lambda1"], r["parametros"]["lambda2"]]
    ajuste = [_nss_a_mano(t, b, lam) for t in pl]
    assert r["curva"]["cero_pct"] == pytest.approx(ajuste, abs=1e-12)
    rmse = math.sqrt(sum((a - o) ** 2 for a, o in zip(ajuste, y)) / len(y)) * 100
    assert r["rmse_pb"] == pytest.approx(rmse, rel=1e-10)
    assert r["residuos_pb"]["10"] == pytest.approx((y[7] - ajuste[7]) * 100, abs=1e-10)
    h = 1e-6   # forward instantáneo = d(τ·y)/dτ
    fwd = [((t + h) * _nss_a_mano(t + h, b, lam) - (t - h) * _nss_a_mano(t - h, b, lam)) / (2 * h) for t in pl]
    assert r["curva"]["forward_pct"] == pytest.approx(fwd, abs=1e-6)
    assert r["pendientes_pb"]["2s10s"] == pytest.approx((_nss_a_mano(10, b, lam) - _nss_a_mano(2, b, lam)) * 100, abs=1e-10)
    # QA r01 de T-112, H-08 (QV05): la 3m10y es y(10 años) − y(3 meses), no y(10) − y(6 meses)
    assert r["pendientes_pb"]["3m10y"] == pytest.approx((_nss_a_mano(10, b, lam) - _nss_a_mano(0.25, b, lam)) * 100, abs=1e-10)
    assert abs(r["pendientes_pb"]["3m10y"] - (_nss_a_mano(10, b, lam) - _nss_a_mano(0.5, b, lam)) * 100) > 1
    # el ajuste es un mínimo: desde la solución, curve_fit no encuentra un coste menor
    pf, _ = optimize.curve_fit(lambda t, *x: [_nss_a_mano(s, x[:4], x[4:]) for s in t], pl, y, p0=b + lam, maxfev=20000)
    coste = sum((_nss_a_mano(t, pf[:4], pf[4:]) - o) ** 2 for t, o in zip(pl, y))
    assert sum((a - o) ** 2 for a, o in zip(ajuste, y)) <= coste * (1 + 1e-6) + 1e-18


def test_fir_curve_diebold_li_por_mco_a_mano():
    lam = 1 / (0.0609 * 12)
    pl = [0.25, 0.5, 1, 2, 3, 5, 7, 10]
    y = [3.0 + 0.2 * t ** 0.5 - 0.01 * t for t in pl]
    r, _ = _correr("FIR-CURVE-001", {"curva": {"fecha": "2026-11-13", "plazos": pl, "rendimientos": y}},
                   {"modelo": "NS", "lambda": "diebold_li"})
    X = np.array([[1, (1 - math.exp(-t / lam)) / (t / lam), (1 - math.exp(-t / lam)) / (t / lam) - math.exp(-t / lam)]
                  for t in pl])
    b = np.linalg.lstsq(X, np.array(y), rcond=None)[0]
    assert [r["parametros"][f"beta{i}"] for i in range(3)] == pytest.approx(list(b), rel=1e-10)
    assert r["parametros"]["lambda1"] == pytest.approx(lam, rel=1e-14) and r["arranques"] == 0


def test_fir_curve_historia_z_y_percentiles():
    pl = [0.25, 0.5, 1, 2, 3, 5, 7, 10]
    lam = 1 / (0.0609 * 12)
    fechas = [(date(2025, 1, 3) + pd.Timedelta(weeks=i)).isoformat() for i in range(30)]
    filas = [[3 + 0.1 * math.sin(i) + (0.3 + 0.05 * math.cos(i)) * math.log1p(t) + 0.002 * math.sin(i * t) for t in pl]
             for i in range(30)]
    act = [3 + 0.6 * math.log1p(t) + 0.002 * math.sin(t) for t in pl]
    r, _ = _correr("FIR-CURVE-001", {"curva": {"fecha": "2026-11-13", "plazos": pl, "rendimientos": act},
                                     "historia": {"fechas": fechas, "rendimientos": filas}},
                   {"modelo": "NS", "lambda": "diebold_li"})
    # a mano: residuos históricos por MCO y z del residuo a 10 años; percentil de la pendiente 2s10s
    X = np.array([[1, (1 - math.exp(-t / lam)) / (t / lam), (1 - math.exp(-t / lam)) / (t / lam) - math.exp(-t / lam)]
                  for t in pl])
    res_h = [(np.array(f) - X @ np.linalg.lstsq(X, np.array(f), rcond=None)[0])[-1] * 100 for f in filas]
    actual = r["residuos_pb"]["10"]
    assert r["z_residuos"]["10"] == pytest.approx((actual - np.mean(res_h)) / np.std(res_h, ddof=1), rel=1e-8)
    pend = []
    for f in filas:
        b = np.linalg.lstsq(X, np.array(f), rcond=None)[0]
        pend.append((_nss_a_mano(10, b, [lam]) - _nss_a_mano(2, b, [lam])) * 100)
    assert r["percentiles_pendientes"]["2s10s"]["percentil"] == pytest.approx(np.mean(np.array(pend) <= r["pendientes_pb"]["2s10s"]))
    assert r["pendientes_pb"]["3m10y"] is not None and r["n_historia"] == 30


@pytest.mark.parametrize("valores,params,motivo", [
    ({"plazos": [1, 2, 3, 5, 10], "rendimientos": [1, 2, 3, 4, 5]}, {}, "< 6"),
    ({"plazos": [1, 2, 3, 5, 7, 10, 20], "rendimientos": [1, 2, 3, 4, 5, 5, 5]}, {"modelo": "NSS"}, "Svensson"),
    ({"plazos": [1, 2, 3, 5, 7, 10, 20, 30], "rendimientos": [1, 2, 3, 4, 5, 5, 5, 5]}, {"lambda": "diebold_li"}, "Diebold"),
    ({"plazos": [0, 2, 3, 5, 7, 10], "rendimientos": [1, 2, 3, 4, 5, 5]}, {}, "positivos"),
    ({"plazos": [1, 2, 2, 5, 7, 10], "rendimientos": [1, 2, 3, 4, 5, 5]}, {}, "crecientes"),
    ({"plazos": [1, 2, 3, 5, 7, 10], "rendimientos": [1, 2, 3, 4, 5]}, {}, "longitud"),
    ({"plazos": [1, 2, 3, 5, 7, 10], "rendimientos": [-1, -2, -3, -4, -5, -6]}, {"modelo": "NS", "lambda": "diebold_li"},
     "β₀ > 0"),
])
def test_fir_curve_rechazos(valores, params, motivo):
    _error("FIR-CURVE-001", {"curva": {"fecha": "2026-11-13", **valores}}, params, motivo)


def test_fir_curve_coherente_con_tcv_slope():
    """TCV-SLOPE-001 toma −β₁ de NSS como pendiente: y(∞) − y(0) = −β₁ con las unidades de FIR-CURVE (% → pb)."""
    r, _ = _correr("FIR-CURVE-001", *_caso("FIR-CURVE-001", 0))
    pend = (r["verificacion"]["y_tau_infinito"] - r["verificacion"]["y_tau_0"]) * fichas_tcv.PB_POR_PUNTO
    assert pend == pytest.approx(-r["parametros"]["beta1"] * fichas_tcv.PB_POR_PUNTO, rel=1e-12)
    v = {**fichas_tcv.sintetico_slope(lambda t, i: 2.0 + 0.1 * t + 0.002 * i),
         "beta1_nss": {"valor": r["parametros"]["beta1"], "fuente": "FIR-CURVE-001"}}
    rt, _ = fichas_tcv.FICHAS["TCV-SLOPE-001"]["fn"]({"valores": v, "series": {}, "series_rol": {}}, {})
    assert rt["segunda_via"]["pendiente_nss_pb"] == pytest.approx(pend, rel=1e-12)


# ============================================================================= FIR-CARRY-001
def test_fir_carry_coherente_con_tcv_carry_tramo():
    plazos, curva = np.array([0.25, 1, 2, 5, 10, 30]), np.array([1.0, 1.5, 2.0, 3.0, 4.0, 4.5])
    for tau, meses, fin in ((2, 3, 1.2), (10, 6, 0.5), (5, 12, 2.0)):
        r, _ = _correr("FIR-CARRY-001", {"curva": {"plazos": list(plazos), "rendimientos": list(curva)}, "tramo": tau,
                                         "financiacion": fin}, {"delta_t": meses})
        t = fichas_tcv._carry_tramo(plazos, curva, tau, meses / 12, fin / 100, [])
        fila = r["tramos"][f"{tau:g}"]
        assert fila["carry_pb"] == pytest.approx(t["carry"] * 1e4, rel=1e-14)
        assert fila["rolldown_pb"] == pytest.approx(t["rolldown"] * 1e4, rel=1e-14)
        assert fila["d_mod"] == pytest.approx(t["d_mod"], rel=1e-14)
    assert V.UMBRALES["FIR-CARRY-001"]["rango_delta_t"] == fichas_tcv.UMBRALES["TCV-SLOPE-001"]["rango_horizonte_carry"]
    assert V.PARAMETROS_POR_DEFECTO["FIR-CARRY-001"]["delta_t"] == fichas_tcv.PARAMETROS_POR_DEFECTO["TCV-SLOPE-001"]["horizonte_carry"]


def test_fir_carry_oraculo_a_mano_con_nss_y_volatilidad():
    b, lam = [4.0, -2.0, 1.5, -1.0], [1.5, 8.0]
    v = {"nss": {"beta0": 4.0, "beta1": -2.0, "beta2": 1.5, "beta3": -1.0, "lambda1": 1.5, "lambda2": 8.0,
                 "fuente": "FIR-CURVE-001 sintética"}, "tramo": [3, 7], "financiacion": 2.5, "volatilidad_rendimiento_pb": 90}
    r, lim = _correr("FIR-CARRY-001", v, {"delta_t": 3})
    for tau in (3, 7):
        y, yr = _nss_a_mano(tau, b, lam) / 100, _nss_a_mano(tau - 0.25, b, lam) / 100
        d = tau / (1 + y)
        carry, roll = (y - 0.025) * 0.25, -d * (yr - y)
        f = r["tramos"][str(tau)]
        assert f["total_pb"] == pytest.approx((carry + roll) * 1e4, rel=1e-12)
        assert f["carry_volatilidad"] == pytest.approx((carry + roll) / (d * 0.009 * 0.5), rel=1e-12)
        exacto = (1 + yr) ** -(tau - 0.25) / (1 + y) ** -tau - 1 - 0.025 * 0.25
        assert f["segunda_via"]["rentabilidad_exceso_pb"] == pytest.approx(exacto * 1e4, rel=1e-12)
        assert abs(f["segunda_via"]["diferencia_pb"]) < abs(f["total_pb"])
    assert r["curva"] == "FIR-CURVE-001" and not any("volatilidad" in x for x in lim)


@pytest.mark.parametrize("cambio,motivo", [
    ({"financiacion": None}, "aclaración"), ({"tramo": 40}, "no se extrapola"), ({"tramo": 0.2}, "vence antes"),
    ({"tramo": -1}, "mínimo"), ({"curva": None}, "falta «curva»"), ({"nss": {"beta0": 1, "lambda1": 1, "fuente": "x"}}, "NS ="),
    ({"nss": {"beta0": 1, "beta1": 1, "beta2": 1, "lambda1": 1}}, "fuente"), ({"tramo": []}, "elementos"),
])
def test_fir_carry_rechazos(cambio, motivo):
    v = {"curva": {"plazos": [0.25, 1, 2, 5, 10], "rendimientos": [1, 2, 2.5, 3, 3.5]}, "tramo": 5, "financiacion": 1.0}
    v = {k: x for k, x in {**v, **cambio}.items() if x is not None}
    _error("FIR-CARRY-001", v, {}, motivo)


# ============================================================================= FIR-SPREAD-001
def test_fir_spread_oraculo_percentil_z_y_ventana():
    v = V.sintetico_spread(n=16 * 52, actual=135.0)
    r, lim = _correr("FIR-SPREAD-001", v, {"ventana": 12})
    s = pd.Series(v["historia"]["diferenciales_pb"], index=pd.to_datetime(v["historia"]["fechas"]))
    w = s[(s.index[-1] - s.index).days <= 12 * 365]
    assert r["n"] == len(w) and r["percentil"] == pytest.approx((w <= 135.0).mean())
    assert r["z"] == pytest.approx((135.0 - w.mean()) / w.std(ddof=1), rel=1e-10)
    assert r["perdida_esperada_pb"] == pytest.approx((0.7 * 0.002 + 0.3 * 0.01) * 0.6 * 1e4, rel=1e-12)
    assert r["referencias_ingenuas"]["RI_MH_pb"] == pytest.approx(w.mean(), rel=1e-12)
    assert any("15 recomendados" in x for x in lim)


def test_fir_spread_ajuste_de_composicion_a_mano():
    v = V.sintetico_spread(actual=150.0)
    r, lim = _correr("FIR-SPREAD-001", v, {"ajuste_composicion": True})
    s, d = np.array(v["historia"]["diferenciales_pb"]), np.array(v["historia"]["duraciones"])
    adj = s * d[-1] / d
    assert r["ajuste_composicion"]["percentil"] == pytest.approx(np.mean(adj <= 150.0))
    assert any("duración" in x for x in lim)


def test_fir_spread_limitaciones_y_rechazos():
    r, lim = _correr("FIR-SPREAD-001", V.sintetico_spread(n=7 * 52))
    assert any("< 10" in x for x in lim)
    _error("FIR-SPREAD-001", V.sintetico_spread(n=4 * 52), {}, "rechazo")
    v = V.sintetico_spread()
    del v["impagos"]
    _error("FIR-SPREAD-001", v, {}, "impagos")
    v = V.sintetico_spread()
    v["impagos"]["por_rating"]["BB"]["peso"] = 0.5
    _error("FIR-SPREAD-001", v, {}, "sumar 1")
    v = V.sintetico_spread()
    v["medida"] = "spread de swap"
    _error("FIR-SPREAD-001", v, {}, "no admitido")
    v = {**V.sintetico_spread(), "incluye_recesion": False, "duracion_diferencial": None}
    del v["medida"]
    r, lim = _correr("FIR-SPREAD-001", {k: x for k, x in v.items() if x is not None})
    assert r["ampliacion_equilibrio_pb"] is None and any("recesión" in x for x in lim) and any("medida" in x for x in lim)


# ============================================================================= FX-MOM-001
def test_fx_mom_oraculo_con_pandas_y_series_de_ht01():
    d = V.sintetico_fx(dif=1.5)
    d["diferencial_pct"] = {"fechas": [d["spot"]["fechas"][0], d["spot"]["fechas"][300]], "valores": [1.5, -0.5]}
    s = pd.Series(d["spot"]["valores"], index=pd.to_datetime(d["spot"]["fechas"]))
    sin_spot = {k: x for k, x in d.items() if k != "spot"}
    r, lim = _correr("FX-MOM-001", {"pares": {"EURUSD": sin_spot}}, {}, series={"EURUSD": s})
    dif = pd.Series([1.5, -0.5], index=pd.to_datetime([d["spot"]["fechas"][0], d["spot"]["fechas"][300]]))
    dif = dif.reindex(s.index, method="ffill")
    for h in (1, 3, 12):
        t0 = s.index[s.index <= s.index[-1] - pd.DateOffset(months=h)][-1]
        tramo = s.index[(s.index >= t0)]
        carry = sum(dif[a] / 100 * (b - a).days / 365 for a, b in pairwise(tramo))
        x = r["pares"]["EURUSD"]["rendimientos_exceso"][str(h)]
        assert x["exceso_pct"] == pytest.approx((s.iloc[-1] / s[t0] - 1 + carry) * 100, rel=1e-12)
    rv = np.log(s).diff()[s.index > s.index[-1] - pd.DateOffset(months=3)]
    assert r["pares"]["EURUSD"]["volatilidad_pct"] == pytest.approx(rv.std(ddof=1) * math.sqrt(252) * 100, rel=1e-12)
    assert r["pares"]["EURUSD"]["carry_volatilidad"] == pytest.approx(-0.5 / r["pares"]["EURUSD"]["volatilidad_pct"])
    assert any("realizada" in x for x in lim) and r["rangos_transversales"]["12"] is None


def test_fx_mom_implicita_forward_y_rango():
    d = V.sintetico_fx()
    fechas, spot = d["spot"]["fechas"], d["spot"]["valores"]
    fwd = {"fechas": fechas, "valores": [x * (1 - 0.01 * 90 / 365) for x in spot], "plazo_dias": 90}
    e = {"direccion": "GBP/USD", "spot": d["spot"], "forward": fwd, "vol_implicita_3m": {"valor": 8.0, "fuente": "sintética"}}
    r, _ = _correr("FX-MOM-001", {"pares": {"GBPUSD": e, "EURUSD": d}, "universo": "G10"})
    g = r["pares"]["GBPUSD"]
    assert g["diferencial_actual_pct"] == pytest.approx((1 / (1 - 0.01 * 90 / 365) - 1) / (90 / 365) * 100, rel=1e-12)
    assert g["volatilidad_pct"] == 8.0 and g["carry_volatilidad"] == pytest.approx(g["diferencial_actual_pct"] / 8.0)
    x = [r["pares"][k]["rendimientos_exceso"]["3"]["exceso_pct"] for k in ("GBPUSD", "EURUSD")]
    assert r["rangos_transversales"]["3"]["GBPUSD"]["percentil"] == (1.0 if x[0] >= x[1] else 0.5)
    assert r["universo"] == "G10"


@pytest.mark.parametrize("cambio,motivo", [
    ({"direccion": None}, "dirección"), ({"direccion": "EURUSD"}, "dirección"), ({"direccion": "EUR/EUR"}, "dirección"),
    ({"diferencial_pct": None}, "diferenciales"), ({"spot": None}, "spot"),
])
def test_fx_mom_rechazos(cambio, motivo):
    d = {k: x for k, x in {**V.sintetico_fx(), **cambio}.items() if x is not None}
    _error("FX-MOM-001", {"pares": {"EURUSD": d}}, {}, motivo)


def test_fx_mom_menos_de_dos_anios():
    _error("FX-MOM-001", {"pares": {"EURUSD": V.sintetico_fx(n_dias=400)}}, {}, "2 años")
    _error("FX-MOM-001", {"pares": {}}, {}, "vacío")


# ============================================================================= FX-PPA-001
def test_fx_ppa_oraculo_desviacion_y_vida_media():
    v = V.sintetico_ppa(25 * 12, 0.0015, 0.0025, ruido=True)
    r, _ = _correr("FX-PPA-001", v)
    S, pb, pc = (np.array(x) for x in (v["tipo_cambio"], v["indices"]["base"]["valores"], v["indices"]["cotizada"]["valores"]))
    senda = S[0] * (pc / pc[0]) / (pb / pb[0])
    dev = np.log(S / senda) * 100
    assert [x["desviacion_pct"] for x in r["serie_desviacion_pct"]] == pytest.approx(list(dev), abs=1e-10)
    q = np.log(S) + np.log(pb) - np.log(pc)
    phi = np.polyfit(q[:-1], q[1:], 1)[0]
    assert r["phi_ar1"] == pytest.approx(phi, rel=1e-9)
    assert r["vida_media_anios"] == pytest.approx(math.log(0.5) / math.log(phi) / 12, rel=1e-8)
    assert r["senda_ppa_final"] == pytest.approx(senda[-1], rel=1e-12)
    rm, _ = _correr("FX-PPA-001", v, {"base": "media_largo_plazo", "suavizado": 12})
    assert rm["desviacion_final_pct"] == pytest.approx((q[-1] - q.mean()) * 100, abs=1e-10)
    assert rm["serie_suavizada"][-1]["desviacion_pct"] == pytest.approx(np.mean((q - q.mean())[-12:]) * 100, abs=1e-10)


def test_fx_ppa_ventana_trimestral_y_limitaciones():
    v = V.sintetico_ppa(60, 0.001, 0.002)
    r, lim = _correr("FX-PPA-001", v, {"ventana": 36})
    assert len(r["serie_desviacion_pct"]) == 37 and r["vida_media_anios"] is None and any("vida media" in x for x in lim)
    t = V.sintetico_ppa(12, 0.003, 0.006)
    t["fechas"] = [d.date().isoformat() for d in pd.date_range("2001-03-31", periods=12, freq="QE")]
    for k in ("base", "cotizada"):
        t["indices"][k]["periodicidad"] = "trimestral"
    r, _ = _correr("FX-PPA-001", t)
    assert r["desviacion_final_pct"] == pytest.approx(0.0, abs=1e-10)


@pytest.mark.parametrize("mod,motivo", [
    (lambda v: v["indices"]["base"].update(canasta="IPC subyacente"), "canastas"),
    (lambda v: v["indices"]["base"].update(periodicidad="trimestral"), "periodicidades"),
    (lambda v: v["indices"]["cotizada"].pop("vintage"), "vintage"),
    (lambda v: v["indices"]["cotizada"].pop("base_indice"), "base_indice"),
    (lambda v: v["fechas"].__setitem__(5, "2001-07-15"), "periodicidad|crecientes"),
    (lambda v: v.update(par="EURUSD"), "par"), (lambda v: v["tipo_cambio"].__setitem__(3, -1.0), "positivos"),
    (lambda v: v["tipo_cambio"].pop(), "longitud"),
])
def test_fx_ppa_rechazos(mod, motivo):
    v = V.sintetico_ppa(36, 0.001, 0.002)
    mod(v)
    _error("FX-PPA-001", v, {}, motivo)


def test_fx_ppa_menos_de_24_meses():
    _error("FX-PPA-001", V.sintetico_ppa(24, 0.001, 0.002), {}, "< 24")
    _correr("FX-PPA-001", V.sintetico_ppa(25, 0.001, 0.002))


# ============================================================================= ACC-ERP-001
def test_acc_erp_oraculo_brent_aparte():
    v = {**V._ERP, "g5": {"valor": 7.0, "fuente": "consenso", "fecha": "2026-11-01"}}
    r, _ = _correr("ACC-ERP-001", v, {"g_L": 3.2})
    cf = 125.0

    def valor(rr):
        flujos = [cf * 1.07 ** k for k in range(1, 6)]
        return sum(f / (1 + rr) ** k for k, f in enumerate(flujos, 1)) + flujos[-1] * 1.032 / (rr - 0.032) / (1 + rr) ** 5
    rr = optimize.brentq(lambda x: valor(x) - 5000, 0.0321, 1.0, xtol=1e-14)
    assert r["r_implicita_pct"] == pytest.approx(rr * 100, rel=1e-9)
    assert r["prm_pp"] == pytest.approx(rr * 100 - 4.0, rel=1e-8)
    r2, _ = _correr("ACC-ERP-001", v, {"incluir_recompras": False})
    assert r2["flujo_accionista_12m"] == 75.0 and r2["r_implicita_pct"] < r["r_implicita_pct"] + 1


def test_acc_erp_cape_desde_beneficios_reales_y_percentiles():
    v = {k: x for k, x in V._ERP.items() if k != "cape"}
    v["beneficios_reales_10a"] = [150.0 + 5 * i for i in range(12)]
    fechas = [d.date().isoformat() for d in pd.date_range("2004-01-31", periods=22 * 12, freq="ME")]
    hist = {"fechas": fechas, **{k: [3 + math.sin(i / 7) for i in range(len(fechas))] for k in ("prm_pp", "simple_pp", "ecy_pp")}}
    r, lim = _correr("ACC-ERP-001", {**v, "historia": hist})
    cape = 5000 / np.mean(v["beneficios_reales_10a"][-10:])
    assert r["cape"] == pytest.approx(cape, rel=1e-14) and r["ecy_pp"] == pytest.approx(100 / cape - 1.8, rel=1e-12)
    h = pd.Series(hist["prm_pp"], index=pd.to_datetime(fechas))
    w = h[(h.index[-1] - h.index).days <= 20 * 365]
    assert r["percentiles"]["prm_pp"]["percentil"] == pytest.approx((w <= r["prm_pp"]).mean())
    r, lim = _correr("ACC-ERP-001", {**v, "historia": {**hist, "fechas": fechas[-60:],
                                                         **{k: hist[k][-60:] for k in ("prm_pp", "simple_pp", "ecy_pp")}}})
    assert r["percentiles"]["prm_pp"] is None and any("< 10" in x for x in lim)


@pytest.mark.parametrize("cambio,motivo", [
    ({"rf_nominal_10a": {"valor": 3.0, "moneda": "EUR", "fuente": "x"}}, "moneda del índice"),
    ({"rf_real_10a": None}, "moneda del índice"), ({"nivel": None}, "nivel"), ({"g5": None}, "g5"),
    ({"g5": {"valor": 5, "fuente": "x"}}, "fecha"), ({"beneficio_adelantado": None}, "beneficio_adelantado"),
    ({"cape": None}, "CAPE"), ({"cape": None, "beneficios_reales_10a": [1.0] * 9}, "< 10"),
    ({"dividendos_12m": 0.0, "recompras_netas_12m": -1.0}, "≤ 0"), ({"g5": {"valor": 5, "fecha": "2026-01-01"}}, "fuente"),
])
def test_acc_erp_rechazos(cambio, motivo):
    v = {k: x for k, x in {**V._ERP, **cambio}.items() if x is not None}
    _error("ACC-ERP-001", v, {}, motivo)


# ============================================================================= ACC-FACT-001
def _nw_a_mano(y, X):
    n, k = X.shape
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    L = int(4 * (n / 100) ** (2 / 9))
    S = np.zeros((k, k))
    for t in range(n):
        S += e[t] ** 2 * np.outer(X[t], X[t])
    for lag in range(1, L + 1):
        w = 1 - lag / (L + 1)
        for t in range(lag, n):
            G = e[t] * e[t - lag] * np.outer(X[t], X[t - lag])
            S += w * (G + G.T)
    inv = np.linalg.inv(X.T @ X)
    return b, np.sqrt(np.diag(inv @ S @ inv)), L


@pytest.mark.parametrize("n", [36, 60, 72, 100, 250, 300, 1000, 5000])
def test_acc_fact_regla_de_rezagos_de_newey_west(n):
    assert V.rezagos_newey_west(n) == math.floor(4 * (n / 100) ** (2 / 9))


def test_acc_fact_oraculo_newey_west_a_mano():
    v = V.sintetico_factores(n=72)
    r, _ = _correr("ACC-FACT-001", v, {"modelo": "FF3", "adicionales": ["QMJ"]})
    nombres = ["MKT", "SMB", "HML", "QMJ"]
    X = np.column_stack([np.ones(72)] + [np.array(v["factores"][k]) for k in nombres])
    b, ee, L = _nw_a_mano(np.array(v["rendimientos"]), X)
    assert r["rezagos_nw"] == L == 3
    assert r["alfa_periodo_pct"] == pytest.approx(b[0], rel=1e-10)
    for j, k in enumerate(nombres, 1):
        assert r["betas"][k]["beta"] == pytest.approx(b[j], rel=1e-10)
        assert r["betas"][k]["t"] == pytest.approx(b[j] / ee[j], rel=1e-9)
    assert r["alfa_anual_pct"] == pytest.approx(((1 + b[0] / 100) ** 12 - 1) * 100, rel=1e-12)
    resid = np.array(v["rendimientos"]) - X @ b
    assert r["r2"] == pytest.approx(1 - resid.var() / np.var(v["rendimientos"]), rel=1e-12)
    W = 36
    bm = np.linalg.lstsq(X[-W:], np.array(v["rendimientos"])[-W:], rcond=None)[0]
    assert r["betas_moviles"][-1]["betas"]["SMB"] == pytest.approx(bm[2], rel=1e-10)
    assert len(r["betas_moviles"]) == 72 - W + 1
    assert r["referencia_ingenua"]["alfa_periodo_pct"] == pytest.approx(
        np.mean(np.array(v["rendimientos"]) - np.array(v["factores"]["MKT"])), rel=1e-12)


def test_acc_fact_semanal_y_rf():
    v = V.sintetico_factores(n=110)
    v["fechas"] = [(date(2023, 1, 6) + pd.Timedelta(weeks=i)).isoformat() for i in range(110)]
    rf = [0.05] * 110
    v2 = {**{k: x for k, x in v.items() if k != "en_exceso"}, "rf": rf,
          "rendimientos": [x + 0.05 for x in v["rendimientos"]]}
    r1, _ = _correr("ACC-FACT-001", v, {"frecuencia": "semanal", "modelo": "CAPM"})
    r2, lim = _correr("ACC-FACT-001", v2, {"frecuencia": "semanal", "modelo": "CAPM"})
    assert r1["betas"]["MKT"]["beta"] == pytest.approx(r2["betas"]["MKT"]["beta"], rel=1e-12)
    assert r1["betas"]["MKT"]["t"] == pytest.approx(r2["betas"]["MKT"]["t"], rel=1e-12) and r1["ventana_movil_obs"] == 156
    assert any("ventana móvil" in x for x in lim)


@pytest.mark.parametrize("cambio,params,motivo", [
    ({"n": 35}, {}, "< 36"), ({"n": 100, "semanal": True}, {"frecuencia": "semanal"}, "< 104"),
    ({"sin": "SMB"}, {}, "SMB"), ({"en_exceso": None}, {}, "rf"), ({"region": None}, {}, "región"),
    ({"hueco": True}, {}, "consecutivas"),
])
def test_acc_fact_rechazos(cambio, params, motivo):
    v = V.sintetico_factores(n=cambio.get("n", 60))
    if cambio.get("semanal"):
        v["fechas"] = [(date(2023, 1, 6) + pd.Timedelta(weeks=i)).isoformat() for i in range(cambio["n"])]
    if "sin" in cambio:
        del v["factores"][cambio["sin"]]
    for k in ("en_exceso", "region"):
        if k in cambio:
            del v[k]
    if cambio.get("hueco"):
        v["fechas"][10] = "2020-12-15"   # de octubre a diciembre: falta noviembre
    _error("ACC-FACT-001", v, params, motivo)


# ============================================================================= ACC-VAL-001
def test_acc_val_oraculo_dcf_a_mano_y_multiplos():
    v = V.sintetico_val(crecimiento=4.0, roic_nuevo_pct=12.0, historia_multiplos={
        "ev_ebitda": {"fechas": [f"{2010 + i}-12-31" for i in range(15)], "valores": [8.0 + 0.2 * i for i in range(15)]}},
        multiplos_mercado={"per_adelantado": 15.0})
    r, lim = _correr("ACC-VAL-001", v, {"anios_explicitos": 7})
    t, ke = 0.25, 3 + 1.1 * 5.5
    wacc = (1500 * ke + 300 * 4 * (1 - t)) / 1800 / 100
    nopat = 160 * (1 - t)
    fcff = nopat + 40 - 50 - 10
    g, n = 0.03, 7
    vp = sum(fcff * 1.04 ** k / (1 + wacc) ** k for k in range(1, n + 1))
    vt = nopat * 1.04 ** n * (1 + g) * (1 - g / 0.12) / (wacc - g)
    ev = vp + vt / (1 + wacc) ** n
    assert r["wacc_pct"] == pytest.approx(wacc * 100, rel=1e-12) and r["ev"] == pytest.approx(ev, rel=1e-12)
    assert r["valor_agregado"] == pytest.approx(ev - 300, rel=1e-12)
    assert r["peso_valor_terminal_pct"] == pytest.approx(vt / (1 + wacc) ** n / ev * 100, rel=1e-12)
    assert r["multiplos"]["ev_ebitda"] == pytest.approx(1800 / 200, rel=1e-14)
    assert r["percentiles_multiplos"]["ev_ebitda"]["percentil"] == pytest.approx(np.mean(np.array(
        v["historia_multiplos"]["ev_ebitda"]["valores"]) <= 9.0))
    assert r["multiplos_frente_mercado"]["per_adelantado"] == pytest.approx(1500 / 110 / 15 - 1, rel=1e-12)
    assert any("margen implícito" in x for x in lim)


def test_acc_val_multiplos_del_agregado_son_la_media_armonica_ponderada():
    """Totales del agregado = media armónica de los PER de los componentes ponderada por capitalización."""
    cap, ben = np.array([600.0, 500.0, 400.0]), np.array([50.0, 40.0, 20.0])
    w = cap / cap.sum()
    armonica = 1 / np.sum(w / (cap / ben))
    v = V.sintetico_val(beneficio_adelantado=float(ben.sum()))
    r, _ = _correr("ACC-VAL-001", v)
    assert r["multiplos"]["per_adelantado"] == pytest.approx(armonica, rel=1e-12)


def test_acc_val_fcfe_margen_implicito_y_sensibilidad():
    r, _ = _correr("ACC-VAL-001", V.sintetico_val(), {"enfoque": "FCFE"})
    ke = (3 + 1.1 * 5.5) / 100
    f0 = 78.0
    val = sum(f0 * 1.03 ** k / (1 + ke) ** k for k in range(1, 6)) + f0 * 1.03 ** 5 * 1.03 / (ke - 0.03) / (1 + ke) ** 5
    assert r["valor_agregado"] == pytest.approx(val, rel=1e-12) and r["ev"] == pytest.approx(val + 300, rel=1e-12)
    rf, _ = _correr("ACC-VAL-001", V.sintetico_val())
    m = rf["dcf_inverso"]["margen_flujo"]
    rm, _ = _correr("ACC-VAL-001", V.sintetico_val())
    assert m["implicito_pct"] == pytest.approx(m["actual_pct"] * rf["ev_mercado"] / rf["ev"], rel=1e-12)
    s = rm["sensibilidad"]["valor_agregado"]
    assert s[0][2] > s[1][1] > s[2][0] and len(s) == 3 and all(len(f) == 3 for f in s)


def test_acc_val_matriz_de_sensibilidad_a_mano():
    """QA r01 de T-112, H-08 (QV06): las nueve celdas WACC ±1 pp × g ±0,5 pp («Método (v)»), con un DCF escrito aquí."""
    r, lim = _correr("ACC-VAL-001", V.sintetico_val())
    t, ke = 0.25, 3 + 1.1 * 5.5
    wacc = (1500 * ke + 300 * 4 * (1 - t)) / 1800
    fcff = 160 * (1 - t) + 40 - 50 - 10

    def valor(w_pct, g_pct):
        w, g = w_pct / 100, g_pct / 100
        flujos = [fcff * 1.03 ** k for k in range(1, 6)]
        ev = sum(f / (1 + w) ** k for k, f in enumerate(flujos, 1)) + flujos[-1] * (1 + g) / (w - g) / (1 + w) ** 5
        return ev - 300
    s = r["sensibilidad"]
    assert s["filas_tasa_pp"] == [-1, 0, 1] and s["columnas_g_pp"] == [-0.5, 0, 0.5]
    for i, dw in enumerate((-1, 0, 1)):
        for j, dg in enumerate((-0.5, 0, 0.5)):
            assert s["valor_agregado"][i][j] == pytest.approx(valor(wacc + dw, 3 + dg), rel=1e-12)
    assert s["valor_agregado"][0][2] - s["valor_agregado"][0][0] == pytest.approx(valor(wacc - 1, 3.5) - valor(wacc - 1, 2.5),
                                                                                 rel=1e-12)
    assert not any("sensibilidad" in x for x in lim)


def test_acc_val_advertencia_de_valor_terminal():
    r, _ = _correr("ACC-VAL-001", V.sintetico_val(), {"anios_explicitos": 3})
    assert r["peso_valor_terminal_pct"] > 85 and any("pesa el" in x for x in r["advertencias"])


@pytest.mark.parametrize("cambio,params,motivo", [
    ({"ejercicios": "tres"}, {}, "lista"), ({"recortar": 2}, {}, "< 3"), ({"moneda_ej": "USD"}, {}, "monedas"),
    ({"rf": {"valor": 3.0, "moneda": "USD"}}, {}, "monedas"), ({"beta": {"valor": 0.0, "fuente": "x"}}, {"g_terminal": 3.0}, "g ≥"),
    ({"capitalizacion": None}, {}, "capitalizacion"), ({"deuda_neta": None}, {}, "deuda_neta"),
    ({"tasa_impositiva_legal": None}, {}, "tasa impositiva"), ({"coste_deuda_pct": None}, {}, "coste de la deuda"),
    ({"crecimiento_explicito": {"valor": 3.0}}, {}, "fuente"), ({"sin_fecha": True}, {}, "fecha_presentacion"),
    ({"prm": {"valor": 9.0, "fuente": "x"}}, {}, "rango"), ({"roic_nuevo_pct": 10.0}, {"enfoque": "FCFE"}, "ROIC"),
    ({"multiplos_mercado": {"pex": 3.0}}, {}, "desconocido"),
])
def test_acc_val_rechazos(cambio, params, motivo):
    v = V.sintetico_val()
    if "recortar" in cambio:
        v["ejercicios"] = v["ejercicios"][:cambio.pop("recortar")]
    if "moneda_ej" in cambio:
        v["ejercicios"][1]["moneda"] = cambio.pop("moneda_ej")
    if cambio.pop("sin_fecha", False):
        del v["ejercicios"][0]["fecha_presentacion"]
    v = {k: x for k, x in {**v, **cambio}.items() if x is not None}
    _error("ACC-VAL-001", v, params, motivo)


def test_acc_val_per_no_aplicable_con_beneficio_negativo():
    r, lim = _correr("ACC-VAL-001", V.sintetico_val(beneficio_adelantado=-5.0))
    assert r["multiplos"]["per_adelantado"] is None and r["segunda_via"]["per_implicito_dcf"] is None
    assert any("PER no aplicable" in x for x in lim)


# ============================================================================= DER-OPT-001
def _N(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _bs_a_mano(S, K, T, r, q, s, call):
    d1 = (math.log(S / K) + (r - q + s * s / 2) * T) / (s * math.sqrt(T))
    d2 = d1 - s * math.sqrt(T)
    if call:
        return S * math.exp(-q * T) * _N(d1) - K * math.exp(-r * T) * _N(d2)
    return K * math.exp(-r * T) * _N(-d2) - S * math.exp(-q * T) * _N(-d1)


def test_der_opt_oraculo_precio_y_griegas_por_diferencias():
    c = {**V._OPT_PAR, "tipo": "put"}
    r, _ = _correr("DER-OPT-001", {"contratos": [c, {**c, "tipo": "call"}]})
    S, K, T, rr, q, s = 105, 95, 0.75, 0.03, 0.015, 0.25
    for fila, call in zip(r["contratos"], (False, True)):
        assert fila["precio"] == pytest.approx(_bs_a_mano(S, K, T, rr, q, s, call), rel=1e-12)
        h = 1e-4
        def f(call=call, **k):
            return _bs_a_mano(**{"S": S, "K": K, "T": T, "r": rr, "q": q, "s": s, "call": call, **k})
        assert fila["delta"] == pytest.approx((f(S=S + h) - f(S=S - h)) / (2 * h), rel=1e-7)
        assert fila["gamma"] == pytest.approx((f(S=S + 0.01) - 2 * f() + f(S=S - 0.01)) / 1e-4, rel=1e-5)
        assert fila["vega"] == pytest.approx((f(s=s + h) - f(s=s - h)) / (2 * h) / 100, rel=1e-7)
        assert fila["rho"] == pytest.approx((f(r=rr + h) - f(r=rr - h)) / (2 * h) / 100, rel=1e-7)
        assert fila["theta_dia"] == pytest.approx(-(f(T=T + h) - f(T=T - h)) / (2 * h) / 365, rel=1e-6)


def _crr_a_mano(S, K, T, r, q, s, call, americana, N):
    dt = T / N
    u = math.exp(s * math.sqrt(dt))
    d = 1 / u
    p = (math.exp((r - q) * dt) - d) / (u - d)
    val = [max((S * u ** (N - 2 * j) - K) if call else (K - S * u ** (N - 2 * j)), 0.0) for j in range(N + 1)]
    for i in range(N - 1, -1, -1):
        val = [math.exp(-r * dt) * (p * val[j] + (1 - p) * val[j + 1]) for j in range(i + 1)]
        if americana:
            val = [max(val[j], (S * u ** (i - 2 * j) - K) if call else (K - S * u ** (i - 2 * j))) for j in range(i + 1)]
    return val[0]


def test_der_opt_oraculo_crr_americana_a_mano():
    c = {"S": 40, "K": 44, "T": 0.5, "r": 4, "q": 1, "tipo": "put", "estilo": "americana", "sigma": 30}
    r, lim = _correr("DER-OPT-001", {"contrato": c}, {"pasos": 60})
    esperado = (_crr_a_mano(40, 44, 0.5, 0.04, 0.01, 0.3, False, True, 60)
                + _crr_a_mano(40, 44, 0.5, 0.04, 0.01, 0.3, False, True, 61)) / 2
    assert r["contratos"][0]["precio"] == pytest.approx(esperado, rel=1e-12)
    assert r["contratos"][0]["modelo"] == "CRR" and any("CRR" in x for x in lim)
    assert r["contratos"][0]["prima_ejercicio_anticipado"] > 0


def test_der_opt_black76_y_volatilidad_implicita_americana():
    c = {"S": 80, "K": 85, "T": 0.4, "r": 2, "tipo": "call", "estilo": "europea", "sigma": 35, "subyacente": "futuro"}
    r, _ = _correr("DER-OPT-001", {"contrato": c})
    F, K, T, rr, s = 80, 85, 0.4, 0.02, 0.35
    assert r["contratos"][0]["precio"] == pytest.approx(_bs_a_mano(F, K, T, rr, rr, s, True), rel=1e-12)
    assert r["contratos"][0]["rho"] == pytest.approx(-T * r["contratos"][0]["precio"] / 100, rel=1e-12)
    assert r["contratos"][0]["modelo"] == "Black-76"
    precio = _crr_a_mano(100, 110, 1, 0.05, 0.0, 0.28, False, True, 80) / 2 + _crr_a_mano(
        100, 110, 1, 0.05, 0.0, 0.28, False, True, 81) / 2
    ra, _ = _correr("DER-OPT-001", {"contrato": {"S": 100, "K": 110, "T": 1, "r": 5, "q": 0, "tipo": "put",
                                                "estilo": "americana", "precio": precio}}, {"pasos": 80})
    assert ra["contratos"][0]["iv_pct"] == pytest.approx(28.0, abs=1e-5)


def test_der_opt_superficie_rr_bf_y_densidad():
    K = [80, 90, 95, 100, 105, 110, 120]
    vol = [28, 24, 22, 20, 19, 18.5, 18.2]
    sup = {"vencimientos": [{"T": 0.5, "forward": 100, "r": 3, "strikes": K, "vol_pct": vol},
                            {"T": 1.0, "forward": 101, "r": 3, "strikes": K, "vol_pct": [v + 1 for v in vol]}]}
    r, _ = _correr("DER-OPT-001", {"superficie": sup}, {"densidad": True})
    f = r["superficie"]["vencimientos"][0]
    assert f["atm_pct"] == pytest.approx(20.0)
    sd = np.array(vol) / 100 * math.sqrt(0.5)
    dc = np.array([_N((math.log(100 / k) + 0.5 * x * x) / x) for k, x in zip(K, sd)])
    c_lado, p_lado = np.array(K) >= 100, np.array(K) <= 100
    sc = np.interp(0.25, dc[c_lado][::-1], np.array(vol)[c_lado][::-1])
    sp = np.interp(0.75, dc[p_lado][::-1], np.array(vol)[p_lado][::-1])
    assert f["rr25_pct"] == pytest.approx(sc - sp, rel=1e-10) and f["bf25_pct"] == pytest.approx((sc + sp) / 2 - 20, rel=1e-10)
    assert r["superficie"]["estructura_temporal_atm"][1]["T"] == 1.0
    assert len(f["densidad"]["q"]) == len(K) - 2 and all(x > 0 for x in f["densidad"]["q"])


@pytest.mark.parametrize("cambio,motivo", [
    ({"precio": 200.0, "sigma": None}, "no arbitraje"), ({"precio": 0.5, "sigma": None, "K": 50}, "no arbitraje"),
    ({"tipo": "digital"}, "fuera de ficha"), ({"estilo": "asiatica"}, "fuera de ficha"), ({"sigma": None}, "uno de los dos"),
    ({"precio": 5.0}, "uno de los dos"), ({"T": 0}, "mínimo"), ({"K": -1}, "mínimo"), ({"q": None}, "falta «q»"),
    ({"subyacente": "futuro"}, "no lleva dividendo"),
])
def test_der_opt_rechazos(cambio, motivo):
    c = {k: x for k, x in {**V._OPT_REF, "tipo": "call", **cambio}.items() if x is not None}
    _error("DER-OPT-001", {"contratos": [c]}, {}, motivo)


def test_der_opt_superficie_con_menos_de_5_strikes():
    _error("DER-OPT-001", {"superficie": {"vencimientos": [{"T": 1, "forward": 100, "r": 3, "strikes": [90, 100, 110, 120],
                                                             "vol_pct": [22, 20, 19, 18]}]}}, {}, "< 5")
    _error("DER-OPT-001", {"contratos": []}, {}, "elementos")


# ============================================================================= QA r01 de T-112: cotas de tamaño (H-01)
def _ejercicios(n):
    return [{**V.sintetico_val()["ejercicios"][0], "ejercicio": 1925 + i, "fecha_presentacion": f"{1926 + i}-03-31"}
            for i in range(n)]


def _semanas(n, inicio=date(2014, 11, 14)):
    return [(inicio + pd.Timedelta(weeks=i)).isoformat() for i in range(n)]


def _meses(n, inicio="1925-01-31"):
    return [d.date().isoformat() for d in pd.date_range(inicio, periods=n, freq="ME")]


def _curva_nodos(n):
    pl = [0.25 + 29.75 * i / (n - 1) for i in range(n)]
    return {"curva": {"fecha": "2026-11-13", "plazos": pl, "rendimientos": [3 + 0.4 * math.log1p(t) for t in pl]}}


def _historia_curvas(n):
    v = _curva_nodos(7)
    pl = v["curva"]["plazos"]
    v["historia"] = {"fechas": _semanas(n, date(1990, 1, 5)),
                     "rendimientos": [[3 + 0.01 * math.sin(i) + 0.4 * math.log1p(t) for t in pl] for i in range(n)]}
    return v


def _semanas_hasta(fin, desde):
    """Fechas semanales hacia atrás desde `fin` hasta `desde` (incluida si cae en la rejilla), en orden creciente."""
    f = [fin - pd.Timedelta(weeks=k) for k in range(((fin - desde).days // 7) + 1)]
    return [x.isoformat() for x in f[::-1]]


def _spread_largo(desde):
    fechas = _semanas_hasta(date(2026, 11, 13), date(1926, 11, 19))
    if desde is not None:
        fechas = [desde] + fechas
    return {**V.sintetico_spread(), "historia": {"fechas": fechas, "diferenciales_pb": [100 + math.sin(i) for i in range(len(fechas))]}}


def _ratings(n):
    return {**V.sintetico_spread(), "impagos": {"fuente": "x", "por_rating": {f"R{i}": {"pd_anual": 0.01, "peso": 1 / n}
                                                                              for i in range(n)}}}


def _fx_con_carry_largo():
    d = V.sintetico_fx()
    d["diferencial_pct"] = {"fechas": ["1924-01-02", d["spot"]["fechas"][0]], "valores": [1.0, 2.0]}
    return d


def _americanas(n):
    return {"contratos": [{**V._OPT_REF, "tipo": "put", "estilo": "americana"} for _ in range(n)]}


def _superficie(n_venc, n_strikes):
    K = [50 + i for i in range(n_strikes)]
    return {"superficie": {"vencimientos": [{"T": 0.1 * (j + 1), "forward": 100, "r": 3, "strikes": K,
                                             "vol_pct": [20 + 0.01 * (k - 100) ** 2 for k in K]} for j in range(n_venc)]}}


# (ficha, umbral, datos en la cota, datos por encima, parámetros). Cada cota se admite y un elemento más se rechaza.
COTAS = [
    ("ACC-VAL-001", "ejercicios_maximos", lambda: V.sintetico_val(ejercicios=_ejercicios(100)),
     lambda: V.sintetico_val(ejercicios=_ejercicios(101)), {}),
    ("ACC-VAL-001", "anios_historia_maximos",
     lambda: V.sintetico_val(historia_multiplos={"ev_ventas": {"fechas": ["1926-11-06", "2026-11-06"], "valores": [1.0, 1.1]}}),
     lambda: V.sintetico_val(historia_multiplos={"ev_ventas": {"fechas": ["1926-11-05", "2026-11-06"], "valores": [1.0, 1.1]}}),
     {}),
    ("ACC-ERP-001", "anios_historia_maximos", lambda: {**V._ERP, "cape": None, "beneficios_reales_10a": [150.0] * 100},
     lambda: {**V._ERP, "cape": None, "beneficios_reales_10a": [150.0] * 101}, {}),
    ("ACC-ERP-001", "anios_historia_maximos",
     lambda: {**V._ERP, "historia": {"fechas": _meses(1201), **{k: [3.0] * 1201 for k in ("prm_pp", "simple_pp", "ecy_pp")}}},
     lambda: {**V._ERP, "historia": {"fechas": _meses(1202), **{k: [3.0] * 1202 for k in ("prm_pp", "simple_pp", "ecy_pp")}}},
     {}),
    ("ACC-FACT-001", "anios_historia_maximos", lambda: {**V.sintetico_factores(n=1201), "fechas": _meses(1201)},
     lambda: {**V.sintetico_factores(n=1202), "fechas": _meses(1202)}, {"modelo": "CAPM"}),
    ("FIR-PRICE-001", "plazo_maximo_anios", lambda: V._bono_datos(5.0, 1, "2026-11-13", "2126-11-13", "30E/360", rendimiento=4.0),
     lambda: V._bono_datos(5.0, 1, "2026-11-13", "2126-11-14", "30E/360", rendimiento=4.0), {}),
    ("FIR-CURVE-001", "nodos_maximos", lambda: _curva_nodos(100), lambda: _curva_nodos(101), {"modelo": "NS", "lambda": "diebold_li"}),
    ("FIR-CURVE-001", "historia_maxima", lambda: _historia_curvas(1040), lambda: _historia_curvas(1041),
     {"modelo": "NS", "lambda": "diebold_li"}),
    ("FIR-CARRY-001", "nodos_maximos",
     lambda: {"curva": {"plazos": list(range(100)), "rendimientos": [3.0] * 100}, "tramo": 5, "financiacion": 1.0},
     lambda: {"curva": {"plazos": list(range(101)), "rendimientos": [3.0] * 101}, "tramo": 5, "financiacion": 1.0}, {}),
    ("FIR-CARRY-001", "tramos_maximos",
     lambda: {"curva": {"plazos": [0.25, 30], "rendimientos": [3.0, 4.0]}, "tramo": [1 + 0.2 * i for i in range(100)],
              "financiacion": 1.0},
     lambda: {"curva": {"plazos": [0.25, 30], "rendimientos": [3.0, 4.0]}, "tramo": [1 + 0.2 * i for i in range(101)],
              "financiacion": 1.0}, {}),
    ("FIR-SPREAD-001", "anios_historia_maximos", lambda: _spread_largo("1926-11-13"), lambda: _spread_largo("1926-11-12"), {}),
    ("FIR-SPREAD-001", "ratings_maximos", lambda: _ratings(22), lambda: _ratings(23), {}),
    ("FX-MOM-001", "pares_maximos", lambda: {"pares": {f"P{i}": V.sintetico_fx(fase=i) for i in range(45)}},
     lambda: {"pares": {f"P{i}": V.sintetico_fx(fase=i) for i in range(46)}}, {"volatilidad": "realizada"}),
    ("FX-MOM-001", "anios_historia_maximos", lambda: {"pares": {"X": V.sintetico_fx()}},
     lambda: {"pares": {"X": _fx_con_carry_largo()}}, {}),
    ("FX-PPA-001", "anios_historia_maximos", lambda: V.sintetico_ppa(1201, 0.001, 0.002),
     lambda: V.sintetico_ppa(1202, 0.001, 0.002), {}),
    ("DER-OPT-001", "contratos_maximos", lambda: {"contratos": [{**V._OPT_REF, "tipo": "call"}] * 50},
     lambda: {"contratos": [{**V._OPT_REF, "tipo": "call"}] * 51}, {"pasos": 2}),
    ("DER-OPT-001", "contratos_arbol_maximos", lambda: _americanas(10), lambda: _americanas(11), {"pasos": 2}),
    ("DER-OPT-001", "contratos_arbol_maximos", lambda: {"contratos": [{**V._OPT_REF, "tipo": "call"}] * 10},
     lambda: {"contratos": [{**V._OPT_REF, "tipo": "call"}] * 11}, {"pasos": 2, "modelo": "CRR"}),
    ("DER-OPT-001", "vencimientos_maximos", lambda: _superficie(24, 5), lambda: _superficie(25, 5), {}),
    ("DER-OPT-001", "strikes_maximos", lambda: _superficie(1, 100), lambda: _superficie(1, 101), {}),
]


@pytest.mark.parametrize("ficha,umbral,en_cota,encima,params", COTAS, ids=[f"{c[0]}:{c[1]}:{i}" for i, c in enumerate(COTAS)])
def test_cada_cota_de_tamano_se_admite_y_un_elemento_mas_se_rechaza(ficha, umbral, en_cota, encima, params):
    assert umbral in V.UMBRALES[ficha]
    limpio = {k: x for k, x in en_cota().items() if x is not None}
    res, _ = _correr(ficha, limpio, params)
    json.dumps(res, allow_nan=False)
    _error(ficha, {k: x for k, x in encima().items() if x is not None}, params, "cota de tamaño|más de 100 años")


def test_fir_price_un_rescate_repetido_se_rechaza():
    _error("FIR-PRICE-001", _bono(precio_limpio=101.0, rescates=[{"fecha": "2028-05-15", "precio": 100.0},
                                                                 {"fecha": "2028-05-15", "precio": 100.0}]), {}, "repetido")


def test_las_cotas_estan_en_umbrales_con_los_valores_de_la_nota():
    U = V.UMBRALES
    assert U["DER-OPT-001"]["rango_pasos"] == [2, 1000] and U["FIR-CURVE-001"]["arranques_maximos"] == 100
    assert U["FIR-CARRY-001"]["nodos_maximos"] == U["FIR-CURVE-001"]["nodos_maximos"] == 100   # la de FIR-CURVE-001
    assert {U[f]["anios_historia_maximos"] for f in ("ACC-VAL-001", "ACC-ERP-001", "ACC-FACT-001", "FIR-SPREAD-001",
                                                     "FX-MOM-001", "FX-PPA-001")} == {100}


# ============================================================================= QA r01 de T-112: conocibilidad (H-07)
def _con_corte(ficha, valores, corte, params=None):
    return V.FICHAS[ficha]["fn"]({**_ent(valores), "fecha_corte": corte}, copy.deepcopy(params or {}))


def _fuga(ficha, valores, corte, params=None):
    with pytest.raises(ErrorFicha, match="no conocible"):
        _con_corte(ficha, valores, corte, params)


def test_acc_val_un_ejercicio_presentado_despues_de_la_valoracion_se_rechaza():
    v = V.sintetico_val()
    v["ejercicios"][-1]["fecha_presentacion"] = "2027-06-30"   # el caso del revisor (r01_06, bloque 7)
    _fuga("ACC-VAL-001", v, "2026-11-13")
    _fuga("ACC-VAL-001", v, None)   # sin fecha de corte, frente a la fecha de la capitalización
    v["ejercicios"][-1]["fecha_presentacion"] = "2026-11-07"   # un día después de la capitalización (06-11-2026)
    _fuga("ACC-VAL-001", v, None)
    v["ejercicios"][-1]["fecha_presentacion"] = v["capitalizacion"]["fecha"]   # el mismo día: conocible
    a, _ = _con_corte("ACC-VAL-001", v, "2026-11-13")
    b, _ = _correr("ACC-VAL-001", v)
    assert a == b


def test_acc_val_capitalizacion_e_historia_de_multiplos_posteriores():
    _fuga("ACC-VAL-001", V.sintetico_val(), "2026-11-05")   # capitalización del 06-11 con corte el 05-11
    h = {"ev_ventas": {"fechas": [f"{2010 + i}-12-31" for i in range(16)] + ["2026-12-31"], "valores": [1.0] * 17}}
    _fuga("ACC-VAL-001", V.sintetico_val(historia_multiplos=h), None)


@pytest.mark.parametrize("ficha,valores,params", [
    ("ACC-ERP-001", {**V._ERP, "g5": {"valor": 4.0, "fuente": "x", "fecha": "2026-11-14"}}, {}),
    ("ACC-ERP-001", {**V._ERP, "historia": {"fechas": _meses(300, "2001-12-31"),
                                            **{k: [3.0] * 300 for k in ("prm_pp", "simple_pp", "ecy_pp")}}}, {}),
    ("ACC-FACT-001", {**V.sintetico_factores(n=84), "fechas": _meses(84, "2020-01-31")}, {}),
    ("FIR-CURVE-001", {"curva": {**_curva_nodos(7)["curva"], "fecha": "2026-11-14"}}, {"modelo": "NS", "lambda": "diebold_li"}),
    ("FIR-SPREAD-001", V.sintetico_spread(n=13 * 52), {}),
    ("FX-MOM-001", {"pares": {"X": V.sintetico_fx(inicio="2025-01-02")}}, {"volatilidad": "realizada"}),
    ("FX-MOM-001", {"pares": {"X": {**V.sintetico_fx(), "diferencial_pct": {"fechas": ["2024-06-03", "2026-11-20"],
                                                                              "valores": [2.0, 3.0]}}}}, {"volatilidad": "realizada"}),
    ("FX-PPA-001", V.sintetico_ppa(400, 0.001, 0.002), {}),
])
def test_un_dato_posterior_a_la_fecha_de_corte_se_rechaza(ficha, valores, params):
    _fuga(ficha, valores, "2026-11-13", params)


def test_con_un_corte_posterior_a_todos_los_datos_el_resultado_no_cambia():
    for f in FICHAS:
        v, p = BASE[f]
        a, la = _con_corte(f, v, "2200-01-01", p)
        b, lb = _correr(f, v, p)
        assert a == b and la == lb, f


def test_fx_ppa_vintage_posterior_o_sin_fecha():
    v = V.sintetico_ppa(36, 0.001, 0.002)   # datos hasta el 31-12-2003, vintage «2026-10-15»
    _fuga("FX-PPA-001", v, "2026-10-14")
    _con_corte("FX-PPA-001", v, "2026-10-15")
    v["indices"]["cotizada"]["vintage"] = "edición de octubre"
    _, lim = _con_corte("FX-PPA-001", v, "2026-10-15")
    assert any("vintage" in x for x in lim)
    _, lim = _correr("FX-PPA-001", v)
    assert not any("vintage" in x for x in lim)


def test_fir_price_liquidacion_posterior_al_corte_se_declara():
    v = _bono(precio_limpio=98.4)   # liquidación 13-11-2026
    r, lim = _con_corte("FIR-PRICE-001", v, "2026-11-11")
    assert any("liquidación" in x and "fecha de corte" in x for x in lim)
    r2, lim2 = _con_corte("FIR-PRICE-001", v, "2026-11-13")
    assert r == r2 and not any("liquidación" in x for x in lim2)


@pytest.mark.parametrize("corte", [20261113, "13/11/2026", "2026-13-01", True, [2026]])
def test_una_fecha_de_corte_mal_formada_se_rechaza(corte):
    v, p = BASE["ACC-VAL-001"]
    with pytest.raises(ErrorFicha, match="fecha_corte"):
        _con_corte("ACC-VAL-001", v, corte, p)


def test_el_motor_rechaza_un_ejercicio_posterior_a_la_fecha_de_corte(tmp_path):
    """El caso del revisor (r01_06, bloque 7) por Motor.servir: RECHAZADO con su entrada en RC."""
    from bloque_a.almacen import Almacen
    from bloque_a.configuracion import cargar_config
    from bloque_a.motor import servicio

    class _Proveedor:
        as_of = None
        nombre = "pruebas"
    m = servicio.Motor(Almacen(Path(tmp_path) / "almacen"), _Proveedor(), cargar_config())
    v = V.sintetico_val()
    v["ejercicios"][-1]["fecha_presentacion"] = "2027-06-30"
    r = m.servir({"operacion": "ACC-VAL-001", "datos": [{"valores": v}], "parametros": {}, "fecha_corte": "2026-11-13"}, "AG-21")
    assert r["estado"] == "RECHAZADO" and "no conocible" in r["detalle"] and "fecha_presentacion" in r["detalle"]
    rc = [e for e in m.almacen.leer("RC") if e.get("calc_id") == r["calc_id"]]
    assert len(rc) == 1 and rc[0]["tipo_entrada"] == "RECHAZO"


# ============================================================================= integración con el Motor (sin tocar servicio.py)
def test_los_casos_de_control_pasan_por_el_motor_y_quedan_en_rc(tmp_path, monkeypatch):
    """Como en la integración: cada ficha registrada en IMPLEMENTADAS con sus casos; verificar_casos_control los supera."""
    from bloque_a.almacen import Almacen
    from bloque_a.configuracion import cargar_config
    from bloque_a.motor import servicio

    class _Proveedor:
        as_of = None
        nombre = "pruebas"
    for f in FICHAS:
        monkeypatch.setitem(servicio.IMPLEMENTADAS, f, V.FICHAS[f])
        monkeypatch.setitem(servicio.CASOS_CONTROL, f, V.CASOS_CONTROL[f])
    m = servicio.Motor(Almacen(Path(tmp_path) / "almacen"), _Proveedor(), cargar_config())
    out = m.verificar_casos_control(FICHAS)
    assert all(out[f]["superados"] for f in FICHAS), {f: [c for c in out[f]["casos"] if not c["superado"]] for f in FICHAS}
    assert sum(1 for e in m.almacen.leer("RC") if e["tipo_entrada"] == "CASOS_CONTROL") == len(FICHAS)
