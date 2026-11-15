"""T-128 · Motor del Bloque A: ninguna ficha entrega la cifra de un instrumento concreto con su identificador (1.6).

Fichas corregidas (tabla de las 80 en `.docs/tickets/T-128/analisis-tecnico.md`, decisiones en INC-T128-01):
- REI-NAV-001: sin `componentes` (prima, peso, NAV y NAV ajustado de cada sociedad); `rango_pct` con 7 distintos o más;
  `dispersion_pct` con 3 o más; las reglas de `frontera_b` (copias a escala, dominancia, aportación).
- REI-FFO-001: sin `cobertura_por_componente`; mínimo de 2 componentes; la cobertura en mediana, IQR, mínimo y máximo con
  7 distintos o más; las reglas de `frontera_b`.
- IDX-REB-001: sin `por_componente`; la demanda de una cesta que aporta casi entera un valor no se entrega.
- CHR-FUND-001: sin la financiación ni el peso de cada plataforma (1.6: ninguna ficha compara plataformas).
- FON-DISC-001 y FON-TD-001: subcategorías y segmentos con menos miembros que el mínimo de la ficha, sin cifra; mínimo,
  máximo y rango de los miembros con 7 o más; las limitaciones no citan miembros.
"""
import copy
import json
import math
import tempfile
from pathlib import Path

import numpy as np
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.motor import fichas_fon_der as fd
from bloque_a.motor import fichas_mon_idx as fm
from bloque_a.motor import fichas_reales as fr
from bloque_a.motor import frontera_b as fb
from bloque_a.motor import servicio
from bloque_a.motor.operaciones import ErrorFicha

MODULO = {"REI-NAV-001": fr, "REI-FFO-001": fr, "CHR-FUND-001": fr, "IDX-REB-001": fm, "FON-DISC-001": fd,
          "FON-TD-001": fd}
COPIAS = "componentes distintos por sus cifras individuales"


class _Proveedor:
    as_of = None
    nombre = "pruebas-t128"


def _correr(ficha, v, p=None):
    return MODULO[ficha].FICHAS[ficha]["fn"]({"valores": copy.deepcopy(v), "series": {}, "series_rol": {}}, dict(p or {}))


def _caso(ficha, i=0):
    v = {}
    for d in MODULO[ficha].CASOS_CONTROL[ficha][i]["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    return v, dict(MODULO[ficha].CASOS_CONTROL[ficha][i]["parametros"])


def _nav_comp(i, cid=None, prima=None):
    """Una sociedad para REI-NAV-001, con su balance cuadrado (NAV = GAV − deuda neta − otros pasivos)."""
    acciones, nav_acc = 5e7 * (1 + 0.3 * i), 20.0 + 3 * i
    nav = acciones * nav_acc
    deuda, otros = 0.3 * nav * (1 + 0.1 * i), 0.05 * nav
    pr = -0.15 + 0.035 * i if prima is None else prima
    return fr._comp_nav(cid or f"S{i}", nav_acc * (1 + pr), acciones, nav_acc, nav + deuda + otros, deuda, otros,
                        0.05 + 0.002 * i)


def _nav(n, **kw):
    v = fr._datos_rei_nav(False)
    v["componentes"] = [_nav_comp(i, **kw) for i in range(n)]
    return v


def _secretos(ficha, v):
    """Los identificadores de los componentes, cambiados por textos que se buscan en la salida."""
    if ficha in ("REI-NAV-001", "REI-FFO-001"):
        for i, c in enumerate(v["componentes"]):
            c["id"] = f"SECRETO_{i}"
    elif ficha == "IDX-REB-001":
        for i, c in enumerate(v["evento"]["cambios"]):
            c["id"] = f"SECRETO_{i}"
    elif ficha == "CHR-FUND-001":
        v["plataformas"] = {f"SECRETO_{i}": x for i, x in enumerate(v["plataformas"].values())}
    else:
        v["miembros"] = {f"SECRETO_{i}": x for i, x in enumerate(v["miembros"].values())}
    return v


# ====================================================================================================== CA-2 · identificadores
@pytest.mark.parametrize("ficha,i", [(f, i) for f in ("REI-NAV-001", "REI-FFO-001", "IDX-REB-001", "FON-DISC-001", "FON-TD-001")
                                     for i in range(len(MODULO[f].CASOS_CONTROL[f]))])
def test_ninguna_salida_ni_limitacion_lleva_el_identificador_de_un_componente(ficha, i):
    v, p = _caso(ficha, i)
    v = _secretos(ficha, v)
    if ficha == "REI-NAV-001":
        v["componentes"] = [_nav_comp(j, f"SECRETO_{j}") for j in range(3)]
        v["componentes"][0].pop("otros_pasivos")                           # una limitación que antes citaba la sociedad
        v["componentes"][1]["fecha_nav"] = "2025-09-30"
    if ficha == "REI-FFO-001":
        v["componentes"][0]["ejercicios"][-1]["dividendo"] = 0.0          # otra que citaba la sociedad
    if ficha == "FON-DISC-001":
        primero = next(iter(v["miembros"].values()))
        primero.update(fecha_nav="2022-06-01", ajuste_nav_declarado="NAV trimestral")
    res, lim = _correr(ficha, v, p)
    texto = json.dumps(res, ensure_ascii=False) + json.dumps(lim, ensure_ascii=False)
    assert "SECRETO" not in texto


def test_chr_fund_no_da_cifras_por_plataforma():
    for i in range(len(fr.CASOS_CONTROL["CHR-FUND-001"])):
        v, p = _caso("CHR-FUND-001", i)
        res, _ = _correr("CHR-FUND-001", _secretos("CHR-FUND-001", v), p)
        assert "financiacion_por_plataforma_pct_anual" not in res and "pesos" not in res
        assert all(isinstance(x, str) for x in res["plataformas"])         # las fuentes, sin cifra al lado
        texto = json.dumps({k: x for k, x in res.items() if k != "plataformas"}, ensure_ascii=False)
        assert "SECRETO" not in texto


def test_las_claves_de_filas_por_componente_ya_no_estan():
    v, p = _caso("REI-NAV-001", 1)
    assert "componentes" not in _correr("REI-NAV-001", v, p)[0]
    v, p = _caso("REI-FFO-001", 1)
    assert "cobertura_por_componente" not in _correr("REI-FFO-001", v, p)[0]
    v, p = _caso("IDX-REB-001", 0)
    assert "por_componente" not in _correr("IDX-REB-001", v, p)[0]


# ====================================================================================================== REI-NAV-001
def test_rei_nav_dispersion_desde_tres_y_rango_desde_siete():
    for n, disp, rango in ((2, False, False), (3, True, False), (6, True, False), (7, True, True)):
        v = _nav(n)
        res, lim = _correr("REI-NAV-001", v, {"cap_objetivo": 0.055})
        caps = np.array([c["precio"] * c["acciones"] for c in v["componentes"]])
        pr = np.array([c["precio"] / c["nav_por_accion"] - 1 for c in v["componentes"]])
        m = np.average(pr, weights=caps)
        assert res["n_componentes"] == n and res["prima_agregada_pct"] == pytest.approx(m * 100, rel=1e-12)
        assert (res["dispersion_pct"] is not None) == disp and (res["rango_pct"] is not None) == rango
        if disp:
            assert res["dispersion_pct"] == pytest.approx(math.sqrt(np.average((pr - m) ** 2, weights=caps)) * 100, rel=1e-12)
        else:
            assert any(x.startswith("sin dispersión de la prima: 2 componentes distintos (< 3)") for x in lim)
        if rango:
            assert res["rango_pct"] == pytest.approx([pr.min() * 100, pr.max() * 100], rel=1e-12)
        else:
            assert any("menos de 7 componentes distintos" in x for x in lim)


def test_rei_nav_copias_a_escala_cuentan_como_una():
    v = _nav(2)
    s0 = v["componentes"][0]
    copia = {**s0, "id": "S9", "acciones": s0["acciones"] * 1.5,
             **{k: s0[k] * 1.5 for k in ("gav", "deuda_neta", "otros_pasivos")}}
    v["componentes"] = [s0, copia]
    with pytest.raises(ErrorFicha, match=rf"rechazo: 1 {COPIAS} \(< 2\)"):
        _correr("REI-NAV-001", v)
    v = _nav(3)
    v["componentes"].append({**copia, "id": "S9"})                          # 4 sociedades, 3 distintas: dispersión sí
    res, _ = _correr("REI-NAV-001", v)
    assert res["n_componentes"] == 4 and res["dispersion_pct"] is not None


def test_rei_nav_dominancia_y_aportacion():
    v = _nav(3)
    for c in v["componentes"][1:]:
        c["acciones"] *= 1e-6
        for k in ("gav", "deuda_neta", "otros_pasivos"):
            c[k] *= 1e-6
    with pytest.raises(ErrorFicha, match="de «capitalizacion»"):
        _correr("REI-NAV-001", v)
    v = _nav(4)
    for i, c in enumerate(v["componentes"][1:], 1):                          # rellenos sin prima: P = NAV
        v["componentes"][i] = _nav_comp(i, prima=0.0)
        v["componentes"][i]["cap_rate_tasacion"] = 0.05 + 0.001 * i
    with pytest.raises(ErrorFicha, match="más del 95% de la prima agregada lo aporta un componente"):
        _correr("REI-NAV-001", v)


def test_rei_nav_ajustado_que_aporta_una_sola_sociedad_no_se_entrega():
    v = _nav(3)
    for i, c in enumerate(v["componentes"]):
        c["cap_rate_tasacion"] = 0.055 if i else 0.05                       # solo S0 cambia con cap_objetivo 0,055
    res, lim = _correr("REI-NAV-001", v, {"cap_objetivo": 0.055})
    assert res["nav_ajustado"] is None
    assert any(x.startswith("sin el NAV ajustado: más del 95%") for x in lim)
    v["componentes"][1]["cap_rate_tasacion"] = 0.052
    assert _correr("REI-NAV-001", v, {"cap_objetivo": 0.055})[0]["nav_ajustado"] is not None


# ====================================================================================================== REI-FFO-001
def test_rei_ffo_un_componente_se_rechaza():
    v, p = _caso("REI-FFO-001", 1)
    v["componentes"] = v["componentes"][:1]
    with pytest.raises(ErrorFicha, match=r"rechazo: 1 componente \(< 2\)"):
        _correr("REI-FFO-001", v, p)
    assert fr.UMBRALES["REI-FFO-001"]["componentes_minimos"] == 2


def test_rei_ffo_cobertura_con_siete_distintos():
    v, p = _caso("REI-FFO-001", 1)
    assert len(v["componentes"]) == 7
    res, _ = _correr("REI-FFO-001", v, p)
    cob = [e["beneficio_neto"] + e["amortizaciones_inmobiliarias"] - e["plusvalias"] - e["capex_mantenimiento"]
           - e["ajuste_rentas_lineales"] for c in v["componentes"] for e in c["ejercicios"] if e["ejercicio"] == 2025]
    div = [e["dividendo"] for c in v["componentes"] for e in c["ejercicios"] if e["ejercicio"] == 2025]
    x = np.array(cob) / np.array(div)
    assert res["cobertura"]["mediana"] == pytest.approx(float(np.median(x)), rel=1e-12)
    assert res["cobertura"]["maximo"] == pytest.approx(float(x.max()), rel=1e-12) and res["cobertura"]["n"] == 7
    v["componentes"] = v["componentes"][:6]
    res, lim = _correr("REI-FFO-001", v, p)
    assert res["cobertura"] is None and res["cobertura_agregada"] is not None
    assert any(x_.startswith("sin estadísticos de orden de la cobertura de los componentes") for x_ in lim)


def test_rei_ffo_copias_dominancia_y_aportacion():
    v, p = _caso("REI-FFO-001", 1)
    x = v["componentes"][0]
    copia = copy.deepcopy(x)
    copia["id"], copia["acciones"] = "X2", x["acciones"] * 1.5
    for e in copia["ejercicios"]:
        for k in ("beneficio_neto", "amortizaciones_inmobiliarias", "plusvalias", "capex_mantenimiento",
                  "ajuste_rentas_lineales", "dividendo"):
            e[k] *= 1.5
    w = {**v, "componentes": [x, copia]}
    with pytest.raises(ErrorFicha, match=rf"rechazo: 1 {COPIAS}"):
        _correr("REI-FFO-001", w, p)
    w = {**v, "componentes": [copy.deepcopy(c) for c in v["componentes"]]}
    for c in w["componentes"][1:]:                                          # rellenos sin FFO en 2025 (BN = −amort.)
        e = c["ejercicios"][-1]
        e.update(beneficio_neto=-e["amortizaciones_inmobiliarias"], plusvalias=0.0, capex_mantenimiento=0.0,
                 ajuste_rentas_lineales=0.0)
    with pytest.raises(ErrorFicha, match="rechazo"):
        _correr("REI-FFO-001", w, p)
    # copias que solo comparten el rendimiento FFO de 2025 (otro CAPEX, otro dividendo y otro 2023): no son un grupo ni
    # dominan una base, pero la aportación al rendimiento FFO es toda de sociedades con la misma cifra
    trio = []
    for j, k in enumerate((1.0, 1.5, 2.0)):
        c = copy.deepcopy(copia)
        c["id"], c["acciones"] = f"K{j}", x["acciones"] * k
        for e in c["ejercicios"]:
            for q in ("beneficio_neto", "amortizaciones_inmobiliarias", "plusvalias", "capex_mantenimiento",
                      "ajuste_rentas_lineales", "dividendo"):
                e[q] = e[q] / 1.5 * k
        c["ejercicios"][-1]["capex_mantenimiento"] *= 1 + 0.3 * j
        c["ejercicios"][-1]["dividendo"] *= 1 + 0.2 * j
        c["ejercicios"][0]["beneficio_neto"] *= 1 + 0.25 * j
        trio.append(c)
    with pytest.raises(ErrorFicha, match="más del 95% de el rendimiento FFO lo aporta un componente"):
        _correr("REI-FFO-001", {**v, "componentes": trio}, p)


# ====================================================================================================== IDX-REB-001
def test_idx_reb_la_cesta_de_un_valor_no_se_entrega():
    ev = fm._evento_reb(cambios=[("IN", 0.001, 5e8), ("OUT1", -0.0007, 2e8), ("OUT2", -0.0003, 1.5e8)])
    res, lim = _correr("IDX-REB-001", {"evento": ev})
    inc, exc = res["demanda_estimada"]["inclusiones"], res["demanda_estimada"]["exclusiones"]
    assert inc == {"demanda": None, "dias_volumen_cesta": None, "n": 1}
    assert exc["demanda"] == pytest.approx(-1e9) and exc["dias_volumen_cesta"] == pytest.approx(-1e9 / 3.5e8)
    assert "sin la demanda estimada de las inclusiones: más del 95% lo aporta un componente (o varios con su misma " \
           "cifra); sería la cifra de ese componente (1.6)" in lim


def test_idx_reb_copias_con_los_mismos_dias_de_volumen_son_un_valor():
    ev = fm._evento_reb(cambios=[("IN1", 0.0006, 5e8), ("IN2", 0.0004, 5e8 * 0.4 / 0.6), ("OUT1", -0.0007, 2e8),
                                 ("OUT2", -0.0003, 1.5e8)])
    res, _ = _correr("IDX-REB-001", {"evento": ev})
    assert res["demanda_estimada"]["inclusiones"]["demanda"] is None
    assert res["demanda_estimada"]["exclusiones"]["demanda"] == pytest.approx(-1e9)


# ====================================================================================================== FON-DISC y FON-TD
def _disc_siete():
    d = fd._ctl_disc(iguales=False)
    base = d["miembros"]["M1"]
    for i in (6, 7):
        nav = np.asarray(base["nav"])
        t = np.arange(nav.size)
        d["miembros"][f"M{i}"] = {"precio": [float(x) for x in nav * (1 - 0.05 + 0.02 * np.cos(t / 7 + i))],
                                  "nav": [float(x) for x in nav], "fecha_nav": base["fecha_nav"], "capitalizacion": 800.0}
    return d


def test_fon_disc_minimo_maximo_y_rango_desde_siete_miembros():
    res, lim = _correr("FON-DISC-001", fd._ctl_disc(iguales=False, constante=True))
    assert res["dispersion_pp"]["rango"] is None and res["verificacion"]["minimo_miembros_pct"] is None
    assert res["dispersion_pp"]["desviacion"] == pytest.approx(math.sqrt(10.0), rel=1e-12)
    assert any(x.startswith("sin mínimo, máximo ni rango de los miembros: menos de 7") for x in lim)
    d = _disc_siete()
    res, _ = _correr("FON-DISC-001", d)
    ult = np.array([m["precio"][-1] / m["nav"][-1] - 1 for m in d["miembros"].values()]) * 100
    assert res["dispersion_pp"]["rango"] == pytest.approx(float(np.ptp(ult)), rel=1e-12)
    assert res["verificacion"]["maximo_miembros_pct"] == pytest.approx(float(ult.max()), rel=1e-12)


def test_fon_disc_subcategoria_con_menos_miembros_que_el_minimo():
    d = _disc_siete()
    for i, m in enumerate(d["miembros"].values()):
        m["subcategoria"] = "inmobiliario" if i < 5 else "infraestructuras"
    res, lim = _correr("FON-DISC-001", d)
    assert res["desglose_subcategoria"]["inmobiliario"]["descuento_mediana_pct"] is not None
    assert res["desglose_subcategoria"]["infraestructuras"] == {"n": 2, "descuento_mediana_pct": None}
    assert any(x.startswith("1 subcategoría(s) con menos de 5 miembros") for x in lim)


def test_fon_td_segmento_con_menos_miembros_que_el_minimo():
    v, p = _caso("FON-TD-001", 1)
    res, lim = _correr("FON-TD-001", v, p)
    seg = res["segmentos"]["replicacion"]
    assert all(s["td_mediana_pb"] is None and s["diferencia_vs_categoria_pb"] is None for s in seg.values())
    assert sum(s["n"] for s in seg.values()) == 5
    assert any("agregado frágil; no calculado, sería la cifra de vehículos concretos (1.6)" in x for x in lim)
    for m in v["miembros"].values():
        m["replicacion"] = "fisica"
    res, _ = _correr("FON-TD-001", v, p)
    assert res["segmentos"]["replicacion"]["fisica"]["td_mediana_pb"] == pytest.approx(res["td_mediana_pb"])


# ====================================================================================================== casos de control
def test_casos_de_control_de_las_fichas_corregidas():
    m = servicio.Motor(Almacen(Path(tempfile.mkdtemp(prefix="t128_"))), _Proveedor(), cargar_config())
    res = m.verificar_casos_control(list(MODULO))
    assert all(x["superados"] for x in res.values()), res


def test_las_reglas_son_las_de_frontera_b_y_la_peticion_no_las_cambia():
    for f in ("REI-NAV-001", "REI-FFO-001"):
        assert {k: fr.UMBRALES[f][k] for k in fb.FRONTERA_B} == fb.FRONTERA_B
        v, p = _caso(f, 1)
        for clave in (*fb.FRONTERA_B, "componentes_minimos"):
            with pytest.raises(ErrorFicha, match="umbrales fijos"):
                _correr(f, v, {**p, clave: 1})
    assert fr.UMBRALES["REI-NAV-001"]["componentes_minimos_dispersion"] == 3
