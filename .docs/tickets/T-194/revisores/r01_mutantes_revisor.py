"""T-194 · QA r01 · mutantes propios del revisor sobre `.docs/scripts/cola_astra.py`.

Mismo mecanismo que `../mutantes.py`: cada mutante se escribe en una carpeta temporal y las pruebas de
`.docs/scripts/pruebas_cola_astra.py` (y, si se pide con --con-autor, también `pruebas_autor_generico.py`, que no
lee COLA_ASTRA_SCRIPT y por eso solo sirve con el original sustituido: no se hace) lo cargan por `COLA_ASTRA_SCRIPT`.
Uso, desde la raíz:  .venv/bin/python .docs/tickets/T-194/revisores/r01_mutantes_revisor.py
Vivo = ninguna prueba lo detecta. Termina con 1 si alguno no aplica o vive.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
ORIGINAL = RAIZ / ".docs/scripts/cola_astra.py"
PRUEBAS = RAIZ / ".docs/scripts/pruebas_cola_astra.py"

MUTANTES = [
    ("R01", "IMPLEMENTAR: un README anterior a la cola cuenta",
     '    if fecha and fecha < FECHA_COLA:', '    if f["tipo"] == "QA" and fecha and fecha < FECHA_COLA:'),
    ("R02", "tipo desconocido cuenta como hecho",
     '    return False, f"tipo desconocido «{f[\'tipo\']}»", commit', '    return True, "", commit'),
    ("R03", "el .env sin quitar las comillas",
     "valores[k] = v.strip().strip('\"').strip(\"'\")", "valores[k] = v.strip()"),
    ("R04", "la fecha de la cola también para REVISION",
     '    if f["tipo"] == "REVISION":\n        if texto', '    if f["tipo"] == "REVISION" and not (fecha and fecha < FECHA_COLA):\n        if texto'),
    ("R05", "solo el correo del git config cuenta",
     'nombre = valores["GIT_AUTOR_NOMBRE"] or git("config", "user.name")', 'nombre = valores["GIT_AUTOR_NOMBRE"] or "Astra"'),
    ("R06", "el estado del ticket IMPLEMENTAR por búsqueda en cualquier parte",
     r'm = re.search(r"^\| Estado \| ([^|]+)\|", texto, re.MULTILINE)', r'm = re.search(r"\| Estado \| ([^|]+)\|", texto)'),
    ("R07", "estado desconocido: sin el ancla final", r'EN CURSO( \d{4}-\d{2}-\d{2})?)$")', r'EN CURSO( \d{4}-\d{2}-\d{2})?)")'),
    ("R08", "el borrador en cualquier parte", 'if texto.lstrip().upper().startswith("BORRADOR"):', 'if "BORRADOR" in texto.upper():'),
    ("R09", "ERROR va al texto pero no a --json en filas rotas", "    if len(en_curso) > 1:", "    errores[:] = [e for e in errores if 'columnas' not in e] if '--json' in sys.argv else errores\n    if len(en_curso) > 1:"),
]


def main() -> int:
    fuente = ORIGINAL.read_text(encoding="utf-8")
    malos = []
    with tempfile.TemporaryDirectory() as tmp:
        for mid, desc, viejo, nuevo in MUTANTES:
            if fuente.count(viejo) != 1:
                print(f"{mid} NO APLICA ({fuente.count(viejo)}): {desc}")
                malos.append(mid)
                continue
            mut = Path(tmp) / f"{mid}.py"
            mut.write_text(fuente.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", str(PRUEBAS)],
                               env={**os.environ, "COLA_ASTRA_SCRIPT": str(mut)}, capture_output=True, text=True,
                               check=False, cwd=RAIZ)
            vivo = r.returncode == 0
            print(f"{mid} {'VIVO' if vivo else 'muerto'}: {desc}", flush=True)
            if vivo:
                malos.append(mid)
    print(f"{len(malos)} vivos o sin aplicar: {malos}" if malos else "todos muertos")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
