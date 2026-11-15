#!/usr/bin/env bash
# T-146 · tres ciclos simulados (cliente mock) con el código de antes y el de después, en la misma ruta, y su diferencia.
# Uso: comparar_ciclos.sh <11_Ejecutor de antes> <11_Ejecutor de después> <carpeta temporal> [python]
# El de antes se saca, por ejemplo, con: git archive <commit> bloque_a | tar -x -C <carpeta>
# Escenarios: «div» (ciclo del 29-03-2024, configuración por defecto: solo divisas, modo vivo), «bt» (backtest del 05-01 al
# 29-03-2024) y «doce» (ciclo con los 12 tipos). Las rutas de salida son las mismas en las dos pasadas porque el estado las
# guarda. Imprime los ficheros que difieren y, de F5, los campos que cambian por RUN.
set -euo pipefail
ANTES=$(cd "$1" && pwd); DESPUES=$(cd "$2" && pwd); TMP=$(mkdir -p "$3" && cd "$3" && pwd); PY=${4:-python3}
cat > "$TMP/correr.py" <<'PYEOF'
import contextlib, io, os, sys
S = os.path.abspath(sys.argv[2]); ej = os.path.abspath(sys.argv[1]); os.chdir(ej); sys.path.insert(0, ej)
from bloque_a import cli
with contextlib.redirect_stdout(io.StringIO()):
    cli.main(["--cliente", "mock", "--datos", "ejemplos/datos_sinteticos", "--estado", S + "/estado", "--salida", S + "/salida"] + sys.argv[3:])
PYEOF
printf 'perfiles: {activos: [RV, RF, DIV, MP, INM, CRI, ALT, IDX, FON, DER, MON, TCV]}\n' > "$TMP/doce.yaml"
for n in antes despues; do
  d=$ANTES; [[ $n == despues ]] && d=$DESPUES
  rm -rf "$TMP/run" "$TMP/$n"
  "$PY" "$TMP/correr.py" "$d" "$TMP/run/div" --as-of 2024-03-29 ciclo
  "$PY" "$TMP/correr.py" "$d" "$TMP/run/bt" backtest --desde 2024-01-05 --hasta 2024-03-29 > /dev/null
  "$PY" "$TMP/correr.py" "$d" "$TMP/run/doce" --as-of 2024-03-29 --config "$TMP/doce.yaml" ciclo
  mv "$TMP/run" "$TMP/$n"
done
echo "== ficheros que difieren (consumo.csv y cache_resultados.jsonl cambian también entre dos pasadas iguales: latencias y orden)"
diff -rq "$TMP/antes" "$TMP/despues" || true
echo "== F5: campos que cambian por RUN (sin _hash, _hash_prev, _ts ni fecha_entrega)"
"$PY" - "$TMP" <<'PYEOF'
import json, sys, pathlib
t = pathlib.Path(sys.argv[1])
for f in sorted((t / "antes").rglob("F5_historial_analisis.jsonl")):
    g = t / "despues" / f.relative_to(t / "antes")
    a = [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines()]
    b = [json.loads(x) for x in g.read_text(encoding="utf-8").splitlines()]
    for x, y in zip(a, b):
        for k in sorted(set(x) | set(y)):
            if k not in ("_hash", "_hash_prev", "_ts", "fecha_entrega") and x.get(k) != y.get(k):
                print(f"  {f.relative_to(t / 'antes').parts[0]} {x.get('id')} {k}: {json.dumps(x.get(k), ensure_ascii=False)[:160]}"
                      f"  →  {json.dumps(y.get(k), ensure_ascii=False)[:160]}")
PYEOF
