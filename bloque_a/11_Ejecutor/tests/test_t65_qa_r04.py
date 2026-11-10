"""T-65 · Correcciones de la QA r04 de T-65 (`.docs/tickets/T-65/qa.md`, «Ronda r04»): H-24 y H-25.

Las pruebas fallan con el código de db6ed93 salvo los controles (ver `.docs/tickets/T-65/pruebas.md`).
"""
import shutil
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config
from bloque_a.herramientas.ht01_datos import (
    DatosInvalidos,
    ProveedorCSV,
    cargar_universo,
)
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
from conftest import DATOS, config_pruebas

EMISION, RESOLUCION_H1, VUELTA = "2026-04-17", "2026-04-24", "2026-04-27"


def _bloque(tmp_path, datos=DATOS):
    return Bloque(config_pruebas(), ProveedorCSV(datos), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(),
                  Path(tmp_path) / "estado", Path(tmp_path) / "ent")


def _parado(tmp_path, simbolo: str, desde: str) -> Path:
    datos = tmp_path / "datos"
    shutil.copytree(DATOS, datos)
    df = pd.read_csv(datos / f"{simbolo}.csv")
    df[df["fecha"] <= desde].to_csv(datos / f"{simbolo}.csv", index=False)
    return datos


def _prg(b, horizonte: str, resolucion: str, proxy="SPY", ref="ACWI", clase="RV") -> None:
    b.fijar_fecha(EMISION)
    b.almacen.escribir("F4", "AG-10", {
        "tipo_entrada": "ALTA", "prg_id": "PRG-2026-0901", "opp_id": "OPP-1", "clase": clase, "horizonte": horizonte,
        "estado": "ABIERTO", "prob_interna": 0.65, "sentido": "POSITIVO", "umbral": 0.0,
        "tipo_pronostico": "RELATIVO" if ref else "DIRECCIONAL", "referencia_indice": ref, "variable": {"serie_ht01": proxy},
        "fecha_emision": EMISION, "fecha_resolucion": resolucion, "nivel_referencia": {"valor": 1.0, "fecha": EMISION},
        "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True})


def _estado(b) -> str:
    return b.almacen.estado("F4")["PRG-2026-0901"]["estado"]


# ---------------------------------------------------------------- H-24 · H1: cada serie, con un dato posterior a la emisión
@pytest.mark.parametrize("parado", ["ACWI", "SPY"])
def test_r04_h24_h1_con_una_serie_parada_en_la_emision_no_se_resuelve(tmp_path, parado):
    b = _bloque(tmp_path, datos=_parado(tmp_path, parado, EMISION))      # deja de publicarse el mismo día de la emisión
    _prg(b, "H1", RESOLUCION_H1)
    b.fijar_fecha(VUELTA)
    b.evaluador.resolver(VUELTA, "RUN-2026-0001")
    assert _estado(b) == "ABIERTO"                                    # db6ed93: RESUELTO con una rentabilidad 0


def test_r04_h24_h1_una_serie_con_una_sola_sesion_nueva_no_basta(tmp_path):
    b = _bloque(tmp_path, datos=_parado(tmp_path, "ACWI", "2026-04-20"))  # 1 de las 5 sesiones del horizonte
    _prg(b, "H1", RESOLUCION_H1)
    b.fijar_fecha(VUELTA)
    b.evaluador.resolver(VUELTA, "RUN-2026-0001")
    assert _estado(b) == "ABIERTO"                                    # PS2 de H1: 1 sesión, no 4


def test_r04_h24_pasado_el_plazo_queda_no_resoluble(tmp_path):
    b = _bloque(tmp_path, datos=_parado(tmp_path, "ACWI", EMISION))
    _prg(b, "H1", RESOLUCION_H1)
    b.fijar_fecha("2026-06-05")
    b.evaluador.resolver("2026-06-05", "RUN-2026-0001")
    assert _estado(b) == "NO_RESOLUBLE"


def test_r04_h24_con_las_dos_series_al_dia_se_resuelve_y_guarda_cada_fecha(tmp_path):
    b = _bloque(tmp_path)
    _prg(b, "H1", RESOLUCION_H1)
    b.fijar_fecha(VUELTA)
    b.evaluador.resolver(VUELTA, "RUN-2026-0001")
    e = b.almacen.estado("F4")["PRG-2026-0901"]
    assert e["estado"] == "RESUELTO"
    res = e["resolucion"]
    assert res["fecha_dato_proxy"] == RESOLUCION_H1 and res["fecha_dato_referencia"] == RESOLUCION_H1   # db6ed93: no estaban


def test_r04_h24_la_tolerancia_es_la_de_ps2_del_horizonte(tmp_path):
    lim = cargar_config()["ps2_antiguedad_maxima_dias"]
    b = _bloque(tmp_path)
    ev = b.evaluador
    assert ev.motivo_no_fresca("2026-04-17", "2026-04-23", "2026-04-24", "H1") is None        # 1 sesión
    assert ev.motivo_no_fresca("2026-04-16", "2026-04-17", "2026-04-20", "H1") is None        # viernes → lunes: 1 sesión
    assert "sesiones" in ev.motivo_no_fresca("2026-04-17", "2026-04-22", "2026-04-24", "H1")  # 2 sesiones > 1
    assert ev.motivo_no_fresca("2026-04-03", "2026-04-28", "2026-05-01", "H2") is None        # 3 días = H2
    assert ev.motivo_no_fresca("2026-04-03", "2026-04-27", "2026-05-01", "H2")                # 4 días > 3
    assert ev.motivo_no_fresca("2026-01-02", "2026-05-01", "2026-05-31", "H4") is None        # 30 días = H4
    assert "posterior a la emisión" in ev.motivo_no_fresca("2026-04-17", "2026-04-17", "2026-04-17", "H1")
    assert lim["H1"] == 1 and lim["H2"] == 3 and lim["H4"] == 30


def test_r04_h24_en_la_cesta_no_cuenta_un_miembro_parado_en_la_emision(tmp_path):
    b0 = _bloque(tmp_path / "a")
    b0.fijar_fecha("2026-06-05")
    miembros = b0.evaluador.simbolos_clase("DIV")
    b = _bloque(tmp_path / "b", datos=_parado(tmp_path / "b", miembros[0], EMISION))
    b.fijar_fecha("2026-06-05")
    r_cesta, _ = b.evaluador.rentabilidad("CESTA", "DIV", EMISION, RESOLUCION_H1, "H1")
    otros = [b.evaluador.rentabilidad(s, "DIV", EMISION, RESOLUCION_H1, "H1")[0] for s in miembros[1:]]
    assert r_cesta == pytest.approx(sum(otros) / len(otros))         # db6ed93: entraba con 0
    r_sin_h, _ = b.evaluador.rentabilidad("CESTA", "DIV", EMISION, RESOLUCION_H1)
    assert r_sin_h == pytest.approx(r_cesta)                          # sin horizonte, tampoco (no tiene dato nuevo)


def test_r04_h24_ps2_de_la_emision_mira_tambien_la_referencia(tmp_path):
    b = _bloque(tmp_path, datos=_parado(tmp_path, "ACWI", "2026-04-14"))   # 3 días antes de la emisión
    b.fijar_fecha(EMISION)
    f = {"senales": {"fecha_dato": EMISION, "riesgo_1a5": 3}, "_referencia": "ACWI", "_tipo_pronostico": "RELATIVO",
         "_objeciones": [], "premortem": "x"}
    assert b._puertas(f, "N1", EMISION, ["H3"])["PS2"] is True        # H3: 7 días
    assert b._puertas(f, "N1", EMISION, ["H1"])["PS2"] is False       # db6ed93: True (solo miraba el proxy)
    assert b._puertas({**f, "_tipo_pronostico": "DIRECCIONAL"}, "N1", EMISION, ["H1"])["PS2"] is True


# ---------------------------------------------------------------- H-25 · solo cuentan las filas publicadas
def test_r04_h25_una_revision_aun_no_publicada_no_cuenta_como_fecha_repetida(tmp_path):
    (tmp_path / "X.csv").write_text("fecha,cierre,fecha_publicacion\n2026-05-28,100,\n2026-05-29,101,\n2026-05-29,99,2026-07-01\n",
                                    encoding="utf-8")
    p = ProveedorCSV(tmp_path)
    p.fijar_as_of("2026-06-05")
    assert list(p.cierres("X")) == [100.0, 101.0]                     # db6ed93: «fechas duplicadas … 2026-05-29»
    assert p.valor_en("X", "2026-05-29")[1] == 101.0
    p.fijar_as_of("2026-07-02")                                       # publicada la revisión: dos valores para el mismo día
    with pytest.raises(DatosInvalidos, match="fechas duplicadas"):
        p.cierres("X")
