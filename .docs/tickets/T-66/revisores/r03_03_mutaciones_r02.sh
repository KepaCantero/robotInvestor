#!/bin/bash
# T-66 · QA r03 · Mutaciones de las correcciones de la r02 (H-09, H-10 y H-12): se revierte UNA corrección en una copia
# del bloque y se ejecuta la prueba de regresión que la cubre. «failed» = la prueba protege la corrección; «passed» = no.
# Uso: SRC=<raíz de bloque_a> DEST=<carpeta de trabajo> PY=<python> r03_04_mutaciones_r02.sh
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
  (cd $E && PYTHONPATH=$E PYTHONDONTWRITEBYTECODE=1 timeout 900 $PY -m pytest -q -p no:cacheprovider "tests/$t" 2>&1 | tail -1 | sed "s/^/[$n] /")
}
P=test_t66_propuestas.py
O=bloque_a/orquestacion.py
# H-09: el veredicto de F3 no se restaura en el arrastre (código de cb12377)
mut h09_veredicto $O 'a="        f[\"_veredicto\"] = v.get(\"veredicto_refutacion\") or self._veredicto_refutacion(f)\n"; assert a in s; s=s.replace(a,"")' "$P::test_h09_la_tesis_fragil_sigue_siendo_especulativa_en_el_arrastre"
# H-09: se recalcula siempre por la regla en vez de conservar el de F3 (debería seguir pasando: misma regla)
mut h09_solo_regla $O 'a="v.get(\"veredicto_refutacion\") or self._veredicto_refutacion(f)"; assert a in s; s=s.replace(a,"self._veredicto_refutacion(f)")' "$P::test_h09_la_tesis_fragil_sigue_siendo_especulativa_en_el_arrastre"
# H-10: no se reabre la fuerte antigua
mut h10_reabrir $O 'a="                o[\"resuelta\"] = False\n                o[\"reabierta_por\"]"; assert a in s; s=s.replace(a,"                o[\"reabierta_por\"]")' "$P::test_h10_una_fuerte_antigua_resuelta_sin_evidencia_se_reabre_en_el_arrastre"
# H-10: condición «o» → «y» (evidencia sin contrarréplica dejaría de reabrirse)
mut h10_y $O 'a="(not o.get(\"evidencia_citada\") or \"contrarreplica\" not in o)"; assert a in s; s=s.replace(a,"(not o.get(\"evidencia_citada\") and \"contrarreplica\" not in o)")' "$P::test_h10_una_fuerte_antigua_resuelta_sin_evidencia_se_reabre_en_el_arrastre"
# H-10: sin recálculo del veredicto tras reabrir (con veredicto guardado en F3)
mut h10_recalculo $O 'a="        if any(o.get(\"reabierta_por\") for o in objs):\n            f[\"_veredicto\"] = self._veredicto_refutacion(f)\n"; assert a in s; s=s.replace(a,"")' "$P::test_h10_una_fuerte_antigua_resuelta_sin_evidencia_se_reabre_en_el_arrastre"
# H-12: la contrarréplica vuelve a recibir solo ids
mut h12_contenido $O 'a="\"evidencia_citada\": [self._contenido_evidencia(f, e) for e in citada]"; assert a in s; s=s.replace(a,"\"evidencia_citada\": [{\"id\": e, \"afirmacion\": None} for e in citada]")' "$P::test_h12_la_contrarreplica_muestra_el_contenido_de_cada_evidencia"
