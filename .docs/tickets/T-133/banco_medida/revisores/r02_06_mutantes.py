"""T-133 QA r02 · Mutantes del revisor sobre lo que cambió el banco 0.5.0 (r02 H-01 a H-09).

Modifica `.docs/scripts/banco_medida.py` SOLO en el worktree que se le pasa (se niega a tocar el árbol principal), ejecuta
`pruebas_banco_medida.py` con cada mutante y restaura el original al terminar, también si se interrumpe.
Uso: .venv/bin/python -B r02_06_mutantes.py <worktree>"""
import subprocess
import sys
from pathlib import Path

ARBOL_PRINCIPAL = Path(__file__).resolve().parents[5]
if len(sys.argv) < 2:
    sys.exit("uso: r02_06_mutantes.py <worktree>")
W = Path(sys.argv[1]).resolve()
if W == ARBOL_PRINCIPAL:
    sys.exit("me niego a mutar el árbol principal: pásame un worktree")
F = W / ".docs" / "scripts" / "banco_medida.py"
ORIGINAL = F.read_text(encoding="utf-8")

MUTANTES = {
    # H-01: la fuente y la huella
    "R01 la fuente vuelve a llevar las huellas (datos cambiados = otro experimento)": (
        '"fuente": f"cliente {a.cliente}",', '"fuente": f"cliente {a.cliente}, datos {huella_d[:16]}, universo {huella_u[:16]}",'),
    "R02 la huella de los datos sin los símbolos del universo (todos los CSV)": (
        "huella_d = huella_datos(datos_ruta, _simbolos_del_universo(universo_ruta))", "huella_d = huella_datos(datos_ruta)"),
    "R03 la huella del universo sin la clase": ('h.update(unicodedata.normalize("NFC", f"{sim}\\t{clase}\\n").encode("utf-8"))',
                                                'h.update(unicodedata.normalize("NFC", f"{sim}\\n").encode("utf-8"))'),
    "R04 la huella del universo con el nombre del fichero": (
        "        for sim, clase in sorted(zip(u[\"simbolo\"], u[\"clase\"])):",
        "        h.update(ruta.name.encode())\n        for sim, clase in sorted(zip(u[\"simbolo\"], u[\"clase\"])):"),
    "R05 la huella del universo sin ordenar las filas": ('for sim, clase in sorted(zip(u["simbolo"], u["clase"])):',
                                                       'for sim, clase in zip(u["simbolo"], u["clase"]):'),
    "R06 sin la comprobación durante la ejecución": (
        "if (huella_datos(tit[\"datos\"], universo[\"simbolo\"].tolist()), huella_datos(tit[\"universo\"])) != (huella_d, huella_u):",
        "if False:"),
    "R07 la comprobación durante la ejecución solo de los datos": (
        "if (huella_datos(tit[\"datos\"], universo[\"simbolo\"].tolist()), huella_datos(tit[\"universo\"])) != (huella_d, huella_u):",
        "if huella_datos(tit[\"datos\"], universo[\"simbolo\"].tolist()) != huella_d:"),
    "R08 la comprobación durante la ejecución solo del universo": (
        "if (huella_datos(tit[\"datos\"], universo[\"simbolo\"].tolist()), huella_datos(tit[\"universo\"])) != (huella_d, huella_u):",
        "if huella_datos(tit[\"universo\"]) != huella_u:"),
    "R09 un símbolo del universo sin CSV aceptado en la huella": ("        if faltan:\n            raise BancoError(f\"no hay datos para",
                                                                "        if False:\n            raise BancoError(f\"no hay datos para"),
    "R10 la huella de los datos sin NFC en el nombre": (
        'h.update(unicodedata.normalize("NFC", f.name).encode("utf-8", "backslashreplace") + b"\\0" + _huella_fichero(f))',
        'h.update(f.name.encode("utf-8", "backslashreplace") + b"\\0" + _huella_fichero(f))'),
    # H-02 y H-03: verificar
    "V11 el registro citado vuelve a ser un problema": (
        '            avisos.append("experimento.json cita otro registro que el indicado: se comprueba contra el indicado")',
        '            problemas.append("experimento.json cita otro registro que el indicado: se comprueba contra el indicado")'),
    "V12 sin el aviso del registro citado": (
        '            avisos.append("experimento.json cita otro registro que el indicado: se comprueba contra el indicado")',
        "            pass"),
    "V13 los avisos no se imprimen": ('        for x in avisos:\n            print(f"· aviso: {x}", file=sys.stderr)',
                                      "        for x in avisos:\n            pass"),
    "V14 sin --registro se usa el que cita la carpeta": ("            registro = rx.REGISTRO_DEFECTO", "            registro = citado"),
    # H-05 y H-06: informe y consumo
    "I15 informe.md sin la línea de la plantilla": ('if inf.get("plantilla") else []),', "if False else []),"),
    "I16 una columna ausente vuelve a salir 0": ('return "sin dato" if k in ausentes else t.get(k, defecto)', "return t.get(k, defecto)"),
    "K17 «llamadas» vacía cuenta 0": ('if k in ("llamadas", "tokens_entrada", "tokens_salida") and (f.get(k)',
                                     'if k in ("tokens_entrada", "tokens_salida") and (f.get(k)'),
    "K18 una fila corta (None) en una obligatoria cuenta 0": ("and (f.get(k) is None or not str(f.get(k)).strip()):",
                                                             "and f.get(k) is not None and not str(f.get(k)).strip():"),
    # H-08: nivel y mínimo
    "Q19 nivel mínimo 0,89": ("NIVEL_MIN, NIVEL_MAX = 0.90, 0.99", "NIVEL_MIN, NIVEL_MAX = 0.89, 0.99"),
    "Q20 nivel mínimo 0,85": ("NIVEL_MIN, NIVEL_MAX = 0.90, 0.99", "NIVEL_MIN, NIVEL_MAX = 0.85, 0.99"),
    "Q21 el mínimo escrito a mano (10) en vez de leído de A": ("MIN_EFECTIVAS = _minimo_de_a()", "MIN_EFECTIVAS = 10"),
    "Q22 el mínimo de A sin validar": ("    if isinstance(v, bool) or not isinstance(v, int) or v < 2:", "    if False:"),
    "Q23 el mínimo de un experimento, uno menos que el de A": ("MIN_EFECTIVAS_MIN = MIN_EFECTIVAS", "MIN_EFECTIVAS_MIN = MIN_EFECTIVAS - 1"),
    # H-09
    "H24 la huella lee el fichero entero": ("        for trozo in iter(lambda: fh.read(1 << 20), b\"\"):", "        for trozo in [fh.read()]:"),
}

vivos = []
try:
    for nombre, (viejo, nuevo) in MUTANTES.items():
        n = ORIGINAL.count(viejo)
        if n != 1:
            print(f"SIN PATRÓN ({n})  {nombre}", flush=True)
            vivos.append(nombre + " (sin patrón)")
            continue
        F.write_text(ORIGINAL.replace(viejo, nuevo), encoding="utf-8")
        r = subprocess.run([str(W / ".venv" / "bin" / "python"), "-B", "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider",
                            ".docs/scripts/pruebas_banco_medida.py"], cwd=W, capture_output=True, text=True, timeout=900, check=False)
        muere = r.returncode != 0
        print(("muere " if muere else "VIVE  ") + nombre, flush=True)
        if not muere:
            vivos.append(nombre)
finally:
    F.write_text(ORIGINAL, encoding="utf-8")
estado = subprocess.run(["git", "status", "--short"], cwd=W, capture_output=True, text=True, check=False).stdout
print(f"\n{len(MUTANTES)} mutantes, {len(vivos)} vivos: {vivos}")
print(f"git status del worktree: {estado.strip() or 'vacío'}")
