---
id: claude/2026-11-15_verificador-ids-contextos
autor: claude
fecha: 2026-11-15
tipo: leccion
etiquetas: [bloque_a, fase0, verificador-ids, corpus]
fuente: .docs/tickets/T-157/analisis-tecnico.md, bloque_a/11_Ejecutor/bloque_a/herramientas/verificador_ids.py
vigencia: vigente
---

## Hecho

La primera pasada del verificador de identificadores del Bloque A (T-157) dio 10 errores y 7 eran falsos: códigos JEL
(«R30», «F31»), la pendiente de una curva de futuros `(F1 − F12) / F12`, las funciones de `03_Funciones` abreviadas
(«Resultados F02–F12» por `PROS-F02…F12`), el número de un documento de trabajo citado en F8 («FIN-00-022») y el símbolo de
una serie ficticia («IDX-FICT-001» en `serie_ht01`).

## Cómo aplicarlo

- Mirar el contexto solo de lo que sería error, nunca de las citas válidas, y deducirlo del propio texto (la línea dice «JEL»,
  el documento define `PROS-F02`, el campo JSON no es `ficha_id`).
- No esconderlo: cada cita descartada sale como INFO con su ubicación y su motivo, para que la QA pueda discutirlo.
- La forma de un ID se saca de los ID que existen (todos los segmentos intermedios de las fichas empiezan por letra), no de
  una expresión inventada.
- El corpus no basta: el único desajuste real del código estaba en un literal (`"catalog_version": "4.0"` en `evaluador.py`),
  que solo salió al escanear también los `.py` del paquete.
- Para regenerar el informe: `python -m bloque_a.herramientas.verificador_ids --auditoria ../../docs/auditoria_ids_bloque_a.md`.
