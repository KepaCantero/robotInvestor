"""QA r01 de T-92: ataques a CT-01 durable (C3, H-03), sobre (C2) y R8 (A2, H-01).

Uso: python -I r01_03_contratos.py <ruta a bloque_a/11_Ejecutor>
"""
import sys, tempfile
from pathlib import Path
EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
import bloque_a
assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
from bloque_a.almacen import Almacen
from bloque_a.contratos import Mensajeria, MensajeInvalido
from bloque_a.llm import contenido_sensible

fallos = 0
def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))

CT01 = {"tipo": "AD_HOC", "alcance": {"clases": ["RV"]}, "horizontes": ["H2"], "prioridad": "NORMAL"}

# 1. Espacio de nombres del msg_id: el del Broker (MSG-AAAA-N) y el interno (MSG-AAAA-NNNNNN) pueden coincidir
with tempfile.TemporaryDirectory() as d:
    ms = Mensajeria(Almacen(Path(d)))
    interno = ms.crear("CT-01", "BROKER", "AG-01", CT01)          # sin msg_id: lo numera el bloque
    ms.procesar_una_vez(interno, lambda m: {"run_id": "RUN-1"})
    externo = ms.crear("CT-01", "BROKER", "AG-01", {**CT01, "horizontes": ["H3"], "msg_id": interno["msg_id"]})
    try:
        ms.procesar_una_vez(externo, lambda m: {"run_id": "RUN-2"})
        informe("1a msg_id externo igual a uno interno ya usado", False, "procesado")
    except MensajeInvalido as x:
        informe("1a un msg_id del Broker que coincide con uno interno se distingue (no se rechaza por «reutilizado»)", False,
                f"{interno['msg_id']} → {x}")
    siguiente = ms.crear("CT-01", "BROKER", "AG-01", {**CT01, "msg_id": "MSG-2026-000005"})
    nuevos = [ms.crear("CT-01", "BROKER", "AG-01", {**CT01, "horizontes": ["H4"]})["msg_id"] for _ in range(5)]
    informe("1b un msg_id interno nuevo nunca repite uno que ya trajo el Broker", siguiente["msg_id"] not in nuevos,
            f"externo {siguiente['msg_id']}; internos {nuevos}")
    reg = [r["msg_id"] for r in ms.registro]
    informe("1c el registro de mensajes no tiene dos mensajes distintos con el mismo msg_id", len(reg) == len(set(reg)),
            f"repetidos: {sorted({m for m in reg if reg.count(m) > 1})}")

# 2. Reconciliación: validar antes de mutar (si no se puede dejar la incidencia en HA, la reserva no se libera)
with tempfile.TemporaryDirectory() as d:
    a = Almacen(Path(d)); ms = Mensajeria(a)
    m = ms.crear("CT-01", "BROKER", "AG-01", {**CT01, "msg_id": "MSG-2026-77"})
    try:
        ms.procesar_una_vez(m, lambda _: (_ for _ in ()).throw(RuntimeError("x")))
    except RuntimeError:
        pass
    orig = a.incidencia
    a.incidencia = lambda *x, **k: (_ for _ in ()).throw(OSError("HA no escribible"))
    try:
        ms.reconciliar(m["msg_id"], "revisado")
    except OSError:
        pass
    a.incidencia = orig
    informe("2  si falla la incidencia en HA, la reserva sigue FALLIDA (sin liberación sin rastro)",
            ms.estado_reserva(m["msg_id"])["estado"] == "FALLIDO", ms.estado_reserva(m["msg_id"])["estado"])

# 3. Idempotencia: la respuesta repetida es la misma que la primera
with tempfile.TemporaryDirectory() as d:
    import pandas as pd
    ms = Mensajeria(Almacen(Path(d)))
    m = ms.crear("CT-01", "BROKER", "AG-01", {**CT01, "msg_id": "MSG-2026-88"})
    r1, _ = ms.procesar_una_vez(m, lambda _: {"run_id": "RUN-1", "fecha": pd.Timestamp("2026-06-05"), "n": (1, 2)})
    r2, rep = ms.procesar_una_vez(m, lambda _: {})
    informe("3  repetir el mismo msg_id devuelve la misma respuesta", rep and r1 == r2, f"{r1} vs {r2}")

# 4. msg_id externo con formas raras
with tempfile.TemporaryDirectory() as d:
    ms = Mensajeria(Almacen(Path(d)))
    for malo in ("MSG-2026-1\n", "msg-2026-1", "MSG-2026-", 7, None, "MSG-2026-1; DROP"):
        try:
            x = ms.crear("CT-01", "BROKER", "AG-01", {**CT01, "msg_id": malo})
            ok = malo is None and x["msg_id"].startswith("MSG-")
        except MensajeInvalido:
            ok = malo is not None
        informe(f"4  msg_id externo {malo!r}", ok)

# 5. R8: falsos negativos y positivos del patrón sk-
SK = "s" + "k-"
for texto, esperado in [(f"OPENAI_KEY_{SK}{'A' * 30}", True), (f"key-{SK}{'B' * 30}", True),
                        (f"/{SK}{'C' * 30}", True), ("SK-Hynix-and-Samsung-memory-duopoly", False)]:
    informe(f"5  R8 {texto[:28]!r}… → {'sensible' if esperado else 'limpio'}", contenido_sensible(texto) == esperado)
print("fallos:", fallos)
