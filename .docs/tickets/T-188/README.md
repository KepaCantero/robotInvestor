# T-188 · Decisión del Broker sin alterar el análisis ni la evaluación y Filtro, agrupación y recurrencia de consultas

| Campo | Valor |
| --- | --- |
| Estado | EN QA (r02: QA r01 NO APTO) |
| Implementación | Astra |
| QA independiente | Claude |

## Alcance y criterios de aceptación

1. PB-11. RET- en F5; `decision_broker` en F3 sin cambio de `estado`; CT-22 al Evaluador; ambos PRG resueltos; OPP-B incluida en el historial de aciertos; lección de producto con la comparación enviadas frente a descartadas cuando haya muestra. Ningún mensaje del bloque al Bloque B; ambos PRG RESUELTO; HAC- con n que incluye OPP-B.
2. PB-62. Solo las dudas que cambian una conclusión llegan al Broker, agrupadas; aviso `CONSULTA_RECURRENTE` y lección de normalización del CT-01. ≤ 3 mensajes CT-23 por RUN-; LEC- de producto creada.

## Registro

21-11-2026 · Plan local basado en el plan de pruebas V3.0 y el encargo de Claude.

El Evaluador escribe en F6 lecciones de producto a partir de decisiones anteriores al resultado y de consultas recurrentes de análisis distintos.
