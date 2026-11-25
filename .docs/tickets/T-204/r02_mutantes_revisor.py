"""T-204 r02: ejecuta los mutantes del revisor (`revisores/r01_03_mutantes.py`) sin cambiar su script.
Solo Q1 se adapta. Su texto original («RETIRADOS[retirado] not in linea») ya no existe, porque la r02 busca la marca como
palabra con `marcada()` (H-06). El mutante equivalente («la marca vale como prefijo (T-20)») se aplica al código nuevo, y
los nueve restantes se aplican tal cual.
Uso (desde la raíz): .venv/bin/python .docs/tickets/T-204/r02_mutantes_revisor.py"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
fuente = (AQUI / "revisores" / "r01_03_mutantes.py").read_text(encoding="utf-8")
viejo = """    ("Q1 la marca vale como prefijo (T-20)", REFS, "RETIRADOS[retirado] not in linea", '"T-20" not in linea'),"""
nuevo = """    ("Q1 la marca vale como prefijo (T-20) [r02: sobre marcada()]", REFS, "not marcada(linea, RETIRADOS[retirado])",
     '"T-20" not in linea'),"""
assert fuente.count(viejo) == 1
sys.argv = [str(AQUI / "revisores" / "r01_03_mutantes.py")]
exec(compile(fuente.replace(viejo, nuevo), sys.argv[0], "exec"), {"__file__": sys.argv[0], "__name__": "__main__"})
