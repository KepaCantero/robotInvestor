"""QA r01 de T-156 · ataques a H-01 (rango de `llm.reintentos.cobro_posible_desde`), sin red, sin clave real y sin coste.

Uso: python -I r01_01_rango_cobro.py <ruta a 11_Ejecutor> <carpeta temporal>

Qué comprueba (FALLA si no):
  V01 bordes: 100 y 500 se admiten (y el valor por defecto, 500); 99, 501, 599, 600, 0, -1 y 10**6 se rechazan con
      ValueError que nombra la clave.
  V02 tipos: True, False, 500.0, 450.5, NaN, ±inf, -0.0, «500», «», «5xx», [500], {"v": 500}, Decimal(500), Fraction(500),
      numpy.int64(500) (si está numpy) se rechazan con ValueError; None con KeyError (clave nula = falta, sin respaldo).
  V03 clave ausente: sin la clave en la configuración del usuario sale la de `por_defecto.yaml` (500); sin ella tampoco en
      `por_defecto.yaml`, KeyError (falla cerrado).
  V04 YAML del operador: `600`, `5e2` (cadena en YAML 1.1), `500.0`, `yes`, `~` y `"500"` se rechazan al crear el cliente
      real (`crear_cliente("anthropic")`), antes de crear el SDK (no sale ninguna petición); `0x1F4` es 500 y vale.
  V05 monotonía: para cada valor admitido d (100…500), cada estado de 0 a 999 y cada `x-should-retry` (ausente, true, false,
      « TRUE », basura), con tres configuraciones de estados y de estados sin cobro: el reintento es el mismo que con 500 y
      el cobro, igual o mayor (más prudente); con 500 es exactamente la regla por defecto.
  V06 de punta a punta con el SDK real sobre `httpx2.MockTransport`: con 400 un 450 se carga una vez por su peor caso y con
      500 se suelta; ninguna reserva colgada; un 429 se suelta con cualquier valor (está en `estados_sin_cobro`).
  OBS: lo que no rompe un criterio (subclases de int como IntEnum).
"""
from __future__ import annotations

import enum
import os
import sys
import types
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
TMP = Path(sys.argv[2]).resolve()
TMP.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(EJ))
import anthropic
import httpx2
from bloque_a.configuracion import cargar_config, fusionar
from bloque_a.consumo import Contabilidad, Presupuesto, ReservaLlamada
from bloque_a.llm import (
    AnthropicClient,
    ReglaReintentos,
    clasificar_error,
    con_guarda,
    crear_cliente,
)

from bloque_a import configuracion

FALLOS: list[str] = []
REQ = httpx2.Request("POST", "https://api.invalid/v1/messages")
SISTEMA = [{"type": "text", "text": "s" * 3600}]
MENSAJES = [{"role": "user", "content": "hola"}]


def check(nombre, ok, detalle=""):
    print(("OK   " if ok else "FALLA") + f" {nombre}" + (f" · {detalle}" if detalle else ""), flush=True)
    if not ok:
        FALLOS.append(nombre)


def cfg_(**extra):
    return cargar_config(extra=fusionar({"modo": "vivo", "perfiles": {"activos": ["DIV"]}}, extra))


def con_desde(v, base=None):
    cfg = base or cfg_()
    cfg["llm"]["reintentos"]["cobro_posible_desde"] = v
    return cfg


def resultado(cfg):
    try:
        return "ok", ReglaReintentos.de_config(cfg)
    except Exception as e:  # noqa: BLE001
        return type(e).__name__, str(e)


# ---------------------------------------------------------------- V01
for v, vale in [(100, True), (500, True), (99, False), (501, False), (599, False), (600, False), (0, False), (-1, False),
                (10**6, False)]:
    tipo, r = resultado(con_desde(v))
    if vale:
        check(f"V01 {v} se admite", tipo == "ok" and r.cobro_posible == v, f"{tipo}")
    else:
        check(f"V01 {v} se rechaza nombrando la clave", tipo == "ValueError" and "cobro_posible_desde" in r, f"{tipo}: {r}")
tipo, r = resultado(cfg_())
check("V01 el valor por defecto (por_defecto.yaml) es 500 y vale", tipo == "ok" and r.cobro_posible == 500, tipo)

# ---------------------------------------------------------------- V02
raros = [True, False, 500.0, 450.5, float("nan"), float("inf"), float("-inf"), -0.0, "500", "", "5xx", [500], {"v": 500},
         Decimal(500), Fraction(500), complex(500, 0)]
try:
    import numpy as np
    raros += [np.int64(500), np.float64(500.0)]
except ImportError:  # pragma: no cover
    pass
for v in raros:
    tipo, r = resultado(con_desde(v))
    check(f"V02 {v!r} ({type(v).__name__}) se rechaza con ValueError", tipo == "ValueError" and "cobro_posible_desde" in str(r),
          f"{tipo}: {str(r)[:90]}")
tipo, r = resultado(con_desde(None))
check("V02 None (clave nula) falla cerrado con KeyError", tipo == "KeyError", f"{tipo}: {str(r)[:90]}")


class Estado(enum.IntEnum):
    INTERNO = 500
    ALTO = 600


class Entero(int):
    pass


for v in (Estado.INTERNO, Estado.ALTO, Entero(450), Entero(600)):
    tipo, r = resultado(con_desde(v))
    print(f"OBS  subclase de int {v!r}: {tipo}" + (f" (cobro_posible {r.cobro_posible})" if tipo == "ok" else f": {str(r)[:60]}"))
    if int(v) > 500 or int(v) < 100:
        check(f"V02 subclase de int fuera de rango {v!r} se rechaza", tipo == "ValueError")

# ---------------------------------------------------------------- V03
cfg = cfg_()
del cfg["llm"]["reintentos"]["cobro_posible_desde"]
tipo, r = resultado(cfg)
check("V03 sin la clave en la configuración: la de por_defecto.yaml (500)", tipo == "ok" and r.cobro_posible == 500, tipo)
orig = configuracion._CONFIG_POR_DEFECTO
try:
    import copy
    sin = copy.deepcopy(configuracion.config_por_defecto())
    del sin["llm"]["reintentos"]["cobro_posible_desde"]
    configuracion._CONFIG_POR_DEFECTO = sin
    tipo, r = resultado(cfg)
    check("V03 sin la clave tampoco en por_defecto.yaml: KeyError", tipo == "KeyError", f"{tipo}: {str(r)[:90]}")
finally:
    configuracion._CONFIG_POR_DEFECTO = orig

# ---------------------------------------------------------------- V04
os.environ["ANTHROPIC_API_KEY"] = "clave-falsa-qa"
creados: list[int] = []
_anth_init = anthropic.Anthropic.__init__


def _espia_init(self, *a, **k):
    creados.append(1)
    _anth_init(self, *a, **k)


anthropic.Anthropic.__init__ = _espia_init  # type: ignore[method-assign]
try:
    for texto, vale, error in [("600", False, "ValueError"), ("5e2", False, "ValueError"), ("500.0", False, "ValueError"),
                               ("yes", False, "ValueError"), ("~", False, "KeyError"), ('"500"', False, "ValueError"),
                               ("0x1F4", True, None), ("100", True, None), ("500", True, None)]:
        ruta = TMP / "operador.yaml"
        ruta.write_text(f"modo: vivo\nllm:\n  reintentos:\n    cobro_posible_desde: {texto}\n", encoding="utf-8")
        creados.clear()
        try:
            cli = crear_cliente("anthropic", cargar_config(str(ruta)))
            obtenido = "ok"
        except Exception as e:  # noqa: BLE001
            cli, obtenido = None, type(e).__name__
        if vale:
            check(f"V04 YAML `cobro_posible_desde: {texto}` crea el cliente", obtenido == "ok" and isinstance(cli, AnthropicClient)
                  and cli.reintentos is not None and 100 <= cli.reintentos.cobro_posible <= 500, obtenido)
        else:
            check(f"V04 YAML `cobro_posible_desde: {texto}` se rechaza antes de crear el SDK", obtenido == error and not creados,
                  f"{obtenido}, SDK creados {len(creados)}")
finally:
    anthropic.Anthropic.__init__ = _anth_init  # type: ignore[method-assign]
    os.environ.pop("ANTHROPIC_API_KEY", None)


# ---------------------------------------------------------------- V05
def estado(n, cab=None):
    resp = types.SimpleNamespace(headers=cab or {})
    e = anthropic.APIStatusError.__new__(anthropic.APIStatusError)
    e.status_code, e.response = n, resp   # type: ignore[assignment]
    return e


def real(n, cab=None):
    return anthropic.APIStatusError("x", response=httpx2.Response(n, request=REQ, headers=cab or {}), body=None)


# el atajo (`__new__`) clasifica igual que un error real del SDK
muestra = [(n, x) for n in (100, 404, 450, 499, 500, 501, 529, 599) for x in (None, "true", "false")]
iguales = all(clasificar_error(estado(n, {} if x is None else {"x-should-retry": x}), ReglaReintentos.de_config(cfg_()))
              == clasificar_error(real(n, {} if x is None else {"x-should-retry": x}), ReglaReintentos.de_config(cfg_()))
              for n, x in muestra)
check("V05 el error construido clasifica igual que uno del SDK", iguales)

variantes = {
    "por defecto": {},
    "4xx en la lista": {"estados_reintentables": [400, 408, 409, 418, 429, 450, 500, 502, 503, 504, 529],
                        "estados_sin_cobro": [429, 450, 529]},
    "sin 5xx en la lista": {"estados_reintentables": [408, 429], "estados_sin_cobro": [429]},
}
cabeceras = [None, "true", "false", " TRUE ", "quiza"]
total = 0
for nombre, cambios in variantes.items():
    base = cfg_(llm={"reintentos": cambios}) if cambios else cfg_()
    r500 = ReglaReintentos.de_config(con_desde(500, base))
    errores = {(n, x): estado(n, {} if x is None else {"X-Should-Retry": x}) for n in range(1000) for x in cabeceras}
    ref = {k: clasificar_error(e, r500) for k, e in errores.items()}
    malos = []
    for d in range(100, 501):
        rd = ReglaReintentos.de_config(con_desde(d, base))
        for k, e in errores.items():
            got = clasificar_error(e, rd)
            total += 1
            if got[0] != ref[k][0] or (ref[k][1] and not got[1]):
                malos.append((d, k, got, ref[k]))
    check(f"V05 monotonía ({nombre}): con 100 ≤ d ≤ 500, mismo reintento y cobro ≥ que con 500", not malos,
          f"{len(malos)} casos que cobran menos {malos[:3]}")
    if not cambios:
        defecto = ReglaReintentos.de_config(cfg_())
        check("V05 con 500 la clasificación es la de la regla por defecto",
              all(clasificar_error(e, defecto) == ref[k] for k, e in errores.items()))
print(f"     V05: {total} clasificaciones comparadas")


# ---------------------------------------------------------------- V06
def _msg():
    return {"id": "m", "type": "message", "role": "assistant", "model": "modelo-de-prueba",
            "content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "stop_sequence": None,
            "usage": {"input_tokens": 100, "output_tokens": 50}}


class Srv:
    def __init__(self, *guion):
        self.guion, self.n = list(guion), 0

    def __call__(self, req):
        self.n += 1
        paso = self.guion[min(self.n, len(self.guion)) - 1]
        if paso == 200:
            return httpx2.Response(200, json=_msg())
        return httpx2.Response(paso, headers={"retry-after": "0"}, json={"type": "error", "error": {"type": "api_error", "message": "x"}})


def correr(srv, cfg):
    sdk = anthropic.Anthropic(api_key="clave-falsa-qa", max_retries=5, http_client=httpx2.Client(transport=httpx2.MockTransport(srv)))
    cli = AnthropicClient(sdk=sdk, reintentos=ReglaReintentos.de_config(cfg), dormir=lambda s: None)
    p = Presupuesto({"DIV": 100.0}, cfg)
    g = ReservaLlamada(p, "DIV", Contabilidad(cfg), "AG-05")
    mt = g.reservar(SISTEMA, MENSAJES, None, 1000)
    with con_guarda(g):
        r = cli.generar(agente="AG-05", modelo="modelo-de-prueba", system=SISTEMA, mensajes=MENSAJES, max_tokens=mt)
    g.pagar_resto(r.uso)
    g.cerrar()
    return r, p


for d, st, cargadas in [(400, 450, 1), (500, 450, 0), (400, 429, 0), (100, 429, 0), (100, 404, 1), (500, 404, 0), (400, 501, 1),
                        (500, 501, 1)]:
    srv = Srv(st)
    r, p = correr(srv, con_desde(d))
    peor = sum(s["reservado_uc"] for s in p.sin_respuesta)
    ok = (len(p.sin_respuesta) == cargadas and abs(p.reservado["DIV"]) < 1e-9 and abs(p.consumido["DIV"] - peor) < 1e-6
          and (peor > 0) == (cargadas > 0))
    check(f"V06 cobro_posible_desde {d}, estado {st}: {cargadas} cargada(s)", ok,
          f"peticiones {srv.n}, sin respuesta {len(p.sin_respuesta)}, consumido {p.consumido['DIV']:.4f}, "
          f"reservado {p.reservado['DIV']:.1e}, fin {r.stop_reason}")

print("RESULTADO:", "todo OK" if not FALLOS else f"{len(FALLOS)} FALLAN: {FALLOS}")
sys.exit(1 if FALLOS else 0)
