#!/usr/bin/env bash
# QA r01 T-203 · 04: ¿se fusionan T-201 y T-203? merge-tree, resolución mínima, ruff/mypy (r01_03) y las pruebas de los dos.
# Uso: r01_04_fusion_t201.sh <repo> <carpeta_nueva> [rama_t201=wip/t201] [rama_t203=wip/t203]
# Resolución aplicada (la que se propone para integrar): envoltorios HT-02/03/07 de T-201 (TYPE_CHECKING, ya sin
# hallazgos de ruff), operaciones.py con las dos cosas (`Sequence[float] | np.ndarray` de T-201 y `-> dict` de T-203),
# las dos líneas de la deuda, cuotas ruff de T-203 y mypy_bloque_a de T-201. No hace commit.
set -u
REPO=$1; W=$2; T201=${3:-wip/t201}; T203=${4:-wip/t203}
HERE=$(cd "$(dirname "$0")" && pwd)
echo "== merge-tree $T201 + $T203"; git -C "$REPO" merge-tree --write-tree --name-only "$T201" "$T203" | sed -n '2,/^$/p'
git -C "$REPO" worktree add --detach "$W" "$T201" >/dev/null 2>&1 || exit 2
ln -sfn "$REPO/.venv" "$W/.venv"
cd "$W" && git -c user.name=qa -c user.email=qa@example.invalid merge --no-commit --no-ff "$T203" >/dev/null 2>&1
E=bloque_a/11_Ejecutor/bloque_a
for f in ht02 ht03 ht07; do git checkout --ours "$E/herramientas/$f.py"; done
.venv/bin/python -I - <<'PY'
import re
def res(p, f):
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", f, s, flags=re.S)
    open(p, "w", encoding="utf-8").write(s)
res("bloque_a/11_Ejecutor/bloque_a/motor/operaciones.py",
    lambda m: "def posicion_historica(valor: float, historia: Sequence[float] | np.ndarray) -> dict:\n")
res("sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md", lambda m: m.group(1) + m.group(2))
res("tools/cuotas.txt", lambda m: "ruff=2735\nmypy_bloque_a=67\n")
PY
if grep -rln '^<<<<<<<\|^>>>>>>>' bloque_a tools sistema_global; then echo "QUEDAN CONFLICTOS"; exit 1; fi
SALIDA=${SALIDA:-/tmp} "$HERE/r01_03_cuotas.sh" "$W"
cd bloque_a/11_Ejecutor && ../../.venv/bin/pytest -q -p no:cacheprovider tests/test_t201_cuotas.py tests/test_t203_cuotas.py 2>&1 | tail -4
