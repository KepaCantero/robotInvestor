"""Mutantes de las correcciones de T-128 (REI-NAV-001, REI-FFO-001, IDX-REB-001, CHR-FUND-001, FON-DISC-001 y FON-TD-001).
Se aplican en una copia desechable del ejecutor (DESTINO/11_Ejecutor, con el Catálogo al lado) y se ejecuta
`tests/test_t128_frontera.py` (-x). MUERTO = alguna prueba falla.
Uso: python impl_mutantes.py ORIGEN_EJECUTOR DESTINO [--solo ID,ID]
(DESTINO: carpeta desechable fuera del repo, cuya ruta contenga «_mut»; sin --solo se borra al acabar)"""
import shutil
import subprocess
import sys
from pathlib import Path

ORIGEN = Path(sys.argv[1]).resolve()
BASE = Path(sys.argv[2]).resolve()
assert "_mut" in BASE.name and not (BASE / ".git").exists() and BASE != ORIGEN, "DESTINO debe ser una carpeta desechable"
COPIA = BASE / "11_Ejecutor"
SOLO = sys.argv[sys.argv.index("--solo") + 1].split(",") if "--solo" in sys.argv else None
PY = sys.executable
PRUEBAS = ["tests/test_t128_frontera.py"]
FR, FM, FD = "bloque_a/motor/fichas_reales.py", "bloque_a/motor/fichas_mon_idx.py", "bloque_a/motor/fichas_fon_der.py"

if BASE.exists():
    shutil.rmtree(BASE)
BASE.mkdir(parents=True)
shutil.copytree(ORIGEN, COPIA, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
shutil.copytree(ORIGEN.parent / "04_Motor_conocimiento_y_catalogo", BASE / "04_Motor_conocimiento_y_catalogo")

M = [
    # REI-NAV-001
    ("N01", FR, '        "antiguedad_nav_dias_max": max(int((f["fecha"] - f["fecha_nav"]).days) for f in filas),',
     '        "antiguedad_nav_dias_max": max(int((f["fecha"] - f["fecha_nav"]).days) for f in filas),\n'
     '        "componentes": {f["id"]: {"prima_pct": 0.0} for f in filas},', "vuelven las filas por sociedad"),
    ("N02", FR, '            derivados += 1                     # T-128 (1.6): la limitación ya no cita la sociedad (abajo, un recuento)',
     '            derivados += 1\n            lim.append(f"{cid}: otros pasivos derivados")', "la limitación cita la sociedad"),
    ("N03", FR, '    if distintos >= u["componentes_minimos_dispersion"]:', "    if True:", "dispersión con cualquier número"),
    ("N04", FR, '    rango = _orden(primas, u, sin_orden, "las primas (mínimo y máximo)", distintos)',
     '    rango = {"minimo": float(np.min(primas)), "maximo": float(np.max(primas))}', "rango siempre"),
    ("N05", FR, '                                  u["componentes_minimos"], u["tolerancia_clon"])\n    distintos = len(set(grupos.tolist()))',
     '                                  1, u["tolerancia_clon"])\n    distintos = len(set(grupos.tolist()))', "REI-NAV sin mínimo de distintos"),
    ("N06", FR, '    _rechazo_concentradas(_concentradas({"la prima agregada": (capit * primas, capit)}, u, tol), f"{F}: componentes", u)',
     "    pass", "REI-NAV sin la aportación a la prima"),
    ("N07", FR, '        if not conc:\n            nav_ajustado =', '        if True:\n            nav_ajustado =',
     "NAV ajustado aunque lo aporte una sociedad"),
    ("N08", FR, '    _sin_dominio({"capitalizacion": capit, "nav": [f["nav"] for f in filas]}, f"{F}: componentes",',
     '    _sin_dominio({"nav": [f["nav"] for f in filas]}, f"{F}: componentes",', "REI-NAV sin la base de capitalización"),
    # REI-FFO-001
    ("F01", FR, '    if len(comps) < u["componentes_minimos"]:   # T-128 (1.6): un agregado de una sociedad es la sociedad',
     "    if False:", "REI-FFO con un componente"),
    ("F02", FR, '        "n_componentes": len(ids), "cobertura": resumen_cob,',
     '        "n_componentes": len(ids), "cobertura": resumen_cob, "cobertura_por_componente": {c: 1.0 for c in ids},',
     "vuelve la cobertura por componente"),
    ("F03", FR, '        lim.append(f"{len(ids) - len(con_div)} componente(s) sin dividendo en {ultimo}: cobertura indefinida en ellos")',
     '        lim.append(f"{ids[0]}: sin dividendo en {ultimo}")', "la limitación cita la sociedad"),
    ("F04", FR, '    if cob.size and _orden(cob, u, sin_orden, "la cobertura de los componentes",',
     '    if cob.size or _orden(cob, u, sin_orden, "la cobertura de los componentes",', "cobertura con cualquier número"),
    ("F05", FR, '                                   for c in ids], f"{F}: componentes", u["componentes_minimos"], u["tolerancia_clon"])',
     '                                   for c in ids], f"{F}: componentes", 1, u["tolerancia_clon"])', "REI-FFO sin copias"),
    ("F06", FR, '    _rechazo_concentradas(_concentradas({"el rendimiento FFO": (ult["ffo"], cap_a), "el rendimiento AFFO": (ult["affo"], cap_a),',
     '    _rechazo_concentradas(_concentradas({"el rendimiento AFFO": (ult["affo"], cap_a),', "REI-FFO sin la aportación al FFO"),
    # IDX-REB-001
    ("R01", FM, "        if conc:\n            _limitacion_concentradas(conc, FRONTERA_B, lim)",
     "        if False:\n            _limitacion_concentradas(conc, FRONTERA_B, lim)", "la cesta de un valor se entrega"),
    ("R02", FM, '        "demanda_estimada": demanda,   # T-128 (1.6): sin la fila de cada valor (antes «por_componente», con su id)',
     '        "demanda_estimada": demanda, "por_componente": filas,', "vuelve la fila por valor"),
    # CHR-FUND-001
    ("P01", FR, '        "financiacion_pct_anual": float(fin.loc[T]) * PCT,\n        "base_pct_anual"',
     '        "financiacion_pct_anual": float(fin.loc[T]) * PCT,\n        "pesos": {k: 0.5 for k in nombres},\n        "base_pct_anual"',
     "vuelve el peso de cada plataforma"),
    # FON-DISC-001 y FON-TD-001
    ("D01", FD, '                       if len(idx) >= m["miembros"] else None}', "                       }",
     "subcategoría de un fondo con cifra"),
    ("D02", FD, '    orden = len(nombres) >= FRONTERA_B["componentes_minimos_orden"]', "    orden = True", "mínimo y máximo siempre"),
    ("D03", FD, '            ajustados.append(ajuste)   # T-128 (1.6): la limitación no cita el miembro (abajo, un recuento)',
     '            ajustados.append(ajuste)\n            lim.append(f"miembro {nom}: NAV")', "la limitación cita el miembro"),
    ("T01", FD, '            pocos = len(grupos[g]) < m["miembros"]', "            pocos = False", "segmento de un vehículo con cifra"),
]
vivos = []
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
