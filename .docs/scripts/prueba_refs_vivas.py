#!/usr/bin/env python3
"""Prueba del gate `refs-vivas` (`tools/refs_vivas.py`), T-65 (QA de T-53, H-11).

Copia el script a un repositorio de juguete en una carpeta temporal y lo ejecuta en cada caso:
1. un informe de `revisores/` que cita un archivo que no existe tiene que hacer fallar el gate (antes, esas carpetas
   quedaban fuera);
2. una orden con argumentos (`.docs/scripts/gate.sh --completo`) cuenta como viva si el script existe;
3. el sufijo de líneas (`archivo.py:10-20`) y una ruta del paquete Python del bloque (`bloque_a/x.py`, que vive en
   `bloque_a/11_Ejecutor/bloque_a/x.py`) cuentan como vivas;
4. un nombre de archivo con espacios se comprueba entero;
5. una ruta rota fuera de `revisores/` sigue haciendo fallar el gate;
6. en una orden, cada argumento con forma de ruta del repo se comprueba también (QA r01 de T-65, H-06).
Uso: python3 .docs/scripts/prueba_refs_vivas.py [ruta del script; por defecto tools/refs_vivas.py]. Sale con 1 si falla.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SCRIPT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else RAIZ / "tools" / "refs_vivas.py"


def _repo(tmp: Path, docs: dict[str, str], archivos: list[str]) -> Path:
    raiz = tmp / "repo"
    (raiz / "tools").mkdir(parents=True)
    shutil.copy(SCRIPT, raiz / "tools" / "refs_vivas.py")
    (raiz / "CLAUDE.md").write_text("Protocolo.\n", encoding="utf-8")
    for a in archivos:
        (raiz / a).parent.mkdir(parents=True, exist_ok=True)
        (raiz / a).write_text("x\n", encoding="utf-8")
    for d, texto in docs.items():
        (raiz / d).parent.mkdir(parents=True, exist_ok=True)
        (raiz / d).write_text(texto, encoding="utf-8")
    return raiz


def _gate(docs: dict[str, str], archivos: list[str]) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as t:
        raiz = _repo(Path(t), docs, archivos)
        r = subprocess.run([sys.executable, "-I", str(raiz / "tools" / "refs_vivas.py")], capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr


CASOS = [
    ("revisores/ con una ruta rota falla", {".docs/tickets/T-99/revisores/informe.md": "Ver `bloque_a/no_existe.py`.\n"}, [], 1),
    ("orden con argumentos viva", {".docs/tickets/T-99/README.md": "Ejecuta `.docs/scripts/gate.sh --completo`.\n"},
     [".docs/scripts/gate.sh"], 0),
    ("sufijo de líneas y ruta de paquete vivas",
     {".docs/tickets/T-99/revisores/codigo.md": "En `bloque_a/orquestacion.py:10-20` y `bloque_a/herramientas/ht03.py:5`.\n"},
     ["bloque_a/11_Ejecutor/bloque_a/orquestacion.py", "bloque_a/11_Ejecutor/bloque_a/herramientas/ht03.py"], 0),
    ("nombre con espacios entero", {"docs/x.md": "Lee `bloque_a/01_Gobernanza/Documento 0 - Protocolo V5.1.md`.\n"},
     ["bloque_a/01_Gobernanza/Documento 0 - Protocolo V5.1.md"], 0),
    ("nombre con espacios roto falla", {"docs/x.md": "Lee `bloque_a/01_Gobernanza/Documento 9 - No existe.md`.\n"},
     ["bloque_a/01_Gobernanza/Documento 0 - Protocolo V5.1.md"], 1),
    ("ruta rota fuera de revisores falla", {".docs/tickets/T-99/README.md": "Ver `tools/no_existe.py`.\n"}, [], 1),
    # QA r01 de T-65, H-06: los argumentos con forma de ruta del repo también se comprueban
    ("argumento roto de una orden falla", {"docs/x.md": "Ejecuta `tools/a.py bloque_a/no_existe.csv`.\n"}, ["tools/a.py"], 1),
    ("argumento vivo de una orden pasa", {"docs/x.md": "Ejecuta `tools/a.py bloque_a/datos.csv --rapido`.\n"},
     ["tools/a.py", "bloque_a/datos.csv"], 0),
]


def main() -> int:
    fallos = 0
    for nombre, docs, archivos, esperado in CASOS:
        codigo, salida = _gate(docs, archivos)
        ok = codigo == esperado
        fallos += not ok
        print(f"{'OK   ' if ok else 'FALLO'} {nombre}: salida {codigo}, esperada {esperado}")
        if not ok:
            print("      " + salida.strip().replace("\n", "\n      "))
    print(f"{len(CASOS) - fallos}/{len(CASOS)} casos correctos")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
