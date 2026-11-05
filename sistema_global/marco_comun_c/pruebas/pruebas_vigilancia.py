"""Pruebas de H (vigilancia de posiciones) y del cierre de posiciones en G, con un intermediario SIMULADO. Datos SIMULADOS.

Uso: python3 pruebas/pruebas_vigilancia.py
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
from ejecucion_g import BrokerSimulado, cartera_para_f, cerrar, conciliar, ejecutar  # noqa: E402
from vigilancia import vigilar  # noqa: E402
from pruebas_ejecucion_g import autorizado, broker  # noqa: E402
from pruebas_orquestador import AHORA, Arnes  # noqa: E402

T1 = "2026-11-06T09:05:00+00:00"   # AHORA + 5 min
PID = "POS-EXP-0001"


def abierta(**kw):
    o, b = autorizado(**kw)
    assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]
    return o, b


def datos(precio, hora=T1):
    return {"EURUSD": {"precio": precio, "hora": hora}}


def main():
    h = Arnes()
    # --- sin novedad
    o, b = abierta()
    r = vigilar(o, b, datos(1.10), T1)
    h.chk("sin_novedad_no_hace_nada", r["acciones"] == [] and r["conciliacion_ok"] and o.posiciones[PID]["estado"] == "ABIERTA", r)
    # --- H-01: el intermediario ejecutó el stop
    o, b = abierta()
    b.mover_precio("EURUSD", 1.04, T1)
    r = vigilar(o, b, datos(1.04), T1)
    h.chk("H01_stop_ejecutado_cierra_la_posicion", [a["regla"] for a in r["acciones"]] == ["H-01"] and r["acciones"][0]["ok"]
          and o.posiciones[PID]["estado"] == "CERRADA" and b.posiciones() == [] and r["conciliacion_ok"], r)
    # --- H-02: objetivo alcanzado
    o, b = abierta()
    r = vigilar(o, b, datos(1.30), T1)
    h.chk("H02_objetivo_cumplido_cierra_a_mercado", [a["regla"] for a in r["acciones"]] == ["H-02"] and r["acciones"][0]["ok"]
          and o.posiciones[PID]["estado"] == "CERRADA" and b.posiciones() == [] and r["conciliacion_ok"], r)
    st = b.consultar("ORD-EXP-0001-S-1")
    h.chk("el_stop_se_retira_al_cerrar", st["estado"] == "CANCELADA", st)
    h.chk("segunda_pasada_no_hace_nada", vigilar(o, b, datos(1.30), T1)["acciones"] == [])
    # --- H-05: el precio cruzó el stop pero el intermediario no lo ejecutó
    o, b = abierta()
    b.precios["EURUSD"] = 1.04     # el intermediario no dispara el stop (fallo)
    r = vigilar(o, b, datos(1.04), T1)
    h.chk("H05_stop_cumplido_sin_ejecutar_cierra_a_mercado", [a["regla"] for a in r["acciones"]] == ["H-05"] and o.posiciones[PID]["estado"] == "CERRADA"
          and b.posiciones() == [], r)
    # --- H-03: dato ausente o viejo
    for nombre, d in (("ausente", {}), ("viejo", datos(1.04, "2026-11-06T08:00:00+00:00")), ("futuro", datos(1.04, "2026-11-06T10:00:00+00:00")),
                      ("basura", {"EURUSD": {"precio": "x", "hora": "ayer"}}), ("no_dict", None), ("negativo", datos(-1.0))):
        o, b = abierta()
        r = vigilar(o, b, d, T1)
        h.chk(f"H03_dato_{nombre}_no_cierra_y_avisa", r["acciones"] and r["acciones"][0]["regla"] == "H-03" and o.posiciones[PID]["estado"] == "ABIERTA"
              and any("DATO_VIEJO" in str(a) for a in o.avisos), r)
    # --- H-04: cierre pendiente y reintento
    o, b = abierta()
    b.rechaza_mercado = True
    r = cerrar(o, PID, b, T1, actor="OPERADOR", motivo="salida manual")
    h.chk("cierre_rechazado_deja_CERRANDO_y_avisa", r["codigo"] == "G-09" and o.posiciones[PID]["estado"] == "CERRANDO" and len(b.posiciones()) == 1
          and r["aviso_registrado"], r)
    b.rechaza_mercado = False
    r = vigilar(o, b, datos(1.10), T1)
    h.chk("H04_reintenta_el_cierre_pendiente", [a["regla"] for a in r["acciones"]] == ["H-04"] and o.posiciones[PID]["estado"] == "CERRADA" and b.posiciones() == [], r)
    # caída antes de enviar
    o, b = abierta()
    b.caido = True
    r = cerrar(o, PID, b, T1, actor="OPERADOR", motivo="salida manual")
    h.chk("sin_conexion_antes_de_enviar_G01_y_sigue_CERRANDO", r["codigo"] == "G-01" and o.posiciones[PID]["estado"] == "CERRANDO", r)
    b.caido = False
    h.chk("reintento_tras_G01_cierra", cerrar(o, PID, b, T1)["ok"] and o.posiciones[PID]["estado"] == "CERRADA")
    # --- cierre manual y validaciones del Orquestador
    o, b = abierta()
    r = cerrar(o, PID, b, T1, actor="OPERADOR")
    h.chk("cierre_manual_sin_motivo_no_envia_nada", r["codigo"] == "G-06" and o.posiciones[PID]["estado"] == "ABIERTA" and len(b.ordenes) == 2, r)
    r = cerrar(o, PID, b, T1, actor="G", condicion={"id": "STOP-1", "valor_observado": 2.0})
    h.chk("cierre_con_condicion_no_cumplida_no_envia_nada", r["codigo"] == "G-06" and o.posiciones[PID]["estado"] == "ABIERTA" and len(b.ordenes) == 2, r)
    r = cerrar(o, "POS-NO-EXISTE", b, T1)
    h.chk("cerrar_posicion_inexistente_G06", r["codigo"] == "G-06")
    r = cerrar(o, PID, b, "2026-11-06T08:00:00+00:00", actor="OPERADOR", motivo="x")
    h.chk("cerrar_con_reloj_atrasado_G06_sin_enviar", r["codigo"] == "G-06" and len(b.ordenes) == 2, r)
    r = cerrar(o, PID, b, T1, actor="OPERADOR", motivo="salida manual")
    h.chk("cierre_manual_con_motivo_OK", r["ok"] and o.posiciones[PID]["estado"] == "CERRADA", r)
    h.chk("cerrar_una_cerrada_G06", cerrar(o, PID, b, T1)["codigo"] == "G-06")
    # --- el stop no se deja retirar
    class NoCancela(BrokerSimulado):
        def cancelar(self, oid):
            return self._res(self.ordenes[oid]) if oid in self.ordenes else None

        def _fill(self, o, q, p):   # el intermediario deja vivo el stop aunque ya no haya posición
            vivos = [r for r in self.ordenes.values() if r["estado"] == "ACEPTADA"]
            super()._fill(o, q, p)
            for r in vivos:
                r["estado"] = "ACEPTADA"
    o, b = abierta(b=NoCancela(100000.0, {"EURUSD": 1.10}, "2026-11-06T08:50:00+00:00", tipos_cambio={"USD": 1.0}))
    r = cerrar(o, PID, b, T1, actor="OPERADOR", motivo="x")
    h.chk("stop_que_no_se_retira_deja_CERRANDO_y_avisa", r["codigo"] == "G-09" and o.posiciones[PID]["estado"] == "CERRANDO" and b.posiciones() == [], r)
    # --- posición desaparecida sin explicación
    o, b = abierta()
    b.pos.clear()
    r = vigilar(o, b, datos(1.10), T1)
    h.chk("posicion_desaparecida_sin_explicacion_no_se_da_por_cerrada", o.posiciones[PID]["estado"] != "CERRADA"
          and any(a["regla"] == "H-07" for a in r["acciones"]), r)
    # --- sin conexión durante la vigilancia: no rompe
    o, b = abierta()
    b.caido = True
    try:
        r = vigilar(o, b, datos(1.30), T1)
        h.chk("vigilar_sin_conexion_no_lanza_ni_da_nada_por_cerrado", o.posiciones[PID]["estado"] != "CERRADA" and not r["conciliacion_ok"], r)
    except Exception as ex:   # noqa: BLE001
        h.chk("vigilar_sin_conexion_no_lanza_ni_da_nada_por_cerrado", False, type(ex).__name__)
    # --- métrica no soportada
    o, b = abierta()
    o.posiciones[PID]["condiciones_salida"]["condiciones"].append({"id": "VOL", "tipo": "OBJETIVO", "metrica": "volatilidad", "operador": ">", "umbral": 1.0})
    r = vigilar(o, b, datos(1.10), T1)
    h.chk("H06_metrica_no_soportada_se_informa", r["no_evaluadas"] and r["no_evaluadas"][0]["regla"] == "H-06", r)
    # --- revisión independiente
    # 1. el stop salta entre la lectura y el cierre: la orden a mercado abre la posición contraria
    class SaltaAlCerrar(BrokerSimulado):
        saltado = False
        def enviar(self, o):
            if o["tipo"] == "MERCADO" and not self.saltado:
                self.saltado = True
                self.mover_precio("EURUSD", 1.04)   # el stop se ejecuta justo antes
            return super().enviar(o)
    o, b = abierta(b=SaltaAlCerrar(100000.0, {"EURUSD": 1.10}, "2026-11-06T08:50:00+00:00"))
    r = cerrar(o, PID, b, T1, actor="OPERADOR", motivo="salida manual")
    h.chk("carrera_stop_vs_cierre_no_deja_posicion_contraria", r["ok"] and b.posiciones() == [] and o.posiciones[PID]["estado"] == "CERRADA"
          and conciliar(o, b, T1)["ok"], (r, b.posiciones()))
    # 2. H-01 con relleno que no cumple la condición (mejor precio, redondeo, ausente)
    for nombre, pm in (("mejor_precio", 1.0501), ("redondeo", 1.0500000000000003), ("sin_precio", None)):
        o, b = abierta()
        b.mover_precio("EURUSD", 1.04, T1)
        b.ordenes["ORD-EXP-0001-S-1"]["precio_medio"] = pm
        r = vigilar(o, b, datos(1.04), T1)
        h.chk(f"H01_relleno_{nombre}_cierra_igual", o.posiciones[PID]["estado"] == "CERRADA" and r["acciones"][0]["ok"], r)
    # 3. cierre parcial a mercado: se completa en la misma llamada o en el reintento
    class PrimeraParcial(BrokerSimulado):
        def enviar(self, o):
            r = super().enviar(o)
            self.fraccion_mercado = 1.0
            return r
    o, b = abierta(b=PrimeraParcial(100000.0, {"EURUSD": 1.10}, "2026-11-06T08:50:00+00:00", fraccion_mercado=0.4))
    b.fraccion_mercado = 0.4
    r = cerrar(o, PID, b, T1, actor="OPERADOR", motivo="salida manual")
    h.chk("cierre_parcial_se_completa", r["ok"] and b.posiciones() == [] and o.posiciones[PID]["estado"] == "CERRADA", (r, b.posiciones()))
    o, b = abierta(b=BrokerSimulado(100000.0, {"EURUSD": 1.10}, "2026-11-06T08:50:00+00:00", fraccion_mercado=0.01, tipos_cambio={"USD": 1.0}))
    r = cerrar(o, PID, b, T1, actor="OPERADOR", motivo="salida manual")
    h.chk("cierre_muy_parcial_G09_y_reintento_continua", r["codigo"] == "G-09" and o.posiciones[PID]["estado"] == "CERRANDO", r)
    b.fraccion_mercado = 1.0
    r = vigilar(o, b, datos(1.10), T1)
    h.chk("reintento_tras_cierre_parcial_termina", o.posiciones[PID]["estado"] == "CERRADA" and b.posiciones() == [], (r, b.posiciones()))
    o, b = abierta()
    b.mover_precio("EURUSD", 1.04, T1)
    b.ordenes["ORD-EXP-0001-S-1"]["estado"] = "PARCIAL"
    b.pos["EURUSD"] = {"cantidad": 30.0, "activo_base": "EUR"}
    r = vigilar(o, b, datos(1.04), T1)
    h.chk("stop_parcial_se_cierra_el_resto", o.posiciones[PID]["estado"] == "CERRADA" and b.posiciones() == [], r)
    # 4. REDUCIENDO
    o, b = abierta()
    o.posicion_transicion(PID, "REDUCIENDO", "OPERADOR", T1, motivo="reducir")
    h.chk("REDUCIENDO_sin_novedad_no_se_cierra", vigilar(o, b, datos(1.30), T1)["acciones"][0]["regla"] == "H-08" and o.posiciones[PID]["estado"] == "REDUCIENDO" and len(b.posiciones()) == 1)
    b.mover_precio("EURUSD", 1.04, T1)
    r = vigilar(o, b, datos(1.04), T1)
    h.chk("REDUCIENDO_con_stop_ejecutado_se_cierra", o.posiciones[PID]["estado"] == "CERRADA" and b.posiciones() == [], r)
    # 5. cantidad distinta: se cierra lo que hay y se avisa
    o, b = abierta()
    b.pos["EURUSD"]["cantidad"] = 40.0
    r = cerrar(o, PID, b, T1, actor="OPERADOR", motivo="x")
    h.chk("cantidad_distinta_se_cierra_lo_que_hay_y_avisa", r["ok"] and b.posiciones() == [] and any("DIFERENCIA_AL_CERRAR" in str(a) for a in o.avisos), r)
    # 6. instante futuro
    o, b = abierta()
    r = vigilar(o, b, datos(1.30), "2027-06-01T00:00:00+00:00")
    h.chk("instante_futuro_H09_no_envenena_el_reloj", r["acciones"][0]["regla"] == "H-09" and o.ultimo_ahora < "2026-12" and o.posiciones[PID]["estado"] == "ABIERTA", (r, o.ultimo_ahora))
    h.chk("instante_ilegible_H09", vigilar(o, b, datos(1.30), "ayer")["acciones"][0]["regla"] == "H-09")
    h.chk("tras_el_instante_futuro_la_vigilancia_sigue", vigilar(o, b, datos(1.30), T1)["acciones"][0]["regla"] == "H-02")
    # --- integridad
    o, b = abierta(); vigilar(o, b, datos(1.30), T1)
    h.chk("integridad_del_historial_tras_cerrar", o.integridad() == [], o.integridad())
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO H:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
