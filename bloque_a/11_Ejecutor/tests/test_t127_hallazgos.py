"""T-127 · Motor del Bloque A: hallazgos abiertos de la QA r02 de T-119 y de la QA r01 de T-121.

- T-119 H-10: frontera con el Bloque B (1.6) en FIR-CRED-001, REI-LEV-001 y CHR-TOKEN-001: casi clones, un componente de
  peso casi total, estadísticos de orden con pocos componentes, subconjuntos (covenants, staking, concentración) y la
  «propia red» de CHR-TOKEN-001 (`fichas_p2.FRONTERA_B`, INC-T127-01).
- T-119 H-11: la caché distingue una tupla de una lista (`servicio._marcado`).
- T-121 H-07: CT-10 solo da CONVENCION_DISTINTA si la re-ejecución ha tomado algo de `por_defecto.yaml` que ya no es lo de
  entonces (`_ConfiguracionLeida.respaldos`).
- T-121 H-08: un único criterio de día para la fecha de corte (`operaciones.dia`) en las fichas con datos en línea.
- T-121 H-09: FON-DISC-001 compara la fecha de NAV por día con la última de «fechas».
"""
import copy
import json
import math
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.motor import (
    fichas_fon_der,
    fichas_mon_idx,
    fichas_reales,
    fichas_tcv,
    servicio,
)
from bloque_a.motor import fichas_p2 as fp
from bloque_a.motor import operaciones as op
from bloque_a.motor.operaciones import ErrorFicha

from bloque_a import configuracion


class _Proveedor:
    as_of = None
    nombre = "pruebas"


def _motor(carpeta, cfg=None):
    return servicio.Motor(Almacen(Path(carpeta)), _Proveedor(), cfg or cargar_config())


def _caso(ficha, i=0, modulo=fp):
    v = {}
    for d in modulo.CASOS_CONTROL[ficha][i]["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    return v, dict(modulo.CASOS_CONTROL[ficha][i]["parametros"])


def _correr(ficha, v, p=None):
    return fp.FICHAS[ficha]["fn"]({"valores": copy.deepcopy(v), "series": {}, "series_rol": {}}, dict(p or {}))


def _peticion(ficha, i=0, v=None, p=None, **extra):
    caso = servicio.CASOS_CONTROL[ficha][i]
    datos = [{"valores": copy.deepcopy(v)}] if v is not None else copy.deepcopy(caso["datos"])
    return {"operacion": ficha, "datos": datos, "parametros": dict(p if p is not None else caso.get("parametros") or {}),
            **extra}


def _escala(c, k, claves, ident):
    c = copy.deepcopy(c)
    c["id"] = ident
    for q in claves:
        c[q] = c[q] * k
    return c


def _numeros(x):
    if isinstance(x, dict):
        for y in x.values():
            yield from _numeros(y)
    elif isinstance(x, list):
        for y in x:
            yield from _numeros(y)
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        yield float(x)


LEV_CAMPOS = ("gav", "deuda", "caja", "ebitda", "gastos_financieros", "ffo")
TOKEN_CAMPOS = ("precio", "oferta_circulante", "oferta_total", "oferta_maxima", "emision_anual", "quema_anual")
FIR_CAMPOS = ("capitalizacion", "volatilidad_acciones", "deuda_corto", "deuda_largo")


def _lev_extra(n, covenants=True):
    """`n` sociedades más para REI-LEV-001, distintas entre sí y de las del caso de control, sin dominar el agregado."""
    out = []
    for i in range(n):
        c = {"id": f"X{i}", "gav": 500.0 + 70 * i, "deuda": 200.0 + 15 * i, "caja": 8.0 + i, "ebitda": 25.0 + 2 * i,
             "gastos_financieros": 6.0 + i, "ffo": 15.0 + i,
             "vencimientos": [{"fecha": "2027-06-30", "importe": 50.0, "coste": 0.02},
                              {"fecha": "2029-06-30", "importe": 150.0 + 15 * i, "coste": 0.03}]}
        if covenants:
            c["covenants"] = {"ltv_max": 0.6, "icr_min": 2.0}
        out.append(c)
    return out


def _token_extra(n):
    return [{"id": f"TX{i}", "precio": 1.0 + 0.3 * i, "oferta_circulante": 1.0e8 + 2.0e7 * i, "oferta_total": 2.0e8 + 3.0e7 * i,
             "oferta_maxima": None, "emision_anual": 1.0e6 * (i + 1), "quema_anual": 0.0,
             "calendario": {"fuente": "documentación", "desbloqueos": []}} for i in range(n)]


# ====================================================================================================== H-10 · umbrales
def test_h10_las_reglas_de_la_frontera_son_umbrales_fijos_de_las_tres_fichas():
    assert fp.FRONTERA_B == {"tolerancia_clon": 0.01, "peso_maximo_componente": 0.95, "componentes_minimos_orden": 7}
    assert fp.FRONTERA_B["componentes_minimos_orden"] == len(fp.ESTADISTICOS_ORDEN) + 2
    assert set(fp._distribucion(np.arange(9.0))) == set(fp.ESTADISTICOS_ORDEN)       # los que entrega la dispersión
    assert fp.UMBRALES["CHR-TOKEN-001"]["redes_propias"] == {"bitcoin": "BTC", "ethereum": "ETH"}
    for ficha in ("FIR-CRED-001", "REI-LEV-001", "CHR-TOKEN-001"):
        assert {k: fp.UMBRALES[ficha][k] for k in fp.FRONTERA_B} == fp.FRONTERA_B
        v, p = _caso(ficha, 1)
        for clave in (*fp.FRONTERA_B, "redes_propias") if ficha == "CHR-TOKEN-001" else fp.FRONTERA_B:
            with pytest.raises(ErrorFicha, match="umbrales fijos"):
                _correr(ficha, v, {**p, clave: 0.5})


# ====================================================================================================== H-10 · casi clones
@pytest.mark.parametrize("ficha,clave,campo,n", [("FIR-CRED-001", "componentes", "capitalizacion", 10),
                                                ("REI-LEV-001", "componentes", "gav", 3),
                                                ("CHR-TOKEN-001", "tokens", "precio", 2)])
def test_h10_casi_clones_de_un_emisor_se_rechazan(ficha, clave, campo, n, tmp_path):
    """El ataque del revisor (`r02_01`, vía A): `n` copias de un emisor que difieren en 1e-9 relativo por copia."""
    v, p = _caso(ficha, 1)
    v[clave] = [_escala(v[clave][0], 1 + i * 1e-9, (campo,), f"EMISOR_SECRETO_{i}") for i in range(n)]
    with pytest.raises(ErrorFicha, match=rf"rechazo: {n - 1} componentes con los mismos datos que otro \(a menos del 1%") as e:
        _correr(ficha, v, p)
    assert "EMISOR_SECRETO" not in str(e.value)
    r = _motor(tmp_path).servir(_peticion(ficha, 1, v, p), "AG-21")
    assert r["estado"] == "RECHAZADO" and "EMISOR_SECRETO" not in r["detalle"]


@pytest.mark.parametrize("factor,clon", [(1.0100, True), (1.0102, False)])
def test_h10_borde_de_la_tolerancia_de_clon(factor, clon):
    """|a − b| ≤ 1 %·max(|a|, |b|): con un factor k, la diferencia relativa es (k − 1)/k (0,0099 y 0,0101)."""
    v, p = _caso("REI-LEV-001", 1)
    otro = _escala(v["componentes"][0], factor, LEV_CAMPOS, "S9")
    otro["vencimientos"] = [{**x, "importe": x["importe"] * factor} for x in otro["vencimientos"]]
    v["componentes"].append(otro)
    if clon:
        with pytest.raises(ErrorFicha, match="rechazo: 1 componentes con los mismos datos que otro"):
            _correr("REI-LEV-001", v, p)
    else:
        assert _correr("REI-LEV-001", v, p)[0]["n_componentes"] == 4


def test_h10_un_solo_dato_distinto_basta_para_no_ser_clon():
    """Un clon lo es en todos los datos del cálculo: basta uno que difiera más de la tolerancia."""
    v, p = _caso("CHR-TOKEN-001", 1)
    otro = _escala(v["tokens"][0], 1.0, (), "TKZ")
    otro["quema_anual"] = otro["quema_anual"] * 1.5
    v["tokens"].append(otro)
    assert _correr("CHR-TOKEN-001", v, p)[0]["n_tokens"] == 3
    otro["quema_anual"] = v["tokens"][0]["quema_anual"] * 1.005
    with pytest.raises(ErrorFicha, match="con los mismos datos que otro"):
        _correr("CHR-TOKEN-001", v, p)


def test_h10_una_cadena_de_casi_clones_es_un_solo_componente():
    """Cada eslabón difiere un 0,8 % del anterior (menos del 1 %), y el primero y el último un 2,4 %: el cierre transitivo
    los junta en un grupo."""
    v, p = _caso("REI-LEV-001", 1)
    base = v["componentes"][0]
    cadena = []
    for i in range(4):
        c = _escala(base, 1.008 ** i, LEV_CAMPOS, f"C{i}")
        c["vencimientos"] = [{**x, "importe": x["importe"] * 1.008 ** i} for x in c["vencimientos"]]
        cadena.append(c)
    assert abs(cadena[3]["gav"] - cadena[0]["gav"]) / cadena[3]["gav"] > 0.02
    v["componentes"] = cadena + v["componentes"][1:]
    with pytest.raises(ErrorFicha, match="rechazo: 3 componentes con los mismos datos que otro"):
        _correr("REI-LEV-001", v, p)
    assert fp._grupos_casi_iguales([(1.0, None), (1.0, None), (1.0, 0.0)], 0.01) == 2   # un dato ausente solo es igual a otro


def test_h10_la_tolerancia_compara_por_el_mayor_y_los_ceros_son_iguales():
    g = fp._grupos_casi_iguales
    assert g([(100.0, 0.0), (99.0, 0.0)], 0.01) == 1                                    # 1/100 = 0,01: clon
    assert g([(100.0, 0.0), (98.99, 0.0)], 0.01) == 2
    assert g([(-100.0,), (-99.5,)], 0.01) == 1 and g([(1.0,), (-1.0,)], 0.01) == 2
    assert g([(0.0,), (1e-300,)], 0.01) == 2 and g([], 0.01) == 0


# ====================================================================================================== H-10 · dominancia
def test_h10_un_componente_de_peso_casi_total_se_rechaza(tmp_path):
    """El ataque del revisor (`r02_01`, vía B): una sociedad y las otras a escala 1e-6; un token y un relleno de precio
    1e-9; un emisor y otros nueve con la deuda a escala 1e-6."""
    v, p = _caso("REI-LEV-001", 1)
    for x in range(3):
        w = copy.deepcopy(v)
        for j, c in enumerate(w["componentes"]):
            if j != x:
                for q in LEV_CAMPOS:
                    c[q] *= 1e-6
                for vto in c["vencimientos"]:
                    vto["importe"] *= 1e-6
        with pytest.raises(ErrorFicha, match=r"rechazo: un componente pesa el 99\.99\d\d% de «gav» \(más del 95%\)"):
            _correr("REI-LEV-001", w, p)
    t, q = _caso("CHR-TOKEN-001", 1)
    t["tokens"][1]["precio"] *= 1e-9
    with pytest.raises(ErrorFicha, match="de «capitalizacion_circulante» \\(más del 95%\\)"):
        _correr("CHR-TOKEN-001", t, q)
    f, pf = _caso("FIR-CRED-001", 1)
    for c in f["componentes"][1:]:
        c["capitalizacion"] *= 1e-6
        c["deuda_corto"] *= 1e-6
        c["deuda_largo"] *= 1e-6
    with pytest.raises(ErrorFicha, match="de «deuda» \\(más del 95%\\)"):
        _correr("FIR-CRED-001", f, pf)
    r = _motor(tmp_path).servir(_peticion("CHR-TOKEN-001", 1, t, q), "AG-21")
    assert r["estado"] == "RECHAZADO" and "TKA" not in r["detalle"] and "TKB" not in r["detalle"]


def test_h10_borde_de_la_dominancia_y_bases_de_rei_lev():
    fp._sin_dominio({"x": [19.0, 1.0]}, "prueba", 0.95)                                  # 95 % justo: se admite
    with pytest.raises(ErrorFicha, match=r"pesa el 95\.0100%"):
        fp._sin_dominio({"x": [19.002, 0.998]}, "prueba", 0.95)
    fp._sin_dominio({"x": [0.0, 0.0]}, "prueba", 0.95)                                   # base nula: nadie domina
    # el ICR del agregado sería el de S1 si las demás tuvieran EBITDA y gastos financieros despreciables
    for q in ("ebitda", "gastos_financieros", "deuda"):
        v, p = _caso("REI-LEV-001", 1)
        for c in v["componentes"][1:]:
            c[q] *= 1e-6
            if q == "deuda":
                c["caja"] = 0.0
                for vto in c["vencimientos"]:
                    vto["importe"] *= 1e-6
        with pytest.raises(ErrorFicha, match=f"de «{q}»"):
            _correr("REI-LEV-001", v, p)
    # el FFO cuenta en valor absoluto: uno negativo no deja de pesar, y un FFO despreciable en los demás se rechaza
    v, p = _caso("REI-LEV-001", 1)
    v["componentes"][2]["ffo"] = -20.0                                   # |30|/(30 + 14 + 20) = 47 %; sin el valor absoluto, 125 %
    assert _correr("REI-LEV-001", v, p)[0]["n_componentes"] == 3
    for c in v["componentes"][1:]:
        c["ffo"] = 1e-9
    with pytest.raises(ErrorFicha, match="de «ffo»"):
        _correr("REI-LEV-001", v, p)


# ====================================================================================================== H-10 · orden
def test_h10_con_tres_componentes_no_se_entregan_sus_cifras_individuales(tmp_path):
    """El caso del revisor (`r02_01`, vía C): con los 3 componentes del caso de control, el mínimo, la mediana y el máximo
    eran las tres cifras. Ahora no hay dispersión, y ningún número de la entrega es el LTV o el ICR de una sociedad."""
    r = _motor(tmp_path).servir(_peticion("REI-LEV-001", 1), "AG-21")
    assert r["estado"] == "SERVED_WITH_LIMITATIONS" and r["resultado"]["dispersion"] is None
    assert any(x.startswith("sin estadísticos de orden de las holguras frente a covenants, la dispersión de los componentes:"
                            " menos de 7 componentes distintos") for x in r["limitaciones"])
    v, _ = _caso("REI-LEV-001", 1)
    individuales = [(c["deuda"] - c["caja"]) / c["gav"] * 100 for c in v["componentes"]]
    individuales += [c["ebitda"] / c["gastos_financieros"] for c in v["componentes"]]
    for x in _numeros(r["resultado"]):
        assert not any(math.isclose(x, y, rel_tol=1e-9) for y in individuales), x


@pytest.mark.parametrize("extra,orden", [(3, False), (4, True)])
def test_h10_la_dispersion_de_rei_lev_empieza_en_siete_componentes(extra, orden):
    v, p = _caso("REI-LEV-001", 1)
    v["componentes"] += _lev_extra(extra)
    res, lim = _correr("REI-LEV-001", v, p)
    assert res["n_componentes"] == 3 + extra and (res["dispersion"] is not None) == orden
    assert (res["covenants"]["holgura_ltv_pp"] is not None) == orden
    assert any("sin estadísticos de orden" in x for x in lim) != orden
    if orden:
        comps = v["componentes"]
        ltv = [(c["deuda"] - c["caja"]) / c["gav"] * 100 for c in comps]
        icr = [c["ebitda"] / c["gastos_financieros"] for c in comps]
        d = res["dispersion"]
        assert d["ltv_pct"] == pytest.approx({"minimo": min(ltv), "q25": np.percentile(ltv, 25), "mediana": np.median(ltv),
                                              "q75": np.percentile(ltv, 75), "maximo": max(ltv)}, rel=1e-12)
        assert d["icr_veces"]["mediana"] == pytest.approx(np.median(icr), rel=1e-12)
        hol = [(c["covenants"]["ltv_max"] - l_ / 100) * 100 for c, l_ in zip(comps, ltv, strict=True)]
        assert res["covenants"]["holgura_ltv_pp"]["q25"] == pytest.approx(np.percentile(hol, 25), rel=1e-12)


@pytest.mark.parametrize("extra,orden", [(4, False), (5, True)])
def test_h10_la_dispersion_de_chr_token_empieza_en_siete_tokens(extra, orden):
    v, p = _caso("CHR-TOKEN-001", 1)
    v["tokens"] += _token_extra(extra)
    res, lim = _correr("CHR-TOKEN-001", v, p)
    assert res["n_tokens"] == 2 + extra and (res["dispersion"] is not None) == orden
    assert any("sin estadísticos de orden de la dispersión de los tokens" in x for x in lim) != orden
    if orden:
        fdv = [t["precio"] * (t["oferta_maxima"] if t["oferta_maxima"] is not None else t["oferta_total"])
               / (t["precio"] * t["oferta_circulante"]) for t in v["tokens"]]
        assert res["dispersion"]["fdv_sobre_capitalizacion_veces"]["q75"] == pytest.approx(np.percentile(fdv, 75), rel=1e-12)


def test_h10_fir_cred_conserva_su_dispersion_con_diez_o_mas():
    v, p = _caso("FIR-CRED-001", 1)
    res, lim = _correr("FIR-CRED-001", v, p)
    assert set(res["neutral_al_riesgo"]["dd"]) == {*fp.ESTADISTICOS_ORDEN, "media_ponderada_deuda"}
    assert not any("estadísticos de orden" in x for x in lim)


# ====================================================================================================== H-10 · subconjuntos
def test_h10_covenants_de_menos_componentes_que_el_minimo_no_se_calculan():
    v, p = _caso("REI-LEV-001", 1)
    v["componentes"][2].pop("covenants")                                                   # S1 y S2: 2 (< 3)
    res, lim = _correr("REI-LEV-001", v, p)
    assert res["covenants"] is None
    assert "covenants de 2 de 3 componentes (< 3): holgura no calculada; con tan pocos serían las cifras de emisores " \
           "concretos (1.6)" in lim
    v["componentes"][1].pop("covenants")                                                   # uno: su «incumplimiento»
    assert _correr("REI-LEV-001", v, p)[0]["covenants"] is None
    v["componentes"] += _lev_extra(1)                                                      # S1 y X0 de 4: 2 (< 3)
    assert _correr("REI-LEV-001", v, p)[0]["covenants"] is None
    v["componentes"] += _lev_extra(2)[1:]                                                  # S1, X0 y X1: 3
    c = _correr("REI-LEV-001", v, p)[0]["covenants"]
    assert c["n_componentes"] == 3 and c["holgura_ltv_pp"] is None


def test_h10_staking_y_concentracion_de_un_solo_token_o_dominados_no_se_calculan():
    v, p = _caso("CHR-TOKEN-001", 1)
    for k in ("staking_nominal", "concentracion_10_mayores"):
        v["tokens"][1].pop(k)
    res, lim = _correr("CHR-TOKEN-001", v, p)
    assert res["rendimiento_real_staking_pct"] is None and res["concentracion_10_mayores_pct"] is None
    assert res["cobertura_staking_pct"] == 0.0 and res["cobertura_concentracion_pct"] == 0.0
    assert any(x.startswith("rendimiento de staking de 1 de 2 tokens, con menos de 2") for x in lim)
    # dos que lo declaran, pero uno pesa el 99 % de su capitalización
    # T-127 r02 (H-02): nominal 4,5 % (antes 4 %): con 4 %, su rendimiento real (4 % − 1 %) era el de TKA (8 % − 5 %), y
    # el de los dos sería la cifra de cada uno (ya no se entrega)
    v["tokens"].append({**_token_extra(1)[0], "precio": 0.1, "staking_nominal": 0.045, "concentracion_10_mayores": 0.3})
    res, lim = _correr("CHR-TOKEN-001", v, p)
    assert res["rendimiento_real_staking_pct"] is None and any("más del 95% de su capitalización" in x for x in lim)
    # dos que lo declaran sin dominar: se calcula sobre ellos, con su cobertura
    v["tokens"][2]["precio"] = 2.0
    res, lim = _correr("CHR-TOKEN-001", v, p)
    cm = [t["precio"] * t["oferta_circulante"] for t in v["tokens"]]
    infl = [(t["emision_anual"] - t["quema_anual"]) / t["oferta_circulante"] for t in v["tokens"]]
    esperado = (cm[0] * (0.08 - infl[0]) + cm[2] * (0.045 - infl[2])) / (cm[0] + cm[2]) * 100
    assert res["rendimiento_real_staking_pct"] == pytest.approx(esperado, rel=1e-12)
    assert res["cobertura_staking_pct"] == pytest.approx((cm[0] + cm[2]) / sum(cm) * 100, rel=1e-12)


# ====================================================================================================== H-10 · red propia
def test_h10_la_propia_red_es_una_red_de_la_ficha_con_su_token(tmp_path):
    v, p = _caso("CHR-TOKEN-001", 1)
    uno = {**v, "tokens": [v["tokens"][0]], "ambito_es_red": True}
    for ambito, ident in (("red TKA", "TKA"), ("sector de capa 2", "TKA"), ("Bitcoin", "ETH"), ("Bitcoin", "TKA"),
                          ("Ethereum", "BTC"), ("Bitcoin y Ethereum", "BTC")):
        w = {**uno, "ambito": ambito, "tokens": [{**uno["tokens"][0], "id": ident}]}
        with pytest.raises(ErrorFicha, match="con un solo token, el ámbito tiene que ser una red con token propio"):
            _correr("CHR-TOKEN-001", w, p)
    for ambito, ident in (("Bitcoin", "BTC"), (" bitcoin ", "btc"), ("ETHEREUM", "ETH")):
        w = {**uno, "ambito": ambito, "tokens": [{**uno["tokens"][0], "id": ident}]}
        res, lim = _correr("CHR-TOKEN-001", w, p)
        assert res["n_tokens"] == 1 and res["dispersion"] is None and res["rendimiento_real_staking_pct"] is not None
        assert any(x.startswith("un solo token: el ámbito declarado es la propia red") for x in lim)
    r = _motor(tmp_path).servir(_peticion("CHR-TOKEN-001", 1, {**uno, "ambito": "red TKA"}, p), "AG-21")
    assert r["estado"] == "RECHAZADO" and "(1.6)" in r["detalle"]


def test_h10_los_casos_de_control_siguen_superados(tmp_path):
    res = _motor(tmp_path).verificar_casos_control(["FIR-CRED-001", "REI-LEV-001", "CHR-TOKEN-001"])
    assert all(x["superados"] for x in res.values()), res


# ====================================================================================================== H-11
def test_h11_la_tupla_no_sale_de_la_cache_de_la_lista_en_ningun_orden(tmp_path):
    v, p = _caso("FIR-CRED-001", 1)
    tupla = {**v, "componentes": tuple(v["componentes"])}
    sola = _motor(tmp_path / "sola").servir(_peticion("FIR-CRED-001", 1, tupla, p), "AG-21")
    assert sola["estado"] == "RECHAZADO" and "se esperaba una lista no vacía" in sola["detalle"]
    m = _motor(tmp_path / "lista_y_tupla")
    assert m.servir(_peticion("FIR-CRED-001", 1, v, p), "AG-21")["estado"].startswith("SERVED")
    r = m.servir(_peticion("FIR-CRED-001", 1, tupla, p), "AG-21")
    assert r["estado"] == "RECHAZADO" and not r.get("cache_hit")
    assert m.servir(_peticion("FIR-CRED-001", 1, v, p), "AG-21")["cache_hit"]               # la lista sigue en la caché
    m2 = _motor(tmp_path / "tupla_y_lista")
    assert m2.servir(_peticion("FIR-CRED-001", 1, tupla, p), "AG-21")["estado"] == "RECHAZADO"
    r2 = m2.servir(_peticion("FIR-CRED-001", 1, v, p), "AG-21")
    assert r2["estado"].startswith("SERVED") and not r2["cache_hit"]


def test_h11_la_firma_distingue_contenedores_y_claves():
    f = servicio._firma_tipos
    assert f([1, 2]) != f((1, 2)) and f({"a": [1]}) != f({"a": (1,)}) and f([[1]]) != f([(1,)])
    assert f({1: "x"}) != f({"1": "x"}) and f({"a": 1}) != f({"a": 1.0}) and f({"a": 1}) != f({"a": True})
    assert f({"a": 1, "b": 2}) == f({"b": 2, "a": 1})                                       # el orden de las claves no cuenta
    assert f({"a": [1, {"b": (2,)}]}) == f({"a": [1, {"b": (2,)}]})
    assert f({"a": 1.5}) == f({"a": np.float64(1.5)}) and f(np.float32(1.5)) != f(1.5)    # como en la r02 de T-119
    assert f({"l": [1]}) != f([1])                                                         # un dict no se confunde con la marca
    assert f({(1, 2): 3}) is None and f({frozenset(): 1}) is None


# ====================================================================================================== H-07
def _artefacto_alterado(m, ficha, i, clave):
    r = m.servir(_peticion(ficha, i), "AG-18")
    assert r["estado"].startswith("SERVED"), r
    e = copy.deepcopy(m.almacen.estado("RC")[r["calc_id"]])
    e["resultado"]["payload"][clave] = e["resultado"]["payload"][clave] * 2 + 1
    e["calc_id"] = m.almacen.nuevo_id("CALC")
    m.almacen.escribir("RC", "AG-13", e)
    return r["calc_id"], e["calc_id"]


def _con_por_defecto(monkeypatch, cambio):
    d = copy.deepcopy(configuracion.config_por_defecto())
    cambio(d)
    monkeypatch.setattr(configuracion, "_CONFIG_POR_DEFECTO", d)
    return copy.deepcopy(d)


@pytest.mark.parametrize("ficha,i,clave,cambio", [
    ("DEC-VOI-001", 1, "voi_puntos", lambda d: d["parametros_ht03"].__setitem__("clave_nueva", 1)),
    ("DEC-VOI-001", 1, "voi_puntos", lambda d: d["parametros_ht03"]["umbrales"].__setitem__("Z", 99)),
    ("RISK-VAR-001", 0, "var", lambda d: d["horizontes"].__setitem__("H6", {"meses": 240})),
], ids=["A2_clave_nueva", "A2b_clave_nueva_anidada", "A5_horizonte_nuevo"])
def test_h07_una_clave_nueva_de_por_defecto_que_la_ficha_no_lee_no_ablanda_el_error(tmp_path, monkeypatch, ficha, i, clave,
                                                                                    cambio):
    """Los casos A2, A2b y A5 del revisor (`r01_02_h01_ct10.py`): el artefacto guarda la sección entera; `por_defecto.yaml`
    gana una clave que nadie lee. El bueno se reproduce y el alterado es ERROR_ORIGINAL."""
    bueno, malo = _artefacto_alterado(_motor(tmp_path), ficha, i, clave)
    cfg = _con_por_defecto(monkeypatch, cambio)
    m = servicio.Motor(Almacen(tmp_path), _Proveedor(), cfg)
    assert m.reejecutar(bueno, "auditoría")["coincide"] == "SI"
    out = m.reejecutar(malo, "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", "ERROR_ORIGINAL"), out


@pytest.mark.parametrize("h5,categoria", [({"meses": 60}, "CONVENCION_DISTINTA"), (None, "ERROR_ORIGINAL")])
def test_h07_convencion_distinta_si_la_ruta_leida_salio_del_fichero_y_este_cambio(tmp_path, monkeypatch, h5, categoria):
    """RISK-VAR-001 lee `horizontes.H5`. Un Motor sin H5 en su configuración la toma de `por_defecto.yaml`; el artefacto
    guarda `horizontes` sin H5. Si después el fichero cambia H5, la re-ejecución no ha podido usar lo de entonces
    (CONVENCION_DISTINTA); si el fichero no cambia, el que difiere es el original (ERROR_ORIGINAL)."""
    cfg = cargar_config()
    del cfg["horizontes"]["H5"]
    m = _motor(tmp_path, cfg)
    bueno, malo = _artefacto_alterado(m, "RISK-VAR-001", 0, "var")
    registro = m.almacen.estado("RC")[bueno]["artefacto"]["configuracion_usada"]["horizontes"]
    assert "H5" not in registro["valor"]
    if h5 is not None:
        cfg = _con_por_defecto(monkeypatch, lambda d: d["horizontes"].__setitem__("H5", h5))
        del cfg["horizontes"]["H5"]
    m2 = servicio.Motor(Almacen(tmp_path), _Proveedor(), cfg)
    out = m2.reejecutar(malo, "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", categoria), out
    if categoria == "CONVENCION_DISTINTA":
        assert "horizontes" in out["diagnostico"]


def test_h07_la_configuracion_leida_apunta_solo_lo_que_sale_del_fichero():
    leida = servicio._ConfiguracionLeida({"horizontes": {"H5": {"meses": 120}}, "evaluacion": {}})
    assert configuracion.parametro(leida, "horizontes.H5") == {"meses": 120} and leida.respaldos == set()
    configuracion.parametro(leida, "evaluacion.nivel_ic")
    configuracion.parametro(leida, "calendario.sesiones_por_semana")
    assert leida.respaldos == {"evaluacion.nivel_ic", "calendario.sesiones_por_semana"}
    assert configuracion.parametro({"a": 1}, "calendario.sesiones_por_semana") == 5           # un dict normal no apunta
    assert servicio._respaldo_en("uc", {"uc.motor_por_plan.PLAN_MIN"}) and servicio._respaldo_en("uc", {"uc"})
    assert not servicio._respaldo_en("uc", {"ucx.a", "calendario.uc"})                          # por sección, no por prefijo


# ====================================================================================================== H-08
@pytest.mark.parametrize("texto,dia", [("2024-02-01T00:30:00+14:00", "2024-01-31"), ("2024-01-31T23:00:00-05:00", "2024-02-01"),
                                       ("2024-01-31T23:59:59.999", "2024-01-31"), ("2024-01-31", "2024-01-31"),
                                       ("2024-01-31T12:00:00Z", "2024-01-31")])
def test_h08_un_solo_criterio_de_dia_en_los_cuatro_modulos(texto, dia):
    esperado = pd.Timestamp(dia)
    assert op.dia(pd.Timestamp(texto)) == esperado
    assert fichas_reales._fecha(texto, "x") == esperado                                     # Fase 2
    assert fichas_mon_idx._dia(fichas_mon_idx._fecha(texto, "x")) == esperado               # MON e IDX
    assert fichas_tcv._fecha(texto, "x") == esperado.date()                                 # TCV
    assert fichas_tcv._corte({"fecha_corte": texto}) == esperado.date()
    assert op.dia(fichas_fon_der._fecha(texto, "F", "x")) == esperado                      # FON y DER
    assert fichas_tcv._fecha(pd.Timestamp(texto).to_pydatetime(), "x") == esperado.date()
    assert fichas_tcv._fecha(pd.Timestamp(texto), "x") == esperado.date()


def test_h08_tcv_rechaza_un_texto_con_basura_tras_la_fecha_y_fon_admite_zonas_mezcladas():
    with pytest.raises(ErrorFicha, match="fecha no válida"):
        fichas_tcv._fecha("2024-01-31 basura", "x")
    assert fichas_tcv._fecha("2024-01-31 ", "x") == date(2024, 1, 31)
    f = fichas_fon_der._fechas({"f": ["2024-01-30", "2024-02-01T00:30:00+14:00"]}, "f", "F")
    assert list(f.normalize()) == [pd.Timestamp("2024-01-30"), pd.Timestamp("2024-01-31")]


def _ultima(ficha, v):
    if ficha == "MON-YLD-001":
        return v["segmentos"][0], "fecha"
    if ficha == "TCV-CDS-001":
        return v["historia"]["fechas"], -1
    return v["fechas"], -1


@pytest.mark.parametrize("nueva,corte,esperado", [
    (lambda d: f"{d}T00:30:00+14:00", lambda d: d, None),                   # hecho en D+1 local = D en UTC: mismo día
    (lambda d: f"{d}T23:00:00-05:00", lambda d: d, "R"),                    # D local = D+1 en UTC: posterior
    (lambda d: d, lambda d: f"{d}T23:00:00-05:00", "S"),                    # el corte es D+1 en UTC
    (lambda d: f"{d}T23:59:59", lambda d: d, "S"),                          # el día del corte, con hora
], ids=["mas14", "menos5", "corte_menos5", "dia_del_corte_con_hora"])
def test_h08_mismo_veredicto_en_mon_tcv_y_fon(tmp_path, nueva, corte, esperado):
    """Los casos del revisor (`r01_03_h04_bordes.py`, «coherencia entre módulos») en los que cambiar la última fecha no
    rompe la frecuencia mensual de FON-FLOW-001. En «mas14» el dato se escribe como del día siguiente en su zona."""
    m = _motor(tmp_path)
    veredictos = {}
    for ficha, i in (("MON-YLD-001", 1), ("TCV-CDS-001", 0), ("FON-FLOW-001", 0)):
        pet = copy.deepcopy(_peticion(ficha, i))
        cont, k = _ultima(ficha, pet["datos"][0]["valores"])
        d = cont[k][:10]
        siguiente = str((pd.Timestamp(d) + pd.Timedelta(days=1)).date())
        cont[k] = nueva(siguiente if esperado is None else d)
        pet["fecha_corte"] = corte(d)
        r = m.servir(pet, "AG-18")
        veredictos[ficha] = "S" if str(r["estado"]).startswith("SERVED") else "R"
    assert len(set(veredictos.values())) == 1 and set(veredictos.values()) == {esperado or "S"}, veredictos


# ====================================================================================================== H-09
def _fon_disc():
    return _caso("FON-DISC-001", 0, servicio)


def test_h09_fon_disc_un_nav_del_ultimo_dia_con_hora_se_sirve(tmp_path):
    v, p = _fon_disc()
    ultima = v["fechas"][-1][:10]
    nombre = min(v["miembros"])
    v["miembros"][nombre]["fecha_nav"] = f"{ultima}T23:59:59"
    r = _motor(tmp_path).servir(_peticion("FON-DISC-001", 0, v, p), "AG-18")
    assert str(r["estado"]).startswith("SERVED"), r
    siguiente = str((pd.Timestamp(ultima) + pd.Timedelta(days=1)).date())
    v["miembros"][nombre]["fecha_nav"] = siguiente
    r = _motor(tmp_path / "b").servir(_peticion("FON-DISC-001", 0, v, p), "AG-18")
    assert r["estado"] == "RECHAZADO"
    assert f"fecha de NAV posterior a la fecha de corte de la ficha (la última de «fechas», {ultima}; no la de la petición)" \
        in r["detalle"]
    v["miembros"][nombre]["fecha_nav"] = f"{siguiente}T00:30:00+14:00"                  # día {ultima} en UTC
    assert str(_motor(tmp_path / "c").servir(_peticion("FON-DISC-001", 0, v, p), "AG-18")["estado"]).startswith("SERVED")


def test_t127_la_entrega_sigue_siendo_json(tmp_path):
    """Las tres fichas, servidas, siguen dando un resultado que se puede escribir y sin cifras no finitas."""
    m = _motor(tmp_path)
    for ficha in ("FIR-CRED-001", "REI-LEV-001", "CHR-TOKEN-001"):
        r = m.servir(_peticion(ficha, 1), "AG-21")
        assert str(r["estado"]).startswith("SERVED"), r
        json.dumps(r["resultado"], allow_nan=False)
