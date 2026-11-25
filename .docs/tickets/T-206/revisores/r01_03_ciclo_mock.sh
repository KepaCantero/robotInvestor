#!/usr/bin/env bash
# QA r01 de T-206 (revisor independiente): ciclo mock de punta a punta por la CLI, con la configuración por defecto tal cual,
# con datos malos (un cierre negativo en EURUSD=X, el último antes de as_of) y un almacén que ya trae INC- de
# tipo DATOS (de antes de T-206). Comprueba: el ciclo termina, todas las INC- nuevas llevan un tipo del esquema de HA (4.8), las
# de datos son OTRO con `categoria` DATOS, las antiguas siguen ahí sin tocar, `estado` se lee y el almacén queda íntegro.
# Uso: r01_03_ciclo_mock.sh <copia_de_trabajo>   (trabaja en una carpeta temporal nueva; no escribe en la copia)
set -euo pipefail
COPIA="$(cd "$1" && pwd)"
EJ="$COPIA/bloque_a/11_Ejecutor"
PY="$COPIA/.venv/bin/python"
TRAB="$(mktemp -d "${TMPDIR:-/tmp}/qa_t206_r01_03.XXXX")"
echo "carpeta de trabajo: $TRAB"
cp -r "$EJ/ejemplos/datos_sinteticos" "$TRAB/datos"
# Datos malos: un cierre negativo en un símbolo de DIV (el ciclo por defecto analiza DIV), el último antes de as_of
"$PY" -I - "$TRAB/datos" <<'EOF'
import csv, sys
from pathlib import Path
d = Path(sys.argv[1])
for nombre, valor in (("EURUSD=X.csv", "-1.0"),):
    p = d / nombre
    filas = list(csv.reader(p.open(encoding="utf-8")))
    i = max(k for k, f in enumerate(filas[1:], 1) if f[0] < "2026-06-05")   # el último cierre antes de as_of
    filas[i][4] = valor
    with p.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(filas)
EOF
# Almacén con dos INC- antiguas (tipo DATOS), escritas como las escribía el ejecutor de antes de T-206
cd "$EJ"
export PYTHONPATH="$EJ" PYTHONHASHSEED=0
"$PY" - "$TRAB/estado" <<'EOF'
import sys
from bloque_a.almacen import Almacen, Reloj
# Ronda de cierre (implementador, T-206 H-04): `escribir` ya rechaza una INC- con DATOS; se monta como lo dejaba el ejecutor
# de antes de T-206, con la comprobación desactivada solo en este proceso de montaje
Almacen._comprobar_tipo_incidencia = staticmethod(lambda tipo, extra=None: None)
a = Almacen(sys.argv[1], Reloj()); a.reloj.fijar("2026-05-29")
for n, esc in ((1, False), (2, True)):
    a.escribir("HA", "AG-18", {"tipo_entrada": "INC", "id": a.nuevo_id("INC"), "tipo": "DATOS", "severidad": "Operativa",
                               "objeto": "AG-01", "detalle": f"antigua {n}", "tratamiento": "registrada", "escalado_operador": esc})
EOF
G=(--cliente mock --datos "$TRAB/datos" --universo config/universo_ejemplo.csv --estado "$TRAB/estado" --salida "$TRAB/entregables")
"$PY" -m bloque_a.cli "${G[@]}" --as-of 2026-06-05 ciclo > "$TRAB/ciclo.out" 2> "$TRAB/ciclo.err" || { echo "ciclo rc=$?"; tail -5 "$TRAB/ciclo.err"; exit 1; }
"$PY" -m bloque_a.cli "${G[@]}" --as-of 2026-06-05 estado > "$TRAB/estado.out" 2> "$TRAB/estado.err" || { echo "estado rc=$?"; tail -5 "$TRAB/estado.err"; exit 1; }
"$PY" - "$TRAB" <<'EOF'
import json, sys
from pathlib import Path
from bloque_a.almacen import TIPOS_INCIDENCIA, Almacen, Reloj, es_incidencia_de_datos
t = Path(sys.argv[1])
a = Almacen(t / "estado", Reloj())
incs = [e for e in a.leer("HA") if e.get("tipo_entrada") == "INC"]
fallos = []
antiguas, nuevas = incs[:2], incs[2:]
if [e["tipo"] for e in antiguas] != ["DATOS", "DATOS"]:
    fallos.append("las antiguas cambiaron")
fuera = [(e["id"], e["tipo"]) for e in nuevas if e["tipo"] not in TIPOS_INCIDENCIA]
if fuera:
    fallos.append(f"tipos fuera del esquema: {fuera}")
datos = [e for e in nuevas if es_incidencia_de_datos(e)]
if not datos or any(e["tipo"] != "OTRO" or e.get("categoria") != "DATOS" for e in datos):
    fallos.append(f"incidencias de datos mal formadas: {[(e['id'], e['tipo'], e.get('categoria')) for e in datos]}")
objetos = {e.get("objeto") for e in datos}
for esperado in ("EURUSD=X",):
    if esperado not in objetos:
        fallos.append(f"falta la incidencia de datos de {esperado}")
if not all(a.verificar_integridad().values()):
    fallos.append("almacén no íntegro")
est = json.loads((t / "estado.out").read_text(encoding="utf-8"))
escaladas = [(e["tipo"], e["detalle"]) for e in est["incidencias_escaladas"]]
if ("DATOS", "antigua 2") not in escaladas:
    fallos.append("estado no muestra la escalada antigua")
print(f"INC- antiguas {len(antiguas)}, nuevas {len(nuevas)} ({len(datos)} de datos; tipos {sorted({e['tipo'] for e in nuevas})})")
print(f"objetos de las de datos: {sorted(map(str, objetos))}")
print(f"escaladas en estado: {escaladas}")
print("RESULTADO:", "OK" if not fallos else f"FALLO {fallos}")
sys.exit(1 if fallos else 0)
EOF
