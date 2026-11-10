"""Pasada de coherencia contra la Constitución V0.6 (V0.68, T-80), PC3-01: vía de entrada DIRECTA y modo CONSULTA (D-28).

Sustituye a la de la V0.67, que miraba si detectar() aceptaba la vía DIRECTA: desde la V0.68 un expediente DIRECTA no nace
DETECTADA, sino en el estado del bloque de entrada, y se abre con abrir_directa(). Imprime CUMPLE si el Orquestador abre por
C (EN_ANALISIS), por D (VALIDADA) y por E (COMPARADA), rechaza F y G, y una consulta deja su rastro sin abrir expediente.
Uso, desde marcoC:
    python3 -I entrega_claude/V0.68/scripts/pc3_01_via_directa.py
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "validador"))
sys.path.insert(0, str(RAIZ / "pruebas"))
from pruebas_orquestador import AHORA, encargo, hasta, nuevo  # noqa: E402

fallos = []
o = nuevo()
enc = encargo(1, producer="BROKER")
enc["expediente_id"], enc["correlation_id"], enc["event_id"] = "EXP-PC3-C", "COR-PC3-C", "EV-ENC-PC3-C"
r = o.abrir_directa("EXP-PC3-C", "COR-PC3-C", "TACTICA", "C", "BROKER", AHORA, encargo=enc)
if not (r["ok"] and o.expedientes["EXP-PC3-C"]["estado"] == "EN_ANALISIS"):
    fallos.append(f"por C: {r['codigo']} {r['motivo']}")
o = nuevo()
hasta(o, "VALIDADA", 1)
assert o.descartar("EXP-0001", "el operador lo aparta por ahora", "OPERADOR", AHORA)["ok"]
for b, estado, kw in (("D", "VALIDADA", {}), ("E", "COMPARADA", {"motivo": "candidato único pedido por el operador"})):
    o2 = __import__("copy").deepcopy(o)
    r = o2.abrir_directa(f"EXP-PC3-{b}", f"COR-PC3-{b}", "TACTICA", b, "BROKER", AHORA, analisis="EV-SOB-0001", **kw)
    if not (r["ok"] and o2.expedientes[f"EXP-PC3-{b}"]["estado"] == estado):
        fallos.append(f"por {b}: {r['codigo']} {r['motivo']}")
for b in ("F", "G"):
    if o.abrir_directa(f"EXP-PC3-{b}", f"COR-PC3-{b}", "TACTICA", b, "BROKER", AHORA, analisis="EV-SOB-0001")["ok"]:
        fallos.append(f"{b} se admite como punto de entrada")
n = len(o.expedientes)
r = o.consultar({"consulta_id": "CON-PC3", "correlation_id": "COR-CON-PC3", "tipo": "COMPARAR", "bloque": "D", "cartera": "TACTICA",
                 "analisis": ["EV-SOB-0001"], "pregunta": "¿Supera este análisis al benchmark de la cartera?"}, "BROKER", AHORA)
if not (r["ok"] and len(o.expedientes) == n and o.consultas["entradas"]):
    fallos.append(f"consulta: {r['codigo']} {r['motivo']}")
if fallos:
    print("FALLA: " + "; ".join(fallos))
    sys.exit(1)
print("CUMPLE: el Orquestador abre expedientes DIRECTA por C, D y E en el estado de su bloque, rechaza F y G, y la consulta deja rastro sin abrir expediente (D-28)")
