"""T-165 QA r02 · de extremo a extremo con el cliente simulado (sin red ni gasto), con familias NUEVAS de r02_01: ¿llega a la
entrega una madurez falsa con G3 APTO?, ¿retira opciones o bloquea el run una frase legítima?

Reutiliza los ayudantes de r01_02 (siembra en el informe de clase del Analista simulado). Además corrige el caso
`guion_no_separable` de r01_02, al que le faltaba la marca (fallaba por el script, no por el código).

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r02_02_extremo_a_extremo.py -rf
"""
import importlib.util
import json
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location("r01_02", Path(__file__).with_name("r01_02_extremo_a_extremo.py"))
r01 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r01)
AS_OF, nuevo_bloque, mock_respuestas = r01.AS_OF, r01.nuevo_bloque, r01.mock_respuestas
universo = r01.universo   # fixture


def _ciclo(tmp_path, universo, marca, clases=("RV",)):
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": list(clases)})
    res, entregados = r01._resultado(b, r, palabra=marca)
    js = entregados.get("paquete_json", "")
    res["estado_g3_json"] = json.loads(js).get("estado_g3") if js else None
    print("  estado_g3 del JSON entregado:", res["estado_g3_json"])
    return res


SIEMBRAS = {
    # r01_02 «guion_no_separable», con su marca
    "r01_guion_no_separable": ("valoracion", lambda x: x + " ST‑DESC‑001 está validado en backtest.", "validado en backtest"),
    "N1_indicador_de_tendencia": ("valoracion", lambda x: x + " ST-DESC-001 es un indicador de tendencia validado en backtest.",
                                  "tendencia validado"),
    "N2_dos_puntos_no": ("valoracion", lambda x: x + " ST-DESC-001 está validado: no hay dudas.", "validado: no hay dudas"),
    "N3_con_exito_la_validacion": ("valoracion", lambda x: x + " ST-DESC-001 completó con éxito la validación fuera de muestra.",
                                   "con éxito la validación"),
    "N4_guion_bajo": ("valoracion", lambda x: x + " ST_DESC_001 está validado en backtest.", "st_desc_001 está validado"),
    # J3 · la ficha en la valoración y la afirmación en otro campo del mismo informe (el mecanismo)
    "J3_otro_campo": ("mecanismo", lambda x: x + " Es un método validado en backtest.", "método validado en backtest"),
}


@pytest.mark.parametrize("caso", sorted(SIEMBRAS))
def test_escapa_catalogo_real(caso, tmp_path, universo, monkeypatch):
    campo, cambio, marca = SIEMBRAS[caso]
    r01._sembrar(monkeypatch, campo, cambio)
    res = _ciclo(tmp_path, universo, marca)
    assert not r01._entregada_con(res), f"{caso}: entregado con «{marca}» y G3 {res['g3']}, estado_g3 {res['estado_g3_json']}"


def test_escapa_pb47_otra_cosa_rechazada(tmp_path, universo, monkeypatch):
    """ML-CLUS-001 en DOCUMENTADO (no se sirve), nombrado como en uso; «rechazada» se dice de otra cosa en la misma unidad."""
    r01._documentado(monkeypatch)
    r01._sembrar(monkeypatch, "mecanismo", lambda x: f"{x} Los clústeres salen de ML-CLUS-001; la alternativa fue rechazada.")
    res = _ciclo(tmp_path, universo, "salen de ml-clus-001")
    assert not r01._entregada_con(res), f"entregado con ML-CLUS-001 en uso y G3 {res['g3']}"


def _n_base(tmp_path, universo):
    b0 = nuevo_bloque(tmp_path / "base", universo)
    r0 = b0.ciclo(AS_OF, alcance={"clases": ["RV"]})
    return sum(len(d["opciones"]) for d in r0["paquete"]["clases"].values())


FP = {
    "S1_hemos_comprobado": ("valoracion", lambda x: "Hemos comprobado con ST-DESC-001 que el precio está en el "
                            + x.split("percentil ", 1)[1].split(" de sus", 1)[0] + " de su rango de tres años.", "hemos comprobado"),
    "D2_ninguna_validada": ("valoracion", lambda x: x + " ST-DESC-001 está implementado; ninguna ficha del Catálogo está validada.",
                            "ninguna ficha"),
}


@pytest.mark.parametrize("caso", sorted(FP))
def test_fp_retira_opciones(caso, tmp_path, universo, monkeypatch):
    n0 = _n_base(tmp_path, universo)
    campo, cambio, marca = FP[caso]
    r01._sembrar(monkeypatch, campo, cambio)
    res = _ciclo(tmp_path / "fp", universo, marca)
    print("  opciones sin la frase:", n0)
    assert res["opciones"] == n0 and all(x[2] == "OK" for x in res["g3"]), res


def test_fp_lectura_del_conjunto_comprobado(tmp_path, universo, monkeypatch):
    """El Analizador escribe en la lectura del conjunto (fuera de una opción) «comprobado con» una ficha servida."""
    original = mock_respuestas._integracion

    def integ(msg, ctx, rng):
        d = original(msg, ctx, rng)
        d["lectura_conjunto"] = "Hemos comprobado con RISK-DD-001 que las caídas máximas son contenidas en casi todas las opciones."
        return d
    monkeypatch.setattr(mock_respuestas, "_integracion", integ)
    res = _ciclo(tmp_path, universo, "hemos comprobado", clases=("RV", "RF"))
    assert not res["entrega_bloqueada"] and all(x[2] == "OK" for x in res["g3"]), res
