"""Sondas del revisor sobre la batería de la pieza 2 (V0.61).

Ejecutar desde la raíz de marcoC:  python3 sondas_revisor_v061.py

S1: inyectar una constante de código nueva en una COPIA de validador -> la batería debe FALLAR
    (la coherencia código-catálogo se vigila de verdad).
S2: corregir el texto de (diario, O-00) al significado real del Diario -> la batería SIGUE EN VERDE
    (demuestra que ningún check protege la exactitud de los textos).
S3: corregir el efecto de (k_calidad, Q-01) a AVISO -> la batería SIGUE EN VERDE (idem efectos).
S4: control positivo: quitar una entrada del catálogo -> la batería debe FALLAR.
S5: conteos auxiliares: 250 códigos distintos (claim), nº de sitios de emisión de O-01/O-00/O-02.

Nota de la pos-revisión: S2 y S3 se escribieron contra la entrega SIN corregir; en el estado pos-revisión
los valores que inyectan son ya los del catálogo (por eso siguen en verde). La protección que pedían la dan
ahora las regresiones r01/r02/r04 de la batería, verificadas en sentido inverso (revertir la corrección hace
fallar la batería); véase revision.md.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

print("S1: código nuevo inyectado en copia temporal")
with tempfile.TemporaryDirectory() as tmp:
    copia = Path(tmp) / "marcoC"
    shutil.copytree(RAIZ, copia, ignore=shutil.ignore_patterns("entrega_glm", "*.pyc", "__pycache__"))
    objetivo = copia / "validador" / "vigilancia.py"
    txt = objetivo.read_text(encoding="utf-8")
    objetivo.write_text(txt + '\nSONDA_REVISOR = "H-99"\n', encoding="utf-8")
    r = subprocess.run([sys.executable, str(copia / "pruebas" / "pruebas_catalogo_codigos.py")],
                       capture_output=True, text=True, cwd=str(copia))
    ultima = [l for l in r.stdout.splitlines() if l.strip()][-1]
    faltan = [l for l in r.stdout.splitlines() if "todo_codigo_en_el_codigo" in l]
    print(f"  exit={r.returncode} | {ultima}")
    print(f"  check que debe dispararse: {faltan[0] if faltan else 'NO APARECIÓ'}")

print("S2/S3: textos y efectos corregidos no alteran el resultado de la batería")
import re
sys.path.insert(0, str(RAIZ / "validador"))
sys.path.insert(0, str(RAIZ / "pruebas"))
import catalogo_codigos
catalogo_codigos.CATALOGO[("diario", "O-00")]["que"] = "operación que lanzó una excepción no recogida: se anota y se reproduce igual"  # S2
catalogo_codigos.CATALOGO[("k_calidad", "Q-01")]["efecto"] = "AVISO"  # S3
import importlib
pc = importlib.import_module("pruebas_catalogo_codigos")
rc = pc.main()
print(f"  batería con textos/efectos CORREGIDOS -> exit {rc} (0 = sigue pasando: no hay check que los vigile)")

print("S4: control positivo (entrada eliminada del catálogo)")
del catalogo_codigos.CATALOGO[("vigilancia", "H-19")]
rc2 = pc.main()
print(f"  batería sin H-19 -> exit {rc2} (1 = falla como debe)")

print("S5: conteos auxiliares")
sys.path.insert(0, str(RAIZ / "validador"))
from catalogo_codigos import codigos_en_el_codigo
cs = codigos_en_el_codigo(RAIZ / "validador")
distintos = {c for _, c in cs}
print(f"  códigos distintos: {len(distintos)} (claim: 250)")
for mod, cod in (("orquestador", "O-01"), ("orquestador", "O-00"), ("orquestador", "O-02")):
    n = (RAIZ / "validador" / f"{mod}.py").read_text(encoding="utf-8").count(f'"{cod}"')
    print(f"  apariciones de \"{cod}\" en {mod}.py: {n}")
