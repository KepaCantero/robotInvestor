"""Vigía (seguimiento), Evaluador (resolución de PRG-B y métricas), consultas N0, decisiones del Broker, estado del
servicio, referencias F7/F8/F9 y barrido de enlaces sin red."""
import json

from bloque_b.broker import consulta, decision, estado, verificar_enlaces
from bloque_b.evaluador import evaluar
from bloque_b.orquestacion import Coordinador
from bloque_b.vigia import clasificar, ronda

from conftest import peticion_ambito, peticion_redes


def _forzar_umbrales(ent, rec_id, revision, invalidacion):
    rec = ent.alm.estado("F3")[rec_id]
    plan = json.loads(json.dumps(rec["plan_de_seguimiento"]))
    for s in plan["senales"]:
        s.update({"direccion": "por_encima", "umbral_revision": revision, "umbral_invalidacion": invalidacion,
                  "umbral_fluctuacion": {"min": -1e9, "max": 1e9}})
    ent.alm.escribir("F3", "AG-B02", {"tipo_entrada": "PLAN_SEGUIMIENTO", "id": rec_id, "plan_de_seguimiento": plan})


def test_clasificar():
    s = {"direccion": "por_debajo", "umbral_revision": -5, "umbral_invalidacion": -15, "umbral_fluctuacion": {"min": -3, "max": 3}}
    assert clasificar(0, s, None) is None
    assert clasificar(-4, s, None) == "FLUCTUACION"
    assert clasificar(-6, s, None) == "REVISION"
    assert clasificar(-20, s, None) == "INVALIDACION_PROBABLE"
    assert clasificar(-20, s, "INVALIDACION_PROBABLE") == "INVALIDACION_CONFIRMADA"


def test_vigia_sin_alertas_y_con_umbrales_forzados(hacer_entorno, rapido):
    ent = hacer_entorno(rapido, nombre="vig")
    c = Coordinador(ent)
    r = c.recibir(peticion_redes())
    rec_id = r["rec_id"]
    base = ronda(ent, c)
    assert base["lecturas"] > 0
    assert ent.alm.estado("F3")[rec_id]["estado_vigilancia"] == "VIGENTE"
    # revisión
    _forzar_umbrales(ent, rec_id, -1e6, 1e6)
    rv = ronda(ent, c)
    assert rv["alertas"] and {a["clasificacion"] for a in rv["alertas"]} == {"REVISION"}
    assert all(a["alr_id"].startswith("ALR-B-") and a["accion_sugerida"] == "CONSULTA_N0" for a in rv["alertas"])
    assert ent.alm.estado("F3")[rec_id]["estado_vigilancia"] == "EN_REVISION"
    assert not ronda(ent, c)["alertas"]                         # misma clasificación: no se repite
    # invalidación probable y luego confirmada
    _forzar_umbrales(ent, rec_id, -1e6, -1e6)
    a1 = ronda(ent, c)["alertas"]
    assert a1 and all(a["clasificacion"] == "INVALIDACION_PROBABLE" and a["peticion_sugerida"] for a in a1)
    a2 = ronda(ent, c)["alertas"]
    assert a2 and all(a["clasificacion"] == "INVALIDACION_CONFIRMADA" for a in a2)
    assert ent.alm.estado("F3")[rec_id]["estado_vigilancia"] == "INVALIDADA"
    assert list((ent.salida / "Alertas").glob("*_alerta_ALR-B-*.json"))
    # el Vigía nunca abre análisis ni cambia el veredicto (R32)
    assert len(ent.alm.estado("F1", tipo="PETICION")) == 1
    assert ent.alm.estado("F3")[rec_id]["veredicto"] == r["resumen"]["veredicto"]


def test_evaluar_resuelve_pronosticos_vencidos(hacer_entorno, rapido):
    ent = hacer_entorno(rapido, nombre="ev", as_of="2026-06-30")
    c = Coordinador(ent)
    r = c.recibir(peticion_ambito("volatilidad_rv_europea"))      # H2: 21 sesiones
    assert r["estado_peticion"] == "ENTREGADA"
    antes = evaluar(ent, c)
    assert antes["resueltos"] == 0
    ent2 = hacer_entorno(rapido, nombre="ev", as_of="2026-09-30")
    res = evaluar(ent2, Coordinador(ent2))
    assert res["resueltos"] >= 1
    f4 = ent2.alm.estado("F4")
    resueltos = [p for p in f4.values() if p["estado"] == "RESUELTO"]
    assert resueltos and all("acierto" in p["resolucion"] for p in resueltos)
    assert all(p["resolucion"]["comprobacion_fuga"] for p in resueltos)
    assert res["metricas"]
    assert any(e.get("tipo_entrada") == "MODELO_TIEMPOS" for e in ent2.alm.leer("F5"))


def test_consulta_n0_y_pregunta_repetida(entrega_redes):
    ent, c = entrega_redes["ent"], entrega_redes["coord"]
    for _ in range(3):
        r = consulta(ent, c, "¿Por qué el veredicto es escalonado?", entrega_redes["res"]["rec_id"])
    assert r["query_id"].startswith("QRY-B-") and r["ruta"] in ("N0", "PROPUESTA_DE_PETICION")
    assert r.get("pregunta_repetida") is True


def test_decisiones_del_broker(hacer_entorno, rapido):
    ent = hacer_entorno(rapido)
    res = Coordinador(ent).recibir(peticion_redes())
    cand = [k for k, v in ent.alm.estado("F3").items() if k.startswith("CAND-B-") and v.get("en_top_n")][0]
    out = decision(ent, {"decision_ambito": {"rec_id": res["rec_id"], "decision": "CANDIDATOS_ENVIADOS_A_C"},
                         "decisiones_candidatos": [{"cand_id": cand, "decision": "ENVIADO_A_C"}],
                         "valoracion_entregables": {"pet_id": res["pet_id"], "utilidad": 4},
                         "credenciales": [{"cred_id": "CRED-B-2026-0001", "estado": "PROVISTA", "credencial_ref": "alias-flujos-etf-diarios"}],
                         "configuracion": {"top_n": {"N2": [6, 2]}}})
    assert out["estado"] == "COMPLETO" and len(out["registrado"]) == 5
    assert ent.alm.estado("F3")[res["rec_id"]]["decision_broker"] == "CANDIDATOS_ENVIADOS_A_C"
    assert ent.f10()["top_n"] == {"N2": [6, 2]}
    import pytest
    with pytest.raises(ValueError):
        decision(ent, {"credenciales": [{"cred_id": "CRED-B-2026-0002", "estado": "PROVISTA", "valor": "x"}]})


def test_estado_del_servicio(entrega_redes):
    ent, c = entrega_redes["ent"], entrega_redes["coord"]
    e = estado(ent, c, entrega_redes["res"]["pet_id"], True)
    assert len(e["agentes"]) == 24
    assert sum(e["agentes_resumen"].values()) == 24
    assert all(e["integridad"].values())
    assert e["peticion"]["estado"] == "ENTREGADA"
    assert e["f10"]["methodology_version"] == "2.1"
    assert set(e["conectores"]) >= {"precios_csv", "flujos_etf_diarios"}
    assert "sk-" not in json.dumps(e)


def test_referencias_reales_cargadas(entrega_redes):
    rc = entrega_redes["ent"].refs.recuento()
    assert set(rc) >= {"F7", "F8", "F9"}
    assert all(v > 0 for k, v in rc.items() if k in ("F7", "F8", "F9")), rc


def test_verificar_enlaces_sin_red(entrega_redes):
    ent, c = entrega_redes["ent"], entrega_redes["coord"]
    r = verificar_enlaces(ent, c, aplicar=True, offline=True, max_fichas=5)
    assert r["aplicado"] is False and r["modo"].startswith("sin red")
    for k in ("F7", "F8", "F9"):
        assert r["informe"][k]["fichas"] > 0
    assert any(e.get("tipo_entrada") == "MANTENIMIENTO" for e in ent.alm.leer("HA"))
