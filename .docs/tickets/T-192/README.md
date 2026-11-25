# T-192 · Fuga de información en evaluación detectada y Recalibración dentro de bandas con evaluación sombra

| Campo | Valor |
| --- | --- |
| Estado | EN QA (r02: QA r01 NO APTO) |
| Implementación | Astra |
| QA independiente | Claude |

## Alcance y criterios de aceptación

1. PB-34. `comprobacion_fuga` FALLIDA en la métrica afectada; recálculo con vintage y tasa base sin fuga como entrada nueva; recalibración bloqueada hasta disponer de métricas limpias; la resolución usa la primera publicación. Ningún AJU- ni CERT- apoyado en métricas FALLIDA; corrección registrada en F6.
2. PB-35. AJU- con cambio ≤ 0,05 y acumulado ≤ 0,15; CFG- con `methodology_version` 4.0 → 4.1; HT-03 calcula en paralelo con 4.0; al cierre, CONFIRMADO o REVERTIDO según la regla, con registro. Bandas respetadas; sombra registrada; decisión documentada con DM-HLN.

## Registro

21-11-2026 · Plan local basado en el plan de pruebas V3.0 y el encargo de Claude.

F6 conserva la corrección de la base contaminada y las nuevas puntuaciones, y documenta la decisión de sombra mediante comparaciones pareadas y DM-HLN.
