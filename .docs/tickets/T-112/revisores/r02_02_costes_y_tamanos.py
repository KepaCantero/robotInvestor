"""QA r02 de T-112 · H-01 de la r01, ¿de verdad cerrado? Coste del caso más caro ADMITIDO y tamaños de los DATOS.

La r01 probó parámetros de tamaño sin cota. Aquí:
 A. cada parámetro de tamaño en su máximo admitido (y combinados), con los datos del caso de control: ¿termina?;
 C. grupo R, que no acota el tamaño de los datos: BT-VAR-001 generando el VaR con un GARCH por observación, BT-PBO-001 con
    muchas configuraciones y ML-PRED-001 con muchas variables;
 D. el servicio más caro que admiten las cotas: REG-HMM-001 y FX-REGIME-001 con sus máximos de observaciones;
 B. los DATOS en línea de cada ficha agrandados (cada lista numérica o de objetos de `valores`, repetida hasta N
    elementos, con las fechas regeneradas): ¿rechaza por cota, sirve en un tiempo razonable o se cuelga / agota memoria?
Cada llamada tiene un límite de LIMITE segundos (SIGALRM) y el proceso se lanza con `ulimit -v`. Se mide por
`Motor.servir` (doble pasada incluida). Uso: (ulimit -v 8000000; .venv/bin/python -I r02_02_costes_y_tamanos.py [A] [B] [C] [D])
"""
import copy
import datetime as dt
import re
import signal
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

BLOQUES = [a for a in sys.argv[1:] if a in ("A", "B", "C", "D")] or ["A", "B", "C", "D"]
C.preparar(["x"])
import numpy as np  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

K = C.Contador("r02_02 costes y tamaños")
LIMITE = 300


class Tiempo(Exception):
    pass


def _alarma(*_):
    raise Tiempo()


signal.signal(signal.SIGALRM, _alarma)


def llamar(pet, limite=LIMITE):
    m = C.motor()
    signal.alarm(limite)
    t0 = time.time()
    try:
        r = m.servir(pet, "AG-18")
        out = r["estado"] + ("" if r["estado"] != "RECHAZADO" else ": " + r["detalle"][:110])
    except Tiempo:
        out = "TIEMPO"
    except BaseException as e:  # noqa: BLE001
        out = f"ESCAPE {type(e).__name__}: {str(e)[:100]}"
    finally:
        signal.alarm(0)
    return out, time.time() - t0


def aplanar(x):
    if isinstance(x, dict):
        return {k: aplanar(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [aplanar(v) for v in x]
    if isinstance(x, np.ndarray):
        return [aplanar(v) for v in x.tolist()]
    if isinstance(x, np.generic):
        return x.item()
    return x


def base(f, i=0, **params):
    c = servicio.CASOS_CONTROL[f][i]
    p = dict(c.get("parametros") or {})
    p.update(params)
    return {"operacion": f, "datos": aplanar(copy.deepcopy(c.get("datos") or [])), "parametros": p, "fecha_corte": None}


lentos, colgados, escapes = [], [], []


def medir(nombre, pet, limite=LIMITE):
    out, t = llamar(pet, limite)
    print(f"   {nombre:<70} {t:7.1f} s  {out[:130]}", flush=True)
    if out == "TIEMPO":
        colgados.append((nombre, limite))
    elif out.startswith("ESCAPE"):
        escapes.append((nombre, out))
    elif t > 60:
        lentos.append((nombre, round(t)))
    return out, t


if "A" in BLOQUES:
    print(f"A. parámetros de tamaño en su máximo admitido (límite {LIMITE} s por llamada)")
    medir("TEM-DIFF-001 B=10000", base("TEM-DIFF-001", B=10000))
    medir("TEM-DIFF-001 arranques=200 B=1000", base("TEM-DIFF-001", arranques=200, B=1000))
    medir("TEM-DIFF-001 B=10000 arranques=200", base("TEM-DIFF-001", B=10000, arranques=200))
    medir("REG-HMM-001 BIC arranques=50", base("REG-HMM-001", 0, n_estados="BIC", arranques=50))
    medir("REG-HMM-001 BIC arranques=50 completa", base("REG-HMM-001", 0, n_estados="BIC", arranques=50, covarianza="completa"))
    medir("FX-REGIME-001 n_estados=3 medias y varianzas", base("FX-REGIME-001", 0, n_estados=3, medias_distintas=True))
    medir("ML-PRED-001 replicas=10000", base("ML-PRED-001", 0, replicas=10000))
    medir("ML-PRED-001 rejilla 20 × pliegues 20 × replicas 10000",
          base("ML-PRED-001", 0, replicas=10000, pliegues=20, rejilla=[10 ** (i / 4 - 2) for i in range(20)]))
    medir("ML-CAL-001 replicas=10000", base("ML-CAL-001", 0, replicas=10000))
    medir("SIM-MC-001 n=1e6 h=25", base("SIM-MC-001", 0, n_trayectorias=1_000_000, horizonte=25))
    medir("SIM-MC-001 n=10000 h=2520", base("SIM-MC-001", 0, n_trayectorias=10_000, horizonte=2520))
    for i, c in enumerate(servicio.CASOS_CONTROL["SIM-MC-001"]):
        tipo = (c["datos"][0]["valores"].get("dinamica") or {}).get("tipo")
        medir(f"SIM-MC-001 caso {i} ({tipo}) n=10000 h=2520 99 cuantiles 99 umbrales",
              base("SIM-MC-001", i, n_trayectorias=10_000, horizonte=2520, cuantiles=[k / 100 for k in range(1, 100)],
                   umbrales=[k / 100 for k in range(-49, 50)]))
    medir("SCN-H-001 n=1e6", base("SCN-H-001", 0, n_trayectorias=1_000_000))
    medir("BT-PBO-001 S=20", base("BT-PBO-001", 0, S=20))
    medir("RISK-VAR-001 horizonte=2520", base("RISK-VAR-001", 0, horizonte=2520))
    medir("FIR-CURVE-001 arranques=100", base("FIR-CURVE-001", 0, arranques=100))
    medir("DER-OPT-001 pasos=1000", base("DER-OPT-001", 0, pasos=1000, modelo="CRR"))
    medir("BT-VAR-001 ventana 250 horizonte 2520", base("BT-VAR-001", 0, horizonte=2520))

_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def agrandar(x, n, ini=dt.date(1900, 1, 1)):
    """Repite cada lista de ≥ 8 elementos hasta n; las listas de fechas ISO y los campos `fecha*` se regeneran diarios."""
    if isinstance(x, dict):
        return {k: agrandar(v, n, ini) for k, v in x.items()}
    if isinstance(x, list) and len(x) >= 8:
        if all(isinstance(e, str) and _ISO.match(e) for e in x):
            return [(ini + dt.timedelta(days=i)).isoformat() for i in range(n)]
        rep = [copy.copy(x[i % len(x)]) for i in range(n)]
        if all(isinstance(e, dict) for e in rep):
            for i, e in enumerate(rep):
                for k in list(e):
                    if isinstance(e[k], str) and _ISO.match(e[k]):
                        e[k] = (ini + dt.timedelta(days=i + (1 if "publicacion" in k or "vencimiento" in k else 0))).isoformat()
                    elif k in ("ejercicio", "anio") and isinstance(e[k], int):
                        e[k] = 1000 + i
        return rep
    if isinstance(x, list):
        return [agrandar(v, n, ini) for v in x]
    return x


if "B" in BLOQUES:
    for n in (20_000, 300_000):
        print(f"B. datos en línea agrandados a {n} elementos por lista (límite {LIMITE} s)")
        for f in sorted(servicio.FASE2):
            pet = base(f)
            for d in pet["datos"]:
                if "valores" in d:
                    d["valores"] = agrandar(d["valores"], n)
            medir(f"{f} × {n}", pet)

if "C" in BLOQUES:
    print(f"C. grupo R: datos sin cota de tamaño con coste alto por elemento (límite {LIMITE} s)")
    rng = np.random.default_rng(1)
    for n in (2_000, 100_000):
        x = [float(a) for a in rng.standard_t(6, n) * 0.01]
        medir(f"BT-VAR-001 generado con historico_filtrado, historia de {n}",
              {"operacion": "BT-VAR-001", "datos": [{"valores": {"rendimientos": x}}],
               "parametros": {"metodo_var": "historico_filtrado", "nivel": 0.95, "ventana_estimacion": 250}})
    for N in (50, 400, 3000):
        cfgs = {f"c{i}": [float(a) for a in rng.normal(0.0003, 0.01, 80)] for i in range(N)}
        medir(f"BT-PBO-001 S=20 con {N} configuraciones de 80 observaciones",
              {"operacion": "BT-PBO-001", "datos": [{"valores": {"rendimientos": cfgs}}], "parametros": {"S": 20}})
    pet = base("ML-PRED-001")
    v = pet["datos"][0]["valores"]
    n_obs = len(v["fechas"])
    for nv in (50, 300):
        v["variables"] = {f"x{i}": {"serie": [float(a) for a in rng.normal(0, 1, n_obs)], "conocible_desde": list(v["fechas"])} for i in range(nv)}
        pet["parametros"].update({"pliegues": 20, "rejilla": [10 ** (i / 4 - 2) for i in range(20)]})
        medir(f"ML-PRED-001 con {nv} variables, 20 pliegues y rejilla de 20", copy.deepcopy(pet))

if "D" in BLOQUES:
    print("D. el servicio más caro que admiten las cotas (el análisis declara ~4 min): REG-HMM-001 al máximo (límite 900 s)")
    rng = np.random.default_rng(2)
    n_obs, n_var = 520, 5
    reg = (np.arange(n_obs) // 40) % 3
    datos = {f"v{j}": [float(a) for a in rng.normal(reg * (j + 1) * 0.3, 1 + reg, n_obs)] for j in range(n_var)}
    import pandas as pd
    fechas = [str(d.date()) for d in pd.date_range("2015-01-02", periods=n_obs, freq="W-FRI")]
    medir("REG-HMM-001 520 semanas × 5 variables, BIC, 50 arranques, covarianza completa",
          {"operacion": "REG-HMM-001", "datos": [{"valores": {"variables": datos, "fechas": fechas}}],
           "parametros": {"n_estados": "BIC", "arranques": 50, "covarianza": "completa"}}, 900)
    y = [float(a) for a in rng.normal(0, 1, 756) * np.where((np.arange(756) // 60) % 3 == 0, 1, 3)]
    medir("FX-REGIME-001 756 observaciones, 3 estados, medias y varianzas",
          {"operacion": "FX-REGIME-001", "datos": [{"valores": {"serie": y}}], "parametros": {"n_estados": 3, "medias_distintas": True}}, 900)

K.comprobar(f"ninguna llamada admitida se cuelga (> {LIMITE} s)", not colgados, str(colgados))
K.comprobar("ninguna excepción escapa (MemoryError incluido)", not escapes, str(escapes)[:600])
K.comprobar("ninguna llamada admitida tarda más de 60 s", not lentos, str(lentos))
sys.exit(K.fin())
