#!/usr/bin/env bash
# QA r01 de T-96 (CA-4). Sin Python 3.12: ejecutable inexistente, otro Python, un ejecutable que no es
# Python, nombre sin ruta y PATH/HOME sin python3.12. Debe fallar con mensaje claro y sin dejar .venv.
source "$(dirname "$0")/r01_00_comun.sh"
W="$BASE/wt_sinpy"; nuevo_wt "$W"; S="$W/.docs/scripts/preparar_entorno.sh"
prueba() {  # prueba <descripción> <regex del mensaje> <cmd...>
  local d="$1" re="$2"; shift 2
  "$@" >"$BASE/s.log" 2>&1; local rc=$?
  echo "     rc=$rc · $(tail -1 "$BASE/s.log")"
  espera "$d: rc≠0" "[[ $rc -ne 0 ]]"
  espera "$d: mensaje claro" "grep -qE '$re' \"\$BASE/s.log\""
  espera "$d: no deja .venv" "[[ ! -e \"\$W/.venv\" ]]"
  rm -rf "$W/.venv"
}
prueba "PYTHON_ENTORNO inexistente" "no encuentro Python 3.12" env PYTHON_ENTORNO=/no/existe/python3.12 "$S"
[[ -n "$OTRO_PY" ]] && prueba "PYTHON_ENTORNO=otro Python" "es Python 3\.[0-9]+; el proyecto usa 3\.12" env PYTHON_ENTORNO="$OTRO_PY" "$S"
prueba "PYTHON_ENTORNO=/bin/false" "no puedo ejecutar" env PYTHON_ENTORNO=/bin/false "$S"
prueba "PYTHON_ENTORNO=/bin/true (no imprime versión)" "el proyecto usa 3\.12" env PYTHON_ENTORNO=/bin/true "$S"
prueba "PYTHON_ENTORNO=directorio" "no encuentro Python 3.12|no puedo ejecutar" env PYTHON_ENTORNO=/usr/bin "$S"
# PATH mínimo sin python3.12 y HOME sin ~/.local/bin/python3.12
mkdir -p "$BASE/bin_min" "$BASE/home_vacio"
for c in bash env dirname cat git sed grep tail; do ln -sf "$(command -v $c)" "$BASE/bin_min/$c"; done
prueba "sin python3.12 en PATH ni en ~/.local/bin" "no encuentro Python 3.12" env -i PATH="$BASE/bin_min" HOME="$BASE/home_vacio" "$S"
# Nombre sin ruta: python3.12 existe en el PATH, pero PYTHON_ENTORNO=python3.12 no se resuelve
env PYTHON_ENTORNO=python3.12 "$S" >"$BASE/s.log" 2>&1; rc=$?
echo "     (informativo) PYTHON_ENTORNO=python3.12 sin ruta: rc=$rc · $(grep -E 'ERROR|creando' "$BASE/s.log" | head -1)"
rm -rf "$W/.venv"
resumen
