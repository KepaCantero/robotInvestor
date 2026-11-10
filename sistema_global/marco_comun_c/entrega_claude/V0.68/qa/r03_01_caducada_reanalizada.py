"""QA r03 · sonda 01 (variante de r02_01, H-09): la corrección de H-09 mira solo los expedientes que TIENEN AHORA el sobre (su
`sobre.event_id`). Un DIRECTA cuya propuesta caduca y que después se vuelve a encargar (CADUCADA -> EN_ANALISIS está en T) y recibe
un sobre nuevo deja de «tener» S1; el origen (EN_OBSERVACION por el operador) sigue teniéndolo y no caducó. ¿Vuelve entonces S1, el
análisis de la propuesta caducada, a nacer VALIDADA en otro DIRECTA y a proponerse sin análisis nuevo (§4.1, regla 4)?
Variante b: lo mismo con un apartado del gestor (T-36) en lugar de la caducidad. (Datos SIMULADOS.)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, ENTRADA, SALIDA, chk, dim, encargo, fin, foto, nuevo, sobre_para  # noqa: E402,F401
from pruebas_orquestador import CART_E, COND_OBS  # noqa: E402
from datetime import datetime, timedelta

T1 = "2026-11-06T09:40:00+00:00"   # pasó la ventana de la propuesta (09:30), no la vigencia de S1 (11-08 18:00)
T2 = "2026-11-06T09:50:00+00:00"
CE = {**ENTRADA, "ventana_hasta": "2026-11-06T09:30:00+00:00"}


def base():
    o = nuevo()
    assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
    assert o.entregar_sobre("EXP-0001", sobre_para(1, None), AHORA)["ok"]
    assert o.observar("EXP-0001", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
    assert o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")["ok"]
    return o


def reanalizar(o, quien, ahora):
    """Encargo y sobre nuevos (S2) para EXP-DD-01."""
    e3 = encargo(1, producer="BROKER")
    e3["expediente_id"], e3["correlation_id"], e3["event_id"] = "EXP-DD-01", "COR-DD-01", "EV-ENC-DD-01-B"
    r = o.emitir_encargo("EXP-DD-01", e3, quien, ahora)
    print("   re-encargar EXP-DD-01:", r["ok"], r["codigo"], r["motivo"][:90])
    assert r["ok"], r
    s2 = sobre_para(1, None)
    s2["expediente_id"], s2["correlation_id"], s2["event_id"] = "EXP-DD-01", "COR-DD-01", "EV-SOB-DD-01-B"
    r = o.entregar_sobre("EXP-DD-01", s2, ahora)
    print("   sobre nuevo S2 para EXP-DD-01:", r["ok"], r["codigo"], "| estado", o.expedientes["EXP-DD-01"]["estado"],
          "| sobre", o.expedientes["EXP-DD-01"]["sobre"]["event_id"])
    assert r["ok"], r


def intento(o, ahora, etiqueta):
    reg = [(x["analisis"], x["reutilizable"], (x["motivo"] or "")[:70]) for x in o.analisis_vigentes(ahora) if x["analisis"] == "EV-SOB-0001"]
    print(f"   registro ({etiqueta}):", reg)
    antes = foto(o)
    r = o.abrir_directa("EXP-DD-02", "COR-DD-02", "TACTICA", "D", "BROKER", ahora, analisis="EV-SOB-0001")
    print(f"   abrir_directa EXP-DD-02 con S1 ({etiqueta}):", r["ok"], r["codigo"], r["motivo"][:90])
    propuesto = False
    if r["ok"]:
        assert o.descartar("EXP-DD-01", "el operador descarta el reanálisis", "OPERADOR", ahora)["ok"]
        r2 = o.comparar(["EXP-DD-02"], "D", ahora)
        print("   comparar EXP-DD-02:", r2["ok"], r2["codigo"], "ganador", r2.get("ganador"))
        if r2["ok"] and not o.expedientes["EXP-DD-02"]["comparacion"]["ganador"]:
            o.elegir("EXP-DD-02", "OPERADOR", "elección de la sonda", ahora)
        r2 = o.proponer("EXP-DD-02", ENTRADA, SALIDA, "BROKER", ahora, dim(o, "EXP-DD-02", ahora=ahora, cartera={**CART_E, "fecha_hora": (datetime.fromisoformat(ahora) - timedelta(minutes=5)).isoformat()}))
        print("   proponer EXP-DD-02 (S1 otra vez):", r2["ok"], r2["codigo"], r2["motivo"][:80], "| integridad", o.integridad())
        propuesto = r2["ok"]
    else:
        chk(f"{etiqueta}_el_rechazo_no_deja_estado", foto(o) == antes)
    return r["ok"], propuesto


# a) caducidad (regla 4)
print("a) la propuesta del DIRECTA caduca y el DIRECTA se reanaliza")
o = base()
assert o.comparar(["EXP-DD-01"], "D", AHORA)["ok"]
r = o.proponer("EXP-DD-01", CE, SALIDA, "BROKER", AHORA, dim(o, "EXP-DD-01", entrada=CE))
assert r["ok"], r
assert o.barrer(T1)["ok"] and o.expedientes["EXP-DD-01"]["estado"] == "CADUCADA"
r = o.abrir_directa("EXP-DD-02", "COR-DD-02", "TACTICA", "D", "BROKER", T1, analisis="EV-SOB-0001")
print("   control: abrir_directa con S1 con el DIRECTA aún CADUCADA:", r["ok"], r["codigo"])
chk("a_control_caducada_O06", not r["ok"] and r["codigo"] == "O-06", r)
reanalizar(o, "BROKER", T2)
abre, prop = intento(o, T2, "a")
chk("a_el_analisis_de_la_propuesta_caducada_no_vuelve_por_otro_DIRECTA", not abre, "nace VALIDADA")
chk("a_ni_se_propone_otra_vez", not prop, "PROPUESTA con S1")

# b) apartado del gestor (T-36)
print("b) el gestor aparta el DIRECTA y el DIRECTA se reanaliza")
o = base()
assert o.observar("EXP-DD-01", COND_OBS, "el gestor lo aparta: no le convence", "GESTOR_TACTICA", AHORA)["ok"]
r = o.abrir_directa("EXP-DD-02", "COR-DD-02", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
print("   control: con el apartado del gestor:", r["ok"], r["codigo"], r["motivo"][:80])
chk("b_control_apartado_O06", not r["ok"] and r["codigo"] == "O-06", r)
assert o.reabrir("EXP-DD-01", "el operador pide un análisis nuevo", "OPERADOR", AHORA)["ok"]
reanalizar(o, "BROKER", AHORA)
abre, prop = intento(o, AHORA, "b")
print("INFO  b) S1 vuelve tras apartarlo el gestor y reanalizar el DIRECTA:", abre, "| propuesto:", prop)

# c) como b, pero sin ninguna acción del operador sobre EXP-DD-01: la reapertura la da la condición FECHA cumplida
print("c) el gestor aparta el DIRECTA, se cumple su condición de reapertura y el Broker lo reanaliza")
T7 = "2026-11-07T10:00:00+00:00"
o = base()
assert o.observar("EXP-DD-01", [{"tipo": "FECHA", "fecha": "2026-11-07"}], "el gestor lo aparta hasta mañana", "GESTOR_TACTICA", AHORA)["ok"]
reanalizar(o, "BROKER", T7)
quien = sorted({z["actor"] for z in o.expedientes["EXP-DD-01"]["historial"]})
print("   actores en el historial de EXP-DD-01:", quien)
abre, prop = intento(o, T7, "c")
chk("c_lo_que_el_gestor_aparto_no_vuelve_por_otro_DIRECTA_sin_el_operador", not abre, "nace VALIDADA")

# d) T-27: el DIRECTA se reanaliza (S2) y un tercer análisis (S3) sale BLOQUEADO (exclusión dura)
print("d) el DIRECTA se reanaliza dos veces y el segundo reanálisis sale BLOQUEADO")
o = base()
assert o.observar("EXP-DD-01", COND_OBS, "el operador pide reanalizar", "OPERADOR", AHORA)["ok"]
assert o.reabrir("EXP-DD-01", "el operador pide un análisis nuevo", "OPERADOR", AHORA)["ok"]
reanalizar(o, "BROKER", AHORA)
assert o.observar("EXP-DD-01", COND_OBS, "el operador pide reanalizar otra vez", "OPERADOR", AHORA)["ok"]
assert o.reabrir("EXP-DD-01", "el operador pide otro análisis", "OPERADOR", AHORA)["ok"]
e4 = encargo(1, producer="BROKER")
e4["expediente_id"], e4["correlation_id"], e4["event_id"] = "EXP-DD-01", "COR-DD-01", "EV-ENC-DD-01-C"
assert o.emitir_encargo("EXP-DD-01", e4, "BROKER", AHORA)["ok"]
s3 = sobre_para(1, None)
s3["expediente_id"], s3["correlation_id"], s3["event_id"] = "EXP-DD-01", "COR-DD-01", "EV-SOB-DD-01-C"
s3["payload"]["exclusiones_duras"]["sanciones"] = "BLOQUEADO"
r = o.entregar_sobre("EXP-DD-01", s3, AHORA)
print("   S3 BLOQUEADO:", r["ok"], r["codigo"], "| estado", o.expedientes["EXP-DD-01"]["estado"],
      "| sobre", o.expedientes["EXP-DD-01"]["sobre"]["event_id"], "| exclusion", bool(o.expedientes["EXP-DD-01"].get("exclusion")))
r = o.abrir_directa("EXP-DD-02", "COR-DD-02", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
print("   abrir_directa EXP-DD-02 con S1 (d):", r["ok"], r["codigo"], r["motivo"][:90])
print("INFO  d) S1 vuelve aunque el candidato salió BLOQUEADO en su último análisis:", r["ok"])
sys.exit(fin())
