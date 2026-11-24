"""T-197 QA r02 (ronda de cierre) · mutantes del revisor sobre H-07 y H-08 (además de los 65 de `mutantes.py`). Aplica cada mutación en una COPIA del ejecutor,
corre las pruebas de PB-09 y restaura.

Uso: python r02_02_mutantes_cierre.py <copia de bloque_a/11_Ejecutor> [R1 R2 …]
(la copia, p. ej. de `git archive HEAD bloque_a`, para no tocar el árbol de trabajo mientras corren otras pruebas)."""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
HT05, PLAN, ORQ, CLI = ("bloque_a/herramientas/ht05_planificador.py", "bloque_a/planificacion_c1.py", "bloque_a/orquestacion.py",
                        "bloque_a/cli.py")
PRUEBAS = ["tests/test_t197_periodicidad.py",
           "tests/test_t87_contratos.py::test_ct04_conserva_frecuencia_y_aplica_desde_fecha_efecto"]
M = [
 ("C1 hora de arranque leída de otro campo de /proc/<pid>/stat (el 23, vsize)", PLAN,
  "int(campos[19]) if len(campos) > 19 and campos[19].isdigit()", "int(campos[20]) if len(campos) > 20 and campos[20].isdigit()"),
 ("C2 sin poder saberlo se cierra como huérfano", PLAN,
  "    if None in ahora.values() or None in guardada.values():\n        return None", "    if None in ahora.values() or None in guardada.values():\n        return False"),
 ("C3 sin poder saberlo cuenta como vivo", PLAN,
  "    if None in ahora.values() or None in guardada.values():\n        return None", "    if None in ahora.values() or None in guardada.values():\n        return True"),
 ("C4 el pid propio no se trata aparte", PLAN, "    if pid == os.getpid():\n", "    if False:\n"),
]
SOLO = set(sys.argv[2:])
if SOLO:
    M = [m for m in M if m[0].split()[0] in SOLO]
vivos = []
for nombre, f, a, b in M:
    p = EJ / f
    orig = p.read_text(encoding="utf-8")
    assert orig.count(a) == 1, (nombre, orig.count(a))
    p.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS],
                           cwd=EJ, capture_output=True, text=True, check=False)
    finally:
        p.write_text(orig, encoding="utf-8")
    muerto = r.returncode != 0
    print(f"{nombre}: {'MUERTO' if muerto else 'VIVO'}", flush=True)
    if not muerto:
        vivos.append(nombre)
print(f"{len(M) - len(vivos)} muertos de {len(M)}; vivos: {vivos}")
sys.exit(1 if vivos else 0)
