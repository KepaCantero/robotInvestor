"""QA r02 de T-178: ataques nuevos del revisor (r01_ataques.py se mantiene sin tocar; su A3 no captura el rechazo, que es
el comportamiento correcto tras H-03, y aquí se rehace). Desde bloque_a/11_Ejecutor:
    PYTHONPATH=. python ../../.docs/tickets/T-178/revisores/r02_ataques.py"""
import datetime as dt
import multiprocessing as mp
import tempfile
from pathlib import Path

from bloque_a.almacen import Almacen
from bloque_a.carga import CLAVE_P3, registrar_carga
from bloque_a.herramientas.ht08_monitor import Monitor

RES = []


def informe(nombre, ok, detalle=""):
    RES.append((nombre, ok))
    print(("OK    " if ok else "FALLO ") + nombre + (f" · {detalle}" if detalle else ""))


def seis():
    return [{"ref": f"MSG-{i}", "prioridad": p, "fecha_objetivo": "2026-06-1%d" % i}
            for i, p in enumerate(["ALTA", "NORMAL", "BAJA", "ALTA", "NORMAL", "BAJA"])]


def saturar(al, run, ag="AG-02"):
    m = Monitor(umbral_cola=3)
    m.encolar(ag, ordenes=seis())
    return [e for e in registrar_carga(al, m.evaluar_instancias(), run) if e["tipo_entrada"] == "CAR"][0]


def p3s(al):
    return sorted({e["id"] for e in al.leer("HA") if e["tipo_entrada"] == "P3" and e.get("clave") == CLAVE_P3})


# B1 · A3 rehecho: cada formato malo se rechaza sin tocar la cola; date y datetime se guardan en ISO y ordenan por fecha
def b1():
    for f in ("2026-6-5", "05/06/2026", "2026-02-30", float("nan"), 20260605, "2026-06-05T10:00", ""):
        m = Monitor(umbral_cola=0)
        try:
            m.encolar("AG-02", ordenes=[{"ref": "A", "fecha_objetivo": "2026-06-01"}, {"ref": "B", "fecha_objetivo": f}])
            informe(f"B1 fecha {f!r} se rechaza", False, "aceptada")
        except ValueError:
            informe(f"B1 fecha {f!r} se rechaza sin tocar la cola", m.cola["AG-02"] == 0 and m.pendientes["AG-02"] == [])
    m = Monitor(umbral_cola=0)
    m.encolar("AG-02", ordenes=[{"ref": "A", "fecha_objetivo": "2026-06-12"}, {"ref": "C", "fecha_objetivo": dt.date(2026, 6, 1)},
                                {"ref": "D", "fecha_objetivo": dt.datetime(2026, 6, 5, 23, 0)}])
    [car] = m.evaluar_instancias()
    informe("B1 date/datetime en ISO y orden por fecha", [c["ref"] for c in car["cola_reordenada"]] == ["C", "D", "A"]
            and car["cola_reordenada"][1]["fecha_objetivo"] == "2026-06-05")


# B2 · H-01 entre procesos reales: dos procesos, barrera tras leer HA, cada uno con su Almacen
def _hijo(d, run, barrera):
    al = Almacen(d)
    orig = al.estado
    def estado(archivo, *a, **kw):
        r = orig(archivo, *a, **kw)
        if archivo == "HA":
            try:
                barrera.wait(3)
            except Exception:   # noqa: BLE001 · el otro proceso está bloqueado en el cerrojo: la barrera se rompe
                pass
        return r
    al.estado = estado
    saturar(al, run)


def b2():
    ctx = mp.get_context("fork")
    for intento in range(3):
        d = str(Path(tempfile.mkdtemp()))
        saturar(Almacen(d), "RUN-0")
        barrera = ctx.Barrier(2)
        ps = [ctx.Process(target=_hijo, args=(d, f"RUN-{k}", barrera)) for k in (1, 2)]
        [p.start() for p in ps]
        [p.join(60) for p in ps]
        al = Almacen(d)
        n = p3s(al)
        cars = [e for e in al.leer("HA") if e["tipo_entrada"] == "CAR"]
        informe(f"B2.{intento} dos procesos: una P3- y los dos CAR- la citan", len(n) == 1 and all(p.exitcode == 0 for p in ps)
                and [c.get("p3_id") for c in cars[1:]] == n * 2 and al.verificar_integridad("HA") == {"HA": True},
                f"P3- {n}; exit {[p.exitcode for p in ps]}")


# B3 · H-05: evidencia útil para el operador, con y sin fallo del CAR-
def b3():
    al = Almacen(Path(tempfile.mkdtemp()))
    c1 = saturar(al, "RUN-1")
    c2 = saturar(al, "RUN-2")
    [p3] = [e for e in al.leer("HA") if e["tipo_entrada"] == "P3"]
    ev = p3["evidencia"]
    ids = {e["id"] for e in al.leer("HA")}
    citan = [e["id"] for e in al.leer("HA") if e.get("p3_id") == p3["id"]]
    informe("B3 la evidencia nombra los dos runs y todo lo citado existe; el CAR- actual la cita",
            ev["car"] == [c1["id"]] and ev["runs"] == ["RUN-1"] and ev["run_actual"] == "RUN-2" and ev["cola"] == 6
            and all(c in ids for c in ev["car"]) and citan == [c2["id"]], str(ev))


# B4 · APLICADA cierra, y una APROBADA posterior a una RECHAZADA (transición fuera del esquema) deja abierta sin duplicar
def b4():
    al = Almacen(Path(tempfile.mkdtemp()))
    saturar(al, "RUN-1")
    pid = saturar(al, "RUN-2")["p3_id"]
    al.escribir("HA", "AG-18", {"tipo_entrada": "P3", "id": pid, "estado": "APROBADA"})
    al.escribir("HA", "AG-18", {"tipo_entrada": "P3", "id": pid, "estado": "APLICADA"})
    a = "p3_id" not in saturar(al, "RUN-3")
    b = saturar(al, "RUN-4").get("p3_id") not in (None, pid)
    informe("B4 tras APLICADA hace falta repetir y luego hay P3- nueva", a and b and len(p3s(al)) == 2)


# B5 · fallo cerrado del tipo: None admitido (sin tipo), mayúsculas exactas, no-str rechazado
def b5():
    ok = True
    for t in ("seguimiento", "C6", 3, ""):
        try:
            Monitor(0).encolar("AG-02", ordenes=[{"ref": "X", "tipo": t}])
            ok = False
        except ValueError:
            pass
    m = Monitor(0)
    m.encolar("AG-02", ordenes=[{"ref": "X"}, {"ref": "Y", "tipo": "SEGUIMIENTO"}])
    informe("B5 tipo en lista cerrada; sin tipo vale", ok and m.cola["AG-02"] == 2)


if __name__ == "__main__":
    for f in (b1, b2, b3, b4, b5):
        try:
            f()
        except Exception as exc:   # noqa: BLE001
            informe(f.__name__ + " (excepción)", False, repr(exc))
    print(f"\n{sum(ok for _, ok in RES)}/{len(RES)} OK")
