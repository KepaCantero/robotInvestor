"""QA r02 de T-196 (revisor): ataques a las correcciones de la r02 (huérfanas, reconciliación, reloj, servir).
Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-196/revisores/r02_ataques.py"""
import subprocess
import sys
import tempfile
import threading
import traceback
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "tests"))
import pandas as pd  # noqa: E402
from conftest import AS_OF, nuevo_bloque  # noqa: E402

from bloque_a import respuesta_final  # noqa: E402
from bloque_a.cola_peticiones import PeticionInvalida  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402

ZONA = "Europe/Madrid"
T0 = pd.Timestamp(f"{AS_OF}T09:00", tz=ZONA)
UNI = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
PREGUNTA_ANALITICA = "¿Qué opinas de las divisas frente a la renta fija?"
RES = {}


def ct01(prioridad="NORMAL", clases=("DIV",), **kw):
    return {"tipo": "AD_HOC", "alcance": {"clases": list(clases)}, "horizontes": ["H2"], "prioridad": prioridad, **kw}


def bloque(tmp=None):
    return nuevo_bloque(tmp or tempfile.mkdtemp(), UNI)


def pets(b):
    return {k: v for k, v in b.almacen.estado("F5").items() if v.get("tipo_entrada") == "PETICION"}


def huerf_inc(b, pid):
    return [e for e in b.almacen.leer("HA") if e.get("peticion_huerfana") == pid]


def caso(nombre):
    def deco(f):
        try:
            veredicto, detalle = f()
        except Exception:   # noqa: BLE001
            veredicto, detalle = "ERROR", traceback.format_exc(limit=4)
        RES[nombre] = veredicto
        print(f"[{veredicto}] {nombre}: {detalle}", flush=True)
        return f
    return deco


@caso("B1 hueco entre el fin del ciclo y la ATENDIDA: otro hilo mira las huérfanas y reconcilia")
def _b1():
    b = bloque()
    q = b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, encolar_escalado=True, instante=T0)
    pid = q["peticion_cola"]
    b.ciclo = lambda as_of, **kw: {"run_id": "RUN-FALSO-1", "estado": "COMPLETO"}
    vistas = {}
    original = b.cola._escalado

    def escalado_con_otro_hilo(*a, **k):   # justo después del ciclo y antes de ATENDIDA
        if threading.current_thread() is not threading.main_thread() or vistas:
            return original(*a, **k)   # la reconciliación del otro hilo también pasa por aquí: sin reentrar

        def otro():
            vistas["huerfanas"] = b.cola.huerfanas()
            try:
                vistas["reconciliar"] = b.cola.reconciliar(pid, "prueba del revisor", T0 + pd.Timedelta(minutes=2))["estado"]
            except PeticionInvalida as e:
                vistas["reconciliar"] = f"rechazada: {str(e)[:50]}"
        h = threading.Thread(target=otro)
        h.start()
        h.join()
        return original(*a, **k)
    b.cola._escalado = escalado_con_otro_hilo
    try:
        b.cola.atender(T0 + pd.Timedelta(minutes=1))
        fin = "atender termina"
    except Exception as e:   # noqa: BLE001
        fin = f"atender lanza {type(e).__name__}"
    estado = pets(b)[pid]["estado"]
    final = (b.almacen.estado("F5")[q["query_id"]].get("respuesta_final") or {})
    finales = [final.get("msg_id"), (b.almacen.estado("F5")[q["query_id"]].get("escalado") or {}).get("estado_run")]
    mala = pid in vistas.get("huerfanas", []) or vistas.get("reconciliar") == "FALLIDA"
    return ("HALLAZGO" if mala else "OK"), (f"huérfanas vistas por el otro hilo {vistas.get('huerfanas')}; reconciliar: "
                                            f"{vistas.get('reconciliar')}; {fin}; estado final {estado}; incidencias de "
                                            f"huérfana {len(huerf_inc(b, pid))}; final en F5 y estado_run del escalado {finales}")


@caso("B2 la PET- la toma otro proceso que muere (os._exit): detección, una sola incidencia y reconciliación con final FALLIDO")
def _b2():
    tmp = tempfile.mkdtemp()
    b = bloque(tmp)
    q = b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, encolar_escalado=True, instante=T0)
    pid = q["peticion_cola"]
    prog = (f"import sys, os; sys.path.insert(0, 'tests'); import pandas as pd; from conftest import nuevo_bloque; "
            f"from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO; from bloque_a.herramientas.ht01_datos import cargar_universo; "
            f"b = nuevo_bloque({tmp!r}, cargar_universo(RUTA_UNIVERSO_EJEMPLO)); "
            f"b.cola.tomar(pd.Timestamp('{AS_OF}T09:01', tz='{ZONA}')); os._exit(0)")
    r = subprocess.run([sys.executable, "-c", prog], capture_output=True, text=True, check=False)
    if r.returncode != 0:
        return "ERROR", r.stderr[-300:]
    pend1 = respuesta_final.enviar_pendientes(b, AS_OF)
    h1 = b.cola.huerfanas()
    s = b.cola.atender(T0 + pd.Timedelta(days=1))
    n_inc = len(huerf_inc(b, pid))
    try:
        b.cola.reconciliar(pid, "  ", T0 + pd.Timedelta(days=1))
        vacio = "admite un motivo vacío"
    except PeticionInvalida:
        vacio = "motivo vacío rechazado"
    rec = b.cola.reconciliar(pid, "proceso caído, revisado F5", T0 + pd.Timedelta(days=1, hours=1))
    fin = rec["respuesta_final"]["respuesta_final"]["resultado_analisis"] if rec["respuesta_final"] else None
    try:
        b.cola.reconciliar(pid, "otra vez", T0 + pd.Timedelta(days=1, hours=2))
        dos = "se reconcilia dos veces"
    except PeticionInvalida:
        dos = "la segunda se rechaza"
    pend2 = respuesta_final.enviar_pendientes(b, AS_OF)
    ok = (h1 == [pid] and not pend1 and not s and n_inc == 1 and vacio.endswith("rechazado") and fin == "FALLIDO"
          and dos.endswith("rechaza") and pets(b)[pid]["estado"] == "FALLIDA"
          and all(f.get("repetido") for f in pend2))   # con un as_of anterior, la misma final idempotente (T-169), no otra
    return ("OK" if ok else "HALLAZGO"), (f"huérfanas {h1}; incidencias {n_inc}; {vacio}; final {fin}; {dos}; "
                                          f"estado {pets(b)[pid]['estado']}; pendientes después {len(pend2)}")


@caso("B3 reconciliar una PET- que otro proceso vivo está sirviendo")
def _b3():
    tmp = tempfile.mkdtemp()
    b = bloque(tmp)
    pid = b.cola.recibir(ct01(), T0)["pet_id"]
    prog = (f"import sys, time; sys.path.insert(0, 'tests'); import pandas as pd; from conftest import nuevo_bloque; "
            f"from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO; from bloque_a.herramientas.ht01_datos import cargar_universo; "
            f"b = nuevo_bloque({tmp!r}, cargar_universo(RUTA_UNIVERSO_EJEMPLO)); "
            f"b.cola.tomar(pd.Timestamp('{AS_OF}T09:01', tz='{ZONA}')); print('tomada', flush=True); time.sleep(20)")
    p = subprocess.Popen([sys.executable, "-c", prog], stdout=subprocess.PIPE, text=True)
    try:
        assert p.stdout.readline().strip() == "tomada"
        h = b.cola.huerfanas()
        try:
            b.cola.reconciliar(pid, "intento indebido", T0 + pd.Timedelta(minutes=5))
            r = "RECONCILIADA"
        except PeticionInvalida:
            r = "rechazada"
    finally:
        p.kill()
        p.wait()
    return ("OK" if not h and r == "rechazada" else "HALLAZGO"), f"huérfanas {h}; reconciliar: {r}"


@caso("B4 servir() con una PET- ENCOLADA (no tomada) o un dict falsificado")
def _b4():
    b = bloque()
    pid = b.cola.recibir(ct01(), T0)["pet_id"]
    salida = []
    for pet in ({"id": pid}, {"id": "PET-2026-9999"}, {}):
        try:
            b.cola.servir(pet, T0 + pd.Timedelta(minutes=1))
            salida.append("servida")
        except PeticionInvalida:
            salida.append("rechazada")
    return ("OK" if salida == ["rechazada"] * 3 else "HALLAZGO"), str(salida)


@caso("B5 atender con un reloj que retrocede y otro que devuelve basura a mitad")
def _b5():
    b = bloque()
    for i in range(3):
        b.cola.recibir(ct01(), T0 + pd.Timedelta(minutes=i))
    b.ciclo = lambda as_of, **kw: {"run_id": "RUN-X", "estado": "COMPLETO"}
    tiempos = iter([T0 + pd.Timedelta(minutes=10), T0 + pd.Timedelta(minutes=10), T0 + pd.Timedelta(seconds=30),
                    T0 + pd.Timedelta(minutes=11), T0 + pd.Timedelta(minutes=12)])
    s = b.cola.atender(lambda: next(tiempos))
    est = sorted(p["estado"] for p in pets(b).values())
    b2 = bloque()
    for i in range(2):
        b2.cola.recibir(ct01(), T0 + pd.Timedelta(minutes=i))
    b2.ciclo = b.ciclo
    malos = iter([T0 + pd.Timedelta(minutes=5), T0 + pd.Timedelta(minutes=5), "basura"])
    try:
        b2.cola.atender(lambda: next(malos))
        r = "no falla"
    except PeticionInvalida:
        r = "PeticionInvalida"
    est2 = sorted(p["estado"] for p in pets(b2).values())
    ok = len(s) == 3 and r == "PeticionInvalida" and est2 == ["ATENDIDA", "ENCOLADA"]
    return ("OK" if ok else "HALLAZGO"), f"reloj que retrocede: {len(s)} servidas, {est}; reloj con basura: {r}, {est2}"


@caso("B6 carrera de Mensajeria._acuses: varias instancias abren por primera vez el mismo almacén a la vez")
def _b6():
    fallos, total = 0, 0
    for _ in range(15):
        tmp = tempfile.mkdtemp()
        bs = [bloque(tmp) for _ in range(6)]
        errores = []
        barrera = threading.Barrier(len(bs))

        def abrir(bb):
            barrera.wait()
            try:
                bb.mensajeria._acuses().close()
            except Exception as e:   # noqa: BLE001
                errores.append(type(e).__name__ + ": " + str(e)[:40])
        hs = [threading.Thread(target=abrir, args=(bb,)) for bb in bs]
        for h in hs:
            h.start()
        for h in hs:
            h.join()
        total += 1
        fallos += bool(errores)
        if errores:
            ejemplo = errores[0]
    det = f"{fallos} de {total} intentos con error" + (f" (p. ej. {ejemplo})" if fallos else "")
    return ("CONFIRMADA" if fallos else "NO REPRODUCIDA"), det


print(RES)
