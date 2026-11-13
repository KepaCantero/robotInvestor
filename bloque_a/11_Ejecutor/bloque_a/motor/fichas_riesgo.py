"""Fichas del Motor del Bloque A, grupo R (T-112, Motor Fase 2): riesgo, simulación, backtest y modelos.

Fuente de verdad: «Catálogo de cálculos del Motor - V5.0», fichas RISK-VAR-001, SIM-MC-001 y ML-CAL-001 (§6,
heredadas de la línea V3.0, implementadas aquí desde la ficha), BT-DSR-001, BT-PBO-001, BT-VAR-001, SCN-H-001,
ML-PRED-001 y DEC-VOI-001 (§7), con las convenciones del §3 y los casos de control del §20.

Convenciones de este módulo:

- Rendimientos simples en tanto por uno (§3.1) salvo donde la ficha pide logarítmicos (las dinámicas de SIM-MC-001 y
  la volatilidad condicional de SCN-H-001 trabajan en log, como VOL-GARCH-001, y entregan rendimientos simples).
- VaR y ES se entregan como pérdidas positivas (fracción del valor): VaR = −q₁₋ₙᵢᵥₑₗ(r), ES = −E[r | r ≤ q]. Es la
  misma convención que el ES de TCV-VIXTS-001 y DER-VRP-001, que toman el nivel de RISK-VAR-001.
- Anualización con 252 sesiones (365 en criptoactivos, `clase` = CRI) y 12 meses (§3.1).
- Determinismo: las fichas con azar exigen o fijan una semilla entera (`semilla` en los parámetros): SIM-MC-001 y
  SCN-H-001 la exigen («Rechazo sin semilla»); ML-CAL-001 y ML-PRED-001 usan la del plan o, si no llega, la de
  `PARAMETROS_POR_DEFECTO` (solo para el bootstrap del IC). BT-PBO-001 es enumeración completa (semilla null).
- Falla cerrado: lo que falta o es incoherente lanza ``ErrorFicha`` con el motivo; lo indefinido se entrega como
  ``None`` con su limitación, nunca como un número no finito (la envoltura `_cerrado` rechaza cualquier NaN o inf).
- Los umbrales de rechazo y de limitación, los rangos admitidos y las cotas de los tamaños (trayectorias, horizonte,
  réplicas, pliegues, cuantiles…) están en `UMBRALES` y no se pueden cambiar desde la petición; cada parámetro de la
  petición tiene tipo y dominio (`_validar`), y un parámetro que la ficha no declara se rechaza (QA r01 de T-112, H-01 y
  H-02).
- Configuración: los números que salen de la configuración (umbrales de HT-03, réplicas y nivel del bootstrap, sesiones
  de cada horizonte) se leen en cada llamada de ``ent["configuracion"]``, la del Motor; si el manejador se llama sin
  ella, de `config/por_defecto.yaml` (QA r01 de T-112, H-04).
- Las «Supuestos y limitaciones» de cada ficha (`ADVERTENCIAS`) van en ``resultado["advertencias"]``, no en la lista de
  limitaciones: el estado SERVED_WITH_LIMITATIONS solo señala problemas de los datos (diseño de T-112).

Interfaz de cada manejador: ``f(ent, params) -> (resultado, limitaciones)``, con
``ent = {"valores": {...}, "series": {alias: pd.Series}, "series_rol": {rol: pd.Series}, "configuracion": {...},
"fecha_corte": "AAAA-MM-DD" | None}`` (las dos últimas las añade el Motor).
"""
from __future__ import annotations

import functools
import itertools
import math
from collections.abc import Callable
from typing import Any

import numpy as np
import pandas as pd
from scipy import integrate, optimize, signal, special, stats

from ..configuracion import (
    CLASES,
    TABLA_HORIZONTES,
    parametro,
    parametros_ht03,
    sesiones_horizonte,
)
from .evaluacion import EPS as EPS_LOG_SCORE
from .evaluacion import ece as ece_fc_cal
from .operaciones import ErrorFicha

Resultado = tuple[dict[str, Any], list[str]]

# ------------------------------------------------------------------ convenciones (§3.1; no son parámetros)
SESIONES_ANIO = 252           # §3.1: anualización con 252 sesiones
SESIONES_ANIO_CRI = 365       # §3.1: 365 días naturales en criptoactivos
MESES_ANIO = 12
PCT = 100
SEMILLA_MAXIMA = int(np.iinfo(np.int64).max)   # dominio técnico de la semilla (entero de 64 bits)

# ------------------------------------------------------------------ parámetros por defecto (campo «Parámetros»)
PARAMETROS_POR_DEFECTO: dict[str, dict[str, Any]] = {
    # RISK-VAR-001 · «Parámetros»: nivel (0,975; 0,90–0,99); horizonte; metodo (historico); moneda. La ficha no da
    # horizonte por defecto: 1 periodo de los datos [PROPUESTO INC-T112-01].
    "RISK-VAR-001": {"nivel": 0.975, "horizonte": 1, "metodo": "historico", "moneda": None},
    # SIM-MC-001 · «Parámetros»: n_trayectorias (10 000; 1 000–1 000 000); horizonte; cuantiles (0,05/0,5/0,95);
    # semilla; reduccion_varianza (antitéticas). Horizonte y semilla sin valor por defecto: se exigen.
    "SIM-MC-001": {"n_trayectorias": 10_000, "horizonte": None, "cuantiles": [0.05, 0.5, 0.95], "semilla": None,
                   "reduccion_varianza": "antiteticas", "umbrales": []},
    # SCN-H-001 · «Parámetros»: n_trayectorias (10 000); cuantiles (0,1/0,5/0,9); semilla; umbrales. `horizontes`
    # (H1–H4 de la ficha; por defecto los que tienen datos) y `clase` (tipo de activo, para la tabla 8.3).
    "SCN-H-001": {"n_trayectorias": 10_000, "cuantiles": [0.1, 0.5, 0.9], "semilla": None, "umbrales": [],
                  "horizontes": None, "clase": None},
    # BT-DSR-001 · «Parámetros»: SR_referencia (0); N (obligatorio); nivel (0,95). `frecuencia` de los rendimientos
    # (diaria o mensual: las dos de «Entradas mínimas») y `clase` (CRI anualiza con 365, §3.1).
    "BT-DSR-001": {"SR_referencia": 0.0, "N": None, "nivel": 0.95, "frecuencia": "diaria", "clase": None},
    # BT-PBO-001 · «Parámetros»: S (16; 8–20, par); metrica (Sharpe).
    "BT-PBO-001": {"S": 16, "metrica": "sharpe"},
    # BT-VAR-001 · «Parámetros»: nivel (el del VaR; por defecto el de RISK-VAR-001, 0,975); significacion (0,05).
    # Para generar el VaR ex ante con RISK-VAR-001 desde una historia: metodo_var (el de RISK-VAR-001) y
    # ventana_estimacion (≥ 250 observaciones, mínimo del histórico de RISK-VAR-001). `horizonte` del VaR (1) y
    # `baja_potencia_declarada` («salvo declaración de baja potencia»).
    "BT-VAR-001": {"nivel": 0.975, "significacion": 0.05, "metodo_var": "historico", "ventana_estimacion": 250,
                   "horizonte": 1, "baja_potencia_declarada": False},
    # ML-CAL-001 · «Parámetros»: esquema (walk_forward_expansivo); horizontes; metricas (todas las aplicables).
    # Bootstrap del IC de la mejora: réplicas y nivel; sin valor en la petición, los de la configuración del Motor
    # (`evaluacion.bootstrap_replicas`, `evaluacion.nivel_ic`, los mismos que FC-EVAL-001), leídos en cada llamada
    # (None = de la configuración); semilla del plan o 12345, la de FC-EVAL-001 en el servicio [PROPUESTO INC-T112-01].
    "ML-CAL-001": {"esquema": "walk_forward_expansivo", "horizontes": None, "metricas": None,
                   "replicas": None, "nivel_ic": None, "semilla": 12345},
    # ML-PRED-001 · «Parámetros»: modelo (logistica_L2); rejilla (≤ 20 en PLAN_STD); embargo (≥ h); calibracion (auto).
    # La rejilla de λ, los pliegues y la fracción inicial no los da la ficha [PROPUESTO INC-T112-01]. IC de la mejora
    # como ML-CAL-001.
    "ML-PRED-001": {"modelo": "logistica_L2", "rejilla": [0.1, 1.0, 10.0], "embargo": None, "calibracion": "auto",
                    "pliegues": 5, "fraccion_inicial": 0.5, "replicas": None, "nivel_ic": None, "semilla": 12345},
    # DEC-VOI-001 · «Parámetros»: umbrales (F10; fijos aquí, ver `UMBRALES`); coste_uc (obligatorio: «Entradas mínimas»).
    "DEC-VOI-001": {"coste_uc": None},
}

# Umbrales de rechazo y de limitación, rangos admitidos, cotas de tamaño y constantes del método (no son parámetros de
# la petición). Cotas de tamaño (QA r01 de T-112, H-01): todo tamaño de la petición tiene tope; el horizonte máximo es el
# de H5 en sesiones (`horizontes.H5` y `calendario` de la configuración del Motor, 120 meses = 2 520 sesiones por
# defecto), que se lee en cada llamada.
_HORIZONTE_MAXIMO = "H5"
# Optimizadores (QA r01 de T-112, H-03): Nelder-Mead de la QMLE del GARCH y de la máxima verosimilitud de la GPD con
# `xatol` = `fatol` = 1e-10, cuatro órdenes por debajo de la tolerancia 1e-6 de RISK-VAR-001 y SCN-H-001, y un tope de
# 1 000 iteraciones y evaluaciones por parámetro, cinco veces el de scipy (200 por parámetro), porque con esas
# tolerancias una verosimilitud plana (β del GARCH en el borde) pide hasta ~500 evaluaciones [PROPUESTO INC-T112-01,
# técnico]. Sin convergencia ⇒ ErrorFicha.
_TOL_OPTIMIZADOR = 1e-10
_ITERACIONES_POR_PARAMETRO = 1000
UMBRALES: dict[str, dict[str, Any]] = {
    # RISK-VAR-001 · «Parámetros»: nivel 0,90–0,99. «Entradas mínimas»: ≥ 250 observaciones (≥ 500 recomendadas);
    # EVT ≥ 50 excedencias. «Aclaración y rechazo»: nivel 99 % empírico con < 500 observaciones. Umbral de EVT-POT en
    # el cuantil 0,90 de las pérdidas [PROPUESTO INC-T112-01]. Histórico filtrado con el GARCH(1,1) de `garch_qmle`
    # (VOL-GARCH-001 sin `arch`). Tolerancia 1e-6. Horizonte de 1 a H5 en sesiones (H-01).
    "RISK-VAR-001": {"rango_nivel": [0.90, 0.99], "observaciones_minimas": 250, "observaciones_recomendadas": 500,
                     "excedencias_minimas_evt": 50, "nivel_empirico_estricto": 0.99,
                     "observaciones_nivel_estricto": 500, "cuantil_umbral_evt": 0.90,
                     "metodos": ["historico", "normal", "t", "cornish_fisher", "historico_filtrado", "evt_pot"],
                     "horizonte_maximo": _HORIZONTE_MAXIMO, "tolerancia_optimizador": _TOL_OPTIMIZADOR},
    # SIM-MC-001 · «Parámetros»: n_trayectorias 1 000–1 000 000. Dinámicas de «Método». Tabla de convergencia por
    # mitades sucesivas de las trayectorias (n, n/2, n/4, n/8) [PROPUESTO INC-T112-01]. Cotas (H-01): horizonte de 1 a
    # H5 en sesiones; presupuesto de trayectorias × pasos = n_trayectorias por defecto × H5 (10 000 × 2 520: con el
    # máximo de trayectorias se llega a 25 pasos, con las de por defecto a H5) [PROPUESTO INC-T112-01]; como mucho 99
    # cuantiles y 99 umbrales (la rejilla de percentiles enteros) [PROPUESTO INC-T112-01].
    "SIM-MC-001": {"rango_n_trayectorias": [1000, 1_000_000],
                   "dinamicas": ["paseo_aleatorio", "garch", "bootstrap_filtrado", "saltos"],
                   "reducciones": ["antiteticas", "ninguna"], "mitades_convergencia": 3,
                   "horizonte_maximo": _HORIZONTE_MAXIMO,
                   "presupuesto_trayectorias_pasos": "n_trayectorias por defecto × sesiones del horizonte máximo",
                   "cuantiles_maximos": 99, "umbrales_maximos": 99},
    # SCN-H-001 · «Método»: favorable/adverso = cuantiles 80/20. «Entradas mínimas»: H1–H2 ≥ 2 años diarios.
    # «Perfiles y horizontes»: H1–H4. n_trayectorias en el rango de SIM-MC-001 (la dinámica que usa), y las cotas de
    # cuantiles y umbrales de SIM-MC-001 (H-01). Los pasos los fijan los horizontes (≤ H4).
    "SCN-H-001": {"cuantil_favorable": 0.8, "cuantil_adverso": 0.2, "anios_minimos_h12": 2,
                  "horizontes_ficha": ["H1", "H2", "H3", "H4"], "rango_n_trayectorias": [1000, 1_000_000],
                  "cuantiles_maximos": 99, "umbrales_maximos": 99, "tolerancia_optimizador": _TOL_OPTIMIZADOR},
    # BT-DSR-001 · «Entradas mínimas»: ≥ 24 meses o 250 sesiones.
    "BT-DSR-001": {"sesiones_minimas": 250, "meses_minimos": 24},
    # BT-PBO-001 · «Parámetros»: S 8–20 par. «Entradas mínimas»: N ≥ 2 (≥ 10 útil); T ≥ 4·S. «Supuestos»: PBO ≥ 0,5
    # sobreajuste probable; 0,2–0,5 sospecha.
    "BT-PBO-001": {"rango_S": [8, 20], "configuraciones_minimas": 2, "configuraciones_utiles": 10, "factor_T": 4,
                   "pbo_sobreajuste": 0.5, "pbo_sospecha": 0.2, "metricas": ["sharpe"]},
    # BT-VAR-001 · «Entradas mínimas»: ≥ 250 observaciones. «Método»: semáforo de Basilea con 250 días al 99 %; zonas de
    # BCBS (1996), referencia de la ficha: verde 0–4, amarilla 5–9, roja ≥ 10 excedencias. Rango del nivel y horizonte
    # máximo: los de RISK-VAR-001.
    "BT-VAR-001": {"observaciones_minimas": 250, "rango_nivel": [0.90, 0.99], "dias_semaforo": 250,
                   "nivel_semaforo": 0.99, "verde_max": 4, "amarilla_max": 9, "horizonte_maximo": _HORIZONTE_MAXIMO},
    # ML-CAL-001 · «Entradas mínimas»: ≥ 30 por horizonte. Réplicas del bootstrap del IC hasta 10 000, el tope de B de
    # FC-EVAL-001 («B (2 000; 1 000–10 000)»), cuyo bootstrap usa (H-01).
    "ML-CAL-001": {"observaciones_minimas": 30, "tipos": ["nivel", "probabilidad", "cuantil"], "rango_replicas": [1, 10_000]},
    # ML-PRED-001 · «Entradas mínimas»: ≥ 60 observaciones independientes (≥ 250 para no lineales). «Parámetros»:
    # rejilla ≤ 20. Newton/IRLS de la logística: hasta 100 iteraciones con tolerancia 1e-10 en la log-verosimilitud
    # relativa [PROPUESTO INC-T112-01]. Réplicas como ML-CAL-001; pliegues de 2 a 20, el mismo tope que la ficha da a
    # la rejilla, de modo que pliegues × rejilla ≤ 400 ajustes [PROPUESTO INC-T112-01] (H-01).
    "ML-PRED-001": {"observaciones_minimas": 60, "observaciones_no_lineal": 250, "rejilla_maxima": 20,
                    "modelos": ["logistica_L2", "ridge"], "calibraciones": ["auto", "platt", "isotonica", "ninguna"],
                    "iteraciones_maximas": 100, "tolerancia_newton": 1e-10, "rango_replicas": [1, 10_000],
                    "rango_pliegues": [2, 20]},
    # DEC-VOI-001 · «Método (iv)»: umbrales E 60, A 55, T 50, GC2 50 (de E) y ±5 de banda marginal. Se leen en cada
    # llamada de `parametros_ht03` de la configuración del Motor (H-04), los mismos con que decide HT-03; aquí, las
    # claves de `parametros_ht03.umbrales` de cada decisión. Búsqueda del corte de la regla de Bayes del EVSI: hasta 60
    # ampliaciones del intervalo [PROPUESTO INC-T112-01, técnico].
    "DEC-VOI-001": {"umbrales": {"E": {"E": "E", "GC2": "GC2_E"}, "A": {"A": "A"}, "T": {"T": "T"}},
                    "banda_marginal": "parametros_ht03.banda_marginal", "ampliaciones_maximas": 60},
}

# Advertencias obligatorias de entrega («Supuestos y limitaciones» de cada ficha, literales).
ADVERTENCIAS: dict[str, list[str]] = {
    "RISK-VAR-001": ["el VaR no es la pérdida máxima ni describe la cola", "√h solo con iid"],
    "SIM-MC-001": ["condicional a la dinámica: no corrige un modelo mal especificado"],
    "SCN-H-001": ["distribuciones condicionales al modelo", "las bandas de H4 son anchas por construcción"],
    "BT-DSR-001": [("N ensayos efectivamente independientes (si están correlacionados, N efectivo por agrupación de "
                    "ML-CLUS-001)"), "rendimientos netos de costes"],
    "BT-PBO-001": ["bloques aproximadamente estacionarios", "PBO ≥ 0,5 = sobreajuste probable; 0,2–0,5 sospecha"],
    "BT-VAR-001": ["VaR solapados (h > 1) inducen dependencia: usar observaciones no solapadas o declarar"],
    "ML-CAL-001": ["la evaluación retrospectiva no certifica el futuro", "número de ensayos obligatorio"],
    "ML-PRED-001": ["relaciones estables en la ventana", "mejora con IC que incluye 0 ⇒ «sin mejora demostrada»"],
    "DEC-VOI-001": ["depende del rango plausible declarado", "no sustituye el juicio sobre incertidumbre profunda"],
}


# ================================================================== utilidades comunes
def _num(x: Any, que: str) -> float:
    if isinstance(x, (bool, np.bool_)) or not isinstance(x, (int, float, np.integer, np.floating)):
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
    if isinstance(x, (float, np.floating)) and math.isfinite(float(x)) and float(x) != math.floor(float(x)):
        raise ErrorFicha(f"{que}: se esperaba un entero ({float(x):g})")
    f = _rango(x, que, lo, hi)
    if f != math.floor(f):
        raise ErrorFicha(f"{que}: se esperaba un entero ({f:g})")
    return int(x) if isinstance(x, (int, np.integer)) else int(f)


def _dict(x: Any, que: str) -> dict[str, Any]:
    if not isinstance(x, dict):
        raise ErrorFicha(f"{que}: se esperaba un objeto (dict)")
    return x


def _lista(x: Any, que: str) -> list[Any]:
    if not isinstance(x, (list, tuple)):
        raise ErrorFicha(f"{que}: se esperaba una lista")
    return list(x)


def _texto(x: Any) -> bool:
    return isinstance(x, str) and bool(x.strip())


def _opcion(x: Any, que: str, opciones: list[str]) -> str:
    """Opción declarada (sin distinguir mayúsculas), devuelta con la grafía canónica de la ficha."""
    canon = {o.lower(): o for o in opciones}
    if not isinstance(x, str) or x.strip().lower() not in canon:
        raise ErrorFicha(f"{que}: «{str(x)[:40]}» no reconocido (admitidos: {', '.join(opciones)})")
    return canon[x.strip().lower()]


def _bool(x: Any, que: str) -> bool:
    if not isinstance(x, (bool, np.bool_)):
        raise ErrorFicha(f"{que}: debe ser true o false")
    return bool(x)


def _vector(x: Any, que: str, minimo: int = 1) -> np.ndarray:
    if isinstance(x, (pd.Series, np.ndarray)):
        x = list(np.asarray(x).ravel())
    v = np.array([_num(e, f"{que}[{i}]") for i, e in enumerate(_lista(x, que))], dtype=float)
    if len(v) < minimo:
        raise ErrorFicha(f"{que}: {len(v)} valores (mínimo {minimo})")
    return v


def _requerido(v: dict[str, Any], clave: str, que: str) -> Any:
    if not isinstance(v, dict) or v.get(clave) is None:
        raise ErrorFicha(f"{que}: falta «{clave}»")
    return v[clave]


def _semilla(x: Any, que: str) -> int:
    return _entero(x, f"{que}: semilla", 0, SEMILLA_MAXIMA)


def _cuantiles(x: Any, que: str) -> list[float]:
    q = [_rango(c, f"{que}: cuantiles", 0, 1, True, True) for c in _lista(x, f"{que}: cuantiles")]
    if not q or len(set(q)) != len(q):
        raise ErrorFicha(f"{que}: cuantiles vacíos o repetidos")
    return sorted(q)


def _sesiones_anio(clase: Any) -> int:
    return SESIONES_ANIO_CRI if clase == "CRI" else SESIONES_ANIO


def _configuracion(ent: dict[str, Any]) -> dict[str, Any] | None:
    """Configuración del Motor que llega en ``ent["configuracion"]``; sin ella (manejador llamado directamente), None, y
    `parametro` y `sesiones_horizonte` toman entonces la de `config/por_defecto.yaml` (QA r01 de T-112, H-04)."""
    cfg = ent.get("configuracion")
    if cfg is not None and not isinstance(cfg, dict):
        raise ErrorFicha("la configuración del Motor no es un objeto")
    return cfg


def _horizonte_maximo(cfg: dict[str, Any] | None) -> int:
    """Sesiones del horizonte más largo del Documento 0 (H5), de la configuración: la cota del horizonte (H-01)."""
    return _entero(sesiones_horizonte(cfg, _HORIZONTE_MAXIMO), f"configuración: sesiones de {_HORIZONTE_MAXIMO}", 1)


def _lista_acotada(x: Any, que: str, maximo: int) -> list[Any]:
    lst = _lista(x, que)
    if len(lst) > maximo:
        raise ErrorFicha(f"{que}: {len(lst)} valores (máximo {maximo})")
    return lst


def _validar(ficha: str, p: dict[str, Any], cfg: dict[str, Any] | None = None) -> None:
    """Tipo y dominio de cada parámetro de la petición (falla cerrado con un motivo claro), con su cota superior si es un
    tamaño; los valores que faltan y vienen de la configuración se leen de `cfg`, la del Motor."""
    F, u = ficha, UMBRALES[ficha]
    if p.get("clase") is not None and p["clase"] not in CLASES:
        raise ErrorFicha(f"{F}: clase «{str(p['clase'])[:20]}» desconocida (admitidas: {', '.join(CLASES)})")
    if F == "RISK-VAR-001":
        p["nivel"] = _rango(p["nivel"], f"{F}: nivel", *u["rango_nivel"])
        p["horizonte"] = _entero(p["horizonte"], f"{F}: horizonte", 1, _horizonte_maximo(cfg))
        p["metodo"] = _opcion(p["metodo"], f"{F}: metodo", u["metodos"])
        if p["moneda"] is not None and not _texto(p["moneda"]):
            raise ErrorFicha(f"{F}: moneda debe ser un texto")
    elif F == "SIM-MC-001":
        p["n_trayectorias"] = _entero(p["n_trayectorias"], f"{F}: n_trayectorias", *u["rango_n_trayectorias"])
        if p["horizonte"] is None:
            raise ErrorFicha(f"{F}: falta el horizonte (pasos de la dinámica)")
        h_max = _horizonte_maximo(cfg)
        p["horizonte"] = _entero(p["horizonte"], f"{F}: horizonte", 1, h_max)
        presupuesto = PARAMETROS_POR_DEFECTO[F]["n_trayectorias"] * h_max
        if p["n_trayectorias"] * p["horizonte"] > presupuesto:
            raise ErrorFicha(f"{F}: {p['n_trayectorias']} trayectorias × {p['horizonte']} pasos superan el presupuesto de "
                             f"{presupuesto} (n_trayectorias por defecto × sesiones de {_HORIZONTE_MAXIMO})")
        p["cuantiles"] = _cuantiles(_lista_acotada(p["cuantiles"], f"{F}: cuantiles", u["cuantiles_maximos"]), F)
        if p["semilla"] is None:
            raise ErrorFicha(f"{F}: rechazo sin semilla (semilla obligatoria)")
        p["semilla"] = _semilla(p["semilla"], F)
        p["reduccion_varianza"] = _opcion(p["reduccion_varianza"], f"{F}: reduccion_varianza", u["reducciones"])
        if p["reduccion_varianza"] == "antiteticas" and p["n_trayectorias"] % 2:
            raise ErrorFicha(f"{F}: con antitéticas, n_trayectorias debe ser par")
        p["umbrales"] = [_num(x, f"{F}: umbrales")
                         for x in _lista_acotada(p["umbrales"], f"{F}: umbrales", u["umbrales_maximos"])]
    elif F == "SCN-H-001":
        p["n_trayectorias"] = _entero(p["n_trayectorias"], f"{F}: n_trayectorias", *u["rango_n_trayectorias"])
        if p["n_trayectorias"] % 2:
            raise ErrorFicha(f"{F}: n_trayectorias debe ser par (antitéticas de SIM-MC-001)")
        p["cuantiles"] = _cuantiles(_lista_acotada(p["cuantiles"], f"{F}: cuantiles", u["cuantiles_maximos"]), F)
        if p["semilla"] is None:
            raise ErrorFicha(f"{F}: rechazo sin semilla (semilla obligatoria)")
        p["semilla"] = _semilla(p["semilla"], F)
        p["umbrales"] = [_num(x, f"{F}: umbrales")
                         for x in _lista_acotada(p["umbrales"], f"{F}: umbrales", u["umbrales_maximos"])]
        if p["clase"] is None:
            raise ErrorFicha(f"{F}: falta la clase (tipo de activo) para comprobar el horizonte en la tabla 8.3")
        if p["horizontes"] is not None:
            hs = _lista(p["horizontes"], f"{F}: horizontes")
            if not hs or len(set(hs)) != len(hs) or any(h not in u["horizontes_ficha"] for h in hs):
                raise ErrorFicha(f"{F}: horizontes admitidos {u['horizontes_ficha']} (sin repetir)")
            p["horizontes"] = [h for h in u["horizontes_ficha"] if h in hs]
    elif F == "BT-DSR-001":
        p["SR_referencia"] = _num(p["SR_referencia"], f"{F}: SR_referencia")
        if p["N"] is None:
            raise ErrorFicha(f"{F}: aclaración: falta N (número de ensayos)")
        p["N"] = _entero(p["N"], f"{F}: N", 1)
        p["nivel"] = _rango(p["nivel"], f"{F}: nivel", 0, 1, True, True)
        p["frecuencia"] = _opcion(p["frecuencia"], f"{F}: frecuencia", ["diaria", "mensual"])
    elif F == "BT-PBO-001":
        S = _entero(p["S"], f"{F}: S", *u["rango_S"])
        if S % 2:
            raise ErrorFicha(f"{F}: S debe ser par ({S})")
        p["S"] = S
        p["metrica"] = _opcion(p["metrica"], f"{F}: metrica", u["metricas"])
    elif F == "BT-VAR-001":
        p["nivel"] = _rango(p["nivel"], f"{F}: nivel", *u["rango_nivel"])
        p["significacion"] = _rango(p["significacion"], f"{F}: significacion", 0, 1, True, True)
        p["metodo_var"] = _opcion(p["metodo_var"], f"{F}: metodo_var", UMBRALES["RISK-VAR-001"]["metodos"])
        p["ventana_estimacion"] = _entero(p["ventana_estimacion"], f"{F}: ventana_estimacion",
                                          UMBRALES["RISK-VAR-001"]["observaciones_minimas"])
        p["horizonte"] = _entero(p["horizonte"], f"{F}: horizonte", 1, _horizonte_maximo(cfg))
        p["baja_potencia_declarada"] = _bool(p["baja_potencia_declarada"], f"{F}: baja_potencia_declarada")
    elif F in ("ML-CAL-001", "ML-PRED-001"):
        # Sin valor en la petición, los de la configuración del Motor (H-04); con la misma cota (H-01)
        if p["replicas"] is None:
            p["replicas"] = parametro(cfg, "evaluacion.bootstrap_replicas")
        if p["nivel_ic"] is None:
            p["nivel_ic"] = parametro(cfg, "evaluacion.nivel_ic")
        p["replicas"] = _entero(p["replicas"], f"{F}: replicas", *u["rango_replicas"])
        p["nivel_ic"] = _rango(p["nivel_ic"], f"{F}: nivel_ic", 0, 1, True, True)
        p["semilla"] = _semilla(p["semilla"], F)
        if F == "ML-CAL-001":
            p["esquema"] = _opcion(p["esquema"], f"{F}: esquema", ["walk_forward_expansivo", "walk_forward_movil"])
            if p["horizontes"] is not None:
                p["horizontes"] = [str(h) for h in _lista(p["horizontes"], f"{F}: horizontes")]
            if p["metricas"] is not None:
                p["metricas"] = [str(m) for m in _lista(p["metricas"], f"{F}: metricas")]
        else:
            p["modelo"] = _opcion(p["modelo"], f"{F}: modelo", u["modelos"])
            rej = [_rango(x, f"{F}: rejilla", 0, abierto_lo=True) for x in _lista(p["rejilla"], f"{F}: rejilla")]
            if not rej or len(rej) > u["rejilla_maxima"] or len(set(rej)) != len(rej):
                raise ErrorFicha(f"{F}: rejilla de 1 a {u['rejilla_maxima']} valores distintos")
            p["rejilla"] = rej
            if p["embargo"] is not None:
                p["embargo"] = _entero(p["embargo"], f"{F}: embargo", 1)
            p["calibracion"] = _opcion(p["calibracion"], f"{F}: calibracion", u["calibraciones"])
            p["pliegues"] = _entero(p["pliegues"], f"{F}: pliegues", *u["rango_pliegues"])
            p["fraccion_inicial"] = _rango(p["fraccion_inicial"], f"{F}: fraccion_inicial", 0, 1, True, True)
    elif F == "DEC-VOI-001":
        if p["coste_uc"] is None:
            raise ErrorFicha(f"{F}: falta coste_uc (coste del cálculo en UC, «Entradas mínimas»)")
        p["coste_uc"] = _rango(p["coste_uc"], f"{F}: coste_uc", 0)


def _parametros(ficha: str, params: dict[str, Any] | None, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    """Parámetros de la petición encima de los de la ficha, validados; los de `UMBRALES` no se cambian y uno que la ficha
    no declara se rechaza (QA r01 de T-112, H-02; INC-T112-01: «un parámetro no declarado por la ficha se rechaza»).
    `clase` (el tipo de activo, que el Motor añade desde la petición) se admite en todas."""
    params = _dict(params if params is not None else {}, f"{ficha}: parámetros")
    fijos = set(params) & set(UMBRALES[ficha])
    if fijos:
        raise ErrorFicha(f"{ficha}: {sorted(fijos)} son umbrales fijos de la ficha, no parámetros de la petición")
    desconocidos = set(params) - set(PARAMETROS_POR_DEFECTO[ficha]) - {"clase"}
    if desconocidos:
        raise ErrorFicha(f"{ficha}: parámetros no declarados por la ficha {sorted(map(str, desconocidos))[:5]} "
                         f"(admitidos: {', '.join(sorted(PARAMETROS_POR_DEFECTO[ficha]))})")
    p = dict(PARAMETROS_POR_DEFECTO[ficha])
    if "clase" in params:
        p["clase"] = params["clase"]
    p.update({k: v for k, v in params.items() if v is not None and k in p})
    _validar(ficha, p, cfg)
    return p


def _no_finitos(x: Any, ruta: str = "resultado") -> list[str]:
    if isinstance(x, dict):
        return [r for k, v in x.items() for r in _no_finitos(v, f"{ruta}.{k}")]
    if isinstance(x, (list, tuple)):
        return [r for i, v in enumerate(x) for r in _no_finitos(v, f"{ruta}[{i}]")]
    if isinstance(x, (float, np.floating)) and not math.isfinite(float(x)):
        return [ruta]
    return []


def _json(x: Any) -> Any:
    """Copia del resultado con tipos de Python (numpy → float/int/bool)."""
    if isinstance(x, dict):
        return {str(k): _json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json(v) for v in x]
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        return float(x)
    return x


def _cerrado(ficha: str, fn: Callable[[dict[str, Any], dict[str, Any]], Resultado]) -> Callable[..., Resultado]:
    """Falla cerrado: entradas mal formadas, aritmética fuera de dominio o resultados no finitos → ErrorFicha."""

    @functools.wraps(fn)
    def envoltura(ent: Any, params: Any = None) -> Resultado:
        if not isinstance(ent, dict):
            raise ErrorFicha(f"{ficha}: la entrada debe ser un objeto")
        for k in ("valores", "series", "series_rol"):
            if ent.get(k) is not None and not isinstance(ent[k], dict):
                raise ErrorFicha(f"{ficha}: «{k}» debe ser un objeto")
        if params is not None and not isinstance(params, dict):
            raise ErrorFicha(f"{ficha}: los parámetros deben ser un objeto")
        try:
            with np.errstate(all="ignore"):
                res, lim = fn(ent, dict(params or {}))
        except ErrorFicha:
            raise
        except (ArithmeticError, ValueError, TypeError, AttributeError, KeyError, IndexError, RuntimeError,
                np.linalg.LinAlgError) as e:
            raise ErrorFicha(f"{ficha}: entrada mal formada o fuera de dominio ({type(e).__name__}: {e})") from e
        res = _json(res)
        malos = _no_finitos(res)
        if malos:
            raise ErrorFicha(f"{ficha}: resultado no finito en {', '.join(malos[:3])} (entradas fuera de dominio)")
        res["advertencias"] = list(ADVERTENCIAS[ficha])          # «Supuestos y limitaciones»: no son limitaciones
        return res, [x for x in lim if x not in ADVERTENCIAS[ficha]]

    return envoltura


def _rendimientos(ent: dict[str, Any], que: str, clave: str = "rendimientos") -> np.ndarray:
    """Rendimientos simples: `valores[clave]` en línea o, si no, la única serie de precios de `ent["series"]`."""
    v = ent.get("valores") or {}
    if v.get(clave) is not None:
        return _vector(v[clave], f"{que}: {clave}")
    series = ent.get("series") or {}
    if len(series) == 1:
        s = next(iter(series.values()))
        if not isinstance(s, pd.Series):
            raise ErrorFicha(f"{que}: la serie de precios no es una serie temporal")
        precios = _vector(s.dropna().to_numpy(), f"{que}: precios", 2)
        if (precios <= 0).any():
            raise ErrorFicha(f"{que}: precios no positivos")
        return precios[1:] / precios[:-1] - 1
    if len(series) > 1:
        raise ErrorFicha(f"{que}: más de una serie; aporte una sola o «{clave}» en línea")
    raise ErrorFicha(f"{que}: faltan «{clave}» (en línea) o una serie de precios")


def _cuantil_dict(x: np.ndarray, cuantiles: list[float]) -> dict[str, float]:
    # Todos los cuantiles en una sola llamada (H-01: coste acotado); mismo valor que uno a uno
    return {f"{q:g}": float(v) for q, v in zip(cuantiles, np.quantile(x, cuantiles))}


# ================================================================== RISK-VAR-001
def _cf_monotona(S: float, K: float, z_cola: float) -> bool:
    """Cornish-Fisher z_cf(z) creciente en (−∞, z_cola]: la derivada c₂z² + c₁z + c₀ es positiva en todo el tramo."""
    c2, c1, c0 = K / 8 - S * S / 6, S / 3, 1 - K / 8 + 5 * S * S / 36
    if c2 < 0 or (c2 == 0 and c1 > 0):
        return False
    if c2 == 0:
        return c1 * z_cola + c0 > 0
    z_min = -c1 / (2 * c2)
    z_eval = min(z_min, z_cola)
    return c2 * z_eval * z_eval + c1 * z_eval + c0 > 0


def _nm(fn: Callable[[np.ndarray], float], x0: np.ndarray, que: str, quien: str) -> np.ndarray:
    """Nelder-Mead con las tolerancias y el tope de iteraciones fijos del módulo (QA r01 de T-112, H-03); sin
    convergencia, ErrorFicha."""
    tope = _ITERACIONES_POR_PARAMETRO * len(x0)
    res = optimize.minimize(fn, x0, method="Nelder-Mead", options={"xatol": _TOL_OPTIMIZADOR, "fatol": _TOL_OPTIMIZADOR,
                                                                    "maxiter": tope, "maxfev": tope})
    if not res.success:
        raise ErrorFicha(f"{que}: {quien} sin convergencia ({res.message})")
    return np.asarray(res.x)


def gpd_mv(y: np.ndarray, que: str = "RISK-VAR-001") -> tuple[float, float]:
    """Máxima verosimilitud de la GPD(ξ, β) de los excesos `y` > 0 (umbral restado, localización 0), en (ξ, ln β), por
    Nelder-Mead con tolerancias fijas desde la exponencial (ξ = 0, β = media de los excesos), un arranque fijo que siempre
    está en el soporte. −ln L = n·ln β + (1 + 1/ξ)·Σ ln(1 + ξ·y/β), y n·ln β + Σy/β con ξ = 0."""
    n = len(y)
    if n < 2 or np.ptp(y) == 0:
        raise ErrorFicha(f"{que}: excesos sin dispersión: GPD no identificada")

    def nlv(th: np.ndarray) -> float:
        xi, lb = float(th[0]), float(th[1])
        b = math.exp(lb)
        z = xi * y / b
        if np.any(z <= -1):
            return math.inf                         # fuera del soporte (ξ < 0 y algún exceso ≥ −β/ξ)
        if xi == 0:
            return n * lb + float(np.sum(y)) / b
        return n * lb + (1 + 1 / xi) * float(np.sum(np.log1p(z)))

    th = _nm(nlv, np.array([0.0, math.log(float(np.mean(y)))]), que, "máxima verosimilitud de la GPD")
    return float(th[0]), float(math.exp(th[1]))


def var_es(r: np.ndarray, nivel: float, metodo: str, que: str = "RISK-VAR-001") -> dict[str, Any]:
    """VaR y ES a un periodo como pérdidas positivas (fracción del valor) al `nivel` con el `metodo` de la ficha."""
    u = UMBRALES["RISK-VAR-001"]
    a = 1 - nivel
    n = len(r)
    mu, s = float(np.mean(r)), float(np.std(r, ddof=1))
    if metodo == "historico":
        q = float(np.quantile(r, a))
        return {"var": -q, "es": -float(np.mean(r[r <= q])), "cuantil": q}
    if s <= 0 or np.ptp(r) == 0:
        raise ErrorFicha(f"{que}: dispersión nula; los métodos paramétricos no están definidos")
    if metodo == "normal":
        z = float(stats.norm.ppf(a))
        return {"var": -(mu + s * z), "es": -mu + s * float(stats.norm.pdf(z)) / a, "media": mu, "desviacion": s}
    if metodo == "t":
        exceso = float(stats.kurtosis(r, fisher=True, bias=False))
        if exceso <= 0:
            raise ErrorFicha(f"{que}: curtosis en exceso ≤ 0 ({exceso:.4g}): la t no se ajusta por momentos (use normal)")
        nu = 4 + 6 / exceso                                   # curtosis en exceso de la t = 6/(ν − 4)
        esc = s * math.sqrt((nu - 2) / nu)
        x = float(stats.t.ppf(a, nu))
        es = -mu + esc * (nu + x * x) / (nu - 1) * float(stats.t.pdf(x, nu)) / a
        return {"var": -(mu + esc * x), "es": es, "media": mu, "desviacion": s, "grados_libertad": nu}
    if metodo == "cornish_fisher":
        S = float(stats.skew(r, bias=False))
        K = float(stats.kurtosis(r, fisher=True, bias=False))
        z = float(stats.norm.ppf(a))
        if not _cf_monotona(S, K, z):
            raise ErrorFicha(f"{que}: Cornish-Fisher no monótona en la cola (asimetría {S:.3g}, curtosis {K:.3g})")

        def zcf(x: float) -> float:
            return x + (x * x - 1) * S / 6 + (x ** 3 - 3 * x) * K / 24 - (2 * x ** 3 - 5 * x) * S * S / 36

        cola = integrate.quad(lambda w: zcf(float(stats.norm.ppf(w))), 0, a, limit=200)[0] / a
        return {"var": -(mu + s * zcf(z)), "es": -(mu + s * cola), "media": mu, "desviacion": s,
                "asimetria": S, "curtosis_exceso": K}
    if metodo == "historico_filtrado":
        g = garch_qmle(r, que)
        z = g["residuos"]
        sig = math.sqrt(g["sigma2_siguiente"])
        qz = float(np.quantile(z, a))
        return {"var": -(g["mu"] + sig * qz), "es": -(g["mu"] + sig * float(np.mean(z[z <= qz]))),
                "sigma_siguiente": sig, "cuantil_residuos": qz, "media": g["mu"],
                "garch": {k: g[k] for k in ("omega", "alpha", "beta")}}
    if metodo == "evt_pot":
        perd = -r
        umbral = float(np.quantile(perd, u["cuantil_umbral_evt"]))
        exc = perd[perd > umbral] - umbral
        nu_ = len(exc)
        if nu_ < u["excedencias_minimas_evt"]:
            raise ErrorFicha(f"{que}: EVT-POT con {nu_} excedencias (< {u['excedencias_minimas_evt']})")
        if a >= nu_ / n:
            raise ErrorFicha(f"{que}: el nivel {nivel:g} no queda en la cola por encima del umbral de EVT-POT")
        xi, beta = gpd_mv(exc, que)
        if beta <= 0 or xi >= 1:
            raise ErrorFicha(f"{que}: ajuste GPD no válido (ξ = {xi:.3g}, β = {beta:.3g}; el ES exige ξ < 1)")
        ratio = n / nu_ * a
        var = umbral + (beta / xi * (ratio ** (-xi) - 1) if xi != 0 else -beta * math.log(ratio))
        return {"var": var, "es": (var + beta - xi * umbral) / (1 - xi), "umbral": umbral, "excedencias": nu_,
                "xi": xi, "beta": beta}
    raise ErrorFicha(f"{que}: método «{metodo}» no reconocido")


def _datos_var(ent: dict[str, Any], F: str, lim: list[str]) -> tuple[np.ndarray, str]:
    v = ent.get("valores") or {}
    if v.get("distribucion") is not None:
        d = _dict(v["distribucion"], f"{F}: distribucion")
        if d.get("semilla") is None:
            raise ErrorFicha(f"{F}: una distribución de MC-05 exige su semilla")
        _semilla(d["semilla"], F)
        r = _vector(_requerido(d, "rendimientos", f"{F}: distribucion"), f"{F}: distribucion.rendimientos")
        return r, "distribucion"
    return _rendimientos(ent, F), "historia"


def f_risk_var(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    F = "RISK-VAR-001"
    lim: list[str] = []
    p, u = _parametros(F, params, _configuracion(ent)), UMBRALES[F]
    v = ent.get("valores") or {}
    r, origen = _datos_var(ent, F, lim)
    n = len(r)
    if n < u["observaciones_minimas"]:
        raise ErrorFicha(f"{F}: {n} observaciones (< {u['observaciones_minimas']})")
    if n < u["observaciones_recomendadas"]:
        lim.append(f"{n} observaciones (< {u['observaciones_recomendadas']} recomendadas)")
    nivel, metodo, h = p["nivel"], p["metodo"], p["horizonte"]
    if metodo == "historico" and nivel >= u["nivel_empirico_estricto"] and n < u["observaciones_nivel_estricto"]:
        raise ErrorFicha(f"{F}: nivel {nivel:g} empírico con {n} observaciones (< {u['observaciones_nivel_estricto']})")
    base = var_es(r, nivel, metodo)
    escala = math.sqrt(h)
    if h > 1:
        lim.append(f"horizonte de {h} periodos por escalado √h (supone rendimientos iid)")
    var, es = base["var"] * escala, base["es"] * escala
    # Verificación: ES ≥ VaR y cuantiles monótonos en el rango de niveles de la ficha
    niveles = sorted({u["rango_nivel"][0], nivel, u["rango_nivel"][1]})
    curva = []
    for nv in niveles:
        try:
            curva.append({"nivel": nv, "var": var_es(r, nv, metodo)["var"] * escala})
        except ErrorFicha as e:
            lim.append(f"verificación de monotonía sin el nivel {nv:g}: {e}")
    vars_ = [c["var"] for c in curva]
    monotonos = all(x <= y for x, y in itertools.pairwise(vars_))
    if not monotonos:
        raise ErrorFicha(f"{F}: cuantiles no monótonos en el nivel con el método {metodo}")
    if es < var:
        raise ErrorFicha(f"{F}: ES < VaR con el método {metodo} (identidad de la ficha incumplida)")
    via = "normal" if metodo == "historico" else "historico"
    otra = var_es(r, nivel, via)
    s = float(np.std(r, ddof=1))
    ref = -s * float(stats.norm.ppf(1 - nivel)) * escala   # VaR normal con la volatilidad histórica (media cero)
    out: dict[str, Any] = {
        "var": var, "es": es, "nivel": nivel, "horizonte": h, "metodo": metodo, "n": n, "origen": origen,
        "detalle_metodo": {k: x for k, x in base.items() if k not in ("var", "es")},
        "verificacion": {"es_mayor_igual_var": bool(es >= var), "cuantiles_monotonos": monotonos, "curva_nivel": curva},
        "segunda_via": {"metodo": via, "var": otra["var"] * escala, "es": otra["es"] * escala,
                        "diferencia_var": var - otra["var"] * escala},
        "referencia_ingenua": {"tipo": "VaR normal con volatilidad histórica", "var": ref},
        "var_moneda": None, "es_moneda": None, "moneda": p["moneda"]}
    if v.get("valor_posicion") is not None:
        valor = _rango(v["valor_posicion"], f"{F}: valor_posicion", 0, abierto_lo=True)
        if p["moneda"] is None:
            raise ErrorFicha(f"{F}: valor_posicion sin moneda declarada")
        out["var_moneda"], out["es_moneda"] = var * valor, es * valor
    else:
        lim.append("sin valor de la posición: VaR y ES solo en fracción del valor")
    return out, lim


# ================================================================== SIM-MC-001
def _garch_params(d: dict[str, Any], que: str) -> tuple[float, float, float, float]:
    om = _rango(_requerido(d, "omega", que), f"{que}: omega", 0, abierto_lo=True)
    al = _rango(_requerido(d, "alpha", que), f"{que}: alpha", 0)
    be = _rango(_requerido(d, "beta", que), f"{que}: beta", 0)
    if d.get("sigma2_inicial") is not None:
        s2 = _rango(d["sigma2_inicial"], f"{que}: sigma2_inicial", 0, abierto_lo=True)
    elif al + be < 1:
        s2 = om / (1 - al - be)
    else:
        raise ErrorFicha(f"{que}: GARCH integrado (α + β ≥ 1) sin sigma2_inicial")
    return om, al, be, s2


def _dinamica(v: dict[str, Any], F: str) -> dict[str, Any]:
    d = _dict(_requerido(v, "dinamica", F), f"{F}: dinamica")
    tipo = _opcion(_requerido(d, "tipo", f"{F}: dinamica"), f"{F}: dinamica.tipo", UMBRALES["SIM-MC-001"]["dinamicas"])
    q = f"{F}: dinamica ({tipo})"
    out: dict[str, Any] = {"tipo": tipo, "mu": _num(_requerido(d, "mu", q), f"{q}: mu")}
    if tipo in ("paseo_aleatorio", "saltos"):
        out["sigma"] = _rango(_requerido(d, "sigma", q), f"{q}: sigma", 0)
    if tipo == "saltos":
        out["intensidad"] = _rango(_requerido(d, "intensidad", q), f"{q}: intensidad", 0)
        out["media_salto"] = _num(_requerido(d, "media_salto", q), f"{q}: media_salto")
        out["desv_salto"] = _rango(_requerido(d, "desv_salto", q), f"{q}: desv_salto", 0)
    if tipo in ("garch", "bootstrap_filtrado"):
        out["omega"], out["alpha"], out["beta"], out["sigma2_inicial"] = _garch_params(d, q)
    if tipo == "bootstrap_filtrado":
        z = _vector(_requerido(d, "residuos", q), f"{q}: residuos", 2)
        out["residuos"] = z
    out["valor_inicial"] = (None if d.get("valor_inicial") is None
                            else _rango(d["valor_inicial"], f"{q}: valor_inicial", 0, abierto_lo=True))
    return out


def simular(din: dict[str, Any], n: int, pasos: int, rng: np.random.Generator, antiteticas: bool,
            puntos: list[int]) -> dict[int, np.ndarray]:
    """Log-rendimiento acumulado de `n` trayectorias de la dinámica `din` en cada paso de `puntos` (≤ `pasos`).

    Con antitéticas, las trayectorias 2i y 2i+1 usan innovaciones gaussianas opuestas (z, −z), de modo que cualquier
    prefijo de longitud par está equilibrado.
    """
    tipo = din["tipo"]

    def normales() -> np.ndarray:
        if not antiteticas:
            return rng.standard_normal(n)
        z = rng.standard_normal(n // 2)
        out = np.empty(n)
        out[0::2], out[1::2] = z, -z
        return out

    x = np.zeros(n)
    h = np.full(n, din.get("sigma2_inicial", 0.0))
    guardar = set(puntos)
    res: dict[int, np.ndarray] = {}
    for t in range(1, pasos + 1):
        if tipo == "paseo_aleatorio":
            x = x + din["mu"] + din["sigma"] * normales()
        elif tipo == "saltos":
            k = rng.poisson(din["intensidad"], n).astype(float)
            x = x + din["mu"] + din["sigma"] * normales() + k * din["media_salto"] + np.sqrt(k) * din["desv_salto"] * normales()
        else:
            if tipo == "garch":
                z = normales()
            else:
                z = din["residuos"][rng.integers(0, len(din["residuos"]), n)]
            eps = np.sqrt(h) * z
            x = x + din["mu"] + eps
            h = din["omega"] + din["alpha"] * eps * eps + din["beta"] * h
        if t in guardar:
            res[t] = x.copy()
    return res


def _resumen_mc(y: np.ndarray, cuantiles: list[float], umbrales: list[float], antiteticas: bool,
                mitades: int) -> dict[str, Any]:
    n = len(y)
    if antiteticas:
        pares = 0.5 * (y[0::2] + y[1::2])
        ee = float(np.std(pares, ddof=1) / math.sqrt(len(pares)))
    else:
        ee = float(np.std(y, ddof=1) / math.sqrt(n))
    prob = {}
    for umb in umbrales:
        pr = float(np.mean(y >= umb))
        prob[f"{umb:g}"] = {"probabilidad": pr, "ee": math.sqrt(pr * (1 - pr) / n)}
    conv = []
    for k in range(mitades + 1):
        m = n // (2 ** k)
        m -= m % 2 if antiteticas else 0
        if m < 2:
            break
        conv.append({"n": m, "media": float(np.mean(y[:m])),
                     "cuantiles": _cuantil_dict(y[:m], cuantiles)})
    return {"media": float(np.mean(y)), "desviacion": float(np.std(y, ddof=1)), "ee_media": ee,
            "cuantiles": _cuantil_dict(y, cuantiles), "probabilidades_umbral": prob, "convergencia": conv}


def f_sim_mc(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    F = "SIM-MC-001"
    lim: list[str] = []
    p = _parametros(F, params, _configuracion(ent))
    din = _dinamica(ent.get("valores") or {}, F)
    n, h = p["n_trayectorias"], p["horizonte"]
    anti = p["reduccion_varianza"] == "antiteticas"
    if anti and din["tipo"] == "bootstrap_filtrado":
        anti = False
        lim.append("antitéticas no aplicables al bootstrap filtrado (residuos empíricos no simétricos): sin reducción")
    rng = np.random.default_rng(p["semilla"])
    x = simular(din, n, h, rng, anti, [h])[h]
    v0 = din["valor_inicial"]
    y = v0 * np.exp(x) if v0 is not None else np.expm1(x)
    unidades = "nivel de la variable" if v0 is not None else "rendimiento simple acumulado (fracción)"
    out: dict[str, Any] = {"dinamica": din["tipo"], "n_trayectorias": n, "horizonte": h, "semilla": p["semilla"],
                           "reduccion_varianza": "antiteticas" if anti else "ninguna", "unidades": unidades}
    out["distribucion"] = _resumen_mc(y, p["cuantiles"], p["umbrales"], anti, UMBRALES[F]["mitades_convergencia"])
    k = float(stats.kurtosis(x, fisher=False, bias=False)) if np.ptp(x) > 0 else None
    out["log_rendimiento"] = {"media": float(np.mean(x)), "varianza": float(np.var(x, ddof=1)), "curtosis": k}
    # Solución analítica donde existe (casos de control de la «Verificación»)
    if din["tipo"] == "paseo_aleatorio":
        m, sd = h * din["mu"], din["sigma"] * math.sqrt(h)
        cq = {f"{q:g}": float((v0 or 1.0) * math.exp(m + sd * float(stats.norm.ppf(q))) - (0 if v0 else 1.0))
              for q in p["cuantiles"]}
        out["solucion_analitica"] = {"media_log": m, "varianza_log": sd * sd, "cuantiles": cq}
    elif din["tipo"] == "saltos":
        lam = din["intensidad"]
        out["solucion_analitica"] = {
            "media_log": h * (din["mu"] + lam * din["media_salto"]),
            "varianza_log": h * (din["sigma"] ** 2 + lam * (din["desv_salto"] ** 2 + din["media_salto"] ** 2))}
    elif din["tipo"] == "garch":
        om, al, be, s2 = din["omega"], din["alpha"], din["beta"], din["sigma2_inicial"]
        per = al + be
        esperadas = [s2]
        for _ in range(h - 1):
            esperadas.append(om + per * esperadas[-1])
        out["solucion_analitica"] = {"media_log": h * din["mu"], "varianza_log": float(sum(esperadas))}
    else:
        out["solucion_analitica"] = None
        lim.append("bootstrap filtrado sin solución analítica: sin contraste analítico")
    # Referencia ingenua RI-CLI: bootstrap simple de la historia, si se aporta
    v = ent.get("valores") or {}
    if v.get("historia_rendimientos") is not None:
        hist = _vector(v["historia_rendimientos"], f"{F}: historia_rendimientos", 2)
        lh = np.log1p(hist)
        if not np.isfinite(lh).all():
            raise ErrorFicha(f"{F}: historia_rendimientos con rendimientos ≤ −100 %")
        rng_ref = np.random.default_rng(p["semilla"])
        xr = lh[rng_ref.integers(0, len(lh), (n, h))].sum(axis=1)
        yr = v0 * np.exp(xr) if v0 is not None else np.expm1(xr)
        out["referencia_ingenua"] = {"tipo": "RI-CLI (bootstrap simple de la historia)",
                                     "cuantiles": _cuantil_dict(yr, p["cuantiles"])}
    else:
        out["referencia_ingenua"] = None
        lim.append("sin historia_rendimientos: referencia RI-CLI no calculada")
    return out, lim


# ================================================================== SCN-H-001
def varianzas_garch(eps: np.ndarray, om: float, al: float, be: float, h0: float) -> np.ndarray:
    """σ²_t = ω + α·ε²_{t−1} + β·σ²_{t−1} (VOL-GARCH-001) con σ²_0 = h0, como filtro recursivo de primer orden."""
    h = np.empty(len(eps))
    h[0] = h0
    if len(eps) > 1:
        h[1:] = signal.lfilter([1.0], [1.0, -be], om + al * eps[:-1] ** 2, zi=[be * h0])[0]
    return h


def garch_qmle(r: np.ndarray, que: str) -> dict[str, Any]:
    """GARCH(1,1) por cuasi máxima verosimilitud gaussiana con objetivo de varianza (ω = σ̄²(1 − α − β)).

    Valores iniciales fijos α = 0,05 y β = 0,90 [PROPUESTO INC-T112-01] (VOL-GARCH-001: «valores iniciales fijos»);
    Nelder-Mead sobre la persistencia y la cuota de α en logit (siempre 0 < α + β < 1), con las tolerancias fijas de
    `_nm` (H-03). No converge ⇒ ErrorFicha.
    """
    eps = r - np.mean(r)
    var = float(np.var(eps))
    if var <= 0:
        raise ErrorFicha(f"{que}: dispersión nula; GARCH no identificado")

    def desplegar(th: np.ndarray) -> tuple[float, float]:
        per = float(special.expit(th[0]))
        cuota = float(special.expit(th[1]))
        return per * cuota, per * (1 - cuota)

    def nlv(th: np.ndarray) -> float:
        al, be = desplegar(th)
        h = varianzas_garch(eps, var * (1 - al - be), al, be, var)
        return float(0.5 * np.sum(np.log(h) + eps * eps / h))

    a0, b0 = 0.05, 0.90
    th0 = np.array([special.logit(a0 + b0), special.logit(a0 / (a0 + b0))])
    al, be = desplegar(_nm(nlv, th0, que, "GARCH(1,1)"))
    om = var * (1 - al - be)
    h = varianzas_garch(eps, om, al, be, var)
    return {"omega": om, "alpha": al, "beta": be, "mu": float(np.mean(r)),
            "sigma2_siguiente": float(om + al * eps[-1] ** 2 + be * h[-1]), "residuos": eps / np.sqrt(h)}


def _residuos_garch(r: np.ndarray, g: dict[str, Any], que: str) -> dict[str, Any]:
    om = _rango(_requerido(g, "omega", que), f"{que}: omega", 0, abierto_lo=True)
    al = _rango(_requerido(g, "alpha", que), f"{que}: alpha", 0)
    be = _rango(_requerido(g, "beta", que), f"{que}: beta", 0)
    if al + be >= 1:
        raise ErrorFicha(f"{que}: GARCH integrado (α + β ≥ 1): sin varianza de largo plazo")
    if not _texto(g.get("fuente")):
        raise ErrorFicha(f"{que}: parámetros GARCH sin fuente (p. ej., VOL-GARCH-001)")
    mu = float(np.mean(r))
    eps = r - mu
    h = varianzas_garch(eps, om, al, be, om / (1 - al - be))
    return {"omega": om, "alpha": al, "beta": be, "mu": mu,
            "sigma2_siguiente": float(om + al * eps[-1] ** 2 + be * h[-1]), "residuos": eps / np.sqrt(h)}


def _con_fuente(d: Any, que: str) -> dict[str, Any]:
    d = _dict(d, que)
    if not _texto(d.get("fuente")):
        raise ErrorFicha(f"{que}: sin fuente")
    return d


def f_scn_h(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    F = "SCN-H-001"
    lim: list[str] = []
    cfg = _configuracion(ent)
    p, u = _parametros(F, params, cfg), UMBRALES[F]
    v = ent.get("valores") or {}
    clase = p["clase"]
    tiene = {"H1": v.get("rendimientos") is not None or len(ent.get("series") or {}) == 1,
             "H3": v.get("regimen") is not None, "H4": v.get("bloques") is not None}
    tiene["H2"] = tiene["H1"]
    pedidos = p["horizontes"] or [h for h in u["horizontes_ficha"] if tiene[h]]
    if not pedidos:
        raise ErrorFicha(f"{F}: sin datos para ningún horizonte (rendimientos, regimen o bloques)")
    for h in pedidos:
        apl = TABLA_HORIZONTES[clase][h]
        if apl == "NO":
            raise ErrorFicha(f"{F}: {h} es «No» para {clase} en la tabla 8.3 del Documento 0")
        if not tiene[h]:
            raise ErrorFicha(f"{F}: {h} pedido sin sus datos")
        if apl == "LIMITADO":
            lim.append(f"{h} «Limitado» para {clase} (8.3): solo con datos suficientes y catalizador identificado")
    v0 = None if v.get("valor_inicial") is None else _rango(v["valor_inicial"], f"{F}: valor_inicial", 0, abierto_lo=True)
    unidades = "unidades de la variable" if v0 is not None else "%"

    def salida(x_log: np.ndarray) -> np.ndarray:
        return v0 * np.exp(x_log) if v0 is not None else np.expm1(x_log) * PCT

    semillas = np.random.SeedSequence(p["semilla"]).spawn(len(u["horizontes_ficha"]))
    rng_de = dict(zip(u["horizontes_ficha"], semillas))
    n, cq = p["n_trayectorias"], p["cuantiles"]
    tabla: dict[str, Any] = {}
    sims: dict[str, np.ndarray] = {}
    ref: dict[str, Any] = {}
    # H1–H2: volatilidad condicional GARCH(1,1) y residuos por bootstrap filtrado (SIM-MC-001)
    h12 = [h for h in ("H1", "H2") if h in pedidos]
    if h12:
        r = _rendimientos(ent, F)
        minimo = u["anios_minimos_h12"] * _sesiones_anio(clase)
        if len(r) < minimo:
            raise ErrorFicha(f"{F}: H1–H2 con {len(r)} rendimientos diarios (< {minimo}, 2 años)")
        lr = np.log1p(r)
        if not np.isfinite(lr).all():
            raise ErrorFicha(f"{F}: rendimientos ≤ −100 %")
        g = (_residuos_garch(lr, _dict(v["garch"], f"{F}: garch"), f"{F}: garch") if v.get("garch") is not None
             else garch_qmle(lr, F))
        pasos = {h: sesiones_horizonte(cfg, h) for h in h12}
        din = {"tipo": "bootstrap_filtrado", "mu": g["mu"], "omega": g["omega"], "alpha": g["alpha"],
               "beta": g["beta"], "sigma2_inicial": g["sigma2_siguiente"], "residuos": g["residuos"]}
        rng = np.random.default_rng(rng_de["H1"])
        caminos = simular(din, n, max(pasos.values()), rng, False, list(pasos.values()))
        rng_ref = np.random.default_rng(rng_de["H2"])
        for h in h12:
            sims[h] = salida(caminos[pasos[h]])
            tabla[h] = {"pasos_sesiones": pasos[h], "metodo": "GARCH(1,1) + bootstrap filtrado (SIM-MC-001)",
                        "garch": {k: g[k] for k in ("omega", "alpha", "beta", "mu")}}
            xr = lr[rng_ref.integers(0, len(lr), (n, pasos[h]))].sum(axis=1)
            ref[h] = {"RI-CLI": _cuantil_dict(salida(xr), cq), "RI-PA": float(salida(np.zeros(1))[0])}
    # H3: mezcla por régimen (probabilidades filtradas de REG-HMM-001) + escenario de valoración de MC-09
    if "H3" in pedidos:
        reg = _con_fuente(v["regimen"], f"{F}: regimen")
        probs = _dict(_requerido(reg, "probabilidades_filtradas", f"{F}: regimen"), f"{F}: probabilidades_filtradas")
        estados = _dict(_requerido(reg, "estados", f"{F}: regimen"), f"{F}: regimen.estados")
        if not probs or set(probs) != set(estados):
            raise ErrorFicha(f"{F}: probabilidades filtradas y estados no coinciden")
        nombres = sorted(probs)
        pr = np.array([_rango(probs[k], f"{F}: probabilidad de {k}", 0, 1) for k in nombres])
        if not math.isclose(float(pr.sum()), 1.0, rel_tol=0, abs_tol=1e-10):
            raise ErrorFicha(f"{F}: las probabilidades filtradas no suman 1 ({float(pr.sum()):.6g})")
        pasos3 = sesiones_horizonte(cfg, "H3")
        rng = np.random.default_rng(rng_de["H3"])
        cuenta = rng.multinomial(n // 2, pr) * 2            # pares antitéticos dentro de cada régimen
        partes = []
        for k, c in zip(nombres, cuenta):
            e = _dict(estados[k], f"{F}: estado {k}")
            din = {"tipo": "paseo_aleatorio", "mu": _num(_requerido(e, "media", f"{F}: estado {k}"), f"{F}: media de {k}"),
                   "sigma": _rango(_requerido(e, "volatilidad", f"{F}: estado {k}"), f"{F}: volatilidad de {k}", 0)}
            if c:
                partes.append(simular(din, int(c), pasos3, rng, True, [pasos3])[pasos3])
        x3 = np.concatenate(partes)
        ajuste = 0.0
        if v.get("valoracion") is not None:
            val = _con_fuente(v["valoracion"], f"{F}: valoracion")
            aj = _rango(_requerido(val, "ajuste", f"{F}: valoracion"), f"{F}: valoracion.ajuste", -1, abierto_lo=True)
            ajuste = math.log1p(aj)
        else:
            lim.append("H3 sin escenario de valoración de MC-09: solo la mezcla por régimen")
        sims["H3"] = salida(x3 + ajuste)
        tabla["H3"] = {"pasos_sesiones": pasos3, "metodo": "mezcla por régimen (REG-HMM-001) + valoración (MC-09)",
                       "probabilidades_regimen": dict(zip(nombres, pr.tolist())), "ajuste_valoracion_log": ajuste}
        ref["H3"] = {"RI-PA": float(salida(np.zeros(1))[0])}
    # H4: bloques de rentabilidad esperada (rendimiento corriente + crecimiento + cambio de valoración ± incertidumbre)
    if "H4" in pedidos:
        bl = _con_fuente(v["bloques"], f"{F}: bloques")
        medias, desv = [], []
        for nombre in ("rendimiento_corriente", "crecimiento", "cambio_valoracion"):
            b = _dict(_requerido(bl, nombre, f"{F}: bloques"), f"{F}: bloque {nombre}")
            medias.append(_num(_requerido(b, "valor", f"{F}: {nombre}"), f"{F}: {nombre}.valor"))
            desv.append(_rango(_requerido(b, "incertidumbre", f"{F}: {nombre}"), f"{F}: {nombre}.incertidumbre", 0))
        anios = sesiones_horizonte(cfg, "H4") / SESIONES_ANIO
        rng = np.random.default_rng(rng_de["H4"])
        z = rng.standard_normal((n // 2, 3))
        z = np.concatenate([z, -z])
        ra = (np.array(medias) + z * np.array(desv)).sum(axis=1)
        if (ra <= -1).any():
            raise ErrorFicha(f"{F}: H4 con rentabilidades anuales ≤ −100 % (incertidumbre de los bloques excesiva)")
        sims["H4"] = salida(anios * np.log1p(ra))
        tabla["H4"] = {"anios": anios, "metodo": "bloques de rentabilidad esperada",
                       "rentabilidad_anual_esperada": float(sum(medias)),
                       "incertidumbre_anual": float(math.sqrt(sum(d * d for d in desv)))}
        ref["H4"] = {"RI-PA": float(salida(np.zeros(1))[0])}
    # Escenarios, cuantiles, probabilidades de umbral y coherencia
    narrativos = _dict(v.get("escenarios_narrativos") or {}, f"{F}: escenarios_narrativos")
    monotonos, anchos = True, []
    for h in [h for h in u["horizontes_ficha"] if h in sims]:
        y = sims[h]
        qs = _cuantil_dict(y, cq)
        vals = list(qs.values())
        monotonos = monotonos and all(a <= b for a, b in itertools.pairwise(vals))
        base = float(np.quantile(y, 0.5))
        fav, adv = float(np.quantile(y, u["cuantil_favorable"])), float(np.quantile(y, u["cuantil_adverso"]))
        if h in narrativos:
            nar = _con_fuente(narrativos[h], f"{F}: escenarios_narrativos.{h}")
            fav = _num(_requerido(nar, "favorable", f"{F}: {h}"), f"{F}: {h}.favorable")
            adv = _num(_requerido(nar, "adverso", f"{F}: {h}"), f"{F}: {h}.adverso")
            if not adv <= base <= fav:
                raise ErrorFicha(f"{F}: escenarios narrativos de {h} incoherentes con la base (adverso ≤ base ≤ favorable)")
        ancho = float(np.quantile(y, cq[-1]) - np.quantile(y, cq[0]))
        anchos.append(ancho)
        tabla[h].update({"aplicabilidad": TABLA_HORIZONTES[clase][h], "unidades": unidades, "cuantiles": qs,
                         "escenarios": {"base": base, "favorable": fav, "adverso": adv,
                                        "origen": "narrativos de Prospectiva" if h in narrativos else "cuantiles 80/20"},
                         "probabilidades_umbral": {f"{x:g}": float(np.mean(y >= x)) for x in p["umbrales"]},
                         "amplitud_banda": ancho, "referencia_ingenua": ref[h]})
    crecientes = all(a <= b for a, b in itertools.pairwise(anchos))
    if not crecientes:
        lim.append("bandas no crecientes entre horizontes (modelos distintos por horizonte): revisar la coherencia")
    if p["umbrales"]:
        lim.append("probabilidades de umbral solo publicables con certificado R13")
    return {"clase": clase, "semilla": p["semilla"], "n_trayectorias": n, "horizontes": tabla,
            "verificacion": {"cuantiles_monotonos": monotonos, "bandas_crecientes": crecientes}}, lim


# ================================================================== BT-DSR-001
def _lo_eta(rho: float, q: int) -> float:
    """Factor de anualización del Sharpe de Lo (2002) con autocorrelación AR(1) ρ: q / √(q + 2 Σ (q − k) ρᵏ)."""
    suma = sum((q - k) * rho ** k for k in range(1, q))
    return q / math.sqrt(q + 2 * suma)


def f_bt_dsr(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    F = "BT-DSR-001"
    lim: list[str] = []
    p, u = _parametros(F, params, _configuracion(ent)), UMBRALES[F]
    v = ent.get("valores") or {}
    r = _rendimientos(ent, F)
    T = len(r)
    q = MESES_ANIO if p["frecuencia"] == "mensual" else _sesiones_anio(p["clase"])
    minimo = u["meses_minimos"] if p["frecuencia"] == "mensual" else u["sesiones_minimas"]
    if T < minimo:
        raise ErrorFicha(f"{F}: {T} rendimientos con frecuencia {p['frecuencia']} (< {minimo})")
    vs = _dict(_requerido(v, "varianza_sr_ensayos", F), f"{F}: varianza_sr_ensayos")
    var_sr = _rango(_requerido(vs, "valor", f"{F}: varianza_sr_ensayos"), f"{F}: varianza_sr_ensayos.valor", 0)
    unidad = _opcion(_requerido(vs, "unidad", f"{F}: varianza_sr_ensayos"), f"{F}: varianza_sr_ensayos.unidad",
                     ["anual", "periodo"])
    var_sr_p = var_sr / q if unidad == "anual" else var_sr
    s = float(np.std(r, ddof=1))
    if s <= 0 or np.ptp(r) == 0:
        raise ErrorFicha(f"{F}: rendimientos sin dispersión: Sharpe indefinido")
    sr = float(np.mean(r)) / s
    g3 = float(stats.skew(r, bias=False))
    g4 = float(stats.kurtosis(r, fisher=False, bias=False))
    den = 1 - g3 * sr + (g4 - 1) / 4 * sr * sr
    if den <= 0:
        raise ErrorFicha(f"{F}: varianza del Sharpe no positiva con estos momentos")
    ee = math.sqrt(den / (T - 1))
    sr_ref = p["SR_referencia"] / math.sqrt(q)
    psr = float(stats.norm.cdf((sr - sr_ref) / ee))
    N = p["N"]
    if N == 1:
        sr0 = 0.0
        lim.append("N = 1: sin deflación (SR*₀ = 0)")
    else:
        g = float(np.euler_gamma)
        sr0 = math.sqrt(var_sr_p) * ((1 - g) * float(stats.norm.ppf(1 - 1 / N))
                                     + g * float(stats.norm.ppf(1 - 1 / (N * math.e))))
    dsr = float(stats.norm.cdf((sr - sr0) / ee))
    z = float(stats.norm.ppf(p["nivel"]))
    if sr > sr_ref:
        min_trl: float | None = 1 + den * (z / (sr - sr_ref)) ** 2
    else:
        min_trl = None
        lim.append("SR ≤ SR_referencia: MinTRL indefinido")
    rho = float(np.corrcoef(r[:-1], r[1:])[0, 1])
    return {"T": T, "periodos_anio": q, "sr_periodo": sr, "sr_anual": sr * math.sqrt(q),
            "sr_anual_lo": sr * _lo_eta(rho, q), "autocorrelacion_1": rho, "asimetria": g3, "curtosis": g4,
            "ee_periodo": ee, "ee_anual": ee * math.sqrt(q), "sr_referencia_anual": p["SR_referencia"],
            "psr": psr, "N": N, "varianza_sr_ensayos_periodo": var_sr_p, "sr0_periodo": sr0,
            "sr0_anual": sr0 * math.sqrt(q), "dsr": dsr, "nivel": p["nivel"], "min_trl_periodos": min_trl,
            "referencia_ingenua": {"sr_cero_psr": float(stats.norm.cdf(sr / ee))}}, lim


# ================================================================== BT-PBO-001
def _matriz_pbo(v: dict[str, Any], F: str) -> tuple[list[str], np.ndarray]:
    m = _dict(_requerido(v, "rendimientos", F), f"{F}: rendimientos (configuración → serie)")
    nombres = sorted(str(k) for k in m)
    if len(nombres) != len(m):
        raise ErrorFicha(f"{F}: nombres de configuración repetidos")
    cols = [_vector(m[k], f"{F}: rendimientos.{k}", 1) for k in sorted(m, key=str)]
    if len({len(c) for c in cols}) > 1:
        raise ErrorFicha(f"{F}: las configuraciones no tienen la misma longitud T")
    return nombres, np.column_stack(cols) if cols else np.empty((0, 0))


def f_bt_pbo(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    F = "BT-PBO-001"
    lim: list[str] = []
    p, u = _parametros(F, params, _configuracion(ent)), UMBRALES[F]
    nombres, M = _matriz_pbo(ent.get("valores") or {}, F)
    N = len(nombres)
    if N < u["configuraciones_minimas"]:
        raise ErrorFicha(f"{F}: {N} configuraciones (< {u['configuraciones_minimas']})")
    if N < u["configuraciones_utiles"]:
        lim.append(f"{N} configuraciones (< {u['configuraciones_utiles']}): PBO poco informativo")
    if (np.ptp(M, axis=0) == 0).any():
        raise ErrorFicha(f"{F}: una configuración sin dispersión: Sharpe indefinido")
    S = p["S"]
    T = M.shape[0]
    if T < u["factor_T"] * S:
        raise ErrorFicha(f"{F}: T = {T} (< {u['factor_T']}·S = {u['factor_T'] * S})")
    b = T // S
    if T % S:
        lim.append(f"{T % S} observaciones más antiguas descartadas para bloques iguales de {b}")
    M = M[T - b * S:]
    bloques = M.reshape(S, b, N)
    s1, s2 = bloques.sum(axis=1), (bloques ** 2).sum(axis=1)
    combos = np.array(list(itertools.combinations(range(S), S // 2)))
    n_med = b * S // 2

    def sharpe(t1: np.ndarray, t2: np.ndarray) -> np.ndarray:
        media = t1 / n_med
        var = (t2 - n_med * media * media) / (n_med - 1)
        if (var <= 0).any():
            raise ErrorFicha(f"{F}: una configuración sin dispersión en una mitad: Sharpe indefinido")
        return np.asarray(media / np.sqrt(var))

    # Por tandas de combinaciones (H-01): la memoria queda en O(tanda·N) aunque S = 20 dé 184 756 combinaciones
    tanda = max(1, _ELEMENTOS_TANDA // (S * N))
    partes: dict[str, list[np.ndarray]] = {"mejor": [], "w": [], "is_m": [], "oos_m": []}
    empates = 0
    for i0 in range(0, len(combos), tanda):
        cb = combos[i0:i0 + tanda]
        is1, is2 = s1[cb].sum(axis=1), s2[cb].sum(axis=1)   # suma de los S/2 bloques de dentro, igual en cualquier tanda
        dentro = sharpe(is1, is2)
        fuera = sharpe(s1.sum(axis=0) - is1, s2.sum(axis=0) - is2)
        mejor = np.argmax(dentro, axis=1)
        empates += int(np.sum((dentro == dentro.max(axis=1, keepdims=True)).sum(axis=1) > 1))
        rangos = stats.rankdata(fuera, axis=1)            # rango medio ante empates, fila a fila (vectorizado)
        fila = np.arange(len(cb))
        w = rangos[fila, mejor] / (N + 1)
        for k, x in (("mejor", mejor), ("w", w), ("is_m", dentro[fila, mejor]), ("oos_m", fuera[fila, mejor])):
            partes[k].append(x)
    identicas = bool(np.all(M == M[:, :1]))
    out: dict[str, Any] = {"N": N, "T_usado": int(b * S), "S": S, "combinaciones": len(combos), "metrica": p["metrica"]}
    if identicas:
        lim.append("configuraciones idénticas: PBO indefinido (no hay mejor configuración dentro de muestra)")
        out.update({"pbo": None, "indefinido": True, "lambda": None, "pendiente_degradacion": None,
                    "probabilidad_perdida": None, "diagnostico": "indefinido"})
        return out, lim
    if empates:
        lim.append(f"{empates} combinaciones con empate en la mejor configuración dentro de muestra (se toma la primera)")
    mejor, w, is_m, oos_m = (np.concatenate(partes[k]) for k in ("mejor", "w", "is_m", "oos_m"))
    lam = np.log(w / (1 - w))
    pbo = float(np.mean(lam <= 0))
    pendiente = float(np.polyfit(is_m, oos_m, 1)[0]) if np.ptp(is_m) > 0 else None
    if pendiente is None:
        lim.append("Sharpe dentro de muestra constante entre combinaciones: pendiente de degradación indefinida")
    diag = ("sobreajuste_probable" if pbo >= u["pbo_sobreajuste"] else
            "sospecha" if pbo >= u["pbo_sospecha"] else "sin_indicios")
    out.update({"pbo": pbo, "indefinido": False,
                "lambda": {"media": float(np.mean(lam)), "desviacion": float(np.std(lam, ddof=1)),
                           "cuantiles": _cuantil_dict(lam, PARAMETROS_POR_DEFECTO["SIM-MC-001"]["cuantiles"]),
                           "minimo": float(lam.min()), "maximo": float(lam.max())},
                "pendiente_degradacion": pendiente, "probabilidad_perdida": float(np.mean(oos_m < 0)),
                "frecuencia_mejor": {nombres[i]: float(np.mean(mejor == i)) for i in range(N)},
                "diagnostico": diag, "referencia_ingenua": {"tipo": "selección aleatoria", "pbo": 0.5}})
    return out, lim


# ================================================================== BT-VAR-001
def kupiec(x: int, T: int, p: float) -> float:
    """LR_uc de Kupiec (1995) con x excedencias en T observaciones y probabilidad de cola p (0·ln 0 = 0)."""
    f = x / T
    l0 = special.xlogy(T - x, 1 - p) + special.xlogy(x, p)
    l1 = special.xlogy(T - x, 1 - f) + special.xlogy(x, f)
    return float(-2 * (l0 - l1))


def christoffersen(exc: np.ndarray) -> dict[str, Any]:
    """LR_ind de Christoffersen (1998) con las transiciones de la secuencia de excedencias."""
    a, b = exc[:-1].astype(int), exc[1:].astype(int)
    n00, n01 = int(np.sum((a == 0) & (b == 0))), int(np.sum((a == 0) & (b == 1)))
    n10, n11 = int(np.sum((a == 1) & (b == 0))), int(np.sum((a == 1) & (b == 1)))
    tot = n00 + n01 + n10 + n11
    pi = (n01 + n11) / tot
    pi01 = n01 / (n00 + n01) if n00 + n01 else 0.0
    pi11 = n11 / (n10 + n11) if n10 + n11 else 0.0
    l0 = special.xlogy(n00 + n10, 1 - pi) + special.xlogy(n01 + n11, pi)
    l1 = (special.xlogy(n00, 1 - pi01) + special.xlogy(n01, pi01) + special.xlogy(n10, 1 - pi11)
          + special.xlogy(n11, pi11))
    return {"lr_ind": float(-2 * (l0 - l1)), "transiciones": {"n00": n00, "n01": n01, "n10": n10, "n11": n11},
            "pi01": pi01, "pi11": pi11}


def _backtest(var_p: np.ndarray, res: np.ndarray, es_p: np.ndarray | None, nivel: float, sig: float,
              lim: list[str]) -> dict[str, Any]:
    u = UMBRALES["BT-VAR-001"]
    T = len(res)
    exc = res < -var_p
    x = int(exc.sum())
    p = 1 - nivel
    lr_uc = kupiec(x, T, p)
    ch = christoffersen(exc)
    lr_cc = lr_uc + ch["lr_ind"]
    p_uc, p_ind, p_cc = (float(stats.chi2.sf(lr_uc, 1)), float(stats.chi2.sf(ch["lr_ind"], 1)),
                         float(stats.chi2.sf(lr_cc, 2)))
    zona = None
    if math.isclose(nivel, u["nivel_semaforo"], rel_tol=0, abs_tol=1e-12) and T >= u["dias_semaforo"]:
        x250 = int(exc[-u["dias_semaforo"]:].sum())
        zona = "verde" if x250 <= u["verde_max"] else "amarilla" if x250 <= u["amarilla_max"] else "roja"
    else:
        lim.append(f"semáforo de Basilea solo con VaR al {u['nivel_semaforo']:g} y ≥ {u['dias_semaforo']} días")
    z2 = None
    if es_p is not None:
        if (es_p <= 0).any():
            raise ErrorFicha("BT-VAR-001: ES previsto no positivo")
        z2 = float(np.sum(res * exc / (T * p * es_p)) + 1)
        lim.append("Z₂ sin p-valor: exige simular la distribución prevista (no aportada)")
    else:
        lim.append("sin ES previsto: Z₂ de Acerbi-Székely no calculado")
    return {"n": T, "excedencias": {"n": x, "pct": x / T * PCT, "esperadas": T * p},
            "lr_uc": lr_uc, "p_uc": p_uc, "lr_ind": ch["lr_ind"], "p_ind": p_ind, "lr_cc": lr_cc, "p_cc": p_cc,
            "rechazo": {"uc": p_uc < sig, "ind": p_ind < sig, "cc": p_cc < sig},
            "transiciones": ch["transiciones"], "zona_semaforo": zona, "z2": z2}


def f_bt_var(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    F = "BT-VAR-001"
    lim: list[str] = []
    p, u = _parametros(F, params, _configuracion(ent)), UMBRALES[F]
    v = ent.get("valores") or {}
    nivel, sig = p["nivel"], p["significacion"]
    ref = None
    if v.get("var_previsto") is not None:
        var_p = _vector(v["var_previsto"], f"{F}: var_previsto")
        res = _vector(_requerido(v, "resultados", F), f"{F}: resultados")
        es_p = None if v.get("es_previsto") is None else _vector(v["es_previsto"], f"{F}: es_previsto")
        if len(var_p) != len(res) or (es_p is not None and len(es_p) != len(res)):
            raise ErrorFicha(f"{F}: VaR/ES previstos y resultados no alinean (longitudes distintas)")
        modo = "previsto"
        lim.append("VaR previsto aportado: referencia ingenua (VaR normal con volatilidad histórica) no calculada")
    else:
        if p["horizonte"] != 1:
            raise ErrorFicha(f"{F}: la generación del VaR ex ante con RISK-VAR-001 solo admite horizonte 1")
        hist = _rendimientos(ent, F)
        w = p["ventana_estimacion"]
        if len(hist) <= w:
            raise ErrorFicha(f"{F}: historia de {len(hist)} (≤ ventana de estimación {w})")
        vp, ep, rp = [], [], []
        for t in range(w, len(hist)):
            ventana = hist[t - w:t]                       # solo lo conocido antes de t (ex ante)
            ve = var_es(ventana, nivel, p["metodo_var"], F)
            vp.append(ve["var"])
            ep.append(ve["es"])
            rp.append(-float(np.std(ventana, ddof=1)) * float(stats.norm.ppf(1 - nivel)))
        var_p, es_p, res = np.array(vp), np.array(ep), hist[w:]
        modo = "generado con RISK-VAR-001"
        ref_lim: list[str] = []
        ref = _backtest(np.array(rp), res, None, nivel, sig, ref_lim)
        ref = {"tipo": "VaR normal con volatilidad histórica", "excedencias": ref["excedencias"],
               "lr_uc": ref["lr_uc"], "p_uc": ref["p_uc"], "zona_semaforo": ref["zona_semaforo"]}
    T = len(res)
    if T < u["observaciones_minimas"]:
        if not p["baja_potencia_declarada"]:
            raise ErrorFicha(f"{F}: {T} observaciones (< {u['observaciones_minimas']}) sin declaración de baja potencia")
        if T < 2:
            raise ErrorFicha(f"{F}: {T} observaciones: contraste no definido")
        lim.append(f"baja potencia declarada: {T} observaciones (< {u['observaciones_minimas']})")
    if p["horizonte"] > 1:
        lim.append(f"VaR a {p['horizonte']} periodos: observaciones solapadas, LR con dependencia inducida")
    out = _backtest(var_p, res, es_p, nivel, sig, lim)
    out.update({"nivel": nivel, "significacion": sig, "modo": modo, "referencia_ingenua": ref})
    return out, lim


# ================================================================== ML-CAL-001
def _alinear(pred: Any, real: Any, que: str) -> tuple[np.ndarray, np.ndarray, list[Any] | None]:
    """Predicciones y realizaciones por posición (listas de números) o por fecha (listas de {'fecha', 'valor'})."""
    pl, rl = _lista(pred, f"{que}: predicciones"), _lista(real, f"{que}: realizaciones")
    if pl and all(isinstance(e, dict) for e in pl + rl):
        def por_fecha(lst: list[Any], q: str) -> dict[str, float]:
            out: dict[str, float] = {}
            for i, e in enumerate(lst):
                f = str(pd.Timestamp(_requerido(e, "fecha", f"{q}[{i}]")).date())
                if f in out:
                    raise ErrorFicha(f"{q}: fecha repetida {f}")
                out[f] = _num(_requerido(e, "valor", f"{q}[{i}]"), f"{q}[{i}].valor")
            return out
        dp, dr = por_fecha(pl, f"{que}: predicciones"), por_fecha(rl, f"{que}: realizaciones")
        if set(dp) != set(dr):
            raise ErrorFicha(f"{que}: predicciones y realizaciones no alinean (fechas distintas)")
        fechas = sorted(dp)
        return np.array([dp[f] for f in fechas]), np.array([dr[f] for f in fechas]), fechas
    p, r = _vector(pl, f"{que}: predicciones"), _vector(rl, f"{que}: realizaciones")
    if len(p) != len(r):
        raise ErrorFicha(f"{que}: predicciones ({len(p)}) y realizaciones ({len(r)}) no alinean")
    return p, r, None


_ELEMENTOS_TANDA = 2 ** 22   # elementos por tanda del bootstrap (32 MiB en float64) [técnico: no cambia el resultado]


def _bloque_bootstrap(n: int) -> int:
    return max(1, round(n ** (1 / 3)))       # longitud de bloque de `evaluacion.bss` (FC-EVAL-001)


def mejora_ic(perdida_ref: np.ndarray, perdida_mod: np.ndarray, replicas: int, nivel: float, semilla: int) -> dict[str, Any]:
    """Mejora media (pérdida de la referencia − pérdida del modelo) con IC por bootstrap de bloques móviles."""
    d = perdida_ref - perdida_mod
    n = len(d)
    b = _bloque_bootstrap(n)
    rng = np.random.default_rng(semilla)
    k = math.ceil(n / b)
    inicios = rng.integers(0, n - b + 1, size=(replicas, k))
    # Por tandas de réplicas para acotar la memoria (H-01): la media de cada réplica es la misma que con todas a la vez
    tanda = max(1, _ELEMENTOS_TANDA // (k * b))
    medias = np.concatenate([
        d[(inicios[i:i + tanda, :, None] + np.arange(b)[None, None, :]).reshape(len(inicios[i:i + tanda]), -1)[:, :n]]
        .mean(axis=1) for i in range(0, replicas, tanda)])
    a = (1 - nivel) / 2
    ic = [float(np.quantile(medias, a)), float(np.quantile(medias, 1 - a))]
    demostrada = ic[0] > 0
    return {"mejora_media": float(d.mean()), "ic": ic, "nivel": nivel, "bloque": b, "replicas": replicas,
            "semilla": semilla, "conclusion": "mejora demostrada" if demostrada else "sin mejora demostrada"}


def _comprobar_particiones(parts: Any, n: int, embargo: int, esquema: str, que: str) -> bool:
    lst = _lista(parts, f"{que}: particiones")
    if not lst:
        raise ErrorFicha(f"{que}: particiones vacías")
    prev_fin, ini0 = -1, None
    for i, pa in enumerate(lst):
        pa = _dict(pa, f"{que}: particiones[{i}]")
        e0, e1 = (_entero(x, f"{que}: entrenamiento", 0, n - 1) for x in _lista(_requerido(pa, "entrenamiento", que), que))
        t0, t1 = (_entero(x, f"{que}: prueba", 0, n - 1) for x in _lista(_requerido(pa, "prueba", que), que))
        if e0 > e1 or t0 > t1:
            raise ErrorFicha(f"{que}: partición {i} con inicio > fin")
        if e1 + embargo >= t0:
            raise ErrorFicha(f"{que}: partición {i} con solape entre entrenamiento y prueba (o sin embargo {embargo})")
        if t0 <= prev_fin:
            raise ErrorFicha(f"{que}: particiones de prueba solapadas ({i})")
        if esquema == "walk_forward_expansivo" and ini0 is not None and e0 != ini0:
            raise ErrorFicha(f"{que}: esquema expansivo con inicio de entrenamiento variable ({i})")
        ini0 = e0 if ini0 is None else ini0
        prev_fin = t1
    return True


def _evaluar(tipo: str, p: np.ndarray, y: np.ndarray, ref: np.ndarray | None, cuantil: float | None) -> dict[str, Any]:
    """Métricas fuera de muestra y pérdidas por observación (para la mejora frente a la referencia)."""
    out: dict[str, Any] = {"n": len(y)}
    if tipo == "nivel":
        e = y - p
        out.update({"mae": float(np.mean(np.abs(e))), "rmse": float(math.sqrt(np.mean(e * e))), "sesgo": float(np.mean(e))})
        esc = float(np.mean(np.abs(np.diff(y))))
        out["mase"] = out["mae"] / esc if esc > 0 else None
        perd = e * e
        perd_ref = None if ref is None else (y - ref) ** 2
        if perd_ref is not None:
            sse_ref = float(np.sum(perd_ref))
            out["r2_oos"] = 1 - float(np.sum(perd)) / sse_ref if sse_ref > 0 else None
    elif tipo == "probabilidad":
        pc = np.clip(p, EPS_LOG_SCORE, 1 - EPS_LOG_SCORE)
        perd = (p - y) ** 2
        out.update({"brier": float(np.mean(perd)),
                    "log_score": float(-np.mean(y * np.log(pc) + (1 - y) * np.log(1 - pc))),
                    "acierto": float(np.mean((p >= 0.5) == (y == 1)))})
        perd_ref = None if ref is None else (ref - y) ** 2
        if perd_ref is not None:
            bref = float(np.mean(perd_ref))
            out["bss"] = 1 - out["brier"] / bref if bref > 0 else None
    else:
        assert cuantil is not None
        e = y - p
        perd = np.maximum(cuantil * e, (cuantil - 1) * e)
        out.update({"pinball": float(np.mean(perd)), "cobertura_cuantil": float(np.mean(y <= p)), "cuantil": cuantil})
        perd_ref = None if ref is None else np.maximum(cuantil * (y - ref), (cuantil - 1) * (y - ref))
    out["_perdida"], out["_perdida_ref"] = perd, perd_ref
    return out


def f_ml_cal(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    F = "ML-CAL-001"
    lim: list[str] = []
    p, u = _parametros(F, params, _configuracion(ent)), UMBRALES[F]
    v = ent.get("valores") or {}
    ensayos = _entero(_requerido(v, "ensayos", F), f"{F}: ensayos (número obligatorio)", 1)
    hz = _dict(_requerido(v, "horizontes", F), f"{F}: horizontes")
    claves = p["horizontes"] or sorted(hz)
    if not claves or any(h not in hz for h in claves):
        raise ErrorFicha(f"{F}: horizontes pedidos sin datos")
    tabla: dict[str, Any] = {}
    for h in claves:
        q = f"{F}: horizonte {h}"
        d = _dict(hz[h], q)
        tipo = _opcion(_requerido(d, "tipo", q), f"{q}: tipo", u["tipos"])
        pr, y, fechas = _alinear(_requerido(d, "predicciones", q), _requerido(d, "realizaciones", q), q)
        n = len(y)
        if n < u["observaciones_minimas"]:
            raise ErrorFicha(f"{q}: {n} pares (< {u['observaciones_minimas']})")
        if tipo == "probabilidad" and (((pr < 0) | (pr > 1)).any() or not np.isin(y, (0.0, 1.0)).all()):
            raise ErrorFicha(f"{q}: probabilidades fuera de [0, 1] o realizaciones no binarias")
        cuantil = (_rango(_requerido(d, "cuantil", q), f"{q}: cuantil", 0, 1, True, True) if tipo == "cuantil" else None)
        # Referencia: la aportada (alineada) o la ingenua de la ficha conocida en t (RI-PA o RI-TB; desde t = 1)
        if d.get("referencia") is not None:
            ref = _vector(d["referencia"], f"{q}: referencia")
            if len(ref) != n:
                raise ErrorFicha(f"{q}: referencia y realizaciones no alinean")
            sel, ref_tipo = np.arange(n), "aportada"
        elif tipo in ("nivel", "probabilidad"):
            sel = np.arange(1, n)
            ref = np.empty(n)
            ref[1:] = y[:-1] if tipo == "nivel" else np.cumsum(y)[:-1] / np.arange(1, n)
            ref_tipo = "RI-PA (último valor)" if tipo == "nivel" else "RI-TB (tasa base expansiva)"
        else:
            sel, ref, ref_tipo = np.arange(n), None, None
            lim.append(f"{h}: cuantil sin referencia aportada: sin mejora frente a referencia")
        m = _evaluar(tipo, pr, y, None, cuantil)
        perd, perd_ref = m.pop("_perdida"), None
        m.pop("_perdida_ref")
        if ref is not None:                       # comparación solo donde la referencia existe (RI-PA y RI-TB: t ≥ 1)
            mc = _evaluar(tipo, pr[sel], y[sel], ref[sel], cuantil)
            perd, perd_ref = mc.pop("_perdida"), mc.pop("_perdida_ref")
            m["comparacion_referencia"] = {k: x for k, x in mc.items() if k in ("r2_oos", "bss", "n")}
        m["referencia"] = ref_tipo
        m["mejora_frente_referencia"] = (None if perd_ref is None else
                                         mejora_ic(perd_ref, perd, p["replicas"], p["nivel_ic"], p["semilla"]))
        # Verificación: métricas recomputadas por otra vía
        if tipo == "nivel":
            e = y - pr
            otra = math.sqrt(float(np.mean(e)) ** 2 + float(np.var(e)))
            dif = abs(otra - m["rmse"])
        elif tipo == "probabilidad":
            otra = float(np.mean(pr * pr) - 2 * np.mean(pr * y) + np.mean(y))
            dif = abs(otra - m["brier"])
        else:
            assert cuantil is not None
            otra = float(np.mean((y - pr) * (cuantil - (y < pr))))
            dif = abs(otra - m["pinball"])
        if dif > FICHAS_TOL[F]:
            raise ErrorFicha(f"{q}: métricas recomputadas no coinciden ({dif:.3g})")
        m["verificacion"] = {"metricas_recomputadas": True, "diferencia": dif}
        if d.get("intervalos") is not None:
            iv = _dict(d["intervalos"], f"{q}: intervalos")
            inf, sup = _vector(_requerido(iv, "inferior", q), f"{q}: inferior"), _vector(_requerido(iv, "superior", q), f"{q}: superior")
            niv = _rango(_requerido(iv, "nivel", q), f"{q}: intervalos.nivel", 0, 1, True, True)
            if len(inf) != n or len(sup) != n or (inf > sup).any():
                raise ErrorFicha(f"{q}: intervalos no alineados o con inferior > superior")
            m["cobertura_intervalos"] = {"nivel": niv, "cobertura": float(np.mean((y >= inf) & (y <= sup)))}
        if d.get("particiones") is not None:
            emb = _entero(d.get("embargo", 0), f"{q}: embargo", 0)
            m["particiones_sin_solape"] = _comprobar_particiones(d["particiones"], n, emb, p["esquema"], q)
        else:
            m["particiones_sin_solape"] = None
            lim.append(f"{h}: sin particiones declaradas: no se verifica la ausencia de solape")
        if d.get("regimenes") is not None:
            reg = _lista(d["regimenes"], f"{q}: regimenes")
            if len(reg) != n or not all(_texto(x) for x in reg):
                raise ErrorFicha(f"{q}: regímenes no alineados o vacíos")
            ra = np.array(reg)
            m["por_regimen"] = {}
            for k in sorted(set(reg)):
                s = ra == k
                mk = _evaluar(tipo, pr[s], y[s], None, cuantil)
                mk.pop("_perdida")
                mk.pop("_perdida_ref")
                m["por_regimen"][k] = mk
        if fechas is not None:
            m["fechas"] = [fechas[0], fechas[-1]]
        if p["metricas"] is not None:
            m = {k: x for k, x in m.items() if k in p["metricas"] or k in ("n", "verificacion", "referencia")}
        m["tipo"] = tipo
        tabla[h] = m
    return {"esquema": p["esquema"], "ensayos": ensayos, "horizontes": tabla}, lim


# ================================================================== ML-PRED-001
def _logistica(X: np.ndarray, y: np.ndarray, lam: float, que: str) -> np.ndarray:
    """Logística con penalización L2 (sin penalizar el intercepto) por Newton-Raphson."""
    u = UMBRALES["ML-PRED-001"]
    Z = np.column_stack([np.ones(len(X)), X])
    w = np.zeros(Z.shape[1])
    pen = np.full(Z.shape[1], lam)
    pen[0] = 0.0
    previo = math.inf
    for _ in range(u["iteraciones_maximas"]):
        eta = Z @ w
        pr = special.expit(eta)
        obj = float(np.sum(np.logaddexp(0, eta) - y * eta) + 0.5 * np.sum(pen * w * w))
        if abs(previo - obj) <= u["tolerancia_newton"] * max(1.0, abs(obj)):
            return w
        previo = obj
        g = Z.T @ (pr - y) + pen * w
        H = (Z * (pr * (1 - pr))[:, None]).T @ Z + np.diag(pen)
        w = w - np.linalg.solve(H, g)
    raise ErrorFicha(f"{que}: la logística no converge en {u['iteraciones_maximas']} iteraciones")


def _ridge(X: np.ndarray, y: np.ndarray, lam: float) -> np.ndarray:
    Z = np.column_stack([np.ones(len(X)), X])
    pen = np.full(Z.shape[1], lam)
    pen[0] = 0.0
    return np.asarray(np.linalg.solve(Z.T @ Z + np.diag(pen), Z.T @ y))


def _ajustar_predecir(modelo: str, X: np.ndarray, y: np.ndarray, Xn: np.ndarray, lam: float, que: str) -> np.ndarray:
    mu, sd = X.mean(axis=0), X.std(axis=0, ddof=1)
    sd = np.where(sd > 0, sd, 1.0)                  # variable constante en la ventana: se deja sin escalar
    Xs, Xns = (X - mu) / sd, (Xn - mu) / sd
    if modelo == "logistica_L2":
        if len(np.unique(y)) < 2:
            return np.full(len(Xn), float(y[0]))
        w = _logistica(Xs, y, lam, que)
        return np.asarray(special.expit(w[0] + Xns @ w[1:]))
    w = _ridge(Xs, y, lam)
    return np.asarray(w[0] + Xns @ w[1:])


def _perdida(modelo: str, pr: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean((pr - y) ** 2))


def _elegir_lambda(modelo: str, X: np.ndarray, y: np.ndarray, rejilla: list[float], emb: int, que: str) -> float:
    """λ por validación temporal interna: el último tramo (20 % [PROPUESTO]) del entrenamiento, con embargo."""
    n = len(y)
    corte = n - max(emb + 1, n // 5)
    if corte - emb < 2 or len(rejilla) == 1:
        return rejilla[0]
    X1, y1 = X[:corte - emb], y[:corte - emb]
    X2, y2 = X[corte:], y[corte:]
    perdidas = [_perdida(modelo, _ajustar_predecir(modelo, X1, y1, X2, lam, que), y2) for lam in rejilla]
    return rejilla[int(np.argmin(perdidas))]


def _platt(praw: np.ndarray, y: np.ndarray, que: str) -> tuple[float, float] | None:
    if len(np.unique(y)) < 2:
        return None
    lg = special.logit(np.clip(praw, EPS_LOG_SCORE, 1 - EPS_LOG_SCORE))[:, None]
    w = _logistica(lg, y, 0.0, que)
    return float(w[0]), float(w[1])


def _isotonica(praw: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Regresión isotónica por PAV: devuelve (umbrales de p ordenados, valor ajustado en cada bloque)."""
    orden = np.argsort(praw, kind="mergesort")
    xs, ys = praw[orden], y[orden].astype(float)
    bloques: list[list[float]] = []            # [suma, peso, x_max]
    for xv, yv in zip(xs, ys):
        bloques.append([yv, 1.0, xv])
        while len(bloques) > 1 and bloques[-2][0] / bloques[-2][1] >= bloques[-1][0] / bloques[-1][1]:
            s, w_, xm = bloques.pop()
            bloques[-1][0] += s
            bloques[-1][1] += w_
            bloques[-1][2] = xm
    return np.array([b[2] for b in bloques]), np.array([b[0] / b[1] for b in bloques])


def _calibrar(metodo: str, praw_hist: np.ndarray, y_hist: np.ndarray, praw: np.ndarray, que: str) -> np.ndarray:
    if metodo == "ninguna" or len(y_hist) == 0:
        return praw
    if metodo in ("auto", "platt"):
        ab = _platt(praw_hist, y_hist, que)
        if ab is None:
            return praw
        return np.asarray(special.expit(ab[0] + ab[1] * special.logit(np.clip(praw, EPS_LOG_SCORE, 1 - EPS_LOG_SCORE))))
    xs, vs = _isotonica(praw_hist, y_hist)
    idx = np.clip(np.searchsorted(xs, praw, side="left"), 0, len(vs) - 1)
    return vs[idx]


def _pendiente_calibracion(p: np.ndarray, y: np.ndarray, que: str) -> float | None:
    if len(np.unique(y)) < 2:
        return None
    lg = special.logit(np.clip(p, EPS_LOG_SCORE, 1 - EPS_LOG_SCORE))
    if np.ptp(lg) == 0:
        return None
    return float(_logistica(lg[:, None], y, 0.0, que)[1])


def _fechas_iso(x: Any, que: str) -> list[pd.Timestamp]:
    out = []
    for i, f in enumerate(_lista(x, que)):
        if not isinstance(f, str):
            raise ErrorFicha(f"{que}[{i}]: fecha no válida (texto ISO)")
        t = pd.Timestamp(f)
        if pd.isna(t):
            raise ErrorFicha(f"{que}[{i}]: fecha no válida")
        out.append(t)
    return out


def _walk_forward(modelo: str, X: np.ndarray, y: np.ndarray, p: dict[str, Any], emb: int, movil: bool,
                  que: str) -> dict[str, Any]:
    L = len(y)
    m0 = int(p["fraccion_inicial"] * L)
    limites = np.linspace(m0, L, p["pliegues"] + 1).astype(int)
    ventana = m0 - emb + 1
    praw_all: list[float] = []
    pcal_all: list[float] = []
    idx_all: list[int] = []
    parts, elegidos = [], []
    for k in range(p["pliegues"]):
        a, b = int(limites[k]), int(limites[k + 1])
        if b <= a:
            continue
        fin = a - emb                                   # entrenamiento: i ≤ a − embargo (etiquetas ya conocidas)
        ini = max(0, fin - ventana + 1) if movil else 0
        if fin - ini + 1 < 2:
            raise ErrorFicha(f"{que}: pliegue {k} sin entrenamiento suficiente")
        Xe, ye = X[ini:fin + 1], y[ini:fin + 1]
        lam = _elegir_lambda(modelo, Xe, ye, p["rejilla"], emb, que)
        elegidos.append(lam)
        praw = _ajustar_predecir(modelo, Xe, ye, X[a:b], lam, que)
        if modelo == "logistica_L2":
            conocidos = [j for j, i in enumerate(idx_all) if i <= a - emb]
            pcal = _calibrar(p["calibracion"], np.array(praw_all)[conocidos], y[np.array(idx_all, dtype=int)[conocidos]],
                             praw, que)
        else:
            pcal = praw
        praw_all += praw.tolist()
        pcal_all += np.asarray(pcal).tolist()
        idx_all += list(range(a, b))
        parts.append({"entrenamiento": [ini, fin], "prueba": [a, b - 1], "lambda": lam})
    return {"indices": np.array(idx_all, dtype=int), "praw": np.array(praw_all), "p": np.array(pcal_all),
            "particiones": parts, "lambdas": elegidos}


def _particiones_correctas(parts: list[dict[str, Any]], emb: int) -> bool:
    fin_prueba = -1
    for pa in parts:
        if pa["entrenamiento"][1] + emb > pa["prueba"][0] or pa["prueba"][0] <= fin_prueba:
            return False
        fin_prueba = pa["prueba"][1]
    return True


def f_ml_pred(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    F = "ML-PRED-001"
    lim: list[str] = []
    p, u = _parametros(F, params, _configuracion(ent)), UMBRALES[F]
    v = ent.get("valores") or {}
    fechas = _fechas_iso(_requerido(v, "fechas", F), f"{F}: fechas")
    n = len(fechas)
    if any(b <= a for a, b in itertools.pairwise(fechas)):
        raise ErrorFicha(f"{F}: fechas no estrictamente crecientes")
    obj = _dict(_requerido(v, "objetivo", F), f"{F}: objetivo")
    if not _texto(obj.get("criterio_resolucion")):
        raise ErrorFicha(f"{F}: objetivo sin criterio de resolución")
    tipo = _opcion(_requerido(obj, "tipo", f"{F}: objetivo"), f"{F}: objetivo.tipo", ["direccion", "nivel"])
    h = _entero(_requerido(obj, "horizonte", f"{F}: objetivo"), f"{F}: objetivo.horizonte", 1)
    serie = _vector(_requerido(obj, "serie", f"{F}: objetivo"), f"{F}: objetivo.serie")
    if len(serie) != n:
        raise ErrorFicha(f"{F}: objetivo y fechas no alinean")
    modelo = p["modelo"]
    if (tipo == "direccion") != (modelo == "logistica_L2"):
        raise ErrorFicha(f"{F}: modelo {modelo} no corresponde a un objetivo de {tipo} (logistica_L2 ↔ direccion)")
    emb = p["embargo"] if p["embargo"] is not None else h
    if emb < h:
        raise ErrorFicha(f"{F}: embargo {emb} < horizonte {h} (la ficha exige embargo ≥ h)")
    variables = _dict(_requerido(v, "variables", F), f"{F}: variables")
    if not variables:
        raise ErrorFicha(f"{F}: sin variables")
    cols = []
    for nombre in sorted(variables):
        q = f"{F}: variable {nombre}"
        d = _dict(variables[nombre], q)
        if d.get("conocible_desde") is None:
            raise ErrorFicha(f"{q}: sin regla de conocibilidad (conocible_desde)")
        x = _vector(_requerido(d, "serie", q), f"{q}: serie")
        cd = _fechas_iso(d["conocible_desde"], f"{q}: conocible_desde")
        if len(x) != n or len(cd) != n:
            raise ErrorFicha(f"{q}: serie o conocibilidad no alinean con las fechas")
        fuga = [i for i in range(n) if cd[i] > fechas[i]]
        if fuga:
            raise ErrorFicha(f"{q}: fuga de información (conocible después de la fecha de uso en {len(fuga)} puntos)")
        cols.append(x)
    X = np.column_stack(cols)
    L = n - h
    if tipo == "direccion":
        y = (serie[h:] > serie[:-h]).astype(float)
    else:
        if (serie <= 0).any():
            raise ErrorFicha(f"{F}: objetivo de nivel con valores no positivos (rendimiento simple no definido)")
        y = serie[h:] / serie[:-h] - 1
    independientes = L // h
    if independientes < u["observaciones_minimas"]:
        raise ErrorFicha(f"{F}: {independientes} observaciones independientes (< {u['observaciones_minimas']})")
    Xl = X[:L]
    wf = _walk_forward(modelo, Xl, y, p, emb, False, F)
    idx, pr = wf["indices"], wf["p"]
    yo = y[idx]
    # Referencia ingenua conocida en t: RI-TB (dirección) o RI-MH (nivel): media de las etiquetas con i ≤ t − embargo
    acum = np.concatenate([[0.0], np.cumsum(y)])
    ref = np.array([acum[t - emb + 1] / (t - emb + 1) for t in idx])
    mt = _evaluar("probabilidad" if tipo == "direccion" else "nivel", pr, yo, ref, None)
    perd, perd_ref = mt.pop("_perdida"), mt.pop("_perdida_ref")
    if tipo == "nivel":
        perd, perd_ref = (yo - pr) ** 2, (yo - ref) ** 2
    mejora = mejora_ic(perd_ref, perd, p["replicas"], p["nivel_ic"], p["semilla"])
    if tipo == "direccion":
        mt["ece"] = ece_fc_cal(pr, yo)["ece"]
        mt["pendiente_b"] = _pendiente_calibracion(pr, yo, F)
    # Segunda vía: ventana móvil del mismo tamaño que la inicial
    wm = _walk_forward(modelo, Xl, y, p, emb, True, F)
    mm = _evaluar("probabilidad" if tipo == "direccion" else "nivel", wm["p"], y[wm["indices"]], None, None)
    mm.pop("_perdida")
    mm.pop("_perdida_ref")
    # Predicción actual: entrenamiento con i ≤ (n − 1) − embargo; variables de la última fecha
    fin = n - 1 - emb
    if fin + 1 > L:
        fin = L - 1
    lam = _elegir_lambda(modelo, Xl[:fin + 1], y[:fin + 1], p["rejilla"], emb, F)
    praw_act = _ajustar_predecir(modelo, Xl[:fin + 1], y[:fin + 1], X[-1:], lam, F)
    if modelo == "logistica_L2":
        conocidos = idx <= (n - 1) - emb
        p_act = float(_calibrar(p["calibracion"], wf["praw"][conocidos], y[idx[conocidos]], praw_act, F)[0])
    else:
        p_act = float(praw_act[0])
    if modelo == "logistica_L2" and p["calibracion"] == "auto":
        lim.append("calibración «auto» = Platt (isotónica solo a petición) [PROPUESTO]")
    lim.append("solo modelos lineales regularizados: el ensamble de árboles no está disponible en el ejecutor")
    if mejora["conclusion"] == "sin mejora demostrada":
        lim.append("sin mejora demostrada frente a la referencia ingenua")
    return {"objetivo": {"tipo": tipo, "horizonte": h, "criterio_resolucion": obj["criterio_resolucion"]},
            "modelo": modelo, "embargo": emb, "calibracion": p["calibracion"],
            "prediccion_actual": {"fecha": str(fechas[-1].date()),
                                  ("probabilidad" if tipo == "direccion" else "nivel"): p_act, "lambda": lam},
            "metricas_oos": mt, "mejora_frente_referencia": mejora,
            "referencia": "RI-TB (tasa base expansiva)" if tipo == "direccion" else "RI-MH (media histórica conocida)",
            "ensayos": {"n": len(p["rejilla"]), "rejilla": p["rejilla"],
                        "elegidos": {f"{lam_:g}": wf["lambdas"].count(lam_) for lam_ in p["rejilla"]}},
            "particiones": wf["particiones"],
            "verificacion": {"particiones_sin_solape": _particiones_correctas(wf["particiones"], emb)},
            "predicciones_oos": [{"indice": int(i), "prediccion": float(a), "realizacion": float(b)}
                                 for i, a, b in zip(idx, pr, yo)],
            "segunda_via_ventana_movil": mm}, lim


# ================================================================== DEC-VOI-001
def _prior(v: dict[str, Any], F: str) -> dict[str, Any]:
    if v.get("rango_plausible") is not None:
        r = _con_fuente(v["rango_plausible"], f"{F}: rango_plausible")
        lo = _num(_requerido(r, "inferior", f"{F}: rango_plausible"), f"{F}: inferior")
        hi = _num(_requerido(r, "superior", f"{F}: rango_plausible"), f"{F}: superior")
        if hi <= lo:
            raise ErrorFicha(f"{F}: rango plausible vacío (superior ≤ inferior)")
        return {"tipo": "uniforme", "lo": lo, "hi": hi, "media": (lo + hi) / 2}
    if v.get("muestras") is not None:
        m = _con_fuente(v["muestras"], f"{F}: muestras")
        s = _vector(_requerido(m, "valores", f"{F}: muestras"), f"{F}: muestras.valores", 2)
        return {"tipo": "empirica", "s": s, "lo": float(s.min()), "hi": float(s.max()), "media": float(s.mean())}
    raise ErrorFicha(f"{F}: aclaración: falta el rango plausible del efecto del cálculo (rango_plausible o muestras)")


def evpi(pri: dict[str, Any], u: float) -> float:
    """EVPI de «actuar si S ≥ u» (pago S − u) frente a decidir con E[S]: E[max(S − u, 0)] − max(E[S] − u, 0)."""
    if pri["tipo"] == "uniforme":
        lo, hi = pri["lo"], pri["hi"]
        c = min(max(u, lo), hi)
        e_max = ((hi - c) * ((hi + c) / 2 - u)) / (hi - lo)
    else:
        e_max = float(np.mean(np.maximum(pri["s"] - u, 0)))
    return e_max - max(pri["media"] - u, 0.0)


def evsi(pri: dict[str, Any], u: float, sigma: float) -> float:
    """EVSI con una señal X = S + ε, ε ~ N(0, σ²). Regla de Bayes: actuar si E[S | X] ≥ u, que es X ≥ x*
    (E[S | X] crece con X); valor = E[(S − u)·Φ((S − x*)/σ)]. Con σ = 0, EVSI = EVPI."""
    if sigma == 0:
        return evpi(pri, u)
    base = max(pri["media"] - u, 0.0)
    if not pri["lo"] < u < pri["hi"]:
        return 0.0

    def media_post(x: float) -> float:
        if pri["tipo"] == "uniforme":
            a, b = (pri["lo"] - x) / sigma, (pri["hi"] - x) / sigma
            masa = float(stats.norm.cdf(b) - stats.norm.cdf(a))
            if masa <= 0:
                return pri["lo"] if x < pri["lo"] else pri["hi"]
            return float(x + sigma * (stats.norm.pdf(a) - stats.norm.pdf(b)) / masa)
        lw = -0.5 * ((x - pri["s"]) / sigma) ** 2
        w = np.exp(lw - lw.max())
        return float(np.sum(w * pri["s"]) / np.sum(w))

    span = pri["hi"] - pri["lo"]
    a_, b_ = pri["lo"] - span - sigma, pri["hi"] + span + sigma
    for _ in range(UMBRALES["DEC-VOI-001"]["ampliaciones_maximas"]):   # se amplía el intervalo hasta encerrar x*
        if media_post(a_) < u < media_post(b_):
            break
        a_, b_ = a_ - span - sigma, b_ + span + sigma
    else:
        raise ErrorFicha("DEC-VOI-001: no se encuentra el corte de la regla de Bayes (umbral pegado al borde del rango)")
    x_corte = optimize.brentq(lambda x: media_post(x) - u, a_, b_, xtol=1e-12)
    if pri["tipo"] == "uniforme":
        val = integrate.quad(lambda s: (s - u) * float(stats.norm.cdf((s - x_corte) / sigma)),
                             pri["lo"], pri["hi"], limit=200)[0] / span
    else:
        val = float(np.mean((pri["s"] - u) * stats.norm.cdf((pri["s"] - x_corte) / sigma)))
    return val - base


def _decision(nombre: str, pri: dict[str, Any], u: float, banda: float, sigma: float | None) -> dict[str, Any]:
    alcanza = pri["hi"] >= u - banda and pri["lo"] <= u + banda
    actuar_previo = pri["media"] >= u
    if pri["tipo"] == "uniforme":
        p_sup = min(max((pri["hi"] - u) / (pri["hi"] - pri["lo"]), 0.0), 1.0)
    else:
        p_sup = float(np.mean(pri["s"] >= u))
    vpi = evpi(pri, u) if alcanza else 0.0
    vsi = (evsi(pri, u, sigma) if alcanza else 0.0) if sigma is not None else None
    return {"decision": nombre, "umbral": u, "alcanza_banda_marginal": alcanza, "evpi": vpi, "evsi": vsi,
            "decision_previa": "por_encima" if actuar_previo else "por_debajo",
            "probabilidad_cambio": (1 - p_sup) if actuar_previo else p_sup}


def _umbrales_ht03(cfg: dict[str, Any] | None, dim: str) -> tuple[dict[str, float], float]:
    """Umbrales de la dimensión y banda marginal de HT-03, de `parametros_ht03` de la configuración del Motor (H-04)."""
    ht = parametros_ht03(cfg)
    val = _dict(ht.get("umbrales"), "DEC-VOI-001: parametros_ht03.umbrales de la configuración")
    umbrales = {k: _num(_requerido(val, c, "DEC-VOI-001: parametros_ht03.umbrales"), f"DEC-VOI-001: umbral {c} de HT-03")
                for k, c in UMBRALES["DEC-VOI-001"]["umbrales"][dim].items()}
    banda = _rango(_requerido(ht, "banda_marginal", "DEC-VOI-001: parametros_ht03"), "DEC-VOI-001: banda marginal de HT-03", 0)
    return umbrales, banda


def f_dec_voi(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    F = "DEC-VOI-001"
    lim: list[str] = []
    cfg = _configuracion(ent)
    p = _parametros(F, params, cfg)
    v = ent.get("valores") or {}
    punt = _dict(_requerido(v, "puntuacion", F), f"{F}: puntuacion")
    dim = _opcion(_requerido(punt, "dimension", f"{F}: puntuacion"), f"{F}: dimension", ["e", "a", "t"]).upper()
    actual = _num(_requerido(punt, "actual", f"{F}: puntuacion"), f"{F}: actual")
    pri = _prior(v, F)
    sigma = None
    if v.get("verosimilitud") is not None:
        sigma = _rango(_requerido(_dict(v["verosimilitud"], f"{F}: verosimilitud"), "desviacion", F),
                       f"{F}: verosimilitud.desviacion", 0)
    else:
        lim.append("sin verosimilitud del cálculo: solo EVPI (EVSI no calculado)")
    umbrales, banda = _umbrales_ht03(cfg, dim)
    decisiones = [_decision(f"umbral {k} ({dim})", pri, x, banda, sigma) for k, x in sorted(umbrales.items())]
    if v.get("ranking") is not None:
        rk = _dict(v["ranking"], f"{F}: ranking")
        rk_op = _num(_requerido(rk, "rk_opcion", f"{F}: ranking"), f"{F}: rk_opcion")
        rk_fr = _num(_requerido(rk, "rk_frontera", f"{F}: ranking"), f"{F}: rk_frontera")
        amp = _rango(_requerido(rk, "amplitud_rk", f"{F}: ranking"), f"{F}: amplitud_rk", 0, abierto_lo=True)
        cambia = abs(rk_op - rk_fr) <= amp
        pri_rk = {"tipo": "uniforme", "lo": rk_op - amp, "hi": rk_op + amp, "media": rk_op}
        d = _decision("orden del top-3 (RK)", pri_rk, rk_fr, 0.0, sigma)
        d["alcanza_banda_marginal"] = cambia
        if not cambia:
            d["evpi"], d["evsi"] = 0.0, (0.0 if sigma is not None else None)
        decisiones.append(d)
    else:
        lim.append("sin ranking: no se evalúa el cambio del orden del top-3")
    regla_cero = not any(d["alcanza_banda_marginal"] for d in decisiones)
    clave = "evsi" if sigma is not None else "evpi"
    voi = 0.0 if regla_cero else max(d[clave] for d in decisiones)
    p_cambio = 0.0 if regla_cero else max(d["probabilidad_cambio"] for d in decisiones if d["alcanza_banda_marginal"])
    voi_uc = None
    if v.get("valor_punto_uc") is not None:
        voi_uc = voi * _rango(v["valor_punto_uc"], f"{F}: valor_punto_uc", 0, abierto_lo=True)
        recomendacion = "EJECUTAR" if voi_uc > p["coste_uc"] else "NO_EJECUTAR"
    else:
        recomendacion = "EJECUTAR" if voi > 0 else "NO_EJECUTAR"
        lim.append("sin equivalencia puntos → UC: la recomendación no pondera el coste (EJECUTAR si VOI > 0)")
    return {"dimension": dim, "puntuacion_actual": actual, "rango_plausible": {"inferior": pri["lo"], "superior": pri["hi"],
                                                                             "media": pri["media"], "tipo": pri["tipo"]},
            "decisiones": decisiones, "regla_simple_voi_cero": regla_cero, "voi_puntos": voi, "voi_uc": voi_uc,
            "medida": clave.upper(), "probabilidad_cambio_decision": p_cambio, "coste_uc": p["coste_uc"],
            "banda_marginal": banda,
            "recomendacion_tecnica": recomendacion, "decision_del_solicitante": True,
            "referencia_ingenua": {"ejecutar_siempre_coste_uc": p["coste_uc"], "no_ejecutar_nunca_voi_perdido": voi}}, lim


# ================================================================== registro de fichas
FICHAS_TOL: dict[str, float] = {
    "RISK-VAR-001": 1e-6, "SIM-MC-001": 1e-6, "SCN-H-001": 1e-6, "BT-DSR-001": 1e-8, "BT-PBO-001": 1e-8,
    "BT-VAR-001": 1e-8, "ML-CAL-001": 1e-8, "ML-PRED-001": 1e-6, "DEC-VOI-001": 1e-8}

FICHAS: dict[str, dict[str, Any]] = {
    "RISK-VAR-001": {"fn": _cerrado("RISK-VAR-001", f_risk_var), "modulo": "MC-07", "version": "1.1",
                     "cifra": "ESTADISTICA", "ri": "VaR normal con volatilidad histórica", "tol": FICHAS_TOL["RISK-VAR-001"]},
    "SIM-MC-001": {"fn": _cerrado("SIM-MC-001", f_sim_mc), "modulo": "MC-05", "version": "1.1", "cifra": "ESTADISTICA",
                   "ri": "RI-CLI (bootstrap simple de la historia)", "tol": FICHAS_TOL["SIM-MC-001"]},
    "SCN-H-001": {"fn": _cerrado("SCN-H-001", f_scn_h), "modulo": "MC-05", "version": "1.0", "cifra": "ESTADISTICA",
                  "ri": "RI-CLI (bootstrap incondicional) y RI-PA", "tol": FICHAS_TOL["SCN-H-001"]},
    "BT-DSR-001": {"fn": _cerrado("BT-DSR-001", f_bt_dsr), "modulo": "MC-10", "version": "1.0", "cifra": "ESTADISTICA",
                   "ri": "SR = 0 y RI-CM", "tol": FICHAS_TOL["BT-DSR-001"]},
    "BT-PBO-001": {"fn": _cerrado("BT-PBO-001", f_bt_pbo), "modulo": "MC-10", "version": "1.0", "cifra": "ESTADISTICA",
                   "ri": "selección aleatoria de configuración", "tol": FICHAS_TOL["BT-PBO-001"]},
    "BT-VAR-001": {"fn": _cerrado("BT-VAR-001", f_bt_var), "modulo": "MC-10", "version": "1.0", "cifra": "ESTADISTICA",
                   "ri": "VaR normal con volatilidad histórica", "tol": FICHAS_TOL["BT-VAR-001"]},
    "ML-CAL-001": {"fn": _cerrado("ML-CAL-001", f_ml_cal), "modulo": "MC-06", "version": "1.1", "cifra": "ESTADISTICA",
                   "ri": "RI-PA, RI-TB o RI-MH según el objetivo", "tol": FICHAS_TOL["ML-CAL-001"]},
    "ML-PRED-001": {"fn": _cerrado("ML-PRED-001", f_ml_pred), "modulo": "MC-06", "version": "1.0", "cifra": "ESTADISTICA",
                    "ri": "RI-TB, RI-PA o RI-MH según objetivo", "tol": FICHAS_TOL["ML-PRED-001"]},
    "DEC-VOI-001": {"fn": _cerrado("DEC-VOI-001", f_dec_voi), "modulo": "MC-07", "version": "1.0", "cifra": "ESTADISTICA",
                    "ri": "ejecutar siempre (coste) frente a no ejecutar nunca", "tol": FICHAS_TOL["DEC-VOI-001"]},
}


# ================================================================== datos sintéticos de los casos de control
# Datos deterministas (semillas fijas de construcción o rejillas exactas). Cada caso comprueba la identidad de la
# «Verificación» de su ficha con datos que no anulan sus términos; las tolerancias de los contrastes por simulación
# (4 errores estándar; 10 % en la curtosis) y de la segunda vía (1 %) son [PROPUESTO INC-T112-01].
_EE_MC = 4                # errores estándar admitidos frente a la solución analítica (simulación)
_TOL_CURTOSIS = 0.10      # error relativo admitido en la curtosis simulada frente a la analítica
_TOL_VIA = 0.01           # diferencia relativa admitida entre histórico y paramétrico en una muestra normal exacta


def _cerca(a: Any, b: float, tol: float) -> bool:
    return a is not None and math.isclose(float(a), b, rel_tol=tol, abs_tol=tol)


def _rejilla_var() -> list[float]:
    """x_i = (i − 500)/10 000, i = 0…1000, en orden barajado: con nivel 0,975, (n − 1)(1 − nivel) = 25 es entero."""
    x = (np.arange(1001) - 500) / 10_000
    return [float(e) for e in np.random.default_rng(112).permutation(x)]


def _normal_exacta(mu: float, sigma: float, n: int, semilla: int) -> list[float]:
    """Muestra con media y desviación (ddof = 1) muestrales exactamente μ y σ."""
    z = np.random.default_rng(semilla).standard_normal(n)
    z = (z - z.mean()) / z.std(ddof=1)
    return [float(e) for e in mu + sigma * z]


def _normal_cuantiles(mu: float, sigma: float, n: int) -> list[float]:
    return [float(e) for e in mu + sigma * stats.norm.ppf((np.arange(n) + 0.5) / n)]


def _colas_gruesas(n: int, semilla: int) -> list[float]:
    rng = np.random.default_rng(semilla)
    return [float(e) for e in 0.0002 + 0.008 * rng.standard_t(5, n) - 0.004 * rng.exponential(1.0, n) + 0.004]


_R_VAR_REJ = _rejilla_var()
_R_VAR_NORMAL = _normal_exacta(0.0004, 0.012, 600, 11201)
_R_VAR_COLAS = _colas_gruesas(1500, 11202)
_R_VAR_CUANT = _normal_cuantiles(0.0003, 0.01, 2000)


def _caso_t(r: dict[str, Any]) -> bool:
    x = np.array(_R_VAR_COLAS)
    mu, s = x.mean(), x.std(ddof=1)
    nu = 4 + 6 / stats.kurtosis(x, fisher=True, bias=False)
    esc = s * math.sqrt((nu - 2) / nu)
    q = stats.t.ppf(0.025, nu)
    es = -mu + esc * (nu + q * q) / (nu - 1) * stats.t.pdf(q, nu) / 0.025
    return (_cerca(r["var"], -(mu + esc * q), 1e-10) and _cerca(r["es"], es, 1e-10) and r["es"] >= r["var"]
            and r["verificacion"]["cuantiles_monotonos"])


def _caso_cf(r: dict[str, Any]) -> bool:
    x = np.array(_R_VAR_COLAS)
    mu, s = x.mean(), x.std(ddof=1)
    S, K = stats.skew(x, bias=False), stats.kurtosis(x, fisher=True, bias=False)
    z = stats.norm.ppf(0.025)
    zcf = z + (z * z - 1) * S / 6 + (z ** 3 - 3 * z) * K / 24 - (2 * z ** 3 - 5 * z) * S * S / 36
    curva = [c["var"] for c in r["verificacion"]["curva_nivel"]]
    return (_cerca(r["var"], -(mu + s * zcf), 1e-10) and r["es"] > r["var"] and len(curva) == 3
            and curva[0] < curva[1] < curva[2])


def _caso_evt(r: dict[str, Any]) -> bool:
    d = r["detalle_metodo"]
    perd = -np.array(_R_VAR_COLAS)
    umbral = float(np.quantile(perd, 0.90))
    nu = int(np.sum(perd > umbral))
    xi, b = d["xi"], d["beta"]
    var = umbral + b / xi * ((len(perd) / nu * 0.025) ** (-xi) - 1)
    return (_cerca(d["umbral"], umbral, 1e-12) and d["excedencias"] == nu and _cerca(r["var"], var, 1e-10)
            and _cerca(r["es"], (var + b - xi * umbral) / (1 - xi), 1e-10) and r["es"] >= r["var"])


def _garch_control(n: int, semilla: int) -> list[float]:
    """Serie GARCH(1,1) de control (ω = 2e-6, α = 0,08, β = 0,90) con innovaciones normales."""
    rng = np.random.default_rng(semilla)
    h, out = 2e-6 / (1 - 0.98), []
    for _ in range(n):
        e = math.sqrt(h) * float(rng.standard_normal())
        out.append(0.0003 + e)
        h = 2e-6 + 0.08 * e * e + 0.9 * h
    return out


_R_VAR_GARCH = _garch_control(1500, 11212)


def _fhs_con(x: np.ndarray, om: float, al: float, be: float, nivel: float) -> tuple[float, float, float]:
    """VaR, ES y σ_T+1 del histórico filtrado con un GARCH(1,1) dado, con la recursión escrita aquí (bucle)."""
    e = x - x.mean()
    hs = [float(np.var(e))]
    for t in range(1, len(e)):
        hs.append(om + al * e[t - 1] ** 2 + be * hs[-1])
    z = e / np.sqrt(hs)
    sig = math.sqrt(om + al * e[-1] ** 2 + be * hs[-1])
    q = float(np.quantile(z, 1 - nivel))
    return -(x.mean() + sig * q), -(x.mean() + sig * float(np.mean(z[z <= q]))), sig


@functools.cache
def _fhs_referencia() -> tuple[float, float, float, float]:
    """Óptimo de referencia de la QMLE con objetivo de varianza de la serie de control, calculado aparte de `garch_qmle`
    (QA r01 de T-112, H-08): otro optimizador (Powell, tres arranques) sobre (α, β) sin transformar, con la recursión
    como filtro lineal propio. Devuelve α, β y el VaR y el ES al 0,975 con ese óptimo."""
    x = np.array(_R_VAR_GARCH)
    e = x - x.mean()
    v = float(np.var(e))

    def nlv(th: np.ndarray) -> float:
        al, be = float(th[0]), float(th[1])
        if al <= 0 or be <= 0 or al + be >= 1:
            return math.inf
        h = signal.lfilter([1.0], [1.0, -be], np.r_[v, v * (1 - al - be) + al * e[:-1] ** 2], zi=[0.0])[0]
        return float(0.5 * np.sum(np.log(h) + e * e / h))

    with np.errstate(all="ignore"):                  # fuera de la región admisible, −ln L = ∞ (Powell lo descarta)
        mejor = min((optimize.minimize(nlv, np.array(x0), method="Powell", options={"xtol": 1e-12, "ftol": 1e-14})
                     for x0 in ([0.05, 0.9], [0.15, 0.8], [0.02, 0.97])), key=lambda o: float(o.fun))
    al, be = float(mejor.x[0]), float(mejor.x[1])
    var, es, _ = _fhs_con(x, v * (1 - al - be), al, be, 0.975)
    return al, be, var, es


def _caso_fhs(r: dict[str, Any]) -> bool:
    """VaR y ES con los residuos del GARCH publicado; ω = σ̄²(1 − α − β) (objetivo de varianza); y VaR y ES iguales,
    a la tolerancia de la ficha, a los de un óptimo de referencia calculado aparte (H-08)."""
    d = r["detalle_metodo"]
    x = np.array(_R_VAR_GARCH)
    g = d["garch"]
    var, es, sig = _fhs_con(x, g["omega"], g["alpha"], g["beta"], 0.975)
    _, _, var_ref, es_ref = _fhs_referencia()
    tol = FICHAS_TOL["RISK-VAR-001"]
    return (_cerca(d["sigma_siguiente"], sig, 1e-10) and _cerca(r["var"], var, 1e-10) and _cerca(r["es"], es, 1e-10)
            and r["es"] >= r["var"] and 0 < g["alpha"] + g["beta"] < 1
            and _cerca(g["omega"], float(np.var(x - x.mean())) * (1 - g["alpha"] - g["beta"]), 1e-12)
            and math.isclose(r["var"], var_ref, rel_tol=tol) and math.isclose(r["es"], es_ref, rel_tol=tol))


def _cuantil_mc(r: dict[str, Any], v0: float, mu: float, sigma: float, h: int, n: int) -> bool:
    """Cuantiles simulados de V0·e^X, X ~ N(hμ, σ²h), dentro de 4 EE del cuantil analítico."""
    sd = sigma * math.sqrt(h)
    for q, val in r["distribucion"]["cuantiles"].items():
        zq = float(stats.norm.ppf(float(q)))
        an = v0 * math.exp(h * mu + sd * zq)
        ee = math.sqrt(float(q) * (1 - float(q)) / n) / float(stats.norm.pdf(zq)) * sd * an
        if abs(val - an) > _EE_MC * ee:
            return False
    return True


def _caso_mc_paseo(r: dict[str, Any]) -> bool:
    lg = r["log_rendimiento"]
    return (math.isclose(lg["media"], 10 * 0.0008, rel_tol=1e-9) and _cuantil_mc(r, 100.0, 0.0008, 0.015, 10, 20_000)
            and r["reduccion_varianza"] == "antiteticas")


def _caso_mc_saltos(r: dict[str, Any]) -> bool:
    h, n, mu, s, lam, mj, sj = 20, 20_000, 0.0002, 0.01, 0.5, -0.03, 0.02
    m, var = h * (mu + lam * mj), h * (s * s + lam * (sj * sj + mj * mj))
    lg = r["log_rendimiento"]
    ee_var = var * math.sqrt((lg["curtosis"] - 1) / n)
    return abs(lg["media"] - m) <= _EE_MC * math.sqrt(var / n) and abs(lg["varianza"] - var) <= _EE_MC * ee_var


def _caso_mc_garch(r: dict[str, Any]) -> bool:
    om, al, be, s2, h, n = 2e-6, 0.08, 0.9, 4e-4, 15, 20_000
    esperadas = [s2]
    for _ in range(h - 1):
        esperadas.append(om + (al + be) * esperadas[-1])
    var = sum(esperadas)
    lg = r["log_rendimiento"]
    ee_var = var * math.sqrt((lg["curtosis"] - 1) / n)
    return (abs(lg["varianza"] - var) <= _EE_MC * ee_var and math.isclose(lg["media"], 0.0, abs_tol=1e-15)
            and _cerca(r["solucion_analitica"]["varianza_log"], var, 1e-12))


def _caso_mc_garch_curtosis(r: dict[str, Any]) -> bool:
    """X₂ = ε₁ + ε₂ con σ²₁ fijo: E[X₂⁴] = 3σ₁⁴ + 6σ²₁(c + 3ασ²₁) + 3(c² + 2cασ²₁ + 3α²σ₁⁴), c = ω + βσ²₁."""
    om, al, be, s2 = 2e-6, 0.08, 0.9, 4e-4
    c = om + be * s2
    m4 = 3 * s2 * s2 + 6 * s2 * (c + 3 * al * s2) + 3 * (c * c + 2 * c * al * s2 + 3 * al * al * s2 * s2)
    var = s2 + c + al * s2
    k = r["log_rendimiento"]["curtosis"]
    return k is not None and abs(k - m4 / var ** 2) <= _TOL_CURTOSIS * m4 / var ** 2


def _caso_mc_convergencia(r: dict[str, Any]) -> bool:
    c = r["distribucion"]["convergencia"]
    return ([x["n"] for x in c] == [20_000, 10_000, 5_000, 2_500]
            and c[0]["media"] == r["distribucion"]["media"] and c[0]["cuantiles"] == r["distribucion"]["cuantiles"])


def _datos_scn(semilla: int = 11203) -> dict[str, Any]:
    rng = np.random.default_rng(semilla)
    return {"rendimientos": [float(e) for e in 0.0003 + 0.01 * rng.standard_normal(600)],
            "regimen": {"fuente": "REG-HMM-001 sintética de control", "probabilidades_filtradas": {"alcista": 0.7, "bajista": 0.3},
                        "estados": {"alcista": {"media": 0.0004, "volatilidad": 0.009},
                                    "bajista": {"media": -0.0006, "volatilidad": 0.016}}},
            "valoracion": {"fuente": "MC-09 sintética de control", "ajuste": -0.02},
            "bloques": {"fuente": "bloques sintéticos de control",
                        "rendimiento_corriente": {"valor": 0.02, "incertidumbre": 0.01},
                        "crecimiento": {"valor": 0.04, "incertidumbre": 0.05},
                        "cambio_valoracion": {"valor": -0.01, "incertidumbre": 0.15}}}


def _caso_scn_coherencia(r: dict[str, Any]) -> bool:
    hs = r["horizontes"]
    ok = list(hs) == ["H1", "H2", "H3", "H4"] and r["verificacion"] == {"cuantiles_monotonos": True, "bandas_crecientes": True}
    for h in hs.values():
        q = list(h["cuantiles"].values())
        e = h["escenarios"]
        ok = ok and q[0] < q[1] < q[2] and e["adverso"] < e["base"] < e["favorable"] and e["base"] == q[1]
    anchos = [hs[h]["amplitud_banda"] for h in ("H1", "H2", "H3", "H4")]
    return ok and anchos[0] < anchos[1] < anchos[2] < anchos[3]


def _caso_scn_h4(r: dict[str, Any]) -> bool:
    h4 = r["horizontes"]["H4"]
    q = h4["cuantiles"]
    suma, sd = 0.05, math.sqrt(0.01 ** 2 + 0.05 ** 2 + 0.15 ** 2)
    ee = math.sqrt(0.9 * 0.1 / 20_000) / float(stats.norm.pdf(stats.norm.ppf(0.9))) * sd * PCT
    return (h4["anios"] == 1.0 and math.isclose(q["0.5"], suma * PCT, rel_tol=1e-12)
            and math.isclose(q["0.1"] + q["0.9"], 2 * suma * PCT, rel_tol=1e-12)
            and abs(q["0.9"] - (suma + float(stats.norm.ppf(0.9)) * sd) * PCT) <= _EE_MC * ee)


def _caso_scn_h3(r: dict[str, Any]) -> bool:
    h3 = r["horizontes"]["H3"]
    # Las trayectorias antitéticas son simétricas en log alrededor de 126·μ; la mediana muestral (media de los dos
    # centrales tras la transformación convexa) se separa de la analítica menos que la tolerancia de la ficha.
    esperado = math.expm1(126 * 0.0005 + math.log1p(0.03)) * PCT
    return h3["pasos_sesiones"] == 126 and math.isclose(h3["cuantiles"]["0.5"], esperado, rel_tol=FICHAS_TOL["SCN-H-001"])


def _dsr_datos() -> tuple[list[float], float]:
    x = _normal_cuantiles(0.0006, 0.01, 1000)
    a = np.array(x)
    return x, float(a.mean() / a.std(ddof=1) * math.sqrt(SESIONES_ANIO))


_DSR_X, _DSR_SR_ANUAL = _dsr_datos()
_DSR_COLAS = [x + 0.0008 for x in _colas_gruesas(756, 11204)]


def _caso_dsr_normal(r: dict[str, Any]) -> bool:
    a = np.array(_DSR_X)
    sr = a.mean() / a.std(ddof=1)
    g4 = stats.kurtosis(a, fisher=False, bias=False)
    psr = stats.norm.cdf(sr * math.sqrt(len(a) - 1) / math.sqrt(1 + (g4 - 1) / 4 * sr * sr))
    return (_cerca(r["sr_periodo"], sr, 1e-12) and abs(r["asimetria"]) < 1e-9 and _cerca(r["psr"], psr, 1e-10)
            and r["dsr"] == r["psr"] and r["sr0_periodo"] == 0)


def _caso_dsr_deflactado(r: dict[str, Any]) -> bool:
    a = np.array(_DSR_COLAS)
    T, sr = len(a), a.mean() / a.std(ddof=1)
    g3, g4 = stats.skew(a, bias=False), stats.kurtosis(a, fisher=False, bias=False)
    ee = math.sqrt((1 - g3 * sr + (g4 - 1) / 4 * sr * sr) / (T - 1))
    v = 0.5 / SESIONES_ANIO
    g = float(np.euler_gamma)
    sr0 = math.sqrt(v) * ((1 - g) * stats.norm.ppf(1 - 1 / 50) + g * stats.norm.ppf(1 - 1 / (50 * math.e)))
    trl = 1 + (1 - g3 * sr + (g4 - 1) / 4 * sr * sr) * (stats.norm.ppf(0.95) / sr) ** 2
    return (_cerca(r["sr0_periodo"], sr0, 1e-12) and _cerca(r["dsr"], stats.norm.cdf((sr - sr0) / ee), 1e-10)
            and _cerca(r["ee_periodo"], ee, 1e-12) and _cerca(r["min_trl_periodos"], trl, 1e-10) and r["dsr"] < r["psr"])


def _pbo_ruido(N: int, T: int, semilla: int) -> dict[str, list[float]]:
    rng = np.random.default_rng(semilla)
    return {f"c{i:02d}": [float(e) for e in 0.01 * rng.standard_normal(T)] for i in range(N)}


def _pbo_dominante() -> dict[str, list[float]]:
    m = _pbo_ruido(10, 640, 11205)
    m["c00"] = [e + 0.02 for e in m["c00"]]
    return m


def _pbo_permutaciones() -> dict[str, list[float]]:
    """Cada configuración es una permutación por bloques de la misma serie: mismo Sharpe en la muestra completa, así que
    lo que gana dentro de muestra lo pierde fuera (sobreajuste puro)."""
    base = np.array(_pbo_ruido(1, 640, 11206)["c00"]).reshape(16, 40)
    rng = np.random.default_rng(11207)
    return {f"p{i:02d}": [float(e) for e in base[rng.permutation(16)].ravel()] for i in range(10)}


_PBO_IDENTICAS = {f"c{i}": _pbo_ruido(1, 640, 11208)["c00"] for i in range(4)}


def _var_espaciado(posiciones: list[int], T: int, var: float) -> dict[str, Any]:
    res = [0.001 * math.sin(i) for i in range(T)]
    for i in posiciones:
        res[i] = -var - 0.005
    return {"var_previsto": [var] * T, "resultados": res}


def _lr_uc_mano(x: int, T: int, p: float) -> float:
    f = x / T
    return -2 * ((T - x) * math.log(1 - p) + x * math.log(p)) + 2 * ((T - x) * math.log(1 - f) + x * math.log(f))


def _lr_ind_agrupadas(r: dict[str, Any]) -> bool:
    n00, n01, n10, n11 = 243, 1, 1, 4                   # 249 transiciones con 5 excedencias seguidas
    pi = (n01 + n11) / (n00 + n01 + n10 + n11)
    p01, p11 = n01 / (n00 + n01), n11 / (n10 + n11)
    l0 = (n00 + n10) * math.log(1 - pi) + (n01 + n11) * math.log(pi)
    l1 = n00 * math.log(1 - p01) + n01 * math.log(p01) + n10 * math.log(1 - p11) + n11 * math.log(p11)
    return (r["transiciones"] == {"n00": n00, "n01": n01, "n10": n10, "n11": n11}
            and _cerca(r["lr_ind"], -2 * (l0 - l1), 1e-10) and r["rechazo"]["ind"] and not r["rechazo"]["uc"])


def _z2_cero() -> dict[str, Any]:
    T, es = 400, 0.03
    res = [0.0005 * math.cos(i) for i in range(T)]
    for i in range(10):
        res[17 + 38 * i] = -es
    return {"var_previsto": [0.02] * T, "es_previsto": [es] * T, "resultados": res}


def _cal_nivel() -> dict[str, Any]:
    y = [0.1 * i + math.sin(i) for i in range(40)]
    e = [(0.5 if i % 2 else -0.5) + (0.2 if i % 3 == 0 else 0.0) for i in range(40)]
    return {"tipo": "nivel", "realizaciones": y, "predicciones": [a - b for a, b in zip(y, e)],
            "referencia": [a - 1.0 for a in y],
            "intervalos": {"inferior": [a - b - 0.6 for a, b in zip(y, e)], "superior": [a - b + 0.6 for a, b in zip(y, e)],
                           "nivel": 0.9}}


def _caso_cal_nivel(r: dict[str, Any]) -> bool:
    d = _cal_nivel()
    y, p = d["realizaciones"], d["predicciones"]
    e = [a - b for a, b in zip(y, p)]
    mae = sum(abs(x) for x in e) / 40
    rmse = math.sqrt(sum(x * x for x in e) / 40)
    esc = sum(abs(y[i] - y[i - 1]) for i in range(1, 40)) / 39
    m = r["horizontes"]["H2"]
    cob = sum(1 for x in e if abs(x) <= 0.6) / 40
    return (_cerca(m["mae"], mae, 1e-12) and _cerca(m["rmse"], rmse, 1e-12) and _cerca(m["sesgo"], sum(e) / 40, 1e-12)
            and _cerca(m["mase"], mae / esc, 1e-12) and _cerca(m["comparacion_referencia"]["r2_oos"], 1 - rmse ** 2 * 40 / 40, 1e-12)
            and m["cobertura_intervalos"]["cobertura"] == cob and m["verificacion"]["metricas_recomputadas"])


def _cal_prob() -> dict[str, Any]:
    p = [0.15 + 0.7 * ((i * 7) % 10) / 9 for i in range(50)]
    o = [1 if ((i * 7) % 10) >= 4 + (i % 3 == 0) else 0 for i in range(50)]
    return {"tipo": "probabilidad", "predicciones": p, "realizaciones": o, "referencia": [0.5] * 50,
            "particiones": [{"entrenamiento": [0, 9], "prueba": [12, 29]}, {"entrenamiento": [0, 27], "prueba": [30, 49]}],
            "embargo": 2, "regimenes": ["calma"] * 25 + ["tension"] * 25}


def _caso_cal_prob(r: dict[str, Any]) -> bool:
    d = _cal_prob()
    p, o = d["predicciones"], d["realizaciones"]
    brier = sum((a - b) ** 2 for a, b in zip(p, o)) / 50
    ls = -sum(b * math.log(a) + (1 - b) * math.log(1 - a) for a, b in zip(p, o)) / 50
    m = r["horizontes"]["H3"]
    reg = m["por_regimen"]["tension"]
    brier_t = sum((a - b) ** 2 for a, b in zip(p[25:], o[25:])) / 25
    return (_cerca(m["brier"], brier, 1e-12) and _cerca(m["log_score"], ls, 1e-12)
            and _cerca(m["comparacion_referencia"]["bss"], 1 - brier / 0.25, 1e-12) and m["particiones_sin_solape"] is True
            and _cerca(reg["brier"], brier_t, 1e-12) and reg["n"] == 25)


def _cal_cuantil() -> dict[str, Any]:
    y = [math.sin(i * 0.7) for i in range(36)]
    return {"tipo": "cuantil", "cuantil": 0.9, "realizaciones": y, "predicciones": [0.8] * 36, "referencia": [0.8] * 36}


def _caso_cal_cuantil(r: dict[str, Any]) -> bool:
    y = _cal_cuantil()["realizaciones"]
    pin = sum(max(0.9 * (a - 0.8), -0.1 * (a - 0.8)) for a in y) / 36
    m = r["horizontes"]["H1"]
    mj = m["mejora_frente_referencia"]
    return (_cerca(m["pinball"], pin, 1e-12) and m["cobertura_cuantil"] == sum(1 for a in y if a <= 0.8) / 36
            and mj["mejora_media"] == 0 and mj["ic"] == [0.0, 0.0] and mj["conclusion"] == "sin mejora demostrada")


def _pred_datos(con_senal: bool, semilla: int, n: int = 420) -> dict[str, Any]:
    rng = np.random.default_rng(semilla)
    fechas = [str(d.date()) for d in pd.bdate_range("2019-01-01", periods=n)]
    x = rng.standard_normal(n)
    mov = (0.01 * np.r_[0.0, x[:-1]] if con_senal else 0.0) + 0.005 * rng.standard_normal(n)
    serie = 100 * np.exp(np.cumsum(mov))
    return {"fechas": fechas, "objetivo": {"serie": [float(e) for e in serie], "horizonte": 1, "tipo": "direccion",
                                           "criterio_resolucion": "cierre de la sesión siguiente por encima del actual"},
            "variables": {"x": {"serie": [float(e) for e in x], "conocible_desde": fechas},
                          "ruido": {"serie": [float(e) for e in rng.standard_normal(n)], "conocible_desde": fechas}}}


def _caso_pred_particiones(r: dict[str, Any]) -> bool:
    e = r["embargo"]
    pa = r["particiones"]
    disj = all(a["prueba"][1] < b["prueba"][0] for a, b in itertools.pairwise(pa))
    return (r["verificacion"]["particiones_sin_solape"] and disj and len(pa) == 5
            and all(x["entrenamiento"][1] + e <= x["prueba"][0] and x["entrenamiento"][0] == 0 for x in pa)
            and [x["indice"] for x in r["predicciones_oos"]] == list(range(pa[0]["prueba"][0], pa[-1]["prueba"][1] + 1)))


def _caso_pred_metricas(r: dict[str, Any]) -> bool:
    """Brier y acierto desde las predicciones fuera de muestra, y BSS frente a RI-TB rehecha con las etiquetas conocidas
    en t (i ≤ t − embargo) a partir de la serie del objetivo."""
    po = r["predicciones_oos"]
    brier = sum((x["prediccion"] - x["realizacion"]) ** 2 for x in po) / len(po)
    acierto = sum(1 for x in po if (x["prediccion"] >= 0.5) == (x["realizacion"] == 1)) / len(po)
    serie = _PRED_SENAL["objetivo"]["serie"]
    y = [1.0 if b > a else 0.0 for a, b in itertools.pairwise(serie)]
    e = r["embargo"]
    ref = [sum(y[:x["indice"] - e + 1]) / (x["indice"] - e + 1) for x in po]
    brier_ref = sum((a - x["realizacion"]) ** 2 for a, x in zip(ref, po)) / len(po)
    return (_cerca(r["metricas_oos"]["brier"], brier, 1e-12) and _cerca(r["metricas_oos"]["acierto"], acierto, 1e-12)
            and r["metricas_oos"]["n"] == len(po) and all(x["realizacion"] == y[x["indice"]] for x in po)
            and _cerca(r["metricas_oos"]["bss"], 1 - brier / brier_ref, 1e-10)
            and _cerca(r["mejora_frente_referencia"]["mejora_media"], brier_ref - brier, 1e-10))


_PRED_SENAL = _pred_datos(True, 11210)

_VOI_U = {"puntuacion": {"dimension": "E", "actual": 58.0},
          "rango_plausible": {"inferior": 52.0, "superior": 66.0, "fuente": "sensibilidad de la ficha prevista"}}
_VOI_M = {"puntuacion": {"dimension": "A", "actual": 54.0},
          "muestras": {"valores": [48.0, 50.5, 52.0, 53.0, 54.5, 55.5, 57.0, 58.0, 60.0, 61.5], "fuente": "RC sintético"}}


def _caso_voi_perfecta(r: dict[str, Any]) -> bool:
    d = r["decisiones"][0]
    evpi_mano = (66 - 60) ** 2 / (2 * (66 - 52)) - max(59 - 60, 0)
    return (d["umbral"] == 60 and _cerca(d["evpi"], evpi_mano, 1e-12) and d["evsi"] == d["evpi"]
            and r["voi_puntos"] == d["evpi"] and r["medida"] == "EVSI" and _cerca(d["probabilidad_cambio"], 6 / 14, 1e-12))


def _caso_voi_ruido(r: dict[str, Any]) -> bool:
    d = r["decisiones"][0]
    return 0 < d["evsi"] < d["evpi"] and r["voi_puntos"] == d["evsi"] and r["recomendacion_tecnica"] == "EJECUTAR"


def _caso_voi_empirica(r: dict[str, Any]) -> bool:
    s = np.array([48.0, 50.5, 52.0, 53.0, 54.5, 55.5, 57.0, 58.0, 60.0, 61.5])   # las muestras de `_VOI_M`
    evpi_mano = float(np.mean(np.maximum(s - 55, 0)) - max(s.mean() - 55, 0))
    d = r["decisiones"][0]
    return _cerca(d["evpi"], evpi_mano, 1e-12) and abs(d["evsi"] - d["evpi"]) <= 1e-6 and d["evsi"] <= d["evpi"]


CASOS_CONTROL: dict[str, list[dict[str, Any]]] = {
    "RISK-VAR-001": [
        {"nombre": "histórico en rejilla exacta: VaR = −x₍₂₅₎·√4 = 0,095 y ES = −media(x₍₀₎…x₍₂₅₎)·√4 = 0,0975 ≥ VaR",
         "datos": [{"valores": {"rendimientos": _R_VAR_REJ}}], "parametros": {"horizonte": 4},
         "comprobar": lambda r: _cerca(r["var"], 0.0475 * 2, 1e-12) and _cerca(r["es"], 0.04875 * 2, 1e-12) and r["es"] >= r["var"]
         and r["verificacion"]["cuantiles_monotonos"]},
        {"nombre": "normal: VaR = −(μ + σ·Φ⁻¹(1 − nivel)), ES = −μ + σ·φ(Φ⁻¹(nivel))/(1 − nivel), con μ y σ muestrales exactos",
         "datos": [{"valores": {"rendimientos": _R_VAR_NORMAL}}], "parametros": {"metodo": "normal"},
         "comprobar": lambda r: _cerca(r["var"], -(0.0004 + 0.012 * float(stats.norm.ppf(0.025))), 1e-10)
         and _cerca(r["es"], -0.0004 + 0.012 * float(stats.norm.pdf(stats.norm.ppf(0.975))) / 0.025, 1e-10)},
        {"nombre": "t por momentos: VaR y ES de la t de Student con ν = 4 + 6/curtosis en exceso; ES ≥ VaR",
         "datos": [{"valores": {"rendimientos": _R_VAR_COLAS}}], "parametros": {"metodo": "t"}, "comprobar": _caso_t},
        {"nombre": "Cornish-Fisher: z_cf con asimetría y curtosis; ES > VaR y cuantiles monótonos 0,90 → 0,975 → 0,99",
         "datos": [{"valores": {"rendimientos": _R_VAR_COLAS}}], "parametros": {"metodo": "cornish_fisher"},
         "comprobar": _caso_cf},
        {"nombre": "EVT-POT: VaR = u + β/ξ·[((n/Nᵤ)(1 − nivel))^(−ξ) − 1], ES = (VaR + β − ξu)/(1 − ξ) ≥ VaR",
         "datos": [{"valores": {"rendimientos": _R_VAR_COLAS}}], "parametros": {"metodo": "evt_pot"},
         "comprobar": _caso_evt},
        {"nombre": ("histórico filtrado: VaR = −(μ + σ_T+1·q(z)) y ES = −(μ + σ_T+1·media(z ≤ q)) con los residuos GARCH, "
                    "ω = σ̄²(1 − α − β) y el VaR del óptimo de referencia (1e-6)"),
         "datos": [{"valores": {"rendimientos": _R_VAR_GARCH}}], "parametros": {"metodo": "historico_filtrado"},
         "comprobar": _caso_fhs},
        {"nombre": "segunda vía: en una muestra normal por cuantiles exactos, histórico y paramétrico coinciden (≤ 1 %)",
         "datos": [{"valores": {"rendimientos": _R_VAR_CUANT}}], "parametros": {},
         "comprobar": lambda r: r["segunda_via"]["metodo"] == "normal"
         and abs(r["segunda_via"]["diferencia_var"]) <= _TOL_VIA * r["var"] and r["var"] > 0},
    ],
    "SIM-MC-001": [
        {"nombre": "paseo aleatorio con antitéticas: media del log-rendimiento = h·μ exacta y cuantiles analíticos (4 EE)",
         "datos": [{"valores": {"dinamica": {"tipo": "paseo_aleatorio", "mu": 0.0008, "sigma": 0.015, "valor_inicial": 100.0}}}],
         "parametros": {"n_trayectorias": 20_000, "horizonte": 10, "semilla": 112}, "comprobar": _caso_mc_paseo},
        {"nombre": "saltos de Merton: media h(μ + λm_J) y varianza h(σ² + λ(s_J² + m_J²)) del log-rendimiento (4 EE)",
         "datos": [{"valores": {"dinamica": {"tipo": "saltos", "mu": 0.0002, "sigma": 0.01, "intensidad": 0.5,
                                             "media_salto": -0.03, "desv_salto": 0.02}}}],
         "parametros": {"n_trayectorias": 20_000, "horizonte": 20, "semilla": 113}, "comprobar": _caso_mc_saltos},
        {"nombre": "GARCH(1,1): varianza del log-rendimiento = Σ E[σ²ₜ] con reversión a ω/(1 − α − β) (4 EE)",
         "datos": [{"valores": {"dinamica": {"tipo": "garch", "mu": 0.0, "omega": 2e-6, "alpha": 0.08, "beta": 0.9,
                                             "sigma2_inicial": 4e-4}}}],
         "parametros": {"n_trayectorias": 20_000, "horizonte": 15, "semilla": 114}, "comprobar": _caso_mc_garch},
        {"nombre": "GARCH(1,1) a dos pasos: curtosis del log-rendimiento analítica (separa α de β)",
         "datos": [{"valores": {"dinamica": {"tipo": "garch", "mu": 0.0, "omega": 2e-6, "alpha": 0.08, "beta": 0.9,
                                             "sigma2_inicial": 4e-4}}}],
         "parametros": {"n_trayectorias": 40_000, "horizonte": 2, "semilla": 119}, "comprobar": _caso_mc_garch_curtosis},
        {"nombre": "tabla de convergencia por mitades (n, n/2, n/4, n/8) coherente con la distribución completa",
         "datos": [{"valores": {"dinamica": {"tipo": "paseo_aleatorio", "mu": 0.0, "sigma": 0.02}}}],
         "parametros": {"n_trayectorias": 20_000, "horizonte": 5, "semilla": 115}, "comprobar": _caso_mc_convergencia},
    ],
    "SCN-H-001": [
        {"nombre": "cuantiles monótonos, adverso < base < favorable y bandas crecientes H1 → H2 → H3 → H4",
         "datos": [{"valores": _datos_scn()}], "parametros": {"semilla": 116, "clase": "RV", "umbrales": [0.0]},
         "comprobar": _caso_scn_coherencia},
        {"nombre": "H4 por bloques: mediana = Σ valores, q10 + q90 = 2·mediana y q90 = Σv + z₀,₉·√Σu² (4 EE)",
         "datos": [{"valores": {"bloques": _datos_scn()["bloques"]}}],
         "parametros": {"semilla": 117, "clase": "RV", "horizontes": ["H4"], "n_trayectorias": 20_000},
         "comprobar": _caso_scn_h4},
        {"nombre": "H3 con un régimen: mediana = e^(126·μ + ln(1 + ajuste de valoración)) − 1",
         "datos": [{"valores": {"regimen": {"fuente": "REG-HMM-001 sintética", "probabilidades_filtradas": {"unico": 1.0},
                                            "estados": {"unico": {"media": 0.0005, "volatilidad": 0.01}}},
                                "valoracion": {"fuente": "MC-09 sintética", "ajuste": 0.03}}}],
         "parametros": {"semilla": 118, "clase": "RV", "horizontes": ["H3"]}, "comprobar": _caso_scn_h3},
    ],
    "BT-DSR-001": [
        {"nombre": "PSR(SR) = 0,5 (referencia igual al Sharpe observado)",
         "datos": [{"valores": {"rendimientos": _DSR_X, "varianza_sr_ensayos": {"valor": 0.5, "unidad": "anual"}}}],
         "parametros": {"N": 10, "SR_referencia": _DSR_SR_ANUAL},
         "comprobar": lambda r: _cerca(r["psr"], 0.5, 1e-12) and r["min_trl_periodos"] is None},
        {"nombre": "caso normal con SR conocido: asimetría 0 y PSR = Φ(SR·√(T − 1)/√(1 + (γ₄ − 1)/4·SR²)); N = 1 ⇒ DSR = PSR",
         "datos": [{"valores": {"rendimientos": _DSR_X, "varianza_sr_ensayos": {"valor": 0.5, "unidad": "anual"}}}],
         "parametros": {"N": 1}, "comprobar": _caso_dsr_normal},
        {"nombre": "SR*₀ esperado del máximo de N = 50 ensayos, DSR = PSR(SR*₀) < PSR(0) y MinTRL con asimetría y curtosis",
         "datos": [{"valores": {"rendimientos": _DSR_COLAS, "varianza_sr_ensayos": {"valor": 0.5, "unidad": "anual"}}}],
         "parametros": {"N": 50}, "comprobar": _caso_dsr_deflactado},
    ],
    "BT-PBO-001": [
        {"nombre": "configuraciones idénticas ⇒ PBO indefinido declarado",
         "datos": [{"valores": {"rendimientos": _PBO_IDENTICAS}}], "parametros": {},
         "comprobar": lambda r: r["pbo"] is None and r["indefinido"] is True},
        {"nombre": "sin habilidad (ruido iid) ⇒ PBO ≈ 0,5 (±0,3, dos desviaciones entre conjuntos)",
         "datos": [{"valores": {"rendimientos": _pbo_ruido(10, 640, 11209)}}], "parametros": {},
         "comprobar": lambda r: abs(r["pbo"] - 0.5) <= 0.3 and r["combinaciones"] == math.comb(16, 8)},
        {"nombre": "configuración dominante ⇒ PBO = 0 y probabilidad de pérdida fuera de muestra 0",
         "datos": [{"valores": {"rendimientos": _pbo_dominante()}}], "parametros": {},
         "comprobar": lambda r: r["pbo"] == 0 and r["probabilidad_perdida"] == 0 and r["frecuencia_mejor"]["c00"] == 1
         and r["lambda"]["minimo"] == math.log(10 / 11 / (1 - 10 / 11))},
        {"nombre": "permutaciones por bloques de una misma serie (sobreajuste puro) ⇒ PBO ≥ 0,5 y pendiente negativa",
         "datos": [{"valores": {"rendimientos": _pbo_permutaciones()}}], "parametros": {},
         "comprobar": lambda r: r["pbo"] >= 0.5 and r["diagnostico"] == "sobreajuste_probable"
         and r["pendiente_degradacion"] < 0},
    ],
    "BT-VAR-001": [
        {"nombre": "250 observaciones, 99 %, 5 excedencias ⇒ LR_uc ≈ 1,96 (zona amarilla)",
         "datos": [{"valores": _var_espaciado([20, 70, 120, 170, 220], 250, 0.02)}], "parametros": {"nivel": 0.99},
         "comprobar": lambda r: r["excedencias"]["n"] == 5 and abs(r["lr_uc"] - 1.96) < 0.005
         and _cerca(r["lr_uc"], _lr_uc_mano(5, 250, 0.01), 1e-10) and r["zona_semaforo"] == "amarilla"},
        {"nombre": "excedencias agrupadas ⇒ LR_ind de Christoffersen con sus transiciones (independencia rechazada)",
         "datos": [{"valores": _var_espaciado([100, 101, 102, 103, 104], 250, 0.02)}], "parametros": {"nivel": 0.99},
         "comprobar": _lr_ind_agrupadas},
        {"nombre": "frecuencia = 1 − nivel y pérdida en la cola = ES ⇒ Z₂ = 0 y LR_uc = 0",
         "datos": [{"valores": _z2_cero()}], "parametros": {},
         "comprobar": lambda r: math.isclose(r["z2"], 0.0, abs_tol=1e-12) and math.isclose(r["lr_uc"], 0.0, abs_tol=1e-9)
         and r["excedencias"]["n"] == 10},
    ],
    "ML-CAL-001": [
        {"nombre": "nivel: MAE, RMSE, sesgo, MASE, R²_OOS y cobertura recomputados a mano",
         "datos": [{"valores": {"ensayos": 4, "horizontes": {"H2": _cal_nivel()}}}], "parametros": {},
         "comprobar": _caso_cal_nivel},
        {"nombre": "probabilidad: Brier, log-score, BSS, por régimen y particiones sin solape",
         "datos": [{"valores": {"ensayos": 4, "horizontes": {"H3": _cal_prob()}}}], "parametros": {},
         "comprobar": _caso_cal_prob},
        {"nombre": "cuantil: pinball y cobertura; modelo = referencia ⇒ mejora 0, IC [0, 0], sin mejora demostrada",
         "datos": [{"valores": {"ensayos": 1, "horizontes": {"H1": _cal_cuantil()}}}], "parametros": {},
         "comprobar": _caso_cal_cuantil},
    ],
    "ML-PRED-001": [
        {"nombre": "particiones walk-forward sin solape con purga y embargo (entrenamiento ≤ inicio − embargo)",
         "datos": [{"valores": _pred_datos(True, 11210)}], "parametros": {"embargo": 2}, "comprobar": _caso_pred_particiones},
        {"nombre": "métricas fuera de muestra recomputadas desde las predicciones",
         "datos": [{"valores": _PRED_SENAL}], "parametros": {}, "comprobar": _caso_pred_metricas},
        {"nombre": "señal conocible ⇒ mejora frente a RI-TB con IC > 0",
         "datos": [{"valores": _pred_datos(True, 11210)}], "parametros": {},
         "comprobar": lambda r: r["mejora_frente_referencia"]["conclusion"] == "mejora demostrada"
         and r["mejora_frente_referencia"]["ic"][0] > 0 and r["metricas_oos"]["bss"] > 0},
        {"nombre": "sin señal ⇒ «sin mejora demostrada»",
         "datos": [{"valores": _pred_datos(False, 11211)}], "parametros": {},
         "comprobar": lambda r: r["mejora_frente_referencia"]["conclusion"] == "sin mejora demostrada"},
    ],
    "DEC-VOI-001": [
        {"nombre": "información perfecta ⇒ VOI = EVPI = (hi − u)²/(2(hi − lo)) − máx(E[S] − u, 0)",
         "datos": [{"valores": {**_VOI_U, "verosimilitud": {"desviacion": 0.0}}}], "parametros": {"coste_uc": 0.5},
         "comprobar": _caso_voi_perfecta},
        {"nombre": "señal ruidosa ⇒ EVPI > EVSI > 0",
         "datos": [{"valores": {**_VOI_U, "verosimilitud": {"desviacion": 3.0}}}], "parametros": {"coste_uc": 0.5},
         "comprobar": _caso_voi_ruido},
        {"nombre": "regla simple: rango que no alcanza ningún umbral ±5 ni el orden del top-3 ⇒ VOI = 0, NO_EJECUTAR",
         "datos": [{"valores": {"puntuacion": {"dimension": "A", "actual": 75.0},
                                "rango_plausible": {"inferior": 70.0, "superior": 80.0, "fuente": "sensibilidad"},
                                "ranking": {"rk_opcion": 72.0, "rk_frontera": 60.0, "amplitud_rk": 5.0}}}],
         "parametros": {"coste_uc": 0.5},
         "comprobar": lambda r: r["voi_puntos"] == 0 and r["regla_simple_voi_cero"] and r["recomendacion_tecnica"] == "NO_EJECUTAR"},
        {"nombre": "muestras del Registro: EVPI = media(máx(s − u, 0)) − máx(media − u, 0) y EVSI → EVPI con σ → 0",
         "datos": [{"valores": {**_VOI_M, "verosimilitud": {"desviacion": 1e-3}}}], "parametros": {"coste_uc": 0.5},
         "comprobar": _caso_voi_empirica},
    ],
}
