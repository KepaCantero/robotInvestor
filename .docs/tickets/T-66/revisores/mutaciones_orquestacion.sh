#!/bin/bash
# T-66 · Mutaciones de la parte de orquestación: se revierte UNA propuesta en una copia del bloque y se ejecuta su prueba.
# Cada prueba debe FALLAR con la mutación. Uso: SRC=<raíz del bloque_a> DEST=<carpeta de trabajo> mutaciones_orquestacion.sh
SRC=${SRC:-/home/claude/repo/bloque_a}
DEST=${DEST:-/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/mut_t66}
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
T=test_t66_propuestas.py
mut pa01_p02 bloque_a/orquestacion.py 'a="perfiles_activos(a), \"SERVICIO\""; assert a in s; s=s.replace(a,"list(CLASES), \"SERVICIO\"")' "$T::test_pa01_ciclo_por_defecto_analiza_solo_divisas"
mut pa01_aviso bloque_a/orquestacion.py 'a="for c in no_activas]"; assert a in s; s=s.replace(a,"for c in []]")' "$T::test_pa01_alcance_mixto_analiza_lo_activo_y_declara_lo_demas"
mut h06 bloque_a/orquestacion.py 'a="        if not clases:   # nada que analizar"; assert a in s; s=s.replace(a,"        if False:   # nada que analizar")' "$T::test_h06_todo_pausado_no_redacta_ni_falla_en_el_esquema"
mut pa05_entrada bloque_a/orquestacion.py 'a="\"calculos\": f[\"senales\"].get(\"calc_ids\", [])} for f in finales]"; assert a in s; s=s.replace(a,"\"calculos\": f[\"senales\"].get(\"calc_ids\", []), \"tesis\": f[\"tesis\"], \"dimensiones\": f[\"dimensiones\"]} for f in finales]")' "$T::test_pa05_el_contradictor_no_recibe_el_razonamiento_del_analista"
mut pa05_sin_replica bloque_a/orquestacion.py 'a="                        o[\"evidencia_citada\"] = citada\n"; assert a in s; s=s.replace(a,a+"                        o[\"resuelta\"] = bool(x.get(\"resuelta\"))\n")' "$T::test_pa05_el_analista_no_resuelve_solo_una_objecion_fuerte_sin_evidencia"
mut pa05_confirmacion bloque_a/orquestacion.py 'a="o[\"resuelta\"] = conf[o[\"objecion_id\"]].get(\"resuelta\") is True"; assert a in s; s=s.replace(a,"o[\"resuelta\"] = True")' "$T::test_pa05_sin_confirmacion_del_contradictor_sigue_abierta"
mut pa05_fragil bloque_a/sintesis.py 'a="                op[\"confianza\"] = \"especulativo\""; assert a in s; s=s.replace(a,"                pass")' "$T::test_pa05_con_evidencia_y_confirmacion_queda_resuelta_y_la_tesis_es_fragil"
mut pa09_marca bloque_a/sintesis.py 'a="\"contaminacion_posible\": bloque.contaminacion_posible(as_of),"; assert a in s; s=s.replace(a,"\"contaminacion_posible\": False,")' "$T::test_pa09_backtest_con_modelo_real_antes_del_corte_marca_y_anonimiza"
mut pa09_auto bloque_a/orquestacion.py 'a="            anon = self.modo == \"backtest\" and bool(getattr(cliente, \"conocimiento_previo\", True))"; assert a in s; s=s.replace(a,"            anon = False")' "$T::test_pa09_backtest_con_modelo_real_antes_del_corte_marca_y_anonimiza"
mut pa14 bloque_a/orquestacion.py 'a="\"n_cand\": max(n_cand, len(evaluadas)), \"ablacion\": ablacion}"; assert a in s; s=s.replace(a,"\"n_cand\": max(n_cand, len(evaluadas))}")' "$T::test_pa14_cada_run_registra_la_ablacion_por_tipo"
mut pa21 bloque_a/sintesis.py 'a="\"prob_analista\": _prob_analista(f, h),"; assert a in s; s=s.replace(a,"\"prob_analista\": None,")' "$T::test_pa21_la_probabilidad_del_analista_llega_a_f4"
