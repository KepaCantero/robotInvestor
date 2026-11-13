"""QA r01 de T-93 (revisor independiente): plazos de CT-23 tras la corrección de H-37 (tipos no texto) y H-38 (plazos guardados
que ya no se leen).

Uso: python -I r01_03_plazos_tipos.py <ruta a bloque_a/11_Ejecutor>
Imprime OK/FALLO por caso (INFO no cuenta) y el número de fallos.
"""
import datetime as dt
import decimal
import fractions
import sys
import tempfile
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
sys.path.insert(0, str(EJ / "tests"))
import bloque_a  # noqa: E402

assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from conftest import nuevo_bloque  # noqa: E402

fallos = 0


def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))


def info(nombre, detalle=""):
    print("INFO  " + nombre + (f" — {detalle}" if detalle else ""))


universo = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
CONSULTA = {"tipo": "OTRA", "modo": "BLOQUEANTE", "clases": ["RV"], "preguntas": [{"texto": "¿RV?", "supuesto_declarado": "esperar"}]}


def enviar(plazo, envio="2026-06-05"):
    with tempfile.TemporaryDirectory() as d:
        b = nuevo_bloque(d, universo)
        try:
            return b.consultas.enviar({**CONSULTA, "plazo_respuesta": plazo}, envio)["plazo_respuesta"]
        except Exception as x:
            return f"{type(x).__name__}"


# ------------------------------------------------------------------------------------------------------------------ 1
print("--- 1. Tipos numéricos y raros como plazo: se rechazan (ValueError), nunca se leen como 1970")
for plazo in [0, 1, -1, 20260608, 2026.5, float("nan"), float("inf"), True, False, np.int64(20260608), np.float64(20260608),
              np.bool_(True), decimal.Decimal("20260608"), fractions.Fraction(20260608, 1), complex(1, 0)]:
    r = enviar(plazo)
    informe(f"1  {type(plazo).__name__} {plazo!r}", r in ("ValueError", "TypeError") and not r.startswith("1970"), r)

# ------------------------------------------------------------------------------------------------------------------ 2
print("--- 2. Formas de fecha sin hora: ¿vencen al terminar el día, como su texto?")
texto = enviar("2026-06-08")
for plazo in [dt.date(2026, 6, 8), np.datetime64("2026-06-08"), pd.Timestamp("2026-06-08"), pd.Period("2026-06-08", "D"),
              dt.datetime(2026, 6, 8)]:
    r = enviar(plazo)
    if isinstance(plazo, dt.date) and not isinstance(plazo, dt.datetime):
        informe(f"2  {type(plazo).__name__}: {r} (texto: {texto})", r == texto)
    else:
        info(f"2  {type(plazo).__name__}: {r} (texto: {texto})")
info("2  «» y None usan el plazo del modo", f"{enviar('')} / {enviar(None)}")
info("2  «   » (solo espacios)", enviar("   "))

# ------------------------------------------------------------------------------------------------------------------ 3
print("--- 3. vencer() con plazos guardados que no se leen: vence con una incidencia y no lanza")


def guardada_con(plazo, quitar=False):
    d = tempfile.mkdtemp()
    b = nuevo_bloque(d, universo)
    c = b.consultas.enviar(dict(CONSULTA), "2026-06-05")
    g = {k: v for k, v in b.almacen.estado("F5", clave="cns_id")[c["cns_id"]].items() if not k.startswith("_")}
    if quitar:
        g.pop("plazo_respuesta")
        # la vista consolidada conserva el campo de la entrada anterior: se reescribe el fichero sin él, como un estado antiguo
    g["plazo_respuesta"] = plazo
    b.almacen.escribir("F5", "AG-01", g)
    return b, c["cns_id"]


for plazo in ["2026-6-8", 20260608, 2026.5, True, None, {"fecha": "2026-06-08"}, ["2026-06-08"], "", "nan"]:
    b, k = guardada_con(plazo)
    try:
        v = b.consultas.vencer("2026-06-06T09:00")
        incid = [e for e in b.almacen.leer("HA") if k in str(e.get("detalle"))]
        informe(f"3  plazo guardado {plazo!r}: vence con incidencia", v == [k] and len(incid) == 1, f"{v}, {len(incid)} incidencia(s)")
        v2 = b.consultas.vencer("2026-06-06T10:00")
        incid2 = [e for e in b.almacen.leer("HA") if k in str(e.get("detalle"))]
        informe(f"3  plazo guardado {plazo!r}: un segundo vencer() no repite nada", v2 == [] and len(incid2) == 1,
                f"{v2}, {len(incid2)}")
        informe(f"3  plazo guardado {plazo!r}: la clase deja de estar pausada",
                not b.consultas.clases_pausadas("2026-06-06", ["RV"]))
    except Exception as x:
        informe(f"3  plazo guardado {plazo!r}: vence con incidencia", False, f"lanza {type(x).__name__}: {x}")

# Un CNS ENVIADA sin el campo (estado antiguo o manipulado): se escribe directamente sin `plazo_respuesta`
d = tempfile.mkdtemp()
b = nuevo_bloque(d, universo)
b.fijar_fecha(dt.date(2026, 6, 5))   # la entrada tiene que existir en la fecha de corte de vencer()
b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CNS", "id": "CNS-2026-9999", "cns_id": "CNS-2026-9999", "sentido": "SALIENTE",
                                   "estado": "ENVIADA", "modo": "BLOQUEANTE", "clases": ["RV"],
                                   "preguntas": [{"texto": "¿RV?", "supuesto_declarado": "esperar"}]})
try:
    v = b.consultas.vencer("2026-06-06T09:00")
    informe("3b CNS ENVIADA sin «plazo_respuesta»: vence con incidencia y no lanza", v == ["CNS-2026-9999"], str(v))
except Exception as x:
    informe("3b CNS ENVIADA sin «plazo_respuesta»: vence con incidencia y no lanza", False, f"lanza {type(x).__name__}: {x}")

# ------------------------------------------------------------------------------------------------------------------ 4
print("--- 4. Bordes del día para un `date` (Madrid, cambio de hora del 29-3 y del 25-10)")
for dia, dentro, fuera in [(dt.date(2026, 3, 29), "2026-03-29T21:59:59.999Z", "2026-03-29T22:00Z"),
                           (dt.date(2026, 10, 25), "2026-10-25T22:59:59.999Z", "2026-10-25T23:00Z")]:
    with tempfile.TemporaryDirectory() as d:
        b = nuevo_bloque(d, universo)
        c = b.consultas.enviar({**CONSULTA, "plazo_respuesta": dia}, "2026-03-02")
        informe(f"4  {dia}: no vence en {dentro} y vence en {fuera}",
                not b.consultas.vencer(dentro) and b.consultas.vencer(fuera) == [c["cns_id"]], c["plazo_respuesta"])

# ------------------------------------------------------------------------------------------------------------------ 5
print("--- 5. vencer() y enviar() con un instante numérico (CLI): se rechaza, no es 1970")
with tempfile.TemporaryDirectory() as d:
    b = nuevo_bloque(d, universo)
    for f, arg in [("vencer", 20260606), ("enviar", 20260606)]:
        try:
            r = b.consultas.vencer(arg) if f == "vencer" else b.consultas.enviar(dict(CONSULTA), arg)
            informe(f"5  {f}({arg})", False, f"acepta: {r}")
        except ValueError as x:
            informe(f"5  {f}({arg}) se rechaza", True, str(x)[:60])

print(f"fallos: {fallos}")
sys.exit(1 if fallos else 0)
