"""T-112 · Motor Fase 2, grupo P: fichas REI-CAP-001, REI-FFO-001, REI-NAV-001, CMD-INV-001, CMD-RETDEC-001,
CHR-FLOW-001, CHR-FUND-001 y ALT-DESMOOTH-001 del Catálogo V5.0.

Casos de control («Verificación»), rechazos de «Aclaración y rechazo» y de «Entradas mínimas», dominio de cada
parámetro, umbrales fijos, determinismo, entradas hostiles y oráculos independientes: cada oráculo recalcula el
resultado por otra vía (pandas, scipy, fracciones exactas, filtros lineales) sin llamar al código de la ficha."""
import copy
import itertools
import json
import math
import statistics
from fractions import Fraction

import numpy as np
import pandas as pd
import pytest
from bloque_a.motor import fichas_reales as fr
from bloque_a.motor.operaciones import ErrorFicha
from scipy import signal, stats

FICHAS_P = ["REI-CAP-001", "REI-FFO-001", "REI-NAV-001", "CMD-INV-001", "CMD-RETDEC-001", "CHR-FLOW-001",
            "CHR-FUND-001", "ALT-DESMOOTH-001"]


def _ent(valores, series_rol=None):
    return {"valores": copy.deepcopy(valores), "series": {}, "series_rol": series_rol or {}}


def _correr(ficha, valores, params=None, series_rol=None):
    return fr.FICHAS[ficha]["fn"](_ent(valores, series_rol), dict(params or {}))


def _valores_caso(caso):
    v = {}
    for d in caso["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    return v


def _base(ficha):
    caso = fr.CASOS_CONTROL[ficha][0]
    return _valores_caso(caso), dict(caso["parametros"])


CASOS = [(f, c) for f, casos in fr.CASOS_CONTROL.items() for c in casos]
IDS = [f"{f}:{c['nombre'][:60]}" for f, c in CASOS]


# ============================================================================= registro
def test_registro_de_las_ocho_fichas():
    for tabla in (fr.FICHAS, fr.PARAMETROS_POR_DEFECTO, fr.UMBRALES, fr.ADVERTENCIAS, fr.CASOS_CONTROL):
        assert sorted(tabla) == sorted(FICHAS_P)
    modulos = {"CMD-INV-001": "MC-02", "CHR-FLOW-001": "MC-02"}
    for f, meta in fr.FICHAS.items():
        assert set(meta) == {"fn", "modulo", "version", "cifra", "ri", "tol"} and callable(meta["fn"])
        assert meta["modulo"] == modulos.get(f, "MC-09") and meta["version"] == "1.0"
        assert meta["cifra"] in ("DETERMINISTA", "ESTADISTICA") and meta["ri"]
        assert meta["tol"] == (1e-8 if f == "ALT-DESMOOTH-001" else 1e-10)       # «Tolerancias y semilla»
    assert fr.FICHAS["CMD-RETDEC-001"]["cifra"] == "DETERMINISTA"
    assert fr.FICHAS["CMD-INV-001"]["ri"] == "RI-EST" and fr.FICHAS["CHR-FUND-001"]["ri"] == "RI-PA"


def test_parametros_por_defecto_salen_de_la_ficha():
    P = fr.PARAMETROS_POR_DEFECTO
    assert P["REI-CAP-001"] == {"base_noi": "adelantado", "ventana": 20}
    assert P["REI-NAV-001"] == {"nav_variante": "EPRA NTA", "cap_objetivo": None}
    assert P["CMD-INV-001"] == {"anos_estacional": 5, "excluir_anos": []}
    assert P["CMD-RETDEC-001"] == {"calendario_roll": "indice", "frecuencia": "mensual"}
    assert P["CHR-FLOW-001"] == {"ventanas": [5, 20], "ventana_z": 1}
    assert P["CHR-FUND-001"] == {"ponderacion": "interes_abierto", "ventana_percentil": 365}
    assert P["ALT-DESMOOTH-001"] == {"metodo": "Geltner", "k": 2, "phi": None}
    U = fr.UMBRALES
    assert U["REI-CAP-001"]["anios_historia_minimos"] == 15 and U["REI-NAV-001"]["meses_antiguedad_nav_max"] == 12
    assert U["REI-FFO-001"]["ejercicios_minimos"] == 3 and U["CMD-INV-001"]["anios_rechazo"] == 3
    assert U["CHR-FLOW-001"]["dias_minimos"] == 120 and U["CHR-FUND-001"]["dias_minimos"] == 90
    assert U["CHR-FUND-001"]["plataformas_minimas"] == 2 and U["ALT-DESMOOTH-001"]["observaciones_minimas"] == 24


# ============================================================================= casos de control
@pytest.mark.parametrize("ficha,caso", CASOS, ids=IDS)
def test_casos_de_control(ficha, caso):
    res, lim = _correr(ficha, _valores_caso(caso), caso["parametros"])
    assert caso["comprobar"](res)
    json.dumps(res, allow_nan=False)
    assert res["advertencias"] == fr.ADVERTENCIAS[ficha]
    assert all(isinstance(x, str) for x in lim) and not set(lim) & set(fr.ADVERTENCIAS[ficha])


def _perturbar(x):
    if isinstance(x, dict):
        return {k: _perturbar(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_perturbar(v) for v in x]
    if isinstance(x, float):
        return x + max(abs(x), 1.0) * 1e-6
    return x


@pytest.mark.parametrize("ficha,caso", CASOS, ids=IDS)
def test_cada_caso_de_control_puede_fallar(ficha, caso):
    """Un caso que no puede fallar no cuenta (T-106, H-08): con las cifras movidas una millonésima, falla."""
    res, _ = _correr(ficha, _valores_caso(caso), caso["parametros"])
    assert not caso["comprobar"](_perturbar(res))


@pytest.mark.parametrize("ficha", FICHAS_P)
def test_al_menos_dos_casos_de_control_por_ficha(ficha):
    assert len(fr.CASOS_CONTROL[ficha]) >= 2


# ============================================================================= determinismo y no mutación
@pytest.mark.parametrize("ficha,caso", CASOS, ids=IDS)
def test_determinismo_dos_pasadas(ficha, caso):
    v = _valores_caso(caso)
    a = json.dumps(_correr(ficha, v, caso["parametros"]), sort_keys=True, allow_nan=False)
    b = json.dumps(_correr(ficha, v, caso["parametros"]), sort_keys=True, allow_nan=False)
    assert a == b


@pytest.mark.parametrize("ficha", FICHAS_P)
def test_no_modifica_la_entrada(ficha):
    v, p = _base(ficha)
    ent = _ent(v)
    antes = json.dumps(ent["valores"], sort_keys=True)
    params = dict(p)
    fr.FICHAS[ficha]["fn"](ent, params)
    assert json.dumps(ent["valores"], sort_keys=True) == antes and params == p


# ============================================================================= umbrales fijos y dominio de parámetros
@pytest.mark.parametrize("ficha,umbral", [(f, k) for f in FICHAS_P for k in fr.UMBRALES[f]])
def test_ningun_umbral_se_cambia_desde_la_peticion(ficha, umbral):
    v, p = _base(ficha)
    valor = fr.UMBRALES[ficha][umbral]
    with pytest.raises(ErrorFicha, match="umbrales fijos"):
        _correr(ficha, v, {**p, umbral: valor})


DOMINIO_MALO = [
    ("REI-CAP-001", "base_noi", ["mixta", 3, True]), ("REI-CAP-001", "ventana", [14, 0, -5, 20.5, "20", True, math.nan]),
    ("REI-FFO-001", "capex_mantenimiento", ["calculado", 1]),
    ("REI-FFO-001", "capex_pct_rentas", [-0.01, 1.0, 1.5, "0,1", math.inf]),
    ("REI-NAV-001", "nav_variante", ["IFRS", 1]), ("REI-NAV-001", "cap_objetivo", [0, 1, -0.05, 1.2, "0,05", math.nan]),
    ("CMD-INV-001", "anos_estacional", [2, 11, 4.5, "5", True]),
    ("CMD-INV-001", "excluir_anos", [2020, [2020, 2020], ["2020"], [2020.5], [0]]),
    ("CMD-RETDEC-001", "calendario_roll", ["propio", 1]), ("CMD-RETDEC-001", "frecuencia", ["diaria", "semanal", 12]),
    ("CHR-FLOW-001", "ventanas", [[], [0], [5, 5], [2.5], 5, ["5"]]), ("CHR-FLOW-001", "ventana_z", [0, 0.5, -1, "1"]),
    ("CHR-FUND-001", "ponderacion", ["capitalizacion", 0]),
    ("CHR-FUND-001", "ventana_percentil", [364, 30, 365.5, "365", math.inf]),
    ("ALT-DESMOOTH-001", "metodo", ["Okunev", 1]), ("ALT-DESMOOTH-001", "k", [0, 4, 1.5, "2", True]),
    ("ALT-DESMOOTH-001", "phi", [-0.1, 1.0, 1.2, "0,4", math.nan]),
]


@pytest.mark.parametrize("ficha,param,malo", [(f, k, m) for f, k, ms in DOMINIO_MALO for m in ms])
def test_dominio_de_cada_parametro(ficha, param, malo):
    v, p = _base(ficha)
    with pytest.raises(ErrorFicha):
        _correr(ficha, v, {**p, param: malo})


@pytest.mark.parametrize("ficha,params", [
    ("REI-CAP-001", {"ventana": 15}), ("REI-CAP-001", {"ventana": 40}),
    ("REI-NAV-001", {"cap_objetivo": 0.0451}), ("CMD-INV-001", {"anos_estacional": 3}),
    ("CMD-INV-001", {"anos_estacional": 10}), ("CHR-FLOW-001", {"ventanas": [1, 7, 30], "ventana_z": 2}),
    ("CHR-FUND-001", {"ponderacion": "igual", "ventana_percentil": 500}),
    ("ALT-DESMOOTH-001", {"phi": 0.999}), ("ALT-DESMOOTH-001", {"k": 1}), ("ALT-DESMOOTH-001", {"k": 3}),
])
def test_valores_admitidos_de_los_parametros(ficha, params):
    v, p = _base(ficha)
    p = {k: x for k, x in p.items() if k not in params}
    res, _ = _correr(ficha, v, {**p, **params})
    json.dumps(res, allow_nan=False)


def test_phi_fijado_solo_con_geltner():
    v, _ = _base("ALT-DESMOOTH-001")
    with pytest.raises(ErrorFicha, match="solo se admite con el método Geltner"):
        _correr("ALT-DESMOOTH-001", v, {"metodo": "GLM", "phi": 0.3})


def test_claves_desconocidas_de_la_peticion_se_ignoran():
    v, p = _base("REI-CAP-001")
    a = _correr("REI-CAP-001", v, p)
    b = _correr("REI-CAP-001", v, {**p, "clase": "REI"})
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


# ============================================================================= entradas hostiles
@pytest.mark.parametrize("ficha", FICHAS_P)
@pytest.mark.parametrize("ent", [None, [], "x", {}, {"valores": None}, {"valores": []}, {"valores": {}}])
def test_entradas_vacias_o_mal_formadas(ficha, ent):
    with pytest.raises(ErrorFicha):
        fr.FICHAS[ficha]["fn"](ent, {})


@pytest.mark.parametrize("ficha", FICHAS_P)
@pytest.mark.parametrize("params", [[], "x", 3])
def test_parametros_que_no_son_un_dict(ficha, params):
    v, _ = _base(ficha)
    with pytest.raises(ErrorFicha):
        fr.FICHAS[ficha]["fn"](_ent(v), params)


def _hojas(x, ruta=()):
    if isinstance(x, dict):
        for k in sorted(x, key=str):
            yield from _hojas(x[k], ruta + (k,))
    elif isinstance(x, list):
        for i, e in enumerate(x):
            yield from _hojas(e, ruta + (i,))
    else:
        yield ruta, x


def _poner(v, ruta, valor):
    d = v
    for k in ruta[:-1]:
        d = d[k]
    d[ruta[-1]] = valor


HOSTILES = [math.nan, math.inf, -math.inf, "texto", True, None, [1.0], {"valor": 1.0}]


@pytest.mark.parametrize("ficha,caso", CASOS, ids=IDS)
def test_cada_hoja_hostil_rechaza_o_da_cifras_finitas(ficha, caso):
    """Cualquier dato hostil en cualquier hoja (muestra fija de hojas): o ErrorFicha o un resultado finito y serializable;
    nunca otra excepción ni un NaN/inf en el resultado."""
    v = _valores_caso(caso)
    hojas = [r for r, x in _hojas(v) if not isinstance(x, str) or r[-1] in ("fecha", "fecha_publicacion", "fecha_nav")]
    paso = max(1, len(hojas) // 25)
    for ruta in hojas[::paso]:
        for malo in HOSTILES:
            w = copy.deepcopy(v)
            _poner(w, ruta, malo)
            try:
                res, _ = _correr(ficha, w, caso["parametros"])
            except ErrorFicha:
                continue
            json.dumps(res, allow_nan=False)


@pytest.mark.parametrize("ficha,ruta", [
    ("REI-CAP-001", ("noi", "valor")), ("REI-CAP-001", ("valor_tasacion",)), ("REI-CAP-001", ("soberano_10a", "rendimiento")),
    ("REI-CAP-001", ("historia", 3, "cap_rate")), ("REI-NAV-001", ("componentes", 0, "precio")),
    ("REI-NAV-001", ("componentes", 1, "gav")), ("REI-FFO-001", ("componentes", 0, "ejercicios", 2, "beneficio_neto")),
    ("REI-FFO-001", ("componentes", 1, "precio")), ("CMD-INV-001", ("inventarios", "observaciones", 50, "valor")),
    ("CMD-RETDEC-001", ("indices", "exceso", 4)), ("CMD-RETDEC-001", ("tipo_colateral", 2)),
    ("CHR-FUND-001", ("plataformas", "P2", "historia", 10, "tasa")), ("CHR-FUND-001", ("spot", 399, "precio")),
    ("CHR-FLOW-001", ("flujos_etf", 100, "flujo")), ("CHR-FLOW-001", ("oferta_stablecoins", "USDX", 3, "oferta")),
    ("ALT-DESMOOTH-001", ("rentabilidades", 7, "r")),
])
@pytest.mark.parametrize("malo", [math.nan, math.inf, "1,5", True, None])
def test_dato_requerido_hostil_se_rechaza(ficha, ruta, malo):
    v, p = _base(ficha)
    _poner(v, ruta, malo)
    with pytest.raises(ErrorFicha):
        _correr(ficha, v, p)


@pytest.mark.parametrize("ficha", FICHAS_P)
def test_fechas_ilegibles_o_numericas_se_rechazan(ficha):
    v, p = _base(ficha)
    rutas = [r for r, x in _hojas(v) if r and r[-1] in ("fecha", "fecha_precio", "fechas") or
             (len(r) > 1 and r[-2] == "fechas")]
    assert rutas
    for malo in ("2024-13-45", 20240131, "", None):
        w = copy.deepcopy(v)
        _poner(w, rutas[len(rutas) // 2], malo)
        with pytest.raises(ErrorFicha):
            _correr(ficha, w, p)


# ============================================================================= REI-CAP-001
def _cap():
    return fr._datos_rei_cap()


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v["noi"].pop("base"), "base del NOI es ambigua"),
    (lambda v: v["noi"].update(base="mixta"), "base del NOI es ambigua"),
    (lambda v: v["noi"].update(base="historico"), "pide la base"),
    (lambda v: v["noi"].pop("definicion"), "definición del NOI"),
    (lambda v: v["noi"].update(definicion="bruto"), "no admitido"),
    (lambda v: v.update(historia=v["historia"][-14 * 4:]), "entradas mínimas"),
    (lambda v: v["soberano_10a"].update(moneda="USD"), "misma moneda"),
    (lambda v: v["equilibrio"].update(r=0.018), "r > g_NOI"),
    (lambda v: v["valor_mercado_implicito"].update(deuda_neta=-7e8), "no positivo"),
    (lambda v: v["noi"].update(valor=0), "NOI"),
    (lambda v: v.update(historia=v["historia"] + [v["historia"][-1]]), "fechas repetidas"),
])
def test_rei_cap_rechazos(cambio, motivo):
    v = _cap()
    cambio(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _correr("REI-CAP-001", v)


def test_rei_cap_historico_con_peticion_historica_y_opcionales_ausentes():
    v = _cap()
    v["noi"]["base"] = "historico"
    for k in ("valor_mercado_implicito", "equilibrio"):
        v.pop(k)
    res, lim = _correr("REI-CAP-001", v, {"base_noi": "historico"})
    assert res["cap_rate_mercado_pct"] is None and res["cap_equilibrio_pct"] is None
    assert any("mercado implícito" in x for x in lim) and any("equilibrio" in x for x in lim)


def test_rei_cap_oraculo_independiente():
    """Fracciones exactas para el cap rate y el diferencial; scipy y statistics para la posición en la ventana."""
    v = _cap()
    res, _ = _correr("REI-CAP-001", v, {"ventana": 15})
    cap = Fraction(52_500_000) / Fraction(1_050_000_000)
    assert res["cap_rate_tasacion_pct"] == pytest.approx(float(cap * 100), rel=1e-14)
    assert res["diferencial_pb"] == pytest.approx(float((cap - Fraction("0.031")) * 10_000), rel=1e-12)
    ultima = pd.Timestamp(v["historia"][-1]["fecha"]).to_pydatetime()
    corte = ultima.replace(year=ultima.year - 15)
    h = [(x["cap_rate"] - x["soberano_10a"]) * 1e4 for x in v["historia"]
         if pd.Timestamp(x["fecha"]).to_pydatetime() > corte]
    x = res["diferencial_pb"]
    assert res["percentil"] == pytest.approx(stats.percentileofscore(h, x, kind="weak") / 100, abs=1e-15)
    assert res["z"] == pytest.approx((x - statistics.fmean(h)) / statistics.stdev(h), rel=1e-10)
    assert res["n_historia"] == len(h)


def test_rei_cap_z_indefinido_con_historia_constante():
    v = _cap()
    for h in v["historia"]:
        h.update(cap_rate=0.05, soberano_10a=0.03)
    res, lim = _correr("REI-CAP-001", v)
    assert res["z"] is None and any("sin dispersión" in x for x in lim)


# ============================================================================= REI-NAV-001
def _nav(misma=False):
    return fr._datos_rei_nav(misma)


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v["componentes"][0].update(fecha_nav="2025-09-29"), "antigüedad > 12 meses"),
    (lambda v: v["componentes"][0].update(fecha_nav="2026-10-01"), "no conocible"),
    (lambda v: v["componentes"][1].update(variante_nav="EPRA NRV"), "no se mezclan variantes"),
    (lambda v: v["componentes"][1].pop("variante_nav"), "sin declarar"),
    (lambda v: v["componentes"][0].update(otros_pasivos=0.25e9), "NAV ≠ GAV"),
    (lambda v: v["componentes"][1].update(fecha_precio="2026-09-29"), "misma fecha de precio"),
    (lambda v: v["componentes"][1].update(id="A"), "repetido"),
    (lambda v: v["componentes"][0].update(cap_rate_tasacion=0), "cap_rate_tasacion"),
    (lambda v: v.update(componentes=[]), "lista no vacía"),
])
def test_rei_nav_rechazos(cambio, motivo):
    v = _nav()
    cambio(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _correr("REI-NAV-001", v, {"cap_objetivo": 0.05})


def test_rei_nav_doce_meses_justos_se_admiten_y_otros_pasivos_derivados_se_declaran():
    v = _nav()
    v["componentes"][0]["fecha_nav"] = "2025-09-30"
    del v["componentes"][1]["otros_pasivos"]
    res, lim = _correr("REI-NAV-001", v, {"cap_objetivo": 0.05})
    assert res["componentes"]["A"]["antiguedad_nav_dias"] == 365
    assert any("derivados por diferencia" in x for x in lim)


def test_rei_nav_historia_corta_no_da_percentil():
    v = _nav()
    v["historia_prima"] = v["historia_prima"][-30:]
    res, lim = _correr("REI-NAV-001", v)
    assert res["percentil"] is None and any("< 10 años" in x for x in lim)


def test_rei_nav_oraculo_independiente():
    """np.average con pesos de capitalización y fracciones exactas para el NAV ajustado."""
    res, _ = _correr("REI-NAV-001", _nav(), {"cap_objetivo": 0.055})
    caps = [18.0 * 1e8, 31.5 * 5e7]
    pr = [18 / 20 - 1, 31.5 / 30 - 1]
    m = np.average(pr, weights=caps)
    assert res["prima_agregada_pct"] == pytest.approx(m * 100, rel=1e-12)
    assert res["dispersion_pct"] == pytest.approx(math.sqrt(np.average((np.array(pr) - m) ** 2, weights=caps)) * 100,
                                                   rel=1e-12)
    adj = (Fraction(3_200_000_000) * Fraction(5, 100) / Fraction(55, 1000) - 1_200_000_000
           + Fraction(2_400_000_000) * Fraction(45, 1000) / Fraction(55, 1000) - 900_000_000)
    assert res["nav_ajustado"]["variacion_pct"] == pytest.approx(float((adj / 3_500_000_000 - 1) * 100), rel=1e-12)
    assert res["rango_pct"] == pytest.approx([-10.0, 5.0], rel=1e-12)


# ============================================================================= REI-FFO-001
def _ffo(**kw):
    return fr._datos_rei_ffo(**kw)


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v["componentes"][0]["ejercicios"][1].pop("amortizaciones_inmobiliarias"), "amortizaciones inmobiliarias"),
    (lambda v: v["componentes"][0]["ejercicios"][1].update(
        amortizaciones=v["componentes"][0]["ejercicios"][1].pop("amortizaciones_inmobiliarias")), "desglosadas"),
    (lambda v: v["componentes"][2].update(ejercicios=v["componentes"][2]["ejercicios"][1:]), "entradas mínimas"),
    (lambda v: v["componentes"][1]["ejercicios"][0].pop("dividendo"), "dividendo"),
    (lambda v: v["componentes"][1]["ejercicios"][0].pop("ajuste_rentas_lineales"), "ajuste_rentas_lineales"),
    (lambda v: v["componentes"][1]["ejercicios"][0].update(capex_mantenimiento=None), "capex_pct_rentas"),
    (lambda v: v["componentes"][1]["ejercicios"][2].update(ejercicio=2024), "repetido"),
    (lambda v: v["componentes"][1].update(id="X"), "repetido"),
    (lambda v: v["componentes"][0].pop("precio"), "precio"),
    (lambda v: v["componentes"][0]["ejercicios"][0].update(amortizaciones_inmobiliarias=-1.0), "amortizaciones"),
])
def test_rei_ffo_rechazos(cambio, motivo):
    v = _ffo()
    cambio(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _correr("REI-FFO-001", v)


def test_rei_ffo_capex_estimado_para_todos_y_ffo_negativo():
    v = _ffo()
    for c in v["componentes"]:
        for e in c["ejercicios"]:
            e["rentas"] = 100e6
    res, lim = _correr("REI-FFO-001", v, {"capex_mantenimiento": "estimado", "capex_pct_rentas": 0.1})
    x25 = v["componentes"][0]["ejercicios"][2]
    assert res["serie"]["2025"]["affo"] == pytest.approx(
        sum(e["beneficio_neto"] + e["amortizaciones_inmobiliarias"] - e["plusvalias"] - 10e6 - e["ajuste_rentas_lineales"]
            for c in v["componentes"] for e in c["ejercicios"] if e["ejercicio"] == 2025), rel=1e-12)
    assert x25["capex_mantenimiento"] == 10e6 and any("estimado" in x for x in lim)
    w = _ffo()
    for c in w["componentes"]:
        for e in c["ejercicios"]:
            e["beneficio_neto"] = -200e6
    res2, lim2 = _correr("REI-FFO-001", w)
    assert res2["p_ffo"] is None and res2["p_affo"] is None and any("no positivo" in x for x in lim2)


def test_rei_ffo_oraculo_independiente():
    """pandas (tabla larga + groupby) para FFO/AFFO, statistics.median y percentileofscore para los múltiplos."""
    v = _ffo()
    res, _ = _correr("REI-FFO-001", v)
    filas = [{"id": c["id"], "cap": c["precio"] * c["acciones"], **e} for c in v["componentes"] for e in c["ejercicios"]]
    df = pd.DataFrame(filas)
    df["ffo"] = df.beneficio_neto + df.amortizaciones_inmobiliarias - df.plusvalias
    df["affo"] = df.ffo - df.capex_mantenimiento - df.ajuste_rentas_lineales
    g = df.groupby("ejercicio")[["ffo", "affo"]].sum()
    for anio, fila in g.iterrows():
        assert res["serie"][str(anio)]["ffo"] == pytest.approx(fila.ffo, rel=1e-13)
        assert res["serie"][str(anio)]["affo"] == pytest.approx(fila.affo, rel=1e-13)
    ult = df[df.ejercicio == 2025]
    cap = float(ult.cap.sum())
    assert res["p_ffo"] == pytest.approx(cap / float(ult.ffo.sum()), rel=1e-13)
    cob = list(ult.affo / ult.dividendo)
    assert res["cobertura"]["mediana"] == pytest.approx(statistics.median(cob), rel=1e-13)
    assert res["cobertura"]["iqr"] == pytest.approx(float(pd.Series(cob).quantile(0.75) - pd.Series(cob).quantile(0.25)),
                                                    rel=1e-12)
    hist = [h["p_ffo"] for h in v["historia_multiplos"]]
    assert res["percentil_p_ffo"] == pytest.approx(stats.percentileofscore(hist, res["p_ffo"], kind="weak") / 100)


# ============================================================================= CMD-INV-001
def _inv(periodica=False):
    return fr._datos_cmd_inv(periodica)


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v["inventarios"].update(observaciones=v["inventarios"]["observaciones"][-35:]), "rechazo con"),
    (lambda v: v["inventarios"]["observaciones"][10].pop("fecha_publicacion"), "sin fecha de publicación"),
    (lambda v: v["inventarios"]["observaciones"][10].update(fecha_publicacion="2017-01-01"), "publicada antes"),
    (lambda v: v["inventarios"]["observaciones"][10].update(fecha="2017-10-15"), "mismo periodo"),
    (lambda v: v["inventarios"].update(frecuencia="diaria"), "no admitido"),
    (lambda v: v["inventarios"].pop("unidad"), "unidad"),
    (lambda v: v["inventarios"]["observaciones"][10].update(valor=-1.0), "mínimo"),
    (lambda v: v["demanda_diaria"].pop("fuente"), "fuente"),
])
def test_cmd_inv_rechazos(cambio, motivo):
    v = _inv()
    cambio(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _correr("CMD-INV-001", v)


def test_cmd_inv_anio_actual_excluido_y_pocos_anios_previos():
    with pytest.raises(ErrorFicha, match="año de la observación actual"):
        _correr("CMD-INV-001", _inv(), {"excluir_anos": [2024]})
    with pytest.raises(ErrorFicha, match="años previos con el mismo periodo < 3"):
        _correr("CMD-INV-001", _inv(), {"anos_estacional": 3, "excluir_anos": [2022]})


def test_cmd_inv_entre_tres_y_cinco_anios_es_limitacion():
    v = _inv()
    v["inventarios"]["observaciones"] = v["inventarios"]["observaciones"][-49:]
    res, lim = _correr("CMD-INV-001", v, {"anos_estacional": 3})
    assert any("entrada mínima de 5" in x for x in lim) and res["anios_referencia"] == 3


def test_cmd_inv_oraculo_independiente_y_segunda_via():
    """pandas: filtro por mes y año para la media estacional; 2×12 con rolling para la segunda vía (FX-STL-001)."""
    v = _inv()
    res, _ = _correr("CMD-INV-001", v)
    s = pd.Series({pd.Timestamp(o["fecha"]): o["valor"] for o in v["inventarios"]["observaciones"]})
    ref = s[(s.index.month == 12) & (s.index.year >= 2019) & (s.index.year <= 2023)]
    x = s.iloc[-1]
    assert res["media_estacional"] == pytest.approx(ref.mean(), rel=1e-13)
    assert res["z"] == pytest.approx((x - ref.mean()) / ref.std(), rel=1e-12)
    assert res["dias_cobertura"] == pytest.approx(x / fr._INV_DEMANDA, rel=1e-13)
    tendencia = s.rolling(12).mean().rolling(2).mean().shift(-6)            # media móvil centrada 2×12
    d = (s - tendencia)[(s.index.year >= 2019) & (s.index.year <= 2023)].dropna()
    indice = d.groupby(d.index.month).mean()
    indice = indice - indice.mean()
    esperado = tendencia.dropna().iloc[-1] + indice.loc[12]
    assert res["segunda_via"]["nivel_esperado"] == pytest.approx(esperado, rel=1e-12)
    assert res["segunda_via"]["desviacion"] == pytest.approx(x - esperado, rel=1e-9)


def test_cmd_inv_semanal_relacion_con_la_curva_y_semana_53():
    fechas = pd.date_range("2015-01-08", "2021-01-07", freq="7D")       # 2015 y 2020 tienen semana ISO 53
    obs = [{"fecha": d.date().isoformat(), "fecha_publicacion": (d + pd.Timedelta(days=5)).date().isoformat(),
            "valor": 400 + 30 * math.sin(2 * math.pi * d.isocalendar()[1] / 52) + 0.05 * i + (i * 7 % 13)}
           for i, d in enumerate(fechas)]
    pend = [{"fecha": o["fecha"], "pendiente": 0.3 + 0.01 * ((i * 5) % 17)} for i, o in enumerate(obs)]
    res, lim = _correr("CMD-INV-001", {"inventarios": {"frecuencia": "semanal", "unidad": "Mbbl", "observaciones": obs},
                                       "pendiente_curva": pend}, {"anos_estacional": 3})
    json.dumps(res, allow_nan=False)
    assert res["relacion_pendiente_curva"]["n"] == len(res["serie_desviacion"]) > 5
    a = [s["desviacion_pct"] for s in res["serie_desviacion"]]
    b = [p["pendiente"] for p in pend if p["fecha"] in {s["fecha"] for s in res["serie_desviacion"]}]
    assert res["relacion_pendiente_curva"]["correlacion"] == pytest.approx(stats.pearsonr(a, b)[0], rel=1e-10)
    assert res["segunda_via"] is not None and res["dias_cobertura"] is None
    assert any("demanda diaria" in x for x in lim)


def test_cmd_inv_huecos_sin_segunda_via():
    v = _inv()
    del v["inventarios"]["observaciones"][40]
    res, lim = _correr("CMD-INV-001", v)
    assert res["segunda_via"] is None and any("segunda vía" in x for x in lim)


# ============================================================================= CMD-RETDEC-001
@pytest.mark.parametrize("cambio,params,motivo", [
    (lambda v: v["indices"].pop("calendario_roll"), {}, "sin calendario de roll"),
    (lambda v: v["indices"].update(calendario_roll="  "), {}, "sin calendario de roll"),
    (lambda v: v.pop("indices"), {}, "faltan los índices"),
    (lambda v: v["indices"]["fechas"].pop(5), {}, "elementos|consecutivos"),
    (lambda v: v["indices"]["fechas"].__setitem__(5, "2024-07-31"), {}, "consecutivos"),
    (lambda v: v["indices"]["spot"].pop(), {}, "alineados"),
    (lambda v: v["tipo_colateral"].pop(), {}, "alineados"),
    (lambda v: v["indices"]["total"].__setitem__(3, 0.0), {}, "mínimo"),
    (lambda v: None, {"frecuencia": "trimestral"}, "consecutivos"),
])
def test_cmd_retdec_rechazos_modo_indice(cambio, params, motivo):
    v = fr._datos_cmd_retdec_indice()
    cambio(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _correr("CMD-RETDEC-001", v, params)


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v["contratos"].pop("calendario_roll"), "sin calendario de roll"),
    (lambda v: v["contratos"].update(calendario_roll=[]), "sin calendario de roll"),
    (lambda v: v["contratos"]["precios"]["F2"].__setitem__(3, None), "falta el precio"),
    (lambda v: v["contratos"]["calendario_roll"][0].update(desde="2024-02-29"), "no cubre la primera fecha"),
    (lambda v: v["contratos"]["calendario_roll"][1].update(contrato="F9"), "sin precios"),
    (lambda v: v["contratos"]["calendario_roll"][1].update(desde="2024-01-31"), "fechas repetidas"),
    (lambda v: v.pop("contratos"), "faltan los precios"),
])
def test_cmd_retdec_rechazos_modo_contratos(cambio, motivo):
    v = fr._datos_cmd_retdec_contratos()
    cambio(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _correr("CMD-RETDEC-001", v, {"calendario_roll": "declarado"})


def test_cmd_retdec_oraculo_independiente():
    """pandas pct_change para los componentes; FIN-CAGR-001 por logaritmos para el total compuesto."""
    v = fr._datos_cmd_retdec_indice()
    v["indice_amplio"] = [100 * 1.004 ** i for i in range(len(v["indices"]["fechas"]))]
    res, lim = _correr("CMD-RETDEC-001", v)
    df = pd.DataFrame({k: v["indices"][k] for k in ("spot", "exceso", "total")}).pct_change().dropna()
    c = res["componentes_pct_anual"]
    assert c["spot"] == pytest.approx(df.spot.mean() * 1200, rel=1e-12)
    assert c["roll"] == pytest.approx((df.exceso - df.spot).mean() * 1200, rel=1e-12)
    assert c["colateral"] == pytest.approx((df.total - df.exceso).mean() * 1200, rel=1e-12)
    anios = len(df) / 12
    assert res["total_compuesto_pct_anual"] == pytest.approx(
        (math.exp(math.log(v["indices"]["total"][-1] / v["indices"]["total"][0]) / anios) - 1) * 100, rel=1e-10)
    assert res["referencia_ingenua"]["indice_amplio_pct_anual"] == pytest.approx(0.4 * 12, rel=1e-10)
    assert not any("RI-CM" in x for x in lim)


def test_cmd_retdec_trimestral():
    fechas = pd.date_range("2022-03-31", periods=9, freq="QE")
    v = {"indices": {"calendario_roll": "trimestral sintético", "fechas": [d.date().isoformat() for d in fechas],
                     "spot": [100 + 2 * i for i in range(9)], "exceso": [100 + 1.5 * i for i in range(9)],
                     "total": [100 + 2.5 * i for i in range(9)]}, "tipo_colateral": [0.02] * 9}
    res, _ = _correr("CMD-RETDEC-001", v, {"frecuencia": "trimestral"})
    s = pd.Series(v["indices"]["spot"]).pct_change().dropna()
    assert res["componentes_pct_anual"]["spot"] == pytest.approx(s.mean() * 400, rel=1e-12) and res["anios"] == 2


# ============================================================================= CHR-FUND-001
def _fund(coherente=False):
    return fr._datos_chr_fund(coherente)


def _recortar_fund(v, n):
    for p in v["plataformas"].values():
        p["historia"] = p["historia"][-n:]
    v["futuro"], v["spot"] = v["futuro"][-n:], v["spot"][-n:]


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v["plataformas"].pop("P2") and v["plataformas"].pop("P3"), "al menos 2 plataformas"),
    (lambda v: _recortar_fund(v, 90), "< 90 días"),
    (lambda v: v.update(futuro=v["futuro"][:-1]), "última fecha común"),
    (lambda v: v["futuro"][-1].update(vencimiento=v["futuro"][-1]["fecha"]), "vencimiento no posterior"),
    (lambda v: v["plataformas"]["P1"].update(periodo_horas=0), "periodo_horas"),
    (lambda v: v["plataformas"]["P1"].update(periodo_horas=48), "periodo_horas"),
    (lambda v: v["plataformas"]["P1"]["historia"][5].update(interes_abierto=0), "interes_abierto"),
    (lambda v: v["capitalizacion"].update(fecha="2025-12-01"), "última fecha común"),
    (lambda v: v["plataformas"]["P1"]["historia"].append(dict(v["plataformas"]["P1"]["historia"][-1])), "repetidas"),
])
def test_chr_fund_rechazos(cambio, motivo):
    v = _fund()
    cambio(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _correr("CHR-FUND-001", v)


def test_chr_fund_entre_90_dias_y_un_anio_sin_percentiles():
    v = _fund()
    _recortar_fund(v, 200)
    res, lim = _correr("CHR-FUND-001", v)
    assert res["percentil_financiacion"] is None and res["percentil_base"] is None
    assert any("percentiles no calculados" in x for x in lim)


def test_chr_fund_oraculo_independiente():
    """pandas (pivot de una tabla larga, np.average por fila) y percentileofscore sobre la ventana de 365 días."""
    v = _fund()
    res, _ = _correr("CHR-FUND-001", v)
    filas = [{"fecha": h["fecha"], "plat": k, "anual": h["tasa"] * 24 / p["periodo_horas"] * 365, "oi": h["interes_abierto"]}
             for k, p in v["plataformas"].items() for h in p["historia"]]
    df = pd.DataFrame(filas)
    a, w = df.pivot(index="fecha", columns="plat", values="anual"), df.pivot(index="fecha", columns="plat", values="oi")
    agg = pd.Series([np.average(a.loc[f], weights=w.loc[f]) for f in a.index], index=pd.to_datetime(a.index))
    assert res["financiacion_pct_anual"] == pytest.approx(agg.iloc[-1] * 100, rel=1e-12)
    ventana = agg[agg.index > agg.index[-1] - pd.Timedelta(days=365)]
    assert res["percentil_financiacion"] == pytest.approx(stats.percentileofscore(ventana, agg.iloc[-1], kind="weak") / 100)
    f, s = v["futuro"][-1], v["spot"][-1]
    dias = (pd.Timestamp(f["vencimiento"]) - pd.Timestamp(f["fecha"])).days
    assert res["base_pct_anual"] == pytest.approx((f["precio"] / s["precio"] - 1) * 365 / dias * 100, rel=1e-12)
    res_i, _ = _correr("CHR-FUND-001", v, {"ponderacion": "igual"})
    assert res_i["financiacion_pct_anual"] == pytest.approx(a.iloc[-1].mean() * 100, rel=1e-12)


# ============================================================================= CHR-FLOW-001
def _flow():
    return fr._datos_chr_flow()


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v["flujos_etf"][17].pop("fecha_publicacion"), "sin fecha de publicación"),
    (lambda v: v["flujos_etf"][17].update(fecha_publicacion="2024-01-01"), "publicado antes"),
    (lambda v: v.update(flujos_etf=v["flujos_etf"][-80:]), "< 120 días"),
    (lambda v: v["oferta_stablecoins"].update(USDX=v["oferta_stablecoins"]["USDX"][-100:]), "< 120 días"),
    (lambda v: v.update(oferta_stablecoins={}), "no vacío"),
    (lambda v: v["flujos_etf"][17].update(patrimonio=0), "patrimonio"),
    (lambda v: v["flujos_etf"].append(dict(v["flujos_etf"][-1])), "repetidas"),
])
def test_chr_flow_rechazos(cambio, motivo):
    v = _flow()
    cambio(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _correr("CHR-FLOW-001", v)


def test_chr_flow_ventana_sin_patrimonio_previo_y_opcionales():
    v = _flow()
    with pytest.raises(ErrorFicha, match="sin patrimonio previo"):
        _correr("CHR-FLOW-001", v, {"ventanas": [300]})
    v.pop("capitalizacion_total")
    res, lim = _correr("CHR-FLOW-001", v)
    assert res["razon_stablecoins_capitalizacion_pct"] is None and any("capitalización total" in x for x in lim)


def test_chr_flow_oraculo_independiente():
    """pandas rolling/shift para acumulados, % de patrimonio y z del último año; asof para el crecimiento."""
    v = _flow()
    res, _ = _correr("CHR-FLOW-001", v)
    df = pd.DataFrame(v["flujos_etf"]).assign(fecha=lambda d: pd.to_datetime(d.fecha)).set_index("fecha")
    for w in (5, 20):
        acum = df.flujo.rolling(w).sum()
        rel = acum / df.patrimonio.shift(w)
        h = rel[rel.index > rel.index[-1] - pd.DateOffset(years=1)].dropna()
        assert res["flujos"][str(w)]["moneda"] == pytest.approx(acum.iloc[-1], rel=1e-12)
        assert res["flujos"][str(w)]["pct_patrimonio"] == pytest.approx(rel.iloc[-1] * 100, rel=1e-12)
        assert res["flujos"][str(w)]["z"] == pytest.approx((h.iloc[-1] - h.mean()) / h.std(), rel=1e-9)
    tot = sum(pd.Series({pd.Timestamp(x["fecha"]): x["oferta"] for x in serie})
              for serie in v["oferta_stablecoins"].values())
    T = tot.index[-1]
    assert res["crecimiento_stablecoins_pct"] == pytest.approx((tot.iloc[-1] / tot.asof(T - pd.Timedelta(days=30)) - 1) * 100,
                                                               rel=1e-12)


# ============================================================================= ALT-DESMOOTH-001
def _alt(serie=None):
    return fr._datos_alt(fr._AD_OBS if serie is None else serie)


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v.update(rentabilidades=v["rentabilidades"][:23]), "< 24"),
    (lambda v: v["rentabilidades"].pop(10), "consecutivas"),
    (lambda v: v["rentabilidades"][10].update(fecha=v["rentabilidades"][11]["fecha"]), "repetidas"),
    (lambda v: v["rentabilidades"][10].update(r=-1.0), "mínimo"),
    (lambda v: v.pop("rentabilidades"), "faltan las rentabilidades"),
    (lambda v: v.update(rentabilidades=[{"fecha": x["fecha"], "r": 0.01 * 1.2 ** i}
                                         for i, x in enumerate(v["rentabilidades"])]), "no estacionaria"),
])
def test_alt_rechazos(cambio, motivo):
    v = _alt()
    cambio(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _correr("ALT-DESMOOTH-001", v)


def test_alt_entre_24_y_40_es_limitacion_y_sin_mercado():
    v = _alt()
    v["rentabilidades"] = v["rentabilidades"][-30:]
    v.pop("mercado")
    res, lim = _correr("ALT-DESMOOTH-001", v)
    assert any("< 40" in x for x in lim) and res["beta_dimson"] is None and any("Dimson" in x for x in lim)


def test_alt_glm_no_invertible_se_rechaza():
    with pytest.raises(ErrorFicha, match="no invertible"):
        _correr("ALT-DESMOOTH-001", _alt(), {"metodo": "GLM", "k": 1})


def test_alt_oraculo_geltner_por_filtro_lineal():
    """scipy.signal.lfilter con el filtro inverso (1 − φL)/(1 − φ); φ por np.polyfit; MDD con pandas cummax."""
    v = _alt()
    res, _ = _correr("ALT-DESMOOTH-001", v)
    rs = np.array([x["r"] for x in v["rentabilidades"]])
    phi = np.polyfit(rs[:-1], rs[1:], 1)[0]
    assert res["phi"] == pytest.approx(phi, rel=1e-10)
    d = signal.lfilter([1, -phi], [1 - phi], rs)[1:]
    assert [x["r"] for x in res["serie_desuavizada"]] == pytest.approx(list(d), rel=1e-10, abs=1e-14)
    riqueza = pd.Series(np.r_[1.0, np.cumprod(1 + d)])
    assert res["mdd_desuavizado_pct"] == pytest.approx(float((1 - riqueza / riqueza.cummax()).max()) * 100, rel=1e-10)
    assert res["volatilidad_desuavizada_pct"] == pytest.approx(statistics.stdev(d) * 2 * 100, rel=1e-10)


def test_alt_oraculo_beta_dimson():
    v = _alt()
    res, _ = _correr("ALT-DESMOOTH-001", v)
    r = pd.Series([x["r"] for x in res["serie_desuavizada"]], index=pd.to_datetime([x["fecha"] for x in res["serie_desuavizada"]]))
    m = pd.Series([x["r"] for x in v["mercado"]], index=pd.to_datetime([x["fecha"] for x in v["mercado"]]))
    df = pd.DataFrame({"r": r, "m0": m, "m1": m.shift(1), "m2": m.shift(2)}).dropna()
    df = df[df.index.isin(r.index[2:])]
    X = np.column_stack([np.ones(len(df)), df.m0, df.m1, df.m2])
    coef = np.linalg.solve(X.T @ X, X.T @ df.r.to_numpy())
    assert res["beta_dimson"]["desuavizada"] == pytest.approx(float(coef[1:].sum()), rel=1e-8)


def test_alt_oraculo_glm_verosimilitud_por_rejilla():
    """Para k = 1, la verosimilitud gaussiana exacta (scipy.stats.multivariate_normal) en una rejilla de θ1 invertibles no
    supera la del θ estimado, y el estimado cae junto al mejor punto de la rejilla."""
    serie = fr._AD_OBS_GLM
    res, _ = _correr("ALT-DESMOOTH-001", _alt(serie), {"metodo": "GLM", "k": 1})
    x = serie - serie.mean()
    n = x.size

    def loglik(t1):
        t0 = 1 - t1
        g = np.zeros(n)
        g[0], g[1] = t0 ** 2 + t1 ** 2, t0 * t1
        R = pd.DataFrame([[g[abs(i - j)] for j in range(n)] for i in range(n)]).to_numpy()
        s2 = float(x @ np.linalg.solve(R, x)) / n
        return stats.multivariate_normal(mean=np.zeros(n), cov=s2 * R).logpdf(x)
    rejilla = np.linspace(0.0, 0.49, 50)
    ll = np.array([loglik(t) for t in rejilla])
    t1 = res["theta"][1]
    assert loglik(t1) >= ll.max() - 1e-9
    assert abs(t1 - rejilla[int(np.argmax(ll))]) <= rejilla[1] - rejilla[0]
    assert sum(res["theta"]) == pytest.approx(1.0, abs=1e-12)


def test_alt_niveles_por_rol_equivalen_a_rentabilidades():
    rs = fr._AD_OBS
    niveles = pd.Series(100 * np.r_[1.0, np.cumprod(1 + rs)],
                        index=pd.date_range("2011-12-31", periods=rs.size + 1, freq="QE"))
    a, _ = _correr("ALT-DESMOOTH-001", {}, {"phi": 0.3}, series_rol={"indice_suavizado": niveles})
    v = _alt()
    v.pop("mercado")
    b, _ = _correr("ALT-DESMOOTH-001", v, {"phi": 0.3})
    assert [x["r"] for x in a["serie_desuavizada"]] == pytest.approx([x["r"] for x in b["serie_desuavizada"]], rel=1e-10)


@pytest.mark.parametrize("ficha,k", list(itertools.product(["ALT-DESMOOTH-001"], [1, 2, 3])))
def test_alt_glm_con_cada_k_invertible_y_suma_uno(ficha, k):
    res, _ = _correr(ficha, _alt(fr._AD_OBS_GLM), {"metodo": "GLM", "k": k})
    th = np.array(res["theta"])
    assert th.size == k + 1 and np.all(th >= 0) and th.sum() == pytest.approx(1.0, abs=1e-12)
    assert np.all(np.abs(np.roots(th[::-1])) > 1)
    assert res["verificacion"]["error_resuavizado_max"] <= fr.FICHAS[ficha]["tol"]


def test_alt_dimson_con_rezagos_colineales_no_se_calcula():
    v = _alt()
    for t, x in enumerate(v["mercado"]):
        x["r"] = 0.015 + 0.06 * math.sin(1.1 * t + 0.5)                 # sinusoide pura: m_t lineal en m_{t−1}, m_{t−2}
    res, lim = _correr("ALT-DESMOOTH-001", v)
    assert res["beta_dimson"] is None and any("colineales" in x for x in lim)


def test_la_envoltura_rechaza_resultados_no_finitos_y_traduce_excepciones():
    @fr._cerrado("PRUEBA")
    def no_finito(ent, params):
        return {"a": {"b": [1.0, math.nan]}}, []

    @fr._cerrado("PRUEBA")
    def infinito(ent, params):
        return {"a": np.float64(math.inf)}, []

    @fr._cerrado("PRUEBA")
    def revienta(ent, params):
        raise ZeroDivisionError("x")
    for fn in (no_finito, infinito):
        with pytest.raises(ErrorFicha, match="no finito"):
            fn({"valores": {}}, {})
    with pytest.raises(ErrorFicha, match="ZeroDivisionError"):
        revienta({"valores": {}}, {})


def test_rei_ffo_percentil_cuenta_los_empates():
    res, _ = _correr("REI-FFO-001", fr._datos_rei_ffo())
    h = np.array([a for a, _ in fr._FFO_HIST])
    assert np.sum(h == res["p_ffo"]) == 1 and res["percentil_p_ffo"] == float(np.mean(h <= res["p_ffo"]))
    assert res["percentil_p_ffo"] > float(np.mean(h < res["p_ffo"]))
