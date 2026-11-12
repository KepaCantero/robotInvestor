"""T-106 · Motor Fase 1: integración de las 21 fichas V5.0 (IDX, FON, DER, MON y TCV) en el Motor, sus casos de control
registrados en RC (§20.2 del Catálogo) y la regla «manda el Catálogo»: una ficha se sirve solo si tiene código y el
Catálogo la da por IMPLEMENTADO."""
from pathlib import Path

import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.motor import servicio

FASE1 = sorted(servicio.CASOS_CONTROL)


class _Proveedor:
    as_of = None
    nombre = "pruebas"


def _motor(tmp_path):
    return servicio.Motor(Almacen(Path(tmp_path)), _Proveedor(), cargar_config())


def test_son_las_21_fichas_v50():
    assert len(FASE1) == 21 and all(f in servicio.FICHAS_CATALOGO and f in servicio.IMPLEMENTADAS for f in FASE1)


def test_el_motor_sirve_exactamente_lo_que_el_catalogo_da_por_implementado():
    """Coherencia código ↔ Catálogo: nada servible sin IMPLEMENTADO en el Catálogo, y nada IMPLEMENTADO sin código."""
    mad = servicio.madurez_catalogo()
    assert len(mad) == 81
    implementadas_catalogo = {f for f, v in mad.items() if v.startswith(("IMPLEMENTADO", "VALIDADO"))}
    servibles = {f for f in servicio.IMPLEMENTADAS if servicio.servible(f)} | ({"VOL-GARCH-001"} if not servicio.garch_disponible() else set())
    assert servibles == implementadas_catalogo


def test_sin_catalogo_legible_no_se_sirve_nada(tmp_path):
    assert servicio.madurez_catalogo(str(tmp_path)) == {}


def test_los_casos_de_control_se_superan_y_quedan_en_rc(tmp_path):
    m = _motor(tmp_path)
    res = m.verificar_casos_control(run_id="RUN-PRUEBA")
    assert set(res) == set(FASE1) and all(r["superados"] for r in res.values()), {f: r for f, r in res.items() if not r["superados"]}
    rc = [e for e in m.almacen.leer("RC") if e.get("tipo_entrada") == "CASOS_CONTROL"]
    assert len(rc) == 21 and all(e["superados"] and e["casos_control"] for e in rc)


def test_un_caso_que_falla_no_se_supera_y_se_registra(tmp_path, monkeypatch):
    f = FASE1[0]
    caso = dict(servicio.CASOS_CONTROL[f][0], comprobar=lambda r: False)
    monkeypatch.setitem(servicio.CASOS_CONTROL, f, [caso])
    m = _motor(tmp_path)
    r = m.verificar_casos_control([f])[f]
    assert not r["superados"] and m.almacen.leer("RC")[-1]["estado"] == "REJECTED"


@pytest.mark.parametrize("ficha", FASE1)
def test_cada_ficha_se_sirve_por_ct09_con_su_primer_caso(tmp_path, ficha):
    caso = servicio.CASOS_CONTROL[ficha][0]
    m = _motor(tmp_path)
    r = m.servir({"operacion": ficha, "datos": caso.get("datos") or [], "parametros": dict(caso.get("parametros") or {}),
                  "fecha_corte": "2026-11-12"}, "AG-21")
    if servicio.citable_segun_catalogo(ficha):
        assert r["estado"] in ("SERVED", "SERVED_WITH_LIMITATIONS"), r
        assert caso["comprobar"](r["resultado"]) or "advertencias" in r["resultado"]
    else:
        assert r["estado"] == "RECHAZADO" and r["motivo"] == "METODO_NO_IMPLEMENTADO"


def test_las_advertencias_fijas_de_la_ficha_no_son_limitaciones():
    """Los «Supuestos y limitaciones» de TCV van en `resultado["advertencias"]`, como en las demás familias."""
    from bloque_a.motor import fichas_tcv
    f = "TCV-VIXTS-001"
    caso = servicio.CASOS_CONTROL[f][0]
    ent = {"valores": {}, "series": {}, "series_rol": {}}
    for d in caso.get("datos") or []:
        ent["valores"].update(d.get("valores") or {})
    r, lim = servicio.IMPLEMENTADAS[f]["fn"](ent, dict(caso.get("parametros") or {}))
    assert set(fichas_tcv.ADVERTENCIAS[f]) <= set(r["advertencias"]) and not set(fichas_tcv.ADVERTENCIAS[f]) & set(lim)
