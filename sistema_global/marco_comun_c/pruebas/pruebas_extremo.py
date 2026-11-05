"""Prueba de extremo a extremo de la Fase 1, con datos SIMULADOS:
detección → encargo → sobre → D (comparar) → E (dimensionar) → propuesta → F → autorización → G (ejecutar) → H (vigilar) → cierre.

Uso: python3 pruebas/pruebas_extremo.py
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from comparador import comparar_candidatos  # noqa: E402
from consola import panel  # noqa: E402
from dimensionado import dimensionar  # noqa: E402
from ejecucion_g import BrokerSimulado, cartera_para_f, conciliar, ejecutar  # noqa: E402
from pruebas_comparador import cand  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_orquestador import AHORA, ENTRADA, SALIDA, Arnes, encargo, nuevo, sobre  # noqa: E402
from vigilancia import vigilar  # noqa: E402

T1 = "2026-11-06T09:05:00+00:00"
HORA_DATOS = "2026-11-06T08:50:00+00:00"


def candidatos(o, ns=(1, 2)):
    """Lleva dos expedientes hasta VALIDADA y devuelve los candidatos para D (sobres de prueba con escenarios propios)."""
    for n in ns:
        eid = f"EXP-{n:04d}"
        assert o.detectar(eid, f"COR-{n:04d}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
        assert o.emitir_encargo(eid, encargo(n), "GESTOR_TACTICA", AHORA)["ok"]
        assert o.entregar_sobre(eid, sobre(n), AHORA)["ok"]


def flujo(h, nombre, precios_finales, esperado_regla, esperado_estado="CERRADA"):
    o = nuevo()
    candidatos(o)
    # D: los sobres de prueba del Orquestador llevan los escenarios de la plantilla; se comparan con los de cand()
    cs = [cand(1), cand(2, esperado=(3.0, 0.5, -4.0))]
    d = comparar_candidatos(cs, AHORA)
    h.chk(nombre + ": D señala un ganador claro", d["ok"] and d["grupos"]["Q"]["decision"] == "CLARA" and d["grupos"]["Q"]["primero"] == "EXP-0001", d)
    ganador = d["grupos"]["Q"]["primero"]
    perdedor = "EXP-0002" if ganador == "EXP-0001" else "EXP-0001"
    h.chk(nombre + ": el Orquestador registra la comparación", o.comparar([ganador, perdedor], "D", AHORA)["ok"])
    b = BrokerSimulado(100000.0, {"EURUSD": 1.10}, HORA_DATOS)
    # E: cantidad con las reglas de F y la cartera real del intermediario
    stop = [c for c in SALIDA["condiciones"] if c["tipo"] == "STOP"][0]
    sol = {"instrumento": ENTRADA["instrumento"], "activo_base": ENTRADA["activo_base"], "direccion": "LARGO", "precio_entrada": ENTRADA["limite"],
           "stop_precio": stop["umbral"], "apalancamiento": 1.0, "cartera": "TACTICA"}
    e = dimensionar(sol, cartera_para_f(b), o.cfg["politica_f"], AHORA, paso=1.0)
    h.chk(nombre + ": E calcula una cantidad", e["ok"] and e["cantidad"] > 0, e)
    h.chk(nombre + ": el Orquestador acepta la propuesta con esa cantidad", o.proponer(ganador, {**ENTRADA, "cantidad": e["cantidad"]}, SALIDA, "GESTOR_TACTICA", AHORA)["ok"])
    inf = informe_f(o, ganador, n=int(ganador[-4:]), cartera=cartera_para_f(b))
    h.chk(nombre + ": F aprueba exactamente lo que propuso E", inf["resultado"] == "APROBADO" and inf["cantidad_aprobada"] == e["cantidad"], inf["resultado"])
    h.chk(nombre + ": el operador autoriza", o.autorizar(ganador, "OPERADOR", inf, AHORA)["ok"])
    r = ejecutar(o, ganador, b, AHORA)
    pid = "POS-" + ganador
    h.chk(nombre + ": G ejecuta, protege y concilia", r["ok"] and o.posiciones[pid]["estado"] == "ABIERTA" and conciliar(o, b, AHORA)["ok"], r)
    h.chk(nombre + ": el panel está en verde con la posición abierta", panel(o, AHORA)["nivel"] == "VERDE", panel(o, AHORA))
    # el mercado se mueve
    for precio in precios_finales:
        b.mover_precio("EURUSD", precio, T1)
    v = vigilar(o, b, {"EURUSD": {"precio": b.precios["EURUSD"], "hora": T1}}, T1)
    h.chk(nombre + f": H aplica {esperado_regla}", [a["regla"] for a in v["acciones"]] == [esperado_regla] and v["acciones"][0]["ok"], v)
    h.chk(nombre + ": la posición queda " + esperado_estado + " y el intermediario plano", o.posiciones[pid]["estado"] == esperado_estado and b.posiciones() == [], b.posiciones())
    h.chk(nombre + ": la conciliación final es limpia y no queda stop vivo", conciliar(o, b, T1)["ok"])
    h.chk(nombre + ": los historiales siguen íntegros", o.integridad() == [], o.integridad())
    h.chk(nombre + ": una pasada más no hace nada", vigilar(o, b, {"EURUSD": {"precio": b.precios["EURUSD"], "hora": T1}}, T1)["acciones"] == [])
    return o, b


def main():
    h = Arnes()
    flujo(h, "objetivo", [1.16], "H-02")
    flujo(h, "stop", [1.04], "H-01")
    # decisión ajustada: el flujo no debe elegir
    d = comparar_candidatos([cand(1), cand(2, instrumento="OTRO")], AHORA)
    h.chk("ajustada: D no señala ganador y el flujo se detiene en el operador", d["grupos"]["Q"]["decision"] == "AJUSTADA" and d["grupos"]["Q"]["primero"] is None)
    # el intermediario cae durante la vigilancia: nada se da por cerrado y el panel lo muestra
    o = nuevo(); candidatos(o)
    assert o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)["ok"]
    b = BrokerSimulado(100000.0, {"EURUSD": 1.10}, HORA_DATOS)
    assert o.proponer("EXP-0001", ENTRADA, SALIDA, "GESTOR_TACTICA", AHORA)["ok"]
    assert o.autorizar("EXP-0001", "OPERADOR", informe_f(o, "EXP-0001", 1, cartera=cartera_para_f(b)), AHORA)["ok"]
    assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]
    b.caido = True
    v = vigilar(o, b, {"EURUSD": {"precio": 1.20, "hora": T1}}, T1)
    h.chk("caida: no se da nada por cerrado y la conciliación falla", o.posiciones["POS-EXP-0001"]["estado"] != "CERRADA" and not v["conciliacion_ok"], v)
    b.caido = False
    v = vigilar(o, b, {"EURUSD": {"precio": 1.20, "hora": T1}}, T1)
    h.chk("caida: al volver la conexión H cierra", o.posiciones["POS-EXP-0001"]["estado"] == "CERRADA" and b.posiciones() == [], v)
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO EXTREMO A EXTREMO:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
