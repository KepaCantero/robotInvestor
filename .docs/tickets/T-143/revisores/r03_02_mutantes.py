"""QA r03 de T-143 · Mutantes sobre lo que reescribió la r03 (CT-05 por tipo, ficha FINALISTA, CT-17, BUSQUEDA), en las dos
direcciones, y D23 de la r02 adaptado al texto nuevo.

Mismo procedimiento que `r01_03_mutantes.py` (importado: copia fuera del repositorio, un cambio, `goldens_ct.py --update
--motivo` y `tests/test_fase3_goldens.py`), con `-x` en pytest. Desde la raíz, con el Python del .venv:

    .venv/bin/python .docs/tickets/T-143/revisores/r03_02_mutantes.py DESTINO [ID ...]

«muere»: lo cubren las pruebas r03 según `pruebas.md`; «?»: nadie dice cubrirlo. Termina con 1 si un «muere» sobrevive o no
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

DOC0, CONTRATOS, ORQ, SEG = r01.DOC0, r01.CONTRATOS, r01.ORQ, r01.SEG

MUTANTES = [
    # ---- D23 de la r02, sobre el texto de la r03
    ("D23b", DOC0, "En SEGUIMIENTO, `memoria` lleva `senales_interes`, y `delta_gc0` va vacío.",
     "En SEGUIMIENTO, `memoria` lleva `senales`, y `delta_gc0` va vacío.", "muere", "CT-05: la prosa cambia la `memoria` de SEGUIMIENTO"),
    # ---- en el Anexo B (texto de la r03)
    ("D24", DOC0, "En SEGUIMIENTO, `memoria` lleva `senales_interes`, y `delta_gc0` va vacío.",
     "En SEGUIMIENTO, `memoria` lleva `senales_interes`, y `delta_gc0`, el resultado de GC0 de cada tipo de activo.", "muere",
     "CT-05: la prosa da otro `delta_gc0` a SEGUIMIENTO"),
    ("D25", DOC0, "En `FINALISTA`, `ambito` lleva `incluye`, `excluye` y `region`.", "En `FINALISTA`, `ambito` lleva `incluye` y `excluye`.",
     "muere", "FINALISTA: `ambito` sin `region` en la prosa"),
    ("D26", DOC0, "VALORACION | ESTRUCTURAL)", "VALORACION)", "muere", "FINALISTA: `naturaleza_inversion` sin ESTRUCTURAL en la prosa"),
    ("D27", DOC0, "`indicador_seguimiento` lleva `nombre` y `simbolo`; admite además `fuente` y `tipo`.",
     "`indicador_seguimiento` lleva `nombre` y `simbolo`.", "muere", "FINALISTA: el indicador sin sus opcionales"),
    ("D28", DOC0, "(Crítica | Material | Operativa | Menor)", "(Crítica | Material | Menor)", "muere", "CT-17: una severidad menos en la prosa"),
    ("D29", DOC0, "En el diseño V6 no hay orden INTEGRACION ni su retorno: la integración la calcula el código.", "", "muere",
     "CT-05: sin la nota del V6"),
    ("D30", DOC0, "y sin `direccion`, neutra.", "y sin `direccion`, favorable.", "?", "BUSQUEDA: otro valor por defecto de `direccion` en la prosa"),
    ("D31", DOC0, "En backtest solo cuentan las referencias registradas que se le ofrecieron.", "", "?",
     "BUSQUEDA: sin la regla de backtest"),
    # ---- en el código
    ("C25", SEG, '"memoria": {"senales_interes": enc.get("senales_interes", [])}, "delta_gc0": {},',
     '"memoria": {"senales_interes": enc.get("senales_interes", [])}, "delta_gc0": {"x": []},', "muere",
     "CT-05 SEGUIMIENTO con `delta_gc0` no vacío"),
    ("C26", CONTRATOS, '"properties": {"severidad": {"enum": ["Crítica", "Material", "Operativa", "Menor"]}}}}, "resumen": TXT},',
     '"properties": {"severidad": {"enum": ["Crítica", "Material", "Operativa", "Menor", "Alta"]}}}}, "resumen": TXT},', "muere",
     "AUDITORIA: una severidad nueva"),
    ("C27", CONTRATOS, '"invertibilidad": INVERTIBILIDAD, "ejemplos_ilustrativos"', '"invertibilidad": INVERTIBILIDAD, "pais": TXT, "ejemplos_ilustrativos"',
     "muere", "FINALISTA: un opcional nuevo"),
    ("C28", ORQ, 'ref.get("direccion", "neutra")', 'ref.get("direccion", "favorable")', "?",
     "BUSQUEDA: el ejecutor cambia el valor por defecto de `direccion`"),
    ("C29", ORQ, '"objeto": h.get("objeto", run_id)', '"objeto": h.get("objeto_auditado", run_id)', "?",
     "CT-17: el ejecutor lee de cada hallazgo otra clave sin esquema"),
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
