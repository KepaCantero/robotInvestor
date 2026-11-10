"""QA r04 · sonda 02: la corrección de H-13 en cadenas de varios DIRECTA, con consultas, y sin cerrar de más. (Datos SIMULADOS.)
  a) cadena: EXP-DD-01 descartado por el operador; EXP-DD-02 reutiliza S1, propone, caduca y se reanaliza: ¿EXP-DD-03 con S1? O-06
  b) un DIRECTA que se reencarga pero su encargo caduca sin sobre (sigue teniendo S1): O-06 (cerrado: se volvió a encargar)
  c) el análisis nuevo S2 de un DIRECTA reanalizado SÍ se reutiliza (no se cierra de más), y su propio reanálisis lo supera
  d) el origen es un DIRECTA por C: su análisis S0 sigue las mismas reglas
  e) consultas: una consulta puede citar S1 superado (es vigente), pero abrir_directa con esa consulta, por D o por E, da O-06 y
     no deja APERTURA; la COMPARAR con S1 no cambia nada
  f) tocar el DIRECTA reanalizado para esquivar la comprobación (analisis_ref a None, via, la anotación de reutilización) se
     detecta, y abrir_directa da O-13
  g) guardar y cargar, y el diario, mantienen el rechazo
  h) analisis_vigentes() dice lo mismo que abrir_directa en cada caso"""
import copy
import os
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, ENTRADA, SALIDA, chk, dim, encargo, fin, foto, nuevo, sobre_para  # noqa: E402
from pruebas_orquestador import COND_OBS  # noqa: E402
import persistencia as pe  # noqa: E402
import diario as di  # noqa: E402

T1 = "2026-11-06T09:40:00+00:00"
T2 = "2026-11-06T09:50:00+00:00"
CE = {**ENTRADA, "ventana_hasta": "2026-11-06T09:30:00+00:00"}
S1 = "EV-SOB-0001"


def origen(o=None):
    o = o or nuevo()
    assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
    assert o.entregar_sobre("EXP-0001", sobre_para(1, None), AHORA)["ok"]
    assert o.observar("EXP-0001", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
    return o


def enc(eid, suf):
    e = encargo(1, producer="BROKER")
    e["expediente_id"], e["correlation_id"], e["event_id"] = eid, f"COR-{eid[4:]}", f"EV-ENC-{eid[4:]}-{suf}"
    return e


def sob(eid, suf):
    s = sobre_para(1, None)
    s["expediente_id"], s["correlation_id"], s["event_id"] = eid, f"COR-{eid[4:]}", f"EV-SOB-{eid[4:]}-{suf}"
    return s


def abre(o, eid, sid=S1, ahora=AHORA, **kw):
    return o.abrir_directa(eid, f"COR-{eid[4:]}", "TACTICA", kw.pop("bloque", "D"), "BROKER", ahora, analisis=sid, **kw)


def registro(o, sid, ahora=AHORA):
    return [x["reutilizable"] for x in o.analisis_vigentes(ahora) if x["analisis"] == sid]


def rechazo_limpio(nombre, o, fn, codigo="O-06", sid=S1, ahora=AHORA):
    antes = foto(o)
    r = fn()
    print(f"   {nombre}:", r["ok"], r["codigo"], r["motivo"][:90])
    chk(nombre, not r["ok"] and r["codigo"] == codigo and foto(o) == antes, r)
    if codigo == "O-06":
        chk(f"{nombre}_registro_coincide", registro(o, sid, ahora) == [False], o.analisis_vigentes(ahora))
    return r


print("a) cadena de tres DIRECTA")
o = origen()
assert abre(o, "EXP-DD-01")["ok"]
assert o.descartar("EXP-DD-01", "el operador descarta el primero", "OPERADOR", AHORA)["ok"]
r = abre(o, "EXP-DD-02")
print("   EXP-DD-02 con S1 tras descartar el operador EXP-DD-01:", r["ok"], r["codigo"])
chk("a_cadena_legitima_se_abre", r["ok"], r)
assert o.comparar(["EXP-DD-02"], "D", AHORA)["ok"]
assert o.proponer("EXP-DD-02", CE, SALIDA, "BROKER", AHORA, dim(o, "EXP-DD-02", entrada=CE))["ok"]
assert o.barrer(T1)["ok"] and o.expedientes["EXP-DD-02"]["estado"] == "CADUCADA"
assert o.emitir_encargo("EXP-DD-02", enc("EXP-DD-02", "B"), "BROKER", T2)["ok"]
assert o.entregar_sobre("EXP-DD-02", sob("EXP-DD-02", "B"), T2)["ok"]
rechazo_limpio("a_EXP-DD-03_con_S1_tras_la_cadena", o, lambda: abre(o, "EXP-DD-03", ahora=T2), ahora=T2)
rechazo_limpio("a_por_E_tambien", o, lambda: abre(o, "EXP-DD-03", ahora=T2, bloque="E", motivo="solo hay un candidato en la cartera, a propósito"),
               ahora=T2)

print("b) un DIRECTA reencargado cuyo encargo caduca sin sobre")
o = origen()
assert abre(o, "EXP-DD-01")["ok"]
assert o.observar("EXP-DD-01", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
assert o.reabrir("EXP-DD-01", "el operador pide un análisis nuevo", "OPERADOR", AHORA)["ok"]
assert o.emitir_encargo("EXP-DD-01", enc("EXP-DD-01", "B"), "BROKER", AHORA)["ok"]
T3 = "2026-11-07T10:00:00+00:00"
assert o.barrer(T3)["ok"]
assert o.observar("EXP-DD-01", COND_OBS, "el operador lo aparta otra vez", "OPERADOR", T3)["ok"]
print("   EXP-DD-01:", o.expedientes["EXP-DD-01"]["estado"], o.expedientes["EXP-DD-01"]["sobre"]["event_id"],
      "| encargo", o.encargos["EV-ENC-DD-01-B"]["estado"])
rechazo_limpio("b_S1_no_vuelve_aunque_el_reencargo_no_diera_sobre", o, lambda: abre(o, "EXP-DD-02", ahora=T3), ahora=T3)

print("c) el análisis nuevo S2 del DIRECTA reanalizado")
o = origen()
assert abre(o, "EXP-DD-01")["ok"]
assert o.observar("EXP-DD-01", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
assert o.reabrir("EXP-DD-01", "el operador pide un análisis nuevo", "OPERADOR", AHORA)["ok"]
assert o.emitir_encargo("EXP-DD-01", enc("EXP-DD-01", "B"), "BROKER", AHORA)["ok"]
assert o.entregar_sobre("EXP-DD-01", sob("EXP-DD-01", "B"), AHORA)["ok"]
assert o.observar("EXP-DD-01", COND_OBS, "el operador lo aparta con S2", "OPERADOR", AHORA)["ok"]
S2 = "EV-SOB-DD-01-B"
r = abre(o, "EXP-DD-03", sid=S2)
print("   EXP-DD-03 con S2:", r["ok"], r["codigo"], r["motivo"][:80])
chk("c_S2_se_reutiliza", r["ok"] and o.expedientes["EXP-DD-03"]["analisis_ref"] == S2, r)
assert o.observar("EXP-DD-03", COND_OBS, "el operador aparta EXP-DD-03", "OPERADOR", AHORA)["ok"]
assert o.reabrir("EXP-DD-03", "el operador pide otro análisis", "OPERADOR", AHORA)["ok"]
assert o.emitir_encargo("EXP-DD-03", enc("EXP-DD-03", "B"), "BROKER", AHORA)["ok"]
rechazo_limpio("c_S2_superado_por_EXP-DD-03", o, lambda: abre(o, "EXP-DD-04", sid=S2), sid=S2)

print("d) el origen es un DIRECTA por C")
o = nuevo()
e0 = enc("EXP-DD-00", "A")
assert o.abrir_directa("EXP-DD-00", "COR-DD-00", "TACTICA", "C", "BROKER", AHORA, encargo=e0)["ok"]
assert o.entregar_sobre("EXP-DD-00", sob("EXP-DD-00", "A"), AHORA)["ok"]
assert o.observar("EXP-DD-00", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
S0 = "EV-SOB-DD-00-A"
assert abre(o, "EXP-DD-01", sid=S0)["ok"]
assert o.comparar(["EXP-DD-01"], "D", AHORA)["ok"]
assert o.proponer("EXP-DD-01", CE, SALIDA, "BROKER", AHORA, dim(o, "EXP-DD-01", entrada=CE))["ok"]
assert o.barrer(T1)["ok"]
assert o.emitir_encargo("EXP-DD-01", enc("EXP-DD-01", "B"), "BROKER", T2)["ok"]
rechazo_limpio("d_S0_superado", o, lambda: abre(o, "EXP-DD-02", sid=S0, ahora=T2), sid=S0, ahora=T2)

print("e) consultas con S1 superado")
o = origen()
assert abre(o, "EXP-DD-01")["ok"]
assert o.observar("EXP-DD-01", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
assert o.reabrir("EXP-DD-01", "el operador pide un análisis nuevo", "OPERADOR", AHORA)["ok"]
assert o.emitir_encargo("EXP-DD-01", enc("EXP-DD-01", "B"), "BROKER", AHORA)["ok"]
assert o.entregar_sobre("EXP-DD-01", sob("EXP-DD-01", "B"), AHORA)["ok"]
assert o.observar("EXP-DD-01", COND_OBS, "el operador lo aparta con S2", "OPERADOR", AHORA)["ok"]
c = {"consulta_id": "CON-0001", "correlation_id": "COR-CON-1", "tipo": "ANALIZAR", "bloque": "C", "cartera": "TACTICA", "analisis": [S1],
     "pregunta": "qué dice el análisis anterior del instrumento"}
r = o.consultar(c, "BROKER", AHORA)
print("   consulta ANALIZAR con S1:", r["ok"], r["codigo"])
antes = foto(o)
cc = {**c, "consulta_id": "CON-0002", "tipo": "COMPARAR", "bloque": "D", "analisis": [S1, "EV-SOB-DD-01-B"], "pregunta": "comparar el viejo y el nuevo"}
r = o.consultar(cc, "BROKER", AHORA)
d = {k: v for k, v in foto(o).items() if v != antes.get(k)}
print("   consulta COMPARAR con S1 y S2:", r["ok"], r["codigo"], (r.get("resultado") or {}).get("excluidos"), "| cambia:", sorted(d))
chk("e_la_COMPARAR_solo_toca_el_rastro", sorted(d) == ["consultas"], sorted(d))
n = len(o.consultas["entradas"])
rechazo_limpio("e_abrir_con_la_consulta_por_D", o, lambda: abre(o, "EXP-DD-02", consulta_id="CON-0001"))
rechazo_limpio("e_abrir_con_la_consulta_por_E", o, lambda: abre(o, "EXP-DD-02", consulta_id="CON-0001", bloque="E",
                                                                motivo="solo hay un candidato en la cartera, a propósito"))
chk("e_sin_APERTURA_en_el_rastro", len(o.consultas["entradas"]) == n and o.consultas_ok() and o.integridad() == [], o.consultas["entradas"][-1])
r = o.abrir_directa("EXP-DD-02", "COR-DD-02", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-DD-01-B", consulta_id="CON-0002")
print("   abrir con la COMPARAR y S2:", r["ok"], r["codigo"], r["motivo"][:60])
chk("e_con_S2_de_la_COMPARAR_si", r["ok"] and o.integridad() == [], r)

print("f) tocar el DIRECTA reanalizado para esquivar la comprobación")
base_f = origen()
assert abre(base_f, "EXP-DD-01")["ok"]
assert base_f.observar("EXP-DD-01", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
assert base_f.reabrir("EXP-DD-01", "el operador pide un análisis nuevo", "OPERADOR", AHORA)["ok"]
assert base_f.emitir_encargo("EXP-DD-01", enc("EXP-DD-01", "B"), "BROKER", AHORA)["ok"]
toques = {
    "analisis_ref_None": lambda x: x.update(analisis_ref=None),
    "via_DISCRECIONAL": lambda x: x.update(via_entrada="DISCRECIONAL"),
    "sin_campos_DIRECTA": lambda x: [x.pop(k) for k in ("bloque_entrada", "analisis_ref", "consulta_ref")] and x.update(via_entrada="DISCRECIONAL"),
    "motivo_de_reutilizacion": lambda x: next(z for z in x["historial"] if str(z["motivo"]).startswith("análisis vigente")).update(motivo="otro"),
    "encargo_emitido_renombrado": lambda x: next(z for z in x["historial"] if z["motivo"] == "encargo emitido").update(motivo="reintento"),
}
for nombre, toque in toques.items():
    o = copy.deepcopy(base_f)
    toque(o.expedientes["EXP-DD-01"])
    integ = o.integridad()
    r = abre(o, "EXP-DD-02")
    print(f"   {nombre}: integridad {integ} | abrir_directa {r['codigo']}")
    chk(f"f_{nombre}_se_detecta_y_para", "EXP:EXP-DD-01" in integ and not r["ok"] and r["codigo"] == "O-13", (integ, r))

print("g) guardar, cargar y diario")
with tempfile.TemporaryDirectory() as d:
    est, dia = os.path.join(d, "estado.json"), os.path.join(d, "diario.jsonl")
    o = nuevo()
    r = di.crear(o, est, dia, AHORA)
    assert r["ok"], r
    D = r["diario"]
    origen(D)
    assert abre(D, "EXP-DD-01")["ok"]
    assert D.observar("EXP-DD-01", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
    assert D.reabrir("EXP-DD-01", "el operador pide un análisis nuevo", "OPERADOR", AHORA)["ok"]
    assert D.emitir_encargo("EXP-DD-01", enc("EXP-DD-01", "B"), "BROKER", AHORA)["ok"]
    assert D.entregar_sobre("EXP-DD-01", sob("EXP-DD-01", "B"), AHORA)["ok"]
    r1 = abre(D, "EXP-DD-02")
    r2 = di.abrir(est, dia)
    assert r2["ok"], r2
    o2 = r2["diario"]
    r3 = abre(o2, "EXP-DD-02")
    print("   antes:", r1["codigo"], "| reabierto desde el diario:", r3["codigo"], "| integridad", o2.integridad())
    chk("g_diario_mantiene_el_rechazo", not r1["ok"] and not r3["ok"] and r3["codigo"] == "O-06" and o2.integridad() == [], (r1, r3))
    ruta = os.path.join(d, "solo.json")
    r = pe.guardar(getattr(o2, "_o", o2), ruta, AHORA)
    print("   guardar:", r["ok"], r["codigo"])
    r = pe.cargar_de(ruta, None)
    r4 = abre(r["orquestador"], "EXP-DD-02") if r["ok"] else r
    chk("g_guardar_y_cargar_mantiene_el_rechazo", r["ok"] and not r4["ok"] and r4["codigo"] == "O-06", (r.get("codigo"), r4))
sys.exit(fin())
