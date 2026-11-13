"""QA r01 de T-88 · 04: mutantes de la corrección (consumo.py y orquestacion.py). Uso en r01_mutar.py.

  .venv/bin/python -I .docs/tickets/T-88/revisores/r01_04_mutantes.py RAIZ_DE_UNA_COPIA [--sin-suite] [--solo=M1,M3]"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from r01_mutar import ejecutar  # noqa: E402

C, O = "bloque_a/consumo.py", "bloque_a/orquestacion.py"
MUTANTES = [
    ("M1", "vuelta atrás: cada llamada carga su coste real", O, "        if r.cache_hit or not cacheados:\n", "        if True:\n"),
    ("M2", "liquidar_primas no hace nada", C, "        with self._lock:\n            total_solo = sum(",
     "        return\n        with self._lock:\n            total_solo = sum("),
    ("M3", "sin la liquidación tras la fase en paralelo", O, "        presupuesto.liquidar_primas()   # T-88", "        pass   # T-88"),
    ("M4", "prefijo sin dividir por los intentos", O, "prefijo = cacheados // max(1, r.intentos)", "prefijo = cacheados"),
    ("M5", "primera llamada por agente, no por (bolsa, agente)", C,
     "            nuevo = (bolsa, agente) not in self._llamados\n            self._llamados.add((bolsa, agente))",
     "            nuevo = agente not in self._llamados\n            self._llamados.add(agente)"),
    ("M6", "sin primas «solo», lo real no va a la bolsa común", C, "            if not total_solo and self._primas_reales:", "            if False:"),
    ("M7", "prima sin descontar la lectura (1 − factor)", C,
     "0.5 * tokens * (1 - float(parametro(self.cfg, \"uc.factor_lectura_cache\")))", "0.5 * tokens"),
    ("M8", "resumen() no liquida", C, "        self.liquidar_primas()\n        with self._lock:\n            return {k:",
     "        with self._lock:\n            return {k:"),
    ("M9", "cada llamada paga la prima «solo»", O, "escrito = prefijo if presupuesto.primera_llamada(bolsa, agente) else 0", "escrito = prefijo"),
    ("M10", "la prima «solo» es la escritura real de la llamada", O,
     "presupuesto.cargar_con_prima(bolsa, leido, escrito, u.cache_escritura)",
     "presupuesto.cargar_con_prima(bolsa, leido, u.cache_escritura, u.cache_escritura)"),
    ("M11", "liquidación sin orden fijo de bolsas (sin sorted)", C, "for bolsa in sorted(self._primas_solo):", "for bolsa in list(self._primas_solo):"),
]
DET = [("r01_01 --rapido", [AQUI / "r01_01_determinismo_y_total.py", "--ejecutor", "{EJ}", "--rapido"])]
ejecutar(MUTANTES, ["tests/test_t88_consumo.py"], DET)
