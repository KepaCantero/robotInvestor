"""QA r01 de T-154 · ataques de unidad a H-01, H-03 y H-04 (sin red, sin clave, sin coste: el SDK real sobre un transporte
falso y SDK dobles).

Uso: python -I r01_01_unidad_t154.py <ruta a 11_Ejecutor>

Qué comprueba (FALLA si no):
  U01 H-01: matriz de estados (500…600, 4xx) × `x-should-retry` (ausente, true, false, « False », basura): (reintenta, cobro)
      = lo que dicen el README e INC-T146-01 (todo ≥ 500 salvo 529 se cobra, se reintente o no; un 4xx solo si se reintenta).
  U02 H-01 de punta a punta con el SDK real: cada petición fallida que pudo cobrarse se carga UNA vez (consumido = suma de
      `peticiones_sin_respuesta`), la que no, se suelta; ninguna reserva colgada; el número de peticiones HTTP = reservas.
  U03 H-04: bordes de la espera del servidor (tope exacto, tope + ε, ms, espacios, «+5», `1e400`, prioridad de `-ms`).
  U04 H-04 de punta a punta: un 503 y un 529 con `retry-after` mayor que el tope: no se duerme, `error_proveedor`, el 503 se
      carga una vez y el 529 se suelta; un tope 0 no reintenta nada que traiga `retry-after`.
  U05 H-03: 200 órdenes aleatorios (semilla fija) de las llamadas de 4 bolsas a dos grupos (AG-14 y ANALISTAS en V6), con la
      petición sin respuesta que escribe el prefijo en cualquier posición: con la marca, lo consumido es idéntico en todos;
      ninguna bolsa ocupa más tras liquidar que antes (consumido + reservado + retenido no sube); la marca es idempotente.
  U06 T-146 × T-154: el factor observado tras un reintento es el mismo que sin el fallo, y la marca no lo toca.
  U07 H-02: cada lista por separado (solo un cierre, solo un recorte, solo un exceso, solo una petición sin respuesta) tras la
      marca basta para que haya entrada F9, y solo con lo nuevo.
  OBS: lo que no rompe un criterio (validación de `cobro_posible_desde`, sobrecarga de H-03 frente a lo escrito).
"""
from __future__ import annotations

import random
import sys
import types
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
sys.path.insert(0, str(EJ / "tests"))
import anthropic  # noqa: E402
import httpx2  # noqa: E402
from bloque_a.configuracion import cargar_config, fusionar  # noqa: E402
from bloque_a.consumo import Contabilidad, Presupuesto, ReservaLlamada  # noqa: E402
from bloque_a.llm import AnthropicClient, ReglaReintentos, Uso, clasificar_error, con_guarda  # noqa: E402
from bloque_a.orquestacion import Bloque, grupo_primas  # noqa: E402

FALLOS: list[str] = []
REQ = httpx2.Request("POST", "https://api.invalid/v1/messages")
SISTEMA = [{"type": "text", "text": "s" * 3600}]
MENSAJES = [{"role": "user", "content": "hola"}]


def cfg_(**extra):
    return cargar_config(extra=fusionar({"modo": "vivo", "perfiles": {"activos": ["DIV"]}}, extra))


def check(nombre, ok, detalle=""):
    print(("OK   " if ok else "FALLA") + f" {nombre}" + (f" · {detalle}" if detalle else ""))
    if not ok:
        FALLOS.append(nombre)


def estado(n, cab=None):
    return anthropic.APIStatusError("x", response=httpx2.Response(n, request=REQ, headers=cab or {}), body=None)


CFG = cfg_()
REGLA = ReglaReintentos.de_config(CFG)
SIN_COBRO = set(CFG["llm"]["reintentos"]["estados_sin_cobro"])
ESTADOS = set(CFG["llm"]["reintentos"]["estados_reintentables"])
DESDE = CFG["llm"]["reintentos"]["cobro_posible_desde"]

# ---------------------------------------------------------------- U01
malos = []
for st in [400, 404, 408, 409, 422, 429, 499, 500, 501, 502, 503, 504, 505, 507, 511, 520, 529, 530, 599, 600]:
    for x in (None, "true", "false", " False ", "TRUE", "quiza"):
        cab = {} if x is None else {"X-Should-Retry": x}
        pide = (x or "").strip().lower()
        rein = pide == "true" or (pide != "false" and st in ESTADOS)
        cobro = (st not in SIN_COBRO) if st >= DESDE else (rein and st not in SIN_COBRO)
        got = clasificar_error(estado(st, cab), REGLA)
        if got != (rein, cobro):
            malos.append((st, x, got, (rein, cobro)))
check("U01 matriz de estados × x-should-retry", not malos, f"{len(malos)} discrepancias {malos[:4]}")
check("U01 el 500 con x-should-retry false es (False, True): se carga, no se reintenta",
      clasificar_error(estado(500, {"x-should-retry": "false"}), REGLA) == (False, True))


# ---------------------------------------------------------------- U02
def _msg():
    return {"id": "m", "type": "message", "role": "assistant", "model": "modelo-de-prueba",
            "content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "stop_sequence": None,
            "usage": {"input_tokens": 100, "output_tokens": 50}}


class Srv:
    def __init__(self, *guion, cab=None):
        self.guion, self.cab, self.n = list(guion), cab or {}, 0

    def __call__(self, req):
        self.n += 1
        paso = self.guion[min(self.n, len(self.guion)) - 1]
        if paso == 200:
            return httpx2.Response(200, json=_msg())
        return httpx2.Response(paso, headers=self.cab, json={"type": "error", "error": {"type": "api_error", "message": "x"}})


class Espia(ReservaLlamada):
    abiertas = 0

    def _abrir(self, w, bruto, mt):
        Espia.abiertas += 1
        return super()._abrir(w, bruto, mt)


def correr(srv, cfg=None):
    cfg = cfg or CFG
    esperas: list[float] = []
    sdk = anthropic.Anthropic(api_key="clave-falsa-qa", max_retries=7, http_client=httpx2.Client(transport=httpx2.MockTransport(srv)))
    cli = AnthropicClient(sdk=sdk, reintentos=ReglaReintentos.de_config(cfg), dormir=esperas.append)
    p = Presupuesto({"DIV": 100.0}, cfg)
    Espia.abiertas = 0
    g = Espia(p, "DIV", Contabilidad(cfg), "AG-05")
    mt = g.reservar(SISTEMA, MENSAJES, None, 1000)
    with con_guarda(g):
        r = cli.generar(agente="AG-05", modelo="modelo-de-prueba", system=SISTEMA, mensajes=MENSAJES, max_tokens=mt)
    g.pagar_resto(r.uso)
    g.cerrar()
    return r, p, esperas, Espia.abiertas


maximo = REGLA.maximo
casos = [((501,), 1, 1), ((520,), 1, 1), ((503,), maximo + 1, maximo + 1), ((529,), maximo + 1, 0), ((429,), maximo + 1, 0),
         ((503, 529, 503, 200), 4, 2), ((500, 200), 2, 1), ((400,), 1, 0), ((408, 200), 2, 1)]
for guion, peticiones, cobradas in casos:
    srv = Srv(*guion, cab={"retry-after": "0"})
    r, p, esperas, abiertas = correr(srv)
    peor = sum(s["reservado_uc"] for s in p.sin_respuesta)
    real = p.consumido["DIV"] - peor
    ok = (srv.n == peticiones and len(p.sin_respuesta) == cobradas and abs(p.reservado["DIV"]) < 1e-9 and abiertas == srv.n
          and abs(real) < 1e-3)   # sin `Bloque._cargar` (unidad): en la bolsa solo queda lo cargado sin respuesta, una vez cada una
    check(f"U02 guion {guion}", ok, f"peticiones {srv.n}/{peticiones} reservas {abiertas} sin respuesta {len(p.sin_respuesta)}/{cobradas} "
          f"consumido {p.consumido['DIV']:.4f} (peor {peor:.4f}) reservado {p.reservado['DIV']:.2e} fin {r.stop_reason}")

# ---------------------------------------------------------------- U03
tope = REGLA.espera_servidor_max_s


def con(h):
    return types.SimpleNamespace(response=types.SimpleNamespace(headers=h))


bordes = [({"retry-after": str(tope)}, tope), ({"retry-after": repr(tope + 1e-6)}, None), ({"retry-after-ms": str(tope * 1000)}, tope),
          ({"retry-after-ms": str(tope * 1000 + 1)}, None), ({"retry-after": " 5 "}, 5.0), ({"retry-after": "+5"}, 5.0),
          ({"retry-after": "1e400"}, REGLA.espera_inicial_s), ({"retry-after": "-0"}, REGLA.espera_inicial_s),
          ({"Retry-After-Ms": "nan", "RETRY-AFTER": "7"}, 7.0), ({"retry-after": "0x10"}, REGLA.espera_inicial_s),
          (httpx2.Headers({"Retry-After": "3"}), 3.0)]
for h, esperado in bordes:
    got = REGLA.espera(1, con(h))
    check(f"U03 espera {dict(h)}", got == esperado, f"{got} (esperado {esperado})")
got = REGLA.espera(1, con({"retry-after-ms": str((tope + 1) * 1000), "retry-after": "1"}))
print(f"OBS  U03 `retry-after-ms` por encima del tope con `retry-after` 1: {got} (manda -ms, como en el SDK: no se reintenta)")

# ---------------------------------------------------------------- U04
for st, cobradas in ((503, 1), (529, 0), (500, 1)):
    srv = Srv(st, 200, cab={"retry-after": str(tope * 10)})
    r, p, esperas, abiertas = correr(srv)
    check(f"U04 {st} con retry-after ×10 del tope", r.stop_reason == "error_proveedor" and srv.n == 1 and not esperas
          and len(p.sin_respuesta) == cobradas and abs(p.reservado["DIV"]) < 1e-9,
          f"fin {r.stop_reason} peticiones {srv.n} esperas {esperas} sin respuesta {len(p.sin_respuesta)}")
cero = cfg_(llm={"reintentos": {"espera_servidor_max_s": 0}})
srv = Srv(503, 200, cab={"retry-after": "1"})
r, p, esperas, _ = correr(srv, cero)
check("U04 tope 0: un retry-after positivo no se reintenta", r.stop_reason == "error_proveedor" and srv.n == 1, f"{r.stop_reason} {srv.n}")
srv = Srv(503, 200)
r, p, esperas, _ = correr(srv, cero)
check("U04 tope 0: sin retry-after, la espera de la regla", r.stop_reason == "end_turn" and srv.n == 2 and esperas == [REGLA.espera_inicial_s])

# ---------------------------------------------------------------- U05
PREF = 20000


def reparto(orden, marca, v6):
    """`orden`: lista de (bolsa, agente, falla). El servidor escribe el prefijo de un grupo la primera vez que lo ve; la petición
    que falla también lo escribe (nadie lo ve) y, tras ella, su reintento lee."""
    cfg = CFG
    fake = types.SimpleNamespace(contabilidad=Contabilidad(cfg), v6=v6)
    p = Presupuesto({"DIV": 50.0, "MP": 50.0, "RV": 50.0, "RF": 50.0, "COMUN": 50.0}, cfg)
    vistos = set()
    for bolsa, agente, falla in orden:
        g = grupo_primas(v6, agente)
        if falla:
            vistos.add(g)   # la fallida escribió; su reintento lee
            if marca:
                p.grupo_sin_respuesta(g)
            u = Uso(entrada=500, salida=100, cache_lectura=PREF)
        elif g in vistos:
            u = Uso(entrada=500, salida=100, cache_lectura=PREF)
        else:
            vistos.add(g)
            u = Uso(entrada=500, salida=100, cache_escritura=PREF)
        r = types.SimpleNamespace(uso=u, cache_hit=False, intentos=1, uc=0.0)
        Bloque._cargar(fake, p, bolsa, agente, r, prefijo=PREF)
    antes = {k: p.consumido[k] + p.reservado[k] + p.retenido[k] for k in p.asignado}
    p.liquidar_primas()
    despues = {k: p.consumido[k] + p.reservado[k] + p.retenido[k] for k in p.asignado}
    return {k: round(v, 9) for k, v in p.consumido.items()}, antes, despues


rnd = random.Random(20261115)
for v6 in (False, True):
    base = [("DIV", "AG-14", False), ("MP", "AG-14", False), ("RV", "AG-14", False), ("RF", "AG-14", False),
            ("DIV", "AG-05" if not v6 else "AG-05", False), ("MP", "AG-07", False), ("RV", "AG-03", False), ("RF", "AG-04", False)]
    for marca in (True, False):
        firmas, sube = set(), []
        for k in range(200):
            orden = list(base)
            i = rnd.randrange(len(orden))
            orden[i] = (orden[i][0], orden[i][1], True)   # la llamada que tiene la petición sin respuesta
            orden_fijo = orden[i]
            for o in (orden, list(reversed(orden))):
                rnd.shuffle(o)
                c, antes, despues = reparto(o, marca, v6)
                firmas.add((orden_fijo, tuple(sorted(c.items()))))
                sube += [(b, antes[b], despues[b]) for b in antes if despues[b] > antes[b] + 1e-9]
        por_fallo: dict = {}
        for f, c in firmas:
            por_fallo.setdefault(f, set()).add(c)
        distintos = sum(len(v) > 1 for v in por_fallo.values())
        if marca:
            check(f"U05 v6={v6} con la marca: mismo reparto en cualquier orden", distintos == 0, f"{distintos} llamadas fallidas con >1 reparto")
            check(f"U05 v6={v6} con la marca: ninguna bolsa ocupa más tras liquidar", not sube, f"{sube[:3]}")
        else:
            print(f"OBS  U05 v6={v6} sin la marca (antes de T-154): {distintos} de {len(por_fallo)} llamadas fallidas dan >1 reparto")
p = Presupuesto({"DIV": 5.0}, CFG)
p.grupo_sin_respuesta("AG-14")
p.grupo_sin_respuesta("AG-14")
p.liquidar_primas()
check("U05 marca idempotente y limpia tras liquidar, sin pesos no carga nada", not p._grupos_sin_respuesta and p.consumido["DIV"] == 0)
# la sobrecarga de H-03: lo cargado de más frente al reparto de lo escrito (con la fallida que escribe primero)
c_m, _, _ = reparto([("DIV", "AG-14", True), ("MP", "AG-14", False), ("RV", "AG-14", False)], True, False)
c_s, _, _ = reparto([("DIV", "AG-14", False), ("MP", "AG-14", False), ("RV", "AG-14", False)], False, False)
extra = sum(c_m.values()) - sum(c_s.values())
print(f"OBS  U05 sobrecarga de un grupo marcado (3 bolsas, prefijo {PREF} tokens): {extra:.4f} UC más que sin fallo "
      f"(= 2 primas «solo», {2 * p._uc_prima(PREF):.4f}); el peor caso de la fallida ya cuenta su entrada como escrita")


# ---------------------------------------------------------------- U06
class SDKFactor:
    """La API cuenta 1,6 veces la estimación (el factor se observa); `fallos` peticiones con 503 antes."""

    def __init__(self, fallos):
        self.messages, self.fallos = self, fallos

    def create(self, **kw):
        if self.fallos:
            self.fallos -= 1
            raise anthropic.APIStatusError("x", response=httpx2.Response(503, request=REQ), body=None)
        from bloque_a.consumo import tokens_de_peticion
        ent = int(tokens_de_peticion(kw["system"], kw["messages"], kw.get("tools")) * 1.6)
        uso = types.SimpleNamespace(input_tokens=ent, output_tokens=50, cache_creation_input_tokens=0, cache_read_input_tokens=0,
                                    server_tool_use=None)
        return types.SimpleNamespace(stop_reason="end_turn", usage=uso, content=[types.SimpleNamespace(type="text", text="ok")])


factores = []
for fallos in (0, 1, 2):
    cli = AnthropicClient(sdk=SDKFactor(fallos), reintentos=REGLA, dormir=lambda s: None)
    p = Presupuesto({"DIV": 100.0}, CFG)
    g = ReservaLlamada(p, "DIV", Contabilidad(CFG), "AG-05")
    mt = g.reservar(SISTEMA, MENSAJES, None, 1000)
    with con_guarda(g):
        r = cli.generar(agente="AG-05", modelo="modelo-de-prueba", system=SISTEMA, mensajes=MENSAJES, max_tokens=mt)
    g.pagar_resto(r.uso)
    g.cerrar()
    p.grupo_sin_respuesta("AG-05")
    p.liquidar_primas()
    factores.append((round(p.factor_observado.get("DIV", 0), 6), len(p.sin_respuesta), abs(p.reservado["DIV"]) < 1e-9))
check("U06 factor observado igual con 0, 1 y 2 reintentos; sin reservas colgadas",
      len({f[0] for f in factores}) == 1 and factores[0][0] > 1.35 and all(f[2] for f in factores) and [f[1] for f in factores] == [0, 1, 2],
      f"{factores}")

# ---------------------------------------------------------------- U07
ENTRADAS = {"cierres": {"clase": "COMUN", "fase": "CT-17", "motivo": "presupuesto insuficiente para AG-19"},
            "recortes": {"clase": "COMUN", "agente": "AG-19", "peticion": 1, "max_tokens": 9, "max_tokens_enviado": 8,
                         "peor_caso_uc": 1.0, "reservado_uc": 0.9},
            "excesos": {"clase": "COMUN", "agente": "AG-19", "reservado_uc": 1.0, "real_uc": 1.5, "busquedas_web": 0},
            "sin_respuesta": {"clase": "COMUN", "agente": "AG-19", "peticion": 1, "reservado_uc": 1.0, "motivo": "APITimeoutError"}}
for lista, entrada in ENTRADAS.items():
    p = Presupuesto({"COMUN": 5.0}, CFG)
    for otra, e in ENTRADAS.items():   # lo de antes de la marca (el RUN) no cuenta
        p.anotar(otra, dict(e))
    marca = p.marca()
    vacio = p.desde(marca)
    p.anotar(lista, dict(entrada))
    tramo = p.desde(marca)
    f5 = Bloque._f5_presupuesto(tramo)
    clave = {"cierres": "cierres_parciales", "recortes": "recortes_salida", "excesos": "excesos_reserva",
             "sin_respuesta": "peticiones_sin_respuesta"}[lista]
    check(f"U07 H-02 solo {lista} tras la marca: hay algo que declarar y solo eso", not vacio.algo() and tramo.algo()
          and len(f5.get(clave, [])) == 1 and all(len(f5.get(k) or []) == 0 for k in
                                                  ("cierres_parciales", "recortes_salida", "excesos_reserva", "peticiones_sin_respuesta")
                                                  if k != clave), f"{ {k: len(v) for k, v in f5.items() if isinstance(v, list)} }")

# ---------------------------------------------------------------- OBS de configuración
for v in (0, 100, 599, 600, 10 ** 6):
    try:
        ReglaReintentos.de_config(cfg_(llm={"reintentos": {"cobro_posible_desde": v}}))
        print(f"OBS  cobro_posible_desde={v}: se acepta")
    except ValueError as e:
        print(f"OBS  cobro_posible_desde={v}: {e}")

print("RESULTADO:", "FALLA " + ", ".join(FALLOS) if FALLOS else "todo OK")
sys.exit(1 if FALLOS else 0)
