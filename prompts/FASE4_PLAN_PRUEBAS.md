# PROMPT — Fase 4 · Planes de pruebas y evidencias (los tres bloques)

> Sesión de ejecución y registro. Modelo: Sonnet. Requisito: Fases 0–3 verificadas.

---

FASE 4 — Ejecutar los planes de pruebas de los tres bloques y registrar las evidencias: bloque_a (67 pruebas), bloque_a_forex (86), bloque_b (204 + 88 comprobaciones G3B). Un bloque por sesión.

Kit de contexto: SOLO `09_Pruebas/Plan de pruebas…` del bloque de la sesión + el mapa de pruebas del ejecutor (`tests/MAPA_PLAN_DE_PRUEBAS.md` si existe).

Reglas de la fase:
- Cada prueba del plan se marca con su resultado REAL y la evidencia (comando + salida o referencia al test automático que la cubre). Prohibido marcar por leído/parecido: la lección de robotTrading es que los checkboxes de planes van rancios — verifica contra código y ejecución.
- Las pruebas que exigen API real NO se ejecutan en esta fase (se quedan «pendiente API» con su motivo): aquí todo es mock/determinista.
- Las que no se pueden automatizar se ejecutan manualmente y se registra cómo.
- Los fallos del plan NO se arreglan en silencio: cada uno es una entrada en docs/incidencias.md; solo se corrige lo que el propietario aprueba o lo trivialmente objetivo (typo en un nombre de test, p. ej.).

Entregables: `docs/evidencias_pruebas_<bloque>.md` por bloque con la tabla completa; suites de los tres bloques en verde; commits `fase4:`.

Criterio de éxito: abro el documento de evidencias de un bloque y cada fila «superada» tiene un comando que puedo re-ejecutar yo y da lo mismo.
