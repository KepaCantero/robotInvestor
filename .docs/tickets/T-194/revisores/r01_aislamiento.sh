#!/usr/bin/env bash
# T-194 · QA r01 · aislamiento (CA-2, R8): las pruebas no leen el git config, el .env, el entorno GIT_* ni la cola
# real de quien las ejecuta, y su salida no contiene nada de ellos. Además (H-01) comprueba la puerta COLA_ASTRA_SCRIPT.
# Uso, desde la raíz de una copia de trabajo desechable:  bash .docs/tickets/T-194/revisores/r01_aislamiento.sh
set -u
RAIZ="$(git rev-parse --show-toplevel)"; cd "$RAIZ"
PY="$RAIZ/.venv/bin/python"
T="$(mktemp -d)"; trap 'rm -rf "$T"; [[ -f "$T.cola" ]] && mv "$T.cola" .docs/tickets/_relevo/cola_astra.md; rm -f "$RAIZ/.env.qa_t194"; [[ -f "$RAIZ/.env.qa_bak" ]] && mv "$RAIZ/.env.qa_bak" "$RAIZ/.env"' EXIT
N="Revisor Ficticio"; C="revisor@qa-""ficticio.invalid"   # ficticio, partido en dos cadenas
ok=0
# 1) Un usuario «personal» en todas partes: HOME con ~/.gitconfig y XDG, GIT_* y GIT_AUTOR_* exportados, .env en la raíz.
mkdir -p "$T/home/.config/git"
printf '[user]\n\tname = %s\n\temail = %s\n[commit]\n\tgpgsign = true\n' "$N" "$C" > "$T/home/.gitconfig"
cp "$T/home/.gitconfig" "$T/home/.config/git/config"
[[ -f .env ]] && mv .env .env.qa_bak
printf 'GIT_AUTOR_NOMBRE=%s\nGIT_AUTOR_EMAIL=%s\n' "$N" "$C" > .env
# 2) La cola real, fuera (CA-2).
mv .docs/tickets/_relevo/cola_astra.md "$T.cola"
out="$(HOME="$T/home" XDG_CONFIG_HOME="$T/home/.config" GIT_AUTOR_NOMBRE="$N" GIT_AUTOR_EMAIL="$C" \
  GIT_AUTHOR_NAME="$N" GIT_AUTHOR_EMAIL="$C" GIT_COMMITTER_NAME="$N" GIT_COMMITTER_EMAIL="$C" GIT_DIR="$RAIZ/.git" \
  "$PY" -m pytest -q -p no:cacheprovider -rA .docs/scripts/pruebas_cola_astra.py 2>&1)"; rc=$?
rm -f .env; [[ -f .env.qa_bak ]] && mv .env.qa_bak .env
out2="$("$PY" -m pytest -q -p no:cacheprovider .docs/scripts/pruebas_autor_generico.py 2>&1)"; rc2=$?
mv "$T.cola" .docs/tickets/_relevo/cola_astra.md
echo "$out2" | tail -1
[[ $rc2 -eq 0 ]] && echo "OK   pruebas_autor_generico.py no depende de la cola real" || { echo "FALLA (H-06) pruebas_autor_generico.py depende de la cola real"; ok=1; }
echo "$out" | tail -1
[[ $rc -eq 0 ]] && echo "OK   con usuario personal en todas partes y sin la cola real: pasan" || { echo "FALLA rc=$rc"; ok=1; }
if grep -qF -e "$N" -e "$C" <<<"$out"; then echo "FALLA la salida contiene el autor personal"; ok=1; else echo "OK   la salida no contiene el autor personal"; fi
# 3) H-01: COLA_ASTRA_SCRIPT exportado en la shell hace que pruebas_scripts.sh pruebe OTRO fichero: con el script real
#    roto y la variable apuntando a una copia buena, el gate de .docs/scripts queda en verde.
cp .docs/scripts/cola_astra.py "$T/bueno.py"
cp .docs/scripts/cola_astra.py "$T/real.bak"
"$PY" - <<'PY'
from pathlib import Path
p = Path(".docs/scripts/cola_astra.py"); s = p.read_text(encoding="utf-8")
p.write_text(s.replace('if f["estado"] == "HECHA" and not hecha:', 'if False:'), encoding="utf-8")
PY
out="$(COLA_ASTRA_SCRIPT="$T/bueno.py" bash .docs/scripts/pruebas_scripts.sh 2>&1)"; rc=$?
cp "$T/real.bak" .docs/scripts/cola_astra.py
echo "$out" | tail -1
if [[ $rc -eq 0 ]]; then echo "FALLA (H-01) con COLA_ASTRA_SCRIPT exportado, un cola_astra.py roto pasa pruebas_scripts.sh"; ok=1
else echo "OK   COLA_ASTRA_SCRIPT no tapa un script roto"; fi
git diff --quiet -- .docs/scripts/cola_astra.py .docs/tickets/_relevo/cola_astra.md || { echo "FALLA el árbol quedó cambiado"; ok=1; }
exit $ok
