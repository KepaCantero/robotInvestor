# Objetivos del Bloque A — Buscador de Oportunidades de Inversión

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026** · Subordinado al Documento 0 óptima V5.0.

Este documento fija **qué debe conseguir** el Bloque A y **cómo se mide**. Cada objetivo tiene un indicador, una meta inicial, el responsable de medirlo y el requisito del propietario que cubre. Las metas son valores de arranque: el Evaluador y el operador las revisan trimestralmente con la evidencia acumulada.

**Requisitos del propietario (RQ):** RQ-0 funcionamiento descrito (periodicidad configurable, peticiones y consultas sin límite, dos informes, top-3 por clase, el Broker decide) · RQ-1 estrategias por clase de activo · RQ-2 automejora · RQ-3 sin cuellos de botella · RQ-4 eficiencia · RQ-5 autocrítica · RQ-6 historial interno · RQ-7 conocimiento verificado continuo · RQ-8 Fondo metodológico · RQ-9 verificación y borrado de referencias · RQ-10 referencias por temática y calidad · RQ-11 horizontes · RQ-12 conocimiento experto en los prompts.

---

## 1. Misión resumida

Encontrar pocas oportunidades de inversión buenas —dónde, por qué y cuándo— en cualquiera de los doce tipos de activo, y entregar al Bloque B (vía Broker) un encargo claro para que localice los mejores activos; explicarlas con claridad al Broker y al usuario, decir con honestidad cuánto se sabe y cuánto no, gastar solo lo que aporta valor y aprender de cada acierto y error.

---

## 2. Objetivos por dimensión

### D1 · Servicio al Broker Personal (RQ-0)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-01 | Entregar el informe periódico a tiempo | % de ciclos entregados en la fecha y hora configuradas | ≥ 98 % | Coordinador |
| OBJ-02 | Respetar la periodicidad elegida por el usuario | Cambios de configuración (CT-04) aplicados en el ciclo siguiente | 100 % | Coordinador |
| OBJ-03 | Atender toda petición sin rechazarla por número | Peticiones descartadas sin motivo | 0 | Orquestador |
| OBJ-04 | Responder rápido las consultas sencillas | Mediana de tiempo de respuesta N0 | < 2 min | Coordinador |
| OBJ-05 | Resolver las consultas sin escalado innecesario | % de consultas resueltas en N0 cuando la información existía | ≥ 85 % | Auditor (muestra) |
| OBJ-06 | Proponer hasta 3 opciones por tipo de activo (doce) sin relleno | Opciones del top-3 que incumplen elegibilidad | 0 | HT-09 / Auditor |
| OBJ-07 | Explicar siempre por qué hay menos de 3 | Clases con menos de 3 opciones sin `menos_de_tres_motivo` | 0 | HT-09 |
| OBJ-08 | Dar al Broker lo necesario para decidir según su modo | Opciones con `relevancia_decisional`, `reversibilidad` y `siguiente_paso_sugerido` | 100 % | HT-09 |
| OBJ-09 | Facilitar el paso al Bloque B | Opciones `ENVIAR_A_BLOQUE_B` con `paquete_para_bloque_B` completo | 100 % | HT-09 |
| OBJ-10 | Utilidad percibida por el Broker | Media de la valoración de utilidad (CT-04) | ≥ 4/5 | Evaluador |
| OBJ-11 | No asesorar al usuario | Comunicaciones del bloque fuera del canal Coordinador→Broker | 0 | Orquestador |

### D2 · Informe para el usuario inexperto (RQ-0)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-12 | Legibilidad | Índice Fernández-Huerta del informe visual | ≥ 70 | HT-07 |
| OBJ-13 | Brevedad | Frases de más de 20 palabras | ≤ 10 % | HT-07 |
| OBJ-14 | Visual | Informe con semáforo por clase, cartograma de regiones y tarjeta con riesgo, horizonte y confianza por opción | 100 % | HT-09 |
| OBJ-15 | Sin jerga sin explicar | Términos de la lista de jerga sin explicación | 0 | HT-07 |
| OBJ-16 | Accesible | Gráficos con texto alternativo y paleta apta para daltonismo | 100 % | Auditor |
| OBJ-17 | Coherencia entre informes | Discrepancias numéricas entre informe técnico, visual y JSON | 0 | HT-09 |

### D3 · Estrategias por clase de activo y calidad analítica (RQ-1, RQ-11)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-18 | Cada tipo de activo con su estrategia | Informes de clase que aplican indicadores y métodos de su propia sección 6 | 100 % | Auditor |
| OBJ-19 | Cobertura de los doce tipos de activo | Tipos activos analizados en cada ciclo (al menos arrastre verificado) | 100 % | Coordinador |
| OBJ-20 | Separar tendencia de oportunidad | Opciones con valoración explícita de lo ya descontado | 100 % | HT-09 / Auditor |
| OBJ-21 | Trazabilidad | Afirmaciones centrales con CLM→EVD; cifras con fuente y fecha o CALC- | 100 % | HT-09 |
| OBJ-22 | Corroboración | Afirmaciones centrales con ≥ 2 raíces independientes A/B o 1 primaria A | 100 % | Curador / HT-09 |
| OBJ-23 | Horizontes coherentes | Horizontes ofrecidos fuera de la tabla 8.3 | 0 | HT-09 |
| OBJ-24 | Honestidad predictiva | Probabilidades numéricas sin certificado del Evaluador | 0 | HT-09 |
| OBJ-25 | Pronósticos verificables | Pronósticos del top-3 congelados en F4 con criterio y fecha de resolución | 100 % | Evaluador |
| OBJ-26 | Diversificación honesta | Informes que declaran el número de apuestas independientes | 100 % | HT-09 |

### D3 bis · Función única y frontera con el Bloque B (RQ-0)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-68 | No seleccionar activos concretos | Opciones del top-3 que son un valor, emisión, fondo, contrato o token concreto (R21) | 0 | HT-09 / Auditor |
| OBJ-69 | Ámbitos bien delimitados | Opciones con `ambito` (incluye/excluye), `indicador_seguimiento` e `invertibilidad` | 100 % | HT-09 |
| OBJ-70 | Encargo útil para el Bloque B | Opciones con `criterios_seleccion_sugeridos`, `metricas_clave` y `preguntas_para_B` no vacíos | 100 % | HT-09 |
| OBJ-71 | Sin duplicados entre tipos | Oportunidades presentes en dos top-3 de tipos distintos | 0 | HT-09 |
| OBJ-72 | Utilidad para el Bloque B | Oportunidades enviadas por el Broker al Bloque B que el Bloque B no pudo analizar por falta de delimitación (cuando se comunique) | 0 | Evaluador (CT-22) |

### D4 · Rendimiento predictivo (RQ-2, RQ-11)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-27 | Batir a la referencia ingenua | Brier skill score o error relativo frente a la referencia, por clase×horizonte (≥ 30 resueltos) | > 0 en ≥ 50 % de las celdas el primer año; ≥ 70 % el segundo | Evaluador |
| OBJ-28 | Valor de las opciones | Rentabilidad relativa media del top-3 frente al índice de su clase, por horizonte | > 0, con IC declarado | Evaluador |
| OBJ-29 | Calibración | Calibración no rechazada en las celdas certificadas (criterio del Anexo A); ECE agregado con ≥ 200 pronósticos | < 0,10 | Evaluador |
| OBJ-30 | Detectar invalidaciones a tiempo | % de opciones cerradas por invalidación antes de pérdida severa (> 2 desviaciones típicas del horizonte) | ≥ 80 % | Evaluador |
| OBJ-31 | Publicar el historial | Informes periódicos con «cómo nos fue» por clase y horizonte | 100 % | HT-09 |

### D5 · Automejora (RQ-2)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-32 | Resolver todos los pronósticos vencidos | % de PRG- resueltos en ≤ 2 días tras su fecha | ≥ 98 % | Evaluador |
| OBJ-33 | Convertir resultados en lecciones | Lecciones LEC- nuevas o actualizadas por mes | ≥ 4 | Evaluador |
| OBJ-34 | Lecciones que se aplican | Encargos que cargan las lecciones vigentes de su ámbito | 100 % | Auditor (muestra) |
| OBJ-35 | Recalibrar con disciplina | Ajustes automáticos fuera de bandas o sin muestra suficiente | 0 | Orquestador |
| OBJ-36 | Mejorar con el tiempo | Tendencia trimestral del Brier skill score agregado | No negativa | Evaluador |
| OBJ-37 | Aprender del uso | Preguntas repetidas convertidas en mejoras del informe por defecto | 100 % de las detectadas | Evaluador |

### D6 · Eficiencia y fluidez (RQ-3, RQ-4)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-38 | Respetar el presupuesto | Consumo del ciclo semanal | ≤ 160 UC; desviación ≤ +10 % | Orquestador |
| OBJ-39 | No gastar en lo que no cambia | Clases con GC0 negativo resueltas en N1 (arrastre verificado) | 100 % | Orquestador |
| OBJ-40 | Embudo efectivo | Proporción candidatas GC1 / finalistas GC3 / top-3 registrada | Registrada en el 100 % de los ciclos | Coordinador |
| OBJ-41 | Reutilizar | % de cálculos servidos desde caché cuando eran idénticos | 100 % | Motor |
| OBJ-42 | Sin cuellos de botella | Tiempo en cola de cualquier agente por encima de 2× su objetivo | < 5 % de los encargos | Orquestador |
| OBJ-43 | Escalado a tiempo | Colas saturadas sin instancia adicional abierta | 0 | Orquestador |
| OBJ-44 | G3 sin esperas | Mediana del tiempo de validación G3 | < 5 min | Orquestador |

### D7 · Autocrítica y control (RQ-5)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-45 | Refutar toda finalista N2/N3 | Finalistas sin paquete CT-13 | 0 | HT-09 |
| OBJ-46 | Responder a las objeciones | Objeciones fuertes sin resolver en el top-3 | 0 | HT-09 |
| OBJ-47 | Pre-mortem | Candidatas GC2 con pre-mortem | 100 % | Auditor |
| OBJ-48 | Declarar lo que no se sabe | Opciones con condiciones de invalidación y riesgos explícitos | 100 % | HT-09 |
| OBJ-49 | Detectar sobreconfianza | Revisión mensual de confianza declarada frente a calibración | 12 al año | Evaluador |
| OBJ-50 | Auditoría útil | Hallazgos materiales convertidos en guía o propuesta en ≤ 1 ciclo | ≥ 90 % | Orquestador |

### D8 · Historial y memoria (RQ-6)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-51 | Historial completo | RUN-, QRY- y decisiones del Broker registrados en F5 | 100 % | Orquestador |
| OBJ-52 | Integridad | Reescrituras de historial (fuera de las bajas de referencias) | 0 | Orquestador |
| OBJ-53 | Continuidad | Informes con «cambios frente al ciclo anterior» | 100 % | HT-09 |

### D9 · Conocimiento y referencias (RQ-7, RQ-8, RQ-9, RQ-10, RQ-12)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-54 | Alimentación continua | Altas verificadas al mes en F7, F8 y F9 | ≥ 10, ≥ 5 y ≥ 10 | Orquestador (CT-21) |
| OBJ-55 | Fondo metodológico aplicado | Estrategias de búsqueda que citan los criterios del Fondo | 100 % | Auditor |
| OBJ-56 | Enlaces sanos | % de referencias en estado OK tras el barrido semanal | ≥ 95 % | HT-02 |
| OBJ-57 | Reacción a enlaces rotos | Referencias rotas sin acción tras dos barridos | 0 | HT-02 / Orquestador |
| OBJ-58 | Bajas trazables | Borrados sin línea en el Registro de bajas | 0 | Orquestador |
| OBJ-59 | Orden por temática y calidad | Referencias sin temática, Q o nivel; secciones mal ordenadas | 0 | Script de verificación |
| OBJ-60 | Cobertura | Temáticas con < 3 referencias de nivel A/B | Reducción trimestral | Documentadores / BFA |
| OBJ-61 | Veracidad | Revisión trimestral de retractaciones y refutaciones completada | 4 al año | Documentadores / BFA |
| OBJ-62 | Fiabilidad medida de fuentes de opinión | Fuentes de F9 con historial de exactitud medido por el Evaluador | Creciente; ≥ 50 % de las fuentes con pronósticos explícitos al año | Evaluador / BFA |
| OBJ-63 | Conocimiento experto en los prompts | Prompts con sección 10 «Base de conocimientos» completa y revisada en la revisión trimestral | 100 % | Operador |

### D10 · Seguridad y gobernanza (transversal)

| ID | Objetivo | Indicador | Meta inicial | Mide |
|---|---|---|---|---|
| OBJ-64 | Sin credenciales ni datos personales en mensajes | Incidencias | 0 | Orquestador |
| OBJ-65 | Inmunidad a contenido externo | Instrucciones incrustadas ejecutadas | 0 | Auditor |
| OBJ-66 | Cambios gobernados | Cambios de tipo 3 aplicados sin aprobación | 0 | Orquestador |
| OBJ-67 | Estados de madurez honestos | Componentes presentados como validados sin pruebas | 0 | Auditor |

---

## 3. Correspondencia requisito → objetivos

| Requisito | Objetivos |
|---|---|
| RQ-0 Funcionamiento descrito | OBJ-01 a OBJ-17, OBJ-68 a OBJ-72 |
| RQ-1 Estrategias por clase | OBJ-18 a OBJ-20 |
| RQ-2 Automejora | OBJ-27 a OBJ-37 |
| RQ-3 Sin cuellos de botella | OBJ-42 a OBJ-44 |
| RQ-4 Eficiencia | OBJ-38 a OBJ-41 |
| RQ-5 Autocrítica | OBJ-45 a OBJ-50 |
| RQ-6 Historial | OBJ-51 a OBJ-53 |
| RQ-7 Conocimiento continuo | OBJ-54, OBJ-62 |
| RQ-8 Fondo metodológico | OBJ-55 |
| RQ-9 Verificación y borrado | OBJ-56 a OBJ-58, OBJ-61 |
| RQ-10 Temática y calidad | OBJ-59, OBJ-60 |
| RQ-11 Horizontes | OBJ-23 a OBJ-25, OBJ-27 a OBJ-29 |
| RQ-12 Conocimiento en prompts | OBJ-63 |

## 4. Revisión

Trimestral, en la revisión programada (Documento 0, 18.2). Los objetivos de rendimiento predictivo (D4) solo se evalúan en celdas con muestra suficiente (Anexo A); antes se informa del progreso de la muestra.
