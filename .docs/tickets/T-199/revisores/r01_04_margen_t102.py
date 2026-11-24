"""QA r01 de T-199 (revisor): CPU de las cuatro pruebas de tiempo de T-102 (T-168), que T-199 no toca, frente a sus topes.
Uso (desde bloque_a/11_Ejecutor/tests): PYTHONPATH=. ../../../.venv/bin/python ../../../.docs/tickets/T-199/revisores/r01_04_margen_t102.py"""
import inspect
import time

import test_t102_filtro as T

import tempfile
from pathlib import Path

perm = T.v6.permitidos_r21(T._bloque(Path(tempfile.mkdtemp())))
for nombre in ("test_textos_largos_en_tiempo_lineal", "test_r04_muchos_espacios_en_tiempo_lineal",
               "test_r05_h37_sufijo_en_tiempo_lineal", "test_r06_h45_marcador_y_muchos_espacios_en_tiempo_lineal"):
    f = getattr(T, nombre)
    medidas = []
    for _ in range(5):
        c, w = time.process_time(), time.perf_counter()
        f(perm)
        medidas.append((time.process_time() - c, time.perf_counter() - w))
    tope = [ln for ln in inspect.getsource(f).splitlines() if "process_time() - t0 <" in ln][0].split("<")[-1].strip()
    print(f"{nombre}: CPU {min(m[0] for m in medidas):.2f}–{max(m[0] for m in medidas):.2f} s, reloj hasta {max(m[1] for m in medidas):.2f} s; tope {tope}")
