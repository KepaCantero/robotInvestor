#!/bin/bash
# r04 · Backtest largo (63 semanas, 12 tipos por defecto) con el código nuevo: ¿alguna ruta legítima dispara PronosticoCongelado (R11)?
# ¿Se resuelven pronósticos, se arrastran vigentes y no queda nada en _borradores? Tiempo y estado final.
S=/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad
OUT=$S/qa_t53/bt_largo; rm -rf $OUT; mkdir -p $OUT
cd $S/wt_new/bloque_a/11_Ejecutor
T0=$(date +%s); PYTHONPATH=$S/wt_new/bloque_a/11_Ejecutor /home/claude/repo/.venv/bin/python -m bloque_a.cli --cliente mock --datos ejemplos/datos_sinteticos \
  --universo config/universo_ejemplo.csv --estado $OUT/estado --salida $OUT/salida backtest --desde 2025-03-07 --hasta 2026-05-29 > $OUT/log.txt 2>&1
echo "rc=$? segundos=$(( $(date +%s) - T0 ))" >> $OUT/log.txt
