"""T-169 r02 · hallazgos de la QA r01 de T-169 (`.docs/tickets/T-169/qa.md`): H-01 a H-04.

Todo con el cliente simulado, sin red ni coste, con un bloque solo de divisas.
"""
import copy
import json
import threading

import pytest
from bloque_a.configuracion import cargar_config
from bloque_a.contratos import DatosSensibles
from bloque_a.llm import ReplayFaltante
from conftest import AS_OF, nuevo_bloque

from bloque_a import respuesta_final

DIV = "Analiza qué conviene hacer ahora"
ORO = "¿Qué opinas del oro frente a la plata a 6 meses?"
CORREO = "ana.garcia.r02@ejemplo.com"
D2, D3 = "2026-06-12", "2026-06-19"


def _bloque(tmp_path, universo):
    return nuevo_bloque(tmp_path, universo, cfg=cargar_config(extra={"modo": "backtest"}))


def _espiar(b) -> list[dict]:
    vistos: list[dict] = []
    crear = b.mensajeria.crear

    def f(*a, **k):
        m = crear(*a, **k)
        vistos.append(copy.deepcopy(m))
        return m

    b.mensajeria.crear = f
    return vistos


def _finales(mensajes):
    return [m["query_id"] for m in mensajes if m["contrato"] == "CT-03" and m["tipo_mensaje"] == "RETORNO" and m.get("respuesta_final")]


def _pendiente(monkeypatch, b, fecha=AS_OF) -> str:
    """Una consulta (sin escalado) cuya final no sale, en `fecha`."""
    real = respuesta_final.enviar
    monkeypatch.setattr(respuesta_final, "enviar", lambda *a, **k: None)
    q = b.consulta(ORO, as_of=fecha, ejecutar_escalado=False)
    monkeypatch.setattr(respuesta_final, "enviar", real)
    return q["query_id"]


def _marcas(b, q):
    return [e for e in b.almacen.leer("F5") if e.get("id") == q and e.get("final_no_enviable")]


def _apartadas(b, q):
    return [e for e in b.almacen.leer("HA") if q in e.get("detalle", "") and "apartada" in e.get("detalle", "")]


def _con_correo(b, q):
    """Estado que hace que la mensajería rechace la final (R8): la clase del fallo guardada lleva un correo."""
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q, "fallo_analisis": f"Error de {CORREO}"})
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q,
                                       "escalado": {**b.almacen.estado("F5", clave="id")[q]["escalado"], "estado_run": "FALLIDO"}})


# ================================================================ H-01 · una pendiente que no se puede construir no para el bloque
def test_r02_h01_una_pendiente_malformada_se_aparta_y_los_ciclos_siguen(tmp_path, universo, monkeypatch):
    """La sonda p05: el `escalado` de la QRY- sin `clases` hace que `construir` lance KeyError."""
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    esc = {k: v for k, v in b.almacen.estado("F5", clave="id")[q]["escalado"].items() if k != "clases"}
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q, "escalado": None})
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q, "escalado": esc})
    mensajes = _espiar(b)
    b.ciclo(D2)
    b.ciclo(D3)                                                                 # el segundo ni la reintenta ni vuelve a escalar
    assert [m["final_no_enviable"] for m in _marcas(b, q)] == [{"error": "KeyError"}]
    inc = _apartadas(b, q)
    assert len(inc) == 1 and inc[0]["escalado_operador"] is True and q not in _finales(mensajes)
    assert respuesta_final.pendientes(b.almacen) == []


def test_r02_h01_un_error_corriente_en_una_pendiente_no_para_la_consulta(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    q1 = _pendiente(monkeypatch, b)
    real = respuesta_final.construir

    def construir(almacen, qry, *a, **k):
        if qry.get("id") == q1:
            raise RuntimeError("texto-interno-r02")
        return real(almacen, qry, *a, **k)

    monkeypatch.setattr(respuesta_final, "construir", construir)
    q2 = b.consulta(ORO, as_of=AS_OF, ejecutar_escalado=False)
    assert q2["respuesta_final"]["repetido"] is False
    assert [m["final_no_enviable"] for m in _marcas(b, q1)] == [{"error": "RuntimeError"}] and len(_apartadas(b, q1)) == 1
    assert "texto-interno-r02" not in json.dumps(b.almacen.leer("HA"), ensure_ascii=False)


# ================================================================ H-02 · ReplayFaltante para la consulta
def test_r02_h02_una_respuesta_sin_grabar_en_modo_reproducir_para_la_consulta(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    mensajes = _espiar(b)

    def ciclo(*a, **k):
        raise ReplayFaltante("Respuesta no grabada para AG-02")

    monkeypatch.setattr(b, "ciclo", ciclo)
    with pytest.raises(ReplayFaltante):
        b.consulta(DIV, as_of=AS_OF)
    assert not [m for m in mensajes if m["contrato"] == "CT-03" and m["tipo_mensaje"] == "RETORNO"]
    assert not [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY"]
    assert not [e for e in b.almacen.leer("HA") if e.get("tipo") == "HERRAMIENTA"]


# ================================================================ H-03 · se aparta una sola vez con varios hilos
def test_r02_h03_ocho_hilos_apartan_y_escalan_una_sola_vez(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    _con_correo(b, q)
    barrera, errores = threading.Barrier(8), []

    def uno():
        barrera.wait()
        try:
            respuesta_final.enviar_pendientes(b, AS_OF)
        except Exception as e:   # noqa: BLE001 - se cuentan, no debe haber ninguno
            errores.append(e)

    hilos = [threading.Thread(target=uno) for _ in range(8)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    assert not errores
    assert [m["final_no_enviable"] for m in _marcas(b, q)] == [{"error": "DatosSensibles"}] and len(_apartadas(b, q)) == 1
    assert CORREO not in json.dumps(b.almacen.leer("HA"), ensure_ascii=False)


# ================================================================ H-04 · Q02, Q03 y Q10
def test_r02_h04_dos_pendientes_salen_en_su_orden_en_la_misma_llamada(tmp_path, universo, monkeypatch):
    """Mata Q02 (pendientes en orden inverso)."""
    b = _bloque(tmp_path, universo)
    q1, q2 = _pendiente(monkeypatch, b), _pendiente(monkeypatch, b)
    assert [x for x, _ in respuesta_final.pendientes(b.almacen)] == [q1, q2]
    mensajes = _espiar(b)
    enviadas = respuesta_final.enviar_pendientes(b, AS_OF)
    assert _finales(mensajes) == [q1, q2] and [e["msg_id"] for e in enviadas] == [m["msg_id"] for m in mensajes]


def test_r02_h04_solo_salen_las_pendientes_hasta_su_fecha(tmp_path, universo, monkeypatch):
    """Mata Q10 (pendientes sin fecha de corte): un ciclo con fecha anterior a una consulta no envía su final."""
    b = _bloque(tmp_path, universo)
    q1, q2 = _pendiente(monkeypatch, b, AS_OF), _pendiente(monkeypatch, b, D3)
    mensajes = _espiar(b)
    b.ciclo(D2)
    assert _finales(mensajes) == [q1]
    b.ciclo(D3)
    assert _finales(mensajes) == [q1, q2]


def test_r02_h04_un_rechazo_con_el_almacen_roto_para_y_no_aparta(tmp_path, universo, monkeypatch):
    """Mata Q03 (el rechazo se aparta sin mirar la integridad): la mensajería rechaza la final y, a la vez, el sello de F2 está
    roto; no se aparta nada y se propaga."""
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    _con_correo(b, q)
    real = respuesta_final.construir

    def construir(almacen, qry, *a, **k):
        salida = real(almacen, qry, *a, **k)
        ruta = almacen._ruta_sellos
        sellos = json.loads(ruta.read_text(encoding="utf-8"))
        sellos["F2"] = [999, "0" * 64]
        ruta.write_text(json.dumps(sellos), encoding="utf-8")
        return salida

    monkeypatch.setattr(respuesta_final, "construir", construir)
    with pytest.raises(DatosSensibles):
        respuesta_final.enviar_pendientes(b, AS_OF)
    assert not _marcas(b, q) and not _apartadas(b, q) and not all(b.almacen.verificar_integridad().values())


def test_r02_h03_una_lista_de_pendientes_vieja_no_vuelve_a_apartar(tmp_path, universo, monkeypatch):
    """Determinista (mata R04): otro proceso leyó la lista de pendientes antes de que esta se apartara; al llegarle el turno,
    dentro de la transacción ve que ya está apartada y no la aparta ni la escala otra vez."""
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    _con_correo(b, q)
    vieja = respuesta_final.pendientes(b.almacen, AS_OF)
    respuesta_final.enviar_pendientes(b, AS_OF)
    monkeypatch.setattr(respuesta_final, "pendientes", lambda *a, **k: list(vieja))
    assert respuesta_final.enviar_pendientes(b, AS_OF) == []
    assert len(_marcas(b, q)) == 1 and len(_apartadas(b, q)) == 1


# ================================================================ ronda de cierre · hallazgos de la QA r02 de T-169
def _romper_f2(almacen):
    ruta = almacen._ruta_sellos
    sellos = json.loads(ruta.read_text(encoding="utf-8"))
    sellos["F2"] = [999, "0" * 64]
    ruta.write_text(json.dumps(sellos), encoding="utf-8")


def _construir_que_lanza(monkeypatch, q, error, romper=False):
    real = respuesta_final.construir

    def construir(almacen, qry, *a, **k):
        if qry.get("id") == q:
            if romper:
                _romper_f2(almacen)
            raise error
        return real(almacen, qry, *a, **k)

    monkeypatch.setattr(respuesta_final, "construir", construir)


@pytest.mark.parametrize("error", [KeyError("clases"), RuntimeError("x"), OSError("disco")], ids=lambda e: type(e).__name__)
def test_cierre_h02_un_error_corriente_con_el_almacen_roto_para_y_no_aparta(tmp_path, universo, monkeypatch, error):
    """Sonda a01 de la r02 (mata S01): el error corriente llega con el sello de F2 roto; para el ciclo y no aparta nada."""
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    _construir_que_lanza(monkeypatch, q, error, romper=True)
    with pytest.raises(type(error)):
        b.ciclo(D2)
    assert not _marcas(b, q) and not _apartadas(b, q)
    assert not all(b.almacen.verificar_integridad().values())


def test_cierre_h01_si_la_incidencia_del_apartado_falla_no_queda_apartada_en_silencio(tmp_path, universo, monkeypatch):
    """Sonda a07 de la r02: la incidencia del apartado falla una vez; la pendiente no queda marcada sin escalar."""
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    _construir_que_lanza(monkeypatch, q, KeyError("clases"))
    real = b.almacen.incidencia
    caer = {"si": True}

    def incidencia(tipo, detalle, *a, **k):
        if caer["si"] and "apartada" in detalle:
            raise OSError("disco lleno simulado")
        return real(tipo, detalle, *a, **k)

    monkeypatch.setattr(b.almacen, "incidencia", incidencia)
    with pytest.raises(OSError):
        b.ciclo(D2)
    assert not _marcas(b, q) and q in [x for x, _ in respuesta_final.pendientes(b.almacen)]
    caer["si"] = False
    b.ciclo(D3)                                     # el disco ya responde: se reintenta, se escala y se aparta una vez
    assert len(_marcas(b, q)) == 1 and len(_apartadas(b, q)) == 1
    assert "revisar antes de reenviar" in _apartadas(b, q)[0]["detalle"]


def test_cierre_h01_contadores_rotos_no_apartan_en_silencio(tmp_path, universo, monkeypatch):
    """Sonda b01 de la r02, sin simular nada: `contadores.json` ilegible hace fallar el MSG- y el INC-; se repara y otro ciclo."""
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    ruta = b.almacen._ruta_contadores
    bueno = ruta.read_text(encoding="utf-8")
    ruta.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError):
        b.ciclo(D2)
    assert not _marcas(b, q) and not _apartadas(b, q)
    ruta.write_text(bueno, encoding="utf-8")
    b.ciclo(D3)
    assert bool(_marcas(b, q)) == bool(_apartadas(b, q))
