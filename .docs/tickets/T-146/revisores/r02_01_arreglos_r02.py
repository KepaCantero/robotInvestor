"""QA r02 de T-146 · ataques a los arreglos de la r02 (sin red, sin clave, sin coste).

Uso: python -I r02_01_arreglos_r02.py <ruta a 11_Ejecutor> <carpeta temporal>
Cada caso imprime OK (el invariante se cumple) o VIOLA (no se cumple) con las cifras. No cambia nada del repo (escribe solo en
la carpeta temporal). Contra el código de la r01 (`b0046a1`) deben dar VIOLA al menos R1 y R4.

Casos:
  R1  H-08 por el camino real (`Bloque._invocar`): dos llamadas de la misma bolsa en hilos; la segunda intenta reservar justo
      después de que la primera suelte lo apartado
  R2  H-04: `presupuesto_uc.reserva.tokens_lectura_por_busqueda` reserva lo que lee cada búsqueda; si lee más, lo que la bolsa
      pasa de su límite no es mayor que lo anotado en `excesos_reserva`; negativo, NaN, texto o nulo fallan cerrado (ausente: el de por_defecto.yaml)
  R3  H-01: lo que leen las búsquedas no sube el factor; el tokenizador peor sí se observa en una petición sin búsquedas o con
      la herramienta y 0 búsquedas
  R4  H-02: la misma petición pagada con el prefijo leído o escrito deja la bolsa igual (apartado, disponible y la decisión de
      la reparación)
  R5  H-05: la llamada se cae (BaseException que el cliente no captura) después de una petición pagada, en la primera
      petición o al registrar el segundo intento: lo pagado queda en la bolsa, nada reservado y la excepción sube
  R6  H-03: la bolsa de C5 (`_comun_minimo_c5`) nunca pasa de la base de COMÚN del reparto real, en todos los niveles posibles
      (periódico con N1 > N2, N3 forzado, profundización, overrides, alcance parcial, V6)
  R7  todo lo gastado está en las bolsas cuando el ciclo no tiene ningún tipo que analizar (alcance con un tipo no activo):
      AG-20 gasta antes y F5 no lo registra en ninguna bolsa
  R8  la salvedad del CA-1 («después no sale ninguna más de esa bolsa»): una petición que pasa del límite actual sin llegar
      al máximo, y la siguiente de una fase que admite ampliación; y que por encima del máximo solo queda un exceso
"""
from __future__ import annotations

import copy
import itertools
import json
import sys
import threading
import types
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
TMP = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(EJ))
from bloque_a import mock_respuestas  # noqa: E402
from bloque_a.agentes import ResultadoAgente  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.consumo import Contabilidad, Presupuesto, ReservaLlamada, tokens_de_peticion  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import AnthropicClient, MockClient, Uso  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

CFG = cargar_config(extra={"modo": "vivo", "llm": {"cache_resultados": False}})
CONT = Contabilidad(CFG)
WEB = [{"type": "web_search_20260318", "name": "web_search", "max_uses": 5}]
DOCE = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]
RES: list[tuple[str, bool, str]] = []
_n = itertools.count()


def informe(caso: str, ok: bool, detalle: str) -> None:
    RES.append((caso, ok, detalle))
    print(f"[{'OK' if ok else 'VIOLA'}] {caso}: {detalle}")


def sistema(n_car: int) -> list[dict]:
    return [{"type": "text", "text": "x" * n_car, "cache_control": {"type": "ephemeral"}}]


def mensajes(n_car: int) -> list[dict]:
    return [{"role": "user", "content": "y" * n_car}]


def bloque(cfg=None, cliente=None) -> Bloque:
    d = TMP / f"b{next(_n)}"
    return Bloque(cfg or CFG, ProveedorCSV(EJ / "ejemplos" / "datos_sinteticos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO),
                  cliente or MockClient(), d / "estado", d / "ent")


# ------------------------------------------------------------------ R1
def r1() -> None:
    b = bloque()
    p = Presupuesto({"RV": 4.0}, CFG)   # límite 5 UC
    lim = p.limite("RV")
    sis, msg = sistema(3600 * 4), mensajes(3600)   # ≈ 5 000 tokens × 1,35: el peor caso ≈ 4,4 UC, cabe una sola a la vez

    def falso_invocar(agente, contrato, mensaje, esquema, instrucciones, ctx, run_id, clase, fase, permitir_web, guarda=None):
        mt = guarda.reservar(sis, msg, None, 12000)
        if mt is None:
            return ResultadoAgente(agente, None, "SIN_PRESUPUESTO", errores=[guarda.negada])
        uso = Uso(entrada=int(5000 * 1.35), salida=mt)   # sin caché: `_cargar` carga r.uc tal cual
        guarda.pagar_resto(uso)
        return ResultadoAgente(agente, {"ok": 1}, "COMPLETO", CONT.uc_de(uso), 1, [], False, uso)

    b.agentes.invocar = falso_invocar
    b._contexto = lambda *a, **k: {}
    paso, sigue = threading.Event(), threading.Event()
    cerrar = ReservaLlamada.cerrar

    def cerrar_y_esperar(self):   # la primera llamada se para justo después de soltar lo suyo
        cerrar(self)
        if threading.current_thread().name == "A":
            paso.set()
            sigue.wait(5)
    ReservaLlamada.cerrar = cerrar_y_esperar
    salidas = {}
    try:
        def llamada(nombre):
            salidas[nombre] = b._invocar("AG-03", "CT-07", {}, "CURACION", "", "2024-03-29", "RUN-QA", "RV", "analisis", p)
        a = threading.Thread(target=llamada, args=("A",), name="A")
        a.start()
        paso.wait(5)
        bb = threading.Thread(target=llamada, args=("B",), name="B")
        bb.start()
        bb.join(5)
        sigue.set()
        a.join(5)
    finally:
        ReservaLlamada.cerrar = cerrar
    c = p.consumido["RV"]
    informe("R1 H-08 por _invocar: dos llamadas de una bolsa en hilos", c <= lim + 1e-9 and p.reservado["RV"] == 0,
            f"consumido {c:.4f} con límite {lim:.4f}; A {getattr(salidas.get('A'), 'estado', None)}, "
            f"B {'no salió' if salidas.get('B') is None else salidas['B'].estado}; reservado {p.reservado['RV']:.4f}")


# ------------------------------------------------------------------ R2
def _peticion_con_busquedas(cfg, lectura_real: int) -> tuple[Presupuesto, float, float]:
    p = Presupuesto({"RV": 18.0}, cfg)   # límite 22,5
    lim = p.limite("RV")
    p.cargar("RV", lim - 5.0)            # quedan 5 UC
    sis, msg = sistema(3600 * 6), mensajes(3600 * 2)
    g = ReservaLlamada(p, "RV", CONT, "AG-14")
    mt = g.reservar(sis, msg, WEB, 3000)
    if mt is None:
        return p, lim, 0.0
    bruto = tokens_de_peticion(sis, msg, WEB)
    uso = Uso(cache_escritura=bruto, entrada=5 * lectura_real, salida=mt, busquedas_web=5)
    g.pagar_resto(uso)
    p.cargar("RV", CONT.uc_de(uso))
    g.cerrar()
    return p, lim, g.peor_total


def r2() -> None:
    cfg = copy.deepcopy(CFG)
    cfg["presupuesto_uc"]["reserva"]["tokens_lectura_por_busqueda"] = 6000
    p, lim, peor = _peticion_con_busquedas(cfg, 6000)
    c = p.consumido["RV"]
    informe("R2 H-04 lectura reservada (6 000 por búsqueda, lee 6 000)",
            peor == 0.0 or (c <= lim + 1e-9 and not p.excesos),
            f"reservado {peor:.3f} UC; consumido {c:.3f} con límite {lim:.3f}; excesos {len(p.excesos)} "
            f"({'no salió' if peor == 0.0 else 'salió'})")
    cfg["presupuesto_uc"]["reserva"]["tokens_lectura_por_busqueda"] = 1000
    p, lim, peor = _peticion_con_busquedas(cfg, 6000)
    c = p.consumido["RV"]
    pasa = max(0.0, c - lim)
    anotado = sum(e["real_uc"] - e["reservado_uc"] for e in p.excesos)
    informe("R2 H-04 lee más de lo reservado (1 000 reservado, lee 6 000): lo que pasa ≤ lo anotado",
            pasa <= anotado + 1e-3 and all(e.get("busquedas_web") == 5 for e in p.excesos),
            f"pasa {pasa:.3f} UC; anotado en excesos {anotado:.3f} UC; excesos {p.excesos}")
    c2 = copy.deepcopy(CFG)   # ausente en la configuración recibida: sale de por_defecto.yaml (regla de `parametro`)
    del c2["presupuesto_uc"]["reserva"]["tokens_lectura_por_busqueda"]
    g = ReservaLlamada(Presupuesto({"RV": 18.0}, c2), "RV", CONT, "AG-14")
    informe("R2 H-04 valor ausente: el de por_defecto.yaml", g.lectura_por_busqueda == 0, f"toma {g.lectura_por_busqueda}")
    for nombre, valor, esperado in (("negativo", -1, ValueError), ("NaN", float("nan"), ValueError), ("texto", "mil", ValueError),
                                    ("nulo", None, KeyError)):
        c2 = copy.deepcopy(CFG)
        c2["presupuesto_uc"]["reserva"]["tokens_lectura_por_busqueda"] = valor
        try:
            ReservaLlamada(Presupuesto({"RV": 18.0}, c2), "RV", CONT, "AG-14")
            informe(f"R2 H-04 valor {nombre}", False, "acepta el valor")
        except esperado as e:
            informe(f"R2 H-04 valor {nombre}", True, f"falla cerrado con {type(e).__name__}: {e}")
        except Exception as e:   # noqa: BLE001
            informe(f"R2 H-04 valor {nombre}", True, f"falla cerrado con {type(e).__name__} (otro tipo): {e}")


# ------------------------------------------------------------------ R3
def r3() -> None:
    sis, msg = sistema(3600 * 6), mensajes(3600 * 2)
    bruto = tokens_de_peticion(sis, msg, WEB)
    casos = (("con 5 búsquedas y tokenizador 1,8", 5, False), ("con la herramienta y 0 búsquedas, tokenizador 1,8", 0, True))
    for nombre, busq, debe_observar in casos:
        p = Presupuesto({"RV": 18.0}, CFG)
        g = ReservaLlamada(p, "RV", CONT, "AG-14")
        mt = g.reservar(sis, msg, WEB, 3000)
        g.pagar_resto(Uso(cache_escritura=int(bruto * 1.8), entrada=busq * 3000, salida=mt, busquedas_web=busq))
        g.cerrar()
        obs = p.factor_observado.get("RV", 0.0)
        ok = (obs >= 1.79) if debe_observar else (obs == 0.0)
        informe(f"R3 H-01 {nombre}", ok, f"factor observado {obs:.2f} (se espera {'1,8' if debe_observar else 'ninguno'})")
    # Declarado: con búsqueda, el error del tokenizador no se aprende; la siguiente petición sin búsqueda sí lo aprende
    p = Presupuesto({"RV": 18.0}, CFG)
    for herr, busq in ((WEB, 5), (None, 0)):
        g = ReservaLlamada(p, "RV", CONT, "AG-14")
        mt = g.reservar(sis, msg, herr, 3000)
        b2 = tokens_de_peticion(sis, msg, herr)
        g.pagar_resto(Uso(cache_escritura=int(b2 * 1.8), salida=mt, busquedas_web=busq))
        g.cerrar()
    informe("R3 H-01 la petición sin búsqueda que sigue aprende el factor", p.factor_observado.get("RV", 0) >= 1.79,
            f"factor observado {p.factor_observado.get('RV', 0):.2f}; excesos {len(p.excesos)} (uno por petición)")


# ------------------------------------------------------------------ R4
def r4() -> None:
    sis, msg = sistema(3600 * 20), mensajes(3600 * 4)
    bruto = tokens_de_peticion(sis, msg, None)
    pref = tokens_de_peticion(sis, [], None)
    estado = []
    for leido in (False, True):
        p = Presupuesto({"RV": 8.0}, CFG)   # límite 10
        g = ReservaLlamada(p, "RV", CONT, "AG-10")
        mt = g.reservar(sis, msg, None, 12000)
        u = Uso(entrada=bruto - pref, salida=mt, cache_lectura=pref if leido else 0, cache_escritura=0 if leido else pref)
        g.pagar_resto(u)
        segunda = g.reservar(sis, msg + [{"role": "assistant", "content": "z" * 3600}, {"role": "user", "content": "otra"}],
                             None, 12000)
        estado.append((round(g.apartado, 6), round(p.disponible("RV"), 6), segunda, len(p.recortes), g.negada))
        g.cerrar()
    informe("R4 H-02 prefijo leído o escrito: la reparación se decide igual", estado[0] == estado[1],
            f"escrito {estado[0]} · leído {estado[1]}")


# ------------------------------------------------------------------ R5
class SDKQueSeCae:
    def __init__(self, caer_en: int, excepcion: BaseException) -> None:
        self.caer_en, self.excepcion, self.n = caer_en, excepcion, 0
        self.messages = self

    def create(self, **kw):
        self.n += 1
        if self.n == self.caer_en:
            raise self.excepcion
        ent = int(tokens_de_peticion(kw["system"], kw["messages"], kw.get("tools")) * 1.35)
        uso = types.SimpleNamespace(input_tokens=0, output_tokens=int(kw["max_tokens"]), cache_creation_input_tokens=ent,
                                    cache_read_input_tokens=0, server_tool_use=types.SimpleNamespace(web_search_requests=0))
        return types.SimpleNamespace(stop_reason="end_turn", usage=uso, content=[types.SimpleNamespace(type="text", text="no es json")])


def r5() -> None:
    for nombre, caer_en, exc, en_registro in (
            ("KeyboardInterrupt en la reparación (tras una petición pagada)", 2, KeyboardInterrupt(), False),
            ("KeyboardInterrupt en la primera petición", 1, KeyboardInterrupt(), False),
            ("error al registrar el segundo intento", 0, None, True)):
        sdk = SDKQueSeCae(caer_en, exc)
        b = bloque(cliente=AnthropicClient(sdk=sdk))
        if en_registro:
            registrar = b.contabilidad.registrar

            def registrar_y_caer(*a, **k):
                if k.get("intento") == 2:
                    raise RuntimeError("fallo del registro")
                return registrar(*a, **k)
            b.contabilidad.registrar = registrar_y_caer
        p = Presupuesto({"RV": 18.0}, CFG)
        sube = None
        try:
            b._invocar("AG-12", "CT-11", {"x": 1}, "CURACION", "Clasifica.", "2024-03-29", "RUN-QA", "RV", "investigacion", p)
        except BaseException as e:   # noqa: BLE001
            sube = type(e).__name__
        p.liquidar_primas()
        gastado = sum(x["uc"] for x in b.contabilidad.llamadas)
        ok = sube is not None and p.reservado["RV"] == 0 and p.consumido["RV"] + 1e-6 >= gastado
        if caer_en == 1:
            ok = ok and p.consumido["RV"] == 0
        informe(f"R5 H-05 {nombre}", ok,
                f"sube {sube}; peticiones {sdk.n}; gastado según la contabilidad {gastado:.3f}; cargado {p.consumido['RV']:.3f}; "
                f"reservado {p.reservado['RV']:.4f}")


# ------------------------------------------------------------------ R6
def r6() -> None:
    tope = float(CFG["presupuesto_uc"]["ciclo_semanal_max"])
    escenarios = [
        ("12 tipos, N2 = 100", {"presupuesto_uc": {"N2": 100}}, "PERIODICO", None, None, None),
        ("12 tipos, N1 = 100 > N2", {"presupuesto_uc": {"N1": 100}}, "PERIODICO", None, None, None),
        ("12 tipos, N3 forzado en el periódico", {}, "PERIODICO", "N3", None, None),
        ("12 tipos, profundización", {}, "PROFUNDIZACION", None, None, None),
        ("12 tipos, override de RV = 200", {}, "PERIODICO", None, {"RV": 200.0}, None),
        ("12 tipos, override de COMÚN = 50 y N2 = 60", {"presupuesto_uc": {"N2": 60}}, "PERIODICO", None, {"COMUN": 50.0}, None),
        ("alcance de 3 tipos, N2 = 100", {"presupuesto_uc": {"N2": 100}}, "PERIODICO", None, None, {"clases": ["RV", "RF", "DIV"]}),
        ("V6, 12 tipos, N2 = 100", {"presupuesto_uc": {"N2": 100}, "diseno": "v6"}, "PERIODICO", None, None, None),
        ("alcance con un tipo no activo", {"presupuesto_uc": {"N2": 100}}, "PERIODICO", None, None, {"clases": ["RV", "XXX"]}),
    ]
    for nombre, extra, tipo, forzado, override, alcance in escenarios:
        cfg = cargar_config(extra=dict({"modo": "vivo", "perfiles": {"activos": DOCE}}, **extra))
        b = bloque(cfg)
        c5 = b._comun_minimo_c5("2024-03-29", tipo, alcance, forzado, override, tope)
        activas = list(b.f10("2024-03-29").get("P-02") or DOCE)
        clases = [c for c in ((alcance or {}).get("clases") or activas) if c in activas]
        peor_real = float("inf")
        # todos los repartos reales posibles: en el periódico sin nivel forzado, cada tipo en N1 o N2 (y cualquier
        # subconjunto pausado: menos tipos dan más COMÚN, así que basta con todos los tipos)
        if tipo == "PERIODICO" and not forzado:
            combos = [dict(zip(clases, ns)) for ns in itertools.product(("N1", "N2"), repeat=len(clases))]
        else:
            n = forzado or ("N3" if tipo == "PROFUNDIZACION" else "N2")
            combos = [{c: n for c in clases}]
        for nivel in combos:
            pr = Presupuesto(b._reparto(tipo, clases, nivel, override, tope), cfg, tope_total=tope)
            peor_real = min(peor_real, pr.base("COMUN"))
        informe(f"R6 H-03 {nombre}", c5 <= peor_real + 1e-9,
                f"bolsa de C5 {c5:.4f} · base de COMÚN más baja de los repartos reales {peor_real:.4f} ({len(combos)} repartos)")


# ------------------------------------------------------------------ R7
class SDKAprendizaje:
    def __init__(self):
        self.n = 0
        self.messages = self

    def create(self, **kw):
        self.n += 1
        ent = int(tokens_de_peticion(kw["system"], kw["messages"], kw.get("tools")) * 1.35)
        texto = json.dumps(mock_respuestas.responder("AG-20", kw["messages"][:1], 1), ensure_ascii=False)
        uso = types.SimpleNamespace(input_tokens=0, output_tokens=int(kw["max_tokens"]), cache_creation_input_tokens=ent,
                                    cache_read_input_tokens=0, server_tool_use=None)
        return types.SimpleNamespace(stop_reason="end_turn", usage=uso, content=[types.SimpleNamespace(type="text", text=texto)])


def r7() -> None:
    cfg = cargar_config(extra={"modo": "vivo", "perfiles": {"activos": ["RV", "RF"]}, "llm": {"cache_resultados": False}})
    b = bloque(cfg)
    sdk = SDKAprendizaje()
    b.agentes.clientes["AG-20"] = AnthropicClient(sdk=sdk)
    b.evaluador.ciclo = lambda as_of, run_id: {
        "resueltos": 3, "metricas": {"RV|H2": {"n": 3, "brier": 0.2, "brier_ref": 0.25, "acierto": {"tasa": 0.66},
                                               "calibracion_global": None}},
        "certificados": {"emitidos": [], "insuficientes": []}, "lecciones_nuevas": []}
    r = b.ciclo("2024-03-29", alcance={"clases": ["DIV"]})   # DIV no está activo: no hay nada que analizar
    run = b.almacen.estado("F5", clave="id")[r["run_id"]]
    gastado = sum(x["uc"] for x in b.contabilidad.llamadas if x["run_id"] == r["run_id"])
    en_bolsas = sum(v["consumido"] for v in (run.get("presupuesto") or {}).values())
    informe("R7 sin tipos que analizar: lo gastado por AG-20 está en las bolsas de F5", abs(gastado - en_bolsas) < 1e-3,
            f"peticiones de AG-20 {sdk.n}; gastado {gastado:.3f} UC; en las bolsas de F5 {en_bolsas:.3f} "
            f"(F5 {'con' if 'presupuesto' in run else 'sin'} «presupuesto»); estado {r['estado']}")


# ------------------------------------------------------------------ R8
def r8() -> None:
    sis, msg = sistema(3600 * 6), mensajes(3600 * 2)
    bruto = tokens_de_peticion(sis, msg, WEB)
    p = Presupuesto({"RV": 18.0}, CFG)   # límite 22,5; máximo 27
    lim0, maximo = p.limite("RV"), p.limite_maximo("RV")
    amplia = lambda est: p.autorizar_hasta_tope("RV", est, True)[0]   # noqa: E731  (fase de prospectiva)
    p.cargar("RV", lim0 - 4.0)
    g = ReservaLlamada(p, "RV", CONT, "AG-14", ampliar=amplia)
    mt = g.reservar(sis, msg, WEB, 3000)
    uso = Uso(cache_escritura=bruto, entrada=5 * 3000, salida=mt, busquedas_web=5)   # lee 3 000 por búsqueda sin reservar
    g.pagar_resto(uso)
    p.cargar("RV", CONT.uc_de(uso))
    g.cerrar()
    pasa = p.consumido["RV"] > p.limite("RV")
    g2 = ReservaLlamada(p, "RV", CONT, "AG-14", ampliar=amplia)
    sale = g2.reservar(sis, msg, None, 2500) is not None
    g2.cerrar()
    informe("R8 tras pasar del límite actual (sin llegar al máximo), la fase con ampliación aún puede sacar peticiones",
            True, f"tras el exceso: consumido {p.consumido['RV']:.3f}, límite {p.limite('RV'):.3f} (pasa: {pasa}), máximo {maximo:.3f}; "
            f"la siguiente {'sale' if sale else 'no sale'} (ampliado {p.ampliado['RV']:.3f}). OBS: «después no sale ninguna más» "
            "solo vale respecto del límite máximo")
    # por encima del máximo, como mucho un exceso: se repite la petición con lectura hasta que ya no sale ninguna
    q = Presupuesto({"RV": 18.0}, CFG)
    amplia_q = lambda est: q.autorizar_hasta_tope("RV", est, True)[0]   # noqa: E731
    excesos = []
    for _ in range(40):
        g = ReservaLlamada(q, "RV", CONT, "AG-14", ampliar=amplia_q)
        mt = g.reservar(sis, msg, WEB, 3000)
        if mt is None:
            break
        u = Uso(cache_escritura=bruto, entrada=5 * 3000, salida=mt, busquedas_web=5)
        antes = q.consumido["RV"]
        g.pagar_resto(u)
        q.cargar("RV", CONT.uc_de(u))
        g.cerrar()
        excesos.append((antes, q.consumido["RV"]))
    cruces = [1 for a, d in excesos if a <= maximo + 1e-9 < d]
    despues = [1 for a, d in excesos if a > maximo + 1e-9]
    informe("R8 por encima del límite máximo: una sola petición lo cruza y ninguna sale después", len(cruces) <= 1 and not despues,
            f"peticiones {len(excesos)}; consumido {q.consumido['RV']:.3f} con máximo {maximo:.3f}; cruces {len(cruces)}, "
            f"peticiones después {len(despues)}")


# ------------------------------------------------------------------ R9
class SDKUltimaSinBusqueda:
    def __init__(self, lectura: int) -> None:
        self.lectura, self.n = lectura, 0
        self.messages = self

    def create(self, **kw):
        self.n += 1
        medida = tokens_de_peticion(kw["system"], kw["messages"], kw.get("tools"))
        vuelta = 1 + sum(1 for m in kw["messages"] if m["role"] == "assistant")
        ultima = vuelta == 4
        nuevas = 0 if ultima else 5
        reenviado = 5 * self.lectura * (vuelta - 1)   # lo leído en las vueltas anteriores, que la API vuelve a cobrar
        uso = types.SimpleNamespace(input_tokens=0, output_tokens=int(kw["max_tokens"]),
                                    cache_creation_input_tokens=int(medida) + reenviado + nuevas * self.lectura, cache_read_input_tokens=0,
                                    server_tool_use=types.SimpleNamespace(web_search_requests=nuevas))
        return types.SimpleNamespace(stop_reason="end_turn" if ultima else "pause_turn", usage=uso,
                                     content=[types.SimpleNamespace(type="text", text="ok")])


def r9() -> None:
    sis, msg = sistema(3600 * 6), mensajes(3600 * 2)
    p = Presupuesto({"RV": 18.0}, CFG)
    g = ReservaLlamada(p, "RV", CONT, "AG-14")
    mt = g.reservar(sis, msg, WEB, 3000)
    cli = AnthropicClient(sdk=SDKUltimaSinBusqueda(3000), max_continuaciones=3)
    from bloque_a.llm import con_guarda
    with con_guarda(g):
        r = cli.generar(agente="AG-14", modelo="m", system=sis, mensajes=msg, max_tokens=mt, herramientas=WEB)
    g.pagar_resto(r.uso)
    g.cerrar()
    obs = p.factor_observado.get("RV", 0.0)
    informe("R9 resto de H-01: la última continuación sin búsquedas no sube el factor por lo reenviado", obs == 0.0,
            f"peticiones {cli.sdk.n}; factor observado {obs:.2f} (peor caso: el reenvío de 15 lecturas de 3 000 tokens no medido)")


for f in (r1, r2, r3, r4, r5, r6, r7, r8, r9):
    try:
        f()
    except Exception as e:   # noqa: BLE001
        informe(f.__name__, False, f"el ataque falló: {type(e).__name__}: {e}")
print(f"\n{sum(ok for _, ok, _ in RES)}/{len(RES)} OK")
