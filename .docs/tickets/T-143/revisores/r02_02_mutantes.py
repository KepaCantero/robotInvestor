"""QA r02 de T-143 · Mutantes de la r02: los de la r01 que dejaron de aplicar, adaptados al texto nuevo, y otros nuevos en las
dos direcciones (el código cambia y el Anexo B no; el Anexo B cambia y el código no).

Usa el mismo procedimiento que `r01_03_mutantes.py` (copia fuera del repositorio, un cambio de texto, re-congelado con
`goldens_ct.py --update --motivo` y `tests/test_fase3_goldens.py`), importado de ese script para no duplicarlo; solo cambia la
lista de mutantes y pasa `-x` a pytest (un mutante muere con el primer fallo). Desde la raíz, con el Python del .venv:

    .venv/bin/python .docs/tickets/T-143/revisores/r02_02_mutantes.py DESTINO [ID ...]

`esperado` "muere": una diferencia que las pruebas de T-143 (r01 y r02) dicen cubrir. "?": una afirmación del Anexo B que
ninguna prueba dice medir (se anota si sobrevive; no hace fallar el script). Termina con 1 si algún «muere» sobrevive o no
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

DOC0, CONTRATOS, ORQ, SEG, MOTOR = r01.DOC0, r01.CONTRATOS, r01.ORQ, r01.SEG, r01.MOTOR

MUTANTES = [
    # ---- D03, D06 y D09 de la r01, sobre el texto de la r02
    ("D03b", DOC0, "Son opcionales `nivel_forzado`, `fecha_objetivo` y `referencia_previa`, y dentro de `alcance` todo es opcional "
     "(sin `clases`, el ciclo usa los tipos activos). ", "", "muere",
     "el Anexo B deja de decir que tres campos de CT-01 son opcionales (pasan a ser obligatorios)"),
    ("D06b", DOC0, "`fuerza` (fuerte | moderada | debil), `argumento` y `que_la_resolveria`.",
     "`fuerza` (fuerte | moderada | debil), `argumento`, `evidencia` y `que_la_resolveria`.", "muere",
     "el Anexo B vuelve a poner `evidencia` en cada objeción de CT-13"),
    ("D09b", DOC0, "`dictamen` (APTO_CON_ADVERTENCIAS | BLOQUEADO)", "`dictamen` (APTO | APTO_CON_ADVERTENCIAS | BLOQUEADO)", "muere",
     "el Anexo B admite APTO en el dictamen del Orquestador"),
    # ---- nuevos, en el código
    ("C11", CONTRATOS, '"required": ["regimen_macro", "factores_dominantes", "lectura_conjunto", "preguntas_sugeridas", "limitaciones"],',
     '"required": ["regimen_macro", "factores_dominantes", "lectura_conjunto", "preguntas_sugeridas", "limitaciones", "cambios_vs_anterior"],',
     "muere", "INTEGRACION (CT-05, nuevo en la r02) exige `cambios_vs_anterior`"),
    ("C14", CONTRATOS, '"glosario": {"type": "array", "maxItems": 5, "items": {"type": "object", "required": ["termino", "definicion"]}},\n'
     '                       "frase_historial": TXT},',
     '"glosario": {"type": "array", "maxItems": 5, "items": {"type": "object", "required": ["termino", "definicion", "ejemplo"]}},\n'
     '                       "frase_historial": TXT},', "muere", "REDACCION (CT-15): cada término del glosario exige `ejemplo`"),
    ("C15", ORQ, '"configuracion", "resultado_comunicado", "aprobar_certificados")):', '"configuracion", "resultado_comunicado")):',
     "muere", "CT-04: un CT-04 con solo `aprobar_certificados` vuelve a rechazarse"),
    ("C16", ORQ, '"respuesta_provisional": d["respuesta"], "run_id": None}', '"respuesta_provisional": d["respuesta"], "run_id": None, "estado_run": None}',
     "muere", "CT-03: `escalado` lleva siempre `estado_run`"),
    ("C17", MOTOR, 'fecha_corte = peticion.get("fecha_corte") or (str(self.proveedor.as_of.date()) if self.proveedor.as_of is not None else None)',
     'fecha_corte = peticion["fecha_corte"]', "muere", "CT-09: el Motor exige `fecha_corte`"),
    ("C20", CONTRATOS, '{"referencias": {"type": "array", "items": {"type": "object", "required": ["ref_id"]}},',
     '{"referencias": {"type": "array", "items": {"type": "object", "required": ["ref_id", "afirmacion"]}},', "muere",
     "BUSQUEDA: cada referencia exige `afirmacion`"),
    ("C21", ORQ, 'fase = "CRIBADO_E_INVESTIGACION" if nivel in ("N2", "N3") else "REVISION_VIGENTES"',
     'fase = "CRIBADO_E_INVESTIGACION" if nivel in ("N3",) else "REVISION_VIGENTES"', "muere", "CT-06: N2 emite REVISION_VIGENTES"),
    ("C24", CONTRATOS, '"escenario_asociado": {"enum": ["BASE", "FAVORABLE", "ADVERSO"]},',
     '"escenario_asociado": {"enum": ["BASE", "FAVORABLE", "ADVERSO", "EXTREMO"]},', "muere", "PROSPECTIVA: un escenario asociado nuevo"),
    ("C12", CONTRATOS, '"type": "object", "required": ["hallazgos", "resumen"],', '"type": "object", "required": ["hallazgos", "resumen", "conclusion"],',
     "?", "AUDITORIA (CT-17) exige un campo más (el Anexo B no describe la respuesta de CT-17)"),
    ("C13", CONTRATOS, '"FACTOR", "ESTILO", "ESTRATEGIA"]   # 2.4 V5.0', '"FACTOR", "ESTILO", "ESTRATEGIA", "PAIS"]   # 2.4 V5.0', "?",
     "FINALISTA: un `tipo_opcion` nuevo (la frase de `finalistas` no da sus valores)"),
    ("C18", SEG, '"memoria": {"senales_interes": enc.get("senales_interes", [])}', '"memoria": {"senales": enc.get("senales_interes", [])}', "?",
     "CT-05 SEGUIMIENTO: `memoria` con otra clave (el Anexo B da otra `memoria`)"),
    ("C19", ORQ, '"memoria": {"run_anterior": anterior[-1]["id"] if anterior else None,', '"memoria": {"run_previo": anterior[-1]["id"] if anterior else None,',
     "?", "CT-05 INTEGRACION: `memoria` con otra clave"),
    # ---- nuevos, en el Anexo B V5.2 (texto de la r02)
    ("D11", DOC0, "`limitaciones`; admite además `cambios_vs_anterior`.", "`limitaciones`.", "muere",
     "CT-05: el Anexo B deja de nombrar `cambios_vs_anterior` de INTEGRACION"),
    ("D12", DOC0, "`lectura_conjunto`, `preguntas_sugeridas` y `limitaciones`. En `REDACCION`", "`lectura_conjunto` y `preguntas_sugeridas`. En `REDACCION`",
     "muere", "CT-15: SINTESIS sin `limitaciones` en la prosa"),
    ("D13", DOC0, "un CT-04 sin ninguno de los cinco se rechaza", "un CT-04 sin ninguno de los cinco se registra", "muere",
     "CT-04: el Anexo B dice que un CT-04 vacío se admite"),
    ("D14", DOC0, "y `estado_run` solo si se ejecutó el análisis; si no se ejecutó (`consulta --sin-escalado`), `run_id` es nulo.",
     "y `estado_run`.", "muere", "CT-03: el Anexo B vuelve a exigir `estado_run`"),
    ("D15", DOC0, "la exige la mensajería, y si una petición llega al Motor sin ella", "obligatoria siempre; si una petición llega al Motor sin ella",
     "muere", "CT-09: el Anexo B vuelve a «obligatoria siempre»"),
    ("D16", DOC0, "`dimensiones`, `premortem`,", "`dimensiones`, `puntuaciones`, `premortem`,", "muere",
     "CT-06: la ficha vuelve a llevar `puntuaciones`"),
    ("D18", DOC0, "El ciclo emite CRIBADO_E_INVESTIGACION en los niveles N2 y N3", "El ciclo emite CRIBADO_E_INVESTIGACION en el nivel N3",
     "muere", "CT-06: el Anexo B cambia cuándo se emite CRIBADO_E_INVESTIGACION"),
    ("D20", DOC0, "Los tres entregables y sus rutas los escribe el ejecutor, que mide su legibilidad al validarlos (G3).",
     "El Redactor devuelve además las rutas de los tres entregables y sus métricas de legibilidad.", "?",
     "CT-15: la prosa vuelve a decir que el Redactor devuelve rutas y legibilidad (lo que corrigió H-02)"),
    ("D21", DOC0, "No hay dictamen APTO: si el validador HT-09 da «apto», la entrega sigue sin dictamen del Orquestador (6.1).",
     "Si el validador HT-09 da «apto», el Orquestador dictamina APTO.", "?", "CT-14: la prosa dice que hay dictamen APTO"),
    ("D23", DOC0, "`memoria` (OPP- vigentes, TND- activas, LEC- aplicables, certificados de horizonte)", "`memoria` (OPP- vigentes)", "?",
     "CT-05: la prosa cambia lo que lleva `memoria`"),
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
