#!/usr/bin/env bash
# QA r05 de T-99: vuelve a ejecutar todo lo de las rondas anteriores (r04_00_todos.sh, que lanza r03_00_todos.sh, r02_00_todos.sh
# y los r01 sentencia a sentencia), después, sentencia a sentencia con r05_00_por_sentencias.py, los scripts que la 0.5.0 corta
# (el sello ya vive dentro de .git y una variante no se repite con un intento abierto), y por último los r05.
# r05_04 ataca pruebas_scripts.sh solo si se le da un worktree desechable. r05_05 (mutantes) cambia ficheros: se lanza aparte,
# y solo sobre un worktree desechable: r05_05_mutantes.py <worktree>.
# Uso: .docs/tickets/T-99/revisores/r05_00_todos.sh [<raíz>] [<worktree desechable>] [<clon completo del proyecto>]
#   Tarda unos 20 min. Necesita el .venv.
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ="${1:-$(cd "$DIR/../../../.." && pwd)}"
DESECHABLE="${2:-}"
COMPLETO="${3:-}"
PY="${PY:-$RAIZ/.venv/bin/python}"
[ -x "$PY" ] || PY="$(cd "$DIR/../../../.." && pwd)/.venv/bin/python"
echo "######## rondas anteriores (r04_00_todos.sh)"
PY="$PY" bash "$DIR/r04_00_todos.sh" "$RAIZ" "$DESECHABLE"
echo "######## cortados por la 0.5.0, sentencia a sentencia"
for s in r02_02_ancla_git r02_04_adopcion r03_01_ancla_historial r03_02_sello_tolerante r03_03_cerrojo_lectores \
         r03_04_adopcion_pendientes r04_03_r03_01_adaptado r04_04_fallido_tardio; do
  echo "=== $s.py (sentencias)"
  PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$DIR/r05_00_por_sentencias.py" "$RAIZ" "$DIR/$s.py" 2>&1 | grep -E '^\[|^[0-9]+/'
done
echo "######## r05"
for s in "$DIR"/r05_0[1-4]_*.py; do
  echo "=== $(basename "$s")"
  extra=""
  [[ "$s" == *r05_01_* && -n "$COMPLETO" ]] && extra="$COMPLETO"
  [[ "$s" == *r05_04_* && -n "$DESECHABLE" ]] && extra="$DESECHABLE"
  PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$s" "$RAIZ" $extra 2>&1 | grep -E '^\[|^[0-9]+/'
done
