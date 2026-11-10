"""r01_02 · QA T-65 · H-11: ¿el nuevo `refs-vivas` deja pasar referencias rotas o rompe en falso?

Uso (desde la raíz del repo):  .venv/bin/python -I .docs/tickets/T-65/revisores/r01_02_refs_vivas.py
Monta repositorios de juguete en una carpeta temporal y llama a `comprobar(raiz)` del script del repo.
"""
import importlib.util
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("refs_vivas", RAIZ / "tools" / "refs_vivas.py")
rv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rv)


def gate(docs: dict, archivos: list) -> list:
    with tempfile.TemporaryDirectory() as t:
        raiz = Path(t)
        (raiz / "CLAUDE.md").write_text("x\n", encoding="utf-8")
        for a in archivos:
            (raiz / a).parent.mkdir(parents=True, exist_ok=True)
            if a.endswith("/"):
                (raiz / a).mkdir(parents=True, exist_ok=True)
            else:
                (raiz / a).write_text("x\n", encoding="utf-8")
        for d, txt in docs.items():
            (raiz / d).parent.mkdir(parents=True, exist_ok=True)
            (raiz / d).write_text(txt, encoding="utf-8")
        return rv.comprobar(raiz)


D = ".docs/tickets/T-99/revisores/informe.md"
CASOS = [
    # (nombre, texto del informe, archivos que existen, ¿debe fallar?)
    ("rota con sufijo de línea", "`bloque_a/no_existe.py:12`", [], True),
    ("orden con script inexistente", "`tools/no_existe.sh --completo`", [], True),
    ("orden .py inexistente con argumentos", "`.docs/scripts/no.py --x 1`", [], True),
    ("paquete de bloque_b viva", "`bloque_b/motor.py:3`", ["bloque_b/11_Ejecutor/bloque_b/motor.py"], False),
    ("paquete de bloque_a_forex viva", "`bloque_a_forex/x.py`", ["bloque_a_forex/11_Ejecutor/bloque_a_forex/x.py"], False),
    ("paquete inexistente en 11_Ejecutor", "`bloque_a/nada.py`", ["bloque_a/11_Ejecutor/bloque_a/otro.py"], True),
    ("ruta de 11_Ejecutor sin paquete: `bloque_a/tests/x.py` (vive en 11_Ejecutor/tests)", "`bloque_a/tests/x.py`",
     ["bloque_a/11_Ejecutor/tests/x.py"], None),
    ("dos rutas en una cita; la segunda rota", "`tools/a.py tools/no_existe.py`", ["tools/a.py"], None),
    ("orden con script vivo y argumento que es una ruta rota", "`tools/a.py bloque_a/no_existe.csv`", ["tools/a.py"], None),
    ("carpeta viva con barra final", "`bloque_a/11_Ejecutor/`", ["bloque_a/11_Ejecutor/"], False),
    ("sufijo de línea en un .md vivo", "`docs/incidencias.md:40`", ["docs/incidencias.md"], False),
    ("rango de líneas y archivo roto", "`bloque_a/11_Ejecutor/bloque_a/x.py:10-20`", [], True),
    ("nombre con espacios y argumentos no se parte", "`bloque_a/Documento 0 - V5.1.md`", ["bloque_a/Documento 0 - V5.1.md"], False),
    ("informe de revisores en un ticket cualquiera, rota", "`sistema_global/no_existe.md`", [], True),
    ("ruta en .docs/memoria (no se toca), rota", "`.docs/no_existe.md`", [], True),
]
hall = 0
for nombre, texto, archivos, debe_fallar in CASOS:
    rotas = gate({D: f"Cita {texto}.\n"}, archivos)
    falla = bool(rotas)
    if debe_fallar is None:
        print(f"INFO      {nombre}: {'falla' if falla else 'pasa'} {rotas}")
        continue
    ok = falla == debe_fallar
    hall += not ok
    print(f"{'OK      ' if ok else 'HALLAZGO'}  {nombre}: {'falla' if falla else 'pasa'} (esperado: {'falla' if debe_fallar else 'pasa'})")

# El repo real con el script nuevo: ¿qué informes de revisores/ quedan rotos?
rotas = rv.comprobar(RAIZ)
print(f"\nRepo real: {len(rotas)} citas rotas")
for r in rotas[:30]:
    print("  " + r)
print(f"HALLAZGOS: {hall}")
sys.exit(1 if hall else 0)
