# T-xx · <título del ticket>

| Campo | Valor |
| --- | --- |
| Estado | ABIERTO · PLANIFICADO · EN CURSO · EN QA · CERRADO · BLOQUEADO (motivo) |
| Pieza | <bloque o módulo; una sola> |
| Planifica · implementa · QA | <claude · astra · el otro agente o un revisor nuevo> |
| Aprobación del operador | <no necesaria · pendiente · aprobada el AAAA-MM-DD: «cita»> |
| Deuda técnica | T-xx en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

<Una frase: qué cambia y por qué ahora.>

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

<Una línea por cambio de estado: AAAA-MM-DD · estado · quién · nota.>
