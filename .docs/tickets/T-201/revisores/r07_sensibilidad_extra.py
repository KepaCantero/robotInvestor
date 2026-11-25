"""QA r02 de T-201 (revisor): cambios a propósito que no prueban ni `sensibilidad.py` ni `r02_sensibilidad_equivalencia.py`.

Uso: python r07_sensibilidad_extra.py <carpeta de equivalencia.sh> <comparar.py> <raiz_nuevo (…/bloque_a)>
Lo que queda enmascarado tras la r02 son las rutas, las dos latencias y los resúmenes encadenados. Aquí se comprueba que el
enmascarado de los resúmenes no se come lo que tienen al lado (el número de entradas de cada sello, una huella corta de RC, la
columna `uc` de consumo.csv, una latencia con otro nombre) y que el cambio de solo un resumen, que sí se enmascara a
propósito porque su contenido se compara entrada a entrada, da EQUIVALENTE. Cada cambio se deshace al acabar.
"""
import re
import subprocess
import sys
from pathlib import Path

EQ, COMPARAR, RAIZ_NUEVO = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
CASOS = [
    ("sellos: número de entradas de F1", "estado/sellos_integridad.json", r'"F1": \[(\d+),', r'"F1": [99,', "DISTINTO"),
    ("RC: huella corta de un dato", "estado/RC_registro_calculos.jsonl", r'"huella": "([0-9a-f])', r'"huella": "Z', "DISTINTO"),
    ("consumo.csv: uc de la primera fila", "bt/consumo.csv", r"(?m)^(RUN-2024-0001,(?:[^,\r\n]*,){9})[0-9.]+,", r"\g<1>99.9,",
     "DISTINTO"),
    ("F3: clave nueva con nombre de latencia («latencia»)", "estado/F3_registro_oportunidades.jsonl", r'"liquidez": "alta"',
     '"latencia": 1, "liquidez": "alta"', "DISTINTO"),
    ("sellos: solo el resumen de F1 (se enmascara a propósito)", "estado/sellos_integridad.json", r'"F1": \[(\d+), "[0-9a-f]',
     r'"F1": [\1, "0', "EQUIVALENTE"),
]
fallos = []
for nombre, rel, pat, sus, esperado in CASOS:
    f = EQ / "r_nuevo" / rel
    original = f.read_bytes()
    texto = original.decode("utf-8")
    nuevo, n = re.subn(pat, sus, texto, count=1)
    if not n or nuevo == texto:
        print(f"  FALLO {nombre}: el patrón no aparece")
        fallos.append(nombre)
        continue
    try:
        f.write_bytes(nuevo.encode("utf-8"))
        r = subprocess.run([sys.executable, "-I", str(COMPARAR), str(EQ / "r_base"), str(EQ / "r_nuevo"), str(EQ / "base" / "bloque_a"),
                            str(RAIZ_NUEVO)], capture_output=True, text=True, check=False)
    finally:
        f.write_bytes(original)
    ver = "DISTINTO" if r.returncode else "EQUIVALENTE"
    print(f"  {'OK   ' if ver == esperado else 'FALLO'} {nombre}: {ver} (esperado {esperado})")
    if ver != esperado:
        fallos.append(nombre)
print("puntos ciegos:", fallos or "ninguno")
sys.exit(1 if fallos else 0)
