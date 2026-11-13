"""Fichas del Motor del Bloque A · grupo S (estadística y series), T-112 (Motor Fase 2).

Fuente de verdad: «Catálogo de cálculos del Motor - V5.0», fichas ST-INF-001, FX-BRK-001, FX-STL-001, FX-REGIME-001,
FX-COINT-001 y BIB-MET-001 (§6, heredadas de la línea V3.0), REG-HMM-001 y TEM-DIFF-001 (§7), y su §3 (convenciones).
Lo que la ficha no fija y aquí se decide está en `.docs/tickets/T-112/grupo_S.md` (INC-T112-01, `[PROPUESTO]`).

Convenciones de este módulo:

- Interfaz de cada manejador: ``f(ent, params) -> (resultado, limitaciones)``, con
  ``ent = {"valores": {...}, "series": {alias: pd.Series}, "series_rol": {rol: pd.Series}}``.
- Las entradas llegan en línea en ``ent["valores"]`` (listas de números, con ``fechas`` ISO opcionales). Las series de
  HT-01 (``ent["series"]``, cierres con índice de fechas) se aceptan donde la ficha trabaja sobre una serie de precios:
  FX-BRK-001, FX-STL-001 y FX-COINT-001 en niveles, y FX-REGIME-001 sobre sus rendimientos simples (3.1).
- ``PARAMETROS_POR_DEFECTO`` son los parámetros del campo «Parámetros» de cada ficha: la petición los cambia dentro de su
  dominio. ``UMBRALES`` son los umbrales de rechazo y de limitación y las constantes del método: una petición que traiga
  uno se rechaza («umbral fijo de la ficha»). Un parámetro desconocido también se rechaza.
- Falla cerrado: lo que falta, está mal formado o no cumple «Entradas mínimas» o «Aclaración y rechazo» lanza
  ``ErrorFicha``; ningún resultado lleva cifras no finitas (lo indefinido va como ``None`` y se declara).
- Las fichas con azar (FX-REGIME-001, REG-HMM-001 y TEM-DIFF-001) usan la semilla del parámetro ``semilla``; dos pasadas
  con la misma semilla dan el mismo resultado.
- Las «Supuestos y limitaciones» de cada ficha van en ``resultado["advertencias"]`` (``ADVERTENCIAS``), no como
  limitaciones del cálculo.
"""
from __future__ import annotations

import math
import re
import unicodedata
import warnings
from collections.abc import Callable
from datetime import date, datetime
from functools import wraps
from itertools import pairwise
from typing import Any

import numpy as np
import pandas as pd
from scipy import linalg, optimize, stats

from .operaciones import ErrorFicha, cagr

Resultado = tuple[dict[str, Any], list[str]]
Manejador = Callable[[dict[str, Any], dict[str, Any]], Resultado]

DIAS_POR_ANIO = 365.0        # Catálogo 3.1: recuento Real/365 (fechas → años)
EPS = float(np.finfo(float).eps)
# INC-T112-01 [PROPUESTO]: el EM para cuando el cambio relativo máximo de los parámetros baja de tolerancia × 1e-2, para
# que la cifra reproduzca la tolerancia de la ficha (1e-6 en parámetros) con convergencia lineal.
FACTOR_CONVERGENCIA = 1e-2

# ====================================================================== parámetros por defecto (campo «Parámetros»)
PARAMETROS_POR_DEFECTO: dict[str, dict[str, Any]] = {
    # ST-INF-001 · tipo_contraste (declarado, sin valor por defecto); alternativa (bilateral); nivel (0,05);
    # correccion (auto si m > 1). «Potencia y n mínimo bajo petición»: efecto_potencia y potencia_objetivo.
    "ST-INF-001": {"tipo_contraste": None, "alternativa": "bilateral", "nivel": 0.05, "correccion": "auto",
                   "efecto_potencia": None, "potencia_objetivo": None},
    # FX-BRK-001 · max_rupturas (1; 1–5); tipo_cambio (auto); nivel (0,05); recorte (15 %).
    "FX-BRK-001": {"max_rupturas": 1, "tipo_cambio": "auto", "nivel": 0.05, "recorte": 0.15},
    # FX-STL-001 · esquema (auto); periodo (según frecuencia); robusto (true).
    "FX-STL-001": {"esquema": "auto", "periodo": None, "robusto": True},
    # FX-REGIME-001 · n_estados (2; 2–3); varianzas_distintas (true); medias_distintas (false); umbral (0,5; 0,3–0,7).
    # Semilla: «entero del plan si hay arranques aleatorios» (por defecto 0, INC-T112-01).
    "FX-REGIME-001": {"n_estados": 2, "varianzas_distintas": True, "medias_distintas": False, "umbral": 0.5,
                      "semilla": 0},
    # REG-HMM-001 · n_estados (BIC; 2–4); covarianza (diagonal; completa); arranques (20). Semilla: entero del plan.
    "REG-HMM-001": {"n_estados": "BIC", "covarianza": "diagonal", "arranques": 20, "semilla": 0},
    # FX-COINT-001 · metodo (Johansen); max_rezagos (AIC); nivel (0,05).
    "FX-COINT-001": {"metodo": "Johansen", "max_rezagos": "AIC", "nivel": 0.05},
    # BIB-MET-001 · granularidad (mensual); categorias (todas).
    "BIB-MET-001": {"granularidad": "mensual", "categorias": "todas"},
    # TEM-DIFF-001 · modelo (auto); m (estimado o fijado por escenarios); arranques (20); B (1 000). Semilla: entero
    # del plan. Horizonte de la adopción prevista: 5 años, el límite de H4 («años», 1–5) del Documento 0.
    "TEM-DIFF-001": {"modelo": "auto", "m": None, "arranques": 20, "B": 1000, "semilla": 0, "horizonte": 5},
}

# Umbrales y constantes del método: no son parámetros de la petición. Cada uno cita su campo de la ficha (o INC-T112-01).
UMBRALES: dict[str, dict[str, Any]] = {
    # ST-INF-001 · «Tolerancias»: 1e-8. «Aclaración y rechazo»: los datos no sostienen el contraste (n < 2, dispersión
    # nula). «correccion (auto si m > 1)». Normalidad (supuesto del t) con Shapiro-Wilk, que exige n ≥ 3.
    "ST-INF-001": {"n_minimo": 2, "n_minimo_normalidad": 3, "m_correccion": 1, "tolerancia": 1e-8},
    # FX-BRK-001 · «Entradas mínimas»: ≥ 30 observaciones para una ruptura, ≥ 50 para dos o más. «Parámetros»:
    # max_rupturas 1–5. «Tolerancias»: 1e-6.
    "FX-BRK-001": {"obs_una_ruptura": 30, "obs_varias_rupturas": 50, "rango_max_rupturas": [1, 5], "tolerancia": 1e-6},
    # FX-STL-001 · «Entradas mínimas»: ≥ 2 ciclos completos (≥ 3 recomendados). «Tolerancias»: 1e-6.
    # INC-T112-01: suavizador estacional n_s = 7 y bucles (interno, externo) = (2, 15) robusto o (5, 0) sin robustez.
    "FX-STL-001": {"ciclos_minimos": 2, "ciclos_recomendados": 3, "tolerancia": 1e-6, "n_s": 7,
                   "bucles_robusto": [2, 15], "bucles_simple": [5, 0]},
    # FX-REGIME-001 · «Entradas mínimas»: ≥ 100 observaciones (≥ 200 recomendadas). «Parámetros»: n_estados 2–3,
    # umbral 0,3–0,7. «Tolerancias»: 1e-6. Arranques: 20, los de REG-HMM-001. INC-T112-01: tope de 1 000 iteraciones.
    "FX-REGIME-001": {"obs_minimas": 100, "obs_recomendadas": 200, "rango_n_estados": [2, 3], "rango_umbral": [0.3, 0.7],
                      "tolerancia": 1e-6, "arranques": 20, "iteraciones_max": 1000},
    # REG-HMM-001 · «Entradas mínimas»: ≥ 260 semanales o ≥ 120 mensuales. «Parámetros»: n_estados 2–4; arranques ≥ 20
    # («≥ 20 arranques con semilla»). «Tolerancias»: 1e-6. INC-T112-01: tope de 1 000 iteraciones.
    "REG-HMM-001": {"obs_minimas": {"semanal": 260, "mensual": 120}, "rango_n_estados": [2, 4], "arranques_minimos": 20,
                    "tolerancia": 1e-6, "iteraciones_max": 1000},
    # FX-COINT-001 · «Entradas mínimas»: ≥ 50 observaciones comunes. «Tolerancias»: 1e-6. INC-T112-01: valores
    # críticos asintóticos (MacKinnon 2010 para ADF y Engle-Granger; MacKinnon, Haug y Michelis 1999, caso 2 de constante
    # restringida, para la traza de Johansen) a los niveles 0,10, 0,05 y 0,01, hasta 5 series.
    "FX-COINT-001": {"obs_minimas": 50, "tolerancia": 1e-6, "series_maximas": 5, "niveles": [0.01, 0.05, 0.10]},
    # BIB-MET-001 · «Tolerancias»: conteos exactos. Granularidades: mensual (por defecto), trimestral, anual.
    "BIB-MET-001": {"granularidades": ["mensual", "trimestral", "anual"]},
    # TEM-DIFF-001 · «Entradas mínimas»: ≥ 8 observaciones con un tramo de aceleración. «Método»: fases introducción
    # < 16 %, crecimiento 16–50 %, madurez > 50 % de m; bandas 10/50/90. «Tolerancias»: 1e-6. Horizonte ≤ 30 años
    # (límite de H5 en el Documento 0).
    "TEM-DIFF-001": {"obs_minimas": 8, "fases": [0.16, 0.50], "cuantiles_bandas": [0.10, 0.50, 0.90],
                     "tolerancia": 1e-6, "horizonte_max": 30},
}

# Advertencias obligatorias de entrega («Supuestos y limitaciones» de cada ficha).
ADVERTENCIAS: dict[str, list[str]] = {
    "ST-INF-001": ["la significación no es relevancia", "el p-valor no es P(H₀)"],
    "FX-BRK-001": ["homocedasticidad dentro de los segmentos (salvo ruptura de varianza)",
                   "una revisión de la fuente puede imitar una ruptura", "la ruptura no identifica su causa"],
    "FX-STL-001": ["la descomposición no es única", "inestable en series cortas"],
    "FX-REGIME-001": ["número de regímenes declarado (BIC)", "los regímenes en series cortas pueden ser artefactos",
                      "usar las probabilidades suavizadas en una previsión es fuga"],
    "REG-HMM-001": ["probabilidades suavizadas solo descriptivas (usarlas en previsión es fuga)",
                    "los regímenes pueden no repetirse"],
    "FX-COINT-001": ["estabilidad del vector obligatoria en PLAN_STD", "baja potencia en muestras cortas",
                     "no es causalidad"],
    "BIB-MET-001": ["describe el corpus registrado, no la literatura", "las citas no son calidad",
                    ("solicitantes por CT-09: Orquestador técnico (paquetes CT-21) y Evaluador; los agentes de "
                     "conocimiento no son clientes del CT-09")],
    "TEM-DIFF-001": ["antes del punto de inflexión el techo m está muy mal identificado (bandas muy anchas)",
                     "la difusión de una tecnología no implica rentabilidad para el inversor (competencia, valoración)"],
}

# Dominio de cada parámetro de la petición: (tipo, comprobación).
_OPCIONES: dict[str, dict[str, tuple[str, ...]]] = {
    "ST-INF-001": {"tipo_contraste": ("t_una_muestra", "t_pareado", "t_welch", "wilcoxon", "mann_whitney"),
                   "alternativa": ("bilateral", "mayor", "menor"), "correccion": ("auto", "holm", "bh")},
    "FX-BRK-001": {"tipo_cambio": ("auto", "nivel", "pendiente", "varianza")},
    "FX-STL-001": {"esquema": ("auto", "aditivo", "multiplicativo")},
    "REG-HMM-001": {"covarianza": ("diagonal", "completa")},
    "FX-COINT-001": {"metodo": ("Johansen", "Engle-Granger")},
    "TEM-DIFF-001": {"modelo": ("auto", "logistica", "gompertz", "bass")},
}


# ====================================================================== utilidades comunes
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
        raise ErrorFicha(f"{que}: {f:g} fuera del dominio (mínimo {lo:g}{', excluido' if abierto_lo else ''})")
    if hi is not None and (f > hi or (abierto_hi and f == hi)):
        raise ErrorFicha(f"{que}: {f:g} fuera del dominio (máximo {hi:g}{', excluido' if abierto_hi else ''})")
    return f


def _entero(x: Any, que: str, lo: int | None = None, hi: int | None = None) -> int:
    f = _rango(x, que, lo, hi)
    if f != math.floor(f):
        raise ErrorFicha(f"{que}: se esperaba un entero ({f:g})")
    return int(f)


def _booleano(x: Any, que: str) -> bool:
    if not isinstance(x, (bool, np.bool_)):
        raise ErrorFicha(f"{que}: se esperaba true o false")
    return bool(x)


def _opcion(F: str, clave: str, x: Any) -> str:
    opciones = _OPCIONES[F][clave]
    if not isinstance(x, str) or x not in opciones:
        raise ErrorFicha(f"{F}: {clave} «{str(x)[:40]}» no admitido ({', '.join(opciones)})")
    return x


def _dict(x: Any, que: str) -> dict[str, Any]:
    if not isinstance(x, dict):
        raise ErrorFicha(f"{que}: se esperaba un objeto (dict)")
    return x


def _lista(x: Any, que: str) -> list[Any]:
    if isinstance(x, np.ndarray):
        return list(x)
    if not isinstance(x, (list, tuple)):
        raise ErrorFicha(f"{que}: se esperaba una lista")
    return list(x)


def _vector(x: Any, que: str, minimo: int = 1) -> np.ndarray:
    a = np.array([_num(e, que) for e in _lista(x, que)], dtype=float)
    if len(a) < minimo:
        raise ErrorFicha(f"{que}: {len(a)} valores (< {minimo})")
    return a


_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}([T ].*)?$")


def _fecha(x: Any, que: str) -> date:
    """Fecha ISO («AAAA-MM-DD»), `date` o `Timestamp`; un número no es una fecha."""
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


def _fechas(x: Any, n: int, que: str) -> list[str] | None:
    """Fechas ISO estrictamente crecientes alineadas con la serie (o None si no se dan)."""
    if x is None:
        return None
    fs = [_fecha(f, que) for f in _lista(x, que)]
    if len(fs) != n:
        raise ErrorFicha(f"{que}: {len(fs)} fechas para {n} observaciones")
    if any(b <= a for a, b in pairwise(fs)):
        raise ErrorFicha(f"{que}: las fechas deben ser estrictamente crecientes (sin repetidas)")
    return [f.isoformat() for f in fs]


def _parametros(F: str, params: Any) -> dict[str, Any]:
    """Parámetros de la petición encima de los de la ficha, validados; un umbral fijo o un parámetro desconocido se
    rechazan. `clase` la añade el servicio a toda petición y no es un parámetro de estas fichas."""
    params = _dict(params if params is not None else {}, f"{F}: parámetros")
    fijos = set(params) & set(UMBRALES[F])
    if fijos:
        raise ErrorFicha(f"{F}: {sorted(fijos)} son umbrales fijos de la ficha, no parámetros de la petición")
    desconocidos = set(params) - set(PARAMETROS_POR_DEFECTO[F]) - {"clase"}
    if desconocidos:
        raise ErrorFicha(f"{F}: parámetros desconocidos {sorted(desconocidos)[:5]}")
    p = dict(PARAMETROS_POR_DEFECTO[F])
    p.update({k: v for k, v in params.items() if k in p and v is not None})
    _validar(F, p)
    p.update(UMBRALES[F])
    return p


def _validar(F: str, p: dict[str, Any]) -> None:
    """Tipo y dominio de cada parámetro de la petición (H-24 de T-108)."""
    u = UMBRALES[F]
    for clave in _OPCIONES.get(F, {}):
        if p.get(clave) is not None:
            p[clave] = _opcion(F, clave, p[clave])
    if "semilla" in p:
        p["semilla"] = _entero(p["semilla"], f"{F}: semilla", 0)
    if F == "ST-INF-001":
        p["nivel"] = _rango(p["nivel"], f"{F}: nivel", 0, 1, True, True)
        if p["efecto_potencia"] is not None:
            p["efecto_potencia"] = _rango(p["efecto_potencia"], f"{F}: efecto_potencia", 0, abierto_lo=True)
        if p["potencia_objetivo"] is not None:
            p["potencia_objetivo"] = _rango(p["potencia_objetivo"], f"{F}: potencia_objetivo", 0, 1, True, True)
            if p["efecto_potencia"] is None:
                raise ErrorFicha(f"{F}: potencia_objetivo exige efecto_potencia (tamaño de efecto d)")
    elif F == "FX-BRK-001":
        p["max_rupturas"] = _entero(p["max_rupturas"], f"{F}: max_rupturas", *u["rango_max_rupturas"])
        p["nivel"] = _rango(p["nivel"], f"{F}: nivel", 0, 1, True, True)
        p["recorte"] = _rango(p["recorte"], f"{F}: recorte", 0, 1 / (p["max_rupturas"] + 1), True, False)
    elif F == "FX-STL-001":
        if p["periodo"] is not None:
            p["periodo"] = _entero(p["periodo"], f"{F}: periodo", 2)
        p["robusto"] = _booleano(p["robusto"], f"{F}: robusto")
    elif F == "FX-REGIME-001":
        p["n_estados"] = _entero(p["n_estados"], f"{F}: n_estados", *u["rango_n_estados"])
        p["varianzas_distintas"] = _booleano(p["varianzas_distintas"], f"{F}: varianzas_distintas")
        p["medias_distintas"] = _booleano(p["medias_distintas"], f"{F}: medias_distintas")
        if not (p["varianzas_distintas"] or p["medias_distintas"]):
            raise ErrorFicha(f"{F}: sin medias ni varianzas distintas no hay regímenes que estimar")
        p["umbral"] = _rango(p["umbral"], f"{F}: umbral", *u["rango_umbral"])
    elif F == "REG-HMM-001":
        if p["n_estados"] != "BIC":
            p["n_estados"] = _entero(p["n_estados"], f"{F}: n_estados", *u["rango_n_estados"])
        p["arranques"] = _entero(p["arranques"], f"{F}: arranques", u["arranques_minimos"])
    elif F == "FX-COINT-001":
        if p["max_rezagos"] != "AIC":
            p["max_rezagos"] = _entero(p["max_rezagos"], f"{F}: max_rezagos", 0)
        nivel = _num(p["nivel"], f"{F}: nivel")
        if not any(math.isclose(nivel, x) for x in u["niveles"]):
            raise ErrorFicha(f"{F}: nivel {nivel:g} sin valor crítico tabulado (admitidos: 0,01, 0,05, 0,10)")
        p["nivel"] = min(u["niveles"], key=lambda x: abs(x - nivel))
    elif F == "BIB-MET-001":
        if p["granularidad"] not in u["granularidades"]:
            raise ErrorFicha(f"{F}: granularidad «{str(p['granularidad'])[:40]}» no admitida "
                             f"({', '.join(u['granularidades'])})")
        if p["categorias"] != "todas":
            cats = _lista(p["categorias"], f"{F}: categorias")
            if not cats or not all(isinstance(c, str) and c.strip() for c in cats):
                raise ErrorFicha(f"{F}: categorias debe ser «todas» o una lista de temáticas")
            p["categorias"] = sorted({c.strip() for c in cats})
    elif F == "TEM-DIFF-001":
        p["arranques"] = _entero(p["arranques"], f"{F}: arranques", 1)
        p["B"] = _entero(p["B"], f"{F}: B", 1)
        p["horizonte"] = _rango(p["horizonte"], f"{F}: horizonte", 0, u["horizonte_max"], abierto_lo=True)
        m = p["m"]
        if m is not None:
            if isinstance(m, (list, tuple)):
                if not m:
                    raise ErrorFicha(f"{F}: m: lista de escenarios vacía")
                p["m"] = [_rango(x, f"{F}: m (escenario)", 0, abierto_lo=True) for x in m]
            else:
                p["m"] = _rango(m, f"{F}: m", 0, abierto_lo=True)


def _no_finitos(x: Any, ruta: str = "resultado") -> list[str]:
    if isinstance(x, dict):
        return [r for k, v in x.items() for r in _no_finitos(v, f"{ruta}.{k}")]
    if isinstance(x, (list, tuple)):
        return [r for i, v in enumerate(x) for r in _no_finitos(v, f"{ruta}[{i}]")]
    if isinstance(x, (float, np.floating)) and not math.isfinite(float(x)):
        return [ruta]
    return []


def _json(x: Any) -> Any:
    """Copia JSON del resultado (tipos de numpy a tipos de Python)."""
    if isinstance(x, dict):
        return {str(k): _json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json(v) for v in x]
    if isinstance(x, np.ndarray):
        return [_json(v) for v in x.tolist()]
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        return float(x)
    return x


def _cerrado(F: str) -> Callable[[Manejador], Manejador]:
    """Falla cerrado: entradas mal formadas o fuera de dominio y resultados no finitos dan ErrorFicha."""
    def decorar(fn: Manejador) -> Manejador:
        @wraps(fn)
        def envoltura(ent: Any, params: Any = None) -> Resultado:
            if not isinstance(ent, dict):
                raise ErrorFicha(f"{F}: la entrada debe ser un objeto")
            for clave in ("valores", "series", "series_rol"):
                if ent.get(clave) is not None and not isinstance(ent[clave], dict):
                    raise ErrorFicha(f"{F}: «{clave}» debe ser un objeto")
            ent = {"valores": ent.get("valores") or {}, "series": ent.get("series") or {},
                   "series_rol": ent.get("series_rol") or {}}
            try:
                with np.errstate(all="ignore"):
                    res, lim = fn(ent, _parametros(F, params))
            except ErrorFicha:
                raise
            except (ArithmeticError, ValueError, TypeError, AttributeError, KeyError, IndexError, RuntimeError,
                    np.linalg.LinAlgError) as e:
                raise ErrorFicha(f"{F}: entrada mal formada o fuera de dominio ({type(e).__name__}: {e})") from e
            res = _json(res)
            malos = _no_finitos(res)
            if malos:
                raise ErrorFicha(f"{F}: resultado no finito en {', '.join(malos[:3])} (entradas fuera de dominio)")
            res["advertencias"] = list(ADVERTENCIAS[F])
            return res, lim
        return envoltura
    return decorar


def _serie_ht01(s: Any, que: str) -> tuple[np.ndarray, list[str]]:
    if not isinstance(s, pd.Series) or not isinstance(s.index, pd.DatetimeIndex):
        raise ErrorFicha(f"{que}: se esperaba una serie con índice de fechas")
    s = s.sort_index()
    if s.index.has_duplicates:
        raise ErrorFicha(f"{que}: fechas repetidas")
    if s.isna().any():
        raise ErrorFicha(f"{que}: la serie tiene huecos (NaN); la ficha no imputa")
    return _vector(list(s.to_numpy()), que), [i.date().isoformat() for i in s.index]


def _univariante(ent: dict[str, Any], F: str, rendimientos: bool = False) -> tuple[np.ndarray, list[str] | None, str]:
    """Serie de `valores["serie"]` (con `valores["fechas"]` opcional) o la única serie de HT-01 de la petición."""
    v = _dict(ent["valores"], f"{F}: valores")
    if v.get("serie") is not None:
        y = _vector(v["serie"], f"{F}: serie")
        return y, _fechas(v.get("fechas"), len(y), f"{F}: fechas"), "valores"
    series = list(ent["series"].values()) + list(ent["series_rol"].values())
    if len(series) != 1:
        raise ErrorFicha(f"{F}: falta «serie» en valores (o exactamente una serie de HT-01)")
    y, fechas = _serie_ht01(series[0], f"{F}: serie de HT-01")
    if rendimientos:
        if np.any(y[:-1] == 0):
            raise ErrorFicha(f"{F}: precio nulo en la serie de HT-01 (rendimiento indefinido)")
        return y[1:] / y[:-1] - 1, fechas[1:], "HT-01 (rendimientos simples)"
    return y, fechas, "HT-01"


def _frecuencia(fechas: list[str]) -> str | None:
    """Frecuencia de pandas («MS», «W-FRI», «QS-OCT»…) o None si es irregular."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        f = pd.infer_freq(pd.DatetimeIndex(fechas))
    if f is not None and not isinstance(f, str):
        f = f.freqstr
    return f


def _etiqueta(i: int, fechas: list[str] | None) -> str | None:
    return fechas[i] if fechas is not None and 0 <= i < len(fechas) else None


# ====================================================================== ST-INF-001
_SCIPY_ALT = {"bilateral": "two-sided", "mayor": "greater", "menor": "less"}


def _p_t(t: float, gl: float, alternativa: str) -> float:
    if alternativa == "bilateral":
        return float(2 * stats.t.sf(abs(t), gl))
    if alternativa == "mayor":
        return float(stats.t.sf(t, gl))
    return float(stats.t.cdf(t, gl))


def _ic_t(centro: float, ee: float, gl: float, nivel: float, alternativa: str) -> dict[str, Any]:
    if alternativa == "bilateral":
        c = float(stats.t.ppf(1 - nivel / 2, gl))
        return {"inferior": centro - c * ee, "superior": centro + c * ee, "confianza": 1 - nivel}
    c = float(stats.t.ppf(1 - nivel, gl))
    if alternativa == "mayor":
        return {"inferior": centro - c * ee, "superior": None, "confianza": 1 - nivel}
    return {"inferior": None, "superior": centro + c * ee, "confianza": 1 - nivel}


def _estadisticos(x: Any, que: str, u: dict[str, Any]) -> tuple[float, float, int, np.ndarray | None]:
    """(media, desviación, n, muestra o None) a partir de una muestra o de sus estadísticos suficientes."""
    if isinstance(x, dict):
        n = _entero(x.get("n"), f"{que}: n", u["n_minimo"])
        return (_num(x.get("media"), f"{que}: media"), _rango(x.get("desviacion"), f"{que}: desviacion", 0), n, None)
    a = _vector(x, que)
    if len(a) < u["n_minimo"]:
        raise ErrorFicha(f"{que}: {len(a)} observaciones (< {u['n_minimo']}): los datos no sostienen el contraste")
    return float(a.mean()), float(a.std(ddof=1)), len(a), a


def _normalidad(a: np.ndarray | None, nombre: str, p: dict[str, Any], lim: list[str]) -> float | None:
    if a is None or len(a) < p["n_minimo_normalidad"] or float(np.ptp(a)) == 0:
        return None
    pv = float(stats.shapiro(a).pvalue)
    if pv < p["nivel"]:
        lim.append(f"«{nombre}»: normalidad rechazada (Shapiro-Wilk p = {pv:.4g}); considere un contraste de rangos")
    return pv


def _potencia_t(d: float, gl: float, ncp_por_d: float, nivel: float, alternativa: str) -> float:
    ncp = d * ncp_por_d
    if alternativa == "bilateral":
        c = stats.t.ppf(1 - nivel / 2, gl)
        return float(stats.nct.sf(c, gl, ncp) + stats.nct.cdf(-c, gl, ncp))
    c = stats.t.ppf(1 - nivel, gl)
    return float(stats.nct.sf(c, gl, ncp))   # d > 0 en la dirección de la alternativa


def _potencia(tipo: str, n: int | tuple[int, int], p: dict[str, Any]) -> dict[str, Any] | None:
    d, objetivo, nivel, alt = p["efecto_potencia"], p["potencia_objetivo"], p["nivel"], p["alternativa"]
    if d is None:
        return None

    def pot(nn: int | tuple[int, int]) -> float:
        if isinstance(nn, tuple):
            n1, n2 = nn
            return _potencia_t(d, n1 + n2 - 2, 1 / math.sqrt(1 / n1 + 1 / n2), nivel, alt)
        return _potencia_t(d, nn - 1, math.sqrt(nn), nivel, alt)

    out: dict[str, Any] = {"efecto_d": d, "potencia": pot(n), "potencia_objetivo": objetivo, "n_minimo": None}
    if objetivo is not None:
        dos = tipo == "t_welch"
        z = stats.norm.ppf(1 - nivel / 2 if alt == "bilateral" else 1 - nivel) + stats.norm.ppf(objetivo)
        m = max(2, math.ceil((2 if dos else 1) * (z / d) ** 2))

        def pm(k: int) -> float:
            return pot((k, k)) if dos else pot(k)
        while pm(m) < objetivo:
            m += 1
        while m > 2 and pm(m - 1) >= objetivo:
            m -= 1
        out["n_minimo"] = m
        out["n_minimo_es_por_grupo"] = dos
    return out


def _un_contraste(c: dict[str, Any], nombre: str, p: dict[str, Any], lim: list[str]) -> dict[str, Any]:
    F, tipo, alt, nivel = "ST-INF-001", p["tipo_contraste"], p["alternativa"], p["nivel"]
    que = f"{F}: contraste «{nombre}»"
    mu0 = _num(c.get("mu0", 0.0), f"{que}: mu0")
    r: dict[str, Any] = {"tipo": tipo, "alternativa": alt, "mu0": mu0}
    if tipo in ("t_una_muestra", "t_pareado"):
        if tipo == "t_pareado":
            a = _vector(c.get("muestra_a"), f"{que}: muestra_a")
            b = _vector(c.get("muestra_b"), f"{que}: muestra_b")
            if len(a) != len(b):
                raise ErrorFicha(f"{que}: muestras pareadas de distinta longitud ({len(a)} y {len(b)})")
            x: Any = list(a - b)
        else:
            x = c.get("muestra") if c.get("muestra") is not None else c.get("estadisticos")
            if x is None:
                raise ErrorFicha(f"{que}: falta «muestra» o «estadisticos»")
        media, sd, n, arr = _estadisticos(x, que, p)
        if sd == 0:
            raise ErrorFicha(f"{que}: dispersión nula: los datos no sostienen el contraste")
        ee = sd / math.sqrt(n)
        t = (media - mu0) / ee
        r.update({"n": n, "media": media, "desviacion": sd, "estadistico": t, "gl": n - 1,
                  "p_valor": _p_t(t, n - 1, alt), "ic": _ic_t(media, ee, n - 1, nivel, alt),
                  "efecto": {"tipo": "d_cohen", "valor": (media - mu0) / sd},
                  "normalidad_p": _normalidad(arr, nombre, p, lim), "potencia": _potencia(tipo, n, p)})
    elif tipo == "t_welch":
        xa = c.get("muestra_a") if c.get("muestra_a") is not None else c.get("estadisticos_a")
        xb = c.get("muestra_b") if c.get("muestra_b") is not None else c.get("estadisticos_b")
        if xa is None or xb is None:
            raise ErrorFicha(f"{que}: faltan las dos muestras (o sus estadísticos)")
        m1, s1, n1, a1 = _estadisticos(xa, f"{que}: a", p)
        m2, s2, n2, a2 = _estadisticos(xb, f"{que}: b", p)
        v1, v2 = s1 ** 2 / n1, s2 ** 2 / n2
        if v1 + v2 == 0:
            raise ErrorFicha(f"{que}: dispersión nula en las dos muestras: los datos no sostienen el contraste")
        ee = math.sqrt(v1 + v2)
        gl = (v1 + v2) ** 2 / ((v1 ** 2 / (n1 - 1) if v1 else 0.0) + (v2 ** 2 / (n2 - 1) if v2 else 0.0))
        t = (m1 - m2 - mu0) / ee
        r.update({"n": [n1, n2], "media": [m1, m2], "desviacion": [s1, s2], "estadistico": t, "gl": gl,
                  "p_valor": _p_t(t, gl, alt), "ic": _ic_t(m1 - m2, ee, gl, nivel, alt),
                  "efecto": {"tipo": "d_cohen", "valor": (m1 - m2 - mu0) / math.sqrt((s1 ** 2 + s2 ** 2) / 2)},
                  "normalidad_p": [_normalidad(a1, nombre + " (a)", p, lim), _normalidad(a2, nombre + " (b)", p, lim)],
                  "potencia": _potencia(tipo, (n1, n2), p)})
    elif tipo == "wilcoxon":
        if c.get("muestra_a") is not None or c.get("muestra_b") is not None:
            a = _vector(c.get("muestra_a"), f"{que}: muestra_a")
            b = _vector(c.get("muestra_b"), f"{que}: muestra_b")
            if len(a) != len(b):
                raise ErrorFicha(f"{que}: muestras pareadas de distinta longitud ({len(a)} y {len(b)})")
            dif = a - b - mu0
        else:
            dif = _vector(c.get("muestra"), f"{que}: muestra") - mu0
        dif = dif[dif != 0]
        if len(dif) < p["n_minimo"]:
            raise ErrorFicha(f"{que}: menos de {p['n_minimo']} diferencias no nulas: los datos no sostienen el contraste")
        rangos = stats.rankdata(np.abs(dif))
        w_mas, w_menos = float(rangos[dif > 0].sum()), float(rangos[dif < 0].sum())
        res = stats.wilcoxon(dif, alternative=_SCIPY_ALT[alt])
        r.update({"n": len(dif), "estadistico": w_mas, "p_valor": float(res.pvalue), "ic": None,
                  "efecto": {"tipo": "correlacion_biserial_de_rangos", "valor": (w_mas - w_menos) / (w_mas + w_menos)}})
        lim.append(f"«{nombre}»: contraste de rangos sin IC (solo el p-valor)")
    else:   # mann_whitney
        a = _vector(c.get("muestra_a"), f"{que}: muestra_a", p["n_minimo"]) - mu0
        b = _vector(c.get("muestra_b"), f"{que}: muestra_b", p["n_minimo"])
        if float(np.ptp(np.concatenate([a, b]))) == 0:
            raise ErrorFicha(f"{que}: todas las observaciones empatadas: los datos no sostienen el contraste")
        res = stats.mannwhitneyu(a, b, alternative=_SCIPY_ALT[alt])
        u1 = float(res.statistic)
        r.update({"n": [len(a), len(b)], "estadistico": u1, "p_valor": float(res.pvalue), "ic": None,
                  "efecto": {"tipo": "correlacion_biserial_de_rangos", "valor": 2 * u1 / (len(a) * len(b)) - 1}})
        lim.append(f"«{nombre}»: contraste de rangos sin IC (solo el p-valor)")
    if p["efecto_potencia"] is not None and tipo in ("wilcoxon", "mann_whitney"):
        lim.append(f"«{nombre}»: potencia solo para los contrastes t")
    r["rechaza_h0"] = r["p_valor"] < nivel
    return r


def ajuste_holm(pv: list[float]) -> list[float]:
    """Holm (1979): p̃_(i) = máx_{j ≤ i} mín(1, (m − j + 1)·p_(j))."""
    m = len(pv)
    orden = np.argsort(pv, kind="stable")
    adj = np.empty(m)
    acumulado = 0.0
    for j, i in enumerate(orden):
        acumulado = max(acumulado, min(1.0, (m - j) * pv[i]))
        adj[i] = acumulado
    return [float(x) for x in adj]


def ajuste_bh(pv: list[float]) -> list[float]:
    """Benjamini-Hochberg (1995): p̃_(i) = mín_{j ≥ i} mín(1, m·p_(j)/j)."""
    m = len(pv)
    orden = np.argsort(pv, kind="stable")
    adj = np.empty(m)
    acumulado = 1.0
    for j in range(m - 1, -1, -1):
        i = orden[j]
        acumulado = min(acumulado, m * pv[i] / (j + 1))
        adj[i] = acumulado
    return [float(x) for x in adj]


@_cerrado("ST-INF-001")
def f_st_inf(ent: dict[str, Any], p: dict[str, Any]) -> Resultado:
    F, lim = "ST-INF-001", []
    if p["tipo_contraste"] is None:
        raise ErrorFicha(f"{F}: contraste no declarado (tipo_contraste: {', '.join(_OPCIONES[F]['tipo_contraste'])})")
    v = _dict(ent["valores"], f"{F}: valores")
    if v.get("contrastes") is not None:
        contrastes = [_dict(c, f"{F}: contraste") for c in _lista(v["contrastes"], f"{F}: contrastes")]
    elif ent["series"]:
        if p["tipo_contraste"] not in ("t_una_muestra", "wilcoxon"):
            raise ErrorFicha(f"{F}: con series de HT-01 solo hay contrastes de una muestra (rendimientos frente a 0)")
        contrastes = []
        for alias, s in sorted(ent["series"].items()):
            y, _ = _serie_ht01(s, f"{F}: serie «{alias}»")
            if np.any(y[:-1] == 0):
                raise ErrorFicha(f"{F}: precio nulo en «{alias}»")
            contrastes.append({"nombre": str(alias), "muestra": list(y[1:] / y[:-1] - 1), "mu0": 0.0})
        lim.append("series de HT-01: contraste sobre los rendimientos simples frente a 0")
    else:
        raise ErrorFicha(f"{F}: faltan «contrastes» (muestras o estadísticos suficientes)")
    if not contrastes:
        raise ErrorFicha(f"{F}: lista de contrastes vacía")
    nombres = [str(c.get("nombre") or f"c{i + 1}") for i, c in enumerate(contrastes)]
    if len(set(nombres)) != len(nombres):
        raise ErrorFicha(f"{F}: nombres de contraste repetidos")
    tabla = {nom: _un_contraste(c, nom, p, lim) for nom, c in zip(nombres, contrastes, strict=True)}
    m = len(tabla)
    pv = [tabla[n]["p_valor"] for n in nombres]
    if m > p["m_correccion"]:
        metodo = "holm" if p["correccion"] in ("auto", "holm") else "bh"
        adj = ajuste_holm(pv) if metodo == "holm" else ajuste_bh(pv)
    else:
        metodo, adj = "ninguna (m = 1)", pv
    for nom, a in zip(nombres, adj, strict=True):
        tabla[nom]["p_ajustado"] = a
        tabla[nom]["rechaza_h0_ajustado"] = a < p["nivel"]
    return {"contrastes": tabla, "m": m, "correccion": metodo, "nivel": p["nivel"],
            "referencia_ingenua": "RI-NA"}, lim


# ====================================================================== FX-BRK-001
def _coste_segmentos(s: np.ndarray, tipo: str, h: int) -> np.ndarray:
    """C[i, j] = coste (−2·log-verosimilitud sin constantes, o SSR) del segmento s[i:j]; inf si j − i < h.

    nivel: SSR de la media; pendiente: SSR de la recta (constante + tendencia); varianza: n_s·ln(σ̂²_s) con la media
    global (la serie llega ya centrada)."""
    n = len(s)
    t = np.arange(n, dtype=float) - (n - 1) / 2
    c1 = np.concatenate([[0.0], np.cumsum(s)])
    c2 = np.concatenate([[0.0], np.cumsum(s * s)])
    i, j = np.meshgrid(np.arange(n + 1), np.arange(n + 1), indexing="ij")
    largo = (j - i).astype(float)
    valido = (j - i) >= h
    with np.errstate(all="ignore"):
        sy, syy = c1[j] - c1[i], c2[j] - c2[i]
        if tipo == "varianza":
            var = syy / largo
            C = largo * np.log(var)
            C[~(var > EPS * max(float(np.mean(s * s)), EPS))] = np.inf
        elif tipo == "nivel":
            C = syy - sy ** 2 / largo
        else:
            ct = np.concatenate([[0.0], np.cumsum(t)])
            ctt = np.concatenate([[0.0], np.cumsum(t * t)])
            cty = np.concatenate([[0.0], np.cumsum(t * s)])
            st, stt, sty = ct[j] - ct[i], ctt[j] - ctt[i], cty[j] - cty[i]
            det = largo * stt - st ** 2
            C = syy - (stt * sy ** 2 - 2 * st * sy * sty + largo * sty ** 2) / det
        if tipo != "varianza":
            C = np.maximum(C, 0.0)
    C[~valido] = np.inf
    return C


def _particion_optima(C: np.ndarray, m: int, n: int) -> tuple[float, list[int]]:
    """Programación dinámica de Bai y Perron (2003): mínimo de Σ C sobre m + 1 segmentos; devuelve (coste, rupturas)."""
    costo = C[0].copy()                 # costo[j]: mejor partición de s[0:j] en 1 segmento
    previos: list[np.ndarray] = []
    for _ in range(m):
        tot = costo[:, None] + C        # tot[i, j] = mejor(s[0:i]) + C[i, j]
        arg = np.argmin(tot, axis=0)
        costo = tot[arg, np.arange(n + 1)]
        previos.append(arg)
    rupturas, j = [], n
    for arg in reversed(previos):
        j = int(arg[j])
        rupturas.append(j)
    return float(costo[n]), sorted(rupturas)


def _cuantil_bai(confianza: float) -> float:
    """Cuantil de |V|, V = argmax de W(s) − |s|/2 (Bai 1997, CDF de Yao 1987): P(|V| ≤ x) = 2·G(x) − 1, con
    G(x) = 1 + √(x/2π)·e^{−x/8} − (x + 5)/2·Φ(−√x/2) + (3/2)·eˣ·Φ(−3√x/2)."""
    def G(x: float) -> float:
        r = math.sqrt(x)
        return (1 + math.sqrt(x / (2 * math.pi)) * math.exp(-x / 8) - (x + 5) / 2 * float(stats.norm.cdf(-r / 2))
                + 1.5 * math.exp(x + float(stats.norm.logcdf(-1.5 * r))))

    hi = 1.0
    while 2 * G(hi) - 1 < confianza:
        hi *= 2
    return float(optimize.brentq(lambda x: 2 * G(x) - 1 - confianza, 1e-12, hi, xtol=1e-12))


def _senal(y: np.ndarray, tipo: str) -> np.ndarray:
    """Serie en la que la ruptura del tipo es un cambio de media: nivel → y; pendiente → Δy; varianza → (y − ȳ)²."""
    if tipo == "nivel":
        return y
    if tipo == "pendiente":
        return np.diff(y)
    return (y - y.mean()) ** 2


def _cusum(s: np.ndarray) -> dict[str, Any]:
    """CUSUM de residuos MCO (Page 1954; Ploberger y Krämer 1992): máx |Σ(s − s̄)|/(σ̂·√n) → sup del puente browniano."""
    n = len(s)
    sd = float(s.std(ddof=1))
    if sd == 0:
        return {"estadistico": 0.0, "p_valor": 1.0, "indice_senal": None}
    S = np.cumsum(s - s.mean())[:-1] / (sd * math.sqrt(n))
    k = int(np.argmax(np.abs(S)))
    est = float(abs(S[k]))
    return {"estadistico": est, "p_valor": float(stats.kstwobign.sf(est)), "indice_senal": k + 1}


@_cerrado("FX-BRK-001")
def f_fx_brk(ent: dict[str, Any], p: dict[str, Any]) -> Resultado:
    F, lim = "FX-BRK-001", []
    y, fechas, origen = _univariante(ent, F)
    n, M = len(y), p["max_rupturas"]
    if n < p["obs_una_ruptura"]:
        raise ErrorFicha(f"{F}: {n} observaciones (< {p['obs_una_ruptura']} para una ruptura)")
    if M > 1 and n < p["obs_varias_rupturas"]:
        raise ErrorFicha(f"{F}: {n} observaciones (< {p['obs_varias_rupturas']} para dos o más rupturas)")
    tipos = ["nivel", "pendiente", "varianza"] if p["tipo_cambio"] == "auto" else [p["tipo_cambio"]]
    q = {"nivel": 1, "pendiente": 2, "varianza": 1}
    yc = y - y.mean()
    escala = float(np.sum(yc * yc))
    if escala == 0:
        raise ErrorFicha(f"{F}: serie constante: no hay ruptura que medir")
    bic: dict[str, dict[str, float]] = {}
    mejor: tuple[float, str, int, list[int]] | None = None
    for tipo in tipos:
        h = max(math.ceil(p["recorte"] * n), q[tipo] + 1)
        C = _coste_segmentos(yc, tipo, h)
        bic[tipo] = {}
        for m in range(M + 1):
            if (m + 1) * h > n:
                break
            coste, rupt = _particion_optima(C, m, n)
            if not math.isfinite(coste):
                continue
            if tipo == "varianza":
                dosll, k_par = coste, (m + 1) + m + 1
            else:
                dosll, k_par = n * math.log(max(coste, EPS * escala) / n), q[tipo] * (m + 1) + m + 1
            b = dosll + k_par * math.log(n)
            bic[tipo][str(m)] = b
            if mejor is None or b < mejor[0]:
                mejor = (b, tipo, m, rupt)
    if mejor is None:
        raise ErrorFicha(f"{F}: ningún modelo admisible con el recorte {p['recorte']:g}")
    b_opt, tipo, m, rupt = mejor
    tipo_txt = tipo if m > 0 else "sin ruptura"
    # Segmentos y cambios
    limites = [0, *rupt, n]
    t = np.arange(n, dtype=float)
    segmentos = []
    for a, b in pairwise(limites):
        ys, ts = y[a:b], t[a:b]
        seg: dict[str, Any] = {"desde": a, "hasta": b - 1, "fecha_desde": _etiqueta(a, fechas),
                               "fecha_hasta": _etiqueta(b - 1, fechas), "n": b - a, "media": float(ys.mean()),
                               "desviacion": float(np.sqrt(np.mean((ys - y.mean()) ** 2))) if tipo == "varianza"
                               else float(ys.std(ddof=1))}
        if tipo == "pendiente":
            pend, ord_ = np.polyfit(ts, ys, 1)
            seg.update({"pendiente": float(pend), "ordenada": float(ord_)})
        segmentos.append(seg)
    senal = _senal(y, tipo)   # en la de pendiente, Δy_t = y_{t+1} − y_t: el régimen nuevo empieza en el mismo índice k
    c_bai = _cuantil_bai(1 - p["nivel"])
    rupturas = []
    for i, k in enumerate(rupt):
        sa, sb = segmentos[i], segmentos[i + 1]
        izq, der = senal[limites[i]:k], senal[k:limites[i + 2]]
        delta = float(der.mean() - izq.mean())
        resid = np.concatenate([izq - izq.mean(), der - der.mean()])
        s2 = float(np.sum(resid ** 2) / max(len(resid) - 2, 1))
        ic: dict[str, Any]
        if delta != 0:
            anchura = math.floor(c_bai * s2 / delta ** 2) + 1
            ic = {"inferior": max(0, k - anchura), "superior": min(n - 1, k + anchura)}
        else:
            ic = {"inferior": 0, "superior": n - 1}
        ic.update({"fecha_inferior": _etiqueta(ic["inferior"], fechas), "fecha_superior": _etiqueta(ic["superior"], fechas),
                   "confianza": 1 - p["nivel"]})
        r: dict[str, Any] = {"indice": k, "fecha": _etiqueta(k, fechas), "tipo": tipo, "ic": ic}
        if tipo == "nivel":
            r["cambio"] = {"media_antes": sa["media"], "media_despues": sb["media"], "salto": sb["media"] - sa["media"]}
        elif tipo == "pendiente":
            r["cambio"] = {"pendiente_antes": sa["pendiente"], "pendiente_despues": sb["pendiente"],
                           "cambio_pendiente": sb["pendiente"] - sa["pendiente"],
                           "salto_nivel": (sb["ordenada"] + sb["pendiente"] * k) - (sa["ordenada"] + sa["pendiente"] * k)}
        else:
            r["cambio"] = {"desviacion_antes": sa["desviacion"], "desviacion_despues": sb["desviacion"],
                           "ratio": sb["desviacion"] / sa["desviacion"] if sa["desviacion"] > 0 else None}
        rupturas.append(r)
    # Primera vía: CUSUM sobre la señal del tipo (para «sin ruptura», la de nivel)
    tipo_cusum = tipo if m > 0 else ("nivel" if p["tipo_cambio"] == "auto" else p["tipo_cambio"])
    cs = _cusum(_senal(y, tipo_cusum))
    k_cusum = cs["indice_senal"]
    cusum = {"tipo": tipo_cusum, "estadistico": cs["estadistico"], "p_valor": cs["p_valor"],
             "rechaza_sin_ruptura": cs["p_valor"] < p["nivel"], "indice": k_cusum, "fecha": _etiqueta(k_cusum or -1, fechas)}
    if rupturas and k_cusum is not None:
        cercana = min(rupturas, key=lambda r: abs(r["indice"] - k_cusum))
        coinciden = cercana["ic"]["inferior"] <= k_cusum <= cercana["ic"]["superior"] and cusum["rechaza_sin_ruptura"]
        segunda = {"indice_cusum": k_cusum, "indice_bai_perron": cercana["indice"], "coinciden": bool(coinciden)}
    else:
        segunda = {"indice_cusum": k_cusum, "indice_bai_perron": None,
                   "coinciden": not cusum["rechaza_sin_ruptura"] and not rupturas}
    if not segunda["coinciden"]:
        lim.append("CUSUM y Bai-Perron no coinciden: ruptura dudosa")
    if tipo == "pendiente" and rupturas:
        lim.append("IC de la fecha de una ruptura de pendiente por la vía de Bai (1997) sobre Δy (conservador)")
    ref_tipo = "nivel" if tipo == "varianza" else tipo
    b0 = bic.get(ref_tipo, {}).get("0", bic[tipo].get("0"))
    return {"tipo_cambio": tipo_txt, "n_rupturas": m, "rupturas": rupturas, "segmentos": segmentos,
            "bic": bic, "bic_elegido": b_opt, "cusum": cusum, "segunda_via": segunda, "n": n, "origen": origen,
            "referencia_ingenua": {"modelo": "sin ruptura", "bic": b0,
                                   "mejora_bic": (b0 - b_opt) if b0 is not None else None}}, lim


# ====================================================================== FX-STL-001
def _loess(y: np.ndarray, q: int, w_rob: np.ndarray | None, x0: np.ndarray) -> np.ndarray:
    """LOESS local lineal con pesos tricúbicos (Cleveland 1979) en las posiciones x0 de una serie equiespaciada."""
    m = len(y)
    x = np.arange(m, dtype=float)
    d = np.abs(x0[:, None] - x[None, :])
    if q <= m:
        h = np.partition(d, q - 1, axis=1)[:, q - 1]
    else:
        h = d.max(axis=1) * q / m
    h = np.maximum(h, EPS)
    u = d / h[:, None]
    w = np.where(u < 1, (1 - u ** 3) ** 3, 0.0)
    if w_rob is not None:
        wr = w * w_rob[None, :]
        vacio = wr.sum(axis=1) <= 0
        w = np.where(vacio[:, None], w, wr)
    sw = w.sum(axis=1)
    xm = (w * x).sum(axis=1) / sw
    ym = (w * y).sum(axis=1) / sw
    sxx = (w * (x - xm[:, None]) ** 2).sum(axis=1)
    sxy = (w * (x - xm[:, None]) * (y - ym[:, None])).sum(axis=1)
    pend = np.where(sxx > EPS * np.maximum(sw, EPS), sxy / np.where(sxx > 0, sxx, 1.0), 0.0)
    return ym + pend * (x0 - xm)


def _impar(x: float) -> int:
    k = math.ceil(x)
    return k if k % 2 == 1 else k + 1


def stl(y: np.ndarray, periodo: int, robusto: bool, n_s: int, bucles: list[int]) -> dict[str, np.ndarray]:
    """STL (Cleveland, Cleveland, McRae y Terpenning 1990), aditivo."""
    n, np_ = len(y), periodo
    n_l = _impar(np_)
    n_t = _impar(1.5 * np_ / (1 - 1.5 / n_s))
    n_i, n_o = bucles
    T = np.zeros(n)
    S = np.zeros(n)
    rob = np.ones(n)
    for vuelta in range(n_o + 1):
        for _ in range(n_i):
            D = y - T
            C = np.zeros(n + 2 * np_)
            for k in range(np_):
                idx = np.arange(k, n, np_)
                sub = D[idx]
                pos = np.arange(-1, len(sub) + 1, dtype=float)
                C[np.arange(k, n + 2 * np_, np_)[: len(pos)]] = _loess(sub, n_s, rob[idx], pos)
            L = np.convolve(C, np.ones(np_) / np_, "valid")
            L = np.convolve(L, np.ones(np_) / np_, "valid")
            L = np.convolve(L, np.ones(3) / 3, "valid")
            L = _loess(L, n_l, None, np.arange(n, dtype=float))
            S = C[np_: np_ + n] - L
            T = _loess(y - S, n_t, rob, np.arange(n, dtype=float))
        if vuelta < n_o:
            R = np.abs(y - T - S)
            hh = 6 * float(np.median(R))
            if hh <= 0:
                rob = np.ones(n)
                break
            u = R / hh
            rob = np.where(u < 1, (1 - u ** 2) ** 2, 0.0)
    return {"tendencia": T, "estacional": S, "resto": y - T - S, "pesos": rob}


def _estacional_mm(y: np.ndarray, periodo: int) -> np.ndarray:
    """Segunda vía: descomposición clásica por medias móviles centradas (2×p si p es par) y medias por posición."""
    if periodo % 2 == 0:
        k = np.concatenate([[0.5], np.ones(periodo - 1), [0.5]]) / periodo
    else:
        k = np.ones(periodo) / periodo
    mm = np.convolve(y, k, "valid")
    ini = (len(k) - 1) // 2
    d = y[ini: ini + len(mm)] - mm
    pos = (np.arange(ini, ini + len(mm))) % periodo
    ind = np.array([d[pos == j].mean() for j in range(periodo)])
    return ind - ind.mean()


def _periodo_por_frecuencia(fechas: list[str] | None, F: str) -> int:
    if fechas is None or len(fechas) < 3:
        raise ErrorFicha(f"{F}: falta «periodo» y no hay fechas de las que deducir la frecuencia")
    frec = _frecuencia(fechas)
    if frec is None:
        raise ErrorFicha(f"{F}: frecuencia irregular: declare «periodo»")
    base = re.sub(r"^\d+", "", frec).split("-")[0].upper()
    tabla = {"M": 12, "MS": 12, "ME": 12, "BM": 12, "BMS": 12, "BME": 12, "Q": 4, "QS": 4, "QE": 4, "BQ": 4,
             "BQS": 4, "BQE": 4, "W": 52, "B": 5, "D": 7}
    if base not in tabla or re.match(r"^\d+", frec):
        raise ErrorFicha(f"{F}: frecuencia «{frec}» sin periodo estacional definido: declare «periodo»")
    return tabla[base]


@_cerrado("FX-STL-001")
def f_fx_stl(ent: dict[str, Any], p: dict[str, Any]) -> Resultado:
    F, lim = "FX-STL-001", []
    y, fechas, origen = _univariante(ent, F)
    periodo = p["periodo"] or _periodo_por_frecuencia(fechas, F)
    n = len(y)
    ciclos = n // periodo
    if ciclos < p["ciclos_minimos"]:
        raise ErrorFicha(f"{F}: {n} observaciones = {ciclos} ciclos de {periodo} (< {p['ciclos_minimos']})")
    if ciclos < p["ciclos_recomendados"]:
        lim.append(f"{ciclos} ciclos completos (< {p['ciclos_recomendados']} recomendados): descomposición inestable")
    bucles = p["bucles_robusto"] if p["robusto"] else p["bucles_simple"]
    positiva = bool(np.all(y > 0))
    if p["esquema"] == "multiplicativo" and not positiva:
        raise ErrorFicha(f"{F}: esquema multiplicativo con valores no positivos")
    adit = stl(y, periodo, p["robusto"], p["n_s"], bucles)
    mult = stl(np.log(y), periodo, p["robusto"], p["n_s"], bucles) if positiva and p["esquema"] != "aditivo" else None
    criterio = None
    if p["esquema"] == "auto":
        if mult is None:
            esquema = "aditivo"
        else:
            rel_a = float(np.var(adit["resto"] / adit["tendencia"])) if np.all(adit["tendencia"] > 0) else math.inf
            rel_m = float(np.var(mult["resto"]))
            esquema = "multiplicativo" if rel_m < rel_a else "aditivo"
            criterio = {"varianza_relativa_resto_aditivo": rel_a if math.isfinite(rel_a) else None,
                        "varianza_resto_log": rel_m}
    else:
        esquema = p["esquema"]
    base = mult if esquema == "multiplicativo" and mult is not None else adit
    if esquema == "multiplicativo":
        T, S, R = np.exp(base["tendencia"]), np.exp(base["estacional"]), np.exp(base["resto"])
        ajustada = y / S
        error = float(np.max(np.abs(T * S * R - y) / np.abs(y)))
        escala_log = np.log(y)
    else:
        T, S, R = base["tendencia"], base["estacional"], base["resto"]
        ajustada = y - S
        error = float(np.max(np.abs(T + S + R - y)) / max(float(np.max(np.abs(y))), EPS))
        escala_log = y
    # Diagnóstico de estabilidad estacional: F de estacionalidad estable (ANOVA por posición) sobre S + R
    sr = base["estacional"] + base["resto"]
    pos = np.arange(n) % periodo
    grupos = [sr[pos == j] for j in range(periodo)]
    f_est: float | None = None
    p_est: float | None = None
    if all(len(g) >= 2 for g in grupos) and float(np.ptp(sr)) > 0:
        an = stats.f_oneway(*grupos)
        if math.isfinite(float(an.statistic)) and math.isfinite(float(an.pvalue)):
            f_est, p_est = float(an.statistic), float(an.pvalue)
    patron = np.array([base["estacional"][pos == j].mean() for j in range(periodo)])
    amplitud = float(np.ptp(patron))
    variacion = [float(np.ptp(base["estacional"][pos == j])) for j in range(periodo)]
    mm = _estacional_mm(escala_log, periodo)
    patron_c = patron - patron.mean()
    corr = float(np.corrcoef(mm, patron_c)[0, 1]) if np.ptp(mm) > 0 and np.ptp(patron_c) > 0 else None
    outliers = int(np.sum(base["pesos"] == 0)) if p["robusto"] else 0
    return {"esquema": esquema, "criterio_esquema": criterio, "periodo": periodo, "n": n, "ciclos": ciclos,
            "robusto": p["robusto"], "origen": origen, "fechas": fechas,
            "tendencia": T, "estacional": S, "resto": R, "ajustada": ajustada,
            "identidad_error_max": error,
            "diagnostico_estacional": {"F_estable": f_est, "p_valor": p_est, "amplitud_patron": amplitud,
                                       "variacion_por_posicion_max": float(max(variacion)),
                                       "patron_medio": patron, "escala": "log" if esquema == "multiplicativo" else "origen",
                                       "observaciones_con_peso_cero": outliers},
            "segunda_via": {"metodo": "medias móviles centradas", "patron_estacional": mm,
                            "diferencia_max": float(np.max(np.abs(mm - patron_c))), "correlacion": corr},
            "referencia_ingenua": "RI-EST"}, lim


# ====================================================================== motor HMM (FX-REGIME-001 y REG-HMM-001)
def _prefijos(M: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Productos prefijo P_t = M_0 ⋯ M_t (barrido de Hillis-Steele) normalizados: P_t = exp(s_t)·Q_t, ΣQ_t = 1."""
    k2 = M.shape[-1] * M.shape[-2]
    tot = M.reshape(*M.shape[:-2], k2).sum(-1)
    Q = M / tot[..., None, None]
    s = np.log(tot)
    off, n = 1, M.shape[1]
    while off < n:
        prod = Q[:, :-off] @ Q[:, off:]
        t2 = prod.reshape(*prod.shape[:-2], k2).sum(-1)
        s_n = s[:, :-off] + s[:, off:] + np.log(t2)
        prod /= t2[..., None, None]
        Q[:, off:] = prod
        s[:, off:] = s_n
        off *= 2
    return Q, s


def _log_emision(X: np.ndarray, mu: np.ndarray, cov: np.ndarray, completa: bool) -> np.ndarray:
    """log N(x_t; μ_k, Σ_k) para cada arranque r, observación t y estado k → (R, n, k)."""
    d = X.shape[1]
    dif = X[None, :, None, :] - mu[:, None, :, :]                    # (R, n, k, d)
    if completa:
        inv = np.linalg.inv(cov)                                     # (R, k, d, d)
        _, logdet = np.linalg.slogdet(cov)
        maha = np.einsum("rtki,rkij,rtkj->rtk", dif, inv, dif)
    else:
        logdet = np.log(cov).sum(-1)
        maha = (dif ** 2 / cov[:, None, :, :]).sum(-1)
    return -0.5 * (d * math.log(2 * math.pi) + logdet[:, None, :] + maha)


def _e_paso(X: np.ndarray, pi0: np.ndarray, A: np.ndarray, mu: np.ndarray, cov: np.ndarray,
            completa: bool) -> dict[str, np.ndarray]:
    """Filtro de Hamilton y suavizado (Kim) por productos de matrices: filtradas, suavizadas, ξ y log-verosimilitud."""
    logB = _log_emision(X, mu, cov, completa)
    mB = logB.max(-1)
    B = np.exp(logB - mB[..., None])
    v1 = pi0 * B[:, 0]
    R, n, k = B.shape
    sv = v1.sum(-1)
    v1n = v1 / sv[:, None]
    filtradas = np.empty((R, n, k))
    filtradas[:, 0] = v1n
    loglik = np.log(sv) + mB.sum(-1)
    if n > 1:
        M = A[:, None, :, :] * B[:, 1:, None, :]                     # M_t = A·diag(B_t), t = 1..n−1
        Q, s = _prefijos(M)
        a = np.einsum("ri,rtij->rtj", v1n, Q)
        sa = a.sum(-1)
        filtradas[:, 1:] = a / sa[..., None]
        loglik = loglik + s[:, -1] + np.log(sa[:, -1])
        Mt = np.swapaxes(M[:, ::-1], -1, -2)                          # sufijos: (M_{t+1} ⋯ M_{n−1})ᵀ
        Qs, _ = _prefijos(Mt)
        beta = np.ones((R, n, k))
        beta[:, :-1] = Qs.sum(-2)[:, ::-1]                            # β̃_t ∝ M_{t+1} ⋯ M_{n−1}·1
        beta = beta / beta.sum(-1, keepdims=True)
        xi = filtradas[:, :-1, :, None] * M * beta[:, 1:, None, :]
        xi = xi / xi.reshape(R, n - 1, k * k).sum(-1)[..., None, None]
    else:
        beta = np.ones((R, n, k))
        xi = np.zeros((R, 0, k, k))
    g = filtradas * beta
    g = g / g.sum(-1, keepdims=True)
    return {"filtradas": filtradas, "suavizadas": g, "xi": xi, "loglik": loglik}


def _m_paso(X: np.ndarray, e: dict[str, np.ndarray], mu: np.ndarray, cov: np.ndarray, completa: bool,
            medias_libres: bool, varianzas_libres: bool, suelo: np.ndarray) -> tuple[np.ndarray, ...]:
    g, xi = e["suavizadas"], e["xi"]
    n, k = g.shape[1], g.shape[2]
    pi0 = g[:, 0]
    cuenta = xi.sum(1)
    filas = cuenta.sum(-1, keepdims=True)
    A = np.where(filas > 0, cuenta / np.where(filas > 0, filas, 1.0), 1.0 / k)
    Nk = g.sum(1)                                                     # (R, k)
    hay = Nk > EPS * n
    Nk_s = np.where(hay, Nk, 1.0)
    Sx = np.einsum("rtk,td->rkd", g, X)
    if medias_libres:
        mu_n = np.where(hay[..., None], Sx / Nk_s[..., None], mu)
    else:   # media común con varianzas distintas (univariante): μ = Σ_k (Σ_t γ x)/σ²_k / Σ_k N_k/σ²_k
        var = cov if not completa else np.diagonal(cov, axis1=-2, axis2=-1)
        num = (Sx / var).sum(1)
        den = (Nk[..., None] / var).sum(1)
        mu_n = np.repeat((num / den)[:, None, :], k, axis=1)
    dif = X[None, :, None, :] - mu_n[:, None, :, :]
    if completa:
        Sk = np.einsum("rtk,rtki,rtkj->rkij", g, dif, dif)
        if varianzas_libres:
            cov_n = np.where(hay[..., None, None], Sk / Nk_s[..., None, None], cov)
        else:
            cov_n = np.repeat((Sk.sum(1) / n)[:, None], k, axis=1)
        cov_n = cov_n + np.diag(suelo)[None, None]
    else:
        Sk = np.einsum("rtk,rtkd->rkd", g, dif ** 2)
        if varianzas_libres:
            cov_n = np.where(hay[..., None], Sk / Nk_s[..., None], cov)
        else:
            cov_n = np.repeat((Sk.sum(1) / n)[:, None], k, axis=1)
        cov_n = np.maximum(cov_n, suelo[None, None, :])
    return pi0, A, mu_n, cov_n


def _inicio(X: np.ndarray, k: int, R: int, rng: np.random.Generator, completa: bool, medias_libres: bool,
            varianzas_libres: bool, suelo: np.ndarray) -> tuple[np.ndarray, ...]:
    """Arranques aleatorios: estados por cuantiles aleatorios de una proyección aleatoria de los datos (o de |x − mediana|
    si solo cambian las varianzas); un paso M desde esa asignación da los parámetros iniciales."""
    n, d = X.shape
    g = np.zeros((R, n, k))
    for r in range(R):
        if medias_libres:
            w = rng.standard_normal(d)
            f = X @ (w / np.linalg.norm(w))
        else:
            f = np.abs(X - np.median(X, axis=0)).sum(1)
        cortes = np.quantile(f, np.sort(rng.uniform(size=k - 1)))
        z = np.searchsorted(cortes, f)
        g[r, np.arange(n), z] = 1.0
    xi = g[:, :-1, :, None] * g[:, 1:, None, :]
    mu0 = np.repeat(X.mean(0)[None, None], R, 0).repeat(k, 1)
    var0 = X.var(0) + suelo
    cov0 = (np.repeat(np.diag(var0)[None, None], R, 0).repeat(k, 1) if completa
            else np.repeat(var0[None, None], R, 0).repeat(k, 1))
    return _m_paso(X, {"suavizadas": g, "xi": xi}, mu0, cov0, completa, medias_libres, varianzas_libres, suelo)


def _vector_parametros(A: np.ndarray, mu: np.ndarray, cov: np.ndarray) -> np.ndarray:
    R = A.shape[0]
    return np.concatenate([A.reshape(R, -1), mu.reshape(R, -1), cov.reshape(R, -1)], axis=1)


def ajustar_hmm(X: np.ndarray, k: int, semilla: int, arranques: int, tol: float, iter_max: int, completa: bool = False,
                medias_libres: bool = True, varianzas_libres: bool = True) -> dict[str, Any]:
    """EM de Baum-Welch con varios arranques; converge cuando el cambio máximo de los parámetros es < tol·1e-2·(1 + |θ|)
    (INC-T112-01). Devuelve el mejor arranque convergido por log-verosimilitud."""
    rng = np.random.default_rng(semilla)
    suelo = tol * X.var(0)
    pi0, A, mu, cov = _inicio(X, k, arranques, rng, completa, medias_libres, varianzas_libres, suelo)
    activos = np.arange(arranques)
    convergido = np.zeros(arranques, dtype=bool)
    fin = {"pi0": pi0.copy(), "A": A.copy(), "mu": mu.copy(), "cov": cov.copy(), "loglik": np.full(arranques, -np.inf)}
    iteraciones = np.zeros(arranques, dtype=int)
    for _ in range(iter_max):
        e = _e_paso(X, pi0, A, mu, cov, completa)
        nuevo = _m_paso(X, e, mu, cov, completa, medias_libres, varianzas_libres, suelo)
        viejo_v, nuevo_v = _vector_parametros(A, mu, cov), _vector_parametros(nuevo[1], nuevo[2], nuevo[3])
        cambio = np.max(np.abs(nuevo_v - viejo_v) / (1 + np.abs(viejo_v)), axis=1)
        pi0, A, mu, cov = nuevo
        iteraciones[activos] += 1
        listo = cambio < tol * FACTOR_CONVERGENCIA
        for nombre, val in (("pi0", pi0), ("A", A), ("mu", mu), ("cov", cov)):
            fin[nombre][activos] = val
        if listo.any():
            convergido[activos[listo]] = True
            seguir = ~listo
            activos = activos[seguir]
            pi0, A, mu, cov = pi0[seguir], A[seguir], mu[seguir], cov[seguir]
        if len(activos) == 0:
            break
    e = _e_paso(X, fin["pi0"], fin["A"], fin["mu"], fin["cov"], completa)
    ll = np.where(convergido, e["loglik"], -np.inf)
    if not convergido.any() or not np.isfinite(ll).any():
        raise ErrorFicha(f"CONVERGENCIA: ningún arranque del EM converge en {iter_max} iteraciones")
    b = int(np.argmax(ll))
    return {"pi0": fin["pi0"][b], "A": fin["A"][b], "mu": fin["mu"][b], "cov": fin["cov"][b], "loglik": float(ll[b]),
            "filtradas": e["filtradas"][b], "suavizadas": e["suavizadas"][b], "iteraciones": int(iteraciones[b]),
            "arranques_convergidos": int(convergido.sum()), "arranques": arranques}


def _ordenar(aj: dict[str, Any], clave: np.ndarray) -> dict[str, Any]:
    o = np.argsort(clave, kind="stable")
    aj = dict(aj)
    aj["A"] = aj["A"][np.ix_(o, o)]
    for c in ("pi0",):
        aj[c] = aj[c][o]
    for c in ("mu", "cov"):
        aj[c] = aj[c][o]
    for c in ("filtradas", "suavizadas"):
        aj[c] = aj[c][:, o]
    return aj


def _estacionaria(A: np.ndarray) -> np.ndarray:
    k = A.shape[0]
    sistema = np.vstack([A.T - np.eye(k), np.ones((1, k))])
    pi = np.linalg.lstsq(sistema, np.concatenate([np.zeros(k), [1.0]]), rcond=None)[0]
    pi = np.clip(pi, 0, None)
    return pi / pi.sum()


def _duraciones(A: np.ndarray, lim: list[str]) -> list[float | None]:
    out: list[float | None] = []
    for i in range(A.shape[0]):
        if A[i, i] >= 1:
            out.append(None)
            lim.append(f"estado {i + 1} absorbente: duración esperada infinita (None)")
        else:
            out.append(float(1 / (1 - A[i, i])))
    return out


def hamilton_filtro(x: np.ndarray, pi0: np.ndarray, A: np.ndarray, medias: np.ndarray,
                    desviaciones: np.ndarray) -> tuple[np.ndarray, float]:
    """Filtro de Hamilton paso a paso (univariante), para verificación: (filtradas, log-verosimilitud)."""
    n, k = len(x), len(pi0)
    filt = np.empty((n, k))
    ll = 0.0
    pred = pi0.copy()
    for t in range(n):
        dens = stats.norm.pdf(x[t], medias, desviaciones)
        a = pred * dens
        c = a.sum()
        ll += math.log(c)
        filt[t] = a / c
        pred = filt[t] @ A
    return filt, ll


@_cerrado("FX-REGIME-001")
def f_fx_regime(ent: dict[str, Any], p: dict[str, Any]) -> Resultado:
    F, lim = "FX-REGIME-001", []
    y, fechas, origen = _univariante(ent, F, rendimientos=True)
    n, k = len(y), p["n_estados"]
    if n < p["obs_minimas"]:
        raise ErrorFicha(f"{F}: {n} observaciones (< {p['obs_minimas']})")
    if n < p["obs_recomendadas"]:
        lim.append(f"{n} observaciones (< {p['obs_recomendadas']} recomendadas): regímenes posiblemente artefactos")
    if float(np.ptp(y)) == 0:
        raise ErrorFicha(f"{F}: serie constante: no hay regímenes")
    X = y[:, None]

    def ajuste(semilla: int) -> dict[str, Any]:
        aj = ajustar_hmm(X, k, semilla, p["arranques"], p["tolerancia"], p["iteraciones_max"], False,
                         p["medias_distintas"], p["varianzas_distintas"])
        clave = aj["cov"][:, 0] if p["varianzas_distintas"] else aj["mu"][:, 0]
        return _ordenar(aj, clave)

    aj = ajuste(p["semilla"])
    aj2 = ajuste(p["semilla"] + 1)
    n_par = (k - 1) + k * (k - 1) + (k if p["medias_distintas"] else 1) + (k if p["varianzas_distintas"] else 1)
    bic = -2 * aj["loglik"] + n_par * math.log(n)
    bic1 = -2 * float(np.sum(stats.norm.logpdf(y, y.mean(), y.std()))) + 2 * math.log(n)
    filt = aj["filtradas"]
    ultimo = filt[-1]
    k_max = int(np.argmax(ultimo))
    actual = f"estado_{k_max + 1}" if ultimo[k_max] >= p["umbral"] else "indeterminado"
    if bic >= bic1:
        lim.append("el modelo de un solo régimen tiene mejor BIC: los regímenes no se sostienen")
    dif_par = float(np.max(np.abs(_vector_parametros(aj["A"][None], aj["mu"][None], aj["cov"][None])
                                  - _vector_parametros(aj2["A"][None], aj2["mu"][None], aj2["cov"][None]))))
    coincide = abs(aj["loglik"] - aj2["loglik"]) <= p["tolerancia"] * (1 + abs(aj["loglik"]))
    if not coincide:
        lim.append("la segunda semilla llega a otro óptimo: regímenes inestables")
    estados = [{"estado": f"estado_{i + 1}", "media": float(aj["mu"][i, 0]), "desviacion": float(math.sqrt(aj["cov"][i, 0])),
                "probabilidad_inicial": float(aj["pi0"][i])} for i in range(k)]
    return {"n_estados": k, "n": n, "origen": origen, "estados": estados, "matriz_transicion": aj["A"],
            "duraciones_esperadas": _duraciones(aj["A"], lim), "distribucion_estacionaria": _estacionaria(aj["A"]),
            "probabilidades_filtradas_actuales": {f"estado_{i + 1}": float(ultimo[i]) for i in range(k)},
            "regimen_actual": actual, "umbral": p["umbral"],
            "serie": {"fechas": fechas, "filtradas": filt, "suavizadas_solo_descriptivas": aj["suavizadas"]},
            "loglik": aj["loglik"], "bic": bic, "iteraciones": aj["iteraciones"],
            "arranques_convergidos": aj["arranques_convergidos"], "arranques": aj["arranques"], "semilla": p["semilla"],
            "etiquetado": "por varianza creciente" if p["varianzas_distintas"] else "por media creciente",
            "segunda_via": {"semilla": p["semilla"] + 1, "loglik": aj2["loglik"], "diferencia_max_parametros": dif_par,
                            "coincide": bool(coincide)},
            "referencia_ingenua": {"modelo": "un solo régimen", "bic": bic1, "mejora_bic": bic1 - bic}}, lim


@_cerrado("REG-HMM-001")
def f_reg_hmm(ent: dict[str, Any], p: dict[str, Any]) -> Resultado:
    F, lim = "REG-HMM-001", []
    v = _dict(ent["valores"], f"{F}: valores")
    variables = _dict(v.get("variables"), f"{F}: «variables» (nombre → lista)") if v.get("variables") is not None else None
    if not variables:
        raise ErrorFicha(f"{F}: faltan «variables» (nombre → serie de datos de entrenamiento)")
    nombres = sorted(variables)
    cols = [_vector(variables[c], f"{F}: variable «{c}»") for c in nombres]
    n = len(cols[0])
    if any(len(c) != n for c in cols):
        raise ErrorFicha(f"{F}: las variables tienen longitudes distintas")
    fechas = _fechas(v.get("fechas"), n, f"{F}: fechas")
    frec = v.get("frecuencia")
    if fechas is not None and len(fechas) >= 3:
        inf = _frecuencia(fechas)
        base = inf.split("-")[0] if inf and not re.match(r"^\d", inf) else ""
        deducida = "semanal" if base == "W" else ("mensual" if base in ("M", "MS", "ME", "BM", "BMS", "BME") else None)
        if frec is not None and deducida is not None and frec != deducida:
            raise ErrorFicha(f"{F}: frecuencia declarada «{frec}» y deducida de las fechas «{deducida}» no coinciden")
        frec = frec or deducida
    if frec not in p["obs_minimas"]:
        raise ErrorFicha(f"{F}: frecuencia «{frec}» no admitida: datos semanales o mensuales (declare «frecuencia»)")
    if n < p["obs_minimas"][frec]:
        raise ErrorFicha(f"{F}: {n} observaciones {frec}es (< {p['obs_minimas'][frec]})")
    X = np.column_stack(cols)
    media, sd = X.mean(0), X.std(0, ddof=1)
    if np.any(sd == 0):
        raise ErrorFicha(f"{F}: variable constante: no se puede estandarizar")
    Z = (X - media) / sd
    completa = p["covarianza"] == "completa"
    d = Z.shape[1]
    ks = list(range(p["rango_n_estados"][0], p["rango_n_estados"][1] + 1)) if p["n_estados"] == "BIC" else [p["n_estados"]]

    def ajuste(k: int, semilla: int) -> dict[str, Any]:
        aj = ajustar_hmm(Z, k, semilla, p["arranques"], p["tolerancia"], p["iteraciones_max"], completa)
        return _ordenar(aj, aj["mu"][:, 0])

    def n_par(k: int) -> int:
        return (k - 1) + k * (k - 1) + k * d + (k * d * (d + 1) // 2 if completa else k * d)

    ajustes, bics = {}, {}
    for k in ks:
        try:
            ajustes[k] = ajuste(k, p["semilla"])
        except ErrorFicha as e:
            lim.append(f"{k} estados: {e}")
            continue
        bics[k] = -2 * ajustes[k]["loglik"] + n_par(k) * math.log(n)
    if not bics:
        raise ErrorFicha(f"{F}: CONVERGENCIA: ningún número de estados converge")
    k = min(bics, key=lambda x: (bics[x], x))
    aj = ajustes[k]
    aj2 = ajuste(k, p["semilla"] + 1)
    filt = aj["filtradas"]
    ultimo = filt[-1]
    coincide = abs(aj["loglik"] - aj2["loglik"]) <= p["tolerancia"] * (1 + abs(aj["loglik"]))
    if not coincide:
        lim.append("la segunda semilla llega a otro óptimo: regímenes inestables")
    if frec and fechas is None:
        lim.append("sin fechas: frecuencia declarada, no comprobada")
    lim.append("estandarización con la ventana de entrenamiento completa: la serie histórica de filtradas no es "
               "estrictamente en tiempo real")
    medias = aj["mu"] * sd + media
    estados = []
    for i in range(k):
        estados.append({"estado": f"estado_{i + 1}",
                        "etiqueta": f"media de «{nombres[0]}» {'más baja' if i == 0 else ('más alta' if i == k - 1 else 'intermedia')}",
                        "medias": {c: float(medias[i, j]) for j, c in enumerate(nombres)},
                        "medias_estandarizadas": {c: float(aj["mu"][i, j]) for j, c in enumerate(nombres)},
                        "covarianza_estandarizada": aj["cov"][i], "probabilidad_inicial": float(aj["pi0"][i])})
    pi_inc = _estacionaria(aj["A"])
    anterior = int(np.argmax(filt[-2])) if len(filt) > 1 else None
    return {"n_estados": k, "criterio": "BIC" if p["n_estados"] == "BIC" else "declarado",
            "bic": {str(x): b for x, b in bics.items()}, "covarianza": p["covarianza"], "variables": nombres,
            "frecuencia": frec, "n": n, "estados": estados, "matriz_transicion": aj["A"],
            "duraciones_esperadas": _duraciones(aj["A"], lim),
            "probabilidades_filtradas_actuales": {f"estado_{i + 1}": float(ultimo[i]) for i in range(k)},
            "serie_filtradas": {"fechas": fechas, "probabilidades": filt}, "loglik": aj["loglik"],
            "arranques": aj["arranques"], "arranques_convergidos": aj["arranques_convergidos"], "semilla": p["semilla"],
            "segunda_via": {"semilla": p["semilla"] + 1, "loglik": aj2["loglik"], "coincide": bool(coincide),
                            "diferencia_max_medias": float(np.max(np.abs(aj["mu"] - aj2["mu"])))},
            "referencia_ingenua": {"regimen_observacion_anterior": None if anterior is None else f"estado_{anterior + 1}",
                                   "incondicional": {f"estado_{i + 1}": float(pi_inc[i]) for i in range(k)}}}, lim


# ====================================================================== FX-COINT-001
# INC-T112-01 [PROPUESTO]: valores críticos asintóticos a 0,01 / 0,05 / 0,10.
# ADF con constante (N = 1) y Engle-Granger con constante en la regresión de cointegración (N = 2..5): MacKinnon (2010),
# «Critical Values for Cointegration Tests», tabla 2, término τ∞.
_CRIT_TAU = {1: (-3.43035, -2.86154, -2.56677), 2: (-3.89644, -3.33613, -3.04445), 3: (-4.29374, -3.74066, -3.45218),
             4: (-4.64332, -4.09600, -3.81020), 5: (-4.95756, -4.41519, -4.13157)}
# Traza de Johansen, caso 2 (constante restringida al vector, sin tendencia en los datos), por número de relaciones
# comunes q − r = 1..5: MacKinnon, Haug y Michelis (1999).
_CRIT_TRAZA = {1: (12.7676, 9.1645, 7.5567), 2: (24.9978, 20.2618, 17.9804), 3: (41.1950, 35.1928, 32.2684),
               4: (61.2676, 54.0790, 50.5245), 5: (85.3365, 76.9725, 72.7559)}


def _critico(tabla: dict[int, tuple[float, float, float]], N: int, nivel: float) -> float:
    return tabla[N][[0.01, 0.05, 0.10].index(nivel)]


def rezagos_regla(T: int) -> int:
    """Rezago máximo: ⌊4·(T/100)^{2/9}⌋, la regla de ACC-FACT-001 (Newey-West)."""
    return math.floor(4 * (T / 100) ** (2 / 9))


def _mco(y: np.ndarray, X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(coeficientes, errores estándar, residuos)."""
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    gl = len(y) - X.shape[1]
    if gl <= 0:
        raise ErrorFicha("regresión sin grados de libertad")
    s2 = float(e @ e) / gl
    cov = s2 * np.linalg.pinv(X.T @ X)
    return b, np.sqrt(np.maximum(np.diag(cov), 0.0)), e


def adf(y: np.ndarray, constante: bool, max_rez: int) -> dict[str, Any]:
    """ADF: Δy_t = [c] + ρ·y_{t−1} + Σ_{i≤p} φ_i·Δy_{t−i}; p por AIC en la muestra común (0..max_rez); τ = ρ/ee(ρ)."""
    dy = np.diff(y)
    n = len(dy)

    def diseno(p_: int, desde: int) -> tuple[np.ndarray, np.ndarray]:
        filas = np.arange(desde, n)
        cols = [y[filas]] + [dy[filas - i] for i in range(1, p_ + 1)]
        if constante:
            cols.append(np.ones(len(filas)))
        return dy[filas], np.column_stack(cols)

    aic = {}
    for p_ in range(max_rez + 1):
        yy, X = diseno(p_, max_rez)
        _, _, e = _mco(yy, X)
        aic[p_] = len(yy) * math.log(max(float(e @ e), EPS) / len(yy)) + 2 * X.shape[1]
    p_ = min(aic, key=lambda x: (aic[x], x))
    yy, X = diseno(p_, p_)
    b, ee, _ = _mco(yy, X)
    if ee[0] == 0:
        raise ErrorFicha("ADF: error estándar nulo (serie determinista)")
    return {"tau": float(b[0] / ee[0]), "rezagos": p_, "n": len(yy)}


def johansen(Y: np.ndarray, k_dif: int) -> dict[str, Any]:
    """Johansen (1991), caso 2: ΔY_t = α(β'Y_{t−1} + ρ₀) + Σ Γ_i ΔY_{t−i} + ε. Autovalores de S₁₀S₀₀⁻¹S₀₁ frente a S₁₁."""
    q = Y.shape[1]
    dY = np.diff(Y, axis=0)
    filas = np.arange(k_dif, len(dY))
    Z0 = dY[filas]
    Z1 = np.column_stack([Y[filas], np.ones(len(filas))])
    if k_dif > 0:
        Z2 = np.column_stack([dY[filas - i] for i in range(1, k_dif + 1)])
        R0 = Z0 - Z2 @ np.linalg.lstsq(Z2, Z0, rcond=None)[0]
        R1 = Z1 - Z2 @ np.linalg.lstsq(Z2, Z1, rcond=None)[0]
    else:
        R0, R1 = Z0, Z1
    T = len(filas)
    S00, S11, S01 = R0.T @ R0 / T, R1.T @ R1 / T, R0.T @ R1 / T
    lam, V = linalg.eigh(S01.T @ np.linalg.solve(S00, S01), S11)
    orden = np.argsort(lam)[::-1]
    lam, V = np.clip(lam[orden][:q], 0.0, 1 - EPS), V[:, orden][:, :q]
    traza = [float(-T * np.sum(np.log(1 - lam[r:]))) for r in range(q)]
    beta = V[:, 0]
    alfa = S01 @ beta
    return {"autovalores": lam, "traza": traza, "beta": beta, "alfa": alfa, "T": T, "R0": R0, "R1": R1}


def _orden_var(Y: np.ndarray, p_max: int) -> int:
    """Orden del VAR en niveles (1..p_max + 1) por AIC en la muestra común: ln det Σ̂ + 2·p·q²/T."""
    T_, q = Y.shape
    p_max = p_max + 1
    aic = {}
    for p_ in range(1, p_max + 1):
        filas = np.arange(p_max, T_)
        if len(filas) <= 1 + p_ * q:      # sin grados de libertad para estimar Σ̂
            break
        X = np.column_stack([np.ones(len(filas))] + [Y[filas - i] for i in range(1, p_ + 1)])
        E = Y[filas] - X @ np.linalg.lstsq(X, Y[filas], rcond=None)[0]
        _, logdet = np.linalg.slogdet(E.T @ E / len(filas))
        aic[p_] = logdet + 2 * p_ * q * q / len(filas)
    return min(aic, key=lambda x: (aic[x], x))


def _vida_media(z: np.ndarray, lim: list[str]) -> dict[str, Any]:
    """AR(1) de la desviación: Δz_t = a + φ·z_{t−1}; ρ = 1 + φ; vida media = ln(1/2)/ln(ρ) si 0 < ρ < 1."""
    b, _, _ = _mco(np.diff(z), np.column_stack([np.ones(len(z) - 1), z[:-1]]))
    rho = 1 + float(b[1])
    if 0 < rho < 1:
        return {"rho": rho, "vida_media_periodos": math.log(0.5) / math.log(rho)}
    lim.append(f"la desviación no revierte (ρ = {rho:.4g}): vida media no definida (None)")
    return {"rho": rho, "vida_media_periodos": None}


def engle_granger(Y: np.ndarray, max_rez: int, nivel: float) -> dict[str, Any]:
    T_, q = Y.shape
    X = np.column_stack([np.ones(T_), Y[:, 1:]])
    b, _, z = _mco(Y[:, 0], X)
    prueba = adf(z, False, max_rez)
    crit = _critico(_CRIT_TAU, q, nivel)
    # MCE de la primera variable: Δy₁_t = c + γ·z_{t−1} + Σ δ_j·Δx_{j,t} + ε
    dY = np.diff(Y, axis=0)
    Xm = np.column_stack([np.ones(T_ - 1), z[:-1], dY[:, 1:]])
    bm, eem, em = _mco(dY[:, 0], Xm)
    return {"vector": np.concatenate([[1.0], -b[1:]]), "constante": float(-b[0]), "residuos": z,
            "adf_residuos": {**prueba, "critico": crit, "rechaza": prueba["tau"] < crit},
            "mce": {"velocidad": float(bm[1]), "ee_velocidad": float(eem[1]), "constante": float(bm[0]),
                    "residuos_media": float(em.mean())}}


@_cerrado("FX-COINT-001")
def f_fx_coint(ent: dict[str, Any], p: dict[str, Any]) -> Resultado:
    F, lim = "FX-COINT-001", []
    v = _dict(ent["valores"], f"{F}: valores")
    fechas: list[str] | None
    if v.get("series") is not None:
        d = _dict(v["series"], f"{F}: series")
        nombres = list(d)
        if len(nombres) < 2:
            raise ErrorFicha(f"{F}: se necesitan al menos dos series")
        cols = [_vector(d[c], f"{F}: serie «{c}»") for c in nombres]
        if len({len(c) for c in cols}) != 1:
            raise ErrorFicha(f"{F}: las series en línea deben tener la misma longitud (observaciones comunes)")
        Y = np.column_stack(cols)
        fechas = _fechas(v.get("fechas"), len(cols[0]), f"{F}: fechas")
    elif ent["series"]:
        nombres = list(ent["series"])
        for c in nombres:
            _serie_ht01(ent["series"][c], f"{F}: serie «{c}»")
        df = pd.concat([ent["series"][c].rename(c) for c in nombres], axis=1, join="inner").sort_index()
        Y = df.to_numpy(dtype=float)
        fechas = [i.date().isoformat() for i in df.index]
    else:
        raise ErrorFicha(f"{F}: faltan las «series» (al menos dos)")
    if len(nombres) < 2:
        raise ErrorFicha(f"{F}: se necesitan al menos dos series")
    if len(set(map(str, nombres))) != len(nombres):
        raise ErrorFicha(f"{F}: nombres de serie repetidos")
    if len(nombres) > p["series_maximas"]:
        raise ErrorFicha(f"{F}: {len(nombres)} series (> {p['series_maximas']}, límite de las tablas de valores críticos)")
    T_, q = Y.shape
    if T_ < p["obs_minimas"]:
        raise ErrorFicha(f"{F}: {T_} observaciones comunes (< {p['obs_minimas']})")
    if np.any(np.ptp(Y, axis=0) == 0):
        raise ErrorFicha(f"{F}: serie constante")
    max_rez = rezagos_regla(T_) if p["max_rezagos"] == "AIC" else p["max_rezagos"]
    nivel = p["nivel"]
    integ = {}
    for j, c in enumerate(nombres):
        a0 = adf(Y[:, j], True, max_rez)
        a1 = adf(np.diff(Y[:, j]), True, max_rez)
        cr = _critico(_CRIT_TAU, 1, nivel)
        orden = "I(0)" if a0["tau"] < cr else ("I(1)" if a1["tau"] < cr else "I(2) o superior")
        integ[str(c)] = {"adf_nivel": {**a0, "critico": cr, "rechaza": a0["tau"] < cr},
                         "adf_diferencia": {**a1, "critico": cr, "rechaza": a1["tau"] < cr}, "orden": orden}
    no_i1 = [c for c, x in integ.items() if x["orden"] != "I(1)"]
    if no_i1:
        lim.append(f"series que no son I(1): {', '.join(no_i1)}; la cointegración presupone I(1)")
    p_var = _orden_var(Y, max_rez)
    jo = johansen(Y, p_var - 1)
    tabla = []
    rango = q
    for r in range(q):
        cr = _critico(_CRIT_TRAZA, q - r, nivel)
        rechaza = jo["traza"][r] > cr
        tabla.append({"r": r, "estadistico": jo["traza"][r], "critico": cr, "rechaza": rechaza})
        if not rechaza and rango == q:
            rango = r
    if rango == q:
        lim.append("la traza rechaza todo rango < q: sistema estacionario (no es cointegración entre I(1))")
    b0 = jo["beta"][0]
    if abs(b0) < EPS:
        raise ErrorFicha(f"{F}: el vector de Johansen no se puede normalizar en la primera serie")
    beta_n, alfa_n = jo["beta"] / b0, jo["alfa"] * b0
    eg = engle_granger(Y, max_rez, nivel)
    z_jo = np.column_stack([Y, np.ones(T_)]) @ beta_n
    coint_jo, coint_eg = rango >= 1, bool(eg["adf_residuos"]["rechaza"])
    if p["metodo"] == "Johansen":
        principal = {"metodo": "Johansen", "cointegracion": coint_jo,
                     "vector_normalizado": {**{str(c): float(beta_n[j]) for j, c in enumerate(nombres)},
                                            "constante": float(beta_n[-1])},
                     "velocidad_ajuste": {str(c): float(alfa_n[j]) for j, c in enumerate(nombres)}}
        z = z_jo
    else:
        principal = {"metodo": "Engle-Granger", "cointegracion": coint_eg,
                     "vector_normalizado": {**{str(c): float(eg["vector"][j]) for j, c in enumerate(nombres)},
                                            "constante": eg["constante"]},
                     "velocidad_ajuste": {str(nombres[0]): eg["mce"]["velocidad"]}}
        z = eg["residuos"]
    vm = _vida_media(z, lim)
    dif_vec = float(np.max(np.abs(beta_n[:q] - eg["vector"])))
    return {"metodo": p["metodo"], "n": T_, "series": [str(c) for c in nombres], "nivel": nivel,
            "rezago_maximo": max_rez, "integracion": integ, **principal, **vm,
            "johansen": {"orden_var": p_var, "autovalores": jo["autovalores"], "traza": tabla, "rango": rango},
            "engle_granger": {"vector": eg["vector"], "constante": eg["constante"], "adf_residuos": eg["adf_residuos"],
                              "mce": eg["mce"]},
            "desviacion_equilibrio": {"fechas": fechas, "valores": z},
            "verificacion": {"media_residuos_eg": float(eg["residuos"].mean()),
                             "media_residuos_mce": eg["mce"]["residuos_media"],
                             "escala": float(np.std(eg["residuos"]))},
            "segunda_via": {"metodo": "Engle-Granger" if p["metodo"] == "Johansen" else "Johansen",
                            "coinciden_en_cointegracion": coint_jo == coint_eg,
                            "diferencia_max_vectores": dif_vec},
            "referencia_ingenua": "RI-PA (sin relación)"}, lim


# ====================================================================== BIB-MET-001
def _titulo_normalizado(t: str) -> str:
    t = unicodedata.normalize("NFKD", t)
    t = "".join(ch for ch in t if not unicodedata.combining(ch)).lower()
    return " ".join(re.sub(r"[^0-9a-z]+", " ", t).split())


def _periodo(f: date, granularidad: str) -> str:
    if granularidad == "mensual":
        return f"{f.year:04d}-{f.month:02d}"
    if granularidad == "trimestral":
        return f"{f.year:04d}-T{(f.month - 1) // 3 + 1}"
    return f"{f.year:04d}"


def _periodos_entre(a: date, b: date, granularidad: str) -> list[str]:
    paso = {"mensual": 1, "trimestral": 3, "anual": 12}[granularidad]
    out, y, m = [], a.year, a.month - (a.month - 1) % paso
    while (y, m) <= (b.year, b.month):
        out.append(_periodo(date(y, m, 1), granularidad))
        m += paso
        if m > 12:
            y, m = y + 1, m - 12
    return out


@_cerrado("BIB-MET-001")
def f_bib_met(ent: dict[str, Any], p: dict[str, Any]) -> Resultado:
    F, lim = "BIB-MET-001", []
    v = _dict(ent["valores"], f"{F}: valores")
    fichas = _lista(v.get("fichas"), f"{F}: fichas") if v.get("fichas") is not None else []
    if not fichas:
        raise ErrorFicha(f"{F}: conjunto de fichas vacío")
    registros = []
    for i, fi in enumerate(fichas):
        if not isinstance(fi, dict):
            raise ErrorFicha(f"{F}: conjunto corrupto (ficha {i} no es un objeto)")
        faltan = [c for c in ("fecha", "tematica", "fuente") if not (isinstance(fi.get(c), str) and fi[c].strip())]
        if faltan:
            raise ErrorFicha(f"{F}: conjunto corrupto (ficha {i} sin {', '.join(faltan)})")
        for c in ("id", "titulo", "hash"):
            if fi.get(c) is not None and not isinstance(fi[c], str):
                raise ErrorFicha(f"{F}: conjunto corrupto (ficha {i}: «{c}» no es texto)")
        registros.append({"i": i, "id": fi.get("id") or f"#{i}", "fecha": _fecha(fi["fecha"], f"{F}: ficha {i}"),
                          "tematica": fi["tematica"].strip(), "fuente": fi["fuente"].strip(),
                          "titulo": _titulo_normalizado(fi["titulo"]) if fi.get("titulo") else None,
                          "hash": str(fi["hash"]).strip().lower() if fi.get("hash") else None})
    if len({r["id"] for r in registros}) != len(registros):
        raise ErrorFicha(f"{F}: conjunto corrupto (identificadores repetidos)")
    if p["categorias"] != "todas":
        registros = [r for r in registros if r["tematica"] in p["categorias"]]
        if not registros:
            raise ErrorFicha(f"{F}: ninguna ficha en las categorías pedidas")
    total = len(registros)
    gran = p["granularidad"]
    periodos = _periodos_entre(min(r["fecha"] for r in registros), max(r["fecha"] for r in registros), gran)
    por_periodo = dict.fromkeys(periodos, 0)
    por_tematica: dict[str, int] = {}
    por_fuente: dict[str, int] = {}
    cruce: dict[str, dict[str, int]] = {}
    for r in registros:
        per = _periodo(r["fecha"], gran)
        por_periodo[per] += 1
        por_tematica[r["tematica"]] = por_tematica.get(r["tematica"], 0) + 1
        por_fuente[r["fuente"]] = por_fuente.get(r["fuente"], 0) + 1
        cruce.setdefault(r["tematica"], dict.fromkeys(periodos, 0))[per] += 1
    cuotas = np.array([c / total for c in por_fuente.values()])
    hhi = float(np.sum(cuotas ** 2))
    # Duplicados: misma huella o mismo título normalizado (componentes conexas)
    padre = list(range(total))

    def raiz(a: int) -> int:
        while padre[a] != a:
            padre[a] = padre[padre[a]]
            a = padre[a]
        return a

    for clave in ("hash", "titulo"):
        visto: dict[str, int] = {}
        for j, r in enumerate(registros):
            if r[clave]:
                if r[clave] in visto:
                    padre[raiz(j)] = raiz(visto[r[clave]])
                else:
                    visto[r[clave]] = j
    grupos: dict[int, list[str]] = {}
    for j, r in enumerate(registros):
        grupos.setdefault(raiz(j), []).append(r["id"])
    duplicados = sorted((sorted(g) for g in grupos.values() if len(g) > 1), key=lambda g: g[0])
    # Crecimiento (FIN-CAGR-001) entre el primer y el último periodo
    por_anio = {"mensual": 12, "trimestral": 4, "anual": 1}[gran]
    anios = (len(periodos) - 1) / por_anio
    v_ini, v_fin = por_periodo[periodos[0]], por_periodo[periodos[-1]]
    crecimiento = cagr(v_ini, v_fin, anios) if anios > 0 and v_ini > 0 and v_fin > 0 else None
    if crecimiento is None:
        lim.append("crecimiento no definido (un solo periodo o conteo nulo en un extremo)")
    # Precisión y exhaustividad frente a un conjunto de referencia
    pr = None
    if v.get("referencia") is not None:
        ref = _lista(v["referencia"], f"{F}: referencia")
        if not ref or not all(isinstance(x, str) and x for x in ref):
            raise ErrorFicha(f"{F}: referencia: lista de identificadores no vacía")
        G, Rr = set(ref), {r["id"] for r in registros}
        acierto = len(G & Rr)
        pr = {"precision": acierto / len(Rr), "exhaustividad": acierto / len(G), "aciertos": acierto,
              "recuperados": len(Rr), "referencia": len(G)}
    verif = {"suma_tematicas": sum(por_tematica.values()), "suma_periodos": sum(por_periodo.values()),
             "suma_fuentes": sum(por_fuente.values())}
    verif["cuadra"] = verif["suma_tematicas"] == verif["suma_periodos"] == verif["suma_fuentes"] == total
    return {"total": total, "granularidad": gran, "categorias": p["categorias"],
            "por_periodo": por_periodo, "por_tematica": dict(sorted(por_tematica.items())),
            "por_fuente": dict(sorted(por_fuente.items())), "tematica_por_periodo": dict(sorted(cruce.items())),
            "hhi_fuentes": hhi, "fuentes": len(por_fuente), "crecimiento_cagr": crecimiento,
            "duplicados": {"grupos": duplicados, "fichas_duplicadas": sum(len(g) - 1 for g in duplicados),
                           "unicas": total - sum(len(g) - 1 for g in duplicados)},
            "precision_exhaustividad": pr, "verificacion": verif, "referencia_ingenua": "RI-NA"}, lim


# ====================================================================== TEM-DIFF-001
def logistica(t: np.ndarray, m: float, k: float, t0: float) -> np.ndarray:
    return m / (1 + np.exp(-k * (t - t0)))


def gompertz(t: np.ndarray, m: float, k: float, t0: float) -> np.ndarray:
    return m * np.exp(-np.exp(-k * (t - t0)))


def bass(tau: np.ndarray, m: float, p_: float, q_: float) -> np.ndarray:
    e = np.exp(-(p_ + q_) * np.maximum(tau, 0.0))
    return m * (1 - e) / (1 + (q_ / p_) * e)


_MODELOS = ("logistica", "gompertz", "bass")


def _curva(modelo: str, t: np.ndarray, th: np.ndarray, origen: float) -> np.ndarray:
    if modelo == "logistica":
        return logistica(t, *th)
    if modelo == "gompertz":
        return gompertz(t, *th)
    return bass(t - origen, *th)


def _inflexion(modelo: str, th: np.ndarray, origen: float) -> float | None:
    if modelo in ("logistica", "gompertz"):
        return float(th[2])
    _, p_, q_ = th
    return origen + math.log(q_ / p_) / (p_ + q_) if q_ > p_ else None


def _ajuste_difusion(modelo: str, t: np.ndarray, y: np.ndarray, origen: float, m_fijo: float | None,
                     inicios: list[np.ndarray], tol: float) -> tuple[np.ndarray, float]:
    """Mínimos cuadrados no lineales (scipy least_squares, trf) desde varios arranques; devuelve (θ, SSR)."""
    mejor: tuple[np.ndarray, float] | None = None
    for th0 in inicios:
        libres = th0[1:] if m_fijo is not None else th0

        def res(x: np.ndarray) -> np.ndarray:
            th = np.concatenate([[m_fijo], x]) if m_fijo is not None else x
            return _curva(modelo, t, th, origen) - y

        lo = np.full(len(libres), EPS)
        hi = np.full(len(libres), np.inf)
        if modelo != "bass":
            lo[-1], hi[-1] = -np.inf, np.inf          # t0 libre
        try:
            sol = optimize.least_squares(res, np.clip(libres, lo + EPS, None), bounds=(lo, hi), method="trf",
                                         xtol=tol ** 2, ftol=tol ** 2, gtol=tol ** 2, x_scale="jac")
        except (ValueError, FloatingPointError):
            continue
        th = np.concatenate([[m_fijo], sol.x]) if m_fijo is not None else sol.x
        ssr = float(np.sum(sol.fun ** 2))
        if np.all(np.isfinite(th)) and math.isfinite(ssr) and (mejor is None or ssr < mejor[1]):
            mejor = (th, ssr)
    if mejor is None:
        raise ErrorFicha(f"TEM-DIFF-001: CONVERGENCIA: el ajuste {modelo} no converge desde ningún arranque")
    return mejor


def _inicios(modelo: str, t: np.ndarray, y: np.ndarray, origen: float, m_fijo: float | None, arranques: int,
             rng: np.random.Generator, umbral_intro: float) -> list[np.ndarray]:
    """Arranques: m₀ ~ U(máx y, máx y/0,16) (o el m fijado); t₀ ~ U en el doble del tramo observado; k₀ y (p₀, q₀) de la
    pendiente máxima observada (relaciones exactas de cada curva)."""
    ymax = float(np.max(y))
    pend = float(np.max(np.diff(y) / np.diff(t)))
    pend = pend if pend > 0 else ymax / float(t[-1] - t[0])
    out = []
    for _ in range(arranques):
        m0 = m_fijo if m_fijo is not None else float(rng.uniform(ymax, ymax / umbral_intro))
        if modelo == "bass":
            p0 = max(float(y[0]) / (m0 * max(float(t[0] - origen), EPS)), EPS)
            q0 = max(4 * pend / m0 - 2 * p0, p0)
            out.append(np.array([m0, p0, q0 * float(rng.uniform(0.5, 2.0))]))
        else:
            t0 = float(rng.uniform(t[0], t[-1] + (t[-1] - t[0])))
            k0 = (4 if modelo == "logistica" else math.e) * pend / m0
            out.append(np.array([m0, k0, t0]))
    return out


def _fase(cuota: float, umbrales: list[float]) -> str:
    return "introduccion" if cuota < umbrales[0] else ("crecimiento" if cuota <= umbrales[1] else "madurez")


def _anio_a_fecha(x: float) -> str:
    y = math.floor(x)
    dias = (date(y + 1, 1, 1) - date(y, 1, 1)).days
    return (date(y, 1, 1) + pd.Timedelta(days=round((x - y) * dias))).isoformat()


@_cerrado("TEM-DIFF-001")
def f_tem_diff(ent: dict[str, Any], p: dict[str, Any]) -> Resultado:
    F, lim = "TEM-DIFF-001", []
    v = _dict(ent["valores"], f"{F}: valores")
    if v.get("adopcion") is None:
        raise ErrorFicha(f"{F}: falta «adopcion» (serie de adopción acumulada)")
    y = _vector(v["adopcion"], f"{F}: adopcion")
    n = len(y)
    if v.get("anios") is not None:
        t = _vector(v["anios"], f"{F}: anios")
        if len(t) != n:
            raise ErrorFicha(f"{F}: {len(t)} años para {n} observaciones")
    elif v.get("fechas") is not None:
        fs = [_fecha(f, f"{F}: fechas") for f in _lista(v["fechas"], f"{F}: fechas")]
        if len(fs) != n:
            raise ErrorFicha(f"{F}: {len(fs)} fechas para {n} observaciones")
        t = np.array([f.year + (f.timetuple().tm_yday - 1) / (date(f.year + 1, 1, 1) - date(f.year, 1, 1)).days
                      for f in fs])
    else:
        raise ErrorFicha(f"{F}: faltan «anios» o «fechas» de la serie")
    if n < p["obs_minimas"]:
        raise ErrorFicha(f"{F}: {n} observaciones (< {p['obs_minimas']})")
    if np.any(np.diff(t) <= 0):
        raise ErrorFicha(f"{F}: el tiempo debe ser estrictamente creciente")
    if np.any(y < 0):
        raise ErrorFicha(f"{F}: adopción negativa")
    dy = np.diff(y)
    if not np.any((dy[1:] > dy[:-1]) & (dy[:-1] > 0)):
        raise ErrorFicha(f"{F}: sin tramo de aceleración observado (ningún incremento positivo seguido de otro mayor)")
    paso = float(np.median(np.diff(t)))
    origen = _num(v["lanzamiento"], f"{F}: lanzamiento") if v.get("lanzamiento") is not None else float(t[0]) - paso
    if origen >= t[0]:
        raise ErrorFicha(f"{F}: el lanzamiento debe ser anterior a la primera observación")
    rng = np.random.default_rng(p["semilla"])
    m_par = p["m"]
    m_fijo = m_par if isinstance(m_par, float) else None
    if m_fijo is not None and m_fijo < float(np.max(y)):
        raise ErrorFicha(f"{F}: techo m fijado ({m_fijo:g}) inferior a la adopción observada ({float(np.max(y)):g})")
    if m_fijo is None:
        lim.append("techo m estimado (no declarado): muy mal identificado antes del punto de inflexión")
    modelos = list(_MODELOS) if p["modelo"] == "auto" else [p["modelo"]]
    tol, umb = p["tolerancia"], p["fases"]
    k_par = 2 if m_fijo is not None else 3
    ajustes: dict[str, dict[str, Any]] = {}
    for mod in modelos:
        th, ssr = _ajuste_difusion(mod, t, y, origen, m_fijo,
                                   _inicios(mod, t, y, origen, m_fijo, p["arranques"], rng, umb[0]), tol)
        aic = n * math.log(max(ssr, EPS * float(np.sum(y ** 2))) / n) + 2 * k_par
        ajustes[mod] = {"theta": th, "ssr": ssr, "aic": aic}
    # Error fuera de muestra en el último tramo (último cuarto), si el tramo de ajuste conserva el mínimo de la ficha
    h = max(1, n // 4)
    oos: dict[str, float] = {}
    if n - h >= p["obs_minimas"]:
        for mod in modelos:
            th_o, _ = _ajuste_difusion(mod, t[:-h], y[:-h], origen, m_fijo,
                                       _inicios(mod, t[:-h], y[:-h], origen, m_fijo, p["arranques"], rng, umb[0]), tol)
            oos[mod] = float(np.sqrt(np.mean((_curva(mod, t[-h:], th_o, origen) - y[-h:]) ** 2)))
    else:
        lim.append(f"sin error fuera de muestra: el tramo de ajuste quedaría con < {p['obs_minimas']} observaciones")
    orden = sorted(ajustes, key=lambda x: (ajustes[x]["aic"], x))
    elegido = orden[0]
    if oos and min(oos, key=lambda x: (oos[x], x)) != elegido:
        lim.append("el AIC y el error fuera de muestra eligen modelos distintos")
    th = ajustes[elegido]["theta"]

    def resumen(mod: str, theta: np.ndarray) -> dict[str, Any]:
        m_ = float(theta[0])
        cuota = float(_curva(mod, t[-1:], theta, origen)[0]) / m_
        infl = _inflexion(mod, theta, origen)
        nombres = ["m", "k", "t0"] if mod != "bass" else ["m", "p", "q"]
        return {"modelo": mod, "parametros": {a: float(b) for a, b in zip(nombres, theta, strict=True)},
                "cuota_actual": cuota, "fase": _fase(cuota, umb), "inflexion_anio": infl,
                "inflexion_fecha": _anio_a_fecha(infl) if infl is not None else None}

    out = resumen(elegido, th)
    if out["inflexion_anio"] is None:
        lim.append("Bass con q ≤ p: sin punto de inflexión posterior al lanzamiento")
    futuro = t[-1] + paso * np.arange(1, math.floor(p["horizonte"] / paso + EPS) + 1)
    if len(futuro) == 0:
        futuro = np.array([t[-1] + p["horizonte"]])
    ajustado = _curva(elegido, t, th, origen)
    resid = y - ajustado
    sims = []
    for _ in range(p["B"]):
        yb = ajustado + rng.choice(resid, size=n, replace=True)
        try:
            thb, _ = _ajuste_difusion(elegido, t, yb, origen, m_fijo, [th.copy()], tol)
        except ErrorFicha:
            continue
        sims.append(_curva(elegido, futuro, thb, origen))
    if not sims:
        raise ErrorFicha(f"{F}: CONVERGENCIA: ninguna réplica del bootstrap converge")
    if len(sims) < p["B"]:
        lim.append(f"{p['B'] - len(sims)} réplicas del bootstrap sin converger, descartadas")
    sims_a = np.array(sims)
    qs = p["cuantiles_bandas"]
    bandas = {f"p{round(c * 100)}": np.quantile(sims_a, c, axis=0) for c in qs}
    prevision = {"anios": futuro, "central": _curva(elegido, futuro, th, origen), **bandas}
    escenarios = None
    if isinstance(m_par, list):
        escenarios = []
        for m_s in m_par:
            if m_s < float(np.max(y)):
                raise ErrorFicha(f"{F}: escenario de techo {m_s:g} inferior a la adopción observada")
            th_s, _ = _ajuste_difusion(elegido, t, y, origen, m_s,
                                       _inicios(elegido, t, y, origen, m_s, p["arranques"], rng, umb[0]), tol)
            r_s = resumen(elegido, th_s)
            r_s["prevision_final"] = float(_curva(elegido, futuro[-1:], th_s, origen)[0])
            escenarios.append({"m": m_s, **r_s})
    alternativo = None
    if len(orden) > 1:
        alt = orden[1]
        alternativo = {**resumen(alt, ajustes[alt]["theta"]), "aic": ajustes[alt]["aic"],
                       "prevision_final": float(_curva(alt, futuro[-1:], ajustes[alt]["theta"], origen)[0])}
    tasa = cagr(float(y[0]), float(y[-1]), float(t[-1] - t[0])) if y[0] > 0 else None
    ingenua = {"lineal_reciente": float(y[-1] + (y[-1] - y[-2]) / (t[-1] - t[-2]) * (futuro[-1] - t[-1])),
               "crecimiento_constante": float(y[-1] * (1 + tasa) ** (futuro[-1] - t[-1])) if tasa is not None else None,
               "anio": float(futuro[-1])}
    return {**out, "aic": {mod: a["aic"] for mod, a in ajustes.items()}, "ssr": ajustes[elegido]["ssr"],
            "error_fuera_de_muestra": oos or None, "tramo_fuera_de_muestra": h if oos else None,
            "lanzamiento": origen, "m_fijado": m_fijo is not None, "prevision": prevision,
            "trayectoria": {"anios": t, "observada": y, "ajustada": ajustado}, "replicas_bootstrap": len(sims),
            "semilla": p["semilla"], "escenarios_m": escenarios, "segunda_via": alternativo,
            "referencia_ingenua": ingenua}, lim


# ====================================================================== registro de fichas
FICHAS: dict[str, dict[str, Any]] = {
    "ST-INF-001": {"fn": f_st_inf, "modulo": "MC-01", "version": "1.1", "cifra": "ESTADISTICA", "ri": "RI-NA",
                   "tol": 1e-8},
    "FX-BRK-001": {"fn": f_fx_brk, "modulo": "MC-02", "version": "1.1", "cifra": "ESTADISTICA",
                   "ri": "Modelo sin ruptura", "tol": 1e-6},
    "FX-STL-001": {"fn": f_fx_stl, "modulo": "MC-02", "version": "1.1", "cifra": "ESTADISTICA", "ri": "RI-EST",
                   "tol": 1e-6},
    "FX-REGIME-001": {"fn": f_fx_regime, "modulo": "MC-02", "version": "1.1", "cifra": "ESTADISTICA",
                      "ri": "Un solo régimen", "tol": 1e-6},
    "REG-HMM-001": {"fn": f_reg_hmm, "modulo": "MC-02", "version": "1.0", "cifra": "ESTADISTICA",
                    "ri": "Régimen de la observación anterior; incondicional", "tol": 1e-6},
    "FX-COINT-001": {"fn": f_fx_coint, "modulo": "MC-03", "version": "1.1", "cifra": "ESTADISTICA",
                     "ri": "RI-PA (sin relación)", "tol": 1e-6},
    # «Tolerancias»: conteos exactos; las cifras no enteras (HHI, CAGR, precisión) con la aritmética determinista de 3.2.
    "BIB-MET-001": {"fn": f_bib_met, "modulo": "MC-01", "version": "1.1", "cifra": "DETERMINISTA", "ri": "RI-NA",
                    "tol": 1e-10},
    "TEM-DIFF-001": {"fn": f_tem_diff, "modulo": "MC-04", "version": "1.0", "cifra": "ESTADISTICA",
                     "ri": "Extrapolación lineal del crecimiento reciente y crecimiento constante (FIN-CAGR-001)",
                     "tol": 1e-6},
}


# ====================================================================== datos sintéticos de los casos de control
def ruido_weyl(n: int, fase: float = 0.0) -> np.ndarray:
    """Ruido determinista equidistribuido en [−½, ½): parte fraccionaria de t·φ (φ = razón áurea)."""
    return (np.arange(n) * (math.sqrt(5) - 1) / 2 + fase) % 1 - 0.5


def ruido_gaussiano(n: int, semilla: int) -> np.ndarray:
    """Ruido gaussiano reproducible (los datos de control llevan su propia semilla)."""
    return np.random.default_rng(semilla).standard_normal(n)


def _cerca(a: Any, b: float, tol: float) -> bool:
    return a is not None and abs(float(a) - b) <= tol * max(1.0, abs(b))


# ST-INF-001: t con 2 gl y con 1 gl tienen CDF cerrada (Student 1908): P(|T₂| > t) = 1 − t/√(2 + t²);
# P(|T₁| > t) = 1 − (2/π)·atan t; cuantil de T₂: (2u − 1)/√(2u(1 − u)).
_T2_975 = 0.95 / math.sqrt(2 * 0.975 * 0.025)
_IC_123 = (2 - _T2_975 / math.sqrt(3), 2 + _T2_975 / math.sqrt(3))
_HOLM_MUESTRAS = [[0.1, 0.5, 0.9, 1.4, 0.2], [0.3, -0.2, 0.4, 0.1, 0.6], [1.2, 1.9, 1.1, 2.3, 1.6],
                  [-0.1, 0.2, -0.3, 0.1, 0.05]]


def _holm_aparte(pv: list[float]) -> list[float]:
    """Holm recalculado por definición, para comprobar (no usa `ajuste_holm`)."""
    m = len(pv)
    orden = sorted(range(m), key=lambda i: pv[i])
    rango = {i: r for r, i in enumerate(orden)}
    return [max(min(1.0, (m - j) * pv[orden[j]]) for j in range(rango[i] + 1)) for i in range(m)]


def _bh_aparte(pv: list[float]) -> list[float]:
    m = len(pv)
    orden = sorted(range(m), key=lambda i: pv[i])
    rango = {i: r for r, i in enumerate(orden)}
    return [min(min(1.0, m * pv[orden[j]] / (j + 1)) for j in range(rango[i], m)) for i in range(m)]


def _correccion_ok(r: dict[str, Any], aparte: Callable[[list[float]], list[float]]) -> bool:
    nombres = sorted(r["contrastes"])
    pv = [r["contrastes"][n]["p_valor"] for n in nombres]
    esperado = aparte(pv)
    return all(_cerca(r["contrastes"][n]["p_ajustado"], e, 1e-12)
               and r["contrastes"][n]["rechaza_h0_ajustado"] == (e < r["nivel"]) for n, e in zip(nombres, esperado, strict=True))


def _coherencia_ic(r: dict[str, Any]) -> bool:
    ok = True
    for c in r["contrastes"].values():
        fuera = c["mu0"] < c["ic"]["inferior"] - 1e-12 or c["mu0"] > c["ic"]["superior"] + 1e-12
        ok = ok and c["rechaza_h0"] == fuera
    extremo = r["contrastes"]["extremo"]
    return ok and _cerca(extremo["p_valor"], r["nivel"], 1e-8) and _cerca(extremo["ic"]["inferior"], _IC_123[0], 1e-8)


# FX-BRK-001
_N_BRK = 120
_K_BRK = np.arange(_N_BRK)
_Y_NIVEL = np.where(_K_BRK < 60, 0.0, 3.0) + ruido_weyl(_N_BRK)
_Y_NIVEL_DEBIL = np.where(_K_BRK < 70, 0.0, 0.6) + ruido_weyl(_N_BRK, 0.3)
_Y_DOS = np.select([_K_BRK < 40, _K_BRK < 80], [0.0, 2.0], -1.0) + ruido_weyl(_N_BRK)
_Y_VAR = np.where(_K_BRK < 60, 1.0, 3.0) * ruido_weyl(_N_BRK)
_Y_PEND = np.where(_K_BRK < 60, 0.1 * _K_BRK, 6 - 0.1 * (_K_BRK - 60)) + 0.2 * ruido_weyl(_N_BRK)


def _ssr_exhaustiva(y: np.ndarray, recorte: float) -> int:
    """Fecha de una ruptura de nivel por búsqueda exhaustiva de la SSR mínima (sin programación dinámica)."""
    n = len(y)
    h = math.ceil(recorte * n)
    mejor = min(range(h, n - h + 1),
                key=lambda k: float(np.sum((y[:k] - y[:k].mean()) ** 2) + np.sum((y[k:] - y[k:].mean()) ** 2)))
    return mejor


# FX-STL-001
_PATRON = np.array([3, 1, -2, 0.5, 2, -1, -3, 0, 1.5, -0.5, -1, -0.5]) - np.mean([3, 1, -2, 0.5, 2, -1, -3, 0, 1.5,
                                                                                  -0.5, -1, -0.5])
_T_STL = np.arange(72)
_Y_STL_EXACTA = 10 + 0.05 * _T_STL + _PATRON[_T_STL % 12]
_Y_STL_RUIDO = 10 + 0.05 * _T_STL + _PATRON[_T_STL % 12] + 0.4 * ruido_weyl(72)
_Y_STL_MULT = 10 * np.exp(0.02 * _T_STL) * np.exp(0.1 * _PATRON[_T_STL % 12])


def _identidad_stl(y: np.ndarray, multiplicativa: bool) -> Callable[[dict[str, Any]], bool]:
    def comprobar(r: dict[str, Any]) -> bool:
        T, S, R = (np.array(r[c]) for c in ("tendencia", "estacional", "resto"))
        rec = T * S * R if multiplicativa else T + S + R
        return float(np.max(np.abs(rec - y))) <= FICHAS["FX-STL-001"]["tol"] * float(np.max(np.abs(y)))
    return comprobar


# FX-REGIME-001 y REG-HMM-001
_REG_VERDAD = (np.arange(300) // 50) % 2
_X_REGIME = ruido_gaussiano(300, 42) * np.where(_REG_VERDAD == 0, 1.0, 3.0)


def _hmm_x() -> tuple[dict[str, list[float]], list[str]]:
    n = 300
    reg = (np.arange(n) // 60) % 2
    a = ruido_gaussiano(n, 7) + np.where(reg == 0, -1.0, 1.5)
    b = ruido_gaussiano(n, 8) * np.where(reg == 0, 1.0, 2.0)
    fechas = [d.date().isoformat() for d in pd.date_range("2015-01-02", periods=n, freq="W-FRI")]
    return {"rendimiento": list(a), "volatilidad": list(b)}, fechas


_HMM_VARIABLES, _HMM_FECHAS = _hmm_x()


def _bic_un_regimen(x: np.ndarray) -> float:
    """BIC de una normal (media y varianza de máxima verosimilitud): −2·Σ ln φ + 2·ln n."""
    n, m, v = len(x), float(np.mean(x)), float(np.var(x))
    return n * math.log(2 * math.pi * v) + float(np.sum((x - m) ** 2)) / v + 2 * math.log(n)


def _suman_uno(r: dict[str, Any], *claves: str) -> bool:
    ok = all(abs(sum(f) - 1) <= 1e-12 for f in r["matriz_transicion"])
    for c in claves:
        bloque: Any = r
        for parte in c.split("."):
            bloque = bloque[parte]
        ok = ok and all(abs(sum(f) - 1) <= 1e-12 for f in bloque)
    return ok


def _filtro_hamilton_ok(x: np.ndarray) -> Callable[[dict[str, Any]], bool]:
    def comprobar(r: dict[str, Any]) -> bool:
        e = r["estados"]
        filt, ll = hamilton_filtro(x, np.array([s["probabilidad_inicial"] for s in e]), np.array(r["matriz_transicion"]),
                                   np.array([s["media"] for s in e]), np.array([s["desviacion"] for s in e]))
        return (float(np.max(np.abs(filt - np.array(r["serie"]["filtradas"])))) <= 1e-10
                and _cerca(ll, r["loglik"], 1e-10))
    return comprobar


def _filtro_hmm_ok(r: dict[str, Any]) -> bool:
    """Filtro hacia delante paso a paso con densidades normales multivariantes (scipy), desde los parámetros servidos."""
    X = np.column_stack([_HMM_VARIABLES[c] for c in r["variables"]])
    Z = (X - X.mean(0)) / X.std(0, ddof=1)
    e = r["estados"]
    A = np.array(r["matriz_transicion"])
    pred = np.array([s["probabilidad_inicial"] for s in e])
    ll, filt = 0.0, []
    for z in Z:
        dens = np.array([stats.multivariate_normal.pdf(
            z, [s["medias_estandarizadas"][c] for c in r["variables"]],
            np.diag(s["covarianza_estandarizada"]) if r["covarianza"] == "diagonal" else s["covarianza_estandarizada"])
            for s in e])
        a = pred * dens
        ll += math.log(a.sum())
        filt.append(a / a.sum())
        pred = filt[-1] @ A
    return float(np.max(np.abs(np.array(filt) - np.array(r["serie_filtradas"]["probabilidades"])))) <= 1e-10 \
        and _cerca(ll, r["loglik"], 1e-10)


# FX-COINT-001
def _par_cointegrado() -> dict[str, list[float]]:
    e = ruido_gaussiano(600, 3)
    x = np.cumsum(e[:300])
    u = np.zeros(300)
    for t in range(1, 300):
        u[t] = 0.5 * u[t - 1] + 0.5 * e[300 + t]
    return {"y": list(2 * x + 1 + u), "x": list(x)}


_PAR = _par_cointegrado()
_INDEP = {"y": list(np.cumsum(ruido_gaussiano(300, 11))), "x": list(np.cumsum(ruido_gaussiano(300, 12)))}


def _traza_ok(r: dict[str, Any]) -> bool:
    lam = np.array(r["johansen"]["autovalores"])
    T = r["n"] - r["johansen"]["orden_var"]
    return all(_cerca(f["estadistico"], -T * float(np.sum(np.log(1 - lam[f["r"]:]))), 1e-10) for f in r["johansen"]["traza"])


# BIB-MET-001
_FICHAS_BIB = [{"id": f"F{i:02d}", "fecha": f"{2024 + i // 12}-{i % 12 + 1:02d}-15", "tematica": f"TM-0{i % 3 + 1}",
                "fuente": "AB"[i % 2] if i % 5 else "C", "titulo": f"Estudio número {i}"} for i in range(24)]
_FICHAS_DUP = [
    {"id": "A", "fecha": "2025-01-10", "tematica": "TM-01", "fuente": "X", "titulo": "Prima de riesgo: Á", "hash": "h1"},
    {"id": "B", "fecha": "2025-02-10", "tematica": "TM-01", "fuente": "Y", "titulo": "prima de riesgo a", "hash": "h2"},
    {"id": "C", "fecha": "2025-03-10", "tematica": "TM-02", "fuente": "X", "titulo": "Otra cosa", "hash": "H2"},
    {"id": "D", "fecha": "2025-03-11", "tematica": "TM-02", "fuente": "Z", "titulo": "Distinto", "hash": "h4"},
    {"id": "E", "fecha": "2025-04-01", "tematica": "TM-03", "fuente": "Z", "titulo": "Nada que ver"},
]


def _conteos_ok(fichas: list[dict[str, Any]]) -> Callable[[dict[str, Any]], bool]:
    def comprobar(r: dict[str, Any]) -> bool:
        por_t: dict[str, int] = {}
        por_f: dict[str, int] = {}
        por_p: dict[str, int] = {}
        for f in fichas:
            por_t[f["tematica"]] = por_t.get(f["tematica"], 0) + 1
            por_f[f["fuente"]] = por_f.get(f["fuente"], 0) + 1
            por_p[f["fecha"][:7]] = por_p.get(f["fecha"][:7], 0) + 1
        return (r["total"] == len(fichas) and r["por_tematica"] == por_t and r["por_fuente"] == por_f
                and {k: v for k, v in r["por_periodo"].items() if v} == por_p
                and sum(r["por_tematica"].values()) == sum(r["por_periodo"].values()) == sum(r["por_fuente"].values())
                == r["total"] and all(sum(c.values()) == por_t[t] for t, c in r["tematica_por_periodo"].items()))
    return comprobar


def _hhi_cagr_ok(r: dict[str, Any]) -> bool:
    cuotas = [v / r["total"] for v in r["por_fuente"].values()]
    per = list(r["por_periodo"].values())
    anios = (len(per) - 1) / 12
    return (_cerca(r["hhi_fuentes"], sum(c * c for c in cuotas), 1e-12)
            and _cerca(r["crecimiento_cagr"], (per[-1] / per[0]) ** (1 / anios) - 1, 1e-12))


# TEM-DIFF-001
_ANIOS = list(range(2010, 2022))
_LOG = [100 / (1 + math.exp(-0.8 * (a - 2016.5))) for a in _ANIOS]
_GOMP = [100 * math.exp(-math.exp(-0.8 * (a - 2016.5))) for a in _ANIOS]
_BASS = list(bass(np.array(_ANIOS, dtype=float) - 2009, 100, 0.01, 0.6))
_LOG_TEMPRANA = [100 / (1 + math.exp(-0.5 * (a - 2026))) for a in _ANIOS]


def _parametros_ok(r: dict[str, Any], verdad: dict[str, float]) -> bool:
    return all(_cerca(r["parametros"][k], v, FICHAS["TEM-DIFF-001"]["tol"]) for k, v in verdad.items())


CASOS_CONTROL: dict[str, list[dict[str, Any]]] = {
    "ST-INF-001": [
        {"nombre": "p-valor conocido: t con 2 gl, p = 1 − t/√(2 + t²) e IC = x̄ ± t₀,₉₇₅(2)·s/√n en forma cerrada",
         "datos": [{"valores": {"contrastes": [{"nombre": "c", "muestra": [1.0, 2.0, 3.0], "mu0": 0.0}]}}],
         "parametros": {"tipo_contraste": "t_una_muestra"},
         "comprobar": lambda r: _cerca(r["contrastes"]["c"]["estadistico"], 2 * math.sqrt(3), 1e-12)
         and _cerca(r["contrastes"]["c"]["p_valor"], 1 - 2 * math.sqrt(3) / math.sqrt(14), 1e-8)
         and _cerca(r["contrastes"]["c"]["ic"]["inferior"], _IC_123[0], 1e-8)
         and _cerca(r["contrastes"]["c"]["ic"]["superior"], _IC_123[1], 1e-8)
         and _cerca(r["contrastes"]["c"]["efecto"]["valor"], 2.0, 1e-12) and r["correccion"].startswith("ninguna")},
        {"nombre": "p-valor conocido: t con 1 gl (Cauchy), p = 1 − (2/π)·atan|t|",
         "datos": [{"valores": {"contrastes": [{"nombre": "c", "muestra": [1.0, 3.0], "mu0": 0.5}]}}],
         "parametros": {"tipo_contraste": "t_una_muestra"},
         "comprobar": lambda r: _cerca(r["contrastes"]["c"]["p_valor"], 1 - 2 / math.pi * math.atan(1.5), 1e-8)},
        {"nombre": "Mann-Whitney exacto con muestras separadas (3 y 3): p = 2/C(6,3) = 0,1 y efecto 1",
         "datos": [{"valores": {"contrastes": [{"nombre": "c", "muestra_a": [4.0, 5.0, 6.0], "muestra_b": [1.0, 2.0, 3.0]}]}}],
         "parametros": {"tipo_contraste": "mann_whitney"},
         "comprobar": lambda r: _cerca(r["contrastes"]["c"]["p_valor"], 2 / math.comb(6, 3), 1e-12)
         and r["contrastes"]["c"]["efecto"]["valor"] == 1.0},
        {"nombre": "IC coherente con el p-valor: μ₀ en el extremo ⇒ p = nivel; rechaza ⟺ μ₀ fuera del IC",
         "datos": [{"valores": {"contrastes": [
             {"nombre": "extremo", "muestra": [1.0, 2.0, 3.0], "mu0": _IC_123[0]},
             {"nombre": "centro", "muestra": [1.0, 2.0, 3.0], "mu0": 2.0},
             {"nombre": "dentro", "muestra": [1.0, 2.0, 3.0], "mu0": 4.0},
             {"nombre": "fuera_abajo", "muestra": [1.0, 2.0, 3.0], "mu0": _IC_123[0] - 0.5},
             {"nombre": "fuera_arriba", "muestra": [1.0, 2.0, 3.0], "mu0": _IC_123[1] + 0.1}]}}],
         "parametros": {"tipo_contraste": "t_una_muestra"}, "comprobar": _coherencia_ic},
        {"nombre": "Holm con m = 4: p ajustados por definición y decisiones con el nivel",
         "datos": [{"valores": {"contrastes": [{"nombre": f"c{i}", "muestra": m} for i, m in enumerate(_HOLM_MUESTRAS)]}}],
         "parametros": {"tipo_contraste": "t_una_muestra"},
         "comprobar": lambda r: r["correccion"] == "holm" and _correccion_ok(r, _holm_aparte)},
        {"nombre": "Benjamini-Hochberg con m = 4: p ajustados por definición",
         "datos": [{"valores": {"contrastes": [{"nombre": f"c{i}", "muestra": m} for i, m in enumerate(_HOLM_MUESTRAS)]}}],
         "parametros": {"tipo_contraste": "t_una_muestra", "correccion": "bh"},
         "comprobar": lambda r: r["correccion"] == "bh" and _correccion_ok(r, _bh_aparte)},
    ],
    "FX-BRK-001": [
        {"nombre": "salto de nivel conocido en t = 60: fecha exacta, salto = diferencia de medias, IC que la contiene y "
                   "CUSUM que coincide (segunda vía)",
         "datos": [{"valores": {"serie": list(_Y_NIVEL)}}], "parametros": {},
         "comprobar": lambda r: r["tipo_cambio"] == "nivel" and r["n_rupturas"] == 1 and r["rupturas"][0]["indice"] == 60
         and _cerca(r["rupturas"][0]["cambio"]["salto"], float(_Y_NIVEL[60:].mean() - _Y_NIVEL[:60].mean()), 1e-10)
         and r["rupturas"][0]["ic"]["inferior"] <= 60 <= r["rupturas"][0]["ic"]["superior"]
         and r["cusum"]["indice"] == 60 and r["cusum"]["rechaza_sin_ruptura"] and r["segunda_via"]["coinciden"]},
        {"nombre": "Bai-Perron = mínimo de la SSR por búsqueda exhaustiva en todas las fechas admisibles",
         "datos": [{"valores": {"serie": list(_Y_NIVEL_DEBIL)}}], "parametros": {"tipo_cambio": "nivel"},
         "comprobar": lambda r: r["n_rupturas"] == 1
         and r["rupturas"][0]["indice"] == _ssr_exhaustiva(_Y_NIVEL_DEBIL, PARAMETROS_POR_DEFECTO["FX-BRK-001"]["recorte"])},
        {"nombre": "serie sin ruptura: el BIC elige 0 rupturas y el CUSUM no rechaza (las dos vías coinciden)",
         "datos": [{"valores": {"serie": list(ruido_weyl(_N_BRK))}}], "parametros": {},
         "comprobar": lambda r: r["n_rupturas"] == 0 and not r["cusum"]["rechaza_sin_ruptura"]
         and r["segunda_via"]["coinciden"] and r["referencia_ingenua"]["mejora_bic"] == 0},
        {"nombre": "dos rupturas de nivel (n ≥ 50): fechas 40 y 80 exactas",
         "datos": [{"valores": {"serie": list(_Y_DOS)}}], "parametros": {"max_rupturas": 2},
         "comprobar": lambda r: r["tipo_cambio"] == "nivel" and [x["indice"] for x in r["rupturas"]] == [40, 80]},
        {"nombre": "ruptura de varianza (σ × 3 en t = 60): clasificada como varianza y fechada dentro de su IC",
         "datos": [{"valores": {"serie": list(_Y_VAR)}}], "parametros": {},
         "comprobar": lambda r: r["tipo_cambio"] == "varianza" and r["n_rupturas"] == 1
         and r["rupturas"][0]["ic"]["inferior"] <= 60 <= r["rupturas"][0]["ic"]["superior"]
         and r["rupturas"][0]["cambio"]["ratio"] > 1},
        {"nombre": "ruptura de pendiente (+0,1 → −0,1 en t = 60): clasificada como pendiente y fechada",
         "datos": [{"valores": {"serie": list(_Y_PEND)}}], "parametros": {},
         "comprobar": lambda r: r["tipo_cambio"] == "pendiente" and r["n_rupturas"] == 1
         and r["rupturas"][0]["ic"]["inferior"] <= 60 <= r["rupturas"][0]["ic"]["superior"]
         and _cerca(r["rupturas"][0]["cambio"]["cambio_pendiente"], -0.2, 0.05)},
    ],
    "FX-STL-001": [
        {"nombre": "identidad tendencia + estacional + resto = serie (con ruido)",
         "datos": [{"valores": {"serie": list(_Y_STL_RUIDO)}}], "parametros": {"periodo": 12, "esquema": "aditivo"},
         "comprobar": _identidad_stl(_Y_STL_RUIDO, False)},
        {"nombre": "estacionalidad conocida: tendencia lineal + patrón periódico ⇒ S = patrón y T = recta (1e-6); "
                   "el esquema auto elige aditivo",
         "datos": [{"valores": {"serie": list(_Y_STL_EXACTA)}}], "parametros": {"periodo": 12},
         "comprobar": lambda r: r["esquema"] == "aditivo"
         and float(np.max(np.abs(np.array(r["estacional"]) - _PATRON[_T_STL % 12]))) <= FICHAS["FX-STL-001"]["tol"]
         and float(np.max(np.abs(np.array(r["tendencia"]) - (10 + 0.05 * _T_STL)))) <= FICHAS["FX-STL-001"]["tol"]},
        {"nombre": "estacionalidad proporcional: el esquema auto elige multiplicativo y T·S·R = serie",
         "datos": [{"valores": {"serie": list(_Y_STL_MULT)}}], "parametros": {"periodo": 12},
         "comprobar": lambda r: r["esquema"] == "multiplicativo" and _identidad_stl(_Y_STL_MULT, True)(r)
         and float(np.max(np.abs(np.array(r["estacional"]) - np.exp(0.1 * _PATRON[_T_STL % 12])))) <= 1e-6},
        {"nombre": "segunda vía: las medias móviles centradas dan el mismo patrón estacional en el caso exacto",
         "datos": [{"valores": {"serie": list(_Y_STL_EXACTA)}}], "parametros": {"periodo": 12},
         "comprobar": lambda r: r["segunda_via"]["diferencia_max"] <= FICHAS["FX-STL-001"]["tol"]
         and float(np.max(np.abs(np.array(r["segunda_via"]["patron_estacional"]) - _PATRON))) <= 1e-10},
    ],
    "FX-REGIME-001": [
        {"nombre": "probabilidades filtradas y suavizadas suman 1 en cada fecha; filas de la transición también",
         "datos": [{"valores": {"serie": list(_X_REGIME)}}], "parametros": {},
         "comprobar": lambda r: _suman_uno(r, "serie.filtradas", "serie.suavizadas_solo_descriptivas")
         and abs(sum(r["probabilidades_filtradas_actuales"].values()) - 1) <= 1e-12},
        {"nombre": "las filtradas y la log-verosimilitud reproducen el filtro de Hamilton paso a paso con los parámetros",
         "datos": [{"valores": {"serie": list(_X_REGIME)}}], "parametros": {},
         "comprobar": _filtro_hamilton_ok(_X_REGIME)},
        {"nombre": "segunda vía: otra semilla llega al mismo óptimo (log-verosimilitud dentro de 1e-6)",
         "datos": [{"valores": {"serie": list(_X_REGIME)}}], "parametros": {},
         "comprobar": lambda r: r["segunda_via"]["coincide"]
         and abs(r["segunda_via"]["loglik"] - r["loglik"]) <= FICHAS["FX-REGIME-001"]["tol"] * (1 + abs(r["loglik"]))},
        {"nombre": "dos regímenes de varianza (σ = 1 y 3): el BIC prefiere dos regímenes y las varianzas quedan ordenadas",
         "datos": [{"valores": {"serie": list(_X_REGIME)}}], "parametros": {},
         "comprobar": lambda r: r["referencia_ingenua"]["mejora_bic"] > 0
         and _cerca(r["referencia_ingenua"]["bic"], _bic_un_regimen(_X_REGIME), 1e-12)
         and _cerca(r["bic"], -2 * r["loglik"] + 6 * math.log(len(_X_REGIME)), 1e-12)
         and _cerca(r["referencia_ingenua"]["mejora_bic"], r["referencia_ingenua"]["bic"] - r["bic"], 1e-12)
         and r["estados"][0]["desviacion"] < r["estados"][1]["desviacion"]
         and r["estados"][0]["media"] == r["estados"][1]["media"]},
    ],
    "REG-HMM-001": [
        {"nombre": "filas de la matriz de transición y probabilidades filtradas suman 1; estados ordenados por medias",
         "datos": [{"valores": {"variables": _HMM_VARIABLES, "fechas": _HMM_FECHAS}}], "parametros": {"n_estados": 2},
         "comprobar": lambda r: _suman_uno(r, "serie_filtradas.probabilidades")
         and r["estados"][0]["medias"]["rendimiento"] < r["estados"][1]["medias"]["rendimiento"]},
        {"nombre": "estabilidad entre semillas: misma log-verosimilitud y mismas medias con las etiquetas alineadas",
         "datos": [{"valores": {"variables": _HMM_VARIABLES, "fechas": _HMM_FECHAS}}], "parametros": {"n_estados": 2},
         "comprobar": lambda r: r["segunda_via"]["coincide"]
         and r["segunda_via"]["diferencia_max_medias"] <= math.sqrt(FICHAS["REG-HMM-001"]["tol"])},
        {"nombre": "las filtradas y la log-verosimilitud reproducen el filtro hacia delante con densidades normales",
         "datos": [{"valores": {"variables": _HMM_VARIABLES, "fechas": _HMM_FECHAS}}], "parametros": {"n_estados": 2},
         "comprobar": _filtro_hmm_ok},
        {"nombre": "covarianza completa: mismas identidades del filtro",
         "datos": [{"valores": {"variables": _HMM_VARIABLES, "fechas": _HMM_FECHAS}}],
         "parametros": {"n_estados": 2, "covarianza": "completa"}, "comprobar": _filtro_hmm_ok},
    ],
    "FX-COINT-001": [
        {"nombre": "residuos de media nula: regresión de cointegración y MCE de Engle-Granger",
         "datos": [{"valores": {"series": _PAR}}], "parametros": {"metodo": "Engle-Granger"},
         "comprobar": lambda r: abs(float(np.mean(r["desviacion_equilibrio"]["valores"]))) <= 1e-10 * r["verificacion"]["escala"]
         and abs(r["verificacion"]["media_residuos_mce"]) <= 1e-10 * r["verificacion"]["escala"]},
        {"nombre": "segunda vía: Johansen y Engle-Granger coinciden en un par cointegrado conocido (y = 2x + 1 + AR(1))",
         "datos": [{"valores": {"series": _PAR}}], "parametros": {},
         "comprobar": lambda r: r["cointegracion"] and r["johansen"]["rango"] == 1
         and r["engle_granger"]["adf_residuos"]["rechaza"] and r["segunda_via"]["coinciden_en_cointegracion"]
         and _cerca(r["vector_normalizado"]["x"], -2.0, 0.05) and _cerca(r["engle_granger"]["vector"][1], -2.0, 0.05)},
        {"nombre": "paseos aleatorios independientes: sin cointegración por las dos vías",
         "datos": [{"valores": {"series": _INDEP}}], "parametros": {},
         "comprobar": lambda r: not r["cointegracion"] and r["johansen"]["rango"] == 0
         and not r["engle_granger"]["adf_residuos"]["rechaza"]},
        {"nombre": "traza = −T·Σ ln(1 − λᵢ) y vida media = ln ½ / ln ρ con 0 < ρ < 1",
         "datos": [{"valores": {"series": _PAR}}], "parametros": {},
         "comprobar": lambda r: _traza_ok(r) and 0 < r["rho"] < 1
         and _cerca(r["vida_media_periodos"], math.log(0.5) / math.log(r["rho"]), 1e-12)
         and r["velocidad_ajuste"]["y"] < 0},
    ],
    "BIB-MET-001": [
        {"nombre": "totales por temática, periodo y fuente suman el total (recontados aparte)",
         "datos": [{"valores": {"fichas": _FICHAS_BIB}}], "parametros": {},
         "comprobar": _conteos_ok(_FICHAS_BIB)},
        {"nombre": "duplicados por huella y por título normalizado (componentes conexas)",
         "datos": [{"valores": {"fichas": _FICHAS_DUP}}], "parametros": {},
         "comprobar": lambda r: r["duplicados"]["grupos"] == [["A", "B", "C"]] and r["duplicados"]["unicas"] == 3},
        {"nombre": "HHI = Σ cuotas² por fuente y crecimiento = CAGR de FIN-CAGR-001 entre periodos extremos",
         "datos": [{"valores": {"fichas": _FICHAS_BIB}}], "parametros": {}, "comprobar": _hhi_cagr_ok},
        {"nombre": "precisión y exhaustividad frente a un conjunto de referencia",
         "datos": [{"valores": {"fichas": _FICHAS_BIB, "referencia": ["F00", "F01", "F02", "X99"]}}], "parametros": {},
         "comprobar": lambda r: r["precision_exhaustividad"]["precision"] == 3 / 24
         and r["precision_exhaustividad"]["exhaustividad"] == 3 / 4},
    ],
    "TEM-DIFF-001": [
        {"nombre": "serie sintética logística recuperada dentro de 1e-6 y elegida por AIC; inflexión en t₀",
         "datos": [{"valores": {"adopcion": _LOG, "anios": _ANIOS}}], "parametros": {"B": 50},
         "comprobar": lambda r: r["modelo"] == "logistica" and _parametros_ok(r, {"m": 100, "k": 0.8, "t0": 2016.5})
         and _cerca(r["inflexion_anio"], 2016.5, 1e-6) and r["fase"] == "madurez"},
        {"nombre": "segunda vía: serie de Gompertz ⇒ elegida Gompertz y servido el modelo alternativo",
         "datos": [{"valores": {"adopcion": _GOMP, "anios": _ANIOS}}], "parametros": {"B": 50},
         "comprobar": lambda r: r["modelo"] == "gompertz" and _parametros_ok(r, {"m": 100, "k": 0.8, "t0": 2016.5})
         and r["segunda_via"] is not None and r["segunda_via"]["modelo"] != "gompertz"},
        {"nombre": "Bass con lanzamiento conocido: (m, p, q) recuperados e inflexión = lanzamiento + ln(q/p)/(p + q)",
         "datos": [{"valores": {"adopcion": _BASS, "anios": _ANIOS, "lanzamiento": 2009}}],
         "parametros": {"B": 50, "modelo": "bass"},
         "comprobar": lambda r: _parametros_ok(r, {"m": 100, "p": 0.01, "q": 0.6})
         and _cerca(r["inflexion_anio"], 2009 + math.log(60) / 0.61, 1e-6)},
        {"nombre": "fase con techo declarado: cuota = N(t)/m < 16 % ⇒ introducción",
         "datos": [{"valores": {"adopcion": _LOG_TEMPRANA, "anios": _ANIOS}}],
         "parametros": {"B": 50, "modelo": "logistica", "m": 100},
         "comprobar": lambda r: r["fase"] == "introduccion" and _cerca(r["cuota_actual"], _LOG_TEMPRANA[-1] / 100, 1e-6)},
    ],
}
