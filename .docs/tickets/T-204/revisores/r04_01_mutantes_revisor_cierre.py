"""QA, ronda de cierre de T-204: ejecuta los mutantes del revisor (`r01_03_mutantes.py`) sobre la punta rebasada, sin cambiar
ese script. Se adaptan dos textos que ya no existen: Q1 (la marca, desde la r02 con `marcada()`) y Q4 (la cuota de ruff,
1533 tras rebasar sobre T-201 y T-203; el mutante vuelve a sumar las 1202 líneas del Forex: 2735).
Uso (desde la raíz): .venv/bin/python .docs/tickets/T-204/revisores/r04_01_mutantes_revisor_cierre.py"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
fuente = (AQUI / "r01_03_mutantes.py").read_text(encoding="utf-8")
cambios = [
    ("""    ("Q1 la marca vale como prefijo (T-20)", REFS, "RETIRADOS[retirado] not in linea", '"T-20" not in linea'),""",
     """    ("Q1 la marca vale como prefijo (T-20)", REFS, "not marcada(linea, RETIRADOS[retirado])", '"T-20" not in linea'),"""),
    ("""    ("Q4 la cuota de ruff sigue contando el Forex", CUO, "ruff=1604", "ruff=2806"),""",
     """    ("Q4 la cuota de ruff sigue contando el Forex", CUO, "ruff=1533", "ruff=2735"),"""),
]
for viejo, nuevo in cambios:
    assert fuente.count(viejo) == 1, viejo
    fuente = fuente.replace(viejo, nuevo)
sys.argv = [str(AQUI / "r01_03_mutantes.py")]
exec(compile(fuente, sys.argv[0], "exec"), {"__file__": sys.argv[0], "__name__": "__main__"})
