"""T-203 · prueba de equivalencia: las salidas del ejecutor del Bloque A no cambian.

Ejecuta, en dos copias del repositorio (la base, p. ej. origin/develop, y la del ticket), con el
cliente simulado y el Python del `.venv`:
  1. el backtest del README de `bloque_a/11_Ejecutor` (2024-01-05 → 2024-03-29);
  2. un ciclo C1 con `--as-of 2026-06-05`;
  3. una petición CT-01 (`ejemplos/peticiones/peticion_ad_hoc.json`) sobre el estado del ciclo;
  4. una consulta CT-03 sobre ese mismo estado.
Las dos copias se ejecutan en la MISMA carpeta temporal (`<trabajo>/run`, que después se renombra), así
que las rutas que el ejecutor escribe en F5, en los informes y en las cadenas de huellas coinciden sin
tocarlas. Compara byte a byte la salida estándar, la de error y todos los ficheros que deja cada orden
(estado y entregables); lo único que se normaliza son las latencias medidas con el reloj real
(`"latencia_s": …` en JSON y la columna `latencia_s` de `consumo.csv`), y las bases SQLite se comparan
por su volcado SQL (`iterdump`), no por sus páginas. Cualquier otra diferencia es un fallo.

Uso (con el Python del `.venv`, fuera del árbol que se compara):
    python -I equivalencia.py <raiz_base> <raiz_ticket> <carpeta_de_trabajo>
Termina con 0 si todo es igual y con 1 si algo difiere (lo nombra).
"""
from __future__ import annotations

import os
import re
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

ORDENES = [
    ("backtest", ["--salida", "{T}/bt", "--estado", "{T}/est_bt", "backtest", "--desde", "2024-01-05", "--hasta", "2024-03-29"]),
    ("ciclo", ["--salida", "{T}/ent", "--estado", "{T}/est", "--as-of", "2026-06-05", "ciclo"]),
    ("peticion", ["--salida", "{T}/ent", "--estado", "{T}/est", "--as-of", "2026-06-05", "peticion", "--json",
                  "ejemplos/peticiones/peticion_ad_hoc.json"]),
    ("consulta", ["--salida", "{T}/ent", "--estado", "{T}/est", "--as-of", "2026-06-05", "consulta",
                  "¿Por qué no aparece la renta fija esta semana?"]),
]
COMUNES = ["--cliente", "mock", "--datos", "ejemplos/datos_sinteticos", "--universo", "config/universo_ejemplo.csv"]
LATENCIAS = re.compile(rb'("latencia_s"\s*:\s*)[0-9.eE+-]+')


def ejecutar(raiz: Path, destino: Path) -> None:
    ejecutor = raiz / "bloque_a" / "11_Ejecutor"
    py = raiz / ".venv" / "bin" / "python"
    trabajo = destino.parent / "run"
    for d in (trabajo, destino):
        if d.exists():
            shutil.rmtree(d)
    trabajo.mkdir(parents=True)
    entorno = dict(os.environ, PYTHONPATH=str(ejecutor), PYTHONHASHSEED="0")
    origen = subprocess.run([str(py), "-c", "import bloque_a; print(bloque_a.__file__)"], cwd=ejecutor, env=entorno,
                            capture_output=True, text=True, check=True).stdout.strip()
    if not origen.startswith(str(ejecutor)):
        sys.exit(f"bloque_a se importa de {origen}, no de {ejecutor}")
    for nombre, args in ORDENES:
        orden = [str(py), "-m", "bloque_a.cli", *COMUNES, *[a.replace("{T}", str(trabajo)) for a in args]]
        r = subprocess.run(orden, cwd=ejecutor, env=entorno, capture_output=True)
        (trabajo / f"{nombre}.out").write_bytes(r.stdout)
        (trabajo / f"{nombre}.err").write_bytes(r.stderr)
        (trabajo / f"{nombre}.rc").write_text(str(r.returncode))
    trabajo.rename(destino)


def contenido(ruta: Path) -> bytes:
    if ruta.suffix == ".sqlite3":
        con = sqlite3.connect(f"file:{ruta}?mode=ro", uri=True)
        try:
            return LATENCIAS.sub(rb"\g<1>0", "\n".join(con.iterdump()).encode())
        finally:
            con.close()
    datos = ruta.read_bytes()
    if ruta.name == "consumo.csv":                      # última columna: latencia_s
        filas = datos.decode().splitlines()
        if filas and filas[0].endswith(",latencia_s"):
            datos = "\n".join(f.rsplit(",", 1)[0] for f in filas).encode()
    return LATENCIAS.sub(rb"\g<1>0", datos)


def main() -> int:
    base, nuevo, trabajo = (Path(a).resolve() for a in sys.argv[1:4])
    tb, tn = trabajo / "base", trabajo / "nuevo"
    ejecutar(base, tb)
    ejecutar(nuevo, tn)
    fb = sorted(p.relative_to(tb) for p in tb.rglob("*") if p.is_file())
    fn = sorted(p.relative_to(tn) for p in tn.rglob("*") if p.is_file())
    fallos = [f"solo en uno: {p}" for p in sorted(set(fb) ^ set(fn))]
    for rel in sorted(set(fb) & set(fn)):
        if contenido(tb / rel) != contenido(tn / rel):
            fallos.append(f"distinto: {rel}")
    rcs = {n: (tb / f"{n}.rc").read_text() for n, _ in ORDENES}
    print(f"{len(fb)} ficheros comparados; códigos de salida de la base: {rcs}")
    for f in fallos:
        print(f)
    print("IGUALES" if not fallos else f"{len(fallos)} DIFERENCIAS")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
