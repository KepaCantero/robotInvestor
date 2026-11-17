#!/usr/bin/env bash
# QA r01 de T-173: backtest mock del README en la base (develop) y en la rama, con el perfil por defecto y con uno con H5.
# Uso: r01_regresion.sh <raiz_base> <raiz_rama> <salida> <python>
set -euo pipefail
BASE=$1; RAMA=$2; OUT=$3; PY=$4
mkdir -p "$OUT"
for perfil in defecto h5; do
  for lado in base rama; do
    raiz=$([ $lado = base ] && echo "$BASE" || echo "$RAMA")/bloque_a/11_Ejecutor
    cfg="$raiz/config/por_defecto.yaml"
    if [ $perfil = h5 ]; then
      cfg="$OUT/cfg_h5_$lado.yaml"
      sed 's/^  activos: \[DIV\]$/  activos: [DIV, RV, MP, RF]/' "$raiz/config/por_defecto.yaml" > "$cfg"
      grep -q "activos: \[DIV, RV, MP, RF\]" "$cfg"
    fi
    d="$OUT/$perfil-$lado"; rm -rf "$d"; mkdir -p "$d"
    (cd "$raiz" && PYTHONPATH=. "$PY" -m bloque_a.cli --config "$cfg" --cliente mock --datos ejemplos/datos_sinteticos \
       --universo config/universo_ejemplo.csv --estado "$d/estado" --salida "$d/salida" \
       backtest --desde 2024-01-05 --hasta 2024-03-29 > "$d/log.txt" 2>&1) &
  done
done
wait
echo hecho
