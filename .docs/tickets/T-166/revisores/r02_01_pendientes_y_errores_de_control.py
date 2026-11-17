"""QA r02 de T-166 · la frase corregida de las finales pendientes («si no se puede enviar, se aparta una vez …, salvo un fallo
de integridad o un error de control, que para la consulta o el ciclo»), medida con el ejecutor (mock).

Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-166/revisores/r02_01_pendientes_y_errores_de_control.py
Dos de los errores de `ERRORES_DE_CONTROL` (DatosSensibles y MensajeInvalido, `RECHAZOS_SIN_EFECTO`) no paran: se apartan.
"""
import sys
from pathlib import Path

import pytest

EJ = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
sys.path[:0] = [str(EJ), str(EJ / "tests")]
from conftest import AS_OF, nuevo_bloque, cargar_universo, RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.contratos import CanalNoPrevisto, DatosSensibles, MensajeInvalido  # noqa: E402
from bloque_a.herramientas.ht01_datos import FugaDeInformacion  # noqa: E402
from bloque_a import respuesta_final as rf  # noqa: E402

DIV = "Analiza qué conviene hacer ahora"
DESPUES = "2026-06-12"


@pytest.fixture(scope="session")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def _pendiente(tmp, universo, monkeypatch):
    b = nuevo_bloque(tmp, universo, cfg=cargar_config(extra={"modo": "backtest"}))
    real = rf.enviar
    monkeypatch.setattr(rf, "enviar", lambda *a, **k: None)
    q = b.consulta(DIV, as_of=AS_OF, ejecutar_escalado=False)
    monkeypatch.setattr(rf, "enviar", real)
    assert [x for x, _ in rf.pendientes(b.almacen)] == [q["query_id"]]
    return b, q["query_id"]


def _falla_la_final_con(b, monkeypatch, error, qry):
    crear = b.mensajeria.crear

    def crear_o_fallar(contrato, emisor, receptor, cuerpo, **k):
        if contrato == "CT-03" and "respuesta_final" in cuerpo and k.get("query_id") == qry:   # solo la pendiente
            raise error
        return crear(contrato, emisor, receptor, cuerpo, **k)
    monkeypatch.setattr(b.mensajeria, "crear", crear_o_fallar)


@pytest.mark.parametrize("error", [DatosSensibles("x"), MensajeInvalido("x")], ids=lambda e: type(e).__name__)
def test_hallazgo_rechazos_de_la_mensajeria_son_de_control_y_no_paran_se_apartan(tmp_path, universo, monkeypatch, error):
    assert isinstance(error, rf.ERRORES_DE_CONTROL)                 # son «errores de control» según la propia frase
    b, qry = _pendiente(tmp_path, universo, monkeypatch)
    _falla_la_final_con(b, monkeypatch, error, qry)
    b.consulta(DIV, as_of=DESPUES, ejecutar_escalado=False)          # no para: la consulta siguiente sigue
    f5 = b.almacen.estado("F5")[qry]
    assert f5.get("final_no_enviable") == {"error": type(error).__name__} and not f5.get("respuesta_final")
    assert any(e.get("escalado_operador") and qry in str(e.get("descripcion", e)) for e in b.almacen.leer("HA"))


@pytest.mark.parametrize("error", [CanalNoPrevisto("x"), FugaDeInformacion("x")], ids=lambda e: type(e).__name__)
def test_los_demas_errores_de_control_si_paran(tmp_path, universo, monkeypatch, error):
    b, qry = _pendiente(tmp_path, universo, monkeypatch)
    _falla_la_final_con(b, monkeypatch, error, qry)
    with pytest.raises(type(error)):
        b.consulta(DIV, as_of=DESPUES, ejecutar_escalado=False)
    assert not b.almacen.estado("F5")[qry].get("final_no_enviable")


def test_otro_error_se_aparta(tmp_path, universo, monkeypatch):
    b, qry = _pendiente(tmp_path, universo, monkeypatch)
    _falla_la_final_con(b, monkeypatch, KeyError("x"), qry)
    b.consulta(DIV, as_of=DESPUES, ejecutar_escalado=False)
    assert b.almacen.estado("F5")[qry]["final_no_enviable"] == {"error": "KeyError"}


def test_mensaje_invalido_no_deja_incidencia_propia_de_la_mensajeria(tmp_path, universo, monkeypatch):
    """«un rechazo de la mensajería deja su incidencia en HA»: cierto para R8 y canal; MensajeInvalido no escribe ninguna
    (`Mensajeria.validar`). Para la final no es alcanzable: su cuerpo pasa antes `ESQUEMA` (sin campos reservados)."""
    b = nuevo_bloque(tmp_path, universo, cfg=cargar_config(extra={"modo": "backtest"}))
    antes = len(b.almacen.leer("HA"))
    with pytest.raises(MensajeInvalido):
        b.mensajeria.crear("CT-03", "AG-01", "BROKER", {"clase_consulta": "DATO"}, query_id="QRY-2026-0099", tipo_mensaje="RETORNO")
    assert len(b.almacen.leer("HA")) == antes
