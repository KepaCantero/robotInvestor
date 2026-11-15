"""QA r03 de T-94 · Lectura de precios (H-16) y de consumo (H-18) estricta, y cotas de un veredicto (H-19), en sus bordes.

1. Precios: cabecera con BOM, espacios alrededor de la fecha, 30 de febrero, fila con menos o más campos, líneas en blanco,
   comillas, fechas desordenadas, fin de semana, cabecera en mayúsculas.
2. consumo.csv: tokens con decimales («10.9»), «-0», columnas que faltan, solo cabecera, fichero vacío, cabecera repetida,
   uc con texto, coste con espacios.
3. Cotas en la línea de órdenes y en la API: bordes exactos (nivel 0,80 y 0,99; 0,7999 y 0,9901; remuestreos 199 y 200;
   min-efectivas 4 y 5; «nan» e «inf»; max-variantes 0 y 5000).
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r03_11_csv_consumo_cotas.py [<carpeta de banco_medida.py>]"""
import argparse
import contextlib
import io
import shutil
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm  # noqa: E402

fallos, notas = [], []
TMP = Path(tempfile.mkdtemp(prefix="r03_t94_csv_"))


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


def nota(msg):
    print("NOTA  " + msg)
    notas.append(msg)


def precios(nombre, contenido, se_espera_error):
    d = TMP / nombre
    d.mkdir()
    (d / "X.csv").write_bytes(contenido.encode("utf-8"))
    try:
        s = bm.cargar_precios(d, ["X"])["X"]
        ok(not se_espera_error, f"{nombre}: aceptado → {list(zip(s.index.strftime('%Y-%m-%d'), s.round(4)))}")
    except bm.BancoError as e:
        ok(se_espera_error, f"{nombre} → BancoError: {e}")
    except Exception as e:  # noqa: BLE001
        ok(False, f"{nombre} → {type(e).__name__}: {e} (sin motivo)")


# 1. Precios
precios("bom", "﻿fecha,cierre\n2026-01-02,100\n2026-01-05,101\n", False)
precios("espacios_fecha", "fecha,cierre\n 2026-01-02 ,100\n2026-01-05,101\n", False)
precios("30_febrero", "fecha,cierre\n2026-02-27,100\n2026-02-30,101\n", True)
precios("fila_corta", "fecha,cierre\n2026-01-02,100\n2026-01-05\n", True)
precios("fila_larga", "fecha,cierre\n2026-01-02,100\n2026-01-05,101,7\n", True)
precios("lineas_en_blanco", "fecha,cierre\n2026-01-02,100\n\n2026-01-05,101\n", False)
precios("comillas", 'fecha,cierre\n"2026-01-02","100"\n2026-01-05,101\n', False)
precios("desordenadas", "fecha,cierre\n2026-01-05,101\n2026-01-02,100\n", False)
precios("mayusculas", "Fecha,Cierre\n2026-01-02,100\n", True)
precios("columna_extra", "fecha,cierre,volumen\n2026-01-02,100,5\n", False)
precios("fecha_vacia", "fecha,cierre\n,100\n2026-01-05,101\n", True)
s = bm.cargar_precios(TMP / "desordenadas", ["X"])["X"]
ok(list(s.index.strftime("%Y-%m-%d")) == ["2026-01-02", "2026-01-05"], "fechas desordenadas: se ordenan")

# 2. consumo.csv
CAB = "agente,llamadas,tokens_entrada,tokens_salida,tokens_cache_escritura,tokens_cache_lectura,uc,coste_estimado\n"


def consumo(nombre, contenido, se_espera_error, comprobar=None):
    f = TMP / f"consumo_{nombre}.csv"
    f.write_text(contenido, encoding="utf-8")
    try:
        c = bm.leer_consumo(f)
        bien = not se_espera_error and (comprobar is None or comprobar(c))
        ok(bien, f"consumo {nombre}: aceptado → {c}")
    except bm.BancoError as e:
        ok(se_espera_error, f"consumo {nombre} → BancoError: {e}")
    except Exception as e:  # noqa: BLE001
        ok(False, f"consumo {nombre} → {type(e).__name__}: {e} (sin motivo)")


consumo("tokens_con_decimales", CAB + "A,1,10.9,1,0,0,0.1,0.5\n", True)
consumo("menos_cero", CAB + "A,1,-0,1,0,0,0.1,0.5\n", False)
consumo("sin_columnas_de_cache", "agente,llamadas,tokens_entrada,tokens_salida,coste_estimado\nA,1,10,1,0.5\n", False,
        lambda c: c.get("tokens_cache_lectura") is None)
consumo("solo_cabecera", CAB, False, lambda c: c["coste_estimado"] is None)
consumo("vacio", "", False, lambda c: c["coste_estimado"] is None)
consumo("cabecera_repetida", "agente,llamadas,llamadas,tokens_entrada,tokens_salida\nA,1,500,10,1\n", True)
consumo("uc_texto", CAB + "A,1,10,1,0,0,mucho,0.5\n", True)
consumo("coste_con_espacios", CAB + "A,1,10,1,0,0,0.1, 0.5 \n", False, lambda c: c["coste_estimado"] == 0.5)
consumo("celda_vacia_tokens", CAB + "A,1,,1,0,0,0.1,0.5\n", False, lambda c: c["tokens_entrada"] is None)

# 3. Cotas en la línea de órdenes (solo el análisis de argumentos: argparse sale antes de ejecutar A si un valor no vale)
BASE = ["a", "--desde", "2024-01-05", "--hasta", "2024-03-01", "--salida", str(TMP / "cli"), "--registro", str(TMP / "reg.jsonl")]


def cli(extra, se_espera_rechazo):
    err = io.StringIO()
    bm_titular, bm.titular_a = bm.titular_a, lambda *a, **k: (_ for _ in ()).throw(bm.BancoError("titular de prueba: no se ejecuta"))
    try:
        with contextlib.redirect_stderr(err):
            codigo = bm.main(BASE + extra)
    except SystemExit as e:
        codigo = f"SystemExit {e.code}"
    finally:
        bm.titular_a = bm_titular
    rechazado = codigo == "SystemExit 2"
    ok(rechazado == se_espera_rechazo, f"{' '.join(extra)}: {'rechazado por argparse' if rechazado else f'admitido (código {codigo})'}")


for extra, rechazo in ((["--nivel", "0.80"], False), (["--nivel", "0.99"], False), (["--nivel", "0.7999"], True),
                       (["--nivel", "0.9901"], True), (["--nivel", "nan"], True), (["--nivel", "inf"], True),
                       (["--remuestreos", "199"], True), (["--remuestreos", "200"], False), (["--min-efectivas", "4"], True),
                       (["--min-efectivas", "5"], False), (["--max-variantes", "0"], True), (["--semilla", "-1"], True),
                       (["--ventana", "0"], True)):
    cli(extra, rechazo)
err = io.StringIO()
bm_titular, bm.titular_a = bm.titular_a, lambda *a, **k: (_ for _ in ()).throw(bm.BancoError("titular de prueba: no se ejecuta"))
try:
    with contextlib.redirect_stderr(err):
        codigo = bm.main(BASE[:-1] + [str(TMP / "reg_mv.jsonl"), "--max-variantes", "5000"])
finally:
    bm.titular_a = bm_titular
print(f"   --max-variantes 5000: código {codigo}; «{err.getvalue().strip()[:140]}»")
ok(codigo == 2 and "max_variantes" in err.getvalue(), "--max-variantes por encima del máximo del registro: detenido con el motivo")
# API: diferencia con los bordes
xa, ga = [0.01] * 12, [f"f{i}" for i in range(12)]
for kw, error in (({"nivel": 0.80}, False), ({"nivel": 0.99}, False), ({"nivel": 0.7999}, True), ({"remuestreos": 199}, True),
                  ({"min_efectivas": 4}, True), ({"nivel": True}, True), ({"remuestreos": 200.0}, True)):
    args = dict(remuestreos=200, semilla=1, nivel=0.9, min_efectivas=10) | kw
    try:
        bm.diferencia(xa, [-x for x in xa], args["remuestreos"], args["semilla"], args["nivel"], args["min_efectivas"], ga, ga)
        ok(not error, f"diferencia con {kw}: admitido")
    except bm.BancoError as e:
        ok(error, f"diferencia con {kw} → BancoError: {e}")

print(f"\n{len(fallos)} fallo(s), {len(notas)} nota(s)")
for f in fallos:
    print(" -", f)
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if fallos else 0)
