"""QA r01 de T-196 (revisor independiente): ataques a la cola de peticiones. Cada caso imprime OK (el comportamiento es el
esperado) o HALLAZGO. Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-196/revisores/r01_ataques.py
"""
import sys
import tempfile
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


def caso(nombre):
    def deco(f):
        try:
            veredicto, detalle = f()
        except Exception:   # noqa: BLE001
            veredicto, detalle = "ERROR", traceback.format_exc(limit=3)
        RES[nombre] = veredicto
        print(f"[{veredicto}] {nombre}: {detalle}", flush=True)
        return f
    return deco


@caso("A1 CT-01 recibido con un instante anterior a otra PET- en cola (entrega fuera de orden)")
def _a1():
    b = bloque()
    b.cola.recibir(ct01(), T0 + pd.Timedelta(seconds=2))
    try:
        b.cola.recibir({**ct01("ALTA"), "msg_id": "MSG-BRK-2026-000777"}, T0 + pd.Timedelta(seconds=1))
    except PeticionInvalida as e:
        # ¿y el reintento del Broker con el mismo msg_id y un instante válido?
        try:
            b.cola.recibir({**ct01("ALTA"), "msg_id": "MSG-BRK-2026-000777"}, T0 + pd.Timedelta(seconds=3))
            reintento = "el reintento entra"
        except Exception as e2:   # noqa: BLE001
            reintento = f"el reintento tampoco entra ({type(e2).__name__}: {str(e2)[:90]})"
        return "HALLAZGO", f"rechazada ({str(e)[:80]}…); {reintento}; PET- en F5: {len(pets(b))}"
    return "OK", f"admitida; PET- {len(pets(b))}"


@caso("A2 atender mientras otro proceso recibe un CT-01 (recibida posterior al instante del servicio)")
def _a2():
    b = bloque()
    for i in range(3):
        b.cola.recibir(ct01(), T0 + pd.Timedelta(seconds=i))
    t_serv = T0 + pd.Timedelta(minutes=1)
    n = {"k": 0}

    def ciclo_lento(as_of, **kw):   # durante el análisis llega otra petición (reloj real: después de t_serv)
        n["k"] += 1
        if n["k"] == 1:
            b.cola.recibir(ct01("BAJA"), t_serv + pd.Timedelta(minutes=5))
        return {"run_id": f"RUN-FALSO-{n['k']}", "estado": "COMPLETO"}
    b.ciclo = ciclo_lento
    try:
        s = b.cola.atender(t_serv)
    except PeticionInvalida as e:
        estados = sorted(p["estado"] for p in pets(b).values())
        return "HALLAZGO", f"atender se corta tras {n['k']} servida(s): {str(e)[:70]}…; estados {estados}"
    return "OK", f"servidas {len(s)}"


@caso("A3 consulta encolada y otro CT-01 registrado durante la llamada al modelo (instante posterior)")
def _a3():
    b = bloque()
    original = respuesta_final.registrar_provisional

    def con_carrera(*a, **k):
        r = original(*a, **k)
        b.cola.recibir(ct01("BAJA"), T0 + pd.Timedelta(seconds=30))   # otro proceso, reloj más adelante
        return r
    respuesta_final.registrar_provisional = con_carrera
    try:
        q = b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, encolar_escalado=True, instante=T0)
        return "OK", f"encolada {q.get('peticion_cola')}"
    except Exception as e:   # noqa: BLE001
        respuesta_final.registrar_provisional = original
        f5 = b.almacen.estado("F5")
        qry = next(v for v in f5.values() if v.get("tipo_entrada") == "QRY")
        en_f5 = qry.get("peticion_cola") in f5
        finales = respuesta_final.enviar_pendientes(b, AS_OF)
        res = finales[0]["respuesta_final"]["resultado_analisis"] if finales else None
        return "HALLAZGO", (f"{type(e).__name__} después de escribir la QRY- y la provisional; PET- {qry.get('peticion_cola')} "
                            f"en F5: {en_f5}; la final que sale luego: {res}")
    finally:
        respuesta_final.registrar_provisional = original


@caso("A4 instante sin zona en el hueco del cambio de hora (2026-03-29T02:30) y en la hora repetida (2026-10-25T02:30)")
def _a4():
    salida = []
    for valor in ("2026-03-29T02:30", "2026-10-25T02:30"):
        b = bloque()
        try:
            b.cola.recibir(ct01(), valor)
            salida.append(f"{valor}: admitido")
        except PeticionInvalida:
            salida.append(f"{valor}: PeticionInvalida")
        except Exception as e:   # noqa: BLE001
            salida.append(f"{valor}: {type(e).__name__} (no PeticionInvalida); F5 PET- {len(pets(b))}")
    hallazgo = any("no PeticionInvalida" in s for s in salida)
    return ("HALLAZGO" if hallazgo else "OK"), "; ".join(salida)


@caso("A5 instante con nanosegundos (pd.Timestamp) y msg_id del Broker")
def _a5():
    b = bloque()
    t = pd.Timestamp("2026-06-05T09:00:00.123456789", tz=ZONA)
    try:
        r = b.cola.recibir({**ct01(), "msg_id": "MSG-BRK-2026-000888"}, t)
        return "OK", f"admitido {r['pet_id']} con recibida {pets(b)[r['pet_id']]['recibida']}"
    except Exception as e:   # noqa: BLE001
        try:
            b.cola.recibir({**ct01(), "msg_id": "MSG-BRK-2026-000888"}, T0)
            reint = "el reintento entra"
        except Exception as e2:   # noqa: BLE001
            reint = f"el reintento no entra: {type(e2).__name__}"
        return "HALLAZGO", f"{type(e).__name__} tras validar: {str(e)[:70]}; {reint}"


@caso("A6 tomar() deja una PET- EN_CURSO que nada puede servir después")
def _a6():
    b = bloque()
    pid = b.cola.recibir(ct01(), T0)["pet_id"]
    b.cola.tomar(T0 + pd.Timedelta(minutes=1))
    b.ciclo = lambda as_of, **kw: {"run_id": "RUN-X", "estado": "COMPLETO"}
    s = b.cola.atender(T0 + pd.Timedelta(minutes=2))
    est = pets(b)[pid]["estado"]
    inc = [e for e in b.almacen.leer("HA") if pid in str(e.get("detalle", ""))]
    return ("HALLAZGO" if est == "EN_CURSO" and not s and not inc else "OK"), \
        f"tras atender: {est}; servidas {len(s)}; incidencias {len(inc)}"


@caso("A7 proceso muerto con la PET- de una consulta EN_CURSO: ¿alguien lo detecta? ¿sale la final?")
def _a7():
    tmp = tempfile.mkdtemp()
    b = bloque(tmp)
    q = b.consulta(PREGUNTA_ANALITICA, as_of=AS_OF, encolar_escalado=True, instante=T0)
    b.cola.tomar(T0 + pd.Timedelta(minutes=1))        # el proceso muere aquí, en pleno ciclo
    b2 = bloque(tmp)                                  # otro proceso, más tarde
    finales = respuesta_final.enviar_pendientes(b2, AS_OF)
    servidas = b2.cola.atender(T0 + pd.Timedelta(days=3))
    inc = [e for e in b2.almacen.leer("HA") if q["peticion_cola"] in str(e.get("detalle", ""))]
    pet = b2.almacen.estado("F5")[q["peticion_cola"]]
    return ("HALLAZGO" if not inc and not finales and pet["estado"] == "EN_CURSO" else "OK"), \
        f"tres días después: PET- {pet['estado']}, finales {len(finales)}, servidas {len(servidas)}, incidencias {len(inc)}"


@caso("A8 CT-01 con clases ajenas o inactivas: ¿se encola con 0 UC?")
def _a8():
    b = bloque()
    try:
        r = b.cola.recibir(ct01(clases=("XXX",)), T0)
    except Exception as e:   # noqa: BLE001
        return "OK", f"rechazado: {type(e).__name__}"
    try:
        s = b.cola.atender(T0 + pd.Timedelta(minutes=1))
        fin = f"servida: {s[0]['estado_run']}"
    except Exception as e:   # noqa: BLE001
        fin = f"el ciclo falla: {type(e).__name__}"
    return "HALLAZGO" if r["presupuesto_uc"] == 0 else "OK", f"encolada con clases {r['clases']} y {r['presupuesto_uc']} UC; {fin}"


@caso("A9 PET- con recibida manipulada en F5 (texto no fecha): ¿integridad o bloqueo de la cola?")
def _a9():
    b = bloque()
    b.cola.recibir(ct01(), T0)
    pid = b.cola.recibir(ct01(), T0 + pd.Timedelta(seconds=1))["pet_id"]
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "PETICION", "id": pid, "recibida": "ayer"})
    try:
        b.cola.orden(T0 + pd.Timedelta(minutes=1))
        return "OK", "ordena"
    except PeticionInvalida as e:
        return "OK", f"falla cerrado: {str(e)[:60]} (una entrada mala detiene toda la cola: fallo cerrado, aceptable)"


@caso("A10 envejecimiento: 9 h 59 min, 10 h y 1000 h de espera; instante en otra zona horaria")
def _a10():
    b = bloque()
    pid = b.cola.recibir(ct01("BAJA"), T0)["pet_id"]
    p = pets(b)[pid]
    v = [b.cola.prioridad({**p, "id": pid}, T0 + pd.Timedelta(hours=h))["efectiva"] for h in (9 + 59 / 60, 10, 1000)]
    utc = b.cola.prioridad({**p, "id": pid}, (T0 + pd.Timedelta(hours=10)).tz_convert("UTC"))["efectiva"]
    ok = v == [19.0, 20.0, 25.0] and utc == 20.0
    return ("OK" if ok else "HALLAZGO"), f"{v}, en UTC {utc}"


print({k: v for k, v in RES.items()})
