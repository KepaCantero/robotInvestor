#!/usr/bin/env bash
# QA r02 de T-99: vuelve a ejecutar los scripts r01 (sentencia a sentencia, sin tocarlos), en los dos modos (sello del
# registro y sello rehecho por el atacante), y después los scripts r02_01 a r02_09 salvo r02_08 (los mutantes cambian
# ficheros: se lanzan aparte, y solo sobre un worktree desechable: r02_08_mutantes.py <worktree>).
# Uso: .docs/tickets/T-99/revisores/r02_00_todos.sh [<raíz>]   Necesita el .venv del proyecto (jsonschema, pandas).
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ="${1:-$(cd "$DIR/../../../.." && pwd)}"
PY="${PY:-$RAIZ/.venv/bin/python}"
[ -x "$PY" ] || PY="$(cd "$DIR/../../../.." && pwd)/.venv/bin/python"
for modo in "" "--sello"; do
  echo "##### r01 sentencia a sentencia ${modo:-(sello del registro)}"
  for s in "$DIR"/r01_0[1-9]_*.py; do
    echo "=== $(basename "$s") $modo"
    PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$DIR/r02_00_r01_por_sentencias.py" "$RAIZ" "$s" $modo 2>&1 | grep -E '^\[HALLAZGO|^\[EXCEP|^[0-9]+/'
  done
done
echo "##### r02"
for s in "$DIR"/r02_0[1-79]_*.py; do
  echo "=== $(basename "$s")"
  PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$s" "$RAIZ" 2>&1 | grep -E '^\[|^[0-9]+/'
done
