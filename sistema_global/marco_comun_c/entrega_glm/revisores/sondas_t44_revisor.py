"""Sondas del revisor T-44 (no son entregables; exploran comportamiento)."""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/
sys.path.insert(0, str(AQUI / "validador"))
sys.path.insert(0, str(AQUI / "pruebas"))

from control_f import POLITICA_DEFECTO
from ejecucion_g import BrokerSimulado, declarar_manual, conciliar, ejecutar
from manual_g import validar_manual
from pruebas_ejecucion_g import autorizado, HORA_DATOS
from pruebas_manual import PID, T1, T2, VIA, a_mano, reg, cambia, estado, abierta_l1
from pruebas_orquestador import AHORA, nuevo

VMIN = 20.0
L1_MIN = {"nivel_autonomia": {"TACTICA": "L1"}, "politica_f": {**POLITICA_DEFECTO, "valor_min_eur": VMIN}}


def abierta_min():
    o, b = autorizado(o=nuevo(dict(L1_MIN)))
    assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]
    return o, b


def sonda1():
    """Hueco de tolerancia relativa: declara 40.00003 con relleno real de 40.0."""
    o, b = abierta_min()
    a_mano(b, "EURUSD", "VENTA", 40.0, "MAN-RED-1")
    b.enviar({"orden_id": "MAN-STOP-2", "tipo": "STOP", "lado": "VENTA", "instrumento": "EURUSD",
              "activo_base": "EUR", "cantidad": 100.0 - 40.00003, "precio": 1.05, "via_acceso": VIA})
    r = reg(event_id="EV-S1", vinculo={"tipo": "POSICION", "id": PID}, lado="VENTA", cantidad=40.00003,
            precio=1.10, ref_intermediario="MAN-RED-1", proteccion_ref="MAN-STOP-2", motivo="parcial sondada")
    res = declarar_manual(o, r, b, T1)
    c = conciliar(o, b, T1)
    print("SONDA1 G:", res["codigo"], "| libros:", o.posiciones[PID]["cantidad"], "| conciliar:", c["diferencias"])


def sonda2():
    """Variante PROTECCION: el stop está por lo que queda REAL (60.0), no por lo declarado (59.99997)."""
    o, b = abierta_min()
    a_mano(b, "EURUSD", "VENTA", 40.0, "MAN-RED-1")
    b.enviar({"orden_id": "MAN-STOP-2", "tipo": "STOP", "lado": "VENTA", "instrumento": "EURUSD",
              "activo_base": "EUR", "cantidad": 60.0, "precio": 1.05, "via_acceso": VIA})
    r = reg(event_id="EV-S2", vinculo={"tipo": "POSICION", "id": PID}, lado="VENTA", cantidad=40.00003,
            precio=1.10, ref_intermediario="MAN-RED-1", proteccion_ref="MAN-STOP-2", motivo="parcial sondada 2")
    res = declarar_manual(o, r, b, T1)
    c = conciliar(o, b, T1)
    print("SONDA2 G:", res["codigo"], "| libros:", o.posiciones[PID]["cantidad"], "| conciliar:", c["diferencias"])


def sonda3():
    """Borde: cantidad = 99.999999 sobre una posición de 100 (ABIERTA)."""
    o, b = abierta_min()
    a_mano(b, "EURUSD", "VENTA", 99.999999, "MAN-RED-1")
    b.enviar({"orden_id": "MAN-STOP-2", "tipo": "STOP", "lado": "VENTA", "instrumento": "EURUSD",
              "activo_base": "EUR", "cantidad": 100.0 - 99.999999, "precio": 1.05, "via_acceso": VIA})
    r = reg(event_id="EV-S3", vinculo={"tipo": "POSICION", "id": PID}, lado="VENTA", cantidad=99.999999,
            precio=1.10, ref_intermediario="MAN-RED-1", proteccion_ref="MAN-STOP-2", motivo="borde sondado")
    out = o.registrar_manual(r, T1)
    print("SONDA3 directo:", out["codigo"], out.get("reglas"), out.get("motivo", "")[:110])
    o2, b2 = abierta_min()
    a_mano(b2, "EURUSD", "VENTA", 99.999999, "MAN-RED-1")
    b2.enviar({"orden_id": "MAN-STOP-2", "tipo": "STOP", "lado": "VENTA", "instrumento": "EURUSD",
               "activo_base": "EUR", "cantidad": 100.0 - 99.999999, "precio": 1.05, "via_acceso": VIA})
    res = declarar_manual(o2, r, b2, T1)
    print("SONDA3 por G:", res["codigo"], res.get("motivo", "")[:110], "| estado:", o2.posiciones[PID]["estado"],
          "| stop viejo:", b2.consultar("ORD-EXP-0001-S-1")["estado"])


def sonda4():
    """El resto cae justo en el mínimo (>= pasa) y justo por debajo (RM-12)."""
    # resto = (100 - q) * 1.10; con VMIN=20: q = 100 - 20/1.1 = 81.81818181818181 -> resto == 19.999999999999996?
    import math
    q = 100.0 - 20.0 / 1.10
    print("SONDA4 q:", q, "resto:", (100.0 - q) * 1.10, "== 20:", (100.0 - q) * 1.10 == 20.0)
    o, b = abierta_min()
    p = o.posiciones[PID]
    ctx = {"ahora": T1, "expediente": None, "posicion": p, "tolerancia_precio": 0.05,
           "valor_min_restante_eur": VMIN, "identidad": ("EXP-0001", "COR-0001")}
    r = reg(event_id="EV-S4", vinculo={"tipo": "POSICION", "id": PID}, lado="VENTA", cantidad=q,
            precio=1.10, ref_intermediario="MAN-RED-1", proteccion_ref="MAN-STOP-2", motivo="borde minimo")
    # ojo: reg() envuelve como EXPEDIENTE por defecto -> usar cambia para forzar el vínculo
    r = cambia(r, vinculo={"tipo": "POSICION", "id": PID})
    f = validar_manual(r, ctx)
    print("SONDA4 validar:", [x["regla"] for x in f])


sonda1()
sonda2()
sonda3()
sonda4()
