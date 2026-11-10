"""r05_04 · QA T-65 r05 · H-25: fechas repetidas con `fecha_publicacion` (revisiones) en HT-01, variantes propias.

Uso (desde bloque_a/11_Ejecutor):  ../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r05_04_revisiones_publicacion.py

Cada caso: (nombre, filas añadidas a una serie sana con columna `fecha_publicacion`, as_of, lectura, esperado).
Regla que se comprueba (README de T-65, H-25): solo cuentan como repetidas las filas ya publicadas a la fecha as_of y
dentro del rango que se lee; con las dos publicadas, el símbolo se rechaza (declarado).
"""
import pathlib
import sys
import tempfile
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path.cwd()))
from bloque_a.herramientas.ht01_datos import DatosInvalidos, DatosNoDisponibles, ProveedorCSV  # noqa: E402

hall = 0
FECHAS = [str(d.date()) for d in pd.bdate_range("2023-01-02", "2026-06-30")]


def csv(extra):
    filas = [(f, 100 + i * 0.01, "") for i, f in enumerate(FECHAS)] + list(extra)
    filas.sort(key=lambda r: r[0])
    return "fecha,cierre,fecha_publicacion\n" + "".join(f"{a},{b},{c}\n" for a, b, c in filas)


def leer(texto, as_of, lectura):
    d = pathlib.Path(tempfile.mkdtemp(prefix="r05_04_"))
    (d / "S.csv").write_text(texto, encoding="utf-8")
    p = ProveedorCSV(d)
    p.fijar_as_of(as_of)
    try:
        if lectura == "ventana":
            s = p.cierres("S", pd.Timestamp(as_of) - pd.DateOffset(years=3), as_of)
            return "ACEPTA", f"{len(s)} cierres, último {s.index[-1].date()}={s.iloc[-1]}"
        if lectura.startswith("valor_en:"):
            f, v = p.valor_en("S", lectura.split(":", 1)[1])
            return "ACEPTA", f"{f.date()}={v}"
        if lectura.startswith("tramo:"):
            a, b = lectura.split(":", 1)[1].split("/")
            s = p.cierres("S", a, b)
            return "ACEPTA", f"{len(s)} cierres"
    except DatosInvalidos as e:
        return "RECHAZA", str(e)[:140]
    except DatosNoDisponibles as e:
        return "NO_DISPONIBLE", str(e)[:140]
    except Exception as e:  # noqa: BLE001
        return "EXCEPCION", f"{type(e).__name__}: {str(e)[:140]}"


REV = ("2026-05-29", 999.0, "2026-07-01")
REV2 = ("2026-05-29", 999.0, "2026-06-15")   # la misma revisión, publicada antes del 2026-06-30
CASOS = [
    ("revisión aún no publicada (ventana)", [REV], "2026-06-05", "ventana", "ACEPTA"),
    ("revisión publicada justo en as_of", [("2026-05-29", 999.0, "2026-06-05")], "2026-06-05", "ventana", "RECHAZA"),
    ("revisión publicada el día después de as_of", [("2026-05-29", 999.0, "2026-06-06")], "2026-06-05", "ventana", "ACEPTA"),
    ("revisión ya publicada (as_of 2026-06-30)", [REV2], "2026-06-30", "ventana", "NO_DISPONIBLE"),
    ("revisión ya publicada, tramo que no la incluye", [REV2], "2026-06-30", "tramo:2026-06-01/2026-06-30", "ACEPTA"),
    ("revisión ya publicada, valor_en de otra fecha", [REV2], "2026-06-30", "valor_en:2026-06-30", "ACEPTA"),
    ("revisión ya publicada, valor_en de esa fecha", [REV2], "2026-06-30", "valor_en:2026-05-29", "RECHAZA"),
    ("dos revisiones futuras de la misma fecha", [REV, ("2026-05-29", 998.0, "2026-08-01")], "2026-06-05", "ventana", "ACEPTA"),
    ("revisión con fecha_publicacion ilegible", [("2026-05-29", 999.0, "pronto")], "2026-06-05", "ventana", "ACEPTA"),
    ("triple: una futura y una sin fecha_publicacion", [REV, ("2026-05-29", 997.0, "")], "2026-06-05", "ventana", "RECHAZA"),
    ("revisión idéntica ya publicada", [("2026-05-29", None, "2026-06-01")], "2026-06-05", "ventana", "RECHAZA"),
    ("revisión antigua (2023) ya publicada, fuera de la ventana de 3 años", [("2023-01-03", 999.0, "2023-02-01")], "2026-06-05",
     "ventana", "ACEPTA"),
]
for nombre, extra, as_of, lectura, esperado in CASOS:
    if extra and extra[0][1] is None:
        i = FECHAS.index(extra[0][0])
        extra = [(extra[0][0], 100 + i * 0.01, extra[0][2])]
    obtenido, detalle = leer(csv(extra), as_of, lectura)
    if esperado == "NO_DISPONIBLE":
        esperado = "RECHAZA"   # la ventana incluye 2026-05-29 con las dos filas visibles
    ok = obtenido == esperado
    hall += 0 if ok else 1
    print(f"{'OK' if ok else 'HALLAZGO':9} {nombre}: {obtenido} (esperado {esperado}) · {detalle}")
print(f"HALLAZGOS: {hall}")
