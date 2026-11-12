"""T-106 · Motor Fase 1: fichas MON (MON-YLD/EXP/REAL/FIX-001) e IDX (IDX-ERP/CONC/REL/REB-001) del Catálogo V5.0.

Casos de control de «Verificación», reglas de «Aclaración y rechazo», determinismo, claves de «Salidas» y valores
calculados a mano con datos sintéticos.
"""
import copy
import json
import math
from itertools import pairwise

import numpy as np
import pandas as pd
import pytest

from bloque_a.motor import fichas_mon_idx as fm
from bloque_a.motor.operaciones import ErrorFicha


def _ejecutar(ficha, valores, params=None, series=None, series_rol=None):
    ent = {"valores": valores, "series": series or {}, "series_rol": series_rol or {}}
    return fm.FICHAS[ficha]["fn"](ent, params or {})


def _valores_caso(caso):
    v = {}
    for d in caso["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    return v


def _primer_caso(ficha):
    caso = fm.CASOS_CONTROL[ficha][0]
    return _valores_caso(caso), dict(caso["parametros"])


CASOS = [(f, c) for f, cs in fm.CASOS_CONTROL.items() for c in cs]


# ------------------------------------------------------------------ registro e interfaz
def test_registro_completo_y_metadatos_de_ficha():
    esperado = {"MON-YLD-001": ("MC-01", "DETERMINISTA", 1e-10), "MON-EXP-001": ("MC-09", "DETERMINISTA", 1e-10),
                "MON-REAL-001": ("MC-01", "DETERMINISTA", 1e-10), "MON-FIX-001": ("MC-09", "DETERMINISTA", 1e-10),
                "IDX-ERP-001": ("MC-09", "DETERMINISTA", 1e-10), "IDX-CONC-001": ("MC-01", "DETERMINISTA", 1e-10),
                "IDX-REL-001": ("MC-09", "ESTADISTICA", 1e-8), "IDX-REB-001": ("MC-03", "ESTADISTICA", 1e-8)}
    assert set(fm.FICHAS) == set(esperado) == set(fm.CASOS_CONTROL) == set(fm.PARAMETROS_POR_DEFECTO)
    for ficha, (modulo, cifra, tol) in esperado.items():
        meta = fm.FICHAS[ficha]
        assert (meta["modulo"], meta["cifra"], meta["tol"], meta["version"]) == (modulo, cifra, tol, "1.0")
        assert meta["ri"].startswith("RI-") and callable(meta["fn"])


def test_parametros_por_defecto_segun_ficha():
    p = fm.PARAMETROS_POR_DEFECTO
    assert p["MON-YLD-001"]["base_salida"] == "TAE" and p["MON-YLD-001"]["plazos_meses"] == [1, 3, 6, 12]
    assert p["MON-YLD-001"]["cobertura"] is False
    assert p["MON-EXP-001"]["incremento_pb"] == 25 and p["MON-EXP-001"]["diferencial_estable_dias"] == 20
    assert p["MON-REAL-001"]["plazo_meses"] == 3 and p["MON-REAL-001"]["expectativa"] == "swap_1a"
    assert (p["MON-FIX-001"]["T_meses"], p["MON-FIX-001"]["tau_meses"]) == (12, 3)
    assert sorted(p["MON-FIX-001"]["escenarios_pb"]) == [-100, -50, 0, 50, 100]
    assert (p["IDX-ERP-001"]["N"], p["IDX-ERP-001"]["lambda_reversion"], p["IDX-ERP-001"]["multiplo"]) == (10, 0.5, "CAPE")
    assert (p["IDX-CONC-001"]["top_n"], p["IDX-CONC-001"]["media_amplitud"]) == (10, 200)
    assert p["IDX-REL-001"]["divisa_comun"] == "EUR" and p["IDX-REL-001"]["ventana_anios"] == 20
    assert (p["IDX-REB-001"]["sesiones_estimacion"], p["IDX-REB-001"]["eventos_min"]) == (250, 20)


@pytest.mark.parametrize("ficha,caso", CASOS, ids=[f"{f}:{c['nombre']}" for f, c in CASOS])
def test_casos_de_control(ficha, caso):
    res, lim = _ejecutar(ficha, _valores_caso(caso), dict(caso["parametros"]))
    assert caso["comprobar"](res), caso["nombre"]
    assert isinstance(lim, list) and all(isinstance(x, str) for x in lim)
    json.dumps(res, allow_nan=False)   # JSON-serializable y sin NaN


def test_cada_ficha_tiene_un_caso_por_frase_de_verificacion():
    minimos = {"MON-YLD-001": 2, "MON-EXP-001": 2, "MON-REAL-001": 2, "MON-FIX-001": 2, "IDX-ERP-001": 2,
               "IDX-CONC-001": 2, "IDX-REL-001": 2, "IDX-REB-001": 2}
    for ficha, n in minimos.items():
        assert len(fm.CASOS_CONTROL[ficha]) >= n


@pytest.mark.parametrize("ficha", sorted(fm.FICHAS))
def test_determinismo(ficha):
    v, p = _primer_caso(ficha)
    r1, l1 = _ejecutar(ficha, copy.deepcopy(v), dict(p))
    r2, l2 = _ejecutar(ficha, copy.deepcopy(v), dict(p))
    assert json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True) and l1 == l2


@pytest.mark.parametrize("ficha", sorted(fm.FICHAS))
def test_entrada_vacia_falla_cerrado(ficha):
    with pytest.raises(ErrorFicha):
        _ejecutar(ficha, {})


SALIDAS = {
    "MON-YLD-001": ["rendimiento_equivalente", "diferenciales_pb", "rendimiento_cubierto", "percentiles"],
    "MON-EXP-001": ["senda", "probabilidades", "cambio_acumulado_pb", "sorpresas_pb"],
    "MON-REAL-001": ["real_ex_ante", "real_ex_post", "diferencial_neutral", "percentiles"],
    "MON-FIX-001": ["fijar", "renovar", "punto_muerto", "holgura_pb", "prima_implicita_pb"],
    "IDX-ERP-001": ["bloques", "er_nominal", "er_real", "prima_rf", "rango_escenarios", "diferencias_entre_indices"],
    "IDX-CONC-001": ["peso_top_n", "hhi", "n_ef", "hhi_sectorial", "amplitud", "diferencial_ponderado_equiponderado",
                     "contribucion", "percentiles"],
    "IDX-REL-001": ["brechas", "z_scores", "percentiles", "brecha_neutral_sectorial", "diferencia_er",
                    "momentum_relativo", "diferencial_revisiones"],
    "IDX-REB-001": ["demanda_estimada", "estudio_eventos", "n_eventos"],
}


@pytest.mark.parametrize("ficha", sorted(SALIDAS))
def test_claves_de_salidas(ficha):
    v, p = _primer_caso(ficha)
    res, _ = _ejecutar(ficha, v, p)
    faltan = [k for k in SALIDAS[ficha] if k not in res]
    assert not faltan
    assert "referencia_ingenua" in res and "unidades" in res


# ------------------------------------------------------------------ MON-YLD-001
def _seg(nombre, conv, valor, plazo=3, dias=91, divisa="EUR", fecha="2026-11-10"):
    return {"segmento": nombre, "convencion": conv, "valor": valor, "plazo_meses": plazo, "dias": dias,
            "divisa": divisa, "fecha": fecha}


def test_mon_yld_valores_a_mano():
    res, _ = _ejecutar("MON-YLD-001", {"segmentos": [_seg("letras", "descuento_360", 0.03, dias=90),
                                                     _seg("pagares", "simple_360", 0.032, dias=90)]})
    letras = res["tabla"]["letras · EUR · 3m"]
    precio = 1 - 0.03 * 90 / 360
    assert letras["precio"] == pytest.approx(precio, rel=1e-12)
    assert letras["simple_365"] == pytest.approx((1 / precio - 1) * 365 / 90, rel=1e-12)
    assert letras["tae"] == pytest.approx((1 / precio) ** (365 / 90) - 1, rel=1e-12)
    assert letras["simple_360"] == pytest.approx(letras["simple_365"] * 360 / 365, rel=1e-12)
    tae_pag = (1 + 0.032 * 90 / 360) ** (365 / 90) - 1
    assert res["diferenciales_pb"]["letras − pagares · EUR · 3m"] == pytest.approx(
        (letras["tae"] - tae_pag) * 10_000, rel=1e-10)


def test_mon_yld_base_act365_y_percentil():
    hist = [{"fecha": f"{2015 + i // 4}-{1 + 3 * (i % 4):02d}-15", "valor_pb": float(i % 7)} for i in range(40)]
    v = {"segmentos": [_seg("a", "simple_365", 0.03), _seg("b", "simple_365", 0.0301)],
         "historia_diferenciales": {"a − b · EUR · 3m": hist}}
    res, _ = _ejecutar("MON-YLD-001", v, {"base_salida": "Act/365"})
    assert res["rendimiento_equivalente"]["a · EUR · 3m"] == pytest.approx(0.03, rel=1e-12)
    dif = res["diferenciales_pb"]["a − b · EUR · 3m"]
    assert dif == pytest.approx(-1.0, rel=1e-9)
    pos = res["percentiles"]["a − b · EUR · 3m"]
    assert pos["percentil"] == 0.0 and pos["n"] == 40


def test_mon_yld_cobertura():
    v = {"segmentos": [_seg("letras_usd", "simple_360", 0.04, dias=91, divisa="USD"),
                       _seg("letras", "simple_360", 0.02, dias=91)],
         "cobertura": {"divisa_destino": "EUR", "segmentos": {"letras_usd · USD · 3m": {"spot": 1.10, "forward": 1.105}}}}
    res, _ = _ejecutar("MON-YLD-001", v, {"cobertura": True})
    bruto = (1 + 0.04 * 91 / 360) * (1.10 / 1.105)
    cub = res["rendimiento_cubierto"]["letras_usd · USD · 3m"]
    assert cub["rendimiento_periodo"] == pytest.approx(bruto - 1, rel=1e-12)
    assert cub["tae"] == pytest.approx(bruto ** (365 / 91) - 1, rel=1e-12)


@pytest.mark.parametrize("mutar,motivo", [
    (lambda v: v["segmentos"][0].pop("convencion"), "convención"),
    (lambda v: v.update(pares=[["letras", "pagares"]]) or v["segmentos"][1].update(plazo_meses=6, dias=182),
     "no son alineables"),
    (lambda v: v["segmentos"][0].update(divisa="USD") or v.update(pares=[["letras", "pagares"]]), "no son alineables"),
    (lambda v: v["segmentos"][0].pop("fecha"), "fecha"),
    (lambda v: v["segmentos"][0].update(convencion="rara"), "convención desconocida"),
])
def test_mon_yld_rechazos(mutar, motivo):
    v = {"segmentos": [_seg("letras", "descuento_360", 0.03), _seg("pagares", "simple_360", 0.032)]}
    mutar(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _ejecutar("MON-YLD-001", v)


def test_mon_yld_cobertura_sin_forward_se_rechaza():
    v = {"segmentos": [_seg("letras_usd", "simple_360", 0.04, divisa="USD")],
         "cobertura": {"divisa_destino": "EUR", "segmentos": {}}}
    with pytest.raises(ErrorFicha, match="spot y forward"):
        _ejecutar("MON-YLD-001", v, {"cobertura": True})


# ------------------------------------------------------------------ MON-EXP-001
def _curva_escalonada(r0, r1, d_reunion, dias, base=360):
    """Curva OIS coherente con un tipo a un día r0 hasta la reunión y r1 después."""
    out = []
    for d in dias:
        lg = min(d, d_reunion) * math.log1p(r0 / base) + max(0, d - d_reunion) * math.log1p(r1 / base)
        out.append({"dias": d, "tipo": math.expm1(lg) * base / d})
    return out


@pytest.mark.parametrize("r1,mov,probs", [(0.0167, -1.0, {"1": 1.0, "2": 0.0}),
                                          (0.0192 - 0.00125, -0.5, {"0": 0.5, "1": 0.5})])
def test_mon_exp_senda_y_probabilidad_a_mano(r1, mov, probs):
    fecha = pd.Timestamp("2026-11-12")
    d_r = (pd.Timestamp("2026-12-17") - fecha).days
    v = {"fecha": "2026-11-12", "base_curva": 360, "tipo_oficial": 0.02, "diferencial_estable": 0.0008,
         "curva": _curva_escalonada(0.0192, r1, d_r, [30, 90, 180, 365]), "reuniones": ["2026-12-17"],
         "decisiones": [{"fecha": "2026-10-30", "tipo_decidido": 0.02, "tipo_esperado": 0.0205}]}
    res, _ = _ejecutar("MON-EXP-001", v)
    s = res["senda"][0]
    assert s["tipo_mercado_implicito"] == pytest.approx(r1, abs=1e-13)
    assert s["tipo_oficial_implicito"] == pytest.approx(r1 + 0.0008, abs=1e-13)
    assert s["movimientos_en_reunion"] == pytest.approx(mov, abs=1e-9)
    assert s["probabilidades"]["sentido"] == "bajada"
    for k, p in probs.items():
        assert s["probabilidades"]["movimientos"][k] == pytest.approx(p, abs=1e-9)
    assert res["cambio_acumulado_pb"]["6m"] == pytest.approx((r1 - 0.0192) * 1e4, abs=1e-8)
    assert res["sorpresas_pb"][0]["sorpresa_pb"] == pytest.approx(-5.0, abs=1e-9)
    assert res["verificacion"]["error_reproduccion_nodos_max"] < 1e-12
    # Los nodos sin reunión nueva se comparan con la senda: aquí coinciden.
    assert all(abs(n["tipo_nodo"] - n["tipo_senda"]) < 1e-12 for n in res["verificacion"]["nodos_redundantes"])


def test_mon_exp_diferencial_como_media_de_20_dias_y_futuros():
    fecha = pd.Timestamp("2026-11-12")
    hist = [0.0005] * 5 + [0.0008] * 20
    futs, ini = [], fecha
    for k in range(4):
        fin = ini + pd.DateOffset(months=3)
        futs.append({"inicio": ini.date().isoformat(), "fin": fin.date().isoformat(), "precio": 100 - 1.92})
        ini = fin
    v = {"fecha": "2026-11-12", "base_curva": 360, "tipo_oficial": 0.02, "historia_diferencial": hist,
         "futuros": futs, "reuniones": ["2027-02-12"]}
    res, _ = _ejecutar("MON-EXP-001", v)
    assert res["diferencial_estable"] == pytest.approx(0.0008, abs=1e-15)
    assert res["verificacion"]["error_reproduccion_nodos_max"] < 1e-12


@pytest.mark.parametrize("mutar,motivo", [
    (lambda v: v.pop("reuniones"), "calendario de reuniones"),
    (lambda v: v.update(curva=v["curva"][:2] + [{"dias": 400, "tipo": 0.016}]), "menos de 3 nodos"),
    (lambda v: v.pop("diferencial_estable"), "diferencial habitual"),
    (lambda v: v.update(historia_diferencial=[0.0008] * 19) or v.pop("diferencial_estable"), "< 20"),
    (lambda v: v.update(reuniones=["2030-01-01"]), "ninguna reunión"),
    (lambda v: v.pop("base_curva"), "base_curva"),
])
def test_mon_exp_rechazos(mutar, motivo):
    v = fm._datos_mon_exp(plana=False)
    mutar(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _ejecutar("MON-EXP-001", v)


def test_mon_exp_futuros_largos_sin_convexidad_se_truncan():
    fecha = pd.Timestamp("2026-11-12")
    futs, ini = [], fecha
    for _ in range(6):
        fin = ini + pd.DateOffset(months=3)
        futs.append({"inicio": ini.date().isoformat(), "fin": fin.date().isoformat(), "precio": 98.1})
        ini = fin
    v = {"fecha": "2026-11-12", "base_curva": 360, "tipo_oficial": 0.02, "diferencial_estable": 0.0008,
         "futuros": futs, "reuniones": ["2027-02-12", "2027-06-12"]}
    _, lim = _ejecutar("MON-EXP-001", v)
    assert any("convexidad" in x for x in lim)


# ------------------------------------------------------------------ MON-REAL-001
def test_mon_real_valores_a_mano():
    v = fm._datos_mon_real(pi_cero=False)
    v["divisas"]["EUR"].update(tipo_nominal=0.03, expectativa_inflacion={"valor": 0.02, "fuente": "s", "tipo": "swap_1a"},
                               tipo_real_neutral={"valor": 0.0, "fuente": "s"})
    v["divisas"]["USD"] = copy.deepcopy(v["divisas"]["EUR"])
    v["divisas"]["USD"]["tipo_nominal"] = 0.045
    res, _ = _ejecutar("MON-REAL-001", v)
    assert res["real_ex_ante"]["EUR"] == pytest.approx(1.03 / 1.02 - 1, rel=1e-12)
    assert res["diferencial_neutral"]["EUR"] == pytest.approx(1.03 / 1.02 - 1, rel=1e-12)
    assert res["diferencias_entre_divisas"]["EUR − USD"]["ex_ante"] == pytest.approx(1.03 / 1.02 - 1.045 / 1.02,
                                                                                    rel=1e-12)
    h0 = v["divisas"]["EUR"]["historia"][0]
    p0 = res["tabla"]["EUR"]["serie_ex_post"][0]
    dias = (pd.Timestamp(h0["fecha_fin"]) - pd.Timestamp(h0["fecha_inicio"])).days
    esperado = (1 + h0["tipo_nominal"] * dias / 360) / (h0["ipc_fin"] / h0["ipc_inicio"]) - 1
    assert p0["real_periodo"] == pytest.approx(esperado, rel=1e-12)


@pytest.mark.parametrize("mutar,motivo", [
    (lambda d: d["expectativa_inflacion"].pop("fuente"), "sin fuente"),
    (lambda d: d.pop("fuente_ipc"), "IPC sin fuente"),
    (lambda d: d["historia"][3].update(vintage_inicio="2020-01-01"), "vintages incompatibles"),
    (lambda d: d["historia"][-1].update(vintage_inicio="2025-01-01", vintage_fin="2025-01-01"), "anterior al fin"),
    (lambda d: d.update(historia=d["historia"][:30]), "< 10"),
    (lambda d: d["expectativa_inflacion"].update(tipo="encuesta"), "expectativa"),
    (lambda d: d["historia"].pop(5), "no contiguas"),
    (lambda d: d.update(tipo_real_neutral={"valor": 0.005}), "sin fuente"),
])
def test_mon_real_rechazos(mutar, motivo):
    v = fm._datos_mon_real(pi_cero=False)
    mutar(v["divisas"]["EUR"])
    with pytest.raises(ErrorFicha, match=motivo):
        _ejecutar("MON-REAL-001", v)


# ------------------------------------------------------------------ MON-FIX-001
def test_mon_fix_valores_a_mano_y_escenarios():
    v = fm._datos_mon_fix(plana=False)
    v["senda_encuesta"] = [0.02, 0.019, 0.018, 0.017]
    v["senda_mon_exp"] = [0.0200, 0.0190, 0.0177, 0.0160]
    v["pesos_escenarios"] = {"base": 0.5, "+50pb": 0.25, "-50pb": 0.25}
    res, _ = _ejecutar("MON-FIX-001", v)
    d_t = (pd.Timestamp("2027-11-12") - pd.Timestamp("2026-11-12")).days
    g = 1 + 0.0181 * d_t / 360
    assert res["fijar"]["tae"] == pytest.approx(g ** (365 / d_t) - 1, rel=1e-12)
    assert res["fijar"]["tipo_simple"] == pytest.approx(0.0181, rel=1e-12)
    # Primer forward = tipo a 3 meses; ±50 pb suben y bajan la renovación.
    assert res["forwards"][0] == pytest.approx(0.0200, rel=1e-12)
    assert res["renovar"]["+50pb"]["tae"] > res["renovar"]["base"]["tae"] > res["renovar"]["-50pb"]["tae"]
    # Punto muerto: tipo constante que iguala fijar y renovar.
    pm = res["punto_muerto"]
    cortes = [(pd.Timestamp("2026-11-12") + pd.DateOffset(months=3 * k) - pd.Timestamp("2026-11-12")).days
              for k in range(5)]
    bruto = np.prod([1 + pm * (b - a) / 360 for a, b in pairwise(cortes)])
    assert bruto == pytest.approx(g, rel=1e-12)
    assert res["prima_implicita_pb"] == pytest.approx((pm - np.mean(v["senda_encuesta"])) * 1e4, rel=1e-10)
    assert res["holgura_senda_descontada_pb"] == res["holgura_pb"]["mon_exp"]
    assert res["holgura_pb"]["base"] == pytest.approx(0.0, abs=1e-8)
    media = sum(w * res["renovar"][k]["tae"] for k, w in v["pesos_escenarios"].items())
    assert res["media_ponderada_renovar_tae"] == pytest.approx(media, rel=1e-12)


@pytest.mark.parametrize("mutar,params,motivo", [
    (lambda v: v["curva"][1].update(base=365), {}, "convenciones incompatibles"),
    (lambda v: None, {"T_meses": 10}, "múltiplo"),
    (lambda v: None, {"T_meses": 36}, "fuera del rango"),
    (lambda v: None, {"tau_meses": 12}, "fuera del rango"),
    (lambda v: v.update(curva=v["curva"][:2] + v["curva"][3:]) or v["curva"].pop(0), {}, "menos de 3 nodos"),
    (lambda v: v.update(curva=v["curva"][:3]), {}, "no llega"),
    (lambda v: v.update(pesos_escenarios={"base": 0.6, "plana": 0.3}), {}, "sumar 1"),
    (lambda v: v.update(senda_encuesta=[0.02, 0.02]), {}, "se esperan 4"),
])
def test_mon_fix_rechazos(mutar, params, motivo):
    v = fm._datos_mon_fix(plana=False)
    v["curva"].append({"plazo_meses": 24, "tipo": 0.017, "base": 360}) if motivo == "fuera del rango" else None
    mutar(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _ejecutar("MON-FIX-001", v, params)


def test_mon_fix_interpola_nodo_ausente_y_lo_declara():
    v = fm._datos_mon_fix(plana=False)
    v["curva"] = [n for n in v["curva"] if n["plazo_meses"] != 9]
    v["curva"].append({"plazo_meses": 1, "tipo": 0.0202, "base": 360})
    res, lim = _ejecutar("MON-FIX-001", v)
    assert any("interpolados" in x for x in lim)
    assert abs(res["verificacion"]["renovar_forwards_menos_fijar_pb"]) < 1e-6


# ------------------------------------------------------------------ IDX-ERP-001
def test_idx_erp_valores_a_mano():
    v = fm._datos_idx_erp(gordon=False)
    v["historia_multiplo"] = [{"fecha": f["fecha"], "valor": 20.0} for f in v["historia_multiplo"]]
    res, _ = _ejecutar("IDX-ERP-001", v)
    fila = res["indices"]["IDX-SINT"]
    assert fila["multiplo_objetivo"] == pytest.approx(24.0, rel=1e-12)
    dval = (24 / 28) ** 0.1 - 1
    er = 0.03 + 0.01 + 0.015 + 0.02 + dval
    assert res["bloques"]["IDX-SINT"]["cambio_valoracion"] == pytest.approx(dval, rel=1e-12)
    assert res["er_nominal"]["IDX-SINT"] == pytest.approx(er, rel=1e-12)
    assert res["er_real"]["IDX-SINT"] == pytest.approx(er - 0.02, rel=1e-12)
    assert res["prima_rf"]["IDX-SINT"] == pytest.approx(er - 0.027, rel=1e-12)
    assert res["rango_escenarios"]["IDX-SINT"]["min"] == pytest.approx(er - 0.01, rel=1e-12)
    assert res["rango_escenarios"]["IDX-SINT"]["max"] == pytest.approx(er + 0.01, rel=1e-12)
    assert fila["segunda_via_rendimiento_beneficio"] == pytest.approx(1 / 28, rel=1e-12)
    assert fila["percentil_multiplo"]["z"] is None   # historia constante: z indefinido


def test_idx_erp_crecimiento_historico_por_cagr_y_comparacion_entre_indices():
    a = fm._datos_idx_erp(gordon=True)
    fechas = pd.date_range("2000-01-31", periods=25 * 12 + 1, freq="ME")
    a.pop("crecimiento_real_bpa")
    a["historia_bpa_real"] = [{"fecha": f.date().isoformat(), "valor": 100 * 1.02 ** (i / 12)}
                              for i, f in enumerate(fechas)]
    b = copy.deepcopy(fm._datos_idx_erp(gordon=True))
    b.update(nombre="IDX-USD", divisa="USD", rf={"valor": 0.04, "plazo_anios": 10, "divisa": "USD"},
             supuesto_fx={"valor": -0.01, "fuente": "s"})
    v = {"indices": [a, b], "divisa_comparacion": "EUR", "rf_comparacion": {"valor": 0.027, "plazo_anios": 10,
                                                                             "divisa": "EUR"}}
    res, lim = _ejecutar("IDX-ERP-001", v, {"cobertura": "ambas"})
    anios = (fechas[-1] - fechas[0]).days / 365
    g = (1.02 ** (300 / 12)) ** (1 / anios) - 1
    assert res["bloques"]["IDX-SINT"]["crecimiento_real_bpa"] == pytest.approx(g, rel=1e-10)
    comp = res["diferencias_entre_indices"]["er_divisa_comun"]
    er_b = res["er_nominal"]["IDX-USD"]
    assert comp["IDX-USD"]["cubierta"] == pytest.approx(er_b + 0.027 - 0.04, rel=1e-12)
    assert comp["IDX-USD"]["no_cubierta"] == pytest.approx((1 + er_b) * 0.99 - 1, rel=1e-12)
    assert any("composición sectorial" in x for x in lim)


@pytest.mark.parametrize("mutar,params,motivo", [
    (lambda v: v.update(historia_multiplo=v["historia_multiplo"][:100]), {}, "< 10"),
    (lambda v: v.pop("rf"), {}, "rf"),
    (lambda v: v["rf"].update(divisa="USD"), {}, "r_f en USD"),
    (lambda v: v["rf"].update(plazo_anios=5), {}, "N = 10"),
    (lambda v: v["inflacion_esperada"].pop("fuente"), {}, "sin fuente"),
    (lambda v: None, {"N": 20}, "fuera del rango"),
    (lambda v: None, {"lambda_reversion": 1.5}, "fuera del rango"),
    (lambda v: v.update(tipo_multiplo="PER_adelantado"), {}, "distinto del pedido"),
])
def test_idx_erp_rechazos(mutar, params, motivo):
    v = fm._datos_idx_erp(gordon=False)
    mutar(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _ejecutar("IDX-ERP-001", v, params)


def test_idx_erp_varios_indices_sin_divisa_de_comparacion_pide_aclaracion():
    a, b = fm._datos_idx_erp(gordon=False), fm._datos_idx_erp(gordon=False)
    b["nombre"] = "OTRO"
    with pytest.raises(ErrorFicha, match="divisa de comparación"):
        _ejecutar("IDX-ERP-001", {"indices": [a, b]})


# ------------------------------------------------------------------ IDX-CONC-001
def test_idx_conc_valores_a_mano():
    comp = {"fecha": "2026-10-31", "componentes": [{"id": "X", "peso": 0.5, "sector": "A"},
                                                   {"id": "Y", "peso": 0.3, "sector": "A"},
                                                   {"id": "Z", "peso": 0.2, "sector": "B"}]}
    ini = {"fecha": "2025-10-31", "componentes": [{"id": "X", "peso": 0.4}, {"id": "Y", "peso": 0.4},
                                                  {"id": "Z", "peso": 0.2}]}
    fechas = pd.bdate_range("2025-06-02", periods=320)
    sube = pd.Series(np.linspace(100, 150, 320), index=fechas)
    baja = pd.Series(np.linspace(150, 100, 320), index=fechas)
    pond = [{"fecha": f.date().isoformat(), "valor": 100 * 1.001 ** i} for i, f in enumerate(fechas)]
    equi = [{"fecha": f.date().isoformat(), "valor": 100.0} for f in fechas]
    v = {"composicion": comp, "composicion_inicio": ini, "rentabilidades_periodo": {"X": 0.2, "Y": -0.1, "Z": 0.05},
         "indice_ponderado": pond, "indice_equiponderado": equi}
    res, lim = _ejecutar("IDX-CONC-001", v, {"top_n": 5}, series={"X": sube, "Y": sube, "Z": baja})
    assert res["hhi"] == pytest.approx(0.38, rel=1e-12)
    assert res["n_ef"] == pytest.approx(1 / 0.38, rel=1e-12)
    assert res["hhi_sectorial"] == pytest.approx(0.68, rel=1e-12)
    assert res["peso_top_n"] == pytest.approx(1.0, rel=1e-12)
    assert res["amplitud"]["porcentaje_sobre_media"] == pytest.approx(2 / 3, rel=1e-12)
    assert res["amplitud"]["linea_avance_retroceso"] == pytest.approx(319.0)
    total = 0.4 * 0.2 + 0.4 * -0.1 + 0.2 * 0.05
    assert res["contribucion"]["rentabilidad_indice"] == pytest.approx(total, rel=1e-12)
    assert res["contribucion"]["porcentaje_top_n"] == pytest.approx(1.0, rel=1e-12)
    assert res["segunda_via"]["hhi_pesos_medios"] == pytest.approx(0.45 ** 2 + 0.35 ** 2 + 0.2 ** 2, rel=1e-12)
    ultimo = fechas[-1]
    ref = pd.Series([f["valor"] for f in pond], index=fechas)
    r3 = ref.iloc[-1] / ref[ref.index <= ultimo - pd.DateOffset(months=3)].iloc[-1] - 1
    assert res["diferencial_ponderado_equiponderado"]["3m"] == pytest.approx(r3, rel=1e-12)
    assert any("< top_n" in x for x in lim)


def test_idx_conc_percentiles_con_historia():
    fechas = pd.date_range("2010-01-31", "2026-09-30", freq="ME")
    hist = [{"fecha": f.date().isoformat(), "peso_top_n": 0.2 + 0.001 * i, "hhi": 0.01 + 0.0001 * i,
             "n_ef": 100 - 0.1 * i, "hhi_sectorial": 0.15} for i, f in enumerate(fechas)]
    v = {"composicion": fm._composicion(30, igual=False), "historia_metricas": hist}
    res, _ = _ejecutar("IDX-CONC-001", v)
    assert set(res["percentiles"]) == {"peso_top_n", "hhi", "n_ef", "hhi_sectorial"}
    assert res["percentiles"]["hhi_sectorial"]["z"] is None
    assert 0.0 <= res["percentiles"]["hhi"]["percentil"] <= 1.0


@pytest.mark.parametrize("mutar,motivo", [
    (lambda v: v["composicion"].pop("fecha"), "sin fecha"),
    (lambda v: v.pop("composicion"), "sin composición fechada"),
    (lambda v: v["composicion"]["componentes"][0].update(peso=0.5), "no 1"),
    (lambda v: v["composicion"]["componentes"][0].update(peso=-0.01), "negativo"),
    (lambda v: v.update(historia_metricas=[{"fecha": "2024-01-31", "peso_top_n": 0.3, "hhi": 0.02, "n_ef": 50},
                                           {"fecha": "2025-01-31", "peso_top_n": 0.3, "hhi": 0.02, "n_ef": 50}]),
     "< 10 años"),
])
def test_idx_conc_rechazos(mutar, motivo):
    v = {"composicion": fm._composicion(20, igual=True)}
    mutar(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _ejecutar("IDX-CONC-001", v)


def test_idx_conc_precios_menores_de_un_anio_se_rechazan():
    s = pd.Series(np.linspace(1, 2, 100), index=pd.bdate_range("2026-01-01", periods=100))
    with pytest.raises(ErrorFicha, match="menos de 1 año"):
        _ejecutar("IDX-CONC-001", {"composicion": fm._composicion(20, igual=True)}, series={"C00": s})


# ------------------------------------------------------------------ IDX-REL-001
def test_idx_rel_ajuste_sectorial_y_momentum_a_mano():
    v = fm._datos_idx_rel(mismo=False)
    v["sectores"] = {"pesos_a": {"tec": 0.6, "fin": 0.4},
                     "multiplos_b": {"per_adelantado": {"tec": 25.0, "fin": 10.0}}}
    v["er_a"], v["er_b"] = {"valor": 0.06, "fuente": "IDX-ERP-001"}, {"valor": 0.05, "fuente": "IDX-ERP-001"}
    res, _ = _ejecutar("IDX-REL-001", v)
    recomp = 1 / (0.6 / 25 + 0.4 / 10)
    neutral = res["brecha_neutral_sectorial"]["per_adelantado"]
    assert neutral["multiplo_b_recompuesto"] == pytest.approx(recomp, rel=1e-12)
    pa = v["indice_a"]["historia"][-1]["per_adelantado"]
    assert neutral["brecha_neutral"] == pytest.approx(pa / recomp - 1, rel=1e-12)
    assert res["diferencia_er"] == pytest.approx(0.01, rel=1e-12)
    # Misma divisa: cubierto = no cubierto; rt de A crece a 1,006 y el de B a 1,0065 por mes.
    r = 1.006 / 1.0065
    for modo in ("cubierta", "no_cubierta"):
        assert res["momentum_relativo"][modo]["12-1"] == pytest.approx(r ** 11 - 1, rel=1e-10)
        assert res["momentum_relativo"][modo]["3m"] == pytest.approx(r ** 3 - 1, rel=1e-10)


def test_idx_rel_divisa_distinta_cubierta_y_no_cubierta():
    v = fm._datos_idx_rel(mismo=False)
    v["indice_b"] = copy.deepcopy(v["indice_b"])
    v["indice_b"]["divisa"] = "USD"
    for i, h in enumerate(v["indice_b"]["historia"]):
        h["fx"] = 0.9 * 1.001 ** i
        h["diferencial_cobertura"] = -0.012
    res, _ = _ejecutar("IDX-REL-001", v)
    r = 1.006 / 1.0065
    nc = res["momentum_relativo"]["no_cubierta"]
    assert nc["3m"] == pytest.approx(r ** 3 / 1.001 ** 3 - 1, rel=1e-10)
    cub = res["momentum_relativo"]["cubierta"]
    assert cub["3m"] == pytest.approx(r ** 3 / (1 - 0.012 / 12) ** 3 - 1, rel=1e-10)


@pytest.mark.parametrize("mutar,params,motivo", [
    (lambda v: [ix.update(historia=ix["historia"][-100:]) for ix in (v["indice_a"], v["indice_b"])], {}, "< 10"),
    (lambda v: None, {"divisa_comun": None}, "sin divisa común"),
    (lambda v: v["indice_b"].update(divisa="USD"), {"cobertura": "no_cubierta"}, "sin «fx»"),
    (lambda v: v["indice_b"].update(divisa="USD"), {"cobertura": "cubierta"}, "sin «diferencial_cobertura»"),
    (lambda v: [h.pop("cape") for h in v["indice_b"]["historia"]], {}, "falta el múltiplo"),
    (lambda v: v.update(sectores={"pesos_a": {"tec": 0.5}, "multiplos_b": {}}), {}, "sumar 1"),
])
def test_idx_rel_rechazos(mutar, params, motivo):
    v = copy.deepcopy(fm._datos_idx_rel(mismo=False))
    mutar(v)
    with pytest.raises(ErrorFicha, match=motivo):
        _ejecutar("IDX-REL-001", v, params)


# ------------------------------------------------------------------ IDX-REB-001
def test_idx_reb_demanda_a_mano():
    res, lim = _ejecutar("IDX-REB-001", {"evento": fm._evento_reb(),
                                         "proximo_evento": {"fecha_anuncio": "2027-05-20",
                                                            "fecha_efectividad": "2027-06-18"}})
    inc, exc = res["demanda_estimada"]["inclusiones"], res["demanda_estimada"]["exclusiones"]
    assert inc["demanda"] == pytest.approx(1e9) and inc["dias_volumen_cesta"] == pytest.approx(2.0)
    assert exc["demanda"] == pytest.approx(-1e9) and exc["dias_volumen_cesta"] == pytest.approx(-5.0)
    assert res["estudio_eventos"] is None and any("< 20" in x for x in lim)
    assert res["calendario_proximo_evento"]["fecha_efectividad"] == "2027-06-18"


def test_idx_reb_estudio_de_eventos_con_ic_bmp_y_tendencia():
    v = {"evento": fm._evento_reb(), "eventos_comparables": copy.deepcopy(fm._EV)}
    res, lim = _ejecutar("IDX-REB-001", v, {"nivel_ic": 0.9})
    e = res["estudio_eventos"]["anuncio_efectividad"]
    assert e["n"] == 20 and e["car_medio"] == pytest.approx(np.mean(fm._CAR1), rel=1e-8)
    assert e["car_mediano"] == pytest.approx(np.median(fm._CAR1), rel=1e-8)
    assert e["ic"]["inf"] < e["car_medio"] < e["ic"]["sup"]
    assert e["t_bmp"] > 0 and 0 <= e["p_valor_bmp"] < 0.05
    assert e["tendencia_por_decada"] > 0   # el CAR plantado crece con el año del evento
    post = res["estudio_eventos"]["efectividad_post"]
    assert post["car_medio"] < 0 and post["tendencia_por_decada"] < 0
    assert res["segunda_via"]["modelo"] == "modelo_mercado"
    assert not any("IC no entregado" in x for x in lim)


def test_idx_reb_eventos_sin_estimacion_suficiente_se_excluyen():
    evs = copy.deepcopy(fm._EV)
    evs[0]["rentabilidades"] = evs[0]["rentabilidades"][100:]
    res, lim = _ejecutar("IDX-REB-001", {"evento": fm._evento_reb(), "eventos_comparables": evs})
    assert res["estudio_eventos"] is None
    assert any("excluidos" in x for x in lim) and any("utilizables" in x for x in lim)


@pytest.mark.parametrize("mutar,params,motivo", [
    (lambda e: e["activos_indexados"].pop("fuente"), {}, "sin fuente"),
    (lambda e: e["cambios"][0].update(delta_peso=0.002), {}, "no es 0"),
    (lambda e: e.update(flujos_declarados=0.001), {}, "no es 0"),
    (lambda e: e["cambios"][0].update(volumen_medio=0), {}, "volumen medio"),
    (lambda e: e.update(fecha_efectividad="2026-11-01"), {}, "anterior al anuncio"),
    (lambda e: None, {"modelo_normal": "fama_french"}, "no admitido"),
])
def test_idx_reb_rechazos(mutar, params, motivo):
    ev = fm._evento_reb()
    mutar(ev)
    with pytest.raises(ErrorFicha, match=motivo):
        _ejecutar("IDX-REB-001", {"evento": ev}, params)
