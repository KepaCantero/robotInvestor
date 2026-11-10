"""QA r05 · sonda 01: la regla nueva de H-16 (en _emitir, el reencargo de un expediente cuyo sobre tiene en juego otro da O-06).
  a) con el DIRECTA en cada estado en juego (VALIDADA, COMPARADA, PROPUESTA, AUTORIZADA) el reencargo del origen da O-06 y no deja nada
  b) no cierra de más: el origen SÍ se reanaliza con el DIRECTA invertido (EJECUTADA), caducado, descartado por el operador, por el
     Broker o apartado por el operador; un expediente sin DIRECTA se reanaliza como siempre; un DIRECTA con el origen apartado, también
  c) reapertura por condición cumplida (FECHA): la condición queda marcada, el reencargo da O-06 sin tocar nada y, al descartar el
     DIRECTA, el reencargo entra y cuenta una sola reapertura
  d) gemelos: dos DIRECTA, el que está en observación no se reanaliza mientras el otro está en juego
  e) el rechazo se mantiene en el diario y tras guardar y cargar
  f) lo que H-16 rompe de las sondas anteriores: r02_02 c) (esperaba el reencargo); sus partes d) y e) (H-01) siguen valiendo
(Datos SIMULADOS.)"""
import os
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import (AHORA, ENTRADA, SALIDA, anotar_entrada, autorizar_op, chk, dim, encargo, fin, foto, informe_f,  # noqa: E402
                       nuevo, sobre_para, hasta)
from pruebas_orquestador import COND_OBS  # noqa: E402
import persistencia as pe  # noqa: E402
import diario as di  # noqa: E402

S1 = "EV-SOB-0001"
T7 = "2026-11-07T10:00:00+00:00"
INFO = {}


def base(o=None, cond=COND_OBS, ahora=AHORA):
    o = o if o is not None else nuevo()
    assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", ahora)["ok"]
    assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", ahora)["ok"]
    assert o.entregar_sobre("EXP-0001", sobre_para(1, None), ahora)["ok"]
    assert o.observar("EXP-0001", cond, "el operador lo aparta por ahora", "OPERADOR", ahora)["ok"]
    r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", ahora, analisis=S1)
    assert r["ok"], r
    return o


def e_origen(suf="B"):
    e = encargo(1)
    e["event_id"] = f"EV-ENC-0001-{suf}"
    return e


def e_dd(eid, suf="B"):
    e = encargo(1, producer="BROKER")
    e["expediente_id"], e["correlation_id"], e["event_id"] = eid, f"COR-{eid[4:]}", f"EV-ENC-{eid[4:]}-{suf}"
    return e


def llevar(o, eid, estado, ahora=AHORA):
    """El DIRECTA de VALIDADA al estado pedido (comparar, proponer, autorizar, ejecutar)."""
    if estado == "VALIDADA":
        return
    r = o.comparar([eid], "D", ahora)
    assert r["ok"], r
    if not o.expedientes[eid]["comparacion"].get("ganador"):
        assert o.elegir(eid, "OPERADOR", "elección de la sonda r05", ahora)["ok"]
    if estado == "COMPARADA":
        return
    r = o.proponer(eid, ENTRADA, SALIDA, "BROKER", ahora, dim(o, eid, ahora=ahora))
    assert r["ok"], r
    if estado == "PROPUESTA":
        return
    r = autorizar_op(o, eid, informe_f(o, eid, 1), ahora)
    assert r["ok"], r
    if estado == "AUTORIZADA":
        return
    anotar_entrada(o, eid, "ORD-R5-1", 100.0, ahora)
    r = o.ejecutar(eid, {"orden_id": "ORD-R5-1", "cantidad": 100.0, "precio": 1.1, "conciliada": True,
                         "proteccion_orden_ids": ["ORD-R5-1-STOP"]}, "G", ahora)
    assert r["ok"], r


print("a) el reencargo del origen con el DIRECTA en cada estado en juego")
for est in ("VALIDADA", "COMPARADA", "PROPUESTA", "AUTORIZADA"):
    o = base()
    llevar(o, "EXP-DD-01", est)
    assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo del origen", "OPERADOR", AHORA)["ok"]
    antes = foto(o)
    r = o.emitir_encargo("EXP-0001", e_origen(), "GESTOR_TACTICA", AHORA)
    print(f"   DIRECTA {est}: {r['ok']} {r['codigo']} {r['motivo'][:70]}")
    chk(f"a_{est}_O06_sin_dejar_nada", not r["ok"] and r["codigo"] == "O-06" and foto(o) == antes, r)
    chk(f"a_{est}_integridad", o.integridad() == [], o.integridad())

print("b) no cierra de más")
# b1) DIRECTA EJECUTADA
o = base()
llevar(o, "EXP-DD-01", "EJECUTADA")
assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo del origen", "OPERADOR", AHORA)["ok"]
r = o.emitir_encargo("EXP-0001", e_origen(), "GESTOR_TACTICA", AHORA)
print("   b1 DIRECTA EJECUTADA, reencargo del origen:", r["ok"], r["codigo"], r["motivo"][:60])
chk("b1_con_el_DIRECTA_invertido_el_origen_se_reanaliza", r["ok"], r)
# b2) DIRECTA CADUCADA por barrer (propuesta con ventana corta)
o = base()
llevar(o, "EXP-DD-01", "COMPARADA")
CE = {**ENTRADA, "ventana_hasta": "2026-11-06T09:30:00+00:00"}
assert o.proponer("EXP-DD-01", CE, SALIDA, "BROKER", AHORA, dim(o, "EXP-DD-01", entrada=CE))["ok"]
assert o.barrer("2026-11-06T09:40:00+00:00")["ok"]
assert o.expedientes["EXP-DD-01"]["estado"] == "CADUCADA"
assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo del origen", "OPERADOR", "2026-11-06T09:41:00+00:00")["ok"]
r = o.emitir_encargo("EXP-0001", e_origen(), "GESTOR_TACTICA", "2026-11-06T09:41:00+00:00")
print("   b2 DIRECTA CADUCADA, reencargo del origen:", r["ok"], r["codigo"], r["motivo"][:60])
chk("b2_con_el_DIRECTA_caducado_el_origen_se_reanaliza", r["ok"], r)
# b2') y el DIRECTA caducado también se reanaliza (su origen está en reanálisis, no en juego)
r = o.emitir_encargo("EXP-DD-01", e_dd("EXP-DD-01"), "BROKER", "2026-11-06T09:42:00+00:00")
print("   b2' reencargo del DIRECTA caducado con el origen en reanálisis:", r["ok"], r["codigo"], r["motivo"][:60])
chk("b2p_el_DIRECTA_caducado_se_reanaliza", r["ok"], r)
# b3/b4) descartado por el operador o por el Broker
for quien in ("OPERADOR", "BROKER"):
    o = base()
    assert o.descartar("EXP-DD-01", f"{quien} aparta el DIRECTA", quien, AHORA)["ok"]
    assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo del origen", "OPERADOR", AHORA)["ok"]
    r = o.emitir_encargo("EXP-0001", e_origen(), "GESTOR_TACTICA", AHORA)
    print(f"   b DIRECTA descartado por {quien}, reencargo del origen:", r["ok"], r["codigo"])
    chk(f"b_descartado_por_{quien}_el_origen_se_reanaliza", r["ok"], r)
    s2 = sobre_para(1, None)
    s2["event_id"] = "EV-SOB-0001-B"
    r = o.entregar_sobre("EXP-0001", s2, AHORA)
    assert r["ok"], r
    r = o.comparar(["EXP-0001"], "D", AHORA)
    c = o.expedientes["EXP-0001"].get("comparacion") or {}
    print(f"     comparar el origen con S2: {r['ok']} {r['codigo']} | testigos {c.get('testigos')} | ganador {c.get('ganador')}"
          f" | apartado_mejor {c.get('apartado_mejor')}")
    INFO[f"b_{quien}_comparar_origen"] = (r["codigo"], c.get("testigos"), c.get("apartado_mejor"))
    chk(f"b_descartado_por_{quien}_el_origen_se_compara", r["ok"], r)
# b5) DIRECTA apartado por el operador (observación): el origen se reanaliza y después el DIRECTA también
o = base()
assert o.observar("EXP-DD-01", COND_OBS, "el operador aparta el DIRECTA", "OPERADOR", AHORA)["ok"]
assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo del origen", "OPERADOR", AHORA)["ok"]
r = o.emitir_encargo("EXP-0001", e_origen(), "GESTOR_TACTICA", AHORA)
chk("b5_DIRECTA_en_observacion_el_origen_se_reanaliza", r["ok"], r)
assert o.reabrir("EXP-DD-01", "el operador pide un análisis nuevo del DIRECTA", "OPERADOR", AHORA)["ok"]
r = o.emitir_encargo("EXP-DD-01", e_dd("EXP-DD-01"), "BROKER", AHORA)
chk("b5_y_el_DIRECTA_tambien", r["ok"], r)
# b6) expediente sin DIRECTA
o = nuevo()
hasta(o, "VALIDADA", 1)
assert o.observar("EXP-0001", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo", "OPERADOR", AHORA)["ok"]
r = o.emitir_encargo("EXP-0001", e_origen(), "GESTOR_TACTICA", AHORA)
chk("b6_sin_DIRECTA_el_reanalisis_es_el_de_siempre", r["ok"], r)

print("c) reapertura por condición FECHA cumplida con el DIRECTA en juego")
o = base(cond=[{"tipo": "FECHA", "fecha": "2026-11-07"}])
r = o.barrer(T7)
x = o.expedientes["EXP-0001"]
print("   barrer:", r["cambios"], "| cumplida", bool(x["reapertura"]["cumplida"]))
antes = foto(o)
r = o.emitir_encargo("EXP-0001", e_origen(), "GESTOR_TACTICA", T7)
print("   reencargo del gestor:", r["ok"], r["codigo"], r["motivo"][:70])
chk("c_O06_sin_tocar_nada", not r["ok"] and r["codigo"] == "O-06" and foto(o) == antes, r)
r = o.comparar(["EXP-DD-01"], "D", T7)
chk("c_el_DIRECTA_sigue_con_S1_vigente_y_no_superado", r["ok"] and o.expedientes["EXP-DD-01"]["sobre"]["event_id"] == S1, r)
assert o.descartar("EXP-DD-01", "el operador aparta el DIRECTA", "OPERADOR", T7)["ok"]
r = o.emitir_encargo("EXP-0001", e_origen(), "GESTOR_TACTICA", T7)
n = o._reaperturas_hechas(o.expedientes["EXP-0001"])
marcas = sum(1 for z in o.expedientes["EXP-0001"]["historial"] if str(z["motivo"]).startswith("condición de reapertura"))
print("   tras descartar el DIRECTA:", r["ok"], r["codigo"], "| reaperturas", n, "| marcas de condición", marcas)
chk("c_tras_descartar_el_DIRECTA_el_reencargo_entra_y_cuenta_una", r["ok"] and n == 1 and marcas == 1, (r, n, marcas))

print("d) gemelos")
o = base()
assert o.observar("EXP-DD-01", COND_OBS, "el operador aparta el primer DIRECTA", "OPERADOR", AHORA)["ok"]
assert o.abrir_directa("EXP-DD-02", "COR-DD-02", "TACTICA", "D", "BROKER", AHORA, analisis=S1)["ok"]
llevar(o, "EXP-DD-02", "PROPUESTA")
assert o.reabrir("EXP-DD-01", "el operador pide un análisis nuevo", "OPERADOR", AHORA)["ok"]
for eid, enc in (("EXP-DD-01", e_dd("EXP-DD-01")), ):
    antes = foto(o)
    r = o.emitir_encargo(eid, enc, "BROKER", AHORA)
    print(f"   reencargo de {eid} con EXP-DD-02 en PROPUESTA:", r["ok"], r["codigo"], r["motivo"][:60])
    chk(f"d_{eid}_O06", not r["ok"] and r["codigo"] == "O-06" and foto(o) == antes, r)
assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo del origen", "OPERADOR", AHORA)["ok"]
r = o.emitir_encargo("EXP-0001", e_origen(), "GESTOR_TACTICA", AHORA)
chk("d_el_origen_tampoco", not r["ok"] and r["codigo"] == "O-06" and "EXP-DD-02" in r["motivo"], r)

print("e) diario y guardar/cargar")
with tempfile.TemporaryDirectory() as d:
    est, dia = os.path.join(d, "estado.json"), os.path.join(d, "diario.jsonl")
    rr = di.crear(nuevo(), est, dia, AHORA)
    assert rr["ok"], rr
    D = rr["diario"]
    base(D)
    assert D.reabrir("EXP-0001", "el operador pide un análisis nuevo del origen", "OPERADOR", AHORA)["ok"]
    r1 = D.emitir_encargo("EXP-0001", e_origen(), "GESTOR_TACTICA", AHORA)
    r2 = di.abrir(est, dia)
    assert r2["ok"], r2
    o2 = r2["diario"]
    r3 = o2.emitir_encargo("EXP-0001", e_origen(), "GESTOR_TACTICA", AHORA)
    chk("e_diario_mantiene_el_rechazo", not r1["ok"] and r3["codigo"] == "O-06" and o2._o.integridad() == [], (r1, r3))
    ruta = os.path.join(d, "solo.json")
    assert pe.guardar(o2._o, ruta, AHORA)["ok"]
    rc = pe.cargar_de(ruta, None)
    r4 = rc["orquestador"].emitir_encargo("EXP-0001", e_origen(), "GESTOR_TACTICA", AHORA) if rc["ok"] else rc
    chk("e_guardar_y_cargar_mantiene_el_rechazo", rc["ok"] and r4["codigo"] == "O-06", (rc.get("codigo"), r4))

print("f) r02_02: c) esperaba el reencargo con el DIRECTA en juego; d) y e) (H-01) se repiten aquí")
o = nuevo()
hasta(o, "VALIDADA", 1)
assert o.observar("EXP-0001", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo", "OPERADOR", AHORA)["ok"]
assert o.emitir_encargo("EXP-0001", e_origen(), "GESTOR_TACTICA", AHORA)["ok"]
T2 = "2026-11-07T10:00:00+00:00"
assert o.barrer(T2)["ok"]
assert o.observar("EXP-0001", COND_OBS, "el operador lo aparta", "OPERADOR", T2)["ok"]
antes = foto(o)
r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", T2, analisis=S1)
chk("f_H01_encargo_nuevo_caducado_sin_sobre_no_reutiliza_S1", not r["ok"] and r["codigo"] == "O-06" and foto(o) == antes, r)
chk("f_H01_el_registro_coincide", [x["reutilizable"] for x in o.analisis_vigentes(T2) if x["analisis"] == S1] == [False])

for k, v in INFO.items():
    print("INFO ", k, v)
sys.exit(fin())
