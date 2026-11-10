"""QA r01 de T-76 (V0.71): sondas del cálculo de la cartera sombra. Datos SIMULADOS.

Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.71/qa/r01_sondas_calculo.py
Cada sonda imprime CONFIRMADO (el fallo existe) o NO (el código se comporta bien). Termina con 0 siempre: es una sonda, no una prueba.
"""
import copy
import sys
from pathlib import Path

MARCO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
import persistencia as pe  # noqa: E402
import sombra as sb  # noqa: E402
from parametros import PARAMETROS  # noqa: E402
from pruebas_orquestador import AHORA, nuevo  # noqa: E402

RES = []


def sonda(nombre, confirmado, detalle=""):
    RES.append((nombre, confirmado))
    print(f"{'CONFIRMADO' if confirmado else 'NO':10s} {nombre}  {detalle}")


def meses_hasta(o, n, robot, precio, ahora_de, inf_ini=100.0, inf_mes=100.0, imp=0.0):
    """Compara los meses que faltan hasta el n (contados desde el inicio en 2026-11)."""
    r = None
    hechos = len([x for x in o.sombra["entradas"] if x["tipo"] == "COMPARACION"])
    for k in range(hechos + 1, n + 1):
        a, m = 2026 + (10 + k) // 12, (10 + k) % 12 + 1
        mes = f"{a:04d}-{m:02d}"
        r = o.comparar_sombra(mes, robot(k) if callable(robot) else robot, precio, inf_ini, inf_mes, imp, "I", ahora_de(mes))
        assert r["ok"], (k, r)
    return r


def dia28(mes):
    return f"{mes}-28T12:00:00+00:00"


# ---------------------------------------------------------------- S1: coste de la sombra sobre todo el periodo, también lo aportado ayer
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]           # 10 unidades el 2026-11-06
meses_hasta(o, 23, 1000.0, 100.0, dia28)
assert o.movimiento_sombra("APORTE", 1_000_000.0, 100.0, "OPERADOR", "2028-11-27T12:00:00+00:00")["ok"]   # 10 000 unidades la víspera
r = o.comparar_sombra("2028-11", 1_000_000.0, 100.0, 100.0, 100.0, 0.0, "I", "2028-11-28T12:00:00+00:00")
c = o.sombra["entradas"][-1]["sombra"]
dias_total = (pe and 0) or None
# coste justo: cada tramo paga por los días que estuvo dentro
ini_dias = 753.125   # 2026-11-06T09 -> 2028-11-28T12
coste_justo = 1000.0 * 0.002 * ini_dias / 365 + 1_000_000.0 * 0.002 * 1 / 365
sonda("S1_coste_prorrateado_cobra_al_aporte_de_ayer_dos_anos_de_coste", c["coste_eur"] > 5 * coste_justo,
      f"coste cobrado {c['coste_eur']:.2f} EUR frente a ~{coste_justo:.2f} EUR justos; el robot con 1 001 000 - {c['coste_eur']:.0f} "
      f"y ~{c['valor_bruto_eur'] - coste_justo:.0f} justos; veredicto {r['veredicto']} con el robot en 1 000 000 (no aporta nada: 1000 EUR por debajo de la sombra bruta)")
sonda("S1b_el_robot_que_pierde_1000_EUR_supera_a_la_sombra", r["veredicto"] == "SUPERA" and 1_000_000.0 < c["valor_bruto_eur"] - coste_justo,
      f"robot {1_000_000.0:.0f}, sombra con coste justo {c['valor_bruto_eur'] - coste_justo:.2f}, sombra según el código {c['valor_eur']:.2f}")

# ---------------------------------------------------------------- S2: una retirada borra el coste ya devengado (el coste no se acumula)
o = nuevo()
assert o.iniciar_sombra(1_000_000.0, 100.0, "OPERADOR", AHORA)["ok"]
meses_hasta(o, 23, 1_000_000.0, 100.0, dia28)
antes = o.sombra["entradas"][-1]["sombra"]["coste_eur"]
assert o.movimiento_sombra("RETIRADA", 999_000.0, 100.0, "OPERADOR", "2028-11-27T12:00:00+00:00")["ok"]
r = o.comparar_sombra("2028-11", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2028-11-28T12:00:00+00:00")
despues = o.sombra["entradas"][-1]["sombra"]["coste_eur"]
sonda("S2_retirar_borra_el_coste_devengado_por_lo_retirado", despues < antes / 100,
      f"coste acumulado el mes 23: {antes:.2f} EUR; el mes 24, tras retirar, {despues:.4f} EUR (el coste de 23 meses sobre 999 000 EUR desaparece)")

# ---------------------------------------------------------------- S3: el coste depende del precio de hoy (sube y baja con el índice, no es lo pagado)
e = [{"tipo": "INICIO", "importe_eur": 1000.0, "precio_indice": 100.0}]
a = sb.estado_sombra(e, 100.0, 365)["coste_eur"]
b = sb.estado_sombra(e, 300.0, 365)["coste_eur"]
sonda("S3_coste_recalculado_al_precio_de_hoy_y_no_acumulado", abs(b - 3 * a) < 1e-9, f"un año al 0,20 %: {a:.2f} EUR si el índice vale 100 y {b:.2f} EUR si vale 300 (el cobrado no cambia con el precio)")

# ---------------------------------------------------------------- S4: el juicio de «24 meses» llega con 23 meses y una hora
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-11-30T23:00:00+00:00")["ok"]
r = meses_hasta(o, 24, 900.0, 100.0, lambda mes: f"{mes}-01T00:00:00+00:00")
dias = (o.sombra["entradas"][-1]["ahora"], o.sombra["entradas"][0]["ahora"])
sonda("S4_juicio_a_los_24_meses_con_23_meses_y_1_hora", r["veredicto"] == "PROPONER_PASIVA" and o.sombra["entradas"][-1]["meses"] == 24,
      f"inicio {dias[1]}, juicio {dias[0]}: veredicto {r['veredicto']} (meses={o.sombra['entradas'][-1]['meses']})")
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-11-30T23:00:00+00:00")["ok"]
r = o.comparar_sombra("2026-12", 900.0, 100.0, 100.0, 100.0, 0.0, "I", "2026-12-01T00:00:00+00:00")
sonda("S4b_el_mes_se_compara_antes_de_cerrarse", r["ok"], f"el mes 2026-12 se compara el 2026-12-01T00:00 (una hora tras el inicio): {r['codigo']}")

# ---------------------------------------------------------------- S5: el mes del inicio sale del texto local, no de UTC
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-11-30T20:00:00-05:00")["ok"]   # en UTC ya es 2026-12-01T01:00
r = o.comparar_sombra("2026-12", 900.0, 100.0, 100.0, 100.0, 0.0, "I", "2026-12-01T01:00:00+00:00")
sonda("S5_mes_del_inicio_con_huso_local_y_el_resto_en_UTC", r["ok"],
      f"inicio 2026-11-30T20:00-05:00 (UTC 1 dic): se acepta comparar 2026-12 en el mismo instante: {r['codigo']} (el mes 1 dura 0 s)")
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-12-01T00:30:00+01:00")["ok"]   # UTC 2026-11-30T23:30
r1 = o.comparar_sombra("2026-12", 900.0, 100.0, 100.0, 100.0, 0.0, "I", "2026-12-28T00:00:00+00:00")
sonda("S5b_el_mismo_instante_con_otro_huso_cambia_el_calendario", not r1["ok"],
      f"inicio 2026-12-01T00:30+01:00 (UTC 30 nov): comparar 2026-12 -> {r1['codigo']}; con +00:00 sería el mes 1")

# ---------------------------------------------------------------- S6: costes de análisis del día del inicio anteriores al inicio
o = nuevo()
from pruebas_orquestador import hasta  # noqa: E402
hasta(o, "EN_ANALISIS", 1)
assert o.registrar_gasto("EV-ENC-0001", 7.0, 1.0, AHORA)["ok"]   # 09:00, antes del inicio
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2026-11-06T18:00:00+00:00")["ok"]
r = o.comparar_sombra("2026-12", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2026-12-28T00:00:00+00:00")
sonda("S6_cuenta_el_gasto_del_dia_del_inicio_hecho_antes_del_inicio", o.sombra["entradas"][-1]["costes_analisis_eur"] == 7.0,
      f"costes_analisis_eur={o.sombra['entradas'][-1]['costes_analisis_eur']} (gasto de las 09:00, inicio a las 18:00; conservador, contra el robot)")

# ---------------------------------------------------------------- S7: inflación del inicio distinta en cada mes
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
r1 = o.comparar_sombra("2026-12", 1000.0, 100.0, 100.0, 101.0, 0.0, "I", "2026-12-28T00:00:00+00:00")
r2 = o.comparar_sombra("2027-01", 1000.0, 100.0, 50.0, 102.0, 0.0, "I", "2027-01-28T00:00:00+00:00")
sonda("S7_el_indice_de_precios_del_inicio_cambia_de_un_mes_a_otro", r1["ok"] and r2["ok"],
      f"inflación acumulada {r1['resultado']['inflacion_acumulada']:.3f} y luego {r2['resultado']['inflacion_acumulada']:.3f} con el mismo inicio")

# ---------------------------------------------------------------- S8: el juicio real es idéntico al nominal (mismo divisor)
iguales = all((sb.comparar(rv, 0, 0, {"valor_eur": sv, "aportado_neto_eur": 1.0}, 100.0, f)["supera"] == (rv > sv))
              for rv in (99.0, 100.0, 101.0) for sv in (100.0,) for f in (50.0, 100.0, 300.0))
sonda("S8_real_y_nominal_dan_siempre_el_mismo_veredicto", iguales, "dividir los dos valores por el mismo factor no cambia cuál es mayor")

# ---------------------------------------------------------------- S9: valores enormes: NaN guardado y estado que no se puede volcar
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
r = o.comparar_sombra("2026-12", 1000.0, 1e308, 100.0, 100.0, 0.0, "I", "2026-12-28T00:00:00+00:00")
vol = None
try:
    pe.volcar(o, "2026-12-28T00:00:01+00:00")
    vol = "se vuelca"
except Exception as ex:   # noqa: BLE001
    vol = f"{type(ex).__name__}: {str(ex)[:80]}"
sonda("S9_precio_finito_enorme_acepta_y_guarda_NaN", r["ok"] and r["resultado"]["sombra_eur"] != r["resultado"]["sombra_eur"],
      f"{r['codigo']} {r.get('veredicto')} sombra_eur={r.get('resultado', {}).get('sombra_eur')}; volcar: {vol}; integridad={o.integridad()}")
o = nuevo()
r = o.iniciar_sombra(1e200, 1e-200, "OPERADOR", AHORA)
r2 = o.comparar_sombra("2026-12", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2026-12-28T00:00:00+00:00")
try:
    pe.volcar(o, "2026-12-28T00:00:01+00:00")
    vol = "se vuelca"
except Exception as ex:   # noqa: BLE001
    vol = f"{type(ex).__name__}: {str(ex)[:80]}"
sonda("S9b_inicio_con_unidades_infinitas", r["ok"] and r["unidades"] == float("inf"),
      f"{r['codigo']} unidades={r.get('unidades')}; comparar luego: {r2['codigo']} {r2.get('veredicto')} sombra_eur={(r2.get('resultado') or {}).get('sombra_eur')}; volcar: {vol}")
o = nuevo()
assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
r = o.comparar_sombra("2026-12", 1000.0, 100.0, 1e300, 1e-5, 0.0, "I", "2026-12-28T00:00:00+00:00")
sonda("S9c_inflacion_diminuta_da_reales_infinitos_o_NaN", r["ok"], f"{r['codigo']} {r.get('veredicto')} {r.get('resultado')}")

# ---------------------------------------------------------------- S10: tolerancia absoluta en unidades: retirar más de lo que hay
o = nuevo()
assert o.iniciar_sombra(1000.0, 1e12, "OPERADOR", AHORA)["ok"]   # 1e-9 unidades
r = o.movimiento_sombra("RETIRADA", 2000.0, 1e12, "OPERADOR", AHORA)
est = sb.estado_sombra(o.sombra["entradas"], 1e12, 0)
sonda("S10_retirada_del_doble_aceptada_por_la_tolerancia_en_unidades", r["ok"] and est["valor_eur"] < 0,
      f"{r['codigo']} valor de la sombra {est['valor_eur'] if est else None} EUR")

# ---------------------------------------------------------------- S11: precio distinto en el mismo instante: retirar barato y aportar caro
o = nuevo()
assert o.iniciar_sombra(10000.0, 100.0, "OPERADOR", AHORA)["ok"]
r1 = o.movimiento_sombra("RETIRADA", 5000.0, 50.0, "G", AHORA)
r2 = o.movimiento_sombra("APORTE", 5000.0, 100.0, "G", AHORA)
est = sb.estado_sombra(o.sombra["entradas"], 100.0, 0)
sonda("S11_G_vacia_la_sombra_con_dos_precios_en_el_mismo_instante", r1["ok"] and r2["ok"] and est["unidades"] < 51,
      f"aporte neto 0 EUR, unidades {est['unidades']:.1f} de 100 (la sombra pasa de 10 000 a {est['valor_eur']:.0f} EUR)")

# ---------------------------------------------------------------- S12: la sombra no paga impuestos ni comisiones por aporte
sonda("S12_la_sombra_no_lleva_impuestos_ni_comisiones_de_compra", "impuestos" not in str(sb.estado_sombra(e, 100.0, 0)),
      "el robot resta impuestos estimados; la sombra solo su coste anual (asimetría no declarada en el documento)")

# ---------------------------------------------------------------- S13: retirada que vacía exactamente y meses siguientes
o = nuevo()
assert o.iniciar_sombra(10000.0, 100.0, "OPERADOR", AHORA)["ok"]
assert o.movimiento_sombra("APORTE", 1100.0, 110.0, "OPERADOR", AHORA)["ok"]
r = o.movimiento_sombra("RETIRADA", 110.0 * 110.0, 110.0, "OPERADOR", AHORA)   # todo: 110 unidades a 110
r2 = o.comparar_sombra("2026-12", 0.0, 120.0, 100.0, 100.0, 0.0, "I", "2026-12-28T00:00:00+00:00")
sonda("S13_vaciar_la_sombra_y_comparar_rompe", not (r["ok"] and r2["ok"]),
      f"retirada {r['codigo']}, comparación {r2['codigo']} {r2.get('veredicto')} exceso_sobre_aportado={(r2.get('resultado') or {}).get('exceso_sobre_aportado')}")

# ---------------------------------------------------------------- S14: año bisiesto y meses de 28 a 31 días
n = sb.meses_entre("2027-02", "2028-02"), sb.meses_entre("2027-12", "2028-01"), sb.meses_entre("2026-11", "2028-11")
sonda("S14_meses_entre_mal_en_bordes_de_anio", n != (12, 1, 24), f"{n}")

print(f"\n{sum(1 for _, c in RES if c)} confirmadas de {len(RES)} sondas; i_coste_anual_sombra_pct={PARAMETROS['i_coste_anual_sombra_pct']}")
