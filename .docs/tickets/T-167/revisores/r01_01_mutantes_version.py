"""T-167 QA r01: mutantes de la versión del Bloque A contra tests/test_t167_version.py.

Uso (desde bloque_a/11_Ejecutor de una COPIA del repo, nunca del árbol principal):
    python ../../.docs/tickets/T-167/revisores/r01_01_mutantes_version.py
Cada mutante cambia pyproject.toml, bloque_a/__init__.py o el título del README, pasa la prueba y restaura siempre
los originales. Un mutante «vivo» es uno con el que la prueba pasa. También comprueba que la prueba importa el
paquete de esta copia (y no el de otra instalación editable).
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path.cwd()
PY, INIT, README = RAIZ / "pyproject.toml", RAIZ / "bloque_a" / "__init__.py", RAIZ / "README.md"
assert PY.is_file() and INIT.is_file() and README.is_file(), "ejecútalo desde bloque_a/11_Ejecutor"
ORIG = {p: p.read_bytes() for p in (PY, INIT, README)}

V_PY, V_INIT, T_README = 'version = "1.2.0"', '__version__ = "1.2.0"', "# Ejecutor programático del Bloque A (V1.2)"
MUTANTES = [
    # (nombre, [(fichero, antes, después)], debe_caer)
    ("M01 pyproject vuelve a 1.1.0", [(PY, V_PY, 'version = "1.1.0"')], True),
    ("M02 __init__ vuelve a 1.1.0", [(INIT, V_INIT, '__version__ = "1.1.0"')], True),
    ("M03 los dos vuelven a 1.1.0 (coinciden entre sí)", [(PY, V_PY, 'version = "1.1.0"'), (INIT, V_INIT, '__version__ = "1.1.0"')], True),
    ("M04 README dice V1.1, código 1.2.0", [(README, T_README, "# Ejecutor programático del Bloque A (V1.1)")], True),
    ("M05 README dice V1.3, código 1.2.0", [(README, T_README, "# Ejecutor programático del Bloque A (V1.3)")], True),
    ("M06 título del README sin versión", [(README, T_README, "# Ejecutor programático del Bloque A")], True),
    ("M07 pyproject 1.2.1", [(PY, V_PY, 'version = "1.2.1"')], True),
    ("M08 __init__ '1.2' sin parche", [(INIT, V_INIT, '__version__ = "1.2"')], True),
    ("M09 __init__ con espacio final", [(INIT, V_INIT, '__version__ = "1.2.0 "')], True),
    ("M10 pyproject y __init__ a 2.0.0", [(PY, V_PY, 'version = "2.0.0"'), (INIT, V_INIT, '__version__ = "2.0.0"')], True),
    ("M11 los tres a 1.3 (coherente)", [(PY, V_PY, 'version = "1.3.0"'), (INIT, V_INIT, '__version__ = "1.3.0"'),
                                         (README, T_README, "# Ejecutor programático del Bloque A (V1.3)")], False),
]

SONDA = RAIZ / "tests" / "test_zz_sonda_qa167.py"


def corre() -> bool:
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_t167_version.py"],
                       capture_output=True, text=True)
    return r.returncode == 0


vivos = 0
try:
    SONDA.write_text("import bloque_a\nfrom pathlib import Path\n\ndef test_sonda():\n"
                     "    assert Path(bloque_a.__file__).resolve().parents[1] == Path(__file__).resolve().parents[1]\n",
                     encoding="utf-8")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(SONDA),
                        "tests/test_t167_version.py"], capture_output=True, text=True)
    print(f"original (3 pruebas, con la sonda de origen del paquete): {'pasa' if r.returncode == 0 else 'FALLA'}")
    SONDA.unlink()
    for nombre, cambios, debe_caer in MUTANTES:
        for f, a, d in cambios:
            t = f.read_text(encoding="utf-8")
            assert t.count(a) == 1, (nombre, f, a)
            f.write_text(t.replace(a, d), encoding="utf-8")
        pasa = corre()
        for p, b in ORIG.items():
            p.write_bytes(b)
        ok = (not pasa) if debe_caer else pasa
        vivos += not ok
        estado = ("cae" if not pasa else "VIVO") if debe_caer else ("pasa (esperado)" if pasa else "FALLA (no esperado)")
        print(f"{nombre}: {estado}")
finally:
    for p, b in ORIG.items():
        p.write_bytes(b)
    SONDA.unlink(missing_ok=True)
print(f"resultado: {len(MUTANTES) - vivos}/{len(MUTANTES)} como se esperaba")
sys.exit(1 if vivos else 0)
