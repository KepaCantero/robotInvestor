"""QA r02 de T-169 (segundo revisor de la ronda) · sondas sin monkeypatch de la incidencia: estado real roto fuera de los
ficheros con sello, varias pendientes en la misma llamada y fallos que no son `Exception`.

Uso, desde `bloque_a/11_Ejecutor` de la copia de trabajo (reutiliza los auxiliares de `r02_01_sondas.py`):
  ../../.venv/bin/python -m pytest -q -p no:cacheprovider -rxX -s ../../.docs/tickets/T-169/revisores/r02_03_sondas.py
Todo con el cliente simulado, sin red ni coste. Las que documentan un hallazgo llevan `xfail(strict=True)` con su ID.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location("r02_01_sondas_aux", Path(__file__).with_name("r02_01_sondas.py"))
aux = importlib.util.module_from_spec(_spec)
sys.modules["r02_01_sondas_aux"] = aux
_spec.loader.exec_module(aux)
respuesta_final = aux.respuesta_final
universo = aux.universo
D2, D3 = aux.D2, aux.D3


@pytest.mark.xfail(strict=True, reason="H-01 de la r02 (baja): contadores.json roto → la pendiente queda apartada sin incidencia")
def test_b01_contadores_rotos_no_apartan_en_silencio(tmp_path, universo, monkeypatch):
    """Sin simular nada en la incidencia: `contadores.json` (sin sello, fuera de `verificar_integridad`) ilegible. `enviar` falla
    al pedir el MSG- (JSONDecodeError, «error corriente» con el almacén «íntegro») → `_apartar` escribe la marca y la incidencia
    falla al pedir el INC-. Se repara el fichero y se lanza otro ciclo."""
    b = aux._bloque(tmp_path, universo)
    q = aux._pendiente(monkeypatch, b)
    ruta = b.almacen._ruta_contadores
    bueno = ruta.read_text(encoding="utf-8")
    ruta.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError):
        b.ciclo(D2)
    print("B01 tras el fallo: marcas", len(aux._marcas(b, q)), "apartadas", len(aux._apartadas(b, q)),
          "pendientes", respuesta_final.pendientes(b.almacen))
    ruta.write_text(bueno, encoding="utf-8")
    b.ciclo(D3)
    marcada, escalada = bool(aux._marcas(b, q)), bool(aux._apartadas(b, q))
    print("B01 reparado: marcada", marcada, "escalada", escalada, "pendientes", respuesta_final.pendientes(b.almacen))
    assert marcada == escalada


def test_b02_dos_pendientes_una_con_error_corriente_la_otra_sale(tmp_path, universo, monkeypatch):
    b = aux._bloque(tmp_path, universo)
    q1 = aux._pendiente(monkeypatch, b)
    q2 = aux._pendiente(monkeypatch, b)
    aux._construir_que_lanza(monkeypatch, q1, RuntimeError("x"))
    ms = aux._espiar(b)
    out = respuesta_final.enviar_pendientes(b, D2)
    assert [m["query_id"] for m in aux._finales(ms)] == [q2] and len(out) == 1
    assert len(aux._marcas(b, q1)) == 1 and len(aux._apartadas(b, q1)) == 1
    for _ in range(2):
        assert respuesta_final.enviar_pendientes(b, D3) == []
    assert len(aux._marcas(b, q1)) == 1 and len(aux._apartadas(b, q1)) == 1 and not aux._marcas(b, q2)


def test_b03_una_interrupcion_no_se_aparta(tmp_path, universo, monkeypatch):
    b = aux._bloque(tmp_path, universo)
    q = aux._pendiente(monkeypatch, b)
    aux._construir_que_lanza(monkeypatch, q, KeyboardInterrupt())
    with pytest.raises(KeyboardInterrupt):
        respuesta_final.enviar_pendientes(b, D2)
    assert not aux._marcas(b, q) and not aux._apartadas(b, q)
    assert [x for x, _ in respuesta_final.pendientes(b.almacen)] == [q]


def test_b04_f5_manipulado_para_sin_apartar(tmp_path, universo, monkeypatch):
    """F5 editado a mano (quitar las clases del escalado de la pendiente): el sello lo detecta y nada se aparta."""
    b = aux._bloque(tmp_path, universo)
    q = aux._pendiente(monkeypatch, b)
    ruta = next(p for p in b.almacen.carpeta.iterdir() if p.name.startswith("F5"))
    texto = ruta.read_text(encoding="utf-8")
    assert '"clases"' in texto
    ruta.write_text(texto.replace('"clases"', '"clases_x"', 1), encoding="utf-8")
    with pytest.raises(ValueError):
        b.ciclo(D2)
    with pytest.raises(ValueError):
        b.ciclo(D3)
    ruta.write_text(texto, encoding="utf-8")
    assert not aux._marcas(b, q) and not aux._apartadas(b, q)
