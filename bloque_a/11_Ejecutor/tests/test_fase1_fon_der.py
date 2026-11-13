"""Pruebas de las fichas FON y DER del Motor (T-106, Motor Fase 1; Catálogo V5.0, secciones 16 y 17).

Cubren: los casos de control de cada ficha (campo «Verificación»), cada regla de rechazo, el determinismo, las
claves de «Salidas», los roles de series y valores calculados a mano con datos sintéticos simples.
"""
import copy
import json
import math

import numpy as np
import pandas as pd
import pytest
from scipy import stats

from bloque_a.motor import fichas_fon_der as fd
from bloque_a.motor.operaciones import ErrorFicha

FICHAS_TAREA = ["FON-DISC-001", "FON-FLOW-001", "FON-TD-001", "FON-LEV-001",
                "DER-VRP-001", "DER-SKEW-001", "DER-TERM-001", "DER-ROLL-001"]
# Frases numéricamente comprobables del campo «Verificación» de cada ficha.
FRASES_VERIFICACION = {"FON-DISC-001": 3, "FON-FLOW-001": 2, "FON-TD-001": 2, "FON-LEV-001": 2,
                       "DER-VRP-001": 3, "DER-SKEW-001": 3, "DER-TERM-001": 2, "DER-ROLL-001": 3}
CASOS = [(f, c) for f, cs in fd.CASOS_CONTROL.items() for c in cs]


def _run(ficha, valores, params=None, series_rol=None):
    ent = {"valores": copy.deepcopy(valores), "series": {}, "series_rol": series_rol or {}}
    return fd.FICHAS[ficha]["fn"](ent, dict(params or {}))


def _base(ficha):
    """Datos válidos de partida: los del primer caso de control no trivial de cada ficha."""
    return {
        "FON-DISC-001": lambda: fd._ctl_disc(iguales=False),
        "FON-FLOW-001": lambda: fd._ctl_flow(False),
        "FON-TD-001": lambda: fd._ctl_td(False),
        "FON-LEV-001": lambda: fd._ctl_lev(2.0),
        "DER-VRP-001": lambda: fd._ctl_vrp(1.3),
        "DER-SKEW-001": fd._ctl_skew_svi,
        "DER-TERM-001": lambda: fd._ctl_term(False),
        "DER-ROLL-001": lambda: fd._ctl_roll(False),
    }[ficha]()


# ------------------------------------------------------------------------------------------- registro
def test_registro_completo_y_coherente():
    assert set(fd.FICHAS) == set(FICHAS_TAREA) == set(fd.PARAMETROS_POR_DEFECTO) == set(fd.CASOS_CONTROL)
    assert "DER-OPT-001" not in fd.FICHAS
    for f, meta in fd.FICHAS.items():
        assert callable(meta["fn"])
        assert meta["modulo"].startswith("MC-") and meta["version"] == "1.0"
        assert meta["cifra"] in ("DETERMINISTA", "ESTADISTICA")
        assert meta["ri"] and meta["tol"] in (1e-10, 1e-8)
        assert len(fd.CASOS_CONTROL[f]) >= FRASES_VERIFICACION[f], f


def test_parametros_por_defecto_segun_fichas():
    p = fd.PARAMETROS_POR_DEFECTO
    assert p["FON-DISC-001"] == {"ventana_media": 52, "ventana_larga": 5, "kappa": 0.5, "agregacion": "mediana"}
    assert p["FON-FLOW-001"]["ventanas"] == [1, 3, 12] and p["FON-FLOW-001"]["ventana_z"] == 36
    assert p["FON-TD-001"]["variante_indice"] == "neta"
    assert p["FON-LEV-001"]["L"] == 2 and p["FON-LEV-001"]["n_trayectorias"] == 10000
    assert p["DER-VRP-001"]["plazo"] == 30 and p["DER-VRP-001"]["prevision_rv"] == "HAR"
    assert p["DER-SKEW-001"]["delta"] == 25 and p["DER-SKEW-001"]["vencimiento"] == 3
    assert p["DER-TERM-001"]["vencimientos"] == [1, 3, 6, 12]
    assert p["DER-ROLL-001"]["anualizacion"] == 365


# ------------------------------------------------------------------------------------------- casos de control
@pytest.mark.parametrize("ficha,caso", CASOS, ids=[f"{f}:{c['nombre']}" for f, c in CASOS])
def test_caso_control(ficha, caso):
    res, lim = fd.ejecutar_caso(ficha, caso)
    assert caso["comprobar"](res), caso["nombre"]
    json.dumps(res)   # JSON-serializable
    assert all(isinstance(x, str) and x for x in lim)


# ------------------------------------------------------------------------------------------- determinismo
@pytest.mark.parametrize("ficha", FICHAS_TAREA)
def test_determinismo_y_sin_mutar_entradas(ficha):
    datos = _base(ficha)
    copia = copy.deepcopy(datos)
    ent = {"valores": datos, "series": {}, "series_rol": {}}
    r1, l1 = fd.FICHAS[ficha]["fn"](ent, {})
    r2, l2 = fd.FICHAS[ficha]["fn"](ent, {})
    assert json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True) and l1 == l2
    assert datos == copia


# ------------------------------------------------------------------------------------------- salidas
SALIDAS = {
    "FON-DISC-001": ["descuento_agregado_pct", "z_scores", "percentil", "dispersion_pp", "vida_media_meses",
                     "rentabilidad_normalizacion_pct", "desglose_subcategoria"],
    "FON-FLOW-001": ["categorias", "serie_flujos_acumulados", "flujo_total"],
    "FON-TD-001": ["td_mediana_pb", "td_cuartiles_pb", "te_mediano_pct", "descomposicion_pb",
                   "tendencia_pb_por_anio", "segmentos"],
    "FON-LEV-001": ["arrastre_pct", "R_L_menos_L_por_R_pp", "umbral_sigma_pct", "rejilla", "percentiles_simulados"],
    "DER-VRP-001": ["sigma_imp_pct", "sigma_real_esperada_pct", "sigma_real_posterior_ultima_pct", "vrp_ex_ante",
                    "percentiles", "frecuencia_vrp_positiva_pct", "es_venta_varianza_pct"],
    "DER-SKEW-001": ["rr_puntos", "bf_puntos", "pendiente_normalizada", "coste_proteccion_pct",
                     "asimetria_neutral_riesgo", "percentiles"],
    "DER-TERM-001": ["sigma_por_vencimiento_pct", "pendiente_puntos", "ratio_1m_3m", "estado", "sigma_fwd",
                     "eventos", "percentiles"],
    "DER-ROLL-001": ["vencimientos", "carry_implicito_pct", "roll_yield_pct", "desviacion_vs_teorico_pb",
                     "percentiles", "descomposicion"],
}


@pytest.mark.parametrize("ficha", FICHAS_TAREA)
def test_claves_de_salidas(ficha):
    res, _ = _run(ficha, _base(ficha))
    for k in SALIDAS[ficha]:
        assert k in res, f"{ficha}: falta la salida {k}"
    assert "unidades" in res


def test_claves_por_categoria_y_vencimiento():
    res, _ = _run("FON-FLOW-001", _base("FON-FLOW-001"))
    for fila in res["categorias"].values():
        for k in ("flujo_ultimo", "flujo_relativo_ultimo_pct", "acumulados", "z_score", "autocorrelaciones", "rango"):
            assert k in fila
    res, _ = _run("DER-ROLL-001", _base("DER-ROLL-001"))
    for fila in res["vencimientos"]:
        for k in ("base_puntos", "base_pct", "carry_implicito_pct", "desviacion_vs_teorico_pb"):
            assert k in fila


# ------------------------------------------------------------------------------------------- rechazos
def _mut(ficha, fn, params=None):
    d = _base(ficha)
    fn(d)
    return d, params


def _recortar_disc(d, n):
    d["fechas"] = d["fechas"][-n:]
    for mb in d["miembros"].values():
        mb["precio"], mb["nav"] = mb["precio"][-n:], mb["nav"][-n:]


def _recortar_flow(d, n):
    d["fechas"] = d["fechas"][-n:]
    for c in d["categorias"].values():
        c["aum"] = c["aum"][-n:]
        c["rentabilidad"] = c["rentabilidad"][-(n - 1):]


def _vrp_recortar(d, n):
    d["precios_subyacente"], d["vol_implicita"] = d["precios_subyacente"][-n:], d["vol_implicita"][-n:]


def _flat_surface(d):
    d["superficie"]["vols"] = [0.2] * len(d["superficie"]["strikes"])


RECHAZOS = [
    # FON-DISC-001
    ("FON-DISC-001", "< 5 miembros", lambda d: d["miembros"].pop("M5"), None, "< 5 miembros"),
    ("FON-DISC-001", "sin fecha de NAV", lambda d: d["miembros"]["M1"].pop("fecha_nav"), None, "sin fecha de NAV"),
    ("FON-DISC-001", "NAV > 6 meses", lambda d: d["miembros"]["M1"].update(fecha_nav="2022-06-01"), None, "> 6 meses"),
    ("FON-DISC-001", "NAV privado > 12 meses",
     lambda d: d["miembros"]["M1"].update(fecha_nav="2021-06-01", privado=True), None, "> 12 meses"),
    ("FON-DISC-001", "NAV posterior al corte", lambda d: d["miembros"]["M1"].update(fecha_nav="2030-01-01"), None,
     "posterior"),
    ("FON-DISC-001", "< 3 años", lambda d: _recortar_disc(d, 2 * 52), None, "3 años"),
    ("FON-DISC-001", "NAV mensual", lambda d: _recortar_disc(d, len(d["fechas"])) or d.update(
        fechas=[str(x.date()) for x in pd.date_range("2010-01-31", periods=len(d["fechas"]), freq="ME")]),
     None, "semanal"),
    ("FON-DISC-001", "huecos", lambda d: d["miembros"]["M2"]["precio"].__setitem__(3, float("nan")), None, "huecos"),
    ("FON-DISC-001", "kappa fuera de rango", lambda d: None, {"kappa": 1.5}, "fuera del rango"),
    ("FON-DISC-001", "ventana_media fuera de rango", lambda d: None, {"ventana_media": 10}, "fuera del rango"),
    ("FON-DISC-001", "media ponderada sin capitalización",
     lambda d: d["miembros"]["M1"].pop("capitalizacion"), {"agregacion": "media_ponderada"}, "capitalización"),
    # FON-FLOW-001
    ("FON-FLOW-001", "sin taxonomía", lambda d: d.pop("taxonomia"), None, "sin taxonomía"),
    ("FON-FLOW-001", "< 12 meses", lambda d: _recortar_flow(d, 11), None, "< 12 meses"),
    ("FON-FLOW-001", "mensual < 3 años", lambda d: _recortar_flow(d, 25), None, "≥ 3 años"),
    ("FON-FLOW-001", "hueco de fechas", lambda d: d["fechas"].__setitem__(5, "2021-07-15"), None, "frecuencia"),
    ("FON-FLOW-001", "sin frecuencia", lambda d: d.pop("frecuencia"), None, "frecuencia"),
    ("FON-FLOW-001", "sin rentabilidad ni flujo", lambda d: d["categorias"]["RF_activa"].pop("rentabilidad"), None,
     "faltan rentabilidad"),
    # FON-TD-001
    ("FON-TD-001", "variante no declarada (aclaración)", lambda d: d.pop("variante_indice"), None, "ACLARACION"),
    ("FON-TD-001", "variante distinta", lambda d: d.update(variante_indice="bruta"), None, "TD espuria"),
    ("FON-TD-001", "< 5 miembros", lambda d: d["miembros"].pop("V1"), None, "< 5 miembros"),
    ("FON-TD-001", "< 3 años", lambda d: [d.update(rentabilidades_indice=d["rentabilidades_indice"][-500:])]
     + [m.update(rentabilidades=m["rentabilidades"][-500:]) for m in d["miembros"].values()], None, "3 años"),
    ("FON-TD-001", "sin replicación", lambda d: d["miembros"]["V2"].pop("replicacion"), None, "replicación"),
    ("FON-TD-001", "sin gastos", lambda d: d["miembros"]["V2"].pop("gastos_corrientes"), None, "gastos_corrientes"),
    # FON-LEV-001
    ("FON-LEV-001", "sin L declarado", lambda d: d.pop("L"), None, "sin L declarado"),
    ("FON-LEV-001", "sin datos diarios", lambda d: d.pop("fechas"), None, "sin datos diarios"),
    ("FON-LEV-001", "fechas semanales", lambda d: d.update(
        fechas=[str(x.date()) for x in pd.date_range("2000-01-07", periods=len(d["fechas"]), freq="W-FRI")]),
     None, "sin datos diarios"),
    ("FON-LEV-001", "L fuera de rango", lambda d: d.update(L=4), None, "fuera del rango"),
    ("FON-LEV-001", "horizonte fuera de rango", lambda d: d.update(horizonte=10), None, "fuera del rango"),
    ("FON-LEV-001", "sin horizonte", lambda d: d.pop("horizonte"), None, "horizonte"),
    ("FON-LEV-001", "< 1 año", lambda d: d.update(rentabilidades_indice=d["rentabilidades_indice"][:200],
                                                  fechas=d["fechas"][:200]), None, "1 año"),
    ("FON-LEV-001", "sin tipo de financiación", lambda d: d.pop("tipo_financiacion"), None, "tipo_financiacion"),
    ("FON-LEV-001", "sin gastos medios", lambda d: d.pop("gastos_medios"), None, "gastos_medios"),
    # DER-VRP-001
    ("DER-VRP-001", "< 2 años", lambda d: _vrp_recortar(d, 400), None, "< 2 años"),
    ("DER-VRP-001", "< 3 años (entradas mínimas)", lambda d: _vrp_recortar(d, 600), None, "entradas mínimas"),
    ("DER-VRP-001", "plazos no alineados", lambda d: d.update(plazo_dias_vol_implicita=60), None, "no alineados"),
    ("DER-VRP-001", "longitudes no alineadas", lambda d: d["vol_implicita"].pop(), None, "no alineados"),
    ("DER-VRP-001", "sin plazo de la implícita", lambda d: d.pop("plazo_dias_vol_implicita"), None, "plazo_dias"),
    ("DER-VRP-001", "réplica con < 5 strikes", lambda d: d.update(cesta_opciones={
        "strikes": [90, 95, 100, 105], "q": [1, 2, 3, 2], "forward": 100, "tipo_interes": 0, "dias": 30}),
     None, "< 5 precios de ejercicio"),
    ("DER-VRP-001", "réplica a otro plazo", lambda d: d.update(cesta_opciones={
        "strikes": [90, 95, 100, 105, 110], "q": [1, 2, 3, 2, 1], "forward": 100, "tipo_interes": 0, "dias": 60}),
     None, "no alineados"),
    ("DER-VRP-001", "prevision_rv desconocida", lambda d: None, {"prevision_rv": "XYZ"}, "no admitida"),
    ("DER-VRP-001", "plazo fuera de rango", lambda d: None, {"plazo": 120}, "fuera del rango"),
    # DER-SKEW-001
    ("DER-SKEW-001", "< 5 strikes", lambda d: d["superficie"].update(
        strikes=d["superficie"]["strikes"][6:10], vols=d["superficie"]["vols"][6:10]), None, "< 5 precios de ejercicio"),
    ("DER-SKEW-001", "superficie con arbitraje", lambda d: d.update(superficie={
        "strikes": [80, 90, 100, 110, 120], "vols": [0.2, 0.2, 0.6, 0.2, 0.2], "forward": 100}), None, "arbitraje"),
    ("DER-SKEW-001", "historia < 2 años", lambda d: d.update(historia_rr=d["historia_rr"][:300]), None, "2 años"),
    ("DER-SKEW-001", "sin superficie ni RR/BF", lambda d: d.pop("superficie") and d.update(delta=25, vol_atm=0.2), None,
     "ni superficie"),
    ("DER-SKEW-001", "vencimiento distinto", lambda d: d.update(vencimiento_meses=6), None, "distinto del parámetro"),
    ("DER-SKEW-001", "SVI sin superficie", lambda d: d.pop("superficie") and d.update(
        delta=25, vol_put=0.22, vol_call=0.2, vol_atm=0.2), {"metodo": "SVI"}, "SVI exige superficie"),
    ("DER-SKEW-001", "delta de cotización distinta", lambda d: d.pop("superficie") and d.update(
        delta=10, vol_put=0.22, vol_call=0.2, vol_atm=0.2), None, "delta"),
    ("DER-SKEW-001", "delta fuera de rango", lambda d: None, {"delta": 40}, "fuera del rango"),
    # DER-TERM-001
    ("DER-TERM-001", "< 3 vencimientos", lambda d: d.update(vencimientos_meses=[1, 3], vol_atm=[0.2, 0.2]), None,
     "< 3 vencimientos"),
    ("DER-TERM-001", "arbitraje de calendario", lambda d: d.update(vol_atm=[0.40, 0.20, 0.15, 0.10]), None,
     "arbitraje de calendario"),
    ("DER-TERM-001", "sin calendario de eventos", lambda d: d.pop("calendario_eventos"), None, "calendario"),
    ("DER-TERM-001", "historia < 2 años", lambda d: d.update(historia_vol_1m=d["historia_vol_1m"][:300],
                                                             historia_vol_3m=d["historia_vol_3m"][:300]), None, "2 años"),
    ("DER-TERM-001", "sin 1 mes cotizado (no se extrapola)", lambda d: d.update(vencimientos_meses=[2, 6, 12],
                                                                                vol_atm=[0.2, 0.2, 0.2]), None,
     "no se extrapola"),
    ("DER-TERM-001", "evento sin σ base", lambda d: d.update(calendario_eventos=[{"nombre": "BCE", "vencimiento_meses": 3}]),
     None, "sigma_base"),
    # DER-ROLL-001
    ("DER-ROLL-001", "< 2 vencimientos", lambda d: d["futuros"].pop(), None, "< 2 vencimientos"),
    ("DER-ROLL-001", "sin tipo de financiación", lambda d: d.pop("tipo_financiacion"), None, "sin tipo de financiación"),
    ("DER-ROLL-001", "tipo de activo desconocido", lambda d: d.update(tipo_activo="acciones"), None, "no admitido"),
    ("DER-ROLL-001", "índice sin dividendos", lambda d: d.pop("rendimiento_dividendo"), None, "rendimiento_dividendo"),
    ("DER-ROLL-001", "anualización no admitida", lambda d: None, {"anualizacion": 300}, "no admitida"),
    ("DER-ROLL-001", "vencimientos repetidos", lambda d: d["futuros"][1].update(dias=30.0), None, "repetidos"),
    ("DER-ROLL-001", "bono sin factor de conversión", lambda d: d.update(
        tipo_activo="bono", precio_entregable=110.0, rendimiento_entregable=0.04), None, "factor_conversion"),
]


@pytest.mark.parametrize("ficha,nombre,mut,params,motivo", RECHAZOS, ids=[f"{r[0]}:{r[1]}" for r in RECHAZOS])
def test_reglas_de_rechazo(ficha, nombre, mut, params, motivo):
    d, p = _mut(ficha, mut, params)
    with pytest.raises(ErrorFicha) as e:
        _run(ficha, d, p)
    assert motivo in str(e.value), str(e.value)
    assert ficha in str(e.value)


def test_error_ficha_es_value_error():
    assert issubclass(ErrorFicha, ValueError)


# ------------------------------------------------------------------------------------------- FON-DISC-001
def test_disc_valores_a_mano():
    d = fd._ctl_disc(iguales=False, constante=True)   # descuentos constantes −10, −8, −6, −4, −2 %
    res, _ = _run("FON-DISC-001", d)
    assert res["descuento_agregado_pct"] == pytest.approx(-6.0, abs=1e-10)
    assert res["dispersion_pp"]["desviacion"] == pytest.approx(math.sqrt(10.0), rel=1e-12)
    assert res["dispersion_pp"]["rango"] == pytest.approx(8.0, rel=1e-12)
    assert res["z_scores"] == {"ventana_media": None, "ventana_larga": None}    # historia sin variación: nunca 0
    assert res["vida_media_meses"] is None
    assert res["rentabilidad_normalizacion_pct"] == pytest.approx(0.0, abs=1e-12)


def test_disc_normalizacion_a_mano():
    d = fd._ctl_disc(iguales=False, constante=True)
    n = len(d["fechas"])
    for mb in d["miembros"].values():   # todos con −10 % y −20 % en la última semana
        nav = np.asarray(mb["nav"])
        dd = np.full(n, -0.10)
        dd[-1] = -0.20
        mb["precio"] = list(nav * (1 + dd))
    res, _ = _run("FON-DISC-001", d, {"kappa": 0.5})
    d_act = -0.20
    media52 = (51 * -0.10 + d_act) / 52
    d_obj = d_act + 0.5 * (media52 - d_act)
    assert res["rentabilidad_normalizacion_pct"] == pytest.approx(((1 + d_obj) / (1 + d_act) - 1) * 100, rel=1e-10)
    assert res["percentil"] == pytest.approx(1 / n)


def test_disc_nav_con_ajuste_declarado_y_privado():
    d = fd._ctl_disc(iguales=False)
    d["miembros"]["M1"].update(fecha_nav="2022-06-01", ajuste_nav_declarado="NAV trimestral rodado con índice")
    d["miembros"]["M2"].update(fecha_nav="2022-11-15", privado=True)   # 7 meses: admitido en activos privados
    res, lim = _run("FON-DISC-001", d)
    assert any("ajuste declarado" in x for x in lim)
    d["catalizadores"] = ["recompras anunciadas"]
    d["rentabilidad_nav_supuesta"] = 0.02
    d["miembros"]["M1"]["subcategoria"] = "inmobiliario"
    res, lim = _run("FON-DISC-001", d)
    assert res["catalizadores"] == ["recompras anunciadas"]
    norm = res["normalizacion"]["ventana_media"]
    assert norm["rentabilidad_total_supuesta_pct"] == pytest.approx(
        ((1 + norm["rentabilidad_normalizacion_pct"] / 100) * 1.02 - 1) * 100, rel=1e-12)
    assert set(res["desglose_subcategoria"]) == {"inmobiliario", "(sin subcategoría)"}


# ------------------------------------------------------------------------------------------- FON-FLOW-001
def test_flow_valores_a_mano():
    fechas = [str(x.date()) for x in pd.date_range("2021-01-31", periods=37, freq="ME")]
    cats = {}
    for nombre in ("A", "B"):
        aum = [100.0] * 36 + [110.0]
        r = [0.0] * 35 + [0.05]
        cats[nombre] = {"aum": aum, "rentabilidad": r}
    res, _ = _run("FON-FLOW-001", {"taxonomia": "T", "frecuencia": "mensual", "fechas": fechas, "categorias": cats})
    a = res["categorias"]["A"]
    assert a["flujo_ultimo"] == pytest.approx(5.0)                       # 110 − 100·1,05
    assert a["flujo_relativo_ultimo_pct"] == pytest.approx(5.0)
    assert a["acumulados"]["12"]["moneda"] == pytest.approx(5.0)
    assert res["flujo_total"][-1] == pytest.approx(10.0)
    assert res["serie_flujos_acumulados"]["A"][-1] == pytest.approx(5.0)
    assert a["rango"] == {"1": 1, "3": 1, "12": 1}                       # empate: por nombre
    assert res["categorias"]["B"]["rango"]["1"] == 2


def test_flow_semanal_un_anio_y_senal_contraria():
    fechas = [str(x.date()) for x in pd.date_range("2023-01-06", periods=54, freq="W-FRI")]
    t = np.arange(53)
    cats = {"X": {"aum": [1000.0] + list(1000 + np.cumsum(5 * np.sin(t))), "flujo": list(5 * np.sin(t)),
                  "gestion": "indexada"}}
    d = {"taxonomia": "T", "frecuencia": "semanal", "fechas": fechas, "categorias": cats}
    res, lim = _run("FON-FLOW-001", d, {"senal_contraria": True})
    assert res["categorias"]["X"]["senal_contraria"] in ("ENTRADAS_EXTREMAS", "SALIDAS_EXTREMAS", "NINGUNA")
    assert res["verificacion"]["identidad_aum_residuo_max_abs"]["X"] is None
    assert any("hipótesis" in x for x in res["advertencias"]) and any("ventana_z" in x for x in lim)


# ------------------------------------------------------------------------------------------- FON-TD-001
def test_td_valores_a_mano():
    n = 3 * 252
    miembros = {}
    for i in range(5):
        g = 0.001 * (i + 1)
        miembros[f"V{i}"] = {"rentabilidades": [-g / 252] * n, "gastos_corrientes": g,
                             "replicacion": "fisica" if i < 3 else "sintetica"}
    res, lim = _run("FON-TD-001", {"rentabilidades_indice": [0.0] * n, "variante_indice": "neta", "miembros": miembros})
    esperado = ((1 - 0.003 / 252) ** 252 - 1) * 1e4
    assert res["td_mediana_pb"] == pytest.approx(esperado, rel=1e-10)
    assert res["te_mediano_pct"] == pytest.approx(0.0, abs=1e-12)
    assert res["tendencia_pb_por_anio"] == pytest.approx(0.0, abs=1e-9)
    assert res["referencia_ingenua_td_pb"] == pytest.approx(-30.0)
    assert res["descomposicion_pb"]["gastos_corrientes"] == pytest.approx(-30.0)
    assert set(res["segmentos"]["replicacion"]) == {"fisica", "sintetica"}
    assert any("frágil" in x for x in lim) and any("residuo" in x for x in lim)


# ------------------------------------------------------------------------------------------- FON-LEV-001
def test_lev_formula_a_mano():
    d = fd._ctl_lev(2.0)
    d.update(sigma=0.20, rendimiento_indice=0.05, horizonte=126, tipo_financiacion=0.0, gastos_medios=0.0)
    res, _ = _run("FON-LEV-001", d)
    T = 126 / 252
    assert res["arrastre_pct"] == pytest.approx(0.5 * 2 * 0.04 * T * 100, rel=1e-12)
    assert res["R_L_formula_pct"] == pytest.approx((1.05 ** 2 * math.exp(-0.02) - 1) * 100, rel=1e-12)
    assert res["umbral_sigma_pct"] == pytest.approx(math.sqrt(-math.log(1.10 / 1.05 ** 2) / (0.5 * 2 * T)) * 100, rel=1e-12)
    assert res["estado_umbral"] == "UMBRAL"
    d.update(tipo_financiacion=0.02, gastos_medios=0.01)
    res, _ = _run("FON-LEV-001", d)
    assert res["R_L_formula_pct"] == pytest.approx((1.05 ** 2 * math.exp(-0.02) - 1 - 0.03 * T) * 100, rel=1e-12)
    assert res["estado_umbral"] == "DOMINA_CON_CUALQUIER_SIGMA" and res["umbral_sigma_pct"] is None
    assert res["percentiles_simulados"] is None


def test_lev_reconstruccion_exacta_a_mano():
    res, lim = _run("FON-LEV-001", fd._ctl_lev(2.0))   # ±1 % alterno, ventanas de 100 sesiones
    assert res["reconstruccion"]["R_L_exacta_ultima_pct"] == pytest.approx(((1 - 4e-4) ** 50 - 1) * 100, rel=1e-10)
    assert any("SIM-MC-001" in x for x in lim)


def test_lev_inverso_y_rol_de_serie():
    d = fd._ctl_lev(-1.0)
    res_v, _ = _run("FON-LEV-001", d)
    precios = 100 * np.cumprod(np.concatenate([[1.0], 1 + np.asarray(d["rentabilidades_indice"])]))
    s = pd.Series(precios, index=pd.bdate_range("2022-12-30", periods=precios.size))
    sin_valores = {k: v for k, v in d.items() if k not in ("rentabilidades_indice", "fechas")}
    res_s, _ = _run("FON-LEV-001", sin_valores, series_rol={"indice": s})
    assert res_s["arrastre_pct"] == pytest.approx(res_v["arrastre_pct"], rel=1e-10)
    assert res_s["reconstruccion"]["R_L_exacta_ultima_pct"] == pytest.approx(
        res_v["reconstruccion"]["R_L_exacta_ultima_pct"], rel=1e-10)
    semanal = pd.Series(precios[:60], index=pd.date_range("2020-01-03", periods=60, freq="W-FRI"))
    with pytest.raises(ErrorFicha, match="sin datos diarios"):
        _run("FON-LEV-001", sin_valores, series_rol={"indice": semanal})


# ------------------------------------------------------------------------------------------- DER-VRP-001
def test_vrp_replica_a_mano():
    d = fd._ctl_vrp(1.0)
    K = np.array([80.0, 90.0, 100.0, 110.0, 120.0])
    Q = np.array([1.0, 2.0, 5.0, 2.0, 1.0])
    d["cesta_opciones"] = {"strikes": list(K), "q": list(Q), "forward": 100.0, "tipo_interes": 0.0, "dias": 30}
    res, _ = _run("DER-VRP-001", d, {"prevision_rv": "realizada_pasada"})
    T = 30 / 365
    var = 2 / T * float(np.sum(10.0 / K ** 2 * Q))
    assert res["replica"]["sigma_imp_replica_pct"] == pytest.approx(math.sqrt(var) * 100, rel=1e-12)


def test_vrp_realizada_pasada_a_mano():
    res, _ = _run("DER-VRP-001", fd._ctl_vrp(1.3), {"prevision_rv": "realizada_pasada"})
    sr = 0.01 * math.sqrt(252)
    assert res["sigma_real_esperada_pct"] == pytest.approx(sr * 100, rel=1e-12)
    assert res["vrp_ex_ante"]["varianza_puntos"] == pytest.approx(((1.3 * sr) ** 2 - sr ** 2) * 1e4, rel=1e-10)
    assert res["vrp_ex_ante"]["volatilidad_puntos"] == pytest.approx(0.3 * sr * 100, rel=1e-10)
    assert res["frecuencia_vrp_positiva_pct"] == pytest.approx(100.0)
    assert res["sesiones_plazo"] == 21


def _gbm(n, semilla=7):
    rng = np.random.default_rng(semilla)   # pseudoaleatorio con semilla: datos de prueba reproducibles
    r = rng.normal(0.0002, 0.012, n)
    precios = 100 * np.cumprod(np.concatenate([[1.0], 1 + r]))
    iv = 0.012 * math.sqrt(252) * 1.15 * np.ones(n + 1)
    return precios, iv


def test_vrp_har_y_roles_de_serie():
    precios, iv = _gbm(3 * 252 + 30)
    v = {"precios_subyacente": list(precios), "vol_implicita": list(iv), "plazo_dias_vol_implicita": 30}
    res_v, lim = _run("DER-VRP-001", v)
    assert res_v["prevision_rv"] == "HAR" and res_v["sigma_real_esperada_pct"] > 0
    assert 0 <= res_v["percentiles"]["vrp_ex_ante_en_historia_ex_post"] <= 1
    assert any("5 años" in x for x in lim)
    idx = pd.bdate_range("2020-01-01", periods=precios.size)
    res_s, _ = _run("DER-VRP-001", {"plazo_dias_vol_implicita": 30},
                    series_rol={"subyacente": pd.Series(precios, index=idx), "vol_implicita": pd.Series(iv, index=idx)})
    assert json.dumps(res_s, sort_keys=True) == json.dumps(res_v, sort_keys=True)


def test_vrp_garch_si_hay_arch():
    pytest.importorskip("arch")
    precios, iv = _gbm(3 * 252 + 30)
    res, _ = _run("DER-VRP-001", {"precios_subyacente": list(precios), "vol_implicita": list(iv),
                                  "plazo_dias_vol_implicita": 30}, {"prevision_rv": "GARCH"})
    assert res["prevision_rv"] == "GARCH" and res["sigma_real_esperada_pct"] > 0


# ------------------------------------------------------------------------------------------- DER-SKEW-001
def test_skew_cotizaciones_rr_bf_a_mano():
    d = {"vencimiento_meses": 3, "delta": 25, "rr": 0.04, "bf": 0.01, "vol_atm": 0.20, "historia_rr": fd._ctl_skew_hist()}
    res, lim = _run("DER-SKEW-001", d)
    assert res["sigma_put_pct"] == pytest.approx(23.0) and res["sigma_call_pct"] == pytest.approx(19.0)
    assert res["rr_puntos"] == pytest.approx(4.0) and res["bf_puntos"] == pytest.approx(1.0)
    assert res["pendiente_normalizada"] == pytest.approx(0.2)
    assert res["coste_proteccion_pct"] is None and res["svi"] is None
    assert any("sin superficie" in x for x in lim)


def test_skew_superficie_plana_y_coste_proteccion_a_mano():
    d = fd._ctl_skew_svi()
    _flat_surface(d)
    d["superficie"]["tipo_interes"] = 0.02
    res, _ = _run("DER-SKEW-001", d)
    assert res["rr_puntos"] == pytest.approx(0.0, abs=1e-10) and res["bf_puntos"] == pytest.approx(0.0, abs=1e-10)
    T, F, S, K, s = 0.25, 100.0, 100.0, 90.0, 0.2
    sd = s * math.sqrt(T)
    d1 = (math.log(F / K) + sd * sd / 2) / sd
    put = K * stats.norm.cdf(-(d1 - sd)) - F * stats.norm.cdf(-d1)
    assert res["coste_proteccion_pct"] == pytest.approx(math.exp(-0.02 * T) * put / S * 100, rel=1e-10)
    assert res["svi"]["sin_arbitraje_mariposa"]


def test_skew_metodo_svi_y_asimetria():
    d = fd._ctl_skew_svi()
    res, _ = _run("DER-SKEW-001", d, {"metodo": "SVI"})
    assert res["metodo"] == "SVI"
    assert res["rr_puntos"] == pytest.approx(res["svi"]["rr_puntos"], rel=1e-12)
    assert res["asimetria_neutral_riesgo"] < 0   # ρ < 0: sesgo bajista ⇒ asimetría negativa
    assert res["svi"]["rho"] == pytest.approx(-0.4, abs=1e-6)


# ------------------------------------------------------------------------------------------- DER-TERM-001
def test_term_valores_a_mano():
    d = fd._ctl_term(False)
    d["calendario_eventos"] = [{"nombre": "resultados", "vencimiento_meses": 3, "sigma_base": 0.20,
                                "fuente_sigma_base": "vencimientos que excluyen el evento"}]
    res, _ = _run("DER-TERM-001", d, {"vencimientos": [1, 2, 3]})
    t1, t3 = 1 / 12, 3 / 12
    w1, w3 = 0.25 ** 2 * t1, 0.22 ** 2 * t3
    assert res["sigma_por_vencimiento_pct"]["2"] == pytest.approx(math.sqrt((w1 + w3) / 2 / (2 / 12)) * 100, rel=1e-12)
    assert res["pendiente_puntos"] == pytest.approx(-3.0)
    assert res["ratio_1m_3m"] == pytest.approx(0.25 / 0.22) and res["estado"] == "INVERTIDA"
    assert res["eventos"][0]["movimiento_descontado_pct"] == pytest.approx(math.sqrt((0.22 ** 2 - 0.2 ** 2) * t3) * 100)
    fwd13 = math.sqrt((w3 - w1) / (t3 - t1)) * 100
    tramos = {(x["desde_meses"], x["hasta_meses"]): x["sigma_fwd_pct"] for x in res["sigma_fwd"]}
    w2 = (w1 + w3) / 2
    assert tramos[(1.0, 2.0)] == pytest.approx(math.sqrt((w2 - w1) / (1 / 12)) * 100, rel=1e-12)
    assert math.sqrt(((w2 - w1) + (w3 - w2)) / (t3 - t1)) * 100 == pytest.approx(fwd13)


def test_term_inversiones_historicas_a_mano():
    d = fd._ctl_term(True)
    n = len(d["historia_vol_1m"])
    h1 = [0.20] * n
    h1[10:15] = [0.25] * 5
    h1[100:103] = [0.25] * 3
    d.update(historia_vol_1m=h1, historia_vol_3m=[0.21] * n)
    res, _ = _run("DER-TERM-001", d)
    inv = res["inversiones_historicas"]
    assert inv["episodios"] == 2 and inv["duracion_media_sesiones"] == 4.0 and inv["duracion_max_sesiones"] == 5
    assert inv["frecuencia_pct"] == pytest.approx(8 / n * 100)
    assert res["estado"] == "PLANA"


# ------------------------------------------------------------------------------------------- DER-ROLL-001
def test_roll_a_mano_indice():
    d = fd._ctl_roll(False)
    d["futuros"] = [{"precio": 4020.0, "dias": 30}, {"precio": 4050.0, "dias": 120}]
    d["historia_carry"] = [0.02 + 0.001 * math.sin(i) for i in range(300)]
    res, lim = _run("DER-ROLL-001", d)
    assert res["roll_yield_pct"] == pytest.approx((4020 / 4050 - 1) * 365 / 90 * 100, rel=1e-12)
    assert res["vencimientos"][0]["base_puntos"] == pytest.approx(20.0)
    assert res["carry_implicito_pct"] == pytest.approx(math.log(4020 / 4000) / (30 / 365) * 100, rel=1e-12)
    assert res["vencimientos"][0]["dividendo_implicito_pct"] == pytest.approx(3.0 - res["carry_implicito_pct"])
    assert res["percentiles"]["carry"] is not None and res["percentiles"]["roll"] is None
    assert any("5 años" in x for x in lim)


def test_roll_divisa_bono_360_y_rol_spot():
    T = 90 / 360
    S = 1.10
    d = {"tipo_activo": "divisa", "tipo_financiacion": 0.04, "tipo_base": 0.02,
         "futuros": [{"precio": S * math.exp(0.02 * T), "dias": 90}, {"precio": S * math.exp(0.02 * 2 * T), "dias": 180}]}
    res, _ = _run("DER-ROLL-001", d, {"anualizacion": 360},
                  series_rol={"spot": pd.Series([1.0, S], index=pd.bdate_range("2024-01-01", periods=2))})
    assert res["spot"] == S
    assert res["carry_implicito_pct"] == pytest.approx(2.0, rel=1e-10)
    assert abs(res["desviacion_vs_teorico_pb"]) <= 1e-8
    b = {"tipo_activo": "bono", "tipo_financiacion": 0.03, "precio_entregable": 110.0, "factor_conversion": 0.9,
         "rendimiento_entregable": 0.04, "futuros": [{"precio": 122.5, "dias": 60}, {"precio": 122.8, "dias": 150}]}
    res, lim = _run("DER-ROLL-001", b)
    s_ef = 110.0 / 0.9
    carry = math.log(122.5 / s_ef) / (60 / 365)
    assert res["carry_implicito_pct"] == pytest.approx(carry * 100, rel=1e-12)
    assert res["carry_teorico_pct"] == pytest.approx(1.0)
    assert res["vencimientos"][0]["repo_implicito_pct"] == pytest.approx((0.04 - carry) * 100, rel=1e-12)
    assert any("opción de entrega" in x for x in res["advertencias"]) and not any("opción de entrega" in x for x in lim)


# ------------------------------------------------------------------------------------------- QA r01 · H-03
@pytest.mark.parametrize("ficha", FICHAS_TAREA)
def test_advertencias_fijas_van_en_el_resultado_no_en_limitaciones(ficha):
    res, lim = _run(ficha, _base(ficha))
    assert res["advertencias"][:len(fd.ADVERTENCIAS[ficha])] == fd.ADVERTENCIAS[ficha]
    assert not set(fd.ADVERTENCIAS[ficha]) & set(lim)


def _completos(ficha):
    """Datos «perfectos» (todas las entradas opcionales y la historia recomendada): sin limitaciones."""
    if ficha == "FON-DISC-001":
        d = fd._ctl_disc(iguales=False)
        n = 5 * 52 + 2
        d["fechas"] = fd._fechas_semanales(n)
        t = np.arange(n)
        for i, mb in enumerate(d["miembros"].values()):
            nav = 100 + t * 0.1
            mb.update(nav=list(nav), precio=list(nav * (1 - 0.08 + 0.03 * np.sin(t / 9 + i))), fecha_nav=d["fechas"][-1])
        d.update(rentabilidad_nav_supuesta=0.02, catalizadores=["recompras"])
        return d
    if ficha == "FON-TD-001":
        d = fd._ctl_td(False)
        for mb in d["miembros"].values():
            mb.update(replicacion="fisica", efecto_replicacion=0.0, efecto_caja=-0.0001)
        return d
    if ficha == "DER-VRP-001":
        d = fd._ctl_vrp(1.3)
        n = 5 * 252 + 30
        d["precios_subyacente"] = [100 * (1.01 if i % 2 else 1.0) for i in range(n)]
        d["vol_implicita"] = [d["vol_implicita"][0]] * n
        d["cesta_opciones"] = dict(fd._CTL_CESTA_RK)
        return d
    if ficha == "DER-SKEW-001":
        d = fd._ctl_skew_svi()
        d["historia_rr"] = d["historia_rr"] + d["historia_rr"][:10]
        return d
    if ficha == "DER-ROLL-001":
        d = fd._ctl_roll(False)
        d["historia_carry"] = [0.02] * (5 * 252)
        d["historia_roll"] = [-0.01] * (5 * 252)
        return d
    return _base(ficha)


@pytest.mark.parametrize("ficha", ["FON-DISC-001", "FON-FLOW-001", "FON-TD-001", "DER-VRP-001", "DER-SKEW-001",
                                   "DER-TERM-001", "DER-ROLL-001"])
def test_datos_completos_sin_limitaciones(ficha):
    res, lim = _run(ficha, _completos(ficha))
    assert lim == [], lim
    assert res["advertencias"]


def test_lev_solo_limita_el_paso_no_servido():
    _, lim = _run("FON-LEV-001", dict(fd._ctl_lev_mano(), rejilla_rendimiento=[-0.05, 0.0, 0.05]))
    assert len(lim) == 1 and "SIM-MC-001" in lim[0]


# ------------------------------------------------------------------------------------------- QA r01 · H-02 y H-11
RAROS = [None, "x", [], {}, float("nan"), float("inf"), float("-inf"), 0, -1, 1e300, True, -1e-300, [1, 2], {"a": 1}]


def _hojas(x, ruta=()):
    if isinstance(x, dict):
        for k in sorted(x, key=str):
            yield ruta + (k,)
            yield from _hojas(x[k], ruta + (k,))
    elif isinstance(x, list):
        for i in sorted({0, len(x) // 2, len(x) - 1}) if len(x) > 3 else range(len(x)):
            yield ruta + (i,)
            yield from _hojas(x[i], ruta + (i,))


def _poner(x, ruta, valor):
    y = copy.deepcopy(x)
    z = y
    for r in ruta[:-1]:
        z = z[r]
    z[ruta[-1]] = valor
    return y


@pytest.mark.parametrize("ficha,caso", CASOS, ids=[f"{f}:{c['nombre']}" for f, c in CASOS])
def test_fuzzer_entradas_mal_formadas_fallan_cerrado(ficha, caso):
    """Cada hoja de los datos del caso, mutada a un valor raro: o ErrorFicha o un resultado sin cifras no finitas."""
    base = {}
    for dd in caso["datos"]:
        base.update(copy.deepcopy(dd["valores"]))
    params = fd._p(ficha, caso.get("parametros"))
    for ruta in _hojas(base):
        for raro in RAROS:
            try:
                res, _ = _run(ficha, _poner(base, ruta, raro), params)
            except ErrorFicha:
                continue
            assert not fd._no_finitos(res), (ruta, raro)
            json.dumps(res, allow_nan=False)
    for k in sorted(params):
        for raro in RAROS:
            try:
                res, _ = _run(ficha, base, {**params, k: raro})
            except ErrorFicha:
                continue
            assert not fd._no_finitos(res), (k, raro)


@pytest.mark.parametrize("ficha,mut", [
    ("FON-DISC-001", lambda d: d["fechas"].__setitem__(0, 20200103)),
    ("FON-DISC-001", lambda d: d["miembros"]["M1"].update(fecha_nav=20231020)),
    ("FON-FLOW-001", lambda d: d.update(fechas=[20210131 + i for i in range(len(d["fechas"]))])),
    ("FON-LEV-001", lambda d: d["fechas"].__setitem__(5, 1e18)),
    ("DER-TERM-001", lambda d: d.update(calendario_eventos=[{"vencimiento_meses": 3, "sigma_base": 0.2,
                                                             "fecha": 20261110}])),
])
def test_fechas_numericas_rechazadas(ficha, mut):
    d = _base(ficha)
    mut(d)
    with pytest.raises(ErrorFicha, match="fecha"):
        _run(ficha, d)


def test_desbordes_y_tipos_dan_error_ficha():
    d = fd._ctl_lev(2.0)
    d["rentabilidades_indice"][0] = 1e300
    with pytest.raises(ErrorFicha, match="no finit|dominio"):
        _run("FON-LEV-001", d)
    d = fd._ctl_term(False)
    d["calendario_eventos"] = True
    with pytest.raises(ErrorFicha, match="calendario"):
        _run("DER-TERM-001", d)
    d = fd._ctl_flow(False)
    d["categorias"]["RF_activa"]["gestion"] = float("nan")
    with pytest.raises(ErrorFicha, match="gestion"):
        _run("FON-FLOW-001", d)
    d = fd._ctl_vrp(1.3)
    d["cesta_opciones"] = dict(fd._CTL_CESTA_RK, forward=1e300)
    with pytest.raises(ErrorFicha):
        _run("DER-VRP-001", d)
    with pytest.raises(ErrorFicha, match="numérico"):
        _run("DER-ROLL-001", dict(fd._ctl_roll(False), spot="4000"))
    with pytest.raises(ErrorFicha, match="numérico"):
        _run("FON-LEV-001", dict(fd._ctl_lev(2.0), L=True))


# ------------------------------------------------------------------------------------------- QA r01 · H-08
def test_svi_con_arbitraje_rechazado_por_metodo_svi():
    with pytest.raises(ErrorFicha, match="arbitraje de mariposa"):
        _run("DER-SKEW-001", fd._ctl_skew_arbitraje(), {"metodo": "SVI"})
    _, lim = _run("DER-SKEW-001", fd._ctl_skew_arbitraje())
    assert any("arbitraje de mariposa" in x for x in lim)


def test_disc_kappa_y_su_complementaria_difieren():
    r1, _ = _run("FON-DISC-001", fd._ctl_disc_kappa(), {"kappa": 0.25})
    r2, _ = _run("FON-DISC-001", fd._ctl_disc_kappa(), {"kappa": 0.75})
    assert r1["rentabilidad_normalizacion_pct"] == pytest.approx(fd._ctl_disc_kappa_esperado(), rel=1e-10)
    assert r2["rentabilidad_normalizacion_pct"] != pytest.approx(r1["rentabilidad_normalizacion_pct"])


def test_roll_descomposicion_frente_a_total_publicado():
    d = fd._ctl_roll(False)
    d["periodo"]["total_publicado"] = (4105 / 4010 - 1) + 0.03 * 30 / 365
    res, _ = _run("DER-ROLL-001", d)
    assert abs(res["descomposicion"]["suma_componentes_menos_publicado_pp"]) <= 1e-10
    assert res["descomposicion"]["colateral_pct"] == pytest.approx(0.03 * 30 / 365 * 100)
