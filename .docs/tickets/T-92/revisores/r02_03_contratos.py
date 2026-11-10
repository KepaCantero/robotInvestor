"""QA r02 de T-92 (revisor nuevo): CT-01 durable tras H-08, H-12 y H-13. Repite los casos 2 a 4 de `r01_03` (que ya no
llegan a ejecutarse porque su caso 1 usa el formato antiguo del msg_id) con el formato nuevo `MSG-BRK-AAAA-N`.

Uso: python -I r02_03_contratos.py <ruta a bloque_a/11_Ejecutor>
"""
import sys, tempfile
from pathlib import Path
EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ))
import bloque_a
assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
import pandas as pd
from bloque_a.almacen import Almacen
from bloque_a.configuracion import CLASES
from bloque_a.contratos import Mensajeria, MensajeInvalido

fallos = 0
def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))

CT01 = {"tipo": "AD_HOC", "alcance": {"clases": ["RV"]}, "horizontes": ["H2"], "prioridad": "NORMAL"}

# 1. Espacios separados: ningún identificador interno (con o sin ámbito de clase) cae en MSG-BRK-
with tempfile.TemporaryDirectory() as d:
    ms = Mensajeria(Almacen(Path(d)))
    internos = [ms.crear("CT-01", "BROKER", "AG-01", CT01)["msg_id"]]
    for c in CLASES:
        with ms.ambito(c):
            internos.append(ms.crear("CT-03", "BROKER", "AG-01", {"pregunta": "x"})["msg_id"])
    informe("1a ningún msg_id interno empieza por MSG-BRK-", not any(i.startswith("MSG-BRK-") for i in internos), str(internos[:3]))
    externo = ms.crear("CT-01", "BROKER", "AG-01", {**CT01, "msg_id": "MSG-BRK-2026-000001"})
    r, rep = ms.procesar_una_vez(externo, lambda m: {"run_id": "RUN-1"})
    nuevo = ms.crear("CT-01", "BROKER", "AG-01", {**CT01, "horizontes": ["H4"]})
    r2, rep2 = ms.procesar_una_vez(nuevo, lambda m: {"run_id": "RUN-2"})
    informe("1b un CT-01 sin msg_id después de uno del Broker se procesa (no choca)", not rep2 and r2 == {"run_id": "RUN-2"})
    for malo in ("MSG-2026-000001", "MSG-BRK-2026-", "MSG-BRK-26-1", "MSG-BRK-2026-1\n", "msg-brk-2026-1", "MSG-BRK-2026-" + "1" * 13,
                 7, ["MSG-BRK-2026-1"]):
        try:
            ms.crear("CT-01", "BROKER", "AG-01", {**CT01, "msg_id": malo}); ok = False
        except MensajeInvalido:
            ok = True
        informe(f"1c msg_id externo {malo!r} se rechaza", ok)

# 2. Reconciliación: si HA falla, la reserva no se libera (H-12)
with tempfile.TemporaryDirectory() as d:
    a = Almacen(Path(d)); ms = Mensajeria(a)
    m = ms.crear("CT-01", "BROKER", "AG-01", {**CT01, "msg_id": "MSG-BRK-2026-77"})
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
    informe("2a si falla la incidencia en HA, la reserva sigue FALLIDA", ms.estado_reserva(m["msg_id"])["estado"] == "FALLIDO")
    lib = ms.reconciliar(m["msg_id"], "F5 revisado")
    r, rep = ms.procesar_una_vez(m, lambda _: {"run_id": "RUN-9"})
    informe("2b tras reconciliar, el mismo msg_id se procesa y deja la incidencia",
            lib["estado"] == "LIBERADA" and not rep and any("liberada" in e["detalle"] for e in a.leer("HA")))
    try:
        ms.reconciliar(m["msg_id"], "otra vez"); ok = False
    except MensajeInvalido:
        ok = True
    informe("2c no se reconcilia un mensaje COMPLETADO", ok)

# 3. Idempotencia: la respuesta repetida es igual a la primera (H-13)
with tempfile.TemporaryDirectory() as d:
    ms = Mensajeria(Almacen(Path(d)))
    m = ms.crear("CT-01", "BROKER", "AG-01", {**CT01, "msg_id": "MSG-BRK-2026-88"})
    r1, _ = ms.procesar_una_vez(m, lambda _: {"run_id": "RUN-1", "fecha": pd.Timestamp("2026-06-05"), "n": (1, 2), "x": float("nan")})
    r2, rep = ms.procesar_una_vez(m, lambda _: {})
    informe("3  repetir el mismo msg_id devuelve la misma respuesta", rep and str(r1) == str(r2), f"{r1} vs {r2}")
print("fallos:", fallos)
