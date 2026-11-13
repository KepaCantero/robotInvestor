"""T-106 · Motor Fase 1: integración de las 21 fichas V5.0 (IDX, FON, DER, MON y TCV) en el Motor, sus casos de control
registrados en RC (§20.2 del Catálogo) y la regla «manda el Catálogo»: una ficha se sirve solo si tiene código y el
Catálogo la da por IMPLEMENTADO."""
from pathlib import Path

import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.motor import servicio

FASE1 = sorted(servicio.FASE1)   # T-112: las 21 de T-106 (CASOS_CONTROL lleva también las de la Fase 2)


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
    servibles |= servicio.SERVICIOS_CT10   # T-112: AUD-REX-001 se sirve por CT-10 (`Motor.reejecutar`), no por CT-09
    assert servibles == implementadas_catalogo


def test_sin_catalogo_legible_no_se_sirve_nada(tmp_path):
    assert servicio.madurez_catalogo(str(tmp_path)) == {}


def test_los_casos_de_control_se_superan_y_quedan_en_rc(tmp_path):
    m = _motor(tmp_path)
    res = m.verificar_casos_control(run_id="RUN-PRUEBA")
    todas = set(servicio.CASOS_CONTROL) | servicio.SERVICIOS_CT10   # T-112: la Fase 2 y AUD-REX-001 (CT-10) también
    assert set(res) == todas and all(r["superados"] for r in res.values()), {f: r for f, r in res.items() if not r["superados"]}
    rc = [e for e in m.almacen.leer("RC") if e.get("tipo_entrada") == "CASOS_CONTROL"]
    assert len(rc) == len(todas) and all(e["superados"] and e["casos_control"] for e in rc)


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
        assert caso["comprobar"](r["resultado"])   # QA r01, H-13: sin el «or» que la hacía pasar siempre
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


# ================================================================================================== ronda r02 (QA r01 de T-106)
def test_r02_h02_cualquier_excepcion_de_una_ficha_es_un_rechazo(tmp_path, monkeypatch):
    f = FASE1[0]

    def revienta(ent, params):
        raise ZeroDivisionError("división por cero")
    monkeypatch.setitem(servicio.IMPLEMENTADAS, f, {**servicio.IMPLEMENTADAS[f], "fn": revienta})
    m = _motor(tmp_path)
    r = m.servir({"operacion": f, "datos": [{"valores": {"x": 1}}], "fecha_corte": "2026-11-12"}, "AG-21")
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "DATOS_INSUFICIENTES" and "ZeroDivisionError" in r["detalle"]
    assert m.almacen.leer("RC")[-1]["tipo_entrada"] == "RECHAZO"


def test_r02_h02_una_cifra_no_finita_es_un_rechazo(tmp_path, monkeypatch):
    f = FASE1[0]
    monkeypatch.setitem(servicio.IMPLEMENTADAS, f, {**servicio.IMPLEMENTADAS[f], "fn": lambda ent, params: ({"x": float("inf")}, [])})
    r = _motor(tmp_path).servir({"operacion": f, "datos": [{"valores": {"x": 1}}], "fecha_corte": "2026-11-12"}, "AG-21")
    assert r["estado"] == "RECHAZADO" and "no finitas" in r["detalle"]


def test_r02_h04_el_catalogo_se_lee_de_la_raiz_configurada(tmp_path):
    cfg = cargar_config()
    cfg.setdefault("rutas", {})["raiz_paquete"] = str(tmp_path)   # una raíz sin Catálogo: no se sirve nada
    m = servicio.Motor(Almacen(tmp_path / "a"), _Proveedor(), cfg)
    r = m.servir({"operacion": "ST-DESC-001", "datos": [], "fecha_corte": "2026-11-12"}, "AG-03")
    assert r["estado"] == "RECHAZADO" and "sin Catálogo legible" in r["detalle"]
    real = Path(servicio.DIR_EJECUTOR.parent)
    cfg["rutas"]["raiz_paquete"] = str(real)
    assert servicio.servible("ST-DESC-001", servicio.raiz_paquete(cfg))


def test_r02_h05_un_catalogo_con_bytes_no_utf8_no_sirve_nada(tmp_path):
    destino = tmp_path.joinpath(*servicio.RUTA_CATALOGO)
    destino.parent.mkdir(parents=True)
    destino.write_bytes(b"\xff\xfe no es UTF-8")
    assert servicio.madurez_catalogo(tmp_path) == {}


def test_r02_h06_solo_cuenta_la_tabla_del_indice_y_un_cambio_se_relee(tmp_path):
    real = servicio.DIR_EJECUTOR.parent.joinpath(*servicio.RUTA_CATALOGO).read_text(encoding="utf-8")
    destino = tmp_path.joinpath(*servicio.RUTA_CATALOGO)
    destino.parent.mkdir(parents=True)
    # una fila falsa antes del §4 no cuenta
    destino.write_text("| MON-EXP-001 | x | MC-09 | P | H | P1 | VALIDADO |\n" + real, encoding="utf-8")
    assert servicio.madurez_catalogo(tmp_path)["MON-EXP-001"].startswith("IMPLEMENTADO")
    import os
    import time
    destino.write_text(real.replace("| MON-EXP-001 | Expectativas implícitas de tipos a corto | MC-09 | PERF-MON (+ PERF-FIR, PERF-TCV, PERF-FX) | H1 (limitado)–H3 | P1 | IMPLEMENTADO",
                                    "| MON-EXP-001 | Expectativas implícitas de tipos a corto | MC-09 | PERF-MON (+ PERF-FIR, PERF-TCV, PERF-FX) | H1 (limitado)–H3 | P1 | Documentado (x"), encoding="utf-8")
    os.utime(destino, ns=(time.time_ns(), time.time_ns() + 10**9))
    assert servicio.madurez_catalogo(tmp_path)["MON-EXP-001"].startswith("Documentado")
