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
from ejecucion_g import foto_cartera, BrokerSimulado, cartera_para_f, conciliar, ejecutar  # noqa: E402
from pruebas_comparador import cand  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_orquestador import autorizar_op, AHORA, ENTRADA, SALIDA, Arnes, dim, encargo, nuevo, sobre  # noqa: E402
from vigilancia import vigilar  # noqa: E402

T1 = "2026-11-06T09:05:00+00:00"
HORA_DATOS = "2026-11-06T08:50:00+00:00"


def candidatos(o, ns=(1, 2), apal=1):
    """Lleva dos expedientes hasta VALIDADA: EXP-0001 en EUR/USD y EXP-0002 en GBP/USD con peores escenarios,
    para que D (que ahora ejecuta el propio Orquestador) dé un ganador claro."""
    for n in ns:
        eid = f"EXP-{n:04d}"
        enc, sob = encargo(n), sobre(n)
        if apal != 1:
            enc["payload"]["mandato"]["apalancamiento_max"] = apal
            sob["payload"]["capital"]["apalancamiento"]["valor"] = apal
        if n == 2:
            enc["payload"]["candidato"]["instrumento"] = "GBP/USD"
            sob["payload"]["identificacion"]["instrumento"] = "GBP/USD"
            sob["payload"]["capa2"]["escenarios"] = [{"nombre": "base", "probabilidad": 0.5, "rentabilidad_neta_pct": 1.0, "horizonte_dias": 90},
                                                     {"nombre": "adverso", "probabilidad": 0.3, "rentabilidad_neta_pct": -4.0, "horizonte_dias": 90},
                                                     {"nombre": "favorable", "probabilidad": 0.2, "rentabilidad_neta_pct": 4.0, "horizonte_dias": 90}]
        assert o.detectar(eid, f"COR-{n:04d}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
        r = o.emitir_encargo(eid, enc, "GESTOR_TACTICA", AHORA)
        assert r["ok"], r
        r = o.entregar_sobre(eid, sob, AHORA)
        assert r["ok"], r


def flujo(h, nombre, precios_finales, esperado_regla, esperado_estado="CERRADA"):
    o = nuevo()
    candidatos(o)
    # D: el Orquestador compara con los sobres que guardó
    d = o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    h.chk(nombre + ": D, dentro del Orquestador, señala un ganador claro", d["ok"] and d["ganador"] == "EXP-0001"
          and o.expedientes["EXP-0001"]["comparacion"]["decision"] == "CLARA", d)
    ganador = d["ganador"]
    h.chk(nombre + ": el perdedor no se puede proponer", o.proponer("EXP-0002", {**ENTRADA, "instrumento": "GBPUSD", "activo_base": "GBP"}, SALIDA,
                                                                    "GESTOR_TACTICA", AHORA, None)["codigo"] == "O-22")
    h.chk(nombre + ": ni elegir habiendo un ganador claro", o.elegir("EXP-0002", "OPERADOR", "prefiero este", AHORA)["codigo"] == "O-22")
    b = BrokerSimulado(100000.0, {"EURUSD": 1.10}, HORA_DATOS)
    # E: cantidad con las reglas de F y la cartera real del intermediario
    stop = [c for c in SALIDA["condiciones"] if c["tipo"] == "STOP"][0]
    sol = {"instrumento": ENTRADA["instrumento"], "activo_base": ENTRADA["activo_base"], "divisa_cotizacion": o.divisa(ENTRADA["instrumento"]), "direccion": "LARGO", "precio_entrada": ENTRADA["limite"],
           "stop_precio": stop["umbral"], "apalancamiento": 1.0, "cartera": "TACTICA"}
    foto = foto_cartera(o, b, AHORA)   # G toma y registra la cartera real, con los tipos de cambio del intermediario
    h.chk(nombre + ": G registra la foto de cartera en euros", foto is not None and abs(foto["tipos_cambio_eur"]["USD"] - 1 / 1.10) < 1e-12, foto)
    e = dimensionar(sol, foto, o.cfg["politica_f"], AHORA, paso=1.0)
    h.chk(nombre + ": E calcula una cantidad", e["ok"] and e["cantidad"] > 0, e)
    ent = {**ENTRADA, "cantidad": e["cantidad"]}
    h.chk(nombre + ": una cantidad mayor que la de E se rechaza", o.proponer(ganador, {**ent, "cantidad": e["cantidad"] + 1}, SALIDA, "GESTOR_TACTICA", AHORA,
                                                                            dim(o, ganador, ent, SALIDA, cartera=foto))["codigo"] == "O-23")
    h.chk(nombre + ": el Orquestador acepta la propuesta con la cantidad de E", o.proponer(ganador, ent, SALIDA, "GESTOR_TACTICA", AHORA,
                                                                                         dim(o, ganador, ent, SALIDA, cartera=foto))["ok"])
    inf = informe_f(o, ganador, n=int(ganador[-4:]), cartera=foto)
    h.chk(nombre + ": F aprueba exactamente lo que propuso E", inf["resultado_politica"]["resultado"] == "APROBADO" and inf["payload"]["cantidad_aprobada"] == e["cantidad"], inf["resultado_politica"])
    h.chk(nombre + ": el operador autoriza", autorizar_op(o, ganador, inf, AHORA)["ok"])
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
    # abstención: si ninguno supera a no hacer nada (referencia de la cartera), el flujo se detiene en D sin órdenes
    from comparador import REFERENCIA_EFECTIVO
    refs = {c: dict(REFERENCIA_EFECTIVO) for c in ("TRADING", "TACTICA", "LARGO_PLAZO")}
    refs["TACTICA"]["rentabilidad_anual_pct"] = 40.0
    o = nuevo({"referencias": refs}); candidatos(o)
    r = o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)
    h.chk("abstencion: D concluye no hacer nada y nadie se puede proponer", r["decision_global"] == "ABSTENERSE" and r["ganador"] is None
          and o.proponer("EXP-0001", ENTRADA, SALIDA, "GESTOR_TACTICA", AHORA, dim(o))["codigo"] == "O-22" and o.posiciones == {}, r)
    # el intermediario cae durante la vigilancia: nada se da por cerrado y el panel lo muestra
    o = nuevo(); candidatos(o)
    assert o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)["ok"]
    b = BrokerSimulado(100000.0, {"EURUSD": 1.10}, HORA_DATOS)
    assert o.proponer("EXP-0001", ENTRADA, SALIDA, "GESTOR_TACTICA", AHORA, dim(o, cartera=cartera_para_f(b)))["ok"]
    assert autorizar_op(o, "EXP-0001", informe_f(o, "EXP-0001", 1, cartera=cartera_para_f(b)), AHORA)["ok"]
    assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]
    b.caido = True
    v = vigilar(o, b, {"EURUSD": {"precio": 1.20, "hora": T1}}, T1)
    h.chk("caida: no se da nada por cerrado y la conciliación falla", o.posiciones["POS-EXP-0001"]["estado"] != "CERRADA" and not v["conciliacion_ok"], v)
    h.chk("caida: no poder conciliar degrada las carteras", o.nivel("TACTICA") == "L1" and any("SIN_CONEXION" in x["motivo"] for x in o.avisos), o.degradadas)
    b.caido = False
    v = vigilar(o, b, {"EURUSD": {"precio": 1.20, "hora": T1}}, T1)
    h.chk("caida: al volver la conexión H prepara el cierre (L1)", [a["regla"] for a in v["acciones"]] == ["H-10"] and o.posiciones["POS-EXP-0001"]["estado"] == "ABIERTA", v)
    for x in o.avisos:
        if x["acuse"] is None:
            o.acusar_aviso(x["id"], "OPERADOR", T1)
    assert o.restablecer_nivel("TACTICA", "OPERADOR", T1)["ok"]
    v = vigilar(o, b, {"EURUSD": {"precio": 1.20, "hora": T1}}, T1)
    h.chk("caida: restablecida la cartera, H cierra", o.posiciones["POS-EXP-0001"]["estado"] == "CERRADA" and b.posiciones() == [], v)
    # apalancamiento: sin permiso se rechaza; con permiso y política de F que lo admita, el recorrido funciona
    o = nuevo(); candidatos(o)
    assert o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)["ok"]
    r = o.proponer("EXP-0001", {**ENTRADA, "apalancamiento": 2.0}, SALIDA, "GESTOR_TACTICA", AHORA, dim(o, entrada={**ENTRADA, "apalancamiento": 2.0}))
    h.chk("apalancamiento: sin permiso la propuesta se rechaza", not r["ok"] and r["codigo"] == "O-06", r)
    from control_f import POLITICA_DEFECTO
    o = nuevo({"apalancamiento_permitido": True, "politica_f": {**POLITICA_DEFECTO, "apalancamiento_max": 3.0}}); candidatos(o, apal=2)
    assert o.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)["ok"]
    b = BrokerSimulado(100000.0, {"EURUSD": 1.10}, HORA_DATOS)
    ap2 = {**ENTRADA, "apalancamiento": 2.0}
    h.chk("apalancamiento: más que el analizado en el sobre se rechaza", o.proponer("EXP-0001", {**ap2, "apalancamiento": 2.5}, SALIDA, "GESTOR_TACTICA", AHORA,
                                                                                     dim(o, entrada={**ap2, "apalancamiento": 2.5}, cartera=cartera_para_f(b)))["codigo"] == "O-21")
    h.chk("apalancamiento: con permiso la propuesta se acepta", o.proponer("EXP-0001", ap2, SALIDA, "GESTOR_TACTICA", AHORA, dim(o, entrada=ap2, cartera=cartera_para_f(b)))["ok"])
    inf = informe_f(o, "EXP-0001", 1, cartera=cartera_para_f(b))
    h.chk("apalancamiento: F lo aprueba dentro de su máximo", inf["resultado_politica"]["resultado"] in ("APROBADO", "REDUCIDO"), inf["resultado_politica"])
    h.chk("apalancamiento: se autoriza y se ejecuta", autorizar_op(o, "EXP-0001", inf, AHORA)["ok"] and ejecutar(o, "EXP-0001", b, AHORA)["ok"])
    o2 = nuevo({"apalancamiento_permitido": True, "politica_f": {**POLITICA_DEFECTO, "apalancamiento_max": 3.0}}); candidatos(o2, apal=5)
    assert o2.comparar(["EXP-0001", "EXP-0002"], "D", AHORA)["ok"]
    ap5 = {**ENTRADA, "apalancamiento": 5.0}
    r = o2.proponer("EXP-0001", ap5, SALIDA, "GESTOR_TACTICA", AHORA, dim(o2, entrada=ap5, cartera=cartera_para_f(b)))
    h.chk("apalancamiento: por encima del máximo de F, E ya no da cantidad y la propuesta se rechaza", r["codigo"] == "O-23", r)
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO EXTREMO A EXTREMO:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
