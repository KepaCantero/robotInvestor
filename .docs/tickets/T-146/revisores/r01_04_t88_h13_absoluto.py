"""QA r01 de T-146 · `test_r04_h13` cambió su «base»: ¿lo que acaba pagando cada bolsa es el mismo que antes de T-146?

Uso: python -I r01_04_t88_h13_absoluto.py <11_Ejecutor de antes> <11_Ejecutor de después> [--compartido]
(--compartido añade AG-10, que escribe en RV y lee y luego reescribe en RF: cambia a propósito, matiza INC-T88-01)
Repite la secuencia de la prueba (RV y RF con su analista; RV reescribe su prompt) en cada código y en un subproceso aparte,
e imprime lo consumido por bolsa tras liquidar. Deben coincidir."""
import json
import subprocess
import sys

CODIGO = r'''
import json, sys
from types import SimpleNamespace
sys.path.insert(0, sys.argv[1])
from bloque_a.configuracion import cargar_config
from bloque_a.consumo import Contabilidad, Presupuesto
from bloque_a.llm import Uso
from bloque_a.orquestacion import Bloque
cfg = cargar_config()
fake = SimpleNamespace(contabilidad=Contabilidad(cfg), v6=False)
p = Presupuesto({"RV": 50, "RF": 50, "COMUN": 50}, cfg)
def r(e, l):
    return SimpleNamespace(uso=Uso(entrada=1000, salida=500, cache_escritura=e, cache_lectura=l), cache_hit=False, intentos=1, uc=0.0)
Bloque._cargar(fake, p, "RV", "AG-03", r(10000, 0))
Bloque._cargar(fake, p, "RF", "AG-04", r(20000, 0))
Bloque._cargar(fake, p, "RV", "AG-03", r(10000, 0))
# y un agente compartido (AG-10) que escribe en RV y lee en RF, con una reescritura en RF
if "--compartido" in sys.argv: Bloque._cargar(fake, p, "RV", "AG-10", r(15000, 0))
if "--compartido" in sys.argv: Bloque._cargar(fake, p, "RF", "AG-10", r(0, 15000))
if "--compartido" in sys.argv: Bloque._cargar(fake, p, "RF", "AG-10", r(15000, 0))
p.liquidar_primas()
print(json.dumps({k: round(v, 6) for k, v in sorted(p.consumido.items())}))
'''
res = [json.loads(subprocess.run([sys.executable, "-I", "-c", CODIGO, d], capture_output=True, text=True, check=True).stdout)
       for d in sys.argv[1:3]]
if "--compartido" in sys.argv:
    res = [json.loads(subprocess.run([sys.executable, "-I", "-c", CODIGO, d, "--compartido"], capture_output=True, text=True,
                                     check=True).stdout) for d in sys.argv[1:3]]
print("antes  ", res[0])
print("después", res[1])
print("IGUAL" if res[0] == res[1] else "DISTINTO")
