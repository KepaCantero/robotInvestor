# T-193 · Cola saturada y apertura de instancia

| Campo | Valor |
| --- | --- |
| Estado | EN QA (r01, revisión independiente pendiente) |
| Implementación | Astra |
| QA independiente | Claude |

## Alcance y criterios de aceptación

1. PB-18. Al superar cola > 3 o tiempo > 2× objetivo, ORD- ABRIR con cálculo c = ⌈λ/(μ·0,75)⌉; escritura de F2 serializada por hash sin conflictos; ORD- CERRAR tras 2 lecturas con cola 0 y ρ < 0,30. Apertura ≤ 1 ciclo de lectura tras superar el umbral; cero duplicados en F2; tiempo medio de ingesta vuelve al objetivo.

## Registro

21-11-2026 · Plan local basado en el plan de pruebas V3.0 y el encargo de Claude.

Comprueba apertura por duración, cierre tras dos lecturas y deduplicación concurrente.
