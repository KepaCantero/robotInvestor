"""Puerta de tiempo real (PT30 previa y en ejecución, PTA), puntos de control persistidos, `autorizar` con las cuatro
opciones, política de autorización automática, N3 expreso, recordatorio a las 24 h y caducidad a los 7 días."""
import datetime as dt
import json
from pathlib import Path

import pytest

from bloque_b.broker import decision, estado
from bloque_b.herramientas import ht08
from bloque_b.orquestacion import Coordinador

from conftest import AS_OF, peticion_redes


def _pausa_en_ejecucion(hacer_entorno, **kw):
    ent = hacer_entorno(**kw)
    c = Coordinador(ent)
    r = c.recibir(peticion_redes())
    assert r["estado"] == "EN_PAUSA" and r["puerta"] == "PT30" and r["momento"] == "EN_EJECUCION", r
    return ent, c, r


def test_pt30_en_ejecucion_persiste_punto_de_control(hacer_entorno):
    ent, c, r = _pausa_en_ejecucion(hacer_entorno)
    assert r["estado_peticion"] == "EN_PAUSA_PUNTO_CONTROL"
    assert set(r["opciones"]) == set(ht08.OPCIONES)
    ruta = ent.alm.dir_puntos_control / f"{r['checkpoint_id']}.json"
    assert ruta.exists()
    st = ht08.cargar_punto_control(ruta)
    assert st["pet_id"] == r["pet_id"] and st["siguiente"] in ("F2L", "F3P", "F2R", "F3", "F5", "F4", "F6", "F7", "F8", "F9")
    aut = ent.alm.estado("F1", tipo="AUTORIZACION")[r["aut_id"]]
    assert aut["estado"] == "PENDIENTE" and aut["justificacion"]["que_aporta"]      # R20: siempre justificada
    assert aut["hecho_hasta_ahora"]["minutos_consumidos"] > 0
    est = estado(ent, c, r["pet_id"])
    assert est["autorizaciones_pendientes"][0]["aut_id"] == r["aut_id"]
    assert est["peticion"]["ultima_proyeccion"]["total_p80"] > 30


def test_autorizar_continuar_reanuda_con_ejecucion_nueva(hacer_entorno, tmp_path):
    ent, c, r = _pausa_en_ejecucion(hacer_entorno)
    # proceso nuevo (otro Entorno sobre el mismo estado): la reanudación sale del disco
    ent2 = hacer_entorno(nombre="e1")
    res = Coordinador(ent2).autorizar(r["aut_id"], "CONTINUAR", decidido_por="BROKER", motivo="prueba")
    assert res["estado_peticion"] == "ENTREGADA"
    assert res["run_ids"] == [f"RUN-B-{r['pet_id'][6:]}-01", f"RUN-B-{r['pet_id'][6:]}-02"]
    assert r["aut_id"] in res["tiempo"]["autorizaciones"]
    assert Coordinador(ent2).autorizar(r["aut_id"], "CONTINUAR")["nota"] == "La autorización no está pendiente"


def test_punto_de_control_alterado_no_se_reanuda(hacer_entorno):
    ent, c, r = _pausa_en_ejecucion(hacer_entorno)
    ruta = ent.alm.dir_puntos_control / f"{r['checkpoint_id']}.json"
    d = json.loads(ruta.read_text(encoding="utf-8"))
    d["datos"]["consumido_min"] = 0.0
    ruta.write_text(json.dumps(d), encoding="utf-8")
    with pytest.raises(ht08.ErrorEntrada):
        c.autorizar(r["aut_id"], "CONTINUAR")


def test_autorizar_valida_entradas(hacer_entorno):
    ent, c, r = _pausa_en_ejecucion(hacer_entorno)
    with pytest.raises(ValueError):
        c.autorizar(r["aut_id"], "SEGUIR")
    with pytest.raises(ValueError):
        c.autorizar(r["aut_id"], "CONTINUAR", decidido_por="AGENTE")
    with pytest.raises(ValueError):
        c.autorizar(r["aut_id"], "CONTINUAR", minutos=-5)
    with pytest.raises(KeyError):
        c.autorizar("AUT-B-2026-9999", "CONTINUAR")


def test_version_30_min_declara_el_recorte(hacer_entorno):
    ent, c, r = _pausa_en_ejecucion(hacer_entorno)
    res = c.autorizar(r["aut_id"], "VERSION_30_MIN")
    assert res["estado_peticion"] == "ENTREGADA"
    assert res["resumen"]["resultado_del_analisis"] == "PARCIAL"
    p = json.loads(Path(res["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    assert any("30 min" in x for x in json.dumps(p, ensure_ascii=False).split('"') if "Versión" in x)


def test_dividir_en_fases(hacer_entorno):
    ent, c, r = _pausa_en_ejecucion(hacer_entorno)
    f1 = c.autorizar(r["aut_id"], "DIVIDIR_EN_FASES")
    assert f1["fase"] == 1 and f1["estado_peticion"] == "DIVIDIDA"
    assert all("_fase1" in Path(x).name for x in f1["entregables"].values())
    assert f1["resumen"]["veredicto"] in ("VIGILAR", "NO_INVERTIR", "DATOS_INSUFICIENTES")   # sin selección no hay INVERTIR
    aut2 = f1["fase_2"]["aut_id"]
    f2 = c.autorizar(aut2, "CONTINUAR")
    assert f2["fase"] == 2 and f2["estado_peticion"] == "ENTREGADA"
    assert all("_fase2" in Path(x).name for x in f2["entregables"].values())
    assert f2["estado_g3"] in ("APTO", "APTO_CON_ADVERTENCIAS")


def test_cancelar_deja_resumen_n0(hacer_entorno):
    ent, c, r = _pausa_en_ejecucion(hacer_entorno)
    res = c.autorizar(r["aut_id"], "CANCELAR", decidido_por="USUARIO_VIA_BROKER")
    assert res["estado"] == "CANCELADA"
    assert (ent.salida / f"{AS_OF}_resumen-n0_{r['pet_id']}.json").exists()
    assert ent.alm.estado("F1", tipo="PETICION")[r["pet_id"]]["estado"] == "CANCELADA"


def test_pt30_previa(hacer_entorno):
    ent = hacer_entorno()
    c = Coordinador(ent)
    p = peticion_redes(nivel="AUTO")
    p["paquete_para_bloque_B"]["relevancia_decisional"] = "ALTA"   # N3 automático (no expreso)
    r = c.recibir(p)
    assert r["momento"] == "PREVIO_F0" and r["estado_peticion"] == "EN_PAUSA_AUTORIZACION"
    assert r["nivel"] == "N3"
    res = c.autorizar(r["aut_id"], "CONTINUAR")
    assert res["estado_peticion"] == "ENTREGADA"


def test_n3_expreso_no_pide_autorizacion(hacer_entorno):
    ent = hacer_entorno()
    r = Coordinador(ent).recibir(peticion_redes(nivel="N3"))
    assert r["estado_peticion"] == "ENTREGADA"
    auts = ent.alm.estado("F1", tipo="AUTORIZACION")
    assert any(a.get("tipo") == "N3_EXPRESO" and a["decision"]["minutos_autorizados"] > 30 for a in auts.values())


def test_limite_del_broker_reduce_lo_autorizado(hacer_entorno):
    ent = hacer_entorno()
    r = Coordinador(ent).recibir(peticion_redes(nivel="N3", limite={"minutos": 20, "uc": None}))
    assert r["estado"] == "EN_PAUSA" and r["momento"] == "PREVIO_F0"


def test_politica_automatica_autoriza_y_notifica(hacer_entorno):
    ent = hacer_entorno()
    out = decision(ent, {"configuracion": {"politica_autorizacion": [
        {"regla_id": "POL-1", "condicion": {"relevancia": "MEDIA", "origen": "BLOQUE_A"}, "accion": "AUTORIZAR_HASTA", "minutos": 120}]}})
    assert out["estado"] == "COMPLETO"
    r = Coordinador(ent).recibir(peticion_redes())
    assert r["estado_peticion"] == "ENTREGADA"
    auto = [a for a in ent.alm.estado("F1", tipo="AUTORIZACION").values() if a.get("tipo") == "AUTORIZACION_AUTOMATICA_NOTIFICADA"]
    assert auto and auto[0]["decision"]["decidido_por"] == "POLITICA_AUTOMATICA" and auto[0]["decision"]["regla_id"] == "POL-1"


def test_politica_no_autorizar_y_reglas_que_no_aplican(hacer_entorno):
    ent = hacer_entorno()
    decision(ent, {"configuracion": {"politica_autorizacion": [
        {"regla_id": "POL-1", "condicion": {"relevancia": "ALTA"}, "accion": "AUTORIZAR_HASTA", "minutos": 120},
        {"regla_id": "POL-2", "condicion": {}, "accion": "NO_AUTORIZAR"}]}})
    r = Coordinador(ent).recibir(peticion_redes())
    assert r["estado"] == "EN_PAUSA"
    assert ent.alm.estado("F1", tipo="AUTORIZACION")[r["aut_id"]]["politica_aplicada"]["regla_id"] == "POL-2"


def test_politica_elegir_opcion(hacer_entorno):
    ent = hacer_entorno()
    decision(ent, {"configuracion": {"politica_autorizacion": [
        {"regla_id": "POL-9", "condicion": {}, "accion": "ELEGIR_OPCION", "opcion": "VERSION_30_MIN"}]}})
    r = Coordinador(ent).recibir(peticion_redes())
    assert r["estado_peticion"] == "ENTREGADA" and r["resumen"]["resultado_del_analisis"] == "PARCIAL"


def test_configuracion_de_politica_validada(hacer_entorno):
    ent = hacer_entorno()
    with pytest.raises(ValueError):
        decision(ent, {"configuracion": {"tope_autorizacion_automatica_min": 600}})
    with pytest.raises(ValueError):
        decision(ent, {"configuracion": {"politica_autorizacion": [{"regla_id": "X", "accion": "AUTORIZAR_HASTA"}]}})
    with pytest.raises(ValueError):
        decision(ent, {"configuracion": {"pesos_S": {}}})       # parámetro calibrable: no lo cambia el Broker


def test_tope_absoluto_impide_autorizacion_automatica():
    pol = [{"regla_id": "POL-1", "condicion": {}, "accion": "AUTORIZAR_HASTA", "minutos": 900}]
    assert ht08.aplicar_politica(pol, {}, 300, 240)["resultado"] == "NO_CUBRE"
    assert ht08.aplicar_politica(pol, {}, 470, 1000)["resultado"] == "AUTORIZA"       # tope efectivo 480
    assert ht08.aplicar_politica(pol, {}, 490, 1000)["resultado"] == "NO_CUBRE"


def test_recordatorio_y_caducidad(hacer_entorno):
    ent, c, r = _pausa_en_ejecucion(hacer_entorno)
    d0 = dt.date.fromisoformat(AS_OF)
    ent2 = hacer_entorno(nombre="e1", as_of=str(d0 + dt.timedelta(days=2)))
    estado(ent2, Coordinador(ent2))
    a = ent2.alm.estado("F1", tipo="AUTORIZACION")[r["aut_id"]]
    assert a["estado"] == "PENDIENTE" and a.get("recordatorio_enviado")
    ent3 = hacer_entorno(nombre="e1", as_of=str(d0 + dt.timedelta(days=8)))
    res = Coordinador(ent3).autorizar(r["aut_id"], "CONTINUAR")
    assert res["estado"] == "CADUCADA"
    assert ent3.alm.estado("F1", tipo="PETICION")[r["pet_id"]]["estado"] == "CADUCADA"


def test_reloj_avanzar_horas():
    from bloque_b.almacen import Reloj
    r = Reloj()
    r.fijar("2026-11-03")
    t0 = r.ahora()
    r.avanzar_horas(25)
    assert ht08.estado_autorizacion(t0, r.ahora()) == "RECORDATORIO"
    r.avanzar_horas(24 * 7)
    assert ht08.estado_autorizacion(t0, r.ahora()) == "CADUCADA"


def test_reloj_real_y_factor_simulado(hacer_entorno, hacer_cfg):
    # reloj real: la ejecución dura segundos, nunca llega a 30 minutos
    r = Coordinador(hacer_entorno(hacer_cfg(reloj={"tipo": "real"}))).recibir(peticion_redes())
    assert r["estado_peticion"] == "ENTREGADA"
    assert r["tiempo"]["real_min"] < 5
    # reloj simulado lento: dispara la PT30 y, tras CONTINUAR con 40 min, la PTA (40 + margen de 5 min)
    ent = hacer_entorno(hacer_cfg(reloj={"factor_simulado": 3.0}))
    c = Coordinador(ent)
    r = c.recibir(peticion_redes())
    assert r["estado"] == "EN_PAUSA"
    r2 = c.autorizar(r["aut_id"], "CONTINUAR", minutos=40)
    assert r2.get("estado") == "EN_PAUSA" and r2["puerta"] == "PTA"
