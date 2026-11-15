#!/usr/bin/env bash
# QA r01 de T-96. Entornos a medias o rotos: venv sin pip, creación de venv que falla a mitad
# (como en Debian/Ubuntu sin python3.12-venv), venv de otro Python, interrupción durante pip, pip borrado.
source "$(dirname "$0")/r01_00_comun.sh"
W="$BASE/wt_medias"; nuevo_wt "$W"; S="$W/.docs/scripts/preparar_entorno.sh"
ejecuta() { "$@" >"$BASE/salida.log" 2>&1; rc=$?; msg="$(tail -3 "$BASE/salida.log" | tr '\n' ' ')"; echo "     rc=$rc · $msg"; }

echo "a) .venv creado sin pip (venv --without-pip)"
"$PY312" -m venv --without-pip "$W/.venv"
ejecuta "$S"
espera "falla cerrado (rc≠0)" "[[ $rc -ne 0 ]]"
espera "el mensaje dice que falta pip o que el entorno está roto" "grep -qiE 'pip.*(no existe|falta|no encontrado|roto)|entorno (roto|a medias|incompleto)|borra' \"\$BASE/salida.log\""
rm -rf "$W/.venv"

echo "b) la creación del venv falla a mitad (simula ensurepip ausente) con PYTHON_ENTORNO"
FAKE="$BASE/python_sin_ensurepip"
cat >"$FAKE" <<EOS
#!/usr/bin/env bash
if [[ "\${1:-}" == "-m" && "\${2:-}" == "venv" ]]; then shift 2; "$PY312" -m venv --without-pip "\$@"; echo "The virtual environment was not created successfully because ensurepip is not available." >&2; exit 1; fi
exec "$PY312" "\$@"
EOS
chmod +x "$FAKE"
PYTHON_ENTORNO="$FAKE" ejecuta "$S"
espera "falla cerrado (rc≠0)" "[[ $rc -ne 0 ]]"
espera "no deja un .venv a medias" "[[ ! -e \"\$W/.venv\" ]]"
echo "   b2) segunda ejecución, ya con un Python correcto"
ejecuta "$S"
espera "la segunda ejecución se recupera sola (rc 0) o explica que hay que borrar .venv" "[[ $rc -eq 0 ]] || grep -qiE 'borra|elimina|a medias|incompleto|roto' \"\$BASE/salida.log\""
rm -rf "$W/.venv"

if [[ -n "$OTRO_PY" ]]; then
  echo "c) .venv existente creado con otro Python ($("$OTRO_PY" -V))"
  "$OTRO_PY" -m venv "$W/.venv"
  n0="$(ls "$W"/.venv/lib/python*/site-packages | wc -l)"
  ejecuta "$S"
  n1="$(ls "$W"/.venv/lib/python*/site-packages | wc -l)"
  espera "falla cerrado (rc≠0)" "[[ $rc -ne 0 ]]"
  espera "el mensaje nombra la versión de Python" "grep -q '3.12' \"\$BASE/salida.log\""
  espera "valida la versión ANTES de instalar (site-packages no cambia: $n0 → $n1)" "[[ $n0 -eq $n1 ]]"
  rm -rf "$W/.venv"
fi

echo "d) interrupción (SIGTERM: un proceso en segundo plano ignora SIGINT) a mitad de pip install y reintento"
"$S" >"$BASE/int.log" 2>&1 & pid=$!
for i in $(seq 1 120); do [[ -x "$W/.venv/bin/pip" ]] && grep -q instalando "$BASE/int.log" && break; sleep 0.5; done
sleep 8; pkill -TERM -P "$pid" 2>/dev/null; kill -TERM "$pid" 2>/dev/null; wait "$pid"; rci=$?
echo "     interrumpido con rc=$rci"
ejecuta "$S" --comprobar
espera "la interrupción llegó a tiempo (rc del script ≠ 0)" "[[ $rci -ne 0 ]]"
espera "tras la interrupción, --comprobar no da por bueno el entorno (rc≠0)" "[[ $rc -ne 0 ]]"
ejecuta "$S"
espera "el reintento completa el entorno (rc 0)" "[[ $rc -eq 0 ]]"

echo "e) pip borrado del .venv"
mv "$W/.venv/bin/pip" "$BASE/pip.bak"
ejecuta "$S" --comprobar
espera "--comprobar falla cerrado (rc≠0)" "[[ $rc -ne 0 ]]"
espera "el mensaje habla de pip, no de 49 paquetes que faltan" "! grep -q 'falta annotated-types' \"\$BASE/salida.log\""
mv "$BASE/pip.bak" "$W/.venv/bin/pip"
resumen
