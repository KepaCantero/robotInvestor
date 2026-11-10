"""r02_02 · QA T-65 r02 · H-06 (r01): `refs-vivas` con los argumentos de una orden. ¿Deja pasar rotas o rompe en falso?

Uso (desde la raíz del repo):  .venv/bin/python -I .docs/tickets/T-65/revisores/r02_02_refs_vivas.py
Monta repositorios de juguete en una carpeta temporal y llama a `comprobar(raiz)` del script del repo. Además comprueba
que el repo real no tiene citas rotas y que `normalizar_cita` (API anterior) sigue dando la ruta principal.
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
            if a.endswith("/"):
                (raiz / a).mkdir(parents=True, exist_ok=True)
            else:
                (raiz / a).write_text("x\n", encoding="utf-8")
        (raiz / "docs").mkdir(exist_ok=True)
        (raiz / "docs" / "x.md").write_text(texto, encoding="utf-8")
        return rv.comprobar(raiz)


# (nombre, texto, archivos que existen, ¿debe fallar?, gravedad si no se cumple: HALLAZGO o INFO)
CASOS = [
    ("arg roto tras opción", "`tools/a.py --datos bloque_a/no.csv`", ["tools/a.py"], True, "HALLAZGO"),
    ("dos args, el segundo roto", "`tools/a.sh docs/si.md docs/no.md`", ["tools/a.sh", "docs/si.md"], True, "HALLAZGO"),
    ("arg con sufijo de líneas roto", "`tools/a.py bloque_a/no.py:10-20`", ["tools/a.py"], True, "HALLAZGO"),
    ("arg de paquete de bloque vivo", "`tools/a.py bloque_a/x.py`", ["tools/a.py", "bloque_a/11_Ejecutor/bloque_a/x.py"], False,
     "HALLAZGO"),
    ("arg carpeta con barra viva", "`tools/a.sh bloque_a/11_Ejecutor/`", ["tools/a.sh", "bloque_a/11_Ejecutor/"], False, "HALLAZGO"),
    ("script vivo, args no-ruta", "`tools/a.sh --completo -q 3`", ["tools/a.sh"], False, "HALLAZGO"),
    ("script roto con args vivos", "`tools/no.sh docs/si.md`", ["docs/si.md"], True, "HALLAZGO"),
    ("arg glob que casa con archivos", "`tools/a.py bloque_a/11_Ejecutor/tests/test_t65_*.py`",
     ["tools/a.py", "bloque_a/11_Ejecutor/tests/test_t65_x.py"], False, "INFO"),
    ("arg de salida aún no creado", "`tools/a.py --salida docs/nuevo.md`", ["tools/a.py"], False, "INFO"),
    ("intérprete delante, script roto", "`python3 tools/no.py docs/si.md`", ["docs/si.md"], True, "INFO"),
    ("arg con comillas, roto", "`tools/a.py \"docs/no.md\"`", ["tools/a.py"], True, "INFO"),
    ("ruta con espacios sin orden, viva", "`bloque_a/01_Gobernanza/Documento 0 - P.md`", ["bloque_a/01_Gobernanza/Documento 0 - P.md"],
     False, "HALLAZGO"),
    ("ruta con espacios sin orden, rota", "`bloque_a/01_Gobernanza/Documento 9 - P.md`", [], True, "HALLAZGO"),
]

hall = info = 0
for nombre, texto, archivos, debe_fallar, grav in CASOS:
    rotas = gate(texto, archivos)
    ok = bool(rotas) == debe_fallar
    if not ok:
        hall += grav == "HALLAZGO"
        info += grav == "INFO"
    estado = "OK" if ok else grav
    print(f"{estado:9s} {nombre}: {'falla' if rotas else 'pasa'} (esperado: {'falla' if debe_fallar else 'pasa'}) {rotas[:1]}")

api = rv.normalizar_cita("tools/a.py bloque_a/x.csv")
print(f"{'OK' if api == 'tools/a.py' else 'HALLAZGO':9s} normalizar_cita da la ruta principal: {api!r}")
hall += api != "tools/a.py"
reales = rv.comprobar(RAIZ)
print(f"{'OK' if not reales else 'HALLAZGO':9s} repo real: {len(reales)} citas rotas {reales[:3]}")
hall += bool(reales)
print(f"HALLAZGOS: {hall} · INFO: {info}")
