"""Ejecuta las 17 mutaciones de T-184 r02 en una copia temporal."""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

raiz = Path(__file__).resolve().parents[3]
ej = Path("bloque_a/11_Ejecutor")
pruebas = ["tests/test_t184_altas.py"]
A = "bloque_a/altas_referencias.py"
mutaciones = [
    ('N1 umbral de A un punto mayor', 'bloque_a/referencias.py', 'if q >= parametro(cfg, f"referencias.niveles_q.{nivel}"):', 'if q >= parametro(cfg, f"referencias.niveles_q.{nivel}") + (nivel == "A"):'),
    ('N2 umbral de B un punto mayor', 'bloque_a/referencias.py', 'if q >= parametro(cfg, f"referencias.niveles_q.{nivel}"):', 'if q >= parametro(cfg, f"referencias.niveles_q.{nivel}") + (nivel == "B"):'),
    ('N3 umbral de C un punto mayor', 'bloque_a/referencias.py', 'if q >= parametro(cfg, f"referencias.niveles_q.{nivel}"):', 'if q >= parametro(cfg, f"referencias.niveles_q.{nivel}") + (nivel == "C"):'),
    ("N4 admite identificadores repetidos", A, 'or rid in ids:', ':'),
    ("N5 sección ambigua admitida", A, 'if len(inicio) != 1:', 'if not inicio:'),
    ("N6 sin filtro de inyección en el título", A, ' or RE_INYECCION.search(titulo):', ':'),
    ('N7 permite otros esquemas', 'bloque_a/altas_referencias.py', 'https?://[^', '(?:https?|ftp)://[^'),
    ("N8 sin control de credenciales", A, ' or contiene_credenciales(a)', ''),
    ("N9 desempate de fichas existentes sin fecha de publicación", A, '    if fecha:\n        try:', '    if False:\n        try:'),
    ('N10 tipo de Q libre', 'bloque_a/altas_referencias.py', 'type(a["q"]) is not int or ', ' '),
    ("N11 escritura sin comparación con lo leído", A, '    publicar(ruta, original, "".join(lineas))',
     '    ruta.write_text("".join(lineas), encoding="utf-8")'),
    ("N12 desempate por año ignorado en fichas existentes", A,
     'return (-(ficha.q or 0), -date(anio, 1, 1).toordinal() if anio else 0, ficha.id)', 'return (-(ficha.q or 0), 0, ficha.id)'),
    ("N13 título multilínea admitido", A, ' or v.splitlines() != [v]', ''),
    ("N14 admite puntos fuera de rúbrica", "bloque_a/mantenimiento_fuentes.py", " or not 0 <= p <= limite", ""),
    ("N15 suma de Q sin comprobar", A, ' or a["q"] != q', ''),
    ("N16 orden por fecha invertido", A, 'clave = (-q, -fecha.toordinal(), rid)', 'clave = (-q, fecha.toordinal(), rid)'),
    ("N17 omite seguimiento de D", A, 'if nivel == "D":', 'if False:'),

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
    vivos = []
    for nombre, ruta, antes, despues in mutaciones:
        archivo = copia / ej / ruta
        original = archivo.read_text()
        assert original.count(antes) == 1, (nombre, original.count(antes))
        archivo.write_text(original.replace(antes, despues))
        r = correr(copia)
        archivo.write_text(original)
        muerto = r.returncode == 1 and " failed" in r.stdout
        if not muerto:
            vivos.append(nombre)
        print("MUERTO" if muerto else "VIVO  ", nombre, flush=True)
    if vivos:
        raise SystemExit(f"Verificar mutaciones sobrevivientes: {vivos}")
