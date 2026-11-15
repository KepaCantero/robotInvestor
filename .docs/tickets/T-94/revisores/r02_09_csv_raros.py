"""QA r02 de T-94 · Validación de datos (H-03) con CSV raros. ¿Se detiene el banco con el motivo, o lee algo distinto de lo
que hay en el fichero?

Cada sonda escribe un CSV en un temporal y llama a `cargar_precios`. «FALLO» marca lo que se acepta en silencio con un
significado dudoso, o lo que se detiene con una excepción que no es BancoError (sin «el motivo»). El Bloque A (que el banco
ejecuta antes con los mismos datos) lee las fechas con `pd.to_datetime` sin formato mixto y rechaza fechas y cabeceras repetidas.
Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r02_09_csv_raros.py [<carpeta de banco_medida.py>]"""
import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

fallos = []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


TMP = Path(tempfile.mkdtemp(prefix="r02_t94_csv_"))


def cargar(nombre, contenido, binario=False):
    d = TMP / nombre
    d.mkdir()
    f = d / "X.csv"
    if binario:
        f.write_bytes(contenido)
    else:
        f.write_text(contenido, encoding="utf-8")
    try:
        return bm.cargar_precios(d, ["X"])["X"]
    except bm.BancoError as e:
        return f"BancoError: {e}"
    except Exception as e:  # noqa: BLE001
        return f"{type(e).__name__}: {e}"


def es_banco_error(r):
    return isinstance(r, str) and r.startswith("BancoError")


# 1. Fechas en formato español dd/mm/aaaa: ¿cada fila se interpreta por separado?
r = cargar("ddmm", "fecha,cierre\n13/01/2026,100\n02/02/2026,101\n03/02/2026,102\n")
print(f"   dd/mm/aaaa → {r if isinstance(r, str) else [d.strftime('%Y-%m-%d') for d in r.index]}")
ok(es_banco_error(r) or [d.strftime("%Y-%m-%d") for d in r.index] == ["2026-01-13", "2026-02-02", "2026-02-03"],
   "fechas dd/mm/aaaa: o se rechazan o se leen todas día-mes (no unas día-mes y otras mes-día)")

# 2. Formatos mezclados en el mismo fichero
r = cargar("mezcla", "fecha,cierre\n2026-01-02,100\n01/05/2026,101\n2026-01-06,102\n")
print(f"   ISO y mm/dd mezclados → {r if isinstance(r, str) else [d.strftime('%Y-%m-%d') for d in r.index]}")
ok(es_banco_error(r), "formatos de fecha mezclados en un fichero: se detiene con el motivo")

# 3. Fecha duplicada con cierres distintos
r = cargar("dup", "fecha,cierre\n2026-01-02,100\n2026-01-02,150\n2026-01-05,101\n")
print(f"   fecha duplicada (100 y 150) → {r if isinstance(r, str) else list(r.values)}")
ok(es_banco_error(r), "una fecha repetida con dos cierres distintos es ambigua: se detiene (como A, «fecha repetida es ambigua»)")

# 4. Zona horaria y mezcla de zona/sin zona
r = cargar("tz", "fecha,cierre\n2026-01-02T00:00:00+01:00,100\n2026-01-05T00:00:00+01:00,101\n")
ok(es_banco_error(r), f"fechas con zona horaria → {str(r)[:110]}")
r = cargar("tzmix", "fecha,cierre\n2026-01-02,100\n2026-01-05T00:00:00Z,101\n")
ok(es_banco_error(r), f"fechas con y sin zona mezcladas → {str(r)[:110]}")

# 5. Codificación y forma del fichero
r = cargar("bom", "﻿fecha,cierre\n2026-01-02,100\n")
ok(es_banco_error(r) or (not isinstance(r, str) and len(r) == 1), f"cabecera con BOM → {str(r)[:110]}")
r = cargar("puntoycoma", "fecha;cierre\n2026-01-02;100\n")
ok(es_banco_error(r), f"separador «;» → {str(r)[:110]}")
r = cargar("latin1", "fecha,cierre,nota\n2026-01-02,100,a\xf1o\n".encode("latin-1"), binario=True)
ok(es_banco_error(r) or not isinstance(r, str), f"fichero en latin-1 → {str(r)[:110]}")
r = cargar("vacio", "")
ok(es_banco_error(r), f"fichero vacío → {str(r)[:110]}")
r = cargar("solocab", "fecha,cierre\n")
print(f"   solo cabecera → {r if isinstance(r, str) else f'serie de {len(r)} filas'}")
ok(es_banco_error(r), "un fichero sin ninguna fila de datos: se detiene («si una fecha no tiene datos, el banco se detiene»)")
r = cargar("cabrep", "fecha,cierre,cierre\n2026-01-02,100,200\n")
print(f"   cabecera repetida «cierre,cierre» → {r if isinstance(r, str) else list(r.values)}")
ok(es_banco_error(r), "cabecera con «cierre» repetido es ambigua: se detiene (A la rechaza)")
r = cargar("alias", "date,close\n2026-01-02,100\n")
ok(es_banco_error(r), f"columnas en inglés (alias que A acepta) → {str(r)[:110]}")

# 6. Números
for nombre, celda in (("miles", '"1,234.5"'), ("coma", '"1234,5"'), ("bool", "True"), ("hex", "0x10"), ("grande", "1e308"),
                      ("desborda", "1e309"), ("espacios", "  101.5  "), ("signo", "+101")):
    r = cargar(nombre, f"fecha,cierre\n2026-01-02,100\n2026-01-05,{celda}\n")
    v = r if isinstance(r, str) else list(r.values)
    print(f"   cierre {celda!r} → {str(v)[:110]}")
    if nombre in ("grande", "espacios", "signo"):
        ok(not isinstance(r, str), f"cierre {celda!r} válido se acepta")
    else:
        ok(es_banco_error(r), f"cierre {celda!r} no válido: se detiene con el motivo")

# 7. Fechas con hora en la misma sesión (dos filas el mismo día)
r = cargar("hora", "fecha,cierre\n2026-01-02 10:00,100\n2026-01-02 16:00,105\n2026-01-05,106\n")
print(f"   dos filas el mismo día con hora distinta → {r if isinstance(r, str) else [(d.isoformat(), v) for d, v in r.items()]}")
ok(es_banco_error(r) or len(r) == 2, "dos cierres del mismo día (con hora) no quedan como dos sesiones")

print(f"\n{len(fallos)} fallo(s)")
for f in fallos:
    print(" -", f)
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if fallos else 0)
