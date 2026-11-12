"""QA r01 de T-103 (revisor independiente): el «\\n» que `escribir` antepone (H-42) frente a cortes, sellos y recuperación.

Uso: python -I r01_03_almacen_cortes.py <ruta a bloque_a/11_Ejecutor>
Para cada escenario se prepara un almacén, se calcula en una copia lo que añade la escritura siguiente (el «\\n» antepuesto más el
registro) y se simula un corte del proceso en CADA byte de lo añadido, con el fichero de sellos de antes (el proceso murió antes
de sellar). Después se abre, se escribe otro registro, se vuelve a abrir y se comprueba la cadena (`verificar_integridad`), los
registros y que el fichero acaba en «\\n». También: una excepción a mitad de escritura deja el fichero byte a byte como estaba, y
un valor con U+2028, U+2029 o U+0085 (anterior a T-103, misma lectura del almacén). Sin red ni claves.
"""
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
import bloque_a  # noqa: E402

assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
from bloque_a import almacen as mod  # noqa: E402
from bloque_a.almacen import Almacen  # noqa: E402

fallos = 0
RAIZ = Path(tempfile.mkdtemp(prefix="qa_t103_"))


def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))


def info(nombre, detalle=""):
    print("INFO  " + nombre + (f" — {detalle}" if detalle else ""))


def f5(d):
    return Path(d) / mod.ARCHIVOS["F5"]


def base(nombre, *, legado=False, sin_salto=True, cola=b""):
    d = RAIZ / nombre
    a = Almacen(d)
    for k in ("uno", "dos", "tres"):
        a.escribir("F5", "AG-01", {"id": k, "nota": "año «ñ» — fin"})
    if legado:
        (d / "sellos_integridad.json").unlink()
        (d / "formato_almacen.json").unlink()
    datos = f5(d).read_bytes()
    if sin_salto:
        datos = datos[:-1]
    f5(d).write_bytes(datos + cola)
    return d


def copia(d, nombre):
    destino = RAIZ / nombre
    shutil.rmtree(destino, ignore_errors=True)
    shutil.copytree(d, destino)
    return destino


def ids(d):
    return list(Almacen(d).estado("F5"))


def escenario(nombre, d0, esperados):
    """`d0` ya abierto una vez (migrado si era legado). Corte en cada byte de la escritura de «cuatro»."""
    antes = f5(d0).read_bytes()
    sellos_antes = (d0 / "sellos_integridad.json").read_bytes()
    c = copia(d0, nombre + "_ref")
    Almacen(c).escribir("F5", "AG-01", {"id": "cuatro", "nota": "x"})
    despues = f5(c).read_bytes()
    assert despues.startswith(antes)
    anadido = despues[len(antes):]
    malos = []
    for k in range(len(anadido) + 1):
        d = copia(d0, nombre + "_corte")
        f5(d).write_bytes(antes + anadido[:k])
        (d / "sellos_integridad.json").write_bytes(sellos_antes)
        try:
            a = Almacen(d)
            visto = list(a.estado("F5"))
            a.escribir("F5", "AG-01", {"id": "cinco"})
            final = ids(d)
            integ = all(Almacen(d).verificar_integridad().values())
            datos = f5(d).read_bytes()
            ok = (visto == esperados and final == esperados + ["cinco"] and integ and datos.endswith(b"\n")
                  and datos.count(b"\n") == len(final))
            if not ok:
                malos.append((k, visto, final, integ, datos[-3:]))
        except Exception as e:   # noqa: BLE001
            malos.append((k, type(e).__name__, str(e)[:80]))
    informe(f"{nombre}: {len(anadido) + 1} cortes (sello de antes) — abre, aparta lo no sellado, escribe y reabre con la cadena entera",
            not malos, f"{len(malos)} mal: {malos[:3]}" if malos else f"«\\n» antepuesto: {anadido[:1] == bytes([10])}")
    # el corte después del sello: el registro quedó confirmado
    d = copia(c, nombre + "_sellado")
    a = Almacen(d)
    a.escribir("F5", "AG-01", {"id": "cinco"})
    informe(f"{nombre}: con el sello escrito, el registro queda confirmado y la cadena sigue",
            ids(d) == esperados + ["cuatro", "cinco"] and all(Almacen(d).verificar_integridad().values()))


# ---------------------------------------------------------------------------------------------------------------- 1
print("--- 1. Almacén sellado cuyo último registro no acaba en «\\n» (H-42 caso 2)")
d = base("sellado_sin_salto")
Almacen(d)
escenario("1  sellado sin «\\n»", d, ["uno", "dos", "tres"])

print("--- 2. Almacén anterior a los sellos con el último registro sin «\\n» (H-42 caso 1), migrado al abrir")
d = base("legado_sin_salto", legado=True)
Almacen(d)
informe("2  la migración sella los tres registros", ids(d) == ["uno", "dos", "tres"])
escenario("2  legado migrado", d, ["uno", "dos", "tres"])

print("--- 3. Almacén sellado normal (acaba en «\\n»): sin separador, como antes")
d = base("sellado_normal", sin_salto=False)
Almacen(d)
escenario("3  sellado normal", d, ["uno", "dos", "tres"])

print("--- 4. Finales raros del último registro")
for nombre, cola in (("CRLF (editado en Windows)", b"\r\n"), ("solo «\\r»", b"\r"), ("espacios", b"   "), ("tabulador", b"\t")):
    d = base("final_" + str(abs(hash(nombre))), cola=cola)
    try:
        a = Almacen(d)
        a.escribir("F5", "AG-01", {"id": "cuatro"})
        ok = ids(d) == ["uno", "dos", "tres", "cuatro"] and all(Almacen(d).verificar_integridad().values())
        informe(f"4  último registro + {nombre}: escribe y reabre", ok, repr(f5(d).read_bytes()[-60:-40]))
    except Exception as e:   # noqa: BLE001
        info(f"4  último registro + {nombre}: no abre o no escribe (falla cerrado)", f"{type(e).__name__}: {str(e)[:80]}")

print("--- 5. Excepción a mitad de escritura (fsync falla): el fichero queda byte a byte como estaba, sin el «\\n»")
d = base("excepcion")
Almacen(d)
antes = f5(d).read_bytes()
a = Almacen(d)
real = os.fsync
llamadas = {"n": 0}


def fsync_falla(fd):
    llamadas["n"] += 1
    raise OSError("disco lleno (simulado)")


mod.os.fsync = fsync_falla
try:
    a.escribir("F5", "AG-01", {"id": "cuatro"})
    informe("5  la escritura lanza", False)
except OSError:
    pass
finally:
    mod.os.fsync = real
informe("5  el fichero no cambia (ni el «\\n» antepuesto)", f5(d).read_bytes() == antes, f"{len(f5(d).read_bytes())} vs {len(antes)}")
a.escribir("F5", "AG-01", {"id": "cuatro"})
informe("5  la misma instancia escribe después y se reabre", ids(d) == ["uno", "dos", "tres", "cuatro"]
        and all(Almacen(d).verificar_integridad().values()))

print("--- 6. Idempotencia: dos instancias sobre el mismo almacén sin «\\n» final escriben alternando")
d = base("dos_instancias")
a, b = Almacen(d), Almacen(d)
a.escribir("F5", "AG-01", {"id": "a1"})
b.escribir("F5", "AG-01", {"id": "b1"})
a.escribir("F5", "AG-01", {"id": "a2"})
datos = f5(d).read_bytes()
informe("6  cinco líneas, una por registro, y la cadena entera", ids(d) == ["uno", "dos", "tres", "a1", "b1", "a2"]
        and datos.count(b"\n") == 6 and b"\n\n" not in datos and all(Almacen(d).verificar_integridad().values()))

print("--- 7. Separadores de línea de Unicode dentro de un valor (lectura con `splitlines`; anterior a T-103)")
for nombre, ch in (("U+2028", " "), ("U+2029", " "), ("U+0085 (NEL)", "\x85"), ("U+001C", "\x1c")):
    d = RAIZ / ("sep_" + nombre[:6].replace("+", ""))
    a = Almacen(d)
    a.escribir("F5", "AG-01", {"id": "uno", "nota": "texto citado" + ch + "de una web"})
    a.escribir("F5", "AG-01", {"id": "dos"})
    try:
        r = ids(d)
        informe(f"7  {nombre} en un valor: el almacén se reabre", r == ["uno", "dos"], str(r))
    except Exception as e:   # noqa: BLE001
        informe(f"7  {nombre} en un valor: el almacén se reabre", False, f"{type(e).__name__}: {str(e)[:70]}")

shutil.rmtree(RAIZ, ignore_errors=True)
print(f"fallos: {fallos}")
sys.exit(1 if fallos else 0)
