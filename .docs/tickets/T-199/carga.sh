#!/usr/bin/env bash
# carga.sh N_CPU N_MEM SEGUNDOS: N_CPU bucles de CPU y N_MEM copias de memoria (numpy) durante SEGUNDOS
ncpu=${1:-8}; nmem=${2:-0}; seg=${3:-600}
PY="$(cd "$(dirname "$0")/../../.." && pwd)/.venv/bin/python"
for i in $(seq $ncpu); do timeout $seg $PY -c "while True: pass" & done
for i in $(seq $nmem); do timeout $seg $PY -c "
import numpy as np
a=np.ones(32_000_000); b=np.empty_like(a)
while True: np.copyto(b,a)" & done
wait
