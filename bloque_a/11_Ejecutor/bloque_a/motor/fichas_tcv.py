"""Fichas V5.0 de la familia TCV (tipos de interés, crédito y volatilidad) del Motor del Bloque A.

Fuente de verdad: «Catálogo de cálculos del Motor - V5.0», sección 19 (TCV-SLOPE-001, TCV-BEI-001, TCV-CDS-001,
TCV-VIXTS-001, TCV-TP-001) y sección 3 (convenciones). Ticket T-106 (Motor Fase 1).

Convenciones comunes (Catálogo 3.1) que se aplican aquí:
- rendimientos y tipos en % anual con capitalización compuesta (anual) salvo que la ficha diga otra cosa;
- recuento de días Real/365 para pasar fechas a años (``DIAS_POR_ANIO``);
- determinista: sin semillas ni aleatoriedad (todas las fichas TCV declaran semilla ``null``);
- falla cerrado: una entrada que falta o es incoherente lanza ``ErrorFicha`` con el motivo; nunca se devuelve
  un 0 ni un valor inventado. Cuando una salida opcional no se puede calcular sin extrapolar o sin un dato que el
  solicitante no aporta, se entrega ``None`` y se declara la limitación;
- el redondeo de entrega (banquero, 4 decimales) se deja a la capa de servicio: aquí no se redondea.

Las «Supuestos y limitaciones» de cada ficha son advertencias obligatorias de entrega (Catálogo 2, campo 8): se
devuelven siempre en la lista de limitaciones.

Interfaz de cada manejador: ``f(ent, params) -> (resultado, limitaciones)``, con
``ent = {"valores": {...}, "series": {alias: pd.Series}, "series_rol": {rol: pd.Series}}`` y ``params`` los
parámetros de la petición (se aplican encima de ``PARAMETROS_POR_DEFECTO`` de la ficha).
"""
from __future__ import annotations

import functools
import itertools
import math
import re
from collections.abc import Callable
from datetime import date, datetime
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from .operaciones import ErrorFicha

Resultado = tuple[dict[str, Any], list[str]]

# ------------------------------------------------------------------ conversiones de unidades (no son parámetros)
PB_POR_PUNTO = 100        # 1 punto porcentual = 100 pb (definición del punto básico)
PB_POR_UNIDAD = 10_000    # 1 (en tanto por uno) = 10 000 pb
PCT = 100                 # tanto por uno → %
MESES_POR_ANIO = 12
DIAS_POR_ANIO = 365       # Catálogo 3.1: recuento de días Real/365

# ------------------------------------------------------------------ parámetros por defecto (campo «Parámetros»)
# Solo los parámetros que la ficha declara como tales: la petición puede cambiarlos dentro de su rango (se validan en
# `_VALIDADORES`). Los umbrales de rechazo y las constantes del método están en `UMBRALES` y no se pueden cambiar.
PARAMETROS_POR_DEFECTO: dict[str, dict[str, Any]] = {
    # TCV-SLOPE-001 · «Parámetros»: tramos (2s10s); regresores (los indicados); ventana (20 años);
    # horizonte_carry (3 meses; rango 1–12 de delta_t en FIR-CARRY-001). El IC usa el nivel por defecto de
    # ST-INF-001 (nivel 0,05) y, sin `rezagos_hac`, los rezagos HAC siguen la regla de Newey-West de ACC-FACT-001.
    "TCV-SLOPE-001": {
        "tramos": "2s10s",
        "regresores": ["cambio_esperado_tipo_oficial_1a", "brecha_actividad", "inflacion_subyacente", "prima_plazo"],
        "ventana": 20,
        "horizonte_carry": 3,
        "alfa_ic": 0.05,
        "rezagos_hac": None,
    },
    # TCV-BEI-001 · «Parámetros»: plazos (2, 5, 10 años; 5y5y); ajuste_estacional (true para < 3 años).
    "TCV-BEI-001": {
        "plazos": [2, 5, 10],
        "forward": [5, 5],
        "ajuste_estacional": True,
    },
    # TCV-CDS-001 · «Parámetros»: recuperacion (0,40 IG; 0,25–0,40 HY); fuente_impagos (declarada);
    # ventana (≥ 10 años; 5 con limitación).
    "TCV-CDS-001": {
        "recuperacion": None,
        "fuente_impagos": None,
        "ventana": 10,
    },
    # TCV-VIXTS-001 · «Parámetros»: vencimiento_constante (30 días); ventana_percentil (5 años). El ES de la
    # exposición corta usa el nivel del método histórico de RISK-VAR-001 (nivel 0,975; rango 0,90–0,99).
    "TCV-VIXTS-001": {
        "vencimiento_constante": 30,
        "ventana_percentil": 5,
        "nivel_es": 0.975,
    },
    # TCV-TP-001 · «Parámetros»: n_factores (5; 3–5); metodo (ACM; publicado; encuesta); ventana (toda la disponible).
    "TCV-TP-001": {
        "n_factores": 5,
        "metodo": "ACM",
        "ventana": None,
    },
}

# Umbrales y constantes del método (no son parámetros de la petición; cada uno cita su campo de la ficha).
UMBRALES: dict[str, dict[str, Any]] = {
    # TCV-SLOPE-001 · «Método (iii)»: forward a 3 y 6 meses. «Aclaración y rechazo»: < 6 nodos o < 5 años.
    # «Entradas mínimas»: ≥ 10 años. FIR-CARRY-001: delta_t en 1–12 meses.
    "TCV-SLOPE-001": {"horizontes_forward": [3, 6], "nodos_minimos": 6, "anios_minimos": 5,
                      "anios_entrada_minima": 10, "rango_horizonte_carry": [1, 12]},
    # TCV-BEI-001 · «Parámetros»: ajuste estacional para < 3 años. «Aclaración y rechazo»: < 3 vencimientos reales.
    # «Método (vi)»: percentil frente a ≥ 10 años.
    "TCV-BEI-001": {"plazo_ajuste_estacional": 3, "vencimientos_reales_minimos": 3, "anios_percentil": 10},
    # TCV-CDS-001 · «Parámetros»: recuperación 0,40 IG y 0,25–0,40 HY. «Aclaración y rechazo»: < 5 años.
    # «Método (vi)»: pendiente 5–10 años. «Salidas»: carry en pb anuales (horizonte de 1 año).
    "TCV-CDS-001": {"recuperacion_ig": 0.40, "recuperacion_hy": [0.25, 0.40], "anios_minimos": 5,
                    "plazos_pendiente": [5, 10], "horizonte_carry_anios": 1},
    # TCV-VIXTS-001 · «Aclaración y rechazo»: < 2 vencimientos. «Entradas mínimas»: ≥ 3 años. RISK-VAR-001:
    # ≥ 250 observaciones para el método histórico y nivel en 0,90–0,99.
    "TCV-VIXTS-001": {"vencimientos_minimos": 2, "anios_minimos": 3, "observaciones_minimas_es": 250,
                      "rango_nivel_es": [0.90, 0.99]},
    # TCV-TP-001 · «Parámetros»: n_factores 3–5. «Método (ii)»: prima a 2, 5 y 10 años. «Entradas mínimas»: curva
    # mensual ≥ 20 años (≥ 10 con limitación) con vencimientos de 1 a 10 años. «Verificación»: error de ajuste
    # < 5 pb. «Aclaración y rechazo»: < 10 años. «Tolerancias y semilla»: 1e-6 · semilla null.
    "TCV-TP-001": {"rango_n_factores": [3, 5], "plazos_prima": [2, 5, 10], "anios_minimos": 10,
                   "anios_entrada_minima": 20, "plazo_minimo_meses": 1, "plazo_maximo_anios": 10,
                   "error_ajuste_max_pb": 5, "tolerancia": 1e-6},
}

# Advertencias obligatorias de entrega («Supuestos y limitaciones» de cada ficha, literales).
ADVERTENCIAS: dict[str, list[str]] = {
    "TCV-SLOPE-001": [
        "relaciones inestables entre regímenes monetarios (compras de activos, control de curva)",
        "la pendiente forward implica que el carry ya descuenta la reversión bajo expectativas",
        "la inversión de la curva no es predictor fiable de mercados en H1–H2",
    ],
    "TCV-BEI-001": [
        "breakeven ≠ inflación esperada (prima de inflación, prima de liquidez y suelo de deflación en ligados)",
        "estacionalidad decisiva a corto",
        "índice de referencia propio de cada mercado",
    ],
    "TCV-CDS-001": [
        "cambios de composición entre series",
        "índices HY cotizados en precio (conversión declarada)",
        "recuperación supuesta",
        "cupón estándar con pago inicial",
    ],
    "TCV-VIXTS-001": [
        "el spot del índice de volatilidad no es invertible",
        "el futuro converge al valor de liquidación en el vencimiento",
        "contango habitual con saltos extremos",
        "las estructuras que mantienen futuros de volatilidad sufren decaimiento (FON-LEV-001 si están apalancadas)",
    ],
    "TCV-TP-001": [
        "dependencia del modelo (las estimaciones de distintos modelos pueden diferir más de 50 pb)",
        "sesgo de muestra finita en el VAR (persistencia infraestimada)",
        "la prima no es observable",
    ],
}


# ================================================================== utilidades comunes
def _num(x: Any, que: str) -> float:
    if isinstance(x, bool) or not isinstance(x, (int, float, np.integer, np.floating)):
        raise ErrorFicha(f"{que}: no es un número ({str(x)[:40]!r})")
    try:
        f = float(x)
    except OverflowError as e:
        raise ErrorFicha(f"{que}: número fuera de rango") from e
    if not math.isfinite(f):
        raise ErrorFicha(f"{que}: valor no finito ({x!r})")
    return f


def _rango(x: Any, que: str, lo: float | None = None, hi: float | None = None, abierto_lo: bool = False,
           abierto_hi: bool = False) -> float:
    f = _num(x, que)
    if lo is not None and (f < lo or (abierto_lo and f == lo)):
        raise ErrorFicha(f"{que}: {f:g} fuera del rango admitido (mínimo {lo:g}{', excluido' if abierto_lo else ''})")
    if hi is not None and (f > hi or (abierto_hi and f == hi)):
        raise ErrorFicha(f"{que}: {f:g} fuera del rango admitido (máximo {hi:g}{', excluido' if abierto_hi else ''})")
    return f


def _entero(x: Any, que: str, lo: int | None = None, hi: int | None = None) -> int:
    f = _rango(x, que, lo, hi)
    if f != math.floor(f):
        raise ErrorFicha(f"{que}: se esperaba un entero ({f:g})")
    return int(f)


def _lista(x: Any, que: str) -> list[Any]:
    if not isinstance(x, (list, tuple)):
        raise ErrorFicha(f"{que}: se esperaba una lista")
    return list(x)


def _dict(x: Any, que: str) -> dict[str, Any]:
    if not isinstance(x, dict):
        raise ErrorFicha(f"{que}: se esperaba un objeto (dict)")
    return x


def _opcional_dict(v: dict[str, Any], clave: str, que: str) -> dict[str, Any] | None:
    x = v.get(clave)
    return None if x is None else _dict(x, f"{que}: «{clave}»")


def _texto(x: Any) -> bool:
    return isinstance(x, str) and bool(x.strip())


def _textos(x: Any, que: str, vacia: bool = False) -> list[str]:
    if isinstance(x, str):
        x = [x]
    lista = _lista(x, que)
    if not lista and not vacia:
        raise ErrorFicha(f"{que}: lista vacía")
    if not all(_texto(e) for e in lista) or len(set(lista)) != len(lista):
        raise ErrorFicha(f"{que}: se esperaban textos no vacíos y sin repetir")
    return lista


def _validar_parametros(ficha: str, p: dict[str, Any]) -> None:
    """Comprueba tipo y rango de cada parámetro de la petición (falla cerrado con un motivo claro)."""
    F = ficha
    u = UMBRALES[F]
    if F == "TCV-SLOPE-001":
        p["tramos"] = _textos(p["tramos"], f"{F}: tramos")
        p["regresores"] = _textos(p["regresores"], f"{F}: regresores", vacia=True)
        p["ventana"] = _rango(p["ventana"], f"{F}: ventana", 0, abierto_lo=True)
        p["horizonte_carry"] = _rango(p["horizonte_carry"], f"{F}: horizonte_carry", *u["rango_horizonte_carry"])
        p["alfa_ic"] = _rango(p["alfa_ic"], f"{F}: alfa_ic", 0, 1, True, True)
        if p["rezagos_hac"] is not None:
            p["rezagos_hac"] = _entero(p["rezagos_hac"], f"{F}: rezagos_hac", 0)
    elif F == "TCV-BEI-001":
        p["plazos"] = [_rango(t, f"{F}: plazos", 0, abierto_lo=True) for t in _lista(p["plazos"], f"{F}: plazos")]
        if not p["plazos"]:
            raise ErrorFicha(f"{F}: plazos vacío")
        fwd = _lista(p["forward"], f"{F}: forward")
        if len(fwd) != 2:
            raise ErrorFicha(f"{F}: forward = [inicio, plazo] en años")
        p["forward"] = [_rango(t, f"{F}: forward", 0, abierto_lo=True) for t in fwd]
        if not isinstance(p["ajuste_estacional"], bool):
            raise ErrorFicha(f"{F}: ajuste_estacional debe ser true o false")
    elif F == "TCV-CDS-001":
        if p["recuperacion"] is not None:
            p["recuperacion"] = _rango(p["recuperacion"], f"{F}: recuperacion", 0, 1, abierto_hi=True)
        if p["fuente_impagos"] is not None and not _texto(p["fuente_impagos"]):
            raise ErrorFicha(f"{F}: fuente_impagos debe ser un texto")
        p["ventana"] = _rango(p["ventana"], f"{F}: ventana", u["anios_minimos"])
    elif F == "TCV-VIXTS-001":
        p["vencimiento_constante"] = _rango(p["vencimiento_constante"], f"{F}: vencimiento_constante", 0, abierto_lo=True)
        p["ventana_percentil"] = _rango(p["ventana_percentil"], f"{F}: ventana_percentil", 0, abierto_lo=True)
        p["nivel_es"] = _rango(p["nivel_es"], f"{F}: nivel_es", *u["rango_nivel_es"])
    elif F == "TCV-TP-001":
        p["n_factores"] = _entero(p["n_factores"], f"{F}: n_factores", *u["rango_n_factores"])
        if not isinstance(p["metodo"], str) or p["metodo"].strip().lower() not in ("acm", "publicado", "encuesta"):
            raise ErrorFicha(f"{F}: metodo «{str(p['metodo'])[:40]}» no reconocido (ACM, publicado o encuesta)")
        if p["ventana"] is not None:
            p["ventana"] = _rango(p["ventana"], f"{F}: ventana", u["anios_minimos"])


def _parametros(ficha: str, params: dict[str, Any] | None) -> dict[str, Any]:
    """Parámetros de la petición encima de los de la ficha, validados; los umbrales de `UMBRALES` no se cambian."""
    params = _dict(params if params is not None else {}, f"{ficha}: parámetros")
    fijos = set(params) & set(UMBRALES[ficha])
    if fijos:
        raise ErrorFicha(f"{ficha}: {sorted(fijos)} son umbrales fijos de la ficha, no parámetros de la petición")
    p = dict(PARAMETROS_POR_DEFECTO[ficha])
    p.update({k: v for k, v in params.items() if v is not None and k in p})
    _validar_parametros(ficha, p)
    p.update(UMBRALES[ficha])
    return p


def _requerido(v: dict[str, Any], clave: str, ficha: str, que: str = "") -> Any:
    if not isinstance(v, dict) or v.get(clave) is None:
        raise ErrorFicha(f"{ficha}: falta «{clave}»{' (' + que + ')' if que else ''}")
    return v[clave]


def _requerido_dict(v: dict[str, Any], clave: str, ficha: str, que: str = "") -> dict[str, Any]:
    return _dict(_requerido(v, clave, ficha, que), f"{ficha}: «{clave}»")


def _vector(x: Any, que: str, minimo: int = 1) -> np.ndarray:
    lista = _lista(x, que) if not isinstance(x, np.ndarray) else list(x)
    a = np.array([_num(e, que) for e in lista], dtype=float)
    if len(a) < minimo:
        raise ErrorFicha(f"{que}: {len(a)} valores (< {minimo})")
    return a


def _matriz(filas: Any, n_filas: int, n_cols: int, que: str) -> np.ndarray:
    filas = _lista(filas, que)
    if len(filas) != n_filas:
        raise ErrorFicha(f"{que}: se esperaban {n_filas} filas")
    m = np.zeros((n_filas, n_cols))
    for i, f in enumerate(filas):
        fila = _vector(f, que)
        if len(fila) != n_cols:
            raise ErrorFicha(f"{que}: cada fila debe tener {n_cols} valores (fila {i})")
        m[i] = fila
    return m


_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}([T ].*)?$")


def _fecha(x: Any, que: str) -> date:
    """Fecha ISO (texto «AAAA-MM-DD»), `date` o `Timestamp`. Los números se rechazan (H-11: 20261110 no es fecha)."""
    if isinstance(x, pd.Timestamp):
        if pd.isna(x):
            raise ErrorFicha(f"{que}: fecha vacía (NaT)")
        return x.date()
    if isinstance(x, datetime):
        return x.date()
    if isinstance(x, date):
        return x
    if not isinstance(x, str) or not _ISO.match(x.strip()):
        raise ErrorFicha(f"{que}: fecha no válida ({str(x)[:40]!r}); se espera texto ISO «AAAA-MM-DD»")
    try:
        return date.fromisoformat(x.strip()[:10])
    except ValueError as e:
        raise ErrorFicha(f"{que}: fecha no válida ({x!r})") from e


def _fechas(x: Any, que: str, minimo: int = 2) -> list[date]:
    f = [_fecha(e, que) for e in _lista(x, que)]
    if len(f) < minimo:
        raise ErrorFicha(f"{que}: {len(f)} fechas (< {minimo})")
    if any(b <= a for a, b in itertools.pairwise(f)):
        raise ErrorFicha(f"{que}: las fechas deben ser estrictamente crecientes")
    return f


def _anios(f0: date, f1: date) -> float:
    """Años entre dos fechas con recuento Real/365 (Catálogo 3.1)."""
    return (f1 - f0).days / DIAS_POR_ANIO


def _nodos(curva: Any, que: str, clave: str = "rendimientos", minimo: int = 2) -> tuple[np.ndarray, np.ndarray]:
    """Nodos (plazo en años, valor) de una curva {"plazos": [...], clave: [...]}, plazos estrictamente crecientes."""
    if not isinstance(curva, dict):
        raise ErrorFicha(f"{que}: se esperaba {{'plazos': [...], '{clave}': [...]}}")
    plazos = _vector(curva.get("plazos"), f"{que}.plazos", minimo)
    valores = _vector(curva.get(clave), f"{que}.{clave}", minimo)
    if len(plazos) != len(valores):
        raise ErrorFicha(f"{que}: plazos y {clave} de distinta longitud")
    if np.any(plazos < 0) or np.any(np.diff(plazos) <= 0):
        raise ErrorFicha(f"{que}: los plazos deben ser no negativos y estrictamente crecientes")
    return plazos, valores


def _tipos(valores: np.ndarray, que: str) -> np.ndarray:
    """Tipos en % anual: deben ser > −100 % para que (1 + y) tenga sentido con capitalización compuesta."""
    if np.any(valores <= -PCT):
        raise ErrorFicha(f"{que}: tipos ≤ −100 %")
    return valores


def _interp(plazos: np.ndarray, valores: np.ndarray, x: float, que: str) -> float:
    """Interpolación lineal entre nodos; fuera del rango de la curva no se extrapola (falla cerrado)."""
    if x < plazos[0] or x > plazos[-1]:
        raise ErrorFicha(f"{que}: el plazo {x:g} queda fuera de la curva [{plazos[0]:g}, {plazos[-1]:g}]; no se extrapola")
    return float(np.interp(x, plazos, valores))


def _interp_o_none(plazos: np.ndarray, valores: np.ndarray, x: float, que: str, lim: list[str]) -> float | None:
    try:
        return _interp(plazos, valores, x, que)
    except ErrorFicha as e:
        lim.append(f"{e}: salida no calculada")
        return None


def _posicion(valor: float, historia: np.ndarray, que: str) -> dict[str, Any]:
    """Percentil (fracción de la historia ≤ valor) y z-score; z = None si la historia no tiene dispersión."""
    h = np.asarray(historia, dtype=float)
    if len(h) < 2:
        raise ErrorFicha(f"{que}: historia insuficiente para percentil y z (< 2 observaciones)")
    sd = float(np.std(h, ddof=1))
    return {"percentil": float(np.mean(h <= valor)), "z": float((valor - np.mean(h)) / sd) if sd > 0 else None,
            "media": float(np.mean(h)), "n": len(h)}


def _serie_a_listas(s: Any, que: str) -> tuple[list[date], list[float]]:
    """Serie de rol (pd.Series con índice de fechas) → (fechas, valores finitos)."""
    if not isinstance(s, pd.Series) or not isinstance(s.index, pd.DatetimeIndex):
        raise ErrorFicha(f"{que}: se esperaba una serie con índice de fechas")
    s = s.dropna()
    return [i.date() for i in s.index], [float(x) for x in _vector(list(s.to_numpy()), que)]


def _finitos(x: Any, ruta: str, malas: list[str]) -> Any:
    """Copia JSON del resultado con cada número no finito sustituido por None (y su ruta anotada)."""
    if isinstance(x, dict):
        return {str(k): _finitos(v, f"{ruta}.{k}", malas) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_finitos(v, f"{ruta}[{i}]", malas) for i, v in enumerate(x)]
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        if not math.isfinite(float(x)):
            malas.append(ruta)
            return None
        return float(x)
    return x


def _blindar(ficha: str, fn: Callable[[dict[str, Any], dict[str, Any]], Resultado]) -> Callable[..., Resultado]:
    """Falla cerrado ante cualquier entrada mal formada y nunca sirve números no finitos (H-02 de la QA r01)."""

    @functools.wraps(fn)
    def blindado(ent: Any, params: Any = None) -> Resultado:
        ent = _dict(ent, f"{ficha}: entrada")
        _dict(ent.get("valores") or {}, f"{ficha}: valores")
        _dict(ent.get("series_rol") or {}, f"{ficha}: series_rol")
        try:
            with np.errstate(all="ignore"):
                res, lim = fn(ent, params)
        except ErrorFicha:
            raise
        except (OverflowError, ZeroDivisionError, FloatingPointError, np.linalg.LinAlgError) as e:
            raise ErrorFicha(f"{ficha}: cálculo numérico no válido con estos datos ({type(e).__name__}: {e})") from e
        except (TypeError, ValueError, AttributeError, KeyError, IndexError) as e:
            raise ErrorFicha(f"{ficha}: entrada mal formada ({type(e).__name__}: {e})") from e
        malas: list[str] = []
        limpio = _finitos(res, "resultado", malas)
        if malas:
            lim.append(f"cifras no finitas no servidas (None): {', '.join(malas[:5])}")
        return limpio, lim

    return blindado


# ================================================================== TCV-SLOPE-001
_TRAMO = re.compile(r"^(\d+(?:\.\d+)?)([smy])(\d+(?:\.\d+)?)([smy])$")


def _tramo(t: Any) -> tuple[float, float]:
    """«2s10s» → (2, 10) años; «3m10y» → (0,25, 10). m = meses; s o y = años."""
    m = _TRAMO.match(str(t).strip().lower())
    if not m:
        raise ErrorFicha(f"TCV-SLOPE-001: tramo no reconocido ({t!r}); formato «2s10s», «5s30s» o «3m10y»")

    def a_anios(n: str, u: str) -> float:
        return float(n) / MESES_POR_ANIO if u == "m" else float(n)

    corto, largo = a_anios(m[1], m[2]), a_anios(m[3], m[4])
    if not 0 < corto < largo:
        raise ErrorFicha(f"TCV-SLOPE-001: tramo {t!r} incoherente (el plazo corto debe ser menor que el largo)")
    return corto, largo


def _rezagos_newey_west(n: int) -> int:
    """Regla de rezagos de Newey-West que fija el Catálogo en ACC-FACT-001: L = ⌊4·(T/100)^(2/9)⌋."""
    return math.floor(4 * (n / 100) ** (2 / 9))


def _mco_hac(y: np.ndarray, X: np.ndarray, rezagos: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """MCO con covarianza HAC de Newey-West (núcleo de Bartlett). Devuelve (β, residuos, V_HAC)."""
    n, k = X.shape
    if n <= k:
        raise ErrorFicha(f"TCV-SLOPE-001: {n} observaciones para {k} coeficientes; regresión no identificada")
    if np.linalg.matrix_rank(X) < k:
        raise ErrorFicha("TCV-SLOPE-001: regresores colineales (o constantes) en la ventana; regresión no identificada")
    xtx_inv = np.linalg.inv(X.T @ X)
    beta = xtx_inv @ (X.T @ y)
    e = y - X @ beta
    u = X * e[:, None]
    S = u.T @ u
    for rez in range(1, rezagos + 1):
        w = 1 - rez / (rezagos + 1)
        G = u[rez:].T @ u[:-rez]
        S = S + w * (G + G.T)
    return beta, e, xtx_inv @ S @ xtx_inv


def _carry_tramo(plazos: np.ndarray, curva: np.ndarray, tau: float, dt: float, fin: float,
                 lim: list[str]) -> dict[str, float] | None:
    """FIR-CARRY-001 sobre un nodo cupón cero: carry = (y − financiación)·Δt; rolldown = −D_mod·[y(τ−Δt) − y(τ)]."""
    y = _interp(plazos, curva, tau, "TCV-SLOPE-001: curva") / PCT
    y_rd = _interp_o_none(plazos, curva, tau - dt, "TCV-SLOPE-001: rolldown", lim)
    if y_rd is None:
        return None
    d_mod = tau / (1 + y)
    carry = (y - fin) * dt
    rolldown = -d_mod * (y_rd / PCT - y)
    return {"carry": carry, "rolldown": rolldown, "d_mod": d_mod}


def _forward(y_ini: float, t_ini: float, y_fin: float, t_fin: float) -> float:
    """Tipo forward entre t_ini y t_fin con capitalización anual compuesta (tantos por uno)."""
    if not (1 + y_ini > 0 and 1 + y_fin > 0 and t_fin > t_ini):
        raise ErrorFicha("forward: tipos ≤ −100 % o plazos incoherentes")
    try:
        f = ((1 + y_fin) ** t_fin / (1 + y_ini) ** t_ini) ** (1 / (t_fin - t_ini)) - 1
    except OverflowError as e:
        raise ErrorFicha("forward: desbordamiento numérico (tipos fuera de escala)") from e
    if not math.isfinite(f):
        raise ErrorFicha("forward: resultado no finito")
    return float(f)


def _regimen(d_pend: float, d_nivel: float) -> str:
    """Régimen por signos (alcista/bajista en sentido del precio del bono: alcista = bajan los tipos)."""
    if d_pend == 0:
        return "sin cambio de pendiente"
    forma = "empinamiento" if d_pend > 0 else "aplanamiento"
    if d_nivel == 0:
        return f"{forma} sin cambio de nivel"
    return f"{forma} {'alcista' if d_nivel < 0 else 'bajista'}"


def f_tcv_slope(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """TCV-SLOPE-001 · Pendiente de la curva y su valor razonable.

    Entradas en ``valores``:
    - ``historia_curva``: {"fechas": [ISO...], "plazos": [años], "rendimientos": [[% por nodo] por fecha]}; curva
      cupón cero (% anual, capitalización anual), diaria o semanal; la última fila es la curva actual.
    - ``regresores``: {nombre: {"serie": [...alineada con fechas...], "conocible_desde": [ISO...], "fuente": str}}
      para cada nombre de ``params["regresores"]`` (salidas de MON-EXP-001 y TCV-TP-001 y variables macro con sus
      vintages: cada dato debe ser conocible en su fecha). El último valor es el actual.
    - ``financiacion`` (opcional, %): tipo de financiación del carry; si falta, el tipo de la curva a Δt.
    - ``beta1_nss`` (opcional): {"valor": %, "fuente": str}, β₁ de FIR-CURVE-001 para la segunda vía.
    No usa ``series_rol`` (una curva es una tabla, no una serie).
    """
    F = "TCV-SLOPE-001"
    p = _parametros(F, params)
    v = ent.get("valores") or {}
    lim = list(ADVERTENCIAS[F])

    hc = _requerido_dict(v, "historia_curva", F, "curva con fechas, plazos y rendimientos")
    fechas = _fechas(hc.get("fechas"), f"{F}: historia_curva.fechas")
    plazos = _vector(hc.get("plazos"), f"{F}: historia_curva.plazos")
    if len(plazos) < int(p["nodos_minimos"]):
        raise ErrorFicha(f"{F}: curva con {len(plazos)} nodos (< {p['nodos_minimos']}): rechazo de la ficha")
    if np.any(plazos <= 0) or np.any(np.diff(plazos) <= 0):
        raise ErrorFicha(f"{F}: los plazos deben ser positivos y estrictamente crecientes")
    R = _tipos(_matriz(hc.get("rendimientos"), len(fechas), len(plazos), f"{F}: historia_curva.rendimientos"),
               f"{F}: historia_curva.rendimientos")
    span = _anios(fechas[0], fechas[-1])
    if span < float(p["anios_minimos"]):
        raise ErrorFicha(f"{F}: historia de {span:.2f} años (< {p['anios_minimos']}): rechazo de la ficha")
    if span < float(p["anios_entrada_minima"]):
        lim.append(f"historia de {span:.2f} años (< {p['anios_entrada_minima']} de la entrada mínima): valor razonable orientativo")

    # Regresores con vintages
    nombres = list(p["regresores"] or [])
    datos_reg = _dict(v.get("regresores") or {}, f"{F}: regresores")
    cols = []
    for nombre in nombres:
        r = datos_reg.get(nombre)
        if not isinstance(r, dict):
            raise ErrorFicha(f"{F}: falta el regresor «{nombre}» (serie, conocible_desde y fuente)")
        if not _texto(r.get("fuente")):
            raise ErrorFicha(f"{F}: el regresor «{nombre}» no declara fuente")
        serie = _vector(r.get("serie"), f"{F}: regresor {nombre}")
        if len(serie) != len(fechas):
            raise ErrorFicha(f"{F}: el regresor «{nombre}» no está alineado con las fechas de la curva")
        conoc = r.get("conocible_desde")
        if not isinstance(conoc, (list, tuple)) or len(conoc) != len(fechas):
            raise ErrorFicha(f"{F}: el regresor «{nombre}» necesita «conocible_desde» (vintage) por observación")
        for fc, fd in zip(conoc, fechas):
            if _fecha(fc, f"{F}: conocible_desde de {nombre}") > fd:
                raise ErrorFicha(f"{F}: el regresor «{nombre}» usa un dato conocible el {fc}, posterior a {fd} (fuga de información)")
        cols.append(serie)
    if not nombres:
        lim.append("sin regresores: el valor razonable es la media de la pendiente en la ventana")

    ventana = float(p["ventana"])
    en_ventana = np.array([_anios(f, fechas[-1]) <= ventana for f in fechas])
    idx_est = np.where(en_ventana)[0][:-1]          # estimación: ventana sin la observación actual
    X_all = np.column_stack([np.ones(len(fechas))] + cols)
    alfa = float(p["alfa_ic"])
    rezagos = p["rezagos_hac"]
    rezagos = _rezagos_newey_west(len(idx_est)) if rezagos is None else int(rezagos)
    if rezagos >= len(idx_est):
        raise ErrorFicha(f"{F}: rezagos_hac ({rezagos}) ≥ observaciones de la ventana ({len(idx_est)})")

    tramos = p["tramos"]
    dt = float(p["horizonte_carry"]) / MESES_POR_ANIO
    actual = R[-1]
    fin_dato = v.get("financiacion")
    if fin_dato is not None:
        fin: float | None = _rango(fin_dato, f"{F}: financiacion", -PCT, abierto_lo=True) / PCT
    else:
        y_fin = _interp_o_none(plazos, actual, dt, f"{F}: financiación (tipo de la curva a Δt)", lim)
        fin = None if y_fin is None else y_fin / PCT

    salida_tramos: dict[str, Any] = {}
    for t in tramos:
        a, b = _tramo(t)
        _interp(plazos, actual, a, f"{F}: tramo {t}")
        _interp(plazos, actual, b, f"{F}: tramo {t}")
        ya = np.array([np.interp(a, plazos, fila) for fila in R])
        yb = np.array([np.interp(b, plazos, fila) for fila in R])
        pend = (yb - ya) * PB_POR_PUNTO                      # (i) pendiente en pb
        if not np.all(np.isfinite(pend)):
            raise ErrorFicha(f"{F}: pendientes no finitas (rendimientos fuera de escala)")
        nivel = (ya + yb) / 2                                # nivel del tramo (media de los dos nodos, %)

        # (ii) valor razonable por regresión con errores HAC
        beta, e, V = _mco_hac(pend[idx_est], X_all[idx_est], rezagos)
        x0 = X_all[-1]
        razonable = float(x0 @ beta)
        ee = float(math.sqrt(max(float(x0 @ V @ x0), 0.0)))
        q = float(stats.norm.ppf(1 - alfa / 2))
        if not (math.isfinite(razonable) and math.isfinite(ee) and np.all(np.isfinite(beta))):
            raise ErrorFicha(f"{F}: valor razonable o su IC no finitos (regresores fuera de escala)")
        residuo = float(pend[-1] - razonable)
        dof = len(idx_est) - X_all.shape[1]
        s = float(math.sqrt(float(e @ e) / dof))
        if s > 0:
            z: float | None = residuo / s
        else:
            z = None
            lim.append(f"{t}: residuos de la regresión sin dispersión: z no definido")
        ee_coef = np.sqrt(np.clip(np.diag(V), 0.0, None))

        # (iii) pendiente forward a 3 y 6 meses y punto muerto
        fwd: dict[str, float | None] = {}
        muerto: dict[str, float | None] = {}
        for h_m in p["horizontes_forward"]:
            h = _num(h_m, f"{F}: horizontes_forward") / MESES_POR_ANIO
            clave = f"{h_m:g}m" if isinstance(h_m, (int, float)) else str(h_m)
            yh = _interp_o_none(plazos, actual, h, f"{F}: forward {clave}", lim)
            yha = _interp_o_none(plazos, actual, h + a, f"{F}: forward {clave}", lim)
            yhb = _interp_o_none(plazos, actual, h + b, f"{F}: forward {clave}", lim)
            if yh is None or yha is None or yhb is None:
                fwd[clave] = muerto[clave] = None
                continue
            fa = _forward(yh / PCT, h, yha / PCT, h + a)
            fb = _forward(yh / PCT, h, yhb / PCT, h + b)
            pend_fwd = (fb - fa) * PB_POR_UNIDAD
            fwd[clave] = pend_fwd
            muerto[clave] = pend_fwd - float(pend[-1])

        # (iv) carry + rolldown de la exposición neutral en DV01 (largo tramo corto, corto tramo largo)
        carry_neutral: dict[str, float] | None = None
        if fin is not None:
            ca = _carry_tramo(plazos, actual, a, dt, fin, lim)
            cb = _carry_tramo(plazos, actual, b, dt, fin, lim)
            if ca is not None and cb is not None:
                c = (ca["carry"] / ca["d_mod"] - cb["carry"] / cb["d_mod"]) * PB_POR_UNIDAD
                r = (ca["rolldown"] / ca["d_mod"] - cb["rolldown"] / cb["d_mod"]) * PB_POR_UNIDAD
                carry_neutral = {"carry_pb": c, "rolldown_pb": r, "total_pb": c + r,
                                 "horizonte_meses": float(p["horizonte_carry"])}

        # (v) régimen por signos de los cambios de nivel y pendiente en el horizonte del carry
        previos = [i for i, f in enumerate(fechas) if _anios(f, fechas[-1]) >= dt]
        if previos:
            j = previos[-1]
            d_p, d_n = float(pend[-1] - pend[j]), float(nivel[-1] - nivel[j])
            regimen: dict[str, Any] | None = {"desde": fechas[j].isoformat(), "cambio_pendiente_pb": d_p,
                                              "cambio_nivel_pb": d_n * PB_POR_PUNTO, "regimen": _regimen(d_p, d_n)}
        else:
            regimen = None
            lim.append(f"{t}: la historia no cubre el horizonte del régimen: régimen no calculado")

        salida_tramos[str(t)] = {
            "pendiente_pb": float(pend[-1]),
            "valor_razonable_pb": razonable,
            "ic_valor_razonable_pb": [razonable - q * ee, razonable + q * ee],
            "nivel_ic": 1 - alfa,
            "residuo_pb": residuo,
            "z": z,
            "percentil_residuo": float(np.mean(e <= residuo)),
            "pendiente_forward_pb": fwd,
            "punto_muerto_pb": muerto,
            "carry_neutral_dv01_pb": carry_neutral,
            "regimen": regimen,
            "regresion": {"n": len(idx_est), "rezagos_hac": rezagos,
                          "coeficientes": dict(zip(["constante"] + nombres, [float(x) for x in beta])),
                          "errores_hac": dict(zip(["constante"] + nombres, [float(x) for x in ee_coef]))},
        }
    if carry_neutral is None:
        lim.append("carry neutral en DV01 no calculado (financiación o nodos de rolldown fuera de la curva)")

    # Segunda vía: β₁ de NSS (FIR-CURVE-001) aportado como dato con fuente. En NSS, y(0) − y(∞) = β₁.
    segunda: dict[str, Any] | None = None
    b1 = v.get("beta1_nss")
    if b1 is not None:
        if not isinstance(b1, dict) or not _texto(b1.get("fuente")):
            raise ErrorFicha(f"{F}: «beta1_nss» necesita valor y fuente")
        menos_b1 = -_num(b1.get("valor"), f"{F}: beta1_nss.valor") * PB_POR_PUNTO
        segunda = {"pendiente_nss_pb": menos_b1, "fuente": b1["fuente"],
                   "signo_coherente": {t: bool(np.sign(menos_b1) == np.sign(d["pendiente_pb"]))
                                       for t, d in salida_tramos.items()}}
    else:
        lim.append("segunda vía (β₁ de NSS, FIR-CURVE-001) no aportada")
    return {"fecha": fechas[-1].isoformat(), "tramos": salida_tramos, "segunda_via": segunda}, lim


# ================================================================== TCV-BEI-001
def _clave_plazo(x: Any) -> str:
    return f"{float(x):g}"


def f_tcv_bei(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """TCV-BEI-001 · Inflación implícita frente a esperada.

    Entradas en ``valores`` (tipos en % anual):
    - ``curva_nominal`` {"plazos", "rendimientos"} y ``curva_real`` {"plazos", "rendimientos",
      "indice_referencia"} con ≥ 3 vencimientos reales; o ``swaps_inflacion`` {"plazos", "tasas",
      "indice_referencia"} (también ≥ 3 vencimientos). Si hay curva real y swaps, son la segunda vía.
    - ``conversion_indice`` (texto): obligatorio si los índices de referencia de curva real y swaps difieren.
    - ``encuestas``: {"fecha", "fuente", "horizontes": {"2": %, "5": %, "10": %, "5y5y": %}}.
    - ``estacionalidad`` (obligatoria si hay nodos < 3 años y ajuste estacional): {"factores": [12 factores
      multiplicativos ene..dic], "mes_liquidacion": 1..12, "retardo_indexacion_meses": int}. El ajuste se aplica a
      cada nodo real (o de swap) de vencimiento < 3 años antes de interpolar.
    - Opcionales: ``historia`` {"fechas", "breakevens": {"10": [...], "5y5y": [...], ...}} (≥ 10 años);
      ``inflacion_devengada`` {"tasa": %, "horizonte_meses": n, "fuente"}; ``descomposicion_afin`` {"fuente", ...}.
    ``series_rol``: rol ``breakeven_<plazo>`` (p. ej. ``breakeven_10``) como historia del breakeven.
    """
    F = "TCV-BEI-001"
    p = _parametros(F, params)
    v = ent.get("valores") or {}
    lim = list(ADVERTENCIAS[F])
    minimo = int(p["vencimientos_reales_minimos"])

    swaps = v.get("swaps_inflacion")
    real = v.get("curva_real")
    if real is None and swaps is None:
        raise ErrorFicha(f"{F}: falta «curva_real» (con «curva_nominal») o «swaps_inflacion»")
    pr = vr = ps = vs = None
    if real is not None:
        pn, vn = _nodos(_requerido(v, "curva_nominal", F), f"{F}: curva_nominal")
        _tipos(vn, f"{F}: curva_nominal")
        real = _dict(real, f"{F}: curva_real")
        pr, vr = _nodos(real, f"{F}: curva_real", minimo=1)
        if len(pr) < minimo:
            raise ErrorFicha(f"{F}: curva real con < {minimo} vencimientos: rechazo de la ficha")
        _tipos(vr, f"{F}: curva_real")
        if not _texto(real.get("indice_referencia")):
            raise ErrorFicha(f"{F}: la curva real no declara «indice_referencia»")
    if swaps is not None:
        swaps = _dict(swaps, f"{F}: swaps_inflacion")
        ps, vs = _nodos(swaps, f"{F}: swaps_inflacion", "tasas", minimo=1)
        if len(ps) < minimo:
            raise ErrorFicha(f"{F}: swaps de inflación con < {minimo} vencimientos: rechazo de la ficha")
        _tipos(vs, f"{F}: swaps_inflacion")
        if not _texto(swaps.get("indice_referencia")):
            raise ErrorFicha(f"{F}: los swaps de inflación no declaran «indice_referencia»")
    if real is not None and swaps is not None and real["indice_referencia"] != swaps["indice_referencia"] \
            and not _texto(v.get("conversion_indice")):
        raise ErrorFicha(f"{F}: índices de referencia distintos ({real['indice_referencia']} / "
                         f"{swaps['indice_referencia']}) sin conversión declarada: rechazo de la ficha")

    enc = _requerido_dict(v, "encuestas", F, "inflación esperada por encuestas con fecha y fuente")
    if not _texto(enc.get("fuente")) or enc.get("fecha") is None:
        raise ErrorFicha(f"{F}: las encuestas necesitan «fecha» y «fuente»")
    _fecha(enc["fecha"], f"{F}: encuestas.fecha")

    est = _opcional_dict(v, "estacionalidad", F)
    ajustar = bool(p["ajuste_estacional"])
    umbral = float(p["plazo_ajuste_estacional"])

    def sesgo(t: float) -> float:
        """Sesgo estacional (%) de un nodo de vencimiento t: [ln s(mes_vto − retardo) − ln s(mes_liq − retardo)]/t.

        El cobro del ligado sigue al índice sin desestacionalizar con su retardo de indexación; si el mes de referencia
        del vencimiento es estacionalmente alto, el rendimiento real cotizado es más bajo y el breakeven más alto.
        """
        if not isinstance(est, dict):
            raise ErrorFicha(f"{F}: nodo de {t:g} años < {umbral:g} con ajuste estacional y sin «estacionalidad» del índice")
        fac = _vector(est.get("factores"), f"{F}: estacionalidad.factores")
        if len(fac) != MESES_POR_ANIO or np.any(fac <= 0):
            raise ErrorFicha(f"{F}: estacionalidad.factores debe tener {MESES_POR_ANIO} factores positivos")
        m_liq = _entero(est.get("mes_liquidacion"), f"{F}: estacionalidad.mes_liquidacion", 1, MESES_POR_ANIO)
        retardo = _entero(est.get("retardo_indexacion_meses"), f"{F}: estacionalidad.retardo_indexacion_meses", 0)
        m0 = (m_liq - 1 - retardo) % MESES_POR_ANIO
        mt = (m_liq - 1 + round(t * MESES_POR_ANIO) - retardo) % MESES_POR_ANIO
        return float((math.log(fac[mt]) - math.log(fac[m0])) / t * PCT)

    # (i) ajuste estacional por nodo (plazos < 3 años) antes de interpolar: real + sesgo; swap − sesgo
    ajustados: list[str] = []
    vr_aj = vr.copy() if vr is not None else None
    vs_aj = vs.copy() if vs is not None else None
    if ajustar:
        if pr is not None and vr_aj is not None:
            for i, t in enumerate(pr):
                if 0 < t < umbral:
                    vr_aj[i] += sesgo(float(t))
                    ajustados.append(f"real {_clave_plazo(t)}")
        elif ps is not None and vs_aj is not None:
            for i, t in enumerate(ps):
                if 0 < t < umbral:
                    vs_aj[i] -= sesgo(float(t))
                    ajustados.append(f"swap {_clave_plazo(t)}")

    def be_bruto(t: float) -> float:
        """Breakeven sin ajuste estacional (base swap−bono)."""
        if pr is not None and vr is not None:
            return _interp(pn, vn, t, f"{F}: curva nominal") - _interp(pr, vr, t, f"{F}: curva real")
        assert ps is not None and vs is not None
        return _interp(ps, vs, t, f"{F}: swaps de inflación")

    def be(t: float) -> float:
        if pr is not None and vr_aj is not None:
            return _interp(pn, vn, t, f"{F}: curva nominal") - _interp(pr, vr_aj, t, f"{F}: curva real")
        assert ps is not None and vs_aj is not None
        return _interp(ps, vs_aj, t, f"{F}: swaps de inflación")

    plazos = [float(x) for x in p["plazos"]]
    bes: dict[str, float | None] = {}
    for t in plazos:
        try:
            bes[_clave_plazo(t)] = be(t)
        except ErrorFicha as e:
            if "fuera de la curva" not in str(e):
                raise
            bes[_clave_plazo(t)] = None
            lim.append(f"{e}: breakeven a {t:g} años no calculado")
    if all(x is None for x in bes.values()):
        raise ErrorFicha(f"{F}: ningún plazo pedido queda dentro de las curvas")

    # (ii) breakeven forward iniciof·plazof (5y5y por defecto)
    t_i, t_p = (float(x) for x in p["forward"])
    clave_fwd = f"{t_i:g}y{t_p:g}y"
    try:
        b_i, b_f = be(t_i) / PCT, be(t_i + t_p) / PCT
        fwd: float | None = _forward(b_i, t_i, b_f, t_i + t_p) * PCT
        fwd_contado: dict[str, float] | None = {_clave_plazo(t_i): b_i * PCT, _clave_plazo(t_i + t_p): b_f * PCT}
    except ErrorFicha as e:
        if "fuera de la curva" not in str(e):
            raise
        fwd = fwd_contado = None
        lim.append(f"{e}: breakeven forward {clave_fwd} no calculado")

    # (iii) segunda vía: swaps − bono (aproximación a la prima de liquidez de los ligados)
    base: dict[str, float | None] | None = None
    if real is not None and ps is not None and vs is not None:
        base = {}
        for t in plazos:
            try:
                base[_clave_plazo(t)] = (_interp(ps, vs, t, f"{F}: swaps") - be_bruto(t)) * PB_POR_PUNTO
            except ErrorFicha as e:
                base[_clave_plazo(t)] = None
                lim.append(f"{e}: base swap−bono a {t:g} años no calculada")
    else:
        lim.append("sin curva real y swaps a la vez: base swap−bono (segunda vía) no calculada")

    # (iv) brecha frente a encuestas a igual horizonte
    hor = _dict(enc.get("horizontes") or {}, f"{F}: encuestas.horizontes")
    brecha: dict[str, float | None] = {}
    for clave, valor in list(bes.items()) + [(clave_fwd, fwd)]:
        if clave in hor and valor is not None:
            brecha[clave] = (valor - _num(hor[clave], f"{F}: encuesta {clave}")) * PB_POR_PUNTO
        else:
            brecha[clave] = None
    if any(x is None for x in brecha.values()):
        lim.append("brecha frente a encuestas sin horizonte comparable en algún plazo")

    # (v) descomposición afín: solo como dato con fuente
    afin = _opcional_dict(v, "descomposicion_afin", F)
    if afin is not None:
        if not _texto(afin.get("fuente")):
            raise ErrorFicha(f"{F}: «descomposicion_afin» necesita fuente")
    else:
        lim.append("sin descomposición en inflación esperada y primas (requiere la salida de un modelo afín aportada con fuente)")

    # (vi) percentil y z-score frente a ≥ 10 años; carry de inflación a corto
    posiciones: dict[str, Any] = {}
    hist = _opcional_dict(v, "historia", F)
    historias: dict[str, tuple[list[date], np.ndarray]] = {}
    if hist is not None:
        fh = _fechas(hist.get("fechas"), f"{F}: historia.fechas")
        for clave, serie in _requerido_dict(hist, "breakevens", F, "historia por plazo").items():
            a = _vector(serie, f"{F}: historia {clave}")
            if len(a) != len(fh):
                raise ErrorFicha(f"{F}: historia {clave} no alineada con sus fechas")
            historias[str(clave)] = (fh, a)
    for rol, s in (ent.get("series_rol") or {}).items():
        if str(rol).startswith("breakeven_"):
            f_s, x_s = _serie_a_listas(s, f"{F}: serie {rol}")
            historias[str(rol)[len("breakeven_"):]] = (f_s, np.array(x_s))
    actuales = dict(bes)
    actuales[clave_fwd] = fwd
    for clave, (fh, a) in historias.items():
        valor_actual = actuales.get(clave)
        if valor_actual is None:
            continue
        posiciones[clave] = _posicion(valor_actual, a, f"{F}: historia {clave}")
        span = _anios(fh[0], fh[-1])
        posiciones[clave]["anios"] = span
        if span < float(p["anios_percentil"]):
            lim.append(f"historia del breakeven {clave} de {span:.2f} años (< {p['anios_percentil']}): percentil orientativo")
    if not posiciones:
        lim.append("sin historia de breakevens: percentiles y z no calculados")

    carry: float | None = None
    dev = _opcional_dict(v, "inflacion_devengada", F)
    validos = [t for t in plazos if bes[_clave_plazo(t)] is not None]
    if dev is not None and validos:
        if not _texto(dev.get("fuente")):
            raise ErrorFicha(f"{F}: «inflacion_devengada» necesita fuente")
        h = _rango(dev.get("horizonte_meses"), f"{F}: inflacion_devengada.horizonte_meses", 0,
                   abierto_lo=True) / MESES_POR_ANIO
        corto = bes[_clave_plazo(min(validos))]
        assert corto is not None
        carry = (_num(dev.get("tasa"), f"{F}: inflacion_devengada.tasa") - corto) * PB_POR_PUNTO * h
    else:
        lim.append("sin inflación devengada esperada: carry de inflación no calculado")

    return {"breakevens_pct": bes, "ajuste_estacional_aplicado": ajustados,
            f"forward_{clave_fwd}_pct": fwd, "breakevens_contado_forward_pct": fwd_contado,
            "base_swap_bono_pb": base, "brecha_encuestas_pb": brecha, "fuente_encuestas": enc["fuente"],
            "percentiles": posiciones or None, "carry_inflacion_pb": carry,
            "descomposicion_afin": afin}, lim


# ================================================================== TCV-CDS-001
def _identificador(x: Any, que: str) -> str | int:
    """Serie o versión del índice: texto no vacío o entero."""
    if _texto(x):
        return str(x)
    return _entero(x, que)


def _rpv01(tau: float, lam: float, r: float) -> float:
    """Duración con riesgo (años) con prima continua: (1 − e^{−(r+λ)τ})/(r+λ); r continuo."""
    k = r + lam
    return tau if k == 0 else float((1 - math.exp(-k * tau)) / k)


def f_tcv_cds(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """TCV-CDS-001 · Diferencial de índice CDS frente a pérdidas esperadas.

    Entradas en ``valores`` (diferenciales en pb):
    - ``indice``: {"nombre", "serie", "version", "segmento": "IG" | "HY", "cotizacion"?: "diferencial" | "precio",
      "conversion_precio"?: texto (obligatorio si cotiza en precio), "enlace_series"?: texto}.
    - ``historia``: {"fechas", "diferenciales_pb"} de la serie on-the-run (≥ 5 años); el último es el actual.
    - ``impagos``: {"fuente", "pd_anual"} (tasa prevista aportada) o {"fuente", "rating_medio",
      "tasas_por_rating": {rating: {año: tasa}}, "anios"?: [años de la fase del ciclo]} (tasas en tanto por uno).
    - ``contado``: {"diferencial_pb", "medida": "OAS" | "Z"}.
    - Opcionales: ``curva_diferenciales`` {"plazos", "diferenciales_pb"}, ``vencimiento_anios`` del índice,
      ``tipo_libre`` (%), para pendiente 5–10, carry + roll-down y DV01.
    ``series_rol``: rol ``diferencial_indice`` como historia del diferencial.
    """
    F = "TCV-CDS-001"
    p = _parametros(F, params)
    v = ent.get("valores") or {}
    lim = list(ADVERTENCIAS[F])

    ind = v.get("indice")
    if not isinstance(ind, dict) or ind.get("serie") is None or ind.get("version") is None:
        raise ErrorFicha(f"{F}: índice sin serie y versión: rechazo de la ficha")
    ficha_indice: dict[str, Any] = {"serie": _identificador(ind["serie"], f"{F}: indice.serie"),
                    "version": _identificador(ind["version"], f"{F}: indice.version")}
    for clave in ("nombre", "segmento", "cotizacion", "conversion_precio", "enlace_series"):
        if ind.get(clave) is not None and not _texto(ind[clave]):
            raise ErrorFicha(f"{F}: indice.{clave} debe ser un texto")
    seg = str(ind.get("segmento") or "").upper()
    if seg and seg not in ("IG", "HY"):
        raise ErrorFicha(f"{F}: segmento «{seg[:20]}» no reconocido (IG o HY)")
    ficha_indice.update(nombre=ind.get("nombre"), segmento=seg or None)
    if ind.get("cotizacion") == "precio" and not _texto(ind.get("conversion_precio")):
        raise ErrorFicha(f"{F}: índice cotizado en precio sin conversión a diferencial declarada")

    if "diferencial_indice" in (ent.get("series_rol") or {}):
        fh, xs = _serie_a_listas(ent["series_rol"]["diferencial_indice"], f"{F}: serie diferencial_indice")
        fechas, hist = _fechas(fh, f"{F}: serie diferencial_indice"), np.array(xs)
    else:
        h = _requerido_dict(v, "historia", F, "diferencial diario del índice con fechas")
        fechas = _fechas(h.get("fechas"), f"{F}: historia.fechas")
        hist = _vector(h.get("diferenciales_pb"), f"{F}: historia.diferenciales_pb")
        if len(hist) != len(fechas):
            raise ErrorFicha(f"{F}: historia no alineada con sus fechas")
    span = _anios(fechas[0], fechas[-1])
    if span < float(p["anios_minimos"]):
        raise ErrorFicha(f"{F}: historia de {span:.2f} años (< {p['anios_minimos']}): rechazo de la ficha")
    if span < float(p["ventana"]):
        lim.append(f"historia de {span:.2f} años (< {p['ventana']}): percentil con limitación")
    if not _texto(ind.get("enlace_series")):
        lim.append("enlace entre series on-the-run no declarado")
    if np.any(hist < 0):
        raise ErrorFicha(f"{F}: diferenciales negativos en la historia")
    s = float(hist[-1])

    # Recuperación: IG 0,40 por defecto; HY sin valor único en la ficha (rango 0,25–0,40) → debe declararse.
    rec = p["recuperacion"] if p["recuperacion"] is not None else v.get("recuperacion")
    if rec is None:
        if seg == "IG":
            rec = p["recuperacion_ig"]
        elif seg == "HY":
            lo, hi = p["recuperacion_hy"]
            raise ErrorFicha(f"{F}: índice HY sin «recuperacion» declarada (la ficha da el rango {lo}–{hi}, no un valor)")
        else:
            raise ErrorFicha(f"{F}: segmento del índice no declarado (IG o HY) y sin «recuperacion»")
    R = _rango(rec, f"{F}: recuperacion (en [0, 1))", 0, 1, abierto_hi=True)
    if seg == "HY":
        lo, hi = p["recuperacion_hy"]
        if not lo <= R <= hi:
            lim.append(f"recuperación {R} fuera del rango HY de la ficha ({lo}–{hi})")

    # (i) intensidad neutral al riesgo
    lam = s / PB_POR_UNIDAD / (1 - R)

    # (ii) pérdida esperada real
    imp = _requerido_dict(v, "impagos", F, "tasas de impago por rating y año con fuente, o tasa prevista")
    fuente = imp.get("fuente") if imp.get("fuente") is not None else p["fuente_impagos"]
    if not _texto(fuente):
        raise ErrorFicha(f"{F}: tasas de impago sin fuente declarada")
    if imp.get("pd_anual") is not None:
        pd_anual = _num(imp["pd_anual"], f"{F}: impagos.pd_anual")
        origen_pd = "tasa prevista aportada"
    else:
        rating = str(imp.get("rating_medio") or "")
        if not _texto(rating):
            raise ErrorFicha(f"{F}: impagos sin «pd_anual» ni «rating_medio»")
        tabla = _dict(imp.get("tasas_por_rating") or {}, f"{F}: impagos.tasas_por_rating").get(rating)
        if not isinstance(tabla, dict) or not tabla:
            raise ErrorFicha(f"{F}: faltan tasas de impago por año para el rating medio «{rating}»")
        anios_dados = imp.get("anios")
        anios_sel = [str(_entero(a, f"{F}: impagos.anios")) for a in _lista(anios_dados, f"{F}: impagos.anios")] \
            if anios_dados is not None else [str(k) for k in tabla]
        if not anios_sel:
            raise ErrorFicha(f"{F}: impagos.anios vacío")
        falta = [a for a in anios_sel if a not in {str(k) for k in tabla}]
        if falta:
            raise ErrorFicha(f"{F}: sin tasa de impago para los años {falta}")
        tabla_s = {str(k): x for k, x in tabla.items()}
        pd_anual = float(np.mean([_num(tabla_s[a], f"{F}: tasa de impago {a}") for a in anios_sel]))
        origen_pd = f"media histórica del rating {rating} ({len(anios_sel)} años)"
    if not 0 <= pd_anual <= 1:
        raise ErrorFicha(f"{F}: probabilidad de impago fuera de [0, 1]")
    el = pd_anual * (1 - R) * PB_POR_UNIDAD

    # (iii) prima de riesgo de crédito
    prima = s - el
    ratio = s / el if el > 0 else None
    if ratio is None:
        lim.append("pérdida esperada nula: ratio diferencial/pérdida no definido")

    # (iv) percentil frente a la historia (toda la disponible; ventana mínima 10 años)
    pos = _posicion(s, hist, f"{F}: historia")

    # (v) base CDS–contado
    cont = _requerido_dict(v, "contado", F, "diferencial al contado comparable (OAS o Z)")
    if not isinstance(cont.get("medida"), str) or cont["medida"].upper() not in ("OAS", "Z"):
        raise ErrorFicha(f"{F}: el diferencial al contado debe declarar medida OAS o Z")
    base = s - _num(cont.get("diferencial_pb"), f"{F}: contado.diferencial_pb")

    # (vi) pendiente 5–10, carry + roll-down y DV01
    pendiente = carry = rpv01 = None
    curva = v.get("curva_diferenciales")
    t5, t10 = (float(x) for x in p["plazos_pendiente"])
    if curva is not None:
        pc, vc = _nodos(curva, f"{F}: curva_diferenciales", "diferenciales_pb")
        s5 = _interp_o_none(pc, vc, t5, f"{F}: pendiente", lim)
        s10 = _interp_o_none(pc, vc, t10, f"{F}: pendiente", lim)
        pendiente = None if s5 is None or s10 is None else s10 - s5
    else:
        lim.append("sin curva de diferenciales por plazo: pendiente 5–10 no calculada")
    venc = v.get("vencimiento_anios")
    libre = v.get("tipo_libre")
    if venc is not None and libre is not None:
        T = _rango(venc, f"{F}: vencimiento_anios", 0, abierto_lo=True)
        r = math.log1p(_rango(libre, f"{F}: tipo_libre", -PCT, abierto_lo=True) / PCT)
        rpv01 = _rpv01(T, lam, r)
        hz = float(p["horizonte_carry_anios"])
        if curva is not None and T - hz > 0:
            s_ant = _interp_o_none(pc, vc, T - hz, f"{F}: roll-down", lim)
            if s_ant is not None:
                carry = s * hz + _rpv01(T - hz, lam, r) * (s - s_ant)
        if carry is None:
            lim.append("carry + roll-down no calculado (falta curva de diferenciales que cubra el plazo tras un año)")
        lim.append("DV01 con prima continua (aproximación al cupón estándar con pago inicial)")
    else:
        lim.append("sin vencimiento del índice o tipo libre de riesgo: DV01 y carry no calculados")

    return {"indice": ficha_indice,
            "diferencial_pb": s, "recuperacion": R, "lambda_pct_anual": lam * PCT,
            "pd_anual": pd_anual, "origen_pd": origen_pd, "fuente_impagos": fuente,
            "perdida_esperada_pb": el, "prima_pb": prima, "ratio_diferencial_perdida": ratio,
            "percentil": pos["percentil"], "z": pos["z"], "media_historica_pb": pos["media"], "anios_historia": span,
            "base_pb": base, "medida_contado": str(cont["medida"]).upper(), "pendiente_pb": pendiente,
            "carry_pb_anual": carry, "duracion_con_riesgo": rpv01,
            "dv01": None if rpv01 is None else rpv01 / PB_POR_UNIDAD}, lim


# ================================================================== TCV-VIXTS-001
def _estado(puntos: list[float]) -> str:
    """Estado con spot, F₁ y F₂: contango (F₂ > F₁ > spot), backwardation (F₂ < F₁ < spot), plana o mixta."""
    d = np.diff(puntos)
    if np.all(d > 0):
        return "contango"
    if np.all(d < 0):
        return "backwardation"
    if np.all(d == 0):
        return "plana"
    return "mixta"


def f_tcv_vixts(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """TCV-VIXTS-001 · Estructura de plazos del VIX y roll de sus futuros.

    Entradas en ``valores`` (puntos del índice):
    - ``spot``; ``futuros``: {"dias": [días naturales al vencimiento], "precios": [...]} con ≥ 2 vencimientos.
    - ``historia``: {"fechas", "spot", "f1", "f2", "rent_larga"?: [% por periodo de una exposición larga a
      vencimiento constante], "fuente_rentabilidades"?} de ≥ 3 años.
    - ``indices_plazo`` (opcional): {"VIX3M": x, ...} para los ratios spot/índice.
    ``series_rol``: ``indice_spot``, ``futuro_1``, ``futuro_2`` y ``rentabilidad_larga`` como historia.
    """
    F = "TCV-VIXTS-001"
    p = _parametros(F, params)
    v = ent.get("valores") or {}
    lim = list(ADVERTENCIAS[F])

    fut = _requerido_dict(v, "futuros", F, "precios y días al vencimiento")
    n_min = int(p["vencimientos_minimos"])
    precios = _vector(fut.get("precios"), f"{F}: futuros.precios", 0)
    if len(precios) < n_min:
        raise ErrorFicha(f"{F}: < {n_min} vencimientos de futuros: rechazo de la ficha")
    dias = _vector(fut.get("dias"), f"{F}: futuros.dias", n_min)
    if len(dias) != len(precios):
        raise ErrorFicha(f"{F}: días y precios de futuros de distinta longitud")
    if np.any(dias <= 0) or np.any(np.diff(dias) <= 0) or np.any(precios <= 0):
        raise ErrorFicha(f"{F}: días al vencimiento positivos y crecientes, y precios positivos")
    spot = _num(_requerido(v, "spot", F, "nivel del índice"), f"{F}: spot")
    if spot <= 0:
        raise ErrorFicha(f"{F}: spot no positivo")

    # Historia (≥ 3 años)
    roles = ent.get("series_rol") or {}
    if all(k in roles for k in ("indice_spot", "futuro_1", "futuro_2")):
        nombres_rol = ["indice_spot", "futuro_1", "futuro_2"] + (["rentabilidad_larga"] if "rentabilidad_larga" in roles else [])
        for k in nombres_rol:
            _serie_a_listas(roles[k], f"{F}: serie {k}")      # valida tipo, índice de fechas y valores finitos
        df = pd.concat([roles[k] for k in nombres_rol], axis=1, join="inner").dropna()
        fh = _fechas([i.date() for i in df.index], f"{F}: series_rol")
        hs, h1, h2 = (df.iloc[:, i].to_numpy(dtype=float) for i in range(3))
        hr = df.iloc[:, 3].to_numpy(dtype=float) if df.shape[1] > 3 else None
    else:
        h = _requerido_dict(v, "historia", F, "spot y dos futuros con fechas, ≥ 3 años")
        fh = _fechas(h.get("fechas"), f"{F}: historia.fechas")
        hs, h1, h2 = (_vector(h.get(k), f"{F}: historia.{k}") for k in ("spot", "f1", "f2"))
        hr = _vector(h["rent_larga"], f"{F}: historia.rent_larga") if h.get("rent_larga") is not None else None
        if hr is not None and not _texto(h.get("fuente_rentabilidades")):
            raise ErrorFicha(f"{F}: rentabilidades históricas sin «fuente_rentabilidades»")
        if any(len(x) != len(fh) for x in (hs, h1, h2)) or (hr is not None and len(hr) != len(fh)):
            raise ErrorFicha(f"{F}: historia no alineada con sus fechas")
    span = _anios(fh[0], fh[-1])
    if span < float(p["anios_minimos"]):
        raise ErrorFicha(f"{F}: historia de {span:.2f} años (< {p['anios_minimos']} de la entrada mínima)")

    # (i) curva y estado
    estado = _estado([spot, float(precios[0]), float(precios[1])])
    # (ii) ratios de la curva
    ratios: dict[str, float] = {"F1/spot": float(precios[0] / spot), "F2/F1": float(precios[1] / precios[0])}
    for nombre, x in _dict(v.get("indices_plazo") or {}, f"{F}: indices_plazo").items():
        val = _num(x, f"{F}: indices_plazo.{nombre}")
        if val <= 0:
            raise ErrorFicha(f"{F}: índice {nombre} no positivo")
        ratios[f"spot/{nombre}"] = spot / val
    # (iii) roll diario implícito del primer futuro; % mensual con mes = vencimiento constante (días)
    vc = _num(p["vencimiento_constante"], f"{F}: vencimiento_constante")
    roll_dia = float((precios[0] - spot) / dias[0])
    roll_pct_mes = float((precios[0] - spot) / precios[0] * vc / dias[0] * PCT)
    # (iv) futuro a vencimiento constante interpolado entre los dos contratos que lo rodean
    f_cm: float | None = None
    pesos: dict[str, float] | None = None
    for i in range(len(dias) - 1):
        if dias[i] <= vc <= dias[i + 1]:
            w = float((dias[i + 1] - vc) / (dias[i + 1] - dias[i]))
            f_cm = w * float(precios[i]) + (1 - w) * float(precios[i + 1])
            pesos = {f"F{i + 1}": w, f"F{i + 2}": 1 - w}
            break
    if f_cm is None:
        lim.append(f"los vencimientos no rodean {vc:g} días: no se extrapola el futuro a vencimiento constante")
        rent_larga = rent_corta = None
    else:
        rent_larga = (spot / f_cm - 1) * PCT
        rent_corta = -rent_larga

    # (v) percentiles, frecuencia de contango, rentabilidades por estado y ES de la exposición corta
    ventana = float(p["ventana_percentil"])
    sel = np.array([_anios(f, fh[-1]) <= ventana for f in fh])
    if span < ventana:
        lim.append(f"historia de {span:.2f} años (< {ventana:g}): percentil orientativo")
    pend_hist = (h2 - h1)[sel]
    pendiente = float(precios[1] - precios[0])
    pos = _posicion(pendiente, pend_hist, f"{F}: historia de la pendiente")
    contango_hist = (h2 > h1) & (h1 > hs)
    estados_hist = np.where(contango_hist, "contango", np.where((h2 < h1) & (h1 < hs), "backwardation", "otros"))
    por_estado: dict[str, Any] | None = None
    es_corta: float | None = None
    if hr is not None:
        por_estado = {}
        for e in ("contango", "backwardation", "otros"):
            m = estados_hist[:-1] == e                     # estado conocido al cierre anterior
            r_e = hr[1:][m]
            por_estado[e] = {"n": int(m.sum()), "larga_pct": float(np.mean(r_e)) if m.any() else None,
                             "corta_pct": float(-np.mean(r_e)) if m.any() else None}
        nivel = float(p["nivel_es"])
        if len(hr) >= int(p["observaciones_minimas_es"]):
            corta = -hr
            q = float(np.quantile(corta, 1 - nivel))
            es_corta = float(-np.mean(corta[corta <= q]))
        else:
            lim.append(f"{len(hr)} rentabilidades (< {p['observaciones_minimas_es']}, RISK-VAR-001): ES no calculado")
    else:
        lim.append("sin rentabilidades históricas de la exposición: rentabilidades por estado y ES no calculados")

    return {"curva_puntos": {"spot": spot, "futuros": [{"dias": float(d), "precio": float(x)} for d, x in zip(dias, precios)]},
            "estado": estado, "ratios": ratios, "roll_puntos_dia": roll_dia, "roll_pct_mensual": roll_pct_mes,
            "futuro_vencimiento_constante": f_cm, "pesos_interpolacion": pesos,
            "rentabilidad_esperada_larga_pct": rent_larga, "rentabilidad_esperada_corta_pct": rent_corta,
            "pendiente_puntos": pendiente, "percentil_pendiente": pos["percentil"], "z_pendiente": pos["z"],
            "media_pendiente": pos["media"], "frecuencia_contango": float(np.mean(contango_hist[sel])),
            "rentabilidades_por_estado": por_estado, "es_corta_pct": es_corta,
            "nivel_es": float(p["nivel_es"])}, lim


# ================================================================== TCV-TP-001
def _meses(f: date) -> int:
    return f.year * MESES_POR_ANIO + f.month


def acm_estimar(Y_pct: np.ndarray, plazos_m: np.ndarray, k: int) -> dict[str, Any]:
    """Modelo afín de regresiones lineales de Adrian, Crump y Moench (2013).

    Y_pct: T×N rendimientos cupón cero (% anual, capitalización anual) en las fechas mensuales; plazos_m: plazos en
    meses (incluye 1). Pasos: (1) k componentes principales de los rendimientos logarítmicos mensuales; (2) VAR(1)
    de los factores por MCO; (3) excesos de rentabilidad a 1 mes sobre [1, innovaciones, factores rezagados];
    (4) precios del riesgo λ₀, λ₁; (5) recursiones de A_n, B_n con y sin precios del riesgo.
    """
    F = "TCV-TP-001"
    Y = np.log1p(Y_pct / PCT) / MESES_POR_ANIO
    T, _N = Y.shape
    media = Y.mean(axis=0)
    Yc = Y - media
    val, vec = np.linalg.eigh(Yc.T @ Yc / T)
    W = vec[:, np.argsort(val)[::-1][:k]]
    for j in range(k):                                    # signo determinista de cada componente
        if W[int(np.argmax(np.abs(W[:, j]))), j] < 0:
            W[:, j] = -W[:, j]
    X = Yc @ W
    if np.linalg.matrix_rank(X) < k:
        raise ErrorFicha(f"{F}: la curva no tiene {k} factores independientes (componentes degenerados)")
    # (2) VAR(1)
    Z = np.column_stack([np.ones(T - 1), X[:-1]])
    coef = np.linalg.lstsq(Z, X[1:], rcond=None)[0]
    mu, Phi = coef[0], coef[1:].T
    V = X[1:] - Z @ coef
    Sigma = V.T @ V / (T - 1)
    # tipo corto r_t = δ₀ + δ₁'X_t
    i1 = int(np.where(plazos_m == 1)[0][0])
    r = Y[:, i1]
    d = np.linalg.lstsq(np.column_stack([np.ones(T), X]), r, rcond=None)[0]
    delta0, delta1 = float(d[0]), d[1:]
    # (3) excesos de rentabilidad a 1 mes: rx_{t+1}^{(n−1)} = −(n−1)·y_{t+1}^{(n−1)} + n·y_t^{(n)} − r_t
    mats = [int(n) for n in plazos_m if n >= 2]
    if len(mats) < k:
        raise ErrorFicha(f"{F}: {len(mats)} plazos para {k} factores; precios del riesgo no identificados")
    RX = np.empty((T - 1, len(mats)))
    for j, n in enumerate(mats):
        y_ant = np.array([np.interp(n - 1, plazos_m, fila) for fila in Y[1:]])
        RX[:, j] = -(n - 1) * y_ant + n * Y[:-1, list(plazos_m).index(n)] - r[:-1]
    Z2 = np.column_stack([np.ones(T - 1), V, X[:-1]])
    c2 = np.linalg.lstsq(Z2, RX, rcond=None)[0]
    a, beta, C = c2[0], c2[1:1 + k], c2[1 + k:].T          # a: M, β: k×M, C: M×k
    E = RX - Z2 @ c2
    sigma2 = float(np.sum(E ** 2) / E.size)
    # (4) precios del riesgo
    Bstar = np.array([np.outer(beta[:, j], beta[:, j]).ravel() for j in range(len(mats))])
    bb = beta @ beta.T
    if np.linalg.matrix_rank(bb) < k:
        raise ErrorFicha(f"{F}: exposiciones de los excesos a los factores colineales")
    proy = np.linalg.solve(bb, beta)
    lam0 = proy @ (a + (Bstar @ Sigma.ravel() + sigma2) / 2)
    lam1 = proy @ C
    return {"X": X, "mu": mu, "Phi": Phi, "Sigma": Sigma, "sigma2": sigma2, "delta0": delta0, "delta1": delta1,
            "lambda0": lam0, "lambda1": lam1, "k": k}


def acm_cargas(n_max: int, mu: np.ndarray, Phi: np.ndarray, Sigma: np.ndarray, sigma2: float,
               lam0: np.ndarray, lam1: np.ndarray, delta0: float, delta1: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Recursiones de ACM (precio logarítmico ln P^(n) = A_n + B_n'X_t), con A_1 = −δ₀ y B_1 = −δ₁:
    A_n = A_{n−1} + B_{n−1}'(μ − λ₀) + ½(B_{n−1}'ΣB_{n−1} + σ²) − δ₀;  B_n' = B_{n−1}'(Φ − λ₁) − δ₁'."""
    A = np.zeros(n_max + 1)
    B = np.zeros((n_max + 1, len(mu)))
    A[1], B[1] = -delta0, -delta1
    for n in range(2, n_max + 1):
        Bp = B[n - 1]
        A[n] = A[n - 1] + Bp @ (mu - lam0) + (Bp @ Sigma @ Bp + sigma2) / 2 - delta0
        B[n] = Bp @ (Phi - lam1) - delta1
    return A, B


def _a_pct(y_log_mes: np.ndarray) -> np.ndarray:
    """Rendimiento logarítmico mensual → % anual con capitalización anual."""
    return np.expm1(y_log_mes * MESES_POR_ANIO) * PCT


def _historia_tp(serie: np.ndarray, fechas: list[date], objetivo: float, lim: list[str], que: str) -> dict[str, Any]:
    span = (_meses(fechas[-1]) - _meses(fechas[0])) / MESES_POR_ANIO
    if span < objetivo:
        lim.append(f"{que}: historia de {span:.2f} años (< {objetivo:g}): percentil orientativo")
    out = _posicion(float(serie[-1]), serie, que)
    out["anios"] = span
    return out


def _tp_acm(v: dict[str, Any], p: dict[str, Any], lim: list[str]) -> dict[str, Any]:
    F = "TCV-TP-001"
    k = int(p["n_factores"])
    c = _requerido_dict(v, "curva", F, "curva cupón cero mensual con fechas, plazos_meses y rendimientos")
    # «Entradas mínimas»: vencimientos de 1 a 10 años (en meses: del tipo corto a 1 mes hasta 120 meses, ambos
    # incluidos). Acotar los plazos acota también el tamaño del panel y de las recursiones.
    min_m = int(p["plazo_minimo_meses"])
    max_m = int(p["plazo_maximo_anios"]) * MESES_POR_ANIO
    plazos = _vector(c.get("plazos_meses"), f"{F}: curva.plazos_meses", 2)
    if np.any(plazos != np.round(plazos)) or np.any(np.diff(plazos) <= 0) or plazos[0] != min_m:
        raise ErrorFicha(f"{F}: plazos en meses enteros, crecientes y empezando en {min_m} (tipo corto a 1 mes)")
    if plazos[-1] != max_m:
        raise ErrorFicha(f"{F}: la curva debe llegar a {p['plazo_maximo_anios']} años ({max_m} meses) y no pasar de ahí "
                         f"(último plazo: {plazos[-1]:g} meses)")
    fechas = _fechas(c.get("fechas"), f"{F}: curva.fechas")
    Y = _matriz(c.get("rendimientos"), len(fechas), len(plazos), f"{F}: curva.rendimientos")
    meses = [_meses(f) for f in fechas]
    if any(b - a != 1 for a, b in itertools.pairwise(meses)):
        raise ErrorFicha(f"{F}: la curva debe ser mensual y sin huecos")
    if p["ventana"] is not None:
        n_v = int(_num(p["ventana"], f"{F}: ventana") * MESES_POR_ANIO) + 1
        fechas, Y = fechas[-n_v:], Y[-n_v:]
    span = (len(fechas) - 1) / MESES_POR_ANIO
    if span < float(p["anios_minimos"]):
        raise ErrorFicha(f"{F}: {span:.2f} años de curva mensual (< {p['anios_minimos']}): rechazo de la ficha")
    if span < float(p["anios_entrada_minima"]):
        lim.append(f"curva de {span:.2f} años (< {p['anios_entrada_minima']}): estimación con limitación")
    if np.any(Y <= -PCT):
        raise ErrorFicha(f"{F}: rendimientos ≤ −100 %")

    est = acm_estimar(Y, plazos.astype(int), k)
    pz = [round(float(t) * MESES_POR_ANIO) for t in p["plazos_prima"]]
    n_max = int(max(max(pz), plazos[-1]))
    A, B = acm_cargas(n_max, est["mu"], est["Phi"], est["Sigma"], est["sigma2"], est["lambda0"], est["lambda1"],
                      est["delta0"], est["delta1"])
    cero = np.zeros_like(est["lambda0"])
    An, Bn = acm_cargas(n_max, est["mu"], est["Phi"], est["Sigma"], est["sigma2"], cero, np.zeros_like(est["lambda1"]),
                        est["delta0"], est["delta1"])
    X = est["X"]

    def rend(Acar: np.ndarray, Bcar: np.ndarray, n: int) -> np.ndarray:
        return _a_pct(-(Acar[n] + X @ Bcar[n]) / n)

    # verificación: error de ajuste en todos los plazos observados
    ajustado_obs = np.column_stack([rend(A, B, int(n)) for n in plazos])
    err = (ajustado_obs - Y) * PB_POR_PUNTO
    rmse = float(np.sqrt(np.mean(err ** 2)))
    max_err = float(np.max(np.abs(err)))
    tope = float(p["error_ajuste_max_pb"])
    if not rmse < tope:
        raise ErrorFicha(f"{F}: ACM no verificado: error de ajuste {rmse:.3f} pb ≥ {tope:g} pb (use metodo publicado o encuesta)")

    prima: dict[str, float] = {}
    neutral: dict[str, float] = {}
    ajustado: dict[str, float] = {}
    observado: dict[str, float] = {}
    serie: dict[str, list[float]] = {}
    pos: dict[str, Any] = {}
    cambios: dict[str, Any] = {}
    for t, n in zip(p["plazos_prima"], pz):
        clave = _clave_plazo(t)
        y_aj, y_rn = rend(A, B, n), rend(An, Bn, n)
        tp = (y_aj - y_rn) * PB_POR_PUNTO
        resid = float(np.max(np.abs(tp / PB_POR_PUNTO + y_rn - y_aj)))
        if resid > float(p["tolerancia"]) * float(np.max(np.abs(y_aj))):
            raise ErrorFicha(f"{F}: identidad prima + neutral = ajustado no se cumple ({resid:g})")
        prima[clave], neutral[clave], ajustado[clave] = float(tp[-1]), float(y_rn[-1]), float(y_aj[-1])
        observado[clave] = float(np.interp(n, plazos, Y[-1]))
        serie[clave] = [float(x) for x in tp]
        pos[clave] = _historia_tp(tp, fechas, float(p["anios_entrada_minima"]), lim, f"prima a {clave} años")
        cambios[clave] = {"desde": fechas[-2].isoformat(), "cambio_ajustado_pb": float((y_aj[-1] - y_aj[-2]) * PB_POR_PUNTO),
                          "senda_esperada_pb": float((y_rn[-1] - y_rn[-2]) * PB_POR_PUNTO),
                          "prima_pb": float(tp[-1] - tp[-2])}
    return {"metodo": "ACM", "n_factores": k, "fecha": fechas[-1].isoformat(), "prima_pb": prima,
            "rendimiento_neutral_pct": neutral, "rendimiento_ajustado_pct": ajustado,
            "rendimiento_observado_pct": observado, "percentiles": pos, "descomposicion_cambios_pb": cambios,
            "serie": {"fechas": [f.isoformat() for f in fechas], "prima_pb": serie},
            "error_ajuste_pb": {"rmse": rmse, "max_abs": max_err, "tope": tope},
            "precios_riesgo": {"lambda0": [float(x) for x in est["lambda0"]],
                               "lambda1": [[float(x) for x in fila] for fila in est["lambda1"]]},
            "sigma2_errores": est["sigma2"]}


def _tp_publicado(ent: dict[str, Any], v: dict[str, Any], p: dict[str, Any], lim: list[str]) -> dict[str, Any]:
    F = "TCV-TP-001"
    sp = v.get("serie_publicada")
    roles = {str(r)[len("prima_publicada_"):]: s for r, s in (ent.get("series_rol") or {}).items()
             if str(r).startswith("prima_publicada_")}
    if roles:
        if not isinstance(sp, dict) or not _texto(sp.get("fuente")):
            raise ErrorFicha(f"{F}: serie publicada sin fuente (declárese «serie_publicada.fuente»)")
        historias = {clave: _serie_a_listas(s, f"{F}: serie prima_publicada_{clave}") for clave, s in roles.items()}
        rends: dict[str, Any] = {}
    else:
        if not isinstance(sp, dict) or not _texto(sp.get("fuente")) or not sp.get("primas_pb"):
            raise ErrorFicha(f"{F}: metodo publicado necesita «serie_publicada» con fuente, fechas y primas_pb")
        fechas = _fechas(sp.get("fechas"), f"{F}: serie_publicada.fechas")
        historias = {}
        for clave, xs in _dict(sp["primas_pb"], f"{F}: serie_publicada.primas_pb").items():
            a = _vector(xs, f"{F}: serie publicada {clave}")
            if len(a) != len(fechas):
                raise ErrorFicha(f"{F}: serie publicada {clave} no alineada con sus fechas")
            historias[str(clave)] = (fechas, [float(x) for x in a])
        rends = _dict(sp.get("rendimientos_pct") or {}, f"{F}: serie_publicada.rendimientos_pct")
    prima: dict[str, float] = {}
    neutral: dict[str, float | None] = {}
    pos: dict[str, Any] = {}
    cambios: dict[str, Any] = {}
    for clave, (fh, xs) in historias.items():
        fh = _fechas(fh, f"{F}: serie publicada {clave}")
        span = _anios(fh[0], fh[-1])
        if span < float(p["anios_minimos"]):
            raise ErrorFicha(f"{F}: serie publicada {clave} de {span:.2f} años (< {p['anios_minimos']}): rechazo de la ficha")
        a = np.array(xs, dtype=float)
        prima[clave] = float(a[-1])
        pos[clave] = _posicion(float(a[-1]), a, f"{F}: serie publicada {clave}")
        if span < float(p["anios_entrada_minima"]):
            lim.append(f"serie publicada {clave} de {span:.2f} años (< {p['anios_entrada_minima']}): percentil orientativo")
        if clave in rends:
            y = _vector(rends[clave], f"{F}: rendimientos {clave}")
            if len(y) != len(a):
                raise ErrorFicha(f"{F}: rendimientos {clave} no alineados con la serie publicada")
            neutral[clave] = float(y[-1] - a[-1] / PB_POR_PUNTO)
            cambios[clave] = {"desde": fh[-2].isoformat(), "cambio_ajustado_pb": float((y[-1] - y[-2]) * PB_POR_PUNTO),
                              "prima_pb": float(a[-1] - a[-2]),
                              "senda_esperada_pb": float((y[-1] - y[-2]) * PB_POR_PUNTO - (a[-1] - a[-2]))}
        else:
            neutral[clave] = None
            lim.append(f"sin rendimientos para el plazo {clave}: rendimiento neutral y descomposición no calculados")
    return {"metodo": "publicado", "fuente": sp["fuente"], "prima_pb": prima, "rendimiento_neutral_pct": neutral,
            "percentiles": pos, "descomposicion_cambios_pb": cambios or None,
            "serie": {clave: {"fechas": [str(f) for f in fh], "prima_pb": [float(x) for x in xs]}
                      for clave, (fh, xs) in historias.items()}}


def _tp_encuesta(v: dict[str, Any], p: dict[str, Any], lim: list[str]) -> dict[str, Any]:
    F = "TCV-TP-001"
    enc = v.get("encuesta")
    if not isinstance(enc, dict) or not _texto(enc.get("fuente")) or enc.get("fecha") is None:
        raise ErrorFicha(f"{F}: metodo encuesta necesita «encuesta» con fuente, fecha y tipos cortos esperados")
    _fecha(enc["fecha"], f"{F}: encuesta.fecha")
    esperados = _vector(enc.get("tipos_cortos_esperados_pct"), f"{F}: encuesta.tipos_cortos_esperados_pct")
    rends = _requerido_dict(v, "rendimientos_pct", F, "rendimiento observado por plazo, {\"10\": %}")
    prima: dict[str, float | None] = {}
    neutral: dict[str, float | None] = {}
    for t in p["plazos_prima"]:
        clave, n = _clave_plazo(t), round(float(t))
        if clave not in rends or n > len(esperados):
            prima[clave] = neutral[clave] = None
            lim.append(f"plazo {clave}: sin rendimiento o sin {n} años de tipos esperados: prima no calculada")
            continue
        media_esperada = float(np.mean(esperados[:n]))
        neutral[clave] = media_esperada
        prima[clave] = (_num(rends[clave], f"{F}: rendimiento {clave}") - media_esperada) * PB_POR_PUNTO
    if all(x is None for x in prima.values()):
        raise ErrorFicha(f"{F}: ningún plazo con rendimiento y tipos esperados suficientes")
    lim.append("aproximación por encuestas: sin percentiles ni descomposición de cambios (no hay historia del modelo)")
    return {"metodo": "encuesta", "fuente": enc["fuente"], "fecha": str(enc["fecha"]), "prima_pb": prima,
            "rendimiento_neutral_pct": neutral, "percentiles": None, "descomposicion_cambios_pb": None}


def f_tcv_tp(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """TCV-TP-001 · Prima por plazo.

    ``params["metodo"]``: ``ACM`` (por defecto), ``publicado`` o ``encuesta``.
    - ACM: ``valores["curva"]`` = {"fechas": [ISO mensuales consecutivas], "plazos_meses": [1, ..., ≥ 120],
      "rendimientos": [[% cupón cero, capitalización anual] por fecha]} con ≥ 10 años. Si además llega
      ``serie_publicada`` o ``encuesta``, se calcula como segunda vía.
    - publicado: ``valores["serie_publicada"]`` = {"fuente", "fechas", "primas_pb": {"10": [...]},
      "rendimientos_pct"?: {"10": [...]}} (ACM o Kim-Wright como dato con fuente); o ``series_rol`` con roles
      ``prima_publicada_<plazo>`` y la fuente en ``serie_publicada.fuente``.
    - encuesta: ``valores["encuesta"]`` = {"fuente", "fecha", "tipos_cortos_esperados_pct": [año 1..10]} y
      ``valores["rendimientos_pct"]`` = {"10": %, ...}.
    """
    F = "TCV-TP-001"
    p = _parametros(F, params)
    v = ent.get("valores") or {}
    lim = list(ADVERTENCIAS[F])
    metodo = str(p["metodo"]).strip().lower()
    if metodo == "acm":
        res = _tp_acm(v, p, lim)
        segunda: dict[str, Any] | None = None
        alt = None
        try:
            if v.get("serie_publicada") is not None:
                alt = _tp_publicado(ent, v, p, [])
            elif v.get("encuesta") is not None:
                alt = _tp_encuesta(v, p, [])
        except ErrorFicha as e:
            lim.append(f"segunda vía no calculada: {e}")
        if alt is not None:
            segunda = {"metodo": alt["metodo"], "fuente": alt["fuente"], "prima_pb": alt["prima_pb"],
                       "diferencia_pb": {c: (res["prima_pb"][c] - x if x is not None and c in res["prima_pb"] else None)
                                         for c, x in alt["prima_pb"].items()}}
        elif v.get("serie_publicada") is None and v.get("encuesta") is None:
            lim.append("segunda vía (serie publicada o encuesta) no aportada")
        res["segunda_via"] = segunda
        return res, lim
    if metodo == "publicado":
        return _tp_publicado(ent, v, p, lim), lim
    if metodo == "encuesta":
        return _tp_encuesta(v, p, lim), lim
    raise ErrorFicha(f"{F}: metodo «{p['metodo']}» no reconocido (ACM, publicado o encuesta)")


# ================================================================== registro de fichas
FICHAS: dict[str, dict[str, Any]] = {
    "TCV-SLOPE-001": {"fn": _blindar("TCV-SLOPE-001", f_tcv_slope), "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA",
                      "ri": "RI-PA de la pendiente y pendiente forward", "tol": 1e-8},
    "TCV-BEI-001": {"fn": _blindar("TCV-BEI-001", f_tcv_bei), "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA",
                    "ri": "Encuesta (inflación esperada) y RI-PA del breakeven", "tol": 1e-10},
    "TCV-CDS-001": {"fn": _blindar("TCV-CDS-001", f_tcv_cds), "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA",
                    "ri": "RI-MH y RI-PA del diferencial", "tol": 1e-8},
    "TCV-VIXTS-001": {"fn": _blindar("TCV-VIXTS-001", f_tcv_vixts), "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA",
                      "ri": "RI-MH de la pendiente y RI-PA del índice", "tol": 1e-10},
    "TCV-TP-001": {"fn": _blindar("TCV-TP-001", f_tcv_tp), "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA",
                   "ri": "RI-MH de la prima y RI-PA", "tol": 1e-6},
}


# ================================================================== datos sintéticos de los casos de control
def _fechas_semanales(inicio: date, n: int) -> list[str]:
    return [(pd.Timestamp(inicio) + pd.Timedelta(weeks=i)).date().isoformat() for i in range(n)]


def _fechas_mensuales(anio: int, n: int) -> list[str]:
    return [date(anio + i // MESES_POR_ANIO, i % MESES_POR_ANIO + 1, 1).isoformat() for i in range(n)]


def sintetico_slope(curva: Callable[[float, int], float], n: int = 270) -> dict[str, Any]:
    """Historia semanal (> 5 años) de una curva de 6 nodos dada por curva(plazo, semana) y cuatro regresores."""
    plazos = [0.25, 1, 2, 5, 10, 30]
    fechas = _fechas_semanales(date(2019, 1, 4), n)
    regs = {nombre: {"serie": [math.sin((i + 1) * (j + 1) * 0.37) + 0.1 * j for i in range(n)],
                     "conocible_desde": list(fechas), "fuente": "sintética de control"}
            for j, nombre in enumerate(PARAMETROS_POR_DEFECTO["TCV-SLOPE-001"]["regresores"])}
    return {"historia_curva": {"fechas": fechas, "plazos": plazos,
                               "rendimientos": [[curva(t, i) for t in plazos] for i in range(n)]},
            "regresores": regs}


def sintetico_vixts(spot: float, precios: list[float], dias: list[float], n: int = 160) -> dict[str, Any]:
    """Curva actual y una historia semanal de ≥ 3 años con alternancia de estados."""
    fechas = _fechas_semanales(date(2021, 1, 1), n)
    hs = [spot + math.sin(i * 0.3) for i in range(n)]
    h1 = [x + math.sin(i * 0.11) for i, x in enumerate(hs)]
    h2 = [x + 0.5 * math.sin(i * 0.11) + 0.3 for i, x in enumerate(h1)]
    return {"spot": spot, "futuros": {"dias": dias, "precios": precios},
            "historia": {"fechas": fechas, "spot": hs, "f1": h1, "f2": h2}}


def sintetico_cds(diferenciales: list[float], pd_anual: float, recuperacion: float | None = None) -> dict[str, Any]:
    n = len(diferenciales)
    fechas = _fechas_semanales(date(2015, 1, 2), n)
    v: dict[str, Any] = {"indice": {"nombre": "índice IG sintético", "serie": 1, "version": 1, "segmento": "IG",
                                    "enlace_series": "serie única de control"},
                         "historia": {"fechas": fechas, "diferenciales_pb": diferenciales},
                         "impagos": {"fuente": "tasa sintética de control", "pd_anual": pd_anual},
                         "contado": {"diferencial_pb": diferenciales[-1], "medida": "OAS"}}
    if recuperacion is not None:
        v["recuperacion"] = recuperacion
    return v


def sintetico_acm(n_meses: int = 241, plazos: list[int] | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    """Curva mensual generada por un modelo afín de 3 factores conocido (precios del riesgo λ₀, λ₁ fijados).

    El camino de los factores es determinista (innovaciones senoidales); la convexidad usa la Σ del VAR(1) estimado
    sobre ese camino, de modo que los rendimientos son exactamente afines con los mismos parámetros que ACM debe
    recuperar. Devuelve (valores, verdad) con la prima «verdadera» a 2, 5 y 10 años.
    """
    plazos = plazos or list(range(1, 121))
    k = 3
    Phi = np.diag([0.98, 0.9, 0.8])
    mu = np.zeros(k)
    PhiQ = np.diag([0.995, 0.95, 0.85])
    muQ = np.array([-1e-5, -2e-5, 0.0])
    delta0, delta1 = 0.03 / MESES_POR_ANIO, np.ones(k)
    X = np.zeros((n_meses, k))
    for t in range(1, n_meses):
        inn = 3e-4 * np.array([math.sin(t * 1.3), math.sin(t * 2.7 + 1), math.sin(t * 0.61 + 2)])
        X[t] = mu + Phi @ X[t - 1] + inn
    Z = np.column_stack([np.ones(n_meses - 1), X[:-1]])
    coef = np.linalg.lstsq(Z, X[1:], rcond=None)[0]
    V = X[1:] - Z @ coef
    Sigma = V.T @ V / (n_meses - 1)
    mu_hat, Phi_hat = coef[0], coef[1:].T
    nmax = max(plazos + [120])
    A, B = acm_cargas(nmax, muQ, PhiQ, Sigma, 0.0, np.zeros(k), np.zeros((k, k)), delta0, delta1)
    An, Bn = acm_cargas(nmax, mu_hat, Phi_hat, Sigma, 0.0, np.zeros(k), np.zeros((k, k)), delta0, delta1)
    Y = np.column_stack([_a_pct(-(A[n] + X @ B[n]) / n) for n in plazos])
    verdad = {_clave_plazo(t): float((_a_pct(-(A[n] + X[-1] @ B[n]) / n) - _a_pct(-(An[n] + X[-1] @ Bn[n]) / n))
                                     * PB_POR_PUNTO)
              for t, n in ((2, 24), (5, 60), (10, 120))}
    valores = {"curva": {"fechas": _fechas_mensuales(2000, n_meses), "plazos_meses": plazos,
                         "rendimientos": [[float(x) for x in fila] for fila in Y]}}
    return valores, verdad


def _identidad_tp(r: dict[str, Any]) -> bool:
    return all(abs(r["prima_pb"][c] / PB_POR_PUNTO + r["rendimiento_neutral_pct"][c] - r["rendimiento_ajustado_pct"][c])
               <= 1e-10 for c in r["prima_pb"])


def _coherencia_5y5y(r: dict[str, Any]) -> bool:
    b5, b10 = r["breakevens_contado_forward_pct"]["5"] / PCT, r["breakevens_contado_forward_pct"]["10"] / PCT
    f = r["forward_5y5y_pct"] / PCT
    return math.isclose((1 + b5) ** 5 * (1 + f) ** 5, (1 + b10) ** 10, rel_tol=1e-10)


_ENCUESTA = {"fecha": "2024-06-01", "fuente": "encuesta sintética de control",
             "horizontes": {"2": 2.0, "5": 2.1, "10": 2.2, "5y5y": 2.3}}
_ACM, _ACM_VERDAD = sintetico_acm()
_PLANA = sintetico_slope(lambda t, i: 3.0)
_PENDIENTE = sintetico_slope(lambda t, i: 2.0 + 0.1 * t + 0.002 * i)
_HIST_CDS = [80.0 + 30 * math.sin(i * 0.05) for i in range(300)] + [140.0]

CASOS_CONTROL: dict[str, list[dict[str, Any]]] = {
    "TCV-SLOPE-001": [
        {"nombre": "curva plana ⇒ pendiente 0 y rolldown 0", "datos": [{"valores": _PLANA}], "parametros": {},
         "comprobar": lambda r: r["tramos"]["2s10s"]["pendiente_pb"] == 0
         and r["tramos"]["2s10s"]["carry_neutral_dv01_pb"]["rolldown_pb"] == 0
         and r["tramos"]["2s10s"]["carry_neutral_dv01_pb"]["carry_pb"] == 0},
        {"nombre": "segunda vía: −β₁ de NSS con el mismo signo que la pendiente directa",
         "datos": [{"valores": {**_PENDIENTE, "beta1_nss": {"valor": -1.5, "fuente": "FIR-CURVE-001 sintética"}}}],
         "parametros": {},
         "comprobar": lambda r: r["tramos"]["2s10s"]["pendiente_pb"] > 0 and r["segunda_via"]["signo_coherente"]["2s10s"]},
    ],
    "TCV-BEI-001": [
        {"nombre": "nominal = real ⇒ BE = 0",
         "datos": [{"valores": {"curva_nominal": {"plazos": [1, 2, 5, 10, 20], "rendimientos": [3.0, 3.1, 3.4, 3.8, 4.0]},
                                "curva_real": {"plazos": [1, 2, 5, 10, 20], "rendimientos": [3.0, 3.1, 3.4, 3.8, 4.0],
                                               "indice_referencia": "IPC sintético"},
                                "encuestas": _ENCUESTA}}],
         "parametros": {"ajuste_estacional": False},
         "comprobar": lambda r: all(x == 0 for x in r["breakevens_pct"].values()) and r["forward_5y5y_pct"] == 0},
        {"nombre": "5y5y coherente con los breakevens al contado",
         "datos": [{"valores": {"curva_nominal": {"plazos": [1, 2, 5, 10, 20], "rendimientos": [3.0, 3.2, 3.6, 4.1, 4.3]},
                                "curva_real": {"plazos": [1, 2, 5, 10, 20], "rendimientos": [1.2, 1.1, 1.3, 1.6, 1.7],
                                               "indice_referencia": "IPC sintético"},
                                "encuestas": _ENCUESTA}}],
         "parametros": {"ajuste_estacional": False}, "comprobar": _coherencia_5y5y},
    ],
    "TCV-CDS-001": [
        # Con prima 0, la intensidad neutral al riesgo λ = s/(1 − R) coincide con la PD real (λ·(1 − R) = s = PD·(1 − R)).
        {"nombre": "s = PD·(1 − R) ⇒ prima 0 (y λ neutral al riesgo = PD)",
         "datos": [{"valores": sintetico_cds([100.0] * 270, 0.0125, 0.2)}],
         "parametros": {}, "comprobar": lambda r: math.isclose(r["prima_pb"], 0.0, abs_tol=1e-10)
         and math.isclose(r["lambda_pct_anual"] / PCT, r["pd_anual"], rel_tol=1e-12)
         and math.isclose(r["ratio_diferencial_perdida"], 1.0, rel_tol=1e-12)},
        {"nombre": "percentil del máximo histórico = 1", "datos": [{"valores": sintetico_cds(_HIST_CDS, 0.01)}],
         "parametros": {}, "comprobar": lambda r: r["percentil"] == 1.0},
    ],
    "TCV-VIXTS-001": [
        {"nombre": "curva plana igual al spot ⇒ roll 0",
         "datos": [{"valores": sintetico_vixts(18.0, [18.0, 18.0, 18.0], [20, 50, 80])}], "parametros": {},
         "comprobar": lambda r: r["roll_puntos_dia"] == 0 and r["roll_pct_mensual"] == 0 and r["estado"] == "plana"},
        {"nombre": "interpolación a 30 días coherente: vencimiento en 30 días ⇒ F₃₀ = F₁",
         "datos": [{"valores": sintetico_vixts(15.0, [16.5, 17.8], [30, 58])}], "parametros": {},
         "comprobar": lambda r: r["futuro_vencimiento_constante"] == 16.5},
        {"nombre": "interpolación a 30 días entre los dos contratos (lineal en días)",
         "datos": [{"valores": sintetico_vixts(15.0, [16.0, 18.0], [20, 40])}], "parametros": {},
         "comprobar": lambda r: math.isclose(r["futuro_vencimiento_constante"], 17.0, rel_tol=1e-12)},
        # Contrapartida no plana del caso «curva plana ⇒ roll 0»: el roll sale de F₁ y del spot, no de F₂.
        {"nombre": "roll del primer futuro = (F₁ − spot)/días al vencimiento",
         "datos": [{"valores": sintetico_vixts(15.0, [16.0, 18.0], [20, 40])}], "parametros": {},
         "comprobar": lambda r: math.isclose(r["roll_puntos_dia"], (16.0 - 15.0) / 20, rel_tol=1e-12)
         and math.isclose(r["roll_pct_mensual"], (16.0 - 15.0) / 16.0 * 30 / 20 * PCT, rel_tol=1e-12)},
    ],
    "TCV-TP-001": [
        {"nombre": "prima + rendimiento neutral = rendimiento ajustado", "datos": [{"valores": _ACM}],
         "parametros": {"n_factores": 3}, "comprobar": _identidad_tp},
        {"nombre": "error de ajuste de la curva < 5 pb", "datos": [{"valores": _ACM}], "parametros": {"n_factores": 3},
         "comprobar": lambda r: r["error_ajuste_pb"]["rmse"] < 5 and r["error_ajuste_pb"]["max_abs"] < 5},
        {"nombre": "ACM recupera la prima del modelo afín generador", "datos": [{"valores": _ACM}],
         "parametros": {"n_factores": 3},
         "comprobar": lambda r: all(math.isclose(r["prima_pb"][c], _ACM_VERDAD[c], abs_tol=1e-6) for c in _ACM_VERDAD)},
        {"nombre": "segunda vía por encuestas: prima = rendimiento − media de tipos esperados",
         "datos": [{"valores": {"encuesta": {"fuente": "encuesta sintética", "fecha": "2024-06-01",
                                             "tipos_cortos_esperados_pct": [3.0] * 10},
                                "rendimientos_pct": {"2": 3.2, "5": 3.5, "10": 4.0}}}],
         "parametros": {"metodo": "encuesta"},
         "comprobar": lambda r: math.isclose(r["prima_pb"]["10"], 100.0, rel_tol=1e-12)
         and math.isclose(r["prima_pb"]["2"], 20.0, rel_tol=1e-12)},
    ],
}
