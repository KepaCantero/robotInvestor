#!/bin/bash
# r08b · Mutaciones de la ronda 2: se revierte UNA corrección (H-01..H-05 y las de la ronda 1) en una copia del ejecutor
# actual y se ejecuta su prueba. Cada prueba debe FALLAR con la mutación.
S=/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad
SRC=${SRC:-/home/claude/repo/bloque_a}
mut() {
  local n=$1 f=$2 py=$3 t=$4 D=$S/qa_t53/mut2/$1
  rm -rf $D; mkdir -p $D; cp -r $SRC $D/raiz; local E=$D/raiz/11_Ejecutor; rm -rf $E/.pytest_cache
  /home/claude/repo/.venv/bin/python - "$E/$f" <<PY
import sys,pathlib
p=pathlib.Path(sys.argv[1]); s=p.read_text(encoding="utf-8")
$py
p.write_text(s,encoding="utf-8")
PY
  (cd $E && PYTHONPATH=$E timeout 600 /home/claude/repo/.venv/bin/python -m pytest -q -p no:cacheprovider "tests/$t" 2>&1 | tail -1 | sed "s/^/[$n] /")
}
T=test_t53_seleccion_y_entrega.py
mut h01_ventana bloque_a/orquestacion.py 'a="self.proveedor.cierres(f[\"simbolo\"], ini, as_of)"; assert a in s; s=s.replace(a,"self.proveedor.valor_en(f[\"simbolo\"], as_of)")' "$T::test_h01_simbolo_deslistado_no_vacia_su_tipo"
mut h01_clusteres bloque_a/orquestacion.py 'a="        if clusteres.get(\"rechazo\"):\n            limitaciones"; assert a in s; s=s.replace(a,"        if False:\n            limitaciones")' "$T::test_h01_historia_corta_tambien_queda_declarada"
mut h02_naturaleza bloque_a/sintesis.py 'a="nat, hp = nat_ag or naturaleza_para(hp_ag), hp_ag"; assert a in s; s=s.replace(a,"nat, hp = nat_ag or NATURALEZA_POR_DEFECTO.get(c, \"CICLICA\"), hp_ag")' "$T::test_h02_h5_declarado_sin_naturaleza_no_se_bloquea_por_la_naturaleza_por_defecto"
mut h02_aviso bloque_a/sintesis.py 'a="limit = [x for x in limit"; s=s.replace("+ avisos_hp","")' "$T::test_h02_horizonte_no_ofrecido_se_declara_como_limitacion"
mut h03_semaforo bloque_a/sintesis.py 'a="return \"VERDE\" if solida else \"AMBAR\""; assert a in s; s=s.replace(a,"return \"VERDE\" if len(opciones) >= 2 else \"AMBAR\"")' "$T::test_h03_semaforo"
mut h03_hp_analista bloque_a/sintesis.py 'a="hp_ag = f.get(\"horizonte_principal\") if f.get(\"horizonte_principal\") in hz else None"; assert a in s; s=s.replace(a,"hp_ag = None")' "$T::test_h03_se_usan_el_horizonte_y_la_justificacion_del_analista"
mut h04_festivos bloque_a/orquestacion.py 'a="holidays=[d.date() for d in cierres]"; assert a in s; s=s.replace(a,"holidays=[]")' "$T::test_h04_ps2_h1_descuenta_festivos"
mut h05_tabla bloque_a/orquestacion.py 'a="        self.cfg[\"_tabla_horizontes\"] = self.evaluador._matriz_aplicabilidad(as_of)\n"; assert a in s; s=s.replace(a,"")' "$T::test_h05_degradacion_h5_cambia_la_tabla_del_ciclo_siguiente"
