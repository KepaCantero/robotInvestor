"""T-118 · Hallazgos abiertos de la QA r02 de T-112 (H-09 a H-14): una regresión por corrección.

- H-09: ML-PRED-001 y ML-CAL-001 rechazan datos fechados después de la fecha de corte.
- H-10: cotas del tamaño de los datos en las nueve fichas del grupo R (en la cota se sirve; con uno más, se rechaza).
- H-11: el artefacto guarda la configuración que la ficha usó y CT-10 re-ejecuta con ella; tras un cambio de
  configuración no se culpa al cálculo original.
- H-12: las cotas de S y P que salen de la configuración siguen a la configuración del Motor.
- H-13: ninguna excepción escapa de `Motor.servir` con una petición mal formada.
- H-14: `reejecutar` registra la re-ejecución que la ficha rechaza (ERROR_REEJECUCION).
"""
import copy
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import (
    cargar_config,
    fusionar,
    parametro,
    sesiones_horizonte,
)
from bloque_a.motor import fichas_reales as P
from bloque_a.motor import fichas_riesgo as R
from bloque_a.motor import fichas_series as S
from bloque_a.motor import servicio
from bloque_a.motor.operaciones import ErrorFicha

H5 = sesiones_horizonte(None, "H5")
SIMULADA = R.UMBRALES["SIM-MC-001"]["rango_n_trayectorias"][1]


class _Proveedor:
    as_of = None
    nombre = "pruebas"


def _motor(carpeta, **extra):
    return servicio.Motor(Almacen(Path(carpeta)), _Proveedor(), cargar_config(extra=extra or None))


def _peticion(ficha, i=0, **extra):
    caso = servicio.CASOS_CONTROL[ficha][i]
    return {"operacion": ficha, "datos": copy.deepcopy(caso["datos"]), "parametros": dict(caso.get("parametros") or {}), **extra}


def _valores(ficha, i=0):
    v = {}
    for d in servicio.CASOS_CONTROL[ficha][i]["datos"]:
        v.update(copy.deepcopy(d["valores"]))
    return v


def _correr(modulo, ficha, valores, params=None, cfg=None, series=None, corte=None):
    ent = {"valores": valores, "series": series or {}, "series_rol": {}, "configuracion": cfg, "fecha_corte": corte}
    return modulo.FICHAS[ficha]["fn"](ent, dict(params or {}))


def _servir_contando(m, pet, solicitante="AG-18"):
    antes = len(m.almacen.leer("RC"))
    r = m.servir(pet, solicitante)   # si escapa una excepción, la prueba falla aquí
    return r, len(m.almacen.leer("RC")) - antes


# ====================================================================================================== H-09
def test_h09_ml_pred_rechaza_datos_posteriores_a_la_fecha_de_corte(tmp_path):
    """El primer caso de control tiene fechas de 2019-01-01 a 2020-08-10: con el corte antes de la última, RECHAZADO."""
    m = _motor(tmp_path)
    ultima = _valores("ML-PRED-001")["fechas"][-1]
    assert ultima == "2020-08-10"
    for corte in ("2008-12-31", "2020-08-09"):
        r, n = _servir_contando(m, _peticion("ML-PRED-001", fecha_corte=corte))
        assert r["estado"] == "RECHAZADO" and "no conocible" in r["detalle"] and corte in r["detalle"] and n == 1, r
    # el dato del día del corte sí es conocible, y sin corte no hay nada que comprobar
    for corte in (ultima, "2026-11-13", None):
        r = m.servir(_peticion("ML-PRED-001", fecha_corte=corte), "AG-18")
        assert r["estado"].startswith("SERVED") and r["resultado"]["prediccion_actual"]["fecha"] == ultima, r


def test_h09_ml_pred_conocible_desde_posterior_al_corte():
    """Una variable conocible después del corte se rechaza por el corte (antes que por la regla de fuga de la ficha)."""
    v = _valores("ML-PRED-001")
    nombre = min(v["variables"])
    v["variables"][nombre]["conocible_desde"] = [*v["fechas"][:-1], "2020-08-11"]   # lista propia: el caso las comparte
    with pytest.raises(ErrorFicha, match="conocible_desde.*posterior a la fecha de corte 2020-08-10"):
        _correr(R, "ML-PRED-001", v, corte="2020-08-10")


def test_h09_ml_pred_la_fecha_de_uso_cuenta_aunque_las_variables_se_conocieran_antes():
    """Variables conocidas con cinco sesiones de adelanto: su `conocible_desde` no pasa del corte, pero la última fecha
    (la del objetivo y la de la predicción actual) sí."""
    v = _valores("ML-PRED-001")
    fechas = list(v["fechas"])
    for d in v["variables"].values():
        d["conocible_desde"] = [fechas[max(i - 5, 0)] for i in range(len(fechas))]
    with pytest.raises(ErrorFicha, match=r"ML-PRED-001: fechas: dato del 2020-08-10 posterior a la fecha de corte 2020-08-07"):
        _correr(R, "ML-PRED-001", copy.deepcopy(v), corte=fechas[-2])
    assert _correr(R, "ML-PRED-001", copy.deepcopy(v), corte=fechas[-1])[0]["prediccion_actual"]["fecha"] == fechas[-1]


def _cal_fechado(n=40):
    fechas = [str(d.date()) for d in pd.bdate_range("2024-01-01", periods=n)]
    y = [0.1 * i + float(np.sin(i)) for i in range(n)]
    return fechas, {"tipo": "nivel", "realizaciones": [{"fecha": f, "valor": a} for f, a in zip(fechas, y)],
                    "predicciones": [{"fecha": f, "valor": a + 0.3} for f, a in zip(fechas, y)]}


def test_h09_ml_cal_rechaza_pares_fechados_despues_del_corte():
    """ML-CAL-001 es la otra ficha del grupo R con datos fechados (predicciones y realizaciones por fecha)."""
    fechas, d = _cal_fechado()
    v = {"ensayos": 1, "horizontes": {"H2": d}}
    with pytest.raises(ErrorFicha, match="posterior a la fecha de corte"):
        _correr(R, "ML-CAL-001", copy.deepcopy(v), corte=fechas[-2])
    r, _ = _correr(R, "ML-CAL-001", copy.deepcopy(v), corte=fechas[-1])
    assert r["horizontes"]["H2"]["fechas"] == [fechas[0], fechas[-1]]
    assert _correr(R, "ML-CAL-001", copy.deepcopy(v))[0]["horizontes"]["H2"]["n"] == 40


def test_h09_una_fecha_de_corte_ilegible_se_rechaza():
    with pytest.raises(ErrorFicha, match="fecha de corte"):
        _correr(R, "ML-PRED-001", _valores("ML-PRED-001"), corte="ayer por la tarde")


# ====================================================================================================== H-10
def _ruido(n, semilla=118, escala=0.01):
    return [float(x) for x in escala * np.random.default_rng(semilla).standard_normal(n)]


def _precios(n):
    return pd.Series(100 * np.exp(np.cumsum(_ruido(n))), index=pd.bdate_range("2000-01-03", periods=n))


def _pred(n, k=1):
    rng = np.random.default_rng(1181)
    fechas = [str(d.date()) for d in pd.bdate_range("2000-01-03", periods=n)]
    x = rng.standard_normal((n, k))
    serie = 100 * np.exp(np.cumsum(0.01 * np.r_[0.0, x[:-1, 0]] + 0.005 * rng.standard_normal(n)))
    return {"fechas": fechas, "objetivo": {"serie": [float(e) for e in serie], "horizonte": 1, "tipo": "direccion",
                                           "criterio_resolucion": "cierre siguiente por encima del actual"},
            "variables": {f"x{i:02d}": {"serie": [float(e) for e in x[:, i]], "conocible_desde": fechas} for i in range(k)}}


def _cal(n):
    y = _ruido(n, 1182, 1.0)
    return {"tipo": "nivel", "realizaciones": y, "predicciones": [a + 0.1 for a in y]}


_GARCH = {"tipo": "bootstrap_filtrado", "mu": 0.0, "omega": 2e-6, "alpha": 0.08, "beta": 0.9}
_REGIMEN = {"fuente": "REG-HMM-001"}
_VOI = {"puntuacion": {"dimension": "E", "actual": 58.0}}


def _estados(k):
    return {**_REGIMEN, "probabilidades_filtradas": {f"e{i}": 1.0 / k for i in range(k)},
            "estados": {f"e{i}": {"media": 0.0002 * i, "volatilidad": 0.01} for i in range(k)}}


# (nombre, ficha, constructor de (valores, series) con n elementos, parámetros, cota)
COTAS_DATOS = [
    ("RISK-VAR-001 rendimientos", "RISK-VAR-001", lambda n: ({"rendimientos": _ruido(n)}, None), {}, H5),
    ("RISK-VAR-001 serie de HT-01", "RISK-VAR-001", lambda n: ({}, {"x": _precios(n + 1)}), {}, H5),
    ("RISK-VAR-001 distribución de MC-05", "RISK-VAR-001",
     lambda n: ({"distribucion": {"semilla": 1, "rendimientos": _ruido(n)}}, None), {}, SIMULADA),
    ("SIM-MC-001 residuos", "SIM-MC-001", lambda n: ({"dinamica": {**_GARCH, "residuos": _ruido(n, escala=1.0)}}, None),
     {"horizonte": 5, "semilla": 1, "n_trayectorias": 1000}, H5),
    ("SIM-MC-001 historia", "SIM-MC-001",
     lambda n: ({"dinamica": {"tipo": "paseo_aleatorio", "mu": 0.0, "sigma": 0.01}, "historia_rendimientos": _ruido(n)}, None),
     {"horizonte": 5, "semilla": 1, "n_trayectorias": 1000}, H5),
    ("SCN-H-001 rendimientos", "SCN-H-001", lambda n: ({"rendimientos": _ruido(n), "garch": {**_GARCH, "fuente": "VOL-GARCH-001"}}, None),
     {"semilla": 1, "n_trayectorias": 1000, "clase": "RV"}, H5),
    ("SCN-H-001 estados del régimen", "SCN-H-001", lambda n: ({"regimen": _estados(n)}, None),
     {"semilla": 1, "n_trayectorias": 1000, "clase": "RV"}, R.UMBRALES["SCN-H-001"]["estados_maximos"]),
    ("BT-DSR-001 rendimientos", "BT-DSR-001",
     lambda n: ({"rendimientos": _ruido(n), "varianza_sr_ensayos": {"valor": 0.5, "unidad": "anual"}}, None), {"N": 10}, H5),
    ("BT-PBO-001 observaciones", "BT-PBO-001", lambda n: ({"rendimientos": {"a": _ruido(n, 1), "b": _ruido(n, 2)}}, None),
     {"S": 8}, H5),
    ("BT-PBO-001 configuraciones", "BT-PBO-001",
     lambda n: ({"rendimientos": {f"c{i:04d}": [float(x) for x in f] for i, f in
                                  enumerate(0.01 * np.random.default_rng(3).standard_normal((n, 64)))}}, None),
     {"S": 8}, R.UMBRALES["BT-PBO-001"]["configuraciones_maximas"]),
    ("BT-VAR-001 VaR previsto", "BT-VAR-001", lambda n: ({"var_previsto": [0.02] * n, "resultados": _ruido(n)}, None), {}, H5),
    ("BT-VAR-001 historia (modo generado)", "BT-VAR-001", lambda n: ({"rendimientos": _ruido(n)}, None), {}, H5),
    ("ML-CAL-001 pares", "ML-CAL-001", lambda n: ({"ensayos": 1, "horizontes": {"H2": _cal(n)}}, None), {"replicas": 10}, H5),
    ("ML-CAL-001 horizontes", "ML-CAL-001", lambda n: ({"ensayos": 1, "horizontes": {f"h{i}": _cal(40) for i in range(n)}}, None),
     {"replicas": 10}, R.UMBRALES["ML-CAL-001"]["horizontes_maximos"]),
    ("ML-PRED-001 observaciones", "ML-PRED-001", lambda n: (_pred(n), None), {"replicas": 10, "pliegues": 2, "rejilla": [1.0]}, H5),
    ("ML-PRED-001 variables", "ML-PRED-001", lambda n: (_pred(420, n), None), {"replicas": 10, "pliegues": 2, "rejilla": [1.0]},
     R.UMBRALES["ML-PRED-001"]["variables_maximas"]),
    ("DEC-VOI-001 muestras", "DEC-VOI-001",
     lambda n: ({**_VOI, "muestras": {"fuente": "SIM-MC-001", "valores": _ruido(n, escala=6.0)}}, None), {"coste_uc": 0.02}, SIMULADA),
]


@pytest.mark.parametrize("nombre,ficha,datos,params,cota", COTAS_DATOS, ids=[c[0] for c in COTAS_DATOS])
def test_h10_cota_de_los_datos_del_grupo_r(nombre, ficha, datos, params, cota):
    """Justo en la cota se sirve; con un elemento más, se rechaza (y lo dice)."""
    valores, series = datos(cota)
    res, _ = _correr(R, ficha, valores, params, series=series)
    assert isinstance(res, dict) and res
    valores, series = datos(cota + 1)
    with pytest.raises(ErrorFicha, match=r"máximo"):
        _correr(R, ficha, valores, params, series=series)


def test_h10_las_cotas_valen_lo_que_dicen_su_ficha_o_la_configuracion():
    assert H5 == 2520 and SIMULADA == 1_000_000
    assert R._observaciones_maximas(None) == H5 and R._MUESTRA_SIMULADA_MAXIMA == SIMULADA
    u = R.UMBRALES
    assert all(u[f]["observaciones_maximas"] == "H5" for f in R.FICHAS if f != "DEC-VOI-001")
    assert u["RISK-VAR-001"]["distribucion_maxima"] == u["DEC-VOI-001"]["muestras_maximas"] == SIMULADA
    assert u["SCN-H-001"]["estados_maximos"] == S.UMBRALES["REG-HMM-001"]["rango_n_estados"][1] == 4
    assert u["ML-CAL-001"]["horizontes_maximos"] == 5
    assert u["BT-PBO-001"]["configuraciones_maximas"] == S.UMBRALES["ST-INF-001"]["contrastes_maximos"] == 1000
    assert u["ML-PRED-001"]["variables_maximas"] == u["ML-PRED-001"]["rejilla_maxima"] == 20


def test_h10_la_cota_de_observaciones_sigue_a_la_configuracion_del_motor():
    cfg = fusionar(cargar_config(), {"horizontes": {"H5": {"meses": 60}}})
    n = sesiones_horizonte(cfg, "H5")
    assert n == 1260
    assert _correr(R, "RISK-VAR-001", {"rendimientos": _ruido(n)}, cfg=cfg)[0]["n"] == n
    with pytest.raises(ErrorFicha, match="máximo 1260"):
        _correr(R, "RISK-VAR-001", {"rendimientos": _ruido(n + 1)}, cfg=cfg)
    assert _correr(R, "RISK-VAR-001", {"rendimientos": _ruido(n + 1)}, cfg=cargar_config())[0]["n"] == n + 1


def test_h10_una_cota_no_se_cambia_desde_la_peticion():
    for ficha, clave in (("BT-PBO-001", "configuraciones_maximas"), ("BT-VAR-001", "observaciones_maximas"),
                         ("DEC-VOI-001", "muestras_maximas")):
        with pytest.raises(ErrorFicha, match="umbrales fijos"):
            _correr(R, ficha, {}, {clave: 10 ** 9})


def test_h10_el_motor_rechaza_enseguida_los_dos_casos_del_revisor(tmp_path):
    """BT-VAR-001 en modo generado con 100 000 rendimientos (GARCH por observación) y BT-PBO-001 con 3 000 configuraciones:
    RECHAZADO con su entrada en RC, sin llegar a calcular."""
    m = _motor(tmp_path)
    r, n = _servir_contando(m, {"operacion": "BT-VAR-001", "datos": [{"valores": {"rendimientos": _ruido(100_000)}}],
                                "parametros": {"metodo_var": "historico_filtrado"}})
    assert r["estado"] == "RECHAZADO" and "máximo 2520" in r["detalle"] and n == 1, r
    conf = {f"c{i:04d}": fila for i, fila in enumerate([_ruido(80, 5)] * 3000)}
    r, n = _servir_contando(m, {"operacion": "BT-PBO-001", "datos": [{"valores": {"rendimientos": conf}}], "parametros": {"S": 20}})
    assert r["estado"] == "RECHAZADO" and "máximo 1000" in r["detalle"] and n == 1, r


# ====================================================================================================== H-11
def _voi(m):
    r = m.servir(_peticion("DEC-VOI-001", 1), "AG-18")
    assert r["estado"].startswith("SERVED"), r
    return r


def _otro_motor(carpeta, **extra):
    """Otro Motor sobre el mismo Registro de cálculos, con otra configuración (un cambio de configuración posterior)."""
    return _motor(carpeta, **extra)


UMBRAL_E_68 = {"parametros_ht03": {"umbrales": {"E": 68}}}


def test_h11_el_registro_apunta_cada_forma_de_leer_la_configuracion():
    for leer, esperadas in ((lambda c: c["a"], {"a"}), (lambda c: c.get("b"), {"b"}), (lambda c: "c" in c, {"c"}),
                            (lambda c: parametro(c, "horizontes.H5"), {"horizontes"}),
                            (lambda c: sesiones_horizonte(c, "H2"), {"horizontes", "calendario"})):
        c = servicio._ConfiguracionLeida({"a": 1, "horizontes": {"H2": {"semanas": 4}, "H5": {"meses": 120}}})
        leer(c)
        assert c.leidas == esperadas
    vacia = servicio._ConfiguracionLeida({})
    assert parametro(vacia, "calendario.sesiones_por_semana") == 5 and vacia.leidas == {"calendario"}   # sale de por_defecto.yaml
    usada = servicio._configuracion_usada({"a": 1}, {"a", "calendario"})
    assert usada["a"]["valor"] == 1 and "valor" not in usada["calendario"] and usada["a"]["por_defecto"] != usada["calendario"]["por_defecto"]


def test_h11_el_artefacto_guarda_la_configuracion_que_uso_la_ficha(tmp_path):
    m = _motor(tmp_path)
    calc = _voi(m)["calc_id"]
    usada = m.almacen.estado("RC")[calc]["artefacto"]["configuracion_usada"]
    assert usada["parametros_ht03"]["valor"] == parametro(m.cfg, "parametros_ht03")
    assert usada["parametros_ht03"]["valor"]["umbrales"]["E"] == 60 and len(usada["parametros_ht03"]["por_defecto"]) == 16
    # una ficha que no lee la configuración lo deja dicho con un registro vacío (no es lo mismo que no tener registro)
    r = m.servir(_peticion(servicio.CASO_AUD_REX), "AG-18")
    assert m.almacen.estado("RC")[r["calc_id"]]["artefacto"]["configuracion_usada"] == {}
    # y las cotas que salen de la configuración también quedan (H5 en sesiones: horizontes y calendario)
    r = m.servir(_peticion("RISK-VAR-001"), "AG-18")
    assert set(m.almacen.estado("RC")[r["calc_id"]]["artefacto"]["configuracion_usada"]) == {"horizontes", "calendario"}


def test_h11_ct10_tras_un_cambio_de_configuracion_reproduce_el_original(tmp_path):
    """El caso del revisor: DEC-VOI-001 servida con el umbral E en 60 y re-ejecutada con el umbral en 68."""
    m = _motor(tmp_path)
    r = _voi(m)
    m68 = _otro_motor(tmp_path, **UMBRAL_E_68)
    assert m68.servir(_peticion("DEC-VOI-001", 1), "AG-18")["resultado"] != r["resultado"]   # el umbral sí cambia la cifra
    out = m68.reejecutar(r["calc_id"], "auditoría tras un cambio de configuración")
    assert (out["coincide"], out["categoria"]) == ("SI", None), out
    rc = m68.almacen.leer("RC")[-1]["reejecucion"]
    assert rc["configuracion"] == {"origen": "artefacto", "distinta_de_la_vigente": ["parametros_ht03"], "sin_registro": []}
    # con la misma configuración, igual que antes: SI y nada distinto
    assert m.reejecutar(r["calc_id"], "auditoría")["coincide"] == "SI"
    assert m.almacen.leer("RC")[-1]["reejecucion"]["configuracion"]["distinta_de_la_vigente"] == []


def test_h11_replicas_e_ic_de_la_configuracion_tambien_viajan_en_el_artefacto(tmp_path):
    m = _motor(tmp_path)
    r = m.servir(_peticion("ML-CAL-001"), "AG-18")
    assert r["estado"].startswith("SERVED"), r
    otro = _otro_motor(tmp_path, evaluacion={"bootstrap_replicas": 500, "nivel_ic": 0.8})
    assert otro.servir(_peticion("ML-CAL-001"), "AG-18")["resultado"] != r["resultado"]
    out = otro.reejecutar(r["calc_id"], "auditoría")
    assert (out["coincide"], out["categoria"]) == ("SI", None), out


def _sin_registro(m, calc_id, cambio=lambda e: None):
    """Copia del artefacto como los anteriores a T-118: sin la configuración usada."""
    e = copy.deepcopy(m.almacen.estado("RC")[calc_id])
    e["artefacto"].pop("configuracion_usada")
    cambio(e)
    e["calc_id"] = m.almacen.nuevo_id("CALC")
    m.almacen.escribir("RC", "AG-13", e)
    return e["calc_id"]


def test_h11_un_artefacto_anterior_se_sigue_pudiendo_reejecutar(tmp_path):
    m = _motor(tmp_path)
    viejo = _sin_registro(m, _voi(m)["calc_id"])
    out = m.reejecutar(viejo, "auditoría")
    assert (out["coincide"], out["categoria"]) == ("SI", None), out
    rc = m.almacen.leer("RC")[-1]["reejecucion"]["configuracion"]
    assert rc["origen"].startswith("vigente") and rc["sin_registro"] == ["_parametros_ht03", "parametros_ht03"]
    # con otra configuración no se puede reproducir, y no se culpa al original: CONVENCION_DISTINTA
    out = _otro_motor(tmp_path, **UMBRAL_E_68).reejecutar(viejo, "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", "CONVENCION_DISTINTA") and out["diferencias"], out
    assert "configuración" in out["diagnostico"]


def _resultado_alterado(e):
    e["resultado"]["payload"]["voi_puntos"] = e["resultado"]["payload"]["voi_puntos"] + 1.0


def test_h11_error_original_solo_con_la_configuracion_registrada_y_vigente(tmp_path):
    m = _motor(tmp_path)
    c = _voi(m)["calc_id"]
    e = copy.deepcopy(m.almacen.estado("RC")[c])
    _resultado_alterado(e)
    e["calc_id"] = m.almacen.nuevo_id("CALC")
    m.almacen.escribir("RC", "AG-13", e)
    # misma configuración, mismos datos, misma versión y otra cifra: el original está mal
    out = m.reejecutar(e["calc_id"], "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", "ERROR_ORIGINAL"), out
    # si la configuración ha cambiado desde entonces, o el artefacto no la guarda, no se afirma tanto
    out = _otro_motor(tmp_path, **UMBRAL_E_68).reejecutar(e["calc_id"], "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", "CONVENCION_DISTINTA"), out
    out = m.reejecutar(_sin_registro(m, c, _resultado_alterado), "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", "CONVENCION_DISTINTA"), out


def test_h11_una_ficha_que_no_lee_la_configuracion_no_cambia_de_categoria(tmp_path):
    """Los artefactos de las fichas que no usan la configuración se clasifican como antes, con registro o sin él y con
    cualquier configuración vigente: una cifra alterada es ERROR_ORIGINAL."""
    m = _motor(tmp_path)
    c = m.servir(_peticion(servicio.CASO_AUD_REX), "AG-18")["calc_id"]

    def alterar(e):
        e["resultado"]["payload"] = {**e["resultado"]["payload"], "_alterado": 1.0}
    out = _otro_motor(tmp_path, **UMBRAL_E_68).reejecutar(_sin_registro(m, c, alterar), "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", "ERROR_ORIGINAL"), out


def test_h11_la_cota_de_la_configuracion_de_entonces_vale_al_reejecutar(tmp_path):
    """Una serie de 1 460 observaciones servida con H5 = 2 520 sesiones se re-ejecuta aunque H5 baje a 1 260: la cota es la
    del artefacto, no la vigente (une H-11, H-12 y H-14)."""
    serie = [float(x) for x in np.where(np.arange(1460) < 700, 0.0, 3.0) + np.sin(np.arange(1460) * 1.7)]
    pet = {"operacion": "FX-BRK-001", "datos": [{"valores": {"serie": serie}}], "parametros": {}}
    m = _motor(tmp_path)
    r = m.servir(copy.deepcopy(pet), "AG-18")
    assert r["estado"].startswith("SERVED"), r
    corto = _otro_motor(tmp_path, horizontes={"H5": {"meses": 60}})
    assert corto.servir(copy.deepcopy(pet), "AG-18")["estado"] == "RECHAZADO"
    out = corto.reejecutar(r["calc_id"], "auditoría")
    assert (out["coincide"], out["categoria"]) == ("SI", None), out


def test_h11_los_seis_casos_de_aud_rex_siguen_superados(tmp_path):
    v = _motor(tmp_path).verificar_casos_control(["AUD-REX-001"])["AUD-REX-001"]
    assert v["superados"] and len(v["casos"]) == 6, v


# ====================================================================================================== H-12
def test_h12_las_cotas_de_s_y_p_salen_de_la_configuracion_por_defecto():
    assert S.OBS_MAXIMAS_SERIES == H5 == S._obs_maximas("FX-BRK-001", None)
    assert S.OBS_MAXIMAS_REGIME == parametro(None, "senales.ventana_anios") * S.SESIONES_POR_ANIO == 756
    assert S.UMBRALES["FX-REGIME-001"]["obs_maximas"] == S._obs_maximas("FX-REGIME-001", None) == 756
    assert P.SESIONES_SEMANA == parametro(None, "calendario.sesiones_por_semana") == 5
    # las cotas que no salen de la configuración no cambian con ella
    cfg = fusionar(cargar_config(), {"horizontes": {"H5": {"meses": 60}}, "senales": {"ventana_anios": 1}})
    assert S._obs_maximas("REG-HMM-001", cfg) == 520 and S._obs_maximas("TEM-DIFF-001", cfg) == 360


@pytest.mark.parametrize("ficha", sorted(S.FICHAS_OBS_H5))
def test_h12_s_la_cota_h5_sigue_a_la_configuracion_del_motor(ficha):
    cfg = fusionar(cargar_config(), {"horizontes": {"H5": {"meses": 60}}})
    assert S._obs_maximas(ficha, cfg) == 1260 and S._obs_maximas(ficha, cargar_config()) == 2520
    assert S._parametros(ficha, {} if ficha != "ST-INF-001" else {"tipo_contraste": "t_una_muestra"}, cfg)["obs_maximas"] == 1260


def test_h12_s_fx_brk_y_fx_regime_por_el_motor(tmp_path):
    """Las dos comprobaciones del revisor: con H5 en 60 meses FX-BRK-001 no sirve 1 460 observaciones, y con una ventana de
    datos de un año FX-REGIME-001 no sirve 600."""
    serie = [float(x) for x in np.where(np.arange(1460) < 700, 0.0, 3.0) + np.sin(np.arange(1460) * 1.7)]
    pet = {"operacion": "FX-BRK-001", "datos": [{"valores": {"serie": serie}}], "parametros": {}}
    assert _motor(tmp_path / "a").servir(copy.deepcopy(pet), "AG-18")["estado"].startswith("SERVED")
    r = _motor(tmp_path / "b", horizontes={"H5": {"meses": 60}}).servir(copy.deepcopy(pet), "AG-18")
    assert r["estado"] == "RECHAZADO" and "1260" in r["detalle"], r
    serie = [float(x) for x in np.random.default_rng(1).normal(0, 1, 600) * np.where((np.arange(600) // 60) % 2, 1, 3)]
    r = _motor(tmp_path / "c", senales={"ventana_anios": 1}).servir(
        {"operacion": "FX-REGIME-001", "datos": [{"valores": {"serie": serie}}], "parametros": {}}, "AG-18")
    assert r["estado"] == "RECHAZADO" and "252" in r["detalle"], r
    with pytest.raises(ErrorFicha, match="252"):
        S.FICHAS["FX-REGIME-001"]["fn"]({"valores": {"serie": serie}, "configuracion": {"senales": {"ventana_anios": 1}}}, {})


def test_h12_p_las_sesiones_por_semana_salen_de_la_configuracion_del_motor():
    v = _valores("CHR-FLOW-001")
    tope = P.SEMANAS_H2_MAX * P.SESIONES_SEMANA
    assert tope == P.UMBRALES["CHR-FLOW-001"]["ventana_sesiones_maxima"] == 40
    assert _correr(P, "CHR-FLOW-001", copy.deepcopy(v), {"ventanas": [tope]})[0]
    with pytest.raises(ErrorFicha, match="ventanas"):
        _correr(P, "CHR-FLOW-001", copy.deepcopy(v), {"ventanas": [tope + 1]})
    cfg = fusionar(cargar_config(), {"calendario": {"sesiones_por_semana": 4}})
    assert _correr(P, "CHR-FLOW-001", copy.deepcopy(v), {"ventanas": [32]}, cfg=cfg)[0]
    with pytest.raises(ErrorFicha, match="ventanas"):
        _correr(P, "CHR-FLOW-001", copy.deepcopy(v), {"ventanas": [33]}, cfg=cfg)
    with pytest.raises(ErrorFicha, match="configuración"):
        _correr(P, "CHR-FLOW-001", copy.deepcopy(v), cfg=["no es un objeto"])


# ====================================================================================================== H-13
def _profunda(n):
    """Una lista con otras `n` dentro, una en otra."""
    x = []
    for _ in range(n):
        x = [x]
    return x


def test_h13_la_profundidad_se_mide_sin_recursion_y_tiene_borde():
    tope = servicio.PROFUNDIDAD_MAXIMA
    assert not servicio._demasiado_anidado(_profunda(tope - 1)) and servicio._demasiado_anidado(_profunda(tope))
    assert servicio._demasiado_anidado({"a": {"b": _profunda(tope - 2)}}) and not servicio._demasiado_anidado({"a": _profunda(tope - 2)})
    assert servicio._demasiado_anidado(_profunda(100_000))   # sin RecursionError
    assert servicio._demasiado_anidado({(((),),): 1}, 2)       # también las claves
    peor = max(servicio._demasiado_anidado(_peticion(f, i), 9) for f, cs in servicio.CASOS_CONTROL.items() for i in range(len(cs)))
    assert not peor   # ningún caso de control pasa de 9 niveles: la cota (32) queda muy por encima


@pytest.mark.parametrize("niveles", [500, 3000])
@pytest.mark.parametrize("campo", ["valores", "parametros", "semilla", "perfil", "clase", "horizonte", "modo", "prioridad"])
@pytest.mark.parametrize("ficha", ["SIM-MC-001", "REI-CAP-001"])
def test_h13_un_campo_anidado_en_profundidad_no_tumba_el_motor(tmp_path, ficha, campo, niveles):
    m = _motor(tmp_path)
    pet = _peticion(ficha)
    if campo == "valores":
        pet["datos"][0]["valores"]["_anidado"] = _profunda(niveles)
    elif campo == "parametros":
        pet["parametros"]["_anidado"] = _profunda(niveles)
    else:
        pet[campo] = _profunda(niveles)
    r, n = _servir_contando(m, pet)
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "DATOS_INCOHERENTES" and n == 1, r


def test_h13_el_borde_de_la_profundidad_por_el_motor(tmp_path):
    """La petición es el nivel 0, `datos` el 1, cada dato el 2, `valores` el 3 y la clave nueva el 4."""
    m = _motor(tmp_path)
    tope = servicio.PROFUNDIDAD_MAXIMA
    pet = _peticion("REI-CAP-001")
    pet["datos"][0]["valores"]["_anidado"] = _profunda(tope - 5)
    r, n = _servir_contando(m, pet)
    assert r["estado"].startswith("SERVED") and n == 1, r
    pet = _peticion("REI-CAP-001")
    pet["datos"][0]["valores"]["_anidado"] = _profunda(tope - 4)
    r, n = _servir_contando(m, pet)
    assert r["estado"] == "RECHAZADO" and "anidamiento" in r["detalle"] and n == 1, r


def test_h13_segunda_barrera_la_copia_de_los_valores_no_escapa(tmp_path, monkeypatch):
    """Aunque la comprobación de la forma dejara pasar unos valores muy anidados, la copia que agota la pila se convierte
    en RECHAZADO (el caso (a) del hallazgo, en el sitio donde escapaba)."""
    monkeypatch.setattr(servicio, "_demasiado_anidado", lambda *_: False)
    m = _motor(tmp_path)
    pet = _peticion("REI-CAP-001")
    pet["datos"][0]["valores"]["_anidado"] = _profunda(3000)
    r, n = _servir_contando(m, pet)
    assert r["estado"] == "RECHAZADO" and "RecursionError" in r["detalle"] and n == 1, r


@pytest.mark.parametrize("campo", ["semilla", "perfil", "clase"])
@pytest.mark.parametrize("ficha", ["SIM-MC-001", "REI-CAP-001"])
def test_h13_un_array_de_numpy_en_la_peticion_no_tumba_el_motor(tmp_path, ficha, campo):
    m = _motor(tmp_path)
    r, n = _servir_contando(m, _peticion(ficha, **{campo: np.array([1, 2])}))
    assert n == 1 and r["estado"] in ("RECHAZADO", "SERVED", "SERVED_WITH_LIMITATIONS"), r
    if campo != "semilla" or ficha in servicio.ACEPTA_SEMILLA:
        assert r["estado"] == "RECHAZADO", r   # una semilla que la ficha no usa no cambia nada


def test_h13_dos_semillas_que_no_se_pueden_comparar_son_dos_semillas(tmp_path):
    m = _motor(tmp_path)
    pet = _peticion("SIM-MC-001", semilla=np.array([1, 2]))
    pet["parametros"]["semilla"] = np.array([1, 2])
    r, n = _servir_contando(m, pet)
    assert r["estado"] == "RECHAZADO" and "dos semillas" in r["detalle"] and n == 1, r
    assert servicio._distintas(1, 2) and not servicio._distintas(7, 7.0) and not servicio._distintas(np.array([7]), np.array([7]))


@pytest.mark.parametrize("campo,valor", [("clase", 0), ("clase", ["RV"]), ("clase", b"RV"), ("perfil", 3), ("perfil", {"a": 1}),
                                         ("perfil", {1, 2})])
def test_h13_clase_y_perfil_tienen_tipo(tmp_path, campo, valor):
    r, n = _servir_contando(_motor(tmp_path), _peticion("REI-CAP-001", **{campo: valor}))
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "DATOS_INCOHERENTES" and n == 1, r


def test_h13_la_peticion_bien_formada_se_sirve_igual(tmp_path):
    m = _motor(tmp_path)
    for extra in ({}, {"clase": "INM"}, {"perfil": ["INM"]}, {"perfil": "TRANSVERSAL"}, {"perfil": ("INM",)}, {"clase": None}):
        assert m.servir(_peticion("REI-CAP-001", **extra), "AG-18")["estado"].startswith("SERVED"), extra


# ====================================================================================================== H-14
def test_h14_reejecutar_registra_la_reejecucion_que_la_ficha_rechaza(tmp_path):
    """Un artefacto con un tamaño que hoy queda fuera de la cota (servido antes de ella): la re-ejecución no escapa como
    ErrorFicha; queda una entrada REEJECUCION con `coincide` NO y la categoría ERROR_REEJECUCION."""
    m = _motor(tmp_path)
    r = m.servir(_peticion("SIM-MC-001"), "AG-18")
    e = copy.deepcopy(m.almacen.estado("RC")[r["calc_id"]])
    e["parametros"]["n_trayectorias"] = 10 ** 9
    e["calc_id"] = m.almacen.nuevo_id("CALC")
    m.almacen.escribir("RC", "AG-13", e)
    antes = len(m.almacen.leer("RC"))
    out = m.reejecutar(e["calc_id"], "auditoría")
    assert (out["coincide"], out["categoria"], out["diferencias"]) == ("NO", "ERROR_REEJECUCION", []), out
    assert "n_trayectorias" in out["diagnostico"]
    rc = m.almacen.leer("RC")
    assert len(rc) == antes + 1 and rc[-1]["tipo_entrada"] == "REEJECUCION" and rc[-1]["calc_id"] == out["calc_id"]
    ree = rc[-1]["reejecucion"]
    assert ree["calc_original"] == e["calc_id"] and ree["categoria"] == "ERROR_REEJECUCION" and ree["doble_pasada"] is False
    assert ree["diagnostico"].startswith("ERROR_REEJECUCION") and "ErrorFicha" in ree["diagnostico"]


def test_h14_sin_motivo_o_sin_artefacto_sigue_siendo_imposible(tmp_path):
    """Lo que ya era imposible (R16: no se reconstruye por inferencia) lo sigue siendo, con su excepción."""
    m = _motor(tmp_path)
    r = m.servir(_peticion("SIM-MC-001"), "AG-18")
    with pytest.raises(ValueError, match="sin motivo"):
        m.reejecutar(r["calc_id"], " ")
    with pytest.raises(KeyError):
        m.reejecutar("CALC-0000-9999", "auditoría")
