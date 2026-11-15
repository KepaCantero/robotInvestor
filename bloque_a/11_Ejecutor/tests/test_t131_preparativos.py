"""T-131 · Preparativos de decisiones del operador: comprobación de una carpeta de datos reales contra el universo
(`.docs/scripts/comprobar_datos_a.py`) y borrador de la corrección del Anexo B (`.docs/scripts/borrador_anexo_b.py`)."""
import importlib.util
import shutil
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import cargar_universo
from conftest import DATOS

SCRIPTS = Path(__file__).resolve().parents[3] / ".docs" / "scripts"


def _modulo(nombre):
    spec = importlib.util.spec_from_file_location(nombre, SCRIPTS / f"{nombre}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def comprobar():
    return _modulo("comprobar_datos_a").comprobar


def _carpeta(tmp_path, universo):
    d = tmp_path / "datos"
    d.mkdir()
    for s in universo["simbolo"]:
        shutil.copy(Path(DATOS) / f"{s}.csv", d / f"{s}.csv")
    return d


def test_los_datos_de_ejemplo_estan_completos(comprobar):
    u = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    filas = comprobar(DATOS, u, "2024-03-29")
    assert len(filas) == len(u) and all(f["estado"] == "OK" for f in filas)
    assert all(f["desde"] <= f["hasta"] <= "2024-03-29" and f["filas"] > 0 for f in filas)


def test_falta_invalido_y_antiguo(tmp_path, comprobar):
    u = cargar_universo(RUTA_UNIVERSO_EJEMPLO).head(4)
    d = _carpeta(tmp_path, u)
    s0, s1, s2, s3 = list(u["simbolo"])
    (d / f"{s0}.csv").unlink()                                              # falta
    (d / f"{s1}.csv").write_text("fecha,precio\n2024-01-02,1\n", encoding="utf-8")   # sin columna de cierre
    df = pd.read_csv(d / f"{s2}.csv")
    df[pd.to_datetime(df["fecha"]) <= "2024-02-01"].to_csv(d / f"{s2}.csv", index=False)   # se corta dos meses antes
    estados = {f["simbolo"]: f["estado"] for f in comprobar(d, u, "2024-03-29")}
    assert estados == {s0: "FALTA", s1: "INVALIDO", s2: "ANTIGUO", s3: "OK"}
    # el umbral de antigüedad es el de la configuración para el horizonte pedido (Anexo A): con H5 (90 días) ya no es antiguo
    assert {f["simbolo"]: f["estado"] for f in comprobar(d, u, "2024-03-29", "H5")}[s2] == "OK"


def test_admite_las_columnas_de_un_proveedor_corriente(tmp_path, comprobar):
    u = cargar_universo(RUTA_UNIVERSO_EJEMPLO).head(1)
    d = _carpeta(tmp_path, u)
    s = u["simbolo"].iloc[0]
    df = pd.read_csv(d / f"{s}.csv").rename(columns={"fecha": "Date", "cierre": "Close"})[["Date", "Close"]]
    df.to_csv(d / f"{s}.csv", index=False)
    assert comprobar(d, u, "2024-03-29")[0]["estado"] == "OK"


def test_el_borrador_del_anexo_b_esta_al_dia():
    mod = _modulo("borrador_anexo_b")
    texto = mod.generar()
    assert mod.SALIDA.read_text(encoding="utf-8") == texto      # si cambian las diferencias, se vuelve a generar
    for ct in ("CT-11.ENCARGO", "CT-22.ENCARGO", "CT-24.RETORNO", "CT-25.RETORNO"):
        assert f"| {ct} |" in texto
    assert "is a required property" not in texto


# ---------------------------------------------------------------- T-131 r02 (QA r01)
def _estropear(tmp_path, cambio):
    u = cargar_universo(RUTA_UNIVERSO_EJEMPLO).head(1)
    d = _carpeta(tmp_path, u)
    s = u["simbolo"].iloc[0]
    df = pd.read_csv(d / f"{s}.csv")
    df = df[pd.to_datetime(df["fecha"]) <= "2024-03-29"]
    cambio(df).to_csv(d / f"{s}.csv", index=False)
    return d, u


@pytest.mark.parametrize("nombre,cambio", [
    ("cierre de texto", lambda df: df.assign(cierre="n/d")),
    ("cierre cero", lambda df: df.assign(cierre=0.0)),
    ("cierre negativo", lambda df: df.assign(cierre=-df["cierre"])),
    ("fechas repetidas dentro del rango", lambda df: pd.concat([df, df.tail(3)])),
])
def test_r02_h01_valida_como_el_ciclo(tmp_path, comprobar, nombre, cambio):
    d, u = _estropear(tmp_path, cambio)
    assert comprobar(d, u, "2024-03-29")[0]["estado"] == "INVALIDO", nombre


def test_r02_h01_lo_posterior_a_as_of_no_cuenta_como_en_el_ciclo(tmp_path, comprobar):
    # un dato malo posterior a as_of no excluye el símbolo (T-65, QA r03, H-21): el ciclo tampoco lo ve
    u = cargar_universo(RUTA_UNIVERSO_EJEMPLO).head(1)
    d = _carpeta(tmp_path, u)
    s = u["simbolo"].iloc[0]
    df = pd.read_csv(d / f"{s}.csv")
    pd.concat([df, df.tail(3)]).to_csv(d / f"{s}.csv", index=False)       # repetidas en 2026, as_of en 2024
    assert comprobar(d, u, "2024-03-29")[0]["estado"] == "OK"


def test_r02_h03_en_h1_cuenta_sesiones(tmp_path, comprobar):
    d, u = _estropear(tmp_path, lambda df: df[pd.to_datetime(df["fecha"]) <= "2024-03-22"])   # último cierre, viernes
    assert comprobar(d, u, "2024-03-25", "H1")[0]["estado"] == "OK"          # el lunes: una sesión
    assert comprobar(d, u, "2024-03-27", "H1")[0]["estado"] == "ANTIGUO"


def test_r02_h04_carpeta_inexistente(capsys):
    mod = _modulo("comprobar_datos_a")
    assert mod.main(["/no/existe/carpeta"]) == 2
    assert "no existe la carpeta" in capsys.readouterr().err


def test_r02_h02_el_borrador_recoge_los_campos_de_primer_nivel_y_los_lotes():
    texto = _modulo("borrador_anexo_b").generar()
    filas = [ln for ln in texto.splitlines() if ln.startswith("| CT-")]
    assert any(ln.startswith("| CT-03.ENCARGO |") and "`query_id`" in ln for ln in filas)
    assert any(ln.startswith("| CT-23.ENCARGO |") and "`run_id`" in ln for ln in filas)
    assert any(ln.startswith("| CT-03.RETORNO |") and "`escalado` llega con otro tipo" in ln for ln in filas)
    assert any(ln.startswith("| CT-09.RETORNO |") and "lo sirve el Motor" not in ln and "Motor" in ln for ln in filas)   # T-140, H-06
    assert "faltan campos mínimos ['piezas']" in texto and "`afirmacion`" in texto
    assert "`fecha_corte` de CT-09" in texto and "esquemas_respuestas.json" in texto
