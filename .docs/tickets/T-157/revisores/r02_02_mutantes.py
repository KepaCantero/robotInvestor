"""QA r02 de T-157 · mutantes del revisor sobre las reglas de la r02 contra `tests/test_t157_verificador_ids.py`.

Cada mutante cambia un trozo del código fuente del verificador (se recompila en el espacio de nombres del módulo desde un
`conftest` temporal; el archivo del módulo no se toca) y se ejecuta el archivo de pruebas entero. MATADO = alguna prueba falla
por una aserción («failed»); VIVO = todo pasa; ROTO = el mutante no se aplica o la recogida falla. El nulo es el control.
Sale 1 si el nulo no queda vivo o algún mutante no se aplica; los VIVOS se informan (son hallazgos, no fallos del script).

Uso (desde bloque_a/11_Ejecutor):
    ../../.venv/bin/python ../../.docs/tickets/T-157/revisores/r02_02_mutantes.py
"""
import os
import re
import subprocess
import sys
from pathlib import Path

EJ = Path.cwd()
MOD = EJ / "bloque_a/herramientas/verificador_ids.py"
FUENTE = MOD.read_text(encoding="utf-8")
CONF = EJ / "tests/conftest_mutante_r02.py"

MUTANTES = {
    "N00 nulo (control)": ("", ""),
    "N01 _clave_id sin desempate por la cadena": ("for t in re.split(r\"(\\d+)\", x)), x)", "for t in re.split(r\"(\\d+)\", x)),)"),
    "N02 rango de funciones con un solo extremo del documento": ("m.group(1) in loc and m.group(2) in loc", "(m.group(1) in loc or m.group(2) in loc)"),
    "N03 familia desconocida parecida, solo INFO": ("        if p:\n            h(\"d\", \"ERROR\", \"FICHA_CITADA_INEXISTENTE\"", "        if False:\n            h(\"d\", \"ERROR\", \"FICHA_CITADA_INEXISTENTE\""),
    "N04 familia desconocida sin mirar los símbolos": ("        if x in simbolos:\n            continue\n", ""),
    "N05 destino que es una carpeta, sin comprobar": ("        if ruta.is_dir():\n            raise EntradaInvalida", "        if False:\n            raise EntradaInvalida"),
    "N06 OSError al escribir sin capturar": ("    except OSError as e:\n        print(f\"verificador_ids: FALLO CERRADO: no se puede escribir la salida: {e}\", file=sys.stderr)\n        return 2\n", ""),
    "N07 fórmula excusa también lo que está fuera": ("m.start() < c.inicio < m.end() and RE_OPERADOR", "RE_OPERADOR"),
    "N08 JEL excusa cualquier código tras «JEL»": ("m.start(1) <= c.inicio < m.end(1)", "m.start(1) <= c.inicio"),
    "N09 sin normalizar los guiones en las citas": ("            linea = linea.translate(GUIONES)   # misma longitud: las columnas no cambian\n", ""),
    "N10 menciones sin IGNORECASE": ("\'|\"catalog_version\"\\s*:\\s*\"(\\d+(?:\\.\\d+)+)\"\', re.IGNORECASE)", "\'|\"catalog_version\"\\s*:\\s*\"(\\d+(?:\\.\\d+)+)\"\')"),
}

PLANTILLA = """import bloque_a.herramientas.verificador_ids as vi
_src = open(vi.__file__, encoding="utf-8").read()
_viejo, _nuevo = {viejo!r}, {nuevo!r}
if _viejo:
    assert _src.count(_viejo) == 1, "el mutante no se aplica"
    exec(compile(_src.replace(_viejo, _nuevo), vi.__file__, "exec"), vi.__dict__)
"""

vivos, rotos = [], []
try:
    for nombre, (viejo, nuevo) in MUTANTES.items():
        if viejo and FUENTE.count(viejo) != 1:
            print(f"{nombre:52s} -> ROTO (el texto aparece {FUENTE.count(viejo)} veces)")
            rotos.append(nombre)
            continue
        CONF.write_text(PLANTILLA.format(viejo=viejo, nuevo=nuevo), encoding="utf-8")
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "tests.conftest_mutante_r02",
                            "tests/test_t157_verificador_ids.py"], cwd=EJ, capture_output=True, text=True, timeout=900)
        ultima = (r.stdout.strip().splitlines() or [""])[-1]
        fallidas = re.findall(r"^FAILED tests/test_t157_verificador_ids.py::(\S+)", r.stdout, re.M)
        if r.returncode == 0:
            estado = "VIVO"
            if viejo:
                vivos.append(nombre)
        elif r.returncode == 1 and fallidas:
            estado = "MATADO"
        else:
            estado = "ROTO"
            rotos.append(nombre)
        print(f"{nombre:52s} -> {estado:6s} {ultima[:60]} {','.join(f[:40] for f in fallidas[:2])}")
finally:
    if CONF.exists():
        os.remove(CONF)

print(f"\nVivos ({len(vivos)}): {vivos}\nRotos ({len(rotos)}): {rotos}")
sys.exit(1 if rotos or "N00 nulo (control)" in vivos else 0)
