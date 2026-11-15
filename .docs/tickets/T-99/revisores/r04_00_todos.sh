#!/usr/bin/env bash
# QA r04 de T-99: vuelve a ejecutar todo lo de las rondas anteriores (r03_00_todos.sh, que lanza r02_00_todos.sh y los r01
# sentencia a sentencia) y después los scripts r04. r04_02 y r04_03 son r03_02 y r03_01 adaptados a la 0.4.0 (el sello ya no se
# sube; los originales se cortan al intentar subirlo). r04_06 ataca la línea base de las pruebas solo si se le da un worktree
# desechable como segundo argumento. r04_07 (mutantes) cambia ficheros: se lanza aparte, y solo sobre un worktree desechable:
# r04_07_mutantes.py <worktree>. r04_08 lee (solo «ver») el registro por defecto de la raíz.
# Uso: .docs/tickets/T-99/revisores/r04_00_todos.sh [<raíz>] [<worktree desechable>]   Tarda unos 12 min. Necesita el .venv.
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ="${1:-$(cd "$DIR/../../../.." && pwd)}"
DESECHABLE="${2:-}"
PY="${PY:-$RAIZ/.venv/bin/python}"
[ -x "$PY" ] || PY="$(cd "$DIR/../../../.." && pwd)/.venv/bin/python"
echo "######## rondas anteriores (r03_00_todos.sh)"
PY="$PY" bash "$DIR/r03_00_todos.sh" "$RAIZ"
echo "######## r04"
for s in "$DIR"/r04_0[1-68]_*.py; do
  echo "=== $(basename "$s")"
  extra=""; [[ "$s" == *r04_06_* && -n "$DESECHABLE" ]] && extra="$DESECHABLE"
  PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$s" "$RAIZ" $extra 2>&1 | grep -E '^\[|^[0-9]+/'
done
