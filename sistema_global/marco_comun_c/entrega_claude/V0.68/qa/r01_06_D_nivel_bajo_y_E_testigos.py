"""QA r01 · sonda 06:
  a) entrada por D sin análisis reutilizable: el encargo de «nivel bajo» (N1) solo admite decisiones que proponer() rechaza
     (T-26: solo ABRIR_POSICION y AUMENTAR llevan a una orden, y exigen N2). ¿Puede ese expediente llegar a PROPUESTA?
  b) entrada por E con un testigo (T-36): un candidato apartado por su gestor que habría ganado. ¿Se respeta?
  c) entrada por E con otro candidato ya COMPARADA en la cartera: ¿se devuelve a D?
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import (AHORA, ENTRADA, SALIDA, chk, descartado_por_operador, dim, enc_directa, fin, foto, hasta, nuevo,  # noqa: E402
                       sobre_directa)
from validar_encargo import NIVEL_MIN_POR_DECISION  # noqa: E402

MOT = "solo hay un candidato en la cartera: lo pidió el operador"

# a) D sin análisis: el encargo de nivel bajo
o = nuevo()
for dec in ("ABRIR_POSICION", "AUMENTAR"):
    r = o.abrir_directa("EXP-DD-05", "COR-EXP-DD-05", "TACTICA", "D", "BROKER", AHORA, encargo=enc_directa("EXP-DD-05", 5, nivel="N1", decision=dec))
    print(f"D + encargo N1 {dec}:", r["ok"], r["codigo"], r["motivo"][:90])
r = o.abrir_directa("EXP-DD-05", "COR-EXP-DD-05", "TACTICA", "D", "BROKER", AHORA, encargo=enc_directa("EXP-DD-05", 5, nivel="N2"))
print("D + encargo N2 ABRIR_POSICION:", r["ok"], r["codigo"], r["motivo"][:90])
r = o.abrir_directa("EXP-DD-05", "COR-EXP-DD-05", "TACTICA", "D", "BROKER", AHORA, encargo=enc_directa("EXP-DD-05", 5, nivel="N1", decision="EXPLORAR"))
assert r["ok"], r
s = sobre_directa("EXP-DD-05", 5)
s["payload"]["identificacion"]["nivel_analisis"] = "N1"
s["event_id"] = "EV-SOB-0005"
r = o.entregar_sobre("EXP-DD-05", s, AHORA)
assert r["ok"], r
assert o.comparar(["EXP-DD-05"], "D", AHORA)["ok"]
r = o.proponer("EXP-DD-05", ENTRADA, SALIDA, "BROKER", AHORA, dim(o, "EXP-DD-05"))
print("proponer el DIRECTA por D con el análisis de nivel bajo:", r["ok"], r["codigo"], r["motivo"][:100])
print("NIVEL_MIN_POR_DECISION:", NIVEL_MIN_POR_DECISION)
chk("D_con_encargo_de_nivel_bajo_puede_acabar_en_una_decision", r["ok"],
    "con N1 solo caben decisiones que proponer() rechaza: la entrada por D sin análisis no puede acabar en una orden")

# b) E con un testigo que habría ganado
o = nuevo()
descartado_por_operador(o, 1)
hasta(o, "VALIDADA", 3)
assert o.observar("EXP-0003", [{"tipo": "FECHA", "fecha": "2026-11-20"}], "el gestor lo deja para más adelante", "GESTOR_TACTICA", AHORA)["ok"]
r = o.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "E", "BROKER", AHORA, analisis="EV-SOB-0001", motivo=MOT)
e = o.expedientes.get("EXP-DE-01") or {}
c = e.get("comparacion") or {}
print("E con testigo:", r["ok"], r["codigo"], "ganador:", c.get("ganador"), "testigos:", c.get("testigos"), "apartado_mejor:", c.get("apartado_mejor"))
chk("E_con_testigo_lo_incluye", c.get("testigos") == ["EXP-0003"], c)
chk("E_con_testigo_mejor_no_da_ganador", not c.get("ganador") or c.get("apartado_mejor") is None, c)

# c) E con otro candidato ya COMPARADA
o = nuevo()
descartado_por_operador(o, 1)
hasta(o, "COMPARADA", 3)   # EXP-0003 y EXP-0004 COMPARADA
antes = foto(o)
r = o.abrir_directa("EXP-DE-01", "COR-DE-01", "TACTICA", "E", "BROKER", AHORA, analisis="EV-SOB-0001", motivo=MOT)
chk("E_con_candidatos_COMPARADA_se_devuelve_a_D", not r["ok"] and r.get("devolver_a") == "D" and set(r.get("faltan", [])) == {"EXP-0003", "EXP-0004"}
    and foto(o) == antes, r)
sys.exit(fin())
