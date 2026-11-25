#!/usr/bin/env bash
# T-202 · QA r01 · H-03: el mismo código da cuentas de mypy distintas en el gate según el .venv tenga o no los stubs.
# 1) r05_sonda_stubs.py: seis usos erróneos de scipy, yaml y jsonschema, con las opciones del gate
#    (--ignore-missing-imports): con stubs los ve todos; sin stubs, ninguno.
# 2) El paquete A de develop (sin las cuatro anotaciones de T-202): sin stubs 102 (cuota, verde); con stubs 158 (rojo).
# Uso: r05_gate_segun_entorno.sh <copia de develop> <.venv con stubs> <.venv sin stubs>
set -u
AQUI="$(cd "$(dirname "$0")" && pwd)"; BASE=$1; CON=$2; SIN=$3; CACHE="$(mktemp -d)"
trap 'rm -rf "$CACHE"' EXIT
for v in "$CON" "$SIN"; do
  n=$(cd "$AQUI" && "$v/bin/mypy" --cache-dir "$CACHE/s$RANDOM" --ignore-missing-imports --no-error-summary r05_sonda_stubs.py | grep -c error)
  a=$(cd "$BASE" && "$v/bin/mypy" --cache-dir "$CACHE/a$RANDOM" --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a 2>/dev/null | wc -l)
  echo "$v: sonda $n errores; gate mypy bloque_a sobre develop = $a (cuota $(grep -E '^mypy_bloque_a=' "$BASE/tools/cuotas.txt" | cut -d= -f2))"
done
