#!/usr/bin/env bash
# QA r01 T-203 · 03: ruff y mypy ×3 en cada copia, con las mismas órdenes que tools/check_all.sh (desde la raíz).
# Uso: r01_03_cuotas.sh <copia> [<copia> ...]   Escribe <copia_basename>.ruff.txt / .mypy_<paq>.txt en $SALIDA (o /tmp).
set -u
SALIDA="${SALIDA:-/tmp}"
for C in "$@"; do
  cd "$C" || exit 2
  n=$(basename "$C")
  .venv/bin/ruff check --no-cache --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor 2>/dev/null > "$SALIDA/$n.ruff.txt"
  linea="$n ruff=$(wc -l < "$SALIDA/$n.ruff.txt")"
  for par in "bloque_a/11_Ejecutor bloque_a" "bloque_a_forex/11_Ejecutor bloque_a_forex" "bloque_b/11_Ejecutor bloque_b"; do
    set -- $par
    .venv/bin/mypy --ignore-missing-imports --no-error-summary --cache-dir "$SALIDA/mypycache_$n" "$1/$2" 2>/dev/null \
      > "$SALIDA/$n.mypy_$2.txt"
    linea="$linea mypy_$2=$(wc -l < "$SALIDA/$n.mypy_$2.txt")"
  done
  echo "$linea"
done
