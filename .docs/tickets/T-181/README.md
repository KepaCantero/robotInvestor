# T-181 · Qué ocurre cuando una fuente pierde su respaldo

| Campo | Valor |
| --- | --- |
| Estado | EN QA (r02: QA r01 NO APTO) |
| Planifica e implementa | Astra |
| QA independiente | Claude, pendiente |

## Objetivo y aceptación

PB-24 exige que un enlace roto de F7, confirmado y sin alternativa tras dos barridos, deje una baja trazable, el aviso CT-11, la evidencia retirada en F2, una revisión en F3 y el registro mensual CT-21. PB-25 exige que el custodio pueda reparar o recalificar una referencia cambiada y retirar una retractación confirmada. Rigen los apartados 13.3 a 13.6 del Documento 0 V5.3.

1. Cada baja confirmada aparece una sola vez en el registro y genera el aviso al Curador.
2. Una EVD afectada queda retirada y el siguiente ciclo revisa por separado las oportunidades vigentes.
3. El CT-21 identifica las bajas del mes.
4. La Q recalculada conserva el motivo. La reparación exige una copia con el contenido original y la retractación exige confirmación del custodio.
5. La pérdida de red, los reintentos y las consultas previas a la baja preservan la coherencia del estado.

## Diseño y alcance

El comando existente `verificar-enlaces` produce los informes. Con `--aplicar` actualiza las fichas operativas e informa al Curador. El ciclo lee las bajas conocidas a su fecha, revisa las oportunidades vigentes y comunica las bajas una vez cerrado el mes. La puntuación Q procede de la rúbrica del archivo y de una revisión documentada. FM conserva su tratamiento específico.

## Registro

21-11-2026 · Implementados el tratamiento de incidencias y la propagación. Véanse [análisis técnico](analisis-tecnico.md), [pruebas](pruebas.md) y [relevo](handoff.md). La revisión independiente corresponde a Claude.
