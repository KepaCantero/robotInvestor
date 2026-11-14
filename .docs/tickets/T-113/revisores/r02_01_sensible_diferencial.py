"""QA r02 de T-113 · H-01: `contenido_sensible` de la r02 frente al de antes de T-113 (3a5fbfe^).
Estructuras dirigidas y al azar: diccionarios dentro de listas, tuplas y conjuntos, anidados y mezclados, claves que no son
texto, bytes, objetos con `str` sensible, estructuras compartidas y cíclicas. Se busca: antes True y ahora no (regresión de
R8), antes False y ahora una excepción, y que acabe siempre. Después, tiempos.
Uso (desde bloque_a/11_Ejecutor de la copia): python .../r02_01_sensible_diferencial.py [n_al_azar] [semilla] [sin_dh] [sin_tiempos]
`sin_dh`: el generador al azar no usa diccionarios con hash (los únicos que caben en un conjunto).
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
PWD = "pass" + "word"
IBAN = "ES" + "91 2100 0418 " + "4502 0005 1332"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1132)
P_DH = 0.0 if "sin_dh" in sys.argv else 0.15


class Obj:
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s


class DH(dict):
    """Diccionario que se puede meter en un conjunto."""

    def __hash__(self):
        return 7


def corre(f, v, t=20.0):
    out = {}

    def _f():
        try:
            out["r"] = f(v)
        except BaseException as exc:  # noqa: BLE001
            out["r"] = type(exc).__name__
    h = threading.Thread(target=_f, daemon=True)
    h.start()
    h.join(t)
    return out.get("r", "NO ACABA")


fallos = 0
cuenta = {"regresion": 0, "nueva_excepcion": 0, "no_acaba": 0, "mas_estricto": 0, "iguales": 0, "otros": 0}


def compara(nombre, v, imprime=False):
    global fallos
    a, b = corre(viejo, v), corre(nuevo, v)
    if b == "NO ACABA":
        cuenta["no_acaba"] += 1
        tipo = "NO ACABA"
    elif a is True and b is not True:
        cuenta["regresion"] += 1
        tipo = "REGRESIÓN"
    elif a is False and b not in (True, False):
        cuenta["nueva_excepcion"] += 1
        tipo = "EXCEPCIÓN NUEVA"
    elif a == b:
        cuenta["iguales"] += 1
        tipo = None
    elif b is True:
        cuenta["mas_estricto"] += 1
        tipo = None
    else:
        cuenta["otros"] += 1
        tipo = "OTRO"
    if tipo in ("REGRESIÓN", "EXCEPCIÓN NUEVA", "NO ACABA"):
        fallos += 1
    if tipo or imprime:
        print(f"  {tipo or 'bien':16s} antes={a!s:15s} ahora={b!s:15s} {nombre}")
    return a, b


print("== dirigidos ==")
par = {CLAVE: "abcdef123456"}
ciclo_l: list = []
ciclo_l.append(ciclo_l)
ciclo_d: dict = {}
ciclo_d["yo"] = ciclo_d
ciclo_ld: list = [{"a": 1}]
ciclo_ld[0]["l"] = ciclo_ld
ciclo_t: list = []
ciclo_t.append((ciclo_t,))
comp = [par]
hondo: list = [par]
for _ in range(3000):
    hondo = [hondo]
hondo_d: dict = dict(par)
for _ in range(3000):
    hondo_d = {"a": hondo_d}
DIRIGIDOS = [
    ("lista > dict", [par]), ("tupla > dict", (par,)), ("lista > lista > dict", [[par]]), ("lista > tupla > lista > dict", [([par],)]),
    ("dict > lista > dict", {"a": [par]}), ("dict > tupla > dict", {"a": (par,)}), ("lista > dict > lista > dict", [{"a": [par]}]),
    ("conjunto > dict con hash", {DH(par)}), ("frozenset > dict con hash", frozenset([DH(par)])),
    ("dict > conjunto > dict con hash", {"a": {DH(par)}}), ("lista > dict > frozenset > dict con hash", [{"a": frozenset([DH(par)])}]),
    ("dict > conjunto > tupla > dict con hash", {"a": {(DH(par),)}}),
    ("lista > dict clave secreta", [{SK: 1}]), ("tupla > dict > dict clave secreta", ({"a": {SK: 1}},)),
    ("lista > dict > objeto str secreto", [{"a": Obj(SK)}]), ("lista > objeto str secreto (no se mira: igual que antes)", [Obj(SK)]),
    ("lista > dict clave entera y par", [{1: 2, CLAVE: "abcdef"}]), ("lista > dict clave None y par", [{None: 2, PWD: "abcdef"}]),
    ("lista > [dict clave tupla, texto secreto]", [{(1, 2): 1}, SK]), ("lista > [texto secreto, dict clave tupla]", [SK, {(1, 2): 1}]),
    ("lista > [dict con par, dict clave tupla]", [par, {(1, 2): 1}]), ("lista > [dict clave tupla, dict con par]", [{(1, 2): 1}, par]),
    ("lista > dict clave tupla sin secreto", [{(1, 2): 1}]), ("dict clave tupla sin secreto", {(1, 2): 1}),
    ("lista > dict clave bytes con par", [{b"k": 1, CLAVE: "abcdef"}]), ("lista > dict {clave tupla, valor secreto}", [{(1, 2): SK}]),
    ("lista > dict {clave tupla: dict con par}", [{(1, 2): par}]), ("lista > dict {a: dict clave tupla, b: dict par}", [{"a": {(1,): 1}, "b": par}]),
    ("bytes secreto en lista > dict", [{"a": SK.encode()}]), ("bytearray par JSON", [bytearray(json.dumps(par).encode())]),
    ("bytes par JSON dentro de dict > tupla", {"a": (json.dumps(par).encode(),)}), ("IBAN con espacios en lista > dict > lista", [{"a": [IBAN]}]),
    ("lista que se contiene", ciclo_l), ("dict que se contiene", ciclo_d), ("lista > dict > la lista", ciclo_ld), ("lista > tupla > la lista", ciclo_t),
    ("[lista cíclica, par]", [ciclo_l, par]), ("[par, lista cíclica]", [par, ciclo_l]),
    ("compartida dos veces (no es ciclo)", [comp, comp, {"a": comp}]), ("compartida sin secreto", [[{"a": 1}]] * 3),
    ("3000 listas > dict con par", hondo), ("3000 dict > par", hondo_d), ("lista > 3000 dict > par", [hondo_d]),
    ("vacíos", [[], {}, (), set(), frozenset(), "", b""]), ("números y None", [1, 2.5, None, True, float("nan")]),
    ("par con el valor vacío (no es secreto)", [{CLAVE: ""}]), ("par partido en dos dict", [{CLAVE: 1}, {"x": "abcdef"}]),
    ("dict cuya clave es el par JSON", [{json.dumps(par): 1}]), ("lista > dict > str con par escapado", [{"a": json.dumps(json.dumps(par))}]),
]
for nombre, v in DIRIGIDOS:
    compara(nombre, v, imprime=True)
dirigidos = dict(cuenta)

print(f"== al azar ({N}) ==")
HOJAS_MALAS = [SK, SK.encode(), "Bearer " + "abcdefghijklmnopqrstuvwxyz012345", IBAN, Obj(SK), json.dumps(par), "AKIA" + "ABCDEFGHIJKLMNOP"]
HOJAS = ["hola", "", 1, 2.5, None, True, b"bytes", "ES", "clave", Obj("nada"), "sk-", "abcdef123456"]
CLAVES_MALAS = [CLAVE, PWD, "secret", SK, "access" + "_token"]
CLAVES = ["a", "b", "c", "valor", 1, None, 2.5, True]
CLAVES_RARAS = [(1, 2), b"k", frozenset([1])]
fondo: list = []


def gen(prof, p_malo, p_raro):
    r = rng.random()
    if prof <= 0 or r < 0.25:
        if rng.random() < p_malo:
            return rng.choice(HOJAS_MALAS)
        return rng.choice(HOJAS)
    if r < 0.30 and fondo:
        return rng.choice(fondo)        # estructura compartida
    n = rng.randint(0, 4)
    if r < 0.60:
        d = DH() if rng.random() < P_DH else {}
        for _ in range(n):
            if rng.random() < p_raro:
                k = rng.choice(CLAVES_RARAS)
            elif rng.random() < p_malo:
                k = rng.choice(CLAVES_MALAS)
            else:
                k = rng.choice(CLAVES)
            d[k] = gen(prof - 1, p_malo, p_raro)
        fondo.append(d)
        return d
    hijos = [gen(prof - 1, p_malo, p_raro) for _ in range(n)]
    if r < 0.80:
        fondo.append(hijos)
        if rng.random() < 0.03 and hijos:
            hijos.append(hijos if rng.random() < 0.5 else rng.choice(fondo))   # ciclo o compartida
        return hijos
    if r < 0.92:
        return tuple(hijos)
    try:
        return (set if rng.random() < 0.5 else frozenset)(hijos)
    except TypeError:
        return hijos


antes = dict(cuenta)
t0 = time.time()
for i in range(N):
    if i % 50 == 0:
        fondo.clear()
    v = gen(rng.randint(1, 7), rng.choice([0.0, 0.02, 0.05, 0.15]), rng.choice([0.0, 0.0, 0.03, 0.2]))
    compara(f"azar {i}: {type(v).__name__}", v)
print(f"  al azar en {time.time() - t0:.1f} s:", {k: cuenta[k] - antes[k] for k in cuenta})
print("  dirigidos:", dirigidos)

if "sin_tiempos" in sys.argv:
    print(f"\nFALLOS: {fallos}  ·  {cuenta}")
    sys.exit(0)
print("== tiempos (s) ==")


def t(nombre, v, con_viejo=True):
    t1 = time.time()
    b = corre(nuevo, v, 120)
    tn = time.time() - t1
    tv = None
    if con_viejo:
        t1 = time.time()
        corre(viejo, v, 120)
        tv = time.time() - t1
    print(f"  {nombre:62s} ahora {tn:7.2f}  antes {'—' if tv is None else format(tv, '7.2f')}  ({b})")
    return tn


t("lista de 200 000 dict pequeños", [{"a": i, "b": "texto"} for i in range(200000)])
t("lista de 200 000 dict de 10 campos", [{f"k{j}": "valor de texto corriente" for j in range(10)} for i in range(200000)])
t("lista de 200 000 veces el MISMO dict", [{"a": 1, "b": "texto"}] * 200000)
t("dict > lista de 200 000 dict", {"a": [{"a": i, "b": "texto"} for i in range(200000)]})
x: dict = {"t": "x" * 2500}
for _ in range(400):
    x = {"a": x, "t": "x" * 2500}
t("400 niveles de dict con 1 MB", x, con_viejo=False)
t("lista > 400 niveles de dict con 1 MB", [x], con_viejo=False)
y: list = [{"t": "x" * 2500}]
for _ in range(400):
    y = [y, {"t": "x" * 2500}]
t("400 niveles de lista, un dict de 2,5 kB en cada uno (1 MB)", y)
z: dict = {"t": "x" * 2500}
for _ in range(400):
    z = {"a": [z], "t": "x" * 2500}
t("400 niveles dict > lista > dict con 1 MB", z, con_viejo=False)
w: list = ["x" * 1000]
for _ in range(100000):
    w = [w]
t("lista de 100 000 niveles", w, con_viejo=False)
t("un texto de 16 MB en lista > dict", [{"a": "palabra " * 2_000_000}])
print(f"\nFALLOS: {fallos}  ·  {cuenta}")
