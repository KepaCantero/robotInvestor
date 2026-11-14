"""QA r01 de T-113 · H-22 de T-108: peticiones del Motor mal formadas. Cada una debe dar RECHAZADO (o servirse) con su entrada
en RC, nunca una excepción al llamador, y no debe dejar la cadena del almacén rota.
Uso (desde bloque_a/11_Ejecutor de la copia): python .../r01_03_motor_forma.py"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402


class _Proveedor:
    as_of = None
    nombre = "pruebas"


class _Obj:
    def __str__(self):
        return "objeto"


tmp = Path(tempfile.mkdtemp(prefix="qa_t113_motor_", dir=os.environ.get("QA_TMP")))
m = servicio.Motor(Almacen(tmp), _Proveedor(), cargar_config())
ciclico: dict = {}
ciclico["yo"] = ciclico
hondo: object = 1
for _ in range(100000):
    hondo = [hondo]
BASE = {"operacion": "ST-DESC-001", "datos": [], "fecha_corte": "2026-11-12"}
CASOS = {
    "plan lista": {"plan": ["PLAN_MIN"]}, "plan dict": {"plan": {"PLAN_MIN": 1}}, "plan None": {"plan": None}, "plan 0": {"plan": 0},
    "plan NaN": {"plan": float("nan")}, "plan bytes": {"plan": b"PLAN_MIN"}, "plan tupla": {"plan": ("PLAN_MIN",)},
    "plan conjunto": {"plan": {"PLAN_MIN"}}, "plan vacío": {"plan": ""}, "plan minúscula": {"plan": "plan_min"},
    "parametros claves mezcladas": {"parametros": {"x": 1, 1: "x"}}, "parametros clave None": {"parametros": {"x": 1, None: 1}},
    "parametros clave tupla": {"parametros": {(1, 2): 3}}, "parametros cíclico": {"parametros": ciclico},
    "parametros hondo": {"parametros": {"a": hondo}}, "parametros con objeto": {"parametros": {"a": _Obj()}},
    "parametros con conjunto": {"parametros": {"a": {1, 2}}}, "parametros con NaN": {"parametros": {"a": float("nan")}},
    "parametros con bytes": {"parametros": {"a": b"\xff"}},
    "perfil claves mezcladas": {"perfil": [{1: 2, "x": 3}]}, "perfil texto": {"perfil": "RV"}, "perfil número": {"perfil": 7},
    "perfil cíclico": {"perfil": ciclico}, "clase dict mezclado": {"clase": {1: 2, "x": 3}}, "clase lista": {"clase": ["RV"]},
    "clase número": {"clase": 5}, "semilla dict mezclado": {"semilla": {1: 2, "x": 3}}, "semilla texto": {"semilla": "abc"},
    "semilla lista": {"semilla": [1]}, "semilla NaN": {"semilla": float("nan")}, "semilla inf": {"semilla": float("inf")},
    "semilla negativa": {"semilla": -1}, "semilla enorme": {"semilla": 10 ** 400},
    "horizonte claves mezcladas": {"horizonte": {1: 2, "x": 3}}, "horizonte cíclico": {"horizonte": ciclico},
    "modo claves mezcladas": {"modo": {1: 2, "x": 3}}, "prioridad claves mezcladas": {"prioridad": {1: 2, "x": 3}},
    "valores claves mezcladas": {"datos": [{"valores": {1: "a", "b": 2}}]}, "valores cíclicos": {"datos": [{"valores": ciclico}]},
    "valores hondos": {"datos": [{"valores": {"a": hondo}}]}, "valores clave tupla": {"datos": [{"valores": {(1, 2): 3}}]},
    "serie con rol dict mezclado": {"datos": [{"serie": "SPY", "rol": {1: 2, "x": 3}}]},
    "serie fin lista": {"datos": [{"serie": "SPY", "fin": [1]}]}, "serie inicio dict": {"datos": [{"serie": "SPY", "inicio": {"a": 1}}]},
    "operacion dict con ficha_id lista": {"operacion": {"ficha_id": ["ST-DESC-001"]}},
    "operacion dict con extra mezclado": {"operacion": {"ficha_id": "ST-DESC-001", 1: 2}},
    "fecha_corte lista": {"fecha_corte": [2026]}, "fecha_corte enorme": {"fecha_corte": 10 ** 30}, "fecha_corte dict": {"fecha_corte": {"a": 1}},
    "campo ajeno mezclado": {"otro": {1: 2, "x": 3}},
}
PETICIONES_RARAS = {"None": None, "lista": [], "texto": "ST-DESC-001", "número": 3, "dict vacío": {}, "clave no texto": {1: 2}}
fallos = 0
for nombre, extra in CASOS.items():
    n0 = len(m.almacen.leer("RC"))
    try:
        r = m.servir({**BASE, **extra}, "AG-03")
        en_rc = len(m.almacen.leer("RC")) - n0
        res = f"{r.get('estado')}/{r.get('motivo')} RC+{en_rc}"
        mal = r.get("estado") not in ("RECHAZADO",) and nombre not in ("plan None",) and r.get("estado") is None or en_rc != 1
    except BaseException as e:  # noqa: BLE001
        res = f"EXCEPCIÓN {type(e).__name__}: {str(e)[:70]}"
        mal = True
    fallos += bool(mal)
    print(f"{'FALLO' if mal else 'ok   '} {nombre:36s} {res}")
for nombre, pet in PETICIONES_RARAS.items():
    try:
        r = m.servir(pet, "AG-03"); res = f"{r.get('estado')}/{r.get('motivo')}"; mal = r.get("estado") != "RECHAZADO"
    except BaseException as e:  # noqa: BLE001
        res = f"EXCEPCIÓN {type(e).__name__}: {str(e)[:70]}"; mal = True
    fallos += bool(mal)
    print(f"{'FALLO' if mal else 'ok   '} petición {nombre:27s} {res}")
for nombre, sol in (("solicitante dict mezclado", {1: 2, "x": 3}), ("solicitante None", None)):
    try:
        r = m.servir(dict(BASE), sol); res = f"{r.get('estado')}/{r.get('motivo')}"; mal = False
    except BaseException as e:  # noqa: BLE001
        res = f"EXCEPCIÓN {type(e).__name__}: {str(e)[:70]}"; mal = True
    print(f"{'aviso' if mal else 'ok   '} {nombre:36s} {res}  (el solicitante lo pone el ejecutor, no la petición)")
# el almacén sigue íntegro y se puede reabrir
try:
    a2 = Almacen(tmp); integ = a2.integridad() if hasattr(a2, "integridad") else "sin integridad()"
    print("almacén reabierto; integridad:", integ if not isinstance(integ, (list, dict)) or integ else "sin fallos", "· RC:", len(a2.leer("RC")))
except BaseException as e:  # noqa: BLE001
    fallos += 1; print("FALLO el almacén no reabre:", type(e).__name__, str(e)[:100])
# idempotencia: la misma petición mal formada dos veces da el mismo rechazo
a = m.servir({**BASE, "plan": ["PLAN_MIN"]}, "AG-03"); b = m.servir({**BASE, "plan": ["PLAN_MIN"]}, "AG-03")
print("idempotencia del rechazo:", (a["estado"], a["motivo"], a.get("detalle")) == (b["estado"], b["motivo"], b.get("detalle")))
print("FALLOS:", fallos)
