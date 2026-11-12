"""QA r01 de T-88 · 01: determinismo del consumo por tipo de F5 con más hilos y más perfiles (V5 y V6), y total cargado
frente al coste real.

  .venv/bin/python -I .docs/tickets/T-88/revisores/r01_01_determinismo_y_total.py [--ejecutor RUTA] [--rapido]

Con --ejecutor apuntando a un worktree de 7feb697^ sirve de control: allí el consumo por tipo debe cambiar entre ejecuciones."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import Marcador, bloque, f5_presupuesto, huella, preparar  # noqa: E402

a, _, ej = preparar(__doc__)
from conftest import AS_OF, config_pruebas  # noqa: E402

TODOS = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]
m = Marcador()
hilos_lista = [1, 6, 12] if a.rapido else [1, 3, 6, 12]
reps = 2 if a.rapido else 3
for diseno in ("v5", "v6"):
    vistos, vistos_cierres = {}, {}
    for h in hilos_lista:
        for k in range(reps if h > 1 else 1):
            b = bloque(config_pruebas(diseno=diseno, perfiles={"activos": TODOS}, paralelismo={"hilos_analistas": h}))
            b.ciclo(AS_OF)
            f5 = f5_presupuesto(b)
            vistos.setdefault(huella(f5), []).append(f"h{h}#{k}")
            real = sum(x["uc"] for x in b.contabilidad.llamadas)
            cargado = sum(x["consumido"] for x in f5.values())
            if h == 12 and k == 0:
                # Llamadas sin bolsa: las de después del registro de F5 (declaradas en el README para la V5)
                print(f"   {diseno}: cargado {cargado:.4f} · real {real:.4f} · diferencia {real - cargado:.4f}", flush=True)
                if diseno == "v6":
                    m.check("CA-2 v6: total cargado = coste real (±0,01)", abs(cargado - real) <= 0.01, f"{cargado:.4f} vs {real:.4f}")
                else:
                    m.check("v5: lo cargado no supera el coste real y la diferencia es pequeña (<= 3,5 UC)",
                            -0.01 <= real - cargado <= 3.5, f"{real - cargado:.4f}")
            cierres = [e for e in b.almacen.leer("F5") if "presupuesto" in e][-1].get("cierres_parciales")
            vistos_cierres.setdefault(huella(cierres), []).append(f"h{h}#{k}")
    m.check(f"CA-1 {diseno}: el mismo presupuesto de F5 con hilos {hilos_lista} y {reps} repeticiones",
            len(vistos) == 1, f"{len(vistos)} variantes: {list(vistos.values())}")
    m.check(f"{diseno}: los mismos cierres parciales en todas las ejecuciones", len(vistos_cierres) == 1,
            f"{len(vistos_cierres)} variantes")
sys.exit(m.fin())
