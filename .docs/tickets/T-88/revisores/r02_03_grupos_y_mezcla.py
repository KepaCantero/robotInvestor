"""QA r02 de T-88 · 03: ¿el reparto por grupos mezcla prefijos? (CA-6, H-02 de la r01)

  .venv/bin/python -I .docs/tickets/T-88/revisores/r02_03_grupos_y_mezcla.py [--ejecutor RUTA] [partes]

Partes (todas por defecto):
  U · `Presupuesto` a mano, con la forma de la V6: RV y RF comparten el núcleo (5.000 tokens); el kit de RV mide 10.000 y el
      de RF 1.000. Lo justo por prefijos: cada kit a su tipo y el núcleo repartido. ¿Paga RF parte del kit de RV?
  G · ciclo V6 real (doce tipos, un hilo): espía `cargar_con_prima` y, para el grupo ANALISTAS, separa el núcleo (lo que
      lee un analista que no escribe primero) del kit de cada tipo. Compara lo que paga cada tipo tras liquidar con «su kit
      entero + su parte del núcleo» (en proporción a las primas «solo», la regla del ticket) y da la mezcla en UC;
  P · ciclo V5 (seis tipos, un hilo) con un cliente que pierde la caché de prompts cada 7 llamadas: el analista que vuelve a
      escribir su prompt, ¿lo paga él o se reparte entre los demás tipos?;
  A · qué pares (bolsa, agente) se cargan con prima, y si algún analista se carga a una bolsa que no es la suya (entonces
      su prompt entra en el reparto de otro tipo) o un agente compartido aparece como «propio»."""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import Marcador, bloque, preparar  # noqa: E402

a, resto, ej = preparar(__doc__)
PARTES = {x for x in resto if len(x) == 1} or set("UGPA")
from bloque_a.consumo import Presupuesto  # noqa: E402
from bloque_a.contratos import AGENTE_CLASE  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402
from conftest import AS_OF, config_pruebas  # noqa: E402

TODOS = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]
ANALISTAS = set(AGENTE_CLASE.values())
m = Marcador()


def espiar():
    """Registra (bolsa, agente, grupo, solo, cargar, reales, prefijo) de cada carga con prima."""
    import threading
    reg, local = [], threading.local()
    orig, orig_cargar = Presupuesto.cargar_con_prima, Bloque._cargar

    def espia(self, bolsa, grupo, leido, tokens_solo, tokens_cargar, tokens_reales):
        reg.append({"bolsa": bolsa, "agente": getattr(local, "agente", None), "grupo": grupo, "solo": int(tokens_solo),
                    "cargar": int(tokens_cargar), "reales": int(tokens_reales), "prefijo": getattr(local, "prefijo", None)})
        return orig(self, bolsa, grupo, leido, tokens_solo, tokens_cargar, tokens_reales)

    def cargar(self, presupuesto, bolsa, agente, r):
        local.agente = agente
        u = r.uso
        local.prefijo = (u.cache_lectura + u.cache_escritura) // max(1, r.intentos)
        return orig_cargar(self, presupuesto, bolsa, agente, r)
    Presupuesto.cargar_con_prima, Bloque._cargar = espia, cargar

    def deshacer():
        Presupuesto.cargar_con_prima, Bloque._cargar = orig, orig_cargar
    return reg, deshacer


def uc(p, tokens):
    return p._uc_prima(tokens)


if "U" in PARTES:
    p = Presupuesto({"RV": 10, "RF": 10, "COMUN": 5}, config_pruebas())
    p.cargar_con_prima("RV", "ANALISTAS", 0.0, 15000, 15000, 15000)   # RV primero: núcleo 5.000 + kit 10.000
    p.cargar_con_prima("RF", "ANALISTAS", 0.0, 6000, 6000, 1000)      # RF: lee el núcleo, escribe su kit de 1.000
    p.liquidar_primas()
    rf = p.consumido["RF"]
    justo_rf = uc(p, 1000 + 5000 * 6000 / 21000)   # su kit + su parte del núcleo, en proporción a las primas «solo»
    justo_rf_igual = uc(p, 1000 + 2500)
    print(f"   U: RF paga {rf:.5f} UC; lo justo por prefijos {justo_rf:.5f} (núcleo proporcional) o {justo_rf_igual:.5f} (a partes "
          f"iguales); RF paga {(rf - justo_rf) / uc(p, 1):.0f} tokens del kit de RV")
    m.check("U: RF no paga nada del kit de RV (CA-6)", rf <= max(justo_rf, justo_rf_igual) + 1e-9,
            f"{rf:.5f} > {max(justo_rf, justo_rf_igual):.5f}")
    m.check("U: el total se conserva", abs(p.consumido["RV"] + rf - uc(p, 16000)) < 1e-9)

if "G" in PARTES or "A" in PARTES:
    reg, deshacer = espiar()
    b = bloque(config_pruebas(diseno="v6", perfiles={"activos": TODOS}, paralelismo={"hilos_analistas": 1}))
    b.ciclo(AS_OF)
    deshacer()
    p = Presupuesto({}, b.cfg)
    if "A" in PARTES:
        pares = sorted({(r["bolsa"], r["agente"], r["grupo"]) for r in reg})
        ajenos = [(bo, ag) for bo, ag, _ in pares if ag in ANALISTAS and AGENTE_CLASE.get(bo) != ag]
        propios_comp = [(bo, ag) for bo, ag, _ in pares if ag not in ANALISTAS and any(
            r["bolsa"] == bo and r["agente"] == ag and r["cargar"] for r in reg)]
        print(f"   A v6: grupos {sorted({g for _, _, g in pares})}; pares (bolsa, agente) {len(pares)}")
        m.check("A v6: ningún analista se carga a una bolsa que no es la suya", not ajenos, f"{ajenos}")
        m.check("A v6: ningún agente compartido carga prima durante la fase", not propios_comp, f"{propios_comp}")
    if "G" in PARTES:
        an = [r for r in reg if r["grupo"] == "ANALISTAS"]
        # núcleo: prefijo − escrito de un analista que escribe su kit pero lee el núcleo
        nucleos = {r["prefijo"] - r["reales"] for r in an if 0 < r["reales"] < r["prefijo"]}
        assert len(nucleos) == 1, nucleos
        nucleo = nucleos.pop()
        solo = defaultdict(int)
        for r in an:
            solo[r["bolsa"]] += r["solo"]
        kits = {bo: s - nucleo for bo, s in solo.items()}
        reales = sum(r["reales"] for r in an)
        total = sum(solo.values())
        assert reales == nucleo + sum(kits.values()), (reales, nucleo, kits)
        mezcla = {}
        for bo in sorted(solo):
            pagado = reales * solo[bo] / total
            justo = kits[bo] + nucleo * solo[bo] / total
            mezcla[bo] = (pagado - justo, uc(p, pagado - justo))
        peor = max(mezcla.items(), key=lambda x: abs(x[1][1]))
        print(f"   G v6: núcleo {nucleo} tokens; kits {dict(sorted(kits.items()))}")
        print("   G v6: tokens de kits ajenos pagados (+) o cobrados a otros (−) por tipo: "
              + ", ".join(f"{bo} {v[0]:+.0f} ({v[1]:+.4f} UC)" for bo, v in mezcla.items()))
        print(f"   G v6: suma de |mezcla| {sum(abs(v[1]) for v in mezcla.values()):.4f} UC; peor {peor[0]} {peor[1][1]:+.4f} UC")
        m.check("G v6: ningún tipo paga parte del kit de otro (CA-6)", all(abs(v[1]) < 1e-4 for v in mezcla.values()),
                f"peor {peor[0]} {peor[1][1]:+.4f} UC")

if "P" in PARTES:
    class Olvidadizo(MockClient):
        """Pierde la caché de prompts cada 7 llamadas (como una caché que caduca o se desaloja a mitad del ciclo)."""
        def generar(self, **kw):
            with self._lock:
                if len(self.llamadas) % 7 == 6:
                    self._vistos.clear()
            return super().generar(**kw)
    reg, deshacer = espiar()
    b = bloque(config_pruebas(diseno="v5", perfiles={"activos": TODOS[:6]}, paralelismo={"hilos_analistas": 1}), Olvidadizo())
    b.ciclo(AS_OF)
    deshacer()
    p = Presupuesto({}, b.cfg)
    an = [r for r in reg if r["grupo"] == "ANALISTAS"]
    propio_real, solo = defaultdict(int), defaultdict(int)
    for r in an:
        propio_real[r["bolsa"]] += r["reales"]
        solo[r["bolsa"]] += r["solo"]
    total_r, total_s = sum(propio_real.values()), sum(solo.values())
    dif = {bo: uc(p, total_r * solo[bo] / total_s - propio_real[bo]) for bo in sorted(solo)}
    print(f"   P v5: escrito de verdad por el analista de cada tipo {dict(propio_real)}; primas «solo» {dict(solo)}")
    print("   P v5: UC del prompt de otros analistas que paga cada tipo (+) o que le pagan (−): "
          + ", ".join(f"{bo} {v:+.4f}" for bo, v in dif.items()))
    m.check("P v5: con una caché que se pierde, cada analista paga sus propias reescrituras (sin mezclar tipos)",
            all(abs(v) < 1e-4 for v in dif.values()), f"{ {k: round(v, 4) for k, v in dif.items()} }")
sys.exit(m.fin())
