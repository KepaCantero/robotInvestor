"""Mutantes de las correcciones de la ronda r02 de T-119 (H-01, H-03, H-05, H-06, H-08 y H-09).
Se aplican en una copia desechable del ejecutor
(DESTINO/11_Ejecutor, con el Catálogo al lado) y se ejecutan `tests/test_t119_r02.py`,
`test_t119_p2.py` y `test_t119_motor.py` (-x). MUERTO = alguna prueba falla.
Uso: python impl_r02_mutantes.py ORIGEN_EJECUTOR DESTINO [--solo ID,ID]   (DESTINO: carpeta desechable fuera del repo; sin
--solo se borra al acabar)"""
import shutil
import subprocess
import sys
from pathlib import Path

ORIGEN = Path(sys.argv[1]).resolve()
BASE = Path(sys.argv[2]).resolve()
assert not (BASE / ".git").exists() and BASE != ORIGEN, "DESTINO debe ser una carpeta desechable"
COPIA = BASE / "11_Ejecutor"
SOLO = sys.argv[sys.argv.index("--solo") + 1].split(",") if "--solo" in sys.argv else None
PY = "/home/user/robotinvestor/.venv/bin/python"
PRUEBAS = ["tests/test_t119_r02.py", "tests/test_t119_p2.py", "tests/test_t119_motor.py"]
MO, TC, FD, SV, SE = (f"bloque_a/motor/{n}.py" for n in ("fichas_mon_idx", "fichas_tcv", "fichas_fon_der", "servicio",
                                                          "fichas_series"))

if BASE.exists():
    shutil.rmtree(BASE)
BASE.mkdir(parents=True)
shutil.copytree(ORIGEN, COPIA, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
shutil.copytree(ORIGEN.parent / "04_Motor_conocimiento_y_catalogo", BASE / "04_Motor_conocimiento_y_catalogo")

P2, RE = "bloque_a/motor/fichas_p2.py", "bloque_a/motor/fichas_reales.py"
M = [
    ("R01", P2, '    _sin_clones(firmas, f"{F}: componentes")   # el mínimo de 10 es de componentes distintos', "    pass", "FIR-CRED: clones admitidos"),
    ("R02", P2, '    _sin_clones(firmas, f"{F}: componentes")\n    a = {k:', "    pass\n    a = {k:", "REI-LEV: clones admitidos"),
    ("R03", P2, '    _sin_clones(firmas, f"{F}: tokens")', "    pass", "CHR-TOKEN: clones admitidos"),
    ("R04", P2, "    if isinstance(comps, list) and 0 < len(comps) < u[\"componentes_minimos\"]:", "    if False:", "REI-LEV: sin mínimo de componentes"),
    ("R05", P2, "    if isinstance(comps, list) and 0 < len(comps) < u[\"componentes_minimos\"]:", "    if isinstance(comps, list) and 0 < len(comps) < 2:", "REI-LEV: mínimo 2 en vez de 3"),
    ("R06", P2, "        if es_red is not True:", "        if False:", "CHR-TOKEN: un token con ámbito de sector"),
    ("R07", P2, "        firmas.append((E, sE, corto, largo))", "        firmas.append((E, sE, corto, largo, c.get(\"id\")))", "FIR-CRED: el clon se distingue por el id"),
    ("R08", RE, "    if len(comps) < u[\"componentes_minimos\"]:   # r02", "    if False:   # r02", "REI-NAV: un solo componente"),
    ("R09", P2, "        if soluciones:", "        if False:", "TIR: con dos soluciones dice «sin TIR»"),
    ("R10", P2, '                     ("el intervalo de la tendencia no lleva', '                     ("el intervalo de la tendencia lleva', "CMD-REAL: advertencia del IC cambiada"),
    ("R11", P2, '                    "LN-PME (Long-Nickels), que la ficha da por opcional, no se calcula"],', "                    ],", "PRV-PME: sin declarar LN-PME"),
    ("R12", SV, "        if previo and (marca is None or firma is None or marca[0] != firma\n", "        if previo and (marca is None or firma is None\n", "caché: no distingue tipos"),
    ("R13", SV, "                       or clave_hash(_configuracion_usada(self.cfg, marca[1])) != marca[2]):", "                       ):", "caché: no distingue la configuración"),
]
vivos = []
for mid, mod, a, b, desc in M:
    if SOLO and mid not in SOLO:
        continue
    ruta = COPIA / mod
    orig = ruta.read_text(encoding="utf-8")
    if isinstance(a, int):
        lineas = orig.split("\n")
        lineas[a - 1] = b
        nuevo = "\n".join(lineas)
    else:
        if orig.count(a) != 1:
            print(f"{mid}: el texto aparece {orig.count(a)} veces; no se aplica · {desc}", flush=True)
            continue
        nuevo = orig.replace(a, b)
    ruta.write_text(nuevo, encoding="utf-8")
    try:
        r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], cwd=COPIA,
                           capture_output=True, text=True, timeout=1800, check=False)
        muerto = r.returncode != 0
        fallo = next((ln for ln in r.stdout.splitlines() if ln.startswith(("FAILED", "ERROR"))), "")
    finally:
        ruta.write_text(orig, encoding="utf-8")
    print(f"{mid} {'muere' if muerto else 'VIVE '} · {desc} · {fallo[:140]}", flush=True)
    if not muerto:
        vivos.append(mid)
print(f"\n{len([m for m in M if not SOLO or m[0] in SOLO])} mutantes; vivos: {', '.join(vivos) or 'ninguno'}")
if not SOLO:
    shutil.rmtree(BASE)
