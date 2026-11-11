#!/usr/bin/env bash
# Crea o comprueba el entorno del proyecto (.venv) con las versiones fijadas en tools/requisitos_entorno.txt (T-96).
# Uso: preparar_entorno.sh              crea .venv si no existe, instala los tres ejecutores y las herramientas, y comprueba
#      preparar_entorno.sh --comprobar  solo compara lo instalado en .venv con el fichero
# Python: el de PYTHON_ENTORNO, o python3.12 del PATH, o ~/.local/bin/python3.12. Tiene que ser 3.12.
# Falla cerrado: si falta Python 3.12, si pip no instala una versión fijada o si lo instalado no coincide.
source "$(dirname "$0")/common.sh"

solo_comprobar=0
case "${1:-}" in
  "") ;;
  --comprobar) solo_comprobar=1 ;;
  *) fallo "uso: preparar_entorno.sh [--comprobar]" ;;
esac

cd "$RAIZ"
REQ="tools/requisitos_entorno.txt"
VENV="$RAIZ/.venv"
[[ -f "$REQ" ]] || fallo "no existe $REQ"

comprobar() {
  [[ -x "$VENV/bin/python" ]] || fallo "no hay entorno en $VENV (ejecuta este script sin --comprobar)"
  local v
  v="$("$VENV/bin/python" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
  [[ "$v" == "3.12" ]] || fallo "el entorno usa Python $v; el proyecto usa 3.12"
  "$VENV/bin/pip" freeze --exclude-editable 2>/dev/null | "$VENV/bin/python" -I -c '
import re, sys
def norma(n): return re.sub(r"[-_.]+", "-", n).lower()
def lee(lineas):
    d = {}
    for l in lineas:
        l = l.strip()
        if not l or l.startswith("#"): continue
        if "==" not in l: sys.exit(f"línea sin versión exacta en el fichero: {l}")
        n, v = l.split("==", 1); d[norma(n)] = v.strip()
    return d
fijado = lee(open(sys.argv[1], encoding="utf-8"))
instalado = lee(sys.stdin)
mal = []
for n, v in sorted(fijado.items()):
    if n not in instalado: mal.append(f"falta {n}=={v}")
    elif instalado[n] != v: mal.append(f"{n}: instalado {instalado[n]}, fijado {v}")
for n in sorted(set(instalado) - set(fijado)):
    print(f"· aviso: {n}=={instalado[n]} instalado y no fijado", file=sys.stderr)
if mal:
    print("ERROR: el entorno no coincide con el fichero de versiones:", file=sys.stderr)
    for m in mal: print("  - " + m, file=sys.stderr)
    sys.exit(1)
print(f"entorno conforme: {len(fijado)} paquetes con la versión fijada")
' "$REQ"
}

if [[ $solo_comprobar -eq 1 ]]; then comprobar; exit 0; fi

if [[ ! -x "$VENV/bin/python" ]]; then
  py="${PYTHON_ENTORNO:-}"
  if [[ -z "$py" ]]; then
    if command -v python3.12 >/dev/null 2>&1; then py="$(command -v python3.12)"
    elif [[ -x "$HOME/.local/bin/python3.12" ]]; then py="$HOME/.local/bin/python3.12"
    fi
  fi
  [[ -n "$py" && -x "$py" ]] || fallo "no encuentro Python 3.12 (instálalo o indica su ruta en PYTHON_ENTORNO)"
  v="$("$py" -c 'import sys; print("%d.%d" % sys.version_info[:2])')" || fallo "no puedo ejecutar $py"
  [[ "$v" == "3.12" ]] || fallo "$py es Python $v; el proyecto usa 3.12"
  aviso "creando $VENV con $py"
  "$py" -m venv "$VENV" || fallo "no se pudo crear el entorno"
fi

aviso "instalando los tres ejecutores y las herramientas con las versiones de $REQ"
"$VENV/bin/pip" install -q -c "$REQ" \
  -e bloque_a/11_Ejecutor -e bloque_a_forex/11_Ejecutor -e bloque_b/11_Ejecutor \
  arch openpyxl python-docx ruff mypy pytest pyyaml jsonschema \
  || fallo "pip no pudo instalar las versiones fijadas"
comprobar
