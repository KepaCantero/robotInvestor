"""QA r01 de T-113 · H-56 de T-104: `contenido_sensible` nuevo frente al anterior (3a5fbfe^), más tiempo, ciclos y fallo cerrado.
Uso (desde bloque_a/11_Ejecutor de la copia): python .../r01_01_sensible_diferencial.py
Las claves falsas van partidas."""
import json
import random
import re
import subprocess
import sys
import threading
import time

sys.path.insert(0, ".")
from bloque_a import llm  # noqa: E402
from bloque_a.contratos import secretos_en_texto  # noqa: E402

fuente = subprocess.run(["git", "show", "3a5fbfe^:bloque_a/11_Ejecutor/bloque_a/llm.py"], capture_output=True, text=True, check=True).stdout
m = re.search(r"^def contenido_sensible\(valor\).*?(?=^\S)", fuente, re.S | re.M)
ns = {"json": json, "secretos_en_texto": secretos_en_texto}
exec(m.group(0), ns)  # noqa: S102 — código del propio repositorio, versión anterior
viejo, nuevo = ns["contenido_sensible"], llm.contenido_sensible

SK = "sk-" + "ant-api03-abcdefghijklmnopqrstuvwxyz0123"
CLAVE = "api" + "_key"
fallos = 0


def caso(nombre, valor, esperado=None):
    global fallos
    try:
        v = viejo(valor)
    except Exception as e:  # noqa: BLE001
        v = f"EXC {type(e).__name__}"
    try:
        n = nuevo(valor)
    except Exception as e:  # noqa: BLE001
        n = f"EXC {type(e).__name__}"
    mal = (v != n) if esperado is None else (n != esperado)
    fallos += mal
    print(f"{'DISTINTO' if mal else 'igual   '} {nombre}: antes={v} ahora={n}" + (f" esperado={esperado}" if esperado is not None else ""))


print("== casos dirigidos")
caso("texto con sk", SK, True)
caso("dict clave:valor patrón", {CLAVE: "abcdef"}, True)
caso("lista > dict clave:valor patrón", [{CLAVE: "abcdef"}], True)
caso("lista > lista > dict patrón", [[{"pass" + "word": "valor-de-prueba"}]], True)
caso("tupla > dict patrón", ({"sec" + "ret": "x1"},), True)
caso("dict > lista > dict patrón", {"a": [{"client_" + "secret": "zz"}]}, True)
caso("sk como CLAVE de un dict dentro de una lista", [{SK: 1}], True)
caso("sk como clave de dict de arriba", {SK: 1}, True)
caso("lista con objeto cuyo str es un secreto en dict", [{"a": type("O", (), {"__str__": lambda s: SK})()}], True)
caso("dict con objeto cuyo str es un secreto", {"a": type("O", (), {"__str__": lambda s: SK})()}, True)
caso("bytes en lista", [SK.encode()], True)
caso("bytes en dict de lista", [{"a": SK.encode()}], True)
caso("conjunto", {SK}, True)
caso("frozenset en tupla", (frozenset({SK}),), True)
caso("None", None, False)
caso("número", 3.5, False)
caso("NaN en dict", {"a": float("nan")}, False)
caso("vacíos", [{}, [], (), set(), ""], False)
caso("mensajes de la API", [[{"type": "text", "text": "hola"}], [{"role": "user", "content": json.dumps({CLAVE: "abcdef"})}]], True)
caso("mensajes de la API con contenido estructurado", [[{"type": "text", "text": "hola"}], [{"role": "user", "content": [{CLAVE: "abcdef"}]}]], True)
caso("clave no texto en dict", {1: SK, (1, 2): "x"})
caso("valor truncado sin comilla", ['{"' + CLAVE + '": "abc'], True)

print("== diferencial al azar (3 000 estructuras)")
rng = random.Random(113)
HOJAS = ["hola", SK, 3, None, 2.5, True, "Bearer " + "a" * 25, "texto normal sk-learn", b"x", SK.encode(), "AKIA" + "ABCDEFGHIJKLMNOP"]
CLAVES = ["a", "b", CLAVE, "pass" + "word", "nota", SK, "sec" + "ret"]


def gen(prof):
    r = rng.random()
    if prof <= 0 or r < 0.35:
        return rng.choice(HOJAS)
    if r < 0.6:
        return {rng.choice(CLAVES): gen(prof - 1) for _ in range(rng.randint(0, 3))}
    if r < 0.8:
        return [gen(prof - 1) for _ in range(rng.randint(0, 3))]
    if r < 0.9:
        return tuple(gen(prof - 1) for _ in range(rng.randint(0, 3)))
    return frozenset(x for x in (rng.choice(HOJAS) for _ in range(2)))


menos = mas = 0
ejemplo = None
for _ in range(3000):
    x = gen(4)
    try:
        v, n = viejo(x), nuevo(x)
    except Exception as e:  # noqa: BLE001
        print("EXC", type(e).__name__, repr(x)[:120]); fallos += 1; continue
    if v and not n:
        menos += 1
        ejemplo = ejemplo or x
    if n and not v:
        mas += 1
print(f"antes sensible y ahora no (REGRESIÓN de R8): {menos}; ahora sensible y antes no: {mas}")
if ejemplo is not None:
    print("  ejemplo:", repr(ejemplo)[:300])
fallos += menos

print("== tiempo")
for prof, tam in ((400, 1 << 20), (900, 1 << 20), (50, 1 << 24)):
    d = "x" * tam
    for _ in range(prof):
        d = {"a": d}
    t0 = time.perf_counter(); r = nuevo(d); print(f"dict {prof} niveles, {tam >> 20} MB: {r} en {time.perf_counter() - t0:.2f} s")
for prof in (400, 5000, 200000):
    d = ["x" * 1000]
    for _ in range(prof):
        d = [d, {"k": "v"}]
    t0 = time.perf_counter(); r = nuevo(d); print(f"lista {prof} niveles: {r} en {time.perf_counter() - t0:.2f} s")
ancho = [{"a": "palabra " * 20, "b": [i, str(i)]} for i in range(200000)]
t0 = time.perf_counter(); r = nuevo(ancho); print(f"lista ancha de 200 000 dicts: {r} en {time.perf_counter() - t0:.2f} s")
t0 = time.perf_counter(); r = nuevo({"x": ancho}); print(f"dict ancho de 200 000 dicts: {r} en {time.perf_counter() - t0:.2f} s")

print("== profundo y fallo cerrado")
p = "inofensivo"
for _ in range(5000):
    p = {"a": [p]}
print("dict de 5 000 niveles SIN secreto ->", nuevo(p), "(se espera True: no se puede comprobar, falla cerrado)")
p = SK
for _ in range(5000):
    p = [{"a": p}]
caso("lista de 5 000 niveles con secreto al fondo", p, True) if False else print("lista 5 000 niveles con secreto al fondo ->", nuevo(p))
p = {CLAVE: "abcdef"}
for _ in range(5000):
    p = [p]
print("lista de 5 000 niveles con dict clave:valor al fondo ->", nuevo(p), "(esperado True)")

print("== ciclos (5 s de tope)")
for nombre, x in (("dict cíclico", (lambda d: (d.__setitem__("a", d), d)[1])({})), ("lista cíclica", (lambda l: (l.append(l), l)[1])([]))):
    res = {}

    def _f(x=x):
        try:
            res["r"] = nuevo(x)
        except Exception as e:  # noqa: BLE001
            res["r"] = f"EXC {type(e).__name__}"
    h = threading.Thread(target=_f, daemon=True); h.start(); h.join(5)
    print(f"{nombre}: {'NO TERMINA (bucle sin fin)' if h.is_alive() else res['r']}")
print("FALLOS:", fallos)
