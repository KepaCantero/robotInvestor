"""QA r01 de T-72 (V0.69): el Reloj nuevo, con tolerancias sanas, se comporta EXACTAMENTE como el de HEAD (V0.68).

Carga los dos `reloj.py` (el del árbol y el de una copia de HEAD) y los ejecuta en paralelo con las mismas fuentes simuladas:
1. bordes exactos de cada tolerancia (salto, deriva desde el ancla, suelo, desfase con la referencia, contraste, estado);
2. 4000 secuencias aleatorias (semilla fija) de lecturas, contrastes, comprobar_estado y rearmes con tolerancias válidas.
Compara cada resultado y el estado interno (salvo `_tol` frente a los tres atributos de antes).

Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.69/qa/r01_01_reloj_diferencial.py <marco_de_HEAD>
"""
import importlib.util
import os
import random
import sys
from datetime import datetime, timezone

AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
HEAD = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(AQUI, "validador"))


def cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


NUEVO = cargar("reloj_nuevo", os.path.join(AQUI, "validador", "reloj.py"))
VIEJO = cargar("reloj_viejo", os.path.join(HEAD, "validador", "reloj.py"))
BASE = datetime(2026, 11, 6, 9, 0, 0, tzinfo=timezone.utc).timestamp()


def iso(s):
    return datetime.fromtimestamp(s, timezone.utc).isoformat()


class F:
    def __init__(self, p=BASE, m=1000.0):
        self.p, self.m = p, m

    def pared(self):
        return self.p

    def mono(self):
        return self.m


class Est:
    def __init__(self, u):
        self.ultimo_ahora = u


def interno(r):
    d = {k: v for k, v in vars(r).items() if k not in ("_pared", "_monotono", "_tol", "max_salto_s", "max_desfase_s", "max_sin_contraste_s")}
    d["tol"] = (r.max_salto_s, r.max_desfase_s, r.max_sin_contraste_s)
    return repr(d)


fallos, casos = [], 0


def par(kw):
    f = F()
    return f, NUEVO.Reloj(f.pared, f.mono, **kw), VIEJO.Reloj(f.pared, f.mono, **kw)


def igual(etq, a, b, rn, rv):
    global casos
    casos += 1
    if repr(a) != repr(b) or interno(rn) != interno(rv) or repr(rn.estado()) != repr(rv.estado()):
        fallos.append((etq, a, b))


def paso(f, rn, rv, op, etq):
    if op[0] == "pasa":
        f.m += op[1]
        f.p += op[2]
        return
    if op[0] == "ahora":
        igual(etq, rn.ahora(), rv.ahora(), rn, rv)
    elif op[0] == "contrastar":
        igual(etq, rn.contrastar(iso(f.p + op[1]), "REF"), rv.contrastar(iso(f.p + op[1]), "REF"), rn, rv)
    elif op[0] == "estado":
        igual(etq, rn.comprobar_estado(Est(iso(f.p + op[1]))), rv.comprobar_estado(Est(iso(f.p + op[1]))), rn, rv)
    elif op[0] == "rearmar":
        m = "Revisado: alguien cambió la hora de la máquina por error"
        igual(etq, rn.rearmar("OPERADOR", m), rv.rearmar("OPERADOR", m), rn, rv)


# 1. bordes exactos (valores binarios exactos: 2.0, 5.0, 0.25…) y una milésima a cada lado
for s, d, c in ((2.0, 5.0, 86400.0), (0.5, 0.25, 3600.0), (60.0, 300.0, 1.0)):
    kw = {"max_salto_s": s, "max_desfase_s": d, "max_sin_contraste_s": c}
    for eps in (-0.001, 0.0, 0.001, -2 ** -20, 2 ** -20):
        guion = [
            [("contrastar", 0.0), ("pasa", 1.0, 1.0 + s + eps), ("ahora",)],                       # salto en el borde
            [("contrastar", 0.0), ("pasa", 1.0, 1.0 - s - eps), ("ahora",)],                       # salto hacia atrás en el borde
            [("contrastar", -(d + eps)), ("ahora",)],                                               # desfase en el borde
            [("contrastar", d + eps), ("ahora",)],
            [("contrastar", 0.0), ("pasa", c + eps, c + eps), ("ahora",)],                          # contraste en el borde
            [("contrastar", 0.0), ("estado", d + eps), ("ahora",)],                                 # estado adelantado en el borde
            [("contrastar", 0.0), ("estado", d - 0.5), ("pasa", 0.0, -(s - 0.0)), ("ahora",)],
            [("contrastar", -d), ("pasa", 1.0, 1.0 - s - eps), ("ahora",), ("pasa", 1.0, 1.0), ("ahora",)],   # suelo en el borde
        ]
        # deriva desde el ancla: muchos saltos pequeños por debajo de s que suman s + tasa·t (+eps)
        t = 100.0
        lim = s + NUEVO.TASA_MAX * t
        g = [("contrastar", 0.0)]
        for _ in range(4):
            g += [("pasa", t / 4, t / 4 + (lim + eps) / 4), ("ahora",)]
        guion.append(g)
        for i, gu in enumerate(guion):
            f, rn, rv = par(kw)
            for j, op in enumerate(gu):
                paso(f, rn, rv, op, f"borde {kw} eps={eps} guion={i} paso={j}")

# 2. secuencias aleatorias
rng = random.Random(20261110)
for k in range(4000):
    kw = {"max_salto_s": rng.choice([0.5, 1.0, 2.0, rng.uniform(0.01, 60.0)]),
          "max_desfase_s": rng.choice([0.25, 5.0, rng.uniform(0.01, 300.0)]),
          "max_sin_contraste_s": rng.choice([1.0, 60.0, 3600.0, rng.uniform(0.5, 1e5)])}
    f, rn, rv = par(kw)
    s, d, c = kw["max_salto_s"], kw["max_desfase_s"], kw["max_sin_contraste_s"]
    for j in range(rng.randint(1, 25)):
        x = rng.random()
        if x < 0.35:
            dm = rng.choice([0.0, rng.uniform(0, 5), rng.uniform(0, c * 1.5), c])
            dp = dm + rng.choice([0.0, s, -s, rng.uniform(-2 * s, 2 * s), rng.uniform(-s / 10, s / 10)])
            op = ("pasa", dm, dp)
        elif x < 0.65:
            op = ("ahora",)
        elif x < 0.82:
            op = ("contrastar", rng.choice([0.0, d, -d, rng.uniform(-2 * d, 2 * d)]))
        elif x < 0.93:
            op = ("estado", rng.choice([0.0, d, -d, rng.uniform(-2 * d, 2 * d), -3600.0]))
        else:
            op = ("rearmar",)
        paso(f, rn, rv, op, f"aleatorio {k} paso {j} {kw} {op}")

print(f"{casos} comparaciones, {len(fallos)} diferencias")
for x in fallos[:10]:
    print("DIFERENCIA", x)
print("RESULTADO r01_01:", "SIN DIFERENCIAS" if not fallos else "HAY DIFERENCIAS")
sys.exit(1 if fallos else 0)
