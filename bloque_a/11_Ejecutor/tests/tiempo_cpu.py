"""T-199: medida del coste de las pruebas de tiempo, que no dependa de la carga de la máquina.

- `time.process_time()` (como T-168): el tiempo de CPU del proceso, no el de reloj. Lo que hacen otros procesos no cuenta.
- Con el recolector de basura parado mientras se mide: su coste depende de lo que han dejado vivo las demás pruebas de la
  suite (miles, en el mismo proceso), no de la función que se mide.
- `minimos_intercalados`: para las pruebas que comparan dos tamaños, cada medida se repite y se queda la mínima, con los
  tamaños alternados, de modo que una ráfaga de carga (caché o frecuencia compartidas) no cae solo sobre uno de los dos.
"""
from __future__ import annotations

import gc
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager

REPETICIONES = 3   # medidas por tamaño en `minimos_intercalados`; la mínima es la menos afectada por la carga


class Medida:
    segundos: float = 0.0


@contextmanager
def medir_cpu() -> Iterator[Medida]:
    """`with medir_cpu() as m: …` y después `m.segundos`: el tiempo de CPU del bloque, sin el recolector de basura."""
    m = Medida()
    activo = gc.isenabled()
    gc.disable()
    t0 = time.process_time()
    try:
        yield m
    finally:
        m.segundos = time.process_time() - t0
        if activo:
            gc.enable()


def cpu(funcion: Callable[[], object]) -> float:
    with medir_cpu() as m:
        funcion()
    return m.segundos


def minimos_intercalados(*funciones: Callable[[], object], repeticiones: int = REPETICIONES) -> list[float]:
    """El mínimo de `repeticiones` medidas de cada función, alternándolas (a, b, a, b, …)."""
    mejores = [float("inf")] * len(funciones)
    for _ in range(repeticiones):
        for i, f in enumerate(funciones):
            mejores[i] = min(mejores[i], cpu(f))
    return mejores
