"""QA r01 de T-106 · Ataques de datos a las 21 fichas V5.0 (fuzzer determinista sobre los casos de control).

Para cada ficha y cada caso de control, se toman sus datos en línea y se muta una hoja (o una lista) cada vez:
None, texto, lista y dict vacíos, NaN, ±inf, 0, −1, 1e300, True, tipo cambiado; y en las listas: vaciar, dejar un
elemento, invertir el orden (fechas desordenadas), duplicar el primer elemento. También se atacan los parámetros.
Se clasifica cada llamada:
  - `ErrorFicha` → correcto (falla cerrado);
  - otra excepción → HALLAZGO (el Motor solo traduce ErrorFicha / NotImplementedError: lo demás le sube al ciclo);
  - resultado con NaN/inf en algún número → HALLAZGO candidato (cifra no finita servida como si fuera válida);
  - más de 5 s → HALLAZGO (rendimiento).
Además: determinismo (dos llamadas idénticas) y tiempo de cada caso nominal.

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r01_01_ataques_datos.py [RAIZ] [--max N]
"""
from __future__ import annotations

import copy
import json
import math
import random
import signal
import sys
import time
import warnings
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
MAX = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 250
M = C.preparar(args[0] if args else None)
S, ErrorFicha = M["servicio"], M["ErrorFicha"]
warnings.simplefilter("ignore")

RAROS = [None, "x", [], {}, float("nan"), float("inf"), float("-inf"), 0, -1, 1e300, True, -1e-300, [1, 2], {"a": 1}]


def hojas(x, ruta=()):
    """Rutas a mutar: hojas y listas (en listas largas, solo los elementos 0, medio y último)."""
    if isinstance(x, dict):
        for k in sorted(x, key=str):
            yield ruta + (k,)
            yield from hojas(x[k], ruta + (k,))
    elif isinstance(x, list):
        idx = range(len(x)) if len(x) <= 3 else sorted({0, len(x) // 2, len(x) - 1})
        for i in idx:
            yield ruta + (i,)
            yield from hojas(x[i], ruta + (i,))


def leer(x, ruta):
    for r in ruta:
        x = x[r]
    return x


def poner(x, ruta, valor):
    y = copy.deepcopy(x)
    leer(y, ruta[:-1])[ruta[-1]] = valor
    return y


def no_finitos(x, ruta="r"):
    out = []
    if isinstance(x, dict):
        for k, v in x.items():
            out += no_finitos(v, f"{ruta}.{k}")
    elif isinstance(x, (list, tuple)):
        for i, v in enumerate(x):
            out += no_finitos(v, f"{ruta}[{i}]")
    elif isinstance(x, (float, int)) and not isinstance(x, bool):
        try:
            if not math.isfinite(float(x)):
                out.append(ruta)
        except OverflowError:
            out.append(ruta)
    elif hasattr(x, "dtype"):
        try:
            if not all(math.isfinite(float(v)) for v in getattr(x, "ravel", lambda: [x])()):
                out.append(ruta)
        except (TypeError, ValueError):
            pass
    return out


class Tiempo(Exception):
    pass


def _alarma(*_):
    raise Tiempo()


signal.signal(signal.SIGALRM, _alarma)


def llamar(fn, ent, params, segundos=5):
    signal.alarm(segundos)
    t0 = time.perf_counter()
    try:
        r, lim = fn(ent, params)
        return "ok", (r, lim), time.perf_counter() - t0
    except ErrorFicha as e:
        return "ErrorFicha", str(e), time.perf_counter() - t0
    except NotImplementedError as e:
        return "NotImplementedError", str(e), time.perf_counter() - t0
    except Tiempo:
        return "TIEMPO", f"> {segundos} s", segundos
    except Exception as e:  # noqa: BLE001
        return "EXCEPCION", f"{type(e).__name__}: {str(e)[:120]}", time.perf_counter() - t0
    finally:
        signal.alarm(0)


rnd = random.Random(20261112)
excepciones: dict[str, list[str]] = defaultdict(list)
no_fin: dict[str, list[str]] = defaultdict(list)
lentos: dict[str, list[str]] = defaultdict(list)
cuenta: Counter = Counter()
tiempos: dict[str, float] = {}
for ficha in sorted(S.CASOS_CONTROL):
    fn = S.IMPLEMENTADAS[ficha]["fn"]
    for ci, caso in enumerate(S.CASOS_CONTROL[ficha]):
        ent0 = C.entrada(caso)
        p0 = dict(caso.get("parametros") or {})
        # nominal: determinismo y tiempo
        e1, r1, t1 = llamar(fn, copy.deepcopy(ent0), dict(p0), 30)
        e2, r2, _ = llamar(fn, copy.deepcopy(ent0), dict(p0), 30)
        tiempos[f"{ficha}#{ci}"] = t1
        det = e1 == e2 == "ok" and json.dumps(S._limpio(r1[0]), sort_keys=True, default=str) == \
            json.dumps(S._limpio(r2[0]), sort_keys=True, default=str)
        C.informe(f"{ficha}#{ci} nominal determinista ({t1:.2f} s)", det, "" if det else f"{e1}/{e2}")
        mutaciones = []
        for ruta in hojas(ent0["valores"]):
            actual = leer(ent0["valores"], ruta)
            for raro in RAROS:
                mutaciones.append((ruta, raro))
            if isinstance(actual, list) and actual:
                mutaciones += [(ruta, []), (ruta, actual[:1]), (ruta, list(reversed(actual))),
                               (ruta, [actual[0]] + actual)]
            if isinstance(actual, (int, float)) and not isinstance(actual, bool):
                mutaciones += [(ruta, -actual), (ruta, actual * 1e6), (ruta, str(actual))]
        for k in sorted(set(S.IMPLEMENTADAS[ficha].get("parametros", {})) | set(p0)):
            for raro in RAROS:
                mutaciones.append((("__param__", k), raro))
        rnd.shuffle(mutaciones)
        for ruta, raro in mutaciones[:MAX]:
            if ruta[0] == "__param__":
                ent, params = copy.deepcopy(ent0), {**p0, ruta[1]: raro}
            else:
                ent, params = {**ent0, "valores": poner(ent0["valores"], ruta, raro)}, dict(p0)
            est, info, t = llamar(fn, ent, params)
            cuenta[est] += 1
            desc = f"{'.'.join(map(str, ruta))} = {str(raro)[:40]!s}"
            if est == "EXCEPCION":
                excepciones[ficha].append(f"{desc} → {info}")
            elif est == "TIEMPO" or t > 5:
                lentos[ficha].append(f"{desc} → {t:.1f} s")
            elif est == "ok":
                nf = no_finitos(info[0])
                if nf:
                    no_fin[ficha].append(f"{desc} → {nf[:3]}")

print("\nResultado de las mutaciones:", dict(cuenta))
for titulo, d in (("EXCEPCIONES que no son ErrorFicha", excepciones), ("Resultados con números no finitos", no_fin),
                  ("Llamadas lentas", lentos)):
    print(f"\n== {titulo}")
    for ficha in sorted(d):
        unicos = sorted(set(x.split(" → ")[1] for x in d[ficha]))
        print(f"  {ficha}: {len(d[ficha])} casos; tipos: {unicos[:6]}")
        for x in d[ficha][:4]:
            print(f"     · {x}")
for ficha in sorted(S.CASOS_CONTROL):
    C.informe(f"{ficha}: sin excepciones ajenas a ErrorFicha", not excepciones.get(ficha), f"{len(excepciones.get(ficha, []))}")
    C.informe(f"{ficha}: sin números no finitos en resultados servidos", not no_fin.get(ficha), f"{len(no_fin.get(ficha, []))}")
    C.informe(f"{ficha}: sin llamadas > 5 s", not lentos.get(ficha), f"{len(lentos.get(ficha, []))}")
print("\nTiempo nominal máximo por caso:", max(tiempos.items(), key=lambda x: x[1]))
sys.exit(C.resumen())
