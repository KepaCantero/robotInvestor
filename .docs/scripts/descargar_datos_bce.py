"""Descarga los tipos de cambio de referencia del BCE y escribe las series de divisas del universo del Bloque A en el formato
de HT-01 (T-141; fuente de datos reales elegida por defecto con el visto bueno del operador del 15-11-2026).

El BCE fija cada día hábil de TARGET el valor de cada moneda frente al euro con los precios del mercado a las 14:15 (CET)
y lo **publica hacia las 16:00 (CET)** (API pública, sin cuenta ni clave: https://data-api.ecb.europa.eu, serie
EXR.D.<moneda>.EUR.SP00.A). El «cierre» de cada serie es esa fijación de las 14:15, no el cierre de un mercado (T-147, QA
r01 de T-141, H-02). Con eso salen los cruces del universo:
EURUSD=X = USD/EUR; USDJPY=X = JPY/USD; GBPUSD=X = USD/GBP; AUDUSD=X = USD/AUD; USDCHF=X = CHF/USD; USDMXN=X = MXN/USD.
Cada CSV lleva `fecha`, `cierre` y `fecha_publicacion`. `fecha_publicacion` es el mismo día: vale para un ciclo con corte
al final del día; un ciclo que corra ese mismo día antes de las 16:00 (CET) usaría un dato aún no publicado (HT-01 solo
lleva la fecha, no la hora). Los datos no se suben al repositorio: se descargan donde se pida.

T-147 (QA r01 de T-141, H-03): todo se valida antes de escribir nada (columnas, ninguna moneda ausente, ninguna fecha
repetida para una moneda, ninguna serie vacía tras quitar los valores no positivos o no finitos); los CSV se escriben en
una carpeta temporal junto al destino y se mueven al final, así que un fallo no deja la carpeta a medias. Una respuesta
rara del servicio (vacía, HTML, error HTTP, sin conexión) termina con un mensaje y el código 1, sin traza.

Uso (desde la raíz): .venv/bin/python .docs/scripts/descargar_datos_bce.py <carpeta> [--desde AAAA-MM-DD]
Luego: .venv/bin/python .docs/scripts/comprobar_datos_a.py <carpeta> --clases DIV
"""
import argparse
import io
import os
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd

URL = "https://data-api.ecb.europa.eu/service/data/EXR/D.{monedas}.EUR.SP00.A?startPeriod={desde}&format=csvdata"
MONEDAS = ("USD", "JPY", "GBP", "AUD", "CHF", "MXN")
COLUMNAS = ("CURRENCY", "TIME_PERIOD", "OBS_VALUE")
# símbolo → (numerador, denominador), cada uno en «unidades por euro»: el cruce es numerador / denominador
CRUCES = {"EURUSD=X": ("USD", None), "USDJPY=X": ("JPY", "USD"), "GBPUSD=X": ("USD", "GBP"), "AUDUSD=X": ("USD", "AUD"),
          "USDCHF=X": ("CHF", "USD"), "USDMXN=X": ("MXN", "USD")}


class RespuestaBCE(ValueError):
    """La respuesta del BCE no sirve: no se escribe nada (T-147)."""


def leer(cuerpo: bytes) -> pd.DataFrame:
    """Tabla fecha × moneda de la respuesta CSV del BCE, validada (T-147, H-03)."""
    try:
        crudo = pd.read_csv(io.BytesIO(cuerpo))
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as e:
        raise RespuestaBCE(f"la respuesta no es un CSV legible ({type(e).__name__})") from e
    falta = [c for c in COLUMNAS if c not in crudo.columns]
    if falta:
        raise RespuestaBCE(f"la respuesta no trae las columnas {', '.join(falta)} (¿una página de error?)")
    crudo = crudo[list(COLUMNAS)]
    if crudo.empty:
        raise RespuestaBCE("la respuesta no trae ninguna observación")
    sin = sorted(set(MONEDAS) - set(crudo["CURRENCY"]))
    if sin:
        raise RespuestaBCE(f"faltan las monedas {', '.join(sin)}")
    repetidas = crudo[crudo.duplicated(["CURRENCY", "TIME_PERIOD"], keep=False)]
    if not repetidas.empty:
        ej = repetidas.iloc[0]
        raise RespuestaBCE(f"{len(repetidas)} filas con una fecha repetida para su moneda (p. ej. {ej['CURRENCY']} el "
                           f"{ej['TIME_PERIOD']}): no se elige una en silencio")
    crudo = crudo.assign(OBS_VALUE=pd.to_numeric(crudo["OBS_VALUE"], errors="coerce"))
    try:
        fechas = pd.to_datetime(crudo["TIME_PERIOD"], format="%Y-%m-%d")
    except (ValueError, TypeError) as e:
        raise RespuestaBCE("fechas que no son AAAA-MM-DD en TIME_PERIOD") from e
    ancho = crudo.assign(TIME_PERIOD=fechas).pivot(index="TIME_PERIOD", columns="CURRENCY", values="OBS_VALUE")
    return ancho.sort_index()


def descargar(desde: str) -> pd.DataFrame:
    with urllib.request.urlopen(URL.format(monedas="+".join(MONEDAS), desde=desde), timeout=120) as r:   # noqa: S310
        return leer(r.read())


def cruces(ancho: pd.DataFrame) -> dict[str, pd.DataFrame]:
    salida = {}
    for simbolo, (num, den) in CRUCES.items():
        s = ancho[num] if den is None else ancho[num] / ancho[den]
        s = s.dropna()
        s = s[s.replace([float("inf"), -float("inf")], float("nan")).notna() & (s > 0)]   # positivo y finito
        if s.empty:   # T-147 (H-03): antes se escribía un CSV vacío y el script caía después
            raise RespuestaBCE(f"{simbolo}: ningún valor positivo y finito")
        fechas = s.index.strftime("%Y-%m-%d")
        salida[simbolo] = pd.DataFrame({"fecha": fechas, "cierre": s.round(8).to_numpy(), "fecha_publicacion": fechas})
    return salida


def escribir(series: dict[str, pd.DataFrame], destino: Path) -> None:
    """Escribe todo en una carpeta temporal junto al destino y lo mueve al final (T-147, H-03)."""
    destino.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix=".bce_", dir=destino))
    try:
        for simbolo, df in series.items():
            df.to_csv(tmp / f"{simbolo}.csv", index=False)
        for simbolo in series:
            os.replace(tmp / f"{simbolo}.csv", destino / f"{simbolo}.csv")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("carpeta")
    ap.add_argument("--desde", default="2015-01-01")
    a = ap.parse_args(argv)
    destino = Path(a.carpeta)
    try:
        series = cruces(descargar(a.desde))
    except RespuestaBCE as e:
        print(f"respuesta del BCE no válida, no se escribe nada: {e}", file=sys.stderr)
        return 1
    except urllib.error.HTTPError as e:
        print(f"el BCE respondió HTTP {e.code} ({e.reason}), no se escribe nada", file=sys.stderr)
        return 1
    except (urllib.error.URLError, OSError) as e:
        print(f"no se pudo descargar del BCE ({type(e).__name__}: {e}), no se escribe nada", file=sys.stderr)
        return 1
    escribir(series, destino)
    for simbolo, df in series.items():
        print(f"{simbolo}: {len(df)} cierres, {df['fecha'].iloc[0]} → {df['fecha'].iloc[-1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
