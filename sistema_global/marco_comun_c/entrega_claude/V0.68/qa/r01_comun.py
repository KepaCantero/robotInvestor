"""QA r01 de T-80: utilidades comunes de las sondas (datos SIMULADOS; reutiliza los arneses de pruebas/)."""
import copy
import sys
from pathlib import Path

MARCO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))

from pruebas_orquestador import (AHORA, ENTRADA, SALIDA, anotar_entrada, autorizar_op, dim, encargo,  # noqa: E402,F401
                                 hasta, nuevo, sobre_para)
from pruebas_control_f import informe_f  # noqa: E402,F401

RES = {"ok": True}


def chk(nombre, cond, detalle=""):
    print(("OK   " if cond else "FALLA"), nombre, "" if cond else detalle)
    RES["ok"] &= bool(cond)


def foto(o):
    return copy.deepcopy({k: v for k, v in o.__dict__.items() if k not in ("avisos", "ultimo_ahora")})


def enc_directa(eid, n, nivel=None, decision=None):
    e = encargo(n, producer="BROKER")
    e["expediente_id"], e["correlation_id"], e["event_id"] = eid, f"COR-{eid}", f"EV-ENC-{eid}"
    if nivel:
        e["payload"]["nivel_analisis"] = nivel
    if decision:
        e["payload"]["decision_informada"] = decision
    return e


def sobre_directa(eid, n):
    s = sobre_para(n, None)
    s["expediente_id"], s["correlation_id"], s["event_id"] = eid, f"COR-{eid}", f"EV-SOB-{eid}"
    return s


def descartado_por_operador(o, n=1):
    hasta(o, "VALIDADA", n)
    r = o.descartar(f"EXP-{n:04d}", "el operador lo aparta por ahora", "OPERADOR", AHORA)
    assert r["ok"], r


def fin():
    print("RESULTADO:", "SIN FALLOS" if RES["ok"] else "HAY FALLOS")
    return 0 if RES["ok"] else 1
