"""QA r04 de T-88 · 01: F5 y el resto de almacenes con la misma forma que antes de T-88 (salvo lo declarado), el `consumo`
del RUN con los mismos valores, y el total cargado a las bolsas igual al coste real de las llamadas hechas hasta F5.

  .venv/bin/python -I .docs/tickets/T-88/revisores/r04_01_f5_estructura_y_total.py --base RUTA_11_EJECUTOR_DE_7feb697^ \
      [--previo RUTA_11_EJECUTOR_DE_0afab6f] [--ejecutor RUTA]

Cada ejecutor corre en su propio subproceso (--trabajador), con los doce perfiles, un hilo y V5 y V6. Comprobaciones:
  E · forma: para cada almacén (F1…, HA…) y cada `tipo_entrada`, el conjunto de rutas de claves (anidadas; las listas como
      «[]») es el mismo en HEAD y en la base. Lo único que puede cambiar es el VALOR de `presupuesto.*.consumido`;
  C · valores: el `consumo`, los `participantes`, la selección (`top3_por_clase`), los `cierres_parciales` y el `asignado` y
      `ampliado` de cada bolsa del RUN son idénticos a la base (T-88 no toca la contabilidad de llamadas);
  P · con --previo (la r03): el RUN de HEAD es el de la r03 más `consumo`, y nada más cambia en ningún almacén;
  T · total: lo cargado a las bolsas (suma de `consumido` del RUN) frente al coste real de las llamadas registradas antes de
      escribir el RUN (V5 y V6, ±0,01 UC), y qué agentes llaman después de F5 (declarado: AG-18, AG-19 y AG-20 en la V5)."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve()
sys.path.insert(0, str(AQUI.parent))
from r01_comun import Marcador, preparar  # noqa: E402

a, resto, ej = preparar(__doc__)
TODOS = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]


def rutas(obj, pref=""):
    if isinstance(obj, dict):
        out = {pref or "."}
        for k, v in obj.items():
            out |= rutas(v, f"{pref}.{k}")
        return out
    if isinstance(obj, list):
        out = {pref + "[]"}
        for v in obj:
            out |= rutas(v, pref + "[]")
        return out
    return {pref}


def sin_volatiles(obj):
    """Sin las claves internas (`_hash`, `_ts`…), sin el criterio de resolución congelado en cada PRG (lo cambia T-91 en el
    mismo commit) y con las rutas de los entregables reducidas a su nombre (cada ejecución usa una carpeta temporal)."""
    if isinstance(obj, dict):
        return {k: sin_volatiles(v) for k, v in obj.items() if not k.startswith("_") and k != "criterio_resolucion"}
    if isinstance(obj, list):
        return [sin_volatiles(v) for v in obj]
    if isinstance(obj, str) and obj.startswith(tempfile.gettempdir()):
        return Path(obj).name
    return obj


def trabajador(o: dict) -> dict:
    from conftest import AS_OF, config_pruebas
    from bloque_a.almacen import ARCHIVOS, Almacen
    from r01_comun import bloque
    salida = {}
    for diseno in ("v5", "v6"):
        b = bloque(config_pruebas(diseno=diseno, perfiles={"activos": TODOS}, paralelismo={"hilos_analistas": 1}))
        corte = {}
        orig = Almacen.escribir

        def espia(self, archivo, autor, entrada, *aa, **kk):
            if archivo == "F5" and isinstance(entrada, dict) and entrada.get("tipo_entrada") == "RUN" and "n" not in corte:
                corte["n"] = len(b.contabilidad.llamadas)
            return orig(self, archivo, autor, entrada, *aa, **kk)
        Almacen.escribir = espia
        try:
            b.ciclo(AS_OF)
        finally:
            Almacen.escribir = orig
        forma, todo = {}, {}
        for f in sorted(ARCHIVOS):
            try:
                ents = b.almacen.leer(f)
            except Exception:
                continue
            for e in ents:
                t = f"{f}:{e.get('tipo_entrada', '-')}" if isinstance(e, dict) else f
                forma.setdefault(t, set()).update(rutas(e))
            todo[f] = sin_volatiles(ents)
        run = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "RUN"][-1]
        ll = b.contabilidad.llamadas
        n = corte.get("n", len(ll))
        salida[diseno] = {
            "forma": {k: sorted(v) for k, v in forma.items()}, "todo": todo, "run": sin_volatiles(run),
            "real_hasta_f5": round(sum(x["uc"] for x in ll[:n]), 4), "real_total": round(sum(x["uc"] for x in ll), 4),
            "despues_f5": sorted({x["agente"] for x in ll[n:]}), "n_llamadas": len(ll), "n_hasta_f5": n, "espia": "n" in corte,
            "real_por_agente": {k: round(sum(x["uc"] for x in ll[:n] if x["agente"] == k), 4) for k in sorted({x["agente"] for x in ll})}}
    return salida


if "--trabajador" in resto:
    print("@@" + json.dumps(trabajador(json.loads(resto[resto.index("--trabajador") + 1])), default=str))
    sys.exit(0)


def lanzar(ejecutor: str) -> dict:
    p = subprocess.run([sys.executable, "-I", str(AQUI), "--ejecutor", ejecutor, "--trabajador", "{}"], capture_output=True,
                       text=True, env={**os.environ})
    lin = [x for x in p.stdout.splitlines() if x.startswith("@@")]
    if not lin:
        sys.exit(f"trabajador sin salida ({ejecutor}):\n{p.stderr[-3000:]}")
    return json.loads(lin[0][2:])


base = resto[resto.index("--base") + 1]
previo = resto[resto.index("--previo") + 1] if "--previo" in resto else None
H = lanzar(str(ej))
B = lanzar(base)
P = lanzar(previo) if previo else None
m = Marcador()
for d in ("v5", "v6"):
    h, bb = H[d], B[d]
    # E · forma
    tipos = sorted(set(h["forma"]) | set(bb["forma"]))
    difs = {t: {"faltan": sorted(set(bb["forma"].get(t, [])) - set(h["forma"].get(t, []))),
                "sobran": sorted(set(h["forma"].get(t, [])) - set(bb["forma"].get(t, [])))} for t in tipos}
    difs = {t: v for t, v in difs.items() if v["faltan"] or v["sobran"]}
    m.check(f"E {d}: misma forma que antes de T-88 en todos los almacenes y tipos de entrada", not difs,
            json.dumps(difs, ensure_ascii=False)[:1500] if difs else f"{len(tipos)} tipos de entrada")
    # C · valores
    for clave in ("consumo", "participantes", "top3_por_clase", "cierres_parciales"):
        m.check(f"C {d}: `{clave}` del RUN igual que antes de T-88", h["run"].get(clave) == bb["run"].get(clave),
                "" if h["run"].get(clave) == bb["run"].get(clave) else f"HEAD={str(h['run'].get(clave))[:300]} base={str(bb['run'].get(clave))[:300]}")
    pres_h = {k: {x: v[x] for x in ("asignado", "ampliado")} for k, v in h["run"]["presupuesto"].items()}
    pres_b = {k: {x: v[x] for x in ("asignado", "ampliado")} for k, v in bb["run"]["presupuesto"].items()}
    m.check(f"C {d}: bolsas, `asignado` y `ampliado` iguales que antes de T-88", pres_h == pres_b)
    otras = sorted(f for f in set(h["todo"]) | set(bb["todo"]) if f != "F5" and h["todo"].get(f) != bb["todo"].get(f))
    print(f"NOTA  C {d}: almacenes con valores distintos de la base (entre la base y HEAD hay otros tickets): {otras}")
    cargado_b = round(sum(v["consumido"] for v in bb["run"]["presupuesto"].values()), 4)
    print(f"NOTA  T {d}: en la base, cargado={cargado_b} frente a real hasta F5={bb['real_hasta_f5']} (espía F5: {bb['espia']})")
    # P · frente a la r03
    if P:
        p = P[d]
        quitado = {k: v for k, v in h["run"].items() if k != "consumo"}
        m.check(f"P {d}: el RUN de HEAD es el de la r03 más `consumo`", quitado == p["run"] and "consumo" not in p["run"],
                f"claves distintas: {sorted(k for k in set(quitado) | set(p['run']) if quitado.get(k) != p['run'].get(k))}")
        otras = sorted(f for f in set(h["todo"]) | set(p["todo"]) if f != "F5" and h["todo"].get(f) != p["todo"].get(f))
        m.check(f"P {d}: los demás almacenes iguales que en la r03", not otras, f"distintos: {otras}")
    # T · total
    cargado = round(sum(v["consumido"] for v in h["run"]["presupuesto"].values()), 4)
    m.check(f"T {d}: cargado a las bolsas = coste real de las llamadas hasta F5 (±0,01)", abs(cargado - h["real_hasta_f5"]) <= 0.01,
            f"cargado={cargado} real_hasta_F5={h['real_hasta_f5']} real_total={h['real_total']} "
            f"llamadas={h['n_hasta_f5']}/{h['n_llamadas']} después de F5: {h['despues_f5']}")
    sin_12 = round(h["real_hasta_f5"] - h["real_por_agente"].get("AG-12", 0.0), 4) if d == "v5" else h["real_hasta_f5"]
    m.check(f"T {d}: cargado = coste real hasta F5 sin la curación AG-12, que se invoca sin presupuesto (±0,01)",
            abs(cargado - sin_12) <= 0.01, f"cargado={cargado} real sin AG-12={sin_12}")
    m.check(f"T {d}: el `consumo.uc_llm` del RUN es el coste real de las llamadas hasta F5",
            abs(h["run"]["consumo"]["uc_llm"] - h["real_hasta_f5"]) <= 0.0002, f"uc_llm={h['run']['consumo']['uc_llm']}")
    m.check(f"T {d}: el espía de F5 se disparó", h["espia"])
    print(f"NOTA  T {d}: coste real por agente hasta F5: {h['real_por_agente']}")
    permitidos = {"AG-18", "AG-19", "AG-20"}
    m.check(f"T {d}: después de F5 solo llaman AG-18, AG-19 o AG-20", set(h["despues_f5"]) <= permitidos, f"{h['despues_f5']}")
sys.exit(m.fin())
