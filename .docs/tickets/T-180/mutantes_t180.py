"""T-180 · regresión: cada comprobación nueva quitada (un mutante) hace fallar alguna prueba de `tests/test_t180_hallazgos_t163.py`.

Uso, desde la raíz:  .venv/bin/python .docs/tickets/T-180/mutantes_t180.py <copia «…_mut» con bloque_a/ entero> [--solo U01,U02]
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
EV, CF = "bloque_a/11_Ejecutor/bloque_a/evaluador.py", "bloque_a/11_Ejecutor/tests/conftest.py"
PRUEBAS = ["tests/test_t180_hallazgos_t163.py"]
MUTANTES = [
    ("U01", "H-01: sin comprobar el solicitante del soporte", EV, '        if s.get("solicitante") != "AG-20":\n',
     "        if False:\n"),
    ("U02", "H-01: sin aplicar el criterio al soporte", EV,
     '        if not crit["certificable"]:\n            return (f"{soporte} no cumple', '        if False:\n            return (f"{soporte} no cumple'),
    ("U03", "H-01: sin la materialidad de una CT-10 DENTRO_TOLERANCIA", EV,
     'pasos_ct10 = 0 if rx.get("coincide") == "SI" else 1', "pasos_ct10 = 0"),
    ("U04", "H-01: CT-04 no mira la p de DM-HLN", EV,
     "holgura_tolerancia(tol_ct04, pasos_ct10), n_cert, ece_max, alfa_holm)", "holgura_tolerancia(tol_ct04, pasos_ct10), n_cert, ece_max, None)"),
    ("U05", "H-01: con una sola celda candidata no se aplica Holm (lo de antes)", EV,
     "                alfa_k = umbrales[etiqueta_celda(k)]\n", "                alfa_k = umbrales[etiqueta_celda(k)] if len(metr) > 1 else None\n"),
    ("U06", "H-01: los umbrales del criterio escritos a mano (los de la entrega)", EV,
     ('return (int(parametro(self.cfg, "evaluacion.min_certificar")), float(parametro(self.cfg, "evaluacion.ece_max")),\n'
      '                float(parametro(self.cfg, "evaluacion.alfa_holm")))'), "return (100, 0.15, 0.10)"),
    ("U07", "H-01: unas cifras del soporte con otra forma lanzan en lugar de no valer", EV,
     "        except (TypeError, ValueError, AttributeError) as e:   # cifras con otra forma",
     "        except ZeroDivisionError as e:   # cifras con otra forma"),
    ("U08", "H-02: la petición no lleva el horizonte", EV, '"horizonte": k[1], "tasa_base": tasa_base', '"tasa_base": tasa_base'),
    ("U09", "ayudante de pruebas: vuelve a los 60 pronósticos de T-163 (n_eff < 100)", CF, "    n = 160\n", "    n = 60\n"),
]
EQUIVALENTES: dict[str, str] = {}


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
