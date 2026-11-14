"""QA r01 de T-113 · H-14, H-15 y H-16 de T-107: con presupuestos justos y 1, 6, 12 y 6 hilos, el `consumo` del RUN de F5 y
las `limitaciones` del paquete son idénticos; y la curación de AG-12 pasa por el presupuesto (lo cargado a las bolsas es el
coste de todas las llamadas).
Uso: cd <árbol>/bloque_a/11_Ejecutor && python <este script> [v5|v6|todo]   (sirve también sobre 3a5fbfe^ para comparar)"""
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "tests")
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402
from conftest import AS_OF, DATOS, config_pruebas  # noqa: E402

TODOS = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]
que = sys.argv[1] if len(sys.argv) > 1 else "v5"
PLAN = {"v5": [("v5", 3.0), ("v5", 3.6), ("v5", None)], "v6": [("v6", 1.4)], "todo": [("v5", 3.0), ("v5", 3.6), ("v5", None), ("v6", 1.4), ("v6", 1.7)]}[que]
fallos = 0
for diseno, justo in PLAN:
    vistos_c, vistos_l, vistos_cz = {}, {}, {}
    for hilos in (1, 6, 12, 6):
        tmp = Path(tempfile.mkdtemp(prefix="qa_t113_hilos_", dir=os.environ.get("QA_TMP")))
        b = Bloque(config_pruebas(diseno=diseno, perfiles={"activos": TODOS}, paralelismo={"hilos_analistas": hilos}),
                   ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "estado", tmp / "ent")
        kw = {"presupuesto_override": {c: justo for c in TODOS}} if justo is not None else {}
        espia = []
        orig = b._invocar

        def invocar(agente, *a, _o=orig, _e=espia, **k):
            # posición 8 (tras agente): presupuesto
            pres = k.get("presupuesto", a[8] if len(a) > 8 else None)
            if agente == "AG-12":
                _e.append(pres is not None)
            return _o(agente, *a, **k)
        b._invocar = invocar
        res = b.ciclo(AS_OF, nivel_forzado="N2", **kw)
        run = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "RUN"][-1]
        cons = {k: v for k, v in run["consumo"].items() if k not in ("latencia_s",)}
        lims = res["paquete"]["limitaciones"]
        vistos_c.setdefault(json.dumps(cons, sort_keys=True, default=str), []).append(hilos)
        vistos_l.setdefault(json.dumps(lims, ensure_ascii=False), []).append(hilos)
        vistos_cz.setdefault(json.dumps(run.get("cierres_parciales"), sort_keys=True, ensure_ascii=False, default=str), []).append(hilos)
        cargado = sum(v for v in (run["presupuesto"].get("consumido") or {}).values()) if isinstance(run.get("presupuesto"), dict) else None
        n_pres = sum(1 for x in lims if x.startswith("Presupuesto agotado"))
        print(f"  {diseno} justo={justo} hilos={hilos}: uc={run['consumo'].get('uc')} uc_llm={run['consumo'].get('uc_llm')} "
              f"cargado a bolsas={cargado if cargado is None else round(cargado, 4)} · limitaciones de presupuesto: {n_pres} · "
              f"AG-12: {len(espia)} llamadas, con presupuesto {sum(espia)}", flush=True)
    for nombre, v in (("consumo", vistos_c), ("limitaciones", vistos_l), ("cierres_parciales", vistos_cz)):
        mal = len(v) != 1
        fallos += mal
        print(f"{'FALLO' if mal else 'ok   '} {diseno} justo={justo}: {nombre} idéntico con 1, 6, 12 y 6 hilos ({len(v)} variantes: {list(v.values())})")
        if mal and nombre != "limitaciones":
            ks = list(v)
            a, bb = json.loads(ks[0]), json.loads(ks[1])
            if isinstance(a, dict):
                print("      difieren:", {k: (a[k], bb.get(k)) for k in a if a[k] != bb.get(k)})
print("FALLOS:", fallos)
