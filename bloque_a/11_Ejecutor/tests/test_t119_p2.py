"""T-119 · Motor, fichas P2 del Catálogo V5.0: FIR-CRED-001, FX-BEER-001, CMD-REAL-001, REI-LEV-001, CHR-ONCHAIN-001,
CHR-TOKEN-001, PRV-PME-001, PRV-CF-001, ALT-HF-001 y ALT-AUC-001.

Casos de control («Verificación»), rechazos de «Aclaración y rechazo» y de «Entradas mínimas», dominio y cota de cada
parámetro y de cada lista de datos, umbrales fijos, fecha de corte, determinismo, entradas hostiles y oráculos
independientes: cada oráculo recalcula el resultado por otra vía (scipy, pandas, fracciones exactas, bucles explícitos) sin
llamar al código de la ficha."""
import copy
import json
import math
from fractions import Fraction

import numpy as np
import pandas as pd
import pytest
from bloque_a.motor import fichas_p2 as fp
from bloque_a.motor.operaciones import ErrorFicha
from scipy import optimize, stats

pytestmark = pytest.mark.filterwarnings("ignore::RuntimeWarning")   # las entradas hostiles desbordan a propósito

FICHAS_P2 = ["FIR-CRED-001", "FX-BEER-001", "CMD-REAL-001", "REI-LEV-001", "CHR-ONCHAIN-001", "CHR-TOKEN-001",
             "PRV-PME-001", "PRV-CF-001", "ALT-HF-001", "ALT-AUC-001"]


def _ent(valores, corte=None, cfg=None):
    ent = {"valores": copy.deepcopy(valores), "series": {}, "series_rol": {}}
    if corte is not None:
        ent["fecha_corte"] = corte
    if cfg is not None:
        ent["configuracion"] = cfg
    return ent


def _correr(ficha, valores, params=None, corte=None, cfg=None):
    return fp.FICHAS[ficha]["fn"](_ent(valores, corte, cfg), dict(params or {}))


def _valores_caso(caso):
    v = {}
    for d in caso["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    return v


def _base(ficha, i=0):
    caso = fp.CASOS_CONTROL[ficha][i]
    return _valores_caso(caso), dict(caso["parametros"])


# Caso «a mano» de cada ficha (con todos los bloques), para rechazos y oráculos
METODO = {"FIR-CRED-001": 1, "FX-BEER-001": 0, "CMD-REAL-001": 1, "REI-LEV-001": 0, "CHR-ONCHAIN-001": 1,
          "CHR-TOKEN-001": 1, "PRV-PME-001": 1, "PRV-CF-001": 2, "ALT-HF-001": 1, "ALT-AUC-001": 2}


def _metodo(ficha):
    return _base(ficha, METODO[ficha])


CASOS = [(f, c) for f, casos in fp.CASOS_CONTROL.items() for c in casos]
IDS = [f"{f}:{c['nombre'][:60]}" for f, c in CASOS]


def _rechaza(ficha, v, p, motivo, corte=None):
    with pytest.raises(ErrorFicha, match=motivo):
        _correr(ficha, v, p, corte)


# ============================================================================= registro
def test_registro_de_las_diez_fichas():
    for tabla in (fp.FICHAS, fp.PARAMETROS_POR_DEFECTO, fp.UMBRALES, fp.ADVERTENCIAS, fp.CASOS_CONTROL):
        assert sorted(tabla) == sorted(FICHAS_P2)
    tol = {"FIR-CRED-001": 1e-6, "FX-BEER-001": 1e-6, "CMD-REAL-001": 1e-10, "REI-LEV-001": 1e-10, "CHR-ONCHAIN-001": 1e-10,
           "CHR-TOKEN-001": 1e-10, "PRV-PME-001": 1e-8, "PRV-CF-001": 1e-8, "ALT-HF-001": 1e-8, "ALT-AUC-001": 1e-6}
    deterministas = {"REI-LEV-001", "CHR-TOKEN-001", "PRV-PME-001", "PRV-CF-001"}     # «Salidas» de cada ficha
    for f, meta in fp.FICHAS.items():
        assert set(meta) == {"fn", "modulo", "version", "cifra", "ri", "tol"} and callable(meta["fn"])
        assert meta["modulo"] == ("MC-03" if f == "FX-BEER-001" else "MC-09")           # «Identificación»
        assert meta["version"] == ("1.1" if f == "FIR-CRED-001" else "1.0")
        assert meta["cifra"] == ("DETERMINISTA" if f in deterministas else "ESTADISTICA") and meta["ri"]
        assert meta["tol"] == tol[f]                                                    # «Tolerancias y semilla»
    assert all("semilla" not in p for p in fp.PARAMETROS_POR_DEFECTO.values())          # todas declaran semilla null


def test_parametros_por_defecto_y_umbrales_salen_de_la_ficha():
    P, U = fp.PARAMETROS_POR_DEFECTO, fp.UMBRALES
    assert P["FIR-CRED-001"] == {"T": 1, "metodo": "iterativo", "mu": "historico"}
    assert P["FX-BEER-001"] == {"metodo": "DOLS", "retardos": 2}
    assert P["CMD-REAL-001"] == {"deflactor": "ipc_moneda_cotizacion", "percentil_coste": 0.90}
    assert P["REI-LEV-001"] == {"caidas_valor": [-0.10, -0.20], "margen": None}
    assert P["CHR-ONCHAIN-001"] == {"media_nvt": 90, "fuente": None}
    assert P["CHR-TOKEN-001"] == {"ventanas_desbloqueo": [30, 90]}
    assert P["PRV-PME-001"] == {"metodo": "KS-PME", "indice": None}
    assert P["PRV-CF-001"] == {"tasas_aportacion": None, "bow": 2.5, "crecimiento": None}
    assert P["ALT-HF-001"] == {"factores": "Fung-Hsieh 7", "desuavizar": True}
    assert P["ALT-AUC-001"] == {"metodo": "ventas_repetidas", "comisiones": None}
    assert U["FIR-CRED-001"]["componentes_minimos"] == 10 and U["FIR-CRED-001"]["dd_umbral"] == 2
    assert U["FIR-CRED-001"]["factor_deuda_largo"] == 0.5 and U["FIR-CRED-001"]["ingenuo_sigma_deuda"] == (0.05, 0.25)
    assert U["FX-BEER-001"]["anios_rechazo"] == 15 and U["FX-BEER-001"]["anios_entrada_minima"] == 20
    assert len(U["FX-BEER-001"]["fundamentales"]) == 4
    assert U["CMD-REAL-001"]["anios_rechazo"] == 15 and U["CMD-REAL-001"]["anios_entrada_minima"] == 30
    assert U["REI-LEV-001"]["meses_vencimientos"] == 24
    assert U["CHR-ONCHAIN-001"]["dias_minimos"] == 730 and U["CHR-ONCHAIN-001"]["dias_recomendados"] == 1460
    assert U["PRV-CF-001"]["rango_bow"] == (1, 5)
    assert U["ALT-HF-001"]["observaciones_minimas"] == 36 and len(U["ALT-HF-001"]["factores_fung_hsieh"]) == 7
    assert U["ALT-AUC-001"]["transacciones_minimas"] == 500 and U["ALT-AUC-001"]["pares_minimos"] == 200
    assert U["ALT-AUC-001"]["rango_comisiones"] == (0.10, 0.25)


def test_las_cotas_de_tamano_salen_de_las_incidencias():
    """INC-T113-01 (historia ≤ 100 años, listas de parámetros ≤ 12), H5 del Documento 0 (30 años) e INC-T119-01."""
    U = fp.UMBRALES
    assert fp.ANIOS_HISTORIA_MAX == 100 and fp.LISTA_PARAMETRO_MAX == 12 and fp.ANIOS_H5_MAX == 30
    assert all(U[f]["anios_historia_maximos"] == 100 for f in ("FX-BEER-001", "CMD-REAL-001", "PRV-PME-001", "PRV-CF-001",
                                                                "ALT-HF-001", "ALT-AUC-001"))
    assert U["FIR-CRED-001"]["T_maximo_anios"] == U["PRV-CF-001"]["vida_maxima_anios"] == 30
    assert U["CHR-ONCHAIN-001"]["dias_maximos"] == U["CHR-TOKEN-001"]["ventana_dias_maxima"] == 30 * 365
    assert U["REI-LEV-001"]["caidas_maximas"] == U["CHR-TOKEN-001"]["ventanas_maximas"] == U["ALT-HF-001"]["factores_maximos"] == 12
    assert fp.COMPONENTES_MAX == 500 and fp.MAGNITUD_MAX == 1e100
    assert U["FIR-CRED-001"]["componentes_maximos"] == U["REI-LEV-001"]["componentes_maximos"] == U["CHR-TOKEN-001"]["tokens_maximos"] == 500
    assert U["CMD-REAL-001"]["tramos_maximos"] == U["CHR-TOKEN-001"]["desbloqueos_maximos"] == 1000
    assert U["REI-LEV-001"]["vencimientos_maximos"] == 100 and U["ALT-AUC-001"]["caracteristicas_maximas"] == 20
    assert U["PRV-PME-001"]["flujos_maximos"] == U["PRV-CF-001"]["flujos_maximos"] == U["PRV-CF-001"]["navs_maximos"] == 10_000
    assert U["ALT-AUC-001"]["transacciones_maximas"] == 50_000 and U["ALT-AUC-001"]["periodos_minimos"] == 3
    for f in ("FIR-CRED-001", "PRV-PME-001", "PRV-CF-001"):                # tolerancia y tope de las raíces, fijados
        assert U[f]["tolerancia_raiz"] == 1e-13 and U[f]["iteraciones_maximas"] == 200
    assert U["PRV-PME-001"]["rango_tir"] == U["PRV-CF-001"]["rango_tir"] == (-0.99, 10.0)
    assert U["FIR-CRED-001"]["cobertura_minima"] == 0.5 and U["FIR-CRED-001"]["volatilidad_maxima"] == 10.0
    assert U["FX-BEER-001"]["nivel_contraste"] == U["CMD-REAL-001"]["nivel_tendencia"] == 0.05
    assert U["PRV-CF-001"]["rendimiento_minimo"] == 0.0 and U["FX-BEER-001"]["rango_retardos"] == (1, 4)


# ============================================================================= casos de control
@pytest.mark.parametrize("ficha,caso", CASOS, ids=IDS)
def test_casos_de_control(ficha, caso):
    res, lim = _correr(ficha, _valores_caso(caso), caso["parametros"])
    assert caso["comprobar"](res)
    json.dumps(res, allow_nan=False)
    assert res["advertencias"] == fp.ADVERTENCIAS[ficha]
    assert all(isinstance(x, str) for x in lim) and not set(lim) & set(fp.ADVERTENCIAS[ficha])


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


@pytest.mark.parametrize("ficha", FICHAS_P2)
def test_al_menos_tres_casos_de_control_por_ficha(ficha):
    assert len(fp.CASOS_CONTROL[ficha]) >= 3


# ============================================================================= determinismo y no mutación
@pytest.mark.parametrize("ficha,caso", CASOS, ids=IDS)
def test_determinismo_dos_pasadas(ficha, caso):
    v = _valores_caso(caso)
    a = json.dumps(_correr(ficha, v, caso["parametros"]), sort_keys=True, allow_nan=False)
    b = json.dumps(_correr(ficha, v, caso["parametros"]), sort_keys=True, allow_nan=False)
    assert a == b


@pytest.mark.parametrize("ficha", FICHAS_P2)
def test_no_modifica_la_entrada(ficha):
    v, p = _metodo(ficha)
    ent = _ent(v)
    antes = json.dumps(ent["valores"], sort_keys=True)
    params = copy.deepcopy(p)
    fp.FICHAS[ficha]["fn"](ent, params)
    assert json.dumps(ent["valores"], sort_keys=True) == antes and params == p


@pytest.mark.parametrize("ficha", FICHAS_P2)
def test_el_orden_de_las_filas_no_cambia_la_cifra(ficha):
    """Las listas fechadas y las de componentes se pueden aportar en cualquier orden."""
    v, p = _metodo(ficha)
    w = copy.deepcopy(v)
    for clave in ("serie", "componentes", "tokens", "flujos", "navs", "transacciones"):
        if isinstance(w.get(clave), list):
            w[clave] = w[clave][::-1]
    a, b = _correr(ficha, v, p)[0], _correr(ficha, w, p)[0]
    if ficha in ("FIR-CRED-001", "REI-LEV-001", "CHR-TOKEN-001", "ALT-AUC-001"):   # sumas en otro orden: a la tolerancia
        assert _iguales(a, b, fp.FICHAS[ficha]["tol"])
    else:
        assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def _iguales(a, b, tol):
    if isinstance(a, dict):
        return set(a) == set(b) and all(_iguales(a[k], b[k], tol) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(_iguales(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, float) and isinstance(b, float):
        return abs(a - b) <= tol * max(abs(a), abs(b), 1.0)
    return a == b


# ============================================================================= umbrales fijos y dominio de parámetros
@pytest.mark.parametrize("ficha,umbral", [(f, k) for f in FICHAS_P2 for k in fp.UMBRALES[f]])
def test_ningun_umbral_se_cambia_desde_la_peticion(ficha, umbral):
    v, p = _base(ficha)
    with pytest.raises(ErrorFicha, match="umbrales fijos"):
        _correr(ficha, v, {**p, umbral: fp.UMBRALES[ficha][umbral]})


DOMINIO_MALO = [
    ("FIR-CRED-001", "T", [0, -1, 30.5, 31, "1", True, math.nan, math.inf, 1e308, [1]]),
    ("FIR-CRED-001", "metodo", ["kmv", 1, True]), ("FIR-CRED-001", "mu", ["mercado", 0.05, True]),
    ("FX-BEER-001", "metodo", ["MCO", "FMOLS", 2]), ("FX-BEER-001", "retardos", [0, 5, 2.5, "2", True, -1, 20261110, 1e308]),
    ("CMD-REAL-001", "deflactor", ["deflactor del PIB", "IPC de EE. UU.", 1]),
    ("CMD-REAL-001", "percentil_coste", [0, -0.1, 1.01, 90, "0,9", True, math.nan]),
    ("REI-LEV-001", "caidas_valor", [[], -0.1, [0.1], [0], [-1], [-0.1, -0.1], ["-0,1"], [True], [math.nan],
                                     [-0.01 * i for i in range(1, 14)]]),
    ("REI-LEV-001", "margen", [-0.01, 1, 1.5, "0,02", True, math.inf]),
    ("CHR-ONCHAIN-001", "media_nvt", [0, -1, 366, 90.5, "90", True, 20261110, 1e308]),
    ("CHR-ONCHAIN-001", "fuente", ["", 3, True, ["a"], "otro proveedor"]),
    ("CHR-TOKEN-001", "ventanas_desbloqueo", [[], 30, [0], [30, 30], [30.5], ["30"], [True], [10951], [20261110], [1e308],
                                              list(range(1, 14))]),
    ("PRV-PME-001", "metodo", ["LN-PME", "mPME", 1]), ("PRV-PME-001", "indice", ["", 3, True, "otro índice"]),
    ("PRV-CF-001", "bow", [0.99, 5.01, 0, -2, "2,5", True, math.nan, 1e308]),
    ("PRV-CF-001", "tasas_aportacion", [[], 0.25, [-0.1], [1.1], ["0,25"], [True], [math.nan], [0.1] * 31]),
    ("PRV-CF-001", "crecimiento", [-1, 1, 2, "0,08", True, math.inf]),
    ("ALT-HF-001", "factores", ["Fama-French", 7, [], ["MKT", "MKT"], ["r"], [1], ["MKT", ""], [f"F{i}" for i in range(13)]]),
    ("ALT-HF-001", "desuavizar", ["true", 1, 0, "no"]),
    ("ALT-AUC-001", "metodo", ["case_shiller_ponderado", 1]),
    ("ALT-AUC-001", "comisiones", [0.0999, 0.2501, 0, 15, "0,15", True, math.nan]),
]


@pytest.mark.parametrize("ficha,param,malo", [(f, k, m) for f, k, ms in DOMINIO_MALO for m in ms])
def test_dominio_de_cada_parametro(ficha, param, malo):
    v, p = _metodo(ficha)
    with pytest.raises(ErrorFicha):
        _correr(ficha, v, {**p, param: malo})


def test_todos_los_parametros_tienen_prueba_de_dominio():
    con_prueba = {(f, k) for f, k, _ in DOMINIO_MALO}
    assert con_prueba == {(f, k) for f, p in fp.PARAMETROS_POR_DEFECTO.items() for k in p}


@pytest.mark.parametrize("ficha,params", [
    ("FIR-CRED-001", {"T": 30}), ("FIR-CRED-001", {"T": 0.25}), ("FIR-CRED-001", {"mu": "r"}),
    ("FX-BEER-001", {"retardos": 1}), ("FX-BEER-001", {"retardos": 4}),
    ("CMD-REAL-001", {"percentil_coste": 1}), ("CMD-REAL-001", {"percentil_coste": 0.5}),
    ("REI-LEV-001", {"caidas_valor": [-0.3], "margen": 0}), ("REI-LEV-001", {"caidas_valor": [-0.01 * i for i in range(1, 13)]}),
    ("CHR-ONCHAIN-001", {"media_nvt": 1}), ("CHR-ONCHAIN-001", {"media_nvt": 365, "fuente": "proveedor en cadena A"}),
    ("CHR-TOKEN-001", {"ventanas_desbloqueo": [1, 30 * 365]}), ("CHR-TOKEN-001", {"ventanas_desbloqueo": list(range(1, 13))}),
    ("PRV-PME-001", {"metodo": "alfa_directo", "indice": "índice de pequeña capitalización, rentabilidad total"}),
    ("PRV-CF-001", {"bow": 1, "tasas_aportacion": [0, 1], "crecimiento": -0.5}), ("PRV-CF-001", {"bow": 5}),
    ("ALT-HF-001", {"factores": ["MKT", "PTFSBD"]}), ("ALT-HF-001", {"desuavizar": False}),
    ("ALT-AUC-001", {"comisiones": 0.10}), ("ALT-AUC-001", {"comisiones": 0.25, "metodo": "hedonico"}),
])
def test_valores_admitidos_de_los_parametros(ficha, params):
    v, p = _metodo(ficha)
    res, _ = _correr(ficha, v, {**{k: x for k, x in p.items() if k not in params}, **params})
    json.dumps(res, allow_nan=False)


@pytest.mark.parametrize("ficha", FICHAS_P2)
def test_la_clase_que_anade_el_servicio_no_cambia_la_cifra(ficha):
    v, p = _base(ficha)
    assert json.dumps(_correr(ficha, v, p), sort_keys=True) == json.dumps(_correr(ficha, v, {**p, "clase": "CRI"}), sort_keys=True)


ERRATAS = {"FIR-CRED-001": {"Metodo": "ingenuo"}, "FX-BEER-001": {"retardo": 2}, "CMD-REAL-001": {"percentil coste": 0.9},
           "REI-LEV-001": {"caidas": [-0.1]}, "CHR-ONCHAIN-001": {"media_NVT": 30}, "CHR-TOKEN-001": {"ventanas": [30]},
           "PRV-PME-001": {"método": "PME+"}, "PRV-CF-001": {"Bow": 3}, "ALT-HF-001": {"desuavizado": False},
           "ALT-AUC-001": {"comision": 0.15}}


@pytest.mark.parametrize("ficha", FICHAS_P2)
def test_un_parametro_no_declarado_se_rechaza(ficha):
    v, p = _base(ficha)
    assert set(ERRATAS[ficha]).isdisjoint(fp.PARAMETROS_POR_DEFECTO[ficha])
    _rechaza(ficha, v, {**p, **ERRATAS[ficha]}, "no declarados en la ficha")
    _rechaza(ficha, v, {**p, "semilla": 1}, "no declarados en la ficha")       # las diez declaran semilla null
    _rechaza(ficha, v, {**p, "ordenar_componentes": True}, "no declarados en la ficha")   # 1.6: no se ordenan instrumentos


# Cota superior de cada parámetro de tamaño: el extremo se admite y el siguiente se rechaza
COTAS = [("FIR-CRED-001", "T", "T_maximo_anios", lambda x: x),
         ("FX-BEER-001", "retardos", "rango_retardos", lambda x: x),
         ("REI-LEV-001", "caidas_valor", "caidas_maximas", lambda x: [-0.01 * i for i in range(1, x + 1)]),
         ("CHR-ONCHAIN-001", "media_nvt", "rango_media_nvt", lambda x: x),
         ("CHR-TOKEN-001", "ventanas_desbloqueo", "ventana_dias_maxima", lambda x: [x]),
         ("CHR-TOKEN-001", "ventanas_desbloqueo", "ventanas_maximas", lambda x: list(range(1, x + 1))),
         ("PRV-CF-001", "tasas_aportacion", "vida_maxima_anios", lambda x: [0.2] * x),
         ("ALT-HF-001", "factores", "factores_maximos", lambda x: [f"F{i}" for i in range(x)])]


@pytest.mark.parametrize("ficha,param,umbral,valor", COTAS, ids=[f"{c[0]}:{c[1]}:{c[2]}" for c in COTAS])
def test_cota_superior_de_cada_parametro_de_tamano(ficha, param, umbral, valor):
    cota = fp.UMBRALES[ficha][umbral]
    cota = cota[1] if isinstance(cota, tuple) else cota
    assert fp._parametros(ficha, {param: valor(cota)})[param] == valor(cota)
    with pytest.raises(ErrorFicha, match="máximo"):
        fp._parametros(ficha, {param: valor(cota + 1)})


def _agrandar(lista, n):
    """`n` copias de filas de la lista, con otro identificador y otra fecha (días consecutivos) en cada una."""
    out = []
    for i in range(n):
        fila = copy.deepcopy(lista[i % len(lista)])
        for k in ("id", "id_pieza"):
            if k in fila:
                fila[k] = f"{fila[k]}-{i}"
        if "fecha" in fila:
            fila["fecha"] = (pd.Timestamp("1900-01-01") + pd.Timedelta(days=i)).date().isoformat()
        out.append(fila)
    return out


# Cota superior de cada lista de datos en línea: (ficha, ruta de la lista, umbral, factor del umbral)
LISTAS = [("FIR-CRED-001", ("componentes",), "componentes_maximos", 1),
          ("FX-BEER-001", ("serie",), "anios_historia_maximos", 4),
          ("CMD-REAL-001", ("serie",), "anios_historia_maximos", 12),
          ("CMD-REAL-001", ("curva_costes", "tramos"), "tramos_maximos", 1),
          ("REI-LEV-001", ("componentes",), "componentes_maximos", 1),
          ("REI-LEV-001", ("componentes", 0, "vencimientos"), "vencimientos_maximos", 1),
          ("CHR-ONCHAIN-001", ("serie",), "dias_maximos", 1),
          ("CHR-TOKEN-001", ("tokens",), "tokens_maximos", 1),
          ("CHR-TOKEN-001", ("tokens", 0, "calendario", "desbloqueos"), "desbloqueos_maximos", 1),
          ("PRV-PME-001", ("flujos",), "flujos_maximos", 1),
          ("PRV-PME-001", ("indice", "niveles"), "flujos_maximos", 1),
          ("PRV-CF-001", ("flujos",), "flujos_maximos", 1),
          ("PRV-CF-001", ("navs",), "navs_maximos", 1),
          ("ALT-HF-001", ("serie",), "anios_historia_maximos", 12),
          ("ALT-AUC-001", ("transacciones",), "transacciones_maximas", 1)]


@pytest.mark.parametrize("ficha,ruta,umbral,factor", LISTAS, ids=[f"{c[0]}:{'.'.join(map(str, c[1]))}" for c in LISTAS])
def test_cota_superior_de_cada_lista_de_datos(ficha, ruta, umbral, factor):
    """Una lista de datos más larga que su cota se rechaza antes de recorrerla (todo dato en línea tiene cota)."""
    v, p = _metodo(ficha)
    cota = fp.UMBRALES[ficha][umbral] * factor + (1 if ruta == ("indice", "niveles") else 0)
    d = v
    for k in ruta[:-1]:
        d = d[k]
    d[ruta[-1]] = _agrandar(d[ruta[-1]], cota + 1)
    _rechaza(ficha, v, p, rf"{cota + 1} (elementos|desbloqueos) \(máximo {cota}\)")


def test_los_anios_de_historia_tambien_tienen_cota():
    v, p = _metodo("ALT-AUC-001")
    v["transacciones"][0]["fecha"] = "1900-06-15"
    _rechaza("ALT-AUC-001", v, p, r"transacciones de 120 años \(máximo 100\)")
    v, p = _metodo("PRV-PME-001")
    v["flujos"][0]["fecha"] = "1900-03-31"
    v["indice"]["niveles"][0]["fecha"] = "1900-03-31"
    _rechaza("PRV-PME-001", v, p, "flujos de más de 100 años")
    v, p = _metodo("PRV-CF-001")
    v["flujos"][0]["fecha"] = "1900-03-31"
    _rechaza("PRV-CF-001", v, p, "flujos de más de 100 años")
    v["flujos"][0]["fecha"] = "2019-03-31"
    v["vida_anios"] = 31
    _rechaza("PRV-CF-001", v, p, "vida_anios")


# ============================================================================= entradas hostiles
@pytest.mark.parametrize("ficha", FICHAS_P2)
@pytest.mark.parametrize("ent", [None, [], "x", {}, {"valores": None}, {"valores": []}, {"valores": {}}])
def test_entradas_vacias_o_mal_formadas(ficha, ent):
    with pytest.raises(ErrorFicha):
        fp.FICHAS[ficha]["fn"](ent, {})


@pytest.mark.parametrize("ficha", FICHAS_P2)
@pytest.mark.parametrize("params", [[], "x", 3])
def test_parametros_que_no_son_un_dict(ficha, params):
    v, _ = _base(ficha)
    with pytest.raises(ErrorFicha):
        fp.FICHAS[ficha]["fn"](_ent(v), params)


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


HOSTILES = [math.nan, math.inf, -math.inf, "texto", True, None, [1.0], {"valor": 1.0}, 1e308, -1e308, 0, -1]


@pytest.mark.parametrize("ficha,caso", CASOS, ids=IDS)
def test_cada_hoja_hostil_rechaza_o_da_cifras_finitas(ficha, caso):
    """Cualquier dato hostil en cualquier hoja (muestra fija de hojas): o ErrorFicha o un resultado finito y serializable;
    nunca otra excepción ni un NaN/inf en el resultado."""
    v = _valores_caso(caso)
    hojas = [r for r, _ in _hojas(v)]
    paso = max(1, len(hojas) // 30)
    for ruta in hojas[::paso] + hojas[:12] + hojas[-12:]:
        for malo in HOSTILES:
            w = copy.deepcopy(v)
            _poner(w, ruta, malo)
            try:
                res, _ = _correr(ficha, w, caso["parametros"])
            except ErrorFicha:
                continue
            json.dumps(res, allow_nan=False)


@pytest.mark.parametrize("ficha", FICHAS_P2)
def test_cada_bloque_de_primer_nivel_hostil_o_ausente(ficha):
    v, p = _metodo(ficha)
    for clave in v:
        for malo in (None, [], {}, "x", 3, [None], [{}], {"x": 1}, [[1]], True):
            w = copy.deepcopy(v)
            w[clave] = malo
            try:
                res, _ = _correr(ficha, w, p)
            except ErrorFicha:
                continue
            json.dumps(res, allow_nan=False)
        w = copy.deepcopy(v)
        del w[clave]
        try:
            res, _ = _correr(ficha, w, p)
        except ErrorFicha:
            continue
        json.dumps(res, allow_nan=False)


REQUERIDOS = [
    ("FIR-CRED-001", ("r",)), ("FIR-CRED-001", ("diferencial_indice_pb",)), ("FIR-CRED-001", ("segmento", "cobertura")),
    ("FIR-CRED-001", ("componentes", 3, "capitalizacion")), ("FIR-CRED-001", ("componentes", 0, "volatilidad_acciones")),
    ("FIR-CRED-001", ("componentes", 11, "deuda_corto")), ("FIR-CRED-001", ("componentes", 5, "mu_historico")),
    ("FX-BEER-001", ("serie", 0, "reer")), ("FX-BEER-001", ("serie", 40, "piin_pib")),
    ("FX-BEER-001", ("serie", 87, "diferencial_tipos_reales")),
    ("CMD-REAL-001", ("serie", 10, "precio")), ("CMD-REAL-001", ("serie", 371, "ipc")),
    ("CMD-REAL-001", ("curva_costes", "tramos", 2, "coste")), ("CMD-REAL-001", ("curva_costes", "tramos", 0, "produccion")),
    ("REI-LEV-001", ("coste_refinanciacion", "swap")), ("REI-LEV-001", ("coste_refinanciacion", "margen")),
    ("REI-LEV-001", ("componentes", 0, "gav")), ("REI-LEV-001", ("componentes", 1, "deuda")),
    ("REI-LEV-001", ("componentes", 2, "caja")), ("REI-LEV-001", ("componentes", 0, "ebitda")),
    ("REI-LEV-001", ("componentes", 1, "gastos_financieros")), ("REI-LEV-001", ("componentes", 2, "ffo")),
    ("REI-LEV-001", ("componentes", 0, "vencimientos", 1, "importe")), ("REI-LEV-001", ("componentes", 0, "vencimientos", 2, "coste")),
    ("REI-LEV-001", ("componentes", 0, "covenants", "ltv_max")), ("REI-LEV-001", ("componentes", 1, "covenants", "icr_min")),
    ("CHR-ONCHAIN-001", ("serie", 0, "capitalizacion")), ("CHR-ONCHAIN-001", ("serie", 799, "capitalizacion_realizada")),
    ("CHR-ONCHAIN-001", ("serie", 400, "volumen_ajustado")),
    ("CHR-TOKEN-001", ("tokens", 0, "precio")), ("CHR-TOKEN-001", ("tokens", 1, "oferta_circulante")),
    ("CHR-TOKEN-001", ("tokens", 0, "oferta_total")), ("CHR-TOKEN-001", ("tokens", 1, "emision_anual")),
    ("CHR-TOKEN-001", ("tokens", 0, "quema_anual")), ("CHR-TOKEN-001", ("tokens", 0, "calendario", "desbloqueos", 1, "cantidad")),
    ("PRV-PME-001", ("flujos", 0, "aportacion")), ("PRV-PME-001", ("flujos", 4, "distribucion")),
    ("PRV-PME-001", ("nav_final", "valor")), ("PRV-PME-001", ("indice", "niveles", 3, "nivel")),
    ("PRV-CF-001", ("compromiso",)), ("PRV-CF-001", ("flujos", 2, "aportacion")), ("PRV-CF-001", ("navs", 1, "valor")),
    ("ALT-HF-001", ("serie", 0, "r")), ("ALT-HF-001", ("serie", 47, "PTFSCOM")), ("ALT-HF-001", ("serie", 20, "MKT")),
    ("ALT-AUC-001", ("transacciones", 0, "precio")), ("ALT-AUC-001", ("transacciones", 599, "precio")),
    ("ALT-AUC-001", ("transacciones", 300, "caracteristicas", "tamano")),
]


@pytest.mark.parametrize("ficha,ruta", REQUERIDOS, ids=[f"{f}:{'.'.join(map(str, r))}" for f, r in REQUERIDOS])
@pytest.mark.parametrize("malo", [math.nan, math.inf, "1,5", True, None, -1e308, [1.0]])
def test_dato_requerido_hostil_se_rechaza(ficha, ruta, malo):
    v, p = _metodo(ficha)
    if ficha == "ALT-AUC-001":
        p = {**p, "metodo": "hedonico"}                                 # las características son obligatorias en el hedónico
    _poner(v, ruta, malo)
    with pytest.raises(ErrorFicha):
        _correr(ficha, v, p)


@pytest.mark.parametrize("ficha", FICHAS_P2)
def test_fechas_ilegibles_o_numericas_se_rechazan(ficha):
    v, p = _metodo(ficha)
    rutas = [r for r, _ in _hojas(v) if r and r[-1] in ("fecha", "vintage")]
    assert rutas
    for ruta in (rutas[0], rutas[len(rutas) // 2], rutas[-1]):
        for malo in ("2024-13-45", 20240131, "", None, 1.5, True, []):
            w = copy.deepcopy(v)
            _poner(w, ruta, malo)
            with pytest.raises(ErrorFicha):
                _correr(ficha, w, p)


@pytest.mark.parametrize("ficha", FICHAS_P2)
def test_una_serie_de_ht01_no_se_ignora_en_silencio(ficha):
    v, p = _base(ficha)
    serie = pd.Series([1.0, 2.0], index=pd.to_datetime(["2024-01-01", "2024-01-02"]))
    for clave in ("series", "series_rol"):
        with pytest.raises(ErrorFicha, match="no usa series de HT-01"):
            fp.FICHAS[ficha]["fn"]({**_ent(v), clave: {"SPY": serie}}, dict(p))


def test_la_envoltura_rechaza_resultados_no_finitos_y_traduce_excepciones(monkeypatch):
    monkeypatch.setattr(fp, "_distribucion", lambda x: {"mediana": math.nan})
    v, p = _metodo("REI-LEV-001")
    _rechaza("REI-LEV-001", v, p, "resultado no finito")
    monkeypatch.setattr(fp, "_distribucion", lambda x: 1 / 0)
    _rechaza("REI-LEV-001", v, p, "ZeroDivisionError")


GIGANTES = [("FIR-CRED-001", ("componentes", 0, "capitalizacion")), ("FIR-CRED-001", ("componentes", 3, "deuda_largo")),
            ("FX-BEER-001", ("serie", 5, "reer")), ("CMD-REAL-001", ("serie", 7, "precio")),
            ("CMD-REAL-001", ("curva_costes", "tramos", 1, "produccion")), ("REI-LEV-001", ("componentes", 0, "gav")),
            ("REI-LEV-001", ("componentes", 1, "ebitda")), ("REI-LEV-001", ("componentes", 2, "ffo")),
            ("CHR-ONCHAIN-001", ("serie", 9, "volumen_ajustado")), ("CHR-TOKEN-001", ("tokens", 0, "precio")),
            ("CHR-TOKEN-001", ("tokens", 1, "oferta_total")), ("PRV-PME-001", ("flujos", 0, "aportacion")),
            ("PRV-PME-001", ("indice", "niveles", 5, "nivel")), ("PRV-CF-001", ("compromiso",)),
            ("PRV-CF-001", ("navs", 1, "valor")), ("ALT-HF-001", ("serie", 4, "MKT")),
            ("ALT-AUC-001", ("transacciones", 3, "precio"))]


@pytest.mark.parametrize("ficha,ruta", GIGANTES, ids=[f"{f}:{'.'.join(map(str, r))}" for f, r in GIGANTES])
def test_cifras_gigantes_se_rechazan_antes_de_calcular(ficha, ruta):
    """Un valor finito enorme desbordaría las sumas: una división por un total infinito daría un cero con apariencia de
    cifra. Se rechaza por magnitud; el extremo de la cota no da cifras no finitas."""
    v, p = _metodo(ficha)
    for malo in (1.0001e100, 1e200, 1e308, -1e308, 10 ** 120):
        w = copy.deepcopy(v)
        _poner(w, ruta, malo)
        _rechaza(ficha, w, p, "magnitud mayor|fuera del rango|mínimo")
    w = copy.deepcopy(v)
    _poner(w, ruta, 1e100)
    try:
        json.dumps(_correr(ficha, w, p)[0], allow_nan=False)
    except ErrorFicha:
        pass


def test_todas_las_cifras_al_borde_de_la_magnitud_no_dan_infinitos():
    for ficha in ("REI-LEV-001", "CHR-TOKEN-001", "PRV-PME-001", "PRV-CF-001"):
        v, p = _metodo(ficha)
        for ruta, x in list(_hojas(v)):
            if isinstance(x, float) and x > 1 and ruta[-1] not in ("nivel",):
                _poner(v, ruta, x * 1e98)
        try:
            json.dumps(_correr(ficha, v, p)[0], allow_nan=False)
        except ErrorFicha:
            pass


# ============================================================================= fecha de corte
def _ultima_fecha(ficha, v):
    """Última fecha observada de los datos en línea de la ficha."""
    if ficha in ("FIR-CRED-001", "REI-LEV-001", "CHR-TOKEN-001"):
        return v["fecha"]
    if ficha == "FX-BEER-001":
        return v["vintage"]
    if ficha == "PRV-PME-001":
        return v["nav_final"]["fecha"]
    if ficha == "PRV-CF-001":
        return v["navs"][-1]["fecha"]
    if ficha == "ALT-AUC-001":
        return max(t["fecha"] for t in v["transacciones"])
    return v["serie"][-1]["fecha"]


@pytest.mark.parametrize("ficha", FICHAS_P2)
def test_fecha_corte_en_la_ultima_fecha_da_la_misma_cifra(ficha):
    v, p = _metodo(ficha)
    a, _ = _correr(ficha, v, p)
    b, _ = _correr(ficha, v, p, corte=_ultima_fecha(ficha, v))
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


@pytest.mark.parametrize("ficha", FICHAS_P2)
def test_dato_posterior_a_la_fecha_de_corte_se_rechaza(ficha):
    v, p = _metodo(ficha)
    corte = (pd.Timestamp(_ultima_fecha(ficha, v)) - pd.Timedelta(days=1)).date().isoformat()
    _rechaza(ficha, v, p, "posterior a la fecha de corte", corte=corte)


@pytest.mark.parametrize("ficha,ruta,fecha", [
    ("FX-BEER-001", ("serie", 87, "fecha"), None),                        # la serie, con el vintage dentro del corte
    ("CMD-REAL-001", ("curva_costes", "fecha"), "2024-07-31"),
    ("PRV-PME-001", ("flujos", 5, "fecha"), None), ("PRV-PME-001", ("indice", "niveles", 5, "fecha"), None),
    ("PRV-CF-001", ("flujos", 5, "fecha"), None), ("PRV-CF-001", ("navs", 0, "fecha"), None),
    ("ALT-AUC-001", ("transacciones", 0, "fecha"), None),
])
def test_cada_bloque_fechado_respeta_la_fecha_de_corte(ficha, ruta, fecha):
    """Con el corte un día antes de la fecha de ese bloque, la petición se rechaza aunque los demás bloques sean anteriores."""
    v, p = _metodo(ficha)
    d = v
    for k in ruta[:-1]:
        d = d[k]
    if fecha is not None:
        d[ruta[-1]] = fecha
    corte = (pd.Timestamp(d[ruta[-1]]) - pd.Timedelta(days=1)).date().isoformat()
    _rechaza(ficha, v, p, "posterior a la fecha de corte", corte=corte)


def test_las_fechas_contractuales_futuras_no_son_fuga():
    """Vencimientos de deuda y desbloqueos de tokens posteriores al corte son el dato, no una observación."""
    v, p = _metodo("REI-LEV-001")
    assert max(x["fecha"] for c in v["componentes"] for x in c["vencimientos"]) > v["fecha"]
    _correr("REI-LEV-001", v, p, corte=v["fecha"])
    v, p = _metodo("CHR-TOKEN-001")
    assert max(x["fecha"] for t in v["tokens"] for x in t["calendario"]["desbloqueos"]) > v["fecha"]
    _correr("CHR-TOKEN-001", v, p, corte=v["fecha"])


@pytest.mark.parametrize("malo", ["2026-13-45", 20261113, [], "x"])
@pytest.mark.parametrize("ficha", FICHAS_P2)
def test_fecha_de_corte_ilegible_se_rechaza(ficha, malo):
    v, p = _metodo(ficha)
    _rechaza(ficha, v, p, "fecha_corte", corte=malo)


# ============================================================================= FIR-CRED-001
def _merton_fsolve(E, sE, D, r, T):
    """Oráculo: el sistema de Merton resuelto en dos dimensiones con `fsolve` y `scipy.stats.norm`."""
    def sistema(x):
        V, s = math.exp(x[0]), math.exp(x[1])
        d1 = (math.log(V / D) + (r + s * s / 2) * T) / (s * math.sqrt(T))
        d2 = d1 - s * math.sqrt(T)
        return [V * stats.norm.cdf(d1) - D * math.exp(-r * T) * stats.norm.cdf(d2) - E, stats.norm.cdf(d1) * s * V / E - sE]
    x = optimize.fsolve(sistema, [math.log(E + D), math.log(sE * E / (E + D))], xtol=1e-14)
    return math.exp(x[0]), math.exp(x[1])


def _datos_cred_reales():
    comps = [{"id": f"E{i}", "capitalizacion": 80.0 + 37.0 * i, "volatilidad_acciones": 0.22 + 0.035 * i,
              "deuda_corto": 12.0 + 3.0 * i, "deuda_largo": 60.0 + 11.0 * (i % 4), "mu_historico": 0.02 + 0.01 * (i % 5)}
             for i in range(14)]
    return {"fecha": "2026-03-31", "segmento": {"nombre": "HY industriales", "financiero": False, "cobertura": 0.65},
            "r": 0.035, "diferencial_indice_pb": 310.0, "componentes": comps}


@pytest.mark.parametrize("T", [1, 0.5, 3])
def test_fir_cred_oraculo_independiente(T):
    v = _datos_cred_reales()
    res, lim = _correr("FIR-CRED-001", v, {"T": T})
    r = v["r"]
    dd, pd_, ddr, dif, w = [], [], [], [], []
    for c in v["componentes"]:
        D = c["deuda_corto"] + 0.5 * c["deuda_largo"]
        V, s = _merton_fsolve(c["capitalizacion"], c["volatilidad_acciones"], D, r, T)
        d1 = (math.log(V / D) + (r + s * s / 2) * T) / (s * math.sqrt(T))
        d2 = d1 - s * math.sqrt(T)
        dd.append(d2)
        pd_.append(stats.norm.cdf(-d2) * 100)
        ddr.append((math.log(V / D) + (c["mu_historico"] - s * s / 2) * T) / (s * math.sqrt(T)))
        valor_deuda = V - c["capitalizacion"]                           # la deuda vale activos − acciones
        dif.append(-math.log(valor_deuda / D) / T - r)                   # rendimiento de la deuda − r
        w.append(c["deuda_corto"] + c["deuda_largo"])
    w = np.array(w) / sum(w)
    nr = res["neutral_al_riesgo"]
    assert nr["dd"]["mediana"] == pytest.approx(np.median(dd), rel=1e-7)
    assert nr["dd"]["q25"] == pytest.approx(np.percentile(dd, 25), rel=1e-7)
    assert nr["pd_pct"]["q75"] == pytest.approx(np.percentile(pd_, 75), rel=1e-6)
    assert nr["pd_pct"]["media_ponderada_deuda"] == pytest.approx(float(w @ np.array(pd_)), rel=1e-6)
    assert nr["proporcion_dd_menor_2_pct"] == pytest.approx(np.mean(np.array(dd) < 2) * 100)
    assert res["real"]["dd"]["mediana"] == pytest.approx(np.median(ddr), rel=1e-7)
    assert res["real"]["pd_pct"]["maximo"] == pytest.approx(stats.norm.cdf(-min(ddr)) * 100, rel=1e-6)
    assert res["diferencial_implicito_pb"] == pytest.approx(float(w @ np.array(dif)) * 1e4, rel=1e-6)
    assert res["brecha_observado_implicito_pb"] == pytest.approx(310.0 - float(w @ np.array(dif)) * 1e4, rel=1e-6)
    assert res["verificacion"]["error_relativo_sistema_max"] < 1e-9
    assert lim == ["sin PD histórica por rating: referencia ingenua no comparada"]
    assert res["referencia_ingenua"]["pd_historica_pct"] is None and res["T_anios"] == T


def test_fir_cred_el_punto_de_impago_pondera_la_deuda_a_largo_a_la_mitad():
    v = _datos_cred_reales()
    a = _correr("FIR-CRED-001", v)[0]
    for c in v["componentes"]:                                           # misma deuda total, toda a corto: más cerca del impago
        c["deuda_corto"], c["deuda_largo"] = c["deuda_corto"] + c["deuda_largo"], 0.0
    b = _correr("FIR-CRED-001", v)[0]
    assert b["neutral_al_riesgo"]["dd"]["mediana"] < a["neutral_al_riesgo"]["dd"]["mediana"]
    for c in v["componentes"]:                 # y con 2·X a largo en vez de X a corto, el mismo punto de impago (los
        c["deuda_corto"], c["deuda_largo"] = 0.0, 2 * c["deuda_corto"]       # pesos por deuda total siguen proporcionales)
    c2 = _correr("FIR-CRED-001", v)[0]
    assert all(c2["neutral_al_riesgo"]["dd"][k] == pytest.approx(b["neutral_al_riesgo"]["dd"][k], rel=1e-9)
               for k in ("mediana", "q25", "q75", "minimo", "maximo", "media_ponderada_deuda"))


def test_fir_cred_mu_r_y_metodo_ingenuo_con_r():
    v = _datos_cred_reales()
    for c in v["componentes"]:
        del c["mu_historico"]
    _rechaza("FIR-CRED-001", v, {}, "mu_historico")
    res, _ = _correr("FIR-CRED-001", v, {"mu": "r"})
    assert res["real"] is None and res["mu"] == "r"
    ing, _ = _correr("FIR-CRED-001", v, {"mu": "r", "metodo": "ingenuo"})
    c = v["componentes"][0]
    E, sE, D = c["capitalizacion"], c["volatilidad_acciones"], c["deuda_corto"] + 0.5 * c["deuda_largo"]
    s = E / (E + D) * sE + D / (E + D) * (0.05 + 0.25 * sE)
    dd0 = (math.log((E + D) / D) + (0.035 - s * s / 2)) / s
    todos = []
    for c in v["componentes"]:
        E, sE, D = c["capitalizacion"], c["volatilidad_acciones"], c["deuda_corto"] + 0.5 * c["deuda_largo"]
        s = E / (E + D) * sE + D / (E + D) * (0.05 + 0.25 * sE)
        todos.append((math.log((E + D) / D) + (0.035 - s * s / 2)) / s)
    assert dd0 in todos and ing["neutral_al_riesgo"]["dd"]["maximo"] == pytest.approx(max(todos), rel=1e-12)
    assert ing["verificacion"]["error_relativo_sistema_max"] == 0.0


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v["segmento"].update(financiero=True), "bancos y aseguradoras"),
    (lambda v: v["segmento"].pop("financiero"), "aclaración: declare si el segmento"),
    (lambda v: v["segmento"].update(financiero="no"), "aclaración: declare si el segmento"),
    (lambda v: v["segmento"].update(cobertura=0.49), "dominado por emisores sin acciones cotizadas"),
    (lambda v: v["segmento"].update(cobertura=1.01), "cobertura"),
    (lambda v: v["segmento"].pop("cobertura"), "cobertura"),
    (lambda v: v.update(componentes=v["componentes"][:9]), r"9 componentes cotizados \(< 10\)"),
    (lambda v: v.update(componentes=[]), r"0 componentes cotizados \(< 10\)"),
    (lambda v: v["componentes"][1].update(id="E0"), "identificadores de componente repetidos"),
    (lambda v: v["componentes"][2].update(deuda_corto=0.0, deuda_largo=0.0), "sin deuda"),
    (lambda v: v["componentes"][2].update(volatilidad_acciones=0.0), "volatilidad_acciones"),
    (lambda v: v["componentes"][2].update(volatilidad_acciones=10.5), "volatilidad_acciones"),
    (lambda v: v["componentes"][2].update(capitalizacion=0.0), "capitalizacion"),
    (lambda v: v["componentes"][2].update(deuda_largo=-1.0), "deuda_largo"),
    (lambda v: v["componentes"][2].update(mu_historico=1.0), "mu_historico"),
    (lambda v: v.update(r=1.0), "FIR-CRED-001: r"), (lambda v: v.update(r=-1.0), "FIR-CRED-001: r"),
    (lambda v: v.update(diferencial_indice_pb=-5.0), "diferencial_indice_pb"),
    (lambda v: v.update(pd_historica_rating_pct=101.0), "pd_historica_rating_pct"),
    (lambda v: v.pop("fecha"), "fecha"), (lambda v: v.pop("segmento"), "segmento"),
])
def test_fir_cred_rechazos(cambio, motivo):
    v = _datos_cred_reales()
    cambio(v)
    _rechaza("FIR-CRED-001", v, {}, motivo)


def test_fir_cred_limites_del_dominio_que_se_admiten():
    v = _datos_cred_reales()
    v["segmento"]["cobertura"] = 0.5
    v["componentes"] = v["componentes"][:10]
    v["componentes"][0]["volatilidad_acciones"] = 10.0
    res, _ = _correr("FIR-CRED-001", v)
    assert res["n_componentes"] == 10 and res["cobertura_segmento_pct"] == 50.0


def test_fir_cred_no_entrega_filas_por_componente():
    """1.6: con la salida no se puede ordenar emisores."""
    v = _datos_cred_reales()
    texto = json.dumps(_correr("FIR-CRED-001", v)[0])
    assert not any(c["id"] in texto.replace("ESTADISTICA", "") for c in v["componentes"])


def test_fir_cred_un_sistema_que_no_converge_se_rechaza(monkeypatch):
    monkeypatch.setitem(fp.UMBRALES["FIR-CRED-001"], "iteraciones_maximas", 2)
    _rechaza("FIR-CRED-001", _datos_cred_reales(), {}, "FIR-CRED-001")


# ============================================================================= FX-BEER-001
def _beer_tabla(v):
    t = pd.DataFrame(v["serie"]).set_index("fecha")
    return np.log(t["reer"].to_numpy()), t[list(fp.UMBRALES["FX-BEER-001"]["fundamentales"])].to_numpy()


def _beer_ruidoso():
    """Tipo real con una desviación que no es ortogonal a los fundamentales: caso general, no el exacto del control."""
    v, _ = _metodo("FX-BEER-001")
    for i, fila in enumerate(v["serie"]):
        fila["reer"] *= math.exp(0.03 * math.sin(0.9 * i) + 0.02 * math.cos(2.3 * i))
    return v


@pytest.mark.parametrize("k", [1, 2, 3])
def test_fx_beer_oraculo_dols_e_ic(k):
    v = _beer_ruidoso()
    res, _ = _correr("FX-BEER-001", v, {"retardos": k})
    q, X = _beer_tabla(v)
    T = len(q)
    filas, y = [], []
    for t in range(k + 1, T - k):                                        # diseño DOLS fila a fila
        fila = [1.0, *X[t]]
        for j in range(-k, k + 1):
            fila += list(X[t + j] - X[t + j - 1])
        filas.append(fila)
        y.append(q[t])
    Z, y = np.array(filas), np.array(y)
    b = np.linalg.solve(Z.T @ Z, Z.T @ y)
    e = y - Z @ b
    n = len(y)
    L = math.floor(4 * (n / 100) ** (2 / 9))
    S = np.zeros((Z.shape[1], Z.shape[1]))
    for i in range(n):                                                   # HAC de Newey-West con bucles
        for j in range(n):
            if abs(i - j) <= L:
                S += (1 - abs(i - j) / (L + 1)) * e[i] * e[j] * np.outer(Z[i], Z[j])
    V = np.linalg.inv(Z.T @ Z) @ S @ np.linalg.inv(Z.T @ Z)
    beta = b[1:5]
    z = q - X @ beta
    z = z - z.mean()
    d = X[-1] - X.mean(axis=0)
    ee = math.sqrt(d @ V[1:5, 1:5] @ d)
    zc = stats.norm.ppf(0.95)                                            # nivel_ic 0,90 de la configuración
    nombres = fp.UMBRALES["FX-BEER-001"]["fundamentales"]
    for j, nb in enumerate(nombres):
        assert res["coeficientes"][nb]["beta"] == pytest.approx(beta[j], rel=1e-7)
        assert res["coeficientes"][nb]["ee"] == pytest.approx(math.sqrt(V[1 + j, 1 + j]), rel=1e-6)
        assert res["coeficientes"][nb]["t"] == pytest.approx(beta[j] / math.sqrt(V[1 + j, 1 + j]), rel=1e-6)
    assert res["desalineamiento_pct"] == pytest.approx((math.exp(z[-1]) - 1) * 100, rel=1e-7)
    assert res["ic_desalineamiento_pct"] == pytest.approx([(math.exp(z[-1] - zc * ee) - 1) * 100,
                                                           (math.exp(z[-1] + zc * ee) - 1) * 100], rel=1e-6)
    assert res["nivel_ic"] == 0.90 and res["n_estimacion"] == n and res["retardos"] == k
    assert res["equilibrio"] == pytest.approx(math.exp(q[-1] - z[-1]), rel=1e-9)
    assert res["constante"] == pytest.approx(float(np.mean(q - X @ beta)), rel=1e-9)
    assert abs(res["verificacion"]["media_desalineamiento"]) < 1e-12
    assert abs(res["verificacion"]["media_residuo_regresion"]) < 1e-12


def test_fx_beer_oraculo_adf_de_los_residuos():
    """Contraste de cointegración: ADF sin constante de los residuos, con el rezago elegido por AIC, recalculado aquí."""
    v = _beer_ruidoso()
    res, _ = _correr("FX-BEER-001", v)
    q, X = _beer_tabla(v)
    beta = np.array([res["coeficientes"][nb]["beta"] for nb in fp.UMBRALES["FX-BEER-001"]["fundamentales"]])
    z = q - X @ beta
    z = z - z.mean()
    dz = np.diff(z)
    pmax = math.floor(4 * (len(z) / 100) ** (2 / 9))

    def ajuste(p_, desde):
        filas = range(desde, len(dz))
        A = np.array([[z[t]] + [dz[t - i] for i in range(1, p_ + 1)] for t in filas])
        yy = np.array([dz[t] for t in filas])
        b = np.linalg.lstsq(A, yy, rcond=None)[0]
        e = yy - A @ b
        s2 = e @ e / (len(yy) - A.shape[1])
        return b[0] / math.sqrt(s2 * np.linalg.inv(A.T @ A)[0, 0]), len(yy) * math.log(e @ e / len(yy)) + 2 * A.shape[1]

    mejor = min(range(pmax + 1), key=lambda p_: (ajuste(p_, pmax)[1], p_))
    tau = ajuste(mejor, mejor)[0]
    c = res["cointegracion"]
    assert c["estadistico"] == pytest.approx(tau, rel=1e-7) and c["nivel"] == 0.05
    assert c["critico"] == -4.41519                                      # MacKinnon (2010), N = 5, 5 %
    assert c["evidencia"] == (tau < -4.41519)


def test_fx_beer_el_nivel_del_ic_sale_de_la_configuracion():
    v = _beer_ruidoso()
    a, _ = _correr("FX-BEER-001", v)
    b, _ = _correr("FX-BEER-001", v, cfg={"evaluacion": {"nivel_ic": 0.99}})
    assert b["nivel_ic"] == 0.99 and a["nivel_ic"] == 0.90
    ancho_a = a["ic_desalineamiento_pct"][1] - a["ic_desalineamiento_pct"][0]
    ancho_b = b["ic_desalineamiento_pct"][1] - b["ic_desalineamiento_pct"][0]
    assert ancho_b > ancho_a * 1.5
    with pytest.raises(ErrorFicha):
        _correr("FX-BEER-001", v, cfg={"evaluacion": {"nivel_ic": 1.5}})


def test_fx_beer_johansen_frente_a_dols_y_sin_ic():
    v = _beer_ruidoso()
    j, lim = _correr("FX-BEER-001", v, {"metodo": "Johansen"})
    assert j["ic_desalineamiento_pct"] is None and j["nivel_ic"] is None and any("Johansen" in x for x in lim)
    assert all(c["ee"] is None and c["t"] is None for c in j["coeficientes"].values())
    assert j["cointegracion"]["contraste"].startswith("traza") and j["cointegracion"]["critico"] == 76.9725
    assert j["verificacion"]["media_residuo_regresion"] is None and abs(j["verificacion"]["media_desalineamiento"]) < 1e-12
    q, X = _beer_tabla(v)
    beta = np.array([j["coeficientes"][nb]["beta"] for nb in fp.UMBRALES["FX-BEER-001"]["fundamentales"]])
    z = q - X @ beta
    assert j["desalineamiento_pct"] == pytest.approx((math.exp(z[-1] - z.mean()) - 1) * 100, rel=1e-9)


def test_fx_beer_sin_cointegracion_se_declara_y_sin_reversion_no_hay_vida_media():
    v, _ = _metodo("FX-BEER-001")
    for i, fila in enumerate(v["serie"]):                                 # un paseo determinista, ajeno a los fundamentales
        fila["reer"] = 100.0 * math.exp(0.004 * i * i / 10)
    res, lim = _correr("FX-BEER-001", v)
    assert res["cointegracion"]["evidencia"] is False and any("sin evidencia de cointegración" in x for x in lim)
    assert res["vida_media_anios"] is None or res["vida_media_anios"] > 0


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v.update(serie=v["serie"][:59]), r"59 trimestres \(< 15 años\)"),
    (lambda v: v.pop("vintage"), "vintage"),
    (lambda v: v.update(vintage="2024-12-30"), "anterior a la última observación"),
    (lambda v: v["serie"].pop(40), "no trimestrales consecutivas"),
    (lambda v: v["serie"][40].update(fecha=v["serie"][41]["fecha"]), "fechas repetidas"),
    (lambda v: v["serie"][3].update(reer=0.0), "reer"),
    (lambda v: v["serie"][3].pop("terminos_intercambio"), "terminos_intercambio"),
    (lambda v: [f.update(piin_pib=0.3) for f in v["serie"]], "no identificada"),
    (lambda v: [f.update(reer=math.exp(4.0 + f["piin_pib"])) for f in v["serie"]], "ajuste exacto"),
])
def test_fx_beer_rechazos(cambio, motivo):
    v, _ = _metodo("FX-BEER-001")
    cambio(v)
    _rechaza("FX-BEER-001", v, {}, motivo)


def test_fx_beer_entre_15_y_20_anios_es_limitacion():
    v, _ = _metodo("FX-BEER-001")
    v["serie"] = v["serie"][-60:]
    res, lim = _correr("FX-BEER-001", v)
    assert res["n"] == 60 and res["anios"] == 15 and any("< 20 años" in x for x in lim)
    v["serie"] = _metodo("FX-BEER-001")[0]["serie"][-80:]
    assert not any("< 20 años" in x for x in _correr("FX-BEER-001", v)[1])


# ============================================================================= CMD-REAL-001
def test_cmd_real_oraculo_independiente():
    v, _ = _metodo("CMD-REAL-001")
    res, lim = _correr("CMD-REAL-001", v, {"percentil_coste": 0.75})
    t = pd.DataFrame(v["serie"])
    real = t["precio"] * t["ipc"].iloc[-1] / t["ipc"]
    assert res["precio_real_actual"] == pytest.approx(real.iloc[-1], rel=1e-12)
    assert res["percentil"] == pytest.approx(stats.percentileofscore(real, real.iloc[-1], kind="weak") / 100, rel=1e-12)
    assert res["z"] == pytest.approx((real.iloc[-1] - real.mean()) / real.std(ddof=1), rel=1e-10)
    pend, _, lo, hi = stats.theilslopes(np.log(real.to_numpy()), np.arange(len(real)), 0.95)
    assert res["tendencia_real_pct_anual"] == pytest.approx((math.exp(12 * pend) - 1) * 100, rel=1e-9)
    assert res["ic_tendencia_pct_anual"][0] <= res["tendencia_real_pct_anual"] <= res["ic_tendencia_pct_anual"][1]
    assert res["ic_tendencia_pct_anual"] == pytest.approx([(math.exp(12 * lo) - 1) * 100, (math.exp(12 * hi) - 1) * 100], abs=0.5)
    # Curva de costes: cuantil ponderado por producción, expandiendo cada tramo en unidades de producción
    costes = np.repeat([c["coste"] for c in v["curva_costes"]["tramos"]], [int(c["produccion"]) for c in v["curva_costes"]["tramos"]])
    coste = float(np.sort(costes)[math.ceil(0.75 * len(costes)) - 1])
    assert res["coste_marginal"]["coste_nominal"] == coste == 55.0
    ipc_curva = t.loc[t["fecha"] == "2023-06-30", "ipc"].iloc[0]
    assert res["coste_marginal"]["coste_real"] == pytest.approx(coste * t["ipc"].iloc[-1] / ipc_curva, rel=1e-12)
    assert res["precio_sobre_coste"] == pytest.approx(real.iloc[-1] / (coste * t["ipc"].iloc[-1] / ipc_curva), rel=1e-12)
    assert res["referencia_ingenua"]["ri_mh"] == pytest.approx(real.mean(), rel=1e-12)
    assert res["referencia_ingenua"]["ri_pa"] == res["precio_real_actual"] and lim == []


@pytest.mark.parametrize("percentil,esperado", [(0.25, 30.0), (0.2500001, 41.0), (0.55, 41.0), (0.75, 55.0), (0.87, 70.0),
                                                (0.90, 92.0), (0.93, 92.0), (0.94, 120.0), (1, 120.0), (0.01, 30.0)])
def test_cmd_real_percentil_de_la_curva_de_costes_en_los_bordes(percentil, esperado):
    v, _ = _metodo("CMD-REAL-001")
    assert _correr("CMD-REAL-001", v, {"percentil_coste": percentil})[0]["coste_marginal"]["coste_nominal"] == esperado


def test_cmd_real_tendencia_decreciente_y_sin_tendencia():
    v, _ = _base("CMD-REAL-001", 2)
    for i, fila in enumerate(v["serie"]):                                # precio real log-lineal decreciente
        fila["precio"] = 40.0 * math.exp(-0.002 * i) * fila["ipc"] / v["serie"][-1]["ipc"]
    res, _ = _correr("CMD-REAL-001", v)
    assert res["tendencia_real_pct_anual"] == pytest.approx((math.exp(-0.024) - 1) * 100, rel=1e-9)
    assert res["tendencia_direccion"] == "decreciente" and res["percentil"] == pytest.approx(1 / 372)


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v.update(serie=v["serie"][:179]), r"179 meses \(< 15 años\)"),
    (lambda v: v.update(ipc_moneda="EUR"), "IPC de la moneda de cotización"),
    (lambda v: v.pop("moneda"), "moneda"),
    (lambda v: v["serie"].pop(100), "no mensuales consecutivas"),
    (lambda v: v["serie"][5].update(ipc=0.0), "ipc"), (lambda v: v["serie"][5].update(precio=-3.0), "precio"),
    (lambda v: v.pop("curva_costes"), "curva_costes"),
    (lambda v: v["curva_costes"].pop("fuente"), "fuente"), (lambda v: v["curva_costes"].pop("fecha"), "fecha"),
    (lambda v: v["curva_costes"].update(fecha="1990-05-31"), "no cae en un mes de la serie"),
    (lambda v: v["curva_costes"].update(tramos=[]), "tramos"),
    (lambda v: v["curva_costes"]["tramos"][0].update(produccion=0.0), "produccion"),
    (lambda v: v["curva_costes"]["tramos"].append("x"), "tramos"),
])
def test_cmd_real_rechazos(cambio, motivo):
    v, _ = _metodo("CMD-REAL-001")
    cambio(v)
    _rechaza("CMD-REAL-001", v, {}, motivo)


def test_cmd_real_entre_15_y_30_anios_es_limitacion_y_precio_constante():
    v, _ = _metodo("CMD-REAL-001")
    v["serie"] = v["serie"][-180:]
    res, lim = _correr("CMD-REAL-001", v)
    assert res["n"] == 180 and res["anios"] == 15 and any("< 30 años" in x for x in lim)
    for fila in v["serie"]:
        fila["precio"], fila["ipc"] = 10.0, 100.0
    res, lim = _correr("CMD-REAL-001", v)
    assert res["z"] is None and res["percentil"] == 1.0 and any("sin dispersión" in x for x in lim)
    assert res["tendencia_real_pct_anual"] == 0.0 and res["tendencia_direccion"] == "sin tendencia"


# ============================================================================= REI-LEV-001
def _lev_oraculo(v, coste_nuevo, caidas):
    c = pd.DataFrame([{k: x for k, x in comp.items() if k not in ("vencimientos", "covenants")} for comp in v["componentes"]])
    venc = pd.concat([pd.DataFrame(comp["vencimientos"]).assign(id=comp["id"]) for comp in v["componentes"]])
    venc["fecha"] = pd.to_datetime(venc["fecha"])
    limite = pd.Timestamp(v["fecha"]) + pd.DateOffset(months=24)
    prox = venc[venc["fecha"] <= limite]
    neta = (c["deuda"] - c["caja"]).sum()
    return {"ltv_pct": neta / c["gav"].sum() * 100, "icr_veces": c["ebitda"].sum() / c["gastos_financieros"].sum(),
            "deuda_neta_sobre_ebitda_veces": neta / c["ebitda"].sum(),
            "vencimientos_24m_pct": prox["importe"].sum() / c["deuda"].sum() * 100,
            "impacto_ffo_pct": -(prox["importe"] * (coste_nuevo - prox["coste"])).sum() / c["ffo"].sum() * 100,
            "ltv_estresado_pct": {f"{x:g}": neta / (c["gav"].sum() * (1 + x)) * 100 for x in caidas}}


def test_rei_lev_oraculo_independiente_con_pandas():
    v, _ = _metodo("REI-LEV-001")
    extra = [{"id": f"X{i}", "gav": 300.0 + 90 * i, "deuda": 150.0 + 20 * i, "caja": 5.0 * i, "ebitda": 14.0 + 3 * i,
              "gastos_financieros": 3.0 + i, "ffo": 6.0 + 2 * i - (9 if i == 2 else 0),
              "vencimientos": [{"fecha": f"{2026 + j}-0{1 + i}-15", "importe": (150.0 + 20 * i) / 5, "coste": 0.01 + 0.006 * j}
                               for j in range(1, 6)]} for i in range(6)]
    v["componentes"] += extra
    res, lim = _correr("REI-LEV-001", v, {"caidas_valor": [-0.05, -0.35], "margen": 0.021})
    esp = _lev_oraculo(v, 0.027 + 0.021, [-0.05, -0.35])
    for k, x in esp.items():
        assert res[k] == pytest.approx(x, rel=1e-12)
    assert res["coste_refinanciacion"] == {"swap": 0.027, "margen": 0.021, "coste": pytest.approx(0.048)}
    ltv = [(c["deuda"] - c["caja"]) / c["gav"] * 100 for c in v["componentes"]]
    assert res["dispersion"]["ltv_pct"]["mediana"] == pytest.approx(np.median(ltv))
    assert res["dispersion"]["ltv_pct"]["q75"] == pytest.approx(np.percentile(ltv, 75))
    assert res["dispersion"]["ltv_pct"]["maximo"] == pytest.approx(max(ltv))
    assert res["n_componentes"] == 9 and res["covenants"]["n_componentes"] == 2
    assert lim == ["covenants de 2 de 9 componentes: holgura sobre los declarados"]


def test_rei_lev_el_borde_de_los_24_meses_y_el_margen_de_los_datos():
    v, _ = _metodo("REI-LEV-001")
    a = _correr("REI-LEV-001", v)[0]
    v["componentes"][1]["vencimientos"][1]["fecha"] = "2028-06-30"         # justo a 24 meses: entra
    b = _correr("REI-LEV-001", v)[0]
    assert b["vencimientos_24m_pct"] == pytest.approx((310.0 + 240.0) / 850.0 * 100)
    assert a["vencimientos_24m_pct"] == pytest.approx(310.0 / 850.0 * 100)
    extra = 120 * (0.045 - 0.015) + 100 * (0.045 - 0.02) + 90 * (0.045 - 0.03) + 240 * (0.045 - 0.025)
    assert b["impacto_ffo_pct"] == pytest.approx(-extra / 56.0 * 100)
    del v["coste_refinanciacion"]["margen"]
    _rechaza("REI-LEV-001", v, {}, "margen")
    assert _correr("REI-LEV-001", v, {"margen": 0.018})[0]["impacto_ffo_pct"] == pytest.approx(b["impacto_ffo_pct"])


def test_rei_lev_covenants_incumplidos_y_sin_covenants():
    v, _ = _metodo("REI-LEV-001")
    v["componentes"][1]["covenants"] = {"ltv_max": 0.45, "icr_min": 3.0}  # S2: LTV 50 % e ICR 2,7
    c = _correr("REI-LEV-001", v)[0]["covenants"]
    assert c["en_incumplimiento_pct"] == 50.0 and c["holgura_ltv_pp"]["minimo"] == pytest.approx(-5.0)
    assert c["holgura_icr_veces"]["minimo"] == pytest.approx(-0.3)
    assert c["caida_valor_que_agota_ltv_pct"]["maximo"] == pytest.approx((0.5 / 0.45 - 1) * 100)
    for comp in v["componentes"]:
        comp.pop("covenants", None)
    res, lim = _correr("REI-LEV-001", v)
    assert res["covenants"] is None and "sin covenants declarados: holgura no calculada" in lim


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v["componentes"][0].pop("vencimientos"), "sin perfil de vencimientos"),
    (lambda v: v["componentes"][0].update(vencimientos=[]), "sin perfil de vencimientos"),
    (lambda v: v["componentes"][0].update(deuda=421.0), "no es la deuda"),
    (lambda v: v["componentes"][0]["vencimientos"].pop(), "no es la deuda"),
    (lambda v: v["componentes"][0]["vencimientos"][0].update(fecha="2026-06-29"), "anterior a la fecha de los datos"),
    (lambda v: v["componentes"][0]["vencimientos"][0].update(coste=1.0), "coste fuera del rango"),
    (lambda v: v["componentes"][0]["vencimientos"][0].update(coste=-1.0), "coste"),
    (lambda v: v["componentes"][0]["vencimientos"][1].update(fecha="2027-03-31"), "fechas repetidas"),
    (lambda v: v["componentes"][1].update(id="S1"), "identificadores de componente repetidos"),
    (lambda v: [c.update(ffo=-1.0) for c in v["componentes"]], "FFO agregado no positivo"),
    (lambda v: v["componentes"][0]["covenants"].update(ltv_max=1.2), "ltv_max"),
    (lambda v: v["componentes"][0]["covenants"].update(icr_min=0), "icr_min"),
    (lambda v: v["coste_refinanciacion"].update(swap=1.0), "swap"),
    (lambda v: v["coste_refinanciacion"].update(margen=-0.001), "margen"),
    (lambda v: v.pop("coste_refinanciacion"), "coste_refinanciacion"),
    (lambda v: v.update(componentes=[]), "componentes"), (lambda v: v.pop("moneda"), "moneda"),
])
def test_rei_lev_rechazos(cambio, motivo):
    v, _ = _metodo("REI-LEV-001")
    cambio(v)
    _rechaza("REI-LEV-001", v, {}, motivo)


def test_rei_lev_un_vencimiento_en_la_fecha_de_los_datos_se_admite_y_no_hay_filas_por_componente():
    v, _ = _metodo("REI-LEV-001")
    v["componentes"][0]["vencimientos"][0]["fecha"] = v["fecha"]
    res, _ = _correr("REI-LEV-001", v)
    assert not any(f'"{c["id"]}"' in json.dumps(res) for c in v["componentes"])


# ============================================================================= CHR-ONCHAIN-001
@pytest.mark.parametrize("w", [1, 90, 365])
def test_chr_onchain_oraculo_con_pandas(w):
    v, _ = _metodo("CHR-ONCHAIN-001")
    res, _ = _correr("CHR-ONCHAIN-001", v, {"media_nvt": w})
    t = pd.DataFrame(v["serie"])
    cm, cr, vol = t["capitalizacion"], t["capitalizacion_realizada"], t["volumen_ajustado"]
    mvrv, z, nvt = cm / cr, (cm - cr) / cm.std(), cm / vol
    senal = (cm / vol.rolling(w).mean()).dropna()
    assert len(senal) == 800 - w + 1
    for k, s in (("mvrv", mvrv), ("mvrv_z", z), ("nvt", nvt), ("senal_nvt", senal)):
        assert res[k] == pytest.approx(s.iloc[-1], rel=1e-11)
        assert res["percentiles"][k] == pytest.approx(stats.percentileofscore(s, s.iloc[-1], kind="weak") / 100, rel=1e-12)
    if w == 1:
        assert res["senal_nvt"] == pytest.approx(res["nvt"], rel=1e-12)


def test_chr_onchain_pocos_ciclos_solo_por_debajo_de_cuatro_anios():
    v, _ = _metodo("CHR-ONCHAIN-001")
    fila = v["serie"][-1]
    largo = [{**fila, "fecha": (pd.Timestamp("2020-01-01") + pd.Timedelta(days=i)).date().isoformat(),
              "capitalizacion": fila["capitalizacion"] * (1 + 0.1 * math.sin(i))} for i in range(1460)]
    assert _correr("CHR-ONCHAIN-001", {**v, "serie": largo})[1] == []
    lim = _correr("CHR-ONCHAIN-001", {**v, "serie": largo[:1459]})[1]
    assert len(lim) == 1 and lim[0].startswith("pocos ciclos")
    assert _correr("CHR-ONCHAIN-001", {**v, "serie": largo[:730]})[0]["n_dias"] == 730


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v.pop("fuente"), "sin fuente en cadena verificable"),
    (lambda v: v["fuente"].pop("metodologia"), "sin fuente en cadena verificable"),
    (lambda v: v["fuente"].update(filtros=" "), "sin fuente en cadena verificable"),
    (lambda v: v["fuente"].update(nombre=3), "sin fuente en cadena verificable"),
    (lambda v: v.update(fuente="proveedor"), "sin fuente en cadena verificable"),
    (lambda v: v.update(serie=v["serie"][:729]), r"729 días \(< 730"),
    (lambda v: v["serie"].pop(300), "no diarias consecutivas"),
    (lambda v: v["serie"][10].update(volumen_ajustado=0.0), "volumen_ajustado"),
    (lambda v: v["serie"][10].update(capitalizacion_realizada=-1.0), "capitalizacion_realizada"),
    (lambda v: [f.update(capitalizacion=5.0) for f in v["serie"]], "sin dispersión"),
])
def test_chr_onchain_rechazos(cambio, motivo):
    v, _ = _metodo("CHR-ONCHAIN-001")
    cambio(v)
    _rechaza("CHR-ONCHAIN-001", v, {}, motivo)


def test_chr_onchain_la_fuente_de_la_peticion_debe_ser_la_de_los_datos():
    v, _ = _metodo("CHR-ONCHAIN-001")
    assert _correr("CHR-ONCHAIN-001", v, {"fuente": "proveedor en cadena A"})[0]["fuente"] == "proveedor en cadena A"
    _rechaza("CHR-ONCHAIN-001", v, {"fuente": "proveedor en cadena B"}, "la petición pide")


# ============================================================================= CHR-TOKEN-001
def test_chr_token_oraculo_con_fracciones_exactas():
    v, _ = _metodo("CHR-TOKEN-001")
    v["tokens"].append({"id": "TKC", "precio": 12.5, "oferta_circulante": 2.0e7, "oferta_total": 2.1e7, "oferta_maxima": 2.1e7,
                        "emision_anual": 0.0, "quema_anual": 5.0e5, "staking_nominal": 0.03, "concentracion_10_mayores": 0.62,
                        "calendario": {"fuente": "contrato", "desbloqueos": [{"fecha": "2026-08-01", "cantidad": 1.0e6}]}})
    res, _ = _correr("CHR-TOKEN-001", v, {"ventanas_desbloqueo": [20, 33, 200]})
    F_ = Fraction
    fecha = pd.Timestamp(v["fecha"])
    cm = [F_(t["precio"]) * F_(t["oferta_circulante"]) for t in v["tokens"]]
    fdv = [F_(t["precio"]) * F_(t["oferta_maxima"] if t["oferta_maxima"] is not None else t["oferta_total"]) for t in v["tokens"]]
    assert res["fdv_sobre_capitalizacion_veces"] == pytest.approx(float(sum(fdv) / sum(cm)), rel=1e-13)
    neta = sum(F_(t["precio"]) * (F_(t["emision_anual"]) - F_(t["quema_anual"])) for t in v["tokens"]) / sum(cm)
    assert res["inflacion_neta_pct_anual"] == pytest.approx(float(neta * 100), rel=1e-12)
    for w in (20, 33, 200):
        d = sum(F_(t["precio"]) * F_(x["cantidad"]) for t in v["tokens"] for x in t["calendario"]["desbloqueos"]
                if 0 < (pd.Timestamp(x["fecha"]) - fecha).days <= w)
        assert res["desbloqueos_pct"][str(w)] == pytest.approx(float(d / sum(cm) * 100), rel=1e-12)
    con = [(c, t) for c, t in zip(cm, v["tokens"]) if "staking_nominal" in t]
    real = sum(c * (F_(t["staking_nominal"]) - (F_(t["emision_anual"]) - F_(t["quema_anual"])) / F_(t["oferta_circulante"]))
               for c, t in con) / sum(c for c, _ in con)
    assert res["rendimiento_real_staking_pct"] == pytest.approx(float(real * 100), rel=1e-12)
    conc = sum(c * F_(t["concentracion_10_mayores"]) for c, t in con) / sum(c for c, _ in con)
    assert res["concentracion_10_mayores_pct"] == pytest.approx(float(conc * 100), rel=1e-12)
    assert res["cobertura_staking_pct"] == pytest.approx(float(sum(c for c, _ in con) / sum(cm) * 100), rel=1e-12)
    assert res["n_tokens"] == 3 and list(res["desbloqueos_pct"]) == ["20", "33", "200"]


def test_chr_token_borde_de_la_ventana_y_desbloqueos_pasados():
    v, _ = _metodo("CHR-TOKEN-001")
    res, lim = _correr("CHR-TOKEN-001", v, {"ventanas_desbloqueo": [19, 20, 29, 30]})
    cm = 2.0 * 6.0e8 + 0.5 * 4.0e8
    assert res["desbloqueos_pct"]["19"] == 0.0                            # el del 20 de julio cae a 20 días
    assert res["desbloqueos_pct"]["20"] == pytest.approx(2.0 * 3.0e7 / cm * 100)
    assert res["desbloqueos_pct"]["29"] == res["desbloqueos_pct"]["20"]
    assert res["desbloqueos_pct"]["30"] == pytest.approx((2.0 * 3.0e7 + 0.5 * 2.0e7) / cm * 100)
    assert any(x.startswith("1 desbloqueos del calendario con fecha no posterior") for x in lim)


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v["tokens"][0].update(oferta_total=5.9e8), "circulante ≤ total ≤ máxima"),
    (lambda v: v["tokens"][0].update(oferta_maxima=8.9e8), "circulante ≤ total ≤ máxima"),
    (lambda v: v["tokens"][0].pop("calendario"), "sin calendario de desbloqueos verificable"),
    (lambda v: v["tokens"][0]["calendario"].pop("fuente"), "sin calendario de desbloqueos verificable"),
    (lambda v: v["tokens"][0]["calendario"].update(desbloqueos=None), "sin calendario de desbloqueos verificable"),
    (lambda v: v["tokens"][0]["calendario"]["desbloqueos"][1].update(cantidad=2.0e8), "superan la oferta no circulante"),
    (lambda v: v["tokens"][0]["calendario"]["desbloqueos"][1].update(cantidad=0), "cantidad"),
    (lambda v: v["tokens"][1].update(id="TKA"), "identificadores de componente repetidos"),
    (lambda v: v["tokens"][0].update(concentracion_10_mayores=1.1), "concentracion_10_mayores"),
    (lambda v: v["tokens"][0].update(staking_nominal=10.0), "staking_nominal"),
    (lambda v: v["tokens"][0].update(emision_anual=-1.0), "emision_anual"),
    (lambda v: v.pop("fuente"), "fuente"), (lambda v: v.pop("ambito"), "ambito"), (lambda v: v.pop("fecha"), "fecha"),
    (lambda v: v.update(tokens=[]), "tokens"),
])
def test_chr_token_rechazos(cambio, motivo):
    v, _ = _metodo("CHR-TOKEN-001")
    cambio(v)
    _rechaza("CHR-TOKEN-001", v, {}, motivo)


def test_chr_token_los_desbloqueos_pueden_agotar_justo_la_oferta_no_circulante():
    v, _ = _metodo("CHR-TOKEN-001")
    v["tokens"][0]["calendario"]["desbloqueos"][3]["cantidad"] = 2.1e8      # 3e7 + 6e7 + 2,1e8 = 3e8 = total − circulante
    res, _ = _correr("CHR-TOKEN-001", v)
    assert res["verificacion"]["holgura_desbloqueos_min"] == pytest.approx(0.0, abs=1e-12)
    assert not any(f'"{t["id"]}"' in json.dumps(res) for t in v["tokens"])


# ============================================================================= PRV-PME-001 y PRV-CF-001
def _tir_oraculo(fechas, flujos):
    """TIR con el método de la secante de scipy sobre el valor actual neto (Real/365)."""
    t = np.array([(pd.Timestamp(f) - pd.Timestamp(fechas[0])).days / 365 for f in fechas])
    return optimize.newton(lambda r: float(np.sum(np.array(flujos) * (1 + r) ** (-t))), 0.1, tol=1e-14, maxiter=200)


def test_prv_pme_oraculo_independiente():
    v, _ = _metodo("PRV-PME-001")
    res, lim = _correr("PRV-PME-001", v, {"metodo": "PME+"})
    fl = pd.DataFrame(v["flujos"])
    ind = pd.DataFrame(v["indice"]["niveles"]).set_index("fecha")["nivel"]
    nav = v["nav_final"]["valor"]
    f = ind.iloc[-1] / ind.loc[fl["fecha"]].to_numpy()
    assert res["ks_pme_veces"] == pytest.approx(((fl["distribucion"] * f).sum() + nav) / (fl["aportacion"] * f).sum(), rel=1e-12)
    neto = (fl["distribucion"] - fl["aportacion"]).to_numpy()
    final = np.zeros(len(neto))
    final[-1] = nav
    tir = _tir_oraculo(list(fl["fecha"]), neto + final)
    assert res["tir_pct"] == pytest.approx(tir * 100, rel=1e-9)
    a = _tir_oraculo(list(fl["fecha"]), neto * f + final)
    assert res["alfa_directo_pct_anual"] == pytest.approx(math.log(1 + a) * 100, rel=1e-8)
    lam = ((fl["aportacion"] * f).sum() - nav) / (fl["distribucion"] * f).sum()
    tir_ind = _tir_oraculo(list(fl["fecha"]), lam * fl["distribucion"].to_numpy() - fl["aportacion"].to_numpy() + final)
    assert res["pme_plus"]["lambda"] == pytest.approx(lam, rel=1e-12)
    assert res["pme_plus"]["tir_indice_pct"] == pytest.approx(tir_ind * 100, rel=1e-9)
    assert res["pme_plus"]["diferencial_tir_pct"] == pytest.approx((tir - tir_ind) * 100, rel=1e-7)
    assert res["referencia_ingenua"]["exceso_ks_pme"] == pytest.approx(res["ks_pme_veces"] - 1) and lim == []
    assert res["valor_futuro"]["aportaciones"] == pytest.approx((fl["aportacion"] * f).sum())
    # un PME > 1 con alfa directo > 0, y al revés (el signo es el mismo)
    assert (res["ks_pme_veces"] > 1) == (res["alfa_directo_pct_anual"] > 0)


def test_prv_pme_el_nav_en_fecha_posterior_al_ultimo_flujo_y_metodo_sin_pme_plus():
    v, _ = _metodo("PRV-PME-001")
    v["nav_final"]["fecha"] = "2025-12-31"
    v["indice"]["niveles"].append({"fecha": "2025-12-31", "nivel": 190.0})
    res, _ = _correr("PRV-PME-001", v)
    fechas = [f["fecha"] for f in v["flujos"]] + ["2025-12-31"]
    neto = [f["distribucion"] - f["aportacion"] for f in v["flujos"]] + [38.0]
    assert res["tir_pct"] == pytest.approx(_tir_oraculo(fechas, neto) * 100, rel=1e-9)
    fac = [190.0 / n["nivel"] for n in v["indice"]["niveles"][:-1]]
    ks = (sum(f["distribucion"] * x for f, x in zip(v["flujos"], fac)) + 38.0) / sum(f["aportacion"] * x for f, x in zip(v["flujos"], fac))
    assert res["ks_pme_veces"] == pytest.approx(ks, rel=1e-12) and res["pme_plus"] is None and res["fecha_nav"] == "2025-12-31"


def test_prv_pme_sin_distribuciones_ni_tir():
    v, _ = _metodo("PRV-PME-001")
    for f in v["flujos"]:
        f["distribucion"] = 0.0
    v["nav_final"]["valor"] = 0.0
    res, lim = _correr("PRV-PME-001", v, {"metodo": "PME+"})
    assert res["tir_pct"] is None and res["alfa_directo_pct_anual"] is None and res["pme_plus"] is None
    assert res["ks_pme_veces"] == 0.0 and res["tvpi_veces"] == 0.0
    assert any("sin cambio de signo" in x for x in lim) and any("λ no está definido" in x for x in lim)


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v.pop("flujos"), "sin flujos fechados"), (lambda v: v.update(flujos=[]), "sin flujos fechados"),
    (lambda v: v["flujos"][2].pop("fecha"), "fecha"),
    (lambda v: [f.update(aportacion=0.0) for f in v["flujos"]], "sin aportaciones"),
    (lambda v: v["flujos"][2].update(aportacion=-1.0), "aportacion"),
    (lambda v: v["nav_final"].update(fecha="2025-06-29"), "anterior al último flujo"),
    (lambda v: v["nav_final"].update(valor=-1.0), "valor"),
    (lambda v: v["indice"].update(moneda="EUR"), "misma moneda"),
    (lambda v: v["indice"].update(rentabilidad_total=False), "rentabilidad total"),
    (lambda v: v["indice"].pop("rentabilidad_total"), "rentabilidad total"),
    (lambda v: v["indice"].pop("riesgo_comparable"), "riesgo_comparable"),
    (lambda v: v["indice"]["niveles"].pop(2), "no tiene nivel en 1 fechas"),
    (lambda v: v["indice"]["niveles"][2].update(nivel=0.0), "nivel"),
    (lambda v: v.pop("indice"), "indice"), (lambda v: v.pop("moneda"), "moneda"),
])
def test_prv_pme_rechazos(cambio, motivo):
    v, _ = _metodo("PRV-PME-001")
    cambio(v)
    _rechaza("PRV-PME-001", v, {}, motivo)


def test_tir_multiples_soluciones_fuera_de_rango_y_polinomio():
    """La TIR de flujos anuales es la raíz de un polinomio: se compara con `numpy.roots`."""
    u, lim = fp.UMBRALES["PRV-CF-001"], []
    dias = np.array([0.0, 365.0, 730.0, 1095.0])
    flujos = np.array([-100.0, 30.0, 40.0, 60.0])
    raices = np.roots(flujos[::-1])                                      # en x = 1/(1 + r)
    x = float(next(z.real for z in raices if abs(z.imag) < 1e-12 and z.real > 0))
    assert fp._tir(dias, flujos, u, lim, "TIR") == pytest.approx(1 / x - 1, rel=1e-11) and lim == []
    # −100, +230, −132: dos raíces (10 % y 20 %), el valor actual neto tiene el mismo signo en los dos extremos del rango:
    # se avisa de las múltiples soluciones y no se entrega ninguna
    assert fp._tir(dias[:3], np.array([-100.0, 230.0, -132.0]), u, lim, "TIR") is None
    assert "múltiples soluciones" in lim[0] and "sin TIR entre" in lim[1]
    lim.clear()
    # −100, +360, −431, +171,6: tres raíces (10 %, 20 % y 30 %): se avisa y se entrega una de ellas
    tres = fp._tir(dias, np.array([-100.0, 360.0, -431.0, 171.6]), u, lim, "TIR")
    assert any(tres == pytest.approx(x_, abs=1e-9) for x_ in (0.1, 0.2, 0.3)) and "3 cambios de signo" in lim[0]
    lim.clear()
    assert fp._tir(dias[:2], np.array([-1.0, 1e6]), u, lim, "TIR") is None and "sin TIR entre" in lim[0]
    lim.clear()
    assert fp._tir(dias[:2], np.array([-100.0, 0.5]), u, lim, "TIR") is None and "sin TIR entre" in lim[0]
    lim.clear()
    assert fp._tir(dias[:2], np.array([0.0, 5.0]), u, lim, "TIR") is None and "sin cambio de signo" in lim[0]
    # pérdida: TIR negativa
    assert fp._tir(dias[:2], np.array([-100.0, 80.0]), u, lim, "TIR") == pytest.approx(-0.2, rel=1e-11)


def test_prv_cf_aviso_de_multiples_soluciones_en_el_servicio():
    v, _ = _base("PRV-CF-001", 0)
    v["flujos"][4]["aportacion"] = 60.0                                   # una aportación tardía: tres cambios de signo
    res, lim = _correr("PRV-CF-001", v)
    assert any("múltiples soluciones" in x for x in lim)
    assert any("aportaciones por encima del compromiso" in x for x in lim) and res["aportado_sobre_compromiso"] == 1.5


def test_prv_cf_oraculo_independiente():
    v, p = _metodo("PRV-CF-001")
    res, lim = _correr("PRV-CF-001", v, {**p, "bow": 1.5, "crecimiento": -0.05, "tasas_aportacion": [0.3]})
    fl = pd.DataFrame(v["flujos"])
    neto = (fl["distribucion"] - fl["aportacion"]).to_numpy()
    final = np.zeros(len(neto))
    final[-1] = 38.0
    assert res["tir_pct"] == pytest.approx(_tir_oraculo(list(fl["fecha"]), neto + final) * 100, rel=1e-9)
    assert res["tvpi_veces"] == pytest.approx((105 + 38) / 90) and res["dpi_veces"] == pytest.approx(105 / 90)
    assert res["rvpi_veces"] == pytest.approx(38 / 90) and res["aportado_sobre_compromiso"] == pytest.approx(0.9)
    assert [s["flujo_neto_acumulado"] for s in res["curva_j"]["serie"]] == pytest.approx(list(np.cumsum(neto)))
    assert res["curva_j"]["minimo_sobre_compromiso"] == pytest.approx(-0.8) and res["curva_j"]["fecha_minimo"] == "2021-06-30"
    # Takahashi-Alexander con recurrencia vectorial distinta: estado (aportado, NAV)
    ap, nav, serie = 90.0, 38.0, []
    for t in range(7, 11):
        c = 0.3 * (100.0 - ap)
        d = (t / 10) ** 1.5 * nav * 0.95
        nav, ap = nav * 0.95 + c - d, ap + c
        serie.append((t, c, d, nav))
    pr = res["proyeccion"]
    assert [(s["anio_vida"], s["aportacion"], s["distribucion"], s["nav"]) for s in pr["serie"]] == [pytest.approx(x) for x in serie]
    tot_d = 105 + sum(x[2] for x in serie)
    assert pr["tvpi_final_veces"] == pytest.approx((tot_d + serie[-1][3]) / ap)
    assert pr["dpi_final_veces"] == pytest.approx(tot_d / ap) and pr["bow"] == 1.5 and pr["crecimiento"] == -0.05
    assert res["referencia_ingenua"]["diferencia_tir_pct"] == pytest.approx(res["tir_pct"] - 11.0) and lim == []


def test_prv_cf_proyeccion_falta_un_supuesto_o_la_vida_ya_cumplida():
    v, p = _metodo("PRV-CF-001")
    for quitar in ("tasas_aportacion", "crecimiento"):
        res, lim = _correr("PRV-CF-001", v, {k: x for k, x in p.items() if k != quitar})
        assert res["proyeccion"] is None and any(quitar in x and "proyección no calculada" in x for x in lim)
    w = copy.deepcopy(v)
    del w["vida_anios"]
    res, lim = _correr("PRV-CF-001", w, p)
    assert res["proyeccion"] is None and any("vida_anios" in x for x in lim)
    w["vida_anios"] = 6                                                    # edad 6: ya cumplida
    res, lim = _correr("PRV-CF-001", w, p)
    assert res["proyeccion"]["serie"] == [] and any("ya ha cumplido su vida" in x for x in lim)
    assert res["proyeccion"]["tvpi_final_veces"] == pytest.approx(res["tvpi_veces"])
    w["vida_anios"] = 7                                                    # un año: se distribuye todo
    res, _ = _correr("PRV-CF-001", w, p)
    s = res["proyeccion"]["serie"]
    assert len(s) == 1 and s[0]["distribucion"] == pytest.approx(38.0 * 1.08) and s[0]["nav"] == pytest.approx(s[0]["aportacion"])


def test_prv_cf_la_edad_son_anios_completos():
    """Real/365: del 2019-03-31 al 2026-03-29 van 2 555 días, 7 años justos; un día menos, 6."""
    v, p = _metodo("PRV-CF-001")
    v["navs"][-1]["fecha"] = "2026-03-28"
    assert _correr("PRV-CF-001", v, p)[0]["proyeccion"]["edad_anios"] == 6
    v["navs"][-1]["fecha"] = "2026-03-29"
    assert _correr("PRV-CF-001", v, p)[0]["proyeccion"]["edad_anios"] == 7


@pytest.mark.parametrize("cambio,motivo", [
    (lambda v: v.pop("flujos"), "sin flujos fechados"), (lambda v: v.pop("navs"), "navs"),
    (lambda v: v.update(navs=[]), "navs"), (lambda v: v.update(compromiso=0), "compromiso"),
    (lambda v: v["navs"][-1].update(fecha="2025-06-29"), "anterior al último flujo"),
    (lambda v: v["navs"][-1].update(valor=-1), "valor"),
    (lambda v: v.update(vida_anios=0), "vida_anios"), (lambda v: v.update(vida_anios=7.5), "vida_anios"),
    (lambda v: v["referencia_cosecha"].pop("tvpi_mediana"), "tvpi_mediana"),
    (lambda v: v["referencia_cosecha"].update(tir_mediana=11.0), "tir_mediana"),
    (lambda v: v["flujos"][1].update(fecha="sin fecha"), "fecha"),
])
def test_prv_cf_rechazos(cambio, motivo):
    v, p = _metodo("PRV-CF-001")
    cambio(v)
    _rechaza("PRV-CF-001", v, p, motivo)


# ============================================================================= ALT-HF-001
def _hf_oraculo(y, Fm):
    """MCO, Newey-West con bucles y R², sin álgebra compartida con la ficha."""
    n = len(y)
    X = np.column_stack([np.ones(n), Fm])
    b = np.linalg.solve(X.T @ X, X.T @ y)
    e = y - X @ b
    L = math.floor(4 * (n / 100) ** (2 / 9))
    S = np.zeros((X.shape[1], X.shape[1]))
    for i in range(n):
        for j in range(n):
            if abs(i - j) <= L:
                S += (1 - abs(i - j) / (L + 1)) * e[i] * e[j] * np.outer(X[i], X[j])
    inv = np.linalg.inv(X.T @ X)
    ee = np.sqrt(np.diag(inv @ S @ inv))
    return b, ee, 1 - np.sum(e ** 2) / np.sum((y - y.mean()) ** 2)


def _hf_datos_ruidosos():
    v, _ = _base("ALT-HF-001", 2)
    for i, fila in enumerate(v["serie"]):
        fila["r"] += 0.8 * math.sin(1.7 * i) + 0.3 * math.cos(0.4 * i)
    return v


@pytest.mark.parametrize("desuavizar", [False, True])
def test_alt_hf_oraculo_independiente(desuavizar):
    v = _hf_datos_ruidosos()
    res, _ = _correr("ALT-HF-001", v, {"desuavizar": desuavizar})
    t = pd.DataFrame(v["serie"])
    nombres = list(fp.UMBRALES["ALT-HF-001"]["factores_fung_hsieh"])
    r, rf, Fm = t["r"].to_numpy(), t["rf"].to_numpy(), t[nombres].to_numpy()
    if desuavizar:
        phi = stats.linregress(r[:-1], r[1:]).slope
        r, rf, Fm = (r[1:] - phi * r[:-1]) / (1 - phi), rf[1:], Fm[1:]
        assert res["desuavizado"] == {"aplicado": True, "phi": pytest.approx(phi, rel=1e-10)}
    else:
        assert res["desuavizado"] == {"aplicado": False, "phi": None}
    b, ee, r2 = _hf_oraculo(r - rf, Fm)
    assert res["alfa_periodo_pct"] == pytest.approx(b[0], rel=1e-8)
    assert res["alfa_anual_pct"] == pytest.approx(((1 + b[0] / 100) ** 12 - 1) * 100, rel=1e-8)
    assert res["t_alfa"] == pytest.approx(b[0] / ee[0], rel=1e-7) and res["r2"] == pytest.approx(r2, rel=1e-9)
    for j, nb in enumerate(nombres):
        assert res["betas"][nb]["beta"] == pytest.approx(b[j + 1], rel=1e-8)
        assert res["betas"][nb]["t"] == pytest.approx(b[j + 1] / ee[j + 1], rel=1e-7)
    d = res["descomposicion_media_pct"]
    assert d["total"] == pytest.approx(float(np.mean(r - rf)), rel=1e-10)
    assert d["por_factores"] == pytest.approx(float(Fm.mean(axis=0) @ b[1:]), rel=1e-8)
    assert d["alfa"] + d["por_factores"] == pytest.approx(d["total"], rel=1e-10)
    assert res["referencia_ingenua"]["exceso_periodo_pct"] == pytest.approx(b[0], rel=1e-8)
    assert res["n"] == len(r) and res["n_observaciones"] == 48 and res["rezagos_nw"] == math.floor(4 * (len(r) / 100) ** (2 / 9))


def test_alt_hf_en_exceso_y_phi_negativo():
    v = _hf_datos_ruidosos()
    a, _ = _correr("ALT-HF-001", v, {"desuavizar": False})
    for fila in v["serie"]:
        fila["r"] -= fila.pop("rf")
    _rechaza("ALT-HF-001", v, {}, "falta «rf»")
    v["en_exceso"] = True
    b, _ = _correr("ALT-HF-001", v, {"desuavizar": False})
    assert b["alfa_periodo_pct"] == pytest.approx(a["alfa_periodo_pct"], rel=1e-10)
    v["serie"][0]["rf"] = 0.1
    _rechaza("ALT-HF-001", v, {}, "declare solo uno")
    v, _ = _base("ALT-HF-001", 1)                                          # serie sin suavizar: φ estimado negativo
    res, lim = _correr("ALT-HF-001", v, {})
    assert res["desuavizado"]["phi"] < 0 and any("sin evidencia de suavizado" in x for x in lim)


@pytest.mark.parametrize("cambio,params,motivo", [
    (lambda v: v.update(serie=v["serie"][:35]), {}, r"35 observaciones mensuales \(< 36\)"),
    (lambda v: v["serie"].pop(20), {}, "no mensuales consecutivas"),
    (lambda v: v["serie"][3].pop("PTFSFX"), {}, "PTFSFX"),
    (lambda v: v["serie"][3].update(rf=None), {}, "falta «rf» en 1 meses"),
    (lambda v: [f.update(SMB=2 * f["MKT"]) for f in v["serie"]], {}, "no identificada"),
    (lambda v: [f.update(r=1.0) for f in v["serie"]], {}, "φ del AR"),
    (lambda v: [f.update(r=f["rf"]) for f in v["serie"]], {"desuavizar": False}, "sin varianza"),
    (lambda v: None, {"factores": ["MKT", "NO_ESTA"]}, "NO_ESTA"),
])
def test_alt_hf_rechazos(cambio, params, motivo):
    v, _ = _base("ALT-HF-001", 2)
    cambio(v)
    _rechaza("ALT-HF-001", v, params, motivo)


def test_alt_hf_con_36_observaciones_justas_y_factores_declarados():
    v, _ = _base("ALT-HF-001", 2)
    v["serie"] = v["serie"][:36]
    res, _ = _correr("ALT-HF-001", v, {"factores": ["MKT", "CREDITO"]})
    assert res["factores"] == ["MKT", "CREDITO"] and set(res["betas"]) == {"MKT", "CREDITO"} and res["n"] == 35


# ============================================================================= ALT-AUC-001
def _auc_indice_por_dummies(tr, anios):
    """Oráculo de ventas repetidas: efectos fijos de pieza y de año sobre todas las ventas de piezas repetidas (con dos
    ventas por pieza equivale a la regresión en diferencias de Bailey-Muth-Nourse)."""
    piezas = sorted({t["id_pieza"] for t in tr})
    X = np.zeros((len(tr), len(piezas) + len(anios) - 1))
    y = np.zeros(len(tr))
    for i, t in enumerate(tr):
        X[i, piezas.index(t["id_pieza"])] = 1.0
        k = anios.index(int(t["fecha"][:4]))
        if k > 0:
            X[i, len(piezas) + k - 1] = 1.0
        y[i] = math.log(t["precio"])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return [100.0] + [100.0 * math.exp(x) for x in b[len(piezas):]]


def test_alt_auc_oraculo_ventas_repetidas_por_efectos_fijos():
    v, p = _metodo("ALT-AUC-001")
    res, lim = _correr("ALT-AUC-001", v, p)
    ind = _auc_indice_por_dummies(v["transacciones"], list(range(2010, 2020)))
    assert [x["indice"] for x in res["indice"]] == pytest.approx(ind, rel=1e-9)
    assert [x["periodo"] for x in res["indice"]] == list(range(2010, 2020))
    total = ind[-1] / ind[0]
    assert res["rentabilidad_anual_bruta_pct"] == pytest.approx((total ** (1 / 9) - 1) * 100, rel=1e-9)
    assert res["rentabilidad_anual_neta_pct"] == pytest.approx(((total * 0.85) ** (1 / 9) - 1) * 100, rel=1e-9)
    assert res["volatilidad_pct"] == pytest.approx(np.std(np.diff(ind) / np.array(ind[:-1]), ddof=1) * 100, rel=1e-9)
    assert res["n_transacciones"] == 600 and res["n_pares"] == 300 and res["pares_descartados_mismo_periodo"] == 0
    assert res["supuesto_neto"] == "una compraventa en los 9 años del índice" and res["comisiones"] == 0.15
    assert res["ajuste_sesgo_seleccion"] == "ninguno (declarado)" and lim == []
    assert res["rentabilidad_anual_neta_pct"] < res["rentabilidad_anual_bruta_pct"]


def test_alt_auc_oraculo_hedonico_por_ecuaciones_normales():
    v, p = _metodo("ALT-AUC-001")
    res, _ = _correr("ALT-AUC-001", v, {**p, "metodo": "hedonico"})
    tr = v["transacciones"]
    X = np.array([[1.0, t["caracteristicas"]["antiguedad"], t["caracteristicas"]["tamano"]]
                  + [1.0 if int(t["fecha"][:4]) == a else 0.0 for a in range(2011, 2020)] for t in tr])
    y = np.array([math.log(t["precio"]) for t in tr])
    b = np.linalg.solve(X.T @ X, X.T @ y)
    e = y - X @ b
    assert [x["indice"] for x in res["indice"]] == pytest.approx([100.0] + [100 * math.exp(x) for x in b[3:]], rel=1e-9)
    assert res["dispersion"]["desviacion_residual_pct"] == pytest.approx(math.sqrt(e @ e / (600 - 12)) * 100, rel=1e-8)
    assert res["dispersion"]["iqr_residual_pct"] == pytest.approx((np.percentile(e, 75) - np.percentile(e, 25)) * 100, rel=1e-7)
    assert res["caracteristicas"] == ["antiguedad", "tamano"]
    sv = res["segunda_via"]
    vr = _correr("ALT-AUC-001", v, p)[0]
    assert sv["metodo"] == "ventas_repetidas" and sv["rentabilidad_anual_bruta_pct"] == pytest.approx(vr["rentabilidad_anual_bruta_pct"])
    assert sv["diferencia_pct"] == pytest.approx(res["rentabilidad_anual_bruta_pct"] - vr["rentabilidad_anual_bruta_pct"])
    assert sv["diferencia_maxima_indice"] == pytest.approx(
        max(abs(a["indice"] - b_["indice"]) for a, b_ in zip(res["indice"], vr["indice"])))


def test_alt_auc_sin_caracteristicas_no_hay_segunda_via_ni_hedonico():
    v, p = _metodo("ALT-AUC-001")
    for t in v["transacciones"][::7]:
        del t["caracteristicas"]
    res, lim = _correr("ALT-AUC-001", v, p)
    assert res["segunda_via"] is None and res["caracteristicas"] == []
    assert any("segunda vía (hedonico) no calculada: sin características" in x for x in lim)
    _rechaza("ALT-AUC-001", v, {"metodo": "hedonico"}, "rechazo: sin características en todas las transacciones")
    del v["referencia"]
    res, lim = _correr("ALT-AUC-001", v, {})
    assert res["rentabilidad_anual_neta_pct"] is None and res["referencia_ingenua"]["rentabilidad_real_anual_pct"] is None
    assert any("sin comisiones declaradas" in x for x in lim) and any("referencias ingenuas no comparadas" in x for x in lim)


def test_alt_auc_pares_del_mismo_anio_se_descartan_y_tres_ventas_dan_dos_pares():
    v, p = _metodo("ALT-AUC-001")
    tr = v["transacciones"]
    tr.append({**tr[0], "fecha": tr[0]["fecha"][:4] + "-12-28"})           # la pieza P000 se vende otra vez el mismo año
    res, _ = _correr("ALT-AUC-001", v, p)
    assert res["n_pares"] == 300 and res["pares_descartados_mismo_periodo"] == 1 and res["n_transacciones"] == 601
    tr.append({**tr[1], "fecha": "2019-12-30", "precio": tr[1]["precio"] * 1.3})   # y una tercera venta en 2019
    res, _ = _correr("ALT-AUC-001", v, p)
    assert res["n_pares"] == 301


@pytest.mark.parametrize("cambio,params,motivo", [
    (lambda v: v.update(transacciones=v["transacciones"][:499]), {}, r"499 transacciones \(< 500\)"),
    (lambda v: v.update(transacciones=[{**t, "id_pieza": f"U{i}"} if i >= 396 else t for i, t in enumerate(v["transacciones"])]),
     {}, r"198 pares de ventas repetidas \(< 200\)"),
    (lambda v: v.update(transacciones=[t for t in v["transacciones"] if t["fecha"][:4] != "2014"] + [
        {**t, "fecha": "2010-03-01"} for t in v["transacciones"][:120]]), {}, "hay años sin transacciones"),
    (lambda v: [t.update(fecha="2015" + t["fecha"][4:]) for t in v["transacciones"] if t["fecha"][:4] > "2011"], {},
     "hay años sin transacciones"),
    (lambda v: [t.update(fecha="2010" + t["fecha"][4:]) for t in v["transacciones"] if t["fecha"][:4] > "2011"], {},
     r"transacciones de 2 años \(< 3\)"),
    (lambda v: v["transacciones"][5]["caracteristicas"].pop("tamano"), {"metodo": "hedonico"}, "no son las mismas"),
    (lambda v: [t["caracteristicas"].update(tamano=1.0) for t in v["transacciones"]], {"metodo": "hedonico"}, "no se identifica"),
    (lambda v: [t.update(caracteristicas={f"c{i}": 1.0 * i for i in range(21)}) for t in v["transacciones"]],
     {"metodo": "hedonico"}, r"21 \(máximo 20\)"),
    (lambda v: v.pop("categoria"), {}, "categoria"),
    (lambda v: v["transacciones"][9].pop("id_pieza"), {}, "id_pieza"),
    (lambda v: v["referencia"].update(inflacion_anual=-1.0), {}, "inflacion_anual"),
    (lambda v: v["referencia"].pop("rv_global_anual"), {}, "rv_global_anual"),
])
def test_alt_auc_rechazos(cambio, params, motivo):
    v, _ = _metodo("ALT-AUC-001")
    cambio(v)
    _rechaza("ALT-AUC-001", v, params, motivo)


def test_alt_auc_periodos_sin_enlace_no_se_identifican():
    """Todas las ventas repetidas enlazan 2010–2014 entre sí y 2015–2019 entre sí, pero no un bloque con el otro."""
    tr = []
    for i in range(300):
        bloque = 0 if i % 2 == 0 else 5
        a, b = bloque + i % 5, bloque + (i % 5 + 1 + (i // 5) % 4) % 5
        for k in sorted((a, b)):
            tr.append({"id_pieza": f"P{i}", "fecha": f"{2010 + k}-06-15", "precio": 100.0 + i + 3 * k})
    v = {"categoria": "arte", "transacciones": tr}
    _rechaza("ALT-AUC-001", v, {}, "no se identifica")
