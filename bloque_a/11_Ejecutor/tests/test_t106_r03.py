"""T-106 · ronda r03 (QA r02 NO APTO): umbrales fijos en MON e IDX (H-14), peticiones mal formadas rechazadas y en RC
(H-15), incertidumbre de las probabilidades de MON-EXP (H-16) y pruebas de las reglas y fórmulas que solo protegían los
oráculos del revisor (H-18). Los oráculos de FON-DISC y FON-FLOW se calculan aquí aparte, desde la ficha del Catálogo."""
import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.motor import fichas_mon_idx, servicio
from bloque_a.motor.operaciones import ErrorFicha


class _Proveedor:
    as_of = None
    nombre = "pruebas"


def _motor(tmp_path, raiz=None):
    cfg = cargar_config()
    if raiz is not None:
        cfg.setdefault("rutas", {})["raiz_paquete"] = str(raiz)
    return servicio.Motor(Almacen(Path(tmp_path) / "almacen"), _Proveedor(), cfg)


def _caso(ficha):
    caso = servicio.CASOS_CONTROL[ficha][0]
    return [dict(d) for d in caso.get("datos") or []], dict(caso.get("parametros") or {})


def _servir(m, ficha, datos, params, **extra):
    return m.servir({"operacion": ficha, "datos": datos, "parametros": params, "fecha_corte": "2026-11-12", **extra}, "AG-21")


# ================================================================================================== H-14
@pytest.mark.parametrize("ficha,umbral", [("IDX-ERP-001", {"anios_historia_min": 1}), ("IDX-ERP-001", {"N_rango": [1, 100]}),
                                          ("IDX-ERP-001", {"lambda_reversion_rango": [-5, 5]}), ("IDX-REL-001", {"anios_min": 1}),
                                          ("IDX-CONC-001", {"top_n_rango": [1, 10 ** 6]}), ("MON-FIX-001", {"nodos_min": 1}),
                                          ("MON-EXP-001", {"nodos_min": 99}), ("MON-REAL-001", {"anios_min": 10 ** 6}),
                                          ("MON-YLD-001", {"anios_percentil_min": 0}), ("IDX-REB-001", {"eventos_min": 1})])
def test_h14_un_umbral_de_la_ficha_en_la_peticion_se_rechaza(tmp_path, ficha, umbral):
    datos, params = _caso(ficha)
    r = _servir(_motor(tmp_path), ficha, datos, {**params, **umbral})
    assert r["estado"] == "RECHAZADO" and "umbrales fijos" in r["detalle"], r


def test_h14_los_parametros_de_metodo_siguen_siendo_de_la_peticion(tmp_path):
    datos, params = _caso("IDX-ERP-001")
    r = _servir(_motor(tmp_path), "IDX-ERP-001", datos, {**params, "lambda_reversion": 0.25})
    assert r["estado"] in ("SERVED", "SERVED_WITH_LIMITATIONS"), r


def test_h14_cada_ficha_mon_idx_declara_sus_umbrales():
    assert set(fichas_mon_idx.UMBRALES) == set(fichas_mon_idx.PARAMETROS_POR_DEFECTO)
    assert {"nodos_min", "meses_nodos"} <= fichas_mon_idx.UMBRALES["MON-EXP-001"]
    assert {"N_rango", "lambda_reversion_rango", "anios_historia_min"} <= fichas_mon_idx.UMBRALES["IDX-ERP-001"]


# ================================================================================================== H-15
@pytest.mark.parametrize("cambio", [{"datos": [5]}, {"datos": [{"valores": 5}]}, {"datos": [{"valores": [1, 2]}]},
                                    {"datos": "x"}, {"datos": [{"serie": 3}]}, {"parametros": "x"}, {"parametros": [1, 2]},
                                    {"plan": "PLAN_X"}, {"fecha_corte": "mañana"}, {"operacion": {"ficha_id": ["x"]}},
                                    {"operacion": 7}])
def test_h15_una_peticion_mal_formada_es_un_rechazo_en_rc(tmp_path, cambio):
    m = _motor(tmp_path)
    datos, params = _caso("IDX-CONC-001")
    pet = {"operacion": "IDX-CONC-001", "datos": datos, "parametros": params, "fecha_corte": "2026-11-12", **cambio}
    r = m.servir(pet, "AG-21")
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "DATOS_INCOHERENTES" and "mal formad" in r["detalle"], r
    assert m.almacen.leer("RC")[-1]["tipo_entrada"] == "RECHAZO"


def test_h15_una_peticion_que_no_es_un_objeto_se_rechaza(tmp_path):
    r = _motor(tmp_path).servir(["IDX-CONC-001"], "AG-21")
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "DATOS_INCOHERENTES"


# ================================================================================================== H-16 y H-18 (X04)
def test_h16_la_incertidumbre_de_cada_probabilidad_es_la_cota_entre_el_incremento():
    datos, params = _caso("MON-EXP-001")
    ent = {"valores": {k: v for d in datos for k, v in (d.get("valores") or {}).items()}, "series": {}, "series_rol": {}}
    r, _ = servicio.IMPLEMENTADAS["MON-EXP-001"]["fn"](ent, params)
    for s in r["senda"]:
        assert s["incertidumbre_probabilidad"] == pytest.approx(min(1.0, s["incertidumbre_redondeo_pb"] / 25), rel=1e-12)
        assert s["incertidumbre_redondeo_pb"] > 0   # X04: sin declarar la precisión, cuenta el medio último dígito


def test_h16_con_una_precision_grande_se_sirve_con_la_limitacion_que_lo_dice():
    datos, params = _caso("MON-EXP-001")
    v = {k: val for d in datos for k, val in (d.get("valores") or {}).items()}
    fn, tol = servicio.IMPLEMENTADAS["MON-EXP-001"]["fn"], servicio.IMPLEMENTADAS["MON-EXP-001"]["tol"]
    vistos = set()
    for prec in (1e-14, 1e-7, 1e-6, 1e-5, 5e-5):
        try:
            r, lim = fn({"valores": {**v, "precision_cotizacion": prec}, "series": {}, "series_rol": {}}, params)
        except ErrorFicha as e:
            assert "senda no identificada" in str(e)
            break
        hay = max(s["incertidumbre_probabilidad"] for s in r["senda"]) > tol
        assert any("puede mover las probabilidades" in x for x in lim) == hay
        vistos.add(hay)
    assert vistos == {True, False}   # el caso pasa por las dos ramas


# ================================================================================================== H-18 · Motor
def _catalogo_con(tmp_path, ficha, madurez):
    real = servicio.DIR_EJECUTOR.parent.joinpath(*servicio.RUTA_CATALOGO).read_text(encoding="utf-8")
    i, j = real.find("\n## 4."), real.find("\n## 5.")
    tabla = real[i:j].split("\n")
    fila = next(k for k, x in enumerate(tabla) if x.startswith(f"| {ficha} |"))
    celdas = tabla[fila].split("|")
    celdas[-2] = f" {madurez} "
    tabla[fila] = "|".join(celdas)
    destino = Path(tmp_path).joinpath(*servicio.RUTA_CATALOGO)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(real[:i] + "\n".join(tabla) + real[j:], encoding="utf-8")
    return Path(tmp_path)


def test_h18_s01_una_ficha_degradada_en_el_catalogo_deja_de_servirse(tmp_path):
    datos, params = _caso("IDX-CONC-001")
    raiz = _catalogo_con(tmp_path / "raiz", "IDX-CONC-001", "Documentado (degradada en la prueba)")
    assert servicio.madurez_catalogo(raiz)["IDX-CONC-001"].startswith("Documentado")
    r = _servir(_motor(tmp_path, raiz), "IDX-CONC-001", datos, params)
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "METODO_NO_IMPLEMENTADO" and "Documentado" in r["detalle"]
    assert _servir(_motor(tmp_path / "b"), "IDX-CONC-001", datos, params)["estado"].startswith("SERVED")


def test_h18_s06_las_documentadas_con_codigo_no_se_sirven_aunque_el_catalogo_diga_implementado(tmp_path, monkeypatch):
    f = "ST-DESC-001"   # T-112: el conjunto quedó vacío; se prueba con una ficha puesta a propósito
    monkeypatch.setattr(servicio, "DOCUMENTADAS_CON_CODIGO", frozenset({f}))
    raiz = _catalogo_con(tmp_path, f, "IMPLEMENTADO (prueba)")
    assert servicio.citable_segun_catalogo(f, raiz) and not servicio.servible(f, raiz)


def test_h18_s11_garch_sin_arch_lo_dice(tmp_path, monkeypatch):
    monkeypatch.setattr(servicio, "garch_disponible", lambda: False)
    raiz = _catalogo_con(tmp_path / "raiz", "VOL-GARCH-001", "IMPLEMENTADO (prueba)")
    r = _servir(_motor(tmp_path, raiz), "VOL-GARCH-001", [], {})
    assert r["estado"] == "RECHAZADO" and "`arch`" in r["detalle"]


@pytest.mark.parametrize("error", [ValueError("x"), TypeError("x"), KeyError("x"), IndexError("x"), AttributeError("x"),
                                   np.linalg.LinAlgError("x"), OverflowError("x")])
def test_h18_s07_cualquier_excepcion_habitual_de_una_ficha_es_un_rechazo(tmp_path, monkeypatch, error):
    f = "IDX-CONC-001"

    def revienta(ent, params):
        raise error
    monkeypatch.setitem(servicio.IMPLEMENTADAS, f, {**servicio.IMPLEMENTADAS[f], "fn": revienta})
    r = _servir(_motor(tmp_path), f, [{"valores": {"x": 1}}], {})
    assert r["estado"] == "RECHAZADO" and type(error).__name__ in r["detalle"]


def test_h18_s09_una_ficha_sin_casos_de_control_no_se_supera(tmp_path, monkeypatch):
    f = "IDX-CONC-001"
    monkeypatch.setitem(servicio.CASOS_CONTROL, f, [])
    assert not _motor(tmp_path).verificar_casos_control([f])[f]["superados"]


def test_h18_s10_un_manejador_no_determinista_no_supera_sus_casos(tmp_path, monkeypatch):
    f = "IDX-CONC-001"
    cuenta = iter(range(10 ** 6))
    orig = servicio.IMPLEMENTADAS[f]["fn"]

    def cambia(ent, params):
        r, lim = orig(ent, params)
        return {**r, "ruido": float(next(cuenta))}, lim
    monkeypatch.setitem(servicio.IMPLEMENTADAS, f, {**servicio.IMPLEMENTADAS[f], "fn": cambia})
    monkeypatch.setitem(servicio.CASOS_CONTROL, f, [dict(c, comprobar=lambda r: True) for c in servicio.CASOS_CONTROL[f]])
    assert not _motor(tmp_path).verificar_casos_control([f])[f]["superados"]


def test_h18_x11_la_envoltura_mon_idx_rechaza_un_resultado_no_finito():
    envuelta = fichas_mon_idx._cerrado("IDX-REL-001")(lambda ent, params: ({"x": float("nan"), "y": [1.0, float("inf")]}, []))
    with pytest.raises(ErrorFicha, match="no finito"):
        envuelta({"valores": {}}, {})


# ================================================================================================== H-18 · FON-DISC y FON-FLOW
def test_h18_fon_disc_mediana_z_normalizacion_y_vida_media():
    """Y01 (media en vez de mediana) e Y02 (vida media con meses de 30 días): ficha FON-DISC-001 del Catálogo."""
    rng = np.random.default_rng(20261113)
    fechas = pd.date_range("2021-11-05", periods=4 * 52 + 1, freq="7D")
    n = len(fechas)
    miembros, d_ = {}, []
    for i in range(6):
        nav = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))
        dsc = -0.08 + 0.03 * np.sin(np.arange(n) / 15 + i) + rng.normal(0, 0.005, n) + (0.05 if i == 0 else 0.0)   # asimétrico
        miembros[f"F{i}"] = {"precio": (nav * (1 + dsc)).tolist(), "nav": nav.tolist(), "fecha_nav": str(fechas[-1].date())}
        d_.append(dsc * nav / nav)
    v = {"fechas": [str(x.date()) for x in fechas], "miembros": miembros, "rentabilidad_nav_supuesta": 0.04,
         "catalizadores": ["recompras"]}
    r, _ = servicio.IMPLEMENTADAS["FON-DISC-001"]["fn"]({"valores": v, "series": {}, "series_rol": {}}, {"kappa": 0.3})
    d_ = np.vstack([np.array(m["precio"]) / np.array(m["nav"]) - 1 for m in miembros.values()])
    agg = np.median(d_, axis=0)
    assert not np.isclose(np.mean(d_[:, -1]), agg[-1], rtol=0, atol=1e-6)   # el caso distingue media y mediana
    d = agg[-1]
    h = agg[fechas > fechas[-1] - pd.Timedelta(weeks=52)]
    assert r["descuento_agregado_pct"] == pytest.approx(d * 100, abs=1e-12)
    assert r["z_scores"]["ventana_media"] == pytest.approx((d - h.mean()) / h.std(ddof=1), abs=1e-9)
    rn = ((1 + d + 0.3 * (h.mean() - d)) / (1 + d) - 1) * 100
    assert r["rentabilidad_normalizacion_pct"] == pytest.approx(rn, abs=1e-10)
    phi = np.polyfit(agg[:-1], agg[1:], 1)[0]
    assert r["phi_ar1"] == pytest.approx(phi, abs=1e-9)
    assert r["vida_media_meses"] == pytest.approx(math.log(0.5) / math.log(phi) * 7 * 12 / 365, abs=1e-7)


def _acf(x, k):
    x = np.asarray(x, dtype=float) - np.mean(x)
    return float(np.sum(x[k:] * x[:-k]) / np.sum(x * x))


def test_h18_fon_flow_flujos_acumulados_z_y_autocorrelaciones():
    """Y04 (acumulado frente al AUM del último periodo), Y05 (z frente a 72 meses) e Y06 (otra autocorrelación)."""
    rng = np.random.default_rng(20261113)
    fm = pd.date_range("2021-10-31", periods=49, freq="ME")
    cats, fl, ap = {}, {}, {}
    for c in ("acciones", "bonos", "mixtos"):
        aum = [1000.0 * (1 + rng.random())]
        rent = rng.normal(0.005, 0.02, len(fm) - 1)
        flu = rng.normal(5, 20, len(fm) - 1)
        for k in range(len(fm) - 1):
            aum.append(aum[-1] * (1 + rent[k]) + flu[k])
        aum = np.array(aum)
        cats[c] = {"aum": aum.tolist(), "rentabilidad": rent.tolist(), "gestion": "indexada" if c != "mixtos" else "activa"}
        fl[c], ap[c] = aum[1:] - aum[:-1] * (1 + rent), aum[:-1]
    v = {"taxonomia": "pruebas", "frecuencia": "mensual", "fechas": [str(x.date()) for x in fm], "categorias": cats}
    r, _ = servicio.IMPLEMENTADAS["FON-FLOW-001"]["fn"]({"valores": v, "series": {}, "series_rol": {}}, {})
    for c in cats:
        t, rel = r["categorias"][c], fl[c] / ap[c]
        assert t["flujo_ultimo"] == pytest.approx(fl[c][-1], abs=1e-8)
        assert t["flujo_relativo_ultimo_pct"] == pytest.approx(rel[-1] * 100, abs=1e-10)
        h = rel[-36:]
        assert t["z_score"] == pytest.approx((rel[-1] - h.mean()) / h.std(ddof=1), abs=1e-9)
        assert all(t["autocorrelaciones"][str(k)] == pytest.approx(_acf(rel, k), abs=1e-10) for k in (1, 2, 3))
        for meses in (3, 12):
            assert t["acumulados"][str(meses)]["moneda"] == pytest.approx(fl[c][-meses:].sum(), abs=1e-8)
            assert t["acumulados"][str(meses)]["pct_aum"] == pytest.approx(fl[c][-meses:].sum() / ap[c][-meses] * 100, abs=1e-10)
    assert np.allclose(r["flujo_total"], sum(fl.values()), atol=1e-8)


# ================================================================================================== H-20
@pytest.mark.parametrize("nivel,servido", [(0.5, False), (0.999, False), (0.90, True), (0.99, True)])
def test_h20_der_vrp_admite_solo_el_rango_de_nivel_de_risk_var(tmp_path, nivel, servido):
    datos, params = _caso("DER-VRP-001")
    r = _servir(_motor(tmp_path), "DER-VRP-001", datos, {**params, "nivel_es": nivel})
    assert r["estado"].startswith("SERVED") == servido, r
    if not servido:
        assert "nivel_es" in r["detalle"] and "fuera del rango" in r["detalle"]
