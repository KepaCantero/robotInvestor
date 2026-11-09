#!/usr/bin/env bash
# Ejecuta todas las suites del marco común de C, leyendo la lista del propio LEEME
# (sección «Cómo se ejecuta»), que es la fuente de verdad. Por defecto ejecuta solo las
# suites de pruebas/; con --generadores también regenera esquemas y casos.
# Avisa si hay scripts de pruebas que no figuran en el LEEME.
# Uso: pruebas_marco.sh [--generadores]
source "$(dirname "$0")/common.sh"

MARCO="$RAIZ/sistema_global/marco_comun_c"
[[ -d "$MARCO" ]] || fallo "no existe $MARCO"
con_generadores=0
[[ "${1:-}" == "--generadores" ]] && con_generadores=1

# Primer bloque de código tras «## Cómo se ejecuta».
mapfile -t ordenes < <(awk '/^## Cómo se ejecuta/{s=1} s&&/^```/{c++; next} s&&c==1' "$MARCO/LEEME.md" | grep -E '^python3 ')
[[ ${#ordenes[@]} -gt 0 ]] || fallo "no encuentro las órdenes en la sección «Cómo se ejecuta» del LEEME"

"$PY" -c "import jsonschema" 2>/dev/null || fallo "falta jsonschema en $PY (pip install jsonschema, o crea el .venv del proyecto)"

cd "$MARCO"
pasan=0; fallan=0; lista_fallos=()
for orden in "${ordenes[@]}"; do
  # Por defecto, solo las suites de pruebas/; los generadores y el ejemplo de uso del validador, con --generadores.
  if [[ $con_generadores -eq 0 && ( "$orden" != "python3 pruebas/"* || "$orden" == *generar_* ) ]]; then
    continue
  fi
  [[ "$orden" == *"sobre.json"* ]] && continue   # ejemplo de uso del LEEME con un archivo propio, no una prueba
  # La orden viene del LEEME del propio repositorio; se ejecuta con el Python del proyecto.
  orden_py="${orden/#python3/$PY}"
  if salida=$(bash -c "$orden_py" 2>&1); then
    pasan=$((pasan + 1))
  else
    fallan=$((fallan + 1)); lista_fallos+=("$orden")
    echo "FALLA: $orden"; echo "$salida" | tail -5
  fi
done

# Scripts de pruebas que no están en el LEEME (se olvidaron al documentar).
for f in pruebas/pruebas_*.py; do
  grep -q "python3 $f" LEEME.md || aviso "no figura en el LEEME: $f"
done

echo "Marco común de C: $pasan pasan, $fallan fallan"
[[ $fallan -eq 0 ]] || { printf ' - %s\n' "${lista_fallos[@]}"; exit 1; }
