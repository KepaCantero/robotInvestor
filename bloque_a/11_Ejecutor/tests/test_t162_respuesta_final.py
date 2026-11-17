"""T-162 · PB-07: respuesta final por CT-03 cuando termina el análisis escalado de una consulta del Broker.

Todo con el cliente simulado (`MockClient`), sin red ni coste. El escenario nominal (un informe entregado y la pregunta de PB-07)
se ejecuta una vez por módulo; los de fallo usan un bloque solo con divisas y un ciclo sustituido, que no analiza nada.
"""
import copy
import json
import threading
from pathlib import Path

import jsonschema
import pytest
from bloque_a.cli import main as cli_main
from bloque_a.configuracion import cargar_config
from bloque_a.contratos import DatosSensibles
from conftest import AS_OF, DATOS, nuevo_bloque

from bloque_a import respuesta_final

PREGUNTA_PB07 = "¿Qué opinas de la renta variable india frente a la indonesia a 6 meses?"
PREGUNTA_ORO = "¿Qué opinas del oro frente a la plata a 6 meses?"
SOBRE = {"msg_id", "contrato", "version_contrato", "emisor", "receptor", "timestamp", "tipo_mensaje", "query_id", "run_id",
         "consumo", "estado"}
# Las claves de la provisional antes de T-162 (formas_flujos_mock.json, flujo consulta_que_escala)
CLAVES_PROVISIONAL = {"autoevaluacion", "clase_consulta", "confianza", "consumo", "contrato", "emisor", "escalado", "estado",
                      "limitaciones", "msg_id", "query_id", "receptor", "referencias", "respuesta", "ruta", "timestamp",
                      "tipo_mensaje", "version_contrato"}
ESCALADO = {"nivel", "clases", "plazo_estimado", "respuesta_provisional", "run_id", "estado_run"}
ANEXO_B = Path(__file__).resolve().parent / "goldens" / "anexo_b_esquemas.json"


def _espiar(b) -> list[dict]:
    """Los mensajes enteros que crea la mensajería del bloque (el registro solo guarda cinco claves)."""
    vistos: list[dict] = []
    crear = b.mensajeria.crear

    def crear_y_anotar(*args, **kwargs):
        msg = crear(*args, **kwargs)
        vistos.append(copy.deepcopy(msg))
        return msg

    b.mensajeria.crear = crear_y_anotar
    return vistos


def _ct03_retornos(mensajes: list[dict]) -> list[dict]:
    return [m for m in mensajes if m["contrato"] == "CT-03" and m["tipo_mensaje"] == "RETORNO"]


def _cuerpo(msg: dict) -> dict:
    return {k: v for k, v in msg.items() if k not in SOBRE | {"autoevaluacion"}}


def _f5_finales(b, qry_id: str) -> list[dict]:
    return [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY" and e.get("id") == qry_id and e.get("respuesta_final")]


@pytest.fixture(scope="module")
def escalada(tmp_path_factory, universo):
    """PB-07: informe entregado (un ciclo de renta variable) y la pregunta del plan, que escala a análisis."""
    b = nuevo_bloque(tmp_path_factory.mktemp("t162"), universo)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    mensajes = _espiar(b)
    q = b.consulta(PREGUNTA_PB07, as_of=AS_OF)
    return b, q, mensajes


def _bloque_div(tmp_path, universo):
    return nuevo_bloque(tmp_path, universo, cfg=cargar_config(extra={"modo": "backtest"}))


# ---------------------------------------------------------------- CA-1 · la final sale, enlazada y validada
def test_ca1_la_final_sale_despues_de_la_provisional_enlazada_a_la_consulta_y_al_run(escalada):
    b, q, mensajes = escalada
    provisional, final = _ct03_retornos(mensajes)[:2]
    assert provisional["msg_id"] == q["msg_id"] and final["msg_id"] == q["respuesta_final"]["msg_id"]
    assert mensajes.index(provisional) < mensajes.index(final)
    assert (final["emisor"], final["receptor"], final["estado"]) == ("AG-01", "BROKER", "COMPLETO")
    assert final["query_id"] == q["query_id"] and final["run_id"] == q["escalado"]["run_id"]
    assert final["respuesta_final"] == {"provisional_msg_id": provisional["msg_id"], "resultado_analisis": "ENTREGADO"}
    assert final["escalado"] == provisional["escalado"]
    jsonschema.validate(_cuerpo(final), respuesta_final.ESQUEMA)
    b.mensajeria.validar(final)                                                         # canal, R8 y campos mínimos
    anexo_b = json.loads(ANEXO_B.read_text(encoding="utf-8"))["CT-03.RETORNO"]          # y la forma del Anexo B
    jsonschema.validate(final, anexo_b)
    ct02 = next(m for m in mensajes if m["contrato"] == "CT-02" and m["run_id"] == final["run_id"])
    assert mensajes.index(ct02) < mensajes.index(final)                                  # después de la entrega del RUN-


def test_ca2_las_referencias_son_las_del_run_y_existen_en_la_memoria(escalada):
    b, q, _ = escalada
    fin = q["respuesta_final"]
    run_id = fin["run_id"]
    run = b.almacen.estado("F5", clave="id")[run_id]
    f3, f1 = b.almacen.estado("F3"), b.almacen.estado("F1")
    clm = {e["clm_id"] for e in b.almacen.leer("F2") if e.get("tipo_entrada") == "CLM"}
    prg = {e["prg_id"]: e for e in b.almacen.leer("F4") if e.get("tipo_entrada") == "ALTA"}
    refs = fin["referencias"]
    assert refs[0] == run_id and len(refs) == len(set(refs))
    top3 = [o for lst in run["top3_por_clase"].values() for o in lst]
    assert top3 and [r for r in refs if r.startswith("OPP-")] == top3
    for opp in top3:
        assert set(f3[opp]["tnd_ids"]) <= set(refs) and set(f3[opp]["evidencias"]) <= set(refs)
        assert {p for p, e in prg.items() if e.get("run_id") == run_id and e.get("opp_id") == opp and p.startswith("PRG-")} <= set(refs)
        assert opp in fin["respuesta"]
    for r in refs:   # cada una es la clave de una entrada, no solo una mención
        assert r in f3 or r in f1 or r in clm or r in prg or (r == run_id and run["tipo_entrada"] == "RUN")
    confs = [f3[o]["confianza"] for o in top3]
    assert fin["confianza"] == min(confs, key=respuesta_final.CONFIANZAS.index)


def test_ca2_la_final_queda_en_f5_en_la_misma_qry(escalada):
    b, q, _ = escalada
    qry = b.almacen.estado("F5", clave="id")[q["query_id"]]
    assert qry["estado"] == "RESPONDIDA_FINAL" and qry["respuesta_final"]["msg_id"] == q["respuesta_final"]["msg_id"]
    # provisional, registro de su msg_id (T-169, H-02) y final
    assert [h["tipo"] for h in qry["_historial"]] == ["QRY", "QRY", "QRY"] and qry["provisional_msg_id"] == q["msg_id"]
    assert qry["respuesta"] == q["respuesta"] and qry["referencias"] == q["referencias"]   # lo de la provisional, intacto
    assert qry["referencias_descartadas_final"] == []


# ---------------------------------------------------------------- CA-6 · lo que ya existía no cambia
def test_ca6_la_provisional_no_cambia(escalada):
    b, q, mensajes = escalada
    provisional = _ct03_retornos(mensajes)[0]
    assert set(provisional) == CLAVES_PROVISIONAL and set(provisional["escalado"]) == ESCALADO
    f5 = next(e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY" and e["id"] == q["query_id"])
    assert {k: provisional[k] for k in ("clase_consulta", "ruta", "respuesta", "referencias", "confianza", "escalado")} == \
           {k: f5[k] for k in ("clase_consulta", "ruta", "respuesta", "referencias", "confianza", "escalado")}
    assert provisional["estado"] == "COMPLETO" and provisional["consumo"] == {} and provisional["limitaciones"] == []


def test_ca6_la_pregunta_repetida_no_cuenta_la_final(escalada):
    b, q, _ = escalada
    qry = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY" and e["id"] == q["query_id"]]
    assert len(qry) == 3 and not any("tema_normalizado" in e for e in qry[1:])   # T-169: + el registro de la provisional
    tema = qry[0]["tema_normalizado"]
    assert sum(e.get("tema_normalizado") == tema for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY") == 1


def test_ca6_la_consulta_n0_no_lleva_final(escalada):
    b, _, mensajes = escalada
    antes = len(_ct03_retornos(mensajes))
    r = b.consulta("¿Por qué no aparece ninguna opción nueva de renta fija esta semana?", as_of=AS_OF)
    assert r["ruta"] == "N0" and r["respuesta_final"] is None
    assert len(_ct03_retornos(mensajes)) == antes + 1


# ---------------------------------------------------------------- CA-4 · idempotencia
def test_ca4_enviar_dos_veces_no_duplica(escalada):
    b, q, mensajes = escalada
    n_msg, n_f5 = len(mensajes), len(b.almacen.leer("F5"))
    otra = respuesta_final.enviar(b, q["query_id"], q["msg_id"], AS_OF)
    assert otra["repetido"] is True and {**otra, "repetido": False} == q["respuesta_final"]
    assert len(mensajes) == n_msg and len(b.almacen.leer("F5")) == n_f5
    assert len(_f5_finales(b, q["query_id"])) == 1


def test_ca4_dos_hilos_a_la_vez_envian_una_sola_final(tmp_path, universo, monkeypatch):
    b = _bloque_div(tmp_path, universo)
    mensajes = _espiar(b)
    real = respuesta_final.enviar
    monkeypatch.setattr(respuesta_final, "enviar", lambda *a, **k: None)                # la consulta no la envía
    q = b.consulta(PREGUNTA_ORO, as_of=AS_OF, ejecutar_escalado=False)
    monkeypatch.setattr(respuesta_final, "enviar", real)
    salidas: list[dict] = []
    hilos = [threading.Thread(target=lambda: salidas.append(real(b, q["query_id"], q["msg_id"], AS_OF))) for _ in range(2)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    assert sorted(s["repetido"] for s in salidas) == [False, True]
    assert salidas[0]["msg_id"] == salidas[1]["msg_id"]
    assert len(_ct03_retornos(mensajes)) == 2 and len(_f5_finales(b, q["query_id"])) == 1


# ---------------------------------------------------------------- CA-3 · fallo cerrado
def test_ca3_si_el_run_falla_la_final_lo_dice_sin_referencias(tmp_path, universo, monkeypatch):
    b = _bloque_div(tmp_path, universo)
    mensajes = _espiar(b)

    def falla(*a, **k):
        raise RuntimeError("detalle interno ES91 2100 0418 4502 0005 1332")

    monkeypatch.setattr(b, "ciclo", falla)
    q = b.consulta(PREGUNTA_ORO, as_of=AS_OF)
    assert q["escalado"]["estado_run"] == "FALLIDO" and q["escalado"]["run_id"] is None
    fin = q["respuesta_final"]
    assert fin["estado"] == "SIN_RESULTADO" and fin["respuesta_final"]["resultado_analisis"] == "FALLIDO"
    assert fin["referencias"] == [] and fin["run_id"] is None
    assert "no terminó" in fin["respuesta"] and "no se confirma" in fin["respuesta"]
    assert any("RuntimeError" in x for x in fin["limitaciones"])
    assert fin["confianza"] in ("especulativo", "en disputa")
    assert "detalle interno" not in json.dumps(mensajes, ensure_ascii=False)          # el texto del error no sale (R8)
    final = _ct03_retornos(mensajes)[-1]
    assert "run_id" not in final and final["query_id"] == q["query_id"]
    inc = [e for e in b.almacen.leer("HA") if e.get("tipo") == "HERRAMIENTA" and q["query_id"] in e.get("detalle", "")]
    assert len(inc) == 1 and "RuntimeError" in inc[0]["detalle"] and "detalle interno" not in inc[0]["detalle"]
    assert b.almacen.estado("F5", clave="id")[q["query_id"]]["estado"] == "FINAL_SIN_RESULTADO"


def test_ca3_un_run_sin_entrega_da_sin_entrega(tmp_path, universo):
    b = _bloque_div(tmp_path, universo)            # solo divisas activas: un análisis de materias primas no analiza nada
    q = b.consulta(PREGUNTA_ORO, contexto={"clases": ["MP"]}, as_of=AS_OF)
    fin = q["respuesta_final"]
    run_id = q["escalado"]["run_id"]
    assert b.almacen.estado("F5", clave="id")[run_id]["entrega"] == "SIN_RESULTADO"
    assert fin["respuesta_final"]["resultado_analisis"] == "SIN_ENTREGA" and fin["estado"] == "SIN_RESULTADO"
    assert fin["referencias"] == [run_id] and fin["run_id"] == run_id
    assert "terminó sin entrega" in fin["respuesta"] and "perfil no activo" in " ".join(fin["limitaciones"])


@pytest.mark.parametrize("registrar, motivo", [(True, "G3 bloqueó la entrega"), (False, "no consta en F5")])
def test_ca3_un_run_bloqueado_o_sin_registro_da_sin_entrega(tmp_path, universo, monkeypatch, registrar, motivo):
    b = _bloque_div(tmp_path, universo)

    def ciclo(as_of, **k):
        run_id = b.almacen.nuevo_id("RUN")
        if registrar:
            # con el disparador que lleva el RUN- de verdad (T-169, H-03: solo cuenta el RUN- que lanzó la consulta)
            b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "RUN", "id": run_id, "estado": "PARCIAL", "entrega": "BLOQUEADA",
                                               "disparador": k["disparador"],
                                               "top3_por_clase": {"DIV": ["OPP-2026-0001"]}, "limitaciones": []})
        return {"run_id": run_id, "estado": "PARCIAL" if registrar else "COMPLETO"}

    monkeypatch.setattr(b, "ciclo", ciclo)
    q = b.consulta(PREGUNTA_ORO, as_of=AS_OF)
    fin = q["respuesta_final"]
    assert fin["respuesta_final"]["resultado_analisis"] == "SIN_ENTREGA" and motivo in fin["respuesta"]
    assert fin["referencias"] == ([q["escalado"]["run_id"]] if registrar else [])
    assert fin["run_id"] == (q["escalado"]["run_id"] if registrar else None)
    assert "OPP-2026-0001" not in json.dumps(fin)                                       # nada de lo no entregado


def test_ca3_sin_escalado_la_final_dice_que_no_se_ejecuto(tmp_path, universo):
    b = _bloque_div(tmp_path, universo)
    mensajes = _espiar(b)
    q = b.consulta(PREGUNTA_ORO, as_of=AS_OF, ejecutar_escalado=False)
    fin = q["respuesta_final"]
    assert fin["respuesta_final"]["resultado_analisis"] == "NO_EJECUTADO" and fin["estado"] == "SIN_RESULTADO"
    assert fin["referencias"] == [] and "no se lanzó" in fin["respuesta"]
    assert not any(m["contrato"] == "CT-05" for m in mensajes) and len(_ct03_retornos(mensajes)) == 2


def test_ca3_sin_escalado_por_la_cli(tmp_path, capsys):
    assert cli_main(["--datos", str(DATOS), "--estado", str(tmp_path / "estado"), "--salida", str(tmp_path / "sal"), "--as-of", AS_OF,
                     "consulta", PREGUNTA_ORO, "--sin-escalado"]) == 0
    r = json.loads(capsys.readouterr().out)
    assert r["ruta"] == "ANALITICA" and r["respuesta_final"]["respuesta_final"]["resultado_analisis"] == "NO_EJECUTADO"


def test_ca3_una_referencia_que_no_existe_no_se_cita(escalada, monkeypatch):
    b, q, _ = escalada
    qry = b.almacen.estado("F5", AS_OF, clave="id")[q["query_id"]]
    opps = [r for r in q["respuesta_final"]["referencias"] if r.startswith("OPP-")]
    clm = [r for r in q["respuesta_final"]["referencias"] if r.startswith("CLM-")][-1]   # de la última opción, que sí se cita
    real = respuesta_final._existentes
    monkeypatch.setattr(respuesta_final, "_existentes", lambda a, f: real(a, f) - {opps[0], clm})
    cuerpo, _, estado, descartadas = respuesta_final.construir(b.almacen, qry, q["msg_id"], AS_OF)
    assert opps[0] not in cuerpo["referencias"] and clm not in cuerpo["referencias"] and clm in descartadas
    assert opps[0] not in cuerpo["respuesta"] and opps[1] in cuerpo["referencias"]
    respuesta_final.validar(cuerpo, estado)


@pytest.mark.parametrize("estropear, error", [
    (lambda c, e: ({**c, "referencias": ["XYZ-2026-0001"]}, e), respuesta_final.RespuestaFinalInvalida),
    (lambda c, e: ({**c, "ruta": "N0"}, e), respuesta_final.RespuestaFinalInvalida),
    (lambda c, e: (c, "COMPLETO"), respuesta_final.RespuestaFinalInvalida),                     # estado incoherente con FALLIDO
    (lambda c, e: ({**c, "respuesta": c["respuesta"] + " ES91 2100 0418 4502 0005 1332"}, e), DatosSensibles),   # R8, mensajería
])
def test_ca1_una_final_que_no_cumple_el_esquema_no_sale_ni_se_registra(tmp_path, universo, monkeypatch, estropear, error):
    b = _bloque_div(tmp_path, universo)
    mensajes = _espiar(b)
    real_enviar, real_construir = respuesta_final.enviar, respuesta_final.construir
    monkeypatch.setattr(respuesta_final, "enviar", lambda *a, **k: None)
    monkeypatch.setattr(b, "ciclo", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("x")))
    q = b.consulta(PREGUNTA_ORO, as_of=AS_OF)

    def construir(*a, **k):
        cuerpo, run_id, estado, desc = real_construir(*a, **k)
        cuerpo, estado = estropear(cuerpo, estado)
        return cuerpo, run_id, estado, desc

    monkeypatch.setattr(respuesta_final, "construir", construir)
    n_msg, n_f5 = len(mensajes), len(b.almacen.leer("F5"))
    with pytest.raises(error):
        real_enviar(b, q["query_id"], q["msg_id"], AS_OF)
    assert len(mensajes) == n_msg and len(b.almacen.leer("F5")) == n_f5 and not _f5_finales(b, q["query_id"])
    monkeypatch.setattr(respuesta_final, "construir", real_construir)                   # sin el defecto, sale una vez
    assert real_enviar(b, q["query_id"], q["msg_id"], AS_OF)["repetido"] is False


def test_ca1_una_consulta_n0_o_inexistente_no_admite_final(escalada):
    b, _, _ = escalada
    n0 = b.consulta("¿Cuál es el estado de las opciones vigentes?", as_of=AS_OF)
    assert n0["ruta"] == "N0"
    n0 = n0["query_id"]
    for qry_id in (n0, "QRY-2026-9999"):
        with pytest.raises(respuesta_final.RespuestaFinalInvalida):
            respuesta_final.enviar(b, qry_id, "MSG-2026-000001", AS_OF)


# ---------------------------------------------------------------- CA-5 · determinismo
def test_ca5_dos_ejecuciones_dan_la_misma_final(tmp_path, universo):
    salidas = []
    for n in range(2):
        b = _bloque_div(tmp_path / str(n), universo)
        mensajes = _espiar(b)
        b.consulta("Analiza qué conviene hacer ahora", as_of=AS_OF)
        salidas.append(json.dumps(_ct03_retornos(mensajes), ensure_ascii=False, sort_keys=True))
    assert salidas[0] == salidas[1]
    finales = json.loads(salidas[0])
    assert len(finales) == 2 and finales[1]["respuesta_final"]["resultado_analisis"] in respuesta_final.RESULTADOS


# ---------------------------------------------------------------- CA-7 · PB-07 de punta a punta
def test_pb07_de_punta_a_punta_con_el_simulado(escalada):
    b, q, mensajes = escalada
    esc = q["escalado"]
    assert q["clase_consulta"] == "CONTRASTE" and q["ruta"] == "ANALITICA"                        # clase y ruta
    assert esc["nivel"] in ("N1", "N2", "N3") and esc["plazo_estimado"] and esc["respuesta_provisional"] == q["respuesta"]
    run = b.almacen.estado("F5", clave="id")[esc["run_id"]]
    assert run["tipo"] == "AD_HOC" and run["disparador"]["qry_id"] == q["query_id"] and list(run["nivel_por_clase"]) == ["RV"]
    tipos = [(m["contrato"], m["tipo_mensaje"]) for m in mensajes]
    encargo, ct05 = tipos.index(("CT-03", "ENCARGO")), tipos.index(("CT-05", "ENCARGO"))
    ct02 = tipos.index(("CT-02", "RETORNO"))
    provisional, final = (mensajes.index(m) for m in _ct03_retornos(mensajes)[:2])
    assert encargo < ct05 < ct02 < provisional < final                                             # seguir el CT-05 resultante
    assert mensajes[ct05]["tipo"] == "AD_HOC" and mensajes[ct02]["run_id"] == esc["run_id"]
    fin = q["respuesta_final"]
    assert fin["estado"] == "COMPLETO" and any(r.startswith("OPP-") for r in fin["referencias"])   # final con referencias
    assert mensajes[final]["query_id"] == q["query_id"] and mensajes[final]["run_id"] == esc["run_id"]
