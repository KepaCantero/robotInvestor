"""QA r01 de T-97 (revisor nuevo sin contexto, Claude). El camino de verdad del Orquestador al enviar la orden (_f_al_enviar):
una autorización con 50.000 € de capital y sin pérdida, y antes de enviar la pérdida de la semana sube al 5,4 % (2.700 €, por
debajo de los 5.000 € del tope en euros). Con el % la orden no sale (O-06 por F-16); con la V0.73 habría salido. También una
cartera grande (1.000.000 €), donde todo sigue como en la V0.73. Datos SIMULADOS.

Uso: python3 -I r01_envio_semana.py <marco_comun_c de hoy>
"""
import sys
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_orquestador import AHORA, CART_E, Arnes, autorizar_op, hasta, nuevo  # noqa: E402

h = Arnes()


def autorizada(capital):
    o = nuevo()
    hasta(o, "PROPUESTA", n=1, cartera_e={**CART_E, "capital_eur": capital})
    r = autorizar_op(o, "EXP-0001", informe_f(o, "EXP-0001", 1, cartera={"capital_eur": capital}), AHORA)
    assert r["ok"], r
    assert o.expedientes["EXP-0001"]["control_f"]["entradas"]["cartera"]["capital_eur"] == capital
    return o


o = autorizada(50000.0)
o.perdidas_dia["2026-11-04"] = 1400.0   # pérdidas de días anteriores de la semana (lo que dejan las fotos de G)
o.perdidas_dia["2026-11-05"] = 1300.0
r = o.orden_entrada("EXP-0001", "ORD-1", "ENVIADA", 0.0, "G", AHORA)
h.chk("envio_con_5_4pct_de_perdida_semanal_tactica_no_sale_O06_F16", not r["ok"] and r["codigo"] == "O-06" and "F-16" in (r.get("reglas") or []), r)

o = autorizada(50000.0)
o.perdidas_dia["2026-11-04"] = 1200.0
o.perdidas_dia["2026-11-05"] = 1200.0   # 2.400 €: 4,8 %, por debajo del 5 % de táctica
r = o.orden_entrada("EXP-0001", "ORD-1", "ENVIADA", 0.0, "G", AHORA)
h.chk("envio_con_4_8pct_tactica_sale", r["ok"], r)

o = autorizada(1e6)
o.perdidas_dia["2026-11-04"] = 1400.0
o.perdidas_dia["2026-11-05"] = 1300.0
r = o.orden_entrada("EXP-0001", "ORD-1", "ENVIADA", 0.0, "G", AHORA)
h.chk("envio_cartera_grande_como_V073_sale", r["ok"], r)

print(f"\n{h.n} comprobaciones")
print("RESULTADO:", "TODAS PASAN" if h.ok else "HAY FALLOS")
sys.exit(0 if h.ok else 1)
