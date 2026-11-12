"""QA r03 de T-76 (V0.75): el mes valorado a su cierre, el plazo de gracia, el mes de juicio y los siguientes, ponerse al día y los
costes de análisis en el borde. Bordes de mes y de año en UTC y en otros husos. Datos SIMULADOS.

Uso: python3 -I .docs/tickets/T-76/revisores/r03_01_cierre_plazos_juicio.py [ruta del marco]
     (por defecto, sistema_global/marco_comun_c de este repositorio)
Cada sonda imprime FALLA (el defecto existe) o BIEN (el código se comporta como debe). Termina con 0 siempre: es una sonda.

Referencia independiente del código: un fondo con valor liquidativo N(t) = (1 - c)^(segundos desde el inicio / (365 · 86 400)).
Cada aporte compra X / (P · N(t)) participaciones; cada retirada las vende igual; el valor en T es participaciones · P_T · N(T).
"""
import copy
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[4] / "sistema_global" / "marco_comun_c"
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
from parametros import PARAMETROS  # noqa: E402
from pruebas_orquestador import AHORA, hasta, nuevo  # noqa: E402

RES = []
C = PARAMETROS["i_coste_anual_sombra_pct"]
G = PARAMETROS["i_dias_gracia_comparacion_sombra"]
J = PARAMETROS["i_meses_juicio_sombra"]


def sonda(nombre, falla, detalle=""):
    RES.append((nombre, falla))
    print(f"{'FALLA' if falla else 'BIEN':6s} {nombre}  {detalle}")


def dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def iso(t):
    return t.astimezone(timezone.utc).isoformat(timespec="microseconds")


def referencia(movs, precio_T, T):
    t0 = dt(movs[0][3])
    N = lambda t: (1 - C / 100.0) ** ((t - t0).total_seconds() / (365 * 86400.0))  # noqa: E731
    part, neto = 0.0, 0.0
    for tipo, imp, p, a in movs:
        s = imp / (p * N(dt(a)))
        part += -s if tipo == "RETIRADA" else s
        neto += -imp if tipo == "RETIRADA" else imp
    return part * precio_T * N(T), neto


def mes_sig(mes):
    a, m = map(int, mes.split("-"))
    return f"{a + m // 12:04d}-{m % 12 + 1:02d}"


def cierre(mes):
    """Último microsegundo del mes en UTC."""
    a, m = map(int, mes_sig(mes).split("-"))
    return datetime(a, m, 1, tzinfo=timezone.utc) - timedelta(microseconds=1)


def mes_k(k, dia="02T06:00:00"):
    """El mes k desde el inicio (AHORA: 2026-11) y un instante del mes siguiente."""
    a, m = 2026 + (10 + k) // 12, (10 + k) % 12 + 1
    a2, m2 = 2026 + (11 + k) // 12, (11 + k) % 12 + 1
    return f"{a:04d}-{m:02d}", f"{a2:04d}-{m2:02d}-{dia}+00:00"


def cod(o, c):
    return [x for x in o.avisos if x["codigo"] == c]


# ------------------------------------------------------------------ A1: movimientos en el borde del cierre (UTC y otros husos)
o = nuevo()
assert o.iniciar_sombra(100000.0, 100.0, "OPERADOR", AHORA)["ok"]
movs = [("INICIO", 100000.0, 100.0, AHORA)]
for tipo, imp, p, a in (("APORTE", 10000.0, 101.0, "2026-12-31T23:59:59.999999+00:00"),   # último µs de diciembre: entra
                        ("APORTE", 3000.0, 102.0, "2027-01-01T00:00:00+00:00"),          # primer instante de enero: no entra
                        ("RETIRADA", 2000.0, 99.0, "2027-01-01T00:30:00+01:00")):        # = 2026-12-31T23:30Z en hora local de enero: es de enero (posterior)
    r = o.movimiento_sombra(tipo, imp, p, "OPERADOR", a)
    movs.append((tipo, imp, p, a))
    assert r["ok"] or r["codigo"] == "O-16", r
# el tercero retrocede el reloj (23:30Z < 00:00Z): se rechaza con O-16 y no se anota
anotados = [x["ahora"] for x in o.sombra["entradas"] if x["tipo"] != "INICIO"]
movs = [m for m in movs if m[0] == "INICIO" or m[3] in anotados]
r = o.comparar_sombra("2026-12", 110000.0, 103.0, 100.0, 100.0, 0.0, "I", "2027-01-02T06:00:00+00:00")
est = o.sombra["entradas"][-1]["sombra"]
ref, neto = referencia([m for m in movs if dt(m[3]) <= cierre("2026-12")], 103.0, cierre("2026-12"))
sonda("A1_mov_en_el_ultimo_microsegundo_entra_y_el_del_primer_instante_no", not (r["ok"] and abs(est["valor_eur"] - ref) < 1e-6 and est["aportado_neto_eur"] == neto == 110000.0),
      f"{r['codigo']}; aportado {est['aportado_neto_eur']} (esperado {neto}); valor {est['valor_eur']:.6f} / ref {ref:.6f}; anotados {len(anotados)}")

# A1b: un movimiento escrito en -05:00 el 31-12 a las 20:00 (01:00Z del 1 de enero) es de enero; en +05:00 el 1-1 a las 04:00 (23:00Z) es de diciembre
o = nuevo()
assert o.iniciar_sombra(100000.0, 100.0, "OPERADOR", AHORA)["ok"]
assert o.movimiento_sombra("APORTE", 5000.0, 100.0, "OPERADOR", "2027-01-01T04:00:00+05:00")["ok"]
assert o.movimiento_sombra("APORTE", 7000.0, 100.0, "OPERADOR", "2026-12-31T20:00:00-05:00")["ok"]
r = o.comparar_sombra("2026-12", 105000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-01-02T06:00:00+00:00")
r2 = o.comparar_sombra("2027-01", 112000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-02-02T06:00:00+00:00")
n1, n2 = (x["sombra"]["aportado_neto_eur"] for x in o.sombra["entradas"] if x["tipo"] == "COMPARACION")
sonda("A1b_el_mes_del_movimiento_es_el_de_UTC_en_otros_husos", not (r["ok"] and r2["ok"] and n1 == 105000.0 and n2 == 112000.0), f"dic {n1}, ene {n2}")

# ------------------------------------------------------------------ A2: costes de análisis en el borde del cierre
o = nuevo()
hasta(o, "EN_ANALISIS", 1)
assert o.registrar_gasto("EV-ENC-0001", 1.0, 1.0, AHORA)["ok"]   # mismo día del inicio, antes de la hora del inicio (convención conservadora)
assert o.iniciar_sombra(100000.0, 100.0, "OPERADOR", "2026-11-06T12:00:00+00:00")["ok"]
assert o.registrar_gasto("EV-ENC-0001", 3.0, 1.0, "2026-12-31T23:59:59.999999+00:00")["ok"]   # último µs: cuenta en diciembre
assert o.registrar_gasto("EV-ENC-0001", 7.0, 1.0, "2027-01-01T00:00:00+00:00")["ok"]          # primer instante de enero: no
r = o.comparar_sombra("2026-12", 100000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-01-03T06:00:00+00:00")
c12 = o.sombra["entradas"][-1]["costes_analisis_eur"]
r = o.comparar_sombra("2027-01", 100000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-02-03T06:00:00+00:00")
c01 = o.sombra["entradas"][-1]["costes_analisis_eur"]
sonda("A2_costes_de_analisis_hasta_el_cierre_y_no_despues", not (c12 == 4.0 and c01 == 11.0), f"diciembre {c12} (esperado 4.0: 1 del día del inicio + 3 del último µs); enero {c01} (esperado 11.0, acumulado)")

# ------------------------------------------------------------------ A3: la sombra se valora al cierre (coste devengado hasta el cierre, no hasta la comparación)
o = nuevo()
assert o.iniciar_sombra(1e6, 100.0, "OPERADOR", AHORA)["ok"]
r = o.comparar_sombra("2026-12", 1e6, 100.0, 100.0, 100.0, 0.0, "I", "2027-01-30T06:00:00+00:00")   # 29 días tarde
est = o.sombra["entradas"][-1]["sombra"]
ref_c, _ = referencia([("INICIO", 1e6, 100.0, AHORA)], 100.0, cierre("2026-12"))
ref_a, _ = referencia([("INICIO", 1e6, 100.0, AHORA)], 100.0, dt("2027-01-30T06:00:00+00:00"))
sonda("A3_el_coste_se_devenga_hasta_el_cierre_aunque_I_compare_tarde", not (abs(est["valor_eur"] - ref_c) < 1e-6),
      f"código {est['valor_eur']:.4f}; ref. al cierre {ref_c:.4f}; ref. a la comparación {ref_a:.4f}")

# ------------------------------------------------------------------ A4: ponerse al día con varios meses en el mismo instante, con movimientos entre medias
o = nuevo()
assert o.iniciar_sombra(50000.0, 100.0, "OPERADOR", AHORA)["ok"]
movs = [("INICIO", 50000.0, 100.0, AHORA)]
for tipo, imp, p, a in (("APORTE", 20000.0, 110.0, "2026-12-15T10:00:00+00:00"), ("RETIRADA", 15000.0, 95.0, "2027-01-31T23:59:59+00:00"),
                        ("APORTE", 5000.0, 120.0, "2027-02-01T00:00:00+00:00"), ("APORTE", 1000.0, 90.0, "2027-03-20T00:00:00-03:00")):
    assert o.movimiento_sombra(tipo, imp, p, "G", a)["ok"]
    movs.append((tipo, imp, p, a))
precios = {"2026-12": 105.0, "2027-01": 98.0, "2027-02": 121.0}
t = "2027-04-08T06:00:00+00:00"   # 2027-03 sin terminar el día... no: abril; se comparan diciembre, enero y febrero el mismo día
dif = []
for mes, p in precios.items():
    r = o.comparar_sombra(mes, 60000.0, p, 100.0, 100.0, 0.0, "I", t)
    est = o.sombra["entradas"][-1]["sombra"]
    ref, neto = referencia([m for m in movs if dt(m[3]) <= cierre(mes)], p, cierre(mes))
    dif.append((mes, r["codigo"], round(est["valor_eur"] - ref, 9), est["aportado_neto_eur"], neto))
sonda("A4_ponerse_al_dia_valora_cada_mes_a_su_propio_cierre", not all(c == "OK" and abs(d) < 1e-6 and a == n for _, c, d, a, n in dif), dif)

# ------------------------------------------------------------------ A5: febrero de un año bisiesto y el cambio de año
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2028-01-15T00:00:00+00:00")["ok"]
assert o.movimiento_sombra("APORTE", 500.0, 100.0, "OPERADOR", "2028-02-29T23:59:59.999999+00:00")["ok"]
r0 = o.comparar_sombra("2028-02", 1500.0, 100.0, 100.0, 100.0, 0.0, "I", "2028-02-29T23:59:59.999999+00:00")
r1 = o.comparar_sombra("2028-02", 1500.0, 100.0, 100.0, 100.0, 0.0, "I", "2028-03-01T00:00:00+00:00")
neto = o.sombra["entradas"][-1]["sombra"]["aportado_neto_eur"] if r1["ok"] else None
p_ant = o.comparaciones_sombra_pendientes(f"2028-04-{G:02d}T23:59:59.999999+00:00")
p_en = o.comparaciones_sombra_pendientes(f"2028-04-{G + 1:02d}T00:00:00+00:00")
sonda("A5_febrero_bisiesto_y_su_plazo", not (r0["codigo"] == "O-01" and r1["ok"] and neto == 1500.0 and p_ant is None and p_en and p_en["primero"] == "2028-03"),
      f"en el último µs: {r0['codigo']}; 1 mar 00:00Z: {r1['codigo']}, aportado {neto}; pendiente al acabar la gracia de marzo: {p_ant} / {p_en}")
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-12-31T23:59:59.999999+00:00")["ok"]   # el último µs del año: el mes del inicio es diciembre
r_a = o.comparar_sombra("2027-01", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-02-01T00:00:00+00:00")
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-12-31T19:00:00-05:00")["ok"]   # = 2027-01-01T00:00Z: el mes del inicio es enero
r_b = o.comparar_sombra("2027-01", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-02-01T00:00:00+00:00")
r_c = o.comparar_sombra("2027-02", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-03-01T00:00:00+00:00")
sonda("A5b_inicio_en_el_cambio_de_anio_en_UTC", not (r_a["ok"] and r_b["codigo"] == "O-01" and r_c["ok"]), f"{r_a['codigo']} {r_b['codigo']} {r_c['codigo']}")

# ------------------------------------------------------------------ A6: el plazo de gracia exacto, en UTC y en otros husos, por barrer()
def o42_tras(ahora):
    o = nuevo()
    assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
    o.barrer(ahora)
    return len(cod(o, "O-42")) + len(cod(o, "O-44"))
lim = datetime(2027, 1, 1, tzinfo=timezone.utc) + timedelta(days=G)
casos = {"lim-1µs": o42_tras(iso(lim - timedelta(microseconds=1))), "lim": o42_tras(iso(lim)),
         "lim+00:30 en +01:00 (antes en UTC)": o42_tras((lim - timedelta(minutes=30)).astimezone(timezone(timedelta(hours=1))).isoformat()),
         "lim-00:30 en -01:00 (después en UTC)": o42_tras((lim + timedelta(minutes=30)).astimezone(timezone(timedelta(hours=-1))).isoformat())}
sonda("A6_el_plazo_de_gracia_exacto_en_cualquier_huso", list(casos.values()) != [0, 1, 0, 1], casos)

# ------------------------------------------------------------------ A7: el mes de juicio (24) y los siguientes: O-41 al pasar a no superarla
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
robots = {k: 2000.0 for k in range(1, 24)}
robots.update({24: 900.0, 25: 2000.0, 26: 900.0, 27: 900.0, 28: 2000.0, 29: 900.0})
vers = []
for k in range(1, 30):
    mes, t = mes_k(k)
    r = o.comparar_sombra(mes, robots[k], 100.0, 100.0, 100.0, 0.0, "I", t)
    vers.append((k, r["veredicto"], len(cod(o, "O-41"))))
esperado = [(k, "EN_PLAZO", 0) for k in range(1, 24)] + [(24, "PROPONER_PASIVA", 1), (25, "SUPERA", 1), (26, "PROPONER_PASIVA", 2),
                                                           (27, "PROPONER_PASIVA", 2), (28, "SUPERA", 2), (29, "PROPONER_PASIVA", 3)]
sonda("A7_mes_de_juicio_y_siguientes", vers != esperado, [v for v in vers if v[0] >= 23])
m24 = [x for x in o.sombra["entradas"] if x["tipo"] == "COMPARACION"][23]
sonda("A7b_el_mes_24_es_2028_11_y_se_juzga_con_mas_de_24_meses_desde_el_inicio",
      not (m24["mes"] == "2028-11" and m24["meses"] == J and (cierre("2028-11") - dt(AHORA)).days >= 365 * 2),
      f"mes {m24['mes']}, meses {m24['meses']}, días del inicio al cierre {(cierre('2028-11') - dt(AHORA)).days}")

# ------------------------------------------------------------------ A8: O-42 frente a O-44 al ponerse al día cruzando el mes de juicio
def con_comparados(n):
    o = nuevo()
    assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
    for k in range(1, n + 1):
        mes, t = mes_k(k)
        assert o.comparar_sombra(mes, 1000.0, 100.0, 100.0, 100.0, 0.0, "I", t)["ok"]
    return o
o = con_comparados(20)   # comparados hasta 2028-07; faltan 2028-08 (21) a 2028-11 (24, juicio)
d_antes = o.comparaciones_sombra_pendientes(f"2028-12-{G:02d}T23:59:59+00:00")    # 21 a 23: aún no ha vencido la gracia del 24
d_juicio = o.comparaciones_sombra_pendientes(f"2028-12-{G + 1:02d}T00:00:00+00:00")
o.barrer(f"2028-12-{G:02d}T23:59:59+00:00")
o.barrer(f"2028-12-{G + 1:02d}T00:00:00+00:00")
cods = [(x["codigo"], x["prioridad"], x["motivo"].split("(")[1].split(")")[0]) for x in o.avisos if x["codigo"] in ("O-42", "O-44")]
sonda("A8_O44_en_cuanto_vence_la_gracia_del_mes_de_juicio_aunque_falten_anteriores",
      not (d_antes == {"primero": "2028-08", "faltan": 3, "juicio": False} and d_juicio == {"primero": "2028-08", "faltan": 4, "juicio": True}
           and [c[:2] for c in cods] == [("O-42", "MEDIA"), ("O-44", "ALTA")]), f"{d_antes} / {d_juicio}; avisos {cods}")
# ponerse al día con 21 a 23: queda el 24 y sigue O-44 (con 1 mes)
t = f"2028-12-{G + 2:02d}T00:00:00+00:00"
for k in (21, 22, 23):
    assert o.comparar_sombra(mes_k(k)[0], 1000.0, 100.0, 100.0, 100.0, 0.0, "I", t)["ok"]
o.barrer(t)
ult = [x for x in o.avisos if x["codigo"] in ("O-42", "O-44")][-1]
r = o.comparar_sombra("2028-11", 900.0, 100.0, 100.0, 100.0, 0.0, "I", t)
o.barrer(f"2028-12-{G + 3:02d}T00:00:00+00:00")
tras = [x["codigo"] for x in o.avisos if x["codigo"] in ("O-42", "O-44")]
sonda("A8b_al_ponerse_al_dia_el_aviso_baja_a_un_mes_y_tras_juzgar_no_vuelve",
      not (ult["codigo"] == "O-44" and "(1 mes(es)" in ult["motivo"] and r["veredicto"] == "PROPONER_PASIVA" and len(tras) == 3),
      f"último aviso {ult['codigo']} «{ult['motivo'][:90]}…»; juicio {r.get('veredicto')}; avisos de pendiente {tras}")

# ------------------------------------------------------------------ A9: repetición: barridos diarios sin comparar durante tres meses; acuse; reiteración del ALTA
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
d = datetime(2027, 1, 1, 6, tzinfo=timezone.utc)
while d < datetime(2027, 3, 31, tzinfo=timezone.utc):
    o.barrer(iso(d))
    d += timedelta(days=1)
mot = [x["motivo"].split(" (")[1].split(" sin")[0] for x in cod(o, "O-42")]
sonda("A9_un_O42_por_cada_mes_que_se_suma_no_uno_por_barrido", mot != ["1 mes(es)", "2 mes(es)", "3 mes(es)"], f"{len(cod(o, 'O-42'))} O-42 en 89 barridos diarios: {mot}")
av = cod(o, "O-42")[-1]
assert o.acusar_aviso(av["id"], "OPERADOR", "2027-03-31T07:00:00+00:00")["ok"]
o.barrer("2027-03-31T08:00:00+00:00")
n_tras_acuse = len(cod(o, "O-42"))
sonda("A9b_tras_el_acuse_vuelve_a_avisar_si_sigue_pendiente", n_tras_acuse != 4, f"O-42 tras acusar el último y barrer: {n_tras_acuse}")
o = con_comparados(23)
o.barrer(f"2028-12-{G + 1:02d}T00:00:00+00:00")
o.barrer(f"2028-12-{G + 3:02d}T00:00:00+00:00")
o44 = cod(o, "O-44")
sonda("A9c_O44_es_ALTA_y_se_reitera_y_escala_como_los_ALTA", not (len(o44) == 1 and o44[0]["reiteraciones"] and o44[0]["canal"] != "CONSOLA"),
      f"O-44 {len(o44)}; reiteraciones {len(o44[0]['reiteraciones']) if o44 else None}; escalado {o44[0]['escalado'] if o44 else None}; canal {o44[0]['canal'] if o44 else None}")

# ------------------------------------------------------------------ A10: el instante exacto del cierre para comparar
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
r_c = o.comparar_sombra("2026-12", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2026-12-31T23:59:59.999999+00:00")
r_l = o.comparar_sombra("2026-12", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-01-01T00:59:59.999999+01:00")   # aún 31-12 en UTC
r_s = o.comparar_sombra("2026-12", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-01-01T00:00:00+00:00")
sonda("A10_comparar_en_el_cierre_no_y_un_microsegundo_despues_si", not (r_c["codigo"] == "O-01" and r_l["codigo"] == "O-01" and r_s["ok"]),
      f"{r_c['codigo']} {r_l['codigo']} {r_s['codigo']}")

# ------------------------------------------------------------------ A11: la comparación del mes no depende del día en que se haga (varias fechas, mismo veredicto y cifras)
def compara_el_24(dia):
    o = con_comparados(23)
    assert o.movimiento_sombra("APORTE", 300.0, 100.0, "OPERADOR", "2028-12-01T00:00:00+00:00")["ok"]
    r = o.comparar_sombra("2028-11", 999.0, 100.0, 100.0, 100.0, 0.0, "I", dia)
    return r["veredicto"], json.dumps(o.sombra["entradas"][-1]["resultado"], sort_keys=True)
res = {d: compara_el_24(d) for d in ("2028-12-01T00:00:01+00:00", "2028-12-20T00:00:00+00:00", "2029-06-01T00:00:00+00:00")}
sonda("A11_el_juicio_del_mes_24_no_depende_del_dia_en_que_se_compara", len({v for v in res.values()}) != 1, {k: v[0] for k, v in res.items()})

# ------------------------------------------------------------------ A12: lo pendiente cuenta desde el mes de inicio en UTC (inicio escrito en hora local del mes siguiente)
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-12-01T00:30:00+01:00")["ok"]   # = 2026-11-30T23:30Z: el primer mes que se compara es 2026-12
d = o.comparaciones_sombra_pendientes(f"2027-01-{G + 1:02d}T00:00:00+00:00")
sonda("A12_pendiente_desde_el_mes_de_inicio_en_UTC", d != {"primero": "2026-12", "faltan": 1, "juicio": False}, d)

print(f"\n{sum(1 for _, c in RES if c)} FALLA de {len(RES)} sondas; coste {C} %, gracia {G} días, juicio {J} meses")
