"""T-66 · QA r01 · PA-03: n_eff con fechas repetidas, pocas fechas, fechas ausentes o raras, residuos constantes;
determinismo del bootstrap por fechas; certificación de extremo a extremo con muestra correlacionada."""
import math
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from r01_comun import cfg, comprobar, fin

from bloque_a.almacen import Almacen
from bloque_a.evaluador import Evaluador
from bloque_a.motor import evaluacion as ev

AS_OF = "2026-01-02"
rng = np.random.default_rng(7)

# 1 · Todas las observaciones en la misma fecha: n_eff = 1
r = ev.n_efectiva(["2025-01-02"] * 200, rng.normal(size=200))
comprobar("una sola fecha: n_eff = 1", math.isclose(r["n_eff"], 1.0), f"{r['n_eff']}")

# 2 · Residuos constantes en cada fecha (dependencia total): n_eff = nº de fechas
f = [f"2025-01-{d:02d}" for d in range(1, 11) for _ in range(20)]
y = [float(d) for d in range(10) for _ in range(20)]
r = ev.n_efectiva(f, y)
comprobar("dependencia total dentro de la fecha: n_eff = 10 fechas", math.isclose(r["n_eff"], 10.0, rel_tol=1e-9), f"{r['n_eff']:.3f} ρ={r['rho']}")

# 3 · Residuos idénticos en todas partes (sin varianza): falla cerrado (ρ = 1)
r = ev.n_efectiva(f, [0.3] * 200)
comprobar("residuos sin varianza: ρ = 1 y n_eff = nº de fechas", r["rho"] == 1.0 and math.isclose(r["n_eff"], 10.0), f"{r['n_eff']}")

# 4 · Fechas independientes (una por observación): n_eff = n
r = ev.n_efectiva([str(pd.Timestamp("2025-01-01") + pd.Timedelta(days=i))[:10] for i in range(150)], rng.normal(size=150))
comprobar("una fecha por observación: n_eff = n", math.isclose(r["n_eff"], 150.0), f"{r['n_eff']}")

# 5 · Entradas raras: None, NaN, vacío, longitudes distintas, residuos infinitos
for nombre, fechas, res in (("fecha None", ["2025-01-01", None], [0.1, 0.2]), ("fecha NaN", ["2025-01-01", float("nan")], [0.1, 0.2]),
                            ("fecha vacía", ["2025-01-01", " "], [0.1, 0.2]), ("longitudes distintas", ["2025-01-01"], [0.1, 0.2]),
                            ("residuo infinito", ["2025-01-01", "2025-01-02"], [0.1, float("inf")]), ("fechas None", None, [0.1])):
    try:
        ev.n_efectiva(fechas, res)
        comprobar(f"n_eff con {nombre}: falla cerrado (ValueError)", False)
    except ValueError:
        comprobar(f"n_eff con {nombre}: falla cerrado (ValueError)", True)

# 6 · Bootstrap por fechas con pocas fechas: sin IC
p = rng.uniform(0.2, 0.8, 120)
o = (rng.random(120) < p).astype(int)
fechas = [f"2025-02-{(i % 5) + 1:02d}" for i in range(120)]
b = ev.bss_conglomerados(p, o, [0.5] * 120, fechas, 500, 0.9, 1, 10)
comprobar("5 fechas < 10: sin IC del BSS", b["ic"] == [None, None], b.get("nota", ""))
b10 = ev.bss_conglomerados(p, o, [0.5] * 120, [f"2025-02-{(i % 10) + 1:02d}" for i in range(120)], 500, 0.9, 1, 10)
b10b = ev.bss_conglomerados(p, o, [0.5] * 120, [f"2025-02-{(i % 10) + 1:02d}" for i in range(120)], 500, 0.9, 1, 10)
comprobar("10 fechas: IC calculado y determinista", b10["ic"][0] is not None and b10["ic"] == b10b["ic"], f"{b10['ic']}")

# 7 · Formatos de fecha distintos del mismo día cuentan como una sola fecha en el Evaluador
lst = [{"fecha_resolucion": "2025-07-02"}, {"fecha_resolucion": "2025-07-02T00:00:00"}, {"fecha_resolucion": "2025-07-02 18:30"}]
comprobar("mismo día con formatos distintos: un conglomerado", len(set(Evaluador._fechas_conglomerado(lst))) == 1,
          f"{Evaluador._fechas_conglomerado(lst)}")
comprobar("fecha ilegible: sin fechas (no certifica)", Evaluador._fechas_conglomerado([{"fecha_resolucion": "no es fecha"}]) is None)


# 8 · De extremo a extremo: 300 PRG hábiles en solo 12 fechas con un choque común por fecha → no certifica
def alta(a, pid, **c):
    base = {"tipo_entrada": "ALTA", "prg_id": pid, "opp_id": "OPP-1", "clase": "RF", "horizonte": "H3", "prob_interna": 0.65,
            "sentido": "POSITIVO", "en_informe": True, "fecha_emision": "2025-01-02", "referencia_ingenua": {"valor_o_prob": 0.5},
            "estado": "ABIERTO"}
    a.escribir("F4", "AG-10", {**base, **c})


def resolver(a, pid, o):
    a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                               "resolucion": {"resultado_binario": o, "comprobacion_fuga": "SUPERADA", "valor_observado": 0.01 if o else -0.01,
                                              "fecha_resuelto": "2025-12-31"}})


a = Almacen(Path(tempfile.mkdtemp(prefix="r01_neff_")))
a.reloj.fijar(AS_OF)
g = np.random.default_rng(3)
for i in range(300):
    d = i % 12
    choque = 1 if d % 2 == 0 else 0      # toda la fecha sale igual: 12 apuestas, no 300
    pp = 0.7 if choque else 0.3
    alta(a, f"PRG-2025-{i + 1:04d}", prob_interna=pp, fecha_resolucion=str((pd.Timestamp("2025-07-01") + pd.Timedelta(days=7 * d)).date()))
    resolver(a, f"PRG-2025-{i + 1:04d}", choque)
e = Evaluador(a, None, None, cfg(), None)
res = e.revisar_certificados(AS_OF)
crit = res["evaluadas"].get("RF|H3", {})
comprobar("300 PRG en 12 fechas perfectamente correlacionadas: no certifica por n_eff", not res["emitidos"]
          and any("n_eff" in m for m in crit.get("motivos", [])), f"{crit.get('motivos')}")

# 9 · El Evaluador no arranca con un mínimo de fechas inválido
for malo in (1, "10", True, 2.5):
    try:
        Evaluador(a, None, None, cfg(evaluacion={"min_conglomerados_bootstrap": malo}), None)
        comprobar(f"min_conglomerados_bootstrap={malo!r}: falla cerrado", False)
    except ValueError:
        comprobar(f"min_conglomerados_bootstrap={malo!r}: falla cerrado", True)
fin()
