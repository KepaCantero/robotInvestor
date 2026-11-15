"""QA r03 de T-94 · Adaptación de r02_10_coste_fuga_parametros.py al banco de la ronda r03 (sin tocar el original).
Cambios, y por qué: sin consumo.csv el banco se detiene ahora con BancoError (H-18, decisión de la ronda r03): se acepta como correcto.
En el punto 3, los parámetros fuera de cota tienen que dar BancoError.

Original:
QA r02 de T-94 · Coste (H-07), aviso de fuga (H-08) y parámetros de la línea de órdenes (H-10).

1. `leer_consumo` con celdas raras (NaN, inf, texto, negativos), sin fichero y con el coste estimado solo en algunas filas.
2. Fuga: titular falso con la advertencia «FUGA POR CONOCIMIENTO DEL MODELO» y un titular que sería «mejor» y otro «peor»;
   con un cliente que no es el simulado ninguna comparación es firme; con el simulado, sí (por diseño).
3. Parámetros: semilla negativa; remuestreos 1; nivel 0,01; min-efectivas 1 (¿se aceptan sin aviso?).
Titular falso y datos en un temporal; nunca se llama a ninguna API ni se escribe en el repositorio.
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r02_10_coste_fuga_parametros.py [<carpeta de banco_medida.py>]"""
import argparse
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

fallos = []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


TMP = Path(tempfile.mkdtemp(prefix="r02_t94_cf_"))
CAB = "run_id,llamadas,tokens_entrada,tokens_salida,tokens_cache_escritura,tokens_cache_lectura,uc,coste_estimado\n"

# 1. Coste
for nombre, fila in (("nan", "R1,1,nan,1,0,0,0.1,"), ("inf", "R1,1,inf,1,0,0,0.1,"), ("texto", "R1,1,muchos,1,0,0,0.1,"),
                     ("negativo", "R1,1,-500,1,0,0,0.1,"), ("coste nan", "R1,1,10,1,0,0,0.1,nan")):
    f = TMP / f"c_{nombre.replace(' ', '_')}.csv"
    f.write_text(CAB + fila + "\n", encoding="utf-8")
    try:
        c = bm.leer_consumo(f)
        bueno = all(v is None or (isinstance(v, (int, float)) and np.isfinite(v) and v >= 0) for k, v in c.items())
        ok(bueno, f"consumo con {nombre}: {c}")
    except bm.BancoError as e:
        ok(True, f"consumo con {nombre} → BancoError: {e}")
    except Exception as e:  # noqa: BLE001
        ok(False, f"consumo con {nombre} → {type(e).__name__}: {e} (no BancoError con motivo)")
try:
    c = bm.leer_consumo(TMP / "no_existe.csv")
    ok(c.get("llamadas") is None, f"sin consumo.csv el coste no se publica como cero llamadas medidas: {c}")
except bm.BancoError as e:
    ok(True, f"sin consumo.csv → BancoError: {e}")
f = TMP / "c_parcial.csv"
f.write_text(CAB + "R1,1,10,1,0,0,0.1,0.50\nR2,1,10,1,0,0,0.1,\n", encoding="utf-8")
c = bm.leer_consumo(f)
print(f"   coste estimado en una fila de dos: {c['coste_estimado']}")
ok(c["coste_estimado"] is None, "si alguna fila no trae coste estimado, el total no se presenta como completo")

# 2. Fuga
datos = TMP / "datos"
datos.mkdir()
fechas = pd.bdate_range("2023-01-02", "2026-06-30")
rng = np.random.default_rng(31)
sims = [f"S{i}" for i in range(10)]
precios = {}
for s in sims:
    v = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(fechas))))
    precios[s] = pd.Series(v, index=fechas)
    pd.DataFrame({"fecha": fechas.strftime("%Y-%m-%d"), "cierre": v}).to_csv(datos / f"{s}.csv", index=False)
universo = TMP / "universo.csv"
pd.DataFrame({"simbolo": sims, "clase": ["C"] * 10}).to_csv(universo, index=False)
CORTES = pd.date_range("2024-01-05", periods=40, freq="7D")


def titular(signo, advertencias):
    def f(desde, hasta, carpeta, cliente, frecuencia, clases, **kw):
        sel = []
        for c in CORTES:
            ret = {s: bm.rentabilidad(precios[s], c, c + pd.Timedelta(days=5)) for s in sims}
            mejor = max(ret, key=lambda s: signo * ret[s])            # con el futuro: lo que la fuga permitiría
            sel.append({"fecha_asof": c.strftime("%Y-%m-%d"), "clase": "C", "simbolo": mejor, "direccion": "LARGO", "horizonte": "H"})
        return {"selecciones": sel, "consumo": {"llamadas": 1, "tokens_entrada": 1, "tokens_salida": 1, "coste_estimado": None},
                "datos": datos, "universo": universo, "fecha_fin": lambda ini, h: ini + pd.Timedelta(days=5),
                "advertencias": advertencias, "excluidos_contaminacion": 3}
    return f


def ns(salida, cliente, **kw):
    d = dict(desde="2024-01-05", hasta="2024-10-04", salida=str(TMP / salida), cliente=cliente, frecuencia=None, clases=None,
             semilla=7, remuestreos=300, ventana=63, registro=None, experimento=None, max_variantes=1)
    d.update(kw)
    return argparse.Namespace(**d)


FUGA = [bm.AVISO_FUGA + ": el periodo empieza el 2024-01-05, antes de la fecha de corte configurada"]
for signo, nombre in ((1, "mejor"), (-1, "peor")):
    bm.titular_a = titular(signo, FUGA)
    inf = bm.ejecutar_a(ns(f"fuga_{nombre}", "anthropic"))
    vs = {k: (v["veredicto"], v["motivo"]) for k, v in inf["comparaciones"].items()}
    ok(all(v[0] == "todavía no se sabe" for v in vs.values()), f"fuga con cliente real y titular que sería «{nombre}»: {vs}")
    ok(any("apartó 3" in a for a in inf["advertencias_titular"]), "los pronósticos apartados por contaminación llegan a las advertencias")
    inf = bm.ejecutar_a(ns(f"fuga_{nombre}_mock", "mock"))
    print(f"   con el cliente simulado (sin fuga real): {[v['veredicto'] for v in inf['comparaciones'].values()]}")
bm.titular_a = titular(1, [])
inf = bm.ejecutar_a(ns("sin_fuga", "anthropic"))
ok(all(v["veredicto"] == "mejor" for v in inf["comparaciones"].values()), "sin advertencia de fuga, el titular con el futuro da «mejor»")

# 3. Parámetros
# (no se llama a main: ejecutaría A; se prueba ejecutar_a con el titular falso)
try:
    bm.ejecutar_a(ns("semneg", "mock", semilla=-3))
    ok(True, "semilla negativa aceptada y ejecutada")
except bm.BancoError as e:
    ok(True, f"semilla negativa → BancoError: {e}")
except Exception as e:  # noqa: BLE001
    ok(False, f"semilla negativa → {type(e).__name__}: {e} (el banco la admite al validar y falla después, sin motivo)")
bm.titular_a = titular(1, [])
for kw in ({"remuestreos": 1}, {"nivel": 0.01}, {"min_efectivas": 1}):
    try:
        inf = bm.ejecutar_a(ns("param", "mock", **kw))
        ok(False, f"{kw}: aceptado; comparaciones {[v['veredicto'] for v in inf['comparaciones'].values()]}")
    except bm.BancoError as e:
        ok(True, f"{kw}: BancoError {e}")

print(f"\n{len(fallos)} fallo(s)")
for f in fallos:
    print(" -", f)
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if fallos else 0)
