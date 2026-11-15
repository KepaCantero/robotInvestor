"""QA r03 de T-125 (revisor sin contexto): mutantes de lo que cambia la r03 (fechas solo ISO, `variable` resoluble, umbral
como número, dirección no textual, `run_id` en RC), contra las pruebas del ticket (`test_t125_r03.py`, `test_t125_r02.py` y
`test_t125_fiabilidad_fuentes.py`).

Uso, desde la raíz:  python .docs/tickets/T-125/revisores/r03_04_mutantes.py <copia desechable de bloque_a, con «_mut» en la ruta>
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "_mut" in str(COPIA) and (COPIA / "11_Ejecutor" / "bloque_a").is_dir()
EV, ORQ = "11_Ejecutor/bloque_a/evaluador.py", "11_Ejecutor/bloque_a/orquestacion.py"
PRUEBAS = ["tests/test_t125_r03.py", "tests/test_t125_r02.py", "tests/test_t125_fiabilidad_fuentes.py"]
MUTANTES = [
    ("M01", "sin el filtro ISO (vuelve a pd.Timestamp de cualquier texto)", EV,
     "    if not RE_FECHA_ISO.fullmatch(v.strip()):", "    if False:"),
    ("M02", "el filtro admite también AAAAMMDD", EV,
     'RE_FECHA_ISO = re.compile(r"\\d{4}-\\d{2}-\\d{2}', 'RE_FECHA_ISO = re.compile(r"(?:\\d{8}|\\d{4}-\\d{2}-\\d{2})'),
    ("M03", "el filtro no admite zona horaria", EV, '(?:Z|[+-]\\d{2}:?\\d{2})?")', '")'),
    ("M04", "cualquier variable es resoluble", EV, "return isinstance(variable, str) and variable.strip().lower() in",
     "return True or isinstance(variable, str) and variable.strip().lower() in"),
    ("M05", "la variable sin strip", EV, "variable.strip().lower() in", "variable.lower() in"),
    ("M06", "la variable sin lower", EV, "variable.strip().lower() in", "variable.strip() in"),
    ("M07", "el Evaluador no mira la variable (solo el alta)", EV,
     'if not variable_resoluble(variable, par["variables_nivel"]) or not isinstance(direccion, str):', "if not isinstance(direccion, str):"),
    ("M08", "el Evaluador no mira si la dirección es texto", EV,
     'if not variable_resoluble(variable, par["variables_nivel"]) or not isinstance(direccion, str):',
     'if not variable_resoluble(variable, par["variables_nivel"]):'),
    ("M09", "el alta no mira la variable", EV, "    if not variable_resoluble(variable, variables_nivel):\n", "    if False:\n"),
    ("M10", "el alta no mira si la dirección es texto", EV,
     '    if not isinstance(direccion, str):\n        return f"dirección no reconocida: {direccion!r}"\n    if direccion in',
     '    if False:\n        return f"dirección no reconocida: {direccion!r}"\n    if direccion in'),
    ("M11", "deduplicación con repr(umbral) (como en la r02)", EV,
     "umbral_n = tuple(float(x) for x in umbral) if isinstance(umbral, list) else float(umbral)", "umbral_n = repr(umbral)"),
    ("M12", "el C5 no pasa el run_id a fiabilidad_fuentes", EV, "fiabilidad = self.fiabilidad_fuentes(as_of, run_id)",
     "fiabilidad = self.fiabilidad_fuentes(as_of)"),
    ("M13", "la petición al Motor sin run_id", EV, '"AG-20", run_id)   # T-125 r03 (H-13)', '"AG-20", None)   # T-125 r03 (H-13)'),
    ("M14", "el alta del ciclo usa la lista por defecto, no la de la configuración", ORQ,
     'parametro(self.cfg, "fiabilidad_fuentes.variables_nivel"))', "None)"),
    ("M15", "la fecha sin strip antes del filtro (más estricto)", EV,
     "    if not RE_FECHA_ISO.fullmatch(v.strip()):", "    if not RE_FECHA_ISO.fullmatch(v):"),
    ("M16", "la lista de la configuración sin lower", EV, "{str(x).lower() for x in variables_nivel}", "{str(x) for x in variables_nivel}"),
]
for mid, que, rel, viejo, nuevo in MUTANTES:
    ruta = COPIA / rel
    original = ruta.read_text(encoding="utf-8")
    assert original.count(viejo) == 1, f"{mid}: el texto no aparece exactamente una vez"
    ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], cwd=COPIA / "11_Ejecutor",
                           capture_output=True, text=True)
    finally:
        ruta.write_text(original, encoding="utf-8")
    assert r.returncode in (0, 1), r.stdout[-1500:] + r.stderr[-1500:]
    print(f"{mid} | {que} | {'MUERTO · ' + r.stdout.strip().splitlines()[-1] if r.returncode else 'VIVO'}", flush=True)
