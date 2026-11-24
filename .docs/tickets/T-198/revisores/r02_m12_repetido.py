"""QA r02 de T-198: ¿mata la suite al mutante M12 (atender_ct19 sin cerrojo) siempre, o depende de la carga de la máquina?
Aplica M12 en una COPIA de 11_Ejecutor y corre N veces la prueba de concurrencia de CA-3. Uso: python r02_m12_repetido.py <copia> [N]"""
import subprocess
import sys
from pathlib import Path

EJ, N = Path(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 5
p = EJ / "bloque_a/fiabilidad_f9.py"
orig = p.read_text(encoding="utf-8")
a, b = "    with almacen._transaccion():\n        f6 = _fue_de_f6", "    if True:\n        f6 = _fue_de_f6"
assert orig.count(a) == 1
p.write_text(orig.replace(a, b), encoding="utf-8")
vivo = 0
try:
    for i in range(N):
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                            "tests/test_t198_buscador_ct19.py::test_ca3_dos_instancias_a_la_vez_dejan_una_entrada_por_fuente"],
                           cwd=EJ, capture_output=True, text=True, check=False)
        print(f"pasada {i + 1}: {'MUERTO' if r.returncode else 'VIVO'}", flush=True)
        vivo += r.returncode == 0
finally:
    p.write_text(orig, encoding="utf-8")
print(f"M12 vivo en {vivo} de {N} pasadas")
sys.exit(1 if vivo else 0)
