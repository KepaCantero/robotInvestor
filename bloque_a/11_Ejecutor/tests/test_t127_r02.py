"""T-127 r02 · Motor del Bloque A: hallazgos de la QA r01 de T-127 en la frontera con el Bloque B (1.6).

- H-01: copias a escala de un emisor (todos sus importes por 1,02^i) daban su cifra exacta. Las cifras individuales que la
  ficha agrega no dependen de la escala: los componentes con las mismas cifras a menos del 1 % son un solo componente para
  el mínimo, la dominancia, los estadísticos de orden y los subconjuntos (`fichas_p2._sin_copias_a_escala`).
- H-02: rellenos de cifra nula daban la de un emisor (la media ponderada dividida por su peso). La dominancia (1, k) se
  aplica también a la aportación a cada cifra agregada (`fichas_p2._aportacion_maxima`): en FIR-CRED-001 y en los cocientes
  principales de REI-LEV-001 se rechaza; los vencimientos y su impacto en FFO y las cifras de CHR-TOKEN-001 van a `null`.
- H-03 (declarado): con 7 componentes o más, el mínimo y el máximo (y la mediana con n impar) son la cifra de un componente,
  sin identificarlo.
Detalle y decisiones: INC-T127-01 («Ronda r02»).
"""
import copy
import math

import numpy as np
import pytest
from bloque_a.motor import fichas_p2 as fp
from bloque_a.motor.operaciones import ErrorFicha
from test_t127_hallazgos import (
    LEV_CAMPOS,
    TOKEN_CAMPOS,
    _caso,
    _correr,
    _escala,
    _lev_extra,
    _motor,
    _peticion,
    _token_extra,
)

COPIAS = "componentes distintos por sus cifras individuales"
APORTA = "lo aporta un componente"


def _lev_a_escala(c, k, ident):
    c = _escala(c, k, LEV_CAMPOS, ident)
    c["vencimientos"] = [{**x, "importe": x["importe"] * k} for x in c["vencimientos"]]
    return c


def _token_a_escala(t, k, ident):
    t = _escala(t, k, tuple(q for q in TOKEN_CAMPOS if q != "precio" and t.get(q) is not None), ident)
    t["calendario"] = {**t["calendario"], "desbloqueos": [{**d, "cantidad": d["cantidad"] * k}
                                                         for d in t["calendario"]["desbloqueos"]]}
    return t


def _fir_a_escala(c, k, ident):
    return _escala(c, k, ("capitalizacion", "deuda_corto", "deuda_largo"), ident)


def _rechazo_sin_ids(ficha, v, p, motivo, ids, tmp_path):
    with pytest.raises(ErrorFicha, match=motivo) as e:
        _correr(ficha, v, p)
    assert not any(i in str(e.value) for i in ids)
    r = _motor(tmp_path).servir(_peticion(ficha, 1, v, p), "AG-21")
    assert r["estado"] == "RECHAZADO" and not any(i in r["detalle"] for i in ids)


# ====================================================================================================== H-01 · copias a escala
@pytest.mark.parametrize("ficha,n", [("FIR-CRED-001", 10), ("FIR-CRED-001", 12), ("REI-LEV-001", 3), ("REI-LEV-001", 7),
                                     ("CHR-TOKEN-001", 2), ("CHR-TOKEN-001", 7)])
def test_h01_copias_a_escala_de_un_emisor_se_rechazan(ficha, n, tmp_path):
    """El ataque del revisor (`r01_01`, vías «E»): el emisor repetido con todos sus importes por 1,02^i (difieren un 2 %,
    más que la tolerancia de clon, pero sus cocientes son los mismos)."""
    v, p = _caso(ficha, 1)
    if ficha == "FIR-CRED-001":
        base = v["componentes"][11]
        v["componentes"] = [_fir_a_escala(base, 1.02 ** i, f"EMISOR_SECRETO_{i}") for i in range(n)]
    elif ficha == "REI-LEV-001":
        base = v["componentes"][0]
        v["componentes"] = [_lev_a_escala(base, 1.02 ** i, f"EMISOR_SECRETO_{i}") for i in range(n)]
    else:
        base = v["tokens"][0]
        v["tokens"] = [_token_a_escala(base, 1.02 ** i, f"EMISOR_SECRETO_{i}") for i in range(n)]
    _rechazo_sin_ids(ficha, v, p, rf"rechazo: 1 {COPIAS} \(< \d+\): {n - 1} tienen las mismas cifras", ["EMISOR_SECRETO"],
                     tmp_path)


def test_h01_las_copias_se_comparan_por_sus_cifras_no_por_sus_datos():
    """FIR-CRED-001: diez emisores con la misma capitalización, volatilidad y punto de impago (corto + ½ largo) y distinto
    reparto de la deuda: sus datos difieren más del 1 % (no son casi clones), pero sus cifras son las mismas."""
    v, p = _caso("FIR-CRED-001", 1)
    base = v["componentes"][11]
    D = base["deuda_corto"] + 0.5 * base["deuda_largo"]
    comps = []
    for i in range(10):
        corto = D * (0.1 + 0.08 * i)
        comps.append({**base, "id": f"R{i}", "deuda_corto": corto, "deuda_largo": 2 * (D - corto)})
    v["componentes"] = comps
    with pytest.raises(ErrorFicha, match=rf"rechazo: 1 {COPIAS}"):
        _correr("FIR-CRED-001", v, p)


def test_h01_la_tolerancia_de_las_cifras_es_la_de_clon():
    """|a − b| ≤ 1 %·max(|a|, |b|) en cada cifra, con cierre transitivo; una cifra ausente solo es igual a otra ausente."""
    s = fp._sin_copias_a_escala
    with pytest.raises(ErrorFicha, match=rf"1 {COPIAS} \(< 2\)"):
        s([(1.0, 2.0), (1.01, 2.0)], "prueba", 2, 0.01)
    assert list(s([(1.0, 2.0), (1.0102, 2.0)], "prueba", 2, 0.01)) == [0, 1]
    assert list(s([(1.0, None), (1.0, 0.0)], "prueba", 2, 0.01)) == [0, 1]
    assert len(set(s([(1.0,), (1.008,), (1.016,), (5.0,)], "prueba", 2, 0.01).tolist())) == 2   # una cadena es un grupo


def test_h01_un_grupo_de_copias_es_un_componente_para_la_dominancia():
    """REI-LEV-001: S1 y 30 copias suyas a escala (3 componentes distintos, ninguno con más del 95 % de su base por sí
    solo) pesan juntas el 97,7 % del GAV."""
    v, p = _caso("REI-LEV-001", 1)
    v["componentes"] += [_lev_a_escala(v["componentes"][0], 1.02 ** (i + 1), f"Z{i}") for i in range(30)]
    with pytest.raises(ErrorFicha, match=r"rechazo: un componente pesa el 97\.\d+% de «gav»"):
        _correr("REI-LEV-001", v, p)
    f, pf = _caso("FIR-CRED-001", 1)                                         # 12 emisores y 80 copias de C11
    f["componentes"] += [_fir_a_escala(f["componentes"][11], 1.02 ** (i + 1), f"Z{i}") for i in range(80)]
    with pytest.raises(ErrorFicha, match=r"rechazo: un componente pesa el 9\d\.\d+% de «deuda»"):
        _correr("FIR-CRED-001", f, pf)
    with pytest.raises(ErrorFicha, match="de «deuda»"):
        fp._sin_dominio({"deuda": [10.0, 10.0, 1.0]}, "prueba", 0.95, np.array([0, 0, 1]))
    fp._sin_dominio({"deuda": [10.0, 10.0, 1.0]}, "prueba", 0.95)                       # sin grupos: cada uno el suyo


def test_h01_una_copia_que_no_domina_cuenta_una_vez():
    """Con S1 copiado a otra escala (1,0102: no es casi clon) hay 3 componentes distintos, no 4: se sirve, pero la
    dispersión empieza en 7 distintos (con 7 componentes y una copia, no hay)."""
    v, p = _caso("REI-LEV-001", 1)
    v["componentes"].append(_lev_a_escala(v["componentes"][0], 1.0102, "S9"))
    assert _correr("REI-LEV-001", v, p)[0]["n_componentes"] == 4
    v, p = _caso("REI-LEV-001", 1)
    v["componentes"] += _lev_extra(3) + [_lev_a_escala(v["componentes"][0], 1.5, "S9")]
    res, lim = _correr("REI-LEV-001", v, p)
    assert res["n_componentes"] == 7 and res["dispersion"] is None and res["covenants"]["holgura_ltv_pp"] is None
    assert any("menos de 7 componentes distintos" in x for x in lim)
    v["componentes"] += _lev_extra(4)[3:]
    res, _ = _correr("REI-LEV-001", v, p)
    assert res["n_componentes"] == 8 and res["dispersion"] is not None and res["covenants"]["holgura_ltv_pp"] is not None


def test_h01_los_subconjuntos_cuentan_componentes_distintos_por_sus_cifras():
    v, p = _caso("REI-LEV-001", 1)
    v["componentes"][2].pop("covenants")
    v["componentes"].append(_lev_a_escala(v["componentes"][0], 1.5, "S9"))                 # S1, S2 y la copia de S1
    res, lim = _correr("REI-LEV-001", v, p)
    assert res["covenants"] is None
    assert "covenants de 3 de 4 componentes, 2 distintos por sus cifras (< 3): holgura no calculada; con tan pocos serían " \
           "las cifras de emisores concretos (1.6)" in lim
    t, q = _caso("CHR-TOKEN-001", 1)
    t["tokens"][1].pop("staking_nominal")
    t["tokens"] += _token_extra(1) + [_token_a_escala(t["tokens"][0], 1.5, "TKZ")]   # staking: TKA y su copia
    res, lim = _correr("CHR-TOKEN-001", t, q)
    assert res["rendimiento_real_staking_pct"] is None and res["concentracion_10_mayores_pct"] is not None
    assert any(x.startswith("rendimiento de staking de 2 de 4 tokens, con menos de 2") for x in lim)


def test_h01_la_red_propia_no_cuenta_copias():
    v, p = _caso("CHR-TOKEN-001", 1)
    res, lim = _correr("CHR-TOKEN-001", {**v, "ambito": "Bitcoin", "ambito_es_red": True,
                                         "tokens": [{**v["tokens"][0], "id": "BTC"}]}, p)
    assert res["n_tokens"] == 1 and res["inflacion_neta_pct_anual"] == pytest.approx(5.0)
    assert not any("lo aporta" in x for x in lim)


# ====================================================================================================== H-01 · copias parciales
def test_h01_copias_que_solo_comparten_una_cifra_no_la_dan():
    """Copias que comparten solo la cifra buscada (las demás distintas): no son un grupo, pero la aportación a esa cifra es
    toda de componentes con la misma (H-02)."""
    v, p = _caso("REI-LEV-001", 1)
    s1 = v["componentes"][0]
    copias = []
    for i in range(3):                                                       # el LTV de S1, con otro EBITDA y otro FFO
        c = _lev_a_escala(s1, 1.02 ** i, f"L{i}")
        c["ebitda"] *= 1 + 0.2 * i
        c["ffo"] *= 1 + 0.3 * i
        copias.append(c)
    v["componentes"] = copias
    with pytest.raises(ErrorFicha, match=rf"rechazo: más del 95% de el LTV.* {APORTA}"):
        _correr("REI-LEV-001", v, p)
    t, q = _caso("CHR-TOKEN-001", 1)
    tka = t["tokens"][0]
    t["tokens"] = []
    for i in range(3):                                                       # la inflación y los desbloqueos de TKA
        x = _token_a_escala(tka, 1.02 ** i, f"T{i}")
        x["oferta_maxima"] = x["oferta_total"] * (1 + 0.2 * (i + 1))
        x["staking_nominal"] = 0.06 + 0.03 * i
        x["concentracion_10_mayores"] = 0.2 + 0.1 * i
        t["tokens"].append(x)
    res, lim = _correr("CHR-TOKEN-001", t, q)
    assert res["inflacion_neta_pct_anual"] is None and set(res["desbloqueos_pct"].values()) == {None}
    assert res["fdv_sobre_capitalizacion_veces"] is not None
    assert any(x.startswith("sin la inflación neta, los desbloqueos a 30 días, los desbloqueos a 90 días: más del 95% "
                            "lo aporta un componente") for x in lim)


# ====================================================================================================== H-02 · rellenos nulos
@pytest.mark.parametrize("peso", [0.30, 0.60])
def test_h02_rellenos_de_pd_nula_se_rechazan(peso, tmp_path):
    """El ataque del revisor (`r01_01`, vía «Z»): C11 con el 30 % o el 60 % de la deuda y nueve rellenos de PD 0."""
    v, p = _caso("FIR-CRED-001", 1)
    cx = v["componentes"][11]
    dX = cx["deuda_corto"] + cx["deuda_largo"]
    resto = dX * (1 - peso) / peso
    reparto = [1 + 0.05 * i for i in range(9)]
    v["componentes"] = [cx] + [{"id": f"Z{i}", "capitalizacion": 1e6 * (1 + 0.1 * i), "volatilidad_acciones": 0.05 + 0.01 * i,
                                "deuda_corto": resto * reparto[i] / sum(reparto), "deuda_largo": 0.0, "mu_historico": 0.05}
                               for i in range(9)]
    _rechazo_sin_ids("FIR-CRED-001", v, p, rf"rechazo: más del 95% de .*la PD media.* {APORTA}", ["C11", "Z0"], tmp_path)
    with pytest.raises(ErrorFicha, match="la PD real media"):
        _correr("FIR-CRED-001", v, p)


def test_h02_rellenos_de_deuda_neta_nula_se_rechazan():
    v, p = _caso("REI-LEV-001", 1)
    for c in v["componentes"][1:]:
        c["caja"] = c["deuda"]                                               # deuda neta 0: su LTV es 0
    with pytest.raises(ErrorFicha, match=rf"más del 95% de el LTV, la deuda neta/EBITDA {APORTA}"):
        _correr("REI-LEV-001", v, p)
    v["componentes"][1]["caja"] = 0.0                                        # S2 vuelve a aportar: se sirve
    assert _correr("REI-LEV-001", v, p)[0]["ltv_pct"] is not None


def test_h02_borde_de_la_aportacion():
    a = fp._aportacion_maxima
    assert a([19.0, 1.0], [1.0, 1.0], 0.01, 0.0) == pytest.approx(0.95)            # 95 % justo: no pasa de 0,95
    assert a([19.002, 0.998], [1.0, 1.0], 0.01, 0.0) > 0.95
    assert a([5.0, 5.0, 0.4], [1.0, 1.0, 1.0], 0.01, 0.0) == pytest.approx(10 / 10.4)  # la misma cifra: un vecindario
    assert a([5.0, 5.0, 0.4], [1.0, 1.02, 1.0], 0.01, 0.0) == pytest.approx(5 / 10.4)  # a más del 1 %: cada uno el suyo
    assert a([-3.0, 1.0], [1.0, 1.0], 0.01, 0.0) == pytest.approx(0.75)            # en valor absoluto
    assert a([0.0, 0.0], [1.0, 1.0], 0.01, 0.0) == 0.0                              # un agregado nulo no es de nadie
    assert a([1e-9, 1e-30], [1.0, 1.0], 0.01, 1e-6) == 0.0                          # ni uno nulo a la tolerancia
    assert a([1e-9, 1e-30], [1.0, 1.0], 0.01, 0.0) > 0.99
    assert a([1.0, 1.0], [0.0, 1.0], 0.01, 0.0) == pytest.approx(0.5)              # sin cifra (÷ 0): solo el suyo
    assert a([1.0, 1.0, 1.0], [0.0, 0.0, 1.0], 0.01, 0.0) == pytest.approx(1 / 3)  # dos sin cifra no comparten la suya
    u = fp.UMBRALES["REI-LEV-001"]
    assert fp._concentradas({"x": ([19.0, 1.0], [1.0, 1.0])}, u, 0.0) == []         # el 95 % justo se entrega
    assert fp._concentradas({"x": ([19.002, 0.998], [1.0, 1.0])}, u, 0.0) == ["x"]


def test_h02_un_segmento_casi_sin_riesgo_no_se_rechaza_por_la_aportacion():
    """Con PD despreciables (por debajo de la tolerancia de la ficha) la PD media es 0 y no es la cifra de nadie, aunque un
    emisor aporte casi toda."""
    v, p = _caso("FIR-CRED-001", 0)                                         # σ_E = 0,001: PD 0 en todos
    v["componentes"][0]["volatilidad_acciones"] = 0.15                       # PD ≈ 1,8e-21 %: aporta toda la PD media
    res, _ = _correr("FIR-CRED-001", v, p)
    d = res["neutral_al_riesgo"]["pd_pct"]
    assert 0 < d["media_ponderada_deuda"] < 1e-4 and d["maximo"] > 0 and d["mediana"] == 0


def test_h02_vencimientos_e_impacto_de_un_solo_componente_no_se_entregan():
    v, p = _caso("REI-LEV-001", 1)
    v["componentes"][0]["vencimientos"] = [{"fecha": "2030-03-31", "importe": 220.0, "coste": 0.015},
                                           {"fecha": "2031-12-31", "importe": 200.0, "coste": 0.035}]   # S1 sin nada a 24 m
    v["componentes"][2]["vencimientos"] = [{"fecha": "2030-01-31", "importe": 100.0, "coste": 0.04}]
    res, lim = _correr("REI-LEV-001", v, p)                                  # solo S2 vence en 24 meses
    assert res["vencimientos_24m_pct"] is None and res["impacto_ffo_pct"] is None
    assert res["ltv_pct"] is not None and res["icr_veces"] is not None
    assert "sin los vencimientos a 24 meses, el impacto en FFO: más del 95% lo aporta un componente (o varios con su misma " \
           "cifra); sería la cifra de ese componente (1.6)" in lim
    v["componentes"][2]["vencimientos"] = [{"fecha": "2027-01-31", "importe": 100.0, "coste": 0.04}]   # y S3: se entregan
    res, _ = _correr("REI-LEV-001", v, p)
    assert res["vencimientos_24m_pct"] == pytest.approx((90.0 + 100.0) / 850.0 * 100)


def test_h02_un_sector_sin_dilucion_no_da_la_cifra_de_cada_token():
    """Tokens con toda la oferta en circulación: FDV/CM = 1 en todos, y la del sector sería la de cada uno."""
    v, p = _caso("CHR-TOKEN-001", 1)
    v["tokens"] = _token_extra(3)
    for t in v["tokens"]:
        t["oferta_total"] = t["oferta_circulante"]
    res, lim = _correr("CHR-TOKEN-001", v, p)
    assert res["fdv_sobre_capitalizacion_veces"] is None and res["inflacion_neta_pct_anual"] is not None
    assert set(res["desbloqueos_pct"].values()) == {0.0}                    # nadie desbloquea: 0 no es la cifra de nadie
    assert any(x.startswith("sin la FDV/capitalización: más del 95%") for x in lim)
    for t in v["tokens"]:                                                    # además sin emisión: las mismas cifras
        t["emision_anual"] = 0.0
    with pytest.raises(ErrorFicha, match=rf"rechazo: 1 {COPIAS} \(< 2\)"):
        _correr("CHR-TOKEN-001", v, p)


def test_h02_staking_concentrado_en_un_token_no_se_entrega():
    v, p = _caso("CHR-TOKEN-001", 1)
    v["tokens"][1]["staking_nominal"] = -0.05                                # TKB: real −5 % − (−5 %) = 0
    res, lim = _correr("CHR-TOKEN-001", v, p)
    assert res["rendimiento_real_staking_pct"] is None and res["concentracion_10_mayores_pct"] is not None
    assert "sin rendimiento de staking: más del 95% lo aporta un componente (o varios con su misma cifra); sería la " \
           "cifra de ese componente (1.6)" in lim


# ====================================================================================================== casos de control
def test_casos_de_control_con_sus_datos_de_la_r02(tmp_path):
    """Los casos de CHR-TOKEN-001 cambian sus datos (INC-T127-01, ronda r02) y comprueban lo mismo: «sin dilución» es la
    propia red (dos tokens sin dilución tienen las mismas cifras); en el método, TKB quema 4e7 y desbloquea 2,4e7 (con los
    de antes, TKA aportaba el 96,8 % de la inflación y los dos desbloqueaban el 5 % a 30 días)."""
    res = _motor(tmp_path).verificar_casos_control(["FIR-CRED-001", "REI-LEV-001", "CHR-TOKEN-001"])
    assert all(x["superados"] for x in res.values()), res
    v, _ = _caso("CHR-TOKEN-001", 0)
    assert v["ambito"] == "Bitcoin" and [t["id"] for t in v["tokens"]] == ["BTC"]
    v, p = _caso("CHR-TOKEN-001", 1)
    v["tokens"][1]["quema_anual"] = 2.4e7
    v["tokens"][1]["calendario"]["desbloqueos"][0]["cantidad"] = 2.0e7
    res, lim = _correr("CHR-TOKEN-001", v, p)
    assert res["inflacion_neta_pct_anual"] is None and res["desbloqueos_pct"]["30"] is None
    assert res["desbloqueos_pct"]["90"] is not None and any(x.startswith("sin la inflación neta, los desbloqueos a 30 días")
                                                            for x in lim)


# ====================================================================================================== H-03 · declarado
def test_h03_con_siete_o_mas_el_maximo_es_la_cifra_de_un_componente_sin_identificarlo():
    """Declarado en INC-T127-01 (ronda r02): un estadístico de orden es siempre la cifra de un componente (el mínimo y el
    máximo; la mediana con n impar), sin decir de cuál. Si esto cambia, hay que cambiar la declaración."""
    v, p = _caso("FIR-CRED-001", 1)
    res, _ = _correr("FIR-CRED-001", v, p)
    pd_ = sorted(fp._fc_directo(V, sV, D)["pd"] * 100 for V, sV, D, _ in fp._FC_ACTIVOS)
    d = res["neutral_al_riesgo"]["pd_pct"]
    assert math.isclose(d["maximo"], pd_[-1], rel_tol=1e-6) and math.isclose(d["minimo"], pd_[0], rel_tol=1e-6, abs_tol=1e-9)
    assert not any(c["id"] in str(res) for c in v["componentes"])
    assert fp.FRONTERA_B == {"tolerancia_clon": 0.01, "peso_maximo_componente": 0.95, "componentes_minimos_orden": 7}


def test_ninguna_regla_nueva_se_cambia_desde_la_peticion():
    for ficha in ("FIR-CRED-001", "REI-LEV-001", "CHR-TOKEN-001"):
        v, p = _caso(ficha, 1)
        for clave in fp.FRONTERA_B:
            with pytest.raises(ErrorFicha, match="umbrales fijos"):
                _correr(ficha, copy.deepcopy(v), {**p, clave: 1.0})
