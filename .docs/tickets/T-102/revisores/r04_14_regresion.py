"""QA r04 de T-102 (revisor nuevo, ronda relanzada sobre `b36176a`) · Regresión de la r04 frente a la r03 con el banco de
control (`r04_10_banco_control.py`), y los bancos de las rondas anteriores con las dos versiones.

Ejecuta el banco de `r04_10` (opción `--lista`) con el código de dos raíces, en procesos aparte, y lista:
- las prohibidas que la raíz ANTES quitaba y la raíz DESPUÉS deja pasar (regresión);
- las legítimas que DESPUÉS se quitan y ANTES no (falsos positivos nuevos).

Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-102/revisores/r04_14_regresion.py <raiz_antes> <raiz_despues>
(p. ej. una copia de `5642ed0~1`, código de la r03, y una de `b36176a`). Sale con 1 si hay alguna regresión.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PY = str(Path(__file__).resolve().parents[4] / ".venv" / "bin" / "python")
LEGITIMAS = ("llana", "sigla", "marcador", "tiempo", "region")
PROHIBIDAS = ("r13_letra", "r13_marcador", "r21_sufijo", "r21_invisible", "r21_vehiculo")


def lista(raiz: str) -> dict[str, tuple[str, str]]:
    p = subprocess.run([PY, "-I", str(AQUI / "r04_10_banco_control.py"), raiz, "--lista"], capture_output=True, text=True,
                       timeout=900, check=False)
    out = {}
    for ln in p.stdout.splitlines():
        partes = ln.split("\t")
        if len(partes) == 3:
            out[partes[2]] = (partes[0], partes[1])
    if not out:
        raise SystemExit(f"sin salida de {raiz}: {p.stderr[-500:]}")
    return out


def main() -> int:
    antes, despues = lista(sys.argv[1]), lista(sys.argv[2])
    regresion = [(g, f) for f, (g, r) in despues.items() if g in PROHIBIDAS and r == "None" and antes[f][1] != "None"]
    nuevos_fp = [(g, r, f) for f, (g, r) in despues.items() if g in LEGITIMAS and r != "None" and antes[f][1] == "None"]
    mejoras = [(g, f) for f, (g, r) in despues.items() if g in PROHIBIDAS and r != "None" and antes[f][1] == "None"]
    print(f"Prohibidas que ANTES se quitaban y DESPUÉS pasan (regresión): {len(regresion)}")
    for g, f in regresion:
        print(f"  [{g}] antes {antes[f][1]} → pasa: {f}")
    print(f"Legítimas que DESPUÉS se quitan y ANTES no: {len(nuevos_fp)}")
    for g, r, f in nuevos_fp:
        print(f"  [{g}] ({r}) {f}")
    print(f"Prohibidas que DESPUÉS se quitan y ANTES pasaban (mejora): {len(mejoras)}")
    for g, f in mejoras:
        print(f"  [{g}] {f}")
    return 1 if regresion else 0


if __name__ == "__main__":
    sys.exit(main())
