"""T-133 QA r01 · `huella_datos` y la fuente del experimento (H-21, H-22).

Titular falso (se sustituye `titular_a`), datos y registros en un temporal; nunca se escribe en el repositorio.
1. ¿La huella identifica los datos que lee A? A solo lee «<carpeta>/<símbolo>.csv» de los símbolos del universo
   (`ProveedorCSV` de HT-01): copia en otra carpeta, universo con otro nombre de fichero, un CSV que no está en el universo,
   un fichero que no es CSV, una subcarpeta, el orden de creación, un nombre en NFD, carpeta vacía o inexistente, un
   enlace simbólico y un fichero grande (memoria).
2. Consecuencia en el registro: con un titular que no es determinista (como A con un modelo real), ¿se puede volver a tirar
   en un experimento nuevo (con su variante libre y adoptable) cambiando algo que A no lee?
3. Lo que dice el README de T-133 (H-21): «unos datos cambiados son otra variante». ¿Lo son, o son otro experimento?
Uso: .venv/bin/python -B r01_01_huella_y_fuente.py [<carpeta de banco_medida.py>]"""
import argparse
import os
import random
import shutil
import sys
import tempfile
import tracemalloc
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[4] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm
import registro_experimentos as rx

fallos, notas = [], []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


def nota(msg):
    print("NOTA  " + msg)
    notas.append(msg)


TMP = Path(tempfile.mkdtemp(prefix="r01_t133_huella_"))
datos = TMP / "datos"
datos.mkdir()
fechas = pd.bdate_range("2023-01-02", "2026-06-30")
rng = np.random.default_rng(41)
sims = [f"S{i}" for i in range(10)]
for s in sims:
    pd.DataFrame({"fecha": fechas.strftime("%Y-%m-%d"),
                  "cierre": 100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(fechas))))}).to_csv(datos / f"{s}.csv", index=False)
universo = TMP / "universo.csv"
pd.DataFrame({"simbolo": sims, "clase": ["C"] * 10}).to_csv(universo, index=False)
H0, HU = bm.huella_datos(datos), bm.huella_datos(universo)


def copia(nombre, origen=datos):
    d = TMP / nombre
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(origen, d, symlinks=True)
    return d


# ---------------------------------------------------------------- 1. ¿Qué identifica la huella?
c = copia("copia")
ok(bm.huella_datos(c) == H0, "los mismos datos en otra carpeta dan la misma huella")
u2 = TMP / "otro_nombre.csv"
shutil.copy(universo, u2)
print(f"   universo idéntico con otro nombre: {bm.huella_datos(u2)[:16]} frente a {HU[:16]}")
ok(bm.huella_datos(u2) == HU, "el mismo universo con otro nombre de fichero da la misma huella (A no lee el nombre)")

c = copia("extra")
(c / "ZZZ_no_esta_en_el_universo.csv").write_text("fecha,cierre\n2024-01-02,1\n", encoding="utf-8")
ok(bm.huella_datos(c) == H0, "un CSV que no está en el universo (A no lo lee) no cambia la huella")
c = copia("txt")
(c / "LEEME.txt").write_text("notas\n", encoding="utf-8")
ok(bm.huella_datos(c) == H0, "un fichero que no es CSV no cambia la huella (A no lo lee)")
c = copia("sub")
(c / "sub").mkdir()
(c / "sub" / "S1.csv").write_text("fecha,cierre\n2024-01-02,1\n", encoding="utf-8")
ok(bm.huella_datos(c) == H0, "una subcarpeta no cambia la huella (A no la lee)")

c = TMP / "orden"
c.mkdir()
for s in reversed(sims):
    shutil.copy(datos / f"{s}.csv", c / f"{s}.csv")
ok(bm.huella_datos(c) == H0, "el orden en que se crean los ficheros no cambia la huella")

c = copia("mayus")
(c / "S1.csv").rename(c / "S1.CSV")
print(f"   S1.csv renombrado a S1.CSV (A ya no lo encuentra): huella distinta {bm.huella_datos(c) != H0}")
ok(bm.huella_datos(c) != H0, "un fichero que A deja de leer cambia la huella")

nfd_dir = TMP / "nfd"
nfd_dir.mkdir()
nfc_dir = TMP / "nfc"
nfc_dir.mkdir()
nombre = "ÍNDICE.csv"
(nfd_dir / unicodedata.normalize("NFD", nombre)).write_text("fecha,cierre\n2024-01-02,1\n", encoding="utf-8")
(nfc_dir / unicodedata.normalize("NFC", nombre)).write_text("fecha,cierre\n2024-01-02,1\n", encoding="utf-8")
if bm.huella_datos(nfd_dir) != bm.huella_datos(nfc_dir):
    nota("un nombre de fichero en NFD (macOS) y el mismo en NFC dan huellas distintas: los mismos datos extraídos en macOS "
         "son otra fuente (y A, en Linux, no encontraría el símbolo en NFC)")

for caso, ruta in (("carpeta vacía", TMP / "vacia"), ("ruta inexistente", TMP / "no_existe")):
    if caso == "carpeta vacía":
        ruta.mkdir()
    try:
        bm.huella_datos(ruta)
        ok(False, f"{caso}: falla cerrado")
    except bm.BancoError as e:
        ok(True, f"{caso}: falla cerrado ({e})")

fuera = TMP / "fuera"
fuera.mkdir()
shutil.copy(datos / "S1.csv", fuera / "S1.csv")
c = copia("enlace")
(c / "S1.csv").unlink()
os.symlink(fuera / "S1.csv", c / "S1.csv")
print(f"   S1.csv como enlace simbólico a un fichero de fuera: huella igual {bm.huella_datos(c) == H0} "
      "(A lo rechaza: «sale de la carpeta configurada»)")

grande = TMP / "grande"
grande.mkdir()
with open(grande / "G.csv", "wb") as fh:
    fh.write(b"fecha,cierre\n" + b"2024-01-02,1\n" * (16 * 1024 * 1024 // 13))
tracemalloc.start()
bm.huella_datos(grande)
pico = tracemalloc.get_traced_memory()[1]
tracemalloc.stop()
print(f"   fichero de 16 MiB: pico de memoria de huella_datos {pico / 2**20:.1f} MiB")
if pico > 8 * 2**20:
    nota(f"huella_datos lee cada fichero entero en memoria (pico {pico / 2**20:.0f} MiB con uno de 16 MiB): con datos de K de "
         "varios GiB puede quedarse sin memoria; leer por bloques")

# ---------------------------------------------------------------- 2. Volver a tirar con un titular no determinista
CORTES = pd.date_range("2024-01-05", periods=60, freq="7D")
PRECIOS = {s: pd.read_csv(datos / f"{s}.csv", index_col="fecha", parse_dates=True)["cierre"] for s in sims}
ESTADO = {"semilla_titular": 0, "datos": datos, "universo": universo}


def titular(desde, hasta, carpeta, cliente, frecuencia, clases, **kw):
    """Sin habilidad y no determinista: cada ejecución elige otro activo al azar en cada corte."""
    r = random.Random(ESTADO["semilla_titular"])
    sel = [{"fecha_asof": c.strftime("%Y-%m-%d"), "clase": "C", "simbolo": r.choice(sims), "direccion": "LARGO", "horizonte": "H"}
           for c in CORTES]
    return {"selecciones": sel, "consumo": {"llamadas": 1, "tokens_entrada": 1, "tokens_salida": 1, "coste_estimado": None},
            "datos": ESTADO["datos"], "universo": ESTADO["universo"],
            "fecha_fin": lambda ini, h: ini + pd.Timedelta(days=5), "advertencias": [], "excluidos_contaminacion": 0}


bm.titular_a = titular


def ns(salida, registro, **kw):
    d = {"desde": "2024-01-05", "hasta": "2025-02-21", "salida": str(TMP / salida), "cliente": "anthropic", "frecuencia": None,
             "clases": None, "semilla": 7, "remuestreos": 300, "ventana": 63, "nivel": 0.9, "min_efectivas": 10, "registro": str(registro),
             "experimento": None, "max_variantes": 1}
    d.update(kw)
    return argparse.Namespace(**d)


def tirar(reg, n, perturbar, parar_al_adoptar=False):
    filas = []
    for i in range(n):
        ESTADO["semilla_titular"] = 1000 + i
        d = datos
        if perturbar:
            d = copia(f"tirada_{i}")
            (d / f"relleno_{i}.csv").write_text("fecha,cierre\n2024-01-02,1\n", encoding="utf-8")   # A no lo lee
        ESTADO["datos"] = d
        inf = bm.ejecutar_a(ns(f"t{int(perturbar)}_{i}", reg, datos=str(d), universo=str(universo)))
        e = inf["experimento"]
        r = rx.Registro(reg)
        filas.append((i + 1, e["exp_id"], e["dentro_del_maximo"],
                      {k: v["veredicto"] for k, v in inf["comparaciones"].items()}, r.adoptable(e["exp_id"]),
                      any("experimento(s) más" in a for a in inf["advertencias_titular"])))
        if parar_al_adoptar and filas[-1][4]:
            break
    return filas


# Se busca una semilla del titular que dé «mejor» frente a las dos referencias (sin habilidad: pasa por azar)
reg_a = TMP / "reg_mismos.jsonl"
reg_b = TMP / "reg_perturbados.jsonl"
N = 40
mismos = tirar(reg_a, N, False)
perturbados = tirar(reg_b, 300, True, parar_al_adoptar=True)
adopt_a = [f for f in mismos if f[4]]
adopt_b = [f for f in perturbados if f[4]]
exps_b = {f[1] for f in perturbados}
print(f"   {N} tiradas con los mismos datos: experimentos {len({f[1] for f in mismos})}, dentro del máximo "
      f"{sum(f[2] for f in mismos)}, adoptables {len(adopt_a)}")
print(f"   {len(perturbados)} tiradas (hasta la primera adoptable, máximo 300) con un CSV de relleno que A no lee: experimentos {len(exps_b)}, dentro del máximo "
      f"{sum(f[2] for f in perturbados)}, tiradas con algún «mejor» {sum('mejor' in f[3].values() for f in perturbados)}, "
      f"experimentos adoptables {len(adopt_b)} {[(f[0], f[1]) for f in adopt_b][:3]}; con la advertencia de «otra fuente» "
      f"en el informe {sum(f[5] for f in perturbados)}")
ok(not adopt_a, "repetir la misma variante con los mismos datos no la hace adoptable (regla de T-99)")
ok(len(exps_b) == 1,
   "cambiar algo que A no lee (un CSV que no está en el universo) no abre un experimento nuevo con su variante libre")
if adopt_b:
    print("   → con un titular sin habilidad, volver a tirar con un relleno distinto cada vez acaba en un experimento adoptable")

# ---------------------------------------------------------------- 3. Datos cambiados: ¿otra variante u otro experimento?
reg_c = TMP / "reg_cambiados.jsonl"
ESTADO.update(semilla_titular=5, datos=datos)
x1 = bm.ejecutar_a(ns("c1", reg_c, datos=str(datos), universo=str(universo)))
d2 = copia("cambiados")
texto = (d2 / "S3.csv").read_text(encoding="utf-8").splitlines()
texto[-1] = texto[-1].rsplit(",", 1)[0] + ",123.0"
(d2 / "S3.csv").write_text("\n".join(texto) + "\n", encoding="utf-8")
ESTADO["datos"] = d2
x2 = bm.ejecutar_a(ns("c2", reg_c, datos=str(d2), universo=str(universo)))
print(f"   datos originales: {x1['experimento']['exp_id']}; un cierre cambiado: {x2['experimento']['exp_id']} "
      f"(dentro del máximo {x2['experimento']['dentro_del_maximo']})")
ok(x1["experimento"]["exp_id"] == x2["experimento"]["exp_id"] and not x2["experimento"]["dentro_del_maximo"],
   "unos datos cambiados son otra variante del mismo experimento (lo que dice el README de T-133 para H-21), fuera del máximo")

print()
print(f"{len(fallos)} fallo(s), {len(notas)} nota(s)")
for f in fallos:
    print(" - " + f)
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if fallos else 0)
