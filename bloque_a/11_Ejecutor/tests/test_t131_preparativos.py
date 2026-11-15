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
