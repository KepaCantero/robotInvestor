"""QA r02 de T-103 (revisor independiente): mutantes de las correcciones de T-103 (r01 y r02) sobre el código de 7feb697.

Uso: python -I r02_04_mutantes.py <ruta a bloque_a/11_Ejecutor de una copia DESECHABLE (worktree temporal en 7feb697)>

Es `r01_04_mutantes.py` con los fragmentos de la r02 (el `r01_04` ya no encuentra el texto original de `RE_ESCAPES` ni de la
regla de cifras, que cambiaron en 7feb697) y con los mutantes de la r02: el lookbehind, el posesivo, cada uno de los tres
lectores de JSONL y la regla de tres tramos. Cada mutante cambia un fragmento, ejecuta `tests/test_t103_r8_y_bajos.py` y
restaura el fichero. Si sobrevive, se mira la batería heredada (`test_t93_hallazgos.py` + `test_t92_revision.py`). Un mutante
que tarda más de TOPE_S se cuenta como muerto por tiempo (la prueba de H-47 tiene un límite de 2 s). FALLO = mutante no
equivalente que sobrevive a las dos baterías.
"""
import subprocess
import sys
import time
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
assert (EJ / "tests" / "test_t103_r8_y_bajos.py").exists(), EJ
assert "/home/user/robotinvestor/bloque_a" not in str(EJ), "usar una copia desechable, no el repositorio de trabajo"
TOPE_S = 900

ESC = r'RE_ESCAPES = re.compile(r"(?<!\\)\\++(?:u[0-9a-fA-F]{4}|U[0-9a-fA-F]{8}|x[0-9a-fA-F]{2}|[0-7]{1,3}|[ntrbf/\"])"'
REGLA = "    if len(tramos) >= 3 and all(t.isdigit() for t in tramos):"
SPLIT_A = 'lineas = texto.split("\\n")'
SPLIT_L = 'for l in self.ruta.read_text(encoding="utf-8").split("\\n"):'
SPLIT_C = 'for linea in self.ruta.read_text(encoding="utf-8").split("\\n"):'
M = [
    # (nombre, fichero, original, mutado, clase)  clase: "" normal, "equivalente", "refuerzo"
    # --- r02, H-47
    ("H-47 sin lookbehind (posesivo solo)", "contratos.py", ESC, ESC.replace(r'r"(?<!\\)\\++(?:', r'r"\\++(?:'), ""),
    ("H-47 sin posesivo (lookbehind solo: lineal, equivalente)", "contratos.py", ESC,
     ESC.replace(r'r"(?<!\\)\\++(?:', r'r"(?<!\\)\\+(?:'), "equivalente"),
    ("H-47 vuelve la r01 (ni lookbehind ni posesivo)", "contratos.py", ESC, ESC.replace(r'r"(?<!\\)\\++(?:', r'r"\\+(?:'), ""),
    ("H-47 una sola barra posesiva (equivalente en la sustitución)", "contratos.py", ESC,
     ESC.replace(r'r"(?<!\\)\\++(?:', r'r"\\(?:'), "equivalente"),
    # --- r01, H-40 (sobre la expresión de la r02)
    ("H-40 vuelve la alternativa «\\\\» de T-93", "contratos.py", ESC,
     ESC.replace(r'r"(?<!\\)\\++(?:', r'r"\\(?:').replace('[ntrbf/\\"]', '[ntrbf/\\"\\\\]'), ""),
    ("H-40 sin \\UXXXXXXXX", "contratos.py", ESC, ESC.replace("|U[0-9a-fA-F]{8}", ""), ""),
    ("H-40 sin \\xNN", "contratos.py", ESC, ESC.replace("|x[0-9a-fA-F]{2}", ""), ""),
    ("H-40 sin octales", "contratos.py", ESC, ESC.replace("|[0-7]{1,3}", ""), ""),
    ("H-40 sin \\b ni \\f", "contratos.py", ESC, ESC.replace("[ntrbf/", "[ntr/"), ""),
    ("H-40 sin \\uXXXX", "contratos.py", ESC, ESC.replace("(?:u[0-9a-fA-F]{4}|", "(?:"), ""),
    ("H-40 sin %25 repetido", "contratos.py", r'r"|%(?:25)*(?:', r'r"|%(?:', ""),
    ("H-40 sin %uXXXX", "contratos.py", r'%(?:25)*(?:u[0-9A-Fa-f]{4}|[0-9A-Fa-f]{2})', r'%(?:25)*(?:[0-9A-Fa-f]{2})', ""),
    # --- H-41 / H-50
    ("H-50 sin la regla", "contratos.py", REGLA, "    if False:", ""),
    ("H-50 vuelve a 4 tramos (r01)", "contratos.py", REGLA, REGLA.replace(">= 3", ">= 4"), ""),
    ("H-50 desde 2 tramos (casi equivalente: 2 tramos de ≤ 8 cifras no llegan a 20)", "contratos.py", REGLA,
     REGLA.replace(">= 3", ">= 2"), "refuerzo"),
    ("H-50 «any» en vez de «all»", "contratos.py", REGLA, REGLA.replace("and all(", "and any("), ""),
    # --- H-44 / H-49
    ("H-49 sin frozenset", "contratos.py", "(list, tuple, set, frozenset)):   # T-103", "(list, tuple, set)):   # T-103", ""),
    # --- H-48: los tres lectores
    ("H-48 almacén vuelve a splitlines", "almacen.py", SPLIT_A, "lineas = texto.splitlines()", ""),
    ("H-48 cinta vuelve a splitlines", "llm.py", SPLIT_L, SPLIT_L.replace('.split("\\n")', ".splitlines()"), ""),
    ("H-48 caché vuelve a splitlines", "herramientas/ht06_indice.py", SPLIT_C, SPLIT_C.replace('.split("\\n")', ".splitlines()"), ""),
    ("H-48 almacén parte por «\\r\\n» (rompe los LF)", "almacen.py", SPLIT_A, 'lineas = texto.split("\\r\\n")', ""),
    # --- H-42 y H-43 (r01)
    ("H-42 nunca antepone", "almacen.py", 'sep = b"" if lec.read(1) == b"\\n" else b"\\n"', 'sep = b""', ""),
    ("H-42 siempre antepone", "almacen.py", 'sep = b"" if lec.read(1) == b"\\n" else b"\\n"', 'sep = b"\\n"', ""),
    ("H-42 sin mirar si el fichero está vacío", "almacen.py", "                if inicio:\n", "                if False:\n", ""),
    ("H-42 mira el primer byte", "almacen.py", "lec.seek(-1, os.SEEK_END)", "lec.seek(0)", ""),
    ("H-43 vuelve a c[...]", "interfaz_broker.py", 'self._instante(c.get("plazo_respuesta"), plazo=True)',
     'self._instante(c["plazo_respuesta"], plazo=True)', ""),
]


def pytest(*ficheros):
    t0 = time.perf_counter()
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *ficheros], cwd=EJ,
                           capture_output=True, text=True, env={"PYTHONPATH": str(EJ), "PATH": "/usr/bin:/bin"}, timeout=TOPE_S)
    except subprocess.TimeoutExpired:
        return True, f"más de {TOPE_S} s (muerto por tiempo)"
    return r.returncode != 0, f"{(r.stdout.strip().splitlines() or [''])[-1]} [{time.perf_counter() - t0:.1f} s]"


limpio, ult = pytest("tests/test_t103_r8_y_bajos.py")
assert not limpio, f"la batería no pasa sin mutar: {ult}"
print(f"INFO  sin mutar: {ult}")
fallos = 0
for nombre, fichero, original, mutado, clase in M:
    ruta = EJ / "bloque_a" / fichero
    texto = ruta.read_text(encoding="utf-8")
    if texto.count(original) != 1 or original == mutado:
        print(f"FALLO {nombre}: el texto original aparece {texto.count(original)} veces en {fichero}")
        fallos += 1
        continue
    ruta.write_text(texto.replace(original, mutado), encoding="utf-8")
    try:
        muere, ultima = pytest("tests/test_t103_r8_y_bajos.py")
        heredada = None
        if not muere and not clase:
            heredada, _ = pytest("tests/test_t93_hallazgos.py", "tests/test_t92_revision.py")
    finally:
        ruta.write_text(texto, encoding="utf-8")
    if clase:
        print(f"INFO  {nombre}: {'muere' if muere else 'sobrevive'} ({clase}) — {ultima}")
    elif muere:
        print(f"OK    {nombre}: muere — {ultima}")
    else:
        fallos += 0 if heredada else 1
        print(f"{'INFO ' if heredada else 'FALLO'} {nombre}: SOBREVIVE a test_t103 — "
              f"{'lo mata la batería heredada (T-92/T-93)' if heredada else 'tampoco lo mata la heredada'}")
print(f"fallos: {fallos}")
sys.exit(1 if fallos else 0)
