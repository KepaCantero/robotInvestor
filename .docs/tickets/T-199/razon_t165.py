"""T-199: razón largo/corto de la prueba de T-165 con un montón grande (como a mitad de suite), antes y después.
Uso (desde bloque_a/11_Ejecutor/tests, con la carga de carga.sh si se quiere): PYTHONPATH=. python ../../../.docs/tickets/T-199/razon_t165.py [CORTO]
CORTO: unidades del texto corto (2000 la prueba de develop; 1000 la de T-199); el largo es 8000."""
import sys
import time

import test_t165_g3_met13 as T
from tiempo_cpu import minimos_intercalados

corto_n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
basura = [{"a": [i]} for i in range(6_000_000)]   # objetos vivos, como los que dejan las pruebas anteriores


def una(t):
    c = time.process_time()
    T._real(t)
    return time.process_time() - c


T._real("ST-DESC-001")
peor_viejo = peor_nuevo = 0.0
for ronda in range(5):
    for u in ("no está validado, ", "ST-DESC-001 implementado. ", "VOL GARCH 001 y ST-DESC-001; "):
        c, l = una(u * corto_n), una(u * 8000)
        c2, l2 = minimos_intercalados(lambda u=u: T._real(u * corto_n), lambda u=u: T._real(u * 8000))
        rv, rn = l / max(c, 0.02), l2 / max(c2, 0.02)
        peor_viejo, peor_nuevo = max(peor_viejo, rv), max(peor_nuevo, rn)
        print(ronda, u[:8], f"una medida {rv:.2f}  mínima de 3 intercaladas {rn:.2f}", flush=True)
print(f"PEOR: una medida {peor_viejo:.2f}; mínima de 3 intercaladas {peor_nuevo:.2f}")
