"""QA r01 de T-178: ataques del revisor. Ejecutar desde bloque_a/11_Ejecutor con el venv:
    python ../../.docs/tickets/T-178/revisores/r01_ataques.py
Cada ataque imprime OK (se comporta como se espera) o FALLO (hallazgo)."""
import datetime as dt
import tempfile
import threading
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


# A1 · dos runs concurrentes (dos procesos = dos Almacen sobre la misma carpeta) tras una saturación previa
def a1():
    d = Path(tempfile.mkdtemp())
    saturar(Almacen(d), "RUN-0")
    a, b = Almacen(d), Almacen(d)
    barrera = threading.Barrier(2, timeout=10)
    for al in (a, b):
        orig = al.estado
        def estado(archivo, *args, _o=orig, **kw):
            r = _o(archivo, *args, **kw)
            if archivo == "HA":
                try:
                    barrera.wait()          # los dos leen HA antes de que ninguno escriba la P3-
                except threading.BrokenBarrierError:
                    pass
            return r
        al.estado = estado
    hs = [threading.Thread(target=saturar, args=(al, run)) for al, run in ((a, "RUN-1"), (b, "RUN-2"))]
    [h.start() for h in hs]
    [h.join() for h in hs]
    n = p3s(Almacen(d))
    informe("A1 dos runs concurrentes no duplican la P3-", len(n) == 1, f"P3- abiertas para AG-02: {n}")


# A2 · estado fuera del enum del esquema (manipulado o mal escrito) en la decisión
def a2():
    for estado in ("Rechazada", None, "EN_ESTUDIO"):
        d = Path(tempfile.mkdtemp())
        al = Almacen(d)
        saturar(al, "RUN-1")
        pid = saturar(al, "RUN-2")["p3_id"]
        al.escribir("HA", "AG-18", {"tipo_entrada": "P3", "id": pid, "estado": estado})
        saturar(al, "RUN-3")
        saturar(al, "RUN-4")
        n = p3s(al)
        informe(f"A2 estado {estado!r} fuera del enum no rearma la propuesta", len(n) == 1, f"P3-: {n}")


# A3 · fecha_objetivo sin validar: formatos o tipos distintos ordenan mal
def a3():
    m = Monitor(umbral_cola=0)
    m.encolar("AG-02", ordenes=[{"ref": "A", "fecha_objetivo": "2026-06-12"}, {"ref": "B", "fecha_objetivo": "2026-6-5"},
                                {"ref": "C", "fecha_objetivo": dt.date(2026, 6, 1)}, {"ref": "D", "fecha_objetivo": "05/06/2026"}])
    [car] = m.evaluar_instancias()
    orden = [c["ref"] for c in car["cola_reordenada"]]
    informe("A3 fecha_objetivo no ISO se rechaza o se ordena por fecha", orden == ["C", "B", "D", "A"], f"orden {orden}")
    try:
        m2 = Monitor(umbral_cola=0)
        m2.encolar("AG-02", ordenes=[{"ref": "A", "fecha_objetivo": float("nan")}, {"ref": "B", "fecha_objetivo": "2026-06-01"}])
        [car] = m2.evaluar_instancias()
        informe("A3b fecha NaN se rechaza al encolar", False, f"aceptada, orden {[c['ref'] for c in car['cola_reordenada']]}")
    except (ValueError, TypeError):
        informe("A3b fecha NaN se rechaza al encolar", True)


# A4 · tipo sin validar: «seguimiento» en minúsculas pasa por C1–C3
def a4():
    m = Monitor(umbral_cola=0)
    try:
        m.encolar("AG-02", ordenes=[{"ref": "S", "prioridad": "ALTA", "tipo": "seguimiento"}, {"ref": "N", "prioridad": "BAJA"}])
    except ValueError:
        informe("A4 tipo fuera de lista se rechaza", True)
        return
    [car] = m.evaluar_instancias()
    orden = [c["ref"] for c in car["cola_reordenada"]]
    informe("A4 tipo fuera de lista se rechaza (o C6 va detrás)", orden == ["N", "S"], f"orden {orden}")


# A5 · fallo a mitad: la P3- se escribe y el CAR- no
def a5():
    d = Path(tempfile.mkdtemp())
    al = Almacen(d)
    saturar(al, "RUN-1")
    orig = al.escribir
    def escribir(archivo, autor, e):
        if e.get("tipo_entrada") == "CAR":
            raise OSError("disco lleno (simulado)")
        return orig(archivo, autor, e)
    al.escribir = escribir
    try:
        saturar(al, "RUN-2")
    except OSError:
        pass
    al.escribir = orig
    ha = al.leer("HA")
    ids = {e["id"] for e in ha}
    [p3] = [e for e in ha if e["tipo_entrada"] == "P3"]
    colgantes = [c for c in p3["evidencia"]["car"] if c not in ids]
    informe("A5 tras un fallo del CAR-, la evidencia de la P3- no cita CAR- inexistentes", not colgantes, f"colgantes {colgantes}")
    car3 = saturar(al, "RUN-3")
    informe("A5b el run siguiente cita la P3- abierta y no duplica", car3.get("p3_id") == p3["id"] and len(p3s(al)) == 1)


# A6 · HA manipulado en disco (estado de la P3- cambiado a mano): lo detecta la integridad
def a6():
    d = Path(tempfile.mkdtemp())
    al = Almacen(d)
    saturar(al, "RUN-1")
    saturar(al, "RUN-2")
    ruta = d / "HA_historial_auditorias.jsonl"
    ruta.write_text(ruta.read_text().replace('"PENDING_OPERATOR"', '"RECHAZADA"'))
    try:
        al2 = Almacen(d)
        ok = al2.verificar_integridad("HA") == {"HA": False}
        if ok:
            try:
                saturar(al2, "RUN-3")
                ok = False
            except ValueError:
                ok = True
    except ValueError:
        ok = True
    informe("A6 HA manipulado falla cerrado", ok)


# A7 · R8: el aviso no lleva más campos que los de la orden (ni credenciales que vengan en ella)
def a7():
    m = Monitor(umbral_cola=0)
    m.encolar("AG-02", ordenes=[{"ref": "MSG-1", "prioridad": "ALTA", "api_key": "sk-ficticia", "texto": "cuerpo del mensaje"}])
    [car] = m.evaluar_instancias()
    s = str(car)
    informe("A7 el CAR- y el aviso no copian campos ajenos (R8)", "sk-ficticia" not in s and "cuerpo" not in s)


# A8 · idempotencia y orden: evaluar dos veces el mismo monitor en el mismo run; retirar y volver a encolar
def a8():
    d = Path(tempfile.mkdtemp())
    al = Almacen(d)
    m = Monitor(umbral_cola=3)
    m.encolar("AG-02", ordenes=seis())
    registrar_carga(al, m.evaluar_instancias(), "RUN-1")
    registrar_carga(al, m.evaluar_instancias(), "RUN-1")
    ok1 = p3s(al) == []
    m.retirar("AG-02", "MSG-0")
    m.encolar("AG-02", ordenes=[{"ref": "MSG-0", "prioridad": "BAJA"}])
    car = [e for e in m.evaluar_instancias() if e["tipo_entrada"] == "CAR"][0]
    ok2 = car["cola"] == 6 and len(car["cola_reordenada"]) == 6
    informe("A8 misma ejecución no propone; retirar y reencolar mantiene contador y detalle", ok1 and ok2)


# A9 · contador y detalle divergen: `fin` (la ruta de `agentes.llamar`) baja la cola pero no retira el detalle
def a9():
    m = Monitor(umbral_cola=0)
    m.encolar("AG-02", ordenes=seis())
    for _ in range(3):
        m.fin("AG-02", m.inicio("AG-02"))
    [car] = m.evaluar_instancias()
    informe("A9 cola y cola_reordenada coherentes tras `fin`", car["cola"] == len(car["cola_reordenada"]),
            f"cola {car['cola']} · detalle {len(car['cola_reordenada'])} · en_espera_sobre_umbral "
            f"{car.get('aviso_coordinador', {}).get('en_espera_sobre_umbral')}")


for f in (a1, a2, a3, a4, a5, a6, a7, a8, a9):
    try:
        f()
    except Exception as exc:   # noqa: BLE001
        informe(f.__name__ + " (excepción)", False, repr(exc))
print(f"\n{sum(ok for _, ok in RES)}/{len(RES)} OK")
