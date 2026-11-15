"""Descarga los tipos de cambio de referencia del BCE y escribe las series de divisas del universo del Bloque A en el formato
de HT-01 (T-141; fuente de datos reales elegida por defecto con el visto bueno del operador del 15-11-2026).

El BCE publica cada día hábil, a las 14:15 (CET), el valor de cada moneda frente al euro (API pública, sin cuenta ni clave:
https://data-api.ecb.europa.eu, serie EXR.D.<moneda>.EUR.SP00.A). Con eso salen los cruces del universo:
EURUSD=X = USD/EUR; USDJPY=X = JPY/USD; GBPUSD=X = USD/GBP; AUDUSD=X = USD/AUD; USDCHF=X = CHF/USD; USDMXN=X = MXN/USD.
Cada CSV lleva `fecha`, `cierre` y `fecha_publicacion` (el mismo día: el dato se conoce a las 14:15). Los datos no se suben
al repositorio: se descargan donde se pida.

Uso (desde la raíz): .venv/bin/python .docs/scripts/descargar_datos_bce.py <carpeta> [--desde AAAA-MM-DD]
Luego: .venv/bin/python .docs/scripts/comprobar_datos_a.py <carpeta> --clases DIV
"""
import argparse
import io
import sys
import urllib.request
from pathlib import Path

import pandas as pd

URL = "https://data-api.ecb.europa.eu/service/data/EXR/D.{monedas}.EUR.SP00.A?startPeriod={desde}&format=csvdata"
MONEDAS = ("USD", "JPY", "GBP", "AUD", "CHF", "MXN")
# símbolo → (numerador, denominador), cada uno en «unidades por euro»: el cruce es numerador / denominador
CRUCES = {"EURUSD=X": ("USD", None), "USDJPY=X": ("JPY", "USD"), "GBPUSD=X": ("USD", "GBP"), "AUDUSD=X": ("USD", "AUD"),
          "USDCHF=X": ("CHF", "USD"), "USDMXN=X": ("MXN", "USD")}


def descargar(desde: str) -> pd.DataFrame:
    with urllib.request.urlopen(URL.format(monedas="+".join(MONEDAS), desde=desde), timeout=120) as r:   # noqa: S310
        crudo = pd.read_csv(io.BytesIO(r.read()), usecols=["CURRENCY", "TIME_PERIOD", "OBS_VALUE"])
    crudo["OBS_VALUE"] = pd.to_numeric(crudo["OBS_VALUE"], errors="coerce")
    ancho = crudo.pivot_table(index="TIME_PERIOD", columns="CURRENCY", values="OBS_VALUE", aggfunc="first")
    ancho.index = pd.to_datetime(ancho.index)
    return ancho.sort_index()


def cruces(ancho: pd.DataFrame) -> dict[str, pd.DataFrame]:
    salida = {}
    for simbolo, (num, den) in CRUCES.items():
        s = ancho[num] if den is None else ancho[num] / ancho[den]
        s = s.dropna()
        s = s[s.replace([float("inf"), -float("inf")], float("nan")).notna() & (s > 0)]   # positivo y finito
        fechas = s.index.strftime("%Y-%m-%d")
        salida[simbolo] = pd.DataFrame({"fecha": fechas, "cierre": s.round(8).to_numpy(), "fecha_publicacion": fechas})
    return salida


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("carpeta")
    ap.add_argument("--desde", default="2015-01-01")
    a = ap.parse_args(argv)
    destino = Path(a.carpeta)
    destino.mkdir(parents=True, exist_ok=True)
    series = cruces(descargar(a.desde))
    for simbolo, df in series.items():
        df.to_csv(destino / f"{simbolo}.csv", index=False)
        print(f"{simbolo}: {len(df)} cierres, {df['fecha'].iloc[0]} → {df['fecha'].iloc[-1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
