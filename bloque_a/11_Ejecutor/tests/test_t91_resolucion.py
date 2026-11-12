"""T-91 · Hallazgos H-26 a H-29 de la QA r05 de T-65 (`.docs/tickets/T-65/qa.md`, «Ronda r05»): la resolución de los
pronósticos cuenta las sesiones de H1 con los festivos de PS2, mide proxy y referencia (y los miembros de la CESTA) hasta la
misma fecha, y congela un criterio que dice la regla. Los casos de H-29 fijan las tres partes de la corrección de H-24 que
sobrevivían a mutaciones."""
import pandas as pd
import pytest
from bloque_a.backtest import COLUMNAS_PRONOSTICOS, filas_pronosticos
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
from bloque_a.sintesis import CRITERIO_RESOLUCION, REGLA_FALLBACK
from conftest import DATOS, config_pruebas
from test_t65_qa_r04 import EMISION, _bloque, _estado, _parado, _prg

FESTIVOS = {"viernes_santo": True, "lunes_de_pascua": True, "fijos": ["01-01", "12-24", "12-25", "12-26", "12-31"]}


def _bloque_festivos(tmp_path, festivos):
    cfg = config_pruebas()
    cfg["ps2_festivos"] = festivos
    return Bloque(cfg, ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp_path / "estado", tmp_path / "ent")


# ---------------------------------------------------------------- H-26 · H1 con los festivos de PS2
@pytest.mark.parametrize(("emision", "ultimo", "resolucion"), [
    ("2025-12-19", "2025-12-23", "2025-12-26"),   # Navidad: Xetra cierra el 24, 25 y 26
    ("2026-03-30", "2026-04-02", "2026-04-06"),   # Pascua: Viernes Santo y lunes de Pascua
])
def test_h26_h1_cuenta_las_sesiones_sin_los_festivos_de_ps2(tmp_path, emision, ultimo, resolucion):
    ev = _bloque_festivos(tmp_path, FESTIVOS).evaluador
    assert ev.motivo_no_fresca(emision, ultimo, resolucion, "H1") is None   # 1 sesión; antes, 2 o 3


def test_h26_sin_festivos_el_cierre_cuenta_como_sesion(tmp_path):
    ev = _bloque_festivos(tmp_path, {"viernes_santo": False, "lunes_de_pascua": False, "fijos": []}).evaluador
    assert "sesiones" in ev.motivo_no_fresca("2025-12-19", "2025-12-23", "2025-12-26", "H1")


def test_h26_la_cesta_descarta_con_los_mismos_festivos(tmp_path):
    """`bases_cesta` mide la antigüedad al emitir con la misma regla que `motivo_no_fresca`."""
    b = _bloque_festivos(tmp_path, FESTIVOS)
    assert b.evaluador._edad_ps2("2025-12-23", "2025-12-29", "H1") == 1
    assert b.evaluador._edad_ps2("2025-12-23", "2025-12-29", "H2") == 6


# ---------------------------------------------------------------- H-27 · las dos series, hasta la misma fecha
def test_h27_proxy_y_referencia_se_miden_hasta_la_fecha_mas_antigua(tmp_path):
    ultimo_ref = "2026-04-29"
    resolucion = "2026-05-01"   # H2: 3 días de tolerancia; ACWI para 2 días antes
    datos = _parado(tmp_path, "ACWI", ultimo_ref)
    b = _bloque(tmp_path, datos=datos)
    _prg(b, "H2", resolucion)
    b.fijar_fecha("2026-05-04")
    b.evaluador.resolver("2026-05-04", "RUN-2026-0001")
    e = b.almacen.estado("F4")["PRG-2026-0901"]
    assert e["estado"] == "RESUELTO"
    r = e["resolucion"]
    assert r["fecha_dato_proxy"] == ultimo_ref and r["fecha_dato_referencia"] == ultimo_ref   # antes, SPY hasta el 1 de mayo
    spy = pd.read_csv(datos / "SPY.csv").set_index("fecha")["cierre"]
    assert r["rent_proxy"] == pytest.approx(spy[ultimo_ref] / 1.0 - 1, abs=1e-8)
    assert r["fecha_dato"] == ultimo_ref


def test_h27_la_cesta_mide_todos_sus_miembros_hasta_la_misma_fecha(tmp_path):
    b0 = _bloque(tmp_path / "a")
    b0.fijar_fecha("2026-06-05")
    miembros = b0.evaluador.simbolos_clase("DIV")
    ultimo = "2026-04-29"
    b = _bloque(tmp_path / "b", datos=_parado(tmp_path / "b", miembros[0], ultimo))
    b.fijar_fecha("2026-06-05")
    bases = b.evaluador.bases_cesta("DIV", EMISION, "H2")
    r, fecha = b.evaluador.rentabilidad("CESTA", "DIV", EMISION, "2026-05-01", "H2", base=bases)
    assert str(fecha.date()) == ultimo                                # H-29 (c): la más antigua, no la más reciente
    patas = [b.evaluador.rentabilidad(s, "DIV", EMISION, ultimo, base=x)[0] for s, x in sorted(bases.items())]
    assert r == pytest.approx(sum(patas) / len(patas))               # todos los miembros, hasta el 29


# ---------------------------------------------------------------- H-28 · criterio congelado y pronosticos.csv
def test_h28_el_criterio_congelado_dice_la_regla():
    c = CRITERIO_RESOLUCION.format(fin="2026-05-01", inicio="2026-04-17", suceso="x")
    assert "posterior a la emisión" in c and "PS2" in c and "la más antigua" in c and "festivos" in c
    assert "espera" in REGLA_FALLBACK.format(dias_nr=10) and "10 días hábiles" in REGLA_FALLBACK.format(dias_nr=10)


def test_h28_pronosticos_csv_lleva_la_fecha_de_cada_serie():
    assert COLUMNAS_PRONOSTICOS[-2:] == ["fecha_dato_proxy", "fecha_dato_referencia"]
    fila = filas_pronosticos({"P": {"prg_id": "P", "resolucion": {"fecha_dato_proxy": "2026-04-29", "fecha_dato_referencia": "2026-04-28"}}})[0]
    assert fila["fecha_dato_proxy"] == "2026-04-29" and fila["fecha_dato_referencia"] == "2026-04-28"


# ---------------------------------------------------------------- H-29 · lo que sobrevivía a mutaciones
def test_h29_a_ps2_con_la_referencia_sin_datos_no_pasa(tmp_path):
    datos = tmp_path / "datos"
    b0 = _parado(tmp_path, "ACWI", "1900-01-01")   # ACWI sin ninguna fila
    assert datos == b0
    b = _bloque(tmp_path, datos=datos)
    b.fijar_fecha(EMISION)
    f = {"senales": {"fecha_dato": EMISION, "riesgo_1a5": 3}, "_referencia": "ACWI", "_tipo_pronostico": "RELATIVO",
         "_objeciones": [], "premortem": "x"}
    assert b._puertas(f, "N1", EMISION, ["H3"])["PS2"] is False       # mutante: deja la fecha del proxy y pasa


def test_h29_b_la_resolucion_guarda_la_fecha_de_la_serie_mas_antigua(tmp_path):
    """Sin alinear (DIRECCIONAL), `fecha_dato` es la del proxy; RELATIVO, la común (ver H-27)."""
    b = _bloque(tmp_path, datos=_parado(tmp_path, "SPY", "2026-04-29"))
    _prg(b, "H2", "2026-05-01", ref=None)
    b.fijar_fecha("2026-05-04")
    b.evaluador.resolver("2026-05-04", "RUN-2026-0001")
    r = b.almacen.estado("F4")["PRG-2026-0901"]["resolucion"]
    assert _estado(b) == "RESUELTO" and r["fecha_dato"] == "2026-04-29" and r["fecha_dato_proxy"] == "2026-04-29"
    assert r["fecha_dato_referencia"] is None


# ================================================================================================== ronda r02 (QA r01 de T-91)
def _sin_dia(tmp_path, datos, simbolo: str, dia: str):
    df = pd.read_csv(datos / f"{simbolo}.csv")
    df[df["fecha"] != dia].to_csv(datos / f"{simbolo}.csv", index=False)


def test_r02_h01_con_un_hueco_antes_de_la_fecha_comun_espera(tmp_path):
    """La serie que queda con un dato más viejo que PS2 al medirla hasta la fecha común no resuelve: el PRG espera."""
    datos = _parado(tmp_path, "ACWI", "2026-04-29")
    df = pd.read_csv(datos / "SPY.csv")
    df[(df["fecha"] <= "2026-04-20") | (df["fecha"] > "2026-04-29")].to_csv(datos / "SPY.csv", index=False)
    b = _bloque(tmp_path, datos=datos)
    _prg(b, "H2", "2026-05-01")
    b.fijar_fecha("2026-05-04")
    b.evaluador.resolver("2026-05-04", "RUN-2026-0001")
    assert _estado(b) == "ABIERTO"                                    # 7feb697: RESUELTO con SPY del 20 de abril


def test_r02_h02_b_fecha_dato_es_la_mas_reciente_de_las_usadas(tmp_path):
    """Con un hueco de un día en la fecha común, el proxy se mide hasta el día anterior y la referencia hasta la fecha común:
    `fecha_dato` es la más reciente de las dos (mutante: solo la del proxy)."""
    datos = _parado(tmp_path, "ACWI", "2026-04-29")
    _sin_dia(tmp_path, datos, "SPY", "2026-04-29")
    b = _bloque(tmp_path, datos=datos)
    _prg(b, "H2", "2026-05-01")
    b.fijar_fecha("2026-05-04")
    b.evaluador.resolver("2026-05-04", "RUN-2026-0001")
    r = b.almacen.estado("F4")["PRG-2026-0901"]["resolucion"]
    assert _estado(b) == "RESUELTO"
    assert r["fecha_dato_proxy"] == "2026-04-28" and r["fecha_dato_referencia"] == "2026-04-29" and r["fecha_dato"] == "2026-04-29"


def test_r02_h02_c_la_cesta_devuelve_la_fecha_mas_antigua(tmp_path):
    b0 = _bloque(tmp_path / "a")
    b0.fijar_fecha("2026-06-05")
    m = b0.evaluador.simbolos_clase("DIV")
    datos = _parado(tmp_path / "b", m[0], "2026-04-29")
    _sin_dia(tmp_path, datos, m[1], "2026-04-29")
    b = _bloque(tmp_path / "b", datos=datos)
    b.fijar_fecha("2026-06-05")
    bases = b.evaluador.bases_cesta("DIV", EMISION, "H2")
    _, fecha = b.evaluador.rentabilidad("CESTA", "DIV", EMISION, "2026-05-01", "H2", base=bases)
    assert str(fecha.date()) == "2026-04-28"                          # mutante (max): 2026-04-29
