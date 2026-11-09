#!/usr/bin/env bash
# Ejecuta el gate del repositorio y deja el log completo en .docs/scripts/.logs/.
# Uso: gate.sh            → ./tools/check_all.sh --core (rápido: corpus, configuración, referencias, pruebas básicas)
#      gate.sh --completo → ./tools/check_all.sh (todo, incluidas las suites de los bloques; varios minutos)
source "$(dirname "$0")/common.sh"

modo="--core"
[[ "${1:-}" == "--completo" ]] && modo=""
mkdir -p "$LOGS"
log="$LOGS/gate_$(date +%Y%m%d_%H%M%S).log"

cd "$RAIZ"
set +e
./tools/check_all.sh $modo >"$log" 2>&1
codigo=$?
set -e

# Resumen: líneas de resultado sin códigos de color.
sed 's/\x1b\[[0-9;]*m//g' "$log" | grep -E "✓|✗|Fallaron|Omitidos|PASARON|FALL" | tail -25 || true
echo "Log completo: $log"
exit $codigo
