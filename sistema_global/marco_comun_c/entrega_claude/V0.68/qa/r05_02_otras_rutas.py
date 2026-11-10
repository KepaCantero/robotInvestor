"""QA r05 · sonda 02: otras rutas hacia una orden con un análisis superado, apartado, caducado o excluido, después de H-16.
  a) linaje sin sobre compartido: el DIRECTA se reanaliza (S2) y queda en juego; el origen, con S1 (ya superado, H-13), se reanaliza
     y sale BLOQUEADO. ¿Sigue el DIRECTA con S2? Contraste: dos expedientes normales del mismo instrumento (sin vía DIRECTA)
  b) reloj: el DIRECTA sigue VALIDADA con S1 vencido porque nadie ha barrido; ¿bloquea el reencargo del origen? ¿y tras barrer?
  c) consultas: una COMPARAR con S1 mientras el DIRECTA lo tiene en juego solo deja rastro; abrir desde ella da O-06
  d) el rechazo de H-16 con un ahora adelantado (H-17): ¿qué caduca?
(Datos SIMULADOS.)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, ENTRADA, SALIDA, chk, dim, encargo, fin, foto, nuevo, sobre_para  # noqa: E402
from pruebas_orquestador import COND_OBS  # noqa: E402

S1 = "EV-SOB-0001"
INFO = {}


def base(o=None):
    o = o if o is not None else nuevo()
    assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
    assert o.entregar_sobre("EXP-0001", sobre_para(1, None), AHORA)["ok"]
    assert o.observar("EXP-0001", COND_OBS, "el operador lo aparta por ahora", "OPERADOR", AHORA)["ok"]
    r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis=S1)
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


def s_dd(eid, suf="B", bloqueado=False):
    s = sobre_para(1, None)
    s["expediente_id"], s["correlation_id"], s["event_id"] = eid, f"COR-{eid[4:]}", f"EV-SOB-{eid[4:]}-{suf}"
    if bloqueado:
        s["payload"]["exclusiones_duras"]["sanciones"] = "BLOQUEADO"
    return s


def proponer(o, eid, ahora=AHORA):
    r = o.comparar([eid], "D", ahora)
    if not r["ok"]:
        return r
    if not o.expedientes[eid]["comparacion"].get("ganador"):
        o.elegir(eid, "OPERADOR", "elección de la sonda r05", ahora)
    return o.proponer(eid, ENTRADA, SALIDA, "BROKER", ahora, dim(o, eid, ahora=ahora))


print("a) linaje: el DIRECTA reanalizado (S2) en juego y el origen (S1) reanalizado y BLOQUEADO")
o = base()
assert o.observar("EXP-DD-01", COND_OBS, "el operador aparta el DIRECTA", "OPERADOR", AHORA)["ok"]
assert o.reabrir("EXP-DD-01", "el operador pide un análisis nuevo del DIRECTA", "OPERADOR", AHORA)["ok"]
assert o.emitir_encargo("EXP-DD-01", e_dd("EXP-DD-01"), "BROKER", AHORA)["ok"]
assert o.entregar_sobre("EXP-DD-01", s_dd("EXP-DD-01"), AHORA)["ok"]
assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo del origen", "OPERADOR", AHORA)["ok"]
r = o.emitir_encargo("EXP-0001", e_origen(), "GESTOR_TACTICA", AHORA)
print("   reencargo del origen (S1, superado) con el DIRECTA en juego con S2:", r["ok"], r["codigo"], r["motivo"][:60])
INFO["a_reencargo_origen"] = r["codigo"]
if r["ok"]:
    s3 = sobre_para(1, None)
    s3["event_id"] = "EV-SOB-0001-B"
    s3["payload"]["exclusiones_duras"]["sanciones"] = "BLOQUEADO"
    r = o.entregar_sobre("EXP-0001", s3, AHORA)
    print("   origen BLOQUEADO:", r["ok"], r["codigo"], "| origen", o.expedientes["EXP-0001"]["estado"])
r = proponer(o, "EXP-DD-01")
print("   el DIRECTA con S2 se propone:", r["ok"], r["codigo"], r["motivo"][:60])
INFO["a_DIRECTA_S2_tras_bloqueo_del_origen"] = o.expedientes["EXP-DD-01"]["estado"]
# contraste en el flujo normal: dos expedientes del mismo instrumento, el segundo BLOQUEADO
o = nuevo()
for n in (1, 2):
    assert o.detectar(f"EXP-000{n}", f"COR-000{n}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.emitir_encargo(f"EXP-000{n}", encargo(n), "GESTOR_TACTICA", AHORA)["ok"]
s = sobre_para(2, None)
s["payload"]["exclusiones_duras"]["sanciones"] = "BLOQUEADO"
assert o.entregar_sobre("EXP-0001", sobre_para(1, None), AHORA)["ok"]
r = o.entregar_sobre("EXP-0002", s, AHORA)
print("   contraste sin DIRECTA, EXP-0002 del mismo instrumento BLOQUEADO:", r["codigo"],
      o.expedientes["EXP-0001"]["sobre"]["documento"]["payload"]["identificacion"]["instrumento"],
      s["payload"]["identificacion"]["instrumento"])
r = proponer(o, "EXP-0001")
print("   EXP-0001 se propone:", r["ok"], r["codigo"])
INFO["a_contraste_flujo_normal"] = o.expedientes["EXP-0001"]["estado"]
chk("a_igual_que_el_flujo_normal", INFO["a_DIRECTA_S2_tras_bloqueo_del_origen"] == INFO["a_contraste_flujo_normal"], INFO)

print("b) reloj: el DIRECTA VALIDADA con S1 vencido y sin barrer")
o = base()
from pruebas_orquestador import S2 as SELLO2  # noqa: E402
assert o.registrar_sello(SELLO2, AHORA)["ok"]   # un sello más nuevo, para que el encargo del 9 tenga datos frescos
T9 = "2026-11-09T09:00:00+00:00"   # S1 vence el 2026-11-08 a las 18:00
assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo del origen", "OPERADOR", T9)["ok"]
e2 = encargo(1, corte="2026-11-06", sello="K-20261106-001")
e2["event_id"] = "EV-ENC-0001-B"
e2["emitido_en"], e2["valid_until"] = "2026-11-09T08:30:00+00:00", "2026-11-12T12:00:00+00:00"
e2["payload"]["presupuesto"]["entrega_antes_de"] = "2026-11-09T20:00:00+00:00"
r = o.emitir_encargo("EXP-0001", e2, "GESTOR_TACTICA", T9)
print("   reencargo sin barrer:", r["ok"], r["codigo"], r["motivo"][:70])
INFO["b_sin_barrer"] = r["codigo"]
rc = o.comparar(["EXP-DD-01"], "D", T9)
print("   comparar el DIRECTA vencido:", rc["ok"], rc["codigo"])
chk("b_el_DIRECTA_vencido_no_sigue", not rc["ok"], rc)
assert o.barrer(T9)["ok"]
r = o.emitir_encargo("EXP-0001", e2, "GESTOR_TACTICA", T9)
print("   tras barrer (DIRECTA", o.expedientes["EXP-DD-01"]["estado"] + "):", r["ok"], r["codigo"], r["motivo"][:70])
INFO["b_tras_barrer"] = r["codigo"]

print("c) consultas con S1 en juego")
o = base()
CON = {"consulta_id": "CON-R5", "correlation_id": "COR-CON-R5", "tipo": "COMPARAR", "bloque": "D", "cartera": "TACTICA",
       "analisis": [S1], "pregunta": "¿cómo queda este candidato frente al benchmark?"}
antes = {k: v for k, v in foto(o).items() if k != "consultas"}
r = o.consultar(CON, "BROKER", AHORA)
print("   consulta COMPARAR con S1 en juego:", r["ok"], r["codigo"])
chk("c_la_consulta_solo_deja_rastro", r["ok"] and {k: v for k, v in foto(o).items() if k != "consultas"} == antes, r)
antes = foto(o)
r = o.abrir_directa("EXP-DD-02", "COR-DD-02", "TACTICA", "D", "BROKER", AHORA, analisis=S1, consulta_id="CON-R5")
chk("c_abrir_desde_la_consulta_O06_sin_nada", not r["ok"] and r["codigo"] == "O-06" and foto(o) == antes, r)

print("d) el rechazo de H-16 con un ahora adelantado")
o = base()
assert o.detectar("EXP-0003", "COR-0003", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
assert o.emitir_encargo("EXP-0003", encargo(3), "GESTOR_TACTICA", AHORA)["ok"]
assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo del origen", "OPERADOR", AHORA)["ok"]
e2 = encargo(1)
e2["event_id"] = "EV-ENC-0001-B"
e2["valid_until"] = "2026-11-09T12:00:00+00:00"
e2["payload"]["presupuesto"]["entrega_antes_de"] = "2026-11-08T20:00:00+00:00"
r = o.emitir_encargo("EXP-0001", e2, "GESTOR_TACTICA", "2026-11-08T13:00:00+00:00")
print("   reencargo rechazado con ahora adelantado:", r["ok"], r["codigo"], r["motivo"][:50], "| reloj", o.ultimo_ahora, "| encargo de EXP-0003:",
      o.encargos["EV-ENC-0003"]["estado"])
INFO["d_encargo_ajeno_tras_rechazo_adelantado"] = o.encargos["EV-ENC-0003"]["estado"]

for k, v in INFO.items():
    print("INFO ", k, v)
sys.exit(fin())
