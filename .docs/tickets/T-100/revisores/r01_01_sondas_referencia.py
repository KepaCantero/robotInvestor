"""QA r01 de T-100 (V0.76): sondas del revisor contra la referencia obligatoria de los movimientos de la sombra (T-76 H-17) y el
barrido con el registro roto (T-76 H-19). Datos SIMULADOS.

Uso (desde la raíz del repositorio): .venv/bin/python -I .docs/tickets/T-100/revisores/r01_01_sondas_referencia.py [ruta del marco]
Cada sonda imprime BIEN (se comporta como dice el diseño), FALLA (un defecto) u OBSERVA (se comporta así a propósito o es un
límite: se anota para el informe). Termina con 0 siempre: es una sonda.
"""
import copy
import json
import sys
import tempfile
import unicodedata
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[4] / "sistema_global" / "marco_comun_c"
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
import diario as di  # noqa: E402
import migraciones as mg  # noqa: E402
import persistencia as pe  # noqa: E402
from pruebas_orquestador import AHORA, nuevo  # noqa: E402

RES = []
T1 = "2026-12-10T10:00:00+00:00"
T2 = "2026-12-10T11:00:00+00:00"
T3 = "2026-12-10T12:00:00+00:00"


def sonda(nombre, estado, detalle=""):
    RES.append((nombre, estado))
    print(f"{estado:7s} {nombre}  {str(detalle)[:500]}")


def base(inicio=100000.0):
    o = nuevo()
    assert o.iniciar_sombra(inicio, 100.0, "OPERADOR", AHORA)["ok"]
    return o


def movs(o):
    return [x for x in o.sombra["entradas"] if x["tipo"] in ("APORTE", "RETIRADA")]


def foto(o):
    return json.dumps(copy.deepcopy(o.__dict__), sort_keys=True, default=repr)


def cods(o):
    return [x["codigo"] for x in o.avisos]


# ------------------------------------------------------------------ S01: tipos raros de referencia (ninguno pasa ni cambia nada)
o = base()
f0 = foto(o)
raros = {"None": None, "int": 7, "float": 1.5, "bool": True, "bytes": b"INT-1", "lista": ["INT-1"], "dict": {"r": 1}, "vacia": "",
         "blancos": "   ", "tab_salto": "\t\n", "nbsp": " "}
malos = {}
for k, v in raros.items():
    r = o.movimiento_sombra("APORTE", 10.0, 100.0, "OPERADOR", T1, ref=v)
    if r["codigo"] != "O-01":
        malos[k] = r["codigo"]
sonda("S01_referencias_de_tipo_raro_o_vacias_dan_O01_y_no_tocan_nada", "BIEN" if not malos and foto(o) == f0 else "FALLA", malos)

# S01b: una referencia invisible (espacio de ancho cero, carácter nulo) no es «en blanco» para str.strip()
o = base()
r_zw = o.movimiento_sombra("APORTE", 10.0, 100.0, "OPERADOR", T1, ref="​")
r_nul = o.movimiento_sombra("APORTE", 10.0, 100.0, "OPERADOR", T2, ref="\x00")
sonda("S01b_referencias_invisibles_se_aceptan", "OBSERVA" if r_zw["ok"] or r_nul["ok"] else "BIEN",
      f"ZWSP={r_zw['codigo']} NUL={r_nul['codigo']}: str.strip() no quita U+200B ni NUL; se guardan como referencia válida")

# ------------------------------------------------------------------ S02: variantes de la misma referencia
o = base()
assert o.movimiento_sombra("APORTE", 50000.0, 100.0, "G", T1, ref="INT-0001")["ok"]
var = {"espacio_final": "INT-0001 ", "espacio_inicial": " INT-0001", "minusculas": "int-0001"}
rv = {k: o.movimiento_sombra("APORTE", 50000.0, 100.0, "OPERADOR", T2, ref=v)["codigo"] for k, v in var.items()}
sonda("S02_la_misma_referencia_con_espacios_o_mayusculas_cuenta_como_otro_movimiento",
      "FALLA" if len(movs(o)) > 1 else "BIEN",
      f"{rv}; aportes en la sombra: {len(movs(o))} (uno real, {len(movs(o)) - 1} repetido(s) por la grafía de la referencia)")
o = base()
nfc = unicodedata.normalize("NFC", "TRANSFERENCIA-ÑÚ-1")
nfd = unicodedata.normalize("NFD", nfc)
assert o.movimiento_sombra("APORTE", 50000.0, 100.0, "G", T1, ref=nfc)["ok"]
r = o.movimiento_sombra("APORTE", 50000.0, 100.0, "OPERADOR", T2, ref=nfd)
sonda("S02b_la_misma_referencia_en_NFC_y_en_NFD_cuenta_dos_veces", "FALLA" if len(movs(o)) > 1 else "BIEN",
      f"segunda (NFD)={r['codigo']}; aportes={len(movs(o))}")

# ------------------------------------------------------------------ S03: referencia muy larga
o = base()
largo = "R" * 1_000_000
r1 = o.movimiento_sombra("APORTE", 10.0, 100.0, "OPERADOR", T1, ref=largo)
r2 = o.movimiento_sombra("RETIRADA", 10.0, 100.0, "OPERADOR", T2, ref=largo)   # conflicto: O-03 con la referencia en el aviso
tam = max((len(x["motivo"]) for x in o.avisos if x["codigo"] == "O-03"), default=0)
try:
    v = pe.volcar(o, T3)
    vol = len(v)
except Exception as ex:  # noqa: BLE001
    vol = f"lanza {type(ex).__name__}"
sonda("S03_referencia_de_un_millon_de_caracteres", "OBSERVA" if r1["ok"] and tam > 10000 else "BIEN",
      f"primera={r1['codigo']} conflicto={r2['codigo']}; motivo del aviso O-03 con {tam} caracteres (sin recortar); volcado {vol} bytes")

# ------------------------------------------------------------------ S04: la misma referencia en APORTE y luego en RETIRADA
o = base()
assert o.movimiento_sombra("APORTE", 50000.0, 100.0, "G", T1, ref="INT-0002")["ok"]
n = len(o.sombra["entradas"])
r = o.movimiento_sombra("RETIRADA", 50000.0, 100.0, "OPERADOR", T2, ref="INT-0002")
sonda("S04_misma_referencia_aporte_y_retirada_es_O03_con_kill", "BIEN" if r["codigo"] == "O-03" and o.kill and len(o.sombra["entradas"]) == n
      and "O-03" in cods(o) and "O-26" in cods(o) else "FALLA", (r["codigo"], o.kill, cods(o)))

# ------------------------------------------------------------------ S05: importes casi iguales, enteros, NaN
o = base()
assert o.movimiento_sombra("APORTE", 50000.0, 100.0, "G", T1, ref="INT-0003")["ok"]
r_int = o.movimiento_sombra("APORTE", 50000, 100.0, "OPERADOR", T2, ref="INT-0003")
sonda("S05_el_mismo_importe_como_entero_es_duplicado", "BIEN" if r_int["codigo"] == "O-02" and o.kill is None else "FALLA", r_int["codigo"])
o2 = copy.deepcopy(o)
import math  # noqa: E402
casi = math.nextafter(50000.0, math.inf)
r_ulp = o2.movimiento_sombra("APORTE", casi, 100.0, "OPERADOR", T2, ref="INT-0003")
r_cent = copy.deepcopy(o).movimiento_sombra("APORTE", 50000.001, 100.0, "OPERADOR", T2, ref="INT-0003")
sonda("S05b_un_importe_que_difiere_en_el_ultimo_decimal_es_O03_con_kill", "OBSERVA",
      f"un ulp más={r_ulp['codigo']} (kill={o2.kill is not None}); +0,001 EUR={r_cent['codigo']}: la igualdad es exacta, por diseño")
o3 = copy.deepcopy(o)
f0 = foto(o3)
rn = [o3.movimiento_sombra("APORTE", v, 100.0, "OPERADOR", T2, ref="INT-0003")["codigo"] for v in (float("nan"), float("inf"), None, "50000", True)]
sonda("S05c_NaN_inf_None_texto_bool_con_referencia_existente_dan_O01_sin_kill", "BIEN" if set(rn) == {"O-01"} and o3.kill is None
      and foto(o3) == f0 else "FALLA", rn)
o4 = copy.deepcopy(o)
r_pr = o4.movimiento_sombra("APORTE", 50000.0, float("nan"), "OPERADOR", T2, ref="INT-0003")
sonda("S05d_duplicado_con_precio_NaN_da_O01_no_O02", "BIEN" if r_pr["codigo"] == "O-01" else "FALLA", r_pr["codigo"])

# ------------------------------------------------------------------ S06: el orden y el reloj
o = base()
assert o.movimiento_sombra("APORTE", 50000.0, 100.0, "G", T2, ref="INT-0004")["ok"]
r_dup_antes = o.movimiento_sombra("APORTE", 50000.0, 100.0, "OPERADOR", T1, ref="INT-0004")
r_conf_antes = o.movimiento_sombra("RETIRADA", 50000.0, 100.0, "OPERADOR", T1, ref="INT-0004")
sonda("S06_duplicado_o_conflicto_con_un_instante_anterior_da_O16", "OBSERVA" if r_dup_antes["codigo"] == "O-16" else "FALLA",
      f"duplicado anterior={r_dup_antes['codigo']}; conflicto anterior={r_conf_antes['codigo']} (kill={o.kill is not None}): el reloj se mira "
      "antes que la referencia, así que un conflicto con un instante anterior no se ve como incidente")
o = base()
assert o.movimiento_sombra("APORTE", 50000.0, 100.0, "G", T1, ref="INT-0005")["ok"]
u0 = o.ultimo_ahora
r = o.movimiento_sombra("APORTE", 50000.0, 100.0, "OPERADOR", T3, ref="INT-0005")
sonda("S06b_un_duplicado_O02_adelanta_el_reloj", "OBSERVA" if o.ultimo_ahora == T3 else "BIEN",
      f"{r['codigo']} ok={r['ok']}; reloj {u0} -> {o.ultimo_ahora} (como los demás O-02 que devuelven ok)")

# S07: tras un O-03 rechazado bajo @_seguro: reloj, avisos y kill-switch
o = base()
assert o.movimiento_sombra("APORTE", 50000.0, 100.0, "G", T1, ref="INT-0006")["ok"]
r = o.movimiento_sombra("RETIRADA", 50000.0, 100.0, "OPERADOR", T3, ref="INT-0006")
reloj = o.ultimo_ahora
kill_t = o.kill and o.kill["ahora"]
r_desp = o.movimiento_sombra("APORTE", 10.0, 100.0, "OPERADOR", T2, ref="INT-0007")   # entre el último instante y el del O-03
avisos_desordenados = [x["ahora"] for x in o.avisos] != sorted([x["ahora"] for x in o.avisos])
sonda("S07_el_O03_deja_aviso_y_kill_pero_el_reloj_vuelve_atras", "OBSERVA" if reloj == T1 else "BIEN",
      f"O-03 a las {T3[11:16]}: reloj tras el rechazo={reloj[11:16]}, kill en {kill_t and kill_t[11:16]}; un movimiento a las {T2[11:16]} "
      f"después da {r_desp['codigo']}; avisos fuera de orden={avisos_desordenados}; integridad={o.integridad()}")
r_rep = o.movimiento_sombra("RETIRADA", 50000.0, 100.0, "OPERADOR", T3, ref="INT-0006")
sonda("S07b_repetir_el_conflicto_no_multiplica_avisos", "BIEN" if cods(o).count("O-03") == 1 and cods(o).count("O-26") == 1 else "FALLA",
      (r_rep["codigo"], cods(o)))
sonda("S07c_con_el_kill_activo_se_siguen_replicando_movimientos", "BIEN" if r_desp["ok"] else "OBSERVA", r_desp["codigo"])

# S07d: comparación con el event_id repetido (el modelo del diseño): ¿también vuelve el reloj atrás?
import inspect  # noqa: E402
import orquestador as oq  # noqa: E402
src = inspect.getsource(oq.Orquestador._duplicado)
sonda("S07d_el_O03_del_event_id_tampoco_fija_el_reloj", "OBSERVA" if "reloj_firme" not in src else "BIEN",
      "el _duplicado de los event_id devuelve _no(O-03) sin reloj_firme: el comportamiento es el mismo que el de la sombra")

# ------------------------------------------------------------------ S08: persistencia con entradas con y sin ref
o = base()
o._anota_sombra({"tipo": "APORTE", "importe_eur": 10.0, "precio_indice": 100.0, "ahora": AHORA}, "OPERADOR", AHORA)   # como la V0.75
assert o.movimiento_sombra("APORTE", 50000.0, 100.0, "G", T1, ref="INT-0008")["ok"]
c = pe.cargar(pe.volcar(o, T1))
oc = c.get("orquestador")
ok = c.get("ok") and oc is not None and oc.integridad() == [] and oc.sombra == o.sombra
r_dup = oc.movimiento_sombra("APORTE", 50000.0, 100.0, "OPERADOR", T2, ref="INT-0008") if oc else {"codigo": None}
r_conf = copy.deepcopy(oc).movimiento_sombra("APORTE", 1.0, 100.0, "OPERADOR", T2, ref="INT-0008") if oc else {"codigo": None}
sonda("S08_volcar_y_cargar_conserva_las_referencias_y_el_duplicado_se_sigue_viendo",
      "BIEN" if ok and r_dup["codigo"] == "O-02" and r_conf["codigo"] == "O-03" else "FALLA", (c.get("codigo"), r_dup["codigo"], r_conf["codigo"]))
o5 = copy.deepcopy(o)
o5.sombra["entradas"][-1]["ref"] = "INT-OTRA"
o6 = copy.deepcopy(o)
o6.sombra["entradas"][-1].pop("ref")
o7 = copy.deepcopy(o)
o7.sombra["entradas"][1]["ref"] = "INT-0008"   # añadir a la entrada antigua la misma referencia
sonda("S08b_tocar_la_referencia_guardada_lo_detecta_integridad", "BIEN" if all("SOMBRA" in x.integridad() for x in (o5, o6, o7)) else "FALLA",
      [x.integridad() for x in (o5, o6, o7)])
r = o5.movimiento_sombra("APORTE", 50000.0, 100.0, "G", T2, ref="INT-OTRA")
sonda("S08c_con_la_referencia_tocada_el_movimiento_da_O13", "BIEN" if r["codigo"] == "O-13" and o5.kill else "FALLA", r["codigo"])

# ------------------------------------------------------------------ S09: el diario reproduce duplicados y conflictos
with tempfile.TemporaryDirectory() as d:
    o = base()
    re_, rd = str(Path(d) / "e.json"), str(Path(d) / "d.log")
    D = di.crear(o, re_, rd, AHORA)["diario"]
    a = D.movimiento_sombra("APORTE", 50000.0, 100.0, "G", T1, ref="INT-0009")
    b = D.movimiento_sombra("APORTE", 50000.0, 101.0, "OPERADOR", T2, ref="INT-0009")
    cc = D.movimiento_sombra("RETIRADA", 50000.0, 100.0, "OPERADOR", T3, ref="INT-0009")
    dd = D.movimiento_sombra("APORTE", 5.0, 100.0, "OPERADOR", T2, ref="INT-0010")
    vivo = foto(o)
    r2 = di.abrir(re_, rd)
    o2 = r2["diario"].orquestador if r2.get("diario") is not None else None
    sonda("S09_el_diario_reproduce_duplicado_conflicto_y_kill", "BIEN" if r2.get("ok") and o2 is not None and foto(o2) == vivo else "FALLA",
          f"{a['codigo']} {b['codigo']} {cc['codigo']} {dd['codigo']}; abrir={r2.get('codigo')} igual={o2 is not None and foto(o2) == vivo}")

# ------------------------------------------------------------------ S10: el barrido con el registro roto
o = base(1000.0)
o.sombra["entradas"][0]["importe_eur"] = 1.0
r1 = o.barrer("2027-03-10T00:00:00+00:00")
r2 = o.barrer("2027-03-11T00:00:00+00:00")
r3 = o.barrer("2027-03-12T00:00:00+00:00")
cs = cods(o)
sonda("S10_tres_barridos_con_el_registro_roto_no_multiplican_avisos",
      "BIEN" if cs.count("O-13") == 1 and cs.count("O-26") == 1 and "O-42" not in cs and "O-44" not in cs and o.kill["motivo"] == "integridad rota en SOMBRA"
      else "FALLA", (cs, [x[0] for x in r1["cambios"]], [x[0] for x in r2["cambios"]], [x[0] for x in r3["cambios"]]))
o = base(1000.0)
assert o.activar_kill_switch("prueba previa del operador", "OPERADOR", "2027-03-09T00:00:00+00:00")["ok"]
o.sombra["entradas"][0]["importe_eur"] = 1.0
o.barrer("2027-03-10T00:00:00+00:00")
sonda("S10b_un_kill_ya_activo_no_se_pisa", "BIEN" if o.kill["motivo"] == "prueba previa del operador" and "O-13" in cods(o) else "FALLA", o.kill)
o = base(1000.0)
o.sombra["entradas"][0]["importe_eur"] = 1.0
o.barrer("2027-03-10T00:00:00+00:00")
for av in o.avisos:
    if av["codigo"] == "O-13":
        av["acuse"] = {"actor": "OPERADOR", "ahora": "2027-03-10T01:00:00+00:00"}
o.barrer("2027-03-11T00:00:00+00:00")
sonda("S10c_tras_acusar_el_O13_el_siguiente_barrido_vuelve_a_avisar", "BIEN" if cods(o).count("O-13") == 2 else "FALLA", cods(o))
# Otros registros rotos: el barrido no los mira (fuera del alcance de H-19, que es la sombra)
o = base(1000.0)
o.consultas["entradas"].append({"x": 1})
o.barrer("2027-01-03T00:00:00+00:00")
sonda("S10d_con_otro_registro_roto_barrer_no_para", "OBSERVA" if o.kill is None else "BIEN",
      f"integridad={o.integridad()}; kill={o.kill is not None}; avisos={cods(o)}: H-19 solo trata la sombra; para los demás registros "
      "para el siguiente punto de decisión")
# Con la sombra íntegra, barrer sigue avisando de lo pendiente (H-04/H-13 no se rompen)
o = base(1000.0)
o.barrer("2027-01-06T00:00:00+00:00")
sonda("S10e_con_la_sombra_integra_lo_pendiente_se_sigue_avisando", "BIEN" if "O-42" in cods(o) and o.kill is None else "FALLA", cods(o))

# ------------------------------------------------------------------ S11: el esquema y la migración
sonda("S11_el_esquema_del_codigo_es_el_de_la_V075", "BIEN" if pe.esquema_actual() == mg.ESQUEMA_V0_75 else "FALLA",
      (pe.esquema_actual()[:12], mg.ESQUEMA_V0_75[:12]))
ultimo = mg.MIGRACIONES[-1]
sonda("S11b_la_ultima_migracion_sigue_siendo_MIG011_y_declara_H20", "BIEN" if ultimo.id == "MIG-011" and "V0.73 y la V0.74" in ultimo.descripcion
      else "FALLA", ultimo.id)

print()
print(f"{sum(e == 'BIEN' for _, e in RES)} BIEN, {sum(e == 'FALLA' for _, e in RES)} FALLA, {sum(e == 'OBSERVA' for _, e in RES)} OBSERVA")
print("FALLA:", [n for n, e in RES if e == "FALLA"])
