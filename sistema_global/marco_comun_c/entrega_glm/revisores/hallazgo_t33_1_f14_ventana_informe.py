"""Hallazgo 1 (T-33): la ventana entre el informe de F y la autorización no guarda el importe del día (F-14) frente a las LIBRES.

T-22 cierra esa ventana para las autorizaciones: si tras emitirse el informe se autorizó OTRO expediente,
`autorizar` rechaza con O-10 («F no lo contó; pide otro informe», el guardia `posterior` de
`_comprobar_autorizacion`). T-33 añade a `importe_dia_eur` las LIBRES declaradas, pero no extiende ese
guardia: una LIBRE registrada después del informe y antes de autorizar no entra en el contexto
recalculado (se filtra por `registrado_en <= emitido_en`), y la recomprobación del envío
(`controles_de_contexto`) solo lleva F-16..F-23, sin los topes de cantidad F-13/F-14/F-15. Resultado:
el tope del día de la cuenta (F-14) se supera de punta a punta sin ningún veto ni aviso, justo lo que
T-33 venía a impedir. (Con el mismo instrumento lo para el O-06 de `_ejecutar`; con otro instrumento,
nada lo para.)

Guion: política con importe_max_dia_eur = 150 EUR. Informe a las 09:00 (importe del día 0) aprueba una
entrada de 110 EUR en EURUSD. A las 09:05 se declara una LIBRE de 65 EUR en GBPUSD (bajo el tope de
cartera de 2.000 EUR: sin O-37). A las 09:10 se autoriza con el informe de las 09:00 y la orden se
envía y ejecuta. El día acaba con 175 EUR comprometidos: F-14 (150 EUR) quedó superado sin que nadie
lo viera. Con otra autorización de expediente en vez de la LIBRE, `autorizar` lo habría rechazado (O-10).

Ejecución: python3 hallazgo_t33_1_f14_ventana_informe.py   (desde la carpeta marcoC)
Imprime FALLA si el defecto existe; OK si está corregido (con el guardia, `autorizar` rechazaría y no
habría ejecución, o la recomprobación del envío recortaría por F-14).
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/
sys.path.insert(0, str(AQUI / "validador"))
sys.path.insert(0, str(AQUI / "pruebas"))

from control_f import POLITICA_DEFECTO
from pruebas_control_f import CART, informe_f, registrar_foto
from pruebas_manual import libre
from pruebas_orquestador import AHORA, autorizar_op, nuevo, hasta
from validar_sobre import _dt

L2 = {"nivel_autonomia": {"TRADING": "L2", "TACTICA": "L2", "LARGO_PLAZO": "L2"}}
POL = {**POLITICA_DEFECTO, "importe_max_dia_eur": 150.0, "importe_max_orden_eur": 150.0}
FOTO = {**CART, "tipos_cambio_eur": {"USD": 1.0, "GBP": 1.2}}


def main():
    o = nuevo({"politica_f": POL, **L2})
    # 1) informe de F a las 09:00 con el día vacío: F-14 tope 150/1,1 = 136,36 >= 100 -> APROBADO (110 EUR)
    hasta(o, "PROPUESTA")
    registrar_foto(o, FOTO)   # la última foto lleva el tipo del GBP (USD 1,0 y GBP 1,2)
    inf = informe_f(o, "EXP-0001", 1, cartera=FOTO, emitido_en=AHORA)
    assert inf["resultado_politica"]["resultado"] == "APROBADO", inf["resultado_politica"]["resultado"]
    assert o.contexto_f("EXP-0001", AHORA)["actividad"]["importe_dia_eur"] == 0.0

    # 2) LIBRE de 65 EUR declarada a las 09:05 (después del informe), bajo el tope de cartera: sin O-37
    #    GBPUSD 50 × 1,30 con USD a 1,0 EUR (GBPUSD cotiza en USD) -> 65,0 EUR
    r = o.registrar_manual(libre(instrumento="GBPUSD", activo_base="GBP", cantidad=50.0, precio=1.30,
                                 event_id="EV-MAN-0100", ref_intermediario="MAN-H1",
                                 emitido_en="2026-11-06T09:05:00+00:00", ejecutado_en="2026-11-06T09:04:00+00:00"),
                           "2026-11-06T09:05:00+00:00")
    assert r["ok"] and r["tope_libres_superado"] is False, r
    assert not [x for x in o.avisos if x["codigo"] == "O-37"], "la LIBRE no debía avisar"

    # 3) autorización a las 09:10 con el informe de las 09:00: hoy el día ya lleva 78 EUR que F no contó
    #    (con otra AUTORIZACIÓN de expediente aquí, el guardia de T-22 lo habría rechazado con O-10)
    ra = autorizar_op(o, "EXP-0001", inf, "2026-11-06T09:10:00+00:00")
    assert o.expedientes["EXP-0001"]["estado"] == "AUTORIZADA" or not ra["ok"], ra
    if not ra["ok"]:
        print("OK  autorizar rechazó el informe que no vio la LIBRE:", ra["motivo"])
        return 0

    # 4) envío y ejecución: la recomprobación del envío (F-16..F-23) tampoco mira F-14
    #    (G refresca el precio del intermediario, como exige F-23, y el envío pasa)
    assert o.registrar_cotizacion({"instrumento": "EURUSD", "valor": 1.10, "fecha_hora": "2026-11-06T09:10:30+00:00"},
                                  "G", "2026-11-06T09:11:00+00:00")["ok"]
    re = o.orden_entrada("EXP-0001", "ORD-1", "ENVIADA", 0.0, "G", "2026-11-06T09:11:00+00:00")
    assert re["ok"], re
    assert o.orden_entrada("EXP-0001", "ORD-1", "EJECUTADA", 100.0, "G", "2026-11-06T09:12:00+00:00")["ok"]
    rj = o.ejecutar("EXP-0001", {"orden_id": "ORD-1", "cantidad": 100.0, "precio": 1.10, "conciliada": True,
                                 "proteccion_orden_ids": ["ORD-1-STOP"]}, "G", "2026-11-06T09:12:00+00:00")
    assert rj["ok"], rj

    # 5) el día acaba con 110 (autorizado) + 65 (LIBRE) = 175 EUR > importe_max_dia_eur (150), sin veto ni aviso
    #    (_actividad sin excluir: el importe de todo lo comprometido en el día de la cuenta)
    dia = o._actividad(None, _dt("2026-11-06T09:13:00+00:00"))["importe_dia_eur"]
    o37 = [x for x in o.avisos if x["codigo"] == "O-37"]
    if not (abs(dia - 175.0) < 1e-9 and dia > POL["importe_max_dia_eur"] and not o37):
        print(f"OK    el día quedó en {dia} EUR con tope {POL['importe_max_dia_eur']} EUR")
        return 0
    print(f"FALLA  F-14 superado sin veto ni aviso: importe del día {dia} EUR > tope {POL['importe_max_dia_eur']} EUR "
          f"(informe de las 09:00, LIBRE de las 09:05, autorización de las 09:10 con ese informe, ejecutada); "
          f"ningún guardia lo impidió")

    # 6) contraste: el mismo hueco con OTRO EXPEDIENTE en vez de la LIBRE sí se cierra con O-10
    o2 = nuevo({"politica_f": POL, **L2})
    hasta(o2, "PROPUESTA")
    inf1 = informe_f(o2, "EXP-0001", 1, emitido_en=AHORA)
    hasta(o2, "PROPUESTA", n=3)   # EXP-0003, otra propuesta de prueba
    ra3 = autorizar_op(o2, "EXP-0003", informe_f(o2, "EXP-0003", 3, emitido_en="2026-11-06T09:05:00+00:00"),
                       "2026-11-06T09:05:00+00:00")
    if ra3["ok"]:
        ra1 = autorizar_op(o2, "EXP-0001", inf1, "2026-11-06T09:10:00+00:00")
        print(("FALLA" if ra1["ok"] else "OK   "), "contraste con otro expediente autorizado a las 09:05:",
              ra1.get("motivo", "autorizado también"))
    else:
        print("OK    contraste no disponible:", ra3["motivo"])
    return 1


if __name__ == "__main__":
    sys.exit(main())
