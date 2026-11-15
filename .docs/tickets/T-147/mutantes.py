"""Mutantes de los cambios de T-147, T-144 y T-148 contra sus pruebas (`tests/test_t147.py`, `test_t144.py`,
`test_t148.py` y las vecinas que fijan lo mismo), en una copia desechable de la raíz con «t147_mut» en la ruta.

Uso, desde la raíz de la copia de trabajo:  python .docs/tickets/T-147/mutantes.py <copia desechable> [--ticket T-144]
Cada mutante cambia un texto que tiene que aparecer exactamente una vez, ejecuta sus pruebas y restaura el fichero.
Imprime MUERTO o VIVO por mutante y termina con 1 si alguno sobrevive."""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "t147_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir(), "copia desechable"
SOLO = sys.argv[sys.argv.index("--ticket") + 1] if "--ticket" in sys.argv else None
A = "bloque_a/11_Ejecutor/bloque_a/"
CB, CT, FB, FM, FP = A + "cadena_b.py", A + "contratos.py", A + "motor/frontera_b.py", A + "motor/fichas_mon_idx.py", A + "motor/fichas_p2.py"
CD, BCE, EST = ".docs/scripts/comprobar_datos_a.py", ".docs/scripts/descargar_datos_bce.py", ".docs/scripts/estimar_coste_ciclo_a.py"
P147 = ["tests/test_t147.py", "tests/test_t142_cadena_b.py"]
P144 = ["tests/test_t144.py", "tests/test_t135_motor.py"]
P148 = ["tests/test_t148.py", "tests/test_t145.py"]
MUTANTES = [
    ("T-147", "M01 sin R8 en la petición", CB, "    if contiene_credenciales(peticion):", "    if False:", P147),
    ("T-147", "M02 sin validar tipos_secundarios", CB, '    if "tipos_secundarios" in opcion:', "    if False:", P147),
    ("T-147", "M03 sin enumeraciones de B.1", CB, "if defecto[k] not in v]", "if False]", P147),
    ("T-147", "M04 idioma sin validar", CB, "    if not isinstance(idioma, str) or not RE_IDIOMA.fullmatch(idioma):", "    if False:", P147),
    ("T-147", "M05 claves con espacios", CB, 'RE_SIN_ESPACIOS = re.compile(r"\\S+")', 'RE_SIN_ESPACIOS = re.compile(r".+")', P147),
    ("T-147", "M06 la sonda arrastra la clave", CB, "    encargo.pop(CLAVE_EXTENSION_B, None)", "    pass", P147),
    ("T-147", "M07 R8 sin correos", CT, "        hallados += [m.group(0) for m in RE_CORREO.finditer(t)] + _asignaciones_de_clave(t)",
     "        hallados += _asignaciones_de_clave(t)", P147),
    ("T-147", "M08 R8 sin asignaciones", CT, "        hallados += [m.group(0) for m in RE_CORREO.finditer(t)] + _asignaciones_de_clave(t)",
     "        hallados += [m.group(0) for m in RE_CORREO.finditer(t)]", P147),
    ("T-147", "M09 nombre fuerte con cualquier valor de 6", CT, "            if any(not c.isalpha() for c in v) or len(v) >= 12:",
     "            if True:", P147),
    ("T-147", "M10 sin excluir 0x…", CT, '        if v.lower().startswith("0x") and all(c in "0123456789abcdefABCDEF" for c in v[2:]):',
     "        if False:", P147),
    ("T-147", "M11 correo de imagen @2x", CT, r"@(?!\d+x\.)", "@", P147),
    ("T-147", "M12 --clases sin choices", CD, "choices=CLASES, metavar=", "metavar=", P147),
    ("T-147", "M13 universo vacío en verde", CD, "    if universo.empty:", "    if False:", P147),
    ("T-147", "M14 BCE con fechas repetidas", BCE, "    if not repetidas.empty:", "    if False:", P147),
    ("T-147", "M15 BCE con una serie vacía", BCE, "        if s.empty:", "        if False:", P147),
    ("T-147", "M16 BCE sin moneda", BCE, "    if sin:\n", "    if False:\n", P147),
    ("T-144", "M17 sin la regla de niveles", FB, "            vivos = vivos[~(distinta[vivos] & (lo[vivos] > hi[vivos]))]",
     "            vivos = vivos[~distinta[vivos]]", P144),
    ("T-144", "M18 cota sin tope", FB, "            B = np.minimum(cota_redondeo[Iv, tramo] + cota_redondeo[Kv, tramo], tope)",
     "            B = cota_redondeo[Iv, tramo] + cota_redondeo[Kv, tramo]", P144),
    ("T-144", "M19 paso de precio siempre 1", FB, "        paso[nuevos] = 10.0 ** -d", "        paso[nuevos] = 1.0", P144),
    ("T-144", "M20 sin el año mínimo en común", FB, "    copia = vivos[ultima[vivos] - primera[vivos] >= anios_minimos]",
     "    copia = vivos", P144),
    ("T-144", "M21 precios ≤ 0 aceptados", FM, "        if not (np.isfinite(x).all() and (x > 0).all()):", "        if False:", P144),
    ("T-144", "M22 lo repetido en los dos no iguala", FB, "            iguales = iguales + (dos_rep & ~igual_j)", "            pass", P144),
    ("T-144", "M23 CHR-TOKEN sin marcar lo repetido", FP, "u[\"tolerancia_clon\"], lim, repetidos_aviso)", "u[\"tolerancia_clon\"], lim)", P144),
    ("T-144", "M24 lo repetido en los dos cuenta como informativo", FB,
     "(cero[:, None] & cero[None, :]) | dos_rep\n", "(cero[:, None] & cero[None, :])\n", P144),
    ("T-148", "M25 la contrarréplica con S4", EST, "papel in MULTIPLICAN_ENCARGO), a)", "False), a)", P148),
    ("T-148", "M26 sin el tope del presupuesto", EST, "else min(tok, encargo(a) + encargo_max(bolsa))", "else tok", P148),
    ("T-148", "M27 tope sin la salida mínima ni el margen (T-146)", EST, "(limite_max[bolsa] - 0.5 * salida_minima / uc[1]) / factor_reserva", "limite_max[bolsa]", P148),
    ("T-148", "M28 los tipos siempre de la configuración", EST,
     "    tipos = list(perfiles_activos(cfg)) if tipos is None else list(tipos)", "    tipos = list(perfiles_activos(cfg))", P148),
    ("T-148", "M29 F10 ignorado", EST, "    return list(p02) if p02 else list(perfiles_activos(cfg))", "    return list(perfiles_activos(cfg))", P148),
    ("T-148", "M30 con T-146 igual que sin", EST, "    if con_t146:   #", "    if False:   #", P148),
    ("T-148", "M31 lecturas de la búsqueda sin los reenvíos", EST, "max_usos * vueltas * (vueltas + 1) / 2", "max_usos", P148),
    ("T-148", "M32 sin el aviso de la historia antigua", CD,
     '            f["aviso"] = f"dato inválido en la historia, anterior', '            pass  # f"dato inválido en la historia, anterior', P148),
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
    print(f"{ticket} {nombre:52} {'MUERTO' if muerto else 'VIVO'}  {r.stdout.strip().splitlines()[-1][:80]}", flush=True)
print(f"\n{vivos} vivos")
sys.exit(1 if vivos else 0)
