"""QA r01 de T-119 · entradas hostiles por `Motor.servir` en las 10 fichas P2.

 1. Cada hoja de `valores` (anidada; primer y último elemento de cada lista) de dos casos de control por ficha, sustituida
    por cada valor hostil, y también quitada. 2. Cada parámetro declarado, con cada valor hostil. 3. Campos de la petición
    con tipos raros. 4. Parámetros no declarados, umbrales de UMBRALES en la petición y `semilla`.
 Se exige: ninguna excepción escapa, una entrada en RC por llamada, nada no finito servido, ninguna llamada > 30 s.
 Se listan (para revisar a mano) los casos en que un tipo no numérico se sirve donde había un número.
Uso: r01_04_hostiles.py [ejecutor] [--ficha F]
"""
import copy
import decimal
import fractions
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import numpy as np  # noqa: E402
from bloque_a.motor import fichas_p2, servicio  # noqa: E402

K = C.Contador("r01_04 hostiles")
honda = []
for _ in range(3000):
    honda = [honda]
HOSTILES = [float("nan"), float("inf"), float("-inf"), -0.0, 0, -1, 1e308, -1e308, 1e-320, 1e101, 10 ** 400, 2 ** 63, "1.5", "abc", "",
            None, True, False, [], {}, [1.0], {"a": 1}, (1.0, 2.0), np.float64("nan"), np.float64("inf"), np.int64(3), np.float32(1.5),
            np.array([1.0, 2.0]), np.bool_(True), decimal.Decimal("1.5"), fractions.Fraction(1, 3), 1 + 2j, b"1.5", honda,
            "9999-12-31", "1600-01-01", "2026-13-45", 20261114]
NO_NUM = (str, bool, type(None), list, dict, tuple, bytes, complex, decimal.Decimal, fractions.Fraction, np.ndarray, np.bool_)


def hojas(x, ruta=()):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from hojas(v, ruta + (k,))
    elif isinstance(x, list):
        if x:
            yield from hojas(x[0], ruta + (0,))
            if len(x) > 1:
                yield from hojas(x[-1], ruta + (len(x) - 1,))
            if len(x) > 2:
                yield from hojas(x[len(x) // 2], ruta + (len(x) // 2,))
    else:
        yield ruta


def poner(x, ruta, valor, quitar=False):
    for k in ruta[:-1]:
        x = x[k]
    if quitar:
        if isinstance(x, dict):
            del x[ruta[-1]]
        else:
            x.pop(ruta[-1])
    else:
        x[ruta[-1]] = valor


def no_finito(x):
    if isinstance(x, dict):
        return any(no_finito(v) for v in x.values())
    if isinstance(x, (list, tuple)):
        return any(no_finito(v) for v in x)
    return isinstance(x, (float, np.floating)) and not math.isfinite(float(x))


class Estado:
    def __init__(self):
        self.m, self.n, self.total, self.escapes, self.rc, self.nofin, self.lentas, self.raros, self.max_t = C.motor(), 0, 0, [], [], [], [], [], 0.0
        self.servidas = 0

    def llamar(self, pet, etiqueta, original=None, valor=None, sol="AG-21"):
        if self.n >= 40:
            self.m, self.n = C.motor(), 0
        self.n += 1
        self.total += 1
        t0 = time.time()
        r, exc, nrc = C.llamar(self.m, pet, sol)
        dt = time.time() - t0
        self.max_t = max(self.max_t, dt)
        if dt > 30:
            self.lentas.append((etiqueta, round(dt, 1)))
        if exc:
            self.escapes.append((etiqueta, exc))
            return None
        if nrc != 1:
            self.rc.append((etiqueta, nrc))
        if r["estado"] != "RECHAZADO":
            self.servidas += 1
            if no_finito(r.get("resultado")):
                self.nofin.append(etiqueta)
            if isinstance(original, (int, float)) and not isinstance(original, bool) and isinstance(valor, NO_NUM):
                self.raros.append(etiqueta)
        return r


S = Estado()
solo = sys.argv[sys.argv.index("--ficha") + 1] if "--ficha" in sys.argv else None
for f in C.P2:
    if solo and f != solo:
        continue
    t_f, n0 = time.time(), S.total
    casos = servicio.CASOS_CONTROL[f]
    for i in sorted({0, len(casos) - 1, 1}):
        v0, p0 = C.caso(f, i)
        for ruta in hojas(v0):
            orig = v0
            for k in ruta:
                orig = orig[k]
            for j, h in enumerate(HOSTILES):
                v = copy.deepcopy(v0)
                poner(v, ruta, h)
                S.llamar({"operacion": f, "datos": [{"valores": v}], "parametros": dict(p0), "fecha_corte": None},
                         (f, i, "valores", ruta, repr(h)[:24]), orig, h)
            v = copy.deepcopy(v0)
            poner(v, ruta, None, quitar=True)
            S.llamar({"operacion": f, "datos": [{"valores": v}], "parametros": dict(p0), "fecha_corte": None}, (f, i, "quitar", ruta, ""))
        # listas enteras sustituidas
        for k, val in v0.items():
            if isinstance(val, (list, dict)):
                for h in HOSTILES:
                    v = copy.deepcopy(v0)
                    v[k] = h
                    S.llamar({"operacion": f, "datos": [{"valores": v}], "parametros": dict(p0), "fecha_corte": None},
                             (f, i, "bloque", k, repr(h)[:24]))
    v0, p0 = C.caso(f, 0)
    for k, d in fichas_p2.PARAMETROS_POR_DEFECTO[f].items():
        for h in HOSTILES:
            S.llamar({"operacion": f, "datos": [{"valores": copy.deepcopy(v0)}], "parametros": {**p0, k: h}, "fecha_corte": None},
                     (f, "param", k, repr(h)[:24]), d if not isinstance(d, (list, str)) else None, h)
            if isinstance(d, list):
                S.llamar({"operacion": f, "datos": [{"valores": copy.deepcopy(v0)}], "parametros": {**p0, k: [h]}, "fecha_corte": None},
                         (f, "param[lista]", k, repr(h)[:24]), d[0], h)
                S.llamar({"operacion": f, "datos": [{"valores": copy.deepcopy(v0)}], "parametros": {**p0, k: [d[0], h]}, "fecha_corte": None},
                         (f, "param[lista+]", k, repr(h)[:24]), d[0], h)
    # campos de la petición
    for campo in ("operacion", "datos", "parametros", "fecha_corte", "plan", "perfil", "clase", "semilla", "horizonte", "modo", "prioridad"):
        for h in HOSTILES:
            pet = {"operacion": f, "datos": [{"valores": copy.deepcopy(v0)}], "parametros": dict(p0), "fecha_corte": None}
            pet[campo] = h
            S.llamar(pet, (f, "petición", campo, repr(h)[:24]))
    for h in HOSTILES:
        S.llamar({"operacion": f, "datos": [{"valores": copy.deepcopy(v0)}], "parametros": dict(p0), "fecha_corte": None},
                 (f, "solicitante", repr(h)[:24]), sol=h)
        S.llamar({"operacion": f, "datos": [{"valores": copy.deepcopy(v0)}, h], "parametros": dict(p0)}, (f, "datos[1]", repr(h)[:24]))
        S.llamar({"operacion": f, "datos": [{"valores": copy.deepcopy(v0), "serie": h}], "parametros": dict(p0)}, (f, "datos.serie", repr(h)[:24]))
    print(f"{f}: {S.total - n0} llamadas en {time.time() - t_f:.0f} s", flush=True)

print(f"total {S.total} llamadas; servidas {S.servidas}; la más lenta {S.max_t:.1f} s")
K.comprobar("ninguna excepción escapa de Motor.servir", not S.escapes, f"{len(S.escapes)}: {S.escapes[:8]}")
K.comprobar("una entrada en RC por llamada", not S.rc, f"{len(S.rc)}: {S.rc[:8]}")
K.comprobar("nada no finito servido", not S.nofin, f"{len(S.nofin)}: {S.nofin[:8]}")
K.comprobar("ninguna llamada > 30 s", not S.lentas, str(S.lentas[:8]))
print(f"tipo no numérico servido donde había un número: {len(S.raros)}")
for x in S.raros[:80]:
    print("   ", x)

print("4. parámetros no declarados, umbrales y semilla")
mal = []
m = C.motor()
for f in C.P2:
    if solo and f != solo:
        continue
    v0, p0 = C.caso(f, 0)
    extras = [("no_declarado", 1), ("Metodo", "x"), ("semilla", 7), (" metodo", "x"), ("", 1)]
    extras += [(k, val) for k, val in fichas_p2.UMBRALES[f].items()]
    extras += [(k, val) for g in fichas_p2.UMBRALES for k, val in fichas_p2.UMBRALES[g].items() if k not in fichas_p2.UMBRALES[f]][:10]
    for k, val in extras:
        val = list(val) if isinstance(val, tuple) else val
        r, exc, nrc = C.llamar(m, {"operacion": f, "datos": [{"valores": copy.deepcopy(v0)}], "parametros": {**p0, k: val}, "fecha_corte": None})
        if exc or nrc != 1 or r["estado"] != "RECHAZADO":
            mal.append((f, k, exc or r["estado"]))
    # semilla en la petición (no en parámetros): la ficha no usa azar
    r, exc, nrc = C.llamar(m, {"operacion": f, "datos": [{"valores": copy.deepcopy(v0)}], "parametros": dict(p0), "semilla": 7})
    print(f"   {f}: `semilla` en la raíz de la petición → {exc or r['estado']}; semilla en RC: {m.almacen.estado('RC')[r['calc_id']].get('semilla') if not exc else None}")
    # umbral en `valores` o en la raíz: no debe cambiar el resultado
    base = C.servir(C.motor(), f, v0, p0)["resultado"]
    for k, val in list(fichas_p2.UMBRALES[f].items())[:6]:
        val = 1 if not isinstance(val, (int, float)) else val * 3 + 1
        r1 = C.servir(C.motor(), f, {**copy.deepcopy(v0), k: val}, p0)
        r2, exc, _ = C.llamar(C.motor(), {"operacion": f, "datos": [{"valores": copy.deepcopy(v0)}], "parametros": dict(p0), k: val})
        if (r1["estado"] != "RECHAZADO" and r1["resultado"] != base) or exc or (r2["estado"] != "RECHAZADO" and r2["resultado"] != base):
            mal.append((f, "umbral fuera de parametros", k))
K.comprobar("parámetro no declarado, umbral o `semilla` en parametros ⇒ RECHAZADO; umbral en valores o raíz no cambia nada", not mal, str(mal[:10]))
sys.exit(K.fin())
