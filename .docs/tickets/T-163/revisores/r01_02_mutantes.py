"""QA r01 de T-163 · mutantes propios del revisor (N01–N12) sobre `evaluador.py`, `motor/servicio.py` y `tests/conftest.py`,
distintos de los T01–T15 de `.docs/tickets/T-163/mutantes_t163.py`.

Uso, desde la raíz:  .venv/bin/python .docs/tickets/T-163/revisores/r01_02_mutantes.py <copia «…_mut» con bloque_a/ y .docs/> [--solo N01,N05]
Cada mutante se aplica en la copia, se pasan las pruebas de `PRUEBAS` (con -x) y se restaura. Vivo = ninguna prueba lo detecta.
A cada vivo se le pasa además `r01_01_ataques.py` de esta ronda (sin sus `test_h0*`, que fallan a propósito). N05 rompe el ayudante
de pruebas y se pasa contra las pruebas que lo usan (sin -x) para ver cuáles lo notan. Termina con 1 si alguno no aplica.
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "_mut" in COPIA.name and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir(), "hace falta una copia «…_mut»"
SOLO = set(sys.argv[sys.argv.index("--solo") + 1].split(",")) if "--solo" in sys.argv else None
PY = str(Path(__file__).resolve().parents[4] / ".venv" / "bin" / "python")
EV, SV, CF = ("bloque_a/11_Ejecutor/bloque_a/evaluador.py", "bloque_a/11_Ejecutor/bloque_a/motor/servicio.py",
              "bloque_a/11_Ejecutor/tests/conftest.py")
PRUEBAS = ["tests/test_t163_hallazgos_t160.py", "tests/test_t160_reejecucion_certificado.py", "tests/test_t66_evaluacion.py",
           "tests/test_t66_propuestas.py"]
ATAQUES = ["../../.docs/tickets/T-163/revisores/r01_01_ataques.py", "-k", "not test_h0"]
ADAPTADAS = ["tests/test_fase4_huecos.py", "tests/test_t53_evaluacion_y_almacen.py", "tests/test_t66_evaluacion.py",
             "tests/test_t87_datos.py", "-k", "pb33 or pb32_la_probabilidad or r13_certificado or ece_cero or umbral_de_revocacion "
             "or pa10_revocar"]
MUTANTES = [
    ("N01", "exclusividad: gana el ÚLTIMO CERT- que cita la re-ejecución", EV,
     'primero.setdefault(e["reejecucion"], e.get("id"))', 'primero[e["reejecucion"]] = e.get("id")'),
    ("N02", "H-05: cuenta cualquier CT-10 con NO posterior al soporte (también las anteriores a la citada)", EV,
     "isinstance(q, int) and q > sq_r and co not in COINCIDE_CT10", "isinstance(q, int) and q > sq_s and co not in COINCIDE_CT10"),
    ("N03", "H-01: no se comparan las cifras de la muestra efectiva", EV,
     "distintas = servicio.comparar(cifras_del_certificado(c), cifras_del_soporte(payload), tol_ct04)",
     'distintas = [d for d in servicio.comparar(cifras_del_certificado(c), cifras_del_soporte(payload), tol_ct04) '
     'if "muestra_efectiva" not in d]'),
    ("N04", "H-01: no se compara el Brier de referencia", EV,
     "distintas = servicio.comparar(cifras_del_certificado(c), cifras_del_soporte(payload), tol_ct04)",
     'distintas = [d for d in servicio.comparar(cifras_del_certificado(c), cifras_del_soporte(payload), tol_ct04) '
     'if "brier_ref" not in d]'),
    ("N05", "ayudante de pruebas: el certificado que escribe no pasa la comprobación (huella de entradas falsa)", CF,
     '"huella_entradas": soporte["datos"][0]["huella"]', '"huella_entradas": "0" * 16'),
    ("N06", "H-02: el VIGENTE revocado no se vuelve a evaluar ni proponer en la misma revisión", EV,
     "            revocados.append(c[\"id\"])\n            vigentes_sin_rex[c[\"id\"]] = motivo_v\n",
     "            revocados.append(c[\"id\"])\n            vigentes_sin_rex[c[\"id\"]] = motivo_v\n"
     "            vigentes[(c[\"celda\"][\"clase\"], c[\"celda\"][\"horizonte\"], c[\"celda\"].get(\"metodo\"))] = c\n"),
    ("N07", "CT-04: dos PROPUESTO de la misma celda en un lote", EV,
     '            vigentes.add((celda.get("clase"), celda.get("horizonte"), celda.get("metodo")))\n', "            pass\n"),
    ("N08", "H-05: solo cuentan las CT-10 del Evaluador", EV,
     'if r.get("tipo_entrada") == "REEJECUCION" and isinstance(rx, dict)',
     'if r.get("tipo_entrada") == "REEJECUCION" and r.get("solicitante") == "AG-20" and isinstance(rx, dict)'),
    ("N09", "H-04: el Evaluador vuelve a aceptar un mínimo de 1 en su configuración", EV,
     "if not servicio.min_conglomerados_valido(v):", "if not (isinstance(v, int) and not isinstance(v, bool) and v >= 1):"),
    ("N10", "H-04: FC-EVAL-001 valida el mínimo también sin fechas", SV,
     'if fechas is not None and "min_conglomerados" in params and not', 'if "min_conglomerados" in params and not'),
    ("N11", "H-01: sin comparar las huellas de la re-ejecución con las del soporte (solo CERT- frente a soporte)", EV,
     "or huellas_s != [c.get(\"huella_entradas\")] or huellas_r != huellas_s", "or huellas_s != [c.get(\"huella_entradas\")]"),
    ("N12", "H-02: la revocación de un VIGENTE sin re-ejecución no se escribe en F6 (solo se informa)", EV,
     "            self.almacen.escribir(\"F6\", \"AG-20\", {\"tipo_entrada\": \"CERT_REVOCACION\", \"id\": c[\"id\"], \"estado\": \"REVOCADO\",\n"
     "                                                  \"motivo_cambio\": \"sin re-ejecución CT-10 coincidente del cálculo que lo \"",
     "            (lambda *a: None)(\"F6\", \"AG-20\", {\"tipo_entrada\": \"CERT_REVOCACION\", \"id\": c[\"id\"], \"estado\": \"REVOCADO\",\n"
     "                                                  \"motivo_cambio\": \"sin re-ejecución CT-10 coincidente del cálculo que lo \""),
]
EQUIVALENTES = {
    "N11": "la REEJECUCION la escribe el Motor con los datos que re-ejecutó; si no son los del soporte, `coincide` ya es NO "
           "(DATOS_DISTINTOS); solo difiere con una REEJECUCION forjada en el RC (AG-13)",
}


def pytest(args, cwd, x=True):
    r = subprocess.run([PY, "-m", "pytest", "-q", *(["-x"] if x else []), "-p", "no:cacheprovider", *args], cwd=cwd,
                       capture_output=True, text=True, timeout=5400)
    return r.returncode == 0, (r.stdout.strip().splitlines() or [""])[-1], r.stdout


ejec = COPIA / "bloque_a" / "11_Ejecutor"
vivos, no_aplica = [], []
for mid, desc, ruta, viejo, nuevo in MUTANTES:
    if SOLO and mid not in SOLO:
        continue
    f = COPIA / ruta
    texto = f.read_text(encoding="utf-8")
    if texto.count(viejo) != 1:
        no_aplica.append(mid)
        print(f"{mid} NO APLICA ({texto.count(viejo)} apariciones): {desc}", flush=True)
        continue
    f.write_text(texto.replace(viejo, nuevo), encoding="utf-8")
    try:
        if mid == "N05":
            pasa, ultima, salida = pytest(ADAPTADAS, ejec, x=False)
            fallan = [x.split("::")[-1] for x in salida.splitlines() if x.startswith("FAILED")]
            print(f"{mid} {'vivo' if pasa else 'muerto'}: {desc} · {ultima} · fallan: {fallan}", flush=True)
            if pasa:
                vivos.append(mid)
            continue
        pasa, ultima, _ = pytest(PRUEBAS, ejec)
        por = "pruebas del ticket"
        if pasa:
            pasa, ultima, _ = pytest(ATAQUES, ejec)
            por = "r01_01 del revisor"
        if pasa:
            vivos.append(mid)
        eq = f" [equivalente: {EQUIVALENTES[mid]}]" if mid in EQUIVALENTES else ""
        print(f"{mid} {'vivo' if pasa else 'muerto (' + por + ')'}{eq}: {desc} · {ultima}", flush=True)
    finally:
        f.write_text(texto, encoding="utf-8")
print(f"\n{len(MUTANTES)} mutantes · vivos {vivos} · no aplican {no_aplica}")
sys.exit(1 if no_aplica else 0)
