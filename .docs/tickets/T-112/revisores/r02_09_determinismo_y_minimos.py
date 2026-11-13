"""QA r02 de T-112 · determinismo entre procesos y «Entradas mínimas» por muestreo.

 1. Determinismo entre PROCESOS (cada proceso de Python tiene su propia aleatorización del hash de textos, así que un
    resultado que dependa del orden de un conjunto o de un `hash()` cambiaría): los 136 casos de control de la Fase 2 se
    sirven en dos procesos distintos y se comparan los resultados, cifra a cifra.
 2. «Entradas mínimas» y «Aclaración y rechazo» del Catálogo, por muestreo: una entrada justo por debajo del mínimo que da
    la ficha se rechaza y una en el mínimo no se rechaza por ese motivo.
Uso: .venv/bin/python -I r02_09_determinismo_y_minimos.py            (lanza él mismo los dos procesos)
"""
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(["x"])
import numpy as np  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402


def todos():
    m = C.motor()
    out = {}
    for f in sorted(servicio.FASE2):
        for i, c in enumerate(servicio.CASOS_CONTROL[f]):
            r = m.servir({"operacion": f, "datos": copy.deepcopy(c.get("datos") or []), "parametros": dict(c.get("parametros") or {}),
                          "fecha_corte": c.get("fecha_corte")}, "AG-18")
            out[f"{f}:{i}"] = hashlib.sha256(json.dumps([r["estado"], r.get("resultado"), r.get("limitaciones")], sort_keys=True,
                                                        ensure_ascii=False, default=str).encode()).hexdigest()
    return out


if "--hijo" in sys.argv:
    print(json.dumps(todos()))
    sys.exit(0)

K = C.Contador("r02_09 determinismo entre procesos y entradas mínimas")
print("1. determinismo entre procesos")
salidas = []
for _ in range(2):
    r = subprocess.run([sys.executable, "-I", __file__, "--hijo"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-800:]
    salidas.append(json.loads(r.stdout.strip().splitlines()[-1]))
dist = sorted(k for k in salidas[0] if salidas[0][k] != salidas[1][k])
K.comprobar(f"{len(salidas[0])} casos de control: mismo resultado en dos procesos", not dist and len(salidas[0]) >= 136, str(dist[:10]))

print("2. entradas mínimas (muestreo)")
m = C.motor()


def servir(f, valores, **par):
    return m.servir({"operacion": f, "datos": [{"valores": valores}], "parametros": par}, "AG-18")


def par(nombre, bajo, justo, motivo_no=None):
    """`bajo` debe rechazarse; `justo` no debe rechazarse por tamaño (si se rechaza, se imprime el motivo)."""
    ok_b = bajo["estado"] == "RECHAZADO"
    ok_j = justo["estado"] != "RECHAZADO"
    K.comprobar(f"{nombre}: por debajo del mínimo se rechaza", ok_b, str(bajo)[:160])
    K.comprobar(f"{nombre}: en el mínimo se sirve", ok_j, justo.get("detalle", "")[:200])


rng = np.random.default_rng(42)
x = lambda n, s=0.01: [float(a) for a in rng.normal(0.0004, s, n)]  # noqa: E731
# RISK-VAR-001 · ≥ 250 observaciones; nivel 99 % empírico con < 500 observaciones se rechaza
par("RISK-VAR-001 (250 observaciones)", servir("RISK-VAR-001", {"rendimientos": x(249)}), servir("RISK-VAR-001", {"rendimientos": x(250)}))
par("RISK-VAR-001 (99 % empírico: 500 observaciones)", servir("RISK-VAR-001", {"rendimientos": x(499)}, nivel=0.99),
    servir("RISK-VAR-001", {"rendimientos": x(500)}, nivel=0.99))
par("RISK-VAR-001 (nivel 0,90–0,99)", servir("RISK-VAR-001", {"rendimientos": x(600)}, nivel=0.995), servir("RISK-VAR-001", {"rendimientos": x(600)}, nivel=0.90))
# BT-DSR-001 · ≥ 250 sesiones; N obligatorio
v = lambda n: {"rendimientos": x(n), "varianza_sr_ensayos": {"valor": 0.5, "unidad": "anual"}}  # noqa: E731
par("BT-DSR-001 (250 sesiones)", servir("BT-DSR-001", v(249), N=10), servir("BT-DSR-001", v(250), N=10))
K.comprobar("BT-DSR-001 sin N: rechazo", servir("BT-DSR-001", v(300))["estado"] == "RECHAZADO")
# BT-VAR-001 · ≥ 250 observaciones salvo declaración de baja potencia
bv = lambda n: {"var_previsto": [0.02] * n, "resultados": x(n)}  # noqa: E731
par("BT-VAR-001 (250 observaciones)", servir("BT-VAR-001", bv(249)), servir("BT-VAR-001", bv(250)))
# FX-BRK-001 · ≥ 30 observaciones (1 ruptura), ≥ 50 (2 o más)
s = lambda n: [float(a) for a in np.where(np.arange(n) < n // 2, 0.0, 3.0) + rng.normal(0, 0.3, n)]  # noqa: E731
par("FX-BRK-001 (30 observaciones)", servir("FX-BRK-001", {"serie": s(29)}), servir("FX-BRK-001", {"serie": s(30)}))
par("FX-BRK-001 (50 para dos rupturas)", servir("FX-BRK-001", {"serie": s(49)}, max_rupturas=2), servir("FX-BRK-001", {"serie": s(50)}, max_rupturas=2))
# FX-REGIME-001 · ≥ 100 observaciones
par("FX-REGIME-001 (100 observaciones)", servir("FX-REGIME-001", {"serie": x(99)}), servir("FX-REGIME-001", {"serie": x(100)}))
# FX-COINT-001 · ≥ 50 observaciones comunes
co = lambda n: (lambda z: {"series": {"y": [float(a) for a in 2 * z + rng.normal(0, 0.3, n)], "x": [float(a) for a in z]}})(np.cumsum(rng.normal(0, 1, n)))  # noqa: E731
par("FX-COINT-001 (50 observaciones)", servir("FX-COINT-001", co(49)), servir("FX-COINT-001", co(50)))
# TEM-DIFF-001 · ≥ 8 observaciones
td = lambda n: {"adopcion": [100 / (1 + np.exp(-0.8 * (a - 2016.5))) for a in range(2010, 2010 + n)], "anios": list(range(2010, 2010 + n))}  # noqa: E731
par("TEM-DIFF-001 (8 observaciones)", servir("TEM-DIFF-001", td(7), B=20), servir("TEM-DIFF-001", td(8), B=20))
# ML-CAL-001 · ≥ 30 por horizonte
c0 = servicio.CASOS_CONTROL["ML-CAL-001"][0]["datos"][0]["valores"]


def mc(n):
    v_ = copy.deepcopy(c0)
    hz = v_["horizontes"]["H2"]
    for k in ("realizaciones", "predicciones", "referencia"):
        hz[k] = list(hz[k])[:n]
    hz["intervalos"]["inferior"], hz["intervalos"]["superior"] = list(hz["intervalos"]["inferior"])[:n], list(hz["intervalos"]["superior"])[:n]
    return v_


par("ML-CAL-001 (30 por horizonte)", servir("ML-CAL-001", mc(29)), servir("ML-CAL-001", mc(30)))
# SIM-MC-001 · rechazo sin semilla; n_trayectorias 1 000–1 000 000
d0 = servicio.CASOS_CONTROL["SIM-MC-001"][0]["datos"][0]["valores"]
K.comprobar("SIM-MC-001 sin semilla: rechazo", servir("SIM-MC-001", copy.deepcopy(d0), horizonte=5)["estado"] == "RECHAZADO")
par("SIM-MC-001 (1 000 trayectorias)", servir("SIM-MC-001", copy.deepcopy(d0), horizonte=5, semilla=1, n_trayectorias=998),
    servir("SIM-MC-001", copy.deepcopy(d0), horizonte=5, semilla=1, n_trayectorias=1000))
K.comprobar("SIM-MC-001 con 1 000 002 trayectorias: rechazo", servir("SIM-MC-001", copy.deepcopy(d0), horizonte=5, semilla=1, n_trayectorias=1_000_002)["estado"] == "RECHAZADO")
# BT-PBO-001 · S 8–20 par; T ≥ 4·S; N ≥ 2
pb = lambda N, T: {"rendimientos": {f"c{i}": x(T) for i in range(N)}}  # noqa: E731
par("BT-PBO-001 (T ≥ 4·S)", servir("BT-PBO-001", pb(4, 63), S=16), servir("BT-PBO-001", pb(4, 64), S=16))
par("BT-PBO-001 (N ≥ 2)", servir("BT-PBO-001", pb(1, 80), S=8), servir("BT-PBO-001", pb(2, 80), S=8))
K.comprobar("BT-PBO-001 con S impar o fuera de 8–20: rechazo", all(servir("BT-PBO-001", pb(4, 200), S=s_)["estado"] == "RECHAZADO" for s_ in (9, 6, 22)))
# FIR-CURVE-001 · ≥ 6 nodos
cu = servicio.CASOS_CONTROL["FIR-CURVE-001"][0]["datos"][0]["valores"]


def curva(n):
    v_ = copy.deepcopy(cu)
    v_["curva"]["plazos"], v_["curva"]["rendimientos"] = list(v_["curva"]["plazos"])[:n], list(v_["curva"]["rendimientos"])[:n]
    return v_


par("FIR-CURVE-001 (6 nodos)", servir("FIR-CURVE-001", curva(5)), servir("FIR-CURVE-001", curva(6)))
# ACC-ERP-001 · g_L entre r_f − 1 pp y r_f
e0 = servicio.CASOS_CONTROL["ACC-ERP-001"][0]["datos"][0]["valores"]
rf = e0["rf_nominal_10a"]["valor"]
par("ACC-ERP-001 (g_L en [r_f − 1 pp, r_f])", servir("ACC-ERP-001", copy.deepcopy(e0), g_L=rf - 1.01), servir("ACC-ERP-001", copy.deepcopy(e0), g_L=rf - 1.0))
K.comprobar("ACC-ERP-001 con g_L > r_f: rechazo", servir("ACC-ERP-001", copy.deepcopy(e0), g_L=rf + 0.01)["estado"] == "RECHAZADO")
# FIR-SPREAD-001 · recuperación 0,2–0,6
f0 = servicio.CASOS_CONTROL["FIR-SPREAD-001"][0]["datos"][0]["valores"]
par("FIR-SPREAD-001 (recuperación 0,2–0,6)", servir("FIR-SPREAD-001", copy.deepcopy(f0), recuperacion=0.19), servir("FIR-SPREAD-001", copy.deepcopy(f0), recuperacion=0.2))
# CMD-INV-001 · anos_estacional 3–10
i0 = servicio.CASOS_CONTROL["CMD-INV-001"][0]["datos"][0]["valores"]
par("CMD-INV-001 (anos_estacional 3–10)", servir("CMD-INV-001", copy.deepcopy(i0), anos_estacional=2), servir("CMD-INV-001", copy.deepcopy(i0), anos_estacional=3))
sys.exit(K.fin())
