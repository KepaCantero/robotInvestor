"""QA r02 · sonda 02 (variantes de r01_02 y r01_03, H-01): la corrección rechaza reutilizar un sobre cuyo origen tiene un «encargo
emitido» posterior a su última validación. Se comprueba que:
  a) un DIRECTA legítimo (S1 con su encargo E1) caduca cuando K anula el sello de E1, como un expediente normal;
  b) volver a encargar el DIRECTA no anula ni cambia el encargo del origen (antes, `previo` era de otro expediente);
  c) el origen re-encargado DESPUÉS de abrir el DIRECTA no rompe la integridad del DIRECTA ni deja reutilizar S1 otra vez;
  d) el origen re-encargado cuyo encargo nuevo caduca sin sobre (vuelve a EN_OBSERVACION con sobre S1) tampoco reutiliza S1;
  e) el registro (analisis_vigentes) dice lo mismo que abrir_directa en cada caso.
(Datos SIMULADOS.)"""
import copy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, ENTRADA, SALIDA, chk, dim, encargo, fin, foto, nuevo, sobre_para  # noqa: E402,F401
from pruebas_orquestador import COND_OBS, S2  # noqa: E402
from pruebas_k import CTX as CTX_K, construir as construir_k  # noqa: E402


def origen_en_observacion():
    o = nuevo()
    assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
    assert o.entregar_sobre("EXP-0001", sobre_para(1, None), AHORA)["ok"]
    assert o.observar("EXP-0001", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
    return o


def reutilizable(o, sid="EV-SOB-0001", ahora=AHORA):
    return [x["reutilizable"] for x in o.analisis_vigentes(ahora) if x["analisis"] == sid]


# a) DIRECTA legítimo y sello anulado
o = origen_en_observacion()
r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
assert r["ok"], r
print("a) DIRECTA encargo_actual:", o.expedientes["EXP-DD-01"]["encargo_actual"])
nuevo_k1 = construir_k(ctx={**CTX_K, "secuencia": 2, "reemplaza_a": "K-20261105-001"})[1]["sello"]
r = o.registrar_sello(nuevo_k1, AHORA)
print("a) K reemplaza K-20261105-001:", r["ok"], r["codigo"])
chk("a_DIRECTA_legitimo_caduca_al_anularse_el_sello_de_su_analisis", o.expedientes["EXP-DD-01"]["estado"] == "CADUCADA",
    o.expedientes["EXP-DD-01"]["estado"])
chk("a_integridad_vacia", o.integridad() == [], o.integridad())

# b) volver a encargar el DIRECTA no toca el encargo del origen
o = origen_en_observacion()
assert o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")["ok"]
assert o.observar("EXP-DD-01", COND_OBS, "el operador aparta el DIRECTA", "OPERADOR", AHORA)["ok"]
assert o.reabrir("EXP-DD-01", "el operador pide un análisis nuevo", "OPERADOR", AHORA)["ok"]
enc_origen = copy.deepcopy(o.encargos["EV-ENC-0001"])
e3 = encargo(1, producer="BROKER")
e3["expediente_id"], e3["correlation_id"], e3["event_id"] = "EXP-DD-01", "COR-DD-01", "EV-ENC-DD-01-B"
r = o.emitir_encargo("EXP-DD-01", e3, "BROKER", AHORA)
print("b) re-encargar el DIRECTA:", r["ok"], r["codigo"], r["motivo"][:80])
chk("b_el_encargo_del_origen_no_cambia", o.encargos["EV-ENC-0001"] == enc_origen,
    (enc_origen["estado"], o.encargos["EV-ENC-0001"]["estado"]))
chk("b_integridad_vacia", o.integridad() == [], o.integridad())
# el DIRECTA en reanálisis tiene S1: nadie más lo reutiliza mientras tanto
r = o.abrir_directa("EXP-DD-02", "COR-DD-02", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
print("b) otro DIRECTA con S1 mientras el primero se reanaliza:", r["ok"], r["codigo"], r["motivo"][:80])
chk("b_S1_no_se_reutiliza_mientras_un_DIRECTA_lo_reanaliza", not r["ok"] and reutilizable(o) == [False], r)

# c) el origen se vuelve a encargar después de abrir el DIRECTA
o = origen_en_observacion()
assert o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")["ok"]
assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo del origen", "OPERADOR", AHORA)["ok"]
e2 = encargo(1)
e2["event_id"] = "EV-ENC-0001-B"
assert o.emitir_encargo("EXP-0001", e2, "GESTOR_TACTICA", AHORA)["ok"]
chk("c_el_DIRECTA_sigue_integro_y_con_E1", o.integridad() == [] and o.expedientes["EXP-DD-01"]["encargo_actual"] == "EV-ENC-0001",
    (o.integridad(), o.expedientes["EXP-DD-01"]["encargo_actual"]))
r = o.comparar(["EXP-DD-01"], "D", AHORA)
print("c) comparar el DIRECTA:", r["ok"], r["codigo"], r["motivo"][:80])
chk("c_el_DIRECTA_se_compara_con_su_sello", r["ok"], r)
assert o.observar("EXP-0001", COND_OBS, "el operador lo aparta otra vez", "OPERADOR", AHORA)["ok"]
r = o.abrir_directa("EXP-DD-02", "COR-DD-02", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
chk("c_S1_no_se_reutiliza_otra_vez", not r["ok"] and r["codigo"] == "O-06", r)

# d) el encargo nuevo del origen caduca sin sobre y el origen vuelve a EN_OBSERVACION con S1
o = origen_en_observacion()
assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo", "OPERADOR", AHORA)["ok"]
e2 = encargo(1)
e2["event_id"] = "EV-ENC-0001-B"
assert o.emitir_encargo("EXP-0001", e2, "GESTOR_TACTICA", AHORA)["ok"]
T2 = "2026-11-07T10:00:00+00:00"
assert o.barrer(T2)["ok"]
print("d) encargo nuevo:", o.encargos["EV-ENC-0001-B"]["estado"], "| sobre del origen:", o.expedientes["EXP-0001"]["sobre"]["event_id"])
assert o.observar("EXP-0001", COND_OBS, "el operador lo aparta", "OPERADOR", T2)["ok"]
antes = foto(o)
r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", T2, analisis="EV-SOB-0001")
print("d) abrir_directa:", r["ok"], r["codigo"], r["motivo"][:90])
chk("d_no_reutiliza_S1_y_no_deja_nada", not r["ok"] and foto(o) == antes, r)
chk("e_el_registro_coincide", reutilizable(o, ahora=T2) == [False], o.analisis_vigentes(T2))
sys.exit(fin())
