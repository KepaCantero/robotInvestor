"""r03_01 · QA T-65 r03 · formas raras de CSV en HT-01 (H-13 y H-14): nunca una excepción que no sea `DatosNoDisponibles`.

Uso (desde bloque_a/11_Ejecutor):  ../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r03_01_formas_csv.py

Para cada CSV se espera una de dos cosas: «LEE» (se lee bien y da los cierres esperados) o «RECHAZA» (`DatosInvalidos` o
`DatosNoDisponibles`). Cualquier otra excepción, o leer otra cosa que la esperada en silencio, es HALLAZGO. Los casos
marcados «ambiguo» son los que H-13 dice no resolver en silencio (dos columnas para el mismo campo).
"""
import pathlib
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path.cwd()))
from bloque_a.herramientas.ht01_datos import DatosNoDisponibles, ProveedorCSV  # noqa: E402

AS_OF = "2026-06-05"
F = list(pd.bdate_range("2026-01-05", AS_OF))
V = [1.0 + (i % 7) / 100 for i in range(len(F))]
hall, info = 0, 0


def filas(fmt=lambda d: str(d.date()), val=lambda v: f"{v:.2f}", n=None):
    return "".join(f"{fmt(d)},{val(v)}\n" for d, v in list(zip(F, V))[: n or len(F)])


CASOS = [  # (nombre, contenido (str o bytes), esperado: LEE | RECHAZA | AMBIGUO)
    ("cabecera en mayúsculas", "FECHA,CIERRE\n" + filas(), "LEE"),
    ("cabecera con espacios", " Fecha , Cierre \n" + filas(), "LEE"),
    ("BOM UTF-8", ("﻿fecha,cierre\n" + filas()).encode("utf-8"), "LEE"),
    ("BOM UTF-8 y Date,Close", ("﻿Date,Close\n" + filas()).encode("utf-8"), "LEE"),
    ("CRLF", ("fecha,cierre\n" + filas()).replace("\n", "\r\n"), "LEE"),
    ("solo Adj Close", "Date,Adj Close\n" + filas(), "LEE"),
    ("Close y Adj Close", "Date,Close,Adj Close\n" + "".join(f"{d.date()},{v},{v * 0.9}\n" for d, v in zip(F, V)), "AMBIGUO"),
    ("cierre y valor", "fecha,cierre,valor\n" + "".join(f"{d.date()},{v},{v}\n" for d, v in zip(F, V)), "AMBIGUO"),
    ("fecha y date", "fecha,date,cierre\n" + "".join(f"{d.date()},{d.date()},{v}\n" for d, v in zip(F, V)), "AMBIGUO"),
    ("cierre repetido (mismo nombre)", "fecha,cierre,cierre\n" + "".join(f"{d.date()},{v},{v * 2}\n" for d, v in zip(F, V)),
     "AMBIGUO"),
    ("Close repetido (mismo nombre)", "Date,Close,Close\n" + "".join(f"{d.date()},{v},{v * 2}\n" for d, v in zip(F, V)),
     "AMBIGUO"),
    ("fecha repetida (mismo nombre)", "fecha,fecha,cierre\n" + "".join(f"{d.date()},2020-01-01,{v}\n" for d, v in zip(F, V)),
     "AMBIGUO"),
    ("separador punto y coma", "fecha;cierre\n" + filas().replace(",", ";"), "RECHAZA"),
    ("separador tabulador", "fecha\tcierre\n" + filas().replace(",", "\t"), "RECHAZA"),
    ("separador barra", "fecha|cierre\n" + filas().replace(",", "|"), "RECHAZA"),
    ("coma decimal entre comillas", "fecha,cierre\n" + filas(val=lambda v: f'"{v:.2f}"'.replace(".", ",")), "RECHAZA"),
    ("miles con coma entre comillas", "fecha,cierre\n" + filas(val=lambda v: f'"1,{int(v * 100):03d}.5"'), "RECHAZA"),
    ("cierre inf en una fila futura", "fecha,cierre\n" + filas() + "2026-06-08,inf\n", "LEE|RECHAZA"),
    ("cierre inf en la ventana", "fecha,cierre\n" + filas(n=len(F) - 1) + f"{F[-1].date()},inf\n", "RECHAZA"),
    ("cierre -inf", "fecha,cierre\n" + filas(n=len(F) - 1) + f"{F[-1].date()},-inf\n", "RECHAZA"),
    ("cierre 1e309 (desborda)", "fecha,cierre\n" + filas(n=len(F) - 1) + f"{F[-1].date()},1e309\n", "RECHAZA"),
    ("cierre Infinity", "fecha,cierre\n" + filas(n=len(F) - 1) + f"{F[-1].date()},Infinity\n", "RECHAZA"),
    ("cierre texto", "fecha,cierre\n" + filas(n=len(F) - 1) + f"{F[-1].date()},abc\n", "RECHAZA"),
    ("cierre -0", "fecha,cierre\n" + filas(n=len(F) - 1) + f"{F[-1].date()},-0\n", "RECHAZA"),
    ("cierre NaN textual (celda vacía)", "fecha,cierre\n" + filas(n=len(F) - 1) + f"{F[-1].date()},NaN\n", "LEE-1"),
    ("todos los cierres NaN", "fecha,cierre\n" + "".join(f"{d.date()},NaN\n" for d in F), "RECHAZA"),
    ("una sola fila", f"fecha,cierre\n{F[-1].date()},1.5\n", "LEE"),
    ("solo cabecera", "fecha,cierre\n", "RECHAZA"),
    ("solo filas futuras", "fecha,cierre\n2026-07-01,1\n2026-07-02,1.1\n", "RECHAZA"),
    ("filas futuras y pasadas", "fecha,cierre\n" + filas() + "2027-01-04,999\n", "LEE"),
    ("fecha_publicacion futura en todas", "fecha,cierre,fecha_publicacion\n" + "".join(
        f"{d.date()},{v},2027-01-01\n" for d, v in zip(F, V)), "RECHAZA"),
    ("fechas desordenadas", "fecha,cierre\n" + "".join(reversed(filas().splitlines(True))), "LEE"),
    ("fecha con Z (UTC)", "fecha,cierre\n" + filas(fmt=lambda d: f"{d.date()}T00:00:00Z"), "RECHAZA"),
    ("zonas mezcladas", "fecha,cierre\n" + "".join(
        f"{d.date()}{'+02:00' if i % 2 else ''},{v}\n" for i, (d, v) in enumerate(zip(F, V))), "RECHAZA"),
    ("fecha AAAAMMDD entera", "fecha,cierre\n" + filas(fmt=lambda d: d.strftime("%Y%m%d")), "LEE|RECHAZA"),
    ("fecha DD/MM/AAAA", "fecha,cierre\n" + filas(fmt=lambda d: d.strftime("%d/%m/%Y")), "LEE|RECHAZA"),
    ("línea de total al final", "fecha,cierre\n" + filas() + "Total,999\n", "RECHAZA"),
    ("campo de más en una fila", "fecha,cierre\n" + filas() + f"{F[-1].date()},1,2\n", "RECHAZA"),
    ("cierre booleano", "fecha,cierre\n" + filas(val=lambda v: "True"), "RECHAZA"),
    ("cierre con espacios", "fecha,cierre\n" + filas(val=lambda v: f"  {v:.2f} "), "LEE"),
    ("UTF-16", ("fecha,cierre\n" + filas()).encode("utf-16"), "RECHAZA"),
    ("bytes nulos", b"fecha,cierre\n\x00\x00\x00\n", "RECHAZA"),
]

tmp = pathlib.Path(tempfile.mkdtemp(prefix="r03_01_"))
esperado_lee = pd.Series(V, index=pd.DatetimeIndex(F))
for i, (nombre, contenido, esperado) in enumerate(CASOS):
    sym = f"S{i:02d}"
    ruta = tmp / f"{sym}.csv"
    (ruta.write_bytes if isinstance(contenido, bytes) else lambda t: ruta.write_text(t, encoding="utf-8"))(contenido)
    p = ProveedorCSV(tmp)
    p.fijar_as_of(AS_OF)
    try:
        s = p.cierres(sym)
        fd, ult = p.valor_en(sym, AS_OF)
        res = "LEE"
        detalle = f"{len(s)} cierres, último {fd.date()}={ult}"
    except DatosNoDisponibles as e:
        res, detalle = "RECHAZA", f"{type(e).__name__}: {str(e)[:110]}"
    except Exception as e:  # noqa: BLE001
        hall += 1
        print(f"HALLAZGO  {nombre}: excepción no controlada {type(e).__name__}: {str(e)[:120]}")
        continue
    if esperado == "AMBIGUO":
        ok = res == "RECHAZA"
        etiqueta = "OK" if ok else "HALLAZGO"
        if not ok:
            hall += 1
            detalle += " · se eligió una de las dos columnas en silencio"
    elif esperado == "LEE-1":
        ok = res == "LEE" and len(s) == len(F) - 1
        etiqueta = "OK" if ok else "INFO"
    elif "|" in esperado:
        ok = res in esperado.split("|")
        if res == "LEE":
            ok = bool(np.isclose(s.reindex(esperado_lee.index).to_numpy(), esperado_lee.to_numpy()).all()) and len(s) == len(F)
            detalle += "" if ok else " · fechas mal interpretadas en silencio"
        etiqueta = "OK" if ok else "HALLAZGO"
        hall += 0 if ok else 1
    else:
        ok = res == esperado
        etiqueta = "OK" if ok else "INFO"
    if etiqueta == "INFO":
        info += 1
    print(f"{etiqueta:9} {nombre}: {res} (esperado {esperado}) · {detalle}")
print(f"HALLAZGOS: {hall} · INFO: {info}")
