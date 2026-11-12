# C-01 · Revisión de Astra del rediseño de A

Fecha: 12-11-2026. Base revisada: 3583c52. Revisión de diseño, sin implementación ni ratificación. La lectura global previa del 11-11 ya incluyó la propuesta de Claude; no se presenta esta revisión como ciega a ella.

## Resumen

1. **DE ACUERDO CON CAMBIOS** con núcleo común, perfiles y coordinación determinista.
2. Reproducidas 8 llamadas y 183.941 tokens aproximados en DIV; 77 y 1.661.929 con doce perfiles.
3. El ahorro futuro y la calidad del rediseño siguen sin demostrar: el simulador no los mide.
4. La crítica debe cubrir toda candidata que finalmente salga, incluidas las sustitutas, y auditar una muestra de descartes.
5. Mantener contratos, seguimiento, procedencia y un responsable de cada registro durante la migración.

## Evidencia y reproducción

Lecturas: arquitectura de A (archivo V4.0, contenido actualizado V5.1), configuración del ejecutor; PA-04/05/06/07/14 en `.docs/tickets/T-53/propuestas.md`, T-67; Constitución P12 y §§3 y 10; propuesta y encargo de esta carpeta. Entorno Python 3.12 creado con `.docs/scripts/preparar_entorno.sh`: 49 paquetes conformes a `tools/requisitos_entorno.txt`. Solo cliente mock; ninguna llamada API.

Desde `bloque_a/11_Ejecutor`:

```sh
../../.venv/bin/python ../../.docs/scripts/medir_consumo_a.py /tmp/ri-c01-div 2024-03-29
../../.venv/bin/python ../../.docs/scripts/medir_consumo_a.py /tmp/ri-c01-todos 2024-03-29 --config ../../.docs/diseno/bloque_a/evidencias_astra/perfiles.yaml
```

Las carpetas de salida deben ser desechables: el medidor las reemplaza. Salidas completas en [DIV](evidencias_astra/consumo_div.txt) y [doce perfiles](evidencias_astra/consumo_todos.txt).

| Caso | Llamadas / agentes | Sistema | Encargo | Total aproximado | Sistema / total |
| --- | --- | --- | --- | --- | --- |
| DIV | 8 / 7 | 167.928 | 16.013 | 183.941 | 91,29 % |
| Doce perfiles | 77 / 20 | 1.495.542 | 166.387 | 1.661.929 | 89,99 % |

Coinciden los redondeos de Claude. En doce perfiles, Contrarias hace 19 llamadas, Prospectiva 12, Curador 12 y Documentador 6. Los tokens se estiman por caracteres, no con el contador del proveedor. El tamaño del encargo real y el número de rondas pueden cambiar con las respuestas reales; ni la salida simulada ni el coste de caché simulado acreditan una factura real. No se validan aquí tarifas ni modelos comerciales. Los 300.000–500.000 tokens del rediseño son un objetivo por comprobar, no un resultado reproducido.

## Veredictos por decisión

| Decisión | Veredicto | Motivo y cambio necesario |
| --- | --- | --- |
| Analista común con kits | DE ACUERDO CON CAMBIOS | Compartir implementación, no mezclar contextos de perfiles. Kit versionado con conocimientos, datos, herramientas, exclusiones y casos de aceptación propios; el perfil sin datos suficientes no se activa. |
| Prospectiva una vez por ciclo | DE ACUERDO CON CAMBIOS | Agrupar solo si caben todas las candidatas y sus evidencias. Límite por tamaño de contexto y salida, lotes separados por perfil/horizonte y control de cobertura por ID. Una omisión no equivale a un pronóstico negativo. |
| Contradictor solo para encargos, una ronda | DE ACUERDO CON CAMBIOS | Selección provisional → crítica → selección final. Si una candidata cae, la sustituta pasa la misma crítica. Una objeción fuerte abierta impide entregar; el límite de rondas no la resuelve. Muestrear descartes para medir lo que el filtro deja escapar. |
| Sintetizador único | DE ACUERDO | Puede integrar y explicar un resultado estructurado inmutable. No cambia puntuaciones, selección, fechas ni pronósticos. Validar también el JSON final después de redactar, no solo antes. |
| GC1, G3 y coordinación a código | DE ACUERDO CON CAMBIOS | G3 y reglas conocidas sí. GC1 requiere catálogo de señales por perfil y ruta explícita para datos insuficientes; revisar falsos negativos. No convertir la ausencia de una señal conocida en prueba de ausencia de oportunidad. |
| Curación a código | DE ACUERDO CON CAMBIOS | Normalización y duplicados exactos sí. Identificar fuentes independientes o si un texto respalda una afirmación requiere evidencia adicional y evaluación semántica; no basta un hash distinto. |
| Auditoría a código/muestreo | DE ACUERDO CON CAMBIOS | El código verifica estructura y trazabilidad. Conservar auditoría semántica independiente por muestreo, que no puede sustituirse íntegramente por un esquema válido. |
| Evaluación y conocimiento fuera de A | DE ACUERDO CON CAMBIOS | I, K, biblioteca y registros con responsable explícito. Migrar solo cuando el receptor exista y conserve IDs e historia. Calificar el paso como «ningún riesgo» es demasiado fuerte. |
| Banco con cuatro alternativas | DE ACUERDO CON CAMBIOS | Mismos universos y cortes, costes y restricciones. Mock mide flujo/consumo aproximado; calidad exige casos etiquetados y evaluación prospectiva. Anonimizar historia no demuestra que el modelo no reconozca el episodio. |
| Migración por pasos | DE ACUERDO | Una modificación evaluable cada vez, criterios fijados antes, posibilidad de volver al diseño anterior y comparación por perfil. |

## Hallazgos que deben cerrarse antes de implementar

**A-01 · Alta · Crítica de la selección definitiva.** La propuesta sitúa crítica antes del top-3 definitivo. Exigir que cada ID entregado tenga contraste válido y que una sustitución invalide la cobertura anterior. Caso de aceptación: la mejor candidata cae y la cuarta entra; esta última no sale sin crítica.

**A-02 · Media · Tamaño y diversidad.** El corpus declara hasta tres opciones por tipo, no tres en todo el ciclo. Una llamada global de Prospectiva puede tener que cubrir muchos más casos que los ejemplos de tres o seis encargos. El presupuesto debe escalar por candidatas y evidencia. Sustituir «el coste deja de crecer con cada perfil» por «se reduce el coste incremental; sigue creciendo con los perfiles y casos procesados».

**A-03 · Alta · Migración de contratos y registros.** Quitar agentes no elimina sus responsabilidades. Mapear CT-01/02/03/04/05 al Orquestador y su adaptador; CT-06 al analista con perfil; CT-07/08/20/21 a servicios de evidencia/conocimiento; CT-09/10 al Motor; CT-11 a curación; CT-12 a Prospectiva; CT-13 a contraste; CT-14/16/17/18 a validación/auditoría; CT-15 a síntesis; CT-19/22 a I; conservar CT-23/24/25 (consultas, seguimiento encargado y credenciales por referencia). El cambio de propietario exige versiones y pruebas de compatibilidad, no renombrar emisores dentro del corpus congelado.

**A-04 · Media · Fronteras.** Mantener R21: A entrega ámbitos al Broker, no selecciona activos concretos ni decide por sí solo el envío a B. El «encargo a B» del diagrama es una propuesta que conduce el Orquestador según autorización. El seguimiento C6 no puede perderse al trasladar vigilancia a H: una oportunidad aún no invertida y una posición abierta tienen ciclos distintos.

**A-05 · Media · Medición de pérdida de cobertura.** Registrar descartes, motivo, perfil, corte y revisión muestral independiente. Medir tanto calidad de lo enviado como oportunidades válidas no enviadas; no usar únicamente la aceptación posterior por C como verdad, porque comparte entradas y sesgos.

## Respuestas a las cuatro preguntas

1. Adelantar el banco y el diseño de PA-06/07: sí. Adoptar recortes solo tras evidencia real suficiente. El rumbo de pauta común ya está aceptado en la tanda 1; el calendario de refactorización sigue sujeto a la enmienda y al encargo de implementación.
2. Respetar el alcance actual: las tareas de código citadas están RETIRADAS de la cola desde el 12-11. Esta revisión no las reactiva.
3. Crítica obligatoria de todo lo finalmente entregado, más muestreo de descartes. Una ronda es un presupuesto, no una garantía de resolución.
4. Misma pauta para A/B/C, sí; contratos, datos y criterios propios por función. El número de papeles no es una meta que prevalezca sobre calidad.

## Condiciones de aceptación propuestas

Matriz CT y propietarios completa; ninguna candidata entregada sin contraste requerido; ninguna omisión por truncamiento silenciosa; seguimiento C6 y consultas conservados; pruebas por perfil de falsos descartes y contaminación temporal; coste real de entrada, salida, reintentos y latencia registrado. Las tolerancias y presupuestos se fijan antes del experimento, sin introducir nuevos valores de producción en esta revisión.
