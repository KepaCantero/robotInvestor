#!/usr/bin/env bash
# Base común de todos los scripts de .docs/scripts/. Se carga con:
#   source "$(dirname "$0")/common.sh"
# Da modo estricto, la raíz del repo, las variables de .env (nunca secretos escritos en un script)
# y utilidades pequeñas.

set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS="$RAIZ/.docs/scripts"
LOGS="$SCRIPTS/.logs"            # ignorado por git
export RAIZ SCRIPTS LOGS

# Secretos y ajustes locales: SOLO desde .env en la raíz (ignorado por git). Plantilla: env.ejemplo.
if [[ -f "$RAIZ/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$RAIZ/.env"
  set +a
fi

fallo() { echo "ERROR: $*" >&2; exit 1; }
aviso() { echo "· $*" >&2; }

# requiere_var NOMBRE...  → falla si alguna variable no está definida en el entorno o en .env
requiere_var() {
  local v
  for v in "$@"; do
    [[ -n "${!v:-}" ]] || fallo "falta $v (defínela en $RAIZ/.env; plantilla en .docs/scripts/env.ejemplo)"
  done
}

# requiere_cmd comando...  → falla si algún comando no está instalado
requiere_cmd() {
  local c
  for c in "$@"; do
    command -v "$c" >/dev/null 2>&1 || fallo "falta el comando $c"
  done
}

# Python: el de la variable PY si viene dada; si no, el del venv del proyecto; si no, el del sistema.
if [[ -z "${PY:-}" ]]; then
  if [[ -x "$RAIZ/.venv/bin/python" ]]; then PY="$RAIZ/.venv/bin/python"; else PY="python3"; fi
fi
export PY

hoy() { date +%Y-%m-%d; }
mes() { date +%Y-%m; }
