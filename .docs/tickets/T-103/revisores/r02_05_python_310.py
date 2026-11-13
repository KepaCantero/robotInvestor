"""QA r02 de T-103 (revisor independiente): ¿el R8 de la r02 carga con el Python mínimo que declara el paquete?

Uso: python -I r02_05_python_310.py <python 3.10> <ruta a bloque_a/11_Ejecutor en 7feb697> <ruta anterior>
     (un Python 3.10 se obtiene, por ejemplo, con `uv python install 3.10` y `uv python find 3.10`)

`pyproject.toml` declara `requires-python = ">=3.10"` y el README del ejecutor «Python ≥ 3.10». Los cuantificadores posesivos
(`\\\\++`) existen desde Python 3.11: en 3.10 `re.compile` lanza «multiple repeat». Se comprueba:
 1. si `bloque_a.contratos` (solo biblioteca estándar) se importa con ese Python, antes y después de la r02;
 2. qué ficheros del paquete no compilan con ese Python (sintaxis), antes y después;
 3. que la variante sin posesivo (solo el lookbehind) compila en 3.10.
Es INFO salvo que la r02 sea lo primero que rompe 3.10. Sin red.
"""
import subprocess
import sys
from pathlib import Path

PY = sys.argv[1]
NUEVO, ANTES = Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
fallos = 0

version = subprocess.run([PY, "-I", "-c", "import sys; print(sys.version.split()[0])"], capture_output=True, text=True).stdout.strip()
print(f"INFO  intérprete: {version}")
IMPORTA = "import sys; sys.path.insert(0, sys.argv[1]); import bloque_a.contratos as c; print('importa')"
SINTAXIS = r"""
import pathlib, sys
malos = []
for p in sorted(pathlib.Path(sys.argv[1], "bloque_a").rglob("*.py")):
    try:
        compile(p.read_text(encoding="utf-8"), str(p), "exec", dont_inherit=True)
    except SyntaxError as e:
        malos.append(f"{p.name}:{e.lineno}")
print(" ".join(malos) or "ninguno")
"""
res = {}
for nombre, ruta in (("antes", ANTES), ("r02", NUEVO)):
    r = subprocess.run([PY, "-I", "-c", IMPORTA, str(ruta)], capture_output=True, text=True)
    imp = r.stdout.strip() or (r.stderr.strip().splitlines() or ["?"])[-1]
    sx = subprocess.run([PY, "-I", "-c", SINTAXIS, str(ruta)], capture_output=True, text=True).stdout.strip()
    res[nombre] = (imp, sx)
    print(f"INFO  {nombre}: import bloque_a.contratos → {imp} · no compilan: {sx}")
var = subprocess.run([PY, "-I", "-c", r"import re; re.compile(r'(?<!\\)\\+(?:u[0-9a-fA-F]{4}|[ntrbf/\"])'); print('compila')"],
                     capture_output=True, text=True)
print(f"INFO  variante sin posesivo en {version}: {var.stdout.strip() or var.stderr.strip().splitlines()[-1]}")
primera_rotura = res["antes"][0] == "importa" and res["antes"][1] == "ninguno" and res["r02"][0] != "importa"
if primera_rotura:
    fallos += 1
    print("FALLO la r02 es lo primero que impide cargar el paquete con el Python mínimo declarado")
else:
    print("INFO  el paquete ya no cargaba entero con ese Python antes de la r02; la r02 añade el núcleo de R8 a lo que no carga")
print(f"fallos: {fallos}")
sys.exit(1 if fallos else 0)
