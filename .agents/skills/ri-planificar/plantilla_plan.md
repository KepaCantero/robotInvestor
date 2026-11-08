# Plan · <título de la tarea>

- **ID de tarea:** <AAAA-MM-DD>_<pieza>_<tema> · **Deuda técnica:** T-xx (si aplica)
- **Pieza:** <bloque o módulo; una sola>
- **Planifica:** <claude | astra> · **Implementa:** <claude | astra> · **QA:** <el otro agente o un revisor nuevo>
- **Aprobación del operador:** <no necesaria | pendiente | aprobada el AAAA-MM-DD: «cita»>

## Objetivo

<Una frase: qué cambia y por qué ahora.>

## Alcance

- Entra: …
- No entra: …

## Diseño

- Contratos CT-G afectados y versión de esquema: …
- Estado persistido: <no cambia | cambia → versión de esquema nueva y migración MIG-xxx con su lista `cambia`>
- Números y su origen (configuración o Documento 0): …
- Cómo falla cerrado (qué pasa con datos ausentes, caducados o inválidos): …
- Decisiones del operador usadas como `[PROPUESTO]`: …

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| … | … | … |

## Criterios de aceptación (binarios)

1. CA-1: …
2. CA-2: …

## Plan de pruebas

| Prueba | Tipo (nominal, límite, fallo cerrado, regresión, migración, integración) | Criterio que cubre |
| --- | --- | --- |
| … | … | CA-1 |

## Documentos que habrá que actualizar

<LEEME de la pieza, deuda técnica, briefing (si cambia la arquitectura), Documento 0, memoria.>
