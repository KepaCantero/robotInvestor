"""QA r01 de T-134 (revisor sin contexto): mutantes de lo que cambia T-134 (`_finito`, `RE_FECHA_ISO`, `variables_nivel` en
`evaluador.py` y `orquestacion.py`) y los M12 y M14 de la r03 de T-125 adaptados al código nuevo (el `r03_04_mutantes.py` de
la r03 ya no aplica: los textos que muta han cambiado), contra `test_t134_r03_t125.py` y las pruebas de T-125.

Uso, desde la raíz:  python .docs/tickets/T-134/revisores/r01_02_mutantes.py <copia desechable de bloque_a, con «_mut» en la ruta>
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "_mut" in str(COPIA) and (COPIA / "11_Ejecutor" / "bloque_a").is_dir()
EV, ORQ = "11_Ejecutor/bloque_a/evaluador.py", "11_Ejecutor/bloque_a/orquestacion.py"
PRUEBAS = ["tests/test_t134_r03_t125.py", "tests/test_t125_r03.py", "tests/test_t125_r02.py", "tests/test_t125_fiabilidad_fuentes.py"]
MUTANTES = [
    ("T01", "_finito da True con un desbordamiento", EV, "    except OverflowError:\n        return False", "    except OverflowError:\n        return True"),
    ("T02", "_finito sin capturar el desbordamiento", EV, "    try:\n        return math.isfinite(x)\n    except OverflowError:\n        return False",
     "    return math.isfinite(x)"),
    ("T03", "_numero_finito con math.isfinite (como antes)", EV,
     "return not isinstance(x, bool) and isinstance(x, (int, float)) and _finito(x)",
     "return not isinstance(x, bool) and isinstance(x, (int, float)) and math.isfinite(x)"),
    ("T04", "_prob_valida con math.isfinite (como antes)", EV, "and _finito(v) and 0.0 <= float(v) <= 1.0",
     "and math.isfinite(v) and 0.0 <= float(v) <= 1.0"),
    ("T05", "RE_FECHA_ISO con \\d (cifras Unicode)", EV, 'RE_FECHA_ISO = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}(',
     'RE_FECHA_ISO = re.compile(r"\\d{4}-\\d{2}-\\d{2}('),
    ("T06", "zona horaria también sin hora", EV, '(?:Z|[+-][0-9]{2}:?[0-9]{2})?)?")', ')?(?:Z|[+-][0-9]{2}:?[0-9]{2})?")'),
    ("T07", "el Evaluador no valida variables_nivel al crearse", EV, "        variables_nivel(cfg)         # T-134 (H-17)\n", ""),
    ("T08", "variables_nivel admite un texto suelto", EV, "if not isinstance(v, list) or not v or", "if not isinstance(v, (list, str)) or not v or"),
    ("T09", "variables_nivel admite textos vacíos", EV, "all(isinstance(x, str) and x.strip() for x in v)", "all(isinstance(x, str) for x in v)"),
    ("T10", "pronosticos_de_fuentes con _numero_finito → math.isfinite en el umbral", EV,
     "                if not _numero_finito(umbral):\n                    continue",
     "                if isinstance(umbral, bool) or not isinstance(umbral, (int, float)) or not math.isfinite(umbral):\n                    continue"),
    ("T11", "pronosticos_de_fuentes: el rango con math.isfinite", EV,
     "all(_numero_finito(x) for x in umbral) and umbral[0] < umbral[1]):\n                    continue",
     "all(isinstance(x, (int, float)) and math.isfinite(x) for x in umbral) and umbral[0] < umbral[1]):\n                    continue"),
    ("T12", "el alta: el rango con math.isfinite", EV,
     "forma = isinstance(umbral, list) and len(umbral) == 2 and all(_numero_finito(x) for x in umbral)",
     "forma = isinstance(umbral, list) and len(umbral) == 2 and all(math.isfinite(x) for x in umbral)"),
    ("M12", "(r03 de T-125, adaptado) el C5 no pasa el run_id a fiabilidad_fuentes", EV,
     "fiabilidad = self.fiabilidad_fuentes(as_of, run_id)", "fiabilidad = self.fiabilidad_fuentes(as_of)"),
    ("M14", "(r03 de T-125, adaptado) el alta del ciclo usa la lista por defecto", ORQ,
     "self.referencias,\n                                                               variables_nivel(self.cfg))",
     "self.referencias,\n                                                               None)"),
    ("T13", "el alta del ciclo con la lista sin validar (equivalente si el Evaluador ya la validó)", ORQ,
     "self.referencias,\n                                                               variables_nivel(self.cfg))",
     "self.referencias,\n                                                               parametro(self.cfg, \"fiabilidad_fuentes.variables_nivel\"))"),
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
