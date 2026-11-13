"""QA r01 de T-88 · 02: ¿la prima «solo» cierra por presupuesto un tipo que antes no cerraba? Compara 7feb697^ con HEAD.

  .venv/bin/python -I .docs/tickets/T-88/revisores/r01_02_cierres_por_presupuesto.py --base RUTA_11_EJECUTOR_DE_7feb697^

Para cada diseño (V5, V6) y nivel (N1, N2), con un hilo (orden determinista también en la base):
  1. mide, por bolsa, el presupuesto mínimo que deja pasar todas las llamadas: max(consumido antes + estimado) sobre las
     llamadas a `Presupuesto.puede` (instrumentado);
  2. compara la selección y los cierres de F5 entre base y HEAD con el presupuesto por defecto;
  3. si en alguna bolsa HEAD necesita más que la base, ejecuta las dos con un override entre los dos mínimos y enseña los
     cierres y el consumo final de F5 (un cierre por presupuesto con consumido final por debajo de lo asignado).
Modo interno: --trabajador JSON (lo lanza el propio script en un subproceso con el ejecutor indicado)."""
import json
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve()
sys.path.insert(0, str(AQUI.parent))
from r01_comun import Marcador, preparar  # noqa: E402

a, resto, ej = preparar(__doc__)
TODOS = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]


def trabajador(orden: dict) -> dict:
    from conftest import AS_OF, config_pruebas
    from bloque_a.consumo import Presupuesto
    from r01_comun import bloque, f5_presupuesto
    registro = {}
    puede_orig = Presupuesto.puede

    def puede(self, clase, estimado):
        with self._lock:
            c = self.consumido[clase]
        registro[clase] = max(registro.get(clase, 0.0), c + estimado)
        return puede_orig(self, clase, estimado)
    Presupuesto.puede = puede
    cfg = config_pruebas(diseno=orden["diseno"], perfiles={"activos": TODOS}, paralelismo={"hilos_analistas": orden.get("hilos", 1)})
    b = bloque(cfg)
    b.ciclo(AS_OF, nivel_forzado=orden["nivel"], presupuesto_override=orden.get("override"))
    f5e = [e for e in b.almacen.leer("F5") if "presupuesto" in e][-1]
    # mínimo «asignado» que deja pasar todo: disponible = asignado·(1 + margen) + ampliado − consumido
    margen = 1 + float(cfg["presupuesto_uc"]["ampliacion_sin_autorizacion"])
    return {"minimo_asignado": {k: round(v / margen, 4) for k, v in registro.items()},
            "presupuesto": f5_presupuesto(b), "cierres": f5e.get("cierres_parciales"),
            "top3": f5e.get("top3_por_clase"), "prg": len(f5e.get("prg_congelados") or [])}


if "--trabajador" in resto:
    print("@@" + json.dumps(trabajador(json.loads(resto[resto.index("--trabajador") + 1])), default=str))
    sys.exit(0)

base = Path(resto[resto.index("--base") + 1]) if "--base" in resto else Path("/no-existe")
assert (base / "bloque_a").is_dir(), "indica --base RUTA (11_Ejecutor de 7feb697^)"


def lanzar(ejecutor: Path, orden: dict) -> dict:
    p = subprocess.run([sys.executable, "-I", str(AQUI), "--ejecutor", str(ejecutor), "--trabajador", json.dumps(orden)],
                       capture_output=True, text=True)
    lineas = [x for x in p.stdout.splitlines() if x.startswith("@@")]
    if not lineas:
        raise RuntimeError(p.stderr[-3000:])
    return json.loads(lineas[-1][2:])


m = Marcador()
for diseno in ("v5", "v6"):
    for nivel in ("N1", "N2"):
        o = {"diseno": diseno, "nivel": nivel}
        rb, rh = lanzar(base, o), lanzar(ej, o)
        print(f"-- {diseno} {nivel}: cierres base {len(rb['cierres'])} · HEAD {len(rh['cierres'])}")
        m.check(f"{diseno} {nivel}: misma selección (top3_por_clase) que la base", rb["top3"] == rh["top3"])
        m.check(f"{diseno} {nivel}: mismos cierres parciales que la base", rb["cierres"] == rh["cierres"],
                f"base {rb['cierres']} · HEAD {rh['cierres']}")
        mb, mh = rb["minimo_asignado"], rh["minimo_asignado"]
        dif = {k: (mb.get(k), mh[k]) for k in mh if mb.get(k) is not None and mh[k] > mb[k] + 1e-3}
        print(f"   bolsas en las que HEAD necesita más presupuesto durante el ciclo que la base: "
              f"{ {k: f'{v[0]:.3f} -> {v[1]:.3f}' for k, v in sorted(dif.items())} }")
        candidatas = [k for k in dif if k in TODOS]
        if not candidatas:
            continue
        bolsa = max(candidatas, key=lambda k: dif[k][1] - dif[k][0])
        lim = round((dif[bolsa][0] + dif[bolsa][1]) / 2, 3)
        o2 = {**o, "override": {bolsa: lim}}
        rb2, rh2 = lanzar(base, o2), lanzar(ej, o2)
        cb = [c for c in rb2["cierres"] if c["clase"] == bolsa]
        ch = [c for c in rh2["cierres"] if c["clase"] == bolsa]
        fin = rh2["presupuesto"][bolsa]
        print(f"   override {bolsa}={lim}: cierres base {cb} · HEAD {ch}")
        print(f"   F5 de HEAD para {bolsa}: {fin}; consumido final de la base {rb2['presupuesto'][bolsa]['consumido']}")
        m.check(f"{diseno} {nivel} override {bolsa}={lim}: HEAD no cierra donde la base no cerraba", len(ch) <= len(cb),
                f"base {len(cb)} cierres · HEAD {len(ch)}; consumido final HEAD {fin['consumido']} <= asignado {fin['asignado']}")
        m.check(f"{diseno} {nivel} override: misma selección que la base", rb2["top3"] == rh2["top3"])
sys.exit(m.fin())
