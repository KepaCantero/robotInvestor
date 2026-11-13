"""QA r03 de T-106 · MON-EXP-001: la limitación nueva por redondeo (H-16) frente a un oráculo propio.

El revisor construye sendas escalonadas conocidas (tipo vigente + movimientos por reunión), calcula aparte la curva OIS
exacta en nodos dentro y fuera de las reuniones (capitalización diaria, Act/base: el modelo de la ficha), la redondea y la
manda por el Motor. Con la verdad conocida se mide, en cada reunión servida:

  - el error real de `probabilidades` (reparto del movimiento de esa reunión) y de `probabilidades_acumuladas` frente a las
    probabilidades verdaderas (mismo reparto binario, aplicado a los movimientos verdaderos);
  - si ese error queda dentro de `incertidumbre_probabilidad`, que la r03 publica como «cota del cambio de cada
    probabilidad por ese redondeo»;
  - si la limitación aparece siempre que alguna incertidumbre supera la tolerancia de la ficha (1e-10), y nunca sin ella.

Escenarios: redondeo a 1 pb y a 0,1 pb con `precision_cotizacion` declarada, y a 0,1 pb con la precisión implícita
(medio último dígito, que sin declarar solo admite la tolerancia de la ficha y se rechaza); nodos
cada 7–30 días; cinco a siete reuniones. Además, una cota propia (independiente del código) del movimiento por reunión:
la diferencia de dos tramos acumula el redondeo de ambos.

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r03_03_mon_exp_oraculo.py [RAIZ] [--n 300]
"""
from __future__ import annotations

import math
import shutil
import sys
import tempfile
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
M = C.preparar(args[0] if args else None)
S = M["servicio"]
N = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 300
warnings.simplefilter("ignore")
TMP = Path(tempfile.mkdtemp(prefix="qa_r03_t106_monexp_"))
MO = C.motor(TMP)
FECHA = pd.Timestamp("2026-11-12")
BASE, OFICIAL, DIF, DELTA = 365, 0.03, 0.0005, 0.0025
TOL = 1e-10


def reparto(x: float) -> dict[int, float]:
    """Reparto binario de la ficha sobre un movimiento con signo → {movimientos con signo: probabilidad}."""
    a = abs(x)
    n = math.floor(a)
    s = 1 if x >= 0 else -1
    out = {s * n: 1 - (a - n)}
    out[s * (n + 1)] = out.get(s * (n + 1), 0.0) + (a - n)
    return out


def publicado(p: dict) -> dict[int, float]:
    s = -1 if p["sentido"] == "bajada" else 1
    out: dict[int, float] = {}
    for k, v in p["movimientos"].items():
        out[s * int(k)] = out.get(s * int(k), 0.0) + float(v)
    return out


def dist(a: dict[int, float], b: dict[int, float]) -> float:
    return max(abs(a.get(k, 0.0) - b.get(k, 0.0)) for k in set(a) | set(b))


def curva_exacta(cortes_dias: list[int], tasas: list[float], dias: list[int]) -> list[float]:
    """Tipo simple Act/base de cada nodo: capitalización diaria de la senda (tramo k desde su reunión)."""
    out = []
    for d in dias:
        lg = 0.0
        for k, r in enumerate(tasas):
            ini, fin = cortes_dias[k], (cortes_dias[k + 1] if k + 1 < len(cortes_dias) else 10 ** 9)
            n = max(0, min(fin, d) - ini)
            lg += n * math.log1p(r / BASE)
        out.append(math.expm1(lg) * BASE / d)
    return out


rng = np.random.default_rng(20261113)
fuera_cota = {"probabilidades": [], "probabilidades_acumuladas": []}
max_ratio = {"probabilidades": 0.0, "probabilidades_acumuladas": 0.0}
lim_mal, servidos, rechazos, propia_mayor = [], 0, 0, 0
motivos: dict[str, int] = {}
for t in range(N):
    n_reu = int(rng.integers(5, 8))
    sep = rng.integers(35, 56, size=n_reu)
    dias_reu = list(np.cumsum(sep) + int(rng.integers(10, 35)))
    reuniones = [(FECHA + pd.Timedelta(days=int(d))).date().isoformat() for d in dias_reu]
    movs = rng.choice([-2, -1, -1, 0, 0, 0, 1, 1, 2], size=n_reu) + rng.choice([0, 0, 0.5, 0.3, -0.4], size=n_reu)
    r0 = OFICIAL - DIF
    tasas = [r0] + list(r0 + DELTA * np.cumsum(movs))
    d_fin = int(dias_reu[-1] + rng.integers(20, 60))
    paso = int(rng.integers(7, 31))
    dias = sorted(set(list(range(paso, d_fin, paso)) + [d_fin]))
    exactos = curva_exacta([0, *[int(d) for d in dias_reu]], tasas, dias)
    modo = ("1pb declarada", "0,1pb declarada", "0,1pb implícita")[t % 3]
    dec = 4 if modo.startswith("1pb") else 5
    redondeados = [round(x, dec) for x in exactos]
    valores = {"fecha": FECHA.date().isoformat(), "base_curva": BASE, "tipo_oficial": OFICIAL, "diferencial_estable": DIF,
               "reuniones": reuniones, "curva": [{"dias": d, "tipo": x} for d, x in zip(dias, redondeados)]}
    if modo.endswith("declarada"):
        valores["precision_cotizacion"] = 0.5 * 10 ** -dec
    r = MO.servir({"operacion": "MON-EXP-001", "datos": [{"valores": valores}], "parametros": {}, "fecha_corte": "2026-11-12"},
                  "AG-21")
    if r["estado"] == "RECHAZADO":
        rechazos += 1
        motivo = r["detalle"].split(":")[1].strip()[:40] if ":" in r["detalle"] else r["detalle"][:40]
        motivos[f"{modo} · {motivo}"] = motivos.get(f"{modo} · {motivo}", 0) + 1
        continue
    servidos += 1
    senda = r["resultado"]["senda"]
    inc = [s["incertidumbre_probabilidad"] for s in senda]
    tiene_lim = any("redondeo de las cotizaciones puede mover las probabilidades" in x for x in r["limitaciones"] or [])
    if tiene_lim != (max(inc) > TOL):
        lim_mal.append(f"t{t}: limitación {tiene_lim} con incertidumbre máx. {max(inc):.3g}")
    acum_verdad = list(np.cumsum(movs))
    for k, s in enumerate(senda):
        if k >= n_reu:
            break
        for clave, verdad in (("probabilidades", movs[k]), ("probabilidades_acumuladas", acum_verdad[k])):
            err = dist(publicado(s[clave]), reparto(float(verdad)))
            cota = s["incertidumbre_probabilidad"]
            if cota > 0:
                max_ratio[clave] = max(max_ratio[clave], err / cota)
            if err > cota + 1e-9:
                fuera_cota[clave].append(f"t{t} {modo} reunión {k + 1}: error {err:.3f} > cota {cota:.3f}")
        # cota propia del movimiento de la reunión k: |δ(r_k − r_{k−1})| ≤ cota_k + cota_{k−1} (el tramo 0 es exacto)
        propia = (s["incertidumbre_redondeo_pb"] + (senda[k - 1]["incertidumbre_redondeo_pb"] if k else 0.0)) / (DELTA * 10_000)
        if min(1.0, propia) > s["incertidumbre_probabilidad"] + 1e-12:
            propia_mayor += 1

print(f"      {N} sendas: {servidos} servidas, {rechazos} rechazadas; motivos de rechazo: {motivos}")
C.informe("hay sendas servidas con redondeo (si no, la prueba no dice nada)", servidos >= N // 10, f"{servidos}")
C.informe("la limitación por redondeo aparece si y solo si alguna incertidumbre supera la tolerancia de la ficha", not lim_mal,
          "; ".join(lim_mal[:4]))
C.informe("probabilidades_acumuladas: el error real queda dentro de incertidumbre_probabilidad",
          not fuera_cota["probabilidades_acumuladas"],
          f"{len(fuera_cota['probabilidades_acumuladas'])} reuniones fuera; máx. error/cota "
          f"{max_ratio['probabilidades_acumuladas']:.3f}; " + "; ".join(fuera_cota["probabilidades_acumuladas"][:3]))
C.informe("probabilidades (por reunión): el error real queda dentro de incertidumbre_probabilidad",
          not fuera_cota["probabilidades"],
          f"{len(fuera_cota['probabilidades'])} reuniones fuera; máx. error/cota {max_ratio['probabilidades']:.3f}; "
          + "; ".join(fuera_cota["probabilidades"][:3]))
print(f"      (informativo) reuniones en que la cota propia del movimiento de la reunión (cota_k + cota_k−1)/Δ supera la "
      f"publicada: {propia_mayor}")

shutil.rmtree(TMP, ignore_errors=True)
sys.exit(C.resumen())
