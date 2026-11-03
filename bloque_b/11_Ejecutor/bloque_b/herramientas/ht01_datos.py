"""HT-01 · Servicio de datos de mercado del Bloque B con guardia anti-fuga (sin anticipación) y bóveda de credenciales.

Adaptado del HT-01 del ejecutor del Bloque A V5.0. La bóveda simulada está en `boveda.py`.

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
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union

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


def a_fecha(f: Optional[Fecha]) -> Optional[pd.Timestamp]:
    if f is None:
        return None
    return pd.Timestamp(f).normalize()


class ProveedorDatos:
    """Interfaz común. Las subclases implementan `_serie_completa` y `simbolos`."""

    nombre = "base"

    def __init__(self) -> None:
        self._as_of: Optional[pd.Timestamp] = None
        self._lock = threading.Lock()
        self.registro_peticiones: List[Dict] = []   # auditoría de lo pedido (pruebas anti-fuga)

    # -- fecha activa -------------------------------------------------------------------------
    def fijar_as_of(self, fecha: Fecha) -> None:
        self._as_of = a_fecha(fecha)

    @property
    def as_of(self) -> Optional[pd.Timestamp]:
        return self._as_of

    # -- a implementar ------------------------------------------------------------------------
    def simbolos(self) -> List[str]:
        raise NotImplementedError

    def _serie_completa(self, simbolo: str) -> pd.DataFrame:
        raise NotImplementedError

    # -- API pública --------------------------------------------------------------------------
    def tiene(self, simbolo: str) -> bool:
        return simbolo in set(self.simbolos())

    def serie(self, simbolo: str, inicio: Optional[Fecha] = None, fin: Optional[Fecha] = None) -> pd.DataFrame:
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
            pub = pd.to_datetime(df["fecha_publicacion"], errors="coerce")
            df = df[(pub.isna()) | (pub <= self._as_of)]
        if len(df) and df.index.max() > self._as_of:  # defensa en profundidad
            raise FugaDeInformacion("HT-01: el proveedor devolvió datos posteriores a as_of")
        return df.copy()

    def cierres(self, simbolo: str, inicio: Optional[Fecha] = None, fin: Optional[Fecha] = None) -> pd.Series:
        df = self.serie(simbolo, inicio, fin)
        if df.empty:
            raise DatosNoDisponibles(f"HT-01: sin datos de {simbolo} en el rango")
        return df["cierre"].astype(float)

    def valor_en(self, simbolo: str, fecha: Fecha) -> Tuple[pd.Timestamp, float]:
        """Último cierre con fecha <= `fecha` (que debe ser <= as_of)."""
        s = self.cierres(simbolo, None, fecha)
        return s.index[-1], float(s.iloc[-1])

    def ultima_fecha(self, simbolo: str) -> Optional[pd.Timestamp]:
        try:
            s = self.cierres(simbolo)
        except DatosNoDisponibles:
            return None
        return s.index[-1]

    def huella(self, simbolo: str, inicio: Optional[Fecha] = None, fin: Optional[Fecha] = None) -> str:
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
    if "fecha" not in df.columns or "cierre" not in df.columns:
        raise ValueError(f"{origen}: el CSV necesita al menos las columnas fecha y cierre")
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.normalize()
    df = df.dropna(subset=["cierre"]).sort_values("fecha")
    if df["fecha"].duplicated().any():
        raise ValueError(f"{origen}: fechas duplicadas")
    df = df.set_index("fecha")
    for c in ("apertura", "maximo", "minimo", "cierre", "volumen"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    keep = [c for c in ("apertura", "maximo", "minimo", "cierre", "volumen", "fecha_publicacion") if c in df.columns]
    return df[keep]


class ProveedorCSV(ProveedorDatos):
    nombre = "csv"

    def __init__(self, carpeta: Union[str, Path]) -> None:
        super().__init__()
        self.carpeta = Path(carpeta)
        if not self.carpeta.is_dir():
            raise FileNotFoundError(f"HT-01: no existe la carpeta de datos {self.carpeta}")
        self._cache: Dict[str, pd.DataFrame] = {}

    def simbolos(self) -> List[str]:
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
    """Series diarias deterministas (días hábiles) con factor común por grupo («TIPO:ámbito») y regímenes de deriva.

    Pensado para pruebas: cada símbolo depende solo de (semilla, símbolo, clase) y de los factores de
    su clase, de modo que añadir símbolos no altera los existentes.
    """

    nombre = "sintetico"

    def __init__(self, simbolos_clase: Dict[str, str], semilla: int = 7, inicio: Fecha = "2021-01-04",
                 fin: Fecha = "2026-12-31", fijos: Optional[Dict[str, pd.DataFrame]] = None,
                 bajas: Optional[Dict[str, str]] = None, altas: Optional[Dict[str, str]] = None) -> None:
        super().__init__()
        self.simbolos_clase = dict(simbolos_clase)
        self.semilla = int(semilla)
        self.fechas = pd.bdate_range(a_fecha(inicio), a_fecha(fin))
        self._cache: Dict[str, pd.DataFrame] = {}
        self._factores: Dict[str, np.ndarray] = {}
        self._fijos = fijos or {}
        self._bajas = {k: a_fecha(v) for k, v in (bajas or {}).items() if v}
        self._altas = {k: a_fecha(v) for k, v in (altas or {}).items() if v}

    def _rng(self, *clave) -> np.random.Generator:
        h = hashlib.sha256(("|".join(map(str, (self.semilla,) + clave))).encode()).digest()
        return np.random.default_rng(int.from_bytes(h[:8], "little"))

    def _factor(self, clase: str) -> np.ndarray:
        if clase not in self._factores:
            vol, mu, _ = PARAM_SINTETICOS.get(clase.split(":")[0], (0.15, 0.03, 100.0))
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

    def simbolos(self) -> List[str]:
        return sorted(set(self.simbolos_clase) | set(self._fijos))

    def _serie_completa(self, simbolo: str) -> pd.DataFrame:
        if simbolo in self._fijos:
            return self._fijos[simbolo]
        if simbolo not in self.simbolos_clase:
            raise DatosNoDisponibles(f"HT-01 sintético: símbolo desconocido {simbolo}")
        if simbolo not in self._cache:
            clase = self.simbolos_clase[simbolo]
            vol, mu, nivel = PARAM_SINTETICOS.get(clase.split(":")[0], (0.15, 0.03, 100.0))
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
            if simbolo in self._bajas:      # valor deslistado: la serie termina en su fecha de baja
                df = df[df.index < self._bajas[simbolo]]
            if simbolo in self._altas:
                df = df[df.index >= self._altas[simbolo]]
            self._cache[simbolo] = df.round(6)
        return self._cache[simbolo]

    def escribir_csv(self, carpeta: Union[str, Path], simbolos: Optional[Iterable[str]] = None) -> List[Path]:
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
        self._cache: Dict[str, pd.DataFrame] = {}

    def simbolos(self) -> List[str]:
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


