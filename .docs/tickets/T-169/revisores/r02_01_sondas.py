"""QA r02 de T-169 (revisor) · sondas de `enviar_pendientes` tras la r02: qué para (falla cerrado), qué se aparta y cuántas
incidencias deja.

Uso, desde `bloque_a/11_Ejecutor` de la copia de trabajo:
  ../../.venv/bin/python -m pytest -q -p no:cacheprovider -rxX ../../.docs/tickets/T-169/revisores/r02_01_sondas.py
Todo con el cliente simulado, sin red ni coste. Las que documentan un hallazgo llevan `xfail(strict=True)` con su ID.
"""
import copy
import json
import sys
from pathlib import Path

import pytest

EJECUTOR = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJECUTOR / "tests"))
sys.path.insert(0, str(EJECUTOR))

from bloque_a import respuesta_final
from bloque_a.almacen import EscrituraFueraDeReserva
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config
from bloque_a.contratos import CanalNoPrevisto, MensajeInvalido
from bloque_a.herramientas.ht01_datos import FugaDeInformacion, cargar_universo
from bloque_a.llm import ReplayFaltante
from conftest import AS_OF, nuevo_bloque

ORO = "¿Qué opinas del oro frente a la plata a 6 meses?"
DIV = "Analiza qué conviene hacer ahora"
CORREO = "marta.ruiz.qa169r02@ejemplo.com"
D2, D3 = "2026-06-12", "2026-06-19"


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


def _finales(ms, q=None):
    return [m for m in ms if m["contrato"] == "CT-03" and m["tipo_mensaje"] == "RETORNO" and m.get("respuesta_final")
            and (q is None or m["query_id"] == q)]


def _pendiente(monkeypatch, b, fecha=AS_OF):
    real = respuesta_final.enviar
    monkeypatch.setattr(respuesta_final, "enviar", lambda *a, **k: None)
    q = b.consulta(ORO, as_of=fecha, ejecutar_escalado=False)["query_id"]
    monkeypatch.setattr(respuesta_final, "enviar", real)
    assert q in [x for x, _ in respuesta_final.pendientes(b.almacen)]
    return q


def _marcas(b, q):
    return [e for e in b.almacen.leer("F5") if e.get("id") == q and e.get("final_no_enviable")]


def _apartadas(b, q):
    return [e for e in b.almacen.leer("HA") if q in e.get("detalle", "") and "apartada" in e.get("detalle", "")]


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


# ------------------------------------------------------------------ falla cerrado: lo que no se aparta
@pytest.mark.parametrize("error", [KeyError("clases"), RuntimeError("x"), OSError("disco")], ids=lambda e: type(e).__name__)
def test_a01_un_error_corriente_con_el_almacen_roto_para_y_no_aparta(tmp_path, universo, monkeypatch, error):
    """Mata el mutante S01 (en `enviar_pendientes`, solo `isinstance(e, ERRORES_DE_CONTROL)`, sin mirar la integridad)."""
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    _construir_que_lanza(monkeypatch, q, error, romper=True)
    with pytest.raises(type(error)):
        b.ciclo(D2)
    assert not _marcas(b, q) and not _apartadas(b, q)
    assert not all(b.almacen.verificar_integridad().values())


@pytest.mark.parametrize("error", [FugaDeInformacion("x"), ReplayFaltante("AG-02"), EscrituraFueraDeReserva("x"),
                                   CanalNoPrevisto("x")], ids=lambda e: type(e).__name__)
def test_a02_un_error_de_control_en_una_pendiente_para_cada_vez_y_no_aparta(tmp_path, universo, monkeypatch, error):
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    _construir_que_lanza(monkeypatch, q, error)
    for fecha in (D2, D3):
        with pytest.raises(type(error)):
            b.ciclo(fecha)
    with pytest.raises(type(error)):
        b.consulta(DIV, as_of=D3, ejecutar_escalado=False)
    assert not _marcas(b, q) and not _apartadas(b, q)
    assert respuesta_final.pendientes(b.almacen) == [(q, AS_OF)]


def test_a03_el_sello_ilegible_para(tmp_path, universo, monkeypatch):
    """El fichero de sellos corrupto (no JSON) durante el envío: no se aparta nada en silencio."""
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    real = respuesta_final.construir

    def construir(almacen, qry, *a, **k):
        almacen._ruta_sellos.write_text("{no es json", encoding="utf-8")
        return real(almacen, qry, *a, **k)

    monkeypatch.setattr(respuesta_final, "construir", construir)
    with pytest.raises(Exception):
        respuesta_final.enviar_pendientes(b, D2)
    assert not any(e.get("final_no_enviable") for e in b.almacen._entradas["F5"])


def test_a04_mensaje_invalido_de_la_mensajeria_se_aparta_una_vez(tmp_path, universo, monkeypatch):
    """Por diseño (RECHAZOS_SIN_EFECTO): un MensajeInvalido al crear la final, con el almacén íntegro, se aparta. Una marca."""
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    crear = b.mensajeria.crear

    def f(contrato, *a, **k):
        if contrato == "CT-03" and k.get("query_id") == q and k.get("tipo_mensaje") == "RETORNO":
            raise MensajeInvalido("x")
        return crear(contrato, *a, **k)

    b.mensajeria.crear = f
    b.ciclo(D2)
    b.ciclo(D3)
    assert [m["final_no_enviable"] for m in _marcas(b, q)] == [{"error": "MensajeInvalido"}] and len(_apartadas(b, q)) == 1


# ------------------------------------------------------------------ incidencias duplicadas
def test_a05_consulta_escalada_con_una_pendiente_rechazada_una_marca_y_una_incidencia(tmp_path, universo, monkeypatch):
    """`consulta` llama a `enviar_pendientes` y su `ciclo` escalado otra vez: una sola marca, una sola incidencia «apartada»
    y, del R8, una sola SEGURIDAD."""
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q, "fallo_analisis": f"Error de {CORREO}"})
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q,
                                       "escalado": {**b.almacen.estado("F5", clave="id")[q]["escalado"], "estado_run": "FALLIDO"}})
    seg0 = len([e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"])
    ms = _espiar(b)
    r = b.consulta(DIV, as_of=D2)
    assert r["respuesta_final"] and r["respuesta_final"]["repetido"] is False
    assert len(_marcas(b, q)) == 1 and len(_apartadas(b, q)) == 1 and not _finales(ms, q)
    assert len([e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"]) - seg0 == 1
    assert CORREO not in json.dumps(b.almacen.leer("HA"), ensure_ascii=False)


def test_a06_una_apartada_no_vuelve_y_el_operador_la_reenvia_una_vez(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    _construir_que_lanza(monkeypatch, q, KeyError("clases"))
    b.ciclo(D2)
    monkeypatch.undo()
    ms = _espiar(b)
    b.ciclo(D3)
    assert not _finales(ms, q)
    f1 = respuesta_final.enviar(b, q, None, AS_OF)
    f2 = respuesta_final.enviar(b, q, None, AS_OF)
    assert f1["repetido"] is False and f2["repetido"] is True and len(_finales(ms, q)) == 1
    assert len(_marcas(b, q)) == 1 and len(_apartadas(b, q)) == 1


# ------------------------------------------------------------------ fallo a mitad del apartado
@pytest.mark.xfail(strict=True, reason="H-01 de la r02 (baja): si falla la incidencia, la pendiente queda apartada sin escalar")
def test_a07_si_la_incidencia_del_apartado_falla_no_queda_apartada_en_silencio(tmp_path, universo, monkeypatch):
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
    caer["si"] = False
    b.ciclo(D3)                                     # el disco ya responde
    # Esperado: o la pendiente sigue pendiente (se reintenta y se escala), o está apartada y escalada. Nunca apartada sin escalar
    marcada, escalada = bool(_marcas(b, q)), bool(_apartadas(b, q))
    print("A07 marcada", marcada, "escalada", escalada, "pendientes", respuesta_final.pendientes(b.almacen))
    assert marcada == escalada


# ------------------------------------------------------------------ nota: fallo tras crear el mensaje
def test_a08_nota_fallo_de_f5_tras_crear_la_final(tmp_path, universo, monkeypatch):
    """Nota (preexistente en T-162, no de la r02): la final se crea y F5 no la guarda (OSError). Se anota lo que pasa."""
    b = _bloque(tmp_path, universo)
    q = _pendiente(monkeypatch, b)
    ms = _espiar(b)
    real = b.almacen.escribir
    veces = {"n": 0}

    def escribir(archivo, autor, entrada):
        if archivo == "F5" and entrada.get("respuesta_final") and veces["n"] == 0:
            veces["n"] += 1
            raise OSError("disco")
        return real(archivo, autor, entrada)

    monkeypatch.setattr(b.almacen, "escribir", escribir)
    respuesta_final.enviar_pendientes(b, D2)
    print("A08 finales creadas", len(_finales(ms, q)), "marcas", len(_marcas(b, q)), "apartadas", len(_apartadas(b, q)))
