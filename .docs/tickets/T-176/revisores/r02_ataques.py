"""QA r02 de T-176 (revisor independiente): ataques nuevos sobre las correcciones H-01 a H-06.

Uso (desde la raíz del repo, con el venv):  python .docs/tickets/T-176/revisores/r02_ataques.py"""
import sys
import tempfile
import threading
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(RAIZ / "bloque_a/11_Ejecutor"), str(RAIZ / "bloque_a/11_Ejecutor/tests")]

from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.evaluador import Evaluador, pruebas_regresion_p3  # noqa: E402
from conftest import RUTA_UNIVERSO_EJEMPLO, cargar_universo, config_pruebas, nuevo_bloque  # noqa: E402
from test_t66_evaluacion import _celda_recalibrable  # noqa: E402

RES = []


def informe(nombre, ok, detalle=""):
    RES.append((nombre, ok))
    print(f"{'OK      ' if ok else 'HALLAZGO'} · {nombre}{' · ' + detalle if detalle else ''}")


def evaluador(tmp, fecha="2026-04-06", **extra):
    a = Almacen(Path(tmp))
    a.reloj.fijar(fecha)
    return Evaluador(a, None, None, config_pruebas(**extra), None)


UNIV = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
RR = {"paso": 0.05, "banda_trimestral": 0.05, "banda_total": 0.02, "dif_ic_min": 0.10, "meses_sombra": 3}

# 1. recalibrar (H-01) concurrente: su deduplicación no va en transacción
with tempfile.TemporaryDirectory() as d:
    b = nuevo_bloque(d, UNIV, cfg=config_pruebas(evaluacion={"recalibracion_rk": RR}))
    b.reloj.fijar("2026-01-02")
    _celda_recalibrable(b.almacen, contaminados=0)
    evs = []
    for _ in range(6):
        a = Almacen(Path(d) / "estado")
        a.reloj.fijar("2026-01-02")
        evs.append(Evaluador(a, None, None, config_pruebas(evaluacion={"recalibracion_rk": RR}), None))
    barrera = threading.Barrier(len(evs))

    def correr(ev):
        barrera.wait()
        ev.recalibrar("2026-01-02")

    hs = [threading.Thread(target=correr, args=(ev,)) for ev in evs]
    [h.start() for h in hs]
    [h.join() for h in hs]
    p3 = {x["id"] for x in Almacen(Path(d) / "estado").leer("F6") if x.get("tipo_entrada") == "P3"}
    informe("recalibrar concurrente deja una sola P3- de P-11", len(p3) == 1, f"{len(p3)} P3-")

# 2. H-03: con la P3- de P-09·E abierta, el componente A sí puede proponer; tras RECHAZADA, E vuelve a proponer dentro de banda
with tempfile.TemporaryDirectory() as d:
    e = evaluador(d)
    p = e.proponer_ajuste("P-09", "E", 48, {}, "2026-04-06")
    a = e.proponer_ajuste("P-09", "A", 52, {}, "2026-04-06")
    informe("P3- de P-09·E no bloquea P-09·A", a["tipo_entrada"] == "AJU" and a["id"] != p["id"])
    e.almacen.escribir("F6", "AG-20", {"tipo_entrada": "P3", "id": p["id"], "estado": "RECHAZADA"})
    nuevo = e.proponer_ajuste("P-09", "E", 57, {}, "2026-04-06")
    informe("tras la decisión del operador, E vuelve a proponer dentro de banda", nuevo["tipo_entrada"] == "AJU")
    informe("sigue sin escribir en F10", not e.almacen.leer("F10"))

# 3. H-05: la batería sale de la configuración, sin repetir y en orden; sin la clave, falla cerrado
cfg = config_pruebas()
lst = pruebas_regresion_p3(cfg)
informe("pruebas_regresion = batería §6 + R18, sin repetir", lst[:16][0] == "PB-01" and lst.count("PB-36") == 1 and lst[-1] == "PB-50"
        and len(lst) == 20, str(len(lst)))
try:
    cfg2 = config_pruebas()
    cfg2["evaluacion"]["bateria_regresion"] = None     # ausente cae a por_defecto.yaml (convención de `parametro`); nula, falla
    pruebas_regresion_p3(cfg2)
    informe("bateria_regresion nula falla cerrado", False)
except (KeyError, ValueError, TypeError):
    informe("bateria_regresion nula falla cerrado", True)

# 4. H-06: P3- con elevada_via y en HA no se reenvía (no hay CT-19 de más)
with tempfile.TemporaryDirectory() as d:
    b = nuevo_bloque(d, UNIV)
    b.fijar_fecha("2026-06-05")
    b.evaluador.proponer_ajuste("P-09", "E", 48, {}, "2026-06-05")
    b.elevar_propuestas_tipo3("2026-06-05", "RUN-2026-0001")
    n = len([m for m in b.mensajeria.registro if m["contrato"] == "CT-19"])
    b.elevar_propuestas_tipo3("2026-06-05", "RUN-2026-0002")
    informe("una P3- ya elevada y en HA no genera otro CT-19",
            len([m for m in b.mensajeria.registro if m["contrato"] == "CT-19"]) == n)

print(f"\n{sum(ok for _, ok in RES)}/{len(RES)} sin hallazgo")
