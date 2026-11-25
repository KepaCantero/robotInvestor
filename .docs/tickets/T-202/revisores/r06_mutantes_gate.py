"""T-202 · QA r02 · mutantes del revisor sobre la comprobación del entorno en `tools/check_all.sh` (H-03).

Cada mutante cambia una línea del bloque de mypy, ejecuta `.docs/scripts/pruebas_gate_entorno.py` y restaura.
Uso (desde la raíz de la copia): .venv/bin/python .docs/tickets/T-202/revisores/r06_mutantes_gate.py [RG01 …]
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path.cwd()
GATE = RAIZ / "tools" / "check_all.sh"
PRUEBA = ".docs/scripts/pruebas_gate_entorno.py"
FALLA = ("((TOTAL++)); ((FAILED++)); echo -e \"${RED}✗ mypy $paq: el .venv no coincide con tools/requisitos_entorno.txt "
         "(stubs incluidos): ejecuta .docs/scripts/preparar_entorno.sh${NC}\"; continue; fi")
M = [
    ("RG01 sin «continue»: mypy se ejecuta aunque el entorno no coincida", FALLA, FALLA.replace("; continue; fi", "; fi")),
    ("RG02 no suma el fallo (FAILED)", FALLA, FALLA.replace(" ((FAILED++));", "")),
    ("RG03 no suma el gate (TOTAL)", FALLA, FALLA.replace("((TOTAL++)); ", "")),
    ("RG04 no muestra la salida de --comprobar", '    [ -z "$entorno_mypy" ] || echo "$entorno_mypy"\n', "\n"),
    ("RG05 --comprobar sin 2>&1 (lo que dice va a stderr y se pierde del motivo)",
     '"$(.docs/scripts/preparar_entorno.sh --comprobar 2>&1)"', '"$(.docs/scripts/preparar_entorno.sh --comprobar)"'),
    ("RG06 la comprobación solo avisa (falla → sigue con mypy)",
     'if [ -n "$entorno_mypy" ]; then', 'if [ -n "$entorno_mypy" ] && false; then'),
    ("RG07 sin el texto de reserva cuando --comprobar falla sin decir nada",
     '"${salida_entorno:-preparar_entorno.sh --comprobar falló}"', '"${salida_entorno}"'),
]


def main() -> int:
    vivos = 0
    for nombre, a, b in M:
        if sys.argv[1:] and nombre.split()[0] not in sys.argv[1:]:
            continue
        orig = GATE.read_text(encoding="utf-8")
        assert orig.count(a) == 1, (nombre, orig.count(a))
        GATE.write_text(orig.replace(a, b), encoding="utf-8")
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", PRUEBA], cwd=RAIZ,
                               capture_output=True, text=True, check=False)
        finally:
            GATE.write_text(orig, encoding="utf-8")
        fallo = next((ln.strip() for ln in r.stdout.splitlines() if ln.startswith(("FAILED ", "ERROR "))), "")
        ok = r.returncode == 0
        vivos += ok
        print(f"{nombre}: {'VIVO' if ok else 'MUERTO'} {fallo[:150]}", flush=True)
    return 1 if vivos else 0


if __name__ == "__main__":
    sys.exit(main())
