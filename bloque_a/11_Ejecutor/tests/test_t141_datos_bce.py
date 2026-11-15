"""T-141 · Datos reales de divisas del BCE: los cruces del universo a partir de los tipos de referencia «unidades por euro».
Sin red: los tipos de entrada son inventados para la prueba."""
import importlib.util
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo

SCRIPTS = Path(__file__).resolve().parents[3] / ".docs" / "scripts"


def _modulo(nombre):
    spec = importlib.util.spec_from_file_location(nombre, SCRIPTS / f"{nombre}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def bce():
    return _modulo("descargar_datos_bce")


def _ancho():
    fechas = pd.to_datetime(["2026-11-12", "2026-11-13"])
    return pd.DataFrame({"USD": [1.10, 1.20], "JPY": [165.0, 180.0], "GBP": [0.85, 0.80], "AUD": [1.65, 1.60],
                         "CHF": [0.95, 0.96], "MXN": [20.0, 21.6]}, index=fechas)


def test_los_seis_cruces_del_universo(bce):
    divisas = set(cargar_universo(RUTA_UNIVERSO_EJEMPLO).query("clase == 'DIV'")["simbolo"])
    assert set(bce.CRUCES) == divisas


def test_cada_cruce_sale_de_los_tipos_por_euro(bce):
    s = {k: v.set_index("fecha")["cierre"] for k, v in bce.cruces(_ancho()).items()}
    d = "2026-11-13"
    assert s["EURUSD=X"][d] == pytest.approx(1.20)
    assert s["USDJPY=X"][d] == pytest.approx(180.0 / 1.20)
    assert s["GBPUSD=X"][d] == pytest.approx(1.20 / 0.80)
    assert s["AUDUSD=X"][d] == pytest.approx(1.20 / 1.60)
    assert s["USDCHF=X"][d] == pytest.approx(0.96 / 1.20)
    assert s["USDMXN=X"][d] == pytest.approx(21.6 / 1.20)


def test_faltan_datos_o_no_positivos_se_quitan(bce):
    a = _ancho()
    a.loc["2026-11-12", "JPY"] = float("nan")
    a.loc["2026-11-13", "GBP"] = 0.0
    s = bce.cruces(a)
    assert list(s["USDJPY=X"]["fecha"]) == ["2026-11-13"]
    assert list(s["GBPUSD=X"]["fecha"]) == ["2026-11-12"]   # 1,2 / 0 es infinito: no es un cierre positivo y finito


def test_el_csv_lo_lee_ht01(bce, tmp_path):
    for simbolo, df in bce.cruces(_ancho()).items():
        df.to_csv(tmp_path / f"{simbolo}.csv", index=False)
    p = ProveedorCSV(tmp_path)
    p.fijar_as_of("2026-11-13")
    assert p.cierres("EURUSD=X").iloc[-1] == pytest.approx(1.20)
