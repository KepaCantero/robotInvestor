"""Mutantes propios de T-200: aplica cada mutación a `bloque_a/contratos.py`, corre tests/test_t200.py y restaura.
Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-200/mutantes.py ."""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
CON = "bloque_a/contratos.py"
CIERRE = "        except BaseException:\n            db.close()   # cerrar sin commit deshace la transacción\n            raise\n"
PRAGMA = "if \"error\" not in {fila[1] for fila in db.execute(\"PRAGMA table_info(acuses)\")}:\n"
CREAR = "db.execute(\"CREATE TABLE IF NOT EXISTS acuses (id TEXT PRIMARY KEY, huella TEXT NOT NULL, respuesta TEXT)\")\n"
ALTER = "db.execute(\"ALTER TABLE acuses ADD COLUMN error TEXT\")\n"
M = [
 ("M1 sin transacción (el código de develop)", CON, "                db.execute(\"BEGIN IMMEDIATE\")\n", ""),
 ("M2 transacción diferida", CON, "db.execute(\"BEGIN IMMEDIATE\")", "db.execute(\"BEGIN DEFERRED\")"),
 ("M3 sin commit", CON, "                db.commit()\n        except BaseException:", "        except BaseException:"),
 ("M4 sin cerrar la conexión al fallar", CON, CIERRE, "        except BaseException:\n            raise\n"),
 ("M5 se traga el OperationalError", CON, CIERRE, "        except sqlite3.OperationalError:\n            pass\n"),
 ("M6 nunca migra", CON, "        try:\n            if \"error\" not in", "        try:\n            if False and \"error\" not in"),
 # r02 (H-01): siempre por el camino lento, con el cerrojo de escritura en cada apertura (el código de la r01)
 ("M7 siempre toma el cerrojo de escritura", CON, "        try:\n            if \"error\" not in", "        try:\n            if True or \"error\" not in"),
 ("M8 arreglo con captura genérica del ALTER", CON, "                    " + ALTER,
  "                    try:\n                        " + ALTER + "                    except sqlite3.OperationalError:\n"
  "                        pass\n"),
 # r02: M9 adaptado a la doble comprobación: la comprobación interior se hace antes de tomar el cerrojo
 ("M9 la comprobación interior fuera de la transacción", CON,
  "                db.execute(\"BEGIN IMMEDIATE\")\n                " + CREAR + "                " + PRAGMA,
  "                " + CREAR + "                falta = " + PRAGMA[3:-2] + "\n                db.execute(\"BEGIN IMMEDIATE\")\n"
  "                if falta:\n"),
 ("M10 sin la comprobación interior (r02)", CON, "                " + PRAGMA + "                    " + ALTER,
  "                if True:\n                    " + ALTER),
 # r02: Q3 de la QA (revisores/r06_mutantes_qa.py) con la sangría de la doble comprobación
 ("M11 commit antes del ALTER (Q3 de la QA)", CON,
  "                " + PRAGMA + "                    " + ALTER + "                db.commit()\n",
  "                falta = " + PRAGMA[3:-2] + "\n                db.commit()\n                if falta:\n                    " + ALTER),
]
vivos = []
for nombre, f, a, b in M:
    p = EJ / f
    orig = p.read_text(encoding="utf-8")
    assert orig.count(a) == 1, (nombre, orig.count(a))
    p.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t200.py"],
                           cwd=EJ, capture_output=True, text=True, check=False)
    finally:
        p.write_text(orig, encoding="utf-8")
    muerto = r.returncode != 0
    print(f"{nombre}: {'MUERTO' if muerto else 'VIVO'}", flush=True)
    if not muerto:
        vivos.append(nombre)
print("vivos:", vivos)
