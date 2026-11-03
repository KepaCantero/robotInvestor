"""HT-01 · Servicio de datos de mercado (tipos de cambio, índices de cestas y estrategias, volatilidad y tipos de
interés por divisa) con guardia anti-fuga.

Regla central: con una fecha `as_of` activa, ningún proveedor devuelve observaciones posteriores.
Pedir explícitamente datos más allá de `as_of` lanza `FugaDeInformacion`.

Formato CSV (ProveedorCSV): una carpeta con un archivo por símbolo, `<SIMBOLO>.csv`, con cabecera
`fecha,apertura,maximo,minimo,cierre,volumen` o, como mínimo, `fecha,cierre` (también se aceptan los
alias `date`, `close`, `adj close`, `valor`). Columna opcional `fecha_publicacion`: si existe, una
fila solo es visible cuando `fecha_publicacion <= as_of` (series macro publicadas con retraso o
revisadas).

Divisas: cada par se guarda con su código sin barra (`EURUSD.csv` = dólares por euro, convención BASE/COTIZADA);
las cestas y estrategias, como índices (`FX-CARRY-G10.csv`); la volatilidad implícita de un par, como serie de nivel
(`VOL-EURUSD-1M.csv`). El tipo de interés a corto plazo de cada divisa (base del carry y del forward) va en
`TIPO-<ISO>.csv` en % anual (p. ej., `TIPO-USD.csv`, `TIPO-JPY.csv`). Con esos tipos, el proveedor calcula sin
anticipación el diferencial de tipos y el carry de un par o de una composición, y el cambio que descuenta el forward.
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
    """Interfaz común. Las subsegmentos implementan `_serie_completa` y `simbolos`."""

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

    # -- tipos de interés, carry y forward (sin anticipación) ----------------------------------------
    @staticmethod
    def simbolo_tipo(divisa: str) -> str:
        return f"TIPO-{divisa}"

    def tipo_interes(self, divisa: str, fecha: Fecha) -> Tuple[pd.Timestamp, float]:
        """Último tipo a corto plazo (% anual) de la divisa conocido en `fecha` (≤ as_of)."""
        return self.valor_en(self.simbolo_tipo(divisa), fecha)

    def carry_composicion(self, composicion: Sequence[Dict], fecha: Fecha) -> Optional[float]:
        """Carry anual (% ) de una composición [{divisa, peso, lado}]: Σ peso·tipo de las largas − Σ peso·tipo de las
        cortas. None si falta algún tipo."""
        total = 0.0
        try:
            for c in composicion:
                _, t = self.tipo_interes(c["divisa"], fecha)
                total += float(c["peso"]) * t * (1 if c["lado"] == "LARGO" else -1)
        except (DatosNoDisponibles, KeyError):
            return None
        return total

    def cambio_forward(self, carry_largo_pct: Optional[float], anios: float) -> Optional[float]:
        """Variación del indicador (precio de lo largo frente a lo corto) que descuenta el forward: −carry·años (UIP)."""
        if carry_largo_pct is None:
            return None
        return -carry_largo_pct / 100.0 * anios

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


# Parámetros sintéticos por segmento: (volatilidad anual, deriva media)
PARAM_SINTETICOS = {"G10N": (0.08, 0.0), "G10M": (0.10, 0.0), "EMAS": (0.06, 0.0), "EMLA": (0.12, 0.0), "EMEA": (0.11, 0.0),
                    "ESTR": (0.07, 0.02), "TIPO": (0.0, 0.0), "VOL": (0.6, 0.0)}
# Niveles de partida orientativos (ficticios) de algunos códigos; el resto parte de 1,0 (pares) o 100 (índices)
NIVELES_SINTETICOS = {"EURUSD": 1.10, "USDJPY": 145.0, "GBPUSD": 1.28, "USDCHF": 0.88, "EURJPY": 158.0, "EURGBP": 0.86, "EURCHF": 0.96,
                      "GBPJPY": 185.0, "AUDUSD": 0.66, "NZDUSD": 0.60, "USDCAD": 1.36, "EURNOK": 11.5, "EURSEK": 11.2, "AUDNZD": 1.09,
                      "AUDJPY": 96.0, "CADJPY": 106.0, "USDCNH": 7.15, "USDINR": 84.0, "USDKRW": 1350.0, "USDTWD": 31.5,
                      "USDIDR": 15800.0, "USDSGD": 1.34, "USDTHB": 35.5, "USDHKD": 7.80, "USDMXN": 18.5, "USDBRL": 5.3,
                      "USDCLP": 920.0, "USDCOP": 4050.0, "USDPEN": 3.75, "EURPLN": 4.30, "EURHUF": 395.0, "EURCZK": 25.0,
                      "USDTRY": 34.0, "USDZAR": 18.2, "USDILS": 3.7, "USDEGP": 48.0}
# Tipos a corto plazo de partida (% anual, ficticios) por divisa
TIPOS_SINTETICOS = {"USD": 4.0, "EUR": 2.5, "JPY": 0.3, "GBP": 4.2, "CHF": 0.8, "AUD": 3.9, "NZD": 4.0, "CAD": 3.2, "NOK": 4.3,
                    "SEK": 2.8, "CNY": 1.8, "CNH": 1.9, "INR": 6.5, "KRW": 3.0, "TWD": 2.0, "IDR": 6.0, "SGD": 2.8, "THB": 2.2,
                    "HKD": 4.1, "MXN": 9.5, "BRL": 12.5, "CLP": 5.5, "COP": 9.5, "PEN": 4.8, "PLN": 5.6, "HUF": 6.5, "CZK": 3.8,
                    "TRY": 40.0, "ZAR": 7.5, "ILS": 4.5, "EGP": 25.0}


class ProveedorSintetico(ProveedorDatos):
    """Series diarias deterministas (días hábiles) de tipos de cambio, índices, volatilidades y tipos de interés.

    Pensado para pruebas: cada código depende solo de (semilla, código, segmento) y de un factor común del dólar
    y otro del segmento, de modo que añadir códigos no altera los existentes. `simbolos_segmento` asigna cada código
    a su segmento; los códigos «TIPO-<ISO>» generan tipos a corto plazo (en % anual) con cambios escalonados; los
    «VOL-…», niveles de volatilidad implícita. Los pares con el USD como cotizada (EURUSD) se mueven al revés que el
    factor del dólar y los que lo tienen como base (USDJPY), a favor.
    """

    nombre = "sintetico"

    def __init__(self, simbolos_segmento: Dict[str, str], semilla: int = 7, inicio: Fecha = "2021-01-04",
                 fin: Fecha = "2026-12-31", fijos: Optional[Dict[str, pd.DataFrame]] = None) -> None:
        super().__init__()
        self.simbolos_segmento = dict(simbolos_segmento)
        self.semilla = int(semilla)
        self.fechas = pd.bdate_range(a_fecha(inicio), a_fecha(fin))
        self._cache: Dict[str, pd.DataFrame] = {}
        self._factores: Dict[str, np.ndarray] = {}
        self._fijos = fijos or {}

    def _rng(self, *clave) -> np.random.Generator:
        h = hashlib.sha256(("|".join(map(str, (self.semilla,) + clave))).encode()).digest()
        return np.random.default_rng(int.from_bytes(h[:8], "little"))

    def _factor(self, nombre: str, vol: float, mu: float = 0.0) -> np.ndarray:
        if nombre not in self._factores:
            rng = self._rng("factor", nombre)
            n = len(self.fechas)
            deriva = np.empty(n)
            i = 0
            while i < n:   # regímenes de deriva de ~3–9 meses
                largo = int(rng.integers(60, 180))
                deriva[i:i + largo] = rng.normal(mu, max(vol * 0.8, 0.03))
                i += largo
            self._factores[nombre] = deriva / 252 + rng.standard_normal(n) * vol * 0.6 / np.sqrt(252)
        return self._factores[nombre]

    def simbolos(self) -> List[str]:
        return sorted(set(self.simbolos_segmento) | set(self._fijos))

    def _serie_completa(self, simbolo: str) -> pd.DataFrame:
        if simbolo in self._fijos:
            return self._fijos[simbolo]
        if simbolo not in self.simbolos_segmento:
            raise DatosNoDisponibles(f"HT-01 sintético: código desconocido {simbolo}")
        if simbolo not in self._cache:
            seg = self.simbolos_segmento[simbolo]
            rng = self._rng("simbolo", simbolo)
            n = len(self.fechas)
            if simbolo.startswith("TIPO-"):
                base = TIPOS_SINTETICOS.get(simbolo[5:], 3.0)
                pasos = np.zeros(n)
                for k in range(0, n, 30):   # decisiones de banco central aproximadamente mensuales: ±25 pb
                    pasos[k] = rng.choice([-0.25, 0.0, 0.0, 0.0, 0.25]) * max(base / 4.0, 0.25)
                nivel = np.maximum(base + np.cumsum(pasos), 0.0)
                df = pd.DataFrame({"cierre": nivel}, index=self.fechas)
            else:
                vol, mu = PARAM_SINTETICOS.get("VOL" if simbolo.startswith("VOL-") else seg, (0.09, 0.0))
                usd = self._factor("USD", 0.07)
                fseg = self._factor(seg, vol, mu)
                signo_usd = 1.0 if simbolo.startswith("USD") else (-1.0 if simbolo.endswith("USD") else 0.0)
                r = (0.7 * signo_usd * usd + rng.uniform(0.5, 1.0) * fseg
                     + np.repeat(rng.normal(0, vol * 0.4, size=n // 120 + 1), 120)[:n] / 252
                     + rng.standard_normal(n) * vol * 0.5 / np.sqrt(252))
                if simbolo.startswith("VOL-"):
                    nivel = 9.0 * np.exp(np.clip(np.cumsum(r) * 0.3, -1.0, 1.2))
                else:
                    nivel = NIVELES_SINTETICOS.get(simbolo, 100.0 if seg == "ESTR" else 1.0) * np.exp(np.cumsum(r))
                ruido = np.abs(rng.standard_normal(n)) * vol / np.sqrt(252) * 0.4
                df = pd.DataFrame({"apertura": nivel * (1 + rng.normal(0, vol / np.sqrt(252) * 0.2, n)),
                                   "maximo": nivel * (1 + ruido), "minimo": nivel * (1 - ruido), "cierre": nivel}, index=self.fechas)
            df.index.name = "fecha"
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


def simbolos_sinteticos(universo: pd.DataFrame) -> Dict[str, str]:
    """Códigos del universo con su segmento más una serie «TIPO-<ISO>» (segmento TIPO) por cada divisa que aparece en
    los pares o en las composiciones: lo que `generar-sinteticos` escribe y el backtest necesita para el carry."""
    out = {str(f["simbolo"]): str(f["segmento"]) for _, f in universo.iterrows()}
    divisas = set()
    for _, f in universo.iterrows():
        for k in ("base", "cotizada", "divisa_financiacion"):
            if str(f.get(k) or "").strip():
                divisas.add(str(f[k]).strip().upper())
        for c in parsear_composicion(f.get("composicion") or ""):
            divisas.add(c["divisa"])
    for d in sorted(divisas):
        out[ProveedorDatos.simbolo_tipo(d)] = "TIPO"
    return out


COLUMNAS_UNIVERSO = ["codigo", "segmento", "tipo", "base", "cotizada", "convertible", "ndf"]
# Columnas opcionales (si faltan se rellenan): composición de cestas «AUD:LARGO:0.34;JPY:CORTO:0.5», divisa de
# financiación, controles de capitales, régimen cambiario de facto, liquidez, nombre, indicador y notas
COLUMNAS_UNIVERSO_OPCIONALES = ["nombre", "composicion", "divisa_financiacion", "controles_capitales", "regimen", "liquidez",
                                "indicador", "notas"]
VERDADERO = {"si", "sí", "true", "1", "verdadero", "s", "yes"}
FALSO = {"no", "false", "0", "falso", "n", ""}


def parsear_composicion(texto: str) -> List[Dict]:
    """«AUD:LARGO:0.34;NZD:LARGO:0.33;JPY:CORTO:0.5» → [{divisa, lado, peso}]."""
    out = []
    for parte in [x.strip() for x in str(texto or "").split(";") if x.strip()]:
        d, lado, peso = [y.strip() for y in parte.split(":")]
        out.append({"divisa": d.upper(), "peso": float(peso), "lado": lado.upper()})
    return out


def cargar_universo(ruta: Union[str, Path]) -> pd.DataFrame:
    """Universo de ámbitos cambiarios del Bloque A Forex (Documento 0 Forex, 2.4–2.6).

    Cada fila es un ámbito (par, cruce, cesta, bloque, estrategia, volatilidad o régimen) de un segmento, y `codigo` es
    la serie HT-01 de su indicador de seguimiento (con la que se miden la tendencia y los pronósticos), no un
    instrumento. Columnas obligatorias `codigo,segmento,tipo,base,cotizada,convertible,ndf` y opcionales
    `nombre,composicion,divisa_financiacion,controles_capitales,regimen,liquidez,indicador,notas`. En los pares,
    `base` y `cotizada` son códigos ISO 4217 en convención de mercado; en las cestas, bloques y estrategias `base`
    va vacía, `cotizada` es la divisa de referencia y `composicion` declara divisas, lados y pesos. La columna
    `simbolo` se añade como alias de `codigo` para el resto del ejecutor."""
    from ..configuracion import SEGMENTOS, TIPOS_CESTA, TIPOS_OPCION
    df = pd.read_csv(ruta, dtype=str).fillna("")
    falta = [c for c in COLUMNAS_UNIVERSO if c not in df.columns]
    if falta:
        raise ValueError(f"Universo: faltan columnas {falta}")
    for c in COLUMNAS_UNIVERSO_OPCIONALES:
        if c not in df.columns:
            df[c] = ""
    malas = sorted(set(df["segmento"]) - set(SEGMENTOS))
    if malas:
        raise ValueError(f"Universo: segmentos desconocidos {malas} (válidos: {', '.join(SEGMENTOS)})")
    if df["codigo"].duplicated().any():
        raise ValueError("Universo: códigos duplicados")
    df["tipo"] = df["tipo"].str.strip().str.upper()
    malos = sorted(set(df["tipo"]) - set(TIPOS_OPCION))
    if malos:
        raise ValueError(f"Universo: tipo no permitido {malos} (válidos: {', '.join(TIPOS_OPCION)})")
    for c in ("convertible", "ndf", "controles_capitales"):
        v = df[c].str.strip().str.lower()
        if not v.isin(VERDADERO | FALSO).all():
            raise ValueError(f"Universo: valores no booleanos en {c}")
        df[c] = v.isin(VERDADERO)
    for _, f in df.iterrows():
        for col in ("base", "cotizada", "divisa_financiacion"):
            if f[col] and (len(f[col]) != 3 or not f[col].isupper()):
                raise ValueError(f"Universo: {f['codigo']}: {col} {f[col]!r} no es un código ISO 4217")
        if f["tipo"] in TIPOS_CESTA:
            comp = parsear_composicion(f["composicion"])
            if len(comp) < 2:
                raise ValueError(f"Universo: {f['codigo']}: {f['tipo']} sin composición")
        elif not (f["base"] and f["cotizada"]) and f["tipo"] != "VOLATILIDAD":
            raise ValueError(f"Universo: {f['codigo']}: {f['tipo']} exige base y cotizada")
    df["liquidez"] = df["liquidez"].replace("", "alta")
    df["simbolo"] = df["codigo"]
    return df[["simbolo"] + COLUMNAS_UNIVERSO + COLUMNAS_UNIVERSO_OPCIONALES]
