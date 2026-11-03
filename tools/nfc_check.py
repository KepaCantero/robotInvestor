#!/usr/bin/env python3
"""Gate NFC: ningún nombre de archivo del repo puede quedar en forma NFD.

Lección pagada dos veces (V5.0 y cada recarga en macOS): las carpetas extraídas
de entregas llegan con nombres NFD y el código compara cadenas NFC — en Linux
pasan los tests y en macOS no. Este gate lo detecta antes de que rompa nada.
"""
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EXCLUIR = {".git", ".venv", "__pycache__", ".pytest_cache"}


def main() -> int:
    malos = []
    for p in RAIZ.rglob("*"):
        if any(part in EXCLUIR for part in p.relative_to(RAIZ).parts):
            continue
        if p.name != unicodedata.normalize("NFC", p.name):
            malos.append(str(p.relative_to(RAIZ)))
    if malos:
        for m in malos[:20]:
            print(f"  NFD: {m}")
        print(f"FALLO: {len(malos)} nombres en NFD; renormalizar a NFC.")
        return 1
    print("NFC: todos los nombres de archivo en forma canónica.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
