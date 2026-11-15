#!/usr/bin/env bash
# Pruebas de .docs/scripts (banco, registro, borradores de contratos, cola) con su línea base: como en los bloques, el
# NÚMERO de pruebas no puede bajar (T-99, QA r02 y r03, H-12). La línea base está en .docs/scripts/linea_base_pruebas.txt.
# Uso: .docs/scripts/pruebas_scripts.sh   (desde cualquier carpeta; lo llaman commit.sh y commit_limpio.sh)
source "$(dirname "$0")/common.sh"
cd "$RAIZ"
base="$(tr -dc '0-9' < .docs/scripts/linea_base_pruebas.txt)"
[[ -n "$base" ]] || fallo "no hay línea base en .docs/scripts/linea_base_pruebas.txt"
salida="$("$PY" -m pytest -q -p no:cacheprovider .docs/scripts/pruebas_*.py 2>&1)"; codigo=$?
echo "$salida" | tail -1
[[ $codigo -eq 0 ]] || fallo "las pruebas de .docs/scripts fallan"
n="$(echo "$salida" | tail -1 | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+')"
[[ -n "$n" && "$n" -ge "$base" ]] || fallo "las pruebas de .docs/scripts son ${n:-0}, por debajo de la línea base $base"
