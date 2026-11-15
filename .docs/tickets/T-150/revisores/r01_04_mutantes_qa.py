"""QA r01 de T-150 (revisor) · mutantes propios del código nuevo, distintos de los 22 de `.docs/tickets/T-150/mutantes.py`.

Uso, desde la raíz de la copia de trabajo:
  .venv/bin/python .docs/tickets/T-150/revisores/r01_04_mutantes_qa.py <copia desechable con «t147_mut»> [--grupo FB|CB|CAB|BCE]
Cada mutante cambia un texto que aparece exactamente una vez, ejecuta las pruebas de T-150 (y las de T-149 y T-144 en
FB), restaura el fichero e imprime MUERTO, VIVO o EQUIVALENTE (los que se esperan equivalentes llevan «(equiv.)»).
Termina con 1 si vive alguno que no se espera equivalente. Sin red ni coste."""
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
MUTANTES = [   # (grupo, nombre, fichero, texto, sustituto, pruebas, ¿equivalente esperado?)
    ("FB", "X01 umbral de desplazamiento al doble (q/p ≤ 2 %)", FB, "    desplaza = 2 * rel <= tol\n", "    desplaza = rel <= tol\n",
     P_FB, False),
    ("FB", "X02 media anchura truncada q/2p̃ en vez de (q/2)/(p̃ + q/2)", FB, "np.minimum(rel / (1 + rel), 0.5)", "np.minimum(rel, 0.5)",
     P_FB, False),
    ("FB", "X03 media anchura truncada a la mitad", FB, "np.minimum(rel / (1 + rel), 0.5)", "np.minimum(rel / (1 + rel) / 2, 0.5)",
     P_FB, False),
    ("FB", "X04 centro desplazado hacia abajo (hipótesis de redondeo hacia arriba)", FB,
     "logp + np.where(desplaza, np.log1p(rel), 0.0)", "logp - np.where(desplaza, np.log1p(rel), 0.0)", P_FB, False),
    ("FB", "X05 sin la combinación truncada-truncada", FB, "    for di, dk in ((0, 0), (n, 0), (0, n), (n, n)):",
     "    for di, dk in ((0, 0), (n, 0), (0, n)):", P_FB, False),
    ("FB", "X06 sin la combinación redondeada-truncada", FB, "    for di, dk in ((0, 0), (n, 0), (0, n), (n, n)):",
     "    for di, dk in ((0, 0), (n, 0), (n, n)):", P_FB, False),
    ("FB", "X07 cota truncada sin la tolerancia numérica", FB, "np.minimum(rel / (1 + rel), 0.5)) + tol_num,",
     "np.minimum(rel / (1 + rel), 0.5)),", P_FB, False),
    ("FB", "X08 todas las series con hipótesis truncada (solo coste)", FB, "    con_paso = (desplaza & (rel > tol_num)).any(axis=1)",
     "    con_paso = np.ones(n, dtype=bool)", P_FB, True),
    ("CB", "Y01 un tramo contenido en otro acorta la unión", CB, "            unidos[-1][1] = max(unidos[-1][1], final)",
     "            unidos[-1][1] = final", P, False),
    ("CB", "Y02 los tramos sin ordenar", CB, "    for inicio, final in sorted(tramos):", "    for inicio, final in tramos:", P, False),
    ("CB", "Y03 solo apariciones que no se solapan", CB, "            i = texto.find(dato, i + 1)",
     "            i = texto.find(dato, i + len(dato))", P, False),
    ("CAB", "Z01 las listas del resumen sin limpiar", CAB, "        return [_sin_datos(v) for v in obj]", "        return obj", P, False),
    ("CAB", "Z02 PAQUETE_ILEGIBLE sin escribir el resumen", CAB,
     '            resumen["sin_envio"] = {"motivo": "PAQUETE_ILEGIBLE", "detalle": f"el paquete del Bloque A no se lee ({motivo})"}\n'
     '            _resumen(w, resumen)\n',
     '            resumen["sin_envio"] = {"motivo": "PAQUETE_ILEGIBLE", "detalle": f"el paquete del Bloque A no se lee ({motivo})"}\n',
     P, False),
    ("CAB", "Z03 el aviso de «sin entrega» sin limpiar", CAB, 'print(cadena_b.sin_datos_protegidos(f"Sin entrega del Bloque A',
     'print((f"Sin entrega del Bloque A', P, False),
    ("CAB", "Z04 un --config-a que no es un diccionario no se mira", CAB,
     "    if datos is not None and not isinstance(datos, dict):", "    if False:", P, False),
    ("CAB", "Z05 el aviso del --config-a sin limpiar (no lleva contenido)", CAB,
     'print(cadena_b.sin_datos_protegidos(f"--config-a no se puede leer', 'print((f"--config-a no se puede leer', P, True),
    ("BCE", "W01 el traslado a medias nombra también el que falló", BCE,
     "                    raise EscrituraIncompleta(movidos, e) from e",
     '                    raise EscrituraIncompleta(movidos + [f"{simbolo}.csv"], e) from e', P, False),
    ("BCE", "W02 solo se rechaza si todas las fechas faltan", BCE, "    if fechas.isna().any():", "    if fechas.isna().all():", P, False),
    ("BCE", "W03 solo IncompleteRead de http.client", BCE, "(urllib.error.URLError, OSError, http.client.HTTPException)",
     "(urllib.error.URLError, OSError, http.client.IncompleteRead)", P, False),
    ("BCE", "W04 el enlace roto solo en el destino, no en su ruta", BCE, "        if p.is_symlink() and not p.exists():",
     "        if p == destino and p.is_symlink() and not p.exists():", P, False),
]
vivos = 0
for grupo, nombre, rel, viejo, nuevo, pruebas, equiv in MUTANTES:
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
    assert r.returncode in (0, 1), r.stdout[-1500:] + r.stderr[-1500:]
    muerto = r.returncode == 1
    vivos += not muerto and not equiv
    estado = "MUERTO" if muerto else ("EQUIVALENTE" if equiv else "VIVO")
    print(f"{grupo:3} {nombre:72} {estado:11} {r.stdout.strip().splitlines()[-1][:60]}", flush=True)
print(f"\n{vivos} vivos (sin contar los equivalentes esperados)")
sys.exit(1 if vivos else 0)
