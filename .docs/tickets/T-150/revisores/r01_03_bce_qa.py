"""QA r01 de T-150 (revisor) · descarga del BCE (H-06, O-05) con dobles, sin red.

Uso, desde la raíz de la copia:  .venv/bin/python -I .docs/tickets/T-150/revisores/r01_03_bce_qa.py <carpeta temporal>
Partes:
  V. `TIME_PERIOD` vacío o nulo de varias formas y en varias posiciones (primera fila, última, solo una moneda, todas);
  L. lecturas cortadas y demás errores de `http.client` en `urlopen` y en `read`;
  M. el traslado a medias en cada CSV (1.º a 6.º): el mensaje nombra exactamente los escritos, los demás CSV del destino
     no cambian y la carpeta temporal no queda;
  E. enlaces simbólicos: destino roto, una carpeta de la ruta rota, un bucle, un enlace a un fichero y uno válido a una
     carpeta (este sí escribe).
Termina con 1 si hay algún hallazgo."""
import contextlib
import http.client
import importlib.util
import io
import os
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
TMP = Path(sys.argv[1]).resolve()
TMP.mkdir(parents=True, exist_ok=True)
CAB = "KEY,FREQ,CURRENCY,CURRENCY_DENOM,EXR_TYPE,EXR_SUFFIX,TIME_PERIOD,OBS_VALUE,OBS_STATUS\n"
VAL = {"USD": 1.1, "JPY": 170.0, "GBP": 0.85, "AUD": 1.7, "CHF": 0.93, "MXN": 20.5}
hallazgos = 0


def caso(nombre, ok, detalle="", obs=False):
    global hallazgos
    hallazgos += (not ok) and not obs
    print(f"{'OK      ' if ok else ('OBS     ' if obs else 'HALLAZGO')} {nombre}" + (f" · {detalle}" if detalle else ""), flush=True)


def fila(m, d, v):
    return f"EXR.D.{m}.EUR.SP00.A,D,{m},EUR,SP00,A,{d},{v},A\n"


def cuerpo(fechas=("2026-11-03", "2026-11-04"), extra="", antes=""):
    return CAB + antes + "".join(fila(m, d, v) for d in fechas for m, v in VAL.items()) + extra


def modulo():
    spec = importlib.util.spec_from_file_location("bce_qa150", RAIZ / ".docs" / "scripts" / "descargar_datos_bce.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def con_respuesta(m, texto=None, fallo_abrir=None, fallo_leer=None):
    llamadas = []

    class R(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self, *a):
            if fallo_leer is not None:
                raise fallo_leer
            return super().read(*a)

    def falso(url, timeout=None):
        llamadas.append(url)
        if fallo_abrir is not None:
            raise fallo_abrir
        return R((texto or "").encode())
    m.urllib.request.urlopen = falso
    return llamadas


def correr(m, destino):
    err = io.StringIO()
    out = io.StringIO()
    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
        try:
            codigo = m.main([str(destino)])
        except BaseException as e:   # noqa: BLE001
            codigo = f"traza {type(e).__name__}"
    return codigo, err.getvalue()


def nuevo(nombre):
    d = TMP / nombre
    shutil.rmtree(d, ignore_errors=True)
    if d.is_symlink():
        d.unlink()
    return d


# ---------------------------------------------------------------- V. TIME_PERIOD vacío
VACIAS = {
    "vacío en la primera fila": cuerpo(antes=fila("USD", "", 1.2)),
    "vacío en la última fila": cuerpo(extra=fila("MXN", "", 20.1)),
    "vacío con el valor vacío": cuerpo(extra=fila("GBP", "", "")),
    "entre comillas vacías": cuerpo(extra=fila("CHF", '""', 0.9)),
    "«NaT» literal": cuerpo(extra=fila("AUD", "NaT", 1.6)),
    "«nan» literal": cuerpo(extra=fila("AUD", "nan", 1.6)),
    "«None» literal": cuerpo(extra=fila("JPY", "None", 171.0)),
    "solo espacios": cuerpo(extra=fila("USD", "   ", 1.2)),
    "todas las fechas vacías": cuerpo(fechas=("", "")),
}
for nombre, texto in VACIAS.items():
    m = modulo()
    con_respuesta(m, texto)
    d = nuevo("v")
    codigo, err = correr(m, d)
    escrito = d.exists() and any(d.iterdir())
    caso(f"V TIME_PERIOD {nombre}: 1, mensaje y nada escrito", codigo == 1 and "no se escribe nada" in err and not escrito,
         f"código {codigo}: {err.strip()[:90]!r}")

# ---------------------------------------------------------------- L. errores de http.client
FALLOS = {
    "IncompleteRead al leer": (None, http.client.IncompleteRead(b"KEY,FREQ,CUR", 100)),
    "IncompleteRead al abrir": (http.client.IncompleteRead(b""), None),
    "BadStatusLine": (http.client.BadStatusLine("HTTP/9"), None),
    "LineTooLong": (http.client.LineTooLong("header line"), None),
    "RemoteDisconnected al leer": (None, http.client.RemoteDisconnected("cerrada")),
    "InvalidURL": (http.client.InvalidURL("url"), None),
    "ResponseNotReady": (None, http.client.ResponseNotReady("x")),
    "ConnectionResetError al leer": (None, ConnectionResetError(104, "reset")),
}
for nombre, (fa, fl) in FALLOS.items():
    m = modulo()
    con_respuesta(m, cuerpo(), fallo_abrir=fa, fallo_leer=fl)
    d = nuevo("l")
    codigo, err = correr(m, d)
    caso(f"L {nombre}: 1, mensaje y nada escrito", codigo == 1 and "no se escribe nada" in err and not d.exists()
         and "Traceback" not in err, f"código {codigo}: {err.strip()[:90]!r}")

# ---------------------------------------------------------------- M. traslado a medias
m0 = modulo()
SIMBOLOS = list(m0.CRUCES)
for falla_en in range(1, len(SIMBOLOS) + 1):
    m = modulo()
    con_respuesta(m, cuerpo())
    d = nuevo("m")
    d.mkdir()
    for s in SIMBOLOS:                     # CSV de una descarga anterior
        (d / f"{s}.csv").write_text("viejo\n", encoding="utf-8")
    reales = m.os.replace
    cuenta = {"n": 0}

    def replace(a, b, _r=reales, _c=cuenta, _f=falla_en):
        _c["n"] += 1
        if _c["n"] == _f:
            raise OSError(28, "No queda espacio en el dispositivo")
        return _r(a, b)
    m.os.replace = replace
    try:
        codigo, err = correr(m, d)
    finally:
        m.os.replace = reales
    nuevos = [f"{s}.csv" for s in SIMBOLOS if (d / f"{s}.csv").read_text(encoding="utf-8") != "viejo\n"]
    esperados = [f"{s}.csv" for s in SIMBOLOS[:falla_en - 1]]
    restos = [p.name for p in d.iterdir() if p.name.startswith(".bce_")]
    nombrados = [s for s in (f"{x}.csv" for x in SIMBOLOS) if s in err]
    if falla_en == 1:
        ok = codigo == 1 and not nuevos and "no se escribe nada" in err and not restos
    else:
        ok = (codigo == 1 and nuevos == esperados and nombrados == esperados and "no se escribe nada" not in err
              and not restos and "Repite la descarga" in err)
    caso(f"M os.replace falla en el CSV {falla_en}: código 1, el mensaje nombra los escritos ({len(esperados)}) y nada más cambia",
         ok, f"código {codigo}, nuevos {nuevos}, nombrados {nombrados}, restos {restos}")

# ---------------------------------------------------------------- E. enlaces simbólicos
ENLACES = {}
roto = nuevo("e_roto")
roto.symlink_to(TMP / "no_existe_1")
ENLACES["destino roto"] = (roto, False)
roto2 = nuevo("e_roto2")
roto2.symlink_to(TMP / "no_existe_2")
ENLACES["carpeta de la ruta rota (dos niveles)"] = (roto2 / "a" / "b", False)
b1, b2 = nuevo("e_bucle1"), nuevo("e_bucle2")
b1.symlink_to(b2)
b2.symlink_to(b1)
ENLACES["bucle de enlaces"] = (b1, False)
fich = TMP / "e_fichero.txt"
fich.write_text("x", encoding="utf-8")
af = nuevo("e_a_fichero")
af.symlink_to(fich)
ENLACES["enlace a un fichero"] = (af, False)
real = nuevo("e_real")
real.mkdir()
av = nuevo("e_valido")
av.symlink_to(real)
ENLACES["enlace válido a una carpeta"] = (av, True)
for nombre, (destino, escribe) in ENLACES.items():
    m = modulo()
    llamadas = con_respuesta(m, cuerpo())
    codigo, err = correr(m, destino)
    if escribe:
        ok = codigo == 0 and len(list(real.glob("*.csv"))) == len(SIMBOLOS)
    else:
        ok = codigo == 1 and not llamadas and "no se descarga" in err and not (TMP / "no_existe_1").exists() \
            and not (TMP / "no_existe_2").exists()
    caso(f"E {nombre}: {'escribe los seis' if escribe else '1 sin descargar ni crear nada'}", ok,
         f"código {codigo}, descargas {len(llamadas)}: {err.strip()[:90]!r}")

print(f"\n{hallazgos} hallazgos")
sys.exit(1 if hallazgos else 0)
