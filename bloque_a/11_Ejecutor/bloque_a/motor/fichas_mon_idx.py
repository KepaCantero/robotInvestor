"""Fichas V5.0 del Motor: instrumentos monetarios (MON, sección 18) e índices bursátiles (IDX, sección 15).

T-106 (Motor Fase 1). Fuente de verdad: «Catálogo de cálculos del Motor - V5.0», fichas MON-YLD-001, MON-EXP-001,
MON-REAL-001, MON-FIX-001, IDX-ERP-001, IDX-CONC-001, IDX-REL-001 e IDX-REB-001, y su sección 3 (convenciones).

Convenciones comunes de este módulo:

- Todas las entradas llegan en línea en ``ent["valores"]`` (curvas, tipos, pesos e historias como listas de dicts
  con ``fecha``). IDX-CONC-001 acepta además series de precios en ``ent["series"]`` (alias = id del componente) y los
  roles ``indice_ponderado`` e ``indice_equiponderado`` en ``ent["series_rol"]``.
- Tipos, rentabilidades y diferenciales en **tanto por uno** (0,03 = 3 %; una diferencia de 0,01 = 1 pp). Solo las
  claves con sufijo ``_pb`` van en puntos básicos, porque la ficha las pide en pb.
- Recuento de días Real/365 (3.1) salvo convención de mercado monetario declarada (Act/360 o Act/365).
- Percentil histórico = proporción de la historia ≤ valor (la misma posición que ``operaciones.posicion_historica``);
  z-score con desviación muestral; si la dispersión es nula el z queda ``None`` (indefinido) y se declara.
- Falla cerrado: lo que falta o es incoherente lanza ``ErrorFicha`` con el motivo; un bloque opcional del método sin
  datos se omite (``None``) y se declara en las limitaciones, nunca se rellena con 0.
- Determinista: sin aleatoriedad; los diccionarios se recorren en orden de claves.
"""
from __future__ import annotations

import datetime as dt
import math
from collections.abc import Callable
from decimal import Decimal
from functools import wraps
from itertools import pairwise
from typing import Any

import numpy as np
import pandas as pd
from scipy import optimize, stats

from .operaciones import ErrorFicha, cagr

# Constantes de convención (parte del método, no parámetros): unidades y bases de recuento.
PB = 10_000                # pb por unidad (tanto por uno)
DIAS_ANIO = 365            # Real/365 y anualización TAE (3.1; MON-YLD-001 (i))
BASE_360 = 360             # convención Act/360 del mercado monetario (MON-YLD-001 (i))
MESES_ANIO = 12
ANIOS_DECADA = 10          # «pp por década» (IDX-REB-001, Salidas)
PRECIO_PAR_FUTURO = 100    # «tipo = 100 − precio» (MON-EXP-001 (i))

# Valores por defecto y rangos, tal como los da el campo «Parámetros» (o el «Método») de cada ficha del Catálogo V5.0.
PARAMETROS_POR_DEFECTO: dict[str, dict[str, Any]] = {
    # MON-YLD-001 · Parámetros: base_salida (TAE; Act/365); plazos (1, 3, 6, 12 meses); cobertura (false).
    # Método (iv): percentil frente a ≥ 5 años.
    "MON-YLD-001": {"base_salida": "TAE", "plazos_meses": [1, 3, 6, 12], "cobertura": False,
                    "anios_percentil_min": 5},
    # MON-EXP-001 · Parámetros: incremento (25 pb); diferencial_estable (media de 20 días); convexidad (true para
    # > 1 año). Método (iv): cambio acumulado a 6 y 12 meses. Rechazo: < 3 nodos en 12 meses.
    "MON-EXP-001": {"incremento_pb": 25, "diferencial_estable_dias": 20, "convexidad": True, "anios_convexidad": 1,
                    "meses_cambio_acumulado": [6, 12], "nodos_min": 3, "meses_nodos": 12},
    # MON-REAL-001 · Parámetros: medida_inflacion (IPC armonizado o índice de referencia); expectativa (swap_1a;
    # encuesta); plazo (3 meses). Entradas: ≥ 10 años (≥ 20 recomendados).
    "MON-REAL-001": {"medida_inflacion": "IPC_armonizado", "expectativa": "swap_1a", "plazo_meses": 3,
                     "anios_min": 10, "anios_recomendados": 20},
    # MON-FIX-001 · Parámetros: T (12 meses; 3–24); tau (3 meses; 1–6); escenarios (base, ±50, ±100 pb).
    # Entradas: ≥ 3 nodos hasta T.
    "MON-FIX-001": {"T_meses": 12, "T_meses_rango": [3, 24], "tau_meses": 3, "tau_meses_rango": [1, 6],
                    "escenarios_pb": [0, 50, -50, 100, -100], "nodos_min": 3},
    # IDX-ERP-001 · Parámetros: N (10; 5–10 años); lambda_reversion (0,5; 0–1); multiplo (CAPE; PER adelantado);
    # cobertura (cubierta; ambas). Entradas: historia del múltiplo ≥ 20 años (rechazo < 10); BPA histórico ≥ 20 años.
    "IDX-ERP-001": {"N": 10, "N_rango": [5, 10], "lambda_reversion": 0.5, "lambda_reversion_rango": [0, 1],
                    "multiplo": "CAPE", "cobertura": "cubierta", "anios_historia_min": 10,
                    "anios_historia_recomendados": 20, "anios_bpa_historico_min": 20},
    # IDX-CONC-001 · Parámetros: top_n (10; 5–50); media_amplitud (200 sesiones); ventana_percentil (20 años; mínimo
    # 10). Método (ii): diferencial a 3 y 12 meses. Entradas: precios ≥ 1 año.
    "IDX-CONC-001": {"top_n": 10, "top_n_rango": [5, 50], "media_amplitud": 200, "ventana_percentil_anios": 20,
                     "ventana_percentil_min_anios": 10, "anios_precios_min": 1, "meses_diferencial": [3, 12]},
    # IDX-REL-001 · Parámetros: multiplos (PER adelantado, CAPE); ajuste_sectorial (true); ventana (20 años);
    # divisa_comun (EUR); cobertura (ambas). Entradas: ≥ 15 años (10 con limitación). Método (iv): momentum 12-1 y a
    # 3 meses; (v): revisiones a 3 meses.
    "IDX-REL-001": {"multiplos": ["per_adelantado", "cape"], "ajuste_sectorial": True, "ventana_anios": 20,
                    "divisa_comun": "EUR", "cobertura": "ambas", "anios_min": 10, "anios_recomendados": 15,
                    "momentum_retro_meses": 12, "momentum_salto_meses": 1, "momentum_corto_meses": 3},
    # IDX-REB-001 · Parámetros: ventana_evento (anuncio→efectividad; efectividad→+20); modelo_normal (índice de
    # mercado; modelo de mercado con 250 sesiones de estimación); contraste (BMP). Rechazo parcial: < 20 eventos.
    "IDX-REB-001": {"ventana_post_sesiones": 20, "modelo_normal": "indice_mercado", "sesiones_estimacion": 250,
                    "contraste": "BMP", "eventos_min": 20},
}


# ======================================================================= utilidades comunes
# T-106 (QA r02, H-14): los umbrales de rechazo y de limitación y los rangos admitidos los fija la ficha; una petición no
# los puede cambiar (como `UMBRALES` en TCV y `MINIMOS`/`RANGOS` en FON y DER).
UMBRALES: dict[str, frozenset[str]] = {
    f: frozenset(k for k in d if k.endswith(("_min", "_rango", "_min_anios", "_recomendados")) or k in ("meses_nodos", "anios_convexidad"))
    for f, d in PARAMETROS_POR_DEFECTO.items()}


# T-113 (H-24 de T-108): dominio de las ventanas, plazos y listas de la petición, como en FON, DER y TCV. Topes [PROPUESTO]
# (INC-T112-01): un horizonte no pasa de H5 de la configuración (120 meses = 2520 sesiones; §3 del Catálogo y horizontes
# del Documento 0); una ventana histórica, de 100 años, la misma cota que usan las fichas de valoración (T-112); las listas,
# de 12 elementos (los plazos de la curva monetaria: 1 a 12 meses) o 20 escenarios.
_MESES_H5, _SESIONES_H5, _ANIOS_HISTORIA = 120, 2520, 100
DOMINIOS: dict[str, dict[str, tuple[str, float, float]]] = {
    "MON-YLD-001": {"plazos_meses": ("lista_entera", 1, _MESES_H5)},
    "MON-EXP-001": {"diferencial_estable_dias": ("entero", 1, 252), "incremento_pb": ("real_positivo", 0, 100),
                    "meses_cambio_acumulado": ("lista_entera", 1, _MESES_H5)},
    "MON-REAL-001": {"plazo_meses": ("entero", 1, _MESES_H5)},
    "MON-FIX-001": {"escenarios_pb": ("lista_real", -1000, 1000)},
    "IDX-CONC-001": {"media_amplitud": ("entero", 1, _SESIONES_H5), "ventana_percentil_anios": ("entero", 1, _ANIOS_HISTORIA),
                     "meses_diferencial": ("lista_entera", 1, _MESES_H5)},
    "IDX-REL-001": {"ventana_anios": ("entero", 1, _ANIOS_HISTORIA), "momentum_retro_meses": ("entero", 2, _MESES_H5),
                    "momentum_salto_meses": ("entero", 0, _MESES_H5 - 1), "momentum_corto_meses": ("entero", 1, _MESES_H5)},
    "IDX-REB-001": {"ventana_post_sesiones": ("entero", 1, _SESIONES_H5), "sesiones_estimacion": ("entero", 1, _SESIONES_H5)},
}
_MAX_LISTA = {"escenarios_pb": 20}


def _dominio(ficha: str, p: dict) -> None:
    for clave, (tipo, lo, hi) in DOMINIOS.get(ficha, {}).items():
        x = p.get(clave)
        if tipo.startswith("lista"):
            if not isinstance(x, (list, tuple)) or not x or len(x) > _MAX_LISTA.get(clave, 12):
                raise ErrorFicha(f"{ficha}: parámetro {clave} debe ser una lista de 1 a {_MAX_LISTA.get(clave, 12)} elementos")
            elementos = list(x)
        else:
            elementos = [x]
        for e in elementos:
            if isinstance(e, bool) or not isinstance(e, (int, float)) or not math.isfinite(float(e)):
                raise ErrorFicha(f"{ficha}: parámetro {clave} = {e!r} no es un número finito")
            if tipo in ("entero", "lista_entera") and float(e) != int(e):
                raise ErrorFicha(f"{ficha}: parámetro {clave} = {e!r} no es entero")
            if not (lo < float(e) <= hi if tipo == "real_positivo" else lo <= float(e) <= hi):
                raise ErrorFicha(f"{ficha}: parámetro {clave} = {e!r} fuera del rango admitido [{lo}, {hi}]")
    if ficha == "IDX-REL-001" and p["momentum_salto_meses"] >= p["momentum_retro_meses"]:
        raise ErrorFicha(f"{ficha}: momentum_salto_meses debe ser menor que momentum_retro_meses")


def _params(ficha: str, params: dict | None) -> dict[str, Any]:
    if params is not None and not isinstance(params, dict):
        raise ErrorFicha(f"{ficha}: los parámetros deben ser un diccionario")
    fijos = set(params or {}) & UMBRALES[ficha]
    if fijos:
        raise ErrorFicha(f"{ficha}: {sorted(fijos)} son umbrales fijos de la ficha, no parámetros de la petición")
    p = dict(PARAMETROS_POR_DEFECTO[ficha])
    p.update(params or {})
    _dominio(ficha, p)
    return p


def _f(x: Any, ctx: str) -> float:
    """Número finito o ErrorFicha (nunca un 0 por defecto)."""
    if x is None or isinstance(x, bool):
        raise ErrorFicha(f"{ctx}: falta el dato o no es numérico")
    try:
        v = float(x)
    except (TypeError, ValueError):
        raise ErrorFicha(f"{ctx}: no es numérico ({x!r})") from None
    if not math.isfinite(v):
        raise ErrorFicha(f"{ctx}: no es finito")
    return v


def _req(d: Any, clave: str, ctx: str) -> Any:
    if not isinstance(d, dict) or d.get(clave) is None:
        raise ErrorFicha(f"{ctx}: falta «{clave}»")
    return d[clave]


def _dict(x: Any, ctx: str) -> dict:
    if not isinstance(x, dict) or not x:
        raise ErrorFicha(f"{ctx}: se espera un dict no vacío")
    return x


def _lista(x: Any, ctx: str) -> list:
    if not isinstance(x, list) or not x:
        raise ErrorFicha(f"{ctx}: se espera una lista no vacía")
    return x


def _fecha(x: Any, ctx: str) -> pd.Timestamp:
    """Solo texto ISO, ``date``/``datetime``, ``Timestamp`` o ``datetime64``; un número no es una fecha (no es epoch)."""
    if not isinstance(x, (str, dt.date, pd.Timestamp, np.datetime64)):
        raise ErrorFicha(f"{ctx}: fecha no válida ({x!r}): se espera texto ISO o una fecha")
    try:
        t = pd.Timestamp(x)
    except (TypeError, ValueError):
        raise ErrorFicha(f"{ctx}: fecha no válida ({x!r})") from None
    if pd.isna(t):
        raise ErrorFicha(f"{ctx}: fecha no válida ({x!r})")
    return t


def _con_fuente(d: Any, ctx: str) -> float:
    """Dato externo {'valor', 'fuente'}: sin fuente se rechaza."""
    if not isinstance(d, dict):
        raise ErrorFicha(f"{ctx}: se espera {{'valor', 'fuente'}}")
    fuente = d.get("fuente")
    if not isinstance(fuente, str) or not fuente.strip():
        raise ErrorFicha(f"{ctx}: dato externo sin fuente")
    return _f(d.get("valor"), ctx)


def _serie(lista: Any, campo: str, ctx: str) -> pd.Series:
    """Lista de dicts con 'fecha' y `campo` → serie ordenada por fecha (fechas repetidas se rechazan)."""
    filas = _lista(lista, ctx)
    fechas, valores = [], []
    for i, fila in enumerate(filas):
        fechas.append(_fecha(_req(fila, "fecha", f"{ctx}[{i}]"), f"{ctx}[{i}]"))
        valores.append(_f(_req(fila, campo, f"{ctx}[{i}]"), f"{ctx}[{i}].{campo}"))
    s = pd.Series(valores, index=pd.DatetimeIndex(fechas)).sort_index()
    if s.index.has_duplicates:
        raise ErrorFicha(f"{ctx}: fechas repetidas")
    return s


def _anios(indice: pd.Index) -> float:
    return float((indice[-1] - indice[0]).days) / DIAS_ANIO


def _posicion(valor: float, historia: Any) -> dict[str, Any]:
    h = np.asarray(historia, dtype=float)
    if len(h) < 2:
        raise ErrorFicha("posición histórica: se necesitan al menos 2 observaciones")
    # Historia constante ⇒ dispersión exactamente nula (np.std deja un residuo de redondeo que inflaría el z).
    sd = float(np.std(h, ddof=1)) if float(np.ptp(h)) > 0 else 0.0
    return {"valor": float(valor), "percentil": float(np.mean(h <= valor)),
            "z": float((valor - np.mean(h)) / sd) if sd > 0 else None, "media": float(np.mean(h)), "n": len(h)}


def _en_rango(p: dict, clave: str, ficha: str) -> float:
    x = _f(p.get(clave), f"{ficha}: parámetro {clave}")
    lo, hi = p[f"{clave}_rango"]
    if not lo <= x <= hi:
        raise ErrorFicha(f"{ficha}: {clave} = {x} fuera del rango admitido [{lo}, {hi}]")
    return x


def _dias_meses(fecha: pd.Timestamp, meses: float) -> int:
    m = _f(meses, "plazo en meses")
    if m != int(m):
        raise ErrorFicha(f"plazo en meses no entero ({meses})")
    try:
        return int((fecha + pd.DateOffset(months=int(m)) - fecha).days)
    except (OverflowError, ValueError) as e:
        raise ErrorFicha(f"plazo de {meses} meses fuera del calendario representable") from e


def _no_finitos(x: Any, ruta: str = "resultado") -> list[str]:
    if isinstance(x, dict):
        return [r for k, val in x.items() for r in _no_finitos(val, f"{ruta}.{k}")]
    if isinstance(x, (list, tuple)):
        return [r for i, val in enumerate(x) for r in _no_finitos(val, f"{ruta}[{i}]")]
    if isinstance(x, (float, np.floating)) and not math.isfinite(float(x)):
        return [ruta]
    return []


Manejador = Callable[[dict, dict], tuple[dict, list[str]]]


def _cerrado(ficha: str) -> Callable[[Manejador], Manejador]:
    """Falla cerrado en profundidad: entradas mal formadas o fuera de dominio y resultados no finitos → ErrorFicha.

    Cada manejador valida sus entradas con motivo propio; esta envoltura traduce lo que se escape (aritmética fuera
    de dominio, tipos inesperados, fechas fuera de rango, no convergencia) y rechaza cualquier NaN/inf del resultado:
    lo indefinido se entrega como ``None``, nunca como un número no finito.
    """
    def decorar(fn: Manejador) -> Manejador:
        @wraps(fn)
        def envoltura(ent: dict, params: dict) -> tuple[dict, list[str]]:
            if not isinstance(ent, dict) or not isinstance(ent.get("valores"), dict):
                raise ErrorFicha(f"{ficha}: los datos en línea («valores») deben ser un dict")
            if params is not None and not isinstance(params, dict):
                raise ErrorFicha(f"{ficha}: los parámetros deben ser un dict")
            try:
                res, lim = fn(ent, params or {})
            except ErrorFicha:
                raise
            except (ArithmeticError, ValueError, TypeError, AttributeError, KeyError, IndexError,
                    RuntimeError) as e:
                raise ErrorFicha(f"{ficha}: entrada mal formada o fuera de dominio ({type(e).__name__}: {e})") from e
            malos = _no_finitos(res)
            if malos:
                raise ErrorFicha(f"{ficha}: resultado no finito en {', '.join(malos[:3])} (entradas fuera de dominio)")
            return res, lim
        return envoltura
    return decorar


# ======================================================================= MON-YLD-001
_CONV_MON = ("descuento_360", "precio", "simple_360", "simple_365", "tae")


def _a_precio(conv: str, x: float, t: float) -> float:
    if conv == "descuento_360":
        precio = 1 - x * t / BASE_360
    elif conv == "precio":
        precio = x
    elif conv in ("simple_360", "simple_365"):
        factor = 1 + x * t / (BASE_360 if conv == "simple_360" else DIAS_ANIO)
        if factor <= 0:
            raise ErrorFicha(f"MON-YLD-001: factor de capitalización no positivo con {conv}")
        precio = 1 / factor
    elif conv == "tae":
        if 1 + x <= 0:
            raise ErrorFicha("MON-YLD-001: TAE ≤ −100 %")
        precio = (1 + x) ** (-t / DIAS_ANIO)
    else:
        raise ErrorFicha(f"MON-YLD-001: convención desconocida «{conv}» (admitidas: {', '.join(_CONV_MON)})")
    if not precio > 0:
        raise ErrorFicha(f"MON-YLD-001: precio implícito no positivo ({precio}) con {conv}")
    return float(precio)


def _desde_precio(conv: str, precio: float, t: float) -> float:
    if conv == "descuento_360":
        return (1 - precio) * BASE_360 / t
    if conv == "precio":
        return precio
    if conv == "simple_360":
        return (1 / precio - 1) * BASE_360 / t
    if conv == "simple_365":
        return (1 / precio - 1) * DIAS_ANIO / t
    return float(precio ** (-DIAS_ANIO / t) - 1)   # tae


@_cerrado("MON-YLD-001")
def f_mon_yld(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """MON-YLD-001 · Rentabilidad equivalente y comparación de segmentos monetarios.

    ``valores``:
      - ``segmentos``: lista de {segmento, divisa, plazo_meses, dias, convencion, valor, fecha}; ``convencion`` ∈
        descuento_360 (P = 1 − d·t/360), precio, simple_360 (money market yield), simple_365, tae.
      - ``pares`` (opcional): [[a, b], …] → diferencial a − b en pb a igual divisa, plazo y fecha. Sin ``pares``, todos
        los pares alineables (orden alfabético).
      - ``historia_diferenciales`` (opcional): {id del diferencial: [{fecha, valor_pb}]} para el percentil (≥ 5 años).
      - ``cobertura`` (si el parámetro cobertura es true): {divisa_destino, segmentos: {id del segmento: {spot,
        forward}}}, con spot y forward en unidades de divisa del segmento por unidad de divisa destino.
    """
    ficha = "MON-YLD-001"
    p = _params(ficha, params)
    v = ent["valores"]
    lim: list[str] = []
    base_salida = p["base_salida"]
    if base_salida not in ("TAE", "Act/365"):
        raise ErrorFicha(f"{ficha}: base_salida «{base_salida}» no admitida (TAE o Act/365)")
    clave_rend = "tae" if base_salida == "TAE" else "simple_365"
    tabla: dict[str, dict[str, Any]] = {}
    meta: dict[str, tuple[str, str, float, pd.Timestamp]] = {}
    err_ida_vuelta = 0.0
    for i, s in enumerate(_lista(_req(v, "segmentos", ficha), f"{ficha}: segmentos")):
        ctx = f"{ficha}: segmentos[{i}]"
        if not isinstance(s, dict) or not s.get("convencion"):
            raise ErrorFicha(f"{ctx}: falta la convención (se pide aclaración)")
        conv = str(s["convencion"])
        nombre = str(_req(s, "segmento", ctx))
        divisa = str(_req(s, "divisa", ctx))
        plazo = _f(_req(s, "plazo_meses", ctx), f"{ctx}.plazo_meses")
        t = _f(_req(s, "dias", ctx), f"{ctx}.dias")
        if t <= 0:
            raise ErrorFicha(f"{ctx}: días no positivos")
        fecha = _fecha(_req(s, "fecha", ctx), ctx)
        x = _f(_req(s, "valor", ctx), f"{ctx}.valor")
        precio = _a_precio(conv, x, t)
        clave = f"{nombre} · {divisa} · {plazo:g}m"
        if clave in tabla:
            raise ErrorFicha(f"{ctx}: segmento repetido «{clave}»")
        if plazo not in [float(m) for m in p["plazos_meses"]]:
            lim.append(f"{clave}: plazo fuera de la rejilla declarada {p['plazos_meses']}")
        fila: dict[str, Any] = {c: _desde_precio(c, precio, t) for c in _CONV_MON}
        # Ida y vuelta de cada conversión (Verificación): convención → precio → convención.
        err_ida_vuelta = max(err_ida_vuelta, abs(_desde_precio(conv, precio, t) - x))
        for c in _CONV_MON:
            err_ida_vuelta = max(err_ida_vuelta, abs(_a_precio(c, fila[c], t) - precio))
        fila.update({"dias": t, "fecha": fecha.date().isoformat(), "convencion_entrada": conv,
                     "rendimiento_equivalente": fila[clave_rend]})
        tabla[clave] = fila
        meta[clave] = (nombre, divisa, plazo, fecha)

    # (ii) Diferenciales a igual plazo, divisa y fecha.
    grupos: dict[tuple[str, float, pd.Timestamp], dict[str, str]] = {}
    for clave, (nombre, divisa, plazo, fecha) in meta.items():
        grupos.setdefault((divisa, plazo, fecha), {})[nombre] = clave
    pares = v.get("pares")
    difs: dict[str, float] = {}
    if pares:
        for par in pares:
            if not isinstance(par, (list, tuple)) or len(par) != 2:
                raise ErrorFicha(f"{ficha}: cada par es [a, b]")
            a, b = str(par[0]), str(par[1])
            alineados = [g for g in sorted(grupos, key=str) if a in grupos[g] and b in grupos[g]]
            if not alineados:
                raise ErrorFicha(f"{ficha}: «{a}» y «{b}» no son alineables (distinto plazo, divisa o fecha)")
            for g in alineados:
                difs[f"{a} − {b} · {g[0]} · {g[1]:g}m"] = (tabla[grupos[g][a]]["rendimiento_equivalente"]
                                                         - tabla[grupos[g][b]]["rendimiento_equivalente"]) * PB
    else:
        for g in sorted(grupos, key=str):
            nombres = sorted(grupos[g])
            for i, a in enumerate(nombres):
                for b in nombres[i + 1:]:
                    difs[f"{a} − {b} · {g[0]} · {g[1]:g}m"] = (tabla[grupos[g][a]]["rendimiento_equivalente"]
                                                             - tabla[grupos[g][b]]["rendimiento_equivalente"]) * PB
        if not difs and len(tabla) > 1:
            lim.append("ningún par de segmentos alineable: sin diferenciales")

    # (iv) Percentiles frente a ≥ 5 años.
    hist = v.get("historia_diferenciales") or {}
    percentiles: dict[str, Any] = {}
    for clave_dif in sorted(difs):
        if clave_dif not in hist:
            percentiles[clave_dif] = None
            continue
        s = _serie(hist[clave_dif], "valor_pb", f"{ficha}: historia {clave_dif}")
        if len(s) < 2 or _anios(s.index) < p["anios_percentil_min"]:
            lim.append(f"{clave_dif}: historia < {p['anios_percentil_min']} años; sin percentil")
            percentiles[clave_dif] = None
            continue
        percentiles[clave_dif] = _posicion(difs[clave_dif], s.values)
    if difs and not hist:
        lim.append("sin historia de diferenciales: percentiles no calculados")

    # (iii) Rendimiento cubierto = (1 + i_ext·t/base_ext)·(S/F) − 1, anualizado en TAE.
    cubierto: dict[str, Any] | None = None
    if p["cobertura"]:
        cob = _req(v, "cobertura", ficha)
        destino = str(_req(cob, "divisa_destino", f"{ficha}: cobertura"))
        datos_cob = cob.get("segmentos") or {}
        cubierto = {}
        for clave in sorted(tabla):
            if meta[clave][1] == destino:
                continue
            if clave not in datos_cob:
                raise ErrorFicha(f"{ficha}: cobertura pedida sin spot y forward para «{clave}»")
            spot = _f(_req(datos_cob[clave], "spot", clave), f"{clave}.spot")
            fwd = _f(_req(datos_cob[clave], "forward", clave), f"{clave}.forward")
            if spot <= 0 or fwd <= 0:
                raise ErrorFicha(f"{ficha}: spot y forward deben ser positivos ({clave})")
            t = tabla[clave]["dias"]
            bruto = (1 / _a_precio("precio", tabla[clave]["precio"], t)) * (spot / fwd)
            cubierto[clave] = {"divisa_destino": destino, "rendimiento_periodo": bruto - 1,
                               "tae": bruto ** (DIAS_ANIO / t) - 1}
        if not cubierto:
            lim.append(f"cobertura pedida, pero ningún segmento en divisa distinta de {destino}")

    res = {
        "tabla": tabla,
        "rendimiento_equivalente": {k: f["rendimiento_equivalente"] for k, f in tabla.items()},
        "base_salida": base_salida,
        "diferenciales_pb": difs,
        "rendimiento_cubierto": cubierto,
        "percentiles": percentiles,
        "verificacion": {"error_ida_vuelta_max": err_ida_vuelta},
        "unidades": {"rendimientos": "tanto por uno (TAE o simple Act/365 según base_salida)",
                     "diferenciales_pb": "pb", "precio": "por unidad de nominal"},
        "referencia_ingenua": "€STR compuesto (8.4 del Documento 0) o su homólogo de la divisa; RI-PA",
        "advertencias": ["los segmentos difieren en riesgo emisor, liquidez y protección: el diferencial no es gratuito",
                         "sin costes ni condiciones de instrumentos concretos (1.6); retenciones solo si se declaran"],
    }
    return res, lim


# ======================================================================= MON-EXP-001
def _media_unidad(x: Any) -> float:
    """Error máximo de redondeo de una cotización: medio último dígito decimal con que viene escrita."""
    texto = x.strip() if isinstance(x, str) else repr(float(x))
    exponente = Decimal(texto).as_tuple().exponent
    if not isinstance(exponente, int):
        raise ErrorFicha(f"cotización no finita ({x!r})")
    return float(Decimal(1).scaleb(exponente)) / 2


def _nodos_ois(v: dict, fecha: pd.Timestamp, base: float, r0: float, p: dict,
               lim: list[str]) -> tuple[list[tuple[int, float, float]], np.ndarray, np.ndarray, float | None]:
    """Nodos (días, log del factor de capitalización, tipo simple) desde una curva OIS o una tira de futuros.

    Devuelve también la sensibilidad G = ∂(log factor del nodo)/∂(cotización) (nodos × cotizaciones) y el error de
    redondeo de cada cotización (``precision_cotizacion`` de ``valores`` si se declara; si no, medio último dígito).
    """
    ficha = "MON-EXP-001"
    if v.get("curva") is not None and v.get("futuros") is not None:
        raise ErrorFicha(f"{ficha}: aporte curva OIS o futuros, no ambos")
    declarada = None
    if v.get("precision_cotizacion") is not None:
        declarada = _f(v["precision_cotizacion"], f"{ficha}.precision_cotizacion")
        if declarada < 0:
            raise ErrorFicha(f"{ficha}: precision_cotizacion negativa")
    nodos: list[tuple[int, float, float]] = []
    filas: list[list[float]] = []
    precision: list[float] = []
    if v.get("curva") is not None:
        curva = _lista(v["curva"], f"{ficha}: curva")
        for i, n in enumerate(curva):
            ctx = f"{ficha}: curva[{i}]"
            if not isinstance(n, dict):
                raise ErrorFicha(f"{ctx}: se espera un dict {{dias | fecha_fin, tipo}}")
            if n.get("fecha_fin") is not None:
                d = int((_fecha(n["fecha_fin"], ctx) - fecha).days)
            else:
                dd = _f(_req(n, "dias", ctx), f"{ctx}.dias")
                if dd != int(dd):
                    raise ErrorFicha(f"{ctx}: días no enteros")
                d = int(dd)
            if d <= 0:
                raise ErrorFicha(f"{ctx}: nodo no posterior a la fecha de cálculo")
            r = _f(_req(n, "tipo", ctx), f"{ctx}.tipo")
            if r * d / base <= -1:
                raise ErrorFicha(f"{ctx}: factor de capitalización no positivo")
            nodos.append((d, math.log1p(r * d / base), r))
            fila = [0.0] * len(curva)
            fila[i] = (d / base) / (1 + r * d / base)
            filas.append(fila)
            precision.append(declarada if declarada is not None else _media_unidad(n["tipo"]))
    elif v.get("futuros") is not None:
        futs = _lista(v["futuros"], f"{ficha}: futuros")
        if not all(isinstance(x, dict) for x in futs):
            raise ErrorFicha(f"{ficha}: cada futuro es un dict {{inicio, fin, precio}}")
        futs = sorted(futs, key=lambda x: _fecha(_req(x, "inicio", ficha), ficha))
        limite = (fecha + pd.DateOffset(years=int(p["anios_convexidad"])) - fecha).days
        acumulado = 0.0   # log del factor de capitalización
        sens: list[float] = []
        anterior = fecha
        for i, fu in enumerate(futs):
            ctx = f"{ficha}: futuros[{i}]"
            ini, fin = _fecha(_req(fu, "inicio", ctx), ctx), _fecha(_req(fu, "fin", ctx), ctx)
            if fin <= ini:
                raise ErrorFicha(f"{ctx}: fin no posterior al inicio")
            if i == 0 and ini > fecha:
                # Tramo inicial hasta el primer contrato: tipo de mercado vigente (tipo oficial − diferencial estable).
                acumulado += int((ini - fecha).days) * math.log1p(r0 / base)
                lim.append("tramo previo al primer futuro capitalizado al tipo de mercado vigente")
            elif i == 0 and ini < fecha:
                raise ErrorFicha(f"{ctx}: el primer contrato empieza antes de la fecha de cálculo")
            elif i > 0 and ini != anterior:
                raise ErrorFicha(f"{ctx}: la tira de futuros no es contigua (hueco o solape)")
            precio = _f(_req(fu, "precio", ctx), f"{ctx}.precio")
            tipo = (PRECIO_PAR_FUTURO - precio) / PRECIO_PAR_FUTURO
            d = int((fin - fecha).days)
            if p["convexidad"] and d > limite:
                if fu.get("ajuste_convexidad") is None:
                    lim.append(f"futuros desde {ini.date()} (> {p['anios_convexidad']} año) sin ajuste de convexidad "
                               "aportado (dato externo con fuente): se trunca la curva")
                    break
                tipo -= _con_fuente(fu["ajuste_convexidad"], f"{ctx}.ajuste_convexidad")
            n_dias = (fin - ini).days
            if tipo * n_dias / base <= -1:
                raise ErrorFicha(f"{ctx}: factor de capitalización no positivo")
            acumulado += math.log1p(tipo * n_dias / base)
            sens.append((n_dias / base) / (1 + tipo * n_dias / base))
            nodos.append((d, acumulado, math.expm1(acumulado) * base / d))
            filas.append(sens + [0.0] * (len(futs) - len(sens)))
            precision.append(declarada if declarada is not None else
                             _media_unidad(fu["precio"]) / PRECIO_PAR_FUTURO)
            anterior = fin
    else:
        raise ErrorFicha(f"{ficha}: falta la curva OIS o los futuros")
    if not nodos:
        raise ErrorFicha(f"{ficha}: curva vacía tras la validación")
    orden = sorted(range(len(nodos)), key=lambda i: nodos[i][0])
    nodos = [nodos[i] for i in orden]
    if len({d for d, _, _ in nodos}) != len(nodos):
        raise ErrorFicha(f"{ficha}: nodos con el mismo plazo")
    g = np.array([filas[i][:len(precision)] for i in orden], dtype=float)
    return nodos, g, np.array(precision, dtype=float), declarada


def _tipo_en(tasas: list[float], cortes: list[int], d: int) -> float:
    """Tipo de la senda vigente en el día d (la reunión aplica desde su fecha; el último tramo cierra en el nodo)."""
    return tasas[max(k for k in range(len(tasas)) if cortes[k] <= d)]


@_cerrado("MON-EXP-001")
def f_mon_exp(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """MON-EXP-001 · Expectativas implícitas de tipos a corto.

    ``valores``: ``fecha``; ``base_curva`` (360 o 365: convención del tipo a un día); ``curva`` [{dias | fecha_fin,
    tipo}] (tipos OIS simples Act/base) o ``futuros`` [{inicio, fin, precio, ajuste_convexidad?}]; ``reuniones``
    [fechas]; ``tipo_oficial``; ``diferencial_estable`` (tipo oficial − tipo de mercado) o ``historia_diferencial``
    [valores, el último el más reciente]; ``decisiones`` (opcional) [{fecha, tipo_decidido, tipo_esperado}] con el tipo
    esperado de la senda del día anterior; ``precision_cotizacion`` (opcional, tanto por uno): error de redondeo de las
    cotizaciones; si no se declara, el medio último dígito con que viene escrita cada una.

    Modelo (un tramo por reunión): el tipo a un día es constante entre reuniones y se capitaliza a diario (día
    natural, Act/base). Antes de la primera reunión vale el tipo de mercado vigente (tipo oficial − diferencial
    estable); los tramos posteriores se resuelven a la vez por mínimos cuadrados con TODOS los nodos (en log del factor
    de capitalización el sistema es lineal). La curva se rechaza:
      - si los nodos no identifican un tramo por reunión (rango insuficiente);
      - si la hipótesis escalonada no se puede contrastar: tantos nodos útiles como tramos y algún tramo sin nodos en
        sus dos extremos (fechas de reunión). Con un sistema justo, cualquier curva se reproduce exactamente, también
        una que no es escalonada (p. ej., una curva cotizada plana con nodos 10 días tras cada reunión daría ±15
        movimientos inventados);
      - si algún nodo, también los que no añaden reunión, no se reproduce dentro de la tolerancia de la ficha
        (relativa, sobre el tipo del nodo): esa curva no admite una senda escalonada. Solo si el solicitante declara
        ``precision_cotizacion`` (cotizaciones redondeadas), el desajuste admitido es el mayor de esa precisión y la
        tolerancia de la ficha: una cotización redondeada no se puede reproducir mejor que su propio redondeo;
      - si el redondeo de las cotizaciones puede mover el tipo de algún tramo un incremento Δ o más (senda no
        identificada: nodos que caen pocos días después de una reunión amplifican el ruido de cotización).
    Cada tramo es exactamente el *forward* entre fechas de reunión de la curva: el «ajuste por días del periodo» queda
    implícito.

    «Tipo vigente» (paso iii) — decisión declarada (INC-T106-01 [PROPUESTO]): ``probabilidades`` reparte el movimiento
    de cada reunión frente al tipo en vigor justo antes de ella (el implícito tras la reunión anterior; en la primera
    reunión coincide con el tipo oficial vigente hoy); ``probabilidades_acumuladas`` aplica la fórmula literal frente
    al tipo oficial vigente hoy (movimientos acumulados hasta esa reunión).
    """
    ficha = "MON-EXP-001"
    tol = FICHAS[ficha]["tol"]
    p = _params(ficha, params)
    v = ent["valores"]
    lim: list[str] = []
    fecha = _fecha(_req(v, "fecha", ficha), ficha)
    base = _f(_req(v, "base_curva", ficha), f"{ficha}.base_curva")
    if base not in (BASE_360, DIAS_ANIO):
        raise ErrorFicha(f"{ficha}: base_curva debe ser {BASE_360} o {DIAS_ANIO}")
    oficial = _f(_req(v, "tipo_oficial", ficha), f"{ficha}.tipo_oficial")
    if v.get("diferencial_estable") is not None:
        dif = _f(v["diferencial_estable"], f"{ficha}.diferencial_estable")
    elif v.get("historia_diferencial") is not None:
        h = [_f(x, f"{ficha}.historia_diferencial") for x in _lista(v["historia_diferencial"], ficha)]
        n = int(_f(p["diferencial_estable_dias"], "diferencial_estable_dias"))
        if len(h) < n:
            raise ErrorFicha(f"{ficha}: historia del diferencial con {len(h)} días (< {n})")
        dif = float(np.mean(h[-n:]))
    else:
        raise ErrorFicha(f"{ficha}: falta el diferencial habitual tipo oficial–tipo de mercado")
    r0 = oficial - dif
    if r0 / base <= -1:
        raise ErrorFicha(f"{ficha}: tipo de mercado vigente fuera de dominio")
    incremento = _f(p["incremento_pb"], "incremento_pb") / PB
    if incremento <= 0:
        raise ErrorFicha(f"{ficha}: incremento no positivo")
    nodos, g_sens, precision, declarada = _nodos_ois(v, fecha, base, r0, p, lim)
    d12 = _dias_meses(fecha, p["meses_nodos"])
    if sum(1 for d, _, _ in nodos if d <= d12) < p["nodos_min"]:
        raise ErrorFicha(f"{ficha}: menos de {p['nodos_min']} nodos en {p['meses_nodos']} meses")
    if v.get("reuniones") is None:
        raise ErrorFicha(f"{ficha}: falta el calendario de reuniones")
    d_fin = nodos[-1][0]
    reuniones = sorted({_fecha(x, f"{ficha}.reuniones") for x in _lista(v["reuniones"], f"{ficha}: reuniones")})
    validas = [m for m in reuniones if fecha < m and (m - fecha).days < d_fin]
    fuera = [m for m in reuniones if m > fecha and (m - fecha).days >= d_fin]
    if fuera:
        lim.append(f"{len(fuera)} reunión(es) en o después del último nodo: fuera de la senda")
    if not validas:
        raise ErrorFicha(f"{ficha}: ninguna reunión dentro del tramo cubierto por la curva")
    cortes = [0] + [int((m - fecha).days) for m in validas] + [d_fin]
    n_tramos = len(validas)
    l0 = math.log1p(r0 / base)
    a_mat = np.zeros((len(nodos), n_tramos))
    y = np.zeros(len(nodos))
    for i, (d, lg, _) in enumerate(nodos):
        y[i] = lg - min(d, cortes[1]) * l0
        for k in range(1, n_tramos + 1):
            if cortes[k] < d:
                a_mat[i, k - 1] = min(cortes[k + 1], d) - cortes[k]
    if int(np.linalg.matrix_rank(a_mat)) < n_tramos:
        raise ErrorFicha(f"{ficha}: los {len(nodos)} nodos no identifican un tramo por cada una de las {n_tramos} "
                         "reuniones (hace falta al menos un nodo nuevo entre cada reunión y la siguiente)")
    # Contraste de la hipótesis escalonada: con tantos nodos útiles como tramos, cualquier curva se «reproduce»
    # exactamente (la verificación sería tautológica) y un nodo pocos días después de una reunión extrapola su tramo
    # entero. Se exige o bien redundancia (más nodos útiles que tramos: el ajuste se contrasta) o bien que cada tramo
    # se lea directamente como forward entre puntos conocidos (fechas de reunión con nodo, o la primera reunión, cuyo
    # factor da el tipo vigente).
    utiles = int(np.count_nonzero(a_mat.any(axis=1)))
    conocidos = {0, cortes[1]} | {d for d, _, _ in nodos}
    alineada = all(cortes[k] in conocidos and cortes[k + 1] in conocidos for k in range(1, n_tramos + 1))
    if utiles <= n_tramos and not alineada:
        raise ErrorFicha(f"{ficha}: la senda escalonada no se puede contrastar: {utiles} nodo(s) útiles para "
                         f"{n_tramos} tramo(s) y nodos fuera de las fechas de reunión; aporte un nodo más o nodos en "
                         "las fechas de reunión")
    x = np.linalg.lstsq(a_mat, y, rcond=None)[0]
    tasas = [r0] + [math.expm1(float(xk)) * base for xk in x]
    # Reproducción de TODOS los nodos (Verificación: «la senda reproduce los forwards de entrada»).
    ajuste = a_mat @ x + np.array([min(d, cortes[1]) * l0 for d, _, _ in nodos])
    filas_nodos = []
    err_max = 0.0
    # T-113 (H-27 de T-108): con la precisión declarada, el desajuste que puede dejar el redondeo en cada nodo no es la
    # precisión de una cotización, sino la del residuo de mínimos cuadrados: |(I − A·A⁺)·G| · precisión, en log del factor,
    # pasado a tipo. Antes se exigía la precisión sola, y se rechazaban curvas escalonadas exactas que solo estaban redondeadas
    if declarada is not None:
        proy = np.eye(len(nodos)) - a_mat @ np.linalg.pinv(a_mat)
        cota_res_log = np.abs(proy @ g_sens) @ precision
    else:
        cota_res_log = np.zeros(len(nodos))
    for (d, _, r_nodo), lg_m, c_log in zip(nodos, ajuste, cota_res_log):
        r_senda = math.expm1(float(lg_m)) * base / d
        err = abs(r_senda - r_nodo)
        filas_nodos.append({"dias": d, "tipo_nodo": r_nodo, "tipo_senda": r_senda})
        err_max = max(err_max, err)
        cota_nodo = math.exp(float(lg_m)) * base / d * float(c_log)
        if err > max(tol * (abs(r_nodo) if r_nodo != 0 else 1.0), declarada or 0.0, cota_nodo * (1 + 1e-6)):
            raise ErrorFicha(f"{ficha}: la curva no se puede reproducir con un tramo por reunión: el nodo a {d} días "
                             f"queda a {err * PB:.6g} pb de la mejor senda escalonada"
                             + ("" if declarada is not None else "; si las cotizaciones vienen redondeadas, declare "
                                "«precision_cotizacion» (QA r02 de T-106, H-19)"))
    # Identificación frente al redondeo de las cotizaciones: cota de |δ tipo| de cada tramo.
    jac = np.linalg.pinv(a_mat) @ g_sens
    cota_x = np.abs(jac) @ precision
    cota_r = [base * math.exp(float(xk)) * float(c) for xk, c in zip(x, cota_x)]
    # T-113 (H-23 de T-108): la probabilidad de cada reunión depende de r_k − r_{k−1}, que suma el redondeo de dos tramos.
    # Su cota sale de la diferencia de filas del jacobiano (la primera reunión se compara con el tipo vigente, sin redondeo)
    d_r = base * np.exp(x)[:, None] * jac   # d r_k / d cotización
    cota_mov = [float(np.abs(d_r[0]) @ precision)] + [float(np.abs(d_r[k] - d_r[k - 1]) @ precision) for k in range(1, len(x))]
    for m, c in zip(validas, cota_r):
        if not c < incremento:
            raise ErrorFicha(f"{ficha}: senda no identificada en la reunión {m.date()}: el redondeo de las "
                             f"cotizaciones puede moverla {c * PB:.4g} pb (≥ incremento de {incremento * PB:g} pb)")
    senda = []
    for k, m in enumerate(validas, start=1):
        rk, previo = tasas[k], tasas[k - 1]
        en_reunion = (rk - previo) / incremento
        acumulados = (rk + dif - oficial) / incremento
        senda.append({"fecha_reunion": m.date().isoformat(), "tipo_mercado_implicito": rk,
                      "tipo_oficial_implicito": rk + dif, "cambio_vs_vigente_pb": (rk - r0) * PB,
                      "movimientos_en_reunion": en_reunion, "movimientos_acumulados": acumulados,
                      "probabilidades": _prob_binaria(en_reunion),
                      "probabilidades_acumuladas": _prob_binaria(acumulados),
                      "incertidumbre_redondeo_pb": cota_r[k - 1] * PB,
                      "incertidumbre_probabilidad": min(1.0, cota_mov[k - 1] / incremento),
                      "incertidumbre_probabilidad_acumulada": min(1.0, cota_r[k - 1] / incremento)})
    # QA r02 de T-106, H-16: por debajo de Δ la senda se identifica, pero el redondeo puede mover cada probabilidad
    # hasta cota/Δ. Si eso supera la tolerancia de la ficha, se sirve con la limitación explícita, no como exacta.
    def _peor(s_):
        return max(s_["incertidumbre_probabilidad"], s_["incertidumbre_probabilidad_acumulada"])
    peor = max(senda, key=_peor)
    if _peor(peor) > tol:
        lim.append(f"el redondeo de las cotizaciones puede mover las probabilidades hasta "
                   f"{_peor(peor) * 100:.3g} puntos (reunión {peor['fecha_reunion']}; "
                   f"{peor['incertidumbre_redondeo_pb']:.3g} pb en el tipo, frente a un incremento de {incremento * PB:g} pb)")
    cambio: dict[str, float | None] = {}
    for meses in p["meses_cambio_acumulado"]:
        d_h = _dias_meses(fecha, meses)
        if d_h > d_fin:
            cambio[f"{meses}m"] = None
            lim.append(f"curva sin cobertura a {meses} meses: cambio acumulado no calculado")
            continue
        cambio[f"{meses}m"] = (_tipo_en(tasas, cortes, d_h) - r0) * PB
    sorpresas = []
    decisiones = v.get("decisiones")
    for i, dec in enumerate(_lista(decisiones, f"{ficha}: decisiones") if decisiones is not None else []):
        ctx = f"{ficha}: decisiones[{i}]"
        sorpresas.append({"fecha": _fecha(_req(dec, "fecha", ctx), ctx).date().isoformat(),
                          "sorpresa_pb": (_f(_req(dec, "tipo_decidido", ctx), ctx)
                                          - _f(_req(dec, "tipo_esperado", ctx), ctx)) * PB})
    res = {
        "senda": senda,
        "probabilidades": {s["fecha_reunion"]: s["probabilidades"] for s in senda},
        "probabilidades_acumuladas": {s["fecha_reunion"]: s["probabilidades_acumuladas"] for s in senda},
        "cambio_acumulado_pb": cambio,
        "sorpresas_pb": sorpresas,
        "tipo_mercado_vigente": r0, "diferencial_estable": dif, "incremento": incremento,
        "verificacion": {"error_reproduccion_nodos_max": err_max, "nodos": filas_nodos},
        "unidades": {"tipos": "tanto por uno, a un día, capitalización diaria Act/base",
                     "cambio_acumulado_pb": "pb", "sorpresas_pb": "pb", "movimientos": "múltiplos del incremento",
                     "incertidumbre_redondeo_pb": "pb (cota por el redondeo de las cotizaciones)",
                     "incertidumbre_probabilidad": "tanto por uno (cota del cambio de la probabilidad de la reunión por ese redondeo)",
                     "incertidumbre_probabilidad_acumulada": "tanto por uno (ídem, de la probabilidad acumulada)"},
        "referencia_ingenua": "RI-PA (tipo oficial sin cambios) y senda de encuesta si se aporta",
        "advertencias": ["los tipos implícitos incluyen una prima por plazo pequeña pero no nula",
                         "probabilidades neutrales al riesgo; método binario simplificado",
                         "el diferencial tipo oficial–mercado puede variar"],
    }
    return res, lim


def _prob_binaria(x: float) -> dict[str, Any]:
    """Reparto binario de |x| movimientos entre el entero inferior y el superior."""
    a = abs(x)
    n = math.floor(a)
    frac = a - n
    sentido = "subida" if x > 0 else "bajada" if x < 0 else "sin_cambio"
    return {"sentido": sentido, "movimientos": {str(n): 1 - frac, str(n + 1): frac}}


# ======================================================================= MON-REAL-001
@_cerrado("MON-REAL-001")
def f_mon_real(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """MON-REAL-001 · Rentabilidad real a corto plazo.

    ``valores["divisas"]``: {divisa: {tipo_nominal (anual, comparable con la inflación esperada),
    expectativa_inflacion {valor, fuente, tipo}, medida_inflacion?, fuente_ipc, historia [{fecha_inicio, fecha_fin,
    tipo_nominal, base, ipc_inicio, ipc_fin, vintage_inicio, vintage_fin}] (renovaciones contiguas al plazo),
    tipo_real_neutral? {valor, fuente}, historia_ex_ante? [{fecha, valor}]}}.

    Ex post por periodo: (1 + i·días/base)/(IPC_fin/IPC_inicio) − 1, anualizado Real/365. Las dos cifras del IPC de
    un periodo deben venir del mismo vintage y ese vintage no puede ser anterior al fin del periodo.
    """
    ficha = "MON-REAL-001"
    p = _params(ficha, params)
    v = ent["valores"]
    lim: list[str] = []
    divisas = _req(v, "divisas", ficha)
    if not isinstance(divisas, dict) or not divisas:
        raise ErrorFicha(f"{ficha}: «divisas» vacío")
    plazo = int(p["plazo_meses"])
    tabla: dict[str, dict[str, Any]] = {}
    for cod in sorted(divisas):
        dv = _dict(divisas[cod], f"{ficha}[{cod}]")
        ctx = f"{ficha}[{cod}]"
        if dv.get("medida_inflacion") is not None and dv["medida_inflacion"] != p["medida_inflacion"]:
            raise ErrorFicha(f"{ctx}: medida de inflación «{dv['medida_inflacion']}» distinta de la pedida "
                             f"«{p['medida_inflacion']}»")
        i_nom = _f(_req(dv, "tipo_nominal", ctx), f"{ctx}.tipo_nominal")
        exp = _req(dv, "expectativa_inflacion", ctx)
        pi_e = _con_fuente(exp, f"{ctx}.expectativa_inflacion")
        if exp.get("tipo") != p["expectativa"]:
            raise ErrorFicha(f"{ctx}: expectativa de tipo «{exp.get('tipo')}», pero se pide «{p['expectativa']}»")
        # (i) real ex ante (Fisher)
        ex_ante = (1 + i_nom) / (1 + pi_e) - 1
        fuente_ipc = dv.get("fuente_ipc")
        if not isinstance(fuente_ipc, str) or not fuente_ipc.strip():
            raise ErrorFicha(f"{ctx}: IPC sin fuente")
        periodos = []
        anterior: pd.Timestamp | None = None
        for j, h in enumerate(_lista(_req(dv, "historia", ctx), f"{ctx}.historia")):
            c = f"{ctx}.historia[{j}]"
            ini, fin = _fecha(_req(h, "fecha_inicio", c), c), _fecha(_req(h, "fecha_fin", c), c)
            if fin != ini + pd.DateOffset(months=plazo):
                raise ErrorFicha(f"{c}: periodo distinto del plazo de {plazo} meses")
            if anterior is not None and ini != anterior:
                raise ErrorFicha(f"{c}: renovaciones no contiguas")
            anterior = fin
            vi, vf = _fecha(_req(h, "vintage_inicio", c), c), _fecha(_req(h, "vintage_fin", c), c)
            if vi != vf:
                raise ErrorFicha(f"{c}: vintages incompatibles ({vi.date()} ≠ {vf.date()})")
            if vf < fin:
                raise ErrorFicha(f"{c}: vintage {vf.date()} anterior al fin del periodo {fin.date()}")
            base = _f(_req(h, "base", c), f"{c}.base")
            if base not in (BASE_360, DIAS_ANIO):
                raise ErrorFicha(f"{c}: base debe ser {BASE_360} o {DIAS_ANIO}")
            ipc0, ipc1 = _f(_req(h, "ipc_inicio", c), c), _f(_req(h, "ipc_fin", c), c)
            if ipc0 <= 0 or ipc1 <= 0:
                raise ErrorFicha(f"{c}: IPC no positivo")
            dias = (fin - ini).days
            nom = 1 + _f(_req(h, "tipo_nominal", c), f"{c}.tipo_nominal") * dias / base
            infl = ipc1 / ipc0
            real_p = nom / infl - 1     # (ii) Fisher ex post sobre el periodo
            periodos.append({"fecha_fin": fin.date().isoformat(), "dias": dias, "nominal_periodo": nom - 1,
                             "inflacion_periodo": infl - 1, "real_periodo": real_p,
                             "real_anualizado": (1 + real_p) ** (DIAS_ANIO / dias) - 1})
        primero = _fecha(dv["historia"][0]["fecha_inicio"], ctx)
        assert anterior is not None
        anios = float((anterior - primero).days) / DIAS_ANIO
        if anios < p["anios_min"]:
            raise ErrorFicha(f"{ctx}: historia de {anios:.2f} años (< {p['anios_min']})")
        if anios < p["anios_recomendados"]:
            lim.append(f"{cod}: historia de {anios:.2f} años (< {p['anios_recomendados']} recomendados)")
        # (iv) política de renovación compuesta y segunda vía FIN-CAGR-001
        g_real = float(np.prod([1 + x["real_periodo"] for x in periodos]))
        g_nom = float(np.prod([1 + x["nominal_periodo"] for x in periodos]))
        g_inf = float(np.prod([1 + x["inflacion_periodo"] for x in periodos]))
        real_comp = cagr(1.0, g_real, anios)
        segunda = (1 + cagr(1.0, g_nom, anios)) / (1 + cagr(1.0, g_inf, anios)) - 1
        # (iii) diferencial frente al tipo real neutral (dato externo con fuente)
        neutral = None
        if dv.get("tipo_real_neutral") is not None:
            neutral = ex_ante - _con_fuente(dv["tipo_real_neutral"], f"{ctx}.tipo_real_neutral")
        else:
            lim.append(f"{cod}: sin estimación publicada del tipo real neutral: diferencial no calculado")
        # (v) percentiles
        ex_post = [x["real_anualizado"] for x in periodos]
        pct: dict[str, Any] = {"ex_post": _posicion(ex_post[-1], ex_post)}
        if dv.get("historia_ex_ante"):
            pct["ex_ante"] = _posicion(ex_ante, _serie(dv["historia_ex_ante"], "valor", ctx).values)
        else:
            pct["ex_ante"] = None
            lim.append(f"{cod}: sin historia del real ex ante: percentil ex ante no calculado")
        tabla[cod] = {"real_ex_ante": ex_ante, "real_ex_post_ultimo": ex_post[-1], "serie_ex_post": periodos,
                      "real_compuesto_renovacion": real_comp, "segunda_via_fin_cagr": segunda,
                      "diferencial_neutral": neutral, "percentiles": pct, "anios_historia": anios}
    codigos = sorted(tabla)
    entre = {f"{a} − {b}": {"ex_ante": tabla[a]["real_ex_ante"] - tabla[b]["real_ex_ante"],
                           "ex_post": tabla[a]["real_ex_post_ultimo"] - tabla[b]["real_ex_post_ultimo"]}
             for i, a in enumerate(codigos) for b in codigos[i + 1:]}
    res = {
        "tabla": tabla,
        "real_ex_ante": {k: t["real_ex_ante"] for k, t in tabla.items()},
        "real_ex_post": {k: t["real_ex_post_ultimo"] for k, t in tabla.items()},
        "diferencial_neutral": {k: t["diferencial_neutral"] for k, t in tabla.items()},
        "percentiles": {k: t["percentiles"] for k, t in tabla.items()},
        "diferencias_entre_divisas": entre,
        "parametros": {"medida_inflacion": p["medida_inflacion"], "expectativa": p["expectativa"],
                       "plazo_meses": plazo},
        "verificacion": {"error_segunda_via_max": max(abs(t["real_compuesto_renovacion"] - t["segunda_via_fin_cagr"])
                                                      for t in tabla.values())},
        "unidades": {"tipos": "tanto por uno anual (diferencias: ×100 = pp)"},
        "referencia_ingenua": "RI-MH del tipo real y RI-PA",
        "advertencias": ["el swap de inflación incluye prima de riesgo", "la inflación medida no es la de cada inversor",
                         "fiscalidad no incluida"],
    }
    return res, lim


# ======================================================================= MON-FIX-001
def _tipo_constante(objetivo_log: float, n_dias: list[int], base: float, lo: float, hi: float) -> float:
    """Tipo constante r con Σ log(1 + r·n_k/base) = objetivo_log (monótona en r)."""
    def g(r: float) -> float:
        return sum(math.log1p(r * n / base) for n in n_dias) - objetivo_log

    g_lo, g_hi = g(lo), g(hi)
    if lo == hi or g_lo == 0:
        return lo
    if g_hi == 0:
        return hi
    if g_lo * g_hi > 0:
        # La raíz está en [lo, hi] por construcción (media de la propia senda); un mismo signo solo puede venir del
        # redondeo con una senda casi constante: se toma el extremo más cercano.
        return lo if abs(g_lo) <= abs(g_hi) else hi
    return float(optimize.brentq(g, lo, hi))


@_cerrado("MON-FIX-001")
def f_mon_fix(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """MON-FIX-001 · Valor de fijar plazo frente a renovar.

    ``valores``: ``fecha``; ``curva`` [{plazo_meses, tipo, base}] del mismo segmento (tipos simples Act/base);
    ``senda_mon_exp`` (opcional) [tipo por periodo de renovación] de MON-EXP-001; ``senda_encuesta`` (opcional) ídem;
    ``pesos_escenarios`` (opcional) {escenario: peso}.

    Días de cada plazo por calendario desde ``fecha``. Los nodos que faltan en múltiplos de tau se interpolan con
    log-factor de descuento lineal en días (forwards planos), declarado.
    """
    ficha = "MON-FIX-001"
    p = _params(ficha, params)
    v = ent["valores"]
    lim: list[str] = []
    T = _en_rango(p, "T_meses", ficha)
    tau = _en_rango(p, "tau_meses", ficha)
    if T != int(T) or tau != int(tau) or int(T) % int(tau):
        raise ErrorFicha(f"{ficha}: plazos incompatibles (T = {T:g} no es múltiplo entero de tau = {tau:g})")
    fecha = _fecha(_req(v, "fecha", ficha), ficha)
    bases, nodos = set(), {}
    for i, n in enumerate(_lista(_req(v, "curva", ficha), f"{ficha}: curva")):
        ctx = f"{ficha}: curva[{i}]"
        bases.add(_f(_req(n, "base", ctx), f"{ctx}.base"))
        m = _f(_req(n, "plazo_meses", ctx), f"{ctx}.plazo_meses")
        if m <= 0 or m in nodos:
            raise ErrorFicha(f"{ctx}: plazo no positivo o repetido")
        nodos[m] = _f(_req(n, "tipo", ctx), f"{ctx}.tipo")
    if len(bases) != 1:
        raise ErrorFicha(f"{ficha}: convenciones incompatibles en la curva ({sorted(bases)})")
    base = bases.pop()
    if base not in (BASE_360, DIAS_ANIO):
        raise ErrorFicha(f"{ficha}: base debe ser {BASE_360} o {DIAS_ANIO}")
    if sum(1 for m in nodos if m <= T) < p["nodos_min"]:
        raise ErrorFicha(f"{ficha}: menos de {p['nodos_min']} nodos hasta T = {T:g} meses")
    puntos = sorted([(0, 0.0)] + [(_dias_meses(fecha, m), -math.log1p(y * _dias_meses(fecha, m) / base))
                                  for m, y in nodos.items()])

    def log_df(d: int) -> float:
        for (d0, l0), (d1, l1) in pairwise(puntos):
            if d0 <= d <= d1:
                return l0 + (l1 - l0) * (d - d0) / (d1 - d0)
        raise ErrorFicha(f"{ficha}: la curva no llega a {d} días (sin extrapolación)")

    n_per = int(T) // int(tau)
    cortes = [_dias_meses(fecha, k * int(tau)) for k in range(n_per + 1)]
    interpolados = [k * int(tau) for k in range(1, n_per + 1) if float(k * int(tau)) not in nodos]
    if interpolados:
        lim.append(f"nodos interpolados (forwards planos) a {interpolados} meses")
    ldf = [log_df(d) for d in cortes]
    n_dias = [cortes[k + 1] - cortes[k] for k in range(n_per)]
    d_T = cortes[-1]
    # (i) Fijar
    log_fijar = -ldf[-1]

    def tae(lg: float) -> float:
        return math.exp(lg * DIAS_ANIO / d_T) - 1

    # (ii) Renovar con forwards (expectativas puras) y escenarios
    fwd = [(math.exp(ldf[k] - ldf[k + 1]) - 1) * base / n_dias[k] for k in range(n_per)]
    sendas: dict[str, list[float]] = {}
    for pb in p["escenarios_pb"]:
        nombre = "base" if pb == 0 else f"{pb:+g}pb"
        sendas[nombre] = [f + _f(pb, "escenarios_pb") / PB for f in fwd]
    sendas["plana"] = [fwd[0]] * n_per
    for clave, nombre in (("senda_mon_exp", "mon_exp"), ("senda_encuesta", "encuesta")):
        if v.get(clave) is not None:
            s = [_f(x, f"{ficha}.{clave}") for x in _lista(v[clave], ficha)]
            if len(s) != n_per:
                raise ErrorFicha(f"{ficha}: {clave} con {len(s)} tipos; se esperan {n_per} (T/tau)")
            sendas[nombre] = s
    if "mon_exp" not in sendas:
        lim.append("sin senda de MON-EXP-001: holgura medida frente a los forwards de la curva")
    renovar = {}
    for nombre, s in sendas.items():
        lg = sum(math.log1p(r * n / base) for r, n in zip(s, n_dias))
        renovar[nombre] = {"tae": tae(lg), "diferencia_vs_fijar_pb": (tae(lg) - tae(log_fijar)) * PB,
                           "tipo_constante_equivalente": _tipo_constante(lg, n_dias, base, min(s), max(s))}
    # (iii) Punto muerto y holgura
    punto_muerto = _tipo_constante(log_fijar, n_dias, base, min(fwd), max(fwd))
    holgura = {k: (punto_muerto - r["tipo_constante_equivalente"]) * PB for k, r in renovar.items()}
    ref = "mon_exp" if "mon_exp" in sendas else "base"
    # (iv) Prima implícita frente a la encuesta
    prima = None
    if "encuesta" in sendas:
        prima = (punto_muerto - float(np.mean(sendas["encuesta"]))) * PB
    else:
        lim.append("sin senda de encuesta: prima implícita no calculada")
    # (v) Media ponderada si hay pesos
    media = None
    if v.get("pesos_escenarios") is not None:
        pesos = {k: _f(w, f"{ficha}.pesos_escenarios")
                 for k, w in _dict(v["pesos_escenarios"], f"{ficha}.pesos_escenarios").items()}
        if set(pesos) - set(renovar):
            raise ErrorFicha(f"{ficha}: pesos para escenarios inexistentes {sorted(set(pesos) - set(renovar))}")
        if any(w < 0 for w in pesos.values()) or abs(sum(pesos.values()) - 1) > FICHAS[ficha]["tol"]:
            raise ErrorFicha(f"{ficha}: los pesos de los escenarios deben ser no negativos y sumar 1")
        media = sum(w * renovar[k]["tae"] for k, w in sorted(pesos.items()))
    res = {
        "fijar": {"tae": tae(log_fijar), "tipo_simple": (math.exp(log_fijar) - 1) * base / d_T},
        "renovar": renovar,
        "forwards": fwd,
        "punto_muerto": punto_muerto,
        "holgura_pb": holgura,
        "holgura_senda_descontada_pb": holgura[ref],
        "prima_implicita_pb": prima,
        "media_ponderada_renovar_tae": media,
        "verificacion": {"renovar_forwards_menos_fijar_pb": renovar["base"]["diferencia_vs_fijar_pb"]},
        "unidades": {"tae": "tanto por uno", "tipos": f"simple Act/{base:g}", "*_pb": "pb"},
        "referencia_ingenua": "renovar al tipo vigente (RI-PA): escenario «plana»",
        "advertencias": [("bajo expectativas puras ambas estrategias rinden igual: la diferencia mide prima por plazo "
                          "o desacuerdo con el mercado"), "mismo segmento y riesgo emisor en ambos lados",
                         "riesgo de reinversión explícito"],
    }
    return res, lim


# ======================================================================= IDX-ERP-001
_BLOQUES_ERP = ("dividendo", "recompras_netas", "crecimiento_real_bpa", "inflacion", "cambio_valoracion")


def _erp_indice(ix: dict, p: dict, N: float, lam: float, lim: list[str]) -> dict[str, Any]:
    ficha = "IDX-ERP-001"
    nombre = str(_req(ix, "nombre", ficha))
    ctx = f"{ficha}[{nombre}]"
    divisa = str(_req(ix, "divisa", ctx))
    if _f(_req(ix, "nivel", ctx), f"{ctx}.nivel") <= 0:
        raise ErrorFicha(f"{ctx}: nivel no positivo")
    dy = _f(_req(ix, "rentabilidad_dividendo", ctx), f"{ctx}.rentabilidad_dividendo")
    if ix.get("recompras_netas") is not None:
        bb = _f(ix["recompras_netas"], f"{ctx}.recompras_netas")
    else:
        bb = _f(_req(ix, "recompras", ctx), ctx) - _f(_req(ix, "emisiones", ctx), ctx)
    # Crecimiento real del BPA: histórico ≥ 20 años (CAGR, FIN-CAGR-001) o consenso con fecha y fuente.
    if ix.get("historia_bpa_real") is not None:
        s = _serie(ix["historia_bpa_real"], "valor", f"{ctx}.historia_bpa_real")
        if len(s) < 2 or _anios(s.index) < p["anios_bpa_historico_min"]:
            raise ErrorFicha(f"{ctx}: historia del BPA real < {p['anios_bpa_historico_min']} años")
        g = cagr(float(s.iloc[0]), float(s.iloc[-1]), _anios(s.index))
    else:
        cg = _req(ix, "crecimiento_real_bpa", ctx)
        g = _con_fuente(cg, f"{ctx}.crecimiento_real_bpa")
        _fecha(_req(cg, "fecha", f"{ctx}.crecimiento_real_bpa"), ctx)
    pi_e = _con_fuente(_req(ix, "inflacion_esperada", ctx), f"{ctx}.inflacion_esperada")
    tipo_m = ix.get("tipo_multiplo")
    if tipo_m is not None and tipo_m != p["multiplo"]:
        raise ErrorFicha(f"{ctx}: múltiplo «{tipo_m}» distinto del pedido «{p['multiplo']}»")
    m_act = _f(_req(ix, "multiplo_actual", ctx), f"{ctx}.multiplo_actual")
    hist = _serie(_req(ix, "historia_multiplo", ctx), "valor", f"{ctx}.historia_multiplo")
    anios_h = _anios(hist.index) if len(hist) > 1 else 0.0
    if anios_h < p["anios_historia_min"]:
        raise ErrorFicha(f"{ctx}: historia del múltiplo de {anios_h:.2f} años (< {p['anios_historia_min']})")
    if anios_h < p["anios_historia_recomendados"]:
        lim.append(f"{nombre}: historia del múltiplo de {anios_h:.2f} años (< {p['anios_historia_recomendados']})")
    if m_act <= 0 or (hist <= 0).any():
        raise ErrorFicha(f"{ctx}: múltiplos no positivos")
    rf = _req(ix, "rf", ctx)
    rf_v = _f(_req(rf, "valor", f"{ctx}.rf"), f"{ctx}.rf")
    if rf.get("divisa") != divisa:
        raise ErrorFicha(f"{ctx}: r_f en {rf.get('divisa')} y el índice en {divisa}")
    if _f(_req(rf, "plazo_anios", f"{ctx}.rf"), f"{ctx}.rf.plazo_anios") != N:
        raise ErrorFicha(f"{ctx}: r_f a {rf['plazo_anios']} años; se pide a N = {N:g}")
    # (ii) múltiplo objetivo: mediana histórica con reversión parcial λ; (i) cambio anualizado de valoración
    mediana = float(np.median(hist.values))
    m_obj = m_act + lam * (mediana - m_act)
    dval = (m_obj / m_act) ** (1 / N) - 1
    bloques = {"dividendo": dy, "recompras_netas": bb, "crecimiento_real_bpa": g, "inflacion": pi_e,
               "cambio_valoracion": dval}
    er = sum(bloques[b] for b in _BLOQUES_ERP)
    # (iv) escenarios bajo/alto declarados por bloque
    escen = {"central": er}
    escenarios_in = ix.get("escenarios")
    escenarios_in = {} if escenarios_in is None else _dict(escenarios_in, f"{ctx}.escenarios")
    for nombre_e, sob in sorted(escenarios_in.items()):
        sob = _dict(sob, f"{ctx}.escenarios.{nombre_e}")
        desconocidos = set(sob) - set(_BLOQUES_ERP)
        if desconocidos:
            raise ErrorFicha(f"{ctx}: escenario «{nombre_e}» con bloques desconocidos {sorted(desconocidos)}")
        b2 = dict(bloques)
        b2.update({k: _f(x, f"{ctx}.escenarios.{nombre_e}.{k}") for k, x in sob.items()})
        escen[nombre_e] = sum(b2[b] for b in _BLOQUES_ERP)
    if len(escen) == 1:
        lim.append(f"{nombre}: sin escenarios declarados: rango no calculado")
    return {"nombre": nombre, "divisa": divisa, "bloques": bloques, "er_nominal": er,
            "er_real": er - pi_e, "prima_rf": er - rf_v, "rf": rf_v, "multiplo_actual": m_act,
            "multiplo_mediana": mediana, "multiplo_objetivo": m_obj,
            "percentil_multiplo": _posicion(m_act, hist.values),
            "escenarios": escen,
            "rango": {"min": min(escen.values()), "max": max(escen.values())} if len(escen) > 1 else None,
            "verificacion_suma_bloques": abs(sum(bloques.values()) - er),
            "segunda_via_rendimiento_beneficio": 1 / m_act,
            "supuesto_fx": ix.get("supuesto_fx")}


@_cerrado("IDX-ERP-001")
def f_idx_erp(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """IDX-ERP-001 · Rentabilidad esperada por índice (Grinold-Kroner).

    ``valores``: un índice o ``indices`` [índice, …] con ``divisa_comparacion`` y ``rf_comparacion`` {valor,
    plazo_anios, divisa}. Cada índice: nombre, divisa, nivel, rentabilidad_dividendo, recompras_netas (o recompras y
    emisiones), crecimiento_real_bpa {valor, fuente, fecha} o historia_bpa_real [{fecha, valor}] (≥ 20 años),
    inflacion_esperada {valor, fuente}, tipo_multiplo, multiplo_actual, historia_multiplo [{fecha, valor}],
    rf {valor, plazo_anios, divisa}, escenarios? {bajo|alto: {bloque: valor}}, supuesto_fx? {valor, fuente} (variación
    anual supuesta de la divisa del índice frente a la de comparación; para la comparación no cubierta).

    Identidad aditiva: E[R] = suma de bloques; real = E[R] − inflación esperada.
    """
    ficha = "IDX-ERP-001"
    p = _params(ficha, params)
    v = ent["valores"]
    lim: list[str] = []
    N = _en_rango(p, "N", ficha)
    lam = _en_rango(p, "lambda_reversion", ficha)
    if p["cobertura"] not in ("cubierta", "ambas"):
        raise ErrorFicha(f"{ficha}: cobertura «{p['cobertura']}» no admitida (cubierta o ambas)")
    indices = v["indices"] if v.get("indices") is not None else [v]
    if not isinstance(indices, list) or not all(isinstance(ix, dict) for ix in indices):
        raise ErrorFicha(f"{ficha}: «indices» debe ser una lista de dicts")
    filas = [_erp_indice(ix, p, N, lam, lim) for ix in _lista(indices, f"{ficha}: indices")]
    if len({f["nombre"] for f in filas}) != len(filas):
        raise ErrorFicha(f"{ficha}: índices con el mismo nombre")
    comparacion: dict[str, Any] | None = None
    if len(filas) > 1:
        divisa_c = v.get("divisa_comparacion")
        if not divisa_c:
            raise ErrorFicha(f"{ficha}: falta la divisa de comparación (se pide aclaración)")
        rf_c = 0.0
        if any(f["divisa"] != divisa_c for f in filas):
            rfc = _req(v, "rf_comparacion", ficha)
            if rfc.get("divisa") != divisa_c or _f(_req(rfc, "plazo_anios", ficha), ficha) != N:
                raise ErrorFicha(f"{ficha}: rf_comparacion debe estar en {divisa_c} y a N = {N:g} años")
            rf_c = _f(_req(rfc, "valor", ficha), f"{ficha}.rf_comparacion")
        er_c: dict[str, dict[str, float]] = {}
        for f in filas:
            cub = f["er_nominal"] if f["divisa"] == divisa_c else f["er_nominal"] + (rf_c - f["rf"])
            er_c[f["nombre"]] = {"cubierta": cub}
            if p["cobertura"] == "ambas":
                if f["divisa"] == divisa_c:
                    er_c[f["nombre"]]["no_cubierta"] = f["er_nominal"]
                else:
                    fx = _con_fuente(f["supuesto_fx"], f"{ficha}[{f['nombre']}].supuesto_fx")
                    er_c[f["nombre"]]["no_cubierta"] = (1 + f["er_nominal"]) * (1 + fx) - 1
        nombres = sorted(er_c)
        comparacion = {"divisa": divisa_c, "er_divisa_comun": er_c,
                       "diferencias": {f"{a} − {b}": {k: er_c[a][k] - er_c[b][k] for k in er_c[a]}
                                       for i, a in enumerate(nombres) for b in nombres[i + 1:]}}
        lim.append("las diferencias entre índices incorporan diferencias de composición sectorial "
                   "(declarar o combinar con IDX-REL-001)")
    res = {
        "indices": {f["nombre"]: f for f in filas},
        "bloques": {f["nombre"]: f["bloques"] for f in filas},
        "er_nominal": {f["nombre"]: f["er_nominal"] for f in filas},
        "er_real": {f["nombre"]: f["er_real"] for f in filas},
        "prima_rf": {f["nombre"]: f["prima_rf"] for f in filas},
        "rango_escenarios": {f["nombre"]: f["rango"] for f in filas},
        "diferencias_entre_indices": comparacion,
        "parametros": {"N": N, "lambda_reversion": lam, "multiplo": p["multiplo"], "cobertura": p["cobertura"]},
        "unidades": {"tipos": "tanto por uno anual (diferencias y prima: ×100 = pp)"},
        "referencia_ingenua": "RI-MH (rentabilidad histórica del índice y prima media histórica)",
        "advertencias": ["identidad aproximada, no previsión", "muy sensible al supuesto de reversión del múltiplo",
                         "el crecimiento del BPA del índice difiere del PIB", "útil en H4"],
    }
    return res, lim


# ======================================================================= IDX-CONC-001
def _pesos(comp: Any, ctx: str, tol: float) -> tuple[pd.Timestamp, dict[str, float], dict[str, str]]:
    if not isinstance(comp, dict) or comp.get("fecha") is None:
        raise ErrorFicha(f"{ctx}: composición sin fecha")
    fecha = _fecha(comp["fecha"], ctx)
    pesos: dict[str, float] = {}
    sectores: dict[str, str] = {}
    for i, c in enumerate(_lista(_req(comp, "componentes", ctx), f"{ctx}.componentes")):
        cid = str(_req(c, "id", f"{ctx}[{i}]"))
        if cid in pesos:
            raise ErrorFicha(f"{ctx}: componente repetido «{cid}»")
        w = _f(_req(c, "peso", f"{ctx}[{i}]"), f"{ctx}[{i}].peso")
        if w < 0:
            raise ErrorFicha(f"{ctx}: peso negativo en «{cid}»")
        pesos[cid] = w
        if c.get("sector") is not None:
            sectores[cid] = str(c["sector"])
    suma = sum(pesos.values())
    if abs(suma - 1) > tol:
        raise ErrorFicha(f"{ctx}: los pesos suman {suma!r}, no 1 (verificación de la ficha)")
    return fecha, pesos, sectores


def _hhi(pesos: dict[str, float]) -> float:
    return float(sum(w * w for w in pesos.values()))


@_cerrado("IDX-CONC-001")
def f_idx_conc(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """IDX-CONC-001 · Concentración y amplitud de un índice.

    ``valores``: ``composicion`` {fecha, componentes [{id, peso, sector?}]} (pesos en tanto por uno, sin
    supervivencia); opcionales: ``precios`` {id: [{fecha, precio}]} (o ``ent["series"]`` con alias = id) para la
    amplitud; ``indice_ponderado`` e ``indice_equiponderado`` [{fecha, valor}] (o los roles homónimos de
    ``ent["series_rol"]``); ``composicion_inicio`` y ``rentabilidades_periodo`` {id: r} para la contribución;
    ``historia_metricas`` [{fecha, peso_top_n, hhi, n_ef, hhi_sectorial?}] para los percentiles.
    """
    ficha = "IDX-CONC-001"
    p = _params(ficha, params)
    v = ent["valores"]
    lim: list[str] = []
    tol = FICHAS[ficha]["tol"]
    top_n = int(_en_rango(p, "top_n", ficha))
    if v.get("composicion") is None:
        raise ErrorFicha(f"{ficha}: sin composición fechada")
    fecha, pesos, sectores = _pesos(v["composicion"], f"{ficha}: composicion", tol)
    orden = sorted(pesos, key=lambda k: (-pesos[k], k))
    hhi = _hhi(pesos)
    conc: dict[str, Any] = {"peso_top_n": sum(pesos[k] for k in orden[:top_n]), "hhi": hhi, "n_ef": 1 / hhi,
                            "n_componentes": len(pesos), "hhi_sectorial": None}
    if len(pesos) < top_n:
        lim.append(f"índice con {len(pesos)} componentes (< top_n = {top_n})")
    if len(sectores) == len(pesos):
        por_sector: dict[str, float] = {}
        for k, w in pesos.items():
            por_sector[sectores[k]] = por_sector.get(sectores[k], 0.0) + w
        conc["hhi_sectorial"] = _hhi(por_sector)
        suma_sectores: float | None = sum(por_sector.values())
    else:
        suma_sectores = None
        lim.append("sector no informado para todos los componentes: HHI sectorial no calculado")

    # (ii) Amplitud
    precios: dict[str, pd.Series] = {}
    if v.get("precios"):
        precios = {k: _serie(s, "precio", f"{ficha}: precios[{k}]")
                   for k, s in sorted(_dict(v["precios"], f"{ficha}: precios").items())}
    elif ent.get("series"):
        precios = {str(k): s.dropna().sort_index() for k, s in sorted(ent["series"].items())}
    amplitud: dict[str, Any] | None = None
    if precios:
        n_media = int(p["media_amplitud"])
        sobre, validos = 0, 0
        for k, s in precios.items():
            if len(s) < 2 or _anios(s.index) < p["anios_precios_min"]:
                raise ErrorFicha(f"{ficha}: precios de «{k}» con menos de {p['anios_precios_min']} año")
            if len(s) >= n_media:
                validos += 1
                sobre += int(float(s.iloc[-1]) > float(s.iloc[-n_media:].mean()))
        if validos < len(precios):
            lim.append(f"{len(precios) - validos} componente(s) con < {n_media} sesiones: fuera de la amplitud")
        rend = pd.DataFrame({k: s.pct_change() for k, s in precios.items()}).iloc[1:]
        neto = (rend > 0).sum(axis=1) - (rend < 0).sum(axis=1)
        amplitud = {"porcentaje_sobre_media": sobre / validos if validos else None, "n_validos": validos,
                    "linea_avance_retroceso": float(neto.cumsum().iloc[-1]), "sesiones": len(neto)}
        if set(precios) != set(pesos):
            lim.append("los precios no cubren exactamente la composición: amplitud sobre los aportados")
    else:
        lim.append("sin precios de componentes: amplitud no calculada")

    def _idx(rol: str) -> pd.Series | None:
        if v.get(rol) is not None:
            return _serie(v[rol], "valor", f"{ficha}: {rol}")
        s = (ent.get("series_rol") or {}).get(rol)
        return None if s is None else s.dropna().sort_index()

    pond, equi = _idx("indice_ponderado"), _idx("indice_equiponderado")
    diferencial: dict[str, Any] | None = None
    if pond is not None and equi is not None:
        diferencial = {}
        for m in p["meses_diferencial"]:
            rs: list[float] = []
            for s in (pond, equi):
                previos = s[s.index <= s.index[-1] - pd.DateOffset(months=int(m))]
                if not previos.empty:
                    rs.append(float(s.iloc[-1]) / float(previos.iloc[-1]) - 1)
            if len(rs) < 2:
                lim.append(f"series del índice sin {m} meses: diferencial no calculado")
                diferencial[f"{m}m"] = None
            else:
                diferencial[f"{m}m"] = rs[0] - rs[1]
    else:
        lim.append("sin versiones ponderada y equiponderada del índice: diferencial no calculado")

    # (iii) Contribución de los n mayores (pesos al inicio del periodo)
    contribucion = None
    segunda_via = None
    if v.get("composicion_inicio") is not None:
        f0, w0, _ = _pesos(v["composicion_inicio"], f"{ficha}: composicion_inicio", tol)
        if f0 >= fecha:
            raise ErrorFicha(f"{ficha}: composicion_inicio no es anterior a la composición actual")
        union = sorted(set(w0) | set(pesos))
        segunda_via = {"hhi_pesos_medios": _hhi({k: (w0.get(k, 0.0) + pesos.get(k, 0.0)) / 2 for k in union}),
                       "hhi_cierre": hhi}
        rp = v.get("rentabilidades_periodo")
        if rp is not None:
            faltan = sorted(set(w0) - set(rp))
            if faltan:
                raise ErrorFicha(f"{ficha}: faltan rentabilidades del periodo de {faltan}")
            contrib = {k: w0[k] * _f(rp[k], f"{ficha}.rentabilidades_periodo[{k}]") for k in w0}
            total = sum(contrib.values())
            top0 = sorted(w0, key=lambda k: (-w0[k], k))[:top_n]
            contribucion = {"rentabilidad_indice": total, "contribucion_top_n": sum(contrib[k] for k in top0),
                            "porcentaje_top_n": sum(contrib[k] for k in top0) / total if total != 0 else None}
            if total == 0:
                lim.append("rentabilidad del periodo nula: porcentaje de contribución indefinido")
        else:
            lim.append("sin rentabilidades del periodo: contribución no calculada")
    else:
        lim.append("sin composición al inicio del periodo: contribución y segunda vía no calculadas")

    # (iv) Percentiles frente a ≥ 10 años (ventana 20)
    percentiles: dict[str, Any] | None = None
    if v.get("historia_metricas"):
        filas = _lista(v["historia_metricas"], f"{ficha}: historia_metricas")
        percentiles = {}
        for met in ("peso_top_n", "hhi", "n_ef", "hhi_sectorial"):
            if conc.get(met) is None or not all(isinstance(f, dict) and f.get(met) is not None for f in filas):
                percentiles[met] = None
                continue
            s = _serie(filas, met, f"{ficha}: historia_metricas")
            s = s[(s.index <= fecha) & (s.index >= fecha - pd.DateOffset(years=int(p["ventana_percentil_anios"])))]
            if len(s) < 2 or _anios(s.index) < p["ventana_percentil_min_anios"]:
                raise ErrorFicha(f"{ficha}: historia de {met} < {p['ventana_percentil_min_anios']} años")
            percentiles[met] = _posicion(conc[met], s.values)
    else:
        lim.append("sin historia de concentración: percentiles no calculados")
    res = {
        **conc,
        "amplitud": amplitud,
        "diferencial_ponderado_equiponderado": diferencial,
        "contribucion": contribucion,
        "percentiles": percentiles,
        "segunda_via": segunda_via,
        "fecha_composicion": fecha.date().isoformat(),
        "verificacion": {"suma_pesos": sum(pesos.values()), "suma_pesos_sectoriales": suma_sectores},
        "unidades": {"pesos": "tanto por uno", "n_ef": "componentes", "diferencial": "tanto por uno (×100 = pp)"},
        "referencia_ingenua": "RI-MH de la concentración; RI-NA para descriptivos",
        "advertencias": ["los componentes son datos de composición, nunca candidatos a selección (1.6)",
                         "la concentración describe el riesgo del índice, no es señal de tiempo",
                         "topes de peso y cambios metodológicos rompen la comparabilidad"],
    }
    return res, lim


# ======================================================================= IDX-REL-001
def _historia_indice(ix: Any, ctx: str) -> pd.DataFrame:
    """Historia mensual validada: cada fila un dict con ``fecha`` y campos numéricos finitos (o ausentes/None)."""
    filas = _lista(_req(_dict(ix, ctx), "historia", ctx), f"{ctx}.historia")
    fechas, limpias = [], []
    for i, fila in enumerate(filas):
        c = f"{ctx}.historia[{i}]"
        if not isinstance(fila, dict):
            raise ErrorFicha(f"{c}: se espera un dict")
        fechas.append(_fecha(_req(fila, "fecha", c), c))
        limpias.append({str(k): (np.nan if x is None else _f(x, f"{c}.{k}")) for k, x in fila.items() if k != "fecha"})
    df = pd.DataFrame(limpias, index=pd.DatetimeIndex(fechas), dtype=float)
    if df.index.has_duplicates:
        raise ErrorFicha(f"{ctx}: fechas repetidas")
    return df.sort_index()


def _comprobar_mensual(indice: pd.DatetimeIndex, ctx: str) -> None:
    """Cada observación, en el mes siguiente a la anterior (sin huecos ni varias por mes): la ficha pide historias
    mensuales y el momentum 12-1 y el devengo de la cobertura cuentan meses por filas."""
    meses = indice.year * MESES_ANIO + indice.month
    saltos = np.diff(np.asarray(meses))
    if len(saltos) and not (saltos == 1).all():
        malo = int(np.argmax(saltos != 1))
        raise ErrorFicha(f"{ctx}: la historia común no es mensual ({indice[malo].date()} → {indice[malo + 1].date()}); "
                         "aporte una observación por mes, sin huecos")


@_cerrado("IDX-REL-001")
def f_idx_rel(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """IDX-REL-001 · Valor relativo entre índices.

    ``valores``: ``indice_a`` e ``indice_b`` {nombre, divisa, historia [{fecha, <múltiplos>, rt, fx?,
    diferencial_cobertura?, revision_bpa_3m?}]} mensual; ``rt`` = índice de rentabilidad total en divisa local;
    ``fx`` = unidades de divisa común por unidad de divisa local; ``diferencial_cobertura`` = tipo de la divisa común −
    tipo local (anual, se devenga por meses). Opcionales: ``sectores`` {pesos_a {sector: w}, multiplos_b {múltiplo:
    {sector: m}}}; ``er_a`` y ``er_b`` {valor, fuente} (IDX-ERP-001).

    Recomposición sectorial de B con los pesos de A: media armónica para precio/beneficio (y precio/valor), media
    aritmética para la rentabilidad por dividendo («rd»).
    """
    ficha = "IDX-REL-001"
    p = _params(ficha, params)
    v = ent["valores"]
    lim: list[str] = []
    divisa_c = p.get("divisa_comun")
    if not divisa_c:
        raise ErrorFicha(f"{ficha}: sin divisa común declarada")
    if p["cobertura"] not in ("cubierta", "no_cubierta", "ambas"):
        raise ErrorFicha(f"{ficha}: cobertura «{p['cobertura']}» no admitida")
    ia, ib = _dict(_req(v, "indice_a", ficha), ficha), _dict(_req(v, "indice_b", ficha), ficha)
    da, db = _historia_indice(ia, f"{ficha}: indice_a"), _historia_indice(ib, f"{ficha}: indice_b")
    comun = da.index.intersection(db.index)
    if len(comun) < 2:
        raise ErrorFicha(f"{ficha}: historias sin fechas comunes")
    fin = comun[-1]
    comun = comun[comun >= fin - pd.DateOffset(years=int(p["ventana_anios"]))]
    da, db = da.loc[comun], db.loc[comun]
    _comprobar_mensual(comun, ficha)
    anios = _anios(comun)
    if anios < p["anios_min"]:
        raise ErrorFicha(f"{ficha}: historia común de {anios:.2f} años (< {p['anios_min']})")
    if anios < p["anios_recomendados"]:
        lim.append(f"historia común de {anios:.2f} años (< {p['anios_recomendados']}): z y percentiles orientativos")
    # (i) Brechas de múltiplos
    brechas: dict[str, Any] = {}
    for m in p["multiplos"]:
        if m not in da or m not in db or da[m].isna().any() or db[m].isna().any():
            raise ErrorFicha(f"{ficha}: falta el múltiplo «{m}» en la historia de algún índice")
        a, b = da[m].astype(float), db[m].astype(float)
        if (a <= 0).any() or (b <= 0).any():
            raise ErrorFicha(f"{ficha}: múltiplo «{m}» no positivo")
        lr = np.log(a.values / b.values)
        pos = _posicion(float(lr[-1]), lr)
        if pos["z"] is None:
            lim.append(f"{m}: dispersión nula de la brecha: z indefinido")
        brechas[m] = {"ratio": float(a.iloc[-1] / b.iloc[-1]), "brecha": float(a.iloc[-1] / b.iloc[-1] - 1),
                      "log_ratio": float(lr[-1]), "z": pos["z"], "percentil": pos["percentil"], "n": pos["n"]}
    # (ii) Ajuste por composición sectorial
    neutral: dict[str, Any] | None = None
    if p["ajuste_sectorial"] and v.get("sectores"):
        sec = _dict(v["sectores"], f"{ficha}.sectores")
        pesos_a = {k: _f(w, f"{ficha}.sectores.pesos_a")
                   for k, w in _dict(_req(sec, "pesos_a", ficha), f"{ficha}.sectores.pesos_a").items()}
        if abs(sum(pesos_a.values()) - 1) > FICHAS[ficha]["tol"] or any(w < 0 for w in pesos_a.values()):
            raise ErrorFicha(f"{ficha}: los pesos sectoriales de A deben ser no negativos y sumar 1")
        neutral = {}
        for m, mult_b in sorted(_dict(_req(sec, "multiplos_b", ficha), f"{ficha}.sectores.multiplos_b").items()):
            if m not in brechas:
                continue
            mult_b = _dict(mult_b, f"{ficha}.sectores.multiplos_b.{m}")
            faltan = sorted(set(pesos_a) - set(mult_b))
            if faltan:
                raise ErrorFicha(f"{ficha}: faltan múltiplos sectoriales de B para {faltan}")
            mb = {k: _f(mult_b[k], f"{ficha}.sectores.multiplos_b") for k in pesos_a}
            if any(x <= 0 for x in mb.values()):
                raise ErrorFicha(f"{ficha}: múltiplo sectorial no positivo")
            if m == "rd":
                recompuesto = sum(pesos_a[k] * mb[k] for k in pesos_a)
            else:
                recompuesto = 1 / sum(pesos_a[k] / mb[k] for k in pesos_a)
            neutral[m] = {"multiplo_b_recompuesto": recompuesto,
                          "brecha_neutral": float(da[m].iloc[-1]) / recompuesto - 1}
    elif p["ajuste_sectorial"]:
        lim.append("sin pesos y múltiplos sectoriales: brecha neutral sectorial no calculada")
    # (iii) Diferencia de E[R]
    dif_er = None
    if v.get("er_a") is not None and v.get("er_b") is not None:
        dif_er = _con_fuente(v["er_a"], f"{ficha}.er_a") - _con_fuente(v["er_b"], f"{ficha}.er_b")
    else:
        lim.append("sin E[R] de IDX-ERP-001: diferencia no calculada")
    # (iv) Momentum relativo en divisa común
    modos = ["cubierta", "no_cubierta"] if p["cobertura"] == "ambas" else [p["cobertura"]]
    momentum: dict[str, Any] = {}
    for modo in modos:
        tr = []
        for d, ix, nom in ((da, ia, "indice_a"), (db, ib, "indice_b")):
            if "rt" not in d or d["rt"].isna().any():
                raise ErrorFicha(f"{ficha}: falta la rentabilidad total («rt») de {nom}")
            local = d["rt"].astype(float)
            if ix.get("divisa") == divisa_c:
                tr.append(local)
                continue
            if not ix.get("divisa"):
                raise ErrorFicha(f"{ficha}: {nom} sin divisa declarada")
            col = "fx" if modo == "no_cubierta" else "diferencial_cobertura"
            if col not in d or d[col].isna().any():
                raise ErrorFicha(f"{ficha}: {nom} en {ix['divisa']} sin «{col}» para pasar a {divisa_c} ({modo})")
            if modo == "no_cubierta":
                tr.append(local * d["fx"].astype(float))
            else:
                acarreo = (1 + d["diferencial_cobertura"].astype(float).shift(1).fillna(0.0) / MESES_ANIO).cumprod()
                tr.append(local * acarreo)
        r = (tr[0] / tr[1]).values
        retro, salto, corto = (int(p["momentum_retro_meses"]), int(p["momentum_salto_meses"]),
                               int(p["momentum_corto_meses"]))
        if len(r) <= retro:
            raise ErrorFicha(f"{ficha}: historia insuficiente para el momentum {retro}-{salto}")
        momentum[modo] = {f"{retro}-{salto}": float(r[-1 - salto] / r[-1 - retro] - 1),
                          f"{corto}m": float(r[-1] / r[-1 - corto] - 1)}
    # (v) Diferencial de revisiones de BPA a 3 meses
    revisiones = None
    if ("revision_bpa_3m" in da and "revision_bpa_3m" in db
            and pd.notna(da["revision_bpa_3m"].iloc[-1]) and pd.notna(db["revision_bpa_3m"].iloc[-1])):
        revisiones = float(da["revision_bpa_3m"].iloc[-1]) - float(db["revision_bpa_3m"].iloc[-1])
    else:
        lim.append("sin revisiones de BPA a 3 meses: diferencial no calculado")
    res = {
        "brechas": brechas,
        "z_scores": {m: b["z"] for m, b in brechas.items()},
        "percentiles": {m: b["percentil"] for m, b in brechas.items()},
        "brecha_neutral_sectorial": neutral,
        "diferencia_er": dif_er,
        "momentum_relativo": momentum,
        "diferencial_revisiones": revisiones,
        "segunda_via": {"multiplos": sorted(brechas), "nota": "brecha con cada múltiplo alternativo pedido"},
        "anios_historia": anios, "divisa_comun": divisa_c,
        "unidades": {"brecha": "tanto por uno", "log_ratio": "log", "diferencias": "tanto por uno (×100 = pp)"},
        "referencia_ingenua": "RI-MH de la brecha y RI-PA del ratio de precios",
        "advertencias": ["las brechas entre regiones pueden persistir", "la valoración relativa no es señal de tiempo en H2",
                         "la divisa puede dominar el resultado"],
    }
    return res, lim


# ======================================================================= IDX-REB-001
def _car_evento(ev: dict, p: dict, modelo: str, ctx: str) -> dict[str, Any] | None:
    """CAR de un evento en las dos ventanas, con su desviación de estimación; None si faltan sesiones."""
    rents = _lista(_req(ev, "rentabilidades", ctx), f"{ctx}.rentabilidades")
    fechas = pd.DatetimeIndex([_fecha(_req(r, "fecha", ctx), ctx) for r in rents])
    rc = np.array([_f(_req(r, "cesta", ctx), f"{ctx}.cesta") for r in rents])
    rm = np.array([_f(_req(r, "indice", ctx), f"{ctx}.indice") for r in rents])
    orden = np.argsort(fechas.values, kind="stable")
    fechas, rc, rm = fechas[orden], rc[orden], rm[orden]
    if fechas.has_duplicates:
        raise ErrorFicha(f"{ctx}: sesiones repetidas")
    anuncio = _fecha(_req(ev, "fecha_anuncio", ctx), ctx)
    efect = _fecha(_req(ev, "fecha_efectividad", ctx), ctx)
    if efect < anuncio:
        raise ErrorFicha(f"{ctx}: efectividad anterior al anuncio")
    ia = int(np.searchsorted(fechas.values, anuncio.to_datetime64()))
    ie = int(np.searchsorted(fechas.values, efect.to_datetime64()))
    n_est, n_post = int(p["sesiones_estimacion"]), int(p["ventana_post_sesiones"])
    if ia < n_est or ie + n_post >= len(fechas) or ie >= len(fechas):
        return None
    ec, em = rc[ia - n_est:ia], rm[ia - n_est:ia]
    if modelo == "indice_mercado":
        alfa, beta, gl = 0.0, 1.0, n_est - 1
    else:
        var_m = float(np.var(em, ddof=1))
        if var_m <= 0:
            raise ErrorFicha(f"{ctx}: varianza del índice nula en la estimación")
        beta = float(np.cov(ec, em, ddof=1)[0, 1]) / var_m
        alfa, gl = float(np.mean(ec) - beta * np.mean(em)), n_est - 2
    resid = ec - alfa - beta * em
    sigma = math.sqrt(float(np.sum((resid - np.mean(resid)) ** 2)) / gl)
    ar = rc - alfa - beta * rm
    v1 = ar[ia:ie + 1]                       # anuncio → efectividad (ambas incluidas)
    v2 = ar[ie + 1:ie + 1 + n_post]          # efectividad → +20 sesiones
    return {"car_1": float(v1.sum()), "car_2": float(v2.sum()), "l_1": len(v1), "l_2": len(v2), "sigma": sigma,
            "anio": efect}


def _estudio(cars: list[dict[str, Any]], p: dict, lim: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    t0 = min(c["anio"] for c in cars)
    x = np.array([(c["anio"] - t0).days / DIAS_ANIO for c in cars])
    for w in ("1", "2"):
        car = np.array([c[f"car_{w}"] for c in cars])
        sig = np.array([c["sigma"] * math.sqrt(c[f"l_{w}"]) for c in cars])
        n = len(car)
        fila: dict[str, Any] = {"car_medio": float(np.mean(car)), "car_mediano": float(np.median(car)), "n": n}
        if (sig > 0).all():
            scar = car / sig
            sd = float(np.std(scar, ddof=1))
            t_bmp = float(np.mean(scar) * math.sqrt(n) / sd) if sd > 0 else None
            fila["t_bmp"] = t_bmp
            fila["p_valor_bmp"] = None if t_bmp is None else float(2 * stats.t.sf(abs(t_bmp), n - 1))
        else:
            fila["t_bmp"] = fila["p_valor_bmp"] = None
            lim.append("desviación de estimación nula en algún evento: contraste BMP no calculado")
        if p.get("nivel_ic") is not None:
            nivel = _f(p["nivel_ic"], "nivel_ic")
            if not 0 < nivel < 1:
                raise ErrorFicha("IDX-REB-001: nivel_ic fuera de (0, 1)")
            ee = float(np.std(car, ddof=1)) / math.sqrt(n)
            q = float(stats.t.ppf((1 + nivel) / 2, n - 1))
            fila["ic"] = {"nivel": nivel, "inf": fila["car_medio"] - q * ee, "sup": fila["car_medio"] + q * ee}
        else:
            fila["ic"] = None
        # Tendencia temporal del efecto: pendiente MCO del CAR sobre el año del evento, por década.
        fila["tendencia_por_decada"] = (float(np.polyfit(x, car, 1)[0]) * ANIOS_DECADA
                                        if float(np.ptp(x)) > 0 else None)
        out["anuncio_efectividad" if w == "1" else "efectividad_post"] = fila
    return out


@_cerrado("IDX-REB-001")
def f_idx_reb(ent: dict, params: dict) -> tuple[dict, list[str]]:
    """IDX-REB-001 · Efecto de rebalanceo y cambios de composición.

    ``valores``: ``evento`` {fecha_anuncio, fecha_efectividad, cambios [{id, delta_peso, volumen_medio}],
    activos_indexados {valor, fuente, fecha}, flujos_declarados?}; ``eventos_comparables`` [{id, fecha_anuncio,
    fecha_efectividad, rentabilidades [{fecha, cesta, indice}]}] con ≥ 250 sesiones antes del anuncio y 20 tras la
    efectividad; ``proximo_evento`` (opcional) {fecha_anuncio, fecha_efectividad}. Parámetro opcional ``nivel_ic``
    (la ficha no fija el nivel; sin él no se entrega IC).

    Ventanas: [anuncio, efectividad] y las 20 sesiones siguientes a la efectividad. BMP sin corrección por error de
    predicción: SCAR = CAR/(σ_est·√L).
    """
    ficha = "IDX-REB-001"
    p = _params(ficha, params)
    v = ent["valores"]
    lim: list[str] = []
    tol = FICHAS[ficha]["tol"]
    modelo = p["modelo_normal"]
    if modelo not in ("indice_mercado", "modelo_mercado"):
        raise ErrorFicha(f"{ficha}: modelo_normal «{modelo}» no admitido")
    if p["contraste"] != "BMP":
        raise ErrorFicha(f"{ficha}: contraste «{p['contraste']}» no implementado (BMP)")
    ev = _req(v, "evento", ficha)
    an = _fecha(_req(ev, "fecha_anuncio", f"{ficha}.evento"), ficha)
    ef = _fecha(_req(ev, "fecha_efectividad", f"{ficha}.evento"), ficha)
    if ef < an:
        raise ErrorFicha(f"{ficha}: efectividad anterior al anuncio")
    aum_d = _req(ev, "activos_indexados", f"{ficha}.evento")
    aum = _con_fuente(aum_d, f"{ficha}.activos_indexados")
    _fecha(_req(aum_d, "fecha", f"{ficha}.activos_indexados"), ficha)
    if aum <= 0:
        raise ErrorFicha(f"{ficha}: activos indexados no positivos")
    cambios = _lista(_req(ev, "cambios", f"{ficha}.evento"), f"{ficha}.cambios")
    filas, suma = {}, 0.0
    for i, c in enumerate(cambios):
        ctx = f"{ficha}.cambios[{i}]"
        cid = str(_req(c, "id", ctx))
        dw = _f(_req(c, "delta_peso", ctx), f"{ctx}.delta_peso")
        vol = _f(_req(c, "volumen_medio", ctx), f"{ctx}.volumen_medio")
        if vol <= 0:
            raise ErrorFicha(f"{ctx}: volumen medio no positivo")
        if cid in filas:
            raise ErrorFicha(f"{ctx}: componente repetido")
        suma += dw
        filas[cid] = {"delta_peso": dw, "demanda": dw * aum, "dias_volumen": dw * aum / vol, "volumen_medio": vol}
    flujos = _f(ev.get("flujos_declarados", 0.0), f"{ficha}.flujos_declarados")
    if abs(suma - flujos) > tol:
        raise ErrorFicha(f"{ficha}: la suma de cambios de peso ({suma!r}) no es 0 ni los flujos declarados ({flujos!r})")
    demanda: dict[str, Any] = {}
    for nombre, sel in (("inclusiones", [f for f in filas.values() if f["delta_peso"] > 0]),
                        ("exclusiones", [f for f in filas.values() if f["delta_peso"] < 0])):
        dem = sum(f["demanda"] for f in sel)
        vol = sum(f["volumen_medio"] for f in sel)
        demanda[nombre] = {"demanda": dem, "dias_volumen_cesta": dem / vol if vol else None, "n": len(sel)}
    # (ii) Estudio de eventos
    comparables = v.get("eventos_comparables")
    comparables = [] if comparables is None else _lista(comparables, f"{ficha}: eventos_comparables")
    estudio, segunda = None, None
    if len(comparables) < p["eventos_min"]:
        lim.append(f"{len(comparables)} eventos comparables (< {p['eventos_min']}): solo la demanda estimada, "
                   "sin estudio de eventos")
    else:
        alterno = "modelo_mercado" if modelo == "indice_mercado" else "indice_mercado"
        cars, cars_alt, fuera = [], [], 0
        for i, e in enumerate(comparables):
            ctx = f"{ficha}.eventos_comparables[{i}]"
            c, ca = _car_evento(e, p, modelo, ctx), _car_evento(e, p, alterno, ctx)
            if c is None or ca is None:
                fuera += 1
                continue
            cars.append(c)
            cars_alt.append(ca)
        if fuera:
            lim.append(f"{fuera} evento(s) sin {p['sesiones_estimacion']} sesiones de estimación o "
                       f"{p['ventana_post_sesiones']} posteriores: excluidos")
        if len(cars) < p["eventos_min"]:
            lim.append(f"{len(cars)} eventos utilizables (< {p['eventos_min']}): sin estudio de eventos")
        else:
            estudio = {"modelo": modelo, **_estudio(cars, p, lim)}
            segunda = {"modelo": alterno, **_estudio(cars_alt, p, [])}
            if p.get("nivel_ic") is None:
                lim.append("IC no entregado: la ficha no fija el nivel (pasar el parámetro nivel_ic)")
    proximo = None
    if v.get("proximo_evento"):
        pe = v["proximo_evento"]
        proximo = {k: _fecha(_req(pe, k, f"{ficha}.proximo_evento"), ficha).date().isoformat()
                   for k in ("fecha_anuncio", "fecha_efectividad")}
    res = {
        "demanda_estimada": demanda,
        "por_componente": filas,
        "estudio_eventos": estudio,
        "segunda_via": segunda,
        "n_eventos": len(comparables),
        "calendario_proximo_evento": proximo,
        "verificacion": {"suma_cambios_peso": suma, "flujos_declarados": flujos},
        "unidades": {"demanda": "moneda de los activos indexados", "dias_volumen": "días de volumen medio",
                     "car": "tanto por uno (×100 = %)", "tendencia_por_decada": "tanto por uno por década"},
        "referencia_ingenua": "CAR nulo; RI-TB para dirección",
        "advertencias": ["activos indexados estimados", "los arbitrajistas anticipan; efecto en declive documentado",
                         "describe la cesta del evento, nunca selecciona valores afectados (1.6)"],
    }
    return res, lim


# ======================================================================= registro de fichas
FICHAS: dict[str, dict[str, Any]] = {
    "MON-YLD-001": {"fn": f_mon_yld, "modulo": "MC-01", "version": "1.0", "cifra": "DETERMINISTA", "ri": "RI-PA",
                    "tol": 1e-10},
    "MON-EXP-001": {"fn": f_mon_exp, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA", "ri": "RI-PA",
                    "tol": 1e-10},
    "MON-REAL-001": {"fn": f_mon_real, "modulo": "MC-01", "version": "1.0", "cifra": "DETERMINISTA", "ri": "RI-MH",
                     "tol": 1e-10},
    "MON-FIX-001": {"fn": f_mon_fix, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA", "ri": "RI-PA",
                    "tol": 1e-10},
    "IDX-ERP-001": {"fn": f_idx_erp, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA", "ri": "RI-MH",
                    "tol": 1e-10},
    "IDX-CONC-001": {"fn": f_idx_conc, "modulo": "MC-01", "version": "1.0", "cifra": "DETERMINISTA", "ri": "RI-MH",
                     "tol": 1e-10},
    "IDX-REL-001": {"fn": f_idx_rel, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-MH",
                    "tol": 1e-8},
    "IDX-REB-001": {"fn": f_idx_reb, "modulo": "MC-03", "version": "1.0", "cifra": "ESTADISTICA", "ri": "RI-TB",
                    "tol": 1e-8},
}


# ======================================================================= datos sintéticos de los casos de control
def _fechas_mensuales(n: int, inicio: str = "2005-01-31") -> list[str]:
    return [d.date().isoformat() for d in pd.date_range(inicio, periods=n, freq="ME")]


def _segmentos_ida_vuelta() -> list[dict]:
    base = {"divisa": "EUR", "plazo_meses": 3, "dias": 91, "fecha": "2026-11-10"}
    return [{**base, "segmento": "letras", "convencion": "descuento_360", "valor": 0.0285},
            {**base, "segmento": "pagares", "convencion": "simple_360", "valor": 0.0310},
            {**base, "segmento": "depositos", "convencion": "simple_365", "valor": 0.0300},
            {**base, "segmento": "repos", "convencion": "tae", "valor": 0.0290},
            {**base, "segmento": "certificados", "convencion": "precio", "valor": 0.9925}]


def _curva_on(r_on: float, base: float, dias: list[int]) -> list[dict]:
    """Curva OIS coherente con un tipo a un día constante capitalizado a diario."""
    return [{"dias": d, "tipo": math.expm1(d * math.log1p(r_on / base)) * base / d} for d in dias]


def _curva_senda(cortes: list[int], tasas: list[float], dias: list[int], base: float) -> list[dict]:
    """Curva OIS coherente con una senda escalonada de tipo a un día (tramo k = [cortes[k], cortes[k+1]))."""
    out = []
    for d in dias:
        lg = sum((min(b, d) - a) * math.log1p(r / base)
                 for a, b, r in zip(cortes, cortes[1:] + [d], tasas, strict=True) if a < d)
        out.append({"dias": d, "tipo": math.expm1(lg) * base / d})
    return out


# Senda del caso de control: bajada, bajada, pausa, bajada (25 pb); nodos que no caen en reuniones, uno antes de la
# primera y otro de más en el último tramo (sistema sobredeterminado y coherente).
_SENDA_EXP: dict[str, Any] = {
    "fecha": "2026-11-12", "reuniones": ["2026-12-17", "2027-02-04", "2027-04-29", "2027-07-22"],
    "cortes": [0, 35, 84, 168, 252], "tasas": [0.0192, 0.0167, 0.0142, 0.0142, 0.0117],
    "dias": [30, 60, 120, 200, 300, 365], "en_reunion": [-1.0, -1.0, 0.0, -1.0], "acumulados": [-1.0, -2.0, -2.0, -3.0]}


def _datos_mon_exp(plana: bool) -> dict:
    e = _SENDA_EXP
    tasas = [e["tasas"][0]] * len(e["tasas"]) if plana else e["tasas"]
    return {"fecha": e["fecha"], "base_curva": BASE_360, "curva": _curva_senda(e["cortes"], tasas, e["dias"], BASE_360),
            "tipo_oficial": 0.0200, "diferencial_estable": 0.0008, "reuniones": list(e["reuniones"])}


def _datos_mon_yld_cubierto() -> dict:
    base = {"plazo_meses": 3, "dias": 91, "fecha": "2026-11-10", "convencion": "simple_360"}
    return {"segmentos": [{**base, "segmento": "letras_usd", "divisa": "USD", "valor": 0.04},
                          {**base, "segmento": "letras", "divisa": "EUR", "valor": 0.02}],
            "cobertura": {"divisa_destino": "EUR",
                          "segmentos": {"letras_usd · USD · 3m": {"spot": 1.10, "forward": 1.105}}}}


def _tae_plana_mon_fix(tipo: float) -> float:
    """TAE de renovar 4 trimestres al tipo `tipo` (Act/360) desde la fecha del caso de MON-FIX-001."""
    fecha = pd.Timestamp("2026-11-12")
    cortes = [_dias_meses(fecha, 3 * k) for k in range(5)]
    bruto = math.prod(1 + tipo * (b - a) / BASE_360 for a, b in pairwise(cortes))
    return bruto ** (DIAS_ANIO / cortes[-1]) - 1


def _datos_mon_real(pi_cero: bool) -> dict:
    historia = []
    ini = pd.Timestamp("2014-01-01")
    ipc = 100.0
    for k in range(48):
        fin = ini + pd.DateOffset(months=3)
        ipc_fin = ipc if pi_cero else ipc * (1.004 + 0.001 * (k % 3))
        historia.append({"fecha_inicio": ini.date().isoformat(), "fecha_fin": fin.date().isoformat(),
                         "tipo_nominal": 0.01 + 0.0005 * (k % 5), "base": BASE_360, "ipc_inicio": ipc,
                         "ipc_fin": ipc_fin, "vintage_inicio": "2026-10-15", "vintage_fin": "2026-10-15"})
        ini, ipc = fin, ipc_fin
    return {"divisas": {"EUR": {"tipo_nominal": 0.021,
                                "expectativa_inflacion": {"valor": 0.0 if pi_cero else 0.019, "fuente": "sintética",
                                                          "tipo": "swap_1a"},
                                "fuente_ipc": "sintética", "historia": historia}}}


def _datos_mon_fix(plana: bool) -> dict:
    fecha = pd.Timestamp("2026-11-12")
    if plana:
        f, curva, acum = 0.025, [], 1.0
        for m in (3, 6, 9, 12):
            d0, d1 = _dias_meses(fecha, m - 3), _dias_meses(fecha, m)
            acum *= 1 + f * (d1 - d0) / BASE_360
            curva.append({"plazo_meses": m, "tipo": (acum - 1) * BASE_360 / d1, "base": BASE_360})
    else:
        curva = [{"plazo_meses": m, "tipo": y, "base": BASE_360}
                 for m, y in ((3, 0.0200), (6, 0.0195), (9, 0.0188), (12, 0.0181))]
    return {"fecha": fecha.date().isoformat(), "curva": curva}


def _datos_idx_erp(gordon: bool, mediana: float | None = None) -> dict:
    fechas = _fechas_mensuales(12 * 25)
    hist = [{"fecha": f, "valor": 20 + 5 * math.sin(i / 17) if mediana is None else mediana}
            for i, f in enumerate(fechas)]
    return {"nombre": "IDX-SINT", "divisa": "EUR", "nivel": 4000, "rentabilidad_dividendo": 0.03,
            "recompras_netas": 0.0 if gordon else 0.01,
            "crecimiento_real_bpa": {"valor": 0.015, "fuente": "sintética", "fecha": "2026-11-01"},
            "inflacion_esperada": {"valor": 0.02, "fuente": "sintética"}, "tipo_multiplo": "CAPE",
            "multiplo_actual": 28.0, "historia_multiplo": hist,
            "rf": {"valor": 0.027, "plazo_anios": 10, "divisa": "EUR"},
            "escenarios": {"bajo": {"crecimiento_real_bpa": 0.005}, "alto": {"crecimiento_real_bpa": 0.025}}}


def _composicion(n: int, igual: bool) -> dict:
    if igual:
        pesos = [1 / n] * n
    else:
        brutos = [float(n - i) for i in range(n)]
        pesos = [b / sum(brutos) for b in brutos]
    return {"fecha": "2026-10-31",
            "componentes": [{"id": f"C{i:02d}", "peso": w, "sector": f"S{i % 4}"} for i, w in enumerate(pesos)]}


def _datos_idx_rel(mismo: bool, escala_b: float = 1.0) -> dict:
    fechas = _fechas_mensuales(12 * 16)

    def hist(escala: float, fase: float) -> list[dict]:
        return [{"fecha": f, "per_adelantado": escala * (15 + 2 * math.sin(i / 9 + fase)),
                 "cape": escala * (25 + 3 * math.cos(i / 11 + fase)), "rt": 100 * (1.006 + 0.001 * fase) ** i}
                for i, f in enumerate(fechas)]

    a = {"nombre": "A", "divisa": "EUR", "historia": hist(1.0, 0.0)}
    b = a if mismo else {"nombre": "B", "divisa": "EUR", "historia": hist(escala_b, 0.0 if escala_b != 1.0 else 0.5)}
    return {"indice_a": a, "indice_b": b}


def _eventos_sinteticos(n: int) -> tuple[list[dict], list[float], list[float]]:
    """Eventos con AR plantada solo en las ventanas; en la estimación cesta = índice + ruido ortogonal de media 0."""
    eventos, car1, car2 = [], [], []
    patron_m, patron_e = (0.01, 0.01, -0.01, -0.01), (0.002, -0.002, -0.002, 0.002)
    for k in range(n):
        fechas = pd.bdate_range(f"{2000 + k}-01-03", periods=250 + 6 + 20)
        ar1, ar2 = 0.002 * (1 + k / n), -0.0005 * (1 + k / n)
        rents = []
        for t, f in enumerate(fechas):
            m = patron_m[t % 4] + (0.003 if t >= 250 else 0.0)
            c = m + (patron_e[t % 4] if t < 250 else ar1 if t <= 255 else ar2)
            rents.append({"fecha": f.date().isoformat(), "cesta": c, "indice": m})
        eventos.append({"id": f"E{k:02d}", "fecha_anuncio": fechas[250].date().isoformat(),
                        "fecha_efectividad": fechas[255].date().isoformat(), "rentabilidades": rents})
        car1.append(6 * ar1)
        car2.append(20 * ar2)
    return eventos, car1, car2


def _evento_reb(flujos: float | None = None, cambios: list[tuple[str, float, float]] | None = None) -> dict:
    ev: dict[str, Any] = {"fecha_anuncio": "2026-11-20", "fecha_efectividad": "2026-12-18",
                          "activos_indexados": {"valor": 1e12, "fuente": "sintética", "fecha": "2026-11-01"},
                          "cambios": [{"id": i, "delta_peso": w, "volumen_medio": vol}
                                      for i, w, vol in (cambios or [("IN", 0.001, 5e8), ("OUT", -0.001, 2e8)])]}
    if flujos is not None:
        ev["flujos_declarados"] = flujos
    return ev


_EV, _CAR1, _CAR2 = _eventos_sinteticos(PARAMETROS_POR_DEFECTO["IDX-REB-001"]["eventos_min"])


def _cerca(a: Any, b: float, tol: float) -> bool:
    return a is not None and abs(float(a) - b) <= tol


def _rel(a: Any, b: float, tol: float) -> bool:
    """Igualdad con la tolerancia relativa de la ficha (3.2)."""
    return a is not None and abs(float(a) - b) <= tol * abs(b)


# Cada caso: una frase comprobable de «Verificación» de la ficha (o una identidad derivada del «Método»).
CASOS_CONTROL: dict[str, list[dict[str, Any]]] = {
    "MON-YLD-001": [
        {"nombre": "ida y vuelta de cada conversión = identidad",
         "datos": [{"valores": {"segmentos": _segmentos_ida_vuelta()}}], "parametros": {},
         "comprobar": lambda r: r["verificacion"]["error_ida_vuelta_max"] <= FICHAS["MON-YLD-001"]["tol"]},
        {"nombre": "t = 365 en base 365 ⇒ simple = TAE",
         "datos": [{"valores": {"segmentos": [{"segmento": "depositos", "divisa": "EUR", "plazo_meses": 12,
                                               "dias": 365, "fecha": "2026-11-10", "convencion": "simple_365",
                                               "valor": 0.031}]}}],
         "parametros": {},
         "comprobar": lambda r: all(_cerca(f["simple_365"], f["tae"], FICHAS["MON-YLD-001"]["tol"])
                                    and _cerca(f["tae"], 0.031, FICHAS["MON-YLD-001"]["tol"])
                                    for f in r["tabla"].values())},
        {"nombre": "método (i): descuento d → P = 1 − d·t/360 → simple Act/365 y TAE",
         "datos": [{"valores": {"segmentos": [{"segmento": "letras", "divisa": "EUR", "plazo_meses": 3, "dias": 90,
                                               "fecha": "2026-11-10", "convencion": "descuento_360",
                                               "valor": 0.03}]}}],
         "parametros": {},
         "comprobar": lambda r: _rel(r["tabla"]["letras · EUR · 3m"]["precio"], 1 - 0.03 * 90 / BASE_360,
                                     FICHAS["MON-YLD-001"]["tol"])
         and _rel(r["tabla"]["letras · EUR · 3m"]["simple_365"], (1 / (1 - 0.03 * 90 / BASE_360) - 1) * DIAS_ANIO / 90,
                  FICHAS["MON-YLD-001"]["tol"])
         and _rel(r["tabla"]["letras · EUR · 3m"]["tae"], (1 - 0.03 * 90 / BASE_360) ** (-DIAS_ANIO / 90) - 1,
                  FICHAS["MON-YLD-001"]["tol"])},
        {"nombre": "método (iii): rendimiento cubierto = (1 + i_ext·t/base_ext)·(S/F) − 1",
         "datos": [{"valores": _datos_mon_yld_cubierto()}], "parametros": {"cobertura": True},
         "comprobar": lambda r: _rel(r["rendimiento_cubierto"]["letras_usd · USD · 3m"]["rendimiento_periodo"],
                                     (1 + 0.04 * 91 / BASE_360) * (1.10 / 1.105) - 1, FICHAS["MON-YLD-001"]["tol"])},
    ],
    "MON-EXP-001": [
        {"nombre": "curva plana al tipo vigente ⇒ probabilidad de movimiento 0",
         "datos": [{"valores": _datos_mon_exp(plana=True)}], "parametros": {},
         "comprobar": lambda r: all(abs(s["movimientos_en_reunion"]) <= FICHAS["MON-EXP-001"]["tol"]
                                    and abs(s["movimientos_acumulados"]) <= FICHAS["MON-EXP-001"]["tol"]
                                    and _cerca(s["probabilidades"]["movimientos"]["0"], 1.0,
                                               FICHAS["MON-EXP-001"]["tol"])
                                    for s in r["senda"])},
        {"nombre": "la senda reproduce los forwards de entrada (todos los nodos, también los que no añaden reunión)",
         "datos": [{"valores": _datos_mon_exp(plana=False)}], "parametros": {},
         "comprobar": lambda r: len(r["verificacion"]["nodos"]) == len(_SENDA_EXP["dias"])
         and all(abs(n["tipo_senda"] - n["tipo_nodo"]) <= FICHAS["MON-EXP-001"]["tol"] * abs(n["tipo_nodo"])
                 for n in r["verificacion"]["nodos"])},
        {"nombre": "senda escalonada exacta recuperada; movimiento de cada reunión frente al tipo en vigor antes de ella",
         "datos": [{"valores": _datos_mon_exp(plana=False)}], "parametros": {},
         "comprobar": lambda r: all(
             abs(s["tipo_mercado_implicito"] - t) <= FICHAS["MON-EXP-001"]["tol"] * t
             and abs(s["movimientos_en_reunion"] - m) <= FICHAS["MON-EXP-001"]["tol"]
             and abs(s["movimientos_acumulados"] - a) <= FICHAS["MON-EXP-001"]["tol"]
             for s, t, m, a in zip(r["senda"], _SENDA_EXP["tasas"][1:], _SENDA_EXP["en_reunion"],
                                   _SENDA_EXP["acumulados"], strict=True))},
    ],
    "MON-REAL-001": [
        {"nombre": "π = 0 ⇒ real = nominal",
         "datos": [{"valores": _datos_mon_real(pi_cero=True)}], "parametros": {},
         "comprobar": lambda r: _cerca(r["real_ex_ante"]["EUR"], 0.021, FICHAS["MON-REAL-001"]["tol"])
         and all(_cerca(x["real_periodo"], x["nominal_periodo"], FICHAS["MON-REAL-001"]["tol"])
                 for x in r["tabla"]["EUR"]["serie_ex_post"])},
        {"nombre": "coherencia con FIN-CAGR-001 (segunda vía de la renovación compuesta)",
         "datos": [{"valores": _datos_mon_real(pi_cero=False)}], "parametros": {},
         "comprobar": lambda r: r["verificacion"]["error_segunda_via_max"] <= FICHAS["MON-REAL-001"]["tol"]},
        {"nombre": "método (i): Fisher exacto ex ante (1 + i)/(1 + π^e) − 1",
         "datos": [{"valores": _datos_mon_real(pi_cero=False)}], "parametros": {},
         "comprobar": lambda r: _rel(r["real_ex_ante"]["EUR"], 1.021 / 1.019 - 1, FICHAS["MON-REAL-001"]["tol"])},
    ],
    "MON-FIX-001": [
        {"nombre": "renovar con los forwards = fijar (identidad sin arbitraje)",
         "datos": [{"valores": _datos_mon_fix(plana=False)}], "parametros": {},
         "comprobar": lambda r: abs(r["verificacion"]["renovar_forwards_menos_fijar_pb"])
         <= FICHAS["MON-FIX-001"]["tol"] * PB},
        {"nombre": "curva y senda planas ⇒ indiferencia",
         "datos": [{"valores": _datos_mon_fix(plana=True)}], "parametros": {},
         "comprobar": lambda r: abs(r["renovar"]["plana"]["diferencia_vs_fijar_pb"]) <= FICHAS["MON-FIX-001"]["tol"] * PB
         and abs(r["holgura_pb"]["plana"]) <= FICHAS["MON-FIX-001"]["tol"] * PB},
        {"nombre": "referencia ingenua: renovar al tipo vigente a tau (curva con pendiente)",
         "datos": [{"valores": _datos_mon_fix(plana=False)}], "parametros": {},
         "comprobar": lambda r: _rel(r["renovar"]["plana"]["tipo_constante_equivalente"], 0.0200,
                                     FICHAS["MON-FIX-001"]["tol"])
         and _rel(r["renovar"]["plana"]["tae"], _tae_plana_mon_fix(0.0200), FICHAS["MON-FIX-001"]["tol"])},
    ],
    "IDX-ERP-001": [
        {"nombre": "sin cambio de múltiplo ni recompras ⇒ E[R] = dividendo + crecimiento nominal (Gordon)",
         "datos": [{"valores": _datos_idx_erp(gordon=True)}], "parametros": {"lambda_reversion": 0},
         "comprobar": lambda r: _cerca(r["er_nominal"]["IDX-SINT"], 0.03 + 0.015 + 0.02, FICHAS["IDX-ERP-001"]["tol"])},
        {"nombre": "suma de bloques = total",
         "datos": [{"valores": _datos_idx_erp(gordon=False)}], "parametros": {},
         "comprobar": lambda r: _cerca(sum(r["bloques"]["IDX-SINT"].values()), r["er_nominal"]["IDX-SINT"],
                                       FICHAS["IDX-ERP-001"]["tol"])},
        {"nombre": "método (i)–(ii): reversión λ compuesta (m_obj/m_act)^{1/N} − 1 y real = nominal − π^e",
         "datos": [{"valores": _datos_idx_erp(gordon=False, mediana=20.0)}], "parametros": {},
         "comprobar": lambda r: _rel(r["bloques"]["IDX-SINT"]["cambio_valoracion"], (24 / 28) ** (1 / 10) - 1,
                                     FICHAS["IDX-ERP-001"]["tol"])
         and _rel(r["er_real"]["IDX-SINT"], r["er_nominal"]["IDX-SINT"] - 0.02, FICHAS["IDX-ERP-001"]["tol"])
         and _rel(r["er_nominal"]["IDX-SINT"], 0.03 + 0.01 + 0.015 + 0.02 + (24 / 28) ** (1 / 10) - 1,
                  FICHAS["IDX-ERP-001"]["tol"])},
    ],
    "IDX-CONC-001": [
        {"nombre": "pesos suman 1 ⇒ el peso de los n mayores con n = todos es 1 (y los sectoriales también suman 1)",
         "datos": [{"valores": {"composicion": _composicion(5, igual=False)}}], "parametros": {"top_n": 5},
         "comprobar": lambda r: _cerca(r["peso_top_n"], 1.0, FICHAS["IDX-CONC-001"]["tol"])
         and _cerca(r["verificacion"]["suma_pesos_sectoriales"], 1.0, FICHAS["IDX-CONC-001"]["tol"])},
        {"nombre": "índice equiponderado de n componentes ⇒ N_ef = n",
         "datos": [{"valores": {"composicion": _composicion(20, igual=True)}}], "parametros": {},
         "comprobar": lambda r: _cerca(r["n_ef"], 20.0, FICHAS["IDX-CONC-001"]["tol"] * 20)},
        {"nombre": "método (i): peso de los 10 mayores y HHI a mano con pesos distintos",
         "datos": [{"valores": {"composicion": _composicion(12, igual=False)}}], "parametros": {},
         "comprobar": lambda r: _rel(r["peso_top_n"], sum(range(3, 13)) / sum(range(1, 13)),
                                     FICHAS["IDX-CONC-001"]["tol"])
         and _rel(r["hhi"], sum(k * k for k in range(1, 13)) / sum(range(1, 13)) ** 2, FICHAS["IDX-CONC-001"]["tol"])},
    ],
    "IDX-REL-001": [
        {"nombre": "un índice frente a sí mismo ⇒ brecha 0 (z indefinido, declarado)",
         "datos": [{"valores": _datos_idx_rel(mismo=True)}], "parametros": {"ajuste_sectorial": False},
         "comprobar": lambda r: all(_cerca(b["brecha"], 0.0, FICHAS["IDX-REL-001"]["tol"])
                                    and _cerca(b["log_ratio"], 0.0, FICHAS["IDX-REL-001"]["tol"]) and b["z"] is None
                                    for b in r["brechas"].values())},
        {"nombre": "segunda vía: brecha con un múltiplo alternativo (A = 2·B en PER adelantado y en CAPE)",
         "datos": [{"valores": _datos_idx_rel(mismo=False, escala_b=0.5)}], "parametros": {"ajuste_sectorial": False},
         "comprobar": lambda r: all(_cerca(r["brechas"][m]["brecha"], 1.0, FICHAS["IDX-REL-001"]["tol"])
                                    and _cerca(r["brechas"][m]["log_ratio"], math.log(2), FICHAS["IDX-REL-001"]["tol"])
                                    for m in ("per_adelantado", "cape"))},
        {"nombre": "método (iv): momentum relativo 12-1 y a 3 meses del ratio de rentabilidades totales",
         "datos": [{"valores": _datos_idx_rel(mismo=False)}], "parametros": {"ajuste_sectorial": False},
         "comprobar": lambda r: all(
             _rel(r["momentum_relativo"][modo]["12-1"], (1.006 / 1.0065) ** 11 - 1, FICHAS["IDX-REL-001"]["tol"])
             and _rel(r["momentum_relativo"][modo]["3m"], (1.006 / 1.0065) ** 3 - 1, FICHAS["IDX-REL-001"]["tol"])
             for modo in ("cubierta", "no_cubierta"))},
    ],
    "IDX-REB-001": [
        {"nombre": "suma de cambios de peso = 0 ⇒ demanda simétrica",
         "datos": [{"valores": {"evento": _evento_reb()}}], "parametros": {},
         "comprobar": lambda r: _cerca(r["verificacion"]["suma_cambios_peso"], 0.0, FICHAS["IDX-REB-001"]["tol"])
         and _cerca(r["demanda_estimada"]["inclusiones"]["demanda"], 1e9, FICHAS["IDX-REB-001"]["tol"] * 1e9)
         and _cerca(r["demanda_estimada"]["exclusiones"]["demanda"], -1e9, FICHAS["IDX-REB-001"]["tol"] * 1e9)},
        {"nombre": "suma de cambios de peso = flujos declarados",
         "datos": [{"valores": {"evento": _evento_reb(flujos=0.002, cambios=[("IN1", 0.0015, 4e8),
                                                                             ("IN2", 0.0005, 1e8)])}}],
         "parametros": {},
         "comprobar": lambda r: _cerca(r["verificacion"]["suma_cambios_peso"], 0.002, FICHAS["IDX-REB-001"]["tol"])},
        {"nombre": "segunda vía: modelo normal alternativo (CAR plantado recuperado por ambos modelos)",
         "datos": [{"valores": {"evento": _evento_reb(), "eventos_comparables": _EV}}], "parametros": {},
         "comprobar": lambda r: all(
             _cerca(m[w]["car_medio"], float(np.mean(c)), FICHAS["IDX-REB-001"]["tol"])
             for m in (r["estudio_eventos"], r["segunda_via"])
             for w, c in (("anuncio_efectividad", _CAR1), ("efectividad_post", _CAR2)))},
    ],
}
