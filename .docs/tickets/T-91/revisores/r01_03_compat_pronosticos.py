"""QA r01 de T-91 · 03: compatibilidad de `pronosticos.csv` entre 7feb697^ y HEAD con el mismo backtest simulado
(RV y DIV, 2026-03-06 a 2026-06-26, datos sintéticos sin tocar).

  .venv/bin/python -I .docs/tickets/T-91/revisores/r01_03_compat_pronosticos.py --base RUTA_11_EJECUTOR_DE_7feb697^ [--ejecutor RUTA]

Esperado: las 30 columnas de la base, con los mismos valores fila a fila (con datos al día no hay nada que alinear), y las dos
nuevas al final. Un lector por posición o por nombre de la V anterior sigue funcionando."""
import csv
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve()
sys.path.insert(0, str(AQUI.parents[2] / "T-88" / "revisores"))
from r01_comun import Marcador, preparar  # noqa: E402

a, resto, ej = preparar(__doc__)
if "--trabajador" in resto:
    from bloque_a.backtest import ejecutar_backtest
    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
    from conftest import DATOS, config_pruebas
    ejecutar_backtest(config_pruebas(perfiles={"activos": ["RV", "DIV"]}), "2026-03-06", "2026-06-26", str(DATOS),
                      str(RUTA_UNIVERSO_EJEMPLO), resto[resto.index("--trabajador") + 1])
    sys.exit(0)
base = Path(resto[resto.index("--base") + 1])
tmp = Path(tempfile.mkdtemp(prefix="qa_t91_compat_"))
salidas = {}
for nombre, e in (("base", base), ("head", ej)):
    salidas[nombre] = tmp / nombre
    subprocess.run([sys.executable, "-I", str(AQUI), "--ejecutor", str(e), "--trabajador", str(salidas[nombre])], check=True,
                   capture_output=True)
leer = {k: list(csv.reader(open(v / "pronosticos.csv", encoding="utf-8"))) for k, v in salidas.items()}
m = Marcador()
cb, ch = leer["base"][0], leer["head"][0]
m.check("cabecera: la de la base es un prefijo de la nueva", ch[:len(cb)] == cb, f"{len(cb)} → {len(ch)} columnas; nuevas {ch[len(cb):]}")
fb = {r[0]: r for r in leer["base"][1:]}
fh = {r[0]: r[:len(cb)] for r in leer["head"][1:]}
m.check("mismos PRG", set(fb) == set(fh), f"{len(fb)} / {len(fh)}")
distintas = {k: [cb[i] for i in range(len(cb)) if fb[k][i] != fh[k][i]] for k in fb if k in fh and fb[k] != fh[k]}
m.check("mismos valores en las 30 columnas anteriores", not distintas, f"{len(distintas)} filas distintas: {list(distintas.items())[:3]}")
# Lector por nombre de la versión anterior (DictReader con la cabecera de la base)
filas = list(csv.DictReader(open(salidas["head"] / "pronosticos.csv", encoding="utf-8")))
m.check("lector por nombre: las columnas de antes con los mismos valores", all({c: f[c] for c in cb} == dict(zip(cb, fb[f["prg_id"]])) for f in filas))
print(f"   salidas en {tmp}")
sys.exit(m.fin())
