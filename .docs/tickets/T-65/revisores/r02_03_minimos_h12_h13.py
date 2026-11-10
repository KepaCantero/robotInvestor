"""r02_03 · QA T-65 r02 · reproducción mínima de H-12 y H-13 (más rápida que r02_01).

Uso (desde bloque_a/11_Ejecutor):  ../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r02_03_minimos_h12_h13.py

H-12: ACWI (índice de referencia de RV en `indices_referencia`) con un cierre 0 la semana anterior, o sin archivo. Ciclo de
RV y DIV. Esperado: el ciclo no cae; DIV sigue; RV se degrada (pronóstico sin referencia, o tipo PARCIAL) y lo declara.
H-13: un par DIV nuevo en el formato de exportación más común (Yahoo: «Date,Open,High,Low,Close,Adj Close,Volume», dos
columnas que son alias de `cierre`) o con fechas con zona horaria («2026-06-05 00:00:00-04:00»). Ciclo de DIV y RV.
Esperado: el símbolo se excluye y se declara (`DatosInvalidos`), o se lee bien; el ciclo no cae.
"""
import pathlib
import shutil
import sys
import tempfile
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path.cwd()))
from bloque_a.configuracion import DIR_EJECUTOR, RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

AS_OF = "2026-06-05"
F = list(pd.bdate_range("2023-01-02", AS_OF))
LINEA = "USDNEW=X,DIV,Dólar frente a nueva divisa,ESTRATEGIA,GLB,G10,USD,SOLO EJEMPLO,Pares,Par nuevo,Otros cruces,USD/NEW,\n"
hall = 0


def ciclo(nombre, cambiar, nuevo_div=False):
    global hall
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="r02_03_"))
    datos = tmp / "datos"
    shutil.copytree(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos", datos)
    uni = pathlib.Path(RUTA_UNIVERSO_EJEMPLO).read_text(encoding="utf-8").rstrip("\n") + "\n" + (LINEA if nuevo_div else "")
    (tmp / "u.csv").write_text(uni, encoding="utf-8")
    cambiar(datos)
    b = Bloque(cargar_config(extra={"modo": "backtest", "perfiles": {"activos": ["RV", "DIV", "IDX"]}}), ProveedorCSV(datos),
               cargar_universo(tmp / "u.csv"), MockClient(), tmp / "e", tmp / "s")
    try:
        r = b.ciclo(AS_OF, alcance={"clases": ["RV", "DIV"]})
        ops = {c: len(v["opciones"]) for c, v in r["paquete"]["clases"].items()}
        print(f"OK        {nombre}: estado={r['estado']} opciones={ops}")
    except Exception as e:  # noqa: BLE001
        hall += 1
        print(f"HALLAZGO  {nombre}: el ciclo de RV y DIV cae: {type(e).__name__}: {str(e)[:140]}")


def acwi_cero(datos):
    t = (datos / "ACWI.csv").read_text(encoding="utf-8").splitlines()
    i = t[0].split(",").index("cierre")
    out = [t[0]]
    for ln in t[1:]:
        c = ln.split(",")
        if c[0] == "2026-05-29":
            c[i] = "0"
        out.append(",".join(c))
    (datos / "ACWI.csv").write_text("\n".join(out) + "\n", encoding="utf-8")


def yahoo(datos):
    (datos / "USDNEW=X.csv").write_text("Date,Open,High,Low,Close,Adj Close,Volume\n" + "".join(
        f"{d.date()},1,1,1,1.0{i % 9},1.0{i % 9},0\n" for i, d in enumerate(F)), encoding="utf-8")


def zona_horaria(datos):
    (datos / "USDNEW=X.csv").write_text("Date,Close\n" + "".join(
        f"{d.date()} 00:00:00-04:00,1.0{i % 9}\n" for i, d in enumerate(F)), encoding="utf-8")


ciclo("H-12 · ACWI con un cierre 0 el 2026-05-29", acwi_cero)
ciclo("H-12 · ACWI sin archivo", lambda d: (d / "ACWI.csv").unlink())
ciclo("H-13 · par DIV con cabecera de Yahoo (Close y Adj Close)", yahoo, nuevo_div=True)
ciclo("H-13 · par DIV con fechas con zona horaria", zona_horaria, nuevo_div=True)
print(f"HALLAZGOS: {hall}")
