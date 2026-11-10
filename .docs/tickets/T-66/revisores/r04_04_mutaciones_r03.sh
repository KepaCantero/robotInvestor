#!/bin/bash
# T-66 · QA r04 · Mutaciones de las correcciones de la r03 (H-15 a H-18): se revierte UNA corrección en una copia del bloque
# y se ejecuta la prueba de regresión que la cubre. «failed» = la prueba protege la corrección; «passed» = no.
# Uso: SRC=<raíz de bloque_a> DEST=<carpeta de trabajo> PY=<python> r04_04_mutaciones_r03.sh
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
  (cd $E && PYTHONPATH=$E PYTHONDONTWRITEBYTECODE=1 timeout 900 $PY -m pytest -q -p no:cacheprovider $t 2>&1 | tail -1 | sed "s/^/[$n] /")
}
P=tests/test_t66_propuestas.py
O=bloque_a/orquestacion.py
# H-15: vuelve a aceptarse cualquier REF- registrada
mut h15_por_id $O 'a="if str(e) in verificables]"; assert a in s; s=s.replace(a,"if str(e) in verificables or self.referencias.por_id(str(e))]")' "$P::test_h15_una_ref_registrada_ajena_a_la_opcion_no_es_evidencia_citable"
# H-16: sin saneado en la pieza
mut h16_pieza $O 'a="\"afirmacion\": _limpio(pieza.get(\"afirmacion\"))"; assert a in s; s=s.replace(a,"\"afirmacion\": pieza.get(\"afirmacion\")")' "$P::test_h16_el_contenido_de_la_contrarreplica_se_sanea"
# H-16: sin saneado en la REF- del corpus (rama del caso de la r03)
mut h16_ref $O 'a="_limpio(ref.get(\"afirmacion\") or ref.get(\"titulo\") or ref.get(\"resumen\"))"; assert a in s; s=s.replace(a,"(ref.get(\"afirmacion\") or ref.get(\"titulo\") or ref.get(\"resumen\"))")' "$P"
# H-16: el saneado no registra la incidencia
mut h16_registro $O 'a="            self._registrar_r9(hall, None)\n"; assert a in s; s=s.replace(a,"")' "$P::test_h16_el_contenido_de_la_contrarreplica_se_sanea"
# H-17: «más estricto» → siempre la regla (función)
mut h17_estricto $O 'a="        if guardado in orden and orden.index(guardado) > orden.index(regla):"; assert a in s; s=s.replace(a,"        if False:")' "$P::test_h17_en_el_arrastre_manda_el_veredicto_mas_estricto"
# H-17: en _desde_f3, vuelve el «guardado o regla» de 03b8c3b (sin recálculo)
mut h17_guardado_o_regla $O 'a="self._veredicto_mas_estricto(v.get(\"veredicto_refutacion\"), self._veredicto_refutacion(f))"; assert a in s; s=s.replace(a,"(v.get(\"veredicto_refutacion\") or self._veredicto_refutacion(f))")' "$P"
# H-17: en _desde_f3, solo la regla (control: debería seguir pasando, la regla coincide con lo guardado por el código)
mut h17_solo_regla $O 'a="self._veredicto_mas_estricto(v.get(\"veredicto_refutacion\"), self._veredicto_refutacion(f))"; assert a in s; s=s.replace(a,"self._veredicto_refutacion(f)")' "$P"
# H-17: `resuelta` vuelve a valer si es verdadera de cualquier tipo
mut h17_resuelta $O 'a="elif o.get(\"resuelta\") is not True:"; assert a in s; s=s.replace(a,"elif not o.get(\"resuelta\"):")' "$P::test_h17_h18_objeciones_del_arrastre_fallan_cerrado"
# H-17: sin la comprobación del enum de `fuerza`
mut h17_fuerza $O 'a="if o.get(\"fuerza\") not in (\"fuerte\", \"moderada\", \"debil\"):"; assert a in s; s=s.replace(a,"if False:")' "$P::test_h17_h18_objeciones_del_arrastre_fallan_cerrado"
# H-17: una objeción que no es un dict ya no se trata
mut h17_nodict $O 'a="            if not isinstance(o, dict):"; assert a in s; s=s.replace(a,"            if False:")' "$P::test_h17_h18_objeciones_del_arrastre_fallan_cerrado"
# H-18: «o» → «y» (evidencia sin contrarréplica dejaría de reabrirse; era h10_y de la r03)
mut h18_y $O 'a="(not o.get(\"evidencia_citada\") or \"contrarreplica\" not in o)"; assert a in s; s=s.replace(a,"(not o.get(\"evidencia_citada\") and \"contrarreplica\" not in o)")' "$P::test_h17_h18_objeciones_del_arrastre_fallan_cerrado"
# H-17/H-18: _desde_f3 deja de normalizar las objeciones
mut h18_sin_normalizar $O 'a="objs = self._objeciones_arrastre(v.get(\"objeciones_internas\"))"; assert a in s; s=s.replace(a,"objs = copy.deepcopy(v.get(\"objeciones_internas\") or [])")' "$P::test_h18_fragil_guardada_con_una_fuerte_que_se_reabre_queda_refutada"
# H-11 (r02_03 h02_ejecutor, contra la prueba que la cubre desde la r02)
mut h02_ejecutor_h11 $O 'a="if c in CLASES] or activas"; assert a in s; s=s.replace(a,"if c in CLASES] or [\"RV\"]")' "$P::test_h11_el_ejecutor_lleva_a_tipos_activos_un_escalado_sin_clases"
