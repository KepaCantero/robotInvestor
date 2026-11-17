"""QA r01 de T-169 (revisor) · sondas propias de las finales pendientes (H-02), de qué fallos paran la consulta (H-01) y de
las referencias por tipo (H-03).

Uso, desde `bloque_a/11_Ejecutor` de la copia de trabajo:
  ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-169/revisores/r01_01_sondas.py
Todo con el cliente simulado, sin red ni coste. Las que documentan un hallazgo llevan `xfail(strict=True)` con su ID: afirman lo
esperado y fallan con el código de hoy. Las de procesos están en `r01_02_procesos_y_base.py`.
"""
import copy
import json
import sys
import threading
from pathlib import Path

import pytest

EJECUTOR = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJECUTOR / "tests"))
sys.path.insert(0, str(EJECUTOR))

from bloque_a import respuesta_final
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config
from bloque_a.herramientas.ht01_datos import cargar_universo
from bloque_a.llm import ReplayFaltante
from conftest import AS_OF, nuevo_bloque

ORO = "¿Qué opinas del oro frente a la plata a 6 meses?"
DIV = "Analiza qué conviene hacer ahora"
CORREO = "luis.perez.qa169@ejemplo.com"
D2 = "2026-06-12"
D3 = "2026-06-19"


@pytest.fixture(scope="module")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def _bloque(tmp, universo):
    return nuevo_bloque(tmp, universo, cfg=cargar_config(extra={"modo": "backtest"}))


def _espiar(b):
    vistos = []
    crear = b.mensajeria.crear

    def f(*a, **k):
        m = crear(*a, **k)
        vistos.append(copy.deepcopy(m))
        return m

    b.mensajeria.crear = f
    return vistos


def _finales(ms, qry=None):
    return [m for m in ms if m["contrato"] == "CT-03" and m["tipo_mensaje"] == "RETORNO" and m.get("respuesta_final")
            and (qry is None or m["query_id"] == qry)]


def _pendiente(monkeypatch, b, as_of=AS_OF, texto=ORO, **kw):
    """Una consulta cuya final no sale: `enviar` falla dentro de `consulta`, después de registrar la provisional."""
    real, real_p = respuesta_final.enviar, respuesta_final.enviar_pendientes
    monkeypatch.setattr(respuesta_final, "enviar_pendientes", lambda *a, **k: [])   # las anteriores siguen pendientes

    def cae(*a, **k):
        raise OSError("corte simulado")

    monkeypatch.setattr(respuesta_final, "enviar", cae)
    with pytest.raises(OSError):
        b.consulta(texto, as_of=as_of, ejecutar_escalado=False, **kw)
    monkeypatch.setattr(respuesta_final, "enviar", real)
    monkeypatch.setattr(respuesta_final, "enviar_pendientes", real_p)
    qry = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY"][-1]["id"]
    assert qry in [x for x, _ in respuesta_final.pendientes(b.almacen)]
    return qry


# ------------------------------------------------------------------ H-02 · orden, fechas y estado manipulado
def test_p01_dos_pendientes_salen_en_su_orden_y_solo_las_de_su_fecha(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    q1 = _pendiente(monkeypatch, b, AS_OF)
    q2 = _pendiente(monkeypatch, b, D3)
    ms = _espiar(b)
    b.ciclo(D2)                                   # entre las dos: solo la primera (la segunda es «futura» para este ciclo)
    assert [m["query_id"] for m in _finales(ms)] == [q1]
    b.ciclo(D3)
    assert [m["query_id"] for m in _finales(ms)] == [q1, q2]
    b.ciclo(D3)
    assert [m["query_id"] for m in _finales(ms)] == [q1, q2]          # ninguna dos veces
    f5 = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY" and e.get("respuesta_final")]
    assert [e["id"] for e in f5] == [q1, q2]


def test_p02_una_final_borrada_a_mano_no_se_reenvia(tmp_path, universo, monkeypatch):
    """Estado manipulado: una entrada posterior de la QRY- con `respuesta_final: None` la hace parecer pendiente."""
    b = _bloque(tmp_path, universo)
    q = b.consulta(ORO, as_of=AS_OF, ejecutar_escalado=False)
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q["query_id"], "respuesta_final": None})
    ms = _espiar(b)
    salidas = respuesta_final.enviar_pendientes(b, AS_OF)
    assert not _finales(ms) and all(s["repetido"] for s in salidas)


def test_p03_ocho_hilos_con_enviar_pendientes(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    ms = _espiar(b)
    barrera, errores = threading.Barrier(8), []

    def uno():
        barrera.wait()
        try:
            respuesta_final.enviar_pendientes(b, AS_OF)
        except Exception as e:   # noqa: BLE001
            errores.append(e)

    hs = [threading.Thread(target=uno) for _ in range(8)]
    for h in hs:
        h.start()
    for h in hs:
        h.join()
    assert not errores and len(_finales(ms, q)) == 1
    assert len([e for e in b.almacen.leer("F5") if e.get("id") == q and e.get("respuesta_final")]) == 1


@pytest.mark.xfail(strict=True, reason="H-03 de T-169 (baja): el apartado no va bajo la transacción; se aparta una vez por hilo o proceso")
def test_p04_ocho_hilos_con_una_pendiente_rechazada(tmp_path, universo, monkeypatch):
    """La que la mensajería rechaza se aparta «una vez»: ¿también con varios hilos a la vez?"""
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q, "fallo_analisis": f"Error de {CORREO}"})
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q,
                                       "escalado": {**b.almacen.estado("F5", clave="id")[q]["escalado"], "estado_run": "FALLIDO"}})
    barrera = threading.Barrier(8)

    def uno():
        barrera.wait()
        respuesta_final.enviar_pendientes(b, AS_OF)

    hs = [threading.Thread(target=uno) for _ in range(8)]
    for h in hs:
        h.start()
    for h in hs:
        h.join()
    marcas = [e for e in b.almacen.leer("F5") if e.get("id") == q and e.get("final_no_enviable")]
    inc = [e for e in b.almacen.leer("HA") if q in e.get("detalle", "") and "apartada" in e.get("detalle", "")]
    print("P04", len(marcas), "marcas y", len(inc), "incidencias")
    ha = json.dumps(b.almacen.leer("HA"), ensure_ascii=False)
    assert CORREO not in ha and marcas and marcas[0]["final_no_enviable"] == {"error": "DatosSensibles"}
    assert len(marcas) == 1 and len(inc) == 1


# ------------------------------------------------------------------ H-02 · una pendiente que no se puede enviar
@pytest.mark.xfail(strict=True, reason="H-01 de T-169 (media): una pendiente con un error que no es un rechazo para todos los ciclos")
def test_p05_una_pendiente_malformada_no_bloquea_el_ciclo_semanal(tmp_path, universo, monkeypatch):
    """Una QRY- pendiente cuyo `escalado` no lleva `clases` (estado de otra versión o manipulado): `construir` lanza KeyError.
    Esperado: se aparta con incidencia escalada y el ciclo sigue. Hoy, cada `ciclo` y cada `consulta` se paran con ese KeyError,
    sin dejar nada en HA, hasta que alguien toque F5 a mano."""
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    esc = {k: v for k, v in b.almacen.estado("F5", clave="id")[q]["escalado"].items() if k != "clases"}
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q, "escalado": None})
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q, "escalado": esc})
    fallos = []
    for fecha in (D2, D3):
        try:
            b.ciclo(fecha)
        except Exception as e:   # noqa: BLE001
            fallos.append(type(e).__name__)
    ha = [e for e in b.almacen.leer("HA") if q in e.get("detalle", "")]
    print("P05", fallos, len(ha), "incidencias de", q)
    assert not fallos and ha and ha[0].get("escalado_operador")


# ------------------------------------------------------------------ H-01 · otros errores que se absorben
@pytest.mark.xfail(strict=True, reason="H-02 de T-169 (baja): ReplayFaltante del modo «reproducir» se absorbe como FALLIDO")
def test_p06_una_respuesta_sin_grabar_en_modo_reproducir_para_la_consulta(tmp_path, universo, monkeypatch):
    """En modo `--cliente replay --replay-modo reproducir` una respuesta que no está grabada es un fallo de la reproducción, no
    del análisis: antes de T-162 paraba la consulta; hoy da una final FALLIDO e incidencia HERRAMIENTA."""
    b = _bloque(tmp_path, universo)

    def ciclo(*a, **k):
        raise ReplayFaltante("Respuesta no grabada para AG-02")

    monkeypatch.setattr(b, "ciclo", ciclo)
    with pytest.raises(ReplayFaltante):
        b.consulta(DIV, as_of=AS_OF)


def test_p07_los_controles_paran_sin_dejar_nada(tmp_path, universo, monkeypatch):
    """Comprobación directa de H-01, con un error de control lanzado tras registrar el RUN- (la auditoría)."""
    from bloque_a.almacen import EscrituraFueraDeReserva
    b = nuevo_bloque(tmp_path, universo)

    def auditar(*a, **k):
        raise EscrituraFueraDeReserva("x")

    b._auditar = auditar
    ms = _espiar(b)
    with pytest.raises(EscrituraFueraDeReserva):
        b.consulta("¿Qué opinas de la renta variable india frente a la indonesia a 6 meses?", as_of=AS_OF)
    assert not [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY"]
    assert not [m for m in ms if m["contrato"] == "CT-03" and m["tipo_mensaje"] == "RETORNO"]
    assert not [e for e in b.almacen.leer("HA") if e.get("tipo") == "HERRAMIENTA"]


def test_p08_la_provisional_registrada_es_de_otro_mensaje(tmp_path, universo, monkeypatch):
    """Estado manipulado: la `provisional_msg_id` de F5 apunta al encargo CT-03 del Broker, no a la provisional. Se anota lo
    que pasa (la final se enlaza a lo que diga F5; no hay registro persistente de mensajes con que compararlo)."""
    b = _bloque(tmp_path, universo)
    ms = _espiar(b)
    q = _pendiente(monkeypatch, b)
    encargo = next(m["msg_id"] for m in ms if m["contrato"] == "CT-03" and m["tipo_mensaje"] == "ENCARGO")
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q, "provisional_msg_id": encargo})
    fin = respuesta_final.enviar_pendientes(b, AS_OF)
    print("P08", fin[0]["respuesta_final"]["provisional_msg_id"] == encargo)
