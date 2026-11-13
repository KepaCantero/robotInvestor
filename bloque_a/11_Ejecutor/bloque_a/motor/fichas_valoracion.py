"""Fichas del Motor del Bloque A · grupo V: valoración de renta variable, renta fija, divisas y derivados.

T-112 (Motor Fase 2). Fuente de verdad: «Catálogo de cálculos del Motor - V5.0», fichas ACC-VAL-001, ACC-ERP-001,
ACC-FACT-001 (sección 8), FIR-PRICE-001, FIR-CURVE-001, FIR-CARRY-001, FIR-SPREAD-001 (sección 9), FX-MOM-001
(sección 10), FX-PPA-001 (heredada, sección 6) y DER-OPT-001 (sección 7), y la sección 3 (convenciones comunes).

Convenciones de este módulo (Catálogo 3.1 salvo que la ficha diga otra cosa):

- Todo dato llega en línea en ``ent["valores"]`` (las fichas de este grupo trabajan con curvas, contratos, agregados
  contables e historias fechadas, que no son series de cierres de HT-01). FX-MOM-001 acepta además el spot de cada par
  en ``ent["series"][par]``.
- **Unidades.** Tipos, rendimientos, cupones, crecimientos, volatilidades y rentabilidades en **% anual** (5 = 5 %),
  salvo que la clave diga otra cosa; diferenciales y sensibilidades por punto básico en **pb**; precios de bonos por
  100 de nominal; plazos en años. ACC-FACT-001 recibe rendimientos en % por periodo. Recuperación (FIR-SPREAD-001) en
  tanto por uno, como la da la ficha (0,40).
- Recuento Real/365 para pasar fechas a años; en FIR-PRICE-001, la convención de mercado declarada (ACT/ACT ICMA o
  30E/360). Anualización con 252 sesiones; capitalización compuesta.
- **Umbrales fijos.** Los umbrales de rechazo y de limitación, los rangos admitidos y las constantes del método están en
  ``UMBRALES`` (cada uno cita su campo de la ficha o va marcado [PROPUESTO], INC-T112-01). Una petición que traiga uno
  se rechaza. Todo parámetro de la petición tiene tipo y rango (``_validar_parametros``); un parámetro desconocido se
  rechaza.
- **Falla cerrado.** Entradas que faltan, mal formadas o fuera de dominio, la «Aclaración y rechazo» y las «Entradas
  mínimas» lanzan ``ErrorFicha`` con el motivo. Lo iterativo (TIR, NSS, r implícita, DCF inverso, volatilidad
  implícita) tiene tope de iteraciones y rechaza si no converge («CONVERGENCIA»). Ningún número no finito sale: la
  envoltura ``_cerrado`` rechaza; una salida opcional que no se puede calcular se entrega como ``None`` con su
  limitación.
- **Advertencias.** Las «Supuestos y limitaciones» de cada ficha van en ``resultado["advertencias"]`` (no como
  limitaciones del cálculo), seguidas de las que dispare el cálculo (p. ej., valor terminal > 85 %).
- **Determinismo.** Sin azar salvo FIR-CURVE-001 (arranques del ajuste), con semilla explícita en los parámetros.
- El redondeo de entrega (banquero, 4 decimales) es de la capa de servicio: aquí no se redondea.

Interfaz: ``f(ent, params) -> (resultado, limitaciones)`` con ``ent = {"valores": {...}, "series": {...},
"series_rol": {...}}``.
"""
from __future__ import annotations

import math
import re
from collections.abc import Callable
from datetime import date, datetime
from functools import wraps
from itertools import pairwise
from typing import Any

import numpy as np
import pandas as pd
from scipy import optimize, stats

from .operaciones import ErrorFicha

Resultado = tuple[dict[str, Any], list[str]]
Manejador = Callable[[dict[str, Any], dict[str, Any]], Resultado]

# ------------------------------------------------------------------ conversiones de unidades (definiciones, no parámetros)
PCT = 100                 # tanto por uno → %
PB_POR_PUNTO = 100        # 1 punto porcentual = 100 pb
PB_POR_UNIDAD = 10_000    # 1 (tanto por uno) = 10 000 pb
MESES_POR_ANIO = 12
SEMANAS_POR_ANIO = 52
DIAS_POR_SEMANA = 7
DIAS_POR_ANIO = 365       # Catálogo 3.1: Real/365 (θ por día también por 365 días naturales)
SESIONES_POR_ANIO = 252   # Catálogo 3.1: anualización con 252 sesiones
NOMINAL = 100             # FIR-PRICE-001, «Salidas»: precio por 100 nominal
BASE_30E = 360            # convención 30E/360 (ICMA): año de 360 días
MES_30E = 30              # convención 30E/360 (ICMA): mes de 30 días

# ------------------------------------------------------------------ parámetros por defecto (campo «Parámetros»)
PARAMETROS_POR_DEFECTO: dict[str, dict[str, Any]] = {
    # ACC-VAL-001 · años_explicitos (5; 3–10); g_terminal (min(r_f, 4 %); 0–r_f); PRM (ACC-ERP-001 o 5 %; 3–7 %);
    # tasa_impositiva (legal marginal). None = el valor por defecto que da la ficha con los datos (r_f, ACC-ERP-001, la
    # tasa legal aportada). enfoque: «FCFF» (método i) o «FCFE» (método vi, flujo al accionista).
    "ACC-VAL-001": {"anios_explicitos": 5, "g_terminal": None, "PRM": None, "tasa_impositiva": None, "enfoque": "FCFF"},
    # ACC-ERP-001 · g_L (r_f; r_f − 1 pp a r_f); incluir_recompras (true); ventana_percentil (20 años; mínimo 10).
    "ACC-ERP-001": {"g_L": None, "incluir_recompras": True, "ventana_percentil": 20},
    # ACC-FACT-001 · modelo (FF5 + UMD; CAPM; FF3); frecuencia (mensual); ventana_movil (36 meses). «Método»: opcional
    # QMJ, BAB (adicionales).
    "ACC-FACT-001": {"modelo": "FF5+UMD", "adicionales": [], "frecuencia": "mensual", "ventana_movil": 36},
    # FIR-PRICE-001 · convencion (de mercado: la declarada en los datos); delta_y (10 pb; 1–25).
    "FIR-PRICE-001": {"convencion": None, "delta_y": 10},
    # FIR-CURVE-001 · modelo (NSS si ≥ 8 nodos; NS); lambda (estimado; fijo Diebold-Li); arranques (20);
    # semilla (entero del plan; 0 por defecto [PROPUESTO]).
    "FIR-CURVE-001": {"modelo": "auto", "lambda": "estimado", "arranques": 20, "semilla": 0},
    # FIR-CARRY-001 · delta_t (3 meses; 1–12).
    "FIR-CARRY-001": {"delta_t": 3},
    # FIR-SPREAD-001 · ventana (20 años; mínimo 10 con limitación); recuperacion (0,40; 0,2–0,6); ajuste_composicion.
    "FIR-SPREAD-001": {"ventana": 20, "recuperacion": 0.40, "ajuste_composicion": False},
    # FX-MOM-001 · retrospecciones (1, 3, 12 meses); volatilidad (implicita_3m).
    "FX-MOM-001": {"retrospecciones": [1, 3, 12], "volatilidad": "implicita_3m"},
    # FX-PPA-001 · ventana (completa); base (primer periodo común o media de largo plazo); suavizado (null).
    "FX-PPA-001": {"ventana": None, "base": "primer_periodo", "suavizado": None},
    # DER-OPT-001 · modelo (BSM; Black-76; CRR); pasos (500); tol_iv (1e-8). «Método»: densidad neutral al riesgo
    # (Breeden-Litzenberger) opcional.
    "DER-OPT-001": {"modelo": "BSM", "pasos": 500, "tol_iv": 1e-8, "densidad": False},
}

# Umbrales y constantes del método: no son parámetros de la petición (una petición que traiga uno se rechaza).
# QA r01 de T-112, H-01: todo tamaño de la petición (parámetro o lista de los datos) tiene cota superior. Las que no fija
# la ficha ni otra ficha citada son [PROPUESTO] (INC-T112-01), entre ellas la regla común «historia ≤ 100 años»: más que
# cualquier serie de mercado que citan las fichas del grupo (los factores de Fama y French de ACC-FACT-001 empiezan en
# 1926); con fechas diarias estrictamente crecientes acota además el número de observaciones (≤ 36 525).
UMBRALES: dict[str, dict[str, Any]] = {
    # ACC-VAL-001 · «Parámetros»: años 3–10, g_terminal tope 4 %, PRM 5 % de respaldo y 3–7 %. «Entradas mínimas»: ≥ 3
    # ejercicios (5 recomendados). «Supuestos»: valor terminal > 85 %. «Método (iv)»: percentil frente a ≥ 10 años;
    # (v): WACC ±1 pp × g ±0,5 pp; (i): β de ACC-FACT-001 o 1. Tope de iteraciones del DCF inverso [PROPUESTO]: 100
    # (el de scipy.optimize.brentq). Cotas [PROPUESTO]: ≤ 100 ejercicios (uno por año) e historia de múltiplos ≤ 100 años.
    "ACC-VAL-001": {"rango_anios_explicitos": [3, 10], "g_terminal_tope_pct": 4, "prm_respaldo_pct": 5,
                    "rango_prm_pct": [3, 7], "ejercicios_minimos": 3, "ejercicios_recomendados": 5,
                    "peso_vt_advertencia_pct": 85, "anios_percentil": 10, "sensibilidad_wacc_pp": 1,
                    "sensibilidad_g_pp": 0.5, "beta_respaldo": 1, "iteraciones_max": 100, "tol_inverso": 1e-6,
                    "ejercicios_maximos": 100, "anios_historia_maximos": 100},
    # ACC-ERP-001 · «Método (i)»: 5 años de flujo; «Parámetros»: g_L en [r_f − 1 pp, r_f], percentil mínimo 10 años;
    # «Entradas mínimas»: beneficios reales de 10 años para CAPE; «Tolerancias»: 1e-6 (iterativo). Tope [PROPUESTO]: 100.
    # Cota [PROPUESTO]: 100 años (ventana_percentil, historia y beneficios reales anuales).
    "ACC-ERP-001": {"anios_explicitos": 5, "amplitud_g_L_pp": 1, "anios_percentil_minimo": 10, "anios_cape": 10,
                    "iteraciones_max": 100, "tol": 1e-6, "anios_historia_maximos": 100},
    # ACC-FACT-001 · «Entradas mínimas»: ≥ 36 mensuales o 104 semanales; «Método»: factores de cada modelo y L de
    # Newey-West; «Supuestos»: t > 3 para afirmar un factor nuevo. Cota [PROPUESTO]: 100 años (fechas y ventana_movil).
    "ACC-FACT-001": {"observaciones_minimas": {"mensual": 36, "semanal": 104},
                     "periodos_por_anio": {"mensual": MESES_POR_ANIO, "semanal": SEMANAS_POR_ANIO},
                     "factores_modelo": {"FF5+UMD": ["MKT", "SMB", "HML", "RMW", "CMA", "UMD"],
                                         "FF3": ["MKT", "SMB", "HML"], "CAPM": ["MKT"]},
                     "adicionales_admitidos": ["QMJ", "BAB"], "t_factor_nuevo": 3, "anios_historia_maximos": 100},
    # FIR-PRICE-001 · «Parámetros»: delta_y 1–25 pb. «Tolerancias»: 1e-10 precio. Frecuencias y convenciones modelables
    # [PROPUESTO]: cupón anual, semestral, trimestral o mensual; ACT/ACT ICMA o 30E/360. Tope [PROPUESTO]: 100. Plazo
    # máximo [PROPUESTO]: 100 años (los bonos centenarios; con cupón mensual, ≤ 1 200 flujos y otros tantos rescates).
    "FIR-PRICE-001": {"rango_delta_y_pb": [1, 25], "frecuencias": [1, 2, 4, 12],
                      "convenciones": ["ACT/ACT-ICMA", "30E/360"], "tol_precio": 1e-10, "iteraciones_max": 100,
                      "plazo_maximo_anios": 100},
    # FIR-CURVE-001 · «Aclaración y rechazo»: < 6 nodos; «Entradas mínimas»: ≥ 8 para Svensson; «Método»: ≥ 20 arranques;
    # Diebold y Li (2006): λ = 0,0609 por mes. Tope de arranques [PROPUESTO]: 100 (5 × el valor por defecto); tope de
    # evaluaciones [PROPUESTO]: 100 por parámetro (el de scipy.optimize.least_squares). Pendientes 2s10s y 3m10y.
    # Cotas [PROPUESTO]: ≤ 100 nodos (un bono por nodo) y ≤ 1 040 curvas en la historia (20 años semanales, la ventana
    # de FIR-SPREAD-001): con las tres cotas, el ajuste más caro tarda unos segundos.
    "FIR-CURVE-001": {"nodos_minimos": 6, "nodos_minimos_nss": 8, "arranques_minimos": 20, "arranques_maximos": 100,
                      "lambda_diebold_li_mes": 0.0609, "evaluaciones_por_parametro": 100,
                      "tramos_pendiente": {"2s10s": [2, 10], "3m10y": [0.25, 10]}, "nodos_maximos": 100,
                      "historia_maxima": 1040},
    # FIR-CARRY-001 · «Parámetros»: delta_t 1–12 meses (el mismo rango que usa TCV-SLOPE-001). Cotas: ≤ 100 nodos de
    # curva (la de FIR-CURVE-001, de la que sale la curva) y ≤ 100 tramos [PROPUESTO] (uno por nodo).
    "FIR-CARRY-001": {"rango_delta_t": [1, 12], "nodos_maximos": 100, "tramos_maximos": 100},
    # FIR-SPREAD-001 · «Parámetros»: recuperación 0,2–0,6; ventana mínima 10. «Aclaración y rechazo»: < 5 años.
    # «Entradas mínimas»: ≥ 10 años (15 recomendados); «Método»: ≥ 15 años con una recesión. Cotas [PROPUESTO]: 100 años
    # (ventana e historia) y 22 ratings (la escala de largo plazo de AAA a D).
    "FIR-SPREAD-001": {"rango_recuperacion": [0.2, 0.6], "ventana_minima": 10, "anios_minimos": 5,
                       "anios_limitacion": 10, "anios_recomendados": 15, "anios_historia_maximos": 100,
                       "ratings_maximos": 22},
    # FX-MOM-001 · «Método»: retrospecciones hasta 12 meses y volatilidad implícita a 3 meses (la realizada se mide en la
    # misma ventana de 3 meses [PROPUESTO]); TSMOM a 12 meses (ACC-MOM-001); «Entradas mínimas»: ≥ 2 años. Cotas
    # [PROPUESTO]: 45 pares (los cruces del G10, el universo mayor que nombra el «Método») e historia ≤ 100 años.
    "FX-MOM-001": {"rango_retrospeccion": [1, 12], "meses_tsmom": 12, "anios_minimos": 2, "meses_vol": 3,
                   "pares_maximos": 45, "anios_historia_maximos": 100},
    # FX-PPA-001 · «Entradas mínimas»: ≥ 24 meses (≥ 20 años para la vida media). Periodicidades admitidas [PROPUESTO]:
    # mensual y trimestral. Cota [PROPUESTO]: 100 años (fechas, ventana en meses y suavizado en periodos mensuales).
    "FX-PPA-001": {"meses_minimos": 24, "anios_vida_media": 20, "periodicidades": {"mensual": 1, "trimestral": 3},
                   "anios_historia_maximos": 100},
    # DER-OPT-001 · «Entradas mínimas»: ≥ 5 precios de ejercicio por vencimiento; «Método»: risk reversal 25Δ.
    # tol_iv no más laxa que la de estimadores iterativos (3.2: 1e-6). Rango de pasos [PROPUESTO]: 2–1000 (Γ del árbol
    # necesita 2 pasos; tope de coste 2 × los 500 de la ficha).
    # Variación para vega y ρ en CRR [PROPUESTO]: ±1 punto (la unidad de la salida). Tope [PROPUESTO]: 100.
    # Cotas de tamaño [PROPUESTO]: 50 contratos por petición, de ellos ≤ 10 valorados con el árbol (americanas o modelo
    # CRR: con volatilidad implícita, unos 0,5 s cada uno a 1 000 pasos), y una superficie de ≤ 24 vencimientos con
    # ≤ 100 precios de ejercicio cada uno.
    "DER-OPT-001": {"strikes_minimos": 5, "delta_rr": 0.25, "tol_iv_maxima": 1e-6, "rango_pasos": [2, 1000],
                    "punto": 1, "iteraciones_max": 100, "contratos_maximos": 50, "contratos_arbol_maximos": 10,
                    "vencimientos_maximos": 24, "strikes_maximos": 100},
}

# «Supuestos y limitaciones» de cada ficha (literales): advertencias obligatorias de entrega.
ADVERTENCIAS: dict[str, list[str]] = {
    "ACC-VAL-001": ["no es precio objetivo", "valor terminal > 85 % ⇒ advertencia",
                    "sectores cíclicos con beneficios normalizados"],
    "ACC-ERP-001": ["sensible a g₅",
                    "comparar rendimiento del beneficio con rendimiento nominal es un error (no se ofrece)"],
    "ACC-FACT-001": ["factores de la región correcta", "α no significativo es lo habitual",
                     "t > 3 para afirmar un factor nuevo"],
    "FIR-PRICE-001": ["la duración modificada no vale en bonos con opciones", "breakeven ≠ inflación esperada pura"],
    "FIR-CURVE-001": ["no convexidad ⇒ mínimos locales", "extremos de la curva poco anclados",
                      "prima temporal no observable"],
    "FIR-CARRY-001": ["curva inalterada (supuesto, no previsión)",
                      "las forwards implican que el carry se neutraliza bajo expectativas puras"],
    "FIR-SPREAD-001": ["cambios de composición del índice alteran la comparabilidad",
                       "percentiles bajos pueden persistir"],
    "FX-MOM-001": ["colapsos del carry (asimetría negativa)", "intervenciones y controles de capital"],
    "FX-PPA-001": ["ancla de largo plazo (vida media habitual 3–5 años)", "no corrige Balassa-Samuelson",
                   "no es previsión ni valor objetivo"],
    "DER-OPT-001": ["probabilidades neutrales al riesgo ≠ reales", "BSM no captura sonrisa ni saltos",
                    "exóticos fuera de ficha"],
}

# Claves que el servicio añade a los parámetros (no son de la ficha): se ignoran.
_AJENOS = frozenset({"clase"})


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


def _bool(x: Any, que: str) -> bool:
    if not isinstance(x, (bool, np.bool_)):
        raise ErrorFicha(f"{que}: debe ser true o false")
    return bool(x)


def _texto(x: Any) -> bool:
    return isinstance(x, str) and bool(x.strip())


def _txt(x: Any, que: str) -> str:
    if not _texto(x):
        raise ErrorFicha(f"{que}: falta o no es un texto")
    return str(x).strip()


def _opcion(x: Any, que: str, admitidas: list[str] | tuple[str, ...]) -> str:
    if not isinstance(x, str) or x.strip() not in admitidas:
        raise ErrorFicha(f"{que}: «{str(x)[:40]}» no admitido ({', '.join(admitidas)})")
    return x.strip()


def _lista(x: Any, que: str, minimo: int = 0) -> list[Any]:
    if not isinstance(x, (list, tuple)):
        raise ErrorFicha(f"{que}: se esperaba una lista")
    if len(x) < minimo:
        raise ErrorFicha(f"{que}: {len(x)} elementos (< {minimo})")
    return list(x)


def _dict(x: Any, que: str) -> dict[str, Any]:
    if not isinstance(x, dict):
        raise ErrorFicha(f"{que}: se esperaba un objeto (dict)")
    return x


def _req(v: dict[str, Any], clave: str, F: str, que: str = "") -> Any:
    if not isinstance(v, dict) or v.get(clave) is None:
        raise ErrorFicha(f"{F}: falta «{clave}»{' (' + que + ')' if que else ''}")
    return v[clave]


def _vector(x: Any, que: str, minimo: int = 1) -> np.ndarray:
    lista = list(x) if isinstance(x, np.ndarray) else _lista(x, que)
    a = np.array([_num(e, que) for e in lista], dtype=float)
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


def _fechas(x: Any, que: str, minimo: int = 2) -> list[date]:
    f = [_fecha(e, que) for e in _lista(x, que)]
    if len(f) < minimo:
        raise ErrorFicha(f"{que}: {len(f)} fechas (< {minimo})")
    if any(b <= a for a, b in pairwise(f)):
        raise ErrorFicha(f"{que}: las fechas deben ser estrictamente crecientes")
    return f


def _anios(f0: date, f1: date) -> float:
    """Años entre dos fechas con recuento Real/365 (Catálogo 3.1)."""
    return (f1 - f0).days / DIAS_POR_ANIO


def _sumar_anios(f: date, anios: int) -> date:
    """La fecha `anios` años de calendario después (antes, si es negativo)."""
    return (pd.Timestamp(f) + pd.DateOffset(years=anios)).date()


def _tope(n: int, maximo: int, que: str) -> None:
    """QA r01 de T-112, H-01: cota superior de un tamaño de la petición (umbral fijo de la ficha)."""
    if n > maximo:
        raise ErrorFicha(f"{que}: {n} elementos (> {maximo}, cota de tamaño de la ficha)")


def _historia_acotada(fechas: list[date], anios: int, que: str) -> None:
    """QA r01 de T-112, H-01: una historia de más de `anios` años de calendario se rechaza (cota de tamaño)."""
    if fechas and fechas[0] < _sumar_anios(fechas[-1], -anios):
        raise ErrorFicha(f"{que}: historia de más de {anios} años ({fechas[0]} a {fechas[-1]}; cota de tamaño de la ficha)")


def _conocible(f: date, limite: date | None, que: str, referencia: str) -> None:
    """QA r01 de T-112, H-07: un dato fechado después de la fecha de corte o de la de valoración no era conocible
    (Catálogo 3.1, «Conocibilidad»): se rechaza, como hace el servicio con las series de HT-01 (FUGA_DE_INFORMACION)."""
    if limite is not None and f > limite:
        raise ErrorFicha(f"{que}: dato del {f} posterior a {referencia} ({limite}): no conocible")


def _con_fuente(d: Any, que: str) -> float:
    """Dato externo {'valor', 'fuente'}: sin fuente se rechaza."""
    if not isinstance(d, dict) or not _texto(d.get("fuente")):
        raise ErrorFicha(f"{que}: se espera {{'valor', 'fuente'}} con la fuente declarada")
    return _num(d.get("valor"), que)


def _serie(x: Any, que: str, minimo: int = 2) -> tuple[list[date], np.ndarray]:
    """Serie fechada: {"fechas": [...], "valores": [...]} o `pd.Series` con índice de fechas."""
    if isinstance(x, pd.Series):
        if not isinstance(x.index, pd.DatetimeIndex):
            raise ErrorFicha(f"{que}: se esperaba una serie con índice de fechas")
        x = x.dropna()
        fechas = _fechas([i.date() for i in x.index], que, minimo)
        return fechas, _vector(list(x.to_numpy()), que, minimo)
    d = _dict(x, que)
    fechas = _fechas(d.get("fechas"), f"{que}.fechas", minimo)
    valores = _vector(d.get("valores"), f"{que}.valores", minimo)
    if len(valores) != len(fechas):
        raise ErrorFicha(f"{que}: fechas y valores de distinta longitud")
    return fechas, valores


def _posicion(valor: float, historia: np.ndarray, que: str) -> dict[str, Any]:
    """Percentil (proporción de la historia ≤ valor) y z-score con desviación muestral; z = None sin dispersión."""
    h = np.asarray(historia, dtype=float)
    if len(h) < 2:
        raise ErrorFicha(f"{que}: historia insuficiente para percentil y z (< 2 observaciones)")
    sd = float(np.std(h, ddof=1)) if float(np.ptp(h)) > 0 else 0.0
    return {"valor": float(valor), "percentil": float(np.mean(h <= valor)),
            "z": float((valor - np.mean(h)) / sd) if sd > 0 else None, "media": float(np.mean(h)), "n": len(h)}


def _meses_entre(a: date, b: date) -> int:
    return (b.year - a.year) * MESES_POR_ANIO + (b.month - a.month)


def _hace_meses(f: date, meses: int) -> date:
    return (pd.Timestamp(f) - pd.DateOffset(months=meses)).date()


def _clave(x: float) -> str:
    """Clave de texto de un plazo o vencimiento: 0.25 → «0.25», 10.0 → «10»."""
    return f"{float(x):g}"


def _json(x: Any, ruta: str, malas: list[str]) -> Any:
    """Copia JSON del resultado; anota la ruta de cada número no finito."""
    if isinstance(x, dict):
        return {str(k): _json(v, f"{ruta}.{k}", malas) for k, v in x.items()}
    if isinstance(x, (list, tuple, np.ndarray)):
        return [_json(v, f"{ruta}[{i}]", malas) for i, v in enumerate(x)]
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        if not math.isfinite(float(x)):
            malas.append(ruta)
        return float(x)
    if isinstance(x, date):
        return x.isoformat()
    return x


def _parametros(F: str, params: dict[str, Any] | None) -> dict[str, Any]:
    """Parámetros de la petición encima de los de la ficha, validados. Un umbral de `UMBRALES` o un parámetro que la
    ficha no declara se rechazan."""
    params = _dict(params if params is not None else {}, f"{F}: parámetros")
    fijos = set(params) & set(UMBRALES[F])
    if fijos:
        raise ErrorFicha(f"{F}: {sorted(fijos)} son umbrales fijos de la ficha, no parámetros de la petición")
    desconocidos = set(params) - set(PARAMETROS_POR_DEFECTO[F]) - _AJENOS
    if desconocidos:
        raise ErrorFicha(f"{F}: parámetros no declarados en la ficha: {sorted(desconocidos)}")
    p = dict(PARAMETROS_POR_DEFECTO[F])
    p.update({k: v for k, v in params.items() if k in p and v is not None})
    _validar_parametros(F, p)
    return p


def _validar_parametros(F: str, p: dict[str, Any]) -> None:
    """Tipo y rango de cada parámetro (los rangos que dependen de los datos se comprueban en el manejador)."""
    u = UMBRALES[F]
    if F == "ACC-VAL-001":
        p["anios_explicitos"] = _entero(p["anios_explicitos"], f"{F}: anios_explicitos", *u["rango_anios_explicitos"])
        if p["g_terminal"] is not None:
            p["g_terminal"] = _rango(p["g_terminal"], f"{F}: g_terminal", 0)
        if p["PRM"] is not None:
            p["PRM"] = _rango(p["PRM"], f"{F}: PRM", *u["rango_prm_pct"])
        if p["tasa_impositiva"] is not None:
            p["tasa_impositiva"] = _rango(p["tasa_impositiva"], f"{F}: tasa_impositiva", 0, PCT, abierto_hi=True)
        p["enfoque"] = _opcion(p["enfoque"], f"{F}: enfoque", ("FCFF", "FCFE"))
    elif F == "ACC-ERP-001":
        if p["g_L"] is not None:
            p["g_L"] = _num(p["g_L"], f"{F}: g_L")
        p["incluir_recompras"] = _bool(p["incluir_recompras"], f"{F}: incluir_recompras")
        p["ventana_percentil"] = _rango(p["ventana_percentil"], f"{F}: ventana_percentil", u["anios_percentil_minimo"],
                                        u["anios_historia_maximos"])
    elif F == "ACC-FACT-001":
        p["modelo"] = _opcion(p["modelo"], f"{F}: modelo", tuple(u["factores_modelo"]))
        ad = _lista(p["adicionales"], f"{F}: adicionales")
        if len(set(map(str, ad))) != len(ad) or any(a not in u["adicionales_admitidos"] for a in ad):
            raise ErrorFicha(f"{F}: adicionales admitidos: {u['adicionales_admitidos']} (sin repetir)")
        p["adicionales"] = [str(a) for a in ad]
        p["frecuencia"] = _opcion(p["frecuencia"], f"{F}: frecuencia", tuple(u["observaciones_minimas"]))
        p["ventana_movil"] = _entero(p["ventana_movil"], f"{F}: ventana_movil", 1,
                                     u["anios_historia_maximos"] * MESES_POR_ANIO)
    elif F == "FIR-PRICE-001":
        if p["convencion"] is not None:
            p["convencion"] = _opcion(p["convencion"], f"{F}: convencion", tuple(u["convenciones"]))
        p["delta_y"] = _rango(p["delta_y"], f"{F}: delta_y", *u["rango_delta_y_pb"])
    elif F == "FIR-CURVE-001":
        p["modelo"] = _opcion(p["modelo"], f"{F}: modelo", ("auto", "NSS", "NS"))
        p["lambda"] = _opcion(p["lambda"], f"{F}: lambda", ("estimado", "diebold_li"))
        p["arranques"] = _entero(p["arranques"], f"{F}: arranques", u["arranques_minimos"], u["arranques_maximos"])
        p["semilla"] = _entero(p["semilla"], f"{F}: semilla", 0)
    elif F == "FIR-CARRY-001":
        p["delta_t"] = _rango(p["delta_t"], f"{F}: delta_t", *u["rango_delta_t"])
    elif F == "FIR-SPREAD-001":
        p["ventana"] = _rango(p["ventana"], f"{F}: ventana", u["ventana_minima"], u["anios_historia_maximos"])
        p["recuperacion"] = _rango(p["recuperacion"], f"{F}: recuperacion", *u["rango_recuperacion"])
        p["ajuste_composicion"] = _bool(p["ajuste_composicion"], f"{F}: ajuste_composicion")
    elif F == "FX-MOM-001":
        r = [_entero(x, f"{F}: retrospecciones", *u["rango_retrospeccion"])
             for x in _lista(p["retrospecciones"], f"{F}: retrospecciones", 1)]
        if len(set(r)) != len(r):
            raise ErrorFicha(f"{F}: retrospecciones repetidas")
        p["retrospecciones"] = sorted(r)
        p["volatilidad"] = _opcion(p["volatilidad"], f"{F}: volatilidad", ("implicita_3m", "realizada"))
    elif F == "FX-PPA-001":
        if p["ventana"] is not None:
            p["ventana"] = _entero(p["ventana"], f"{F}: ventana (meses)", u["meses_minimos"],
                                   u["anios_historia_maximos"] * MESES_POR_ANIO)
        p["base"] = _opcion(p["base"], f"{F}: base", ("primer_periodo", "media_largo_plazo"))
        if p["suavizado"] is not None:
            p["suavizado"] = _entero(p["suavizado"], f"{F}: suavizado (periodos de media móvil)", 1,
                                     u["anios_historia_maximos"] * MESES_POR_ANIO)
    elif F == "DER-OPT-001":
        p["modelo"] = _opcion(p["modelo"], f"{F}: modelo", ("BSM", "Black-76", "CRR"))
        p["pasos"] = _entero(p["pasos"], f"{F}: pasos", *u["rango_pasos"])
        p["tol_iv"] = _rango(p["tol_iv"], f"{F}: tol_iv", 0, u["tol_iv_maxima"], abierto_lo=True)
        p["densidad"] = _bool(p["densidad"], f"{F}: densidad")


def _cerrado(F: str) -> Callable[[Manejador], Callable[..., Resultado]]:
    """Falla cerrado en profundidad: entradas mal formadas o fuera de dominio y resultados no finitos → ErrorFicha.

    Traduce lo que se escape de cada manejador (aritmética fuera de dominio, tipos inesperados, fechas fuera de rango),
    rechaza cualquier NaN/inf del resultado y añade las advertencias obligatorias de la ficha."""
    def decorar(fn: Manejador) -> Callable[..., Resultado]:
        @wraps(fn)
        def envoltura(ent: Any, params: Any = None) -> Resultado:
            if not isinstance(ent, dict) or not isinstance(ent.get("valores", {}), dict):
                raise ErrorFicha(f"{F}: los datos en línea («valores») deben ser un objeto")
            if not isinstance(ent.get("series", {}), dict) or not isinstance(ent.get("series_rol", {}), dict):
                raise ErrorFicha(f"{F}: «series» y «series_rol» deben ser objetos")
            if params is not None and not isinstance(params, dict):
                raise ErrorFicha(f"{F}: los parámetros deben ser un objeto")
            # QA r01 de T-112, H-07: la fecha de corte que pone el servicio (texto AAAA-MM-DD o None) llega a la ficha
            corte = ent.get("fecha_corte")
            e = {"valores": ent.get("valores") or {}, "series": ent.get("series") or {},
                 "series_rol": ent.get("series_rol") or {},
                 "fecha_corte": None if corte is None else _fecha(corte, f"{F}: fecha_corte de la petición")}
            try:
                with np.errstate(all="ignore"):
                    res, lim = fn(e, params or {})
            except ErrorFicha:
                raise
            except (ArithmeticError, ValueError, TypeError, AttributeError, KeyError, IndexError, RuntimeError,
                    np.linalg.LinAlgError) as exc:
                raise ErrorFicha(f"{F}: entrada mal formada o fuera de dominio ({type(exc).__name__}: {exc})") from exc
            malas: list[str] = []
            limpio = _json(res, "resultado", malas)
            if malas:
                raise ErrorFicha(f"{F}: resultado no finito en {', '.join(malas[:3])} (entradas fuera de dominio)")
            limpio["advertencias"] = list(ADVERTENCIAS[F]) + [str(a) for a in limpio.get("advertencias") or []]
            return limpio, [str(x) for x in lim]
        return envoltura
    return decorar


def _raiz_creciente(g: Callable[[float], float], que: str, iteraciones: int, xtol: float) -> float:
    """Raíz de g creciente y continua en (0, ∞) con g(0⁺) < 0 < g(∞): acota doblando y partiendo por 2 desde 1 y
    resuelve con Brent. Rechaza si no acota o no converge en el tope de iteraciones."""
    hi = 1.0
    for _ in range(iteraciones):
        if g(hi) >= 0:
            break
        hi *= 2
    else:
        raise ErrorFicha(f"{que}: CONVERGENCIA (sin cota superior en {iteraciones} iteraciones)")
    lo = hi
    for _ in range(iteraciones):
        lo /= 2
        if g(lo) < 0:
            break
    else:
        raise ErrorFicha(f"{que}: CONVERGENCIA (sin cota inferior en {iteraciones} iteraciones)")
    if g(hi) == 0:
        return hi
    x, info = optimize.brentq(g, lo, hi, xtol=xtol, maxiter=iteraciones, full_output=True, disp=False)
    if not info.converged:
        raise ErrorFicha(f"{que}: CONVERGENCIA (Brent no converge en {iteraciones} iteraciones)")
    return float(x)


# ================================================================== FIR-PRICE-001
def _dias_30e(d1: date, d2: date) -> int:
    """Días 30E/360 (ICMA): cada mes de 30 días, el 31 cuenta como 30."""
    return (BASE_30E * (d2.year - d1.year) + MES_30E * (d2.month - d1.month)
            + (min(d2.day, MES_30E) - min(d1.day, MES_30E)))


def _calendario(liq: date, venc: date, f: int, F: str) -> list[date]:
    """Fechas de cupón hacia atrás desde el vencimiento: [cupón anterior ≤ liquidación, cupones siguientes…, venc]."""
    if venc <= liq:
        raise ErrorFicha(f"{F}: el vencimiento debe ser posterior a la liquidación")
    meses = MESES_POR_ANIO // f
    fechas = [venc]
    k = 1
    while fechas[-1] > liq:
        fechas.append((pd.Timestamp(venc) - pd.DateOffset(months=meses * k)).date())
        k += 1
    return fechas[::-1]


def bono(cupon_pct: float, f: int, liq: date, fechas: list[date], conv: str, reembolso: float = NOMINAL) -> dict[str, Any]:
    """Flujos de un bono a tipo fijo con amortización única: periodos t_k = w + k − 1 hasta `fechas[-1]`."""
    prev, sig = fechas[0], fechas[1]
    if conv == "ACT/ACT-ICMA":
        a = (liq - prev).days / (sig - prev).days
    else:
        a = _dias_30e(prev, liq) / (BASE_30E / f)
    n = len(fechas) - 1
    t = (1 - a) + np.arange(n, dtype=float)
    cf = np.full(n, NOMINAL * cupon_pct / PCT / f)
    cf[-1] += reembolso
    return {"t": t, "cf": cf, "f": f, "corrido": NOMINAL * cupon_pct / PCT / f * a, "cupon": cupon_pct,
            "fecha_fin": fechas[-1]}


def _v(y_pct: float, f: int) -> float:
    base = 1 + y_pct / PCT / f
    if not base > 0:
        raise ErrorFicha("FIR-PRICE-001: rendimiento ≤ −100 % · frecuencia (fuera de dominio)")
    return 1 / base


def precio_sucio(b: dict[str, Any], y_pct: float) -> float:
    """Precio sucio por 100 nominal: Σ CF_k / (1 + y/f)^{t_k}."""
    return float(np.sum(b["cf"] * _v(y_pct, b["f"]) ** b["t"]))


def sensibilidades(b: dict[str, Any], y_pct: float) -> dict[str, float]:
    """D_Macaulay y D_mod (años), convexidad (años²) y DV01 (por 100 nominal y pb)."""
    f, t, v = b["f"], b["t"], _v(y_pct, b["f"])
    pv = b["cf"] * v ** t
    P = float(np.sum(pv))
    d_mac = float(np.sum(t * pv)) / P / f
    d_mod = d_mac * v
    conv = float(np.sum(t * (t + 1) * pv)) * v * v / P / (f * f)
    return {"d_macaulay": d_mac, "d_mod": d_mod, "convexidad": conv, "dv01": d_mod * P / PB_POR_UNIDAD}


def rendimiento(b: dict[str, Any], sucio: float, u: dict[str, Any], F: str = "FIR-PRICE-001") -> float:
    """Rendimiento (% anual, capitalización f) que iguala el precio sucio: Newton sobre v = 1/(1 + y/f) desde el cupón,
    con respaldo de Brent. El precio es creciente en v, así que la raíz es única."""
    t, cf, f = b["t"], b["cf"], b["f"]
    tol = u["tol_precio"] * sucio

    def g(v: float) -> float:
        return float(np.sum(cf * v ** t)) - sucio

    v = 1 / (1 + b["cupon"] / PCT / f)
    for _ in range(u["iteraciones_max"]):
        gv = g(v)
        if abs(gv) <= tol:
            return (1 / v - 1) * f * PCT
        d = float(np.sum(cf * t * v ** (t - 1)))
        nuevo = v - gv / d if d > 0 else float("nan")
        if not (math.isfinite(nuevo) and nuevo > 0):
            break
        v = nuevo
    v = _raiz_creciente(g, f"{F}: rendimiento", u["iteraciones_max"], np.finfo(float).eps)
    if abs(g(v)) > tol:
        raise ErrorFicha(f"{F}: CONVERGENCIA (el rendimiento no reproduce el precio con la tolerancia de la ficha)")
    return (1 / v - 1) * f * PCT


@_cerrado("FIR-PRICE-001")
def f_fir_price(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """FIR-PRICE-001 · Precio, rendimiento, duración y convexidad del bono genérico de un tramo o segmento.

    ``valores``: ``cupon`` (% anual), ``frecuencia`` (1, 2, 4 o 12), ``vencimiento`` y ``liquidacion`` (ISO),
    ``convencion`` (ACT/ACT-ICMA o 30E/360; o en los parámetros), y ``precio_limpio`` (por 100) **o** ``rendimiento``
    (%). Opcionales: ``estructura`` («bullet»: tipo fijo y amortización única; otra se rechaza), ``rescates``
    [{"fecha": cupón, "precio": por 100}] para YTW y duración efectiva al peor (exige precio limpio),
    ``ligado_inflacion`` (true: el rendimiento es real y la duración es real) y ``rendimiento_nominal_comparable``
    ({"valor": %, "fuente"}) para el breakeven del ligado.
    """
    F = "FIR-PRICE-001"
    p = _parametros(F, params)
    u = UMBRALES[F]
    v = ent["valores"]
    lim: list[str] = []
    estructura = v.get("estructura", "bullet")
    if estructura != "bullet":
        raise ErrorFicha(f"{F}: flujos no modelables en ficha (estructura «{str(estructura)[:30]}»; solo «bullet»)")
    conv_d, conv_p = v.get("convencion"), p["convencion"]
    if conv_d is None and conv_p is None:
        raise ErrorFicha(f"{F}: aclaración requerida: falta la convención de días")
    if conv_d is not None and conv_p is not None and conv_d != conv_p:
        raise ErrorFicha(f"{F}: aclaración requerida: convención de los datos y de los parámetros distintas")
    conv = _opcion(conv_d if conv_d is not None else conv_p, f"{F}: convencion", tuple(u["convenciones"]))
    cupon = _rango(_req(v, "cupon", F), f"{F}: cupon", 0)
    f = _entero(_req(v, "frecuencia", F), f"{F}: frecuencia")
    if f not in u["frecuencias"]:
        raise ErrorFicha(f"{F}: frecuencia {f} no modelable en ficha (admitidas {u['frecuencias']})")
    liq = _fecha(_req(v, "liquidacion", F), f"{F}: liquidacion")
    venc = _fecha(_req(v, "vencimiento", F), f"{F}: vencimiento")
    if venc > _sumar_anios(liq, u["plazo_maximo_anios"]):   # QA r01 de T-112, H-01: ≤ 1 200 flujos
        raise ErrorFicha(f"{F}: vencimiento a más de {u['plazo_maximo_anios']} años de la liquidación (cota de tamaño)")
    corte = ent["fecha_corte"]
    if corte is not None and liq > corte:   # H-07: la liquidación es un dato del contrato (T + n), no una observación
        lim.append(f"liquidación ({liq}) posterior a la fecha de corte ({corte}): el precio o el rendimiento aportado debe "
                   "ser el conocido en la fecha de corte para liquidar en esa fecha")
    fechas = _calendario(liq, venc, f, F)
    b = bono(cupon, f, liq, fechas, conv)
    tiene_p, tiene_y = v.get("precio_limpio") is not None, v.get("rendimiento") is not None
    if tiene_p == tiene_y:
        raise ErrorFicha(f"{F}: aclaración requerida: aporte el precio limpio o el rendimiento (uno de los dos)")
    if tiene_p:
        limpio = _rango(v["precio_limpio"], f"{F}: precio_limpio", 0, abierto_lo=True)
        sucio = limpio + b["corrido"]
        ytm = rendimiento(b, sucio, u)
    else:
        ytm = _num(v["rendimiento"], f"{F}: rendimiento")
        sucio = precio_sucio(b, ytm)
        limpio = sucio - b["corrido"]
    ida_vuelta = abs(precio_sucio(b, rendimiento(b, sucio, u)) - sucio) / sucio
    s = sensibilidades(b, ytm)

    # YTW y efectivas (precio al peor) con calendario de rescates
    escenarios: list[dict[str, Any]] = [{"fecha": venc, "bono": b, "rendimiento": ytm}]
    rescates = v.get("rescates")
    if rescates is not None:
        if not tiene_p:
            raise ErrorFicha(f"{F}: aclaración requerida: con calendario de rescates se necesita el precio limpio")
        for i, r in enumerate(_lista(rescates, f"{F}: rescates", 1)):
            r = _dict(r, f"{F}: rescates[{i}]")
            fr = _fecha(_req(r, "fecha", F), f"{F}: rescates[{i}].fecha")
            pr = _rango(_req(r, "precio", F), f"{F}: rescates[{i}].precio", 0, abierto_lo=True)
            if fr not in fechas[1:-1]:
                raise ErrorFicha(f"{F}: rescate {fr} fuera de una fecha de cupón futura: flujos no modelables en ficha")
            if any(e["fecha"] == fr for e in escenarios):   # H-01: ≤ un rescate por fecha de cupón
                raise ErrorFicha(f"{F}: rescate {fr} repetido en el calendario de rescates")
            br = bono(cupon, f, liq, fechas[:fechas.index(fr) + 1], conv, reembolso=pr)
            escenarios.append({"fecha": fr, "bono": br, "rendimiento": rendimiento(br, sucio, u)})
    peor = min(escenarios, key=lambda e: e["rendimiento"])
    ytw = float(peor["rendimiento"])
    dy = p["delta_y"] / PB_POR_PUNTO

    def p_peor(y: float) -> float:
        return min(precio_sucio(e["bono"], y) for e in escenarios)

    p0, pm, pp = p_peor(ytw), p_peor(ytw - dy), p_peor(ytw + dy)
    dy_u = p["delta_y"] / PB_POR_UNIDAD
    efectivas = {"duracion": (pm - pp) / (2 * p0 * dy_u), "convexidad": (pm + pp - 2 * p0) / (p0 * dy_u * dy_u),
                 "delta_y_pb": p["delta_y"],
                 "metodo": "precio al peor (sin modelo de opción)" if len(escenarios) > 1 else "reprecio ±Δy"}
    if len(escenarios) > 1:
        lim.append("duración y convexidad efectivas por precio al peor (sin modelo de opción ni curva) [PROPUESTO]")

    # Ligado a inflación: duración real y breakeven con su bono nominal
    ligado = _bool(v.get("ligado_inflacion", False), f"{F}: ligado_inflacion")
    breakeven = None
    if ligado:
        nominal = v.get("rendimiento_nominal_comparable")
        if nominal is not None:
            breakeven = (_con_fuente(nominal, f"{F}: rendimiento_nominal_comparable") - ytm) * PB_POR_PUNTO
        else:
            lim.append("sin rendimiento del bono nominal comparable: breakeven no calculado")
    elif v.get("rendimiento_nominal_comparable") is not None:
        raise ErrorFicha(f"{F}: el breakeven solo se calcula para un bono ligado a inflación")

    # Segunda vía: aproximación por duración + convexidad frente al reprecio exacto (+Δy)
    exacto = precio_sucio(b, ytm + dy) - sucio
    orden1 = -s["d_mod"] * sucio * dy_u
    orden2 = orden1 + 0.5 * s["convexidad"] * sucio * dy_u * dy_u
    return {"precio_limpio": limpio, "precio_sucio": sucio, "cupon_corrido": b["corrido"], "ytm_pct": ytm,
            "ytw_pct": ytw, "fecha_peor": peor["fecha"], **s,
            "duracion_real": s["d_mod"] if ligado else None, "breakeven_pb": breakeven, "efectivas": efectivas,
            "flujos": len(b["cf"]), "convencion": conv, "frecuencia": f,
            "segunda_via": {"delta_y_pb": p["delta_y"], "variacion_exacta": exacto, "aprox_duracion": orden1,
                            "aprox_duracion_convexidad": orden2, "error_duracion": abs(orden1 - exacto),
                            "error_duracion_convexidad": abs(orden2 - exacto)},
            "verificacion": {"error_ida_vuelta_precio": ida_vuelta}}, lim


# ================================================================== FIR-CURVE-001
def _l1(x: np.ndarray) -> np.ndarray:
    """(1 − e^{−x})/x, con límite 1 en x = 0 y 0 en x = ∞."""
    x = np.asarray(x, dtype=float)
    return np.divide(-np.expm1(-x), x, out=np.ones_like(x), where=x > 0)


def _l2(x: np.ndarray) -> np.ndarray:
    """(1 − e^{−x})/x − e^{−x}."""
    return _l1(x) - np.exp(-np.asarray(x, dtype=float))


def nss_rendimiento(tau: Any, betas: Any, lambdas: Any) -> np.ndarray:
    """Curva cupón cero NS (3 β, 1 λ) o NSS (4 β, 2 λ) en %: y(τ) = β₀ + β₁·L₁(τ/λ₁) + β₂·L₂(τ/λ₁) [+ β₃·L₂(τ/λ₂)]."""
    tau = np.asarray(tau, dtype=float)
    b, lam = np.asarray(betas, dtype=float), np.asarray(lambdas, dtype=float)
    x1 = tau / lam[0]
    y = b[0] + b[1] * _l1(x1) + b[2] * _l2(x1)
    if len(lam) > 1:
        y = y + b[3] * _l2(tau / lam[1])
    return np.asarray(y, dtype=float)


def nss_forward(tau: Any, betas: Any, lambdas: Any) -> np.ndarray:
    """Forward instantáneo en % (τ finito): β₀ + β₁e^{−x₁} + β₂x₁e^{−x₁} [+ β₃x₂e^{−x₂}]."""
    tau = np.asarray(tau, dtype=float)
    b, lam = np.asarray(betas, dtype=float), np.asarray(lambdas, dtype=float)
    x1 = tau / lam[0]
    f = b[0] + b[1] * np.exp(-x1) + b[2] * x1 * np.exp(-x1)
    if len(lam) > 1:
        x2 = tau / lam[1]
        f = f + b[3] * x2 * np.exp(-x2)
    return np.asarray(f, dtype=float)


def _diseno(tau: np.ndarray, lam: np.ndarray) -> np.ndarray:
    cols = [np.ones_like(tau), _l1(tau / lam[0]), _l2(tau / lam[0])]
    if len(lam) > 1:
        cols.append(_l2(tau / lam[1]))
    return np.column_stack(cols)


def _ajuste_desde(tau: np.ndarray, y: np.ndarray, x0: np.ndarray, k: int, max_nfev: int) -> Any:
    """Mínimos cuadrados no lineales (trf) en (β, ln λ) con β₀ ≥ 0; devuelve el resultado de scipy o None."""
    nb = len(x0) - k

    def resid(x: np.ndarray) -> np.ndarray:
        return nss_rendimiento(tau, x[:nb], np.exp(x[nb:])) - y

    lb = np.full(len(x0), -np.inf)
    lb[0] = 0.0
    x0 = np.array(x0, dtype=float)
    x0[0] = max(x0[0], np.finfo(float).eps)
    r = optimize.least_squares(resid, x0, bounds=(lb, np.full(len(x0), np.inf)), method="trf", max_nfev=max_nfev)
    if r.status <= 0 or not np.all(np.isfinite(r.x)) or not math.isfinite(float(r.cost)):
        return None
    return r


def ajustar_curva(tau: np.ndarray, y: np.ndarray, modelo: str, lam_fijo: float | None, arranques: int, semilla: int,
                  u: dict[str, Any], F: str = "FIR-CURVE-001") -> dict[str, Any]:
    """Ajuste NS/NSS: λ fijo (Diebold-Li) por MCO, o ≥ 20 arranques con semilla (λ log-uniformes entre el plazo
    mínimo y el máximo; β de MCO dado λ) y se queda el de menor suma de cuadrados entre los que convergen."""
    k = 2 if modelo == "NSS" else 1
    if lam_fijo is not None:
        lam = np.array([lam_fijo])
        beta = np.linalg.lstsq(_diseno(tau, lam), y, rcond=None)[0]
        res = {"betas": beta, "lambdas": lam, "convergidos": 1}
    else:
        rng = np.random.default_rng(semilla)
        max_nfev = u["evaluaciones_por_parametro"] * (2 + 2 * k)   # NS: 3 β + 1 λ; NSS: 4 β + 2 λ
        mejor, n_ok = None, 0
        for _ in range(arranques):
            s = rng.uniform(math.log(tau[0]), math.log(tau[-1]), size=k)
            b0 = np.linalg.lstsq(_diseno(tau, np.exp(s)), y, rcond=None)[0]
            r = _ajuste_desde(tau, y, np.concatenate([b0, s]), k, max_nfev)
            if r is None:
                continue
            n_ok += 1
            if mejor is None or r.cost < mejor.cost:
                mejor = r
        if mejor is None:
            raise ErrorFicha(f"{F}: CONVERGENCIA (ningún arranque converge en el tope de evaluaciones)")
        nb = 3 + (k - 1)
        res = {"betas": mejor.x[:nb], "lambdas": np.exp(mejor.x[nb:]), "convergidos": n_ok}
    if not res["betas"][0] > 0:
        raise ErrorFicha(f"{F}: la restricción β₀ > 0 no se cumple con esta curva (ajuste no válido)")
    if not np.all(res["lambdas"] > 0) or not np.all(np.isfinite(res["lambdas"])):
        raise ErrorFicha(f"{F}: la restricción λ > 0 no se cumple con esta curva (ajuste no válido)")
    res["residuos"] = y - nss_rendimiento(tau, res["betas"], res["lambdas"])
    return res


@_cerrado("FIR-CURVE-001")
def f_fir_curve(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """FIR-CURVE-001 · Curva Nelson-Siegel(-Svensson) y valor relativo.

    ``valores``: ``curva`` = {"fecha": ISO, "plazos": [años > 0, crecientes], "rendimientos": [% cupón cero]} (≥ 6
    nodos; ≥ 8 para NSS). Opcional ``historia`` = {"fechas": [ISO], "rendimientos": [[% por nodo] por fecha]} con los
    mismos plazos, para el z-score de los residuos y el percentil de las pendientes (cada fecha se ajusta desde la
    solución de la anterior).
    """
    F = "FIR-CURVE-001"
    p = _parametros(F, params)
    u = UMBRALES[F]
    v = ent["valores"]
    lim: list[str] = []
    curva = _dict(_req(v, "curva", F), f"{F}: curva")
    fecha = _fecha(_req(curva, "fecha", F), f"{F}: curva.fecha")
    _conocible(fecha, ent["fecha_corte"], f"{F}: curva.fecha", "la fecha de corte")
    tau = _vector(curva.get("plazos"), f"{F}: curva.plazos")
    y = _vector(curva.get("rendimientos"), f"{F}: curva.rendimientos")
    if len(tau) != len(y):
        raise ErrorFicha(f"{F}: plazos y rendimientos de distinta longitud")
    if len(tau) < u["nodos_minimos"]:
        raise ErrorFicha(f"{F}: {len(tau)} nodos (< {u['nodos_minimos']}): rechazo de la ficha")
    _tope(len(tau), u["nodos_maximos"], f"{F}: curva.plazos")
    if np.any(tau <= 0) or np.any(np.diff(tau) <= 0):
        raise ErrorFicha(f"{F}: los plazos deben ser positivos y estrictamente crecientes")
    modelo = p["modelo"]
    if modelo == "auto":
        modelo = "NSS" if len(tau) >= u["nodos_minimos_nss"] else "NS"
    if modelo == "NSS" and len(tau) < u["nodos_minimos_nss"]:
        raise ErrorFicha(f"{F}: Svensson exige ≥ {u['nodos_minimos_nss']} nodos ({len(tau)})")
    lam_fijo = None
    if p["lambda"] == "diebold_li":
        if modelo != "NS":
            raise ErrorFicha(f"{F}: λ fijo de Diebold-Li solo con el modelo NS")
        lam_fijo = 1 / (u["lambda_diebold_li_mes"] * MESES_POR_ANIO)
    aj = ajustar_curva(tau, y, modelo, lam_fijo, p["arranques"], p["semilla"], u)
    b, lam = aj["betas"], aj["lambdas"]
    resid_pb = aj["residuos"] * PB_POR_PUNTO
    rmse = float(np.sqrt(np.mean(resid_pb ** 2)))

    def pendientes(bb: np.ndarray, ll: np.ndarray) -> dict[str, float | None]:
        out: dict[str, float | None] = {}
        for nombre, (a, c) in u["tramos_pendiente"].items():
            if a < tau[0] or c > tau[-1]:
                out[nombre] = None
            else:
                ya, yc = nss_rendimiento([a, c], bb, ll)
                out[nombre] = float(yc - ya) * PB_POR_PUNTO
        return out

    pend = pendientes(b, lam)
    for nombre, x in pend.items():
        if x is None:
            lim.append(f"pendiente {nombre} fuera del rango de nodos: no se extrapola")

    # Historia: residuos por nodo y pendientes ajustadas en cada fecha (arranque en la solución anterior)
    z_res: dict[str, float | None] = {_clave(t): None for t in tau}
    perc: dict[str, dict[str, Any] | None] = {n: None for n in pend}
    n_hist = 0
    hist = v.get("historia")
    if hist is not None:
        hist = _dict(hist, f"{F}: historia")
        fh = _fechas(hist.get("fechas"), f"{F}: historia.fechas", 2)
        filas = _lista(hist.get("rendimientos"), f"{F}: historia.rendimientos")
        if len(filas) != len(fh):
            raise ErrorFicha(f"{F}: historia: fechas y filas de distinta longitud")
        _tope(len(fh), u["historia_maxima"], f"{F}: historia.fechas")
        if fh[-1] >= fecha:
            raise ErrorFicha(f"{F}: la historia debe ser anterior a la fecha de la curva")
        k = len(lam)
        x_h = np.concatenate([b, np.log(lam)])
        max_nfev = u["evaluaciones_por_parametro"] * len(x_h)
        res_h, pend_h, fallidas = [], [], 0
        for i, fila in enumerate(filas):
            yh = _vector(fila, f"{F}: historia.rendimientos[{i}]")
            if len(yh) != len(tau):
                raise ErrorFicha(f"{F}: historia: la fila {i} no tiene un rendimiento por plazo")
            if lam_fijo is not None:
                bh = np.linalg.lstsq(_diseno(tau, lam), yh, rcond=None)[0]
                lh = lam
            else:
                r = _ajuste_desde(tau, yh, x_h, k, max_nfev)
                if r is None or not r.x[0] > 0:
                    fallidas += 1
                    continue
                x_h = r.x
                bh, lh = r.x[:len(b)], np.exp(r.x[len(b):])
            res_h.append((yh - nss_rendimiento(tau, bh, lh)) * PB_POR_PUNTO)
            pend_h.append(pendientes(bh, lh))
        if fallidas:
            lim.append(f"historia: {fallidas} fechas sin ajuste convergente, excluidas")
        n_hist = len(res_h)
        if n_hist >= 2:
            R = np.vstack(res_h)
            for j, t in enumerate(tau):
                z_res[_clave(t)] = _posicion(float(resid_pb[j]), R[:, j], F)["z"]
            for nombre, x_act in pend.items():
                serie = [ph[nombre] for ph in pend_h if ph[nombre] is not None]
                if x_act is not None and len(serie) >= 2:
                    perc[nombre] = _posicion(x_act, np.array(serie), F)
        else:
            lim.append("historia con < 2 ajustes: sin z-scores ni percentiles")
    else:
        lim.append("sin historia de curvas: z-scores de residuos y percentiles de pendientes no calculados")

    # Segunda vía: interpolación lineal de los nodos (bootstrapping lineal de una curva cupón cero)
    medios = (tau[:-1] + tau[1:]) / 2
    dif = (nss_rendimiento(medios, b, lam) - np.interp(medios, tau, y)) * PB_POR_PUNTO
    nombres = ["beta0", "beta1", "beta2", "beta3"][:len(b)]
    return {"fecha": fecha, "modelo": modelo, "parametros": {**dict(zip(nombres, map(float, b))),
                                                            **{f"lambda{i + 1}": float(x) for i, x in enumerate(lam)}},
            "rmse_pb": rmse, "residuos_pb": {_clave(t): float(r) for t, r in zip(tau, resid_pb)},
            "z_residuos": z_res, "pendientes_pb": pend, "percentiles_pendientes": perc,
            "curva": {"plazos": tau, "cero_pct": nss_rendimiento(tau, b, lam), "forward_pct": nss_forward(tau, b, lam)},
            "segunda_via": {"metodo": "interpolación lineal de los nodos", "plazos_medios": medios,
                            "diferencia_nss_menos_lineal_pb": dif, "max_abs_pb": float(np.max(np.abs(dif)))},
            "verificacion": {"y_tau_0": float(nss_rendimiento([0.0], b, lam)[0]),
                             "y_tau_infinito": float(nss_rendimiento([np.inf], b, lam)[0])},
            "arranques": p["arranques"] if lam_fijo is None else 0, "arranques_convergidos": aj["convergidos"],
            "semilla": p["semilla"], "n_historia": n_hist}, lim


# ================================================================== FIR-CARRY-001
def _curva_funcion(v: dict[str, Any], F: str) -> tuple[Callable[[float], float], str]:
    """Curva de entrada: nodos {"plazos", "rendimientos"} (interpolación lineal, sin extrapolar) o parámetros de
    FIR-CURVE-001 {"nss": {"beta0"…, "lambda1"…, "fuente"}}. Devuelve (y(τ) en %, origen)."""
    if v.get("nss") is not None:
        d = _dict(v["nss"], f"{F}: nss")
        _txt(d.get("fuente"), f"{F}: nss.fuente")
        lam = [_rango(d[k], f"{F}: nss.{k}", 0, abierto_lo=True) for k in ("lambda1", "lambda2") if d.get(k) is not None]
        betas = [_num(d[k], f"{F}: nss.{k}") for k in ("beta0", "beta1", "beta2", "beta3") if d.get(k) is not None]
        if not lam or len(betas) != 2 + len(lam):
            raise ErrorFicha(f"{F}: nss: NS = beta0–beta2 y lambda1; NSS = beta0–beta3, lambda1 y lambda2")
        return (lambda t: float(nss_rendimiento([t], betas, lam)[0])), "FIR-CURVE-001"
    c = _dict(_req(v, "curva", F, "nodos o parámetros NSS de FIR-CURVE-001"), f"{F}: curva")
    pl = _vector(c.get("plazos"), f"{F}: curva.plazos", 2)
    rd = _vector(c.get("rendimientos"), f"{F}: curva.rendimientos", 2)
    if len(pl) != len(rd) or np.any(pl < 0) or np.any(np.diff(pl) <= 0):
        raise ErrorFicha(f"{F}: curva: plazos no negativos y estrictamente crecientes, uno por rendimiento")
    _tope(len(pl), UMBRALES[F]["nodos_maximos"], f"{F}: curva.plazos")

    def y(t: float) -> float:
        if t < pl[0] or t > pl[-1]:
            raise ErrorFicha(f"{F}: el plazo {t:g} queda fuera de la curva [{pl[0]:g}, {pl[-1]:g}]; no se extrapola")
        return float(np.interp(t, pl, rd))
    return y, "nodos"


def carry_tramo(y: Callable[[float], float], tau: float, dt: float, fin_pct: float) -> dict[str, float]:
    """Carry = (y − financiación)·Δt; rolldown = −D_mod·[y(τ − Δt) − y(τ)] con D_mod = τ/(1 + y) del nodo cupón
    cero; total; subida de equilibrio = total/D_mod. Tantos por uno (la misma fórmula que TCV-SLOPE-001)."""
    yt, yr = y(tau) / PCT, y(tau - dt) / PCT
    if not 1 + yt > 0:
        raise ErrorFicha("FIR-CARRY-001: tipo ≤ −100 % en el tramo")
    d_mod = tau / (1 + yt)
    carry = (yt - fin_pct / PCT) * dt
    rolldown = -d_mod * (yr - yt)
    total = carry + rolldown
    return {"carry": carry, "rolldown": rolldown, "total": total, "d_mod": d_mod, "subida_equilibrio": total / d_mod,
            "y": yt, "y_rolldown": yr}


@_cerrado("FIR-CARRY-001")
def f_fir_carry(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """FIR-CARRY-001 · Carry y rolldown de un tramo con la curva estable.

    ``valores``: curva (``curva`` con nodos en % o ``nss`` de FIR-CURVE-001), ``tramo`` (años; o lista),
    ``financiacion`` (% anual: repo o tipo a corto) y, opcional, ``volatilidad_rendimiento_pb`` (volatilidad anual del
    rendimiento, pb) para carry/volatilidad.
    """
    F = "FIR-CARRY-001"
    p = _parametros(F, params)
    v = ent["valores"]
    lim: list[str] = []
    if v.get("financiacion") is None:
        raise ErrorFicha(f"{F}: aclaración requerida: falta la financiación (repo o tipo a corto)")
    fin = _num(v["financiacion"], f"{F}: financiacion")
    y, origen = _curva_funcion(v, F)
    tramos = v.get("tramo")
    lista = _lista(tramos, f"{F}: tramo", 1) if isinstance(tramos, (list, tuple)) else [_req(v, "tramo", F)]
    _tope(len(lista), UMBRALES[F]["tramos_maximos"], f"{F}: tramo")
    dt = p["delta_t"] / MESES_POR_ANIO
    vol = v.get("volatilidad_rendimiento_pb")
    sigma = None if vol is None else _rango(vol, f"{F}: volatilidad_rendimiento_pb", 0, abierto_lo=True) / PB_POR_UNIDAD
    if sigma is None:
        lim.append("sin volatilidad del rendimiento: carry/volatilidad no calculado")
    salida: dict[str, Any] = {}
    for t in lista:
        tau = _rango(t, f"{F}: tramo", 0, abierto_lo=True)
        if tau <= dt:
            raise ErrorFicha(f"{F}: el tramo ({tau:g} años) vence antes del horizonte Δt ({dt:g} años)")
        c = carry_tramo(y, tau, dt, fin)
        p0 = (1 + c["y"]) ** -tau
        p1 = (1 + c["y_rolldown"]) ** -(tau - dt)
        exacto = p1 / p0 - 1 - fin / PCT * dt
        salida[f"{tau:g}"] = {
            "carry_pb": c["carry"] * PB_POR_UNIDAD, "carry_pct": c["carry"] * PCT,
            "rolldown_pb": c["rolldown"] * PB_POR_UNIDAD, "rolldown_pct": c["rolldown"] * PCT,
            "total_pb": c["total"] * PB_POR_UNIDAD, "total_pct": c["total"] * PCT,
            "subida_equilibrio_pb": c["subida_equilibrio"] * PB_POR_UNIDAD, "d_mod": c["d_mod"],
            "carry_volatilidad": None if sigma is None else c["total"] / (c["d_mod"] * sigma * math.sqrt(dt)),
            "segunda_via": {"metodo": "reprecio del cupón cero a t + Δt con la curva inalterada",
                            "rentabilidad_exceso_pb": exacto * PB_POR_UNIDAD,
                            "diferencia_pb": (exacto - c["total"]) * PB_POR_UNIDAD}}
    return {"curva": origen, "delta_t_meses": p["delta_t"], "financiacion_pct": fin, "tramos": salida}, lim


# ================================================================== FIR-SPREAD-001
@_cerrado("FIR-SPREAD-001")
def f_fir_spread(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """FIR-SPREAD-001 · Percentil y valor del diferencial de crédito.

    ``valores``: ``historia`` = {"fechas": [ISO, semanales], "diferenciales_pb": [...], opcional "duraciones": [años]}
    (el último es el actual); ``impagos`` = {"fuente", "pd_anual"} o {"fuente", "por_rating": {rating: {"pd_anual",
    "peso"}}} (tantos por uno); opcionales ``duracion_diferencial`` (años) para la ampliación de equilibrio,
    ``medida`` (OAS o Z-spread) e ``incluye_recesion`` (true si la ventana contiene una recesión).
    """
    F = "FIR-SPREAD-001"
    p = _parametros(F, params)
    u = UMBRALES[F]
    v = ent["valores"]
    lim: list[str] = []
    h = _dict(_req(v, "historia", F), f"{F}: historia")
    fechas = _fechas(h.get("fechas"), f"{F}: historia.fechas")
    _historia_acotada(fechas, u["anios_historia_maximos"], f"{F}: historia.fechas")
    _conocible(fechas[-1], ent["fecha_corte"], f"{F}: historia.fechas", "la fecha de corte")
    s = _vector(h.get("diferenciales_pb"), f"{F}: historia.diferenciales_pb", 2)
    if len(s) != len(fechas):
        raise ErrorFicha(f"{F}: historia: fechas y diferenciales de distinta longitud")
    imp = _dict(_req(v, "impagos", F, "tasas de impago por rating"), f"{F}: impagos")
    _txt(imp.get("fuente"), f"{F}: impagos.fuente")
    if imp.get("por_rating") is not None:
        filas = _dict(imp["por_rating"], f"{F}: impagos.por_rating")
        if not filas:
            raise ErrorFicha(f"{F}: impagos.por_rating vacío")
        _tope(len(filas), u["ratings_maximos"], f"{F}: impagos.por_rating")
        pesos = np.array([_rango(_dict(x, f"{F}: {r}").get("peso"), f"{F}: {r}.peso", 0) for r, x in filas.items()])
        pds = np.array([_rango(x.get("pd_anual"), f"{F}: {r}.pd_anual", 0, 1) for r, x in filas.items()])
        if not math.isclose(float(pesos.sum()), 1.0, rel_tol=0, abs_tol=FICHAS_TOL[F]):
            raise ErrorFicha(f"{F}: los pesos por rating deben sumar 1")
        pd_anual = float(pesos @ pds)
    else:
        pd_anual = _rango(imp.get("pd_anual"), f"{F}: impagos.pd_anual", 0, 1)
    medida = v.get("medida")
    if medida is None:
        lim.append("medida del diferencial no declarada (OAS o Z-spread)")
    else:
        _opcion(medida, f"{F}: medida", ("OAS", "Z-spread"))

    # Ventana: los últimos `ventana` años (Real/365) de la historia
    idx = [i for i, f in enumerate(fechas) if _anios(f, fechas[-1]) <= p["ventana"]]
    fw, sw = [fechas[i] for i in idx], s[idx]
    anios = _anios(fw[0], fw[-1])
    if anios < u["anios_minimos"]:
        raise ErrorFicha(f"{F}: historia de {anios:.2f} años (< {u['anios_minimos']}): rechazo de la ficha")
    if anios < u["anios_limitacion"]:
        lim.append(f"historia de {anios:.2f} años (< {u['anios_limitacion']}): percentil orientativo")
    elif anios < u["anios_recomendados"]:
        lim.append(f"historia de {anios:.2f} años (< {u['anios_recomendados']} recomendados)")
    if v.get("incluye_recesion") is not True:
        lim.append("no consta que la ventana incluya una recesión")
    if float(np.median(np.diff([f.toordinal() for f in fw]))) > DIAS_POR_SEMANA:
        lim.append("frecuencia menor que semanal")
    actual = float(sw[-1])
    pos = _posicion(actual, sw, F)
    ajustado = None
    if p["ajuste_composicion"]:
        dur = _vector(_req(h, "duraciones", F, "ajuste de composición por duración"), f"{F}: historia.duraciones", 2)
        if len(dur) != len(s) or np.any(dur <= 0):
            raise ErrorFicha(f"{F}: historia.duraciones: una duración positiva por fecha")
        dw = dur[idx]
        adj = sw * dw[-1] / dw
        ajustado = {"metodo": "diferenciales históricos reescalados a la duración actual [PROPUESTO]",
                    **_posicion(actual, adj, F)}
        lim.append("ajuste de composición solo por duración (no por rating)")
    rec = p["recuperacion"]
    perdida = pd_anual * (1 - rec) * PB_POR_UNIDAD
    dur_d = v.get("duracion_diferencial")
    ampliacion = None
    if dur_d is not None:
        ampliacion = actual / _rango(dur_d, f"{F}: duracion_diferencial", 0, abierto_lo=True)
    else:
        lim.append("sin duración del diferencial: ampliación de equilibrio no calculada")
    return {"diferencial_pb": actual, "percentil": pos["percentil"], "z": pos["z"], "media_pb": pos["media"],
            "n": pos["n"], "anios_historia": anios, "pd_anual": pd_anual, "recuperacion": rec,
            "perdida_esperada_pb": perdida, "exceso_perdida_esperada_pb": actual - perdida,
            "ampliacion_equilibrio_pb": ampliacion, "ajuste_composicion": ajustado,
            "referencias_ingenuas": {"RI_PA_pb": actual, "RI_MH_pb": pos["media"]}}, lim


# ================================================================== FX-PPA-001
def _indice_precios(x: Any, que: str) -> dict[str, Any]:
    d = _dict(x, que)
    return {"valores": _vector(d.get("valores"), f"{que}.valores", 2), "base": _txt(d.get("base_indice"), f"{que}.base_indice"),
            "vintage": _txt(d.get("vintage"), f"{que}.vintage"), "canasta": _txt(d.get("canasta"), f"{que}.canasta"),
            "periodicidad": _txt(d.get("periodicidad"), f"{que}.periodicidad")}


@_cerrado("FX-PPA-001")
def f_fx_ppa(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """FX-PPA-001 · Desviación de la paridad de poder adquisitivo relativa.

    ``valores``: ``par`` («BASE/COT»: el tipo de cambio son unidades de la cotizada por una de la base), ``fechas``
    (mensuales o trimestrales), ``tipo_cambio`` y ``indices`` = {"base": {...}, "cotizada": {...}}, cada uno con
    ``valores``, ``base_indice``, ``vintage``, ``canasta`` y ``periodicidad``. Senda PPA = S₀·(P_cot/P_cot,₀)/(P_base/
    P_base,₀); desviación = ln S − ln senda (%); q = s + p_base − p_cot; vida media por AR(1) de q.
    """
    F = "FX-PPA-001"
    p = _parametros(F, params)
    u = UMBRALES[F]
    v = ent["valores"]
    lim: list[str] = []
    par = _txt(_req(v, "par", F), f"{F}: par")
    if not re.fullmatch(r"[A-Z]{3}/[A-Z]{3}", par) or par[:3] == par[4:]:
        raise ErrorFicha(f"{F}: par «{par}» no válido (se espera «BASE/COT»)")
    fechas = _fechas(_req(v, "fechas", F), f"{F}: fechas")
    _historia_acotada(fechas, u["anios_historia_maximos"], f"{F}: fechas")
    corte = ent["fecha_corte"]
    _conocible(fechas[-1], corte, f"{F}: fechas", "la fecha de corte")
    S = _vector(_req(v, "tipo_cambio", F), f"{F}: tipo_cambio", 2)
    ind = _dict(_req(v, "indices", F), f"{F}: indices")
    ib, ic = _indice_precios(_req(ind, "base", F), f"{F}: indices.base"), _indice_precios(
        _req(ind, "cotizada", F), f"{F}: indices.cotizada")
    for lado, ix in (("base", ib), ("cotizada", ic)):   # H-07: el vintage es la fecha de publicación de los índices
        if _ISO.match(ix["vintage"]):
            _conocible(_fecha(ix["vintage"], f"{F}: indices.{lado}.vintage"), corte, f"{F}: indices.{lado}.vintage",
                       "la fecha de corte")
        elif corte is not None:
            lim.append(f"vintage del índice {lado} sin fecha ISO: no se comprueba que fuera conocible en la fecha de corte")
    if ib["canasta"] != ic["canasta"]:
        raise ErrorFicha(f"{F}: canastas incompatibles («{ib['canasta']}» frente a «{ic['canasta']}»)")
    if ib["periodicidad"] != ic["periodicidad"] or ib["periodicidad"] not in u["periodicidades"]:
        raise ErrorFicha(f"{F}: periodicidades incompatibles o no admitidas ({ib['periodicidad']}, {ic['periodicidad']})")
    paso = u["periodicidades"][ib["periodicidad"]]
    if any(_meses_entre(a, b) != paso for a, b in pairwise(fechas)):
        raise ErrorFicha(f"{F}: las fechas no siguen la periodicidad declarada ({ib['periodicidad']})")
    if not len(S) == len(ib["valores"]) == len(ic["valores"]) == len(fechas):
        raise ErrorFicha(f"{F}: tipo de cambio, índices y fechas de distinta longitud")
    if np.any(S <= 0) or np.any(ib["valores"] <= 0) or np.any(ic["valores"] <= 0):
        raise ErrorFicha(f"{F}: el tipo de cambio y los índices deben ser positivos")
    n = len(fechas)
    if p["ventana"] is not None:
        n_v = p["ventana"] // paso + 1
        if n_v < n:
            fechas, S = fechas[-n_v:], S[-n_v:]
            ib["valores"], ic["valores"] = ib["valores"][-n_v:], ic["valores"][-n_v:]
        else:
            lim.append("la ventana pedida supera la historia: se usa la completa")
    meses = _meses_entre(fechas[0], fechas[-1])
    if meses < u["meses_minimos"]:
        raise ErrorFicha(f"{F}: {meses} meses (< {u['meses_minimos']}): entradas mínimas de la ficha")
    q = np.log(S) + np.log(ib["valores"]) - np.log(ic["valores"])
    ancla = q[0] if p["base"] == "primer_periodo" else float(np.mean(q))
    desv = (q - ancla) * PCT
    senda = S * np.exp(-(q - ancla))
    suav = None
    if p["suavizado"] is not None:
        k = p["suavizado"]
        if k > len(desv):
            raise ErrorFicha(f"{F}: suavizado de {k} periodos mayor que la serie ({len(desv)})")
        suav = [{"fecha": f, "desviacion_pct": float(np.mean(desv[i - k + 1:i + 1]))}
                for i, f in enumerate(fechas) if i >= k - 1]
    vida, phi = None, None
    if meses >= u["anios_vida_media"] * MESES_POR_ANIO:
        X = np.column_stack([np.ones(len(q) - 1), q[:-1]])
        phi = float(np.linalg.lstsq(X, q[1:], rcond=None)[0][1])
        if 0 < phi < 1:
            vida = math.log(0.5) / math.log(phi) * paso / MESES_POR_ANIO
        else:
            lim.append(f"AR(1) con φ = {phi:.4f} fuera de (0, 1): vida media no definida")
    else:
        lim.append(f"historia de {meses / MESES_POR_ANIO:.1f} años (< {u['anios_vida_media']}): vida media no calculada")
    return {"par": par, "base": p["base"], "fechas": fechas,
            "serie_desviacion_pct": [{"fecha": f, "desviacion_pct": float(d)} for f, d in zip(fechas, desv)],
            "desviacion_final_pct": float(desv[-1]), "tipo_real_log_final": float(q[-1]),
            "senda_ppa_final": float(senda[-1]), "tipo_cambio_final": float(S[-1]),
            "inflacion_acumulada_pct": {"base": float(ib["valores"][-1] / ib["valores"][0] - 1) * PCT,
                                        "cotizada": float(ic["valores"][-1] / ic["valores"][0] - 1) * PCT},
            "serie_suavizada": suav, "phi_ar1": phi, "vida_media_anios": vida,
            "indices": {"base": {k: ib[k] for k in ("base", "vintage", "canasta")},
                        "cotizada": {k: ic[k] for k in ("base", "vintage", "canasta")}}}, lim


# ================================================================== FX-MOM-001
def _alinear(fechas: list[date], fd: list[date], d: np.ndarray, que: str) -> np.ndarray:
    """Valor de `d` conocido en cada fecha (el último con fecha ≤; sin dato anterior se rechaza)."""
    out = np.empty(len(fechas))
    j = -1
    for i, f in enumerate(fechas):
        while j + 1 < len(fd) and fd[j + 1] <= f:
            j += 1
        if j < 0:
            raise ErrorFicha(f"{que}: sin dato conocido en {f}")
        out[i] = d[j]
    return out


def rendimiento_exceso(fechas: list[date], spot: np.ndarray, dif_pct: np.ndarray, i0: int, i1: int) -> dict[str, float]:
    """Rendimiento en exceso de la posición larga en la base entre i0 e i1: variación del spot + carry (identidad
    aditiva de FX-CARRY-001), con el carry devengado con el diferencial vigente al inicio de cada tramo (Real/365)."""
    var = float(spot[i1] / spot[i0] - 1)
    carry = float(sum(dif_pct[k - 1] / PCT * (fechas[k] - fechas[k - 1]).days / DIAS_POR_ANIO
                      for k in range(i0 + 1, i1 + 1)))
    return {"variacion_spot": var, "carry": carry, "exceso": var + carry}


@_cerrado("FX-MOM-001")
def f_fx_mom(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """FX-MOM-001 · Momentum cambiario y carry ajustado por volatilidad.

    ``valores["pares"]`` = {par: {"direccion": «BASE/COT» (spot = unidades de COT por BASE, posición larga en la base),
    "spot": {"fechas", "valores"} (o la serie ``ent["series"][par]``), "diferencial_pct": {"fechas", "valores"}
    (tipo de la base − tipo de la cotizada, % anual) o "forward": {"fechas", "valores", "plazo_dias"}, opcional
    "vol_implicita_3m": {"valor": %, "fuente"}}}; opcional ``universo`` (G10, emergentes…).
    """
    F = "FX-MOM-001"
    p = _parametros(F, params)
    u = UMBRALES[F]
    v = ent["valores"]
    lim: list[str] = []
    pares = _dict(_req(v, "pares", F), f"{F}: pares")
    if not pares:
        raise ErrorFicha(f"{F}: pares vacío")
    _tope(len(pares), u["pares_maximos"], f"{F}: pares")
    corte = ent["fecha_corte"]
    horizontes = sorted(set(p["retrospecciones"]) | {u["meses_tsmom"]})
    tabla: dict[str, Any] = {}
    for par, d in pares.items():
        d = _dict(d, f"{F}: {par}")
        dirc = str(d["direccion"]).strip() if _texto(d.get("direccion")) else ""
        if not re.fullmatch(r"[A-Z]{3}/[A-Z]{3}", dirc) or dirc[:3] == dirc[4:]:
            raise ErrorFicha(f"{F}: {par}: rechazo: sin dirección del par declarada («BASE/COT»)")
        sp = d.get("spot") if d.get("spot") is not None else ent["series"].get(par)
        if sp is None:
            raise ErrorFicha(f"{F}: {par}: falta el spot")
        fs, s = _serie(sp, f"{F}: {par}.spot")
        _historia_acotada(fs, u["anios_historia_maximos"], f"{F}: {par}.spot")
        _conocible(fs[-1], corte, f"{F}: {par}.spot", "la fecha de corte")
        if np.any(s <= 0):
            raise ErrorFicha(f"{F}: {par}: spot no positivo")
        if d.get("diferencial_pct") is not None:
            fd, dd = _serie(d["diferencial_pct"], f"{F}: {par}.diferencial_pct", 1)
            fuente_carry = "diferencial de tipos"
        elif d.get("forward") is not None:
            fw = _dict(d["forward"], f"{F}: {par}.forward")
            fd, fwd = _serie(fw, f"{F}: {par}.forward", 1)
            plazo = _rango(fw.get("plazo_dias"), f"{F}: {par}.forward.plazo_dias", 0, abierto_lo=True)
            if np.any(fwd <= 0):
                raise ErrorFicha(f"{F}: {par}: forward no positivo")
            sp_f = _alinear(fd, fs, s, f"{F}: {par}.spot en las fechas del forward")
            dd = (sp_f / fwd - 1) / (plazo / DIAS_POR_ANIO) * PCT
            fuente_carry = "puntos forward (S/F − 1)/τ [PROPUESTO]"
        else:
            raise ErrorFicha(f"{F}: {par}: faltan los diferenciales o los forwards")
        _historia_acotada(fd, u["anios_historia_maximos"], f"{F}: {par}.carry")
        _conocible(fd[-1], corte, f"{F}: {par}.carry (diferencial o forward)", "la fecha de corte")
        keep = [i for i, f in enumerate(fs) if f >= fd[0]]
        fs, s = [fs[i] for i in keep], s[keep]
        if len(fs) < 2 or _anios(fs[0], fs[-1]) < u["anios_minimos"]:
            raise ErrorFicha(f"{F}: {par}: menos de {u['anios_minimos']} años de spot con carry conocido")
        dif = _alinear(fs, fd, dd, f"{F}: {par}.diferencial")
        fin = len(fs) - 1
        rend: dict[str, Any] = {}
        for h in horizontes:
            obj = _hace_meses(fs[-1], h)
            ini = [i for i, f in enumerate(fs) if f <= obj]
            if not ini:
                rend[str(h)] = None
                lim.append(f"{par}: sin historia para {h} meses")
                continue
            r = rendimiento_exceso(fs, s, dif, ini[-1], fin)
            rend[str(h)] = {"exceso_pct": r["exceso"] * PCT, "variacion_spot_pct": r["variacion_spot"] * PCT,
                            "carry_pct": r["carry"] * PCT, "desde": fs[ini[-1]]}
        ts = rend.get(str(u["meses_tsmom"]))
        senal = None if ts is None else int(np.sign(ts["exceso_pct"]))
        iv = d.get("vol_implicita_3m")
        if p["volatilidad"] == "implicita_3m" and iv is not None:
            vol = _rango(_con_fuente(iv, f"{F}: {par}.vol_implicita_3m"), f"{F}: {par}.vol_implicita_3m", 0,
                         abierto_lo=True)
            origen = "implícita 3 meses"
        else:
            obj = _hace_meses(fs[-1], u["meses_vol"])
            ls = np.log(s)
            r_log = [ls[i] - ls[i - 1] for i in range(1, len(fs)) if fs[i] > obj]
            if len(r_log) < 2:
                raise ErrorFicha(f"{F}: {par}: menos de 2 rendimientos en {u['meses_vol']} meses para la volatilidad")
            vol = float(np.std(r_log, ddof=1) * math.sqrt(SESIONES_POR_ANIO)) * PCT
            origen = f"realizada {u['meses_vol']} meses"
            if p["volatilidad"] == "implicita_3m":
                lim.append(f"{par}: sin volatilidad implícita: se usa la realizada a {u['meses_vol']} meses")
        if not vol > 0:
            raise ErrorFicha(f"{F}: {par}: volatilidad nula: carry/volatilidad no definido")
        tabla[str(par)] = {"direccion": dirc, "rendimientos_exceso": rend, "senal_tsmom": senal,
                           "diferencial_actual_pct": float(dif[-1]), "fuente_carry": fuente_carry,
                           "volatilidad_pct": vol, "fuente_volatilidad": origen,
                           "carry_volatilidad": float(dif[-1]) / vol, "fecha": fs[-1]}
    rangos: dict[str, Any] = {}
    for h in horizontes:
        vals = {k: t["rendimientos_exceso"][str(h)]["exceso_pct"] for k, t in tabla.items()
                if t["rendimientos_exceso"].get(str(h)) is not None}
        if len(vals) >= 2:
            rangos[str(h)] = {k: {kk: pos[kk] for kk in ("percentil", "z")}
                              for k, x in vals.items() for pos in [_posicion(x, np.array(list(vals.values())), F)]}
        else:
            rangos[str(h)] = None
    if len(tabla) < 2:
        lim.append("un solo par: sin rango transversal")
    universo = v.get("universo")
    return {"pares": tabla, "rangos_transversales": rangos,
            "universo": _txt(universo, f"{F}: universo") if universo is not None else None}, lim


# ================================================================== ACC-ERP-001
def valor_damodaran(r: float, cf0: float, g5: float, gL: float, n: int) -> float:
    """Valor (tantos por uno) del flujo al accionista: n años creciendo a g₅ y perpetuidad a g_L desde el año n."""
    vp = sum(cf0 * (1 + g5) ** k / (1 + r) ** k for k in range(1, n + 1))
    vt = cf0 * (1 + g5) ** n * (1 + gL) / (r - gL)
    return float(vp + vt / (1 + r) ** n)


@_cerrado("ACC-ERP-001")
def f_acc_erp(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """ACC-ERP-001 · Prima de riesgo implícita del índice.

    ``valores``: ``moneda``; ``nivel``; ``dividendos_12m`` y ``recompras_netas_12m`` (puntos de índice); ``g5``
    ({"valor": %, "fuente", "fecha"}); ``rf_nominal_10a`` y ``rf_real_10a`` ({"valor": %, "moneda", "fuente"});
    ``beneficio_adelantado`` (puntos); ``cape`` ({"valor", "fuente"}) o ``beneficios_reales_10a`` (≥ 10 años, puntos
    reales). Opcional ``historia`` = {"fechas", "prm_pp", "simple_pp", "ecy_pp"} para percentiles (≥ 10 años).
    """
    F = "ACC-ERP-001"
    p = _parametros(F, params)
    u = UMBRALES[F]
    v = ent["valores"]
    lim: list[str] = []
    moneda = _txt(_req(v, "moneda", F), f"{F}: moneda")
    tipos = {}
    for k in ("rf_nominal_10a", "rf_real_10a"):
        d = v.get(k)
        if not isinstance(d, dict) or d.get("moneda") != moneda:
            raise ErrorFicha(f"{F}: rechazo: sin r_f de la moneda del índice ({k} en {moneda})")
        tipos[k] = _con_fuente(d, f"{F}: {k}")
    rf, rr = tipos["rf_nominal_10a"], tipos["rf_real_10a"]
    nivel = _rango(_req(v, "nivel", F), f"{F}: nivel", 0, abierto_lo=True)
    div = _rango(_req(v, "dividendos_12m", F), f"{F}: dividendos_12m", 0)
    rec = _num(_req(v, "recompras_netas_12m", F), f"{F}: recompras_netas_12m") if p["incluir_recompras"] else 0.0
    cf0 = div + rec
    if not cf0 > 0:
        raise ErrorFicha(f"{F}: flujo al accionista ≤ 0: r implícita no definida")
    g5d = _dict(_req(v, "g5", F), f"{F}: g5")
    g5 = _con_fuente(g5d, f"{F}: g5")
    corte = ent["fecha_corte"]
    _conocible(_fecha(_req(g5d, "fecha", F, "consenso con fecha"), f"{F}: g5.fecha"), corte, f"{F}: g5.fecha",
               "la fecha de corte")
    gL = rf if p["g_L"] is None else p["g_L"]
    if not rf - u["amplitud_g_L_pp"] <= gL <= rf:
        raise ErrorFicha(f"{F}: g_L = {gL:g} % fuera del rango admitido [r_f − {u['amplitud_g_L_pp']} pp, r_f]")
    if not (g5 > -PCT and gL > -PCT):
        raise ErrorFicha(f"{F}: crecimientos ≤ −100 %")
    n = u["anios_explicitos"]
    g5u, gLu = g5 / PCT, gL / PCT

    def g(x: float) -> float:   # x = r − g_L > 0; decreciente en r ⇒ −(valor − nivel) creciente en x
        return nivel - valor_damodaran(gLu + x, cf0, g5u, gLu, n)

    x = _raiz_creciente(g, f"{F}: r implícita", u["iteraciones_max"], u["tol"] * np.finfo(float).eps)
    r = gLu + x
    error = abs(valor_damodaran(r, cf0, g5u, gLu, n) - nivel) / nivel
    if error > u["tol"]:
        raise ErrorFicha(f"{F}: CONVERGENCIA (r implícita no reproduce el nivel con la tolerancia de la ficha)")
    ey = _rango(_req(v, "beneficio_adelantado", F), f"{F}: beneficio_adelantado", 0, abierto_lo=True) / nivel * PCT
    if v.get("cape") is not None:
        cape = _rango(_con_fuente(v["cape"], f"{F}: cape"), f"{F}: cape", 0, abierto_lo=True)
    else:
        br = _vector(_req(v, "beneficios_reales_10a", F, "beneficios reales 10 años para CAPE"),
                     f"{F}: beneficios_reales_10a", u["anios_cape"])
        _tope(len(br), u["anios_historia_maximos"], f"{F}: beneficios_reales_10a (uno por año)")
        media = float(np.mean(br[-u["anios_cape"]:]))
        if not media > 0:
            raise ErrorFicha(f"{F}: media de beneficios reales ≤ 0: CAPE no definido")
        cape = nivel / media
    prm, simple, ecy = r * PCT - rf, ey - rr, PCT / cape - rr
    perc: dict[str, Any] = {"prm_pp": None, "simple_pp": None, "ecy_pp": None}
    hist = v.get("historia")
    if hist is None:
        lim.append("sin historia: percentiles y z-scores no calculados")
    else:
        hist = _dict(hist, f"{F}: historia")
        fh = _fechas(hist.get("fechas"), f"{F}: historia.fechas")
        _historia_acotada(fh, u["anios_historia_maximos"], f"{F}: historia.fechas")
        _conocible(fh[-1], corte, f"{F}: historia.fechas", "la fecha de corte")
        idx = [i for i, f in enumerate(fh) if _anios(f, fh[-1]) <= p["ventana_percentil"]]
        anios = _anios(fh[idx[0]], fh[-1])
        if anios < u["anios_percentil_minimo"]:
            lim.append(f"historia de {anios:.1f} años (< {u['anios_percentil_minimo']}): percentiles no calculados")
        else:
            if anios < p["ventana_percentil"]:
                lim.append(f"historia de {anios:.1f} años (< {p['ventana_percentil']:g} de la ventana)")
            for clave, actual in (("prm_pp", prm), ("simple_pp", simple), ("ecy_pp", ecy)):
                serie = _vector(_req(hist, clave, F), f"{F}: historia.{clave}", 2)
                if len(serie) != len(fh):
                    raise ErrorFicha(f"{F}: historia.{clave} de distinta longitud que las fechas")
                perc[clave] = _posicion(actual, serie[idx], F)
    return {"moneda": moneda, "r_implicita_pct": r * PCT, "prm_pp": prm, "version_simple_pp": simple, "ecy_pp": ecy,
            "cape": cape, "rendimiento_beneficio_pct": ey, "flujo_accionista_12m": cf0, "g5_pct": g5, "g_L_pct": gL,
            "rf_nominal_pct": rf, "rf_real_pct": rr, "percentiles": perc,
            "segunda_via": {"version_simple_pp": simple, "diferencia_prm_menos_simple_pp": prm - simple},
            "verificacion": {"error_relativo_nivel": error}}, lim


# ================================================================== ACC-FACT-001
def rezagos_newey_west(n: int) -> int:
    """L = ⌊4·(T/100)^{2/9}⌋ (ACC-FACT-001, «Método»)."""
    return math.floor(4 * (n / 100) ** (2 / 9))


def mco_newey_west(y: np.ndarray, X: np.ndarray, rezagos: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """MCO con covarianza HAC de Newey-West (núcleo de Bartlett): (β, residuos, errores estándar)."""
    n, k = X.shape
    if n <= k or np.linalg.matrix_rank(X) < k:
        raise ErrorFicha("ACC-FACT-001: regresión no identificada (pocas observaciones o factores colineales)")
    xtx = np.linalg.inv(X.T @ X)
    beta = xtx @ (X.T @ y)
    e = y - X @ beta
    g = X * e[:, None]
    S = g.T @ g
    for rez in range(1, rezagos + 1):
        w = 1 - rez / (rezagos + 1)
        G = g[rez:].T @ g[:-rez]
        S = S + w * (G + G.T)
    V = xtx @ S @ xtx
    return beta, e, np.sqrt(np.clip(np.diag(V), 0.0, None))


def _regresion(y: np.ndarray, Fm: np.ndarray, nombres: list[str], P: int, lim: list[str], que: str) -> dict[str, Any]:
    X = np.column_stack([np.ones(len(y)), Fm])
    L = rezagos_newey_west(len(y))
    beta, e, ee = mco_newey_west(y, X, L)
    vt = float(np.var(y))
    if not vt > 0:
        raise ErrorFicha(f"{que}: rendimientos sin varianza")
    t = [float(b / s) if s > 0 else None for b, s in zip(beta, ee)]
    if any(x is None for x in t):
        lim.append(f"{que}: error estándar nulo (ajuste exacto): estadístico t no definido")
    ajustado = Fm @ beta[1:]
    contrib = {n: float(beta[j + 1] * np.mean((Fm[:, j] - Fm[:, j].mean()) * (ajustado - ajustado.mean())) / vt * PCT)
               for j, n in enumerate(nombres)}
    contrib["residuo"] = float(np.var(e) / vt * PCT)
    return {"alfa_periodo_pct": float(beta[0]), "alfa_anual_pct": ((1 + beta[0] / PCT) ** P - 1) * PCT,
            "t_alfa": t[0], "betas": {n: {"beta": float(beta[j + 1]), "ee": float(ee[j + 1]), "t": t[j + 1]}
                                      for j, n in enumerate(nombres)},
            "r2": 1 - float(np.var(e)) / vt, "contribuciones_varianza_pct": contrib, "rezagos_nw": L, "n": len(y)}


@_cerrado("ACC-FACT-001")
def f_acc_fact(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """ACC-FACT-001 · Exposición factorial del indicador del ámbito.

    ``valores``: ``fechas`` (mensuales consecutivas o semanales cada 7 días), ``rendimientos`` (% por periodo),
    ``rf`` (% por periodo) o ``en_exceso: true``, ``factores`` = {MKT, SMB, …: [% por periodo]} y ``region``.
    """
    F = "ACC-FACT-001"
    p = _parametros(F, params)
    u = UMBRALES[F]
    v = ent["valores"]
    lim: list[str] = []
    fr = p["frecuencia"]
    _txt(_req(v, "region", F, "región de los factores"), f"{F}: region")
    fechas = _fechas(_req(v, "fechas", F), f"{F}: fechas")
    _historia_acotada(fechas, u["anios_historia_maximos"], f"{F}: fechas")
    _conocible(fechas[-1], ent["fecha_corte"], f"{F}: fechas", "la fecha de corte")
    if fr == "mensual" and any(_meses_entre(a, b) != 1 for a, b in pairwise(fechas)):
        raise ErrorFicha(f"{F}: las fechas no son mensuales consecutivas")
    if fr == "semanal" and any((b - a).days != DIAS_POR_SEMANA for a, b in pairwise(fechas)):
        raise ErrorFicha(f"{F}: las fechas no son semanales consecutivas")
    n = len(fechas)
    if n < u["observaciones_minimas"][fr]:
        raise ErrorFicha(f"{F}: {n} observaciones {fr}es (< {u['observaciones_minimas'][fr]}): rechazo de la ficha")
    r = _vector(_req(v, "rendimientos", F), f"{F}: rendimientos", n)
    if len(r) != n:
        raise ErrorFicha(f"{F}: rendimientos de distinta longitud que las fechas")
    if v.get("rf") is not None:
        rf = _vector(v["rf"], f"{F}: rf", n)
        if len(rf) != n:
            raise ErrorFicha(f"{F}: rf de distinta longitud que las fechas")
        r = r - rf
    elif v.get("en_exceso") is not True:
        raise ErrorFicha(f"{F}: falta «rf» (o declare «en_exceso»: true)")
    fac = _dict(_req(v, "factores", F), f"{F}: factores")
    nombres = list(u["factores_modelo"][p["modelo"]]) + list(p["adicionales"])
    cols = [_vector(_req(fac, k, F, f"factor del modelo {p['modelo']}"), f"{F}: factores.{k}", n) for k in nombres]
    if any(len(c) != n for c in cols):
        raise ErrorFicha(f"{F}: factores de distinta longitud que las fechas")
    Fm = np.column_stack(cols)
    P = u["periodos_por_anio"][fr]
    base = _regresion(r, Fm, nombres, P, lim, F)
    capm = _regresion(r, Fm[:, :1], nombres[:1], P, lim, f"{F} (CAPM)")
    nuevos = {a: base["betas"][a]["t"] is not None and abs(base["betas"][a]["t"]) > u["t_factor_nuevo"]
              for a in p["adicionales"]}
    W = p["ventana_movil"] if fr == "mensual" else p["ventana_movil"] * SEMANAS_POR_ANIO // MESES_POR_ANIO
    moviles = []
    if W > Fm.shape[1] + 1 and W <= n:
        X = np.column_stack([np.ones(n), Fm])
        for i in range(W, n + 1):
            b = np.linalg.lstsq(X[i - W:i], r[i - W:i], rcond=None)[0]
            moviles.append({"fecha": fechas[i - 1], "betas": dict(zip(nombres, map(float, b[1:])))})
    else:
        lim.append(f"ventana móvil de {W} observaciones no admisible con {n} datos y {Fm.shape[1]} factores")
    ingenua = float(np.mean(r - Fm[:, 0]))
    return {"modelo": p["modelo"], "factores": nombres, "frecuencia": fr, **base, "factores_nuevos_t_mayor_3": nuevos,
            "betas_moviles": moviles, "ventana_movil_obs": W,
            "segunda_via_capm": {"beta_mkt": capm["betas"]["MKT"]["beta"], "t_beta": capm["betas"]["MKT"]["t"],
                                 "alfa_anual_pct": capm["alfa_anual_pct"], "t_alfa": capm["t_alfa"], "r2": capm["r2"]},
            "referencia_ingenua": {"metodo": "CAPM con β = 1", "alfa_periodo_pct": ingenua,
                                   "alfa_anual_pct": ((1 + ingenua / PCT) ** P - 1) * PCT}}, lim


# ================================================================== ACC-VAL-001
def ev_dcf(flujo0: float, g_exp: float, n: int, tasa: float, g_t: float, nopat0: float | None = None,
           roic: float | None = None) -> dict[str, Any]:
    """DCF (tantos por uno): flujos F_k = F₀(1 + g_exp)^k, k = 1..n, descontados a `tasa`, y valor terminal de Gordon
    F_n(1 + g)/(tasa − g); con ROIC_nuevo, VT = NOPAT_n(1 + g)(1 − g/ROIC)/(tasa − g) (tasa de reinversión = g/ROIC)."""
    if g_t >= tasa:
        raise ErrorFicha("ACC-VAL-001: rechazo: g ≥ tasa de descuento")
    flujos = [flujo0 * (1 + g_exp) ** k for k in range(1, n + 1)]
    vp = [f / (1 + tasa) ** k for k, f in enumerate(flujos, start=1)]
    if roic is not None and nopat0 is not None:
        vt = nopat0 * (1 + g_exp) ** n * (1 + g_t) * (1 - g_t / roic) / (tasa - g_t)
    else:
        vt = flujos[-1] * (1 + g_t) / (tasa - g_t)
    vp_vt = vt / (1 + tasa) ** n
    return {"flujos": flujos, "vp_flujos": vp, "vt": vt, "vp_vt": vp_vt, "valor": float(sum(vp) + vp_vt)}


@_cerrado("ACC-VAL-001")
def f_acc_val(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """ACC-VAL-001 · DCF, DCF inverso y múltiplos de un agregado (sector, temática o índice).

    ``valores``: ``moneda``; ``ejercicios`` (≥ 3) [{"ejercicio", "fecha_presentacion", "moneda", "ventas", "ebit",
    "amortizaciones", "capex", "variacion_circulante", opcionales "ebitda", "fondos_propios", "flujo_accionista"}];
    ``capitalizacion`` ({"valor", "fecha"}); ``deuda_neta``; ``rf`` ({"valor": %, "moneda"}); ``coste_deuda_pct``;
    ``crecimiento_explicito`` ({"valor": %, "fuente"}); opcionales ``beta`` y ``prm`` ({"valor", "fuente"}: ACC-FACT-001 y
    ACC-ERP-001), ``tasa_impositiva_legal`` (%), ``roic_nuevo_pct``, ``beneficio_adelantado``, ``historia_multiplos``
    ({múltiplo: {"fechas", "valores"}}) y ``multiplos_mercado`` ({múltiplo: valor}).
    """
    F = "ACC-VAL-001"
    p = _parametros(F, params)
    u = UMBRALES[F]
    v = ent["valores"]
    lim: list[str] = []
    adv: list[str] = []
    moneda = _txt(_req(v, "moneda", F), f"{F}: moneda")
    ejs = _lista(_req(v, "ejercicios", F), f"{F}: ejercicios")
    if len(ejs) < u["ejercicios_minimos"]:
        raise ErrorFicha(f"{F}: {len(ejs)} ejercicios (< {u['ejercicios_minimos']}): rechazo de la ficha")
    _tope(len(ejs), u["ejercicios_maximos"], f"{F}: ejercicios")
    if len(ejs) < u["ejercicios_recomendados"]:
        lim.append(f"{len(ejs)} ejercicios (< {u['ejercicios_recomendados']} recomendados)")
    filas, presentaciones = [], []
    for i, e in enumerate(ejs):
        e = _dict(e, f"{F}: ejercicios[{i}]")
        if e.get("moneda") != moneda:
            raise ErrorFicha(f"{F}: rechazo: monedas inconsistentes (ejercicio {i} en {e.get('moneda')!r}, agregado en {moneda})")
        presentaciones.append(_fecha(_req(e, "fecha_presentacion", F), f"{F}: ejercicios[{i}].fecha_presentacion"))
        filas.append({k: _num(_req(e, k, F, f"ejercicio {i}"), f"{F}: ejercicios[{i}].{k}")
                      for k in ("ejercicio", "ventas", "ebit", "amortizaciones", "capex", "variacion_circulante")}
                     | {k: _num(e[k], f"{F}: ejercicios[{i}].{k}") for k in ("ebitda", "fondos_propios", "flujo_accionista")
                        if e.get(k) is not None})
    if any(b["ejercicio"] <= a["ejercicio"] for a, b in pairwise(filas)):
        raise ErrorFicha(f"{F}: ejercicios no ordenados de forma estrictamente creciente")
    ult = filas[-1]
    rfd = _dict(_req(v, "rf", F), f"{F}: rf")
    if rfd.get("moneda") != moneda:
        raise ErrorFicha(f"{F}: rechazo: monedas inconsistentes (r_f en {rfd.get('moneda')!r}, flujos en {moneda})")
    rf = _num(rfd.get("valor"), f"{F}: rf.valor")
    cap_d = _dict(_req(v, "capitalizacion", F), f"{F}: capitalizacion")
    cap = _rango(cap_d.get("valor"), f"{F}: capitalizacion.valor", 0, abierto_lo=True)
    # QA r01 de T-112, H-07: la «fecha de presentación» de la ficha es la del punto en el tiempo. La fecha de valoración es
    # la de la capitalización (HT-01); ni ella puede ser posterior a la fecha de corte ni un ejercicio presentado después
    # de ella entra en el cálculo: se rechaza (no se excluye, porque el último ejercicio es la base del flujo).
    f_val = _fecha(_req(cap_d, "fecha", F, "fecha HT-01"), f"{F}: capitalizacion.fecha")
    _conocible(f_val, ent["fecha_corte"], f"{F}: capitalizacion.fecha", "la fecha de corte")
    for i, f_pres in enumerate(presentaciones):
        _conocible(f_pres, f_val, f"{F}: ejercicios[{i}].fecha_presentacion", "la fecha de valoración (capitalización)")
    deuda = _num(_req(v, "deuda_neta", F), f"{F}: deuda_neta")
    t_imp = p["tasa_impositiva"] if p["tasa_impositiva"] is not None else _rango(
        _req(v, "tasa_impositiva_legal", F, "tasa impositiva legal marginal"), f"{F}: tasa_impositiva_legal", 0, PCT,
        abierto_hi=True)
    t = t_imp / PCT
    beta = u["beta_respaldo"] if v.get("beta") is None else _con_fuente(v["beta"], f"{F}: beta")
    if v.get("beta") is None:
        lim.append("β = 1 (sin β de ACC-FACT-001)")
    if p["PRM"] is not None:
        prm = p["PRM"]
    elif v.get("prm") is not None:
        prm = _rango(_con_fuente(v["prm"], f"{F}: prm"), f"{F}: prm", *u["rango_prm_pct"])
    else:
        prm = u["prm_respaldo_pct"]
        lim.append(f"PRM = {prm} % de respaldo (sin PRM de ACC-ERP-001)")
    g_t = min(rf, u["g_terminal_tope_pct"]) if p["g_terminal"] is None else p["g_terminal"]
    if not 0 <= g_t <= rf:
        raise ErrorFicha(f"{F}: g_terminal = {g_t:g} % fuera del rango admitido [0, r_f = {rf:g} %]")
    g_exp = _con_fuente(_req(v, "crecimiento_explicito", F), f"{F}: crecimiento_explicito")
    if not g_exp > -PCT:
        raise ErrorFicha(f"{F}: crecimiento explícito ≤ −100 %")
    ke = rf + beta * prm
    d_pos = max(deuda, 0.0)
    if d_pos > 0:
        kd = _num(_req(v, "coste_deuda_pct", F, "coste de la deuda para el WACC"), f"{F}: coste_deuda_pct")
    else:
        kd = 0.0
        lim.append("deuda neta ≤ 0: peso de la deuda nulo en el WACC")
    wacc = (cap * ke + d_pos * kd * (1 - t)) / (cap + d_pos)
    n = p["anios_explicitos"]
    ev_mkt = cap + deuda
    nopat0 = ult["ebit"] * (1 - t)
    fcff0 = nopat0 + ult["amortizaciones"] - ult["capex"] - ult["variacion_circulante"]
    roic = None if v.get("roic_nuevo_pct") is None else _rango(v["roic_nuevo_pct"], f"{F}: roic_nuevo_pct", 0,
                                                               abierto_lo=True) / PCT
    if p["enfoque"] == "FCFF":
        flujo0, tasa = fcff0, wacc
    else:
        flujo0, tasa = _num(_req(ult, "flujo_accionista", F, "flujo al accionista del último ejercicio (FCFE)"),
                            f"{F}: flujo_accionista"), ke
        if roic is not None:
            raise ErrorFicha(f"{F}: ROIC_nuevo solo con el enfoque FCFF")
    if not flujo0 > 0:
        raise ErrorFicha(f"{F}: flujo base ≤ 0: DCF no aplicable (normalice beneficios del ciclo)")
    base = ev_dcf(flujo0, g_exp / PCT, n, tasa / PCT, g_t / PCT, nopat0 if roic else None, roic)
    if p["enfoque"] == "FCFF":
        ev, equity = base["valor"], base["valor"] - deuda
    else:
        equity, ev = base["valor"], base["valor"] + deuda
    peso_vt = base["vp_vt"] / base["valor"] * PCT
    if peso_vt > u["peso_vt_advertencia_pct"]:
        adv.append(f"el valor terminal pesa el {peso_vt:.1f} % del valor (> {u['peso_vt_advertencia_pct']} %)")

    # DCF inverso: crecimiento explícito que iguala el precio; margen de flujo sobre ventas implícito
    objetivo = ev_mkt if p["enfoque"] == "FCFF" else cap

    def gi(x: float) -> float:   # x = 1 + g_exp > 0; valor creciente en x
        return ev_dcf(flujo0, x - 1, n, tasa / PCT, g_t / PCT, nopat0 if roic else None, roic)["valor"] - objetivo

    if not objetivo > 0:
        raise ErrorFicha(f"{F}: valor de mercado ≤ 0: DCF inverso no definido")
    x = _raiz_creciente(gi, f"{F}: DCF inverso", u["iteraciones_max"], u["tol_inverso"] * np.finfo(float).eps)
    g_impl = (x - 1) * PCT
    err_inv = abs(gi(x)) / objetivo
    if err_inv > u["tol_inverso"]:
        raise ErrorFicha(f"{F}: CONVERGENCIA (DCF inverso fuera de la tolerancia de la ficha)")
    margen = None
    if roic is None and ult["ventas"] > 0:
        margen = {"actual_pct": flujo0 / ult["ventas"] * PCT, "implicito_pct": flujo0 / ult["ventas"] * PCT * objetivo
                  / base["valor"]}
    else:
        lim.append("margen implícito no calculado (ROIC_nuevo declarado o ventas ≤ 0)")

    # Sensibilidad: tasa ±1 pp × g ±0,5 pp
    pasos_w = [-u["sensibilidad_wacc_pp"], 0, u["sensibilidad_wacc_pp"]]
    pasos_g = [-u["sensibilidad_g_pp"], 0, u["sensibilidad_g_pp"]]
    matriz: list[list[float | None]] = []
    for dw in pasos_w:
        fila: list[float | None] = []
        for dg in pasos_g:
            if g_t + dg >= tasa + dw or g_t + dg < 0:
                fila.append(None)
                continue
            val = ev_dcf(flujo0, g_exp / PCT, n, (tasa + dw) / PCT, (g_t + dg) / PCT, nopat0 if roic else None,
                         roic)["valor"]
            fila.append(val - deuda if p["enfoque"] == "FCFF" else val)
        matriz.append(fila)
    if any(c is None for f in matriz for c in f):
        lim.append("sensibilidad: celdas con g ≥ tasa de descuento o g < 0 no calculadas")

    # Múltiplos del agregado (totales = media armónica ponderada por capitalización de los componentes)
    ebitda = ult.get("ebitda", ult["ebit"] + ult["amortizaciones"])
    bfa = v.get("beneficio_adelantado")
    mult: dict[str, float | None] = {}
    if bfa is None or _num(bfa, f"{F}: beneficio_adelantado") <= 0:
        mult["per_adelantado"] = None
        lim.append("PER no aplicable con beneficio ≤ 0 (o no aportado)")
    else:
        mult["per_adelantado"] = cap / float(bfa)
    mult["ev_ebitda"] = ev_mkt / ebitda if ebitda > 0 else None
    mult["ev_ventas"] = ev_mkt / ult["ventas"] if ult["ventas"] > 0 else None
    fp = ult.get("fondos_propios")
    mult["p_vc"] = cap / fp if fp is not None and fp > 0 else None
    mult["fcf_yield_pct"] = fcff0 / ev_mkt * PCT if ev_mkt > 0 else None
    for k, x_m in mult.items():
        if x_m is None and k != "per_adelantado":
            lim.append(f"múltiplo {k} no aplicable con estos datos")
    perc: dict[str, Any] = {}
    hm = v.get("historia_multiplos") or {}
    for k, serie in _dict(hm, f"{F}: historia_multiplos").items():
        if k not in mult:
            raise ErrorFicha(f"{F}: historia_multiplos: múltiplo «{k}» desconocido ({sorted(mult)})")
        if mult[k] is None:
            continue
        fh, vh = _serie(serie, f"{F}: historia_multiplos.{k}")
        _historia_acotada(fh, u["anios_historia_maximos"], f"{F}: historia_multiplos.{k}")
        _conocible(fh[-1], f_val, f"{F}: historia_multiplos.{k}", "la fecha de valoración (capitalización)")
        if _anios(fh[0], fh[-1]) < u["anios_percentil"]:
            perc[k] = None
            lim.append(f"historia de {k} < {u['anios_percentil']} años: percentil no calculado")
        else:
            perc[k] = _posicion(float(mult[k] or 0.0), vh, F)
    rel: dict[str, float] = {}
    for k, x_r in _dict(v.get("multiplos_mercado") or {}, f"{F}: multiplos_mercado").items():
        if k not in mult:
            raise ErrorFicha(f"{F}: multiplos_mercado: múltiplo «{k}» desconocido ({sorted(mult)})")
        ref = _rango(x_r, f"{F}: multiplos_mercado.{k}", 0, abierto_lo=True)
        if mult[k] is not None:
            rel[k] = float(mult[k] or 0.0) / ref - 1
    segunda = {"per_implicito_dcf": equity / float(bfa) if mult["per_adelantado"] is not None else None,
               "per_mercado": mult["per_adelantado"],
               "ev_ebitda_implicito_dcf": ev / ebitda if ebitda > 0 else None, "ev_ebitda_mercado": mult["ev_ebitda"]}
    return {"moneda": moneda, "enfoque": p["enfoque"], "wacc_pct": wacc, "coste_capital_pct": ke, "tasa_descuento_pct": tasa,
            "beta": beta, "prm_pct": prm, "g_terminal_pct": g_t, "crecimiento_explicito_pct": g_exp,
            "flujo_base": flujo0, "fcff_0": fcff0, "flujos": base["flujos"], "vp_flujos": base["vp_flujos"],
            "valor_terminal": base["vt"], "vp_valor_terminal": base["vp_vt"], "ev": ev, "valor_agregado": equity,
            "peso_valor_terminal_pct": peso_vt, "capitalizacion": cap, "ev_mercado": ev_mkt,
            "brecha_pct": (equity / cap - 1) * PCT,
            "dcf_inverso": {"crecimiento_implicito_pct": g_impl, "error_relativo": err_inv, "margen_flujo": margen},
            "sensibilidad": {"filas_tasa_pp": pasos_w, "columnas_g_pp": pasos_g, "valor_agregado": matriz},
            "multiplos": mult, "percentiles_multiplos": perc, "multiplos_frente_mercado": rel,
            "segunda_via": segunda, "advertencias": adv}, lim


# ================================================================== DER-OPT-001
def _d12(S: float, K: float, T: float, r: float, q: float, s: float) -> tuple[float, float]:
    sd = s * math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * s * s) * T) / sd
    return d1, d1 - sd


def bsm(S: float, K: float, T: float, r: float, q: float, s: float, call: bool) -> float:
    """Black-Scholes-Merton con dividendo continuo (tantos por uno). Black-76 = bsm con q = r y S = F."""
    d1, d2 = _d12(S, K, T, r, q, s)
    N = stats.norm.cdf
    if call:
        return float(S * math.exp(-q * T) * N(d1) - K * math.exp(-r * T) * N(d2))
    return float(K * math.exp(-r * T) * N(-d2) - S * math.exp(-q * T) * N(-d1))


def griegas_bsm(S: float, K: float, T: float, r: float, q: float, s: float, call: bool, black: bool) -> dict[str, float]:
    """Δ, Γ, vega (por punto de volatilidad), θ (por día) y ρ (por punto de tipo)."""
    d1, d2 = _d12(S, K, T, r, q, s)
    N, n = stats.norm.cdf, stats.norm.pdf
    eq, er = math.exp(-q * T), math.exp(-r * T)
    gamma = eq * n(d1) / (S * s * math.sqrt(T))
    vega = S * eq * n(d1) * math.sqrt(T)
    comun = -S * eq * n(d1) * s / (2 * math.sqrt(T))
    if call:
        delta = eq * N(d1)
        theta = comun - r * K * er * N(d2) + q * S * eq * N(d1)
        rho = K * T * er * N(d2)
    else:
        delta = eq * (N(d1) - 1)
        theta = comun + r * K * er * N(-d2) - q * S * eq * N(-d1)
        rho = -K * T * er * N(-d2)
    if black:
        rho = -T * bsm(S, K, T, r, q, s, call)
    return {"delta": float(delta), "gamma": float(gamma), "vega": float(vega) / PCT, "theta_dia": float(theta) / DIAS_POR_ANIO,
            "rho": float(rho) / PCT}


def crr(S: float, K: float, T: float, r: float, q: float, s: float, call: bool, americana: bool, N: int) -> dict[str, float]:
    """Árbol de Cox-Ross-Rubinstein con N pasos: precio y Δ, Γ, θ del propio árbol."""
    dt = T / N
    up = math.exp(s * math.sqrt(dt))
    dn = 1 / up
    pr = (math.exp((r - q) * dt) - dn) / (up - dn)
    if not 0 < pr < 1:
        raise ErrorFicha("DER-OPT-001: probabilidad del árbol fuera de (0, 1): aumente los pasos")
    disc = math.exp(-r * dt)
    j = np.arange(N + 1)
    precios = S * up ** (N - 2 * j)
    ejer = np.maximum(precios - K, 0.0) if call else np.maximum(K - precios, 0.0)
    val = ejer.copy()
    capas: dict[int, np.ndarray] = {N: val.copy()} if N <= 2 else {}   # r02: con N = 2 la capa 2 es la terminal
    for paso in range(N - 1, -1, -1):
        precios = S * up ** (paso - 2 * np.arange(paso + 1))
        val = disc * (pr * val[:-1] + (1 - pr) * val[1:])
        if americana:
            val = np.maximum(val, precios - K if call else K - precios)
        if paso <= 2:
            capas[paso] = val.copy()
    out = {"precio": float(capas[0][0])}
    if N >= 2:
        su, sd_ = S * up, S * dn
        out["delta"] = float((capas[1][0] - capas[1][1]) / (su - sd_))
        g_u = (capas[2][0] - capas[2][1]) / (S * up * up - S)
        g_d = (capas[2][1] - capas[2][2]) / (S - S * dn * dn)
        out["gamma"] = float((g_u - g_d) / ((S * up * up - S * dn * dn) / 2))
        out["theta_dia"] = float((capas[2][1] - capas[0][0]) / (2 * dt)) / DIAS_POR_ANIO
    return out


def crr_promedio(S: float, K: float, T: float, r: float, q: float, s: float, call: bool, americana: bool,
                 N: int) -> dict[str, float]:
    """Promedio de los árboles de N y N + 1 pasos (DER-OPT-001, «Método»)."""
    a, b = crr(S, K, T, r, q, s, call, americana, N), crr(S, K, T, r, q, s, call, americana, N + 1)
    return {k: (a[k] + b[k]) / 2 for k in a if k in b}


def _cotas(S: float, K: float, T: float, r: float, q: float, call: bool, americana: bool) -> tuple[float, float]:
    """Cotas de no arbitraje del precio (europea o americana)."""
    fs, fk = S * math.exp(-q * T), K * math.exp(-r * T)
    if call:
        lo = max(fs - fk, 0.0) if not americana else max(S - K, fs - fk, 0.0)
        return lo, (fs if not americana else S)
    lo = max(fk - fs, 0.0) if not americana else max(K - S, fk - fs, 0.0)
    return lo, (fk if not americana else K)


def vol_implicita(precio: Callable[[float], float], vega: Callable[[float], float] | None, objetivo: float, tol: float,
                  iteraciones: int, s0: float) -> float:
    """σ (tanto por uno) que reproduce el precio: Newton con vega y respaldo de Brent (precio creciente en σ)."""
    s = s0
    if vega is not None:
        for _ in range(iteraciones):
            dv = vega(s)
            if not dv > 0:
                break
            paso = (precio(s) - objetivo) / dv
            nuevo = s - paso
            if not (math.isfinite(nuevo) and nuevo > 0):
                break
            s = nuevo
            if abs(paso) <= tol:
                return s
    return _raiz_creciente(lambda x: precio(x) - objetivo, "DER-OPT-001: volatilidad implícita", iteraciones, tol)


def _contrato(c: dict[str, Any], p: dict[str, Any], u: dict[str, Any], lim: list[str], que: str) -> dict[str, Any]:
    tipo = _opcion(_req(c, "tipo", que), f"{que}: tipo (payoff fuera de ficha)", ("call", "put"))
    estilo = _opcion(_req(c, "estilo", que), f"{que}: estilo (payoff fuera de ficha)", ("europea", "americana"))
    S = _rango(_req(c, "S", que), f"{que}: S", 0, abierto_lo=True)
    K = _rango(_req(c, "K", que), f"{que}: K", 0, abierto_lo=True)
    T = _rango(_req(c, "T", que), f"{que}: T (años)", 0, abierto_lo=True)
    r = _num(_req(c, "r", que), f"{que}: r") / PCT
    modelo = p["modelo"]
    black = modelo == "Black-76" or c.get("subyacente") == "futuro"
    if black and c.get("q") is not None:
        raise ErrorFicha(f"{que}: Black-76 (subyacente futuro) no lleva dividendo q")
    q = r if black else _num(_req(c, "q", que), f"{que}: q") / PCT
    call, americana = tipo == "call", estilo == "americana"
    if americana and modelo != "CRR":
        modelo = "CRR"
        lim.append(f"{que}: americana: se valora con CRR (DER-OPT-001, «Método»)")
    N = p["pasos"]
    lo, hi = _cotas(S, K, T, r, q, call, americana)

    def precio(s: float) -> float:
        if modelo == "CRR":
            return crr_promedio(S, K, T, r, q, s, call, americana, N)["precio"]
        return bsm(S, K, T, r, q, s, call)

    tiene_p, tiene_s = c.get("precio") is not None, c.get("sigma") is not None
    if tiene_p == tiene_s:
        raise ErrorFicha(f"{que}: aporte el precio de la opción o σ (uno de los dos)")
    if tiene_p:
        pr = _num(c["precio"], f"{que}: precio")
        if not lo < pr < hi:
            raise ErrorFicha(f"{que}: rechazo: el precio {pr:g} viola las cotas de no arbitraje ({lo:g}, {hi:g})")
        vg = None if modelo == "CRR" else (lambda s: griegas_bsm(S, K, T, r, q, s, call, black)["vega"] * PCT)
        s0 = math.sqrt(2 * math.pi / T) * pr / S   # arranque de Brenner y Subrahmanyam (1988), aproximación ATM
        sigma = vol_implicita(precio, vg, pr, p["tol_iv"], u["iteraciones_max"], s0 if s0 > 0 else 1.0)
    else:
        sigma = _rango(c["sigma"], f"{que}: sigma", 0, abierto_lo=True) / PCT
        pr = precio(sigma)
    if modelo == "CRR":
        arbol = crr_promedio(S, K, T, r, q, sigma, call, americana, N)
        h = u["punto"] / PCT
        if sigma - h <= 0:
            raise ErrorFicha(f"{que}: σ ≤ 1 punto: vega del árbol no definida")
        g = {"delta": arbol["delta"], "gamma": arbol["gamma"], "theta_dia": arbol["theta_dia"],
             "vega": (precio(sigma + h) - precio(sigma - h)) / 2,
             "rho": (crr_promedio(S, K, T, r + h, q if not black else q + h, sigma, call, americana, N)["precio"]
                     - crr_promedio(S, K, T, r - h, q if not black else q - h, sigma, call, americana, N)["precio"]) / 2}
    else:
        g = griegas_bsm(S, K, T, r, q, sigma, call, black)
    fila: dict[str, Any] = {"tipo": tipo, "estilo": estilo, "modelo": "Black-76" if black and modelo != "CRR" else modelo,
                            "precio": pr, "iv_pct": sigma * PCT, **g}
    # Paridad put-call (europeas) y segunda vía CRR frente a BSM
    if not americana:
        otra = bsm(S, K, T, r, q, sigma, not call) if modelo != "CRR" else crr_promedio(
            S, K, T, r, q, sigma, not call, False, N)["precio"]
        c_, p_ = (pr, otra) if call else (otra, pr)
        fila["paridad"] = {"call_menos_put": c_ - p_, "forward_descontado": S * math.exp(-q * T) - K * math.exp(-r * T)}
        fila["paridad"]["error"] = fila["paridad"]["call_menos_put"] - fila["paridad"]["forward_descontado"]
        if modelo != "CRR":
            arbol_p = crr_promedio(S, K, T, r, q, sigma, call, False, N)["precio"]
            fila["segunda_via"] = {"crr": arbol_p, "diferencia": arbol_p - pr, "pasos": N}
        else:
            fila["segunda_via"] = {"bsm": bsm(S, K, T, r, q, sigma, call), "diferencia": pr - bsm(S, K, T, r, q, sigma, call)}
    else:
        fila["prima_ejercicio_anticipado"] = pr - bsm(S, K, T, r, q, sigma, call)
    return fila


def _interp_en(x: float, xs: np.ndarray, ys: np.ndarray) -> float | None:
    if len(xs) < 2 or x < xs.min() or x > xs.max():
        return None
    o = np.argsort(xs)
    return float(np.interp(x, xs[o], ys[o]))


def _vencimiento(d: dict[str, Any], p: dict[str, Any], u: dict[str, Any], lim: list[str], que: str) -> dict[str, Any]:
    T = _rango(_req(d, "T", que), f"{que}: T", 0, abierto_lo=True)
    Fw = _rango(_req(d, "forward", que), f"{que}: forward", 0, abierto_lo=True)
    r = _num(_req(d, "r", que), f"{que}: r") / PCT
    K = _vector(_req(d, "strikes", que), f"{que}: strikes")
    vol = _vector(_req(d, "vol_pct", que), f"{que}: vol_pct") / PCT
    if len(K) < u["strikes_minimos"]:
        raise ErrorFicha(f"{que}: {len(K)} precios de ejercicio (< {u['strikes_minimos']}): entradas mínimas de la ficha")
    _tope(len(K), u["strikes_maximos"], f"{que}: strikes")
    if len(K) != len(vol) or np.any(K <= 0) or np.any(np.diff(K) <= 0) or np.any(vol <= 0):
        raise ErrorFicha(f"{que}: strikes positivos crecientes y una volatilidad positiva por strike")
    atm = _interp_en(Fw, K, vol)
    sd = vol * math.sqrt(T)
    dc = stats.norm.cdf((np.log(Fw / K) + 0.5 * sd * sd) / sd)   # delta forward de la call, sin prima [PROPUESTO]
    lado_c, lado_p = K >= Fw, K <= Fw
    s_c = _interp_en(u["delta_rr"], dc[lado_c], vol[lado_c])
    s_p = _interp_en(1 - u["delta_rr"], dc[lado_p], vol[lado_p])
    rr = bf = None
    if s_c is not None and s_p is not None:
        rr = (s_c - s_p) * PCT
        if atm is not None:
            bf = ((s_c + s_p) / 2 - atm) * PCT
    else:
        lim.append(f"{que}: sin cobertura de deltas 25: risk reversal y butterfly no calculados")
    if atm is None:
        lim.append(f"{que}: forward fuera de los strikes: volatilidad ATM no calculada")
    out: dict[str, Any] = {"T": T, "atm_pct": None if atm is None else atm * PCT, "rr25_pct": rr, "bf25_pct": bf}
    if p["densidad"]:
        C = np.array([bsm(Fw, float(k), T, 0.0, 0.0, float(s), True) for k, s in zip(K, vol)])   # Black sin descontar
        dens = [float(2 * ((C[i + 1] - C[i]) / (K[i + 1] - K[i]) - (C[i] - C[i - 1]) / (K[i] - K[i - 1]))
                      / (K[i + 1] - K[i - 1])) for i in range(1, len(K) - 1)]
        if any(x < 0 for x in dens):
            lim.append(f"{que}: densidad negativa en algún strike (sonrisa con arbitraje de mariposa)")
        out["densidad"] = {"strikes": K[1:-1], "q": dens, "descuento": math.exp(-r * T)}
    return out


@_cerrado("DER-OPT-001")
def f_der_opt(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """DER-OPT-001 · Opciones genéricas: BSM, Black-76, CRR, griegas y volatilidad implícita; lectura de la superficie.

    ``valores``: ``contratos`` (o ``contrato``) = [{"S", "K", "T" (años), "r" (%), "q" (%), "tipo" (call | put),
    "estilo" (europea | americana), "precio" o "sigma" (%), opcional "subyacente": "futuro" (Black-76)}]; opcional
    ``superficie`` = {"vencimientos": [{"T", "forward", "r" (%), "strikes" (≥ 5), "vol_pct"}]}.
    """
    F = "DER-OPT-001"
    p = _parametros(F, params)
    u = UMBRALES[F]
    v = ent["valores"]
    lim: list[str] = []
    if v.get("contratos") is None and v.get("contrato") is None and v.get("superficie") is None:
        raise ErrorFicha(f"{F}: falta «contratos» o «superficie»")
    contratos = _lista(v["contratos"], f"{F}: contratos", 1) if v.get("contratos") is not None else (
        [v["contrato"]] if v.get("contrato") is not None else [])
    # QA r01 de T-112, H-01: cotas de tamaño. Lo caro es el árbol (cada contrato con volatilidad implícita lo recalcula
    # una veintena de veces), así que se acota aparte cuántos contratos se valoran con él.
    _tope(len(contratos), u["contratos_maximos"], f"{F}: contratos")
    _tope(sum(1 for c in contratos if p["modelo"] == "CRR" or (isinstance(c, dict) and c.get("estilo") == "americana")),
          u["contratos_arbol_maximos"], f"{F}: contratos valorados con el árbol CRR (americanas o modelo CRR)")
    tabla = [_contrato(_dict(c, f"{F}: contratos[{i}]"), p, u, lim, f"{F}: contratos[{i}]") for i, c in enumerate(contratos)]
    sup = None
    if v.get("superficie") is not None:
        vs = _lista(_dict(v["superficie"], f"{F}: superficie").get("vencimientos"), f"{F}: superficie.vencimientos", 1)
        _tope(len(vs), u["vencimientos_maximos"], f"{F}: superficie.vencimientos")
        filas = [_vencimiento(_dict(d, f"{F}: vencimientos[{i}]"), p, u, lim, f"{F}: vencimientos[{i}]")
                 for i, d in enumerate(vs)]
        if any(b["T"] <= a["T"] for a, b in pairwise(filas)):
            raise ErrorFicha(f"{F}: vencimientos de la superficie no crecientes")
        sup = {"vencimientos": filas,
               "estructura_temporal_atm": [{"T": f_["T"], "atm_pct": f_["atm_pct"]} for f_ in filas]}
    return {"contratos": tabla, "superficie": sup}, lim


# ================================================================== registro de fichas
FICHAS_TOL: dict[str, float] = {
    "ACC-VAL-001": 1e-8, "ACC-ERP-001": 1e-6, "ACC-FACT-001": 1e-8, "FIR-PRICE-001": 1e-10, "FIR-CURVE-001": 1e-6,
    "FIR-CARRY-001": 1e-10, "FIR-SPREAD-001": 1e-8, "FX-MOM-001": 1e-10, "FX-PPA-001": 1e-8, "DER-OPT-001": 1e-8,
}

FICHAS: dict[str, dict[str, Any]] = {
    "ACC-VAL-001": {"fn": f_acc_val, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA",
                    "ri": "valor = precio de mercado (brecha); RI-CM para previsión", "tol": FICHAS_TOL["ACC-VAL-001"]},
    "ACC-ERP-001": {"fn": f_acc_erp, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-MH",
                    "tol": FICHAS_TOL["ACC-ERP-001"]},
    "ACC-FACT-001": {"fn": f_acc_fact, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA",
                     "ri": "CAPM con β = 1", "tol": FICHAS_TOL["ACC-FACT-001"]},
    "FIR-PRICE-001": {"fn": f_fir_price, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA",
                      "ri": "RI-NA (cálculo); RI-PA para previsión de rendimientos", "tol": FICHAS_TOL["FIR-PRICE-001"]},
    "FIR-CURVE-001": {"fn": f_fir_curve, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA",
                      "ri": "interpolación lineal (ajuste); RI-PA (previsión)", "tol": FICHAS_TOL["FIR-CURVE-001"]},
    "FIR-CARRY-001": {"fn": f_fir_carry, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA",
                      "ri": "curva forward realizada y RI-PA", "tol": FICHAS_TOL["FIR-CARRY-001"]},
    "FIR-SPREAD-001": {"fn": f_fir_spread, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA",
                       "ri": "RI-PA y RI-MH del diferencial", "tol": FICHAS_TOL["FIR-SPREAD-001"]},
    "FX-MOM-001": {"fn": f_fx_mom, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-PA",
                   "tol": FICHAS_TOL["FX-MOM-001"]},
    "FX-PPA-001": {"fn": f_fx_ppa, "modulo": "MC-03", "version": "1.1", "cifra": "ESTADISTICA",
                   "ri": "RI-PA del tipo de cambio", "tol": FICHAS_TOL["FX-PPA-001"]},
    "DER-OPT-001": {"fn": f_der_opt, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA",
                    "ri": "volatilidad realizada histórica (RI-EWMA)", "tol": FICHAS_TOL["DER-OPT-001"]},
}


# ================================================================== datos sintéticos de los casos de control
# Todos deterministas (sin azar): sendas trigonométricas y fórmulas cerradas. Cada caso comprueba la identidad entera de
# la «Verificación» de su ficha con datos que no anulan ninguno de sus términos.
def _bono_datos(cupon: float, f: int, liq: str, venc: str, conv: str, **extra: Any) -> dict[str, Any]:
    return {"cupon": cupon, "frecuencia": f, "liquidacion": liq, "vencimiento": venc, "convencion": conv, **extra}


def _precio_por_rendimiento(v: dict[str, Any], y: float) -> float:
    """Ida y vuelta por la vía pública: el precio limpio que da la ficha con el rendimiento `y`."""
    w = {k: x for k, x in v.items() if k != "precio_limpio"}
    return float(f_fir_price({"valores": {**w, "rendimiento": y}}, {})[0]["precio_limpio"])


_BONO_SV = _bono_datos(2.0, 1, "2026-02-10", "2046-02-10", "ACT/ACT-ICMA", precio_limpio=88.0)
# Fuera de fecha de cupón. ACT/ACT ICMA: cupón anterior 15-05-2026, siguiente 15-11-2026 (A = 182, E = 184 días).
# 30E/360 con el día 31: anterior 31-08-2026, siguiente 28-02-2027, liquidación 15-10-2026 (A = 30·2 + 15 − 30 = 45;
# E = 360/2 = 180).
_BONO_ACT = _bono_datos(4.0, 2, "2026-11-13", "2034-05-15", "ACT/ACT-ICMA", rendimiento=3.7)
_BONO_30E = _bono_datos(5.0, 2, "2026-10-15", "2031-08-31", "30E/360", rendimiento=4.6)
_CORRIDO = {"ACT/ACT-ICMA": ("2026-11-15", 182, 184), "30E/360": ("2027-02-28", 45, 180)}


def _fuera_de_cupon(r: dict[str, Any], datos: dict[str, Any], sig: str, A: int, E: int) -> bool:
    """Cupón corrido = (C/f)·A/E de la convención, y precio sucio = (C/f + precio sucio en el cupón siguiente)
    descontado w = 1 − A/E periodos al mismo rendimiento (el precio en el cupón siguiente, por la vía pública)."""
    f, cf = datos["frecuencia"], datos["cupon"] / datos["frecuencia"]
    siguiente = f_fir_price({"valores": {**datos, "liquidacion": sig}}, {})[0]["precio_sucio"]
    v = 1 / (1 + datos["rendimiento"] / PCT / f)
    tol = FICHAS_TOL["FIR-PRICE-001"]
    return _cerca_rel(r["cupon_corrido"], cf * A / E, tol) and _cerca_rel(r["precio_sucio"], (cf + siguiente) * v ** (1 - A / E), tol)


def _segunda_via_precio(r: dict[str, Any]) -> bool:
    """ΔP exacto (reprecio por la vía pública a y + Δy) = variación exacta; aproximaciones de orden 1 y 2 con D_mod y
    convexidad; y el error de orden 2 menor que el de orden 1."""
    s, tol = r["segunda_via"], FICHAS_TOL["FIR-PRICE-001"]
    dy = s["delta_y_pb"] / PB_POR_UNIDAD
    sucio = r["precio_sucio"]
    w = {k: x for k, x in _BONO_SV.items() if k != "precio_limpio"}
    exacto = f_fir_price({"valores": {**w, "rendimiento": r["ytm_pct"] + s["delta_y_pb"] / PB_POR_PUNTO}}, {})[0][
        "precio_sucio"] - sucio
    o1 = -r["d_mod"] * sucio * dy
    o2 = o1 + 0.5 * r["convexidad"] * sucio * dy * dy
    menos = f_fir_price({"valores": {**w, "rendimiento": r["ytm_pct"] - s["delta_y_pb"] / PB_POR_PUNTO}}, {})[0][
        "precio_sucio"] - sucio
    convexidad_num = (exacto + menos) / (sucio * dy * dy)   # segunda derivada del reprecio exacto (error de orden Δy²)
    return (_cerca_rel(s["variacion_exacta"], exacto, tol) and _cerca_rel(s["aprox_duracion"], o1, tol)
            and _cerca_rel(s["aprox_duracion_convexidad"], o2, tol)
            and abs(o2 - exacto) < abs(o1 - exacto) and _cerca_rel(s["error_duracion_convexidad"], abs(o2 - exacto), tol)
            and abs(convexidad_num - r["convexidad"]) <= dy * r["convexidad"])


_PLAZOS_NSS = [0.25, 0.5, 1, 2, 3, 5, 7, 10, 15, 20, 30]
_NSS_VERDAD = {"betas": [4.0, -2.0, 1.5, -1.0], "lambdas": [1.5, 8.0]}
_NS_DL = {"betas": [3.5, -1.5, 2.0]}


def _nss_cerrada(t: float, b: list[float], lam: list[float]) -> float:
    """NSS escrita aparte (Svensson, 1994) con `math`, sin las cargas del módulo: los datos de control no heredan un
    error de la fórmula que se verifica."""
    def pendiente(x: float) -> float:
        return 1.0 if x == 0 else (1 - math.exp(-x)) / x
    y = b[0] + b[1] * pendiente(t / lam[0]) + b[2] * (pendiente(t / lam[0]) - math.exp(-t / lam[0]))
    return y + (b[3] * (pendiente(t / lam[1]) - math.exp(-t / lam[1])) if len(lam) > 1 else 0.0)


def _forward_cerrada(t: float, b: list[float], lam: list[float]) -> float:
    """Forward instantáneo f(τ) = d(τ·y)/dτ de la NSS, derivado a mano."""
    x1 = t / lam[0]
    f = b[0] + b[1] * math.exp(-x1) + b[2] * x1 * math.exp(-x1)
    return f + (b[3] * (t / lam[1]) * math.exp(-t / lam[1]) if len(lam) > 1 else 0.0)


def sintetico_curva(betas: list[float], lambdas: list[float], plazos: list[float] | None = None) -> dict[str, Any]:
    pl = plazos or _PLAZOS_NSS
    return {"curva": {"fecha": "2026-11-06", "plazos": list(pl),   # conocible en el corte de las pruebas (H-07)
                      "rendimientos": [_nss_cerrada(float(t), betas, lambdas) for t in pl]}}


def _limites_y_forward(r: dict[str, Any]) -> bool:
    """τ → ∞ ⇒ y → β₀; τ → 0 ⇒ y → β₀ + β₁ (también para la curva de la verdad) y forward de la SERIE = f(τ)."""
    b = [r["parametros"][f"beta{i}"] for i in range(4)]
    lam = [r["parametros"]["lambda1"], r["parametros"]["lambda2"]]
    return (_cerca_rel(r["verificacion"]["y_tau_infinito"], b[0], 1e-12)
            and _cerca_rel(r["verificacion"]["y_tau_0"], b[0] + b[1], 1e-12)
            and _cerca_rel(r["verificacion"]["y_tau_0"], _NSS_VERDAD["betas"][0] + _NSS_VERDAD["betas"][1],
                           FICHAS_TOL["FIR-CURVE-001"])
            and all(_cerca_rel(f, _forward_cerrada(t, b, lam), 1e-12)
                    for t, f in zip(r["curva"]["plazos"], r["curva"]["forward_pct"])))


def _cerca_rel(a: Any, b: float, tol: float) -> bool:
    return a is not None and abs(float(a) - b) <= tol * max(abs(b), 1.0)


def _recupera_nss(r: dict[str, Any], verdad: dict[str, Any], tol: float) -> bool:
    nombres = ["beta0", "beta1", "beta2", "beta3"]
    ok = all(_cerca_rel(r["parametros"][n], b, tol) for n, b in zip(nombres, verdad["betas"]))
    return ok and all(_cerca_rel(r["parametros"][f"lambda{i + 1}"], x, tol) for i, x in enumerate(verdad["lambdas"]))


def sintetico_spread(n: int = 12 * SEMANAS_POR_ANIO + 1, actual: float | None = None) -> dict[str, Any]:
    fechas = [(date(2014, 11, 14) + pd.Timedelta(weeks=i)).isoformat() for i in range(n)]
    s = [120.0 + 40 * math.sin(i * 0.031) + 10 * math.sin(i * 0.17) for i in range(n)]
    if actual is not None:
        s[-1] = actual
    return {"historia": {"fechas": fechas, "diferenciales_pb": s,
                         "duraciones": [5.0 + 0.5 * math.sin(i * 0.05) for i in range(n)]},
            "impagos": {"fuente": "tasas sintéticas de control", "por_rating": {"BBB": {"pd_anual": 0.002, "peso": 0.7},
                                                                              "BB": {"pd_anual": 0.01, "peso": 0.3}}},
            "duracion_diferencial": 4.5, "medida": "OAS", "incluye_recesion": True}


def sintetico_ppa(n: int, infl_base: float, infl_cot: float, desvio_final: float = 0.0, s0: float = 1.1,
                  ruido: bool = False) -> dict[str, Any]:
    """Serie mensual: índices con inflación mensual constante; spot sobre la senda PPA (× e^{desvío} al final)."""
    fechas = [d.date().isoformat() for d in pd.date_range("2001-01-31", periods=n, freq="ME")]
    pb = [100 * (1 + infl_base) ** i for i in range(n)]
    pc = [100 * (1 + infl_cot) ** i for i in range(n)]
    S = [s0 * (pc[i] / pc[0]) / (pb[i] / pb[0]) * (math.exp(0.05 * math.sin(i * 0.2)) if ruido else 1.0) for i in range(n)]
    S[-1] *= math.exp(desvio_final)
    meta = {"base_indice": "2001=100", "vintage": "2026-10-15", "canasta": "IPC general", "periodicidad": "mensual"}
    return {"par": "EUR/USD", "fechas": fechas, "tipo_cambio": S,
            "indices": {"base": {"valores": pb, **meta}, "cotizada": {"valores": pc, **meta}}}


def sintetico_ppa_ar1(n: int, phi: float, q0: float) -> dict[str, Any]:
    """q_t = φ^t·q₀ exacto (sin ruido): el AR(1) recupera φ y la vida media ln 0,5/ln φ meses."""
    v = sintetico_ppa(n, 0.001, 0.003)
    pb, pc = v["indices"]["base"]["valores"], v["indices"]["cotizada"]["valores"]
    v["tipo_cambio"] = [math.exp(q0 * phi ** i) * pc[i] / pb[i] for i in range(n)]
    return v


def sintetico_fx(n_dias: int = 560, dif: float = 2.0, amplitud: float = 0.04, inicio: str = "2024-06-03",
                 fase: float = 0.0) -> dict[str, Any]:
    fechas = [d.date().isoformat() for d in pd.bdate_range(inicio, periods=n_dias)]
    spot = [1.10 * math.exp(amplitud * math.sin(i * 0.013 + fase) + 0.002 * math.sin(i * 0.9)) for i in range(n_dias)]
    return {"direccion": "EUR/USD", "spot": {"fechas": fechas, "valores": spot},
            "diferencial_pct": {"fechas": fechas[:1], "valores": [dif]}}


def sintetico_fx_escalon() -> dict[str, Any]:
    d = sintetico_fx()
    f = d["spot"]["fechas"]
    d["diferencial_pct"] = {"fechas": [f[0], f[400], f[480]], "valores": [2.0, -1.0, 3.5]}
    return d


def _carry_sin_mirar_adelante(r: dict[str, Any]) -> bool:
    """Carry devengado tramo a tramo con el diferencial conocido al inicio de cada tramo (conocibilidad, 3.1)."""
    d = sintetico_fx_escalon()
    fechas = [_fecha(x, "") for x in d["spot"]["fechas"]]
    fd = [_fecha(x, "") for x in d["diferencial_pct"]["fechas"]]
    ok = True
    for t in r["pares"]["X"]["rendimientos_exceso"].values():
        i0 = fechas.index(_fecha(t["desde"], ""))
        carry = 0.0
        for k in range(i0 + 1, len(fechas)):
            vigente = [x for f_, x in zip(fd, d["diferencial_pct"]["valores"]) if f_ <= fechas[k - 1]][-1]
            carry += vigente / PCT * (fechas[k] - fechas[k - 1]).days / DIAS_POR_ANIO
        var = d["spot"]["valores"][-1] / d["spot"]["valores"][i0] - 1
        ok = ok and _cerca_rel(t["exceso_pct"], (var + carry) * PCT, FICHAS_TOL["FX-MOM-001"])
    return ok and r["pares"]["X"]["diferencial_actual_pct"] == 3.5


def _coherencia_fx_carry(r: dict[str, Any], datos: dict[str, Any], par: str) -> bool:
    """FX-CARRY-001 (operaciones.carry_divisas): variación cambiaria + carry·años = rentabilidad total."""
    from .operaciones import carry_divisas
    t = r["pares"][par]["rendimientos_exceso"]["12"]
    fechas = [_fecha(x, "") for x in datos["spot"]["fechas"]]
    i0, i1 = fechas.index(_fecha(t["desde"], "")), len(fechas) - 1
    anios = (fechas[i1] - fechas[i0]).days / DIAS_POR_ANIO
    d = datos["diferencial_pct"]["valores"][0] / PCT
    total = carry_divisas(d, 0.0, datos["spot"]["valores"][i0], datos["spot"]["valores"][i1], anios)["rentabilidad_total"]
    return math.isclose(t["exceso_pct"], total * PCT, rel_tol=FICHAS_TOL["FX-MOM-001"])


_ERP: dict[str, Any] = {"moneda": "USD", "nivel": 5000.0, "dividendos_12m": 75.0, "recompras_netas_12m": 50.0,
        "g5": {"valor": 4.0, "fuente": "consenso sintético", "fecha": "2026-11-01"},
        "rf_nominal_10a": {"valor": 4.0, "moneda": "USD", "fuente": "curva sintética"},
        "rf_real_10a": {"valor": 1.8, "moneda": "USD", "fuente": "curva real sintética"},
        "beneficio_adelantado": 260.0, "cape": {"valor": 30.0, "fuente": "CAPE sintético"}}


def _pv_damodaran_aparte(r: float, cf0: float, g5: float, gL: float) -> float:
    """Vía aparte: suma explícita año a año de los cinco flujos y del valor terminal de Gordon."""
    total, flujo = 0.0, cf0
    for k in range(1, 6):
        flujo *= 1 + g5
        total += flujo / (1 + r) ** k
    return total + flujo * (1 + gL) / (r - gL) / (1 + r) ** 5


def sintetico_factores(n: int = 60, ruido: bool = True) -> dict[str, Any]:
    """Factores mensuales (trigonométricos, no colineales) y un indicador r = 0,2 + 1,1·MKT + 0,3·SMB − 0,2·HML + e."""
    fechas = [d.date().isoformat() for d in pd.date_range("2020-01-31", periods=n, freq="ME")]
    nombres = ["MKT", "SMB", "HML", "RMW", "CMA", "UMD", "QMJ", "BAB"]
    fac = {k: [2.0 * math.sin(i * (0.7 + 0.37 * j) + j) + 0.1 * j for i in range(n)] for j, k in enumerate(nombres)}
    e = [0.5 * math.sin(i * 2.3 + 0.4) * math.cos(i * 0.11) if ruido else 0.0 for i in range(n)]
    r = [0.2 + 1.1 * fac["MKT"][i] + 0.3 * fac["SMB"][i] - 0.2 * fac["HML"][i] + e[i] for i in range(n)]
    return {"fechas": fechas, "rendimientos": r, "en_exceso": True, "factores": fac, "region": "Europa"}


def _nw_aparte(r: dict[str, Any], v: dict[str, Any]) -> bool:
    """Regla de rezagos L = ⌊4(T/100)^{2/9}⌋, t de Newey-West con núcleo de Bartlett escrito con bucles, α anualizado
    con capitalización compuesta (3.1) y R²."""
    nombres = r["factores"]
    n = len(v["rendimientos"])
    X = np.column_stack([np.ones(n)] + [np.array(v["factores"][k]) for k in nombres])
    y = np.array(v["rendimientos"])
    b = np.linalg.solve(X.T @ X, X.T @ y)
    e = y - X @ b
    L = math.floor(4 * (n / 100) ** (2 / 9))
    S = sum(e[t] ** 2 * np.outer(X[t], X[t]) for t in range(n))
    for lag in range(1, L + 1):
        for t in range(lag, n):
            G = (1 - lag / (L + 1)) * e[t] * e[t - lag] * np.outer(X[t], X[t - lag])
            S = S + G + G.T
    inv = np.linalg.inv(X.T @ X)
    ee = np.sqrt(np.diag(inv @ S @ inv))
    tol = FICHAS_TOL["ACC-FACT-001"]
    return (r["rezagos_nw"] == L and all(_cerca_rel(r["betas"][k]["t"], b[j + 1] / ee[j + 1], tol) for j, k in enumerate(nombres))
            and _cerca_rel(r["t_alfa"], b[0] / ee[0], tol)
            and _cerca_rel(r["alfa_anual_pct"], ((1 + b[0] / PCT) ** MESES_POR_ANIO - 1) * PCT, tol))


_FACT_LARGO = sintetico_factores(n=300)


def sintetico_val(crecimiento: float = 3.0, **extra: Any) -> dict[str, Any]:
    ejs = [{"ejercicio": 2021 + i, "fecha_presentacion": f"{2022 + i}-03-31", "moneda": "EUR", "ventas": 1000.0 + 50 * i,
            "ebit": 140.0 + 5 * i, "amortizaciones": 40.0, "capex": 50.0, "variacion_circulante": 10.0,
            "fondos_propios": 800.0 + 20 * i, "flujo_accionista": 70.0 + 2 * i} for i in range(5)]
    return {"moneda": "EUR", "ejercicios": ejs, "capitalizacion": {"valor": 1500.0, "fecha": "2026-11-06"},
            "deuda_neta": 300.0, "rf": {"valor": 3.0, "moneda": "EUR"}, "coste_deuda_pct": 4.0,
            "tasa_impositiva_legal": 25.0, "beta": {"valor": 1.1, "fuente": "ACC-FACT-001 sintética"},
            "prm": {"valor": 5.5, "fuente": "ACC-ERP-001 sintética"},
            "crecimiento_explicito": {"valor": crecimiento, "fuente": "supuesto de control"},
            "beneficio_adelantado": 110.0, **extra}


def _identidad_ev(r: dict[str, Any]) -> bool:
    return math.isclose(sum(r["vp_flujos"]) + r["vp_valor_terminal"], r["ev"], rel_tol=FICHAS_TOL["ACC-VAL-001"])


def _inverso_aparte(r: dict[str, Any]) -> bool:
    """Vía aparte: el EV con el crecimiento implícito, descontado año a año, iguala el EV de mercado."""
    w, g_t, g, n = r["tasa_descuento_pct"] / PCT, r["g_terminal_pct"] / PCT, r["dcf_inverso"]["crecimiento_implicito_pct"] / PCT, 5
    flujo, ev = r["flujo_base"], 0.0
    for k in range(1, n + 1):
        flujo *= 1 + g
        ev += flujo / (1 + w) ** k
    ev += flujo * (1 + g_t) / (w - g_t) / (1 + w) ** n
    return math.isclose(ev, r["ev_mercado"], rel_tol=UMBRALES["ACC-VAL-001"]["tol_inverso"])


_OPT_REF: dict[str, Any] = {"S": 100, "K": 100, "T": 1, "r": 5, "q": 0, "estilo": "europea", "sigma": 20}
_OPT_PAR: dict[str, Any] = {"S": 105, "K": 95, "T": 0.75, "r": 3, "q": 1.5, "estilo": "europea", "sigma": 25}


def _paridad(r: dict[str, Any]) -> bool:
    c, p_ = r["contratos"][0]["precio"], r["contratos"][1]["precio"]
    S, K, T, rr, q = (_OPT_PAR[k] for k in ("S", "K", "T", "r", "q"))
    return math.isclose(c - p_, S * math.exp(-q / PCT * T) - K * math.exp(-rr / PCT * T), rel_tol=FICHAS_TOL["DER-OPT-001"])


def _args(c: dict[str, Any]) -> tuple[float, float, float, float, float, float]:
    return (c["S"], c["K"], c["T"], c["r"] / PCT, c["q"] / PCT, c["sigma"] / PCT)


def _segunda_via_crr(r: dict[str, Any]) -> bool:
    """Precio BSM y árbol CRR (N/N + 1) de cada europea, su diferencia, y |CRR − BSM| ≤ precio/N (orden 1/N)."""
    N = PARAMETROS_POR_DEFECTO["DER-OPT-001"]["pasos"]
    ok = True
    for fila, c in zip(r["contratos"], ({**_OPT_PAR, "tipo": "call"}, {**_OPT_REF, "tipo": "put"})):
        call = c["tipo"] == "call"
        b, a = bsm(*_args(c), call), crr_promedio(*_args(c), call, False, N)["precio"]
        sv = fila["segunda_via"]
        ok = ok and _cerca_rel(fila["precio"], b, FICHAS_TOL["DER-OPT-001"]) and _cerca_rel(sv["crr"], a, 1e-12) \
            and _cerca_rel(sv["diferencia"], a - b, FICHAS_TOL["DER-OPT-001"]) and abs(a - b) <= b / sv["pasos"]
    return ok


def _americanas(r: dict[str, Any]) -> bool:
    """Put americana = árbol con ejercicio anticipado y > europea BSM; call americana sin dividendo = europea (orden 1/N)."""
    N = PARAMETROS_POR_DEFECTO["DER-OPT-001"]["pasos"]
    put, call = r["contratos"]
    pa = crr_promedio(*_args(_OPT_REF), False, True, N)["precio"]
    ca = crr_promedio(*_args(_OPT_REF), True, True, N)["precio"]
    pe, ce = bsm(*_args(_OPT_REF), False), bsm(*_args(_OPT_REF), True)
    return (_cerca_rel(put["precio"], pa, 1e-12) and _cerca_rel(put["prima_ejercicio_anticipado"], pa - pe, 1e-10)
            and pa > pe and _cerca_rel(call["precio"], ca, 1e-12)
            and _cerca_rel(call["prima_ejercicio_anticipado"], ca - ce, 1e-10) and abs(ca - ce) <= ce / N)


def _griegas_por_diferencias(r: dict[str, Any]) -> bool:
    """Δ, Γ, vega (por punto), θ (por día) y ρ (por punto) = derivadas centrales del precio BSM. Paso y tolerancia
    relativos √tol de la ficha (paso óptimo de una diferencia central)."""
    h = FICHAS_TOL["DER-OPT-001"] ** 0.5
    ok = True
    for fila in r["contratos"]:
        call = fila["tipo"] == "call"
        S, K, T, rr, q, s = _args(_OPT_PAR)

        def P(S: float = S, T: float = T, rr: float = rr, s: float = s, call: bool = call, K: float = K,
              q: float = q) -> float:
            return bsm(S, K, T, rr, q, s, call)
        dS = h * S
        num = {"delta": (P(S=S + dS) - P(S=S - dS)) / (2 * dS),
               "gamma": (P(S=S + dS) - 2 * P() + P(S=S - dS)) / (dS * dS),
               "vega": (P(s=s + h) - P(s=s - h)) / (2 * h) / PCT,
               "theta_dia": -(P(T=T + h) - P(T=T - h)) / (2 * h) / DIAS_POR_ANIO,
               "rho": (P(rr=rr + h) - P(rr=rr - h)) / (2 * h) / PCT}
        ok = ok and all(abs(fila[k] - x) <= h * max(abs(x), h) for k, x in num.items())
    return ok


CASOS_CONTROL: dict[str, list[dict[str, Any]]] = {
    "FIR-PRICE-001": [
        {"nombre": "cupón = rendimiento (en fecha de cupón) ⇒ precio 100",
         "datos": [{"valores": _bono_datos(4.25, 2, "2026-03-15", "2033-03-15", "ACT/ACT-ICMA", rendimiento=4.25)}],
         "parametros": {},
         "comprobar": lambda r: _cerca_rel(r["precio_limpio"], NOMINAL, FICHAS_TOL["FIR-PRICE-001"])
         and r["cupon_corrido"] == 0},
        {"nombre": "10 años, 5 % anual ⇒ D_mac 8,1078 y D_mod 7,7217",
         "datos": [{"valores": _bono_datos(5.0, 1, "2026-01-15", "2036-01-15", "ACT/ACT-ICMA", precio_limpio=100.0)}],
         "parametros": {},
         "comprobar": lambda r: round(r["d_macaulay"], 4) == 8.1078 and round(r["d_mod"], 4) == 7.7217
         and _cerca_rel(r["ytm_pct"], 5.0, FICHAS_TOL["FIR-PRICE-001"])},
        {"nombre": "ida y vuelta precio → rendimiento → precio (fuera de fecha de cupón, 30E/360)",
         "datos": [{"valores": _bono_datos(3.5, 2, "2026-11-13", "2031-06-30", "30E/360", precio_limpio=97.25)}],
         "parametros": {},
         "comprobar": lambda r: _cerca_rel(_precio_por_rendimiento(_bono_datos(
             3.5, 2, "2026-11-13", "2031-06-30", "30E/360"), r["ytm_pct"]), 97.25, FICHAS_TOL["FIR-PRICE-001"])
         and r["cupon_corrido"] > 0},
        {"nombre": "fuera de fecha de cupón (ACT/ACT ICMA): corrido = C/f·A/E y precio = (C/f + P siguiente)·v^(1 − A/E)",
         "datos": [{"valores": _BONO_ACT}], "parametros": {},
         "comprobar": lambda r: _fuera_de_cupon(r, _BONO_ACT, *_CORRIDO["ACT/ACT-ICMA"])},
        {"nombre": "fuera de fecha de cupón (30E/360 con día 31): corrido = C/f·45/180 y precio descontado",
         "datos": [{"valores": _BONO_30E}], "parametros": {},
         "comprobar": lambda r: _fuera_de_cupon(r, _BONO_30E, *_CORRIDO["30E/360"])},
        {"nombre": "segunda vía: duración + convexidad frente al reprecio exacto a y + Δy (y mejora a la duración sola)",
         "datos": [{"valores": _BONO_SV}], "parametros": {"delta_y": 25}, "comprobar": _segunda_via_precio},
    ],
    "FIR-CURVE-001": [
        {"nombre": "NSS recupera los parámetros de una curva NSS exacta (RMSE < 1e-4 pb)",
         "datos": [{"valores": sintetico_curva(**_NSS_VERDAD)}], "parametros": {},
         "comprobar": lambda r: r["modelo"] == "NSS" and r["rmse_pb"] < 1e-4
         and _recupera_nss(r, _NSS_VERDAD, FICHAS_TOL["FIR-CURVE-001"])},
        {"nombre": "τ → ∞ ⇒ y → β₀; τ → 0 ⇒ y → β₀ + β₁; forward de la serie = d(τ·y)/dτ",
         "datos": [{"valores": sintetico_curva(**_NSS_VERDAD)}], "parametros": {}, "comprobar": _limites_y_forward},
        {"nombre": "NS con λ de Diebold-Li recupera los β exactos (MCO)",
         "datos": [{"valores": sintetico_curva(_NS_DL["betas"], [1 / (UMBRALES["FIR-CURVE-001"]["lambda_diebold_li_mes"]
                                                                       * MESES_POR_ANIO)], _PLAZOS_NSS[:7])}],
         "parametros": {"modelo": "NS", "lambda": "diebold_li"},
         "comprobar": lambda r: all(_cerca_rel(r["parametros"][f"beta{i}"], b, 1e-10) for i, b in enumerate(_NS_DL["betas"]))},
    ],
    "FIR-CARRY-001": [
        {"nombre": "curva plana ⇒ rolldown 0 (y carry = (y − financiación)·Δt)",
         "datos": [{"valores": {"curva": {"plazos": [0.25, 1, 2, 5, 10], "rendimientos": [3.0] * 5}, "tramo": 5,
                                "financiacion": 1.0}}], "parametros": {"delta_t": 3},
         "comprobar": lambda r: r["tramos"]["5"]["rolldown_pb"] == 0
         and _cerca_rel(r["tramos"]["5"]["carry_pb"], (0.03 - 0.01) * 3 / MESES_POR_ANIO * PB_POR_UNIDAD,
                        FICHAS_TOL["FIR-CARRY-001"])
         and r["tramos"]["5"]["total_pb"] == r["tramos"]["5"]["carry_pb"]},
        {"nombre": "rolldown = −D_mod·[y(τ − Δt) − y(τ)] y subida de equilibrio = total/D_mod (curva con pendiente)",
         "datos": [{"valores": {"curva": {"plazos": [1, 2, 5, 10], "rendimientos": [1.0, 2.0, 3.0, 4.0]}, "tramo": 5,
                                "financiacion": 1.0}}], "parametros": {"delta_t": 6},
         "comprobar": lambda r: _cerca_rel(r["tramos"]["5"]["rolldown_pb"],
                                           -5 / 1.03 * ((2 + 2.5 / 3) / PCT - 0.03) * PB_POR_UNIDAD, FICHAS_TOL["FIR-CARRY-001"])
         and _cerca_rel(r["tramos"]["5"]["subida_equilibrio_pb"], r["tramos"]["5"]["total_pb"] * 1.03 / 5,
                        FICHAS_TOL["FIR-CARRY-001"])},
        {"nombre": "segunda vía: reprecio a t + Δt con curva plana = (1 + y)^Δt − 1 − financiación·Δt",
         "datos": [{"valores": {"curva": {"plazos": [0.25, 1, 2, 5, 10], "rendimientos": [3.0] * 5}, "tramo": 5,
                                "financiacion": 1.0}}], "parametros": {"delta_t": 3},
         "comprobar": lambda r: _cerca_rel(r["tramos"]["5"]["segunda_via"]["rentabilidad_exceso_pb"],
                                           (1.03 ** 0.25 - 1 - 0.01 * 0.25) * PB_POR_UNIDAD, FICHAS_TOL["FIR-CARRY-001"])},
    ],
    "FIR-SPREAD-001": [
        {"nombre": "percentil del máximo histórico = 1", "datos": [{"valores": sintetico_spread(actual=400.0)}],
         "parametros": {}, "comprobar": lambda r: r["percentil"] == 1.0 and r["diferencial_pb"] == 400.0},
        {"nombre": "exceso sobre pérdida esperada = s − PD·(1 − R) y ampliación de equilibrio = s/duración",
         "datos": [{"valores": sintetico_spread(actual=150.0)}], "parametros": {"recuperacion": 0.35},
         "comprobar": lambda r: _cerca_rel(r["exceso_perdida_esperada_pb"],
                                           150.0 - (0.7 * 0.002 + 0.3 * 0.01) * (1 - 0.35) * PB_POR_UNIDAD,
                                           FICHAS_TOL["FIR-SPREAD-001"])
         and _cerca_rel(r["ampliacion_equilibrio_pb"], 150.0 / 4.5, FICHAS_TOL["FIR-SPREAD-001"])},
    ],
    "FX-MOM-001": [
        {"nombre": "coherencia con FX-CARRY-001: exceso a 12 meses = variación cambiaria + carry·años",
         "datos": [{"valores": {"pares": {"EURUSD": sintetico_fx()}}}], "parametros": {"volatilidad": "realizada"},
         "comprobar": lambda r: _coherencia_fx_carry(r, sintetico_fx(), "EURUSD")},
        {"nombre": "carry con el diferencial conocido al inicio de cada tramo (diferencial escalonado)",
         "datos": [{"valores": {"pares": {"X": sintetico_fx_escalon()}}}], "parametros": {"volatilidad": "realizada"},
         "comprobar": _carry_sin_mirar_adelante},
        {"nombre": "TSMOM = signo del exceso a 12 meses; rango transversal: el mayor tiene percentil 1",
         "datos": [{"valores": {"pares": {"A": sintetico_fx(dif=4.0, fase=0.5), "B": sintetico_fx(dif=-3.0, fase=2.0),
                                          "C": sintetico_fx(dif=0.5, fase=4.0)}}}],
         "parametros": {"volatilidad": "realizada"},
         "comprobar": lambda r: all(t["senal_tsmom"] == int(np.sign(t["rendimientos_exceso"]["12"]["exceso_pct"]))
                                    for t in r["pares"].values())
         and len({t["senal_tsmom"] for t in r["pares"].values()}) > 1
         and r["rangos_transversales"]["12"][max(r["pares"], key=lambda k: r["pares"][k]["rendimientos_exceso"]["12"][
             "exceso_pct"])]["percentil"] == 1.0},
    ],
    "FX-PPA-001": [
        {"nombre": "inflación constante igual y cambio constante ⇒ desviación nula",
         "datos": [{"valores": sintetico_ppa(36, 0.002, 0.002)}], "parametros": {},
         "comprobar": lambda r: all(abs(x["desviacion_pct"]) <= FICHAS_TOL["FX-PPA-001"] for x in r["serie_desviacion_pct"])},
        {"nombre": "el cambio sigue la PPA con inflaciones distintas ⇒ desviación nula",
         "datos": [{"valores": sintetico_ppa(60, 0.001, 0.004)}], "parametros": {},
         "comprobar": lambda r: all(abs(x["desviacion_pct"]) <= FICHAS_TOL["FX-PPA-001"] for x in r["serie_desviacion_pct"])
         and r["inflacion_acumulada_pct"]["cotizada"] > r["inflacion_acumulada_pct"]["base"]},
        {"nombre": "cambio un 10 % sobre la senda ⇒ desviación final = 100·ln 1,1",
         "datos": [{"valores": sintetico_ppa(48, 0.001, 0.003, desvio_final=math.log(1.1))}], "parametros": {},
         "comprobar": lambda r: _cerca_rel(r["desviacion_final_pct"], PCT * math.log(1.1), FICHAS_TOL["FX-PPA-001"])},
        {"nombre": "AR(1) exacto ⇒ vida media = ln 0,5/ln φ (en años)",
         "datos": [{"valores": sintetico_ppa_ar1(25 * MESES_POR_ANIO, 0.98, 0.3)}], "parametros": {},
         "comprobar": lambda r: _cerca_rel(r["vida_media_anios"], math.log(0.5) / math.log(0.98) / MESES_POR_ANIO,
                                           FICHAS_TOL["FX-PPA-001"])},
    ],
    "ACC-ERP-001": [
        {"nombre": "con g₅ = g_L, r = rendimiento de flujo × (1 + g) + g",
         "datos": [{"valores": _ERP}], "parametros": {},
         "comprobar": lambda r: _cerca_rel(r["r_implicita_pct"], (125 / 5000 * 1.04 + 0.04) * PCT, FICHAS_TOL["ACC-ERP-001"])
         and _cerca_rel(r["prm_pp"], (125 / 5000 * 1.04 + 0.04) * PCT - 4.0, FICHAS_TOL["ACC-ERP-001"])},
        {"nombre": "r implícita con g₅ ≠ g_L reproduce el nivel (suma año a año aparte)",
         "datos": [{"valores": {**_ERP, "g5": {"valor": 9.0, "fuente": "consenso sintético", "fecha": "2026-11-01"}}}],
         "parametros": {"g_L": 3.5},
         "comprobar": lambda r: _cerca_rel(_pv_damodaran_aparte(r["r_implicita_pct"] / PCT, 125.0, 0.09, 0.035), 5000.0,
                                           FICHAS_TOL["ACC-ERP-001"])},
        {"nombre": "segunda vía: versión simple = rendimiento del beneficio − real; ECY = 1/CAPE − real",
         "datos": [{"valores": _ERP}], "parametros": {},
         "comprobar": lambda r: _cerca_rel(r["version_simple_pp"], 260 / 5000 * PCT - 1.8, 1e-12)
         and _cerca_rel(r["ecy_pp"], PCT / 30 - 1.8, 1e-12)},
    ],
    "ACC-FACT-001": [
        {"nombre": "regresión de un factor sobre sí mismo ⇒ β = 1, α = 0 (FF5 + UMD)",
         "datos": [{"valores": {**sintetico_factores(), "rendimientos": sintetico_factores()["factores"]["MKT"]}}],
         "parametros": {},
         "comprobar": lambda r: abs(r["betas"]["MKT"]["beta"] - 1) <= FICHAS_TOL["ACC-FACT-001"]
         and all(abs(r["betas"][k]["beta"]) <= FICHAS_TOL["ACC-FACT-001"] for k in r["betas"] if k != "MKT")
         and abs(r["alfa_periodo_pct"]) <= FICHAS_TOL["ACC-FACT-001"]},
        {"nombre": "segunda vía CAPM: el mercado sobre sí mismo ⇒ β = 1, α = 0",
         "datos": [{"valores": {**sintetico_factores(), "rendimientos": sintetico_factores()["factores"]["MKT"]}}],
         "parametros": {"modelo": "CAPM"},
         "comprobar": lambda r: abs(r["segunda_via_capm"]["beta_mkt"] - 1) <= FICHAS_TOL["ACC-FACT-001"]
         and abs(r["segunda_via_capm"]["alfa_anual_pct"]) <= FICHAS_TOL["ACC-FACT-001"]},
        {"nombre": "errores de Newey-West con L = ⌊4(T/100)^{2/9}⌋ (T = 300) y α anualizado compuesto",
         "datos": [{"valores": _FACT_LARGO}], "parametros": {"modelo": "FF3"},
         "comprobar": lambda r: _nw_aparte(r, _FACT_LARGO)},
        {"nombre": "con ruido: contribuciones a la varianza que suman 100 % y R² = 1 − residuo",
         "datos": [{"valores": sintetico_factores()}], "parametros": {"modelo": "FF3"},
         "comprobar": lambda r: abs(sum(r["contribuciones_varianza_pct"].values()) - PCT) <= FICHAS_TOL["ACC-FACT-001"]
         and abs(r["r2"] - (1 - r["contribuciones_varianza_pct"]["residuo"] / PCT)) <= FICHAS_TOL["ACC-FACT-001"]
         and 0 < r["contribuciones_varianza_pct"]["residuo"] < PCT and r["t_alfa"] is not None},
    ],
    "ACC-VAL-001": [
        {"nombre": "suma de VP + VT = EV", "datos": [{"valores": sintetico_val()}], "parametros": {},
         "comprobar": _identidad_ev},
        {"nombre": "g = 0 y flujo constante ⇒ perpetuidad FCF/WACC",
         "datos": [{"valores": sintetico_val(crecimiento=0.0)}], "parametros": {"g_terminal": 0},
         "comprobar": lambda r: _cerca_rel(r["ev"], r["fcff_0"] / (r["wacc_pct"] / PCT), FICHAS_TOL["ACC-VAL-001"])
         and _cerca_rel(r["wacc_pct"], (1500 * (3 + 1.1 * 5.5) + 300 * 4 * 0.75) / 1800, 1e-12)
         and _cerca_rel(r["fcff_0"], 160 * 0.75 + 40 - 50 - 10, 1e-12)},
        {"nombre": "DCF inverso: el crecimiento implícito reproduce el EV de mercado (descuento aparte)",
         "datos": [{"valores": sintetico_val()}], "parametros": {}, "comprobar": _inverso_aparte},
        {"nombre": "segunda vía: PER implícito del DCF = valor/beneficio; celda central de la sensibilidad = valor base",
         "datos": [{"valores": sintetico_val()}], "parametros": {},
         "comprobar": lambda r: _cerca_rel(r["segunda_via"]["per_implicito_dcf"], r["valor_agregado"] / 110.0, 1e-12)
         and r["sensibilidad"]["valor_agregado"][1][1] == r["valor_agregado"]},
    ],
    "DER-OPT-001": [
        {"nombre": "S = K = 100, r = 5 %, σ = 20 %, T = 1 ⇒ call 10,4506 y put 5,5735",
         "datos": [{"valores": {"contratos": [{**_OPT_REF, "tipo": "call"}, {**_OPT_REF, "tipo": "put"}]}}],
         "parametros": {},
         "comprobar": lambda r: round(r["contratos"][0]["precio"], 4) == 10.4506
         and round(r["contratos"][1]["precio"], 4) == 5.5735},
        {"nombre": "paridad put-call con dividendo: C − P = S·e^{−qT} − K·e^{−rT}",
         "datos": [{"valores": {"contratos": [{**_OPT_PAR, "tipo": "call"}, {**_OPT_PAR, "tipo": "put"}]}}],
         "parametros": {}, "comprobar": _paridad},
        {"nombre": "griegas = derivadas del precio (vega por punto de volatilidad, θ por día, ρ por punto de tipo)",
         "datos": [{"valores": {"contratos": [{**_OPT_PAR, "tipo": "call"}, {**_OPT_PAR, "tipo": "put"}]}}],
         "parametros": {}, "comprobar": _griegas_por_diferencias},
        {"nombre": "segunda vía: CRR (N/N + 1) frente a BSM en europeas, error relativo ≤ 1/N",
         "datos": [{"valores": {"contratos": [{**_OPT_PAR, "tipo": "call"}, {**_OPT_REF, "tipo": "put"}]}}],
         "parametros": {}, "comprobar": _segunda_via_crr},
        {"nombre": "volatilidad implícita: el precio a σ = 31 % devuelve σ = 31 %",
         "datos": [{"valores": {"contratos": [{**{k: x for k, x in _OPT_PAR.items() if k != "sigma"}, "tipo": "put",
                                               "precio": bsm(105, 95, 0.75, 0.03, 0.015, 0.31, False)}]}}],
         "parametros": {},
         "comprobar": lambda r: abs(r["contratos"][0]["iv_pct"] - 31.0) <= FICHAS_TOL["DER-OPT-001"] * PCT},
        {"nombre": "americanas: put ≥ europea; call sin dividendo = europea",
         "datos": [{"valores": {"contratos": [{**_OPT_REF, "tipo": "put", "estilo": "americana"},
                                              {**_OPT_REF, "tipo": "call", "estilo": "americana"}]}}],
         "parametros": {}, "comprobar": _americanas},
    ],
}
