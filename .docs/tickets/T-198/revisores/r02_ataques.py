"""QA r02 de T-198 (revisor independiente): ataques a las correcciones de la r02.
Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-198/revisores/r02_ataques.py
Cada prueba afirma lo que DEBERÍA pasar: una prueba en rojo es un hallazgo (ver qa.md, ronda r02)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "tests"))

from conftest import AS_OF, config_pruebas, nuevo_bloque, universo  # noqa: E402,F401 — fixture de sesión
from test_t125_fiabilidad_fuentes import _sembrar  # noqa: E402

from bloque_a import fiabilidad_f9  # noqa: E402

FUENTE_A, FUENTE_B = "REF-RF-0001", "REF-RF-0003"


def _bloque(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas())
    b.fijar_fecha(AS_OF)
    return b


def _f9(b):
    return [e for e in b.almacen.leer("F9") if e.get("tipo_entrada") == "FIABILIDAD_MEDIDA"]


# ---- H-08: si F9 entero no se puede leer en un ciclo (ruta mal puesta, archivo ausente o vacío), apartar_no_atendibles marca
# TODAS las FUE- como no atendibles para siempre: un fallo pasajero se vuelve una pérdida permanente
def test_r02_f9_ilegible_un_ciclo_no_quema_las_fue(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 20, 5)
    _sembrar(b, FUENTE_B, 13, 12, inicio_id=101)
    b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")
    fichas = b.referencias.fichas
    monkeypatch.setattr(b.referencias, "fichas", {k: ([] if k == "F9" else v) for k, v in fichas.items()})   # F9 no se leyó
    b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0002")
    monkeypatch.setattr(b.referencias, "fichas", fichas)                                                      # vuelve
    b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0003")
    marcadas = fiabilidad_f9.no_atendibles(b.almacen)
    print("marcadas:", sorted(marcadas), "F9:", sorted(e["ref_id"] for e in _f9(b)))
    assert sorted(e["ref_id"] for e in _f9(b)) == [FUENTE_A, FUENTE_B], "un ciclo con F9 ilegible quema todas las FUE-"


# ---- La marca no se duplica con dos ciclos y la FUE- marcada no vuelve aunque se reenvíe a mano: atender_ct19 la sigue
# admitiendo si alguien la manda (el mensaje cuadra), y eso es coherente con «todo o nada para lo que llega de fuera»
def test_r02_la_marca_es_unica_en_varios_ciclos(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 20, 5)
    _sembrar(b, FUENTE_B, 13, 12, inicio_id=101)
    b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")
    original = b.referencias.por_id
    monkeypatch.setattr(b.referencias, "por_id", lambda r: None if r == FUENTE_B else original(r))
    for i in range(4):
        b._comunicar_fiabilidad(b.reloj.fecha, f"RUN-2026-000{i + 2}")
    marcas = [e for e in b.almacen.leer("HA") if e.get("fue_no_atendible")]
    assert len(marcas) == 1 and [e["ref_id"] for e in _f9(b)] == [FUENTE_A]
    assert all(b.almacen.verificar_integridad().values())


# ---- El timestamp que da el propio ciclo (Reloj.ahora, con zona) pasa la comprobación nueva con la configuración por defecto
def test_r02_el_timestamp_del_ciclo_pasa(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    ts = b.almacen.reloj.ahora()
    assert fiabilidad_f9._fecha_del_mensaje({"timestamp": ts}, AS_OF) == AS_OF
