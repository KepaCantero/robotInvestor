"""QA r01 · sonda 09: argumentos que abrir_directa() ignora sin decirlo.
  a) por D con un análisis reutilizable Y un encargo: se reutiliza y el encargo se descarta en silencio;
  b) por D con un análisis NO reutilizable Y un encargo: se encarga y el análisis pedido se descarta en silencio
     (analisis_ref queda None), aunque venga de una consulta que lo citaba."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, chk, descartado_por_operador, enc_directa, fin, hasta, nuevo  # noqa: E402

o = nuevo()
descartado_por_operador(o, 1)
r = o.abrir_directa("EXP-DD-05", "COR-EXP-DD-05", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001",
                    encargo=enc_directa("EXP-DD-05", 5, nivel="N1", decision="EXPLORAR"))
print("a)", r)
chk("a_D_con_analisis_y_encargo_no_ignora_el_encargo_en_silencio", not r["ok"] or "encargo" in r, r)

o = nuevo()
hasta(o, "VALIDADA", 1)   # EV-SOB-0001 en juego: no reutilizable
r = o.abrir_directa("EXP-DD-05", "COR-EXP-DD-05", "TACTICA", "D", "BROKER", AHORA, analisis="EV-SOB-0001",
                    encargo=enc_directa("EXP-DD-05", 5, nivel="N1", decision="EXPLORAR"))
e = o.expedientes.get("EXP-DD-05") or {}
print("b)", r["ok"], r["codigo"], "analisis_ref:", e.get("analisis_ref"), "estado:", e.get("estado"))
chk("b_D_con_analisis_no_reutilizable_dice_por_que_no_lo_usa", not r["ok"] or "reutiliza" in r and r.get("motivo_no_reutiliza"), r)
sys.exit(fin())
