"""QA r01 · sonda 02: el expediente DIRECTA hereda `encargo_actual` del ORIGEN, que no tiene por qué ser el encargo al que respondió
el sobre reutilizado. Si el origen se volvió a encargar después de validar (observar → re-encargo → apartar por el operador), el
DIRECTA queda con el sobre viejo y el encargo nuevo. Con eso:
  a) un análisis hecho para EXPLORAR (N1) llega a PROPUESTA, saltándose la regla T-26 («un encargo EXPLORAR no lleva a una orden»);
  b) el sello que se vigila (_sello_anulado) es el del encargo nuevo, no el del análisis reutilizado.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import (AHORA, ENTRADA, SALIDA, chk, dim, encargo, fin, nuevo, sobre_para)  # noqa: E402


def escenario():
    o = nuevo()
    assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    e1 = encargo(1)
    e1["payload"]["nivel_analisis"], e1["payload"]["decision_informada"] = "N1", "EXPLORAR"
    r = o.emitir_encargo("EXP-0001", e1, "GESTOR_TACTICA", AHORA)
    assert r["ok"], r
    s1 = sobre_para(1, None)
    s1["payload"]["identificacion"]["nivel_analisis"] = "N1"
    r = o.entregar_sobre("EXP-0001", s1, AHORA)
    assert r["ok"], r
    # el operador lo aparta y lo vuelve a encargar, ahora para abrir posición (N3)
    assert o.observar("EXP-0001", [{"tipo": "FECHA", "fecha": "2026-11-20"}], "el operador lo deja para más adelante", "OPERADOR", AHORA)["ok"]
    assert o.reabrir("EXP-0001", "el operador quiere un análisis completo", "OPERADOR", AHORA)["ok"]
    e2 = encargo(1)
    e2["event_id"] = "EV-ENC-0001-B"   # ABRIR_POSICION, N3 (el encargo de prueba por defecto)
    r = o.emitir_encargo("EXP-0001", e2, "GESTOR_TACTICA", AHORA)
    assert r["ok"], r
    # antes de que llegue el sobre nuevo, el operador lo aparta (sigue con el sobre S1 y con encargo_actual = E2)
    assert o.observar("EXP-0001", [{"tipo": "FECHA", "fecha": "2026-11-20"}], "el operador lo aparta otra vez", "OPERADOR", AHORA)["ok"]
    return o


o = escenario()
x = o.expedientes["EXP-0001"]
print("origen:", x["estado"], "sobre", x["sobre"]["event_id"], "nivel", x["sobre"]["nivel"], "encargo_actual", x["encargo_actual"],
      o.encargos[x["encargo_actual"]]["msg"]["payload"]["decision_informada"])
reg = {f["analisis"]: f for f in o.analisis_vigentes(AHORA, "TACTICA")}
print("registro:", reg.get("EV-SOB-0001"))
r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
print("abrir_directa:", r)
e = o.expedientes.get("EXP-DD-01")
chk("el_DIRECTA_no_hereda_un_encargo_al_que_su_sobre_no_respondio",
    e is None or e["encargo_actual"] == "EV-ENC-0001", (e or {}).get("encargo_actual"))
if e is not None:
    r = o.comparar(["EXP-DD-01"], "D", AHORA)
    print("comparar:", r["ok"], r["codigo"], r.get("ganador"))
    r = o.proponer("EXP-DD-01", ENTRADA, SALIDA, "BROKER", AHORA, dim(o, "EXP-DD-01"))
    print("proponer:", r)
    chk("un_analisis_N1_EXPLORAR_no_llega_a_PROPUESTA_T26", not r["ok"], r)
    print("integridad():", o.integridad())
    if r["ok"]:
        from r01_comun import autorizar_op, informe_f
        r = autorizar_op(o, "EXP-DD-01", informe_f(o, "EXP-DD-01", 41), AHORA)
        print("autorizar (F y operador):", r["ok"], r["codigo"], r["motivo"][:100])
        chk("el_analisis_EXPLORAR_no_llega_a_AUTORIZADA", not r["ok"], r)

# contraste: el mismo análisis EXPLORAR sin re-encargo SÍ se rechaza al proponer (T-26 funciona en el caso simple)
o2 = nuevo()
assert o2.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
e1 = encargo(1)
e1["payload"]["nivel_analisis"], e1["payload"]["decision_informada"] = "N1", "EXPLORAR"
assert o2.emitir_encargo("EXP-0001", e1, "GESTOR_TACTICA", AHORA)["ok"]
s1 = sobre_para(1, None)
s1["payload"]["identificacion"]["nivel_analisis"] = "N1"
assert o2.entregar_sobre("EXP-0001", s1, AHORA)["ok"]
assert o2.descartar("EXP-0001", "el operador lo aparta", "OPERADOR", AHORA)["ok"]
assert o2.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")["ok"]
assert o2.comparar(["EXP-DD-01"], "D", AHORA)["ok"]
r = o2.proponer("EXP-DD-01", ENTRADA, SALIDA, "BROKER", AHORA, dim(o2, "EXP-DD-01"))
chk("contraste_sin_reencargo_EXPLORAR_se_rechaza_O06", not r["ok"] and r["codigo"] == "O-06", r)
sys.exit(fin())
