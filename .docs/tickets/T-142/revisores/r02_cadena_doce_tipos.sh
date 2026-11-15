#!/usr/bin/env bash
# QA r01 de T-142: la cadena A → B con los doce tipos activos en el Bloque A (más opciones enviables, más filas de la
# correspondencia en juego). Mock en los dos bloques, coste cero. Uso: r02_cadena_doce_tipos.sh <python> <carpeta_trabajo>
set -euo pipefail
PY="$1"; W="$2"
RAIZ="$(cd "$(dirname "$0")/../../../.." && pwd)"
mkdir -p "$W"
printf 'perfiles:\n  activos: [RV, RF, DIV, MP, IDX, FON, DER, INM, CRI, ALT, MON, TCV]\n' > "$W/doce_tipos.yaml"
set +e
"$PY" "$RAIZ/.docs/scripts/cadena_a_b.py" --trabajo "$W/cadena" --config-a "$W/doce_tipos.yaml" > "$W/salida.json" 2> "$W/errores.txt"
echo "código de salida: $?"
set -e
"$PY" - "$W/cadena/resumen.json" <<'PYEOF'
import json, sys
r = json.load(open(sys.argv[1], encoding="utf-8"))
print("enviables:", len(r.get("opciones_enviables", [])), "· enviadas:", len(r["envios"]), "· no enviadas:", len(r["no_enviadas"]))
for e in r["envios"]:
    print(" ", e["opp_id"], e["clave_universo"], e["admision"], e["estado_peticion"], e.get("veredicto"), "válido:", e.get("paquete_b_valido"), "RET:", (e.get("vuelta_a") or {}).get("ret_id"))
for n in r["no_enviadas"]:
    print("  no:", n["opp_id"], n["codigo"], n["detalle"][:90])
print("veredicto_cadena:", r.get("veredicto_cadena"))
PYEOF
