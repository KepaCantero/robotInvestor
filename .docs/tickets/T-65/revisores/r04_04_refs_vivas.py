"""r04_04 · QA T-65 r04 · H-22: `refs-vivas` con `shlex`: que no deje pasar rutas rotas ni rompa en falso.

Uso (desde la raíz del repo):  .venv/bin/python -I .docs/tickets/T-65/revisores/r04_04_refs_vivas.py
Como r03_03: repositorios de juguete y `comprobar(raiz)` del script del repo. «HALLAZGO» si deja pasar una ruta rota en
una forma que el docstring de `tools/refs_vivas.py` dice cubrir, o si rompe en falso con una cita correcta; «INFO» para
formas que no promete (se anotan, no cuentan).
"""
import importlib.util
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("refs_vivas", RAIZ / "tools" / "refs_vivas.py")
rv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rv)


def gate(texto: str, archivos: list) -> list:
    with tempfile.TemporaryDirectory() as t:
        raiz = Path(t)
        (raiz / "CLAUDE.md").write_text("x\n", encoding="utf-8")
        for a in archivos:
            (raiz / a).parent.mkdir(parents=True, exist_ok=True)
            (raiz / a).write_text("x\n", encoding="utf-8")
        (raiz / "docs").mkdir(exist_ok=True)
        (raiz / "docs" / "x.md").write_text(texto, encoding="utf-8")
        return rv.comprobar(raiz)


DOC0 = "bloque_a/01_Gobernanza/Documento 0 - P.md"
APOS = "docs/l'acta.md"
CASOS = [  # (nombre, texto, archivos que existen, ¿debe fallar?, gravedad si no se cumple)
    # rutas sueltas (no son órdenes): la cita entera
    ("ruta suelta con espacios, rota", "`bloque_a/01_Gobernanza/Documento 9 - P.md`", [], True, "HALLAZGO"),
    ("ruta suelta con espacios, viva", f"`{DOC0}`", [DOC0], False, "HALLAZGO"),
    ("ruta suelta con apóstrofo, viva", f"`{APOS}`", [APOS], False, "HALLAZGO"),
    ("ruta suelta con apóstrofo, rota", "`docs/l'otra.md`", [], True, "HALLAZGO"),
    ("ruta suelta con espacios cuyo primer trozo acaba en .py, viva", "`tools/a.py b.md`", ["tools/a.py b.md"], False, "INFO"),
    ("ruta con .. dentro del repo, viva", "`docs/../tools/a.py`", ["tools/a.py"], False, "INFO"),
    ("ruta que sale del repo", "`docs/../../etc/passwd`", [], True, "HALLAZGO"),
    ("ruta con :líneas, rota", "`tools/no.py:10-20`", [], True, "HALLAZGO"),
    ("directorio vivo con barra final", "`tools/`", ["tools/a.py"], False, "HALLAZGO"),
    # órdenes
    ("script vivo + arg entre comillas con espacios, vivo", f"`tools/a.py \"{DOC0}\"`", ["tools/a.py", DOC0], False, "HALLAZGO"),
    ("script vivo + arg entre comillas con espacios, roto", "`tools/a.py \"bloque_a/01_Gobernanza/Documento 9 - P.md\"`",
     ["tools/a.py"], True, "HALLAZGO"),
    ("script vivo + arg con espacio escapado, vivo", "`tools/a.py bloque_a/01_Gobernanza/Documento\\ 0\\ -\\ P.md`",
     ["tools/a.py", DOC0], False, "HALLAZGO"),
    ("script vivo + arg con apóstrofo (comillas sin cerrar), roto", "`tools/a.py docs/l'otra.md`", ["tools/a.py"], True, "HALLAZGO"),
    ("script vivo + arg con apóstrofo (comillas sin cerrar), vivo", f"`tools/a.py {APOS}`", ["tools/a.py", APOS], False, "HALLAZGO"),
    ("script roto entre comillas", "`\"tools/no.py\" --x`", [], True, "HALLAZGO"),
    ("python3 -I -X utf8 + script roto", "`python3 -I -X utf8 tools/no.py`", [], True, "HALLAZGO"),
    ("python3 -Xutf8 + script roto", "`python3 -Xutf8 tools/no.py`", [], True, "HALLAZGO"),
    ("python3 -W ignore + script roto", "`python3 -W ignore tools/no.py`", [], True, "HALLAZGO"),
    ("python3 -c código: no se comprueba", "`python3 -c \"import tools.no\"`", [], False, "HALLAZGO"),
    ("python3 -m módulo + arg roto", "`python3 -m pytest -q bloque_a/11_Ejecutor/tests/test_no.py`", [], True, "HALLAZGO"),
    ("python3 -m módulo + arg vivo", "`python3 -m pytest -q bloque_a/11_Ejecutor/tests/t.py`", ["bloque_a/11_Ejecutor/tests/t.py"],
     False, "HALLAZGO"),
    ("python3 -Im pytest + arg roto", "`python3 -Im pytest bloque_a/11_Ejecutor/tests/test_no.py`", [], True, "INFO"),
    ("bash -x + script roto", "`bash -x tools/no.sh`", [], True, "HALLAZGO"),
    ("bash -c código", "`bash -c \"tools/no.sh\"`", [], False, "INFO"),
    ("pytest + arg roto", "`pytest -q bloque_a/11_Ejecutor/tests/test_no.py`", [], True, "HALLAZGO"),
    ("pytest + arg vivo y -k con espacios", "`pytest -q -k \"a and b\" bloque_a/11_Ejecutor/tests/t.py`",
     ["bloque_a/11_Ejecutor/tests/t.py"], False, "HALLAZGO"),
    ("pytest -o ini=valor + arg roto", "`pytest -o addopts= bloque_a/11_Ejecutor/tests/test_no.py`", [], True, "INFO"),
    ("pytest -p no:cacheprovider + arg roto", "`pytest -p no:cacheprovider bloque_a/11_Ejecutor/tests/test_no.py`", [], True,
     "HALLAZGO"),
    ("script vivo + --salida=archivo futuro", "`tools/a.py --salida=docs/futuro.md`", ["tools/a.py"], False, "HALLAZGO"),
    ("script vivo + -o archivo futuro + arg roto", "`tools/a.py -o docs/futuro.md docs/no.md`", ["tools/a.py"], True, "HALLAZGO"),
    ("comodín vivo como arg", "`tools/a.py bloque_a/11_Ejecutor/tests/test_*.py`", ["tools/a.py", "bloque_a/11_Ejecutor/tests/test_x.py"],
     False, "HALLAZGO"),
    ("comodín que no casa", "`tools/a.py bloque_a/11_Ejecutor/tests/zz_*.py`", ["tools/a.py"], True, "HALLAZGO"),
    ("variable de entorno delante + script roto", "`PYTHONPATH=. python3 tools/no.py`", [], True, "INFO"),
    ("cd && orden con script roto", "`cd bloque_a/11_Ejecutor && ../../.venv/bin/python tools/no.py`", [], True, "INFO"),
    ("tubería a un archivo de salida futuro", "`tools/a.py | tee docs/futuro.log`", ["tools/a.py"], False, "INFO"),
    ("python solo", "`python3`", [], False, "HALLAZGO"),
    ("palabra «sh» con ruta rota detrás (prosa)", "`sh docs/no.md`", [], True, "INFO"),
]

hall = info = 0
for nombre, texto, archivos, debe_fallar, grav in CASOS:
    try:
        rotas = gate(texto, archivos)
    except Exception as e:  # noqa: BLE001
        hall += 1
        print(f"HALLAZGO  {nombre}: el script lanza {type(e).__name__}: {e}")
        continue
    falla = bool(rotas)
    ok = falla == debe_fallar
    et = "OK" if ok else grav
    if not ok:
        hall += grav == "HALLAZGO"
        info += grav == "INFO"
    print(f"{et:9} {nombre}: {'falla' if falla else 'pasa'} (esperado: {'falla' if debe_fallar else 'pasa'}) {rotas[:2]}")

rotas = rv.comprobar(RAIZ)
hall += 1 if rotas else 0
print(f"{'OK' if not rotas else 'HALLAZGO':9} repo real: {len(rotas)} citas rotas {rotas[:3]}")
print(f"HALLAZGOS: {hall} · INFO: {info}")
