"""QA de T-177 · verificación de la segunda ronda de cierre (H-18): urgencia, impacto y claves literales, y el mutante M08.

Ejecutar desde bloque_a/11_Ejecutor:
  python -m pytest -q -s -p no:cacheprovider ../../.docs/tickets/T-177/revisores/r03d_cierre2.py"""
import json
import sys
from pathlib import Path

import pytest

EJ = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJ / "tests"))
from conftest import AS_OF, config_pruebas, nuevo_bloque, universo  # noqa: E402,F401

from bloque_a.llm import solicitud_con_valor  # noqa: E402

SOL = {"servicio": "API de fondos cerrados", "motivo": "m", "impacto_si_falta": "i"}


@pytest.mark.parametrize("urg,sensible", [("ALTA", False), ("NORMAL", False), ("", False), (None, False), (False, False),
                                          ("alta", True), ("Alta", True), (" ALTA", True), ("ALTA ", True), ("MEDIA", True),
                                          (0, True), (" ", False), ([""], False), ({"": ""}, False)])
def test_r03d_urgencia(urg, sensible):
    """Mayúsculas y espacios: falla cerrado declarado (INC-T177-01). Sin contenido (" ", [""], {"": ""}): pasa."""
    assert solicitud_con_valor(json.dumps({"solicitudes_credenciales": [{**SOL, "urgencia": urg}]})) is sensible


@pytest.mark.parametrize("urg", [" ", [""], {"": ""}])
def test_r03d_HALLAZGO_H19_m08_no_es_equivalente(tmp_path, universo, urg):
    """Una urgencia sin contenido pasa la barrera y llega a `desde_retorno`, que la reduce a NORMAL. Con el mutante M08
    (`urgencia = s.get("urgencia") or "NORMAL"`) el CT-25 lleva " ", [""] o {"": ""}: M08 no es equivalente. Esta prueba es
    la que lo mata (con el código actual pasa)."""
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(credenciales={"servicios_bfa": []}))
    r = b.credenciales.desde_retorno({"solicitudes_credenciales": [{**SOL, "urgencia": urg}]}, "AG-16", AS_OF)
    crd = [c for c in b.almacen.estado("F5").values() if c.get("tipo_entrada") == "CRD"]
    assert r["solicitudes"][0]["resultado"] == "SOLICITADA" and [c["urgencia"] for c in crd] == ["NORMAL"]


@pytest.mark.parametrize("sol,sensible", [
    ({"servicio": "S", "motivo": "m", "impacto": "i"}, False),                       # impacto solo: se copia
    ({"servicio": "S", "motivo": "m", "impacto_si_falta": "", "impacto": "i"}, True),  # clave presente vacía: no se copia
    ({"servicio": "S", "motivo": "m", "impacto_si_falta": "i", "impacto": ""}, False),
    ({"Servicio": "S", "motivo": "m", "impacto_si_falta": "i"}, True),
    ({"servicio": "S", "motivo": "m", "impacto_si_falta": "i", "urgencia": "ALTA", "nota": None}, False),
])
def test_r03d_literales_e_impacto(sol, sensible):
    assert solicitud_con_valor(json.dumps({"solicitudes_credenciales": [sol]})) is sensible
