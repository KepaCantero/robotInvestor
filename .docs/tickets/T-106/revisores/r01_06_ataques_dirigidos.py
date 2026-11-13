"""QA r01 de T-106 · Ataques dirigidos (casos concretos que el fuzzer no construye).

1. IDX-REL-001 con historia diaria en vez de mensual: ¿lo rechaza o llama «12-1» a 12 sesiones?
2. MON-EXP-001 con un nodo exactamente a 12 meses: ¿calcula el cambio acumulado a 12 meses?
3. Fechas como enteros (epoch) en MON-YLD-001: ¿se aceptan en silencio como 1970-01-01?
4. Mensaje de rechazo de una ficha IMPLEMENTADO no servible por dependencia (VOL-GARCH-001 sin `arch`, simulado).
5. Rendimiento: 50 llamadas seguidas a cada ficha con sus datos nominales.

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r01_06_ataques_dirigidos.py [RAIZ]
"""
from __future__ import annotations

import copy
import sys
import tempfile
import time
import warnings
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

M = C.preparar(sys.argv[1] if len(sys.argv) > 1 else None)
S, ErrorFicha = M["servicio"], M["ErrorFicha"]
warnings.simplefilter("ignore")

# 1. IDX-REL diaria
caso = S.CASOS_CONTROL["IDX-REL-001"][1]
ent = C.entrada(caso)
fechas = pd.bdate_range("2010-01-01", periods=len(ent["valores"]["indice_a"]["historia"]))
for ix in ("indice_a", "indice_b"):
    for h, f in zip(ent["valores"][ix]["historia"], fechas):
        h["fecha"] = f.date().isoformat()
# ampliar a > 10 años de sesiones repitiendo el patrón
for ix in ("indice_a", "indice_b"):
    base = ent["valores"][ix]["historia"]
    hist = []
    fechas = pd.bdate_range("2010-01-01", periods=11 * 261)
    for j, f in enumerate(fechas):
        h = dict(base[j % len(base)])
        h["fecha"] = f.date().isoformat()
        hist.append(h)
    ent["valores"][ix]["historia"] = hist
try:
    r, lim = S.IMPLEMENTADAS["IDX-REL-001"]["fn"](ent, dict(caso["parametros"]))
    ok, det = False, f"servido con historia DIARIA: momentum {r['momentum_relativo']} (las «12-1» son 12 sesiones)"
except ErrorFicha as e:
    ok, det = True, str(e)[:120]
C.informe("IDX-REL-001 rechaza una historia que no es mensual", ok, det)

# 2. MON-EXP con nodo a 12 meses
caso = S.CASOS_CONTROL["MON-EXP-001"][0]
r, lim = S.IMPLEMENTADAS["MON-EXP-001"]["fn"](C.entrada(caso), {})
C.informe("MON-EXP-001: con un nodo a 365 días (12 meses), el cambio acumulado a 12 meses se calcula",
          r["cambio_acumulado_pb"].get("12m") is not None, f"{r['cambio_acumulado_pb']} · {[x for x in lim if '12' in x]}")

# 3. fechas epoch
caso = S.CASOS_CONTROL["MON-YLD-001"][1]
ent = C.entrada(caso)
ent["valores"]["segmentos"][0]["fecha"] = 20261110
try:
    r, _ = S.IMPLEMENTADAS["MON-YLD-001"]["fn"](ent, {})
    ok, det = False, f"fecha 20261110 aceptada como {next(iter(r['tabla'].values()))['fecha']}"
except ErrorFicha as e:
    ok, det = True, str(e)[:100]
C.informe("MON-YLD-001 rechaza una fecha numérica (no la convierte en epoch)", ok, det)

# 4. mensaje de rechazo de GARCH sin arch
orig = S.garch_disponible
S.garch_disponible = lambda: False
try:
    mo = C.motor(tempfile.mkdtemp())
    r = mo.servir({"operacion": "VOL-GARCH-001", "datos": [], "fecha_corte": "2026-11-12"}, "AG-21")
finally:
    S.garch_disponible = orig
C.informe("VOL-GARCH-001 sin `arch`: el detalle no dice que el Catálogo la da por «Documentado»",
          "Documentado" not in r["detalle"], r["detalle"][:120])

# 5. rendimiento
lento = []
for f in sorted(S.CASOS_CONTROL):
    caso = S.CASOS_CONTROL[f][0]
    ent = C.entrada(caso)
    t0 = time.perf_counter()
    for _ in range(50):
        S.IMPLEMENTADAS[f]["fn"](copy.deepcopy(ent), dict(caso.get("parametros") or {}))
    dt = (time.perf_counter() - t0) / 50
    if dt > 0.5:
        lento.append(f"{f}: {dt:.2f} s")
    print(f"      {f}: {dt * 1000:.1f} ms por llamada")
C.informe("cada ficha < 0,5 s por llamada con sus datos nominales", not lento, "; ".join(lento))
sys.exit(C.resumen())
