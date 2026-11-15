#!/usr/bin/env python3
"""Ejecuta los mutantes de un script de revisor contra más pruebas que las que el script fija.

Los scripts de mutantes de la QA (`.docs/tickets/T-NN/revisores/rNN_*mutantes*.py`) fijan en `PRUEBAS = [...]` los ficheros de
prueba que había en su ronda. Cuando la ronda siguiente añade las pruebas nuevas en otro fichero (p. ej. `tests/test_t125_r02.py`),
este script ejecuta los MISMOS mutantes del revisor, sin cambiar su script, contra sus pruebas y las nuevas.

Uso, desde la raíz del repositorio:
    python .docs/scripts/mutantes_revisor_ampliado.py <script del revisor> <copia desechable con «_mut»> <prueba> [<prueba> …]
Las pruebas son rutas relativas a `11_Ejecutor` de la copia (las del script del revisor se conservan y van primero).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    if len(argv) < 4:
        print(__doc__)
        return 2
    script, copia, extra = Path(argv[1]), argv[2], argv[3:]
    fuente = script.read_text(encoding="utf-8")
    m = re.search(r"^PRUEBAS = (\[.*?\])$", fuente, flags=re.MULTILINE)
    if not m:
        print(f"{script}: no tiene una línea «PRUEBAS = [...]»")
        return 2
    pruebas = list(dict.fromkeys([*eval(m.group(1)), *extra]))   # noqa: S307 — lista literal del script del revisor
    fuente = fuente[:m.start()] + f"PRUEBAS = {pruebas!r}" + fuente[m.end():]
    print(f"pruebas: {pruebas}", flush=True)
    sys.argv = [str(script), copia]
    exec(compile(fuente, str(script), "exec"), {"__name__": "__main__", "__file__": str(script)})   # noqa: S102
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
