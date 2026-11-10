"""r04_02 · QA T-65 r04 · H-21: HT-01 valida por filas solo lo que se usa, hasta as_of y en la ventana.

Uso (desde bloque_a/11_Ejecutor):  ../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r04_02_filas_en_rango.py

Busca huecos del cambio: un dato malo DENTRO del rango que pase, una fila futura (o aún no publicada) que cambie lo que se
ve a la fecha as_of (fuga), y diferencias entre lo que valida la emisión (cierres del rango) y la resolución (valor_en).
Cada caso: (nombre, filas del CSV, as_of, lectura, esperado) con esperado RECHAZA / ACEPTA.
"""
import pathlib
import sys
import tempfile
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path.cwd()))
from bloque_a.herramientas.ht01_datos import DatosInvalidos, DatosNoDisponibles, ProveedorCSV  # noqa: E402

hall, info = 0, 0
FECHAS = [str(d.date()) for d in pd.bdate_range("2023-01-02", "2026-06-30")]


def csv(mod=None, pub=False):
    filas = [{"fecha": f, "cierre": 100 + i * 0.01} for i, f in enumerate(FECHAS)]
    if pub:
        for r in filas:
            r["fecha_publicacion"] = ""
    if mod:
        filas = mod(filas)
    cols = ["fecha", "cierre"] + (["fecha_publicacion"] if pub else [])
    return ",".join(cols) + "\n" + "".join(",".join(str(r.get(c, "")) for c in cols) + "\n" for r in filas)


def leer(texto, as_of, lectura):
    d = pathlib.Path(tempfile.mkdtemp(prefix="r04_02_"))
    (d / "S.csv").write_text(texto, encoding="utf-8")
    p = ProveedorCSV(d)
    p.fijar_as_of(as_of)
    try:
        if lectura == "cierres_ventana":
            s = p.cierres("S", pd.Timestamp(as_of) - pd.DateOffset(years=3), as_of)
            return "ACEPTA", f"{len(s)} cierres, último {s.index[-1].date()}={s.iloc[-1]}"
        if lectura == "valor_en":
            f, v = p.valor_en("S", as_of)
            return "ACEPTA", f"{f.date()}={v}"
        if lectura == "serie":
            df = p.serie("S")
            return "ACEPTA", f"columnas={list(df.columns)} filas={len(df)} NaN en cierre={int(df['cierre'].isna().sum())}"
    except DatosInvalidos as e:
        return "RECHAZA", f"DatosInvalidos: {str(e)[:150]}"
    except DatosNoDisponibles as e:
        return "NO_DISPONIBLE", str(e)[:150]
    except Exception as e:  # noqa: BLE001
        return "EXCEPCION", f"{type(e).__name__}: {str(e)[:150]}"


def poner(fecha, valor):
    def f(filas):
        for r in filas:
            if r["fecha"] == fecha:
                r["cierre"] = valor
        return filas
    return f


def duplicar(fecha, valor, pub=""):
    def f(filas):
        i = next(k for k, r in enumerate(filas) if r["fecha"] == fecha)
        extra = dict(filas[i], cierre=valor)
        if pub:
            extra["fecha_publicacion"] = pub
        return filas[: i + 1] + [extra] + filas[i + 1:]
    return f


AS = "2026-06-05"
CASOS = [
    # Dentro del rango: deben rechazarse
    ("n.d. dentro de la ventana (2025-03-03)", csv(poner("2025-03-03", "n.d.")), AS, "cierres_ventana", "RECHAZA"),
    ("inf dentro de la ventana", csv(poner("2025-03-03", "inf")), AS, "cierres_ventana", "RECHAZA"),
    ("booleano suelto dentro de la ventana", csv(poner("2025-03-03", "True")), AS, "cierres_ventana", "RECHAZA"),
    ("fecha repetida dentro de la ventana", csv(duplicar("2025-03-03", 150)), AS, "cierres_ventana", "RECHAZA"),
    ("fecha repetida con el mismo valor", csv(duplicar("2025-03-03", 100 + FECHAS.index("2025-03-03") * 0.01)), AS, "cierres_ventana", "RECHAZA"),
    ("n.d. en la fecha as_of", csv(poner(AS, "n.d.")), AS, "valor_en", "RECHAZA"),
    ("fecha repetida en la fecha as_of", csv(duplicar(AS, 150)), AS, "valor_en", "RECHAZA"),
    ("n.d. justo en el primer día de la ventana", csv(poner("2023-06-05", "n.d.")), AS, "cierres_ventana", "RECHAZA"),
    # Fuera del rango: no deben importar
    ("n.d. el día antes de la ventana", csv(poner("2023-06-02", "n.d.")), AS, "cierres_ventana", "ACEPTA"),
    ("n.d. el día después de as_of", csv(poner("2026-06-08", "n.d.")), AS, "cierres_ventana", "ACEPTA"),
    ("fecha repetida posterior a as_of", csv(duplicar("2026-06-08", 150)), AS, "valor_en", "ACEPTA"),
    # Fugas por fecha_publicacion: lo que aún no se ha publicado no puede cambiar lo que se ve a la fecha as_of
    ("n.d. visible solo desde 2026-07-01", csv(lambda fs: [dict(r, cierre="n.d.", fecha_publicacion="2026-07-01") if r["fecha"] == "2026-05-04" else r for r in fs], pub=True),
     AS, "cierres_ventana", "ACEPTA"),
    ("revisión de 2026-05-29 publicada el 2026-07-01 (fecha repetida, la 2.ª copia aún no publicada)",
     csv(duplicar("2026-05-29", 150, pub="2026-07-01"), pub=True), AS, "cierres_ventana", "ACEPTA"),
    ("revisión de 2026-05-29 publicada el 2026-07-01, leída con valor_en del 2026-05-29",
     csv(duplicar("2026-05-29", 150, pub="2026-07-01"), pub=True), "2026-05-29", "valor_en", "ACEPTA"),
    ("misma revisión ya publicada (as_of 2026-07-02)", csv(duplicar("2026-05-29", 150, pub="2026-07-01"), pub=True), "2026-07-02",
     "cierres_ventana", "RECHAZA"),
]

for nombre, texto, as_of, lectura, esperado in CASOS:
    got, det = leer(texto, as_of, lectura)
    ok = got == esperado
    hall += 0 if ok else 1
    print(f"{'OK' if ok else 'HALLAZGO':9} {nombre} [{lectura}, as_of {as_of}]: {got} (esperado {esperado}) · {det}")

# serie(): lo que devuelve a quien la lea directamente (hoy nadie fuera de HT-01)
got, det = leer(csv(poner("2025-03-03", "n.d.")), AS, "serie")
info += 1
print(f"INFO      serie() con un n.d. en la ventana: {got} · {det}")

print(f"HALLAZGOS: {hall} · INFO: {info}")
