#!/usr/bin/env bash
# Añade una entrada al diario del mes (.docs/diario/AAAA-MM.md), la más reciente arriba.
# Uso: diario.sh "Título" [autor]
# Crea la plantilla con sus cuatro apartados; después se rellenan a mano.
source "$(dirname "$0")/common.sh"

titulo="${1:-}"; autor="${2:-}"
[[ -n "$titulo" ]] || fallo "uso: diario.sh \"Título\" [autor]"
archivo="$RAIZ/.docs/diario/$(mes).md"

TITULO="$titulo" AUTOR="$autor" HOY="$(hoy)" MES="$(mes)" "$PY" - "$archivo" <<'EOF'
import os, sys, pathlib
p = pathlib.Path(sys.argv[1])
cab = f"# Diario · {os.environ['MES']}\n\nUna entrada por día y tema, la más reciente arriba. Formato: `.docs/README.md`.\n"
texto = p.read_text(encoding="utf-8") if p.exists() else cab
autor = f" ({os.environ['AUTOR']})" if os.environ.get("AUTOR") else ""
entrada = (f"\n## {os.environ['HOY']} — {os.environ['TITULO']}{autor}\n\n"
           "**Resultado.** …\n\n**Causas y hallazgos.** …\n\n**Correcciones.** …\n\n**Operaciones y siguiente.** …\n")
# Insertar tras la cabecera (antes de la primera entrada existente).
i = texto.find("\n## ")
texto = texto.rstrip("\n") + "\n" + entrada if i == -1 else texto[:i] + "\n" + entrada.strip("\n") + "\n" + texto[i:]
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(texto, encoding="utf-8")
print(p)
EOF
