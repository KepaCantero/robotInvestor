#!/bin/bash
# r08 · Muestra de mutaciones: se revierte UNA corrección en una copia del ejecutor nuevo y se ejecuta su prueba.
# Cada prueba debe FALLAR con la mutación (si pasa, la prueba no protege la regla).
S=/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad
SRC=$S/wt_new/bloque_a
mut() {  # nombre archivo python_de_mutacion prueba
  local n=$1 f=$2 py=$3 t=$4 D=$S/qa_t53/mut/$1
  rm -rf $D; mkdir -p $D; cp -r $SRC $D/bloque_a_root
  local E=$D/bloque_a_root/11_Ejecutor
  /home/claude/repo/.venv/bin/python - "$E/$f" <<PY
import sys,pathlib
p=pathlib.Path(sys.argv[1]); s=p.read_text(encoding="utf-8")
$py
p.write_text(s,encoding="utf-8")
PY
  (cd $E && PYTHONPATH=$E timeout 600 /home/claude/repo/.venv/bin/python -m pytest -q -p no:cacheprovider "tests/$t" 2>&1 | tail -1 | sed "s/^/[$n] /")
}
mut holm bloque_a/motor/evaluacion.py 'a="if not _valida(p) or p > out[k]:\n            detenido = True"; assert a in s; s=s.replace(a,"pass")' "test_t53_evaluacion_y_almacen.py::test_holm_escalonado_se_detiene_en_el_primer_fallo"
mut es_hito bloque_a/evaluador.py 'a="if p.get(\"estado\") == \"RESUELTO\" and not p.get(\"es_hito\")"; assert a in s; s=s.replace(a,"if p.get(\"estado\") == \"RESUELTO\"")' "test_t53_evaluacion_y_almacen.py::test_hitos_h5_no_cuentan_en_h4_ni_en_el_historial"
mut ece0 bloque_a/evaluador.py 'a="or ece_m is None or ece_m >= ece_rev"; assert a in s; s=s.replace(a,"or (ece_m or 1) >= ece_rev")' "test_t53_evaluacion_y_almacen.py::test_ece_cero_no_revoca_un_certificado"
mut sin_historia bloque_a/orquestacion.py 'a="                self.proveedor.valor_en(f[\"simbolo\"], as_of)\n"; assert a in s; s=s.replace(a,"")' "test_t53_seleccion_y_entrega.py::test_un_simbolo_sin_historia_no_vacia_su_tipo"
mut ps1 bloque_a/orquestacion.py 'a="and p.get(\"origen\") != \"AG-13\""; assert a in s; s=s.replace(a,"")' "test_t53_seleccion_y_entrega.py::test_ps1_no_se_supera_solo_con_la_pieza_automatica_de_momentum"
mut semaforo bloque_a/sintesis.py 'a="sem = \"GRIS\" if n == 0 else (\"VERDE\" if solida else \"AMBAR\")"; assert a in s; s=s.replace(a,"sem = \"GRIS\" if n == 0 else (\"VERDE\" if n >= 2 else \"AMBAR\")")' ""
mut hp_analista bloque_a/sintesis.py 'a="hp_ag = f.get(\"horizonte_principal\") if f.get(\"horizonte_principal\") in hz else None"; assert a in s; s=s.replace(a,"hp_ag = None")' ""
mut f4_resolucion bloque_a/almacen.py 'a="            if \"RESOLUCION\" in previas:\n"; assert a in s; s=s.replace(a,"            if False:\n")' "test_t53_evaluacion_y_almacen.py::test_f4_congelacion_rechaza_realta_y_resoluciones_invalidas"
