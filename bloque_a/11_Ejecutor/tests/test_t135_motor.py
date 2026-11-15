"""T-135 · Motor del Bloque A: hallazgos de las QA r03 de T-127 y r02 de T-128 en la frontera con el Bloque B (1.6).

- T-128 H-05 (media): IDX-CONC-001 daba la amplitud de un valor con una copia suya (exacta o a escala). Las series de precios
  se agrupan por sus rentabilidades (`frontera_b._etiquetas_series_copiadas`): un grupo de copias es un componente para el
  mínimo `IDX_CONC_COMPONENTES_MINIMOS` y para la dominancia (1, k).
- T-128 H-06 (baja): la dominancia por grupos de copias de CHR-FLOW-001 (`_sin_dominio(..., grupos)`) no tenía prueba.
- T-127 H-06 (baja): falsos avisos de CHR-TOKEN-001 con tokens de oferta fija y redonda. Las coincidencias triviales (``None``
  con ``None``, 0 con 0) no bastan para el aviso (`AVISO_B["coincidencias_informativas_minimas"]`), y la firma del aviso de
  la ficha deja en ``None`` lo que repite otro dato y lleva el staking y la concentración.
- T-127 H-07 (baja): REI-NAV-001 sin `otros_pasivos` y con un dato movido no daba aviso (el derivado se movía solo): la
  firma son los datos aportados.
- T-127 H-08 (baja): el docstring de `frontera_b` matiza la frase absoluta.
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
from bloque_a.motor import fichas_p2 as fp
from bloque_a.motor import fichas_reales as fr
from bloque_a.motor import frontera_b as fb
from bloque_a.motor import servicio
from bloque_a.motor.operaciones import ErrorFicha

MODULO = {"IDX-CONC-001": fm, "CHR-FLOW-001": fr, "REI-NAV-001": fr, "CHR-TOKEN-001": fp, "FIR-CRED-001": fp,
          "REI-LEV-001": fp}
AVISO = "aviso (1.6)"
FECHAS = pd.bdate_range("2025-06-02", periods=320)


class _Proveedor:
    as_of = None
    nombre = "pruebas-t135"


def _correr(ficha, v, p=None, series=None):
    ent = {"valores": copy.deepcopy(v), "series": series or {}, "series_rol": {}}
    return MODULO[ficha].FICHAS[ficha]["fn"](ent, dict(p or {}))


def _caso(ficha, i=0):
    v = {}
    for d in MODULO[ficha].CASOS_CONTROL[ficha][i]["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    return v, dict(MODULO[ficha].CASOS_CONTROL[ficha][i].get("parametros") or {})


def _avisos(lim):
    return [x for x in lim if x.startswith(AVISO)]


def _paseo(semilla, deriva=0.0):
    rng = np.random.default_rng(semilla)
    return pd.Series(100 * np.exp(np.cumsum(rng.normal(deriva, 0.01, len(FECHAS)))), index=FECHAS)


def _conc(n=10):
    return {"composicion": fm._composicion(n, igual=False)}


def _amplitud_a_mano(series):
    """Porcentaje sobre la media de 200 sesiones y línea avance–retroceso contando cada serie (método (ii))."""
    sobre = [float(s.iloc[-1] > s.iloc[-200:].mean()) for s in series]
    linea = sum(float(np.sign(s.pct_change().iloc[1:]).sum()) for s in series)
    return sum(sobre) / len(sobre), linea


# ====================================================================================================== T-128 H-05 · IDX-CONC
@pytest.mark.parametrize("copia", [lambda s: s.copy(), lambda s: s * 0.5, lambda s: s * 37.0,
                                   lambda s: s.iloc[40:] * 2.0],
                         ids=["exacta", "escala_0_5", "escala_37", "recortada_y_a_escala"])
def test_h05_un_valor_y_su_copia_no_dan_su_amplitud(copia):
    """La vía del revisor (bloque C de `r02_01`): C00 y una copia suya (exacta, a escala o recortada en el tiempo con más
    de un año) son un componente: la amplitud no se entrega y la limitación no cita identificadores."""
    x00 = _paseo(7, 0.0005)
    res, lim = _correr("IDX-CONC-001", _conc(), {"top_n": 5}, series={"C00": x00, "SECRETA": copia(x00)})
    assert res["amplitud"] is None
    assert any(x.startswith("1 componente(s) con las mismas rentabilidades que otro (a menos del 1%)") for x in lim)
    assert any(x.startswith("amplitud no calculada: precios de 1 componente (< 2) distinto por sus rentabilidades")
               for x in lim)
    assert not any("SECRETA" in x or "C00" in x for x in lim)


def test_h05_dos_valores_distintos_se_sirven_con_la_amplitud_a_mano():
    x00, x01 = _paseo(7, 0.0005), _paseo(8, -0.0005)
    res, lim = _correr("IDX-CONC-001", _conc(), {"top_n": 5}, series={"C00": x00, "C01": x01})
    pct, linea = _amplitud_a_mano([x00, x01])
    assert res["amplitud"]["porcentaje_sobre_media"] == pytest.approx(pct)
    assert res["amplitud"]["linea_avance_retroceso"] == pytest.approx(linea)
    assert not any("mismas rentabilidades" in x for x in lim)


def test_h05_con_un_valor_distinto_mas_las_copias_cuentan_cada_serie():
    """El grupo de copias es un componente para el mínimo, no para el cálculo: con C00, una copia y C01 hay 2 componentes
    distintos y la amplitud cuenta las tres series (como `test_idx_conc_valores_a_mano`, con X e Y iguales)."""
    x00, x01 = _paseo(7, 0.0005), _paseo(8, -0.0005)
    res, lim = _correr("IDX-CONC-001", _conc(), {"top_n": 5}, series={"C00": x00, "C00B": x00 * 3, "C01": x01})
    pct, linea = _amplitud_a_mano([x00, x00, x01])
    assert res["amplitud"]["porcentaje_sobre_media"] == pytest.approx(pct)
    assert res["amplitud"]["linea_avance_retroceso"] == pytest.approx(linea)
    assert any(x.startswith("1 componente(s) con las mismas rentabilidades") for x in lim)


@pytest.mark.parametrize("grupo,servida", [(19, True), (20, False)])
def test_h05_dominancia_de_un_grupo_de_copias(grupo, servida):
    """Regla (1, k) con el mismo peso por serie: C00 y 18 copias (un grupo de 19) con C01 son el 95 % de 20 series (se
    sirve); un grupo de 20 con C01, el 95,2 % de 21 (más del 95 %: la amplitud sería la de C00)."""
    x00, x01 = _paseo(7, 0.0005), _paseo(8, -0.0005)
    series = {"C01": x01, **{f"K{j:02d}": x00 * (1 + j) for j in range(grupo)}}
    res, lim = _correr("IDX-CONC-001", _conc(), {"top_n": 5}, series=series)
    if servida:
        assert res["amplitud"] is not None
    else:
        assert res["amplitud"] is None
        assert any(x.startswith("amplitud no calculada: un componente y sus copias son el 95.2% de las series (más del "
                                "95%)") for x in lim)


def test_h05_el_porcentaje_cuenta_los_validos_distintos():
    """C00 y su copia con 320 sesiones y C01 semanal (menos de 200 sesiones): la amplitud se sirve (2 distintos), pero el
    porcentaje sobre la media sería el de C00 (1 distinto entre los válidos): `null`."""
    x00 = _paseo(7, 0.0005)
    semanas = pd.date_range(end=FECHAS[-1], periods=60, freq="W-FRI")
    corto = pd.Series(np.linspace(100, 90, 60), index=semanas)
    res, lim = _correr("IDX-CONC-001", _conc(), {"top_n": 5}, series={"C00": x00, "C00B": x00 * 0.25, "C01": corto})
    assert res["amplitud"] is not None and res["amplitud"]["n_validos"] == 2
    assert res["amplitud"]["porcentaje_sobre_media"] is None
    assert any(x.startswith("porcentaje sobre la media no calculado: 1 componente con 200 sesiones (< 2) distinto")
               for x in lim)
    # dominancia entre los válidos: 20 copias válidas de C00 y C01 válida, con una serie corta más que no cuenta
    series = {"C01": _paseo(8), "CORTA": corto, **{f"K{j:02d}": x00 * (1 + j) for j in range(21)}}
    series["C02"] = _paseo(9)
    res, lim = _correr("IDX-CONC-001", _conc(), {"top_n": 5}, series=series)
    assert res["amplitud"] is not None and res["amplitud"]["porcentaje_sobre_media"] is not None   # 21/23 = 91,3 %
    del series["C02"]
    series["CORTA2"] = corto * 2.5          # copia de la corta: no cambia los válidos; 21 de 22 válidos son copias de C00
    res, lim = _correr("IDX-CONC-001", _conc(), {"top_n": 5}, series=series)
    assert res["amplitud"] is not None and res["amplitud"]["porcentaje_sobre_media"] is None
    assert any(x.startswith("porcentaje sobre la media no calculado: un componente y sus copias son el 95.5%") for x in lim)


def test_h05_la_concentracion_no_cambia():
    """La ficha mide la concentración (peso de los n mayores, HHI, N_ef): las copias en los precios no la tocan."""
    x00 = _paseo(7)
    con, _ = _correr("IDX-CONC-001", _conc(), {"top_n": 5}, series={"C00": x00, "C01": x00 * 2})
    sin, _ = _correr("IDX-CONC-001", _conc(), {"top_n": 5})
    assert {k: con[k] for k in ("peso_top_n", "hhi", "n_ef", "hhi_sectorial", "n_componentes")} == \
        {k: sin[k] for k in ("peso_top_n", "hhi", "n_ef", "hhi_sectorial", "n_componentes")}


def test_h05_la_peticion_no_cambia_la_regla():
    """`anios_precios_min` es un umbral fijo (se rechaza en la petición); `tolerancia_clon` y `peso_maximo_componente` no
    son parámetros de IDX-CONC-001 y la ficha los lee de `FRONTERA_B`: en la petición no cambian nada."""
    x00 = _paseo(7)
    with pytest.raises(ErrorFicha, match="umbrales fijos"):
        _correr("IDX-CONC-001", _conc(), {"top_n": 5, "anios_precios_min": 0}, series={"C00": x00, "C01": x00 * 2})
    for clave, valor in (("tolerancia_clon", 0.0), ("peso_maximo_componente", 1.0)):
        try:
            res, _ = _correr("IDX-CONC-001", _conc(), {"top_n": 5, clave: valor}, series={"C00": x00, "C01": x00 * 2})
        except ErrorFicha:
            continue
        assert res["amplitud"] is None, clave


def test_h05_etiquetas_de_series_copiadas():
    """La regla, a mano: rentabilidades a menos del 1 % relativo en cada fecha común, durante al menos el año mínimo;
    cierre transitivo; una serie sin fechas comunes con otra no es su copia."""
    et = fb._etiquetas_series_copiadas
    anios = np.arange(5) / 2.0                                    # 0; 0,5; 1; 1,5; 2 años
    # T-144 (QA r01 de T-135, H-01): precios sin redondear (con un factor de muchos decimales). Con los enteros de antes, la
    # serie tiene paso 1 (0,5 % de redondeo a 100) y la regla nueva de niveles toma por copia a «lejos», que a esa
    # resolución lo es; esta prueba fija la regla de las rentabilidades, que no cambia (la de niveles, en test_t144.py)
    base = np.array([100.0, 110.0, 99.0, 120.0, 108.0]) * 1.0123456789
    r = base[1:] / base[:-1] - 1
    casi = np.concatenate([[50.0], 50.0 * np.cumprod(1 + r * 1.0099)])     # cada rentabilidad, a menos del 1 %
    lejos = np.concatenate([[50.0], 50.0 * np.cumprod(1 + r * 1.0102)])    # una ya pasa del 1 %
    assert et(np.vstack([base, casi]), anios, 0.01, 1.0).tolist() == [0, 0]
    # la tolerancia es relativa al mayor de los dos (la de `_datos_que_coinciden`): un 1,005 % del menor aún es copia
    borde = np.concatenate([[50.0], 50.0 * np.cumprod(1 + r * 1.01005)])
    assert et(np.vstack([base, borde]), anios, 0.01, 1.0).tolist() == [0, 0]
    assert len(set(et(np.vstack([base, lejos]), anios, 0.01, 1.0).tolist())) == 2
    corta = np.array([np.nan, np.nan, np.nan, 120.0, 108.0])          # 0,5 años en común (< 1): no es copia
    assert len(set(et(np.vstack([base, corta]), anios, 0.01, 1.0).tolist())) == 2
    media = np.array([np.nan, np.nan, 99.0, 120.0, 108.0]) * 3        # 1 año en común: copia recortada
    assert et(np.vstack([base, media]), anios, 0.01, 1.0).tolist() == [0, 0]
    sin_comun = np.array([np.nan, np.nan, np.nan, np.nan, 7.0])
    assert len(set(et(np.vstack([base[:4].tolist() + [np.nan], sin_comun]), anios, 0.01, 0.0).tolist())) == 2
    # cadena: A ~ B (fechas 0–2) y B ~ C (fechas 2–4) con A y C sin fechas comunes suficientes
    a = np.array([100.0, 110.0, 99.0, np.nan, np.nan])
    b = base * 2
    c = np.array([np.nan, np.nan, 99.0, 120.0, 108.0])
    assert et(np.vstack([a, b, c]), anios, 0.01, 1.0).tolist() == [0, 0, 0]
    assert et(np.zeros((0, 5)), anios, 0.01, 1.0).tolist() == []
    assert et(base[None, :], anios, 0.01, 1.0).tolist() == [0]


# ====================================================================================================== T-128 H-06 · CHR-FLOW
def test_h06_chr_flow_dominancia_de_un_grupo_de_copias():
    """USDX al 4 % de la oferta y EURX en dos copias a escala del 48 % cada una: ninguna moneda pasa del 95 %, pero el grupo
    de copias (el mismo crecimiento) es el 96 %: rechazo. Mata el mutante que quita `grupos` de `_sin_dominio` (sin grupos
    se serviría con el crecimiento a `null`). Con la segunda moneda de crecimiento distinto, se sirve."""
    v, p = _caso("CHR-FLOW-001")
    usd, eur = v["oferta_stablecoins"]["USDX"], v["oferta_stablecoins"]["EURX"]
    k = 0.48 / 0.04 * usd[-1]["oferta"] / eur[-1]["oferta"]
    v["oferta_stablecoins"] = {"USDX": usd, "EUR_A": [{**x, "oferta": x["oferta"] * k} for x in eur],
                               "EUR_B": [{**x, "oferta": x["oferta"] * k} for x in eur]}
    with pytest.raises(ErrorFicha, match=r"rechazo: un componente pesa el 96\.0+% de «oferta de stablecoins") as e:
        _correr("CHR-FLOW-001", v, p)
    assert "EUR_" not in str(e.value) and "USDX" not in str(e.value)
    n = len(eur)
    v["oferta_stablecoins"]["EUR_B"] = [{**x, "oferta": x["oferta"] * k * (1 + 0.05 * i / n)} for i, x in enumerate(eur)]
    res, _ = _correr("CHR-FLOW-001", v, p)
    assert res["oferta_stablecoins"] > 0


# ====================================================================================================== T-127 H-06 · CHR-TOKEN
def _tokens_fijos(staking=True):
    """El caso del revisor (bloque A3 de `r03_01`): el caso de control 1 con dos tokens más de oferta fija y redonda, toda en
    circulación, sin emisión ni quema, precios 0,42 y 7,9."""
    v, p = _caso("CHR-TOKEN-001", 1)
    base = v["tokens"][0]
    for j, (precio, st, co) in enumerate(((0.42, 0.031, 0.22), (7.9, 0.047, 0.41))):
        t = copy.deepcopy(base)
        t.update(id=f"GOB{j}", precio=precio, oferta_circulante=1e9, oferta_total=1e9, oferta_maxima=1e9,
                 emision_anual=0.0, quema_anual=0.0, staking_nominal=st, concentracion_10_mayores=co)
        if not staking:
            t.pop("staking_nominal")
            t.pop("concentracion_10_mayores")
        t["calendario"] = {"fuente": "documentación del proyecto", "desbloqueos": []}
        v["tokens"].append(t)
    return v, p


@pytest.mark.parametrize("staking", [True, False])
def test_h06_dos_tokens_de_oferta_fija_y_redonda_no_dan_aviso(staking):
    """Con su staking y su concentración (el caso del revisor) o sin ellos (``None``): las coincidencias que quedan son
    triviales (0 con 0, ``None`` con ``None``) o repiten la oferta circulante (total y máxima): sin aviso."""
    v, p = _tokens_fijos(staking)
    _, lim = _correr("CHR-TOKEN-001", v, p)
    assert _avisos(lim) == []


@pytest.mark.parametrize("campo,factor", [("emision_anual", 1.3), ("quema_anual", 1.3), ("staking_nominal", 1.2),
                                          ("concentracion_10_mayores", 1.2)])
def test_h06_una_copia_con_un_dato_movido_sigue_dando_aviso(campo, factor):
    """Los casos del revisor (`test_t127_r03.py::test_h04_aviso_en_rei_lev_y_chr_token`) y los datos nuevos de la firma:
    una copia de TKB con un dato movido da el aviso."""
    v, p = _caso("CHR-TOKEN-001", 1)
    otro = copy.deepcopy(v["tokens"][-1])
    otro["id"] = "COPIA_SECRETA"
    otro[campo] = otro[campo] * factor
    v["tokens"].append(otro)
    if campo in ("staking_nominal", "concentracion_10_mayores"):
        # no están en los datos de los casi clones: la copia coincide en todos ellos y se rechaza (más que un aviso)
        with pytest.raises(ErrorFicha, match="con los mismos datos que otro"):
            _correr("CHR-TOKEN-001", v, p)
        return
    _, lim = _correr("CHR-TOKEN-001", v, p)
    assert len(_avisos(lim)) == 1 and _avisos(lim)[0].startswith(f"{AVISO}: 2 componentes coinciden con otro")
    assert not any("COPIA_SECRETA" in x for x in lim)


def test_h06_el_staking_distingue_a_dos_tokens_con_la_misma_concentracion():
    """Los dos tokens del revisor con la misma concentración (0,3) y distinto staking: difieren en el precio y el staking,
    dos datos; sin aviso (el staking está en la firma del aviso)."""
    v, p = _tokens_fijos(True)
    for t in v["tokens"][-2:]:
        t["concentracion_10_mayores"] = 0.3
    _, lim = _correr("CHR-TOKEN-001", v, p)
    assert _avisos(lim) == []


def test_h06_copia_de_un_token_fijo_con_el_precio_movido_y_su_staking():
    """Un token de oferta fija y entera en circulación copiado con otro precio, con su staking y su concentración: coincide en
    tres datos informativos (oferta, staking y concentración) y da el aviso."""
    v, p = _tokens_fijos(True)
    v["tokens"][-1].update(staking_nominal=0.031, concentracion_10_mayores=0.22)
    _, lim = _correr("CHR-TOKEN-001", v, p)
    assert len(_avisos(lim)) == 1 and _avisos(lim)[0].startswith(f"{AVISO}: 2 componentes coinciden con otro")


def test_h06_coincidencias_triviales_no_bastan():
    aviso = fb._aviso_casi_clones
    assert aviso([(1.0, 0.0, None), (2.0, 0.0, None)], 0.01, []) == 0            # solo coinciden 0 y None
    assert aviso([(1.0, 5.0, None), (2.0, 5.0, None)], 0.01, []) == 0            # 1 informativa (< 2)
    assert aviso([(1.0, 5.0, 7.0, None), (2.0, 5.0, 7.0, None)], 0.01, []) == 2  # 2 informativas
    assert aviso([(1.0, 5.0, 7.0, 0.0), (2.0, 5.0, 7.0, None)], 0.01, []) == 0   # 0 frente a None: otro dato distinto
    assert aviso([(5.0, 7.0, 0.0), (5.0, 7.0, 3.0)], 0.01, []) == 2              # el dato movido desde 0 no es trivial
    assert fb.AVISO_B["coincidencias_informativas_minimas"] == fb.AVISO_B["datos_distintos_aviso"] + 1


# ====================================================================================================== T-127 H-07 · REI-NAV
def _nav_sin_otros(d=0.04, quitar=True):
    """El caso del revisor (bloque A4 de `r03_01`): la sociedad A del caso 2 en dos partes con el NAV por acción ±4 % y sin
    `otros_pasivos`."""
    v, p = _caso("REI-NAV-001", 2)
    a = v["componentes"][0]
    partes = []
    for j, s in enumerate((d, -d)):
        c = copy.deepcopy(a)
        c.update(id=f"SOCIEDAD_SECRETA_{j}", acciones=a["acciones"] / 2, nav_por_accion=a["nav_por_accion"] / (1 + s),
                 deuda_neta=a["deuda_neta"] / 2, gav=a["gav"] / 2)
        if quitar:
            c.pop("otros_pasivos", None)
        else:
            c["otros_pasivos"] = a["otros_pasivos"] / 2
            c["gav"] = c["nav_por_accion"] * c["acciones"] + c["deuda_neta"] + c["otros_pasivos"]
        partes.append(c)
    v["componentes"] = partes
    return v, p, a


@pytest.mark.parametrize("quitar", [True, False])
def test_h07_rei_nav_un_dato_movido_da_aviso_con_o_sin_otros_pasivos(quitar):
    v, p, a = _nav_sin_otros(quitar=quitar)
    res, lim = _correr("REI-NAV-001", v, p)
    assert res["prima_agregada_pct"] == pytest.approx((a["precio"] / a["nav_por_accion"] - 1) * 100, rel=1e-9)  # límite
    assert len(_avisos(lim)) == 1 and _avisos(lim)[0].startswith(f"{AVISO}: 2 componentes coinciden con otro")
    assert not any("SOCIEDAD_SECRETA" in x for x in lim)


def test_h07_rei_nav_sin_otros_pasivos_con_dos_datos_movidos_no_da_aviso():
    """Límite del aviso: el NAV por acción y el GAV (el dato aportado cuando `otros_pasivos` se deriva) movidos."""
    v, p, _ = _nav_sin_otros()
    v["componentes"][1]["gav"] *= 1.05
    _, lim = _correr("REI-NAV-001", v, p)
    assert _avisos(lim) == []


def test_h07_rei_nav_sociedades_distintas_sin_otros_pasivos_no_dan_aviso():
    for i in range(len(fr.CASOS_CONTROL["REI-NAV-001"])):
        v, p = _caso("REI-NAV-001", i)
        for c in v.get("componentes") or []:
            c.pop("otros_pasivos", None)
        try:
            _, lim = _correr("REI-NAV-001", v, p)
        except ErrorFicha:
            continue
        assert _avisos(lim) == [], i


# ====================================================================================================== T-127 H-08 · docstring
def test_h08_el_docstring_de_frontera_b_no_es_absoluto():
    primera = fb.__doc__.split("\n\n")[1]
    assert "salvo que quien pide haya construido los componentes para ello" in " ".join(primera.split())


# ====================================================================================================== casos de control
def test_casos_de_control_no_cambian_ni_dan_aviso(tmp_path):
    m = servicio.Motor(Almacen(Path(tempfile.mkdtemp(prefix="t135_", dir=tmp_path))), _Proveedor(), cargar_config())
    res = m.verificar_casos_control()
    assert len(res) == 67 and all(x["superados"] for x in res.values()), res
    rc = [e for e in m.almacen.leer("RC") if any(str(x).startswith(AVISO) for x in e.get("limitaciones") or [])]
    assert rc == []
