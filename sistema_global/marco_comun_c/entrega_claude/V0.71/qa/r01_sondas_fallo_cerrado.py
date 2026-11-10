"""QA r01 de T-76 (V0.71): sondas de fallo cerrado, atomicidad, actores, veredicto e integridad del registro. Datos SIMULADOS.

Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.71/qa/r01_sondas_fallo_cerrado.py
Cada sonda imprime CONFIRMADO (el fallo existe) o NO (el código se comporta bien).
"""
import copy
import json
import sys
from pathlib import Path

MARCO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
from pruebas_orquestador import AHORA, nuevo  # noqa: E402

RES = []
NAN, INF = float("nan"), float("inf")


def sonda(nombre, confirmado, detalle=""):
    RES.append((nombre, confirmado))
    print(f"{'CONFIRMADO' if confirmado else 'NO':10s} {nombre}  {detalle}")


def foto(o):
    d = copy.deepcopy(o.__dict__)
    return json.dumps(d, sort_keys=True, default=str)


def mes_k(k):
    a, m = 2026 + (10 + k) // 12, (10 + k) % 12 + 1
    return f"{a:04d}-{m:02d}", f"{a:04d}-{m:02d}-28T12:00:00+00:00"


def base(comparados=0, robot=900.0):
    o = nuevo()
    assert o.iniciar_sombra(1000.0, 100.0, "OPERADOR", AHORA)["ok"]
    for k in range(1, comparados + 1):
        mes, t = mes_k(k)
        assert o.comparar_sombra(mes, robot, 100.0, 100.0, 100.0, 0.0, "I", t)["ok"]
    return o


# ---------------------------------------------------------------- F1: rechazos con entradas raras no cambian nada
raros = [NAN, INF, -INF, -1.0, 0, True, False, None, "100", [100.0], {"x": 1}, 10 ** 400, complex(1, 0)]
cambian, excepciones = [], []
o = nuevo()
for v in raros:
    for args in ((v, 100.0), (1000.0, v)):
        antes = foto(o)
        try:
            r = o.iniciar_sombra(*args, "OPERADOR", AHORA)
        except Exception as ex:   # noqa: BLE001
            excepciones.append(("iniciar", repr(v), type(ex).__name__)); continue
        if r["ok"]:
            cambian.append(("iniciar acepta", repr(v)))
            o = nuevo()
        elif foto(o) != antes:
            cambian.append(("iniciar cambia", repr(v), r["codigo"]))
o = base()
for v in raros:
    for args in (("APORTE", v, 100.0), ("APORTE", 10.0, v), ("RETIRADA", v, 100.0), (v, 10.0, 100.0)):
        antes = foto(o)
        try:
            r = o.movimiento_sombra(*args, "OPERADOR", AHORA)
        except Exception as ex:   # noqa: BLE001
            excepciones.append(("movimiento", repr(args), type(ex).__name__)); continue
        if r["ok"]:
            cambian.append(("movimiento acepta", repr(args)))
            o = base()
        elif foto(o) != antes:
            cambian.append(("movimiento cambia", repr(args), r["codigo"]))
o = base()
mes1, t1 = mes_k(1)
for v in raros:
    for i in range(6):
        args = [mes1, 900.0, 100.0, 100.0, 100.0, 0.0]
        args[i] = v
        if i in (1, 5) and v in (0, False):
            continue   # cero es válido para el valor del robot y los impuestos
        antes = foto(o)
        try:
            r = o.comparar_sombra(*args, "I", t1)
        except Exception as ex:   # noqa: BLE001
            excepciones.append(("comparar", i, repr(v), type(ex).__name__)); continue
        if r["ok"]:
            cambian.append(("comparar acepta", i, repr(v)))
            o = base()
        elif foto(o) != antes:
            cambian.append(("comparar cambia", i, repr(v), r["codigo"]))
sonda("F1_entradas_raras_aceptadas_o_que_cambian_el_estado", bool(cambian or excepciones), f"{cambian[:6]} {excepciones[:4]}")

# ---------------------------------------------------------------- F2: actores
o = base()
malos = []
for act in ("I", "BROKER", "D", "F", "operador", "OPERADOR ", None, 1):
    r = o.iniciar_sombra(1.0, 1.0, act, AHORA)
    if r["codigo"] != "O-05" and act != "OPERADOR":
        malos.append(("iniciar", act, r["codigo"]))
for act in ("I", "BROKER", "D", "F", "g", None):
    r = o.movimiento_sombra("APORTE", 1.0, 1.0, act, AHORA)
    if r["ok"]:
        malos.append(("movimiento", act))
for act in ("OPERADOR", "G", "i", "BROKER", None):
    r = o.comparar_sombra(mes1, 900.0, 100.0, 100.0, 100.0, 0.0, act, t1)
    if r["ok"]:
        malos.append(("comparar", act))
sonda("F2_actor_no_autorizado_aceptado", bool(malos), f"{malos}")

# ---------------------------------------------------------------- F3: repetir, desordenar, saltar
o = base(1)
r_rep = o.comparar_sombra(mes1, 5000.0, 100.0, 100.0, 100.0, 0.0, "I", t1)
r_ant = o.comparar_sombra("2026-11", 5000.0, 100.0, 100.0, 100.0, 0.0, "I", t1)
r_salta = o.comparar_sombra(mes_k(3)[0], 5000.0, 100.0, 100.0, 100.0, 0.0, "I", mes_k(3)[1])
sonda("F3_comparar_dos_veces_hacia_atras_o_saltando", any(x["ok"] for x in (r_rep, r_ant, r_salta)),
      f"{r_rep['codigo']} {r_ant['codigo']} {r_salta['codigo']}")

# ---------------------------------------------------------------- F4: silenciar O-41 sin comparar: nada avisa
o = base(23)
avisos_antes = len(o.avisos)
r = o.barrer("2029-06-30T12:00:00+00:00") if hasattr(o, "barrer") else None
nuevos = [a["codigo"] for a in o.avisos[avisos_antes:]]
sonda("F4_si_I_no_compara_el_mes_24_nada_avisa_nunca", "O-41" not in nuevos and not any("sombra" in a["motivo"] for a in o.avisos[avisos_antes:]),
      f"7 meses después del plazo, barrer() emite {nuevos}; la sombra sigue en 23 comparaciones, sin O-41 ni aviso de retraso")

# ---------------------------------------------------------------- F5: comparar el mes 24 tarde, con el último día que convenga
o = base(23)
r = o.comparar_sombra(mes_k(24)[0], 900.0, 100.0, 100.0, 100.0, 0.0, "I", "2030-01-01T00:00:00+00:00")
sonda("F5_el_mes_24_se_puede_comparar_un_anio_tarde", r["ok"], f"{r['codigo']} veredicto {r.get('veredicto')} (los días de coste son los de 2030)")

# ---------------------------------------------------------------- F6: O-41 cada mes tras el plazo, sin duplicar el mismo mes
o = base(26)
n41 = [a for a in o.avisos if a["codigo"] == "O-41"]
sonda("F6_O41_duplicado_o_ausente_tras_el_plazo", len(n41) != 3, f"{len(n41)} avisos O-41 en los meses 24, 25 y 26")

# ---------------------------------------------------------------- F7: registro tocado que esquiva el O-13 y el kill-switch
fallos = []
for nombre, toque in (("sin_ahora_en_el_inicio", lambda L: L["entradas"][0].pop("ahora")),
                      ("sin_mes_en_una_comparacion", lambda L: L["entradas"][-1].pop("mes")),
                      ("tipo_no_texto", lambda L: L["entradas"][-1].__setitem__("tipo", None))):
    o = base(2)
    toque(o.sombra)
    mes, t = mes_k(3)
    r = o.comparar_sombra(mes, 900.0, 100.0, 100.0, 100.0, 0.0, "I", t)
    if not (r["codigo"] == "O-13" and o.kill is not None):
        fallos.append((nombre, r["codigo"], o.kill is not None, o.integridad()))
o = base(2)
o.sombra["entradas"][0]["tipo"] = "X"
r = o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2027-02-01T00:00:00+00:00")
if not (r["codigo"] == "O-13" and o.kill is not None):
    fallos.append(("iniciar_con_registro_tocado", r["codigo"], o.kill is not None, o.integridad()))
sonda("F7_registro_tocado_rechazado_sin_O13_ni_kill", bool(fallos), f"{fallos}")

# ---------------------------------------------------------------- F8: vaciar o recortar el registro no se detecta (falta el ancla)
o = base(24)
o.sombra = {"historial": [], "estado": "VIGENTE", "entradas": []}
vacio = o.integridad() == [] and o.sombra_ok()
r = o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2028-12-01T00:00:00+00:00")
o2 = base(24)
for _ in range(1):
    o2.sombra["historial"].pop(); o2.sombra["entradas"].pop()
recorte = o2.integridad() == []
r2 = o2.comparar_sombra(mes_k(24)[0], 99999.0, 100.0, 100.0, 100.0, 0.0, "I", "2028-12-01T00:00:00+00:00")
sonda("F8_vaciar_o_recortar_el_registro_reinicia_o_rehace_el_juicio", vacio and r["ok"] or (recorte and r2["ok"]),
      f"vaciado: integridad limpia={vacio}, nuevo inicio {r['codigo']} (el reloj de 24 meses vuelve a cero); recorte del último: "
      f"integridad limpia={recorte}, mes 24 otra vez {r2['codigo']} {r2.get('veredicto')} (límite conocido del encadenado sin ancla externa)")

# ---------------------------------------------------------------- F9: gasto_dia tocado en memoria (sin diario) no se detecta
o = base(23)
o.gasto_dia["2027-01-01"] = {"coste": -1e6, "tiempo": 0.0}
r = o.comparar_sombra(mes_k(24)[0], 900.0, 100.0, 100.0, 100.0, 0.0, "I", mes_k(24)[1])
sonda("F9_gasto_dia_negativo_inyectado_regala_un_millon_al_robot", r["ok"] and r["veredicto"] == "SUPERA" and o.integridad() == [],
      f"{r['codigo']} {r.get('veredicto')} costes={o.sombra['entradas'][-1]['costes_analisis_eur'] if r['ok'] else None}; integridad {o.integridad()}")

# ---------------------------------------------------------------- F10: rechazo por retirada excesiva: atómico
o = base(1)
antes = foto(o)
r = o.movimiento_sombra("RETIRADA", 1e9, 100.0, "OPERADOR", t1)
sonda("F10_retirada_excesiva_cambia_algo", foto(o) != antes, f"{r['codigo']}")

# ---------------------------------------------------------------- F11: informe_sombra devuelve copias
o = base(1)
inf = o.informe_sombra()
inf["ultima"]["veredicto"] = "SUPERA"; inf["inicio"]["importe_eur"] = 1.0
sonda("F11_informe_sombra_expone_el_registro", not o.sombra_ok(), "")

# ---------------------------------------------------------------- F12: comparar con el kill-switch activo o la configuración rota
o = base(1)
o.cfg["dia_coste_max_eur"] = 1e9
r = o.comparar_sombra(mes_k(2)[0], 900.0, 100.0, 100.0, 100.0, 0.0, "I", mes_k(2)[1])
sonda("F12_config_rota_no_para_la_comparacion", r["ok"], f"{r['codigo']} kill={o.kill is not None}")

# ---------------------------------------------------------------- F13: la sombra se inicia sin cartera real o con otro capital
o = nuevo()
r = o.iniciar_sombra(123456789.0, 1.0, "OPERADOR", AHORA)
sonda("F13_el_capital_inicial_no_se_contrasta_con_la_cartera_real", r["ok"], f"{r['codigo']}: cualquier importe, sin foto de la cartera real")

print(f"\n{sum(1 for _, c in RES if c)} confirmadas de {len(RES)} sondas")
