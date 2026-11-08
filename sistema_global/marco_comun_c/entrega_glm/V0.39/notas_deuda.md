# Notas de deuda — V0.39 (cortacircuito global por pérdida)

La pieza avanza la fila T-40 de la tabla T (queda en parte resuelta). Ninguna otra fila cambia y no se abre ninguna fila nueva en la tabla D: los límites del cortacircuito son los de D-11 (ya existentes en `politica_f`), sin decisiones nuevas.

## Tabla T (texto nuevo de la cuarta columna de filas existentes)

- T-40: «EN PARTE RESUELTO en V0.39: el cortacircuito global por pérdida ya está hecho (Fase 1): al registrar una foto de cartera válida, `registrar_cartera` compara la pérdida del día de la foto y la de la semana (siete días que acaban en la fecha UTC de la foto, el criterio de F-16) con `perdida_dia_max_eur` y `perdida_semana_max_eur` [PROPUESTO, D-11] y, al llegar a alguno (comparación `>=`, el umbral en el que F-16 empieza a vetar), activa solo el kill-switch (§8 y §11, actor ORQUESTADOR, motivo «cortacircuito global: …»), emite el aviso O-38 de prioridad ALTA con las dos cifras y sus límites, anota el disparo una vez por día UTC en `self.cortacircuitos` y devuelve el registro con `cortacircuito: True/False`; el rearme se rechaza con O-35 mientras la última foto siga en o por encima de alguno de los dos límites (solo si el kill vino del cortacircuito: actor ORQUESTADOR y su prefijo, no un kill manual con un motivo parecido; r02) (batería `pruebas/pruebas_cortacircuito_t40.py`, 27 comprobaciones —25 originales y las regresiones r01–r02 de la revisión—). Queda para la Fase 3: el vigilante con latido como proceso independiente (que compruebe el límite aunque el plano de control se cuelgue)»

## Qué queda fuera de la pieza (y dónde vive)

- El vigilante con latido (la otra parte de T-40, Fase 3): hoy el cortacircuito solo salta cuando G registra una foto; si el plano de control se cuelga, nadie comprueba los límites hasta la próxima foto. Es exactamente el hueco que el vigilante independiente cerrará.
- El cortacircuito por cartera de cada estrategia (§7.3) y los umbrales propios de cada una: fuera del alcance de la Fase 1.
