"""T-66 · QA r01 · utilidades comunes de los scripts de ataque (revisor independiente).

Uso: PYTHONPATH=<ejecutor de A> python r01_xx.py   (cada script imprime OK / HALLAZGO / INFO por comprobación)
"""
import copy
import json
import sys
import tempfile
from pathlib import Path

import bloque_a
from bloque_a import mock_respuestas as mr
from bloque_a.configuracion import CLASES, RUTA_UNIVERSO_EJEMPLO, cargar_config, fusionar
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient, RespuestaLLM
from bloque_a.orquestacion import Bloque

RAIZ = Path(bloque_a.__file__).resolve().parents[1]
DATOS = RAIZ / "ejemplos" / "datos_sinteticos"
AS_OF = "2026-06-05"
TODAS = list(CLASES)
RESUMEN: list[tuple[str, str]] = []


def cfg(todas=True, **extra):
    base = {"modo": "backtest", "evaluacion": {"bootstrap_replicas": 300, "simulaciones_ece": 300}}
    if todas:
        base["perfiles"] = {"activos": TODAS}
    return cargar_config(extra=fusionar(base, extra))


def bloque(c=None, cliente=None, tmp=None):
    tmp = Path(tmp or tempfile.mkdtemp(prefix="r01_"))
    return Bloque(c or cfg(), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cliente or MockClient(),
                  tmp / "estado", tmp / "ent")


class Gancho(MockClient):
    """Simulado con un gancho que puede reescribir la respuesta de cada agente: gancho(agente, msg, datos) -> datos.
    Si el gancho lanza una excepción, se propaga (simula un fallo del proveedor)."""

    def __init__(self, gancho, conocimiento_previo=False, **kw):
        super().__init__(**kw)
        self.gancho = gancho
        self.conocimiento_previo = conocimiento_previo

    def generar(self, *, agente, modelo, system, mensajes, max_tokens, herramientas=None, esquema=None):
        r = super().generar(agente=agente, modelo=modelo, system=system, mensajes=mensajes, max_tokens=max_tokens,
                            herramientas=herramientas, esquema=esquema)
        msg = mr.extraer_encargo(mensajes[0]["content"])["mensaje"]
        datos = json.loads(r.texto)
        nuevo = self.gancho(agente, msg, copy.deepcopy(datos))
        if nuevo is None:
            nuevo = datos
        return RespuestaLLM(texto=nuevo if isinstance(nuevo, str) else json.dumps(nuevo, ensure_ascii=False),
                            uso=r.uso, modelo=r.modelo, stop_reason=r.stop_reason)


def comprobar(nombre: str, ok: bool, detalle: str = "", hallazgo: bool = True) -> bool:
    etiqueta = "OK" if ok else ("HALLAZGO" if hallazgo else "INFO")
    RESUMEN.append((etiqueta, nombre))
    print(f"[{etiqueta}] {nombre}" + (f" · {detalle}" if detalle else ""))
    return ok


def fin():
    n = sum(1 for e, _ in RESUMEN if e == "HALLAZGO")
    print(f"--- {len(RESUMEN)} comprobaciones, {n} con hallazgo")
    sys.exit(0)


def opciones_f3(b):
    return list(b.almacen.estado("F3").values())


def ultimo_run(b):
    return [x for x in b.almacen.leer("F5") if x.get("tipo_entrada") == "RUN"][-1]
