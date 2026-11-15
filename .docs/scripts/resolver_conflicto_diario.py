"""Resuelve un conflicto de rebase en el diario mensual juntando las dos versiones (nada se borra de .docs/).

Durante un `git pull --rebase`, el bloque HEAD trae las entradas que otra sesión subió antes y el otro bloque, las del
commit que se reaplica. Las del commit que se reaplica van arriba (son las más recientes) y las de HEAD debajo.
Uso: python3 .docs/scripts/resolver_conflicto_diario.py <fichero> [<fichero> ...]"""
import sys
from pathlib import Path


def resolver(texto: str) -> str:
    while "<<<<<<< " in texto:
        a = texto.index("<<<<<<< ")
        m = texto.index("\n=======\n", a)
        b = texto.index("\n>>>>>>> ", m)
        fin = texto.find("\n", b + 1)
        fin = len(texto) if fin < 0 else fin + 1
        arriba = texto[texto.index("\n", a) + 1:m]
        abajo = texto[m + len("\n=======\n"):b]
        texto = texto[:a] + abajo.rstrip("\n") + "\n\n" + arriba.rstrip("\n") + "\n" + texto[fin:]
    return texto


for f in sys.argv[1:]:
    p = Path(f)
    original = p.read_text(encoding="utf-8")
    nuevo = resolver(original)
    p.write_text(nuevo, encoding="utf-8")
    print(f"{f}: conflicto resuelto juntando las dos versiones" if nuevo != original else f"{f}: sin conflicto")
