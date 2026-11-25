"""QA r01 de T-184 (Claude): mutantes propios de altas_referencias.py, contra la prueba del ticket.

    .venv/bin/python .docs/tickets/T-184/revisores/r01_mutantes.py

Imprime MUERTO o VIVO por mutante; un VIVO que cambia el comportamiento es hallazgo (H-05 del qa.md).
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

raiz = Path(__file__).resolve().parents[4]
ej = Path("bloque_a/11_Ejecutor")
pruebas = ["tests/test_t184_altas.py"]
A = "bloque_a/altas_referencias.py"
mutaciones = [
    ("N1 umbral A 80 → 81", A, 'nivel = "A" if q >= 80', 'nivel = "A" if q >= 81'),
    ("N2 umbral B 65 → 66", A, 'else "B" if q >= 65', 'else "B" if q >= 66'),
    ("N3 umbral C 50 → 51", A, 'else "C" if q >= 50', 'else "C" if q >= 51'),
    ("N4 admite identificadores repetidos", A, 'or rid in ids:', ':'),
    ("N5 sección ambigua admitida", A, 'if len(inicio) != 1:', 'if not inicio:'),
    ("N6 sin filtro de inyección en el título", A, ' or RE_INYECCION.search(titulo):', ':'),
    ("N7 admite cualquier esquema de URL", A, 'enlace.scheme not in ("https", "http") or ', ''),
    ("N8 sin control de credenciales", A, ' or contiene_credenciales(a)', ''),
    ("N9 desempate de fichas existentes sin fecha de publicación", A, '    if fecha:\n        try:', '    if False:\n        try:'),
    ("N10 Q booleana o real admitida", A, 'type(q) is not int', 'not isinstance(q, (int, float))'),
    ("N11 escritura sin comparación con lo leído", A, '    publicar(ruta, original, "".join(lineas))',
     '    ruta.write_text("".join(lineas), encoding="utf-8")'),
    ("N12 desempate por año ignorado en fichas existentes", A,
     'return (-(ficha.q or 0), -date(anio, 1, 1).toordinal() if anio else 0, ficha.id)', 'return (-(ficha.q or 0), 0, ficha.id)'),
    ("N13 título multilínea admitido", A, ' or len(v.splitlines()) != 1', ''),
    ("N14 Q fuera de rango", A, ' or not 0 <= q <= 100', ''),
]


def correr(carpeta):
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *pruebas], cwd=carpeta / ej,
                          text=True, capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


with tempfile.TemporaryDirectory() as tmp:
    copia = Path(tmp)
    shutil.copytree(raiz / "bloque_a", copia / "bloque_a", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    base = correr(copia)
    if base.returncode:
        raise SystemExit(base.stdout[-3000:] + base.stderr[-3000:])
    for nombre, ruta, antes, despues in mutaciones:
        archivo = copia / ej / ruta
        original = archivo.read_text()
        assert original.count(antes) == 1, (nombre, original.count(antes))
        archivo.write_text(original.replace(antes, despues))
        r = correr(copia)
        archivo.write_text(original)
        print("MUERTO" if r.returncode else "VIVO  ", nombre, flush=True)
