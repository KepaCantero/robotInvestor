"""QA r01 de T-112 · re-ejecución CT-10 (AUD-REX-001): artefactos alterados y clasificación de `coincide` y `categoria`.

Cada caso copia un artefacto servido, lo altera y lo escribe como entrada nueva del RC (el original no se toca), y
comprueba lo que devuelve `Motor.reejecutar`. También: series de HT-01 (huella), semilla de la petición, versión de la
ficha, entradas que no son servicios, un manejador no determinista y que la entrada original no cambia.
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

eje = C.preparar(sys.argv)
from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

K = C.Contador("r01_07 CT-10")
import tempfile  # noqa: E402

prov = ProveedorCSV(eje / "ejemplos" / "datos_sinteticos")
prov.fijar_as_of("2024-06-28")
m = servicio.Motor(Almacen(Path(tempfile.mkdtemp())), prov, cargar_config())


def copia(calc_id, cambio):
    e = copy.deepcopy(m.almacen.estado("RC")[calc_id])
    cambio(e)
    e["calc_id"] = m.almacen.nuevo_id("CALC")
    m.almacen.escribir("RC", "AG-13", e)
    return e["calc_id"]


def rex(calc_id, motivo="QA r01"):
    try:
        out = m.reejecutar(calc_id, motivo)
        return (out["coincide"], out["categoria"]), None
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__}: {str(e)[:150]}"


def servir(f, i=0, **extra):
    c = servicio.CASOS_CONTROL[f][i]
    r = m.servir({"operacion": f, "datos": copy.deepcopy(c.get("datos") or []), "parametros": dict(c.get("parametros") or {}),
                  "fecha_corte": None, **extra}, "AG-18")
    assert r["estado"].startswith("SERVED"), r
    return r["calc_id"]


def primer_float(x, ruta=()):
    if isinstance(x, dict):
        for k, v in x.items():
            h = primer_float(v, ruta + (k,))
            if h:
                return h
    if isinstance(x, list):
        for i, v in enumerate(x):
            h = primer_float(v, ruta + (i,))
            if h:
                return h
    if isinstance(x, float) and x != 0:
        return ruta
    return None


def poner(e, ruta, fn):
    c = e["resultado"]["payload"]
    for k in ruta[:-1]:
        c = c[k]
    c[ruta[-1]] = fn(c[ruta[-1]])


# 1. Fichas de la Fase 2 servidas y re-ejecutadas
for f in ("FIR-PRICE-001", "BT-PBO-001", "ACC-VAL-001", "FX-COINT-001"):
    c = servir(f)
    K.comprobar(f"{f}: re-ejecución del original ⇒ SI", rex(c)[0] == ("SI", None), str(rex(c)))
c = servir("SIM-MC-001", semilla=4242)
orig = copy.deepcopy(m.almacen.estado("RC")[c])
K.comprobar("SIM-MC-001 con la semilla de la petición: SI (la semilla viaja en los parámetros del artefacto)", rex(c)[0] == ("SI", None), str(rex(c)))
K.comprobar("la entrada original del RC no cambia tras la re-ejecución", m.almacen.estado("RC")[c] == orig)

# 2. Serie de HT-01
r = m.servir({"operacion": "FX-STL-001", "datos": [{"serie": "EURUSD=X", "fin": "2024-06-28"}], "parametros": {}, "fecha_corte": "2024-06-28"}, "AG-18")
if K.comprobar("FX-STL-001 sobre una serie de HT-01: servida", r["estado"].startswith("SERVED"), str(r)[:300]):
    c = r["calc_id"]
    K.comprobar("  re-ejecución ⇒ SI", rex(c)[0] == ("SI", None), str(rex(c)))
    c2 = copia(c, lambda e: e["datos"][0].__setitem__("huella", "0" * 16))
    K.comprobar("  huella de la serie alterada ⇒ NO / DATOS_DISTINTOS", rex(c2)[0] == ("NO", "DATOS_DISTINTOS"), str(rex(c2)))
    c3 = copia(c, lambda e: e["datos"][0].__setitem__("fecha_dato", "2024-03-29"))
    K.comprobar("  fecha_dato recortada ⇒ NO / DATOS_DISTINTOS", rex(c3)[0] == ("NO", "DATOS_DISTINTOS"), str(rex(c3)))

# 3. Alteraciones del artefacto en línea
base = servir("FIR-PRICE-001", 1)
tol = servicio.IMPLEMENTADAS["FIR-PRICE-001"]["tol"]
ruta = primer_float(m.almacen.estado("RC")[base]["resultado"]["payload"])
casos = [
    ("cifra × (1 + tol/10) ⇒ DENTRO_TOLERANCIA", lambda e: poner(e, ruta, lambda x: x * (1 + tol / 10)), ("DENTRO_TOLERANCIA", None)),
    ("cifra × (1 + 10·tol) ⇒ NO / ERROR_ORIGINAL", lambda e: poner(e, ruta, lambda x: x * (1 + 10 * tol)), ("NO", "ERROR_ORIGINAL")),
    ("clave eliminada del resultado ⇒ NO", lambda e: e["resultado"]["payload"].pop("ytm_pct"), ("NO", "ERROR_ORIGINAL")),
    ("clave añadida al resultado ⇒ NO", lambda e: e["resultado"]["payload"].__setitem__("extra", 1.0), ("NO", "ERROR_ORIGINAL")),
    ("texto del resultado cambiado ⇒ NO", lambda e: e["resultado"]["payload"].__setitem__("convencion", "30E/360"), ("NO", "ERROR_ORIGINAL")),
    ("cifra cambiada a None ⇒ NO", lambda e: poner(e, ruta, lambda x: None), ("NO", "ERROR_ORIGINAL")),
    ("cifra cambiada a True (1.0 ⇒ bool) ⇒ NO", lambda e: e["resultado"]["payload"].__setitem__("flujos", True), ("NO", "ERROR_ORIGINAL")),
    ("versión de la ficha distinta y cifra distinta ⇒ CONVENCION_DISTINTA",
     lambda e: (e["operacion"].__setitem__("ficha_version", "0.9"), poner(e, ruta, lambda x: x * 1.01)), ("NO", "CONVENCION_DISTINTA")),
    ("valores en línea alterados sin rehacer la huella ⇒ DATOS_DISTINTOS",
     lambda e: e["datos"][0]["valor"].__setitem__("cupon", 5.5), ("NO", "DATOS_DISTINTOS")),
    ("huella en línea alterada ⇒ DATOS_DISTINTOS", lambda e: e["datos"][0].__setitem__("huella", "f" * 16), ("NO", "DATOS_DISTINTOS")),
]
for nombre, cambio, esperado in casos:
    cc = copia(base, cambio)
    got, exc = rex(cc)
    K.comprobar(nombre, got == esperado, f"obtenido {got or exc}")


def rehacer_huella(e):
    e["datos"][0]["valor"]["cupon"] = 5.5
    e["datos"][0]["huella"] = servicio.clave_hash(e["datos"][0]["valor"])[:16]


cc = copia(base, rehacer_huella)
print("   valores alterados con la huella rehecha:", rex(cc))
cc = copia(base, lambda e: e["parametros"].__setitem__("rango_delta_y_pb", [0, 1000]))
got, exc = rex(cc)
print("   parámetros del artefacto con un umbral fijo:", got or exc)
K.comprobar("parámetros del artefacto con un umbral fijo: no se re-ejecuta en silencio con él", got is None or got[0] == "NO",
            f"{got or exc}")
cc = copia(base, lambda e: e["datos"][0].__setitem__("valor", "en línea"))
got, exc = rex(cc)
K.comprobar("artefacto anterior a T-112 («en línea»): imposible", exc is not None and "imposible" in exc, f"{got or exc}")
cc = copia(base, lambda e: e["operacion"].__setitem__("ficha_id", "NO-EXISTE-001"))
K.comprobar("ficha sin manejador: imposible", rex(cc)[1] is not None)
for motivo in (None, "", "   ", 7, ["x"]):
    K.comprobar(f"motivo {motivo!r}: imposible", rex(base, motivo)[1] is not None)
rech = m.servir({"operacion": "FIR-PRICE-001", "datos": [{"valores": {"cupon": 1}}], "parametros": {}}, "AG-18")["calc_id"]
K.comprobar("un rechazo no se re-ejecuta", rex(rech)[1] is not None)
c1 = servir("FIR-PRICE-001", 1)
hit = m.servir({"operacion": "FIR-PRICE-001", "datos": copy.deepcopy(servicio.CASOS_CONTROL["FIR-PRICE-001"][1]["datos"]),
                "parametros": dict(servicio.CASOS_CONTROL["FIR-PRICE-001"][1].get("parametros") or {}), "fecha_corte": None}, "AG-18")
K.comprobar("un acierto de caché no es un servicio re-ejecutable", hit.get("cache_hit") and rex(hit["calc_id_cache"])[1] is not None,
            str(rex(hit.get("calc_id_cache", "x"))))

# 4. Manejador no determinista (solo en memoria del proceso)
import random  # noqa: E402

fn0 = servicio.IMPLEMENTADAS["FIR-PRICE-001"]["fn"]


def ruidoso(ent, params):
    r_, lim = fn0(ent, params)
    return {**r_, "ruido": random.random()}, lim


servicio.IMPLEMENTADAS["FIR-PRICE-001"]["fn"] = ruidoso
try:
    got, exc = rex(base)
finally:
    servicio.IMPLEMENTADAS["FIR-PRICE-001"]["fn"] = fn0
K.comprobar("manejador no determinista ⇒ NO / NO_DETERMINISMO", got == ("NO", "NO_DETERMINISMO"), str(got or exc))

# 5. Casos de control de AUD-REX-001 desde verificar_casos_control
v = m.verificar_casos_control(["AUD-REX-001"])
K.comprobar("verificar_casos_control(AUD-REX-001): superados y registrados", v["AUD-REX-001"].get("superados") is True,
            str(v)[:300])
sys.exit(K.fin())
