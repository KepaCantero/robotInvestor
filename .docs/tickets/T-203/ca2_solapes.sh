#!/usr/bin/env bash
# T-203, cierre (H-01 de la QA r01): CA-2, ficheros de T-203 (commits sobre origin/develop, cambios y no seguidos)
# frente a los de las otras ramas y tickets. Uso: ca2_solapes.sh <copia de wip/t203>
cd "$1" || exit 2
L=$(mktemp)
git diff --name-only origin/develop > "$L"
git diff --name-only origin/develop HEAD >> "$L"
git ls-files --others --exclude-standard >> "$L"
M=$(sort -u "$L")
echo "T-203 toca $(echo "$M" | wc -l) ficheros"
comun() { echo "== $1"; comm -12 <(echo "$M") <(sort -u) | sed 's/^/   /'; }
git diff --name-only origin/develop...origin/astra/encargos-bloque-a-c38-c47 | comun "PR 3 de Astra (origin/develop...origin/astra/encargos-bloque-a-c38-c47, $(git rev-parse --short origin/astra/encargos-bloque-a-c38-c47))"
git diff --name-only origin/develop...wip/t196 | comun "T-196 pendiente (origin/develop...wip/t196; ya integrado en be35f28e)"
git diff --name-only be35f28e^ be35f28e | comun "T-196 integrado (be35f28e)"
git diff --name-only 358576c3^ 358576c3 | comun "T-201 integrado (358576c3)"
git diff --name-only origin/develop...wip/t204 | comun "T-204 (origin/develop...wip/t204, $(git rev-parse --short wip/t204))"
grep -E '^[0-9a-f]{64}  ' tools/corpus_manifest.txt | awk '{print $2}' | comun "corpus congelado (tools/corpus_manifest.txt)"
