#!/usr/bin/env bash
# QA r01 de T-198: ciclo mock con la configuración por defecto en develop y en T-198; compara las salidas.
# Uso: r01_ciclo_mock.sh <11_Ejecutor de develop> <11_Ejecutor de T-198> <python> <carpeta de trabajo>
set -u
DEV=$1; T198=$2; PY=$3; OUT=$4
mkdir -p "$OUT"
for lado in dev t198; do
  EJ=$DEV; [ "$lado" = t198 ] && EJ=$T198
  rm -rf "$OUT/$lado"
  (cd "$EJ" && "$PY" -m bloque_a.cli --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv \
     --estado "$OUT/$lado/estado" --salida "$OUT/$lado/salida" --as-of 2026-06-05 ciclo > "$OUT/$lado.log" 2>&1; echo "$lado rc=$?")
done
(cd "$OUT/dev/salida" && find . -type f | sort) | while IFS= read -r f; do
  cmp -s "$OUT/dev/salida/$f" "$OUT/t198/salida/$f" && echo "igual  $f" || echo "DISTINTO $f (las rutas temporales difieren: comparar a mano)"
done
ls "$OUT/t198/estado" | grep -c F9_registro_fuentes && echo "hay F9 de la instancia (no debería sin FUE-)" || echo "sin F9_registro_fuentes.jsonl"
