"""QA r01 de T-149 (revisor) · `.docs/scripts/descargar_datos_bce.py` sin trazas (T-147 H-02), sin red.

Uso, desde la raíz de la copia:  .venv/bin/python -I .docs/tickets/T-149/revisores/r01_04_bce_qa.py <carpeta temporal>
La descarga se sustituye por un doble de `urllib.request.urlopen` (y, donde hace falta, de `os.replace`,
`tempfile.mkdtemp` o la lectura de la respuesta). Para cada caso se espera: código 1, un mensaje sin traza y nada
escrito (salvo los límites declarados, que se imprimen como OBS); y para los válidos, código 0 y los seis CSV.
Termina con 1 si hay algún hallazgo."""
import contextlib
import http.client
import importlib.util
import io
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
TMP = Path(sys.argv[1]).resolve()
TMP.mkdir(parents=True, exist_ok=True)
CAB = "KEY,FREQ,CURRENCY,CURRENCY_DENOM,EXR_TYPE,EXR_SUFFIX,TIME_PERIOD,OBS_VALUE,OBS_STATUS\n"
VAL = {"USD": 1.1, "JPY": 170.0, "GBP": 0.85, "AUD": 1.7, "CHF": 0.93, "MXN": 20.5}
hallazgos = 0


def fila(m, d, v):
    return f"EXR.D.{m}.EUR.SP00.A,D,{m},EUR,SP00,A,{d},{v},A\n"


def cuerpo(extra="", fechas=("2026-11-03", "2026-11-04")):
    return CAB + "".join(fila(m, d, v) for d in fechas for m, v in VAL.items()) + extra


def modulo():
    spec = importlib.util.spec_from_file_location("bce_qa", RAIZ / ".docs" / "scripts" / "descargar_datos_bce.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Respuesta(io.BytesIO):
    def __init__(self, datos, fallo=None):
        super().__init__(datos)
        self.fallo = fallo

    def read(self, *a):
        if self.fallo:
            raise self.fallo
        return super().read(*a)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def ejecutar(destino, texto=None, fallo=None, parche=None):
    mod = modulo()
    llamadas = []

    def urlopen(url, timeout=None):
        llamadas.append(url)
        return Respuesta((texto if texto is not None else cuerpo()).encode(), fallo)
    mod.urllib.request.urlopen = urlopen
    if parche:
        parche(mod)
    err, out = io.StringIO(), io.StringIO()
    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
        try:
            codigo = mod.main([str(destino)])
        except BaseException as e:   # noqa: BLE001
            codigo = f"traza {type(e).__name__}"
    return codigo, err.getvalue(), llamadas


def contenido(d):
    return sorted(p.name for p in d.iterdir()) if d.is_dir() else []


def caso(nombre, ok, detalle="", obs=False):
    global hallazgos
    hallazgos += (not ok) and not obs
    print(f"{'OK      ' if ok else ('OBS     ' if obs else 'HALLAZGO')} {nombre}" + (f" · {detalle}" if detalle else ""), flush=True)


n = 0


def nuevo():
    global n
    n += 1
    return TMP / f"c{n:02d}"


# ---------------------------------------------------------------- respuestas raras: 1, mensaje, nada escrito
RARAS = {
    "fecha con espacio detrás": cuerpo(extra=fila("USD", "2026-11-05 ", 1.2)),
    "fecha con hora": cuerpo(extra=fila("USD", "2026-11-05T00:00", 1.2)),
    "fecha vacía (una fila de USD sin TIME_PERIOD)": cuerpo(extra=fila("USD", "", 1.2)),
    "mes de tres cifras («2026-011-03») repetida": cuerpo(extra=fila("USD", "2026-011-03", 1.2)),
    "repetida «2026-11-03» y «2026-11-3» en JPY": cuerpo(extra=fila("JPY", "2026-11-3", 171.0)),
    "repetida con valor vacío": cuerpo(extra=fila("USD", "2026-11-04", "")),
    "repetida «2026-1-3» y «2026-01-03»": cuerpo(fechas=("2026-01-03", "2026-01-04"), extra=fila("GBP", "2026-1-3", 0.9)),
    "fechas numéricas de 8 cifras": cuerpo(fechas=("20261103", "20261104")),
    "fecha imposible (2026-02-30)": cuerpo(extra=fila("USD", "2026-02-30", 1.2)),
}
for nombre, texto in RARAS.items():
    d = nuevo()
    d.mkdir()
    codigo, err, _ = ejecutar(d, texto)
    caso(f"BCE {nombre}: 1, mensaje y nada escrito", codigo == 1 and "no se escribe nada" in err and not contenido(d),
         f"código {codigo}; {err.strip()[:90]}")

# fallos de la transferencia que no son OSError (la respuesta cortada a medias)
for nombre, fallo in (("lectura cortada (IncompleteRead)", http.client.IncompleteRead(b"KEY,FR")),
                      ("conexión cerrada sin respuesta (RemoteDisconnected)", http.client.RemoteDisconnected("cerrada")),
                      ("tiempo agotado al leer", TimeoutError("lectura")),):
    d = nuevo()
    codigo, err, _ = ejecutar(d, fallo=fallo)
    caso(f"BCE {nombre}: 1, mensaje y nada escrito", codigo == 1 and not contenido(d), f"código {codigo}; {err.strip()[:80]}",
         obs="IncompleteRead" in nombre)   # fuera de T-149 (no es una de las dos trazas de T-147 H-02): se informa

# ---------------------------------------------------------------- destinos
f = TMP / "fichero.txt"
f.write_text("no tocar", encoding="utf-8")
for nombre, destino in (("un fichero", f), ("dentro de un fichero", f / "a" / "b")):
    codigo, err, llamadas = ejecutar(destino)
    caso(f"destino {nombre}: 1 sin descargar", codigo == 1 and not llamadas and f.read_text(encoding="utf-8") == "no tocar",
         f"código {codigo}, descargas {len(llamadas)}")
roto = TMP / "enlace_roto"
if not roto.is_symlink():
    roto.symlink_to(TMP / "no_existe_nunca")
codigo, err, llamadas = ejecutar(roto)
caso("destino enlace simbólico roto: 1 sin traza (se mira antes de descargar)", codigo == 1 and not llamadas,
     f"código {codigo}, descargas {len(llamadas)}; {err.strip()[:80]}", obs=codigo == 1)
d = nuevo()
d.mkdir()
(d / "GBPUSD=X.csv").symlink_to(TMP / "no_existe_tampoco")
codigo, err, _ = ejecutar(d)
caso("un CSV de destino que es un enlace roto: se sustituye por el CSV", codigo == 0 and (d / "GBPUSD=X.csv").is_file()
     and not (d / "GBPUSD=X.csv").is_symlink(), f"código {codigo}")
d = nuevo()
(d / "AUDUSD=X.csv").mkdir(parents=True)
codigo, err, llamadas = ejecutar(d)
caso("un CSV de destino que es una carpeta: 1 sin descargar", codigo == 1 and not llamadas and contenido(d) == ["AUDUSD=X.csv"],
     f"código {codigo}")

# ---------------------------------------------------------------- fallos al escribir
d = nuevo()


def sin_permiso(mod):
    def mkdtemp(*a, **k):
        raise PermissionError(13, "Permiso denegado")
    mod.tempfile.mkdtemp = mkdtemp


mkdtemp_real = __import__("tempfile").mkdtemp
try:
    codigo, err, _ = ejecutar(d, parche=sin_permiso)
finally:
    __import__("tempfile").mkdtemp = mkdtemp_real   # el módulo es el mismo para todos: se restaura
caso("sin permiso para la carpeta temporal: 1, mensaje", codigo == 1 and "no se escribe nada" in err and not contenido(d),
     f"código {codigo}; contenido {contenido(d)}")
d = nuevo()
reales = os.replace
cuenta = {"n": 0}


def falla_al_tercero(mod):
    def replace(a, b):
        cuenta["n"] += 1
        if cuenta["n"] == 3:
            raise OSError(5, "Error de E/S")
        return reales(a, b)
    mod.os.replace = replace


try:
    codigo, err, _ = ejecutar(d, parche=falla_al_tercero)
finally:
    os.replace = reales
quedan = [p for p in contenido(d) if p.endswith(".csv")]
temporales = [p for p in contenido(d) if p.startswith(".bce_")]
caso("os.replace falla en el tercer CSV: 1, mensaje y sin carpeta temporal", codigo == 1 and not temporales, f"código {codigo}")
caso("os.replace falla en el tercer CSV: nada a medias", not quedan,
     f"quedan {quedan} y el mensaje dice «{err.strip()[-22:]}» (límite declarado en analisis-tecnico.md)", obs=True)

# ---------------------------------------------------------------- válidos e idempotencia
d = nuevo()
c1, _, _ = ejecutar(d)
antes = {p: (d / p).read_text(encoding="utf-8") for p in contenido(d)}
c2, _, _ = ejecutar(d)
despues = {p: (d / p).read_text(encoding="utf-8") for p in contenido(d)}
caso("respuesta válida dos veces: 0, seis CSV, los mismos", c1 == 0 and c2 == 0 and len(antes) == 6 and antes == despues,
     f"códigos {c1}, {c2}; {len(antes)} CSV")
d = nuevo()
codigo, _, _ = ejecutar(d, cuerpo(fechas=("2026-11-3", "2026-11-4")))
caso("fechas sin ceros, sin repetir: 0 y fechas AAAA-MM-DD", codigo == 0
     and (d / "EURUSD=X.csv").read_text(encoding="utf-8").splitlines()[1].startswith("2026-11-03,"), f"código {codigo}")

print(f"\n{hallazgos} hallazgos")
sys.exit(1 if hallazgos else 0)
