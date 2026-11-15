"""T-145 · tasas de R8 en filas de tabla que la regla nueva puede marcar (la fecha detrás) y que no debe marcar. Uso (desde la raíz): python -I .docs/tickets/T-145/medir_filas_r8.py <contratos.py>... (p. ej., el de T-136, el de T-140 y el actual)"""
import importlib.util
import random
import sys

mods = []
for i, r in enumerate(sys.argv[1:]):
    spec = importlib.util.spec_from_file_location(f"c{i}", r); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); mods.append(m)
N = 5000
def nivel(rng): return str(rng.randint(4000, 5999))
def oro(rng): return str(rng.randint(1800, 2700))
def mmdd(rng): return f"{rng.randint(1, 12):02d}{rng.randint(1, 28):02d}"
def cualquiera(rng): return str(rng.randint(1000, 9999))
filas = {
    "cuatro cierres de un índice y la fecha MMDD detrás": lambda r: " ".join([nivel(r) for _ in range(4)] + [mmdd(r)]),
    "cuatro cierres, fecha MMDD y otro cierre": lambda r: " ".join([nivel(r) for _ in range(4)] + [mmdd(r), nivel(r)]),
    "cuatro precios del oro y la fecha MMDD detrás": lambda r: " ".join([oro(r) for _ in range(4)] + [mmdd(r)]),
    "ocho cierres y la fecha MMDD detrás": lambda r: " ".join([nivel(r) for _ in range(8)] + [mmdd(r)]),
    "cinco números de cuatro cifras al azar (1000–9999)": lambda r: " ".join(cualquiera(r) for _ in range(5)),
    "seis números de cuatro cifras al azar": lambda r: " ".join(cualquiera(r) for _ in range(6)),
    "fecha MMDD, cuatro cierres y otra fecha": lambda r: " ".join([mmdd(r)] + [nivel(r) for _ in range(4)] + [mmdd(r)]),
}
for nombre, gen in filas.items():
    tasas = []
    for m in mods:
        rng = random.Random(nombre)
        tasas.append(sum(bool(m.tarjetas_en_texto(gen(rng))) for _ in range(N)))
    print(f"  {nombre:52} " + " · ".join(f"{t:4}/{N} ({100*t/N:4.1f} %)" for t in tasas))
