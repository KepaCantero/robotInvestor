"""T-127 r03 · Motor del Bloque A: hallazgos de la QA r02 de T-127 en la frontera con el Bloque B (1.6).

- H-04 (alta): un emisor troceado en partes con repartos distintos, o copiado con perturbaciones simétricas, da su cifra en
  una sola petición. Los componentes los aporta quien pide (datos en línea de CT-09; HT-01 solo sirve series de precios), y
  ninguna regla sobre ellos lo distingue de varios emisores reales: **límite declarado** (INC-T127-01 «Ronda r03», pregunta
  para T-57). Mitigación barata: un aviso en las limitaciones (y en el Registro de cálculos) cuando dos componentes solo
  difieren en un dato (`frontera_b._aviso_casi_clones`, `AVISO_B`). Las pruebas fijan el límite: el troceo se sirve y queda
  en el Registro con sus datos.
- H-05 (baja): con dos rellenos que se compensan (+400 y −400) el agregado dividido por el peso de S1 era su LTV exacto. La
  aportación se mide también con signo (`frontera_b._aportacion_maxima`): se rechaza, y con las dos medidas por debajo de
  k = 95 % el error de esa estimación es de al menos (1 − k)/(2 − k).
"""
import copy

import numpy as np
import pytest
from bloque_a.motor import fichas_p2 as fp
from bloque_a.motor import frontera_b as fb
from bloque_a.motor.operaciones import ErrorFicha
from test_t127_hallazgos import _caso, _correr, _motor, _peticion

AVISO = "aviso (1.6)"
APORTA = "lo aporta un componente"


def _avisos(lim):
    return [x for x in lim if x.startswith(AVISO)]


def _fir_perturbado(datos=("volatilidad_acciones",)):
    """FIR-CRED-001: C11 del caso de control 1 en 10 copias con σ_E·(1 ± δ) (δ de 2 % a 10 %), el ataque «S» del revisor; con
    `datos` de dos campos, los dos movidos a la vez."""
    v, p = _caso("FIR-CRED-001", 1)
    base = v["componentes"][11]
    comps = []
    for k, d in enumerate((0.02, 0.04, 0.06, 0.08, 0.10)):
        for sg in (1, -1):
            c = copy.deepcopy(base)
            c["id"] = f"EMISOR_SECRETO_{k}{sg}"
            for q in datos:
                c[q] = base[q] * (1 + sg * d)
            comps.append(c)
    v["componentes"] = comps
    return v, p


def _lev_troceado():
    """REI-LEV-001: S1 del caso de control en 3 partes con repartos distintos de cada importe (el ataque «T» del revisor)."""
    v, p = _caso("REI-LEV-001", 1)
    s1 = v["componentes"][0]
    rep = {"gav": (0.5, 0.3, 0.2), "deuda": (0.3, 0.4, 0.3), "caja": (0.5, 0.25, 0.25), "ebitda": (0.4, 0.4, 0.2),
           "gastos_financieros": (0.25, 0.35, 0.4), "ffo": (0.5, 0.3, 0.2)}
    venc = [(60.0, 30.0, 36.0), (40.0, 50.0, 78.0), (20.0, 20.0, 86.0)]
    partes = []
    for k in range(3):
        c = copy.deepcopy(s1)
        c["id"] = f"S1_PARTE_{k}"
        for q, s in rep.items():
            c[q] = s1[q] * s[k]
        c["vencimientos"] = [{**x, "importe": venc[k][j]} for j, x in enumerate(s1["vencimientos"])]
        partes.append(c)
    v["componentes"] = partes
    return v, p, s1


# ====================================================================================================== H-05 · con signo
def test_h05_rellenos_que_se_compensan_se_rechazan(tmp_path):
    """La vía «C» del revisor: S1 + un relleno de deuda neta +400 y otro de −400 (caja mayor que la deuda). En valor absoluto
    S1 aporta un tercio del LTV; con signo, todo: se rechaza (el LTV y la deuda neta/EBITDA), sin citar identificadores."""
    v, p = _caso("REI-LEV-001", 1)
    s1 = v["componentes"][0]
    f1 = copy.deepcopy(s1) | {"id": "RELLENO_MAS", "gav": 1500.0, "deuda": 410.0, "caja": 10.0, "ebitda": 90.0,
                              "gastos_financieros": 15.0, "ffo": 50.0,
                              "vencimientos": [{"fecha": "2030-12-31", "importe": 410.0, "coste": 0.03}]}
    f2 = copy.deepcopy(s1) | {"id": "RELLENO_MENOS", "gav": 1200.0, "deuda": 10.0, "caja": 410.0, "ebitda": 70.0,
                              "gastos_financieros": 9.0, "ffo": 40.0,
                              "vencimientos": [{"fecha": "2030-12-31", "importe": 10.0, "coste": 0.03}]}
    for f in (f1, f2):
        f.pop("covenants", None)
    v["componentes"] = [s1, f1, f2]
    with pytest.raises(ErrorFicha, match=rf"más del 95% de el LTV, la deuda neta/EBITDA {APORTA}") as e:
        _correr("REI-LEV-001", v, p)
    assert "RELLENO" not in str(e.value) and s1["id"] not in str(e.value)
    r = _motor(tmp_path).servir(_peticion("REI-LEV-001", 1, v, p), "AG-21")
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "DATOS_INSUFICIENTES"


def test_h05_la_aportacion_con_signo():
    a = fb._aportacion_maxima
    assert a([400.0, 400.0, -400.0], [1000.0, 1500.0, 1200.0], 0.01, 0.0) == pytest.approx(1.0)
    assert a([400.0, 400.0, -380.0], [1000.0, 1500.0, 1200.0], 0.01, 0.0) == pytest.approx(1 - 20 / 420)   # 0,952
    assert a([400.0, 400.0, -370.0], [1000.0, 1500.0, 1200.0], 0.01, 0.0) == pytest.approx(1 - 30 / 430)   # 0,930
    # del mismo signo, la medida con signo es la de siempre (num_G / Σnum = |num_G| / Σ|num|)
    assert a([3.0, 1.0, 1.0], [1.0, 1.0, 1.0], 0.01, 0.0) == pytest.approx(0.6)
    assert a([-3.0, -1.0, -1.0], [1.0, 1.0, 1.0], 0.01, 0.0) == pytest.approx(0.6)
    # el resto de signo contrario que no compensa del todo: el mayor de los dos
    assert a([-3.0, 1.0], [1.0, 1.0], 0.01, 0.0) == pytest.approx(0.75)
    assert a([10.0, 1.0, -1.05], [1.0, 1.0, 1.0], 0.01, 0.0) == pytest.approx(1 - 0.05 / 9.95)
    # con signo, también por grupos de la misma cifra: dos con cifra 5 y dos rellenos que se compensan (7 y −7)
    assert a([5.0, 5.0, 7.0, -7.0], [1.0, 1.0, 1.0, 1.0], 0.01, 0.0) == pytest.approx(1.0)
    assert a([5.0, 5.0, 7.0, -7.0], [1.0, 1.02, 1.0, 1.0], 0.01, 0.0) == pytest.approx(0.7)   # cada uno el suyo: el 7
    # un agregado nulo a la tolerancia de la ficha sigue sin ser de nadie
    assert a([400.0, -400.0], [1.0, 1.0], 0.01, 1e-9) == 0.0
    u = fp.UMBRALES["REI-LEV-001"]
    assert fb._concentradas({"x": ([400.0, 400.0, -380.0], [1000.0, 1500.0, 1200.0])}, u, 0.0) == ["x"]
    assert fb._concentradas({"x": ([400.0, 400.0, -370.0], [1000.0, 1500.0, 1200.0])}, u, 0.0) == []


def test_h05_por_debajo_de_k_el_error_es_de_al_menos_la_cota():
    """La frase corregida de INC-T127-01: con la aportación (en valor absoluto y con signo) a lo sumo k, el agregado
    multiplicado por Σden y dividido por el peso del grupo de un componente (den_G) da su cifra con un error relativo de al
    menos (1 − k)/(2 − k), sea cual sea el signo del resto. Barrido con rellenos de los dos signos."""
    k = fp.FRONTERA_B["peso_maximo_componente"]
    cota = (1 - k) / (2 - k)
    rng = np.random.default_rng(127)
    vistos = 0
    for _ in range(4000):
        n = int(rng.integers(2, 6))
        den = rng.uniform(0.5, 3.0, n)
        x = rng.normal(0.0, 1.0, n)
        x[1:] *= rng.uniform(0.0, 0.2)                     # el resto, pequeño: cerca del borde
        num = den * x
        if fb._aportacion_maxima(num, den, 0.01, 0.0) > k:
            continue
        vistos += 1
        estimado = float(np.sum(num)) / float(den[0])
        assert abs(estimado - x[0]) >= cota * abs(x[0]) * (1 - 1e-9)
    assert vistos > 100


# ====================================================================================================== H-04 · aviso
def test_h04_un_dato_perturbado_de_forma_simetrica_se_sirve_con_aviso(tmp_path):
    """El ataque «S» de FIR-CRED-001 (σ_E·(1 ± δ)): se sirve (límite declarado) con el aviso, que llega al Registro de
    cálculos con los datos de la petición y no cita identificadores."""
    v, p = _fir_perturbado()
    _, lim = _correr("FIR-CRED-001", v, p)
    aviso = (f"{AVISO}: 10 componentes coinciden con otro en todos los datos del cálculo menos 1 (a menos del 1%): pueden "
             f"ser un mismo emisor con un dato movido, y el agregado, su cifra; la petición queda en el Registro de cálculos "
             f"con sus datos")
    assert _avisos(lim) == [aviso]
    m = _motor(tmp_path)
    r = m.servir(_peticion("FIR-CRED-001", 1, v, p), "AG-21")
    assert r["estado"] == "SERVED_WITH_LIMITATIONS" and _avisos(r["limitaciones"])
    rc = [e for e in m.almacen.leer("RC") if e.get("calc_id") == r["calc_id"]]
    assert len(rc) == 1 and _avisos(rc[0]["limitaciones"]) and rc[0]["datos"][0]["valor"]["componentes"]
    assert not any("EMISOR_SECRETO" in x for x in r["limitaciones"])


def test_h04_dos_datos_movidos_no_dan_aviso():
    """Límite declarado del aviso: con dos datos movidos (σ_E y la capitalización) ya no coinciden en todos menos uno."""
    v, p = _fir_perturbado(("volatilidad_acciones", "capitalizacion"))
    _, lim = _correr("FIR-CRED-001", v, p)
    assert _avisos(lim) == []


@pytest.mark.parametrize("ficha,campo,mas", [("REI-LEV-001", "caja", 1.0), ("CHR-TOKEN-001", "emision_anual", 1e6),
                                             ("CHR-TOKEN-001", "quema_anual", 1e6)])
def test_h04_aviso_en_rei_lev_y_chr_token(ficha, campo, mas):
    """Una copia del último componente con un solo dato movido (la caja, la emisión o la quema): se sirve con el aviso."""
    v, p = _caso(ficha, 1)
    clave = "componentes" if ficha == "REI-LEV-001" else "tokens"
    otro = copy.deepcopy(v[clave][-1])
    otro["id"] = "COPIA_SECRETA"
    otro[campo] = otro[campo] * 1.3 + mas
    v[clave].append(otro)
    _, lim = _correr(ficha, v, p)
    assert len(_avisos(lim)) == 1 and _avisos(lim)[0].startswith(f"{AVISO}: 2 componentes coinciden con otro")
    assert not any("COPIA_SECRETA" in x for x in lim)
    v[clave][-1]["precio" if ficha == "CHR-TOKEN-001" else "gav"] *= 1.5      # y otro dato más: ya no hay aviso
    try:
        _, lim = _correr(ficha, v, p)
    except ErrorFicha:           # con el precio movido, CHR-TOKEN la toma por copia a escala (FDV/CM): no se sirve
        assert ficha == "CHR-TOKEN-001"
        return
    assert _avisos(lim) == []


def test_h04_los_casos_de_control_no_dan_aviso():
    for ficha in ("FIR-CRED-001", "REI-LEV-001", "CHR-TOKEN-001"):
        for i in range(len(fp.CASOS_CONTROL[ficha])):
            v, p = _caso(ficha, i)
            try:
                _, lim = _correr(ficha, v, p)
            except ErrorFicha:
                continue
            assert _avisos(lim) == [], (ficha, i)


def test_h04_el_aviso_cuenta_los_datos_que_coinciden():
    d = fb._datos_que_coinciden
    assert d([(1.0, 2.0, None), (1.005, 3.0, None), (1.0, 2.0, 0.0)], 0.01).tolist() == [[3, 2, 2], [2, 3, 1], [2, 1, 3]]
    assert d([], 0.01).shape == (0, 0)
    lim: list[str] = []
    assert fb._aviso_casi_clones([(1.0, 2.0, 3.0), (1.0, 2.0, 9.0), (5.0, 6.0, 7.0)], 0.01, lim) == 2 and len(lim) == 1
    lim = []
    assert fb._aviso_casi_clones([(1.0, 2.0, 3.0), (1.0, 4.0, 9.0), (5.0, 6.0, 7.0)], 0.01, lim) == 0 and lim == []
    assert fb._aviso_casi_clones([(1.0, 2.0)], 0.01, lim) == 0 and lim == []
    # el borde del 1 %, el de los casi clones
    assert fb._aviso_casi_clones([(1.0, 2.0, 3.0), (1.01, 2.0, 9.0)], 0.01, []) == 2
    assert fb._aviso_casi_clones([(1.0, 2.0, 3.0), (1.0102, 2.0, 9.0)], 0.01, []) == 0
    # los grupos de casi clones no cambian (`_etiquetas_casi_iguales` cuenta ahora con `_datos_que_coinciden`)
    assert fb._grupos_casi_iguales([(1.0, 2.0), (1.008, 2.0), (1.016, 2.0), (1.0, 2.5)], 0.01) == 2
    assert fb._grupos_casi_iguales([(1.0, None), (1.0, 0.0)], 0.01) == 2
    assert fb.AVISO_B == {"datos_distintos_aviso": 1}


# ====================================================================================================== H-04 · límite declarado
def test_h04_limite_declarado_un_emisor_troceado_se_sirve_y_queda_en_el_registro(tmp_path):
    """INC-T127-01 «Ronda r03»: el ataque «T» del revisor sigue dando el LTV y el ICR de S1 en una sola petición. Ninguna
    regla sobre los datos lo distingue de tres sociedades reales; el control es el propósito de la petición (1.6) y el
    Registro de cálculos, que guarda las tres partes. Si esta prueba falla porque el troceo se rechaza, se ha cerrado el
    límite: actualizar INC-T127-01 y la pregunta para T-57."""
    v, p, s1 = _lev_troceado()
    res, lim = _correr("REI-LEV-001", v, p)
    assert res["ltv_pct"] == pytest.approx((s1["deuda"] - s1["caja"]) / s1["gav"] * 100, rel=1e-9)
    assert res["icr_veces"] == pytest.approx(s1["ebitda"] / s1["gastos_financieros"], rel=1e-9)
    assert _avisos(lim) == []                   # repartos distintos de cada importe: ni copias ni un dato movido
    m = _motor(tmp_path)
    r = m.servir(_peticion("REI-LEV-001", 1, v, p), "AG-21")
    assert r["estado"].startswith("SERVED")
    rc = next(e for e in m.almacen.leer("RC") if e.get("calc_id") == r["calc_id"])
    assert [c["id"] for c in rc["datos"][0]["valor"]["componentes"]] == ["S1_PARTE_0", "S1_PARTE_1", "S1_PARTE_2"]


def test_h04_limite_declarado_perturbacion_simetrica_da_la_dd_a_menos_del_uno_por_ciento():
    """El ataque «S» de FIR-CRED-001: la DD media y la mediana quedan a menos del 1 % de la de C11 (Merton no es lineal: a
    segundo orden). Se sirve con el aviso; el límite está declarado."""
    v, p = _fir_perturbado()
    res, _ = _correr("FIR-CRED-001", v, p)
    c11 = fp._fc_directo(*fp._FC_ACTIVOS[11][:3])["dd"]
    assert abs(res["neutral_al_riesgo"]["dd"]["mediana"] / c11 - 1) < 1e-2
