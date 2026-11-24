"""T-194 · mutantes de `.docs/scripts/cola_astra.py`: cada uno quita o tuerce una comprobación y alguna prueba de
`.docs/scripts/pruebas_cola_astra.py` tiene que fallar.

Uso, desde la raíz:  .venv/bin/python .docs/tickets/T-194/mutantes.py [--solo M01,M02]
Cada mutante se escribe en una carpeta temporal (el script original no se toca) y las pruebas lo copian a su
repositorio de prueba por `COLA_ASTRA_SCRIPT`. Vivo = ninguna prueba lo detecta. Termina con 1 si un mutante no aplica
o vive.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
ORIGINAL = RAIZ / ".docs/scripts/cola_astra.py"
PRUEBAS = RAIZ / ".docs/scripts/pruebas_cola_astra.py"
SOLO = set(sys.argv[sys.argv.index("--solo") + 1].split(",")) if "--solo" in sys.argv else None

MUTANTES = [
    # Las comprobaciones de siempre
    ("M01", "HECHA sin entregable no da error", 'if f["estado"] == "HECHA" and not hecha:', 'if False:'),
    ("M02", "un entregable que no existe cuenta", 'if not f["entregable"] or not p.exists():', 'if not f["entregable"]:'),
    ("M03", "el borrador cuenta", 'if texto.lstrip().upper().startswith("BORRADOR"):', 'if False:'),
    ("M04", "el borrador solo en mayúsculas", 'if texto.lstrip().upper().startswith("BORRADOR"):',
     'if texto.lstrip().startswith("BORRADOR"):'),
    ("M05", "un entregable fuera de git cuenta", 'if not git("ls-files", "--error-unmatch", f["entregable"]):', 'if False:'),
    ("M06", "entregable sin marcar no avisa", 'if hecha and f["estado"] not in ("HECHA", "RETIRADA"):', 'if False:'),
    ("M07", "RETIRADA con entregable avisa", 'if hecha and f["estado"] not in ("HECHA", "RETIRADA"):',
     'if hecha and f["estado"] != "HECHA":'),
    ("M08", "sin la sección del rediseño", 'REQUISITOS = {"C-02": "Rediseño"}', 'REQUISITOS = {}'),
    ("M09", "la sección del rediseño en otra fila", 'REQUISITOS = {"C-02": "Rediseño"}', 'REQUISITOS = {"C-03": "Rediseño"}'),
    ("M10", "la sección no se busca", '        if req and req not in texto:', '        if False:'),
    ("M11", "EN CURSO viejo no avisa", 'elif date.fromisoformat(m.group(0)) < hoy - timedelta(days=DIAS_EN_CURSO):',
     'elif False:'),
    ("M12", "EN CURSO: el día 3 ya es viejo", 'elif date.fromisoformat(m.group(0)) < hoy - timedelta(days=DIAS_EN_CURSO):',
     'elif date.fromisoformat(m.group(0)) <= hoy - timedelta(days=DIAS_EN_CURSO):'),
    ("M13", "EN CURSO: 30 días", "DIAS_EN_CURSO = 3", "DIAS_EN_CURSO = 30"),
    ("M14", "EN CURSO sin fecha no avisa", '                avisos.append(f"{f[\'id\']}: EN CURSO sin fecha")',
     '                pass'),
    ("M15", "la siguiente no es la EN CURSO", 'siguiente = next((f for f in resumen if f["estado"].startswith("EN CURSO")), None) or \\',
     'siguiente = None or \\'),
    ("M16", "dos EN CURSO no avisa", "    if len(en_curso) > 1:", "    if len(en_curso) > 2:"),
    ("M17", "cambios sin commit no avisa", '        if f["entregable"] in sin_subir:', '        if False:'),
    ("M18", "cambios sin commit: recorta la primera columna", "sin_subir = {l[3:] for l in st.splitlines() if len(l) > 3}",
     "sin_subir = {l.strip()[3:] for l in st.splitlines() if len(l) > 3}"),
    ("M19", "QA anterior a la cola cuenta", "    if fecha and fecha < FECHA_COLA:", "    if False:"),
    ("M20", "QA del día de la cola no cuenta", "    if fecha and fecha < FECHA_COLA:", "    if fecha and fecha <= FECHA_COLA:"),
    ("M21", "QA sin veredicto cuenta", '        return (True, "", commit) if v else (False, "sin veredicto rellenado", commit)',
     '        return (True, "", commit)'),
    ("M22", "QA: la plantilla cuenta como veredicto", ' and "APTO / NO APTO" not in trozos[-1][:200]', ''),
    ("M23", "QA: el primer veredicto, no el último", "trozos[-1])\n", "trozos[1])\n"),
    ("M24", "QA: sin la sección del veredicto", "    if len(trozos) < 2:\n        return None", "    if False:\n        return None"),
    ("M25", "IMPLEMENTAR: cualquier estado cuenta", 'if est.startswith(("EN QA", "CERRADO"))', 'if True'),
    ("M26", "IMPLEMENTAR: CERRADO no cuenta", 'if est.startswith(("EN QA", "CERRADO"))', 'if est.startswith("EN QA")'),
    ("M27", "RETIRADA es la siguiente", 'next((f for f in resumen if f["estado"] == "PENDIENTE"), None)',
     'next((f for f in resumen if f["estado"] in ("PENDIENTE", "RETIRADA")), None)'),
    ("M28", "RETIRADA no se cuenta", '("HECHA", "EN CURSO", "PENDIENTE", "BLOQUEADA", "RETIRADA")}',
     '("HECHA", "EN CURSO", "PENDIENTE", "BLOQUEADA")} | {"RETIRADA": 0}'),
    ("M29", "estado desconocido no avisa", '        if not ESTADOS.match(f["estado"]):', '        if False:'),
    ("M30", "estado desconocido: vale cualquier EN CURSO", r'EN CURSO( \d{4}-\d{2}-\d{2})?)$', r'EN CURSO.*)$'),
    ("M31", "estado desconocido: RETIRADA desconocida", "BLOQUEADA|RETIRADA|EN CURSO", "BLOQUEADA|EN CURSO"),
    ("M32", "fila rota no da error", '            errores.append(f"{f[\'id\']}: {f[\'error_forma\']}")\n', ''),
    ("M33", "«…» no es una ruta", 're.findall(r"`([^`]+)`|«([^»]+)»", c[4])', 're.findall(r"`([^`]+)`|`([^»]+)»", c[4])'),
    ("M34", "--json sin errores", '"errores": errores, "avisos": avisos}', '"errores": [], "avisos": avisos}'),
    ("M35", "con errores devuelve 0", "    return 1 if errores else 0", "    return 0"),
    # Autor genérico
    ("M36", "sin comprobar el autor", "    if autor not in AUTORES_GENERICOS:", "    if False:"),
    ("M37", "el autor por el nombre solo", "    if autor not in AUTORES_GENERICOS:",
     '    if autor.split(" <")[0] not in ("Astra", "Claude"):'),
    ("M38", "el autor sin leer .env", '    if env.is_file():', '    if False:'),
    ("M39", "el .env manda sobre el entorno", '            if k in valores and not valores[k]:', '            if k in valores:'),
    ("M40", "el autor sin el git config", 'nombre = valores["GIT_AUTOR_NOMBRE"] or git("config", "user.name")',
     'nombre = valores["GIT_AUTOR_NOMBRE"] or "Claude"'),
    # r01b: INC-T194-01
    ("M42", "cambios sin commit: sin los ficheros de una carpeta nueva", ', "--untracked-files=all"]', ']'),
    # r02: QA r01 (los R del revisor y H-07)
    ("M43", "R01 · IMPLEMENTAR: un README anterior a la cola cuenta",
     '    if fecha and fecha < FECHA_COLA:', '    if f["tipo"] == "QA" and fecha and fecha < FECHA_COLA:'),
    ("M44", "R02 · tipo desconocido cuenta como hecho",
     '    return False, f"tipo desconocido «{f[\'tipo\']}»", commit', '    return True, "", commit'),
    ("M45", "R04 · la fecha de la cola también para REVISION",
     '    if f["tipo"] == "REVISION":\n        if texto',
     '    if f["tipo"] == "REVISION" and not (fecha and fecha < FECHA_COLA):\n        if texto'),
    ("M46", "R06 · el estado del ticket en cualquier parte del README",
     r'm = re.search(r"^\| Estado \| ([^|]+)\|", texto, re.MULTILINE)', r'm = re.search(r"\| Estado \| ([^|]+)\|", texto)'),
    ("M47", "R09 · la fila rota en el texto pero no en --json", "    if len(en_curso) > 1:",
     ("    errores[:] = [e for e in errores if 'columnas' not in e] if '--json' in sys.argv else errores\n"
     "    if len(en_curso) > 1:")),
    ("M49", "R03 · el .env sin quitar las comillas",
     "valores[k] = v.strip().strip('\"').strip(\"'\")", "valores[k] = v.strip()"),
    ("M48", "H-07 · rutas no ASCII entrecomilladas", '"-c", "core.quotePath=false", ', ''),
    ("M41", "el error repite el autor", 'errores.append("autor de los commits no genérico (repositorio público',
     'errores.append(autor + "autor de los commits no genérico (repositorio público'),
]
EQUIVALENTES: dict[str, str] = {}


def main() -> int:
    fuente = ORIGINAL.read_text(encoding="utf-8")
    malos = []
    with tempfile.TemporaryDirectory() as tmp:
        for mid, desc, viejo, nuevo in MUTANTES:
            if SOLO and mid not in SOLO:
                continue
            if fuente.count(viejo) != 1:
                print(f"{mid} NO APLICA ({fuente.count(viejo)} apariciones): {desc}")
                malos.append(mid)
                continue
            mut = Path(tmp) / f"{mid}.py"
            mut.write_text(fuente.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", str(PRUEBAS)],
                               env={**os.environ, "COLA_ASTRA_SCRIPT": str(mut)}, capture_output=True, text=True,
                               check=False, cwd=RAIZ)
            vivo = r.returncode == 0
            estado = "VIVO (equivalente)" if vivo and mid in EQUIVALENTES else ("VIVO" if vivo else "muerto")
            print(f"{mid} {estado}: {desc}", flush=True)
            if vivo and mid not in EQUIVALENTES:
                malos.append(mid)
    print(f"{len(malos)} vivos o sin aplicar: {malos}" if malos else "todos muertos")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
