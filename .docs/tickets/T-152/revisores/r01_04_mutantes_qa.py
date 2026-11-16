"""T-152 · QA r01 · mutantes del revisor sobre la línea nueva del umbral, contra TODAS las pruebas que tocan
`motor/frontera_b.py` o IDX-CONC-001 (no solo las de T-150, T-149 y T-144).

Uso, desde la raíz:  .venv/bin/python .docs/tickets/T-152/revisores/r01_04_mutantes_qa.py <copia desechable con «t147_mut»>
La copia ha de ser completa (`git archive <commit> | tar -x`). Primero ejecuta las pruebas sin mutar (han de pasar);
después cada mutante, restaurando el fichero. Imprime MUERTO o VIVO; termina con 1 si vive alguno (V01 y V02 se esperan
vivos: el umbral más alto que la decisión del operador no lo ve ninguna prueba, H-01 de esta QA)."""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "t147_mut" in str(COPIA) and (COPIA / "bloque_b" / "11_Ejecutor").is_dir(), "copia desechable y completa"
EJ = COPIA / "bloque_a" / "11_Ejecutor"
FB = EJ / "bloque_a" / "motor" / "frontera_b.py"
PRUEBAS = ["tests/test_fase1_mon_idx.py", "tests/test_t106_r03.py", "tests/test_t113_deuda.py", "tests/test_t121_hallazgos.py",
           "tests/test_t127_hallazgos.py", "tests/test_t127_r02.py", "tests/test_t127_r03.py", "tests/test_t128_frontera.py",
           "tests/test_t128_r02.py", "tests/test_t135_motor.py", "tests/test_t144.py", "tests/test_t149.py", "tests/test_t150.py",
           "tests/test_t165_g3_met13.py"]
LINEA = "    desplaza = rel <= tol\n"
MUTANTES = [
    ("V01 umbral en q/p ≤ 2,5 % (un 25 % más alto)", "    desplaza = 2 * rel <= 1.25 * 2 * tol\n"),
    ("V02 umbral en q/p ≤ 4 % (el U2 de T-152)", "    desplaza = rel <= 2 * tol\n"),
    ("V03 umbral en q/p ≤ 10 %", "    desplaza = rel <= 5 * tol\n"),
    ("V04 umbral estricto (q/p < 2 %)", "    desplaza = rel < tol\n"),
    ("V05 umbral con la media anchura de la hipótesis truncada (q/(2p̃+q) ≤ tol, q/p̃ ≲ 2,04 %)",
     "    desplaza = rel / (1 + rel) <= tol\n"),
    ("V06 umbral un 1 % más bajo (q/p ≤ 1,98 %)", "    desplaza = rel <= 0.99 * tol\n"),
]


def pytest():
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], cwd=EJ,
                       capture_output=True, text=True, check=False)
    assert r.returncode in (0, 1), r.stdout[-1500:] + r.stderr[-1500:]
    return r.returncode, r.stdout.strip().splitlines()[-1][:70]


original = FB.read_text(encoding="utf-8")
assert original.count(LINEA) == 1
codigo, linea = pytest()
print(f"sin mutar: {linea}", flush=True)
assert codigo == 0, "la copia sin mutar no pasa: no se puede leer ningún mutante"
vivos = 0
for nombre, nueva in MUTANTES:
    FB.write_text(original.replace(LINEA, nueva), encoding="utf-8")
    try:
        codigo, linea = pytest()
    finally:
        FB.write_text(original, encoding="utf-8")
    vivos += codigo == 0
    print(f"{nombre:92} {'VIVO' if codigo == 0 else 'MUERTO':7} {linea}", flush=True)
print(f"\n{vivos} vivos")
sys.exit(1 if vivos else 0)
