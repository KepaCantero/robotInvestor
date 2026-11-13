"""T-112 · Motor Fase 2: integración de las fichas P0 y P1 y la re-ejecución independiente CT-10 (AUD-REX-001)."""
import copy
from pathlib import Path

import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.motor import servicio


class _Proveedor:
    as_of = None
    nombre = "pruebas"


def _motor(tmp_path):
    return servicio.Motor(Almacen(Path(tmp_path)), _Proveedor(), cargar_config())


def _servido(m):
    caso = servicio.CASOS_CONTROL[servicio.CASO_AUD_REX][0]
    r = m.servir({"operacion": servicio.CASO_AUD_REX, "datos": copy.deepcopy(caso["datos"]), "parametros": dict(caso.get("parametros") or {}),
                  "fecha_corte": "2026-11-12"}, "AG-21")
    assert r["estado"].startswith("SERVED"), r
    return r["calc_id"]


def _copia(m, calc_id, cambio):
    e = copy.deepcopy(m.almacen.estado("RC")[calc_id])
    cambio(e)
    e["calc_id"] = m.almacen.nuevo_id("CALC")
    m.almacen.escribir("RC", "AG-13", e)
    return e["calc_id"]


# ================================================================================================== AUD-REX-001 (CT-10)
def test_aud_rex_el_artefacto_guarda_los_valores_en_linea_y_su_huella(tmp_path):
    m = _motor(tmp_path)
    c = _servido(m)
    e = m.almacen.estado("RC")[c]
    d = next(x for x in e["datos"] if "valor" in x)
    assert isinstance(d["valor"], dict) and d["huella"] == servicio.clave_hash(d["valor"])[:16]


def test_aud_rex_un_calculo_servido_se_reejecuta_igual_con_doble_pasada(tmp_path):
    m = _motor(tmp_path)
    out = m.reejecutar(_servido(m), "auditoría")
    rc = m.almacen.leer("RC")[-1]["reejecucion"]
    assert (out["coincide"], out["categoria"]) == ("SI", None) and rc["doble_pasada"] and rc["aislamiento"] == "CONFIRMADO"


@pytest.mark.parametrize("motivo", ["", "  ", None])
def test_aud_rex_sin_motivo_es_imposible(tmp_path, motivo):
    m = _motor(tmp_path)
    with pytest.raises(ValueError, match="sin motivo"):
        m.reejecutar(_servido(m), motivo)


def test_aud_rex_un_artefacto_sin_los_valores_es_imposible(tmp_path):
    """Los artefactos anteriores a T-112 solo guardaban «en línea»: no se reconstruyen por inferencia."""
    m = _motor(tmp_path)

    def viejo(e):
        for d in e["datos"]:
            if "valor" in d:
                d["valor"] = "en línea"
    with pytest.raises(NotImplementedError, match="imposible"):
        m.reejecutar(_copia(m, _servido(m), viejo), "auditoría")


def test_aud_rex_datos_alterados_son_datos_distintos(tmp_path):
    m = _motor(tmp_path)

    def otro(e):
        next(d for d in e["datos"] if isinstance(d.get("valor"), dict))["valor"]["x_alterado"] = 1
    out = m.reejecutar(_copia(m, _servido(m), otro), "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", "DATOS_DISTINTOS")


def _escala(f):
    def cambio(e):
        p = e["resultado"]["payload"]
        k = next(k for k, v in p.items() if isinstance(v, float) and v != 0)
        p[k] = p[k] * (1 + f)
    return cambio


def test_aud_rex_dentro_y_fuera_de_la_tolerancia(tmp_path):
    m = _motor(tmp_path)
    c = _servido(m)
    tol = servicio.IMPLEMENTADAS[servicio.CASO_AUD_REX]["tol"]
    dentro = m.reejecutar(_copia(m, c, _escala(tol / 10)), "auditoría")
    fuera = m.reejecutar(_copia(m, c, _escala(tol * 1e3)), "auditoría")
    assert (dentro["coincide"], dentro["categoria"]) == ("DENTRO_TOLERANCIA", None)
    assert (fuera["coincide"], fuera["categoria"]) == ("NO", "ERROR_ORIGINAL") and fuera["diferencias"]


def test_aud_rex_otra_version_de_la_ficha_es_convencion_distinta(tmp_path):
    m = _motor(tmp_path)

    def otra(e):
        e["operacion"]["ficha_version"] = "0.9"
        _escala(1.0)(e)
    out = m.reejecutar(_copia(m, _servido(m), otra), "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", "CONVENCION_DISTINTA")


def test_aud_rex_un_manejador_no_determinista_se_detecta(tmp_path, monkeypatch):
    m = _motor(tmp_path)
    c = _servido(m)
    f = servicio.CASO_AUD_REX
    cuenta = iter(range(10 ** 6))
    orig = servicio.IMPLEMENTADAS[f]["fn"]
    monkeypatch.setitem(servicio.IMPLEMENTADAS, f, {**servicio.IMPLEMENTADAS[f],
                                                    "fn": lambda ent, p: ({**orig(ent, p)[0], "ruido": float(next(cuenta))}, [])})
    out = m.reejecutar(c, "auditoría")
    assert (out["coincide"], out["categoria"]) == ("NO", "NO_DETERMINISMO")


def test_aud_rex_sus_casos_de_control_se_superan_y_quedan_en_rc(tmp_path):
    m = _motor(tmp_path)
    r = m.verificar_casos_control(["AUD-REX-001"])["AUD-REX-001"]
    assert r["superados"] and len(r["casos"]) == 5
    e = m.almacen.leer("RC")[-1]
    assert e["tipo_entrada"] == "CASOS_CONTROL" and e["operacion"]["ficha_id"] == "AUD-REX-001"
    assert not [x for x in m.almacen.leer("RC") if x.get("tipo_entrada") in ("SERVICIO", "REEJECUCION")]   # Registro aparte


# ================================================================================================== integración de la Fase 2
FASE2 = sorted(servicio.FASE2)


def test_son_las_35_fichas_de_la_fase_2_y_estan_en_el_catalogo():
    assert len(FASE2) == 35 and all(f in servicio.FICHAS_CATALOGO and f in servicio.IMPLEMENTADAS for f in FASE2)
    assert not servicio.FASE1 & servicio.FASE2 and servicio.ESTRICTAS == servicio.FASE1 | servicio.FASE2
    mad = servicio.madurez_catalogo()
    assert all(mad[f].startswith("IMPLEMENTADO") for f in FASE2 + ["AUD-REX-001"])
    assert not servicio.DOCUMENTADAS_CON_CODIGO


@pytest.mark.parametrize("ficha", FASE2)
def test_cada_ficha_de_la_fase_2_se_sirve_por_ct09_con_su_primer_caso(tmp_path, ficha):
    caso = servicio.CASOS_CONTROL[ficha][0]
    solicitante = "AG-18" if ficha in servicio.SOLICITANTES_FICHA else "AG-03"
    r = _motor(tmp_path).servir({"operacion": ficha, "datos": copy.deepcopy(caso.get("datos") or []),
                                 "parametros": dict(caso.get("parametros") or {}), "fecha_corte": "2026-11-12"}, solicitante)
    assert r["estado"] in ("SERVED", "SERVED_WITH_LIMITATIONS"), r
    assert caso["comprobar"](r["resultado"])


def test_bib_met_solo_la_piden_el_orquestador_y_el_evaluador(tmp_path):
    caso = servicio.CASOS_CONTROL["BIB-MET-001"][0]
    pet = {"operacion": "BIB-MET-001", "datos": copy.deepcopy(caso.get("datos") or []), "parametros": dict(caso.get("parametros") or {}),
           "fecha_corte": "2026-11-12"}
    m = _motor(tmp_path)
    no = m.servir(copy.deepcopy(pet), "AG-14")   # un agente de conocimiento no es cliente de la ficha
    assert no["estado"] == "RECHAZADO" and no["motivo"] == "CANAL_NO_AUTORIZADO"
    for ag in ("AG-18", "AG-20"):
        assert _motor(tmp_path / ag).servir(copy.deepcopy(pet), ag)["estado"].startswith("SERVED")


def test_la_semilla_de_la_peticion_llega_a_las_fichas_con_azar(tmp_path, monkeypatch):
    assert {"SIM-MC-001", "SCN-H-001"} <= servicio.ACEPTA_SEMILLA and "ST-DESC-001" not in servicio.ACEPTA_SEMILLA
    f = "SIM-MC-001"
    vistos = []
    orig = servicio.IMPLEMENTADAS[f]["fn"]

    def espia(ent, params):
        vistos.append(params.get("semilla"))
        return orig(ent, params)
    monkeypatch.setitem(servicio.IMPLEMENTADAS, f, {**servicio.IMPLEMENTADAS[f], "fn": espia})
    caso = servicio.CASOS_CONTROL[f][0]
    params = {k: v for k, v in (caso.get("parametros") or {}).items() if k != "semilla"}
    r = _motor(tmp_path).servir({"operacion": f, "datos": copy.deepcopy(caso.get("datos") or []), "parametros": params,
                                 "semilla": 4242, "fecha_corte": "2026-11-12"}, "AG-03")
    assert vistos and set(vistos) == {4242}, (vistos, r)


def test_una_cifra_no_finita_de_la_fase_2_es_un_rechazo(tmp_path, monkeypatch):
    f = FASE2[0]
    monkeypatch.setitem(servicio.IMPLEMENTADAS, f, {**servicio.IMPLEMENTADAS[f], "fn": lambda ent, params: ({"x": float("nan")}, [])})
    r = _motor(tmp_path).servir({"operacion": f, "datos": [{"valores": {"x": 1}}], "fecha_corte": "2026-11-12"}, "AG-18")
    assert r["estado"] == "RECHAZADO" and "no finitas" in r["detalle"]


def test_aud_rex_por_ct09_dice_que_se_pide_por_ct10(tmp_path):
    r = _motor(tmp_path).servir({"operacion": "AUD-REX-001", "datos": [], "fecha_corte": "2026-11-12"}, "AG-18")
    assert r["estado"] == "RECHAZADO" and "CT-10" in r["detalle"]
