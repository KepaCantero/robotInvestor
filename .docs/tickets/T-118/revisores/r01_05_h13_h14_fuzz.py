"""QA r01 de T-118 · H-13 y H-14: fuzzing de la petición entera y de los artefactos que se re-ejecutan.

 1. `Motor.servir`: cada campo de la petición (y los argumentos `solicitante`, `run_id`, `msg_id`; la petición entera; los
    elementos y las claves de `datos`) con ~45 valores raros, en 4 fichas. Nada escapa y cada llamada deja UNA entrada en
    RC; al final el RC se puede volver a abrir y su cadena de hash es íntegra.
 2. Anidamiento: listas y objetos a 1…40, 500 y 3 000 niveles en cada sitio; el borde exacto (PROFUNDIDAD_MAXIMA); la
    profundidad de las peticiones legítimas (casos de control) y de lo que el ciclo simulado pide al Motor.
 3. `Motor.reejecutar`: artefactos con cada campo alterado. Solo pueden salir las excepciones declaradas (CT-10 sin
    motivo, calc_id que no es un servicio, ficha sin manejador, artefacto sin valores en línea); lo demás, una entrada
    REEJECUCION.
Uso: .venv/bin/python -I r01_05_h13_h14_fuzz.py
"""
import copy
import datetime as dt
import decimal
import fractions
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.herramientas.ht01_datos import DatosNoDisponibles  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

K = C.Contador("r01_05 H-13 y H-14")


class ProveedorSerie:
    """HT-01 de juguete: una serie diaria determinista; «NOEXISTE» no está."""
    as_of = None
    nombre = "qa-t118"

    def cierres(self, serie, inicio=None, fin=None):
        if serie == "NOEXISTE":
            raise DatosNoDisponibles(f"sin datos de {serie}")
        idx = pd.bdate_range("2015-01-01", "2024-12-31")
        s = pd.Series(100 * np.exp(np.cumsum(0.01 * np.random.default_rng(len(str(serie))).standard_normal(len(idx)))), index=idx)
        s = s.loc[inicio:fin] if (inicio or fin) else s
        if s.empty:        # como el HT-01 real (`_tramo`): un rango sin datos es DatosNoDisponibles
            raise DatosNoDisponibles(f"sin datos de {serie} en el rango")
        return s

    def huella(self, serie, inicio=None, fin=None):
        return f"h-{serie}-{inicio}-{fin}"[:32]


tmp = tempfile.mkdtemp(prefix="qa_t118_fuzz_")
m = servicio.Motor(Almacen(Path(tmp)), ProveedorSerie(), cargar_config())


def profunda(n, tipo="lista"):
    x = [] if tipo == "lista" else {}
    for _ in range(n):
        x = [x] if tipo == "lista" else {"a": x}
    return x


def gen():
    yield 1


RAROS = {
    "None": None, "True": True, "False": False, "0": 0, "-1": -1, "1.5": 1.5, "nan": float("nan"), "inf": float("inf"), "-inf": float("-inf"),
    "10**400": 10 ** 400, "''": "", "' '": " ", "texto largo": "x" * 100_000, "texto con nulo": "a\x00b", "unicode raro": "\ud800",
    "bytes": b"RV", "bytearray": bytearray(b"x"), "[]": [], "[None]": [None], "[1]": [1], "['RV']": ["RV"], "{}": {}, "{'a':1}": {"a": 1},
    "{1:2}": {1: 2}, "{None:1}": {None: 1}, "{(1,2):3}": {(1, 2): 3}, "tupla": (1, 2), "set": {1, 2}, "frozenset": frozenset({1}),
    "np.array": np.array([1, 2]), "np.array vacío": np.array([]), "np.array 0-d": np.array(7), "np.float64 nan": np.float64("nan"),
    "np.int64": np.int64(7), "np.bool_": np.bool_(True), "Decimal": decimal.Decimal("1.5"), "Fraction": fractions.Fraction(1, 3),
    "complejo": 1 + 2j, "object()": object(), "lambda": (lambda: 1), "clase": dict, "Timestamp": pd.Timestamp("2024-01-01"),
    "NaT": pd.NaT, "date": dt.date(2024, 1, 1), "Series": pd.Series([1.0, 2.0]), "DataFrame": pd.DataFrame({"a": [1]}), "range": range(3),
    "generador": None,   # se crea en cada uso
    "lista a 31": profunda(31), "lista a 33": profunda(33), "lista a 500": profunda(500), "lista a 3000": profunda(3000),
    "objeto a 33": profunda(33, "objeto"), "objeto a 3000": profunda(3000, "objeto"), "lista que se contiene": None,
}


def raro(nombre):
    if nombre == "generador":
        return gen()
    if nombre == "lista que se contiene":
        x = []
        x.append(x)
        return x
    return RAROS[nombre]


FICHAS = ["SIM-MC-001", "REI-CAP-001", "DEC-VOI-001", "FX-BRK-001"]
CAMPOS = ["operacion", "datos", "parametros", "perfil", "clase", "horizonte", "modo", "plan", "prioridad", "semilla", "fecha_corte",
          "campo_desconocido"]
escapes, sin_rc, total = {}, {}, 0


def probar(etiqueta, pet, solicitante="AG-18", **kw):
    global total
    total += 1
    antes = len(m.almacen.leer("RC"))
    try:
        m.servir(pet, solicitante, **kw)
    except RecursionError as e:
        escapes.setdefault("RecursionError", []).append(etiqueta)
    except Exception as e:  # noqa: BLE001
        escapes.setdefault(type(e).__name__, []).append(f"{etiqueta}: {str(e)[:80]}")
    try:
        n = len(m.almacen.leer("RC")) - antes
    except Exception as e:  # noqa: BLE001
        sin_rc.setdefault("RC ilegible", []).append(f"{etiqueta}: {type(e).__name__}")
        return
    if n != 1:
        sin_rc.setdefault(f"{n} entradas", []).append(etiqueta)


print("[1] cada campo de la petición con valores raros")
for f in FICHAS:
    for campo in CAMPOS:
        for nombre in RAROS:
            pet = C.peticion(f)
            pet[campo] = raro(nombre)
            probar(f"{f} · {campo} = {nombre}", pet)
    # dentro de datos
    for nombre in RAROS:
        for sitio, hacer in (
                ("datos=[X]", lambda p, x: p.__setitem__("datos", [x])),
                ("datos=[{valores: X}]", lambda p, x: p.__setitem__("datos", [{"valores": x}])),
                ("datos=[{serie: X}]", lambda p, x: p.__setitem__("datos", [{"serie": x}])),
                ("datos[0].valores[k]=X", lambda p, x: p["datos"][0]["valores"].__setitem__("_qa", x)),
                ("datos=[{serie:'A', inicio: X}]", lambda p, x: p.__setitem__("datos", [{"serie": "A", "inicio": x}])),
                ("datos=[{serie:'A', fin: X}]", lambda p, x: p.__setitem__("datos", [{"serie": "A", "fin": x}])),
                ("datos=[{serie:'A', rol: X}]", lambda p, x: p.__setitem__("datos", [{"serie": "A", "rol": x}])),
                ("datos=[{serie:'A', alias: X}]", lambda p, x: p.__setitem__("datos", [{"serie": "A", "alias": x}])),
                ("parametros[k]=X", lambda p, x: p["parametros"].__setitem__("_qa", x)),
                ("parametros.semilla=X", lambda p, x: p["parametros"].__setitem__("semilla", x)),
                ("parametros.clase=X", lambda p, x: p["parametros"].__setitem__("clase", x)),
                ("operacion={ficha_id: X}", lambda p, x: p.__setitem__("operacion", {"ficha_id": x})),
                ("clave rara en valores", lambda p, x: p["datos"][0]["valores"].__setitem__(x, 1)),
                ("clave rara en la petición", lambda p, x: p.__setitem__(x, 1))):
            pet = C.peticion(f)
            try:
                hacer(pet, raro(nombre))
            except TypeError:      # no hashable como clave: no es una petición construible
                continue
            probar(f"{f} · {sitio} · {nombre}", pet)
    print(f"   {f}: acumulado {total} llamadas; escapes {sum(map(len, escapes.values()))}; sin una entrada en RC {sum(map(len, sin_rc.values()))}")
    sys.stdout.flush()
for nombre in RAROS:
    probar(f"petición = {nombre}", raro(nombre))
    probar(f"solicitante = {nombre}", C.peticion("REI-CAP-001"), raro(nombre))
    probar(f"run_id = {nombre}", C.peticion("REI-CAP-001"), run_id=raro(nombre))
    probar(f"msg_id = {nombre}", C.peticion("REI-CAP-001"), msg_id=raro(nombre))
for nombre in ("NOEXISTE", "A"):
    probar(f"serie {nombre}", {"operacion": "RISK-VAR-001", "datos": [{"serie": nombre}], "parametros": {}})
print(f"   llamadas: {total}")
for k, v in escapes.items():
    print(f"   ESCAPA {k}: {len(v)}")
    for e in v[:12]:
        print(f"      {e}")
for k, v in sin_rc.items():
    print(f"   {k}: {len(v)}")
    for e in v[:12]:
        print(f"      {e}")
K.comprobar(f"ninguna excepción escapa de Motor.servir en {total} llamadas", not escapes, str({k: len(v) for k, v in escapes.items()}))
K.comprobar("cada llamada deja exactamente una entrada en RC", not sin_rc, str({k: len(v) for k, v in sin_rc.items()}))
try:
    m2 = servicio.Motor(Almacen(Path(tmp)), ProveedorSerie(), cargar_config())
    integ = m2.almacen.verificar_integridad("RC")
    n_rc = len(m2.almacen.leer("RC"))
except Exception as e:  # noqa: BLE001
    integ, n_rc = f"{type(e).__name__}: {str(e)[:200]}", None
K.comprobar(f"el RC resultante ({n_rc} entradas) se vuelve a abrir y su cadena es íntegra", isinstance(integ, dict) and integ.get("RC") is True, str(integ))

# ------------------------------------------------------------------ 2
print("\n[2] anidamiento")
tope = servicio.PROFUNDIDAD_MAXIMA


def prof(x):
    """Niveles de contenedor por debajo de x (x contenedor = 1), sin recursión de Python profunda (los casos son llanos)."""
    if isinstance(x, dict):
        return 1 + max([prof(v) for v in x.values()] + [prof(k) for k in x] + [0])
    if isinstance(x, (list, tuple, set, frozenset)):
        return 1 + max([prof(v) for v in x] + [0])
    return 0


pmax = max((prof(C.peticion(f, i)), f, i) for f, cs in servicio.CASOS_CONTROL.items() for i in range(len(cs)))
print(f"   petición legítima más profunda entre los casos de control: {pmax[0]} niveles ({pmax[1]} caso {pmax[2]}); tope {tope}")
K.comprobar("ningún caso de control se acerca al tope de anidamiento (≤ 16 niveles)", pmax[0] <= 16, str(pmax))
borde = {}
for sitio, hacer in (("valores", lambda p, x: p["datos"][0]["valores"].__setitem__("_qa", x)),
                     ("parametros", lambda p, x: p["parametros"].__setitem__("_qa", x)),
                     ("campo de la petición", lambda p, x: p.__setitem__("_qa", x))):
    for tipo in ("lista", "objeto"):
        primero = None
        for n in list(range(1, 41)) + [500, 3000]:
            pet = C.peticion("REI-CAP-001")
            hacer(pet, profunda(n, tipo))
            r, exc, k = C.servir_contando(m, pet)
            if exc is not None or k != 1:
                K.comprobar(f"anidamiento {tipo} × {n} en {sitio}", False, f"{type(exc).__name__ if exc else ''} · {k} entradas")
                break
            if r["estado"] == "RECHAZADO" and "anidamiento" in r["detalle"] and primero is None:
                primero = (n, prof(pet))
        borde[(sitio, tipo)] = primero
        print(f"   {sitio} · {tipo}: primer rechazo por anidamiento con {primero[0] if primero else None} niveles añadidos "
              f"(petición de {primero[1] if primero else None} niveles)")
K.comprobar(f"el rechazo empieza exactamente cuando la petición tiene {tope + 1} niveles de contenedor (tope {tope}), en todos los sitios",
            all(v and v[1] == tope + 1 for v in borde.values()), str(borde))
# peticiones que el propio ejecutor hace al Motor en un ciclo: profundidad máxima vista
print("   (la profundidad de las peticiones que el ciclo hace al Motor se mide en r01_06, con el RC del ciclo)")

# ------------------------------------------------------------------ 3
print("\n[3] reejecutar con artefactos alterados")
DECLARADAS = (ValueError, KeyError, NotImplementedError)
base = {f: m.servir(C.peticion(f), "AG-18")["calc_id"] for f in ("SIM-MC-001", "REI-CAP-001", "DEC-VOI-001")}
r_serie = m.servir({"operacion": "RISK-VAR-001", "datos": [{"serie": "A", "inicio": "2020-01-01", "fin": "2023-12-29"}], "parametros": {},
                    "fecha_corte": "2024-01-31"}, "AG-18")
print(f"   RISK-VAR-001 con serie de HT-01: {r_serie['estado']}")
if str(r_serie["estado"]).startswith("SERVED"):
    base["RISK-VAR-001 (HT-01)"] = r_serie["calc_id"]
ALTER = {
    "parametros None": lambda e: e.__setitem__("parametros", None),
    "parametros lista": lambda e: e.__setitem__("parametros", [1]),
    "parametro desconocido": lambda e: e["parametros"].__setitem__("_qa", 1),
    "parametros con NaN": lambda e: e["parametros"].__setitem__("semilla", float("nan")),
    "sin parametros": lambda e: e.pop("parametros"),
    "datos None": lambda e: e.__setitem__("datos", None),
    "datos []": lambda e: e.__setitem__("datos", []),
    "datos [7]": lambda e: e.__setitem__("datos", [7]),
    "dato sin valor ni serie": lambda e: e.__setitem__("datos", [{"claves": []}]),
    "valor en línea texto": lambda e: e["datos"][0].__setitem__("valor", "en línea") if "valor" in e["datos"][0] else e["datos"][0].__setitem__("serie_ht01", 7),
    "valor en línea vacío": lambda e: e["datos"][0].__setitem__("valor", {}) if "valor" in e["datos"][0] else e["datos"][0].__setitem__("serie_ht01", "NOEXISTE"),
    "valor muy anidado": lambda e: e["datos"][0].__setitem__("valor", {"x": profunda(3000)}) if "valor" in e["datos"][0] else e["datos"][0].__setitem__("inicio", "ayer"),
    "sin huella": lambda e: e["datos"][0].pop("huella", None),
    "fecha_dato posterior al as_of": lambda e: e["datos"][0].__setitem__("fecha_dato", "2030-01-01"),
    "as_of None": lambda e: e.__setitem__("as_of", None),
    "as_of ilegible": lambda e: e.__setitem__("as_of", "ayer"),
    "as_of 1900": lambda e: e.__setitem__("as_of", "1900-01-01"),
    "operacion None": lambda e: e.__setitem__("operacion", None),
    "operacion sin ficha_id": lambda e: e["operacion"].pop("ficha_id"),
    "ficha_id lista": lambda e: e["operacion"].__setitem__("ficha_id", ["SIM-MC-001"]),
    "ficha_id de otra ficha": lambda e: e["operacion"].__setitem__("ficha_id", "ACC-ERP-001"),
    "ficha sin manejador": lambda e: e["operacion"].__setitem__("ficha_id", "NO-EXISTE-001"),
    "resultado None": lambda e: e.__setitem__("resultado", None),
    "sin resultado": lambda e: e.pop("resultado"),
    "payload None": lambda e: e["resultado"].__setitem__("payload", None),
    "payload lista": lambda e: e["resultado"].__setitem__("payload", [1, 2]),
    "payload con NaN": lambda e: e["resultado"].__setitem__("payload", {"a": float("nan")}),
    "payload muy anidado": lambda e: e["resultado"].__setitem__("payload", {"a": profunda(31)}),
    "tipo_entrada RECHAZO": lambda e: e.__setitem__("tipo_entrada", "RECHAZO"),
    "n_trayectorias 1e9 / tamaño fuera de cota": lambda e: e["parametros"].__setitem__("n_trayectorias", 10 ** 9),
    "semilla texto": lambda e: e.__setitem__("semilla", "siete"),
}
no_declaradas, sin_entrada, tabla = [], [], {}
for f, calc in base.items():
    for nombre, cambio in ALTER.items():
        e = copy.deepcopy(m.almacen.estado("RC")[calc])
        try:
            cambio(e)
            e["calc_id"] = m.almacen.nuevo_id("CALC")
            m.almacen.escribir("RC", "AG-13", e)
        except Exception as exc:  # noqa: BLE001
            tabla[(f, nombre)] = f"(no se puede construir o escribir: {type(exc).__name__})"
            continue
        antes = len(m.almacen.leer("RC"))
        try:
            out = m.reejecutar(e["calc_id"], "QA r01 de T-118")
            res = f"{out['coincide']}/{out['categoria']}"
        except DECLARADAS as exc:
            res = f"declarada {type(exc).__name__}: {str(exc)[:70]}"
        except BaseException as exc:  # noqa: BLE001
            if isinstance(exc, KeyboardInterrupt):
                raise
            res = f"ESCAPA {type(exc).__name__}: {str(exc)[:90]}"
            no_declaradas.append((f, nombre, res))
        n = len(m.almacen.leer("RC")) - antes
        tabla[(f, nombre)] = res
        if not res.startswith(("declarada", "ESCAPA")) and n != 1:
            sin_entrada.append((f, nombre, n))
import collections  # noqa: E402

por_resultado = collections.Counter(v.split(":")[0] for v in tabla.values())
print(f"   {len(tabla)} artefactos alterados: {dict(por_resultado)}")
for (f, nombre), v in tabla.items():
    if v.startswith(("declarada", "ESCAPA")):
        print(f"      {f} · {nombre}: {v}")
K.comprobar("de reejecutar solo salen excepciones de las tres clases declaradas (ValueError, KeyError, NotImplementedError)",
            not no_declaradas, str(no_declaradas)[:900])
# de las «declaradas», ¿cuáles no son ninguno de los cuatro casos documentados (sin motivo, no es servicio, sin manejador, sin valores)?
DOCUMENTADAS = ("sin motivo", "no es un servicio", "ya no tiene manejador", "sin los valores en línea")
no_doc = {k: v for k, v in tabla.items() if v.startswith("declarada") and not any(d in v for d in DOCUMENTADAS)}
print(f"   excepciones de clase declarada que NO son uno de los cuatro casos documentados: {len(no_doc)}")
for (f, nombre), v in no_doc.items():
    print(f"      {f} · {nombre}: {v}")
K.comprobar("toda re-ejecución que no es uno de los cuatro casos «imposibles» documentados queda registrada (H-14)", not no_doc,
            f"{len(no_doc)} artefactos acaban en excepción sin entrada REEJECUCION")
K.comprobar("toda re-ejecución que termina deja una entrada REEJECUCION", not sin_entrada, str(sin_entrada)[:300])

sys.exit(K.fin())
