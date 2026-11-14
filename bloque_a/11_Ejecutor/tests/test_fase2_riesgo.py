"""T-112 · Motor Fase 2, grupo R: RISK-VAR-001, SIM-MC-001, SCN-H-001, BT-DSR-001, BT-PBO-001, BT-VAR-001, ML-CAL-001,
ML-PRED-001 y DEC-VOI-001 (Catálogo del Motor V5.0).

Casos de control de la «Verificación», rechazos de «Aclaración y rechazo» y de «Entradas mínimas», dominio de los
parámetros, umbrales fijos, determinismo con semilla, entradas hostiles y, por ficha, al menos un oráculo independiente
que recalcula el resultado por otra vía sin llamar al código de la ficha.
"""
import copy
import itertools
import json
import math
import re
import statistics
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config, parametro, sesiones_horizonte
from bloque_a.motor import fichas_fon_der, fichas_tcv, servicio
from bloque_a.motor import fichas_riesgo as R
from bloque_a.motor.operaciones import ErrorFicha
from scipy import integrate, optimize, stats

FICHAS = sorted(R.FICHAS)
CATALOGO = (Path(__file__).resolve().parents[2] / "04_Motor_conocimiento_y_catalogo"
            / "Catálogo de cálculos del Motor - V5.0.md")


def _ent(valores, series=None):
    return {"valores": copy.deepcopy(valores), "series": series or {}, "series_rol": {}}


def _correr(ficha, valores, params=None, series=None):
    return R.FICHAS[ficha]["fn"](_ent(valores, series), dict(params or {}))


def _valores_caso(caso):
    v = {}
    for d in caso["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    return v


CASOS = [(f, c) for f, casos in R.CASOS_CONTROL.items() for c in casos]

# Entrada válida de referencia de cada ficha (el primer caso de control) y la clave de su dato principal
BASE = {f: (_valores_caso(R.CASOS_CONTROL[f][0]), dict(R.CASOS_CONTROL[f][0]["parametros"])) for f in FICHAS}
BASE["BT-PBO-001"] = ({"rendimientos": R._pbo_ruido(4, 64, 7)}, {"S": 8})
BASE["SCN-H-001"] = ({"rendimientos": R._datos_scn()["rendimientos"]}, {"semilla": 5, "clase": "RV", "n_trayectorias": 2000})
BASE["SIM-MC-001"] = (BASE["SIM-MC-001"][0], {"n_trayectorias": 2000, "horizonte": 5, "semilla": 9})


def _rendimientos(n, semilla=1, escala=0.01):
    return [float(x) for x in escala * np.random.default_rng(semilla).standard_normal(n)]


# ============================================================================= registro, catálogo y casos de control
def test_registro_de_las_nueve_fichas():
    esperadas = {"RISK-VAR-001", "SIM-MC-001", "SCN-H-001", "BT-DSR-001", "BT-PBO-001", "BT-VAR-001", "ML-CAL-001",
                 "ML-PRED-001", "DEC-VOI-001"}
    assert set(R.FICHAS) == set(R.PARAMETROS_POR_DEFECTO) == set(R.UMBRALES) == set(R.ADVERTENCIAS) \
        == set(R.CASOS_CONTROL) == esperadas
    for meta in R.FICHAS.values():
        assert set(meta) == {"fn", "modulo", "version", "cifra", "ri", "tol"} and callable(meta["fn"])
        assert meta["cifra"] == "ESTADISTICA" and meta["ri"] and meta["tol"] > 0


def _bloque_catalogo(ficha):
    texto = CATALOGO.read_text(encoding="utf-8")
    i = texto.index(f"### {ficha} ·")
    j = texto.index("\n### ", i + 1)
    return texto[i:j]


@pytest.mark.parametrize("ficha", FICHAS)
def test_version_modulo_y_tolerancia_salen_de_la_ficha(ficha):
    bloque = _bloque_catalogo(ficha)
    ident = re.search(r"\*\*Identificación\.\*\* v(\d+\.\d+) · VIGENTE · (MC-\d+)", bloque)
    assert ident and R.FICHAS[ficha]["version"] == ident.group(1) and R.FICHAS[ficha]["modulo"] == ident.group(2)
    tol = re.search(r"\*\*Tolerancias y semilla\.\*\* (1e-\d+)", bloque)
    assert tol and R.FICHAS[ficha]["tol"] == float(tol.group(1))


@pytest.mark.parametrize("ficha", FICHAS)
def test_advertencias_literales_de_supuestos_y_limitaciones(ficha):
    supuestos = re.search(r"\*\*Supuestos y limitaciones\.\*\* (.+)", _bloque_catalogo(ficha)).group(1).lower()
    normal = re.sub(r"[^\wáéíóúñ√≥]+", " ", supuestos)
    for adv in R.ADVERTENCIAS[ficha]:
        trozo = re.sub(r"[^\wáéíóúñ√≥]+", " ", adv.lower()).split()[:3]
        assert " ".join(trozo) in normal, adv


@pytest.mark.parametrize("ficha,caso", CASOS, ids=[f"{f}:{c['nombre'][:50]}" for f, c in CASOS])
def test_casos_de_control(ficha, caso):
    res, lim = _correr(ficha, _valores_caso(caso), caso["parametros"])
    assert caso["comprobar"](res)
    json.dumps(res, allow_nan=False)
    assert all(isinstance(x, str) for x in lim)
    assert res["advertencias"] == R.ADVERTENCIAS[ficha] and not set(lim) & set(R.ADVERTENCIAS[ficha])


@pytest.mark.parametrize("ficha", FICHAS)
def test_al_menos_dos_casos_de_control_por_ficha(ficha):
    assert len(R.CASOS_CONTROL[ficha]) >= 2


def _perturbar(x, factor):
    if isinstance(x, dict):
        return {k: _perturbar(v, factor) for k, v in x.items()}
    if isinstance(x, list):
        return [_perturbar(v, factor) for v in x]
    if isinstance(x, float):
        return x * factor + (factor - 1)
    return x


# Casos cuya identidad es estructural (no numérica): se prueban aparte con su contraejemplo.
_ESTRUCTURALES = {"configuraciones idénticas ⇒ PBO indefinido declarado", "sin señal ⇒ «sin mejora demostrada»",
                  "regla simple: rango que no alcanza ningún umbral ±5 ni el orden del top-3 ⇒ VOI = 0, NO_EJECUTAR",
                  "señal ruidosa ⇒ EVPI > EVSI > 0",
                  "permutaciones por bloques de una misma serie (sobreajuste puro) ⇒ PBO ≥ 0,5 y pendiente negativa",
                  "sin habilidad (ruido iid) ⇒ PBO ≈ 0,5 (±0,3, dos desviaciones entre conjuntos)",
                  "señal conocible ⇒ mejora frente a RI-TB con IC > 0",
                  "particiones walk-forward sin solape con purga y embargo (entrenamiento ≤ inicio − embargo)",
                  "segunda vía: en una muestra normal por cuantiles exactos, histórico y paramétrico coinciden (≤ 1 %)",
                  "tabla de convergencia por mitades (n, n/2, n/4, n/8) coherente con la distribución completa",
                  "GARCH(1,1) a dos pasos: curtosis del log-rendimiento analítica (separa α de β)",
                  "cuantiles monótonos, adverso < base < favorable y bandas crecientes H1 → H2 → H3 → H4",
                  "excedencias agrupadas ⇒ LR_ind de Christoffersen con sus transiciones (independencia rechazada)"}


@pytest.mark.parametrize("ficha,caso", [(f, c) for f, c in CASOS if c["nombre"] not in _ESTRUCTURALES],
                         ids=[f"{f}:{c['nombre'][:50]}" for f, c in CASOS if c["nombre"] not in _ESTRUCTURALES])
def test_cada_caso_numerico_puede_fallar(ficha, caso):
    """H-08 de T-106: un caso que no puede fallar no cuenta. Un 1 ‰ de error en las cifras (10 % en las de simulación,
    que se contrastan con 4 errores estándar) lo hace fallar."""
    res, _ = _correr(ficha, _valores_caso(caso), caso["parametros"])
    factor = 1.1 if ficha in ("SIM-MC-001", "SCN-H-001") else 1.001   # simulación: tolerancia de 4 EE
    try:
        sigue = bool(caso["comprobar"](_perturbar(res, factor)))
    except (TypeError, KeyError, ValueError, ZeroDivisionError):
        sigue = False
    assert not sigue


def test_casos_estructurales_tienen_contraejemplo():
    c = {x["nombre"]: x for f in FICHAS for x in R.CASOS_CONTROL[f]}
    assert not c["configuraciones idénticas ⇒ PBO indefinido declarado"]["comprobar"]({"pbo": 0.5, "indefinido": False})
    assert not c["sin señal ⇒ «sin mejora demostrada»"]["comprobar"](
        {"mejora_frente_referencia": {"conclusion": "mejora demostrada"}})
    r, _ = _correr("BT-PBO-001", {"rendimientos": R._pbo_dominante()})
    assert not c["permutaciones por bloques de una misma serie (sobreajuste puro) ⇒ PBO ≥ 0,5 y pendiente negativa"][
        "comprobar"](r)
    r, _ = _correr("ML-PRED-001", R._pred_datos(False, 11211))
    assert not c["señal conocible ⇒ mejora frente a RI-TB con IC > 0"]["comprobar"](r)
    r, _ = _correr("DEC-VOI-001", {**R._VOI_U, "verosimilitud": {"desviacion": 0.0}}, {"coste_uc": 0.5})
    assert not c["señal ruidosa ⇒ EVPI > EVSI > 0"]["comprobar"](r)
    r, _ = _correr("DEC-VOI-001", {**R._VOI_U}, {"coste_uc": 0.5})
    assert not c["regla simple: rango que no alcanza ningún umbral ±5 ni el orden del top-3 ⇒ VOI = 0, NO_EJECUTAR"][
        "comprobar"](r)
    r, _ = _correr("RISK-VAR-001", {"rendimientos": R._R_VAR_COLAS})   # colas gruesas: histórico ≠ normal
    assert not c["segunda vía: en una muestra normal por cuantiles exactos, histórico y paramétrico coinciden (≤ 1 %)"][
        "comprobar"](r)
    r, _ = _correr("BT-VAR-001", R._var_espaciado([20, 70, 120, 170, 220], 250, 0.02), {"nivel": 0.99})
    assert not c["excedencias agrupadas ⇒ LR_ind de Christoffersen con sus transiciones (independencia rechazada)"][
        "comprobar"](r)
    datos = R._datos_scn()
    r, _ = _correr("SCN-H-001", {**datos, "bloques": {**datos["bloques"], "cambio_valoracion": {"valor": 0.0, "incertidumbre": 0.0}}},
                   {"semilla": 116, "clase": "RV"})
    assert not c["cuantiles monótonos, adverso < base < favorable y bandas crecientes H1 → H2 → H3 → H4"]["comprobar"](r)
    r, _ = _correr("ML-PRED-001", R._pred_datos(True, 11210), {"embargo": 2, "pliegues": 4})
    assert not c["particiones walk-forward sin solape con purga y embargo (entrenamiento ≤ inicio − embargo)"]["comprobar"](r)
    r, _ = _correr("SIM-MC-001", {"dinamica": {"tipo": "paseo_aleatorio", "mu": 0.0, "sigma": 0.02}},
                   {"n_trayectorias": 16_000, "horizonte": 5, "semilla": 115})
    assert not c["tabla de convergencia por mitades (n, n/2, n/4, n/8) coherente con la distribución completa"]["comprobar"](r)
    r, _ = _correr("SIM-MC-001", {"dinamica": {"tipo": "garch", "mu": 0.0, "omega": 2e-6, "alpha": 0.9, "beta": 0.08,
                                               "sigma2_inicial": 4e-4}},
                   {"n_trayectorias": 40_000, "horizonte": 2, "semilla": 119})          # α y β cambiados
    assert not c["GARCH(1,1) a dos pasos: curtosis del log-rendimiento analítica (separa α de β)"]["comprobar"](r)
    # PBO ≈ 0,5: el ruido de otra semilla puede salir de la banda, pero la configuración dominante no entra
    r, _ = _correr("BT-PBO-001", {"rendimientos": R._pbo_dominante()})
    assert not c["sin habilidad (ruido iid) ⇒ PBO ≈ 0,5 (±0,3, dos desviaciones entre conjuntos)"]["comprobar"](r)


# ============================================================================= determinismo, salidas y entrada intacta
@pytest.mark.parametrize("ficha", FICHAS)
def test_determinismo_dos_pasadas(ficha):
    v, p = BASE[ficha]
    a = json.dumps(_correr(ficha, v, p), sort_keys=True, allow_nan=False)
    b = json.dumps(_correr(ficha, v, p), sort_keys=True, allow_nan=False)
    assert a == b


@pytest.mark.parametrize("ficha", ["SIM-MC-001", "SCN-H-001", "ML-CAL-001", "ML-PRED-001"])
def test_la_semilla_manda(ficha):
    v, p = BASE[ficha]
    a, _ = _correr(ficha, v, {**p, "semilla": 1})
    b, _ = _correr(ficha, v, {**p, "semilla": 2})
    assert json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True)


@pytest.mark.parametrize("ficha", FICHAS)
def test_no_modifica_la_entrada(ficha):
    v, p = BASE[ficha]
    ent = _ent(v)
    antes = json.dumps(ent["valores"], sort_keys=True)
    p2 = dict(p)
    R.FICHAS[ficha]["fn"](ent, p2)
    assert json.dumps(ent["valores"], sort_keys=True) == antes and p2 == p


# ============================================================================= umbrales fijos y dominio de parámetros
@pytest.mark.parametrize("ficha,umbral", [(f, k) for f in FICHAS for k in R.UMBRALES[f]])
def test_ningun_umbral_se_cambia_desde_la_peticion(ficha, umbral):
    v, p = BASE[ficha]
    with pytest.raises(ErrorFicha, match="umbrales fijos"):
        _correr(ficha, v, {**p, umbral: R.UMBRALES[ficha][umbral]})


DOMINIO = [
    ("RISK-VAR-001", "nivel", 0.899), ("RISK-VAR-001", "nivel", 0.991), ("RISK-VAR-001", "nivel", "0.95"),
    ("RISK-VAR-001", "horizonte", 0), ("RISK-VAR-001", "horizonte", 1.5), ("RISK-VAR-001", "metodo", "garch"),
    ("RISK-VAR-001", "moneda", 3), ("RISK-VAR-001", "nivel", True),
    ("SIM-MC-001", "n_trayectorias", 999), ("SIM-MC-001", "n_trayectorias", 1_000_001), ("SIM-MC-001", "horizonte", 0),
    ("SIM-MC-001", "cuantiles", [0.5, 1.0]), ("SIM-MC-001", "cuantiles", []), ("SIM-MC-001", "semilla", -1),
    ("SIM-MC-001", "semilla", 1.5), ("SIM-MC-001", "reduccion_varianza", "control"), ("SIM-MC-001", "umbrales", ["x"]),
    ("SIM-MC-001", "n_trayectorias", 2001),
    ("SCN-H-001", "horizontes", ["H5"]), ("SCN-H-001", "horizontes", ["H1", "H1"]), ("SCN-H-001", "clase", "XX"),
    ("SCN-H-001", "n_trayectorias", 500), ("SCN-H-001", "cuantiles", [0.0, 0.5]), ("SCN-H-001", "semilla", "7"),
    ("BT-DSR-001", "N", 0), ("BT-DSR-001", "N", 2.5), ("BT-DSR-001", "nivel", 1.0), ("BT-DSR-001", "frecuencia", "semanal"),
    ("BT-DSR-001", "SR_referencia", float("nan")),
    ("BT-PBO-001", "S", 6), ("BT-PBO-001", "S", 22), ("BT-PBO-001", "S", 9), ("BT-PBO-001", "metrica", "sortino"),
    ("BT-VAR-001", "nivel", 0.5), ("BT-VAR-001", "significacion", 0.0), ("BT-VAR-001", "ventana_estimacion", 249),
    ("BT-VAR-001", "metodo_var", "x"), ("BT-VAR-001", "baja_potencia_declarada", "si"), ("BT-VAR-001", "horizonte", 0),
    ("ML-CAL-001", "replicas", 0), ("ML-CAL-001", "nivel_ic", 1.2), ("ML-CAL-001", "semilla", -3),
    ("ML-CAL-001", "esquema", "k_fold"),
    ("ML-PRED-001", "modelo", "arboles"), ("ML-PRED-001", "rejilla", []), ("ML-PRED-001", "rejilla", [0.0]),
    ("ML-PRED-001", "rejilla", list(range(1, 22))), ("ML-PRED-001", "embargo", 0), ("ML-PRED-001", "calibracion", "beta"),
    ("ML-PRED-001", "pliegues", 1), ("ML-PRED-001", "fraccion_inicial", 1.0),
    ("DEC-VOI-001", "coste_uc", -1.0), ("DEC-VOI-001", "coste_uc", "1"),
]


@pytest.mark.parametrize("ficha,param,valor", DOMINIO, ids=[f"{f}:{k}={v!r}"[:60] for f, k, v in DOMINIO])
def test_dominio_de_cada_parametro(ficha, param, valor):
    v, p = BASE[ficha]
    with pytest.raises(ErrorFicha):
        _correr(ficha, v, {**p, param: valor})


@pytest.mark.parametrize("ficha,params", [
    ("RISK-VAR-001", {"nivel": 0.90}), ("RISK-VAR-001", {"nivel": 0.99, "metodo": "normal"}),
    ("SIM-MC-001", {"n_trayectorias": 1000}), ("BT-PBO-001", {"S": 8}), ("BT-PBO-001", {"S": 16}),
    ("ML-PRED-001", {"rejilla": [float(x) for x in range(1, 21)]}), ("ML-PRED-001", {"calibracion": "isotonica"}),
    ("ML-PRED-001", {"calibracion": "ninguna"}), ("DEC-VOI-001", {"coste_uc": 0.0})])
def test_bordes_admitidos_del_dominio(ficha, params):
    v, p = BASE[ficha]
    res, _ = _correr(ficha, v, {**p, **params})
    json.dumps(res, allow_nan=False)


def test_nivel_de_risk_var_coincide_con_tcv_vixts_y_der_vrp():
    nivel, rango = R.PARAMETROS_POR_DEFECTO["RISK-VAR-001"]["nivel"], R.UMBRALES["RISK-VAR-001"]["rango_nivel"]
    assert fichas_tcv.PARAMETROS_POR_DEFECTO["TCV-VIXTS-001"]["nivel_es"] == nivel
    assert fichas_tcv.UMBRALES["TCV-VIXTS-001"]["rango_nivel_es"] == rango
    assert fichas_tcv.UMBRALES["TCV-VIXTS-001"]["observaciones_minimas_es"] == R.UMBRALES["RISK-VAR-001"]["observaciones_minimas"]
    assert fichas_fon_der.PARAMETROS_POR_DEFECTO["DER-VRP-001"]["nivel_es"] == nivel
    assert list(fichas_fon_der.RANGOS["DER-VRP-001"]["nivel_es"]) == rango


# ============================================================================= entradas hostiles
PRINCIPAL = {"RISK-VAR-001": "rendimientos", "SIM-MC-001": "dinamica", "SCN-H-001": "rendimientos",
             "BT-DSR-001": "rendimientos", "BT-PBO-001": "rendimientos", "BT-VAR-001": "var_previsto",
             "ML-CAL-001": "horizontes", "ML-PRED-001": "fechas", "DEC-VOI-001": "rango_plausible"}
HOSTILES = [[], None, "texto", 5, [float("nan")] * 300, [float("inf")] * 300, ["a"] * 300, [True] * 300,
            {"x": 1}, [[1, 2]] * 300]


@pytest.mark.parametrize("ficha,hostil", [(f, h) for f in FICHAS for h in HOSTILES],
                         ids=[f"{f}:{str(h)[:20]}" for f in FICHAS for h in HOSTILES])
def test_entradas_hostiles_se_rechazan(ficha, hostil):
    v, p = BASE[ficha]
    v = copy.deepcopy(v)
    v[PRINCIPAL[ficha]] = hostil
    with pytest.raises(ErrorFicha):
        _correr(ficha, v, p)


@pytest.mark.parametrize("ficha", FICHAS)
@pytest.mark.parametrize("ent", [None, [], "x", {"valores": [1, 2]}, {"valores": {}}, {"valores": {}, "series": [1]}])
def test_entrada_mal_formada(ficha, ent):
    with pytest.raises(ErrorFicha):
        R.FICHAS[ficha]["fn"](ent, {})


@pytest.mark.parametrize("ficha", FICHAS)
def test_parametros_que_no_son_un_objeto(ficha):
    v, _ = BASE[ficha]
    with pytest.raises(ErrorFicha):
        R.FICHAS[ficha]["fn"](_ent(v), [1, 2])


@pytest.mark.parametrize("ficha,cambio", [
    ("RISK-VAR-001", lambda v: v.update(rendimientos=[1e308] * 300 + [-1e308] * 300)),
    ("BT-DSR-001", lambda v: v.update(rendimientos=[1e308, -1e308] * 200)),
    ("SIM-MC-001", lambda v: v["dinamica"].update(mu=1e300, sigma=1e300)),
    ("DEC-VOI-001", lambda v: v["rango_plausible"].update(inferior=-1e308, superior=1e308)),
])
def test_desbordes_no_sirven_no_finitos(ficha, cambio):
    v, p = BASE[ficha]
    v = copy.deepcopy(v)
    cambio(v)
    try:
        res, _ = _correr(ficha, v, p)
    except ErrorFicha:
        return
    json.dumps(res, allow_nan=False)


def test_la_envoltura_rechaza_un_resultado_no_finito(monkeypatch):
    envuelta = R._cerrado("RISK-VAR-001", lambda ent, params: ({"x": float("nan")}, []))
    with pytest.raises(ErrorFicha, match="no finito"):
        envuelta({"valores": {}}, {})


# ============================================================================= RISK-VAR-001
def test_risk_var_rechazos():
    with pytest.raises(ErrorFicha, match="249 observaciones"):
        _correr("RISK-VAR-001", {"rendimientos": _rendimientos(249)})
    corto = {"rendimientos": _rendimientos(300)}
    with pytest.raises(ErrorFicha, match="empírico"):
        _correr("RISK-VAR-001", corto, {"nivel": 0.99})
    _, lim = _correr("RISK-VAR-001", corto, {"nivel": 0.99, "metodo": "normal"})   # paramétrico: admitido
    assert any("500 recomendadas" in x for x in lim)
    with pytest.raises(ErrorFicha, match="excedencias"):
        _correr("RISK-VAR-001", {"rendimientos": _rendimientos(400)}, {"metodo": "evt_pot"})
    with pytest.raises(ErrorFicha, match="semilla"):
        _correr("RISK-VAR-001", {"distribucion": {"rendimientos": _rendimientos(1000)}})
    with pytest.raises(ErrorFicha, match="moneda"):
        _correr("RISK-VAR-001", {"rendimientos": _rendimientos(300), "valor_posicion": 1e6})
    uniforme = [float(x) for x in np.linspace(-0.02, 0.02, 600)]       # curtosis en exceso negativa
    with pytest.raises(ErrorFicha, match="curtosis"):
        _correr("RISK-VAR-001", {"rendimientos": uniforme}, {"metodo": "t"})
    sesgada = [float(x) for x in np.r_[np.full(590, 0.001), np.full(10, -0.3)]]
    with pytest.raises(ErrorFicha, match="Cornish-Fisher"):
        _correr("RISK-VAR-001", {"rendimientos": sesgada}, {"metodo": "cornish_fisher"})
    with pytest.raises(ErrorFicha, match="dispersión"):
        _correr("RISK-VAR-001", {"rendimientos": [0.001] * 300}, {"metodo": "normal"})


def _cuantil_tipo7(x, a):
    """Cuantil de Hyndman y Fan tipo 7 a mano: h = (n − 1)·a; x₍⌊h⌋₎ + (h − ⌊h⌋)(x₍⌊h⌋+1₎ − x₍⌊h⌋₎)."""
    s = sorted(x)
    h = (len(s) - 1) * a
    i = math.floor(h)
    return s[i] + (h - i) * (s[min(i + 1, len(s) - 1)] - s[i])


def test_risk_var_oraculo_historico_normal_y_horizonte():
    x = R._R_VAR_COLAS
    q = _cuantil_tipo7(x, 0.025)
    cola = [e for e in x if e <= q]
    res, lim = _correr("RISK-VAR-001", {"rendimientos": x}, {"horizonte": 4})
    assert res["var"] == pytest.approx(-q * 2, rel=1e-12) and res["es"] == pytest.approx(-sum(cola) / len(cola) * 2, rel=1e-12)
    assert any("√h" in a for a in lim)
    nd = statistics.NormalDist(statistics.fmean(x), statistics.stdev(x))
    assert res["segunda_via"]["var"] == pytest.approx(-nd.inv_cdf(0.025) * 2, rel=1e-9)
    z = statistics.NormalDist().inv_cdf(0.975)
    assert res["referencia_ingenua"]["var"] == pytest.approx(statistics.stdev(x) * z * 2, rel=1e-9)
    res, _ = _correr("RISK-VAR-001", {"rendimientos": x, "valor_posicion": 2e6}, {"moneda": "EUR"})
    assert res["var_moneda"] == pytest.approx(res["var"] * 2e6, rel=1e-12) and res["moneda"] == "EUR"


def test_risk_var_es_igual_al_de_tcv_vixts():
    """El ES histórico de RISK-VAR coincide con el que TCV-VIXTS-001 calcula para su exposición corta."""
    hr = np.array(R._R_VAR_COLAS)
    corta = -hr
    q = float(np.quantile(corta, 1 - 0.975))
    es_vixts = -float(np.mean(corta[corta <= q]))
    res, _ = _correr("RISK-VAR-001", {"rendimientos": corta.tolist()})
    assert res["es"] == pytest.approx(es_vixts, rel=1e-12)


def test_risk_var_acepta_una_serie_de_precios_y_una_distribucion_con_semilla():
    precios = pd.Series(100 * np.cumprod(1 + np.array(R._R_VAR_COLAS)), index=pd.bdate_range("2020-01-01", periods=1500))
    res, _ = _correr("RISK-VAR-001", {}, series={"X": precios})
    r = precios.pct_change().dropna().to_numpy()
    assert res["n"] == 1499 and res["var"] == pytest.approx(-np.quantile(r, 0.025), rel=1e-10)
    res, _ = _correr("RISK-VAR-001", {"distribucion": {"rendimientos": R._R_VAR_COLAS, "semilla": 3}})
    assert res["origen"] == "distribucion"
    with pytest.raises(ErrorFicha, match="más de una serie"):
        _correr("RISK-VAR-001", {}, series={"A": precios, "B": precios})


# ============================================================================= SIM-MC-001
def test_sim_mc_rechazos():
    din = {"dinamica": {"tipo": "paseo_aleatorio", "mu": 0.0, "sigma": 0.01}}
    with pytest.raises(ErrorFicha, match="sin semilla"):
        _correr("SIM-MC-001", din, {"horizonte": 5})
    with pytest.raises(ErrorFicha, match="dinamica"):
        _correr("SIM-MC-001", {}, {"horizonte": 5, "semilla": 1})
    with pytest.raises(ErrorFicha, match="horizonte"):
        _correr("SIM-MC-001", din, {"semilla": 1})
    with pytest.raises(ErrorFicha, match="sigma"):
        _correr("SIM-MC-001", {"dinamica": {"tipo": "paseo_aleatorio", "mu": 0.0}}, {"horizonte": 5, "semilla": 1})
    with pytest.raises(ErrorFicha, match="integrado"):
        _correr("SIM-MC-001", {"dinamica": {"tipo": "garch", "mu": 0, "omega": 1e-6, "alpha": 0.2, "beta": 0.8}},
                {"horizonte": 5, "semilla": 1})
    with pytest.raises(ErrorFicha, match="no reconocido"):
        _correr("SIM-MC-001", {"dinamica": {"tipo": "levy", "mu": 0}}, {"horizonte": 5, "semilla": 1})


def test_sim_mc_oraculo_probabilidad_de_umbral_lognormal():
    """P(V_T ≥ u) = 1 − Φ((ln(u/V₀) − hμ)/(σ√h)), por la distribución lognormal (NormalDist), dentro de 4 EE."""
    v0, mu, s, h, n = 50.0, 0.0005, 0.02, 30, 40_000
    res, _ = _correr("SIM-MC-001", {"dinamica": {"tipo": "paseo_aleatorio", "mu": mu, "sigma": s, "valor_inicial": v0}},
                     {"n_trayectorias": n, "horizonte": h, "semilla": 21, "umbrales": [55.0, 45.0]})
    for u in (55.0, 45.0):
        p = 1 - statistics.NormalDist(h * mu, s * math.sqrt(h)).cdf(math.log(u / v0))
        est = res["distribucion"]["probabilidades_umbral"][f"{u:g}"]["probabilidad"]
        assert abs(est - p) <= 4 * math.sqrt(p * (1 - p) / n)


def test_sim_mc_bootstrap_filtrado_y_referencia_ri_cli():
    z = [float(x) for x in np.random.default_rng(4).standard_t(6, 500)]
    v = {"dinamica": {"tipo": "bootstrap_filtrado", "mu": 0.0, "omega": 1e-6, "alpha": 0.05, "beta": 0.9, "residuos": z},
         "historia_rendimientos": _rendimientos(500)}
    res, lim = _correr("SIM-MC-001", v, {"horizonte": 10, "semilla": 3})
    assert res["reduccion_varianza"] == "ninguna" and any("antitéticas no aplicables" in x for x in lim)
    assert res["solucion_analitica"] is None and res["referencia_ingenua"]["tipo"].startswith("RI-CLI")
    # Oráculo: con α = β = 0 la varianza es ω constante y el log-rendimiento a h pasos es la suma de h residuos remuestreados
    v2 = {"dinamica": {"tipo": "bootstrap_filtrado", "mu": 0.0, "omega": 1e-4, "alpha": 0.0, "beta": 0.0,
                       "sigma2_inicial": 1e-4, "residuos": z}}
    res, _ = _correr("SIM-MC-001", v2, {"horizonte": 10, "semilla": 3, "n_trayectorias": 40_000})
    var_z = statistics.pvariance(z)                                      # varianza de la distribución de remuestreo
    assert res["log_rendimiento"]["varianza"] == pytest.approx(10 * 1e-4 * var_z, rel=0.05)


# ============================================================================= SCN-H-001
def test_scn_h_rechazos():
    datos = R._datos_scn()
    with pytest.raises(ErrorFicha, match="sin semilla"):
        _correr("SCN-H-001", datos, {"clase": "RV"})
    with pytest.raises(ErrorFicha, match="«No» para DER"):
        _correr("SCN-H-001", datos, {"semilla": 1, "clase": "DER"})           # H4 «No» en la tabla 8.3
    with pytest.raises(ErrorFicha, match="«No» para FON"):
        _correr("SCN-H-001", datos, {"semilla": 1, "clase": "FON", "horizontes": ["H1"]})
    with pytest.raises(ErrorFicha, match="clase"):
        _correr("SCN-H-001", datos, {"semilla": 1})
    with pytest.raises(ErrorFicha, match="2 años"):
        _correr("SCN-H-001", {"rendimientos": _rendimientos(503)}, {"semilla": 1, "clase": "RV"})
    _correr("SCN-H-001", {"rendimientos": _rendimientos(504)}, {"semilla": 1, "clase": "RV", "n_trayectorias": 2000})
    with pytest.raises(ErrorFicha, match="< 730"):
        _correr("SCN-H-001", {"rendimientos": _rendimientos(504)}, {"semilla": 1, "clase": "CRI"})
    malo = copy.deepcopy(datos)
    malo["regimen"]["probabilidades_filtradas"]["alcista"] = 0.8
    with pytest.raises(ErrorFicha, match="no suman 1"):
        _correr("SCN-H-001", malo, {"semilla": 1, "clase": "RV", "horizontes": ["H3"]})
    with pytest.raises(ErrorFicha, match="sin sus datos"):
        _correr("SCN-H-001", {"rendimientos": datos["rendimientos"]}, {"semilla": 1, "clase": "RV", "horizontes": ["H4"]})
    with pytest.raises(ErrorFicha, match="incoherentes"):
        _correr("SCN-H-001", {**datos, "escenarios_narrativos": {"H4": {"favorable": -50.0, "adverso": 50.0, "fuente": "P"}}},
                {"semilla": 1, "clase": "RV", "horizontes": ["H4"]})
    with pytest.raises(ErrorFicha, match="fuente"):
        _correr("SCN-H-001", {"bloques": {**datos["bloques"], "fuente": ""}}, {"semilla": 1, "clase": "RV"})


def test_scn_h_limitado_y_narrativos():
    datos = R._datos_scn()
    res, lim = _correr("SCN-H-001", {**datos, "escenarios_narrativos": {"H4": {"favorable": 30.0, "adverso": -20.0,
                                                                             "fuente": "Prospectiva"}}},
                       {"semilla": 1, "clase": "TCV", "horizontes": ["H3", "H4"], "n_trayectorias": 2000})
    assert res["horizontes"]["H4"]["aplicabilidad"] == "LIMITADO" and any("H4 «Limitado»" in x for x in lim)
    e = res["horizontes"]["H4"]["escenarios"]
    assert (e["favorable"], e["adverso"], e["origen"]) == (30.0, -20.0, "narrativos de Prospectiva")


def test_scn_h_oraculo_h4_normal_y_ri_pa():
    """H4 a un año es Σ N(vᵢ, uᵢ): cuantiles de la normal (NormalDist) dentro de 4 EE; RI-PA es el valor inicial."""
    b = R._datos_scn()["bloques"]
    v = {"bloques": b, "valor_inicial": 200.0}
    n = 40_000
    res, _ = _correr("SCN-H-001", v, {"semilla": 9, "clase": "RV", "n_trayectorias": n, "cuantiles": [0.1, 0.5, 0.9]})
    h4 = res["horizontes"]["H4"]
    mu = sum(b[k]["valor"] for k in ("rendimiento_corriente", "crecimiento", "cambio_valoracion"))
    sd = math.sqrt(sum(b[k]["incertidumbre"] ** 2 for k in ("rendimiento_corriente", "crecimiento", "cambio_valoracion")))
    nd = statistics.NormalDist(mu, sd)
    for q, val in h4["cuantiles"].items():
        ee = math.sqrt(float(q) * (1 - float(q)) / n) / nd.pdf(nd.inv_cdf(float(q))) * 200
        assert abs(val - 200 * (1 + nd.inv_cdf(float(q)))) <= 4 * ee
    assert h4["referencia_ingenua"]["RI-PA"] == 200.0 and h4["unidades"] == "unidades de la variable"
    assert h4["escenarios"]["favorable"] == pytest.approx(200 * (1 + nd.inv_cdf(0.8)), abs=4 * 200 * sd / math.sqrt(n) * 3)


def _garch_simulado(om, al, be, n, semilla):
    rng = np.random.default_rng(semilla)
    h, eps = om / (1 - al - be), []
    for _ in range(n):
        e = math.sqrt(h) * rng.standard_normal()
        eps.append(e)
        h = om + al * e * e + be * h
    return np.array(eps)


def test_scn_h_oraculo_garch_qmle_recupera_los_parametros():
    """Datos generados con un GARCH(1,1) conocido (bucle propio): la QMLE recupera α y β."""
    eps = _garch_simulado(2e-6, 0.08, 0.9, 4000, 31)
    g = R.garch_qmle(eps, "prueba")
    assert g["alpha"] == pytest.approx(0.08, abs=0.03) and g["beta"] == pytest.approx(0.9, abs=0.04)
    # y la recursión filtrada coincide con un bucle a mano
    h = [float(np.var(eps - eps.mean()))]
    e = eps - eps.mean()
    for t in range(1, 50):
        h.append(g["omega"] + g["alpha"] * e[t - 1] ** 2 + g["beta"] * h[-1])
    np.testing.assert_allclose(R.varianzas_garch(e[:50], g["omega"], g["alpha"], g["beta"], h[0]), h, rtol=1e-12)


def test_scn_h_garch_aportado_con_fuente():
    datos = R._datos_scn()
    g = {"omega": 2e-6, "alpha": 0.05, "beta": 0.93, "fuente": "VOL-GARCH-001"}
    res, _ = _correr("SCN-H-001", {"rendimientos": datos["rendimientos"], "garch": g},
                     {"semilla": 2, "clase": "RV", "n_trayectorias": 2000})
    assert res["horizontes"]["H1"]["garch"]["alpha"] == 0.05
    with pytest.raises(ErrorFicha, match="fuente"):
        _correr("SCN-H-001", {"rendimientos": datos["rendimientos"], "garch": {**g, "fuente": None}},
                {"semilla": 2, "clase": "RV"})
    with pytest.raises(ErrorFicha, match="integrado"):
        _correr("SCN-H-001", {"rendimientos": datos["rendimientos"], "garch": {**g, "beta": 0.95}},
                {"semilla": 2, "clase": "RV"})


# ============================================================================= BT-DSR-001
def test_bt_dsr_rechazos():
    v = {"rendimientos": _rendimientos(300), "varianza_sr_ensayos": {"valor": 0.5, "unidad": "anual"}}
    with pytest.raises(ErrorFicha, match="aclaración: falta N"):
        _correr("BT-DSR-001", v)
    with pytest.raises(ErrorFicha, match="249"):
        _correr("BT-DSR-001", {**v, "rendimientos": _rendimientos(249)}, {"N": 3})
    with pytest.raises(ErrorFicha, match="23 rendimientos con frecuencia mensual"):
        _correr("BT-DSR-001", {**v, "rendimientos": _rendimientos(23)}, {"N": 3, "frecuencia": "mensual"})
    _correr("BT-DSR-001", {**v, "rendimientos": _rendimientos(24)}, {"N": 3, "frecuencia": "mensual"})
    with pytest.raises(ErrorFicha, match="varianza_sr_ensayos"):
        _correr("BT-DSR-001", {"rendimientos": _rendimientos(300)}, {"N": 3})
    with pytest.raises(ErrorFicha, match="unidad"):
        _correr("BT-DSR-001", {**v, "varianza_sr_ensayos": {"valor": 0.5, "unidad": "semanal"}}, {"N": 3})
    with pytest.raises(ErrorFicha, match="dispersión"):
        _correr("BT-DSR-001", {**v, "rendimientos": [0.001] * 300}, {"N": 3})


def test_bt_dsr_oraculo_a_mano():
    """PSR, SR*₀, DSR y MinTRL con momentos calculados en Python puro y la normal de `statistics`."""
    x = [e + 0.0008 for e in R._colas_gruesas(400, 5)]
    T = len(x)
    m = sum(x) / T
    s = math.sqrt(sum((e - m) ** 2 for e in x) / (T - 1))
    m2 = sum((e - m) ** 2 for e in x) / T
    g3 = (sum((e - m) ** 3 for e in x) / T) / m2 ** 1.5 * math.sqrt(T * (T - 1)) / (T - 2)
    g2 = (sum((e - m) ** 4 for e in x) / T) / m2 ** 2 - 3
    g4 = ((T + 1) * g2 + 6) * (T - 1) / ((T - 2) * (T - 3)) + 3      # curtosis sin sesgo (fórmula de Fisher)
    sr = m / s
    nd = statistics.NormalDist()
    den = 1 - g3 * sr + (g4 - 1) / 4 * sr * sr
    ee = math.sqrt(den / (T - 1))
    sr_ref = 0.3 / math.sqrt(252)
    v = 0.8 / 252
    sr0 = math.sqrt(v) * ((1 - 0.5772156649015329) * nd.inv_cdf(1 - 1 / 30) + 0.5772156649015329 * nd.inv_cdf(1 - 1 / (30 * math.e)))
    res, _ = _correr("BT-DSR-001", {"rendimientos": x, "varianza_sr_ensayos": {"valor": 0.8, "unidad": "anual"}},
                     {"N": 30, "SR_referencia": 0.3})
    assert res["sr_anual"] == pytest.approx(sr * math.sqrt(252), rel=1e-12)
    assert res["asimetria"] == pytest.approx(g3, rel=1e-9) and res["curtosis"] == pytest.approx(g4, rel=1e-9)
    assert res["psr"] == pytest.approx(nd.cdf((sr - sr_ref) / ee), rel=1e-9)
    assert res["sr0_periodo"] == pytest.approx(sr0, rel=1e-9)
    assert res["dsr"] == pytest.approx(nd.cdf((sr - sr0) / ee), rel=1e-9)
    if sr > sr_ref:
        assert res["min_trl_periodos"] == pytest.approx(1 + den * (nd.inv_cdf(0.95) / (sr - sr_ref)) ** 2, rel=1e-9)
    # Lo (2002), AR(1): η(q) = q/√(q + 2ρ/(1 − ρ)²·[(q − 1)(1 − ρ) − ρ(1 − ρ^(q−1))])
    rho, q = res["autocorrelacion_1"], 252
    eta = q / math.sqrt(q + 2 * rho / (1 - rho) ** 2 * ((q - 1) * (1 - rho) - rho * (1 - rho ** (q - 1))))
    assert res["sr_anual_lo"] == pytest.approx(sr * eta, rel=1e-9)


def test_bt_dsr_mensual_y_cripto():
    x = _rendimientos(36, 3, 0.04)
    v = {"rendimientos": [e + 0.01 for e in x], "varianza_sr_ensayos": {"valor": 1e-3, "unidad": "periodo"}}
    res, _ = _correr("BT-DSR-001", v, {"N": 5, "frecuencia": "mensual"})
    assert res["periodos_anio"] == 12 and res["varianza_sr_ensayos_periodo"] == 1e-3
    res, _ = _correr("BT-DSR-001", {**v, "rendimientos": _rendimientos(300)}, {"N": 5, "clase": "CRI"})
    assert res["periodos_anio"] == 365


# ============================================================================= BT-PBO-001
def test_bt_pbo_rechazos():
    with pytest.raises(ErrorFicha, match="1 configuraciones"):
        _correr("BT-PBO-001", {"rendimientos": R._pbo_ruido(1, 64, 1)}, {"S": 8})
    with pytest.raises(ErrorFicha, match="T = 31"):
        _correr("BT-PBO-001", {"rendimientos": R._pbo_ruido(3, 31, 1)}, {"S": 8})
    with pytest.raises(ErrorFicha, match="longitud"):
        _correr("BT-PBO-001", {"rendimientos": {"a": _rendimientos(64), "b": _rendimientos(63)}}, {"S": 8})
    res, lim = _correr("BT-PBO-001", {"rendimientos": R._pbo_ruido(3, 67, 1)}, {"S": 8})
    assert res["T_usado"] == 64 and any("3 observaciones más antiguas" in x for x in lim)
    assert any("(< 10)" in x for x in lim)


def _sharpe(x):
    return statistics.fmean(x) / statistics.stdev(x)


def test_bt_pbo_oraculo_cscv_por_fuerza_bruta():
    """CSCV de Bailey et al. (2017) con bucles de Python: combinaciones, mejor dentro, rango fuera, λ y PBO."""
    M = R._pbo_ruido(5, 80, 13)
    nombres = sorted(M)
    S, b = 8, 10
    bloques = {k: [M[k][i * b:(i + 1) * b] for i in range(S)] for k in nombres}
    lams, perdidas, is_m, oos_m = [], [], [], []
    for c in itertools.combinations(range(S), S // 2):
        dentro = {k: _sharpe([e for i in c for e in bloques[k][i]]) for k in nombres}
        fuera = {k: _sharpe([e for i in range(S) if i not in c for e in bloques[k][i]]) for k in nombres}
        mejor = max(nombres, key=lambda k: dentro[k])
        orden = sorted(fuera.values())
        rango = orden.index(fuera[mejor]) + 1
        w = rango / (len(nombres) + 1)
        lams.append(math.log(w / (1 - w)))
        perdidas.append(fuera[mejor] < 0)
        is_m.append(dentro[mejor])
        oos_m.append(fuera[mejor])
    res, _ = _correr("BT-PBO-001", {"rendimientos": M}, {"S": 8})
    assert res["pbo"] == pytest.approx(sum(1 for x in lams if x <= 0) / len(lams), abs=1e-12)
    assert res["probabilidad_perdida"] == pytest.approx(sum(perdidas) / len(perdidas), abs=1e-12)
    assert res["lambda"]["media"] == pytest.approx(statistics.fmean(lams), rel=1e-10)
    mx, my = statistics.fmean(is_m), statistics.fmean(oos_m)
    pend = sum((a - mx) * (c - my) for a, c in zip(is_m, oos_m)) / sum((a - mx) ** 2 for a in is_m)
    assert res["pendiente_degradacion"] == pytest.approx(pend, rel=1e-8)


def test_bt_pbo_sin_habilidad_en_media_es_un_medio():
    """El PBO de un conjunto sin habilidad varía mucho entre conjuntos; su media sobre 16 conjuntos queda cerca de 0,5."""
    pbos = [_correr("BT-PBO-001", {"rendimientos": R._pbo_ruido(10, 160, s)}, {"S": 8})[0]["pbo"] for s in range(16)]
    assert abs(statistics.fmean(pbos) - 0.5) <= 3 * statistics.stdev(pbos) / 4


# ============================================================================= BT-VAR-001
def test_bt_var_rechazos_y_baja_potencia():
    v = R._var_espaciado([10, 50], 200, 0.02)
    with pytest.raises(ErrorFicha, match="200 observaciones"):
        _correr("BT-VAR-001", v)
    res, lim = _correr("BT-VAR-001", v, {"baja_potencia_declarada": True})
    assert any("baja potencia declarada" in x for x in lim) and res["excedencias"]["n"] == 2
    with pytest.raises(ErrorFicha, match="no alinean"):
        _correr("BT-VAR-001", {"var_previsto": [0.02] * 300, "resultados": [0.0] * 299})
    with pytest.raises(ErrorFicha, match="no alinean"):
        _correr("BT-VAR-001", {"var_previsto": [0.02] * 300, "resultados": [0.0] * 300, "es_previsto": [0.03] * 10})
    with pytest.raises(ErrorFicha, match="ES previsto no positivo"):
        _correr("BT-VAR-001", {"var_previsto": [0.02] * 300, "resultados": [0.0] * 300, "es_previsto": [0.0] * 300})
    with pytest.raises(ErrorFicha, match="horizonte 1"):
        _correr("BT-VAR-001", {"rendimientos": _rendimientos(600)}, {"horizonte": 5})
    with pytest.raises(ErrorFicha, match="ventana"):
        _correr("BT-VAR-001", {"rendimientos": _rendimientos(250)})


def test_bt_var_oraculo_binomial_markov_y_semaforo():
    """LR_uc con la verosimilitud binomial de scipy, LR_ind con una cadena de Markov a mano y zonas de Basilea por la
    probabilidad binomial acumulada (BCBS 1996: verde < 95 %, amarilla < 99,99 %)."""
    rng = np.random.default_rng(8)
    T = 500
    res_ = [float(x) for x in 0.01 * rng.standard_t(4, T)]
    var = [0.022] * T
    r, _ = _correr("BT-VAR-001", {"var_previsto": var, "resultados": res_}, {"nivel": 0.99})
    exc = [1 if a < -b else 0 for a, b in zip(res_, var)]
    x, p = sum(exc), 0.01
    lr_uc = 2 * (stats.binom.logpmf(x, T, x / T) - stats.binom.logpmf(x, T, p))
    assert r["lr_uc"] == pytest.approx(lr_uc, rel=1e-10) and r["p_uc"] == pytest.approx(stats.chi2.sf(lr_uc, 1), rel=1e-10)
    cuenta = {(a, b): 0 for a in (0, 1) for b in (0, 1)}
    for a, b in itertools.pairwise(exc):
        cuenta[(a, b)] += 1

    def ll(prob, k0, k1):
        return (k0 * math.log(1 - prob) if k0 else 0.0) + (k1 * math.log(prob) if k1 else 0.0)
    n00, n01, n10, n11 = cuenta[(0, 0)], cuenta[(0, 1)], cuenta[(1, 0)], cuenta[(1, 1)]
    pi = (n01 + n11) / (T - 1)
    l1 = ll(n01 / (n00 + n01), n00, n01) + (ll(n11 / (n10 + n11), n10, n11) if n10 + n11 else 0.0)
    assert r["lr_ind"] == pytest.approx(-2 * (ll(pi, n00 + n10, n01 + n11) - l1), rel=1e-10, abs=1e-12)
    assert r["lr_cc"] == pytest.approx(r["lr_uc"] + r["lr_ind"], rel=1e-12)
    zonas = {k: ("verde" if stats.binom.cdf(k, 250, 0.01) < 0.95 else "amarilla" if stats.binom.cdf(k, 250, 0.01) < 0.9999
                 else "roja") for k in range(251)}
    assert [k for k in range(15) if zonas[k] == "verde"] == list(range(R.UMBRALES["BT-VAR-001"]["verde_max"] + 1))
    assert max(k for k in range(15) if zonas[k] == "amarilla") == R.UMBRALES["BT-VAR-001"]["amarilla_max"]
    assert r["zona_semaforo"] == zonas[sum(exc[-250:])]


@pytest.mark.parametrize("k,zona", [(0, "verde"), (4, "verde"), (5, "amarilla"), (9, "amarilla"), (10, "roja")])
def test_bt_var_zonas_del_semaforo_en_sus_bordes(k, zona):
    """BCBS (1996): 250 días al 99 %, verde 0–4, amarilla 5–9, roja ≥ 10 excedencias (en los últimos 250 días)."""
    v = R._var_espaciado(list(range(60, 60 + 23 * k, 23)), 300, 0.02)
    v["resultados"][:50] = [-0.05] * 50                     # excedencias fuera de la ventana de 250 días: no cuentan
    r, _ = _correr("BT-VAR-001", v, {"nivel": 0.99})
    assert r["zona_semaforo"] == zona


def test_bt_var_generado_ex_ante_con_risk_var():
    hist = R._colas_gruesas(700, 17)
    r, _ = _correr("BT-VAR-001", {"rendimientos": hist}, {"ventana_estimacion": 300})
    assert r["modo"] == "generado con RISK-VAR-001" and r["n"] == 400
    # Oráculo de no anticipación: el VaR de t solo usa hist[t − 300:t] (cuantil tipo 7 a mano)
    excedencias = sum(1 for t in range(300, 700) if hist[t] < _cuantil_tipo7(hist[t - 300:t], 0.025))
    assert r["excedencias"]["n"] == excedencias
    nd = [statistics.stdev(hist[t - 300:t]) * statistics.NormalDist().inv_cdf(0.975) for t in range(300, 700)]
    assert r["referencia_ingenua"]["excedencias"]["n"] == sum(1 for t, v in zip(range(300, 700), nd) if hist[t] < -v)


# ============================================================================= ML-CAL-001
def test_ml_cal_rechazos():
    h = R._cal_nivel()
    with pytest.raises(ErrorFicha, match="ensayos"):
        _correr("ML-CAL-001", {"horizontes": {"H2": h}})
    with pytest.raises(ErrorFicha, match="no alinean"):
        _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H2": {**h, "predicciones": h["predicciones"][:-1]}}})
    fechas = [str(d.date()) for d in pd.bdate_range("2024-01-01", periods=40)]
    pred = [{"fecha": f, "valor": x} for f, x in zip(fechas, h["predicciones"])]
    real = [{"fecha": f, "valor": x} for f, x in zip(fechas[1:] + ["2030-01-01"], h["realizaciones"])]
    with pytest.raises(ErrorFicha, match="fechas distintas"):
        _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H2": {"tipo": "nivel", "predicciones": pred, "realizaciones": real}}})
    with pytest.raises(ErrorFicha, match="29 pares"):
        _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H2": {"tipo": "nivel", "predicciones": h["predicciones"][:29],
                                                                    "realizaciones": h["realizaciones"][:29]}}})
    p = R._cal_prob()
    with pytest.raises(ErrorFicha, match="solape"):
        _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H3": {**p, "particiones": [{"entrenamiento": [0, 20], "prueba": [15, 30]}]}}})
    with pytest.raises(ErrorFicha, match="embargo"):
        _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H3": {**p, "embargo": 3}}})
    with pytest.raises(ErrorFicha, match="expansivo"):
        _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H3": {**p, "particiones": [
            {"entrenamiento": [0, 9], "prueba": [12, 29]}, {"entrenamiento": [5, 27], "prueba": [30, 49]}]}}})
    with pytest.raises(ErrorFicha, match="no binarias"):
        _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H3": {**p, "predicciones": [1.2] * 50}}})
    with pytest.raises(ErrorFicha, match="sin datos"):
        _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H3": p}}, {"horizontes": ["H9"]})


def test_ml_cal_alinea_por_fecha_aunque_lleguen_desordenadas():
    h = R._cal_nivel()
    fechas = [str(d.date()) for d in pd.bdate_range("2024-01-01", periods=40)]
    pred = [{"fecha": f, "valor": x} for f, x in zip(fechas, h["predicciones"])]
    real = [{"fecha": f, "valor": x} for f, x in zip(fechas, h["realizaciones"])]
    a, _ = _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H2": {"tipo": "nivel", "predicciones": pred[::-1],
                                                                     "realizaciones": real}}})
    b, _ = _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H2": {"tipo": "nivel", "predicciones": h["predicciones"],
                                                                     "realizaciones": h["realizaciones"]}}})
    assert a["horizontes"]["H2"]["mae"] == b["horizontes"]["H2"]["mae"] and a["horizontes"]["H2"]["fechas"] == [fechas[0], fechas[-1]]


def test_ml_cal_oraculo_referencias_ingenuas_a_mano():
    """Sin referencia aportada: RI-PA (último valor) para niveles y RI-TB (frecuencia expansiva) para probabilidades,
    comparadas desde t = 1; R²_OOS y BSS recalculados con bucles."""
    h = R._cal_nivel()
    y, p = h["realizaciones"], h["predicciones"]
    r, _ = _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H2": {"tipo": "nivel", "predicciones": p, "realizaciones": y}}})
    sse = sum((y[t] - p[t]) ** 2 for t in range(1, 40))
    sse_ref = sum((y[t] - y[t - 1]) ** 2 for t in range(1, 40))
    c = r["horizontes"]["H2"]
    assert c["referencia"].startswith("RI-PA") and c["comparacion_referencia"]["n"] == 39
    assert c["comparacion_referencia"]["r2_oos"] == pytest.approx(1 - sse / sse_ref, rel=1e-12)
    assert c["mejora_frente_referencia"]["mejora_media"] == pytest.approx((sse_ref - sse) / 39, rel=1e-12)
    q = R._cal_prob()
    pp, o = q["predicciones"], q["realizaciones"]
    r, _ = _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H3": {"tipo": "probabilidad", "predicciones": pp, "realizaciones": o}}})
    tb = [sum(o[:t]) / t for t in range(1, 50)]
    b_mod = sum((pp[t] - o[t]) ** 2 for t in range(1, 50)) / 49
    b_ref = sum((tb[t - 1] - o[t]) ** 2 for t in range(1, 50)) / 49
    assert r["horizontes"]["H3"]["comparacion_referencia"]["bss"] == pytest.approx(1 - b_mod / b_ref, rel=1e-12)


def test_ml_cal_ic_por_bootstrap_frente_a_la_aproximacion_normal():
    """Con diferencias de pérdida iid, el IC al 90 % del bootstrap de bloques ≈ media ± z₀,₉₅·s/√n (normal)."""
    rng = np.random.default_rng(23)
    n = H5   # T-118 (H-10): la muestra más larga que admite la cota de observaciones (antes 3 000)
    y = [float(x) for x in rng.standard_normal(n)]
    p = [a + 0.8 * float(rng.standard_normal()) for a in y]
    ref = [a + 1.0 * float(rng.standard_normal()) for a in y]
    r, _ = _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H": {"tipo": "nivel", "predicciones": p,
                                                                    "realizaciones": y, "referencia": ref}}})
    m = r["horizontes"]["H"]["mejora_frente_referencia"]
    d = [(a - c) ** 2 - (a - b) ** 2 for a, b, c in zip(y, p, ref)]
    semi = statistics.NormalDist().inv_cdf(0.95) * statistics.stdev(d) / math.sqrt(n)
    assert m["mejora_media"] == pytest.approx(statistics.fmean(d), rel=1e-10)
    assert (m["ic"][1] - m["ic"][0]) / 2 == pytest.approx(semi, rel=0.10)


def test_ml_cal_ic_por_bloques_contiene_la_mejora_y_se_estrecha_con_n():
    rng = np.random.default_rng(3)
    y = list(np.cumsum(rng.standard_normal(400)))
    p = [a + 0.3 * rng.standard_normal() for a in y]
    r, _ = _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H": {"tipo": "nivel", "predicciones": p, "realizaciones": y}}})
    m = r["horizontes"]["H"]["mejora_frente_referencia"]
    assert m["ic"][0] <= m["mejora_media"] <= m["ic"][1] and m["bloque"] == round(399 ** (1 / 3))
    r2, _ = _correr("ML-CAL-001", {"ensayos": 1, "horizontes": {"H": {"tipo": "nivel", "predicciones": p[:60], "realizaciones": y[:60]}}})
    m2 = r2["horizontes"]["H"]["mejora_frente_referencia"]
    assert m2["ic"][1] - m2["ic"][0] > m["ic"][1] - m["ic"][0]


# ============================================================================= ML-PRED-001
def test_ml_pred_rechazos():
    v = R._pred_datos(True, 1)
    fuga = copy.deepcopy(v)
    fuga["variables"]["x"]["conocible_desde"] = v["fechas"][1:] + ["2030-01-01"]
    with pytest.raises(ErrorFicha, match="fuga"):
        _correr("ML-PRED-001", fuga)
    sin = copy.deepcopy(v)
    del sin["variables"]["x"]["conocible_desde"]
    with pytest.raises(ErrorFicha, match="conocibilidad"):
        _correr("ML-PRED-001", sin)
    with pytest.raises(ErrorFicha, match="independientes"):
        _correr("ML-PRED-001", R._pred_datos(True, 1, n=60))
    largo = copy.deepcopy(v)
    largo["objetivo"]["horizonte"] = 5
    with pytest.raises(ErrorFicha, match="embargo 2 < horizonte 5"):
        _correr("ML-PRED-001", largo, {"embargo": 2})
    with pytest.raises(ErrorFicha, match="no corresponde"):
        _correr("ML-PRED-001", v, {"modelo": "ridge"})
    sin_criterio = copy.deepcopy(v)
    sin_criterio["objetivo"]["criterio_resolucion"] = " "
    with pytest.raises(ErrorFicha, match="criterio"):
        _correr("ML-PRED-001", sin_criterio)
    desordenado = copy.deepcopy(v)
    desordenado["fechas"][5], desordenado["fechas"][6] = desordenado["fechas"][6], desordenado["fechas"][5]
    with pytest.raises(ErrorFicha, match="crecientes"):
        _correr("ML-PRED-001", desordenado)


def _logistica_scipy(X, y, lam):
    Z = np.column_stack([np.ones(len(X)), X])

    def obj(w):
        eta = Z @ w
        return float(np.sum(np.logaddexp(0, eta) - y * eta) + 0.5 * lam * np.sum(w[1:] ** 2))
    return optimize.minimize(obj, np.zeros(Z.shape[1]), method="BFGS", options={"gtol": 1e-10}).x


def test_ml_pred_oraculo_logistica_y_prediccion_actual():
    """La predicción actual (sin calibrar, un λ) coincide con una logística L2 ajustada con scipy sobre las etiquetas
    conocidas en la última fecha (i ≤ n − 1 − embargo), con las variables estandarizadas con esa misma ventana."""
    v = R._pred_datos(True, 5)
    res, _ = _correr("ML-PRED-001", v, {"rejilla": [2.0], "calibracion": "ninguna", "embargo": 3})
    serie = np.array(v["objetivo"]["serie"])
    X = np.column_stack([v["variables"][k]["serie"] for k in sorted(v["variables"])])
    n = len(serie)
    y = (serie[1:] > serie[:-1]).astype(float)
    fin = n - 1 - 3
    Xe, ye = X[:fin + 1], y[:fin + 1]
    mu, sd = Xe.mean(axis=0), Xe.std(axis=0, ddof=1)
    w = _logistica_scipy((Xe - mu) / sd, ye, 2.0)
    p = 1 / (1 + math.exp(-(w[0] + ((X[-1] - mu) / sd) @ w[1:])))
    assert res["prediccion_actual"]["probabilidad"] == pytest.approx(p, rel=1e-5)


def test_ml_pred_oraculo_ridge_nivel():
    v = R._pred_datos(True, 6)
    v["objetivo"]["tipo"] = "nivel"
    res, _ = _correr("ML-PRED-001", v, {"modelo": "ridge", "rejilla": [0.5]})
    serie = np.array(v["objetivo"]["serie"])
    X = np.column_stack([v["variables"][k]["serie"] for k in sorted(v["variables"])])
    y = serie[1:] / serie[:-1] - 1
    fin = len(serie) - 1 - 1
    Xe, ye = X[:fin + 1], y[:fin + 1]
    mu, sd = Xe.mean(axis=0), Xe.std(axis=0, ddof=1)
    Z = np.column_stack([np.ones(len(Xe)), (Xe - mu) / sd])
    aum = np.vstack([Z, np.sqrt(0.5) * np.eye(Z.shape[1])[1:]])         # ridge como mínimos cuadrados aumentados
    w = np.linalg.lstsq(aum, np.r_[ye, np.zeros(Z.shape[1] - 1)], rcond=None)[0]
    assert res["prediccion_actual"]["nivel"] == pytest.approx(w[0] + ((X[-1] - mu) / sd) @ w[1:], rel=1e-8)
    assert res["referencia"].startswith("RI-MH") and "rmse" in res["metricas_oos"]


def test_ml_pred_no_anticipa_cambiar_el_futuro_no_cambia_el_pasado():
    """Las predicciones fuera de muestra del primer pliegue no dependen de datos posteriores a su prueba."""
    v = R._pred_datos(True, 7)
    a, _ = _correr("ML-PRED-001", v, {"calibracion": "ninguna"})
    fin = a["particiones"][0]["prueba"][1]
    w = copy.deepcopy(v)
    for k in range(fin + 2, len(w["fechas"])):
        w["objetivo"]["serie"][k] *= 1.5
        w["variables"]["x"]["serie"][k] = -w["variables"]["x"]["serie"][k]
    b, _ = _correr("ML-PRED-001", w, {"calibracion": "ninguna"})
    pa = [x["prediccion"] for x in a["predicciones_oos"] if x["indice"] <= fin]
    pb = [x["prediccion"] for x in b["predicciones_oos"] if x["indice"] <= fin]
    assert pa == pb and a["predicciones_oos"] != b["predicciones_oos"]


def test_ml_pred_isotonica_monotona_y_segunda_via():
    v = R._pred_datos(True, 8)
    res, _ = _correr("ML-PRED-001", v, {"calibracion": "isotonica"})
    assert res["segunda_via_ventana_movil"]["n"] == res["metricas_oos"]["n"]
    _, vs = R._isotonica(np.array([0.1, 0.2, 0.3, 0.4, 0.5]), np.array([0, 1, 0, 1, 1]))
    assert list(vs) == sorted(vs) and vs[0] == 0 and vs[-1] == 1


# ============================================================================= DEC-VOI-001
def test_dec_voi_rechazos():
    with pytest.raises(ErrorFicha, match="aclaración"):
        _correr("DEC-VOI-001", {"puntuacion": {"dimension": "E", "actual": 58}}, {"coste_uc": 1})
    with pytest.raises(ErrorFicha, match="coste_uc"):
        _correr("DEC-VOI-001", R._VOI_U)
    with pytest.raises(ErrorFicha, match="vacío"):
        _correr("DEC-VOI-001", {**R._VOI_U, "rango_plausible": {"inferior": 60, "superior": 60, "fuente": "x"}}, {"coste_uc": 1})
    with pytest.raises(ErrorFicha, match="dimension"):
        _correr("DEC-VOI-001", {**R._VOI_U, "puntuacion": {"dimension": "Z", "actual": 1}}, {"coste_uc": 1})
    with pytest.raises(ErrorFicha, match="fuente"):
        _correr("DEC-VOI-001", {**R._VOI_U, "rango_plausible": {"inferior": 50, "superior": 70}}, {"coste_uc": 1})


def test_dec_voi_oraculo_evsi_por_integracion_directa():
    """EVSI = ∫ f_X(x)·máx(E[S | x] − u, 0) dx − máx(E[S] − u, 0), con E[S | x] por cuadratura (sin el corte x*)."""
    lo, hi, u, sig = 52.0, 66.0, 60.0, 3.0
    res, _ = _correr("DEC-VOI-001", {**R._VOI_U, "verosimilitud": {"desviacion": sig}}, {"coste_uc": 0.5})

    def fx(x):
        return (stats.norm.cdf((hi - x) / sig) - stats.norm.cdf((lo - x) / sig)) / (hi - lo)

    def media(x):
        num = integrate.quad(lambda s: s * stats.norm.pdf((x - s) / sig), lo, hi)[0]
        den = integrate.quad(lambda s: stats.norm.pdf((x - s) / sig), lo, hi)[0]
        return num / den
    valor = integrate.quad(lambda x: fx(x) * max(media(x) - u, 0.0), lo - 8 * sig, hi + 8 * sig, limit=200)[0]
    assert res["decisiones"][0]["evsi"] == pytest.approx(valor - max((lo + hi) / 2 - u, 0), rel=1e-6)


def test_dec_voi_oraculo_monte_carlo_evpi_y_conversion_uc():
    rng = np.random.default_rng(12)
    s = rng.uniform(52, 66, 400_000)
    evpi_mc = float(np.mean(np.maximum(s - 60, 0)) - max(s.mean() - 60, 0))
    res, lim = _correr("DEC-VOI-001", {**R._VOI_U, "valor_punto_uc": 0.2}, {"coste_uc": 0.5})
    d = res["decisiones"][0]
    assert d["evpi"] == pytest.approx(evpi_mc, abs=0.01) and d["evsi"] is None and res["medida"] == "EVPI"
    assert res["voi_uc"] == pytest.approx(0.2 * d["evpi"], rel=1e-12)
    assert res["recomendacion_tecnica"] == ("EJECUTAR" if 0.2 * d["evpi"] > 0.5 else "NO_EJECUTAR")
    assert any("EVSI no calculado" in x for x in lim)


def test_dec_voi_top3_y_regla_simple():
    base = {"puntuacion": {"dimension": "A", "actual": 75.0},
            "rango_plausible": {"inferior": 70.0, "superior": 80.0, "fuente": "s"}}
    r, _ = _correr("DEC-VOI-001", {**base, "ranking": {"rk_opcion": 62.0, "rk_frontera": 60.0, "amplitud_rk": 5.0}},
                   {"coste_uc": 0.0})
    top3 = r["decisiones"][-1]
    assert top3["decision"].startswith("orden del top-3") and top3["alcanza_banda_marginal"]
    assert top3["evpi"] == pytest.approx((67 - 60) ** 2 / (2 * 10) - (62 - 60), abs=1e-12)
    assert not r["regla_simple_voi_cero"] and r["voi_puntos"] == top3["evpi"]
    banda = {**base, "rango_plausible": {"inferior": 56.0, "superior": 58.0, "fuente": "s"}}
    r, _ = _correr("DEC-VOI-001", banda, {"coste_uc": 0.0})     # alcanza la banda 50–60 pero no cruza 55 ⇒ EVPI 0
    assert not r["regla_simple_voi_cero"] and r["voi_puntos"] == 0 and r["recomendacion_tecnica"] == "NO_EJECUTAR"


# ============================================================================= QA r01 de T-112 (ronda r02)
H5 = sesiones_horizonte(None, "H5")          # 120 meses × 21 sesiones = 2 520 (la cota del horizonte)


class _Proveedor:
    as_of = None
    nombre = "pruebas"


def _motor(tmp_path, extra=None):
    return servicio.Motor(Almacen(Path(tmp_path)), _Proveedor(), cargar_config(extra=extra))


def _correr_cfg(ficha, valores, params=None, cfg=None):
    return R.FICHAS[ficha]["fn"]({**_ent(valores), "configuracion": cfg, "fecha_corte": None}, dict(params or {}))


# --- H-01: cota superior de cada tamaño de la petición (una prueba por cota)
COTAS: list[tuple[str, dict, dict]] = [
    # (ficha, parámetros admitidos en la cota, parámetros que la superan)
    ("RISK-VAR-001", {"horizonte": H5}, {"horizonte": H5 + 1}),
    ("BT-VAR-001", {"horizonte": H5}, {"horizonte": H5 + 1}),
    ("SIM-MC-001", {"horizonte": H5, "n_trayectorias": 10_000, "semilla": 1}, {"horizonte": H5 + 1, "semilla": 1}),
    ("SIM-MC-001", {"horizonte": 25, "n_trayectorias": 1_000_000, "semilla": 1},
     {"horizonte": 26, "n_trayectorias": 1_000_000, "semilla": 1}),                      # presupuesto 10 000 × H5
    ("SIM-MC-001", {"horizonte": 1, "semilla": 1, "cuantiles": [i / 100 for i in range(1, 100)]},
     {"horizonte": 1, "semilla": 1, "cuantiles": [i / 101 for i in range(1, 101)]}),
    ("SIM-MC-001", {"horizonte": 1, "semilla": 1, "umbrales": list(range(99))},
     {"horizonte": 1, "semilla": 1, "umbrales": list(range(100))}),
    ("SCN-H-001", {"semilla": 1, "clase": "RV", "n_trayectorias": 1_000_000},
     {"semilla": 1, "clase": "RV", "n_trayectorias": 1_000_002}),
    ("SCN-H-001", {"semilla": 1, "clase": "RV", "cuantiles": [i / 100 for i in range(1, 100)]},
     {"semilla": 1, "clase": "RV", "cuantiles": [i / 101 for i in range(1, 101)]}),
    ("SCN-H-001", {"semilla": 1, "clase": "RV", "umbrales": list(range(99))},
     {"semilla": 1, "clase": "RV", "umbrales": list(range(100))}),
    ("BT-PBO-001", {"S": 20}, {"S": 22}),
    ("ML-CAL-001", {"replicas": 10_000}, {"replicas": 10_001}),
    ("ML-PRED-001", {"replicas": 10_000}, {"replicas": 10_001}),
    ("ML-PRED-001", {"pliegues": 20}, {"pliegues": 21}),
    ("ML-PRED-001", {"rejilla": [float(x) for x in range(1, 21)]}, {"rejilla": [float(x) for x in range(1, 22)]}),
]


@pytest.mark.parametrize("ficha,dentro,fuera", COTAS, ids=[f"{f}:{sorted(d)}" for f, d, _ in COTAS])
def test_cada_tamano_tiene_cota_superior(ficha, dentro, fuera):
    """La validación admite el tamaño en su cota y rechaza el siguiente (sin calcular: `_parametros`)."""
    R._parametros(ficha, dentro)
    with pytest.raises(ErrorFicha, match="máximo|presupuesto|fuera del rango|rejilla de 1 a"):
        R._parametros(ficha, fuera)


@pytest.mark.parametrize("ficha,clave", [("ML-CAL-001", "replicas"), ("ML-PRED-001", "replicas"),
                                         ("ML-PRED-001", "pliegues"), ("SIM-MC-001", "horizonte"),
                                         ("RISK-VAR-001", "horizonte"), ("BT-VAR-001", "horizonte"),
                                         ("SCN-H-001", "n_trayectorias"), ("SIM-MC-001", "n_trayectorias")])
@pytest.mark.parametrize("valor", [20261110, 10 ** 12, 1e308])
def test_tamanos_desmesurados_se_rechazan_sin_calcular(ficha, clave, valor):
    """El caso de H-01: un número grande en un CT-09 no agota la memoria ni cuelga el proceso."""
    v, p = BASE[ficha]
    with pytest.raises(ErrorFicha):
        _correr(ficha, v, {**p, clave: valor, **({"semilla": 1} if ficha == "SIM-MC-001" else {})})


def test_cota_del_horizonte_sale_de_la_configuracion_del_motor():
    """La cota es H5 en sesiones de la configuración del Motor: con H5 de 60 meses (1 260 sesiones), 1 261 se rechaza."""
    cfg = cargar_config(extra={"horizontes": {"H5": {"meses": 60}}})
    tope = sesiones_horizonte(cfg, "H5")
    v, p = BASE["RISK-VAR-001"]
    assert tope == 1260 and _correr_cfg("RISK-VAR-001", v, {**p, "horizonte": tope}, cfg)[0]["horizonte"] == tope
    with pytest.raises(ErrorFicha, match="máximo 1260"):
        _correr_cfg("RISK-VAR-001", v, {**p, "horizonte": tope + 1}, cfg)
    assert _correr("RISK-VAR-001", v, {**p, "horizonte": tope + 1})[0]["horizonte"] == tope + 1   # por defecto, 2 520


@pytest.mark.parametrize("clave,valor", [("replicas", 20261110), ("horizonte", 20261110), ("pliegues", 10 ** 9)])
def test_por_el_motor_un_tamano_desmesurado_es_rechazado_y_queda_en_rc(tmp_path, clave, valor):
    ficha = {"replicas": "ML-CAL-001", "horizonte": "SIM-MC-001", "pliegues": "ML-PRED-001"}[clave]
    m = _motor(tmp_path)
    caso = R.CASOS_CONTROL[ficha][0]
    antes = len(m.almacen.leer("RC"))
    r = m.servir({"operacion": ficha, "datos": copy.deepcopy(caso["datos"]),
                  "parametros": {**caso["parametros"], clave: valor}}, "AG-18")
    assert r["estado"] == "RECHAZADO" and "máximo" in r["detalle"] and len(m.almacen.leer("RC")) == antes + 1


def test_bootstrap_por_tandas_da_lo_mismo_que_de_una_vez(monkeypatch):
    """La memoria del bootstrap se acota por tandas de réplicas sin cambiar el resultado (bit a bit)."""
    rng = np.random.default_rng(4)
    a, b = rng.standard_normal(700), rng.standard_normal(700)
    entero = R.mejora_ic(a, b, 3000, 0.9, 11)
    monkeypatch.setattr(R, "_ELEMENTOS_TANDA", 500)
    assert R.mejora_ic(a, b, 3000, 0.9, 11) == entero
    # y frente a la expresión de una vez, hecha aquí
    d, n = a - b, 700
    blq = max(1, round(n ** (1 / 3)))
    ini = np.random.default_rng(11).integers(0, n - blq + 1, size=(3000, math.ceil(n / blq)))
    medias = d[(ini[:, :, None] + np.arange(blq)[None, None, :]).reshape(3000, -1)[:, :n]].mean(axis=1)
    cola = (1 - 0.9) / 2
    assert entero["ic"] == [float(np.quantile(medias, cola)), float(np.quantile(medias, 1 - cola))]


def test_cscv_por_tandas_da_lo_mismo_que_de_una_vez(monkeypatch):
    v = {"rendimientos": R._pbo_ruido(6, 160, 21)}
    entero, _ = _correr("BT-PBO-001", v, {"S": 10})
    for elementos in (37, 5 * 10 * 6):                                  # tandas de 1 y de 5 combinaciones (de 252)
        monkeypatch.setattr(R, "_ELEMENTOS_TANDA", elementos)
        assert _correr("BT-PBO-001", v, {"S": 10})[0] == entero


def test_la_ficha_mas_cara_en_su_cota_cabe_en_tiempo():
    """SIM-MC-001 con las trayectorias por defecto hasta H5 (el presupuesto entero) y 99 cuantiles: una pasada en segundos.
    La medida completa (1e6 × 25, SCN-H con 1e6, BT-PBO con S = 20, bootstrap con 10 000 réplicas) está en grupo_R.md."""
    import time
    t0 = time.perf_counter()
    r, _ = _correr("SIM-MC-001", {"dinamica": {"tipo": "paseo_aleatorio", "mu": 0.0, "sigma": 0.01}},
                   {"n_trayectorias": 10_000, "horizonte": H5, "semilla": 3, "cuantiles": [i / 100 for i in range(1, 100)]})
    assert time.perf_counter() - t0 < 30 and len(r["distribucion"]["cuantiles"]) == 99


# --- H-02: un parámetro no declarado (errata) se rechaza en las 9 fichas; `clase` se admite en todas
@pytest.mark.parametrize("ficha", FICHAS)
def test_parametro_con_errata_se_rechaza(ficha):
    v, p = BASE[ficha]
    clave = min(R.PARAMETROS_POR_DEFECTO[ficha])
    errata = clave.upper() if clave.lower() == clave else clave.lower()
    with pytest.raises(ErrorFicha, match="no declarados"):
        _correr(ficha, v, {**p, errata: R.PARAMETROS_POR_DEFECTO[ficha][clave]})
    with pytest.raises(ErrorFicha, match="no declarados"):
        _correr(ficha, v, {**p, "parametro_inexistente": 1})


@pytest.mark.parametrize("ficha", FICHAS)
def test_la_clase_de_la_peticion_se_admite_en_todas(ficha):
    v, p = BASE[ficha]
    _correr(ficha, v, {**p, "clase": p.get("clase", "RV")})


def test_metodo_con_errata_no_se_sirve_con_el_metodo_por_defecto():
    with pytest.raises(ErrorFicha, match="Metodo"):
        _correr("RISK-VAR-001", {"rendimientos": R._R_VAR_NORMAL}, {"Metodo": "evt_pot"})


# --- H-03: máximos de verosimilitud con la precisión de la ficha, frente a referencias propias
def _gpd_perfil(y):
    """MV de la GPD por la verosimilitud perfil de Grimshaw (1993) en θ = ξ/β: ξ(θ) = media(ln(1 + θy)) y
    −ln L(θ) = n·ln(ξ(θ)/θ) + n·(1 + ξ(θ)), minimizada en una variable (otra vía que la de la ficha)."""
    n = len(y)

    def menos_l(t):
        x = np.mean(np.log1p(t * y))
        return n * math.log(x / t) + n * (1 + x)
    res = optimize.minimize_scalar(menos_l, bounds=(-(1 - 1e-12) / y.max(), 1e3 / y.mean()), method="bounded",
                                   options={"xatol": 1e-14, "maxiter": 10_000})
    xi = float(np.mean(np.log1p(res.x * y)))
    return xi, xi / res.x


def _nll_gpd(xi, b, y):
    return len(y) * math.log(b) + (1 + 1 / xi) * float(np.sum(np.log1p(xi * y / b)))


@pytest.mark.parametrize("datos,nivel", [(R._R_VAR_COLAS, 0.975), ("t3", 0.99), ("t5", 0.975)])
def test_evt_pot_es_el_maximo_de_verosimilitud_a_la_tolerancia_de_la_ficha(datos, nivel):
    if isinstance(datos, str):
        datos = [float(x) for x in 0.01 * np.random.default_rng(int(datos[1])).standard_t(int(datos[1]), H5)]   # T-118 (H-10): antes 3 000
    res, _ = _correr("RISK-VAR-001", {"rendimientos": datos}, {"metodo": "evt_pot", "nivel": nivel})
    d = res["detalle_metodo"]
    perd = -np.array(datos)
    u = float(np.quantile(perd, 0.90))
    y = perd[perd > u] - u
    xi, b = _gpd_perfil(y)
    var = u + b / xi * ((len(perd) / len(y) * (1 - nivel)) ** (-xi) - 1)
    es = (var + b - xi * u) / (1 - xi)
    tol = R.FICHAS_TOL["RISK-VAR-001"]
    assert res["var"] == pytest.approx(var, rel=tol) and res["es"] == pytest.approx(es, rel=tol)
    assert d["xi"] == pytest.approx(xi, abs=tol) and d["beta"] == pytest.approx(b, rel=tol)
    assert _nll_gpd(d["xi"], d["beta"], y) <= _nll_gpd(xi, b, y) + 1e-9      # no es peor que la referencia
    # el ajuste por defecto de scipy (fmin con xtol 1e-4) no llegaba a esa precisión en la primera serie (H-03)
    if nivel == 0.975 and len(datos) == len(R._R_VAR_COLAS) and datos == R._R_VAR_COLAS:
        g = stats.genpareto.fit(y, floc=0)
        assert abs(g[0] - xi) > tol


def _garch_referencia(x):
    """QMLE con objetivo de varianza en (α, β) por Powell desde tres arranques, con la recursión en un bucle propio."""
    e = np.asarray(x) - np.mean(x)
    v = float(np.var(e))

    def nll(th):
        a, b = th
        if a <= 0 or b <= 0 or a + b >= 1:
            return 1e12
        h, tot = v, 0.0
        for t in range(len(e)):
            if t:
                h = v * (1 - a - b) + a * e[t - 1] ** 2 + b * h
            tot += math.log(h) + e[t] ** 2 / h
        return 0.5 * tot
    mejor = min((optimize.minimize(nll, x0, method="Powell", options={"xtol": 1e-10, "ftol": 1e-13})
                 for x0 in ([0.05, 0.9], [0.15, 0.8], [0.02, 0.97])), key=lambda o: o.fun)
    return float(mejor.x[0]), float(mejor.x[1]), nll


@pytest.mark.parametrize("serie", ["control", "otra"])
def test_garch_qmle_y_var_filtrado_frente_a_un_optimo_de_referencia(serie):
    """H-03 y H-08 (QR04): el VaR y el ES publicados del histórico filtrado son los de un óptimo de referencia calculado
    aparte, a la tolerancia de la ficha, y ω = σ̄²(1 − α − β)."""
    x = np.array(R._R_VAR_GARCH if serie == "control" else _garch_simulado(5e-6, 0.12, 0.8, 800, 77) + 0.0002)
    res, _ = _correr("RISK-VAR-001", {"rendimientos": x.tolist()}, {"metodo": "historico_filtrado"})
    g = res["detalle_metodo"]["garch"]
    a, b, nll = _garch_referencia(x)
    assert nll([g["alpha"], g["beta"]]) <= nll([a, b]) + 1e-9 * abs(nll([a, b]))
    e = x - x.mean()
    v = float(np.var(e))
    assert g["omega"] == pytest.approx(v * (1 - g["alpha"] - g["beta"]), rel=1e-12)
    hs = [v]
    for t in range(1, len(e)):
        hs.append(v * (1 - a - b) + a * e[t - 1] ** 2 + b * hs[-1])
    z = e / np.sqrt(hs)
    sig = math.sqrt(v * (1 - a - b) + a * e[-1] ** 2 + b * hs[-1])
    q = float(np.quantile(z, 0.025))
    tol = R.FICHAS_TOL["RISK-VAR-001"]
    assert res["var"] == pytest.approx(-(x.mean() + sig * q), rel=tol)
    assert res["es"] == pytest.approx(-(x.mean() + sig * float(np.mean(z[z <= q]))), rel=tol)


def test_caso_fhs_falla_con_omega_sin_objetivo_de_varianza():
    """Contraejemplo del caso de FHS (mutante QR04 del revisor): ω = σ̄²(1 − α) y σ_T+1 rehecha con ese ω."""
    caso = R.CASOS_CONTROL["RISK-VAR-001"][5]
    res, _ = _correr("RISK-VAR-001", _valores_caso(caso), caso["parametros"])
    assert caso["comprobar"](res)
    x = np.array(R._R_VAR_GARCH)
    g = dict(res["detalle_metodo"]["garch"])
    g["omega"] = float(np.var(x - x.mean())) * (1 - g["alpha"])
    var, es, sig = R._fhs_con(x, g["omega"], g["alpha"], g["beta"], 0.975)
    malo = {**res, "var": var, "es": es, "detalle_metodo": {**res["detalle_metodo"], "garch": g, "sigma_siguiente": sig}}
    assert not caso["comprobar"](malo)


@pytest.mark.parametrize("cual", ["gpd", "garch"])
def test_sin_convergencia_del_optimizador_se_rechaza(monkeypatch, cual):
    monkeypatch.setattr(R, "_ITERACIONES_POR_PARAMETRO", 1)
    metodo = "evt_pot" if cual == "gpd" else "historico_filtrado"
    with pytest.raises(ErrorFicha, match="sin convergencia"):
        _correr("RISK-VAR-001", {"rendimientos": R._R_VAR_COLAS}, {"metodo": metodo})


# --- H-04: la configuración del Motor, leída en cada llamada (no la de por defecto al importar)
def test_los_numeros_de_configuracion_no_se_fijan_al_importar():
    for f in ("ML-CAL-001", "ML-PRED-001"):
        assert R.PARAMETROS_POR_DEFECTO[f]["replicas"] is None and R.PARAMETROS_POR_DEFECTO[f]["nivel_ic"] is None
    assert all(isinstance(x, str) for d in R.UMBRALES["DEC-VOI-001"]["umbrales"].values() for x in d.values())


def test_dec_voi_lee_los_umbrales_y_la_banda_de_ht03_de_la_configuracion():
    cfg = cargar_config(extra={"parametros_ht03": {"umbrales": {"E": 62}, "banda_marginal": 2}})
    v = {**R._VOI_U, "verosimilitud": {"desviacion": 0.0}}
    r, _ = _correr_cfg("DEC-VOI-001", v, {"coste_uc": 0.5}, cfg)
    d = next(x for x in r["decisiones"] if x["decision"] == "umbral E (E)")
    assert d["umbral"] == 62 and r["banda_marginal"] == 2
    assert d["evpi"] == pytest.approx((66 - 62) ** 2 / (2 * 14) - max(59 - 62, 0), abs=1e-12)
    r0, _ = _correr("DEC-VOI-001", v, {"coste_uc": 0.5})                       # sin configuración: la de por defecto
    assert next(x for x in r0["decisiones"] if x["decision"] == "umbral E (E)")["umbral"] == parametro(None, "parametros_ht03.umbrales")["E"]
    # la banda de la configuración decide la regla simple: rango 56–58 con A 55 alcanza ±5 pero no ±0,5
    rango = {"puntuacion": {"dimension": "A", "actual": 57.0}, "rango_plausible": {"inferior": 56.0, "superior": 58.0, "fuente": "s"}}
    assert not _correr("DEC-VOI-001", rango, {"coste_uc": 0.0})[0]["regla_simple_voi_cero"]
    estrecha = cargar_config(extra={"parametros_ht03": {"banda_marginal": 0.5}})
    assert _correr_cfg("DEC-VOI-001", rango, {"coste_uc": 0.0}, estrecha)[0]["regla_simple_voi_cero"]


@pytest.mark.parametrize("ficha,caso", [("ML-CAL-001", 0), ("ML-PRED-001", 1)])
def test_ml_cal_y_ml_pred_leen_el_bootstrap_de_la_configuracion(ficha, caso):
    cfg = cargar_config(extra={"evaluacion": {"bootstrap_replicas": 37, "nivel_ic": 0.8}})
    c = R.CASOS_CONTROL[ficha][caso]
    r, _ = _correr_cfg(ficha, _valores_caso(c), c["parametros"], cfg)
    mj = r["mejora_frente_referencia"] if ficha == "ML-PRED-001" else next(iter(r["horizontes"].values()))["mejora_frente_referencia"]
    assert mj["replicas"] == 37 and mj["nivel"] == 0.8
    r2, _ = _correr_cfg(ficha, _valores_caso(c), {**c["parametros"], "replicas": 41}, cfg)   # la petición manda
    mj2 = r2["mejora_frente_referencia"] if ficha == "ML-PRED-001" else next(iter(r2["horizontes"].values()))["mejora_frente_referencia"]
    assert mj2["replicas"] == 41 and mj2["nivel"] == 0.8
    r0, _ = _correr(ficha, _valores_caso(c), c["parametros"])
    mj0 = r0["mejora_frente_referencia"] if ficha == "ML-PRED-001" else next(iter(r0["horizontes"].values()))["mejora_frente_referencia"]
    assert mj0["replicas"] == parametro(None, "evaluacion.bootstrap_replicas")
    with pytest.raises(ErrorFicha, match="máximo"):                           # la cota vale también para la configuración
        _correr_cfg(ficha, _valores_caso(c), c["parametros"], cargar_config(extra={"evaluacion": {"bootstrap_replicas": 10 ** 6}}))


def test_scn_h_lee_las_sesiones_de_los_horizontes_de_la_configuracion():
    cfg = cargar_config(extra={"horizontes": {"H3": {"meses": 3}}})
    c = R.CASOS_CONTROL["SCN-H-001"][2]
    r, _ = _correr_cfg("SCN-H-001", _valores_caso(c), c["parametros"], cfg)
    assert r["horizontes"]["H3"]["pasos_sesiones"] == 3 * parametro(None, "calendario.sesiones_por_mes")


def test_por_el_motor_dec_voi_usa_la_configuracion_del_motor(tmp_path):
    m = _motor(tmp_path, {"parametros_ht03": {"umbrales": {"E": 64}}})
    c = R.CASOS_CONTROL["DEC-VOI-001"][0]
    r = m.servir({"operacion": "DEC-VOI-001", "datos": copy.deepcopy(c["datos"]), "parametros": dict(c["parametros"])}, "AG-18")
    assert r["estado"].startswith("SERVED")
    assert next(x for x in r["resultado"]["decisiones"] if x["decision"] == "umbral E (E)")["umbral"] == 64


def test_configuracion_que_no_es_un_objeto_se_rechaza():
    with pytest.raises(ErrorFicha, match="configuración"):
        R.FICHAS["DEC-VOI-001"]["fn"]({**_ent(R._VOI_U), "configuracion": [1]}, {"coste_uc": 1})
