"""Hallazgo 2 (T-33): un producto que subdesborda a 0.0 se valora como 0 EUR y el tope 0.0 no lo prohíbe.

El diseño de la pieza dice que con `libres_tope_dia_eur` en 0.0 «se prohíbe cualquier LIBRE valorada»
(comentario de `_valida_config` y LEEME de la V0.38), y que un producto que no da un número finito no se
puede valorar (importe None -> aviso O-37 y degradación). Por arriba se cumple: 1e308 × 1e308 desborda,
`OverflowError`/infinito -> importe None -> O-37. Por abajo no: 1e-200 × 1e-200 × 1,0 subdesborda a 0.0,
el código lo trata como un importe REAL de 0.0 EUR (`suma 0.0 <= tope 0.0` -> no superado), y la LIBRE se
acepta sin O-37, sin degradación y con `tope_libres_superado: False`. Falla cerrada al revés: un producto
no representable (el valor verdadero es positivo) se toma en el caso favorable, exactamente lo que el
propio módulo evita en el desborde por arriba.

Ejecución: python3 hallazgo_t33_2_subdesborde_tope_cero.py   (desde la carpeta marcoC)
Imprime FALLA si el defecto existe; OK si está corregido (si el producto no representable da importe None
y avisa O-37, o si el tope 0.0 con importe 0.0 avisa).
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parents[2]   # V0.53: movido a entrega_glm/revisores/
sys.path.insert(0, str(AQUI / "validador"))
sys.path.insert(0, str(AQUI / "pruebas"))

from pruebas_control_f import CART, registrar_foto
from pruebas_manual import libre
from pruebas_orquestador import nuevo

L2 = {"nivel_autonomia": {"TRADING": "L2", "TACTICA": "L2", "LARGO_PLAZO": "L2"}}


def main():
    o = nuevo({**L2, "libres_tope_dia_eur": {"TRADING": 0.0, "TACTICA": 0.0, "LARGO_PLAZO": 0.0}})
    registrar_foto(o, {**CART, "tipos_cambio_eur": {"USD": 1.0}})   # EURUSD -> divisa USD -> fx 1,0
    r = o.registrar_manual(libre(instrumento="EURUSD", activo_base="EUR", cantidad=1e-200, precio=1e-200,
                                 event_id="EV-MAN-0200", ref_intermediario="MAN-H2"), "2026-11-06T09:05:00+00:00")
    o37 = [x for x in o.avisos if x["codigo"] == "O-37"]
    fila = o.libres[0] if o.libres else {}
    # El contraste por arriba (lo que sí hace el código): dos 1e308 dan importe None y O-37
    o2 = nuevo({**L2, "libres_tope_dia_eur": {"TRADING": 0.0, "TACTICA": 0.0, "LARGO_PLAZO": 0.0}})
    registrar_foto(o2, {**CART, "tipos_cambio_eur": {"USD": 1.0}})
    r2 = o2.registrar_manual(libre(instrumento="EURUSD", activo_base="EUR", cantidad=1e300, precio=1e300,
                                   event_id="EV-MAN-0201", ref_intermediario="MAN-H2b"), "2026-11-06T09:05:00+00:00")
    print(f"  desborde por arriba: ok={r2['ok']} tope_superado={r2.get('tope_libres_superado')} "
          f"importe={o2.libres[0]['importe_eur']} O-37={len([x for x in o2.avisos if x['codigo'] == 'O-37'])}")
    print(f"  subdesborde a cero : ok={r['ok']} tope_superado={r.get('tope_libres_superado')} "
          f"importe={fila.get('importe_eur')} O-37={len(o37)}")
    if r["ok"] and r.get("tope_libres_superado") is False and fila.get("importe_eur") == 0.0 and not o37:
        print("FALLA  con tope 0.0 (que prohíbe las LIBRES valoradas), una LIBRE cuyo producto subdesborda a 0.0 "
              "se acepta sin O-37, sin degradación y con tope_libres_superado False")
        return 1
    print("OK    el producto no representable no se valora como cero real")
    return 0


if __name__ == "__main__":
    sys.exit(main())
