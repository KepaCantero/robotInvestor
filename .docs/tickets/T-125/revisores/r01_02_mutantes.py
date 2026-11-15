"""QA r01 de T-125 (revisor sin contexto): mutantes de `fiabilidad_fuentes`, `pronosticos_de_fuentes` y del alta en F2,
contra `tests/test_t125_fiabilidad_fuentes.py` (las 12 pruebas del ticket, que son las que el mapa cita para PB-46).

Uso:  python .docs/tickets/T-125/revisores/r01_02_mutantes.py <copia desechable de bloque_a, con «_mut» en la ruta>
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "_mut" in str(COPIA) and (COPIA / "11_Ejecutor" / "bloque_a").is_dir()
EV, ORQ = "11_Ejecutor/bloque_a/evaluador.py", "11_Ejecutor/bloque_a/orquestacion.py"
PRUEBAS = ["tests/test_t125_fiabilidad_fuentes.py"]
MUTANTES = [
    ("K01", "el alta en F2 deja de guardar el bloque pronostico_fuente de la pieza", ORQ,
     'clm["pronostico_fuente"] = dict(p["pronostico_fuente"])', 'pass'),
    ("K02", "la FUE- no anota el msg_id del CT-19", ORQ, '"comunicado_ct19": msg["msg_id"]', '"comunicado_ct19": None'),
    ("K03", "sin contracción n / (n + k)", EV, "bss_c = None if bss is None else n / (n + k) * bss", "bss_c = bss"),
    ("K04", "sin «una vez al mes»", EV, 'if any(e.get("tipo_entrada") == "FUE" and e.get("periodo") == periodo',
     'if False and any(e.get("tipo_entrada") == "FUE" and e.get("periodo") == periodo'),
    ("K05", "sin ventana de 24 meses", EV, "emision < objetivo <= corte and objetivo >= desde", "emision < objetivo <= corte"),
    ("K06", "sin el control de antigüedad del cierre (H2)", EV, "if pd.Timestamp(fecha_dato) < objetivo - pd.Timedelta(",
     "if False and pd.Timestamp(fecha_dato) < objetivo - pd.Timedelta("),
    ("K07", "cuenta pronósticos no vencidos", EV, "emision < objetivo <= corte and", "emision < objetivo and"),
    ("K08", "admite fecha de emisión igual a la objetivo", EV, "emision < objetivo <= corte and", "emision <= objetivo <= corte and"),
    ("K09", "prob sin declarar = 0,5 en vez de la configuración", EV, 'prob = float(par["prob_sin_declarar"])', "prob = 0.5"),
    ("K10", "n_min uno menos", EV, 'if n < int(par["n_min"]):', 'if n < int(par["n_min"]) - 1:'),
    ("K11", "puntos sin acotar a [0, 20]", EV, "min(maximo, max(0.0, neutro * (1 + bss_c)))", "neutro * (1 + bss_c)"),
    ("K12", "admite probabilidad 0 y 1", EV, "not 0 < prob < 1:", "not 0 <= prob <= 1:"),
    ("K13", "«dentro» con bordes abiertos", EV, "ocurre = umbral[0] <= valor <= umbral[1]\n            else:",
     "ocurre = umbral[0] < valor < umbral[1]\n            else:"),
    ("K14", "referencia ingenua fija en 0,4 (ignora la configuración)", EV,
     'k, neutro, maximo, ref = float(par["k_contraccion"]), float(par["puntos_neutro"]), float(par["puntos_max"]), float(par["referencia"])',
     'k, neutro, maximo, ref = float(par["k_contraccion"]), float(par["puntos_neutro"]), float(par["puntos_max"]), 0.4'),
]
for mid, que, rel, viejo, nuevo in MUTANTES:
    ruta = COPIA / rel
    original = ruta.read_text(encoding="utf-8")
    assert original.count(viejo) == 1, f"{mid}: el texto no aparece exactamente una vez"
    ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *PRUEBAS], cwd=COPIA / "11_Ejecutor",
                           capture_output=True, text=True)
    finally:
        ruta.write_text(original, encoding="utf-8")
    assert r.returncode in (0, 1), r.stdout[-1500:] + r.stderr[-1500:]
    print(f"{mid} | {que} | {'MUERTO · ' + r.stdout.strip().splitlines()[-1] if r.returncode else 'VIVO'}", flush=True)
