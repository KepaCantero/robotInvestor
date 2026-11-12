"""QA r01 de T-100 (V0.76): vuelve a ejecutar una sonda r03 de T-76 escrita para la V0.75, cuando `movimiento_sombra` no tenía
referencia. Con la V0.76, esas llamadas sin `ref` darían O-01 y la sonda no mediría nada; aquí se les pone una referencia
determinista sacada del propio movimiento (tipo, importe e instante), que es lo que haría G con el identificador del
intermediario: el mismo movimiento declarado otra vez lleva la misma referencia, y dos movimientos distintos, referencias
distintas. Con esto, F2 y F2b (T-76 H-17) miden lo que la V0.76 corrige. Datos SIMULADOS.

Uso (desde la raíz del repositorio):
    .venv/bin/python -I .docs/tickets/T-100/revisores/r01_05_rejecuta_r03.py <sonda r03 de T-76> [ruta del marco]
"""
import functools
import hashlib
import runpy
import sys
from pathlib import Path

SONDA = Path(sys.argv[1]).resolve()
MARCO = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path(__file__).resolve().parents[4] / "sistema_global" / "marco_comun_c"
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
import orquestador as oq  # noqa: E402

_orig = oq.Orquestador.movimiento_sombra


@functools.wraps(_orig)
def _con_ref(self, tipo, importe_eur, precio_indice, actor, ahora, ref=None):
    if ref is None:
        ref = "AUTO-" + hashlib.sha256(repr((tipo, importe_eur, ahora)).encode()).hexdigest()[:16]
    return _orig(self, tipo, importe_eur, precio_indice, actor, ahora, ref=ref)


oq.Orquestador.movimiento_sombra = _con_ref
sys.argv = [str(SONDA), str(MARCO)]
runpy.run_path(str(SONDA), run_name="__main__")
