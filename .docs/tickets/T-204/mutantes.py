"""Mutantes propios de T-204: aplica cada mutación al gate, a sus cuotas, a los scripts que enumeran los bloques o a
`refs_vivas.py`, corre `.docs/scripts/pruebas_gate_bloques.py` (que también ejecuta `prueba_refs_vivas.py`) y restaura.
Uso (desde la raíz del repositorio): .venv/bin/python .docs/tickets/T-204/mutantes.py"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
GATE, CUO, REFS = "tools/check_all.sh", "tools/cuotas.txt", "tools/refs_vivas.py"
PREP, QA, CORPUS = ".docs/scripts/preparar_entorno.sh", ".docs/scripts/qa_rama.sh", "tools/corpus_integridad.py"
LIMPIAR = ".docs/tickets/T-204/limpiar_docs.py"
M = [
 # El gate y sus cuotas
 ("M1 vuelve el ejecutor del Forex", GATE, "EJECUTORES=(bloque_a/11_Ejecutor bloque_b/11_Ejecutor)",
  "EJECUTORES=(bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor)"),
 ("M2 vuelve el paquete del Forex", GATE, "PAQUETES=(bloque_a bloque_b)", "PAQUETES=(bloque_a bloque_a_forex bloque_b)"),
 ("M3 bucle de mypy con índices fijos", GATE, 'for i in "${!PAQUETES[@]}"; do', "for i in 0 1 2; do"),
 ("M4 pytest de B con el ejecutor de A", GATE, '"${EJECUTORES[1]}" "$(cuota pytest_bloque_b)"', '"${EJECUTORES[0]}" "$(cuota pytest_bloque_b)"'),
 ("M5 pytest de B con la base de A", GATE, '"${EJECUTORES[1]}" "$(cuota pytest_bloque_b)"', '"${EJECUTORES[1]}" "$(cuota pytest_bloque_a)"'),
 ("M6 sin pytest de B", GATE, 'pytest_con_base "pytest bloque_b"        "${EJECUTORES[1]}" "$(cuota pytest_bloque_b)"\n', ""),
 ("M7 vuelve el pytest del Forex", GATE, 'pytest_con_base "pytest bloque_b"',
  'pytest_con_base "pytest bloque_a_forex"  "bloque_a_forex/11_Ejecutor" "68"\npytest_con_base "pytest bloque_b"'),
 ("M8 yaml sin la configuración de B", GATE, ",'bloque_b/11_Ejecutor/config/por_defecto.yaml']", "]"),
 ("M9 sin refs-vivas", GATE, 'run_check "refs-vivas" $PY tools/refs_vivas.py\n', ""),
 ("M10 vuelve la cuota de mypy del Forex", CUO, "mypy_bloque_b=159\n", "mypy_bloque_a_forex=174\nmypy_bloque_b=159\n"),
 ("M11 vuelve la línea base del Forex", CUO, "pytest_bloque_b=174\n", "pytest_bloque_b=174\npytest_bloque_a_forex=68\n"),
 ("M12 sin la línea base de B", CUO, "pytest_bloque_b=174\n", ""),
 # Scripts que enumeran los bloques
 ("M13 preparar_entorno instala el Forex", PREP, "-e bloque_a/11_Ejecutor -e bloque_b/11_Ejecutor",
  "-e bloque_a/11_Ejecutor -e bloque_a_forex/11_Ejecutor -e bloque_b/11_Ejecutor"),
 ("M14 preparar_entorno sin B", PREP, "-e bloque_a/11_Ejecutor -e bloque_b/11_Ejecutor", "-e bloque_a/11_Ejecutor"),
 ("M15 qa_rama prueba el Forex", QA, "for ej in bloque_a bloque_b; do", "for ej in bloque_a bloque_a_forex bloque_b; do"),
 ("M16 el corpus vuelve a incluir el Forex", CORPUS, '("bloque_a", "bloque_b")', '("bloque_a", "bloque_a_forex", "bloque_b")'),
 # refs-vivas: el bloque retirado
 ("M17 sin bloques retirados", REFS, 'RETIRADOS = {"bloque_a_forex": "T-204"}', "RETIRADOS: dict = {}"),
 ("M18 la marca no se acepta", REFS, " and not marcada(linea, RETIRADOS[retirado]):", ":"),
 ("M19 la marca vale en cualquier línea", REFS, "not marcada(linea, RETIRADOS[retirado])", "not marcada(texto, RETIRADOS[retirado])"),
 ("M20 los registros no se eximen", REFS, "if not rel.startswith(REGISTROS) and", "if"),
 ("M21 docs/ cuenta como registro", REFS, 'REGISTROS = (".docs/tickets/"', 'REGISTROS = ("docs/", ".docs/tickets/"'),
 ("M22 .docs entero cuenta como registro", REFS, 'REGISTROS = (".docs/tickets/", ".docs/diario/", ".docs/memoria/", ".docs/diseno/")',
  'REGISTROS = (".docs/",)'),
 ("M23 el diseño no es registro", REFS, ', ".docs/diseno/")', ")"),
 ("M24 solo la cita entera", REFS, "    for r in [cita.strip()] + partes:", "    for r in [cita.strip()]:"),
 ("M25 sin --opcion=ruta", REFS, '            r = r.split("=", 1)[-1]\n', '            pass\n'),
 ("M26 sin quitar ./", REFS, '        primero = r.removeprefix("./").split("/", 1)[0]', '        primero = r.split("/", 1)[0]'),
 ("M27 el retirado se mira después de las abreviaturas", REFS,
  "            retirado = bloque_retirado(bruta)\n", "            retirado = None if \"…\" in bruta else bloque_retirado(bruta)\n"),
 ("M28 una cita con el bloque retirado no comprueba sus otras rutas", REFS,
  "            # Las demás rutas de la cita se comprueban como siempre; las del bloque retirado ya no son de una raíz válida.\n",
  "                continue\n"),
 ("M29 la línea acaba antes de la cita", REFS, "linea = texto[texto.rfind(\"\\n\", 0, m.start()) + 1:fin if fin != -1 else len(texto)]",
  "linea = texto[texto.rfind(\"\\n\", 0, m.start()) + 1:m.start()]"),
 # r02 (QA r01, H-06)
 ("M30 la marca como subcadena (T-2040 vale)", REFS, 'return re.search(rf"(?<![\\w-]){re.escape(marca)}(?!\\d)", linea) is not None',
  "return marca in linea"),
 ("M31 «=» en todas las palabras", REFS, '        if r.startswith("-") or RE_ASIGNACION.match(r):', '        if True:'),
 # r03 (QA r02, H-11 y H-12)
 ("M37 limpiar sin la evidencia de la r03", LIMPIAR, '|\\b\\d+/\\d+\\b|\\b\\d+ de \\d+ en verde\\b|\\bpasadas\\b|\\btres (?:suites|ejecutores|bloques)\\b"\n', '"\n'),
 ("M38 sin partir NOMBRE=ruta", REFS, '        if r.startswith("-") or RE_ASIGNACION.match(r):', '        if r.startswith("-"):'),
 # cierre 2 (H-14): mayúsculas y recuento «A-Forex N, B N» como evidencia
 ("M40 limpiar: mypy y pytest solo en minúscula", LIMPIAR, "(?i:\\bmypy\\b|\\bpytest\\b|\\bruff\\b)", "\\bmypy\\b|\\bpytest\\b|\\bruff\\b"),
 ("M41 limpiar: sin el recuento A-Forex N, B N", LIMPIAR, '                          r"|\\b(?:A-Forex|FX) \\d+, B \\d+")', '                          r"")'),
 # cierre de la QA r03 (H-13): la fila T-54 sin la anotación de la enmienda 6
 ("M39 T-54 sin anotar", "sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md",
  "; desde la V0.7, enmienda 6, D-48, D-20 solo nombra B Forex):", "):"),
 # r02 (QA r01, H-03): limpiar_docs.py
 ("M32 limpiar reescribe líneas con T-204", LIMPIAR, " or RE_MARCA.search(linea) or", " or"),
 ("M33 limpiar reescribe la evidencia de gates", LIMPIAR, " or RE_EVIDENCIA.search(linea):", ":"),
 ("M34 limpiar entra en los encargos", LIMPIAR, " and not RE_ENCARGO.fullmatch(p.relative_to(RAIZ).as_posix()))", ")"),
 ("M35 limpiar recorta citas «…»", LIMPIAR, '        if re.findall(r"«[^»]*»", nueva) != re.findall(r"«[^»]*»", linea):', "        if False:"),
 ("M36 limpiar borra la viñeta de la historia", LIMPIAR, '    r"- A-Forex;",\n', '    r"- A-Forex;",\n    r"\\s*- \\*\\*Bloque A Forex V1\\.1\\*\\*;",\n'),
]
vivos = []
for nombre, f, a, b in M:
    p = RAIZ / f
    orig = p.read_text(encoding="utf-8")
    assert orig.count(a) == 1, (nombre, orig.count(a))
    p.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", ".docs/scripts/pruebas_gate_bloques.py"],
                           cwd=RAIZ, capture_output=True, text=True, check=False)
    finally:
        p.write_text(orig, encoding="utf-8")
    muerto = r.returncode != 0
    print(f"{nombre}: {'MUERTO' if muerto else 'VIVO'}", flush=True)
    if not muerto:
        vivos.append(nombre)
print(f"{len(M) - len(vivos)} de {len(M)} muertos" + (f"; vivos: {', '.join(vivos)}" if vivos else ""))
sys.exit(1 if vivos else 0)
