# T-68 · Revisión del Bloque B: evaluación de precisión frente a consumo y discusión de arquitectura

| Campo | Valor |
| --- | --- |
| Estado | EN REVISIÓN (evaluación de Claude hecha; revisión independiente de Astra pendiente; después, discusión de arquitectura con el operador) |
| Pieza | bloque_b |
| Planifica · implementa · QA | Claude (evaluación) · nada que implementar todavía · Astra (revisión independiente de la evaluación) |
| Aprobación del operador | Revisión pedida por el operador; ninguna mejora se implementa sin que él decida la arquitectura |
| Deuda técnica | T-68 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Evaluar el Bloque B con el objetivo del operador («la mejor relación precisión/consumo de tokens») antes de discutir su arquitectura y la de los demás bloques. Evaluación de Claude: `evaluacion_claude.md`. Encargo de revisión a Astra: `encargo_revision_astra.md`. Revisión de Astra: «revision_astra.md», pendiente.

## Alcance

- Entra: …
- No entra: …

## Diseño

- Contratos CT-G afectados y versión de esquema: …
- Estado persistido: <no cambia · cambia → versión de esquema nueva y migración MIG-xxx con su lista `cambia`>
- Números y su origen (configuración o Documento 0); cada parámetro nuevo con su valor por defecto y su pregunta del cuestionario (D-45): …
- Cómo falla cerrado: …
- Decisiones del operador usadas como `[PROPUESTO]`: …

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| … | … | … |

## Criterios de aceptación (binarios)

1. CA-1: …

## Plan de pruebas

| Prueba | Tipo (nominal, límite, fallo cerrado, regresión, migración, integración) | Criterio |
| --- | --- | --- |
| … | … | CA-1 |

## Scripts

<Scripts de `.docs/scripts/` que usa o crea este ticket.>

## Registro

- 2026-11-11 · ABIERTO · creado con nuevo_ticket.sh
