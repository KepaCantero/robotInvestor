#!/usr/bin/env bash
# QA r01 de T-96. Coherencia de tools/requisitos_entorno.txt con lo que de verdad necesitan los tres
# ejecutores y el gate: pip check, cierre de dependencias desde las raíces, herramientas del gate,
# importaciones de terceros del repo, y comparación con el .venv del repositorio principal (solo lectura).
# Con VENV_QA=<ruta a un .venv de T-96 ya creado> no crea worktree (solo lee ese entorno).
source "$(dirname "$0")/r01_00_comun.sh"
if [[ -n "${VENV_QA:-}" ]]; then V="$VENV_QA"; W="$(dirname "$V")"; else
  W="$BASE/wt_coh"; nuevo_wt "$W"; "$W/.docs/scripts/preparar_entorno.sh" >"$BASE/prep.log" 2>&1 || exit 2; V="$W/.venv"; fi
F="$W/tools/requisitos_entorno.txt"

"$V/bin/pip" check >"$BASE/check.log" 2>&1; rc=$?
espera "pip check sin conflictos ($(tail -1 "$BASE/check.log"))" "[[ $rc -eq 0 ]]"

"$V/bin/python" -I - "$F" >"$BASE/cierre.log" 2>&1 <<'PYEOF'
import re, sys
from importlib import metadata as md
from packaging.requirements import Requirement
from packaging.markers import default_environment
norma = lambda n: re.sub(r"[-_.]+", "-", n).lower()
fijado = {norma(l.split("==")[0]) for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")}
raices = ["bloque-a", "bloque-a-forex", "bloque-b", "arch", "openpyxl", "python-docx", "ruff", "mypy", "pytest", "pyyaml", "jsonschema"]
dists = {norma(d.metadata["Name"]): d for d in md.distributions()}
visto, pila = set(), list(raices)
while pila:
    n = pila.pop()
    if n in visto: continue
    visto.add(n)
    for r in dists[n].requires or []:
        req = Requirement(r)
        if req.marker and not req.marker.evaluate({**default_environment(), "extra": ""}): continue
        pila.append(norma(req.name))
editables = {"bloque-a", "bloque-a-forex", "bloque-b"}
print("sobran (fijados y no necesarios):", sorted(fijado - visto) or "ninguno")
print("faltan (necesarios y no fijados):", sorted(visto - fijado - editables) or "ninguno")
sys.exit(1 if (fijado - visto) or (visto - fijado - editables) else 0)
PYEOF
rc=$?; sed 's/^/     /' "$BASE/cierre.log"
espera "el fichero es exactamente el cierre de dependencias de las raíces" "[[ $rc -eq 0 ]]"

for t in ruff mypy pytest; do espera "herramienta del gate $t en el .venv" "[[ -x \"\$V/bin/$t\" ]]"; done
espera "importan yaml, jsonschema, arch, openpyxl, docx, numpy, pandas, scipy, anthropic" \
  "(cd / && \"\$V/bin/python\" -c 'import yaml, jsonschema, arch, openpyxl, docx, numpy, pandas, scipy, anthropic')"

# importaciones de terceros en el código del repo que no resuelven con este entorno
"$V/bin/python" -I - "$W" >"$BASE/imp.log" 2>&1 <<'PYEOF'
import ast, sys, pathlib, importlib.util
raiz = pathlib.Path(sys.argv[1]); locales = set(); mods = {}
dirs = ["bloque_a/11_Ejecutor", "bloque_a_forex/11_Ejecutor", "bloque_b/11_Ejecutor", "tools", ".docs/scripts"]
for p in raiz.rglob("*.py"):  # módulos locales: cualquier .py o carpeta del repo (sys.path manipulado en pruebas)
    if ".venv" not in p.parts: locales.add(p.stem); [locales.add(x.name) for x in p.parents]
for d in dirs:
    for p in (raiz / d).rglob("*.py"):
        try: arbol = ast.parse(p.read_text(encoding="utf-8"))
        except SyntaxError: continue
        for n in ast.walk(arbol):
            if isinstance(n, ast.Import): ns = [a.name for a in n.names]
            elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module: ns = [n.module]
            else: continue
            for m in ns: mods.setdefault(m.split(".")[0], p.relative_to(raiz))
fuera = sorted(m for m in mods if m not in sys.stdlib_module_names and m not in locales and importlib.util.find_spec(m) is None)
for m in fuera: print(f"{m}  (p. ej. {mods[m]})")
PYEOF
echo "     importaciones de terceros sin resolver: $(tr '\n' ';' <"$BASE/imp.log")"
espera "solo quedan sin resolver opcionales declarados (yfinance)" "! grep -vE '^(yfinance)' \"\$BASE/imp.log\" | grep -q ."

diff <("$REPO/.venv/bin/pip" freeze --exclude-editable 2>/dev/null) <(grep -v '^#' "$F") >"$BASE/diff.log"; rc=$?
espera "el fichero coincide con pip freeze del .venv principal (solo lectura)" "[[ $rc -eq 0 ]]"
diff <("$REPO/.venv/bin/pip" freeze --exclude-editable 2>/dev/null) <("$V/bin/pip" freeze --exclude-editable 2>/dev/null) >/dev/null; rc=$?
espera "el .venv nuevo tiene exactamente los mismos paquetes que el principal" "[[ $rc -eq 0 ]]"
echo "     (informativo) pip del .venv nuevo: $("$V/bin/pip" --version | cut -d' ' -f1-2) · principal: $("$REPO/.venv/bin/pip" --version | cut -d' ' -f1-2) · python $("$V/bin/python" -V) / $("$REPO/.venv/bin/python" -V)"
resumen
