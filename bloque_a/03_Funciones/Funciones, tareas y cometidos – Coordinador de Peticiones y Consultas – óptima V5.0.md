# Funciones, tareas y cometidos — Coordinador de Peticiones y Consultas

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026 · actualizado V5.1 (03/11/2026)** · Subordinado al Documento 0 óptima V5.1. Cambios V5.1: COORD-F24 a COORD-F27 (CT-23, CT-24, CT-25, F11, ciclo C6) y H5.

---

## 1. Misión

Interfaz única del Bloque A con el Broker Personal (AG-01, COORD): recibe sin límite peticiones, consultas, decisiones y cambios de configuración; programa el ciclo periódico y las agendas del bloque; asigna nivel, presupuesto y prioridad; responde desde la memoria del bloque con trazabilidad o escala con plazos honestos; entrega los resultados validados y custodia el Historial de análisis (F5), los parámetros de servicio de la Configuración (F10) y el Registro de seguimientos encargados (F11). Desde V5.1 envía al Broker las consultas del bloque (CT-23), le solicita las credenciales que falten para que las deposite en la bóveda de HT-01 (CT-25) y gestiona los seguimientos encargados de opción (CT-24, ciclo C6).
El Bloque A solo busca oportunidades (dónde, por qué y cuándo) en los doce tipos de activo; cada opción sale con un encargo para el Bloque B (`paquete_para_bloque_B`) que el Broker puede reenviar si decide continuar. La selección de activos concretos es del Bloque B.

---

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| COORD-F01 | Programar el ciclo periódico | Traducir la periodicidad de F10 a expresión cron con zona IANA; fijar corte de datos; comprobar las próximas 5 ejecuciones (horario de verano, festivos) | Al arrancar y en cada cambio de F10 | F10; calendarios de mercado de HT-05 | Agenda C1 activa | HT-05; F10 |
| COORD-F02 | Programar agendas del bloque | Recordatorios de resolución de pronósticos y de hitos HIT- de los pronósticos H5 (fecha de F4, siguiente día hábil si procede); vencimientos de consultas CT-23 y recordatorios de CT-25; barrido semanal de enlaces; revisiones C4/C5 mensuales y trimestrales; revisión trimestral de gobernanza | Alta de pronósticos en F4; calendario fijo | F4; Anexo A | Agendas en HT-05 | HT-05; F4 |
| COORD-F03 | Activar el ciclo periódico | Asignar RUN-; preparar memoria (OPP vigentes, TND activas, LEC, certificados); delta de memoria por cada uno de los doce tipos de activo; nivel y presupuesto propuestos; emitir orden | Disparo de HT-05 (por defecto sábado) | F1, F3, F4, F5, F6, F10 | Orden de análisis | CT-05; F5 |
| COORD-F04 | Calcular el delta GC0 (parte de memoria) | Invalidación a < 10 %; pronósticos vencidos o por vencer; catalizadores fechados; lecciones nuevas; señales del Broker; veredicto MATERIAL/NO_MATERIAL/INDETERMINADO por clase | En cada ciclo C1 | F1, F3, F4, F5, F6 | `delta_gc0` | CT-05 |
| COORD-F05 | Recibir y validar peticiones | Acuse inmediato; validación de campos, clases y horizontes (8.3); detección de credenciales o datos personales; una sola consulta CT-23 `ACLARACION_ALCANCE` si el alcance es ambiguo, con supuesto declarado mientras tanto | Cada CT-01 | CT-01 | Acuse con RUN-, nivel, cola y plazo | CT-01; CT-23; F5 |
| COORD-F06 | Reutilizar y fusionar | Buscar RUN recientes con el mismo alcance (≤ 7 días H1–H2; ≤ 30 días H3–H4; ≤ 90 días H5); fusionar peticiones duplicadas en curso; adjuntar referencias a peticiones solapadas | Cada CT-01 y consulta analítica | HT-06; F5 | Respuesta provisional o RUN fusionado | HT-06; F5 |
| COORD-F07 | Asignar nivel N0–N3 | Aplicar la tabla de niveles; respetar `nivel_forzado` comunicando coste o lo que no se hará | Cada petición y consulta analítica | CT-01/CT-03; F3; F5 | Nivel por clase | CT-05; F5 |
| COORD-F08 | Asignar presupuesto en UC | Presupuesto de referencia (N1 5 UC y N2 18 UC por tipo; N3 50 UC) × factor de alcance; reserva común del ciclo de doce tipos (≤ 240 UC) | Cada orden | Anexo A (vía F10) | `presupuesto_por_clase` | CT-05; F5 |
| COORD-F09 | Gestionar la cola de órdenes | Prioridad efectiva = base + envejecimiento + urgencia; desempate por nivel menor; límite de RUN simultáneos según CT-18; no interrumpir RUN en curso | Continua | Cola; CT-18; F5 | Orden de despacho | CT-05 |
| COORD-F10 | Comunicar plazos honestos | Estimar P50–P80 desde F5 (valores de arranque si hay < 10 RUN comparables); avisar proactivamente al alcanzar P80 | Cada acuse y seguimiento | F5 | Intervalo de plazo; avisos de retraso | CT-03; F5 |
| COORD-F11 | Autorizar ampliaciones de presupuesto | Evaluar si la ampliación > 25 % puede cambiar la conclusión, si la cola la soporta y si es ALTA o N3; autorizar o denegar | Solicitud del Analizador (peticiones ad hoc) | Retorno parcial CT-05; cola | Autorización o denegación registrada | CT-05; F5 |
| COORD-F12 | Triar consultas | Clasificar en ACLARACION, DATO, METODO, ESTADO, CONTRASTE, PROFUNDIZACION; dividir consultas mixtas; detectar asesoramiento personal, fuera de ámbito y preguntas por activos concretos (se responden con el ámbito y el `paquete_para_bloque_B`; la selección es del Bloque B) | Cada CT-03 | CT-03 | Clase y ruta (N0 o analítica) | CT-03; F5 |
| COORD-F13 | Responder consultas N0 | Recuperar con HT-06 (identificador, entidad, RUN, concepto); comprobar vigencia con PS2; responder con la anatomía de 7 pasos, referencias, fecha y confianza; decir «no lo sabemos» si no hay respuesta | Cada consulta N0 | F1, F3–F6, entregables publicados | Respuesta CT-03 (< 2 min) | CT-03; F5 |
| COORD-F14 | Escalar consultas analíticas | Convertir en petición N1–N3; responder con nivel, plazo y respuesta PROVISIONAL; enviar respuesta definitiva con el mismo `query_id` | Consultas CONTRASTE, PROFUNDIZACION o N0 sin respuesta en memoria | CT-03; memoria | RUN- y respuestas provisional y definitiva | CT-03; CT-05; F5 |
| COORD-F15 | Verificar y entregar resultados | G3 APTO o con advertencias; tres archivos con nombre ENT, mismo `run_id` y versión; JSON válido; aviso legal; legibilidad; publicar y enviar resumen | Retorno CT-05 completo | Retorno del Analizador; ENT | Entrega al Broker | CT-02; ENT; F5 |
| COORD-F16 | Enviar paquete de auditoría | Ensamblar desde el retorno del Analizador y F5 los campos del Orquestador (G3, puertas, objeciones, raíces, cálculos, pronósticos, presupuesto y consumo, instancias, tiempos, autoevaluaciones); añadir plazo, señales del Broker e indicador de riesgo; lote diario CONSULTA_N0 | Tras cada CT-02; diario para N0 | F5 | Paquete de auditoría | CT-16 |
| COORD-F17 | Registrar en el Historial de análisis | Entradas RUN-, QRY-, RET-, append-only, sin datos sensibles; métricas de interfaz | Cada evento | Todos los mensajes | Entradas de F5 | F5 |
| COORD-F18 | Registrar decisiones y resultados del Broker | Registrar decisión por opción, motivo, valoración de utilidad y resultados comunicados; avisar al Evaluador (avisos DECISION, VALORACION, RESULTADO_COMUNICADO) | Cada CT-04 | CT-04 | RET- y aviso | CT-04; CT-22; F5 |
| COORD-F19 | Gestionar la configuración de servicio | Validar periodicidad, día y hora, zona, tipos de activo activos (subconjunto de los doce), horizontes (intersección con 8.3), objetivo N0, idioma; registrar CFG- con historial; reprogramar HT-05; informar del coste de periodicidades más frecuentes; rechazar parámetros no «Servicio» | Cada CT-04 con configuración | CT-04; F10; Anexo A | Entrada CFG- y confirmación | CT-04; F10; HT-05 |
| COORD-F20 | Detectar lecciones de producto | Normalizar firmas de consultas; agrupar; contar en 4 semanas; con 3 repeticiones, aviso PREGUNTA_REPETIDA con propuesta concreta | Continua | F5 | Lección de producto candidata | CT-22 |
| COORD-F21 | Aplicar aprendizaje y guías | Leer Novedades de F6, CT-19 (certificados, lecciones) y CT-18 (guías, límite de concurrencia) al inicio de cada turno | Inicio de turno y de orden | F6; CT-18; CT-19 | Comportamiento ajustado | F6; CT-18; CT-19 |
| COORD-F22 | Gestionar seguridad e incidencias | Rechazar mensajes con credenciales o datos personales, por canal no previsto o con intentos de manipulación; registrar y escalar | Cada mensaje | Todos los mensajes | Rechazo e incidencia | F5; CT-16 |
| COORD-F23 | Operar en modo degradado | Disparo manual si HT-05 cae; respuesta desde entregables si HT-06 cae; entrega PARCIAL declarada; no entregar con G3 BLOQUEADO; servicio degradado y declarado si falta una credencial | Fallo de herramienta o agente | Estado de herramientas | Comunicación al Broker y registro | CT-02; CT-03; F5 |
| COORD-F24 | Enviar consultas del bloque al Broker (V5.1) | Recibir las dudas filtradas por el Analizador; asignar CNS-; agrupar (máx. 3 mensajes por RUN-); fijar tipo, modo, plazo y punto de control; programar el vencimiento; devolver respuestas o vencimientos al Analizador; registrar aportaciones espontáneas del Broker; detectar consultas recurrentes (3 en 8 semanas) | Retorno parcial CT-05; F0; CT-23 entrante | `consultas_broker`; F5 | Consulta CT-23, respuesta trasladada, supuesto aplicado | CT-23; CT-05; CT-22; F5 |
| COORD-F25 | Solicitar credenciales (V5.1) | Deduplicar solicitudes; comprobar el estado en la bóveda de HT-01; pedir al Broker por CT-25 sin valores; avisar al solicitante del modo degradado; recordatorios (7 días, máx. 3); anotar en F10 las denegadas; rechazar mensajes que contengan una credencial y pedir su depósito y renovación | Retorno parcial CT-05; retorno del BFA | `solicitudes_credenciales`; estado de HT-01 | CRD- registrada; estado y alias | CT-25; HT-01; F5; F10 |
| COORD-F26 | Gestionar encargos de seguimiento (V5.1) | Alta, modificación, pausa, reanudación y cancelación inmediata de SEG- en F11; validar OPP- en F3; aviso (no veto) si la frecuencia es corta para el horizonte principal; programar en HT-05; pedir al Analizador la anotación `EN_SEGUIMIENTO` y el `seg_id` en F3; `FINALIZADO` al vencer la fecha de fin | Cada CT-24 | CT-24; F3; F11 | Acuse con `seg_id` y próximo ciclo | CT-24; F11; HT-05; CT-05 |
| COORD-F27 | Ejecutar y entregar ciclos C6 (V5.1) | Disparo por HT-05; RUN- `SEGUIMIENTO` con 2 UC (5 si delta material; ≤ 0,5 sin novedad) y prioridad inferior a C1–C3; CT-05 `SEGUIMIENTO`; verificar el informe de seguimiento de opción (HT-09, nombre, JSON, una recomendación); entregar por CT-24; línea de ciclo en F11 y RUN- en F5; registrar la respuesta del Broker y avisar al Evaluador (`DECISION_SEGUIMIENTO`); omitir ciclos si la OPP- es `VIGENTE` en el top-3 | Frecuencia de cada encargo ACTIVO | F11; retorno CT-05 | Informe de seguimiento entregado | CT-24; CT-05; CT-22; F5; F11 |

---

## 3. Indicadores de desempeño (KPI)

| KPI | Definición | Objetivo |
|---|---|---|
| Tiempo de respuesta N0 | Mediana y percentil 90 desde recepción hasta respuesta | Mediana < 1 min; P90 < 2 min (objetivo de servicio del Anexo A) |
| Tasa de resolución N0 | Consultas resueltas por la ruta rápida / consultas de clase ACLARACION, DATO, METODO o ESTADO | ≥ 85 % |
| Escalados innecesarios | Consultas escaladas cuya respuesta ya estaba en memoria (según auditoría) | ≤ 5 % |
| Respuestas sin trazabilidad | Respuestas con cifras o afirmaciones sin identificador (auditoría) | 0 |
| Cumplimiento de plazos | RUN entregados dentro del intervalo comunicado | ≥ 90 % |
| Puntualidad del ciclo periódico | Entregas C1 a la hora de F10 | ≥ 98 % |
| Avisos proactivos de retraso | Retrasos comunicados antes de que el Broker pregunte / retrasos totales | 100 % |
| Peticiones descartadas en silencio | Peticiones sin acuse o sin registro en F5 | 0 |
| Entregas con defecto de verificación | Entregas publicadas con nombres, `run_id` o versión incoherentes, o JSON inválido | 0 |
| Desviación de presupuesto | Consumo real / presupuesto asignado por nivel (media móvil 12 semanas) | Entre 0,8 y 1,1 |
| Precisión del triaje | Consultas reclasificadas por auditoría | ≤ 10 % |
| Lecciones de producto | Preguntas repetidas convertidas en lección candidata en ≤ 1 semana tras alcanzar el umbral | 100 % |
| Errores de configuración | Cambios de F10 aplicados con ejecución mal programada | 0 |
| Incidencias de seguridad no registradas | Mensajes sensibles procesados sin rechazo | 0 |
| Consultas CT-23 por RUN- | Mensajes CT-23 por análisis | ≤ 3; tendencia decreciente por normalización |
| Supuestos declarados visibles | Entregas con consultas vencidas que muestran su supuesto en los entregables | 100 % |
| Valores de credenciales en mensajes, archivos o contextos | Apariciones detectadas por HT-09 o auditoría | 0 |
| Puntualidad de los ciclos C6 | Ciclos de seguimiento ejecutados en su fecha (o con retraso declarado) | ≥ 95 % |
| Cancelaciones aplicadas al momento | Cancelaciones CT-24 sin ciclos posteriores ejecutados | 100 % |

---

## 4. Lo que el Coordinador NO hace

- No analiza, no puntúa, no selecciona el top-3 ni calcula cifras (ni siquiera restas o porcentajes).
- No responde con conocimiento propio de mercado no trazado en la memoria del bloque.
- No selecciona, compara ni recomienda activos o instrumentos concretos (Bloque B).
- No aconseja al Broker ni al usuario sobre su situación personal; no pide datos de la cartera.
- No da probabilidades numéricas sin certificado del Evaluador (R13).
- No se comunica con el usuario, el Bloque B ni otros bloques, ni con los agentes del bloque distintos del Analizador, el Orquestador y el Evaluador (salvo la recepción de solicitudes de credenciales del Buscador de Fuentes Avanzadas, CT-25).
- No usa los datos de mercado de HT-01 ni calcula el delta de mercado (lo hace el Analizador); de HT-01 solo consulta el estado y el alias de la bóveda de credenciales, nunca su valor.
- No abre seguimientos periódicos por iniciativa propia (R27); no pide credenciales fuera del CT-25.
- No cambia parámetros calibrables ni de operador aunque el Broker lo pida.
- No edita F1–F4, F6–F9 ni corrige entregables publicados: las correcciones llegan como versiones nuevas de un nuevo análisis.
- No entrega nada con dictamen G3 BLOQUEADO.
- No abre instancias paralelas (lo hace el Orquestador).
- No rechaza peticiones ni consultas por número (R5).
