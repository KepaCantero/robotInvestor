"""QA r02 de T-94 · Reutilización del experimento en el registro (H-04) y la orden `verificar`.

Titular falso y rápido (se sustituye `titular_a`) sobre datos construidos en un temporal; registro y salidas en el temporal,
nunca en el repositorio.
1. Reutilización: misma hipótesis y periodo con el cliente simulado y después con otro cliente u otros datos → ¿el mismo
   experimento? ¿Queda la ejecución «de verdad» fuera del máximo por una prueba de tubería anterior?
2. Periodo desplazado un día (mismas fechas de corte efectivas): ¿experimento nuevo y adoptable? ¿Avisa el informe de que ya
   hay otro experimento con la misma hipótesis (con exactamente uno previo)?
3. `verificar` frente a reescrituras: informe.json con el veredicto cambiado y experimento.json borrado; informe.md cambiado;
   prerregistro.json o informe.json que faltan; experimento.json dañado o sin claves; registro ajeno o roto.
4. Una ejecución que falla con los mismos parámetros que una anterior buena: ¿qué dice `verificar` de la carpeta?
5. --experimento inexistente o registro roto: ¿«banco de medida detenido» con el motivo, o una traza?
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r02_11_registro_y_verificar.py [<carpeta de banco_medida.py>]"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm
import registro_experimentos as rx

fallos = []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


TMP = Path(tempfile.mkdtemp(prefix="r02_t94_reg_"))
datos = TMP / "datos"
datos.mkdir()
fechas = pd.bdate_range("2023-01-02", "2026-06-30")
rng = np.random.default_rng(21)
sims = [f"S{i}" for i in range(10)]
for s in sims:
    pd.DataFrame({"fecha": fechas.strftime("%Y-%m-%d"),
                  "cierre": 100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(fechas))))}).to_csv(datos / f"{s}.csv", index=False)
universo = TMP / "universo.csv"
pd.DataFrame({"simbolo": sims, "clase": ["C"] * 10}).to_csv(universo, index=False)
CORTES = [d.strftime("%Y-%m-%d") for d in pd.date_range("2024-01-05", periods=60, freq="7D")]
ADVERTENCIAS: list[str] = []


def titular_falso(desde, hasta, carpeta, cliente, frecuencia, clases, **kw):
    sel = [{"fecha_asof": c, "clase": "C", "simbolo": sims[i % 10], "direccion": "LARGO", "horizonte": "H"} for i, c in enumerate(CORTES)]
    return {"selecciones": sel, "consumo": {"llamadas": 1, "tokens_entrada": 1, "tokens_salida": 1, "coste_estimado": None},
            "datos": datos, "universo": universo, "fecha_fin": lambda ini, h: ini + pd.Timedelta(days=5),
            "advertencias": list(ADVERTENCIAS), "excluidos_contaminacion": 0}


bm.titular_a = titular_falso


def ns(salida, registro, **kw):
    d = dict(desde="2024-01-05", hasta="2025-02-21", salida=str(TMP / salida), cliente="mock", frecuencia=None, clases=None,
             semilla=7, remuestreos=200, ventana=63, registro=str(registro), experimento=None, max_variantes=1)
    d.update(kw)
    return argparse.Namespace(**d)


# 1. Reutilización con cliente y datos distintos
reg = TMP / "reg1.jsonl"
bm.ejecutar_a(ns("prueba_tuberia", reg))                                       # prueba de tubería: mock, datos de ejemplo
inf = bm.ejecutar_a(ns("de_verdad", reg, cliente="anthropic", datos=str(datos), universo=str(universo)))
R = rx.Registro(reg)
exps = sorted({x["exp_id"] for x in R.anotaciones() if x["tipo"] == "PRERREGISTRO"})
res = R.resumen(exps[0])
print(f"   mock y después «anthropic» con otros datos: {len(exps)} experimento(s); intentos {res['intentos']}, "
      f"fuera del máximo {res['fuera_del_maximo']}; datos del prerregistro del registro: «{R.experimento(exps[0])['prerregistro']['contenido']['datos'][:60]}…»")
ok(len(exps) == 2 or res["fuera_del_maximo"] == [],
   "una prueba de tubería con el cliente simulado no consume la variante del experimento con otro cliente y otros datos")

# 2. Periodo desplazado un día
reg = TMP / "reg2.jsonl"
a1 = bm.ejecutar_a(ns("p1", reg, desde="2024-01-05"))
a2 = bm.ejecutar_a(ns("p2", reg, desde="2024-01-04"))
R = rx.Registro(reg)
print(f"   desde 2024-01-05 y desde 2024-01-04 (mismos cortes): {a1['experimento']['exp_id']} y {a2['experimento']['exp_id']}; "
      f"adoptables {[R.resumen(e)['adoptable'] for e in (a1['experimento']['exp_id'], a2['experimento']['exp_id'])]}; "
      f"veredictos {[R.resumen(e)['veredictos'] for e in (a1['experimento']['exp_id'], a2['experimento']['exp_id'])]}")
ok(any("misma hipótesis" in x for x in a2["advertencias_titular"]),
   "con un experimento previo de la misma hipótesis (otro periodo), el informe del nuevo lo avisa")
a3 = bm.ejecutar_a(ns("p3", reg, desde="2024-01-03"))
aviso3 = next((x for x in a3["advertencias_titular"] if "misma hipótesis" in x), "")
print(f"   con dos previos: «{aviso3}» (hay 3 experimentos con esa hipótesis en el registro)")
ok("3 experimentos" in aviso3, "el aviso cuenta bien los experimentos con la misma hipótesis (incluido el nuevo)")

# 2b. Escapar del máximo de variantes desplazando el periodo un día: un titular con algo de habilidad (acierta el mejor
# activo de la semana el 20 % de las veces) da «todavía no se sabe» al 90 % y «mejor» al 70 %.
import random  # noqa: E402

PRECIOS = {s: pd.read_csv(datos / f"{s}.csv", index_col="fecha", parse_dates=True)["cierre"] for s in sims}


def titular_con_algo(desde, hasta, carpeta, cliente, frecuencia, clases, **kw):
    r, sel = random.Random(5), []
    for c in pd.date_range("2024-01-05", periods=60, freq="7D"):
        ret = {s: bm.rentabilidad(PRECIOS[s], c, c + pd.Timedelta(days=5)) for s in sims}
        s = max(ret, key=ret.get) if r.random() < 0.2 else r.choice(sims)
        sel.append({"fecha_asof": c.strftime("%Y-%m-%d"), "clase": "C", "simbolo": s, "direccion": "LARGO", "horizonte": "H"})
    return {**titular_falso(desde, hasta, carpeta, cliente, frecuencia, clases), "selecciones": sel}


bm.titular_a = titular_con_algo
reg = TMP / "reg2b.jsonl"
b1 = bm.ejecutar_a(ns("b1", reg, remuestreos=500, nivel=0.9))
b2 = bm.ejecutar_a(ns("b2", reg, remuestreos=500, nivel=0.7))
b3 = bm.ejecutar_a(ns("b3", reg, remuestreos=500, nivel=0.7, desde="2024-01-04"))
R = rx.Registro(reg)
for nombre, b in (("90 %, periodo P", b1), ("70 %, periodo P", b2), ("70 %, P desde un día antes", b3)):
    e = b["experimento"]
    print(f"   {nombre}: {e['exp_id']} intento {e['intento']}, dentro del máximo {e['dentro_del_maximo']}, "
          f"conjunto «{bm.veredicto_conjunto(b['comparaciones'])}», adoptable {R.resumen(e['exp_id'])['adoptable']}, "
          f"avisos {[x for x in b['advertencias_titular'] if 'hipótesis' in x]}")
ok(not R.resumen(b3["experimento"]["exp_id"])["adoptable"] or any("hipótesis" in x for x in b3["advertencias_titular"]),
   "cambiar el nivel tras ver «todavía no se sabe» y desplazar el periodo un día no da un «mejor» adoptable sin ningún aviso")
bm.titular_a = titular_falso

# 3. verificar frente a reescrituras
reg = TMP / "reg3.jsonl"
bm.ejecutar_a(ns("v", reg))
v = TMP / "v"
ok(bm.verificar(v) == [] and bm.verificar(v, reg) == [], "carpeta recién escrita: verificar no ve problemas (sin y con --registro)")
original = {f: (v / f).read_bytes() for f in ("prerregistro.json", "informe.json", "informe.md", "experimento.json")}


def restaurar():
    for f, b in original.items():
        (v / f).write_bytes(b)


j = json.loads(original["informe.json"])
for c in j["comparaciones"].values():
    c["veredicto"] = "mejor"
(v / "informe.json").write_text(json.dumps(j, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
ok(bm.verificar(v) != [], "informe.json con el veredicto cambiado: verificar lo ve (con experimento.json)")
(v / "experimento.json").unlink()
p = bm.verificar(v)
r = subprocess.run([sys.executable, "-B", str(CARPETA / "banco_medida.py"), "verificar", str(v)], capture_output=True, text=True, check=False)
print(f"   veredicto cambiado y experimento.json borrado: verificar → {p}; orden: código {r.returncode}, «{r.stdout.strip()}»")
ok(p != [] and r.returncode != 0, "veredicto cambiado y experimento.json borrado: `verificar <carpeta>` (sin --registro) no dice que las huellas casan")
restaurar()
(v / "informe.md").write_text(original["informe.md"].decode("utf-8").replace("todavía no se sabe", "mejor"), encoding="utf-8")
ok(bm.verificar(v, reg) != [], "informe.md reescrito («mejor» donde decía «todavía no se sabe»): verificar lo ve")
restaurar()
for f in ("prerregistro.json", "informe.json"):
    (v / f).unlink()
    ok(bm.verificar(v) != [], f"falta {f}: verificar lo dice")
    restaurar()
for nombre, contenido in (("dañado", "{no es json"), ("sin intento", json.dumps({"exp_id": "EXP-2026-0001", "registro": str(reg)}))):
    (v / "experimento.json").write_text(contenido, encoding="utf-8")
    try:
        p = bm.verificar(v)
        ok(p != [], f"experimento.json {nombre}: verificar lo dice ({p})")
    except Exception as e:  # noqa: BLE001
        ok(False, f"experimento.json {nombre}: verificar revienta con {type(e).__name__}: {e} (en vez de decir el problema)")
    restaurar()
ajeno = TMP / "ajeno.jsonl"
bm.ejecutar_a(ns("otra", ajeno, semilla=8))                                     # otro registro, mismo EXP-…-0001
p = bm.verificar(v, ajeno)
ok(p != [], f"verificar contra un registro ajeno con el mismo identificador de experimento: {p}")
roto = TMP / "roto.jsonl"
lineas = reg.read_text(encoding="utf-8").splitlines()
roto.write_text("\n".join(lineas[:1] + [lineas[1].replace('"n": 1', '"n": 7')] + lineas[2:]) + "\n", encoding="utf-8")
p = bm.verificar(v, roto)
ok(any("registro" in x for x in p), f"registro roto: verificar lo dice ({p})")

# 4. Fallo con los mismos parámetros que una ejecución buena anterior
reg = TMP / "reg4.jsonl"
bm.ejecutar_a(ns("rep", reg))
bueno = bm.titular_a


def titular_que_falla(*a, **k):
    raise bm.BancoError("se cayó el proveedor de datos")


bm.titular_a = titular_que_falla
try:
    bm.ejecutar_a(ns("rep", reg))
except bm.BancoError:
    pass
bm.titular_a = bueno
p0, p1 = bm.verificar(TMP / "rep"), bm.verificar(TMP / "rep", reg)
print(f"   carpeta de una ejecución fallida que deja el informe de la anterior: sin --registro {p0}; con --registro {p1}")
ok(p0 != [], "una carpeta cuyo último intento falló no se da por verificada sin --registro (el informe es del intento anterior)")

# 5. Errores de la línea de órdenes
r = subprocess.run([sys.executable, "-B", str(CARPETA / "banco_medida.py"), "a", "--desde", "2024-01-05", "--hasta", "2025-02-21",
                    "--salida", str(TMP / "cli"), "--registro", str(TMP / "vacio.jsonl"), "--experimento", "EXP-2026-0099"],
                   capture_output=True, text=True, check=False)
ultima = (r.stderr.strip().splitlines() or [""])[-1]
print(f"   --experimento inexistente: código {r.returncode}; «{ultima[:120]}»")
ok(r.returncode == 2 and "detenido" in r.stderr, "--experimento inexistente: «banco de medida detenido» con el motivo (no una traza)")
r = subprocess.run([sys.executable, "-B", str(CARPETA / "banco_medida.py"), "a", "--desde", "2024-01-05", "--hasta", "2025-02-21",
                    "--salida", str(TMP / "cli2"), "--registro", str(roto)], capture_output=True, text=True, check=False)
ultima = (r.stderr.strip().splitlines() or [""])[-1]
print(f"   registro roto: código {r.returncode}; «{ultima[:120]}»")
ok(r.returncode == 2 and "detenido" in r.stderr, "registro roto: «banco de medida detenido» con el motivo (no una traza)")

print(f"\n{len(fallos)} fallo(s)")
for f in fallos:
    print(" -", f)
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if fallos else 0)
