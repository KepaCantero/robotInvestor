"""QA r02 de T-174 (revisor independiente): concurrencia entre responder y relanzar, EN_CURSO huérfana y relanzado.

Uso (desde la copia):  cd bloque_a/11_Ejecutor && python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-174/revisores/r02_01_ataques.py"""
import sys
import threading
import time
from pathlib import Path

import pandas as pd
import pytest

TESTS = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor" / "tests"
sys.path.insert(0, str(TESTS))
from conftest import AS_OF, nuevo_bloque, universo  # noqa: E402,F401

SEM2 = str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date())
P = {"texto": "¿Incluimos stablecoins?", "supuesto_declarado": "No se incluyen"}


def _revs(b):
    return [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "RUN" and (e.get("disparador") or {}).get("origen") == "CT-23"]


def _entregado(tmp, universo):
    b = nuevo_bloque(tmp, universo)
    cns = b.consultas.enviar({"tipo": "OTRA", "modo": "NO_BLOQUEANTE", "preguntas": [dict(P)]}, AS_OF)["cns_id"]
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    return b, cns


def _lento(b, barrera, metodo):
    """Ensancha la ventana justo antes del cerrojo de reclamación (no cambia la lógica)."""
    orig = getattr(b.consultas, metodo)

    def f(*a, **k):
        barrera.wait(timeout=60)
        time.sleep(0.3)
        return orig(*a, **k)
    setattr(b.consultas, metodo, f)


def _a_la_vez(*fs):
    res, errs = [], []

    def run(f):
        try:
            res.append(f())
        except BaseException as e:  # noqa: BLE001
            errs.append(e)
    hs = [threading.Thread(target=run, args=(f,)) for f in fs]
    [h.start() for h in hs]
    [h.join(900) for h in hs]
    return res, errs


# B1 · Una PENDIENTE: un proceso la relanza mientras otro recibe una respuesta repetida (que también relanza): una revisión
def test_b1_relanzar_y_responder_a_la_vez(tmp_path, universo):
    b, cns = _entregado(tmp_path, universo)
    b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF, ejecutar_revision=False)
    b2 = nuevo_bloque(tmp_path, universo)
    bar = threading.Barrier(2)
    _lento(b, bar, "revisiones_pendientes")
    _lento(b2, bar, "revisiones_pendientes")
    _res, errs = _a_la_vez(lambda: b.consultas.relanzar_revisiones(AS_OF),
                           lambda: b2.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF))
    assert not errs, errs
    assert len(_revs(b)) == 1, [r["id"] for r in _revs(b)]
    assert [r["estado"] for r in b.consultas._todas()[cns]["revisiones_c2"]] == ["ENTREGADA"]


# B2 · Dos relanzar a la vez sobre una FALLIDA: una sola revisión
def test_b2_dos_relanzar_a_la_vez(tmp_path, universo):
    b, cns = _entregado(tmp_path, universo)
    orig = b.ciclo
    b.ciclo = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("x"))
    assert b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)["revision_c2"]["estado"] == "FALLIDA"
    b.ciclo = orig
    b2 = nuevo_bloque(tmp_path, universo)
    bar = threading.Barrier(2)
    _lento(b, bar, "revisiones_pendientes")
    _lento(b2, bar, "revisiones_pendientes")
    _res, errs = _a_la_vez(lambda: b.consultas.relanzar_revisiones(AS_OF), lambda: b2.consultas.relanzar_revisiones(AS_OF))
    assert not errs, errs
    assert len(_revs(b)) == 1


# B3 · Dos respuestas distintas a la vez (índices 0 y 1): cada una abre la suya, sin perder ninguna en revisiones_c2
def test_b3_dos_respuestas_distintas_a_la_vez(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    cns = b.consultas.enviar({"tipo": "OTRA", "modo": "NO_BLOQUEANTE", "preguntas": [dict(P), {"texto": "¿Y DeFi?", "supuesto_declarado": "No se incluyen protocolos DeFi"}]},
                             AS_OF)["cns_id"]
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    b2 = nuevo_bloque(tmp_path, universo)
    bar = threading.Barrier(2)
    _lento(b, bar, "_contestadas")
    _lento(b2, bar, "_contestadas")
    _res, errs = _a_la_vez(lambda: b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], estado="PARCIAL", as_of=AS_OF),
                           lambda: b2.consultas.responder(cns, [{"indice": 1, "texto": "Sí"}], estado="PARCIAL", as_of=AS_OF))
    assert not errs, errs
    c = b.consultas._todas()[cns]
    assert sorted(c["indices_respondidos"]) == [0, 1], c["indices_respondidos"]
    assert len(c["revisiones_c2"]) == 2 and all(r["estado"] == "ENTREGADA" for r in c["revisiones_c2"]), c["revisiones_c2"]
    assert len(_revs(b)) == 2


# B4 · EN_CURSO huérfana: el proceso muere en mitad del ciclo (BaseException: Ctrl-C, SIGTERM con KeyboardInterrupt, OOM)
def test_b4_en_curso_huerfana_se_detecta_y_se_avisa(tmp_path, universo):
    b, cns = _entregado(tmp_path, universo)

    def muere(*a, **k):
        raise KeyboardInterrupt
    orig = b.ciclo
    b.ciclo = muere
    with pytest.raises(KeyboardInterrupt):
        b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    b.ciclo = orig
    # "otro día, otro proceso": nueva instancia; llega la respuesta repetida y corre el ciclo semanal siguiente
    b2 = nuevo_bloque(tmp_path, universo)
    out = b2.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=SEM2)
    b2.ciclo(SEM2, alcance={"clases": ["RV"]})
    estado = [r["estado"] for r in b2.consultas._todas()[cns]["revisiones_c2"]]
    avisos = [i for i in b2.almacen.leer("HA") if cns in str(i)]
    print("estado:", estado, "| relanzadas por responder:", out.get("revisiones_relanzadas"), "| avisos en HA:", len(avisos),
          "| listada en revisiones_pendientes:", [r["estado"] for r in b2.consultas.revisiones_pendientes()])
    assert estado == ["EN_CURSO"]                      # no se relanza sola (desviación 2, correcta)
    assert avisos, "EN_CURSO huérfana: ninguna incidencia ni aviso al operador; solo la ve quien ejecute «consulta-broker revisiones»"


# B5 · --incluir-en-curso sobre una EN_CURSO viva (otro proceso ejecutándola) duplica la revisión: queda a cargo del operador
def test_b5_incluir_en_curso_con_la_revision_viva(tmp_path, universo):
    b, cns = _entregado(tmp_path, universo)
    b2 = nuevo_bloque(tmp_path, universo)
    empezado, seguir = threading.Event(), threading.Event()
    orig = b.ciclo

    def lento(*a, **k):
        empezado.set()
        seguir.wait(120)
        return orig(*a, **k)
    b.ciclo = lento
    h = threading.Thread(target=lambda: b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF))
    h.start()
    empezado.wait(120)
    r = b2.consultas.relanzar_revisiones(AS_OF, estados=("EN_CURSO",))
    seguir.set()
    h.join(900)
    print("relanzadas con EN_CURSO viva:", [x.get("run_id") for x in r], "| RUN CT-23:", [x["id"] for x in _revs(b)])
    assert len(_revs(b)) == 2    # se documenta: la orden es del operador y la ayuda del CLI lo advierte
