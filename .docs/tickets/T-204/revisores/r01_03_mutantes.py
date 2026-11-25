"""QA r01 de T-204: mutantes propios del revisor. Aplica cada mutación, corre `.docs/scripts/pruebas_gate_bloques.py`
(que ejecuta también `prueba_refs_vivas.py`) y, aparte, `tools/refs_vivas.py` sobre el repositorio real (lo que haría el
gate `refs-vivas`); restaura siempre. Uso (desde la raíz): .venv/bin/python .docs/tickets/T-204/revisores/r01_03_mutantes.py"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
GATE, CUO, REFS = "tools/check_all.sh", "tools/cuotas.txt", "tools/refs_vivas.py"
M = [
    ("Q1 la marca vale como prefijo (T-20)", REFS, "RETIRADOS[retirado] not in linea", '"T-20" not in linea'),
    ("Q2 mypy solo del primer paquete", GATE, 'for i in "${!PAQUETES[@]}"; do', "for i in 0; do"),
    ("Q3 ruff solo sobre A", GATE, '--output-format=concise "${EJECUTORES[@]}"', '--output-format=concise "${EJECUTORES[0]}"'),
    ("Q4 la cuota de ruff sigue contando el Forex", CUO, "ruff=1604", "ruff=2806"),
    ("Q5 pytest de A con el ejecutor de B", GATE, '"${EJECUTORES[0]}" "$(cuota pytest_bloque_a)"', '"${EJECUTORES[1]}" "$(cuota pytest_bloque_a)"'),
    ("Q6 yaml vuelve a leer el Forex", GATE, "for f in ['bloque_a/11_Ejecutor/config/por_defecto.yaml',",
     "for f in ['bloque_a/11_Ejecutor/config/por_defecto.yaml','bloque_a_forex/11_Ejecutor/config/por_defecto.yaml',"),
    ("Q7 la línea empieza en la cita (marca antes de la cita no vale)", REFS,
     'linea = texto[texto.rfind("\\n", 0, m.start()) + 1:fin if fin != -1 else len(texto)]',
     "linea = texto[m.start():fin if fin != -1 else len(texto)]"),
    ("Q8 .docs/knowledge cuenta como registro", REFS, '".docs/diseno/")', '".docs/diseno/", ".docs/knowledge/")'),
    ("Q9 el bloque retirado vuelve a ser raíz válida", REFS, 'RAICES_VALIDAS = ("bloque_a/", "bloque_b/",',
     'RAICES_VALIDAS = ("bloque_a/", "bloque_a_forex/", "bloque_b/",'),
    ("Q10 sin el aviso del bloque retirado (solo se cuenta)", REFS,
     '                    rotas.append(f"{rel} cita el bloque retirado', '                    pass  # rotas.append(f"{rel} cita el bloque retirado'),
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
        g = subprocess.run([sys.executable, "-I", REFS], cwd=RAIZ, capture_output=True, text=True, check=False)
    finally:
        p.write_text(orig, encoding="utf-8")
    pruebas, gate = r.returncode != 0, g.returncode != 0
    estado = "MUERTO (pruebas)" if pruebas else ("MUERTO (solo gate refs-vivas)" if gate else "VIVO")
    print(f"{nombre}: {estado}", flush=True)
    if estado == "VIVO":
        vivos.append(nombre)
print(f"{len(M) - len(vivos)} de {len(M)} muertos" + (f"; vivos: {', '.join(vivos)}" if vivos else ""))
sys.exit(1 if vivos else 0)
