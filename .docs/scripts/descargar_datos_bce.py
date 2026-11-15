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
T-149 (QA r01 de T-147, H-02): también una fecha repetida escrita de dos formas («2026-11-3» y «2026-11-03») y un
destino que no es una carpeta (se mira antes de descargar) o en el que no se puede escribir.
T-150 (QA r01 de T-149, H-06): una fila sin fecha (`TIME_PERIOD` vacío) y una lectura cortada a medias
(`http.client.IncompleteRead` y los demás errores de `http.client`, que no son `OSError`) terminan también con un mensaje
y el código 1 sin escribir nada; si el traslado de los CSV falla cuando ya se han movido algunos, el mensaje dice cuáles
quedaron escritos (antes decía «no se escribe nada»).

Uso (desde la raíz): .venv/bin/python .docs/scripts/descargar_datos_bce.py <carpeta> [--desde AAAA-MM-DD]
Luego: .venv/bin/python .docs/scripts/comprobar_datos_a.py <carpeta> --clases DIV
"""
import argparse
import http.client
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
    crudo = crudo.assign(OBS_VALUE=pd.to_numeric(crudo["OBS_VALUE"], errors="coerce"))
    try:
        fechas = pd.to_datetime(crudo["TIME_PERIOD"].astype(str), format="%Y-%m-%d")   # T-149: el texto, no un número
    except (ValueError, TypeError) as e:
        raise RespuestaBCE("fechas que no son AAAA-MM-DD en TIME_PERIOD") from e
    if fechas.isna().any():   # T-150 (H-06): un TIME_PERIOD vacío pasa a NaT sin error y dejaba una fila sin fecha
        raise RespuestaBCE(f"{int(fechas.isna().sum())} filas sin fecha en TIME_PERIOD")
    # T-149 (QA r01 de T-147, H-02): las repetidas se buscan en la fecha ya convertida, no en el texto («2026-11-3» y
    # «2026-11-03» son el mismo día; antes `pivot` caía con una traza)
    repetidas = crudo[pd.DataFrame({"m": crudo["CURRENCY"], "f": fechas}).duplicated(keep=False)]
    if not repetidas.empty:
        ej = repetidas.iloc[0]
        raise RespuestaBCE(f"{len(repetidas)} filas con una fecha repetida para su moneda (p. ej. {ej['CURRENCY']} el "
                           f"{ej['TIME_PERIOD']}): no se elige una en silencio")
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


class EscrituraIncompleta(OSError):
    """T-150 (QA r01 de T-149, O-05 y H-06): el traslado de los CSV falló cuando ya se habían movido algunos; `movidos` son
    los que quedaron escritos en el destino (nuevos o sustituidos)."""

    def __init__(self, movidos: list[str], causa: OSError) -> None:
        super().__init__(causa.errno, causa.strerror)
        self.movidos = movidos
        self.causa = causa


class DestinoNoValido(OSError):
    """El destino no admite los CSV: no se escribe nada (T-149)."""


def comprobar_destino(destino: Path, simbolos) -> None:
    """T-149 (QA r01 de T-147, H-02): antes de descargar y de escribir, el destino es una carpeta (o no existe) y ninguno
    de los CSV que se van a escribir es ya una carpeta; si no, `DestinoNoValido` (antes, una traza de `mkdir`). T-150: ni
    el destino ni una carpeta de su ruta es un enlace simbólico roto."""
    for p in (destino, *destino.parents):
        if p.is_symlink() and not p.exists():   # T-150 (O-05): antes se descargaba y fallaba después
            raise DestinoNoValido(f"{p} es un enlace simbólico roto")
        if p.exists():
            if not p.is_dir():
                raise DestinoNoValido(f"{p} existe y no es una carpeta")
            break
    ocupados = [s for s in simbolos if (destino / f"{s}.csv").exists() and not (destino / f"{s}.csv").is_file()]
    if ocupados:
        raise DestinoNoValido(f"en {destino} ya hay algo que no es un fichero con el nombre de {', '.join(ocupados)}")


def escribir(series: dict[str, pd.DataFrame], destino: Path) -> None:
    """Escribe todo en una carpeta temporal junto al destino y lo mueve al final (T-147, H-03)."""
    comprobar_destino(destino, series)
    destino.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix=".bce_", dir=destino))
    try:
        for simbolo, df in series.items():
            df.to_csv(tmp / f"{simbolo}.csv", index=False)
        movidos: list[str] = []
        for simbolo in series:
            try:
                os.replace(tmp / f"{simbolo}.csv", destino / f"{simbolo}.csv")
            except OSError as e:
                if movidos:
                    raise EscrituraIncompleta(movidos, e) from e
                raise
            movidos.append(f"{simbolo}.csv")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("carpeta")
    ap.add_argument("--desde", default="2015-01-01")
    a = ap.parse_args(argv)
    destino = Path(a.carpeta)
    try:
        comprobar_destino(destino, CRUCES)   # T-149: antes de descargar
        series = cruces(descargar(a.desde))
    except DestinoNoValido as e:
        print(f"destino no válido, no se descarga y no se escribe nada: {e}", file=sys.stderr)
        return 1
    except RespuestaBCE as e:
        print(f"respuesta del BCE no válida, no se escribe nada: {e}", file=sys.stderr)
        return 1
    except urllib.error.HTTPError as e:
        print(f"el BCE respondió HTTP {e.code} ({e.reason}), no se escribe nada", file=sys.stderr)
        return 1
    except (urllib.error.URLError, OSError, http.client.HTTPException) as e:   # T-150 (H-06): también IncompleteRead
        print(f"no se pudo descargar del BCE ({type(e).__name__}: {e}), no se escribe nada", file=sys.stderr)
        return 1
    try:
        escribir(series, destino)
    except EscrituraIncompleta as e:   # T-150 (O-05): no se puede decir «no se escribe nada»
        print(f"no se pudo escribir en {destino} ({type(e.causa).__name__}: {e.causa}) cuando ya se habían escrito "
              f"{', '.join(e.movidos)} (de esta descarga); los demás CSV del destino no se han tocado. "
              "Repite la descarga", file=sys.stderr)
        return 1
    except OSError as e:   # T-149 (H-02): sin permiso, disco lleno…: mensaje y 1, y la carpeta temporal se borra
        print(f"no se pudo escribir en {destino} ({type(e).__name__}: {e}), no se escribe nada", file=sys.stderr)
        return 1
    for simbolo, df in series.items():
        print(f"{simbolo}: {len(df)} cierres, {df['fecha'].iloc[0]} → {df['fecha'].iloc[-1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
