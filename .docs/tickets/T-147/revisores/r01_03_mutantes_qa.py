"""QA r01 de T-147, T-144 y T-148 (revisor) · mutantes propios, además de los de `.docs/tickets/T-147/mutantes.py`.

Uso, desde la raíz de la copia de trabajo:
  .venv/bin/python .docs/tickets/T-147/revisores/r01_03_mutantes_qa.py <copia desechable con «t147_mut»> [--ticket T-144]
Cada mutante cambia un texto que aparece exactamente una vez, ejecuta las mismas pruebas que `mutantes.py` usa para su
ticket y restaura el fichero. Imprime MUERTO o VIVO y termina con 1 si alguno sobrevive."""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "t147_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir(), "copia desechable"
SOLO = sys.argv[sys.argv.index("--ticket") + 1] if "--ticket" in sys.argv else None
A = "bloque_a/11_Ejecutor/bloque_a/"
CB, CT, FB, FM = A + "cadena_b.py", A + "contratos.py", A + "motor/frontera_b.py", A + "motor/fichas_mon_idx.py"
CD, BCE, EST = ".docs/scripts/comprobar_datos_a.py", ".docs/scripts/descargar_datos_bce.py", ".docs/scripts/estimar_coste_ciclo_a.py"
P147 = ["tests/test_t147.py", "tests/test_t142_cadena_b.py"]
P144 = ["tests/test_t144.py", "tests/test_t135_motor.py"]
P148 = ["tests/test_t148.py", "tests/test_t145.py"]
MUTANTES = [
    ("T-147", "Q01 idioma con match en vez de fullmatch", CB, "RE_IDIOMA.fullmatch(idioma)", "RE_IDIOMA.match(idioma)", P147),
    ("T-147", "Q02 clave genérica desde 8 caracteres", CT, r"[A-Za-z0-9._~+/=\-]{16,}", r"[A-Za-z0-9._~+/=\-]{8,}", P147),
    ("T-147", "Q03 dominio de primer nivel de 1 letra", CT, r"\.[A-Za-z]{2,24}(?![A-Za-z0-9\-])", r"\.[A-Za-z]{1,24}(?![A-Za-z0-9\-])", P147),
    ("T-147", "Q04 --clases admite la lista vacía", CD, 'nargs="+"', 'nargs="*"', P147),
    ("T-147", "Q05 BCE con fechas en cualquier formato", BCE, ', format="%Y-%m-%d")', ")", P147),
    ("T-147", "Q06 BCE sin comprobar las columnas", BCE, "    falta = [c for c in COLUMNAS if c not in crudo.columns]",
     "    falta = []", P147),
    ("T-147", "Q07 la sonda sin los filtros", ".docs/scripts/cadena_a_b.py",
     '                resumen["sonda_sin_correspondencia"] = {"opp_id": sin["opp_id"], "codigo": e.codigo, "detalle": e.detalle}\n                pet = None',
     '                raise', P147),
    ("T-144", "Q08 cota de redondeo sin la tolerancia numérica", FB,
     "    cota_redondeo = -np.log1p(-np.minimum(rel, 0.5)) + tol_num", "    cota_redondeo = -np.log1p(-np.minimum(rel, 0.5))", P144),
    ("T-144", "Q09 error de redondeo de un paso entero (q/p en vez de q/2p)", FB,
     "paso[:, None] / (2 * np.where(hay, precios, 1.0))", "paso[:, None] / (np.where(hay, precios, 1.0))", P144),
    ("T-144", "Q10 lo > hi pasa a lo >= hi", FB, "(lo[vivos] > hi[vivos])", "(lo[vivos] >= hi[vivos])", P144),
    ("T-144", "Q11 precio 0 aceptado", FM, "(x > 0).all()", "(x >= 0).all()", P144),
    ("T-148", "Q12 con T-146, la búsqueda no entra en el precio por UC", EST,
     "cota_presupuesto = limites * max(p_busq / p_tipos, p_busq / p_comun, 1.0)", "cota_presupuesto = limites", P148),
    ("T-148", "Q13 la COMÚN con los tipos en N2", EST,
     'limite_max["COMUN"] = (1 + amp) * max(minimo_comun, tope - len(tipos) * niveles[0])',
     'limite_max["COMUN"] = (1 + amp) * max(minimo_comun, tope - len(tipos) * niveles[-1])', P148),
    ("T-148", "Q14 S4b sin lo medido", EST, "tok = encargo(a) + encargo_max(bolsa) if multiplica", "tok = encargo_max(bolsa) if multiplica", P148),
    ("T-148", "Q15 --estado inexistente se acepta", EST, "    if not Path(estado).is_dir():", "    if False:", P148),
]
vivos = 0
for ticket, nombre, rel, viejo, nuevo, pruebas in MUTANTES:
    if SOLO and ticket != SOLO:
        continue
    ruta = COPIA / rel
    original = ruta.read_text(encoding="utf-8")
    assert original.count(viejo) == 1, f"{nombre}: el texto aparece {original.count(viejo)} veces"
    ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *pruebas],
                           cwd=COPIA / "bloque_a" / "11_Ejecutor", capture_output=True, text=True, check=False)
    finally:
        ruta.write_text(original, encoding="utf-8")
    muerto = r.returncode == 1
    assert r.returncode in (0, 1), r.stdout[-1500:] + r.stderr[-1500:]
    vivos += not muerto
    print(f"{ticket} {nombre:60} {'MUERTO' if muerto else 'VIVO'}  {r.stdout.strip().splitlines()[-1][:80]}", flush=True)
print(f"\n{vivos} vivos")
sys.exit(1 if vivos else 0)
