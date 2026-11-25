"""QA T-203, ronda de cierre · 02 (r01_02 con la base como argumento): ningún nombre que T-203 quita de un módulo lo usa otro módulo del repositorio.

1. Para cada .py que cambia entre <base> y <ticket>, calcula con ast los nombres de nivel de módulo que desaparecen.
2. Recorre TODOS los .py del repositorio <ticket> (bloque_a, bloque_a_forex, bloque_b, sistema_global, tools, .docs…)
   y busca: `from <mod> import <nombre>`, `import *` de esos módulos, `<alias>.<nombre>` sobre un alias del módulo
   (`import x as y`, `from p import x as y`) y cadenas literales con el nombre junto al módulo (getattr, importlib,
   monkeypatch.setattr("mod.nombre")).
Uso: python -I rc_02_reexportaciones.py <copia_base> <copia_ticket> <commit_base>   (ronda de cierre: base explícita)
"""
import ast
import subprocess
import sys
from pathlib import Path

base, ticket = Path(sys.argv[1]), Path(sys.argv[2])
cambiados = subprocess.run(["git", "-C", str(ticket), "diff", "--name-only", sys.argv[3], "HEAD", "--", "*.py"],
                           capture_output=True, text=True, check=True).stdout.split()


def nombres_modulo(p: Path) -> set[str]:
    if not p.exists():
        return set()
    t = ast.parse(p.read_text(encoding="utf-8"))
    out = set()
    for n in t.body:
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names:
                out.add((a.asname or a.name).split(".")[0])
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.add(n.name)
        elif isinstance(n, ast.Assign):
            for tg in n.targets:
                for x in ast.walk(tg):
                    if isinstance(x, ast.Name):
                        out.add(x.id)
    return out


quitados = {}
for rel in cambiados:
    q = nombres_modulo(base / rel) - nombres_modulo(ticket / rel)
    if q:
        quitados[rel] = q
print("Nombres de módulo que desaparecen:")
for rel, q in quitados.items():
    print("  ", rel, sorted(q))

# nombre de módulo importable de cada fichero con nombres quitados
def nombre_mod(rel: str) -> str:
    p = Path(rel)
    return p.stem  # se compara por la última componente (operaciones, mock_respuestas, test_unitarias…)

objetivos = {nombre_mod(r): q for r, q in quitados.items()}
usos = []
for f in ticket.rglob("*.py"):
    if any(x in f.parts for x in (".venv", "node_modules", "__pycache__", ".git")):
        continue
    try:
        src = f.read_text(encoding="utf-8")
        t = ast.parse(src)
    except (SyntaxError, UnicodeDecodeError, ValueError):
        continue
    alias = {}
    for n in ast.walk(t):
        if isinstance(n, ast.ImportFrom) and n.module:
            ult = n.module.split(".")[-1]
            for a in n.names:
                if ult in objetivos and (a.name in objetivos[ult] or a.name == "*"):
                    usos.append((str(f.relative_to(ticket)), n.lineno, f"from {n.module} import {a.name}"))
                if a.name in objetivos:
                    alias[a.asname or a.name] = a.name
        elif isinstance(n, ast.Import):
            for a in n.names:
                ult = a.name.split(".")[-1]
                if ult in objetivos:
                    alias[a.asname or a.name] = ult
    for n in ast.walk(t):
        if isinstance(n, ast.Attribute):
            raiz = n.value
            nombre = raiz.id if isinstance(raiz, ast.Name) else (raiz.attr if isinstance(raiz, ast.Attribute) else None)
            m = alias.get(nombre) if nombre else None
            if m is None and nombre in objetivos:
                m = nombre
            if m and n.attr in objetivos[m]:
                usos.append((str(f.relative_to(ticket)), n.lineno, f"{nombre}.{n.attr}"))
        elif isinstance(n, ast.Constant) and isinstance(n.value, str):
            for m, q in objetivos.items():
                for nm in q:
                    if f"{m}.{nm}" in n.value:
                        usos.append((str(f.relative_to(ticket)), n.lineno, repr(n.value)[:80]))
# un uso dentro del propio fichero que define el nombre no cuenta si es un nombre local nuevo; se listan todos
print("Usos externos de nombres quitados:", len(usos))
for u in usos:
    print("  ", *u)
sys.exit(1 if usos else 0)
