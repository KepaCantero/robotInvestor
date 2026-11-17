"""T-168 QA r01 · 01: las cuatro cargas medidas con reloj y con CPU, con y sin carga extra.
Comprueba además que la ruta medida no crea hilos ni procesos (cuyo coste escaparía a process_time)
y que process_time no cuenta a los hijos. Uso, desde bloque_a/11_Ejecutor:
    python <este script> [n_quemadores]"""
import multiprocessing as mp
import os
import resource
import sys
import threading
import time

sys.path.insert(0, "tests")
import test_t102_filtro as t  # noqa: E402
from bloque_a import diseno_v6 as v6  # noqa: E402

M = t.MARCAS


def cargas(perm):
    def c1():
        for x in ["Apple Microsoft Alphabet Amazon " * 2000, "acciones de " * 2500, "Comprar oro, " * 2500, "{n_ideas} " * 5000]:
            v6.texto_prohibido(x, perm, M)

    def c2():
        for x in (" " * 50_000 + "x", "\t" * 50_000 + "x", "a." + " " * 50_000 + "b"):
            v6.limpiar(x, perm, M)

    def c3():
        for n in (20000, 40000):
            v6.frase_prohibida("A." * n, perm)
            v6.frase_prohibida("Abc " * n + "Inc", perm)

    def c4():
        for n in (16000, 32000):
            v6.frase_prohibida("{tipo:RV}" + " " * n + "{tipo:RV}", perm)
    return {"textos_largos (<2)": c1, "r04_espacios (<2)": c2, "r05_h37 (<2)": c3, "r06_h45 (<1)": c4}


def quemar(_):
    fin = time.time() + 60
    x = 0
    while time.time() < fin:
        x += 1


def main():
    import tempfile
    from pathlib import Path
    perm = v6.permitidos_r21(t._bloque(Path(tempfile.mkdtemp())))
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    procs = [mp.Process(target=quemar, args=(i,), daemon=True) for i in range(n)]
    for p in procs:
        p.start()
    time.sleep(1)
    print(f"carga: {os.getloadavg()} · quemadores extra: {n} · núcleos: {os.cpu_count()}")
    hilos0, hijos0 = threading.active_count(), resource.getrusage(resource.RUSAGE_CHILDREN)
    for nombre, f in cargas(perm).items():
        th0 = set(threading.enumerate())
        r0 = resource.getrusage(resource.RUSAGE_SELF)
        w0, c0, tc0 = time.perf_counter(), time.process_time(), time.thread_time()
        f()
        w, c, tc = time.perf_counter() - w0, time.process_time() - c0, time.thread_time() - tc0
        r1 = resource.getrusage(resource.RUSAGE_SELF)
        nuevos = set(threading.enumerate()) - th0
        print(f"{nombre:20s} reloj {w:6.3f} s · CPU proceso {c:6.3f} s · CPU hilo principal {tc:6.3f} s · "
              f"cambios de contexto involuntarios {r1.ru_nivcsw - r0.ru_nivcsw} · hilos nuevos {len(nuevos)}")
    hijos1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    print(f"hilos antes/después: {hilos0}/{threading.active_count()} · CPU de hijos durante las cargas: "
          f"{(hijos1.ru_utime + hijos1.ru_stime) - (hijos0.ru_utime + hijos0.ru_stime):.3f} s (debe ser 0: no hay hijos)")
    for p in procs:
        p.terminate()


if __name__ == "__main__":
    main()
