# T-61 · Objeciones y evaluación histórica del Bloque B

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | bloque_b |
| Planifica e implementa | Astra |
| Revisión independiente | Claude: APTO en r01 y r02 (ver [qa.md](qa.md)) |

- Pieza e ID: ejecutor B, 2026-11-09_bloque-b_objeciones-y-evaluacion.
- Planifica e implementa Astra. Claude realizará la revisión independiente.
- Alcance acordado el 9 de noviembre de 2026: «Solo Bloque B por ahora». Relación con T-53: aportación parcial a la revisión previa a la conexión. T-53 continúa abierta.
- Base de integración: 104f4c8. La comparación con c83b211 muestra idéntico contenido inicial para B.

## Objetivo y diseño

Trasladar los cambios locales de revisión de objeciones, evaluación histórica y ejemplos del crítico. Se conservan CT-B-17 y los contratos globales. Los campos adicionales del informe estadístico explican la muestra usada para certificar. El registro de certificados usa ese recuento en nuevas evaluaciones; el histórico ya escrito queda intacto. El estado del marco global no requiere migración.

El protocolo maestro de B, §§7, 9 y 12, regula las objeciones y la certificación. El mínimo de muestra y las réplicas proceden de la configuración de evaluación; el README del ejecutor contempla submuestrear periodos solapados. Los precios ausentes se marcan como no evaluables para ese símbolo. Se conserva el tratamiento documentado de las bajas. Quedan fuera los datos BCE, las instrucciones antiguas de agentes y la conexión al intermediario. No se introduce una decisión de perfil del operador.

## Criterios y pruebas

| Criterio | Comprobación |
| --- | --- |
| 1. Solo un verdadero lógico cierra una objeción fuerte y cambia la puerta correspondiente. | Casos unitarios con tipos diferentes y entrega completa con objeción abierta y cerrada. |
| 2. La ficha llega al seleccionador y este solo responde por sus candidatos. Un matiz débil permite completar el informe. | Dos ejecuciones pareadas, respuesta con identificador ajeno y caso con un único matiz. |
| 3. Una serie ausente o vacía no trunca el ranking de las demás. | Dos proveedores CSV con un símbolo afectado; contrastar el rendimiento de otra empresa. |
| 4. Los periodos superpuestos no cuentan dos veces para certificar. | Ventanas superpuestas y consecutivas, observación histórica sin fecha y exportación de un backtest. |
| 5. Los ejemplos del crítico son reproducibles sin red. | Ejecutar el par simulado dos veces y comparar salidas. Verificar que los tres casos manuales solo difieren en el dato del fabricante. |

Primero reproducir los fallos sobre el código original con las nuevas pruebas. Después ejecutar las suites y los controles del repositorio. Documentar los resultados y el traspaso a Claude. Riesgos principales: confundir simulación con eficacia del modelo y tratar una muestra reducida como prueba de independencia. Los informes deben declarar ambos límites.

Documentos afectados: README del ejecutor, documentos de esta tarea y traspaso a Claude en [handoff.md](handoff.md).

## Registro

- 2026-11-09 · Implementación y pruebas en 4bbc952.
- 2026-11-09 · EN QA · Astra adapta la documentación al espacio de trabajo de a6ceb76. Véase [traspaso](handoff.md).
- 2026-11-09 · CERRADO · claude · QA APTO (r01, 4 hallazgos bajos); rama fusionada en `develop` por avance rápido.
- 2026-11-09 · CERRADO · claude · QA r02 APTO (cobertura y comparación con el azar, 3 hallazgos bajos); `astra/bloque-b-backtesting-cobertura-y-azar` fusionada en `develop` por avance rápido.
- 2026-11-09 · CERRADO · claude · tras fusionar, en `develop`: gate completo 12/12 (A 58, A Forex 68, B 141); el marco común de C no se toca en estas ramas, así que no hacía falta `pruebas_marco.sh`.
