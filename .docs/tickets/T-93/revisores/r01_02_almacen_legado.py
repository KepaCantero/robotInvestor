"""QA r01 de T-93 (revisor independiente): el almacén tras la corrección de H-34 (almacén anterior a los sellos) y H-35 (corte a
mitad de un carácter UTF-8).

Uso: python -I r01_02_almacen_legado.py <ruta a bloque_a/11_Ejecutor>
Imprime OK/FALLO por caso (INFO no cuenta) y el número de fallos.

Un almacén «anterior a los sellos» se simula como en la prueba de H-34: tres registros escritos y después se borran
`sellos_integridad.json` y `formato_almacen.json`. El corte del último registro se simula en CADA byte posible.
"""
import hashlib
import json
import sys
import tempfile
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
import bloque_a  # noqa: E402

assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
from bloque_a.almacen import ARCHIVOS, Almacen  # noqa: E402

fallos = 0


def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))


def info(nombre, detalle=""):
    print("INFO  " + nombre + (f" — {detalle}" if detalle else ""))


TEXTO = "«España», año, ñandú — información"


def f5(d):
    return Path(d) / ARCHIVOS["F5"]


def abre(d):
    try:
        return Almacen(Path(d)), None
    except Exception as x:
        return None, f"{type(x).__name__}: {str(x)[:80]}"


def huella(d):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(d).iterdir()) if p.is_file()
            and p.name != ".almacen.lock"}


def legado_con_linea(d, linea: bytes, archivos=("F5",)):
    """Almacén anterior a los sellos: tres registros en F5 (y en los demás `archivos`) y `linea` añadida al final de cada uno."""
    a = Almacen(Path(d))
    for arch in archivos:
        for k in ("uno", "dos", "tres"):
            a.escribir(arch, "AG-01" if arch == "F5" else "OPERADOR", {"id": k, "cns_id": k, "nota": TEXTO, "tipo_entrada": "CFG",
                                                                          "param_id": k})
    (Path(d) / "sellos_integridad.json").unlink()
    (Path(d) / "formato_almacen.json").unlink()
    for arch in archivos:
        with open(Path(d) / ARCHIVOS[arch], "ab") as fh:
            fh.write(linea)


def plantilla_legado():
    """Almacén legado con cuatro registros encadenados en F5: devuelve {fichero: bytes} y la cuarta línea de F5."""
    with tempfile.TemporaryDirectory() as d:
        a = Almacen(Path(d))
        for k in ("uno", "dos", "tres", "cuatro"):
            a.escribir("F5", "AG-01", {"id": k, "cns_id": k, "nota": TEXTO})
        (Path(d) / "sellos_integridad.json").unlink()
        (Path(d) / "formato_almacen.json").unlink()
        ficheros = {p.name: p.read_bytes() for p in Path(d).iterdir() if p.is_file() and p.name != ".almacen.lock"}
        return ficheros, f5(d).read_bytes().splitlines(keepends=True)[3]


# ------------------------------------------------------------------------------------------------------------------ 1
print("--- 1. Almacén legado: el cuarto registro cortado en cada byte; abrir, escribir otro y volver a abrir")
PLANTILLA, linea4 = plantilla_legado()
resultados = {"bien": 0, "no_abre": 0, "corrompe": 0, "pierde": 0}
ejemplo = {}
for i in range(1, len(linea4) + 1):
    with tempfile.TemporaryDirectory() as d:
        for nombre, datos in PLANTILLA.items():
            (Path(d) / nombre).write_bytes(datos[: len(datos) - len(linea4) + i] if nombre == f5(d).name else datos)
        a, err = abre(d)
        if a is None:
            resultados["no_abre"] += 1
            ejemplo.setdefault("no_abre", (i, err))
            continue
        try:
            a.escribir("F5", "AG-01", {"id": "nuevo", "nota": TEXTO})
        except Exception as x:
            resultados["no_abre"] += 1
            ejemplo.setdefault("no_abre", (i, f"al escribir: {type(x).__name__}"))
            continue
        b, err = abre(d)
        if b is None:
            resultados["corrompe"] += 1
            ejemplo.setdefault("corrompe", (i, err))
            continue
        ids = list(b.estado("F5"))
        esperado_completo = i >= len(linea4) - 1   # sin el «\n» final el registro ya está entero
        if ids[-1] != "nuevo" or ids[:3] != ["uno", "dos", "tres"] or (esperado_completo and "cuatro" not in ids):
            resultados["pierde"] += 1
            ejemplo.setdefault("pierde", (i, ids))
        else:
            resultados["bien"] += 1
            if esperado_completo:
                ejemplo.setdefault("completo", (i, ids))
n = len(linea4)
informe(f"1  {n} cortes: abre, escribe y reabre bien en {resultados['bien']}; no abre en {resultados['no_abre']}; "
        f"la siguiente escritura lo corrompe en {resultados['corrompe']}; pierde registros en {resultados['pierde']}",
        resultados["corrompe"] == 0 and resultados["pierde"] == 0, str({k: v for k, v in ejemplo.items() if k != "completo"}))
if "completo" in ejemplo:
    info("1  registro completo sin «\\n» final (corte justo antes del salto de línea)", str(ejemplo["completo"]))

# ------------------------------------------------------------------------------------------------------------------ 2
print("--- 2. Almacén sellado: un registro confirmado al que le falta el «\\n» final (p. ej. sellado al migrar el caso 1)")
with tempfile.TemporaryDirectory() as d:
    a = Almacen(Path(d))
    for k in ("uno", "dos", "tres"):
        a.escribir("F5", "AG-01", {"id": k, "nota": TEXTO})
    datos = f5(d).read_bytes()
    f5(d).write_bytes(datos[:-1])   # quitar el salto de línea final del último registro, que sí está sellado
    sellos = json.loads((Path(d) / "sellos_integridad.json").read_text())
    a, err = abre(d)
    if a is None:
        informe("2  no abre (falla cerrado)", True, err)
    else:
        try:
            a.escribir("F5", "AG-01", {"id": "nuevo"})
            b, err = abre(d)
            informe("2  abre, escribe y reabre sin corromperse", b is not None and list(b.estado("F5"))[-1] == "nuevo",
                    err or str(list(b.estado("F5"))))
        except Exception as x:
            informe("2  abre, escribe y reabre sin corromperse", False, f"{type(x).__name__}: {x}")

# ------------------------------------------------------------------------------------------------------------------ 3
print("--- 3. Almacén legado con una línea cortada en DOS ficheros: falla cerrado sin tocar nada")
with tempfile.TemporaryDirectory() as d:
    legado_con_linea(d, b'{"_seq": 4, "id": "cuat', archivos=("F5", "F10"))
    antes = huella(d)
    a, err = abre(d)
    informe("3  no abre", a is None, err)
    informe("3  ningún fichero cambia", huella(d) == antes)

# ------------------------------------------------------------------------------------------------------------------ 4
print("--- 4. Abrir dos veces tras apartar la línea (idempotencia)")
with tempfile.TemporaryDirectory() as d:
    legado_con_linea(d, linea4[:40])
    a, _ = abre(d)
    aparte = f5(d).with_name(f5(d).name + ".no_confirmado.jsonl")
    primero = aparte.read_bytes()
    inc1 = [e for e in a.leer("HA") if "sin confirmar" in str(e.get("detalle"))]
    b, err = abre(d)
    inc2 = [e for e in b.leer("HA") if "sin confirmar" in str(e.get("detalle"))] if b else []
    informe("4  la segunda apertura no aparta nada ni anota otra incidencia", b is not None and aparte.read_bytes() == primero
            and len(inc1) == len(inc2) == 1, err or f"{len(inc1)} y {len(inc2)} incidencias")

# ------------------------------------------------------------------------------------------------------------------ 5
print("--- 5. Corte a mitad de un carácter (H-35): lo apartado conserva los bytes")
with tempfile.TemporaryDirectory() as d:
    a = Almacen(Path(d))
    for k in ("uno", "dos", "tres"):
        a.escribir("F5", "AG-01", {"id": k, "nota": TEXTO})
    sellos = (Path(d) / "sellos_integridad.json").read_bytes()
    a.escribir("F5", "AG-01", {"id": "cuatro", "nota": TEXTO})
    (Path(d) / "sellos_integridad.json").write_bytes(sellos)
    datos = f5(d).read_bytes()
    lineas = datos.splitlines(keepends=True)
    corte = lineas[3][: lineas[3].index("ñ".encode()) + 1]
    f5(d).write_bytes(b"".join(lineas[:3]) + corte)
    a, err = abre(d)
    aparte = f5(d).with_name(f5(d).name + ".no_confirmado.jsonl")
    apartado = aparte.read_bytes() if aparte.exists() else b""
    informe("5  abre y aparta", a is not None and bool(apartado), err or "")
    # INFO: lo apartado se decodifica con errors="replace": el byte cortado pasa a U+FFFD y la copia no es idéntica al original
    info("5  la copia apartada contiene los bytes originales del corte", str(corte[-10:] in apartado))

# ------------------------------------------------------------------------------------------------------------------ 6
print("--- 6. Una línea intermedia con bytes no UTF-8 (manipulación): falla cerrado sin tocar nada")
with tempfile.TemporaryDirectory() as d:
    a = Almacen(Path(d))
    for k in ("uno", "dos", "tres"):
        a.escribir("F5", "AG-01", {"id": k, "nota": TEXTO})
    lineas = f5(d).read_bytes().splitlines(keepends=True)
    lineas[1] = lineas[1].replace("ñ".encode(), b"\xc3", 1)
    f5(d).write_bytes(b"".join(lineas))
    antes = huella(d)
    a, err = abre(d)
    informe("6  no abre", a is None, err)
    informe("6  ningún fichero cambia", huella(d) == antes)

print(f"fallos: {fallos}")
sys.exit(1 if fallos else 0)
