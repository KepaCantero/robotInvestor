"""QA r01 de T-130 · lo que T-130 cambia frente a la r02 de T-123 (commit anterior, 08b357e~1) en los casos de r01_01:
¿los IBAN con letras que ya no se detectan, la fila CSV con campo numérico y las filas de cuatro cifras con un espacio son
regresiones de T-130 o ya estaban?

Carga de `git show <commit>:bloque_a/11_Ejecutor/bloque_a/contratos.py` el tramo entre `LONGITUD_IBAN = {` y
`def secretos_en_texto`. Uso (desde la raíz de la copia git): python -I r01_02_comparacion_r02.py
"""
import random
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "bloque_a" / "11_Ejecutor"))
from bloque_a import contratos as ahora  # noqa: E402


def cargar(commit):
    src = subprocess.run(["git", "show", f"{commit}:bloque_a/11_Ejecutor/bloque_a/contratos.py"], cwd=RAIZ,
                         capture_output=True, text=True, check=True).stdout
    tramo = src[src.index("LONGITUD_IBAN = {"):src.index("def secretos_en_texto")]
    ns = {"re": re}
    exec(tramo, ns)
    return ns


antes = cargar("08b357e~1")


def iban(pais, bban):
    num = "".join(str(int(c, 36)) for c in bban + pais + "00")
    return f"{pais}{98 - int(num) % 97:02d}{bban}"


def g4(s):
    return " ".join(s[i:i + 4] for i in range(0, len(s), 4))


CASOS = {"RO Banca Transilvania (BTRL RONCRT …)": iban("RO", "BTRL" + "RONCRT" + "0V12345678"),
         "RO ejemplo del registro": "RO49" + "AAAA" + "1B31007593840000",
         "CY con letras en la cuenta": iban("CY", "002" + "00128" + "AB00000012005276"),
         "LV con 6 letras": iban("LV", "BANK" + "XY00435195001"),
         "IT con letras en la cuenta": iban("IT", "X" + "05428" + "11101" + "CC0000123456")}
print("IBAN (junto y en grupos de 4): r02 → T-130")
for k, s in CASOS.items():
    for forma in (s, g4(s)):
        print(f"  {k:40} {'grupos' if ' ' in forma else 'junto '}: "
              f"{bool(antes['ibanes_en_texto'](forma))} → {bool(ahora.ibanes_en_texto(forma))}")

VISA = "4111" + "1111" + "1111" + "1111"
print("tarjetas: r02 → T-130")
for k, t in {"17,<tarjeta>,12/27": "17," + VISA + ",12/27", "[17,<tarjeta>]": "[17," + VISA + "]",
             "Juan,<tarjeta>": "Juan," + VISA}.items():
    print(f"  {k:40} {bool(antes['tarjetas_en_texto'](t))} → {bool(ahora.tarjetas_en_texto(t))}")

rng = random.Random(7)
for sep, nombre in ((" ", "un espacio"), ("  ", "dos espacios"), ("\n", "salto de línea")):
    filas = [sep.join(str(rng.randint(4000, 5999)) for _ in range(8)) for _ in range(5000)]
    a = sum(bool(antes["tarjetas_en_texto"](f)) for f in filas)
    b = sum(bool(ahora.tarjetas_en_texto(f)) for f in filas)
    print(f"  8 niveles de 4 cifras (4000–5999), {nombre:15}: r02 {a}/5000 → T-130 {b}/5000")
filas = [" ".join(str(rng.randint(1000, 9999)) for _ in range(4)) for _ in range(20000)]
print(f"  4 enteros de 4 cifras al azar, un espacio: T-130 {sum(bool(ahora.tarjetas_en_texto(f)) for f in filas)}/20000 "
      "(INC-T123-01 declara «unas 2 de cada 100»)")
