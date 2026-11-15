"""T-121 · Hallazgos abiertos de la QA r01 de T-118 (`.docs/tickets/T-118/qa.md`): una regresión por corrección.

- H-04: las 14 fichas de la Fase 1 que servían datos en línea posteriores a la fecha de corte los rechazan (el dato del día
  del corte se sirve, también con hora); las fechas futuras por naturaleza (reuniones, efectividad anunciada) no.
- H-01: CT-10 da ERROR_ORIGINAL si la re-ejecución usó la configuración guardada en el artefacto y aun así difiere, cambie
  o no la vigente; CONVENCION_DISTINTA solo si falta esa configuración o su parte de `por_defecto.yaml` ya no es la de
  entonces.
- H-02: ninguna excepción escapa de `Motor.servir` con un texto que no se puede escribir, un valor que no es JSON o unos
  argumentos `solicitante`, `run_id` y `msg_id` raros: RECHAZADO y una entrada en RC.
- H-03: `reejecutar` deja su entrada REEJECUCION (NO / ERROR_REEJECUCION) si los datos del artefacto ya no se pueden
  resolver o el artefacto está alterado.
- H-05: la cota de REG-HMM-001 sale de `horizontes.H5` (en semanas), no va escrita a mano.
(H-06, las cinco pruebas de los mutantes M05, M38, M50, M68 y M78, están en `test_t118_hallazgos.py`: el script del
revisor las filtra por el nombre de su hallazgo de origen.)
"""
import copy
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config, fusionar, parametro
from bloque_a.motor import fichas_fon_der, fichas_mon_idx, fichas_tcv, servicio
from bloque_a.motor import fichas_series as S
from bloque_a.motor.operaciones import ErrorFicha


class _Proveedor:
    as_of = None
    nombre = "pruebas"


def _motor(carpeta, proveedor=None, **extra):
    return servicio.Motor(Almacen(Path(carpeta)), proveedor or _Proveedor(), cargar_config(extra=extra or None))


def _peticion(ficha, i=0, **extra):
    caso = servicio.CASOS_CONTROL[ficha][i]
    return {"operacion": ficha, "datos": copy.deepcopy(caso.get("datos") or []),
            "parametros": dict(caso.get("parametros") or {}), **extra}


def _servir_contando(m, pet, solicitante="AG-18", **kw):
    antes = len(m.almacen.leer("RC"))
    r = m.servir(pet, solicitante, **kw)   # si escapa una excepción, la prueba falla aquí
    return r, len(m.almacen.leer("RC")) - antes


# ====================================================================================================== H-04
FASE1 = ("FON-DISC-001", "FON-FLOW-001", "FON-LEV-001", "IDX-CONC-001", "IDX-ERP-001", "IDX-REL-001", "MON-FIX-001",
         "MON-REAL-001", "MON-YLD-001", "TCV-BEI-001", "TCV-CDS-001", "TCV-SLOPE-001", "TCV-TP-001", "TCV-VIXTS-001")
CASOS_FASE1 = [(f, i) for f in FASE1 for i in range(len(servicio.CASOS_CONTROL[f]))]
_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}")
# Hojas cuyo desplazamiento al día siguiente del corte lo rechaza otra regla antes que la del corte (el periodo de MON-REAL
# deja de medir su plazo; el regresor de TCV-SLOPE se conoce después de usarse): también es un rechazo, con otro motivo
OTRA_REGLA = {("MON-REAL-001", "divisas/EUR/historia/#/fecha_inicio"), ("MON-REAL-001", "divisas/EUR/historia/#/fecha_fin"),
              ("FON-FLOW-001", "fechas/#")}


def _hojas_fecha(x, ruta=()):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from _hojas_fecha(v, ruta + (k,))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from _hojas_fecha(v, ruta + (i,))
    elif isinstance(x, str) and _FECHA.match(x):
        yield ruta, x


def _ultima_fecha(pet):
    return max(x[:10] for d in pet["datos"] for _, x in _hojas_fecha(d.get("valores") or {}))


def _dia(fecha, dias):
    return str((pd.Timestamp(fecha) + pd.Timedelta(days=dias)).date())


def test_h04_son_las_catorce_fichas_del_hallazgo_y_todas_tienen_datos_fechados():
    assert len(FASE1) == 14 and all(servicio.servible(f) for f in FASE1)
    assert len(CASOS_FASE1) == 42 and all(_ultima_fecha(_peticion(f, i)) for f, i in CASOS_FASE1)


@pytest.mark.parametrize("ficha,i", CASOS_FASE1, ids=[f"{f}:{i}" for f, i in CASOS_FASE1])
def test_h04_corte_en_la_ultima_fecha_se_sirve_igual_y_en_la_vispera_se_rechaza(tmp_path, ficha, i):
    """El caso del revisor (`r01_01_h09_fecha_corte.py`, bloque 2): con el corte en la víspera de la última fecha de los
    datos, RECHAZADO; con el corte en ese mismo día, el resultado es el de siempre (sin corte), y el caso de control pasa."""
    m = _motor(tmp_path)
    ultima = _ultima_fecha(_peticion(ficha, i))
    sin_corte = m.servir(_peticion(ficha, i), "AG-21")
    con_corte = m.servir(_peticion(ficha, i, fecha_corte=ultima), "AG-21")
    assert con_corte["estado"].startswith("SERVED"), con_corte
    assert con_corte["resultado"] == sin_corte["resultado"] and con_corte["limitaciones"] == sin_corte["limitaciones"]
    assert servicio.CASOS_CONTROL[ficha][i]["comprobar"](con_corte["resultado"])
    r, n = _servir_contando(m, _peticion(ficha, i, fecha_corte=_dia(ultima, -1)), "AG-21")
    assert r["estado"] == "RECHAZADO" and "posterior a la fecha de corte" in r["detalle"] and n == 1, r
    assert "no conocible" in r["detalle"] and ultima in r["detalle"]


@pytest.mark.parametrize("ficha", FASE1)
def test_h04_cada_campo_fechado_posterior_al_corte_se_rechaza(tmp_path, ficha):
    """Campo a campo: con el corte en la última fecha de los datos, la última fecha de cada lista (o cada fecha suelta)
    llevada al día siguiente se rechaza; no basta con comprobar un campo por ficha."""
    m = _motor(tmp_path)
    probados = 0
    for i in range(len(servicio.CASOS_CONTROL[ficha])):
        base = _peticion(ficha, i)
        ultima = _ultima_fecha(base)
        vistos = set()
        for j, d in enumerate(base["datos"]):
            for ruta, x in _hojas_fecha(d.get("valores") or {}):
                padre = d["valores"]
                for k in ruta[:-1]:
                    padre = padre[k]
                if isinstance(ruta[-1], int) and ruta[-1] != len(padre) - 1:
                    continue
                nombre = "/".join("#" if isinstance(k, int) else str(k) for k in ruta)
                if (j, nombre) in vistos:
                    continue
                vistos.add((j, nombre))
                pet = _peticion(ficha, i, fecha_corte=ultima)
                hoja = pet["datos"][j]["valores"]
                for k in ruta[:-1]:
                    hoja = hoja[k]
                hoja[ruta[-1]] = _dia(ultima, 1) + x[10:]
                r, n = _servir_contando(m, pet, "AG-21")
                assert r["estado"] == "RECHAZADO" and n == 1, (ficha, i, nombre, r)
                if (ficha, nombre) not in OTRA_REGLA and "conocible_desde" not in nombre:
                    assert "posterior a la fecha de corte" in r["detalle"], (ficha, i, nombre, r["detalle"])
                probados += 1
    assert probados >= len(servicio.CASOS_CONTROL[ficha])


def test_h04_el_dato_con_hora_del_dia_del_corte_es_conocible():
    """Se compara por día en los tres módulos: las 23:59 del día del corte se sirven; el día siguiente, no."""
    hora, dia_sig = pd.Timestamp("2024-01-19T23:59:59"), pd.Timestamp("2024-01-20T00:00:00")
    corte = fichas_mon_idx._corte({"fecha_corte": "2024-01-19T08:00:00"})
    assert fichas_mon_idx._hasta_corte([hora], corte, "x") is None
    with pytest.raises(ErrorFicha, match="posterior a la fecha de corte"):
        fichas_mon_idx._hasta_corte([dia_sig], corte, "x")
    ent = {"fecha_corte": "2024-01-19T08:00:00"}
    assert fichas_fon_der._hasta_corte_peticion(pd.DatetimeIndex([hora]), ent, "F", "fechas") is None
    with pytest.raises(ErrorFicha, match="posterior a la fecha de corte"):
        fichas_fon_der._hasta_corte_peticion(pd.DatetimeIndex([dia_sig]), ent, "F", "fechas")
    c = fichas_tcv._corte(ent)
    assert fichas_tcv._hasta_corte([hora.date()], c, "x") is None
    with pytest.raises(ErrorFicha, match="posterior a la fecha de corte"):
        fichas_tcv._hasta_corte([dia_sig.date()], c, "x")
    # sin corte no hay nada que comprobar; un corte que no es una fecha se rechaza
    assert fichas_mon_idx._corte({}) is None and fichas_tcv._corte({}) is None
    for raro in (20240119, True, ["2024-01-19"], "no es una fecha"):
        with pytest.raises(ErrorFicha):
            fichas_tcv._corte({"fecha_corte": raro})


def test_h04_tcv_tp_una_segunda_via_posterior_al_corte_rechaza_la_peticion(tmp_path):
    """La segunda vía (encuesta) de TCV-TP-001 con ACM no se degrada a limitación si su dato es posterior al corte: es una
    observación no conocible y rechaza la petición, como la vía principal."""
    acm = _peticion("TCV-TP-001", 0)
    enc = next(d["valores"]["encuesta"] for d in _peticion("TCV-TP-001", 3)["datos"] if "encuesta" in d.get("valores", {}))
    acm["datos"][0]["valores"]["encuesta"] = copy.deepcopy(enc)
    acm["datos"][0]["valores"].setdefault("rendimientos_pct", next(
        d["valores"]["rendimientos_pct"] for d in _peticion("TCV-TP-001", 3)["datos"] if "rendimientos_pct" in d["valores"]))
    ultima_curva = acm["datos"][0]["valores"]["curva"]["fechas"][-1]
    m = _motor(tmp_path)
    acm["fecha_corte"] = max(ultima_curva, enc["fecha"])
    assert m.servir(copy.deepcopy(acm), "AG-21")["estado"].startswith("SERVED")
    acm["datos"][0]["valores"]["encuesta"]["fecha"] = _dia(acm["fecha_corte"], 1)
    r, n = _servir_contando(m, acm, "AG-21")
    assert r["estado"] == "RECHAZADO" and "encuesta.fecha" in r["detalle"] and "posterior" in r["detalle"] and n == 1, r


@pytest.mark.parametrize("ficha", ["MON-EXP-001", "IDX-REB-001"])
def test_h04_las_fechas_futuras_por_naturaleza_no_son_observaciones(tmp_path, ficha):
    """Reuniones de un banco central y la efectividad de un rebalanceo anunciado son posteriores al corte por naturaleza:
    con el corte en la víspera de la última (que es una de ellas) se sirve igual; la fecha de los datos sí se compara."""
    m = _motor(tmp_path)
    pet = _peticion(ficha)
    ultima = _ultima_fecha(pet)
    sin_corte = m.servir(_peticion(ficha), "AG-21")
    r = m.servir(_peticion(ficha, fecha_corte=_dia(ultima, -1)), "AG-21")
    assert r["estado"].startswith("SERVED") and r["resultado"] == sin_corte["resultado"], r
    v = pet["datos"][0]["valores"]
    observada = v["fecha"] if ficha == "MON-EXP-001" else v["evento"]["fecha_anuncio"]
    r = m.servir(_peticion(ficha, fecha_corte=_dia(observada, -1)), "AG-21")
    assert r["estado"] == "RECHAZADO" and "posterior a la fecha de corte" in r["detalle"], r


# Bloques opcionales fechados que los casos de control no traen (mutantes C02…C26 de `mut_t121.py`): con el corte en la
# última fecha observada se calcula; con la última fecha del bloque un día después del corte, la ficha rechaza.
def _seg(nombre, valor):
    return {"segmento": nombre, "convencion": "simple_365", "valor": valor, "plazo_meses": 3, "dias": 91, "divisa": "EUR",
            "fecha": "2026-11-10"}


def _mon_yld():
    hist = [{"fecha": f"{2015 + i // 4}-{1 + 3 * (i % 4):02d}-15", "valor_pb": float(i % 7)} for i in range(40)]
    v = {"segmentos": [_seg("a", 0.03), _seg("b", 0.0301)], "historia_diferenciales": {"a − b · EUR · 3m": hist}}
    return v, {"base_salida": "Act/365"}, {}, "2026-11-10", lambda v, d: v["historia_diferenciales"]["a − b · EUR · 3m"][-1].update(fecha=d)


def _mon_exp():
    d_r = (pd.Timestamp("2026-12-17") - pd.Timestamp("2026-11-12")).days
    v = {"fecha": "2026-11-12", "base_curva": 360, "tipo_oficial": 0.02, "diferencial_estable": 0.0008,
         "curva": fichas_mon_idx._curva_senda([0, d_r], [0.0192, 0.0167], [30, 90, 180, 365], 360),
         "reuniones": ["2026-12-17"], "decisiones": [{"fecha": "2026-10-30", "tipo_decidido": 0.02, "tipo_esperado": 0.0205}]}
    return v, {}, {}, "2026-11-12", lambda v, d: v["decisiones"][0].update(fecha=d)


def _mon_real():
    v = fichas_mon_idx._datos_mon_real(pi_cero=False)
    fechas = pd.date_range("2014-03-31", "2026-09-30", freq="QE")
    v["divisas"]["EUR"]["historia_ex_ante"] = [{"fecha": f.date().isoformat(), "valor": 0.001 * (i % 9)}
                                               for i, f in enumerate(fechas)]
    return v, {}, {}, "2026-10-15", lambda v, d: v["divisas"]["EUR"]["historia_ex_ante"][-1].update(fecha=d)


def _idx_erp():
    v = fichas_mon_idx._datos_idx_erp(gordon=True)
    v.pop("crecimiento_real_bpa")
    fechas = pd.date_range("2000-01-31", periods=25 * 12 + 1, freq="ME")
    v["historia_bpa_real"] = [{"fecha": f.date().isoformat(), "valor": 100 * 1.02 ** (i / 12)} for i, f in enumerate(fechas)]
    corte = max(x[:10] for _, x in _hojas_fecha(v))
    return v, {}, {}, corte, lambda v, d: v["historia_bpa_real"][-1].update(fecha=d)


def _idx_conc_precios():
    fechas = pd.bdate_range("2025-06-02", periods=300)
    v = {"composicion": fichas_mon_idx._composicion(20, igual=True),
         "precios": {"C00": [{"fecha": f.date().isoformat(), "precio": 100 + i} for i, f in enumerate(fechas)]}}
    return v, {}, {}, "2026-10-31", lambda v, d: v["precios"]["C00"][-1].update(fecha=d)


def _idx_conc_indices():
    fechas = pd.bdate_range("2025-06-02", periods=320)
    v = {"composicion": fichas_mon_idx._composicion(20, igual=True),
         "indice_ponderado": [{"fecha": f.date().isoformat(), "valor": 100 * 1.001 ** i} for i, f in enumerate(fechas)],
         "indice_equiponderado": [{"fecha": f.date().isoformat(), "valor": 100.0} for f in fechas]}
    return v, {}, {}, "2026-10-31", lambda v, d: v["indice_ponderado"][-1].update(fecha=d)


def _idx_conc_historia():
    fechas = pd.date_range("2010-01-31", "2026-09-30", freq="ME")
    hist = [{"fecha": f.date().isoformat(), "peso_top_n": 0.2 + 0.001 * i, "hhi": 0.01 + 0.0001 * i, "n_ef": 100 - 0.1 * i,
             "hhi_sectorial": 0.15} for i, f in enumerate(fechas)]
    v = {"composicion": fichas_mon_idx._composicion(30, igual=False), "historia_metricas": hist}
    return v, {}, {}, "2026-10-31", lambda v, d: v["historia_metricas"][-1].update(fecha=d)


def _idx_reb_comparables():
    v = {"evento": fichas_mon_idx._evento_reb(), "eventos_comparables": copy.deepcopy(fichas_mon_idx._EV)}
    return v, {}, {}, "2026-11-20", lambda v, d: v["eventos_comparables"][0]["rentabilidades"][-1].update(fecha=d)


def _idx_reb_aum():
    return {"evento": fichas_mon_idx._evento_reb()}, {}, {}, "2026-11-20", \
        lambda v, d: v["evento"]["activos_indexados"].update(fecha=d)


def _tcv_bei():
    caso = fichas_tcv.CASOS_CONTROL["TCV-BEI-001"][0]
    v = {}
    for dd in caso["datos"]:
        v.update(copy.deepcopy(dd["valores"]))
    fechas = pd.date_range("2010-01-01", "2024-05-01", freq="MS").strftime("%Y-%m-%d").tolist()
    v["historia"] = {"fechas": fechas, "breakevens": {"10": [2.0 + 0.001 * i for i in range(len(fechas))]}}
    return v, dict(caso.get("parametros") or {}), {}, "2024-06-01", lambda v, d: v["historia"]["fechas"].__setitem__(-1, d)


def _tcv_tp_publicado():
    fechas = pd.date_range("2010-01-01", periods=181, freq="MS").strftime("%Y-%m-%d").tolist()
    v = {"serie_publicada": {"fuente": "Kim-Wright (sintética)", "fechas": fechas,
                             "primas_pb": {"10": [10.0 + i * 0.5 for i in range(181)]},
                             "rendimientos_pct": {"10": [3.0 + i * 0.01 for i in range(181)]}}}
    return v, {"metodo": "publicado"}, {}, fechas[-1], lambda v, d: v["serie_publicada"]["fechas"].__setitem__(-1, d)


OPCIONALES = {"MON-YLD-001 historia_diferenciales": ("MON-YLD-001", _mon_yld),
              "MON-EXP-001 decisiones": ("MON-EXP-001", _mon_exp),
              "MON-REAL-001 historia_ex_ante": ("MON-REAL-001", _mon_real),
              "IDX-ERP-001 historia_bpa_real": ("IDX-ERP-001", _idx_erp),
              "IDX-CONC-001 precios": ("IDX-CONC-001", _idx_conc_precios),
              "IDX-CONC-001 indice_ponderado": ("IDX-CONC-001", _idx_conc_indices),
              "IDX-CONC-001 historia_metricas": ("IDX-CONC-001", _idx_conc_historia),
              "IDX-REB-001 eventos_comparables": ("IDX-REB-001", _idx_reb_comparables),
              "IDX-REB-001 activos_indexados": ("IDX-REB-001", _idx_reb_aum),
              "TCV-BEI-001 historia": ("TCV-BEI-001", _tcv_bei),
              "TCV-TP-001 serie_publicada": ("TCV-TP-001", _tcv_tp_publicado)}


@pytest.mark.parametrize("nombre", sorted(OPCIONALES))
def test_h04_un_bloque_opcional_fechado_despues_del_corte_se_rechaza(nombre):
    ficha, construir = OPCIONALES[nombre]
    fn = servicio.IMPLEMENTADAS[ficha]["fn"]
    v, params, series, corte, mover = construir()

    def correr(valores):
        return fn({"valores": valores, "series": series, "series_rol": {}, "configuracion": None, "fecha_corte": corte},
                  dict(params))

    res, _ = correr(copy.deepcopy(v))                      # con el corte en la última fecha observada, se calcula
    assert res
    mover(v, _dia(corte, 1))
    with pytest.raises(ErrorFicha, match="posterior a la fecha de corte"):
        correr(v)


# ====================================================================================================== H-01
UMBRAL_E_68 = {"parametros_ht03": {"umbrales": {"E": 68}}}


def _voi(m):
    r = m.servir(_peticion("DEC-VOI-001", 1), "AG-18")
    assert r["estado"].startswith("SERVED"), r
    return r


def _copia(m, calc_id, cambio):
    e = copy.deepcopy(m.almacen.estado("RC")[calc_id])
    cambio(e)
    e["calc_id"] = m.almacen.nuevo_id("CALC")
    m.almacen.escribir("RC", "AG-13", e)
    return e["calc_id"]


def _alterar_voi(e):
    e["resultado"]["payload"]["voi_puntos"] = e["resultado"]["payload"]["voi_puntos"] + 1.0


@pytest.mark.parametrize("cambio", [UMBRAL_E_68, {"parametros_ht03": {"cambio_material": 0.123}}],
                         ids=["clave_leida", "otra_clave_de_la_seccion"])
def test_h01_error_real_del_original_es_error_original_aunque_cambie_la_vigente(tmp_path, cambio):
    """El caso del revisor (`r01_03_h11_ct10_configuracion.py`, bloque 5): artefacto con el registro de configuración
    completo y una cifra alterada. Con otra configuración vigente (la clave leída u otra de la misma sección), la
    re-ejecución usa la del artefacto: el que difiere es el original."""
    m = _motor(tmp_path)
    alterado = _copia(m, _voi(m)["calc_id"], _alterar_voi)
    otro = _motor(tmp_path, **cambio)
    out = otro.reejecutar(alterado, "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", "ERROR_ORIGINAL") and out["diferencias"], out
    conf = otro.almacen.leer("RC")[-1]["reejecucion"]["configuracion"]
    assert conf["origen"] == "artefacto" and conf["distinta_de_la_vigente"] == ["parametros_ht03"]
    # el artefacto bueno se reproduce con esa misma configuración vigente
    bueno = next(k for k, e in otro.almacen.estado("RC").items() if e.get("tipo_entrada") == "SERVICIO" and k != alterado)
    assert otro.reejecutar(bueno, "auditoría")["coincide"] == "SI"


def test_h01_riesgo_con_otra_clave_de_horizontes_es_error_original(tmp_path):
    m = _motor(tmp_path)
    r = m.servir(_peticion("RISK-VAR-001"), "AG-18")
    assert r["estado"].startswith("SERVED"), r
    payload = r["resultado"]

    def alterar(e):
        clave = next(k for k, x in e["resultado"]["payload"].items() if isinstance(x, float))
        e["resultado"]["payload"][clave] = e["resultado"]["payload"][clave] * 2 + 1

    assert any(isinstance(x, float) for x in payload.values())
    alterado = _copia(m, r["calc_id"], alterar)
    out = _motor(tmp_path, horizontes={"H1": {"sesiones": 7}}).reejecutar(alterado, "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", "ERROR_ORIGINAL"), out


def _por_defecto_de_entonces(valor):
    """El artefacto se calculó con otro `por_defecto.yaml` (otra huella de la sección) y con `valor` como sección."""
    def alterar(e):
        _alterar_voi(e)
        reg = e["artefacto"]["configuracion_usada"]["parametros_ht03"]
        reg["por_defecto"] = "0123456789abcdef"
        if valor is None:
            reg.pop("valor")
        else:
            reg["valor"] = valor(reg["valor"])
    return alterar


def _sin_una_clave(v):
    v = copy.deepcopy(v)
    v.pop("max_por_cluster")   # una clave que DEC-VOI-001 no usa: la ficha se re-ejecuta igual
    return v


@pytest.mark.parametrize("valor,categoria", [(None, "CONVENCION_DISTINTA"), (_sin_una_clave, "ERROR_ORIGINAL")],
                         ids=["sin_valor", "valor_parcial"])
def test_h01_convencion_distinta_si_la_parte_de_por_defecto_que_se_uso_ya_no_es_la_de_entonces(tmp_path, valor, categoria):
    """Una sección guardada sin valor cuyo `por_defecto` (de donde `parametro` la toma) ya no es el vigente: la
    re-ejecución no ha podido reproducir sus condiciones y no se culpa al original. T-127 (QA r01 de T-121, H-07): con un
    valor guardado al que le falta una clave que DEC-VOI-001 no usa, la ficha lee la sección guardada entera y no toma
    nada de `por_defecto.yaml` (`parametro` no mezcla una sección encontrada con la del fichero): el que difiere es el
    original. Antes se daba CONVENCION_DISTINTA porque el valor «no cubría» las claves del fichero."""
    m = _motor(tmp_path)
    out = m.reejecutar(_copia(m, _voi(m)["calc_id"], _por_defecto_de_entonces(valor)), "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", categoria), out
    if categoria == "CONVENCION_DISTINTA":
        assert "parametros_ht03" in out["diagnostico"] and "por_defecto.yaml" in out["diagnostico"]


def test_h01_un_cambio_de_por_defecto_que_el_valor_guardado_cubre_no_ablanda_la_categoria(tmp_path):
    """Tras la sesión T-57, que cambiará `por_defecto.yaml`: el artefacto guarda la sección entera, la re-ejecución no toma
    nada del fichero nuevo, y un resultado alterado sigue siendo ERROR_ORIGINAL."""
    m = _motor(tmp_path)
    out = m.reejecutar(_copia(m, _voi(m)["calc_id"], _por_defecto_de_entonces(lambda v: v)), "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", "ERROR_ORIGINAL"), out
    # T-127 (H-07): la regla ya no compara el valor guardado con las claves del fichero (`_cubre`), sino lo que la
    # re-ejecución ha tomado de él: las rutas que `parametro` no encuentra en la configuración de la ficha
    leida = servicio._ConfiguracionLeida({"a": {"b": 1}})
    assert parametro(leida, "a.b") == 1 and leida.respaldos == set()
    parametro(leida, "horizontes.H5")
    assert leida.respaldos == {"horizontes.H5"}


def test_h01_sin_la_configuracion_en_el_artefacto_sigue_siendo_convencion_distinta(tmp_path):
    m = _motor(tmp_path)

    def alterar(e):
        _alterar_voi(e)
        e["artefacto"].pop("configuracion_usada")

    out = _motor(tmp_path, **UMBRAL_E_68).reejecutar(_copia(m, _voi(m)["calc_id"], alterar), "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", "CONVENCION_DISTINTA"), out


# ====================================================================================================== H-02
class _Raro:
    """Un objeto que no se puede copiar."""

    def __deepcopy__(self, memo):
        raise TypeError("no se copia")


def _circular():
    x: list = []
    x.append(x)
    return x


def _generador():
    return (i for i in range(3))


@pytest.mark.parametrize("campo", ["operacion", "horizonte", "modo", "plan", "prioridad", "fecha_corte"])
def test_h02_un_sustituto_unicode_suelto_es_un_rechazo_en_rc(tmp_path, campo):
    """El caso mínimo del revisor: un texto con "\\ud800" (que `json.loads` produce) no se puede escribir en UTF-8."""
    m = _motor(tmp_path)
    r, n = _servir_contando(m, _peticion("REI-CAP-001", **{campo: "\ud800"}))
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "DATOS_INCOHERENTES" and n == 1, r
    assert m.almacen.leer("RC")[-1]["tipo_entrada"] == "RECHAZO"


@pytest.mark.parametrize("donde", ["serie", "rol", "inicio", "fin"])
def test_h02_un_sustituto_unicode_en_un_dato_de_ht01_es_un_rechazo_en_rc(tmp_path, donde):
    m = _motor(tmp_path)
    dato = {"serie": "SPY", "rol": "serie", "inicio": "2020-01-01", "fin": "2020-12-31", donde: "\ud800"}
    r, n = _servir_contando(m, {"operacion": "ST-DESC-001", "datos": [dato], "fecha_corte": "2026-11-12"})
    assert r["estado"] == "RECHAZADO" and n == 1, r


@pytest.mark.parametrize("campo,valor", [("horizonte", _generador), ("modo", lambda: {(1, 2): "a"}), ("prioridad", _Raro),
                                         ("horizonte", lambda: 5), ("modo", lambda: ["SYNC_CALC"]),
                                         ("parametros", lambda: {"x": _generador()}), ("parametros", lambda: {"x": _Raro()})])
def test_h02_un_valor_que_no_es_json_o_no_es_texto_es_un_rechazo_en_rc(tmp_path, campo, valor):
    m = _motor(tmp_path)
    r, n = _servir_contando(m, _peticion("REI-CAP-001", **{campo: valor()}))
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "DATOS_INCOHERENTES" and n == 1, r


def _anidada(n):
    x: list = []
    for _ in range(n):
        x = [x]
    return x


# ("solicitante", 3 000 niveles) es el caso de H-07 de la QA r01 de T-119 (`r01_04_hostiles.py`: RecursionError)
@pytest.mark.parametrize("argumento,valor", [("solicitante", _circular), ("solicitante", lambda: "\ud800"),
                                             ("solicitante", lambda: _anidada(3000)), ("solicitante", lambda: ["AG-18"]),
                                             ("run_id", _circular), ("run_id", lambda: 7), ("msg_id", lambda: "\udfff"),
                                             ("msg_id", lambda: {"a": _Raro()})])
def test_h02_argumentos_de_la_llamada_que_no_son_texto(tmp_path, argumento, valor):
    m = _motor(tmp_path)
    kw = {"solicitante": "AG-18", "run_id": None, "msg_id": None, argumento: valor()}
    antes = len(m.almacen.leer("RC"))
    r = m.servir(_peticion("REI-CAP-001"), kw.pop("solicitante"), **kw)
    rc = m.almacen.leer("RC")
    assert r["estado"] == "RECHAZADO" and len(rc) == antes + 1 and argumento in r["detalle"], r
    assert rc[-1][argumento] is None   # la entrada lo lleva vacío, no el valor ilegible
    esperado = "CANAL_NO_AUTORIZADO" if argumento == "solicitante" else "DATOS_INCOHERENTES"
    assert r["motivo"] == esperado


def test_h02_la_peticion_bien_formada_se_sirve_igual(tmp_path):
    m = _motor(tmp_path)
    r = m.servir(_peticion("REI-CAP-001", horizonte="H3", modo="SYNC_CALC", prioridad="MATERIAL"), "AG-18", run_id="RUN-1",
                 msg_id="MSG-1")
    assert r["estado"].startswith("SERVED"), r
    e = m.almacen.estado("RC")[r["calc_id"]]
    assert (e["run_id"], e["msg_id"], e["solicitante"]) == ("RUN-1", "MSG-1", "AG-18")


# ====================================================================================================== H-03
class _ProveedorSeries:
    """Proveedor de HT-01 en memoria: una serie que después «desaparece» (el proveedor recorta su historia)."""

    as_of = None
    nombre = "pruebas-series"

    def __init__(self):
        idx = pd.bdate_range("2018-01-01", periods=800)
        rng = np.random.default_rng(121)
        self.series = {"SINT": pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(idx)))), index=idx)}

    def cierres(self, serie, inicio=None, fin=None):
        from bloque_a.herramientas.ht01_datos import DatosNoDisponibles
        if serie not in self.series:
            raise DatosNoDisponibles(f"sin datos de {serie}")
        s = self.series[serie]
        return s[(s.index >= pd.Timestamp(inicio or s.index[0])) & (s.index <= pd.Timestamp(fin or s.index[-1]))]

    def huella(self, serie, inicio=None, fin=None):
        return "h-" + serie


def _var_con_serie(tmp_path):
    prov = _ProveedorSeries()
    m = _motor(tmp_path, proveedor=prov)
    r = m.servir({"operacion": "RISK-VAR-001", "datos": [{"serie": "SINT"}], "parametros": {}, "fecha_corte": "2021-01-29"},
                 "AG-18")
    assert r["estado"].startswith("SERVED"), r
    return m, prov, r["calc_id"]


def _reejecucion_registrada(m, calc_id, antes):
    out = m.reejecutar(calc_id, "auditoría")   # si escapa una excepción, la prueba falla aquí
    rc = m.almacen.leer("RC")
    assert len(rc) == antes + 1 and rc[-1]["tipo_entrada"] == "REEJECUCION" and rc[-1]["calc_id"] == out["calc_id"]
    assert rc[-1]["reejecucion"]["calc_original"] == calc_id and rc[-1]["reejecucion"]["categoria"] == "ERROR_REEJECUCION"
    assert (out["coincide"], out["categoria"], out["diferencias"]) == ("NO", "ERROR_REEJECUCION", []), out
    return out


def test_h03_una_serie_de_ht01_que_ya_no_esta_deja_la_reejecucion_registrada(tmp_path):
    m, prov, c = _var_con_serie(tmp_path)
    assert m.reejecutar(c, "auditoría")["coincide"] == "SI"
    del prov.series["SINT"]
    out = _reejecucion_registrada(m, c, len(m.almacen.leer("RC")))
    assert "DatosNoDisponibles" in out["diagnostico"] and "ya no se pueden resolver" in out["diagnostico"]


def test_h03_una_fecha_del_dato_posterior_al_as_of_deja_la_reejecucion_registrada(tmp_path):
    m, _, c = _var_con_serie(tmp_path)
    alterado = _copia(m, c, lambda e: e["datos"][0].__setitem__("fecha_dato", "2030-01-01"))
    out = _reejecucion_registrada(m, alterado, len(m.almacen.leer("RC")))
    assert "FugaDeInformacion" in out["diagnostico"]


@pytest.mark.parametrize("cambio", [lambda e: e.__setitem__("datos", None), lambda e: e.__setitem__("operacion", None),
                                    lambda e: e["operacion"].__setitem__("ficha_id", ["RISK-VAR-001"]),
                                    lambda e: e.__setitem__("resultado", None), lambda e: e.pop("resultado"),
                                    lambda e: e.__setitem__("parametros", None), lambda e: e.__setitem__("as_of", "ilegible")],
                         ids=["datos_nulos", "operacion_nula", "ficha_lista", "resultado_nulo", "sin_resultado",
                              "parametros_nulos", "as_of_ilegible"])
def test_h03_un_artefacto_alterado_deja_la_reejecucion_registrada(tmp_path, cambio):
    m, _, c = _var_con_serie(tmp_path)
    alterado = _copia(m, c, cambio)
    out = _reejecucion_registrada(m, alterado, len(m.almacen.leer("RC")))
    assert out["diagnostico"].startswith("ERROR_REEJECUCION")


def test_h03_lo_imposible_sigue_siendo_imposible(tmp_path):
    m, _, c = _var_con_serie(tmp_path)
    with pytest.raises(ValueError):
        m.reejecutar(c, " ")
    with pytest.raises(KeyError):
        m.reejecutar("CALC-0000-9999", "auditoría")


# ====================================================================================================== H-05
def test_h05_la_cota_de_reg_hmm_sale_de_h5_en_semanas():
    """120 meses de `horizontes.H5` son 520 semanas (52 por año); con H5 en 60 meses, 260; en semanas, tal cual."""
    assert parametro(None, "horizontes.H5") == {"meses": 120}
    assert S.OBS_MAXIMAS_HMM == S.UMBRALES["REG-HMM-001"]["obs_maximas"] == S._obs_maximas("REG-HMM-001", None) == 520
    cfg = fusionar(cargar_config(), {"horizontes": {"H5": {"meses": 60}}})
    assert S._obs_maximas("REG-HMM-001", cfg) == 260
    assert S._semanas_h5({"horizontes": {"H5": {"semanas": 300}}}) == 300
    for malo in ({"meses": 0}, {"meses": 1.5}, {"meses": True}, "120 meses"):
        with pytest.raises(ErrorFicha):
            S._semanas_h5({"horizontes": {"H5": malo}})
