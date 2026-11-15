"""QA r01 de T-97 (revisor nuevo sin contexto, Claude). CA-2 con los números del README (20.000 € de capital: 100 € al año) y
bordes del tope anual: justo en el límite, céntimos, reservas de varios encargos, sin foto, capital declarado frente a foto,
capital que baja, cambio de año UTC, aviso O-43 y rutinas sin IA con el tope agotado. Datos SIMULADOS.

Uso: python3 -I r01_tope_anual.py <marco_comun_c de hoy>
"""
import copy
import sys
from datetime import datetime, timezone
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
from pruebas_orquestador import AHORA, CART_E, Arnes, encargo, nuevo  # noqa: E402

h = Arnes()
BASE = {"tope_anual_gasto_pct_capital": 0.5, "capital_referencia_eur": None}   # los valores de partida


def foto(capital, hora="2026-11-06T08:55:00+00:00"):
    return {**copy.deepcopy(CART_E), "fecha_hora": hora, "capital_eur": capital, "tipos_cambio_eur": {"USD": 1.0}}


def emitir(o, n, coste):
    assert o.detectar(f"EXP-{n:04d}", f"COR-{n:04d}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    e = encargo(n)
    e["payload"]["presupuesto"]["coste_max_eur"] = coste
    return o.emitir_encargo(f"EXP-{n:04d}", e, "GESTOR_TACTICA", AHORA)


def o43(o):
    return [a for a in o.avisos if a["codigo"] == "O-43"]


# A. sin foto ni capital declarado
o = nuevo(BASE)
r = emitir(o, 1, 5.0)
h.chk("A_sin_foto_ni_capital_O43", not r["ok"] and r["codigo"] == "O-43", r)
print("   A: avisos O-43 tras rechazar por falta de capital:", len(o43(o)))

# B. CA-2: 20.000 € en la foto, 90 € gastados este año en días anteriores
o = nuevo(BASE)
assert o.registrar_cartera(foto(20000.0), "G", AHORA, cuenta="SIM-1")["ok"]
o.gasto_dia["2026-03-02"] = {"coste": 40.0, "tiempo": 10.0}
o.gasto_dia["2026-10-15"] = {"coste": 50.0, "tiempo": 10.0}
o.gasto_dia["2025-12-31"] = {"coste": 999.0, "tiempo": 10.0}   # otro año: no cuenta
ga, ra, tope = o._gasto_anio(datetime(2026, 11, 6, 9, tzinfo=timezone.utc))
h.chk("B_tope_100_euros_con_20000", abs(tope - 100.0) < 1e-9 and abs(ga - 90.0) < 1e-9 and ra == 0.0, (ga, ra, tope))
r = emitir(o, 1, 10.0)
h.chk("B_justo_hasta_100_se_admite", r["ok"], r)
n_avisos = len(o.avisos)
assert o.detectar("EXP-0002", "COR-0002", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
e2 = encargo(2)
e2["payload"]["presupuesto"]["coste_max_eur"] = 0.01
r = h.rechaza("B_un_centimo_mas_O43_sin_mutar_el_estado", o, lambda: o.emitir_encargo("EXP-0002", e2, "GESTOR_TACTICA", AHORA), "O-43")
print("   B: avisos O-43 tras rechazar un encargo que pasa el tope (comprometido):", len(o43(o)))
r = emitir(o, 3, 25.0)
h.chk("B_encargo_que_pasa_los_100_O43", not r["ok"] and r["codigo"] == "O-43", r)
# el gasto llega al tope
r = o.registrar_gasto("EV-ENC-0001", 10.0, 1.0, AHORA)
h.chk("C_al_llegar_a_100_aviso_O43_ALTA", r["ok"] and "O-43" in r["alertas"] and any(a["prioridad"] == "ALTA" and a["acuse"] is None for a in o43(o)), r)
r = o.registrar_gasto("EV-ENC-0001", 0.5, 1.0, AHORA)   # el gasto es un hecho: se registra aunque pase
h.chk("C_un_gasto_despues_del_tope_se_registra", r["ok"], r)
print("   C: avisos O-43 sin acusar tras dos gastos:", len([a for a in o43(o) if a["acuse"] is None]))
h.chk("C_rutina_sin_IA_foto_sigue", o.registrar_cartera(foto(20000.0, "2026-11-06T08:58:00+00:00"), "G", AHORA, cuenta="SIM-1")["ok"])
h.chk("C_acuse_del_aviso", o.acusar_aviso(o43(o)[0]["id"], "OPERADOR", AHORA)["ok"])
r = emitir(o, 4, 0.01)
h.chk("C_con_el_tope_agotado_ningun_encargo", not r["ok"] and r["codigo"] == "O-43", r)
r = emitir(o, 5, 0.0)
h.chk("C_un_encargo_de_coste_cero_no_es_valido_no_esquiva_el_tope", not r["ok"], r)
print("   C: coste 0 ->", r.get("codigo"), (r.get("motivo") or "")[:80])

# D. reservas de varios encargos a la vez
o = nuevo(BASE)
assert o.registrar_cartera(foto(20000.0), "G", AHORA, cuenta="SIM-1")["ok"]
o.gasto_dia["2026-02-01"] = {"coste": 80.0, "tiempo": 1.0}
h.chk("D_primero_10", emitir(o, 1, 10.0)["ok"])
h.chk("D_segundo_10_hasta_100", emitir(o, 3, 10.0)["ok"])
r = emitir(o, 5, 0.01)
h.chk("D_tercero_no_cabe_por_las_reservas", not r["ok"] and r["codigo"] == "O-43", r)

# E. capital declarado sin foto; luego la foto baja el capital
o = nuevo({**BASE, "capital_referencia_eur": 20000.0})
o.gasto_dia["2026-02-01"] = {"coste": 60.0, "tiempo": 1.0}
h.chk("E_capital_declarado_admite", emitir(o, 1, 5.0)["ok"])
assert o.registrar_cartera(foto(10000.0), "G", AHORA, cuenta="SIM-1")["ok"]   # 50 € al año
r = emitir(o, 3, 5.0)
h.chk("E_la_foto_manda_y_el_capital_bajo_frena", not r["ok"] and r["codigo"] == "O-43", r)
o = nuevo({**BASE, "capital_referencia_eur": 20000.0})
assert o.registrar_cartera(foto(1e6), "G", AHORA, cuenta="SIM-1")["ok"]
_, _, tope = o._gasto_anio(datetime(2026, 11, 6, 9, tzinfo=timezone.utc))
h.chk("E_con_foto_grande_manda_la_foto_5000", abs(tope - 5000.0) < 1e-9, tope)

# F. cambio de año UTC (un instante de Nochevieja en hora local que ya es 2027 en UTC)
o = nuevo(BASE)
assert o.registrar_cartera(foto(20000.0), "G", AHORA, cuenta="SIM-1")["ok"]
o.gasto_dia["2026-12-31"] = {"coste": 100.0, "tiempo": 1.0}
ga, _, _ = o._gasto_anio(datetime.fromisoformat("2026-12-31T23:30:00-02:00"))
h.chk("F_anio_natural_UTC_2027_empieza_de_cero", ga == 0.0, ga)
ga, _, _ = o._gasto_anio(datetime.fromisoformat("2026-12-31T23:30:00+02:00"))
h.chk("F_anio_natural_UTC_2026_cuenta_los_100", ga == 100.0, ga)

print(f"\n{h.n} comprobaciones")
print("RESULTADO:", "TODAS PASAN" if h.ok else "HAY FALLOS")
sys.exit(0 if h.ok else 1)
