"""Pruebas de G (ejecución y conciliación) con un intermediario SIMULADO, y del primer tramo completo
(detección → posición abierta → conciliación). Datos SIMULADOS.

Uso: python3 pruebas/pruebas_ejecucion_g.py
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from ejecucion_g import BrokerSimulado, ConexionPerdida, _aviso, cartera_para_f, conciliar, ejecutar  # noqa: E402
from consola import panel  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_orquestador import autorizar_op, AHORA, ENTRADA, OBJ, STOP, Arnes, hasta, nuevo  # noqa: E402

HORA_DATOS = "2026-11-06T08:50:00+00:00"


def broker(**kw):
    kw.setdefault("tipos_cambio", {"USD": 1.0})   # neutro: las cifras de estas pruebas son las de antes de la conversión (T-10)
    return BrokerSimulado(100000.0, {"EURUSD": kw.pop("precio", 1.10)}, HORA_DATOS, **kw)


class CaeAlEnviarStop(BrokerSimulado):
    def enviar(self, o):
        if isinstance(o, dict) and o.get("tipo") == "STOP" and not self.caido and getattr(self, "armado", True):
            self.caido = True
        return super().enviar(o)


class ExplotaAlConsultar(BrokerSimulado):
    explota = False

    def enviar(self, o):
        r = super().enviar(o)
        if o.get("tipo") == "LIMITE":
            self.explota = True
        return r

    def consultar(self, orden_id):
        if self.explota and orden_id.startswith("ORD-EXP-0001-S"):
            raise TimeoutError("el intermediario tarda demasiado")
        return super().consultar(orden_id)


class StopSeActiva(BrokerSimulado):
    def enviar(self, o):
        if isinstance(o, dict) and o.get("tipo") == "STOP":
            self.ordenes[o["orden_id"]] = {"orden": dict(o), "estado": "EJECUTADA", "ejecutada": o["cantidad"], "precio_medio": o["precio"]}
            self._fill(o, o["cantidad"], o["precio"])
            return self._res(self.ordenes[o["orden_id"]])
        return super().enviar(o)


def autorizado(entrada=None, salida=None, b=None, n=1, o=None):
    o = o or nuevo()
    hasta(o, "PROPUESTA", n=n, entrada=entrada, salida=salida)
    b = b or broker()
    eid = f"EXP-{n:04d}"
    r = autorizar_op(o, eid, informe_f(o, eid, n=n, cartera=cartera_para_f(b)), AHORA)
    assert r["ok"], r
    return o, b


def main():
    h = Arnes()
    # --- camino feliz
    o, b = autorizado()
    r = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("ejecuta_y_abre_posicion", r["ok"] and o.posiciones["POS-EXP-0001"]["estado"] == "ABIERTA" and o.posiciones["POS-EXP-0001"]["cantidad"] == 100.0, r)
    h.chk("el_intermediario_tiene_posicion_y_stop", b.posiciones() == [{"instrumento": "EURUSD", "activo_base": "EUR", "cantidad": 100.0}]
          and b.consultar("ORD-EXP-0001-S-1")["estado"] == "ACEPTADA")
    c = conciliar(o, b, AHORA)
    h.chk("conciliacion_sin_diferencias", c["ok"] and c["diferencias"] == [] and o.avisos == [], c)
    h.chk("reejecutar_es_rechazado", ejecutar(o, "EXP-0001", b, AHORA)["codigo"] == "G-06" and len(b.posiciones()) == 1)
    h.chk("cartera_para_f_sale_del_intermediario", cartera_para_f(b)["posiciones"] == [{"instrumento": "EURUSD", "activo_base": "EUR", "valor_eur": 110.00000000000001}]
          or abs(cartera_para_f(b)["posiciones"][0]["valor_eur"] - 110.0) < 1e-9)
    # --- el segundo expediente ve la posición del primero
    hasta(o, "PROPUESTA", n=3)
    h.rechaza("segunda_con_cartera_vacia_O01", o, lambda: autorizar_op(o, "EXP-0003", informe_f(o, "EXP-0003", n=30), AHORA), "O-01", mutacion_permitida=True)
    h.chk("segunda_con_cartera_del_intermediario_ok", autorizar_op(o, "EXP-0003", informe_f(o, "EXP-0003", n=31, cartera=cartera_para_f(b)), AHORA)["ok"])
    # --- fallos del intermediario
    o, b = autorizado(b=broker(caido=True) if False else None)
    b.caido = True
    r = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("intermediario_caido_G01_sin_efectos", r["codigo"] == "G-01" and not o.posiciones and o.expedientes["EXP-0001"]["estado"] == "AUTORIZADA", r)
    b.caido = False
    h.chk("reintento_tras_caida_ok", ejecutar(o, "EXP-0001", b, AHORA)["ok"] and len(b.posiciones()) == 1)
    o, b = autorizado(b=broker(precio=1.12))
    r = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("precio_fuera_del_limite_queda_viva_G11", r["codigo"] == "G-11" and not b.posiciones() and b.consultar("ORD-EXP-0001-E-1")["estado"] == "ACEPTADA"
          and o.expedientes["EXP-0001"]["orden_entrada"]["estado"] == "ENVIADA", r)
    from ejecucion_g import revisar_entrada
    r = revisar_entrada(o, "EXP-0001", b, "2026-11-08T12:30:00+00:00")
    h.chk("al_vencer_la_ventana_se_cancela_G02", r["codigo"] == "G-02" and b.consultar("ORD-EXP-0001-E-1")["estado"] == "CANCELADA"
          and o.expedientes["EXP-0001"]["orden_entrada"]["estado"] == "CANCELADA", r)
    o, b = autorizado(entrada={**ENTRADA, "cantidad": 1000.0}, b=broker(fraccion_fill=0.4))
    r = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("ejecucion_parcial_protege_lo_ejecutado", r["ok"] and abs(r["cantidad"] - 400.0) < 1e-9 and abs(o.posiciones["POS-EXP-0001"]["cantidad"] - 400.0) < 1e-9
          and abs(b.posiciones()[0]["cantidad"] - 400.0) < 1e-9 and abs(b.consultar("ORD-EXP-0001-S-1")["cantidad_ejecutada"]) == 0.0, r)
    h.chk("parcial_concilia", conciliar(o, b, AHORA)["ok"])
    o, b = autorizado(b=broker(fraccion_fill=0.4))   # 40 uds valen 44 EUR: por debajo del mínimo de F
    r = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("parcial_demasiado_pequena_se_deshace_G05", r["codigo"] == "G-05" and r.get("cerrada") is True and not b.posiciones() and not o.posiciones, r)
    o, b = autorizado(b=broker(rechaza_stops=True))
    r = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("stop_rechazado_se_cierra_G03", r["codigo"] == "G-03" and r.get("cerrada") is True and not b.posiciones() and not o.posiciones, r)
    h.chk("stop_rechazado_deja_aviso_alto", any(a["codigo"] == "O-18" and a["prioridad"] == "ALTA" for a in o.avisos) and panel(o, AHORA)["nivel"] == "ROJO")
    h.chk("stop_rechazado_expediente_sigue_autorizado", o.expedientes["EXP-0001"]["estado"] == "AUTORIZADA")
    o, b = autorizado(b=broker(rechaza_stops=True, rechaza_mercado=True))
    r = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("sin_poder_cerrar_G04_critico", r["codigo"] == "G-04" and r.get("cerrada") is False and len(b.posiciones()) == 1, r)
    c = conciliar(o, b, AHORA)
    h.chk("la_posicion_huerfana_aparece_en_conciliacion", not c["ok"] and c["diferencias"][0]["tipo"] == "POSICION_DESCONOCIDA", c)
    # el Orquestador rechaza lo ejecutado (precio sobre el stop): se cierra
    o, b = autorizado(b=broker(precio=1.05))
    r = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("orquestador_rechaza_lo_ejecutado_G05_y_se_cierra", r["codigo"] in ("G-03", "G-05") and r.get("cerrada") is True and not b.posiciones() and not o.posiciones, r)
    # --- posición corta
    corto_sal = {"condiciones": [{"id": "STOP-1", "tipo": "STOP", "metrica": "precio", "operador": ">=", "umbral": 1.15, "unidad": "USD"},
                                 {"id": "OBJ-1", "tipo": "OBJETIVO", "metrica": "precio", "operador": "<=", "umbral": 1.00, "unidad": "USD"},
                                 {"id": "INV-1", "tipo": "INVALIDEZ", "metrica": "precio_cierre", "operador": ">", "umbral": 1.15, "unidad": "EUR"}], "fecha": "2026-12-05"}
    o, b = autorizado(salida=corto_sal)
    r = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("corto_ejecuta_y_concilia", r["ok"] and b.posiciones()[0]["cantidad"] == -100.0 and conciliar(o, b, AHORA)["ok"], r)
    # --- conciliación
    o, b = autorizado(); ejecutar(o, "EXP-0001", b, AHORA)
    b.pos["EURUSD"]["cantidad"] = 90.0
    c = conciliar(o, b, AHORA)
    h.chk("diferencia_de_cantidad", [d["tipo"] for d in c["diferencias"]] == ["CANTIDAD"], c)
    b.pos["EURUSD"]["cantidad"] = 100.0; b.cancelar("ORD-EXP-0001-S-1")
    c = conciliar(o, b, AHORA)
    h.chk("stop_desaparecido", [d["tipo"] for d in c["diferencias"]] == ["PROTECCION"], c)
    b.pos["GBPUSD"] = {"cantidad": 5.0, "activo_base": "GBP"}; b.precios["GBPUSD"] = 1.3
    c = conciliar(o, b, AHORA)
    h.chk("posicion_desconocida", "POSICION_DESCONOCIDA" in [d["tipo"] for d in c["diferencias"]], c)
    h.chk("las_diferencias_quedan_como_avisos_altos", sum(1 for a in o.avisos if a["codigo"] == "O-18") >= 3 and panel(o, AHORA)["nivel"] == "ROJO")
    b.caido = True
    h.chk("conciliar_sin_conexion_no_da_ok", conciliar(o, b, AHORA)["ok"] is False)
    h.rechaza("reportar_discrepancia_actor_ajeno_O05", o, lambda: o.reportar_discrepancia([{"tipo": "X"}], "BROKER", AHORA), "O-05")
    h.rechaza("reportar_discrepancia_vacia_O01", o, lambda: o.reportar_discrepancia([], "G", AHORA), "O-01")
    # --- fallos tras enviar órdenes (revisión independiente)
    o, b = autorizado(b=CaeAlEnviarStop(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0}))
    r = ejecutar(o, "EXP-0001", b, AHORA)
    b.caido = False
    h.chk("caida_al_enviar_el_stop_no_dice_que_no_hay_efectos", r["codigo"] == "G-08" and r.get("incierto") is True and r["aviso_registrado"] is True
          and any("ESTADO_INCIERTO" in a["motivo"] for a in o.avisos) and len(b.posiciones()) == 1, r)
    b.armado = False
    r = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("reintento_tras_caida_con_posicion_viva_la_protege", r["ok"] and len(b.posiciones()) == 1 and o.posiciones["POS-EXP-0001"]["estado"] == "ABIERTA"
          and conciliar(o, b, AHORA)["ok"], r)
    o, b = autorizado(b=ExplotaAlConsultar(100000.0, {"EURUSD": 1.10}, HORA_DATOS, tipos_cambio={"USD": 1.0}))
    try:
        r = ejecutar(o, "EXP-0001", b, AHORA)
        h.chk("excepcion_inesperada_tras_enviar_G08_sin_lanzar", r["codigo"] == "G-08" and r["aviso_registrado"], r)
    except Exception as ex:   # noqa: BLE001
        h.chk("excepcion_inesperada_tras_enviar_G08_sin_lanzar", False, type(ex).__name__)
    o, b = autorizado(b=StopSeActiva(100000.0, {"EURUSD": 1.10}, HORA_DATOS))
    r = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("stop_ya_activado_no_abre_posicion_contraria", r["codigo"] == "G-03" and b.posiciones() == [] and r.get("cerrada") is True, (r, b.posiciones()))
    # segunda posición sobre el mismo instrumento: no se envía nada
    o, b = autorizado(); ejecutar(o, "EXP-0001", b, AHORA)
    hasta(o, "PROPUESTA", n=3)
    autorizar_op(o, "EXP-0003", informe_f(o, "EXP-0003", n=40, cartera=cartera_para_f(b)), AHORA)
    antes = dict(b.ordenes)
    r = ejecutar(o, "EXP-0003", b, AHORA)
    h.chk("segunda_posicion_en_el_mismo_instrumento_G06_sin_enviar", r["codigo"] == "G-06" and b.ordenes.keys() == antes.keys(), r)
    # ventana vencida: no se envía nada
    o, b = autorizado()
    r = ejecutar(o, "EXP-0001", b, "2026-11-08T12:30:00+00:00")
    h.chk("ventana_vencida_G06_sin_enviar", r["codigo"] == "G-06" and b.ordenes == {}, r)
    o, b = autorizado(); o.barrer("2026-11-06T09:30:00+00:00")
    r = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("reloj_atrasado_G06_sin_enviar", r["codigo"] == "G-06" and b.ordenes == {}, r)
    o, b = autorizado(); o.barrer("2026-11-06T09:30:00+00:00")
    h.chk("el_aviso_no_se_pierde_con_el_reloj_por_delante", _aviso(o, [{"tipo": "X", "ref": None, "detalle": "d"}], AHORA) is True and any(a["codigo"] == "O-18" for a in o.avisos))
    # reintento que converge tras G-04
    o, b = autorizado(b=broker(rechaza_stops=True, rechaza_mercado=True))
    r = ejecutar(o, "EXP-0001", b, AHORA)
    b.rechaza_stops = b.rechaza_mercado = False
    r2 = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("reintento_tras_G04_converge", r["codigo"] == "G-04" and r2["ok"] and len(b.posiciones()) == 1 and conciliar(o, b, AHORA)["ok"], (r, r2))
    o, b = autorizado(b=broker(rechaza_stops=True))
    r = ejecutar(o, "EXP-0001", b, AHORA); b.rechaza_stops = False
    r2 = ejecutar(o, "EXP-0001", b, AHORA)
    h.chk("reintento_tras_cierre_de_emergencia_abre_una_posicion_nueva", r["codigo"] == "G-03" and r2["ok"] and len(b.posiciones()) == 1 and b.posiciones()[0]["cantidad"] == 100.0, (r, r2))
    # --- conciliación más estricta
    o, b = autorizado(); ejecutar(o, "EXP-0001", b, AHORA)
    b.pos["EURUSD"]["cantidad"] = -100.0
    h.chk("conciliar_distingue_largo_de_corto", [d["tipo"] for d in conciliar(o, b, AHORA)["diferencias"]] == ["SENTIDO_O_ACTIVO"])
    b.pos["EURUSD"]["cantidad"] = 100.0; b.pos["EURUSD"]["activo_base"] = "GBP"
    h.chk("conciliar_comprueba_el_activo_base", [d["tipo"] for d in conciliar(o, b, AHORA)["diferencias"]] == ["SENTIDO_O_ACTIVO"])
    b.pos["EURUSD"]["activo_base"] = "EUR"
    b.ordenes["ORD-EXP-0001-S-1"]["orden"]["cantidad"] = 5000.0
    h.chk("conciliar_comprueba_la_cantidad_del_stop", [d["tipo"] for d in conciliar(o, b, AHORA)["diferencias"]] == ["PROTECCION"])
    b.ordenes["ORD-EXP-0001-S-1"]["orden"]["cantidad"] = 100.0; b.ordenes["ORD-EXP-0001-S-1"]["orden"]["precio"] = 0.5
    h.chk("conciliar_comprueba_el_precio_del_stop", [d["tipo"] for d in conciliar(o, b, AHORA)["diferencias"]] == ["PROTECCION"])
    o, b = autorizado(); ejecutar(o, "EXP-0001", b, AHORA)
    o.posicion_transicion("POS-EXP-0001", "CERRANDO", "OPERADOR", AHORA, motivo="salida manual")
    o.posicion_transicion("POS-EXP-0001", "CERRADA", "G", AHORA, restante=0, orden={"orden_id": "C1", "conciliada": True})
    c = conciliar(o, b, AHORA)
    h.chk("stop_vivo_de_posicion_cerrada_se_detecta", "PROTECCION_HUERFANA" in [d["tipo"] for d in c["diferencias"]], c)
    # --- robustez
    o = nuevo(); b = broker()
    for nombre, args in (("expediente_inexistente", (o, "EXP-9", b, AHORA)), ("orquestador_none", (None, "EXP-1", b, AHORA)), ("broker_none", (o, "EXP-1", None, AHORA))):
        try:
            r = ejecutar(*args)
            h.chk("ejecutar_no_lanza_" + nombre, r["ok"] is False and r["codigo"].startswith("G-"), r)
        except Exception as ex:   # noqa: BLE001
            h.chk("ejecutar_no_lanza_" + nombre, False, type(ex).__name__)
    for nombre, orden in (("sin_id", {"tipo": "LIMITE"}), ("cantidad_negativa", {"orden_id": "A", "tipo": "MERCADO", "lado": "COMPRA", "instrumento": "EURUSD", "activo_base": "EUR", "cantidad": -1.0}),
                          ("cantidad_nan", {"orden_id": "A", "tipo": "MERCADO", "lado": "COMPRA", "instrumento": "EURUSD", "activo_base": "EUR", "cantidad": float("nan")}), ("no_objeto", [])):
        h.chk("broker_rechaza_" + nombre, broker().enviar(orden)["estado"] == "RECHAZADA")
    b = broker()
    ok1 = b.enviar({"orden_id": "A1", "tipo": "MERCADO", "lado": "COMPRA", "instrumento": "EURUSD", "activo_base": "EUR", "cantidad": 10.0})
    ok2 = b.enviar({"orden_id": "A1", "tipo": "MERCADO", "lado": "COMPRA", "instrumento": "EURUSD", "activo_base": "EUR", "cantidad": 10.0})
    dist = b.enviar({"orden_id": "A1", "tipo": "MERCADO", "lado": "COMPRA", "instrumento": "EURUSD", "activo_base": "EUR", "cantidad": 99.0})
    h.chk("broker_idempotente_por_orden_id", ok1 == ok2 and b.posiciones()[0]["cantidad"] == 10.0 and dist["estado"] == "RECHAZADA")
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO G:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
