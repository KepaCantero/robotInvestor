#!/bin/bash
# T-66 · QA r01 · Mutaciones de la parte de evaluación (PA-03, PA-09, PA-10, PA-21) y de CT-04 aprobar_certificados.
# Se revierte UNA propuesta en una copia del bloque y se ejecuta la prueba que la cubre: cada línea debe decir «failed».
# Uso: SRC=<raíz de bloque_a> DEST=<carpeta de trabajo> PY=<python> r01_07_mutaciones_evaluacion.sh
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
V=test_t66_evaluacion.py
P=test_t66_propuestas.py
EV=bloque_a/evaluador.py
MO=bloque_a/motor/evaluacion.py
mut pa10_propuesto $EV 'a="\"estado\": \"PROPUESTO\" if solo_endurecer else \"VIGENTE\","; assert a in s; s=s.replace(a,"\"estado\": \"VIGENTE\",")' "$V::test_pa10_certificado_nace_propuesto_y_no_habilita_probabilidades"
mut pa10_recal $EV 'a="aju.update({\"aplicado_en_produccion\": False, \"propuesta\": True,"; assert a in s; s=s.replace(a,"aju.update({\"propuesta\": True,")' "$V::test_pa10_recalibracion_siempre_propuesta"
mut pa10_retirar $EV 'a="elif k in propuestos and not crit[\"certificable\"]:"; assert a in s; s=s.replace(a,"elif False:")' "$V::test_pa10_revocar_y_retirar_siguen_siendo_automaticos"
mut pa10_valida $EV 'a="if c.get(\"estado\") != \"PROPUESTO\":"; assert a in s; s=s.replace(a,"if False:")' "$V::test_pa10_aprobar_certificados_por_ct04"
mut pa10_ct04 bloque_a/orquestacion.py 'a="self.evaluador.aprobar_certificados([str(cid)], as_of, autor=\"BROKER\")"; assert a in s; s=s.replace(a,"pass")' "$P::test_pa10_ct04_aprueba_un_certificado_propuesto_y_rechaza_uno_desconocido"
mut pa09_resueltos $EV 'a="out = [p for p in out if not contaminacion_posible(p)]"; assert a in s; s=s.replace(a,"out = out")' "$V::test_pa09_contaminados_no_cuentan_para_certificados"
mut pa09_lecciones $EV 'a="out = [p for p in out if not contaminacion_posible(p)]"; assert a in s; s=s.replace(a,"out = out")' "$V::test_pa09_contaminados_no_generan_lecciones"
mut pa09_recal $EV 'a="out = [p for p in out if not contaminacion_posible(p)]"; assert a in s; s=s.replace(a,"out = out")' "$V::test_pa09_contaminados_no_cuentan_para_la_recalibracion"
mut pa09_h5 $EV 'a="admis = [h for h in resueltos_h if not (contaminacion_posible(p) or contaminacion_posible(h))]"; assert a in s; s=s.replace(a,"admis = resueltos_h")' "$V::test_pa09_contaminados_no_cuentan_para_la_degradacion_de_h5"
mut pa09_backtest bloque_a/backtest.py 'a="    if excl.get(\"total\"):"; assert a in s; s=s.replace(a,"    if False:")' "$P::test_pa09_backtest_con_modelo_real_separa_las_metricas_no_admisibles"
mut pa03_criterio $MO 'a="elif not (math.isfinite(n_eff) and n_eff >= n_min):"; assert a in s; s=s.replace(a,"elif not (n >= n_min):")' "$V::test_pa03_pronosticos_duplicados_en_la_misma_fecha_no_certifican"
mut pa03_bootstrap $MO 'a="        ic_bss = bss_conglomerados(p, o, p_ref, fechas, replicas, nivel, semilla, min_conglomerados)"; assert a in s; s=s.replace(a,"        ic_bss = bss(p, o, p_ref, replicas, nivel, semilla)")' "$V::test_pa03_minimo_de_conglomerados_desde_la_configuracion"
mut pa03_fechas $EV 'a="f = x.get(\"fecha_resolucion\") or x.get(\"fecha_emision\")"; assert a in s; s=s.replace(a,"f = x.get(\"fecha_emision\")")' "$V::test_pa03_conglomerado_por_fecha_de_resolucion_y_si_falta_de_emision"
mut pa21_metrica $EV 'a="analista = self._analista_vs_prospectiva(lst)"; assert a in s; s=s.replace(a,"analista = None")' "$V::test_pa21_brier_del_analista_frente_a_prospectiva"
