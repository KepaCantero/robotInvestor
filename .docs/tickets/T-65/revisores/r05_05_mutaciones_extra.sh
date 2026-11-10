#!/usr/bin/env bash
# r05_05 · QA T-65 r05 · mutaciones de las correcciones de la r04 que no están en mutaciones.py: ¿las detecta la suite
# ENTERA de bloque_a? Uso: r05_05_mutaciones_extra.sh <raíz de una COPIA del repo (worktree)> — nunca sobre el árbol real.
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
# PS2 al emitir: el dato más reciente de las dos series en vez del más antiguo
mutar "H-24 PS2 con max en vez de min" bloque_a/orquestacion.py \
  's/fecha_dato = str(min(pd.Timestamp(fecha_dato), self.proveedor.valor_en(ref, as_of)\[0\]).date())/fecha_dato = str(max(pd.Timestamp(fecha_dato), self.proveedor.valor_en(ref, as_of)[0]).date())/'
# PS2 al emitir: si la referencia no está disponible, se queda la fecha del proxy
mutar "H-24 PS2 con la referencia ausente usa la del proxy" bloque_a/orquestacion.py \
  '/def _puertas/,/if fecha_dato:/{s/                fecha_dato = None/                pass/}'
# Resolución: la fecha guardada como fecha_dato vuelve a ser solo la del proxy
mutar "H-24 fecha_dato solo del proxy" bloque_a/evaluador.py \
  's/"fecha_dato": max(d1, d1b) if d1b is not None else d1, /"fecha_dato": d1, /'
# CESTA: la fecha devuelta es la más reciente de los miembros (antes de la r04, max)
mutar "H-24 cesta con la fecha más reciente" bloque_a/evaluador.py \
  's/            return float(np.mean(vals)), min(fechas)/            return float(np.mean(vals)), max(fechas)/'
