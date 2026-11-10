"""QA r01 · sonda 04: tipos inesperados, None, NaN, listas, dicts y rechazos en abrir_directa() y consultar(): ninguno debe lanzar
una excepción ni dejar el estado cambiado (salvo el reloj y los avisos). También: repetir, reordenar y la hora en el borde."""
import copy
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, chk, descartado_por_operador, enc_directa, fin, foto, nuevo  # noqa: E402

o = nuevo()
descartado_por_operador(o, 1)
base = foto(o)
MOT = "solo hay un candidato en la cartera: lo pidió el operador"
raros = [None, [], {}, ["C"], {"C": 1}, 1, 1.5, math.nan, math.inf, True, "", " ", "C ", "c", "EV-SOB-0001\n", "x" * 70, b"C"]


BASE_O = copy.deepcopy(o)
ACEPTADOS = []


def prueba(nombre, fn):
    """fn recibe un Orquestador nuevo (copia de la base). Un valor raro que resulta válido puede aceptarse (se lista aparte);
    lo que no puede pasar es una excepción o un rechazo que deje el estado cambiado."""
    global o
    o = copy.deepcopy(BASE_O)
    try:
        r = fn()
    except Exception as ex:   # noqa: BLE001
        chk(nombre + "_no_lanza", False, f"{type(ex).__name__}: {ex}")
        return None
    if isinstance(r, dict) and r.get("ok") is True:
        ACEPTADOS.append((nombre, r.get("codigo")))
        return r
    cambio = foto(o) != base
    chk(nombre, isinstance(r, dict) and r.get("ok") is False and not cambio, (r, "estado cambió" if cambio else ""))
    return r


for i, v in enumerate(raros):
    prueba(f"bloque_raro_{i}_{type(v).__name__}", lambda v=v: o.abrir_directa("EXP-Z", "COR-Z", "TACTICA", v, "BROKER", AHORA, analisis="EV-SOB-0001"))
    prueba(f"cartera_rara_{i}_{type(v).__name__}", lambda v=v: o.abrir_directa("EXP-Z", "COR-Z", v, "D", "BROKER", AHORA, analisis="EV-SOB-0001"))
    prueba(f"actor_raro_{i}_{type(v).__name__}", lambda v=v: o.abrir_directa("EXP-Z", "COR-Z", "TACTICA", "D", v, AHORA, analisis="EV-SOB-0001"))
    if v is not None:
        prueba(f"analisis_raro_{i}_{type(v).__name__}", lambda v=v: o.abrir_directa("EXP-Z", "COR-Z", "TACTICA", "D", "BROKER", AHORA, analisis=v))
        prueba(f"consulta_id_raro_{i}_{type(v).__name__}", lambda v=v: o.abrir_directa("EXP-Z", "COR-Z", "TACTICA", "D", "BROKER", AHORA,
                                                                                         analisis="EV-SOB-0001", consulta_id=v))
        prueba(f"motivo_E_raro_{i}_{type(v).__name__}", lambda v=v: o.abrir_directa("EXP-Z", "COR-Z", "TACTICA", "E", "BROKER", AHORA,
                                                                                     analisis="EV-SOB-0001", motivo=v))
        prueba(f"encargo_raro_{i}_{type(v).__name__}", lambda v=v: o.abrir_directa("EXP-Z", "COR-Z", "TACTICA", "C", "BROKER", AHORA, encargo=v))
    prueba(f"ahora_raro_{i}_{type(v).__name__}", lambda v=v: o.abrir_directa("EXP-Z", "COR-Z", "TACTICA", "D", "BROKER", v, analisis="EV-SOB-0001"))

# encargo por C con payload raro o con nivel raro por D
for i, v in enumerate(raros):
    enc = enc_directa("EXP-Z", 9)
    enc["payload"]["nivel_analisis"] = v
    prueba(f"D_encargo_nivel_raro_{i}", lambda enc=enc: o.abrir_directa("EXP-Z", "COR-EXP-Z", "TACTICA", "D", "BROKER", AHORA, encargo=enc))
    enc2 = enc_directa("EXP-Z", 9)
    enc2["payload"] = v
    prueba(f"C_encargo_payload_raro_{i}", lambda enc=enc2: o.abrir_directa("EXP-Z", "COR-EXP-Z", "TACTICA", "C", "BROKER", AHORA, encargo=enc))

# consultas raras
CB = {"consulta_id": "CON-Z", "correlation_id": "COR-CON-Z", "tipo": "COMPARAR", "bloque": "D", "cartera": "TACTICA",
      "analisis": ["EV-SOB-0001"], "pregunta": "¿Cuál de estos análisis rinde más que el benchmark?"}
for campo in CB:
    for i, v in enumerate(raros):
        c = {**copy.deepcopy(CB), campo: v}
        if c == CB:
            continue
        prueba(f"consulta_{campo}_raro_{i}_{type(v).__name__}", lambda c=c: o.consultar(c, "BROKER", AHORA))
for i, v in enumerate(raros):
    prueba(f"consulta_entera_rara_{i}", lambda v=v: o.consultar(v, "BROKER", AHORA))
prueba("consulta_51_analisis", lambda: o.consultar({**CB, "analisis": [f"EV-SOB-{k:04d}" for k in range(51)]}, "BROKER", AHORA))
prueba("consulta_analisis_no_str", lambda: o.consultar({**CB, "analisis": [1]}, "BROKER", AHORA))

print("aceptados (valores válidos aunque raros):", ACEPTADOS)
o = copy.deepcopy(BASE_O)
# el borde del valid_until del sobre (2026-11-08T18:00:00Z): justo en él vale, un segundo después no
vu = o.expedientes["EXP-0001"]["sobre"]["valid_until"]
o2 = copy.deepcopy(o)
r = o2.abrir_directa("EXP-B1", "COR-B1", "TACTICA", "D", "BROKER", vu, analisis="EV-SOB-0001")
print("en el borde exacto:", vu, r["ok"], r["codigo"], r["motivo"][:80])
o3 = copy.deepcopy(o)
r = o3.abrir_directa("EXP-B1", "COR-B1", "TACTICA", "D", "BROKER", vu.replace(":00+00:00", ":01+00:00"), analisis="EV-SOB-0001")
chk("un_segundo_despues_del_valid_until_no", not r["ok"] and r["codigo"] == "O-10", r)

# idempotencia: la misma apertura dos veces
o4 = copy.deepcopy(o)
r1 = o4.abrir_directa("EXP-I1", "COR-I1", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
r2 = o4.abrir_directa("EXP-I1", "COR-I1", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
chk("repetir_la_apertura_no_crea_otra_ni_cambia_nada", r1["ok"] and not r2["ok"] and r2["codigo"] == "O-03", (r1, r2))
# reloj hacia atrás
r = o4.abrir_directa("EXP-I2", "COR-I2", "TACTICA", "C", "BROKER", "2026-11-05T09:00:00+00:00", encargo=enc_directa("EXP-I2", 8))
chk("reloj_hacia_atras_O16", not r["ok"] and r["codigo"] == "O-16" and "EXP-I2" not in o4.expedientes, r)
sys.exit(fin())
