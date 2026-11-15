#!/usr/bin/env bash
# QA r01 de T-96 (revisor nuevo sin contexto, Claude). Utilidades comunes de los scripts r01_*.
# Cada script crea sus propios worktrees desechables desde origin/develop en BASE (por defecto, un
# directorio temporal) y los borra al final. Nunca toca el .venv del repositorio principal.
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
BASE="${BASE_QA:-$(mktemp -d)}"
mkdir -p "$BASE"
REF="${REF_QA:-origin/develop}"
PY312="${PY312_QA:-$(command -v python3.12)}"
OTRO_PY="${OTRO_PY_QA:-$(command -v python3.13 || command -v python3.11 || true)}"
OK=0; MAL=0
WTS=()

nuevo_wt() {  # nuevo_wt <ruta>  → worktree limpio, sin .venv
  git -C "$REPO" worktree add -q --detach "$1" "$REF" >/dev/null 2>&1 || { echo "no pude crear el worktree $1"; exit 2; }
  WTS+=("$1")
}
limpia() {
  local w
  for w in "${WTS[@]}"; do git -C "$REPO" worktree remove --force "$w" >/dev/null 2>&1; done
  git -C "$REPO" worktree prune
}
trap limpia EXIT

espera() {  # espera <descripción> <condición bash>
  if eval "$2"; then echo "  OK    $1"; OK=$((OK+1)); else echo "  FALLO $1"; MAL=$((MAL+1)); fi
}
resumen() { echo "== $(basename "$0"): $OK OK, $MAL FALLO"; [[ $MAL -eq 0 ]]; }
huella_venv() { (cd "$1/.venv" && find . -printf '%p %s %T@\n' | LC_ALL=C sort | sha256sum | cut -c1-16); }
