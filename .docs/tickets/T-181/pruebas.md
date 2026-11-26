# Pruebas del 21-11-2026

- Python 3.12.6. Las once pruebas específicas pasan. Incluyen la CLI en modo informe y aplicación, retractación del editor de F8 con el verificador HTTP real y transporte simulado, y comprobación de F2 persistido al final del comando.
- PB-24 cubre retirada, aviso al Curador, reintento, lectura al corte, revisión con y sin respaldo alternativo en F3 y bajas en CT-21. Un fallo de conectividad del servicio de archivo conserva la referencia.
- PB-25 cubre recálculo de Q con motivo, rechazo de revisión obsoleta, reparación desde una copia idéntica, indicio sin confirmar y retractación confirmada.
- Los ocho mutantes propios provocan fallos de aserción. Se ejecutan en una copia temporal. La versión anterior carece del módulo y no recoge la nueva prueba.
- Comparación con 9ce57b2. El ciclo del 05-06-2026 entrega el mismo resumen al normalizar las rutas de salida. Backtest semanal en modo mock del 03-07 al 25-12-2026, 26 ciclos, 18 señales, 6 pronósticos y 4 resueltos. Los CSV de señales y pronósticos y el JSON de métricas son idénticos byte a byte. En el CSV de consumo solo varía el tiempo de ejecución. No se ha medido rentabilidad con un modelo real.
- Evidencias regeneradas con el servidor HTTP de prueba en la interfaz local. El plan recoge 349/349 pruebas automáticas citadas superadas, incluidos PB-24 y PB-25. Pasaron también las 337 pruebas de los scripts del repositorio.
- Suite completa del ejecutor A dentro de la comprobación general del repositorio: 8369 pruebas superadas. Ruff 2807 y mypy de A 102, dentro de las cuotas de la versión de partida.
- La comprobación general del repositorio pasó los doce controles, sin omisiones.

## Ronda r02

En la base de Claude el script r01 registró seis hallazgos, incluidas 22 listas de respaldo perdidas al segundo ciclo. El test de dos ciclos exige una oportunidad con raíces supervivientes e interrumpe la prueba si no existe. Los casos de la suite ejercen la deduplicación, el cierre del mes, el esquema de CT-11, el contenido de CT-21, las fechas, las revisiones sin observación HTTP y las fronteras de la rúbrica.

El script original de casos funcionales exige aceptar una fecha imposible. H-06 del dictamen exige rechazarla citando archivo y fila. La implementación sigue H-06 y la prueba de regresión comprueba el mensaje. Por ello ese script antiguo conserva un aviso, reproducible. La copia r02 del programa de mutantes adapta únicamente la ubicación del corte Q a la función compartida configurable. En sus 18 ensayos las pruebas detectaron los 18 fallos deliberados.

La regresión adicional de PB-24 interrumpe la escritura de la afirmación después de guardar la retirada de la evidencia en F2. El primer reintento corrige las raíces y PS1 y el siguiente conserva el historial íntegro. En la base anterior la afirmación conservaba una raíz retirada. M13 de la copia r02 aplica la misma duplicación de la retirada al condicional separado.

Integración con T-183. La lista de evidencias que conserva F3 se calcula después de enlazar los documentos y descartar las reproducciones. M17 en la copia portada r02 vacía esa lista final y comprueba que el ciclo detecta la pérdida del respaldo. En el ejecutor, el ciclo llama al registro de clase y F3 lee la lista después de que termine la transacción. El cargador de opciones previas reconstruye la lista desde F3. Ninguno de estos lectores usa la acumulación provisional eliminada.

En el recálculo de F3, la lista admisible de estados de verificación ya excluye todas las retiradas. M3 se porta a esa regla y añade FUENTE_RETIRADA entre los estados admisibles. El caso OPP-5 exige reevaluación cuando solo sobrevive una fuente secundaria B.

## Corrección local del 26-11-2026 sobre c4f2d1b

Las dos variantes de `test_retractacion_cli_al_corte_y_tras_interrupcion` fallaron en el código de partida y pasan tras la corrección. Ambas invocan `verificar-enlaces` y confirman la retractación con la huella del informe generado por HT-02. Solo se simulan el transporte HTTP del editor y, en el caso de recuperación, una interrupción al entregar el aviso.

- **Consulta histórica.** Antes y después de retirar el 5 de junio una fuente primaria A publicada en 2020, el corte del 4 ofrece los mismos metadatos. Se comprueban el lector en memoria, uno recién abierto, la fecha de publicación, la retirada desde el día 5 y el uso de la fuente en el flujo de evidencia de un bloque con reloj del día 4. F2 recibe el nivel A, el tipo primario y el año 2020.
- **Recuperación.** El primer intento guarda la baja y falla antes de entregar el CT-11. Repetir el mismo comando y el mismo fichero de decisiones retira la EVD y registra un único aviso. Un tercer intento conserva exactamente las filas de F2. Una decisión con otra huella sigue rechazándose. También se verifica que un barrido posterior sin red puede reconocer una retractación ya aplicada.
- **Lote de decisiones.** La retransmisión de una degradación y una retractación en el mismo archivo conserva Q 75 (B) y una sola baja. Cambiar el motivo invalida el reconocimiento de la decisión anterior.
- **Registros preexistentes.** Las bajas de cinco columnas conservan lectura, fecha y motivo. Una fila antigua sin copia de la ficha carece de los datos para reconstruir Q, temática y año. Tampoco acredita una decisión nueva del custodio.

Con Python 3.12, las 33 pruebas de T-181 pasaron. La selección de T-181, T-182, T-183, T-184, T-125, T-140 y V5 pasó sus 170 casos. Los servicios de red se sustituyeron por transporte local en los casos nuevos.

Las dos baterías de mutantes detectaron las 8 alteraciones originales y las 18 portadas. El programa funcional r01 mantiene la discrepancia documentada con H-06 respecto al rechazo de una fecha imposible.
