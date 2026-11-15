"""QA r01 de T-141: `descargar_datos_bce.py` frente a respuestas raras del servicio (sin red: se sustituye `urlopen`).
Para cada caso: ¿termina con error claro (falla cerrado) o escribe CSV? ¿deja la carpeta a medias?

Uso (desde la raíz): <python> -I .docs/tickets/T-141/revisores/r03_respuestas_raras.py <carpeta_temporal>"""
import importlib.util
import io
import shutil
import sys
import urllib.error
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("bce", RAIZ / ".docs" / "scripts" / "descargar_datos_bce.py")
bce = importlib.util.module_from_spec(spec); spec.loader.exec_module(bce)
W = Path(sys.argv[1])
CAB = "KEY,FREQ,CURRENCY,CURRENCY_DENOM,EXR_TYPE,EXR_SUFFIX,TIME_PERIOD,OBS_VALUE,OBS_STATUS\n"


def fila(m, d, v):
    return f"EXR.D.{m}.EUR.SP00.A,D,{m},EUR,SP00,A,{d},{v},A\n"


def normal(dias=("2026-11-12", "2026-11-13"), quitar=(), valores=None):
    v = valores or {"USD": 1.1, "JPY": 170.0, "GBP": 0.85, "AUD": 1.7, "CHF": 0.93, "MXN": 20.5}
    return CAB + "".join(fila(m, d, v[m]) for d in dias for m in bce.MONEDAS if m not in quitar)


class Resp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False


casos = {
    "normal": normal(),
    "vacía (solo cabecera)": CAB,
    "cuerpo vacío": "",
    "falta MXN entera": normal(quitar=("MXN",)),
    "fila duplicada con otro valor": normal() + fila("USD", "2026-11-13", 9.99),
    "OBS_VALUE NaN en USD": normal(valores={"USD": "NaN", "JPY": 170.0, "GBP": 0.85, "AUD": 1.7, "CHF": 0.93, "MXN": 20.5}),
    "OBS_VALUE negativo en JPY": normal(valores={"USD": 1.1, "JPY": -170.0, "GBP": 0.85, "AUD": 1.7, "CHF": 0.93, "MXN": 20.5}),
    "HTML de error con 200": "<html><body>Service unavailable</body></html>",
    "HTTP 404": urllib.error.HTTPError("u", 404, "No Results Found", {}, io.BytesIO(b"")),
}
for nombre, cuerpo in casos.items():
    d = W / nombre.replace(" ", "_")
    shutil.rmtree(d, ignore_errors=True)
    def falso(url, timeout=None, _c=cuerpo):
        if isinstance(_c, Exception):
            raise _c
        return Resp(_c.encode())
    bce.urllib.request.urlopen = falso
    try:
        codigo = bce.main([str(d)])
        res = f"código {codigo}"
    except SystemExit as e:
        res = f"SystemExit {e.code}"
    except Exception as e:   # noqa: BLE001
        res = f"excepción {type(e).__name__}: {str(e)[:60]}"
    escritos = sorted(p.name for p in d.glob("*.csv")) if d.exists() else []
    extra = ""
    if "duplicada" in nombre and escritos:
        extra = " · EURUSD 13-11 = " + (d / "EURUSD=X.csv").read_text().splitlines()[-1]
    if "NaN" in nombre or "negativo" in nombre:
        extra = " · filas por símbolo: " + ", ".join(f"{p.stem}={len(p.read_text().splitlines()) - 1}" for p in sorted(d.glob('*.csv')))
    print(f"{nombre:32} → {res:55} · {len(escritos)} CSV escritos{extra}")
