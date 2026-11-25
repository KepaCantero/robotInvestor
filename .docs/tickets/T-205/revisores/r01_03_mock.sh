#!/bin/bash
# QA r01 de T-205 (revisor): backtest del README, ciclo C1 mock, alta y C6 de seguimiento por la CLI en un árbol, con la salida
# siempre en la MISMA carpeta ($2/out) para poder comparar dos árboles byte a byte; después se mueve a $2/<etiqueta>.
# Pasos extra (5-7): F3 estropeado a mano (clase = una marca), alta por la CLI y C6 de un encargo con la clase estropeada.
# Uso: r01_03_mock.sh <árbol> <carpeta> <etiqueta>
set -u
cd "$1/bloque_a/11_Ejecutor" || exit 1
O="$2/out"; rm -rf "$O" "$2/$3"; mkdir -p "$O"
PY=../../.venv/bin/python
C=($PY -m bloque_a.cli --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv)
"${C[@]}" --salida "$O/bt" backtest --desde 2024-01-05 --hasta 2024-03-29 > "$O/1_bt.log" 2>&1; echo "1 backtest rc=$?"
"${C[@]}" --estado "$O/estado" --salida "$O/ent" --as-of 2024-03-29 ciclo > "$O/2_ciclo.log" 2>&1; echo "2 ciclo rc=$?"
"${C[@]}" --estado "$O/estado" --salida "$O/ent" --as-of 2024-03-29 seguimiento alta --json '{"opp_id":"OPP-2024-0001","frecuencia":"SEMANAL","motivo":"mock"}' > "$O/3_alta.log" 2>&1; echo "3 alta rc=$?"
"${C[@]}" --estado "$O/estado" --salida "$O/ent" --as-of 2024-04-05 seguimiento ejecutar > "$O/4_c6.log" 2>&1; echo "4 c6 rc=$?"
cp -r "$O/estado" "$O/estado_tras_4"
M="MARCA""_T205_""CLI"
$PY -I -c "
import sys; sys.path.insert(0, '.')
from bloque_a.almacen import Almacen
a = Almacen('$O/estado'); a.reloj.fijar('2024-04-05')
for o in ('OPP-2024-0001', 'OPP-2024-0002'):
    a.escribir('F3', 'AG-02', {'tipo_entrada': 'ACTUALIZACION', 'opp_id': o, 'clase': '$M'})
"
"${C[@]}" --estado "$O/estado" --salida "$O/ent" --as-of 2024-04-05 seguimiento alta --json '{"opp_id":"OPP-2024-0002","frecuencia":"SEMANAL","motivo":"mock"}' > "$O/5_alta_mala.log" 2>&1; echo "5 alta con clase estropeada rc=$?"
"${C[@]}" --estado "$O/estado" --salida "$O/ent" --as-of 2024-04-12 seguimiento ejecutar > "$O/6_c6_malo.log" 2>&1; echo "6 c6 con clase estropeada rc=$?"
"${C[@]}" --estado "$O/estado" --salida "$O/ent" --as-of 2024-04-13 seguimiento ejecutar > "$O/7_c6_malo_dia2.log" 2>&1; echo "7 c6 al día siguiente rc=$?"
echo "marca fuera de F3: $(grep -rl "$M" "$O" | grep -v '/F3_' | grep -v 'estado_tras_4' | tr '\n' ' ')"
mv "$O" "$2/$3"
