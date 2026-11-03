# Objetivos del Bloque A Forex — Buscador de Oportunidades de Inversión en Divisas

**Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026 · actualizado V1.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque A Forex, versión óptima V1.1 (ante discrepancia, manda el Documento 0). Actualización V1.1: dimensión D12 (OBJ-97 a OBJ-106) sobre comunicación con el Broker, credenciales, horizonte principal y H5, y seguimiento encargado de opciones.

Este documento fija **qué debe conseguir** el Bloque A Forex y **cómo se mide**. Cada objetivo tiene un indicador, una meta inicial, el responsable de medirlo y el requisito del propietario que cubre. Las metas son valores de arranque: el Evaluador y el operador las revisan trimestralmente con la evidencia acumulada (Documento 0, 18.2). Los objetivos OBJ-01 a OBJ-72 conservan la numeración del Bloque A general para facilitar el mantenimiento conjunto, con su contenido adaptado a divisas; OBJ-73 a OBJ-96 son propios del mercado de divisas.

**Requisitos del propietario (RQ):** RQ-0 funcionamiento descrito (periodicidad configurable, peticiones y consultas sin límite, dos informes, top-3 por segmento, el Broker decide) · RQ-1 estrategias por segmento de divisas · RQ-2 automejora · RQ-3 sin cuellos de botella · RQ-4 eficiencia · RQ-5 autocrítica · RQ-6 historial interno · RQ-7 conocimiento verificado continuo · RQ-8 Fondo metodológico · RQ-9 verificación y borrado de referencias · RQ-10 referencias por temática y calidad · RQ-11 horizontes · RQ-12 conocimiento experto en los prompts · RQ-13 especialización exclusiva en divisas (segmentos, capas transversales, notación, carry, convertibilidad, exposición agregada y humildad frente al paseo aleatorio).

---

## 1. Misión resumida

Encontrar pocas oportunidades cambiarias buenas —un par, un cruce, una cesta, un bloque, una estrategia o un cambio de régimen; por qué existen y en qué horizonte— en los seis segmentos del universo de divisas (G10N, G10M, EMAS, EMLA, EMEA y ESTR), y entregar al Bloque B (vía Broker) un encargo claro para que elija instrumento, coste y cobertura; explicarlas con claridad al Broker y al usuario, decir con honestidad cuánto se sabe y cuánto no en un mercado donde batir al paseo aleatorio es difícil (Meese y Rogoff, 1983), gastar solo lo que aporta valor y aprender de cada acierto y error.

---

## 2. Objetivos por dimensión

### D1 · Servicio al Broker Personal (RQ-0)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-01 | Entregar el informe periódico a tiempo | % de ciclos entregados en la fecha y hora configuradas (por defecto, lunes 07:00 en la zona del usuario, tras la ejecución del sábado posterior al cierre de Nueva York) | ≥ 98 % | Coordinador |
| OBJ-02 | Respetar la configuración elegida por el usuario | Cambios de servicio (CT-04: periodicidad, segmentos activos, divisa base, horizontes, idioma) aplicados en el ciclo siguiente | 100 % | Coordinador |
| OBJ-03 | Atender toda petición sin rechazarla por número | Peticiones descartadas sin motivo | 0 | Orquestador |
| OBJ-04 | Responder rápido las consultas sencillas | Mediana de tiempo de respuesta N0 | < 2 min | Coordinador |
| OBJ-05 | Resolver las consultas sin escalado innecesario | % de consultas resueltas en N0 cuando la información existía en F1–F6, RC o los informes (incluidos los informes transversales archivados en F5) | ≥ 85 % | Auditor (muestra) |
| OBJ-06 | Proponer hasta 3 opciones por segmento de divisas (seis) sin relleno | Opciones del top-3 que incumplen la elegibilidad de 9.2 | 0 | HT-09 / Auditor |
| OBJ-07 | Explicar siempre por qué hay menos de 3 | Segmentos con menos de 3 opciones sin `menos_de_tres_motivo` | 0 | HT-09 |
| OBJ-08 | Dar al Broker lo necesario para decidir según su modo | Opciones con `relevancia_decisional`, `reversibilidad` y `siguiente_paso_sugerido` | 100 % | HT-09 |
| OBJ-09 | Facilitar el paso al Bloque B | Opciones `ENVIAR_A_BLOQUE_B` con `paquete_para_bloque_B` completo (par o composición, dirección, divisa de financiación, carry esperado, consideraciones de implementación, métricas clave y preguntas) | 100 % | HT-09 |
| OBJ-10 | Utilidad percibida por el Broker | Media de la valoración de utilidad (CT-04) | ≥ 4/5 | Evaluador |
| OBJ-11 | No asesorar al usuario | Comunicaciones del bloque fuera del canal Coordinador→Broker (incluidas las dirigidas al Bloque B o al Bloque A general) | 0 | Orquestador |

### D2 · Informe para el usuario inexperto (RQ-0)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-12 | Legibilidad | Índice Fernández-Huerta corregido (Law, 2011) del informe visual | ≥ 70 | HT-07 |
| OBJ-13 | Brevedad | Frases de más de 20 palabras en el informe visual | ≤ 5 % | HT-07 |
| OBJ-14 | Visual | Informe con los siete elementos de 14.2: «la semana en 30 segundos», mapa de divisas (verde gana valor, rojo pierde), termómetro del euro, semáforo de los seis segmentos, tarjetas con banderas o icono de cesta, riesgo 1–5, horizonte y confianza, «cómo nos fue» y mini-glosario | 100 % | HT-09 |
| OBJ-15 | Sin jerga sin explicar | Términos de la lista de jerga de HT-07 (carry, forward, NDF, *risk reversal*, PPA, tipo fijo, intervención…) sin explicación en su primera aparición | 0 | HT-07 |
| OBJ-16 | Accesible | Gráficos con texto alternativo y paleta apta para daltonismo | 100 % | Auditor |
| OBJ-17 | Coherencia entre informes | Discrepancias de OPP-, orden, dirección o cifras entre informe técnico, visual y JSON | 0 | HT-09 |
| OBJ-73 | Dirección comprensible | Tarjetas que dicen explícitamente qué divisa se espera que gane valor y cuál que lo pierda (nunca solo «el par sube» o «USD/JPY baja») | 100 % | HT-09 / Auditor |

### D3 · Estrategias por segmento y calidad analítica (RQ-1, RQ-11, RQ-13)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-18 | Cada segmento con su estrategia | Informes de segmento que aplican al menos tres indicadores de su fila de 8.2 y las seis lentes cambiarias de 8.1 | 100 % | Auditor |
| OBJ-19 | Cobertura de los seis segmentos | Segmentos activos analizados en cada ciclo (al menos arrastre verificado) | 100 % | Coordinador |
| OBJ-20 | Separar tendencia de oportunidad | Opciones con valoración explícita de lo que ya descuentan el forward, la curva de tipos y el posicionamiento | 100 % | HT-09 / Auditor |
| OBJ-21 | Trazabilidad | Afirmaciones centrales con CLM→EVD; cifras con fuente, fecha y fijación de HT-01, o CALC- | 100 % | HT-09 |
| OBJ-22 | Corroboración | Afirmaciones centrales con ≥ 2 raíces independientes A/B o 1 primaria A (p. ej., el comunicado del banco central) | 100 % | Curador / HT-09 |
| OBJ-23 | Horizontes coherentes | Horizontes ofrecidos fuera de la matriz 8.3 vigente en F10, o «limitados» sin liquidez ni catalizador declarados | 0 | HT-09 |
| OBJ-24 | Honestidad predictiva | Probabilidades numéricas sin certificado del Evaluador para la celda segmento × horizonte × método | 0 | HT-09 |
| OBJ-25 | Pronósticos verificables | Pronósticos del top-3 congelados en F4 con criterio, fijación y fecha de resolución, y tipo de rentabilidad declarado (contado o total) | 100 % | Evaluador |
| OBJ-26 | Diversificación honesta | Informes que declaran el número de apuestas efectivamente independientes, considerando los factores comunes (dólar, yen y refugio, carry y riesgo global, materias primas) | 100 % | HT-09 |
| OBJ-74 | Usar las capas transversales | Informes de segmento en N2/N3 que citan los informes CT-06T del ciclo (AG-09 y AG-21) y no rehacen su análisis | 100 % | Auditor |
| OBJ-75 | Capas transversales a tiempo | Ciclos en los que los informes de AG-09 y AG-21 están disponibles antes del inicio de F1 (o, en N1 sin cambio material, se reconfirman los anteriores) | ≥ 95 % | Orquestador |
| OBJ-76 | Transversales sin opciones | Opciones propuestas directamente por AG-09 o AG-21 (que solo aportan señales y contexto) | 0 | Auditor |

### D3 bis · Función única y frontera con el Bloque B (RQ-0, RQ-13)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-68 | No seleccionar instrumentos | Opciones del top-3 que proponen un instrumento (contado, forward, futuro, opción, ETF/ETC, CFD), un proveedor, un coste, un apalancamiento, un tamaño o un nivel de entrada (R21) | 0 | HT-09 / Auditor |
| OBJ-69 | Ámbitos bien delimitados | Opciones con `tipo_opcion`, par o composición, dirección, divisa de financiación, `ambito` (incluye/excluye), `indicador_seguimiento` y `convertibilidad` | 100 % | HT-09 |
| OBJ-70 | Encargo útil para el Bloque B | Opciones con `consideraciones_implementacion`, `metricas_clave`, `preguntas_para_B` y `carry_esperado` no vacíos | 100 % | HT-09 |
| OBJ-71 | Sin duplicados entre segmentos | Oportunidades presentes en dos top-3 de segmentos distintos | 0 | HT-09 |
| OBJ-72 | Utilidad para el Bloque B | Oportunidades enviadas por el Broker al Bloque B que este no pudo analizar por falta de delimitación (cuando se comunique) | 0 | Evaluador (CT-22) |
| OBJ-77 | Segmento bien asignado | Opciones cuyo segmento no sigue las reglas de 2.6 (divisa menos líquida; tres o más divisas o regla sistemática → ESTR; volatilidad de un par → segmento del par) o sin motivo registrado | 0 | HT-09 / Auditor |
| OBJ-78 | Notación correcta | Opciones con par fuera de la convención de mercado BASE/COTIZADA, dirección no referida a la base o incoherente con la composición y el nombre llano | 0 | HT-09 |
| OBJ-79 | Niveles solo como invalidación | Niveles del par presentados como nivel de entrada, objetivo de precio u orden | 0 | HT-09 / Auditor |

### D4 · Rendimiento predictivo (RQ-2, RQ-11, RQ-13)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-27 | Batir al paseo aleatorio | Brier skill score o error relativo frente al paseo aleatorio (sin cambio), por segmento × horizonte (≥ 30 resueltos), con prueba de Diebold-Mariano (corrección HLN) | > 0 en ≥ 40 % de las celdas el primer año; ≥ 55 % el segundo | Evaluador |
| OBJ-28 | Valor de las opciones | Rentabilidad total relativa media del top-3 frente a la referencia de su segmento (8.4: rentabilidad en exceso nula en G10N y G10M; cesta equiponderada con carry en EMAS, EMLA y EMEA; índice de la estrategia o rentabilidad nula en ESTR), por horizonte | > 0, con IC 90 % declarado | Evaluador |
| OBJ-29 | Calibración | Calibración no rechazada en las celdas certificadas (Anexo A, nota 1); ECE agregado con ≥ 200 pronósticos | < 0,10 | Evaluador |
| OBJ-30 | Detectar invalidaciones a tiempo | % de opciones cerradas por invalidación antes de una pérdida severa (> 2 desviaciones típicas del horizonte) | ≥ 80 % | Evaluador |
| OBJ-31 | Publicar el historial | Informes periódicos con «cómo nos fue» por segmento y horizonte, frente al paseo aleatorio y con tamaño muestral | 100 % | HT-09 |
| OBJ-80 | Contrastar con el forward | Celdas con pronósticos de rentabilidad total evaluadas también frente al forward como predictor (Clark-West cuando los modelos están anidados) | 100 % evaluadas; skill > 0 en ≥ 50 % de ellas el segundo año | Evaluador |
| OBJ-81 | Riesgo de cola del carry bien medido | Frecuencia con que la pérdida de las opciones con carry a favor supera el escenario adverso del Motor, frente a su frecuencia nominal | ≤ nominal + 5 pp | Evaluador |

### D5 · Automejora (RQ-2)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-32 | Resolver todos los pronósticos vencidos | % de PRG-FX- resueltos en ≤ 2 días hábiles tras su fecha, con la fijación pactada | ≥ 98 % | Evaluador |
| OBJ-33 | Convertir resultados en lecciones | Lecciones LEC- nuevas o actualizadas por mes | ≥ 4 | Evaluador |
| OBJ-34 | Lecciones que se aplican | Encargos que cargan las lecciones vigentes de su ámbito (segmento, divisa, horizonte, agente) | 100 % | Auditor (muestra) |
| OBJ-35 | Recalibrar con disciplina | Ajustes automáticos fuera de bandas o sin muestra suficiente | 0 | Orquestador |
| OBJ-36 | Mejorar con el tiempo | Tendencia trimestral del Brier skill score agregado frente al paseo aleatorio | No negativa | Evaluador |
| OBJ-37 | Aprender del uso | Preguntas repetidas convertidas en mejoras del informe por defecto | 100 % de las detectadas | Evaluador |

### D6 · Eficiencia y fluidez (RQ-3, RQ-4)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-38 | Respetar el presupuesto | Consumo del ciclo semanal completo (seis segmentos y dos informes transversales) | ≤ 140 UC; desviación ≤ +10 % | Orquestador |
| OBJ-39 | No gastar en lo que no cambia | Segmentos con GC0 negativo resueltos en N1 (arrastre verificado) | 100 % | Orquestador |
| OBJ-40 | Embudo efectivo | Proporción candidatas GC1 / finalistas GC3 / top-3 registrada por segmento | Registrada en el 100 % de los ciclos | Coordinador |
| OBJ-41 | Reutilizar | % de cálculos servidos desde caché cuando eran idénticos | 100 % | Motor |
| OBJ-42 | Sin cuellos de botella | Tiempo en cola de cualquier agente por encima de 2× su objetivo | < 5 % de los encargos | Orquestador |
| OBJ-43 | Escalado a tiempo | Colas saturadas sin instancia adicional abierta | 0 | Orquestador |
| OBJ-44 | G3 sin esperas | Mediana del tiempo de validación G3 | < 5 min | Orquestador |
| OBJ-82 | Capas transversales sin duplicación | Búsquedas o cálculos de un Analista de segmento que repiten lo ya servido en el CT-06T del ciclo (AS-02); consumo de cada informe transversal | 0 casos; ≤ 6 UC por informe | Orquestador |

### D7 · Autocrítica y control (RQ-5)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-45 | Refutar toda finalista N2/N3 | Finalistas sin paquete CT-13 | 0 | HT-09 |
| OBJ-46 | Responder a las objeciones | Objeciones fuertes sin resolver en el top-3 | 0 | HT-09 |
| OBJ-47 | Pre-mortem | Candidatas GC2 con pre-mortem | 100 % | Auditor |
| OBJ-48 | Declarar lo que no se sabe | Opciones con condiciones de invalidación y riesgos explícitos | 100 % | HT-09 |
| OBJ-49 | Detectar sobreconfianza | Revisión mensual de confianza declarada frente a calibración | 12 al año | Evaluador |
| OBJ-50 | Auditoría útil | Hallazgos materiales convertidos en guía o propuesta en ≤ 1 ciclo | ≥ 90 % | Orquestador |
| OBJ-83 | Refutación cambiaria completa | Paquetes CT-13 que examinan lo que ya descuentan el forward y el posicionamiento, el riesgo de intervención y la fragilidad del carry | 100 % | Auditor |

### D8 · Historial y memoria (RQ-6)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-51 | Historial completo | RUN-FX-, QRY- y decisiones del Broker registrados en F5 | 100 % | Orquestador |
| OBJ-52 | Integridad | Reescrituras de historial (fuera de las bajas de referencias) | 0 | Orquestador |
| OBJ-53 | Continuidad | Informes con «cambios frente al ciclo anterior» | 100 % | HT-09 |
| OBJ-84 | Capas transversales archivadas | RUN- con los informes CT-06T del ciclo (o su ausencia motivada) archivados en F5 | 100 % | Orquestador |

### D9 · Conocimiento y referencias (RQ-7, RQ-8, RQ-9, RQ-10, RQ-12)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-54 | Alimentación continua | Altas verificadas al mes en F7 (TX-), F8 (TMX-) y F9 (TFX-) | ≥ 8, ≥ 4 y ≥ 10 | Orquestador (CT-21) |
| OBJ-55 | Fondo metodológico aplicado | Estrategias de búsqueda que citan los criterios del Fondo | 100 % | Auditor |
| OBJ-56 | Enlaces sanos | % de referencias en estado OK tras el barrido semanal | ≥ 95 % | HT-02 |
| OBJ-57 | Reacción a enlaces rotos | Referencias rotas sin acción tras dos barridos | 0 | HT-02 / Orquestador |
| OBJ-58 | Bajas trazables | Borrados sin línea en el Registro de bajas | 0 | Orquestador |
| OBJ-59 | Orden por temática y calidad | Referencias sin área TX-/TMX-/TFX-, Q o nivel; secciones mal ordenadas | 0 | Script de verificación |
| OBJ-60 | Cobertura | Áreas del Anexo D con < 3 referencias de nivel A/B | Reducción trimestral | Documentadores / BFA |
| OBJ-61 | Veracidad | Revisión trimestral de retractaciones y refutaciones completada | 4 al año | Documentadores / BFA |
| OBJ-62 | Fiabilidad medida de fuentes de opinión | Fuentes de F9 con previsiones explícitas de pares (bancos, gestoras, casas de análisis, encuestas de previsiones) con historial de exactitud medido por el Evaluador frente al paseo aleatorio | Creciente; ≥ 50 % al año | Evaluador / BFA |
| OBJ-63 | Conocimiento experto en los prompts | Prompts con sección 10 «Base de conocimientos» específica de divisas, completa y revisada en la revisión trimestral | 100 % | Operador |
| OBJ-85 | Calendario cambiario al día | Calendario de reuniones de bancos centrales (TFX-01, TFX-02), datos clave, elecciones y festivos de liquidación (TFX-09) del trimestre siguiente verificado antes de su inicio | 100 % | BFA |

### D10 · Seguridad y gobernanza (transversal)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-64 | Sin credenciales ni datos personales en mensajes | Incidencias | 0 | Orquestador |
| OBJ-65 | Inmunidad a contenido externo | Instrucciones incrustadas ejecutadas | 0 | Auditor |
| OBJ-66 | Cambios gobernados | Cambios de tipo 3 aplicados sin aprobación | 0 | Orquestador |
| OBJ-67 | Estados de madurez honestos | Componentes presentados como validados sin pruebas | 0 | Auditor |
| OBJ-86 | Independencia del Bloque A general | Mensajes intercambiados con el Bloque A general | 0 | Orquestador |
| OBJ-87 | Identificadores sin colisión | RUN-, OPP-, TND- o PRG- emitidos sin el prefijo FX; `methodology_version` o `version_contrato` sin la forma «FX-x.y» | 0 | HT-09 |
| OBJ-88 | Respeto de las sanciones | Opciones que implican una exposición prohibida por sanciones vigentes de la UE, EE. UU. o la ONU (PS7) | 0 | HT-09 / Auditor |

### D11 · Especialización cambiaria (RQ-1, RQ-13)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-89 | Exposición agregada visible | Informes técnicos y paquetes JSON con `exposicion_agregada` por divisa del conjunto de opciones (signo y magnitud cualitativa) | 100 % | HT-09 |
| OBJ-90 | Contradicciones resueltas | Divisas con signo opuesto en dos segmentos (p. ej., USD alcista en G10N y bajista en EMLA) sin mecanismo distinto justificado ni resolución | 0 | HT-09 / Auditor |
| OBJ-91 | Diversidad por divisa | Segmentos con una misma divisa en la misma dirección en más de dos opciones | 0 | HT-09 |
| OBJ-92 | Convertibilidad documentada | Opciones del top-3 con PS3 completa (convertibilidad, NDF, controles de capitales, repatriación, profundidad y exposición alternativa accesible); opciones con tipo fijo con riesgo de ruptura o con controles que tienen riesgo ≥ 4 y relevancia ALTA | 100 % | HT-09 |
| OBJ-93 | Carry explícito | Opciones con carry anual, signo respecto de la tesis y carry ajustado por volatilidad, calculados por el Motor | 100 % | HT-09 |
| OBJ-94 | Regímenes bien caracterizados | Opciones `REGIMEN` con clasificación de facto (Ilzetzki, Reinhart y Rogoff), indicadores de sostenibilidad (reservas frente a necesidades, puntos forward implícitos, diferencial onshore–offshore) y escenario de salto simulado (MC-05) | 100 % | Auditor |
| OBJ-95 | Sin anticipación en fijaciones | PRG o métricas con nivel de referencia o datos no conocibles en la fecha de congelación (fijación posterior, COT publicado después, dato revisado) | 0 | Evaluador (`comprobacion_fuga`) |
| OBJ-96 | Cribado cuantitativo del universo | Divisas de cada segmento activo con señales de las seis lentes cambiarias calculadas en el cribado (PLAN_MIN), incluida la rotación exploratoria | ≥ 95 % del universo de 2.6 | Orquestador |

---

### D12 · Comunicación con el Broker, horizontes y seguimiento encargado (V1.1; RQ-0, RQ-11, RQ-14 a RQ-16)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-97 | Preguntar antes que suponer, sin abrumar | Consultas CT-23 por RUN-FX- (máximo del Anexo A: 3 mensajes) y % de consultas que el bloque podía resolver con sus archivos | ≤ 3 por RUN; < 10 % evitables | Orquestador / Auditor |
| OBJ-98 | Supuestos visibles | Conclusiones que dependen de una consulta sin respuesta y llevan `supuestos_declarados` (supuesto, CNS-FX- y efecto si fuera falso) | 100 % | HT-09 (C19) |
| OBJ-99 | Bloquear solo lo afectado | Consultas BLOQUEANTE que paralizan más de la parte afectada o retrasan la entrega periódica | 0 | Orquestador |
| OBJ-100 | Aprender de las consultas | Consultas recurrentes (3 en 8 semanas) convertidas en lección de normalización de las peticiones | 100 % | Evaluador |
| OBJ-101 | Credenciales seguras | Valores de credenciales en mensajes, archivos, entregables o contextos de agentes; credenciales pedidas fuera del CT-25 | 0 | HT-09 (C13) / Auditor |
| OBJ-102 | Degradación declarada | Servicios con credencial ausente o denegada que se declaran en `limitaciones` y usan alternativas de calidad declarada (nunca acceso simulado) | 100 % | Auditor |
| OBJ-103 | Horizonte adecuado a la inversión | Opciones con `naturaleza_inversion` y `horizonte_principal` coherentes (8.3) o con justificación aceptada por el Orquestador | 100 % | HT-09 (C17) |
| OBJ-104 | H5 honesto | Pronósticos H5 fuera de los tres ámbitos, con probabilidad numérica o sin ≥ 3 hitos HIT-FX- | 0 | HT-09 (C18) |
| OBJ-105 | H5 evaluable | Hitos H5 vencidos resueltos en su fecha (sin fuga) y estado del PRG publicado en F6 | 100 % | Evaluador |
| OBJ-106 | Seguimiento encargado fiable | Ciclos C6 entregados en su fecha (sin retrasar C1–C3), cancelaciones aplicadas de inmediato, informes ≤ 300 palabras con HT-09 superado; recomendaciones `PROPONER_ENVIO_A_B` con elegibilidad 9.2 | ≥ 95 % a tiempo; 100 % del resto | Coordinador / HT-09 / Auditor |

## 3. Correspondencia requisito → objetivos

| Requisito | Objetivos |
|---|---|
| RQ-0 Funcionamiento descrito | OBJ-01 a OBJ-17, OBJ-68 a OBJ-73, OBJ-77 a OBJ-79 |
| RQ-1 Estrategias por segmento | OBJ-18 a OBJ-20, OBJ-74 a OBJ-76, OBJ-89 a OBJ-96 |
| RQ-2 Automejora | OBJ-27 a OBJ-37, OBJ-80, OBJ-81 |
| RQ-3 Sin cuellos de botella | OBJ-42 a OBJ-44, OBJ-75 |
| RQ-4 Eficiencia | OBJ-38 a OBJ-41, OBJ-82 |
| RQ-5 Autocrítica | OBJ-45 a OBJ-50, OBJ-83 |
| RQ-6 Historial | OBJ-51 a OBJ-53, OBJ-84 |
| RQ-7 Conocimiento continuo | OBJ-54, OBJ-62, OBJ-85 |
| RQ-8 Fondo metodológico | OBJ-55 |
| RQ-9 Verificación y borrado | OBJ-56 a OBJ-58, OBJ-61 |
| RQ-10 Temática y calidad | OBJ-59, OBJ-60 |
| RQ-11 Horizontes | OBJ-23 a OBJ-25, OBJ-27 a OBJ-29, OBJ-80, OBJ-103 a OBJ-105 |
| RQ-12 Conocimiento en prompts | OBJ-63 |
| RQ-13 Especialización en divisas | OBJ-68 a OBJ-71, OBJ-73 a OBJ-81, OBJ-83, OBJ-86 a OBJ-96 |
| RQ-14 Comunicación fluida con el Broker (V1.1) | OBJ-97 a OBJ-100 |
| RQ-15 Credenciales por CT-25 y bóveda (V1.1) | OBJ-101, OBJ-102 |
| RQ-16 Horizonte principal, H5 y seguimiento encargado (V1.1) | OBJ-103 a OBJ-106 |

## 4. Revisión

Trimestral, en la revisión programada (Documento 0, 18.2). Los objetivos de rendimiento predictivo (D4) solo se evalúan en celdas segmento × horizonte con muestra suficiente (Anexo A: 30 resueltos para medir y recalibrar; 100 para certificar); antes se informa del progreso de la muestra. Las metas de D4 son deliberadamente prudentes: en divisas, la referencia ingenua (paseo aleatorio) es especialmente difícil de batir y una meta exigente sin evidencia incentivaría la sobreconfianza.
