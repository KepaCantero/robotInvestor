"""QA r02 de T-103 (revisor independiente): R8 con entradas adversarias nuevas tras `(?<!\\\\)\\\\++…` (H-47), y equivalencia
de la expresión nueva con la de la r01.

Uso: python -I r02_02_r8_rendimiento_adversario.py <ruta a bloque_a/11_Ejecutor en 7feb697> [<ruta en 33385c9 o 9297df9>]

1. Equivalencia: `RE_ESCAPES.sub` de la r02 y de la r01 dan lo mismo en 400 000 cadenas aleatorias de un alfabeto hostil
   (barras, letras de escape, hexadecimales, «%», «25», «u», «U», «x», octales, comillas). Sin la segunda ruta, se compara con
   la expresión de la r01 copiada aquí.
2. Linealidad: tiempos de `contenido_sensible` y `contiene_credenciales` con entradas de 100 000 y 1 000 000 de caracteres;
   FALLO si una de 100 000 tarda más de LIMITE_S (2 s, el criterio de CA-6) o si el cociente 1 000 000 / 100 000 pasa de 30
   (lineal da unas 10 veces).
3. (INFO) Estructuras anidadas: `contenido_sensible` vuelca el JSON de cada dict en cada nivel, así que su coste es la
   profundidad por el tamaño. No es de la r02; se mide para declararlo.
Sin red, sin claves (las entradas no contienen ninguna).
"""
import json
import random
import re
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
ANTES = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
LIMITE_S = 2.0
fallos = 0


def ver(ok, nombre, detalle=""):
    global fallos
    print(f"{'OK   ' if ok else 'FALLO'} {nombre}{' — ' + str(detalle) if detalle else ''}")
    fallos += 0 if ok else 1


ESC_R01 = re.compile(r"\\+(?:u[0-9a-fA-F]{4}|U[0-9a-fA-F]{8}|x[0-9a-fA-F]{2}|[0-7]{1,3}|[ntrbf/\"])"
                     r"|%(?:25)*(?:u[0-9A-Fa-f]{4}|[0-9A-Fa-f]{2})")

sys.path.insert(0, str(EJ))
from bloque_a import contratos as C

print("--- 1. Equivalencia de la sustitución (r02 frente a r01)")
if ANTES:
    prog = ("import sys,re; sys.path.insert(0, sys.argv[1]); from bloque_a.contratos import RE_ESCAPES as R;"
            "print(R.pattern)")
    patron_antes = subprocess.run([sys.executable, "-I", "-c", prog, str(ANTES)], capture_output=True, text=True,
                                  check=True).stdout.rstrip("\n")
    viejo = re.compile(patron_antes)
else:
    viejo = ESC_R01
print(f"INFO  r01: {viejo.pattern[:60]}…  r02: {C.RE_ESCAPES.pattern[:60]}…")
rnd = random.Random(20261112)
ALF = ["\\", "\\", "\\", "n", "t", "r", "b", "f", "/", '"', "u", "U", "x", "0", "7", "8", "a", "F", "g", "%", "2", "5", "z", " ",
       "sk-", "\\\\", "%25", "%5C", "\\u00", "\\x"]
distintas = 0
ejemplo = None
for i in range(400_000):
    s = "".join(rnd.choice(ALF) for _ in range(rnd.randint(1, 24)))
    if C.RE_ESCAPES.sub(" ", s) != viejo.sub(" ", s):
        distintas += 1
        ejemplo = ejemplo or s
ver(distintas == 0, "misma sustitución en 400 000 cadenas", f"{distintas} distintas{'; p. ej. ' + repr(ejemplo) if ejemplo else ''}")
# casos dirigidos: el tramo empieza tras un escape que acaba justo antes de una barra
for s in ["\\n\\\\nsk-", "%5C\\\\n", "\\u0041\\\\\\t", "\\\\\\", "a\\\\\\\\\\\\\\\\b", "\\x41\\x42\\\\x43", "%2525\\\\\\\\n",
          "\\" * 7 + "u00e9" + "\\" * 3 + "U0001F511"]:
    ver(C.RE_ESCAPES.sub(" ", s) == viejo.sub(" ", s), f"dirigido {s!r}", C.RE_ESCAPES.sub(" ", s))

print("--- 2. Linealidad con entradas adversarias (100 000 y 1 000 000 de caracteres)")
PROG = r"""
import json, sys, time
sys.path.insert(0, sys.argv[1])
from bloque_a.llm import contenido_sensible
from bloque_a.contratos import contiene_credenciales
gen = {
 "barras + z": lambda n: "\\" * (n - 1) + "z",
 "barras solas": lambda n: "\\" * n,
 "barras + u casi escape": lambda n: ("\\" * 97 + "u00g") * (n // 101),
 "barras + %": lambda n: ("\\" * 50 + "%") * (n // 51),
 "barra y z alternas": lambda n: "\\z" * (n // 2),
 "dos barras y z": lambda n: "\\\\z" * (n // 3),
 "%25 sin fin": lambda n: "%" + "25" * (n // 2 - 1) + "z",
 "%25 repetido": lambda n: "%25" * (n // 3),
 "%u casi": lambda n: "%u00g" * (n // 5),
 "sk- y 19 caracteres": lambda n: ("sk-" + "a" * 19 + " ") * (n // 23),
 "sk-sk-sk": lambda n: "sk-" * (n // 3),
 "sk- y tramos de cifras": lambda n: "sk-" + "-".join(["123456"] * (n // 7)),
 "sk- y cola de guiones": lambda n: "sk-" + "-" * (n - 3),
 "sk- tras barras": lambda n: ("\\" * 20 + "nsk-" + "a1-" * 10 + " ") * (n // 54),
 "password abierto": lambda n: ('"password"' + " " * 40 + ":") * (n // 51),
 "password sin cierre": lambda n: '"password": "' + "x" * (n - 14),
 "Bearer y espacios": lambda n: ("Bearer" + " " * 60) * (n // 66),
 "BEGIN sin fin": lambda n: "-----BEGIN " + "A " * ((n - 11) // 2),
 "cifras y guiones (DNI)": lambda n: "12345678-" * (n // 9),
}
n = int(sys.argv[2])
out = {}
for nombre, g in gen.items():
    t = g(n)
    t0 = time.perf_counter(); contenido_sensible(t); a = time.perf_counter() - t0
    t0 = time.perf_counter(); contiene_credenciales({"d": t}); b = time.perf_counter() - t0
    out[nombre] = [len(t), round(a, 4), round(b, 4)]
print(json.dumps(out))
"""


def medir(n):
    r = subprocess.run([sys.executable, "-I", "-c", PROG, str(EJ), str(n)], capture_output=True, text=True, check=True, timeout=1200)
    return json.loads(r.stdout)


m1, m2 = medir(100_000), medir(1_000_000)
peor = 0.0
for k in m1:
    l1, a1, b1 = m1[k]
    l2, a2, b2 = m2[k]
    t1, t2 = a1 + b1, a2 + b2
    peor = max(peor, t1)
    cociente = t2 / t1 if t1 > 0.002 else 0.0
    ver(t1 < LIMITE_S and (cociente < 30 or t2 < LIMITE_S), f"{k}",
        f"100k: {a1:.3f}+{b1:.3f} s · 1M: {a2:.3f}+{b2:.3f} s · ×{cociente:.1f}")
print(f"INFO  peor tiempo con 100 000 caracteres: {peor:.3f} s")

print("--- 3. (INFO) Diccionarios anidados: coste profundidad × tamaño (anterior a T-103)")
PROG3 = r"""
import json, sys, time
sys.path.insert(0, sys.argv[1])
from bloque_a.llm import contenido_sensible
from bloque_a.contratos import contiene_credenciales
prof, n = int(sys.argv[2]), int(sys.argv[3])
o = "x" * n
for _ in range(prof):
    o = {"a": o}
t0 = time.perf_counter(); contenido_sensible(o); a = time.perf_counter() - t0
t0 = time.perf_counter(); contiene_credenciales(o); b = time.perf_counter() - t0
print(json.dumps([round(a, 3), round(b, 3)]))
"""
for prof, n in [(10, 100_000), (100, 100_000), (400, 100_000), (400, 1_000_000)]:
    r = subprocess.run([sys.executable, "-I", "-c", PROG3, str(EJ), str(prof), str(n)], capture_output=True, text=True, timeout=1200)
    print(f"INFO  {prof} niveles, hoja de {n} caracteres — contenido_sensible / contiene_credenciales: "
          f"{r.stdout.strip() or r.stderr.strip().splitlines()[-1]}")

print(f"fallos: {fallos}")
sys.exit(1 if fallos else 0)
