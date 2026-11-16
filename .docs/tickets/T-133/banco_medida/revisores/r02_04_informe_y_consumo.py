"""T-133 QA r02 · La línea de la plantilla en informe.md y el consumo estricto (banco 0.5.0, r02 H-05 y H-06).

1. informe.md con la plantilla: ¿dice el total y lo que entra? ¿cuadra con la tabla? ¿y con una plantilla vacía (0)?
2. Columnas opcionales ausentes: «sin dato» en la línea del titular ¿y en «Por selección resuelta»?
3. Celdas vacías: obligatorias (llamadas, tokens_entrada, tokens_salida) → error; opcionales presentes y vacías → ¿0 sin decirlo?
4. Fila larga (más campos que la cabecera), BOM, CRLF, espacios alrededor del número, «+5», «0x10», «1_000».
Uso: .venv/bin/python -B r02_04_informe_y_consumo.py <carpeta de banco_medida.py>"""
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import banco_medida as bm

fallos, notas = [], []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg, flush=True)
    if not cond:
        fallos.append(msg)


def nota(msg):
    print("NOTA  " + msg, flush=True)
    notas.append(msg)


TMP = Path(tempfile.mkdtemp(prefix="r02_t133_consumo_"))
TIT = [{"fecha_asof": f"2026-{m:02d}-01", "fecha_fin": f"2026-{m:02d}-20", "resuelta": True, "exceso": 0.01 * (m % 3 - 1),
        "clase": "C"} for m in range(1, 13)]


def consumo(nombre, texto, binario=None):
    f = TMP / nombre
    if binario is not None:
        f.write_bytes(binario)
    else:
        f.write_text(texto, encoding="utf-8")
    try:
        return bm.leer_consumo(f), None
    except bm.BancoError as e:
        return None, str(e)


def md(c, plantilla=None):
    inf = bm.construir_informe({"titular": TIT, "azar": TIT}, c, 200, 1, None, "h" * 64)
    if plantilla is not None:
        inf["plantilla"] = plantilla
    return bm.informe_md(inf, "t")


# 1. plantilla
c, _ = consumo("ok.csv", "llamadas,tokens_entrada,tokens_salida,tokens_cache_escritura,tokens_cache_lectura,uc,coste_estimado\n"
                         "2,10,5,1,3,0.5,0.01\n")
t = md(c, {"selecciones": 300, "en_muestra": 12})
ok("tenía 300 selecciones y 12 entran en la muestra" in t, "1. la línea de la plantilla dice el total y lo que entra")
fila = next(x for x in t.splitlines() if x.startswith("| titular"))
print(f"   fila del titular: {fila}")
if "| 0 |" in fila.split("|", 4)[3:4][0:1] or fila.split("|")[4].strip() == "0":
    nota("1b. la columna «Fuera de muestra» del titular sigue en 0 con 288 fuera: lo explica la línea de encima, pero la tabla "
         "y la línea dicen cosas distintas de lo mismo")
t0 = md(c, {"selecciones": 0, "en_muestra": 0})
ok("tenía 0 selecciones" in t0, "1c. con una plantilla vacía la línea también sale (un dict no vacío)")

# 2. columnas ausentes
c, _ = consumo("min.csv", "llamadas,tokens_entrada,tokens_salida\n2,10,5\n")
t = md(c)
lin = next(x for x in t.splitlines() if x.startswith("- Titular"))
ps = next(x for x in t.splitlines() if x.startswith("- Por selección"))
ok("sin dato escritos" in lin and "sin dato uc" in lin, f"2. línea del titular con «sin dato»: {lin}")
ok("sin dato" in ps.split("coste")[0], f"2b. «Por selección resuelta» sin columnas de caché ni uc: {ps}")

# 3. celdas vacías
for col in ("llamadas", "tokens_entrada", "tokens_salida"):
    cab = "llamadas,tokens_entrada,tokens_salida"
    vals = {"llamadas": "2", "tokens_entrada": "10", "tokens_salida": "5"}
    vals[col] = ""
    c, e = consumo(f"vacia_{col}.csv", f"{cab}\n{vals['llamadas']},{vals['tokens_entrada']},{vals['tokens_salida']}\n")
    ok(e is not None and "vacío" in e, f"3. «{col}» vacío → error ({e})")
for col in ("tokens_cache_escritura", "tokens_cache_lectura", "uc"):
    c, e = consumo(f"op_{col}.csv", f"llamadas,tokens_entrada,tokens_salida,{col}\n2,10,5,\n2,10,5,7\n")
    if e is None:
        print(f"   «{col}» presente con una celda vacía: suma {c[col]}, columnas_ausentes {c['columnas_ausentes']}")
        if c[col] == 7 and col not in c["columnas_ausentes"]:
            nota(f"3b. «{col}» presente con una celda vacía cuenta 0 sin decirlo: la suma sale como total completo")

# 4. formatos raros
c, e = consumo("larga.csv", "llamadas,tokens_entrada,tokens_salida\n2,10,5,99\n")
print(f"   4. fila larga: {e or ('aceptada: ' + str({k: c[k] for k in ('llamadas', 'tokens_salida')}))}")
if e is None:
    nota("4a. una fila con un campo de más (99) se acepta: el campo sobrante se descarta sin decirlo")
c, e = consumo("bom.csv", None, b"\xef\xbb\xbfllamadas,tokens_entrada,tokens_salida\n2,10,5\n")
print(f"   4b. consumo.csv con BOM: {e or 'aceptado'}")
c, e = consumo("crlf.csv", None, b"llamadas,tokens_entrada,tokens_salida\r\n2,10,5\r\n")
ok(e is None and c["llamadas"] == 2, f"4c. CRLF aceptado ({e})")
for v in (" 5 ", "+5", "0x10", "1_000", "5e0"):
    c, e = consumo("raro.csv", f"llamadas,tokens_entrada,tokens_salida\n2,10,{v}\n")
    print(f"   4d. tokens_salida «{v}»: {e or c['tokens_salida']}")
print(f"\n{len(fallos)} fallo(s), {len(notas)} nota(s)")
for f in fallos:
    print(" - " + f)
sys.exit(1 if fallos else 0)
