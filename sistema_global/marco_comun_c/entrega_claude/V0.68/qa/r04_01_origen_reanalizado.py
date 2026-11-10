"""QA r04 · sonda 01 (el espejo de H-13): la corrección de H-13 mira los DIRECTA que tuvieron S1 y se volvieron a analizar. ¿Y al
revés? El DIRECTA abre con S1 cuando el origen está en observación por el operador (legítimo) y DESPUÉS el origen se reabre y se
vuelve a encargar. En el flujo normal un candidato en juego no se puede reanalizar (T no tiene VALIDADA -> EN_ANALISIS); con la
vía DIRECTA el mismo candidato está a la vez en juego (el DIRECTA) y en reanálisis (el origen), y §3 del Documento 0 dice que un
análisis «en reanálisis» no se reutiliza. Se mira:
  a) el reanálisis del origen sale BLOQUEADO (exclusión dura T-27): ¿sigue el DIRECTA con S1 hasta PROPUESTA y AUTORIZADA?
  b) el reanálisis del origen sale bien (S2): ¿quedan dos expedientes del mismo candidato en juego, uno con el análisis superado?
  c) como a), sin ninguna reapertura del operador: la condición FECHA que puso el operador se cumple y el gestor reencarga.
  d) control: con el origen ya reencargado ANTES de abrir el DIRECTA, abrir_directa da O-06 (H-01).
(Datos SIMULADOS.)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, ENTRADA, SALIDA, autorizar_op, chk, dim, encargo, fin, informe_f, nuevo, sobre_para  # noqa: E402
from pruebas_orquestador import COND_OBS  # noqa: E402

INFO = {}


def base(cond=COND_OBS):
    o = nuevo()
    assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
    assert o.entregar_sobre("EXP-0001", sobre_para(1, None), AHORA)["ok"]
    assert o.observar("EXP-0001", cond, "el operador lo aparta por ahora", "OPERADOR", AHORA)["ok"]
    r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
    assert r["ok"], r
    return o


def reencargar_origen(o, ahora, bloqueado, reabre=True):
    if reabre:
        assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo del origen", "OPERADOR", ahora)["ok"]
    e2 = encargo(1)
    e2["event_id"] = "EV-ENC-0001-B"
    r = o.emitir_encargo("EXP-0001", e2, "GESTOR_TACTICA", ahora)
    print("   reencargar el origen con el DIRECTA en juego:", r["ok"], r["codigo"], r["motivo"][:90])
    if not r["ok"]:
        return r
    s2 = sobre_para(1, None)
    s2["event_id"] = "EV-SOB-0001-B"
    if bloqueado:
        s2["payload"]["exclusiones_duras"]["sanciones"] = "BLOQUEADO"
    r = o.entregar_sobre("EXP-0001", s2, ahora)
    x = o.expedientes["EXP-0001"]
    print("   sobre nuevo del origen:", r["ok"], r["codigo"], "| origen", x["estado"], "| exclusion", bool(x.get("exclusion")),
          "| DIRECTA", o.expedientes["EXP-DD-01"]["estado"], o.expedientes["EXP-DD-01"]["sobre"]["event_id"])
    return r


def seguir_directa(o, ahora, etiqueta):
    """¿Llega el DIRECTA, con S1, a PROPUESTA y a AUTORIZADA?"""
    r = o.comparar(["EXP-DD-01"], "D", ahora)
    if not r["ok"] and r.get("faltan"):
        print(f"   comparar solo el DIRECTA ({etiqueta}): {r['codigo']} faltan {r['faltan']}")
        r = o.comparar(sorted(["EXP-DD-01", *r["faltan"]]), "D", ahora)
    print(f"   comparar ({etiqueta}):", r["ok"], r["codigo"], r["motivo"][:80])
    if not r["ok"]:
        return "VALIDADA"
    if not o.expedientes["EXP-DD-01"]["comparacion"].get("ganador"):
        r = o.elegir("EXP-DD-01", "OPERADOR", "elección de la sonda", ahora)
        print(f"   elegir ({etiqueta}):", r["ok"], r["codigo"], r["motivo"][:80])
    r = o.proponer("EXP-DD-01", ENTRADA, SALIDA, "BROKER", ahora, dim(o, "EXP-DD-01", ahora=ahora))
    print(f"   proponer el DIRECTA con S1 ({etiqueta}):", r["ok"], r["codigo"], r["motivo"][:90])
    if not r["ok"]:
        return o.expedientes["EXP-DD-01"]["estado"]
    r = autorizar_op(o, "EXP-DD-01", informe_f(o, "EXP-DD-01", 1), ahora)
    print(f"   autorizar el DIRECTA ({etiqueta}):", r["ok"], r["codigo"], r["motivo"][:90], "| integridad", o.integridad())
    return o.expedientes["EXP-DD-01"]["estado"]


print("a) el reanálisis del origen sale BLOQUEADO con el DIRECTA en juego")
o = base()
r = reencargar_origen(o, AHORA, bloqueado=True)
INFO["a_reencargo_aceptado"] = r["ok"]
INFO["a_estado_final_DIRECTA"] = seguir_directa(o, AHORA, "a")

print("b) el reanálisis del origen sale bien (S2) con el DIRECTA en juego")
o = base()
r = reencargar_origen(o, AHORA, bloqueado=False)
vivos = sorted(k for k, x in o.expedientes.items() if x["estado"] in ("VALIDADA", "COMPARADA"))
print("   en juego:", vivos, "| sobres:", [o.expedientes[k]["sobre"]["event_id"] for k in vivos])
INFO["b_dos_expedientes_del_mismo_candidato_en_juego"] = vivos == ["EXP-0001", "EXP-DD-01"]
INFO["b_estado_final_DIRECTA"] = seguir_directa(o, AHORA, "b")

print("c) como a), sin reapertura del operador: se cumple su condición FECHA y el gestor reencarga")
T7 = "2026-11-07T10:00:00+00:00"
o = base(cond=[{"tipo": "FECHA", "fecha": "2026-11-07"}])
r = reencargar_origen(o, T7, bloqueado=True, reabre=False)
INFO["c_reencargo_aceptado"] = r["ok"]

print("d) control: el origen reencargado ANTES de abrir el DIRECTA")
o = nuevo()
assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
assert o.entregar_sobre("EXP-0001", sobre_para(1, None), AHORA)["ok"]
assert o.observar("EXP-0001", COND_OBS, "el operador lo aparta", "OPERADOR", AHORA)["ok"]
assert o.reabrir("EXP-0001", "el operador pide un análisis nuevo", "OPERADOR", AHORA)["ok"]
e2 = encargo(1)
e2["event_id"] = "EV-ENC-0001-B"
assert o.emitir_encargo("EXP-0001", e2, "GESTOR_TACTICA", AHORA)["ok"]
r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
print("   abrir_directa con el origen en reanálisis:", r["ok"], r["codigo"], r["motivo"][:80])
chk("d_control_origen_en_reanalisis_O06", not r["ok"] and r["codigo"] == "O-06", r)

for k, v in INFO.items():
    print("INFO ", k, v)
# lo que espera esta sonda (§3 del Documento 0 y T-27): el mismo candidato no puede estar en juego con un análisis que su
# reanálisis ya superó, y menos si ese reanálisis lo bloqueó
chk("a_el_DIRECTA_no_llega_a_AUTORIZADA_con_un_analisis_que_el_origen_bloqueo", INFO["a_estado_final_DIRECTA"] not in ("PROPUESTA", "AUTORIZADA"),
    INFO["a_estado_final_DIRECTA"])
chk("b_no_quedan_dos_expedientes_del_mismo_candidato_en_juego", not INFO["b_dos_expedientes_del_mismo_candidato_en_juego"])
sys.exit(fin())
