"""QA r01 de T-97 (revisor nuevo sin contexto, Claude). F-14 y F-16 (semana) en % del capital: bordes exactos (CA-3, CA-4),
céntimos, capital cero o negativo, contexto sin capital, varias carteras a la vez, y una prueba de propiedad contra el control
de F de la V0.73 (cargado de un worktree del commit anterior a T-97): con la misma política en euros, el F de hoy nunca aprueba
más cantidad ni deja de vetar lo que vetaba la V0.73, y fuera de F-14 y F-16 los controles son idénticos. Datos SIMULADOS.

Uso: python3 -I r01_f_bordes_y_solo_endurece.py <marco_comun_c de hoy> <marco_comun_c de la V0.73>
"""
import copy
import importlib.util
import math
import random
import sys
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve()
V073 = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
import control_f as cf  # noqa: E402
from pruebas_control_f import AHORA_F, CART, solicitud  # noqa: E402
from pruebas_control_f_t22 import cx  # noqa: E402

spec = importlib.util.spec_from_file_location("control_f_v073", V073 / "validador" / "control_f.py")
c73 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c73)   # mandatos y validar_sobre no cambian entre V0.73 y hoy (git diff vacío)
assert c73.VERSION_REGLAS == "F-0.3.0" and cf.VERSION_REGLAS == "F-0.4.0"

P = cf.POLITICA_DEFECTO
NUEVAS = ("importe_max_dia_pct", "perdida_semana_max_pct_trading", "perdida_semana_max_pct_tactica", "perdida_semana_max_pct_largo_plazo")
P73 = {k: v for k, v in P.items() if k not in NUEVAS}
assert set(P73) == set(c73.POLITICA_DEFECTO) and all(P73[k] == c73.POLITICA_DEFECTO[k] for k in P73), "la política en euros cambió"
fallos = 0


def chk(nombre, cond, detalle=""):
    global fallos
    print(("OK   " if cond else "FALLA"), nombre, "" if cond else detalle)
    fallos += 0 if cond else 1


def regla(r, nombre):
    return [c for c in r["controles"] if c["regla"] == nombre]


ENT_EUR = 1.10 * CART["tipos_cambio_eur"]["USD"]

# ------------------------------------------------------------------ CA-3, bordes de F-14
def f14(cap, hoy, q=100000.0, cartera="TACTICA"):
    r = cf.controlar(solicitud(cantidad=q, cartera=cartera), {**CART, "capital_eur": cap}, P, AHORA_F, cx(actividad__importe_dia_eur=hoy))
    return r, regla(r, "F-14")[0]


r, c = f14(20000.0, 4500.0)
chk("CA3_20000_4500_deja_500", c["resultado"] == "REDUCE" and abs(c["limite"] * ENT_EUR - 500.0) < 1e-6 and abs(r["cantidad_aprobada"] * ENT_EUR - 500.0) < 1e-6
    or r["cantidad_aprobada"] * ENT_EUR <= 500.0 + 1e-6, (c, r["cantidad_aprobada"] * ENT_EUR))
print("   CA-3: cantidad aprobada en euros", round(r["cantidad_aprobada"] * ENT_EUR, 4), "resultado", r["resultado"],
      "límites que reducen", [(x["regla"], round(x["limite"] * ENT_EUR, 2)) for x in r["controles"] if x["resultado"] == "REDUCE"])
r, c = f14(20000.0, 4500.0, q=500.0 / ENT_EUR)
chk("F14_justo_en_el_limite_pasa", c["resultado"] == "OK", c)
r, c = f14(20000.0, 4500.0, q=500.01 / ENT_EUR)
chk("F14_un_centimo_por_encima_reduce", c["resultado"] == "REDUCE", c)
r, c = f14(20000.0, 5000.0)
chk("F14_dia_agotado_exacto_no_aprueba_nada", c["limite"] == 0.0 and r["cantidad_aprobada"] == 0.0 and r["resultado"] != "APROBADO", (c, r["resultado"]))
r, c = f14(20000.0, 6000.0)
chk("F14_dia_ya_pasado_limite_cero", c["limite"] == 0.0 and r["cantidad_aprobada"] == 0.0, c)
r, c = f14(20000.04, 0.0, q=5000.01 / ENT_EUR)
chk("F14_centimos_del_capital_25pct_de_20000_04_es_5000_01", c["resultado"] == "OK", (c, c["limite"] * ENT_EUR))
r, c = f14(200000.0, 0.0)
chk("F14_frontera_200000_el_25pct_igual_a_50000", abs(c["limite"] * ENT_EUR - 50000.0) < 1e-6, c)
r, c = f14(1e6, 4500.0)
chk("CA3_1000000_manda_el_euro_45500", abs(c["limite"] * ENT_EUR - 45500.0) < 1e-6, c)
for cap in (0.0, -20000.0, float("nan"), float("inf"), None, "20000"):
    r, _ = (cf.controlar(solicitud(), {**CART, "capital_eur": cap}, P, AHORA_F, cx()), None)
    chk(f"F_capital_{cap!r}_veta_F01", r["resultado"] == "VETADO" and r["controles"][0]["regla"] == "F-01", r["controles"][:1])


# ------------------------------------------------------------------ CA-4, bordes de F-16 semanal por cartera
def f16(cap, perd, cartera):
    r = cf.controlar(solicitud(cartera=cartera), {**CART, "capital_eur": cap}, P, AHORA_F, cx(actividad__perdida_semana_eur=perd))
    return r, [x for x in r["controles"] if x["regla"] == "F-16" and x["limite"] != P["perdida_dia_max_eur"]][0]


for cartera, pct in (("TRADING", 4.0), ("TACTICA", 5.0), ("LARGO_PLAZO", 5.0)):
    lim = pct / 100 * 20000.0
    r, c = f16(20000.0, lim, cartera)
    chk(f"F16_{cartera}_perdida_exacta_{pct}pct_veta", r["resultado"] == "VETADO" and c["resultado"] == "VETA", c)
    r, c = f16(20000.0, lim - 0.01, cartera)
    chk(f"F16_{cartera}_un_centimo_por_debajo_abre", c["resultado"] == "OK" and r["resultado"] != "VETADO", c)
r, c = f16(20000.0, 800.0, "TACTICA")
chk("CA4_4pct_tactica_abre", r["resultado"] != "VETADO", c)
r, c = f16(20000.0, 800.0, "TRADING")
chk("CA4_4pct_trading_no_abre", r["resultado"] == "VETADO", c)
# una pérdida del 4 % con un capital "raro": la cuenta en coma flotante no deja pasar lo que en decimal es exactamente el 4 %
raros = [x for x in (12345.67, 33333.33, 98765.43, 7777.77, 15000.15, 29999.99) if True]
malos = []
for cap in raros:
    perd = round(cap * 4 / 100, 6)
    r, c = f16(cap, perd, "TRADING")
    if c["resultado"] != "VETA" and abs(perd - 0.04 * cap) < 1e-9:
        malos.append((cap, perd, c["limite"]))
# hallazgo bajo (H-04 de la QA r01), no una comprobación: sin esto el script no serviría para matar mutantes
print("   HALLAZGO H-04 (bajo): 4 % exacto en decimal que NO veta por la coma flotante:" if malos else "   4 % exacto: veta siempre", malos)

# contexto al enviar: sin capital solo euros (por diseño); cap bool / lista
for nombre, cap in (("bool", True), ("lista", [1]), ("muy_pequeno", 1e-300)):
    c = cf.controles_de_contexto(solicitud(cartera="TRADING"), P, AHORA_F, cx(actividad__perdida_semana_eur=0.0), cap)
    print(f"   al enviar con capital {nombre}:", [(x['regla'], x['resultado']) for x in c if x["resultado"] == "VETA"][:2])
    if nombre != "muy_pequeno":
        chk(f"al_enviar_capital_{nombre}_falla_cerrado", len(c) == 1 and c[0]["regla"] == "F-01", c[:1])
    else:
        # pérdida 0 < 4 % de un capital positivo minúsculo: no veta, y está bien (el capital positivo lo valida quien lo da)
        chk("al_enviar_capital_minusculo_no_lanza", all(x["resultado"] in ("OK", "VETA") for x in c), c)
# solicitud con cartera ajena al catálogo en el envío: falla cerrado
c = cf.controles_de_contexto(solicitud(cartera="OTRA"), P, AHORA_F, cx(), 20000.0)
chk("al_enviar_cartera_ajena_falla_cerrado", any(x["resultado"] == "VETA" for x in c), c)

# varias carteras a la vez: la misma cuenta, la misma pérdida de la semana (4,5 %): trading veta; táctica y largo plazo abren
res = {k: f16(20000.0, 900.0, k)[0]["resultado"] for k in ("TRADING", "TACTICA", "LARGO_PLAZO")}
chk("varias_carteras_4_5pct_solo_trading_veta", res["TRADING"] == "VETADO" and res["TACTICA"] != "VETADO" and res["LARGO_PLAZO"] != "VETADO", res)

# ------------------------------------------------------------------ política inválida con las claves nuevas
for nombre, cambio in (("dia_pct_nan", {"importe_max_dia_pct": float("nan")}), ("dia_pct_negativo", {"importe_max_dia_pct": -1.0}),
                       ("semana_pct_bool", {"perdida_semana_max_pct_trading": True}), ("semana_pct_texto", {"perdida_semana_max_pct_largo_plazo": "5"}),
                       ("dia_pct_inf", {"importe_max_dia_pct": float("inf")}), ("dia_pct_cero", {"importe_max_dia_pct": 0.0})):
    pv = cf.politica_valida({**P, **cambio})
    r = cf.controlar(solicitud(), CART, {**P, **cambio}, AHORA_F, cx())
    chk(f"politica_{nombre}_invalida_y_F_veta", not pv and r["resultado"] == "VETADO", (pv, r["resultado"]))
chk("politica_con_pct_100_valida", cf.politica_valida({**P, **{k: 100.0 for k in NUEVAS}}))

# ------------------------------------------------------------------ propiedad: nunca más laxo que la V0.73
rnd = random.Random(97)
casos = laxos = distintos = endurece = 0
ejemplos = []
for i in range(4000):
    cap = 10 ** rnd.uniform(2, 7)
    cart = {**CART, "capital_eur": cap, "perdida_dia_eur": rnd.choice([0.0, rnd.uniform(0, 0.03 * cap)]),
            "posiciones": rnd.choice([[], [{"instrumento": "EURUSD", "activo_base": "EUR", "valor_eur": rnd.uniform(0, 0.3 * cap)}]])}
    sol = solicitud(cartera=rnd.choice(["TRADING", "TACTICA", "LARGO_PLAZO"]), cantidad=10 ** rnd.uniform(0, 6),
                    direccion="LARGO", stop_precio=rnd.uniform(0.9, 1.09))
    ctx = cx(actividad__importe_dia_eur=rnd.choice([0.0, rnd.uniform(0, 0.4 * cap), rnd.uniform(0, 60000)]),
             actividad__perdida_semana_eur=rnd.choice([0.0, rnd.uniform(0, 0.08 * cap), rnd.uniform(0, 6000)]))
    pol = {**P, **{k: rnd.choice([P[k], rnd.uniform(0.01, 100.0), 100.0]) for k in NUEVAS}}
    if not cf.politica_valida(pol):
        continue
    con_ctx = rnd.random() < 0.85
    a = c73.controlar(copy.deepcopy(sol), copy.deepcopy(cart), copy.deepcopy(P73), AHORA_F, copy.deepcopy(ctx) if con_ctx else None)
    b = cf.controlar(copy.deepcopy(sol), copy.deepcopy(cart), copy.deepcopy(pol), AHORA_F, copy.deepcopy(ctx) if con_ctx else None)
    casos += 1
    if b["cantidad_aprobada"] > a["cantidad_aprobada"] * (1 + 1e-12) + 1e-12 or (a["resultado"] == "VETADO" and b["resultado"] != "VETADO"):
        laxos += 1
        ejemplos.append((cap, sol["cartera"], a["resultado"], b["resultado"]))
    if b["cantidad_aprobada"] < a["cantidad_aprobada"] or (b["resultado"] == "VETADO") != (a["resultado"] == "VETADO"):
        endurece += 1
    # F-11 (valor mínimo del resto) depende de la cantidad aprobada: si F-14 reduce más, F-11 puede pasar de OK a VETA (endurece),
    # nunca al revés
    otros_a = [(x["regla"], x["resultado"], x["limite"]) for x in a["controles"] if x["regla"] not in ("F-14", "F-16", "F-11")]
    otros_b = [(x["regla"], x["resultado"], x["limite"]) for x in b["controles"] if x["regla"] not in ("F-14", "F-16", "F-11")]
    f11a = [x["resultado"] for x in a["controles"] if x["regla"] == "F-11"]
    f11b = [x["resultado"] for x in b["controles"] if x["regla"] == "F-11"]
    if otros_a != otros_b or ("VETA" in f11a and "VETA" not in f11b):
        distintos += 1
    # con los porcentajes al 100 % y un capital tan grande que nunca muerden, resultado idéntico al de la V0.73
chk(f"propiedad_nunca_mas_laxo_que_V073_({casos}_casos,_{endurece}_endurecen)", laxos == 0, ejemplos[:5])
chk("propiedad_fuera_de_F14_F16_F11_controles_identicos_y_F11_solo_endurece", distintos == 0, distintos)
grandes = 0
for i in range(500):
    cap = 10 ** rnd.uniform(6.5, 8)   # 25 % de >= 3,16 M € > 50.000 €; 4 % > 5.000 €: los euros mandan
    sol = solicitud(cartera=rnd.choice(["TRADING", "TACTICA", "LARGO_PLAZO"]), cantidad=10 ** rnd.uniform(0, 6))
    ctx = cx(actividad__importe_dia_eur=rnd.uniform(0, 60000), actividad__perdida_semana_eur=rnd.uniform(0, 6000))
    a = c73.controlar(sol, {**CART, "capital_eur": cap}, P73, AHORA_F, ctx)
    b = cf.controlar(sol, {**CART, "capital_eur": cap}, P, AHORA_F, ctx)
    grandes += (a["resultado"], a["cantidad_aprobada"]) != (b["resultado"], b["cantidad_aprobada"])
chk("carteras_grandes_identicas_a_V073", grandes == 0, grandes)

print("FALLOS:", fallos)
sys.exit(1 if fallos else 0)
