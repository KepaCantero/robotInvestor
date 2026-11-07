"""Pruebas de T-43 (V0.52): la cantidad de una reducción se ajusta al paso de cantidad del instrumento (el que usó E) y nunca
deja un resto que valga menos que el mínimo de F; la toma parcial automática se redondea hacia abajo y, si no cabe, H no la
intenta en cada pasada: deja una propuesta al operador. Datos SIMULADOS.

Uso: python3 pruebas/pruebas_reduccion_t43.py
"""
import copy
import sys
from datetime import datetime, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from decimal import Decimal  # noqa: E402
import pruebas_orquestador as po  # noqa: E402
from ejecucion_g import BrokerSimulado, conciliar, ejecutar, reducir  # noqa: E402
from vigilancia import vigilar  # noqa: E402
from pruebas_control_f import CART, registrar_foto  # noqa: E402
from pruebas_ejecucion_g import autorizado, broker  # noqa: E402
from pruebas_orquestador import AHORA, INV, OBJ, STOP, Arnes, nuevo  # noqa: E402

PID = "POS-EXP-0001"
T1 = "2026-11-06T09:05:00+00:00"
M = "reducir riesgo antes del dato de empleo"


def t(minutos):
    return (datetime.fromisoformat(AHORA) + timedelta(minutes=minutos)).isoformat()


def salida(fraccion):
    return {"condiciones": [STOP, OBJ, {"id": "OBJ-P", "tipo": "OBJETIVO", "metrica": "precio", "operador": ">=", "umbral": 1.12,
                                        "unidad": "USD", "fraccion": fraccion}, INV], "fecha": "2026-12-05"}


def abierta(fraccion=0.5, cfg=None, paso=1.0, cantidad=100.0):
    """Posición de EURUSD a 1,10 (100 unidades = 110 EUR con el tipo neutro), cartera en L2, con el paso de E indicado."""
    o = nuevo(cfg) if cfg else None
    viejo = po.dim.__defaults__
    po.dim.__defaults__ = viejo[:-1] + (paso,)
    try:
        o, b = autorizado(entrada={**po.ENTRADA, "cantidad": cantidad}, salida=salida(fraccion), o=o)
    finally:
        po.dim.__defaults__ = viejo
    r = ejecutar(o, "EXP-0001", b, AHORA)
    assert r["ok"], r
    return o, b


class ConPaso(BrokerSimulado):
    """Como uno real: una orden a mercado cuya cantidad (como decimal) no es múltiplo exacto del paso se rechaza."""
    def enviar(self, x):
        if getattr(self, "paso", None) and isinstance(x, dict) and x.get("tipo") == "MERCADO" and not self.caido:
            if Decimal(repr(x["cantidad"])) % Decimal(repr(self.paso)) != 0:
                return {"orden_id": x.get("orden_id"), "estado": "RECHAZADA", "cantidad_ejecutada": 0.0, "precio_medio": None}
        return super().enviar(x)


def con_paso(b, paso):
    nb = ConPaso.__new__(ConPaso)
    nb.__dict__.update(b.__dict__)
    nb.paso = paso
    return nb


def foto(o):
    return (copy.deepcopy(o.posiciones), copy.deepcopy(o.expedientes), len(o.avisos))


def ventas(b):
    return [k for k, x in b.ordenes.items() if "-R" in k and x["ejecutada"] > 0]


def main():
    h = Arnes()
    # ------------------------------------------------------------------------------------------- lo que pide el operador
    o, b = abierta()
    v = o.cantidad_reduccion(PID, T1, cantidad=40.5)
    h.chk("operador_cantidad_que_no_es_multiplo_del_paso_O06", not v["ok"] and v["codigo"] == "O-06" and "por debajo es 40" in v["motivo"], v)
    antes = foto(o)
    r = reducir(o, PID, b, T1, cantidad=40.5, actor="OPERADOR", motivo=M)
    h.chk("y_G_no_reduce_ni_envia_nada", r["codigo"] == "G-06" and "múltiplo" in r["motivo"] and foto(o)[:2] == antes[:2] and not ventas(b), r)
    v = o.cantidad_reduccion(PID, T1, cantidad=40.0)
    h.chk("cantidad_reduccion_dice_la_cantidad_y_lo_que_queda", v["ok"] and v["cantidad"] == 40.0 and v["restante"] == 60.0, v)
    h.chk("cantidad_reduccion_no_cambia_nada", foto(o)[:2] == antes[:2])
    r = reducir(o, PID, b, T1, cantidad=40.0, actor="OPERADOR", motivo=M)
    h.chk("operador_multiplo_del_paso_reduce", r["ok"] and o.posiciones[PID]["cantidad"] == 60.0 and abs(sum(x["cantidad"] for x in b.posiciones()) - 60.0) < 1e-9, r)
    h.chk("y_concilia_e_integra", conciliar(o, b, T1)["ok"] and o.integridad() == [])

    o, b = abierta()
    antes = foto(o)
    r = reducir(o, PID, b, T1, cantidad=95.0, actor="OPERADOR", motivo=M)   # quedan 5 x 1,10 = 5,50 EUR < 10 EUR (mínimo de F de las pruebas)
    h.chk("resto_por_debajo_del_minimo_de_F_O06", r["codigo"] == "G-06" and "ciérrela entera" in r["motivo"] and foto(o)[:2] == antes[:2] and not ventas(b), r)
    h.chk("el_resto_justo_en_el_minimo_vale", o.cantidad_reduccion(PID, T1, cantidad=90.0)["ok"])   # 10 x 1,10 = 11 EUR
    o2, b2 = abierta(cfg={"politica_f": {**o.cfg["politica_f"], "valor_min_eur": 11.0}})
    h.chk("el_resto_igual_al_minimo_vale", o2.cantidad_reduccion(PID, T1, cantidad=90.0)["ok"])
    h.chk("y_un_centimo_por_debajo_no", not o2.cantidad_reduccion(PID, T1, cantidad=91.0)["ok"])
    h.chk("toda_la_posicion_sigue_siendo_un_cierre_O06", "use el cierre" in o.cantidad_reduccion(PID, T1, cantidad=100.0)["motivo"])
    for nombre, q in (("cero", 0.0), ("negativa", -1.0), ("texto", "40"), ("nan", float("nan")), ("none", None)):
        v = o.cantidad_reduccion(PID, T1, cantidad=q)
        h.chk(f"cantidad_{nombre}_O06", not v["ok"] and v["codigo"] == "O-06", v)

    # ------------------------------------------------------------------------------------------- la valoración del resto
    o, b = abierta()
    v = o.cantidad_reduccion(PID, t(120), cantidad=40.0)
    h.chk("sin_cotizacion_fresca_de_G_O06", not v["ok"] and "cotización reciente" in v["motivo"], v)
    b.mover_precio("EURUSD", 1.10, t(120))
    r = reducir(o, PID, b, t(120), cantidad=40.0, actor="OPERADOR", motivo=M)
    h.chk("G_cotiza_antes_de_reducir_y_entonces_vale", r["ok"] and o.posiciones[PID]["cantidad"] == 60.0, r)
    o, b = abierta()
    o.ultima_foto = None
    h.chk("sin_foto_no_hay_tipo_de_cambio_O06", "tipo de cambio" in o.cantidad_reduccion(PID, T1, cantidad=40.0)["motivo"])
    o, b = abierta()
    o.expedientes["EXP-0001"]["propuesta"]["dimensionado"]["paso"] = None
    h.chk("sin_paso_conocido_O06", "paso de cantidad" in o.cantidad_reduccion(PID, T1, cantidad=40.0)["motivo"])
    o, b = abierta()
    h.chk("con_tipo_neutro_88_deja_13_20_EUR", o.cantidad_reduccion(PID, T1, cantidad=88.0)["ok"])
    registrar_foto(o, {**CART, "fecha_hora": T1, "tipos_cambio_eur": {"USD": 0.75}})
    v = o.cantidad_reduccion(PID, T1, cantidad=88.0)
    h.chk("el_resto_se_valora_en_euros_con_el_tipo_de_la_ultima_foto", not v["ok"] and "9.90 EUR" in v["motivo"], v)
    o, b = abierta(cfg={"politica_f": {**o.cfg["politica_f"], "valor_min_eur": 10.8}})
    h.chk("al_precio_de_entrada_cabria", o.cantidad_reduccion(PID, T1, cantidad=90.0)["ok"])   # 10 x 1,10 = 11 EUR
    b.mover_precio("EURUSD", 1.06, T1)   # el precio baja: lo que queda vale menos
    r = reducir(o, PID, b, T1, cantidad=90.0, actor="OPERADOR", motivo=M)   # 10 x 1,06 = 10,60 EUR
    h.chk("pero_se_valora_al_precio_de_ahora", r["codigo"] == "G-06" and "10.60 EUR" in r["motivo"], r)

    # ------------------------------------------------------------------------------------------- la toma parcial automática (H en L2)
    o, b = abierta(0.333)
    b.mover_precio("EURUSD", 1.125, T1)
    r = vigilar(o, b, {"EURUSD": {"precio": 1.125, "hora": T1}}, T1)
    p = o.posiciones[PID]
    h.chk("la_fraccion_se_redondea_hacia_abajo_al_paso", any(a["regla"] == "H-12" and a["ok"] for a in r["acciones"]) and p["cantidad"] == 67.0
          and p["reducciones"][-1]["cantidad"] == 33.0 and abs(sum(x["cantidad"] for x in b.posiciones()) - 67.0) < 1e-9, r["acciones"])
    h.chk("y_el_stop_cubre_lo_que_queda", b.consultar(p["protecciones"][0])["cantidad"] == 67.0 and conciliar(o, b, T1)["ok"] and o.integridad() == [])
    v = o.cantidad_reduccion(PID, T1, condicion_id="OBJ-1")
    h.chk("una_condicion_sin_fraccion_no_es_toma_parcial", not v["ok"] and v["codigo"] == "O-06", v)

    for nombre, fr, frase in (("no_llega_a_un_paso", 0.005, "no llega a un paso"), ("deja_un_resto_minimo", 0.95, "ciérrela entera")):
        o, b = abierta(fr)
        b.mover_precio("EURUSD", 1.125, T1)
        r = vigilar(o, b, {"EURUSD": {"precio": 1.125, "hora": T1}}, T1)
        p = o.posiciones[PID]
        prop = [x for x in p["propuestas"] if x["texto"].startswith("REDUCCIÓN NO VIABLE")]
        h.chk(f"toma_parcial_que_{nombre}_no_vende_y_lo_propone", p["cantidad"] == 100.0 and not ventas(b) and len(prop) == 1 and frase in prop[0]["texto"]
              and any(x.get("regla") == "H-12" and frase in x.get("motivo", "") for x in r["no_evaluadas"]), (r, prop))
        vigilar(o, b, {"EURUSD": {"precio": 1.126, "hora": t(6)}}, t(6))
        h.chk(f"toma_parcial_que_{nombre}_no_repite_la_propuesta", len([x for x in o.posiciones[PID]["propuestas"] if x["texto"].startswith("REDUCCIÓN NO VIABLE")]) == 1)
    o, b = abierta(0.95)
    b.mover_precio("EURUSD", 1.145, T1)   # se cumplen a la vez la toma parcial que no cabe y el objetivo total
    r = vigilar(o, b, {"EURUSD": {"precio": 1.145, "hora": T1}}, T1)
    h.chk("si_la_toma_parcial_no_cabe_las_demas_condiciones_siguen", o.posiciones[PID]["estado"] == "CERRADA"
          and any(a["regla"] == "H-02" and a["ok"] for a in r["acciones"]), r["acciones"])
    o, b = abierta(0.333)
    b.mover_precio("EURUSD", 1.125, T1)
    r = o.posicion_transicion(PID, "REDUCIENDO", "G", T1, condicion={"id": "OBJ-P", "valor_observado": 1.125}, cantidad=33.3)
    h.chk("automatica_con_la_cantidad_sin_redondear_O06", not r["ok"] and r["codigo"] == "O-06" and "(33" in r["motivo"], r)

    # ------------------------------------------------------------------------------------------- regresiones de la revisión de V0.52
    o, b = abierta(0.95)
    for i, precio in enumerate((1.125, 1.127, 1.129, 1.13)):
        b.mover_precio("EURUSD", precio, t(5 + 5 * i))
        vigilar(o, b, {"EURUSD": {"precio": precio, "hora": t(5 + 5 * i)}}, t(5 + 5 * i))
    h.chk("r01_la_propuesta_no_viable_no_se_repite_aunque_cambie_el_precio",
          len([x for x in o.posiciones[PID]["propuestas"] if x["texto"].startswith("REDUCCIÓN NO VIABLE")]) == 1)
    o, b = abierta(paso=1e-6, cantidad=5000.0)
    h.chk("r02_tolerancia_relativa_al_paso_no_a_la_cantidad", not o.cantidad_reduccion(PID, T1, cantidad=2000.0000009)["ok"])
    o, b = abierta()
    v = o.cantidad_reduccion(PID, T1, cantidad=39.99999999999)
    h.chk("r02_la_cantidad_del_operador_se_ajusta_a_la_rejilla", v["ok"] and v["cantidad"] == 40.0, v)
    o, b = abierta(0.3, paso=0.1, cantidad=98.0)
    v = o.cantidad_reduccion(PID, T1, condicion_id="OBJ-P")
    h.chk("r03_la_automatica_sale_en_la_rejilla_decimal", v["ok"] and v["cantidad"] == 29.4, v)
    b = con_paso(b, 0.1)
    b.mover_precio("EURUSD", 1.125, T1)
    r = vigilar(o, b, {"EURUSD": {"precio": 1.125, "hora": T1}}, T1)
    h.chk("r03_y_un_intermediario_que_exige_el_paso_la_acepta", o.posiciones[PID]["estado"] == "ABIERTA" and o.posiciones[PID]["cantidad"] == 68.6, r["acciones"])
    o, b = abierta(paso=0.1, cantidad=98.0)
    b = con_paso(b, 0.1)
    r = reducir(o, PID, b, T1, cantidad=29.4, actor="OPERADOR", motivo=M)
    h.chk("r04_G_envia_la_cantidad_validada", r["ok"] and o.posiciones[PID]["cantidad"] == 68.6, r)
    o, b = abierta()
    b.mover_precio("EURUSD", 1.10, t(20))
    from ejecucion_g import cotizar
    cotizar(o, b, "EURUSD", t(20))
    h.chk("r05_la_cotizacion_vale_15_min_como_en_F23", o.cantidad_reduccion(PID, t(35), cantidad=40.0)["ok"]
          and "cotización reciente" in o.cantidad_reduccion(PID, t(36), cantidad=40.0)["motivo"])
    for nombre, x in (("entero", 5), ("none", None), ("lista", [T1]), ("sin_zona", "2026-11-06T09:05:00")):
        v = o.cantidad_reduccion(PID, x, cantidad=40.0)
        h.chk(f"r06_instante_{nombre}_O01_sin_lanzar", v["codigo"] == "O-01", v)
    o, b = abierta(0.95, cfg={"nivel_autonomia": {"TRADING": "L1", "TACTICA": "L1", "LARGO_PLAZO": "L1"}})
    b.mover_precio("EURUSD", 1.125, T1)
    vigilar(o, b, {"EURUSD": {"precio": 1.125, "hora": T1}}, T1)
    tx = [x["texto"] for x in o.posiciones[PID]["propuestas"]]
    h.chk("r09_en_L1_una_toma_parcial_que_no_cabe_no_se_prepara_se_avisa", any(x.startswith("REDUCCIÓN NO VIABLE") for x in tx)
          and not any(x.startswith("REDUCCIÓN PREPARADA") for x in tx), tx)
    o, b = abierta(0.333, cfg={"nivel_autonomia": {"TRADING": "L1", "TACTICA": "L1", "LARGO_PLAZO": "L1"}})
    b.mover_precio("EURUSD", 1.125, T1)
    vigilar(o, b, {"EURUSD": {"precio": 1.125, "hora": T1}}, T1)
    h.chk("r09_y_la_preparada_dice_la_cantidad_con_el_paso", any("33.0 con el paso" in x["texto"] for x in o.posiciones[PID]["propuestas"]))
    o, b = abierta()
    b.caido = True
    b.mover_precio("EURUSD", 1.125, t(120))
    vigilar(o, b, {"EURUSD": {"precio": 1.125, "hora": t(120)}}, t(120))
    h.chk("sin_precio_del_intermediario_no_se_deja_propuesta_no_viable", not any(x["texto"].startswith("REDUCCIÓN NO VIABLE") for x in o.posiciones[PID]["propuestas"]))
    o, b = abierta(0.333)
    b.mover_precio("EURUSD", 1.125, T1)
    vigilar(o, b, {"EURUSD": {"precio": 1.125, "hora": T1}}, T1)
    h.chk("una_condicion_ya_consumida_no_es_viable", "ya redujo" in o.cantidad_reduccion(PID, T1, condicion_id="OBJ-P")["motivo"])
    return h


if __name__ == "__main__":
    h = main()
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO REDUCCION T-43:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    sys.exit(0 if h.ok else 1)
