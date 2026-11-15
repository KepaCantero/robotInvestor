"""Mutantes de la ronda r03 de T-127 (H-04 aviso, H-05 aportación con signo) y de la r02 de T-128 (H-02: CHR-FLOW-001 e
IDX-CONC-001; aviso en REI-NAV-001). Se aplican en una copia desechable del ejecutor (DESTINO/11_Ejecutor, con el Catálogo
al lado) y se ejecutan `tests/test_t127_r03.py`, `tests/test_t128_r02.py`, `tests/test_t127_r02.py`,
`tests/test_t128_frontera.py` y `tests/test_fase1_mon_idx.py` (-x). MUERTO = alguna prueba falla. «REV» pone los cuatro
módulos de la revisión `--base` (la de antes de la ronda; `git show`) y ejecuta las dos pruebas nuevas: tienen que fallar.
Uso: python impl_r03_mutantes.py ORIGEN_EJECUTOR DESTINO [--base REV] [--solo ID,ID]
(DESTINO: carpeta desechable fuera del repo, cuya ruta contenga «t127r03_mut»; sin --solo se borra al acabar)"""
import shutil
import subprocess
import sys
from pathlib import Path

ORIGEN = Path(sys.argv[1]).resolve()
BASE = Path(sys.argv[2]).resolve()
assert "t127r03_mut" in str(BASE) and not (BASE / ".git").exists() and BASE != ORIGEN, "DESTINO debe ser una carpeta desechable"
COPIA = BASE / "11_Ejecutor"
SOLO = sys.argv[sys.argv.index("--solo") + 1].split(",") if "--solo" in sys.argv else None
REV = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else None
PY = sys.executable
NUEVAS = ["tests/test_t127_r03.py", "tests/test_t128_r02.py"]
PRUEBAS = [*NUEVAS, "tests/test_t127_r02.py", "tests/test_t128_frontera.py", "tests/test_fase1_mon_idx.py"]
FB = "bloque_a/motor/frontera_b.py"
P2 = "bloque_a/motor/fichas_p2.py"
FR = "bloque_a/motor/fichas_reales.py"
MI = "bloque_a/motor/fichas_mon_idx.py"

if BASE.exists():
    shutil.rmtree(BASE)
BASE.mkdir(parents=True)
shutil.copytree(ORIGEN, COPIA, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
shutil.copytree(ORIGEN.parent / "04_Motor_conocimiento_y_catalogo", BASE / "04_Motor_conocimiento_y_catalogo")

AV = "    _aviso_casi_clones(firmas, u[\"tolerancia_clon\"], lim)   # T-127 r03 (H-04): un dato movido, aviso en RC\n"
M = [
    # T-127 H-04 · aviso
    ("V01", FB, 'AVISO_B: dict[str, Any] = {"datos_distintos_aviso": 1}', 'AVISO_B: dict[str, Any] = {"datos_distintos_aviso": 0}',
     "aviso solo con clones exactos"),
    ("V02", FB, 'AVISO_B: dict[str, Any] = {"datos_distintos_aviso": 1}', 'AVISO_B: dict[str, Any] = {"datos_distintos_aviso": 2}',
     "aviso con dos datos movidos"),
    ("V03", FB, "    par = _datos_que_coinciden(firmas, tol) >= len(firmas[0]) - d",
     "    par = _datos_que_coinciden(firmas, tol) > len(firmas[0]) - d", "aviso en el borde (uno menos)"),
    ("V04", FB, "    np.fill_diagonal(par, False)\n    k =", "    k =", "cada componente se cuenta a sí mismo"),
    ("V05", FB, "    if k:\n        lim.append(f\"aviso", "    if False:\n        lim.append(f\"aviso", "sin el aviso"),
    ("V06", P2, "    _aviso_casi_clones(firmas, u[\"tolerancia_clon\"], lim)   # T-127 r03 (H-04): un dato movido (σ_E·(1 ± δ)), aviso en RC\n",
     "", "FIR-CRED sin aviso"),
    ("V07", P2, '    _sin_clones(firmas, f"{F}: componentes", u["tolerancia_clon"])\n' + AV,
     '    _sin_clones(firmas, f"{F}: componentes", u["tolerancia_clon"])\n', "REI-LEV sin aviso"),
    ("V08", P2, '    _sin_clones(firmas, f"{F}: tokens", u["tolerancia_clon"])\n' + AV,
     '    _sin_clones(firmas, f"{F}: tokens", u["tolerancia_clon"])\n', "CHR-TOKEN sin aviso"),
    ("V09", FR, '    _aviso_casi_clones([(f["precio"], f["acciones"], f["nav_acc"], f["deuda"], f["otros"], f["cap"]) for f in filas],',
     '    _aviso_casi_clones([(f["precio"], f["acciones"], f["nav_acc"], f["deuda"], f["gav"], f["cap"]) for f in filas],',
     "REI-NAV con el GAV en la firma (lo fija la identidad)"),
    ("V10", FR, '    _aviso_casi_clones([(f["precio"], f["acciones"], f["nav_acc"], f["deuda"], f["otros"], f["cap"]) for f in filas],\n'
                '                       u["tolerancia_clon"], lim)\n', "", "REI-NAV sin aviso"),
    ("V11", FB, "        iguales += cerca & (nulo[:, None] == nulo[None, :])", "        iguales += cerca",
     "un dato ausente igual a un cero"),
    ("V12", FB, "    cerca = _datos_que_coinciden(firmas, tol) == len(firmas[0])",
     "    cerca = _datos_que_coinciden(firmas, tol) >= len(firmas[0]) - 1", "casi clones con un dato distinto (refactor)"),
    # mutantes de la r02 cuyo texto cambió con `_datos_que_coinciden` y la medida con signo (E12 es V11)
    ("K02t", FB, "        cerca = np.abs(x[:, None] - x[None, :]) <= tol * np.maximum(a[:, None], a[None, :])",
     "        cerca = np.abs(x[:, None] - x[None, :]) < tol * np.maximum(a[:, None], a[None, :])", "tolerancia estricta (r02 K02r)"),
    ("K03t", FB, "        cerca = np.abs(x[:, None] - x[None, :]) <= tol * np.maximum(a[:, None], a[None, :])",
     "        cerca = np.abs(x[:, None] - x[None, :]) <= tol * np.minimum(a[:, None], a[None, :])",
     "tolerancia por el menor (r02 K03r)"),
    ("A01t", FB, "    np.fill_diagonal(cerca, True)\n    grupo =", "    cerca = np.eye(len(a), dtype=bool)\n    grupo =",
     "aportación sin vecindario de la misma cifra (r02 A01)"),
    # T-127 H-05 · aportación con signo
    ("S01", FB, "    return max(sin_signo, con_signo)", "    return sin_signo", "sin la medida con signo"),
    ("S02", FB, "    con_signo = 1.0 - float(np.min(np.abs(suma - grupo @ n_))) / abs(suma)",
     "    con_signo = 1.0 - float(np.min(np.abs(suma - grupo @ a))) / abs(suma)", "el resto en valor absoluto"),
    ("S03", FB, "    con_signo = 1.0 - float(np.min(np.abs(suma - grupo @ n_))) / abs(suma)",
     "    con_signo = 1.0 - float(np.max(np.abs(suma - grupo @ n_))) / abs(suma)", "el grupo que menos aporta"),
    ("S04", FB, "    con_signo = 1.0 - float(np.min(np.abs(suma - grupo @ n_))) / abs(suma)",
     "    con_signo = 1.0 - float(np.min(np.abs(suma - n_))) / abs(suma)", "con signo sin el vecindario de la misma cifra"),
    # T-128 H-02 · CHR-FLOW-001
    ("F01", FR, '                     "monedas_estables_minimas": 2, **FRONTERA_B},',
     '                     "monedas_estables_minimas": 1, **FRONTERA_B},', "una moneda basta"),
    ("F02", FR, '    _sin_dominio({"oferta de stablecoins": o_T, "oferta de stablecoins de la base del crecimiento": o_b},\n'
                '                 f"{F}: oferta_stablecoins", u["peso_maximo_componente"], grupos)\n', "", "sin dominancia de la oferta"),
    ("F03", FR, "    grupos = _etiquetas_casi_iguales([(float(x),) for x in o_T / o_b - 1], u[\"tolerancia_clon\"])",
     "    grupos = np.arange(len(por_moneda))", "copias a escala de una moneda cuentan como dos"),
    ("F04", FR, "    if conc:\n        crecimiento = None\n", "", "el crecimiento concentrado se entrega"),
    ("F05", FR, "    o_b = np.array([float(s.loc[previos.index[-1]]) for s in por_moneda])",
     "    o_b = np.array([float(s.iloc[0]) for s in por_moneda])", "base del crecimiento en otra fecha"),
    # T-128 H-02 · IDX-CONC-001
    ("C01", MI, "IDX_CONC_COMPONENTES_MINIMOS = 2", "IDX_CONC_COMPONENTES_MINIMOS = 1", "un componente basta"),
    ("C02", MI, "        if len(precios) < IDX_CONC_COMPONENTES_MINIMOS:", "        if False:", "amplitud de un componente"),
    ("C03", MI, '            amplitud = {"porcentaje_sobre_media": sobre / validos if validos >= IDX_CONC_COMPONENTES_MINIMOS else None,',
     '            amplitud = {"porcentaje_sobre_media": sobre / validos if validos else None,', "porcentaje de un solo válido"),
    ("C04", MI, "            if len(w0) < IDX_CONC_COMPONENTES_MINIMOS or sin_contrib:", "            if sin_contrib:",
     "contribución de un componente con rentabilidad nula"),
    ("C05", MI, "            if len(w0) < IDX_CONC_COMPONENTES_MINIMOS or sin_contrib:",
     "            if len(w0) < IDX_CONC_COMPONENTES_MINIMOS:", "contribución dominada"),
]


def pytest(pruebas: list[str], x: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run([PY, "-m", "pytest", "-q", *(["-x"] if x else []), "-p", "no:cacheprovider", *pruebas], cwd=COPIA,
                          capture_output=True, text=True, timeout=1800, check=False)


vivos = []
if REV is not None and (not SOLO or "REV" in SOLO):
    raiz = ORIGEN.parent.parent
    guardados = {}
    for mod in (FB, P2, FR, MI):
        ruta = COPIA / mod
        guardados[ruta] = ruta.read_text(encoding="utf-8")
        antes = subprocess.run(["git", "-C", str(raiz), "show", f"{REV}:bloque_a/11_Ejecutor/{mod}"], capture_output=True,
                               text=True, check=True).stdout
        ruta.write_text(antes, encoding="utf-8")
    try:
        r = pytest(NUEVAS, x=False)
    finally:
        for ruta, txt in guardados.items():
            ruta.write_text(txt, encoding="utf-8")
    print(f"REV · módulos de {REV} · {r.stdout.strip().splitlines()[-1][:160]}", flush=True)
for mid, mod, a, b, desc in M:
    if SOLO and mid not in SOLO:
        continue
    ruta = COPIA / mod
    orig = ruta.read_text(encoding="utf-8")
    if orig.count(a) != 1:
        print(f"{mid}: el texto aparece {orig.count(a)} veces; no se aplica · {desc}", flush=True)
        vivos.append(f"{mid}?")
        continue
    ruta.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        r = pytest(PRUEBAS)
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
