"""QA, ronda de cierre de T-204: la limpieza de `.docs/` tras rebasar sobre develop (T-196, T-201 y T-203).
1. `limpiar_docs.py` sin opciones no propone ningún cambio: lo que develop trajo después de la limpieza también está limpio,
   o se ha declarado en INC-T204-03 que se queda como registro.
2. `limpiar()` deja intactas las líneas de evidencia medida que traen esos tickets (recuentos con «Pytest:» o «Mypy:» en
   mayúscula, o la continuación de una línea de recuentos).
Uso (desde la raíz): .venv/bin/python -I .docs/tickets/T-204/revisores/r04_02_limpieza_tras_rebase.py. Sale con 1 si hay casos."""
import importlib.util
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
SCRIPT = RAIZ / ".docs" / "tickets" / "T-204" / "limpiar_docs.py"
casos = []
salida = subprocess.run([sys.executable, "-I", str(SCRIPT)], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
ultima = salida.strip().splitlines()[-1]
inc = (RAIZ / "docs" / "incidencias.md").read_text(encoding="utf-8")
inc03 = inc[inc.index("**INC-T204-03"):]
inc03 = inc03[:inc03.find("\n**INC-", 1)]
if not ultima.startswith("0 ") and not all(t in inc03 for t in ("T-196", "T-201", "T-203")):
    casos.append(f"limpiar_docs.py propone cambios tras el rebase ({ultima}) y INC-T204-03 no dice que se quedan")
spec = importlib.util.spec_from_file_location("limpiar_t204", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for linea in ("  - Pytest: A 8415 (antes 8400), FX 68, B 176.", "  - Mypy: A 102, FX 174, B 159, todos en su cuota.",
              "  T-201 sola), A-Forex 174, B 159. **Equivalencia** de la combinación contra la base: **IGUALES** (90 ficheros)."):
    nuevo, cambios = mod.limpiar(linea)
    if nuevo != linea:
        casos.append(f"limpiar() reescribe evidencia medida: {linea.strip()[:90]} → {nuevo.strip()[:90]}")
print(f"{len(casos)} casos")
for c in casos:
    print("  " + c)
sys.exit(1 if casos else 0)
