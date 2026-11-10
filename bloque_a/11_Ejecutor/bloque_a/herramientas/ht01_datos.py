"""HT-01 · Servicio de datos de mercado con guardia anti-fuga.

Regla central: con una fecha `as_of` activa, ningún proveedor devuelve observaciones posteriores.
Pedir explícitamente datos más allá de `as_of` lanza `FugaDeInformacion`.

Formato CSV (ProveedorCSV): una carpeta con un archivo por símbolo, `<SIMBOLO>.csv`, con cabecera
`fecha,apertura,maximo,minimo,cierre,volumen` o, como mínimo, `fecha,cierre` (también se aceptan los
alias `date`, `close`, `adj close`, `valor`). Columna opcional `fecha_publicacion`: si existe, una
fila solo es visible cuando `fecha_publicacion <= as_of` (series macro publicadas con retraso o
revisadas). Las series adicionales (tipos, curvas, inventarios…) usan el mismo formato con símbolos
propios (p. ej., `TIPO_USD_3M.csv`).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import threading
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

Fecha = Union[str, dt.date, pd.Timestamp]

ALIAS_COLUMNAS = {
    "fecha": "fecha", "date": "fecha", "datetime": "fecha",
    "apertura": "apertura", "open": "apertura",
    "maximo": "maximo", "máximo": "maximo", "high": "maximo",
    "minimo": "minimo", "mínimo": "minimo", "low": "minimo",
    "cierre": "cierre", "close": "cierre", "adj close": "cierre", "adj_close": "cierre", "valor": "cierre", "value": "cierre",
    "volumen": "volumen", "volume": "volumen",
    "fecha_publicacion": "fecha_publicacion", "fecha_publicación": "fecha_publicacion",
}


class FugaDeInformacion(RuntimeError):
    """Se ha pedido una observación posterior a la fecha as_of activa."""


class DatosNoDisponibles(KeyError):
    """El símbolo no existe en el proveedor o no tiene datos en el rango."""


class DatosInvalidos(DatosNoDisponibles):
    """La serie trae valores que no se pueden interpretar (p. ej., un cierre `-`, `n.d.` o `1.234,5`).

    Falla cerrado: la serie se rechaza entera y se trata como no disponible (nunca se rellena ni se
    convierte en un valor inventado). Es subclase de `DatosNoDisponibles` para que los llamadores que ya
    tratan la falta de datos (espera, `NO_RESOLUBLE`, símbolo excluido de una cesta) la traten igual."""


def _fechas_publicacion(col: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Interpreta `fecha_publicacion` en ISO 8601. Devuelve (fechas, inválidas): una celda vacía es «sin
    retraso de publicación» (NaT, visible); una celda no vacía que no se interpreta (p. ej., `31/06/2026`)
    es inválida y su fila no debe ser visible nunca."""
    if pd.api.types.is_datetime64_any_dtype(col):
        return col.dt.normalize(), pd.Series(False, index=col.index)
    texto = col.astype("string").str.strip()
    vacia = (texto.isna() | (texto == "")).fillna(True).astype(bool)
    fechas = pd.to_datetime(texto.where(~vacia), errors="coerce", format="ISO8601")
    return fechas.dt.normalize(), (~vacia) & fechas.isna()


def a_fecha(f: Fecha | None) -> pd.Timestamp | None:
    if f is None:
        return None
    return pd.Timestamp(f).normalize()


class ProveedorDatos:
    """Interfaz común. Las subclases implementan `_serie_completa` y `simbolos`."""

    nombre = "base"

    def __init__(self) -> None:
        self._as_of: pd.Timestamp | None = None
        self._lock = threading.Lock()
        self.registro_peticiones: list[dict] = []   # auditoría de lo pedido (pruebas anti-fuga)

    # -- fecha activa -------------------------------------------------------------------------
    def fijar_as_of(self, fecha: Fecha) -> None:
        self._as_of = a_fecha(fecha)

    @property
    def as_of(self) -> pd.Timestamp | None:
        return self._as_of

    # -- a implementar ------------------------------------------------------------------------
    def simbolos(self) -> list[str]:
        raise NotImplementedError

    def _serie_completa(self, simbolo: str) -> pd.DataFrame:
        raise NotImplementedError

    # -- API pública --------------------------------------------------------------------------
    def tiene(self, simbolo: str) -> bool:
        return simbolo in set(self.simbolos())

    def serie(self, simbolo: str, inicio: Fecha | None = None, fin: Fecha | None = None) -> pd.DataFrame:
        """Observaciones de `simbolo` entre `inicio` y `fin` (inclusive), nunca posteriores a as_of."""
        if self._as_of is None:
            raise RuntimeError("HT-01: fije la fecha as_of (fijar_as_of) antes de pedir datos")
        fin_ts = a_fecha(fin) if fin is not None else self._as_of
        if fin_ts > self._as_of:
            raise FugaDeInformacion(
                f"HT-01: se pidió {simbolo} hasta {fin_ts.date()} con as_of {self._as_of.date()} (fuga de información)")
        ini_ts = a_fecha(inicio)
        with self._lock:
            self.registro_peticiones.append({"simbolo": simbolo, "inicio": None if ini_ts is None else str(ini_ts.date()),
                                             "fin": str(fin_ts.date()), "as_of": str(self._as_of.date())})
        df = self._serie_completa(simbolo)
        df = df[df.index <= fin_ts]
        if ini_ts is not None:
            df = df[df.index >= ini_ts]
        if "fecha_publicacion" in df.columns:
            # Una fecha de publicación no interpretable no se da por publicada (falla cerrado)
            pub, invalida = _fechas_publicacion(df["fecha_publicacion"])
            df = df[~invalida & (pub.isna() | (pub <= self._as_of))]
        if len(df) and df.index.max() > self._as_of:  # defensa en profundidad
            raise FugaDeInformacion("HT-01: el proveedor devolvió datos posteriores a as_of")
        return df.copy()

    def cierres(self, simbolo: str, inicio: Fecha | None = None, fin: Fecha | None = None) -> pd.Series:
        df = self.serie(simbolo, inicio, fin)
        if df.empty:
            raise DatosNoDisponibles(f"HT-01: sin datos de {simbolo} en el rango")
        s = df["cierre"].astype(float)
        # T-65 (QA de T-53, H-15): las rentabilidades se calculan como cociente de niveles; un cierre ≤ 0 (o no finito)
        # no es un precio válido y nunca se convierte en una cifra: la serie se rechaza en el rango pedido
        malos = ~np.isfinite(s.to_numpy()) | (s.to_numpy() <= 0)
        if malos.any():
            ej = [f"{f.date()}={v!r}" for f, v in zip(s.index[malos][:3], s.to_numpy()[malos][:3])]
            raise DatosInvalidos(f"HT-01: {int(malos.sum())} cierres no positivos o no finitos de {simbolo} "
                                 f"(p. ej., {', '.join(ej)}); serie rechazada")
        return s

    def valor_en(self, simbolo: str, fecha: Fecha) -> tuple[pd.Timestamp, float]:
        """Último cierre con fecha <= `fecha` (que debe ser <= as_of)."""
        s = self.cierres(simbolo, None, fecha)
        return s.index[-1], float(s.iloc[-1])

    def ultima_fecha(self, simbolo: str) -> pd.Timestamp | None:
        try:
            s = self.cierres(simbolo)
        except DatosNoDisponibles:
            return None
        return s.index[-1]

    def huella(self, simbolo: str, inicio: Fecha | None = None, fin: Fecha | None = None) -> str:
        """Hash de los datos efectivos (linaje del artefacto del Motor)."""
        s = self.cierres(simbolo, inicio, fin)
        h = hashlib.sha256()
        h.update(simbolo.encode())
        h.update(np.ascontiguousarray(s.values.astype("float64")).tobytes())
        h.update(",".join(str(d.date()) for d in s.index[[0, -1]]).encode())
        return h.hexdigest()[:16]


def _normalizar_df(df: pd.DataFrame, origen: str) -> pd.DataFrame:
    cols = {}
    for c in df.columns:
        k = ALIAS_COLUMNAS.get(str(c).strip().lower())
        if k:
            cols[c] = k
    df = df.rename(columns=cols)
    # T-65 (H-15): un CSV mal formado es un dato inválido del símbolo (DatosInvalidos, que los llamadores tratan como falta
    # de datos: el símbolo se excluye y se declara), no un error que tumbe el ciclo
    if "fecha" not in df.columns or "cierre" not in df.columns:
        raise DatosInvalidos(f"{origen}: el CSV necesita al menos las columnas fecha y cierre")
    try:
        df["fecha"] = pd.to_datetime(df["fecha"]).dt.normalize()
    except (ValueError, TypeError) as e:
        raise DatosInvalidos(f"HT-01 {origen}: fechas no interpretables ({str(e).splitlines()[0][:120]}); serie rechazada") from e
    # Conversión a número ANTES de eliminar filas: un cierre no vacío que no es un número finito
    # (`-`, `n.d.`, `1.234,5`, `inf`) invalida la serie entera; nunca se convierte en NaN silencioso.
    crudo = df["cierre"]
    vacio = (crudo.isna() | (crudo.astype("string").str.strip() == "")).fillna(True).astype(bool)
    num = pd.to_numeric(crudo.where(~vacio), errors="coerce").astype(float)
    malos = ~vacio & ~np.isfinite(num)          # NaN tras convertir una celda no vacía, o ±inf
    if malos.any():
        ej = [f"{f.date()}={v!r}" for f, v in zip(df.loc[malos, "fecha"].head(3), crudo[malos].head(3))]
        raise DatosInvalidos(f"HT-01 {origen}: {int(malos.sum())} cierres no numéricos o no finitos (p. ej., {', '.join(ej)}); "
                             "serie rechazada")
    df["cierre"] = num
    # Fechas de publicación: las filas con una fecha no interpretable se rechazan (no se dan por publicadas)
    descartadas: list[str] = []
    if "fecha_publicacion" in df.columns:
        pub, invalida = _fechas_publicacion(df["fecha_publicacion"])
        descartadas += [f"{f.date()}: fecha_publicacion no interpretable" for f in df.loc[invalida, "fecha"]]
        df["fecha_publicacion"] = pub
        df = df[~invalida]
    # Filas sin cierre (celda vacía): se eliminan y se declaran
    descartadas += [f"{f.date()}: cierre vacío" for f in df.loc[df["cierre"].isna(), "fecha"]]
    df = df.dropna(subset=["cierre"]).sort_values("fecha")
    if df["fecha"].duplicated().any():   # T-65 (H-15): dato inválido del símbolo, no un error del ciclo
        dup = sorted({str(f.date()) for f in df.loc[df["fecha"].duplicated(), "fecha"]})[:3]
        raise DatosInvalidos(f"HT-01 {origen}: fechas duplicadas ({', '.join(dup)}); serie rechazada")
    df = df.set_index("fecha")
    for c in ("apertura", "maximo", "minimo", "volumen"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    keep = [c for c in ("apertura", "maximo", "minimo", "cierre", "volumen", "fecha_publicacion") if c in df.columns]
    out = df[keep]
    out.attrs["filas_descartadas"] = descartadas
    return out


class ProveedorCSV(ProveedorDatos):
    nombre = "csv"

    def __init__(self, carpeta: str | Path) -> None:
        super().__init__()
        self.carpeta = Path(carpeta)
        if not self.carpeta.is_dir():
            raise FileNotFoundError(f"HT-01: no existe la carpeta de datos {self.carpeta}")
        self._cache: dict[str, pd.DataFrame] = {}

    def simbolos(self) -> list[str]:
        return sorted(p.stem for p in self.carpeta.glob("*.csv"))

    def _serie_completa(self, simbolo: str) -> pd.DataFrame:
        if simbolo not in self._cache:
            ruta = self.carpeta / f"{simbolo}.csv"
            if not ruta.exists():
                raise DatosNoDisponibles(f"HT-01: no hay archivo {ruta.name}")
            self._cache[simbolo] = _normalizar_df(pd.read_csv(ruta), ruta.name)
        return self._cache[simbolo]


PARAM_SINTETICOS = {   # (volatilidad anual, deriva media, nivel de partida) por tipo de activo
    "RV": (0.18, 0.07, 100.0), "RF": (0.06, 0.02, 100.0), "DIV": (0.08, 0.0, 1.2), "MP": (0.24, 0.03, 50.0),
    "IDX": (0.16, 0.06, 4000.0), "FON": (0.09, 0.04, 30.0), "DER": (0.12, 0.05, 2000.0),
    "INM": (0.20, 0.04, 80.0), "CRI": (0.65, 0.20, 20000.0), "ALT": (0.15, 0.05, 15.0),
    "MON": (0.005, 0.03, 100.0), "TCV": (0.40, 0.0, 20.0),
}


class ProveedorSintetico(ProveedorDatos):
    """Series diarias deterministas (días hábiles) con factor común por clase y regímenes de deriva.

    Pensado para pruebas: cada símbolo depende solo de (semilla, símbolo, clase) y de los factores de
    su clase, de modo que añadir símbolos no altera los existentes.
    """

    nombre = "sintetico"

    def __init__(self, simbolos_clase: dict[str, str], semilla: int = 7, inicio: Fecha = "2021-01-04",
                 fin: Fecha = "2026-12-31", fijos: dict[str, pd.DataFrame] | None = None) -> None:
        super().__init__()
        self.simbolos_clase = dict(simbolos_clase)
        self.semilla = int(semilla)
        self.fechas = pd.bdate_range(a_fecha(inicio), a_fecha(fin))
        self._cache: dict[str, pd.DataFrame] = {}
        self._factores: dict[str, np.ndarray] = {}
        self._fijos = fijos or {}

    def _rng(self, *clave) -> np.random.Generator:
        h = hashlib.sha256(("|".join(map(str, (self.semilla,) + clave))).encode()).digest()
        return np.random.default_rng(int.from_bytes(h[:8], "little"))

    def _factor(self, clase: str) -> np.ndarray:
        if clase not in self._factores:
            vol, mu, _ = PARAM_SINTETICOS.get(clase, (0.15, 0.03, 100.0))
            rng = self._rng("factor", clase)
            n = len(self.fechas)
            # regímenes de deriva de ~6 meses
            deriva = np.empty(n)
            i = 0
            while i < n:
                largo = int(rng.integers(60, 180))
                deriva[i:i + largo] = rng.normal(mu, max(vol * 0.8, 0.05))
                i += largo
            self._factores[clase] = deriva / 252 + rng.standard_normal(n) * vol * 0.7 / np.sqrt(252)
        return self._factores[clase]

    def simbolos(self) -> list[str]:
        return sorted(set(self.simbolos_clase) | set(self._fijos))

    def _serie_completa(self, simbolo: str) -> pd.DataFrame:
        if simbolo in self._fijos:
            return self._fijos[simbolo]
        if simbolo not in self.simbolos_clase:
            raise DatosNoDisponibles(f"HT-01 sintético: símbolo desconocido {simbolo}")
        if simbolo not in self._cache:
            clase = self.simbolos_clase[simbolo]
            vol, mu, nivel = PARAM_SINTETICOS.get(clase, (0.15, 0.03, 100.0))
            rng = self._rng("simbolo", simbolo)
            n = len(self.fechas)
            beta = rng.uniform(0.6, 1.2)
            deriva_propia = np.repeat(rng.normal(0, vol * 0.5, size=n // 120 + 1), 120)[:n] / 252
            r = beta * self._factor(clase) + deriva_propia + rng.standard_normal(n) * vol * 0.6 / np.sqrt(252)
            precio = nivel * rng.uniform(0.6, 1.6) * np.exp(np.cumsum(r))
            ruido = np.abs(rng.standard_normal(n)) * vol / np.sqrt(252) * 0.5
            df = pd.DataFrame({
                "apertura": precio * (1 + rng.normal(0, vol / np.sqrt(252) * 0.2, n)),
                "maximo": precio * (1 + ruido), "minimo": precio * (1 - ruido), "cierre": precio,
                "volumen": rng.integers(200_000, 5_000_000, n).astype(float),
            }, index=self.fechas)
            df.index.name = "fecha"
            self._cache[simbolo] = df.round(6)
        return self._cache[simbolo]

    def escribir_csv(self, carpeta: str | Path, simbolos: Iterable[str] | None = None) -> list[Path]:
        carpeta = Path(carpeta)
        carpeta.mkdir(parents=True, exist_ok=True)
        out = []
        for s in simbolos or self.simbolos():
            df = self._serie_completa(s).copy()
            df.index = df.index.strftime("%Y-%m-%d")
            p = carpeta / f"{s}.csv"
            df.to_csv(p, index_label="fecha", float_format="%.6f")
            out.append(p)
        return out


class ProveedorYahoo(ProveedorDatos):
    """Proveedor opcional (yfinance) SOLO para modo vivo. Requiere `pip install yfinance` y red."""

    nombre = "yahoo"

    def __init__(self, simbolos: Sequence[str], modo: str = "vivo", inicio: Fecha = "2015-01-01") -> None:
        super().__init__()
        if modo != "vivo":
            raise RuntimeError("ProveedorYahoo solo se admite en modo vivo (en backtest use datos congelados en CSV)")
        try:
            import yfinance  # noqa: F401
        except ImportError as e:  # pragma: no cover - dependencia opcional
            raise RuntimeError("ProveedorYahoo requiere el paquete opcional yfinance") from e
        self._lista = list(simbolos)
        self._inicio = inicio
        self._cache: dict[str, pd.DataFrame] = {}

    def simbolos(self) -> list[str]:
        return list(self._lista)

    def _serie_completa(self, simbolo: str) -> pd.DataFrame:  # pragma: no cover - requiere red
        if simbolo not in self._cache:
            import yfinance as yf
            df = yf.Ticker(simbolo).history(start=str(self._inicio), auto_adjust=True)
            if df.empty:
                raise DatosNoDisponibles(f"Yahoo: sin datos de {simbolo}")
            df = df.reset_index().rename(columns={"Date": "fecha"})
            df["fecha"] = pd.to_datetime(df["fecha"]).dt.tz_localize(None)
            self._cache[simbolo] = _normalizar_df(df, simbolo)
        return self._cache[simbolo]


COLUMNAS_UNIVERSO = ["simbolo", "clase", "nombre", "tipo_opcion", "region", "sector", "divisa", "notas"]
# Columnas opcionales V5.0 (si faltan se rellenan vacías): delimitación del ámbito e indicador de seguimiento
COLUMNAS_UNIVERSO_OPCIONALES = ["subtipo", "ambito_incluye", "ambito_excluye", "indicador", "subyacente"]


def cargar_universo(ruta: str | Path) -> pd.DataFrame:
    """Universo de ámbitos con su indicador de seguimiento (Documento 0 V5.0, 2.4–2.6).

    Columnas obligatorias `simbolo,clase,nombre,tipo_opcion,region,sector,divisa,notas` y opcionales
    `subtipo,ambito_incluye,ambito_excluye,indicador,subyacente`. Cada fila es un ÁMBITO (mercado, sector,
    subsector, temática, segmento, factor, estilo o estrategia) de un tipo de activo, y `simbolo` es la serie HT-01
    de su indicador de seguimiento (con la que se miden la tendencia y los pronósticos), no un activo propuesto.
    Compatibilidad V4.x: `tipo_opcion` INSTRUMENTO_GENERICO se lee como SEGMENTO e INDUSTRIA como SUBSECTOR."""
    from ..configuracion import CLASES, TIPOS_OPCION, TIPOS_OPCION_RETIRADOS
    df = pd.read_csv(ruta, dtype=str).fillna("")
    falta = [c for c in COLUMNAS_UNIVERSO if c not in df.columns]
    if falta:
        raise ValueError(f"Universo: faltan columnas {falta}")
    for c in COLUMNAS_UNIVERSO_OPCIONALES:
        if c not in df.columns:
            df[c] = ""
    malas = sorted(set(df["clase"]) - set(CLASES))
    if malas:
        raise ValueError(f"Universo: tipos de activo desconocidos {malas} (válidos: {', '.join(CLASES)})")
    if df["simbolo"].duplicated().any():
        raise ValueError("Universo: símbolos duplicados")
    df["tipo_opcion"] = df["tipo_opcion"].str.strip().str.upper().replace(TIPOS_OPCION_RETIRADOS)
    malos = sorted(set(df["tipo_opcion"]) - set(TIPOS_OPCION))
    if malos:
        raise ValueError(f"Universo: tipo_opcion no permitido {malos} (válidos: {', '.join(TIPOS_OPCION)})")
    return df[COLUMNAS_UNIVERSO + COLUMNAS_UNIVERSO_OPCIONALES]
