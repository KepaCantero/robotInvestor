"""QA r01 de T-149 (revisor) · mutantes propios del código nuevo de T-149, además de los de `T-147/mutantes.py` y de
`T-147/revisores/r01_03_mutantes_qa.py`.

Uso, desde la raíz de la copia de trabajo:
  .venv/bin/python .docs/tickets/T-149/revisores/r01_02_mutantes_qa.py <copia desechable con «t147_mut»> [--grupo FB|CB|BCE]
Cada mutante cambia un texto que aparece exactamente una vez, ejecuta las pruebas de su grupo (las de T-149 y las vecinas
que fijan lo mismo) y restaura el fichero. Imprime MUERTO, VIVO o EQUIVALENTE (un mutante que no puede cambiar el
resultado; se ejecuta igual, para que se vea) y termina con 1 si alguno no equivalente sobrevive."""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "t147_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir(), "copia desechable"
SOLO = sys.argv[sys.argv.index("--grupo") + 1] if "--grupo" in sys.argv else None
A = "bloque_a/11_Ejecutor/bloque_a/"
FB, CB = A + "motor/frontera_b.py", A + "cadena_b.py"
CAB, BCE = ".docs/scripts/cadena_a_b.py", ".docs/scripts/descargar_datos_bce.py"
P_FB = ["tests/test_t149.py", "tests/test_t144.py", "tests/test_t135_motor.py"]
P_CB = ["tests/test_t149.py", "tests/test_t147.py", "tests/test_t142_cadena_b.py"]
P_BCE = ["tests/test_t149.py", "tests/test_t147.py", "tests/test_t141_datos_bce.py"]
MUTANTES = [   # (grupo, nombre, fichero, texto, sustituto, pruebas, equivalente)
    ("FB", "N01 fracción en la rejilla 0,9 → 1 (todos los precios)", FB, '"fraccion_en_rejilla": 0.9}', '"fraccion_en_rejilla": 1.0}', P_FB, False),
    ("FB", "N02 fracción en la rejilla 0,9 → 0,5", FB, '"fraccion_en_rejilla": 0.9}', '"fraccion_en_rejilla": 0.5}', P_FB, False),
    ("FB", "N03 sin el múltiplo 25", FB, '{"multiplos_de_la_decada": (25, 5, 2),', '{"multiplos_de_la_decada": (5, 2),', P_FB, False),
    ("FB", "N04 sin el múltiplo 2", FB, '{"multiplos_de_la_decada": (25, 5, 2),', '{"multiplos_de_la_decada": (25, 5),', P_FB, False),
    ("FB", "N05 denominador binario 256 → 16", FB, '"denominador_binario_maximo": 256,', '"denominador_binario_maximo": 16,', P_FB, False),
    ("FB", "N06 sin el paso por década", FB, "    rel = np.maximum(rel, _paso_por_decada(", "    rel = np.maximum(rel, 0 * _paso_por_decada(", P_FB, False),
    ("FB", "N07 potencias desde 1 (sin pasos de 5, 10, 50…)", FB, "    d0 = -int(np.floor(np.log10(mayor))) if mayor >= 1 else 0",
     "    d0 = 0", P_FB, False),
    ("FB", "N08 los huecos (NaN) cuentan como precios en la rejilla", FB, "    encaja &= hay\n", "    pass\n", P_FB, False),
    ("FB", "N09 la fracción sobre todas las fechas, no sobre las que tienen precio", FB,
     'REJILLAS_PRECIO["fraccion_en_rejilla"] * hay.sum(axis=1)', 'REJILLAS_PRECIO["fraccion_en_rejilla"] * hay.shape[1]', P_FB, False),
    ("FB", "N10 el paso de la última década pisa los de las demás", FB,
     "paso[cruzan] = np.where(en, _paso_de_precio(sub, en, tol_numerica)[:, None], paso[cruzan])",
     "paso[cruzan] = np.where(hay[cruzan], _paso_de_precio(sub, en, tol_numerica)[:, None], paso[cruzan])", P_FB, False),
    ("FB", "N11 fracciones binarias sin el margen numérico (potencia > 10⁻ᵏ)", FB,
     "(potencia >= 10.0 ** -k * (1 - tol_numerica)) & (q > paso)", "(potencia > 10.0 ** -k) & (q > paso)", P_FB, False),
    ("FB", "N12 un múltiplo más fino pisa uno más grueso", FB, "(potencia > 0) & (m * potencia > paso)", "(potencia > 0)", P_FB, False),
    ("CB", "N20 ErrorCadenaB sin limpiar el detalle", CB, "        detalle = sin_datos_protegidos(detalle)", "        pass", P_CB, False),
    ("CB", "N21 mensajes de jsonschema recortados antes de limpiarlos", CB,
     "return [sin_datos_protegidos(f\"{'/'.join(map(str, e.absolute_path)) or '(raíz)'}: {e.message}\")[:200]",
     "return [sin_datos_protegidos(f\"{'/'.join(map(str, e.absolute_path)) or '(raíz)'}: {e.message}\"[:200])", P_CB, False),
    ("CB", "N22 sin el aviso cuando el dato no se puede quitar", CB, "    if secretos_en_texto(texto) or contiene_credenciales(texto):",
     "    if False:", P_CB, False),
    ("CB", "N23 sin la comprobación de G3 en la librería", CB, '    if paquete.get("estado_g3") not in ESTADOS_G3_ENTREGA:', "    if False:", P_CB, False),
    ("CB", "N24 APTO_CON_ADVERTENCIAS no se envía", CB, 'ESTADOS_G3_ENTREGA = ("APTO", "APTO_CON_ADVERTENCIAS")', 'ESTADOS_G3_ENTREGA = ("APTO",)', P_CB, False),
    ("CB", "N25 el script sin mirar «entrega» (G3 y ruta bastan)", CAB, 'ciclo.get("entrega") != "ENTREGADA" or ', "", P_CB, True),
    ("CB", "N26 el script sin la comprobación de entrega (la librería la repite)", CAB,
     '        if ciclo.get("entrega") != "ENTREGADA" or ciclo.get("g3") not in cadena_b.ESTADOS_G3_ENTREGA or not ruta_paquete:',
     "        if not ruta_paquete:", P_CB, False),
    ("CB", "N27 el script imprime el fallo de un ejecutor sin limpiar", CAB,
     "        print(cadena_b.sin_datos_protegidos(str(e)), file=sys.stderr)", "        print(str(e), file=sys.stderr)", P_CB, False),
    ("BCE", "N30 sin comprobar el destino antes de descargar", BCE, "        comprobar_destino(destino, CRUCES)   # T-149: antes de descargar",
     "        pass", P_BCE, False),
    ("BCE", "N31 sin comprobar el destino al escribir (main ya lo mira)", BCE, "    comprobar_destino(destino, series)", "    pass", P_BCE, True),
    ("BCE", "N32 fechas sin pasar a texto", BCE, 'pd.to_datetime(crudo["TIME_PERIOD"].astype(str), format="%Y-%m-%d")',
     'pd.to_datetime(crudo["TIME_PERIOD"], format="%Y-%m-%d")', P_BCE, True),   # equivalente con pandas 3 (aviso de cambio futuro)
    ("BCE", "N33 repetidas en el texto (como antes)", BCE,
     'repetidas = crudo[pd.DataFrame({"m": crudo["CURRENCY"], "f": fechas}).duplicated(keep=False)]',
     'repetidas = crudo[crudo.duplicated(["CURRENCY", "TIME_PERIOD"], keep=False)]', P_BCE, False),
    ("BCE", "N34 un CSV de destino que es una carpeta no se mira", BCE,
     'if (destino / f"{s}.csv").exists() and not (destino / f"{s}.csv").is_file()]', "if False]", P_BCE, False),
    ("BCE", "N35 un antecesor que es un fichero no se mira", BCE, "            if not p.is_dir():", "            if False:", P_BCE, False),
]
vivos = 0
for grupo, nombre, rel, viejo, nuevo, pruebas, equivalente in MUTANTES:
    if SOLO and grupo != SOLO:
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
    vivos += (not muerto) and not equivalente
    estado = "MUERTO" if muerto else ("EQUIVALENTE" if equivalente else "VIVO")
    print(f"{grupo:3} {nombre:75} {estado:11} {r.stdout.strip().splitlines()[-1][:70]}", flush=True)
print(f"\n{vivos} vivos (sin contar los equivalentes)")
sys.exit(1 if vivos else 0)
