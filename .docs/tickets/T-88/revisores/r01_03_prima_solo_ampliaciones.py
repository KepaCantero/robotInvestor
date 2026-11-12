"""QA r01 de T-88 · 03: efectos de la prima «solo» sobre el control de presupuesto (cierres y ampliaciones), 7feb697^ frente a HEAD.

  .venv/bin/python -I .docs/tickets/T-88/revisores/r01_03_prima_solo_ampliaciones.py --base RUTA_11_EJECUTOR_DE_7feb697^

Casos (un hilo, orden determinista también en la base):
  A. V5 N2 con el presupuesto de un tipo justo por encima de lo que necesitaba la base (mínimo de r01_02 + 0,05 UC);
  B. PROFUNDIZACION N3 con los doce tipos y los presupuestos por defecto (N3 / 12 por tipo), V5 y V6.
Para cada uno: cierres parciales, autorizaciones de ampliación (HA, tipo AUT) y consumo final de F5 del tipo."""
import json
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve()
sys.path.insert(0, str(AQUI.parent))
from r01_comun import Marcador, preparar  # noqa: E402

a, resto, ej = preparar(__doc__)
TODOS = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]


def trabajador(o: dict) -> dict:
    from conftest import AS_OF, config_pruebas
    from r01_comun import bloque, f5_presupuesto
    b = bloque(config_pruebas(diseno=o["diseno"], perfiles={"activos": TODOS}, paralelismo={"hilos_analistas": 1}))
    b.ciclo(AS_OF, tipo=o.get("tipo", "PERIODICO"), nivel_forzado=o["nivel"], presupuesto_override=o.get("override"),
            alcance=o.get("alcance"))
    f5e = [e for e in b.almacen.leer("F5") if "presupuesto" in e][-1]
    aut = [{"bolsa": e["bolsa"], "decision": e["decision"], "ampliacion_uc": e["ampliacion_uc"]}
           for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "AUT"]
    return {"presupuesto": f5_presupuesto(b), "cierres": f5e.get("cierres_parciales"), "aut": aut,
            "top3": f5e.get("top3_por_clase")}


if "--trabajador" in resto:
    print("@@" + json.dumps(trabajador(json.loads(resto[resto.index("--trabajador") + 1])), default=str))
    sys.exit(0)
base = Path(resto[resto.index("--base") + 1]) if "--base" in resto else Path("/no-existe")
assert (base / "bloque_a").is_dir(), "indica --base RUTA (11_Ejecutor de 7feb697^)"


def lanzar(ejecutor: Path, o: dict) -> dict:
    p = subprocess.run([sys.executable, "-I", str(AQUI), "--ejecutor", str(ejecutor), "--trabajador", json.dumps(o)],
                       capture_output=True, text=True)
    lineas = [x for x in p.stdout.splitlines() if x.startswith("@@")]
    if not lineas:
        raise RuntimeError(p.stderr[-3000:])
    return json.loads(lineas[-1][2:])


def comparar(nombre, o, bolsas):
    rb, rh = lanzar(base, o), lanzar(ej, o)
    for k in bolsas:
        cb = [c["fase"] for c in rb["cierres"] if c["clase"] == k]
        ch = [c["fase"] for c in rh["cierres"] if c["clase"] == k]
        ab = [x["decision"] for x in rb["aut"] if x["bolsa"] == k]
        ah = [x["decision"] for x in rh["aut"] if x["bolsa"] == k]
        pb, ph = rb["presupuesto"].get(k, {}), rh["presupuesto"].get(k, {})
        print(f"   {nombre} {k}: cierres base {cb} · HEAD {ch} | AUT base {ab} · HEAD {ah} | F5 base {pb} · HEAD {ph}")
        m.check(f"{nombre} {k}: HEAD no cierra más fases que la base", len(ch) <= len(cb), f"{len(cb)} → {len(ch)}")
        m.check(f"{nombre} {k}: HEAD no pide más ampliaciones que la base", len(ah) <= len(ab), f"{len(ab)} → {len(ah)}")
    m.check(f"{nombre}: misma selección que la base", rb["top3"] == rh["top3"])
    return rb, rh


m = Marcador()
# A. mínimos de r01_02 (V5 N2, base): CRI 3,004 · RF 4,029 · DIV 5,219 (asignado sin margen)
for k, minimo in (("CRI", 3.004), ("RF", 4.029), ("DIV", 5.219)):
    comparar(f"A v5 N2 {k}={minimo + 0.05:.3f}", {"diseno": "v5", "nivel": "N2", "override": {k: round(minimo + 0.05, 3)}}, [k])
# B. PROFUNDIZACION N3, doce tipos, presupuestos por defecto
for d in ("v5", "v6"):
    comparar(f"B {d} PROFUNDIZACION N3", {"diseno": d, "nivel": "N3", "tipo": "PROFUNDIZACION", "alcance": {"clases": TODOS}}, TODOS)
sys.exit(m.fin())
