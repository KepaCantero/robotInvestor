"""T-174 · PB-61: una respuesta del Broker que contesta un supuesto que ya figuraba en un informe entregado abre una revisión
C2 y se comunica al Broker (Documento 0 V5.3, §7.9.4 y §7.9.5; INC-T116-03 e INC-T174-01)."""
import json
import threading
import time
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.herramientas.referencia import ht09_validador_g3 as ht09
from conftest import AS_OF, nuevo_bloque

SEMANA_SIG = str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date())
SEMANA_3 = str((pd.Timestamp(AS_OF) + pd.Timedelta(days=14)).date())
PREGUNTA = {"texto": "¿Incluimos stablecoins?", "supuesto_declarado": "No se incluyen",
            "efecto_si_falso": "Se ampliaría el cribado de CRI"}


def _consulta(b, modo="BLOQUEANTE", clases=("CRI",), preguntas=(PREGUNTA,)):
    return b.consultas.enviar({"tipo": "ACLARACION_ALCANCE", "modo": modo, "clases": list(clases),
                               "preguntas": [dict(p) for p in preguntas]}, AS_OF)["cns_id"]


def _runs(b):
    return [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "RUN"]


def _bloque(tmp, universo):
    """Bloque con un espía de los mensajes que salen hacia el Broker (contrato y run_id)."""
    b = nuevo_bloque(tmp, universo)
    b._al_broker = []
    crear = b.mensajeria.crear

    def espia(contrato, emisor, receptor, cuerpo, **kw):
        m = crear(contrato, emisor, receptor, cuerpo, **kw)
        if receptor == "BROKER":
            b._al_broker.append((contrato, m.get("run_id")))
        return m
    b.mensajeria.crear = espia
    return b


def _ct02(b, run_id):
    return [x for x in b._al_broker if x == ("CT-02", run_id)]


@pytest.fixture
def entregado_con_supuesto(tmp_path, universo):
    """Pasos 1 y 2 del plan: CT-23 BLOQUEANTE sobre CRI; el ciclo pausa CRI; a la semana vence y el informe se entrega con
    el supuesto declarado."""
    b = _bloque(tmp_path, universo)
    cns = _consulta(b)
    r1 = b.ciclo(AS_OF, alcance={"clases": ["RV", "CRI"]})
    assert list(r1["paquete"]["clases"]) == ["RV"]
    r2 = b.ciclo(SEMANA_SIG, alcance={"clases": ["RV", "CRI"]})
    assert [s["cns_id"] for s in r2["paquete"]["supuestos_declarados"]] == [cns]
    assert r2.get("entrega", "ENTREGADA") == "ENTREGADA" and _ct02(b, r2["run_id"])
    return b, cns, r1, r2


def test_pb61_respuesta_tardia_que_invalida_el_supuesto_abre_una_revision_c2(entregado_con_supuesto):
    b, cns, r1, r2 = entregado_con_supuesto
    f5 = {e["id"]: e for e in _runs(b)}
    assert f5[r2["run_id"]]["supuestos_cns"] == [cns] and "supuestos_cns" not in f5[r1["run_id"]]
    antes = {e["id"] for e in _runs(b)}
    # Paso 3: respuesta tardía que contradice el supuesto
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí, inclúyelas"}], as_of=SEMANA_SIG)
    assert out["tardia"]
    rev = out["revision_c2"]
    assert rev["estado"] == "ENTREGADA" and rev["revisa"] == [r2["run_id"]] and rev["clases"] == ["CRI"]
    assert rev["supuestos_invalidados"] == [{"indice": 0, "supuesto": "No se incluyen", "respuesta": "Sí, inclúyelas"}]
    assert rev["run_id"] in out["accion"] and r2["run_id"] in out["accion"]
    # CA-1: un RUN AD_HOC nuevo, disparado por la CT-23, con los RUN- revisados
    nuevo = [e for e in _runs(b) if e["id"] not in antes]
    assert [e["id"] for e in nuevo] == [rev["run_id"]]
    run = nuevo[0]
    assert run["tipo"] == "AD_HOC" and run["entrega"] == "ENTREGADA"
    assert run["disparador"]["origen"] == "CT-23" and run["disparador"]["cns_id"] == cns
    assert run["disparador"]["revisa"] == [r2["run_id"]] and run["disparador"]["indices"] == [0]
    assert "Sí, inclúyelas" in run["alcance"]["pregunta"] and run["alcance"]["clases"] == ["CRI"]
    # CA-2: la revisión ya no lleva el supuesto, declara la revisión en sus entregables y llega al Broker por CT-02
    js = json.loads(Path(run["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    tecnico = Path(run["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    assert js["supuestos_declarados"] == [] and "supuestos_cns" not in run
    nota = [x for x in js["limitaciones"] if "Revisión C2" in x]
    assert len(nota) == 1 and cns in nota[0] and r2["run_id"] in nota[0] and "No se incluyen" in nota[0]
    assert nota[0] in tecnico
    assert next(x for x in ht09.validar(js)["comprobaciones"] if x["id"] == "C19")["resultado"] == "OK"
    assert _ct02(b, rev["run_id"])
    # CA-3: queda en la CNS- de F5
    f5_cns = b.almacen.estado("F5", clave="cns_id")[cns]
    assert f5_cns["estado"] == "RESPONDIDA" and f5_cns["indices_respondidos"] == [0]
    assert [x["run_id"] for x in f5_cns["revisiones_c2"]] == [rev["run_id"]]


def test_pb61_sin_informe_entregado_no_hay_revision(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    cns = _consulta(b)
    b.ciclo(AS_OF, alcance={"clases": ["RV", "CRI"]})                   # CRI pausado: ningún entregable lleva el supuesto
    b.consultas.vencer(SEMANA_SIG + "T12:00")
    antes = len(_runs(b))
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí, inclúyelas"}], as_of=SEMANA_SIG)
    assert out["tardia"] and out["revision_c2"] is None and "ningún informe entregado" in out["accion"]
    assert len(_runs(b)) == antes
    # una respuesta en plazo sin entrega previa tampoco abre nada
    b2 = _bloque(tmp_path / "b2", universo)
    out2 = b2.consultas.responder(_consulta(b2), [{"indice": 0, "texto": "No"}], as_of=AS_OF)
    assert not out2["tardia"] and out2["revision_c2"] is None and "accion" not in out2


def test_pb61_un_run_bloqueado_no_cuenta_como_entregado(entregado_con_supuesto):
    b, cns, _r1, r2 = entregado_con_supuesto
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "RUN", "id": r2["run_id"], "entrega": "BLOQUEADA"})
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=SEMANA_SIG)
    assert out["revision_c2"] is None


def test_pb61_segunda_respuesta_sin_indices_nuevos_no_reabre(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    otra = {"texto": "¿Incluimos tokens de gobernanza?", "supuesto_declarado": "Sí se incluyen"}
    cns = _consulta(b, preguntas=(PREGUNTA, otra))
    b.ciclo(AS_OF, alcance={"clases": ["CRI"]})
    b.ciclo(SEMANA_SIG, alcance={"clases": ["CRI"]})
    p1 = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], estado="PARCIAL", as_of=SEMANA_SIG)
    assert p1["revision_c2"]["supuestos_invalidados"] == [{"indice": 0, "supuesto": "No se incluyen", "respuesta": "Sí"}]
    n = len(_runs(b))
    p2 = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí, ya lo dije"}], estado="PARCIAL", as_of=SEMANA_SIG)
    assert p2["revision_c2"] is None and len(_runs(b)) == n                 # nada nuevo contestado: no se reabre
    # un índice booleano no es el índice 1 (True == 1 en Python) ni cuenta como contestado
    pb = b.consultas.responder(cns, [{"indice": True, "texto": "No"}], estado="PARCIAL", as_of=SEMANA_SIG)
    assert pb["revision_c2"] is None and len(_runs(b)) == n
    p3 = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}, {"indice": 1, "texto": "No"}], as_of=SEMANA_SIG)
    assert [x["indice"] for x in p3["revision_c2"]["supuestos_invalidados"]] == [1]
    # índices fuera de rango, repetidos o sin texto no cuentan
    p4 = b.consultas.responder(cns, [{"indice": 7, "texto": "x"}, {"indice": True, "texto": "x"}, {"indice": 1, "texto": ""}],
                               as_of=SEMANA_SIG)
    assert p4["revision_c2"] is None
    assert b.almacen.estado("F5", clave="cns_id")[cns]["indices_respondidos"] == [0, 1]


def test_pb61_revision_pendiente_sin_ejecutar(entregado_con_supuesto):
    b, cns, _r1, _r2 = entregado_con_supuesto
    n = len(_runs(b))
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=SEMANA_SIG, ejecutar_revision=False)
    assert out["revision_c2"]["estado"] == "PENDIENTE" and out["revision_c2"]["run_id"] is None and len(_runs(b)) == n
    assert b.almacen.estado("F5", clave="cns_id")[cns]["revisiones_c2"][-1]["estado"] == "PENDIENTE"


def test_pb61_revision_fallida_queda_anotada_y_el_error_de_control_se_relanza(entregado_con_supuesto, monkeypatch):
    b, cns, _r1, _r2 = entregado_con_supuesto

    def falla(*a, **k):
        raise RuntimeError("detalle que no debe copiarse")
    monkeypatch.setattr(b, "ciclo", falla)
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=SEMANA_SIG)
    assert out["revision_c2"]["estado"] == "FALLIDA" and out["revision_c2"]["fallo"] == "RuntimeError"
    inc = [e for e in b.almacen.leer("HA") if "revisión C2" in str(e.get("descripcion", e))]
    assert inc and "detalle que no debe copiarse" not in json.dumps(inc, ensure_ascii=False)
    # un error de control no se esconde
    b2_cns = _consulta(b, modo="NO_BLOQUEANTE")
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "RUN", "id": "RUN-2026-0900", "entrega": "ENTREGADA", "supuestos_cns": [b2_cns],
                                       "nivel_por_clase": {"CRI": "N1"}})

    def control(*a, **k):
        raise PermissionError("control")
    monkeypatch.setattr(b, "ciclo", control)
    with pytest.raises(PermissionError):
        b.consultas.responder(b2_cns, [{"indice": 0, "texto": "Sí"}], as_of=SEMANA_SIG)


def test_pb61_no_bloqueante_contestada_en_plazo_tras_una_entrega(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    cns = _consulta(b, modo="NO_BLOQUEANTE", clases=())                  # sin tipos: afecta a todo el alcance
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert [s["cns_id"] for s in r["paquete"]["supuestos_declarados"]] == [cns]
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    assert not out["tardia"] and out["revision_c2"]["revisa"] == [r["run_id"]] and out["revision_c2"]["clases"] == ["RV"]
    assert out["revision_c2"]["estado"] == "ENTREGADA"


def test_pb61_informe_de_seguimiento_c6_entregado_con_el_supuesto(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    opp = r["paquete"]["clases"]["RV"]["opciones"][0]["opp_id"]
    seg = b.seguimientos.procesar({"accion": "ALTA", "opp_id": opp, "frecuencia": "SEMANAL", "motivo": "Vigilar"}, AS_OF)["seg_id"]
    cns = _consulta(b, modo="NO_BLOQUEANTE", clases=("RV",))
    c6 = b.seguimientos.ejecutar(SEMANA_SIG)
    hecho = [x for x in c6 if x.get("seg_id") == seg and x.get("entregado")] if isinstance(c6, list) else []
    assert hecho and [s["cns_id"] for s in hecho[0]["informe"]["supuestos_declarados"]] == [cns]
    run_c6 = next(e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "RUN_C6" and e["id"] == hecho[0]["run_id"])
    assert run_c6["supuestos_cns"] == [cns]
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Otra cosa"}], as_of=SEMANA_SIG)
    assert out["revision_c2"]["revisa"] == [hecho[0]["run_id"]] and out["revision_c2"]["clases"] == ["RV"]


# ---------------------------------------------------------------- ronda r02 (QA r01 NO APTO, H-01 a H-06)
def _entregado_rv(tmp, universo, clases=(), alcance=("RV",)):
    b = _bloque(tmp, universo)
    cns = _consulta(b, modo="NO_BLOQUEANTE", clases=clases)
    r = b.ciclo(AS_OF, alcance={"clases": list(alcance)})
    assert [s["cns_id"] for s in r["paquete"]["supuestos_declarados"]] == [cns]
    return b, cns, r


def _revisiones_ct23(b):
    return [e for e in _runs(b) if (e.get("disparador") or {}).get("origen") == "CT-23"]


def test_r02_h01_dos_procesos_con_la_misma_respuesta_abren_una_sola_revision(tmp_path, universo):
    b, cns, _ = _entregado_rv(tmp_path, universo)
    b2 = nuevo_bloque(tmp_path, universo)                       # otro proceso sobre la misma carpeta de estado
    barrera = threading.Barrier(2)
    for x in (b, b2):   # los dos leen la consulta antes de que ninguno escriba
        orig = x.consultas._contestadas

        def lento(c, r, _o=orig):
            barrera.wait(timeout=60)
            time.sleep(0.3)
            return _o(c, r)
        x.consultas._contestadas = lento
    res: list = []
    hilos = [threading.Thread(target=lambda x=x: res.append(x.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)))
             for x in (b, b2)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join(900)
    assert len(res) == 2 and len([o for o in res if o["revision_c2"]]) == 1
    assert len(_revisiones_ct23(b)) == 1
    revs = b.consultas._todas()[cns]["revisiones_c2"]
    assert len(revs) == 1 and revs[0]["estado"] == "ENTREGADA" and revs[0]["msg_id"]


def test_r02_h01_la_reserva_queda_en_curso_en_la_misma_entrada_que_la_respuesta(tmp_path, universo, monkeypatch):
    b, cns, _ = _entregado_rv(tmp_path, universo)
    vistas = []

    def mira(*a, **k):
        vistas.append(b.consultas._todas()[cns])
        raise RuntimeError("x")
    monkeypatch.setattr(b, "ciclo", mira)
    b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    c = vistas[0]
    assert c["indices_respondidos"] == [0] and c["estado"] == "RESPONDIDA" and c["revisiones_c2"][0]["estado"] == "EN_CURSO"
    ultima = [e for e in b.almacen.leer("F5") if e.get("cns_id") == cns and "indices_respondidos" in e][-1]
    assert ultima["revisiones_c2"][0]["msg_id"] == c["revisiones_c2"][0]["msg_id"]   # una sola entrada: índices y reserva


def test_r02_h02_error_de_control_deja_la_revision_interrumpida_y_se_relanza(tmp_path, universo, monkeypatch):
    b, cns, _ = _entregado_rv(tmp_path, universo)
    orig = b.ciclo

    def control(*a, **k):
        raise PermissionError("control")
    monkeypatch.setattr(b, "ciclo", control)
    with pytest.raises(PermissionError):
        b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    rev = b.consultas._todas()[cns]["revisiones_c2"][0]
    assert rev["estado"] == "INTERRUMPIDA" and rev["fallo"] == "PermissionError"
    inc = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and cns in e.get("detalle", "")]
    assert inc and inc[-1]["escalado_operador"] is True and "relanzar" in inc[-1]["tratamiento"]
    assert [p["cns_id"] for p in b.consultas.revisiones_pendientes()] == [cns]
    monkeypatch.setattr(b, "ciclo", orig)
    otra = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)   # nada nuevo, pero se relanza la debida
    assert otra["revision_c2"] is None and [x["estado"] for x in otra["revisiones_relanzadas"]] == ["ENTREGADA"]
    assert len(_revisiones_ct23(b)) == 1 and b.consultas.revisiones_pendientes() == []


def test_r02_h02_la_pendiente_se_relanza_en_la_siguiente_respuesta_y_la_en_curso_solo_si_se_pide(tmp_path, universo, monkeypatch):
    b, cns, _ = _entregado_rv(tmp_path, universo)
    assert b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF, ejecutar_revision=False)["revision_c2"]["estado"] == "PENDIENTE"
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    assert [x["estado"] for x in out["revisiones_relanzadas"]] == ["ENTREGADA"]
    # una EN_CURSO (p. ej., de un proceso que murió) no se relanza sola: puede estar en marcha en otro proceso
    b2, cns2, _ = _entregado_rv(tmp_path / "b2", universo)
    monkeypatch.setattr(b2.consultas, "_ejecutar_revision", lambda cns_id, rev, as_of: rev)   # el proceso «muere» sin anotar
    b2.consultas.responder(cns2, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    monkeypatch.undo()
    assert b2.consultas.relanzar_revisiones(AS_OF) == []
    hechas = b2.consultas.relanzar_revisiones(AS_OF, estados=("EN_CURSO",))
    assert [x["estado"] for x in hechas] == ["ENTREGADA"] and len(_revisiones_ct23(b2)) == 1


def test_r02_h03_el_alcance_es_la_interseccion_con_lo_entregado(tmp_path, universo):
    b, cns, r = _entregado_rv(tmp_path, universo, clases=("CRI", "IDX"), alcance=("CRI", "RV"))
    assert sorted(r["paquete"]["clases"]) == ["CRI", "RV"]
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    assert out["revision_c2"]["clases"] == ["CRI"]


def test_r02_h03_sin_tipos_que_revisar_no_se_lanza_un_ciclo_de_todo_el_alcance(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    cns = _consulta(b, modo="NO_BLOQUEANTE", clases=())
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "RUN", "id": "RUN-2026-0900", "entrega": "ENTREGADA", "supuestos_cns": [cns]})
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    assert out["revision_c2"]["estado"] == "SIN_ALCANCE" and _runs(b)[-1]["id"] == "RUN-2026-0900"
    assert any(e.get("escalado_operador") and cns in e.get("detalle", "") for e in b.almacen.leer("HA"))


def test_r02_h04_una_respuesta_fechada_antes_de_la_entrega_no_la_revisa(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    cns = _consulta(b, modo="NO_BLOQUEANTE", clases=())
    r = b.ciclo(SEMANA_SIG, alcance={"clases": ["RV"]})
    assert [s["cns_id"] for s in r["paquete"]["supuestos_declarados"]] == [cns]
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    assert out["revision_c2"] is None and _revisiones_ct23(b) == []


def test_r02_h05_un_fallo_tras_entregar_deja_la_revision_entregada(tmp_path, universo, monkeypatch):
    b, cns, _ = _entregado_rv(tmp_path, universo)
    orig = b.ciclo

    def a_medias(*a, **k):
        orig(*a, **k)
        raise RuntimeError("secreto-del-broker 1234")
    monkeypatch.setattr(b, "ciclo", a_medias)
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    rev = out["revision_c2"]
    assert rev["estado"] == "ENTREGADA" and rev["fallo"] == "RuntimeError" and rev["run_id"] == _revisiones_ct23(b)[0]["id"]
    assert "entregada al Broker por CT-02" in out["accion"] and b.consultas.revisiones_pendientes() == []
    assert "secreto-del-broker" not in str(b.almacen.leer("HA")) + str(b.almacen.leer("F5"))


def test_r02_h06_la_fallida_va_al_operador_y_se_relanza_por_la_linea_de_ordenes(tmp_path, universo, monkeypatch):
    from bloque_a import cli
    b, cns, _ = _entregado_rv(tmp_path, universo)
    orig = b.ciclo

    def falla(*a, **k):
        raise RuntimeError("x")
    monkeypatch.setattr(b, "ciclo", falla)
    assert b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)["revision_c2"]["estado"] == "FALLIDA"
    inc = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and cns in e.get("detalle", "")]
    assert inc[-1]["escalado_operador"] is True and f"consulta-broker relanzar --cns {cns}" in inc[-1]["tratamiento"]
    monkeypatch.setattr(b, "ciclo", orig)
    args = type("A", (), {"accion": "revisiones", "cns": None, "incluir_en_curso": False})()
    assert [p["estado"] for p in cli._consulta_broker(b, args, AS_OF)] == ["FALLIDA"]
    args.accion, args.cns = "relanzar", cns
    hechas = cli._consulta_broker(b, args, AS_OF)
    assert [x["estado"] for x in hechas] == ["ENTREGADA"] and b.consultas.revisiones_pendientes() == []
    assert b.consultas._todas()[cns]["revisiones_c2"][0]["intentos"] == 2


def test_r02_h06_relanzar_reclama_bajo_el_cerrojo_y_no_repite_una_ya_hecha(tmp_path, universo, monkeypatch):
    b, cns, _ = _entregado_rv(tmp_path, universo)
    b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF, ejecutar_revision=False)
    viejas = b.consultas.revisiones_pendientes()
    assert [p["estado"] for p in viejas] == ["PENDIENTE"]
    assert [x["estado"] for x in b.consultas.relanzar_revisiones(AS_OF)] == ["ENTREGADA"]
    # otro proceso con la lista de antes (ya hecha por el primero): al reclamarla bajo el cerrojo ve que ya no está pendiente
    monkeypatch.setattr(b.consultas, "revisiones_pendientes", lambda *a, **k: viejas)
    assert b.consultas.relanzar_revisiones(AS_OF) == [] and len(_revisiones_ct23(b)) == 1


# ---------------------------------------------------------------- ronda r03 (QA r02, H-07 y H-08)
def test_r03_h07_la_en_curso_huerfana_se_avisa_una_sola_vez(tmp_path, universo, monkeypatch):
    b, cns, _ = _entregado_rv(tmp_path, universo)

    def muere(*a, **k):
        raise KeyboardInterrupt   # como un Ctrl-C o un corte: no pasa por el except de la revisión
    monkeypatch.setattr(b, "ciclo", muere)
    with pytest.raises(KeyboardInterrupt):
        b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    monkeypatch.undo()
    rev = b.consultas._todas()[cns]["revisiones_c2"][0]
    assert rev["estado"] == "EN_CURSO" and rev["proceso"]["pid"] > 0 and rev["proceso"]["host"] and rev["intentos"] == 1
    b2 = nuevo_bloque(tmp_path, universo)                       # otro día, otra instancia

    def _avisos():
        return [e for e in b2.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and "EN_CURSO sin proceso" in e.get("detalle", "")]
    b2.ciclo(SEMANA_SIG, alcance={"clases": ["RV"]})
    assert len(_avisos()) == 1                                  # el ciclo periódico la avisa
    b2.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=SEMANA_SIG)
    b2.ciclo(SEMANA_3, alcance={"clases": ["RV"]})
    avisos = _avisos()
    assert len(avisos) == 1 and avisos[0]["escalado_operador"] is True
    assert avisos[0]["tratamiento"] == f"consulta-broker relanzar --incluir-en-curso --cns {cns}"
    rev = b2.consultas._todas()[cns]["revisiones_c2"][0]
    assert rev["estado"] == "EN_CURSO" and rev["aviso_huerfana"] == avisos[0]["id"]   # no se relanza sola
    pend = b2.consultas.revisiones_pendientes()
    assert [(p["estado"], p.get("huerfana")) for p in pend] == [("EN_CURSO", True)]
    hechas = b2.consultas.relanzar_revisiones(SEMANA_3, estados=("EN_CURSO",))
    assert [x["estado"] for x in hechas] == ["ENTREGADA"] and b2.consultas._todas()[cns]["revisiones_c2"][0]["intentos"] == 2


def test_r03_h07_una_en_curso_viva_no_es_huerfana(tmp_path, universo, monkeypatch):
    from bloque_a import interfaz_broker as ib
    b, cns, _ = _entregado_rv(tmp_path, universo)
    vistas = []
    orig = b.ciclo

    def mira(*a, **k):
        vistas.append(b.consultas.huerfanas())             # la propia revisión, en marcha, no es huérfana
        return orig(*a, **k)
    monkeypatch.setattr(b, "ciclo", mira)
    b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    assert vistas == [[]]
    # de otro proceso vivo del mismo host (este mismo pytest visto desde otro pid) o de otro host: no se marca
    rev = {"estado": "EN_CURSO", "msg_id": "M", "proceso": {"host": ib.socket.gethostname(), "pid": ib.os.getppid()}}
    assert not b.consultas._es_huerfana(cns, rev)
    assert not b.consultas._es_huerfana(cns, {**rev, "proceso": {"host": "otro-host", "pid": 1}})
    assert not b.consultas._es_huerfana(cns, {"estado": "EN_CURSO", "msg_id": "M"})
    monkeypatch.setattr(ib, "_pid_vivo", lambda pid: False)
    assert b.consultas._es_huerfana(cns, rev)


def test_r03_h08_el_proceso_muere_tras_entregar_y_relanzar_no_duplica(tmp_path, universo, monkeypatch):
    b, cns, _ = _entregado_rv(tmp_path, universo)
    orig = b.ciclo
    vistos = []

    def entrega_y_muere(*a, **k):
        vistos.append(k["disparador"]["intento"])
        orig(*a, **k)
        raise KeyboardInterrupt
    monkeypatch.setattr(b, "ciclo", entrega_y_muere)
    with pytest.raises(KeyboardInterrupt):
        b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    monkeypatch.undo()
    assert vistos == [1] and len(_revisiones_ct23(b)) == 1
    hechas = b.consultas.relanzar_revisiones(AS_OF, estados=("EN_CURSO",))
    assert [(x["estado"], x["run_id"]) for x in hechas] == [("ENTREGADA", _revisiones_ct23(b)[0]["id"])]
    assert len(_revisiones_ct23(b)) == 1 and b.consultas.revisiones_pendientes() == []


def test_r03_h08_cada_reclamacion_lleva_su_numero_de_intento(tmp_path, universo, monkeypatch):
    b, cns, _ = _entregado_rv(tmp_path, universo)
    orig = b.ciclo
    vistos = []

    def falla(*a, **k):
        vistos.append(k["disparador"]["intento"])
        raise RuntimeError("x")
    monkeypatch.setattr(b, "ciclo", falla)
    b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    b.consultas.relanzar_revisiones(AS_OF)
    assert vistos == [1, 2] and b.consultas._todas()[cns]["revisiones_c2"][0]["intentos"] == 2
    monkeypatch.setattr(b, "ciclo", orig)
    b.consultas.relanzar_revisiones(AS_OF)
    assert b.consultas._todas()[cns]["revisiones_c2"][0]["intentos"] == 3
    assert [e["disparador"]["intento"] for e in _revisiones_ct23(b)] == [3]


# ---------------------------------------------------------------- ronda de cierre de la QA r03 (bajos H-09 a H-11)
def _avisos_huerfana(b, cns):
    return [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and "EN_CURSO sin proceso" in e.get("detalle", "")
            and cns in e.get("detalle", "")]


def test_cierre_h09_la_revision_esta_en_marcha_desde_la_reserva(tmp_path, universo, monkeypatch):
    from bloque_a import interfaz_broker as ib
    b, cns, _ = _entregado_rv(tmp_path, universo)
    b2 = nuevo_bloque(tmp_path, universo)
    vistas = []
    orig = b.consultas._ejecutar_revision

    def entre_reserva_y_ciclo(*a, **k):   # otra instancia del mismo proceso mira justo tras soltar el cerrojo
        vistas.append(b2.consultas.huerfanas())
        return orig(*a, **k)
    monkeypatch.setattr(b.consultas, "_ejecutar_revision", entre_reserva_y_ciclo)
    b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    assert vistas == [[]] and _avisos_huerfana(b, cns) == [] and not ib._EN_MARCHA   # y se da de baja al terminar


def test_cierre_h09_se_da_de_baja_tambien_sin_alcance_y_si_falla_la_escritura(tmp_path, universo, monkeypatch):
    from bloque_a import interfaz_broker as ib
    b = _bloque(tmp_path, universo)
    cns = _consulta(b, modo="NO_BLOQUEANTE", clases=())
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "RUN", "id": "RUN-2026-0900", "entrega": "ENTREGADA", "supuestos_cns": [cns]})
    assert b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)["revision_c2"]["estado"] == "SIN_ALCANCE"
    assert not ib._EN_MARCHA
    b2, cns2, _ = _entregado_rv(tmp_path / "b2", universo)
    orig = b2.almacen.escribir

    def falla_f5(archivo, autor, entrada, *a, **k):
        if archivo == "F5" and entrada.get("cns_id") == cns2 and entrada.get("revisiones_c2"):
            raise OSError("disco")
        return orig(archivo, autor, entrada, *a, **k)
    monkeypatch.setattr(b2.almacen, "escribir", falla_f5)
    with pytest.raises(OSError):
        b2.consultas.responder(cns2, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    assert not ib._EN_MARCHA


def test_cierre_h10_la_clave_lleva_la_carpeta_del_almacen(tmp_path, universo, monkeypatch):
    bx, cx, _ = _entregado_rv(tmp_path / "x", universo)
    by, cy, _ = _entregado_rv(tmp_path / "y", universo)

    def muere(*a, **k):
        raise KeyboardInterrupt
    monkeypatch.setattr(bx, "ciclo", muere)
    with pytest.raises(KeyboardInterrupt):
        bx.consultas.responder(cx, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    monkeypatch.undo()
    vistas = []
    orig = by.ciclo

    def mira(*a, **k):   # Y ejecuta la suya, con los mismos ids que la huérfana de X
        vistas.append(bx.consultas.huerfanas())
        return orig(*a, **k)
    monkeypatch.setattr(by, "ciclo", mira)
    by.consultas.responder(cy, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    mx, my = (z.consultas._todas()[c]["revisiones_c2"][0]["msg_id"] for z, c in ((bx, cx), (by, cy)))
    assert (cx, mx) == (cy, my) and len(vistas[0]) == 1 and len(_avisos_huerfana(bx, cx)) == 1


def test_cierre_h11_lo_que_no_se_puede_juzgar_se_dice(tmp_path, universo, monkeypatch):
    b, cns, _ = _entregado_rv(tmp_path, universo)
    monkeypatch.setattr(b.consultas, "_ejecutar_revision", lambda cns_id, rev, as_of: rev)   # el proceso «muere» sin anotar
    b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    monkeypatch.undo()
    msg = b.consultas._todas()[cns]["revisiones_c2"][0]["msg_id"]
    b.consultas._anotar_revision(cns, msg, {"proceso": {"host": "otro-host", "pid": 1}, "aviso_huerfana": None})
    antes = len(_avisos_huerfana(b, cns))
    pend = b.consultas.revisiones_pendientes()
    assert [(p["estado"], p["huerfana"]) for p in pend] == [("EN_CURSO", None)] and "no se puede juzgar" in pend[0]["nota_huerfana"]
    assert len(_avisos_huerfana(b, cns)) == antes                 # sin aviso nuevo: no se sabe si vive
    b.consultas._anotar_revision(cns, msg, {"proceso": {}})
    assert [p["huerfana"] for p in b.consultas.revisiones_pendientes()] == [None]
