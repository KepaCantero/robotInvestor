#!/bin/bash
# ===========================================
# check_all.sh - QA completo del repo (solo lectura)
# ===========================================
# Es EL script de calidad del repo (adaptación del check_all de robotTrading
# a un monorepo de corpus canónico + ejecutores entregados).
#
# Uso:
#   ./tools/check_all.sh                 # todos los gates (reporte)
#   ./tools/check_all.sh --core          # solo corpus+config+tests (rápido)
#   ./tools/check_all.sh --strict        # corta en el primer fallo (CI)
#   ./tools/check_all.sh --update-corpus # re-congelar el corpus (SOLO deliberado:
#                                        # mismo commit que el cambio + motivo)
#
# Gates:
#   1. corpus-integridad   (goldens de robotTrading adaptados: el corpus .md
#                           congelado por hash; re-congelado deliberado)
#   2. nombres-nfc         (lección macOS: NFD rompe los tests)
#   3. yaml-configs        (los 3 por_defecto.yaml parsean)
#   4. secrets             (repo público; allowlist explícita)
#   5. refs-vivas          (rutas citadas en CLAUDE.md/prompts/docs existen —
#                           antídoto contra planes rancios)
#   6. ruff (cuota)        (código entregado no era ruff-limpio: ratchet)
#   7-9. mypy (cuota ×3)   (ídem; las cuotas solo bajan)
#   10-12. pytest ×3       (con línea base: >= 117 / 68 / 141; ver tools/cuotas.txt)
#
# Retirados conscientemente (y por qué): ruff-format y format-check (reescribiría
# 3.100 líneas de código entregado antes de tiempo), vulture (falso positivo
# estructural con params — trampa conocida de robotTrading), radon (sin acción
# asociada), vale (era para docs ELI5 en inglés; el corpus es es-ES canónico e
# intocable), pylint (ruff ya cubre E/F aquí).
# ===========================================

set -uo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

if [ -f .venv/bin/activate ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi
PY=".venv/bin/python"
EJECUTORES=(bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor)
PAQUETES=(bloque_a bloque_a_forex bloque_b)

CORE_ONLY=false
STRICT_MODE=false
UPDATE_CORPUS=false
for arg in "$@"; do
    case $arg in
        --core)   CORE_ONLY=true ;;
        --strict) STRICT_MODE=true ;;
        --update-corpus) UPDATE_CORPUS=true ;;
        -h|--help) grep '^# ' "$0" | cut -c3-; exit 0 ;;
        *) echo "Opción desconocida: $arg (usa -h)"; exit 1 ;;
    esac
done

TOTAL=0; PASSED=0; FAILED=0; SKIPPED=0

section() {
    echo -e "\n${CYAN}╔════════════════════════════════════════════════════════╗"
    echo -e "║  $1"
    echo -e "╚════════════════════════════════════════════════════════╝${NC}"
}

run_check() {
    local name="$1"; shift
    ((TOTAL++))
    echo -e "${YELLOW}>>> $name${NC}"
    if "$@"; then
        echo -e "${GREEN}✓ $name${NC}"; ((PASSED++))
    elif [ "$STRICT_MODE" = true ]; then
        echo -e "${RED}✗ $name falló (modo estricto)${NC}"; ((FAILED++)); exit 1
    else
        echo -e "${RED}✗ $name${NC}"; ((FAILED++))
    fi
}

cuota() { grep -E "^$1=" tools/cuotas.txt | head -1 | cut -d= -f2; }

# gate_cuota <nombre> <cuota_actual> <cuota_congelada>
gate_cuota() {
    local nombre="$1" actual="$2" congelada="$3"
    ((TOTAL++))
    echo -e "${YELLOW}>>> $nombre (cuota $congelada, actual $actual)${NC}"
    if [ "$actual" -le "$congelada" ]; then
        echo -e "${GREEN}✓ $nombre${NC}"; ((PASSED++))
    else
        echo -e "${RED}✗ $nombre: $actual > cuota $congelada (las cuotas solo bajan)${NC}"; ((FAILED++))
    fi
}

# pytest_con_base <nombre> <dir> <base>
pytest_con_base() {
    local nombre="$1" dir="$2" base="$3"
    ((TOTAL++))
    echo -e "${YELLOW}>>> $nombre (base >= $base)${NC}"
    local salida
    salida="$(.venv/bin/pytest -q "$dir" 2>&1 | tail -3)"
    local pasan
    pasan="$(echo "$salida" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+' | tail -1)"
    if [ -n "$pasan" ] && echo "$salida" | grep -q "passed" && ! echo "$salida" | tail -1 | grep -qE "failed|error"; then
        if [ "$pasan" -ge "$base" ]; then
            echo -e "${GREEN}✓ $nombre: $pasan passed${NC}"; ((PASSED++))
        else
            echo -e "${RED}✗ $nombre: $pasan < base $base (línea base innegociable)${NC}"; ((FAILED++))
        fi
    else
        echo "$salida" | tail -3
        echo -e "${RED}✗ $nombre${NC}"; ((FAILED++))
    fi
}

# ============================================
if [ "$UPDATE_CORPUS" = true ]; then
    section "RECONGELADO DEL CORPUS (deliberado)"
    run_check "corpus --update" $PY tools/corpus_integridad.py --update
    exit 0
fi

section "CORPUS CANÓNICO"
run_check "corpus-integridad" $PY tools/corpus_integridad.py
run_check "nombres-nfc" $PY tools/nfc_check.py

section "CONFIGURACIÓN Y SEGURIDAD"
run_check "yaml-configs" $PY -c "
import yaml, sys
for f in ['bloque_a/11_Ejecutor/config/por_defecto.yaml','bloque_a_forex/11_Ejecutor/config/por_defecto.yaml','bloque_b/11_Ejecutor/config/por_defecto.yaml']:
    yaml.safe_load(open(f, encoding='utf-8')); print('ok', f)
"
run_check "secrets" $PY tools/secrets_scan.py

section "DOCUMENTACIÓN PROPIA"
run_check "refs-vivas" $PY tools/refs_vivas.py

if [ "$CORE_ONLY" = false ]; then
    section "LINT Y TIPOS (CUOTAS: solo bajan)"

    if command -v .venv/bin/ruff &> /dev/null; then
        actual="$(.venv/bin/ruff check --output-format=concise "${EJECUTORES[@]}" 2>/dev/null | wc -l | tr -d ' ')"
        gate_cuota "ruff (hallazgos)" "$actual" "$(cuota ruff)"
    else
        echo "ruff no instalado, omitiendo"; ((SKIPPED++)); ((TOTAL++))
    fi

    if command -v .venv/bin/mypy &> /dev/null; then
        for i in 0 1 2; do
            paq="${PAQUETES[$i]}"
            actual="$(.venv/bin/mypy --ignore-missing-imports --no-error-summary "${EJECUTORES[$i]}/$paq" 2>/dev/null | wc -l | tr -d ' ')"
            gate_cuota "mypy $paq" "$actual" "$(cuota mypy_$paq)"
        done
    else
        echo "mypy no instalado, omitiendo"; ((SKIPPED++)); ((TOTAL++))
    fi
fi

section "TESTS (líneas base innegociables)"
pytest_con_base "pytest bloque_a"        "${EJECUTORES[0]}" "$(cuota pytest_bloque_a)"
pytest_con_base "pytest bloque_a_forex"  "${EJECUTORES[1]}" "$(cuota pytest_bloque_a_forex)"
pytest_con_base "pytest bloque_b"        "${EJECUTORES[2]}" "$(cuota pytest_bloque_b)"

# ============================================
section "RESUMEN"
echo -e "Gates ejecutados: $TOTAL"
echo -e "${GREEN}Pasaron: $PASSED${NC}"
echo -e "${RED}Fallaron: $FAILED${NC}"
echo -e "${YELLOW}Omitidos: $SKIPPED${NC}"

if [ "$FAILED" -eq 0 ]; then
    echo -e "\n${GREEN}✅ TODOS LOS GATES PASARON${NC}"
    exit 0
else
    echo -e "\n${YELLOW}⚠️  ALGUNOS GATES FALLARON${NC}"
    exit 1
fi
