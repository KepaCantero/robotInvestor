"""Mutantes de T-135 (T-128 H-05 y H-06; T-127 H-06 y H-07). Se aplican en una copia desechable del ejecutor
(DESTINO/11_Ejecutor, con el Catálogo al lado) y se ejecutan `tests/test_t135_motor.py` y las vecinas (-x). MUERTO = alguna
prueba falla. «REV» pone los módulos del Motor de la revisión `--base` (la de antes de T-135; `git show`) y ejecuta
`tests/test_t135_motor.py`: sus pruebas de los hallazgos tienen que fallar.
Uso: python impl_mutantes.py ORIGEN_EJECUTOR DESTINO [--base REV] [--solo ID,ID]
(DESTINO: carpeta desechable fuera del repo, cuya ruta contenga «t135_mut»; sin --solo se borra al acabar)"""
import shutil
import subprocess
import sys
from pathlib import Path

ORIGEN = Path(sys.argv[1]).resolve()
BASE = Path(sys.argv[2]).resolve()
assert "t135_mut" in str(BASE) and not (BASE / ".git").exists() and BASE != ORIGEN, "DESTINO debe ser una carpeta desechable"
COPIA = BASE / "11_Ejecutor"
SOLO = sys.argv[sys.argv.index("--solo") + 1].split(",") if "--solo" in sys.argv else None
REV = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else None
PY = sys.executable
NUEVAS = ["tests/test_t135_motor.py"]
PRUEBAS = [*NUEVAS, "tests/test_t128_r02.py", "tests/test_t127_r03.py", "tests/test_fase1_mon_idx.py"]
FB = "bloque_a/motor/frontera_b.py"
P2 = "bloque_a/motor/fichas_p2.py"
FR = "bloque_a/motor/fichas_reales.py"
MI = "bloque_a/motor/fichas_mon_idx.py"

if BASE.exists():
    shutil.rmtree(BASE)
BASE.mkdir(parents=True)
shutil.copytree(ORIGEN, COPIA, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
shutil.copytree(ORIGEN.parent / "04_Motor_conocimiento_y_catalogo", BASE / "04_Motor_conocimiento_y_catalogo")

CMP = "        cerca = np.abs(x[:, None] - x[None, :]) <= tol * np.maximum(a[:, None], a[None, :])\n        distinta |="
M = [
    # T-128 H-05 · IDX-CONC-001: copias por sus rentabilidades
    ("C01", MI, "        grupos = _etiquetas_series_copiadas(", "        grupos = np.arange(len(precios)) if True else _etiquetas_series_copiadas(",
     "sin agrupar copias"),
    ("C02", MI, "        elif dominio > k_max:", "        elif False:", "sin dominancia del grupo en la amplitud"),
    ("C03", MI, "            sin_porcentaje = 0 < distintos_v < IDX_CONC_COMPONENTES_MINIMOS or dominio_v > k_max",
     "            sin_porcentaje = 0 < distintos_v < IDX_CONC_COMPONENTES_MINIMOS", "sin dominancia entre los válidos"),
    ("C04", MI, "        distintos_v, dominio_v = _distintos_y_dominio(grupos[en_validos])",
     "        distintos_v, dominio_v = int(en_validos.sum()), _distintos_y_dominio(grupos[en_validos])[1]",
     "los válidos se cuentan por series"),
    ("C05", MI, "        if distintos < IDX_CONC_COMPONENTES_MINIMOS:   # T-128 r02",
     "        if len(precios) < IDX_CONC_COMPONENTES_MINIMOS:   # T-128 r02", "el mínimo cuenta series (el hallazgo)"),
    ("C06", MI, "        elif dominio > k_max:", "        elif dominio >= k_max:", "dominancia en el borde"),
    ("C07", MI, "    return len(tam), float(np.max(tam)) / len(grupos)", "    return len(tam), float(np.min(tam)) / len(grupos)",
     "el grupo menor"),
    ("E01", FB, "    copia = ~distinta & (ultima - primera >= anios_minimos)", "    copia = ~distinta",
     "sin el alcance mínimo de las fechas comunes"),
    ("E02", FB, "    copia = ~distinta & (ultima - primera >= anios_minimos)",
     "    copia = ~distinta & (ultima - primera > anios_minimos)", "alcance en el borde"),
    ("E03", FB, CMP, CMP.replace("<= tol *", "<= 0 *"), "copias solo exactas"),
    ("E04", FB, CMP, CMP.replace("np.maximum(a[:, None]", "np.minimum(a[:, None]").replace("a[None, :])\n", "a[None, :])\n"),
     "tolerancia por el menor"),
    ("E05", FB, "        rend[i, donde[1:]] = precios[i, donde[1:]] / precios[i, donde[:-1]] - 1",
     "        rend[i, donde[1:]] = precios[i, donde[1:]] - precios[i, donde[:-1]]", "diferencias de precio (dependen de la escala)"),
    ("E07", FB, "        distinta |= con_r[:, j][:, None] & con_r[:, j][None, :] & ~cerca",
     "        distinta |= ~cerca", "una rentabilidad ausente cuenta como distinta"),
    # T-128 H-06 · CHR-FLOW-001: dominancia por grupos
    ("F01", FR, '                 f"{F}: oferta_stablecoins", u["peso_maximo_componente"], grupos)',
     '                 f"{F}: oferta_stablecoins", u["peso_maximo_componente"])', "dominancia sin grupos (el mutante de la QA)"),
    # T-127 H-06 · aviso con coincidencias informativas
    ("V01", FB, '"coincidencias_informativas_minimas": 2}', '"coincidencias_informativas_minimas": 0}', "sin el mínimo informativo"),
    ("V02", FB, '"coincidencias_informativas_minimas": 2}', '"coincidencias_informativas_minimas": 1}', "mínimo informativo de 1"),
    ("V03", FB, '"coincidencias_informativas_minimas": 2}', '"coincidencias_informativas_minimas": 3}', "mínimo informativo de 3"),
    ("V04", FB, "        triviales += (nulo[:, None] & nulo[None, :]) | (cero[:, None] & cero[None, :])",
     "        triviales += nulo[:, None] & nulo[None, :]", "el cero no es trivial"),
    ("V05", FB, "        triviales += (nulo[:, None] & nulo[None, :]) | (cero[:, None] & cero[None, :])",
     "        triviales += cero[:, None] & cero[None, :]", "el None no es trivial"),
    ("V06", FB, "        triviales += (nulo[:, None] & nulo[None, :]) | (cero[:, None] & cero[None, :])",
     "        triviales += (nulo[:, None] | nulo[None, :]) | (cero[:, None] | cero[None, :])", "trivial si lo es en uno"),
    ("T01", P2, "        firmas_aviso.append((precio, circ, None if total == circ else total,",
     "        firmas_aviso.append((precio, circ, total,", "la total que repite la circulante cuenta"),
    ("T02", P2, "                             None if maxima is None or maxima == total else maxima, emision, quema,",
     "                             maxima, emision, quema,", "la máxima que repite la total cuenta"),
    ("T03", P2, "    _aviso_casi_clones(firmas_aviso, u[\"tolerancia_clon\"], lim)",
     "    _aviso_casi_clones(firmas, u[\"tolerancia_clon\"], lim)", "la firma del aviso de antes"),
    ("T04", P2, "                             None if tk.get(\"staking_nominal\") is None else float(tk[\"staking_nominal\"]),\n",
     "                             None,\n", "sin el staking en la firma"),
    # T-127 H-07 · REI-NAV-001: firma de los datos aportados
    ("N01", FR, '                         None if f["otros_derivados"] else f["otros"], f["gav"] if f["otros_derivados"] else None, f["cap"])',
     '                         f["otros"], None, f["cap"])', "la firma de antes (con el derivado)"),
    ("N02", FR, '                         None if f["otros_derivados"] else f["otros"], f["gav"] if f["otros_derivados"] else None, f["cap"])',
     '                         None if f["otros_derivados"] else f["otros"], None, f["cap"])', "sin el GAV aportado"),
    ("N03", FR, '"err": err, "otros_derivados": err is None})', '"err": err, "otros_derivados": False})',
     "nunca derivados"),
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
    fallan = [ln.split("::")[1][:90] for ln in r.stdout.splitlines() if ln.startswith(("FAILED", "ERROR")) and "::" in ln]
    print(f"REV · módulos de {REV} · {r.stdout.strip().splitlines()[-1][:160]}", flush=True)
    for f in fallan:
        print(f"    falla: {f}", flush=True)
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
