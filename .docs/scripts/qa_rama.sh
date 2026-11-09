#!/usr/bin/env bash
# Prepara la QA de una rama de otro agente: la saca en una copia limpia (worktree), muestra sus
# commits y archivos, y ejecuta contra SU código las pruebas de cada pieza que toca.
# Uso: qa_rama.sh <rama-remota> [--base develop]
#   p. ej. qa_rama.sh astra/bloque-b-objeciones-y-evaluacion
# Deja la copia en .docs/scripts/.logs/qa_<rama>/ (ignorada por git); bórrala con git worktree remove.
# Ojo: el venv tiene los bloques instalados en modo editable desde la copia principal, así que
# las pruebas se lanzan con PYTHONPATH apuntando al ejecutor de la copia limpia.
source "$(dirname "$0")/common.sh"

rama="${1:-}"; [[ -n "$rama" ]] || fallo "uso: qa_rama.sh <rama-remota> [--base develop]"
base="develop"; [[ "${2:-}" == "--base" ]] && base="${3:-develop}"
cd "$RAIZ"
git fetch -q origin
git rev-parse -q --verify "origin/$rama" >/dev/null || fallo "no existe origin/$rama"

echo "== Commits de $rama que no están en $base"
git log --oneline "origin/$base..origin/$rama"
echo "== ¿Se puede fusionar por avance rápido? $(git merge-base --is-ancestor "origin/$base" "origin/$rama" && echo sí || echo no)"
echo "== Archivos"
git diff --stat "origin/$base...origin/$rama" | tail -40

mkdir -p "$LOGS"
copia="$LOGS/qa_${rama//\//_}"
[[ ! -e "$copia" ]] || fallo "ya existe $copia (git worktree remove \"$copia\" para empezar de cero)"
git worktree add -q "$copia" "origin/$rama"

piezas=$(git diff --name-only "origin/$base...origin/$rama" | cut -d/ -f1-2 | sort -u)
codigo=0
for ej in bloque_a bloque_a_forex bloque_b; do
  if grep -q "^$ej/" <<<"$piezas"; then
    echo "== pytest $ej (código de la rama)"
    (cd "$copia/$ej/11_Ejecutor" && PYTHONPATH="$PWD" "$PY" -m pytest -q -p no:cacheprovider 2>&1 | tail -3) || codigo=1
  fi
done
if grep -q "^sistema_global/marco_comun_c" <<<"$piezas"; then
  echo "== suites del marco común de C (código de la rama)"
  PY="$PY" "$copia/.docs/scripts/pruebas_marco.sh" | tail -3 || codigo=1
fi
echo "Copia limpia: $copia"
exit $codigo
