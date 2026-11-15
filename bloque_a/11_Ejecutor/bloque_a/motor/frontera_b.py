"""Frontera con el Bloque B (1.6 del Catálogo): reglas comunes de las fichas del Motor con componentes.

T-127 (QA r02 de T-119, H-10; ronda r02, QA r01 H-01 y H-02) las escribió para FIR-CRED-001, REI-LEV-001 y CHR-TOKEN-001
(`fichas_p2`); T-128 las saca a este módulo para aplicarlas también a REI-NAV-001 y REI-FFO-001 (`fichas_reales`),
IDX-REB-001 (`fichas_mon_idx`), FON-DISC-001 y FON-TD-001 (`fichas_fon_der`). Ninguna cifra de una entrega puede ser la de
un instrumento concreto (un valor, una emisión, una sociedad, un fondo, un token), ni con su identificador ni de forma que
se pueda despejar de una sola respuesta:

- casi clones: dos componentes con los mismos datos a menos de `tolerancia_clon` son uno (`_sin_clones`);
- copias a escala: dos componentes con las mismas cifras individuales (cocientes que no dependen del tamaño) son uno para el
  mínimo, la dominancia, los estadísticos de orden y los subconjuntos (`_sin_copias_a_escala`);
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
}
# T-127 r03 (QA r02, H-04) [PROPUESTO INC-T127-01]: aviso, no rechazo. Dos componentes que coinciden (a menos de
# `tolerancia_clon`) en todos los datos del cálculo menos uno son, con toda probabilidad, un mismo emisor con un dato movido
# (la perturbación simétrica más sencilla: σ·(1 ± δ)); dos emisores reales que coincidan en todos los demás datos a la vez
# no se esperan, por lo mismo que los casi clones. No se rechaza porque moviendo dos datos, o troceando, se esquiva igual:
# la entrega lleva el aviso como limitación y queda en el Registro de cálculos con los datos de la petición.
AVISO_B: dict[str, Any] = {"datos_distintos_aviso": 1}


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


def _aviso_casi_clones(firmas: list[tuple[Any, ...]], tol: float, lim: list[str]) -> int:
    """T-127 r03 (QA r02, H-04): cuántos componentes coinciden con otro, a menos de `tol`, en todos los datos de su firma
    menos `datos_distintos_aviso` (`AVISO_B`) o menos; si hay alguno, un aviso en las limitaciones (va al Registro de
    cálculos con los datos de la petición). No rechaza: es la marca de una perturbación de un dato, no una regla que
    impida el troceo (límite declarado en INC-T127-01 «Ronda r03»). El aviso no cita identificadores."""
    n = len(firmas)
    if n < 2:
        return 0
    d = AVISO_B["datos_distintos_aviso"]
    par = _datos_que_coinciden(firmas, tol) >= len(firmas[0]) - d
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
