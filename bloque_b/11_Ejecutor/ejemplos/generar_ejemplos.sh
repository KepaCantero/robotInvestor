#!/usr/bin/env bash
# Regenera la salida simulada de ejemplos/ (cliente simulado, datos sintéticos, fecha de corte fija).
# Uso: bash ejemplos/generar_ejemplos.sh   (desde 11_Ejecutor; tarda menos de un minuto)
set -euo pipefail
cd "$(dirname "$0")/.."
BB="python3 -m bloque_b.cli"
S=ejemplos/salida_simulada
B=ejemplos/backtest_simulado
rm -rf "$S" "$B"
mkdir -p "$S/respuestas"
G="--estado $S/estado --salida $S/ENT --as-of 2026-11-03"

# 1. Petición N2 desde un paquete del Bloque A: la puerta PT30 la detiene en ejecución
$BB $G analizar --json ejemplos/peticiones/peticion_redes_bloque_a.json > "$S/respuestas/01_analizar_en_pausa.json"
AUT=$(python3 -c "import json;print(json.load(open('$S/respuestas/01_analizar_en_pausa.json'))['aut_id'])")
PET=$(python3 -c "import json;print(json.load(open('$S/respuestas/01_analizar_en_pausa.json'))['pet_id'])")
$BB $G estado --pet "$PET" > "$S/respuestas/02_estado_en_pausa.json"
# 2. El Broker autoriza continuar: se reanuda desde el punto de control y se entregan los seis entregables (V2.1:
#    capas 0-4 con PV1-PV3, mapa por eslabón, radar de emergentes y una consulta NO_BLOQUEANTE con supuesto aplicado)
$BB $G autorizar --aut "$AUT" --opcion CONTINUAR --decidido-por BROKER --motivo "Ampliación razonable" > "$S/respuestas/03_autorizar_continuar.json"
REC=$(python3 -c "import json;print(json.load(open('$S/respuestas/03_autorizar_continuar.json'))['rec_id'])")
# 3. Servicios posteriores
$BB $G vigia > "$S/respuestas/04_vigia.json"
$BB $G consulta "¿Qué parte de la cadena captura el valor del cuello de botella?" --contexto "$REC" > "$S/respuestas/05_consulta.json"
python3 - "$REC" "$S" <<'EOF'
import json, sys
rec, s = sys.argv[1], sys.argv[2]
d = {"decision_ambito": {"rec_id": rec, "decision": "CANDIDATOS_ENVIADOS_A_C", "motivo": "Ejemplo ficticio"},
     "valoracion_entregables": {"pet_id": rec.replace("REC-B-", "PET-B-"), "utilidad": 4, "comentario": "Ejemplo ficticio"}}
open("ejemplos/decision_ejemplo.json", "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
EOF
$BB $G decision --json ejemplos/decision_ejemplo.json > "$S/respuestas/06_decision.json"
$BB $G decision --json ejemplos/politica.json > "$S/respuestas/07_politica.json"
$BB $G estado --config > "$S/respuestas/08_estado_config.json"
$BB $G verificar-enlaces --max-fichas 20 > "$S/respuestas/09_verificar_enlaces_sin_red.json"
# 4. V2.1 · seguimiento encargado por el Broker (CT-B-29, archivo F11): alta, ciclo N1-SEG con informe y listado
python3 - "$REC" <<'EOF'
import json, sys
d = {"accion": "ALTA", "objeto": {"tipo": "AMBITO_ANALIZADO", "rec_id": sys.argv[1]}, "frecuencia": {"tipo": "MENSUAL"},
     "motivo": "Vigilar la cartera de pedidos y la valoración del ámbito (ejemplo ficticio)",
     "senales_de_interes": ["book-to-bill de los fabricantes de cable", "valoración relativa del ámbito"],
     "disparadores_broker": [{"descripcion": "book-to-bill inferior a 1 durante dos trimestres", "umbral": "1,0"}],
     "dimensiones_clave": ["D3", "D9"], "fecha_fin": "2027-11-03"}
open("ejemplos/seguimiento_ejemplo.json", "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
EOF
$BB $G seguimiento alta --json ejemplos/seguimiento_ejemplo.json > "$S/respuestas/10_seguimiento_alta.json"
SEG=$(python3 -c "import json;print(json.load(open('$S/respuestas/10_seguimiento_alta.json'))['seg_id'])")
$BB $G seguimiento ciclo --seg "$SEG" > "$S/respuestas/11_seguimiento_ciclo.json"
$BB $G seguimiento listar > "$S/respuestas/12_seguimiento_listar.json"
# 5. V2.1 · consultas al Broker (CT-B-28): listado y aporte entrante del Broker
$BB $G consulta-broker listar > "$S/respuestas/13_consultas_broker.json"
$BB $G consulta-broker aporte --json ejemplos/aporte_ejemplo.json > "$S/respuestas/14_aporte_broker.json"
# 6. V2.1 · parada en PV1 (ningún tipo admitido con instrumentos invertibles): informe de parada
$BB $G analizar --json ejemplos/peticiones/peticion_parada_pv1.json > "$S/respuestas/15_analizar_parada_pv1.json"

# Solo se conserva el punto de control de la pausa (los demás se regeneran al ejecutar)
find "$S/estado/puntos_control" -name 'CKP-*.json' ! -name "$(python3 -c "import json;print(json.load(open('$S/respuestas/01_analizar_en_pausa.json'))['checkpoint_id'])").json" -delete

# 7. Backtest: selección determinista (24 fechas) y completo con agentes simulados (3 fechas)
mkdir -p "$B/solo_seleccion" "$B/completo"
$BB --estado "$B/estado_seleccion" --salida "$B/solo_seleccion" backtest --peticion ejemplos/peticiones/peticion_redes_bloque_a.json \
    --desde 2023-01-01 --hasta 2024-12-31 --frecuencia mensual --solo-seleccion > "$B/solo_seleccion/resultado.json"
$BB --estado "$B/estado_completo" --salida "$B/completo" backtest --peticion ejemplos/peticiones/peticion_redes_bloque_a.json \
    --desde 2025-01-01 --hasta 2025-03-31 --frecuencia mensual > "$B/completo/resultado.json"
rm -rf "$B/estado_seleccion" "$B/estado_completo"
echo "Ejemplos regenerados en $S y $B"
