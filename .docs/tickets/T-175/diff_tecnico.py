"""T-175 (CA-4): el técnico de un ciclo mock normal solo cambia en 4.N.4 y en las filas «(alternativa descartada)» de la sección 6.

    cd bloque_a/11_Ejecutor
    ../../.venv/bin/python ../../.docs/tickets/T-175/diff_tecnico.py generar /ruta/tecnico.md     # con el código de esta copia
    ../../.venv/bin/python ../../.docs/tickets/T-175/diff_tecnico.py comparar antes.md despues.md  # 1 si algo cambia fuera de lo esperado

Para el «antes», `generar` con el código de origin/develop anterior a T-175 (otra copia de trabajo).
"""
import difflib
import re
import shutil
import sys
import tempfile
from pathlib import Path


def generar(destino: str) -> int:
    sys.path.insert(0, "tests")
    from conftest import AS_OF, RUTA_UNIVERSO_EJEMPLO, cargar_universo, nuevo_bloque
    tmp = tempfile.mkdtemp()
    try:
        r = nuevo_bloque(tmp, cargar_universo(RUTA_UNIVERSO_EJEMPLO)).ciclo(AS_OF)
        Path(destino).write_text(Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8"), encoding="utf-8")
        print(f"técnico en {destino} · entrega {r.get('entrega') or 'ENTREGADA'} · G3 {r['g3'].get('dictamen')}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


ESPERADAS = (re.compile(r"^#### 4\.\d+\.4 Alternativas descartadas relevantes$"),
             re.compile(r"^Finalistas que no entran en el top-3 porque no son elegibles"),
             re.compile(r"^\| Candidata \| Puerta en la que quedó \| Motivo \| Qué tendría que ocurrir \|$"),
             re.compile(r"^\|---\|---\|---\|---\|$"),
             re.compile(r"^\| .* · `OPP-\d{4}-\d+`( \(RK [\d.]+\))? \| "),
             re.compile(r"^\| `OPP-\d{4}-\d+` \(alternativa descartada\) \| "),
             re.compile(r"^$"))


def comparar(antes: str, despues: str) -> int:
    a = Path(antes).read_text(encoding="utf-8").splitlines()
    d = Path(despues).read_text(encoding="utf-8").splitlines()
    ruta = re.compile(r"^\| Entregables hermanos \|")   # lleva la carpeta temporal del ciclo
    malas, nuevas = [], []
    for linea in difflib.unified_diff(a, d, lineterm="", n=0):
        if linea.startswith(("---", "+++", "@@")):
            continue
        cuerpo = linea[1:]
        if ruta.match(cuerpo):
            continue
        if linea.startswith("+") and any(p.match(cuerpo) for p in ESPERADAS):
            nuevas.append(cuerpo)
        else:
            malas.append(linea)
    print(f"{len(nuevas)} líneas nuevas esperadas · {len(malas)} cambios fuera de lo esperado")
    for x in malas:
        print("  ", x[:200])
    return 1 if malas else 0


if __name__ == "__main__":
    orden, *args = sys.argv[1:]
    sys.exit(generar(*args) if orden == "generar" else comparar(*args))
