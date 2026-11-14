"""QA r02 de T-113 · H-01 por el camino real, con más formas que `r01_13`: `Agentes.invocar` (cliente simulado) y
`AnthropicClient.generar` (SDK simulado) con contenido estructurado: diccionarios bajo listas y tuplas a varios niveles,
bloques de herramienta, bytes, estructuras cíclicas y compartidas. Nada con un secreto debe llegar al cliente ni al SDK; lo
limpio debe llegar. Y el estado de H-04 (peticiones del Motor que siguen lanzando).
Uso (desde bloque_a/11_Ejecutor de la copia): QA_TMP=<carpeta> python .../r02_05_r8_camino_real.py"""
import os
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, ".")
sys.path.insert(0, "tests")
from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import AnthropicClient, MockClient  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402
from conftest import DATOS, config_pruebas  # noqa: E402

CLAVE = "api" + "_key"
SK = "sk-" + "ant-api03-abcdefghijklmnopqrstuvwxyz0123"
IBAN = "ES" + "91 2100 0418 " + "4502 0005 1332"
par = {CLAVE: "abcdef123456"}
t = Path(tempfile.mkdtemp(prefix="qa_t113_r02_r8_", dir=os.environ.get("QA_TMP")))
fallos = 0

ciclo: list = [{"type": "text", "text": "hola"}]
ciclo.append(ciclo)
comp = [{"type": "text", "text": "hola"}]
SUCIOS = {
    "lista > dict": [par], "tupla > dict": (par,), "lista > lista > tupla > dict": [[(par,)]], "dict > lista > dict": {"a": [par]},
    "bloque tool_result con dict": [{"type": "tool_result", "content": par}], "bloque tool_result con lista de dict": [{"type": "tool_result", "content": [par]}],
    "bloque con input anidado": [{"type": "tool_use", "input": {"q": [{"x": (par,)}]}}], "clave secreta en dict bajo tupla": ({"a": {SK: 1}},),
    "bytes con sk": [{"type": "text", "text": SK.encode()}], "IBAN con espacios en bloque": [{"type": "text", "text": f"cobren en {IBAN}"}],
    "ciclo (no se puede comprobar: falla cerrado)": ciclo,
}
LIMPIOS = {"texto": "hola", "bloques": [{"type": "text", "text": "hola"}], "la misma lista dos veces": [comp, comp],
           "bloque con dict vacío y números": [{"type": "tool_result", "content": {"a": 1, "b": [None, 2.5]}}]}

print("== AnthropicClient.generar (SDK simulado)")
enviados = []
sdk = SimpleNamespace(messages=SimpleNamespace(create=lambda **k: (enviados.append(k), SimpleNamespace(usage=None, stop_reason="end_turn", content=[]))[1]))
c = AnthropicClient.__new__(AnthropicClient)
c.sdk, c.salida_estructurada, c.max_continuaciones = sdk, False, 0
for sucio, casos in ((True, SUCIOS), (False, LIMPIOS)):
    for nombre, contenido in casos.items():
        for donde in ("mensajes", "system"):
            n0 = len(enviados)
            mensajes = [{"role": "user", "content": contenido if donde == "mensajes" else "hola"}]
            system = [{"type": "text", "text": "s"}] + ([{"type": "text", "text": "x", "extra": contenido}] if donde == "system" else [])
            try:
                r = c.generar(agente="AG-01", modelo="m", system=system, mensajes=mensajes, max_tokens=10)
                res = f"stop={r.stop_reason}"
            except Exception as e:  # noqa: BLE001
                res = f"EXC {type(e).__name__}"
            n = len(enviados) - n0
            mal = (n != 0) if sucio else (n != 1)
            fallos += mal
            print(f"{'FALLO' if mal else 'ok   '} {'sucio ' if sucio else 'limpio'} {donde:8s} {nombre:46s} {res} · enviado al SDK: {n}")

print("== Agentes.invocar (cliente simulado)")
cli = MockClient()
b = Bloque(config_pruebas(), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cli, t / "e", t / "n")
for nombre, contenido in SUCIOS.items():
    for donde in ("mensaje", "contexto"):
        n0 = len(cli.llamadas)
        msg = {"piezas": contenido} if donde == "mensaje" else {"piezas": []}
        ctx = {"fecha_as_of": "2026-06-05", "modo": "backtest", **({"extra": contenido} if donde == "contexto" else {})}
        try:
            r = b.agentes.invocar("AG-12", "CT-11", msg, "CURACION", "Clasifica.", ctx)
            res = f"{r.estado} {r.errores}"
        except Exception as e:  # noqa: BLE001
            res = f"EXC {type(e).__name__}: {str(e)[:50]}"
        n = len(cli.llamadas) - n0
        fallos += n != 0
        print(f"{'FALLO' if n else 'ok   '} {donde:8s} {nombre:46s} {res[:70]} · llamadas al cliente: {n}")

print("== H-04 de la r01 (lo que T-118 dice haber corregido en `motor/servicio.py`)")


class _P:
    as_of = None
    nombre = "pruebas"


m = servicio.Motor(Almacen(t / "motor"), _P(), cargar_config())
BASE = {"operacion": "ST-DESC-001", "datos": [], "fecha_corte": "2026-11-12"}   # la misma base que `r01_03`
cic: dict = {}
cic["yo"] = cic
hondo: object = 1
for _ in range(5000):
    hondo = [hondo]
h04 = 0
for nombre, extra in {"horizonte claves mezcladas": {"horizonte": {1: 2, "x": 3}}, "modo claves mezcladas": {"modo": {1: 2, "x": 3}},
                      "prioridad claves mezcladas": {"prioridad": {1: 2, "x": 3}}, "horizonte cíclico": {"horizonte": cic}, "modo cíclico": {"modo": cic},
                      "valores muy hondos": {"datos": [{"valores": {"a": hondo}}]}, "horizonte muy hondo": {"horizonte": hondo},
                      "horizonte clave tupla": {"horizonte": {(1, 2): 3}}, "prioridad conjunto": {"prioridad": {1, 2}}}.items():
    n0 = len(m.almacen.leer("RC"))
    try:
        r = m.servir({**BASE, **extra}, "AG-03")
        res = f"{r.get('estado')}/{r.get('motivo')}"
    except BaseException as e:  # noqa: BLE001
        res = f"EXCEPCIÓN {type(e).__name__}: {str(e)[:60]}"
        h04 += 1
    print(f"   {nombre:28s} {res} · RC +{len(m.almacen.leer('RC')) - n0}")
try:
    print("   el almacén reabre:", len(Almacen(t / "motor").leer("RC")), "entradas en RC")
except BaseException as e:  # noqa: BLE001
    fallos += 1
    print("FALLO el almacén no reabre:", type(e).__name__)
print(f"H-04: peticiones que aún lanzan una excepción al llamador: {h04}")
print("FALLOS (R8):", fallos)
