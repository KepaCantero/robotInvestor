"""T-118 · Coste del servicio más caro que admiten las cotas del grupo R (H-10), medido por `Motor.servir` (dos pasadas).
Cada petición lleva sus datos y sus parámetros de tamaño en el máximo admitido.
Uso: cd bloque_a/11_Ejecutor && ../../.venv/bin/python ../../.docs/tickets/T-118/revisores/impl_costes_motor.py"""
import sys, time, tempfile
from pathlib import Path
import numpy as np, pandas as pd
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.motor import servicio
class Pv:
    as_of, nombre = None, "t118"
m = servicio.Motor(Almacen(Path(tempfile.mkdtemp(prefix="t118_"))), Pv(), cargar_config())
rng = np.random.default_rng(7)
def garch(n, s=1):
    g = np.random.default_rng(s); h = 1e-4; out = []
    for _ in range(n):
        e = np.sqrt(h) * g.standard_t(6) * np.sqrt(4/6); out.append(float(e)); h = 2e-6 + 0.08 * e * e + 0.9 * h
    return out
def t(nombre, ficha, valores, params):
    t0 = time.time()
    r = m.servir({"operacion": ficha, "datos": [{"valores": valores}], "parametros": params}, "AG-18")
    print(f"{time.time()-t0:7.1f} s  {nombre}: {r['estado']} {r.get('detalle', '')[:80]}", flush=True)
H = garch(2520)
for met in ("cornish_fisher", "historico_filtrado", "t"):
    t(f"BT-VAR-001 generado, historia 2520, ventana 250, {met}", "BT-VAR-001", {"rendimientos": H}, {"metodo_var": met, "nivel": 0.95})
t("BT-VAR-001 generado, historia 2520, ventana 500, evt_pot", "BT-VAR-001", {"rendimientos": H}, {"metodo_var": "evt_pot", "ventana_estimacion": 500, "nivel": 0.95})
M = {f"c{i:04d}": [float(e) for e in 0.01 * rng.standard_normal(2520)] for i in range(1000)}
t("BT-PBO-001 S 20, 1000 configuraciones × 2520", "BT-PBO-001", {"rendimientos": M}, {"S": 20})
D = garch(1_000_000, 3)
t("RISK-VAR-001 distribución de 1 000 000, historico_filtrado", "RISK-VAR-001", {"distribucion": {"semilla": 1, "rendimientos": D}}, {"metodo": "historico_filtrado", "nivel": 0.95})
n, k = 2520, 20
fechas = [str(d.date()) for d in pd.bdate_range("2010-01-01", periods=n)]
X = rng.standard_normal((n, k)); mov = 0.01 * np.r_[0.0, X[:-1, 0]] + 0.005 * rng.standard_normal(n)
serie = 100 * np.exp(np.cumsum(mov))
v = {"fechas": fechas, "objetivo": {"serie": [float(e) for e in serie], "horizonte": 1, "tipo": "direccion", "criterio_resolucion": "x"},
     "variables": {f"x{i:02d}": {"serie": [float(e) for e in X[:, i]], "conocible_desde": fechas} for i in range(k)}}
rej = [float(10 ** e) for e in np.linspace(-3, 3, 20)]
t("ML-PRED-001 2520 × 20 variables, 20 pliegues, rejilla 20, 10 000 réplicas", "ML-PRED-001", v, {"pliegues": 20, "rejilla": rej, "replicas": 10000})
hz = {f"H{i}": {"tipo": "nivel", "predicciones": [float(e) for e in rng.standard_normal(n)], "realizaciones": [float(e) for e in rng.standard_normal(n)],
                "regimenes": [f"r{j % 50}" for j in range(n)]} for i in range(1, 6)}
t("ML-CAL-001 5 horizontes × 2520, 10 000 réplicas", "ML-CAL-001", {"ensayos": 1, "horizontes": hz}, {"replicas": 10000})
t("DEC-VOI-001 1 000 000 muestras con verosimilitud y ranking", "DEC-VOI-001", {"puntuacion": {"dimension": "E", "actual": 58.0},
  "muestras": {"fuente": "x", "valores": [float(e) for e in 58 + 6 * rng.standard_normal(1_000_000)]},
  "verosimilitud": {"desviacion": 3.0}, "ranking": {"rk_opcion": 60, "rk_frontera": 62, "amplitud_rk": 5}}, {"coste_uc": 0.02})
t("SCN-H-001 1 000 000 trayectorias, 2520 rendimientos, 99 cuantiles", "SCN-H-001", {"rendimientos": H}, {"n_trayectorias": 1_000_000, "semilla": 1, "clase": "RV", "cuantiles": [i / 100 for i in range(1, 100)]})
t("SIM-MC-001 bootstrap filtrado 10 000 × 2520, residuos e historia 2520", "SIM-MC-001",
  {"dinamica": {"tipo": "bootstrap_filtrado", "mu": 0.0, "omega": 2e-6, "alpha": 0.08, "beta": 0.9, "residuos": [float(e) for e in rng.standard_normal(2520)]},
   "historia_rendimientos": H}, {"n_trayectorias": 10_000, "horizonte": 2520, "semilla": 1})
