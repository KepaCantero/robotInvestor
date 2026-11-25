#!/usr/bin/env bash
# T-203, cierre: `revisores/r01_04_fusion_t201.sh` adaptado a T-201 ya integrado en develop (358576c3).
# Ya no hay fusión que resolver: comprueba que la copia está rebasada sobre origin/develop, que no quedan marcas de
# conflicto, que los envoltorios HT-02/03/07 son los de T-201 (T-203 ya no los cambia), las cuotas con las órdenes del
# gate (`revisores/r01_03_cuotas.sh`) frente a `tools/cuotas.txt` y las pruebas de los dos tickets.
# Uso: cierre_r01_04.sh <copia de wip/t203>   (SALIDA: carpeta para las salidas de r01_03; por defecto, una temporal)
set -u
C=$1
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$C" || exit 2
fallos=0
mal() { echo "FALLO: $*"; fallos=$((fallos + 1)); }

base=$(git merge-base HEAD origin/develop)
[ "$base" = "$(git rev-parse origin/develop)" ] && echo "rebasada sobre origin/develop $(git rev-parse --short origin/develop)" \
  || mal "no está rebasada: merge-base $base"
git merge-base --is-ancestor 358576c3 HEAD && echo "contiene T-201 (358576c3)" || mal "no contiene T-201"
if git merge-tree --write-tree --name-only origin/develop HEAD > /dev/null; then echo "merge-tree con origin/develop: limpio"
else mal "merge-tree con origin/develop con conflictos"; fi
if grep -rlE '^(<<<<<<<|>>>>>>>) ' bloque_a tools sistema_global .docs/tickets/T-203 2>/dev/null; then mal "marcas de conflicto"
else echo "sin marcas de conflicto"; fi
E=bloque_a/11_Ejecutor/bloque_a/herramientas
if git diff --quiet origin/develop -- "$E/ht02.py" "$E/ht03.py" "$E/ht07.py"; then echo "envoltorios HT-02/03/07: los de T-201"
else mal "los envoltorios difieren de develop"; fi
grep -q 'historia: Sequence\[float\] | np.ndarray) -> dict:' bloque_a/11_Ejecutor/bloque_a/motor/operaciones.py \
  && echo "posicion_historica: Sequence[float] | np.ndarray -> dict" || mal "firma de posicion_historica"

export SALIDA=${SALIDA:-$(mktemp -d)}
linea=$("$HERE/revisores/r01_03_cuotas.sh" "$C")
echo "$linea"
for clave in ruff mypy_bloque_a mypy_bloque_a_forex mypy_bloque_b; do
  medido=$(echo "$linea" | grep -oE "(^| )$clave=[0-9]+" | cut -d= -f2)
  cuota=$(grep -E "^$clave=" tools/cuotas.txt | cut -d= -f2)
  if [ -z "$cuota" ]; then echo "$clave: sin cuota (bloque retirado o línea borrada), medido ${medido:-—}"; continue; fi
  [ "$medido" = "$cuota" ] && echo "$clave: $medido = cuota" || mal "$clave: medido $medido, cuota $cuota"
done

cd bloque_a/11_Ejecutor || exit 2
r=$(../../.venv/bin/pytest -q -p no:cacheprovider tests/test_t201_cuotas.py tests/test_t203_cuotas.py 2>&1 | tail -1)
echo "pruebas de T-201 y T-203: $r"
echo "$r" | grep -qE "failed|error" && mal "pruebas"
echo "$r" | grep -qE "^[0-9]+ passed" || mal "pruebas sin resultado"

[ "$fallos" -eq 0 ] && echo "TODO BIEN" || echo "$fallos FALLOS"
exit $((fallos > 0))
