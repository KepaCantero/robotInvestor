# Relevo local a Claude · 21 de noviembre de 2026

El clon de trabajo es `Trabajo-T181`, rama local `develop`. La cola C-38 a C-47 corresponde a diez encargos. [T-181](../../tickets/T-181/handoff.md) tiene su propio relevo. Los nueve siguientes comparten una comprobación general del árbol resultante. Cada directorio contiene los criterios, pruebas reproducibles y un programa que introduce fallos deliberados para comprobar que las pruebas los detectan.

| Encargo | Cambio que debe revisar Claude | Límite o decisión |
|---|---|---|
| [T-182](../../tickets/T-182/handoff.md) | Una recuperación CT-07 de una fuente contaminada deja EVD, incidencia y baja de F9. G3-EST-06 bloquea contenido contaminado en la salida. | La detección usa las reglas R9 del proyecto. La atribución libre de una respuesta del modelo permite poner la pieza en cuarentena; una baja en el catálogo exige comprobar la fuente local. |
| [T-183](../../tickets/T-183/handoff.md) | El ejecutor distingue una raíz y veinte derivadas documentadas; G3 contrasta las cifras de las afirmaciones de cada oportunidad con F2. | La identificación de reproducciones sin atribución documental requiere curación. Los registros históricos sin traza de PS1 siguen siendo legibles. |
| [T-184](../../tickets/T-184/handoff.md) | La CLI incorpora treinta referencias en TA-06, TM-11 y TF-04 y mantiene el orden por calidad y fecha sin alterar el registro de bajas. | La entrada exige fecha de publicación para las altas nuevas. Las fichas antiguas sin fecha quedan detrás de las fechadas a igual calidad. Usar la configuración de la instancia para indicar el directorio operativo. |
| [T-185](../../tickets/T-185/handoff.md) | Un ciclo registra en F5 el presupuesto de cribado de N1, la reserva de exploración y las celdas ofrecidas. | El proveedor factura la llamada CT-06 completa. El presupuesto de exploración se conoce por separado; su coste efectivo dentro de esa llamada no se puede desglosar. |
| [T-188](../../tickets/T-188/handoff.md) | El Evaluador escribe en F6 lecciones de producto a partir de decisiones anteriores al resultado y de consultas recurrentes de análisis distintos. | La comparación es descriptiva. El umbral por grupo reutiliza evaluacion.min_calibrar [PROPUESTO]. Las lecciones de PRODUCTO solo van a agentes de producto. |
| [T-189](../../tickets/T-189/handoff.md) | CT-04 conserva P-03 cuando rechaza una celda; AUT lleva CPI y EAC; R8 registra la clase de dato sin guardar el valor. | EV estima el avance por las fases servidas anteriores a la fase solicitante. Una sola llamada no revela progreso interno. Las categorías de R8 no contienen fragmentos del dato. |
| [T-191](../../tickets/T-191/handoff.md) | Las caídas simuladas en F6 y F7 terminan con bloqueo justificado, comunicación CT-14 y registros en HA y F5. | El modo manual no acredita que se hayan ejecutado los controles de la herramienta caída. El resultado seguro es un bloqueo justificado. |
| [T-192](../../tickets/T-192/handoff.md) | F6 conserva la corrección de la base contaminada y las nuevas puntuaciones, y documenta la decisión de sombra mediante comparaciones pareadas y DM-HLN. | Se evalúan ordenaciones observadas y resultados disponibles antes del cierre. Una sombra sin muestra suficiente se retira. Confirmar una propuesta en F6 no autoriza a relajar parámetros de producción. El estudio no sustituye a un proveedor con vintages históricos. |
| [T-193](../../tickets/T-193/handoff.md) | Comprueba apertura por duración, cierre tras dos lecturas y deduplicación concurrente. | El operador debe fijar el objetivo de segundos y verificar la recuperación bajo carga real. Las órdenes del monitor no despliegan trabajadores físicos. |

La revisión independiente se realiza en la sesión de Claude. El operador mantiene la publicación en GitHub pendiente de autorización. Si aparecen hallazgos, registrar el dictamen en el ticket correspondiente antes de la siguiente ronda.

## Comparación frente a la versión 9ce57b2

Python 3.12.6 y cliente simulado. El ciclo del 05-06-2026 conserva las tres oportunidades, el estado, los entregables por nombre y el consumo. En las 26 semanas del 03-07 al 25-12-2026 coinciden los ficheros de 18 señales y 6 pronósticos; 4 pronósticos quedaron resueltos. El único cambio de métricas agregadas está en el consumo: 112 llamadas en ambos casos, 173796 → 174950 tokens de entrada y 53,9873 → 54,0592 UC. Los tiempos por ciclo dependen del equipo. El ejemplo utiliza datos sintéticos.

## Pruebas de entrega

Los diez tickets acumulan 29 casos específicos y 25 mutaciones detectadas en copias temporales. El [informe del plan](../../../docs/evidencias_pruebas_bloque_a.md) recoge 365 comprobaciones automáticas citadas. Para reproducir, ejecutar desde la raíz `.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar` y `bash tools/check_all.sh`. Las pruebas de HT-02 necesitan poder abrir un servidor local.

## Compatibilidad comprobada el 22 de noviembre

La primera pasada completa detectó 16 fallos. En el commit local `64dc158` se admite una referencia antigua sin registro de bajas y una respuesta de catálogo que omite la lista de incidencias. También se actualizó el ejemplo de CT-06 que comprueba su formato: el único cambio observado fue el campo opcional `reparto_cribado` de T-185. Los 206 casos de los dos módulos afectados pasaron tras la corrección.
