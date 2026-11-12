"""QA r01 de T-103 (revisor independiente): tiempo de R8 con entradas adversarias tras el `RE_ESCAPES` nuevo (H-40).

Uso: python -I r01_02_r8_rendimiento.py <ruta a bloque_a/11_Ejecutor> [<ruta anterior a T-103>]
Mide `contenido_sensible` y `contiene_credenciales` con tramos largos de barras invertidas que NO acaban en un escape (la
alternativa `\\\\+(?:…)` vuelve a empezar en cada barra del tramo y lo recorre entero: coste cuadrático). Con la segunda ruta,
compara con el código anterior en un proceso aparte. FALLO si una entrada de 100 000 caracteres tarda más de LIMITE_S segundos
(el peor tiempo que registró `r04_01` de T-92 para sus entradas adversarias fue 0,92 s; se usa 2 s de margen). Comprueba además
que la variante propuesta (`(?<!\\\\)\\\\++…`) da la misma sustitución en 300 000 cadenas aleatorias y es lineal. Sin red.
"""
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
ANTES = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
LIMITE_S = 2.0

PROG = r"""
import json, sys, time
sys.path.insert(0, sys.argv[1])
from bloque_a.llm import contenido_sensible
from bloque_a.contratos import contiene_credenciales
out = {}
for nombre, t in json.load(sys.stdin).items():
    t0 = time.perf_counter(); contenido_sensible(t); a = time.perf_counter() - t0
    t0 = time.perf_counter(); contiene_credenciales({"dato": t}); b = time.perf_counter() - t0
    out[nombre] = [round(a, 3), round(b, 3)]
print(json.dumps(out))
"""


def medir(ruta, entradas):
    r = subprocess.run([sys.executable, "-I", "-c", PROG, str(ruta)], input=json.dumps(entradas), capture_output=True, text=True,
                       check=True, timeout=1800)
    return json.loads(r.stdout)


B = "\\"
entradas = {
    "10 000 barras + «z»": B * 10_000 + "z",
    "20 000 barras + «z»": B * 20_000 + "z",
    "100 000 caracteres: 99 999 barras + «z»": B * 99_999 + "z",
    "100 000 caracteres: 1 000 tramos de 99 barras + «q»": (B * 99 + "q") * 1_000,
    "100 000 caracteres: 100 tramos de 999 barras + «q»": (B * 999 + "q") * 100,
    "100 000 caracteres: «%» + «25» × 49 999 + «z»": "%" + "25" * 49_999 + "z",
    "100 000 caracteres: barras solas": B * 100_000,
}
fallos = 0
ahora = medir(EJ, entradas)
prev = medir(ANTES, entradas) if ANTES else {k: None for k in entradas}
for nombre in entradas:
    a, b = ahora[nombre]
    largo = len(entradas[nombre]) >= 100_000
    ok = not largo or max(a, b) <= LIMITE_S
    fallos += 0 if ok else 1
    print(f"{'OK   ' if ok else 'FALLO'} {nombre}: contenido_sensible {a} s, contiene_credenciales {b} s (antes: {prev[nombre]})")

# ---------------------------------------------------------------------------------------------- variante lineal propuesta
sys.path.insert(0, str(EJ))
from bloque_a.contratos import RE_ESCAPES  # noqa: E402

PROPUESTA = re.compile(r"(?<!\\)" + RE_ESCAPES.pattern.replace("\\\\+(?:", "\\\\++(?:", 1))
assert PROPUESTA.pattern != RE_ESCAPES.pattern
rnd = random.Random(20261112)
alfabeto = "\\\\\\\\nturbfx0123u4567UaAbBcCdDeEfF%25zZ\"/ s"
dif = 0
for _ in range(300_000):
    s = "".join(rnd.choice(alfabeto) for _ in range(rnd.randint(1, 18)))
    dif += RE_ESCAPES.sub(" ", s) != PROPUESTA.sub(" ", s)
t0 = time.perf_counter()
PROPUESTA.sub(" ", B * 1_000_000 + "z")
t = time.perf_counter() - t0
print(f"INFO  variante propuesta {PROPUESTA.pattern!r}: {dif} diferencias en 300 000 cadenas; 1 000 000 barras + «z» en {t:.3f} s")
print(f"fallos: {fallos}")
sys.exit(1 if fallos else 0)
