"""QA r03 de T-76 (V0.75): vuelve a ejecutar las sondas de la r02 (`entrega_claude/V0.71/qa/r02_sondas_*.py`) contra la V0.75.

Uso: python3 -I .docs/tickets/T-76/revisores/r03_05_rejecuta_r02.py [juicio|calculo] [--sin-gracia]
Las sondas r02 se escribieron antes del plazo de gracia de O-42 (H-13): J1 a J4 esperan el aviso en el mismo instante del cierre y
J4 se para si no llega. Con --sin-gracia, el plazo de gracia por defecto de `comparaciones_sombra_pendientes` se pone a 0 en este
proceso (solo el valor por defecto del método; PARAMETROS y la configuración no cambian), para que las sondas r02 corran con sus
supuestos y lleguen a J5, J5c, J5b, J6 y siguientes. Termina con el código de la sonda.
"""
import runpy
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
MARCO = RAIZ / "sistema_global" / "marco_comun_c"
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
import orquestador as oq  # noqa: E402

cual = sys.argv[1] if len(sys.argv) > 1 else "juicio"
if "--sin-gracia" in sys.argv:
    f = oq.Orquestador.comparaciones_sombra_pendientes
    f.__defaults__ = (0,)
    print(f"(plazo de gracia por defecto puesto a 0 en este proceso; PARAMETROS sigue en {oq.PARAMETROS['i_dias_gracia_comparacion_sombra']})")
sys.argv = [sys.argv[0]]
runpy.run_path(str(MARCO / "entrega_claude" / "V0.71" / "qa" / f"r02_sondas_{cual}.py"), run_name="__main__")
