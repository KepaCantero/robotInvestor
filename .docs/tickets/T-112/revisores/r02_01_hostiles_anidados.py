"""QA r02 de T-112 · entradas hostiles en profundidad por Motor.servir, en las 35 fichas de la Fase 2.

La r01 (r01_06) solo cambiaba las claves de primer nivel de `valores` y los parámetros. Aquí:
 1. cada hoja ANIDADA de `valores` (hasta 6 niveles; de cada lista, el primero y el último elemento) y cada parámetro,
    con valores hostiles nuevos: NaN, ±inf, -0.0, 1e-320, 10**400 (entero que no cabe en float), -10**400, 2**63, texto
    numérico, bytes, complex, Decimal, Fraction, tupla, lista vacía, objeto vacío, True, None, np.float64('nan'),
    np.int64, np.array, una lista anidada a 3 000 niveles;
 2. cada parámetro con tipos raros (los mismos);
 3. la petición entera con tipos raros en `datos`, `perfil`, `clase`, `plan`, `semilla`, `fecha_corte`.
Nada debe escapar como excepción, cada llamada deja exactamente una entrada en RC, nada servido lleva cifras no finitas y
ninguna llamada pasa de LIMITE segundos.
Uso: .venv/bin/python -I r02_01_hostiles_anidados.py [ejecutor] [--rapido]
"""
import copy
import decimal
import fractions
import math
import signal
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

RAPIDO = "--rapido" in sys.argv
C.preparar([a for a in sys.argv if not a.startswith("--")])
import numpy as np  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

K = C.Contador("r02_01 hostiles anidados")
m = C.motor()
LIMITE = 120
LENTAS = {"REG-HMM-001", "FIR-CURVE-001", "TEM-DIFF-001", "FX-REGIME-001", "BT-PBO-001", "ML-PRED-001", "SCN-H-001"}


def profunda(n=3000):
    x = []
    for _ in range(n):
        x = [x]
    return x


HOSTILES = [float("nan"), float("inf"), -0.0, 1e-320, 10 ** 400, -(10 ** 400), 2 ** 63, "1.5", b"1", 1 + 2j,
            decimal.Decimal("1.5"), fractions.Fraction(1, 3), (1, 2), [], {}, True, None, np.float64("nan"), np.int64(3),
            np.array([1.0, 2.0]), "PROFUNDA", "2026-11-13", -1, 0, 1e308]
HOSTILES_LENTAS = [float("nan"), 10 ** 400, "1.5", [], {}, True, None, "PROFUNDA", -1]


class Tiempo(Exception):
    pass


def _alarma(*_):
    raise Tiempo()


signal.signal(signal.SIGALRM, _alarma)


def llamar(pet, solicitante="AG-18", limite=LIMITE):
    antes = len(m.almacen.leer("RC"))
    signal.alarm(limite)
    t0 = time.time()
    try:
        r, exc = m.servir(pet, solicitante), None
    except Tiempo:
        r, exc = None, "TIEMPO"
    except BaseException as e:  # noqa: BLE001
        r, exc = None, f"{type(e).__name__}: {str(e)[:120]}"
    finally:
        signal.alarm(0)
    return r, exc, len(m.almacen.leer("RC")) - antes, time.time() - t0


def no_finito(x):
    if isinstance(x, dict):
        return any(no_finito(v) for v in x.values())
    if isinstance(x, (list, tuple)):
        return any(no_finito(v) for v in x)
    return isinstance(x, float) and not math.isfinite(x)


def base(f, i=0):
    c = servicio.CASOS_CONTROL[f][i]
    return {"operacion": f, "datos": copy.deepcopy(c.get("datos") or []), "parametros": dict(c.get("parametros") or {}),
            "fecha_corte": None}


def rutas(x, pref=(), nivel=0):
    """Rutas a las hojas (y a los contenedores) de un objeto; de cada lista, solo el primero y el último."""
    out = [pref] if pref else []
    if nivel >= 6:
        return out
    if isinstance(x, dict):
        for k in x:
            out += rutas(x[k], pref + (k,), nivel + 1)
    elif isinstance(x, list) and x:
        for i in sorted({0, len(x) - 1}):
            out += rutas(x[i], pref + (i,), nivel + 1)
    return out


def poner(obj, ruta, valor):
    for k in ruta[:-1]:
        obj = obj[k]
    obj[ruta[-1]] = valor


def era_numero(pet0, ruta):
    x = next(d for d in pet0["datos"] if "valores" in d)["valores"]
    for k in ruta:
        x = x[k]
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def aplanar(x):
    """Las series de numpy de los casos de control, a listas (para poder cambiar un elemento por cualquier tipo)."""
    if isinstance(x, dict):
        return {k: aplanar(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [aplanar(v) for v in x]
    if isinstance(x, np.ndarray):
        return [aplanar(v) for v in x.tolist()]
    if isinstance(x, np.generic):
        return x.item()
    return x


escapes, sin_rc, no_fin, lentas, n = [], [], [], [], 0
servidas_raras = []
t_ini = time.time()
fichas = sorted(servicio.FASE2)
for f in fichas:
    m = C.motor()   # un Registro de cálculos por ficha: `leer("RC")` relee el fichero entero en cada llamada
    pet0 = base(f)
    pet0["datos"] = aplanar(pet0["datos"])
    hostiles = HOSTILES_LENTAS if (f in LENTAS or RAPIDO) else HOSTILES
    bloque = next((d for d in pet0["datos"] if "valores" in d), None)
    rs = rutas(bloque["valores"]) if bloque else []
    if f in LENTAS or RAPIDO:
        rs = rs[:: max(1, len(rs) // 12)]
    mod = next(md for md in servicio.MODULOS_FASE2 if f in md.FICHAS)
    objetivos = [("valores", r) for r in rs] + [("parametros", (k,)) for k in sorted(mod.PARAMETROS_POR_DEFECTO[f])]
    ref, _, _, _ = llamar(copy.deepcopy(pet0))
    nf = 0
    for donde, ruta in objetivos:
        for h in hostiles:
            pet = copy.deepcopy(pet0)
            h = profunda() if isinstance(h, str) and h == "PROFUNDA" else h
            if donde == "parametros":
                pet["parametros"][ruta[0]] = h
            else:
                poner(next(d for d in pet["datos"] if "valores" in d)["valores"], ruta, h)
            r, exc, nrc, dt = llamar(pet)
            n += 1
            nf += 1
            et = (f, donde, "/".join(map(str, ruta)), repr(h)[:24])
            if exc:
                escapes.append(et + (exc,))
                if "RecursionError" not in exc:
                    print("   ESCAPE", et, exc, flush=True)
            elif nrc != 1:
                sin_rc.append(et + (nrc,))
            elif r["estado"] != "RECHAZADO" and no_finito(r["resultado"]):
                no_fin.append(et)
            elif r["estado"] != "RECHAZADO" and isinstance(h, (str, bytes, complex, bool, decimal.Decimal, fractions.Fraction)) \
                    and donde == "valores" and era_numero(pet0, ruta):
                servidas_raras.append(et)   # donde había un número se ha servido un texto, un bool, un Decimal…
            if dt > 30:
                lentas.append(et + (round(dt, 1),))
    print(f"   {f}: {nf} llamadas, acumulado {time.time() - t_ini:.0f} s; escapes {len(escapes)}", flush=True)

print(f"   {n} llamadas en {time.time() - t_ini:.0f} s")
for e in servidas_raras[:40]:
    print("   SERVIDA con un tipo raro donde había un número", e)
rec = [e for e in escapes if "RecursionError" in e[-1]]
otros = [e for e in escapes if "RecursionError" not in e[-1]]
print(f"   escapes: {len(rec)} RecursionError (lista anidada a 3 000 niveles en `valores`), {len(otros)} de otro tipo")
K.comprobar(f"ninguna excepción escapa del Motor con un dato anidado en profundidad ({len(rec)} RecursionError)", not rec,
            f"{len(rec)}; p. ej. {rec[:2]}")
K.comprobar(f"ninguna otra excepción escapa del Motor ({n} llamadas)", not otros, f"{len(otros)}: {otros[:5]}")
K.comprobar("cada llamada deja exactamente una entrada en RC", not sin_rc, str(sin_rc[:5]))
K.comprobar("nada servido con cifras no finitas", not no_fin, str(no_fin[:5]))
K.comprobar("ninguna llamada > 30 s", not lentas, str(lentas[:8]))
K.comprobar("ningún tipo raro (texto, bytes, complejo, bool, Decimal, Fraction) se sirve donde el dato era un número",
            not servidas_raras, f"{len(servidas_raras)}: {servidas_raras[:6]}")

# ---------------------------------------------------------------- 3. la petición entera
print("3. campos de la petición con tipos raros")
m = C.motor()
RAROS = [float("nan"), 10 ** 400, b"x", 1 + 2j, {1, 2}, [1], {"a": 1}, object(), np.array([1, 2]), profunda(), "", 0, True,
         decimal.Decimal("1")]
esc3 = []
for campo in ("semilla", "perfil", "clase", "plan", "fecha_corte", "horizonte", "modo", "prioridad", "datos", "parametros",
              "operacion"):
    for h in RAROS:
        for f in ("SIM-MC-001", "REI-CAP-001"):
            pet = base(f)
            pet[campo] = h
            try:
                r, exc, nrc, dt = llamar(pet)
            except BaseException as e:  # noqa: BLE001
                exc, nrc = f"{type(e).__name__}", 0
            if exc or nrc != 1:
                esc3.append((f, campo, repr(h)[:24], exc or f"RC {nrc}"))
for e in esc3[:40]:
    print("   ESCAPE", e)
K.comprobar("campos de la petición con tipos raros: sin excepción y con una entrada en RC", not esc3, f"{len(esc3)}")
sys.exit(K.fin())
