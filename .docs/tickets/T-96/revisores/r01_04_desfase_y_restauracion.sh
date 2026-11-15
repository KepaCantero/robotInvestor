#!/usr/bin/env bash
# QA r01 de T-96 (CA-3). Otra versión de un paquete fijado (arch 9.0.0) → --comprobar ≠ 0 y lo nombra;
# el script sin opciones vuelve a la versión fijada; un paquete instalado y no fijado; el script nunca
# actualiza por su cuenta. Con MYPY_QA=1 mide además la cuota de mypy de A con arch 9.0.0 (motivo de T-96).
source "$(dirname "$0")/r01_00_comun.sh"
W="$BASE/wt_desfase"; nuevo_wt "$W"; S="$W/.docs/scripts/preparar_entorno.sh"; P="$W/.venv/bin/pip"
"$S" >"$BASE/prep.log" 2>&1 || { echo "no se pudo preparar el entorno base"; exit 2; }
comprueba() { "$S" --comprobar >"$BASE/c.log" 2>&1; rc=$?; echo "     rc=$rc · $(tail -2 "$BASE/c.log" | tr '\n' ' ')"; }

echo "1) entorno recién creado"
comprueba; espera "--comprobar da 0" "[[ $rc -eq 0 ]]"
grep -nE -- '-U|--upgrade|--force-reinstall' "$W/.docs/scripts/preparar_entorno.sh" >/dev/null; up=$?
espera "el script no usa -U/--upgrade/--force-reinstall" "[[ $up -ne 0 ]]"

echo "2) arch 9.0.0 instalada a mano"
"$P" install -q arch==9.0.0 >"$BASE/arch9.log" 2>&1 || { echo "no se pudo instalar arch 9.0.0"; exit 2; }
comprueba
espera "--comprobar da ≠ 0" "[[ $rc -ne 0 ]]"
espera "y nombra arch con las dos versiones" "grep -q 'arch: instalado 9.0.0, fijado 8.0.0' \"\$BASE/c.log\""
if [[ "${MYPY_QA:-0}" == 1 ]]; then
  n="$(cd "$W" && .venv/bin/mypy --cache-dir "$BASE/mypy_cache" --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a 2>/dev/null | wc -l)"
  q="$(grep '^mypy_bloque_a=' "$W/tools/cuotas.txt" | cut -d= -f2)"
  echo "     mypy bloque_a con arch 9.0.0: $n (cuota $q)"
fi

echo "3) el script sin opciones vuelve a la versión fijada"
"$S" >"$BASE/rest.log" 2>&1; rc=$?
v="$("$P" show arch 2>/dev/null | awk '/^Version:/{print $2}')"
espera "rc 0 y arch vuelve a 8.0.0 (ahora $v)" "[[ $rc -eq 0 && \"$v\" == 8.0.0 ]]"

echo "4) un paquete instalado y no fijado (six)"
"$P" install -q six >/dev/null 2>&1
comprueba
espera "--comprobar lo menciona" "grep -q 'six' \"\$BASE/c.log\""
echo "     (informativo) rc de --comprobar con un paquete sin fijar: $rc"
f1="$("$P" freeze 2>/dev/null | sha256sum)"; "$S" >/dev/null 2>&1; f2="$("$P" freeze 2>/dev/null | sha256sum)"
espera "el script no desinstala ni cambia nada al repetir (freeze igual)" "[[ \"\$f1\" == \"\$f2\" ]]"
"$P" uninstall -y -q six >/dev/null 2>&1

echo "5) un paquete fijado borrado a mano (tzdata) → el script lo repone con la versión fijada"
"$P" uninstall -y -q tzdata >/dev/null 2>&1
comprueba; espera "--comprobar da ≠ 0 y nombra tzdata" "[[ $rc -ne 0 ]] && grep -q 'falta tzdata' \"\$BASE/c.log\""
"$S" >/dev/null 2>&1; rc=$?
espera "el script lo repone (rc 0)" "[[ $rc -eq 0 ]]"
resumen
