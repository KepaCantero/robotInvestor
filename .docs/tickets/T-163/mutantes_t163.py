"""T-163 · regresión: cada comprobación nueva quitada (un mutante) hace fallar alguna prueba de `tests/test_t163_hallazgos_t160.py`.

Uso, desde la raíz:  .venv/bin/python .docs/tickets/T-163/mutantes_t163.py <copia «…_mut» con bloque_a/ entero> [--solo T01,T02]
Cada mutante se aplica en la copia, se pasan las pruebas de `PRUEBAS` (con -x) y se restaura. Vivo = ninguna prueba lo detecta.
Los equivalentes se marcan en EQUIVALENTES. Termina con 1 si alguno no aplica o si vive uno que no es equivalente.
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "_mut" in COPIA.name and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir(), "hace falta una copia desechable «…_mut»"
SOLO = set(sys.argv[sys.argv.index("--solo") + 1].split(",")) if "--solo" in sys.argv else None
PY = str(Path(__file__).resolve().parents[3] / ".venv" / "bin" / "python")
EV, SV = "bloque_a/11_Ejecutor/bloque_a/evaluador.py", "bloque_a/11_Ejecutor/bloque_a/motor/servicio.py"
PRUEBAS = ["tests/test_t163_hallazgos_t160.py"]
MUTANTES = [
    ("T01", "H-01: sin comprobar el método del soporte", EV,
     'if "metodo" not in prm or prm["metodo"] != celda.get("metodo"):', "if False:"),
    ("T02", "H-01: sin comprobar las entradas", EV,
     '        if (not huellas_s or huellas_s != [c.get("huella_entradas")] or huellas_r != huellas_s\n'
     '                or r.get("operacion") != s.get("operacion")):', "        if False:"),
    ("T03", "H-01: sin comprobar que la CT-10 es posterior al soporte", EV, " or sq_r <= sq_s:", ":"),
    ("T04", "H-05: una CT-10 posterior con NO no importa", EV,
     '        if despues:\n            return f"una re-ejecución', '        if False:\n            return f"una re-ejecución'),
    ("T05", "H-01: una re-ejecución puede sostener varios certificados", EV,
     'if quien is not None and quien != c.get("id"):', "if False:"),
    ("T06", "H-01: sin comparar las cifras del CERT- con las del soporte", EV, "        if distintas:\n", "        if False:\n"),
    ("T07", "H-02: certificados_vigentes no mira la re-ejecución", EV,
     "return [c for c in vig if self.motivo_sin_reejecucion(c, ctx) is None]", "return vig"),
    ("T08", "H-02: la revisión no revoca los VIGENTE sin re-ejecución", EV, "            if motivo_v is None:\n",
     "            if True:\n"),
    ("T09", "H-02: CT-04 solo mira los VIGENTE que se usan", EV,
     'for c in self._vigentes_en_f6(as_of) if c.get("celda")}', 'for c in self.certificados_vigentes(as_of) if c.get("celda")}'),
    ("T10", "H-03: la emisión no pasa el borrador por la comprobación de CT-04", EV, "                        if sin_borrador:\n",
     "                        if False:\n"),
    ("T11", "H-01: la petición no lleva el método", EV, '"tasa_base": tasa_base, "metodo": k[2]}', '"tasa_base": tasa_base}'),
    ("T12", "H-01: el CERT- no cita la huella de sus entradas", EV, '"huella_entradas": ver["huella_entradas"],', ""),
    ("T13", "H-04: FC-EVAL-001 no valida min_conglomerados", SV,
     'if fechas is not None and "min_conglomerados" in params and not min_conglomerados_valido(params["min_conglomerados"]):',
     "if False:"),
    ("T14", "H-04: un booleano vale como mínimo", SV, " and not isinstance(x, (bool, np.bool_))", ""),
    ("T15", "H-04: el suelo baja a 1", SV, "MIN_CONGLOMERADOS = 2\n", "MIN_CONGLOMERADOS = 1\n"),
]
EQUIVALENTES = {
    "T14": "con el suelo en 2, True (1) y False (0) ya quedan por debajo: la exclusión de booleanos solo importa si el suelo baja a 1",
}


def pytest(args, cwd):
    r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *args], cwd=cwd, capture_output=True, text=True,
                       timeout=3600)
    return r.returncode == 0, (r.stdout.strip().splitlines() or [""])[-1]


ejec = COPIA / "bloque_a" / "11_Ejecutor"
ok, ultima = pytest(PRUEBAS, ejec)
assert ok, f"las pruebas no pasan sin mutar: {ultima}"
vivos, no_aplica = [], []
for mid, desc, ruta, viejo, nuevo in MUTANTES:
    if SOLO and mid not in SOLO:
        continue
    f = COPIA / ruta
    texto = f.read_text(encoding="utf-8")
    if texto.count(viejo) != 1:
        no_aplica.append(mid)
        print(f"{mid} NO APLICA ({texto.count(viejo)} apariciones): {desc}", flush=True)
        continue
    f.write_text(texto.replace(viejo, nuevo), encoding="utf-8")
    try:
        pasa, ultima = pytest(PRUEBAS, ejec)
        if pasa:
            vivos.append(mid)
        eq = f" [equivalente: {EQUIVALENTES[mid]}]" if mid in EQUIVALENTES else ""
        print(f"{mid} {'vivo' if pasa else 'muerto'}{eq}: {desc} · {ultima}", flush=True)
    finally:
        f.write_text(texto, encoding="utf-8")
print(f"\n{len(MUTANTES)} mutantes · vivos {vivos} · no aplican {no_aplica}")
sys.exit(1 if [m for m in vivos if m not in EQUIVALENTES] or no_aplica else 0)
