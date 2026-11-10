# Revisión independiente — V0.63 (semana simulada)

Estado: **pendiente de revisión**. La batería se entrega en verde (53 baterías, 0 con fallos; ver `salida_pruebas.txt`).

**Nota del 10 de noviembre de 2026 (al aplicar la revisión independiente de V0.66, hallazgo 3b):** la revisión
independiente de esta pieza no llegó a ejecutarse y **se da por renunciada** — no hay hallazgos que registrar, ni
los hubo. La pieza sigue verificada por su batería, que corre en el lote completo desde entonces (55 baterías, 0
con fallos, repetido por el revisor de V0.66), y su recorrido de la semana quedó fijado paso a paso por las
pruebas doradas de V0.66 (`pruebas/doradas/semana.json`, gemelo contrastado línea a línea con esta batería por
esa misma revisión). Lo que sigue es la nota de entrega original.

Cuando se ejecute la revisión (en otra conversación, con el ZIP de la pieza ya en verde y el prompt de la sección 9 de
las directrices, sin el historial de la pieza), cada hallazgo se anotará aquí con: gravedad, script del revisor,
resultado antes y después, arreglo y prueba de regresión (`r01_...`, `r02_...`). Como la pieza es sobre todo pruebas,
al revisor se le pedirá además una propiedad que la batería debería comprobar y no comprueba, demostrada con un script:
un hueco en la batería cuenta como hallazgo.

Sugerencia para el revisor (además de lo que dice el prompt): el corte a medias solo se provoca en el diario sin clave
(miércoles); un segundo corte en el diario FIRMADO (jueves o viernes) y un arranque con el reloj por detrás del estado
son las dos propiedades vecinas que esta batería no ejercita (tienen cobertura parcial en `pruebas_diario_t03.py` y
`pruebas_reloj_t03.py`).

**Nota del 10 de noviembre de 2026 (T-84):** la renuncia de arriba ya no vale. La revisión independiente de esta pieza
se hizo en T-84 (`.docs/tickets/T-84/qa.md`, ronda r01: **NO APTO**, H-01 medio y H-02 a H-08 bajos) con las sondas de
`entrega_claude/V0.63_revision/`. Las dos propiedades que sugería esta nota (un segundo corte en el diario firmado y un
arranque con el reloj por detrás del estado) fallan cerrado en el producto; la batería no ejercitaba el Reloj. La ronda de
correcciones de T-84 cambia `pruebas/pruebas_semana.py` (instantes de `Reloj.ahora()` con desfase, arranques contados,
mañana con el reloj atrasado y cortes en el diario firmado), `pruebas/pruebas_reloj_t03.py` (H-07) y `validador/diario.py`
(H-06); el detalle, en `.docs/tickets/T-84/analisis-tecnico.md` y `.docs/tickets/T-84/pruebas.md`. Lo de arriba se deja
como estaba.
