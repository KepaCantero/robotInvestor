"""QA r02 de T-76 (V0.73): el devengo del coste de la sombra contra un cálculo independiente, meses terminados en UTC y no finitos.
Datos SIMULADOS.

Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.71/qa/r02_sondas_calculo.py
Cada sonda imprime FALLA (el defecto existe) o BIEN (el código se comporta como debe). Termina con 0 siempre: es una sonda.

Cálculo de referencia (independiente del código): un fondo con valor liquidativo N(t) = (1 - c)^(años desde el inicio), con
años = segundos / (365 · 86 400). Cada aporte compra X / (P · N(t)) participaciones «brutas»; cada retirada las vende igual; el
valor en T es participaciones · P_T · N(T). Es lo que hace un fondo que descuenta su gasto corriente del valor liquidativo.
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

MARCO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
import persistencia as pe  # noqa: E402
import sombra as sb  # noqa: E402
from parametros import PARAMETROS  # noqa: E402
from pruebas_orquestador import AHORA, nuevo  # noqa: E402

RES = []
C = PARAMETROS["i_coste_anual_sombra_pct"]


def sonda(nombre, falla, detalle=""):
    RES.append((nombre, falla))
    print(f"{'FALLA' if falla else 'BIEN':6s} {nombre}  {detalle}")


def dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def referencia(movs, precio_T, T, c=C):
    """movs: [(tipo, importe, precio, ahora_iso)], el primero INICIO. Devuelve (valor, bruto sin coste)."""
    t0 = dt(movs[0][3])
    N = lambda t: (1 - c / 100.0) ** ((t - t0).total_seconds() / (365 * 86400.0))  # noqa: E731
    part, bruto_u = 0.0, 0.0
    for tipo, x, p, t in movs:
        s = -1 if tipo == "RETIRADA" else 1
        part += s * x / (p * N(dt(t)))
        bruto_u += s * x / p
    return part * precio_T * N(T), bruto_u * precio_T


def entradas(movs):
    return [{"tipo": t, "importe_eur": x, "precio_indice": p, "ahora": a} for t, x, p, a in movs]


def cerca(a, b, rel=1e-9):
    return abs(a - b) <= rel * max(1.0, abs(a), abs(b))


# ---------------------------------------------------------------- C1: varios aportes y retiradas en fechas distintas (incluye 2028, bisiesto)
casos = {
    "aporte_y_retirada": [("INICIO", 10000.0, 100.0, "2026-11-06T09:00:00+00:00"), ("APORTE", 5000.0, 110.0, "2027-03-15T10:00:00+00:00"),
                          ("RETIRADA", 3000.0, 95.0, "2027-09-01T00:00:00+00:00"), ("APORTE", 250.0, 130.0, "2028-02-29T23:59:59+00:00")],
    "huso_distinto": [("INICIO", 1000.0, 100.0, "2026-12-01T00:30:00+01:00"), ("APORTE", 1000.0, 100.0, "2027-06-30T20:00:00-05:00")],
    "mismo_instante": [("INICIO", 1000.0, 100.0, AHORA), ("APORTE", 1000.0, 50.0, AHORA), ("RETIRADA", 500.0, 50.0, AHORA)],
    "aporte_la_vispera": [("INICIO", 1000.0, 100.0, AHORA), ("APORTE", 1_000_000.0, 100.0, "2028-11-30T12:00:00+00:00")],
}
T = dt("2028-12-01T12:00:00+00:00")
for nombre, movs in casos.items():
    est = sb.estado_sombra(entradas(movs), 120.0, T)
    v, b = referencia(movs, 120.0, T)
    sonda(f"C1_{nombre}_distinto_del_calculo_independiente", est is None or not (cerca(est["valor_eur"], v) and cerca(est["valor_bruto_eur"], b)),
          f"código {est and round(est['valor_eur'], 6)} / {est and round(est['valor_bruto_eur'], 6)}; referencia {v:.6f} / {b:.6f}")

# ---------------------------------------------------------------- C2: coste 0: la sombra vale lo bruto, exactamente
movs = casos["aporte_y_retirada"]
est = sb.estado_sombra(entradas(movs), 120.0, T, coste_anual_pct=0.0)
sonda("C2_coste_cero_no_da_el_valor_bruto", est is None or not (est["coste_eur"] == 0.0 and est["valor_eur"] == est["valor_bruto_eur"]), f"{est}")

# ---------------------------------------------------------------- C3: un año exacto (365 días y 366 en bisiesto)
e1 = entradas([("INICIO", 1000.0, 100.0, "2027-01-01T00:00:00+00:00")])
a365 = sb.estado_sombra(e1, 100.0, dt("2028-01-01T00:00:00+00:00"))
e2 = entradas([("INICIO", 1000.0, 100.0, "2028-01-01T00:00:00+00:00")])
a366 = sb.estado_sombra(e2, 100.0, dt("2029-01-01T00:00:00+00:00"))
sonda("C3_un_anio_natural_no_cobra_el_coste_anual", not cerca(a365["coste_eur"], 1000.0 * C / 100.0),
      f"2027: {a365['coste_eur']:.6f} EUR (esperado {1000 * C / 100:.6f}); 2028 (366 días): {a366['coste_eur']:.6f} EUR "
      f"(cobra 366/365 de año: convención días/365, anotada como observación)")

# ---------------------------------------------------------------- C4: retirada total exacta, y un pelo más
movs = [("INICIO", 1000.0, 100.0, "2026-11-06T09:00:00+00:00")]
T4 = dt("2027-11-06T09:00:00+00:00")
v, _ = referencia(movs, 100.0, T4)
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
r_todo = o.movimiento_sombra("RETIRADA", v, 100.0, "OPERADOR", "2027-11-06T09:00:00+00:00")
est = sb.estado_sombra(o.sombra["entradas"], 100.0, T4)
o2 = nuevo()
assert o2.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
r_mas = o2.movimiento_sombra("RETIRADA", v * (1 + 1e-9), 100.0, "OPERADOR", "2027-11-06T09:00:00+00:00")
r_bruto = o2.movimiento_sombra("RETIRADA", 1000.0, 100.0, "OPERADOR", "2027-11-06T09:00:00+00:00")
sonda("C4_retirada_total_mal", not (r_todo["ok"] and est is not None and abs(est["valor_eur"]) < 1e-9 and not r_mas["ok"] and not r_bruto["ok"]),
      f"retirar {v:.6f} (todo, neto de coste): {r_todo['codigo']}, queda {est and est['valor_eur']}; un 1e-9 más: {r_mas['codigo']}; "
      f"los 1000 EUR brutos: {r_bruto['codigo']}")
r_c = o.comparar_sombra("2026-12", 0.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-11-07T00:00:00+00:00")
sonda("C4b_tras_vaciarla_la_comparacion_rompe", not r_c["ok"] or r_c["resultado"]["exceso_sobre_aportado"] is not None,
      f"{r_c['codigo']} {r_c.get('veredicto')} (sombra vacía y robot a 0: se compara, sin proporción sobre lo aportado)")

# ---------------------------------------------------------------- C5: el caso de la r01 (H-01, S1): aporte de un millón la víspera
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
for k in range(1, 24):
    a, m = 2026 + (10 + k) // 12, (10 + k) % 12 + 1
    a2, m2 = 2026 + (11 + k) // 12, (11 + k) % 12 + 1
    assert o.comparar_sombra(f"{a:04d}-{m:02d}", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", f"{a2:04d}-{m2:02d}-01T06:00:00+00:00")["ok"]
assert o.movimiento_sombra("APORTE", 1_000_000.0, 100.0, "OPERADOR", "2028-11-30T12:00:00+00:00")["ok"]
r = o.comparar_sombra("2028-11", 1_000_000.0, 100.0, 100.0, 100.0, 0.0, "I", "2028-12-01T12:00:00+00:00")
c = o.sombra["entradas"][-1]["sombra"]
v, b = referencia([("INICIO", 1000.0, 100.0, AHORA), ("APORTE", 1_000_000.0, 100.0, "2028-11-30T12:00:00+00:00")], 100.0, dt("2028-12-01T12:00:00+00:00"))
sonda("C5_aporte_de_la_vispera_sigue_pagando_dos_anios", not (cerca(c["valor_eur"], v) and r["veredicto"] == "PROPONER_PASIVA"),
      f"coste {c['coste_eur']:.2f} EUR (referencia {b - v:.2f}); robot 1 000 000 frente a sombra {c['valor_eur']:.2f}: {r['veredicto']}")

# ---------------------------------------------------------------- C6: el caso de la r01 (H-01, S2): la retirada no borra lo devengado
movs = [("INICIO", 1_000_000.0, 100.0, AHORA), ("RETIRADA", 999_000.0, 100.0, "2028-11-30T12:00:00+00:00")]
est = sb.estado_sombra(entradas(movs), 100.0, dt("2028-12-01T12:00:00+00:00"))
sonda("C6_la_retirada_tiene_que_poder_hacerse_y_dejar_lo_que_toca", est is not None,
      "retirar 999 000 de 1 000 000 tras dos años de coste (quedan ~995 000 netos): " + ("aceptada" if est else "RECHAZADA: queda menos de 999 000"))

# ---------------------------------------------------------------- C7: el coste no depende del precio de hoy en proporción a lo pagado (H-01, S3)
e = entradas([("INICIO", 1000.0, 100.0, "2026-11-06T00:00:00+00:00")])
a1 = sb.estado_sombra(e, 100.0, dt("2027-11-06T00:00:00+00:00"))
a3 = sb.estado_sombra(e, 300.0, dt("2027-11-06T00:00:00+00:00"))
sonda("C7_proporcion_del_coste_cambia_con_el_precio", not cerca(a1["coste_eur"] / a1["valor_bruto_eur"], a3["coste_eur"] / a3["valor_bruto_eur"]),
      f"coste/bruto {a1['coste_eur'] / a1['valor_bruto_eur']:.6f} a 100 y {a3['coste_eur'] / a3['valor_bruto_eur']:.6f} a 300 "
      "(en euros escala con el precio, como en un fondo: el coste se cobra en participaciones)")

# ---------------------------------------------------------------- C8: meses terminados en UTC: bordes de mes, de año y husos
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-12-31T23:30:00-01:00")["ok"]   # UTC 2027-01-01T00:30: mes del inicio 2027-01
r_ant = o.comparar_sombra("2027-01", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-02-01T06:00:00+00:00")   # el mes del inicio (UTC) no
r_dic = o.comparar_sombra("2027-02", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-03-01T00:30:00+01:00")   # UTC 28 feb 23:30
r_ene = o.comparar_sombra("2027-02", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-02-28T23:00:00-01:00")  # UTC 1 mar 00:00
sonda("C8_borde_de_mes_con_huso", r_ant["ok"] or r_dic["ok"] or not r_ene["ok"],
      f"inicio 31 dic 23:30 -01:00 (UTC 1 ene): comparar 2027-01: {r_ant['codigo']}; 2027-02 el 28 feb 23:30 UTC escrito en +01:00: "
      f"{r_dic['codigo']}; el 1 mar 00:00 UTC escrito en -01:00: {r_ene['codigo']}")
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-11-30T23:59:59+00:00")["ok"]
r1 = o.comparar_sombra("2026-12", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2026-12-31T23:59:59.999999+00:00")
r2 = o.comparar_sombra("2026-12", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-01-01T00:00:00Z")
sonda("C8b_borde_de_anio", r1["ok"] or not r2["ok"], f"31 dic 23:59:59.999999: {r1['codigo']}; 1 ene 00:00Z: {r2['codigo']}")
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-11-30T23:00:00+00:00")["ok"]
ver, t_juicio = None, None
for k in range(1, 25):
    a, m = 2026 + (10 + k) // 12, (10 + k) % 12 + 1
    a2, m2 = 2026 + (11 + k) // 12, (11 + k) % 12 + 1
    t_juicio = f"{a2:04d}-{m2:02d}-01T00:00:00+00:00"
    r = o.comparar_sombra(f"{a:04d}-{m:02d}", 900.0, 100.0, 100.0, 100.0, 0.0, "I", t_juicio)
    assert r["ok"], (k, r)
dias = (dt(t_juicio) - dt("2026-11-30T23:00:00+00:00")).days
sonda("C8c_juicio_con_menos_de_24_meses", dias < 731, f"juicio {r['veredicto']} el {t_juicio}: {dias} días desde el inicio")

# ---------------------------------------------------------------- C9: no finitos (r01 S9, S9b, S9c, D2)
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
r = o.comparar_sombra("2026-11", 1000.0, 1e308, 100.0, 100.0, 0.0, "I", "2026-12-01T00:00:00+00:00")
r = o.comparar_sombra("2026-12", 1000.0, 1e308, 100.0, 100.0, 0.0, "I", "2027-01-01T00:00:00+00:00")
r_b = o.comparar_sombra("2026-12", 1e308, 100.0, 1e-300, 1e10, 0.0, "I", "2027-01-01T00:00:00+00:00")
r_c = o.comparar_sombra("2026-12", 1000.0, 100.0, 1e300, 1e-5, 0.0, "I", "2027-01-01T00:00:00+00:00")
vol = "se vuelca"
try:
    pe.volcar(o, "2027-01-01T00:00:01+00:00")
except Exception as ex:   # noqa: BLE001
    vol = f"{type(ex).__name__}"
sonda("C9_no_finitos_anotados", r["ok"] or r_b["ok"] or vol != "se vuelca",
      f"precio 1e308: {r['codigo']}; robot 1e308 con inflación 1e10/1e-300: {r_b['codigo']}; inflación 1e-5/1e300: {r_c['codigo']} "
      f"{(r_c.get('resultado') or {}).get('inflacion_acumulada')}; volcar: {vol}")
o = nuevo()
ri = o.iniciar_sombra(1e200, 1e-200, "OPERADOR", AHORA)
rc = o.comparar_sombra("2026-12", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-01-01T00:00:00+00:00")
ra = o.movimiento_sombra("APORTE", 10.0, 100.0, "OPERADOR", "2027-01-01T00:00:01+00:00")
sonda("C9b_inicio_con_unidades_infinitas_aceptado", ri["ok"],
      f"iniciar(1e200, 1e-200): {ri['codigo']} unidades={ri.get('unidades')}; luego comparar {rc['codigo']} y aportar {ra['codigo']} "
      f"«{ra.get('motivo')}»: la sombra queda inservible para siempre y no se puede reiniciar")
r_inf_cmp = o.comparar_sombra("2026-12", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-01-02T00:00:00+00:00")

# ---------------------------------------------------------------- C10: H-06: retirar el doble con precios enormes
o = nuevo()
assert o.iniciar_sombra(1000.0, 1e12, "OPERADOR", AHORA)["ok"]
r = o.movimiento_sombra("RETIRADA", 2000.0, 1e12, "OPERADOR", AHORA)
r2 = o.movimiento_sombra("RETIRADA", 1000.0 * (1 - 1e-6), 1e12, "OPERADOR", AHORA)
sonda("C10_retirada_del_doble_aceptada", r["ok"] or not r2["ok"], f"el doble: {r['codigo']}; casi todo: {r2['codigo']}")

print(f"\n{sum(1 for _, c in RES if c)} FALLA de {len(RES)} sondas; i_coste_anual_sombra_pct={C}")
