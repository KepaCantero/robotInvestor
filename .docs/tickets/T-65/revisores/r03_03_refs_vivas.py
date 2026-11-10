"""r03_03 · QA T-65 r03 · H-15: `refs-vivas` con intérpretes, comodines, comillas y opciones de salida.

Uso (desde la raíz del repo):  .venv/bin/python -I .docs/tickets/T-65/revisores/r03_03_refs_vivas.py
Monta repositorios de juguete en una carpeta temporal y llama a `comprobar(raiz)` del script del repo.
«HALLAZGO» si deja pasar una ruta rota de verdad en una forma que H-15 dice cubrir, o si rompe en falso con una cita
correcta; «INFO» para formas que H-15 no promete (se anotan, no cuentan).
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
CASOS = [  # (nombre, texto, archivos que existen, ¿debe fallar?, gravedad si no se cumple)
    # intérpretes
    ("bash + script roto", "`bash tools/no.sh`", [], True, "HALLAZGO"),
    ("sh + script vivo", "`sh tools/a.sh --x`", ["tools/a.sh"], False, "HALLAZGO"),
    (".venv/bin/python + script roto", "`.venv/bin/python tools/no.py`", [], True, "HALLAZGO"),
    ("../../.venv/bin/python + script roto", "`../../.venv/bin/python tools/no.py`", [], True, "HALLAZGO"),
    ("python3 -I + script roto", "`python3 -I tools/no.py`", [], True, "HALLAZGO"),
    (".venv/bin/python -I + script roto", "`.venv/bin/python -I .docs/scripts/no.py`", [], True, "HALLAZGO"),
    ("python3 -I + script vivo", "`python3 -I tools/a.py docs/si.md`", ["tools/a.py", "docs/si.md"], False, "HALLAZGO"),
    ("python3 -I + script vivo, arg roto", "`python3 -I tools/a.py docs/no.md`", ["tools/a.py"], True, "HALLAZGO"),
    (".venv/bin/python3 + script roto", "`.venv/bin/python3 tools/no.py`", [], True, "INFO"),
    ("python3.12 + script roto", "`python3.12 tools/no.py`", [], True, "INFO"),
    ("python3 -m pytest + prueba rota", "`python3 -m pytest bloque_a/11_Ejecutor/tests/test_no.py`", [], True, "INFO"),
    ("pytest + prueba rota", "`.venv/bin/pytest -q bloque_a/11_Ejecutor/tests/test_no.py`", [], True, "INFO"),
    ("python3 solo", "`python3`", [], False, "HALLAZGO"),
    # comillas
    ("arg con comillas y espacios, vivo", f"`tools/a.py \"{DOC0}\"`", ["tools/a.py", DOC0], False, "HALLAZGO"),
    ("arg con comillas simples y espacios, vivo", f"`tools/a.py '{DOC0}'`", ["tools/a.py", DOC0], False, "HALLAZGO"),
    ("arg con comillas y espacios, roto", "`tools/a.py \"bloque_a/01_Gobernanza/Documento 9 - P.md\"`", ["tools/a.py"], True,
     "HALLAZGO"),
    ("script entre comillas, roto", "`python3 \"tools/no.py\"`", [], True, "HALLAZGO"),
    # comodines
    ("comodín ? que casa", "`tools/a.py docs/x?.md`", ["tools/a.py", "docs/x1.md"], False, "HALLAZGO"),
    ("comodín [] que casa", "`tools/a.py docs/x[12].md`", ["tools/a.py", "docs/x1.md"], False, "HALLAZGO"),
    ("comodín ** que casa", "`tools/a.py docs/**/y.md`", ["tools/a.py", "docs/s/y.md"], False, "HALLAZGO"),
    ("comodín que no casa", "`tools/a.py docs/zz*.md`", ["tools/a.py"], True, "HALLAZGO"),
    ("comodín suelto que no casa", "`docs/zz*.md`", [], True, "HALLAZGO"),
    ("comodín de paquete de bloque que casa", "`tools/a.py bloque_a/herramientas/*.py`",
     ["tools/a.py", "bloque_a/11_Ejecutor/bloque_a/herramientas/h.py"], False, "HALLAZGO"),
    ("comodín que sube fuera del repo", "`tools/a.py docs/../../*`", ["tools/a.py"], True, "INFO"),
    ("corchete literal en el nombre, vivo", "`docs/[PROPUESTO].md`", ["docs/[PROPUESTO].md"], False, "INFO"),
    # opciones de salida
    ("--salida= sin crear", "`tools/a.py --salida=docs/nuevo.md`", ["tools/a.py"], False, "HALLAZGO"),
    ("--out sin crear", "`tools/a.py --out docs/nuevo.md`", ["tools/a.py"], False, "HALLAZGO"),
    ("-o sin crear y entrada rota después", "`tools/a.py -o docs/nuevo.md docs/no.md`", ["tools/a.py"], True, "HALLAZGO"),
    ("-o al final sin valor", "`tools/a.py docs/si.md -o`", ["tools/a.py", "docs/si.md"], False, "HALLAZGO"),
    ("opción de entrada no es salida", "`tools/a.py --datos docs/no.md`", ["tools/a.py"], True, "HALLAZGO"),
    ("--salida con intérprete", "`python3 tools/a.py --salida docs/nuevo.md`", ["tools/a.py"], False, "HALLAZGO"),
    ("-O (mayúscula) no es salida", "`tools/a.py -O docs/no.md`", ["tools/a.py"], True, "INFO"),
    # lo de siempre
    ("ruta suelta rota", "`docs/no.md`", [], True, "HALLAZGO"),
    ("ruta suelta con espacios, viva", f"`{DOC0}`", [DOC0], False, "HALLAZGO"),
]

hall = info = 0
for nombre, texto, archivos, debe_fallar, grav in CASOS:
    rotas = gate(texto, archivos)
    ok = bool(rotas) == debe_fallar
    if not ok:
        hall += grav == "HALLAZGO"
        info += grav == "INFO"
    print(f"{'OK' if ok else grav:9s} {nombre}: {'falla' if rotas else 'pasa'} (esperado: {'falla' if debe_fallar else 'pasa'}) "
          f"{rotas[:1]}")
reales = rv.comprobar(RAIZ)
print(f"{'OK' if not reales else 'HALLAZGO':9s} repo real: {len(reales)} citas rotas {reales[:3]}")
hall += bool(reales)
print(f"HALLAZGOS: {hall} · INFO: {info}")
