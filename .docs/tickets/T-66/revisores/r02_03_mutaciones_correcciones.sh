#!/bin/bash
# T-66 · QA r02 · Mutaciones de las correcciones de la r01 (H-01 a H-05): se revierte UNA corrección en una copia del bloque
# y se ejecuta la prueba de regresión que la cubre. Cada línea debe decir «failed»; «passed» = la prueba no protege esa corrección.
# Uso: SRC=<raíz de bloque_a> DEST=<carpeta de trabajo> PY=<python> r02_03_mutaciones_correcciones.sh
SRC=${SRC:?SRC = raíz de bloque_a}
DEST=${DEST:?DEST = carpeta de trabajo}
PY=${PY:-/home/claude/repo/.venv/bin/python}
mut() {
  local n=$1 f=$2 py=$3 t=$4 D=$DEST/$1
  rm -rf $D; mkdir -p $D; cp -r $SRC $D/raiz; local E=$D/raiz/11_Ejecutor; rm -rf $E/.pytest_cache
  $PY - "$E/$f" <<PY
import sys,pathlib
p=pathlib.Path(sys.argv[1]); s=p.read_text(encoding="utf-8")
$py
p.write_text(s,encoding="utf-8")
PY
  (cd $E && PYTHONPATH=$E timeout 900 $PY -m pytest -q -p no:cacheprovider "tests/$t" 2>&1 | tail -1 | sed "s/^/[$n] /")
}
P=test_t66_propuestas.py
O=bloque_a/orquestacion.py
mut h01_ids $O 'a="oid = f\"OBJ-{f[\x27proxy\x27]}-{nn:02d}\""; assert a in s; s=s.replace(a,"oid = o[\"id\"]")' "$P::test_h01_ids_repetidos_del_modelo_no_cruzan_entre_opciones"
mut h01_enviadas $O 'a="if isinstance(x, dict) and x.get(\"objecion_id\") in enviadas}"; assert a in s; s=s.replace(a,"if isinstance(x, dict)}")' "$P::test_h01_la_contrarreplica_no_resuelve_objeciones_que_no_se_le_enviaron"
mut h02_ejecutor $O 'a="if c in CLASES] or activas"; assert a in s; s=s.replace(a,"if c in CLASES] or [\"RV\"]")' "$P::test_h02_un_escalado_sin_tipo_va_a_un_tipo_activo"
mut h02_simulado bloque_a/mock_respuestas.py 'a="or list(msg.get(\"clases_activas\") or [\"DIV\"])[:1]"; assert a in s; s=s.replace(a,"or [\"RV\"]")' "$P::test_h02_un_escalado_sin_tipo_va_a_un_tipo_activo"
mut h03 $O 'a="if not isinstance(v, list) or not v:"; assert a in s; s=s.replace(a,"if False:")' "$P::test_h03_clases_activas_vacia_se_rechaza"
mut h04 $O 'a="if not isinstance(pedidos, list):"; assert a in s; s=s.replace(a,"if False:")' "$P::test_h04_aprobar_certificados_que_no_es_lista_da_un_solo_rechazo"
mut h05 bloque_a/motor/evaluacion.py 'a="if float(np.ptp(y)) <= _TOL_VARIANZA"; assert a in s; s=s.replace(a,"if False and float(np.ptp(y)) <= _TOL_VARIANZA")' "$P::test_h05_residuos_constantes_dan_rho_1_sea_cual_sea_el_valor"
