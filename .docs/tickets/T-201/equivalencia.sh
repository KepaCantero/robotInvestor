#!/usr/bin/env bash
# T-201: prueba de equivalencia. Ejecuta la misma secuencia del ejecutor del Bloque A con el código de origin/develop y con el
# de la copia de trabajo y compara todas las salidas (estado y entregables) byte a byte, salvo rutas temporales y latencias.
# Uso: .docs/tickets/T-201/equivalencia.sh <copia_de_trabajo> [<ref_base>]   (por defecto, origin/develop)
# Trabaja fuera del repositorio, en una carpeta temporal nueva (TMPDIR), y termina con 1 si algo difiere o si el testigo de
# sensibilidad (sensibilidad.py) encuentra un punto ciego de la comparación.
set -euo pipefail
COPIA="$(cd "$1" && pwd)"
REF="${2:-origin/develop}"
AQUI="$(cd "$(dirname "$0")" && pwd)"
TRAB="$(mktemp -d "${TMPDIR:-/tmp}/t201_equivalencia.XXXX")"
echo "carpeta de trabajo: $TRAB"
PY="$COPIA/.venv/bin/python"
git -C "$COPIA" archive "$REF" bloque_a | tar -x -C "$TRAB"   # el paquete del Bloque A tal como está en la base
mkdir -p "$TRAB/base" && mv "$TRAB/bloque_a" "$TRAB/base/"

secuencia() {   # $1 raíz del paquete (…/bloque_a), $2 carpeta de resultados
  local EJ="$1/11_Ejecutor" R="$2"
  mkdir -p "$R"
  cd "$EJ"
  export PYTHONPATH="$EJ" BLOQUE_A_RAIZ="$1" PYTHONHASHSEED=0
  local G=(--cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv)
  "$PY" -m bloque_a.cli "${G[@]}" --salida "$R/bt" backtest --desde 2024-01-05 --hasta 2024-03-29 > "$R/01_backtest.out" 2>&1
  "$PY" -m bloque_a.cli "${G[@]}" --estado "$R/estado" --salida "$R/entregables" --as-of 2026-06-05 ciclo > "$R/02_ciclo.out" 2>&1
  "$PY" -m bloque_a.cli "${G[@]}" --estado "$R/estado" --salida "$R/entregables" --as-of 2026-06-05 \
       peticion --json ejemplos/peticiones/peticion_ad_hoc.json > "$R/03_peticion.out" 2>&1
  "$PY" -m bloque_a.cli "${G[@]}" --estado "$R/estado" --salida "$R/entregables" --as-of 2026-06-05 \
       consulta "¿Por qué no aparece la renta fija esta semana?" > "$R/04_consulta.out" 2>&1
  local OPP
  OPP="$("$PY" -c 'import json,sys
ultimo = {}
for l in open(sys.argv[1], encoding="utf-8"):
    e = json.loads(l)
    if str(e.get("opp_id", "")).startswith("OPP-") and e.get("estado"):
        ultimo[e["opp_id"]] = e["estado"]
print(next(o for o, est in sorted(ultimo.items()) if est != "VIGENTE"))' "$(ls "$R"/estado/F3*.jsonl | head -1)")"   # una no VIGENTE: el C6 se ejecuta
  "$PY" -m bloque_a.cli "${G[@]}" --estado "$R/estado" --salida "$R/entregables" --as-of 2026-06-05 \
       seguimiento alta --json "{\"opp_id\":\"$OPP\",\"frecuencia\":\"SEMANAL\",\"motivo\":\"equivalencia T-201\",\"senales_interes\":[],\"fecha_fin\":null}" \
       > "$R/05_seg_alta.out" 2>&1
  "$PY" -m bloque_a.cli "${G[@]}" --estado "$R/estado" --salida "$R/entregables" --as-of 2026-06-12 \
       seguimiento ejecutar > "$R/06_seg_ejecutar.out" 2>&1
  "$PY" -m bloque_a.cli "${G[@]}" --estado "$R/estado" --salida "$R/entregables" --as-of 2026-06-12 evaluar > "$R/07_evaluar.out" 2>&1
  "$PY" -m bloque_a.cli "${G[@]}" --estado "$R/estado" --as-of 2026-06-12 estado > "$R/08_estado.out" 2>&1
  cd - > /dev/null
}

secuencia "$TRAB/base/bloque_a" "$TRAB/r_base" &
secuencia "$COPIA/bloque_a" "$TRAB/r_nuevo" &
wait

rc=0
"$PY" -I "$AQUI/comparar.py" "$TRAB/r_base" "$TRAB/r_nuevo" "$TRAB/base/bloque_a" "$COPIA/bloque_a" || rc=1
# r02 (QA r01, H-01): el testigo de sensibilidad comprueba que la comparación no normaliza de más
"$PY" -I "$AQUI/sensibilidad.py" "$TRAB" "$AQUI/comparar.py" "$COPIA/bloque_a" || rc=1
exit $rc
