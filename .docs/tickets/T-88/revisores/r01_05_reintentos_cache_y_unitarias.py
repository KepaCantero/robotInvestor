"""QA r01 de T-88 · 05: reintentos, aciertos de la caché de respuestas, una caché de prompts que se pierde, y la regla de
reparto de `Presupuesto` a mano.

  .venv/bin/python -I .docs/tickets/T-88/revisores/r01_05_reintentos_cache_y_unitarias.py [--ejecutor RUTA]

  R · reintentos: el analista de un solo tipo (AG-03, RV) con dos respuestas no conformes. Mismo F5 con 1, 6 y 12 hilos; la
      prima «solo» de su primera llamada es la del prefijo (no una por intento); en la V6 el total cargado es el real;
  K · caché de respuestas: un segundo ciclo con la mitad de las respuestas ya en caché (elegidas por la clave, no por el orden
      de escritura): mismo F5 con 1, 6 y 12 hilos y total = real (V6);
  P · una caché de prompts que se pierde a mitad del ciclo (cliente que olvida lo escrito cada 7 llamadas): ¿carga cada tipo
      durante la fase al menos su escritura real?, ¿el total sigue siendo el real?;
  U · `Presupuesto` a mano: orden de las cargas, liquidación repetida, una bolsa que no usó un prefijo y paga parte de él."""
import json
import random
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import Marcador, bloque, f5_presupuesto, huella, preparar  # noqa: E402

a, resto, ej = preparar(__doc__)
PARTES = {x for x in resto if len(x) == 1} or set("RKPU")
import pytest  # noqa: E402
from bloque_a.consumo import Presupuesto  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from conftest import AS_OF, config_pruebas  # noqa: E402

m = Marcador()
SEIS = ["RV", "RF", "DIV", "MP", "IDX", "FON"]


def cfg(d, h):
    return config_pruebas(diseno=d, perfiles={"activos": SEIS}, paralelismo={"hilos_analistas": h})


def espiar_cargas():
    """Registra (bolsa, tokens_solo, tokens_reales, agente, intentos) de cada carga con prima."""
    import threading

    from bloque_a.orquestacion import Bloque
    reg, local = [], threading.local()
    orig, orig_cargar = Presupuesto.cargar_con_prima, Bloque._cargar

    def espia(self, bolsa, leido, tokens_solo, tokens_reales):
        reg.append((bolsa, int(tokens_solo), int(tokens_reales), getattr(local, "agente", None), getattr(local, "intentos", None)))
        return orig(self, bolsa, leido, tokens_solo, tokens_reales)

    def cargar(self, presupuesto, bolsa, agente, r):
        local.agente, local.intentos = agente, r.intentos
        return orig_cargar(self, presupuesto, bolsa, agente, r)
    Presupuesto.cargar_con_prima, Bloque._cargar = espia, cargar

    def deshacer():
        Presupuesto.cargar_con_prima, Bloque._cargar = orig, orig_cargar
    return reg, deshacer


if "R" in PARTES:
    for d in ("v5", "v6"):
        vistos = set()
        for h in (1, 6, 12):
            reg, deshacer = espiar_cargas()
            b = bloque(cfg(d, h), MockClient(fallos={"AG-03": 2}))
            b.ciclo(AS_OF)
            deshacer()
            f5 = f5_presupuesto(b)
            vistos.add(huella(f5))
            if h == 1:
                ll = [c for c in b.contabilidad.llamadas if c["agente"] == "AG-03"]
                intentos = max(c["intento"] for c in ll)
                b2 = bloque(cfg(d, 1))
                reg2, deshacer2 = espiar_cargas()
                b2.ciclo(AS_OF)
                deshacer2()
                # la primera llamada de AG-03 en RV (con reintentos) frente a la misma sin ellos: misma prima «solo»
                p1 = [(s, n) for k, s, _, ag, n in reg if k == "RV" and ag == "AG-03"][0]
                p2 = [(s, n) for k, s, _, ag, n in reg2 if k == "RV" and ag == "AG-03"][0]
                m.check(f"R {d}: la primera llamada de AG-03 con {p1[1]} intentos paga la misma prima «solo» que con {p2[1]}",
                        p1[0] == p2[0] and p1[1] > p2[1], f"{p1[0]} vs {p2[0]} tokens")
                if d == "v6":
                    real = sum(c["uc"] for c in b.contabilidad.llamadas)
                    m.check("R v6: con reintentos, total cargado = real", abs(sum(x["consumido"] for x in f5.values()) - real) <= 0.01)
        m.check(f"R {d}: con reintentos, el mismo F5 con 1, 6 y 12 hilos", len(vistos) == 1, f"{len(vistos)} variantes")

if "K" in PARTES:
    for d in ("v5", "v6"):
        tmp0 = Path(tempfile.mkdtemp(prefix="qa_t88_k_"))
        b0 = bloque(cfg(d, 1), tmp=tmp0)
        b0.ciclo(AS_OF)
        lineas = (tmp0 / "estado" / "cache_resultados.jsonl").read_text(encoding="utf-8").splitlines()
        mitad = [x for x in lineas if int(json.loads(x)["clave"][-1], 16) % 2 == 0] if lineas and "clave" in json.loads(lineas[0]) \
            else sorted(lineas)[::2]
        vistos, hits = set(), []
        for h in (1, 6, 12):
            tmp = Path(tempfile.mkdtemp(prefix="qa_t88_k_"))
            (tmp / "estado").mkdir()
            (tmp / "estado" / "cache_resultados.jsonl").write_text("\n".join(mitad) + "\n", encoding="utf-8")
            b = bloque(cfg(d, h), tmp=tmp)
            b.ciclo(AS_OF)
            f5 = f5_presupuesto(b)
            vistos.add(huella(f5))
            hits.append(sum(1 for c in b.contabilidad.llamadas if c.get("cache_hit")))
            if d == "v6" and h == 12:
                real = sum(c["uc"] for c in b.contabilidad.llamadas)
                m.check("K v6: con aciertos de caché, total cargado = real", abs(sum(x["consumido"] for x in f5.values()) - real) <= 0.01,
                        f"{sum(x['consumido'] for x in f5.values()):.4f} vs {real:.4f}")
            shutil.rmtree(tmp, ignore_errors=True)
        m.check(f"K {d}: con la mitad de las respuestas en caché ({len(mitad)} de {len(lineas)}; aciertos {hits}), el mismo F5 con 1, 6 y 12 hilos",
                len(vistos) == 1 and min(hits) > 0, f"{len(vistos)} variantes")
        shutil.rmtree(tmp0, ignore_errors=True)

if "P" in PARTES:
    class Olvidadizo(MockClient):
        """Pierde la caché de prompts cada 7 llamadas (como una caché que caduca o se desaloja a mitad del ciclo)."""
        def generar(self, **kw):
            with self._lock:
                if len(self.llamadas) % 7 == 6:
                    self._vistos.clear()
            return super().generar(**kw)
    reg, deshacer = espiar_cargas()
    b = bloque(cfg("v6", 1), Olvidadizo())
    b.ciclo(AS_OF)
    deshacer()
    por_bolsa = {}
    for k, s, r, _, _ in reg:
        x = por_bolsa.setdefault(k, [0, 0])
        x[0] += s
        x[1] += r
    menos = {k: v for k, v in por_bolsa.items() if v[0] < v[1]}
    print(f"   P: tokens «solo» frente a escritos de verdad por bolsa: {por_bolsa}")
    m.check("P: con una caché que se pierde, cada bolsa carga durante la fase al menos su escritura real (README: «nunca carga menos»)",
            not menos, f"bolsas por debajo: {menos}")
    f5 = f5_presupuesto(b)
    real = sum(c["uc"] for c in b.contabilidad.llamadas)
    m.check("P: el total cargado sigue siendo el real", abs(sum(x["consumido"] for x in f5.values()) - real) <= 0.01)

if "U" in PARTES:
    c = config_pruebas()
    cargas = [("RV", 0.31, 20000, 20000), ("RF", 0.27, 20000, 0), ("RV", 0.12, 0, 0), ("DIV", 0.4, 5000, 5000), ("RF", 0.2, 8000, 8000),
              ("COMUN", 0.1, 3000, 0)]
    vistos = set()
    for k in range(50):
        p = Presupuesto({"RV": 9, "RF": 9, "DIV": 9, "COMUN": 9}, c)
        orden = cargas[:]
        random.Random(k).shuffle(orden)
        for x in orden:
            p.cargar_con_prima(*x)
        vistos.add(huella(p.resumen()))
        r1 = huella(p.resumen())
        m.n += 0
    m.check("U: 50 órdenes distintos de las mismas cargas dan el mismo resumen (redondeado a 4 decimales)", len(vistos) == 1, f"{len(vistos)}")
    m.check("U: resumen() repetido no cambia nada", r1 == huella(p.resumen()))
    total = sum(v["consumido"] for v in p.resumen().values())
    esperado = sum(x[1] for x in cargas) + p._uc_prima(sum(x[3] for x in cargas))
    m.check("U: total tras liquidar = lectura + prima real", total == pytest.approx(esperado, abs=1e-3), f"{total:.4f} vs {esperado:.4f}")
    # RV usa un prefijo propio (10.000) y otro compartido (5.000); RF solo el compartido. Reparto por prefijo: RV 12.500, RF 2.500
    p = Presupuesto({"RV": 9, "RF": 9, "COMUN": 9}, c)
    p.cargar_con_prima("RV", 0.0, 10000, 10000)
    p.cargar_con_prima("RV", 0.0, 5000, 5000)
    p.cargar_con_prima("RF", 0.0, 5000, 0)
    p.liquidar_primas()
    rf_tokens = p.consumido["RF"] / p._uc_prima(1)
    print(f"   U: RF, que no usó el prefijo de 10.000 tokens de RV, acaba pagando {rf_tokens:.0f} tokens de escritura (su parte del"
          f" compartido sería 2.500)")
    m.check("U: una bolsa no paga parte de un prefijo que no usó", abs(rf_tokens - 2500) < 1, f"{rf_tokens:.0f} tokens")
sys.exit(m.fin())
