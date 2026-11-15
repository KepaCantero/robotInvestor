"""QA r01 de T-122 · CA-4: los mutantes A1b, B7 y C1 de `.docs/tickets/T-113/revisores/r02_04_mutantes.py` (mismas cadenas)
frente a las pruebas NUEVAS de T-122 (`tests/test_t122_hallazgos.py`). El script de origen solo ejecuta las pruebas de T-113 y
sus vecinas, así que ahí sobreviven por construcción.
Uso: python r01_02_mutantes_a1b_b7_c1.py <raíz de una copia> <carpeta desechable>
"""
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ, DEST = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
PY = "/home/user/robotinvestor/.venv/bin/python"
E = "bloque_a/"
M = [
    ("A1b", E + "llm.py", "            hallados.append(x)\n        elif isinstance(x, (list, tuple, set, frozenset)):",
     "            hallados.append(x)\n        elif isinstance(x, (list, tuple)):"),
    ("B7", E + "herramientas/ht06_indice.py", "        except (ValueError, RecursionError):\n            fh.truncate", "        except ValueError:\n            fh.truncate"),
    ("C1", E + "orquestacion.py", '("grabación del cliente", getattr(cliente, "descartadas", 0))):', '("grabación del cliente", 0)):'),
]
vivos = []
for mid, rel, orig, mut in M:
    d = DEST / f"m_{mid}"
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(RAIZ / "bloque_a", d / "bloque_a", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    f = d / "bloque_a" / "11_Ejecutor" / rel
    t = f.read_text(encoding="utf-8")
    assert t.count(orig) == 1, f"{mid}: el original no aparece una sola vez"
    f.write_text(t.replace(orig, mut), encoding="utf-8")
    r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t122_hallazgos.py"],
                       cwd=d / "bloque_a" / "11_Ejecutor", capture_output=True, text=True)
    ultima = (r.stdout.strip().splitlines() or [""])[-1]
    fallida = next((x for x in r.stdout.splitlines() if x.startswith("FAILED")), "")
    estado = "MUERE" if r.returncode != 0 else "VIVE"
    if estado == "VIVE":
        vivos.append(mid)
    print(f"{mid} {estado} · {ultima} · {fallida[:160]}")
    shutil.rmtree(d, ignore_errors=True)
print(f"vivos: {vivos or 'ninguno'}")
