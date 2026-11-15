"""QA r01 de T-147 (revisor) · respuestas raras del BCE que no prueba `T-141/revisores/r03_respuestas_raras.py` y
`--clases` de `comprobar_datos_a.py`. Sin red: `urllib.request.urlopen` se sustituye por una respuesta fija.

Uso, desde la raíz de la copia:  .venv/bin/python -I .docs/tickets/T-147/revisores/r01_02_bce_y_clases.py <carpeta de trabajo>
Esperado en cada respuesta rara: código 1, un mensaje y ningún CSV (ni traza). Termina con 1 si algún caso no lo cumple."""
import contextlib
import importlib.util
import io
import subprocess
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
SCRIPTS = RAIZ / ".docs" / "scripts"
TRABAJO = Path(sys.argv[1]).resolve()
TRABAJO.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location("descargar_datos_bce", SCRIPTS / "descargar_datos_bce.py")
bce = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bce)

MON = ("USD", "JPY", "GBP", "AUD", "CHF", "MXN")
VAL = {"USD": 1.08, "JPY": 160.1, "GBP": 0.85, "AUD": 1.65, "CHF": 0.95, "MXN": 18.5}


def csv(filas):
    return ("KEY,FREQ,CURRENCY,CURRENCY_DENOM,EXR_TYPE,EXR_SUFFIX,TIME_PERIOD,OBS_VALUE\n"
            + "".join(f"EXR.D.{m}.EUR.SP00.A,D,{m},EUR,SP00,A,{f},{v}\n" for m, f, v in filas)).encode()


def normal(fechas=("2026-11-12", "2026-11-13")):
    return [(m, f, VAL[m]) for f in fechas for m in MON]


class Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


CASOS = {
    "fecha repetida escrita de otra forma (2026-11-13 y 2026-11-13T00:00)": normal() + [("USD", "2026-11-13T00:00", 1.09)],
    "fecha repetida sin ceros (2026-11-3 y 2026-11-03)": normal(("2026-11-03", "2026-11-04")) + [("USD", "2026-11-3", 1.09)],
    "CURRENCY vacía": normal() + [("", "2026-11-14", 1.0)],
    "una moneda ajena al universo (SEK) además de las seis": normal() + [("SEK", "2026-11-13", 11.5)],
    "OBS_VALUE con coma decimal": [(m, f, f'"{str(VAL[m]).replace(".", ",")}"') for m, f, _ in normal()],
    "solo fechas de fin de semana futuras": normal(("2099-01-03", "2099-01-04")),
}


def ejecuta(cuerpo, destino):
    original = urllib.request.urlopen
    urllib.request.urlopen = lambda *a, **k: Resp(cuerpo)
    err = io.StringIO()
    try:
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            codigo = bce.main([str(destino)])
        traza = None
    except BaseException as e:   # noqa: BLE001 · una traza es justo lo que se busca
        codigo, traza = None, f"{type(e).__name__}: {str(e)[:90]}"
    finally:
        urllib.request.urlopen = original
    return codigo, traza, sorted(p.name for p in destino.glob("*.csv")) if destino.exists() else [], err.getvalue().strip()


fallos = 0
for i, (nombre, filas) in enumerate(CASOS.items()):
    destino = TRABAJO / f"bce_{i}"
    codigo, traza, csvs, err = ejecuta(csv(filas), destino)
    ok = codigo == 1 and not csvs and traza is None
    # una moneda de más no estorba (se ignora); el resto debería fallar cerrado
    if nombre.startswith("una moneda ajena"):
        ok = codigo == 0 and len(csvs) == 6 and traza is None
    obs = nombre.startswith(("solo fechas", "CURRENCY vacía"))   # observaciones: el BCE real no lo manda; no cuentan
    if obs:
        ok = traza is None
    fallos += not ok
    etiqueta = "OBS     " if obs and ok else ("OK      " if ok else "HALLAZGO")
    print(f"{etiqueta} {nombre:70} código {codigo} · {len(csvs)} CSV"
          + (f" · traza {traza}" if traza else "") + (f" · {err[:90]}" if err and not ok else ""))

# destino que es un fichero (no una carpeta)
f = TRABAJO / "soy_un_fichero"
f.write_text("x", encoding="utf-8")
codigo, traza, _, err = ejecuta(csv(normal()), f)
ok = codigo in (1, 2) and traza is None
fallos += not ok
print(f"{'OK      ' if ok else 'HALLAZGO'} {'destino que es un fichero':70} código {codigo}" + (f" · traza {traza}" if traza else ""))

# --clases de comprobar_datos_a.py
CD = [sys.executable, str(SCRIPTS / "comprobar_datos_a.py"), str(TRABAJO / "bce_3")]
for args, esperado in ((["--clases", "XXX"], 2), (["--clases", "div"], 2), (["--clases"], 2), (["--clases", "DIV", "DIV"], None),
                       (["--clases", "RV", "XXX"], 2), (["--clases", "DIV", "--as-of", "2026-11-13"], None)):
    r = subprocess.run(CD + args, capture_output=True, text=True, check=False)
    ok = (r.returncode == esperado) if esperado is not None else r.returncode in (0, 1) and "Traceback" not in r.stderr
    fallos += not ok
    print(f"{'OK      ' if ok else 'HALLAZGO'} comprobar_datos_a {' '.join(args):46} código {r.returncode}"
          + ("" if ok else f" · {r.stderr.strip()[-120:]}"))

print(f"\n{fallos} hallazgos")
sys.exit(1 if fallos else 0)
