"""QA r01 de T-143 · Mutantes: ¿fallan las pruebas si el Anexo B V5.2 y el código vuelven a diferir?

Desde la raíz del repositorio, con el Python del .venv:

    .venv/bin/python .docs/tickets/T-143/revisores/r01_03_mutantes.py DESTINO [ID ...]

DESTINO es una carpeta vacía fuera del repositorio. El script copia allí el árbol (sin .git, .venv ni cachés) y, para cada
mutante, restaura la copia, aplica un único cambio de texto (en el código o en el Anexo B V5.2) y hace lo que haría quien no
mira: re-congela con `goldens_ct.py --update --motivo` (así la huella del Documento 0 y los goldens generados ya no protegen)
y pasa `tests/test_fase3_goldens.py`. Un mutante MUERE si alguna prueba falla después del re-congelado; SOBREVIVE si todas
pasan. Sin re-congelar, cualquier cambio del Documento 0 o de lo que el ejecutor emite falla ya por las huellas y por la
comparación byte a byte; lo que se mide aquí es si las pruebas de T-143 entienden la diferencia.

`esperado` es lo que el revisor espera: "muere" para una diferencia que las pruebas de T-143 dicen cubrir; "?" para las que
nadie dice cubrir. Termina con 1 si algún mutante con `esperado` "muere" sobrevive. No usa red. Cada mutante tarda unos 3 min.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
PY = str(RAIZ / ".venv" / "bin" / "python")
DOC0 = "bloque_a/01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.2.md"
CONTRATOS = "bloque_a/11_Ejecutor/bloque_a/contratos.py"
ORQ = "bloque_a/11_Ejecutor/bloque_a/orquestacion.py"
SEG = "bloque_a/11_Ejecutor/bloque_a/seguimiento.py"
MOTOR = "bloque_a/11_Ejecutor/bloque_a/motor/servicio.py"

# (id, fichero, texto viejo, texto nuevo, esperado, qué representa)
MUTANTES = [
    # ---- en el código
    ("C01", CONTRATOS, '"CURACION": {\n        "type": "object", "required": ["piezas"],',
     '"CURACION": {\n        "type": "object", "required": ["piezas", "evd_id"],', "muere",
     "CURACION exige un campo nuevo (el Anexo B dice que solo exige `piezas`)"),
    ("C02", CONTRATOS, '"veredicto_global": {"enum": ["tesis robusta", "tesis frágil", "tesis refutada"]}',
     '"veredicto_global": {"enum": ["tesis robusta", "tesis frágil", "tesis refutada", "tesis dudosa"]}', "?",
     "REFUTACION admite un veredicto que el Anexo B no nombra"),
    ("C03", CONTRATOS, '"CT-25": ("PROVISTA", "DENEGADA", "APLAZADA")}', '"CT-25": ("PROVISTA", "DENEGADA", "APLAZADA", "CADUCADA")}', "muere",
     "estado propio de CT-25 con un valor nuevo"),
    ("C04", ORQ, 'for k in ("afirmacion", "fuente", "direccion", "extracto")}', 'for k in ("afirmacion", "fuente", "direccion")}', "muere",
     "CT-11: las piezas dejan de llevar `extracto`"),
    ("C05", SEG, '{"tipo_aviso": "DECISION_SEGUIMIENTO", "seg_id": seg_id,', '{"tipo": "DECISION_SEGUIMIENTO", "seg_id": seg_id,', "muere",
     "CT-22: DECISION_SEGUIMIENTO vuelve a `tipo`"),
    ("C06", MOTOR, '"informe_calidad_datos": efectivos, "cache_hit": False}',
     '"informe_calidad_datos": efectivos, "cache_hit": False, "incertidumbre": None}', "muere",
     "CT-09: el Motor devuelve una clave más"),
    ("C07", ORQ, 'msg = {"clase": clase, "tipo_activo": clase, "fase": fase,',
     'msg = {"clase": clase, "tipo_activo": clase, "fase": "PROFUNDIZACION" if fase == "REVISION_VIGENTES" else fase,', "?",
     "CT-06: en N0/N1 se emite PROFUNDIZACION en vez de REVISION_VIGENTES (el Anexo B dice cuándo se emite cada fase)"),
    ("C08", ORQ, '"objeciones": o["objeciones"], "riesgo_1a5": o["riesgo_1a5"], "relevancia_decisional"',
     '"objeciones": o["objeciones"], "relevancia_decisional"', "muere", "CT-17: las opciones dejan de llevar `riesgo_1a5`"),
    ("C09", CONTRATOS, '"CT-03": ["pregunta"],', '"CT-03": ["pregunta", "urgencia"],', "?",
     "la mensajería pasa a exigir `urgencia` de CT-03, que el Anexo B marca opcional"),
    ("C10", ORQ, '"umbral_senal_gc1": (v6.umbral_gc1', '"lecciones_x": 1, "umbral_senal_gc1": (v6.umbral_gc1', "?",
     "CT-06: un campo de más en el encargo (el Anexo B lo admite: 6.2.3)"),
    # ---- en el Anexo B V5.2
    ("D01", DOC0, "con `CURACION`, que exige `piezas`.", "con `CURACION`, que exige `piezas` y `alertas`.", "muere",
     "el Anexo B dice que CURACION exige un campo que no exige"),
    ("D02", DOC0, '"estado_consulta":"RESPONDIDA|PARCIAL|VENCIDA|RECIBIDA"', '"estado_consulta":"RESPONDIDA|PARCIAL|VENCIDA"', "muere",
     "el Anexo B quita RECIBIDA del estado propio de CT-23"),
    ("D03", DOC0, "Son opcionales `nivel_forzado`, `fecha_objetivo` y `referencia_previa`. ", "", "?",
     "el Anexo B deja de decir que tres campos de CT-01 son opcionales (pasan a ser obligatorios)"),
    ("D04", DOC0, "En la solicitud, `herramienta` y `urgencia` son opcionales", "En la solicitud, `herramienta` es opcional", "?",
     "el Anexo B pasa a exigir `urgencia` de CT-25"),
    ("D05", DOC0, "SEGUIMIENTO | CRIBADO_E_INVESTIGACION | REVISION_VIGENTES | RESPUESTA_OBJECIONES)",
     "SEGUIMIENTO | CRIBADO_E_INVESTIGACION | RESPUESTA_OBJECIONES)", "?", "el Anexo B quita REVISION_VIGENTES de la lista de fases de CT-06"),
    ("D06", DOC0, "`fuerza` (fuerte | moderada | debil), `argumento`, `que_la_resolveria`}]",
     "`fuerza` (fuerte | moderada | debil), `argumento`, `evidencia`, `que_la_resolveria`}]", "?",
     "el Anexo B vuelve a poner `evidencia` en cada objeción de CT-13"),
    ("D07", DOC0, "`informe_calidad_datos` (los datos efectivos) y `cache_hit`;", "`informe_calidad_datos` (los datos efectivos);", "muere",
     "el Anexo B deja de nombrar `cache_hit` de CT-09"),
    ("D08", DOC0, "o `tipo_aviso` (CONSULTA_RECURRENTE o DECISION_SEGUIMIENTO)", "o `tipo` (CONSULTA_RECURRENTE o DECISION_SEGUIMIENTO)", "muere",
     "el Anexo B vuelve a poner los cuatro valores de CT-22 en `tipo`"),
    ("D09", DOC0, "`dictamen` es APTO_CON_ADVERTENCIAS o BLOQUEADO", "`dictamen` es APTO, APTO_CON_ADVERTENCIAS o BLOQUEADO", "?",
     "el Anexo B admite APTO en el dictamen del Orquestador"),
    ("D10", DOC0, "`clase_cifra` (DETERMINISTA | ESTADISTICA)", "`clase_cifra` (DETERMINISTA | ESTADISTICA | MIXTA)", "?",
     "el Anexo B nombra un valor de `clase_cifra` que el Motor no da (prosa, sin que cambie el esquema derivado)"),
]

IGNORAR = shutil.ignore_patterns(".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "estado_bloque_a",
                                 "entregables", ".logs")


def ejecutar(args: list[str], cwd: Path, limite: int = 1800) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=limite, check=False)


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    destino = Path(argv[0]).resolve()
    if RAIZ in destino.parents or destino == RAIZ:
        print("DESTINO debe estar fuera del repositorio")
        return 2
    elegidos = set(argv[1:])
    copia = destino / "arbol"
    if not copia.exists():
        shutil.copytree(RAIZ, copia, ignore=IGNORAR, symlinks=True)
    originales = {f: (copia / f).read_text(encoding="utf-8") for f in {m[1] for m in MUTANTES} | {
        "bloque_a/11_Ejecutor/tests/goldens/REGISTRO.md"}}
    goldens = copia / "bloque_a/11_Ejecutor/tests/goldens"
    respaldo = destino / "goldens_original"
    if not respaldo.exists():
        shutil.copytree(goldens, respaldo)
    malos = []
    for ident, fichero, viejo, nuevo, esperado, que in MUTANTES:
        if elegidos and ident not in elegidos:
            continue
        for f, t in originales.items():
            (copia / f).write_text(t, encoding="utf-8")
        shutil.rmtree(goldens)
        shutil.copytree(respaldo, goldens)
        texto = originales[fichero]
        if texto.count(viejo) != 1:
            print(f"{ident} · NO APLICA (el texto aparece {texto.count(viejo)} veces) · {que}")
            malos.append(ident)
            continue
        (copia / fichero).write_text(texto.replace(viejo, nuevo), encoding="utf-8")
        t0 = time.time()
        ejecutor = copia / "bloque_a/11_Ejecutor"
        up = ejecutar([PY, "tests/goldens_ct.py", "--update", "--motivo", f"mutante {ident} del revisor"], ejecutor)
        if up.returncode != 0:
            print(f"{ident} · MUERE al re-congelar (rc {up.returncode}: {(up.stderr or up.stdout).strip().splitlines()[-1][:160]}) · {que}")
            continue
        pr = ejecutar([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/test_fase3_goldens.py"], ejecutor)
        fallos = [l.split(" ", 1)[1].split(" - ")[0] for l in pr.stdout.splitlines() if l.startswith("FAILED ")]
        estado = "MUERE" if pr.returncode != 0 else "SOBREVIVE"
        print(f"{ident} · {estado} ({time.time() - t0:.0f} s; {up.stdout.strip()[:120]}) · {que}"
              + (f"\n      fallan: {', '.join(f.split('::')[-1] for f in fallos[:6])}" if fallos else ""))
        if estado == "SOBREVIVE" and esperado == "muere":
            malos.append(ident)
    for f, t in originales.items():
        (copia / f).write_text(t, encoding="utf-8")
    print(f"\nmutantes que debían morir y sobreviven o no aplican: {malos or 'ninguno'}")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
