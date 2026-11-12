"""QA r02 de T-103 (revisor independiente): la regla de «tres o más tramos de solo cifras» de `_es_clave_sk` (H-50).

Uso: python -I r02_03_tres_tramos_falsos_positivos.py <ruta a bloque_a/11_Ejecutor en 7feb697> <ruta anterior (regla de 4)>

1. Recall: colas de 3 grupos de cifras con 20 caracteres o más (6-6-6, 5-6-7, 7-7-7, 8-8-8, fechas, con «_» y con separadores
   repetidos) → todas clave. Por debajo de 20 (5-5-5, 5-5-6, 5-6-6) → ninguna candidata (límite de T-92, declarado).
2. Falsos positivos (INFO, para «Límites»): textos corrientes con «sk-» y tres grupos de cifras (marcas de tiempo, periodos con
   código de cotización, referencias de pedido); cuántos marca la r02 y cuántos la regla anterior.
3. Lo que no debe cambiar: los titulares con un tramo de letras siguen sin marcarse (los 12 de H-33 están en r04_01 de T-92).
Las claves se arman en tiempo de ejecución con cifras aleatorias. Sin red.
"""
import json
import random
import string
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
ANTES = Path(sys.argv[2]).resolve()
fallos = 0


def ver(ok, nombre, detalle=""):
    global fallos
    print(f"{'OK   ' if ok else 'FALLO'} {nombre}{' — ' + str(detalle) if detalle else ''}")
    fallos += 0 if ok else 1


def marca(ruta, textos):
    prog = ("import json,sys; sys.path.insert(0, sys.argv[1]); from bloque_a.llm import contenido_sensible;"
            "print(json.dumps([contenido_sensible(t) for t in json.load(sys.stdin)]))")
    r = subprocess.run([sys.executable, "-I", "-c", prog, str(ruta)], input=json.dumps(textos), capture_output=True, text=True,
                       check=True)
    return json.loads(r.stdout)


rnd = random.Random(20261112)
PRE = "s" + "k-"


def cifras(n):
    return "".join(rnd.choice(string.digits) for _ in range(n))


def fecha():
    return f"{rnd.randint(1990, 2030)}{rnd.randint(1, 12):02d}{rnd.randint(1, 28):02d}"


print("--- 1. Recall de tres grupos de cifras")
casos = {
    "6-6-6 (20)": lambda: "-".join(cifras(6) for _ in range(3)),
    "5-6-7 (20)": lambda: "-".join([cifras(5), cifras(6), cifras(7)]),
    "7-7-7": lambda: "-".join(cifras(7) for _ in range(3)),
    "8-8-8": lambda: "-".join(cifras(8) for _ in range(3)),
    "tres fechas": lambda: "-".join(fecha() for _ in range(3)),
    "6_6_6 con «_»": lambda: "_".join(cifras(6) for _ in range(3)),
    "separadores repetidos 5--5--5-": lambda: "--".join(cifras(5) for _ in range(3)) + "--",
    "mayúsculas SK- 6-6-6": lambda: "-".join(cifras(6) for _ in range(3)),
}
for nombre, g in casos.items():
    pre = "SK-" if nombre.startswith("mayúsculas") else PRE
    textos = ["clave: " + pre + g() for _ in range(300)]
    n, v = sum(marca(EJ, textos)), sum(marca(ANTES, textos[:50]))
    ver(n == 300, f"1 {nombre}", f"r02 {n}/300 · antes {v}/50")
for nombre, g in {"5-5-5 (17)": lambda: "-".join(cifras(5) for _ in range(3)),
                  "5-6-6 (19)": lambda: "-".join([cifras(5), cifras(6), cifras(6)])}.items():
    textos = ["clave: " + PRE + g() for _ in range(300)]
    print(f"INFO  1 {nombre}: r02 {sum(marca(EJ, textos))}/300 (no candidata: cola de menos de 20; declarado en «Límites»)")

print("--- 2. Falsos positivos de la regla de tres tramos (INFO)")
fp = [
    f"log {PRE}20241112-103000-123456 sin errores",
    f"https://www.example.com/informes/{PRE}000660-20240725-20240726",
    f"periodo {PRE}20240101-20241231-000660",
    "Ref. pedido SK-2024110012-000345-01",
    f"lote {PRE}000123_000456_000789",
    f"fichero {PRE}20231231_235959_000001.csv",
    f"id de ejecución {PRE}1731400000-000001-42",
    f"{PRE}100000-200000-300000 (rango de nominales)",
]
n, v = marca(EJ, fp), marca(ANTES, fp)
for t, a, b in zip(fp, n, v):
    print(f"INFO  2 {'MARCA' if a else 'no marca'} (antes: {'MARCA' if b else 'no marca'}) — {t}")
nuevos = sum(1 for a, b in zip(n, v) if a and not b)
print(f"INFO  2 falsos positivos nuevos de la regla de tres tramos: {nuevos} de {len(fp)}")

print("--- 3. Titulares con un tramo de letras: siguen sin marcarse")
tit = [f"{PRE}hynix-2024-07-25-q2-results", f"{PRE}hynix_000660_20240725_earnings", f"{PRE}telecom-2023-annual-report-2024",
       f"{PRE}innovation-20240101-20241231-review", f"https://www.example.com/{PRE}hynix-000660-20241112-103000"]
r = marca(EJ, tit)
ver(not any(r), "3 cinco titulares con letras", f"{sum(r)} marcados")
print(f"fallos: {fallos}")
sys.exit(1 if fallos else 0)
