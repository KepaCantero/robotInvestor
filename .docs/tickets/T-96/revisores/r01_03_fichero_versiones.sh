#!/usr/bin/env bash
# QA r01 de T-96. El fichero de versiones: ausente, líneas sin ==, nombres con mayúsculas, guiones,
# puntos y guiones bajos, comentario al final de línea, ===, CRLF, duplicados, una línea quitada,
# un paquete fijado que nadie usa, argumentos extra. Solo --comprobar (sin red) salvo la última prueba.
source "$(dirname "$0")/r01_00_comun.sh"
W="$BASE/wt_fichero"; nuevo_wt "$W"; S="$W/.docs/scripts/preparar_entorno.sh"; F="$W/tools/requisitos_entorno.txt"
"$S" >"$BASE/prep.log" 2>&1 || { echo "no se pudo preparar el entorno base"; exit 2; }
restaura() { git -C "$W" checkout -q -- tools/requisitos_entorno.txt; }
comprueba() { "$S" --comprobar "$@" >"$BASE/c.log" 2>&1; rc=$?; echo "     rc=$rc · $(grep -v '^· aviso' "$BASE/c.log" | tail -2 | tr '\n' ' ')"; }
edita() { "$PY312" -I -c "$1" "$F"; }

echo "1) fichero ausente"
mv "$F" "$F.bak"
comprueba;            espera "--comprobar falla con 'no existe'" "[[ $rc -ne 0 ]] && grep -q 'no existe' \"\$BASE/c.log\""
"$S" >"$BASE/c.log" 2>&1; rc=$?
espera "sin --comprobar también falla, sin tocar el .venv" "[[ $rc -ne 0 ]] && grep -q 'no existe' \"\$BASE/c.log\""
mv "$F.bak" "$F"

echo "2) línea sin == (arch>=8.0.0)"
edita 'import sys;p=sys.argv[1];t=open(p).read().replace("arch==8.0.0","arch>=8.0.0");open(p,"w").write(t)'
comprueba; espera "rechaza la línea sin versión exacta y la nombra" "[[ $rc -ne 0 ]] && grep -q 'arch>=8.0.0' \"\$BASE/c.log\""; restaura

echo "3) nombres con otra grafía (pyyaml, Typing-Extensions, ast.serialize, RPDS_PY)"
edita 'import sys;p=sys.argv[1];t=open(p).read();t=t.replace("PyYAML==","pyyaml==").replace("typing_extensions==","Typing-Extensions==").replace("ast_serialize==","ast.serialize==").replace("rpds-py==","RPDS_PY==");open(p,"w").write(t)'
comprueba; espera "normaliza los nombres (rc 0)" "[[ $rc -eq 0 ]]"; restaura

echo "4) comentario al final de línea (pip lo acepta)"
edita 'import sys;p=sys.argv[1];t=open(p).read().replace("arch==8.0.0","arch==8.0.0  # nota");open(p,"w").write(t)'
"$W/.venv/bin/pip" install --dry-run -q -c "$F" arch >"$BASE/pip.log" 2>&1; rcp=$?
comprueba
espera "script y pip interpretan igual la línea (pip rc=$rcp, script rc=$rc)" "[[ ( $rcp -eq 0 && $rc -eq 0 ) || ( $rcp -ne 0 && $rc -ne 0 ) ]]"; restaura

echo "5) operador === (identidad arbitraria)"
edita 'import sys;p=sys.argv[1];t=open(p).read().replace("arch==8.0.0","arch===8.0.0");open(p,"w").write(t)'
comprueba; espera "falla cerrado o lo trata como 8.0.0, sin mensaje engañoso con '=8.0.0'" "! grep -q 'fijado =8.0.0' \"\$BASE/c.log\""; restaura

echo "6) fin de línea CRLF"
edita 'import sys;p=sys.argv[1];t=open(p,newline="").read().replace("\n","\r\n");open(p,"w",newline="").write(t)'
comprueba; espera "acepta CRLF (rc 0)" "[[ $rc -eq 0 ]]"; restaura

echo "7) duplicado contradictorio (arch==9.0.0 al final)"
echo "arch==9.0.0" >>"$F"
comprueba; espera "falla cerrado (rc≠0)" "[[ $rc -ne 0 ]]"
espera "el mensaje señala el duplicado y no solo una versión distinta" "grep -qi 'duplicad\|repetid\|dos veces' \"\$BASE/c.log\""; restaura

echo "8) línea quitada (tzdata): lo instalado deja de estar fijado"
edita 'import sys;p=sys.argv[1];t="".join(l for l in open(p) if not l.startswith("tzdata=="));open(p,"w").write(t)'
comprueba
espera "--comprobar avisa del paquete no fijado" "grep -q 'tzdata' \"\$BASE/c.log\""
espera "--comprobar falla si hay un paquete instalado sin fijar (rc≠0)" "[[ $rc -ne 0 ]]"; restaura

echo "9) paquete fijado que ningún ejecutor usa (six==1.16.0)"
echo "six==1.16.0" >>"$F"
comprueba; espera "--comprobar lo da por que falta (rc≠0)" "[[ $rc -ne 0 ]] && grep -q 'falta six' \"\$BASE/c.log\""; restaura

echo "10) argumentos"
"$S" --comprobar --otra >"$BASE/c.log" 2>&1; rc=$?
espera "rechaza argumentos de más (rc≠0)" "[[ $rc -ne 0 ]]"
"$S" --desconocida >"$BASE/c.log" 2>&1; rc=$?
espera "rechaza una opción desconocida con el uso" "[[ $rc -ne 0 ]] && grep -q uso \"\$BASE/c.log\""

echo "11) .venv ausente con --comprobar: falla y no lo crea"
mv "$W/.venv" "$W/.venv.bak"
comprueba; espera "rc≠0 y sin .venv nuevo" "[[ $rc -ne 0 && ! -e \"\$W/.venv\" ]]"
mv "$W/.venv.bak" "$W/.venv"
resumen
