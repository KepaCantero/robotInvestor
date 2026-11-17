"""QA r01 de T-174 (revisor independiente): ataques a la revisión C2 por respuesta CT-23 (PB-61).

Uso (desde la copia):  cd bloque_a/11_Ejecutor && python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-174/revisores/r01_01_ataques.py
Cada prueba documenta lo que se observa; las que fallan señalan un hallazgo (ver qa.md)."""
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


def _runs(b):
    return [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "RUN"]


def _revs(b):
    return [e for e in _runs(b) if (e.get("disparador") or {}).get("origen") == "CT-23"]


def _entregado(tmp, universo, modo="NO_BLOQUEANTE", clases=(), alcance=("RV",)):
    b = nuevo_bloque(tmp, universo)
    cns = b.consultas.enviar({"tipo": "ACLARACION_ALCANCE", "modo": modo, "clases": list(clases), "preguntas": [dict(P)]}, AS_OF)["cns_id"]
    r = b.ciclo(AS_OF, alcance={"clases": list(alcance)})
    assert [s["cns_id"] for s in r["paquete"]["supuestos_declarados"]] == [cns]
    return b, cns, r


# A1 · Repetición: la misma respuesta tres veces abre una sola revisión
def test_a1_repeticion_idempotente(tmp_path, universo):
    b, cns, _ = _entregado(tmp_path, universo)
    outs = [b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF) for _ in range(3)]
    assert outs[0]["revision_c2"] and outs[1]["revision_c2"] is None and outs[2]["revision_c2"] is None
    assert len(_revs(b)) == 1


# A2 · Concurrencia: dos instancias (dos procesos del ejecutor sobre la misma carpeta) responden a la vez
def test_a2_concurrencia_dos_respuestas_iguales(tmp_path, universo):
    b, cns, _ = _entregado(tmp_path, universo)
    b2 = nuevo_bloque(tmp_path, universo)            # misma carpeta de estado: otro "proceso"
    barrera = threading.Barrier(2)
    for x in (b, b2):   # ensancha la ventana entre leer `indices_respondidos` y escribirlos (no cambia la lógica)
        orig = x.consultas._contestadas

        def lento(c, r, _o=orig):
            barrera.wait(timeout=30)
            time.sleep(0.3)
            return _o(c, r)
        x.consultas._contestadas = lento
    res = []
    hs = [threading.Thread(target=lambda x=x: res.append(x.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)))
          for x in (b, b2)]
    [h.start() for h in hs]
    [h.join(600) for h in hs]
    abiertas = [o for o in res if o.get("revision_c2")]
    assert len(abiertas) == 1, f"{len(abiertas)} revisiones por la misma respuesta: {[o['revision_c2']['run_id'] for o in abiertas]}"


# A3 · Un error de control en la revisión se relanza... pero la respuesta ya quedó registrada con sus índices:
# reintentar no reabre y en F5 no queda rastro de que faltaba una revisión
def test_a3_error_de_control_no_pierde_la_revision(tmp_path, universo):
    b, cns, _ = _entregado(tmp_path, universo)
    orig = b.ciclo

    def control(*a, **k):
        raise PermissionError("control")
    b.ciclo = control
    with pytest.raises(PermissionError):
        b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    b.ciclo = orig
    c = b.consultas._todas()[cns]
    huella = c.get("revisiones_c2") or [i for i in b.almacen.leer("HA") if cns in str(i)]
    otra = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    assert huella or otra["revision_c2"], ("revisión C2 debida y perdida: índices marcados como respondidos "
                                           f"({c.get('indices_respondidos')}), sin revisiones_c2 ni incidencia, y el reintento no la abre")


# A4 · Una CNS- ajena (entrante, o sin RUN entregado con su supuesto) no abre revisión aunque haya RUN entregados
def test_a4_cns_ajena(tmp_path, universo):
    b, cns, _ = _entregado(tmp_path, universo)
    ent = b.consultas.entrante("Dato espontáneo", as_of=AS_OF)["cns_id"]
    assert b.consultas.responder(ent, [{"indice": 0, "texto": "x"}], as_of=AS_OF)["revision_c2"] is None
    ajena = b.consultas.enviar({"tipo": "OTRA", "modo": "NO_BLOQUEANTE", "clases": ["CRI"], "preguntas": [dict(P)]}, AS_OF)["cns_id"]
    assert b.consultas.responder(ajena, [{"indice": 0, "texto": "x"}], as_of=AS_OF)["revision_c2"] is None
    with pytest.raises(KeyError):
        b.consultas.responder("CNS-2026-9999", [{"indice": 0, "texto": "x"}], as_of=AS_OF)
    assert _revs(b) == []


# A5 · RUN no entregado: BLOQUEADA, sin campo entrega o con otro valor, no cuenta
@pytest.mark.parametrize("entrega", ["BLOQUEADA", None, "PENDIENTE", "entregada"])
def test_a5_run_no_entregado(tmp_path, universo, entrega):
    b, cns, r = _entregado(tmp_path, universo)
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "RUN", "id": r["run_id"], "entrega": entrega})
    assert b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)["revision_c2"] is None


# A6 · Entradas raras en `respuestas`: ni revisión ni excepción no controlada
@pytest.mark.parametrize("resp", [[], [{"indice": -1, "texto": "x"}], [{"indice": 0.0, "texto": "x"}], [{"indice": "0", "texto": "x"}],
                                  [{"indice": 0, "texto": "   "}], [{"indice": 0, "texto": None}], [{"indice": 0}],
                                  [{"indice": float("nan"), "texto": "x"}]])
def test_a6_respuestas_raras(tmp_path, universo, resp):
    b, cns, _ = _entregado(tmp_path, universo)
    try:
        out = b.consultas.responder(cns, resp, as_of=AS_OF)
    except (ValueError, TypeError, Exception) as e:   # rechazo de la mensajería: aceptable si no deja revisión
        assert _revs(b) == [], e
        return
    assert out["revision_c2"] is None and _revs(b) == []


# A7 · Alcance: la consulta declara CRI e IDX y lo entregado solo analizó CRI. ¿La revisión amplía el alcance a IDX?
def test_a7_alcance_no_amplia_lo_entregado(tmp_path, universo):
    b, cns, r = _entregado(tmp_path, universo, clases=("CRI", "IDX"), alcance=("CRI", "RV"))
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    print("clases de la revisión:", out["revision_c2"]["clases"], "| analizadas en lo entregado:", sorted(r["paquete"]["clases"]))
    assert set(out["revision_c2"]["clases"]) <= set(r["paquete"]["clases"])


# A8 · Fallo a mitad (el RUN de la revisión se escribe y luego algo falla): ENTREGADA (H-05, corregido en la r03), con su run_id y sin texto
def test_a8_fallo_tras_escribir_el_run(tmp_path, universo):
    b, cns, _ = _entregado(tmp_path, universo)
    orig = b.ciclo

    def a_medias(*a, **k):
        orig(*a, **k)
        raise RuntimeError("secreto-del-broker 1234")
    b.ciclo = a_medias
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    rev = out["revision_c2"]
    assert rev["estado"] == "ENTREGADA" and rev["run_id"] == _revs(b)[0]["id"]   # r03: H-05 (el RUN llegó al Broker)
    assert "secreto-del-broker" not in str(b.almacen.leer("HA")) and "secreto-del-broker" not in str(b.almacen.leer("F5"))
    print("RUN de la revisión:", _revs(b)[0].get("entrega"), "| estado de la revisión en F5:", b.consultas._todas()[cns]["revisiones_c2"][-1]["estado"])


# A9 · Respuesta con fecha anterior a la entrega del RUN revisado (as_of en el pasado)
def test_a9_respuesta_con_fecha_anterior_a_la_entrega(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    cns = b.consultas.enviar({"tipo": "OTRA", "modo": "NO_BLOQUEANTE", "preguntas": [dict(P)]}, AS_OF)["cns_id"]
    r = b.ciclo(SEM2, alcance={"clases": ["RV"]})
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    print("revisión con as_of", AS_OF, "de un RUN entregado el", SEM2, "->", out["revision_c2"] and out["revision_c2"]["revisa"])
    assert out["revision_c2"] is None or r["run_id"] not in out["revision_c2"]["revisa"]


# A10 · Coste: la revisión consume presupuesto como un AD_HOC cualquiera (se lee lo que registra F5)
def test_a10_consumo_de_la_revision(tmp_path, universo):
    b, cns, r = _entregado(tmp_path, universo)
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    run = next(e for e in _runs(b) if e["id"] == out["revision_c2"]["run_id"])
    orig = next(e for e in _runs(b) if e["id"] == r["run_id"])
    print("consumo original:", orig.get("consumo"), "| revisión:", run.get("consumo"), "| nivel:", run.get("nivel_por_clase"))
    assert run.get("consumo") is not None
