# Evidencias del Plan de pruebas del Bloque A (Fase 4, T-116)

Generado por `.docs/scripts/evidencias_plan_a.py --ejecutar` el 2026-11-15 sobre el commit `5098b09`, con el cliente simulado (`MockClient`): sin red, sin clave y sin coste. No se edita a mano: se regenera.

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
| Superada en parte | 37 |
| Superada | 21 |
| Pendiente API | 7 |
| Requiere usuarios | 1 |
| Revisión documental | 1 |
| **Total** | **67** |

## Tabla

| Prueba | Resultado | Comprueba | No comprueba |
| --- | --- | --- | --- |
| PB-01 Ciclo periódico completo de extremo a extremo | Superada | Entregables con su nombre, archivos F1–F5, G3 APTO, tres opciones como máximo, RUN- completo en F5 y pronósticos congelados; con un ciclo anterior en memoria, N2 donde GC0 ve cambio material y N1 en el resto; los mensajes del ciclo (CT-05, CT-06, CT-11, CT-12, CT-13, CT-15, CT-02) son todos del catálogo, y solo el Coordinador escribe al Broker; sin G3 APTO no se congela ningún pronóstico ni se entrega. | La entrega en hora: el reloj es simulado. Que sean precisamente RV, RF y MP las que cambian depende de los datos sintéticos; se afirma la regla (nivel según GC0). |
| PB-02 Top-3 con menos de tres elegibles | Superada en parte | Motivo obligatorio con menos de tres opciones (ciclo y HT-09) y segunda pasada en banda marginal (HT-03). | El caso sembrado del plan (exactamente dos opciones, con una en banda marginal) no se ejecuta de extremo a extremo. |
| PB-03 Clase sin ninguna opción elegible | Superada en parte | Un tipo con cero opciones se entrega sin relleno (por presupuesto agotado) y HT-03 admite cero opciones. | El caso del plan (ALT sin ninguna elegible por puntuación) y que el Auditor no registre hallazgo, que exige el modelo real. |
| PB-04 Misma tendencia, estrategias distintas por clase | Pendiente API | — | Las lentes por tipo de activo las aplica el modelo. |
| PB-05 Marco de otra clase aplicado sin justificación | Pendiente API | — | Lo detecta el Auditor con el modelo real. |
| PB-06 Consulta N0 sin escalado | Superada | Clase ACLARACION y ruta N0; cada referencia de la respuesta es el identificador de una entrada de F1–F6 (no solo un prefijo válido); QRY- en F5 con sus referencias; cero encargos CT-05, ningún RUN- nuevo y consumo de 1 UC como máximo. | El tiempo de respuesta real (< 2 minutos) y que cada afirmación del texto del modelo real lleve su referencia. |
| PB-07 Consulta que escala a análisis | Superada en parte | Clase CONTRASTE y ruta ANALITICA; respuesta provisional por CT-03 con el nivel y el plazo; RUN- ad hoc de alcance mínimo enlazado a la QRY-. | La respuesta final por CT-03 con referencias al acabar el RUN-: el ejecutor solo envía la provisional, con el RUN- enlazado (INC-T116-03). El tiempo real de la respuesta provisional y que el Coordinador no responda con conocimiento propio (modelo real). |
| PB-08 Ráfaga de peticiones sin límite | Superada en parte | Idempotencia y acuse por mensaje; cola del monitor HT-08. | La ráfaga del plan: el 100 % registradas y respondidas, el p90 de N0, el orden por prioridad con envejecimiento y el presupuesto por nivel. |
| PB-09 Cambio de periodicidad por el Broker | Superada en parte | La periodicidad cambia en F10 (P-01) desde su fecha de efecto, los valores no válidos se rechazan y se avisa al Evaluador (CT-22). | El disparo del siguiente C1 en la fecha nueva (lo hace el planificador externo, HT-05) y que ningún otro parámetro cambie. |
| PB-10 Configuración no permitida rechazada parcialmente | Superada en parte | Estado APLICADA_PARCIALMENTE; el umbral E y la celda ALT×H1 se rechazan con su motivo y la celda sigue sin aplicarse; P-02 aplicado; ningún otro parámetro de F10 cambia salvo la lista de horizontes; HA sin incidencia de escritura. | Que F10 cambie solo en P-02: el CT-04 del ejecutor lleva una lista global de horizontes y la guarda en P-03 aunque rechace la celda ALT×H1 (INC-T116-01). |
| PB-11 Decisión del Broker sin alterar el análisis ni la evaluación | Superada en parte | La decisión del Broker se anota sin cambiar el estado de la opción en F3 y se avisa al Evaluador (CT-22); al vencer, los PRG de la opción enviada y de la descartada quedan RESUELTO y el historial de aciertos los cuenta; ningún mensaje al Bloque B. | La lección de producto que compara las enviadas con las descartadas cuando haya muestra: el Evaluador no la genera (INC-T116-03). |
| PB-12 Campos de decisión y paquete para el Bloque B | Superada | El JSON entregado cumple el esquema publicado y G3 APTO (C01, C10 y C11 en OK); la relevancia de cada opción sigue la regla del Anexo A (una CRI nueva, ALTA; una RF de seguimiento, MEDIA o BAJA); `siguiente_paso_sugerido`, `reversibilidad` y `que_cambiaria_la_conclusion` presentes; `paquete_para_bloque_B` con una entrada por opción y los mismos datos; HT-09 bloquea un paquete para B incompleto. | — |
| PB-13 GC0 negativo con arrastre verificado | Superada en parte | Nivel N1 con 5 UC como máximo, arrastre verificado, sin candidatas nuevas, solo modo ligero; las celdas de rotación exploratoria salen de la configuración. | Que la rotación exploratoria quede entre el 15 % y el 25 %. |
| PB-14 Arrastre con invalidación activada | Superada | Opción CERRADA con motivo INVALIDACION en F3 y en el paquete; sus PRG siguen ABIERTO en F4. | La explicación en «cambios frente al ciclo anterior», que es texto del modelo real. |
| PB-15 Reglas de parada por rendimientos decrecientes | Pendiente API | — | Las iteraciones del Analizador las decide el modelo. |
| PB-16 Presupuesto agotado: alcance reducido, verificación intacta | Superada | Estado PARCIAL, limitación en el informe técnico y en el visual, laguna declarada en F5, menos candidatas investigadas en RV, y G3 en F6 y F7 con las mismas comprobaciones que un ciclo completo, ninguna sin aplicar y C08 (ninguna cifra sin origen) en OK. | — |
| PB-17 Ampliación de presupuesto en el ciclo periódico | Superada en parte | Una ampliación que puede cambiar el top-3 y cabe en el tope se autoriza; una que no puede cambiarlo o que supera el tope se deniega; cada decisión deja su AUT- en HA con el motivo; en un ciclo, la denegada cierra con alcance reducido y el consumo real queda en F5. | Los campos CPI y EAC de la AUT-, que el ejecutor no registra (INC-T116-02), y una ampliación autorizada dentro de un ciclo completo. |
| PB-18 Cola saturada y apertura de instancia | Superada en parte | El monitor ordena abrir instancia (ORD-) de un agente sin estado al superar el umbral de cola. | Cero duplicados en F2 y la vuelta del tiempo medio de ingesta al objetivo. |
| PB-19 Agente de instancia única saturado | Superada en parte | Ninguna ORD- para AG-02 con seis órdenes en cola: el monitor deja un registro CAR- de su saturación, que el ciclo escribe en HA; un agente de instancia única saturado (AG-20) también deja su CAR-. | La reordenación por prioridad y el aviso al Coordinador sobre plazos, y la propuesta de tipo 3 si se repite: el CAR- solo lo anota (INC-T116-03). |
| PB-20 Instrucción incrustada en una fuente | Superada en parte | La instrucción se neutraliza, queda una incidencia MANIPULACION, ninguna puntuación cambia y el texto no llega a los entregables. | La degradación o el borrado de la fuente en F9 con su línea en el Registro de bajas; el camino del plan (una fuente que trae el Buscador y que pasa al Curador) no se ejerce; ninguna prueba afirma la EVD con `incidencia_manipulacion`; la comprobación G3-EST-06 no existe en el ejecutor ni en HT-09; y el «destino» de la fuente no se prueba. |
| PB-21 Credencial en un mensaje | Superada en parte | El CT-04 del plan (una clave API y un IBAN en el comentario) se rechaza íntegro, deja una incidencia SEGURIDAD con el campo y sin el valor, y ni la clave ni el IBAN aparecen en ningún archivo ni mensaje; lo mismo en CT-03 y con las credenciales de CT-25. | El tipo de dato protegido en la incidencia (clave API, IBAN): el ejecutor registra el campo y «credenciales o datos personales», no el tipo (INC-T116-03). |
| PB-22 Canal no previsto | Superada | Los tres mensajes del plan (Auditor → Analizador, Analista → Analista, Redactor → Broker) se rechazan, dejan tres incidencias CANAL_NO_PREVISTO marcadas para escalar al operador, que las ve en el estado (`incidencias_escaladas` de la orden `estado`, r05), y no cambian ningún archivo salvo el historial de auditoría. | — |
| PB-23 Escritura fuera de reserva | Superada | Los tres intentos del plan (el Analizador escribe en F4, Prospectiva escribe un campo de resolución y el Evaluador cambia la afirmación) se rechazan, dejan tres incidencias y la huella de F4 no cambia tras ninguno. | — |
| PB-24 Enlace roto y borrado con registro de bajas | Superada en parte | HT-02 confirma el enlace roto y borra con línea en el Registro de bajas y motivo obligatorio. | La integración en el bloque: EVD marcada, revisión registrada en F3 y el paquete CT-21 del mes. El ejecutor solo invoca HT-02. |
| PB-25 Contenido cambiado y retractación | Superada en parte | HT-02 detecta el contenido cambiado y la retractación. | El recálculo de Q con motivo en F9, que hace el Documentador con el modelo real. |
| PB-26 Clasificación temática y orden por calidad | Superada en parte | En los F7, F8 y F9 entregados: cada referencia está físicamente en la sección `## TX-nn` de su temática del Anexo D (y su campo «Temática» lo dice), 0 inversiones del orden por Q dentro de cada sección, a igualdad de Q la de año de publicación más reciente primero, el nivel A/B/C/D coherente con Q (13.3) y las de nivel D marcadas como candidatas a baja o única fuente; las mismas comprobaciones detectan un desorden, un nivel, una temática, una sección o un desempate estropeados. | El alta de 30 referencias nuevas que pide el plan: la hacen los Documentadores con el modelo real; aquí se comprueba el estado de los archivos. El desempate solo compara fichas con año de publicación: un «Documento vivo» (ANA-DOC-0089) y las fuentes de F9, que no tienen año, no se desempatan (INC-T126-01, [PROPUESTO]). |
| PB-27 Aplicación del Fondo metodológico | Pendiente API | — | Las etapas del Fondo metodológico las aplica el modelo. |
| PB-28 Alimentación continua y Novedades | Pendiente API | — | La publicación y la lectura de Novedades dependen del modelo. |
| PB-29 Contar raíces, no menciones | Superada en parte | La puerta PS1 cuenta raíces independientes con el mínimo de la configuración. | La comprobación G3 de raíces sobre un paquete real y el recuento del Auditor. El ejecutor no distingue derivadas (escribe `grado_independencia = RAIZ` siempre): «1 raíz y 20 derivadas» depende del Curador, que es un agente de lenguaje. |
| PB-30 Cifra sin artefacto bloqueada por G3 | Superada en parte | HT-09 detecta una opción sin evidencias o sin cálculos. | El caso del plan de extremo a extremo: cifra sin artefacto, dos G3V- en HA y la cifra retirada o con su CALC-. |
| PB-31 Horizonte no certificado sin probabilidad | Superada | Sin certificado, `prob` y `prob_publicada` son nulas y la etiqueta «sin ventaja demostrada todavía» figura en el JSON, en el técnico y en el visual; la banda publicada de cada horizonte es la de su probabilidad interna (`banda_publicable`) y la de 0,65 (preparación del plan) es «más probable que no» en el JSON, en la fila del técnico y en la tarjeta del visual (r05); ningún entregable da una cifra de probabilidad y el visual no pinta confianza «Alta»; HT-09 bloquea una probabilidad sin certificado. | — |
| PB-32 Certificación de un horizonte | Superada en parte | El caso del plan: con una celda con habilidad (RF × H3) y otra sin ella (RV × H3) se emite un solo certificado, el de RF. Cada condición del certificado (muestra efectiva, IC del BSS, calibración frente al nulo y tope de ECE) impide por sí sola certificar, y también Holm: el criterio exige el alfa corregido y el Evaluador se lo pasa (una celda hábil en la que Holm se detiene no se certifica). El certificado es de la celda × método y cada método cuenta aparte. La probabilidad solo se publica en la celda certificada, con su `certificado_ref`, y HT-09 la bloquea en las demás. | La re-ejecución CT-10 coincidente que el plan pide para el certificado: el Evaluador no la hace (INC-T116-03). |
| PB-33 Revocación de certificado por deterioro | Superada en parte | Un certificado se revoca por falta de habilidad o por calibración, con el umbral de la configuración; queda REVOCADO con motivo y fecha, antes de esa fecha seguía vigente y los pronósticos congelados no cambian. Con el caso del plan (celda certificada que pierde la habilidad), la revisión del ciclo revoca, deja en F6 la lección CALIBRACION de sobreconfianza de la celda y el RUN- posterior no publica probabilidad en ella; HT-09 bloquea probabilidades con un certificado no vigente. | La sección «Novedades» de F6: el ejecutor no la publica; la revocación y la lección quedan como entradas de F6 (INC-T116-03). |
| PB-34 Fuga de información en evaluación detectada | Superada en parte | Ningún dato posterior a la fecha de corte (proveedor, Motor y resolución) y los pronósticos contaminados no cuentan para recalibrar. | La corrección registrada en F6 tras detectar la fuga. |
| PB-35 Recalibración dentro de bandas con evaluación sombra | Superada en parte | La recalibración respeta el paso y las bandas de la configuración y queda como propuesta. | El registro de la evaluación sombra y la decisión documentada con DM-HLN. |
| PB-36 Recalibración fuera de bandas rechazada | Superada en parte | Fuera de banda no se aplica: sale una propuesta P3 con el motivo. | El caso del plan (umbral E en P-09 y P-05 con banda PENDIENTE_OPERADOR): el Evaluador solo recalibra los pesos de RK (P-11), y su P3- queda en F6, no en la cola de HA como PENDING_OPERATOR (INC-T116-03). |
| PB-37 Pronóstico congelado inmutable | Superada | El alta congelada no se puede reescribir; la corrección es un PRG nuevo con `version_de`; la entrada original queda igual byte a byte; al adelantar el reloj a cada vencimiento, `Evaluador.resolver` resuelve el original en su fecha (con su nivel mal transcrito, sin cambios) y la corrección en la suya (r05): los dos RESUELTO y los dos en las métricas. Un pronóstico modificado a mano rompe la cadena de huellas. | Que Prospectiva decida corregir (modelo real): el ejecutor no tiene una operación propia de corrección; la corrección es un alta nueva de AG-10 con `version_de`. |
| PB-38 Objeción fuerte sin resolver impide el top-3 | Superada en parte | La opción con una objeción fuerte sin resolver no entra en el top-3 y queda en F3 como no elegible; HT-09 lo bloquea. | Que la objeción figure en el informe técnico como sin resolver y la opción como alternativa documentada: el técnico solo lista las objeciones de las opciones del top-3 (INC-T116-03). |
| PB-39 Informe visual con legibilidad < 70 bloqueado | Superada en parte | El visual entregado tiene índice de 70 o más; HT-07 mide un texto difícil por debajo y HT-09 comprueba la legibilidad. | El bloqueo y la reescritura en un ciclo con un visual por debajo de 70. |
| PB-40 Comprensión del informe visual por usuarios inexpertos | Requiere usuarios | — | Requiere usuarios reales. |
| PB-41 Coherencia entre entregables y entre clases | Superada en parte | El ciclo solo entrega con la comprobación de coherencia superada (G3 APTO); con entregables incoherentes, G3 bloquea, nada llega a las carpetas de entrega y no se congela ningún pronóstico. | El caso del plan (RF larga, REIT y RV de crecimiento con el mismo factor en un clúster común y `apuestas_independientes` que lo refleja) y el recuento del Auditor (modelo real). |
| PB-42 Auditoría asíncrona sin bloqueo y hallazgo posterior | Pendiente API | — | Los hallazgos de la auditoría posterior exigen el modelo real; el ejecutor registra AUD- y HAL- tras la entrega. |
| PB-43 Pregunta repetida y lección de producto | Superada | A la tercera repetición, aviso CT-22 al Evaluador y una lección de producto en F6 enlazada a las tres QRY-, con un tema normalizado común en F5. | Que preguntas con palabras distintas den el mismo tema (lo normaliza el Coordinador, modelo real) y la sección en el informe siguiente (la aplica el modelo a partir de la lección). |
| PB-44 Historial de aciertos honesto | Superada en parte | El historial publicado no usa resoluciones posteriores a su fecha, ni contaminados, ni hitos de H5. | El recuento exacto del historial contra F4 y F3 con el escenario del plan (28 opciones, n = 27 con la NO_RESOLUBLE declarada); `significativo` false con n < 30 y su nota de muestra pequeña; que el técnico y el visual («Cómo nos fue») den el mismo dato; y G3-CON-18 PASA sobre ese historial. |
| PB-45 Lección aplicada en el siguiente encargo | Superada | Con 14 lecciones vigentes del tipo y una estadística, el encargo CT-06 lleva diez: la estadística primero, después las recurrentes, y ninguna de otro tipo de activo. | La aplicación de la lección en el informe del Analista y la comprobación AS-11 del Auditor, que son del modelo real. |
| PB-46 Fiabilidad de fuentes de opinión | Superada en parte | El caso del plan (dos fuentes de 25 pronósticos explícitos, una con habilidad y otra sin ella): FUE- en F6 con n, aciertos, BSS (Brier del Motor, FC-EVAL-001, con su `calc_id`), BSS contraído con k = 20 y puntos de historial (por encima y por debajo del neutro 10), una por fuente y mes y comunicadas al Buscador por CT-19. En ciclos (r02 de T-125): el pronóstico que devuelve el Analista o el Buscador llega a F2 con su bloque y, vencido, sale en la FUE- y en el CT-19; solo cuenta lo registrado antes de su fecha objetivo, de una fuente de F9, dentro de la ventana y con cierre reciente. | La recalificación de Q y el orden en F9, que hace el Buscador con el modelo real (T-125). En backtest no entra ningún pronóstico de una fuente de F9 sin fecha (el filtro de evidencia no la da por conocible): el camino se prueba en modo vivo con el cliente simulado. |
| PB-47 Estados de madurez | Superada en parte | Una ficha no implementada se rechaza con METODO_NO_IMPLEMENTADO y una con código provisional no da cifras. | Que el entregable final declare «documentado» cuando un método no se pudo usar. |
| PB-48 Conflicto de normas: la más restrictiva | Superada en parte | Una lección vigente que sugiere omitir la segunda pasada en banda marginal llega al Analista en su CT-06 pero no a las entradas de HT-03; en el ciclo, las opciones en banda marginal llegan a HT-03 con la segunda pasada del Analista, se resuelven con ella y la segunda pasada queda registrada en F3 (sin ella, PS8 las dejaría fuera); ninguna opción entregada incumple un control; HT-03 exige la segunda pasada en banda marginal (R23 por construcción). | El registro del conflicto (COR-) y su escalado (P3-): el ejecutor no tiene las guías CT-18 del Orquestador (INC-T126-01). La segunda pasada la decide el Analista (simulado, que la hace siempre en la prueba); el ejecutor no la pide si falta: la opción queda no elegible por PS8. |
| PB-49 Historial íntegro y supresiones permitidas | Superada | En ocho semanas simuladas, cada instantánea de F1–F6, RC y HA contiene la anterior byte a byte (solo añadidos) y todo sigue íntegro; la cadena de huellas detecta una entrada modificada y una borrada (del medio o la última); las supresiones de F7–F9 las hace HT-02 con su línea en el Registro de bajas y motivo obligatorio. | — |
| PB-50 Horizontes según la clase de activo | Superada en parte | La tabla de horizontes por tipo y el bloqueo de HT-09 a un horizonte no aplicable. | El cambio automático de «Sí» a «Limitado» de un horizonte que pierde frente a la referencia (RF × H2, con DM-HLN) y su CFG- de P-31: el Evaluador solo degrada H5, por hitos (INC-T116-03). |
| PB-51 Conocimiento específico en los system prompts | Revisión documental | — | Revisión documental de los prompts de sistema; no es una prueba del ejecutor. |
| PB-52 Modo degradado: herramienta caída | Superada en parte | Una salida no conforme o un símbolo sin datos dan una entrega PARCIAL con la limitación declarada y sin cifras inventadas. | El caso del plan como tal: una herramienta caída a mitad de ciclo. |
| PB-53 Frontera A/B: un Analista propone un activo concreto | Superada | El caso del plan en un C1: el Analista RV propone una empresa concreta y no llega al top-3 ni al encargo para B ni a los informes; la ficha de finalista no admite vehículos, la propuesta de una empresa se retira antes de entregar y HT-09 bloquea un activo concreto. | — |
| PB-54 Encargo completo para el Bloque B | Superada | Cada encargo para el Bloque B lleva sus once campos presentes y no vacíos (ámbito, tesis, horizontes, pronósticos, catalizadores, riesgos, invalidación, indicador, criterios, métricas y preguntas) y cumple el esquema. | — |
| PB-55 Cobertura de los doce tipos de activo | Superada | Los doce tipos en el paquete, en el informe visual y en el técnico (un apartado con su semáforo por tipo), con tres opciones como máximo cada uno y el motivo cuando hay menos. | — |
| PB-56 Oportunidad duplicada entre tipos | Superada | El caso del plan en un C1: RV e IDX proponen el mismo ámbito y queda en un solo top-3, con el motivo de la otra en F3; ningún nombre ni ámbito en dos top-3. La regla (se quita la de menor RK, con su motivo) sobre la función, y HT-09 bloquea un duplicado por nombre, por ámbito o por identificador. | — |
| PB-57 Estrategias de los tipos nuevos | Pendiente API | — | Lo audita el Auditor con el modelo real. |
| PB-58 Solicitud y provisión de una credencial por CT-25 | Superada en parte | Solicitud con CRD- en F5 sin valor; servicio degradado y declarado en los entregables hasta la provisión (corrección de INC-T116-03); depósito en la bóveda y respuesta solo con estado y alias; la herramienta obtiene el valor de la bóveda; la segunda solicitud se resuelve sin volver al Broker; el valor no aparece en ningún archivo, mensaje, entregable ni contexto enviado a los agentes. | Los pasos 1 y 2 del plan: el ejecutor no lee `solicitudes_credenciales` del retorno del Buscador (ni de un Analista) ni tiene el mantenimiento C4 en el que el Buscador las detecta; la solicitud CT-25 se emite con `credenciales.solicitar` (orden `credencial solicitar`). Declarado en INC-T116-03 (r05). |
| PB-59 Credencial expuesta en un mensaje del Broker | Superada | El mensaje con el valor se rechaza, queda una incidencia SEGURIDAD en HA, el valor no aparece en ningún archivo ni mensaje y se pide depositar y renovar; HT-09 bloquea un valor de credencial en el paquete. | — |
| PB-60 Credencial denegada | Superada | Tras la denegación queda la limitación de servicio en F10; una nueva necesidad del mismo servicio no envía ninguna CT-25, salvo con cambio de circunstancias; el paquete, el informe técnico, el JSON y el visual del ciclo declaran la degradación, y dejan de declararla cuando la credencial se provee (corrección de INC-T116-03). | — |
| PB-61 Consulta bloqueante al Broker con vencimiento | Superada en parte | Solo CRI se pausa y RV sigue; al vencer, el análisis continúa con el supuesto declarado, que figura en el paquete, en el JSON y en el informe técnico (C19 de HT-09 en OK); la respuesta tardía se marca. | Que la respuesta tardía abra una revisión C2: el ejecutor solo lo indica en la respuesta (INC-T116-03). Que el modelo no invente un dato del Broker. |
| PB-62 Filtro, agrupación y recurrencia de consultas | Superada en parte | Tres CT-23 como máximo por RUN- (la cuarta se agrupa), validaciones y aviso de consulta recurrente. | La LEC- de producto: el aviso CONSULTA_RECURRENTE sale, pero el ejecutor no crea la lección (INC-T116-03). |
| PB-63 Pronóstico H5 con hitos | Superada | H5 solo con banda y tres hitos HIT- o más, cada uno con fecha, indicador y criterio, el primero a 12 meses como máximo y 24 como máximo entre hitos, congelados en F4 con su PRG padre (C18 en OK); HT-09 bloquea un H5 sin hitos o con probabilidad numérica y advierte del espaciado. | — |
| PB-64 Evaluación de H5 por hitos y degradación | Superada en parte | H5 se evalúa por hitos con sus tres estados (EN_CURSO_CONFORME, DESVIADO, INVALIDADO); con 20 hitos y el 40 % cumplidos MP × H5 baja de «Sí» a «Limitado» con el ajuste en F6 y en F10 y cambia la tabla del ciclo siguiente; la revisión de certificados no emite ninguno para H5. | Que los estados se publiquen: el ejecutor los calcula y los usa en el seguimiento C6, pero no los publica en F6 ni en los entregables (INC-T116-03). |
| PB-65 Horizonte principal incoherente con la naturaleza | Superada | Los tres casos del plan en HT-09: fuera de rango sin justificación, BLOQUEADO; con justificación, APTO_CON_ADVERTENCIAS; principal en una celda «No» (DER con H5), BLOQUEADO. En el ciclo, cada opción es coherente o está justificada. | El dictamen del Orquestador sobre la advertencia (CT-14), que es del modelo real. |
| PB-66 Seguimiento encargado: alta, ciclos y cancelación | Superada | Alta con SEG- en F11 y EN_SEGUIMIENTO y `seg_id` en F3; dos ciclos C6 con informe de 300 palabras como máximo, una recomendación y HT-09 sin bloqueo; pausa y reanudación con la fecha del siguiente ciclo; cancelación inmediata y ningún ciclo después. | Que C6 no retrase C1–C3: el reloj es simulado. |
| PB-67 Seguimiento que propone el envío al Bloque B | Superada en parte | HT-09 (perfil SEGUIMIENTO) da APTO a PROPONER_ENVIO_A_B con su paquete y elegible, y BLOQUEADO sin él. | Un ciclo C6 del ejecutor que produzca esa recomendación y la comprobación de que no hay envío automático. |

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
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_ciclo_semanal_completo_apto')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht03_puntuaciones.py::TestSeleccion::test_menos_de_tres' 'tests/test_ht09_validador_g3.py::TestBloqueos::test_menos_de_tres_sin_motivo' 'tests/test_ht03_puntuaciones.py::TestOpcion::test_banda_marginal_sin_y_con_segunda_pasada')
```

- `11_Ejecutor/tests/test_integracion.py::test_ciclo_semanal_completo_apto`: SUPERADA
- `10_Herramientas/tests/test_ht03_puntuaciones.py::TestSeleccion::test_menos_de_tres`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_menos_de_tres_sin_motivo`: SUPERADA
- `10_Herramientas/tests/test_ht03_puntuaciones.py::TestOpcion::test_banda_marginal_sin_y_con_segunda_pasada`: SUPERADA

### PB-03 · Clase sin ninguna opción elegible

Criterio de aprobación del plan: Cero opciones ALT; el Auditor no registra hallazgo por ello

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_presupuesto_agotado_parcial_declarado')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht03_puntuaciones.py::TestSeleccion::test_cero_opciones')
```

- `11_Ejecutor/tests/test_integracion.py::test_presupuesto_agotado_parcial_declarado`: SUPERADA
- `10_Herramientas/tests/test_ht03_puntuaciones.py::TestSeleccion::test_cero_opciones`: SUPERADA

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
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_consulta_que_escala_y_pregunta_repetida' 'tests/test_fase4_huecos.py::test_pb07_la_consulta_de_contraste_responde_provisional_con_nivel_y_plazo')
```

- `11_Ejecutor/tests/test_integracion.py::test_consulta_que_escala_y_pregunta_repetida`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb07_la_consulta_de_contraste_responde_provisional_con_nivel_y_plazo`: SUPERADA

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
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_peticion_ad_hoc_y_decisiones' 'tests/test_fase4_huecos.py::test_pb10_la_configuracion_rechazada_en_parte_no_toca_nada_mas')
```

- `11_Ejecutor/tests/test_integracion.py::test_peticion_ad_hoc_y_decisiones`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb10_la_configuracion_rechazada_en_parte_no_toca_nada_mas`: SUPERADA

### PB-11 · Decisión del Broker sin alterar el análisis ni la evaluación

Criterio de aprobación del plan: Ningún mensaje del bloque al Bloque B; ambos PRG RESUELTO; HAC- con n que incluye OPP-B

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_peticion_ad_hoc_y_decisiones' 'tests/test_fase4_huecos.py::test_pb11_la_opcion_descartada_se_resuelve_y_cuenta_en_el_historial')
```

- `11_Ejecutor/tests/test_integracion.py::test_peticion_ad_hoc_y_decisiones`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb11_la_opcion_descartada_se_resuelve_y_cuenta_en_el_historial`: SUPERADA

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
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_gc0_negativo_arrastre_verificado' 'tests/test_t65_resto_t53.py::test_cs10_celdas_de_rotacion_exploratoria_de_la_configuracion')
```

- `11_Ejecutor/tests/test_integracion.py::test_gc0_negativo_arrastre_verificado`: SUPERADA
- `11_Ejecutor/tests/test_t65_resto_t53.py::test_cs10_celdas_de_rotacion_exploratoria_de_la_configuracion`: SUPERADA

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
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_fase4_huecos.py::test_pb17_ampliacion_autorizada_y_denegada_dejan_su_aut_en_ha' 'tests/test_fase4_huecos.py::test_pb17_en_un_ciclo_la_ampliacion_denegada_cierra_con_alcance_reducido')
```

- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb17_ampliacion_autorizada_y_denegada_dejan_su_aut_en_ha`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb17_en_un_ciclo_la_ampliacion_denegada_cierra_con_alcance_reducido`: SUPERADA

### PB-18 · Cola saturada y apertura de instancia

Criterio de aprobación del plan: Apertura ≤ 1 ciclo de lectura tras superar el umbral; cero duplicados en F2; tiempo medio de ingesta vuelve al objetivo

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_ht04_y_ht06_y_ht08' 'tests/test_t53_evaluacion_y_almacen.py::test_monitor_abre_instancias_de_los_analistas_nuevos')
```

- `11_Ejecutor/tests/test_unitarias.py::test_ht04_y_ht06_y_ht08`: SUPERADA
- `11_Ejecutor/tests/test_t53_evaluacion_y_almacen.py::test_monitor_abre_instancias_de_los_analistas_nuevos`: SUPERADA

### PB-19 · Agente de instancia única saturado

Criterio de aprobación del plan: Cero ORD- para AG-02; registro CAR- de la saturación

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_ht04_y_ht06_y_ht08' 'tests/test_t53_evaluacion_y_almacen.py::test_monitor_abre_instancias_de_los_analistas_nuevos' 'tests/test_fase4_huecos.py::test_pb19_el_analizador_saturado_no_abre_instancias_y_deja_su_registro_car_en_ha')
```

- `11_Ejecutor/tests/test_unitarias.py::test_ht04_y_ht06_y_ht08`: SUPERADA
- `11_Ejecutor/tests/test_t53_evaluacion_y_almacen.py::test_monitor_abre_instancias_de_los_analistas_nuevos`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb19_el_analizador_saturado_no_abre_instancias_y_deja_su_registro_car_en_ha`: SUPERADA

### PB-20 · Instrucción incrustada en una fuente

Criterio de aprobación del plan: Ninguna puntuación ni destino alterado; INC- registrada; fuente degradada o borrada en F9 con línea en el Registro de bajas

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_instruccion_incrustada_ignorada_y_registrada' 'tests/test_unitarias.py::test_saneamiento_r9')
```

- `11_Ejecutor/tests/test_integracion.py::test_instruccion_incrustada_ignorada_y_registrada`: SUPERADA
- `11_Ejecutor/tests/test_unitarias.py::test_saneamiento_r9`: SUPERADA

### PB-21 · Credencial en un mensaje

Criterio de aprobación del plan: Búsqueda del valor en todos los archivos: cero coincidencias

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_contratos_canales_credenciales_e_idempotencia' 'tests/test_v51.py::test_credenciales_boveda' 'tests/test_fase4_huecos.py::test_pb21_un_ct04_con_una_clave_y_un_iban_se_rechaza_y_no_queda_en_ningun_archivo')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestBloqueos::test_credenciales')
```

- `11_Ejecutor/tests/test_unitarias.py::test_contratos_canales_credenciales_e_idempotencia`: SUPERADA
- `11_Ejecutor/tests/test_v51.py::test_credenciales_boveda`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_credenciales`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb21_un_ct04_con_una_clave_y_un_iban_se_rechaza_y_no_queda_en_ningun_archivo`: SUPERADA

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
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht02_verificador_enlaces.py::TestEstados::test_roto_confirmado_y_baja' 'tests/test_ht02_verificador_enlaces.py::TestEscritura::test_borrar_crea_registro_y_exige_motivo' 'tests/test_ht02_verificador_enlaces.py::TestEscritura::test_borrar_con_registro_existente')
```

- `10_Herramientas/tests/test_ht02_verificador_enlaces.py::TestEstados::test_roto_confirmado_y_baja`: SUPERADA
- `10_Herramientas/tests/test_ht02_verificador_enlaces.py::TestEscritura::test_borrar_crea_registro_y_exige_motivo`: SUPERADA
- `10_Herramientas/tests/test_ht02_verificador_enlaces.py::TestEscritura::test_borrar_con_registro_existente`: SUPERADA

### PB-25 · Contenido cambiado y retractación

Criterio de aprobación del plan: Q recalculada con motivo; baja registrada

```bash
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht02_verificador_enlaces.py::TestEstados::test_contenido_igual_casi_y_cambiado' 'tests/test_ht02_verificador_enlaces.py::TestEstados::test_retractacion')
```

- `10_Herramientas/tests/test_ht02_verificador_enlaces.py::TestEstados::test_contenido_igual_casi_y_cambiado`: SUPERADA
- `10_Herramientas/tests/test_ht02_verificador_enlaces.py::TestEstados::test_retractacion`: SUPERADA

### PB-26 · Clasificación temática y orden por calidad

Criterio de aprobación del plan: Comprobación automática del orden: 0 inversiones; 100 % con temática válida

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t126_pb26_pb48.py::test_pb26_cada_referencia_esta_en_una_tematica_del_anexo_d' 'tests/test_t126_pb26_pb48.py::test_pb26_dentro_de_cada_tematica_el_orden_es_por_calidad_descendente' 'tests/test_t126_pb26_pb48.py::test_pb26_el_nivel_es_coherente_con_la_calidad' 'tests/test_t126_pb26_pb48.py::test_pb26_una_fuente_de_nivel_d_esta_marcada_como_candidata_a_baja_o_unica' 'tests/test_t126_pb26_pb48.py::test_pb26_la_comprobacion_detecta_un_orden_o_un_nivel_mal_puestos' 'tests/test_t126_r02.py::test_h02_cada_referencia_esta_fisicamente_en_la_seccion_de_su_tematica' 'tests/test_t126_r02.py::test_h02_a_igualdad_de_q_va_primero_la_mas_reciente' 'tests/test_t126_r02.py::test_h03_las_comprobaciones_detectan_fichas_estropeadas')
```

- `11_Ejecutor/tests/test_t126_pb26_pb48.py::test_pb26_cada_referencia_esta_en_una_tematica_del_anexo_d`: SUPERADA
- `11_Ejecutor/tests/test_t126_pb26_pb48.py::test_pb26_dentro_de_cada_tematica_el_orden_es_por_calidad_descendente`: SUPERADA
- `11_Ejecutor/tests/test_t126_pb26_pb48.py::test_pb26_el_nivel_es_coherente_con_la_calidad`: SUPERADA
- `11_Ejecutor/tests/test_t126_pb26_pb48.py::test_pb26_una_fuente_de_nivel_d_esta_marcada_como_candidata_a_baja_o_unica`: SUPERADA
- `11_Ejecutor/tests/test_t126_pb26_pb48.py::test_pb26_la_comprobacion_detecta_un_orden_o_un_nivel_mal_puestos`: SUPERADA
- `11_Ejecutor/tests/test_t126_r02.py::test_h02_cada_referencia_esta_fisicamente_en_la_seccion_de_su_tematica`: SUPERADA
- `11_Ejecutor/tests/test_t126_r02.py::test_h02_a_igualdad_de_q_va_primero_la_mas_reciente`: SUPERADA
- `11_Ejecutor/tests/test_t126_r02.py::test_h03_las_comprobaciones_detectan_fichas_estropeadas`: SUPERADA

### PB-29 · Contar raíces, no menciones

Criterio de aprobación del plan: G3-DAT-09 coherente; el Auditor no encuentra doble cómputo

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t65_qa_r01.py::test_r01_h08_ps1_con_el_minimo_de_raices_de_la_configuracion')
```

- `11_Ejecutor/tests/test_t65_qa_r01.py::test_r01_h08_ps1_con_el_minimo_de_raices_de_la_configuracion`: SUPERADA

### PB-30 · Cifra sin artefacto bloqueada por G3

Criterio de aprobación del plan: Tiempo de dictamen ≤ 10 min; dos G3V- en HA; la cifra no aparece en la entrega o aparece con CALC-

```bash
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestBloqueos::test_evidencias_y_calculos')
```

- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_evidencias_y_calculos`: SUPERADA

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
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_certificado_emitido_con_muestra_suficiente' 'tests/test_unitarias.py::test_metricas_de_pronostico_con_pronosticadores_sinteticos' 'tests/test_t87_datos.py::test_r13_certificado_por_metodo_en_la_entrega' 'tests/test_fase4_huecos.py::test_pb32_se_certifica_la_celda_con_habilidad_y_no_la_que_no_la_tiene' 'tests/test_fase4_huecos.py::test_pb32_cada_condicion_del_certificado_cuenta_por_separado' 'tests/test_fase4_huecos.py::test_pb32_una_celda_habil_que_no_supera_holm_no_se_certifica_y_el_certificado_lleva_su_metodo' 'tests/test_fase4_huecos.py::test_pb32_el_criterio_exige_el_alfa_de_holm' 'tests/test_fase4_huecos.py::test_pb32_el_certificado_es_de_la_celda_por_metodo' 'tests/test_fase4_huecos.py::test_pb32_la_probabilidad_se_publica_solo_en_la_celda_certificada_y_con_su_certificado_ref' 'tests/test_t87_datos.py::test_certificados_separan_metodos' 'tests/test_t53_evaluacion_y_almacen.py::test_holm_escalonado_se_detiene_en_el_primer_fallo')
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

### PB-33 · Revocación de certificado por deterioro

Criterio de aprobación del plan: Estado del CERT- y fecha de efecto; G3-CON-10 bloquea probabilidades posteriores

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t66_evaluacion.py::test_pa10_revocar_y_retirar_siguen_siendo_automaticos' 'tests/test_t53_evaluacion_y_almacen.py::test_ece_cero_no_revoca_un_certificado' 'tests/test_t53_evaluacion_y_almacen.py::test_umbral_de_revocacion_ece_sale_de_la_configuracion' 'tests/test_fase4_huecos.py::test_pb33_la_revocacion_registra_estado_motivo_y_fecha_de_efecto' 'tests/test_fase4_huecos.py::test_pb33_tras_la_revocacion_hay_alerta_de_sobreconfianza_y_el_run_siguiente_no_publica_probabilidad')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestBloqueos::test_certificado_no_vigente')
```

- `11_Ejecutor/tests/test_t66_evaluacion.py::test_pa10_revocar_y_retirar_siguen_siendo_automaticos`: SUPERADA
- `11_Ejecutor/tests/test_t53_evaluacion_y_almacen.py::test_ece_cero_no_revoca_un_certificado`: SUPERADA
- `11_Ejecutor/tests/test_t53_evaluacion_y_almacen.py::test_umbral_de_revocacion_ece_sale_de_la_configuracion`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_certificado_no_vigente`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb33_la_revocacion_registra_estado_motivo_y_fecha_de_efecto`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb33_tras_la_revocacion_hay_alerta_de_sobreconfianza_y_el_run_siguiente_no_publica_probabilidad`: SUPERADA

### PB-34 · Fuga de información en evaluación detectada

Criterio de aprobación del plan: Ningún AJU- ni CERT- apoyado en métricas FALLIDA; corrección registrada en F6

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_pronosticos_resueltos_sin_look_ahead' 'tests/test_unitarias.py::test_guardia_de_fuga_del_proveedor' 'tests/test_unitarias.py::test_fecha_publicacion_filtra_revisiones' 'tests/test_unitarias.py::test_servicio_del_motor_rc_cache_fuga_y_reejecucion' 'tests/test_t66_evaluacion.py::test_pa09_contaminados_no_cuentan_para_la_recalibracion')
```

- `11_Ejecutor/tests/test_integracion.py::test_pronosticos_resueltos_sin_look_ahead`: SUPERADA
- `11_Ejecutor/tests/test_unitarias.py::test_guardia_de_fuga_del_proveedor`: SUPERADA
- `11_Ejecutor/tests/test_unitarias.py::test_fecha_publicacion_filtra_revisiones`: SUPERADA
- `11_Ejecutor/tests/test_unitarias.py::test_servicio_del_motor_rc_cache_fuga_y_reejecucion`: SUPERADA
- `11_Ejecutor/tests/test_t66_evaluacion.py::test_pa09_contaminados_no_cuentan_para_la_recalibracion`: SUPERADA

### PB-35 · Recalibración dentro de bandas con evaluación sombra

Criterio de aprobación del plan: Bandas respetadas; sombra registrada; decisión documentada con DM-HLN

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t66_evaluacion.py::test_pa10_recalibracion_siempre_propuesta' 'tests/test_t65_qa_r01.py::test_r01_h08_recalibracion_de_rk_con_el_paso_y_las_bandas_de_la_configuracion')
```

- `11_Ejecutor/tests/test_t66_evaluacion.py::test_pa10_recalibracion_siempre_propuesta`: SUPERADA
- `11_Ejecutor/tests/test_t65_qa_r01.py::test_r01_h08_recalibracion_de_rk_con_el_paso_y_las_bandas_de_la_configuracion`: SUPERADA

### PB-36 · Recalibración fuera de bandas rechazada

Criterio de aprobación del plan: F10 intacto en P-09 y P-05; P3- en la cola de HA

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t65_qa_r01.py::test_r01_h08_recalibracion_de_rk_con_el_paso_y_las_bandas_de_la_configuracion')
```

- `11_Ejecutor/tests/test_t65_qa_r01.py::test_r01_h08_recalibracion_de_rk_con_el_paso_y_las_bandas_de_la_configuracion`: SUPERADA

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
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_autocritica.py::test_objecion_fuerte_sin_resolver_excluye_del_top3')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestBloqueos::test_objecion_fuerte_sin_resolver' 'tests/test_ht09_validador_g3.py::TestBloqueos::test_objecion_fuerte_respondida_pero_no_resuelta')
```

- `11_Ejecutor/tests/test_autocritica.py::test_objecion_fuerte_sin_resolver_excluye_del_top3`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_objecion_fuerte_sin_resolver`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_objecion_fuerte_respondida_pero_no_resuelta`: SUPERADA

### PB-39 · Informe visual con legibilidad < 70 bloqueado

Criterio de aprobación del plan: Ningún informe visual entregado con índice < 70

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_ciclo_semanal_completo_apto')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht07_legibilidad.py::TestIndice::test_texto_dificil_no_cumple' 'tests/test_ht09_validador_g3.py::TestBloqueos::test_legibilidad')
```

- `11_Ejecutor/tests/test_integracion.py::test_ciclo_semanal_completo_apto`: SUPERADA
- `10_Herramientas/tests/test_ht07_legibilidad.py::TestIndice::test_texto_dificil_no_cumple`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_legibilidad`: SUPERADA

### PB-41 · Coherencia entre entregables y entre clases

Criterio de aprobación del plan: G3-ENT-07 PASA; el Auditor no recuenta menos apuestas que las declaradas

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_ciclo_semanal_completo_apto' 'tests/test_t53_seleccion_y_entrega.py::test_entregable_bloqueado_no_llega_a_las_carpetas_de_entrega' 'tests/test_fase4_huecos.py::test_pb01_sin_g3_apto_no_se_congela_ningun_pronostico_ni_se_entrega')
```

- `11_Ejecutor/tests/test_integracion.py::test_ciclo_semanal_completo_apto`: SUPERADA
- `11_Ejecutor/tests/test_t53_seleccion_y_entrega.py::test_entregable_bloqueado_no_llega_a_las_carpetas_de_entrega`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb01_sin_g3_apto_no_se_congela_ningun_pronostico_ni_se_entrega`: SUPERADA

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
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_integracion.py::test_pronosticos_resueltos_sin_look_ahead' 'tests/test_t66_evaluacion.py::test_pa09_contaminados_se_registran_pero_no_cuentan_en_metricas_ni_historial' 'tests/test_t53_evaluacion_y_almacen.py::test_hitos_h5_no_cuentan_en_h4_ni_en_el_historial')
```

- `11_Ejecutor/tests/test_integracion.py::test_pronosticos_resueltos_sin_look_ahead`: SUPERADA
- `11_Ejecutor/tests/test_t66_evaluacion.py::test_pa09_contaminados_se_registran_pero_no_cuentan_en_metricas_ni_historial`: SUPERADA
- `11_Ejecutor/tests/test_t53_evaluacion_y_almacen.py::test_hitos_h5_no_cuentan_en_h4_ni_en_el_historial`: SUPERADA

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
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_servicio_del_motor_rc_cache_fuga_y_reejecucion' 'tests/test_t65_resto_t53.py::test_cs08_fichas_documentadas_no_entregan_cifras')
```

- `11_Ejecutor/tests/test_unitarias.py::test_servicio_del_motor_rc_cache_fuga_y_reejecucion`: SUPERADA
- `11_Ejecutor/tests/test_t65_resto_t53.py::test_cs08_fichas_documentadas_no_entregan_cifras`: SUPERADA

### PB-48 · Conflicto de normas: la más restrictiva

Criterio de aprobación del plan: Segunda pasada registrada; COR- y P3- en HA

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_t126_pb26_pb48.py::test_pb48_una_guia_que_relaja_un_control_no_llega_a_la_elegibilidad' 'tests/test_t126_pb26_pb48.py::test_pb48_ht03_exige_la_segunda_pasada_en_banda_marginal' 'tests/test_t126_r02.py::test_h01_en_el_ciclo_una_opcion_en_banda_marginal_se_resuelve_con_su_segunda_pasada' 'tests/test_t126_r02.py::test_h01_sin_la_segunda_pasada_esas_opciones_no_serian_elegibles' 'tests/test_t126_r02.py::test_h04_la_leccion_que_relaja_el_control_llega_al_analista_en_su_ct06')
```

- `11_Ejecutor/tests/test_t126_pb26_pb48.py::test_pb48_una_guia_que_relaja_un_control_no_llega_a_la_elegibilidad`: SUPERADA
- `11_Ejecutor/tests/test_t126_pb26_pb48.py::test_pb48_ht03_exige_la_segunda_pasada_en_banda_marginal`: SUPERADA
- `11_Ejecutor/tests/test_t126_r02.py::test_h01_en_el_ciclo_una_opcion_en_banda_marginal_se_resuelve_con_su_segunda_pasada`: SUPERADA
- `11_Ejecutor/tests/test_t126_r02.py::test_h01_sin_la_segunda_pasada_esas_opciones_no_serian_elegibles`: SUPERADA
- `11_Ejecutor/tests/test_t126_r02.py::test_h04_la_leccion_que_relaja_el_control_llega_al_analista_en_su_ct06`: SUPERADA

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
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v5.py::test_doce_tipos_agentes_y_canales')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestBloqueos::test_horizonte_no_aplicable' 'tests/test_ht09_validador_g3.py::TestV5::test_doce_tipos_y_tabla_8_3')
```

- `11_Ejecutor/tests/test_v5.py::test_doce_tipos_agentes_y_canales`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestBloqueos::test_horizonte_no_aplicable`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV5::test_doce_tipos_y_tabla_8_3`: SUPERADA

### PB-52 · Modo degradado: herramienta caída

Criterio de aprobación del plan: Entrega con limitaciones declaradas o bloqueo justificado; ninguna cifra sin dato

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_unitarias.py::test_busqueda_web_solo_en_vivo_y_reparacion_json' 'tests/test_t53_seleccion_y_entrega.py::test_un_simbolo_sin_historia_no_vacia_su_tipo' 'tests/test_t65_hallazgos.py::test_h15_simbolo_con_datos_invalidos_se_excluye_y_se_declara')
```

- `11_Ejecutor/tests/test_unitarias.py::test_busqueda_web_solo_en_vivo_y_reparacion_json`: SUPERADA
- `11_Ejecutor/tests/test_t53_seleccion_y_entrega.py::test_un_simbolo_sin_historia_no_vacia_su_tipo`: SUPERADA
- `11_Ejecutor/tests/test_t65_hallazgos.py::test_h15_simbolo_con_datos_invalidos_se_excluye_y_se_declara`: SUPERADA

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
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v51.py::test_credenciales_boveda' 'tests/test_v51.py::test_cli_v51' 'tests/test_fase4_huecos.py::test_pb58_el_servicio_pendiente_se_declara_hasta_la_provision_y_el_valor_no_llega_a_ningun_contexto')
```

- `11_Ejecutor/tests/test_v51.py::test_credenciales_boveda`: SUPERADA
- `11_Ejecutor/tests/test_v51.py::test_cli_v51`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb58_el_servicio_pendiente_se_declara_hasta_la_provision_y_el_valor_no_llega_a_ningun_contexto`: SUPERADA

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
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v51.py::test_consulta_bloqueante_pausa_y_vencimiento' 'tests/test_fase4_huecos.py::test_pb61_solo_cri_se_pausa_y_al_vencer_el_supuesto_figura_en_los_entregables')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestV51::test_supuestos_declarados')
```

- `11_Ejecutor/tests/test_v51.py::test_consulta_bloqueante_pausa_y_vencimiento`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV51::test_supuestos_declarados`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb61_solo_cri_se_pausa_y_al_vencer_el_supuesto_figura_en_los_entregables`: SUPERADA

### PB-62 · Filtro, agrupación y recurrencia de consultas

Criterio de aprobación del plan: ≤ 3 mensajes CT-23 por RUN-; LEC- de producto creada

```bash
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v51.py::test_consulta_validaciones_agrupacion_y_entrante')
```

- `11_Ejecutor/tests/test_v51.py::test_consulta_validaciones_agrupacion_y_entrante`: SUPERADA

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
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q 'tests/test_v51.py::test_estado_h5_por_hitos' 'tests/test_t53_evaluacion_y_almacen.py::test_degradacion_h5_se_aplica_en_f6_y_f10' 'tests/test_t53_seleccion_y_entrega.py::test_h05_degradacion_h5_cambia_la_tabla_del_ciclo_siguiente' 'tests/test_t65_hallazgos.py::test_h13_la_degradacion_registra_el_efecto_desde_el_mismo_ciclo' 'tests/test_fase4_huecos.py::test_pb64_la_revision_de_certificados_no_emite_ninguno_para_h5' 'tests/test_fase4_huecos.py::test_pb64_los_tres_estados_h5_por_hitos_y_mp_baja_de_si_a_limitado_en_f6_y_f10')
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestV51::test_h5_certificado_no_habilita_probabilidad')
```

- `11_Ejecutor/tests/test_v51.py::test_estado_h5_por_hitos`: SUPERADA
- `11_Ejecutor/tests/test_t53_evaluacion_y_almacen.py::test_degradacion_h5_se_aplica_en_f6_y_f10`: SUPERADA
- `11_Ejecutor/tests/test_t53_seleccion_y_entrega.py::test_h05_degradacion_h5_cambia_la_tabla_del_ciclo_siguiente`: SUPERADA
- `11_Ejecutor/tests/test_t65_hallazgos.py::test_h13_la_degradacion_registra_el_efecto_desde_el_mismo_ciclo`: SUPERADA
- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV51::test_h5_certificado_no_habilita_probabilidad`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb64_la_revision_de_certificados_no_emite_ninguno_para_h5`: SUPERADA
- `11_Ejecutor/tests/test_fase4_huecos.py::test_pb64_los_tres_estados_h5_por_hitos_y_mp_baja_de_si_a_limitado_en_f6_y_f10`: SUPERADA

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
(cd bloque_a/10_Herramientas && ../../.venv/bin/python -m pytest -q 'tests/test_ht09_validador_g3.py::TestV51::test_seguimiento_envio_a_b')
```

- `10_Herramientas/tests/test_ht09_validador_g3.py::TestV51::test_seguimiento_envio_a_b`: SUPERADA
