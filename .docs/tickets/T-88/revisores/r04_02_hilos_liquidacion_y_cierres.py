"""QA r04 de T-88 · 02: el registro entero de F5 (no solo `presupuesto`) con varios hilos y presupuestos justos, la
liquidación grupo a grupo con lo que de verdad llega a ella, y desde qué hilos se carga cada bolsa.

  .venv/bin/python -I .docs/tickets/T-88/revisores/r04_02_hilos_liquidacion_y_cierres.py [--ejecutor RUTA] [--rapido]

Doce perfiles, N2, PERIODICO. Para V5 y V6 y dos presupuestos justos por tipo (override igual para los doce; elegidos para
que haya cierres parciales y ampliaciones AUT), con 1, 2, 5, 6 y 12 hilos (y 6 dos veces):
  D · el RUN de F5 entero (sin claves internas ni rutas temporales: `presupuesto`, `consumo`, `participantes`,
      `cierres_parciales`, selección…), F2, F3 y F4 son idénticos en todas las ejecuciones; las AUT de HA, como conjunto
      (su orden de llegada está declarado en `analisis-tecnico.md`);
  L · en cada liquidación (espiada): cada grupo reparte exactamente sus tokens reales (a la bolsa común si no tiene pesos);
      cada bolsa termina con lo que tenía + su parte de cada grupo − lo que cargó durante la fase; la suma total cambia en
      prima(reales) − prima(cargadas); una segunda liquidación no cambia nada; en la V5, en el grupo de un analista solo pesa
      su tipo; en la V6 ningún analista es su propio grupo;
  H · durante la fase en paralelo, cada bolsa recibe cargas de un solo hilo (si no, el orden de las sumas en coma flotante
      dependería de los hilos);
  T · lo cargado a las bolsas es el coste real de las llamadas que pasan por el presupuesto (todas salvo AG-12), ±0,01 UC;
  V · la V5 con presupuestos justos no cierra fases nuevas frente a la r03 (el mismo código: solo cambia el RUN de F5)."""
import json
import sys
import tempfile
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import Marcador, bloque, preparar  # noqa: E402

a, resto, ej = preparar(__doc__)
from conftest import AS_OF, config_pruebas  # noqa: E402

from bloque_a.consumo import Presupuesto  # noqa: E402
from bloque_a.orquestacion import AGENTE_CLASE  # noqa: E402

TODOS = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]
JUSTOS = {"v5": [3.0, 3.6], "v6": [1.4, 1.7]}
HILOS = [1, 6, 12] if a.rapido else [1, 2, 5, 6, 6, 12]
ANALISTAS = set(AGENTE_CLASE.values())
m = Marcador()


def limpio(obj):
    if isinstance(obj, dict):
        return {k: limpio(v) for k, v in obj.items() if not k.startswith("_")}
    if isinstance(obj, list):
        return [limpio(v) for v in obj]
    if isinstance(obj, str) and obj.startswith(tempfile.gettempdir()):
        return Path(obj).name
    return obj


# ---------------------------------------------------------------- espías (liquidación e hilos por bolsa)
LIQ: list = []
HILOS_BOLSA: dict = {}
FASE = {"paralela": False}
orig_liq, orig_ccp, orig_cargar = Presupuesto.liquidar_primas, Presupuesto.cargar_con_prima, Presupuesto.cargar


def esp_liq(self):
    antes = dict(self.consumido)
    pesos = {g: dict(p) for g, p in self._pesos.items()}
    reales, cargadas = dict(self._reales), dict(self._cargadas)
    orig_liq(self)
    despues = dict(self.consumido)
    orig_liq(self)   # segunda liquidación: no debe cambiar nada
    LIQ.append({"antes": antes, "despues": despues, "otra": dict(self.consumido), "pesos": pesos, "reales": reales,
                "cargadas": cargadas, "prima": self._uc_prima})
    FASE["paralela"] = False


def anotar(bolsa):
    if FASE["paralela"]:
        HILOS_BOLSA.setdefault(bolsa, set()).add(threading.get_ident())


def esp_ccp(self, bolsa, *aa, **kk):
    anotar(bolsa)
    return orig_ccp(self, bolsa, *aa, **kk)


def esp_cargar(self, bolsa, uc):
    anotar(bolsa)
    return orig_cargar(self, bolsa, uc)


Presupuesto.liquidar_primas, Presupuesto.cargar_con_prima, Presupuesto.cargar = esp_liq, esp_ccp, esp_cargar
orig_init = Presupuesto.__init__


def esp_init(self, *aa, **kk):
    orig_init(self, *aa, **kk)
    FASE["paralela"] = True   # el Presupuesto se crea justo antes de la fase en paralelo


Presupuesto.__init__ = esp_init


def ejecutar(diseno, hilos, justo):
    b = bloque(config_pruebas(diseno=diseno, perfiles={"activos": TODOS}, paralelismo={"hilos_analistas": hilos}))
    LIQ.clear()
    HILOS_BOLSA.clear()
    b.ciclo(AS_OF, nivel_forzado="N2", presupuesto_override={c: justo for c in TODOS})
    run = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "RUN"][-1]
    aut = sorted(json.dumps(limpio({k: v for k, v in e.items() if k != "id"}), sort_keys=True)
                 for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "AUT")
    huella = json.dumps({"run": limpio(run), **{f: limpio(b.almacen.leer(f)) for f in ("F2", "F3", "F4")}}, sort_keys=True, default=str)
    real = sum(x["uc"] for x in b.contabilidad.llamadas if x["agente"] != "AG-12")   # AG-12 se invoca sin presupuesto (r04_01)
    cargado = sum(v["consumido"] for v in run["presupuesto"].values())
    return {"huella": huella, "aut": aut, "run": limpio(run), "liq": list(LIQ), "hilos_bolsa": {k: len(v) for k, v in HILOS_BOLSA.items()},
            "real": real, "cargado": cargado}


def comprobar_liq(d, etiqueta, liqs):
    malos = []
    for i, L in enumerate(liqs):
        prima = L["prima"]
        esperado = dict(L["antes"])
        for g, reales in L["reales"].items():
            pesos = L["pesos"].get(g, {})
            tot = sum(pesos.values())
            if not tot:
                esperado["COMUN"] = esperado.get("COMUN", 0.0) + prima(reales)
                continue
            reparto = 0.0
            for bolsa, w in pesos.items():
                parte = prima(reales * w / tot)
                esperado[bolsa] = esperado.get(bolsa, 0.0) + parte
                reparto += parte
            if abs(reparto - prima(reales)) > 1e-9:
                malos.append(f"#{i} grupo {g} reparte {reparto} de {prima(reales)}")
            if d == "v5" and g in ANALISTAS and set(pesos) - {c for c, ag in AGENTE_CLASE.items() if ag == g}:
                malos.append(f"#{i} V5: en el grupo del analista {g} pesan {sorted(pesos)}")
            if d == "v6" and g in ANALISTAS:
                malos.append(f"#{i} V6: el analista {g} es su propio grupo")
        for bolsa, t in L["cargadas"].items():
            esperado[bolsa] = esperado.get(bolsa, 0.0) - prima(t)
        for bolsa in set(esperado) | set(L["despues"]):
            if abs(esperado.get(bolsa, 0.0) - L["despues"].get(bolsa, 0.0)) > 1e-9:
                malos.append(f"#{i} {bolsa}: esperado {esperado.get(bolsa)} obtenido {L['despues'].get(bolsa)}")
        delta = sum(L["despues"].values()) - sum(L["antes"].values())
        if abs(delta - (prima(sum(L["reales"].values())) - prima(sum(L["cargadas"].values())))) > 1e-9:
            malos.append(f"#{i} la suma cambia {delta}")
        if L["otra"] != L["despues"]:
            malos.append(f"#{i} una segunda liquidación cambia {sorted(k for k in L['otra'] if L['otra'][k] != L['despues'].get(k))}")
    m.check(f"L {etiqueta}: liquidaciones exactas grupo a grupo e idempotentes ({len(liqs)} liquidaciones)", not malos, "; ".join(malos[:6]))


ref_v5 = {}
for diseno in ("v5", "v6"):
    for justo in JUSTOS[diseno]:
        et = f"{diseno} justo={justo}"
        res = {h_i: ejecutar(diseno, h, justo) for h_i, h in enumerate(HILOS)}
        r0 = res[0]
        cierres, nauts = len(r0["run"]["cierres_parciales"]), len(r0["aut"])
        dist = [HILOS[i] for i, r in res.items() if r["huella"] != r0["huella"]]
        detalle = ""
        if dist:
            r1 = res[next(i for i, r in res.items() if r["huella"] != r0["huella"])]
            j0, j1 = json.loads(r0["huella"]), json.loads(r1["huella"])
            detalle = f"partes distintas: {[k for k in j0 if j0[k] != j1[k]]}; RUN: {[k for k in j0['run'] if j0['run'][k] != j1['run'].get(k)]}"
        m.check(f"D {et}: el mismo RUN de F5 entero, F2, F3 y F4 con hilos {HILOS} ({cierres} cierres, {nauts} AUT)", not dist,
                detalle or f"distintos con hilos {dist}")
        m.check(f"D {et}: las mismas AUT (como conjunto)", all(r["aut"] == r0["aut"] for r in res.values()))
        peor = max(abs(r["cargado"] - r["real"]) for r in res.values())
        m.check(f"T {et}: cargado = coste real de las llamadas con presupuesto (±0,01), con cualquier número de hilos", peor <= 0.01,
                f"peor diferencia {peor:.4f} UC")
        comprobar_liq(diseno, et, [L for r in res.values() for L in r["liq"]])
        varios = {i: {b: n for b, n in r["hilos_bolsa"].items() if n > 1} for i, r in res.items()}
        varios = {HILOS[i]: v for i, v in varios.items() if v}
        m.check(f"H {et}: durante la fase en paralelo cada bolsa se carga desde un solo hilo", not varios, f"{varios}")
        if diseno == "v5":
            ref_v5[justo] = r0["run"]
        print(f"NOTA  {et}: cierres {[(c['clase'], c['fase']) for c in r0['run']['cierres_parciales']]}", flush=True)

# V · frente a la r03, si se da --previo (otro 11_Ejecutor): mismos cierres y AUT con presupuestos justos en la V5
if "--previo" in resto:
    import subprocess
    previo = resto[resto.index("--previo") + 1]
    codigo = f"""
import sys, json, tempfile
sys.path[:0] = [{str(Path(previo) / 'tests')!r}, {previo!r}, {str(Path(__file__).resolve().parent)!r}]
from conftest import AS_OF, config_pruebas
from r01_comun import bloque
out = {{}}
for justo in {JUSTOS['v5']!r}:
    b = bloque(config_pruebas(diseno='v5', perfiles={{'activos': {TODOS!r}}}, paralelismo={{'hilos_analistas': 6}}))
    b.ciclo(AS_OF, nivel_forzado='N2', presupuesto_override={{c: justo for c in {TODOS!r}}})
    run = [e for e in b.almacen.leer('F5') if e.get('tipo_entrada') == 'RUN'][-1]
    out[str(justo)] = {{'cierres': run['cierres_parciales'], 'presupuesto': run['presupuesto'], 'top3': run['top3_por_clase']}}
print('@@' + json.dumps(out))
"""
    p = subprocess.run([sys.executable, "-I", "-c", codigo], capture_output=True, text=True)
    lin = [x for x in p.stdout.splitlines() if x.startswith("@@")]
    if not lin:
        m.check("V: el control --previo se ejecuta", False, p.stderr[-1500:])
    else:
        prev = json.loads(lin[0][2:])
        for justo, run in ref_v5.items():
            pv = prev[str(justo)]
            m.check(f"V v5 justo={justo}: los mismos cierres, presupuesto y selección que la r03",
                    (run["cierres_parciales"], run["presupuesto"], run["top3_por_clase"]) == (pv["cierres"], pv["presupuesto"], pv["top3"]))
sys.exit(m.fin())
