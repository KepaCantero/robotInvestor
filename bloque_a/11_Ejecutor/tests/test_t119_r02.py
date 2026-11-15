"""T-119 · Ronda r02: una regresión por hallazgo de la QA r01 (`.docs/tickets/T-119/qa.md`).

- H-01: frontera con el Bloque B. REI-LEV-001 exige 3 componentes distintos; FIR-CRED-001, REI-LEV-001 y CHR-TOKEN-001
  rechazan componentes con los mismos datos; CHR-TOKEN-001 solo admite un token si el ámbito se declara como la propia
  red, y lo dice en la entrega; REI-NAV-001 (T-112) rechaza un solo componente.
- H-03: la TIR con un número par de soluciones no dice «sin TIR».
- H-05 y H-09: PRV-PME-001 declara que LN-PME no se calcula y CMD-REAL-001, que el IC de la tendencia no lleva la
  corrección de autocorrelación.
- H-06 y H-08 (`servicio.py`): la caché no entrega el resultado de una petición con otros tipos en sus datos ni el
  calculado con otra configuración.

Las pruebas que matan los mutantes de H-02 están en `test_t119_p2.py` (es el fichero que ejecuta `r01_09_mutantes.py`).
"""
import copy
import json
from decimal import Decimal
from pathlib import Path

import numpy as np
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.motor import fichas_p2 as fp
from bloque_a.motor import fichas_reales as fr
from bloque_a.motor import servicio
from bloque_a.motor.operaciones import ErrorFicha


class _Proveedor:
    as_of = None
    nombre = "pruebas"


def _motor(carpeta, cfg=None):
    return servicio.Motor(Almacen(Path(carpeta)), _Proveedor(), cfg or cargar_config())


def _caso(ficha, i, modulo=fp):
    caso = modulo.CASOS_CONTROL[ficha][i]
    v = {}
    for d in caso["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    return v, dict(caso["parametros"])


def _correr(ficha, v, p=None, modulo=fp):
    return modulo.FICHAS[ficha]["fn"]({"valores": copy.deepcopy(v), "series": {}, "series_rol": {}}, dict(p or {}))


def _servir(m, ficha, v, p=None):
    return m.servir({"operacion": ficha, "datos": [{"valores": copy.deepcopy(v)}], "parametros": dict(p or {}),
                     "fecha_corte": None}, "AG-21")


# ====================================================================================================== H-01
def test_h01_los_minimos_de_componentes_son_umbrales_fijos():
    assert fp.UMBRALES["FIR-CRED-001"]["componentes_minimos"] == 10          # el de la ficha
    assert fp.UMBRALES["REI-LEV-001"]["componentes_minimos"] == 3            # [PROPUESTO] INC-T119-01
    assert fp.UMBRALES["CHR-TOKEN-001"]["tokens_minimos_sector"] == 2        # [PROPUESTO] INC-T119-01
    assert fr.UMBRALES["REI-NAV-001"]["componentes_minimos"] == 2            # [PROPUESTO] INC-T119-01
    for ficha, umbral in (("REI-LEV-001", "componentes_minimos"), ("CHR-TOKEN-001", "tokens_minimos_sector")):
        with pytest.raises(ErrorFicha, match="umbrales fijos"):
            _correr(ficha, _caso(ficha, 1)[0], {umbral: 1})


@pytest.mark.parametrize("n", [1, 2])
def test_h01_rei_lev_con_menos_de_tres_componentes_se_rechaza(n, tmp_path):
    v, p = _caso("REI-LEV-001", 0)
    assert len(v["componentes"]) == 3 and _correr("REI-LEV-001", v, p)[0]["n_componentes"] == 3   # con 3 se sirve
    v["componentes"] = v["componentes"][:n]
    with pytest.raises(ErrorFicha, match=rf"rechazo: {n} componentes \(< 3\)"):
        _correr("REI-LEV-001", v, p)
    m = _motor(tmp_path)
    r = _servir(m, "REI-LEV-001", v, p)
    assert r["estado"] == "RECHAZADO" and "(1.6)" in r["detalle"] and len(m.almacen.leer("RC")) == 1


def test_h01_rei_lev_no_se_ordenan_emisores_con_una_peticion_por_emisor(tmp_path):
    v, p = _caso("REI-LEV-001", 0)
    m = _motor(tmp_path)
    estados = [_servir(m, "REI-LEV-001", {**v, "componentes": [c]}, p)["estado"] for c in v["componentes"]]
    assert estados == ["RECHAZADO"] * 3


def _clonar(fila, n):
    return [{**copy.deepcopy(fila), "id": f"EMISOR_SECRETO_{j:02d}"} for j in range(n)]


@pytest.mark.parametrize("ficha,clave,n", [("FIR-CRED-001", "componentes", 10), ("REI-LEV-001", "componentes", 3),
                                           ("CHR-TOKEN-001", "tokens", 2)])
def test_h01_el_minimo_no_se_burla_clonando_un_componente(ficha, clave, n, tmp_path):
    """`n` copias del mismo emisor o token con otro identificador: el «agregado» serían sus cifras. Se rechaza, y el
    mensaje no cita identificadores."""
    v, p = _caso(ficha, 1)
    v[clave] = _clonar(v[clave][0], n)
    with pytest.raises(ErrorFicha, match="con los mismos datos que otro") as e:
        _correr(ficha, v, p)
    assert "EMISOR_SECRETO" not in str(e.value) and f"{n - 1} componentes" in str(e.value)
    r = _servir(_motor(tmp_path), ficha, v, p)
    assert r["estado"] == "RECHAZADO" and "EMISOR_SECRETO" not in r["detalle"]


@pytest.mark.parametrize("ficha,clave", [("FIR-CRED-001", "componentes"), ("REI-LEV-001", "componentes"),
                                         ("CHR-TOKEN-001", "tokens")])
def test_h01_un_solo_clon_entre_componentes_distintos_tambien_se_rechaza(ficha, clave):
    v, p = _caso(ficha, 1)
    _correr(ficha, v, p)
    v[clave].append({**copy.deepcopy(v[clave][0]), "id": "OTRO_ID"})
    with pytest.raises(ErrorFicha, match="rechazo: 1 componentes con los mismos datos que otro"):
        _correr(ficha, v, p)


def test_h01_fir_cred_el_clon_se_reconoce_por_los_datos_del_modelo_no_por_el_rendimiento_historico():
    """Cambiar solo `mu_historico` (que con `mu: r` no se usa) no hace distinto a un emisor; otra capitalización, sí."""
    v, p = _caso("FIR-CRED-001", 1)
    extra = {**copy.deepcopy(v["componentes"][0]), "id": "OTRO_ID", "mu_historico": 0.2}
    with pytest.raises(ErrorFicha, match="con los mismos datos que otro"):
        _correr("FIR-CRED-001", {**v, "componentes": v["componentes"] + [extra]}, p)
    extra["capitalizacion"] *= 1.5
    res, _ = _correr("FIR-CRED-001", {**v, "componentes": v["componentes"] + [extra]}, p)
    assert res["n_componentes"] == len(v["componentes"]) + 1


def test_h01_chr_token_un_solo_token_solo_si_el_ambito_es_la_propia_red(tmp_path):
    v, p = _caso("CHR-TOKEN-001", 1)
    assert "ambito_es_red" not in v and len(v["tokens"]) == 2
    base, lim_base = _correr("CHR-TOKEN-001", v, p)
    uno = {**v, "tokens": [v["tokens"][0]]}
    for declarado in ({}, {"ambito_es_red": False}):
        with pytest.raises(ErrorFicha, match=r"rechazo: 1 token \(< 2\) y el ámbito no se declara como la propia red"):
            _correr("CHR-TOKEN-001", {**uno, **declarado}, p)
    for malo in ("sí", 1, [True]):
        with pytest.raises(ErrorFicha, match="«ambito_es_red» debe ser true o false"):
            _correr("CHR-TOKEN-001", {**v, "ambito_es_red": malo}, p)
    # declarado como la propia red, se sirve y se dice en la entrega. T-127 (H-10): la red es una de `redes_propias` y el
    # token, su token nativo (antes valía cualquier ámbito, como «red TKA»: lo comprueba `test_t127_hallazgos.py`)
    red = {**uno, "tokens": [{**uno["tokens"][0], "id": "BTC"}], "ambito": "Bitcoin", "ambito_es_red": True}
    r = _servir(_motor(tmp_path), "CHR-TOKEN-001", red, p)
    assert r["estado"] == "SERVED_WITH_LIMITATIONS" and r["resultado"]["n_tokens"] == 1
    assert any("un solo token: el ámbito declarado es la propia red" in x for x in r["limitaciones"])
    assert r["resultado"]["fdv_sobre_capitalizacion_veces"] == pytest.approx(1.0e9 / 6.0e8)
    # con dos tokens la declaración no cambia nada
    for declarado in (True, False):
        res, lim = _correr("CHR-TOKEN-001", {**v, "ambito_es_red": declarado}, p)
        assert json.dumps(res, sort_keys=True) == json.dumps(base, sort_keys=True) and lim == lim_base


def test_h01_rei_nav_un_solo_componente_se_rechaza():
    """El mismo hueco en una ficha de T-112: el agregado de una sociedad es la sociedad."""
    v, p = _caso("REI-NAV-001", 1, fr)
    assert len(v["componentes"]) == 2
    _correr("REI-NAV-001", v, p, fr)
    with pytest.raises(ErrorFicha, match=r"rechazo: 1 componente \(< 2\)"):
        _correr("REI-NAV-001", {**v, "componentes": v["componentes"][:1]}, p, fr)
    with pytest.raises(ErrorFicha, match="umbrales fijos"):
        _correr("REI-NAV-001", v, {**p, "componentes_minimos": 1}, fr)


def test_h01_los_casos_de_control_de_las_cuatro_fichas_siguen_superados(tmp_path):
    res = _motor(tmp_path).verificar_casos_control(["FIR-CRED-001", "REI-LEV-001", "CHR-TOKEN-001", "REI-NAV-001"])
    assert all(x["superados"] for x in res.values()), res


# ====================================================================================================== H-03
def _prv_cf(flujos):
    return {"compromiso": 1000.0, "navs": [{"fecha": "2023-01-01", "valor": 0.0}],
            "flujos": [{"fecha": f, "aportacion": float(a), "distribucion": float(d)} for f, a, d in flujos]}


def test_h03_dos_tir_no_es_sin_tir(tmp_path):
    """−100, +230, −132 a 0, 1 y 2 años: hay dos TIR (10 % y 20 %). No se entrega ninguna, y no se dice que no hay."""
    m = _motor(tmp_path)
    r = _servir(m, "PRV-CF-001", _prv_cf([("2021-01-01", 100, 0), ("2022-01-01", 0, 230), ("2023-01-01", 132, 0)]))
    tir = [x for x in r["limitaciones"] if x.startswith("TIR")]
    assert r["resultado"]["tir_pct"] is None and not any("sin TIR" in x for x in tir)
    assert any("múltiples soluciones" in x for x in tir)
    assert any("2 soluciones entre -0.99 y 10 (rejilla de 1000 puntos): no se aísla una TIR única" in x for x in tir)
    # −100, +230, −133: ninguna raíz real; ahí sí
    r = _servir(m, "PRV-CF-001", _prv_cf([("2021-01-01", 100, 0), ("2022-01-01", 0, 230), ("2023-01-01", 133, 0)]))
    assert r["resultado"]["tir_pct"] is None and any("sin TIR entre -0.99 y 10" in x for x in r["limitaciones"])
    # un solo cambio de signo y la TIR fuera del rango: el texto de siempre, sin rejilla
    lim: list[str] = []
    assert fp._tir(np.array([0.0, 365.0]), np.array([-100.0, 0.5]), fp.UMBRALES["PRV-CF-001"], lim, "TIR") is None
    assert lim == ["TIR: sin TIR entre -0.99 y 10"]


def test_h03_la_rejilla_es_un_umbral_fijo():
    assert fp.UMBRALES["PRV-CF-001"]["rejilla_tir"] == fp.UMBRALES["PRV-PME-001"]["rejilla_tir"] == 1000
    with pytest.raises(ErrorFicha, match="umbrales fijos"):
        _correr("PRV-CF-001", _caso("PRV-CF-001", 0)[0], {"rejilla_tir": 3})


# ====================================================================================================== H-05 y H-09
@pytest.mark.parametrize("ficha,texto", [("PRV-PME-001", "LN-PME (Long-Nickels), que la ficha da por opcional, no se calcula"),
                                         ("CMD-REAL-001", "el intervalo de la tendencia no lleva la corrección de autocorrelación")])
def test_h05_h09_lo_que_no_se_calcula_se_declara_en_la_entrega(ficha, texto, tmp_path):
    v, p = _caso(ficha, 1)
    r = _servir(_motor(tmp_path), ficha, v, p)
    assert r["estado"] == "SERVED"                                       # una advertencia fija no es una limitación
    assert any(texto in x for x in r["resultado"]["advertencias"]) and not any(texto in x for x in r["limitaciones"])


# ====================================================================================================== H-06 y H-08
def test_h06_la_cache_no_entrega_el_resultado_de_otra_peticion_con_otros_tipos(tmp_path):
    """`numpy.float32(1.5)`, `Decimal("1.5")` y el texto "1.5" dan la misma clave de idempotencia; solas, las dos últimas
    se rechazan, y tras servir la primera también."""
    m = _motor(tmp_path)
    v, p = _caso("FIR-CRED-001", 1)

    def con(x):
        w = copy.deepcopy(v)
        w["componentes"][0]["deuda_corto"] = x
        return w

    r1 = _servir(m, "FIR-CRED-001", con(np.float32(1.5)), p)
    assert r1["estado"].startswith("SERVED") and not r1["cache_hit"]
    for raro in (Decimal("1.5"), "1.5"):
        assert _servir(_motor(tmp_path / str(type(raro).__name__)), "FIR-CRED-001", con(raro), p)["estado"] == "RECHAZADO"
        r = _servir(m, "FIR-CRED-001", con(raro), p)
        assert r["estado"] == "RECHAZADO" and not r.get("cache_hit"), r
    # la misma petición, con los mismos tipos, sí sale de la caché
    r2 = _servir(m, "FIR-CRED-001", con(np.float32(1.5)), p)
    assert r2["cache_hit"] and r2["resultado"] == r1["resultado"]
    assert [e["tipo_entrada"] for e in m.almacen.leer("RC")] == ["SERVICIO", "RECHAZO", "RECHAZO", "CACHE_HIT"]


def test_h06_la_firma_distingue_el_tipo_de_lo_que_no_es_json():
    f = servicio._firma_tipos
    assert len({f(np.float32(1.5)), f(Decimal("1.5")), f("1.5"), f(1.5)}) == 4
    assert f({"a": 1.5}) == f({"a": np.float64(1.5)})                    # float64 es un float: mismo valor, misma firma
    assert f({(1, 2): 3}) is None                                        # lo que no se puede firmar no usa la caché


def test_h08_un_cambio_de_configuracion_en_caliente_no_sale_de_la_cache(tmp_path):
    """FX-BEER-001 lee `evaluacion.nivel_ic`. Si la configuración del Motor cambia sobre el mismo objeto, la petición
    repetida se vuelve a calcular; si cambia una sección que la ficha no lee, sigue saliendo de la caché."""
    m = _motor(tmp_path, copy.deepcopy(cargar_config()))
    v, p = _caso("FX-BEER-001", 0)
    r1 = _servir(m, "FX-BEER-001", v, p)
    assert _servir(m, "FX-BEER-001", v, p)["cache_hit"]
    m.cfg["uc"]["motor_por_plan"]["PLAN_MAX"] = 0.5                        # la ficha no lee `uc`
    assert _servir(m, "FX-BEER-001", v, p)["cache_hit"]
    m.cfg["evaluacion"]["nivel_ic"] = 0.5
    r3 = _servir(m, "FX-BEER-001", v, p)
    assert not r3["cache_hit"] and r3["resultado"]["nivel_ic"] == 0.5 != r1["resultado"]["nivel_ic"]
    assert r3["resultado"]["ic_desalineamiento_pct"] != r1["resultado"]["ic_desalineamiento_pct"]
    assert _servir(m, "FX-BEER-001", v, p)["cache_hit"]                    # y la nueva queda en la caché
    # una ficha que no lee la configuración no se ve afectada
    w, q = _caso("REI-LEV-001", 0)
    _servir(m, "REI-LEV-001", w, q)
    m.cfg["evaluacion"]["nivel_ic"] = 0.8
    assert _servir(m, "REI-LEV-001", w, q)["cache_hit"]
