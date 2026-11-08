"""T-44, hallazgo 1 — _declarar_parcial acepta con tolerancia RELATIVA lo que toda la cadena restante mide ABSOLUTO.

En ejecucion_g._declarar_parcial (T-44) tanto el contraste del relleno con lo declarado como el del neto del
intermediario con lo que queda usan _cuadra (tolerancia relativa: 1e-6 * max(1, |y|)). Pero todo lo que viene
después mide en absoluto: TOL_Q = 1e-6 del Orquestador, la conciliación (CANTIDAD con TOL=1e-6 y
tolerancia_conciliacion_rel=0.0 por defecto) y su control de protección (1e-6 absoluto). El cierre total, además,
sí rechaza el desfase equivalente (su control del neto es absoluto, G-10: «el intermediario aún tiene cantidad»).

Consecuencia: el operador declara haber vendido 40.00003 cuando el intermediario ejecutó 40.0 (diferencia 3e-5,
dentro de 1e-6*max(1,40)=4e-5 y de 1e-6*max(1,60)=6e-5). G la registra con OK (libros: 59.99997) y la
conciliación inmediatamente siguiente — sin ningún otro evento — reporta CANTIDAD («Orquestador 59.99997,
intermediario 60.0»), discrepancia de la clase kill-switch (TIPOS_KILL). El diseño promete lo contrario para una
parcial que G da por buena: «tras una parcial correcta la cantidad esperada es la nueva, el stop vivo nuevo es
exacto y los viejos están cancelados» (punto 4), y asigna a G-10 justo este caso: «lo declarado no cuadra con el
intermediario». Variante gemela: con el stop colocado por lo que queda REAL (60.0) en vez de por lo declarado,
G también acepta y la conciliación da PROTECCION y CANTIDAD.

FALLA si G registra la parcial (ok) y la conciliación inmediata reporta discrepancia.
OK si G la rechaza (G-10) o la conciliación queda limpia.

Uso: python3 hallazgo_t44_1_conciliacion_tras_parcial_con_desfase.py
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/
sys.path.insert(0, str(AQUI / "validador"))
sys.path.insert(0, str(AQUI / "pruebas"))

from control_f import POLITICA_DEFECTO  # noqa: E402
from ejecucion_g import declarar_manual, conciliar, ejecutar  # noqa: E402
from pruebas_ejecucion_g import autorizado  # noqa: E402
from pruebas_manual import PID, T1, VIA, a_mano, reg  # noqa: E402
from pruebas_orquestador import AHORA, nuevo  # noqa: E402

VMIN = 20.0   # [solo prueba] como en pruebas_manual_t44.py: sin bajar el mínimo no cabe ninguna parcial
L1_MIN = {"nivel_autonomia": {"TACTICA": "L1"}, "politica_f": {**POLITICA_DEFECTO, "valor_min_eur": VMIN}}


def abierta_min():
    o, b = autorizado(o=nuevo(dict(L1_MIN)))
    assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]
    return o, b


def main():
    fallos = []
    # caso 1: lo declarado difiere de lo ejecutado; el stop está por lo declarado
    o, b = abierta_min()
    a_mano(b, "EURUSD", "VENTA", 40.0, "MAN-RED-1")
    b.enviar({"orden_id": "MAN-STOP-2", "tipo": "STOP", "lado": "VENTA", "instrumento": "EURUSD",
              "activo_base": "EUR", "cantidad": 100.0 - 40.00003, "precio": 1.05, "via_acceso": VIA})
    r = reg(event_id="EV-H1-1", vinculo={"tipo": "POSICION", "id": PID}, lado="VENTA", cantidad=40.00003,
            precio=1.10, ref_intermediario="MAN-RED-1", proteccion_ref="MAN-STOP-2",
            motivo="vendo una parte a mano (declaración con desfase)")
    res = declarar_manual(o, r, b, T1)
    c = conciliar(o, b, T1)
    print(f"caso 1: G={res['codigo']} libros={o.posiciones[PID]['cantidad']} conciliar={c['diferencias']}")
    if res["ok"] and not c["ok"]:
        fallos.append("caso 1: G registra (libros 59.99997) y la conciliación da CANTIDAD (intermediario 60.0)")

    # caso 2: el stop está por lo que queda REAL (60.0), no por lo declarado (59.99997)
    o, b = abierta_min()
    a_mano(b, "EURUSD", "VENTA", 40.0, "MAN-RED-1")
    b.enviar({"orden_id": "MAN-STOP-2", "tipo": "STOP", "lado": "VENTA", "instrumento": "EURUSD",
              "activo_base": "EUR", "cantidad": 60.0, "precio": 1.05, "via_acceso": VIA})
    r = reg(event_id="EV-H1-2", vinculo={"tipo": "POSICION", "id": PID}, lado="VENTA", cantidad=40.00003,
            precio=1.10, ref_intermediario="MAN-RED-1", proteccion_ref="MAN-STOP-2",
            motivo="vendo una parte a mano (stop por lo real)")
    res = declarar_manual(o, r, b, T1)
    c = conciliar(o, b, T1)
    print(f"caso 2: G={res['codigo']} libros={o.posiciones[PID]['cantidad']} conciliar={c['diferencias']}")
    if res["ok"] and not c["ok"]:
        fallos.append("caso 2: G registra y la conciliación da PROTECCION y CANTIDAD")

    if fallos:
        for f in fallos:
            print("FALLA:", f)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
