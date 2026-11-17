"""T-168 QA r01 · 03: plugin de pytest que, en las cuatro pruebas de tiempo lineal y con el fichero entero,
anota los hilos vivos y la CPU de hijos antes y después de la llamada (debe ser 1 hilo y 0 s de hijos).
Uso, desde bloque_a/11_Ejecutor:  pytest -q -p r01_03_hilos_en_la_medicion tests/test_t102_filtro.py
(con el directorio de este script en PYTHONPATH)."""
import resource
import threading
import time

import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    if "tiempo_lineal" not in item.name:
        yield
        return
    h0 = threading.active_count()
    ch0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    w0, c0 = time.perf_counter(), time.process_time()
    yield
    ch1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    print(f"\n[T-168 r01_03] {item.name}: hilos {h0}->{threading.active_count()} · reloj {time.perf_counter() - w0:.3f} s · "
          f"CPU {time.process_time() - c0:.3f} s · CPU hijos {ch1.ru_utime + ch1.ru_stime - ch0.ru_utime - ch0.ru_stime:.3f} s")
