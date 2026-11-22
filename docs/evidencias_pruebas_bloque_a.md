# Evidencias del Plan de pruebas del Bloque A (Fase 4, T-116)

Generado por `.docs/scripts/evidencias_plan_a.py --ejecutar` el 2026-11-22 sobre el commit `64dc158`, con el cliente simulado (`MockClient`): sin red, sin clave y sin coste. No se edita a mano: se regenera.

Qué significa cada resultado:

- **Superada:** las pruebas citadas pasan y comprueban todo el criterio de aprobación del plan, salvo lo que solo existe con tiempo real o con el modelo real, que se dice en «No comprueba».
- **Superada en parte:** las pruebas citadas pasan, pero queda alguna cláusula del criterio que el ejecutor podría comprobar y ninguna prueba comprueba. Está en «No comprueba».
- **Pendiente API:** el criterio lo juzga el modelo real; no se ejecuta en esta fase.
- **Requiere usuarios**, **Revisión documental:** no son pruebas del ejecutor.
- **Sin prueba:** ninguna prueba automática cubre el caso.
- **FALLA**, **No ejecutada:** alguna prueba citada falla o no se pudo ejecutar.

Con el cliente simulado se valida la tubería (canales, archivos, puertas, herramientas, cálculos), no la calidad analítica de los agentes (R22).

## Resumen

| Resultado | Pruebas del plan |
| --- | --- |
| Superada | 50 |
| Superada en parte | 9 |
| Pendiente API | 7 |
| Requiere usuarios | 1 |
| **Total** | **67** |

## Tabla

| Prueba | Resultado | Comprueba | No comprueba |
| --- | --- | --- | --- |
| PB-01 Ciclo periódico completo de extremo a extremo | Superada | Entregables con su nombre, archivos F1–F5, G3 APTO, tres opciones como máximo, RUN- completo en F5 y pronósticos congelados; con un ciclo anterior en memoria, N2 donde GC0 ve cambio material y N1 en el resto; los mensajes del ciclo (CT-05, CT-06, CT-11, CT-12, CT-13, CT-15, CT-02) son todos del catálogo, y solo el Coordinador escribe al Broker; sin G3 APTO no se congela ningún pronóstico ni se entrega. | La entrega en hora: el reloj es simulado. Que sean precisamente RV, RF y MP las que cambian depende de los datos sintéticos; se afirma la regla (nivel según GC0). |
| PB-02 Top-3 con menos de tres elegibles | Superada | Motivo obligatorio con menos de tres opciones (ciclo y HT-09) y segunda pasada en banda marginal (HT-03). El caso sembrado del plan en un C1 de DIV (T-159): de las candidatas, dos superan E y A, una queda en banda marginal (primera pasada en el umbral, segunda con media 57,5, que HT-03 redondea a 55) y el resto lejos; salen exactamente dos opciones, la marginal no aparece y su segunda pasada queda en F3 como la que decide; el motivo de «menos de tres» da las candidatas analizadas, el motivo de cada una y qué tendría que ocurrir; C03 (G3-CON-03) en OK en las dos validaciones G3, y ninguna opción entregada incumple un umbral. | La «E = 58» del plan no existe como total: HT-03 redondea a múltiplos de 5 y las dimensiones van de 10 en 10; se siembra una segunda pasada de media 57,5. El universo de ejemplo tiene seis ámbitos DIV, no siete. |
| PB-03 Clase sin ninguna opción elegible | Superada | Un tipo con cero opciones se entrega sin relleno (por presupuesto agotado) y HT-03 admite cero opciones. El caso del plan en un C1 (T-159): las candidatas de ALT no superan PS3 (sin universo invertible para un minorista); ALT queda con cero opciones y semáforo GRIS, cada candidata queda en F3 no elegible con PS3 en su motivo, el técnico da el motivo por candidata, el visual no pinta ninguna tarjeta de ALT y lo explica en lenguaje llano, y el resto del ciclo se entrega. | Que el Auditor no registre hallazgo por ello, que exige el modelo real. El universo de ejemplo tiene dos ámbitos ALT y uno pasa el cribado: la prueba lo hace con esa finalista, no con tres. |
| PB-04 Misma tendencia, estrategias distintas por clase | Pendiente API | — | Las lentes por tipo de activo las aplica el modelo. |
| PB-05 Marco de otra clase aplicado sin justificación | Pendiente API | — | Lo detecta el Auditor con el modelo real. |
| PB-06 Consulta N0 sin escalado | Superada | Clase ACLARACION y ruta N0; cada referencia de la respuesta es el identificador de una entrada de F1–F6 (no solo un prefijo válido); QRY- en F5 con sus referencias; cero encargos CT-05, ningún RUN- nuevo y consumo de 1 UC como máximo. | El tiempo de respuesta real (< 2 minutos) y que cada afirmación del texto del modelo real lleve su referencia. |
| PB-07 Consulta que escala a análisis | Superada | Clase CONTRASTE y ruta ANALITICA; respuesta provisional por CT-03 con el nivel y el plazo; RUN- ad hoc de alcance mínimo enlazado a la QRY-; al terminar el RUN-, respuesta final por CT-03 (después de la provisional y de la entrega CT-02), enlazada a la QRY- y al RUN-, con referencias que existen en F1–F5 (el RUN- y las OPP- del top-3 con sus TND-, CLM- y PRG-), validada contra su esquema y por la mensajería, una sola vez; si el RUN- falla, no entrega o no se lanza, la final lo dice sin citar nada (T-162); un fallo de integridad del almacén para la consulta sin responder, y una final que no salió la envía la consulta siguiente, enlazada a la provisional registrada en F5 (T-169). | El tiempo real de la respuesta provisional (< 2 minutos) y que el Coordinador no responda con conocimiento propio con un modelo real (modo sombra). En el ejecutor síncrono la provisional se crea al terminar el RUN-, justo antes de la final. |
| PB-08 Ráfaga de peticiones sin límite | Superada en parte | Idempotencia y acuse por mensaje; cola del monitor HT-08. | La ráfaga del plan: el ejecutor atiende cada CT-01 y cada CT-03 en el momento, sin cola de peticiones con prioridad y envejecimiento ni presupuesto por nivel (INC-T159-01). El p90 de N0 es de tiempo real. |
| PB-09 Cambio de periodicidad por el Broker | Superada en parte | La periodicidad cambia en F10 (P-01) desde su fecha de efecto, los valores no válidos se rechazan y se avisa al Evaluador (CT-22). | El disparo del siguiente C1 en la fecha nueva: HT-05 tiene `proxima_ejecucion`, pero nada la llama con el P-01 de F10, y el P-01 que escribe el CT-04 guarda la hora de entrega y pierde la del ciclo (INC-T159-01). Que ningún otro parámetro cambie. |
| PB-10 Configuración no permitida rechazada parcialmente | Superada | Estado APLICADA_PARCIALMENTE; el umbral E y la celda ALT×H1 se rechazan con su motivo y la celda sigue sin aplicarse; P-02 aplicado; ningún otro parámetro de F10 cambia salvo la lista de horizontes; HA sin incidencia de escritura. CT-04 conserva P-03 cuando rechaza una celda; AUT lleva CPI y EAC; R8 registra la clase de dato sin guardar el valor. | — |
| PB-11 Decisión del Broker sin alterar el análisis ni la evaluación | Superada | La decisión del Broker se anota sin cambiar el estado de la opción en F3 y se avisa al Evaluador (CT-22); al vencer, los PRG de la opción enviada y de la descartada quedan RESUELTO y el historial de aciertos los cuenta; ningún mensaje al Bloque B. El Evaluador escribe en F6 lecciones de producto a partir de decisiones anteriores al resultado y de consultas recurrentes de análisis distintos. | — |
| PB-12 Campos de decisión y paquete para el Bloque B | Superada | El JSON entregado cumple el esquema publicado y G3 APTO (C01, C10 y C11 en OK); la relevancia de cada opción sigue la regla del Anexo A (una CRI nueva, ALTA; una RF de seguimiento, MEDIA o BAJA); `siguiente_paso_sugerido`, `reversibilidad` y `que_cambiaria_la_conclusion` presentes; `paquete_para_bloque_B` con una entrada por opción y los mismos datos; HT-09 bloquea un paquete para B incompleto. | — |
| PB-13 GC0 negativo con arrastre verificado | Superada en parte | Nivel N1 con 5 UC como máximo, arrastre verificado, sin candidatas nuevas, solo modo ligero; las celdas de rotación exploratoria salen de la configuración. Un ciclo registra en F5 el presupuesto de cribado de N1, la reserva de exploración y las celdas ofrecidas. | AS-06 corresponde al Auditor con el modelo real. La llamada conjunta no mide consumo efectivo por símbolo. |
| PB-14 Arrastre con invalidación activada | Superada | Opción CERRADA con motivo INVALIDACION en F3 y en el paquete; sus PRG siguen ABIERTO en F4. | La explicación en «cambios frente al ciclo anterior», que es texto del modelo real. |
| PB-15 Reglas de parada por rendimientos decrecientes | Pendiente API | — | Las iteraciones del Analizador las decide el modelo. |
| PB-16 Presupuesto agotado: alcance reducido, verificación intacta | Superada | Estado PARCIAL, limitación en el informe técnico y en el visual, laguna declarada en F5, menos candidatas investigadas en RV, y G3 en F6 y F7 con las mismas comprobaciones que un ciclo completo, ninguna sin aplicar y C08 (ninguna cifra sin origen) en OK. | — |
| PB-17 Ampliación de presupuesto en el ciclo periódico | Superada | Una ampliación que puede cambiar el top-3 y cabe en el tope se autoriza; una que no puede cambiarlo o que supera el tope se deniega; cada decisión deja su AUT- en HA con el motivo; en un ciclo, la denegada cierra con alcance reducido y el consumo real queda en F5. CT-04 conserva P-03 cuando rechaza una celda; AUT lleva CPI y EAC; R8 registra la clase de dato sin guardar el valor. | — |
| PB-18 Cola saturada y apertura de instancia | Superada en parte | El monitor ordena abrir instancia (ORD-) de un agente sin estado al superar el umbral de cola. Comprueba apertura por duración, cierre tras dos lecturas y deduplicación concurrente. | Falta medir la vuelta al objetivo bajo carga real y con un tiempo objetivo acordado. |
| PB-19 Agente de instancia única saturado | Superada | Ninguna ORD- para AG-02 con seis órdenes CT-05 en cola (ni para ningún agente de instancia única, ni con umbral 0): el monitor deja un registro CAR- de su saturación, que el ciclo escribe en HA; la cola se reordena por prioridad (C1–C3 antes que C6; ALTA, NORMAL, BAJA; fecha objetivo; llegada) en el monitor y en el CAR-; el CAR- de un agente del camino de la entrega (AG-01, AG-02, AG-18) lleva el aviso de plazos al Coordinador, que lo lee en HA (AG-19 y AG-20 no avisan); si la saturación se repite en otro run, P3- PENDING_OPERATOR en HA, una sola mientras está abierta (T-178, INC-T178-01). | — |
| PB-20 Instrucción incrustada en una fuente | Superada | La instrucción se neutraliza, queda una incidencia MANIPULACION, ninguna puntuación cambia y el texto no llega a los entregables. Una recuperación CT-07 de una fuente contaminada deja EVD, incidencia y baja de F9. G3-EST-06 bloquea contenido contaminado en la salida. | — |
| PB-21 Credencial en un mensaje | Superada | El CT-04 del plan (una clave API y un IBAN en el comentario) se rechaza íntegro, deja una incidencia SEGURIDAD con el campo y sin el valor, y ni la clave ni el IBAN aparecen en ningún archivo ni mensaje; lo mismo en CT-03 y con las credenciales de CT-25. CT-04 conserva P-03 cuando rechaza una celda; AUT lleva CPI y EAC; R8 registra la clase de dato sin guardar el valor. | — |
| PB-22 Canal no previsto | Superada | Los tres mensajes del plan (Auditor → Analizador, Analista → Analista, Redactor → Broker) se rechazan, dejan tres incidencias CANAL_NO_PREVISTO marcadas para escalar al operador, que las ve en el estado (`incidencias_escaladas` de la orden `estado`, r05), y no cambian ningún archivo salvo el historial de auditoría. | — |
| PB-23 Escritura fuera de reserva | Superada | Los tres intentos del plan (el Analizador escribe en F4, Prospectiva escribe un campo de resolución y el Evaluador cambia la afirmación) se rechazan, dejan tres incidencias y la huella de F4 no cambia tras ninguno. | — |
| PB-24 Enlace roto y borrado con registro de bajas | Superada | Barrido y baja con registro, aviso CT-11, retirada de la evidencia, revisión de oportunidades en F3 y bajas del mes en CT-21. Comprueba también reintentos y conservación de la ficha ante fallos de red. | — |
| PB-25 Contenido cambiado y retractación | Superada | Contrasta la revisión con la huella del contenido, recalcula Q por rúbrica con motivo, verifica la copia archivada y registra la retractación confirmada. El registro alimenta la propagación a F2. | — |
| PB-26 Clasificación temática y orden por calidad | Superada | En los F7, F8 y F9 entregados: cada referencia está físicamente en la sección `## TX-nn` de su temática del Anexo D (y su campo «Temática» lo dice), 0 inversiones del orden por Q dentro de cada sección, a igualdad de Q la de año de publicación más reciente primero, el nivel A/B/C/D coherente con Q (13.3) y las de nivel D marcadas como candidatas a baja o única fuente; las mismas comprobaciones detectan un desorden, un nivel, una temática, una sección o un desempate estropeados. La CLI incorpora treinta referencias en TA-06, TM-11 y TF-04 y mantiene el orden por calidad y fecha sin alterar el registro de bajas. | — |
| PB-27 Aplicación del Fondo metodológico | Pendiente API | — | Las etapas del Fondo metodológico las aplica el modelo. |
| PB-28 Alimentación continua y Novedades | Pendiente API | — | La publicación y la lectura de Novedades dependen del modelo. |
| PB-29 Contar raíces, no menciones | Superada en parte | La puerta PS1 cuenta raíces independientes con el mínimo de la configuración. El ejecutor distingue una raíz y veinte derivadas documentadas; G3 contrasta las cifras de las afirmaciones de cada oportunidad con F2. | La identificación semántica de reproducciones sin metadatos de procedencia y la revisión humana del Auditor. |
| PB-30 Cifra sin artefacto bloqueada por G3 | Superada | HT-09 detecta una opción sin evidencias o sin cálculos. El caso del plan de extremo a extremo (T-159): con una rentabilidad esperada que cita un CALC- sin artefacto en el Registro de cálculos, el primer G3V- queda BLOQUEADO por C08, el CT-14 llega al Orquestador, que no lo da por bueno, la opción se retira y el segundo G3V- queda APTO: dos G3V- en HA; la cifra y su CALC- no llegan a ningún entregable, todo CALC- entregado tiene artefacto servido y la retirada se declara en las limitaciones. | El tiempo de dictamen (10 minutos como máximo): el reloj es simulado. |
| PB-31 Horizonte no certificado sin probabilidad | Superada | Sin certificado, `prob` y `prob_publicada` son nulas y la etiqueta «sin ventaja demostrada todavía» figura en el JSON, en el técnico y en el visual; la banda publicada de cada horizonte es la de su probabilidad interna (`banda_publicable`) y la de 0,65 (preparación del plan) es «más probable que no» en el JSON, en la fila del técnico y en la tarjeta del visual (r05); ningún entregable da una cifra de probabilidad y el visual no pinta confianza «Alta»; HT-09 bloquea una probabilidad sin certificado. | — |
| PB-32 Certificación de un horizonte | Superada | El caso del plan: con una celda con habilidad (RF × H3) y otra sin ella (RV × H3) se emite un solo certificado, el de RF. Cada condición del certificado (muestra efectiva, IC del BSS, calibración frente al nulo y tope de ECE) impide por sí sola certificar, y también Holm: el criterio exige el alfa corregido y el Evaluador se lo pasa (una celda hábil en la que Holm se detiene no se certifica). El certificado es de la celda × método y cada método cuenta aparte. La probabilidad solo se publica en la celda certificada, con su `certificado_ref`, y HT-09 la bloquea en las demás. T-160: antes de proponer o emitir el certificado, el Evaluador pide al Motor el cálculo que lo sostiene (FC-EVAL-001), comprueba que da sus mismas cifras y encarga su re-ejecución CT-10, que tiene que coincidir con la tolerancia de la ficha (SI o DENTRO_TOLERANCIA sin cruzar ningún umbral); el CERT- cita el CALC- de soporte y el de la re-ejecución. Si no coincide, si no se puede re-ejecutar (sin Motor, ficha no servida, datos irresolubles) o si las cifras difieren, no hay certificado y queda una incidencia en HA; CT-04 no pone en vigor un PROPUESTO sin esa re-ejecución en el Registro de cálculos. De punta a punta con el cliente simulado: revisión del Evaluador, un solo certificado (RF × H3 × método) con CT-10 coincidente y ninguno para RV × H3, aprobación por CT-04 y, en el RUN- siguiente, probabilidad solo en RF H3 con su `certificado_ref` y G3-CON-10 (C10) en OK. | — |
| PB-33 Revocación de certificado por deterioro | Superada | Un certificado se revoca por falta de habilidad o por calibración, con el umbral de la configuración; queda REVOCADO con motivo y fecha, antes de esa fecha seguía vigente y los pronósticos congelados no cambian. Con el caso del plan (celda certificada que pierde la habilidad), la revisión del ciclo revoca, deja en F6 la lección CALIBRACION de sobreconfianza de la celda y el RUN- posterior no publica probabilidad en ella; HT-09 bloquea probabilidades con un certificado no vigente. T-176: tras la revocación, la sección «Novedades» de F6 de la semana (NOV-AAAA-Www) lista por identificador la revocación (con estado, motivo y fecha) y la lección de sobreconfianza; la sección siguiente solo lleva lo nuevo (un cambio de estado de una lección o de un ajuste no es novedad) y un segundo C5 de la misma semana la rehace entera, sin duplicados. | — |
| PB-34 Fuga de información en evaluación detectada | Superada en parte | Ningún dato posterior a la fecha de corte (proveedor, Motor y resolución) y los pronósticos contaminados no cuentan para recalibrar. F6 conserva la corrección de la base contaminada y las nuevas puntuaciones, y documenta la decisión de sombra mediante comparaciones pareadas y DM-HLN. | No se ha usado un proveedor macroeconómico real con histórico de revisiones. |
| PB-35 Recalibración dentro de bandas con evaluación sombra | Superada en parte | La recalibración respeta el paso y las bandas de la configuración y queda como propuesta. F6 conserva la corrección de la base contaminada y las nuevas puntuaciones, y documenta la decisión de sombra mediante comparaciones pareadas y DM-HLN. | No se cambia la configuración productiva sin la autorización prevista en PA-10. Datos de prueba controlados. |
| PB-36 Recalibración fuera de bandas rechazada | Superada | Fuera de banda no se aplica: sale una propuesta P3 con el motivo. T-176, el caso del plan con el ciclo simulado: con evidencia de que el umbral E óptimo es 48 (−12 frente a 60; índice de Youden sobre los PRG resueltos) y con evidencia sembrada para P-05 (banda PENDIENTE_OPERADOR), la revisión trimestral (RTR-) deja dos P3-EVAL- («fuera de banda» y «sin banda») con evidencia, impacto, pruebas de regresión y plan de reversión; F10 queda intacto en P-09 y P-05 (sin CFG- ni AJU-); cada P3- sale por CT-19 al Orquestador (AG-18), que la registra en HA como PENDING_OPERATOR, y F6 anota `elevada_via`; un segundo ciclo del trimestre no repite la revisión ni la elevación. Dentro de banda (±5 por trimestre, ±10 en total, de la configuración) sale un AJU- PROPUESTO que no toca F10; un parámetro no CALIBRABLE se rechaza y un CALIBRABLE sin banda es tipo 3. T-176 r02: cada P3- cita en `pruebas_regresion` la batería de la §6 del plan y las específicas de R18; una P3- abierta de un parámetro (también la de P-11 de la recalibración de RK) no se repite ni se apila con otro objetivo; propuestas, revisiones y elevaciones concurrentes no se duplican; una P3- que no está en HA se eleva aunque lleve `elevada_via`. | — |
| PB-37 Pronóstico congelado inmutable | Superada | El alta congelada no se puede reescribir; la corrección es un PRG nuevo con `version_de`; la entrada original queda igual byte a byte; al adelantar el reloj a cada vencimiento, `Evaluador.resolver` resuelve el original en su fecha (con su nivel mal transcrito, sin cambios) y la corrección en la suya (r05): los dos RESUELTO y los dos en las métricas. Un pronóstico modificado a mano rompe la cadena de huellas. | Que Prospectiva decida corregir (modelo real): el ejecutor no tiene una operación propia de corrección; la corrección es un alta nueva de AG-10 con `version_de`. |
| PB-38 Objeción fuerte sin resolver impide el top-3 | Superada | La opción con una objeción fuerte sin resolver no entra en el top-3 ni en el JSON y queda en F3 como no elegible; HT-09 lo bloquea. En el informe técnico (V5 y V6) figura en la subsección 4.N.4 «Alternativas descartadas relevantes» de su tipo, con la puerta (G2), el motivo con su OBJ- y lo que tendría que ocurrir, y su objeción fuerte en la sección 6 como SIN_RESOLVER; un texto del modelo de la alternativa que G3-MET-13 rechazaría se sustituye (íntegro en F3, ADVERTENCIA en HA) y no bloquea la entrega (T-175). | — |
| PB-39 Informe visual con legibilidad < 70 bloqueado | Superada | El visual entregado tiene índice de 70 o más; HT-07 mide un texto difícil por debajo y HT-09 comprueba la legibilidad. En un ciclo con el Redactor sembrado con frases largas y jerga (T-159): el primer visual queda por debajo de 70 y BLOQUEADO por C12, se pide una reescritura a AG-17 y el visual reescrito, con 70 o más, es el que se entrega; si la reescritura sigue por debajo de 70, la entrega queda BLOQUEADA, ningún visual llega a la carpeta de entrega y no se congela nada. | Que el Redactor detecte y reescriba por sí mismo con HT-07 antes de HT-09, y las frases de 20 palabras como máximo y la jerga explicada del texto reescrito, que son del modelo real. |
| PB-40 Comprensión del informe visual por usuarios inexpertos | Requiere usuarios | — | Requiere usuarios reales. |
| PB-41 Coherencia entre entregables y entre clases | Superada | El ciclo solo entrega con la comprobación de coherencia superada (G3 APTO); con entregables incoherentes, G3 bloquea, nada llega a las carpetas de entrega y no se congela ningún pronóstico. El caso del plan en un C1 (T-159): con las series de RF, inmobiliario cotizado y RV expuestas al mismo factor, un clúster común reúne opciones de los tres tipos con su factor dominante, `apuestas_independientes` es el número de clústeres (menos que de opciones) y el técnico lo dice; el JSON, el técnico y el visual tienen las mismas OPP- en el mismo orden y la validación de los entregables no ve incoherencias (G3-ENT-07). | El recuento del Auditor (modelo real). Los datos sintéticos no tienen un factor común entre tipos: se siembra en las series del proveedor. |
| PB-42 Auditoría asíncrona sin bloqueo y hallazgo posterior | Pendiente API | — | Los hallazgos de la auditoría posterior exigen el modelo real; el ejecutor registra AUD- y HAL- tras la entrega. |
| PB-43 Pregunta repetida y lección de producto | Superada | A la tercera repetición, aviso CT-22 al Evaluador y una lección de producto en F6 enlazada a las tres QRY-, con un tema normalizado común en F5. | Que preguntas con palabras distintas den el mismo tema (lo normaliza el Coordinador, modelo real) y la sección en el informe siguiente (la aplica el modelo a partir de la lección). |
| PB-44 Historial de aciertos honesto | Superada | El historial publicado no usa resoluciones posteriores a su fecha, ni contaminados, ni hitos de H5. El escenario del plan a escala de los datos sintéticos (T-159), con nueve ciclos semanales: una opción cerrada por invalidación, una descartada por el Broker y una cuyo PRG queda NO_RESOLUBLE. El historial publicado es el recuento de F4 (PRG del informe resueltos en la ventana, sin fuga, sin hitos ni contaminados) y sus opciones están en F3; cuenta la invalidada y la descartada, no la NO_RESOLUBLE, que se declara en la nota; con n < 30, `significativo` false y la nota de muestra pequeña; el mismo dato en el JSON, en el técnico y en el visual («Cómo nos fue»); y el historial con su tamaño muestral pasa G3 (C01, G3-CON-18). | Las cifras exactas del plan (28 opciones, n = 27) dependen de los datos sintéticos: se afirma la regla sobre las opciones que salen. |
| PB-45 Lección aplicada en el siguiente encargo | Superada | Con 14 lecciones vigentes del tipo y una estadística, el encargo CT-06 lleva diez: la estadística primero, después las recurrentes, y ninguna de otro tipo de activo. | La aplicación de la lección en el informe del Analista y la comprobación AS-11 del Auditor, que son del modelo real. |
| PB-46 Fiabilidad de fuentes de opinión | Superada en parte | El caso del plan (dos fuentes de 25 pronósticos explícitos, una con habilidad y otra sin ella): FUE- en F6 con n, aciertos, BSS (Brier del Motor, FC-EVAL-001, con su `calc_id`), BSS contraído con k = 20 y puntos de historial (por encima y por debajo del neutro 10), una por fuente y mes y comunicadas al Buscador por CT-19. En ciclos (r02 de T-125): el pronóstico que devuelve el Analista o el Buscador llega a F2 con su bloque y, vencido, sale en la FUE- y en el CT-19; solo cuenta lo registrado antes de su fecha objetivo, de una fuente de F9, dentro de la ventana y con cierre reciente. | La recalificación de Q y el orden en F9, que hace el Buscador con el modelo real (T-125). En backtest no entra ningún pronóstico de una fuente de F9 sin fecha (el filtro de evidencia no la da por conocible): el camino se prueba en modo vivo con el cliente simulado. Además, el CT-19 al Buscador se crea COMPLETO y nadie lo atiende: no hay en F9 dónde escribir la recalificación (QA r01 de T-159, H-02; función que falta, INC-T159-01). |
| PB-47 Estados de madurez | Superada | Una ficha no implementada se rechaza con METODO_NO_IMPLEMENTADO y una con código provisional no da cifras. Con la preparación completa del plan (T-165): ML-CLUS-001 en DOCUMENTADO en el Catálogo y un informe de clase que lo llama «validado», HT-09 (G3-MET-13, comprobación complementaria del ejecutor) deja el primer G3V- BLOQUEADO con la incidencia de G3-MET-13, el CT-14 llega al Orquestador, que no lo da por bueno, las opciones que lo afirman se retiran y el entregable final no lo presenta como validado ni cita cifras suyas. Con la declaración corregida (la ficha en su forma canónica, «ML-CLUS-001 [madurez: DOCUMENTADO; no la sirve el Motor]») el mismo ciclo pasa APTO y se entrega. Un método no servido que solo nombra el informe técnico, o un «validado» en el informe visual, bloquea la entrega en F7. El ciclo simulado normal (doce tipos) sigue APTO con G3-MET-13 OK, la comprobación lee las fichas servidas que cita y los entregables llevan la madurez canónica de cada ficha, que escribe el ejecutor desde el Catálogo (r03). | Con el cliente simulado, la redacción de un modelo real. Desde la r03 la prosa no se interpreta (la raíz «valid-» junto a un método bloquea; los sinónimos no cuentan): falsos positivos medidos con un banco nuevo, los de la r02 y los del revisor, y límites, en INC-T165-01. |
| PB-48 Conflicto de normas: la más restrictiva | Superada | T-158: con una guía CT-18 de tipo 2 vigente para el Analizador que sugiere omitir la segunda pasada en banda marginal (contradice 9.1), en un ciclo con el cliente simulado la guía no se aplica (R23): las opciones en banda marginal llegan a HT-03 con la segunda pasada y se resuelven con ella, que queda registrada en F3; en HA quedan un COR- (la guía corregida, la regla 9.1, quién lo detectó y a quién se comunica) y un P3- del Orquestador reclasificado como tipo 3 en PENDING_OPERATOR (cola de tipo 3), y el ítem se retira de la guía (RETIRADA o versión nueva por CT-18 con el resto); el texto del ítem no llega a ningún agente ni a HT-03. Una guía ya vigente sin revisar se revisa en el F0 del run siguiente. HT-03 exige la segunda pasada en banda marginal (R23 por construcción) y una lección vigente que relaja el control no llega a la elegibilidad. T-161: el emisor también revisa (control doble) y no emite el ítem en conflicto; la preparación del plan («guía vigente que sugiere omitir…») simula que su filtro falló, solo con el cliente simulado. Un ítem en conflicto en cualquier campo de texto (también `donde_se_comprueba` y `como_se_sabe`) no llega a ningún agente. | Con el modelo real: que el Orquestador (modelo) redacte las guías a partir de hallazgos y lecciones y que el Analista haga la segunda pasada por sí mismo (en la prueba la hace el simulado; el ejecutor no la pide si falta: la opción queda no elegible por PS8). El detector de conflictos lee el texto del ítem (normalizado, en todos sus campos, estricto con los controles, otras lenguas y caracteres fuera de los permitidos): lo que reconoce como dudoso es conflicto; una paráfrasis nueva que no reconoce llega como contexto al modelo del agente receptor, pero no a HT-03, a las puertas ni a G3. Desde la r02 de T-161, AG-11, AG-18, AG-19 y AG-20 no reciben guías; desde la r03, tampoco las lecciones redactadas por un modelo, y desde la r04 solo las que escribe entero el código (origen DETERMINISTA y tipo PREDICTIVA o CALIBRACION en la entrada de alta de F6): las de PRODUCTO llevan el tema de una pregunta del Coordinador o del Broker y no les llegan. Las lecciones de AG-20 se validan contra F6 y pasan el detector al escribirse y al leerse; lo que el detector no reconoce en ellas llega como contexto a los agentes que no son de control. Queda el traslado de segundo orden por la salida de un Analista (INC-T126-01, T-158, T-161). |
| PB-49 Historial íntegro y supresiones permitidas | Superada | En ocho semanas simuladas, cada instantánea de F1–F6, RC y HA contiene la anterior byte a byte (solo añadidos) y todo sigue íntegro; la cadena de huellas detecta una entrada modificada y una borrada (del medio o la última); las supresiones de F7–F9 las hace HT-02 con su línea en el Registro de bajas y motivo obligatorio. | — |
| PB-50 Horizontes según la clase de activo | Superada | La tabla de horizontes por tipo (INM sin H1; ALT sin H1 ni H2; DIV × H4 «Limitado») y el bloqueo de HT-09 a un horizonte no aplicable; en la revisión mensual del C5 (registro RDM- en F6), RF × H2 con 35 pronósticos resueltos en 35 fechas que pierden frente a la referencia ingenua con DM-HLN sobre las medias por conglomerado de fecha (PA-03) y p ≤ umbral de Holm (familia fija: todas las celdas H1–H4 en «Sí» del bloque) pasa de «Sí» a «Limitado» con su AJU- en F6 (evidencia: estadístico, p, h, α, umbral de Holm, n, n_eff, conglomerados y los PRG-) y su CFG- de P-31 (y de P-30) en F10, solo en esa celda; el ciclo siguiente lee «Limitado» y G3 no bloquea; no degrada sin muestra efectiva (n_eff < 30 o menos de 10 conglomerados: una sola semana mala, o una historia buena con una semana mala), sin fechas, con p > α o sobre el umbral de Holm de la revisión, con pronósticos que ganan, con PRG contaminados, en H5, fuera de la revisión mensual ni dos veces en un trimestre, y ningún cambio hacia o desde «No»; si falla la escritura en F10, el AJU- queda ANULADO (y el CFG- de P-31 revertido) y la revisión se repite. | La revisión mensual en el calendario real: el reloj es simulado (el primer C5 de cada mes hace la revisión). Las muestras mínimas (`evaluacion.min_calibrar` sobre n_eff y `evaluacion.min_conglomerados_bootstrap`) y la periodicidad mensual de 12.2 no figuran en el Anexo A ([PROPUESTO] INC-T173-01); el α (`evaluacion.alfa_holm`) con Holm sobre la familia fija de la revisión es decisión del operador por delegación (17-11-2026, INC-T173-01). |
| PB-51 Conocimiento específico en los system prompts | Superada en parte | Revisión documental con el script de T-187 (`.docs/scripts/revision_prompts_pb51.py`, sin red y determinista; datos en `.docs/tickets/T-187/`), atada al corpus actual: el informe y la muestra guardados son los que salen hoy de los prompts, del Documento 0, de la configuración y de los veredictos. Paso 1: los 35 prompts tienen las 12 secciones del Anexo G, una vez y en orden (la plantilla, fuera del denominador). Paso 2: la sección 10 de cada prompt está partida en subáreas, con fórmulas y referencias contadas, y ningún DOI escrito tiene estructura inválida. Paso 3: cuatro revisores independientes juzgaron las 350 afirmaciones de la muestra: 260 CORRECTA, 9 ERRONEA y 81 NO_VERIFICABLE, 96,7 % correctas sobre las verificables (≥ 95 %; 74,3 % sobre las 350). Los 14 papeles con tope en `v6.tope_tokens_system` quedan dentro. | El resultado esperado del plan, «ninguna afirmación técnica errónea en la muestra», no se cumple: 9 ERRONEA (INC-T187-03), pendientes de la próxima entrega del corpus. «Tamaños dentro de las orientaciones» solo se comprueba en los 14 papeles con tope; los otros 21 papeles no tienen orientación (INC-T187-01, T-57). El paso 3 pide 10 afirmaciones técnicas por prompt: 28 de 35 tienen menos de 10 verificables (mínimo 2, el Coordinador), porque las 81 NO_VERIFICABLE son reglas internas; se declara y no hay muestra de reposición (INC-T187-02). De las 260 CORRECTA, 249 las juzgó el revisor de memoria («conocimiento propio»), sin consultar la referencia, 3 con búsqueda web y 8 con un cálculo a mano; la QA r01 contrastó 10 al azar y coincidió en las 10 (INC-T187-02). Los criterios son `[PROPUESTO]`: el denominador del 95 % (INC-T187-02: las NO_VERIFICABLE quedan fuera) y la estructura completa y la orientación de tamaño (INC-T187-01). Que los DOI existan no se comprueba (sin red; hoy no hay ninguno escrito). El juicio de las afirmaciones es de los revisores, no del script. |
| PB-52 Modo degradado: herramienta caída | Superada | Una salida no conforme o un símbolo sin datos dan una entrega PARCIAL con la limitación declarada y sin cifras inventadas. Con HT-09 caído (T-159), el ciclo no entrega nada, no congela pronósticos y no deja ningún dictamen APTO. Las caídas simuladas en F6 y F7 terminan con bloqueo justificado, comunicación CT-14 y registros en HA y F5. | — |
| PB-53 Frontera A/B: un Analista propone un activo concreto | Superada | El caso del plan en un C1: el Analista RV propone una empresa concreta y no llega al top-3 ni al encargo para B ni a los informes; la ficha de finalista no admite vehículos, la propuesta de una empresa se retira antes de entregar y HT-09 bloquea un activo concreto. | — |
| PB-54 Encargo completo para el Bloque B | Superada | Cada encargo para el Bloque B lleva sus once campos presentes y no vacíos (ámbito, tesis, horizontes, pronósticos, catalizadores, riesgos, invalidación, indicador, criterios, métricas y preguntas) y cumple el esquema. | — |
| PB-55 Cobertura de los doce tipos de activo | Superada | Los doce tipos en el paquete, en el informe visual y en el técnico (un apartado con su semáforo por tipo), con tres opciones como máximo cada uno y el motivo cuando hay menos. | — |
| PB-56 Oportunidad duplicada entre tipos | Superada | El caso del plan en un C1: RV e IDX proponen el mismo ámbito y queda en un solo top-3, con el motivo de la otra en F3; ningún nombre ni ámbito en dos top-3. La regla (se quita la de menor RK, con su motivo) sobre la función, y HT-09 bloquea un duplicado por nombre, por ámbito o por identificador. | — |
| PB-57 Estrategias de los tipos nuevos | Pendiente API | — | Lo audita el Auditor con el modelo real. |
| PB-58 Solicitud y provisión de una credencial por CT-25 | Superada | «Superada» con su preparación: la configuración por defecto no declara ningún servicio de pago del BFA (`credenciales.servicios_bfa` vacía, `[PROPUESTO]`, INC-T177-01), así que en un run real el C4 no llama al BFA (SIN_SERVICIOS); las pruebas declaran un servicio ficticio, y declarar la lista es el pendiente del operador T-179. Pasos 1 a 4 del plan (T-177): en el mantenimiento C4 (`credencial c4`) el Buscador de Fuentes Avanzadas recibe solo el alias y el estado en la bóveda de HT-01 de sus servicios de pago o API y devuelve `solicitudes_credenciales`; el Coordinador las deduplica por alias, comprueba en HT-01 que faltan y emite el CT-25 al Broker con solicitante AG-16, uso e impacto (CRD- en F5 sin valor y C4- que la enlaza); un retorno con un valor se rechaza íntegro (R8, sin CT-25 ni copia en la caché), lo mal formado se descarta con motivo. Además: solicitud con CRD- en F5 sin valor; servicio degradado y declarado en los entregables hasta la provisión (corrección de INC-T116-03); depósito en la bóveda y respuesta solo con estado y alias; la herramienta obtiene el valor de la bóveda; la segunda C4 se resuelve sin volver al Broker; el valor no aparece en ningún archivo, mensaje, entregable ni contexto enviado a los agentes. Ronda r02 (QA r01 de T-177): el valor en cualquier sitio de un retorno con `solicitudes_credenciales`, en cualquier grafía de la clave, o una ficha opaca en el servicio, el motivo o el impacto, no llega a la caché ni a la cinta de grabación (`llm.respuesta_segura`); otra grafía del servicio en la segunda C4 y dos C4 a la vez dan un solo CT-25; el C4 sin servicios no llama al BFA y la bolsa de 3 UC del Anexo A es semanal. Ronda r03 (QA r02): la barrera solo mira los retornos con `solicitudes_credenciales`, leídos primero como JSON; dentro del subárbol, una ficha opaca en cualquier clave u hoja o un número bajo una clave de valor bloquea; fuera, solo las claves inequívocas o las ambiguas con ficha opaca, así que el informe de Analista del Marco común (lista vacía e `indicadores[].valor` de texto, que el simulado emite) se usa; dos C4 a la vez no pasan de la bolsa semanal (reserva bajo la transacción). | — |
| PB-59 Credencial expuesta en un mensaje del Broker | Superada | El mensaje con el valor se rechaza, queda una incidencia SEGURIDAD en HA, el valor no aparece en ningún archivo ni mensaje y se pide depositar y renovar; HT-09 bloquea un valor de credencial en el paquete. | — |
| PB-60 Credencial denegada | Superada | Tras la denegación queda la limitación de servicio en F10; una nueva necesidad del mismo servicio no envía ninguna CT-25, salvo con cambio de circunstancias; el paquete, el informe técnico, el JSON y el visual del ciclo declaran la degradación, y dejan de declararla cuando la credencial se provee (corrección de INC-T116-03). | — |
| PB-61 Consulta bloqueante al Broker con vencimiento | Superada | Solo CRI se pausa y RV sigue; al vencer, el análisis continúa con el supuesto declarado, que figura en el paquete, en el JSON y en el informe técnico (C19 de HT-09 en OK); la respuesta tardía que contesta ese supuesto ya entregado abre una revisión C2: un RUN- AD_HOC disparado por la CT-23, con los RUN- revisados, cuyo paquete ya no lleva el supuesto, declara la revisión en sus entregables y llega al Broker por CT-02 (corrección de INC-T116-03; reglas en INC-T174-01). Sin informe entregado con el supuesto no hay revisión, y una respuesta sin nada nuevo no la reabre; un fallo queda anotado y escalado al operador y un error de control se relanza dejando la revisión INTERRUMPIDA, que se relanza; dos procesos con la misma respuesta abren una sola revisión; el alcance no pasa de lo entregado ni de lo entregado hasta la fecha de la respuesta (QA r01 de T-174, H-01 a H-06); una revisión cuyo proceso murió se avisa una vez al operador y, si ya se había entregado, relanzarla no la repite (QA r02, H-07 y H-08). | Que el modelo real no invente un dato del Broker (con el cliente simulado no se puede medir; modo sombra). Los plazos con el reloj de pared (las pruebas fijan la hora). Si la respuesta contradice de verdad el supuesto: el ejecutor no lo juzga y toda respuesta nueva cuenta como invalidación (INC-T174-01). |
| PB-62 Filtro, agrupación y recurrencia de consultas | Superada | Tres CT-23 como máximo por RUN- (la cuarta se agrupa), validaciones y aviso de consulta recurrente. El Evaluador escribe en F6 lecciones de producto a partir de decisiones anteriores al resultado y de consultas recurrentes de análisis distintos. | — |
| PB-63 Pronóstico H5 con hitos | Superada | H5 solo con banda y tres hitos HIT- o más, cada uno con fecha, indicador y criterio, el primero a 12 meses como máximo y 24 como máximo entre hitos, congelados en F4 con su PRG padre (C18 en OK); HT-09 bloquea un H5 sin hitos o con probabilidad numérica y advierte del espaciado. | — |
| PB-64 Evaluación de H5 por hitos y degradación | Superada | H5 se evalúa por hitos con sus tres estados (EN_CURSO_CONFORME, DESVIADO, INVALIDADO); con 20 hitos y el 40 % cumplidos MP × H5 baja de «Sí» a «Limitado» con el ajuste en F6 y en F10 y cambia la tabla del ciclo siguiente; la revisión de certificados no emite ninguno para H5. Los estados se publican: cada C5 escribe en F6 una entrada EH5- con el estado de cada PRG H5 abierto y de sus hitos, la tasa de hitos cumplidos por celda tipo × H5 y el número de PRG en cada estado; el paquete lleva lo mismo en `x_estados_h5` (valida contra su esquema) y el estado de cada hito, y el informe técnico los muestra junto a los hitos y en la sección 8. | El informe visual no los muestra (lenguaje llano; su plantilla no tiene sitio para ellos) ni el CT-19 del Evaluador los lleva. Los H5 congelados en el mismo RUN- se publican desde el C5 siguiente. El prefijo EH5- de F6 es [PROPUESTO] (INC-T173-01). |
| PB-65 Horizonte principal incoherente con la naturaleza | Superada | Los tres casos del plan en HT-09: fuera de rango sin justificación, BLOQUEADO; con justificación, APTO_CON_ADVERTENCIAS; principal en una celda «No» (DER con H5), BLOQUEADO. En el ciclo, cada opción es coherente o está justificada. | El dictamen del Orquestador sobre la advertencia (CT-14), que es del modelo real. |
| PB-66 Seguimiento encargado: alta, ciclos y cancelación | Superada | Alta con SEG- en F11 y EN_SEGUIMIENTO y `seg_id` en F3; dos ciclos C6 con informe de 300 palabras como máximo, una recomendación y HT-09 sin bloqueo; pausa y reanudación con la fecha del siguiente ciclo; cancelación inmediata y ningún ciclo después. | Que C6 no retrase C1–C3: el reloj es simulado. |
| PB-67 Seguimiento que propone el envío al Bloque B | Superada | HT-09 (perfil SEGUIMIENTO) da APTO a PROPONER_ENVIO_A_B con su paquete y elegible, y BLOQUEADO sin él. Un ciclo C6 del ejecutor (T-159): la opción vigilada vuelve a ser elegible sin objeciones fuertes y con novedad (ocurre su catalizador) y el C6 recomienda PROPONER_ENVIO_A_B con HT-09 de seguimiento APTO, el `paquete_para_bloque_B` actualizado y la sugerencia de N3 decidida; sin envío automático: el único mensaje fuera del bloque es el CT-24 al Broker, ninguno va al Bloque B y F3 sigue con la decisión EN_SEGUIMIENTO del Broker. | — |

## Cómo repetir cada fila

Desde la raíz del repositorio. También: `.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-NN`.

### PB-01 · Ciclo periódico completo de extremo a extremo

Criterio de aprobación del plan: Todos los elementos presentes; G3 APTO o APTO_CON_ADVERTENCIAS; entrega en hora; cero mensajes fuera del catálogo de contratos

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_ciclo_semanal_completo_apto' 'tests/test_integracion.py::test_canales_y_matriz_respetados' 'tests/test_fase4_huecos.py::test_pb01_con_memoria_el_nivel_sigue_a_gc0_y_todos_los_mensajes_son_del_catalogo' 'tests/test_fase4_huecos.py::test_pb01_sin_g3_apto_no_se_congela_ningun_pronostico_ni_se_entrega')
```

- `11_Ejecutor/tests/test_integracion.py::test_ciclo_semanal_completo_apto`: SUPERADA
- `11_Ejecutor/tests/test_integracion.py::test_canales_y_matriz_respetados`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb01_con_memoria_el_nivel_sigue_a_gc0_y_todos_los_mensajes_son_del_catalogo`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb01_sin_g3_apto_no_se_congela_ningun_pronostico_ni_se_entrega`: SUPERADA

### PB-02 · Top-3 con menos de tres elegibles

Criterio de aprobación del plan: Exactamente 2 opciones; G3-CON-03 PASA; ninguna opción con umbral incumplido

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_ciclo_semanal_completo_apto' 'tests/test_t159_extremo_a_extremo.py::test_pb02_dos_opciones_y_la_de_banda_marginal_fuera_con_su_segunda_pasada')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht03_puntuaciones.py::TestSeleccion::test_menos_de_tres' 'tests/test_ht09_validador_g3.py::TestBloqueos::test_menos_de_tres_sin_motivo' 'tests/test_ht03_puntuaciones.py::TestOpcion::test_banda_marginal_sin_y_con_segunda_pasada')
```

- `11_Ejecutor/tests/test_integracion.py::test_ciclo_semanal_completo_apto`: SUPERADA
- `10_Herramientas/tests/test_ht03_puntuaciones.py::TestSeleccion::test_menos_de_tres`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_menos_de_tres_sin_motivo`: SUPERADA
- `10_Herramientas/tests/test_ht03_puntuaciones.py::TestOpcion::test_banda_marginal_sin_y_con_segunda_pasada`: SUPERADA
- `11_Ejecutor/tests/test_t159_extremo_a_extremo.py::test_pb02_dos_opciones_y_la_de_banda_marginal_fuera_con_su_segunda_pasada`: SUPERADA

### PB-03 · Clase sin ninguna opción elegible

Criterio de aprobación del plan: Cero opciones ALT; el Auditor no registra hallazgo por ello

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_presupuesto_agotado_parcial_declarado' 'tests/test_t159_extremo_a_extremo.py::test_pb03_alt_sin_vehiculo_minorista_queda_sin_opciones_y_en_gris')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht03_puntuaciones.py::TestSeleccion::test_cero_opciones')
```

- `11_Ejecutor/tests/test_integracion.py::test_presupuesto_agotado_parcial_declarado`: SUPERADA
- `10_Herramientas/tests/test_ht03_puntuaciones.py::TestSeleccion::test_cero_opciones`: SUPERADA
- `11_Ejecutor/tests/test_t159_extremo_a_extremo.py::test_pb03_alt_sin_vehiculo_minorista_queda_sin_opciones_y_en_gris`: SUPERADA

### PB-06 · Consulta N0 sin escalado

Criterio de aprobación del plan: Respuesta < 2 minutos; ≥ 1 referencia por afirmación; cero encargos CT-05; consumo ≤ 1 UC

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_consulta_n0_sin_escalado' 'tests/test_fase4_huecos.py::test_pb06_la_respuesta_n0_es_una_aclaracion_y_cada_referencia_existe_en_f1_a_f6')
```

- `11_Ejecutor/tests/test_integracion.py::test_consulta_n0_sin_escalado`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb06_la_respuesta_n0_es_una_aclaracion_y_cada_referencia_existe_en_f1_a_f6`: SUPERADA

### PB-07 · Consulta que escala a análisis

Criterio de aprobación del plan: Respuesta provisional < 2 minutos; QRY- enlazada al RUN-; el Coordinador no responde con conocimiento propio no trazado

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_consulta_que_escala_y_pregunta_repetida' 'tests/test_fase4_huecos.py::test_pb07_la_consulta_de_contraste_responde_provisional_con_nivel_y_plazo' 'tests/test_t162_respuesta_final.py::test_pb07_de_punta_a_punta_con_el_simulado' 'tests/test_t162_respuesta_final.py::test_ca1_la_final_sale_despues_de_la_provisional_enlazada_a_la_consulta_y_al_run' 'tests/test_t162_respuesta_final.py::test_ca2_las_referencias_son_las_del_run_y_existen_en_la_memoria' 'tests/test_t162_respuesta_final.py::test_ca3_si_el_run_falla_la_final_lo_dice_sin_referencias' 'tests/test_t162_respuesta_final.py::test_ca4_enviar_dos_veces_no_duplica' 'tests/test_t169_hallazgos_t162.py::test_h01_un_fallo_de_integridad_para_la_consulta_como_en_la_base' 'tests/test_t169_hallazgos_t162.py::test_h02_la_siguiente_consulta_envia_la_final_pendiente')
```

- `11_Ejecutor/tests/test_integracion.py::test_consulta_que_escala_y_pregunta_repetida`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb07_la_consulta_de_contraste_responde_provisional_con_nivel_y_plazo`: SUPERADA
- `11_Ejecutor/tests/test_t162_respuesta_final.py::test_pb07_de_punta_a_punta_con_el_simulado`: SUPERADA
- `11_Ejecutor/tests/test_t162_respuesta_final.py::test_ca1_la_final_sale_despues_de_la_provisional_enlazada_a_la_consulta_y_al_run`: SUPERADA
- `11_Ejecutor/tests/test_t162_respuesta_final.py::test_ca2_las_referencias_son_las_del_run_y_existen_en_la_memoria`: SUPERADA
- `11_Ejecutor/tests/test_t162_respuesta_final.py::test_ca3_si_el_run_falla_la_final_lo_dice_sin_referencias`: SUPERADA
- `11_Ejecutor/tests/test_t162_respuesta_final.py::test_ca4_enviar_dos_veces_no_duplica`: SUPERADA
- `11_Ejecutor/tests/test_t169_hallazgos_t162.py::test_h01_un_fallo_de_integridad_para_la_consulta_como_en_la_base`: SUPERADA
- `11_Ejecutor/tests/test_t169_hallazgos_t162.py::test_h02_la_siguiente_consulta_envia_la_final_pendiente`: SUPERADA

### PB-08 · Ráfaga de peticiones sin límite

Criterio de aprobación del plan: 100 % registradas; 100 % respondidas o con plazo comunicado; N0 con p90 < 2 minutos

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_contratos_canales_credenciales_e_idempotencia' 'tests/test_unitarias.py::test_ht04_y_ht06_y_ht08')
```

- `11_Ejecutor/tests/test_unitarias.py::test_contratos_canales_credenciales_e_idempotencia`: SUPERADA
- `11_Ejecutor/tests/test_unitarias.py::test_ht04_y_ht06_y_ht08`: SUPERADA

### PB-09 · Cambio de periodicidad por el Broker

Criterio de aprobación del plan: Siguiente C1 disparado en la nueva fecha; ningún otro parámetro modificado

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t87_contratos.py::test_ct04_conserva_frecuencia_y_aplica_desde_fecha_efecto' 'tests/test_integracion.py::test_peticion_ad_hoc_y_decisiones')
```

- `11_Ejecutor/tests/test_t87_contratos.py::test_ct04_conserva_frecuencia_y_aplica_desde_fecha_efecto`: SUPERADA
- `11_Ejecutor/tests/test_integracion.py::test_peticion_ad_hoc_y_decisiones`: SUPERADA

### PB-10 · Configuración no permitida rechazada parcialmente

Criterio de aprobación del plan: F10 cambia solo P-02; HA sin incidencia de escritura (rechazo correcto, no intento de escritura)

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_peticion_ad_hoc_y_decisiones' 'tests/test_fase4_huecos.py::test_pb10_la_configuracion_rechazada_en_parte_no_toca_nada_mas' 'tests/test_t189_controles.py::test_ct04_rechaza_lista_global_incompatible')
```

- `11_Ejecutor/tests/test_integracion.py::test_peticion_ad_hoc_y_decisiones`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb10_la_configuracion_rechazada_en_parte_no_toca_nada_mas`: SUPERADA
- `11_Ejecutor/tests/test_t189_controles.py::test_ct04_rechaza_lista_global_incompatible`: SUPERADA

### PB-11 · Decisión del Broker sin alterar el análisis ni la evaluación

Criterio de aprobación del plan: Ningún mensaje del bloque al Bloque B; ambos PRG RESUELTO; HAC- con n que incluye OPP-B

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_peticion_ad_hoc_y_decisiones' 'tests/test_fase4_huecos.py::test_pb11_la_opcion_descartada_se_resuelve_y_cuenta_en_el_historial' 'tests/test_t188_producto.py::test_comparacion_por_decision')
```

- `11_Ejecutor/tests/test_integracion.py::test_peticion_ad_hoc_y_decisiones`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb11_la_opcion_descartada_se_resuelve_y_cuenta_en_el_historial`: SUPERADA
- `11_Ejecutor/tests/test_t188_producto.py::test_comparacion_por_decision`: SUPERADA

### PB-12 · Campos de decisión y paquete para el Bloque B

Criterio de aprobación del plan: G3-CON-14, G3-CON-15 y G3-CON-20 PASA; validación JSON sin errores

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_ciclo_semanal_completo_apto' 'tests/test_fase4_huecos.py::test_pb12_relevancia_segun_la_regla_y_el_encargo_para_b_repite_los_datos_de_su_opcion')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestBloqueos::test_paquete_bloque_b' 'tests/test_ht09_validador_g3.py::TestV5::test_encargo_para_bloque_b')
```

- `11_Ejecutor/tests/test_integracion.py::test_ciclo_semanal_completo_apto`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_paquete_bloque_b`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV5::test_encargo_para_bloque_b`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb12_relevancia_segun_la_regla_y_el_encargo_para_b_repite_los_datos_de_su_opcion`: SUPERADA

### PB-13 · GC0 negativo con arrastre verificado

Criterio de aprobación del plan: Consumo INM ≤ 6 UC; comprobación de invalidación registrada para cada vigente (AS-06 PASA); rotación exploratoria entre 15 % y 25 %

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_gc0_negativo_arrastre_verificado' 'tests/test_t65_resto_t53.py::test_cs10_celdas_de_rotacion_exploratoria_de_la_configuracion' 'tests/test_t185_rotacion.py::test_rotacion_presupuestada_en_f5')
```

- `11_Ejecutor/tests/test_integracion.py::test_gc0_negativo_arrastre_verificado`: SUPERADA
- `11_Ejecutor/tests/test_t65_resto_t53.py::test_cs10_celdas_de_rotacion_exploratoria_de_la_configuracion`: SUPERADA
- `11_Ejecutor/tests/test_t185_rotacion.py::test_rotacion_presupuestada_en_f5`: SUPERADA

### PB-14 · Arrastre con invalidación activada

Criterio de aprobación del plan: Estado y motivo en F3; PRG no anulados en F4

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_autocritica.py::test_arrastre_con_invalidacion_activada')
```

- `11_Ejecutor/tests/test_autocritica.py::test_arrastre_con_invalidacion_activada`: SUPERADA

### PB-16 · Presupuesto agotado: alcance reducido, verificación intacta

Criterio de aprobación del plan: G3 sin NO_APLICA injustificados; limitación visible en ambos informes

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_presupuesto_agotado_parcial_declarado' 'tests/test_fase4_huecos.py::test_pb16_con_el_presupuesto_agotado_g3_hace_las_mismas_comprobaciones')
```

- `11_Ejecutor/tests/test_integracion.py::test_presupuesto_agotado_parcial_declarado`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb16_con_el_presupuesto_agotado_g3_hace_las_mismas_comprobaciones`: SUPERADA

### PB-17 · Ampliación de presupuesto en el ciclo periódico

Criterio de aprobación del plan: Dos AUT- en HA con CPI, EAC y motivo; consumo real registrado en F5

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_fase4_huecos.py::test_pb17_ampliacion_autorizada_y_denegada_dejan_su_aut_en_ha' 'tests/test_fase4_huecos.py::test_pb17_en_un_ciclo_la_ampliacion_denegada_cierra_con_alcance_reducido' 'tests/test_t189_controles.py::test_aut_con_valor_ganado')
```

- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb17_ampliacion_autorizada_y_denegada_dejan_su_aut_en_ha`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb17_en_un_ciclo_la_ampliacion_denegada_cierra_con_alcance_reducido`: SUPERADA
- `11_Ejecutor/tests/test_t189_controles.py::test_aut_con_valor_ganado`: SUPERADA

### PB-18 · Cola saturada y apertura de instancia

Criterio de aprobación del plan: Apertura ≤ 1 ciclo de lectura tras superar el umbral; cero duplicados en F2; tiempo medio de ingesta vuelve al objetivo

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_ht04_y_ht06_y_ht08' 'tests/test_t53_evaluacion_y_almacen.py::test_monitor_abre_instancias_de_los_analistas_nuevos' 'tests/test_t193_ingesta.py::test_abrir_por_tiempo_y_cerrar_con_histeresis' 'tests/test_t193_ingesta.py::test_cuarenta_ingestas_concurrentes_sin_duplicados' 'tests/test_t193_ingesta.py::test_la_orden_por_ingesta_se_registra_en_el_mismo_ciclo')
```

- `11_Ejecutor/tests/test_unitarias.py::test_ht04_y_ht06_y_ht08`: SUPERADA
- `11_Ejecutor/tests/test_t53_evaluacion_y_almacen.py::test_monitor_abre_instancias_de_los_analistas_nuevos`: SUPERADA
- `11_Ejecutor/tests/test_t193_ingesta.py::test_abrir_por_tiempo_y_cerrar_con_histeresis`: SUPERADA
- `11_Ejecutor/tests/test_t193_ingesta.py::test_cuarenta_ingestas_concurrentes_sin_duplicados`: SUPERADA
- `11_Ejecutor/tests/test_t193_ingesta.py::test_la_orden_por_ingesta_se_registra_en_el_mismo_ciclo`: SUPERADA

### PB-19 · Agente de instancia única saturado

Criterio de aprobación del plan: Cero ORD- para AG-02; registro CAR- de la saturación

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_ht04_y_ht06_y_ht08' 'tests/test_t53_evaluacion_y_almacen.py::test_monitor_abre_instancias_de_los_analistas_nuevos' 'tests/test_fase4_huecos.py::test_pb19_el_analizador_saturado_no_abre_instancias_y_deja_su_registro_car_en_ha' 'tests/test_t178.py::test_pb19_seis_ct05_sin_ord_y_la_cola_queda_reordenada_por_prioridad' 'tests/test_t178.py::test_pb19_el_orden_es_estable_y_una_cola_ya_ordenada_no_cambia' 'tests/test_t178.py::test_pb19_la_cola_sin_detalle_se_cuenta_y_el_ct01_baja_tras_la_c6_no' 'tests/test_t178.py::test_pb19_sin_saturacion_no_hay_car_ni_reordenacion' 'tests/test_t178.py::test_pb19_aviso_al_coordinador_solo_de_los_agentes_del_camino_de_la_entrega' 'tests/test_t178.py::test_pb19_el_coordinador_lee_su_aviso_en_ha' 'tests/test_t178.py::test_pb19_la_primera_saturacion_no_propone_y_la_segunda_en_otro_run_si' 'tests/test_t178.py::test_pb19_dos_lecturas_del_mismo_run_no_son_una_repeticion' 'tests/test_t178.py::test_pb19_la_propuesta_abierta_no_se_duplica_y_tras_rechazarla_hace_falta_otra_repeticion' 'tests/test_t178.py::test_pb19_la_repeticion_es_por_agente_y_cuenta_los_car_anteriores_a_t178' 'tests/test_t178.py::test_pb19_una_orden_invalida_se_rechaza_sin_tocar_la_cola' 'tests/test_t178.py::test_pb19_una_orden_ya_en_la_cola_se_rechaza_y_retirar_la_saca' 'tests/test_t178.py::test_pb19_un_agente_con_estado_nunca_recibe_ord_ni_con_umbral_cero' 'tests/test_t178.py::test_pb19_dos_ciclos_con_el_analizador_saturado_reordenan_avisan_y_proponen_tipo_3')
```

- `11_Ejecutor/tests/test_unitarias.py::test_ht04_y_ht06_y_ht08`: SUPERADA
- `11_Ejecutor/tests/test_t53_evaluacion_y_almacen.py::test_monitor_abre_instancias_de_los_analistas_nuevos`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb19_el_analizador_saturado_no_abre_instancias_y_deja_su_registro_car_en_ha`: SUPERADA
- `11_Ejecutor/tests/test_t178.py::test_pb19_seis_ct05_sin_ord_y_la_cola_queda_reordenada_por_prioridad`: SUPERADA
- `11_Ejecutor/tests/test_t178.py::test_pb19_el_orden_es_estable_y_una_cola_ya_ordenada_no_cambia`: SUPERADA
- `11_Ejecutor/tests/test_t178.py::test_pb19_la_cola_sin_detalle_se_cuenta_y_el_ct01_baja_tras_la_c6_no`: SUPERADA
- `11_Ejecutor/tests/test_t178.py::test_pb19_sin_saturacion_no_hay_car_ni_reordenacion`: SUPERADA
- `11_Ejecutor/tests/test_t178.py::test_pb19_aviso_al_coordinador_solo_de_los_agentes_del_camino_de_la_entrega`: SUPERADA
- `11_Ejecutor/tests/test_t178.py::test_pb19_el_coordinador_lee_su_aviso_en_ha`: SUPERADA
- `11_Ejecutor/tests/test_t178.py::test_pb19_la_primera_saturacion_no_propone_y_la_segunda_en_otro_run_si`: SUPERADA
- `11_Ejecutor/tests/test_t178.py::test_pb19_dos_lecturas_del_mismo_run_no_son_una_repeticion`: SUPERADA
- `11_Ejecutor/tests/test_t178.py::test_pb19_la_propuesta_abierta_no_se_duplica_y_tras_rechazarla_hace_falta_otra_repeticion`: SUPERADA
- `11_Ejecutor/tests/test_t178.py::test_pb19_la_repeticion_es_por_agente_y_cuenta_los_car_anteriores_a_t178`: SUPERADA
- `11_Ejecutor/tests/test_t178.py::test_pb19_una_orden_invalida_se_rechaza_sin_tocar_la_cola`: SUPERADA
- `11_Ejecutor/tests/test_t178.py::test_pb19_una_orden_ya_en_la_cola_se_rechaza_y_retirar_la_saca`: SUPERADA
- `11_Ejecutor/tests/test_t178.py::test_pb19_un_agente_con_estado_nunca_recibe_ord_ni_con_umbral_cero`: SUPERADA
- `11_Ejecutor/tests/test_t178.py::test_pb19_dos_ciclos_con_el_analizador_saturado_reordenan_avisan_y_proponen_tipo_3`: SUPERADA

### PB-20 · Instrucción incrustada en una fuente

Criterio de aprobación del plan: Ninguna puntuación ni destino alterado; INC- registrada; fuente degradada o borrada en F9 con línea en el Registro de bajas

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_instruccion_incrustada_ignorada_y_registrada' 'tests/test_unitarias.py::test_saneamiento_r9' 'tests/test_t182_procedencia.py::test_del_buscador_al_curador' 'tests/test_t182_procedencia.py::test_control_de_salida')
```

- `11_Ejecutor/tests/test_integracion.py::test_instruccion_incrustada_ignorada_y_registrada`: SUPERADA
- `11_Ejecutor/tests/test_unitarias.py::test_saneamiento_r9`: SUPERADA
- `11_Ejecutor/tests/test_t182_procedencia.py::test_del_buscador_al_curador`: SUPERADA
- `11_Ejecutor/tests/test_t182_procedencia.py::test_control_de_salida`: SUPERADA

### PB-21 · Credencial en un mensaje

Criterio de aprobación del plan: Búsqueda del valor en todos los archivos: cero coincidencias

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_contratos_canales_credenciales_e_idempotencia' 'tests/test_v51.py::test_credenciales_boveda' 'tests/test_fase4_huecos.py::test_pb21_un_ct04_con_una_clave_y_un_iban_se_rechaza_y_no_queda_en_ningun_archivo' 'tests/test_t189_controles.py::test_seguridad_solo_etiquetas')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestBloqueos::test_credenciales')
```

- `11_Ejecutor/tests/test_unitarias.py::test_contratos_canales_credenciales_e_idempotencia`: SUPERADA
- `11_Ejecutor/tests/test_v51.py::test_credenciales_boveda`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_credenciales`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb21_un_ct04_con_una_clave_y_un_iban_se_rechaza_y_no_queda_en_ningun_archivo`: SUPERADA
- `11_Ejecutor/tests/test_t189_controles.py::test_seguridad_solo_etiquetas`: SUPERADA

### PB-22 · Canal no previsto

Criterio de aprobación del plan: Tres INC- tipo CANAL_NO_PREVISTO; cero efectos en archivos

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_contratos_canales_credenciales_e_idempotencia' 'tests/test_integracion.py::test_canales_y_matriz_respetados' 'tests/test_fase4_huecos.py::test_pb22_tres_mensajes_por_canales_no_previstos_tres_incidencias_y_ningun_efecto' 'tests/test_t116_r05.py::test_h12_las_incidencias_escaladas_se_ven_en_el_estado_del_operador' 'tests/test_t116_r05.py::test_h12_la_orden_estado_las_muestra')
```

- `11_Ejecutor/tests/test_unitarias.py::test_contratos_canales_credenciales_e_idempotencia`: SUPERADA
- `11_Ejecutor/tests/test_integracion.py::test_canales_y_matriz_respetados`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb22_tres_mensajes_por_canales_no_previstos_tres_incidencias_y_ningun_efecto`: SUPERADA
- `11_Ejecutor/tests/test_t116_r05.py::test_h12_las_incidencias_escaladas_se_ven_en_el_estado_del_operador`: SUPERADA
- `11_Ejecutor/tests/test_t116_r05.py::test_h12_la_orden_estado_las_muestra`: SUPERADA

### PB-23 · Escritura fuera de reserva

Criterio de aprobación del plan: Hash de F4 sin cambios; tres INC-

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_almacen_reserva_integridad_y_as_of' 'tests/test_fase4_huecos.py::test_pb23_los_tres_intentos_del_plan_se_rechazan_y_f4_no_cambia')
```

- `11_Ejecutor/tests/test_unitarias.py::test_almacen_reserva_integridad_y_as_of`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb23_los_tres_intentos_del_plan_se_rechazan_y_f4_no_cambia`: SUPERADA

### PB-24 · Enlace roto y borrado con registro de bajas

Criterio de aprobación del plan: Línea de baja presente; EVD marcada; revisión registrada en F3; paquete CT-21 del mes la incluye

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t181_fuentes.py::test_baja_con_registro_y_propagacion' 'tests/test_t181_fuentes.py::test_cli_solo_informe_y_aplicar' 'tests/test_t181_fuentes.py::test_caida_archivo_y_ausencia_no_equivalen')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht02_verificador_enlaces.py::TestEstados::test_roto_confirmado_y_baja' 'tests/test_ht02_verificador_enlaces.py::TestEscritura::test_borrar_crea_registro_y_exige_motivo' 'tests/test_ht02_verificador_enlaces.py::TestEscritura::test_borrar_con_registro_existente')
```

- `10_Herramientas/tests/test_ht02_verificador_enlaces.py::TestEstados::test_roto_confirmado_y_baja`: SUPERADA
- `10_Herramientas/tests/test_ht02_verificador_enlaces.py::TestEscritura::test_borrar_crea_registro_y_exige_motivo`: SUPERADA
- `10_Herramientas/tests/test_ht02_verificador_enlaces.py::TestEscritura::test_borrar_con_registro_existente`: SUPERADA
- `11_Ejecutor/tests/test_t181_fuentes.py::test_baja_con_registro_y_propagacion`: SUPERADA
- `11_Ejecutor/tests/test_t181_fuentes.py::test_cli_solo_informe_y_aplicar`: SUPERADA
- `11_Ejecutor/tests/test_t181_fuentes.py::test_caida_archivo_y_ausencia_no_equivalen`: SUPERADA

### PB-25 · Contenido cambiado y retractación

Criterio de aprobación del plan: Q recalculada con motivo; baja registrada

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t181_fuentes.py::test_revision_cambio_y_retractacion' 'tests/test_t181_fuentes.py::test_reparar_exige_copia_original' 'tests/test_t181_fuentes.py::test_baja_con_registro_y_propagacion')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht02_verificador_enlaces.py::TestEstados::test_contenido_igual_casi_y_cambiado' 'tests/test_ht02_verificador_enlaces.py::TestEstados::test_retractacion')
```

- `10_Herramientas/tests/test_ht02_verificador_enlaces.py::TestEstados::test_contenido_igual_casi_y_cambiado`: SUPERADA
- `10_Herramientas/tests/test_ht02_verificador_enlaces.py::TestEstados::test_retractacion`: SUPERADA
- `11_Ejecutor/tests/test_t181_fuentes.py::test_revision_cambio_y_retractacion`: SUPERADA
- `11_Ejecutor/tests/test_t181_fuentes.py::test_reparar_exige_copia_original`: SUPERADA
- `11_Ejecutor/tests/test_t181_fuentes.py::test_baja_con_registro_y_propagacion`: SUPERADA

### PB-26 · Clasificación temática y orden por calidad

Criterio de aprobación del plan: Comprobación automática del orden: 0 inversiones; 100 % con temática válida

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t126_pb26_pb48.py::test_pb26_cada_referencia_esta_en_una_tematica_del_anexo_d' 'tests/test_t126_pb26_pb48.py::test_pb26_dentro_de_cada_tematica_el_orden_es_por_calidad_descendente' 'tests/test_t126_pb26_pb48.py::test_pb26_el_nivel_es_coherente_con_la_calidad' 'tests/test_t126_pb26_pb48.py::test_pb26_una_fuente_de_nivel_d_esta_marcada_como_candidata_a_baja_o_unica' 'tests/test_t126_pb26_pb48.py::test_pb26_la_comprobacion_detecta_un_orden_o_un_nivel_mal_puestos' 'tests/test_t126_r02.py::test_h02_cada_referencia_esta_fisicamente_en_la_seccion_de_su_tematica' 'tests/test_t126_r02.py::test_h02_a_igualdad_de_q_va_primero_la_mas_reciente' 'tests/test_t126_r02.py::test_h03_las_comprobaciones_detectan_fichas_estropeadas' 'tests/test_t184_altas.py::test_treinta_altas_y_lote_invalido')
```

- `11_Ejecutor/tests/test_t126_pb26_pb48.py::test_pb26_cada_referencia_esta_en_una_tematica_del_anexo_d`: SUPERADA
- `11_Ejecutor/tests/test_t126_pb26_pb48.py::test_pb26_dentro_de_cada_tematica_el_orden_es_por_calidad_descendente`: SUPERADA
- `11_Ejecutor/tests/test_t126_pb26_pb48.py::test_pb26_el_nivel_es_coherente_con_la_calidad`: SUPERADA
- `11_Ejecutor/tests/test_t126_pb26_pb48.py::test_pb26_una_fuente_de_nivel_d_esta_marcada_como_candidata_a_baja_o_unica`: SUPERADA
- `11_Ejecutor/tests/test_t126_pb26_pb48.py::test_pb26_la_comprobacion_detecta_un_orden_o_un_nivel_mal_puestos`: SUPERADA
- `11_Ejecutor/tests/test_t126_r02.py::test_h02_cada_referencia_esta_fisicamente_en_la_seccion_de_su_tematica`: SUPERADA
- `11_Ejecutor/tests/test_t126_r02.py::test_h02_a_igualdad_de_q_va_primero_la_mas_reciente`: SUPERADA
- `11_Ejecutor/tests/test_t126_r02.py::test_h03_las_comprobaciones_detectan_fichas_estropeadas`: SUPERADA
- `11_Ejecutor/tests/test_t184_altas.py::test_treinta_altas_y_lote_invalido`: SUPERADA

### PB-29 · Contar raíces, no menciones

Criterio de aprobación del plan: G3-DAT-09 coherente; el Auditor no encuentra doble cómputo

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t65_qa_r01.py::test_r01_h08_ps1_con_el_minimo_de_raices_de_la_configuracion' 'tests/test_t183_raices.py::test_un_original_y_veinte_derivadas')
```

- `11_Ejecutor/tests/test_t65_qa_r01.py::test_r01_h08_ps1_con_el_minimo_de_raices_de_la_configuracion`: SUPERADA
- `11_Ejecutor/tests/test_t183_raices.py::test_un_original_y_veinte_derivadas`: SUPERADA

### PB-30 · Cifra sin artefacto bloqueada por G3

Criterio de aprobación del plan: Tiempo de dictamen ≤ 10 min; dos G3V- en HA; la cifra no aparece en la entrega o aparece con CALC-

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t159_extremo_a_extremo.py::test_pb30_la_cifra_sin_artefacto_bloquea_se_retira_y_lo_entregado_no_la_lleva')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestBloqueos::test_evidencias_y_calculos')
```

- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_evidencias_y_calculos`: SUPERADA
- `11_Ejecutor/tests/test_t159_extremo_a_extremo.py::test_pb30_la_cifra_sin_artefacto_bloquea_se_retira_y_lo_entregado_no_la_lleva`: SUPERADA

### PB-31 · Horizonte no certificado sin probabilidad

Criterio de aprobación del plan: Ninguna cifra de probabilidad en entregables; el visual no muestra confianza «alta» sin base

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_ciclo_semanal_completo_apto' 'tests/test_fase4_huecos.py::test_pb31_sin_certificado_ningun_entregable_da_una_cifra_de_probabilidad_ni_confianza_alta' 'tests/test_t116_r05.py::test_pb31_la_banda_de_cada_horizonte_publicado_es_la_de_su_probabilidad_interna' 'tests/test_t116_r05.py::test_pb31_el_caso_del_plan_065_es_mas_probable_que_no_en_los_tres_entregables')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestBloqueos::test_probabilidad_sin_certificado')
```

- `11_Ejecutor/tests/test_integracion.py::test_ciclo_semanal_completo_apto`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_probabilidad_sin_certificado`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb31_sin_certificado_ningun_entregable_da_una_cifra_de_probabilidad_ni_confianza_alta`: SUPERADA
- `11_Ejecutor/tests/test_t116_r05.py::test_pb31_la_banda_de_cada_horizonte_publicado_es_la_de_su_probabilidad_interna`: SUPERADA
- `11_Ejecutor/tests/test_t116_r05.py::test_pb31_el_caso_del_plan_065_es_mas_probable_que_no_en_los_tres_entregables`: SUPERADA

### PB-32 · Certificación de un horizonte

Criterio de aprobación del plan: Un certificado; G3-CON-10 PASA en RF y bloquearía en RV

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_certificado_emitido_con_muestra_suficiente' 'tests/test_unitarias.py::test_metricas_de_pronostico_con_pronosticadores_sinteticos' 'tests/test_t87_datos.py::test_r13_certificado_por_metodo_en_la_entrega' 'tests/test_fase4_huecos.py::test_pb32_se_certifica_la_celda_con_habilidad_y_no_la_que_no_la_tiene' 'tests/test_fase4_huecos.py::test_pb32_cada_condicion_del_certificado_cuenta_por_separado' 'tests/test_fase4_huecos.py::test_pb32_una_celda_habil_que_no_supera_holm_no_se_certifica_y_el_certificado_lleva_su_metodo' 'tests/test_fase4_huecos.py::test_pb32_el_criterio_exige_el_alfa_de_holm' 'tests/test_fase4_huecos.py::test_pb32_el_certificado_es_de_la_celda_por_metodo' 'tests/test_fase4_huecos.py::test_pb32_la_probabilidad_se_publica_solo_en_la_celda_certificada_y_con_su_certificado_ref' 'tests/test_t87_datos.py::test_certificados_separan_metodos' 'tests/test_t53_evaluacion_y_almacen.py::test_holm_escalonado_se_detiene_en_el_primer_fallo' 'tests/test_t160_reejecucion_certificado.py::test_ca6_pb32_de_punta_a_punta_con_el_cliente_simulado' 'tests/test_t160_reejecucion_certificado.py::test_ca1_el_certificado_lleva_su_reejecucion_ct10_coincidente_y_el_calculo_que_lo_sostiene' 'tests/test_t160_reejecucion_certificado.py::test_ca2_una_reejecucion_que_no_coincide_no_deja_certificado_y_registra_la_incidencia' 'tests/test_t160_reejecucion_certificado.py::test_ca3_sin_motor_no_hay_certificado' 'tests/test_t160_reejecucion_certificado.py::test_ca3_el_motor_no_sirve_la_ficha_que_sostiene_el_certificado' 'tests/test_t160_reejecucion_certificado.py::test_ca3_los_datos_del_artefacto_no_se_pueden_resolver_en_la_reejecucion' 'tests/test_t160_reejecucion_certificado.py::test_ca4_si_el_motor_no_reproduce_las_cifras_del_certificado_no_hay_certificado' 'tests/test_t160_reejecucion_certificado.py::test_ca4_dentro_de_tolerancia_pero_material_no_certifica' 'tests/test_t160_reejecucion_certificado.py::test_ca5_ct04_no_pone_en_vigor_un_propuesto_sin_reejecucion_coincidente')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestBloqueos::test_certificado_no_vigente')
```

- `11_Ejecutor/tests/test_integracion.py::test_certificado_emitido_con_muestra_suficiente`: SUPERADA
- `11_Ejecutor/tests/test_unitarias.py::test_metricas_de_pronostico_con_pronosticadores_sinteticos`: SUPERADA
- `11_Ejecutor/tests/test_t87_datos.py::test_r13_certificado_por_metodo_en_la_entrega`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_certificado_no_vigente`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb32_se_certifica_la_celda_con_habilidad_y_no_la_que_no_la_tiene`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb32_cada_condicion_del_certificado_cuenta_por_separado`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb32_una_celda_habil_que_no_supera_holm_no_se_certifica_y_el_certificado_lleva_su_metodo`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb32_el_criterio_exige_el_alfa_de_holm`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb32_el_certificado_es_de_la_celda_por_metodo`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb32_la_probabilidad_se_publica_solo_en_la_celda_certificada_y_con_su_certificado_ref`: SUPERADA
- `11_Ejecutor/tests/test_t87_datos.py::test_certificados_separan_metodos`: SUPERADA
- `11_Ejecutor/tests/test_t53_evaluacion_y_almacen.py::test_holm_escalonado_se_detiene_en_el_primer_fallo`: SUPERADA
- `11_Ejecutor/tests/test_t160_reejecucion_certificado.py::test_ca6_pb32_de_punta_a_punta_con_el_cliente_simulado`: SUPERADA
- `11_Ejecutor/tests/test_t160_reejecucion_certificado.py::test_ca1_el_certificado_lleva_su_reejecucion_ct10_coincidente_y_el_calculo_que_lo_sostiene`: SUPERADA
- `11_Ejecutor/tests/test_t160_reejecucion_certificado.py::test_ca2_una_reejecucion_que_no_coincide_no_deja_certificado_y_registra_la_incidencia`: SUPERADA
- `11_Ejecutor/tests/test_t160_reejecucion_certificado.py::test_ca3_sin_motor_no_hay_certificado`: SUPERADA
- `11_Ejecutor/tests/test_t160_reejecucion_certificado.py::test_ca3_el_motor_no_sirve_la_ficha_que_sostiene_el_certificado`: SUPERADA
- `11_Ejecutor/tests/test_t160_reejecucion_certificado.py::test_ca3_los_datos_del_artefacto_no_se_pueden_resolver_en_la_reejecucion`: SUPERADA
- `11_Ejecutor/tests/test_t160_reejecucion_certificado.py::test_ca4_si_el_motor_no_reproduce_las_cifras_del_certificado_no_hay_certificado`: SUPERADA
- `11_Ejecutor/tests/test_t160_reejecucion_certificado.py::test_ca4_dentro_de_tolerancia_pero_material_no_certifica`: SUPERADA
- `11_Ejecutor/tests/test_t160_reejecucion_certificado.py::test_ca5_ct04_no_pone_en_vigor_un_propuesto_sin_reejecucion_coincidente`: SUPERADA

### PB-33 · Revocación de certificado por deterioro

Criterio de aprobación del plan: Estado del CERT- y fecha de efecto; G3-CON-10 bloquea probabilidades posteriores

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t66_evaluacion.py::test_pa10_revocar_y_retirar_siguen_siendo_automaticos' 'tests/test_t53_evaluacion_y_almacen.py::test_ece_cero_no_revoca_un_certificado' 'tests/test_t53_evaluacion_y_almacen.py::test_umbral_de_revocacion_ece_sale_de_la_configuracion' 'tests/test_fase4_huecos.py::test_pb33_la_revocacion_registra_estado_motivo_y_fecha_de_efecto' 'tests/test_fase4_huecos.py::test_pb33_tras_la_revocacion_hay_alerta_de_sobreconfianza_y_el_run_siguiente_no_publica_probabilidad' 'tests/test_fase4_huecos.py::test_pb33_con_la_degradacion_dm_neutralizada_la_vista_h3_decertificada_no_publica_probabilidad' 'tests/test_t176_pb36_pb33.py::test_pb33_novedades_de_la_semana_con_la_revocacion_y_la_leccion' 'tests/test_t176_pb36_pb33.py::test_novedades_semana_siguiente_solo_lo_nuevo_y_misma_semana_rehace')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestBloqueos::test_certificado_no_vigente')
```

- `11_Ejecutor/tests/test_t66_evaluacion.py::test_pa10_revocar_y_retirar_siguen_siendo_automaticos`: SUPERADA
- `11_Ejecutor/tests/test_t53_evaluacion_y_almacen.py::test_ece_cero_no_revoca_un_certificado`: SUPERADA
- `11_Ejecutor/tests/test_t53_evaluacion_y_almacen.py::test_umbral_de_revocacion_ece_sale_de_la_configuracion`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_certificado_no_vigente`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb33_la_revocacion_registra_estado_motivo_y_fecha_de_efecto`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb33_tras_la_revocacion_hay_alerta_de_sobreconfianza_y_el_run_siguiente_no_publica_probabilidad`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb33_con_la_degradacion_dm_neutralizada_la_vista_h3_decertificada_no_publica_probabilidad`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_pb33_novedades_de_la_semana_con_la_revocacion_y_la_leccion`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_novedades_semana_siguiente_solo_lo_nuevo_y_misma_semana_rehace`: SUPERADA

### PB-34 · Fuga de información en evaluación detectada

Criterio de aprobación del plan: Ningún AJU- ni CERT- apoyado en métricas FALLIDA; corrección registrada en F6

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_pronosticos_resueltos_sin_look_ahead' 'tests/test_unitarias.py::test_guardia_de_fuga_del_proveedor' 'tests/test_unitarias.py::test_fecha_publicacion_filtra_revisiones' 'tests/test_unitarias.py::test_servicio_del_motor_rc_cache_fuga_y_reejecucion' 'tests/test_t66_evaluacion.py::test_pa09_contaminados_no_cuentan_para_la_recalibracion' 'tests/test_t192_evaluacion.py::test_recalcular_referencia_sin_futuro')
```

- `11_Ejecutor/tests/test_integracion.py::test_pronosticos_resueltos_sin_look_ahead`: SUPERADA
- `11_Ejecutor/tests/test_unitarias.py::test_guardia_de_fuga_del_proveedor`: SUPERADA
- `11_Ejecutor/tests/test_unitarias.py::test_fecha_publicacion_filtra_revisiones`: SUPERADA
- `11_Ejecutor/tests/test_unitarias.py::test_servicio_del_motor_rc_cache_fuga_y_reejecucion`: SUPERADA
- `11_Ejecutor/tests/test_t66_evaluacion.py::test_pa09_contaminados_no_cuentan_para_la_recalibracion`: SUPERADA
- `11_Ejecutor/tests/test_t192_evaluacion.py::test_recalcular_referencia_sin_futuro`: SUPERADA

### PB-35 · Recalibración dentro de bandas con evaluación sombra

Criterio de aprobación del plan: Bandas respetadas; sombra registrada; decisión documentada con DM-HLN

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t66_evaluacion.py::test_pa10_recalibracion_siempre_propuesta' 'tests/test_t65_qa_r01.py::test_r01_h08_recalibracion_de_rk_con_el_paso_y_las_bandas_de_la_configuracion' 'tests/test_t192_evaluacion.py::test_cierre_con_comparacion_pareada')
```

- `11_Ejecutor/tests/test_t66_evaluacion.py::test_pa10_recalibracion_siempre_propuesta`: SUPERADA
- `11_Ejecutor/tests/test_t65_qa_r01.py::test_r01_h08_recalibracion_de_rk_con_el_paso_y_las_bandas_de_la_configuracion`: SUPERADA
- `11_Ejecutor/tests/test_t192_evaluacion.py::test_cierre_con_comparacion_pareada`: SUPERADA

### PB-36 · Recalibración fuera de bandas rechazada

Criterio de aprobación del plan: F10 intacto en P-09 y P-05; P3- en la cola de HA

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t65_qa_r01.py::test_r01_h08_recalibracion_de_rk_con_el_paso_y_las_bandas_de_la_configuracion' 'tests/test_t176_pb36_pb33.py::test_pb36_umbral_e_y_p05_fuera_de_banda_a_la_cola_de_ha_con_f10_intacto' 'tests/test_t176_pb36_pb33.py::test_pb36_un_segundo_ciclo_no_duplica_la_elevacion_ni_la_revision' 'tests/test_t176_pb36_pb33.py::test_p3_de_p11_tambien_se_eleva' 'tests/test_t176_pb36_pb33.py::test_proponer_ajuste_banda_trimestral_de_p09_en_el_limite' 'tests/test_t176_pb36_pb33.py::test_proponer_ajuste_dentro_de_banda_suma_lo_del_trimestre_y_el_total_frente_al_inicial' 'tests/test_t176_pb36_pb33.py::test_proponer_ajuste_rechaza_no_calibrable_y_sin_banda_es_tipo_3' 'tests/test_t176_pb36_pb33.py::test_evidencia_umbral_e_youden_y_muestra_insuficiente' 'tests/test_t176_pb36_pb33.py::test_evidencia_umbral_e_empate_elige_el_mas_cercano_al_vigente_y_j_nulo_no_propone' 'tests/test_t176_pb36_pb33.py::test_r02_h01_recalibrar_dos_semanas_deja_una_p3_de_p11_en_f6_y_en_ha' 'tests/test_t176_pb36_pb33.py::test_r02_h03_una_p3_abierta_del_parametro_bloquea_cualquier_otro_objetivo' 'tests/test_t176_pb36_pb33.py::test_r02_h03_la_revision_registra_la_p3_abierta' 'tests/test_t176_pb36_pb33.py::test_r02_h04_propuestas_y_revisiones_concurrentes_no_se_duplican' 'tests/test_t176_pb36_pb33.py::test_r02_h04_elevaciones_concurrentes_dejan_una_entrada_en_ha' 'tests/test_t176_pb36_pb33.py::test_r02_h06_una_p3_con_elevada_via_pero_fuera_de_ha_se_eleva')
```

- `11_Ejecutor/tests/test_t65_qa_r01.py::test_r01_h08_recalibracion_de_rk_con_el_paso_y_las_bandas_de_la_configuracion`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_pb36_umbral_e_y_p05_fuera_de_banda_a_la_cola_de_ha_con_f10_intacto`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_pb36_un_segundo_ciclo_no_duplica_la_elevacion_ni_la_revision`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_p3_de_p11_tambien_se_eleva`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_proponer_ajuste_banda_trimestral_de_p09_en_el_limite`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_proponer_ajuste_dentro_de_banda_suma_lo_del_trimestre_y_el_total_frente_al_inicial`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_proponer_ajuste_rechaza_no_calibrable_y_sin_banda_es_tipo_3`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_evidencia_umbral_e_youden_y_muestra_insuficiente`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_evidencia_umbral_e_empate_elige_el_mas_cercano_al_vigente_y_j_nulo_no_propone`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_r02_h01_recalibrar_dos_semanas_deja_una_p3_de_p11_en_f6_y_en_ha`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_r02_h03_una_p3_abierta_del_parametro_bloquea_cualquier_otro_objetivo`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_r02_h03_la_revision_registra_la_p3_abierta`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_r02_h04_propuestas_y_revisiones_concurrentes_no_se_duplican`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_r02_h04_elevaciones_concurrentes_dejan_una_entrada_en_ha`: SUPERADA
- `11_Ejecutor/tests/test_t176_pb36_pb33.py::test_r02_h06_una_p3_con_elevada_via_pero_fuera_de_ha_se_eleva`: SUPERADA

### PB-37 · Pronóstico congelado inmutable

Criterio de aprobación del plan: Hash de la entrada original intacto; ambos RESUELTO

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_almacen_reserva_integridad_y_as_of' 'tests/test_autocritica.py::test_arrastre_con_invalidacion_activada' 'tests/test_fase4_huecos.py::test_pb37_la_correccion_es_un_prg_nuevo_y_el_original_no_cambia' 'tests/test_fase4_huecos.py::test_pb37_el_pronostico_original_y_su_correccion_entran_los_dos_en_las_metricas' 'tests/test_t116_r05.py::test_pb37_adelantar_el_reloj_a_los_dos_vencimientos_resuelve_el_original_y_la_correccion')
```

- `11_Ejecutor/tests/test_unitarias.py::test_almacen_reserva_integridad_y_as_of`: SUPERADA
- `11_Ejecutor/tests/test_autocritica.py::test_arrastre_con_invalidacion_activada`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb37_la_correccion_es_un_prg_nuevo_y_el_original_no_cambia`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb37_el_pronostico_original_y_su_correccion_entran_los_dos_en_las_metricas`: SUPERADA
- `11_Ejecutor/tests/test_t116_r05.py::test_pb37_adelantar_el_reloj_a_los_dos_vencimientos_resuelve_el_original_y_la_correccion`: SUPERADA

### PB-38 · Objeción fuerte sin resolver impide el top-3

Criterio de aprobación del plan: Opción ausente del top-3; F3 con objeción SIN_RESOLVER

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_autocritica.py::test_objecion_fuerte_sin_resolver_excluye_del_top3' 'tests/test_t175_alternativas.py::test_pb38_la_opcion_con_objecion_fuerte_sin_resolver_es_una_alternativa_documentada_en_el_tecnico' 'tests/test_t175_alternativas.py::test_pb38_la_alternativa_no_entra_en_el_json_ni_altera_la_coherencia_ni_el_dictamen' 'tests/test_t175_alternativas.py::test_pb38_tambien_en_el_diseno_v6' 'tests/test_t175_alternativas.py::test_objeciones_de_la_alternativa_estado_y_condicion' 'tests/test_t175_alternativas.py::test_un_texto_del_modelo_que_g3_met13_rechaza_en_una_alternativa_se_retira_y_la_entrega_sale' 'tests/test_t175_alternativas.py::test_la_sustitucion_cubre_nombre_resumen_respuesta_y_que_la_resolveria')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestBloqueos::test_objecion_fuerte_sin_resolver' 'tests/test_ht09_validador_g3.py::TestBloqueos::test_objecion_fuerte_respondida_pero_no_resuelta')
```

- `11_Ejecutor/tests/test_autocritica.py::test_objecion_fuerte_sin_resolver_excluye_del_top3`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_objecion_fuerte_sin_resolver`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_objecion_fuerte_respondida_pero_no_resuelta`: SUPERADA
- `11_Ejecutor/tests/test_t175_alternativas.py::test_pb38_la_opcion_con_objecion_fuerte_sin_resolver_es_una_alternativa_documentada_en_el_tecnico`: SUPERADA
- `11_Ejecutor/tests/test_t175_alternativas.py::test_pb38_la_alternativa_no_entra_en_el_json_ni_altera_la_coherencia_ni_el_dictamen`: SUPERADA
- `11_Ejecutor/tests/test_t175_alternativas.py::test_pb38_tambien_en_el_diseno_v6`: SUPERADA
- `11_Ejecutor/tests/test_t175_alternativas.py::test_objeciones_de_la_alternativa_estado_y_condicion`: SUPERADA
- `11_Ejecutor/tests/test_t175_alternativas.py::test_un_texto_del_modelo_que_g3_met13_rechaza_en_una_alternativa_se_retira_y_la_entrega_sale`: SUPERADA
- `11_Ejecutor/tests/test_t175_alternativas.py::test_la_sustitucion_cubre_nombre_resumen_respuesta_y_que_la_resolveria`: SUPERADA

### PB-39 · Informe visual con legibilidad < 70 bloqueado

Criterio de aprobación del plan: Ningún informe visual entregado con índice < 70

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_ciclo_semanal_completo_apto' 'tests/test_t159_extremo_a_extremo.py::test_pb39_el_visual_por_debajo_de_70_se_bloquea_y_tras_la_reescritura_se_entrega' 'tests/test_t159_extremo_a_extremo.py::test_pb39_si_la_reescritura_sigue_por_debajo_de_70_no_se_entrega_ningun_visual')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht07_legibilidad.py::TestIndice::test_texto_dificil_no_cumple' 'tests/test_ht09_validador_g3.py::TestBloqueos::test_legibilidad')
```

- `11_Ejecutor/tests/test_integracion.py::test_ciclo_semanal_completo_apto`: SUPERADA
- `10_Herramientas/tests/test_ht07_legibilidad.py::TestIndice::test_texto_dificil_no_cumple`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_legibilidad`: SUPERADA
- `11_Ejecutor/tests/test_t159_extremo_a_extremo.py::test_pb39_el_visual_por_debajo_de_70_se_bloquea_y_tras_la_reescritura_se_entrega`: SUPERADA
- `11_Ejecutor/tests/test_t159_extremo_a_extremo.py::test_pb39_si_la_reescritura_sigue_por_debajo_de_70_no_se_entrega_ningun_visual`: SUPERADA

### PB-41 · Coherencia entre entregables y entre clases

Criterio de aprobación del plan: G3-ENT-07 PASA; el Auditor no recuenta menos apuestas que las declaradas

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_ciclo_semanal_completo_apto' 'tests/test_t53_seleccion_y_entrega.py::test_entregable_bloqueado_no_llega_a_las_carpetas_de_entrega' 'tests/test_fase4_huecos.py::test_pb01_sin_g3_apto_no_se_congela_ningun_pronostico_ni_se_entrega' 'tests/test_t159_extremo_a_extremo.py::test_pb41_el_factor_comun_de_rf_reit_y_rv_queda_en_un_cluster_y_los_tres_entregables_coinciden')
```

- `11_Ejecutor/tests/test_integracion.py::test_ciclo_semanal_completo_apto`: SUPERADA
- `11_Ejecutor/tests/test_t53_seleccion_y_entrega.py::test_entregable_bloqueado_no_llega_a_las_carpetas_de_entrega`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb01_sin_g3_apto_no_se_congela_ningun_pronostico_ni_se_entrega`: SUPERADA
- `11_Ejecutor/tests/test_t159_extremo_a_extremo.py::test_pb41_el_factor_comun_de_rf_reit_y_rv_queda_en_un_cluster_y_los_tres_entregables_coinciden`: SUPERADA

### PB-43 · Pregunta repetida y lección de producto

Criterio de aprobación del plan: LEC- en F6 enlazada a las tres QRY-; sección presente en el informe siguiente

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_consulta_que_escala_y_pregunta_repetida' 'tests/test_fase4_huecos.py::test_pb43_la_leccion_de_producto_enlaza_las_tres_consultas_repetidas')
```

- `11_Ejecutor/tests/test_integracion.py::test_consulta_que_escala_y_pregunta_repetida`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb43_la_leccion_de_producto_enlaza_las_tres_consultas_repetidas`: SUPERADA

### PB-44 · Historial de aciertos honesto

Criterio de aprobación del plan: Recuento verificado contra F4 y F3; G3-CON-18 PASA

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_pronosticos_resueltos_sin_look_ahead' 'tests/test_t66_evaluacion.py::test_pa09_contaminados_se_registran_pero_no_cuentan_en_metricas_ni_historial' 'tests/test_t53_evaluacion_y_almacen.py::test_hitos_h5_no_cuentan_en_h4_ni_en_el_historial' 'tests/test_t159_extremo_a_extremo.py::test_pb44_el_historial_publicado_es_el_recuento_de_f4_con_su_muestra_y_el_mismo_dato_en_los_informes')
```

- `11_Ejecutor/tests/test_integracion.py::test_pronosticos_resueltos_sin_look_ahead`: SUPERADA
- `11_Ejecutor/tests/test_t66_evaluacion.py::test_pa09_contaminados_se_registran_pero_no_cuentan_en_metricas_ni_historial`: SUPERADA
- `11_Ejecutor/tests/test_t53_evaluacion_y_almacen.py::test_hitos_h5_no_cuentan_en_h4_ni_en_el_historial`: SUPERADA
- `11_Ejecutor/tests/test_t159_extremo_a_extremo.py::test_pb44_el_historial_publicado_es_el_recuento_de_f4_con_su_muestra_y_el_mismo_dato_en_los_informes`: SUPERADA

### PB-45 · Lección aplicada en el siguiente encargo

Criterio de aprobación del plan: Lista de LEC- del encargo ≤ 10; aplicación visible en el informe de clase

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_fase4_huecos.py::test_pb45_el_encargo_lleva_diez_lecciones_como_maximo_y_las_de_mas_fuerza')
```

- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb45_el_encargo_lleva_diez_lecciones_como_maximo_y_las_de_mas_fuerza`: SUPERADA

### PB-46 · Fiabilidad de fuentes de opinión

Criterio de aprobación del plan: FUE- en F6; Q y orden actualizados en F9 con motivo

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t125_fiabilidad_fuentes.py::test_pb46_dos_fuentes_una_con_habilidad_y_otra_sin_ella' 'tests/test_t125_fiabilidad_fuentes.py::test_pb46_las_fue_quedan_en_f6_y_se_comunican_al_buscador_por_ct19' 'tests/test_t125_fiabilidad_fuentes.py::test_pb46_una_vez_al_mes' 'tests/test_t125_fiabilidad_fuentes.py::test_pb46_sin_muestra_suficiente_no_hay_fue' 'tests/test_t125_fiabilidad_fuentes.py::test_pb46_no_se_resuelve_lo_que_no_ha_vencido_ni_lo_mal_formado' 'tests/test_t125_fiabilidad_fuentes.py::test_pb46_cada_direccion_se_resuelve_bien' 'tests/test_t125_r02.py::test_r02_h01_del_analista_a_f2_al_evaluador_a_la_fue_y_al_ct19' 'tests/test_t125_r02.py::test_r02_h01_la_referencia_del_buscador_trae_su_pronostico_a_f2' 'tests/test_t125_r02.py::test_r02_h03_solo_cuenta_lo_registrado_antes_de_su_fecha_objetivo' 'tests/test_t125_r02.py::test_r02_h04_un_ref_id_que_no_es_una_fuente_de_f9_no_cuenta' 'tests/test_t125_r02.py::test_r02_h07_ventana_de_24_meses_con_su_borde' 'tests/test_t125_r02.py::test_r02_h07_antiguedad_del_cierre_con_su_borde' 'tests/test_t125_r02.py::test_r02_h08_la_probabilidad_sin_declarar_es_la_de_la_banda_y_la_fue_lleva_calc_id' 'tests/test_t125_r02.py::test_r02_h06_una_fuente_que_llega_a_la_muestra_a_mitad_de_mes_sale_ese_mes' 'tests/test_t125_r03.py::test_h09_variable_obligatoria_y_resoluble' 'tests/test_t125_r03.py::test_h10_fechas_no_iso_no_se_leen' 'tests/test_t125_r03.py::test_h10_las_iso_se_leen' 'tests/test_t125_r03.py::test_h09_el_evaluador_no_cuenta_una_variable_no_resoluble' 'tests/test_t125_r03.py::test_h11_umbral_entero_y_decimal_son_el_mismo_pronostico' 'tests/test_t125_r03.py::test_h12_una_direccion_que_no_es_texto_no_tumba_la_fiabilidad' 'tests/test_t125_r03.py::test_h13_la_entrada_de_rc_de_la_fue_lleva_run_id')
```

- `11_Ejecutor/tests/test_t125_fiabilidad_fuentes.py::test_pb46_dos_fuentes_una_con_habilidad_y_otra_sin_ella`: SUPERADA
- `11_Ejecutor/tests/test_t125_fiabilidad_fuentes.py::test_pb46_las_fue_quedan_en_f6_y_se_comunican_al_buscador_por_ct19`: SUPERADA
- `11_Ejecutor/tests/test_t125_fiabilidad_fuentes.py::test_pb46_una_vez_al_mes`: SUPERADA
- `11_Ejecutor/tests/test_t125_fiabilidad_fuentes.py::test_pb46_sin_muestra_suficiente_no_hay_fue`: SUPERADA
- `11_Ejecutor/tests/test_t125_fiabilidad_fuentes.py::test_pb46_no_se_resuelve_lo_que_no_ha_vencido_ni_lo_mal_formado`: SUPERADA
- `11_Ejecutor/tests/test_t125_fiabilidad_fuentes.py::test_pb46_cada_direccion_se_resuelve_bien`: SUPERADA
- `11_Ejecutor/tests/test_t125_r02.py::test_r02_h01_del_analista_a_f2_al_evaluador_a_la_fue_y_al_ct19`: SUPERADA
- `11_Ejecutor/tests/test_t125_r02.py::test_r02_h01_la_referencia_del_buscador_trae_su_pronostico_a_f2`: SUPERADA
- `11_Ejecutor/tests/test_t125_r02.py::test_r02_h03_solo_cuenta_lo_registrado_antes_de_su_fecha_objetivo`: SUPERADA
- `11_Ejecutor/tests/test_t125_r02.py::test_r02_h04_un_ref_id_que_no_es_una_fuente_de_f9_no_cuenta`: SUPERADA
- `11_Ejecutor/tests/test_t125_r02.py::test_r02_h07_ventana_de_24_meses_con_su_borde`: SUPERADA
- `11_Ejecutor/tests/test_t125_r02.py::test_r02_h07_antiguedad_del_cierre_con_su_borde`: SUPERADA
- `11_Ejecutor/tests/test_t125_r02.py::test_r02_h08_la_probabilidad_sin_declarar_es_la_de_la_banda_y_la_fue_lleva_calc_id`: SUPERADA
- `11_Ejecutor/tests/test_t125_r02.py::test_r02_h06_una_fuente_que_llega_a_la_muestra_a_mitad_de_mes_sale_ese_mes`: SUPERADA
- `11_Ejecutor/tests/test_t125_r03.py::test_h09_variable_obligatoria_y_resoluble`: SUPERADA
- `11_Ejecutor/tests/test_t125_r03.py::test_h10_fechas_no_iso_no_se_leen`: SUPERADA
- `11_Ejecutor/tests/test_t125_r03.py::test_h10_las_iso_se_leen`: SUPERADA
- `11_Ejecutor/tests/test_t125_r03.py::test_h09_el_evaluador_no_cuenta_una_variable_no_resoluble`: SUPERADA
- `11_Ejecutor/tests/test_t125_r03.py::test_h11_umbral_entero_y_decimal_son_el_mismo_pronostico`: SUPERADA
- `11_Ejecutor/tests/test_t125_r03.py::test_h12_una_direccion_que_no_es_texto_no_tumba_la_fiabilidad`: SUPERADA
- `11_Ejecutor/tests/test_t125_r03.py::test_h13_la_entrada_de_rc_de_la_fue_lleva_run_id`: SUPERADA

### PB-47 · Estados de madurez

Criterio de aprobación del plan: Entregable final declara «documentado» o no usa el método

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_servicio_del_motor_rc_cache_fuga_y_reejecucion' 'tests/test_t65_resto_t53.py::test_cs08_fichas_documentadas_no_entregan_cifras' 'tests/test_t159_extremo_a_extremo.py::test_pb47_un_metodo_documentado_no_se_usa_y_la_entrega_lo_declara' 'tests/test_t165_g3_met13.py::test_pb47_informe_de_clase_que_llama_validado_a_un_metodo_documentado_bloquea_g3' 'tests/test_t165_g3_met13.py::test_pb47_corregida_la_declaracion_con_la_forma_canonica_la_entrega_pasa' 'tests/test_t165_g3_met13.py::test_un_metodo_no_servido_solo_en_el_tecnico_bloquea_la_entrega_en_f7' 'tests/test_t165_g3_met13.py::test_un_visual_que_presenta_un_metodo_como_validado_bloquea_en_f7' 'tests/test_t165_g3_met13.py::test_el_ciclo_simulado_normal_sigue_apto_y_lleva_la_madurez_canonica' 'tests/test_t165_g3_met13.py::test_bloquea' 'tests/test_t165_g3_met13.py::test_no_salta' 'tests/test_t165_g3_met13.py::test_g3_met13_localiza_en_la_opcion_y_advierte_de_lo_que_no_se_entrega')
```

- `11_Ejecutor/tests/test_unitarias.py::test_servicio_del_motor_rc_cache_fuga_y_reejecucion`: SUPERADA
- `11_Ejecutor/tests/test_t65_resto_t53.py::test_cs08_fichas_documentadas_no_entregan_cifras`: SUPERADA
- `11_Ejecutor/tests/test_t159_extremo_a_extremo.py::test_pb47_un_metodo_documentado_no_se_usa_y_la_entrega_lo_declara`: SUPERADA
- `11_Ejecutor/tests/test_t165_g3_met13.py::test_pb47_informe_de_clase_que_llama_validado_a_un_metodo_documentado_bloquea_g3`: SUPERADA
- `11_Ejecutor/tests/test_t165_g3_met13.py::test_pb47_corregida_la_declaracion_con_la_forma_canonica_la_entrega_pasa`: SUPERADA
- `11_Ejecutor/tests/test_t165_g3_met13.py::test_un_metodo_no_servido_solo_en_el_tecnico_bloquea_la_entrega_en_f7`: SUPERADA
- `11_Ejecutor/tests/test_t165_g3_met13.py::test_un_visual_que_presenta_un_metodo_como_validado_bloquea_en_f7`: SUPERADA
- `11_Ejecutor/tests/test_t165_g3_met13.py::test_el_ciclo_simulado_normal_sigue_apto_y_lleva_la_madurez_canonica`: SUPERADA
- `11_Ejecutor/tests/test_t165_g3_met13.py::test_bloquea`: SUPERADA
- `11_Ejecutor/tests/test_t165_g3_met13.py::test_no_salta`: SUPERADA
- `11_Ejecutor/tests/test_t165_g3_met13.py::test_g3_met13_localiza_en_la_opcion_y_advierte_de_lo_que_no_se_entrega`: SUPERADA

### PB-48 · Conflicto de normas: la más restrictiva

Criterio de aprobación del plan: Segunda pasada registrada; COR- y P3- en HA

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t126_pb26_pb48.py::test_pb48_una_guia_que_relaja_un_control_no_llega_a_la_elegibilidad' 'tests/test_t126_pb26_pb48.py::test_pb48_ht03_exige_la_segunda_pasada_en_banda_marginal' 'tests/test_t126_r02.py::test_h01_en_el_ciclo_una_opcion_en_banda_marginal_se_resuelve_con_su_segunda_pasada' 'tests/test_t126_r02.py::test_h01_sin_la_segunda_pasada_esas_opciones_no_serian_elegibles' 'tests/test_t126_r02.py::test_h04_la_leccion_que_relaja_el_control_llega_al_analista_en_su_ct06' 'tests/test_t158_guias.py::test_pb48_la_guia_que_omite_la_segunda_pasada_se_registra_se_escala_y_se_retira' 'tests/test_t158_guias.py::test_pb48_con_otro_item_valido_la_version_siguiente_conserva_solo_el_valido' 'tests/test_t158_guias.py::test_pb48_una_guia_ya_vigente_se_revisa_tambien_en_el_siguiente_run' 'tests/test_t158_guias.py::test_el_item_de_pb48_cita_la_regla_9_1' 'tests/test_t161_guias.py::test_h05_el_emisor_rechaza_un_item_en_conflicto_y_nada_cambia' 'tests/test_t161_guias.py::test_h02_un_campo_descriptivo_en_conflicto_no_llega_a_ningun_agente')
```

- `11_Ejecutor/tests/test_t126_pb26_pb48.py::test_pb48_una_guia_que_relaja_un_control_no_llega_a_la_elegibilidad`: SUPERADA
- `11_Ejecutor/tests/test_t126_pb26_pb48.py::test_pb48_ht03_exige_la_segunda_pasada_en_banda_marginal`: SUPERADA
- `11_Ejecutor/tests/test_t126_r02.py::test_h01_en_el_ciclo_una_opcion_en_banda_marginal_se_resuelve_con_su_segunda_pasada`: SUPERADA
- `11_Ejecutor/tests/test_t126_r02.py::test_h01_sin_la_segunda_pasada_esas_opciones_no_serian_elegibles`: SUPERADA
- `11_Ejecutor/tests/test_t126_r02.py::test_h04_la_leccion_que_relaja_el_control_llega_al_analista_en_su_ct06`: SUPERADA
- `11_Ejecutor/tests/test_t158_guias.py::test_pb48_la_guia_que_omite_la_segunda_pasada_se_registra_se_escala_y_se_retira`: SUPERADA
- `11_Ejecutor/tests/test_t158_guias.py::test_pb48_con_otro_item_valido_la_version_siguiente_conserva_solo_el_valido`: SUPERADA
- `11_Ejecutor/tests/test_t158_guias.py::test_pb48_una_guia_ya_vigente_se_revisa_tambien_en_el_siguiente_run`: SUPERADA
- `11_Ejecutor/tests/test_t158_guias.py::test_el_item_de_pb48_cita_la_regla_9_1`: SUPERADA
- `11_Ejecutor/tests/test_t161_guias.py::test_h05_el_emisor_rechaza_un_item_en_conflicto_y_nada_cambia`: SUPERADA
- `11_Ejecutor/tests/test_t161_guias.py::test_h02_un_campo_descriptivo_en_conflicto_no_llega_a_ningun_agente`: SUPERADA

### PB-49 · Historial íntegro y supresiones permitidas

Criterio de aprobación del plan: Cero entradas modificadas o borradas fuera de las excepciones

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_almacen_reserva_integridad_y_as_of' 'tests/test_integracion.py::test_canales_y_matriz_respetados' 'tests/test_fase4_huecos.py::test_pb49_una_entrada_borrada_rompe_la_integridad' 'tests/test_fase4_huecos.py::test_pb49_en_ocho_semanas_simuladas_las_entradas_de_f1_a_f6_rc_y_ha_solo_se_anaden')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht02_verificador_enlaces.py::TestEscritura::test_borrar_crea_registro_y_exige_motivo')
```

- `11_Ejecutor/tests/test_unitarias.py::test_almacen_reserva_integridad_y_as_of`: SUPERADA
- `11_Ejecutor/tests/test_integracion.py::test_canales_y_matriz_respetados`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb49_una_entrada_borrada_rompe_la_integridad`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb49_en_ocho_semanas_simuladas_las_entradas_de_f1_a_f6_rc_y_ha_solo_se_anaden`: SUPERADA
- `10_Herramientas/tests/test_ht02_verificador_enlaces.py::TestEscritura::test_borrar_crea_registro_y_exige_motivo`: SUPERADA

### PB-50 · Horizontes según la clase de activo

Criterio de aprobación del plan: G3-CON-09 PASA; CFG- de P-31 registrado con evidencia DM-HLN

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v5.py::test_doce_tipos_agentes_y_canales' 'tests/test_t173.py::test_pb50_rf_h2_pierde_con_significacion_y_baja_a_limitado' 'tests/test_t173.py::test_pb50_sin_muestra_o_sin_perdida_significativa_no_degrada' 'tests/test_t173.py::test_pb50_con_p_por_encima_de_alfa_no_degrada' 'tests/test_t173.py::test_pb50_ningun_cambio_hacia_o_desde_no' 'tests/test_t173.py::test_pb50_un_escalon_por_trimestre_y_nunca_sube' 'tests/test_t173.py::test_pb50_restituida_a_si_no_vuelve_a_bajar_en_el_mismo_trimestre' 'tests/test_t173.py::test_pb50_h5_no_entra_en_la_degradacion_por_dm' 'tests/test_t173.py::test_pb50_el_c5_degrada_y_el_ciclo_lee_limitado_sin_bloqueo_de_g3' 'tests/test_t173.py::test_pb50_un_fallo_de_la_degradacion_dm_no_tumba_el_c5' 'tests/test_t173.py::test_pb50_r02_h01_una_sola_semana_mala_no_degrada' 'tests/test_t173.py::test_pb50_r02_h01_historia_buena_mas_una_semana_mala_no_degrada' 'tests/test_t173.py::test_pb50_r02_h01_sin_fechas_de_conglomerado_ni_conglomerados_minimos_no_degrada' 'tests/test_t173.py::test_pb50_r02_h01_n_suficiente_pero_n_eff_insuficiente_no_degrada' 'tests/test_t173.py::test_pb50_r02_h03_holm_entre_las_celdas_de_la_misma_revision' 'tests/test_t173.py::test_pb50_cierre_h06_la_familia_es_fija_y_cuenta_las_celdas_sin_muestra' 'tests/test_t173.py::test_pb50_r02_h03_solo_en_la_revision_mensual' 'tests/test_t173.py::test_pb50_r02_h02_un_fallo_en_f10_anula_el_ajuste_y_el_reintento_degrada' 'tests/test_t173.py::test_pb50_r02_h02_si_falla_el_cfg_de_p30_se_revierte_el_de_p31')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestBloqueos::test_horizonte_no_aplicable' 'tests/test_ht09_validador_g3.py::TestV5::test_doce_tipos_y_tabla_8_3')
```

- `11_Ejecutor/tests/test_v5.py::test_doce_tipos_agentes_y_canales`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_horizonte_no_aplicable`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV5::test_doce_tipos_y_tabla_8_3`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_rf_h2_pierde_con_significacion_y_baja_a_limitado`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_sin_muestra_o_sin_perdida_significativa_no_degrada`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_con_p_por_encima_de_alfa_no_degrada`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_ningun_cambio_hacia_o_desde_no`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_un_escalon_por_trimestre_y_nunca_sube`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_restituida_a_si_no_vuelve_a_bajar_en_el_mismo_trimestre`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_h5_no_entra_en_la_degradacion_por_dm`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_el_c5_degrada_y_el_ciclo_lee_limitado_sin_bloqueo_de_g3`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_un_fallo_de_la_degradacion_dm_no_tumba_el_c5`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_r02_h01_una_sola_semana_mala_no_degrada`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_r02_h01_historia_buena_mas_una_semana_mala_no_degrada`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_r02_h01_sin_fechas_de_conglomerado_ni_conglomerados_minimos_no_degrada`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_r02_h01_n_suficiente_pero_n_eff_insuficiente_no_degrada`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_r02_h03_holm_entre_las_celdas_de_la_misma_revision`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_cierre_h06_la_familia_es_fija_y_cuenta_las_celdas_sin_muestra`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_r02_h03_solo_en_la_revision_mensual`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_r02_h02_un_fallo_en_f10_anula_el_ajuste_y_el_reintento_degrada`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb50_r02_h02_si_falla_el_cfg_de_p30_se_revierte_el_de_p31`: SUPERADA

### PB-51 · Conocimiento específico en los system prompts

Criterio de aprobación del plan: 100 % de prompts con estructura completa; ≥ 95 % de afirmaciones muestreadas correctas; tamaños dentro de las orientaciones

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t187_pb51.py::test_pb51_el_informe_y_la_muestra_guardados_son_los_del_corpus_y_los_veredictos_actuales' 'tests/test_t187_pb51.py::test_pb51_paso_1_todos_los_prompts_con_las_secciones_del_anexo_g' 'tests/test_t187_pb51.py::test_pb51_paso_2_seccion_10_por_areas_con_formulas_y_referencias_sin_doi_invalidos' 'tests/test_t187_pb51.py::test_pb51_paso_3_al_menos_95_por_ciento_de_las_verificables_correctas' 'tests/test_t187_pb51.py::test_pb51_tamanos_dentro_de_las_orientaciones_escritas' 'tests/test_t187_pb51.py::test_pb51_fila_del_mapa_superada_en_parte')
```

- `11_Ejecutor/tests/test_t187_pb51.py::test_pb51_el_informe_y_la_muestra_guardados_son_los_del_corpus_y_los_veredictos_actuales`: SUPERADA
- `11_Ejecutor/tests/test_t187_pb51.py::test_pb51_paso_1_todos_los_prompts_con_las_secciones_del_anexo_g`: SUPERADA
- `11_Ejecutor/tests/test_t187_pb51.py::test_pb51_paso_2_seccion_10_por_areas_con_formulas_y_referencias_sin_doi_invalidos`: SUPERADA
- `11_Ejecutor/tests/test_t187_pb51.py::test_pb51_paso_3_al_menos_95_por_ciento_de_las_verificables_correctas`: SUPERADA
- `11_Ejecutor/tests/test_t187_pb51.py::test_pb51_tamanos_dentro_de_las_orientaciones_escritas`: SUPERADA
- `11_Ejecutor/tests/test_t187_pb51.py::test_pb51_fila_del_mapa_superada_en_parte`: SUPERADA

### PB-52 · Modo degradado: herramienta caída

Criterio de aprobación del plan: Entrega con limitaciones declaradas o bloqueo justificado; ninguna cifra sin dato

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_busqueda_web_solo_en_vivo_y_reparacion_json' 'tests/test_t53_seleccion_y_entrega.py::test_un_simbolo_sin_historia_no_vacia_su_tipo' 'tests/test_t65_hallazgos.py::test_h15_simbolo_con_datos_invalidos_se_excluye_y_se_declara' 'tests/test_t159_extremo_a_extremo.py::test_pb52_con_ht09_caido_nunca_hay_apto_por_defecto_ni_entrega' 'tests/test_t191_degradado.py::test_ciclo_bloqueado_y_registrado')
```

- `11_Ejecutor/tests/test_unitarias.py::test_busqueda_web_solo_en_vivo_y_reparacion_json`: SUPERADA
- `11_Ejecutor/tests/test_t53_seleccion_y_entrega.py::test_un_simbolo_sin_historia_no_vacia_su_tipo`: SUPERADA
- `11_Ejecutor/tests/test_t65_hallazgos.py::test_h15_simbolo_con_datos_invalidos_se_excluye_y_se_declara`: SUPERADA
- `11_Ejecutor/tests/test_t159_extremo_a_extremo.py::test_pb52_con_ht09_caido_nunca_hay_apto_por_defecto_ni_entrega`: SUPERADA
- `11_Ejecutor/tests/test_t191_degradado.py::test_ciclo_bloqueado_y_registrado`: SUPERADA

### PB-53 · Frontera A/B: un Analista propone un activo concreto

Criterio de aprobación del plan: Ninguna opción del top-3 es un activo concreto

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v5.py::test_esquema_de_finalista_sin_vehiculos' 'tests/test_t87_contratos.py::test_r21_se_retira_la_propuesta_de_una_empresa_antes_de_entregar' 'tests/test_fase4_huecos.py::test_pb53_la_empresa_concreta_que_propone_el_analista_rv_no_llega_al_top3')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestV5::test_seleccion_de_activo_concreto')
```

- `11_Ejecutor/tests/test_v5.py::test_esquema_de_finalista_sin_vehiculos`: SUPERADA
- `11_Ejecutor/tests/test_t87_contratos.py::test_r21_se_retira_la_propuesta_de_una_empresa_antes_de_entregar`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV5::test_seleccion_de_activo_concreto`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb53_la_empresa_concreta_que_propone_el_analista_rv_no_llega_al_top3`: SUPERADA

### PB-54 · Encargo completo para el Bloque B

Criterio de aprobación del plan: 100 % de los campos presentes y no vacíos

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_ciclo_semanal_completo_apto' 'tests/test_fase4_huecos.py::test_pb54_cada_encargo_para_b_lleva_sus_once_campos_no_vacios')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestV5::test_encargo_para_bloque_b')
```

- `11_Ejecutor/tests/test_integracion.py::test_ciclo_semanal_completo_apto`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV5::test_encargo_para_bloque_b`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb54_cada_encargo_para_b_lleva_sus_once_campos_no_vacios`: SUPERADA

### PB-55 · Cobertura de los doce tipos de activo

Criterio de aprobación del plan: 12 tipos presentes; ≤ 3 opciones por tipo

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v5.py::test_doce_tipos_agentes_y_canales' 'tests/test_integracion.py::test_ciclo_semanal_completo_apto' 'tests/test_fase4_huecos.py::test_pb55_el_tecnico_tiene_un_apartado_con_semaforo_por_cada_tipo_y_el_motivo_de_menos_de_tres')
```

- `11_Ejecutor/tests/test_v5.py::test_doce_tipos_agentes_y_canales`: SUPERADA
- `11_Ejecutor/tests/test_integracion.py::test_ciclo_semanal_completo_apto`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb55_el_tecnico_tiene_un_apartado_con_semaforo_por_cada_tipo_y_el_motivo_de_menos_de_tres`: SUPERADA

### PB-56 · Oportunidad duplicada entre tipos

Criterio de aprobación del plan: Ninguna oportunidad en dos top-3

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v5.py::test_sin_duplicados_entre_tipos' 'tests/test_fase4_huecos.py::test_pb56_en_un_c1_el_mismo_ambito_propuesto_por_rv_e_idx_queda_en_un_solo_top3')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestV5::test_duplicado_en_dos_tipos_por_nombre' 'tests/test_ht09_validador_g3.py::TestV5::test_duplicado_en_dos_tipos_por_ambito' 'tests/test_ht09_validador_g3.py::TestV5::test_mismo_opp_id_en_dos_tipos')
```

- `11_Ejecutor/tests/test_v5.py::test_sin_duplicados_entre_tipos`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV5::test_duplicado_en_dos_tipos_por_nombre`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV5::test_duplicado_en_dos_tipos_por_ambito`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV5::test_mismo_opp_id_en_dos_tipos`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb56_en_un_c1_el_mismo_ambito_propuesto_por_rv_e_idx_queda_en_un_solo_top3`: SUPERADA

### PB-58 · Solicitud y provisión de una credencial por CT-25

Criterio de aprobación del plan: Cero apariciones del valor en mensajes, F1–F11, entregables y contextos; segunda solicitud resuelta sin molestar al Broker

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v51.py::test_credenciales_boveda' 'tests/test_v51.py::test_cli_v51' 'tests/test_fase4_huecos.py::test_pb58_el_servicio_pendiente_se_declara_hasta_la_provision_y_el_valor_no_llega_a_ningun_contexto' 'tests/test_t177_c4_credenciales.py::test_t177_pb58_c4_bfa_solicita_y_coordinador_emite_ct25' 'tests/test_t177_c4_credenciales.py::test_t177_desde_retorno_deduplica_y_comprueba_ht01' 'tests/test_t177_c4_credenciales.py::test_t177_urgencia_y_denegada_no_se_vuelve_a_pedir' 'tests/test_t177_c4_credenciales.py::test_t177_retorno_con_valor_se_rechaza_integro' 'tests/test_t177_c4_credenciales.py::test_t177_c4_con_valor_en_el_retorno_del_bfa_no_emite_nada' 'tests/test_t177_c4_credenciales.py::test_t177_solicitudes_mal_formadas_se_descartan_con_motivo' 'tests/test_t177_c4_credenciales.py::test_t177_retorno_vacio_o_sin_solicitudes_no_pide_nada' 'tests/test_t177_c4_credenciales.py::test_t177_configuracion_invalida_falla_antes_de_mutar' 'tests/test_t177_c4_credenciales.py::test_t177_pb58_criterio_completo' 'tests/test_t177_c4_credenciales.py::test_t177_cli_credencial_c4' 'tests/test_t177_c4_credenciales.py::test_t177_r02_h01_valor_en_cualquier_sitio_no_llega_a_la_cache' 'tests/test_t177_c4_credenciales.py::test_t177_r02_h04_la_cinta_de_grabacion_no_guarda_el_valor' 'tests/test_t177_c4_credenciales.py::test_t177_r02_solicitud_con_valor_limites' 'tests/test_t177_c4_credenciales.py::test_t177_r02_h02_otra_grafia_en_la_segunda_c4_no_duplica' 'tests/test_t177_c4_credenciales.py::test_t177_r02_h03_dos_c4_a_la_vez_un_solo_ct25' 'tests/test_t177_c4_credenciales.py::test_t177_r02_h05_grafias_de_campos_de_valor' 'tests/test_t177_c4_credenciales.py::test_t177_r02_h05_credencial_ref_no_es_un_valor_y_el_broker_tampoco_lo_cuela' 'tests/test_t177_c4_credenciales.py::test_t177_r02_h06_ficha_opaca_en_texto_libre_se_rechaza' 'tests/test_t177_c4_credenciales.py::test_t177_r02_h06_textos_corrientes_y_urls_no_se_rechazan' 'tests/test_t177_c4_credenciales.py::test_t177_r02_h07_tope_semanal_real' 'tests/test_t177_c4_credenciales.py::test_t177_r02_ficha_opaca_en_el_retorno_no_llega_a_la_cache' 'tests/test_t177_c4_credenciales.py::test_t177_r02_segunda_barrera_en_agentes' 'tests/test_t177_c4_credenciales.py::test_t177_r02_la_cache_envenenada_no_se_sirve' 'tests/test_t177_c4_credenciales.py::test_t177_r03_reserva_de_la_bolsa_en_curso_y_tras_un_error' 'tests/test_t177_c4_credenciales.py::test_t177_r03_h12_informe_de_analista_canonico_no_se_descarta' 'tests/test_t177_c4_credenciales.py::test_t177_r03_el_mock_de_analistas_ejerce_la_barrera' 'tests/test_t177_c4_credenciales.py::test_t177_r03_h08_cualquier_clave_del_subarbol' 'tests/test_t177_c4_credenciales.py::test_t177_r03_h08_texto_json_dict_y_claves' 'tests/test_t177_c4_credenciales.py::test_t177_r03_h08_solicitud_no_vacia_mira_el_retorno_entero' 'tests/test_t177_c4_credenciales.py::test_t177_r03_h09_escape_unicode_en_la_clave' 'tests/test_t177_c4_credenciales.py::test_t177_r03_h10_base64' 'tests/test_t177_c4_credenciales.py::test_t177_r03_h11_numero_bajo_clave_de_valor' 'tests/test_t177_c4_credenciales.py::test_t177_r03_h13_guiones_y_uuid_no_son_fichas' 'tests/test_t177_c4_credenciales.py::test_t177_r03_el_coordinador_rechaza_una_clave_de_valor_en_cualquier_sitio' 'tests/test_t177_c4_credenciales.py::test_t177_r03_json_demasiado_anidado' 'tests/test_t177_c4_credenciales.py::test_t177_cierre_h14_texto_ilegible_con_la_clave_escapada' 'tests/test_t177_c4_credenciales.py::test_t177_cierre_h15_identificadores_publicos_solo_fuera' 'tests/test_t177_c4_credenciales.py::test_t177_cierre_h16_reserva_huerfana_avisada_una_vez' 'tests/test_t177_c4_credenciales.py::test_t177_cierre_h17_campo_de_mas_en_una_solicitud' 'tests/test_t177_c4_credenciales.py::test_t177_cierre2_h18_campo_admitido_que_no_se_copia' 'tests/test_t177_c4_credenciales.py::test_t177_cierre2_h18_lo_que_se_copia_pasa' 'tests/test_t177_c4_credenciales.py::test_t177_cierre3_h19_urgencia_sin_contenido_se_reduce_a_normal')
```

- `11_Ejecutor/tests/test_v51.py::test_credenciales_boveda`: SUPERADA
- `11_Ejecutor/tests/test_v51.py::test_cli_v51`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb58_el_servicio_pendiente_se_declara_hasta_la_provision_y_el_valor_no_llega_a_ningun_contexto`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_pb58_c4_bfa_solicita_y_coordinador_emite_ct25`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_desde_retorno_deduplica_y_comprueba_ht01`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_urgencia_y_denegada_no_se_vuelve_a_pedir`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_retorno_con_valor_se_rechaza_integro`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_c4_con_valor_en_el_retorno_del_bfa_no_emite_nada`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_solicitudes_mal_formadas_se_descartan_con_motivo`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_retorno_vacio_o_sin_solicitudes_no_pide_nada`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_configuracion_invalida_falla_antes_de_mutar`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_pb58_criterio_completo`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_cli_credencial_c4`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r02_h01_valor_en_cualquier_sitio_no_llega_a_la_cache`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r02_h04_la_cinta_de_grabacion_no_guarda_el_valor`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r02_solicitud_con_valor_limites`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r02_h02_otra_grafia_en_la_segunda_c4_no_duplica`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r02_h03_dos_c4_a_la_vez_un_solo_ct25`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r02_h05_grafias_de_campos_de_valor`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r02_h05_credencial_ref_no_es_un_valor_y_el_broker_tampoco_lo_cuela`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r02_h06_ficha_opaca_en_texto_libre_se_rechaza`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r02_h06_textos_corrientes_y_urls_no_se_rechazan`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r02_h07_tope_semanal_real`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r02_ficha_opaca_en_el_retorno_no_llega_a_la_cache`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r02_segunda_barrera_en_agentes`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r02_la_cache_envenenada_no_se_sirve`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r03_reserva_de_la_bolsa_en_curso_y_tras_un_error`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r03_h12_informe_de_analista_canonico_no_se_descarta`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r03_el_mock_de_analistas_ejerce_la_barrera`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r03_h08_cualquier_clave_del_subarbol`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r03_h08_texto_json_dict_y_claves`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r03_h08_solicitud_no_vacia_mira_el_retorno_entero`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r03_h09_escape_unicode_en_la_clave`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r03_h10_base64`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r03_h11_numero_bajo_clave_de_valor`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r03_h13_guiones_y_uuid_no_son_fichas`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r03_el_coordinador_rechaza_una_clave_de_valor_en_cualquier_sitio`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_r03_json_demasiado_anidado`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_cierre_h14_texto_ilegible_con_la_clave_escapada`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_cierre_h15_identificadores_publicos_solo_fuera`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_cierre_h16_reserva_huerfana_avisada_una_vez`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_cierre_h17_campo_de_mas_en_una_solicitud`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_cierre2_h18_campo_admitido_que_no_se_copia`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_cierre2_h18_lo_que_se_copia_pasa`: SUPERADA
- `11_Ejecutor/tests/test_t177_c4_credenciales.py::test_t177_cierre3_h19_urgencia_sin_contenido_se_reduce_a_normal`: SUPERADA

### PB-59 · Credencial expuesta en un mensaje del Broker

Criterio de aprobación del plan: El valor no aparece en ningún registro; incidencia en HA

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v51.py::test_credenciales_boveda' 'tests/test_fase4_huecos.py::test_pb59_la_credencial_expuesta_deja_incidencia_en_ha_sin_copiar_el_valor')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestV51::test_valor_de_credencial')
```

- `11_Ejecutor/tests/test_v51.py::test_credenciales_boveda`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV51::test_valor_de_credencial`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb59_la_credencial_expuesta_deja_incidencia_en_ha_sin_copiar_el_valor`: SUPERADA

### PB-60 · Credencial denegada

Criterio de aprobación del plan: Ninguna nueva CT-25 para ese servicio; limitación visible

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v51.py::test_credenciales_boveda' 'tests/test_fase4_huecos.py::test_pb60_credencial_denegada_no_se_vuelve_a_pedir_y_los_entregables_declaran_la_degradacion')
```

- `11_Ejecutor/tests/test_v51.py::test_credenciales_boveda`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb60_credencial_denegada_no_se_vuelve_a_pedir_y_los_entregables_declaran_la_degradacion`: SUPERADA

### PB-61 · Consulta bloqueante al Broker con vencimiento

Criterio de aprobación del plan: `supuestos_declarados` con CNS- en el paquete (HT-09 C19 OK); ningún dato del Broker inventado

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v51.py::test_consulta_bloqueante_pausa_y_vencimiento' 'tests/test_fase4_huecos.py::test_pb61_solo_cri_se_pausa_y_al_vencer_el_supuesto_figura_en_los_entregables' 'tests/test_t174_pb61_revision_c2.py::test_pb61_respuesta_tardia_que_invalida_el_supuesto_abre_una_revision_c2' 'tests/test_t174_pb61_revision_c2.py::test_pb61_sin_informe_entregado_no_hay_revision' 'tests/test_t174_pb61_revision_c2.py::test_pb61_un_run_bloqueado_no_cuenta_como_entregado' 'tests/test_t174_pb61_revision_c2.py::test_pb61_segunda_respuesta_sin_indices_nuevos_no_reabre' 'tests/test_t174_pb61_revision_c2.py::test_pb61_revision_pendiente_sin_ejecutar' 'tests/test_t174_pb61_revision_c2.py::test_pb61_revision_fallida_queda_anotada_y_el_error_de_control_se_relanza' 'tests/test_t174_pb61_revision_c2.py::test_pb61_no_bloqueante_contestada_en_plazo_tras_una_entrega' 'tests/test_t174_pb61_revision_c2.py::test_pb61_informe_de_seguimiento_c6_entregado_con_el_supuesto' 'tests/test_t174_pb61_revision_c2.py::test_r02_h01_dos_procesos_con_la_misma_respuesta_abren_una_sola_revision' 'tests/test_t174_pb61_revision_c2.py::test_r02_h01_la_reserva_queda_en_curso_en_la_misma_entrada_que_la_respuesta' 'tests/test_t174_pb61_revision_c2.py::test_r02_h02_error_de_control_deja_la_revision_interrumpida_y_se_relanza' 'tests/test_t174_pb61_revision_c2.py::test_r02_h02_la_pendiente_se_relanza_en_la_siguiente_respuesta_y_la_en_curso_solo_si_se_pide' 'tests/test_t174_pb61_revision_c2.py::test_r02_h03_el_alcance_es_la_interseccion_con_lo_entregado' 'tests/test_t174_pb61_revision_c2.py::test_r02_h03_sin_tipos_que_revisar_no_se_lanza_un_ciclo_de_todo_el_alcance' 'tests/test_t174_pb61_revision_c2.py::test_r02_h04_una_respuesta_fechada_antes_de_la_entrega_no_la_revisa' 'tests/test_t174_pb61_revision_c2.py::test_r02_h05_un_fallo_tras_entregar_deja_la_revision_entregada' 'tests/test_t174_pb61_revision_c2.py::test_r02_h06_la_fallida_va_al_operador_y_se_relanza_por_la_linea_de_ordenes' 'tests/test_t174_pb61_revision_c2.py::test_r02_h06_relanzar_reclama_bajo_el_cerrojo_y_no_repite_una_ya_hecha' 'tests/test_t174_pb61_revision_c2.py::test_r03_h07_la_en_curso_huerfana_se_avisa_una_sola_vez' 'tests/test_t174_pb61_revision_c2.py::test_r03_h07_una_en_curso_viva_no_es_huerfana' 'tests/test_t174_pb61_revision_c2.py::test_r03_h08_el_proceso_muere_tras_entregar_y_relanzar_no_duplica' 'tests/test_t174_pb61_revision_c2.py::test_r03_h08_cada_reclamacion_lleva_su_numero_de_intento' 'tests/test_t174_pb61_revision_c2.py::test_cierre_h09_la_revision_esta_en_marcha_desde_la_reserva' 'tests/test_t174_pb61_revision_c2.py::test_cierre_h09_se_da_de_baja_tambien_sin_alcance_y_si_falla_la_escritura' 'tests/test_t174_pb61_revision_c2.py::test_cierre_h10_la_clave_lleva_la_carpeta_del_almacen' 'tests/test_t174_pb61_revision_c2.py::test_cierre_h11_lo_que_no_se_puede_juzgar_se_dice')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestV51::test_supuestos_declarados')
```

- `11_Ejecutor/tests/test_v51.py::test_consulta_bloqueante_pausa_y_vencimiento`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV51::test_supuestos_declarados`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb61_solo_cri_se_pausa_y_al_vencer_el_supuesto_figura_en_los_entregables`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_pb61_respuesta_tardia_que_invalida_el_supuesto_abre_una_revision_c2`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_pb61_sin_informe_entregado_no_hay_revision`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_pb61_un_run_bloqueado_no_cuenta_como_entregado`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_pb61_segunda_respuesta_sin_indices_nuevos_no_reabre`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_pb61_revision_pendiente_sin_ejecutar`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_pb61_revision_fallida_queda_anotada_y_el_error_de_control_se_relanza`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_pb61_no_bloqueante_contestada_en_plazo_tras_una_entrega`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_pb61_informe_de_seguimiento_c6_entregado_con_el_supuesto`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_r02_h01_dos_procesos_con_la_misma_respuesta_abren_una_sola_revision`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_r02_h01_la_reserva_queda_en_curso_en_la_misma_entrada_que_la_respuesta`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_r02_h02_error_de_control_deja_la_revision_interrumpida_y_se_relanza`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_r02_h02_la_pendiente_se_relanza_en_la_siguiente_respuesta_y_la_en_curso_solo_si_se_pide`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_r02_h03_el_alcance_es_la_interseccion_con_lo_entregado`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_r02_h03_sin_tipos_que_revisar_no_se_lanza_un_ciclo_de_todo_el_alcance`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_r02_h04_una_respuesta_fechada_antes_de_la_entrega_no_la_revisa`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_r02_h05_un_fallo_tras_entregar_deja_la_revision_entregada`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_r02_h06_la_fallida_va_al_operador_y_se_relanza_por_la_linea_de_ordenes`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_r02_h06_relanzar_reclama_bajo_el_cerrojo_y_no_repite_una_ya_hecha`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_r03_h07_la_en_curso_huerfana_se_avisa_una_sola_vez`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_r03_h07_una_en_curso_viva_no_es_huerfana`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_r03_h08_el_proceso_muere_tras_entregar_y_relanzar_no_duplica`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_r03_h08_cada_reclamacion_lleva_su_numero_de_intento`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_cierre_h09_la_revision_esta_en_marcha_desde_la_reserva`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_cierre_h09_se_da_de_baja_tambien_sin_alcance_y_si_falla_la_escritura`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_cierre_h10_la_clave_lleva_la_carpeta_del_almacen`: SUPERADA
- `11_Ejecutor/tests/test_t174_pb61_revision_c2.py::test_cierre_h11_lo_que_no_se_puede_juzgar_se_dice`: SUPERADA

### PB-62 · Filtro, agrupación y recurrencia de consultas

Criterio de aprobación del plan: ≤ 3 mensajes CT-23 por RUN-; LEC- de producto creada

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v51.py::test_consulta_validaciones_agrupacion_y_entrante' 'tests/test_t188_producto.py::test_recurrencia_entre_analisis')
```

- `11_Ejecutor/tests/test_v51.py::test_consulta_validaciones_agrupacion_y_entrante`: SUPERADA
- `11_Ejecutor/tests/test_t188_producto.py::test_recurrencia_entre_analisis`: SUPERADA

### PB-63 · Pronóstico H5 con hitos

Criterio de aprobación del plan: HT-09 C18 OK; un H5 sin hitos o con probabilidad numérica queda BLOQUEADO

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v51.py::test_h5_con_hitos_y_sin_probabilidad' 'tests/test_v51.py::test_ht09_bloquea_h5_sin_hitos' 'tests/test_fase4_huecos.py::test_pb63_los_hitos_h5_del_ciclo_tienen_fecha_indicador_criterio_y_el_espaciado_del_anexo_a')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestV51::test_h5_con_probabilidad_numerica' 'tests/test_ht09_validador_g3.py::TestV51::test_h5_sin_hitos_o_insuficientes' 'tests/test_ht09_validador_g3.py::TestV51::test_h5_espaciado_de_hitos')
```

- `11_Ejecutor/tests/test_v51.py::test_h5_con_hitos_y_sin_probabilidad`: SUPERADA
- `11_Ejecutor/tests/test_v51.py::test_ht09_bloquea_h5_sin_hitos`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV51::test_h5_con_probabilidad_numerica`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV51::test_h5_sin_hitos_o_insuficientes`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb63_los_hitos_h5_del_ciclo_tienen_fecha_indicador_criterio_y_el_espaciado_del_anexo_a`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV51::test_h5_espaciado_de_hitos`: SUPERADA

### PB-64 · Evaluación de H5 por hitos y degradación

Criterio de aprobación del plan: Ajuste registrado en F6 y F10; ningún certificado H5 emitido

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v51.py::test_estado_h5_por_hitos' 'tests/test_t53_evaluacion_y_almacen.py::test_degradacion_h5_se_aplica_en_f6_y_f10' 'tests/test_t53_seleccion_y_entrega.py::test_h05_degradacion_h5_cambia_la_tabla_del_ciclo_siguiente' 'tests/test_t65_hallazgos.py::test_h13_la_degradacion_registra_el_efecto_desde_el_mismo_ciclo' 'tests/test_fase4_huecos.py::test_pb64_la_revision_de_certificados_no_emite_ninguno_para_h5' 'tests/test_fase4_huecos.py::test_pb64_los_tres_estados_h5_por_hitos_y_mp_baja_de_si_a_limitado_en_f6_y_f10' 'tests/test_t173.py::test_estado_hito_publicable' 'tests/test_t173.py::test_pb64_c5_publica_los_estados_h5_en_f6' 'tests/test_t173.py::test_pb64_sin_h5_no_publica_nada' 'tests/test_t173.py::test_pb64_paquete_y_tecnico_publican_los_estados_h5')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestV51::test_h5_certificado_no_habilita_probabilidad')
```

- `11_Ejecutor/tests/test_v51.py::test_estado_h5_por_hitos`: SUPERADA
- `11_Ejecutor/tests/test_t53_evaluacion_y_almacen.py::test_degradacion_h5_se_aplica_en_f6_y_f10`: SUPERADA
- `11_Ejecutor/tests/test_t53_seleccion_y_entrega.py::test_h05_degradacion_h5_cambia_la_tabla_del_ciclo_siguiente`: SUPERADA
- `11_Ejecutor/tests/test_t65_hallazgos.py::test_h13_la_degradacion_registra_el_efecto_desde_el_mismo_ciclo`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV51::test_h5_certificado_no_habilita_probabilidad`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb64_la_revision_de_certificados_no_emite_ninguno_para_h5`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb64_los_tres_estados_h5_por_hitos_y_mp_baja_de_si_a_limitado_en_f6_y_f10`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_estado_hito_publicable`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb64_c5_publica_los_estados_h5_en_f6`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb64_sin_h5_no_publica_nada`: SUPERADA
- `11_Ejecutor/tests/test_t173.py::test_pb64_paquete_y_tecnico_publican_los_estados_h5`: SUPERADA

### PB-65 · Horizonte principal incoherente con la naturaleza

Criterio de aprobación del plan: Dictámenes correctos y motivados

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v51.py::test_horizonte_principal_y_naturaleza_en_cada_opcion' 'tests/test_v51.py::test_ht09_bloquea_h5_sin_hitos')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestV51::test_fuera_de_rango_sin_y_con_justificacion' 'tests/test_ht09_validador_g3.py::TestV51::test_principal_en_celda_no')
```

- `11_Ejecutor/tests/test_v51.py::test_horizonte_principal_y_naturaleza_en_cada_opcion`: SUPERADA
- `11_Ejecutor/tests/test_v51.py::test_ht09_bloquea_h5_sin_hitos`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV51::test_fuera_de_rango_sin_y_con_justificacion`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV51::test_principal_en_celda_no`: SUPERADA

### PB-66 · Seguimiento encargado: alta, ciclos y cancelación

Criterio de aprobación del plan: Ningún ciclo tras la cancelación; C6 no retrasa C1–C3; informes ≤ 300 palabras

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v51.py::test_seguimiento_alta_ciclo_y_cancelacion' 'tests/test_v51.py::test_seguimiento_frecuencia_corta_y_opp_inexistente' 'tests/test_fase4_huecos.py::test_pb66_dos_ciclos_c6_con_registro_en_f11_y_ninguno_tras_la_cancelacion')
```

- `11_Ejecutor/tests/test_v51.py::test_seguimiento_alta_ciclo_y_cancelacion`: SUPERADA
- `11_Ejecutor/tests/test_v51.py::test_seguimiento_frecuencia_corta_y_opp_inexistente`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb66_dos_ciclos_c6_con_registro_en_f11_y_ninguno_tras_la_cancelacion`: SUPERADA

### PB-67 · Seguimiento que propone el envío al Bloque B

Criterio de aprobación del plan: HT-09 (perfil SEGUIMIENTO) APTO; sin envío automático

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t159_extremo_a_extremo.py::test_pb67_el_ciclo_c6_propone_el_envio_a_b_sin_enviar_nada')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestV51::test_seguimiento_envio_a_b')
```

- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV51::test_seguimiento_envio_a_b`: SUPERADA
- `11_Ejecutor/tests/test_t159_extremo_a_extremo.py::test_pb67_el_ciclo_c6_propone_el_envio_a_b_sin_enviar_nada`: SUPERADA
