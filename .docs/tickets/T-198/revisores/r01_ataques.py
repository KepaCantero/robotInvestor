"""QA r01 de T-198 (revisor independiente): ataques al CT-19 atendido por el Buscador.
Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-198/revisores/r01_ataques.py
Cada prueba afirma lo que DEBERÍA pasar: una prueba en rojo es un hallazgo (ver qa.md)."""
import copy
import sys
from pathlib import Path

EJ = Path.cwd()
sys.path.insert(0, str(EJ / "tests"))

import pytest  # noqa: E402
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


def _inc(b):
    return [e for e in b.almacen.leer("HA") if "no atendido por el Buscador" in str(e.get("detalle"))]


# ---- H-01: una FUE- que ya no se puede atender (su fuente salió de F9: baja R19, versión nueva de F9) bloquea para siempre
# todas las demás, y deja una incidencia en cada ciclo
def test_r01_una_fue_envenenada_no_bloquea_a_las_demas(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 20, 5)
    _sembrar(b, FUENTE_B, 13, 12, inicio_id=101)
    fues = {f["ref_id"]: f for f in b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")}
    assert set(fues) == {FUENTE_A, FUENTE_B}
    original = b.referencias.por_id
    monkeypatch.setattr(b.referencias, "por_id", lambda r: None if r == FUENTE_B else original(r))   # B dada de baja
    for i in range(3):
        b._comunicar_fiabilidad(b.reloj.fecha, f"RUN-2026-000{i + 2}")
    hechas = {e["ref_id"] for e in _f9(b)}
    print("F9:", hechas, "incidencias:", len(_inc(b)))
    assert FUENTE_A in hechas, "la FUE- buena de A nunca se atiende por culpa de la de B"
    assert len(_inc(b)) <= 1, "una incidencia por ciclo, para siempre"


# ---- H-03: el `timestamp` del mensaje no se comprueba y da la `fecha_ct19` que ve el Buscador
def test_r01_fecha_ct19_no_puede_ser_posterior_a_as_of(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 20, 5)
    fues = b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")
    msg = b.mensajeria.crear("CT-19", "AG-20", "AG-16", fiabilidad_f9.cuerpo_ct19(fues), run_id="RUN-2026-0001",
                             tipo_mensaje="RETORNO", estado="COMPLETO")
    for f in fues:
        b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "FUE", "id": f["fue_id"], "comunicado_ct19": msg["msg_id"]})
    malo = copy.deepcopy(msg)
    malo["timestamp"] = "2099-01-01T06:00:00+01:00"
    try:
        fiabilidad_f9.atender_ct19(b, malo, b.reloj.fecha, "RUN-2026-0001")
    except fiabilidad_f9.FiabilidadNoAtendible:
        return
    fechas = [e["fecha_ct19"] for e in _f9(b)]
    print("fecha_ct19:", fechas)
    assert all(f <= AS_OF for f in fechas), "fecha_ct19 posterior a as_of en F9"


# ---- Fallo a mitad: el almacén falla en la segunda escritura de F9. No hay rollback (la «transacción» es un cerrojo), pero
# el ciclo siguiente debe completar lo que falta sin duplicar
def test_r01_fallo_a_mitad_se_recupera_sin_duplicar(tmp_path, universo, monkeypatch):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 20, 5)
    _sembrar(b, FUENTE_B, 13, 12, inicio_id=101)
    b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")
    escribir, n = b.almacen.escribir, {"f9": 0}

    def roto(archivo, autor, entrada):
        if archivo == "F9":
            n["f9"] += 1
            if n["f9"] == 2:
                raise OSError("disco lleno")
        return escribir(archivo, autor, entrada)
    monkeypatch.setattr(b.almacen, "escribir", roto)
    with pytest.raises(OSError):
        b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0001")
    a_medias = len(_f9(b))
    monkeypatch.setattr(b.almacen, "escribir", escribir)
    b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0002")
    print("tras el fallo:", a_medias, "tras el reintento:", len(_f9(b)))
    assert sorted(e["ref_id"] for e in _f9(b)) == sorted([FUENTE_A, FUENTE_B])
    assert all(b.almacen.verificar_integridad().values())


# ---- Datos hostiles en las fuentes: tipos raros no deben pasar ni romper con algo que no sea FiabilidadNoAtendible
@pytest.mark.parametrize("fuentes", [[None], ["FUE"], [[]], [{"fue_id": None}], [{k: None for k in fiabilidad_f9.CAMPOS_CT19}],
                                     [{**{k: None for k in fiabilidad_f9.CAMPOS_CT19}, "fue_id": ["x"]}]])
def test_r01_fuentes_hostiles_fallan_cerrado(tmp_path, universo, fuentes):
    b = _bloque(tmp_path, universo)
    msg = {"contrato": "CT-19", "emisor": "AG-20", "receptor": "AG-16", "msg_id": "MSG-2026-000001", "tipo": "FIABILIDAD_FUENTES",
           "fuentes": fuentes}
    with pytest.raises(fiabilidad_f9.FiabilidadNoAtendible):
        fiabilidad_f9.atender_ct19(b, msg, b.reloj.fecha, "RUN-2026-0001")
    assert _f9(b) == []


# ---- El ciclo mock completo con FUE- dos veces seguidas: una entrada por FUE-, ninguna incidencia, almacén íntegro
def test_r01_dos_ciclos_seguidos(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    _sembrar(b, FUENTE_A, 20, 5)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert len(_f9(b)) == 1 and _inc(b) == []
    assert all(b.almacen.verificar_integridad().values())
