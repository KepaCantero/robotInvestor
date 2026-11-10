# Notas de deuda — V0.64 (panel con el estado del sistema)

Cambios en «Deuda técnica y pendientes del operador» de `Deuda_tecnica.md`:

## Tabla T

- **T-63 (nueva, sin resolver): método público para el estado del diario.** La comprobación «diario» del panel lee dos
  privados del `Diario` (`_roto`, el motivo del bloqueo, y `_n`, el número de la última línea, que `punto()` deja en 1).
  La consola es parte del sistema y la pieza lo anota en el Documento 0, pero lo limpio es un método público de solo
  lectura en `diario.py` (por ejemplo `estado()`, como el que esta misma pieza añade a `Reloj`) que devuelva
  `{"roto", "lineas_desde_punto", ...}` sin cambiar nada. Se propone, no se implementa: la pieza manda leer los
  privados y anotar la propuesta. Si se hace, la comprobación «diario» de `consola.py` pasa a llamarlo y los privados
  dejan de cruzar la frontera del módulo.
- Ninguna fila más cambia: la pieza no corrige ningún defecto de producto (no hay cambios fuera de `consola.py` y el
  método `estado()` de `reloj.py`, todas las baterías pasan y las 53 anteriores sin tocarlas).

## Tabla D

- Ninguna fila nueva. El único umbral nuevo de la pieza (1.000 líneas del diario sin punto de control) va a la fila
  **D-09**, que ya existe (umbrales de la consola), como valor por defecto del parámetro `lineas_diario_ambar` de
  `panel`, marcado [PROPUESTO] en su docstring.
