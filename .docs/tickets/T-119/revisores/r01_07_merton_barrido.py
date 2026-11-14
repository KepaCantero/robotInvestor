"""QA r01 de T-119 · FIR-CRED-001: barrido del sistema de Merton (robustez de las dos raíces anidadas).

Rejilla de E/D, σ_E, T y r (1 800 combinaciones) servida por `Motor.servir` con 10 componentes iguales salvo un factor de
escala (la escala no cambia DD ni PD). Para cada una: o se sirve y el (V, σ_V) implícito en la DD servida cumple el sistema
(comprobado por sustitución con una búsqueda propia por rejilla + `fsolve`), o se rechaza. Se cuenta cuántas combinaciones
plausibles se rechazan y por qué, y se busca una segunda solución del sistema (no unicidad) con arranques múltiples.
"""
import math
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import numpy as np  # noqa: E402
from scipy import optimize, stats  # noqa: E402

K = C.Contador("r01_07 barrido de Merton")
N = stats.norm.cdf


def sistema(x, E, sE, D, r, T):
    V, s = math.exp(x[0]), math.exp(x[1])
    d1 = (math.log(V / D) + (r + s * s / 2) * T) / (s * math.sqrt(T))
    return [(V * N(d1) - D * math.exp(-r * T) * N(d1 - s * math.sqrt(T))) / E - 1, N(d1) * s * V / (E * sE) - 1]


def soluciones(E, sE, D, r, T):
    out = []
    for v0 in (E + D * math.exp(-r * T), E + D, E * 1.01, 2 * (E + D)):
        for s0 in (sE * E / (E + D), sE, sE / 2, 0.01, sE * 0.01):
            try:
                sol, _, ier, _ = optimize.fsolve(sistema, [math.log(v0), math.log(s0)], args=(E, sE, D, r, T), full_output=True, xtol=1e-13)
            except (ValueError, OverflowError, ZeroDivisionError):
                continue
            try:
                res = max(abs(z) for z in sistema(sol, E, sE, D, r, T))
            except (ValueError, OverflowError, ZeroDivisionError):
                continue
            if res < 1e-9 and not any(abs(sol[0] - o[0]) < 1e-6 and abs(sol[1] - o[1]) < 1e-6 for o in out):
                out.append((sol[0], sol[1]))
    return [(math.exp(a), math.exp(b)) for a, b in out]


m = C.motor()
motivos, mal, dobles, servidas, n = Counter(), [], [], 0, 0
ejemplos = {}
for ed in (1e-4, 1e-3, 0.01, 0.05, 0.2, 1, 5, 100, 1e4):
    for sE in (0.01, 0.05, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0):
        for T in (0.01, 0.25, 1, 5, 30):
            for r in (-0.5, -0.02, 0.0, 0.05, 0.5):
                n += 1
                D = 100.0
                E = ed * D
                comps = [{"id": f"C{i}", "capitalizacion": E * (i + 1), "volatilidad_acciones": sE, "deuda_corto": D * (i + 1), "deuda_largo": 0.0}
                         for i in range(10)]
                v = {"fecha": "2026-06-30", "segmento": {"nombre": "s", "financiero": False, "cobertura": 1.0}, "r": r,
                     "diferencial_indice_pb": 100.0, "componentes": comps}
                x = C.servir(m, "FIR-CRED-001", v, {"T": T, "mu": "r"})
                sols = soluciones(E, sE, D, r, T)
                if len(sols) > 1:
                    dobles.append((ed, sE, T, r, sols))
                if x["estado"] == "RECHAZADO":
                    mot = x["detalle"].split("(")[0][:70] + ("(" + x["detalle"].split("(")[1][:28] if "(" in x["detalle"] else "")
                    motivos[mot] += 1
                    ejemplos.setdefault(mot, []).append((ed, sE, T, r, len(sols)))
                    continue
                servidas += 1
                dd = x["resultado"]["neutral_al_riesgo"]["dd"]["mediana"]
                if sols:
                    esperadas = [(math.log(V / D) + (r - s * s / 2) * T) / (s * math.sqrt(T)) for V, s in sols]
                    if min(abs(dd - e) for e in esperadas) > 1e-5 * max(1, abs(dd)):
                        mal.append((ed, sE, T, r, dd, esperadas))
print(f"{n} combinaciones: {servidas} servidas, {n - servidas} rechazadas")
for mot, c in motivos.most_common():
    con_sol = sum(1 for e in ejemplos[mot] if e[4] > 0)
    print(f"   {c:5d} × {mot} · con solución propia: {con_sol} · p. ej. (E/D, σ_E, T, r, nº sol.) {ejemplos[mot][:3]}")
K.comprobar("lo servido coincide con una solución propia del sistema", not mal, str(mal[:4]))
K.comprobar("el sistema no tiene dos soluciones en la rejilla (unicidad)", not dobles, str(dobles[:3]))
plaus = [(mot, e) for mot, es in ejemplos.items() for e in es if e[4] > 0 and 0.05 <= e[0] <= 100 and 0.05 <= e[1] <= 2 and 0.25 <= e[2] <= 5 and abs(e[3]) <= 0.05]
K.comprobar("ninguna combinación plausible con solución (E/D 0,05–100, σ_E 5–200 %, T 0,25–5, |r| ≤ 5 %) se rechaza", not plaus, str(plaus[:6]))
todas = [(mot, e) for mot, es in ejemplos.items() for e in es if e[4] > 0]
print(f"   rechazadas teniendo solución propia: {len(todas)}; p. ej. {todas[:6]}")
sys.exit(K.fin())
