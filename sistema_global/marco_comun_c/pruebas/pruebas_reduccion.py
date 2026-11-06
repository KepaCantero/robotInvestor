"""Pruebas de la reducción parcial con stop redimensionado (T-12), con un intermediario SIMULADO. Datos SIMULADOS.

Comprueba: reducción pedida por el operador y automática por un OBJETIVO con fracción declarada; el stop nuevo se pone
antes de retirar el anterior y nunca puede abrir la posición contraria (solo reducción); reintentos tras caídas;
ejecuciones parciales; el stop que salta a mitad; la conciliación durante la reducción; la integridad del estado.

Uso: python3 pruebas/pruebas_reduccion.py
"""
import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from ejecucion_g import BrokerSimulado, ConexionPerdida, cerrar, conciliar, ejecutar, reducir  # noqa: E402
from vigilancia import vigilar  # noqa: E402
from pruebas_ejecucion_g import HORA_DATOS, autorizado, broker  # noqa: E402
from pruebas_orquestador import AHORA, INV, OBJ, STOP, Arnes, ENTRADA, hasta, nuevo  # noqa: E402

T1 = "2026-11-06T09:05:00+00:00"
T2 = "2026-11-06T09:10:00+00:00"
PID = "POS-EXP-0001"
S0 = "ORD-EXP-0001-S-1"                 # stop de la entrada
OBJ_P = {"id": "OBJ-P", "tipo": "OBJETIVO", "metrica": "precio", "operador": ">=", "umbral": 1.12, "unidad": "USD", "fraccion": 0.5}
SAL_P = {"condiciones": [STOP, OBJ, OBJ_P, INV], "fecha": "2026-12-05"}


def abierta(**kw):
    o, b = autorizado(**kw)
    r = ejecutar(o, "EXP-0001", b, AHORA)
    assert r["ok"], r
    if isinstance(b, Vigilado):
        b.fallos.clear()   # la invariante se vigila desde que la posición está abierta y protegida
    return o, b


def datos(precio, hora=T1):
    return {"EURUSD": {"precio": precio, "hora": hora}}


def red(o, b, q=40.0, ahora=T1, **kw):
    kw.setdefault("actor", "OPERADOR")
    kw.setdefault("motivo", "reducir riesgo")
    return reducir(o, PID, b, ahora, cantidad=q, **kw)


def neto(b):
    return sum(p["cantidad"] for p in b.posiciones())


def ejecutadas(b, prefijo):
    return [k for k, r in b.ordenes.items() if k.startswith(prefijo) and r["ejecutada"] > 0]


class Vigilado(BrokerSimulado):
    """Tras cada operación comprueba la invariante: si hay posición, hay un stop vivo que la cubre entera
    y nunca hay posición contraria a la del sistema."""
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.fallos = []

    def _chk(self, que):
        n = sum(v["cantidad"] for v in self.pos.values())
        if n < -1e-6:
            self.fallos.append(f"{que}: posición contraria {n}")
        if n > 1e-6 and not any(r["estado"] == "ACEPTADA" and r["orden"]["tipo"] == "STOP" and r["orden"]["lado"] == "VENTA"
                                and r["orden"]["cantidad"] + 1e-6 >= n for r in self.ordenes.values()):
            self.fallos.append(f"{que}: {n} sin stop que la cubra")

    def enviar(self, o):
        r = super().enviar(o)
        self._chk(f"enviar {o.get('orden_id')}")
        return r

    def cancelar(self, oid):
        r = super().cancelar(oid)
        self._chk(f"cancelar {oid}")
        return r


def vigilado(**kw):
    return Vigilado(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0}, **kw)


def main():
    h = Arnes()
    # ------------------------------------------------------------ camino feliz del operador
    o, b = abierta(b=vigilado())
    r = red(o, b)
    p = o.posiciones[PID]
    sid = "ORD-POS-EXP-0001-R1-S-1"
    h.chk("operador_reduce_40_de_100", r["ok"] and r["restante"] == 60.0 and p["estado"] == "ABIERTA" and p["cantidad"] == 60.0 and neto(b) == 60.0, r)
    nuevo_stop = b.consultar(sid)
    h.chk("stop_nuevo_del_tamano_de_lo_que_queda", nuevo_stop["estado"] == "ACEPTADA" and nuevo_stop["cantidad"] == 60.0 and nuevo_stop["precio"] == 1.05
          and nuevo_stop["solo_reduccion"], nuevo_stop)
    h.chk("stop_anterior_retirado", b.consultar(S0)["estado"] == "CANCELADA")
    h.chk("orquestador_anota_stops_y_reduccion", p["protecciones"] == [sid] and p["protecciones_anteriores"] == [S0] and len(p["reducciones"]) == 1
          and p["reducciones"][0]["restante"] == 60.0 and p["reduccion"] is None and p["cantidad_inicial"] == 100.0, p)
    h.chk("nunca_sin_stop_ni_al_reves", b.fallos == [], b.fallos)
    c = conciliar(o, b, T1)
    h.chk("concilia_tras_reducir", c["ok"] and c["diferencias"] == [], c)
    h.chk("integridad_tras_reducir", o.integridad() == [])
    r = red(o, b, 30.0, T2)
    p = o.posiciones[PID]
    h.chk("segunda_reduccion", r["ok"] and p["cantidad"] == 30.0 and neto(b) == 30.0 and p["protecciones"] == ["ORD-POS-EXP-0001-R2-S-1"]
          and p["protecciones_anteriores"] == [S0, sid] and b.consultar(sid)["estado"] == "CANCELADA" and conciliar(o, b, T2)["ok"], r)
    b.mover_precio("EURUSD", 1.04, T2)
    h.chk("el_stop_redimensionado_cierra_lo_que_queda_y_no_mas", neto(b) == 0.0 and b.fallos == [], b.posiciones())
    r = vigilar(o, b, datos(1.04, T2), T2)
    h.chk("H01_confirma_el_cierre_tras_reducir", o.posiciones[PID]["estado"] == "CERRADA" and r["conciliacion_ok"], r)

    # ------------------------------------------------------------ peticiones no válidas: no se envía nada
    for nombre, kw in (("sin_motivo", {"motivo": ""}), ("todo", {"q": 100.0}), ("mas_que_todo", {"q": 150.0}), ("cero", {"q": 0.0}),
                       ("negativa", {"q": -5.0}), ("texto", {"q": "40"}), ("G_sin_condicion", {"actor": "G"}),
                       ("H_no_puede", {"actor": "H"})):
        o, b = abierta()
        antes = copy.deepcopy(b.ordenes)
        q = kw.pop("q", 40.0)
        r = red(o, b, q, **kw)
        h.chk(f"reduccion_{nombre}_rechazada_sin_enviar", r["codigo"] == "G-06" and b.ordenes == antes and o.posiciones[PID]["estado"] == "ABIERTA", r)
    o, b = abierta()
    o.posiciones[PID]["estado"] = "CERRADA"
    h.chk("posicion_no_reducible_G06", red(o, b)["codigo"] == "G-06")

    # ------------------------------------------------------------ el stop salta a mitad de la reducción
    class SaltaAlVender(Vigilado):
        def enviar(self, x):
            if x.get("tipo") == "MERCADO":
                self.mover_precio("EURUSD", 1.04)   # el stop anterior salta justo antes de la venta
            return super().enviar(x)
    o, b = abierta(b=SaltaAlVender(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0}))
    r = red(o, b)
    h.chk("stop_salta_a_mitad_se_termina_como_cierre_sin_posicion_contraria", o.posiciones[PID]["estado"] == "CERRADA" and neto(b) == 0.0
          and not [f for f in b.fallos if "contraria" in f] and conciliar(o, b, T1)["ok"], (r, b.fallos, b.posiciones()))

    # ------------------------------------------------------------ caídas y reintentos (idempotencia)
    class CaeTrasVender(BrokerSimulado):
        armado = True
        def enviar(self, x):
            r = super().enviar(x)
            if x.get("tipo") == "MERCADO" and self.armado:
                self.armado = False
                raise ConexionPerdida("se cae tras vender")
            return r
    o, b = abierta(b=CaeTrasVender(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0}))
    r = red(o, b)
    h.chk("caida_tras_vender_G08_incierto", r["codigo"] == "G-08" and o.posiciones[PID]["estado"] == "REDUCIENDO" and neto(b) == 60.0, r)
    c = conciliar(o, b, T1)
    h.chk("a_media_reduccion_la_diferencia_esta_explicada", c["ok"] and any(x["tipo"] == "REDUCCION_EN_CURSO" for x in c["explicadas"]), c)
    r = vigilar(o, b, datos(1.10), T1)
    h.chk("H08_retoma_y_termina_sin_vender_dos_veces", o.posiciones[PID]["estado"] == "ABIERTA" and o.posiciones[PID]["cantidad"] == 60.0
          and neto(b) == 60.0 and len(ejecutadas(b, "ORD-POS-EXP-0001-R1-M")) == 1 and r["conciliacion_ok"], (r, b.posiciones()))

    class CaeAlCancelar(BrokerSimulado):
        armado = True
        def cancelar(self, oid):
            if self.armado:
                self.armado = False
                raise ConexionPerdida("se cae al retirar el stop anterior")
            return super().cancelar(oid)
    o, b = abierta(b=CaeAlCancelar(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0}))
    r = red(o, b)
    h.chk("caida_con_dos_stops_vivos_G08", r["codigo"] == "G-08" and b.consultar(S0)["estado"] == "ACEPTADA"
          and b.consultar("ORD-POS-EXP-0001-R1-S-1")["estado"] == "ACEPTADA", r)
    h.chk("dos_stops_de_solo_reduccion_no_son_discrepancia", conciliar(o, b, T1)["ok"])
    r = red(o, b)
    h.chk("reintento_reutiliza_el_stop_nuevo", r["ok"] and r["stop_id"] == "ORD-POS-EXP-0001-R1-S-1" and b.consultar("ORD-POS-EXP-0001-R1-S-2") is None
          and b.consultar(S0)["estado"] == "CANCELADA" and conciliar(o, b, T1)["ok"], r)
    b.mover_precio("EURUSD", 1.04, T1)
    h.chk("con_dos_stops_saltan_ambos_y_no_da_la_vuelta", neto(b) == 0.0)

    o, b = abierta(b=broker(caido=False))
    o.posicion_transicion(PID, "REDUCIENDO", "OPERADOR", T1, motivo="reducir", cantidad=40.0)
    b.caido = True
    r = reducir(o, PID, b, T1)
    h.chk("sin_conexion_antes_de_enviar_G01", r["codigo"] == "G-01" and o.posiciones[PID]["estado"] == "REDUCIENDO", r)
    b.caido = False
    h.chk("retomar_con_otra_cantidad_G06", reducir(o, PID, b, T1, cantidad=10.0)["codigo"] == "G-06")
    h.chk("retomar_sin_parametros_termina", reducir(o, PID, b, T1)["ok"] and neto(b) == 60.0)

    # ------------------------------------------------------------ ejecuciones parciales y rechazos
    o, b = abierta(b=vigilado(fraccion_mercado=0.5))
    r = red(o, b)
    h.chk("venta_muy_parcial_G12_sigue_reduciendo", r["codigo"] == "G-12" and o.posiciones[PID]["estado"] == "REDUCIENDO" and 60.0 < neto(b) < 100.0
          and b.consultar(S0)["estado"] == "ACEPTADA" and b.fallos == [], (r, neto(b)))
    c = conciliar(o, b, T1)
    h.chk("parcial_explicada_y_protegida", c["ok"], c)
    b.fraccion_mercado = 1.0
    r = vigilar(o, b, datos(1.10), T1)
    h.chk("reintento_completa_la_parcial", o.posiciones[PID]["estado"] == "ABIERTA" and o.posiciones[PID]["cantidad"] == 60.0 and neto(b) == 60.0
          and b.fallos == [] and r["conciliacion_ok"], (r, neto(b)))

    class RechazaStopNuevo(BrokerSimulado):
        def enviar(self, x):
            if x.get("tipo") == "STOP" and "-R" in x["orden_id"]:
                self.ordenes[x["orden_id"]] = {"orden": dict(x), "estado": "RECHAZADA", "ejecutada": 0.0, "precio_medio": None}
                return self._res(self.ordenes[x["orden_id"]])
            return super().enviar(x)
    o, b = abierta(b=RechazaStopNuevo(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0}))
    r = red(o, b)
    h.chk("stop_nuevo_rechazado_G12_y_el_anterior_sigue", r["codigo"] == "G-12" and b.consultar(S0)["estado"] == "ACEPTADA" and neto(b) == 60.0
          and o.posiciones[PID]["estado"] == "REDUCIENDO" and any("REDUCCION_INCOMPLETA" in str(a) for a in o.avisos), r)
    h.chk("stop_anterior_cubre_lo_que_queda", conciliar(o, b, T1)["ok"])

    o, b = abierta()
    b.rechaza_mercado = True
    r = red(o, b)
    h.chk("venta_rechazada_G12_sin_tocar_el_stop", r["codigo"] == "G-12" and neto(b) == 100.0 and b.consultar(S0)["estado"] == "ACEPTADA", r)

    # ------------------------------------------------------------ cierre total desde REDUCIENDO
    o, b = abierta(b=vigilado(fraccion_mercado=0.5))
    red(o, b)
    b.fraccion_mercado = 1.0
    r = cerrar(o, PID, b, T1, actor="OPERADOR", motivo="cerrar del todo")
    h.chk("cierre_total_desde_reduciendo", r["ok"] and o.posiciones[PID]["estado"] == "CERRADA" and neto(b) == 0.0 and conciliar(o, b, T1)["ok"]
          and o.posiciones[PID]["reducciones"][-1].get("interrumpida") == "cierre", r)
    o, b = abierta(b=CaeAlCancelar(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0}))
    red(o, b)
    r = cerrar(o, PID, b, T1, actor="OPERADOR", motivo="cerrar del todo")
    h.chk("el_cierre_retira_tambien_los_stops_de_la_reduccion", r["ok"] and b.consultar("ORD-POS-EXP-0001-R1-S-1")["estado"] == "CANCELADA"
          and conciliar(o, b, T1)["ok"], r)

    # ------------------------------------------------------------ reducción automática por un OBJETIVO con fracción
    o, b = abierta(salida=SAL_P)
    r = vigilar(o, b, datos(1.125), T1)
    h.chk("H12_objetivo_parcial_reduce_la_mitad", [a["regla"] for a in r["acciones"]] == ["H-12"] and r["acciones"][0]["ok"]
          and o.posiciones[PID]["cantidad"] == 50.0 and neto(b) == 50.0 and o.posiciones[PID]["condiciones_consumidas"] == ["OBJ-P"]
          and r["conciliacion_ok"], r)
    r = vigilar(o, b, datos(1.125, T2), T2)
    h.chk("la_toma_parcial_no_se_repite", r["acciones"] == [] and neto(b) == 50.0, r)
    r = vigilar(o, b, datos(1.15, T2), T2)
    h.chk("despues_el_objetivo_total_cierra", [a["regla"] for a in r["acciones"]] == ["H-02"] and o.posiciones[PID]["estado"] == "CERRADA"
          and neto(b) == 0.0, r)
    o, b = abierta(salida=SAL_P)
    o.degradar("TACTICA", "prueba", "OPERADOR", T1)
    antes = copy.deepcopy(b.ordenes)
    r = vigilar(o, b, datos(1.125), T1)
    h.chk("en_L1_H_prepara_la_reduccion_y_no_vende", [a["regla"] for a in r["acciones"]] == ["H-10"] and b.ordenes == antes
          and any("REDUCCIÓN PREPARADA" in x["texto"] for x in o.posiciones[PID]["propuestas"]), r)
    h.chk("en_L1_el_operador_confirma", red(o, b, 50.0)["ok"] and neto(b) == 50.0)
    o, b = abierta(salida=SAL_P)
    cond = {"id": "OBJ-P", "valor_observado": 1.125}
    h.rechaza("automatica_con_otra_cantidad_O06", o, lambda: o.posicion_transicion(PID, "REDUCIENDO", "G", T1, condicion=cond, cantidad=10.0), "O-06")
    h.rechaza("fraccion_no_sirve_para_cerrar_O06", o, lambda: o.posicion_transicion(PID, "CERRANDO", "G", T1, condicion=cond), "O-06")
    h.rechaza("objetivo_parcial_sin_cumplirse_O06", o, lambda: o.posicion_transicion(PID, "REDUCIENDO", "G", T1, condicion={"id": "OBJ-P", "valor_observado": 1.11}), "O-06")
    h.rechaza("objetivo_total_no_reduce_O06", o, lambda: o.posicion_transicion(PID, "REDUCIENDO", "G", T1, condicion={"id": "OBJ-1", "valor_observado": 1.15}), "O-06")
    h.chk("automatica_con_su_cantidad", reducir(o, PID, b, T1, condicion=cond)["ok"] and neto(b) == 50.0)
    h.rechaza("condicion_consumida_O06", o, lambda: o.posicion_transicion(PID, "REDUCIENDO", "G", T1, condicion=cond), "O-06")

    # ------------------------------------------------------------ la fracción en la propuesta
    for nombre, cambio in (("en_un_stop", lambda s: s["condiciones"][0].__setitem__("fraccion", 0.5)),
                           ("igual_a_uno", lambda s: s["condiciones"][2].__setitem__("fraccion", 1.0)),
                           ("cero", lambda s: s["condiciones"][2].__setitem__("fraccion", 0)),
                           ("texto", lambda s: s["condiciones"][2].__setitem__("fraccion", "0.5")),
                           ("suman_todo", lambda s: s["condiciones"].insert(3, {**OBJ_P, "id": "OBJ-Q", "fraccion": 0.5}))):
        o = nuevo()
        sal = copy.deepcopy(SAL_P)
        cambio(sal)
        hasta(o, "COMPARADA", salida=sal)
        from pruebas_orquestador import dim, elegir_si_hace_falta
        elegir_si_hace_falta(o, "EXP-0001")
        r = o.proponer("EXP-0001", ENTRADA, sal, "GESTOR_TACTICA", AHORA, dim(o, "EXP-0001", None, sal))
        h.chk(f"fraccion_{nombre}_O01", r["codigo"] == "O-01", r)

    # ------------------------------------------------------------ el Orquestador al terminar una reducción
    o, b = abierta()
    o.posicion_transicion(PID, "REDUCIENDO", "OPERADOR", T1, motivo="reducir", cantidad=40.0)
    ORD = {"orden_id": "ORD-R-X", "conciliada": True}
    h.rechaza("restante_por_encima_del_objetivo_O06", o, lambda: o.posicion_transicion(PID, "ABIERTA", "G", T1, restante=80.0, orden=ORD, protecciones=["ORD-NUEVO"]), "O-06")
    h.rechaza("sin_stop_nuevo_O06", o, lambda: o.posicion_transicion(PID, "ABIERTA", "G", T1, restante=60.0, orden=ORD), "O-06")
    h.rechaza("stop_vacio_O06", o, lambda: o.posicion_transicion(PID, "ABIERTA", "G", T1, restante=60.0, orden=ORD, protecciones=[]), "O-06")
    h.rechaza("stop_igual_a_la_orden_O03", o, lambda: o.posicion_transicion(PID, "ABIERTA", "G", T1, restante=60.0, orden=ORD, protecciones=["ORD-R-X"]), "O-03")
    h.rechaza("stop_ya_usado_en_otra_cosa_O03", o, lambda: o.posicion_transicion(PID, "ABIERTA", "G", T1, restante=60.0, orden=ORD,
                                                                                    protecciones=["ORD-EXP-0001-E-1"]), "O-03")
    h.rechaza("solo_G_termina_O05", o, lambda: o.posicion_transicion(PID, "ABIERTA", "OPERADOR", T1, restante=60.0, orden=ORD, protecciones=["ORD-N"]), "O-05")
    h.rechaza("stops_solo_al_terminar_O01", o, lambda: o.posicion_transicion(PID, "CERRANDO", "OPERADOR", T1, motivo="x", protecciones=["ORD-N"]), "O-01")
    h.chk("termina_con_stop_nuevo", o.posicion_transicion(PID, "ABIERTA", "G", T1, restante=60.0, orden=ORD, protecciones=["ORD-NUEVO"])["ok"])
    o.posicion_transicion(PID, "REDUCIENDO", "OPERADOR", T1, motivo="otra", cantidad=10.0)
    h.rechaza("stop_retirado_no_vuelve_O03", o, lambda: o.posicion_transicion(PID, "ABIERTA", "G", T1, restante=50.0, orden={"orden_id": "ORD-R-Y", "conciliada": True},
                                                                                 protecciones=[S0]), "O-03")
    h.rechaza("cantidad_fuera_de_reduccion_O01", o, lambda: o.posicion_transicion(PID, "CERRANDO", "OPERADOR", T1, motivo="x", cantidad=5.0), "O-01")

    # ------------------------------------------------------------ integridad del estado de control
    for nombre, mut in (("cantidad", lambda p: p.__setitem__("cantidad", 1000.0)),
                        ("stops", lambda p: p.__setitem__("protecciones", ["ORD-FALSO"])),
                        ("inicial", lambda p: p.__setitem__("cantidad_inicial", 1000.0)),
                        ("consumidas", lambda p: p["condiciones_consumidas"].append("OBJ-P"))):
        o, b = abierta()
        mut(o.posiciones[PID])
        h.chk(f"alterar_{nombre}_se_detecta_O13", red(o, b)["codigo"] == "G-06" and o.posicion_transicion(PID, "EN_REVISION", "H", T1)["codigo"] == "O-13"
              and o.integridad() == ["POS:" + PID])
    o, b = abierta()
    o.posicion_transicion(PID, "REDUCIENDO", "OPERADOR", T1, motivo="reducir", cantidad=40.0)
    o.posiciones[PID]["reduccion"]["objetivo_restante"] = 0.0
    h.chk("alterar_la_reduccion_en_curso_se_detecta", o.integridad() == ["POS:" + PID] and reducir(o, PID, b, T1)["ok"] is False)

    # ------------------------------------------------------------ posición corta
    corto = {"condiciones": [{"id": "STOP-1", "tipo": "STOP", "metrica": "precio", "operador": ">=", "umbral": 1.15, "unidad": "USD"},
                             {"id": "OBJ-1", "tipo": "OBJETIVO", "metrica": "precio", "operador": "<=", "umbral": 1.00, "unidad": "USD"},
                             {"id": "INV-1", "tipo": "INVALIDEZ", "metrica": "precio_cierre", "operador": ">", "umbral": 1.15, "unidad": "USD"}], "fecha": "2026-12-05"}
    o, b = abierta(salida=corto)
    r = red(o, b, 25.0)
    st = b.consultar("ORD-POS-EXP-0001-R1-S-1")
    h.chk("corto_reduce_comprando", r["ok"] and neto(b) == -75.0 and st["lado"] == "COMPRA" and st["cantidad"] == 75.0 and conciliar(o, b, T1)["ok"], r)
    b.mover_precio("EURUSD", 1.20, T1)
    h.chk("corto_el_stop_no_da_la_vuelta", neto(b) == 0.0)

    # ------------------------------------------------------------ revisión independiente (regresiones)
    from ejecucion_g import declarar_manual
    from pruebas_manual import a_mano, cambia, sin, reg as reg_manual
    # G1: retomar una reducción con el estado alterado no envía nada
    o, b = abierta()
    b.rechaza_mercado = True
    red(o, b)
    b.rechaza_mercado = False
    o.posiciones[PID]["reduccion"]["objetivo_restante"] = 0.0
    antes = copy.deepcopy(b.ordenes)
    r = vigilar(o, b, datos(1.10), T1)
    h.chk("G1_H_no_retoma_una_reduccion_alterada_H13", [a["regla"] for a in r["acciones"]] == ["H-13"] and b.ordenes == antes and neto(b) == 100.0, r)
    h.chk("G1_reducir_tampoco", reducir(o, PID, b, T1)["codigo"] == "G-06" and b.ordenes == antes)
    h.chk("G1_cerrar_tampoco", cerrar(o, PID, b, T1, actor="OPERADOR", motivo="x")["codigo"] == "G-06" and b.ordenes == antes)
    # G2: las condiciones de salida, el sentido y el instrumento de la posición están en la cadena
    for nombre, mut in (("fraccion", lambda p: p["condiciones_salida"]["condiciones"][2].update(fraccion=0.95, umbral=1.101)),
                        ("direccion", lambda p: p.__setitem__("direccion", "CORTO")),
                        ("instrumento", lambda p: p.__setitem__("instrumento", "GBPUSD"))):
        o, b = abierta(salida=SAL_P)
        mut(o.posiciones[PID])
        antes = copy.deepcopy(b.ordenes)
        r = vigilar(o, b, datos(1.125), T1)
        h.chk(f"G2_alterar_{nombre}_se_detecta_y_no_vende", o.integridad() == ["POS:" + PID] and b.ordenes == antes and neto(b) == 100.0
              and any(a["regla"] == "H-13" for a in r["acciones"]), r)
    # M1: cierre manual (CT-G-14) a media reducción
    o, b = abierta()
    b.rechaza_mercado = True
    red(o, b)
    b.rechaza_mercado = False
    b.fraccion_mercado = 0.5
    b.rechaza_mercado = False
    o2, b2 = abierta(b=vigilado(fraccion_mercado=0.5))
    red(o2, b2)   # queda a medias: 62,5 en el intermediario
    b2.fraccion_mercado = 1.0
    a_mano(b2, "EURUSD", "VENTA", 62.5, "MAN-CIERRE-1")
    cierre = reg_manual(event_id="EV-MAN-0002", vinculo={"tipo": "POSICION", "id": PID}, lado="VENTA", ref_intermediario="MAN-CIERRE-1", cantidad=62.5)
    cierre = sin(cierre, "proteccion_ref")
    r = declarar_manual(o2, cierre, b2, T1)
    h.chk("M1_cierre_manual_a_media_reduccion", r["ok"] and o2.posiciones[PID]["estado"] == "CERRADA" and conciliar(o2, b2, T1)["ok"]
          and o2.posiciones[PID]["reducciones"][-1]["interrumpida"] == "cierre manual", r)
    o2, b2 = abierta(b=vigilado(fraccion_mercado=0.5))
    red(o2, b2)
    h.chk("M1_cierre_manual_de_mas_RM06", "RM-06" in o2.registrar_manual(cambia(cierre, cantidad=10.0), T1).get("reglas", []))
    # M9: una declaración manual rechazada no deja la posición sin stop
    o2, b2 = abierta()
    red(o2, b2)                     # quedan 60 con el stop redimensionado
    a_mano(b2, "EURUSD", "VENTA", 30.0, "MAN-CIERRE-1")
    r = declarar_manual(o2, cambia(cierre, cantidad=30.0), b2, T1)
    # desde T-47 el Orquestador la rechaza (RM-06) antes de que G consulte o toque el intermediario
    h.chk("M9_declaracion_rechazada_no_quita_el_stop", r["codigo"] == "O-01" and "RM-06" in r.get("reglas", []) and b2.consultar("ORD-POS-EXP-0001-R1-S-1")["estado"] == "ACEPTADA", r)
    # M2: cerrar del todo desde REDUCIENDO sin falsos avisos y con el cierre a medias explicado
    o2, b2 = abierta(b=vigilado(fraccion_mercado=0.5))
    red(o2, b2)
    n_avisos = len(o2.avisos)
    b2.fraccion_mercado = 0.01
    r = cerrar(o2, PID, b2, T1, actor="OPERADOR", motivo="cerrar del todo")
    h.chk("M2_sin_aviso_DIFERENCIA_AL_CERRAR", not any("DIFERENCIA_AL_CERRAR" in str(a) for a in o2.avisos[n_avisos:]), o2.avisos[n_avisos:])
    c = conciliar(o2, b2, T1)
    h.chk("M2_cierre_a_medias_explicado", r["codigo"] == "G-09" and c["ok"] and any(x["tipo"] == "CIERRE_EN_CURSO" for x in c["explicadas"]), (r, c))
    # M3: una toma parcial que ya no cabe no bloquea el objetivo total
    o2, b2 = abierta(salida=SAL_P)
    red(o2, b2, 60.0)                # quedan 40 y la toma parcial (50) ya no cabe
    antes = copy.deepcopy(b2.ordenes)
    r = vigilar(o2, b2, datos(1.125), T1)
    h.chk("M3_toma_parcial_que_no_cabe_se_informa_y_no_actua", r["acciones"] == [] and b2.ordenes == antes
          and any(x["regla"] == "H-12" and x["condicion"] == "OBJ-P" for x in r["no_evaluadas"]), r)
    r = vigilar(o2, b2, datos(1.16, T2), T2)
    h.chk("M3_y_el_objetivo_total_sigue_vivo", o2.posiciones[PID]["estado"] == "CERRADA" and neto(b2) == 0.0, r)
    # M4: una reducción desde EN_REVISION vuelve a EN_REVISION
    o2, b2 = abierta()
    o2.posicion_transicion(PID, "EN_REVISION", "H", T1)
    r = red(o2, b2)
    h.chk("M4_reducir_no_confirma_la_tesis", r["ok"] and o2.posiciones[PID]["estado"] == "EN_REVISION" and o2.posiciones[PID]["cantidad"] == 60.0, r)
    o2, b2 = abierta()
    o2.posicion_transicion(PID, "EN_REVISION", "H", T1)
    o2.posicion_transicion(PID, "REDUCIENDO", "OPERADOR", T1, motivo="x", cantidad=40.0)
    h.rechaza("M4_no_vuelve_a_ABIERTA_O04", o2, lambda: o2.posicion_transicion(PID, "ABIERTA", "G", T1, restante=60.0, orden={"orden_id": "ORD-R-Z", "conciliada": True},
                                                                                  protecciones=["ORD-N"]), "O-04")
    # M5: cantidad por debajo de la tolerancia
    o2, b2 = abierta()
    antes = copy.deepcopy(b2.ordenes)
    h.chk("M5_cantidad_minima_rechazada", red(o2, b2, 5e-7)["codigo"] == "G-06" and b2.ordenes == antes and o2.posiciones[PID]["estado"] == "ABIERTA")
    # M6: una venta ajena durante la reducción no se toma por parte de ella
    o2, b2 = abierta()
    b2.rechaza_mercado = True
    red(o2, b2)
    b2.rechaza_mercado = False
    a_mano(b2, "EURUSD", "VENTA", 30.0, "AJENA-1")
    c = conciliar(o2, b2, T1)
    h.chk("M6_venta_ajena_es_discrepancia", not c["ok"] and any(x["tipo"] == "CANTIDAD" for x in c["diferencias"]), c)
    antes = copy.deepcopy(b2.ordenes)
    r = reducir(o2, PID, b2, T1)
    h.chk("M6_G_no_vende_a_ciegas", r["codigo"] == "G-12" and b2.ordenes == antes and neto(b2) == 70.0
          and any("DIFERENCIA_AL_REDUCIR" in str(a) for a in o2.avisos), r)
    # M7: el resto de una venta parcial no queda vivo
    class ParcialQueSigue(BrokerSimulado):
        """Como un intermediario real: el resto de una orden a mercado parcial sigue vivo y se ejecuta después."""
        def enviar(self, x):
            r = super().enviar(x)
            if x.get("tipo") == "MERCADO" and r["estado"] == "PARCIAL":
                self.ordenes[x["orden_id"]]["estado"] = "PARCIAL"
            return r
        def ejecutar_restos(self):
            for k, r in self.ordenes.items():
                if r["estado"] == "PARCIAL" and r["orden"]["tipo"] == "MERCADO":
                    q = min(r["orden"]["cantidad"] - r["ejecutada"], max(self._reducible(r["orden"]), 0.0) if r["orden"].get("solo_reduccion") else 1e9)
                    if q > 1e-6:
                        self._fill(r["orden"], q, self.precios["EURUSD"])
                        r["ejecutada"] += q
                    r["estado"] = "EJECUTADA"
    o2, b2 = abierta(b=ParcialQueSigue(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0}, fraccion_mercado=0.5))
    red(o2, b2)
    b2.ejecutar_restos()
    h.chk("M7_los_restos_parciales_se_cancelan", neto(b2) >= 60.0 - 1e-6 and all(r["estado"] != "PARCIAL" or r["orden"]["tipo"] != "MERCADO" for r in b2.ordenes.values()),
          neto(b2))
    o2, b2 = abierta()
    b2.enviar({"orden_id": "ORD-POS-EXP-0001-C-1", "instrumento": "EURUSD", "activo_base": "EUR", "tipo": "LIMITE", "lado": "VENTA", "cantidad": 10.0, "precio": 9.0})
    c = conciliar(o2, b2, T1)
    h.chk("M7_orden_de_G_viva_es_discrepancia", not c["ok"] and any(x["tipo"] == "ORDEN_VIVA" for x in c["diferencias"]), c)
    # M8: el cierre a mercado es de solo reducción
    class SaltaAlCerrar(Vigilado):
        def enviar(self, x):
            if x.get("tipo") == "MERCADO" and "-C-" in x["orden_id"]:
                self.mover_precio("EURUSD", 1.04)
            return super().enviar(x)
    o2, b2 = abierta(b=SaltaAlCerrar(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0}, fraccion_mercado=0.5))
    red(o2, b2)
    b2.fraccion_mercado = 1.0
    r = cerrar(o2, PID, b2, T1, actor="OPERADOR", motivo="cerrar")
    h.chk("M8_el_cierre_nunca_abre_la_contraria", r["ok"] and neto(b2) == 0.0 and not [f for f in b2.fallos if "contraria" in f]
          and o2.posiciones[PID]["estado"] == "CERRADA", (r, b2.fallos))
    # m1: a media reducción H sigue vigilando el cierre
    class RechazaReducir(BrokerSimulado):
        def enviar(self, x):
            if x.get("tipo") == "MERCADO" and "-R" in x["orden_id"]:
                self.ordenes[x["orden_id"]] = {"orden": dict(x), "estado": "RECHAZADA", "ejecutada": 0.0, "precio_medio": None}
                return self._res(self.ordenes[x["orden_id"]])
            return super().enviar(x)
    o2, b2 = abierta(b=RechazaReducir(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0}))
    red(o2, b2)
    b2.precios["EURUSD"] = 1.04      # el intermediario no dispara el stop
    r = vigilar(o2, b2, datos(1.04), T1)   # el G-12 avisó y degradó la cartera: H prepara el cierre para el operador
    h.chk("m1_reduciendo_H_sigue_vigilando_el_stop", [a["regla"] for a in r["acciones"]] == ["H-08", "H-10"]
          and any("CIERRE PREPARADO: STOP-1" in x["texto"] for x in o2.posiciones[PID]["propuestas"]), r)
    r = cerrar(o2, PID, b2, T1, actor="OPERADOR", motivo="confirmo el cierre preparado")
    h.chk("m1_el_operador_cierra_desde_reduciendo", r["ok"] and o2.posiciones[PID]["estado"] == "CERRADA" and neto(b2) == 0.0
          and conciliar(o2, b2, T1)["ok"], r)
    # m2: retomar con una cantidad que no es número
    o2, b2 = abierta()
    o2.posicion_transicion(PID, "REDUCIENDO", "OPERADOR", T1, motivo="x", cantidad=40.0)
    h.chk("m2_retomar_con_basura_G06", reducir(o2, PID, b2, T1, cantidad="40")["codigo"] == "G-06")
    # m3: muchas parciales seguidas no agotan los identificadores
    o2, b2 = abierta(b=broker(fraccion_mercado=0.5))
    for _ in range(6):
        r = reducir(o2, PID, b2, T1) if o2.posiciones[PID]["estado"] == "REDUCIENDO" else red(o2, b2)
    h.chk("m3_parciales_repetidas_sin_agotar_ids", r["codigo"] in ("OK", "G-12") and r["codigo"] != "G-08" and conciliar(o2, b2, T1)["ok"], r)

    # ------------------------------------------------------------ intermediario simulado: solo reducción
    b = broker()
    b.pos["EURUSD"] = {"cantidad": 10.0, "activo_base": "EUR"}
    r = b.enviar({"orden_id": "X-1", "instrumento": "EURUSD", "activo_base": "EUR", "tipo": "MERCADO", "lado": "VENTA", "cantidad": 25.0, "solo_reduccion": True})
    h.chk("mercado_solo_reduccion_no_abre_la_contraria", r["cantidad_ejecutada"] == 10.0 and neto(b) == 0.0 and r["estado"] == "PARCIAL", r)
    r = b.enviar({"orden_id": "X-2", "instrumento": "EURUSD", "activo_base": "EUR", "tipo": "MERCADO", "lado": "VENTA", "cantidad": 5.0, "solo_reduccion": True})
    h.chk("mercado_solo_reduccion_sin_posicion_no_ejecuta", r["cantidad_ejecutada"] == 0.0 and neto(b) == 0.0, r)
    r = b.enviar({"orden_id": "X-3", "instrumento": "EURUSD", "activo_base": "EUR", "tipo": "STOP", "lado": "VENTA", "cantidad": 5.0, "precio": 1.0,
                  "solo_reduccion": True})
    h.chk("stop_solo_reduccion_sin_posicion_rechazado", r["estado"] == "RECHAZADA", r)
    r = b.enviar({"orden_id": "X-4", "instrumento": "EURUSD", "activo_base": "EUR", "tipo": "LIMITE", "lado": "VENTA", "cantidad": 5.0, "precio": 1.0,
                  "solo_reduccion": True})
    h.chk("limite_solo_reduccion_no_se_admite", r["estado"] == "RECHAZADA", r)

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO REDUCCION:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
