"""QA r02 de T-88 · 01: determinismo con 1, 3, 6 y 12 hilos (V5 y V6, doce perfiles), también de lo que ve el control
DURANTE la fase en paralelo, y total cargado frente al coste real.

  .venv/bin/python -I .docs/tickets/T-88/revisores/r02_01_determinismo_fase_y_total.py [--ejecutor RUTA] [--rapido]

Para cada ejecución guarda:
  · el `presupuesto` y los cierres de F5;
  · el consumo por bolsa justo ANTES de la liquidación que sigue a la fase en paralelo (lo que ha visto el control de
    presupuesto de cada tipo durante la fase) y justo después;
  · lo cargado frente al coste real de las llamadas hechas hasta ese momento y al final.
Esperado (CA-1, CA-2, CA-5): todo idéntico entre hilos y repeticiones; en V6, total = real (±0,01); antes de liquidar, cada
tipo ha cargado su lectura y la escritura de su propio analista."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import Marcador, bloque, f5_presupuesto, huella, preparar  # noqa: E402

a, _, ej = preparar(__doc__)
from bloque_a.consumo import Presupuesto  # noqa: E402
from conftest import AS_OF, config_pruebas  # noqa: E402

TODOS = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]
m = Marcador()
hilos_lista = [1, 6, 12] if a.rapido else [1, 3, 6, 12]
reps = 2 if a.rapido else 3

orig_liq = Presupuesto.liquidar_primas
capturas: list = []


def liq(self):
    # solo la primera llamada explícita (tras la fase en paralelo); `resumen()` vuelve a llamar
    if not capturas or capturas[-1][2] is not self:
        antes = {k: round(v, 6) for k, v in sorted(self.consumido.items())}
        orig_liq(self)
        despues = {k: round(v, 6) for k, v in sorted(self.consumido.items())}
        capturas.append((antes, despues, self, len(BLOQUE[0].contabilidad.llamadas), sum(x["uc"] for x in BLOQUE[0].contabilidad.llamadas)))
    else:
        orig_liq(self)


Presupuesto.liquidar_primas = liq
BLOQUE: list = [None]
for diseno in ("v5", "v6"):
    vistos, vistos_fase, vistos_cierres = {}, {}, {}
    for h in hilos_lista:
        for k in range(reps if h > 1 else 1):
            capturas.clear()
            b = bloque(config_pruebas(diseno=diseno, perfiles={"activos": TODOS}, paralelismo={"hilos_analistas": h}))
            BLOQUE[0] = b
            b.ciclo(AS_OF)
            f5 = f5_presupuesto(b)
            antes, despues, _, n_llam, real_fase = capturas[0]
            etiqueta = f"h{h}#{k}"
            vistos.setdefault(huella(f5), []).append(etiqueta)
            vistos_fase.setdefault(huella([antes, despues]), []).append(etiqueta)
            cierres = [e for e in b.almacen.leer("F5") if "presupuesto" in e][-1].get("cierres_parciales")
            vistos_cierres.setdefault(huella(cierres), []).append(etiqueta)
            if h == hilos_lista[-1] and k == 0:
                real = sum(x["uc"] for x in b.contabilidad.llamadas)
                cargado = sum(x["consumido"] for x in f5.values())
                print(f"   {diseno}: final cargado {cargado:.4f} · real {real:.4f} · dif {real - cargado:.4f}")
                print(f"   {diseno}: en la fase ({n_llam} llamadas) antes de liquidar {sum(antes.values()):.4f} · después "
                      f"{sum(despues.values()):.4f} · real {real_fase:.4f}")
                print(f"   {diseno}: por tipo antes → después de liquidar: "
                      + ", ".join(f"{c} {antes.get(c, 0):.3f}→{despues.get(c, 0):.3f}" for c in TODOS + ["COMUN", "V6_GLOBAL"] if c in despues))
                m.check(f"{diseno}: tras liquidar la fase, lo cargado es el coste real de sus llamadas (±0,01)",
                        abs(sum(despues.values()) - real_fase) <= 0.01, f"{sum(despues.values()):.4f} vs {real_fase:.4f}")
                if diseno == "v6":
                    m.check("CA-2 v6: total cargado = coste real (±0,01)", abs(cargado - real) <= 0.01, f"{cargado:.4f} vs {real:.4f}")
    m.check(f"CA-1 {diseno}: el mismo presupuesto de F5 con hilos {hilos_lista} × {reps}", len(vistos) == 1,
            f"{len(vistos)} variantes: {list(vistos.values())}")
    m.check(f"CA-5 {diseno}: el mismo consumo por tipo antes y después de la liquidación de la fase", len(vistos_fase) == 1,
            f"{len(vistos_fase)} variantes: {list(vistos_fase.values())}")
    m.check(f"{diseno}: los mismos cierres parciales", len(vistos_cierres) == 1, f"{len(vistos_cierres)} variantes")
sys.exit(m.fin())
