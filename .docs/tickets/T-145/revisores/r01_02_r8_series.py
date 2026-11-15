"""QA r01 de T-145 · R8 en series de cinco o más grupos de cuatro cifras (`tarjetas_en_texto`, `_tarjetas_de_la_serie`).

Formas que ni `r01_03` de T-140 ni `medir_filas_r8.py` miran: filas de tabla con longitudes de 5 a 12 y la fecha (o la
hora) detrás, cabeceras de años, precios en el rango de Mastercard; tres tarjetas, tarjetas con separadores mezclados,
«tarjeta, caducidad y año»; series largas (tiempo) y repetición. Las tarjetas se generan al azar con su Luhn y su prefijo:
ninguna está escrita en el fichero (gate de secretos). Solo biblioteca estándar.
Uso (desde la raíz de la copia): python -I r01_02_r8_series.py
"""
import importlib.util
import random
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("c", RAIZ / "bloque_a" / "11_Ejecutor" / "bloque_a" / "contratos.py")
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
rng = random.Random(20261115)
N = 3000
fallos = 0


def tarjeta(prefijo="4", sep=" "):
    while True:
        c = prefijo + "".join(str(rng.randint(0, 9)) for _ in range(15 - len(prefijo)))
        for d in "0123456789":
            if C._luhn(c + d):
                return sep.join((c + d)[i:i + 4] for i in range(0, 16, 4))


def mc():
    return tarjeta(rng.choice(["51", "52", "53", "54", "55"]))


def cad():
    return f"{rng.randint(1, 12):02d}{rng.randint(26, 35)}"


def tasa(nombre, gen, maximo=None, minimo=None, declarado=""):
    global fallos
    rng.seed(nombre)
    n = sum(bool(C.tarjetas_en_texto(gen())) for _ in range(N))
    mal = (maximo is not None and n > maximo * N) or (minimo is not None and n < minimo * N)
    fallos += mal
    print(f"  {'FALLA' if mal else 'ok   '} {nombre:70} {n:4}/{N} ({100 * n / N:5.2f} %) {declarado}")


print("1. falsos positivos (filas de tabla)")
for k in (5, 6, 8, 9, 12):
    tasa(f"{k - 1} niveles de 4000–5999 y la fecha MMDD detrás",
         lambda k=k: " ".join([str(rng.randint(4000, 5999)) for _ in range(k - 1)] + [f"{rng.randint(1, 12):02d}{rng.randint(1, 28):02d}"]),
         maximo=0.08, declarado="(declarado para 4 y 8: 7,1 % y 0,5 %)")
for k in (5, 6, 7, 10, 12):
    tasa(f"{k} números de 1000 a 9999", lambda k=k: " ".join(str(rng.randint(1000, 9999)) for _ in range(k)), maximo=0.005)
tasa("cabecera de años («2019 2020 … 2026»)", lambda: " ".join(str(a) for a in range(rng.randint(2010, 2018), 2027)), maximo=0)
tasa("cuatro precios en 2221–2720 (rango de Mastercard) y la hora HHMM", lambda: " ".join(
    [str(rng.randint(2221, 2720)) for _ in range(4)] + [f"{rng.randint(0, 12):02d}{rng.choice(['00', '15', '30', '45'])}"]),
    maximo=0.10, declarado="(la forma declarada; su techo es Luhn 1/10 × mes válido)")
tasa("fecha MMDD delante, ocho niveles", lambda: " ".join([f"{rng.randint(1, 12):02d}{rng.randint(1, 28):02d}"]
                                                         + [str(rng.randint(4000, 5999)) for _ in range(8)]), maximo=0.01)
tasa("año delante, cuatro niveles y la fecha detrás", lambda: " ".join(
    [str(rng.randint(2015, 2026))] + [str(rng.randint(4000, 5999)) for _ in range(4)] + [f"{rng.randint(1, 12):02d}15"]),
    maximo=0)

print("2. detección (falsos negativos)")
tasa("tres tarjetas seguidas", lambda: f"{tarjeta()} {mc()} {tarjeta()}", minimo=1)
tasa("tres tarjetas, cada una con su caducidad", lambda: f"{tarjeta()} {cad()} {mc()} {cad()} {tarjeta()} {cad()}", minimo=1)
tasa("dos tarjetas y una caducidad al final", lambda: f"{tarjeta()} {mc()} {cad()}", minimo=1)
tasa("tarjeta con guiones y la caducidad con guion", lambda: f"{tarjeta(sep='-')}-{cad()}", minimo=1)
tasa("tarjeta y caducidad con espacio duro", lambda: f"{tarjeta(sep=chr(160))}{chr(160)}{cad()}", minimo=1)
tasa("tarjeta, caducidad y año («… 0128 2028»)", lambda: f"{tarjeta()} {cad()} 2028", declarado="(no declarado tal cual; "
     "INC-T123-01 declara el PIN tras la caducidad)")
tasa("tarjeta, caducidad y CVV de 3 cifras (grupos no todos de cuatro)", lambda: f"{tarjeta()} {cad()} 737", minimo=1)
tasa("tarjeta en una frase con la caducidad tras «/»", lambda: f"pago con {tarjeta()} cad. 01/28", minimo=1)

print("3. series largas y repetición")
largo = " ".join(str(rng.randint(1000, 9999)) for _ in range(200_000))
t0 = time.perf_counter()
C.tarjetas_en_texto(largo)
dt = time.perf_counter() - t0
fallos += dt > 5
print(f"  {'FALLA' if dt > 5 else 'ok   '} 200 000 grupos en {dt:.2f} s")
cadena = " ".join(tarjeta() + " " + cad() for _ in range(5000))
t0 = time.perf_counter()
r1 = C.tarjetas_en_texto(cadena)
dt = time.perf_counter() - t0
r2 = C.tarjetas_en_texto(cadena)
ok = r1 == r2 and len(r1) >= 1 and dt < 5
fallos += not ok
print(f"  {'ok   ' if ok else 'FALLA'} 5000 tarjetas con caducidad seguidas: {len(r1)} distintas (enmascaradas), {dt:.2f} s, "
      "repetir da lo mismo")
print(f"\nfallos: {fallos}")
