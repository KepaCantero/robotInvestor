#!/usr/bin/env bash
# QA r01 de T-96. Ruta con espacios y no ASCII; dos ejecuciones seguidas (idempotencia, sin actualizar
# versiones); --comprobar no modifica nada; el .venv creado es el del worktree.
source "$(dirname "$0")/r01_00_comun.sh"
W="$BASE/ruta con espacios/año 1"
mkdir -p "$BASE/ruta con espacios"
nuevo_wt "$W"
S="$W/.docs/scripts/preparar_entorno.sh"

echo "1) primera ejecución en: $W"
"$S" >"$BASE/r01_01_a.log" 2>&1; rc=$?
espera "rc 0 en ruta con espacios (rc=$rc)" "[[ $rc -eq 0 ]]"
espera "el .venv es el del worktree" "[[ -x \"\$W/.venv/bin/python\" ]] && grep -q 'creando $W/.venv' \"\$BASE/r01_01_a.log\""
espera "el ejecutable bloque-a arranca (shebang con espacios)" "\"\$W/.venv/bin/bloque-a\" --help >/dev/null 2>&1"
espera "pytest y mypy arrancan" "\"\$W/.venv/bin/pytest\" --version >/dev/null 2>&1 && \"\$W/.venv/bin/mypy\" --version >/dev/null 2>&1"
f1="$("$W/.venv/bin/pip" freeze 2>/dev/null | sha256sum)"

echo "2) segunda ejecución (idempotencia)"
"$S" >"$BASE/r01_01_b.log" 2>&1; rc=$?
f2="$("$W/.venv/bin/pip" freeze 2>/dev/null | sha256sum)"
espera "rc 0 en la segunda ejecución (rc=$rc)" "[[ $rc -eq 0 ]]"
espera "pip freeze idéntico antes y después (no actualiza nada)" "[[ \"\$f1\" == \"\$f2\" ]]"
espera "no vuelve a crear el entorno" "! grep -q creando \"\$BASE/r01_01_b.log\""

echo "3) --comprobar no modifica el .venv ni el árbol de trabajo"
h1="$(huella_venv "$W")"; g1="$(git -C "$W" status --porcelain | sha256sum)"
"$S" --comprobar >"$BASE/r01_01_c.log" 2>&1; rc=$?
h2="$(huella_venv "$W")"; g2="$(git -C "$W" status --porcelain | sha256sum)"
espera "--comprobar rc 0 (rc=$rc)" "[[ $rc -eq 0 ]]"
espera "huella del .venv igual tras --comprobar" "[[ \"\$h1\" == \"\$h2\" ]]"
espera "git status igual tras --comprobar" "[[ \"\$g1\" == \"\$g2\" ]]"
espera "git status limpio (el script no deja ficheros versionables)" "[[ -z \"\$(git -C \"\$W\" status --porcelain)\" ]]"

echo "4) el .venv del repositorio principal no se tocó"
espera "el .venv principal sigue intacto (python del principal apunta a su prefijo)" "[[ \"\$(\"\$REPO/.venv/bin/python\" -c 'import sys;print(sys.prefix)')\" == \"\$REPO/.venv\" ]]"
resumen
