"""QA r01 de T-93 (revisor independiente): mutantes contra la batería `tests/test_t93_hallazgos.py`.

Uso: python -I r01_04_mutantes.py <ruta a bloque_a/11_Ejecutor de una copia DESECHABLE (worktree temporal)>
Cada mutante cambia una línea del código de T-93, ejecuta la batería y restaura el fichero. Un mutante «muere» si alguna prueba
falla. Los marcados «equivalente» no deberían morir (no cambian lo que se detecta); el resto sí.
Imprime OK/FALLO por mutante y el número de fallos (mutantes que sobreviven sin ser equivalentes).
"""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
assert (EJ / "tests" / "test_t93_hallazgos.py").exists(), EJ
assert "robotinvestor/bloque_a" not in str(EJ), "usar una copia desechable, no el repositorio de trabajo"

M = [
    # (nombre, fichero, original, mutado, equivalente)
    ("R8 sin \\uXXXX", "contratos.py", r'r"\\u[0-9a-fA-F]{4}|', 'r"', False),
    ("R8 sin \\xNN", "contratos.py", r'|\\x[0-9a-fA-F]{2}|', '|', False),
    ("R8 sin %XX", "contratos.py", r'|%[0-9A-Fa-f]{2}")', '")', False),
    ("R8 sin \\b ni \\f", "contratos.py", r'\\[ntr/bf\"\\]', r'\\[ntr/\"\\]', False),
    ("R8 sin \\\" ni \\\\ (equivalente: ni «\"» ni «\\» son letra o cifra)", "contratos.py", r'\\[ntr/bf\"\\]', r'\\[ntr/bf]', True),
    ("R8 sin la segunda variante", "contratos.py", 'for t in {texto, RE_ESCAPES.sub(" ", texto)}:', 'for t in {texto}:', False),
    ("contenido_sensible sin conjuntos", "llm.py", "(list, tuple, set, frozenset)", "(list, tuple)", False),
    ("contenido_sensible sin frozenset", "llm.py", "(list, tuple, set, frozenset)", "(list, tuple, set)", False),
    ("tramos sin códigos de cotización de 5-7 cifras", "contratos.py", "|[0-9]{5,7}", "", False),
    ("tramos sin siglas largas", "contratos.py", "|[A-Z]{1,15}|", "|[A-Z]{1,6}|", False),
    ("tramos sin CamelCase", "contratos.py", r'r"|(?:[A-Z][a-z]{1,14}){2,4}")', '"")', False),
    ("tramos sin periodos en minúsculas", "contratos.py", "|[a-z]{1,2}[0-9]{1,4}|", "|", False),
    ("fecha de 8 cifras sin comprobar que existe", "contratos.py",
     "            date(int(t[:4]), int(t[4:6]), int(t[6:]))\n", "", False),
    ("fecha de 8 cifras nunca es texto", "contratos.py", "    if RE_FECHA_8.fullmatch(t):", "    if False:", False),
    ("almacén legado no aparta la línea", "almacen.py", "        if legado and parcial is not None:", "        if False:", False),
    ("almacén decodifica todo antes de separar (como la r04)", "almacen.py",
     "            datos = ruta.read_bytes()\n", "            datos = ruta.read_bytes()\n            ruta.read_text(encoding=\"utf-8\")\n", False),
    ("plazo numérico aceptado", "interfaz_broker.py",
     '            raise ValueError(f"Fecha u hora de consulta CT-23 no válida (se espera ISO 8601, no un número): {fecha!r}")',
     "            pass", False),
    ("plazo bool aceptado (solo int/float)", "interfaz_broker.py", "if isinstance(fecha, bool) or (", "if (", True),
    ("date sin convertir a texto", "interfaz_broker.py", "            fecha = fecha.isoformat()", "            pass", False),
    ("False o 0 como «sin plazo»", "interfaz_broker.py", "if dado is None or dado == \"\" else", "if not dado else", False),
    ("vencer sin capturar", "interfaz_broker.py", "            except (ValueError, TypeError):", "            except ZeroDivisionError:", False),
    ("vencer captura pero no vence", "interfaz_broker.py", "                vencida = True\n", "                vencida = False\n", False),
    ("vencer sin incidencia", "interfaz_broker.py", '                self.b.almacen.incidencia("DATOS", f"Consulta CT-23 {k}',
     '                (lambda *a, **k: None)("DATOS", f"Consulta CT-23 {k}', False),
]

fallos = 0
for nombre, fichero, original, mutado, equivalente in M:
    ruta = EJ / "bloque_a" / fichero
    texto = ruta.read_text(encoding="utf-8")
    if texto.count(original) != 1:
        print(f"FALLO {nombre}: el texto original aparece {texto.count(original)} veces en {fichero}")
        fallos += 1
        continue
    ruta.write_text(texto.replace(original, mutado), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t93_hallazgos.py"],
                           cwd=EJ, capture_output=True, text=True, env={"PYTHONPATH": str(EJ), "PATH": "/usr/bin:/bin"})
    finally:
        ruta.write_text(texto, encoding="utf-8")
    muere = r.returncode != 0
    ultima = (r.stdout.strip().splitlines() or [""])[-1]
    if equivalente:
        print(f"{'INFO ' if not muere else 'INFO '} {nombre}: {'muere' if muere else 'sobrevive (equivalente)'} — {ultima}")
    else:
        ok = muere
        fallos += 0 if ok else 1
        print(f"{'OK   ' if ok else 'FALLO'} {nombre}: {'muere' if muere else 'SOBREVIVE'} — {ultima}")
print(f"fallos: {fallos}")
sys.exit(1 if fallos else 0)
