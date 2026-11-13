"""Fichas del Motor del Bloque A: inmobiliario cotizado, materias primas, criptoactivos y alternativos (grupo P).

T-112 (Motor Fase 2). Fuente de verdad: «Catálogo de cálculos del Motor - V5.0», fichas REI-CAP-001, REI-FFO-001,
REI-NAV-001 (sección 12), CMD-INV-001, CMD-RETDEC-001 (sección 11), CHR-FLOW-001, CHR-FUND-001 (sección 13) y
ALT-DESMOOTH-001 (sección 14), con las convenciones de su sección 3.

Convenciones de este módulo:

- Todas las entradas llegan en línea en ``ent["valores"]`` (bloques con ``fecha`` en texto ISO). ALT-DESMOOTH-001 acepta
  además niveles de índice en ``ent["series_rol"]`` (roles ``indice_suavizado`` y ``mercado``).
- Tipos, rentabilidades, cap rates y primas de entrada en **tanto por uno** (0,05 = 5 %). Las salidas llevan la unidad
  que pide la ficha en el sufijo de la clave: ``_pct`` en %, ``_pb`` en puntos básicos; sin sufijo, tanto por uno o
  la unidad de origen (moneda, unidades físicas, veces).
- Recuento de días Real/365 (3.1). Percentil histórico = proporción de la historia ≤ valor (como
  ``operaciones.posicion_historica``); z-score con desviación muestral (n − 1, ST-DESC-001); si la dispersión es nula,
  el z queda ``None`` y se declara.
- Falla cerrado: lo que falta o es incoherente lanza ``ErrorFicha`` con el motivo; un bloque opcional del método sin
  datos se entrega como ``None`` y se declara en las limitaciones, nunca se rellena con 0. Ningún resultado lleva
  cifras no finitas (lo comprueba la envoltura ``_cerrado``).
- Umbrales fijos (T-106, H-14): los umbrales de rechazo y de limitación y los rangos admitidos están en ``UMBRALES`` y
  una petición que traiga uno se rechaza. Cada parámetro de la petición tiene tipo y rango (T-108, H-24).
- Las «Supuestos y limitaciones» de cada ficha van en ``resultado["advertencias"]`` (``ADVERTENCIAS``), no como
  limitaciones: las limitaciones solo señalan problemas de los datos de esa petición.
- Determinista: ninguna de estas fichas usa azar (todas declaran semilla ``null``); los diccionarios se recorren en
  orden de claves. El redondeo de entrega lo hace la capa de servicio.

Interfaz de cada manejador: ``fn(ent, params) -> (resultado, limitaciones)``.
"""
from __future__ import annotations

import math
from collections.abc import Callable
from functools import wraps
from typing import Any

import numpy as np
import pandas as pd
from scipy import linalg, optimize

from .operaciones import ErrorFicha

Resultado = tuple[dict[str, Any], list[str]]
Manejador = Callable[[dict[str, Any], dict[str, Any]], Resultado]

# ------------------------------------------------------------------ conversiones de unidades (no son parámetros)
PB = 10_000            # pb por unidad (tanto por uno)
PCT = 100              # tanto por uno → %
DIAS_ANIO = 365        # 3.1: recuento Real/365; CHR-FUND-001: «× 365», «365/días»
HORAS_DIA = 24         # CHR-FUND-001: periodos por día = 24 h / duración del periodo («3 × 365 con periodos de 8 h»)
DIAS_SEMANA = 7
MESES_ANIO = 12
SEMANAS_ANIO = 52      # periodo estacional semanal (la semana ISO 53 se compara con la 52 de los años que no la tienen)
TRIMESTRES_ANIO = 4    # ALT-DESMOOTH-001: rentabilidades trimestrales → volatilidad % anual con √4
PERIODOS_ANIO = {"mensual": MESES_ANIO, "trimestral": TRIMESTRES_ANIO, "anual": 1}
FREQ_PANDAS = {"mensual": "M", "trimestral": "Q", "anual": "Y"}

# ------------------------------------------------------------------ parámetros por defecto (campo «Parámetros»)
PARAMETROS_POR_DEFECTO: dict[str, dict[str, Any]] = {
    # REI-CAP-001 · «Parámetros»: base_noi (adelantado); ventana (20 años).
    "REI-CAP-001": {"base_noi": "adelantado", "ventana": 20},
    # REI-FFO-001 · «Parámetros»: capex_mantenimiento (reportado; estimado como % de rentas si no). El % de rentas no
    # lo fija la ficha: lo aporta el solicitante en `capex_pct_rentas` (sin valor por defecto, [PROPUESTO] INC-T112-01).
    "REI-FFO-001": {"capex_mantenimiento": "reportado", "capex_pct_rentas": None},
    # REI-NAV-001 · «Parámetros»: nav_variante (EPRA NTA); cap_objetivo (implícito de REI-CAP-001 o null).
    "REI-NAV-001": {"nav_variante": "EPRA NTA", "cap_objetivo": None},
    # CMD-INV-001 · «Parámetros»: anos_estacional (5; 3–10); excluir_anos (ninguno).
    "CMD-INV-001": {"anos_estacional": 5, "excluir_anos": []},
    # CMD-RETDEC-001 · «Parámetros»: calendario_roll (el del índice); frecuencia (mensual).
    "CMD-RETDEC-001": {"calendario_roll": "indice", "frecuencia": "mensual"},
    # CHR-FLOW-001 · «Parámetros»: ventanas (5, 20 días); ventana_z (1 año).
    "CHR-FLOW-001": {"ventanas": [5, 20], "ventana_z": 1},
    # CHR-FUND-001 · «Parámetros»: ponderacion (interes_abierto); ventana_percentil (365 días).
    "CHR-FUND-001": {"ponderacion": "interes_abierto", "ventana_percentil": 365},
    # ALT-DESMOOTH-001 · «Parámetros»: metodo (Geltner; GLM); k (2; 1–3); phi (estimado o fijado).
    "ALT-DESMOOTH-001": {"metodo": "Geltner", "k": 2, "phi": None},
}

# Umbrales de rechazo y de limitación y rangos admitidos: los fija la ficha y la petición no los puede cambiar.
UMBRALES: dict[str, dict[str, Any]] = {
    # REI-CAP-001 · «Entradas mínimas»: historia ≥ 15 años; «Método»: percentil frente a ≥ 15 años (la ventana no
    # puede bajar de ahí). «Aclaración»: base del NOI ambigua (bases admitidas: adelantado o histórico); «Supuestos»:
    # definición del NOI antes o después de CAPEX, declarada.
    "REI-CAP-001": {"anios_historia_minimos": 15, "bases_noi": ("adelantado", "historico"),
                    "definiciones_noi": ("antes_capex", "despues_capex")},
    # REI-FFO-001 · «Entradas mínimas»: ≥ 3 ejercicios. Percentiles de múltiplos con ≥ 5 observaciones
    # (ST-DESC-001, «Entradas mínimas»). «Parámetros»: capex reportado o estimado como % de rentas, en [0, 1).
    "REI-FFO-001": {"ejercicios_minimos": 3, "observaciones_minimas_percentil": 5,
                    "capex_admitidos": ("reportado", "estimado"), "rango_capex_pct_rentas": (0.0, 1.0)},
    # REI-NAV-001 · «Aclaración y rechazo»: NAV de antigüedad > 12 meses. «Método»: percentil frente a ≥ 10 años.
    # Variantes de NAV de EPRA (Best Practices Recommendations, referencia de la ficha) [PROPUESTO].
    "REI-NAV-001": {"meses_antiguedad_nav_max": 12, "anios_percentil_minimos": 10,
                    "variantes_nav": ("EPRA NTA", "EPRA NRV", "EPRA NDV")},
    # CMD-INV-001 · «Aclaración y rechazo»: < 3 años. «Entradas mínimas»: ≥ 5 años (10 recomendados).
    # «Parámetros»: anos_estacional 3–10; el mínimo del rango (3) es también el mínimo de años previos con el mismo
    # periodo. Correlación con la pendiente de la curva con ≥ 5 observaciones (ST-DESC-001).
    "CMD-INV-001": {"anios_rechazo": 3, "anios_entrada_minima": 5, "anios_recomendados": 10,
                    "rango_anos_estacional": (3, 10), "anios_previos_minimos": 3,
                    "observaciones_minimas_correlacion": 5, "frecuencias_admitidas": ("semanal", "mensual")},
    # CMD-RETDEC-001 · «Parámetros»: calendario_roll (el del índice, o uno declarado con precios de contratos, según
    # «Entradas mínimas»); frecuencia (mensual; trimestral y anual [PROPUESTO]).
    "CMD-RETDEC-001": {"calendarios_admitidos": ("indice", "declarado"),
                       "frecuencias_admitidas": ("mensual", "trimestral", "anual")},
    # CHR-FLOW-001 · «Entradas mínimas»: ≥ 120 días. «Método»: crecimiento de stablecoins a 30 días. z-score con ≥ 2
    # observaciones (desviación muestral, ST-DESC-001).
    "CHR-FLOW-001": {"dias_minimos": 120, "dias_crecimiento_stablecoins": 30},
    # CHR-FUND-001 · «Aclaración y rechazo»: < 2 plataformas. «Entradas mínimas»: ≥ 90 días (≥ 1 año = 365 días para
    # percentiles). Ponderaciones: interés abierto (ficha) o igual [PROPUESTO]. Coherencia base–financiación con ≥ 5
    # observaciones para la correlación (ST-DESC-001).
    "CHR-FUND-001": {"plataformas_minimas": 2, "dias_minimos": 90, "dias_percentil_minimos": 365,
                     "ponderaciones_admitidas": ("interes_abierto", "igual"), "observaciones_minimas_correlacion": 5},
    # ALT-DESMOOTH-001 · «Aclaración y rechazo»: < 24 observaciones. «Entradas mínimas»: ≥ 40 (24 con limitación).
    # «Parámetros»: k 1–3; metodo Geltner o GLM; phi fijado en [0, 1) [PROPUESTO] (suavizado no negativo, 1 − φ ≠ 0).
    "ALT-DESMOOTH-001": {"observaciones_minimas": 24, "observaciones_entrada_minima": 40, "rango_k": (1, 3),
                         "metodos_admitidos": ("Geltner", "GLM"), "rango_phi": (0.0, 1.0)},
}

# Advertencias obligatorias de entrega («Supuestos y limitaciones» de cada ficha, literales).
ADVERTENCIAS: dict[str, list[str]] = {
    "REI-CAP-001": ["cap rates de tasación suavizados",
                    "definición de NOI (antes o después de CAPEX) declarada por el solicitante"],
    "REI-FFO-001": ["definiciones no homogéneas entre emisores (EPRA frente a Nareit)"],
    "REI-NAV-001": ["NAV retrasado (6–18 meses frente al mercado cotizado)", "no es precio objetivo",
                    "las sociedades individuales solo entran como componentes del agregado (1.6)"],
    "CMD-INV-001": ["cambios de definición y reservas estratégicas", "revisiones de datos",
                    "inventarios no observados (flotantes, China)"],
    "CMD-RETDEC-001": ["spot de referencia y contrato próximo pueden diferir (base física)"],
    "CHR-FLOW-001": ["flujos de ETF publicados con retraso", "acuñación de stablecoins no equivale a compra"],
    "CHR-FUND-001": ["plataformas con datos poco fiables", "liquidaciones en cascada"],
    "ALT-DESMOOTH-001": ["suavizado lineal y estable", "φ estimado con error"],
}


# ================================================================== utilidades comunes
def _num(x: Any, que: str) -> float:
    """Número finito o ErrorFicha (un booleano, un texto o un None no son números)."""
    if isinstance(x, bool) or not isinstance(x, (int, float, np.integer, np.floating)):
        raise ErrorFicha(f"{que}: falta o no es un número ({str(x)[:40]!r})")
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


def _texto(x: Any, que: str) -> str:
    if not isinstance(x, str) or not x.strip():
        raise ErrorFicha(f"{que}: falta o no es un texto")
    return x.strip()


def _opcion(x: Any, que: str, admitidas: tuple[str, ...]) -> str:
    """Texto que debe ser una de las opciones admitidas (sin distinguir mayúsculas ni espacios repetidos)."""
    normal = {" ".join(a.lower().split()): a for a in admitidas}
    if not isinstance(x, str) or " ".join(x.lower().split()) not in normal:
        raise ErrorFicha(f"{que}: «{str(x)[:40]}» no admitido (opciones: {', '.join(admitidas)})")
    return normal[" ".join(x.lower().split())]


def _dict(x: Any, que: str) -> dict[str, Any]:
    if not isinstance(x, dict) or not x:
        raise ErrorFicha(f"{que}: se esperaba un objeto (dict) no vacío")
    return x


def _lista(x: Any, que: str) -> list[Any]:
    if not isinstance(x, list) or not x:
        raise ErrorFicha(f"{que}: se esperaba una lista no vacía")
    return x


def _fecha(x: Any, que: str) -> pd.Timestamp:
    """Solo texto ISO o fecha; un número no es una fecha (no es epoch)."""
    if isinstance(x, bool) or not isinstance(x, (str, pd.Timestamp, np.datetime64)) and not hasattr(x, "isoformat"):
        raise ErrorFicha(f"{que}: fecha no válida ({str(x)[:40]!r}): se espera texto ISO o una fecha")
    try:
        t = pd.Timestamp(x)
    except (TypeError, ValueError, OverflowError):
        raise ErrorFicha(f"{que}: fecha no válida ({str(x)[:40]!r})") from None
    if pd.isna(t):
        raise ErrorFicha(f"{que}: fecha no válida ({str(x)[:40]!r})")
    return t.normalize() if t.tz is None else t.tz_convert(None).normalize()


def _tabla(filas: Any, campos: dict[str, tuple[float | None, bool]], que: str,
           opcionales: tuple[str, ...] = ()) -> pd.DataFrame:
    """Lista de dicts con «fecha» y los `campos` numéricos ({campo: (mínimo, mínimo_excluido)}) → tabla por fecha.

    Fechas repetidas se rechazan; los `opcionales` pueden faltar (quedan NaN en la tabla y se tratan aparte)."""
    filas = _lista(filas, que)
    fechas: list[pd.Timestamp] = []
    datos: dict[str, list[float]] = {c: [] for c in campos}
    for i, fila in enumerate(filas):
        if not isinstance(fila, dict):
            raise ErrorFicha(f"{que}[{i}]: se esperaba un objeto con «fecha»")
        fechas.append(_fecha(fila.get("fecha"), f"{que}[{i}].fecha"))
        for c, (lo, abierto) in campos.items():
            if c in opcionales and fila.get(c) is None:
                datos[c].append(math.nan)
            else:
                datos[c].append(_rango(fila.get(c), f"{que}[{i}].{c}", lo, abierto_lo=abierto))
    t = pd.DataFrame(datos, index=pd.DatetimeIndex(fechas)).sort_index()
    if t.index.has_duplicates:
        raise ErrorFicha(f"{que}: fechas repetidas")
    return t


def _anios(indice: pd.Index) -> float:
    return float((indice[-1] - indice[0]).days) / DIAS_ANIO


def _posicion(valor: float, historia: Any) -> dict[str, Any]:
    """Percentil (proporción ≤ valor), z con desviación muestral y media (RI-MH) del valor frente a su historia."""
    h = np.asarray(historia, dtype=float)
    if h.size < 2:
        raise ErrorFicha("posición histórica: se necesitan al menos 2 observaciones")
    sd = float(np.std(h, ddof=1)) if float(np.ptp(h)) > 0 else 0.0
    media = float(np.mean(h))
    return {"percentil": float(np.mean(h <= valor)), "z": (float(valor) - media) / sd if sd > 0 else None,
            "media": media, "n": int(h.size)}


def _error_rel(a: float, b: float, escala: float) -> float:
    """|a − b| relativo a la escala de los términos de la identidad (absoluto si todos son 0)."""
    return abs(a - b) / escala if escala > 0 else abs(a - b)


def _no_finitos(x: Any, ruta: str = "resultado") -> list[str]:
    if isinstance(x, dict):
        return [r for k, val in x.items() for r in _no_finitos(val, f"{ruta}.{k}")]
    if isinstance(x, (list, tuple)):
        return [r for i, val in enumerate(x) for r in _no_finitos(val, f"{ruta}[{i}]")]
    if isinstance(x, (float, np.floating)) and not math.isfinite(float(x)):
        return [ruta]
    return []


def _cerrado(ficha: str) -> Callable[[Manejador], Manejador]:
    """Falla cerrado en profundidad (patrón de `fichas_mon_idx`): entradas mal formadas, aritmética fuera de dominio y
    resultados no finitos → ErrorFicha con el motivo; lo indefinido se entrega como ``None``."""
    def decorar(fn: Manejador) -> Manejador:
        @wraps(fn)
        def envoltura(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
            if not isinstance(ent, dict) or not isinstance(ent.get("valores"), dict):
                raise ErrorFicha(f"{ficha}: los datos en línea («valores») deben ser un dict")
            if params is not None and not isinstance(params, dict):
                raise ErrorFicha(f"{ficha}: los parámetros deben ser un dict")
            try:
                res, lim = fn(ent, params or {})
            except ErrorFicha:
                raise
            except (ArithmeticError, ValueError, TypeError, AttributeError, KeyError, IndexError, RuntimeError) as e:
                raise ErrorFicha(f"{ficha}: entrada mal formada o fuera de dominio ({type(e).__name__}: {e})") from e
            malos = _no_finitos(res)
            if malos:
                raise ErrorFicha(f"{ficha}: resultado no finito en {', '.join(malos[:3])} (entradas fuera de dominio)")
            return res, lim
        return envoltura
    return decorar


def _validar_parametros(F: str, p: dict[str, Any]) -> None:
    """Tipo y rango de cada parámetro de la petición (T-108, H-24)."""
    u = UMBRALES[F]
    if F == "REI-CAP-001":
        p["base_noi"] = _opcion(p["base_noi"], f"{F}: base_noi", u["bases_noi"])
        p["ventana"] = _entero(p["ventana"], f"{F}: ventana (años)", u["anios_historia_minimos"])
    elif F == "REI-FFO-001":
        p["capex_mantenimiento"] = _opcion(p["capex_mantenimiento"], f"{F}: capex_mantenimiento", u["capex_admitidos"])
        if p["capex_pct_rentas"] is not None:
            lo, hi = u["rango_capex_pct_rentas"]
            p["capex_pct_rentas"] = _rango(p["capex_pct_rentas"], f"{F}: capex_pct_rentas", lo, hi, abierto_hi=True)
    elif F == "REI-NAV-001":
        p["nav_variante"] = _opcion(p["nav_variante"], f"{F}: nav_variante", u["variantes_nav"])
        if p["cap_objetivo"] is not None:
            p["cap_objetivo"] = _rango(p["cap_objetivo"], f"{F}: cap_objetivo", 0, 1, True, True)
    elif F == "CMD-INV-001":
        p["anos_estacional"] = _entero(p["anos_estacional"], f"{F}: anos_estacional", *u["rango_anos_estacional"])
        excl = p["excluir_anos"]
        if not isinstance(excl, list):
            raise ErrorFicha(f"{F}: excluir_anos debe ser una lista de años")
        anios = [_entero(a, f"{F}: excluir_anos", 1) for a in excl]
        if len(set(anios)) != len(anios):
            raise ErrorFicha(f"{F}: excluir_anos con años repetidos")
        p["excluir_anos"] = sorted(anios)
    elif F == "CMD-RETDEC-001":
        p["calendario_roll"] = _opcion(p["calendario_roll"], f"{F}: calendario_roll", u["calendarios_admitidos"])
        p["frecuencia"] = _opcion(p["frecuencia"], f"{F}: frecuencia", u["frecuencias_admitidas"])
    elif F == "CHR-FLOW-001":
        vent = p["ventanas"]
        if not isinstance(vent, list) or not vent:
            raise ErrorFicha(f"{F}: ventanas debe ser una lista no vacía de días")
        vs = [_entero(w, f"{F}: ventanas (días)", 1) for w in vent]
        if len(set(vs)) != len(vs):
            raise ErrorFicha(f"{F}: ventanas repetidas")
        p["ventanas"] = sorted(vs)
        p["ventana_z"] = _entero(p["ventana_z"], f"{F}: ventana_z (años)", 1)
    elif F == "CHR-FUND-001":
        p["ponderacion"] = _opcion(p["ponderacion"], f"{F}: ponderacion", u["ponderaciones_admitidas"])
        p["ventana_percentil"] = _entero(p["ventana_percentil"], f"{F}: ventana_percentil (días)",
                                         u["dias_percentil_minimos"])
    elif F == "ALT-DESMOOTH-001":
        p["metodo"] = _opcion(p["metodo"], f"{F}: metodo", u["metodos_admitidos"])
        p["k"] = _entero(p["k"], f"{F}: k", *u["rango_k"])
        if p["phi"] is not None:
            if p["metodo"] != "Geltner":
                raise ErrorFicha(f"{F}: phi fijado solo se admite con el método Geltner")
            lo, hi = u["rango_phi"]
            p["phi"] = _rango(p["phi"], f"{F}: phi", lo, hi, abierto_hi=True)


def _parametros(ficha: str, params: dict[str, Any] | None) -> dict[str, Any]:
    """Parámetros de la petición encima de los de la ficha, validados; un umbral de `UMBRALES` en la petición se rechaza.

    Las claves que la ficha no declara se ignoran (la capa de servicio añade, por ejemplo, «clase»)."""
    if params is not None and not isinstance(params, dict):
        raise ErrorFicha(f"{ficha}: los parámetros deben ser un dict")
    params = params or {}
    fijos = set(params) & set(UMBRALES[ficha])
    if fijos:
        raise ErrorFicha(f"{ficha}: {sorted(fijos)} son umbrales fijos de la ficha, no parámetros de la petición")
    p = dict(PARAMETROS_POR_DEFECTO[ficha])
    p.update({k: v for k, v in params.items() if v is not None and k in p})
    if isinstance(p.get("excluir_anos"), list):
        p["excluir_anos"] = list(p["excluir_anos"])
    if isinstance(p.get("ventanas"), list):
        p["ventanas"] = list(p["ventanas"])
    _validar_parametros(ficha, p)
    return p


# ================================================================== REI-CAP-001
@_cerrado("REI-CAP-001")
def f_rei_cap(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """REI-CAP-001 · Cap rate y diferencial cap rate–bono (MC-09).

    ``valores``: ``moneda`` del subsector; ``noi`` = {"valor" > 0, "base": "adelantado" | "historico",
    "definicion": "antes_capex" | "despues_capex"}; ``valor_tasacion`` (> 0, misma moneda); opcional
    ``valor_mercado_implicito`` = {"capitalizacion" > 0, "deuda_neta"} del agregado cotizado (valor implícito =
    capitalización + deuda neta [PROPUESTO]); ``soberano_10a`` = {"rendimiento", "moneda"}; ``historia`` = lista de
    {"fecha", "cap_rate", "soberano_10a"} del subsector y país (≥ 15 años); opcional ``equilibrio`` = {"r", "g_noi"}.
    """
    F = "REI-CAP-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    lim: list[str] = []
    moneda = _texto(v.get("moneda"), f"{F}: «moneda» del subsector")
    noi_d = _dict(v.get("noi"), f"{F}: «noi»")
    if not isinstance(noi_d.get("base"), str) or " ".join(noi_d["base"].lower().split()) not in u["bases_noi"]:
        raise ErrorFicha(f"{F}: aclaración: la base del NOI es ambigua o no se declara (adelantado o historico)")
    base = _opcion(noi_d["base"], f"{F}: base del NOI", u["bases_noi"])
    if base != p["base_noi"]:
        raise ErrorFicha(f"{F}: aclaración: el NOI aportado es «{base}» y la petición pide la base «{p['base_noi']}»")
    if noi_d.get("definicion") is None:
        raise ErrorFicha(f"{F}: aclaración: definición del NOI (antes o después de CAPEX) sin declarar")
    definicion = _opcion(noi_d["definicion"], f"{F}: definición del NOI", u["definiciones_noi"])
    noi = _rango(noi_d.get("valor"), f"{F}: NOI", 0, abierto_lo=True)
    valor_tas = _rango(v.get("valor_tasacion"), f"{F}: valor_tasacion", 0, abierto_lo=True)
    cap_tas = noi / valor_tas                                            # cap rate = NOI/valor (tasación)
    cap_mer: float | None = None
    valor_mer: float | None = None
    if v.get("valor_mercado_implicito") is None:
        lim.append("sin valor de mercado implícito del agregado cotizado: cap rate de mercado no calculado")
    else:
        md = _dict(v["valor_mercado_implicito"], f"{F}: «valor_mercado_implicito»")
        capit = _rango(md.get("capitalizacion"), f"{F}: capitalizacion", 0, abierto_lo=True)
        deuda = _num(md.get("deuda_neta"), f"{F}: deuda_neta")
        valor_mer = capit + deuda
        if valor_mer <= 0:
            raise ErrorFicha(f"{F}: valor de mercado implícito (capitalización + deuda neta) no positivo")
        cap_mer = noi / valor_mer                                        # cap rate implícito del agregado cotizado
    sob = _dict(v.get("soberano_10a"), f"{F}: «soberano_10a»")
    y10 = _num(sob.get("rendimiento"), f"{F}: rendimiento del soberano a 10 años")
    if _texto(sob.get("moneda"), f"{F}: moneda del soberano") != moneda:
        raise ErrorFicha(f"{F}: el soberano a 10 años debe ser de la misma moneda que el subsector ({moneda})")
    hist = _tabla(v.get("historia"), {"cap_rate": (0, True), "soberano_10a": (None, False)}, f"{F}: historia")
    anios = _anios(hist.index)
    if anios < u["anios_historia_minimos"]:
        raise ErrorFicha(f"{F}: historia de {anios:.2f} años < {u['anios_historia_minimos']} años (entradas mínimas)")
    if anios < p["ventana"]:
        lim.append(f"historia de {anios:.2f} años, menor que la ventana de {p['ventana']}: percentil sobre la disponible")
    h = hist[hist.index > hist.index[-1] - pd.DateOffset(years=p["ventana"])]
    dif_hist = (h["cap_rate"].to_numpy() - h["soberano_10a"].to_numpy()) * PB
    dif = (cap_tas - y10) * PB
    pos = _posicion(dif, dif_hist)
    if pos["z"] is None:
        lim.append("historia del diferencial sin dispersión: z indefinido")
    cap_eq: float | None = None
    if v.get("equilibrio") is None:
        lim.append("sin r ni g_NOI: cap rate de equilibrio no calculado")
    else:
        eq = _dict(v["equilibrio"], f"{F}: «equilibrio»")
        r = _num(eq.get("r"), f"{F}: equilibrio.r")
        g = _num(eq.get("g_noi"), f"{F}: equilibrio.g_noi")
        if r <= g:
            raise ErrorFicha(f"{F}: cap de equilibrio r − g_NOI exige r > g_NOI")
        cap_eq = r - g                                                   # cap de equilibrio ≈ r − g_NOI
    res = {
        "moneda": moneda, "base_noi": base, "definicion_noi": definicion,
        "cap_rate_tasacion_pct": cap_tas * PCT,
        "cap_rate_mercado_pct": None if cap_mer is None else cap_mer * PCT,
        "prima_mercado_tasacion_pb": None if cap_mer is None else (cap_mer - cap_tas) * PB,
        "soberano_10a_pct": y10 * PCT,
        "diferencial_pb": dif,
        "diferencial_mercado_pb": None if cap_mer is None else (cap_mer - y10) * PB,
        "percentil": pos["percentil"], "z": pos["z"], "media_historica_pb": pos["media"], "n_historia": pos["n"],
        "ventana_anios": p["ventana"],
        "cap_equilibrio_pct": None if cap_eq is None else cap_eq * PCT,
        "brecha_equilibrio_pb": None if cap_eq is None else (cap_tas - cap_eq) * PB,
        "referencia_ingenua": {"tipo": "RI-MH", "diferencial_pb": pos["media"]},
        "verificacion": {  # «Verificación»: coherencia NOI/valor (cap × valor reproduce el NOI)
            "error_relativo_noi_tasacion": abs(cap_tas * valor_tas - noi) / noi,
            "error_relativo_noi_mercado": None if cap_mer is None or valor_mer is None
            else abs(cap_mer * valor_mer - noi) / noi},
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== REI-NAV-001
@_cerrado("REI-NAV-001")
def f_rei_nav(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """REI-NAV-001 · Prima/descuento sobre NAV (MC-09).

    ``valores``: ``componentes`` = lista de {"id", "fecha_precio", "precio" > 0, "acciones" > 0, "nav_por_accion" > 0,
    "fecha_nav", "variante_nav", "gav" > 0, "deuda_neta", "otros_pasivos" (opcional), "cap_rate_tasacion" en (0, 1)},
    todos a la misma fecha de precio; opcional ``historia_prima`` = lista de {"fecha", "prima"} del agregado.
    """
    F = "REI-NAV-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    tol = FICHAS[F]["tol"]
    lim: list[str] = []
    comps = _lista(v.get("componentes"), f"{F}: componentes")
    filas: list[dict[str, Any]] = []
    for i, c in enumerate(comps):
        ctx = f"{F}: componentes[{i}]"
        c = _dict(c, ctx)
        cid = _texto(c.get("id"), f"{ctx}.id")
        fp = _fecha(c.get("fecha_precio"), f"{ctx}.fecha_precio")
        fn_ = _fecha(c.get("fecha_nav"), f"{ctx}.fecha_nav")
        if fn_ > fp:
            raise ErrorFicha(f"{ctx}: NAV con fecha posterior a la del precio (no conocible)")
        if fn_ + pd.DateOffset(months=u["meses_antiguedad_nav_max"]) < fp:
            raise ErrorFicha(f"{ctx}: NAV de antigüedad > {u['meses_antiguedad_nav_max']} meses (rechazo de la ficha)")
        if c.get("variante_nav") is None:
            raise ErrorFicha(f"{ctx}: variante de NAV sin declarar")
        variante = _opcion(c["variante_nav"], f"{ctx}.variante_nav", u["variantes_nav"])
        if variante != p["nav_variante"]:
            raise ErrorFicha(f"{ctx}: NAV {variante} y la petición pide {p['nav_variante']} (no se mezclan variantes)")
        precio = _rango(c.get("precio"), f"{ctx}.precio", 0, abierto_lo=True)
        acciones = _rango(c.get("acciones"), f"{ctx}.acciones", 0, abierto_lo=True)
        nav_acc = _rango(c.get("nav_por_accion"), f"{ctx}.nav_por_accion", 0, abierto_lo=True)
        gav = _rango(c.get("gav"), f"{ctx}.gav", 0, abierto_lo=True)
        deuda = _num(c.get("deuda_neta"), f"{ctx}.deuda_neta")
        cap_tas = _rango(c.get("cap_rate_tasacion"), f"{ctx}.cap_rate_tasacion", 0, 1, True, True)
        nav = nav_acc * acciones
        if c.get("otros_pasivos") is None:
            otros = gav - deuda - nav
            err: float | None = None
            lim.append(f"{cid}: otros pasivos derivados por diferencia (GAV − deuda neta − NAV): identidad no verificable")
        else:
            otros = _num(c.get("otros_pasivos"), f"{ctx}.otros_pasivos")
            err = abs(gav - deuda - otros - nav) / nav                 # «Verificación»: NAV = activos − pasivos
            if err > tol:
                raise ErrorFicha(f"{ctx}: NAV ≠ GAV − deuda neta − otros pasivos (error relativo {err:.3g})")
        filas.append({"id": cid, "fecha": fp, "fecha_nav": fn_, "precio": precio, "acciones": acciones,
                      "nav_acc": nav_acc, "nav": nav, "gav": gav, "deuda": deuda, "otros": otros, "cap": cap_tas,
                      "capit": precio * acciones, "err": err})
    ids = [f["id"] for f in filas]
    if len(set(ids)) != len(ids):
        raise ErrorFicha(f"{F}: componentes con «id» repetido")
    if len({f["fecha"] for f in filas}) != 1:
        raise ErrorFicha(f"{F}: los componentes deben cotizar a la misma fecha de precio (agregado a una fecha)")
    filas.sort(key=lambda f: f["id"])
    capit_total = sum(f["capit"] for f in filas)
    w = np.array([f["capit"] / capit_total for f in filas])
    primas = np.array([f["precio"] / f["nav_acc"] - 1 for f in filas])  # P/NAV − 1
    prima_agg = float(np.sum(w * primas))                              # agregado ponderado por capitalización
    dispersion = math.sqrt(float(np.sum(w * (primas - prima_agg) ** 2)))
    cap_obj = p["cap_objetivo"]
    nav_ajustado: dict[str, Any] | None = None
    ajustados: dict[str, float | None] = {f["id"]: None for f in filas}
    if cap_obj is None:
        lim.append("sin cap_objetivo (implícito de REI-CAP-001): NAV ajustado no calculado")
    else:
        for f in filas:   # NAV ajustado = GAV × (cap_tasación/cap_objetivo) − deuda neta − otros pasivos
            ajustados[f["id"]] = f["gav"] * (f["cap"] / cap_obj) - f["deuda"] - f["otros"]
        nav_total = sum(f["nav"] for f in filas)
        adj_total = float(sum(x for x in ajustados.values() if x is not None))
        nav_ajustado = {"cap_objetivo": cap_obj, "nav_total": nav_total, "nav_ajustado_total": adj_total,
                        "variacion_pct": (adj_total / nav_total - 1) * PCT}
    pos: dict[str, Any] | None = None
    if v.get("historia_prima") is None:
        lim.append("sin historia de la prima agregada: percentil no calculado")
    else:
        hist = _tabla(v["historia_prima"], {"prima": (-1, True)}, f"{F}: historia_prima")
        if _anios(hist.index) < u["anios_percentil_minimos"]:
            lim.append(f"historia de la prima < {u['anios_percentil_minimos']} años: percentil no calculado")
        else:
            pos = _posicion(prima_agg, hist["prima"].to_numpy())
    errores = [f["err"] for f in filas if f["err"] is not None]
    res = {
        "fecha_precio": filas[0]["fecha"].date().isoformat(), "nav_variante": p["nav_variante"],
        "prima_agregada_pct": prima_agg * PCT, "dispersion_pct": dispersion * PCT,
        "rango_pct": [float(np.min(primas)) * PCT, float(np.max(primas)) * PCT],
        "componentes": {f["id"]: {"prima_pct": float(pr) * PCT, "peso": float(wi), "nav": f["nav"],
                                  "nav_ajustado": ajustados[f["id"]],
                                  "antiguedad_nav_dias": int((f["fecha"] - f["fecha_nav"]).days)}
                        for f, pr, wi in zip(filas, primas, w, strict=True)},
        "nav_ajustado": nav_ajustado,
        "percentil": None if pos is None else pos["percentil"], "z": None if pos is None else pos["z"],
        "media_historica_pct": None if pos is None else pos["media"] * PCT,
        "referencia_ingenua": {"tipo": "RI-MH", "prima_pct": None if pos is None else pos["media"] * PCT},
        "verificacion": {"error_relativo_nav_max": max(errores) if errores else None},
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== REI-FFO-001
@_cerrado("REI-FFO-001")
def f_rei_ffo(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """REI-FFO-001 · FFO/AFFO y sostenibilidad del dividendo del agregado de un subsector (MC-09).

    ``valores``: ``moneda``; ``componentes`` = lista de {"id", "precio" > 0, "acciones" > 0, "ejercicios": lista de
    {"ejercicio" (año), "beneficio_neto", "amortizaciones_inmobiliarias" ≥ 0, "plusvalias", "capex_mantenimiento" ≥ 0
    (si se reporta), "rentas" ≥ 0 (para estimar el CAPEX), "ajuste_rentas_lineales", "dividendo" ≥ 0}} (importes en
    moneda); opcional ``historia_multiplos`` = lista de {"fecha", "p_ffo", "p_affo"} del subsector.
    """
    F = "REI-FFO-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    lim: list[str] = []
    moneda = _texto(v.get("moneda"), f"{F}: «moneda»")
    comps = _lista(v.get("componentes"), f"{F}: componentes")
    por_comp: dict[str, dict[int, dict[str, float]]] = {}
    capit: dict[str, float] = {}
    errores_bn: list[float] = []
    errores_affo: list[float] = []
    estimado = False
    for i, c in enumerate(comps):
        ctx = f"{F}: componentes[{i}]"
        c = _dict(c, ctx)
        cid = _texto(c.get("id"), f"{ctx}.id")
        if cid in por_comp:
            raise ErrorFicha(f"{F}: componentes con «id» repetido ({cid})")
        capit[cid] = (_rango(c.get("precio"), f"{ctx}.precio", 0, abierto_lo=True)
                      * _rango(c.get("acciones"), f"{ctx}.acciones", 0, abierto_lo=True))
        ejs = _lista(c.get("ejercicios"), f"{ctx}.ejercicios")
        tabla: dict[int, dict[str, float]] = {}
        for j, e in enumerate(ejs):
            cj = f"{ctx}.ejercicios[{j}]"
            e = _dict(e, cj)
            anio = _entero(e.get("ejercicio"), f"{cj}.ejercicio", 1)
            if anio in tabla:
                raise ErrorFicha(f"{cj}: ejercicio {anio} repetido")
            if e.get("amortizaciones_inmobiliarias") is None:
                raise ErrorFicha(f"{cj}: rechazo sin amortizaciones inmobiliarias desglosadas")
            bn = _num(e.get("beneficio_neto"), f"{cj}.beneficio_neto")
            am = _rango(e.get("amortizaciones_inmobiliarias"), f"{cj}.amortizaciones_inmobiliarias", 0)
            pl = _num(e.get("plusvalias"), f"{cj}.plusvalias")
            aj = _num(e.get("ajuste_rentas_lineales"), f"{cj}.ajuste_rentas_lineales")
            div = _rango(e.get("dividendo"), f"{cj}.dividendo", 0)
            if p["capex_mantenimiento"] == "reportado" and e.get("capex_mantenimiento") is not None:
                capex = _rango(e.get("capex_mantenimiento"), f"{cj}.capex_mantenimiento", 0)
            else:
                if p["capex_pct_rentas"] is None:
                    raise ErrorFicha(f"{cj}: CAPEX de mantenimiento sin reportar y sin capex_pct_rentas para estimarlo")
                capex = p["capex_pct_rentas"] * _rango(e.get("rentas"), f"{cj}.rentas", 0)
                estimado = True
            ffo = bn + am - pl                          # FFO = beneficio neto + amortizaciones inmobiliarias − plusvalías
            affo = ffo - capex - aj                     # AFFO = FFO − CAPEX de mantenimiento − ajustes de rentas lineales
            errores_bn.append(_error_rel(ffo - am + pl, bn, abs(bn) + am + abs(pl)))   # reconciliación con el BN
            errores_affo.append(_error_rel(affo + capex + aj, ffo, abs(ffo) + capex + abs(aj)))
            tabla[anio] = {"bn": bn, "ffo": ffo, "affo": affo, "div": div, "capex": capex}
        por_comp[cid] = tabla
    if estimado:
        lim.append(f"CAPEX de mantenimiento estimado como {p['capex_pct_rentas'] * PCT:g} % de las rentas en algún ejercicio")
    ids = sorted(por_comp)
    comunes = sorted(set.intersection(*(set(t) for t in por_comp.values())))
    if len(comunes) < u["ejercicios_minimos"]:
        raise ErrorFicha(f"{F}: {len(comunes)} ejercicios comunes < {u['ejercicios_minimos']} (entradas mínimas)")
    ultimo = comunes[-1]
    if any(max(t) > ultimo for t in por_comp.values()):
        lim.append(f"hay componentes con ejercicios posteriores a {ultimo}: el agregado usa el último ejercicio común")
    serie = {str(a): {"ffo": sum(por_comp[c][a]["ffo"] for c in ids), "affo": sum(por_comp[c][a]["affo"] for c in ids),
                      "dividendo": sum(por_comp[c][a]["div"] for c in ids),
                      "beneficio_neto": sum(por_comp[c][a]["bn"] for c in ids)} for a in comunes}
    act = serie[str(ultimo)]
    cap_total = sum(capit.values())
    p_ffo = cap_total / act["ffo"] if act["ffo"] > 0 else None
    p_affo = cap_total / act["affo"] if act["affo"] > 0 else None
    if p_ffo is None or p_affo is None:
        lim.append("FFO o AFFO agregado no positivo: múltiplo indefinido")
    coberturas: dict[str, float | None] = {}
    for c in ids:
        d = por_comp[c][ultimo]
        coberturas[c] = d["affo"] / d["div"] if d["div"] > 0 else None
        if d["div"] <= 0:
            lim.append(f"{c}: sin dividendo en {ultimo}: cobertura indefinida")
    cob = np.array([x for x in coberturas.values() if x is not None])
    resumen_cob: dict[str, Any] | None = None
    if cob.size:
        q25, q50, q75 = (float(x) for x in np.quantile(cob, [0.25, 0.5, 0.75]))   # cuantiles tipo 7 (ST-DESC-001)
        resumen_cob = {"mediana": q50, "iqr": q75 - q25, "minimo": float(np.min(cob)), "maximo": float(np.max(cob)),
                       "n": int(cob.size)}
    pos_ffo: dict[str, Any] | None = None
    pos_affo: dict[str, Any] | None = None
    if v.get("historia_multiplos") is None:
        lim.append("sin historia de múltiplos del subsector: percentiles no calculados")
    else:
        hist = _tabla(v["historia_multiplos"], {"p_ffo": (0, True), "p_affo": (0, True)}, f"{F}: historia_multiplos",
                      opcionales=("p_affo",))
        for col, actual, destino in (("p_ffo", p_ffo, "ffo"), ("p_affo", p_affo, "affo")):
            h = hist[col].dropna().to_numpy()
            if actual is None or h.size < u["observaciones_minimas_percentil"]:
                lim.append(f"percentil de {col} no calculado (múltiplo indefinido o < "
                           f"{u['observaciones_minimas_percentil']} observaciones)")
                continue
            if destino == "ffo":
                pos_ffo = _posicion(actual, h)
            else:
                pos_affo = _posicion(actual, h)
    res = {
        "moneda": moneda, "ejercicio": ultimo, "ejercicios": [str(a) for a in comunes],
        "ffo_agregado": act["ffo"], "affo_agregado": act["affo"], "capitalizacion_agregada": cap_total,
        "rendimiento_ffo_pct": act["ffo"] / cap_total * PCT, "rendimiento_affo_pct": act["affo"] / cap_total * PCT,
        "p_ffo": p_ffo, "p_affo": p_affo,
        "percentil_p_ffo": None if pos_ffo is None else pos_ffo["percentil"],
        "percentil_p_affo": None if pos_affo is None else pos_affo["percentil"],
        "cobertura_agregada": act["affo"] / act["dividendo"] if act["dividendo"] > 0 else None,
        "cobertura": resumen_cob, "cobertura_por_componente": coberturas,
        "serie": serie,
        "referencia_ingenua": {"tipo": "RI-MH", "p_ffo": None if pos_ffo is None else pos_ffo["media"],
                               "p_affo": None if pos_affo is None else pos_affo["media"]},
        "verificacion": {"error_reconciliacion_beneficio_max": max(errores_bn),
                         "error_reconciliacion_affo_max": max(errores_affo)},
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== CMD-INV-001
def _clave_periodo(fecha: pd.Timestamp, frecuencia: str) -> tuple[int, int]:
    if frecuencia == "mensual":
        return int(fecha.year), int(fecha.month)
    iso = fecha.isocalendar()
    return int(iso[0]), int(iso[1])


def _contiguas(a: pd.Timestamp, b: pd.Timestamp, frecuencia: str) -> bool:
    """b es el periodo inmediatamente posterior a a (mes siguiente o 7 días después)."""
    if frecuencia == "mensual":
        return (b.year * MESES_ANIO + b.month) - (a.year * MESES_ANIO + a.month) == 1
    return (b - a).days == DIAS_SEMANA


def _mismo_periodo(claves: dict[tuple[int, int], int], anio: int, per: int, frecuencia: str) -> int | None:
    """Índice de la observación del mismo periodo del año `anio` (la semana ISO 53 cae en la 52 si ese año no la tiene)."""
    if (anio, per) in claves:
        return claves[(anio, per)]
    if frecuencia == "semanal" and per > SEMANAS_ANIO:
        return claves.get((anio, SEMANAS_ANIO))
    return None


def _referencia_estacional(x: np.ndarray, fechas: pd.DatetimeIndex, claves: dict[tuple[int, int], int], i: int,
                           frecuencia: str, anos: int, excluir: list[int]) -> list[int]:
    """Índices de la misma época del año en los `anos` años anteriores a la observación i (sin los excluidos)."""
    anio, per = _clave_periodo(fechas[i], frecuencia)
    out = []
    for a in range(anio - anos, anio):
        if a in excluir:
            continue
        j = _mismo_periodo(claves, a, per, frecuencia)
        if j is not None and j < i:
            out.append(j)
    return out


@_cerrado("CMD-INV-001")
def f_cmd_inv(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """CMD-INV-001 · Inventarios frente a media estacional (MC-02).

    ``valores``: ``inventarios`` = {"frecuencia": "semanal" | "mensual", "unidad", "observaciones": lista de {"fecha"
    (periodo de referencia), "fecha_publicacion", "valor" ≥ 0}}; opcional ``demanda_diaria`` = {"valor" > 0, "fuente"}
    (mismas unidades por día); opcional ``pendiente_curva`` = lista de {"fecha", "pendiente"} (CMD-CURVE-001).
    """
    F = "CMD-INV-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    lim: list[str] = []
    inv = _dict(v.get("inventarios"), f"{F}: «inventarios»")
    frec = _opcion(inv.get("frecuencia"), f"{F}: frecuencia", u["frecuencias_admitidas"])
    unidad = _texto(inv.get("unidad"), f"{F}: unidad física del inventario")
    obs = _lista(inv.get("observaciones"), f"{F}: observaciones")
    for i, o in enumerate(obs):
        if not isinstance(o, dict) or o.get("fecha_publicacion") is None:
            raise ErrorFicha(f"{F}: observaciones[{i}] sin fecha de publicación")
        if _fecha(o["fecha_publicacion"], f"{F}: observaciones[{i}].fecha_publicacion") < \
                _fecha(o.get("fecha"), f"{F}: observaciones[{i}].fecha"):
            raise ErrorFicha(f"{F}: observaciones[{i}] publicada antes de su periodo de referencia")
    t = _tabla(obs, {"valor": (0, False)}, f"{F}: observaciones")
    x, fechas = t["valor"].to_numpy(), t.index
    claves: dict[tuple[int, int], int] = {}
    for i, f in enumerate(fechas):
        k = _clave_periodo(f, frec)
        if k in claves:
            raise ErrorFicha(f"{F}: dos observaciones del mismo periodo {k}")
        claves[k] = i
    anios = _anios(fechas)
    if anios < u["anios_rechazo"]:
        raise ErrorFicha(f"{F}: rechazo con {anios:.2f} años < {u['anios_rechazo']}")
    if anios < u["anios_entrada_minima"]:
        lim.append(f"serie de {anios:.2f} años, por debajo de la entrada mínima de {u['anios_entrada_minima']}")
    elif anios < u["anios_recomendados"]:
        lim.append(f"serie de {anios:.2f} años, por debajo de los {u['anios_recomendados']} recomendados")
    anos, excl = p["anos_estacional"], p["excluir_anos"]
    n = x.size
    i = n - 1
    if _clave_periodo(fechas[i], frec)[0] in excl:
        raise ErrorFicha(f"{F}: excluir_anos no puede contener el año de la observación actual")
    ref = _referencia_estacional(x, fechas, claves, i, frec, anos, excl)
    if len(ref) < u["anios_previos_minimos"]:
        raise ErrorFicha(f"{F}: {len(ref)} años previos con el mismo periodo < {u['anios_previos_minimos']}")
    if len(ref) < anos:
        lim.append(f"media estacional con {len(ref)} de los {anos} años pedidos")
    xr = x[ref]
    media = float(np.mean(xr))
    sd = float(np.std(xr, ddof=1)) if float(np.ptp(xr)) > 0 else 0.0
    desv = float(x[i]) - media
    if sd == 0:
        lim.append("misma época de los años previos sin dispersión: z indefinido")
    if media <= 0:
        lim.append("media estacional nula: desviación en % indefinida")
    # sorpresa: variación del periodo frente a la variación típica de la misma época
    sorpresa: dict[str, Any] | None = None
    if i >= 1 and _contiguas(fechas[i - 1], fechas[i], frec):
        dv = [float(x[j] - x[j - 1]) for j in ref if j >= 1 and _contiguas(fechas[j - 1], fechas[j], frec)]
        if len(dv) >= u["anios_previos_minimos"]:
            d_act = float(x[i] - x[i - 1])
            tipica = float(np.mean(dv))
            sd_d = float(np.std(dv, ddof=1)) if float(np.ptp(dv)) > 0 else 0.0
            sorpresa = {"variacion": d_act, "variacion_estacional_tipica": tipica, "sorpresa": d_act - tipica,
                        "z": (d_act - tipica) / sd_d if sd_d > 0 else None, "n": len(dv)}
    if sorpresa is None:
        lim.append("sin el periodo anterior (o sin sus variaciones en ≥ 3 años previos): sorpresa no calculada")
    demanda: float | None = None
    if v.get("demanda_diaria") is None:
        lim.append("sin demanda diaria: días de cobertura no calculados")
    else:
        dd = _dict(v["demanda_diaria"], f"{F}: «demanda_diaria»")
        _texto(dd.get("fuente"), f"{F}: fuente de la demanda diaria")
        demanda = _rango(dd.get("valor"), f"{F}: demanda diaria", 0, abierto_lo=True)
    # serie de desviaciones (para la relación con la curva): cada punto con ≥ 3 años previos del mismo periodo
    serie: list[dict[str, Any]] = []
    for j in range(n):
        rj = _referencia_estacional(x, fechas, claves, j, frec, anos, excl)
        if len(rj) >= u["anios_previos_minimos"] and _clave_periodo(fechas[j], frec)[0] not in excl:
            mj = float(np.mean(x[rj]))
            serie.append({"fecha": fechas[j].date().isoformat(), "desviacion": float(x[j]) - mj,
                          "desviacion_pct": (float(x[j]) / mj - 1) * PCT if mj > 0 else None})
    relacion: dict[str, Any] | None = None
    if v.get("pendiente_curva") is None:
        lim.append("sin la pendiente de la curva (CMD-CURVE-001): relación no calculada")
    else:
        pc = _tabla(v["pendiente_curva"], {"pendiente": (None, False)}, f"{F}: pendiente_curva")
        pares = [(s["desviacion_pct"], float(pc.loc[pd.Timestamp(s["fecha"]), "pendiente"])) for s in serie
                 if s["desviacion_pct"] is not None and pd.Timestamp(s["fecha"]) in pc.index]
        a = np.array([q[0] for q in pares])
        b = np.array([q[1] for q in pares])
        if len(pares) < u["observaciones_minimas_correlacion"] or float(np.ptp(a)) == 0 or float(np.ptp(b)) == 0:
            lim.append("relación con la pendiente de la curva no calculable (pocas fechas comunes o sin dispersión)")
        else:
            relacion = {"correlacion": float(np.corrcoef(a, b)[0, 1]), "n": len(pares)}
    segunda = _segunda_via_stl(x, fechas, frec, ref, i, lim)
    res = {
        "frecuencia": frec, "unidad": unidad, "fecha": fechas[i].date().isoformat(), "inventario": float(x[i]),
        "media_estacional": media, "desviacion_estacional": sd, "anios_referencia": len(ref),
        "desviacion": desv, "desviacion_pct": (float(x[i]) / media - 1) * PCT if media > 0 else None,
        "z": desv / sd if sd > 0 else None,
        "sorpresa": sorpresa,
        "dias_cobertura": None if demanda is None else float(x[i]) / demanda,
        "dias_cobertura_media_estacional": None if demanda is None else media / demanda,
        "relacion_pendiente_curva": relacion,
        "serie_desviacion": serie,
        "referencia_ingenua": {"tipo": "RI-EST", "media_estacional": media},
        "segunda_via": segunda,
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


def _segunda_via_stl(x: np.ndarray, fechas: pd.DatetimeIndex, frec: str, ref: list[int], i: int,
                     lim: list[str]) -> dict[str, Any] | None:
    """Segunda vía (FX-STL-001, medias móviles, esquema aditivo): tendencia con media móvil centrada 2×P, índice
    estacional del periodo con la serie sin tendencia de los mismos años previos (normalizado a suma 0) y nivel
    esperado = última tendencia disponible + índice estacional. En una serie periódica pura coincide con la media
    estacional (desviación 0). Exige una serie regular (sin huecos)."""
    P = MESES_ANIO if frec == "mensual" else SEMANAS_ANIO
    regular = all(_contiguas(fechas[j - 1], fechas[j], frec) for j in range(1, x.size))
    if not regular or x.size < P + 1:
        lim.append("segunda vía FX-STL-001 no calculada (serie con huecos o más corta que un ciclo)")
        return None
    pesos = np.r_[0.5, np.ones(P - 1), 0.5] / P            # media móvil centrada 2×P (P par)
    tendencia = np.full(x.size, np.nan)
    tendencia[P // 2: x.size - P // 2] = np.convolve(x, pesos, mode="valid")
    def periodo(j: int) -> int:
        per = _clave_periodo(fechas[j], frec)[1]
        return min(per, SEMANAS_ANIO) if frec == "semanal" else per
    anios_ref = {int(_clave_periodo(fechas[j], frec)[0]) for j in ref}
    indices: dict[int, list[float]] = {}
    for j in range(x.size):
        if j < i and int(_clave_periodo(fechas[j], frec)[0]) in anios_ref and not math.isnan(tendencia[j]):
            indices.setdefault(periodo(j), []).append(float(x[j] - tendencia[j]))
    if len(indices) != P:
        lim.append("segunda vía FX-STL-001 no calculada (no todos los periodos del ciclo tienen índice estacional)")
        return None
    s = {k: float(np.mean(val)) for k, val in indices.items()}
    centro = float(np.mean(list(s.values())))
    validos = np.flatnonzero(~np.isnan(tendencia))
    nivel = float(tendencia[validos[-1]])
    esperado = nivel + s[periodo(i)] - centro
    return {"metodo": "FX-STL-001 (medias móviles 2×P, aditivo)", "nivel_tendencia": nivel,
            "indice_estacional": s[periodo(i)] - centro, "nivel_esperado": esperado,
            "desviacion": float(x[i]) - esperado}


# ================================================================== CMD-RETDEC-001
def _vector(x: Any, que: str, n: int | None = None, lo: float | None = None, abierto: bool = False) -> np.ndarray:
    lista = _lista(x, que)
    out = np.array([_rango(e, f"{que}[{i}]", lo, abierto_lo=abierto) for i, e in enumerate(lista)], dtype=float)
    if n is not None and out.size != n:
        raise ErrorFicha(f"{que}: {out.size} elementos y se esperaban {n} (alineados con «fechas»)")
    return out


def _fechas_regulares(x: Any, que: str, frecuencia: str) -> pd.DatetimeIndex:
    lista = _lista(x, que)
    f = pd.DatetimeIndex([_fecha(e, f"{que}[{i}]") for i, e in enumerate(lista)])
    if f.size < 2:
        raise ErrorFicha(f"{que}: se necesitan al menos dos fechas (un periodo)")
    per = f.to_period(FREQ_PANDAS[frecuencia])
    pasos = np.diff(per.asi8)
    if not bool(np.all(pasos == 1)):
        raise ErrorFicha(f"{que}: las fechas no son periodos {frecuencia}es consecutivos (huecos, desorden o repetidas)")
    return f


@_cerrado("CMD-RETDEC-001")
def f_cmd_retdec(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """CMD-RETDEC-001 · Descomposición de la rentabilidad de futuros (MC-09).

    Con ``calendario_roll = "indice"``: ``valores["indices"]`` = {"calendario_roll" (texto: el calendario declarado del
    índice), "fechas", "exceso", "total", "spot"} (niveles alineados con ``fechas``). Con ``"declarado"``:
    ``valores["contratos"]`` = {"fechas", "precios": {contrato: [nivel o null por fecha]}, "calendario_roll": lista de
    {"desde", "contrato"}, "spot": [...]}. En ambos, ``valores["tipo_colateral"]`` = tipos anuales (tanto por uno)
    alineados con las fechas; opcional ``valores["indice_amplio"]`` (niveles, RI-CM).

    Componentes por periodo (aditivos): spot = ΔS/S; roll = rentabilidad del futuro (o del índice de exceso) − spot;
    colateral = total − exceso (modo índice) o tipo·días/365 (modo contratos). Anualización aritmética: media por
    periodo × periodos por año [PROPUESTO], para que la suma de componentes sea el total exactamente.
    """
    F = "CMD-RETDEC-001"
    p, v = _parametros(F, params), ent["valores"]
    lim: list[str] = []
    frec, modo = p["frecuencia"], p["calendario_roll"]
    if modo == "indice":
        bloque = v.get("indices")
        if not isinstance(bloque, dict):
            raise ErrorFicha(f"{F}: calendario del índice: faltan los índices de exceso y total («indices»)")
        if not isinstance(bloque.get("calendario_roll"), str) or not bloque["calendario_roll"].strip():
            raise ErrorFicha(f"{F}: rechazo sin calendario de roll (el índice debe declarar el suyo)")
        calendario: Any = bloque["calendario_roll"].strip()
        fechas = _fechas_regulares(bloque.get("fechas"), f"{F}: indices.fechas", frec)
        n = fechas.size
        er = _vector(bloque.get("exceso"), f"{F}: indices.exceso", n, 0, True)
        tr = _vector(bloque.get("total"), f"{F}: indices.total", n, 0, True)
        spot = _vector(bloque.get("spot"), f"{F}: indices.spot", n, 0, True)
        r_s = spot[1:] / spot[:-1] - 1
        r_f = er[1:] / er[:-1] - 1
        r_tot = tr[1:] / tr[:-1] - 1
        col = r_tot - r_f
    else:
        bloque = v.get("contratos")
        if not isinstance(bloque, dict):
            raise ErrorFicha(f"{F}: calendario declarado: faltan los precios de contratos («contratos»)")
        cal = bloque.get("calendario_roll")
        if not isinstance(cal, list) or not cal:
            raise ErrorFicha(f"{F}: rechazo sin calendario de roll")
        fechas = _fechas_regulares(bloque.get("fechas"), f"{F}: contratos.fechas", frec)
        n = fechas.size
        precios = _dict(bloque.get("precios"), f"{F}: contratos.precios")
        tabla_p: dict[str, list[float | None]] = {}
        for cid, serie in precios.items():
            s = _lista(serie, f"{F}: precios[{cid}]")
            if len(s) != n:
                raise ErrorFicha(f"{F}: precios[{cid}] no alineado con «fechas»")
            tabla_p[str(cid)] = [None if e is None else _rango(e, f"{F}: precios[{cid}]", 0, abierto_lo=True) for e in s]
        tramos = []
        for i, e in enumerate(cal):
            e = _dict(e, f"{F}: calendario_roll[{i}]")
            c = _texto(e.get("contrato"), f"{F}: calendario_roll[{i}].contrato")
            if c not in tabla_p:
                raise ErrorFicha(f"{F}: calendario_roll[{i}]: contrato {c} sin precios")
            tramos.append((_fecha(e.get("desde"), f"{F}: calendario_roll[{i}].desde"), c))
        tramos.sort()
        if len({t_[0] for t_ in tramos}) != len(tramos):
            raise ErrorFicha(f"{F}: calendario_roll con fechas repetidas")
        if tramos[0][0] > fechas[0]:
            raise ErrorFicha(f"{F}: el calendario de roll no cubre la primera fecha")
        spot = _vector(bloque.get("spot"), f"{F}: contratos.spot", n, 0, True)
        r_s = spot[1:] / spot[:-1] - 1
        r_f = np.empty(n - 1)
        calendario = [{"desde": d.date().isoformat(), "contrato": c} for d, c in tramos]
        for i in range(1, n):
            vigente = [c for d, c in tramos if d <= fechas[i - 1]][-1]   # contrato mantenido en (t−1, t]
            a, b = tabla_p[vigente][i - 1], tabla_p[vigente][i]
            if a is None or b is None:
                raise ErrorFicha(f"{F}: falta el precio del contrato {vigente} en {fechas[i - 1].date()} o "
                                 f"{fechas[i].date()} (calendario de roll)")
            r_f[i - 1] = b / a - 1
        col = np.empty(n - 1)
    tipo = _vector(v.get("tipo_colateral"), f"{F}: tipo_colateral", fechas.size)
    dias = np.diff(fechas.values).astype("timedelta64[D]").astype(float)
    col_tipo = tipo[:-1] * dias / DIAS_ANIO                              # rendimiento del colateral, Real/365
    if modo == "declarado":
        col = col_tipo
        r_tot = r_f + col
    roll = r_f - r_s
    ppa = PERIODOS_ANIO[frec]
    comp = {"spot": r_s, "roll": roll, "colateral": col}
    anual = {k: float(np.mean(a)) * ppa * PCT for k, a in comp.items()}
    total = float(np.mean(r_tot)) * ppa * PCT
    anios = (fechas.size - 1) / ppa
    crec = float(np.prod(1 + r_tot))
    ref: dict[str, Any] = {"tipo": "RI-CM", "indice_amplio_pct_anual": None}
    if v.get("indice_amplio") is None:
        lim.append("sin índice amplio de materias primas: referencia RI-CM no calculada")
    else:
        amplio = _vector(v["indice_amplio"], f"{F}: indice_amplio", fechas.size, 0, True)
        ref["indice_amplio_pct_anual"] = float(np.mean(amplio[1:] / amplio[:-1] - 1)) * ppa * PCT
    res = {
        "frecuencia": frec, "calendario_roll": calendario, "periodos": int(fechas.size - 1), "anios": anios,
        "desde": fechas[0].date().isoformat(), "hasta": fechas[-1].date().isoformat(),
        "componentes_pct_anual": anual, "total_pct_anual": total,
        "total_compuesto_pct_anual": (crec ** (1 / anios) - 1) * PCT if crec > 0 else None,
        "acumulados": {k: float(np.sum(a)) for k, a in comp.items()} | {"total": float(np.sum(r_tot))},
        "colateral_implicito_menos_tipo_pb_anual": float(np.mean(col - col_tipo)) * ppa * PB,
        "referencia_ingenua": ref,
        "verificacion": {"identidad_pct_anual": sum(anual.values()) - total,   # «Verificación»: suma = total
                         "identidad_por_periodo_max": float(np.max(np.abs(r_s + roll + col - r_tot)))},
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== CHR-FUND-001
@_cerrado("CHR-FUND-001")
def f_chr_fund(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """CHR-FUND-001 · Financiación de perpetuos y base (MC-09).

    ``valores``: ``plataformas`` = {nombre: {"periodo_horas" > 0, "historia": lista diaria de {"fecha", "tasa" (por
    periodo, tanto por uno), "interes_abierto" > 0 (moneda)}}}; ``futuro`` = lista de {"fecha", "precio" > 0,
    "vencimiento"} (contrato genérico); ``spot`` = lista de {"fecha", "precio" > 0}; opcional ``capitalizacion`` =
    {"fecha", "valor" > 0}.
    """
    F = "CHR-FUND-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    lim: list[str] = []
    plat = _dict(v.get("plataformas"), f"{F}: «plataformas»")
    if len(plat) < u["plataformas_minimas"]:
        raise ErrorFicha(f"{F}: rechazo sin al menos {u['plataformas_minimas']} plataformas")
    anual: dict[str, pd.Series] = {}
    oi: dict[str, pd.Series] = {}
    for nombre in sorted(plat, key=str):
        d = _dict(plat[nombre], f"{F}: plataformas[{nombre}]")
        horas = _rango(d.get("periodo_horas"), f"{F}: plataformas[{nombre}].periodo_horas", 0, HORAS_DIA, abierto_lo=True)
        t = _tabla(d.get("historia"), {"tasa": (None, False), "interes_abierto": (0, True)},
                   f"{F}: plataformas[{nombre}].historia")
        anual[str(nombre)] = t["tasa"] * (HORAS_DIA / horas) * DIAS_ANIO   # tasa × periodos por año
        oi[str(nombre)] = t["interes_abierto"]
    nombres = sorted(anual)
    comunes = anual[nombres[0]].index
    for k in nombres[1:]:
        comunes = comunes.intersection(anual[k].index)
    if comunes.size < 2 or (comunes[-1] - comunes[0]).days < u["dias_minimos"]:
        raise ErrorFicha(f"{F}: < {u['dias_minimos']} días de fechas comunes entre plataformas (entradas mínimas)")
    A = pd.DataFrame({k: anual[k].loc[comunes] for k in nombres})
    W = pd.DataFrame({k: oi[k].loc[comunes] for k in nombres})
    if p["ponderacion"] == "igual":
        W = pd.DataFrame(1.0, index=comunes, columns=nombres)
    fin = (A * W).sum(axis=1) / W.sum(axis=1)                          # financiación agregada ponderada
    fut = _lista(v.get("futuro"), f"{F}: «futuro»")
    for i, e in enumerate(fut):
        if not isinstance(e, dict):
            raise ErrorFicha(f"{F}: futuro[{i}] mal formado")
    tf = _tabla(fut, {"precio": (0, True)}, f"{F}: futuro")
    venc = pd.Series([_fecha(e.get("vencimiento"), f"{F}: futuro[{i}].vencimiento") for i, e in enumerate(fut)],
                     index=pd.DatetimeIndex([_fecha(e.get("fecha"), f"{F}: futuro[{i}].fecha") for i, e in enumerate(fut)]))
    venc = venc.sort_index()
    ts = _tabla(v.get("spot"), {"precio": (0, True)}, f"{F}: spot")
    fb = tf.index.intersection(ts.index)
    if fb.empty or fb[-1] != comunes[-1]:
        raise ErrorFicha(f"{F}: el futuro y el spot deben cotizar en la última fecha común de financiación")
    dias = np.array([(venc.loc[f] - f).days for f in fb], dtype=float)
    if np.any(dias <= 0):
        raise ErrorFicha(f"{F}: futuro con vencimiento no posterior a su fecha")
    base = pd.Series((tf.loc[fb, "precio"].to_numpy() / ts.loc[fb, "precio"].to_numpy() - 1) * DIAS_ANIO / dias,
                     index=fb)                                         # base anualizada = (F/S − 1) × 365/días
    T = comunes[-1]

    def percentil(serie: pd.Series) -> float | None:
        if (serie.index[-1] - serie.index[0]).days < u["dias_percentil_minimos"]:
            return None
        h = serie[serie.index > serie.index[-1] - pd.Timedelta(days=p["ventana_percentil"])]
        return float(np.mean(h.to_numpy() <= float(serie.iloc[-1])))
    pf, pb_ = percentil(fin), percentil(base)
    if pf is None or pb_ is None:
        lim.append(f"historia < {u['dias_percentil_minimos']} días: percentiles no calculados")
    oi_total = float(W.loc[T].sum()) if p["ponderacion"] == "interes_abierto" else float(
        sum(float(oi[k].loc[T]) for k in nombres))
    ratio: float | None = None
    if v.get("capitalizacion") is None:
        lim.append("sin capitalización: interés abierto/capitalización no calculado")
    else:
        cd = _dict(v["capitalizacion"], f"{F}: «capitalizacion»")
        fc = _fecha(cd.get("fecha"), f"{F}: capitalizacion.fecha")
        if fc != T:
            raise ErrorFicha(f"{F}: la capitalización debe ser de la última fecha común ({T.date()})")
        ratio = oi_total / _rango(cd.get("valor"), f"{F}: capitalizacion.valor", 0, abierto_lo=True) * PCT
    # «Verificación»: coherencia base–financiación (arbitraje aproximado: la base anualizada ≈ financiación anualizada)
    fc_ = fin.index.intersection(base.index)
    dif = (base.loc[fc_] - fin.loc[fc_]).to_numpy()
    a_, b_ = base.loc[fc_].to_numpy(), fin.loc[fc_].to_numpy()
    corr = (float(np.corrcoef(a_, b_)[0, 1]) if fc_.size >= u["observaciones_minimas_correlacion"]
            and float(np.ptp(a_)) > 0 and float(np.ptp(b_)) > 0 else None)
    if corr is None:
        lim.append("correlación base–financiación no calculable (pocas fechas comunes o sin dispersión)")
    res = {
        "fecha": T.date().isoformat(), "ponderacion": p["ponderacion"], "plataformas": nombres,
        "financiacion_pct_anual": float(fin.loc[T]) * PCT,
        "financiacion_por_plataforma_pct_anual": {k: float(A.loc[T, k]) * PCT for k in nombres},
        "pesos": {k: float(W.loc[T, k] / W.loc[T].sum()) for k in nombres},
        "base_pct_anual": float(base.loc[T]) * PCT, "dias_vencimiento": int(dias[-1]),
        "percentil_financiacion": pf, "percentil_base": pb_, "ventana_percentil_dias": p["ventana_percentil"],
        "interes_abierto_total": oi_total, "interes_abierto_capitalizacion_pct": ratio,
        "referencia_ingenua": {"tipo": "RI-PA", "financiacion_pct_anual": float(fin.loc[T]) * PCT},
        "verificacion": {"base_menos_financiacion_pb": float(dif[-1]) * PB,
                         "base_menos_financiacion_media_pb": float(np.mean(dif)) * PB,
                         "correlacion": corr, "n": int(fc_.size)},
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== CHR-FLOW-001
@_cerrado("CHR-FLOW-001")
def f_chr_flow(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """CHR-FLOW-001 · Flujos de ETF y oferta de stablecoins (MC-02).

    ``valores``: ``flujos_etf`` = lista diaria (sesiones con flujo publicado) de {"fecha", "fecha_publicacion", "flujo"
    (moneda), "patrimonio" > 0 (al cierre de la sesión)} del agregado de ETF spot; ``oferta_stablecoins`` = {moneda
    estable principal: lista de {"fecha", "oferta" > 0}} (se suman en las fechas comunes); opcional
    ``capitalizacion_total`` = lista de {"fecha", "valor" > 0}.

    Ventanas en sesiones con flujo publicado [PROPUESTO]; % de patrimonio sobre el patrimonio previo a la ventana
    (flujo relativo = flujo/AUM_{t−1}, FON-FLOW-001 (ii)); z del acumulado relativo frente a los acumulados del último
    año (ventana_z) [PROPUESTO].
    """
    F = "CHR-FLOW-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    lim: list[str] = []
    filas = _lista(v.get("flujos_etf"), f"{F}: flujos_etf")
    for i, f in enumerate(filas):
        if not isinstance(f, dict) or f.get("fecha_publicacion") is None:
            raise ErrorFicha(f"{F}: rechazo sin fecha de publicación de flujos (flujos_etf[{i}])")
        if _fecha(f["fecha_publicacion"], f"{F}: flujos_etf[{i}].fecha_publicacion") < \
                _fecha(f.get("fecha"), f"{F}: flujos_etf[{i}].fecha"):
            raise ErrorFicha(f"{F}: flujos_etf[{i}] publicado antes de su fecha")
    t = _tabla(filas, {"flujo": (None, False), "patrimonio": (0, True)}, f"{F}: flujos_etf")
    if _anios(t.index) * DIAS_ANIO < u["dias_minimos"]:
        raise ErrorFicha(f"{F}: flujos de ETF con < {u['dias_minimos']} días (entradas mínimas)")
    ofertas = _dict(v.get("oferta_stablecoins"), f"{F}: «oferta_stablecoins»")
    so: pd.Series | None = None
    for nombre in sorted(ofertas, key=str):
        s = _tabla(ofertas[nombre], {"oferta": (0, True)}, f"{F}: oferta_stablecoins[{nombre}]")["oferta"]
        so = s if so is None else so.loc[so.index.intersection(s.index)] + s.loc[so.index.intersection(s.index)]
    if so is None or so.size < 2 or _anios(so.index) * DIAS_ANIO < u["dias_minimos"]:
        raise ErrorFicha(f"{F}: oferta de stablecoins con < {u['dias_minimos']} días comunes (entradas mínimas)")
    fl, pat = t["flujo"].to_numpy(), t["patrimonio"].to_numpy()
    n = fl.size
    acum = np.concatenate([[0.0], np.cumsum(fl)])                       # C_t: acumulado desde el inicio
    corte_z = t.index[-1] - pd.DateOffset(years=p["ventana_z"])
    if t.index[0] > corte_z:
        lim.append(f"historia de flujos < {p['ventana_z']} año(s): z sobre la historia disponible")
    ventanas: dict[str, Any] = {}
    errores = []
    for w in p["ventanas"]:
        if w >= n:
            raise ErrorFicha(f"{F}: ventana de {w} sesiones sin patrimonio previo (hay {n} sesiones)")
        mon = float(np.sum(fl[n - w:]))                                 # flujo neto acumulado a w sesiones
        errores.append(_error_rel(mon, float(acum[n] - acum[n - w]), float(np.sum(np.abs(fl[n - w:])))))
        rel = mon / float(pat[n - w - 1])                               # % del patrimonio previo a la ventana
        rel_hist = np.array([float(np.sum(fl[j - w + 1: j + 1])) / float(pat[j - w]) for j in range(w, n)])
        fechas_fin = t.index[w:]
        h = rel_hist[np.asarray(fechas_fin > corte_z)]
        pos = _posicion(rel, h) if h.size >= 2 else None
        ventanas[str(w)] = {"moneda": mon, "pct_patrimonio": rel * PCT, "z": None if pos is None else pos["z"],
                            "n_z": 0 if pos is None else pos["n"]}
        if pos is None or pos["z"] is None:
            lim.append(f"ventana {w}: z indefinido (menos de 2 acumulados en ventana_z o sin dispersión)")
    T = so.index[-1]
    previos = so[so.index <= T - pd.Timedelta(days=u["dias_crecimiento_stablecoins"])]
    if previos.empty:
        raise ErrorFicha(f"{F}: sin oferta de stablecoins {u['dias_crecimiento_stablecoins']} días antes de {T.date()}")
    crecimiento = float(so.iloc[-1] / previos.iloc[-1] - 1)
    razon: float | None = None
    if v.get("capitalizacion_total") is None:
        lim.append("sin capitalización total: razón stablecoins/capitalización no calculada")
    else:
        ct = _tabla(v["capitalizacion_total"], {"valor": (0, True)}, f"{F}: capitalizacion_total")
        if T not in ct.index:
            lim.append(f"sin capitalización total en {T.date()}: razón no calculada")
        else:
            razon = float(so.iloc[-1] / ct.loc[T, "valor"]) * PCT
    res = {
        "fecha_flujos": t.index[-1].date().isoformat(), "fecha_publicacion_ultima": max(
            _fecha(f["fecha_publicacion"], "fecha_publicacion") for f in filas).date().isoformat(),
        "flujos": ventanas, "ventana_z_anios": p["ventana_z"],
        "fecha_stablecoins": T.date().isoformat(), "oferta_stablecoins": float(so.iloc[-1]),
        "crecimiento_stablecoins_pct": crecimiento * PCT,
        "fecha_base_crecimiento": previos.index[-1].date().isoformat(),
        "razon_stablecoins_capitalizacion_pct": razon,
        "referencia_ingenua": {"tipo": "flujo nulo y RI-PA", "flujo_nulo": 0.0, "paseo_aleatorio_flujo": float(fl[-1])},
        "verificacion": {"error_acumulados_max": max(errores)},          # acumulados coherentes con los diarios
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== ALT-DESMOOTH-001
def _rentabilidades(ent: dict[str, Any], clave: str, rol: str, que: str) -> pd.Series | None:
    """Rentabilidades trimestrales: ``valores[clave]`` (lista de {"fecha", "r"}) o niveles en ``series_rol[rol]``."""
    v = ent["valores"]
    if v.get(clave) is not None:
        return _tabla(v[clave], {"r": (-1, True)}, que)["r"]
    s = (ent.get("series_rol") or {}).get(rol)
    if s is None:
        return None
    if not isinstance(s, pd.Series) or s.size < 2:
        raise ErrorFicha(f"{que}: el rol {rol} debe ser una serie de niveles")
    niveles = pd.Series([_rango(x, f"{que} (nivel)", 0, abierto_lo=True) for x in s.to_numpy()],
                        index=pd.DatetimeIndex([_fecha(f, f"{que} (fecha)") for f in s.index])).sort_index()
    if niveles.index.has_duplicates:
        raise ErrorFicha(f"{que}: fechas repetidas")
    return (niveles / niveles.shift(1) - 1).iloc[1:]


def _mdd(r: np.ndarray) -> float:
    """MDD de la trayectoria de riqueza (1 + r) (RISK-DD-001), en tanto por uno ∈ [0, 1]."""
    riqueza = np.concatenate([[1.0], np.cumprod(1 + r)])
    return float(np.max(1 - riqueza / np.maximum.accumulate(riqueza)))


def _ar1(x: np.ndarray) -> float:
    """φ del AR(1) por mínimos cuadrados con constante: x_t = c + φ·x_{t−1} + e_t."""
    a, b = x[1:], x[:-1]
    db = b - b.mean()
    return float(np.sum((a - a.mean()) * db) / np.sum(db * db))


def _glm_nll(theta: np.ndarray, x: np.ndarray) -> float:
    """−log verosimilitud exacta (gaussiana, σ concentrada) del MA(k) de GLM: x_t − μ = Σ θ_j η_{t−j}."""
    n, k = x.size, theta.size - 1
    gam = np.zeros(n)
    for j in range(k + 1):
        gam[j] = float(np.sum(theta[: k + 1 - j] * theta[j:]))
    try:
        c, low = linalg.cho_factor(linalg.toeplitz(gam), lower=True)
    except (linalg.LinAlgError, ValueError):
        return float(np.finfo(float).max)
    s2 = float(x @ linalg.cho_solve((c, low), x)) / n
    if not s2 > 0:
        return float(np.finfo(float).max)
    return 0.5 * n * math.log(s2) + float(np.sum(np.log(np.diag(c))))


def _glm_theta(r: np.ndarray, k: int, tol: float) -> np.ndarray:
    """θ de Getmansky-Lo-Makarov por máxima verosimilitud con θ_j ≥ 0 y Σθ = 1 (θ0 = 1 − Σ θ_{1..k} > 0)."""
    x = r - r.mean()
    def objetivo(t: np.ndarray) -> float:
        return _glm_nll(np.r_[1 - np.sum(t), t], x)
    inicio = np.full(k, 1 / (k + 1))                                     # θ iguales: arranque fijo, sin azar
    res = optimize.minimize(objetivo, inicio, method="SLSQP", bounds=[(0.0, 1.0)] * k,
                            constraints=[{"type": "ineq", "fun": lambda t: 1 - np.sum(t)}],
                            options={"ftol": tol})
    if not res.success:
        raise ErrorFicha(f"ALT-DESMOOTH-001: el estimador GLM no converge ({res.message})")
    t = np.clip(np.asarray(res.x, dtype=float), 0.0, 1.0)
    return _invertible(np.r_[1 - np.sum(t), t])


def _invertible(theta: np.ndarray) -> np.ndarray:
    """Representación invertible del MA (la que exige GLM): las raíces de θ0 + θ1·z + … + θk·z^k dentro del círculo
    unidad se reflejan (ρ → 1/ρ̄), lo que deja la misma autocovarianza salvo escala y, por tanto, la misma
    verosimilitud con σ concentrada; después se renormaliza a Σθ = 1."""
    k = theta.size - 1
    raices = np.roots(theta[::-1])
    if raices.size == 0 or np.all(np.abs(raices) > 1):
        return theta
    coef = np.array([1.0 + 0j])
    for rho in raices:
        rho = 1 / np.conj(rho) if abs(rho) < 1 else rho
        coef = np.convolve(coef, [1.0, -1 / rho])                       # ∏ (1 − z/ρ), valor 1 en z = 0
    c = np.zeros(k + 1)
    c[: coef.size] = np.real(coef)
    return c / np.sum(c)


def _dimson(r: pd.Series, m: pd.Series, rezagos: int) -> float | None:
    """Beta de Dimson: suma de las pendientes de r_t sobre m_t, m_{t−1}, …, m_{t−L}."""
    al = pd.concat([r.rename("r"), m.rename("m")], axis=1, join="inner").dropna()
    if al.shape[0] < rezagos + 3:
        return None
    X = np.column_stack([np.ones(al.shape[0] - rezagos)] +
                        [al["m"].to_numpy()[rezagos - j: al.shape[0] - j] for j in range(rezagos + 1)])
    y = al["r"].to_numpy()[rezagos:]
    if np.linalg.matrix_rank(X) < X.shape[1]:
        return None                                                     # rezagos colineales: beta no identificada
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(np.sum(coef[1:]))


@_cerrado("ALT-DESMOOTH-001")
def f_alt_desmooth(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """ALT-DESMOOTH-001 · Desuavizado de rentabilidades (MC-09).

    ``valores``: ``rentabilidades`` = lista de {"fecha", "r"} trimestrales consecutivas (tanto por uno; o niveles en
    ``series_rol["indice_suavizado"]``); opcional ``mercado`` (igual, o ``series_rol["mercado"]``) para la beta de
    Dimson con L = k rezagos [PROPUESTO].

    Geltner: r_t = (r*_t − φ·r*_{t−1})/(1 − φ), t = 2…n, con φ fijado o estimado por AR(1) (MCO con constante).
    GLM: θ por máxima verosimilitud exacta del MA(k) con Σθ = 1; r_t = (r*_t − Σ_{j≥1} θ_j·r_{t−j})/θ0, arrancando
    con r_t = r*_t en t ≤ k [PROPUESTO]. Volatilidad (% anual, √4) y MDD sobre las mismas fechas en las dos series.
    """
    F = "ALT-DESMOOTH-001"
    p, u = _parametros(F, params), UMBRALES[F]
    tol = FICHAS[F]["tol"]
    lim: list[str] = []
    obs = _rentabilidades(ent, "rentabilidades", "indice_suavizado", f"{F}: rentabilidades")
    if obs is None:
        raise ErrorFicha(f"{F}: faltan las rentabilidades observadas («rentabilidades» o rol indice_suavizado)")
    per = obs.index.to_period("Q")
    if obs.size >= 2 and not bool(np.all(np.diff(per.asi8) == 1)):
        raise ErrorFicha(f"{F}: rentabilidades no trimestrales consecutivas (huecos, repetidas o desordenadas)")
    n = obs.size
    if n < u["observaciones_minimas"]:
        raise ErrorFicha(f"{F}: rechazo con {n} observaciones < {u['observaciones_minimas']}")
    if n < u["observaciones_entrada_minima"]:
        lim.append(f"{n} observaciones < {u['observaciones_entrada_minima']} (entrada mínima): estimación imprecisa")
    rs = obs.to_numpy()
    k = p["k"]
    parametros: dict[str, Any]
    if p["metodo"] == "Geltner":
        phi = p["phi"] if p["phi"] is not None else _ar1(rs)
        if not -1 < phi < 1:
            raise ErrorFicha(f"{F}: φ estimado = {phi:.4f} fuera de (−1, 1): serie no estacionaria")
        if phi < 0:
            lim.append(f"φ estimado negativo ({phi:.4f}): sin evidencia de suavizado")
        r = (rs[1:] - phi * rs[:-1]) / (1 - phi)                          # Geltner
        inicio = 1
        resuav = (1 - phi) * r + phi * rs[:-1]                           # r*_t = (1 − φ)·r_t + φ·r*_{t−1}
        borde = phi / (1 - phi) * (rs[-1] - rs[0]) / (n - 1)             # Σ r − Σ r* = φ/(1 − φ)·(r*_n − r*_1)
        parametros = {"phi": phi, "phi_fijado": p["phi"] is not None}
    else:
        theta = _glm_theta(rs, k, tol)
        if theta[0] <= 0 or np.any(theta < 0) or np.any(np.abs(np.roots(theta[::-1])) <= 1):
            raise ErrorFicha(f"{F}: θ = {np.round(theta, 6).tolist()} no invertible: el desuavizado GLM no es estable")
        rr = rs.copy()
        for t_ in range(k, n):
            rr[t_] = (rs[t_] - float(np.sum(theta[1:] * rr[t_ - k: t_][::-1]))) / theta[0]
        r = rr[k:]
        inicio = k
        resuav = np.array([float(np.sum(theta * rr[t_ - k: t_ + 1][::-1])) for t_ in range(k, n)])
        # Σ_{t>k} r_t − Σ_{t>k} r*_t = Σ_j θ_j·(Σ_{n−j<t≤n} r_t − Σ_{k−j<t≤k} r_t)
        borde = float(sum(theta[j] * (np.sum(rr[n - j:]) - np.sum(rr[k - j: k])) for j in range(1, k + 1))) / (n - k)
        parametros = {"theta": theta.tolist(), "indice_suavizado": float(np.sum(theta ** 2)), "k": k}
        lim.append(f"GLM: el filtro arranca con la serie observada en los {k} primeros trimestres")
    ro = rs[inicio:]
    fechas = obs.index[inicio:]
    anual = math.sqrt(TRIMESTRES_ANIO)
    beta: dict[str, Any] | None = None
    merc = _rentabilidades(ent, "mercado", "mercado", f"{F}: mercado")
    if merc is None:
        lim.append("sin rentabilidades de mercado: beta de Dimson no calculada")
    else:
        bo = _dimson(pd.Series(ro, index=fechas), merc, k)
        bd = _dimson(pd.Series(r, index=fechas), merc, k)
        if bo is None or bd is None:
            lim.append("beta de Dimson no calculada (pocas fechas comunes con el mercado o rezagos colineales)")
        else:
            beta = {"observada": bo, "desuavizada": bd, "rezagos": k}
    media_o, media_d = float(np.mean(ro)), float(np.mean(r))
    res = {
        "metodo": p["metodo"], **parametros, "n": n,
        "serie_desuavizada": [{"fecha": f.date().isoformat(), "r": float(x)} for f, x in zip(fechas, r, strict=True)],
        "volatilidad_observada_pct": float(np.std(ro, ddof=1)) * anual * PCT,
        "volatilidad_desuavizada_pct": float(np.std(r, ddof=1)) * anual * PCT,
        "mdd_observado_pct": _mdd(ro) * PCT, "mdd_desuavizado_pct": _mdd(r) * PCT,
        "beta_dimson": beta,
        "media_observada": media_o, "media_desuavizada": media_d,
        "referencia_ingenua": {"tipo": "serie observada sin ajuste"},
        "verificacion": {  # φ = 0 ⇒ serie sin cambios; media conservada salvo el término de borde (exacto)
            "error_resuavizado_max": float(np.max(np.abs(resuav - ro))),
            "termino_borde_media": borde, "error_identidad_media": abs(media_d - media_o - borde)},
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== registro de fichas
FICHAS: dict[str, dict[str, Any]] = {
    "REI-CAP-001": {"fn": f_rei_cap, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-MH",
                    "tol": 1e-10},
    "REI-FFO-001": {"fn": f_rei_ffo, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-MH",
                    "tol": 1e-10},
    "REI-NAV-001": {"fn": f_rei_nav, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-MH",
                    "tol": 1e-10},
    "CMD-INV-001": {"fn": f_cmd_inv, "modulo": "MC-02", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-EST",
                    "tol": 1e-10},
    "CMD-RETDEC-001": {"fn": f_cmd_retdec, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA", "ri": "RI-CM",
                       "tol": 1e-10},
    "CHR-FLOW-001": {"fn": f_chr_flow, "modulo": "MC-02", "version": "1.0", "cifra": "ESTADISTICA",
                     "ri": "flujo nulo y RI-PA", "tol": 1e-10},
    "CHR-FUND-001": {"fn": f_chr_fund, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-PA",
                     "tol": 1e-10},
    "ALT-DESMOOTH-001": {"fn": f_alt_desmooth, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA",
                         "ri": "serie observada sin ajuste", "tol": 1e-8},
}


# ================================================================== datos sintéticos de los casos de control
def _iso(d: pd.Timestamp) -> str:
    return d.date().isoformat()


# ---- REI-CAP-001
_REI_CAP_FECHAS = pd.date_range("2009-03-31", periods=16 * TRIMESTRES_ANIO + 1, freq="QE")
_REI_CAP_HIST: list[dict[str, Any]] = [{"fecha": _iso(d), "cap_rate": 0.05 + 0.01 * math.sin(0.7 * i),
                  "soberano_10a": 0.03 + 0.008 * math.cos(0.4 * i)} for i, d in enumerate(_REI_CAP_FECHAS)]


def _datos_rei_cap() -> dict[str, Any]:
    return {"moneda": "EUR", "noi": {"valor": 52.5e6, "base": "adelantado", "definicion": "despues_capex"},
            "valor_tasacion": 1.05e9, "valor_mercado_implicito": {"capitalizacion": 6.0e8, "deuda_neta": 6.5e8},
            "soberano_10a": {"rendimiento": 0.031, "moneda": "EUR"}, "historia": [dict(h) for h in _REI_CAP_HIST],
            "equilibrio": {"r": 0.072, "g_noi": 0.018}}


def _dif_rei_cap(ventana: int) -> np.ndarray:
    corte = _REI_CAP_FECHAS[-1] - pd.DateOffset(years=ventana)
    return np.array([(h["cap_rate"] - h["soberano_10a"]) * PB for h, d in zip(_REI_CAP_HIST, _REI_CAP_FECHAS, strict=True)
                     if d > corte])


def _caso_rei_cap_posicion(r: dict[str, Any]) -> bool:
    h, x, tol = _dif_rei_cap(15), (0.05 - 0.031) * PB, FICHAS["REI-CAP-001"]["tol"]
    return (_rel(r["diferencial_pb"], x, tol) and r["n_historia"] == h.size < len(_REI_CAP_HIST)
            and r["percentil"] == float(np.mean(h <= x)) and 0 < r["percentil"] < 1
            and _rel(r["z"], (x - h.mean()) / h.std(ddof=1), tol) and _rel(r["media_historica_pb"], h.mean(), tol)
            and _rel(r["diferencial_mercado_pb"], (52.5e6 / 1.25e9 - 0.031) * PB, tol))


# ---- REI-NAV-001
def _comp_nav(cid: str, precio: float, acciones: float, nav_acc: float, gav: float, deuda: float, otros: float,
              cap: float) -> dict[str, Any]:
    return {"id": cid, "fecha_precio": "2026-09-30", "precio": precio, "acciones": acciones, "nav_por_accion": nav_acc,
            "fecha_nav": "2026-06-30", "variante_nav": "EPRA NTA", "gav": gav, "deuda_neta": deuda,
            "otros_pasivos": otros, "cap_rate_tasacion": cap}


def _datos_rei_nav(misma_cap: bool) -> dict[str, Any]:
    return {"componentes": [_comp_nav("A", 18.0, 1e8, 20.0, 3.2e9, 1.0e9, 0.2e9, 0.05),
                            _comp_nav("B", 31.5, 5e7, 30.0, 2.4e9, 0.75e9, 0.15e9, 0.05 if misma_cap else 0.045)],
            "historia_prima": [{"fecha": _iso(d), "prima": -0.08 + 0.06 * math.sin(0.9 * i)}
                               for i, d in enumerate(pd.date_range("2014-12-31", periods=12 * 4 + 1, freq="QE"))]}


def _caso_rei_nav_metodo(r: dict[str, Any]) -> bool:
    tol = FICHAS["REI-NAV-001"]["tol"]
    w = np.array([18.0 * 1e8, 31.5 * 5e7]) / (18.0 * 1e8 + 31.5 * 5e7)
    pr = np.array([18 / 20 - 1, 31.5 / 30 - 1])
    agg = float(np.sum(w * pr))
    adj = (3.2e9 * 0.05 / 0.055 - 1.0e9 - 0.2e9) + (2.4e9 * 0.045 / 0.055 - 0.75e9 - 0.15e9)
    return (_rel(r["prima_agregada_pct"], agg * PCT, tol) and _rel(r["dispersion_pct"],
                                                                 math.sqrt(float(np.sum(w * (pr - agg) ** 2))) * PCT, tol)
            and _rel(r["nav_ajustado"]["variacion_pct"], (adj / 3.5e9 - 1) * PCT, tol)
            and _rel(r["componentes"]["A"]["nav_ajustado"], 3.2e9 * 0.05 / 0.055 - 1.0e9 - 0.2e9, tol))


def _caso_rei_nav_percentil(r: dict[str, Any]) -> bool:
    h = np.array([x["prima"] for x in _datos_rei_nav(False)["historia_prima"]])
    agg = r["prima_agregada_pct"] / PCT
    tol = FICHAS["REI-NAV-001"]["tol"]
    return (r["percentil"] == float(np.mean(h <= agg)) and 0 < r["percentil"] < 1
            and _rel(r["z"], (agg - h.mean()) / h.std(ddof=1), tol) and _rel(r["media_historica_pct"], h.mean() * PCT, tol))


# ---- REI-FFO-001
_FFO_EJ = {  # (beneficio neto, amortizaciones inmobiliarias, plusvalías, capex, ajuste rentas lineales, dividendo)
    "X": (25.0, 4e7, {2023: (40e6, 30e6, 10e6, 8e6, 2e6, 45e6), 2024: (42e6, 31e6, 5e6, 9e6, 1e6, 48e6),
                      2025: (38e6, 33e6, -4e6, 10e6, 3e6, 50e6)}),
    "Y": (12.0, 5e7, {2023: (20e6, 15e6, 2e6, 3.5e6, 1e6, 22e6), 2024: (21e6, 16e6, 3e6, 4e6, 1e6, 23e6),
                      2025: (22e6, 17e6, 1e6, 4.5e6, 0.5e6, 24e6)}),
    "Z": (8.0, 5e7, {2023: (10e6, 8e6, 0.0, 2e6, 0.0, 15e6), 2024: (11e6, 8e6, 1e6, 2e6, 0.0, 15e6),
                     2025: (9e6, 9e6, 0.0, 3e6, 1e6, 16e6)}),
}
_FFO_RENTAS_Y_2023 = 50e6
# la historia incluye un empate exacto con los múltiplos actuales (2e9/131e6 y 2e9/109e6): el percentil cuenta los ≤
_FFO_HIST = [(12.0, 15.0), (13.5, 16.0), (15.0, 18.0), (11.0, 13.0), (14.0, 17.0), (16.0, 19.0), (13.0, 15.5), (12.5, 14.8),
             (2e9 / 131e6, 2e9 / 109e6)]


def _datos_rei_ffo(capex_y_2023: bool = True) -> dict[str, Any]:
    comps = []
    for cid, (precio, acciones, ejs) in _FFO_EJ.items():
        filas = []
        for anio, (bn, am, pl, cx, aj, div) in ejs.items():
            fila: dict[str, Any] = {"ejercicio": anio, "beneficio_neto": bn, "amortizaciones_inmobiliarias": am, "plusvalias": pl,
                    "capex_mantenimiento": cx, "ajuste_rentas_lineales": aj, "dividendo": div}
            if cid == "Y" and anio == 2023:
                fila["rentas"] = _FFO_RENTAS_Y_2023
                if not capex_y_2023:
                    fila["capex_mantenimiento"] = None
            filas.append(fila)
        comps.append({"id": cid, "precio": precio, "acciones": acciones, "ejercicios": filas})
    return {"moneda": "EUR", "componentes": comps,
            "historia_multiplos": [{"fecha": f"{2017 + i}-12-31", "p_ffo": a, "p_affo": b} for i, (a, b) in enumerate(_FFO_HIST)]}


def _ffo_a_mano(anio: int, capex_y_2023: float | None = None) -> tuple[float, float, float]:
    ffo = affo = bn_total = 0.0
    for cid, (_, _, ejs) in _FFO_EJ.items():
        bn, am, pl, cx, aj, _ = ejs[anio]
        if cid == "Y" and anio == 2023 and capex_y_2023 is not None:
            cx = capex_y_2023
        ffo += bn + am - pl
        affo += bn + am - pl - cx - aj
        bn_total += bn
    return ffo, affo, bn_total


def _caso_rei_ffo_reconciliacion(r: dict[str, Any]) -> bool:
    tol = FICHAS["REI-FFO-001"]["tol"]
    v = r["verificacion"]
    return (v["error_reconciliacion_beneficio_max"] <= tol and v["error_reconciliacion_affo_max"] <= tol
            and all(_rel(r["serie"][str(a)]["ffo"], _ffo_a_mano(a)[0], tol)
                    and _rel(r["serie"][str(a)]["affo"], _ffo_a_mano(a)[1], tol)
                    and _rel(r["serie"][str(a)]["beneficio_neto"], _ffo_a_mano(a)[2], tol) for a in (2023, 2024, 2025)))


def _caso_rei_ffo_metodo(r: dict[str, Any]) -> bool:
    tol = FICHAS["REI-FFO-001"]["tol"]
    cap = sum(pr * ac for pr, ac, _ in _FFO_EJ.values())
    ffo, affo, _ = _ffo_a_mano(2025)
    cob = np.array([(bn + am - pl - cx - aj) / div for _, _, e in _FFO_EJ.values() for bn, am, pl, cx, aj, div
                    in [e[2025]]])
    q = np.quantile(cob, [0.25, 0.5, 0.75])
    hf, ha = np.array([a for a, _ in _FFO_HIST]), np.array([b for _, b in _FFO_HIST])
    return (_rel(r["p_ffo"], cap / ffo, tol) and _rel(r["p_affo"], cap / affo, tol)
            and _rel(r["rendimiento_ffo_pct"], ffo / cap * PCT, tol) and _rel(r["rendimiento_affo_pct"], affo / cap * PCT, tol)
            and _rel(r["cobertura"]["mediana"], float(q[1]), tol) and _rel(r["cobertura"]["iqr"], float(q[2] - q[0]), tol)
            and r["percentil_p_ffo"] == float(np.mean(hf <= cap / ffo))
            and r["percentil_p_affo"] == float(np.mean(ha <= cap / affo))
            and _rel(r["referencia_ingenua"]["p_ffo"], float(hf.mean()), tol))


def _caso_rei_ffo_capex(r: dict[str, Any]) -> bool:
    tol = FICHAS["REI-FFO-001"]["tol"]
    capex = 0.08 * _FFO_RENTAS_Y_2023
    return (_rel(r["serie"]["2023"]["affo"], _ffo_a_mano(2023, capex)[1], tol)
            and _rel(r["serie"]["2024"]["affo"], _ffo_a_mano(2024)[1], tol))


# ---- CMD-INV-001
_INV_FECHAS = pd.date_range("2017-01-31", periods=8 * MESES_ANIO, freq="ME")
_INV_DEMANDA = 9.5


def _x_inv(anio: int, mes: int, periodica: bool) -> float:
    base = 300 + 40 * math.sin(2 * math.pi * mes / MESES_ANIO) + 15 * math.cos(4 * math.pi * mes / MESES_ANIO)
    if periodica:
        return base
    k = (anio - 2017) * MESES_ANIO + mes                               # curvatura: la 2×12 deja un sesgo constante
    return base + 6.0 * (anio - 2017) + 0.02 * k * k + float((anio * 7 + mes * 3) % 17)


def _datos_cmd_inv(periodica: bool) -> dict[str, Any]:
    obs = [{"fecha": _iso(d), "fecha_publicacion": _iso(d + pd.Timedelta(days=10)),
            "valor": _x_inv(d.year, d.month, periodica)} for d in _INV_FECHAS]
    return {"inventarios": {"frecuencia": "mensual", "unidad": "kt", "observaciones": obs},
            "demanda_diaria": {"valor": _INV_DEMANDA, "fuente": "sintética"}}


def _caso_cmd_inv_periodica(r: dict[str, Any]) -> bool:
    tol = FICHAS["CMD-INV-001"]["tol"]
    x = _x_inv(2024, 12, True)
    return (abs(r["desviacion"]) <= tol * x and abs(r["desviacion_pct"]) <= tol * PCT and r["z"] is None
            and _rel(r["media_estacional"], x, tol) and abs(r["sorpresa"]["sorpresa"]) <= tol * x
            and len(r["serie_desviacion"]) == (8 - 3) * MESES_ANIO
            and all(abs(s["desviacion"]) <= tol * x for s in r["serie_desviacion"]))


def _caso_cmd_inv_stl(r: dict[str, Any]) -> bool:
    tol = FICHAS["CMD-INV-001"]["tol"]
    x = _x_inv(2024, 12, True)
    s = r["segunda_via"]
    media = float(np.mean([_x_inv(2024, m, True) for m in range(1, 13)]))
    return (s is not None and abs(s["desviacion"]) <= tol * x and _rel(s["nivel_esperado"], x, tol)
            and _rel(s["nivel_tendencia"], media, tol) and _rel(s["indice_estacional"], x - media, tol))


def _caso_cmd_inv_stl_tendencia(r: dict[str, Any]) -> bool:
    """Segunda vía a mano, término a término, en la serie con tendencia y ruido (índices sin normalizar de partida)."""
    tol = FICHAS["CMD-INV-001"]["tol"]
    x = [_x_inv(d.year, d.month, False) for d in _INV_FECHAS]
    n = len(x)
    tend = {j: (0.5 * x[j - 6] + sum(x[j - 5: j + 6]) + 0.5 * x[j + 6]) / MESES_ANIO for j in range(6, n - 6)}
    por_mes: dict[int, list[float]] = {}
    for j, d in enumerate(_INV_FECHAS):
        if 2019 <= d.year <= 2023 and j in tend:
            por_mes.setdefault(d.month, []).append(x[j] - tend[j])
    s = {m: sum(v) / len(v) for m, v in por_mes.items()}
    centro = sum(s.values()) / len(s)
    esperado = tend[n - 7] + s[12] - centro
    sv = r["segunda_via"]
    return (sv is not None and abs(centro) > tol and _rel(sv["nivel_tendencia"], tend[n - 7], tol)
            and _rel(sv["indice_estacional"], s[12] - centro, tol) and _rel(sv["nivel_esperado"], esperado, tol)
            and _rel(sv["desviacion"], x[-1] - esperado, tol * PB))


def _caso_cmd_inv_metodo(r: dict[str, Any]) -> bool:
    tol = FICHAS["CMD-INV-001"]["tol"]
    anios = [2019, 2020, 2022, 2023]                                    # 2019–2023 sin 2021 (excluido)
    ref = np.array([_x_inv(a, 12, False) for a in anios])
    x = _x_inv(2024, 12, False)
    dv = np.array([_x_inv(a, 12, False) - _x_inv(a, 11, False) for a in anios])
    d_act = x - _x_inv(2024, 11, False)
    return (r["anios_referencia"] == len(anios) and _rel(r["media_estacional"], float(ref.mean()), tol)
            and _rel(r["desviacion"], x - float(ref.mean()), tol)
            and _rel(r["desviacion_pct"], (x / float(ref.mean()) - 1) * PCT, tol)
            and _rel(r["z"], (x - float(ref.mean())) / float(ref.std(ddof=1)), tol)
            and _rel(r["dias_cobertura"], x / _INV_DEMANDA, tol)
            and _rel(r["sorpresa"]["sorpresa"], d_act - float(dv.mean()), tol))


# ---- CMD-RETDEC-001
_RD_N = 13
_RD_FECHAS = pd.date_range("2024-01-31", periods=_RD_N, freq="ME")
_RD_RS = np.array([0.005 + 0.01 * math.sin(i) for i in range(1, _RD_N)])
_RD_ROLL = np.array([-0.004 + 0.002 * math.cos(i) for i in range(1, _RD_N)])
_RD_TIPO = np.array([0.03 + 0.001 * i for i in range(_RD_N)])
_RD_DIAS = np.diff(_RD_FECHAS.values).astype("timedelta64[D]").astype(float)
_RD_COL = _RD_TIPO[:-1] * _RD_DIAS / DIAS_ANIO


def _niveles(r: np.ndarray, inicio: float) -> list[float]:
    return [float(x) for x in inicio * np.concatenate([[1.0], np.cumprod(1 + r)])]


def _datos_cmd_retdec_indice() -> dict[str, Any]:
    return {"indices": {"calendario_roll": "quinto a noveno día hábil (índice sintético)",
                        "fechas": [_iso(d) for d in _RD_FECHAS], "spot": _niveles(_RD_RS, 100.0),
                        "exceso": _niveles(_RD_RS + _RD_ROLL, 250.0),
                        "total": _niveles(_RD_RS + _RD_ROLL + _RD_COL * 1.1, 400.0)},
            "tipo_colateral": [float(x) for x in _RD_TIPO]}


def _caso_cmd_retdec_indice(r: dict[str, Any]) -> bool:
    tol = FICHAS["CMD-RETDEC-001"]["tol"]
    c = r["componentes_pct_anual"]
    k = MESES_ANIO * PCT
    total = float(np.mean(_RD_RS + _RD_ROLL + _RD_COL * 1.1)) * k
    return (abs(r["verificacion"]["identidad_pct_anual"]) <= tol * abs(total)
            and r["verificacion"]["identidad_por_periodo_max"] <= tol
            and _rel(c["spot"], float(np.mean(_RD_RS)) * k, tol) and _rel(c["roll"], float(np.mean(_RD_ROLL)) * k, tol)
            and _rel(c["colateral"], float(np.mean(_RD_COL * 1.1)) * k, tol) and _rel(r["total_pct_anual"], total, tol))


# contratos: F1 hasta el 2.º cierre, F2 desde el 2.º, F3 desde el 4.º (roll en el cierre indicado)
_RC_FECHAS = pd.date_range("2024-01-31", periods=7, freq="ME")
_RC_PRECIOS: dict[str, list[float | None]] = {
    "F1": [80.0, 81.2, 80.5, None, None, None, None],
    "F2": [None, 82.0, 82.9, 84.1, 83.0, None, None],
    "F3": [None, None, None, 85.5, 84.0, 86.2, 87.0],
}
_RC_CAL = [("2024-01-31", "F1"), ("2024-03-31", "F2"), ("2024-05-31", "F3")]
_RC_SPOT = [79.0, 79.8, 80.1, 81.5, 80.9, 82.4, 83.3]
_RC_TIPO = [0.031, 0.0315, 0.032, 0.0318, 0.033, 0.0325, 0.034]


def _datos_cmd_retdec_contratos() -> dict[str, Any]:
    return {"contratos": {"fechas": [_iso(d) for d in _RC_FECHAS], "precios": {k: list(v) for k, v in _RC_PRECIOS.items()},
                          "calendario_roll": [{"desde": d, "contrato": c} for d, c in _RC_CAL], "spot": list(_RC_SPOT)},
            "tipo_colateral": list(_RC_TIPO)}


def _caso_cmd_retdec_contratos(r: dict[str, Any]) -> bool:
    tol = FICHAS["CMD-RETDEC-001"]["tol"]
    mantenido = ["F1", "F1", "F2", "F2", "F3", "F3"]                    # contrato vigente al inicio de cada periodo
    rf, rs, col = [], [], []
    for i in range(1, len(_RC_FECHAS)):
        a, b = _RC_PRECIOS[mantenido[i - 1]][i - 1], _RC_PRECIOS[mantenido[i - 1]][i]
        assert a is not None and b is not None
        rf.append(b / a - 1)
        rs.append(_RC_SPOT[i] / _RC_SPOT[i - 1] - 1)
        col.append(_RC_TIPO[i - 1] * (_RC_FECHAS[i] - _RC_FECHAS[i - 1]).days / DIAS_ANIO)
    k = MESES_ANIO * PCT
    c = r["componentes_pct_anual"]
    total = float(np.mean(np.array(rf) + np.array(col))) * k
    return (abs(r["verificacion"]["identidad_pct_anual"]) <= tol * abs(total)
            and _rel(c["spot"], float(np.mean(rs)) * k, tol)
            and _rel(c["roll"], float(np.mean(np.array(rf) - np.array(rs))) * k, tol)
            and _rel(c["colateral"], float(np.mean(col)) * k, tol) and _rel(r["total_pct_anual"], total, tol))


# ---- CHR-FUND-001
_CF_FECHAS = pd.date_range("2025-01-01", periods=400, freq="D")
_CF_PLAT = {"P1": (8.0, lambda t: 1.0e-4 + 4e-5 * math.sin(0.11 * t), lambda t: 6e9 + 1e9 * math.cos(0.05 * t)),
            "P2": (8.0, lambda t: 0.6e-4 + 3e-5 * math.cos(0.07 * t), lambda t: 3e9 + 5e8 * math.sin(0.03 * t)),
            "P3": (4.0, lambda t: 0.4e-4 + 1e-5 * math.sin(0.19 * t), lambda t: 1.5e9 + 2e8 * math.sin(0.02 * t))}
_CF_CAP = 1.6e12


def _cf_agregada(t: int) -> float:
    num = sum(oi(t) * tasa(t) * (HORAS_DIA / h) * DIAS_ANIO for h, tasa, oi in _CF_PLAT.values())
    return num / sum(oi(t) for _, _, oi in _CF_PLAT.values())


def _cf_dias(t: int) -> int:
    return 30 + t % 60


def _datos_chr_fund(coherente: bool) -> dict[str, Any]:
    plat = {k: {"periodo_horas": h, "historia": [{"fecha": _iso(d), "tasa": tasa(t), "interes_abierto": oi(t)}
                                                  for t, d in enumerate(_CF_FECHAS)]}
            for k, (h, tasa, oi) in _CF_PLAT.items()}
    spot = [60_000.0 + 2_000 * math.sin(0.02 * t) for t in range(len(_CF_FECHAS))]
    fut = []
    for t, d in enumerate(_CF_FECHAS):
        b = _cf_agregada(t) if coherente else _cf_agregada(t) + 0.02 * math.sin(0.3 * t)
        fut.append({"fecha": _iso(d), "precio": spot[t] * (1 + b * _cf_dias(t) / DIAS_ANIO),
                    "vencimiento": _iso(d + pd.Timedelta(days=_cf_dias(t)))})
    return {"plataformas": plat, "futuro": fut, "spot": [{"fecha": _iso(d), "precio": s} for d, s in zip(_CF_FECHAS, spot, strict=True)],
            "capitalizacion": {"fecha": _iso(_CF_FECHAS[-1]), "valor": _CF_CAP}}


def _caso_chr_fund_coherencia(r: dict[str, Any]) -> bool:
    tol = FICHAS["CHR-FUND-001"]["tol"]
    f = _cf_agregada(len(_CF_FECHAS) - 1)
    v = r["verificacion"]
    return (abs(v["base_menos_financiacion_pb"]) <= tol * f * PB and abs(v["base_menos_financiacion_media_pb"]) <= tol * f * PB
            and v["correlacion"] is not None and v["correlacion"] >= 1 - tol and v["n"] == len(_CF_FECHAS))


def _caso_chr_fund_metodo(r: dict[str, Any]) -> bool:
    tol = FICHAS["CHR-FUND-001"]["tol"]
    T = len(_CF_FECHAS) - 1
    pl = {k: tasa(T) * (HORAS_DIA / h) * DIAS_ANIO * PCT for k, (h, tasa, _) in _CF_PLAT.items()}
    oi_T = sum(oi(T) for _, _, oi in _CF_PLAT.values())
    s = 60_000.0 + 2_000 * math.sin(0.02 * T)
    b_raw = _cf_agregada(T) + 0.02 * math.sin(0.3 * T)
    F_ = s * (1 + b_raw * _cf_dias(T) / DIAS_ANIO)
    return (all(_rel(r["financiacion_por_plataforma_pct_anual"][k], pl[k], tol) for k in pl)
            and _rel(r["financiacion_pct_anual"], _cf_agregada(T) * PCT, tol)
            and _rel(r["base_pct_anual"], (F_ / s - 1) * DIAS_ANIO / _cf_dias(T) * PCT, tol)
            and _rel(r["interes_abierto_capitalizacion_pct"], oi_T / _CF_CAP * PCT, tol)
            and _rel(r["pesos"]["P1"], _CF_PLAT["P1"][2](T) / oi_T, tol))


def _caso_chr_fund_percentil(r: dict[str, Any]) -> bool:
    T = len(_CF_FECHAS) - 1
    serie = np.array([_cf_agregada(t) for t in range(len(_CF_FECHAS))])
    ventana = serie[T - 364:]                                            # (T − 365 días, T]
    return r["percentil_financiacion"] == float(np.mean(ventana <= serie[T])) and 0 < r["percentil_financiacion"] < 1


# ---- CHR-FLOW-001
_FL_FECHAS = pd.bdate_range("2024-06-03", periods=300)
_FL_FLUJO = np.array([1e7 * math.sin(0.3 * t) + 5e6 for t in range(len(_FL_FECHAS))])
_FL_PAT = 5e10 + np.cumsum(_FL_FLUJO + np.array([1e8 * math.sin(0.05 * t) for t in range(len(_FL_FECHAS))]))
_FL_SC_FECHAS = pd.date_range("2025-01-01", "2025-07-31", freq="D")
_FL_SC = {"USDX": lambda t: 1.2e11 + 1e8 * t, "EURX": lambda t: 4e10 + 5e7 * t + 1e8 * math.sin(0.1 * t)}
_FL_CAP = 2.9e12


def _datos_chr_flow() -> dict[str, Any]:
    return {"flujos_etf": [{"fecha": _iso(d), "fecha_publicacion": _iso(d + pd.Timedelta(days=1)), "flujo": float(f),
                            "patrimonio": float(p)} for d, f, p in zip(_FL_FECHAS, _FL_FLUJO, _FL_PAT, strict=True)],
            "oferta_stablecoins": {k: [{"fecha": _iso(d), "oferta": fn(t)} for t, d in enumerate(_FL_SC_FECHAS)]
                                   for k, fn in _FL_SC.items()},
            "capitalizacion_total": [{"fecha": _iso(_FL_SC_FECHAS[-1]), "valor": _FL_CAP}]}


def _caso_chr_flow_acumulados(r: dict[str, Any]) -> bool:
    tol = FICHAS["CHR-FLOW-001"]["tol"]
    f = r["flujos"]
    seis_a_veinte = float(np.sum(_FL_FLUJO[-20:-5]))
    return (r["verificacion"]["error_acumulados_max"] <= tol
            and _rel(f["5"]["moneda"], float(np.sum(_FL_FLUJO[-5:])), tol)
            and _rel(f["20"]["moneda"], float(np.sum(_FL_FLUJO[-20:])), tol)
            and _rel(f["20"]["moneda"] - f["5"]["moneda"], seis_a_veinte, tol * PB))


def _caso_chr_flow_metodo(r: dict[str, Any]) -> bool:
    tol = FICHAS["CHR-FLOW-001"]["tol"]
    T = len(_FL_SC_FECHAS) - 1
    o = sum(fn(T) for fn in _FL_SC.values())
    o30 = sum(fn(T - UMBRALES["CHR-FLOW-001"]["dias_crecimiento_stablecoins"]) for fn in _FL_SC.values())
    n = len(_FL_FLUJO)
    return (_rel(r["flujos"]["20"]["pct_patrimonio"], float(np.sum(_FL_FLUJO[-20:])) / float(_FL_PAT[n - 21]) * PCT, tol)
            and _rel(r["crecimiento_stablecoins_pct"], (o / o30 - 1) * PCT, tol)
            and _rel(r["razon_stablecoins_capitalizacion_pct"], o / _FL_CAP * PCT, tol))


def _caso_chr_flow_z(r: dict[str, Any]) -> bool:
    tol = FICHAS["CHR-FLOW-001"]["tol"]
    w, n = 5, len(_FL_FLUJO)
    corte = _FL_FECHAS[-1] - pd.DateOffset(years=1)
    rel = np.array([float(np.sum(_FL_FLUJO[j - w + 1: j + 1])) / float(_FL_PAT[j - w]) for j in range(w, n)
                    if _FL_FECHAS[j] > corte])
    return (_rel(r["flujos"]["5"]["z"], (rel[-1] - rel.mean()) / rel.std(ddof=1), tol)
            and r["flujos"]["5"]["n_z"] == rel.size < n - w)


# ---- ALT-DESMOOTH-001
_AD_N = 48
_AD_FECHAS = pd.date_range("2012-03-31", periods=_AD_N, freq="QE")
_AD_REAL = np.array([0.02 + 0.05 * math.sin(1.3 * t) + 0.03 * math.cos(0.7 * t) for t in range(_AD_N)])
_AD_PHI = 0.4


def _suavizar_geltner(r: np.ndarray, phi: float) -> np.ndarray:
    s = np.empty_like(r)
    s[0] = r[0]
    for t in range(1, r.size):
        s[t] = (1 - phi) * r[t] + phi * s[t - 1]
    return s


def _suavizar_glm(r: np.ndarray, theta: tuple[float, ...]) -> np.ndarray:
    k = len(theta) - 1
    return np.array([r[t] if t < k else sum(theta[j] * r[t - j] for j in range(k + 1)) for t in range(r.size)])


_AD_OBS = _suavizar_geltner(_AD_REAL, _AD_PHI)
# GLM: serie real pseudoaleatoria determinista (sin generador ni semilla), para que el MA(k) tenga sentido
_AD_REAL_GLM = np.array([0.02 + 0.12 * ((math.sin(12.9898 * (t + 1)) * 43758.5453) % 1 - 0.5) for t in range(_AD_N)])
_AD_OBS_GLM = _suavizar_glm(_AD_REAL_GLM, (0.6, 0.3, 0.1))


def _datos_alt(serie: np.ndarray) -> dict[str, Any]:
    return {"rentabilidades": [{"fecha": _iso(d), "r": float(x)} for d, x in zip(_AD_FECHAS, serie, strict=True)],
            "mercado": [{"fecha": _iso(d), "r": 0.015 + 0.1 * ((math.sin(78.233 * (t + 1)) * 43758.5453) % 1 - 0.5)}
                        for t, d in enumerate(_AD_FECHAS)]}


def _serie_alt(r: dict[str, Any]) -> np.ndarray:
    return np.array([x["r"] for x in r["serie_desuavizada"]])


def _caso_alt_phi_cero(r: dict[str, Any]) -> bool:
    tol = FICHAS["ALT-DESMOOTH-001"]["tol"]
    d = _serie_alt(r)
    return (r["phi"] == 0 and d.size == _AD_N - 1 and bool(np.all(np.abs(d - _AD_OBS[1:]) <= tol * np.abs(_AD_OBS[1:])))
            and _rel(r["volatilidad_desuavizada_pct"], r["volatilidad_observada_pct"], tol)
            and _rel(r["mdd_desuavizado_pct"], r["mdd_observado_pct"], tol) and r["mdd_observado_pct"] > 0)


def _caso_alt_geltner(r: dict[str, Any]) -> bool:
    tol = FICHAS["ALT-DESMOOTH-001"]["tol"]
    d = _serie_alt(r)
    borde = _AD_PHI / (1 - _AD_PHI) * (_AD_OBS[-1] - _AD_OBS[0]) / (_AD_N - 1)
    v = r["verificacion"]
    return (bool(np.all(np.abs(d - _AD_REAL[1:]) <= tol * np.max(np.abs(_AD_REAL))))
            and _rel(r["media_desuavizada"], float(np.mean(_AD_REAL[1:])), tol)
            and _rel(v["termino_borde_media"], borde, tol) and abs(borde) > tol
            and v["error_identidad_media"] <= tol * abs(borde) and v["error_resuavizado_max"] <= tol
            and _rel(r["volatilidad_desuavizada_pct"], float(np.std(_AD_REAL[1:], ddof=1)) * 2 * PCT, tol)
            and r["volatilidad_desuavizada_pct"] > r["volatilidad_observada_pct"])


def _caso_alt_ar1(r: dict[str, Any]) -> bool:
    tol = FICHAS["ALT-DESMOOTH-001"]["tol"]
    a, b = _AD_OBS[1:], _AD_OBS[:-1]
    X = np.column_stack([np.ones(b.size), b])
    phi = float(np.linalg.solve(X.T @ X, X.T @ a)[1])                   # MCO con constante (ecuaciones normales)
    d = _serie_alt(r)
    return (_rel(r["phi"], phi, tol) and not r["phi_fijado"]
            and bool(np.all(np.abs(d - (_AD_OBS[1:] - phi * _AD_OBS[:-1]) / (1 - phi)) <= tol))
            and r["verificacion"]["error_identidad_media"] <= tol)


def _caso_alt_glm(r: dict[str, Any]) -> bool:
    tol = FICHAS["ALT-DESMOOTH-001"]["tol"]
    th = np.array(r["theta"])
    v = r["verificacion"]
    d = _serie_alt(r)
    return (th.size == 3 and bool(np.all(th >= 0)) and abs(float(th.sum()) - 1) <= tol and th[0] < 1 and th[1] > 0
            and bool(np.all(np.abs(np.roots(th[::-1])) > 1))
            and v["error_resuavizado_max"] <= tol and v["error_identidad_media"] <= tol
            and abs(float(np.mean(d)) - float(np.mean(_AD_OBS_GLM[2:])) - v["termino_borde_media"]) <= tol
            and _rel(r["indice_suavizado"], float(np.sum(th ** 2)), tol))


def _cerca(a: Any, b: float, tol: float) -> bool:
    return a is not None and abs(float(a) - b) <= tol


def _rel(a: Any, b: float, tol: float) -> bool:
    """Igualdad con la tolerancia relativa de la ficha (3.2)."""
    return a is not None and abs(float(a) - b) <= tol * abs(b)


# Cada caso: una frase comprobable de la «Verificación» de la ficha (o una identidad del «Método»), con datos que no
# anulan sus términos; cada comprobación recalcula el valor esperado desde los datos sintéticos, no desde el resultado.
CASOS_CONTROL: dict[str, list[dict[str, Any]]] = {
    "REI-CAP-001": [
        {"nombre": "coherencia NOI/valor: cap × valor = NOI (tasación y mercado implícito)",
         "datos": [{"valores": _datos_rei_cap()}], "parametros": {},
         "comprobar": lambda r: _rel(r["cap_rate_tasacion_pct"], 52.5e6 / 1.05e9 * PCT, FICHAS["REI-CAP-001"]["tol"])
         and _rel(r["cap_rate_mercado_pct"], 52.5e6 / (6.0e8 + 6.5e8) * PCT, FICHAS["REI-CAP-001"]["tol"])
         and _rel(r["cap_rate_tasacion_pct"] / PCT * 1.05e9, 52.5e6, FICHAS["REI-CAP-001"]["tol"])
         and r["verificacion"]["error_relativo_noi_tasacion"] <= FICHAS["REI-CAP-001"]["tol"]
         and r["verificacion"]["error_relativo_noi_mercado"] <= FICHAS["REI-CAP-001"]["tol"]},
        {"nombre": "diferencial frente al soberano de la misma moneda y su posición en la ventana (15 años)",
         "datos": [{"valores": _datos_rei_cap()}], "parametros": {"ventana": 15},
         "comprobar": _caso_rei_cap_posicion},
        {"nombre": "cap rate de equilibrio ≈ r − g_NOI y brecha frente al de tasación",
         "datos": [{"valores": _datos_rei_cap()}], "parametros": {},
         "comprobar": lambda r: _rel(r["cap_equilibrio_pct"], (0.072 - 0.018) * PCT, FICHAS["REI-CAP-001"]["tol"])
         and _rel(r["brecha_equilibrio_pb"], (0.05 - (0.072 - 0.018)) * PB, FICHAS["REI-CAP-001"]["tol"])},
    ],
    "REI-NAV-001": [
        {"nombre": "NAV = activos − pasivos: con cap_objetivo = cap de tasación el NAV ajustado es el NAV publicado",
         "datos": [{"valores": _datos_rei_nav(misma_cap=True)}], "parametros": {"cap_objetivo": 0.05},
         "comprobar": lambda r: r["verificacion"]["error_relativo_nav_max"] <= FICHAS["REI-NAV-001"]["tol"]
         and _cerca(r["nav_ajustado"]["variacion_pct"], 0.0, FICHAS["REI-NAV-001"]["tol"])
         and _rel(r["nav_ajustado"]["nav_total"], 20.0 * 1e8 + 30.0 * 5e7, FICHAS["REI-NAV-001"]["tol"])
         and all(_rel(c["nav_ajustado"], c["nav"], FICHAS["REI-NAV-001"]["tol"]) for c in r["componentes"].values())},
        {"nombre": "método: P/NAV − 1 ponderado por capitalización, dispersión y NAV ajustado a otro cap rate",
         "datos": [{"valores": _datos_rei_nav(misma_cap=False)}], "parametros": {"cap_objetivo": 0.055},
         "comprobar": _caso_rei_nav_metodo},
        {"nombre": "percentil de la prima agregada frente a ≥ 10 años (RI-MH: media histórica)",
         "datos": [{"valores": _datos_rei_nav(misma_cap=False)}], "parametros": {},
         "comprobar": _caso_rei_nav_percentil},
    ],
    "REI-FFO-001": [
        {"nombre": "reconciliación con el beneficio neto (FFO − amortizaciones + plusvalías = BN; AFFO + CAPEX + ajustes = FFO)",
         "datos": [{"valores": _datos_rei_ffo()}], "parametros": {},
         "comprobar": _caso_rei_ffo_reconciliacion},
        {"nombre": "método: P/FFO, P/AFFO, rendimientos, cobertura en mediana e IQR y percentiles a mano",
         "datos": [{"valores": _datos_rei_ffo()}], "parametros": {},
         "comprobar": _caso_rei_ffo_metodo},
        {"nombre": "CAPEX de mantenimiento estimado como % de rentas cuando no se reporta",
         "datos": [{"valores": _datos_rei_ffo(capex_y_2023=False)}], "parametros": {"capex_pct_rentas": 0.08},
         "comprobar": _caso_rei_ffo_capex},
    ],
    "CMD-INV-001": [
        {"nombre": "media estacional de una serie periódica pura ⇒ desviación 0 (y sorpresa 0)",
         "datos": [{"valores": _datos_cmd_inv(periodica=True)}], "parametros": {},
         "comprobar": _caso_cmd_inv_periodica},
        {"nombre": "segunda vía FX-STL-001 (medias móviles, aditivo): también desviación 0 en la serie periódica pura",
         "datos": [{"valores": _datos_cmd_inv(periodica=True)}], "parametros": {},
         "comprobar": _caso_cmd_inv_stl},
        {"nombre": "método a mano: misma época de los 5 años previos (uno excluido), %, z, cobertura y sorpresa",
         "datos": [{"valores": _datos_cmd_inv(periodica=False)}], "parametros": {"excluir_anos": [2021]},
         "comprobar": _caso_cmd_inv_metodo},
        {"nombre": "segunda vía FX-STL-001 a mano en una serie con tendencia y ruido (índice estacional normalizado)",
         "datos": [{"valores": _datos_cmd_inv(periodica=False)}], "parametros": {},
         "comprobar": _caso_cmd_inv_stl_tendencia},
    ],
    "CMD-RETDEC-001": [
        {"nombre": "suma de componentes = total con índices de exceso y total (calendario del índice)",
         "datos": [{"valores": _datos_cmd_retdec_indice()}], "parametros": {},
         "comprobar": _caso_cmd_retdec_indice},
        {"nombre": "suma de componentes = total con precios de contratos y calendario de roll declarado",
         "datos": [{"valores": _datos_cmd_retdec_contratos()}], "parametros": {"calendario_roll": "declarado"},
         "comprobar": _caso_cmd_retdec_contratos},
    ],
    "CHR-FUND-001": [
        {"nombre": "coherencia base–financiación: base igual a la financiación ponderada ⇒ diferencia 0",
         "datos": [{"valores": _datos_chr_fund(coherente=True)}], "parametros": {},
         "comprobar": _caso_chr_fund_coherencia},
        {"nombre": "método: tasa × periodos por año (8 h y 4 h), ponderada por interés abierto; base (F/S − 1)·365/días",
         "datos": [{"valores": _datos_chr_fund(coherente=False)}], "parametros": {},
         "comprobar": _caso_chr_fund_metodo},
        {"nombre": "percentil de la financiación en 1 año",
         "datos": [{"valores": _datos_chr_fund(coherente=False)}], "parametros": {},
         "comprobar": _caso_chr_fund_percentil},
    ],
    "CHR-FLOW-001": [
        {"nombre": "acumulados coherentes con los flujos diarios (5 y 20 días; 20 = 5 + días 6 a 20)",
         "datos": [{"valores": _datos_chr_flow()}], "parametros": {},
         "comprobar": _caso_chr_flow_acumulados},
        {"nombre": "método: % del patrimonio previo, crecimiento de stablecoins a 30 días y razón con la capitalización",
         "datos": [{"valores": _datos_chr_flow()}], "parametros": {},
         "comprobar": _caso_chr_flow_metodo},
        {"nombre": "z-score del acumulado en 1 año",
         "datos": [{"valores": _datos_chr_flow()}], "parametros": {},
         "comprobar": _caso_chr_flow_z},
    ],
    "ALT-DESMOOTH-001": [
        {"nombre": "φ = 0 ⇒ serie sin cambios (volatilidad y MDD iguales)",
         "datos": [{"valores": _datos_alt(_AD_OBS)}], "parametros": {"phi": 0},
         "comprobar": _caso_alt_phi_cero},
        {"nombre": "Geltner con φ fijado recupera la serie real; media conservada salvo el término de borde exacto",
         "datos": [{"valores": _datos_alt(_AD_OBS)}], "parametros": {"phi": _AD_PHI},
         "comprobar": _caso_alt_geltner},
        {"nombre": "φ estimado = AR(1) por MCO con constante",
         "datos": [{"valores": _datos_alt(_AD_OBS)}], "parametros": {},
         "comprobar": _caso_alt_ar1},
        {"nombre": "GLM: θ ≥ 0 con Σθ = 1, resuavizar reproduce la observada y media conservada salvo el borde",
         "datos": [{"valores": _datos_alt(_AD_OBS_GLM)}], "parametros": {"metodo": "GLM", "k": 2},
         "comprobar": _caso_alt_glm},
    ],
}
