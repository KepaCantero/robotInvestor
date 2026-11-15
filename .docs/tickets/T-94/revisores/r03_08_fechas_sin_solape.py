"""QA r03 de T-94 · La selección de fechas de corte sin solape (`fechas_sin_solape`, H-13) y cómo entra en el informe.

1. Horizontes mezclados en una fecha: manda la ventana más larga; con el orden de entrada barajado, la muestra no cambia.
2. Bordes de la ventana: la fecha que empieza el mismo día en que termina la anterior entra; un día antes, no.
3. Filas sin «fecha_fin» (por la API, como haría un contendiente B o C que no pase por `evaluar`): ¿falla cerrado o se
   tratan como ventanas de un día y vuelve el solape de H-13?
4. Referencias con fechas distintas de las del titular, o con una ventana más larga en la misma fecha: ¿entran en la muestra
   o en el veredicto?
5. Filas que no puntúan (NEUTRAL, repetidas, sin resolver) en una fecha de la muestra: ¿gastan su ventana? Una fecha de la
   muestra que solo tiene filas de ese tipo, ¿cuánto quita? Una H5 sin resolver al principio, ¿deja el banco sin muestra?
6. Lo que se pierde con el patrón de A (oportunidad NUEVA que sigue VIGENTE semanas): una apuesta abierta en una fecha fuera
   de la muestra y repetida en una fecha de la muestra no cuenta en ninguna de las dos; con referencias, ¿se pierden filas de
   forma distinta en el titular y en la referencia (azar con clases pequeñas, momento que repite su favorito)?
7. Fecha escrita con hora o con otro formato en filas que no pasan por `evaluar`.
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r03_08_fechas_sin_solape.py [<carpeta de banco_medida.py>]"""
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

fallos, notas = [], []
CONSUMO = {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0, "coste_estimado": None}


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


def nota(msg):
    print("NOTA  " + msg)
    notas.append(msg)


def fila(d, fin, exceso=0.01, resuelta=True, **kw):
    return {"fecha_asof": d, "fecha_corte": d, "fecha_fin": fin, "resuelta": resuelta, "exceso": exceso if resuelta else None, **kw}


# 1. Horizontes mezclados
filas = [fila("2026-01-01", "2026-01-08"), fila("2026-01-01", "2026-02-01"), fila("2026-01-08", "2026-01-15"),
         fila("2026-01-15", "2026-01-22"), fila("2026-02-01", "2026-02-08"), fila("2026-02-05", "2026-02-12")]
m = bm.fechas_sin_solape(filas)
print(f"   horizontes mezclados: {sorted(m)}")
ok(m == {"2026-01-01", "2026-02-01"}, "con H corto y H largo en la misma fecha manda la ventana más larga")
for k in range(20):
    b = filas[:]
    random.Random(k).shuffle(b)
    if bm.fechas_sin_solape(b) != m:
        ok(False, f"el orden de entrada cambia la muestra (barajado {k})")
        break
else:
    ok(True, "20 órdenes de entrada barajados dan la misma muestra")

# 2. Bordes
m = bm.fechas_sin_solape([fila("2026-01-01", "2026-01-10"), fila("2026-01-10", "2026-01-20")])
ok(m == {"2026-01-01", "2026-01-10"}, "la fecha que empieza el día en que termina la anterior entra (comparten solo el cierre)")
m = bm.fechas_sin_solape([fila("2026-01-01", "2026-01-10"), fila("2026-01-09", "2026-01-20")])
ok(m == {"2026-01-01"}, "la fecha que empieza un día antes del fin de la anterior no entra")

# 3. Filas sin fecha_fin: 30 fechas consecutivas cuyas ventanas (por el horizonte que traen) se solapan
sin_fin = [{"fecha_asof": d.strftime("%Y-%m-%d"), "horizonte": "H3", "resuelta": True, "exceso": 0.01}
           for d in pd.date_range("2026-01-05", periods=30, freq="7D")]
try:
    m = bm.fechas_sin_solape(sin_fin)
    print(f"   30 fechas semanales con horizonte H3 y sin fecha_fin: {len(m)} en la muestra")
    ok(len(m) < 30, "filas sin fecha_fin no cuentan como ventanas de un día (o el banco se detiene con el motivo)")
    inf = bm.construir_informe({"titular": sin_fin, "azar": [dict(x, exceso=-0.01) for x in sin_fin]}, CONSUMO, 200, 1, None, "h")
    print(f"   construir_informe con esas filas: efectivas {inf['contendientes']['titular']['efectivas']}, "
          f"veredicto {inf['comparaciones']['titular_vs_azar']['veredicto']}")
except bm.BancoError as e:
    ok(True, f"filas sin fecha_fin → BancoError: {e}")
except Exception as e:  # noqa: BLE001
    ok(False, f"filas sin fecha_fin → {type(e).__name__}: {e} (sin motivo)")

# 4. Referencias con fechas o ventanas distintas de las del titular
tit = [fila(d.strftime("%Y-%m-%d"), (d + pd.Timedelta(days=7)).strftime("%Y-%m-%d"), 0.0)
       for d in pd.date_range("2026-01-05", periods=12, freq="7D")]
ref_otras = [fila(d.strftime("%Y-%m-%d"), (d + pd.Timedelta(days=7)).strftime("%Y-%m-%d"), -0.05)
             for d in pd.date_range("2026-01-06", periods=12, freq="7D")]          # un día después: ninguna fecha común
inf = bm.construir_informe({"titular": tit, "azar": ref_otras}, CONSUMO, 200, 1, None, "h")
c = inf["comparaciones"]["titular_vs_azar"]
print(f"   referencia sin ninguna fecha común: azar fuera de muestra {inf['contendientes']['azar']['fuera_de_muestra']}, "
      f"veredicto «{c['veredicto']}»")
ok(c["veredicto"] in ("sin datos", "todavía no se sabe") and inf["contendientes"]["azar"]["resueltas"] == 0,
   "una referencia con otras fechas de corte no entra en la comparación")
ref_larga = [dict(x, fecha_fin=(pd.Timestamp(x["fecha_asof"]) + pd.Timedelta(days=60)).strftime("%Y-%m-%d"), exceso=-0.05) for x in tit]
inf = bm.construir_informe({"titular": tit, "azar": ref_larga}, CONSUMO, 200, 1, None, "h")
c = inf["comparaciones"]["titular_vs_azar"]
print(f"   referencia con ventanas de 60 días en las fechas del titular (de 7): efectivas {c['efectivas']}, «{c['veredicto']}»")
if c["efectivas"][1] >= 10:
    nota("la muestra se calcula solo con las ventanas del titular: una referencia que llegue por la API con ventanas más "
         "largas en las mismas fechas entra con sus fechas solapadas como independientes. Con azar y momento no pasa (copian "
         "el horizonte del titular y pasan por el mismo `evaluar`), pero B o C conectados como referencia sí podrían")

# 5. Filas que no puntúan gastan ventana
dias = pd.date_range("2026-01-05", periods=60, freq="7D")
base = [fila(d.strftime("%Y-%m-%d"), (d + pd.Timedelta(days=7)).strftime("%Y-%m-%d")) for d in dias]
m0 = bm.fechas_sin_solape(base)
con_neutral = base + [fila(dias[0].strftime("%Y-%m-%d"), (dias[0] + pd.Timedelta(days=182)).strftime("%Y-%m-%d"),
                           resuelta=False, direccion="NEUTRAL")]
m1 = bm.fechas_sin_solape(con_neutral)
print(f"   60 fechas con ventanas de 7 días: {len(m0)} en la muestra; con una NEUTRAL de 26 semanas en la primera: {len(m1)}")
if len(m1) < len(m0):
    nota(f"una fila NEUTRAL (que no se puntúa) en una fecha alarga su ventana y quita {len(m0) - len(m1)} fechas de la muestra")
con_h5 = base + [fila(dias[0].strftime("%Y-%m-%d"), "2036-01-05", resuelta=False)]
m2 = bm.fechas_sin_solape(con_h5)
print(f"   con una selección H5 (10 años) sin resolver en la primera fecha: {len(m2)} fecha(s) en la muestra")
if len(m2) <= 1:
    nota("una sola selección sin resolver de horizonte largo (H5, décadas) en la primera fecha deja la muestra en 1 fecha: "
         "el banco nunca da veredicto en ese periodo (falla cerrado, pero sin decir por qué en el informe)")

# 6. El patrón de A: oportunidades que siguen VIGENTES. Un titular que abre una apuesta NUEVA cada semana y la repite
#    mientras dura su ventana (26 semanas); azar con clases de 4 activos.
rng = np.random.default_rng(5)
fechas = pd.bdate_range("2023-01-02", "2029-12-31")
sims = [f"S{i}" for i in range(4)]
P = {s: pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(fechas)))), index=fechas) for s in sims}
U = pd.DataFrame({"simbolo": sims, "clase": ["C"] * 4})
finf = lambda ini, h: pd.Timestamp(ini) + pd.Timedelta(weeks=26)   # noqa: E731
cortes = pd.date_range("2024-01-05", periods=156, freq="7D")
pl, abiertas = [], []
for i, c in enumerate(cortes):
    abiertas = [(s, f) for s, f in abiertas if f > c]
    if i % 9 == 4:                                                     # una NUEVA cada 9 semanas, en semanas «impares»
        libres = [s for s in sims if s not in {x[0] for x in abiertas}]
        if libres:
            abiertas.append((libres[0], finf(c, "H")))
    for s, _ in abiertas:                                              # y sigue VIGENTE cada semana mientras dura
        pl.append({"fecha_asof": c.strftime("%Y-%m-%d"), "clase": "C", "simbolo": s, "direccion": "LARGO", "horizonte": "H"})
ev_t = bm.evaluar(pl, P, U, finf)
ev_a = bm.evaluar(bm.azar(pl, U, 3), P, U, finf)
ev_m = bm.evaluar(bm.momento(pl, U, P, 63), P, U, finf)
inf = bm.construir_informe({"titular": ev_t, "azar": ev_a, "momento": ev_m}, CONSUMO, 200, 1, None, "h")
nuevas = sum(1 for f in ev_t if not f["repetida"] and f["resuelta"])
print(f"   A-like: {len(pl)} filas, {nuevas} apuestas distintas resueltas; muestra de {len(inf['fechas_en_muestra'])} fechas")
for n in ("titular", "azar", "momento"):
    r = inf["contendientes"][n]
    print(f"     {n}: resueltas en la muestra {r['resueltas']}, fechas efectivas {r['efectivas']}, repetidas {r['repetidas']}")
t, a = inf["contendientes"]["titular"], inf["contendientes"]["azar"]
if t["resueltas"] == 0 and nuevas > 0:
    nota("con el patrón de A (apuesta NUEVA fuera de las fechas de la muestra y VIGENTE después), el titular no tiene ninguna "
         "selección puntuada en la muestra: en las fechas de la muestra todas sus filas son «repetidas» de apuestas abiertas "
         "fuera de ella, que tampoco cuentan. Se pierden todas sus apuestas")
if abs(t["resueltas"] - a["resueltas"]) > 0:
    nota(f"en las mismas fechas de la muestra, el titular puntúa {t['resueltas']} filas y azar {a['resueltas']}: la regla de "
         "repetidas se aplica con TODAS las fechas, también las de fuera de la muestra, y quita filas distintas a cada lado")
muestra = set(inf["fechas_en_muestra"])
rep_dentro = [f for f in ev_t if f["fecha_corte"] in muestra and f["repetida"]]
abiertas_fuera = {f["motivo"].rsplit(" ", 1)[-1] for f in rep_dentro}
print(f"   filas del titular repetidas en fechas de la muestra: {len(rep_dentro)}; abiertas en fechas fuera de la muestra: "
      f"{len(abiertas_fuera - muestra)}")
ok(not (rep_dentro and (abiertas_fuera - muestra)) or t["resueltas"] > 0,
   "una apuesta abierta fuera de la muestra y repetida dentro cuenta una vez (en la muestra) o el informe dice que se pierde")

# 7. Fecha con hora en filas que no pasan por evaluar
mx = bm.fechas_sin_solape([{"fecha_asof": "2026-01-05 00:00:00", "fecha_fin": "2026-01-12", "resuelta": True, "exceso": 0.0},
                           {"fecha_asof": "2026-01-05", "fecha_fin": "2026-01-12", "resuelta": True, "exceso": 0.0}])
ok(mx == {"2026-01-05"}, f"la misma fecha con y sin hora es una sola fecha de la muestra: {sorted(mx)}")
try:
    mf = bm.fechas_sin_solape([{"fecha_asof": "2026-01-05", "fecha_fin": "2026-1-20", "resuelta": True, "exceso": 0.0},
                               {"fecha_asof": "2026-01-12", "fecha_fin": "2026-01-19", "resuelta": True, "exceso": 0.0}])
    print(f"   fecha_fin «2026-1-20» (sin ceros): muestra {sorted(mf)}")
    ok(mf == {"2026-01-05"}, "una fecha_fin sin ceros a la izquierda no se compara como texto (o se rechaza)")
except bm.BancoError as e:
    ok(True, f"fecha_fin mal escrita → BancoError: {e}")

print(f"\n{len(fallos)} fallo(s), {len(notas)} nota(s)")
for f in fallos:
    print(" -", f)
sys.exit(1 if fallos else 0)
