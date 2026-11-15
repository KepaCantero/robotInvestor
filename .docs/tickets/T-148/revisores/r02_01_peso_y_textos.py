"""QA r02 de T-148 (revisor) · el peso de lo que lee cada búsqueda, los textos de la salida y las opciones excluyentes.

Uso, desde la raíz de la copia:
  .venv/bin/python -I .docs/tickets/T-148/revisores/r02_01_peso_y_textos.py <medida divisas> <medida 12 tipos> <doce.yaml> <trabajo>
(las medidas, de `medir_consumo_a.py` lanzado desde `bloque_a/11_Ejecutor` con `PYTHONPATH=$PWD`). Sin red ni coste.

Comprueba:
  P1. los dos pesos por cada 1 000 tokens leídos (cota por llamadas y por presupuesto), a mano desde la configuración y la
      tarifa, frente a lo que imprime el estimador (divisas y 12 tipos), y que el de la salida es el de la cota que manda;
  P2. ninguna salida (por defecto, `--con-t146`, `--sin-t146`, divisas y 12 tipos, y con lectura reservada por búsqueda)
      promete cubrir lo que lee cada búsqueda; todas dicen «salvo lo que lee cada búsqueda»; con
      `tokens_lectura_por_busqueda` > 0 lo dice y que el peso no lo descuenta;
  P3. `--sin-t146` y `--con-t146` se excluyen en los dos órdenes (código 2);
  P4. con el código de T-146 (reserva, cliente real, ampliación de la fase de prospectiva): una llamada con cuatro vueltas
      de `pause_turn` y cinco búsquedas por vuelta, cuyo reenvío de lo leído la reserva no ve (el peor caso), con la bolsa
      llenada a distintos niveles: lo que la bolsa acaba por encima de su límite máximo, en USD, no pasa del peso por bolsa
      de la cota por presupuesto (para 1 000, 8 000 y 50 000 tokens leídos por búsqueda);
  P5. la cota más su peso sigue siendo cota cuando la lectura es tan grande que cambiaría cuál manda.
Imprime OK / HALLAZGO por caso y termina con 1 si hay algún hallazgo."""
import re
import subprocess
import sys
import types
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
EST = RAIZ / ".docs" / "scripts" / "estimar_coste_ciclo_a.py"
sys.path.insert(0, str(EJ))
import yaml  # noqa: E402

from bloque_a.configuracion import cargar_config, modelo_de, parametro  # noqa: E402
from bloque_a.consumo import Contabilidad, Presupuesto, ReservaLlamada, tokens_de_peticion  # noqa: E402
from bloque_a.llm import AnthropicClient, Uso, con_guarda  # noqa: E402

M_DIV, M_12, DOCE, TRABAJO = (Path(x).resolve() for x in sys.argv[1:5])
TRABAJO.mkdir(parents=True, exist_ok=True)
RES: list[tuple[str, bool, str]] = []
PRECIOS = yaml.safe_load((EJ / "config" / "precios_anthropic.yaml").read_text(encoding="utf-8"))["precios_por_millon"]


def informe(caso: str, ok: bool, detalle: str) -> None:
    RES.append((caso, ok, detalle))
    print(f"{'OK      ' if ok else 'HALLAZGO'} {caso} · {detalle}")


def estimar(medida: Path, *extra: str) -> subprocess.CompletedProcess:
    import os
    env = dict(os.environ, PYTHONPATH=str(EJ))
    return subprocess.run([sys.executable, str(EST), str(medida), *extra], capture_output=True, text=True, check=False, cwd=EJ,
                          env=env)


def cifras(salida: str) -> dict:
    m = re.search(r"Cota superior del ciclo: ([\d.]+) USD", salida)
    ll = re.search(r"por llamadas +([\d.]+) USD", salida)
    pr = re.search(r"por presupuesto +([\d.]+) USD", salida)
    w = re.search(r"la cota que manda \(por (\w+)\) sube ([\d.]+) USD \(la cota por llamadas, ([\d.]+); la cota por presupuesto, "
                  r"([\d.]+)\)", salida)
    return {"cota": float(m[1]), "llamadas": float(ll[1]), "presupuesto": float(pr[1]), "manda": w[1], "peso": float(w[2]),
            "peso_ll": float(w[3]), "peso_pr": float(w[4])}


# ------------------------------------------------------------------ P1
def p1() -> None:
    cfg = cargar_config()
    max_usos = int(parametro(cfg, "busqueda_web.max_usos_por_llamada"))
    vueltas = 1 + int(parametro(cfg, "llm.max_continuaciones_pause_turn"))
    buscan = [a for a in parametro(cfg, "busqueda_web.agentes") if a in ("AG-14", "AG-15", "AG-16")]   # V5: los de cada tipo
    caro = max(PRECIOS[modelo_de(cfg, a)]["escritura_cache"] for a in buscan)
    por_bolsa = max_usos * vueltas * caro * 1000 / 1e6
    for nombre, medida, extra, n_tipos in (("divisas", M_DIV, [], 1), ("12 tipos", M_12, ["--config", str(DOCE)], 12)):
        c = cifras(estimar(medida, *extra).stdout)
        esperado_pr = n_tipos * por_bolsa
        manda = "presupuesto" if c["presupuesto"] < c["llamadas"] else "llamadas"
        ok = (abs(c["peso_pr"] - round(esperado_pr, 2)) < 0.006 and c["manda"] == manda
              and c["peso"] == (c["peso_pr"] if manda == "presupuesto" else c["peso_ll"]))
        informe(f"P1 {nombre}: el peso de la cota por presupuesto, a mano", ok,
                f"a mano {n_tipos} × {max_usos} × {vueltas} × {caro} USD/M × 1 000 = {esperado_pr:.2f} · impreso {c['peso_pr']:.2f}; "
                f"manda {c['manda']} (esperado {manda}), peso impreso {c['peso']:.2f}")


# ------------------------------------------------------------------ P2
PROHIBIDAS = ("acota también", "acota tambien", "acota lo que lee", "cubre lo que lee", "también lo que lee")


def p2() -> None:
    reserva = TRABAJO / "reserva_2000.yaml"
    doce = yaml.safe_load(DOCE.read_text(encoding="utf-8"))
    reserva.write_text(yaml.safe_dump(dict(doce, presupuesto_uc={"reserva": {"tokens_lectura_por_busqueda": 2000}})), encoding="utf-8")
    for nombre, medida, extra in (("divisas", M_DIV, []), ("divisas --con-t146", M_DIV, ["--con-t146"]),
                                  ("divisas --sin-t146", M_DIV, ["--sin-t146"]), ("12 tipos", M_12, ["--config", str(DOCE)]),
                                  ("12 tipos --sin-t146", M_12, ["--config", str(DOCE), "--sin-t146"]),
                                  ("12 tipos con 2 000 reservados", M_12, ["--config", str(reserva)])):
        r = estimar(medida, *extra)
        bajo = r.stdout.lower()
        malas = [f for f in PROHIBIDAS if f in bajo]
        ok = r.returncode == 0 and not malas and "salvo lo que lee cada búsqueda" in r.stdout
        if "2 000" in nombre:
            ok = ok and "aparta 2000 tokens por búsqueda" in r.stdout and "que el peso no descuenta" in r.stdout
        informe(f"P2 {nombre}: la salida no promete cubrir lo leído", ok,
                f"código {r.returncode}; frases prohibidas {malas or 'ninguna'}; "
                + (re.search(r"Lo que lee cada búsqueda.*", r.stdout)[0][-120:] if "Lo que lee" in r.stdout else r.stderr[-200:]))


# ------------------------------------------------------------------ P3
def p3() -> None:
    for orden in (["--sin-t146", "--con-t146"], ["--con-t146", "--sin-t146"]):
        r = estimar(M_DIV, *orden)
        informe(f"P3 {' '.join(orden)}", r.returncode == 2 and "not allowed" in r.stderr, f"código {r.returncode}")


# ------------------------------------------------------------------ P4
class SDKLecturaInvisible:
    """Cada vuelta hace 5 búsquedas que leen `lectura` tokens; la API cobra en cada petición lo leído en esa y en las anteriores
    del intento (las reenvía), pero el contenido devuelto es corto: la medida de la reserva no ve el reenvío (peor caso)."""

    def __init__(self, lectura: int, max_usos: int) -> None:
        self.lectura, self.max_usos, self.n = lectura, max_usos, 0
        self.messages = self

    def create(self, **kw):
        self.n += 1
        medida = tokens_de_peticion(kw["system"], kw["messages"], kw.get("tools"))
        vuelta = 1 + sum(1 for m in kw["messages"] if m["role"] == "assistant")
        uso = types.SimpleNamespace(input_tokens=int(medida) + self.max_usos * self.lectura * vuelta,
                                    output_tokens=int(kw["max_tokens"]), cache_creation_input_tokens=0, cache_read_input_tokens=0,
                                    server_tool_use=types.SimpleNamespace(web_search_requests=self.max_usos))
        stop = "pause_turn" if vuelta < 4 else "end_turn"
        return types.SimpleNamespace(stop_reason=stop, usage=uso, content=[types.SimpleNamespace(type="text", text="ok")])


def p4() -> None:
    cfg = cargar_config(extra={"modo": "vivo"})
    cont = Contabilidad(cfg)
    max_usos = int(parametro(cfg, "busqueda_web.max_usos_por_llamada"))
    vueltas = 1 + int(parametro(cfg, "llm.max_continuaciones_pause_turn"))
    precio_ent = PRECIOS[modelo_de(cfg, "AG-14")]["entrada"]
    peso_bolsa_mil = max_usos * vueltas * PRECIOS[modelo_de(cfg, "AG-14")]["escritura_cache"] * 1000 / 1e6
    web = [{"type": "web_search_20260318", "name": "web_search", "max_uses": max_usos}]
    sis = [{"type": "text", "text": "x" * 3600 * 8, "cache_control": {"type": "ephemeral"}}]
    msg = [{"role": "user", "content": "y" * 3600 * 2}]
    for lectura in (1000, 8000, 50000):
        peor_usd, peor_detalle = 0.0, ""
        for relleno in [x / 4 for x in range(0, 4 * 27)]:   # la bolsa DIV (N2 = 18) llena de 0 a 27 UC, de 0,25 en 0,25
            p = Presupuesto({"DIV": float(parametro(cfg, "presupuesto_uc.N2"))}, cfg)
            p.cargar("DIV", relleno)
            g = ReservaLlamada(p, "DIV", cont, "AG-14", ampliar=lambda est, p=p: p.autorizar_hasta_tope("DIV", est, True)[0])
            mt = g.reservar(sis, msg, web, 3000)
            if mt is None:
                continue
            cli = AnthropicClient(sdk=SDKLecturaInvisible(lectura, max_usos), max_continuaciones=vueltas - 1)
            with con_guarda(g):
                r = cli.generar(agente="AG-14", modelo="m", system=sis, mensajes=msg, max_tokens=mt, herramientas=web)
            g.pagar_resto(r.uso)
            p.cargar("DIV", cont.uc_de(r.uso))
            g.cerrar()
            encima_uc = p.consumido["DIV"] - p.limite_maximo("DIV")
            # UC de entrada → tokens (0,5 × entrada / 8 000) → USD al precio de entrada del agente (lo que cobra la API)
            usd = max(0.0, encima_uc) / (0.5 / float(parametro(cfg, "uc.tokens_entrada_por_uc"))) * precio_ent / 1e6
            if usd > peor_usd:
                peor_usd, peor_detalle = usd, f"relleno {relleno} UC: {encima_uc:.3f} UC encima del máximo ({r.stop_reason})"
        cota = peso_bolsa_mil * lectura / 1000
        informe(f"P4 lectura {lectura} por búsqueda: lo que pasa del límite máximo ≤ el peso por bolsa", peor_usd <= cota + 1e-9,
                f"peor {peor_usd:.4f} USD ({peor_detalle or 'nunca pasa'}) · peso de la bolsa {cota:.4f} USD")


# ------------------------------------------------------------------ P5
def p5() -> None:
    for nombre, medida, extra in (("divisas", M_DIV, []), ("12 tipos", M_12, ["--config", str(DOCE)])):
        c = cifras(estimar(medida, *extra).stdout)
        malos = []
        for mil in (0, 10, 56, 100, 1000):
            verdad = min(c["llamadas"] + c["peso_ll"] * mil, c["presupuesto"] + c["peso_pr"] * mil)
            if c["cota"] + c["peso"] * mil + 0.01 < verdad:
                malos.append(mil)
        informe(f"P5 {nombre}: cota + peso × lectura ≥ la menor de las dos con esa lectura", not malos, f"falla en {malos or 'ninguna'}")


for f in (p1, p2, p3, p4, p5):
    try:
        f()
    except Exception as e:   # noqa: BLE001
        informe(f.__name__, False, f"el ataque falló: {type(e).__name__}: {e}")
n = sum(not ok for _, ok, _ in RES)
print(f"\n{n} hallazgos")
sys.exit(1 if n else 0)
