"""QA r01 de T-151 · ataques a los reintentos en el cliente (H-09) y a H-11, a nivel de unidad (sin red, sin clave, sin coste).

Uso: python -I r01_01_reintentos_unidad.py <ruta a 11_Ejecutor>
Cada caso imprime OK (el invariante se cumple), VIOLA (no se cumple) u OBS (comportamiento que se documenta, sin criterio que
lo exija) con las cifras. No escribe nada. El SDK es el real (anthropic) sobre un transporte falso (`httpx2.MockTransport`)
o un SDK doble en Python; ninguna petición sale de la máquina y la clave es falsa.

Casos:
  X1  el SDK real con `max_retries=5` recibido por el constructor: cada intento es una sola petición HTTP (el SDK no reintenta
      por su cuenta), cada reintento reserva antes de salir y lo que no se cobró (529) no queda en la bolsa
  X2  `AnthropicClient(api_key=…)` y `crear_cliente("anthropic")` crean el SDK con `max_retries=0` (sin enviar nada)
  X3  timeout → 503 → 529 → 200: lo que pudo cobrarse (timeout y 503) queda cargado por su peor caso, el 529 no, el 200 por lo
      real; nada reservado al cerrar y ningún cobro doble
  X4  agotar los reintentos con 500: `max_reintentos_api` + 1 peticiones, todas cargadas, `error_proveedor`, bolsa sin colgar
  X5  el reintento que no cabe tras un timeout: no sale, `presupuesto_agotado`, motivo con «reintento», lo fallido cargado
  X6  error no reintentable (400) y error ajeno al proveedor (TypeError del SDK): una sola petición, reserva suelta
  X7  KeyboardInterrupt en la espera entre reintentos (camino de `Bloque._invocar`): lo del timeout queda cargado, nada reservado
  X8  un reintento que acaba bien no se cobra dos veces: lo cargado = real + peor caso del que falló, exactamente
  X9  estados 5xx fuera de la lista (501, 505, 520) y 500 con `x-should-retry: false`: ¿se reintentan? ¿se cargan? (el SDK
      2.8 los reintenta todos; el README dice «5xx salvo 529» se carga)
  X10 `retry-after` muy grande: la espera no tiene tope (el SDK 2.8 tampoco, salvo 4 294 967 s)
  X11 H-11: búsqueda con pause_turn → continuación sin búsqueda (no observa) → reparación sin búsqueda (sí observa); y una
      continuación que falla con timeout entre medias no borra la memoria de la generación
  X12 regla con estados raros (200, negativos) y máximo 0: lo que hace la validación
"""
from __future__ import annotations

import copy
import sys
import types
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
import anthropic  # noqa: E402
import httpx2  # noqa: E402
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.consumo import Contabilidad, Presupuesto, ReservaLlamada  # noqa: E402
from bloque_a.llm import AnthropicClient, ReglaReintentos, Uso, con_guarda, crear_cliente  # noqa: E402

CFG = cargar_config(extra={"modo": "vivo", "perfiles": {"activos": ["DIV"]}, "llm": {"cache_resultados": False}})
CONT = Contabilidad(CFG)
REGLA = ReglaReintentos.de_config(CFG)
SISTEMA = [{"type": "text", "text": "s" * 3600}]
MENSAJES = [{"role": "user", "content": "hola"}]
MODELO = "modelo-de-prueba"
RES: list[tuple[str, str, str]] = []


def informe(caso: str, estado: str, detalle: str) -> None:
    RES.append((caso, estado, detalle))
    print(f"[{estado}] {caso}: {detalle}")


def ok(caso, cond, detalle):
    informe(caso, "OK" if cond else "VIOLA", detalle)


def _mensaje(entrada=1000, salida=200, stop="end_turn", busq=0, texto="ok"):
    u = {"input_tokens": entrada, "output_tokens": salida}
    if busq:
        u["server_tool_use"] = {"web_search_requests": busq}
    return {"id": "msg_qa", "type": "message", "role": "assistant", "model": MODELO,
            "content": [{"type": "text", "text": texto}], "stop_reason": stop, "stop_sequence": None, "usage": u}


class Servidor:
    """Cada petición HTTP toma el siguiente paso del guion: un estado (int), una excepción de httpx2, («200», dict) o 200."""

    def __init__(self, *guion, cabeceras=None):
        self.guion, self.cab, self.n = list(guion), cabeceras or {}, 0

    def __call__(self, req):
        self.n += 1
        paso = self.guion[min(self.n, len(self.guion)) - 1]
        if isinstance(paso, Exception):
            raise paso
        if isinstance(paso, tuple):
            return httpx2.Response(200, json=paso[1])
        if paso == 200:
            return httpx2.Response(200, json=_mensaje())
        return httpx2.Response(paso, headers=self.cab.get(paso, {}),
                               json={"type": "error", "error": {"type": "api_error", "message": "fallo de prueba"}})


def sdk_real(servidor, max_retries=5):
    return anthropic.Anthropic(api_key="clave-falsa-qa", max_retries=max_retries,
                               http_client=httpx2.Client(transport=httpx2.MockTransport(servidor)))


def cliente(servidor, regla=REGLA, esperas=None, dormir=None):
    esperas = [] if esperas is None else esperas
    return AnthropicClient(sdk=sdk_real(servidor), reintentos=regla, dormir=dormir or esperas.append), esperas


class Espia(ReservaLlamada):
    """Cuenta las reservas (una por petición que sale) sin cambiar nada."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.reservas: list[float] = []

    def reservar(self, *a, **k):
        antes = self.peor_total
        mt = super().reservar(*a, **k)
        if mt is not None:
            self.reservas.append(self.peor_total - antes)
        return mt


def guarda(asignado=18.0, cfg=CFG):
    p = Presupuesto({"DIV": asignado}, cfg)
    return p, Espia(p, "DIV", CONT, "AG-05")


def generar(cli, g, herramientas=None, mensajes=MENSAJES):
    """Como `Agentes.invocar` + la cola de `Bloque._invocar`: reserva, genera, paga el resto, carga lo real y cierra."""
    mt = g.reservar(SISTEMA, mensajes, herramientas, 1000)
    if mt is None:
        return None
    with con_guarda(g):
        r = cli.generar(agente="AG-05", modelo=MODELO, system=SISTEMA, mensajes=mensajes, max_tokens=mt,
                        herramientas=herramientas)
    g.pagar_resto(r.uso)
    real = CONT.uc_de(r.uso)
    g.p.cargar(g.bolsa, real)   # `Bloque._cargar` (sin prima de caché: el uso no tiene caché)
    g.cerrar()
    return r, real


# ------------------------------------------------------------------ X1
def x1():
    srv = Servidor(529, 529, 200)
    cli, esperas = cliente(srv)
    p, g = guarda()
    r, real = generar(cli, g)
    ok("X1 SDK real con max_retries=5: el SDK no reintenta y cada reintento reserva", srv.n == 3 and len(g.reservas) == 3
       and cli.sdk.max_retries == 0 and abs(p.consumido["DIV"] - real) < 1e-9 and p.reservado["DIV"] == 0 and not p.sin_respuesta,
       f"peticiones HTTP {srv.n}; reservas {len(g.reservas)}; max_retries del SDK {cli.sdk.max_retries}; esperas {esperas}; "
       f"consumido {p.consumido['DIV']:.4f} = real {real:.4f}; reservado {p.reservado['DIV']}; stop {r.stop_reason}")


# ------------------------------------------------------------------ X2
def x2():
    c1 = AnthropicClient(api_key="clave-falsa-qa", reintentos=REGLA)
    import os
    previo = os.environ.get("ANTHROPIC_API_KEY")
    os.environ["ANTHROPIC_API_KEY"] = "clave-falsa-qa"
    try:
        c2 = crear_cliente("anthropic", CFG)
    finally:
        if previo is None:
            del os.environ["ANTHROPIC_API_KEY"]
        else:
            os.environ["ANTHROPIC_API_KEY"] = previo
    ok("X2 el SDK creado por el cliente sale con max_retries=0", c1.sdk.max_retries == 0 and c2.sdk.max_retries == 0
       and c2.reintentos == REGLA and float(c2.sdk.timeout) == float(CFG["llm"]["timeout_s"]),
       f"AnthropicClient(api_key) {c1.sdk.max_retries}; crear_cliente {c2.sdk.max_retries}; timeout {c2.sdk.timeout}; "
       f"regla {c2.reintentos.maximo} reintentos")


# ------------------------------------------------------------------ X3 y X8
def x3_x8():
    srv = Servidor(httpx2.ReadTimeout("t"), 503, 529, 200)
    cli, esperas = cliente(srv)
    p, g = guarda()
    r, real = generar(cli, g)
    sin = p.sin_respuesta
    cargado_esperado = real + g.reservas[0] + g.reservas[1]
    ok("X3 timeout → 503 → 529 → 200: cargado lo que pudo cobrarse, suelto el 529, nada colgado",
       srv.n == 4 and len(g.reservas) == 4 and len(sin) == 2 and sin[0]["motivo"] == "APITimeoutError"
       and sin[1]["motivo"] != "OverloadedError"
       and abs(p.consumido["DIV"] - cargado_esperado) < 1e-6 and p.reservado["DIV"] == 0 and r.stop_reason == "end_turn",
       f"peticiones {srv.n}; reservas {[round(x, 3) for x in g.reservas]}; sin respuesta {[(s['motivo'], s['peticion'], s['reservado_uc']) for s in sin]}; "
       f"consumido {p.consumido['DIV']:.4f} (real {real:.4f} + {g.reservas[0]:.4f} + {g.reservas[1]:.4f}); reservado {p.reservado['DIV']}; esperas {esperas}")
    ok("X8 el reintento que acaba bien no se cobra dos veces (ni lo real dos veces ni el 529)",
       abs(p.consumido["DIV"] - cargado_esperado) < 1e-6 and len(sin) == 2,
       f"consumido {p.consumido['DIV']:.4f}; esperado {cargado_esperado:.4f}; uso devuelto {r.uso.entrada}/{r.uso.salida}")


# ------------------------------------------------------------------ X4
def x4():
    srv = Servidor(500)
    cli, esperas = cliente(srv)
    p, g = guarda(asignado=100.0)
    r, real = generar(cli, g)
    n = REGLA.maximo + 1
    ok("X4 agotar con 500: max+1 peticiones, todas cargadas, error_proveedor, nada colgado",
       srv.n == n and len(p.sin_respuesta) == n and r.stop_reason == "error_proveedor" and real == 0
       and abs(p.consumido["DIV"] - sum(g.reservas)) < 1e-6 and p.reservado["DIV"] == 0,
       f"peticiones {srv.n} (esperado {n}); cargadas {len(p.sin_respuesta)}; consumido {p.consumido['DIV']:.4f} = "
       f"Σ reservas {sum(g.reservas):.4f}; esperas {esperas}; stop {r.stop_reason}")


# ------------------------------------------------------------------ X5
def x5():
    srv = Servidor(httpx2.ReadTimeout("t"), 200)
    cli, _ = cliente(srv)
    p0, g0 = guarda()
    w = g0._peor(0, 0, 0)  # noqa: F841 (solo para tener la contabilidad caliente)
    mt = g0.reservar(SISTEMA, MENSAJES, None, 1000)
    w1 = g0.peor_total
    g0.cerrar()
    # una bolsa en la que cabe una petición y no dos (límite = asignado × (1 + ampliación sin autorización))
    amp = float(CFG["presupuesto_uc"]["ampliacion_sin_autorizacion"])
    asignado = 1.5 * w1 / (1 + amp)
    p, g = guarda(asignado=asignado)
    r, real = generar(cli, g)
    ok("X5 el reintento que no cabe no sale; lo del timeout queda cargado; el motivo dice «reintento»",
       srv.n == 1 and r.stop_reason == "presupuesto_agotado" and "reintento" in (g.negada or "")
       and abs(p.consumido["DIV"] - w1) < 1e-4 and p.reservado["DIV"] == 0 and len(p.sin_respuesta) == 1,
       f"límite {p.limite('DIV'):.4f}; peor caso {w1:.4f} (mt {mt}); peticiones {srv.n}; stop {r.stop_reason}; negada «{g.negada}»; "
       f"consumido {p.consumido['DIV']:.4f}; reservado {p.reservado['DIV']}")


# ------------------------------------------------------------------ X6
def x6():
    srv = Servidor(400)
    cli, _ = cliente(srv)
    p, g = guarda()
    r, _ = generar(cli, g)
    a = srv.n == 1 and p.consumido["DIV"] == 0 and p.reservado["DIV"] == 0 and not p.sin_respuesta and r.stop_reason == "error_proveedor"

    class Roto:
        def __init__(self):
            self.n, self.messages = 0, self

        def create(self, **kw):
            self.n += 1
            raise TypeError("fallo del código, no del proveedor")
    sdk = Roto()
    cli2 = AnthropicClient(sdk=sdk, reintentos=REGLA, dormir=lambda s: None)
    p2, g2 = guarda()
    r2, _ = generar(cli2, g2)
    b = sdk.n == 1 and p2.consumido["DIV"] == 0 and p2.reservado["DIV"] == 0 and r2.stop_reason == "error_proveedor"
    ok("X6 400 y error ajeno: sin reintento y reserva suelta", a and b,
       f"400: peticiones {srv.n}, consumido {p.consumido['DIV']}, stop {r.stop_reason}; TypeError: llamadas {sdk.n}, "
       f"consumido {p2.consumido['DIV']}, stop {r2.stop_reason}")


# ------------------------------------------------------------------ X7
def x7():
    srv = Servidor(httpx2.ReadTimeout("t"), 200)

    def dormir(s):
        raise KeyboardInterrupt
    cli, _ = cliente(srv, dormir=dormir)
    p, g = guarda()
    mt = g.reservar(SISTEMA, MENSAJES, None, 1000)
    subio = None
    try:
        with con_guarda(g):
            cli.generar(agente="AG-05", modelo=MODELO, system=SISTEMA, mensajes=MENSAJES, max_tokens=mt)
    except BaseException as e:   # la rama de `Bloque._invocar`
        subio = type(e).__name__
        p.cargar("DIV", g.apartado)
        g.cerrar()
    ok("X7 KeyboardInterrupt en la espera: sube, lo del timeout cargado, nada reservado",
       subio == "KeyboardInterrupt" and abs(p.consumido["DIV"] - g.reservas[0]) < 1e-6 and p.reservado["DIV"] == 0,
       f"sube {subio}; consumido {p.consumido['DIV']:.4f} (peor caso del timeout {g.reservas[0]:.4f}); reservado {p.reservado['DIV']}")


# ------------------------------------------------------------------ X9
def x9():
    filas = []
    sdk_dice = {}
    probe = anthropic.Anthropic(api_key="clave-falsa-qa", max_retries=2)
    for estado, cab in ((501, {}), (505, {}), (520, {}), (500, {"x-should-retry": "false"}), (400, {"x-should-retry": "true"})):
        srv = Servidor(estado, 200, cabeceras={estado: cab})
        cli, _ = cliente(srv)
        p, g = guarda()
        r, real = generar(cli, g)
        sdk_dice[estado] = probe._should_retry(httpx2.Response(estado, headers=cab))
        filas.append(f"{estado}{'+' + str(cab) if cab else ''}: peticiones {srv.n}, cargado sin respuesta "
                     f"{len(p.sin_respuesta)}, SDK 2.8 reintentaría {sdk_dice[estado]}")
    informe("X9 5xx fuera de la lista y x-should-retry", "OBS", "; ".join(filas))


# ------------------------------------------------------------------ X10
def x10():
    e = types.SimpleNamespace(response=types.SimpleNamespace(headers={"retry-after": "100000"}))
    e2 = types.SimpleNamespace(response=types.SimpleNamespace(headers={"retry-after-ms": "-5", "retry-after": "nan"}))
    e3 = types.SimpleNamespace(response=types.SimpleNamespace(headers={"retry-after": "Wed, 21 Oct 2015 07:28:00 GMT"}))
    informe("X10 retry-after sin tope", "OBS", f"retry-after 100000 → espera {REGLA.espera(1, e)} s; ms negativo y nan → "
            f"{REGLA.espera(1, e2)} s; fecha → {REGLA.espera(3, e3)} s; reintento 10 → {REGLA.espera(10, e3)} s")


# ------------------------------------------------------------------ X11
def x11():
    web = [{"type": "web_search_20260318", "name": "web_search", "max_uses": 5}]
    entrada_alta = 20000   # mucho más que la medida × factor: si se observara, el factor subiría
    srv = Servidor(("200", _mensaje(entrada=entrada_alta, stop="pause_turn", busq=3)), httpx2.ReadTimeout("t"),
                   ("200", _mensaje(entrada=entrada_alta, stop="end_turn", busq=0)))
    cli, _ = cliente(srv)
    p, g = guarda(asignado=200.0)
    mt = g.reservar(SISTEMA, MENSAJES, web, 1000)
    with con_guarda(g):
        r = cli.generar(agente="AG-05", modelo=MODELO, system=SISTEMA, mensajes=MENSAJES, max_tokens=mt, herramientas=web)
    g.pagar_resto(r.uso)
    f1 = p.factor_observado.get("DIV", 0.0)
    # reparación: otra generación, sin búsquedas, con la misma entrada alta → sí observa
    srv2 = Servidor(("200", _mensaje(entrada=entrada_alta, stop="end_turn", busq=0)))
    cli.sdk = sdk_real(srv2).with_options(max_retries=0)
    msgs = MENSAJES + [{"role": "assistant", "content": "x"}, {"role": "user", "content": "repara"}]
    mt = g.reservar(SISTEMA, msgs, web, 1000)
    with con_guarda(g):
        r2 = cli.generar(agente="AG-05", modelo=MODELO, system=SISTEMA, mensajes=msgs, max_tokens=mt, herramientas=web)
    g.pagar_resto(r2.uso)
    f2 = p.factor_observado.get("DIV", 0.0)
    g.cerrar()
    ok("X11 H-11 con un timeout en la continuación: no observa en la generación que buscó; la reparación sí",
       srv.n == 3 and f1 == 0.0 and f2 > 1.35 and len(p.sin_respuesta) == 1,
       f"peticiones {srv.n}; factor tras la generación {f1:.2f}; tras la reparación {f2:.2f}; sin respuesta {len(p.sin_respuesta)}")


# ------------------------------------------------------------------ X12
def x12():
    filas = []
    for nombre, cambio in (("estados [200]", {"estados_reintentables": [200], "estados_sin_cobro": []}),
                           ("estado negativo", {"estados_reintentables": [-1], "estados_sin_cobro": []}),
                           ("listas vacías", {"estados_reintentables": [], "estados_sin_cobro": []}),
                           ("espera 0", {"espera_inicial_s": 0, "espera_max_s": 0})):
        cfg = copy.deepcopy(CFG)
        cfg["llm"]["reintentos"].update(cambio)
        try:
            ReglaReintentos.de_config(cfg)
            filas.append(f"{nombre}: aceptada")
        except (ValueError, KeyError) as e:
            filas.append(f"{nombre}: {type(e).__name__}")
    cfg = copy.deepcopy(CFG)
    cfg["llm"]["max_reintentos_api"] = 0
    srv = Servidor(529, 200)
    cli, _ = cliente(srv, regla=ReglaReintentos.de_config(cfg))
    p, g = guarda()
    r, _ = generar(cli, g)
    filas.append(f"máximo 0 con 529: peticiones {srv.n}, stop {r.stop_reason}, consumido {p.consumido['DIV']}")
    informe("X12 validación de la regla con valores raros", "OBS", "; ".join(filas))


for caso in (x1, x2, x3_x8, x4, x5, x6, x7, x9, x10, x11, x12):
    caso()
viola = [c for c, e, _ in RES if e == "VIOLA"]
print(f"\n{sum(1 for _, e, _ in RES if e == 'OK')}/{sum(1 for _, e, _ in RES if e != 'OBS')} OK; OBS {sum(1 for _, e, _ in RES if e == 'OBS')}")
sys.exit(1 if viola else 0)
