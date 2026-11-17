"""QA r03 de T-166 · los dos extremos de la frase corregida de H-07 que r02_01 no mide: «también si la rechazan su esquema» (se
aparta) y «salvo un fallo de integridad» (un rechazo R8 con el almacén no íntegro para y no se aparta).

Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-166/revisores/r03_01_pendientes_esquema_e_integridad.py
"""
import sys
from pathlib import Path

import pytest

EJ = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
sys.path[:0] = [str(EJ), str(EJ / "tests"), str(Path(__file__).resolve().parent)]
from r02_01_pendientes_y_errores_de_control import DESPUES, DIV, _falla_la_final_con, _pendiente, universo  # noqa: E402,F401
from bloque_a.contratos import DatosSensibles  # noqa: E402
from bloque_a import respuesta_final as rf  # noqa: E402


def test_un_rechazo_del_esquema_se_aparta(tmp_path, universo, monkeypatch):
    b, qry = _pendiente(tmp_path, universo, monkeypatch)
    real = rf.validar

    def validar(cuerpo, estado):
        if b.almacen.estado("F5").get(qry, {}).get("respuesta_final") is None and cuerpo["respuesta_final"]["provisional_msg_id"] == \
                b.almacen.estado("F5")[qry]["provisional_msg_id"]:
            raise rf.RespuestaFinalInvalida("esquema")
        return real(cuerpo, estado)
    monkeypatch.setattr(rf, "validar", validar)
    b.consulta(DIV, as_of=DESPUES, ejecutar_escalado=False)
    assert b.almacen.estado("F5")[qry]["final_no_enviable"] == {"error": "RespuestaFinalInvalida"}


def test_un_rechazo_r8_con_el_almacen_no_integro_para_y_no_se_aparta(tmp_path, universo, monkeypatch):
    b, qry = _pendiente(tmp_path, universo, monkeypatch)
    _falla_la_final_con(b, monkeypatch, DatosSensibles("x"), qry)
    monkeypatch.setattr(b.almacen, "verificar_integridad", lambda: {"F5": False})
    with pytest.raises(DatosSensibles):
        b.consulta(DIV, as_of=DESPUES, ejecutar_escalado=False)
    assert not b.almacen.estado("F5")[qry].get("final_no_enviable")
