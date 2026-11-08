"""T-44, hallazgo 2 — una parcial deja los stops viejos fuera de la vista de la conciliación y el camino directo
del Orquestador no comprueba que estén muertos: queda un stop vivo que ningún control ve.

La mutación de orquestador.registrar_manual (T-44) saca los stops de p["protecciones"] y los guarda en
p["protecciones_anteriores"], pero ni _stops_de (ejecucion_g) ni conciliar miran protecciones_anteriores: los
controles de stop huérfano de la conciliación (PROTECCION_HUERFANA) solo recorren p["protecciones"] más los
identificadores R{n}-S de las reducciones de G. El diseño asume que «los viejos están cancelados» (punto 4), pero
esa garantía solo la produce el camino por G (_declarar_parcial los cancela antes de registrar y falla con G-10
si no puede). Por el camino directo (o.registrar_manual sin G — camino propio de la batería: «camino bueno por el
Orquestador (sin G)») nadie toca el intermediario: el stop viejo sigue ACEPTADA y, al haber salido de
p["protecciones"], la conciliación deja de verlo (antes de T-44 un estado así era imposible o visible: el cierre
total deja la posición CERRADA con p["protecciones"] intactas y conciliar sí comprueba esos stops).

Consecuencia: el stop viejo (VENTA 100 a 1.05, solo reducción) sigue vivo cubriendo una posición de la que los
libros dicen 60. Si el precio cruza 1.05, se ejecuta sin que nadie lo haya detectado: el intermediario se queda
plano mientras el Orquestador cree tener 60 — discrepancia CANTIDAD (kill-switch) tras una venta fuera de todo
control. Es exactamente el caso que el propio prompt del revisor pregunta: «¿queda algún stop viejo vivo sin que
la conciliación lo vea?».

FALLA si tras la parcial registrada por el Orquestador la conciliación está limpia (ok) con el stop viejo aún
ACEPTADA en el intermediario (y el stop llega a ejecutarse al cruzar su precio).
OK si la conciliación reporta el stop huérfano (PROTECCION_HUERFANA) o G/Orquestador impiden el estado.

Uso: python3 hallazgo_t44_2_stop_viejo_vivo_invisible_a_conciliacion.py
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/
sys.path.insert(0, str(AQUI / "validador"))
sys.path.insert(0, str(AQUI / "pruebas"))

from control_f import POLITICA_DEFECTO  # noqa: E402
from ejecucion_g import conciliar, ejecutar  # noqa: E402
from pruebas_ejecucion_g import autorizado  # noqa: E402
from pruebas_manual import PID, T1, T2, VIA, a_mano, reg  # noqa: E402
from pruebas_orquestador import AHORA, nuevo  # noqa: E402

STOP_VIEJO = "ORD-EXP-0001-S-1"   # el stop de la entrada de G: VENTA 100 a 1.05, solo reducción
VMIN = 20.0   # [solo prueba] como en pruebas_manual_t44.py
L1_MIN = {"nivel_autonomia": {"TACTICA": "L1"}, "politica_f": {**POLITICA_DEFECTO, "valor_min_eur": VMIN}}


def abierta_min():
    o, b = autorizado(o=nuevo(dict(L1_MIN)))
    assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]
    return o, b


def main():
    o, b = abierta_min()
    # el operador vende 40 a mano y coloca el stop nuevo por lo que queda (al precio del stop de la posición)
    a_mano(b, "EURUSD", "VENTA", 40.0, "MAN-RED-1")
    b.enviar({"orden_id": "MAN-STOP-2", "tipo": "STOP", "lado": "VENTA", "instrumento": "EURUSD",
              "activo_base": "EUR", "cantidad": 60.0, "precio": 1.05, "via_acceso": VIA})
    r = reg(event_id="EV-H2-1", vinculo={"tipo": "POSICION", "id": PID}, lado="VENTA", cantidad=40.0,
            precio=1.10, ref_intermediario="MAN-RED-1", proteccion_ref="MAN-STOP-2",
            motivo="vendo una parte a mano (camino directo del Orquestador)")
    res = o.registrar_manual(r, T1)
    print("registro:", res["codigo"], "| libros:", o.posiciones[PID]["cantidad"],
          "| protecciones:", o.posiciones[PID]["protecciones"],
          "| anteriores:", o.posiciones[PID]["protecciones_anteriores"])
    vivo = b.consultar(STOP_VIEJO)["estado"]
    c = conciliar(o, b, T1)
    print("stop viejo en el intermediario:", vivo, "| conciliar:", c["codigo"] if c.get("codigo") else c["diferencias"],
          "| ok:", c["ok"])
    if not (res["ok"] and vivo == "ACEPTADA" and c["ok"]):
        print("OK: el estado no se produce o la conciliación lo ve")
        return 0
    # la munición: el precio cruza el stop viejo y se ejecuta sin que nadie lo hubiera detectado
    b.mover_precio("EURUSD", 1.04, T2)
    c2 = conciliar(o, b, T2)
    print("tras cruzar 1.05: stop viejo:", b.consultar(STOP_VIEJO)["estado"],
          "| intermediario:", {p["instrumento"]: p["cantidad"] for p in b.posiciones()} or "plano",
          "| libros:", o.posiciones[PID]["cantidad"], "| conciliar:", c2["diferencias"])
    print("FALLA: el stop viejo quedó vivo e invisible a la conciliación (PROTECCION_HUERFANA no emitida) y se ejecutó fuera de control")
    return 1


if __name__ == "__main__":
    sys.exit(main())
