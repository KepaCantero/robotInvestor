#!/usr/bin/env bash
# Crea una entrada de memoria con su cabecera y la añade al índice de su carpeta.
# Uso: memoria.sh <carpeta> <tema-corto> <tipo> "<resumen de una línea>" [--autor X] [--sustituye <id>]
#   carpeta: compartida | claude | astra | … (si no existe, se crea con su INDICE.md)
#   tipo:    estado | decision | regla | leccion | convencion | traspaso | contexto
#   --sustituye: marca la entrada anterior como sustituida (en su archivo y en su índice)
# Después, se escribe el contenido de la entrada a mano. Protocolo: .docs/memoria/LEEME.md
source "$(dirname "$0")/common.sh"

carpeta="${1:-}"; tema="${2:-}"; tipo="${3:-}"; resumen="${4:-}"
[[ -n "$carpeta" && -n "$tema" && -n "$tipo" && -n "$resumen" ]] || fallo "uso: memoria.sh <carpeta> <tema-corto> <tipo> \"<resumen>\" [--autor X] [--sustituye <id>]"
shift 4
autor=""; sustituye=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --autor) autor="${2:-}"; shift 2 ;;
    --sustituye) sustituye="${2:-}"; shift 2 ;;
    *) fallo "opción desconocida: $1" ;;
  esac
done
[[ "$tema" =~ ^[a-z0-9-]+$ ]] || fallo "el tema va en minúsculas con guiones (p. ej. lecciones-marco-c)"
case "$tipo" in estado|decision|regla|leccion|convencion|traspaso|contexto) ;; *) fallo "tipo no válido: $tipo" ;; esac
if [[ -z "$autor" ]]; then
  [[ "$carpeta" != "compartida" ]] || fallo "en compartida hay que indicar --autor"
  autor="$carpeta"
fi

CARPETA="$carpeta" TEMA="$tema" TIPO="$tipo" RESUMEN="$resumen" AUTOR="$autor" SUST="$sustituye" HOY="$(hoy)" \
"$PY" - "$RAIZ/.docs/memoria" <<'EOF'
import os, sys, pathlib, re
base = pathlib.Path(sys.argv[1]); e = os.environ
d = base / e["CARPETA"]
indice = d / "INDICE.md"
if not d.exists():
    d.mkdir(parents=True)
    indice.write_text(f"# Índice · memoria de {e['CARPETA']}\n\n| id | tipo | resumen | vigencia |\n| --- | --- | --- | --- |\n", encoding="utf-8")
nid = f"{e['CARPETA']}/{e['HOY']}_{e['TEMA']}"
arch = d / f"{e['HOY']}_{e['TEMA']}.md"
if arch.exists():
    sys.exit(f"ERROR: ya existe {arch} (las entradas no se reescriben: crea otra y usa --sustituye)")
nota = f"Sustituye a `{e['SUST']}`.\n\n" if e.get("SUST") else ""
arch.write_text(
    f"---\nid: {nid}\nautor: {e['AUTOR']}\nfecha: {e['HOY']}\ntipo: {e['TIPO']}\netiquetas: []\n"
    f"fuente: <commit, ruta del repo o enlace>\nvigencia: vigente\n---\n\n{nota}<Contenido: el hecho, por qué importa y cómo aplicarlo.>\n",
    encoding="utf-8")
with indice.open("a", encoding="utf-8") as f:
    f.write(f"| {nid} | {e['TIPO']} | {e['RESUMEN']} | vigente |\n")
if e.get("SUST"):
    old_dir, old_name = e["SUST"].split("/", 1)
    old = base / old_dir / f"{old_name}.md"
    if not old.exists():
        sys.exit(f"ERROR: no existe la entrada a sustituir {old}")
    t = old.read_text(encoding="utf-8")
    t = re.sub(r"^vigencia: .*$", f"vigencia: sustituida por {nid}", t, count=1, flags=re.M)
    old.write_text(t, encoding="utf-8")
    oi = base / old_dir / "INDICE.md"
    lines = oi.read_text(encoding="utf-8").split("\n")
    lines = [re.sub(r"\| [^|]* \|$", f"| sustituida por {nid} |", l) if l.startswith(f"| {e['SUST']} |") else l for l in lines]
    oi.write_text("\n".join(lines), encoding="utf-8")
print(arch)
EOF
