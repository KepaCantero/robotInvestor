"""T-133 QA r01 · La muestra elegida antes de evaluar (H-24) y lo que el lector ve en informe.md.

Con la muestra elegida antes de evaluar, `ejecutar_a` pasa a `construir_informe` solo las selecciones de la muestra: la
columna «Fuera de muestra» del informe queda siempre en 0 y el total va a `inf["plantilla"]`. ¿Lo ve quien lee informe.md?
Además: una selección H5 sin resolver en la primera fecha (H-25 c) y el filtro con fechas con hora.
Uso: .venv/bin/python -B r01_06_muestra_en_el_informe.py [<carpeta de banco_medida.py>]"""
import argparse
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[4] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

fallos, notas = [], []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


TMP = Path(tempfile.mkdtemp(prefix="r01_t133_muestra_"))
datos = TMP / "datos"
datos.mkdir()
fechas = pd.bdate_range("2022-01-03", "2026-06-30")
rng = np.random.default_rng(9)
sims = [f"S{i}" for i in range(12)]
for s in sims:
    pd.DataFrame({"fecha": fechas.strftime("%Y-%m-%d"),
                  "cierre": 100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(fechas))))}).to_csv(datos / f"{s}.csv", index=False)
universo = TMP / "universo.csv"
pd.DataFrame({"simbolo": sims, "clase": ["C"] * 12}).to_csv(universo, index=False)
CORTES = pd.date_range("2023-01-06", periods=150, freq="7D")
SEL = {"v": []}


def titular(*a, **kw):
    return {"selecciones": SEL["v"], "consumo": {"llamadas": 1, "tokens_entrada": 1, "tokens_salida": 1, "coste_estimado": None},
            "datos": datos, "universo": universo, "fecha_fin": SEL["fin"], "advertencias": [], "excluidos_contaminacion": 0}


bm.titular_a = titular


def correr(nombre):
    ns = argparse.Namespace(desde="2023-01-06", hasta="2025-11-21", salida=str(TMP / nombre), cliente="mock", frecuencia=None,
                            clases=None, semilla=7, remuestreos=200, ventana=63, nivel=0.9, min_efectivas=10, registro=None,
                            experimento=None, max_variantes=1, datos=str(datos), universo=str(universo))
    inf = bm.ejecutar_a(ns)
    md = (TMP / nombre / "informe.md").read_text(encoding="utf-8")
    return inf, md


# 1. Patrón de A: dos oportunidades VIGENTES 26 semanas, horizonte de 13 semanas
v, act = [], [None, None]
for w, c in enumerate(CORTES):
    for j in (0, 1):
        if (w + 13 * j) % 26 == 0 or act[j] is None:
            act[j] = sims[(w + 5 * j) % 12]
        v.append({"fecha_asof": c.strftime("%Y-%m-%d"), "clase": "C", "simbolo": act[j], "direccion": "LARGO", "horizonte": "H3"})
SEL.update(v=v, fin=lambda ini, h: ini + pd.Timedelta(weeks=13))
inf, md = correr("a")
fila = next(x for x in md.splitlines() if x.startswith("| titular"))
print(f"   plantilla en informe.json: {inf['plantilla']}; fila del titular en informe.md: «{fila}»")
ok(str(inf["plantilla"]["selecciones"]) in md,
   "informe.md dice cuántas selecciones tenía el titular y cuántas quedaron fuera de la muestra (no «Fuera de muestra 0»)")

# 2. H5 sin resolver en la primera fecha
v2 = [dict(x) for x in v]
v2.insert(0, {"fecha_asof": CORTES[0].strftime("%Y-%m-%d"), "clase": "C", "simbolo": "S11", "direccion": "LARGO", "horizonte": "H5"})
SEL.update(v=v2, fin=lambda ini, h: ini + (pd.DateOffset(years=10) if h == "H5" else pd.Timedelta(weeks=13)))
inf2, md2 = correr("b")
print(f"   con una H5 sin resolver en la primera fecha: {len(inf2['fechas_en_muestra'])} fecha(s) en la muestra; "
      f"motivo {inf2['comparaciones']['titular_vs_azar']['motivo']!r}")
if len(inf2["fechas_en_muestra"]) < 10 and "H5" not in md2 and "ventana" not in (inf2["comparaciones"]["titular_vs_azar"]["motivo"] or ""):
    notas.append("una H5 sin resolver en la primera fecha deja la muestra en 1 fecha y el informe no dice por qué (H-25 c)")
    print("NOTA  " + notas[-1])

# 3. Fechas con hora en fecha_asof: el filtro previo normaliza como _fecha
v3 = [dict(x, fecha_asof=x["fecha_asof"] + " 18:00:00") for x in v]
SEL.update(v=v3, fin=lambda ini, h: ini + pd.Timedelta(weeks=13))
inf3, _ = correr("c")
ok(inf3["plantilla"]["en_muestra"] == inf["plantilla"]["en_muestra"] and inf3["fechas_en_muestra"] == inf["fechas_en_muestra"],
   "fechas de corte con hora: la misma muestra y las mismas selecciones dentro")

print()
print(f"{len(fallos)} fallo(s), {len(notas)} nota(s)")
for f in fallos:
    print(" - " + f)
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if fallos else 0)
