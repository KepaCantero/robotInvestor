"""QA r01 de T-118 · H-10: cotas del tamaño de los datos del grupo R y coste del servicio más caro que admiten.

 A. Inventario mecánico: en cada caso de control de las nueve fichas del grupo R, cada lista y cada objeto de `valores`
    (a cualquier profundidad) se agranda —solo, y todas las listas de la misma longitud a la vez, para no romper la
    alineación— hasta 3 000 y 1 000 001 elementos (listas) y 1 001 y 5 001 claves (objetos). ¿Se sirve alguno? ¿Cuánto tarda?
 B. Tiempo hasta el rechazo de los dos casos del hallazgo y de las listas más grandes: ¿se rechaza antes de calcular?
 C. El servicio más caro que admiten las cotas, por Motor.servir, con cada dato en su cota y los parámetros de tamaño en
    su máximo (candidatos por ficha).
Uso: .venv/bin/python -I r01_02_h10_cotas_y_costes.py [A] [B] [C]     (sin letras: las tres)
"""
import copy
import signal
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from bloque_a.motor import fichas_riesgo as R  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

BLOQUES = {a for a in sys.argv[1:] if a in ("A", "B", "C")} or {"A", "B", "C"}
K = C.Contador("r01_02 H-10")
m = C.motor()
LIMITE = 420
FICHAS_R = sorted(R.FICHAS)
H5 = 2520


class Tarde(Exception):
    pass


def _alarma(*_):
    raise Tarde()


signal.signal(signal.SIGALRM, _alarma)


def llamar(pet, limite=LIMITE):
    t0 = time.perf_counter()
    signal.alarm(limite)
    try:
        r, exc, n = C.servir_contando(m, pet)
    except Tarde:
        return f"NO TERMINA en {limite} s", time.perf_counter() - t0, None
    finally:
        signal.alarm(0)
    dt = time.perf_counter() - t0
    if exc is not None:
        return f"EXCEPCION {type(exc).__name__}: {str(exc)[:100]}", dt, n
    return (r["estado"] if str(r["estado"]).startswith("SERVED") else f"RECHAZADO: {r['detalle'][:120]}"), dt, n


def contenedores(x, camino=()):
    if isinstance(x, dict):
        yield camino, x
        for k, v in x.items():
            yield from contenedores(v, (*camino, k))
    elif isinstance(x, list):
        yield camino, x
        for i, v in enumerate(x[:1]):
            yield from contenedores(v, (*camino, i))


def en(x, camino):
    for c in camino:
        x = x[c]
    return x


def poner(x, camino, valor):
    en(x, camino[:-1])[camino[-1]] = valor


def agrandar_lista(lst, n):
    return [copy.deepcopy(lst[i % len(lst)]) for i in range(n)] if lst else lst


def agrandar_objeto(d, n):
    if not d:
        return d
    k0 = next(iter(d))
    out = dict(d)
    for i in range(n - len(d)):
        out[f"zz_extra_{i:05d}"] = copy.deepcopy(d[k0])
    return out


if "A" in BLOQUES:
    print("[A] inventario: cada contenedor de `valores` agrandado")
    servidos, lentos, total, sin_maximo = [], [], 0, {}
    for f in FICHAS_R:
        for i, caso in enumerate(servicio.CASOS_CONTROL[f]):
            base = C.peticion(f, i)
            e0, _, _ = llamar(base)
            if not e0.startswith("SERVED"):
                continue
            vals = base["datos"][0]["valores"] if base["datos"] and "valores" in base["datos"][0] else None
            if vals is None:
                continue
            caminos = [(c, x) for c, x in contenedores(vals) if c]
            for camino, x in caminos:
                tamanos = (3000, 1_000_001) if isinstance(x, list) else (1001, 5001)
                for n in tamanos:
                    if isinstance(x, list) and n > 3000 and x and isinstance(x[0], (dict, list)):
                        n = 100_001          # listas de objetos: bastan cien mil
                    pet = copy.deepcopy(base)
                    v = pet["datos"][0]["valores"]
                    poner(v, camino, agrandar_lista(x, n) if isinstance(x, list) else agrandar_objeto(x, n))
                    e, dt, k = llamar(pet, 120)
                    total += 1
                    nombre = f"{f} caso {i} · {'/'.join(map(str, camino))} × {n}"
                    if e.startswith("SERVED"):
                        servidos.append((nombre, round(dt, 1)))
                    elif "máximo" not in e and "cota" not in e:
                        sin_maximo[nombre] = e[:110]
                    if dt > 20 or e.startswith(("NO TERMINA", "EXCEPCION")) or k != 1:
                        lentos.append((nombre, round(dt, 1), e[:80], k))
            # todas las listas de la longitud más frecuente ≥ 30, a la vez (mantiene la alineación)
            listas = [(c, x) for c, x in caminos if isinstance(x, list) and len(x) >= 30]
            for L in sorted({len(x) for _, x in listas}):
                grupo = [(c, x) for c, x in listas if len(x) == L]
                for n in (H5 + 1, 3000, 20_000):
                    pet = copy.deepcopy(base)
                    v = pet["datos"][0]["valores"]
                    for c, x in grupo:
                        poner(v, c, agrandar_lista(x, n))
                    e, dt, k = llamar(pet, 120)
                    total += 1
                    nombre = f"{f} caso {i} · las {len(grupo)} listas de longitud {L} × {n}"
                    if e.startswith("SERVED"):
                        servidos.append((nombre, round(dt, 1)))
                    elif "máximo" not in e and "cota" not in e:
                        sin_maximo[nombre] = e[:110]
                    if dt > 20 or e.startswith(("NO TERMINA", "EXCEPCION")) or k != 1:
                        lentos.append((nombre, round(dt, 1), e[:80], k))
        print(f"   {f}: acumulado {total} peticiones, {len(servidos)} servidas, {len(lentos)} lentas o anómalas")
        sys.stdout.flush()
    print(f"   peticiones: {total}")
    print(f"   SERVIDAS con un contenedor agrandado: {len(servidos)}")
    for s in servidos:
        print(f"      {s}")
    print(f"   rechazadas por otro motivo que la cota (se listan para leerlas): {len(sin_maximo)}")
    for k_, v_ in sin_maximo.items():
        print(f"      {k_}: {v_}")
    K.comprobar("ninguna petición con un dato agrandado tarda más de 20 s, escapa o deja de registrar", not lentos, str(lentos)[:800])

if "B" in BLOQUES:
    print("\n[B] tiempo hasta el rechazo")
    rng = np.random.default_rng(7)
    grande = [float(x) for x in 0.01 * rng.standard_normal(100_000)]
    casosB = [
        ("BT-VAR-001 generado, historico_filtrado, 100 000 rendimientos",
         {"operacion": "BT-VAR-001", "datos": [{"valores": {"rendimientos": grande}}], "parametros": {"metodo_var": "historico_filtrado"}}),
        ("BT-VAR-001 generado, historico_filtrado, 2 521 rendimientos",
         {"operacion": "BT-VAR-001", "datos": [{"valores": {"rendimientos": grande[:2521]}}], "parametros": {"metodo_var": "historico_filtrado"}}),
        ("BT-PBO-001 S=20, 3 000 configuraciones de 80",
         {"operacion": "BT-PBO-001", "datos": [{"valores": {"rendimientos": {f"c{i:04d}": grande[i:i + 80] for i in range(3000)}}}], "parametros": {"S": 20}}),
        ("BT-PBO-001 S=20, 1 001 configuraciones de 2 520",
         {"operacion": "BT-PBO-001", "datos": [{"valores": {"rendimientos": {f"c{i:04d}": grande[i:i + 2520] for i in range(1001)}}}], "parametros": {"S": 20}}),
        ("BT-PBO-001 S=20, 1 000 configuraciones, la última de 2 521",
         {"operacion": "BT-PBO-001", "datos": [{"valores": {"rendimientos": {f"c{i:04d}": grande[i:i + 2520 + (i == 999)] for i in range(1000)}}}], "parametros": {"S": 20}}),
        ("DEC-VOI-001 con 1 000 001 muestras",
         {"operacion": "DEC-VOI-001", "datos": [{"valores": {"puntuacion": {"dimension": "E", "actual": 58.0},
                                                             "muestras": {"fuente": "SIM-MC-001", "valores": [1.0, 2.0] * 500_000 + [3.0]}}}],
          "parametros": {"coste_uc": 0.02}}),
        ("RISK-VAR-001 distribución de 1 000 001",
         {"operacion": "RISK-VAR-001", "datos": [{"valores": {"distribucion": {"semilla": 1, "rendimientos": (grande * 10) + [0.0]}}}], "parametros": {}}),
        ("ML-PRED-001 con 21 variables",
         None),
    ]
    v21 = C.valores("ML-PRED-001")
    x0 = next(iter(v21["variables"].values()))
    v21["variables"] = {f"x{i:02d}": copy.deepcopy(x0) for i in range(21)}
    casosB[-1] = ("ML-PRED-001 con 21 variables", {"operacion": "ML-PRED-001", "datos": [{"valores": v21}], "parametros": {}})
    for nombre, pet in casosB:
        e, dt, k = llamar(pet, 300)
        print(f"   {nombre:62} {dt:6.2f} s  {e[:130]}")
        K.comprobar(f"{nombre}: RECHAZADO por la cota en menos de 10 s y con su entrada en RC",
                    e.startswith("RECHAZADO") and "máximo" in e and dt < 10 and k == 1, f"{dt:.1f} s · {e}")

if "C" in BLOQUES:
    print("\n[C] el servicio más caro que admiten las cotas (por Motor.servir; cada uno con su reloj)")
    rng = np.random.default_rng(11)

    def ruido(n, escala=0.01, s=0):
        return [float(x) for x in escala * np.random.default_rng(100 + s).standard_normal(n)]

    def garch_serie(n):
        r, s2 = [], 1e-4
        g = np.random.default_rng(5)
        for _ in range(n):
            e = float(np.sqrt(s2) * g.standard_normal())
            r.append(e)
            s2 = 2e-6 + 0.08 * e * e + 0.9 * s2
        return r

    def pred(n, k):
        g = np.random.default_rng(1181)
        fechas = [str(d.date()) for d in pd.bdate_range("2000-01-03", periods=n)]
        x = g.standard_normal((n, k))
        serie = 100 * np.exp(np.cumsum(0.01 * np.r_[0.0, x[:-1, 0]] + 0.005 * g.standard_normal(n)))
        return {"fechas": fechas, "objetivo": {"serie": [float(e) for e in serie], "horizonte": 1, "tipo": "direccion",
                                               "criterio_resolucion": "cierre siguiente por encima del actual"},
                "variables": {f"x{i:02d}": {"serie": [float(e) for e in x[:, i]], "conocible_desde": fechas} for i in range(k)}}

    def cal(n, s):
        y = ruido(n, 1.0, s)
        return {"tipo": "nivel", "realizaciones": y, "predicciones": [a + 0.1 * b for a, b in zip(y, ruido(n, 1.0, s + 50))]}

    G = garch_serie(H5)
    rej20 = [float(x) for x in np.logspace(-3, 3, 20)]
    candidatos = [
        ("BT-VAR-001 generado · historico_filtrado · 2 520 · ventana 250", "BT-VAR-001", {"rendimientos": G},
         {"metodo_var": "historico_filtrado", "ventana_estimacion": 250}),
        ("BT-VAR-001 generado · evt_pot · 2 520 · ventana 500", "BT-VAR-001", {"rendimientos": G},
         {"metodo_var": "evt_pot", "ventana_estimacion": 500}),
        ("BT-VAR-001 generado · t · 2 520 · ventana 250", "BT-VAR-001", {"rendimientos": G}, {"metodo_var": "t"}),
        ("BT-VAR-001 generado · cornish_fisher · 2 520 · ventana 250", "BT-VAR-001", {"rendimientos": G}, {"metodo_var": "cornish_fisher"}),
        ("BT-PBO-001 · S 20 · 1 000 configuraciones × 2 520", "BT-PBO-001",
         {"rendimientos": {f"c{i:04d}": [float(x) for x in fila] for i, fila in enumerate(0.01 * rng.standard_normal((1000, H5)))}}, {"S": 20}),
        ("BT-PBO-001 · S 20 · 1 000 configuraciones × 80", "BT-PBO-001",
         {"rendimientos": {f"c{i:04d}": [float(x) for x in fila] for i, fila in enumerate(0.01 * rng.standard_normal((1000, 80)))}}, {"S": 20}),
        ("ML-PRED-001 · 2 520 × 20 variables · rejilla 20 · pliegues 20 · réplicas 10 000 · logística", "ML-PRED-001", pred(H5, 20),
         {"rejilla": rej20, "pliegues": 20, "replicas": 10_000}),
        ("ML-PRED-001 · ídem · calibración isotónica", "ML-PRED-001", pred(H5, 20),
         {"rejilla": rej20, "pliegues": 20, "replicas": 10_000, "calibracion": "isotonica"}),
        ("ML-PRED-001 · ídem · ridge", "ML-PRED-001", {**pred(H5, 20), "objetivo": {**pred(H5, 1)["objetivo"], "tipo": "nivel"}},
         {"rejilla": rej20, "pliegues": 20, "replicas": 10_000, "modelo": "ridge"}),
        ("ML-CAL-001 · 5 horizontes × 2 520 · réplicas 10 000", "ML-CAL-001",
         {"ensayos": 1, "horizontes": {f"H{i}": cal(H5, i) for i in range(1, 6)}}, {"replicas": 10_000}),
        ("SIM-MC-001 · bootstrap filtrado · 2 520 residuos · historia 2 520 · n 10 000 × h 2 520 · 99 cuantiles y umbrales", "SIM-MC-001",
         {"dinamica": {"tipo": "bootstrap_filtrado", "mu": 0.0, "omega": 2e-6, "alpha": 0.08, "beta": 0.9, "residuos": ruido(H5, 1.0)},
          "historia_rendimientos": ruido(H5)},
         {"horizonte": H5, "semilla": 1, "n_trayectorias": 10_000, "reduccion_varianza": "ninguna",
          "cuantiles": [i / 100 for i in range(1, 100)], "umbrales": [i / 1000 - 0.05 for i in range(99)]}),
        ("SIM-MC-001 · garch · n 1 000 000 × h 25", "SIM-MC-001",
         {"dinamica": {"tipo": "garch", "mu": 0.0, "omega": 2e-6, "alpha": 0.08, "beta": 0.9}},
         {"horizonte": 25, "semilla": 1, "n_trayectorias": 1_000_000}),
        ("SCN-H-001 · 2 520 rendimientos · n 1 000 000 · H1 y H2", "SCN-H-001", {"rendimientos": G},
         {"semilla": 1, "n_trayectorias": 1_000_000, "clase": "RV"}),
        ("RISK-VAR-001 · historico_filtrado · 2 520", "RISK-VAR-001", {"rendimientos": G}, {"metodo": "historico_filtrado"}),
        ("RISK-VAR-001 · evt_pot · distribución de 1 000 000", "RISK-VAR-001",
         {"distribucion": {"semilla": 1, "rendimientos": [float(x) for x in 0.01 * rng.standard_t(4, 1_000_000)]}}, {"metodo": "evt_pot"}),
        ("DEC-VOI-001 · 1 000 000 muestras", "DEC-VOI-001",
         {"puntuacion": {"dimension": "E", "actual": 58.0},
          "muestras": {"fuente": "SIM-MC-001", "valores": [float(x) for x in 6.0 * rng.standard_normal(1_000_000)]}}, {"coste_uc": 0.02}),
        ("BT-DSR-001 · 2 520", "BT-DSR-001", {"rendimientos": G, "varianza_sr_ensayos": {"valor": 0.5, "unidad": "anual"}}, {"N": 10}),
    ]
    solo = [a for a in sys.argv[1:] if a.startswith("--solo=")]
    peor = (0.0, "")
    for nombre, f, vals, params in candidatos:
        if solo and not any(s[7:] in nombre for s in solo):
            continue
        e, dt, k = llamar({"operacion": f, "datos": [{"valores": vals}], "parametros": params})
        print(f"   {nombre:100} {dt:7.1f} s  {e[:110]}")
        sys.stdout.flush()
        if e.startswith("SERVED") and dt > peor[0]:
            peor = (dt, nombre)
        K.comprobar(f"{nombre}: termina (límite {LIMITE} s) y deja su entrada en RC", not e.startswith(("NO TERMINA", "EXCEPCION")) and k == 1, e)
    print(f"   el más caro servido: {peor[0]:.1f} s · {peor[1]}")
    K.comprobar("el servicio más caro que admiten las cotas termina «en torno a un minuto» (≤ 120 s con la máquina compartida)",
                peor[0] <= 120, f"{peor[0]:.0f} s · {peor[1]}")

sys.exit(K.fin())
