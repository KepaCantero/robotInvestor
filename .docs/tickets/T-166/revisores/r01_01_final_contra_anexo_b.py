"""QA r01 de T-166 · cada frase del párrafo «Respuesta final (V5.3)» del Anexo B, medida con el ejecutor (mock, sin red).

Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-166/revisores/r01_01_final_contra_anexo_b.py
Las pruebas «hallazgo_*» documentan lo que el párrafo NO dice bien: pasan mientras el código haga lo que hace hoy.
"""
import copy
import sys
from pathlib import Path

import pytest

EJ = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
sys.path[:0] = [str(EJ), str(EJ / "tests")]
from conftest import AS_OF, nuevo_bloque, cargar_universo, RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.contratos import CanalNoPrevisto, DatosSensibles  # noqa: E402
from bloque_a.herramientas.ht01_datos import FugaDeInformacion  # noqa: E402
from bloque_a.llm import ReplayFaltante  # noqa: E402
from bloque_a import respuesta_final as rf  # noqa: E402

PB07 = "¿Qué opinas de la renta variable india frente a la indonesia a 6 meses?"
DIV = "Analiza qué conviene hacer ahora"
CUERPO = {"clase_consulta", "ruta", "respuesta", "referencias", "confianza", "escalado", "limitaciones", "respuesta_final"}
SOBRE = {"msg_id", "contrato", "version_contrato", "emisor", "receptor", "timestamp", "tipo_mensaje", "query_id", "run_id",
         "consumo", "estado", "autoevaluacion"}


@pytest.fixture(scope="session")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def _espiar(b):
    vistos, crear = [], b.mensajeria.crear

    def otro(*a, **k):
        m = crear(*a, **k)
        vistos.append(copy.deepcopy(m))
        return m
    b.mensajeria.crear = otro
    return vistos


def _ct03(ms):
    return [m for m in ms if m["contrato"] == "CT-03" and m["tipo_mensaje"] == "RETORNO"]


def _div(tmp, universo):
    return nuevo_bloque(tmp, universo, cfg=cargar_config(extra={"modo": "backtest"}))


@pytest.fixture(scope="module")
def nominal(tmp_path_factory, universo):
    b = nuevo_bloque(tmp_path_factory.mktemp("r01"), universo)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    ms = _espiar(b)
    q = b.consulta(PB07, as_of=AS_OF)
    return b, q, ms


def test_campos_sobre_y_f5_nominal(nominal):
    b, q, ms = nominal
    prov, fin = _ct03(ms)[:2]
    cuerpo = set(fin) - SOBRE
    assert cuerpo == CUERPO                                                    # «y ningún otro campo»
    assert "respuesta_final" not in prov                                       # opcional: la provisional no lo lleva
    assert fin["escalado"] == prov["escalado"]                                 # «el mismo que la provisional»
    assert (fin["emisor"], fin["receptor"]) == ("AG-01", "BROKER")
    assert fin["query_id"] == q["query_id"] and fin["run_id"] == q["escalado"]["run_id"]
    assert fin["respuesta_final"]["provisional_msg_id"] == prov["msg_id"]
    res = fin["respuesta_final"]["resultado_analisis"]
    assert fin["estado"] == rf.RESULTADOS[res]
    f5 = b.almacen.estado("F5")[q["query_id"]]
    assert f5["estado"] == rf.ESTADO_F5[fin["estado"]] and f5["provisional_msg_id"] == prov["msg_id"]
    # referencias: el RUN- primero, sin repetir, solo con los cinco prefijos
    refs = fin["referencias"]
    assert refs[0] == q["escalado"]["run_id"] and len(refs) == len(set(refs))
    assert all(r.split("-")[0] in ("RUN", "OPP", "TND", "CLM", "PRG") for r in refs)
    # una sola vez
    again = rf.enviar(b, q["query_id"], None, AS_OF)
    assert again["repetido"] and len([m for m in _ct03(ms) if m.get("respuesta_final")]) == 1


def test_orden_de_referencias_por_opcion(nominal):
    b, q, _ = nominal
    fin = q["respuesta_final"]
    run = b.almacen.estado("F5")[q["escalado"]["run_id"]]
    f3 = b.almacen.estado("F3")
    esperado = [run["id"]]
    for opps in run["top3_por_clase"].values():
        for o in opps:
            e = f3[o]
            esperado += [o, *[t for t in (e.get("tnd_ids") or [e.get("tnd_id")]) if t], *(e.get("evidencias") or [])]
            esperado += [x["prg_id"] for x in b.almacen.leer("F4") if x.get("tipo_entrada") == "ALTA"
                         and x.get("run_id") == run["id"] and x.get("opp_id") == o]
    vistos = list(dict.fromkeys(esperado))
    assert fin["referencias"] == [x for x in vistos if x in fin["referencias"]]
    assert set(fin["referencias"]) <= set(vistos)


def test_no_ejecutado_sin_referencias_y_sobre_sin_run(tmp_path, universo):
    b = _div(tmp_path, universo)
    ms = _espiar(b)
    q = b.consulta(DIV, as_of=AS_OF, ejecutar_escalado=False)
    fin = [m for m in _ct03(ms) if m.get("respuesta_final")][0]
    assert fin["respuesta_final"]["resultado_analisis"] == "NO_EJECUTADO" and fin["referencias"] == []
    assert fin["estado"] == "SIN_RESULTADO" and q["respuesta_final"]["run_id"] is None
    assert "no se confirma ni se amplía" in fin["respuesta"]
    assert fin["confianza"] in ("en disputa", "especulativo")


def test_hallazgo_sobre_sin_run_id_no_es_nulo_es_ausente(tmp_path, universo):
    """Anexo B: «`run_id` el del RUN- solo si consta en F5 y lo lanzó esta consulta (si no, nulo)». En el sobre del CT-03, la
    clave no está (la mensajería solo la pone si hay valor); nulo solo en la copia guardada en F5."""
    b = _div(tmp_path, universo)
    ms = _espiar(b)
    b.consulta(DIV, as_of=AS_OF, ejecutar_escalado=False)
    fin = [m for m in _ct03(ms) if m.get("respuesta_final")][0]
    assert "run_id" not in fin


@pytest.mark.parametrize("error", [FugaDeInformacion("x"), ReplayFaltante("x"), CanalNoPrevisto("x")],
                         ids=lambda e: type(e).__name__)
def test_hallazgo_errores_que_no_son_de_integridad_ni_del_almacen_tambien_paran(tmp_path, universo, monkeypatch, error):
    """Anexo B: «Un fallo de integridad o de control del almacén durante el análisis para la consulta». También paran (sin
    provisional ni final, no FALLIDO) la fuga de información de HT-01, la falta de grabación del replay y los controles de la
    mensajería (`respuesta_final.ERRORES_DE_CONTROL`)."""
    b = _div(tmp_path, universo)
    ms = _espiar(b)

    def ciclo(*a, **k):
        raise error
    monkeypatch.setattr(b, "ciclo", ciclo)
    with pytest.raises(type(error)):
        b.consulta(DIV, as_of=AS_OF)
    assert not _ct03(ms)
    assert not [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY"]


def test_error_corriente_da_fallido(tmp_path, universo, monkeypatch):
    b = _div(tmp_path, universo)

    def ciclo(*a, **k):
        raise KeyError("x")
    monkeypatch.setattr(b, "ciclo", ciclo)
    q = b.consulta(DIV, as_of=AS_OF)
    fin = q["respuesta_final"]
    assert fin["respuesta_final"]["resultado_analisis"] == "FALLIDO" and fin["estado"] == "SIN_RESULTADO"
    assert len(fin["referencias"]) <= 1
    assert b.almacen.estado("F5")[q["query_id"]]["estado"] == "FINAL_SIN_RESULTADO"


def test_hallazgo_un_rechazo_r8_de_la_final_escribe_en_ha(tmp_path, universo, monkeypatch):
    """Anexo B: «La final se valida con su esquema y por la mensajería antes de escribir nada». Un rechazo R8 de la mensajería
    deja una incidencia SEGURIDAD en HA (y el contador MSG- avanza): lo que no se escribe es la final en F5."""
    b = _div(tmp_path, universo)
    real = rf.construir

    def construir(*a, **k):
        cuerpo, run_id, estado, desc = real(*a, **k)
        cuerpo["limitaciones"] = cuerpo["limitaciones"] + ["contacto: ana.qa.r01@ejemplo.com"]
        return cuerpo, run_id, estado, desc
    monkeypatch.setattr(rf, "construir", construir)
    antes = len([e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"])
    with pytest.raises(DatosSensibles):
        b.consulta(DIV, as_of=AS_OF, ejecutar_escalado=False)
    despues = [e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"]
    assert len(despues) == antes + 1
    q = [e for e in b.almacen.estado("F5").values() if e.get("tipo_entrada") == "QRY"][0]
    assert not q.get("respuesta_final")                                        # en F5 no se escribe la final


def test_pendiente_con_la_fecha_de_su_consulta_y_se_aparta_una_vez(tmp_path, universo, monkeypatch):
    b = _div(tmp_path, universo)
    real = rf.enviar
    monkeypatch.setattr(rf, "enviar", lambda *a, **k: None)
    q = b.consulta(DIV, as_of=AS_OF, ejecutar_escalado=False)
    monkeypatch.setattr(rf, "enviar", real)
    assert rf.pendientes(b.almacen) == [(q["query_id"], AS_OF)] or rf.pendientes(b.almacen)[0][0] == q["query_id"]
    fechas = []
    construir = rf.construir

    def espia(alm, qry, msg, as_of, fallo=None):
        fechas.append(str(as_of)[:10])
        return construir(alm, qry, msg, as_of, fallo)
    monkeypatch.setattr(rf, "construir", espia)
    b.consulta(DIV, as_of="2026-06-12", ejecutar_escalado=False)
    assert fechas[0] == AS_OF


@pytest.mark.parametrize("provisional, final", [("establecido", "especulativo"), ("probable", "especulativo"),
                                                ("especulativo", "especulativo"), ("en disputa", "en disputa")])
def test_sin_resultado_la_confianza_es_la_mas_baja_entre_la_provisional_y_especulativo(tmp_path, universo, monkeypatch,
                                                                                       provisional, final):
    """Anexo B: «sin opciones o sin resultado, la más baja entre la de la provisional y especulativo». Ninguna prueba del
    implementador ni de T-162/T-169 lo ejercita (el mutante M4 de r01_03 vive)."""
    b = _div(tmp_path, universo)
    real = rf.construir

    def construir(alm, qry, msg, as_of, fallo=None):
        return real(alm, {**qry, "confianza": provisional}, msg, as_of, fallo)
    monkeypatch.setattr(rf, "construir", construir)
    q = b.consulta(DIV, as_of=AS_OF, ejecutar_escalado=False)
    assert q["respuesta_final"]["confianza"] == final
