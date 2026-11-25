import json
from pathlib import Path

import jsonschema
import pytest
from bloque_a.almacen import EscrituraFueraDeReserva
from bloque_a.contratos import DatosSensibles
from conftest import AS_OF, nuevo_bloque

from bloque_a import sintesis


@pytest.mark.parametrize(("fallo", "fase"), [(1, "F6"), (2, "F7")])
def test_ciclo_bloqueado_y_registrado(tmp_path, universo, monkeypatch, fallo, fase):
    b = nuevo_bloque(tmp_path, universo)
    original = sintesis.ht09.validar
    n = 0

    def control(*args):
        nonlocal n
        n += 1
        if n == fallo:
            raise OSError("Verificador no disponible")
        return original(*args)

    mensajes = []
    crear = b.mensajeria.crear

    def registrar(*args, **kwargs):
        mensaje = crear(*args, **kwargs)
        if mensaje["contrato"] == "CT-14":
            mensajes.append(mensaje)
        return mensaje

    monkeypatch.setattr(b.mensajeria, "crear", registrar)
    monkeypatch.setattr(sintesis.ht09, "validar", control)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["estado"] == "PARCIAL" and r["entrega"] == "BLOQUEADA"
    run = b.almacen.estado("F5")[r["run_id"]]
    assert run["entrega"] == "BLOQUEADA" and r["g3"]["modo"] == "G3_MANUAL"
    inc, = [e for e in b.almacen.leer("HA") if e.get("tipo") == "HERRAMIENTA" and e.get("fase") == fase]
    assert inc["detalle"] in run["limitaciones"]
    mensaje, = [m for m in mensajes if m["msg_id"] == inc["msg_id"]]
    assert (mensaje["contrato"], mensaje["emisor"], mensaje["receptor"]) == ("CT-14", "AG-02", "AG-18")
    esquema = json.loads((Path(__file__).parent / "goldens/anexo_b_esquemas.json").read_text())
    jsonschema.validate(mensaje, esquema["CT-14.ENCARGO"])
    paquete = mensaje["paquete_sintesis"]
    assert paquete["resultado_ht09"] == {"fase": fase, "dictamen": "NO_DISPONIBLE"}
    assert paquete["run_id"] == r["run_id"] and paquete["clases"] == r["paquete"]["clases"]
    manual, = [e for e in b.almacen.leer("HA") if e.get("tipo_control") == "G3_MANUAL"]
    assert manual["fase"] == fase and manual["dictamen_efectivo"] == "BLOQUEADO"
    assert manual["dictamen_ht09"] == "NO_DISPONIBLE" and not b.almacen.leer("F4")


@pytest.mark.parametrize("error", [DatosSensibles, EscrituraFueraDeReserva, KeyError, TypeError, RuntimeError])
def test_control_o_programacion_para_el_ciclo(tmp_path, universo, monkeypatch, error):
    b = nuevo_bloque(tmp_path, universo)

    def falla(*args):
        raise error("prueba")

    monkeypatch.setattr(sintesis.ht09, "validar", falla)
    with pytest.raises(error, match="prueba"):
        b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert not any(e.get("tipo") == "HERRAMIENTA" for e in b.almacen.leer("HA"))
    assert not any(m["contrato"] == "CT-14" for m in b.mensajeria.registro)


def test_integridad_prevalece_sobre_indisponibilidad(tmp_path, universo, monkeypatch):
    b = nuevo_bloque(tmp_path, universo)

    def falla(*args):
        monkeypatch.setattr(b.almacen, "verificar_integridad", lambda: {"F2": False})
        raise OSError("herramienta sin conexión")

    monkeypatch.setattr(sintesis.ht09, "validar", falla)
    with pytest.raises(ValueError, match="integridad"):
        b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert not any(e.get("tipo") == "HERRAMIENTA" for e in b.almacen.leer("HA"))
    assert not any(m["contrato"] == "CT-14" for m in b.mensajeria.registro)


def test_pb52_caida_combinada(tmp_path, universo, monkeypatch):
    b = nuevo_bloque(tmp_path, universo)
    original = b.senales_clase

    def senales(clase, *args):
        if clase == "RF":
            raise OSError("HT-01 sin datos para RF")
        return original(clase, *args)

    def caida(*args):
        raise ImportError("Componente de HT-09 no disponible")

    monkeypatch.setattr(b, "senales_clase", senales)
    monkeypatch.setattr(sintesis.ht09, "validar", caida)
    r = b.ciclo(AS_OF, alcance={"clases": ["RF", "RV"]})
    assert not r["paquete"]["clases"]["RF"]["opciones"]
    assert "HT-01 sin datos para RF" in str(r["paquete"]["limitaciones"])
    assert r["entrega"] == "BLOQUEADA" and not r["entregables"]
    assert not any(str(e.get("dictamen_efectivo")).startswith("APTO") for e in b.almacen.leer("HA"))
    assert not b.almacen.leer("F4")
