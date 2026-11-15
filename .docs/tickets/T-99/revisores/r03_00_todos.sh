#!/usr/bin/env bash
# QA r03 de T-99: vuelve a ejecutar todo lo de las rondas anteriores (r02_00_todos.sh, que incluye los r01 sentencia a sentencia)
# y después los scripts r03 salvo r03_08 (los mutantes cambian ficheros: se lanzan aparte, y solo sobre un worktree desechable:
# r03_08_mutantes.py <worktree>). r03_10 es r02_03 adaptado (el original se corta con una traza en la 0.3.0).
# Uso: .docs/tickets/T-99/revisores/r03_00_todos.sh [<raíz>]   Tarda unos 6 min. Necesita el .venv del proyecto.
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ="${1:-$(cd "$DIR/../../../.." && pwd)}"
PY="${PY:-$RAIZ/.venv/bin/python}"
[ -x "$PY" ] || PY="$(cd "$DIR/../../../.." && pwd)/.venv/bin/python"
echo "######## rondas anteriores (r02_00_todos.sh)"
PY="$PY" bash "$DIR/r02_00_todos.sh" "$RAIZ"
echo "######## r03"
for s in "$DIR"/r03_0[1-79]_*.py "$DIR"/r03_10_*.py; do
  echo "=== $(basename "$s")"
  PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$s" "$RAIZ" 2>&1 | grep -E '^\[|^[0-9]+/'
done
