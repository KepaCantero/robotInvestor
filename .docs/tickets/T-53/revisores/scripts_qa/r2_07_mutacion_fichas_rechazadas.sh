#!/bin/bash
# r2_07 · CA-1 para la parte de H-01 que declara las fichas rechazadas: se quita la declaración (registro y laguna) en una copia
# del ejecutor y se ejecuta la suite ENTERA de A. Si pasan las 116, esa parte de la corrección no tiene prueba.
S=/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/qa_t53_r02
SRC=${SRC:-$S/wt/bloque_a}
D=$S/mut_r2/fichas_rechazadas; rm -rf $D; mkdir -p $D; cp -r $SRC $D/raiz; E=$D/raiz/11_Ejecutor
/home/claude/repo/.venv/bin/python - "$E/bloque_a/orquestacion.py" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding="utf-8")
a = "                self._fichas_rechazadas[(clase, run_id)].append(ficha)\n"
assert a in s; s = s.replace(a, "")
p.write_text(s, encoding="utf-8")
PY
(cd $E && PYTHONPATH=$E timeout 900 /home/claude/repo/.venv/bin/python -m pytest -q -p no:cacheprovider tests 2>&1 | tail -1 | sed "s/^/[fichas_rechazadas] /")
