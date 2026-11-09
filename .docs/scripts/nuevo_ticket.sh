#!/usr/bin/env bash
# Crea la carpeta de un ticket a partir de la plantilla.
# Uso: nuevo_ticket.sh T-60 "Título del ticket" [pieza]
# El ID es el de la deuda técnica (T-xx): toda tarea tiene su fila allí antes de su ticket.
source "$(dirname "$0")/common.sh"

id="${1:-}"; titulo="${2:-}"; pieza="${3:-<bloque o módulo; una sola>}"
[[ "$id" =~ ^T-[0-9]+$ ]] || fallo "uso: nuevo_ticket.sh T-NN \"Título\" [pieza]"
[[ -n "$titulo" ]] || fallo "falta el título"

deuda="$RAIZ/sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md"
grep -q "^| $id |" "$deuda" || aviso "$id no está en la deuda técnica; añádelo allí también"

destino="$RAIZ/.docs/tickets/$id"
[[ ! -e "$destino" ]] || fallo "ya existe $destino (los tickets no se sobrescriben)"
cp -r "$RAIZ/.docs/tickets/_plantilla" "$destino"
rm -f "$destino/handoff.md"   # solo se crea si el trabajo cambia de manos (copiar de la plantilla)

TITULO="$titulo" PIEZA="$pieza" ID="$id" HOY="$(hoy)" "$PY" - "$destino" <<'EOF'
import os, sys, pathlib
d = pathlib.Path(sys.argv[1])
for f in d.glob("*.md"):
    t = f.read_text(encoding="utf-8").replace("T-xx", os.environ["ID"])
    t = t.replace("<título del ticket>", os.environ["TITULO"])
    if f.name == "README.md":
        t = t.replace("| Estado | ABIERTO · PLANIFICADO · EN CURSO · EN QA · CERRADO · BLOQUEADO (motivo) |", "| Estado | ABIERTO |")
        t = t.replace("<bloque o módulo; una sola>", os.environ["PIEZA"])
        t = t.replace("<Una línea por cambio de estado: AAAA-MM-DD · estado · quién · nota.>",
                      f"- {os.environ['HOY']} · ABIERTO · creado con nuevo_ticket.sh")
    f.write_text(t, encoding="utf-8")
EOF
echo "$destino"
