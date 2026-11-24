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

# Autores genéricos (operador, 24-11-2026: «Usa un autor genérico»). El repositorio es público: ningún commit lleva un
# nombre, un correo o un equipo personal. Lista cerrada de pares «Nombre <correo>»; lo que no está, no se acepta.
AUTORES_GENERICOS=("Astra <astra@users.noreply.github.com>" "Claude <noreply@anthropic.com>")

# autor_efectivo → «Nombre <correo>» con el que saldría el commit (GIT_AUTOR_* de .env o del entorno; si no, git).
autor_efectivo() {
  local n e
  n="${GIT_AUTOR_NOMBRE:-}"; e="${GIT_AUTOR_EMAIL:-}"
  [[ -n "$n" ]] || n="$(git -C "$RAIZ" config user.name 2>/dev/null || true)"
  [[ -n "$e" ]] || e="$(git -C "$RAIZ" config user.email 2>/dev/null || true)"
  printf '%s <%s>' "$n" "$e"
}

# requiere_autor_generico → falla si el autor efectivo no es uno de AUTORES_GENERICOS.
requiere_autor_generico() {
  local a g
  a="$(autor_efectivo)"
  for g in "${AUTORES_GENERICOS[@]}"; do [[ "$a" == "$g" ]] && return 0; done
  fallo "el autor del commit no es genérico. Pon GIT_AUTOR_NOMBRE y GIT_AUTOR_EMAIL en .env con uno de: ${AUTORES_GENERICOS[*]} (repositorio público: nada de nombres ni correos personales)"
}

hoy() { date +%Y-%m-%d; }
mes() { date +%Y-%m; }
