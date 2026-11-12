"""QA r01 de T-103 (revisor independiente): mutantes contra `tests/test_t103_r8_y_bajos.py` (método de T-93 r01_04).

Uso: python -I r01_04_mutantes.py <ruta a bloque_a/11_Ejecutor de una copia DESECHABLE (worktree temporal en 33385c9)>
Cada mutante cambia un fragmento de las correcciones de T-103, ejecuta la batería nueva y restaura el fichero. Un mutante «muere»
si alguna prueba falla. Si sobrevive a la batería nueva, se mira además si lo mata `test_t93_hallazgos.py` + `test_t92_revision.py`
(cobertura heredada). Los marcados «equivalente» o «refuerzo» no tienen por qué morir. FALLO = mutante no equivalente que
sobrevive a la batería nueva Y a la heredada.
"""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
assert (EJ / "tests" / "test_t103_r8_y_bajos.py").exists(), EJ
assert "/home/user/robotinvestor/bloque_a" not in str(EJ), "usar una copia desechable, no el repositorio de trabajo"

ESC = r'RE_ESCAPES = re.compile(r"\\+(?:u[0-9a-fA-F]{4}|U[0-9a-fA-F]{8}|x[0-9a-fA-F]{2}|[0-7]{1,3}|[ntrbf/\"])"'
M = [
    # (nombre, fichero, original, mutado, clase)  clase: "" normal, "equivalente", "refuerzo"
    # sin «+» la última barra del tramo y su letra se sustituyen igual: delante de «sk-» queda un espacio (equivalente, y lineal)
    ("H-40 barra única sin «+» (equivalente)", "contratos.py", ESC, ESC.replace(r'r"\\+(?:', r'r"\\(?:'), "equivalente"),
    # la expresión real de T-93: la alternativa «\\\\» consume la barra escapada y deja la «n» pegada (la causa de H-40)
    ("H-40 vuelve la alternativa «\\\\» de T-93", "contratos.py", ESC,
     ESC.replace(r'r"\\+(?:', r'r"\\(?:').replace('[ntrbf/\\"]', '[ntrbf/\\"\\\\]'), ""),
    ("H-40 sin \\UXXXXXXXX", "contratos.py", ESC, ESC.replace("|U[0-9a-fA-F]{8}", ""), ""),
    ("H-40 sin \\xNN", "contratos.py", ESC, ESC.replace("|x[0-9a-fA-F]{2}", ""), ""),
    ("H-40 sin octales", "contratos.py", ESC, ESC.replace("|[0-7]{1,3}", ""), ""),
    ("H-40 sin \\b ni \\f", "contratos.py", ESC, ESC.replace("[ntrbf/", "[ntr/"), ""),
    ("H-40 sin \\uXXXX", "contratos.py", ESC, ESC.replace("(?:u[0-9a-fA-F]{4}|", "(?:"), ""),
    ("H-40 sin %25 repetido", "contratos.py", r'r"|%(?:25)*(?:', r'r"|%(?:', ""),
    ("H-40 sin %uXXXX", "contratos.py", r'%(?:25)*(?:u[0-9A-Fa-f]{4}|[0-9A-Fa-f]{2})', r'%(?:25)*(?:[0-9A-Fa-f]{2})', ""),
    ("H-40 variante lineal propuesta (equivalente)", "contratos.py", ESC, ESC.replace(r'r"\\+(?:', r'r"(?<!\\)\\++(?:'),
     "equivalente"),
    ("H-41 sin la regla", "contratos.py", "    if len(tramos) >= 4 and all(t.isdigit() for t in tramos):",
     "    if False:", ""),
    ("H-41 desde 5 tramos", "contratos.py", "len(tramos) >= 4 and all(", "len(tramos) >= 5 and all(", ""),
    ("H-41 desde 3 tramos (refuerzo: ve también 3×5..3×7)", "contratos.py", "len(tramos) >= 4 and all(",
     "len(tramos) >= 3 and all(", "refuerzo"),
    ("H-41 «any» en vez de «all»", "contratos.py", "and all(t.isdigit() for t in tramos)", "and any(t.isdigit() for t in tramos)", ""),
    ("H-44 sin frozenset", "contratos.py", "(list, tuple, set, frozenset)):   # T-103", "(list, tuple, set)):   # T-103", ""),
    ("H-42 nunca antepone", "almacen.py", 'sep = b"" if lec.read(1) == b"\\n" else b"\\n"', 'sep = b""', ""),
    ("H-42 siempre antepone", "almacen.py", 'sep = b"" if lec.read(1) == b"\\n" else b"\\n"', 'sep = b"\\n"', ""),
    ("H-42 sin mirar si el fichero está vacío", "almacen.py", "                if inicio:\n", "                if False:\n", ""),
    ("H-42 mira el primer byte", "almacen.py", "lec.seek(-1, os.SEEK_END)", "lec.seek(0)", ""),
    ("H-43 vuelve a c[...]", "interfaz_broker.py", 'self._instante(c.get("plazo_respuesta"), plazo=True)',
     'self._instante(c["plazo_respuesta"], plazo=True)', ""),
]


def pytest(*ficheros):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *ficheros], cwd=EJ, capture_output=True,
                       text=True, env={"PYTHONPATH": str(EJ), "PATH": "/usr/bin:/bin"})
    return r.returncode != 0, (r.stdout.strip().splitlines() or [""])[-1]


limpio, ult = pytest("tests/test_t103_r8_y_bajos.py")
assert not limpio, f"la batería no pasa sin mutar: {ult}"
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
