#!/usr/bin/env bash
# QA T-203, ronda de cierre · 05 (r01_05 sobre la copia rebasada; los envoltorios son los de T-201): mutantes de lo que protege tests/test_t203_cuotas.py, en una copia desechable (worktree) de wip/t203.
# Uso: rc_05_mutantes_prueba.sh <copia_desechable>   (la deja como estaba con git checkout al terminar cada mutante)
set -u
C=$1; E=$C/bloque_a/11_Ejecutor; B=$E/bloque_a
mut() {  # nombre fichero python-de-sustitución
  local n=$1 f=$2 viejo=$3 nuevo=$4
  "$C/.venv/bin/python" -I -c "import sys; p,a,b=sys.argv[1:]; s=open(p,encoding='utf-8').read(); assert a in s, 'no está'; open(p,'w',encoding='utf-8').write(s.replace(a,b,1))" "$f" "$viejo" "$nuevo" || { echo "$n: NO APLICA"; return; }
  if (cd "$E" && ../../.venv/bin/pytest -q -x -p no:cacheprovider tests/test_t203_cuotas.py >/dev/null 2>&1); then echo "$n: VIVO"; else echo "$n: muerto"; fi
  git -C "$C" checkout -q -- "$f"
}
mut M1_sin_future_mock "$B/mock_respuestas.py" "from __future__ import annotations" ""
mut M2_sin_future_op "$B/motor/operaciones.py" "from __future__ import annotations" ""
mut M3_vuelve_Dict "$B/mock_respuestas.py" "from typing import Any" "from typing import Any, Dict"
mut M4_anotacion_irresoluble "$B/motor/operaciones.py" "-> float | None:" "-> float | Nada:"
mut M5_sin_DIR_REFERENCIA_ht07 "$B/herramientas/ht07.py" "from . import DIR_REFERENCIA" "pass  #"
mut M6_nombre_extra_ht02 "$B/herramientas/ht02.py" "modulo = _ref" "modulo = _ref
extra = 1"
mut M7_otro_objeto_ht03 "$B/herramientas/ht03.py" "modulo = _ref" "modulo = _ref
evaluar_opcion = lambda *a, **k: _ref.evaluar_opcion(*a, **k)"
mut M8_ref_por_paquete_ht02 "$B/herramientas/ht02.py" "import ht02_verificador_enlaces as _ref" "from .referencia import ht02_verificador_enlaces as _ref"
mut M9_sin_sys_path_init "$B/herramientas/__init__.py" "    sys.path.insert(0, str(DIR_REFERENCIA))" "    pass"
