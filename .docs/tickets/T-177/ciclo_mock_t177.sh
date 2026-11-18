#!/usr/bin/env bash
# T-177 · PB-58 de punta a punta con la CLI y el cliente simulado: C4 del BFA → CT-25 → ciclo degradado → depósito del
# Broker (fuera de banda, desde una variable de entorno) → segunda C4 sin CT-25 nuevo → ciclo sin la limitación → el valor
# no aparece en ningún archivo salvo `boveda/secretos.json`. Uso: .docs/tickets/T-177/ciclo_mock_t177.sh [carpeta de trabajo]
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/../../.." && pwd)"
# El .venv del repositorio principal (también desde un worktree); PY lo sustituye
PY="${PY:-$(git -C "$RAIZ" rev-parse --path-format=absolute --git-common-dir)/../.venv/bin/python}"
EJ="$RAIZ/bloque_a/11_Ejecutor"
T="${1:-$(mktemp -d)}"
mkdir -p "$T"
cat > "$T/c4.yaml" <<'EOF'
credenciales:
  servicios_bfa:
    - {servicio: "API de fondos cerrados", uso_previsto: "Cribado de FON", impacto_si_falta: "Datos públicos semanales"}
EOF
export T177_CLAVE="clave-ficticia-""ciclo-mock-177"
cli() { (cd "$EJ" && "$PY" -m bloque_a.cli --cliente mock --config "$T/c4.yaml" --datos ejemplos/datos_sinteticos \
         --estado "$T/estado" --salida "$T/salida" "$@"); }
cli --as-of 2024-03-01 credencial c4 > "$T/c4_1.json"
CRD="$("$PY" -c 'import json,sys; print(json.load(open(sys.argv[1]))["solicitudes"][0]["crd_id"])' "$T/c4_1.json")"
cli --as-of 2024-03-01 ciclo > "$T/ciclo_1.json"
cli --as-of 2024-03-01 credencial depositar --crd "$CRD" --valor-desde-entorno T177_CLAVE --caducidad 2027-12-31 > "$T/dep.json"
cli --as-of 2024-03-08 credencial c4 > "$T/c4_2.json"
cli --as-of 2024-03-08 ciclo > "$T/ciclo_2.json"
"$PY" - "$T" "$CRD" <<'EOF'
import json, os, sys
from pathlib import Path
t, crd = Path(sys.argv[1]), sys.argv[2]
valor = os.environ["T177_CLAVE"]
c1, c2 = json.loads((t / "c4_1.json").read_text()), json.loads((t / "c4_2.json").read_text())
assert c1["solicitudes"][0]["resultado"] == "SOLICITADA", c1
assert c2["solicitudes"] == [] and c2["servicios_revisados"][0]["estado"] == "PROVISTA", c2
def limitaciones(n):
    r = json.loads((t / f"ciclo_{n}.json").read_text())
    return json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))["limitaciones"]
assert [x for x in limitaciones(1) if crd in x], "el ciclo 1 no declara el servicio degradado"
assert not [x for x in limitaciones(2) if "API de fondos cerrados" in x], "el ciclo 2 sigue declarándolo"
malos = [str(p) for p in t.rglob("*") if p.is_file() and p.name != "secretos.json"
         and valor in p.read_text(encoding="utf-8", errors="ignore")]
assert not malos, malos
print(f"OK: {crd} solicitada en C4, degradada en el ciclo 1, provista y sin CT-25 nuevo en la C4 2; valor en ningún archivo")
EOF
