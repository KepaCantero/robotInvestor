"""QA r03 de T-88 · 02: grupos de prefijos de la r03 (H-05 de la r02), leídos de lo que de verdad llega a la liquidación.

  .venv/bin/python -I .docs/tickets/T-88/revisores/r03_02_grupos_v5_v6.py [--ejecutor RUTA] [partes]

Antes de cada liquidación se guardan los pesos «solo» y los tokens reales de cada grupo (`Presupuesto._pesos`/`_reales`).
Partes (todas por defecto):
  V · V5, doce tipos, seis hilos: cada analista es su propio grupo (`AG-xx`) y en ese grupo solo pesa su tipo, así que lo que
      escribe de verdad vuelve entero a su tipo; no hay grupo «ANALISTAS»; ningún analista se carga a una bolsa ajena;
  P · V5, seis tipos, un hilo, con un cliente que pierde la caché de prompts cada 7 llamadas (el caso P de la r02): cada tipo
      paga exactamente las reescrituras de su analista (tokens);
  S · V6, doce tipos, seis hilos: los analistas van en «ANALISTAS» (núcleo común, declarado en INC-T88-01) y ningún analista
      aparece como grupo propio; los agentes compartidos, cada uno en el suyo."""
import sys
import threading
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import Marcador, bloque, preparar  # noqa: E402

a, resto, ej = preparar(__doc__)
PARTES = {x for x in resto if len(x) == 1} or set("VPS")
from bloque_a.consumo import Presupuesto  # noqa: E402
from bloque_a.contratos import AGENTE_CLASE, CLASE_AGENTE  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402
from conftest import AS_OF, config_pruebas  # noqa: E402

TODOS = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]
ANALISTAS = set(AGENTE_CLASE.values())
m = Marcador()


def instrumentar():
    snaps, cargas, local = [], [], threading.local()
    orig_liq, orig_cargar, orig_ccp = Presupuesto.liquidar_primas, Bloque._cargar, Presupuesto.cargar_con_prima

    def liq(self):
        snaps.append({g: (dict(self._pesos.get(g, {})), int(r)) for g, r in self._reales.items()})
        return orig_liq(self)

    def cargar(self, p, bolsa, agente, r):
        local.agente = agente
        return orig_cargar(self, p, bolsa, agente, r)

    def ccp(self, bolsa, grupo, leido, solo, cargar_, reales):
        cargas.append((bolsa, getattr(local, "agente", None), grupo, int(reales)))
        return orig_ccp(self, bolsa, grupo, leido, solo, cargar_, reales)
    Presupuesto.liquidar_primas, Bloque._cargar, Presupuesto.cargar_con_prima = liq, cargar, ccp

    def deshacer():
        Presupuesto.liquidar_primas, Bloque._cargar, Presupuesto.cargar_con_prima = orig_liq, orig_cargar, orig_ccp
    return snaps, cargas, deshacer


def comprobar_v5(etiqueta, snaps, cargas):
    grupos = set().union(*[set(s) for s in snaps]) if snaps else set()
    m.check(f"{etiqueta}: no hay grupo ANALISTAS en la V5", "ANALISTAS" not in grupos, f"grupos={sorted(grupos)}")
    malos = []
    for s in snaps:
        for g, (pesos, reales) in s.items():
            if g in ANALISTAS and set(pesos) - {CLASE_AGENTE[g]}:
                malos.append((g, sorted(pesos)))
    m.check(f"{etiqueta}: en el grupo de cada analista solo pesa su tipo", not malos, f"{malos[:4]}")
    ajenos = sorted({(bo, ag) for bo, ag, _, _ in cargas if ag in ANALISTAS and AGENTE_CLASE.get(bo) != ag})
    m.check(f"{etiqueta}: ningún analista se carga a una bolsa ajena", not ajenos, f"{ajenos[:6]}")
    mal_grupo = sorted({(ag, g) for _, ag, g, _ in cargas if g != ag})
    m.check(f"{etiqueta}: en la V5 el grupo de cada carga es su agente", not mal_grupo, f"{mal_grupo[:6]}")


if "V" in PARTES:
    snaps, cargas, deshacer = instrumentar()
    b = bloque(config_pruebas(diseno="v5", perfiles={"activos": TODOS}, paralelismo={"hilos_analistas": 6}))
    b.ciclo(AS_OF)
    deshacer()
    comprobar_v5("V v5", snaps, cargas)

if "P" in PARTES:
    class Olvidadizo(MockClient):
        def generar(self, **kw):
            with self._lock:
                if len(self.llamadas) % 7 == 6:
                    self._vistos.clear()
            return super().generar(**kw)
    snaps, cargas, deshacer = instrumentar()
    b = bloque(config_pruebas(diseno="v5", perfiles={"activos": TODOS[:6]}, paralelismo={"hilos_analistas": 1}), Olvidadizo())
    b.ciclo(AS_OF)
    deshacer()
    comprobar_v5("P v5 (caché que se pierde)", snaps, cargas)
    escrito = defaultdict(int)
    for bo, ag, _, reales in cargas:
        if ag in ANALISTAS:
            escrito[bo] += reales
    liquidado = defaultdict(float)
    for s in snaps:
        for g, (pesos, reales) in s.items():
            if g in ANALISTAS:
                tot = sum(pesos.values())
                for bo, w in pesos.items():
                    liquidado[bo] += reales * w / tot if tot else 0
    dif = {bo: round(liquidado[bo] - escrito[bo], 3) for bo in sorted(set(escrito) | set(liquidado))}
    reescriben = sorted(bo for bo in escrito if escrito[bo] > min(escrito.values()))
    print(f"   P: tokens escritos por el analista de cada tipo {dict(sorted(escrito.items()))}")
    m.check("P v5: cada tipo paga exactamente lo que escribe su analista (sin mezclar)", all(v == 0 for v in dif.values()), f"{dif}")

if "S" in PARTES:
    snaps, cargas, deshacer = instrumentar()
    b = bloque(config_pruebas(diseno="v6", perfiles={"activos": TODOS}, paralelismo={"hilos_analistas": 6}))
    b.ciclo(AS_OF)
    deshacer()
    grupos = set().union(*[set(s) for s in snaps])
    print(f"   S v6: grupos {sorted(grupos)}")
    m.check("S v6: los analistas comparten el grupo ANALISTAS", "ANALISTAS" in grupos and not (grupos & ANALISTAS), f"{sorted(grupos)}")
    ajenos = sorted({(bo, ag) for bo, ag, _, _ in cargas if ag in ANALISTAS and AGENTE_CLASE.get(bo) != ag})
    m.check("S v6: ningún analista se carga a una bolsa ajena", not ajenos, f"{ajenos[:6]}")
    comp = sorted({(ag, g) for _, ag, g, _ in cargas if ag not in ANALISTAS and g != ag})
    m.check("S v6: cada agente compartido va en su propio grupo", not comp, f"{comp[:6]}")
sys.exit(m.fin())
