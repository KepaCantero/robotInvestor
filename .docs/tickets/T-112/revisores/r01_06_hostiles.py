"""QA r01 de T-112 · entradas hostiles y reglas transversales por Motor.servir, en las 35 fichas de la Fase 2.

Bloques:
 1. Fuzzer: cada parámetro y cada clave de primer nivel de `valores` del primer caso de control, con valores hostiles
    (NaN, ±inf, bool, texto, None, listas, objetos, 1e308, −1, 0, número como fecha). Nada debe escapar como excepción,
    cada llamada deja una entrada en RC y lo servido no lleva cifras no finitas.
 2. Parámetro no declarado (con errata): INC-T112-01 dice que se rechaza.
 3. Umbrales fijos: cada clave de `UMBRALES` en `parametros` se rechaza; en `valores`, o en la raíz de la petición, no
    cambia la cifra.
 4. Dominio: parámetros de tamaño sin cota superior (réplicas, arranques, B, horizonte de la simulación).
 5. Determinismo y semilla de la petición (ACEPTA_SEMILLA); semilla de la petición frente a la de `parametros`.
 6. BIB-MET-001: solicitantes.
 7. Datos en línea fechados después de la fecha de corte (fuga).
"""
import copy
import math
import signal
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import numpy as np  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

K = C.Contador("r01_06 hostiles y reglas transversales")
m = C.motor()
LENTAS = {"REG-HMM-001", "FIR-CURVE-001", "TEM-DIFF-001", "FX-REGIME-001", "BT-PBO-001"}
HOSTILES = [float("nan"), float("inf"), -float("inf"), True, "x", None, [], {}, [1, "a"], 1e308, -1, 0, 20261110, {"a": [1]}]


class Tiempo(Exception):
    pass


def _alarma(*_):
    raise Tiempo()


signal.signal(signal.SIGALRM, _alarma)


def llamar(pet, solicitante="AG-18", limite=90):
    antes = len(m.almacen.leer("RC"))
    signal.alarm(limite)
    try:
        r = m.servir(pet, solicitante)
        exc = None
    except Tiempo:
        r, exc = None, "TIEMPO"
    except BaseException as e:  # noqa: BLE001
        r, exc = None, f"{type(e).__name__}: {str(e)[:120]}"
    finally:
        signal.alarm(0)
    return r, exc, len(m.almacen.leer("RC")) - antes


def no_finito(x):
    if isinstance(x, dict):
        return any(no_finito(v) for v in x.values())
    if isinstance(x, list):
        return any(no_finito(v) for v in x)
    return isinstance(x, float) and not math.isfinite(x)


def modulo(f):
    return next(md for md in servicio.MODULOS_FASE2 if f in md.FICHAS)


def base(f, i=0):
    c = servicio.CASOS_CONTROL[f][i]
    return {"operacion": f, "datos": copy.deepcopy(c.get("datos") or []), "parametros": dict(c.get("parametros") or {}), "fecha_corte": None}


# ---------------------------------------------------------------- 1. fuzzer
print("1. fuzzer")
escapes, sin_rc, no_fin, lentas, n = [], [], [], [], 0
t_ini = time.time()
for f in sorted(servicio.FASE2):
    pet0 = base(f)
    hostiles = HOSTILES if f not in LENTAS else [float("nan"), True, "x", [], -1, 1e308]
    mod = modulo(f)
    claves_p = sorted(getattr(mod, "PARAMETROS_POR_DEFECTO", {}).get(f, {}))
    vals = next((d["valores"] for d in pet0["datos"] if "valores" in d), {})
    claves_v = sorted(vals) if f not in LENTAS else sorted(vals)[:3]
    for donde, claves in (("parametros", claves_p), ("valores", claves_v)):
        for k in claves:
            for h in hostiles:
                pet = copy.deepcopy(pet0)
                if donde == "parametros":
                    pet["parametros"][k] = h
                else:
                    next(d for d in pet["datos"] if "valores" in d)["valores"][k] = h
                t0 = time.time()
                print(f"   · {f} {donde}.{k} = {repr(h)[:20]}", flush=True)
                r, exc, nrc = llamar(pet)
                dt = time.time() - t0
                n += 1
                if exc:
                    escapes.append((f, donde, k, repr(h)[:20], exc))
                elif nrc < 1:
                    sin_rc.append((f, donde, k, repr(h)[:20]))
                elif r["estado"] != "RECHAZADO" and no_finito(r["resultado"]):
                    no_fin.append((f, donde, k, repr(h)[:20]))
                if dt > 30:
                    lentas.append((f, donde, k, repr(h)[:20], round(dt, 1)))
print(f"   {n} llamadas en {time.time() - t_ini:.0f} s")
K.comprobar(f"fuzzer: ninguna excepción escapa del Motor ({n} llamadas)", not escapes, str(escapes[:8]))
K.comprobar("fuzzer: cada llamada deja una entrada en RC", not sin_rc, str(sin_rc[:5]))
K.comprobar("fuzzer: nada servido con cifras no finitas", not no_fin, str(no_fin[:5]))
K.comprobar("fuzzer: ninguna llamada > 30 s", not lentas, str(lentas[:5]))

# ---------------------------------------------------------------- 2. parámetro no declarado
print("2. parámetro no declarado (errata)")
silenciosos = []
for f in sorted(servicio.FASE2):
    pet = base(f)
    mod = modulo(f)
    claves_p = sorted(getattr(mod, "PARAMETROS_POR_DEFECTO", {}).get(f, {}))
    if not claves_p:
        continue
    k = claves_p[0]
    pet["parametros"][k.upper() if k.lower() == k else k.lower()] = pet["parametros"].get(k, getattr(mod, "PARAMETROS_POR_DEFECTO")[f][k])
    pet["parametros"]["parametro_inexistente_qa"] = 1
    r, exc, _ = llamar(pet, limite=120)
    if r and r["estado"] != "RECHAZADO":
        silenciosos.append(f)
print("   servidas pese a un parámetro no declarado:", silenciosos)
K.comprobar("un parámetro no declarado se rechaza en las 35 (INC-T112-01)", not silenciosos, f"{len(silenciosos)} fichas: {silenciosos}")
# Ejemplo de consecuencia: método pedido con errata servido con el método por defecto
r, _, _ = llamar({"operacion": "RISK-VAR-001", "datos": base("RISK-VAR-001", 1)["datos"], "parametros": {"Metodo": "evt_pot"}})
print("   RISK-VAR-001 con {'Metodo': 'evt_pot'}:", r["estado"], r.get("resultado", {}).get("metodo"))
r, _, _ = llamar({"operacion": "ALT-DESMOOTH-001", "datos": base("ALT-DESMOOTH-001", 2)["datos"], "parametros": {"metodo ": "GLM", "fi": 0.1}})
print("   ALT-DESMOOTH-001 con {'metodo ': 'GLM', 'fi': 0.1}:", r["estado"], r.get("resultado", {}).get("metodo"), r.get("resultado", {}).get("phi"))

# ---------------------------------------------------------------- 3. umbrales fijos
print("3. umbrales fijos")
aceptados, cambian = [], []
for f in sorted(servicio.FASE2):
    mod = modulo(f)
    U = getattr(mod, "UMBRALES", {}).get(f, {})
    ref, _, _ = llamar(base(f), limite=120)
    for k in U:
        for val in (0, 1, 10 ** 6, U[k]):
            pet = base(f)
            pet["parametros"][k] = val
            r, exc, _ = llamar(pet, limite=120)
            if exc or r["estado"] != "RECHAZADO":
                aceptados.append((f, k, val, exc or r["estado"]))
    if f in LENTAS:
        continue
    for k in U:
        for val in (0, 1, 10 ** 6):
            pet = base(f)
            next(d for d in pet["datos"] if "valores" in d)["valores"][k] = val
            pet[k] = val
            r, exc, _ = llamar(pet, limite=120)
            if exc:
                cambian.append((f, k, val, exc))
            elif r["estado"] != "RECHAZADO" and ref["estado"] != "RECHAZADO":
                a = {x: y for x, y in r["resultado"].items() if x != "advertencias"}
                b = {x: y for x, y in ref["resultado"].items() if x != "advertencias"}
                if a != b:
                    cambian.append((f, k, val, "cifra distinta"))
K.comprobar("cada clave de UMBRALES en «parametros» se rechaza, con cualquier valor", not aceptados, str(aceptados[:8]))
K.comprobar("una clave de UMBRALES en «valores» o en la raíz de la petición no cambia la cifra", not cambian, str(cambian[:8]))

# ---------------------------------------------------------------- 4. dominio sin cota superior
print("4. dominio sin cota superior (solo validación: no se ejecuta el cálculo)")
from bloque_a.motor import fichas_riesgo, fichas_series  # noqa: E402

sin_cota = []
for mod, f, k, v in [(fichas_riesgo, "ML-PRED-001", "replicas", 10 ** 12), (fichas_riesgo, "ML-CAL-001", "replicas", 10 ** 12),
                     (fichas_riesgo, "SIM-MC-001", "horizonte", 10 ** 12), (fichas_series, "TEM-DIFF-001", "B", 10 ** 12),
                     (fichas_series, "TEM-DIFF-001", "arranques", 10 ** 12), (fichas_series, "REG-HMM-001", "arranques", 10 ** 12),
                     (fichas_riesgo, "RISK-VAR-001", "horizonte", 10 ** 12)]:
    extra = {"semilla": 1} if f == "SIM-MC-001" else {}
    try:
        mod._parametros(f, {k: v, **extra})
        sin_cota.append(f"{f}.{k}={v:g}")
    except Exception:  # noqa: BLE001
        pass
print("   aceptados por la validación:", sin_cota)
# Coste real con un valor moderado: ML-PRED-001 con 10⁵ réplicas y TEM-DIFF-001 con B = 20 000
pet = base("ML-PRED-001", 1)
for rep in (1000, 100_000):
    pet["parametros"]["replicas"] = rep
    t0 = time.time()
    r, exc, _ = llamar(pet, limite=300)
    print(f"   ML-PRED-001 replicas = {rep}: {time.time() - t0:.1f} s, {exc or r['estado']}")
pet = base("TEM-DIFF-001")
for B in (1000, 10_000):
    pet["parametros"]["B"] = B
    t0 = time.time()
    r, exc, _ = llamar(pet, limite=600)
    print(f"   TEM-DIFF-001 B = {B}: {time.time() - t0:.1f} s, {exc or r['estado']}")
K.comprobar("los tamaños de la petición (réplicas, arranques, B, horizonte) tienen cota superior", not sin_cota, str(sin_cota))

# ---------------------------------------------------------------- 5. determinismo y semilla
print("5. determinismo y semilla")
distintos = []
for f in sorted(servicio.FASE2):
    m2 = C.motor()
    a = m.servir(base(f), "AG-18")
    b = m2.servir(base(f), "AG-18")
    if a.get("resultado") != b.get("resultado") or a["estado"] != b["estado"]:
        distintos.append(f)
K.comprobar("mismo resultado en dos Motores nuevos (35 fichas)", not distintos, str(distintos))
sin_efecto, sin_registro = [], []
for f in sorted(servicio.ACEPTA_SEMILLA & servicio.FASE2):
    pet = base(f)
    pet["parametros"].pop("semilla", None)
    r1 = C.motor().servir({**pet, "semilla": 101}, "AG-18")
    r2 = C.motor().servir({**pet, "semilla": 101}, "AG-18")
    r3 = C.motor().servir({**pet, "semilla": 202}, "AG-18")
    if r1.get("resultado") != r2.get("resultado"):
        distintos.append(f + " (misma semilla)")
    if r1.get("resultado") == r3.get("resultado"):
        sin_efecto.append(f)
    rs = r1.get("resultado", {}).get("semilla")
    if rs is not None and rs != 101:
        sin_registro.append((f, rs))
print("   semilla de la petición sin efecto en la cifra:", sin_efecto)
K.comprobar("la semilla de la petición llega a la ficha (la que publica la ficha es la pedida)", not sin_registro, str(sin_registro))
K.comprobar("misma semilla ⇒ mismo resultado", not any("misma" in d for d in distintos), str(distintos))
# Semilla en «parametros» y en la petición, distintas: ¿qué semilla queda en el artefacto de RC?
pet = base("SIM-MC-001")
pet["parametros"]["semilla"] = 5
mm = C.motor()
r = mm.servir({**pet, "semilla": 7}, "AG-18")
e = mm.almacen.estado("RC")[r["calc_id"]]
print(f"   SIM-MC-001 con parametros.semilla 5 y semilla 7: usada {r['resultado'].get('semilla')}, RC.semilla {e.get('semilla')}, "
      f"RC.parametros.semilla {e['parametros'].get('semilla')}")
K.comprobar("el artefacto no registra una semilla distinta de la usada", e.get("semilla") in (None, r["resultado"].get("semilla")),
            f"RC.semilla {e.get('semilla')} frente a la usada {r['resultado'].get('semilla')}")

# ---------------------------------------------------------------- 6. BIB-MET-001
print("6. BIB-MET-001 y sus solicitantes")
for sol, esperado in [("AG-18", "SERVED"), ("AG-20", "SERVED"), ("AG-21", "RECHAZADO"), ("AG-13", "RECHAZADO"), ("ag-18", "RECHAZADO"),
                      (" AG-18", "RECHAZADO"), (None, "RECHAZADO"), ("", "RECHAZADO")]:
    r, exc, nrc = llamar(base("BIB-MET-001"), solicitante=sol)
    ok = (exc is None and r["estado"].startswith(esperado) and (esperado == "SERVED" or r["motivo"] == "CANAL_NO_AUTORIZADO") and nrc == 1)
    K.comprobar(f"BIB-MET-001 pedida por {sol!r}: {esperado}", ok, str(exc or r)[:200])
r, exc, _ = llamar(base("BIB-MET-001"), solicitante=["AG-18"])
K.comprobar("BIB-MET-001 con un solicitante no textual: RECHAZADO sin excepción", exc is None and r["estado"] == "RECHAZADO", str(exc or r)[:200])
mm = C.motor()
a = mm.servir(base("BIB-MET-001"), "AG-18")
b = mm.servir(base("BIB-MET-001"), "AG-21")
K.comprobar("la caché no entrega a AG-21 lo que pidió AG-18", b["estado"] == "RECHAZADO", str(b)[:200])

# ---------------------------------------------------------------- 7. fuga en datos en línea
print("7. datos en línea posteriores a la fecha de corte")
pet = base("ACC-VAL-001")
v = next(d for d in pet["datos"] if "valores" in d)["valores"]
v["ejercicios"][-1]["fecha_presentacion"] = "2027-06-30"
pet["fecha_corte"] = "2026-11-13"
r, exc, _ = llamar(pet)
print("   ACC-VAL-001 con un ejercicio presentado el 2027-06-30 y corte 2026-11-13:", exc or r["estado"])
K.comprobar("ACC-VAL-001 no usa un ejercicio presentado después de la fecha de la capitalización", exc is None and r["estado"] == "RECHAZADO",
            str(exc or r.get("limitaciones"))[:200])
sys.exit(K.fin())
