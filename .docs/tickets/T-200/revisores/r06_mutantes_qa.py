"""Mutantes propios de la QA r01 de T-200 (además de ../mutantes.py). Aplica cada mutación a bloque_a/contratos.py, corre
tests/test_t200.py y restaura. Uso (desde bloque_a/11_Ejecutor): python ../../.docs/tickets/T-200/revisores/r06_mutantes_qa.py ."""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
CON = "bloque_a/contratos.py"
CON_ = 'db = sqlite3.connect(self.almacen.carpeta / "acuses.sqlite3")'
M = [
 ("Q1 timeout 0 en la conexión", CON_, CON_[:-1] + ", timeout=0)"),
 ("Q2 rollback en vez de cerrar", "            db.close()   # cerrar sin commit deshace la transacción\n",
  "            db.rollback()\n"),
  # r02: la sangría de la doble comprobación (camino lento dentro del primer if)
 ("Q3 commit antes del ALTER (ALTER fuera de la transacción)",
  ('                if "error" not in {fila[1] for fila in db.execute("PRAGMA table_info(acuses)")}:\n'
   '                    db.execute("ALTER TABLE acuses ADD COLUMN error TEXT")\n                db.commit()\n'),
  ('                falta = "error" not in {fila[1] for fila in db.execute("PRAGMA table_info(acuses)")}\n'
   '                db.commit()\n                if falta:\n                    db.execute("ALTER TABLE acuses ADD COLUMN error TEXT")\n')),
 ("Q4 se devuelve la conexión cerrada al fallar sin relanzar", "            db.close()   # cerrar sin commit deshace la transacción\n            raise\n",
  "            db.close()   # cerrar sin commit deshace la transacción\n            return db\n"),
 # r02: mutantes del camino rápido (lectura sin cerrojo)
 ("Q7 camino lento sin CREATE TABLE",
  '                db.execute("CREATE TABLE IF NOT EXISTS acuses (id TEXT PRIMARY KEY, huella TEXT NOT NULL, respuesta TEXT)")\n', ""),
 ("Q8 la lectura de fuera mira otra columna", '        try:\n            if "error" not in', '        try:\n            if "huella" not in'),
 ("Q9 el camino rápido deja una transacción abierta", '        try:\n            if "error" not in',
  '        try:\n            db.execute("BEGIN")\n            if "error" not in'),
 ("Q5 [equivalente] BEGIN EXCLUSIVE", 'db.execute("BEGIN IMMEDIATE")', 'db.execute("BEGIN EXCLUSIVE")'),
 ("Q6 [equivalente] except Exception", "        except BaseException:\n            db.close()", "        except Exception:\n            db.close()"),
]
vivos = []
for nombre, a, b in M:
    p = EJ / CON
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
    if not muerto and "[equivalente]" not in nombre:
        vivos.append(nombre)
print("vivos no equivalentes:", vivos)
