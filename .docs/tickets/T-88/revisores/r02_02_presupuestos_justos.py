"""QA r02 de T-88 · 02: presupuestos justos frente a 7feb697^ (antes de T-88): cierres, ampliaciones, selección, determinismo
con varios hilos y bolsas que acaban por encima de su límite tras liquidar.

  .venv/bin/python -I .docs/tickets/T-88/revisores/r02_02_presupuestos_justos.py --base RUTA_11_EJECUTOR_DE_7feb697^ [--ejecutor RUTA] [--rapido]

1. Para V5 y V6 (N2, doce tipos, PERIODICO), mide en la base y en HEAD el presupuesto mínimo por tipo que deja pasar todas
   las llamadas (instrumentando `Presupuesto.puede`, como r01_02).
2. Barrido: todos los tipos a la vez con su mínimo de la BASE + δ (δ en UC, de −0,4 a +0,4) y un hilo (orden determinista
   en la base). Por tipo: HEAD no cierra más fases ni pide más ampliaciones AUT que la base (CA-5); se cuenta la selección
   distinta.
3. Determinismo con presupuestos justos: cada δ en HEAD con 1, 6 y 12 hilos da el mismo presupuesto de F5, cierres (como
   conjunto), AUT (como conjunto) y selección (CA-1); el orden de los cierres de F5 entre hilos se cuenta aparte.
4. Límite tras liquidar: bolsas cuyo consumo final supera asignado × (1 + margen automático) + ampliado, en la base y en
   HEAD, y por cuánto (lo que el control no vio durante la fase).
Modo interno: --trabajador JSON."""
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
    from bloque_a.consumo import Presupuesto
    from r01_comun import bloque, f5_presupuesto
    registro: dict = {}
    puede_orig = Presupuesto.puede

    def puede(self, clase, estimado):
        with self._lock:
            c = self.consumido[clase]
        registro[clase] = max(registro.get(clase, 0.0), c + estimado)
        return puede_orig(self, clase, estimado)
    Presupuesto.puede = puede
    cfg = config_pruebas(diseno=o["diseno"], perfiles={"activos": TODOS}, paralelismo={"hilos_analistas": o.get("hilos", 1)})
    b = bloque(cfg)
    b.ciclo(AS_OF, tipo=o.get("tipo", "PERIODICO"), nivel_forzado=o["nivel"], presupuesto_override=o.get("override"),
            alcance=o.get("alcance"))
    f5e = [e for e in b.almacen.leer("F5") if "presupuesto" in e][-1]
    margen = 1 + float(cfg["presupuesto_uc"]["ampliacion_sin_autorizacion"])
    pres = f5_presupuesto(b)
    exceso = {k: round(v["consumido"] - (v["asignado"] * margen + v["ampliado"]), 4) for k, v in pres.items()
              if k in TODOS and v["consumido"] > v["asignado"] * margen + v["ampliado"] + 1e-6}
    aut = [{"bolsa": e["bolsa"], "decision": e["decision"]} for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "AUT"]
    return {"minimo_asignado": {k: round(v / margen, 4) for k, v in registro.items()}, "presupuesto": pres,
            "cierres": f5e.get("cierres_parciales"), "top3": f5e.get("top3_por_clase"), "aut": aut, "exceso": exceso}


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


def por_tipo(r, k):
    return ([c["fase"] for c in r["cierres"] if c["clase"] == k], [x["decision"] for x in r["aut"] if x["bolsa"] == k])


m = Marcador()
deltas = [-0.2, 0.0, 0.1, 0.3] if a.rapido else [-0.4, -0.2, -0.1, 0.0, 0.05, 0.1, 0.2, 0.4]
for diseno in ("v5", "v6"):
    o = {"diseno": diseno, "nivel": "N2"}
    rb, rh = lanzar(base, o), lanzar(ej, o)
    mb, mh = rb["minimo_asignado"], rh["minimo_asignado"]
    print(f"-- {diseno} N2 mínimos por tipo (base → HEAD): "
          + ", ".join(f"{k} {mb.get(k, 0):.3f}→{mh.get(k, 0):.3f}" for k in TODOS))
    m.check(f"{diseno}: con los presupuestos por defecto, mismos cierres y selección que la base",
            rb["cierres"] == rh["cierres"] and rb["top3"] == rh["top3"])
    mas_cierres, mas_aut, sel_dif, menos_cierres, no_det, orden_cierres = [], [], 0, [], [], []
    exc_b, exc_h = {}, {}
    for d in deltas:
        ov = {k: round(mb[k] + d, 3) for k in TODOS if k in mb}
        o2 = {**o, "override": ov}
        rb2 = lanzar(base, o2)
        rh2 = {h: lanzar(ej, {**o2, "hilos": h}) for h in (1, 6, 12)}
        r1 = rh2[1]
        for k in TODOS:
            (cb, ab), (ch, ah) = por_tipo(rb2, k), por_tipo(r1, k)
            if len(ch) > len(cb):
                mas_cierres.append(f"δ={d} {k}: base {cb} · HEAD {ch}")
            if len(ch) < len(cb):
                menos_cierres.append(f"δ={d} {k}: base {cb} · HEAD {ch}")
            if len(ah) > len(ab):
                mas_aut.append(f"δ={d} {k}: base {ab} · HEAD {ah}")
        sel_dif += sum(1 for k in TODOS if (rb2["top3"] or {}).get(k) != (r1["top3"] or {}).get(k))
        # las AUT de HA y los cierres parciales de F5 se escriben en el orden en que llegan los hilos (anterior a T-88): el
        # contenido se compara como conjunto y el orden se cuenta aparte
        firmas = {h: json.dumps([r["presupuesto"], sorted(map(json.dumps, r["cierres"])), r["top3"], sorted(map(json.dumps, r["aut"]))],
                                sort_keys=True) for h, r in rh2.items()}
        if len(set(firmas.values())) > 1:
            no_det.append(f"δ={d}")
        if len({json.dumps(r["cierres"]) for r in rh2.values()}) > 1:
            orden_cierres.append(f"δ={d}")
        for k, v in rb2["exceso"].items():
            exc_b[f"δ={d} {k}"] = v
        for k, v in r1["exceso"].items():
            exc_h[f"δ={d} {k}"] = v
        print(f"   δ={d:+.2f}: cierres base {len(rb2['cierres'])} · HEAD {len(r1['cierres'])}; AUT base {len(rb2['aut'])} · "
              f"HEAD {len(r1['aut'])}; tipos por encima del límite base {len(rb2['exceso'])} · HEAD {len(r1['exceso'])}", flush=True)
    m.check(f"CA-5 {diseno}: con presupuestos justos, HEAD no cierra ninguna fase que la base no cerrase", not mas_cierres,
            f"{len(mas_cierres)}: {mas_cierres[:6]}")
    m.check(f"{diseno}: HEAD no pide más ampliaciones AUT que la base", not mas_aut, f"{len(mas_aut)}: {mas_aut[:6]}")
    print(f"   {diseno}: tipos con MENOS cierres en HEAD que en la base: {len(menos_cierres)}: {menos_cierres[:8]}")
    print(f"   {diseno}: tipos con selección distinta de la base: {sel_dif}")
    m.check(f"CA-1 {diseno}: con presupuestos justos, el mismo presupuesto de F5, cierres, AUT y selección con 1, 6 y 12 hilos", not no_det,
            f"distintos en {no_det}")
    print(f"   {diseno}: orden de `cierres_parciales` de F5 distinto entre hilos (mismo contenido; anterior a T-88): {orden_cierres}")
    print(f"   {diseno}: por encima del límite tras liquidar · base {len(exc_b)} (máx {max(exc_b.values(), default=0):.4f}) · "
          f"HEAD {len(exc_h)} (máx {max(exc_h.values(), default=0):.4f}); base {exc_b} · HEAD {exc_h}")
    nuevos = {k: v for k, v in exc_h.items() if v > exc_b.get(k, 0) + 1e-4}
    print(f"   {diseno}: HEAD por encima del límite donde la base no lo estaba (o más): {len(nuevos)}: "
          f"{dict(list(sorted(nuevos.items(), key=lambda x: -x[1]))[:8])}")
    m.check(f"{diseno}: HEAD no deja más bolsas por encima de su límite que la base", len(nuevos) == 0, f"{len(nuevos)}")
sys.exit(m.fin())
