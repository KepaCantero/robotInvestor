"""QA r03 de T-88 · 03: mutantes de la ronda r03 (grupo por analista en la V5, `cierres_parciales` ordenados), con el motor de
r01_mutar.py, sobre una COPIA completa del repo (worktree con `bloque_a` entero).

  .venv/bin/python -I .docs/tickets/T-88/revisores/r03_03_mutantes.py RAIZ_DE_UNA_COPIA [--sin-suite] [--solo=R1,R2] [--suite=...]

Primero `tests/test_t88_consumo.py`; si sobrevive, la segunda etapa (--suite); si sigue vivo, los detectores propios
(r03_02 V P S y r02_02 no se lanza aquí por coste)."""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from r01_mutar import ejecutar  # noqa: E402

O = "bloque_a/orquestacion.py"
G = '        grupo = "ANALISTAS" if (self.v6 and agente in set(AGENTE_CLASE.values())) else agente\n'
CI = 'sorted(presupuesto.cierres, key=lambda c: (c["clase"], c["fase"], c["motivo"]))'
MUTANTES = [
    ("R1", "vuelta a la r02 (H-05): en la V5 los analistas comparten el grupo ANALISTAS", O, G,
     '        grupo = "ANALISTAS" if agente in set(AGENTE_CLASE.values()) else agente\n'),
    ("R2", "en la V6 cada analista es su propio grupo (sin el núcleo común)", O, G, "        grupo = agente\n"),
    ("R3", "un único grupo para todo", O, G, '        grupo = "TODOS"\n'),
    ("R4", "vuelta atrás de H-09: `cierres_parciales` en el orden de llegada", O, CI, "presupuesto.cierres"),
    ("R5", "`cierres_parciales` ordenado solo por tipo (orden de fases y motivos de llegada)", O, CI,
     'sorted(presupuesto.cierres, key=lambda c: c["clase"])'),
]
DET = [("r03_02 V P S", [AQUI / "r03_02_grupos_v5_v6.py", "--ejecutor", "{EJ}"])]
ejecutar(MUTANTES, ["tests/test_t88_consumo.py"], DET)
