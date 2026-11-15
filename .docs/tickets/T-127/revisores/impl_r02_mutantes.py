"""Mutantes de las correcciones de la ronda r02 de T-127 (H-01 copias a escala, H-02 aportación) y de las reglas de la r01
cuyo texto cambió en la r02. Se aplican en una copia desechable del ejecutor (DESTINO/11_Ejecutor, con el Catálogo al
lado) y se ejecutan `tests/test_t127_r02.py`, `tests/test_t127_hallazgos.py` y `tests/test_t119_r02.py` (-x). MUERTO =
alguna prueba falla. «REV» es el `fichas_p2.py` de antes de la r02 (`git show fb3ccd4:…`, se pasa con --antes): las
pruebas nuevas tienen que fallar con él (desde T-128 las funciones comunes están en `frontera_b.py`; el `fichas_p2.py` de
antes no lo importa y funciona solo).
Uso: python impl_r02_mutantes.py ORIGEN_EJECUTOR DESTINO [--antes FICHERO] [--solo ID,ID]
(DESTINO: carpeta desechable fuera del repo, cuya ruta contenga «t127r02_mut»; sin --solo se borra al acabar)"""
import shutil
import subprocess
import sys
from pathlib import Path

ORIGEN = Path(sys.argv[1]).resolve()
BASE = Path(sys.argv[2]).resolve()
assert "t127r02_mut" in str(BASE) and not (BASE / ".git").exists() and BASE != ORIGEN, "DESTINO debe ser una carpeta desechable"
COPIA = BASE / "11_Ejecutor"
SOLO = sys.argv[sys.argv.index("--solo") + 1].split(",") if "--solo" in sys.argv else None
ANTES = Path(sys.argv[sys.argv.index("--antes") + 1]).resolve() if "--antes" in sys.argv else None
PY = sys.executable
PRUEBAS = ["tests/test_t127_r02.py", "tests/test_t127_hallazgos.py", "tests/test_t119_r02.py"]
P2 = "bloque_a/motor/fichas_p2.py"
FB = "bloque_a/motor/frontera_b.py"   # T-128: las funciones comunes de la frontera salieron de fichas_p2 a este módulo

if BASE.exists():
    shutil.rmtree(BASE)
BASE.mkdir(parents=True)
shutil.copytree(ORIGEN, COPIA, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
shutil.copytree(ORIGEN.parent / "04_Motor_conocimiento_y_catalogo", BASE / "04_Motor_conocimiento_y_catalogo")

M = [
    # H-01 · copias a escala
    ("E01", FB, "    if distintos < minimo:", "    if distintos < 1:", "sin mínimo de componentes distintos por sus cifras"),
    ("E02", P2, '    grupos = _sin_copias_a_escala([tuple(f.values()) for f in filas], f"{F}: componentes", u["componentes_minimos"],',
     '    grupos = _sin_copias_a_escala([tuple(f.values()) for f in filas], f"{F}: componentes", 1,', "FIR-CRED sin el mínimo"),
    ("E03", P2, '                                  f"{F}: componentes", u["componentes_minimos"], u["tolerancia_clon"])',
     '                                  f"{F}: componentes", 1, u["tolerancia_clon"])', "REI-LEV sin el mínimo"),
    ("E04", P2, '            f"{F}: tokens", u["tokens_minimos_sector"], u["tolerancia_clon"])',
     '            f"{F}: tokens", 1, u["tolerancia_clon"])', "CHR-TOKEN sin el mínimo"),
    ("E05", P2, '    sin_escala = np.column_stack([a["neta"] / a["gav"], a["ebitda"] / a["gf"], a["neta"] / a["ebitda"],',
     '    sin_escala = np.column_stack([a["gav"], a["ebitda"] / a["gf"], a["neta"] / a["ebitda"],', "REI-LEV con el GAV (escala)"),
    ("E06", FB, "    if grupos is None or not len(a):", "    if True:", "dominancia sin grupos"),
    ("E07", P2, '    _sin_dominio({"deuda": deudas}, f"{F}: componentes", u["peso_maximo_componente"], grupos)   # T-127 (H-10)',
     '    _sin_dominio({"deuda": deudas}, f"{F}: componentes", u["peso_maximo_componente"])', "FIR-CRED: dominancia sin grupos"),
    ("E08", P2, '                  "ffo": col["ffo"]}, f"{F}: componentes", u["peso_maximo_componente"], grupos)',
     '                  "ffo": col["ffo"]}, f"{F}: componentes", u["peso_maximo_componente"])', "REI-LEV: dominancia sin grupos"),
    ("E09", FB, '    if (len(x) if distintos is None else distintos) >= u["componentes_minimos_orden"]:',
     '    if len(x) >= u["componentes_minimos_orden"]:', "orden por número de componentes, no distintos"),
    ("E10", P2, "    if 0 < cov_distintos < u[\"componentes_minimos\"]:", "    if 0 < len(holg_ltv) < u[\"componentes_minimos\"]:",
     "covenants por número, no distintos"),
    ("E11", P2, '        if not red and (len(set(g.tolist())) < u["tokens_minimos_sector"]',
     '        if not red and (len(pares) < u["tokens_minimos_sector"]', "staking por número, no distintos"),
    ("E12", FB, "        cerca &= nulo[:, None] == nulo[None, :]\n", "", "un dato ausente igual a un cero (r01 K04)"),
    # H-02 · aportación
    ("A01", FB, "    np.fill_diagonal(cerca, True)\n    return", "    cerca = np.eye(len(a), dtype=bool)\n    return",
     "aportación sin vecindario de la misma cifra"),
    ("A02", FB, '            if _aportacion_maxima(n_, d_, u["tolerancia_clon"], cero) > u["peso_maximo_componente"]]',
     '            if _aportacion_maxima(n_, d_, u["tolerancia_clon"], cero) >= u["peso_maximo_componente"]]', "aportación en el borde"),
    ("A03", FB, "    if not total > 0 or (suma_den != 0 and abs(float(np.sum(n_)) / suma_den) <= cero):",
     "    if not total > 0:", "sin el cero de la tolerancia de la ficha"),
    ("A04", P2, '    _rechazo_concentradas(_concentradas({n: (d_ * col[k], d_) for n, k in medias.items()}, u, tol), f"{F}: componentes", u)',
     "    pass", "FIR-CRED sin la aportación"),
    ("A05", P2, '    medias = {"la DD media": "dd", "la PD media": "pd", "el diferencial implícito": "dif",',
     '    medias = {"la DD media": "dd", "el diferencial implícito": "dif",', "FIR-CRED sin la PD"),
    ("A06", P2, '        medias |= {"la DD real media": "dd_real", "la PD real media": "pd_real"}', "        pass", "FIR-CRED sin la real"),
    ("A07", P2, '    _rechazo_concentradas(_concentradas({"el LTV": (a["neta"], a["gav"]), "el ICR": (a["ebitda"], a["gf"]),',
     '    _rechazo_concentradas(_concentradas({"el ICR": (a["ebitda"], a["gf"]),', "REI-LEV sin el LTV"),
    ("A08", P2, '    _limitacion_concentradas(sin_venc, u, lim)\n', "    sin_venc = []\n", "REI-LEV sin la aportación a los vencimientos"),
    ("A09", P2, "    if not red:\n        sin_cifra = _concentradas(", "    if False:\n        sin_cifra = _concentradas(",
     "CHR-TOKEN sin la aportación"),
    ("A10", P2, "        if not red and _concentradas({que: (c_ * x_, c_)}, u, tol):", "        if False:",
     "staking y concentración sin la aportación"),
    ("A11", FB, "    a = np.abs(n_)\n", "    a = n_\n", "aportación sin valor absoluto"),
    ("A12", FB, "    cerca &= definida[:, None] & definida[None, :]\n", "", "cifras sin definir (÷ 0) como un vecindario"),
    # reglas de la r01 cuyo texto cambió (el mutante de la r01 ya no se aplica tal cual)
    ("D05r", P2, '    _sin_dominio({"deuda": deudas}, f"{F}: componentes", u["peso_maximo_componente"], grupos)   # T-127 (H-10)',
     "    pass", "FIR-CRED sin dominancia (r01 D05)"),
    ("D07r", P2, '        _sin_dominio({"capitalizacion_circulante": cm, "fdv": fdv}, f"{F}: tokens", u["peso_maximo_componente"], grupos)',
     "        pass", "CHR-TOKEN sin dominancia (r01 D07)"),
    ("D08r", FB, "    a = np.abs(np.asarray(x, dtype=float))\n    if grupos", "    a = np.asarray(x, dtype=float)\n    if grupos",
     "dominancia sin valor absoluto (r01 D08)"),
    ("O02r", FB, '    if (len(x) if distintos is None else distintos) >= u["componentes_minimos_orden"]:',
     '    if (len(x) if distintos is None else distintos) > u["componentes_minimos_orden"]:', "orden desde 8 (r01 O02)"),
    ("O03r", P2, '    if _orden(a["gav"], u, sin_orden, "la dispersión de los componentes",\n              len(set(grupos.tolist()))) is not None:',
     "    if True:", "REI-LEV con dispersión siempre (r01 O03)"),
    ("O04r", P2, '    if not red and _orden(a_cm, u, sin_orden, "la dispersión de los tokens",\n                          len(set(grupos.tolist()))) is not None:',
     "    if not red:", "CHR-TOKEN con dispersión siempre (r01 O04)"),
    ("O05r", P2, '            "holgura_ltv_pp": _orden(np.array(holg_ltv), u, sin_orden, "las holguras frente a covenants", cov_distintos),',
     '            "holgura_ltv_pp": _distribucion(np.array(holg_ltv)),', "holgura del LTV con orden siempre (r01 O05)"),
    ("K01r", FB, '    "tolerancia_clon": 0.01,', '    "tolerancia_clon": 0.0,', "clones solo exactos (r01 K01)"),
    ("K02r", FB, "        cerca &= np.abs(x[:, None] - x[None, :]) <= tol * np.maximum(a[:, None], a[None, :])",
     "        cerca &= np.abs(x[:, None] - x[None, :]) < tol * np.maximum(a[:, None], a[None, :])", "tolerancia estricta (r01 K02)"),
    ("K03r", FB, "        cerca &= np.abs(x[:, None] - x[None, :]) <= tol * np.maximum(a[:, None], a[None, :])",
     "        cerca &= np.abs(x[:, None] - x[None, :]) <= tol * np.minimum(a[:, None], a[None, :])",
     "tolerancia por el menor (r01 K03)"),
    ("K05r", FB, "    repetidos = len(firmas) - _grupos_casi_iguales(firmas, tol)", "    repetidos = len(firmas) - len(set(firmas))",
     "vuelve la comparación exacta (r01 K05)"),
    ("D01r", FB, '    "peso_maximo_componente": 0.95,', '    "peso_maximo_componente": 1.0,', "sin dominancia (r01 D01)"),
    ("D02r", FB, "        if peso > peso_maximo:", "        if peso >= peso_maximo:", "dominancia en el borde (r01 D02)"),
    ("D03r", P2, '                  "ffo": col["ffo"]}, f"{F}: componentes", u["peso_maximo_componente"], grupos)',
     '                  }, f"{F}: componentes", u["peso_maximo_componente"], grupos)', "REI-LEV sin la base del FFO (r01 D03)"),
    ("O01r", FB, '    "componentes_minimos_orden": len(ESTADISTICOS_ORDEN) + 2,',
     '    "componentes_minimos_orden": len(ESTADISTICOS_ORDEN) + 1,', "orden desde 6 (r01 O01)"),
    ("S01r", P2, '    if 0 < cov_distintos < u["componentes_minimos"]:', '    if 0 < cov_distintos < 2:', "covenants desde 2 (r01 S01)"),
    ("S03r", P2, "                        or float(np.max(_por_grupo(c_, np.unique(g, return_inverse=True)[1]))) / peso\n"
                 "                        > u[\"peso_maximo_componente\"]):",
     "                        or False):", "staking sin dominancia (r01 S03)"),
]
vivos = []
if ANTES is not None and (not SOLO or "REV" in SOLO):
    ruta = COPIA / P2
    orig = ruta.read_text(encoding="utf-8")
    ruta.write_text(ANTES.read_text(encoding="utf-8"), encoding="utf-8")
    try:
        r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_t127_r02.py"], cwd=COPIA,
                           capture_output=True, text=True, timeout=1800, check=False)
    finally:
        ruta.write_text(orig, encoding="utf-8")
    print(f"REV · fichas_p2.py de antes de la r02 · {r.stdout.strip().splitlines()[-1][:160]}", flush=True)
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
