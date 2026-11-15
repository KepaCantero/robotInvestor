"""QA r01 de T-146 · ataques de unidad a la reserva petición a petición (sin red, sin clave, sin coste).

Uso: python -I r01_01_reserva_unidad.py <ruta a 11_Ejecutor>
Cada caso imprime OK (el invariante se cumple) o VIOLA (no se cumple) con las cifras. No cambia nada del repo.

Casos:
  U1  hilos que reservan a la vez sobre la misma bolsa (Presupuesto.reservar): nunca pasa del límite
  U2  la ventana entre `cerrar` (suelta lo reservado) y `_cargar` (carga lo real) con dos llamadas de la misma bolsa en hilos
  U3  lo que lee una búsqueda (entrada de la misma petición): la bolsa pasa de su límite
  U4  lo que lee una búsqueda sube el factor observado de la bolsa: la siguiente petición sin búsqueda reserva varias veces más
  U5  tokenizador peor que 1,35 × (3,6 caracteres por token): exceso y bolsa por encima de su límite
  U6  continuaciones de pause_turn con el cliente real: cada una reserva antes de salir; la que no cabe no sale
  U7  reparación que no cabe tras un primer intento pagado: no sale, lo pagado se carga
  U8  parámetros límite en la configuración (factor 0, NaN, salida mínima 0): ¿falla cerrado?
  U9  excepción a mitad de una llamada (JSON muy anidado en la reparación): lo ya pagado no llega a la bolsa
"""
from __future__ import annotations

import copy
import json
import sys
import threading
import time
import types
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
sys.path.insert(0, str(EJ / "tests"))
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.consumo import Contabilidad, Presupuesto, ReservaLlamada, tokens_de_peticion  # noqa: E402
from bloque_a.llm import AnthropicClient, Uso, con_guarda  # noqa: E402

CFG = cargar_config(extra={"modo": "vivo"})
CONT = Contabilidad(CFG)
WEB = [{"type": "web_search_20260318", "name": "web_search", "max_uses": 5}]
RES: list[tuple[str, bool, str]] = []


def informe(caso: str, ok: bool, detalle: str) -> None:
    RES.append((caso, ok, detalle))
    print(f"[{'OK' if ok else 'VIOLA'}] {caso}: {detalle}")


def sistema(n_car: int) -> list[dict]:
    return [{"type": "text", "text": "x" * n_car, "cache_control": {"type": "ephemeral"}}]


def mensajes(n_car: int) -> list[dict]:
    return [{"role": "user", "content": "y" * n_car}]


# ------------------------------------------------------------------ U1
def u1() -> None:
    p = Presupuesto({"RV": 18.0}, CFG)
    lim = p.limite("RV")
    hechos = []
    barrera = threading.Barrier(32)

    def trabajo():
        barrera.wait()
        for _ in range(50):
            if p.reservar("RV", 0.37):
                hechos.append(1)
    hs = [threading.Thread(target=trabajo) for _ in range(32)]
    for h in hs:
        h.start()
    for h in hs:
        h.join()
    ocupado = p.reservado["RV"]
    informe("U1 reservas concurrentes", ocupado <= lim + 1e-9, f"reservado {ocupado:.4f} con límite {lim:.4f} ({len(hechos)} reservas)")


# ------------------------------------------------------------------ U2
def u2() -> None:
    """Reproduce el orden de `Bloque._invocar`: reservar → petición → pagar_resto → cerrar → cargar. Si dos llamadas de la
    misma bolsa corren en hilos, la otra puede reservar entre `cerrar` y `cargar`. En el ejecutor de hoy cada bolsa la usa un
    solo hilo (las de tipo en su hilo; COMÚN y la del ciclo V6 en el principal), así que es un riesgo latente."""
    p = Presupuesto({"RV": 4.0}, CFG)   # límite 5 UC
    lim = p.limite("RV")
    sis, msg = sistema(3600 * 4), mensajes(3600)   # ≈ 5 000 tokens × 1,35
    paso = threading.Event()
    sigue = threading.Event()

    def llamada(espera: bool):
        g = ReservaLlamada(p, "RV", CONT, "AG-03")
        mt = g.reservar(sis, msg, None, 12000)   # ≈ 4,4 UC: en un límite de 5 solo cabe una a la vez
        if mt is None:
            return
        uso = Uso(entrada=0, cache_escritura=int(5000 * 1.35), salida=mt)
        g.pagar_resto(uso)
        g.cerrar()
        if espera:
            paso.set()
            sigue.wait(2)
        p.cargar("RV", CONT.uc_de(uso))

    a = threading.Thread(target=llamada, args=(True,))
    a.start()
    paso.wait(2)
    b = threading.Thread(target=llamada, args=(False,))
    b.start()
    b.join()
    sigue.set()
    a.join()
    c = p.consumido["RV"]
    informe("U2 ventana cerrar→cargar (latente: hoy no hay dos hilos en una bolsa)", c <= lim + 1e-9,
            f"consumido {c:.4f} con límite {lim:.4f}")


# ------------------------------------------------------------------ U3 y U4
def u3_u4() -> None:
    p = Presupuesto({"RV": 18.0}, CFG)   # límite 22,5
    lim = p.limite("RV")
    p.cargar("RV", lim - 4.0)            # quedan 4 UC
    sis, msg = sistema(3600 * 6), mensajes(3600 * 2)   # ≈ 8 000 tokens brutos
    g = ReservaLlamada(p, "RV", CONT, "AG-14")
    mt = g.reservar(sis, msg, WEB, 3000)
    reservado = g.peor_total
    bruto = tokens_de_peticion(sis, msg, WEB)
    # la API cobra como entrada lo que traen las 5 búsquedas (p. ej. 5 × 6 000 tokens) en la misma petición
    uso = Uso(cache_escritura=bruto, entrada=5 * 6000, salida=mt or 0, busquedas_web=5)
    g.pagar_resto(uso)
    g.cerrar()
    p.cargar("RV", CONT.uc_de(uso))
    c = p.consumido["RV"]
    informe("U3 lectura de búsquedas en la misma petición", c <= lim + 1e-9,
            f"reservado {reservado:.3f} UC, real {CONT.uc_de(uso):.3f} UC; consumido {c:.3f} con límite {lim:.3f} "
            f"(excesos anotados: {len(p.excesos)})")
    # U4: la siguiente petición de la bolsa, sin búsqueda, con el mismo tamaño
    q = Presupuesto({"RV": 18.0}, CFG)
    g1 = ReservaLlamada(q, "RV", CONT, "AG-14")
    g1.reservar(sis, msg, WEB, 3000)
    g1.pagar_resto(Uso(cache_escritura=bruto, entrada=5 * 6000, salida=3000, busquedas_web=5))
    g1.cerrar()
    antes = ReservaLlamada(Presupuesto({"RV": 18.0}, CFG), "RV", CONT, "AG-10")
    antes.reservar(sis, msg, None, 3000)
    despues = ReservaLlamada(q, "RV", CONT, "AG-10")
    despues.reservar(sis, msg, None, 3000)
    informe("U4 una búsqueda sube el factor de toda la bolsa", despues.peor_total <= antes.peor_total * 1.05,
            f"factor observado {q.factor_observado.get('RV', 0):.2f}; peor caso de la misma petición sin búsqueda "
            f"{antes.peor_total:.3f} UC en una bolsa limpia y {despues.peor_total:.3f} UC tras la búsqueda")


# ------------------------------------------------------------------ U5
def u5() -> None:
    p = Presupuesto({"RV": 18.0}, CFG)
    lim = p.limite("RV")
    sis, msg = sistema(3600 * 40), mensajes(3600 * 10)   # ≈ 50 000 tokens brutos
    bruto = tokens_de_peticion(sis, msg, None)
    total = 0
    for i in range(20):
        g = ReservaLlamada(p, "RV", CONT, "AG-03")
        mt = g.reservar(sis, msg, None, 12000)
        if mt is None:
            break
        uso = Uso(cache_escritura=int(bruto * 1.8), salida=mt)   # JSON con cifras: ≈ 2 caracteres por token
        g.pagar_resto(uso)
        g.cerrar()
        p.cargar("RV", CONT.uc_de(uso))
        total += 1
    c = p.consumido["RV"]
    informe("U5 tokenizador 1,8 × la aproximación", c <= lim + 1e-9,
            f"{total} peticiones; consumido {c:.3f} con límite {lim:.3f}; excesos {len(p.excesos)}; factor observado "
            f"{p.factor_observado.get('RV', 0):.2f}")


# ------------------------------------------------------------------ SDK falso para U6, U7 y U9
class SDK:
    def __init__(self, respuestas):
        self.respuestas = list(respuestas)
        self.n = 0
        self.messages = self

    def create(self, **kw):
        self.n += 1
        stop, texto, uso = self.respuestas.pop(0)
        uso = dict(uso, output_tokens=min(uso["output_tokens"], int(kw["max_tokens"])))   # la API nunca pasa de max_tokens
        if uso["cache_creation_input_tokens"] == "auto":   # la entrada de la petición con el margen 1,35 (lo que se reserva)
            uso["cache_creation_input_tokens"] = int(tokens_de_peticion(kw["system"], kw["messages"], kw.get("tools")) * 1.35)
        return types.SimpleNamespace(stop_reason=stop, usage=types.SimpleNamespace(**uso),
                                     content=[types.SimpleNamespace(type="text", text=texto)])


def uso_api(ent, sal, busq=0):
    return {"input_tokens": 0, "output_tokens": sal, "cache_creation_input_tokens": ent, "cache_read_input_tokens": 0,
            "server_tool_use": types.SimpleNamespace(web_search_requests=busq)}


def u6() -> None:
    p = Presupuesto({"RV": 4.0}, CFG)   # límite 5 UC
    lim = p.limite("RV")
    sis, msg = sistema(3600 * 8), mensajes(3600)
    sdk = SDK([("pause_turn", "a" * 36000, uso_api(12150, 10000, 5))] * 6)
    cli = AnthropicClient(sdk=sdk, max_continuaciones=3)
    g = ReservaLlamada(p, "RV", CONT, "AG-14")
    mt = g.reservar(sis, msg, WEB, 10000)
    with con_guarda(g):
        r = cli.generar(agente="AG-14", modelo="m", system=sis, mensajes=msg, max_tokens=mt, herramientas=WEB)
    g.pagar_resto(r.uso)
    g.cerrar()
    p.cargar("RV", CONT.uc_de(r.uso))
    c = p.consumido["RV"]
    informe("U6 continuaciones de pause_turn", c <= lim + 1e-9 and r.stop_reason == "presupuesto_agotado",
            f"peticiones {sdk.n}, stop {r.stop_reason}, consumido {c:.3f} con límite {lim:.3f}")


def _bloque_con(cliente, cfg=None):
    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
    from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
    from bloque_a.orquestacion import Bloque
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="qa19_r01_"))
    return Bloque(cfg or CFG, ProveedorCSV(EJ / "ejemplos" / "datos_sinteticos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO),
                  cliente, tmp / "estado", tmp / "ent"), tmp


def u7() -> None:
    cfg = copy.deepcopy(CFG)
    cfg["llm"]["cache_resultados"] = False
    ok_json = "{}"
    sdk = SDK([("end_turn", "no es json " * 3000, uso_api("auto", 8000)), ("end_turn", ok_json, uso_api("auto", 100))])
    b, tmp = _bloque_con(AnthropicClient(sdk=sdk), cfg)
    sis = b.agentes.prompts.system("AG-12", True, "1h")
    n = tokens_de_peticion(sis, [{"role": "user", "content": "z" * 20000}], None)
    peor1 = CONT.uc_de(Uso(entrada=int(n * 1.35) + 1, salida=8000))
    p = Presupuesto({"RV": (peor1 + 0.3) / 1.25}, cfg)   # cabe la primera, no la reparación
    lim = p.limite("RV")
    r = b._invocar("AG-12", "CT-11", {"x": "z" * 20000}, "CURACION", "Clasifica.", "2024-03-29", "RUN-QA", "RV", "investigacion",
                   p, permitir_web=False)
    p.liquidar_primas()
    gastado = sum(x["uc"] for x in b.contabilidad.llamadas)
    c = p.consumido["RV"]
    informe("U7 reparación que no cabe", sdk.n == 1 and abs(c - gastado) < 1e-3 and bool(p.cierres),
            f"peticiones {sdk.n}, estado {getattr(r, 'estado', r)}, consumido {c:.3f} (gastado {gastado:.3f}) límite {lim:.3f}, "
            f"cierres {len(p.cierres)}")


def u8() -> None:
    sis, msg = sistema(3600 * 8), mensajes(3600)
    for nombre, cambio in (("factor 0", ("factor_tokens_entrada", 0.0)), ("factor NaN", ("factor_tokens_entrada", float("nan"))),
                           ("factor -1", ("factor_tokens_entrada", -1.0)), ("salida mínima 0", ("salida_minima_tokens", 0))):
        cfg = copy.deepcopy(CFG)
        cfg["presupuesto_uc"]["reserva"][cambio[0]] = cambio[1]
        p = Presupuesto({"RV": 0.5}, cfg)
        try:
            g = ReservaLlamada(p, "RV", CONT, "AG-03")
            mt = g.reservar(sis, msg, None, 12000)
            sale = mt is not None
            informe(f"U8 {nombre}", not sale or (mt and mt > 0 and g.peor_total >= CONT.uc_de(Uso(entrada=tokens_de_peticion(sis, msg, None), salida=mt)) - 1e-9),
                    f"sale con max_tokens {mt}, reservado {g.peor_total:.3f} UC (límite {p.limite('RV'):.3f})")
        except Exception as e:   # noqa: BLE001
            informe(f"U8 {nombre}", True, f"falla cerrado con {type(e).__name__}: {e}")


def u9() -> None:
    cfg = copy.deepcopy(CFG)
    cfg["llm"]["cache_resultados"] = False
    anidado = "[" * 200000 + "]" * 200000
    sdk = SDK([("end_turn", "no es json", uso_api("auto", 8000)), ("end_turn", anidado, uso_api("auto", 100))])
    b, tmp = _bloque_con(AnthropicClient(sdk=sdk), cfg)
    p = Presupuesto({"RV": 18.0}, cfg)
    try:
        b._invocar("AG-12", "CT-11", {"x": 1}, "CURACION", "Clasifica.", "2024-03-29", "RUN-QA", "RV", "investigacion", p)
        exc = None
    except BaseException as e:   # noqa: BLE001
        exc = type(e).__name__
    p.liquidar_primas()
    gastado = sum(x["uc"] for x in b.contabilidad.llamadas)
    informe("U9 excepción a mitad de llamada", exc is None and abs(p.consumido["RV"] - gastado) < 1e-3,
            f"excepción {exc}; peticiones {sdk.n}; gastado según la contabilidad {gastado:.3f} UC; cargado en la bolsa "
            f"{p.consumido['RV']:.3f}; reservado que queda {p.reservado['RV']:.3f}")


for f in (u1, u2, u3_u4, u5, u6, u7, u8, u9):
    t0 = time.perf_counter()
    try:
        f()
    except Exception as e:   # noqa: BLE001
        informe(f.__name__, False, f"el ataque falló: {type(e).__name__}: {e}")
print(f"\n{sum(ok for _, ok, _ in RES)}/{len(RES)} OK")
