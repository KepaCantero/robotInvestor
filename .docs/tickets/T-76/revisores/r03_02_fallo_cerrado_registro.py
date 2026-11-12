"""QA r03 de T-76 (V0.75): fallo cerrado con NaN, inf, None y tipos raros; idempotencia y orden; registro manipulado; barrer() con
el registro roto; prioridad y repetición de O-42 y O-44. Datos SIMULADOS.

Uso: python3 -I .docs/tickets/T-76/revisores/r03_02_fallo_cerrado_registro.py [ruta del marco]
Cada sonda imprime FALLA (el defecto existe) o BIEN (el código se comporta como debe). Las que llevan «LIMITE» miden un límite
declarado: FALLA quiere decir que el límite sigue ahí. Termina con 0 siempre: es una sonda.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[4] / "sistema_global" / "marco_comun_c"
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
import orquestador as oq  # noqa: E402
import persistencia as pe  # noqa: E402
from parametros import PARAMETROS  # noqa: E402
from pruebas_orquestador import AHORA, nuevo  # noqa: E402

RES = []
NAN, INF = float("nan"), float("inf")
G = PARAMETROS["i_dias_gracia_comparacion_sombra"]


def sonda(nombre, falla, detalle=""):
    RES.append((nombre, falla))
    print(f"{'FALLA' if falla else 'BIEN':6s} {nombre}  {str(detalle)[:400]}")


def foto(o):
    return json.dumps(copy.deepcopy(o.__dict__), sort_keys=True, default=repr)


def mes_k(k, dia="02T06:00:00"):
    a, m = 2026 + (10 + k) // 12, (10 + k) % 12 + 1
    a2, m2 = 2026 + (11 + k) // 12, (11 + k) % 12 + 1
    return f"{a:04d}-{m:02d}", f"{a2:04d}-{m2:02d}-{dia}+00:00"


def base(n=0, inicio=1000.0):
    o = nuevo()
    assert o.iniciar_sombra(inicio, 100.0, "OPERADOR", AHORA)["ok"]
    for k in range(1, n + 1):
        mes, t = mes_k(k)
        assert o.comparar_sombra(mes, 1000.0, 100.0, 100.0, 100.0, 0.0, "I", t)["ok"]
    return o


class Raro(float):
    """Un float que miente al compararse."""
    def __gt__(self, o):
        return True


# ------------------------------------------------------------------ F1: valores raros en los tres métodos; ningún rechazo cambia el estado
raros = [NAN, INF, -INF, None, "100", b"1", True, False, 0, -1.0, 1e-320, 10 ** 400, complex(1, 0), [100.0], {"v": 1}, Raro(1.0)]
malos = []
for v in raros:
    o = nuevo()
    f0 = foto(o)
    r = o.iniciar_sombra(v, 100.0, "OPERADOR", AHORA)
    r2 = o.iniciar_sombra(1000.0, v, "OPERADOR", AHORA)
    if (r["ok"] or r2["ok"]) and not (isinstance(v, (int, float)) and not isinstance(v, bool) and 0 < v < INF):
        malos.append(("iniciar", repr(v)[:20], r["codigo"], r2["codigo"]))
    if not r["ok"] and not r2["ok"] and foto(o) != f0:
        malos.append(("iniciar_cambia", repr(v)[:20]))
    o = base(0)
    f0 = foto(o)
    for args in ((v, 10.0, 100.0), ("APORTE", v, 100.0), ("RETIRADA", 10.0, v)):
        r = o.movimiento_sombra(*args, "OPERADOR", "2026-11-07T00:00:00+00:00")
        if r["ok"] and args[0] in (v,) and not isinstance(v, str):
            malos.append(("movimiento_tipo", repr(v)[:20], r["codigo"]))
        if r["ok"] and not (isinstance(v, (int, float)) and not isinstance(v, bool) and 0 < v < INF) and args[0] != v:
            malos.append(("movimiento", repr(v)[:20], r["codigo"]))
        if r["ok"]:
            o = base(0); f0 = foto(o)
        elif foto(o) != f0:
            malos.append(("movimiento_cambia", repr(v)[:20], r["codigo"]))
    o = base(0)
    f0 = foto(o)
    for i in range(6):
        args = ["2026-12", 1000.0, 100.0, 100.0, 100.0, 0.0]
        args[i] = v
        r = o.comparar_sombra(*args, "I", "2027-01-02T00:00:00+00:00")
        if r["ok"] and i == 0:
            malos.append(("comparar_mes", repr(v)[:20]))
        elif r["ok"] and not (isinstance(v, (int, float)) and not isinstance(v, bool) and (0 <= v < INF if i in (1, 5) else 0 < v < INF)):
            malos.append(("comparar", i, repr(v)[:20], r["codigo"]))
        if r["ok"]:
            o = base(0); f0 = foto(o)
        elif foto(o) != f0:
            malos.append(("comparar_cambia", i, repr(v)[:20], r["codigo"]))
sonda("F1_valores_raros_pasan_o_cambian_el_estado", bool(malos), malos)

# F1b: meses mal escritos
o = base(0)
f0 = foto(o)
rs = {m: o.comparar_sombra(m, 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-01-02T00:00:00+00:00")["codigo"]
      for m in ("2026-12 ", " 2026-12", "2026-12\n", "2026-1", "2026-012", "２０２６-１２", "2026/12", "2026-00", "2026-13", 202612, None)}
sonda("F1b_meses_mal_escritos", any(c == "OK" for c in rs.values()) or foto(o) != f0, rs)

# F1c: actores con variantes
o = base(0)
f0 = foto(o)
rs = [o.comparar_sombra("2026-12", 1000.0, 100.0, 100.0, 100.0, 0.0, a, "2027-01-02T00:00:00+00:00")["codigo"] for a in ("i", " I", "I ", "Ｉ", None, "OPERADOR", "G")]
rs += [o.movimiento_sombra("APORTE", 1.0, 100.0, a, "2027-01-02T00:00:00+00:00")["codigo"] for a in ("g", "G ", "operador", "I", "ORQUESTADOR", None)]
rs += [nuevo().iniciar_sombra(1000.0, 100.0, a, AHORA)["codigo"] for a in ("operador", "G", "ORQUESTADOR", "I")]
sonda("F1c_actores_ajenos_o_mal_escritos", set(rs) != {"O-05"} or foto(o) != f0, rs)

# F1d: el reloj: un movimiento o una comparación con un instante anterior al último no entra y deja el estado igual
o = base(1)
f0 = foto(o)
r1 = o.movimiento_sombra("APORTE", 10.0, 100.0, "OPERADOR", "2026-12-15T00:00:00+00:00")   # antes de la comparación de diciembre
r2 = o.comparar_sombra("2027-01", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-01-01T00:00:00+00:00")
sonda("F1d_reloj_hacia_atras", not (r1["codigo"] == "O-16" and r2["codigo"] in ("O-16", "O-01") and foto(o) == f0), f"{r1['codigo']} {r2['codigo']}")

# ------------------------------------------------------------------ F2: idempotencia de los movimientos (el mismo aporte declarado dos veces)
o = base(0, inicio=100000.0)
r1 = o.movimiento_sombra("APORTE", 50000.0, 100.0, "G", "2026-12-10T10:00:00+00:00")
r2 = o.movimiento_sombra("APORTE", 50000.0, 100.0, "OPERADOR", "2026-12-10T10:00:00+00:00")   # el operador declara el mismo aporte que vio G
r3 = o.movimiento_sombra("APORTE", 50000.0, 100.0, "G", "2026-12-10T10:00:00+00:00")          # G lo reenvía tras un corte
n = len([x for x in o.sombra["entradas"] if x["tipo"] == "APORTE"])
sonda("F2_el_mismo_movimiento_dos_veces_se_cuenta_dos_veces", n != 1, f"{r1['codigo']} {r2['codigo']} {r3['codigo']}: {n} aportes de 50 000 anotados (la cartera real recibió uno)")
# consecuencia en el juicio: robot = cartera real con un aporte de 50 000 y un 0,5 % de rentabilidad
o = base(0, inicio=100000.0)
assert o.movimiento_sombra("APORTE", 50000.0, 100.0, "G", "2026-12-10T10:00:00+00:00")["ok"]
assert o.movimiento_sombra("APORTE", 50000.0, 100.0, "G", "2026-12-10T10:00:00+00:00")["ok"]
for k in range(1, 25):
    mes, t = mes_k(k)
    r = o.comparar_sombra(mes, 150750.0, 100.0, 100.0, 100.0, 0.0, "I", t)
sonda("F2b_un_aporte_repetido_da_la_vuelta_al_juicio", r["veredicto"] == "PROPONER_PASIVA",
      f"mes 24: robot 150 750 frente a sombra {r['resultado']['sombra_eur']:.2f}: {r['veredicto']}, O-41 {sum(a['codigo'] == 'O-41' for a in o.avisos)}")

# F2c: repetir la comparación de un mes (O-02, duplicado) y comparar en otro orden
o = base(2)
f0 = foto(o)
rr = [o.comparar_sombra(mes_k(k)[0], 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-03-05T00:00:00+00:00")["codigo"] for k in (1, 2, 4)]
sonda("F2c_repetir_o_saltar_meses", rr != ["O-02", "O-02", "O-01"] or foto(o) != f0, rr)

# ------------------------------------------------------------------ F3: registro manipulado: cada toque se detecta, y los tres métodos dan O-13 con kill-switch
def toques():
    yield "ahora_de_un_movimiento", lambda L: L["entradas"][1].__setitem__("ahora", "2026-12-31T23:59:59+00:00")
    yield "importe_de_un_movimiento", lambda L: L["entradas"][1].__setitem__("importe_eur", 1.0)
    yield "mes_de_una_comparacion", lambda L: L["entradas"][-1].__setitem__("mes", "2027-05")
    yield "veredicto", lambda L: L["entradas"][-1].__setitem__("veredicto", "SUPERA")
    yield "estado_del_registro", lambda L: L.__setitem__("estado", "CERRADO")
    yield "orden_de_dos_entradas", lambda L: L["entradas"].__setitem__(slice(1, 3), [L["entradas"][2], L["entradas"][1]])
    yield "historial_sin_la_ultima", lambda L: L["historial"].pop()
    yield "entradas_None", lambda L: L.__setitem__("entradas", None)
    yield "sombra_lista", None
    yield "tipo_desconocido", lambda L: L["entradas"][1].__setitem__("tipo", "DIVIDENDO")
no_detectados, sin_kill = [], []
for nombre, toque in toques():
    for metodo in ("iniciar", "movimiento", "comparar", "barrer"):
        o = base(0)
        assert o.movimiento_sombra("APORTE", 10.0, 100.0, "OPERADOR", "2026-11-20T00:00:00+00:00")["ok"]
        assert o.comparar_sombra("2026-12", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-01-02T00:00:00+00:00")["ok"]
        if toque is None:
            o.sombra = []
        else:
            toque(o.sombra)
        if "SOMBRA" not in o.integridad():
            no_detectados.append((nombre, "integridad"))
            break
        t = "2027-02-10T00:00:00+00:00"
        r = {"iniciar": lambda: o.iniciar_sombra(1000.0, 100.0, "OPERADOR", t),
             "movimiento": lambda: o.movimiento_sombra("APORTE", 10.0, 100.0, "G", t),
             "comparar": lambda: o.comparar_sombra("2027-01", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", t),
             "barrer": lambda: o.barrer(t)}[metodo]()
        if metodo == "barrer":
            if not any(a["codigo"] == "O-13" and "sombra" in a["motivo"] for a in o.avisos):
                no_detectados.append((nombre, "barrer", r["codigo"]))
        elif not (r["codigo"] == "O-13" and o.kill is not None):
            sin_kill.append((nombre, metodo, r["codigo"]))
sonda("F3_un_toque_del_registro_sin_O13_o_sin_kill", bool(no_detectados or sin_kill), {"no_detectados": no_detectados, "sin_kill": sin_kill})

# F3b: barrer() con el registro roto avisa con O-13, pero sigue calculando lo pendiente con el registro roto
o = base(0)
o.sombra["entradas"][0]["ahora"] = "2020-01-01T00:00:00+00:00"   # el inicio, retrasado casi siete años
r = o.barrer("2027-01-10T00:00:00+00:00")
cods = [(a["codigo"], a["motivo"][:80]) for a in o.avisos if a["codigo"] in ("O-13", "O-42", "O-44")]
sonda("F3b_con_el_registro_roto_barrer_avisa_tambien_de_lo_pendiente_leido_del_registro_roto",
      any(c in ("O-42", "O-44") for c, _ in cods), f"{cods}; kill {o.kill is not None}")

# F3c: barrer() con el registro roto no activa el kill-switch (los tres métodos que escriben sí)
o = base(0)
o.sombra["entradas"][0]["importe_eur"] = 1.0
o.barrer("2026-12-10T00:00:00+00:00")
sonda("F3c_barrer_con_el_registro_roto_no_activa_el_kill_switch", o.kill is None,
      f"O-13 {sum(a['codigo'] == 'O-13' for a in o.avisos)}, kill {o.kill}; integridad {o.integridad()}")

# F3d (LIMITE T-02): reescribir el registro con sus huellas recalculadas no se detecta
o = base(3)
L = o.sombra
L["entradas"][2]["veredicto"] = "SUPERA"
hs = []
for i, (h, x) in enumerate(zip(L["historial"], L["entradas"])):
    h["datos"] = oq._hash(x)
    h["hash_prev"] = L["historial"][i - 1]["hash"] if i else "0" * 64
    h["hash"] = oq._hash({k: v for k, v in h.items() if k != "hash"})
sonda("F3d_LIMITE_reescribir_con_las_huellas_recalculadas", o.sombra_ok() and o.integridad() == [],
      f"sombra_ok {o.sombra_ok()}, integridad {o.integridad()} (límite T-02: sin ancla externa)")

# ------------------------------------------------------------------ F4: persistencia: la cabeza SOMBRA, volcar/cargar con un toque en el texto
o = base(3)
t = pe.volcar(o, "2027-03-05T00:00:00+00:00")
c = pe.cargar(t)
d = json.loads(t)
s = json.dumps(d)
d2 = json.loads(s)
txt = json.dumps(d2)
toc = t.replace('"veredicto":"EN_PLAZO"', '"veredicto":"SUPERA"', 1)
c2 = pe.cargar(toc)
sonda("F4_volcar_cargar_y_toque_en_el_texto", not (c["ok"] and c["orquestador"].sombra == o.sombra and toc != t and not (c2["ok"] and c2["orquestador"].integridad() == [])),
      f"carga {c['codigo']}; con el veredicto cambiado en el texto: {c2['codigo']} {c2.get('motivo', '')[:80]}")

# ------------------------------------------------------------------ F5: lectura: comparaciones_sombra_pendientes con argumentos raros solo lee y no lanza
o = base(0)
f0 = foto(o)
out = {}
for g in (NAN, INF, -5, None, "5", 0, 10 ** 6):
    try:
        out[repr(g)] = o.comparaciones_sombra_pendientes("2027-03-10T00:00:00+00:00", g)
    except Exception as e:   # noqa: BLE001
        out[repr(g)] = f"EXC {type(e).__name__}"
for a in ("ayer", None, 5, "2027-03-10"):
    try:
        out[repr(a)] = o.comparaciones_sombra_pendientes(a)
    except Exception as e:   # noqa: BLE001
        out[repr(a)] = f"EXC {type(e).__name__}"
sonda("F5_pendientes_con_argumentos_raros_lanza_o_cambia", any(isinstance(v, str) and v.startswith("EXC") for v in out.values()) or foto(o) != f0, out)
far = o.comparaciones_sombra_pendientes("9999-12-31T23:59:59+00:00")
sonda("F5b_LIMITE_con_una_fecha_absurda_no_hay_aviso", far is None, f"en 9999: {far}")

# ------------------------------------------------------------------ F6: prioridad de O-42/O-44 en el catálogo y en PRIORIDAD_AVISO; textos
import catalogo_codigos as cc  # noqa: E402
cat = {k[1]: v for k, v in cc.CATALOGO.items() if k[0] == "orquestador"} if hasattr(cc, "CATALOGO") else {}
pr = {c: (oq.PRIORIDAD_AVISO.get(c), cat.get(c, {}).get("prioridad")) for c in ("O-41", "O-42", "O-44", "O-13")}
sonda("F6_prioridades_O41_O42_O44_coherentes", pr != {"O-41": ("ALTA", "ALTA"), "O-42": ("MEDIA", "MEDIA"), "O-44": ("ALTA", "ALTA"), "O-13": ("ALTA", "ALTA")}, pr)

# ------------------------------------------------------------------ F7: informe_sombra devuelve copias y no lanza con el registro roto
o = base(2)
i1 = o.informe_sombra()
i1["inicio"]["importe_eur"] = 0.0
i1["ultima"]["veredicto"] = "X"
ok_copia = o.sombra_ok()
o.sombra = {"historial": [], "estado": "VIGENTE", "entradas": [{"tipo": "COMPARACION"}]}
try:
    i2 = o.informe_sombra()
    exc = None
except Exception as e:   # noqa: BLE001
    exc = type(e).__name__
sonda("F7_informe_copias_y_no_lanza", not (ok_copia and exc is None), f"copia {ok_copia}; con registro raro: {exc or 'sin excepción'}")

# ------------------------------------------------------------------ F8: un fallo a mitad de comparar_sombra deja el estado intacto
o = base(1)
f0 = foto(o)
orig = oq.Orquestador._anota_sombra
def roto(self, entrada, actor, ahora):
    self.sombra["entradas"].append(entrada)
    raise TypeError("fallo simulado a mitad de la anotación")
oq.Orquestador._anota_sombra = roto
r = o.comparar_sombra("2027-01", 1000.0, 100.0, 100.0, 100.0, 0.0, "I", "2027-02-02T06:00:00+00:00")
r2 = o.movimiento_sombra("APORTE", 10.0, 100.0, "G", "2027-02-02T07:00:00+00:00")
oq.Orquestador._anota_sombra = orig
sonda("F8_fallo_a_mitad_deja_el_estado_intacto", not (r["codigo"] == "O-00" and r2["codigo"] == "O-00" and foto(o) == f0), f"{r['codigo']} {r2['codigo']}; estado igual {foto(o) == f0}")

# ------------------------------------------------------------------ F9: un resultado no finito de la comparación (H-03) se rechaza sin anotar
o = base(0)
f0 = foto(o)
rs = [o.comparar_sombra("2026-12", 1e308, 100.0, 1e10, 1e-300, 0.0, "I", "2027-01-02T00:00:00+00:00")["codigo"],
      o.comparar_sombra("2026-12", 1000.0, 1e308, 1.0, 1.0, 0.0, "I", "2027-01-02T00:00:00+00:00")["codigo"]]
sonda("F9_comparacion_no_finita_se_rechaza", rs != ["O-01", "O-01"] or foto(o) != f0, rs)
# F9b: la regresión H-03 de la batería ya no compara nada: su inicio (1e200 / 1e-200) lo rechaza ahora H-11
o8 = nuevo()
r8 = o8.iniciar_sombra(1e200, 1e-200, "OPERADOR", AHORA)
sonda("F9b_la_regresion_H03_de_la_bateria_es_vacia", not r8["ok"] and not o8.sombra["entradas"],
      f"iniciar(1e200, 1e-200): {r8['codigo']}; entradas {len(o8.sombra['entradas'])}: la prueba toma la rama «{{'codigo': 'O-01', 'ok': False}}» sin llamar a comparar_sombra")

print(f"\n{sum(1 for _, c in RES if c)} FALLA de {len(RES)} sondas")
