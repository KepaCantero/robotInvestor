"""T-133 QA r02 · La huella de «solo lo que lee A» (banco 0.5.0, r02 H-01 y H-09).

Adapta r01_01 a la firma nueva (`huella_datos(carpeta, simbolos)`) y ataca lo nuevo:
1. API: un CSV fuera del universo, un cierre cambiado, el universo con otro nombre, filas en otro orden, BOM, CRLF,
   columnas de más; un símbolo que cambia de clase; columnas del universo que A sí lee (nombre, tipo_opcion, ámbito,
   indicador, subyacente).
2. Lo que A lee además de los CSV de los símbolos del universo: `indices_referencia` de su configuración y la columna
   «subyacente» del universo (código de A; el cliente simulado solo analiza DIV y no llega a leerlos).
3. Con A de verdad (cliente simulado, `titular_a`): ¿cambiar solo columnas del universo que la huella no recoge cambia lo
   que entrega A? ¿Y unos datos con CRLF o con BOM (mismos números, otros bytes)?
Todo va a un temporal; nunca se escribe en el repositorio. Uso:
  .venv/bin/python -B r02_01_huella_lo_que_lee_a.py <carpeta de banco_medida.py> [--sin-a]"""
import hashlib
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

fallos, notas = [], []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg, flush=True)
    if not cond:
        fallos.append(msg)


def nota(msg):
    print("NOTA  " + msg, flush=True)
    notas.append(msg)


TMP = Path(tempfile.mkdtemp(prefix="r02_t133_huella_"))
datos = TMP / "datos"
datos.mkdir()
fechas = pd.bdate_range("2023-01-02", "2026-06-30")
rng = np.random.default_rng(5)
sims = [f"S{i}" for i in range(6)]
for s in sims + ["REF"]:
    pd.DataFrame({"fecha": fechas.strftime("%Y-%m-%d"),
                  "cierre": 100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(fechas))))}).to_csv(datos / f"{s}.csv", index=False)
universo = TMP / "universo.csv"
pd.DataFrame({"simbolo": sims, "clase": ["RV"] * 6, "nombre": [f"n{s}" for s in sims], "tipo_opcion": ["SECTOR"] * 6,
              "subyacente": ["REF"] + [""] * 5}).to_csv(universo, index=False)


def hd(d, u=universo):
    return bm.huella_datos(d, bm._simbolos_del_universo(u))


H0, HU = hd(datos), bm.huella_datos(universo)


def copia(nombre):
    d = TMP / nombre
    shutil.copytree(datos, d)
    return d


def universo_con(nombre, f):
    df = pd.read_csv(universo, dtype=str, keep_default_na=False)
    df = f(df)
    p = TMP / nombre
    df.to_csv(p, index=False)
    return p


print("1. API")
c = copia("extra")
(c / "ZZZ.csv").write_text("fecha,cierre\n2024-01-02,1\n", encoding="utf-8")
ok(hd(c) == H0, "un CSV que no es de ningún símbolo del universo no cambia la huella (con los símbolos, como en ejecutar_a)")
nota(f"sin símbolos, huella_datos sigue resumiendo todos los CSV (cambia con ZZZ.csv: {bm.huella_datos(c) != bm.huella_datos(datos)});"
     " r01_01 la llamaba así: cambio de firma, no defecto")
c = copia("cierre")
t = (c / "S1.csv").read_text(encoding="utf-8").splitlines()
t[7] = t[7].rsplit(",", 1)[0] + ",1.5"
(c / "S1.csv").write_text("\n".join(t) + "\n", encoding="utf-8")
ok(hd(c) != H0, "un cierre cambiado de un símbolo del universo cambia la huella")
c = copia("crlf")
(c / "S2.csv").write_bytes((c / "S2.csv").read_bytes().replace(b"\n", b"\r\n"))
nota(f"S2.csv con CRLF (los mismos números): huella distinta {hd(c) != H0} → otra variante (lado cerrado)")
c = copia("bom")
(c / "S2.csv").write_bytes(b"\xef\xbb\xbf" + (c / "S2.csv").read_bytes())
try:
    bm.cargar_precios(c, sims)
    acepta = "lo acepta"
except bm.BancoError as e:
    acepta = f"lo rechaza ({e})"
nota(f"S2.csv con BOM: huella distinta {hd(c) != H0}; cargar_precios {acepta}")
u2 = TMP / "otro_nombre.csv"
shutil.copy(universo, u2)
ok(bm.huella_datos(u2) == HU, "el mismo universo con otro nombre de fichero da la misma huella")
ok(bm.huella_datos(universo_con("orden.csv", lambda d: d.iloc[::-1])) == HU, "filas del universo en otro orden: la misma huella")
ub = TMP / "bom.csv"
ub.write_bytes(b"\xef\xbb\xbf" + universo.read_bytes())
ok(bm.huella_datos(ub) == HU, "el universo con BOM: la misma huella (lo que lee A es lo mismo)")
uc = TMP / "crlf.csv"
uc.write_bytes(universo.read_bytes().replace(b"\n", b"\r\n"))
ok(bm.huella_datos(uc) == HU, "el universo con CRLF: la misma huella")
ok(bm.huella_datos(universo_con("clase.csv", lambda d: d.assign(clase=["RV"] * 5 + ["RF"]))) != HU,
   "un símbolo que cambia de clase cambia la huella del universo")
ok(hd(datos, universo_con("clase2.csv", lambda d: d.assign(clase=["RV"] * 5 + ["RF"]))) == H0,
   "... y no la de los datos (los mismos ficheros)")
for col, val in (("nombre", "otro nombre"), ("tipo_opcion", "ESTRATEGIA"), ("subyacente", "S3")):
    p = universo_con(f"col_{col}.csv", lambda d, col=col, val=val: d.assign(**{col: [val] + list(d[col][1:])}))
    if bm.huella_datos(p) == HU:
        nota(f"cambiar «{col}» de una fila del universo NO cambia su huella (A lee esa columna: HT-01 cargar_universo)")
    else:
        print(f"   cambiar «{col}» cambia la huella")

print("2. Lo que A lee fuera de los símbolos del universo")
conf = yaml.safe_load((bm.EJECUTOR_A / "config" / "por_defecto.yaml").read_text(encoding="utf-8"))
refs = sorted({str(v) for v in conf["indices_referencia"].values() if str(v).upper() not in ("CESTA", "SUBYACENTE", "NINGUNA")})
print(f"   indices_referencia con símbolo propio (A los lee con el proveedor CSV al analizar la clase): {refs}")
c = copia("ref")
t = (c / "REF.csv").read_text(encoding="utf-8").splitlines()
t[9] = t[9].rsplit(",", 1)[0] + ",9.9"
(c / "REF.csv").write_text("\n".join(t) + "\n", encoding="utf-8")
if hd(c) == H0:
    nota("REF.csv (el «subyacente» de S0, o un índice de referencia que no está en el universo) cambia y la huella de los "
         "datos no: A lo lee (orquestacion.py, _referencia_invalida y gc0) y el banco no lo resume")

if "--sin-a" not in sys.argv:
    print("3. Con A de verdad (cliente simulado)")
    A = bm.EJECUTOR_A
    ub = TMP / "a_universo.csv"
    shutil.copy(A / "config" / "universo_ejemplo.csv", ub)
    da = TMP / "a_datos"
    shutil.copytree(A / "ejemplos" / "datos_sinteticos", da)

    def corre(nombre, d, u):
        t = bm.titular_a("2026-03-06", "2026-05-29", TMP / nombre, "mock", None, None, d, u)
        sen = (TMP / nombre / "salida" / "senales.csv").read_bytes()
        return t, hashlib.sha256(sen).hexdigest()[:12], (hd(d, u), bm.huella_datos(u))

    t0, s0, h0 = corre("base", da, ub)
    print(f"   base: {len(t0['selecciones'])} selecciones, senales {s0}")
    df = pd.read_csv(ub, dtype=str, keep_default_na=False)
    div = df.index[df["clase"] == "DIV"]
    df2 = df.copy()
    df2.loc[div, "nombre"] = [f"Par {i}" for i in range(len(div))]
    df2.loc[div, "ambito_incluye"] = "otro ámbito"
    u_nom = TMP / "a_universo_nombres.csv"
    df2.to_csv(u_nom, index=False)
    t1, s1, h1 = corre("nombres", da, u_nom)
    print(f"   nombre y ámbito de las DIV cambiados: huellas iguales {h1 == h0}, senales {s1}, mismas selecciones "
          f"{t1['selecciones'] == t0['selecciones']}")
    if h1 == h0 and s1 != s0:
        nota("con el universo cambiado solo en columnas que la huella no recoge, A entrega otro senales.csv con las mismas "
             f"huellas (selecciones iguales: {t1['selecciones'] == t0['selecciones']}); con un modelo real, el nombre y el "
             "ámbito van al prompt")
    dc = TMP / "a_datos_crlf"
    shutil.copytree(da, dc)
    for f in dc.glob("*.csv"):
        f.write_bytes(f.read_bytes().replace(b"\n", b"\r\n"))
    t2, s2, h2 = corre("crlf", dc, ub)
    print(f"   datos con CRLF: huella de los datos distinta {h2[0] != h0[0]}, senales igual {s2 == s0}")
    if h2[0] != h0[0] and s2 == s0:
        nota("datos con CRLF: A entrega lo mismo y la huella cambia → otra variante (lado cerrado, ver H-01 r02)")

shutil.rmtree(TMP, ignore_errors=True)
print(f"\n{len(fallos)} fallo(s), {len(notas)} nota(s)")
for f in fallos:
    print(" - " + f)
sys.exit(1 if fallos else 0)
