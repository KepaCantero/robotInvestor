"""Fichas del Motor del Bloque A: las diez fichas de prioridad P2 del Catálogo V5.0 (ampliación).

T-119. Fuente de verdad: «Catálogo de cálculos del Motor - V5.0», fichas FIR-CRED-001 (sección 9), FX-BEER-001 (10),
CMD-REAL-001 (11), REI-LEV-001 (12), CHR-ONCHAIN-001 y CHR-TOKEN-001 (13), PRV-PME-001, PRV-CF-001, ALT-HF-001 y
ALT-AUC-001 (14), con las convenciones de su sección 3. Sigue el patrón de `fichas_reales` (T-112) y aplica desde el diseño
las lecciones de las QA de T-106 y T-112.

Convenciones de este módulo:

- Todas las entradas llegan en línea en ``ent["valores"]`` (bloques con ``fecha`` en texto ISO). Ninguna ficha lee series
  de HT-01: son datos especializados (P2) que aporta el solicitante con su fuente.
- Tipos, volatilidades, rentabilidades de flujos y comisiones de entrada en **tanto por uno**; ALT-HF-001 recibe los
  rendimientos en % por periodo, como ACC-FACT-001, con la que debe ser coherente. Las salidas llevan la unidad en el sufijo
  de la clave: ``_pct`` en %, ``_pb`` en puntos básicos; sin sufijo, tanto por uno, veces o la unidad de origen.
- Recuento de días Real/365 (3.1). Percentil histórico = proporción de la historia ≤ valor; cuantiles de tipo 7
  (ST-DESC-001); desviaciones muestrales (n − 1).
- Falla cerrado: lo que falta o es incoherente lanza ``ErrorFicha`` con el motivo; un bloque opcional sin datos se entrega
  como ``None`` y se declara en las limitaciones. Ningún resultado lleva cifras no finitas (envoltura ``_cerrado``).
- Umbrales fijos: los umbrales de rechazo y de limitación, los rangos admitidos y las cotas de tamaño de cada parámetro y de
  cada lista de datos están en ``UMBRALES``; una petición que traiga uno se rechaza, y también la que traiga un parámetro
  que la ficha no declara. Lo que la ficha no fija está marcado [PROPUESTO] (INC-T119-01).
- Fecha de corte: un dato observado con fecha posterior a ``ent["fecha_corte"]`` se rechaza (no conocible). Las fechas
  contractuales futuras (vencimientos de deuda, desbloqueos de tokens) no son observaciones: son el dato.
- Frontera con el Bloque B (1.6): las fichas con componentes (FIR-CRED, REI-LEV, CHR-TOKEN) entregan solo el agregado y su
  dispersión, nunca una fila por componente: con su salida no se puede ordenar emisores ni tokens.
- Determinista: ninguna ficha usa azar (todas declaran semilla ``null``).

Interfaz de cada manejador: ``fn(ent, params) -> (resultado, limitaciones)``.
"""
from __future__ import annotations

import math
import statistics
from collections.abc import Callable
from functools import wraps
from itertools import pairwise
from typing import Any

import numpy as np
import pandas as pd
from scipy import optimize, special, stats

from ..configuracion import parametro
from . import fichas_series as fs
from . import fichas_valoracion as fv
from . import operaciones as op
from .fichas_reales import (
    ANIOS_H5_MAX,
    DIAS_ANIO,
    MESES_ANIO,
    PB,
    PCT,
    TRIMESTRES_ANIO,
    Manejador,
    Resultado,
    _ar1,
    _corte,
    _dict,
    _entero,
    _fecha,
    _hasta_corte,
    _lista,
    _num,
    _opcion,
    _posicion,
    _rango,
    _tabla,
    _texto,
)
from .fichas_reales import (
    _cerrado as _cerrado_reales,
)
from .operaciones import ErrorFicha

# ------------------------------------------------------------------ cotas de tamaño [PROPUESTO INC-T119-01]
ANIOS_HISTORIA_MAX = 100     # una ventana histórica no pasa de 100 años (INC-T113-01 y fichas de valoración de T-112)
LISTA_PARAMETRO_MAX = 12     # una lista de parámetros no pasa de 12 elementos (INC-T113-01)
COMPONENTES_MAX = 500        # componentes de un agregado (segmento, subsector, ecosistema)
BASE_INDICE = 100            # ALT-AUC-001: «índice base 100»
# Magnitud máxima de cualquier cifra de los datos en línea: por encima, las sumas y los productos desbordan y una división
# por un total infinito daría un cero con apariencia de cifra; se rechaza antes de calcular
MAGNITUD_MAX = 1e100

# ------------------------------------------------------------------ parámetros por defecto (campo «Parámetros»)
PARAMETROS_POR_DEFECTO: dict[str, dict[str, Any]] = {
    # FIR-CRED-001 · «Parámetros»: T (1 año); metodo (iterativo; ingenuo); mu (rendimiento histórico de activos o r).
    "FIR-CRED-001": {"T": 1, "metodo": "iterativo", "mu": "historico"},
    # FX-BEER-001 · «Parámetros»: metodo (DOLS; Johansen); retardos (2).
    "FX-BEER-001": {"metodo": "DOLS", "retardos": 2},
    # CMD-REAL-001 · «Parámetros»: deflactor (IPC de la moneda de cotización); percentil_coste (0,90).
    "CMD-REAL-001": {"deflactor": "ipc_moneda_cotizacion", "percentil_coste": 0.90},
    # REI-LEV-001 · «Parámetros»: caidas_valor (−10 %, −20 %); margen (de mercado: el de los datos si no se fija).
    "REI-LEV-001": {"caidas_valor": [-0.10, -0.20], "margen": None},
    # CHR-ONCHAIN-001 · «Parámetros»: media_nvt (90 días); fuente (declarada: la de los datos si no se fija).
    "CHR-ONCHAIN-001": {"media_nvt": 90, "fuente": None},
    # CHR-TOKEN-001 · «Parámetros»: ventanas_desbloqueo (30, 90 días).
    "CHR-TOKEN-001": {"ventanas_desbloqueo": [30, 90]},
    # PRV-PME-001 · «Parámetros»: metodo (KS-PME; alfa_directo; PME+); indice (comparable en riesgo declarado).
    "PRV-PME-001": {"metodo": "KS-PME", "indice": None},
    # PRV-CF-001 · «Parámetros»: tasas_aportacion (por año de vida); bow (2,5; 1–5); crecimiento (supuesto declarado).
    # La ficha no da valor por defecto a las tasas ni al crecimiento: los declara el solicitante.
    "PRV-CF-001": {"tasas_aportacion": None, "bow": 2.5, "crecimiento": None},
    # ALT-HF-001 · «Parámetros»: factores (Fung-Hsieh 7); desuavizar (true).
    "ALT-HF-001": {"factores": "Fung-Hsieh 7", "desuavizar": True},
    # ALT-AUC-001 · «Parámetros»: metodo (ventas_repetidas; hedonico); comisiones (supuesto declarado, 10–25 %).
    "ALT-AUC-001": {"metodo": "ventas_repetidas", "comisiones": None},
}

# Umbrales de rechazo y de limitación, rangos admitidos y cotas de tamaño: los fija la ficha (o INC-T119-01) y la petición
# no los puede cambiar.
UMBRALES: dict[str, dict[str, Any]] = {
    # FIR-CRED-001 · «Entradas mínimas» y «Aclaración y rechazo»: ≥ 10 componentes cotizados. «Método»: punto de impago =
    # deuda a corto + ½ deuda a largo; proporción con DD < 2; alternativa ingenua de Bharath y Shumway (2008):
    # σ_D = 0,05 + 0,25·σ_E. «Supuestos»: no válido para segmentos dominados por emisores sin acciones cotizadas
    # (cobertura < 0,5 [PROPUESTO]). T hasta H5 (30 años); tipos en (−1, 1); volatilidad de las acciones hasta 10
    # (1 000 % anual); tolerancia y tope de iteraciones de la raíz [PROPUESTO].
    "FIR-CRED-001": {"componentes_minimos": 10, "componentes_maximos": COMPONENTES_MAX, "factor_deuda_largo": 0.5,
                     "dd_umbral": 2, "ingenuo_sigma_deuda": (0.05, 0.25), "metodos_admitidos": ("iterativo", "ingenuo"),
                     "mu_admitidos": ("historico", "r"), "cobertura_minima": 0.5, "T_maximo_anios": ANIOS_H5_MAX,
                     "rango_tipo": (-1.0, 1.0), "volatilidad_maxima": 10.0, "tolerancia_raiz": 1e-13,
                     "iteraciones_maximas": 200},
    # FX-BEER-001 · «Aclaración y rechazo»: < 15 años. «Entradas mínimas»: trimestrales ≥ 20 años. «Método»: los cuatro
    # fundamentales. Retardos 1–4 trimestres [PROPUESTO]; contraste al 0,05, uno de los niveles tabulados de FX-COINT-001.
    "FX-BEER-001": {"anios_rechazo": 15, "anios_entrada_minima": 20,
                    "fundamentales": ("terminos_intercambio", "diferencial_productividad", "piin_pib",
                                      "diferencial_tipos_reales"),
                    "metodos_admitidos": ("DOLS", "Johansen"), "rango_retardos": (1, 4), "nivel_contraste": 0.05,
                    "anios_historia_maximos": ANIOS_HISTORIA_MAX},
    # CMD-REAL-001 · «Aclaración y rechazo»: < 15 años. «Entradas mínimas»: mensual ≥ 30 años. Tendencia con
    # FX-TREND-001 (nivel 0,05, su valor por defecto). percentil_coste en (0, 1]; tramos de la curva de costes ≤ 1 000.
    "CMD-REAL-001": {"anios_rechazo": 15, "anios_entrada_minima": 30, "deflactores_admitidos": ("ipc_moneda_cotizacion",),
                     "rango_percentil_coste": (0.0, 1.0), "nivel_tendencia": 0.05, "tramos_maximos": 1000,
                     "anios_historia_maximos": ANIOS_HISTORIA_MAX},
    # REI-LEV-001 · «Método»: vencimientos a 24 meses; caídas de valor en (−1, 0). Costes y swap en (−1, 1); margen en
    # [0, 1). Cotas de componentes, vencimientos por componente y caídas [PROPUESTO].
    "REI-LEV-001": {"meses_vencimientos": 24, "componentes_maximos": COMPONENTES_MAX, "vencimientos_maximos": 100,
                    "caidas_maximas": LISTA_PARAMETRO_MAX, "rango_caida": (-1.0, 0.0), "rango_coste": (-1.0, 1.0),
                    "rango_margen": (0.0, 1.0)},
    # CHR-ONCHAIN-001 · «Entradas mínimas»: diarias ≥ 2 años (≥ 4 recomendados; con menos, «pocos ciclos», sección 13).
    # media_nvt 1–365 días; historia hasta H5 (30 años) en días [PROPUESTO], como CHR-FUND-001.
    "CHR-ONCHAIN-001": {"dias_minimos": 2 * DIAS_ANIO, "dias_recomendados": 4 * DIAS_ANIO, "rango_media_nvt": (1, DIAS_ANIO),
                        "dias_maximos": ANIOS_H5_MAX * DIAS_ANIO},
    # CHR-TOKEN-001 · «Parámetros»: ventanas de desbloqueo en días, hasta H5 (30 años) y 12 ventanas [PROPUESTO].
    # Concentración en [0, 1]; rendimiento de staking en (−1, 10).
    "CHR-TOKEN-001": {"tokens_maximos": COMPONENTES_MAX, "desbloqueos_maximos": 1000, "ventanas_maximas": LISTA_PARAMETRO_MAX,
                      "ventana_dias_maxima": ANIOS_H5_MAX * DIAS_ANIO, "rango_staking": (-1.0, 10.0)},
    # PRV-PME-001 · métodos de la ficha. Flujos ≤ 10 000 fechas; TIR buscada en (−0,99, 10) con tolerancia fija
    # [PROPUESTO] (la ficha da 1e-8 para la re-ejecución).
    "PRV-PME-001": {"metodos_admitidos": ("KS-PME", "alfa_directo", "PME+"), "flujos_maximos": 10_000,
                    "rango_tir": (-0.99, 10.0), "tolerancia_raiz": 1e-13, "iteraciones_maximas": 200,
                    "anios_historia_maximos": ANIOS_HISTORIA_MAX},
    # PRV-CF-001 · «Parámetros»: bow 1–5. Tasas de aportación en [0, 1]; crecimiento en (−1, 1); vida ≤ H5 (30 años);
    # rendimiento mínimo de distribución Y = 0 (la ficha no lo nombra) [PROPUESTO].
    "PRV-CF-001": {"rango_bow": (1, 5), "rango_tasa_aportacion": (0.0, 1.0), "rango_crecimiento": (-1.0, 1.0),
                   "vida_maxima_anios": ANIOS_H5_MAX, "rendimiento_minimo": 0.0, "flujos_maximos": 10_000,
                   "navs_maximos": 10_000, "rango_tir": (-0.99, 10.0), "tolerancia_raiz": 1e-13, "iteraciones_maximas": 200,
                   "anios_historia_maximos": ANIOS_HISTORIA_MAX},
    # ALT-HF-001 · «Entradas mínimas» y «Aclaración y rechazo»: ≥ 36 rentabilidades mensuales. Los siete factores de Fung y
    # Hsieh (2004): mercado, tamaño, bono a 10 años, diferencial de crédito y los tres de tendencia (bonos, divisas y
    # materias primas). Factores declarados ≤ 12.
    "ALT-HF-001": {"observaciones_minimas": 36,
                   "factores_fung_hsieh": ("MKT", "SMB", "BONO10A", "CREDITO", "PTFSBD", "PTFSFX", "PTFSCOM"),
                   "factores_maximos": LISTA_PARAMETRO_MAX, "anios_historia_maximos": ANIOS_HISTORIA_MAX},
    # ALT-AUC-001 · «Entradas mínimas» y «Aclaración y rechazo»: ≥ 500 transacciones (ventas repetidas: ≥ 200 pares).
    # «Parámetros»: comisiones 10–25 %. Índice anual con ≥ 3 periodos; transacciones ≤ 50 000; características ≤ 20
    # [PROPUESTO].
    "ALT-AUC-001": {"transacciones_minimas": 500, "pares_minimos": 200, "transacciones_maximas": 50_000,
                    "rango_comisiones": (0.10, 0.25), "metodos_admitidos": ("ventas_repetidas", "hedonico"),
                    "periodos_minimos": 3, "caracteristicas_maximas": 20, "anios_historia_maximos": ANIOS_HISTORIA_MAX},
}

# Claves de los parámetros que añade la capa de servicio y que no son de la ficha (`Motor.servir`: «clase»).
AJENOS = frozenset({"clase"})

# Advertencias obligatorias de entrega («Supuestos y limitaciones» de cada ficha).
ADVERTENCIAS: dict[str, list[str]] = {
    "FIR-CRED-001": ["infraestima diferenciales a corto plazo",
                     ("no válido para financieras ni para segmentos dominados por emisores sin acciones cotizadas "
                      "(cobertura del segmento declarada)"),
                     "los emisores individuales son solo componentes del agregado; la ficha no ordena emisores (1.6)"],
    "FX-BEER-001": ["equilibrio dependiente de la especificación", "rupturas de régimen cambiario invalidan la muestra"],
    "CMD-REAL-001": ["las curvas de coste cambian con la tecnología", "superciclos largos con pocas observaciones"],
    "REI-LEV-001": ["coste de refinanciación supuesto", "acceso al mercado no garantizado en crisis",
                    "agregado y dispersión de los componentes, sin ordenar emisores (1.6)"],
    "CHR-ONCHAIN-001": ["capitalización realizada solo directa en cadenas UTXO",
                        "umbrales históricos sobre ≈ 3–4 ciclos", "volumen contaminado por movimientos internos"],
    "CHR-TOKEN-001": ["calendarios modificables por gobernanza",
                      "las direcciones de custodios distorsionan la concentración",
                      "los tokens individuales solo como componentes o cuando el ámbito es la propia red (1.6)"],
    "PRV-PME-001": ["NAV final de tasación", "la elección del índice es decisiva (pequeña capitalización para buyout)",
                    "sin ajuste por apalancamiento salvo declaración"],
    "PRV-CF-001": ["las líneas de suscripción inflan la TIR",
                   "la TIR no es comparable con rentabilidades anuales de índices",
                   "proyección determinista sobre supuestos declarados (tasas de aportación, bow y crecimiento)"],
    "ALT-HF-001": ["exposiciones no lineales (opcionalidad) solo parcialmente capturadas",
                   "sesgos de supervivencia y de relleno retrospectivo de las bases de datos, de varios puntos anuales"],
    "ALT-AUC-001": ["sesgo de selección (solo se subasta lo revalorizado); sin ajuste, declarado",
                    "la mediana del índice no es la rentabilidad de una pieza", "autenticidad no evaluada"],
}


# ================================================================== utilidades comunes
def _magnitud_excesiva(x: Any) -> bool:
    if isinstance(x, bool):
        return False
    if isinstance(x, (int, float)):                     # un entero de Python puede no caber en un float: se compara tal cual
        return abs(x) > MAGNITUD_MAX
    return isinstance(x, (np.integer, np.floating)) and abs(float(x)) > MAGNITUD_MAX


def _cerrado(ficha: str) -> Callable[[Manejador], Manejador]:
    """La envoltura de `fichas_reales` (entradas mal formadas, excepciones y resultados no finitos → ErrorFicha) y, antes,
    el rechazo de una serie de HT-01 (no se usaría, y no se ignora en silencio) y de cualquier cifra de los datos en línea
    cuya magnitud pase de `MAGNITUD_MAX`."""
    def decorar(fn: Manejador) -> Manejador:
        interior = _cerrado_reales(ficha)(fn)

        @wraps(fn)
        def envoltura(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
            if isinstance(ent, dict) and (ent.get("series") or ent.get("series_rol")):
                raise ErrorFicha(f"{ficha}: la ficha no usa series de HT-01: sus datos se aportan en línea, con su fuente")
            pila: list[Any] = [ent.get("valores")] if isinstance(ent, dict) else []
            while pila:
                x = pila.pop()
                if isinstance(x, dict):
                    pila.extend(x.values())
                elif isinstance(x, (list, tuple)):
                    pila.extend(x)
                elif _magnitud_excesiva(x):
                    raise ErrorFicha(f"{ficha}: cifra de magnitud mayor que {MAGNITUD_MAX:g} en los datos: fuera de dominio")
            return interior(ent, params)
        return envoltura
    return decorar


def _acotada(x: Any, que: str, maximo: int) -> list[Any]:
    """Lista no vacía con cota superior de tamaño, comprobada antes de recorrerla."""
    lst = _lista(x, que)
    if len(lst) > maximo:
        raise ErrorFicha(f"{que}: {len(lst)} elementos (máximo {maximo})")
    return lst


def _tabla_acotada(filas: Any, campos: dict[str, tuple[float | None, bool]], que: str, maximo: int,
                   opcionales: tuple[str, ...] = ()) -> pd.DataFrame:
    return _tabla(_acotada(filas, que, maximo), campos, que, opcionales)


def _consecutivas(indice: pd.DatetimeIndex, frecuencia: str, que: str) -> None:
    """Una observación por periodo («D», «M» o «Q»), sin huecos."""
    per = indice.to_period(frecuencia)
    if len(per) >= 2 and not bool(np.all(np.diff(per.asi8) == 1)):
        nombres = {"D": "diarias", "M": "mensuales", "Q": "trimestrales"}
        raise ErrorFicha(f"{que}: fechas no {nombres[frecuencia]} consecutivas (huecos o periodos repetidos)")


def _iso(d: pd.Timestamp) -> str:
    return d.date().isoformat()


def _distribucion(x: np.ndarray) -> dict[str, float]:
    """Dispersión de los componentes: mediana, cuartiles (tipo 7, ST-DESC-001), mínimo y máximo."""
    q25, q50, q75 = (float(q) for q in np.quantile(x, [0.25, 0.5, 0.75]))
    return {"mediana": q50, "q25": q25, "q75": q75, "minimo": float(np.min(x)), "maximo": float(np.max(x))}


def _ids_unicos(ids: list[str], que: str) -> None:
    if len(set(ids)) != len(ids):
        raise ErrorFicha(f"{que}: identificadores de componente repetidos")


def _lista_parametro(x: Any, que: str, maximo: int) -> list[Any]:
    if not isinstance(x, list) or not x:
        raise ErrorFicha(f"{que}: se esperaba una lista no vacía")
    if len(x) > maximo:
        raise ErrorFicha(f"{que}: {len(x)} elementos (máximo {maximo})")
    return x


def _validar_parametros(F: str, p: dict[str, Any]) -> None:
    """Tipo y rango de cada parámetro de la petición, con cota superior en los tamaños."""
    u = UMBRALES[F]
    if F == "FIR-CRED-001":
        p["T"] = _rango(p["T"], f"{F}: T (años)", 0, u["T_maximo_anios"], abierto_lo=True)
        p["metodo"] = _opcion(p["metodo"], f"{F}: metodo", u["metodos_admitidos"])
        p["mu"] = _opcion(p["mu"], f"{F}: mu", u["mu_admitidos"])
    elif F == "FX-BEER-001":
        p["metodo"] = _opcion(p["metodo"], f"{F}: metodo", u["metodos_admitidos"])
        p["retardos"] = _entero(p["retardos"], f"{F}: retardos (trimestres)", *u["rango_retardos"])
    elif F == "CMD-REAL-001":
        p["deflactor"] = _opcion(p["deflactor"], f"{F}: deflactor", u["deflactores_admitidos"])
        lo, hi = u["rango_percentil_coste"]
        p["percentil_coste"] = _rango(p["percentil_coste"], f"{F}: percentil_coste", lo, hi, abierto_lo=True)
    elif F == "REI-LEV-001":
        caidas = _lista_parametro(p["caidas_valor"], f"{F}: caidas_valor", u["caidas_maximas"])
        lo, hi = u["rango_caida"]
        cs = [_rango(c, f"{F}: caidas_valor", lo, hi, abierto_lo=True, abierto_hi=True) for c in caidas]
        if len(set(cs)) != len(cs):
            raise ErrorFicha(f"{F}: caidas_valor repetidas")
        p["caidas_valor"] = sorted(cs, reverse=True)
        if p["margen"] is not None:
            lo, hi = u["rango_margen"]
            p["margen"] = _rango(p["margen"], f"{F}: margen", lo, hi, abierto_hi=True)
    elif F == "CHR-ONCHAIN-001":
        p["media_nvt"] = _entero(p["media_nvt"], f"{F}: media_nvt (días)", *u["rango_media_nvt"])
        if p["fuente"] is not None:
            p["fuente"] = _texto(p["fuente"], f"{F}: fuente")
    elif F == "CHR-TOKEN-001":
        vent = _lista_parametro(p["ventanas_desbloqueo"], f"{F}: ventanas_desbloqueo", u["ventanas_maximas"])
        vs = [_entero(w, f"{F}: ventanas_desbloqueo (días)", 1, u["ventana_dias_maxima"]) for w in vent]
        if len(set(vs)) != len(vs):
            raise ErrorFicha(f"{F}: ventanas_desbloqueo repetidas")
        p["ventanas_desbloqueo"] = sorted(vs)
    elif F == "PRV-PME-001":
        p["metodo"] = _opcion(p["metodo"], f"{F}: metodo", u["metodos_admitidos"])
        if p["indice"] is not None:
            p["indice"] = _texto(p["indice"], f"{F}: indice")
    elif F == "PRV-CF-001":
        p["bow"] = _rango(p["bow"], f"{F}: bow", *u["rango_bow"])
        if p["tasas_aportacion"] is not None:
            tasas = _lista_parametro(p["tasas_aportacion"], f"{F}: tasas_aportacion", u["vida_maxima_anios"])
            p["tasas_aportacion"] = [_rango(t, f"{F}: tasas_aportacion", *u["rango_tasa_aportacion"]) for t in tasas]
        if p["crecimiento"] is not None:
            lo, hi = u["rango_crecimiento"]
            p["crecimiento"] = _rango(p["crecimiento"], f"{F}: crecimiento", lo, hi, abierto_lo=True, abierto_hi=True)
    elif F == "ALT-HF-001":
        if not isinstance(p["desuavizar"], bool):
            raise ErrorFicha(f"{F}: desuavizar debe ser true o false")
        if isinstance(p["factores"], list):
            nombres = [_texto(n, f"{F}: factores") for n in _lista_parametro(p["factores"], f"{F}: factores",
                                                                              u["factores_maximos"])]
            if len(set(nombres)) != len(nombres) or set(nombres) & {"fecha", "r", "rf"}:
                raise ErrorFicha(f"{F}: factores repetidos o con un nombre reservado (fecha, r, rf)")
            p["factores"] = nombres
        else:
            p["factores"] = _opcion(p["factores"], f"{F}: factores", ("Fung-Hsieh 7",))
    elif F == "ALT-AUC-001":
        p["metodo"] = _opcion(p["metodo"], f"{F}: metodo", u["metodos_admitidos"])
        if p["comisiones"] is not None:
            p["comisiones"] = _rango(p["comisiones"], f"{F}: comisiones", *u["rango_comisiones"])


def _parametros(ficha: str, params: dict[str, Any] | None) -> dict[str, Any]:
    """Parámetros de la petición encima de los de la ficha, validados. Se rechazan un umbral de `UMBRALES` en la petición y
    una clave que la ficha no declara (salvo las que añade la capa de servicio, `AJENOS`)."""
    if params is not None and not isinstance(params, dict):
        raise ErrorFicha(f"{ficha}: los parámetros deben ser un dict")
    params = params or {}
    fijos = set(params) & set(UMBRALES[ficha])
    if fijos:
        raise ErrorFicha(f"{ficha}: {sorted(fijos)} son umbrales fijos de la ficha, no parámetros de la petición")
    desconocidos = set(params) - set(PARAMETROS_POR_DEFECTO[ficha]) - AJENOS
    if desconocidos:
        raise ErrorFicha(f"{ficha}: parámetros no declarados en la ficha: {sorted(map(str, desconocidos))[:5]}")
    p = dict(PARAMETROS_POR_DEFECTO[ficha])
    p.update({k: v for k, v in params.items() if v is not None and k in p})
    for k, val in p.items():
        if isinstance(val, list):
            p[k] = list(val)
    _validar_parametros(ficha, p)
    return p


def _fecha_dato(v: dict[str, Any], clave: str, corte: pd.Timestamp | None, que: str) -> pd.Timestamp:
    """Fecha de un dato observado: obligatoria y no posterior a la fecha de corte."""
    f = _fecha(v.get(clave), f"{que}: «{clave}»")
    _hasta_corte([f], corte, f"{que}: «{clave}»")
    return f


# ================================================================== FIR-CRED-001
def _merton(E: float, sE: float, D: float, r: float, T: float, u: dict[str, Any], tol: float) -> tuple[float, float, float]:
    """(V, σ_V, error relativo) del sistema de Merton: E = V·N(d₁) − D·e^{−rT}·N(d₂) y σ_E·E = N(d₁)·σ_V·V.

    Dos raíces de Brent anidadas: para cada σ_V, el V que da la capitalización E (la opción crece con V, y V está entre E
    y E + D·e^{−rT}); fuera, el σ_V que reproduce la volatilidad de las acciones (σ_V ≤ σ_E, porque N(d₁)·V ≥ E)."""
    rt, it = u["tolerancia_raiz"], u["iteraciones_maximas"]
    desc = D * math.exp(-r * T)
    vmax, raiz = E + desc, math.sqrt(T)

    def opcion(V: float, s: float) -> tuple[float, float]:
        d1 = (math.log(V / D) + (r + 0.5 * s * s) * T) / (s * raiz)
        return V * float(special.ndtr(d1)) - desc * float(special.ndtr(d1 - s * raiz)), d1

    def activos(s: float) -> float:
        if opcion(vmax, s)[0] <= E:
            return vmax
        return float(optimize.brentq(lambda V: opcion(V, s)[0] - E, E, vmax, xtol=rt * E, rtol=rt, maxiter=it))

    def brecha(s: float) -> float:
        V = activos(s)
        return float(special.ndtr(opcion(V, s)[1])) * s * V / E - sE

    lo = 0.5 * sE * E / vmax
    sV = sE if brecha(sE) <= 0 else float(optimize.brentq(brecha, lo, sE, xtol=rt * lo, rtol=rt, maxiter=it))
    V = activos(sV)
    valor, d1 = opcion(V, sV)
    error = max(abs(valor - E) / E, abs(float(special.ndtr(d1)) * sV * V / E - sE) / sE)
    if not error <= tol:
        raise ErrorFicha(f"FIR-CRED-001: el sistema de Merton no converge (error relativo {error:.3g} > {tol:g})")
    return V, sV, error


def _merton_medidas(V: float, sV: float, D: float, r: float, mu: float, T: float) -> dict[str, float]:
    """DD y PD (neutral al riesgo con r; real con μ), diferencial implícito y triángulo de crédito de un componente."""
    raiz = sV * math.sqrt(T)
    d1 = (math.log(V / D) + (r + 0.5 * sV * sV) * T) / raiz
    d2 = d1 - raiz
    dd_real = (math.log(V / D) + (mu - 0.5 * sV * sV) * T) / raiz
    pd_rn = float(special.ndtr(-d2))
    recuperado = V * math.exp(r * T) / D * float(special.ndtr(-d1))        # valor esperado recuperado, por unidad de D
    dif = -math.log(float(special.ndtr(d2)) + recuperado) / T              # e^{−sT} = N(d₂) + (V·e^{rT}/D)·N(−d₁)
    # Triángulo de crédito: s ≈ λ·LGD, con λ = −ln(1 − PD)/T y LGD = 1 − recuperado/PD (la pérdida que da el modelo)
    tri = -math.log1p(-pd_rn) / T * (1 - recuperado / pd_rn) if pd_rn > 0 else 0.0
    return {"dd": d2, "pd": pd_rn, "dd_real": dd_real, "pd_real": float(special.ndtr(-dd_real)), "dif": dif, "tri": tri}


@_cerrado("FIR-CRED-001")
def f_fir_cred(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """FIR-CRED-001 · Merton agregado: distancia al impago y diferencial implícito de un segmento (MC-09).

    ``valores``: ``fecha``; ``segmento`` = {"nombre", "financiero": bool, "cobertura" ∈ (0, 1] (parte de la deuda del
    segmento que representan los componentes cotizados)}; ``r`` (tipo sin riesgo continuo); ``diferencial_indice_pb``
    (el observado del índice del segmento); ``componentes`` = lista (≥ 10) de {"id", "capitalizacion" > 0,
    "volatilidad_acciones" > 0 (anual, 1 año diario), "deuda_corto" ≥ 0, "deuda_largo" ≥ 0 y, con ``mu: historico``,
    "mu_historico" (rendimiento histórico anual de los activos; en el método ingenuo, el de las acciones en el año
    previo, como Bharath y Shumway)}; opcional ``pd_historica_rating_pct`` (referencia ingenua).
    """
    F = "FIR-CRED-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    tol = FICHAS[F]["tol"]
    lim: list[str] = []
    fecha = _fecha_dato(v, "fecha", _corte(ent), F)
    seg = _dict(v.get("segmento"), f"{F}: «segmento»")
    nombre = _texto(seg.get("nombre"), f"{F}: segmento.nombre")
    if not isinstance(seg.get("financiero"), bool):
        raise ErrorFicha(f"{F}: aclaración: declare si el segmento es de bancos o aseguradoras (segmento.financiero)")
    if seg["financiero"]:
        raise ErrorFicha(f"{F}: rechazo: la ficha no es válida para segmentos de bancos y aseguradoras")
    cobertura = _rango(seg.get("cobertura"), f"{F}: segmento.cobertura (declarada)", 0, 1, abierto_lo=True)
    if cobertura < u["cobertura_minima"]:
        raise ErrorFicha(f"{F}: rechazo: segmento dominado por emisores sin acciones cotizadas (cobertura "
                         f"{cobertura:.2f} < {u['cobertura_minima']})")
    lo_r, hi_r = u["rango_tipo"]
    r = _rango(v.get("r"), f"{F}: r", lo_r, hi_r, abierto_lo=True, abierto_hi=True)
    observado = _rango(v.get("diferencial_indice_pb"), f"{F}: diferencial_indice_pb", 0)
    T = p["T"]
    comps = v.get("componentes")
    if isinstance(comps, list) and len(comps) < u["componentes_minimos"]:
        raise ErrorFicha(f"{F}: rechazo: {len(comps)} componentes cotizados (< {u['componentes_minimos']})")
    comps = _acotada(comps, f"{F}: componentes", u["componentes_maximos"])
    a_sd, b_sd = u["ingenuo_sigma_deuda"]
    ids: list[str] = []
    filas: list[dict[str, float]] = []
    deudas: list[float] = []
    error = 0.0
    for i, c in enumerate(comps):
        que = f"{F}: componentes[{i}]"
        c = _dict(c, que)
        ids.append(_texto(c.get("id"), f"{que}.id"))
        E = _rango(c.get("capitalizacion"), f"{que}.capitalizacion", 0, abierto_lo=True)
        sE = _rango(c.get("volatilidad_acciones"), f"{que}.volatilidad_acciones", 0, u["volatilidad_maxima"], abierto_lo=True)
        corto = _rango(c.get("deuda_corto"), f"{que}.deuda_corto", 0)
        largo = _rango(c.get("deuda_largo"), f"{que}.deuda_largo", 0)
        D = corto + u["factor_deuda_largo"] * largo                         # punto de impago
        if not D > 0:
            raise ErrorFicha(f"{que}: sin deuda, la distancia al impago no está definida (retírelo del agregado y "
                             f"declárelo en la cobertura)")
        mu = r if p["mu"] == "r" else _rango(c.get("mu_historico"), f"{que}.mu_historico (o use mu: r)", lo_r, hi_r,
                                             abierto_lo=True, abierto_hi=True)
        if p["metodo"] == "iterativo":
            V, sV, err = _merton(E, sE, D, r, T, u, tol)
            error = max(error, err)
        else:                                                              # Bharath y Shumway (2008)
            V = E + D
            sV = E / V * sE + D / V * (a_sd + b_sd * sE)
        filas.append(_merton_medidas(V, sV, D, r, mu, T))
        deudas.append(corto + largo)
    _ids_unicos(ids, F)
    w = np.array(deudas) / float(np.sum(deudas))

    def bloque(dd: np.ndarray, pd_: np.ndarray) -> dict[str, Any]:
        return {"dd": {**_distribucion(dd), "media_ponderada_deuda": float(w @ dd)},
                "pd_pct": {**_distribucion(pd_ * PCT), "media_ponderada_deuda": float(w @ pd_) * PCT},
                "proporcion_dd_menor_2_pct": float(np.mean(dd < u["dd_umbral"])) * PCT}

    col = {k: np.array([f[k] for f in filas]) for k in filas[0]}
    implicito = float(w @ col["dif"]) * PB
    triangulo = float(w @ col["tri"]) * PB
    pd_hist: float | None = None
    if v.get("pd_historica_rating_pct") is None:
        lim.append("sin PD histórica por rating: referencia ingenua no comparada")
    else:
        pd_hist = _rango(v["pd_historica_rating_pct"], f"{F}: pd_historica_rating_pct", 0, PCT)
    neutral = bloque(col["dd"], col["pd"])
    real = bloque(col["dd_real"], col["pd_real"]) if p["mu"] == "historico" else None
    pd_ref = (real or neutral)["pd_pct"]["media_ponderada_deuda"]
    res = {
        "segmento": nombre, "fecha": _iso(fecha), "metodo": p["metodo"], "mu": p["mu"], "T_anios": T,
        "n_componentes": len(filas), "cobertura_segmento_pct": cobertura * PCT,
        "neutral_al_riesgo": neutral, "real": real,
        "diferencial_implicito_pb": implicito, "diferencial_observado_pb": observado,
        "brecha_observado_implicito_pb": observado - implicito,
        "segunda_via_triangulo": {"diferencial_pb": triangulo, "diferencia_con_implicito_pb": triangulo - implicito},
        "referencia_ingenua": {"tipo": "PD histórica por rating", "pd_historica_pct": pd_hist,
                               "diferencia_pd_pct": None if pd_hist is None else pd_ref - pd_hist},
        "verificacion": {"error_relativo_sistema_max": error},
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== FX-BEER-001
def _mco_hac(y: np.ndarray, X: np.ndarray, rezagos: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """MCO con covarianza HAC de Newey-West (núcleo de Bartlett), como ACC-FACT-001: (β, residuos, covarianza)."""
    xtx = np.linalg.inv(X.T @ X)
    beta = xtx @ (X.T @ y)
    e = y - X @ beta
    g = X * e[:, None]
    S = g.T @ g
    for rez in range(1, rezagos + 1):
        G = g[rez:].T @ g[:-rez]
        S = S + (1 - rez / (rezagos + 1)) * (G + G.T)
    return beta, e, xtx @ S @ xtx


def _dols(q: np.ndarray, X: np.ndarray, k: int) -> dict[str, Any]:
    """DOLS (Stock y Watson): q_t = c + β'x_t + Σ_{j=−k..k} γ_j'Δx_{t+j} + u_t, en la muestra t = k+1 … T−k−1."""
    T_, m = X.shape
    dX = np.diff(X, axis=0)                                # Δx_t = dX[t − 1]
    filas = np.arange(k + 1, T_ - k)
    Z = np.column_stack([np.ones(len(filas)), X[filas]] + [dX[filas - 1 + j] for j in range(-k, k + 1)])
    if len(filas) <= Z.shape[1] or np.linalg.matrix_rank(Z) < Z.shape[1]:
        raise ErrorFicha("FX-BEER-001: regresión DOLS no identificada (pocas observaciones o fundamentales colineales)")
    L = fv.rezagos_newey_west(len(filas))
    b, e, V = _mco_hac(q[filas], Z, L)
    return {"beta": b[1:m + 1], "cov": V[1:m + 1, 1:m + 1], "media_residuo": float(np.mean(e)), "n": len(filas),
            "rezagos_nw": L}


@_cerrado("FX-BEER-001")
def f_fx_beer(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """FX-BEER-001 · Tipo de cambio real de equilibrio (BEER) (MC-03).

    ``valores``: ``serie`` = lista trimestral consecutiva de {"fecha", "reer" > 0 (tipo real efectivo, nivel),
    "terminos_intercambio", "diferencial_productividad", "piin_pib", "diferencial_tipos_reales"} (los fundamentales, en
    la transformación que declare el solicitante); ``vintage`` = fecha de la edición de los datos (≥ la última
    observación y ≤ la fecha de corte).

    q = ln(reer). El equilibrio es c + β'x con c tal que el desalineamiento z = q − c − β'x tenga media nula en la muestra
    [PROPUESTO]; desalineamiento (%) = e^{z_T} − 1. IC del desalineamiento (solo DOLS) con la covarianza HAC de β:
    Var(z_T) = (x_T − x̄)'V(x_T − x̄).
    """
    F = "FX-BEER-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    corte = _corte(ent)
    lim: list[str] = []
    nombres = list(u["fundamentales"])
    campos: dict[str, tuple[float | None, bool]] = {"reer": (0, True), **dict.fromkeys(nombres, (None, False))}
    t = _tabla_acotada(v.get("serie"), campos, f"{F}: serie", u["anios_historia_maximos"] * TRIMESTRES_ANIO)
    _hasta_corte(t.index, corte, f"{F}: serie")
    _consecutivas(t.index, "Q", f"{F}: serie")
    vintage = _fecha_dato(v, "vintage", corte, F)
    if vintage < t.index[-1]:
        raise ErrorFicha(f"{F}: el vintage ({vintage.date()}) es anterior a la última observación ({t.index[-1].date()})")
    n = len(t)
    if n < u["anios_rechazo"] * TRIMESTRES_ANIO:
        raise ErrorFicha(f"{F}: rechazo: {n} trimestres (< {u['anios_rechazo']} años)")
    if n < u["anios_entrada_minima"] * TRIMESTRES_ANIO:
        lim.append(f"{n} trimestres (< {u['anios_entrada_minima']} años, la entrada mínima): equilibrio impreciso")
    q = np.log(t["reer"].to_numpy())
    X = t[nombres].to_numpy()
    m, k, nivel = len(nombres), p["retardos"], u["nivel_contraste"]
    coef: dict[str, dict[str, Any]]
    if p["metodo"] == "DOLS":
        est = _dols(q, X, k)
        beta = est["beta"]
        ee = np.sqrt(np.clip(np.diag(est["cov"]), 0.0, None))
        coef = {nb: {"beta": float(beta[j]), "ee": float(ee[j]), "t": float(beta[j] / ee[j]) if ee[j] > 0 else None}
                for j, nb in enumerate(nombres)}
        n_est, media_res = est["n"], est["media_residuo"]
    else:
        if n - k - 1 <= (m + 1) * (k + 1) + 1:
            raise ErrorFicha(f"{F}: Johansen no identificado con {n} trimestres y {k} retardos")
        joh = fs.johansen(np.column_stack([q, X]), k)
        vec = joh["beta"]
        if not abs(vec[0]) > 0:
            raise ErrorFicha(f"{F}: el vector de cointegración no se puede normalizar sobre el tipo real")
        beta = -vec[1:m + 1] / vec[0]
        coef = {nb: {"beta": float(beta[j]), "ee": None, "t": None} for j, nb in enumerate(nombres)}
        n_est, media_res = joh["T"], None
        lim.append("Johansen: sin error estándar de los coeficientes ni IC del desalineamiento (solo con DOLS)")
    sin_centrar = q - X @ beta
    const = float(np.mean(sin_centrar))
    z = sin_centrar - const                                            # desalineamiento = residuo, de media nula
    if not float(np.ptp(z)) > FICHAS[F]["tol"] * max(float(np.ptp(q)), 1.0):
        raise ErrorFicha(f"{F}: ajuste exacto: el tipo real es combinación exacta de los fundamentales (datos no independientes)")
    ic: list[float] | None = None
    nivel_ic: float | None = None
    if p["metodo"] == "DOLS":
        nivel_ic = _rango(parametro(ent.get("configuracion"), "evaluacion.nivel_ic"), "configuración: evaluacion.nivel_ic",
                          0, 1, abierto_lo=True, abierto_hi=True)
        d = X[-1] - X.mean(axis=0)
        ee_z = math.sqrt(max(float(d @ est["cov"] @ d), 0.0))
        zc = float(stats.norm.ppf(1 - (1 - nivel_ic) / 2))
        ic = [math.expm1(float(z[-1]) - zc * ee_z) * PCT, math.expm1(float(z[-1]) + zc * ee_z) * PCT]
        prueba = fs.adf(z, False, fs.rezagos_regla(n))
        critico = fs._critico(fs._CRIT_TAU, m + 1, nivel)
        coint = {"contraste": "ADF de los residuos (Engle-Granger)", "estadistico": prueba["tau"], "critico": critico,
                 "nivel": nivel, "evidencia": bool(prueba["tau"] < critico)}
    else:
        critico = fs._critico(fs._CRIT_TRAZA, m + 1, nivel)
        coint = {"contraste": "traza de Johansen (r = 0)", "estadistico": joh["traza"][0], "critico": critico,
                 "nivel": nivel, "evidencia": bool(joh["traza"][0] > critico)}
    if not coint["evidencia"]:
        lim.append(f"sin evidencia de cointegración al {nivel:g}: el equilibrio puede ser espurio")
    vm = fs._vida_media(z, lim)
    ppa = math.expm1(float(q[-1] - np.mean(q))) * PCT                  # FX-PPA-001: media histórica del tipo real
    des = math.expm1(float(z[-1])) * PCT
    res = {
        "metodo": p["metodo"], "retardos": k, "n": n, "n_estimacion": n_est, "anios": n / TRIMESTRES_ANIO,
        "vintage": _iso(vintage), "fecha": _iso(t.index[-1]),
        "coeficientes": coef, "constante": const,
        "tipo_real_actual": float(t["reer"].iloc[-1]), "equilibrio": math.exp(const + float(X[-1] @ beta)),
        "desalineamiento_pct": des, "ic_desalineamiento_pct": ic, "nivel_ic": nivel_ic,
        "velocidad_correccion_trimestral": vm["rho"] - 1,
        "vida_media_anios": None if vm["vida_media_periodos"] is None else vm["vida_media_periodos"] / TRIMESTRES_ANIO,
        "cointegracion": coint,
        "segunda_via_ppa": {"desalineamiento_pct": ppa, "diferencia_pct": des - ppa},
        "referencia_ingenua": {"tipo": "PPA (media histórica del tipo real) y RI-PA", "ppa_desalineamiento_pct": ppa,
                               "ri_pa_tipo_real": float(t["reer"].iloc[-1])},
        "verificacion": {"media_desalineamiento": float(np.mean(z)), "media_residuo_regresion": media_res},
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== CMD-REAL-001
@_cerrado("CMD-REAL-001")
def f_cmd_real(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """CMD-REAL-001 · Precio real y coste marginal (MC-09).

    ``valores``: ``moneda`` (de cotización) e ``ipc_moneda`` (la del IPC: debe ser la misma); ``serie`` = lista mensual
    consecutiva de {"fecha", "precio" > 0, "ipc" > 0}; ``curva_costes`` = {"fecha", "fuente", "tramos": lista de
    {"produccion" > 0, "coste" > 0}} (coste nominal de cada tramo de producción en la fecha de la curva).

    Precio real en moneda constante del último mes: precio_t·IPC_T/IPC_t. Coste marginal = coste del tramo en el que la
    producción acumulada (ordenada por coste) alcanza el percentil; se lleva a moneda constante con el IPC de su mes.
    """
    F = "CMD-REAL-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    corte = _corte(ent)
    tol = FICHAS[F]["tol"]
    lim: list[str] = []
    moneda = _texto(v.get("moneda"), f"{F}: «moneda» de cotización")
    if _texto(v.get("ipc_moneda"), f"{F}: «ipc_moneda»") != moneda:
        raise ErrorFicha(f"{F}: el deflactor debe ser el IPC de la moneda de cotización ({moneda})")
    t = _tabla_acotada(v.get("serie"), {"precio": (0, True), "ipc": (0, True)}, f"{F}: serie",
                       u["anios_historia_maximos"] * MESES_ANIO)
    _hasta_corte(t.index, corte, f"{F}: serie")
    _consecutivas(t.index, "M", f"{F}: serie")
    n = len(t)
    if n < u["anios_rechazo"] * MESES_ANIO:
        raise ErrorFicha(f"{F}: rechazo: {n} meses (< {u['anios_rechazo']} años)")
    if n < u["anios_entrada_minima"] * MESES_ANIO:
        lim.append(f"{n} meses (< {u['anios_entrada_minima']} años, la entrada mínima): percentil sobre la historia disponible")
    precio, ipc = t["precio"].to_numpy(), t["ipc"].to_numpy()
    real = precio * ipc[-1] / ipc
    actual = float(real[-1])
    pos = _posicion(actual, real)
    if pos["z"] is None:
        lim.append("precio real sin dispersión: z indefinido")
    mk = op.mann_kendall(np.log(real), u["nivel_tendencia"], True)      # FX-TREND-001 sobre el logaritmo del precio real

    def anual(pendiente: float) -> float:
        return math.expm1(MESES_ANIO * pendiente) * PCT

    cc = _dict(v.get("curva_costes"), f"{F}: «curva_costes» (con fecha y fuente)")
    f_cc = _fecha_dato(cc, "fecha", corte, f"{F}: curva_costes")
    fuente = _texto(cc.get("fuente"), f"{F}: curva_costes.fuente")
    mes = t.index.to_period("M").get_indexer([f_cc.to_period("M")])[0]
    if mes < 0:
        raise ErrorFicha(f"{F}: la curva de costes ({f_cc.date()}) no cae en un mes de la serie: no se puede deflactar")
    tramos = _acotada(cc.get("tramos"), f"{F}: curva_costes.tramos", u["tramos_maximos"])
    pares = sorted((_rango(_dict(tr, f"{F}: curva_costes.tramos[{i}]").get("coste"), f"{F}: tramos[{i}].coste", 0, abierto_lo=True),
                    _rango(tr.get("produccion"), f"{F}: tramos[{i}].produccion", 0, abierto_lo=True))
                   for i, tr in enumerate(tramos))
    acumulada = np.cumsum([prod for _, prod in pares])
    i_p = int(np.argmax(acumulada >= p["percentil_coste"] * acumulada[-1] * (1 - tol)))
    coste = pares[i_p][0]
    coste_real = coste * float(ipc[-1] / ipc[mes])
    res = {
        "moneda": moneda, "fecha": _iso(t.index[-1]), "n": n, "anios": n / MESES_ANIO,
        "precio_nominal_actual": float(precio[-1]), "precio_real_actual": actual, "base_moneda_constante": _iso(t.index[-1]),
        "percentil": pos["percentil"], "z": pos["z"], "media_real": pos["media"],
        "tendencia_real_pct_anual": anual(mk["pendiente_sen"]),
        "ic_tendencia_pct_anual": [anual(mk["ic_pendiente"][0]), anual(mk["ic_pendiente"][1])],
        "tendencia_direccion": mk["direccion"], "tendencia_p_valor": mk["p_valor"],
        "coste_marginal": {"percentil_coste": p["percentil_coste"], "coste_nominal": coste, "coste_real": coste_real,
                           "fecha": _iso(f_cc), "fuente": fuente, "n_tramos": len(pares)},
        "precio_sobre_coste": actual / coste_real,
        "referencia_ingenua": {"tipo": "RI-MH del precio real y RI-PA", "ri_mh": pos["media"], "ri_pa": actual},
        "verificacion": {  # «Verificación»: IPC constante ⇒ real = nominal
            "ipc_constante": bool(np.ptp(ipc) == 0),
            "diferencia_real_nominal_max": float(np.max(np.abs(real - precio) / precio))},
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== REI-LEV-001
@_cerrado("REI-LEV-001")
def f_rei_lev(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """REI-LEV-001 · Apalancamiento y riesgo de refinanciación (MC-09).

    ``valores``: ``fecha``; ``moneda``; ``coste_refinanciacion`` = {"swap", "margen" (el de mercado, si la petición no fija
    `margen`)}; ``componentes`` = lista de {"id", "gav" > 0, "deuda" > 0 (bruta), "caja" ≥ 0, "ebitda" > 0,
    "gastos_financieros" > 0, "ffo", "vencimientos": lista de {"fecha", "importe" > 0, "coste"} (el perfil completo: su
    suma es la deuda), opcional "covenants": {"ltv_max", "icr_min"}}.

    LTV = deuda neta/GAV [PROPUESTO: deuda neta, como EPRA]; ICR = EBITDA/gastos financieros. Impacto en FFO de
    refinanciar al coste actual los vencimientos a 24 meses: −Σ importe·(swap + margen − coste)/FFO.
    """
    F = "REI-LEV-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    tol = FICHAS[F]["tol"]
    lim: list[str] = []
    fecha = _fecha_dato(v, "fecha", _corte(ent), F)
    moneda = _texto(v.get("moneda"), f"{F}: «moneda»")
    cr = _dict(v.get("coste_refinanciacion"), f"{F}: «coste_refinanciacion»")
    lo_c, hi_c = u["rango_coste"]
    swap = _rango(cr.get("swap"), f"{F}: coste_refinanciacion.swap", lo_c, hi_c, abierto_lo=True, abierto_hi=True)
    if p["margen"] is not None:
        margen = p["margen"]
    else:
        lo_m, hi_m = u["rango_margen"]
        margen = _rango(cr.get("margen"), f"{F}: coste_refinanciacion.margen (o el parámetro margen)", lo_m, hi_m,
                        abierto_hi=True)
    coste_nuevo = swap + margen
    horizonte = fecha + pd.DateOffset(months=u["meses_vencimientos"])
    comps = _acotada(v.get("componentes"), f"{F}: componentes", u["componentes_maximos"])
    ids: list[str] = []
    col: dict[str, list[float]] = {k: [] for k in ("gav", "deuda", "neta", "ebitda", "gf", "ffo", "venc", "extra")}
    holg_ltv: list[float] = []
    holg_icr: list[float] = []
    caida_rompe: list[float] = []
    ltv_max: list[float] = []
    error = 0.0
    for i, c in enumerate(comps):
        que = f"{F}: componentes[{i}]"
        c = _dict(c, que)
        ids.append(_texto(c.get("id"), f"{que}.id"))
        gav = _rango(c.get("gav"), f"{que}.gav", 0, abierto_lo=True)
        deuda = _rango(c.get("deuda"), f"{que}.deuda", 0, abierto_lo=True)
        caja = _rango(c.get("caja"), f"{que}.caja", 0)
        ebitda = _rango(c.get("ebitda"), f"{que}.ebitda", 0, abierto_lo=True)
        gf = _rango(c.get("gastos_financieros"), f"{que}.gastos_financieros", 0, abierto_lo=True)
        ffo = _num(c.get("ffo"), f"{que}.ffo")
        if not isinstance(c.get("vencimientos"), list) or not c["vencimientos"]:
            raise ErrorFicha(f"{que}: rechazo: sin perfil de vencimientos")
        perfil = _tabla_acotada(c["vencimientos"], {"importe": (0, True), "coste": (lo_c, True)}, f"{que}.vencimientos",
                                u["vencimientos_maximos"])
        if perfil.index[0] < fecha:
            raise ErrorFicha(f"{que}.vencimientos: vencimiento del {perfil.index[0].date()} anterior a la fecha de los "
                             f"datos ({fecha.date()})")
        if float(perfil["coste"].max()) >= hi_c:
            raise ErrorFicha(f"{que}.vencimientos: coste fuera del rango admitido (máximo {hi_c:g}, excluido)")
        suma = float(perfil["importe"].sum())
        err = abs(suma - deuda) / deuda
        if err > tol:                                                   # «Verificación»: suma de vencimientos = deuda
            raise ErrorFicha(f"{que}: la suma de vencimientos ({suma:g}) no es la deuda ({deuda:g}): perfil incompleto")
        error = max(error, err)
        prox = perfil[perfil.index <= horizonte]
        for k, x in (("gav", gav), ("deuda", deuda), ("neta", deuda - caja), ("ebitda", ebitda), ("gf", gf), ("ffo", ffo),
                     ("venc", float(prox["importe"].sum())),
                     ("extra", float((prox["importe"] * (coste_nuevo - prox["coste"])).sum()))):
            col[k].append(x)
        if c.get("covenants") is not None:
            cov = _dict(c["covenants"], f"{que}.covenants")
            lmax = _rango(cov.get("ltv_max"), f"{que}.covenants.ltv_max", 0, 1, abierto_lo=True)
            imin = _rango(cov.get("icr_min"), f"{que}.covenants.icr_min", 0, abierto_lo=True)
            ltv_i = (deuda - caja) / gav
            holg_ltv.append((lmax - ltv_i) * PCT)
            holg_icr.append(ebitda / gf - imin)
            caida_rompe.append((ltv_i / lmax - 1) * PCT)                # variación del GAV que lleva el LTV a su máximo
            ltv_max.append(lmax)
    _ids_unicos(ids, F)
    a = {k: np.array(x) for k, x in col.items()}
    tot = {k: float(np.sum(x)) for k, x in a.items()}
    if not tot["ffo"] > 0:
        raise ErrorFicha(f"{F}: FFO agregado no positivo: el impacto en FFO no está definido")
    covenants: dict[str, Any] | None = None
    if holg_ltv:
        neta_cov = np.array([n_ for n_, c in zip(col["neta"], comps, strict=True) if c.get("covenants") is not None])
        gav_cov = np.array([g for g, c in zip(col["gav"], comps, strict=True) if c.get("covenants") is not None])
        lmax_a = np.array(ltv_max)
        covenants = {
            "n_componentes": len(holg_ltv),
            "holgura_ltv_pp": _distribucion(np.array(holg_ltv)), "holgura_icr_veces": _distribucion(np.array(holg_icr)),
            "caida_valor_que_agota_ltv_pct": _distribucion(np.array(caida_rompe)),
            "en_incumplimiento_pct": float(np.mean((np.array(holg_ltv) < 0) | (np.array(holg_icr) < 0))) * PCT,
            "en_incumplimiento_ltv_estresado_pct": {
                f"{c:g}": float(np.mean(neta_cov / (gav_cov * (1 + c)) > lmax_a)) * PCT for c in p["caidas_valor"]}}
        if len(holg_ltv) < len(comps):
            lim.append(f"covenants de {len(holg_ltv)} de {len(comps)} componentes: holgura sobre los declarados")
    else:
        lim.append("sin covenants declarados: holgura no calculada")
    res = {
        "moneda": moneda, "fecha": _iso(fecha), "n_componentes": len(comps),
        "ltv_pct": tot["neta"] / tot["gav"] * PCT, "icr_veces": tot["ebitda"] / tot["gf"],
        "deuda_neta_sobre_ebitda_veces": tot["neta"] / tot["ebitda"],
        "vencimientos_24m_pct": tot["venc"] / tot["deuda"] * PCT,
        "coste_refinanciacion": {"swap": swap, "margen": margen, "coste": coste_nuevo},
        "impacto_ffo_pct": -tot["extra"] / tot["ffo"] * PCT,
        "ltv_estresado_pct": {f"{c:g}": tot["neta"] / (tot["gav"] * (1 + c)) * PCT for c in p["caidas_valor"]},
        "dispersion": {"ltv_pct": _distribucion(a["neta"] / a["gav"] * PCT), "icr_veces": _distribucion(a["ebitda"] / a["gf"]),
                       "deuda_neta_sobre_ebitda_veces": _distribucion(a["neta"] / a["ebitda"]),
                       "vencimientos_24m_pct": _distribucion(a["venc"] / a["deuda"] * PCT)},
        "covenants": covenants,
        "referencia_ingenua": {"tipo": "RI-NA"},
        "verificacion": {"error_relativo_vencimientos_max": error},     # suma de vencimientos = deuda
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== CHR-ONCHAIN-001
@_cerrado("CHR-ONCHAIN-001")
def f_chr_onchain(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """CHR-ONCHAIN-001 · MVRV y NVT (MC-09).

    ``valores``: ``fuente`` = {"nombre", "metodologia", "filtros"} (la fuente en cadena declarada); ``serie`` = lista diaria
    consecutiva de {"fecha", "capitalizacion" > 0, "capitalizacion_realizada" > 0, "volumen_ajustado" > 0}.

    MVRV = CM/CR; MVRV-Z = (CM − CR)/σ(CM) con σ muestral de toda la ventana; NVT = CM/volumen; señal NVT = CM/media
    móvil del volumen (`media_nvt` días); percentil de cada medida en su historia disponible.
    """
    F = "CHR-ONCHAIN-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    lim: list[str] = []
    fu = v.get("fuente")
    if not isinstance(fu, dict) or any(not isinstance(fu.get(k), str) or not fu[k].strip()
                                       for k in ("nombre", "metodologia", "filtros")):
        raise ErrorFicha(f"{F}: rechazo: sin fuente en cadena verificable (fuente.nombre, metodologia y filtros)")
    fuente = fu["nombre"].strip()
    if p["fuente"] is not None and p["fuente"] != fuente:
        raise ErrorFicha(f"{F}: los datos son de la fuente «{fuente[:40]}» y la petición pide «{p['fuente'][:40]}»")
    t = _tabla_acotada(v.get("serie"), {"capitalizacion": (0, True), "capitalizacion_realizada": (0, True),
                                        "volumen_ajustado": (0, True)}, f"{F}: serie", u["dias_maximos"])
    _hasta_corte(t.index, _corte(ent), f"{F}: serie")
    _consecutivas(t.index, "D", f"{F}: serie")
    n = len(t)
    if n < u["dias_minimos"]:
        raise ErrorFicha(f"{F}: {n} días (< {u['dias_minimos']}, 2 años): entradas mínimas")
    if n < u["dias_recomendados"]:
        lim.append(f"pocos ciclos: {n} días de historia (< {u['dias_recomendados']}, 4 años recomendados)")
    cm, cr = t["capitalizacion"].to_numpy(), t["capitalizacion_realizada"].to_numpy()
    vol = t["volumen_ajustado"].to_numpy()
    sd = float(np.std(cm, ddof=1))
    if not sd > 0:
        raise ErrorFicha(f"{F}: capitalización sin dispersión: MVRV-Z indefinido")
    mvrv, z, nvt = cm / cr, (cm - cr) / sd, cm / vol
    w = p["media_nvt"]
    senal = cm[w - 1:] / (np.convolve(vol, np.ones(w), "valid") / w)   # media móvil de `w` días, hasta cada día
    res = {
        "fuente": fuente, "fecha": _iso(t.index[-1]), "n_dias": n,
        "mvrv": float(mvrv[-1]), "mvrv_z": float(z[-1]), "nvt": float(nvt[-1]), "senal_nvt": float(senal[-1]),
        "media_nvt_dias": w,
        "percentiles": {"mvrv": _posicion(float(mvrv[-1]), mvrv)["percentil"], "mvrv_z": _posicion(float(z[-1]), z)["percentil"],
                        "nvt": _posicion(float(nvt[-1]), nvt)["percentil"],
                        "senal_nvt": _posicion(float(senal[-1]), senal)["percentil"]},
        "referencia_ingenua": {"tipo": "RI-PA y RI-CM (índice cripto de gran capitalización)"},
        "verificacion": {"capitalizacion_sobre_realizada": float(cm[-1] / cr[-1])},   # MVRV = 1 si precio = coste medio
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== CHR-TOKEN-001
@_cerrado("CHR-TOKEN-001")
def f_chr_token(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """CHR-TOKEN-001 · Tokenómica y dilución (MC-09).

    ``valores``: ``fecha``; ``fuente``; ``ambito`` (la red o el sector del ecosistema); ``tokens`` = lista de {"id",
    "precio" > 0, "oferta_circulante" > 0, "oferta_total", "oferta_maxima" (o null si no tiene tope), "emision_anual" ≥ 0,
    "quema_anual" ≥ 0 (unidades del token), "calendario": {"fuente", "desbloqueos": lista de {"fecha", "cantidad" > 0}},
    opcionales "staking_nominal" (tanto por uno anual) y "concentracion_10_mayores" ∈ [0, 1]}.

    Agregado ponderado por capitalización circulante: FDV/CM = Σ precio·oferta máxima (o total, sin tope) / Σ precio·
    circulante; inflación neta = Σ precio·(emisión − quema)/Σ CM; desbloqueos a w días = Σ precio·cantidad con fecha en
    (fecha, fecha + w] / Σ CM; rendimiento real de staking = nominal − inflación neta.
    """
    F = "CHR-TOKEN-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    tol = FICHAS[F]["tol"]
    lim: list[str] = []
    fecha = _fecha_dato(v, "fecha", _corte(ent), F)
    fuente = _texto(v.get("fuente"), f"{F}: «fuente»")
    ambito = _texto(v.get("ambito"), f"{F}: «ambito» (red o sector del ecosistema)")
    tokens = _acotada(v.get("tokens"), f"{F}: tokens", u["tokens_maximos"])
    ventanas = p["ventanas_desbloqueo"]
    ids: list[str] = []
    cm: list[float] = []
    fdv: list[float] = []
    neta: list[float] = []
    desb: dict[int, list[float]] = {w: [] for w in ventanas}
    staking: list[tuple[float, float]] = []
    conc: list[tuple[float, float]] = []
    pasados, holgura = 0, math.inf
    for i, tk in enumerate(tokens):
        que = f"{F}: tokens[{i}]"
        tk = _dict(tk, que)
        ids.append(_texto(tk.get("id"), f"{que}.id"))
        precio = _rango(tk.get("precio"), f"{que}.precio", 0, abierto_lo=True)
        circ = _rango(tk.get("oferta_circulante"), f"{que}.oferta_circulante", 0, abierto_lo=True)
        total = _rango(tk.get("oferta_total"), f"{que}.oferta_total", 0, abierto_lo=True)
        maxima = None if tk.get("oferta_maxima") is None else _rango(tk["oferta_maxima"], f"{que}.oferta_maxima", 0,
                                                                     abierto_lo=True)
        if circ > total or (maxima is not None and total > maxima):     # «Verificación»: circulante ≤ total ≤ máxima
            raise ErrorFicha(f"{que}: ofertas incoherentes: debe cumplirse circulante ≤ total ≤ máxima")
        emision = _rango(tk.get("emision_anual"), f"{que}.emision_anual", 0)
        quema = _rango(tk.get("quema_anual"), f"{que}.quema_anual", 0)
        cal = tk.get("calendario")
        if not isinstance(cal, dict) or not isinstance(cal.get("fuente"), str) or not cal["fuente"].strip() \
                or not isinstance(cal.get("desbloqueos"), list):
            raise ErrorFicha(f"{que}: rechazo: sin calendario de desbloqueos verificable (calendario.fuente y desbloqueos)")
        if len(cal["desbloqueos"]) > u["desbloqueos_maximos"]:
            raise ErrorFicha(f"{que}.calendario: {len(cal['desbloqueos'])} desbloqueos (máximo {u['desbloqueos_maximos']})")
        futuros: list[tuple[pd.Timestamp, float]] = []
        for j, d in enumerate(cal["desbloqueos"]):
            d = _dict(d, f"{que}.calendario.desbloqueos[{j}]")
            f_d = _fecha(d.get("fecha"), f"{que}.calendario.desbloqueos[{j}].fecha")
            cantidad = _rango(d.get("cantidad"), f"{que}.calendario.desbloqueos[{j}].cantidad", 0, abierto_lo=True)
            if f_d > fecha:
                futuros.append((f_d, cantidad))
            else:
                pasados += 1
        bloqueada = total - circ
        pendiente = math.fsum(c for _, c in futuros)
        if pendiente > bloqueada * (1 + tol) + tol * total:
            raise ErrorFicha(f"{que}: los desbloqueos futuros ({pendiente:g}) superan la oferta no circulante "
                             f"({bloqueada:g}): calendario u ofertas incoherentes")
        holgura = min(holgura, (bloqueada - pendiente) / total)
        cm_i = precio * circ
        cm.append(cm_i)
        fdv.append(precio * (maxima if maxima is not None else total))
        neta.append((emision - quema) / circ)
        for w in ventanas:
            limite = fecha + pd.Timedelta(days=w)
            desb[w].append(math.fsum(c for f_d, c in futuros if f_d <= limite) / circ)
        if tk.get("staking_nominal") is not None:
            lo, hi = u["rango_staking"]
            staking.append((cm_i, _rango(tk["staking_nominal"], f"{que}.staking_nominal", lo, hi, abierto_lo=True,
                                         abierto_hi=True) - neta[-1]))
        if tk.get("concentracion_10_mayores") is not None:
            conc.append((cm_i, _rango(tk["concentracion_10_mayores"], f"{que}.concentracion_10_mayores", 0, 1)))
    _ids_unicos(ids, F)
    if pasados:
        lim.append(f"{pasados} desbloqueos del calendario con fecha no posterior a la de los datos: ya están en la oferta "
                   f"circulante y no cuentan como dilución futura")
    a_cm = np.array(cm)
    w_cm = a_cm / float(np.sum(a_cm))
    a_fdv, a_neta = np.array(fdv) / a_cm, np.array(neta)

    def parcial(pares: list[tuple[float, float]], que: str) -> tuple[float | None, float]:
        if not pares:
            lim.append(f"sin {que} declarado: no calculado")
            return None, 0.0
        peso = float(sum(c for c, _ in pares))
        if len(pares) < len(tokens):
            lim.append(f"{que} de {len(pares)} de {len(tokens)} tokens: media ponderada sobre los declarados")
        return float(sum(c * x for c, x in pares)) / peso * PCT, peso / float(np.sum(a_cm)) * PCT

    real, cob_staking = parcial(staking, "rendimiento de staking")
    concentracion, cob_conc = parcial(conc, "dato de concentración de tenedores")
    res = {
        "ambito": ambito, "fecha": _iso(fecha), "fuente": fuente, "n_tokens": len(tokens),
        "capitalizacion_circulante": float(np.sum(a_cm)),
        "fdv_sobre_capitalizacion_veces": float(np.sum(fdv)) / float(np.sum(a_cm)),
        "inflacion_neta_pct_anual": float(w_cm @ a_neta) * PCT,
        "desbloqueos_pct": {str(w): float(w_cm @ np.array(desb[w])) * PCT for w in ventanas},
        "rendimiento_real_staking_pct": real, "cobertura_staking_pct": cob_staking,
        "concentracion_10_mayores_pct": concentracion, "cobertura_concentracion_pct": cob_conc,
        "dispersion": {"fdv_sobre_capitalizacion_veces": _distribucion(a_fdv),
                       "inflacion_neta_pct_anual": _distribucion(a_neta * PCT)},
        "referencia_ingenua": {"tipo": "RI-NA"},
        "verificacion": {"circulante_le_total_le_maxima": True,       # se rechaza si no se cumple
                         "holgura_desbloqueos_min": holgura},          # (no circulante − desbloqueos futuros)/total ≥ 0
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== PRV-PME-001 y PRV-CF-001: flujos y TIR
def _tir(dias: np.ndarray, flujos: np.ndarray, u: dict[str, Any], lim: list[str], que: str) -> float | None:
    """TIR anual (Real/365) de unos flujos fechados: Σ F_i/(1 + r)^{t_i} = 0. Sin cambio de signo no está definida; con
    más de uno puede haber varias soluciones y se avisa (PRV-CF-001, «Método»). La raíz se busca en `rango_tir`."""
    signos = np.sign(flujos[flujos != 0])
    cambios = int(np.sum(signos[1:] != signos[:-1]))
    if cambios == 0:
        lim.append(f"{que}: flujos sin cambio de signo: TIR no definida")
        return None
    if cambios > 1:
        lim.append(f"{que}: {cambios} cambios de signo en los flujos: la TIR puede tener múltiples soluciones")
    t = (dias - dias[0]) / DIAS_ANIO

    def van(r: float) -> float:
        return float(np.sum(flujos * (1 + r) ** (-t)))

    lo, hi = u["rango_tir"]
    if not van(lo) * van(hi) < 0:
        lim.append(f"{que}: sin TIR entre {lo:g} y {hi:g}")
        return None
    return float(optimize.brentq(van, lo, hi, xtol=u["tolerancia_raiz"], rtol=u["tolerancia_raiz"],
                                 maxiter=u["iteraciones_maximas"]))


def _flujos_privados(v: dict[str, Any], corte: pd.Timestamp | None, u: dict[str, Any], F: str) -> pd.DataFrame:
    """Flujos agregados fechados de la cosecha o segmento: {"fecha", "aportacion" ≥ 0, "distribucion" ≥ 0}."""
    if not isinstance(v.get("flujos"), list) or not v["flujos"]:
        raise ErrorFicha(f"{F}: rechazo: sin flujos fechados")
    fl = _tabla_acotada(v["flujos"], {"aportacion": (0, False), "distribucion": (0, False)}, f"{F}: flujos",
                        u["flujos_maximos"])
    _hasta_corte(fl.index, corte, f"{F}: flujos")
    if (fl.index[-1] - fl.index[0]).days > u["anios_historia_maximos"] * DIAS_ANIO:
        raise ErrorFicha(f"{F}: flujos de más de {u['anios_historia_maximos']} años")
    if not float(fl["aportacion"].sum()) > 0:
        raise ErrorFicha(f"{F}: sin aportaciones: los múltiplos no están definidos")
    return fl


def _dias(indice: pd.DatetimeIndex) -> np.ndarray:
    return np.asarray((indice - indice[0]).days, dtype=float)


def _con_nav(fl: pd.DataFrame, neto: np.ndarray, f_nav: pd.Timestamp, nav: float) -> tuple[np.ndarray, np.ndarray]:
    """Flujos netos con el NAV como último flujo, en su fecha (que no es anterior al último flujo)."""
    if f_nav == fl.index[-1]:
        return _dias(fl.index), np.concatenate([neto[:-1], [neto[-1] + nav]])
    return _dias(fl.index.append(pd.DatetimeIndex([f_nav]))), np.concatenate([neto, [nav]])


@_cerrado("PRV-PME-001")
def f_prv_pme(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """PRV-PME-001 · Public market equivalent (MC-09).

    ``valores``: ``moneda``; ``flujos`` = lista de {"fecha", "aportacion" ≥ 0, "distribucion" ≥ 0} agregados de la cosecha
    o segmento; ``nav_final`` = {"fecha", "valor" ≥ 0}; ``indice`` = {"nombre", "moneda", "rentabilidad_total": true,
    "riesgo_comparable" (declaración), "niveles": lista de {"fecha", "nivel" > 0}} con un nivel en cada fecha de flujo y en
    la del NAV (no se interpola).

    KS-PME = [Σ D_t·(I_T/I_t) + NAV_T]/Σ C_t·(I_T/I_t). Alfa directo (Gredil, Griffiths y Stucke) = ln(1 + TIR de los flujos
    capitalizados con el índice). PME+ (con `metodo: PME+`): λ = (Σ C·I_T/I_t − NAV_T)/Σ D·I_T/I_t y TIR de −C + λ·D con el
    NAV. LN-PME no se calcula (la ficha no le da parámetro) [PROPUESTO].
    """
    F = "PRV-PME-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    corte = _corte(ent)
    lim: list[str] = []
    moneda = _texto(v.get("moneda"), f"{F}: «moneda»")
    fl = _flujos_privados(v, corte, u, F)
    nd = _dict(v.get("nav_final"), f"{F}: «nav_final»")
    f_nav = _fecha_dato(nd, "fecha", corte, f"{F}: nav_final")
    nav = _rango(nd.get("valor"), f"{F}: nav_final.valor", 0)
    if f_nav < fl.index[-1]:
        raise ErrorFicha(f"{F}: el NAV final ({f_nav.date()}) es anterior al último flujo ({fl.index[-1].date()})")
    ind = _dict(v.get("indice"), f"{F}: «indice»")
    nombre = _texto(ind.get("nombre"), f"{F}: indice.nombre")
    if p["indice"] is not None and p["indice"] != nombre:
        raise ErrorFicha(f"{F}: los datos son del índice «{nombre[:40]}» y la petición pide «{p['indice'][:40]}»")
    if _texto(ind.get("moneda"), f"{F}: indice.moneda") != moneda:
        raise ErrorFicha(f"{F}: el índice debe estar en la misma moneda que los flujos ({moneda})")
    if ind.get("rentabilidad_total") is not True:
        raise ErrorFicha(f"{F}: el índice debe ser de rentabilidad total (indice.rentabilidad_total: true)")
    riesgo = _texto(ind.get("riesgo_comparable"), f"{F}: indice.riesgo_comparable (declaración)")
    niveles = _tabla_acotada(ind.get("niveles"), {"nivel": (0, True)}, f"{F}: indice.niveles",
                             u["flujos_maximos"] + 1)["nivel"]
    _hasta_corte(niveles.index, corte, f"{F}: indice.niveles")
    faltan = [f for f in [*fl.index, f_nav] if f not in niveles.index]
    if faltan:
        raise ErrorFicha(f"{F}: el índice no tiene nivel en {len(faltan)} fechas de flujo o del NAV "
                         f"(la primera, {faltan[0].date()}): no se interpola")
    factor = float(niveles[f_nav]) / niveles.reindex(fl.index).to_numpy()   # I_T/I_t
    C, D = fl["aportacion"].to_numpy(), fl["distribucion"].to_numpy()
    vf_c, vf_d = float(np.sum(C * factor)), float(np.sum(D * factor))
    ks = (vf_d + nav) / vf_c
    tir = _tir(*_con_nav(fl, D - C, f_nav, nav), u, lim, "TIR")
    capitalizada = _tir(*_con_nav(fl, (D - C) * factor, f_nav, nav), u, lim, "alfa directo")
    plus: dict[str, Any] | None = None
    if p["metodo"] == "PME+":
        if not vf_d > 0:
            lim.append("PME+: sin distribuciones, el factor λ no está definido")
        else:
            lam = (vf_c - nav) / vf_d
            tir_ind = _tir(*_con_nav(fl, lam * D - C, f_nav, nav), u, lim, "PME+")
            plus = {"lambda": lam, "tir_indice_pct": None if tir_ind is None else tir_ind * PCT,
                    "diferencial_tir_pct": None if tir is None or tir_ind is None else (tir - tir_ind) * PCT}
    res = {
        "metodo": p["metodo"], "moneda": moneda, "indice": nombre, "riesgo_comparable": riesgo,
        "fecha_nav": _iso(f_nav), "n_flujos": len(fl),
        "ks_pme_veces": ks,
        "alfa_directo_pct_anual": None if capitalizada is None else math.log1p(capitalizada) * PCT,
        "tir_pct": None if tir is None else tir * PCT,
        "tvpi_veces": (float(np.sum(D)) + nav) / float(np.sum(C)), "dpi_veces": float(np.sum(D)) / float(np.sum(C)),
        "pme_plus": plus,
        "valor_futuro": {"aportaciones": vf_c, "distribuciones": vf_d, "nav_final": nav},
        "referencia_ingenua": {"tipo": "índice cotizado (PME = 1)", "exceso_ks_pme": ks - 1},
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


def _takahashi_alexander(compromiso: float, aportado: float, nav: float, edad: int, vida: int, tasas: list[float],
                         bow: float, g: float, y_min: float) -> list[dict[str, float]]:
    """Takahashi y Alexander (2002), por año de vida t = edad + 1 … vida: C_t = RC_t·(compromiso − aportado);
    D_t = max(Y, (t/vida)^bow)·NAV_{t−1}·(1 + g); NAV_t = NAV_{t−1}·(1 + g) + C_t − D_t."""
    serie = []
    for t in range(edad + 1, vida + 1):
        c = tasas[min(t, len(tasas)) - 1] * max(compromiso - aportado, 0.0)
        d = max(y_min, (t / vida) ** bow) * nav * (1 + g)
        nav = nav * (1 + g) + c - d
        aportado += c
        serie.append({"anio_vida": t, "aportacion": c, "distribucion": d, "nav": nav})
    return serie


@_cerrado("PRV-CF-001")
def f_prv_cf(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """PRV-CF-001 · TIR, múltiplos, curva J y proyección de flujos (MC-09).

    ``valores``: ``compromiso`` > 0; ``flujos`` = lista de {"fecha", "aportacion" ≥ 0, "distribucion" ≥ 0} agregados;
    ``navs`` = lista de {"fecha", "valor" ≥ 0} (el último, no anterior al último flujo, es el NAV actual); opcionales
    ``vida_anios`` (vida de la cosecha, para la proyección) y ``referencia_cosecha`` = {"tvpi_mediana", "tir_mediana"}.

    Curva J = flujo neto acumulado (distribuciones − aportaciones) en cada fecha de flujo, sobre el compromiso. La
    proyección necesita `tasas_aportacion`, `crecimiento` y `vida_anios`; la edad es el número de años completos desde el
    primer flujo; la tasa del último año declarado se mantiene en los siguientes [PROPUESTO].
    """
    F = "PRV-CF-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    corte = _corte(ent)
    lim: list[str] = []
    compromiso = _rango(v.get("compromiso"), f"{F}: «compromiso»", 0, abierto_lo=True)
    fl = _flujos_privados(v, corte, u, F)
    navs = _tabla_acotada(v.get("navs"), {"valor": (0, False)}, f"{F}: navs (fechados)", u["navs_maximos"])["valor"]
    _hasta_corte(navs.index, corte, f"{F}: navs")
    f_nav, nav = navs.index[-1], float(navs.iloc[-1])
    if f_nav < fl.index[-1]:
        raise ErrorFicha(f"{F}: el último NAV ({f_nav.date()}) es anterior al último flujo ({fl.index[-1].date()})")
    C, D = fl["aportacion"].to_numpy(), fl["distribucion"].to_numpy()
    aportado, distribuido = float(np.sum(C)), float(np.sum(D))
    if aportado > compromiso:
        lim.append("aportaciones por encima del compromiso (distribuciones reaportables): compromiso pendiente nulo")
    tir = _tir(*_con_nav(fl, D - C, f_nav, nav), u, lim, "TIR")
    acumulado = np.cumsum(D - C)
    i_min = int(np.argmin(acumulado))
    proyeccion: dict[str, Any] | None = None
    falta = [k for k, x in (("tasas_aportacion", p["tasas_aportacion"]), ("crecimiento", p["crecimiento"]),
                            ("vida_anios", v.get("vida_anios"))) if x is None]
    if falta:
        lim.append(f"sin {', '.join(falta)} (supuestos que declara el solicitante): proyección no calculada")
    else:
        vida = _entero(v["vida_anios"], f"{F}: vida_anios", 1, u["vida_maxima_anios"])
        edad = int((f_nav - fl.index[0]).days // DIAS_ANIO)
        serie = _takahashi_alexander(compromiso, aportado, nav, edad, vida, p["tasas_aportacion"], p["bow"],
                                     p["crecimiento"], u["rendimiento_minimo"])
        if not serie:
            lim.append(f"la cosecha ya ha cumplido su vida ({edad} de {vida} años): proyección vacía")
        ap_f = aportado + math.fsum(s["aportacion"] for s in serie)
        di_f = distribuido + math.fsum(s["distribucion"] for s in serie)
        nav_f = serie[-1]["nav"] if serie else nav
        proyeccion = {"edad_anios": edad, "vida_anios": vida, "bow": p["bow"], "crecimiento": p["crecimiento"],
                      "tasas_aportacion": list(p["tasas_aportacion"]), "serie": serie,
                      "tvpi_final_veces": (di_f + nav_f) / ap_f, "dpi_final_veces": di_f / ap_f,
                      "aportado_final_sobre_compromiso": ap_f / compromiso}
    ref: dict[str, Any] = {"tipo": "mediana de la cosecha y estrategia", "tvpi_mediana": None, "tir_mediana_pct": None,
                           "diferencia_tvpi": None, "diferencia_tir_pct": None}
    tvpi = (distribuido + nav) / aportado
    if v.get("referencia_cosecha") is None:
        lim.append("sin mediana de la cosecha y estrategia: referencia ingenua no comparada")
    else:
        rc = _dict(v["referencia_cosecha"], f"{F}: «referencia_cosecha»")
        ref["tvpi_mediana"] = _rango(rc.get("tvpi_mediana"), f"{F}: referencia_cosecha.tvpi_mediana", 0)
        lo, hi = u["rango_tir"]
        ref["tir_mediana_pct"] = _rango(rc.get("tir_mediana"), f"{F}: referencia_cosecha.tir_mediana", lo, hi) * PCT
        ref["diferencia_tvpi"] = tvpi - ref["tvpi_mediana"]
        ref["diferencia_tir_pct"] = None if tir is None else tir * PCT - ref["tir_mediana_pct"]
    res = {
        "fecha_nav": _iso(f_nav), "n_flujos": len(fl), "compromiso": compromiso,
        "aportado_sobre_compromiso": aportado / compromiso,
        "tir_pct": None if tir is None else tir * PCT,
        "tvpi_veces": tvpi, "dpi_veces": distribuido / aportado, "rvpi_veces": nav / aportado,
        "curva_j": {"serie": [{"fecha": _iso(f), "flujo_neto_acumulado": float(x), "sobre_compromiso": float(x) / compromiso}
                              for f, x in zip(fl.index, acumulado, strict=True)],
                    "minimo_sobre_compromiso": float(acumulado[i_min]) / compromiso, "fecha_minimo": _iso(fl.index[i_min])},
        "proyeccion": proyeccion,
        "referencia_ingenua": ref,
        "verificacion": {"tvpi_menos_dpi_menos_rvpi": tvpi - distribuido / aportado - nav / aportado},   # TVPI = DPI + RVPI
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== ALT-HF-001
@_cerrado("ALT-HF-001")
def f_alt_hf(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """ALT-HF-001 · Exposición factorial de estrategias hedge (MC-09).

    ``valores``: ``serie`` = lista mensual consecutiva de {"fecha", "r" (% del mes, del índice de la estrategia o del
    agregado de la categoría), "rf" (% del mes; o ``en_exceso: true`` sin "rf"), y un valor (% del mes) por factor}. Los
    factores son los siete de Fung y Hsieh (MKT, SMB, BONO10A, CREDITO, PTFSBD, PTFSFX, PTFSCOM) o los que declare la
    petición en `factores`.

    Con `desuavizar`, antes de la regresión se aplica el Geltner de ALT-DESMOOTH-001 con φ = AR(1) estimado (se pierde la
    primera observación). Regresión y Newey-West, los de ACC-FACT-001 (L = ⌊4·(T/100)^{2/9}⌋).
    """
    F = "ALT-HF-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    lim: list[str] = []
    nombres = list(u["factores_fung_hsieh"]) if p["factores"] == "Fung-Hsieh 7" else list(p["factores"])
    campos: dict[str, tuple[float | None, bool]] = dict.fromkeys(["r", "rf", *nombres], (None, False))
    t = _tabla_acotada(v.get("serie"), campos, f"{F}: serie", u["anios_historia_maximos"] * MESES_ANIO, opcionales=("rf",))
    _hasta_corte(t.index, _corte(ent), f"{F}: serie")
    _consecutivas(t.index, "M", f"{F}: serie")
    n = len(t)
    if n < u["observaciones_minimas"]:
        raise ErrorFicha(f"{F}: rechazo: {n} observaciones mensuales (< {u['observaciones_minimas']})")
    r, rf, Fm = t["r"].to_numpy(), t["rf"].to_numpy(), t[nombres].to_numpy()
    sin_rf = np.isnan(rf)
    if v.get("en_exceso") is True:
        if not bool(np.all(sin_rf)):
            raise ErrorFicha(f"{F}: «en_exceso»: true y «rf» a la vez: declare solo uno")
        rf = np.zeros(n)
    elif bool(np.any(sin_rf)):
        raise ErrorFicha(f"{F}: falta «rf» en {int(np.sum(sin_rf))} meses (o declare «en_exceso»: true)")
    phi: float | None = None
    if p["desuavizar"]:
        phi = _ar1(r)
        if not -1 < phi < 1:
            raise ErrorFicha(f"{F}: φ del AR(1) fuera de (−1, 1) o indefinido: no se puede desuavizar")
        if phi < 0:
            lim.append(f"φ estimado negativo ({phi:.4f}): sin evidencia de suavizado")
        r, rf, Fm = (r[1:] - phi * r[:-1]) / (1 - phi), rf[1:], Fm[1:]   # Geltner (ALT-DESMOOTH-001)
    y = r - rf
    X = np.column_stack([np.ones(len(y)), Fm])
    if len(y) <= X.shape[1] or np.linalg.matrix_rank(X) < X.shape[1]:
        raise ErrorFicha(f"{F}: regresión no identificada (pocas observaciones o factores colineales)")
    base = fv._regresion(y, Fm, nombres, MESES_ANIO, lim, F)
    media = float(np.mean(y))
    pasiva = float(sum(base["betas"][nb]["beta"] * float(np.mean(Fm[:, j])) for j, nb in enumerate(nombres)))
    res = {
        "factores": nombres, "fecha": _iso(t.index[-1]), "n_observaciones": n,
        "desuavizado": {"aplicado": p["desuavizar"], "phi": phi},
        **base,
        "descomposicion_media_pct": {"total": media, "por_factores": pasiva, "alfa": base["alfa_periodo_pct"]},
        "referencia_ingenua": {"tipo": "cartera pasiva de factores", "rentabilidad_media_periodo_pct": pasiva,
                               "exceso_periodo_pct": media - pasiva},
        "verificacion": {"error_identidad_media": abs(media - pasiva - base["alfa_periodo_pct"])},
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== ALT-AUC-001
def _indice(coef: np.ndarray) -> np.ndarray:
    """Índice base 100 en el primer periodo a partir de los efectos temporales en logaritmos."""
    return BASE_INDICE * np.exp(np.concatenate([[0.0], coef]))


def _ventas_repetidas(ids: list[str], fechas: list[pd.Timestamp], lp: np.ndarray, per: np.ndarray, P: int) -> dict[str, Any]:
    """Bailey, Muth y Nourse (1963): ln(P_venta/P_compra) = β_venta − β_compra + ε por MCO, con pares de ventas
    consecutivas de la misma pieza en periodos distintos. Devuelve el índice, o el motivo por el que no se identifica."""
    orden = sorted(range(len(ids)), key=lambda i: (ids[i], fechas[i], i))
    pares = [(a, b) for a, b in pairwise(orden) if ids[a] == ids[b]]
    utiles = [(a, b) for a, b in pares if per[a] != per[b]]
    out: dict[str, Any] = {"n_pares": len(utiles), "descartados": len(pares) - len(utiles), "indice": None, "motivo": None}
    if not utiles:
        out["motivo"] = "sin pares de ventas repetidas en periodos distintos"
        return out
    M = np.zeros((len(utiles), P))
    filas = np.arange(len(utiles))
    M[filas, per[[b for _, b in utiles]]] = 1.0
    M[filas, per[[a for a, _ in utiles]]] = -1.0
    M = M[:, 1:]                                                       # el primer periodo es la base (β = 0)
    y = lp[[b for _, b in utiles]] - lp[[a for a, _ in utiles]]
    if len(utiles) <= P - 1:
        out["motivo"] = "el índice de ventas repetidas no se identifica (menos pares que periodos)"
        return out
    beta, _, rango, _ = np.linalg.lstsq(M, y, rcond=None)
    if rango < P - 1:
        out["motivo"] = "el índice de ventas repetidas no se identifica (periodos sin pares que los enlacen)"
        return out
    e = y - M @ beta
    out.update({"indice": _indice(beta), "residuos": e, "gl": len(utiles) - (P - 1)})
    return out


def _hedonico(lp: np.ndarray, per: np.ndarray, P: int, car: np.ndarray | None) -> dict[str, Any]:
    """Regresión hedónica: ln P = c + γ'x + δ_periodo + ε, con efectos temporales (el primer periodo es la base)."""
    out: dict[str, Any] = {"indice": None, "motivo": None}
    if car is None:
        out["motivo"] = "sin características en todas las transacciones"
        return out
    dum = np.zeros((len(lp), P))
    dum[np.arange(len(lp)), per] = 1.0
    X = np.column_stack([np.ones(len(lp)), car, dum[:, 1:]])
    if len(lp) <= X.shape[1]:
        out["motivo"] = "la regresión hedónica no se identifica (menos transacciones que coeficientes)"
        return out
    b, _, rango, _ = np.linalg.lstsq(X, lp, rcond=None)
    if rango < X.shape[1]:
        out["motivo"] = "la regresión hedónica no se identifica (características colineales o constantes)"
        return out
    out.update({"indice": _indice(b[1 + car.shape[1]:]), "residuos": lp - X @ b, "gl": len(lp) - X.shape[1]})
    return out


def _caracteristicas(trans: list[dict[str, Any]], maximo: int, F: str) -> tuple[list[str], np.ndarray | None]:
    """Matriz de características si todas las transacciones las traen, con las mismas claves; si ninguna o solo algunas,
    ``None`` (las claves distintas entre transacciones que sí las traen se rechazan)."""
    con = [tr.get("caracteristicas") for tr in trans]
    if any(c is None for c in con):
        return [], None
    claves = sorted(_dict(con[0], f"{F}: transacciones[0].caracteristicas"))
    if len(claves) > maximo or not all(isinstance(k, str) for k in claves):
        raise ErrorFicha(f"{F}: características: {len(claves)} (máximo {maximo}), con nombre de texto")
    M = np.empty((len(con), len(claves)))
    for i, c in enumerate(con):
        if not isinstance(c, dict) or sorted(c, key=str) != claves:
            raise ErrorFicha(f"{F}: transacciones[{i}].caracteristicas: no son las mismas que las de la primera transacción")
        M[i] = [_num(c[k], f"{F}: transacciones[{i}].caracteristicas.{k}") for k in claves]
    return claves, M


@_cerrado("ALT-AUC-001")
def f_alt_auc(ent: dict[str, Any], params: dict[str, Any]) -> Resultado:
    """ALT-AUC-001 · Índice de transacciones de coleccionables (MC-09; regresión hedónica con MC-03 de invitado).

    ``valores``: ``categoria``; ``transacciones`` = lista (≥ 500) de {"id_pieza", "fecha", "precio" > 0, opcional
    "caracteristicas": {nombre: número}}; opcional ``referencia`` = {"inflacion_anual", "rv_global_anual"} (tanto por uno).

    Índice anual [PROPUESTO], base 100 en el primer año. Rentabilidad anual bruta = (I_final/I_inicial)^{1/años} − 1;
    volatilidad = desviación de las variaciones anuales del índice; dispersión = desviación e IQR de los residuos de la
    regresión (logaritmos, %). Neta de comisiones: una compraventa en toda la ventana del índice [PROPUESTO]. La segunda
    vía es el otro método, si los datos lo permiten.
    """
    F = "ALT-AUC-001"
    p, u, v = _parametros(F, params), UMBRALES[F], ent["valores"]
    lim: list[str] = []
    categoria = _texto(v.get("categoria"), f"{F}: «categoria»")
    trans = v.get("transacciones")
    if isinstance(trans, list) and len(trans) < u["transacciones_minimas"]:
        raise ErrorFicha(f"{F}: rechazo: {len(trans)} transacciones (< {u['transacciones_minimas']})")
    trans = _acotada(trans, f"{F}: transacciones", u["transacciones_maximas"])
    ids: list[str] = []
    fechas: list[pd.Timestamp] = []
    precios: list[float] = []
    for i, tr in enumerate(trans):
        tr = _dict(tr, f"{F}: transacciones[{i}]")
        ids.append(_texto(tr.get("id_pieza"), f"{F}: transacciones[{i}].id_pieza"))
        fechas.append(_fecha(tr.get("fecha"), f"{F}: transacciones[{i}].fecha"))
        precios.append(_rango(tr.get("precio"), f"{F}: transacciones[{i}].precio", 0, abierto_lo=True))
    _hasta_corte(fechas, _corte(ent), f"{F}: transacciones")
    anios = np.array([f.year for f in fechas])
    primero, P = int(anios.min()), int(anios.max() - anios.min()) + 1
    if P > u["anios_historia_maximos"]:
        raise ErrorFicha(f"{F}: transacciones de {P} años (máximo {u['anios_historia_maximos']})")
    if P < u["periodos_minimos"]:
        raise ErrorFicha(f"{F}: transacciones de {P} años (< {u['periodos_minimos']}): sin índice ni volatilidad")
    per = anios - primero
    if len(np.unique(per)) < P:
        raise ErrorFicha(f"{F}: hay años sin transacciones entre {primero} y {primero + P - 1}: el índice no se identifica")
    lp = np.log(np.array(precios))
    claves, car = _caracteristicas(trans, u["caracteristicas_maximas"], F)
    vr = _ventas_repetidas(ids, fechas, lp, per, P)
    if vr["indice"] is not None and vr["n_pares"] < u["pares_minimos"]:
        vr.update({"indice": None, "motivo": f"{vr['n_pares']} pares de ventas repetidas (< {u['pares_minimos']})"})
    elif vr["indice"] is None and vr["n_pares"] < u["pares_minimos"]:
        vr["motivo"] = f"{vr['n_pares']} pares de ventas repetidas (< {u['pares_minimos']})"
    he = _hedonico(lp, per, P, car)
    principal, otra = (vr, he) if p["metodo"] == "ventas_repetidas" else (he, vr)
    otro_metodo = "hedonico" if p["metodo"] == "ventas_repetidas" else "ventas_repetidas"
    if principal["indice"] is None:
        raise ErrorFicha(f"{F}: rechazo: {principal['motivo']}")

    def anual(ind: np.ndarray, coste: float = 0.0) -> float:
        return float((ind[-1] / ind[0] * (1 - coste)) ** (1 / (P - 1)) - 1) * PCT

    ind = principal["indice"]
    bruta = anual(ind)
    e = principal["residuos"]
    q25, q75 = (float(x) for x in np.quantile(e, [0.25, 0.75]))
    neta: float | None = None
    if p["comisiones"] is None:
        lim.append("sin comisiones declaradas (supuesto del solicitante, 10–25 %): rentabilidad neta no calculada")
    else:
        neta = anual(ind, p["comisiones"])
    segunda: dict[str, Any] | None = None
    if otra["indice"] is None:
        lim.append(f"segunda vía ({otro_metodo}) no calculada: {otra['motivo']}")
    else:
        segunda = {"metodo": otro_metodo, "rentabilidad_anual_bruta_pct": anual(otra["indice"]),
                   "diferencia_pct": bruta - anual(otra["indice"]),
                   "diferencia_maxima_indice": float(np.max(np.abs(otra["indice"] - ind)))}
    ref: dict[str, Any] = {"tipo": "IPC (rentabilidad real nula) y RI-CM de renta variable global",
                           "rentabilidad_real_anual_pct": None, "exceso_sobre_rv_global_pct": None}
    if v.get("referencia") is None:
        lim.append("sin inflación ni rentabilidad de la renta variable global: referencias ingenuas no comparadas")
    else:
        rf_ = _dict(v["referencia"], f"{F}: «referencia»")
        infl = _rango(rf_.get("inflacion_anual"), f"{F}: referencia.inflacion_anual", -1, abierto_lo=True)
        rv = _rango(rf_.get("rv_global_anual"), f"{F}: referencia.rv_global_anual", -1, abierto_lo=True)
        ref["rentabilidad_real_anual_pct"] = ((1 + bruta / PCT) / (1 + infl) - 1) * PCT
        ref["exceso_sobre_rv_global_pct"] = bruta - rv * PCT
    res = {
        "categoria": categoria, "metodo": p["metodo"], "n_transacciones": len(trans),
        "n_pares": vr["n_pares"], "pares_descartados_mismo_periodo": vr["descartados"],
        "caracteristicas": claves,
        "indice": [{"periodo": primero + i, "indice": float(x)} for i, x in enumerate(ind)],
        "rentabilidad_anual_bruta_pct": bruta, "rentabilidad_anual_neta_pct": neta, "comisiones": p["comisiones"],
        "supuesto_neto": f"una compraventa en los {P - 1} años del índice",
        "volatilidad_pct": float(np.std(ind[1:] / ind[:-1] - 1, ddof=1)) * PCT,
        "dispersion": {"desviacion_residual_pct": math.sqrt(float(e @ e) / principal["gl"]) * PCT,
                       "iqr_residual_pct": (q75 - q25) * PCT},
        "ajuste_sesgo_seleccion": "ninguno (declarado)",
        "segunda_via": segunda,
        "referencia_ingenua": ref,
        "verificacion": {"indice_base": float(ind[0])},                 # índice = 100 en la base
        "advertencias": list(ADVERTENCIAS[F]),
    }
    return res, lim


# ================================================================== registro de fichas
FICHAS: dict[str, dict[str, Any]] = {
    "FIR-CRED-001": {"fn": f_fir_cred, "modulo": "MC-09", "version": "1.1", "cifra": "ESTADISTICA",
                     "ri": "PD histórica por rating", "tol": 1e-6},
    "FX-BEER-001": {"fn": f_fx_beer, "modulo": "MC-03", "version": "1.0", "cifra": "ESTADISTICA",
                    "ri": "PPA (media histórica del tipo real) y RI-PA", "tol": 1e-6},
    "CMD-REAL-001": {"fn": f_cmd_real, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA",
                     "ri": "RI-MH del precio real y RI-PA", "tol": 1e-10},
    "REI-LEV-001": {"fn": f_rei_lev, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA", "ri": "RI-NA",
                    "tol": 1e-10},
    "CHR-ONCHAIN-001": {"fn": f_chr_onchain, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA",
                        "ri": "RI-PA y RI-CM", "tol": 1e-10},
    "CHR-TOKEN-001": {"fn": f_chr_token, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA", "ri": "RI-NA",
                      "tol": 1e-10},
    "PRV-PME-001": {"fn": f_prv_pme, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA",
                    "ri": "índice cotizado (PME = 1)", "tol": 1e-8},
    "PRV-CF-001": {"fn": f_prv_cf, "modulo": "MC-09", "version": "1.0", "cifra": "DETERMINISTA",
                   "ri": "mediana de la cosecha y estrategia", "tol": 1e-8},
    "ALT-HF-001": {"fn": f_alt_hf, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA",
                   "ri": "cartera pasiva de factores (o 60/40)", "tol": 1e-8},
    "ALT-AUC-001": {"fn": f_alt_auc, "modulo": "MC-09", "version": "1.0", "cifra": "ESTADISTICA",
                    "ri": "IPC (rentabilidad real nula) y RI-CM de renta variable global", "tol": 1e-6},
}


# ================================================================== datos sintéticos de los casos de control
# Deterministas y sin azar: cada serie sale de una fórmula. Las comprobaciones recalculan el valor esperado desde estos
# datos por otra vía (fórmula directa, `statistics`, `math.erfc`), nunca desde el resultado.
def _ruido(i: int, k: int) -> float:
    """Pseudo-ruido determinista en (−0,5, 0,5), sin generador de azar."""
    return math.sin(12.9898 * i + 78.233 * k) * 43758.5453 % 1 - 0.5


def _N(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2))


def _tol_caso(F: str) -> float:
    """Tolerancia de las comprobaciones: la de la ficha, y 1e-8 donde la ficha da 1e-6, para que una desviación de una
    millonésima haga fallar el caso (un caso que no puede fallar no cuenta)."""
    return min(FICHAS[F]["tol"], 1e-8)


def _cerca(a: Any, b: float, tol: float) -> bool:
    return a is not None and abs(float(a) - b) <= tol


def _rel(a: Any, b: float, tol: float) -> bool:
    return a is not None and abs(float(a) - b) <= tol * abs(b)


def _dist_a_mano(x: list[float]) -> dict[str, float]:
    q = statistics.quantiles(x, n=4, method="inclusive")               # tipo 7
    return {"mediana": statistics.median(x), "q25": q[0], "q75": q[2], "minimo": min(x), "maximo": max(x)}


def _dist_ok(d: dict[str, Any], x: list[float], tol: float) -> bool:
    return all(_rel(d[k], e, tol) if e != 0 else _cerca(d[k], 0.0, tol) for k, e in _dist_a_mano(x).items())


# ---- FIR-CRED-001
_FC_R, _FC_T, _FC_N = 0.03, 1.0, 12
_FC_ACTIVOS = [(100.0 + 15 * i, 0.12 + 0.02 * i, 45.0 + 9 * i, 0.04 + 0.005 * i) for i in range(_FC_N)]   # V, σ_V, D, μ


def _fc_directo(V: float, sV: float, D: float) -> dict[str, float]:
    """De (V, σ_V) a lo observable (E, σ_E) y a las medidas, con las fórmulas directas de Merton."""
    rz = sV * math.sqrt(_FC_T)
    d1 = (math.log(V / D) + (_FC_R + sV * sV / 2) * _FC_T) / rz
    d2 = d1 - rz
    E = V * _N(d1) - D * math.exp(-_FC_R * _FC_T) * _N(d2)
    rec = V * math.exp(_FC_R * _FC_T) / D * _N(-d1)
    return {"E": E, "sE": _N(d1) * sV * V / E, "dd": d2, "pd": _N(-d2), "dif": -math.log(_N(d2) + rec) / _FC_T,
            "tri": -math.log(1 - _N(-d2)) / _FC_T * (1 - rec / _N(-d2))}


def _datos_fir_cred(sigma_e: float | None = None) -> dict[str, Any]:
    comps = []
    for i, (V, sV, D, mu) in enumerate(_FC_ACTIVOS):
        d = _fc_directo(V, sV, D)
        comps.append({"id": f"C{i:02d}", "capitalizacion": d["E"] if sigma_e is None else 60.0 + i,
                      "volatilidad_acciones": d["sE"] if sigma_e is None else sigma_e,
                      "deuda_corto": 0.4 * D, "deuda_largo": 1.2 * D, "mu_historico": mu})   # 0,4·D + ½·1,2·D = D
    return {"fecha": "2026-06-30", "segmento": {"nombre": "corporativo BBB, industriales", "financiero": False,
                                                "cobertura": 0.8},
            "r": _FC_R, "diferencial_indice_pb": 140.0, "componentes": comps, "pd_historica_rating_pct": 0.25}


def _fc_pesos() -> list[float]:
    total = sum(1.6 * D for _, _, D, _ in _FC_ACTIVOS)
    return [1.6 * D / total for _, _, D, _ in _FC_ACTIVOS]


def _caso_fir_cred_sistema(r: dict[str, Any]) -> bool:
    tol = _tol_caso("FIR-CRED-001")
    m = [_fc_directo(V, sV, D) for V, sV, D, _ in _FC_ACTIVOS]
    w = _fc_pesos()
    dd_real = [(math.log(V / D) + (mu - sV * sV / 2) * _FC_T) / (sV * math.sqrt(_FC_T)) for V, sV, D, mu in _FC_ACTIVOS]
    nr, re_ = r["neutral_al_riesgo"], r["real"]
    return (_dist_ok(nr["dd"], [x["dd"] for x in m], tol) and _dist_ok(nr["pd_pct"], [x["pd"] * PCT for x in m], tol)
            and _rel(nr["dd"]["media_ponderada_deuda"], sum(a * x["dd"] for a, x in zip(w, m, strict=True)), tol)
            and _rel(nr["pd_pct"]["media_ponderada_deuda"], sum(a * x["pd"] for a, x in zip(w, m, strict=True)) * PCT, tol)
            and _rel(nr["proporcion_dd_menor_2_pct"], sum(x["dd"] < 2 for x in m) / _FC_N * PCT, tol)
            and _dist_ok(re_["dd"], dd_real, tol) and _dist_ok(re_["pd_pct"], [_N(-x) * PCT for x in dd_real], tol)
            and _rel(r["diferencial_implicito_pb"], sum(a * x["dif"] for a, x in zip(w, m, strict=True)) * PB, tol)
            and _rel(r["brecha_observado_implicito_pb"],
                     140.0 - sum(a * x["dif"] for a, x in zip(w, m, strict=True)) * PB, tol)
            and r["verificacion"]["error_relativo_sistema_max"] <= FICHAS["FIR-CRED-001"]["tol"])


def _caso_fir_cred_triangulo(r: dict[str, Any]) -> bool:
    tol = _tol_caso("FIR-CRED-001")
    m = [_fc_directo(V, sV, D) for V, sV, D, _ in _FC_ACTIVOS]
    tri = sum(a * x["tri"] for a, x in zip(_fc_pesos(), m, strict=True)) * PB
    dif = sum(a * x["dif"] for a, x in zip(_fc_pesos(), m, strict=True)) * PB
    sv = r["segunda_via_triangulo"]
    return (_rel(sv["diferencial_pb"], tri, tol) and _rel(sv["diferencia_con_implicito_pb"], tri - dif, tol * tri / (tri - dif))
            and 0 < sv["diferencia_con_implicito_pb"] < dif)             # el triángulo aproxima por arriba


def _caso_fir_cred_sin_riesgo(r: dict[str, Any]) -> bool:
    nr = r["neutral_al_riesgo"]
    return (_cerca(nr["pd_pct"]["maximo"], 0.0, _tol_caso("FIR-CRED-001"))
            and _cerca(nr["pd_pct"]["media_ponderada_deuda"], 0.0, _tol_caso("FIR-CRED-001"))
            and _cerca(r["diferencial_implicito_pb"], 0.0, _tol_caso("FIR-CRED-001"))
            and _cerca(nr["proporcion_dd_menor_2_pct"], 0.0, _tol_caso("FIR-CRED-001")) and r["real"] is None)


def _caso_fir_cred_ingenuo(r: dict[str, Any]) -> bool:
    tol = _tol_caso("FIR-CRED-001")
    dd, pd_ = [], []
    for V, sV, D, mu in _FC_ACTIVOS:
        o = _fc_directo(V, sV, D)
        E, sE = o["E"], o["sE"]
        s = E / (E + D) * sE + D / (E + D) * (0.05 + 0.25 * sE)        # Bharath y Shumway (2008)
        dd.append((math.log((E + D) / D) + (mu - s * s / 2) * _FC_T) / (s * math.sqrt(_FC_T)))
        pd_.append(_N(-dd[-1]) * PCT)
    w = _fc_pesos()
    return (_dist_ok(r["real"]["dd"], dd, tol) and _dist_ok(r["real"]["pd_pct"], pd_, tol)
            and _rel(r["real"]["pd_pct"]["media_ponderada_deuda"], sum(a * x for a, x in zip(w, pd_, strict=True)), tol)
            and _rel(r["real"]["proporcion_dd_menor_2_pct"], sum(x < 2 for x in dd) / _FC_N * PCT, tol)
            and _rel(r["referencia_ingenua"]["diferencia_pd_pct"], sum(a * x for a, x in zip(w, pd_, strict=True)) - 0.25, tol))


# ---- FX-BEER-001
_FB_N, _FB_K = 88, 2
_FB_BETA, _FB_C = (0.5, 0.8, 0.3, 1.2), 4.6
_FB_FECHAS = pd.date_range("2003-03-31", periods=_FB_N, freq="QE")


def _fb_fundamentales() -> np.ndarray:
    return np.cumsum(np.array([[0.02 * _ruido(i, k) + 0.001 * (k - 1) for k in range(4)] for i in range(_FB_N)]), axis=0)


def _fb_desvio() -> np.ndarray:
    """Desviación AR(1) determinista, ortogonal en la muestra de estimación al diseño DOLS (constante, niveles y Δx con
    2 adelantos y retardos): así MCO devuelve exactamente los coeficientes con los que se construyó el tipo real."""
    u = np.zeros(_FB_N)
    for i in range(1, _FB_N):
        u[i] = 0.6 * u[i - 1] + 0.05 * _ruido(i, 9)
    X = _fb_fundamentales()
    dX = np.diff(X, axis=0)
    filas = np.arange(_FB_K + 1, _FB_N - _FB_K)
    Z = np.column_stack([np.ones(len(filas)), X[filas]] + [dX[filas - 1 + j] for j in range(-_FB_K, _FB_K + 1)])
    u[filas] = u[filas] - Z @ np.linalg.lstsq(Z, u[filas], rcond=None)[0]
    return u


def _fb_q() -> np.ndarray:
    return _FB_C + _fb_fundamentales() @ np.array(_FB_BETA) + _fb_desvio()


def _datos_fx_beer() -> dict[str, Any]:
    X, q = _fb_fundamentales(), _fb_q()
    nombres = UMBRALES["FX-BEER-001"]["fundamentales"]
    return {"vintage": "2025-02-15",
            "serie": [{"fecha": _iso(f), "reer": math.exp(q[i]), **{nb: float(X[i, j]) for j, nb in enumerate(nombres)}}
                      for i, f in enumerate(_FB_FECHAS)]}


def _fb_z(beta: np.ndarray) -> np.ndarray:
    z = _fb_q() - _fb_fundamentales() @ beta
    return z - z.mean()


def _caso_fx_beer_dols(r: dict[str, Any]) -> bool:
    tol = _tol_caso("FX-BEER-001")
    z = _fb_z(np.array(_FB_BETA))
    nombres = UMBRALES["FX-BEER-001"]["fundamentales"]
    return (all(_rel(r["coeficientes"][nb]["beta"], b, tol) for nb, b in zip(nombres, _FB_BETA, strict=True))
            and _rel(r["desalineamiento_pct"], math.expm1(z[-1]) * PCT, tol)
            and _rel(r["equilibrio"], math.exp(_fb_q()[-1] - z[-1]), tol)
            and _cerca(r["verificacion"]["media_desalineamiento"], 0.0, tol)
            and _cerca(r["verificacion"]["media_residuo_regresion"], 0.0, tol)
            and r["ic_desalineamiento_pct"][0] < r["desalineamiento_pct"] < r["ic_desalineamiento_pct"][1])


def _caso_fx_beer_ppa(r: dict[str, Any]) -> bool:
    tol = _tol_caso("FX-BEER-001")
    reer = [math.exp(x) for x in _fb_q()]
    ppa = (reer[-1] / statistics.geometric_mean(reer) - 1) * PCT
    z = _fb_z(np.array(_FB_BETA))
    return (_rel(r["segunda_via_ppa"]["desalineamiento_pct"], ppa, tol)
            and _rel(r["segunda_via_ppa"]["diferencia_pct"], math.expm1(z[-1]) * PCT - ppa, tol)
            and _rel(r["referencia_ingenua"]["ri_pa_tipo_real"], reer[-1], tol))


def _caso_fx_beer_vida_media(r: dict[str, Any]) -> bool:
    tol = _tol_caso("FX-BEER-001")
    z = _fb_z(np.array(_FB_BETA))
    phi = float(np.polyfit(z[:-1], np.diff(z), 1)[0])                  # Δz_t = a + φ·z_{t−1}
    return (_rel(r["velocidad_correccion_trimestral"], phi, tol)
            and _rel(r["vida_media_anios"], math.log(0.5) / math.log(1 + phi) / TRIMESTRES_ANIO, tol))


def _caso_fx_beer_johansen(r: dict[str, Any]) -> bool:
    tol = _tol_caso("FX-BEER-001")
    joh = fs.johansen(np.column_stack([_fb_q(), _fb_fundamentales()]), _FB_K)   # FX-COINT-001
    beta = -joh["beta"][1:5] / joh["beta"][0]
    z = _fb_z(beta)
    nombres = UMBRALES["FX-BEER-001"]["fundamentales"]
    return (all(_rel(r["coeficientes"][nb]["beta"], float(b), tol) for nb, b in zip(nombres, beta, strict=True))
            and _rel(r["desalineamiento_pct"], math.expm1(z[-1]) * PCT, tol)
            and _cerca(r["verificacion"]["media_desalineamiento"], 0.0, tol)
            and _rel(r["cointegracion"]["estadistico"], joh["traza"][0], tol) and r["ic_desalineamiento_pct"] is None)


# ---- CMD-REAL-001
_CR_N = 31 * MESES_ANIO
_CR_FECHAS = pd.date_range("1994-01-31", periods=_CR_N, freq="ME")
_CR_G = 0.0015                                                          # deriva mensual del logaritmo del precio real
_CR_TRAMOS = [(55.0, 20.0), (30.0, 25.0), (92.0, 6.0), (41.0, 30.0), (70.0, 12.0), (120.0, 7.0)]   # (coste, producción)


def _cr_precio(i: int) -> float:
    return 50.0 * 1.002 ** i * (1 + 0.2 * math.sin(0.37 * i))


def _datos_cmd_real(ipc_constante: bool = False, tendencia_pura: bool = False) -> dict[str, Any]:
    ipc = [100.0 if ipc_constante else 100.0 * 1.0025 ** i for i in range(_CR_N)]
    precio = [40.0 * math.exp(_CR_G * i) * ipc[i] / ipc[-1] if tendencia_pura else _cr_precio(i) for i in range(_CR_N)]
    return {"moneda": "USD", "ipc_moneda": "USD",
            "serie": [{"fecha": _iso(f), "precio": precio[i], "ipc": ipc[i]} for i, f in enumerate(_CR_FECHAS)],
            "curva_costes": {"fecha": "2023-06-30", "fuente": "curva de costes del sector, edición 2023",
                             "tramos": [{"coste": c, "produccion": q} for c, q in _CR_TRAMOS]}}


def _caso_cmd_real_ipc_constante(r: dict[str, Any]) -> bool:
    tol = FICHAS["CMD-REAL-001"]["tol"]
    precios = [_cr_precio(i) for i in range(_CR_N)]
    return (_rel(r["precio_real_actual"], precios[-1], tol) and _rel(r["media_real"], math.fsum(precios) / _CR_N, tol)
            and _rel(r["precio_real_actual"], r["precio_nominal_actual"], tol) and r["verificacion"]["ipc_constante"] is True
            and r["verificacion"]["diferencia_real_nominal_max"] <= tol)


def _caso_cmd_real_metodo(r: dict[str, Any]) -> bool:
    tol = FICHAS["CMD-REAL-001"]["tol"]
    real = [_cr_precio(i) * 1.0025 ** (_CR_N - 1 - i) for i in range(_CR_N)]
    return (_rel(r["precio_real_actual"], _cr_precio(_CR_N - 1), tol) and _rel(r["media_real"], math.fsum(real) / _CR_N, tol)
            and _rel(r["percentil"], sum(x <= real[-1] for x in real) / _CR_N, tol)
            and _rel(r["z"], (real[-1] - statistics.fmean(real)) / statistics.stdev(real), tol)
            and r["verificacion"]["ipc_constante"] is False)


def _caso_cmd_real_tendencia(r: dict[str, Any]) -> bool:
    tol = _tol_caso("CMD-REAL-001")
    return (_rel(r["tendencia_real_pct_anual"], math.expm1(MESES_ANIO * _CR_G) * PCT, tol)
            and r["tendencia_direccion"] == "creciente"
            and _rel(r["precio_real_actual"], 40.0 * math.exp(_CR_G * (_CR_N - 1)), tol))


def _caso_cmd_real_coste(r: dict[str, Any]) -> bool:
    tol = FICHAS["CMD-REAL-001"]["tol"]
    # Por coste: 30 (25), 41 (30), 55 (20), 70 (12), 92 (6), 120 (7); acumulada 25, 55, 75, 87, 93, 100 → el 90 % cae en 92
    meses_desde_curva = _CR_N - 1 - list(_CR_FECHAS).index(pd.Timestamp("2023-06-30"))
    coste_real = 92.0 * 1.0025 ** meses_desde_curva
    cm = r["coste_marginal"]
    return (_rel(cm["coste_nominal"], 92.0, tol) and _rel(cm["coste_real"], coste_real, tol)
            and _rel(r["precio_sobre_coste"], _cr_precio(_CR_N - 1) / coste_real, tol))


# ---- REI-LEV-001
def _datos_rei_lev() -> dict[str, Any]:
    return {"fecha": "2026-06-30", "moneda": "EUR", "coste_refinanciacion": {"swap": 0.027, "margen": 0.018},
            "componentes": [
                {"id": "S1", "gav": 1000.0, "deuda": 420.0, "caja": 20.0, "ebitda": 48.0, "gastos_financieros": 12.0,
                 "ffo": 30.0, "covenants": {"ltv_max": 0.6, "icr_min": 2.0},
                 "vencimientos": [{"fecha": "2027-03-31", "importe": 120.0, "coste": 0.015},
                                  {"fecha": "2028-06-30", "importe": 100.0, "coste": 0.02},
                                  {"fecha": "2031-12-31", "importe": 200.0, "coste": 0.035}]},
                {"id": "S2", "gav": 600.0, "deuda": 330.0, "caja": 30.0, "ebitda": 27.0, "gastos_financieros": 10.0,
                 "ffo": 14.0, "covenants": {"ltv_max": 0.55, "icr_min": 2.5},
                 "vencimientos": [{"fecha": "2026-12-31", "importe": 90.0, "coste": 0.03},
                                  {"fecha": "2028-07-01", "importe": 240.0, "coste": 0.025}]},
                {"id": "S3", "gav": 400.0, "deuda": 100.0, "caja": 10.0, "ebitda": 20.0, "gastos_financieros": 4.0,
                 "ffo": 12.0,
                 "vencimientos": [{"fecha": "2030-01-31", "importe": 100.0, "coste": 0.04}]}]}


def _caso_rei_lev_vencimientos(r: dict[str, Any]) -> bool:
    tol = FICHAS["REI-LEV-001"]["tol"]
    # Hasta el 2028-06-30 (24 meses): S1 120 + 100; S2 90 (el del 2028-07-01 queda fuera); S3 nada
    return (r["verificacion"]["error_relativo_vencimientos_max"] <= tol
            and _rel(r["vencimientos_24m_pct"], (120.0 + 100.0 + 90.0) / (420.0 + 330.0 + 100.0) * PCT, tol)
            and _dist_ok(r["dispersion"]["vencimientos_24m_pct"], [220.0 / 420.0 * PCT, 90.0 / 330.0 * PCT, 0.0], tol))


def _caso_rei_lev_ratios(r: dict[str, Any]) -> bool:
    tol = FICHAS["REI-LEV-001"]["tol"]
    neta, gav, ebitda, gf = 400.0 + 300.0 + 90.0, 2000.0, 95.0, 26.0
    return (_rel(r["ltv_pct"], neta / gav * PCT, tol) and _rel(r["icr_veces"], ebitda / gf, tol)
            and _rel(r["deuda_neta_sobre_ebitda_veces"], neta / ebitda, tol)
            and _rel(r["ltv_estresado_pct"]["-0.1"], neta / (gav * 0.9) * PCT, tol)
            and _rel(r["ltv_estresado_pct"]["-0.2"], neta / (gav * 0.8) * PCT, tol)
            and _dist_ok(r["dispersion"]["ltv_pct"], [40.0, 50.0, 22.5], tol)
            and _dist_ok(r["dispersion"]["icr_veces"], [4.0, 2.7, 5.0], tol))


def _caso_rei_lev_refinanciacion(r: dict[str, Any]) -> bool:
    tol = FICHAS["REI-LEV-001"]["tol"]
    extra = 120.0 * (0.045 - 0.015) + 100.0 * (0.045 - 0.02) + 90.0 * (0.045 - 0.03)   # coste nuevo = 2,7 % + 1,8 %
    c = r["covenants"]
    return (_rel(r["impacto_ffo_pct"], -extra / 56.0 * PCT, tol) and _rel(r["coste_refinanciacion"]["coste"], 0.045, tol)
            and c["n_componentes"] == 2 and _dist_ok(c["holgura_ltv_pp"], [20.0, 5.0], tol)
            and _dist_ok(c["holgura_icr_veces"], [2.0, 0.2], tol)
            and _dist_ok(c["caida_valor_que_agota_ltv_pct"], [(0.4 / 0.6 - 1) * PCT, (0.5 / 0.55 - 1) * PCT], tol)
            and _cerca(c["en_incumplimiento_pct"], 0.0, tol)
            # con −10 %: S1 0,444 ≤ 0,6; S2 0,556 > 0,55. Con −20 %: S2 0,625 > 0,55
            and _rel(c["en_incumplimiento_ltv_estresado_pct"]["-0.1"], 50.0, tol)
            and _rel(c["en_incumplimiento_ltv_estresado_pct"]["-0.2"], 50.0, tol))


# ---- CHR-ONCHAIN-001
_CO_N = 800
_CO_FECHAS = pd.date_range("2023-01-01", periods=_CO_N, freq="D")


def _co_series(coste_medio: bool) -> tuple[list[float], list[float], list[float]]:
    cm = [1e9 * (1 + 0.3 * math.sin(0.01 * i) + 0.001 * i) for i in range(_CO_N)]
    cr = [0.8e9 * (1 + 0.0008 * i) for i in range(_CO_N)]
    vol = [5e7 * (1 + 0.5 * math.sin(0.05 * i) ** 2) for i in range(_CO_N)]
    if coste_medio:
        cr[-1] = cm[-1]                                                 # precio = coste medio de los tenedores
    return cm, cr, vol


def _datos_chr_onchain(coste_medio: bool = False) -> dict[str, Any]:
    cm, cr, vol = _co_series(coste_medio)
    return {"fuente": {"nombre": "proveedor en cadena A", "metodologia": "UTXO: precio del último movimiento",
                       "filtros": "sin movimientos internos de plataformas"},
            "serie": [{"fecha": _iso(f), "capitalizacion": cm[i], "capitalizacion_realizada": cr[i],
                       "volumen_ajustado": vol[i]} for i, f in enumerate(_CO_FECHAS)]}


def _caso_chr_onchain_coste_medio(r: dict[str, Any]) -> bool:
    tol = FICHAS["CHR-ONCHAIN-001"]["tol"]
    return (_rel(r["mvrv"], 1.0, tol) and _cerca(r["mvrv_z"], 0.0, tol)
            and _rel(r["verificacion"]["capitalizacion_sobre_realizada"], 1.0, tol))


def _co_a_mano(w: int) -> dict[str, float]:
    cm, cr, vol = _co_series(False)
    sd = statistics.stdev(cm)
    mvrv = [a / b for a, b in zip(cm, cr, strict=True)]
    z = [(a - b) / sd for a, b in zip(cm, cr, strict=True)]
    nvt = [a / b for a, b in zip(cm, vol, strict=True)]
    senal = [cm[i] / (math.fsum(vol[i - w + 1: i + 1]) / w) for i in range(w - 1, _CO_N)]
    return {"mvrv": mvrv[-1], "mvrv_z": z[-1], "nvt": nvt[-1], "senal_nvt": senal[-1],
            "p_mvrv": sum(x <= mvrv[-1] for x in mvrv) / _CO_N, "p_mvrv_z": sum(x <= z[-1] for x in z) / _CO_N,
            "p_nvt": sum(x <= nvt[-1] for x in nvt) / _CO_N, "p_senal_nvt": sum(x <= senal[-1] for x in senal) / len(senal)}


def _caso_chr_onchain_metodo(r: dict[str, Any], w: int = 90) -> bool:
    tol = FICHAS["CHR-ONCHAIN-001"]["tol"]
    e = _co_a_mano(w)
    return (all(_rel(r[k], e[k], tol) for k in ("mvrv", "mvrv_z", "nvt", "senal_nvt"))
            and all(_rel(r["percentiles"][k], e[f"p_{k}"], tol) for k in ("mvrv", "mvrv_z", "nvt", "senal_nvt"))
            and r["media_nvt_dias"] == w)


# ---- CHR-TOKEN-001
def _datos_chr_token(sin_dilucion: bool = False) -> dict[str, Any]:
    if sin_dilucion:
        tokens = [{"id": t, "precio": pr, "oferta_circulante": q, "oferta_total": q, "oferta_maxima": q, "emision_anual": 0.0,
                   "quema_anual": 0.0, "calendario": {"fuente": "documentación del protocolo", "desbloqueos": []}}
                  for t, pr, q in (("TKA", 2.0, 1.0e9), ("TKB", 0.5, 4.0e8))]
    else:
        tokens = [
            {"id": "TKA", "precio": 2.0, "oferta_circulante": 6.0e8, "oferta_total": 9.0e8, "oferta_maxima": 1.0e9,
             "emision_anual": 4.5e7, "quema_anual": 1.5e7, "staking_nominal": 0.08, "concentracion_10_mayores": 0.35,
             "calendario": {"fuente": "documentación del protocolo", "desbloqueos": [
                 {"fecha": "2026-06-30", "cantidad": 5.0e7},                                   # no posterior: no cuenta
                 {"fecha": "2026-07-20", "cantidad": 3.0e7}, {"fecha": "2026-09-15", "cantidad": 6.0e7},
                 {"fecha": "2027-01-01", "cantidad": 9.0e7}]}},
            {"id": "TKB", "precio": 0.5, "oferta_circulante": 4.0e8, "oferta_total": 5.0e8, "oferta_maxima": None,
             "emision_anual": 2.0e7, "quema_anual": 2.4e7,
             "calendario": {"fuente": "panel de desbloqueos B", "desbloqueos": [{"fecha": "2026-07-30", "cantidad": 2.0e7}]}}]
    return {"fecha": "2026-06-30", "fuente": "agregador de datos de tokens, 2026-06-30", "ambito": "sector de capa 2",
            "tokens": tokens}


def _caso_chr_token_sin_dilucion(r: dict[str, Any]) -> bool:
    tol = FICHAS["CHR-TOKEN-001"]["tol"]
    return (_rel(r["fdv_sobre_capitalizacion_veces"], 1.0, tol) and _cerca(r["inflacion_neta_pct_anual"], 0.0, tol)
            and all(_cerca(x, 0.0, tol) for x in r["desbloqueos_pct"].values())
            and r["verificacion"]["circulante_le_total_le_maxima"] is True
            and _cerca(r["verificacion"]["holgura_desbloqueos_min"], 0.0, tol))


def _caso_chr_token_metodo(r: dict[str, Any]) -> bool:
    tol = FICHAS["CHR-TOKEN-001"]["tol"]
    cm_a, cm_b = 2.0 * 6.0e8, 0.5 * 4.0e8
    cm = cm_a + cm_b
    return (_rel(r["fdv_sobre_capitalizacion_veces"], (2.0 * 1.0e9 + 0.5 * 5.0e8) / cm, tol)   # TKB sin tope: oferta total
            and _rel(r["inflacion_neta_pct_anual"], (2.0 * 3.0e7 + 0.5 * -4.0e6) / cm * PCT, tol)
            and _rel(r["desbloqueos_pct"]["30"], (2.0 * 3.0e7 + 0.5 * 2.0e7) / cm * PCT, tol)
            and _rel(r["desbloqueos_pct"]["90"], (2.0 * 9.0e7 + 0.5 * 2.0e7) / cm * PCT, tol)
            and _rel(r["capitalizacion_circulante"], cm, tol)
            and _dist_ok(r["dispersion"]["fdv_sobre_capitalizacion_veces"], [1.0e9 / 6.0e8, 5.0e8 / 4.0e8], tol)
            and _dist_ok(r["dispersion"]["inflacion_neta_pct_anual"], [3.0e7 / 6.0e8 * PCT, -4.0e6 / 4.0e8 * PCT], tol)
            # holgura: TKA (9e8 − 6e8 − 1,8e8)/9e8 = 0,133; TKB (5e8 − 4e8 − 2e7)/5e8 = 0,16
            and _rel(r["verificacion"]["holgura_desbloqueos_min"], (9.0e8 - 6.0e8 - 1.8e8) / 9.0e8, tol))


def _caso_chr_token_staking(r: dict[str, Any]) -> bool:
    tol = FICHAS["CHR-TOKEN-001"]["tol"]
    cm_a, cm_b = 2.0 * 6.0e8, 0.5 * 4.0e8
    return (_rel(r["rendimiento_real_staking_pct"], (0.08 - 3.0e7 / 6.0e8) * PCT, tol)       # nominal − inflación neta
            and _rel(r["concentracion_10_mayores_pct"], 35.0, tol)
            and _rel(r["cobertura_staking_pct"], cm_a / (cm_a + cm_b) * PCT, tol)
            and _rel(r["cobertura_concentracion_pct"], cm_a / (cm_a + cm_b) * PCT, tol))


# ---- PRV-PME-001 y PRV-CF-001
_PV_FECHAS = ["2019-03-31", "2020-03-31", "2021-06-30", "2022-09-30", "2023-12-31", "2025-06-30"]
_PV_INDICE = [100.0, 92.0, 131.0, 118.0, 150.0, 181.0]
_PV_APORT = [40.0, 35.0, 15.0, 0.0, 0.0, 0.0]
_PV_DISTR = [0.0, 0.0, 10.0, 30.0, 45.0, 20.0]
_PV_NAV = 38.0


def _datos_prv_pme(replica: bool = False) -> dict[str, Any]:
    distr, nav = list(_PV_DISTR), _PV_NAV
    if replica:   # cada aportación compra participaciones del índice y cada distribución vende una parte
        part = 0.0
        for i, (c, ind) in enumerate(zip(_PV_APORT, _PV_INDICE, strict=True)):
            part += c / ind
            vendidas = part * (0.0, 0.0, 0.1, 0.3, 0.5, 0.4)[i]
            distr[i] = vendidas * ind
            part -= vendidas
        nav = part * _PV_INDICE[-1]
    return {"moneda": "USD",
            "flujos": [{"fecha": f, "aportacion": c, "distribucion": d} for f, c, d in zip(_PV_FECHAS, _PV_APORT, distr, strict=True)],
            "nav_final": {"fecha": _PV_FECHAS[-1], "valor": nav},
            "indice": {"nombre": "índice de pequeña capitalización, rentabilidad total", "moneda": "USD",
                       "rentabilidad_total": True, "riesgo_comparable": "pequeña capitalización, comparable a buyout",
                       "niveles": [{"fecha": f, "nivel": x} for f, x in zip(_PV_FECHAS, _PV_INDICE, strict=True)]}}


def _pv_t() -> list[float]:
    d0 = pd.Timestamp(_PV_FECHAS[0])
    return [(pd.Timestamp(f) - d0).days / DIAS_ANIO for f in _PV_FECHAS]


def _pv_van(flujos: list[float], tir_pct: Any) -> float:
    """Valor actual neto de los flujos a la TIR entregada, relativo al total aportado: debe ser nulo."""
    if tir_pct is None:
        return math.inf
    return sum(f / (1 + tir_pct / PCT) ** t for f, t in zip(flujos, _pv_t(), strict=True)) / sum(_PV_APORT)


def _caso_prv_pme_replica(r: dict[str, Any]) -> bool:
    tol = FICHAS["PRV-PME-001"]["tol"]
    return (_rel(r["ks_pme_veces"], 1.0, tol) and _cerca(r["alfa_directo_pct_anual"], 0.0, tol)
            and _cerca(r["referencia_ingenua"]["exceso_ks_pme"], 0.0, tol) and _rel(r["pme_plus"]["lambda"], 1.0, tol)
            and _cerca(r["pme_plus"]["diferencial_tir_pct"], 0.0, tol))


def _caso_prv_pme_metodo(r: dict[str, Any]) -> bool:
    tol = FICHAS["PRV-PME-001"]["tol"]
    fac = [_PV_INDICE[-1] / x for x in _PV_INDICE]
    vf_c = sum(c * f for c, f in zip(_PV_APORT, fac, strict=True))
    vf_d = sum(d * f for d, f in zip(_PV_DISTR, fac, strict=True))
    neto = [d - c for c, d in zip(_PV_APORT, _PV_DISTR, strict=True)]
    neto[-1] += _PV_NAV
    cap = [(d - c) * f for c, d, f in zip(_PV_APORT, _PV_DISTR, fac, strict=True)]
    cap[-1] += _PV_NAV
    alfa = r["alfa_directo_pct_anual"]
    return (_rel(r["ks_pme_veces"], (vf_d + _PV_NAV) / vf_c, tol)
            and _rel(r["tvpi_veces"], (sum(_PV_DISTR) + _PV_NAV) / sum(_PV_APORT), tol)
            and _rel(r["dpi_veces"], sum(_PV_DISTR) / sum(_PV_APORT), tol)
            and abs(_pv_van(neto, r["tir_pct"])) <= tol
            and alfa is not None and abs(_pv_van(cap, math.expm1(alfa / PCT) * PCT)) <= tol)


def _caso_prv_pme_plus(r: dict[str, Any]) -> bool:
    tol = FICHAS["PRV-PME-001"]["tol"]
    fac = [_PV_INDICE[-1] / x for x in _PV_INDICE]
    lam = (sum(c * f for c, f in zip(_PV_APORT, fac, strict=True)) - _PV_NAV) / sum(d * f for d, f in zip(_PV_DISTR, fac, strict=True))
    fl = [lam * d - c for c, d in zip(_PV_APORT, _PV_DISTR, strict=True)]
    fl[-1] += _PV_NAV
    pp = r["pme_plus"]
    return (_rel(pp["lambda"], lam, tol) and abs(_pv_van(fl, pp["tir_indice_pct"])) <= tol
            and _rel(pp["diferencial_tir_pct"], r["tir_pct"] - pp["tir_indice_pct"], tol))


def _datos_prv_cf(simple: bool = False) -> dict[str, Any]:
    if simple:   # 100 aportados y 121 de NAV a los 730 días: TIR = 10 % exacto
        return {"compromiso": 100.0, "flujos": [{"fecha": "2023-01-01", "aportacion": 100.0, "distribucion": 0.0}],
                "navs": [{"fecha": "2024-12-31", "valor": 121.0}]}
    return {"compromiso": 100.0, "vida_anios": 10,
            "flujos": [{"fecha": f, "aportacion": c, "distribucion": d} for f, c, d in zip(_PV_FECHAS, _PV_APORT, _PV_DISTR, strict=True)],
            "navs": [{"fecha": "2023-12-31", "valor": 55.0}, {"fecha": _PV_FECHAS[-1], "valor": _PV_NAV}],
            "referencia_cosecha": {"tvpi_mediana": 1.45, "tir_mediana": 0.11}}


def _caso_prv_cf_multiplos(r: dict[str, Any]) -> bool:
    tol = FICHAS["PRV-CF-001"]["tol"]
    ap, di = sum(_PV_APORT), sum(_PV_DISTR)
    neto = [d - c for c, d in zip(_PV_APORT, _PV_DISTR, strict=True)]
    acum = [sum(neto[: i + 1]) for i in range(len(neto))]
    neto[-1] += _PV_NAV
    return (_rel(r["tvpi_veces"], (di + _PV_NAV) / ap, tol) and _rel(r["dpi_veces"], di / ap, tol)
            and _rel(r["rvpi_veces"], _PV_NAV / ap, tol)
            and _rel(r["tvpi_veces"], r["dpi_veces"] + r["rvpi_veces"], tol)                  # «Verificación»
            and _cerca(r["verificacion"]["tvpi_menos_dpi_menos_rvpi"], 0.0, tol)
            and abs(_pv_van(neto, r["tir_pct"])) <= tol
            and all(_rel(s["flujo_neto_acumulado"], a, tol) for s, a in zip(r["curva_j"]["serie"], acum, strict=True))
            and _rel(r["curva_j"]["minimo_sobre_compromiso"], min(acum) / 100.0, tol)
            and r["curva_j"]["fecha_minimo"] == _PV_FECHAS[acum.index(min(acum))]
            and _rel(r["referencia_ingenua"]["diferencia_tvpi"], (di + _PV_NAV) / ap - 1.45, tol))


def _caso_prv_cf_tir(r: dict[str, Any]) -> bool:
    tol = FICHAS["PRV-CF-001"]["tol"]
    return (_rel(r["tir_pct"], 10.0, tol) and _rel(r["tvpi_veces"], 1.21, tol) and _cerca(r["dpi_veces"], 0.0, tol)
            and r["proyeccion"] is None)


def _caso_prv_cf_proyeccion(r: dict[str, Any]) -> bool:
    tol = FICHAS["PRV-CF-001"]["tol"]
    # Edad 6 (2019-03-31 a 2025-06-30), vida 10, compromiso 100, aportado 90, NAV 38, crecimiento 8 %, bow 2,5; tasas de
    # aportación 25 %, 33 % y 50 % (la última se mantiene). Años 7 a 10, a mano:
    c7 = 0.5 * 10.0
    d7 = 0.7 ** 2.5 * 38.0 * 1.08
    n7 = 38.0 * 1.08 + c7 - d7
    c8 = 0.5 * (10.0 - c7)
    d8 = 0.8 ** 2.5 * n7 * 1.08
    n8 = n7 * 1.08 + c8 - d8
    c9 = 0.5 * (10.0 - c7 - c8)
    d9 = 0.9 ** 2.5 * n8 * 1.08
    n9 = n8 * 1.08 + c9 - d9
    c10 = 0.5 * (10.0 - c7 - c8 - c9)
    d10 = n9 * 1.08                                                     # (10/10)^bow = 1: se distribuye todo
    esperado = [(7, c7, d7, n7), (8, c8, d8, n8), (9, c9, d9, n9), (10, c10, d10, c10)]
    pr = r["proyeccion"]
    ap = 90.0 + c7 + c8 + c9 + c10
    return (pr is not None and pr["edad_anios"] == 6 and len(pr["serie"]) == 4
            and all(s["anio_vida"] == t and _rel(s["aportacion"], c, tol) and _rel(s["distribucion"], d, tol)
                    and _rel(s["nav"], n_, tol) for s, (t, c, d, n_) in zip(pr["serie"], esperado, strict=True))
            and _rel(pr["tvpi_final_veces"], (105.0 + d7 + d8 + d9 + d10 + c10) / ap, tol)
            and _rel(pr["aportado_final_sobre_compromiso"], ap / 100.0, tol))


# ---- ALT-HF-001
_HF_N = 48
_HF_FECHAS = pd.date_range("2021-01-31", periods=_HF_N, freq="ME")
_HF_FF = ("MKT", "SMB", "HML", "RMW", "CMA", "UMD")                     # FF5+UMD de ACC-FACT-001
_HF_ALFA, _HF_PHI = 0.35, 0.5


def _hf_betas(nombres: tuple[str, ...]) -> list[float]:
    return [0.45 - 0.11 * j + 0.02 * j * j for j in range(len(nombres))]


def _hf_factores(nombres: tuple[str, ...]) -> np.ndarray:
    return np.array([[4.0 * _ruido(i, j + 20) + 0.2 for j in range(len(nombres))] for i in range(_HF_N)])


def _hf_rf() -> np.ndarray:
    return np.array([0.25 + 0.05 * math.sin(0.3 * i) for i in range(_HF_N)])


def _hf_exceso(nombres: tuple[str, ...]) -> np.ndarray:
    """α + β'F + e, con e ortogonal a la constante y a los factores: MCO devuelve exactamente α y β."""
    Fm = _hf_factores(nombres)
    X = np.column_stack([np.ones(_HF_N), Fm])
    e = np.array([1.5 * _ruido(i, 40) for i in range(_HF_N)])
    e = e - X @ np.linalg.lstsq(X, e, rcond=None)[0]
    return _HF_ALFA + Fm @ np.array(_hf_betas(nombres)) + e


def _hf_observada(nombres: tuple[str, ...], suavizada: bool) -> np.ndarray:
    """Rentabilidad de la estrategia; `suavizada`, con el filtro de Geltner r*_t = (1 − φ)·r_t + φ·r*_{t−1}, φ = 0,5."""
    r = _hf_exceso(nombres) + _hf_rf()
    if suavizada:
        for i in range(1, _HF_N):
            r[i] = (1 - _HF_PHI) * r[i] + _HF_PHI * r[i - 1]
    return r


def _datos_alt_hf(nombres: tuple[str, ...], suavizada: bool = False) -> dict[str, Any]:
    Fm, r = _hf_factores(nombres), _hf_observada(nombres, suavizada)
    return {"serie": [{"fecha": _iso(f), "r": float(r[i]), "rf": float(_hf_rf()[i]),
                       **{nb: float(Fm[i, j]) for j, nb in enumerate(nombres)}} for i, f in enumerate(_HF_FECHAS)]}


def _caso_alt_hf_acc_fact(r: dict[str, Any]) -> bool:
    """«Verificación»: coherencia con ACC-FACT-001, que se ejecuta aquí con los mismos datos."""
    tol = FICHAS["ALT-HF-001"]["tol"]
    Fm = _hf_factores(_HF_FF)
    ref, _ = fv.FICHAS["ACC-FACT-001"]["fn"](
        {"valores": {"region": "global", "fechas": [_iso(f) for f in _HF_FECHAS],
                     "rendimientos": [float(x) for x in _hf_exceso(_HF_FF) + _hf_rf()], "rf": [float(x) for x in _hf_rf()],
                     "factores": {nb: [float(x) for x in Fm[:, j]] for j, nb in enumerate(_HF_FF)}},
         "series": {}, "series_rol": {}, "fecha_corte": None}, {"modelo": "FF5+UMD"})
    return (_rel(r["alfa_anual_pct"], ref["alfa_anual_pct"], tol) and _rel(r["t_alfa"], ref["t_alfa"], tol)
            and _rel(r["r2"], ref["r2"], tol)
            and all(_rel(r["betas"][nb]["beta"], ref["betas"][nb]["beta"], tol)
                    and _rel(r["betas"][nb]["t"], ref["betas"][nb]["t"], tol) for nb in _HF_FF))


def _caso_alt_hf_exacto(r: dict[str, Any]) -> bool:
    tol = FICHAS["ALT-HF-001"]["tol"]
    nombres = UMBRALES["ALT-HF-001"]["factores_fung_hsieh"]
    betas = _hf_betas(nombres)
    medias = _hf_factores(nombres).mean(axis=0)
    pasiva = sum(b * float(m) for b, m in zip(betas, medias, strict=True))
    d = r["descomposicion_media_pct"]
    return (_rel(r["alfa_periodo_pct"], _HF_ALFA, tol)
            and _rel(r["alfa_anual_pct"], ((1 + _HF_ALFA / PCT) ** MESES_ANIO - 1) * PCT, tol)
            and all(_rel(r["betas"][nb]["beta"], b, tol) for nb, b in zip(nombres, betas, strict=True))
            and _rel(d["por_factores"], pasiva, tol) and _rel(d["total"], _HF_ALFA + pasiva, tol)
            and _rel(d["total"], d["alfa"] + d["por_factores"], tol)
            and r["verificacion"]["error_identidad_media"] <= tol and r["desuavizado"]["phi"] is None)


def _caso_alt_hf_desuavizado(r: dict[str, Any]) -> bool:
    tol = FICHAS["ALT-HF-001"]["tol"]
    nombres = UMBRALES["ALT-HF-001"]["factores_fung_hsieh"]
    obs = _hf_observada(nombres, suavizada=True)
    phi = float(np.polyfit(obs[:-1], obs[1:], 1)[0])                    # AR(1) con constante
    y = (obs[1:] - phi * obs[:-1]) / (1 - phi) - _hf_rf()[1:]
    X = np.column_stack([np.ones(_HF_N - 1), _hf_factores(nombres)[1:]])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return (phi > 0 and _rel(r["desuavizado"]["phi"], phi, tol) and _rel(r["alfa_periodo_pct"], float(b[0]), tol)
            and all(_rel(r["betas"][nb]["beta"], float(b[j + 1]), tol) for j, nb in enumerate(nombres))
            and r["n"] == _HF_N - 1)


# ---- ALT-AUC-001
_AU_P, _AU_PIEZAS, _AU_ANIO0 = 10, 300, 2010


def _au_indice(k: int) -> float:
    return BASE_INDICE * math.exp(0.05 * k + 0.03 * math.sin(1.3 * k))


def _au_transacciones(ruido: float = 0.0) -> list[dict[str, Any]]:
    """Dos ventas por pieza en años distintos; precio = calidad (log-lineal en dos características) × índice del año."""
    out = []
    for i in range(_AU_PIEZAS):
        x1, x2 = (i % 7) / 7, (i % 11) / 11
        a = i % _AU_P
        b = (a + 1 + (i // _AU_P) % (_AU_P - 1)) % _AU_P
        for j, k in enumerate(sorted((a, b))):
            precio = math.exp(5.0 + 0.8 * x1 - 0.4 * x2 + ruido * _ruido(i, 60 + j)) * _au_indice(k) / BASE_INDICE
            out.append({"id_pieza": f"P{i:03d}", "fecha": f"{_AU_ANIO0 + k}-{1 + (i + 5 * j) % 12:02d}-15", "precio": precio,
                        "caracteristicas": {"tamano": x1, "antiguedad": x2}})
    return out


def _datos_alt_auc(ruido: float = 0.0) -> dict[str, Any]:
    return {"categoria": "relojes de pulsera de subasta", "transacciones": _au_transacciones(ruido),
            "referencia": {"inflacion_anual": 0.02, "rv_global_anual": 0.07}}


def _caso_alt_auc_base(r: dict[str, Any]) -> bool:
    tol = _tol_caso("ALT-AUC-001")
    bruta = ((_au_indice(_AU_P - 1) / BASE_INDICE) ** (1 / (_AU_P - 1)) - 1) * PCT
    return (_rel(r["indice"][0]["indice"], BASE_INDICE, tol) and _rel(r["verificacion"]["indice_base"], BASE_INDICE, tol)
            and all(x["periodo"] == _AU_ANIO0 + k and _rel(x["indice"], _au_indice(k), tol) for k, x in enumerate(r["indice"]))
            and _rel(r["rentabilidad_anual_bruta_pct"], bruta, tol) and r["n_pares"] == _AU_PIEZAS
            and _rel(r["referencia_ingenua"]["rentabilidad_real_anual_pct"], ((1 + bruta / PCT) / 1.02 - 1) * PCT, tol)
            and _rel(r["referencia_ingenua"]["exceso_sobre_rv_global_pct"], bruta - 7.0, tol))


def _caso_alt_auc_segunda_via(r: dict[str, Any]) -> bool:
    tol = _tol_caso("ALT-AUC-001")
    sv = r["segunda_via"]
    return (sv is not None and sv["metodo"] == "ventas_repetidas" and r["metodo"] == "hedonico"
            and all(_rel(x["indice"], _au_indice(k), tol) for k, x in enumerate(r["indice"]))
            and _cerca(sv["diferencia_pct"], 0.0, tol) and _cerca(sv["diferencia_maxima_indice"], 0.0, tol * BASE_INDICE))


def _caso_alt_auc_metodo(r: dict[str, Any]) -> bool:
    """Bailey-Muth-Nourse a mano con precios con ruido; neta de comisiones del 15 %; volatilidad y dispersión."""
    tol = _tol_caso("ALT-AUC-001")
    tr = _au_transacciones(ruido=0.2)
    M, y = np.zeros((_AU_PIEZAS, _AU_P - 1)), np.zeros(_AU_PIEZAS)
    for i in range(_AU_PIEZAS):
        compra, venta = tr[2 * i], tr[2 * i + 1]
        kc, kv = int(compra["fecha"][:4]) - _AU_ANIO0, int(venta["fecha"][:4]) - _AU_ANIO0
        if kv > 0:
            M[i, kv - 1] = 1.0
        if kc > 0:
            M[i, kc - 1] = -1.0
        y[i] = math.log(venta["precio"] / compra["precio"])
    beta = np.linalg.solve(M.T @ M, M.T @ y)                            # ecuaciones normales
    ind = [BASE_INDICE] + [BASE_INDICE * math.exp(b) for b in beta]
    e = y - M @ beta
    total = ind[-1] / ind[0]
    var = [ind[k + 1] / ind[k] - 1 for k in range(_AU_P - 1)]
    return (all(_rel(x["indice"], v_, tol) for x, v_ in zip(r["indice"], ind, strict=True))
            and _rel(r["rentabilidad_anual_bruta_pct"], (total ** (1 / (_AU_P - 1)) - 1) * PCT, tol)
            and _rel(r["rentabilidad_anual_neta_pct"], ((total * 0.85) ** (1 / (_AU_P - 1)) - 1) * PCT, tol)
            and _rel(r["volatilidad_pct"], statistics.stdev(var) * PCT, tol)
            and _rel(r["dispersion"]["desviacion_residual_pct"],
                     math.sqrt(float(e @ e) / (_AU_PIEZAS - (_AU_P - 1))) * PCT, tol))


# Cada caso: una frase comprobable de la «Verificación» de la ficha (o una identidad del «Método»), con datos que no
# anulan sus términos; cada comprobación recalcula el valor esperado desde los datos sintéticos, no desde el resultado.
CASOS_CONTROL: dict[str, list[dict[str, Any]]] = {
    "FIR-CRED-001": [
        {"nombre": "σ_V → 0 con V > D ⇒ PD → 0 (y diferencial implícito nulo)",
         "datos": [{"valores": _datos_fir_cred(sigma_e=1e-3)}], "parametros": {"mu": "r"},
         "comprobar": _caso_fir_cred_sin_riesgo},
        {"nombre": "sistema de Merton: recupera (V, σ_V) de cada componente; DD, PD, agregación y diferencial implícito",
         "datos": [{"valores": _datos_fir_cred()}], "parametros": {}, "comprobar": _caso_fir_cred_sistema},
        {"nombre": "segunda vía: triángulo de crédito con la PD (aproxima por arriba el diferencial implícito)",
         "datos": [{"valores": _datos_fir_cred()}], "parametros": {}, "comprobar": _caso_fir_cred_triangulo},
        {"nombre": "alternativa ingenua de Bharath-Shumway a mano, con la PD histórica por rating de referencia",
         "datos": [{"valores": _datos_fir_cred()}], "parametros": {"metodo": "ingenuo"}, "comprobar": _caso_fir_cred_ingenuo},
    ],
    "FX-BEER-001": [
        {"nombre": "residuo de media nula; DOLS recupera los coeficientes con los que se construyó el tipo real",
         "datos": [{"valores": _datos_fx_beer()}], "parametros": {}, "comprobar": _caso_fx_beer_dols},
        {"nombre": "segunda vía FX-PPA-001: desalineamiento frente a la media histórica del tipo real",
         "datos": [{"valores": _datos_fx_beer()}], "parametros": {}, "comprobar": _caso_fx_beer_ppa},
        {"nombre": "velocidad de corrección y vida media del desalineamiento (AR(1)) a mano",
         "datos": [{"valores": _datos_fx_beer()}], "parametros": {}, "comprobar": _caso_fx_beer_vida_media},
        {"nombre": "Johansen: vector normalizado sobre el tipo real y traza de FX-COINT-001; residuo de media nula",
         "datos": [{"valores": _datos_fx_beer()}], "parametros": {"metodo": "Johansen"}, "comprobar": _caso_fx_beer_johansen},
    ],
    "CMD-REAL-001": [
        {"nombre": "IPC constante ⇒ real = nominal",
         "datos": [{"valores": _datos_cmd_real(ipc_constante=True)}], "parametros": {}, "comprobar": _caso_cmd_real_ipc_constante},
        {"nombre": "método a mano: precio real en moneda constante del último mes, media (RI-MH), percentil y z",
         "datos": [{"valores": _datos_cmd_real()}], "parametros": {}, "comprobar": _caso_cmd_real_metodo},
        {"nombre": "tendencia real (FX-TREND-001): un precio real log-lineal da su pendiente exacta",
         "datos": [{"valores": _datos_cmd_real(tendencia_pura=True)}], "parametros": {}, "comprobar": _caso_cmd_real_tendencia},
        {"nombre": "razón precio/coste en el percentil 90 de la curva de costes, en moneda constante",
         "datos": [{"valores": _datos_cmd_real()}], "parametros": {}, "comprobar": _caso_cmd_real_coste},
    ],
    "REI-LEV-001": [
        {"nombre": "suma de vencimientos = deuda; vencimientos a 24 meses (% de la deuda) y su dispersión",
         "datos": [{"valores": _datos_rei_lev()}], "parametros": {}, "comprobar": _caso_rei_lev_vencimientos},
        {"nombre": "LTV, ICR y deuda neta/EBITDA del agregado y LTV ante caídas de valor de −10 % y −20 %",
         "datos": [{"valores": _datos_rei_lev()}], "parametros": {}, "comprobar": _caso_rei_lev_ratios},
        {"nombre": "impacto en FFO de refinanciar al coste actual (swap + margen) y holgura frente a covenants",
         "datos": [{"valores": _datos_rei_lev()}], "parametros": {}, "comprobar": _caso_rei_lev_refinanciacion},
    ],
    "CHR-ONCHAIN-001": [
        {"nombre": "MVRV = 1 si precio = coste medio (y MVRV-Z = 0)",
         "datos": [{"valores": _datos_chr_onchain(coste_medio=True)}], "parametros": {},
         "comprobar": _caso_chr_onchain_coste_medio},
        {"nombre": "método a mano: MVRV, MVRV-Z, NVT, señal NVT con media de 90 días y percentiles",
         "datos": [{"valores": _datos_chr_onchain()}], "parametros": {}, "comprobar": _caso_chr_onchain_metodo},
        {"nombre": "señal NVT con otra media (30 días)",
         "datos": [{"valores": _datos_chr_onchain()}], "parametros": {"media_nvt": 30},
         "comprobar": lambda r: _caso_chr_onchain_metodo(r, 30)},
    ],
    "CHR-TOKEN-001": [
        {"nombre": "circulante = total = máxima ⇒ FDV/CM = 1, sin inflación ni desbloqueos",
         "datos": [{"valores": _datos_chr_token(sin_dilucion=True)}], "parametros": {}, "comprobar": _caso_chr_token_sin_dilucion},
        {"nombre": "método a mano: FDV/CM, inflación neta y desbloqueos a 30 y 90 días, ponderados por capitalización",
         "datos": [{"valores": _datos_chr_token()}], "parametros": {}, "comprobar": _caso_chr_token_metodo},
        {"nombre": "rendimiento real de staking = nominal − inflación neta; concentración de tenedores y su cobertura",
         "datos": [{"valores": _datos_chr_token()}], "parametros": {}, "comprobar": _caso_chr_token_staking},
    ],
    "PRV-PME-001": [
        {"nombre": "flujos que replican el índice ⇒ KS-PME = 1 (alfa directo 0 y λ de PME+ = 1)",
         "datos": [{"valores": _datos_prv_pme(replica=True)}], "parametros": {"metodo": "PME+"}, "comprobar": _caso_prv_pme_replica},
        {"nombre": "método a mano: KS-PME, TVPI, DPI, TIR y alfa directo (valor actual neto nulo)",
         "datos": [{"valores": _datos_prv_pme()}], "parametros": {}, "comprobar": _caso_prv_pme_metodo},
        {"nombre": "PME+: factor λ de las distribuciones y TIR del índice",
         "datos": [{"valores": _datos_prv_pme()}], "parametros": {"metodo": "PME+"}, "comprobar": _caso_prv_pme_plus},
    ],
    "PRV-CF-001": [
        {"nombre": "TVPI = DPI + RVPI; TIR con valor actual neto nulo y curva J a mano",
         "datos": [{"valores": _datos_prv_cf()}], "parametros": {}, "comprobar": _caso_prv_cf_multiplos},
        {"nombre": "TIR exacta: 100 aportados y 121 de NAV a los dos años ⇒ 10 %",
         "datos": [{"valores": _datos_prv_cf(simple=True)}], "parametros": {}, "comprobar": _caso_prv_cf_tir},
        {"nombre": "proyección de Takahashi-Alexander a mano (tasas de aportación, bow y crecimiento declarados)",
         "datos": [{"valores": _datos_prv_cf()}],
         "parametros": {"tasas_aportacion": [0.25, 0.33, 0.5], "crecimiento": 0.08}, "comprobar": _caso_prv_cf_proyeccion},
    ],
    "ALT-HF-001": [
        {"nombre": "coherencia con ACC-FACT-001: mismos datos y factores FF5+UMD, mismas exposiciones, alfa, t y R²",
         "datos": [{"valores": _datos_alt_hf(_HF_FF)}], "parametros": {"factores": list(_HF_FF), "desuavizar": False},
         "comprobar": _caso_alt_hf_acc_fact},
        {"nombre": "siete factores de Fung-Hsieh: recupera alfa y exposiciones exactas; media = alfa + factores",
         "datos": [{"valores": _datos_alt_hf(UMBRALES["ALT-HF-001"]["factores_fung_hsieh"])}],
         "parametros": {"desuavizar": False}, "comprobar": _caso_alt_hf_exacto},
        {"nombre": "desuavizado previo (Geltner con φ del AR(1), ALT-DESMOOTH-001) y regresión a mano",
         "datos": [{"valores": _datos_alt_hf(UMBRALES["ALT-HF-001"]["factores_fung_hsieh"], suavizada=True)}],
         "parametros": {}, "comprobar": _caso_alt_hf_desuavizado},
    ],
    "ALT-AUC-001": [
        {"nombre": "índice = 100 en la base; ventas repetidas recuperan el índice con el que se construyeron los precios",
         "datos": [{"valores": _datos_alt_auc()}], "parametros": {}, "comprobar": _caso_alt_auc_base},
        {"nombre": "segunda vía: el método alternativo (hedónico frente a ventas repetidas) da el mismo índice",
         "datos": [{"valores": _datos_alt_auc()}], "parametros": {"metodo": "hedonico"}, "comprobar": _caso_alt_auc_segunda_via},
        {"nombre": "Bailey-Muth-Nourse a mano con ruido: índice, rentabilidad bruta y neta (15 %), volatilidad y dispersión",
         "datos": [{"valores": _datos_alt_auc(ruido=0.2)}], "parametros": {"comisiones": 0.15}, "comprobar": _caso_alt_auc_metodo},
    ],
}
