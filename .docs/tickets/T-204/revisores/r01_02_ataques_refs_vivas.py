"""QA r01 de T-204: ataques a `tools/refs_vivas.py` (bloque retirado). Cada caso monta un repositorio de juguete con el
script y espera un código de salida. Los casos «hueco» documentan por dónde se cuela una cita viva al Forex sin la marca;
los casos «no se relaja» comprueban que una ruta muerta que no es del Forex sigue fallando aunque la línea lleve la marca.
Uso: python3 -I r01_02_ataques_refs_vivas.py [ruta de refs_vivas.py]. Sale con 1 si algún caso no da lo esperado."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
SCRIPT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else RAIZ / "tools" / "refs_vivas.py"
CASOS = [
    # (nombre, documentos, archivos que existen, salida esperada)
    ("hueco: marca de otro ticket (T-2040) no vale", {"docs/x.md": "Ver `bloque_a_forex/x.py` (T-2040).\n"}, [], 1),
    ("hueco: marca T-204 dentro de T-2041 no vale", {"CLAUDE.md": "| `bloque_a_forex/` | ver T-2041 |\n"}, [], 1),
    ("hueco: nombre de archivo con = sigue siendo del bloque retirado", {"docs/x.md": "Ver `bloque_a_forex/a=b.md`.\n"}, [], 1),
    ("no se relaja: marca y ruta muerta de A en la misma línea", {"docs/x.md": "`bloque_a_forex/` y `bloque_a/no_existe.py` (T-204).\n"}, [], 1),
    ("no se relaja: marca y ruta muerta de B en la misma cita (orden)",
     {"prompts/x.md": "`pytest -q bloque_a_forex/11_Ejecutor bloque_b/no_existe.py` (T-204).\n"}, [], 1),
    ("no se relaja: ruta muerta de tools en un ticket con el Forex",
     {".docs/tickets/T-1/x.md": "`tools/a.py --datos=bloque_a_forex/x.csv tools/no.csv`.\n"}, ["tools/a.py"], 1),
    ("no se relaja: ruta muerta de .docs fuera de los registros", {".docs/knowledge/x.md": "Ver `.docs/scripts/no_existe.sh` (T-204).\n"}, [], 1),
    ("no se relaja: ruta muerta normal en un registro", {".docs/diario/2026-11.md": "Ver `tools/no_existe.py`.\n"}, [], 1),
    ("no se relaja: bloque_a_forexx (otro nombre) muerto no es raíz válida, como en develop",
     {"docs/x.md": "Ver `bloque_a_forexx/x.py`.\n"}, [], 0),
    ("vivo: cita marcada del bloque retirado", {"docs/x.md": "`bloque_a_forex/` (eliminado, T-204).\n"}, [], 0),
    ("vivo: cita del Forex en la memoria", {".docs/memoria/claude/x.md": "`bloque_a_forex/x`\n"}, [], 0),
]


def correr(docs: dict, archivos: list) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as t:
        raiz = Path(t) / "repo"
        (raiz / "tools").mkdir(parents=True)
        shutil.copy(SCRIPT, raiz / "tools" / "refs_vivas.py")
        (raiz / "CLAUDE.md").write_text("Protocolo.\n", encoding="utf-8")
        for a in archivos:
            (raiz / a).parent.mkdir(parents=True, exist_ok=True)
            (raiz / a).write_text("x\n", encoding="utf-8")
        for d, texto in docs.items():
            (raiz / d).parent.mkdir(parents=True, exist_ok=True)
            (raiz / d).write_text(texto, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(raiz / "tools" / "refs_vivas.py")], capture_output=True, text=True, check=False)
        return r.returncode, r.stdout.strip()


malos = 0
for nombre, docs, archivos, esperada in CASOS:
    rc, out = correr(docs, archivos)
    ok = rc == esperada
    malos += not ok
    print(f"{'OK   ' if ok else 'FALLO'} {nombre}: salida {rc}, esperada {esperada}")
    if not ok:
        print("      " + out.replace("\n", "\n      "))
print(f"{len(CASOS) - malos}/{len(CASOS)} casos correctos")
sys.exit(1 if malos else 0)
