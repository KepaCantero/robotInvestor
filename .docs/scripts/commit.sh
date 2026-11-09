#!/usr/bin/env bash
# Comprueba, hace commit y sube a develop en un paso.
# Uso: commit.sh "mensaje" [rutas...] [--completo] [--sin-push]
#   rutas: lo que se añade (por defecto, todo lo cambiado: git add -A)
#   --completo: gate completo en lugar del rápido
# Autor: GIT_AUTOR_NOMBRE/GIT_AUTOR_EMAIL de .env o tu git config. Líneas finales: GIT_TRAILERS de .env.
source "$(dirname "$0")/common.sh"

mensaje="${1:-}"; [[ -n "$mensaje" ]] || fallo "uso: commit.sh \"mensaje\" [rutas...] [--completo] [--sin-push]"
shift
rutas=(); gate_opt=""; push=1
for a in "$@"; do
  case "$a" in
    --completo) gate_opt="--completo" ;;
    --sin-push) push=0 ;;
    *) rutas+=("$a") ;;
  esac
done

cd "$RAIZ"
rama="$(git rev-parse --abbrev-ref HEAD)"
[[ "$rama" == "develop" ]] || fallo "estás en la rama $rama; el proyecto trabaja en develop"

"$SCRIPTS/gate.sh" $gate_opt || fallo "el gate no pasa: no se hace commit"

if [[ ${#rutas[@]} -gt 0 ]]; then git add -- "${rutas[@]}"; else git add -A; fi
git diff --cached --quiet && fallo "no hay nada que confirmar"
git status --short

autor=()
[[ -n "${GIT_AUTOR_NOMBRE:-}" ]] && autor+=(-c "user.name=$GIT_AUTOR_NOMBRE")
[[ -n "${GIT_AUTOR_EMAIL:-}" ]] && autor+=(-c "user.email=$GIT_AUTOR_EMAIL")
cuerpo="$mensaje"
[[ -n "${GIT_TRAILERS:-}" ]] && cuerpo="$cuerpo"$'\n\n'"$(printf '%b' "$GIT_TRAILERS")"
git "${autor[@]}" commit -q -m "$cuerpo"
git log --oneline -1
if [[ $push -eq 1 ]]; then git push -q origin develop && git status -sb | head -1; fi
