"""QA r01 de T-137 · R8, series de cinco o más grupos de cuatro cifras (`tarjetas_en_texto`, `_forma_de_fecha`).

Falsos positivos nuevos (filas de tabla que T-136 no marcaba) y falsos negativos que INC-T123-01 no declara. Compara con el
`contratos.py` de T-136 (el del commit anterior), que se pasa como argumento. Solo biblioteca estándar.
Las tarjetas se generan al azar con su Luhn y su prefijo de red: no hay ninguna escrita en el fichero (gate de secretos).
Uso (desde la raíz de la copia): python -I r01_03_tarjetas_series_largas.py <contratos.py de T-136>
"""
import importlib.util
import random
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]


def cargar(ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


NUEVO = cargar(RAIZ / "bloque_a" / "11_Ejecutor" / "bloque_a" / "contratos.py", "c_nuevo")
VIEJO = cargar(sys.argv[1], "c_viejo") if len(sys.argv) > 1 else None
rng = random.Random(20261115)
N = 2000


def tarjeta(prefijo="4"):
    while True:
        c = prefijo + "".join(str(rng.randint(0, 9)) for _ in range(15 - len(prefijo)))
        for d in "0123456789":
            if NUEVO._luhn(c + d):
                return " ".join((c + d)[i:i + 4] for i in range(0, 16, 4))


def tasa(gen, mod):
    return sum(bool(mod.tarjetas_en_texto(gen())) for _ in range(N))


def fila(nombre, gen, esperado_cero):
    rng.seed(nombre)
    n = tasa(gen, NUEVO)
    rng.seed(nombre)
    v = tasa(gen, VIEJO) if VIEJO else None
    marca = "FALLA" if (esperado_cero and n) or (not esperado_cero and n < N) else "ok   "
    print(f"  {marca} {nombre:62} T-137 {n:4}/{N} ({100 * n / N:4.1f} %)" + (f" · T-136 {v:4}/{N}" if v is not None else ""))
    return n


def nivel():
    return str(rng.randint(4000, 5999))        # p. ej. S&P 500 o Euro Stoxx 50 de 2021–2024 (prefijo 4 o 51–55: Visa o MC)


def oro():
    return str(rng.randint(1800, 2700))        # oro en USD por onza de 2020–2024 (2221–2720: prefijo de Mastercard)


def anio():
    return str(rng.randint(2015, 2026))


def mmdd():
    return f"{rng.randint(1, 12):02d}{rng.randint(1, 28):02d}"


print("1. falsos positivos: filas de tabla de cinco o más números de cuatro cifras (T-136 no marcaba ninguna)")
fp = 0
fp += fila("año y cuatro cierres trimestrales de un índice (4000–5999)", lambda: " ".join([anio()] + [nivel() for _ in range(4)]), True)
fp += fila("cuatro cierres de un índice y el año al final", lambda: " ".join([nivel() for _ in range(4)] + [anio()]), True)
fp += fila("fecha MMDD y cuatro cierres", lambda: " ".join([mmdd()] + [nivel() for _ in range(4)]), True)
fp += fila("año y cuatro precios del oro (1800–2700)", lambda: " ".join([anio()] + [oro() for _ in range(4)]), True)
fp += fila("año y cuatro cierres con guiones («2023-4770-…»)", lambda: "-".join([anio()] + [nivel() for _ in range(4)]), True)
fp += fila("dos años y cuatro cierres («2023 2024 …»)", lambda: " ".join([anio(), anio()] + [nivel() for _ in range(4)]), True)
fp += fila("año, cuatro cierres y otro año", lambda: " ".join([anio()] + [nivel() for _ in range(4)] + [anio()]), True)
fp += fila("ocho cierres de un índice (declarado en INC-T123-01: 0,6 %)", lambda: " ".join(nivel() for _ in range(8)), True)
fp += fila("año y ocho cierres", lambda: " ".join([anio()] + [nivel() for _ in range(8)]), True)

print("2. falsos negativos que INC-T123-01 no declara (declara: «una tarjeta seguida de un número de cuatro cifras que no es")
print("   una fecha»)")
fn = 0
fn += N - fila("año, tarjeta y caducidad MMAA («2027 <tarjeta> 0128»)", lambda: f"2027 {tarjeta()} 0128", False)
fn += N - fila("caducidad MMAA delante y año detrás", lambda: f"0128 {tarjeta()} 2028", False)
fn += N - fila("tarjeta, caducidad MMAA y otra tarjeta", lambda: f"{tarjeta()} 0128 {tarjeta(rng.choice(['51', '52', '53', '54', '55']))}", False)
fn += N - fila("dos tarjetas, cada una con su caducidad MMAA", lambda: f"{tarjeta()} 0128 {tarjeta(rng.choice(['51', '52', '53', '54', '55']))} 0329", False)
fn += N - fila("tarjeta, caducidad MMAA y un PIN que no es fecha («… 0128 4321»)", lambda: f"{tarjeta()} 0128 4321", False)
fn += N - fila("número de cliente de 4 cifras delante («4711 <tarjeta>»)", lambda: f"4711 {tarjeta()}", False)
print("3. lo que T-137 dice detectar (control)")
fila("tarjeta y caducidad MMAA", lambda: f"{tarjeta()} 0128", False)
fila("año delante", lambda: f"2026 {tarjeta()}", False)
fila("dos tarjetas seguidas", lambda: f"{tarjeta()} {tarjeta(rng.choice(['51', '52', '53', '54', '55']))}", False)
print("4. idempotencia y orden: el resultado no depende de repetir la llamada; cada tarjeta, una vez")
t1, t2 = tarjeta(), tarjeta("5")
r = NUEVO.tarjetas_en_texto(f"{t1} {t2}")
print(f"  {'ok   ' if r == NUEVO.tarjetas_en_texto(f'{t1} {t2}') and len(r) == len(set(r)) == 2 else 'FALLA'} {r}")
print(f"\nfalsos positivos nuevos en filas: {fp} · falsos negativos no declarados: {fn}")
