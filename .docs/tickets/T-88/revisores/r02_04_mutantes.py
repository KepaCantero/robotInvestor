"""QA r02 de T-88 · 04: mutantes de la ronda r02 (consumo.py y orquestacion.py), con el motor de r01_mutar.py.

  .venv/bin/python -I .docs/tickets/T-88/revisores/r02_04_mutantes.py RAIZ_DE_UNA_COPIA [--sin-suite] [--solo=P1,P2] [--suite=...]

Primero las pruebas del ticket; si sobrevive, la segunda etapa (--suite o la suite entera); si sigue vivo, los detectores
propios (r02_01 --rapido y r02_03 A)."""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from r01_mutar import ejecutar  # noqa: E402

C, O = "bloque_a/consumo.py", "bloque_a/orquestacion.py"
MUTANTES = [
    ("P1", "durante la fase nadie carga prima (tampoco el analista propio)", O,
     "        propio = AGENTE_CLASE.get(bolsa) == agente\n", "        propio = False\n"),
    ("P2", "vuelta a la r01: todos cargan la prima «solo» durante la fase", O,
     "        propio = AGENTE_CLASE.get(bolsa) == agente\n", "        propio = True\n"),
    ("P3", "vuelta a la r01: un único grupo para todos los prefijos", O,
     '        grupo = "ANALISTAS" if agente in set(AGENTE_CLASE.values()) else agente\n', '        grupo = "TODOS"\n'),
    ("P4", "un grupo por agente (analistas por separado)", O,
     '        grupo = "ANALISTAS" if agente in set(AGENTE_CLASE.values()) else agente\n', "        grupo = agente\n"),
    ("P5", "la liquidación no descuenta lo ya cargado", C,
     "            for bolsa in sorted(self._cargadas):\n                self.consumido[bolsa] -= self._uc_prima(self._cargadas[bolsa])\n",
     ""),
    ("P6", "un grupo sin pesos no va a la bolsa común", C,
     '                    self.consumido["COMUN"] += self._uc_prima(reales)\n', "                    pass\n"),
    ("P7", "sin la liquidación tras la fase en paralelo", O, "        presupuesto.liquidar_primas()   # T-88", "        pass   # T-88"),
    ("P8", "prefijo sin dividir por los intentos", O, "prefijo = cacheados // max(1, r.intentos)", "prefijo = cacheados"),
    ("P9", "cada llamada tiene prima «solo» (no solo la primera de cada agente en la bolsa)", O,
     "solo = prefijo if presupuesto.primera_llamada(bolsa, agente) else 0", "solo = prefijo"),
    ("P10", "el analista propio carga su escritura real en vez de la prima «solo»", O,
     "presupuesto.cargar_con_prima(bolsa, grupo, leido, solo, solo if propio else 0, u.cache_escritura)",
     "presupuesto.cargar_con_prima(bolsa, grupo, leido, solo, u.cache_escritura if propio else 0, u.cache_escritura)"),
    ("P11", "la liquidación no vacía lo cargado (una segunda liquidación descuenta otra vez)", C,
     "            self._cargadas.clear()\n", ""),
    ("P12", "los pesos son los tokens reales y no la prima «solo»", C,
     "            self._pesos[grupo][bolsa] += int(tokens_solo)\n", "            self._pesos[grupo][bolsa] += int(tokens_reales)\n"),
    ("P13", "resumen() no liquida", C, "        self.liquidar_primas()\n        with self._lock:\n            return {k:",
     "        with self._lock:\n            return {k:"),
]
DET = [("r02_01 --rapido", [AQUI / "r02_01_determinismo_fase_y_total.py", "--ejecutor", "{EJ}", "--rapido"]),
       ("r02_03 A", [AQUI / "r02_03_grupos_y_mezcla.py", "--ejecutor", "{EJ}", "A"])]
ejecutar(MUTANTES, ["tests/test_t88_consumo.py"], DET)
