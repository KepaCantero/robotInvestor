"""QA r01 de T-97 (revisor nuevo sin contexto, Claude). CA-7 sobre un estado guardado de verdad con la V0.73
(r01_genera_estado_v073.py): MIG-010 en la cadena, claves nuevas con su valor de partida, valores personalizados intactos,
integridad, y qué pasa con una autorización de la V0.73 al enviar su orden con el código de hoy. También estados manipulados
o intermedios. Datos SIMULADOS.

Uso: python3 -I r01_migracion_v073.py <marco_comun_c de hoy> <estado_v073.json> <estado_v074.json>
"""
import copy
import json
import sys
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
import migraciones as mg  # noqa: E402
import persistencia as pe  # noqa: E402

texto = Path(sys.argv[2]).read_text(encoding="ascii")
AHORA = "2026-11-06T09:00:00+00:00"
fallos = 0


def chk(nombre, cond, detalle=""):
    global fallos
    print(("OK   " if cond else "FALLA"), nombre, "" if cond else detalle)
    fallos += 0 if cond else 1


antes = json.loads(texto)["estado"]["cfg"]
r = mg.migrar(texto, AHORA, "QA r01 de T-97: estado de la V0.73")
chk("migra_ok", r["ok"], r.get("motivo"))
print("   cadena:", r.get("migraciones"))
o = r["orquestador"]
chk("MIG010_en_la_cadena_y_solo_desde_V073", r["migraciones"][0] == "MIG-010")
chk("integridad_vacia", o.integridad() == [], o.integridad())
c = o.cfg
chk("claves_nuevas_con_su_valor", c["tope_anual_gasto_pct_capital"] == 0.5 and c["capital_referencia_eur"] is None
    and c["divisas_principales"] == ["USD", "GBP", "JPY", "CHF"] and c["tolerancia_tipo_k_rel_principales"] == 0.005
    and c["politica_f"]["importe_max_dia_pct"] == 25.0 and c["politica_f"]["perdida_semana_max_pct_trading"] == 4.0
    and c["politica_f"]["perdida_semana_max_pct_tactica"] == 5.0 and c["politica_f"]["perdida_semana_max_pct_largo_plazo"] == 5.0, c)
chk("valores_personalizados_intactos", c["politica_f"]["importe_max_dia_eur"] == 30000.0 and c["politica_f"]["perdida_semana_max_eur"] == 4000.0
    and c["tolerancia_tipo_k_rel"] == 0.2 and c["dia_coste_max_eur"] == 40.0 and c["nivel_autonomia"] == antes["nivel_autonomia"])
chk("ninguna_otra_clave_de_cfg_cambia", all(c[k] == v for k, v in antes.items() if k not in ("version_config", "politica_f"))
    and all(c["politica_f"][k] == v for k, v in antes["politica_f"].items()))
chk("version_config_CFG_0_12_0", c["version_config"] == "CFG-0.12.0", c["version_config"])
chk("gasto_y_expedientes_conservados", o.gasto_dia == json.loads(texto)["estado"]["gasto_dia"]
    and {k: v["estado"] for k, v in o.expedientes.items()} == {"EXP-0001": "AUTORIZADA", "EXP-0002": "COMPARADA"})

# la autorización de la V0.73 guarda la política de F de entonces, sin las claves en %
pol_aut = o.expedientes["EXP-0001"]["control_f"]["entradas"]["politica"]
print("   política guardada en la autorización tiene las claves nuevas:", "importe_max_dia_pct" in pol_aut)
r_env = o.orden_entrada("EXP-0001", "ORD-1", "ENVIADA", 0.0, "G", AHORA)
print("   envío de la orden autorizada en la V0.73, con el código de hoy:", r_env["ok"], r_env["codigo"], r_env["motivo"][:160])
# V0.46: una migración que cambia la configuración deja sin valor las autorizaciones anteriores (falla cerrado: vuelve a F)
chk("autorizacion_V073_no_se_envia_tras_migrar_vuelve_a_F", not r_env["ok"] and r_env["codigo"] == "O-05", r_env)

# idempotencia: aplicar _v074 dos veces no cambia nada más
e1 = mg._v074(copy.deepcopy(json.loads(texto)["estado"]))
e2 = mg._v074(copy.deepcopy(e1))
chk("MIG010_idempotente", e1 == e2)

# estado manipulado: subir a mano un límite en la copia guardada sin rehacer la huella
doc = json.loads(texto)
doc["estado"]["cfg"]["politica_f"]["perdida_semana_max_eur"] = 999999.0
r = mg.migrar(pe._texto(doc), AHORA, "QA r01: estado manipulado")
chk("estado_manipulado_no_migra", not r["ok"], r)
print("   manipulado:", r.get("codigo"), (r.get("motivo") or "")[:100])

# estado de la V0.73 que ya trae, a mano, una clave de la V0.74 más laxa (con la huella rehecha: lo que haría alguien con acceso)
doc = json.loads(texto)
doc["estado"]["cfg"]["politica_f"]["importe_max_dia_pct"] = 100.0
doc["estado"]["cfg"]["tolerancia_tipo_k_rel_principales"] = 0.2
doc["huella"] = pe._huella(doc["estado"])
r = mg.migrar(pe._texto(doc), AHORA, "QA r01: V0.73 con claves de la V0.74 ya puestas")
print("   V0.73 con claves V0.74 metidas a mano (huella rehecha):", r["ok"], r.get("codigo"), (r.get("motivo") or "")[:140])
if r["ok"]:
    print("     conserva importe_max_dia_pct =", r["orquestador"].cfg["politica_f"]["importe_max_dia_pct"])

# un estado ya migrado (V0.74/V0.76) vuelto a guardar y vuelto a migrar: no debe haber nada que migrar
t2 = pe.volcar(o, AHORA)
r = mg.migrar(t2, AHORA, "QA r01: estado ya en el esquema de hoy")
print("   estado de hoy otra vez por migrar:", r["ok"], r.get("codigo"), (r.get("motivo") or "")[:120], r.get("migraciones"))
r = pe.cargar(t2)
chk("estado_de_hoy_se_carga", r["ok"], r)

# un estado de hoy con la etiqueta de esquema de la V0.74 (manipulado): no se cuela
doc = json.loads(t2)
doc["esquema"] = mg.ESQUEMA_V0_74
r = mg.migrar(pe._texto(doc), AHORA, "QA r01: estado de hoy disfrazado de V0.74")
chk("estado_de_hoy_disfrazado_de_V074_no_migra", not r["ok"], r)

# un estado guardado de verdad con la V0.74 (intermedio, personalizado): solo MIG-011 y nada cambia
t74 = Path(sys.argv[3]).read_text(encoding="ascii")
a74 = json.loads(t74)["estado"]["cfg"]
r = mg.migrar(t74, AHORA, "QA r01: estado de la V0.74")
chk("estado_V074_solo_MIG011", r["ok"] and r["migraciones"] == ["MIG-011"], r.get("migraciones") or r)
if r["ok"]:
    c74 = r["orquestador"].cfg
    chk("estado_V074_conserva_sus_valores_personalizados", c74 == a74, {k: (a74.get(k), c74.get(k)) for k in c74 if a74.get(k) != c74.get(k)})
    chk("estado_V074_integridad", r["orquestador"].integridad() == [], r["orquestador"].integridad())

print("FALLOS:", fallos)
sys.exit(1 if fallos else 0)
