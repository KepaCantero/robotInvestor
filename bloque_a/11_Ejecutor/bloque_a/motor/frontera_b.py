"""Frontera con el Bloque B (1.6 del Catálogo): reglas comunes de las fichas del Motor con componentes.

T-127 (QA r02 de T-119, H-10; ronda r02, QA r01 H-01 y H-02) las escribió para FIR-CRED-001, REI-LEV-001 y CHR-TOKEN-001
(`fichas_p2`); T-128 las saca a este módulo para aplicarlas también a REI-NAV-001 y REI-FFO-001 (`fichas_reales`),
IDX-REB-001 (`fichas_mon_idx`), FON-DISC-001 y FON-TD-001 (`fichas_fon_der`). Ninguna cifra de una entrega puede ser la de
un instrumento concreto (un valor, una emisión, una sociedad, un fondo, un token), ni con su identificador ni de forma que
se pueda despejar de una sola respuesta, salvo que quien pide haya construido los componentes para ello (T-135, QA r03 de
T-127, H-08: es el límite declarado del último párrafo, INC-T127-01 «Ronda r03»):

- casi clones: dos componentes con los mismos datos a menos de `tolerancia_clon` son uno (`_sin_clones`);
- copias a escala: dos componentes con las mismas cifras individuales (cocientes que no dependen del tamaño) son uno para el
  mínimo, la dominancia, los estadísticos de orden y los subconjuntos (`_sin_copias_a_escala`); en series de precios (la
  amplitud de IDX-CONC-001, T-135), dos series con las mismas rentabilidades o, salvo el redondeo de cada una, con un
  cociente de precios constante (T-144) (`_etiquetas_series_copiadas`);
- dominancia (1, k): ningún componente (o grupo de copias) pesa más de `peso_maximo_componente` de una base del agregado
  (`_sin_dominio`), ni aporta más de eso a una cifra agregada (`_aportacion_maxima`, `_concentradas`);
- estadísticos de orden (mínimo, cuartiles, máximo) solo con `componentes_minimos_orden` componentes distintos (`_orden`).

Los números están en `FRONTERA_B` [PROPUESTO INC-T127-01]; cada ficha los lleva en sus `UMBRALES` o los lee de aquí, y la
petición no los cambia.

T-127 r03 (QA r02, H-04 y H-05; T-128 r02, H-01): límite declarado. Los componentes los aporta quien pide (datos en línea
de CT-09: HT-01 solo sirve series de precios, no balances, ofertas de tokens ni flujos), así que ninguna regla sobre ellos
distingue un emisor troceado en partes, o copiado con perturbaciones simétricas, de varios emisores reales: estas reglas
evitan la revelación por descuido (uno o pocos componentes, casi clones, copias a escala, dominancia), no la de un
solicitante que construye los componentes a propósito. Lo cubren el propósito de la petición (1.6) y el Registro de
cálculos, que guarda los datos en línea de cada petición; `_aviso_casi_clones` deja en él un aviso cuando dos componentes
solo difieren en un dato (pregunta para T-57, INC-T127-01 «Ronda r03»).
"""
from __future__ import annotations

from typing import Any

import numpy as np
from scipy.sparse import csgraph, csr_matrix

from .operaciones import ErrorFicha

# ------------------------------------------------------------------ frontera con el Bloque B (1.6) [PROPUESTO INC-T127-01]
# T-127 (QA r02 de T-119, H-10). Reglas comunes de FIR-CRED-001, REI-LEV-001 y CHR-TOKEN-001 para que ninguna cifra de la
# entrega sea la de un emisor o un token concreto. Las tres fichas las llevan en sus `UMBRALES` (la petición no las cambia).
ESTADISTICOS_ORDEN = ("minimo", "q25", "mediana", "q75", "maximo")   # los que entrega `_distribucion`
FRONTERA_B: dict[str, Any] = {
    # Casi clones: dos componentes cuyos datos del cálculo difieren todos, cada uno, en menos de un 1 % relativo son el
    # mismo emisor o token con ruido; su agregado sería su cifra con dos o más cifras significativas.
    "tolerancia_clon": 0.01,
    # Regla de dominancia (1, k) del control de revelación estadística: ningún componente puede pesar más del 95 % de una
    # base de ponderación del agregado (por encima, el agregado es la cifra de ese componente). Los casos de control llegan
    # a un 88,9 % (la FDV de TKA en CHR-TOKEN-001; T-127 r02: el caso «sin dilución», que llegaba al 90,9 %, es ahora la
    # propia red). T-127 r02 (QA r01, H-01 y H-02): el mismo 95 % se aplica a los grupos de componentes con las mismas
    # cifras individuales (copias a escala) y a la aportación a cada cifra agregada (Σ|wᵢ·xᵢ|), no solo a su peso.
    "peso_maximo_componente": 0.95,
    # Estadísticos de orden solo con al menos 7 componentes distintos: con n ≤ 6, los cinco estadísticos (cuantiles de tipo 7)
    # y el agregado ponderado de la misma métrica son n ecuaciones o más que dan la cifra de cada componente.
    "componentes_minimos_orden": len(ESTADISTICOS_ORDEN) + 2,
    # T-144 (QA r01 de T-135, H-01) [PROPUESTO INC-T128-01]: tolerancia numérica de la regla de niveles de las copias de una
    # serie de precios (`_etiquetas_series_copiadas`): la de verificación de IDX-CONC-001, la ficha que la usa
    # (`FICHAS["IDX-CONC-001"]["tol"]`, 1e-10; `tests/test_t144.py` comprueba que son la misma). Fija el paso de precio de
    # una serie sin redondear y el margen del error de coma flotante de los logaritmos.
    "tolerancia_numerica_copias": 1e-10,
}
# T-127 r03 (QA r02, H-04) [PROPUESTO INC-T127-01]: aviso, no rechazo. Dos componentes que coinciden (a menos de
# `tolerancia_clon`) en todos los datos del cálculo menos uno son, con toda probabilidad, un mismo emisor con un dato movido
# (la perturbación simétrica más sencilla: σ·(1 ± δ)); dos emisores reales que coincidan en todos los demás datos a la vez
# no se esperan, por lo mismo que los casi clones. No se rechaza porque moviendo dos datos, o troceando, se esquiva igual:
# la entrega lleva el aviso como limitación y queda en el Registro de cálculos con los datos de la petición.
# T-135 (QA r03 de T-127, H-06) [PROPUESTO INC-T127-01]: un dato ausente (``None``) o nulo (0) en los dos componentes no es
# una coincidencia que informe (dos tokens sin oferta máxima, o sin emisión ni quema, no son por eso el mismo); el par
# tiene que coincidir además en al menos `coincidencias_informativas_minimas` datos no triviales: uno más de los que se le
# permite mover (`datos_distintos_aviso` + 1), para que lo que coincide pese más que lo que difiere.
AVISO_B: dict[str, Any] = {"datos_distintos_aviso": 1, "coincidencias_informativas_minimas": 2}


def _distribucion(x: np.ndarray) -> dict[str, float]:
    """Dispersión de los componentes: mediana, cuartiles (tipo 7, ST-DESC-001), mínimo y máximo."""
    q25, q50, q75 = (float(q) for q in np.quantile(x, [0.25, 0.5, 0.75]))
    return {"mediana": q50, "q25": q25, "q75": q75, "minimo": float(np.min(x)), "maximo": float(np.max(x))}


def _datos_que_coinciden(firmas: list[tuple[Any, ...]], tol: float) -> np.ndarray:
    """Matriz n × n: cuántos datos de la firma de cada par de componentes son iguales a menos de `tol` relativo
    (|a − b| ≤ tol·max(|a|, |b|); un dato ausente, ``None``, solo es igual a otro ausente)."""
    n = len(firmas)
    iguales = np.zeros((n, n), dtype=int)
    for j in range(len(firmas[0]) if n else 0):
        nulo = np.array([f[j] is None for f in firmas])
        x = np.array([0.0 if f[j] is None else float(f[j]) for f in firmas])
        a = np.abs(x)
        cerca = np.abs(x[:, None] - x[None, :]) <= tol * np.maximum(a[:, None], a[None, :])
        iguales += cerca & (nulo[:, None] == nulo[None, :])
    return iguales


def _etiquetas_casi_iguales(firmas: list[tuple[Any, ...]], tol: float) -> np.ndarray:
    """T-127 (H-10): el grupo de cada componente; en un grupo, los que tienen los mismos datos a menos de `tol` relativo en
    cada uno (`_datos_que_coinciden`). Dos componentes casi iguales a un tercero están en su grupo aunque entre ellos
    difieran algo más (cierre transitivo): una cadena de casi clones es un solo componente."""
    n = len(firmas)
    if not n:
        return np.zeros(0, dtype=int)
    cerca = _datos_que_coinciden(firmas, tol) == len(firmas[0])
    return np.asarray(csgraph.connected_components(csr_matrix(cerca), directed=False)[1], dtype=int)


# T-149 (QA r01 de T-144, H-01) [PROPUESTO INC-T128-01]: rejillas de precio de la regla de niveles (`_paso_de_precio`).
# Además de las potencias de 10, los pasos de cotización de las tablas de los mercados: 2·10⁻ᵈ, 5·10⁻ᵈ y 25·10⁻ᵈ
# (= 2,5·10⁻ᵈ⁺¹: 0,25, 0,025…) dentro de cada década, y las fracciones 1/2ᵏ hasta 1/`denominador_binario_maximo` (octavos,
# treintaidosavos de los bonos y sus cuartos, 1/128, y 1/256). Un paso más grueso que el real solo ensancha la cota (se
# agrupa más: falla cerrado); uno más fino la estrecha y deja pasar una copia, así que se busca el mayor que encaje. Una
# serie está en una rejilla si lo están al menos `fraccion_en_rejilla` de sus precios: así un precio suelto sin redondear,
# o unos pocos de otra fuente, no la hunden al paso de la coma flotante. Ha de ser bastante mayor que 1/2, la fracción de
# precios de una rejilla que caen por azar en la siguiente más gruesa que la contiene (los pares de 0,01 en 0,02).
REJILLAS_PRECIO: dict[str, Any] = {"multiplos_de_la_decada": (25, 5, 2), "denominador_binario_maximo": 256,
                                   "fraccion_en_rejilla": 0.9}


def _en_rejilla(x: np.ndarray, hay: np.ndarray, paso: np.ndarray, tol_numerica: float) -> np.ndarray:
    """T-149: qué series tienen al menos `fraccion_en_rejilla` de sus precios en múltiplos de su `paso` (uno por serie) a
    menos de `tol_numerica` relativo. Una serie sin precios encaja en cualquiera (no tiene fechas comunes con nadie)."""
    y = np.abs(x / paso[:, None])
    resto = np.rint(y)
    np.subtract(y, resto, out=resto)
    np.abs(resto, out=resto)                              # |y − round(y)|
    np.maximum(y, 1.0, out=y)
    y *= tol_numerica                                     # tol·max(|y|, 1)
    encaja = resto <= y
    encaja &= hay
    return encaja.sum(axis=1) >= REJILLAS_PRECIO["fraccion_en_rejilla"] * hay.sum(axis=1)


def _paso_de_precio(precios: np.ndarray, hay: np.ndarray, tol_numerica: float) -> np.ndarray:
    """T-144 (QA r01 de T-135, H-01): el paso de precio de cada serie. Primero la mayor potencia de 10, 10⁻ᵈ (desde la de
    su mayor precio hasta las cifras decimales que guarda un float64), en la que está la serie; después, la mayor rejilla
    de `REJILLAS_PRECIO` más gruesa que esa potencia en la que también está (T-149, QA r01 de T-144, H-01: los múltiplos
    de 0,05 lo son de 0,01, y con 0,01 el error de redondeo supuesto era la quinta parte del real). Una serie está en una
    rejilla si lo están `fraccion_en_rejilla` de sus precios (T-149: un precio suelto sin redondear la llevaba antes al
    paso de la coma flotante). Una serie sin redondear encaja cuando 10ᵈ·p pasa de 1/(2·`tol_numerica`), así que su paso
    relativo (paso / precio) es como mucho del orden de `tol_numerica`: la cota de redondeo nunca es más laxa que eso
    para una serie de precio corriente."""
    n = precios.shape[0]
    paso = np.zeros(n)
    sin_paso = np.ones(n, dtype=bool)
    x = np.where(hay, precios, 0.0)
    mayor = float(np.max(np.abs(x))) if x.size else 0.0
    d0 = -int(np.floor(np.log10(mayor))) if mayor >= 1 else 0   # la década del mayor precio: un paso de 10, 50 o 100
    for d in range(d0, np.finfo(float).precision + 1):
        nuevos = sin_paso & _en_rejilla(x, hay, np.full(n, 10.0 ** -d), tol_numerica)
        paso[nuevos] = 10.0 ** -d
        sin_paso &= ~nuevos
        if not sin_paso.any():
            break
    potencia = paso.copy()
    for m in REJILLAS_PRECIO["multiplos_de_la_decada"]:
        filas = np.flatnonzero((potencia > 0) & (m * potencia > paso))
        if len(filas):
            mejor = filas[_en_rejilla(x[filas], hay[filas], m * potencia[filas], tol_numerica)]
            paso[mejor] = m * potencia[mejor]
    # 1/2ᵏ = 5ᵏ·10⁻ᵏ: una serie en esa rejilla está también en la de 10⁻ᵏ, así que solo se mira donde la potencia llega
    for k in range(1, int(np.log2(REJILLAS_PRECIO["denominador_binario_maximo"])) + 1):
        q = 2.0 ** -k
        filas = np.flatnonzero((potencia >= 10.0 ** -k * (1 - tol_numerica)) & (q > paso))
        if len(filas):
            mejor = filas[_en_rejilla(x[filas], hay[filas], np.full(len(filas), q), tol_numerica)]
            paso[mejor] = q
    return paso


def _paso_por_decada(precios: np.ndarray, hay: np.ndarray, tol_numerica: float) -> np.ndarray:
    """T-149 (QA r01 de T-144, H-01): el paso de cada precio según los de su serie en su misma década (10ᵏ ≤ p < 10ᵏ⁺¹),
    n × T. Una serie redondeada a cifras significativas cambia de paso al cruzar una potencia de 10 (4 cifras: 0,01 por
    debajo de 100 y 0,1 por encima); el paso de la serie entera es el de la parte más fina. Solo se calcula para las
    series que cruzan una década; en las demás es el de la serie (0 aquí: `_etiquetas_series_copiadas` toma el mayor)."""
    paso = np.zeros(precios.shape)
    dec = np.where(hay, np.floor(np.log10(np.where(hay, precios, 1.0))), np.nan)
    cruzan = np.flatnonzero(np.nanmax(dec, axis=1, initial=-np.inf) > np.nanmin(dec, axis=1, initial=np.inf))
    if not len(cruzan):
        return paso
    sub, dsub = precios[cruzan], dec[cruzan]
    for k in np.unique(dsub[~np.isnan(dsub)]):
        en = dsub == k
        paso[cruzan] = np.where(en, _paso_de_precio(sub, en, tol_numerica)[:, None], paso[cruzan])
    return paso


def _pares(n: int, limite: int):
    """Los pares (i, k) con i < k, en tramos de unos `limite` pares (la memoria no crece con n²)."""
    i0 = 0
    while i0 < n - 1:
        filas: list[int] = []
        cuenta = 0
        while i0 < n - 1 and (not filas or cuenta + (n - 1 - i0) <= limite):
            filas.append(i0)
            cuenta += n - 1 - i0
            i0 += 1
        I = np.concatenate([np.full(n - 1 - i, i) for i in filas])
        K = np.concatenate([np.arange(i + 1, n) for i in filas])
        yield I, K


def _pares_por_hipotesis(n: int, limite: int, con_paso: np.ndarray):
    """T-150 (QA r01 de T-149, H-05): los pares de `_pares` bajo cada hipótesis de cómo se llevó cada serie a su paso:
    redondeada (fila i) o truncada hacia abajo (fila n + i de `_etiquetas_series_copiadas`). Una serie sin paso que cuente
    (`con_paso` falso: sin redondear) es la misma en las dos, así que sus pares truncados no se repiten."""
    for di, dk in ((0, 0), (n, 0), (0, n), (n, n)):
        for I, K in _pares(n, limite):
            if di or dk:
                quedan = (con_paso[I] | (di == 0)) & (con_paso[K] | (dk == 0))
                I, K = I[quedan], K[quedan]
                if not len(I):
                    continue
            yield I + di, K + dk


# T-144 (QA r01 de T-135, H-03): elementos de cada tramo de pares × fechas que se compara de una vez. Solo cambia el coste y
# la memoria (unos 8 MB por matriz), no el resultado (`tests/test_t144.py` lo comprueba con un tramo pequeño)
ELEMENTOS_POR_TRAMO = 1 << 20


def _etiquetas_series_copiadas(precios: np.ndarray, anios: np.ndarray, tol: float, anios_minimos: float,
                               tol_numerica: float | None = None) -> np.ndarray:
    """T-135 (QA r02 de T-128, H-05): el grupo de cada serie de precios, con sus copias. `precios` es n × T (NaN donde la
    serie no tiene precio) sobre las T fechas comunes, con `anios` la posición de cada fecha en años. Dos series son
    copias (exactas o a escala ×c) de un mismo valor si sus precios comunes abarcan al menos `anios_minimos` y cumplen
    una de estas dos reglas:

    - **rentabilidades** (T-135): en todas las fechas en que las dos tienen rentabilidad (cada una entre sus propios
      precios consecutivos) coinciden a menos de `tol` relativo (la regla de los casi clones, `_datos_que_coinciden`);
    - **niveles** (T-144, QA r01 de T-135, H-01): en sus fechas comunes, el cociente de precios es una constante salvo el
      redondeo de cada serie. Con pᵢ redondeado a su paso qᵢ (`_paso_de_precio`), |log pᵢ − log p̃ᵢ| ≤ −log(1 − qᵢ/2pᵢ);
      son copias si hay una constante c con |log(pᵢ/pₖ) − c| ≤ bᵢ + bₖ + 2·`tol_numerica` en cada fecha común, la cota
      tope en log(1 + `tol`) (nunca más laxa que la de los casi clones). Así se agrupan la misma serie con una sesión
      ausente (solo cuentan las fechas comunes), en otra divisa a un cambio fijo, en libras redondeada a 2 decimales (la
      acción que cotiza en peniques) o de otra fuente con 2 o 3 decimales. Dos series de verdad distintas pero muy
      correladas no: con datos sin redondear la cota es del orden de `tol_numerica`, y el cociente de dos índices con
      ρ ≈ 0,995 o de un fondo y su índice con un error de seguimiento de 0,01 %/año se mueve mucho más que eso.

    T-149 (QA r01 de T-144, H-01): el paso de cada serie admite las rejillas de `REJILLAS_PRECIO` (0,05, 0,25, 1/8,
    1/32…), no solo potencias de 10, aunque una minoría de sus precios no esté en ella, y el de cada precio es el mayor de
    los de su serie entera y de su década (`_paso_por_decada`: cifras significativas).

    Cierre transitivo, como en `_etiquetas_casi_iguales`. Límites declarados (INC-T128-01): una copia con rentabilidades
    perturbadas a propósito, desfasada una sesión o con un cambio de divisa variable no se detecta; con un paso de precio
    grande frente al precio (p. ej. 0,01 en un valor de 0,50) la cota llega a la de los casi clones y dos series que se
    mueven poco pueden tomarse por copias (falla cerrado: la amplitud no se sirve). T-149: tampoco se agrupa una copia
    en una rejilla que no es de `REJILLAS_PRECIO` (pasos de 0,03 o de 1/3), una que cambia de resolución dentro de una
    misma década (2 decimales unos meses y 1 después, o una tabla de paso por tramo de precio como las de MiFID II:
    0,01 por debajo de 40 y 0,05 por encima) ni una con más de 1 − `fraccion_en_rejilla` de sus precios fuera de su
    rejilla. T-150 (QA r01 de T-149, H-05): una copia truncada hacia abajo (⌊p/q⌋·q) sí se agrupa (cada serie se prueba
    redondeada y truncada); una redondeada hacia arriba (⌈p/q⌉·q), no (límite declarado en INC-T127-01, ronda T-150).

    T-144 (H-03): se comparan solo los pares que siguen siendo candidatos (en tramos de `ELEMENTOS_POR_TRAMO`); un par sale
    en cuanto incumple las dos reglas, así que el coste es del orden de n²·(unas pocas fechas) y no n²·T."""
    n = precios.shape[0]
    if not n:
        return np.zeros(0, dtype=int)
    tol_num = FRONTERA_B["tolerancia_numerica_copias"] if tol_numerica is None else float(tol_numerica)
    T = precios.shape[1]
    hay = ~np.isnan(precios)
    rend = np.full(precios.shape, np.nan)
    for i in range(n):
        donde = np.flatnonzero(hay[i])
        rend[i, donde[1:]] = precios[i, donde[1:]] / precios[i, donde[:-1]] - 1
    logp = np.log(np.where(hay, precios, 1.0))
    paso = _paso_de_precio(precios, hay, tol_num)
    rel = np.where(hay, paso[:, None] / (2 * np.where(hay, precios, 1.0)), 0.0)
    rel = np.maximum(rel, _paso_por_decada(precios, hay, tol_num) / (2 * np.where(hay, precios, 1.0)))   # T-149
    cota_redondeo = -np.log1p(-np.minimum(rel, 0.5)) + tol_num
    # T-150 (QA r01 de T-149, H-05): una copia truncada hacia abajo (p̃ = ⌊p/q⌋·q) tiene el valor de verdad en [p̃, p̃ +
    # q): un paso entero, siempre por debajo, que la cota de medio paso centrada en p̃ no cubre cuando el precio cambia.
    # Su hipótesis es la misma cota de medio paso centrada en p̃ + q/2: log p̃ + log(1 + q/2p̃), con media anchura
    # (q/2)/(p̃ + q/2). Cada serie va dos veces (filas i y n + i) y un par es copia si lo es en alguna de las cuatro
    # combinaciones (`_pares_por_hipotesis`). No ensancha la cota (eso dobla los falsos positivos): solo la desplaza. Se
    # desplaza solo en los precios cuyo paso entero, q/p, no pasa de 2·`tol` (T-152; era `tol`): con un paso grande frente
    # al precio (1 en un monetario a 1,00) la cota ya llega al tope, y desplazarla medio paso, que cambia con el precio,
    # alinea por azar series distintas (el límite declarado de los pasos grandes); esos precios se quedan como
    # redondeados. Una serie sin ningún precio desplazado más que `tol_numerica` (sin redondear) es la misma en las dos
    # hipótesis.
    # T-152 (QA r01 de T-150, H-02; decisión del operador del 16-11-2026): el umbral es q/p ≤ 2·`tol` (la media anchura
    # q/2p, `rel`, no pasa de `tol`), no q/p ≤ `tol`. Es donde la cota llega al tope: medido con 100 semillas
    # (`.docs/tickets/T-152/medir_umbral.py`), entre q/p del 1 y del 2 % agrupa las copias truncadas sin agrupar más series
    # distintas; con todos los precios por encima, la cota está en el tope y el umbral no cambia nada. Una serie que cruza el
    # 2 % se desplaza a medias y su resultado sí depende del umbral (T-190, límite declarado en INC-T127-01).
    desplaza = rel <= tol
    logp = np.vstack([logp, logp + np.where(desplaza, np.log1p(rel), 0.0)])
    cota_redondeo = np.vstack([cota_redondeo, np.where(desplaza, -np.log1p(-np.minimum(rel / (1 + rel), 0.5)) + tol_num,
                                                       cota_redondeo)])
    con_paso = (desplaza & (rel > tol_num)).any(axis=1)
    tope = float(np.log1p(tol))
    filas: list[np.ndarray] = []
    columnas: list[np.ndarray] = []
    for I, K in _pares_por_hipotesis(n, ELEMENTOS_POR_TRAMO, con_paso):
        m = len(I)
        vivos = np.arange(m)
        lo, hi = np.full(m, -np.inf), np.full(m, np.inf)
        distinta = np.zeros(m, dtype=bool)
        primera, ultima = np.full(m, np.inf), np.full(m, -np.inf)
        j = 0
        while j < T and len(vivos):
            Iv, Kv = I[vivos], K[vivos]
            Ib, Kb = Iv % n, Kv % n                       # la serie de cada fila (T-150)
            tramo = slice(j, j + max(1, min(T - j, ELEMENTOS_POR_TRAMO // len(vivos))))
            comun = hay[Ib, tramo] & hay[Kb, tramo]
            a = anios[tramo][None, :]
            primera[vivos] = np.minimum(primera[vivos], np.where(comun, a, np.inf).min(axis=1))
            ultima[vivos] = np.maximum(ultima[vivos], np.where(comun, a, -np.inf).max(axis=1))
            ri, rk = rend[Ib, tramo], rend[Kb, tramo]
            ambas = ~np.isnan(ri) & ~np.isnan(rk)
            x, y = np.where(ambas, ri, 0.0), np.where(ambas, rk, 0.0)
            cerca = np.abs(x - y) <= tol * np.maximum(np.abs(x), np.abs(y))
            distinta[vivos] |= (ambas & ~cerca).any(axis=1)
            L = logp[Iv, tramo] - logp[Kv, tramo]
            B = np.minimum(cota_redondeo[Iv, tramo] + cota_redondeo[Kv, tramo], tope)
            lo[vivos] = np.maximum(lo[vivos], np.where(comun, L - B, -np.inf).max(axis=1))
            hi[vivos] = np.minimum(hi[vivos], np.where(comun, L + B, np.inf).min(axis=1))
            vivos = vivos[~(distinta[vivos] & (lo[vivos] > hi[vivos]))]
            j = tramo.stop
        copia = vivos[ultima[vivos] - primera[vivos] >= anios_minimos]   # sin pareja, cada serie es su propio grupo
        filas.append(I[copia])
        columnas.append(K[copia])
    f = np.concatenate(filas) % n if filas else np.zeros(0, dtype=int)
    c = np.concatenate(columnas) % n if columnas else np.zeros(0, dtype=int)
    grafo = csr_matrix((np.ones(len(f), dtype=bool), (f, c)), shape=(n, n))
    return np.asarray(csgraph.connected_components(grafo, directed=False)[1], dtype=int)


def _aviso_casi_clones(firmas: list[tuple[Any, ...]], tol: float, lim: list[str],
                       repetidos: list[tuple[bool, ...]] | None = None) -> int:
    """T-127 r03 (QA r02, H-04): cuántos componentes coinciden con otro, a menos de `tol`, en todos los datos de su firma
    menos `datos_distintos_aviso` (`AVISO_B`) o menos; si hay alguno, un aviso en las limitaciones (va al Registro de
    cálculos con los datos de la petición). No rechaza: es la marca de una perturbación de un dato, no una regla que
    impida el troceo (límite declarado en INC-T127-01 «Ronda r03»). El aviso no cita identificadores.

    T-135 (QA r03 de T-127, H-06): las coincidencias triviales (``None`` con ``None``, 0 con 0) siguen contando para «todos
    menos d», pero el par tiene que coincidir además en `coincidencias_informativas_minimas` datos que no lo sean. La ficha
    pone a ``None`` en la firma los datos que se derivan de otros (`otros_pasivos` de REI-NAV-001 cuando se calcula por
    diferencia): no son datos de quien pide.

    T-144 (QA r01 de T-135, H-02): un dato que repite otro del mismo componente (la oferta total cuando toda está en
    circulación) va en la firma tal cual, y `repetidos` (una tupla de booleanos por componente, como su firma) lo marca.
    Si los dos componentes lo repiten, ese dato no es uno más: su coincidencia o su diferencia es la del dato que repite,
    así que cuenta como coincidencia trivial (iguala, pero no informa). Si solo uno de los dos lo repite, se compara como
    los demás: mover el dato del que cuelga (la circulante de una copia) es un dato movido, no dos. En T-135 se ponía a
    ``None`` y mover la oferta circulante de una copia daba dos diferencias (sin aviso)."""
    n = len(firmas)
    if n < 2:
        return 0
    d = AVISO_B["datos_distintos_aviso"]
    iguales = _datos_que_coinciden(firmas, tol)
    triviales = np.zeros((n, n), dtype=int)
    for j in range(len(firmas[0])):
        nulo = np.array([f[j] is None for f in firmas])
        cero = np.array([f[j] is not None and float(f[j]) == 0 for f in firmas])
        rep = np.array([bool(r[j]) for r in repetidos]) if repetidos is not None else np.zeros(n, dtype=bool)
        dos_rep = rep[:, None] & rep[None, :]
        if dos_rep.any():   # T-144 (H-02): lo repetido en los dos iguala siempre (su diferencia es la de su dato)
            x = np.array([0.0 if f[j] is None else float(f[j]) for f in firmas])
            a = np.abs(x)
            igual_j = (np.abs(x[:, None] - x[None, :]) <= tol * np.maximum(a[:, None], a[None, :])) & (nulo[:, None] == nulo[None, :])
            iguales = iguales + (dos_rep & ~igual_j)
        triviales += (nulo[:, None] & nulo[None, :]) | (cero[:, None] & cero[None, :]) | dos_rep
    par = (iguales >= len(firmas[0]) - d) & (iguales - triviales >= AVISO_B["coincidencias_informativas_minimas"])
    np.fill_diagonal(par, False)
    k = int(np.sum(par.any(axis=1)))
    if k:
        lim.append(f"aviso (1.6): {k} componentes coinciden con otro en todos los datos del cálculo menos {d} (a menos del "
                   f"{tol:.0%}): pueden ser un mismo emisor con un dato movido, y el agregado, su cifra; la petición queda "
                   f"en el Registro de cálculos con sus datos")
    return k


def _grupos_casi_iguales(firmas: list[tuple[Any, ...]], tol: float) -> int:
    """T-127 (H-10): número de grupos de `_etiquetas_casi_iguales`."""
    return len(set(_etiquetas_casi_iguales(firmas, tol).tolist()))


def _sin_copias_a_escala(cifras: list[tuple[Any, ...]], que: str, minimo: int, tol: float) -> np.ndarray:
    """T-127 r02 (QA r01, H-01): las cifras individuales que la ficha agrega no dependen del tamaño del componente (son
    cocientes). Dos componentes con las mismas cifras a menos de `tol` (copias a escala de un emisor, aunque difieran sus
    importes) son, para la frontera, un solo componente: el agregado de copias es la cifra de una. Devuelve el grupo de
    cada componente y rechaza si hay menos de `minimo` grupos (el mensaje no cita identificadores)."""
    grupos = _etiquetas_casi_iguales(cifras, tol)
    distintos = len(set(grupos.tolist()))
    if distintos < minimo:
        raise ErrorFicha(f"{que}: rechazo: {distintos} componentes distintos por sus cifras individuales (< {minimo}): "
                         f"{len(cifras) - distintos} tienen las mismas cifras que otro (a menos del {tol:.0%}) aunque "
                         f"difieran sus importes; un componente copiado a otra escala no cuenta como componente distinto "
                         f"del agregado (1.6)")
    return grupos


def _por_grupo(x: Any, grupos: np.ndarray | None) -> np.ndarray:
    """Suma de |x| de cada grupo de `_sin_copias_a_escala` (sin grupos, cada componente es el suyo)."""
    a = np.abs(np.asarray(x, dtype=float))
    if grupos is None or not len(a):
        return a
    return np.bincount(grupos, weights=a)


def _aportacion_maxima(num: Any, den: Any, tol: float, cero: float) -> float:
    """T-127 r02 (QA r01, H-02): parte de la cifra agregada Σnumᵢ/Σdenᵢ (una media ponderada es num = wᵢ·xᵢ, den = wᵢ) que
    aporta el componente que más aporta junto con los que tienen su misma cifra numᵢ/denᵢ a menos de `tol` relativo:
    max_i Σ_{j ~ i}|numⱼ| / Σ|numⱼ|. Con rellenos de cifra nula, o con copias que solo comparten esa cifra, es 1: el
    agregado dividido por el peso del componente (que conoce quien pide) da su cifra. Un agregado nulo a la tolerancia de
    la ficha (`cero`) no es la cifra de nadie: 0.

    T-127 r03 (QA r02, H-05): también con signo. Con rellenos que se compensan (+X y −X), el resto no aporta nada neto al
    agregado aunque Σ|numⱼ| sea grande; por eso se toma además 1 − |Σnum − num_G| / |Σnum| (num_G, la suma con signo del
    grupo) y se devuelve la mayor de las dos. Con las dos por debajo de k, el agregado dividido por el peso del grupo da su
    cifra con un error relativo de al menos (1 − k)/(2 − k) (≈ 4,76 % con k = 95 %), sea cual sea el signo del resto."""
    n_ = np.asarray(num, dtype=float)
    d_ = np.asarray(den, dtype=float)
    a = np.abs(n_)
    total = float(np.sum(a))
    suma_den = float(np.sum(d_))
    if not total > 0 or (suma_den != 0 and abs(float(np.sum(n_)) / suma_den) <= cero):
        return 0.0
    definida = d_ != 0
    x = np.where(definida, n_ / np.where(definida, d_, 1.0), 0.0)
    ax = np.abs(x)
    cerca = np.abs(x[:, None] - x[None, :]) <= tol * np.maximum(ax[:, None], ax[None, :])
    cerca &= definida[:, None] & definida[None, :]
    np.fill_diagonal(cerca, True)
    grupo = cerca.astype(float)
    sin_signo = float(np.max(grupo @ a)) / total
    suma = float(np.sum(n_))
    if suma == 0:
        return sin_signo
    con_signo = 1.0 - float(np.min(np.abs(suma - grupo @ n_))) / abs(suma)
    return max(sin_signo, con_signo)


def _concentradas(cifras: dict[str, tuple[Any, Any]], u: dict[str, Any], cero: float) -> list[str]:
    """T-127 r02 (H-02): las cifras agregadas de `cifras` (nombre → (num, den)) cuya aportación pasa de
    `peso_maximo_componente`."""
    return [k for k, (n_, d_) in cifras.items()
            if _aportacion_maxima(n_, d_, u["tolerancia_clon"], cero) > u["peso_maximo_componente"]]


def _rechazo_concentradas(nombres: list[str], que: str, u: dict[str, Any]) -> None:
    if nombres:
        raise ErrorFicha(f"{que}: rechazo: más del {u['peso_maximo_componente']:.0%} de {', '.join(nombres)} lo aporta un "
                         f"componente (o varios con su misma cifra): el agregado dividido por su peso sería la cifra de ese "
                         f"componente (1.6)")


def _limitacion_concentradas(nombres: list[str], u: dict[str, Any], lim: list[str]) -> None:
    if nombres:
        lim.append(f"sin {', '.join(nombres)}: más del {u['peso_maximo_componente']:.0%} lo aporta un componente (o varios "
                   f"con su misma cifra); sería la cifra de ese componente (1.6)")


def _sin_clones(firmas: list[tuple[Any, ...]], que: str, tol: float) -> None:
    """Ronda r02 (QA r01, H-01): dos componentes con los mismos datos son el mismo emisor (o token) con otro identificador;
    no cuentan como componentes distintos y el agregado se rechaza (el mensaje no cita identificadores). T-127 (QA r02,
    H-10): «los mismos» a menos de `tol` relativo en cada dato del cálculo (`FRONTERA_B`), no solo exactamente."""
    repetidos = len(firmas) - _grupos_casi_iguales(firmas, tol)
    if repetidos:
        raise ErrorFicha(f"{que}: rechazo: {repetidos} componentes con los mismos datos que otro (a menos del {tol:.0%} "
                         f"relativo en cada dato del cálculo): un componente repetido con otro identificador no cuenta "
                         f"como componente distinto del agregado (1.6)")


def _sin_dominio(bases: dict[str, Any], que: str, peso_maximo: float, grupos: np.ndarray | None = None) -> None:
    """T-127 (H-10): regla de dominancia (1, k). Si un componente pesa más de `peso_maximo` de una base de ponderación del
    agregado (la suma de los valores absolutos), el agregado es su cifra: se rechaza (el mensaje no cita identificadores).
    T-127 r02 (H-01): con `grupos`, el peso es el de cada grupo de copias a escala (`_sin_copias_a_escala`)."""
    for nombre, x in bases.items():
        a = _por_grupo(x, grupos)
        total = float(np.sum(a))
        peso = float(np.max(a)) / total if total > 0 else 0.0
        if peso > peso_maximo:
            raise ErrorFicha(f"{que}: rechazo: un componente pesa el {peso:.4%} de «{nombre}» (más del {peso_maximo:.0%}): "
                             f"el agregado sería la cifra de ese componente (1.6)")


def _orden(x: np.ndarray, u: dict[str, Any], sin_orden: list[str], que: str,
           distintos: int | None = None) -> dict[str, float] | None:
    """T-127 (H-10): la dispersión de `_distribucion` si hay al menos `componentes_minimos_orden` componentes; si no,
    ``None``, y `que` se apunta en `sin_orden` para declararlo una vez en las limitaciones. T-127 r02 (H-01): los
    componentes que cuentan son los `distintos` por sus cifras (los grupos de copias a escala), si se dan."""
    if (len(x) if distintos is None else distintos) >= u["componentes_minimos_orden"]:
        return _distribucion(x)
    sin_orden.append(que)
    return None


def _limitacion_orden(sin_orden: list[str], u: dict[str, Any], lim: list[str]) -> None:
    if sin_orden:
        lim.append(f"sin estadísticos de orden de {', '.join(dict.fromkeys(sin_orden))}: menos de "
                   f"{u['componentes_minimos_orden']} componentes distintos; con tan pocos, el mínimo, los cuartiles y el "
                   f"máximo darían la cifra de cada componente (1.6)")
