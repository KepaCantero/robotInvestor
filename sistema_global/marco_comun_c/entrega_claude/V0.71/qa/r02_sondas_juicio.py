"""QA r02 de T-76 (V0.73): el juicio de los 24 meses y sus avisos (O-41, O-42), comparaciones atrasadas, integridad antes de leer,
índice de precios del inicio y límites H-07/H-09. Datos SIMULADOS.

Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.71/qa/r02_sondas_juicio.py
Cada sonda imprime FALLA (el defecto existe) o BIEN (el código se comporta como debe). Las que llevan «LIMITE» miden un límite
declarado (H-07, H-09): FALLA quiere decir que el límite sigue ahí, no que sea un defecto nuevo. Termina con 0 siempre.
"""
import copy
import json
import sys
from pathlib import Path

MARCO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
from pruebas_orquestador import AHORA, hasta, nuevo  # noqa: E402

RES = []


def sonda(nombre, falla, detalle=""):
    RES.append((nombre, falla))
    print(f"{'FALLA' if falla else 'BIEN':6s} {nombre}  {detalle}")


def mes_k(k, dia="01T06:00:00"):
    """El mes k desde el inicio (2026-11) y un instante del mes siguiente (cuando ya terminó)."""
    a, m = 2026 + (10 + k) // 12, (10 + k) % 12 + 1
    a2, m2 = 2026 + (11 + k) // 12, (11 + k) % 12 + 1
    return f"{a:04d}-{m:02d}", f"{a2:04d}-{m2:02d}-{dia}+00:00"


def base(comparados=0, robot=900.0, inicio=1000.0):
    o = nuevo()
    assert o.iniciar_sombra(inicio, 100.0, "OPERADOR", AHORA)["ok"]
    for k in range(1, comparados + 1):
        mes, t = mes_k(k)
        r = o.comparar_sombra(mes, robot(k) if callable(robot) else robot, 100.0, 100.0, 100.0, 0.0, "I", t)
        assert r["ok"], (k, r)
    return o


def foto(o):
    return json.dumps(copy.deepcopy(o.__dict__), sort_keys=True, default=str)


def o42(o):
    return [a for a in o.avisos if a["codigo"] == "O-42"]


# ---------------------------------------------------------------- J1: O-42 no salta antes de que termine el mes (UTC)
o = base()
o.barrer("2026-12-31T23:59:59+00:00")
n1 = len(o42(o))
o.barrer("2027-01-01T00:30:00+01:00")   # UTC 2026-12-31T23:30... pero el reloj no puede retroceder: se usa otro orquestador
o = base()
o.barrer("2027-01-01T00:30:00+01:00")
n2 = len(o42(o))
o.barrer("2027-01-01T00:00:00Z")
n3 = len(o42(o))
sonda("J1_O42_antes_de_tiempo_o_tarde", not (n1 == 0 and n2 == 0 and n3 == 1),
      f"31 dic 23:59:59Z: {n1}; 1 ene 00:30+01:00 (aún 31 dic en UTC): {n2}; 1 ene 00:00Z: {n3}")

# ---------------------------------------------------------------- J2: O-42 sin plazo de gracia: salta en el instante en que termina el mes
o = base(23, robot=lambda k: 900.0)
o.barrer(mes_k(24, "01T00:00:00")[1])
sonda("J2_O42_salta_en_el_mismo_instante_en_que_termina_el_mes", len(o42(o)) == 1,
      f"mes 24 ({mes_k(24)[0]}) sin comparar a las 00:00:00 del día 1 siguiente: {len(o42(o))} O-42 (MEDIA); sin plazo [PROPUESTO], "
      "cada mes en que I compare unas horas después del cierre habrá un O-42")

# ---------------------------------------------------------------- J3: varios meses sin comparar: un aviso por mes pendiente, no repetido, y ponerse al día
o = base(3)
for d in ("2027-04-01T06:00:00+00:00", "2027-04-15T06:00:00+00:00", "2027-05-01T06:00:00+00:00", "2027-06-01T06:00:00+00:00", "2027-06-02T06:00:00+00:00"):
    o.barrer(d)
meses_av = [a["motivo"].split("el mes ")[1][:7] for a in o42(o)]
# ponerse al día: 4 meses seguidos en el mismo instante
t = "2027-06-10T06:00:00+00:00"
rs = [o.comparar_sombra(mes_k(k)[0], 900.0, 100.0, 100.0, 100.0, 0.0, "I", t) for k in (4, 5, 6)]
o.barrer("2027-06-10T07:00:00+00:00")
tras = len(o42(o))
sonda("J3_O42_repetido_o_sin_poder_ponerse_al_dia", not (meses_av == ["2027-03"] and all(r["ok"] for r in rs) and tras == 1),
      f"O-42 por barrido de mar a may: {meses_av} (uno para el primer mes que falta, aunque al final falten 3: 2027-03 a 2027-05); "
      f"ponerse al día en el mismo instante: {[r['codigo'] for r in rs]}; O-42 tras ponerse al día: {tras}")

# ---------------------------------------------------------------- J4: el operador acusa el O-42 y el siguiente barrido lo repite
o = base(3)
o.barrer("2027-04-01T06:00:00+00:00")
av = o42(o)[0]["id"]
o.acusar_aviso(av, "OPERADOR", "2027-04-01T07:00:00+00:00")
for h in range(8, 12):
    o.barrer(f"2027-04-01T{h:02d}:00:00+00:00")
sonda("J4_tras_acusar_O42_se_repite_en_cada_barrido", len(o42(o)) > 2, f"{len(o42(o))} O-42 tras acusar el primero y 4 barridos")

# ---------------------------------------------------------------- J5: comparar un mes atrasado mezcla lo que pasó después del mes
# Mes 24 (2028-11): al cierre del mes el robot vale 99 000 y la sombra ~100 000 (el robot pierde). El 2028-12-02 el operador retira
# 50 000 (G lo replica en la sombra). I compara el mes 24 el 2028-12-03 con el valor del robot al cierre del mes (99 000).
def mes24(retirar, robot24):
    o = base(23, robot=100_000.0, inicio=100_000.0)
    if retirar:
        assert o.movimiento_sombra("RETIRADA", 50_000.0, 100.0, "OPERADOR", "2028-12-02T10:00:00+00:00")["ok"]
    r = o.comparar_sombra("2028-11", robot24, 100.0, 100.0, 100.0, 0.0, "I", "2028-12-03T10:00:00+00:00")
    return r, o


r_sin, _ = mes24(False, 99_000.0)
r_con, oc = mes24(True, 99_000.0)
sonda("J5_comparacion_atrasada_cuenta_movimientos_posteriores_al_mes", r_sin["veredicto"] != r_con["veredicto"],
      f"sin la retirada de diciembre: {r_sin['veredicto']} (robot 99 000, sombra {r_sin['resultado']['sombra_eur']:.0f}); con ella: "
      f"{r_con['veredicto']} (sombra {r_con['resultado']['sombra_eur']:.0f}); O-41: {sum(a['codigo'] == 'O-41' for a in oc.avisos)}")

# ---------------------------------------------------------------- J5c: y al revés: un aporte tras el cierre da un O-41 a un robot que gana
o = base(23, robot=100_000.0, inicio=100_000.0)
assert o.movimiento_sombra("APORTE", 50_000.0, 100.0, "OPERADOR", "2028-12-02T10:00:00+00:00")["ok"]
r = o.comparar_sombra("2028-11", 101_000.0, 100.0, 100.0, 100.0, 0.0, "I", "2028-12-03T10:00:00+00:00")
sonda("J5c_aporte_tras_el_cierre_da_O41_a_un_robot_que_gana", r["veredicto"] == "PROPONER_PASIVA",
      f"robot al cierre 101 000 (sombra al cierre ~99 585): {r['veredicto']}, sombra {r['resultado']['sombra_eur']:.0f}; "
      f"O-41: {sum(a['codigo'] == 'O-41' for a in o.avisos)}")

# ---------------------------------------------------------------- J5b: y el instante elegido para comparar mueve la sombra y los costes
o = base(23, robot=100_000.0, inicio=100_000.0)
o2 = copy.deepcopy(o)
r_pronto = o.comparar_sombra("2028-11", 99_950.0, 100.0, 100.0, 100.0, 0.0, "I", "2028-12-01T00:00:00+00:00")
r_tarde = o2.comparar_sombra("2028-11", 99_950.0, 100.0, 100.0, 100.0, 0.0, "I", "2029-11-30T00:00:00+00:00")
sonda("J5b_el_mes_24_comparado_un_anio_tarde_cambia_el_veredicto", r_pronto["veredicto"] != r_tarde["veredicto"],
      f"mismos datos del mes: el 1 dic {r_pronto['veredicto']} (sombra {r_pronto['resultado']['sombra_eur']:.2f}); un año tarde "
      f"{r_tarde['veredicto']} (sombra {r_tarde['resultado']['sombra_eur']:.2f}): la sombra paga coste hasta el día de la comparación")

# ---------------------------------------------------------------- J6: O-41 al pasar a no superarla, y otra vez si vuelve a pasar
seq = {24: 900.0, 25: 900.0, 26: 5000.0, 27: 900.0, 28: 900.0}
o = base(23, robot=5000.0)
vers = []
for k in range(24, 29):
    r = o.comparar_sombra(mes_k(k)[0], seq[k], 100.0, 100.0, 100.0, 0.0, "I", mes_k(k)[1])
    vers.append(r["veredicto"])
n41 = [a["motivo"][:7] for a in o.avisos if a["codigo"] == "O-41"]
sonda("J6_O41_mal_en_las_transiciones", n41 != [mes_k(24)[0], mes_k(27)[0]], f"veredictos {vers}; O-41 en {n41}")
o = base(23, robot=900.0)   # ya por debajo en EN_PLAZO: el mes 24 es la primera PROPONER_PASIVA
r = o.comparar_sombra(mes_k(24)[0], 900.0, 100.0, 100.0, 100.0, 0.0, "I", mes_k(24)[1])
sonda("J6b_sin_O41_si_ya_iba_por_debajo_antes_del_plazo", sum(a["codigo"] == "O-41" for a in o.avisos) != 1, f"{r['veredicto']}")

# ---------------------------------------------------------------- J7: H-05: con el registro tocado, O-13 y kill-switch antes de leerlo (los tres métodos)
fallos = []
toques = (("sin_ahora_en_el_inicio", lambda L: L["entradas"][0].pop("ahora")),
          ("sin_mes_en_una_comparacion", lambda L: L["entradas"][-1].pop("mes")),
          ("tipo_no_texto", lambda L: L["entradas"][-1].__setitem__("tipo", None)),
          ("inicio_cambiado_de_tipo", lambda L: L["entradas"][0].__setitem__("tipo", "X")),
          ("mes_al_futuro", lambda L: L["entradas"][-1].__setitem__("mes", "2099-01")),
          ("entradas_vaciadas", lambda L: L["entradas"].clear()),
          ("sin_clave_entradas", lambda L: L.pop("entradas")))
llamadas = (("comparar", lambda o: o.comparar_sombra(mes_k(3)[0], 900.0, 100.0, 100.0, 100.0, 0.0, "I", mes_k(3)[1])),
            ("movimiento", lambda o: o.movimiento_sombra("APORTE", 10.0, 100.0, "G", mes_k(3)[1])),
            ("iniciar", lambda o: o.iniciar_sombra(1000.0, 100.0, "OPERADOR", mes_k(3)[1])))
for nt, toque in toques:
    for nl, ll in llamadas:
        o = base(2)
        toque(o.sombra)
        r = ll(o)
        if not (r["codigo"] == "O-13" and o.kill is not None):
            fallos.append((nt, nl, r["codigo"], o.kill is not None))
sonda("J7_registro_tocado_sin_O13_ni_kill", bool(fallos), f"{fallos}")

# ---------------------------------------------------------------- J7b: barrer con el registro tocado: ¿se calla el O-42?
o = base(2)
o.sombra["entradas"][-1]["mes"] = "2099-01"
o.barrer(mes_k(5)[1])
sonda("J7b_registro_tocado_calla_el_O42_en_barrer", not o42(o) and o.kill is None,
      f"O-42: {len(o42(o))}; kill: {o.kill is not None}; integridad: {o.integridad()} (lo para el siguiente punto de decisión)")

# ---------------------------------------------------------------- J8: H-07: el índice de precios del inicio, fijo desde la primera comparación
o = base(1)
r_otro = o.comparar_sombra(mes_k(2)[0], 900.0, 100.0, 50.0, 100.0, 0.0, "I", mes_k(2)[1])
r_int = o.comparar_sombra(mes_k(2)[0], 900.0, 100.0, 100, 100.0, 0.0, "I", mes_k(2)[1])
sonda("J8_indice_del_inicio_cambia", r_otro["ok"] or not r_int["ok"], f"50 en vez de 100: {r_otro['codigo']}; 100 entero: {r_int['codigo']}")
o = base()
r1 = o.comparar_sombra(mes_k(1)[0], 900.0, 100.0, 1.0, 1000.0, 0.0, "I", mes_k(1)[1])
sonda("LIMITE_J8b_el_indice_del_inicio_lo_elige_la_primera_comparacion", r1["ok"],
      f"{r1['codigo']} inflación acumulada {(r1.get('resultado') or {}).get('inflacion_acumulada')} en un mes (no cambia el veredicto: real = nominal)")

# ---------------------------------------------------------------- J9: lo que I declara decide el juicio (H-07, límite)
o = base(23, robot=900.0)
r = o.comparar_sombra(mes_k(24)[0], 1e9, 100.0, 100.0, 100.0, 0.0, "I", mes_k(24)[1])
sonda("LIMITE_J9_el_valor_del_robot_lo_declara_I_sin_contraste", r["veredicto"] == "SUPERA", f"robot 1e9 EUR declarado: {r['veredicto']}")
o = base(23, robot=900.0)
r = o.comparar_sombra(mes_k(24)[0], 1000.0, 0.01, 100.0, 100.0, 0.0, "I", mes_k(24)[1])
sonda("LIMITE_J9b_el_precio_del_indice_lo_declara_I_sin_contraste", r["veredicto"] == "SUPERA", f"precio 0,01: {r['veredicto']}")

# ---------------------------------------------------------------- J10: H-09 (límite): vaciar o recortar el registro
o = base(24)
o.sombra = {"historial": [], "estado": "VIGENTE", "entradas": []}
vacio = o.integridad() == [] and o.sombra_ok()
r = o.iniciar_sombra(1000.0, 100.0, "OPERADOR", "2028-12-02T00:00:00+00:00")
sonda("LIMITE_J10_vaciar_el_registro_reinicia_el_plazo", vacio and r["ok"], f"integridad limpia {vacio}; nuevo inicio {r['codigo']}")

# ---------------------------------------------------------------- J11: gasto_dia: ¿puede entrar un coste negativo por la API? (H-07)
o = nuevo()
hasta(o, "EN_ANALISIS", 1)
rg = o.registrar_gasto("EV-ENC-0001", -1e6, 1.0, AHORA)
sonda("J11_registrar_gasto_acepta_negativo", rg["ok"], f"{rg['codigo']}")

# ---------------------------------------------------------------- J12: rechazos atómicos en comparar (mes sin terminar, índice distinto)
o = base(1)
antes = foto(o)
o.comparar_sombra(mes_k(2)[0], 900.0, 100.0, 100.0, 100.0, 0.0, "I", f"{mes_k(2)[0]}-28T00:00:00+00:00")
o.comparar_sombra(mes_k(2)[0], 900.0, 100.0, 99.0, 100.0, 0.0, "I", mes_k(2)[1])
o.comparar_sombra(mes_k(2)[0], 900.0, 1e308, 100.0, 100.0, 0.0, "I", mes_k(2)[1])
sonda("J12_un_rechazo_cambia_el_estado", foto(o) != antes, "")

print(f"\n{sum(1 for n, c in RES if c and not n.startswith('LIMITE'))} FALLA (sin contar límites) de {len(RES)} sondas")
