"""QA r02 de T-148 · mutantes propios del revisor sobre la r02 del estimador (distintos de M25–M37 de `T-147/mutantes.py`).

Uso: python r02_02_mutantes_qa.py <copia desechable con «qa21_» y «_mut» en la ruta, con `bloque_a/` y `.docs/scripts/`>
Cada mutante se aplica, se pasan `tests/test_t148.py` y `tests/test_t145.py` (con -x) y se restaura. Vivo = ninguna prueba lo
detecta. Termina con 1 si alguno no aplica."""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "qa21_" in str(COPIA) and "_mut" in str(COPIA) and (COPIA / ".docs" / "scripts" / "estimar_coste_ciclo_a.py").is_file()
EST = ".docs/scripts/estimar_coste_ciclo_a.py"
PRUEBAS = ["tests/test_t148.py", "tests/test_t145.py"]
MUT = [
    ("W01", "manda al revés", "    manda_presupuesto = cota_presupuesto < cota_llamadas", "    manda_presupuesto = cota_presupuesto > cota_llamadas"),
    ("W02", "las lecturas de los papeles de una bolsa se suman (no la mayor)",
     "            por_bolsa[x[\"bolsa\"]] = max(por_bolsa[x[\"bolsa\"]], una)", "            por_bolsa[x[\"bolsa\"]] += una"),
    ("W03", "el peso por bolsa al precio de entrada (no al de escritura de caché)",
     "            una = (max_usos * vueltas * precio(x[\"agente\"])[\"escritura_cache\"]",
     "            una = (max_usos * vueltas * precio(x[\"agente\"])[\"entrada\"]"),
    ("W04", "la salida no dice lo que reserva T-146 por búsqueda", "tokens_lectura_por_busqueda`), que el peso no descuenta\" if reservado else",
     "tokens_lectura_por_busqueda`), que el peso no descuenta\" if False else"),
    ("W05", "con --sin-t146 el peso por bolsa es el de T-146 (una petición)",
     "            una = (max_usos * vueltas * precio(x[\"agente\"])[\"escritura_cache\"] * 1000 / 1e6 if con_t146",
     "            una = (max_usos * vueltas * precio(x[\"agente\"])[\"escritura_cache\"] * 1000 / 1e6 if True"),
]

vivos, no_aplica = [], []
for mid, desc, viejo, nuevo in MUT:
    f = COPIA / EST
    orig = f.read_text(encoding="utf-8")
    if orig.count(viejo) != 1:
        print(f"{mid} NO APLICA ({orig.count(viejo)} apariciones) · {desc}", flush=True)
        no_aplica.append(mid)
        continue
    f.write_text(orig.replace(viejo, nuevo), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS],
                           cwd=COPIA / "bloque_a" / "11_Ejecutor", capture_output=True, text=True, timeout=1800)
        muerto = r.returncode != 0
    finally:
        f.write_text(orig, encoding="utf-8")
    print(f"{mid} {'muerto' if muerto else 'VIVO  '} · {desc}", flush=True)
    if not muerto:
        vivos.append(mid)
print(f"{len(MUT) - len(vivos) - len(no_aplica)}/{len(MUT)} muertos; vivos: {', '.join(vivos) or 'ninguno'}; "
      f"no aplican: {', '.join(no_aplica) or 'ninguno'}")
sys.exit(1 if no_aplica else 0)
