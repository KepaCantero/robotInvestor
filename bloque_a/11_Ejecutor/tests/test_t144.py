"""T-144 · Hallazgos de la QA r01 de T-135: copias de una serie en la amplitud de IDX-CONC-001 con una sesión ausente o
redondeada (H-01), el aviso de CHR-TOKEN-001 con un dato movido (H-02), el coste n²·T (H-03), precios ≤ 0 (H-04) y dos
copias más otra serie (H-05, límite declarado)."""
import copy
import time

import numpy as np
import pandas as pd
import pytest
from bloque_a.motor import fichas_mon_idx as fm
from bloque_a.motor import fichas_p2 as fp
from bloque_a.motor import frontera_b as fb
from bloque_a.motor.operaciones import ErrorFicha

FECHAS = pd.bdate_range("2025-06-02", periods=320)
AVISO = "aviso (1.6)"


def _paseo(semilla, deriva=0.0, sd=0.01, nivel=100.0, fechas=FECHAS):
    rng = np.random.default_rng(semilla)
    return pd.Series(nivel * np.exp(np.cumsum(rng.normal(deriva, sd, len(fechas)))), index=fechas)


def _correr(series, comp=None, p=None):
    v = {"composicion": comp or fm._composicion(10, igual=False)}
    return fm.FICHAS["IDX-CONC-001"]["fn"]({"valores": v, "series": series, "series_rol": {}}, dict(p or {"top_n": 5}))


def _es_copia(x, y, anios_minimos=1.0):
    t = pd.DataFrame({"x": x, "y": y}).sort_index()
    g = fb._etiquetas_series_copiadas(t.to_numpy(dtype=float).T,
                                      np.asarray((t.index - t.index[0]).days, dtype=float) / fm.DIAS_ANIO,
                                      fb.FRONTERA_B["tolerancia_clon"], anios_minimos)
    return bool(g[0] == g[1])


A = _paseo(7, 0.0005, nivel=1234.5)
A50 = _paseo(7, 0.0005, nivel=50.0)


# ---------------------------------------------------------------- H-01 · copias que antes no se agrupaban
@pytest.mark.parametrize("nombre, copia, base", [
    ("una sesión ausente", A.drop(A.index[150]), A),
    ("tres sesiones ausentes y a escala", A.drop(A.index[[10, 150, 300]]) * 3, A),
    ("en libras con 2 decimales (cotiza en peniques)", (A / 100).round(2), A),
    ("a otra divisa a un cambio fijo con 4 decimales", (A * 1.0837).round(4), A),
    ("otro proveedor con 2 decimales", A50.round(2), A50.round(6)),
    ("otro proveedor con 3 decimales", A50.round(3), A50.round(6)),
    ("redondeada y con una sesión ausente", (A / 100).round(2).drop(A.index[200]), A),
])
def test_h01_la_misma_serie_de_otra_fuente_es_una_copia(nombre, copia, base):
    assert _es_copia(base, copia), nombre
    res, lim = _correr({"C00": base, "SECRETA": copia})
    assert res["amplitud"] is None and not any("SECRETA" in x or "C00" in x for x in lim)


@pytest.mark.parametrize("decimales", [None, 3, 2])
def test_h01_series_distintas_muy_correladas_no_son_copias(decimales):
    """Dos índices de un mercado con ρ ≈ 0,995, un índice de precios y su rentabilidad total (2 %/año) y, sin redondear,
    un fondo frente a su índice con un error de seguimiento del 0,1 % y del 0,01 % al año: 0 de 100 en cada caso (el
    revisor midió que un cociente ingenuo al 1 % agrupaba el 6 % de los índices y todos los fondos)."""
    def r(s):
        return s if decimales is None else s.round(decimales)
    cuentas = {"indices": 0, "rentabilidad_total": 0, "fondo_01": 0, "fondo_001": 0}
    for s in range(100):
        rng = np.random.default_rng(1000 + s)
        m = rng.normal(0.0003, 0.011, len(FECHAS))
        precio = r(pd.Series(100 * np.cumprod(1 + m), index=FECHAS))
        cuentas["indices"] += _es_copia(precio, r(pd.Series(100 * np.cumprod(1 + m + rng.normal(0, 0.0011, len(FECHAS))), index=FECHAS)))
        cuentas["rentabilidad_total"] += _es_copia(precio, r(pd.Series(100 * np.cumprod(1 + m + 0.02 / 252), index=FECHAS)))
        f1 = r(pd.Series(100 * np.cumprod(1 + m + rng.normal(0, 0.001 / np.sqrt(252), len(FECHAS))), index=FECHAS))
        f2 = r(pd.Series(100 * np.cumprod(1 + m + rng.normal(0, 0.0001 / np.sqrt(252), len(FECHAS))), index=FECHAS))
        cuentas["fondo_01"] += _es_copia(precio, f1)
        cuentas["fondo_001"] += _es_copia(precio, f2)
    assert cuentas["indices"] == 0 and cuentas["rentabilidad_total"] == 0
    if decimales is None or decimales == 3:
        assert cuentas["fondo_01"] == 0
    if decimales is None:
        assert cuentas["fondo_001"] == 0
    # Con 2 decimales a 100 (paso relativo 5e-5), un fondo con un error de seguimiento de 0,01 %/año no se distingue de su
    # índice a esa resolución: se toma por copia a menudo (límite declarado en INC-T128-01; falla cerrado)


def test_h01_paso_de_precio():
    x = np.array([[12.34, 12.35, 99.99], [1.0, 2.0, 3.0], [1.2345, 1.2, np.nan], [np.pi, np.e, 1.1]])
    hay = ~np.isnan(x)
    paso = fb._paso_de_precio(x, hay, 1e-10)
    assert paso[:3].tolist() == [0.01, 1.0, 0.0001]
    assert paso[3] * 0.5 / 1.1 <= 1e-9                                 # sin redondear: del orden de la tolerancia numérica


def test_h01_la_regla_de_niveles_a_mano():
    """Cociente constante salvo el redondeo de cada serie: |log(pᵢ/pₖ) − c| ≤ bᵢ + bₖ en cada fecha común."""
    anios = np.arange(5) / 2.0
    base = np.array([100.0, 110.0, 99.0, 120.0, 108.0]) * 1.0123456789       # sin redondear
    redondeada = np.round(base / 7, 2)                                   # paso 0,01 a ~15: cota ~3,3e-4 por fecha
    assert fb._etiquetas_series_copiadas(np.vstack([base, redondeada]), anios, 0.01, 1.0).tolist() == [0, 0]
    movida = redondeada.copy()
    movida[2] += 0.02                                                     # dos pasos: ya no es el redondeo
    assert len(set(fb._etiquetas_series_copiadas(np.vstack([base, movida]), anios, 0.01, 1.0).tolist())) == 2
    con_hueco = base.copy()
    con_hueco[2] = np.nan                                                 # una fecha sin precio: solo cuentan las comunes
    assert fb._etiquetas_series_copiadas(np.vstack([base * 2, con_hueco]), anios, 0.01, 1.0).tolist() == [0, 0]
    corta = np.array([np.nan, np.nan, np.nan, 120.0, 108.0]) * 1.0123456789  # 0,5 años en común (< 1): no es copia
    assert len(set(fb._etiquetas_series_copiadas(np.vstack([base, corta]), anios, 0.01, 1.0).tolist())) == 2


def test_h01_la_cota_no_es_mas_laxa_que_la_de_los_casi_clones():
    """Con un paso de precio grande frente al precio (0,01 a 0,05: 10 %), la cota se queda en log(1 + tolerancia_clon)."""
    anios = np.arange(5) / 2.0
    a = np.array([0.05, 0.06, 0.05, 0.07, 0.06])
    b = a * 1.0123456789 * np.array([1.0, 1.0, 1.0, 1.0, 1.03])          # un 3 % fuera en la última fecha
    assert len(set(fb._etiquetas_series_copiadas(np.vstack([a, b]), anios, 0.01, 1.0).tolist())) == 2
    c = a * 1.0123456789 * np.array([1.0, 1.0, 1.0, 1.0, 1.009])         # dentro del 1 %
    assert fb._etiquetas_series_copiadas(np.vstack([a, c]), anios, 0.01, 1.0).tolist() == [0, 0]


def test_h01_tolerancia_numerica_es_la_de_la_ficha():
    assert fb.FRONTERA_B["tolerancia_numerica_copias"] == fm.FICHAS["IDX-CONC-001"]["tol"]


def test_h01_la_regla_de_rentabilidades_sigue_viva():
    """Una cadena de casi copias (rentabilidades ×1,009ʲ) no tiene cociente constante, pero se agrupa por las
    rentabilidades (cierre transitivo), como en T-135."""
    rA = A.pct_change().fillna(0).to_numpy()
    cadena = {"B": _paseo(8, -0.0005), "A": A}
    for j in range(1, 30):
        cadena[f"K{j:02d}"] = pd.Series(100 * np.cumprod(1 + rA * (1 + 0.009 * j)), index=FECHAS)
    res, _ = _correr(cadena)
    assert res["amplitud"] is None


def test_h01_el_desfase_de_una_sesion_sigue_siendo_un_limite_declarado():
    desfase = pd.Series(A.to_numpy(), index=FECHAS + pd.offsets.BDay(1))
    assert not _es_copia(A, desfase)


# ---------------------------------------------------------------- H-03 · coste
def test_h03_el_tramo_no_cambia_el_resultado(monkeypatch):
    rng = np.random.default_rng(3)
    series = {f"S{i:02d}": _paseo(100 + i) for i in range(12)}
    series["S03"] = series["S00"] * 2
    series["S05"] = (series["S01"] / 100).round(2).drop(FECHAS[40])
    series["S07"] = series["S03"].iloc[30:] * 5
    series["S09"] = series["S09"].iloc[-280:]
    tabla = pd.DataFrame(series).sort_index()
    m, anios = tabla.to_numpy(dtype=float).T, np.asarray((tabla.index - tabla.index[0]).days, dtype=float) / 365
    ref = fb._etiquetas_series_copiadas(m, anios, 0.01, 1.0)
    assert len(set(ref.tolist())) == 12 - 3 and ref[0] == ref[3] == ref[7] and ref[1] == ref[5]
    for tramo in (1, 7, 64, 10_000):
        monkeypatch.setattr(fb, "ELEMENTOS_POR_TRAMO", tramo)
        assert fb._etiquetas_series_copiadas(m, anios, 0.01, 1.0).tolist() == ref.tolist(), tramo
    del rng


def test_h03_indice_grande_con_salida_y_exclusion_sin_fechas_comunes():
    """El caso del revisor con n = 2000: 164 s en T-135; ahora segundos (cota holgada de 60 s en la prueba)."""
    fl = pd.bdate_range("2016-11-01", periods=2520)
    rng = np.random.default_rng(2000)
    m = rng.normal(0, 0.01, len(fl))
    series = {f"S{i:04d}": pd.Series(100 * np.exp(np.cumsum(m + rng.normal(0, 0.01, len(fl)))), index=fl)
              for i in range(2000)}
    series["S0000"] = series["S0000"].iloc[-380:]
    series["S0001"] = series["S0001"].iloc[:300]
    comp = {"fecha": "2026-10-31", "componentes": [{"id": k, "peso": 1 / 2000, "sector": "X"} for k in series]}
    t0 = time.perf_counter()
    res, _ = _correr(series, comp=comp)
    assert time.perf_counter() - t0 < 60 and res["amplitud"] is not None


# ---------------------------------------------------------------- H-04 · precios ≤ 0 o no finitos
@pytest.mark.parametrize("malo", [0.0, -1.0, np.inf])
@pytest.mark.parametrize("via", ["valores", "series"])
def test_h04_precios_no_positivos_se_rechazan(malo, via):
    x = A.copy()
    x.iloc[100] = malo
    if via == "series":
        with pytest.raises(ErrorFicha, match="no finitos"):
            _correr({"C00": x, "C01": _paseo(8)})
        return
    v = {"composicion": fm._composicion(10, igual=False),
         "precios": {"C00": [{"fecha": str(d.date()), "precio": float(p)} for d, p in x.items()],
                     "C01": [{"fecha": str(d.date()), "precio": float(p)} for d, p in _paseo(8).items()]}}
    with pytest.raises(ErrorFicha):
        fm.FICHAS["IDX-CONC-001"]["fn"]({"valores": v, "series": {}, "series_rol": {}}, {"top_n": 5})


# ---------------------------------------------------------------- H-02 · el aviso de CHR-TOKEN-001 con un dato movido
def _tokens(staking: bool, campo: str):
    caso = fp.CASOS_CONTROL["CHR-TOKEN-001"][1]
    v = {}
    for d in caso["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    base = copy.deepcopy(v["tokens"][0])
    base.update(id="FIJO", precio=3.3, oferta_circulante=4.2e8, oferta_total=4.2e8, oferta_maxima=4.2e8,
                emision_anual=0.0, quema_anual=0.0, calendario={"fuente": "documentación", "desbloqueos": []})
    base.pop("staking_nominal", None)
    base.pop("concentracion_10_mayores", None)
    if staking:
        base.update(staking_nominal=0.037, concentracion_10_mayores=0.28)
    c = copy.deepcopy(base)
    c["id"] = "COPIA_SECRETA"
    if campo == "oferta_total":
        c["oferta_total"] = c["oferta_maxima"] = base["oferta_total"] * 1.04
    elif campo in ("emision_anual", "quema_anual"):
        c[campo] = 1.2e6
    elif campo == "oferta_circulante":
        c[campo] = base[campo] * 0.96
    else:
        c[campo] = base[campo] * 1.04
    v["tokens"] += [base, c]
    return v, dict(caso.get("parametros") or {})


@pytest.mark.parametrize("staking, campo", [(s, c) for s in (False, True) for c in ("oferta_circulante", "oferta_total",
                                                                                  "oferta_maxima")] + [(True, "precio")])
def test_h02_un_dato_movido_de_un_token_de_oferta_fija_da_el_aviso(staking, campo):
    """`oferta_total` mueve la total y la máxima a la vez (la máxima repite la total en los dos). Sin *staking* ni
    concentración, mover solo el precio no da aviso: es la forma de dos tokens distintos de la misma oferta fija y
    redonda (T-135, QA r03 de T-127, H-06), que solo coinciden en un dato informativo; el revisor tampoco lo pide."""
    v, p = _tokens(staking, campo)
    try:
        _, lim = fp.FICHAS["CHR-TOKEN-001"]["fn"]({"valores": v, "series": {}, "series_rol": {}}, p)
    except ErrorFicha:
        return                                                            # un rechazo también cierra la vía
    assert sum(x.startswith(AVISO) for x in lim) >= 1, (staking, campo)
    assert not any("COPIA_SECRETA" in x or "FIJO" in x for x in lim)


def test_h02_lo_que_repiten_los_dos_no_es_coincidencia_informativa():
    """Dos tokens distintos de la misma oferta fija y redonda (circulante = total = máxima) y otro precio: coinciden en la
    circulante (informativa) y en la total y la máxima (repetidas en los dos: triviales), así que no hay aviso (T-135 H-06
    no vuelve)."""
    firmas = [(3.3, 1e9, 1e9, 1e9, 0.0, 0.0, None, None), (7.1, 1e9, 1e9, 1e9, 0.0, 0.0, None, None)]
    rep = [(False, False, True, True, False, False, False, False)] * 2
    lim: list[str] = []
    assert fb._aviso_casi_clones(firmas, 0.01, lim, rep) == 0 and lim == []
    # el mismo par con la circulante movida en uno: un dato movido (la total del otro ya no repite)
    firmas2 = [(3.3, 1e9, 1e9, 1e9, 0.0, 0.0, 0.03, 0.2), (3.3, 0.96e9, 1e9, 1e9, 0.0, 0.0, 0.03, 0.2)]
    rep2 = [(False, False, True, True, False, False, False, False), (False, False, False, True, False, False, False, False)]
    assert fb._aviso_casi_clones(firmas2, 0.01, lim, rep2) == 2 and lim
    # sin `repetidos` (las fichas que no lo pasan) se comparan todos los datos de la firma tal cual
    assert fb._aviso_casi_clones(firmas2, 0.01, [], None) == 2
    assert fb._aviso_casi_clones(firmas, 0.01, [], None) == 2             # sin marcar, la total y la máxima sí informan


# ---------------------------------------------------------------- H-05 · límite declarado (documentado, no cambia)
def test_h05_dos_copias_y_otra_serie_siguen_pesando_cada_una():
    """Decisión documentada en INC-T128-01 (Ronda T-144): cada serie pesa en el cálculo; contar cada grupo una vez
    cambiaría el caso a mano de la ficha y es del operador."""
    b = next(_paseo(s, 0.002) for s in range(100, 200) if float(_paseo(s, 0.002).iloc[-1] > _paseo(s, 0.002).iloc[-200:].mean())
             != float(A.iloc[-1] > A.iloc[-200:].mean()))
    res, _ = _correr({"B": b, "K0": A, "K1": A * 2})
    assert res["amplitud"] is not None and res["amplitud"]["porcentaje_sobre_media"] in (1 / 3, 2 / 3)
