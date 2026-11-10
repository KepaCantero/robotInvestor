# -*- coding: utf-8 -*-
"""Sondas de no-vacuidad de la batería dorada (V0.66, pieza 7 del kit 2).

Cada sonda muta `pruebas/doradas.py` en una COPIA del árbol (en una carpeta temporal; el árbol real no se
toca) y corre ahí `pruebas/pruebas_doradas.py`. La batería está bien hecha si cae en las cinco: sin ella,
una sonda que pase diría que hay una comprobación que no prueba lo que dice.

Las cinco mutaciones: S1 sin redondeo de las cantidades, S2 sin quitar los «motivo», S3 con el
kill-switch siempre a False, S4 con el comparador vacío y S5 con las claves sin ordenar al escribir.

Uso (desde la carpeta marcoC): python3 entrega_glm/V0.66/sondas_no_vacuidad_v066.py
Salida: una línea por sonda («CAZADA» si la batería falla con la mutación, «VACUA» si no) y el resultado.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent          # entrega_glm/V0.66
RAIZ = AQUI.parent.parent                       # marcoC
MUTACIONES = [
    ("S1_sin_redondeo", "return round(x, DECIMALES)", "return x"),
    ("S2_con_motivo", '            if ks == "motivo":\n                continue', "            pass"),
    ("S3_kill_fijo_falso", 'e["kill"] = o.kill is not None', 'e["kill"] = False'),
    ("S4_comparador_vacio", "    if not isinstance(antigua, list) or not isinstance(nueva, list):",
     "    return []\n    if not isinstance(antigua, list) or not isinstance(nueva, list):"),
    ("S5_claves_sin_ordenar", 'sort_keys=True, allow_nan=False) + "\\n"', 'sort_keys=False, allow_nan=False) + "\\n"'),
]


def sonda(nombre, viejo, nuevo):
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / "marcoC"
        shutil.copytree(RAIZ, copia, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        mod = copia / "pruebas" / "doradas.py"
        texto = mod.read_text(encoding="utf-8")
        if viejo not in texto:
            return f"VACUA (la mutación {nombre} no se pudo aplicar: el texto cambió)"
        mod.write_text(texto.replace(viejo, nuevo, 1), encoding="utf-8")
        r = subprocess.run([sys.executable, str(copia / "pruebas" / "pruebas_doradas.py")],
                           capture_output=True, text=True, cwd=str(copia))
        cayo = r.returncode != 0 and "HAY FALLOS" in r.stdout
        malas = [l.split()[1] for l in r.stdout.splitlines() if l.startswith("FALLA")] if cayo else []
        return f"CAZADA (la batería falla en: {', '.join(malas[:4])})" if cayo else f"VACUA (exit={r.returncode})"


def main():
    print("Sondas de no-vacuidad de la batería dorada (cada una muta una copia del árbol):")
    resultado = []
    for nombre, viejo, nuevo in MUTACIONES:
        r = sonda(nombre, viejo, nuevo)
        resultado.append("VACUA" not in r)
        print(f"  {nombre}: {r}")
    print("RESULTADO SONDA DORADAS:", "LAS CINCO CAZADAS" if all(resultado) else "HAY SONDA VACUA")
    return 0 if all(resultado) else 1


if __name__ == "__main__":
    sys.exit(main())
