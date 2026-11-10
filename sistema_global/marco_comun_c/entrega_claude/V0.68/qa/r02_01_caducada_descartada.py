"""QA r02 · sonda 01 (variante de r01_08, H-03): §4.1 regla 4, «una propuesta caducada no se ejecuta: vuelve a EN_ANÁLISIS o pasa
a DESCARTADA». La r01 quitó CADUCADA de REUTILIZABLE_DESDE. Pero CADUCADA -> DESCARTADA es una transición permitida (T) y
DESCARTADA sí es reutilizable; _salida_no_operador no cuenta la caducidad del Orquestador como apartado. ¿Basta con que el Broker
(o el gestor, o el operador) pase la propuesta caducada a DESCARTADA para que la vía DIRECTA la vuelva a sacar a VALIDADA y se
proponga otra vez sin análisis nuevo? (Datos SIMULADOS.)"""
import copy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, ENTRADA, SALIDA, chk, dim, fin, hasta, nuevo  # noqa: E402,F401
from pruebas_orquestador import CART_E  # noqa: E402

A2 = "2026-11-08T13:00:00+00:00"   # pasó la ventana de la propuesta (12:00), no la vigencia del sobre (18:00)
CE = {**ENTRADA, "ventana_hasta": "2026-11-08T17:00:00+00:00"}
CART = {**copy.deepcopy(CART_E), "fecha_hora": "2026-11-08T12:55:00+00:00"}


def caso(quien):
    o = nuevo()
    hasta(o, "PROPUESTA", 1)
    assert o.barrer(A2)["ok"] and o.expedientes["EXP-0001"]["estado"] == "CADUCADA"
    r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", A2, analisis="EV-SOB-0001")
    print(f"[{quien}] directa desde CADUCADA:", r["ok"], r["codigo"])
    r = o.descartar("EXP-0001", "la propuesta caducó y el Broker la descarta (regla 4)", quien, A2)
    print(f"[{quien}] CADUCADA -> DESCARTADA:", r["ok"], r["codigo"])
    r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", A2, analisis="EV-SOB-0001")
    print(f"[{quien}] abrir_directa por D con el análisis de la propuesta caducada y descartada:", r["ok"], r["codigo"], r["motivo"][:80])
    propuesta = False
    if r["ok"]:
        assert o.descartar("EXP-0002", "el operador descarta al rival", "OPERADOR", A2)["ok"]
        r = o.comparar(["EXP-DD-01"], "D", A2)
        print(f"[{quien}] comparar:", r["ok"], r["codigo"], "ganador:", r.get("ganador"))
        if r["ok"] and not o.expedientes["EXP-DD-01"]["comparacion"]["ganador"]:
            o.elegir("EXP-DD-01", "OPERADOR", "elección de la sonda", A2)
        r = o.proponer("EXP-DD-01", CE, SALIDA, "BROKER", A2, dim(o, "EXP-DD-01", entrada=CE, cartera=CART, ahora=A2))
        print(f"[{quien}] proponer otra vez el mismo análisis:", r["ok"], r["codigo"], r["motivo"][:80], "| integridad:", o.integridad())
        propuesta = r["ok"]
    chk(f"{quien}_la_propuesta_caducada_y_descartada_no_vuelve_sin_analisis_nuevo", not propuesta)


for quien in ("BROKER", "GESTOR_TACTICA", "OPERADOR"):
    caso(quien)

# la misma puerta con el propio DIRECTA: un DIRECTA cuya propuesta caduca y se descarta deja su análisis otra vez reutilizable
o = nuevo()
hasta(o, "VALIDADA", 1)
assert o.observar("EXP-0001", [{"tipo": "FECHA", "fecha": "2026-11-20"}], "el operador lo aparta", "OPERADOR", AHORA)["ok"]
assert o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")["ok"]
assert o.comparar(["EXP-DD-01"], "D", AHORA)["ok"]
assert o.proponer("EXP-DD-01", ENTRADA, SALIDA, "BROKER", AHORA, dim(o, "EXP-DD-01"))["ok"]
assert o.barrer(A2)["ok"] and o.expedientes["EXP-DD-01"]["estado"] == "CADUCADA"
r = o.analisis_vigentes(A2)
print("registro con el DIRECTA caducado:", [(x["analisis"], x["reutilizable"], x["motivo"]) for x in r])
assert o.descartar("EXP-DD-01", "caducó: el Broker lo descarta", "BROKER", A2)["ok"]
r = o.abrir_directa("EXP-DD-02", "COR-DD-02", "TACTICA", "D", "BROKER", A2, analisis="EV-SOB-0001")
print("segundo DIRECTA con el análisis de la propuesta caducada y descartada:", r["ok"], r["codigo"], r["motivo"][:80])
chk("DIRECTA_caducado_y_descartado_no_devuelve_su_analisis", not r["ok"], r)
sys.exit(fin())
