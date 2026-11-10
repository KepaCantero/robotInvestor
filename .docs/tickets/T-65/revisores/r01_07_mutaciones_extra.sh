#!/usr/bin/env bash
# r01_07 · QA T-65 · mutaciones que no están en mutaciones.py: ¿las detecta la suite ENTERA de bloque_a?
# Uso: r01_07_mutaciones_extra.sh <raíz de una COPIA del repo (worktree)>  — nunca sobre el árbol de trabajo real.
# Cada mutación se aplica con sed sobre la copia, se ejecuta pytest -x de bloque_a y se restaura desde la copia .orig.
set -u
R="${1:?raíz de la copia}"
EJ="$R/bloque_a/11_Ejecutor"
PY="$R/.venv/bin/python"
mutar() {  # nombre archivo patrón_sed
  local nombre="$1" archivo="$2" expr="$3"
  cp "$EJ/$archivo" "$EJ/$archivo.orig"
  sed -i "$expr" "$EJ/$archivo"
  if cmp -s "$EJ/$archivo" "$EJ/$archivo.orig"; then echo "ERROR  $nombre: la sustitución no cambió nada"; mv "$EJ/$archivo.orig" "$EJ/$archivo"; return; fi
  if (cd "$EJ" && "$PY" -m pytest -q -x -p no:cacheprovider >/dev/null 2>&1); then
    echo "PASA!  $nombre (ninguna prueba la detecta)"
  else
    echo "FALLA  $nombre (detectada)"
  fi
  mv "$EJ/$archivo.orig" "$EJ/$archivo"
}
mutar "CS-10 pregunta repetida: veces fijo a 3" bloque_a/orquestacion.py 's/>= int(pr_rep\["veces"\])/>= 3/'
mutar "CS-10 recalibración RK: paso fijo a 0,05" bloque_a/evaluador.py 's/delta, b_trim, b_tot = float(rr\["paso"\])/delta, b_trim, b_tot = 0.05/'
mutar "CS-10 PS1: raíces mínimas fijas a 2" bloque_a/orquestacion.py 's/>= int(parametro(self.cfg, "ps1.raices_min"))/>= 2/'
mutar "H-10c sin incidencia DATOS en HA" bloque_a/orquestacion.py 's/self.almacen.incidencia("DATOS", f"HT-01: datos inválidos/(lambda *a, **k: None)("DATOS", f"HT-01: datos inválidos/'
mutar "H-16 run COMPLETO con proxies sin medir" bloque_a/orquestacion.py 's/ or clusteres.get("sin_historia") or / or /'
