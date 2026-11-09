# T-62 · Alcance de las objeciones por eslabón

Estado inicial: PLANIFICADO. Base 0a865bb (T-61). Implementación de Astra, QA de Claude. El operador autorizó el caso pareado en el chat el 9 de noviembre.

## Objetivo y aceptación

Una objeción al eslabón de transformadores debe llegar a los candidatos expuestos con el motivo y la situación de la respuesta. La misma objeción sobre la tesis completa sigue pasando por PA5.

1. Reproducir ambos casos por la entrada normal del ejecutor con igual fecha, universo y objeción fuerte abierta.
2. Aceptar tanto ESLABON con identificador como TESIS con identificador del eslabón (las dos grafías de CT-B-17). Entregar una representación válida en el esquema congelado: CADENA con extensión x_eslabon_id. Los candidatos con exposición principal o secundaria reciben la advertencia. Mantener el límite de prioridad cuando sigue abierta y fuerte.
3. Verificar destinatarios ajenos, objeción resuelta y rechazo explícito de una referencia de eslabón desconocida. Incluir encargos por eslabón adicionales al ranking si se generan.
4. Mantener el contrato de salida y las pruebas de T-61. Riesgo principal: tratar una referencia desconocida como válida o interpretar una objeción al sector como local. Las objeciones específicas a emergentes quedan para una tarea propia.

Los identificadores se toman del mapa y la asignación de candidatos de la petición. El director recibe las objeciones del eslabón. Las puntuaciones numéricas del mapa siguen su procedimiento vigente. Este cambio no añade parámetros ni modifica los estados persistidos del marco global.

## Estado actual

EN QA. Astra implementó y verificó la corrección. Véase el [traspaso a Claude](handoff.md).
