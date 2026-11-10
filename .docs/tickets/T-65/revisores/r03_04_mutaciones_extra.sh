#!/usr/bin/env bash
# r03_04 · QA T-65 r03 · mutaciones de las correcciones de la r02 que no están en mutaciones.py: ¿las detecta la suite ENTERA
# de bloque_a? Uso: r03_04_mutaciones_extra.sh <raíz de una COPIA del repo (worktree)> — nunca sobre el árbol de trabajo real.
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
# H-12: la referencia guardada en las vigentes del tipo deja de validarse (solo la de la configuración)
mutar "H-12 sin validar la referencia de las vigentes" bloque_a/orquestacion.py \
  's/refs_tipo = {self._referencia(clase)} | {v.get("referencia_indice") for v in self.vigentes(as_of, clase)}/refs_tipo = {self._referencia(clase)}/'
# H-12: una fuga de información en la referencia se declara como referencia inválida en vez de cortar el ciclo
mutar "H-12 la fuga de la referencia se absorbe" bloque_a/orquestacion.py \
  '/def _referencia_invalida/,/return None/{s/        except FugaDeInformacion:/        except ZeroDivisionError:/}'
# H-13: fecha_publicacion con zona aceptada
mutar "H-13 fecha_publicacion con zona aceptada" bloque_a/herramientas/ht01_datos.py \
  's/        if getattr(pub.dt, "tz", None) is not None:   # T-65 (QA r02, H-13): como en `fecha`/        if False:/'
