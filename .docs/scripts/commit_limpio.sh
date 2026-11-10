#!/usr/bin/env bash
# Commit desde una copia limpia: para cuando el árbol de trabajo tiene cambios a medias de otras tareas.
# Crea una copia de HEAD (git worktree), copia en ella SOLO las rutas indicadas, pasa allí las pruebas del marco
# (si alguna ruta es del marco común de C), su LEEME y el gate completo, y hace commit de esas mismas copias
# probadas (aunque el árbol principal haya cambiado mientras tanto) y push a develop.
# Uso: commit_limpio.sh "mensaje" ruta [ruta...] [--sin-push]
# Autor y líneas finales: GIT_AUTOR_NOMBRE, GIT_AUTOR_EMAIL y GIT_TRAILERS de .env (como commit.sh).
source "$(dirname "$0")/common.sh"

mensaje="${1:-}"; [[ -n "$mensaje" ]] || fallo "uso: commit_limpio.sh \"mensaje\" ruta [ruta...] [--sin-push]"
shift
rutas=(); push=1
for a in "$@"; do
  case "$a" in
    --sin-push) push=0 ;;
    *) rutas+=("$a") ;;
  esac
done
[[ ${#rutas[@]} -gt 0 ]] || fallo "indica las rutas de la tarea: en una copia limpia no se añade todo"

cd "$RAIZ"
rama="$(git rev-parse --abbrev-ref HEAD)"
[[ "$rama" == "develop" ]] || fallo "estás en la rama $rama; el proyecto trabaja en develop"
for r in "${rutas[@]}"; do [[ -f "$r" ]] || fallo "no existe el fichero $r (esta herramienta no borra ficheros)"; done

W="$(mktemp -d "${TMPDIR:-/tmp}/commit_limpio.XXXXXX")"
rmdir "$W"
limpiar() { git -C "$RAIZ" worktree remove --force "$W" 2>/dev/null || true; }
trap limpiar EXIT
git worktree add --detach -q "$W" HEAD
for r in "${rutas[@]}"; do mkdir -p "$W/$(dirname "$r")"; cp -p "$r" "$W/$r"; done
[[ -e "$RAIZ/.venv" ]] && ln -s "$RAIZ/.venv" "$W/.venv"

aviso "copia limpia en $W con ${#rutas[@]} fichero(s)"
if printf '%s\n' "${rutas[@]}" | grep -q '^sistema_global/marco_comun_c/'; then
  (cd "$W" && .docs/scripts/pruebas_marco.sh) || fallo "las pruebas del marco no pasan en la copia limpia: no se hace commit"
  (cd "$W" && "$PY" -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c) || fallo "el LEEME del marco no coincide en la copia limpia"
fi
(cd "$W" && .docs/scripts/gate.sh --completo) || fallo "el gate no pasa en la copia limpia: no se hace commit"

# Se sube la copia probada de cada fichero, no la del árbol principal (que pudo cambiar durante las pruebas).
for r in "${rutas[@]}"; do
  if ! cmp -s "$r" "$W/$r"; then aviso "$r cambió durante las pruebas: se sube la versión probada"; fi
  h="$(git hash-object -w "$W/$r")"
  modo=100644; [[ -x "$W/$r" ]] && modo=100755
  git update-index --add --cacheinfo "$modo,$h,$r"
done

autor=()
[[ -n "${GIT_AUTOR_NOMBRE:-}" ]] && autor+=(-c "user.name=$GIT_AUTOR_NOMBRE")
[[ -n "${GIT_AUTOR_EMAIL:-}" ]] && autor+=(-c "user.email=$GIT_AUTOR_EMAIL")
cuerpo="$mensaje"
[[ -n "${GIT_TRAILERS:-}" ]] && cuerpo="$mensaje"$'\n\n'"$(printf '%b' "$GIT_TRAILERS")"
git "${autor[@]}" commit -q -m "$cuerpo"
aviso "commit $(git rev-parse --short HEAD)"
if [[ $push -eq 1 ]]; then git push -q origin develop && aviso "subido a origin/develop"; fi
