"""QA r04 de T-143 · D12 (r02) y D29 (r03), cuyo anclaje cambió en la r04, adaptados al texto nuevo (como D23b en la r03).

Mismo procedimiento que `r01_03_mutantes.py` (importado: copia fuera del repositorio, un cambio, `goldens_ct.py --update
--motivo` y `tests/test_fase3_goldens.py`), con `-x` en pytest. Desde la raíz, con el Python del .venv:

    .venv/bin/python .docs/tickets/T-143/revisores/r04_03_mutantes_adaptados.py DESTINO [ID ...]

«muere»: lo cubren las pruebas r04 según `pruebas.md`; «?»: nadie dice cubrirlo. Termina con 1 si un «muere» sobrevive o no
aplica. Sin red.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("r01_03", AQUI / "r01_03_mutantes.py")
r01 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r01)

DOC0, ORQ = r01.DOC0, r01.ORQ

MUTANTES = [
    ("D12b", DOC0, "`lectura_conjunto`, `preguntas_sugeridas` y `limitaciones`. Los campos de integración",
     "`lectura_conjunto` y `preguntas_sugeridas`. Los campos de integración", "muere", "CT-15: SINTESIS sin `limitaciones` en la prosa (D12 de la r02)"),
    ("D29b", DOC0, (" En el diseño V6 (con `v6.sintetizador`, el valor por defecto) no hay orden INTEGRACION ni su retorno: el código "
                    "calcula antes de G3 el régimen de cada tipo y los cambios frente al run anterior, y el Sintetizador escribe después "
                    "la integración con `SINTESIS` (CT-15). Con `v6.sintetizador` desactivado, el V6 emite la orden INTEGRACION como el V5."),
     "", "muere", "CT-05: sin la nota del V6 (D29 de la r03)"),
]

_ejecutar = r01.ejecutar


def _ejecutar_x(args, cwd, limite=1800):
    if "pytest" in args:
        args = [*args, "-x"]
    return _ejecutar(args, cwd, limite)


if __name__ == "__main__":
    r01.MUTANTES = MUTANTES
    r01.ejecutar = _ejecutar_x
    sys.exit(r01.main(sys.argv[1:]))
