"""QA r04 de T-143 · Mutantes sobre lo que añadió la r04 (interruptores del V6 en CT-05, CT-11, CT-14 y CT-15; tres primeras
referencias de BUSQUEDA), en el código y en la prosa.

Mismo procedimiento que `r01_03_mutantes.py` (importado: copia fuera del repositorio, un cambio, `goldens_ct.py --update
--motivo` y `tests/test_fase3_goldens.py`), con `-x` en pytest. Desde la raíz, con el Python del .venv:

    .venv/bin/python .docs/tickets/T-143/revisores/r04_02_mutantes.py DESTINO [ID ...]

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
    # ---- en el código: lo que la frase dice del V6
    ("E01", ORQ, 'if self.v6 and not v6.op(self, "dictamen_g3_llm"):   # T-101', 'if False:   # T-101', "?",
     "CT-14: el V6 pide el dictamen a AG-18 aunque `v6.dictamen_g3_llm` esté desactivado"),
    ("E02", ORQ, 'not (self.v6 and not v6.op(self, "curacion_llm"))', 'not self.v6', "?",
     "CT-11: el V6 no pide la curación ni con `v6.curacion_llm`"),
    ("E03", ORQ, 'if an["nivel"] in ("N2", "N3") and', 'if an["nivel"] in ("N1", "N2", "N3") and', "?",
     "CT-11: la curación también en N1"),
    ("E04", ORQ, 'for ref in datos.get("referencias", [])[:3]:', 'for ref in datos.get("referencias", [])[:4]:', "muere",
     "BUSQUEDA: cuatro referencias en vez de tres"),
    ("E05", ORQ, 'integ = v6.integracion_determinista(self, seleccion, analisis, as_of)',
     'integ = self._integrar(seleccion, analisis, gc0, nivel, as_of, run_id, presupuesto)', "muere",
     "CT-05: el V6 por defecto emite la orden INTEGRACION"),
    # ---- en el Anexo B (texto de la r04)
    ("F01", DOC0, " Los campos de integración de `SINTESIS` son la integración del V6.", "", "?",
     "CT-15: sin la frase de la integración del V6"),
    ("F02", DOC0, " (con `v6.sintetizador`, el valor por defecto; si no, responde el Redactor con `REDACCION`)", "", "?",
     "CT-15: sin la condición del Sintetizador"),
    ("F03", DOC0, "apto con advertencias si no hay bloqueos y bloqueado si los hay", "apto con advertencias siempre", "muere",
     "CT-14: otra regla del dictamen en la prosa"),
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
