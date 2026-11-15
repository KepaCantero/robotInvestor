#!/usr/bin/env bash
# QA r01 de T-96. Las cuotas de ruff y mypy salen iguales con el .venv nuevo y con el .venv principal,
# sobre el MISMO código (el del worktree) y con cachés en un directorio temporal (no escribe en el repo).
# Con VENV_QA=<ruta a un .venv de T-96 ya creado> no crea worktree.
source "$(dirname "$0")/r01_00_comun.sh"
if [[ -n "${VENV_QA:-}" ]]; then V="$VENV_QA"; W="$(dirname "$V")"; else
  W="$BASE/wt_cuotas"; nuevo_wt "$W"; "$W/.docs/scripts/preparar_entorno.sh" >"$BASE/prep.log" 2>&1 || exit 2; V="$W/.venv"; fi
cd "$W"
EJ=(bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor); PQ=(bloque_a bloque_a_forex bloque_b)
cuenta() {  # cuenta <venv> <etiqueta>
  local v="$1" e="$2" i
  echo "ruff=$("$v/bin/ruff" check --no-cache --output-format=concise "${EJ[@]}" 2>/dev/null | wc -l | tr -d ' ')"
  for i in 0 1 2; do
    echo "mypy_${PQ[$i]}=$("$v/bin/mypy" --cache-dir "$BASE/cache_$e" --ignore-missing-imports --no-error-summary "${EJ[$i]}/${PQ[$i]}" 2>/dev/null | wc -l | tr -d ' ')"
  done
}
cuenta "$V" nuevo >"$BASE/nuevo.txt"
cuenta "$REPO/.venv" principal >"$BASE/principal.txt"
paste -d' ' "$BASE/nuevo.txt" "$BASE/principal.txt" | sed 's/^/     nuevo · principal: /'
espera "mismas cifras con los dos entornos" "diff -q \"\$BASE/nuevo.txt\" \"\$BASE/principal.txt\" >/dev/null"
while IFS== read -r k n; do
  q="$(grep "^$k=" tools/cuotas.txt | cut -d= -f2)"
  espera "$k=$n dentro de la cuota $q" "[[ $n -le $q ]]"
done <"$BASE/nuevo.txt"
resumen
