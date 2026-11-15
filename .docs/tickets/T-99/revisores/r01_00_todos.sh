#!/usr/bin/env bash
# QA r01 de T-99: ejecuta todos los scripts de ataque contra una raíz (por defecto, la de este repositorio).
# Uso: .docs/tickets/T-99/revisores/r01_00_todos.sh [<raíz>]   Necesita el .venv del proyecto (jsonschema, pandas).
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ="${1:-$(cd "$DIR/../../../.." && pwd)}"
PY="${PY:-$RAIZ/.venv/bin/python}"
[ -x "$PY" ] || PY="$(cd "$DIR/../../../.." && pwd)/.venv/bin/python"
for s in "$DIR"/r01_0[1-9]_*.py; do
  echo "=== $(basename "$s")"
  PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$s" "$RAIZ" 2>&1 | grep -E '^\[|^[0-9]+/'
done
