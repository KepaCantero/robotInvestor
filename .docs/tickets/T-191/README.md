# T-191 · Modo degradado: herramienta caída

| Campo | Valor |
| --- | --- |
| Estado | EN QA (r02: QA r01 NO APTO) |
| Implementación | Astra |
| QA independiente | Claude |

## Alcance y criterios de aceptación

1. PB-52. El Analizador eleva por CT-14; el Orquestador ejecuta G3 manual con etiqueta; nunca APTO por defecto; la clase sin datos se cierra con alcance reducido declarado (PS2). Entrega con limitaciones declaradas o bloqueo justificado; ninguna cifra sin dato.

## Registro

21-11-2026 · Plan local basado en el plan de pruebas V3.0 y el encargo de Claude.

Las caídas simuladas en F6 y F7 terminan con bloqueo justificado, comunicación CT-14 y registros en HA y F5.
