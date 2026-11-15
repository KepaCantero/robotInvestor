"""T-128 r02 · Motor del Bloque A: hallazgos de la QA r01 de T-128 en la frontera con el Bloque B (1.6).

- H-01 (alta): una sociedad o un valor troceados (o con una perturbación simétrica) dan su cifra en una sola petición en
  REI-NAV-001, REI-FFO-001 e IDX-REB-001. La misma raíz que T-127 H-04: **límite declarado** (INC-T128-01 e INC-T127-01
  «Ronda r03», pregunta para T-57), con el aviso de `frontera_b._aviso_casi_clones` en REI-NAV-001. Las pruebas fijan el
  límite.
- H-02 (media): CHR-FLOW-001 servía la oferta y el crecimiento de una sola moneda estable. Ahora, al menos 2 monedas
  distintas por su crecimiento y ninguna (o grupo de copias) con más del 95 % de la oferta (si no, rechazo); el crecimiento
  que aporta casi entero una va a `null`. En la tabla de CA-1, IDX-CONC-001 tenía lo mismo en la amplitud y la contribución
  con un solo componente (o una que la aporta casi entera): van a `null`.
- H-03 (baja): declarado en INC-T128-01 (CHR-FLOW, PRV-CF y PRV-PME reciben flujos ya agregados).
"""
import copy
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.motor import fichas_mon_idx as fm
from bloque_a.motor import fichas_reales as fr
from bloque_a.motor import frontera_b as fb
from bloque_a.motor import servicio
from bloque_a.motor.operaciones import ErrorFicha

MODULO = {"REI-NAV-001": fr, "REI-FFO-001": fr, "CHR-FLOW-001": fr, "IDX-CONC-001": fm, "IDX-REB-001": fm}
AVISO = "aviso (1.6)"


class _Proveedor:
    as_of = None
    nombre = "pruebas-t128-r02"


def _correr(ficha, v, p=None, series=None):
    ent = {"valores": copy.deepcopy(v), "series": series or {}, "series_rol": {}}
    return MODULO[ficha].FICHAS[ficha]["fn"](ent, dict(p or {}))


def _caso(ficha, i=0):
    v = {}
    for d in MODULO[ficha].CASOS_CONTROL[ficha][i]["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    return v, dict(MODULO[ficha].CASOS_CONTROL[ficha][i]["parametros"])


def _serie(v, nombre):
    return pd.Series({pd.Timestamp(x["fecha"]): x["oferta"] for x in v["oferta_stablecoins"][nombre]}).sort_index()


def _crecimiento(s):
    return s.iloc[-1] / s[s.index <= s.index[-1] - pd.Timedelta(days=30)].iloc[-1] - 1


# ====================================================================================================== H-02 · CHR-FLOW-001
def test_h02_una_sola_moneda_estable_se_rechaza(tmp_path):
    """La vía «U» del revisor: el caso de control 0 con solo EURX. Rechazo (la oferta es una entrada obligatoria), sin citar
    la moneda."""
    v, p = _caso("CHR-FLOW-001")
    v["oferta_stablecoins"] = {"EURX": v["oferta_stablecoins"]["EURX"]}
    with pytest.raises(ErrorFicha, match=r"rechazo: 1 moneda\(s\) estable\(s\) distinta\(s\) por su crecimiento \(< 2\)") as e:
        _correr("CHR-FLOW-001", v, p)
    assert "EURX" not in str(e.value)
    m = servicio.Motor(Almacen(Path(tmp_path)), _Proveedor(), cargar_config())
    r = m.servir({"operacion": "CHR-FLOW-001", "datos": [{"valores": v}], "parametros": p}, "AG-21")
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "DATOS_INSUFICIENTES" and "EURX" not in r["detalle"]


def test_h02_dos_monedas_con_el_mismo_crecimiento_son_una():
    """EURX y una copia suya a escala (×0,8): sus crecimientos coinciden, son un grupo; se rechaza aunque sean dos."""
    v, p = _caso("CHR-FLOW-001")
    eur = v["oferta_stablecoins"]["EURX"]
    v["oferta_stablecoins"] = {"EURX": eur, "COPIA": [{**x, "oferta": x["oferta"] * 0.8} for x in eur]}
    with pytest.raises(ErrorFicha, match=r"rechazo: 1 moneda\(s\) estable\(s\) distinta\(s\)"):
        _correr("CHR-FLOW-001", v, p)


@pytest.mark.parametrize("escala,rechazo", [(1e-4, True), (0.051, True), (0.06, False)])
def test_h02_dominancia_de_la_oferta(escala, rechazo):
    """USDX con EURX a otra escala: con EURX al 0,01 % o al 5,1 % de USDX, USDX pasa del 95 % de la oferta y se rechaza;
    al 6 % (USDX, el 94,3 %) se sirve."""
    v, p = _caso("CHR-FLOW-001")
    usd = v["oferta_stablecoins"]["USDX"]
    eur = v["oferta_stablecoins"]["EURX"]
    k = escala * usd[-1]["oferta"] / eur[-1]["oferta"]
    v["oferta_stablecoins"]["EURX"] = [{**x, "oferta": x["oferta"] * k} for x in eur]
    if rechazo:
        with pytest.raises(ErrorFicha, match=r"rechazo: un componente pesa el 9\d\.\d+% de «oferta de stablecoins"):
            _correr("CHR-FLOW-001", v, p)
    else:
        res, _ = _correr("CHR-FLOW-001", v, p)
        tot = _serie(v, "USDX") + _serie(v, "EURX")
        assert res["crecimiento_stablecoins_pct"] == pytest.approx(_crecimiento(tot) * 100, rel=1e-12)


def test_h02_un_crecimiento_que_aporta_casi_entero_una_moneda_no_se_entrega():
    """USDX plana (crecimiento 0) y EURX creciendo: el crecimiento agregado lo aporta EURX entero; va a `null` con su
    limitación y la oferta y la razón se entregan."""
    v, p = _caso("CHR-FLOW-001")
    plano = v["oferta_stablecoins"]["USDX"][0]["oferta"]
    v["oferta_stablecoins"]["USDX"] = [{**x, "oferta": plano} for x in v["oferta_stablecoins"]["USDX"]]
    res, lim = _correr("CHR-FLOW-001", v, p)
    assert res["crecimiento_stablecoins_pct"] is None
    assert res["oferta_stablecoins"] == pytest.approx(plano + _serie(v, "EURX").iloc[-1], rel=1e-12)
    assert res["razon_stablecoins_capitalizacion_pct"] is not None
    assert any(x.startswith("sin el crecimiento de las stablecoins: más del 95%") for x in lim)


def test_h02_el_crecimiento_se_mide_desde_su_base():
    """USDX crece hasta 40 días antes del final y luego queda plana: en los 30 días del crecimiento lo aporta entero EURX
    (va a `null`), aunque desde el principio de la serie USDX haya crecido más."""
    v, p = _caso("CHR-FLOW-001")
    usd = v["oferta_stablecoins"]["USDX"]
    tope = len(usd) - 40
    v["oferta_stablecoins"]["USDX"] = [{**x, "oferta": 1e11 * (1 + 0.01 * min(i, tope))} for i, x in enumerate(usd)]
    res, lim = _correr("CHR-FLOW-001", v, p)
    assert res["crecimiento_stablecoins_pct"] is None
    assert any(x.startswith("sin el crecimiento de las stablecoins") for x in lim)


def test_h02_el_caso_de_control_no_cambia():
    v, p = _caso("CHR-FLOW-001")
    res, lim = _correr("CHR-FLOW-001", v, p)
    tot = _serie(v, "USDX") + _serie(v, "EURX")
    assert res["crecimiento_stablecoins_pct"] == pytest.approx(_crecimiento(tot) * 100, rel=1e-12)
    assert res["oferta_stablecoins"] == pytest.approx(tot.iloc[-1], rel=1e-12)
    assert not any("stablecoins" in x and "95%" in x for x in lim)


def test_h02_la_capitalizacion_se_valida_aunque_el_crecimiento_no_se_entregue():
    """Falla cerrado: con el crecimiento en `null`, una capitalización total posterior a la fecha de corte se sigue
    rechazando."""
    v, p = _caso("CHR-FLOW-001")
    plano = v["oferta_stablecoins"]["USDX"][0]["oferta"]
    v["oferta_stablecoins"]["USDX"] = [{**x, "oferta": plano} for x in v["oferta_stablecoins"]["USDX"]]
    v["capitalizacion_total"] = [{"fecha": "2026-12-01", "valor": 3e12}]
    ent = {"valores": v, "series": {}, "series_rol": {}, "fecha_corte": "2025-08-15"}
    with pytest.raises(ErrorFicha, match="capitalizacion_total"):
        fr.FICHAS["CHR-FLOW-001"]["fn"](ent, p)


def test_h02_las_reglas_de_chr_flow_son_umbrales_fijos():
    u = fr.UMBRALES["CHR-FLOW-001"]
    assert {k: u[k] for k in fb.FRONTERA_B} == fb.FRONTERA_B and u["monedas_estables_minimas"] == 2
    v, p = _caso("CHR-FLOW-001")
    for clave in (*fb.FRONTERA_B, "monedas_estables_minimas"):
        with pytest.raises(ErrorFicha, match="umbrales fijos"):
            _correr("CHR-FLOW-001", v, {**p, clave: 1})


# ====================================================================================================== H-02 · IDX-CONC-001
def _conc(n, rent=None, precios=None):
    comp = fm._composicion(n, igual=False)
    ini = {"fecha": "2025-10-31", "componentes": [{"id": c["id"], "peso": c["peso"]} for c in comp["componentes"]]}
    v = {"composicion": comp, "composicion_inicio": ini}
    if rent is not None:
        v["rentabilidades_periodo"] = dict(zip([c["id"] for c in comp["componentes"]], rent, strict=True))
    return v, precios


def test_h02_idx_conc_amplitud_y_contribucion_de_un_componente_no_se_entregan():
    fechas = pd.bdate_range("2025-06-02", periods=320)
    sube = pd.Series(np.linspace(100, 150, 320), index=fechas)
    v, _ = _conc(1, rent=[0.2])
    res, lim = _correr("IDX-CONC-001", v, {"top_n": 5}, series={"C00": sube})
    assert res["amplitud"] is None and res["contribucion"] is None
    assert res["peso_top_n"] == pytest.approx(1.0) and res["hhi"] == pytest.approx(1.0)   # la concentración no cambia
    assert any(x.startswith("amplitud no calculada: precios de 1 componente (< 2)") for x in lim)
    assert any(x.startswith("sin la contribución a la rentabilidad del índice") for x in lim)
    v, _ = _conc(1, rent=[0.0])                     # una rentabilidad nula tampoco: es la del componente
    res, _ = _correr("IDX-CONC-001", v, {"top_n": 5})
    assert res["contribucion"] is None


def test_h02_idx_conc_contribucion_dominada_no_se_entrega():
    v, _ = _conc(3, rent=[0.2, 1e-6, -1e-6])          # C00 aporta casi toda la rentabilidad del índice
    res, _ = _correr("IDX-CONC-001", v, {"top_n": 5})
    assert res["contribucion"] is None
    v, _ = _conc(3, rent=[0.2, -0.1, 0.05])           # el caso de `test_idx_conc_valores_a_mano`: se entrega
    res, _ = _correr("IDX-CONC-001", v, {"top_n": 5})
    pesos = [c["peso"] for c in v["composicion_inicio"]["componentes"]]
    assert res["contribucion"]["rentabilidad_indice"] == pytest.approx(float(np.dot(pesos, [0.2, -0.1, 0.05])), rel=1e-12)


def test_h02_idx_conc_porcentaje_sobre_la_media_de_un_solo_valido():
    """Dos componentes con precios y solo uno con 200 sesiones (el otro, semanal): el porcentaje sobre la media sería el
    suyo."""
    fechas = pd.bdate_range("2025-06-02", periods=320)
    largo = pd.Series(np.linspace(100, 150, 320), index=fechas)
    semanas = pd.date_range(end=fechas[-1], periods=60, freq="W-FRI")      # más de un año, menos de 200 sesiones
    corto = pd.Series(np.linspace(100, 90, 60), index=semanas)
    v, _ = _conc(2)
    res, lim = _correr("IDX-CONC-001", v, {"top_n": 5}, series={"C00": largo, "C01": corto})
    assert res["amplitud"]["porcentaje_sobre_media"] is None and res["amplitud"]["n_validos"] == 1
    assert any(x.startswith("porcentaje sobre la media no calculado: 1 componente") for x in lim)
    res, _ = _correr("IDX-CONC-001", v, {"top_n": 5}, series={"C00": largo, "C01": largo * 0.5})
    assert res["amplitud"]["porcentaje_sobre_media"] == pytest.approx(1.0)


# ====================================================================================================== H-01 · límite declarado
def _nav_simetrica():
    """REI-NAV-001: la sociedad A del caso de control 2 en dos partes con el mismo peso y NAV por acción 20/1,04 y 20/0,96
    (el ataque «S» del revisor)."""
    v, p = _caso("REI-NAV-001", 2)
    a = v["componentes"][0]
    partes = []
    for k, d in enumerate((0.04, -0.04)):
        c = copy.deepcopy(a)
        c["id"] = f"SOCIEDAD_SECRETA_{k}"
        c["acciones"] = a["acciones"] / 2
        c["nav_por_accion"] = a["nav_por_accion"] / (1 + d)
        c["deuda_neta"] = a["deuda_neta"] / 2
        c["otros_pasivos"] = a["otros_pasivos"] / 2
        c["gav"] = c["nav_por_accion"] * c["acciones"] + c["deuda_neta"] + c["otros_pasivos"]
        partes.append(c)
    v["componentes"] = partes
    return v, p, a


def test_h01_rei_nav_simetrica_se_sirve_con_aviso_y_es_el_limite_declarado():
    """La prima agregada es la de A (límite declarado, INC-T128-01); el aviso dice que las dos solo difieren en un dato
    (el GAV no cuenta: lo fija la identidad del balance) y no cita identificadores."""
    v, p, a = _nav_simetrica()
    res, lim = _correr("REI-NAV-001", v, p)
    assert res["prima_agregada_pct"] == pytest.approx((a["precio"] / a["nav_por_accion"] - 1) * 100, rel=1e-9)
    avisos = [x for x in lim if x.startswith(AVISO)]
    assert len(avisos) == 1 and avisos[0].startswith(f"{AVISO}: 2 componentes coinciden con otro en todos los datos")
    assert not any("SOCIEDAD_SECRETA" in x for x in lim)
    v["componentes"][1]["deuda_neta"] *= 1.5            # dos datos movidos: sin aviso (límite del aviso)
    v["componentes"][1]["gav"] += v["componentes"][1]["deuda_neta"] / 3
    res, lim = _correr("REI-NAV-001", v, p)
    assert not any(x.startswith(AVISO) for x in lim)


def test_h01_rei_nav_los_casos_de_control_no_dan_aviso():
    for i in range(len(fr.CASOS_CONTROL["REI-NAV-001"])):
        v, p = _caso("REI-NAV-001", i)
        try:
            _, lim = _correr("REI-NAV-001", v, p)
        except ErrorFicha:
            continue
        assert not any(x.startswith(AVISO) for x in lim), i


def test_h01_limite_declarado_rei_ffo_e_idx_reb_troceados_se_sirven():
    """REI-FFO-001 (X en dos partes con repartos distintos) e IDX-REB-001 (IN en IN-a e IN-b) siguen dando la cifra del
    entero: el límite declarado de INC-T128-01. Si falla porque se rechazan, actualizar la incidencia."""
    v, p = _caso("REI-FFO-001", 1)
    x = v["componentes"][0]
    sh = {"beneficio_neto": 0.2, "amortizaciones_inmobiliarias": 0.5, "plusvalias": 0.5, "capex_mantenimiento": 0.4,
          "ajuste_rentas_lineales": 0.5, "dividendo": 0.45, "rentas": 0.4}
    p1, p2 = copy.deepcopy(x), copy.deepcopy(x)
    p1["id"], p2["id"] = "X-1", "X-2"
    p1["acciones"], p2["acciones"] = x["acciones"] * 0.4, x["acciones"] * 0.6
    for e1, e2, e in zip(p1["ejercicios"], p2["ejercicios"], x["ejercicios"], strict=True):
        for q, s in sh.items():
            if e.get(q) is not None:
                e1[q], e2[q] = e[q] * s, e[q] * (1 - s)
    ult = max(x["ejercicios"], key=lambda e: e["ejercicio"])
    ffo = ult["beneficio_neto"] + ult["amortizaciones_inmobiliarias"] - ult["plusvalias"]
    v["componentes"] = [p1, p2]
    v.pop("historia_multiplos", None)
    res, _ = _correr("REI-FFO-001", v, p)
    assert res["p_ffo"] == pytest.approx(x["precio"] * x["acciones"] / ffo, rel=1e-9)

    v, p = _caso("IDX-REB-001", 0)
    aum = v["evento"]["activos_indexados"]["valor"]
    v["evento"]["cambios"] = [{"id": "IN-a", "delta_peso": 0.0007, "volumen_medio": 3e8},
                              {"id": "IN-b", "delta_peso": 0.0003, "volumen_medio": 2e8},
                              {"id": "OUT-a", "delta_peso": -0.0006, "volumen_medio": 1.0e8},
                              {"id": "OUT-b", "delta_peso": -0.0004, "volumen_medio": 1.0e8}]
    res, _ = _correr("IDX-REB-001", v, p)
    assert res["demanda_estimada"]["inclusiones"]["demanda"] == pytest.approx(0.001 * aum, rel=1e-9)


def test_casos_de_control_de_las_fichas_de_la_r02(tmp_path):
    m = servicio.Motor(Almacen(Path(tempfile.mkdtemp(prefix="t128r02_", dir=tmp_path))), _Proveedor(), cargar_config())
    res = m.verificar_casos_control(list(MODULO))
    assert all(x["superados"] for x in res.values()), res
