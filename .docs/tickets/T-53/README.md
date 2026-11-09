# T-53 · Revisión del Bloque A con el operador

| Campo | Valor |
| --- | --- |
| Estado | ABIERTO |
| Pieza | bloque_a |
| Planifica · implementa · QA | claude con el operador · por decidir · el agente que no implemente |
| Aprobación del operador | Necesaria: es una revisión con el operador (D-42) antes de conectar A |
| Deuda técnica | T-53 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Repasar con el operador cómo funciona hoy el Bloque A (V5.1) y qué le falta frente a la Constitución V0.6 y el marco común, y acordar las mejoras antes de conectarlo al resto (D-42, regla 9 del §14).

## Alcance

- Entra: resumen de cómo funciona A; huecos frente a la Constitución (núcleo + perfiles, contratos CT-G, probabilidades verificables, ficha de bloque, valores por defecto con su pregunta); lista priorizada de mejoras acordadas.
- No entra: implementar las mejoras (cada una tendrá su ticket); el Bloque B (siguiente revisión).

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

- 2026-11-09 · ABIERTO · creado con nuevo_ticket.sh
