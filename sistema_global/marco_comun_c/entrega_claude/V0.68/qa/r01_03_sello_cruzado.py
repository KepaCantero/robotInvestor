"""QA r01 · sonda 03: misma raíz que la 02. El DIRECTA hereda el encargo nuevo del origen (con otro sello de K), así que cuando K
reemplaza (anula) el sello con el que se hizo el análisis reutilizado, el DIRECTA no caduca y sigue compitiendo y proponiéndose
con datos anulados. Un expediente normal con ese sobre sí caduca (contraste al final)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, ENTRADA, SALIDA, chk, dim, encargo, fin, nuevo, sobre_para  # noqa: E402
from pruebas_orquestador import S1, S2  # noqa: E402
from pruebas_k import CTX as CTX_K, construir as construir_k  # noqa: E402

o = nuevo()
assert o.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
assert o.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]            # E1, sello K-20261105-001
assert o.entregar_sobre("EXP-0001", sobre_para(1, None), AHORA)["ok"]                      # S1 cita K-20261105-001
assert o.observar("EXP-0001", [{"tipo": "FECHA", "fecha": "2026-11-20"}], "el operador lo aparta", "OPERADOR", AHORA)["ok"]
assert o.registrar_sello(S2, AHORA)["ok"]   # K publica un corte nuevo
assert o.reabrir("EXP-0001", "el operador pide un análisis con datos nuevos", "OPERADOR", AHORA)["ok"]
e2 = encargo(1, corte="2026-11-06", sello="K-20261106-001")
e2["event_id"] = "EV-ENC-0001-B"
r = o.emitir_encargo("EXP-0001", e2, "GESTOR_TACTICA", AHORA)
assert r["ok"], r
assert o.observar("EXP-0001", [{"tipo": "FECHA", "fecha": "2026-11-20"}], "el operador lo aparta otra vez", "OPERADOR", AHORA)["ok"]
r = o.abrir_directa("EXP-DD-01", "COR-DD-01", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001")
print("abrir_directa:", r["ok"], r["codigo"], "encargo_actual:", o.expedientes.get("EXP-DD-01", {}).get("encargo_actual"))
nuevo_k1 = construir_k(ctx={**CTX_K, "secuencia": 2, "reemplaza_a": "K-20261105-001"})[1]["sello"]
r = o.registrar_sello(nuevo_k1, AHORA)
print("K reemplaza K-20261105-001:", r["ok"], r["codigo"], "sello viejo:", o.sellos["K-20261105-001"]["estado"])
e = o.expedientes["EXP-DD-01"]
chk("el_DIRECTA_con_el_analisis_de_un_sello_anulado_caduca", e["estado"] == "CADUCADA", e["estado"])
r = o.comparar(["EXP-DD-01"], "D", AHORA)
print("comparar:", r["ok"], r["codigo"], r["motivo"][:90])
if r["ok"]:
    r = o.proponer("EXP-DD-01", ENTRADA, SALIDA, "BROKER", AHORA, dim(o, "EXP-DD-01"))
    print("proponer:", r["ok"], r["codigo"], r["motivo"][:90])
    chk("no_se_propone_con_un_analisis_de_sello_anulado", not r["ok"], r)

# contraste: un expediente normal con ese mismo sobre caduca al reemplazarse el sello
o2 = nuevo()
assert o2.detectar("EXP-0001", "COR-0001", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
assert o2.emitir_encargo("EXP-0001", encargo(1), "GESTOR_TACTICA", AHORA)["ok"]
assert o2.entregar_sobre("EXP-0001", sobre_para(1, None), AHORA)["ok"]
assert o2.registrar_sello(nuevo_k1, AHORA)["ok"]
chk("contraste_expediente_normal_caduca", o2.expedientes["EXP-0001"]["estado"] == "CADUCADA", o2.expedientes["EXP-0001"]["estado"])
sys.exit(fin())
