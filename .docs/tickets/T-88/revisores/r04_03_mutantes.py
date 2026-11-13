"""QA r04 de T-88 · 03: mutantes de la ronda r04 (el `consumo` del RUN de F5, `estado()` y el orden de `cierres_parciales`) y
dos de la liquidación que no cubrían las rondas anteriores, con el motor de r01_mutar.py, sobre una COPIA completa del repo.

  .venv/bin/python -I .docs/tickets/T-88/revisores/r04_03_mutantes.py RAIZ_DE_UNA_COPIA [--sin-suite] [--solo=S1,S2] [--suite=...]

Primero `tests/test_t88_consumo.py`; si sobrevive, la segunda etapa (--suite o la suite entera)."""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from r01_mutar import ejecutar  # noqa: E402

O, C = "bloque_a/orquestacion.py", "bloque_a/consumo.py"
CONS = '            "consumo": {k: cons[k] for k in ("llamadas", "uc", "uc_llm", "uc_motor", "entrada", "salida", "cache_escritura", "cache_lectura")},\n'
CI = 'sorted(presupuesto.cierres, key=lambda c: (c["clase"], c["fase"], c["motivo"]))'
MUTANTES = [
    ("S1", "vuelta atrás de H-10: el RUN de F5 sin `consumo`", O, CONS, ""),
    ("S2", "`consumo` sin `uc_motor`", O, CONS, CONS.replace(' "uc_motor",', "")),
    ("S3", "`consumo` sin `uc` (estado() da None)", O, CONS, CONS.replace(' "uc",', "", 1)),
    ("S4", "`cierres_parciales` por tipo y fase, sin el motivo", O, CI, 'sorted(presupuesto.cierres, key=lambda c: (c["clase"], c["fase"]))'),
    ("S5", "`cierres_parciales` en orden inverso", O, CI, CI[:-1] + ", reverse=True)"),
    ("S6", "los tokens reales del grupo son los pesos «solo»", C, "            self._reales[grupo] += int(tokens_reales)\n",
     "            self._reales[grupo] += int(tokens_solo)\n"),
    ("S7", "estado() no lee el `uc` del RUN", O, '"uc": (r.get("consumo") or {}).get("uc")', '"uc": None'),
]
ejecutar(MUTANTES, ["tests/test_t88_consumo.py"])
