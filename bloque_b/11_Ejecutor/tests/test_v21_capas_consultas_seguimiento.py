"""Bloque B V2.1 en el ejecutor: capas 0–4 con puertas PV1–PV3 (parada, informe de parada, continuación forzada,
HASTA_PV2), consultas al Broker (CT-B-28), seguimiento encargado (CT-B-29, F11, N1-SEG), AG-B24, entregable 6 y H5."""
import json
from pathlib import Path

import pytest

from bloque_b import mock_respuestas as mr
from bloque_b import seguimiento as sg
from bloque_b.broker import decision
from bloque_b.cli import main as cli_main
from bloque_b.herramientas import ht09
from bloque_b.orquestacion import Coordinador

from conftest import peticion_redes


def _paquete(res):
    return json.loads(Path(res["entregables"]["paquete_json"]).read_text(encoding="utf-8"))


# ------------------------------------------------------------------------------------------------ entrega completa
def test_entrega_v21_mapa_capas_lista_y_consultas(entrega_redes):
    res, ent = entrega_redes["res"], entrega_redes["ent"]
    p = _paquete(res)
    assert p["capas"]["puertas_viabilidad"] == {"PV1": "SUPERADA", "PV2": "SUPERADA", "PV3": "SUPERADA"}
    assert set(p["capas"]["minutos_por_capa"]) == {"0", "1", "2", "3", "4"}
    ids = {e["eslabon_id"] for e in p["mapa_cadena_valor"]["eslabones"]}
    assert all(c["eslabon_id"] in ids for t in p["candidatos_por_tipo"].values() if t.get("aplicable") for c in t["top_n"])
    assert any(e["opciones"] for e in p["mapa_cadena_valor"]["eslabones"])
    assert any(e["emergentes"] for e in p["mapa_cadena_valor"]["eslabones"])      # radar de AG-B24
    assert "AG-B24" in p["estrategia"]["especialistas_activados"]
    assert len(p["lista_profesional"]) == 22
    # la consulta NO_BLOQUEANTE del Seleccionador (RF) se cierra con su supuesto y se declara en todos los entregables
    q = p["consultas_broker"][0]
    assert q["modo"] == "NO_BLOQUEANTE" and q["resolucion"] == "SUPUESTO_APLICADO"
    assert p["supuestos_aplicados"][0]["cns_id"] == q["cns_id"]
    for k in ("informe_tecnico", "memorando"):
        assert q["cns_id"] in Path(res["entregables"][k]).read_text(encoding="utf-8")
    # entregable 6: Markdown, copia .docx y JSON; tablas por eslabón en el informe visual
    md = Path(res["entregables"]["mapa_eslabones"]).read_text(encoding="utf-8")
    assert "Árbol de la cadena" in md and all(i in md for i in ids)
    assert Path(res["entregables"]["mapa_eslabones_docx"]).stat().st_size > 1000
    assert json.loads(Path(res["entregables"]["mapa_eslabones_json"]).read_text(encoding="utf-8"))["eslabones"]
    html = Path(res["entregables"]["informe_visual"]).read_text(encoding="utf-8")
    assert 'id="t-eslabones"' in html and ht09.AVISO_TABLAS_ESLABON in html and "Décadas" in html
    # registros: CAND-B con eslabón en F3; F1 con puertas y consultas; F6 con el mapa
    cands = [c for k, c in ent.alm.estado("F3").items() if str(k).startswith("CAND-B-") and c.get("en_top_n")]
    assert cands and all(c.get("eslabon_id") for c in cands)
    assert {e["puerta"] for e in ent.alm.leer("F1") if e.get("tipo_entrada") == "PUERTA_VIABILIDAD"} == {"PV1", "PV2", "PV3"}
    assert any(e.get("mapa_cadena_valor") for e in ent.alm.leer("F6"))
    # PCB, AE y PEM reconstruibles con HT-03 (G3B-MET-19, G3B-SEL-18)
    r = ht09.validar(p)
    for c in ("G3B-MET-18", "G3B-MET-19", "G3B-MET-21", "G3B-SEL-16", "G3B-SEL-17", "G3B-SEL-18", "G3B-TMP-05", "G3B-CON-21"):
        assert next(x for x in r["comprobaciones"] if x["id"] == c)["resultado"] == "PASA", c


# ------------------------------------------------------------------------------------------------ PV1, parada y forzar
def test_pv1_parada_informe_y_continuacion_forzada(hacer_entorno, rapido, monkeypatch):
    monkeypatch.setitem(mr._TAREAS, ("AG-B02", "viabilidad"),
                        lambda m, c, r: {"tesis_basica": "x", "ya_descontado": True, "sin_mecanismo": True, "alerta_integridad": False})
    ent = hacer_entorno(rapido)
    c = Coordinador(ent)
    res = c.recibir(peticion_redes())
    assert res["estado_peticion"] == "DETENIDA_EN_PUERTA"
    assert res["entregables"]["informe_parada"] and res["entregables"]["informe_tecnico"] is None
    inf = json.loads(Path(res["entregables"]["informe_parada"]["json"]).read_text(encoding="utf-8"))
    assert inf["puerta"] == "PV1" and inf["capa"] == 1 and {m["criterio"] for m in inf["motivos"]} == {"YA_DESCONTADO", "SIN_MECANISMO"}
    assert inf["veredicto_registrado"] == "VIGILAR" and 3 <= len(inf["por_que_no_merece_seguir"]) <= 6
    md = Path(res["entregables"]["informe_parada"]["markdown"]).read_text(encoding="utf-8")
    assert ht09.validar_informe_parada(inf, md)["dictamen"] == "APTO"
    rec = ent.alm.estado("F3")[inf["rec_id"]]
    assert rec["resultado_del_analisis"] == "DETENIDO_EN_PUERTA"
    assert not [p for p in ent.alm.leer("F4")]                       # sin pronósticos congelados (7.11)
    # el Broker fuerza la continuación (CT-B-04)
    out = decision(ent, {"forzar_continuacion": {"pet_id": res["pet_id"], "puerta": "PV1", "motivo": "tesis diferencial conocida"}}, c)
    f = out["forzar_continuacion"]
    assert f["estado_peticion"] == "ENTREGADA", f
    p = _paquete(f)
    assert p["capas"]["continuacion_forzada"]["puerta"] == "PV1"
    assert any("Continuación forzada por el Broker tras PV1 no superada" in x for x in p["limitaciones"])
    assert "continuación forzada" in Path(f["entregables"]["informe_tecnico"]).read_text(encoding="utf-8").lower()
    assert any(e.get("tipo_entrada") == "CONTINUACION_FORZADA" for e in ent.alm.leer("F1"))
    # forzar dos veces o una puerta que no detiene: rechazado
    assert c.forzar_continuacion(res["pet_id"], "PV1")["estado"] == "RECHAZADO"
    assert c.forzar_continuacion(res["pet_id"], "PV3")["estado"] == "RECHAZADO"


def test_pv1_sin_invertibilidad_descarta(hacer_entorno, rapido):
    ent = hacer_entorno(rapido)
    res = Coordinador(ent).recibir(peticion_redes(tipos_activo_admitidos=["CRI"]))
    assert res["estado_peticion"] == "DETENIDA_EN_PUERTA"
    inf = json.loads(Path(res["entregables"]["informe_parada"]["json"]).read_text(encoding="utf-8"))
    assert inf["motivos"][0]["criterio"] == "SIN_INVERTIBILIDAD" and inf["sugerencia"] == "DESCARTAR"


def test_pv2_tesis_refutada_parada(hacer_entorno, rapido, monkeypatch):
    base = mr._integracion_provisional
    monkeypatch.setitem(mr._TAREAS, ("AG-B02", "integracion_provisional"), lambda m, c, r: dict(base(m, c, r), tesis_viva=False))
    ent = hacer_entorno(rapido)
    res = Coordinador(ent).recibir(peticion_redes())
    assert res["estado_peticion"] == "DETENIDA_EN_PUERTA"
    inf = json.loads(Path(res["entregables"]["informe_parada"]["json"]).read_text(encoding="utf-8"))
    assert inf["puerta"] == "PV2" and inf["capa"] == 2 and inf["motivos"][0]["criterio"] == "TESIS_REFUTADA"
    assert set(inf["tiempo_consumo"]["por_capa_min"]) == {"0", "1", "2"}


def test_pv2_solo_e_baja_consulta_bloqueante_y_forzar(hacer_entorno, rapido, monkeypatch):
    base = mr._integracion_provisional
    monkeypatch.setitem(mr._TAREAS, ("AG-B02", "integracion_provisional"), lambda m, c, r: dict(
        base(m, c, r), componentes_E={"calidad_raices": 0, "calidad_metodologica": 10, "discrepancias_resueltas": 0, "actualidad": 0}))
    ent = hacer_entorno(rapido)
    c = Coordinador(ent)
    res = c.recibir(peticion_redes())
    assert res["estado_peticion"] == "EN_PAUSA_CONSULTA" and len(res["cns_ids"]) == 1
    q = ent.alm.estado("F1", tipo="CONSULTA_BROKER")[res["cns_ids"][0]]
    assert q["tipo"] == "CONFIRMACION_SUPUESTO" and q["modo"] == "BLOQUEANTE"
    f = c.responder_consulta(res["cns_ids"][0], "Sí, continúen", forzar_continuacion=True, motivo="hay datos en camino")
    assert f["estado_peticion"] == "ENTREGADA", f
    p = _paquete(f)
    assert p["capas"]["continuacion_forzada"]["puerta"] == "PV2"
    assert p["veredicto"]["resultado_del_analisis"] == "PARCIAL"


def test_pv2_consulta_sin_respuesta_aplica_supuesto_y_para(hacer_entorno, rapido, monkeypatch):
    base = mr._integracion_provisional
    monkeypatch.setitem(mr._TAREAS, ("AG-B02", "integracion_provisional"), lambda m, c, r: dict(
        base(m, c, r), componentes_E={"calidad_raices": 0, "calidad_metodologica": 10, "discrepancias_resueltas": 0, "actualidad": 0}))
    ent = hacer_entorno(rapido)
    c = Coordinador(ent)
    res = c.recibir(peticion_redes())
    assert c.revisar_consultas() == []                                # dentro de plazo
    ent.alm.reloj.avanzar_horas(5)                                    # BLOQUEANTE: 4 h (Anexo A)
    out = c.revisar_consultas()
    assert out[0]["estado"] == "SUPUESTO_APLICADO" and out[0]["reanudacion"]["estado_peticion"] == "DETENIDA_EN_PUERTA"


def test_pv3_no_superada_entrega_sin_seleccion_completa(hacer_entorno, rapido, monkeypatch):
    def plano(m, c, r):
        d = mr._desglose_cadena(m, c, r)
        for e in d["eslabones"]:
            e["indicadores_cuello"] = []
            e["componentes_AE"] = {k: 30 for k in e["componentes_AE"]}
        return d
    monkeypatch.setitem(mr._TAREAS, ("AG-B03", "desglose_cadena"), plano)
    ent = hacer_entorno(rapido)
    res = Coordinador(ent).recibir(peticion_redes())
    assert res["estado_peticion"] == "ENTREGADA", res
    p = _paquete(res)
    assert p["capas"]["puertas_viabilidad"]["PV3"] == "NO_SUPERADA"
    assert p["veredicto"]["valor"] in ("VIGILAR", "DESCARTAR") and p["veredicto"]["resultado_del_analisis"] == "PARCIAL"
    assert not any(p["paquete_para_bloque_C"].values())
    assert all(o["veredicto"] == "SECUNDARIO" for e in p["mapa_cadena_valor"]["eslabones"] for o in e["opciones"])
    assert "PV3 no superada" in Path(res["entregables"]["mapa_eslabones"]).read_text(encoding="utf-8")


# ------------------------------------------------------------------------------------------------ PT30 y HASTA_PV2
def test_hasta_pv2_pide_nueva_autorizacion_tras_pv2(hacer_entorno):
    ent = hacer_entorno()
    c = Coordinador(ent)
    r = c.recibir(peticion_redes())
    assert r["estado"] == "EN_PAUSA" and "HASTA_PV2" in r["opciones"]
    r2 = c.autorizar(r["aut_id"], "HASTA_PV2")
    assert r2["estado"] == "EN_PAUSA" and r2["aut_id"] != r["aut_id"], r2
    assert {e["puerta"] for e in ent.alm.leer("F1") if e.get("tipo_entrada") == "PUERTA_VIABILIDAD"} == {"PV1", "PV2"}
    r3 = c.autorizar(r2["aut_id"], "CONTINUAR")
    assert r3["estado_peticion"] == "ENTREGADA", r3
    assert len(_paquete(r3)["tiempo_consumo"]["autorizaciones"]) >= 2


# ------------------------------------------------------------------------------------------------ consultas al Broker
def test_consulta_bloqueante_pausa_y_respuesta_reanuda(hacer_entorno, rapido, monkeypatch):
    base = mr._plan
    monkeypatch.setitem(mr._TAREAS, ("AG-B02", "plan"), lambda m, c, r: dict(base(m, c, r), consultas_propuestas=[
        {"pregunta": "¿Incluye el Reino Unido y Suiza?", "tipo": "ACLARACION_ALCANCE", "por_que_importa": "cambia el universo",
         "supuesto_si_no_hay_respuesta": "Sí, se incluyen", "efecto_si_supuesto_falso": "universo distinto", "bloqueante": True},
        {"pregunta": "¿Mi cartera?", "tipo": "OTRA", "supuesto_si_no_hay_respuesta": "x", "bloqueante": True}]))
    ent = hacer_entorno(rapido)
    c = Coordinador(ent)
    r = c.recibir(peticion_redes())
    assert r["estado_peticion"] == "EN_PAUSA_CONSULTA" and len(r["cns_ids"]) == 1      # límite N2: 1 bloqueante
    cns = r["cns_ids"][0]
    assert (ent.salida / "Consultas al Broker").is_dir()
    f = c.responder_consulta(cns, "Sí, se incluyen")
    assert f["estado_peticion"] == "ENTREGADA", f
    q = next(x for x in _paquete(f)["consultas_broker"] if x["cns_id"] == cns)
    assert q["resolucion"] == "RESPONDIDA" and q["efecto"] == "SIN_CAMBIO"
    assert c.responder_consulta(cns, "otra cosa")["estado"] == "RESPUESTA_TARDIA"
    assert any(e.get("tipo") == "CONSULTA_CERRADA" for e in ent.alm.leer("F1") if e.get("tipo_entrada") == "AVISO_EVALUADOR")


def test_aporte_del_broker_y_credenciales_rechazadas(hacer_entorno, rapido):
    ent = hacer_entorno(rapido)
    c = Coordinador(ent)
    a = c.aporte_broker({"pet_id": "PET-B-2026-0001", "naturaleza": "PREFERENCIA", "contenido": "Prefiero vehículos UCITS"})
    assert a["sentido"] == "ENTRANTE" and "vincula" in a["efecto"]
    with pytest.raises(Exception):
        c.aporte_broker({"naturaleza": "DATO", "contenido": "api_key=abcdefgh12345"})


# ------------------------------------------------------------------------------------------------ seguimiento encargado
def test_seguimiento_encargado_ciclo_pausa_cancelacion(entrega_redes):
    ent, c = entrega_redes["ent"], entrega_redes["coord"]
    rec_id = entrega_redes["res"]["rec_id"]
    a = sg.encargo(ent, c, {"accion": "ALTA", "objeto": {"tipo": "AMBITO_ANALIZADO", "rec_id": rec_id},
                            "frecuencia": {"tipo": "DIARIA"}, "motivo": "vigilar la cartera de pedidos",
                            "disparadores_broker": [{"descripcion": "book-to-bill < 1"}], "dimensiones_clave": ["D3", "D9"]})
    assert a["estado"] == "ACTIVO" and a["advertencias"]               # diaria > frecuencia del Vigía en H4
    seg = a["seg_id"]
    r = sg.ciclo(ent, c, seg)
    assert r["estado"] == "ENTREGADO" and r["estado_g3"] == "APTO" and r["recomendacion"] in (
        "MANTENER_VIGILANCIA", "REACTIVAR_ANALISIS_PROFUNDO", "PROPONER_PASAR_A_C", "CANCELAR_SEGUIMIENTO")
    inf = json.loads(Path(r["informe_seguimiento"]["json"]).read_text(encoding="utf-8"))
    assert inf["ciclo_id"].endswith("-01") and "_c01" in r["informe_seguimiento"]["markdown"]
    assert all(x["eslabon_id"] for x in inf["candidatos"])
    assert ent.alm.estado("F11", tipo="CIC")[r["ciclo_id"]]["estado"] == "ENTREGADO"
    assert any(e.get("actualizado_por_ciclo") == r["ciclo_id"] for e in ent.alm.leer("F6"))
    n_pet = len(ent.alm.estado("F1", tipo="PETICION"))
    sg.ciclo(ent, c, seg)
    assert len(ent.alm.estado("F1", tipo="PETICION")) == n_pet        # un ciclo nunca abre una petición (R35)
    d = decision(ent, {"decision_seguimiento": {"seg_id": seg, "ciclo_id": r["ciclo_id"], "decision": "MANTENER", "motivo": "sin novedad"}}, c)
    assert f"decision_seguimiento {seg}" in d["registrado"]
    assert any(e.get("tipo_entrada") == "DEC" and e.get("ciclo_id") == r["ciclo_id"] for e in ent.alm.leer("F11"))
    with pytest.raises(ValueError):
        decision(ent, {"decision_seguimiento": {"seg_id": "SEG-B-2099-0001", "decision": "MANTENER"}}, c)
    assert sg.encargo(ent, c, {"accion": "PAUSA", "seg_id": seg})["estado"] == "PAUSADO"
    assert sg.ciclo(ent, c, seg)["estado"] == "PAUSADO"
    assert sg.encargo(ent, c, {"accion": "REANUDACION", "seg_id": seg})["estado"] == "ACTIVO"
    m = sg.encargo(ent, c, {"accion": "MODIFICACION", "seg_id": seg, "frecuencia": {"tipo": "SEMANAL"}})
    assert "frecuencia" in m["modificado"]
    assert sg.encargo(ent, c, {"accion": "CANCELACION", "seg_id": seg, "motivo": "ya no interesa"})["estado"] == "CANCELADO"
    assert sg.ciclo(ent, c, seg)["estado"] == "CANCELADO"
    assert seg in [x["seg_id"] for x in sg.listar(ent)["seguimientos"]]


def test_seguimiento_ambito_nuevo_linea_base_y_pendientes(hacer_entorno, rapido):
    ent = hacer_entorno(rapido)
    c = Coordinador(ent)
    a = sg.encargo(ent, c, {"accion": "ALTA", "objeto": {"tipo": "AMBITO_NUEVO", "ambito": {"descripcion": "Cobre", "clave_universo": "cobre"}},
                            "frecuencia": {"tipo": "PERSONALIZADA", "cada_dias": 10}})
    assert a["linea_base"]["necesaria"] and a["proximo_ciclo"] == ent.as_of
    out = sg.pendientes(ent, c)
    assert len(out["ciclos"]) == 1 and out["ciclos"][0]["estado"] == "ENTREGADO"
    assert sg.pendientes(ent, c)["ciclos"] == []                      # el siguiente vence en 10 días
    with pytest.raises(ValueError):
        sg.encargo(ent, c, {"accion": "ALTA", "objeto": {"tipo": "AMBITO_NUEVO"}, "frecuencia": {"tipo": "HORARIA"}})


def test_cli_seguimiento_y_consulta_broker(entrega_redes, capsys):
    d = entrega_redes["dir"]
    g = ["--config", str(d / "cfg.yaml"), "--estado", str(d / "estado"), "--salida", str(d / "salida"), "--as-of", "2026-11-03"]
    (d / "cfg.yaml").write_text(f"rutas: {{prompts: '{d / 'prompts'}'}}\nreloj: {{factor_simulado: 0.3}}\n", encoding="utf-8")
    enc = d / "seg.json"
    enc.write_text(json.dumps({"objeto": {"tipo": "AMBITO_ANALIZADO", "rec_id": entrega_redes["res"]["rec_id"]},
                               "frecuencia": {"tipo": "MENSUAL"}}), encoding="utf-8")
    assert cli_main(g + ["seguimiento", "alta", "--json", str(enc)]) == 0
    seg = json.loads(capsys.readouterr().out)["seg_id"]
    assert cli_main(g + ["seguimiento", "ciclo", "--seg", seg]) == 0
    assert json.loads(capsys.readouterr().out)["estado"] == "ENTREGADO"
    assert cli_main(g + ["seguimiento", "listar"]) == 0
    assert any(x["seg_id"] == seg for x in json.loads(capsys.readouterr().out)["seguimientos"])
    assert cli_main(g + ["consulta-broker", "listar"]) == 0
    assert json.loads(capsys.readouterr().out)["consultas"]
    assert cli_main(g + ["vigia"]) == 0
    assert "R32" in json.loads(capsys.readouterr().out)["nota"]


# ------------------------------------------------------------------------------------------------ H5
def test_h5_hitos_y_probabilidades_cualitativas(hacer_entorno, rapido):
    ent = hacer_entorno(rapido)
    res = Coordinador(ent).recibir(peticion_redes(horizontes=["H5"]))
    assert res["estado_peticion"] == "ENTREGADA", res
    p = _paquete(res)
    assert p["estrategia"]["horizonte_dominante"] == "H5"
    hitos = [x for x in p["pronosticos_detalle"] if x["tipo"] == "HITO_H5"]
    assert len(hitos) >= 3 and all(x["probabilidad_publicada"] is None for x in p["pronosticos_detalle"])
    assert p["estrategia"]["profundidad"]["D9"] in ("P2", "P3")
