"""QA r04 · sonda 03 (H-14, decisión de documentarlo): un rechazo de abrir_directa() por C caduca encargos vencidos de otros
expedientes «como haría el siguiente barrer». Pero @_seguro no deja que una llamada rechazada adelante el reloj del Orquestador.
Si la llamada rechazada trae un `ahora` adelantado (p. ej. un error del Broker), ¿caduca un encargo que con el reloj del
Orquestador sigue vigente? Y, después, ¿una entrega legítima en plazo se rechaza? Se compara con emitir_encargo() y
entregar_sobre() (lo mismo antes de T-80) y con consultar() (no caduca nada). (Datos SIMULADOS.)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, chk, encargo, enc_directa, fin, nuevo, sobre_para  # noqa: E402

FUTURO = "2026-11-09T09:00:00+00:00"   # pasado el valid_until del encargo de EXP-0001
DESPUES = "2026-11-06T09:05:00+00:00"  # en plazo para EXP-0001


def base():
    o = nuevo()
    assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
    assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
    return o


def caso(nombre, llamada):
    o = base()
    vu = o.encargos["EV-ENC-0001"]["valid_until"]
    r = llamada(o)
    est = o.encargos["EV-ENC-0001"]["estado"]
    print(f"{nombre}: {r['ok']} {r['codigo']} | reloj {o.ultimo_ahora} | encargo de EXP-0001 (valid_until {vu}): {est}")
    r2 = o.entregar_sobre("EXP-0001", sobre_para(1, None), DESPUES)
    print(f"   entrega legítima a las {DESPUES[11:16]}: {r2['ok']} {r2['codigo']} {r2['motivo'][:60]}")
    return est, r2


mala = enc_directa("EXP-DD-01", 5)
mala["payload"]["cartera_destino"] = "TRADING"
est, r2 = caso("abrir_directa por C rechazada con ahora adelantado",
               lambda o: o.abrir_directa("EXP-DD-01", "COR-EXP-DD-01", "TACTICA", "C", "BROKER", FUTURO, encargo=mala))
chk("abrir_directa_rechazada_no_caduca_lo_que_el_reloj_aun_no_vencio", est == "EN_CURSO" and r2["ok"], (est, r2["codigo"]))
est, r2 = caso("antes de T-80: emitir_encargo rechazado con ahora adelantado",
               lambda o: o.emitir_encargo("EXP-0001", {**encargo(1), "event_id": "EV-ENC-0001-X", "expediente_id": "EXP-9999"}, "GESTOR_TACTICA", FUTURO))
print("INFO  emitir_encargo hace lo mismo (anterior a T-80):", est)
est, r2 = caso("consultar rechazada con ahora adelantado",
               lambda o: o.consultar({"consulta_id": "CON-1", "correlation_id": "COR-1", "tipo": "OTRO", "bloque": "C", "cartera": None,
                                      "analisis": [], "pregunta": "una pregunta suficientemente larga"}, "BROKER", FUTURO))
chk("consultar_no_caduca_nada", est == "EN_CURSO" and r2["ok"], (est, r2["codigo"]))
sys.exit(fin())
