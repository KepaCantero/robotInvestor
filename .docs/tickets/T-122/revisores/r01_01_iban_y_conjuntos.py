"""QA r01 de T-122 · patrón nuevo del IBAN español y `contenido_sensible` con conjuntos.

 1. IBAN «ES»/«es» + 22 cifras: formas que deben detectarse (impreso, espacio duro y estrecho, dos separadores, minúsculas,
    JSON escapado) y textos corrientes que no (series de cifras que empiezan por «ES»/«es», ISIN, separadores raros, tres
    separadores, 21 y 23 cifras, palabras que acaban en «es»). Coste con textos grandes.
 2. `contenido_sensible`: diferencial frente a la versión anterior a T-122 (b9abb29, extraída con git y ejecutada con el
    `secretos_en_texto` actual): estructuras al azar con listas, tuplas, conjuntos, frozensets, diccionarios con hash dentro
    de conjuntos, ciclos y anidamiento profundo. Nada que antes diera True da False; ninguna excepción nueva; termina.
Uso (desde bloque_a/11_Ejecutor de la copia): ../../.venv/bin/python ../../.docs/tickets/T-122/revisores/r01_01_iban_y_conjuntos.py
Las claves e IBAN de ejemplo van partidos.
"""
import json
import random
import re
import subprocess
import sys
import time

sys.path.insert(0, ".")
from bloque_a import llm  # noqa: E402
from bloque_a.contratos import RE_ESCAPES, RE_SECRETO, secretos_en_texto  # noqa: E402

fallos = []


def ok(nombre, cond, detalle=""):
    print(f"  {'ok   ' if cond else 'FALLA'} {nombre} {'' if cond else detalle}")
    if not cond:
        fallos.append(nombre)


def es_iban_es(t):   # solo el patrón de T-122 (RE_SECRETO, sobre el texto y sobre el texto sin escapes, como hace
    # `secretos_en_texto`), sin el validador de T-123
    return any(m.group(0)[:2].upper() == "ES" for u in (t, RE_ESCAPES.sub(" ", t)) for m in RE_SECRETO.finditer(u))


ES = "ES91" + "21000418450200051332"
print("[1] patrón del IBAN español (RE_SECRETO)")
positivos = {"junto": ES, "grupos": " ".join(ES[i:i + 4] for i in range(0, 24, 4)), "impreso": f"{ES[:4]} {ES[4:8]} {ES[8:12]} {ES[12:14]} {ES[14:]}",
             "espacio duro": " ".join(ES[i:i + 4] for i in range(0, 24, 4)), "estrecho": " ".join(ES[i:i + 4] for i in range(0, 24, 4)),
             "dos espacios": "  ".join(ES[i:i + 4] for i in range(0, 24, 4)), "minúsculas": ES.lower(), "guion y punto": "-.".join(ES[i:i + 4] for i in range(0, 24, 4)),
             "JSON escapado (\\u00a0)": json.dumps({"c": " ".join(ES[i:i + 4] for i in range(0, 24, 4))}),
             "JSON con \\n": json.dumps({"c": "\n".join(ES[i:i + 4] for i in range(0, 24, 4))}), "tab": "\t".join(ES[i:i + 4] for i in range(0, 24, 4)),
             "Es mixto": "Es" + ES[2:], "seguido de cifra tras espacio": " ".join(ES[i:i + 4] for i in range(0, 24, 4)) + " 15 de noviembre"}
for n, t in positivos.items():
    ok(f"se detecta: {n}", es_iban_es(f"pago a {t}."), t)
rng = random.Random(122)
negativos = {
    "tres espacios entre grupos (fuera de lo declarado)": "   ".join(ES[i:i + 4] for i in range(0, 24, 4)),
    "21 cifras": "ES91" + "2100041845020005133", "palabra «Res» + 22 cifras": "Res" + "91" + "21000418450200051332",
    "«mes» + cifras": "mes12 3456 7890 1234 5678 9012 34", "ISIN ES": "ES0113900J37 ES0144580Y14 ES0178430E18",
    "barra": "ES91/2100/0418/4502/0005/1332", "coma": "ES91,2100,0418,4502,0005,1332", "ES con espacio y cifras": "ES 9121 0004 1845 0200 0513 32",
    "decimales tras ES": "ES1.2 3.4 5.6 7.8 9.0 1.2 3.4 5.6 7.8 9.0 1.2", "ES-año": "ES-2024-01-05 2024-03-29",
}
for n, t in negativos.items():
    print(f"    {n:52s} → {'MARCADO' if es_iban_es(t) else 'no'}")
# textos corrientes al azar con «es»/«ES» y cifras
corriente = 0
plantillas = ["el valor es {} y sube", "ES {} EUR", "es: {}", "ES{}", "la serie es{}", "país ES; cuenta {}", "es {}"]
for _ in range(20000):
    cif = " ".join(str(rng.randint(0, 9999)) for _ in range(rng.randint(3, 8)))
    t = rng.choice(plantillas).format(cif)
    corriente += es_iban_es(t)
print(f"    textos corrientes con «es»/«ES» y series de cifras al azar marcados: {corriente} de 20 000 (solo cuenta «ES»+cifras pegadas)")
pegados = sum(es_iban_es("ES" + "".join(str(rng.randint(0, 9)) for _ in range(rng.choice([21, 22, 23])))) for _ in range(3000))
print(f"    «ES» + 21/22/23 cifras pegadas al azar marcados: {pegados} de 3000 (≈ un tercio son de 22: el patrón no lleva control)")
for nombre, unidad in (("ES y cifras", "ES12 3456 7890 "), ("es y espacios duros", "es12 3 4 "), ("cifras y dos separadores", "1 .2 -3 .")):
    ts = []
    for n in (100_000, 400_000):
        t = (unidad * (n // len(unidad) + 1))[:n]
        t0 = time.perf_counter()
        secretos_en_texto(t)
        ts.append(time.perf_counter() - t0)
    ok(f"coste lineal ({nombre}): 100 k {ts[0]:.3f} s, 400 k {ts[1]:.3f} s", ts[1] / max(ts[0], 1e-9) < 8 and ts[1] < 10)

print("\n[2] contenido_sensible: diferencial frente a b9abb29")
fuente = subprocess.run(["git", "show", "b9abb29:bloque_a/11_Ejecutor/bloque_a/llm.py"], capture_output=True, text=True, check=True).stdout
ns = {"json": json, "secretos_en_texto": secretos_en_texto}
for nombre in ("contenido_sensible", "_diccionarios_de_arriba"):
    exec(re.search(rf"^def {nombre}\(valor\).*?(?=^\S)", fuente, re.S | re.M).group(0), ns)  # noqa: S102 — versión anterior del repo
viejo, nuevo = ns["contenido_sensible"], llm.contenido_sensible
CLAVE, SK = "api" + "_key", "sk-" + "ant-api03-abcdefghijklmnopqrstuvwxyz0123"


class DH(dict):
    def __hash__(self):
        return id(self)


def hoja(r):
    x = r.random()
    if x < 0.08:
        return SK
    if x < 0.14:
        return "pago " + ES
    if x < 0.2:
        return "tarjeta " + "4111" + " 1111 1111 1111"
    return r.choice(["hola", "1.5", "", "ES", "x" * 30, "0.4228715933084759"])


def estructura(r, prof=0):
    if prof > r.randint(2, 7):
        return hoja(r)
    t = r.random()
    hijos = [estructura(r, prof + 1) for _ in range(r.randint(0, 4))]
    if t < 0.2:
        return hijos
    if t < 0.35:
        return tuple(hijos)
    if t < 0.5:
        return frozenset(h for h in hijos if _hashable(h))
    if t < 0.6:
        return set(h for h in hijos if _hashable(h))
    if t < 0.75:
        d = DH()
        for h in hijos:
            d[r.choice([CLAVE, "nota", "v", "password"])] = h
        return d
    d = {}
    for h in hijos:
        d[r.choice([CLAVE, "nota", "v", "password", "texto"])] = h
    return d


def _hashable(x):
    try:
        hash(x)
        return True
    except TypeError:
        return False


def evalua(f, v):
    t0 = time.perf_counter()
    try:
        out = f(v)
    except Exception as e:  # noqa: BLE001
        out = type(e).__name__
    return out, time.perf_counter() - t0


reg, exc_nuevas, mas_det, tmax, con_conj = [], [], 0, 0.0, 0
r = random.Random(1122)
for i in range(6000):
    v = estructura(r)
    if r.random() < 0.05 and isinstance(v, (list, dict)):   # ciclo
        (v.append(v) if isinstance(v, list) else v.__setitem__("yo", v))
    a, _ = evalua(viejo, v)
    b, t = evalua(nuevo, v)
    tmax = max(tmax, t)
    con_conj += "set" in repr(type(v)) or "frozenset" in str(v)[:0]
    if a is True and b is not True:
        reg.append((i, a, b))
    if isinstance(b, str) and not isinstance(a, str):
        exc_nuevas.append((i, a, b))
    if b is True and a is not True:
        mas_det += 1
print(f"    6 000 estructuras: True→no True {len(reg)} · excepciones nuevas {len(exc_nuevas)} · detecta de más {mas_det} · tiempo máximo {tmax:.3f} s")
ok("ninguna regresión (True → False o excepción)", not reg, str(reg[:5]))
ok("ninguna excepción nueva", not exc_nuevas, str(exc_nuevas[:5]))
# conjunto grande y profundo
grande = {"a": frozenset(DH(v=frozenset((f"t{i}",))) for i in range(20000))}
_, t = evalua(nuevo, grande)
ok(f"conjunto de 20 000 diccionarios con hash: {t:.2f} s (< 10)", t < 10)
prof = "x"
for _ in range(3000):
    prof = frozenset([prof])
b, t = evalua(nuevo, {"a": prof})
a, _ = evalua(viejo, {"a": prof})
print(f"    frozenset anidado 3000 niveles: antes {a} · ahora {b} · {t:.2f} s")
ok("frozenset anidado 3000 niveles: termina y no da False si antes daba True", not (a is True and b is not True) and t < 10)
d = DH(nota="x")
d[CLAVE] = "abcdefghijklmnop"
caso = {"cfg": {frozenset([("k", 1)]), (1, 2)}, "lista": [{"s": {d}}]}
print(f"    dict > lista > dict > set > DH con «{CLAVE}»: antes {evalua(viejo, caso)[0]} · ahora {evalua(nuevo, caso)[0]}")
print(f"\nFALLOS: {len(fallos)} {fallos}")
