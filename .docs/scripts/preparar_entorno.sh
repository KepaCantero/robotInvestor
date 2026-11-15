#!/usr/bin/env bash
# Crea o comprueba el entorno del proyecto (.venv) con las versiones fijadas en tools/requisitos_entorno.txt (T-96).
# Uso: preparar_entorno.sh              crea .venv si no existe, instala los tres ejecutores y las herramientas, y comprueba
#      preparar_entorno.sh --comprobar  solo compara lo instalado en .venv con el fichero
# Python: el de PYTHON_ENTORNO, o python3.12 del PATH, o ~/.local/bin/python3.12. Tiene que ser 3.12.
# Falla cerrado: si falta Python 3.12, si pip no instala una versión fijada o si lo instalado no coincide.
source "$(dirname "$0")/common.sh"

solo_comprobar=0
[[ $# -le 1 ]] || fallo "uso: preparar_entorno.sh [--comprobar]"   # T-137 (H-06): ningún argumento de más
case "${1:-}" in
  "") ;;
  --comprobar) solo_comprobar=1 ;;
  *) fallo "uso: preparar_entorno.sh [--comprobar]" ;;
esac

cd "$RAIZ"
REQ="tools/requisitos_entorno.txt"
VENV="$RAIZ/.venv"
[[ -f "$REQ" ]] || fallo "no existe $REQ"

# T-137 (H-01, H-02): un .venv que ya existe se valida ANTES de tocarlo: Python 3.12 y pip que funciona. Si no, se para y se
# dice cómo salir; nunca se instala en un entorno de otro Python ni se reutiliza uno a medias.
valida_venv() {
  local v
  v="$("$VENV/bin/python" -c 'import sys; print("%d.%d" % sys.version_info[:2])' 2>/dev/null)" \
    || fallo "$VENV está roto (su Python no arranca): bórralo (rm -rf .venv) y vuelve a ejecutar este script"
  [[ "$v" == "3.12" ]] || fallo "$VENV usa Python $v; el proyecto usa 3.12: bórralo (rm -rf .venv) y vuelve a ejecutar este script"
  "$VENV/bin/python" -m pip --version >/dev/null 2>&1 \
    || fallo "$VENV está a medias (no tiene pip; p. ej., falta el paquete python3.12-venv del sistema): bórralo (rm -rf .venv), instala lo que falte y vuelve a ejecutar este script"
}

comprobar() {
  [[ -x "$VENV/bin/python" ]] || fallo "no hay entorno en $VENV (ejecuta este script sin --comprobar)"
  valida_venv
  "$VENV/bin/python" -m pip freeze --exclude-editable 2>/dev/null | "$VENV/bin/python" -I -c '
import re, sys
def norma(n): return re.sub(r"[-_.]+", "-", n).lower()
def lee(lineas, origen):
    d = {}
    for l in lineas:
        l = re.sub(r"\s+#.*$", "", l).strip()   # T-137 (H-05): un comentario al final de la línea, como lo lee pip
        if not l or l.startswith("#"): continue
        m = re.fullmatch(r"([A-Za-z0-9][A-Za-z0-9._-]*)==([^=\s][^\s]*)", l)
        if not m: sys.exit(f"línea sin una versión exacta «paquete==versión» {origen}: {l}")
        n = norma(m.group(1))
        if n in d: sys.exit(f"{m.group(1)} está repetido {origen}")
        d[n] = m.group(2)
    return d
fijado = lee(open(sys.argv[1], encoding="utf-8"), "en el fichero de versiones")
instalado = lee(sys.stdin, "en lo instalado (pip freeze)")
mal = []
for n, v in sorted(fijado.items()):
    if n not in instalado: mal.append(f"falta {n}=={v}")
    elif instalado[n] != v: mal.append(f"{n}: instalado {instalado[n]}, fijado {v}")
for n in sorted(set(instalado) - set(fijado)):   # T-137 (H-03): un paquete sin fijar es un error, no un aviso
    mal.append(f"{n}=={instalado[n]} está instalado y no está fijado en el fichero")
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
  if [[ -n "$py" && "$py" != */* ]]; then py="$(command -v "$py" || true)"; fi   # T-137 (H-06): un nombre del PATH
  if [[ -z "$py" ]]; then
    if command -v python3.12 >/dev/null 2>&1; then py="$(command -v python3.12)"
    elif [[ -x "$HOME/.local/bin/python3.12" ]]; then py="$HOME/.local/bin/python3.12"
    fi
  fi
  [[ -n "$py" && -x "$py" ]] || fallo "no encuentro Python 3.12 (instálalo o indica su ruta en PYTHON_ENTORNO)"
  v="$("$py" -c 'import sys; print("%d.%d" % sys.version_info[:2])')" || fallo "no puedo ejecutar $py"
  [[ "$v" == "3.12" ]] || fallo "$py es Python $v; el proyecto usa 3.12"
  aviso "creando $VENV con $py"
  if ! "$py" -m venv "$VENV"; then
    rm -rf "$VENV"   # lo acaba de crear este script: no se deja un entorno a medias (T-137, H-01)
    fallo "no se pudo crear el entorno (en Debian y Ubuntu suele faltar el paquete python3.12-venv)"
  fi
fi
valida_venv

aviso "instalando los tres ejecutores y las herramientas con las versiones de $REQ"
"$VENV/bin/python" -m pip install -q -c "$REQ" \
  -e bloque_a/11_Ejecutor -e bloque_a_forex/11_Ejecutor -e bloque_b/11_Ejecutor \
  arch openpyxl python-docx ruff mypy pytest pyyaml jsonschema \
  || fallo "pip no pudo instalar las versiones fijadas"
comprobar
