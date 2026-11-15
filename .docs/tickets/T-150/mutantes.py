"""T-150 · mutantes del código nuevo (H-01, H-02, H-04, H-05, H-06 y las observaciones de la QA r01 de T-149).

Uso, desde la raíz de la copia de trabajo:
  .venv/bin/python .docs/tickets/T-150/mutantes.py <copia desechable con «t147_mut»> [--grupo FB|CB|CAB|BCE]
Cada mutante cambia un texto que aparece exactamente una vez, ejecuta las pruebas de su grupo y restaura el fichero.
Imprime MUERTO o VIVO y termina con 1 si alguno sobrevive. Sin red ni coste."""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "t147_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir(), "copia desechable"
SOLO = sys.argv[sys.argv.index("--grupo") + 1] if "--grupo" in sys.argv else None
A = "bloque_a/11_Ejecutor/bloque_a/"
FB, CB = A + "motor/frontera_b.py", A + "cadena_b.py"
CAB, BCE = ".docs/scripts/cadena_a_b.py", ".docs/scripts/descargar_datos_bce.py"
P_FB = ["tests/test_t150.py", "tests/test_t149.py", "tests/test_t144.py"]
P = ["tests/test_t150.py", "tests/test_t149.py"]
MUTANTES = [   # (grupo, nombre, fichero, texto, sustituto, pruebas)
    ("FB", "F1 sin la hipótesis truncada", FB, "    for di, dk in ((0, 0), (n, 0), (0, n), (n, n)):", "    for di, dk in ((0, 0),):", P_FB),
    ("FB", "F2 el centro truncado sin desplazar", FB, "logp + np.where(desplaza, np.log1p(rel), 0.0)", "logp + 0.0", P_FB),
    ("FB", "F3 se desplazan también los pasos grandes", FB, "    desplaza = 2 * rel <= tol\n", "    desplaza = rel >= 0\n", P_FB),
    ("FB", "F4 la hipótesis por serie, no por precio", FB, "    con_paso = (desplaza & (rel > tol_num)).any(axis=1)",
     "    con_paso = (rel > tol_num).any(axis=1) & desplaza.all(axis=1)", P_FB),
    ("FB", "F5 sin pares truncados con la segunda serie", FB, "quedan = (con_paso[I] | (di == 0)) & (con_paso[K] | (dk == 0))",
     "quedan = (con_paso[I] | (di == 0)) & (con_paso[K] | (dk == 0)) & (dk == 0)", P_FB),
    ("FB", "F6 las etiquetas sin volver a la serie", FB, "    f = np.concatenate(filas) % n if filas", "    f = np.concatenate(filas) if filas", P_FB),
    ("CB", "C1 los tramos que se solapan no se unen", CB, "        if unidos and inicio <= unidos[-1][1]:", "        if False:", P),
    ("CB", "C2 los tramos que se tocan no se unen", CB, "        if unidos and inicio <= unidos[-1][1]:",
     "        if unidos and inicio < unidos[-1][1]:", P),
    ("CB", "C3 solo la primera aparición de cada dato", CB, "            i = texto.find(dato, i + 1)", "            i = -1", P),
    ("CB", "C4 sustitución por cadenas, como antes", CB, "    texto = _sin_tramos(texto, secretos_en_texto(texto))",
     "    for dato in sorted(secretos_en_texto(texto), key=len, reverse=True):\n        texto = texto.replace(dato, DATO_PROTEGIDO)", P),
    ("CAB", "S1 el stderr recortado antes de limpiarlo", CAB, "{cadena_b.sin_datos_protegidos(r.stderr)[-2000:]}",
     "{cadena_b.sin_datos_protegidos(r.stderr[-2000:])}", P),
    ("CAB", "S2 la salida que no es JSON recortada antes de limpiarla", CAB, "{cadena_b.sin_datos_protegidos(r.stdout)[-1000:]}",
     "{cadena_b.sin_datos_protegidos(r.stdout[-1000:])}", P),
    ("CAB", "S3 el resumen sin limpiar", CAB, "    limpio = _sin_datos(resumen)", "    limpio = resumen", P),
    ("CAB", "S4 las claves del resumen sin limpiar", CAB, "{_sin_datos(k): _sin_datos(v)", "{k: _sin_datos(v)", P),
    ("CAB", "S5 el error de yaml tal cual", CAB,
     '        return f"{type(e).__name__} en la línea {marca.line + 1}, columna {marca.column + 1}"', "        return str(e)", P),
    ("CAB", "S6 sin mirar el --config-a antes", CAB, "            _leer_yaml_extra(a.config_a)", "            pass", P),
    ("CAB", "S7 un paquete que no es un objeto se acepta", CAB, "            if not isinstance(paquete, dict):", "            if False:", P),
    ("CAB", "S8 sin capturar el paquete que no se lee", CAB,
     "        except (OSError, UnicodeDecodeError, json.JSONDecodeError, TypeError) as e:", "        except ZeroDivisionError as e:", P),
    ("BCE", "B1 filas sin fecha aceptadas", BCE, "    if fechas.isna().any():", "    if False:", P),
    ("BCE", "B2 sin los errores de http.client", BCE, "(urllib.error.URLError, OSError, http.client.HTTPException)",
     "(urllib.error.URLError, OSError)", P),
    ("BCE", "B3 el traslado a medias como antes", BCE, "                if movidos:", "                if False:", P),
    ("BCE", "B4 un enlace roto como destino no se mira", BCE, "        if p.is_symlink() and not p.exists():", "        if False:", P),
]
vivos = 0
for grupo, nombre, rel, viejo, nuevo, pruebas in MUTANTES:
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
    vivos += not muerto
    print(f"{grupo:3} {nombre:60} {'MUERTO' if muerto else 'VIVO':7} {r.stdout.strip().splitlines()[-1][:70]}", flush=True)
print(f"\n{vivos} vivos")
sys.exit(1 if vivos else 0)
