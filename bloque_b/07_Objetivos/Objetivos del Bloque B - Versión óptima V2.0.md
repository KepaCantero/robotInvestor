# Objetivos del Bloque B — Analizador de Mercados y Seleccionador de Activos Candidatos

**Bloque B · Robot Investor · Versión óptima V2.0 · actualizado V2.1, 03/11/2026** · Subordinado al Documento 0 del Bloque B óptima V2.1 (ante discrepancia, manda el Documento 0). La V2.1 incorpora los cambios del propietario B1–B7 (Documento 0, E.4): requisitos RQ-B16 a RQ-B19 y objetivos OBJ-B-129 a OBJ-B-152.

Este documento fija **qué debe conseguir** el Bloque B y **cómo se mide**. Cada objetivo tiene un indicador observable, una meta inicial, la fuente de la que se obtiene, la frecuencia de medición y el responsable de medirlo, y cubre uno o más requisitos del propietario. Las metas son valores de arranque: el Evaluador, el Orquestador y el operador las revisan cada trimestre (Documento 0, 18.2) con la evidencia acumulada. Los objetivos de rendimiento predictivo y de ranking solo se evalúan en celdas con muestra suficiente (Anexo A); antes se informa del progreso de la muestra.

---

## 1. Misión resumida

Cuando el Broker Personal pide el análisis de un ámbito —sector, subsector, temática, mercado geográfico, segmento de una clase de activo, estrategia o eslabón de una cadena de valor—, responder con el máximo rigor y exhaustividad si la oportunidad es real, por qué, cuánto descuenta ya el precio, cuándo y con qué riesgos, y **qué activos concretos la capturan mejor**, ordenados con su incertidumbre y con un encargo preparado para cada Bloque C.x; hacerlo en el tiempo autorizado y justificando cualquier ampliación; decir con honestidad cuánto se sabe y cuánto no; vigilar lo entregado sin reanalizar por iniciativa propia; y aprender de cada acierto y de cada error.

## 2. Requisitos del propietario

| ID | Requisito | Anclaje en el Documento 0 |
|---|---|---|
| RQ-B01 | Función única bajo petición: análisis en profundidad de un ámbito que pide el Broker; una petición = un análisis independiente; sin análisis periódicos por iniciativa propia (sí los seguimientos que encarga el Broker, R5 reformulada); frontera con los Bloques A y C; el Broker decide | 2.1–2.3, 2.8; R3–R7 |
| RQ-B02 | Rigor y exhaustividad máximos: doce dimensiones, despliegue estructural, máquina de proyecciones, tesis falsable, trazabilidad total | 8.2, 8.7–8.9; R9, R15–R17 |
| RQ-B03 | Estrategias de análisis variables según el tipo de objeto, los tipos de activo y el horizonte | 8.1–8.6 |
| RQ-B04 | Selección cuantitativa, trazable y robusta de los mejores activos candidatos, con un encargo preparado para cada Bloque C.x | 8.5; 9.4–9.7; R21 |
| RQ-B05 | Tiempo y coste bajo control: niveles, estimación previa, puerta de 30 minutos con justificación argumentada y opciones, política de autorización automática del Broker, registro del consumo | 7.2; 9.9; 10.3; R20, R23 |
| RQ-B06 | Autocrítica estructural | 11; R18, R19 |
| RQ-B07 | Aprendizaje y autorregulación verificables dentro de bandas (pronósticos, rankings, tiempos) | 12; R13, R14, R24 |
| RQ-B08 | Eficiencia y fluidez sin cuellos de botella (Biblioteca, embudo, paralelismo, instancias) | 10; 4.5; R22, R29 |
| RQ-B09 | Conocimiento verificado y vivo: Documentadores y Buscador, Fondo metodológico, verificación y borrado, temática y calidad | 13; R25 |
| RQ-B10 | Seis entregables: informe técnico exhaustivo, informe visual para el usuario novato, paquete JSON (encargos C.x, plan de seguimiento y `mapa_cadena_valor`), memorando ejecutivo, anexo de datos y mapa de oportunidades por eslabón de la cadena de valor; informe de parada e informe de seguimiento cuando corresponden | 14; 14.6–14.8 |
| RQ-B11 | Seguridad: credenciales vía Broker y bóveda, sin datos personales, contenido externo como dato, datos gratuitos | 17; R10–R12, R30 |
| RQ-B12 | Seguimiento de lo entregado sin análisis nuevos (Vigía), consultas del Broker y seguimientos periódicos encargados por el Broker | 7.6, 7.7, 7.13; R32, R35 |
| RQ-B13 | Historial íntegro de peticiones, ejecuciones, autorizaciones y decisiones | 15; R28 |
| RQ-B14 | Horizontes según el tipo de objeto y de activo (H1–H5) y honestidad sobre la capacidad predictiva (H5 con hitos y probabilidades cualitativas) | 8.6, 12.8; R13 |
| RQ-B15 | Conocimiento experto, preciso y específico en cada system prompt, con inventario de competencias | 13.8; Anexo G |
| RQ-B16 | (V2.1, B1 y B3) Valor por eslabón de la cadena: desglose jerárquico, cuellos de botella cuantificados (PCB), atractivo por eslabón (AE), hasta cinco mejores opciones por eslabón, radar de emergentes, startups y spin-offs (AG-B24), lista de comprobación profesional y entregable 6 | 8.7, 8.7.4, 8.10, 9.12, 9.13, 14.6 |
| RQ-B17 | (V2.1, B4) Análisis por capas 0–4 con puertas de viabilidad PV1–PV3, parada temprana con informe de parada y continuación solo si la fuerza el Broker | 7.10, 7.11; R33 |
| RQ-B18 | (V2.1, B5) Comunicación fluida en los dos sentidos con el Broker por un solo cauce: consultas del bloque con supuesto declarado y aportes del Broker en cualquier momento | 7.12; R34 |
| RQ-B19 | (V2.1, B7) Seguimientos periódicos encargados por el Broker (alta, modificación, pausa y cancelación en cualquier momento), ligeros y distintos del Vigía | 7.13; R5, R35 |

**Convenciones de las tablas.** «Fuente»: archivo o herramienta de la que se extrae el indicador. «Frecuencia»: *Por petición* (se comprueba en cada entrega, normalmente por HT-09), *Continua* (se vigila en cada evento), *Mensual*, *Trimestral* o *Semestral* (agregado del periodo). «Mide»: agente o herramienta responsable. Las comprobaciones G3B-xxx-nn son las del catálogo del «Plan de pruebas del Bloque B - V2.0», sección 3.

---

## 3. Objetivos por dimensión

### 3.1 · Función, servicio al Broker y frontera (RQ-B01, RQ-B12)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-01 | Atender toda petición con una decisión motivada | PET-B con admisión (ADMITIDA o RECHAZADA con motivo de D.5) y acuse en dos tiempos (recepción inmediata; estimación tras F0) | 100 %; mediana del acuse de recepción < 2 min | F1 | Mensual | Coordinador |
| OBJ-B-02 | No analizar sin petición | RUN-B sin PET-B admitida; INC-B `ANALISIS_SIN_PETICION` | 0 | F1, HA | Continua | Orquestador |
| OBJ-B-03 | Peticiones independientes | Lecturas de borradores de otra petición en curso (R6) | 0 | Registros de HT-06, HA | Mensual | Orquestador |
| OBJ-B-04 | Respetar la frontera con los Bloques C.x | Peticiones sobre un único activo devueltas con `bloque_c_sugerido`; entregables con precio objetivo o valoración individual completa | 100 %; 0 | F1; G3B-CON-16 | Por petición | Coordinador; HT-09 |
| OBJ-B-05 | Respetar la frontera con el Bloque A | Ámbitos no pedidos propuestos como análisis | 0 | ENT; Auditor (foco 9) | Por petición | Auditor |
| OBJ-B-06 | No asesorar al usuario ni comunicarse fuera del Broker | Comunicaciones fuera de CT-B-02, -03, -05, -06 y -07; entregables con lenguaje de orden o tamaño de posición | 0; 0 | HA; G3B-CON-15 | Continua | Orquestador; HT-09 |
| OBJ-B-07 | Consultas sencillas inmediatas | Tiempo de respuesta N0 | Mediana < 2 min; p90 < 5 min | F1 (QRY-B) | Mensual | Coordinador |
| OBJ-B-08 | Consultas trazables | Respuestas N0 con ≥ 1 referencia por afirmación y caducidades declaradas | 100 % | F1; muestreo del Auditor (10 %) | Mensual | Auditor |
| OBJ-B-09 | Consultas analíticas sin análisis encubierto | Consultas CONTRASTE o PROFUNDIZACION respondidas con propuesta de petición (nivel, alcance, estimación) | 100 % | F1 | Mensual | Orquestador |
| OBJ-B-10 | Utilidad percibida | Media de la valoración del Broker por entregable (CT-B-04) | ≥ 4/5 en cada entregable | F1 (RET-B), F5 (PRO-B) | Trimestral | Evaluador |
| OBJ-B-11 | Dar al Broker lo necesario para decidir | Entregas con `relevancia_decisional`, `siguiente_paso_sugerido` y `que_cambiaria_la_conclusion` | 100 % | G3B-CON-04 | Por petición | HT-09 |

### 3.2 · Rigor y exhaustividad (RQ-B02)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-12 | Doce dimensiones cubiertas | Dimensiones sin tratar ni excluir con motivo; tratadas por debajo de la profundidad exigida | 0; 0 | G3B-MET-05; PLAN-B | Por petición | HT-09 |
| OBJ-B-13 | Exclusiones defendibles | Exclusiones juzgadas insostenibles por el Auditor | ≤ 5 % de las exclusiones | HA (HAL-B) | Trimestral | Auditor |
| OBJ-B-14 | Despliegue estructural completo | Entregas con 4a–4e según el alcance del nivel | 100 % | G3B-MET-14 | Por petición | HT-09 |
| OBJ-B-15 | Toda cifra con origen | Cifras sin CALC-B servido ni DAT-B con fuente y fecha | 0 | G3B-DAT-01, -13 | Por petición | HT-09 |
| OBJ-B-16 | Toda afirmación trazada y etiquetada | Afirmaciones sin CLM-B→EVD-B, sin etiqueta epistémica o cifras sin clase | 0 | G3B-DAT-02, -03, -04 | Por petición | HT-09 |
| OBJ-B-17 | Corroboración de las premisas centrales | Premisas centrales con PA1 cumplida (o veredicto limitado a VIGILAR) | 100 % | G3B-DAT-11; F2 | Por petición | Curador; HT-09 |
| OBJ-B-18 | Datos declarados | Cifras críticas sobre DAT-B incompletas | 0 | G3B-DAT-05 | Por petición | HT-09 |
| OBJ-B-19 | Tesis falsable contrastada | Análisis N1–N3 con tesis falsable (o desmentido honesto) y el mínimo de hipótesis competidoras cerradas con evidencia | 100 % | G3B-MET-07, -08 | Por petición | HT-09; Auditor |
| OBJ-B-20 | Discriminación real de hipótesis | Hipótesis «cerradas» sin evidencia discriminante (hallazgo del foco 5) | ≤ 5 % de las auditorías | HA | Trimestral | Auditor |
| OBJ-B-21 | Proyecciones con protocolo | Máquinas de proyecciones con escenarios, modelos, sensibilidades y validación (o exclusión motivada) | 100 % | G3B-MET-09, -10 | Por petición | HT-09 |
| OBJ-B-22 | Mapa de cobertura honesto | Omisiones sin motivo; ámbitos «sin oportunidades» no distinguidos de «insuficientemente estudiados» | 0 | G3B-CON-12 | Por petición | HT-09 |
| OBJ-B-23 | Responder a lo preguntado | Preguntas del Broker y `preguntas_para_B` sin respuesta explícita | 0 | G3B-CON-14 | Por petición | HT-09 |
| OBJ-B-24 | Herencia re-verificada | Afirmaciones heredadas del Bloque A etiquetadas [HECHO] sin re-verificación; informes de origen BLOQUE_A sin «confirmado / refutado» | 0; 0 | G3B-DAT-12 | Por petición | HT-09 |
| OBJ-B-25 | Reproducibilidad | Re-ejecuciones CT-B-14 coincidentes o dentro de tolerancia sobre una muestra de artefactos decisivos | ≥ 98 % | RC; HA | Trimestral | Orquestador |

### 3.3 · Estrategias variables (RQ-B03)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-26 | Estrategia derivada de la matriz | Planes cuyos pesos efectivos reproduce HT-03 desde la matriz, los moduladores y las desviaciones declaradas | 100 % | PLAN-B; G3B-MET-02, -06 | Por petición | HT-09 |
| OBJ-B-27 | Desviaciones justificadas | Desviaciones > ±5 puntos sin motivo sustantivo aceptado por el Auditor | 0 | HA | Trimestral | Auditor |
| OBJ-B-28 | Especialistas según la matriz de activación | Planes con líderes activados y condicionales con disparador registrado | 100 % | PLAN-B | Por petición | Orquestador |
| OBJ-B-29 | Métodos según el objeto y el activo | Cálculos con perfil PERF-B- o SEL- incoherente sin composición declarada | 0 | G3B-MET-12; RC | Por petición | HT-09 |
| OBJ-B-30 | Playbook de horizonte aplicado | Memorandos e informes visuales con el énfasis del horizonte dominante (8.6) | ≥ 90 % de la muestra | Auditor (muestreo) | Trimestral | Auditor |
| OBJ-B-31 | Clasificación correcta del ámbito | Tipos de objeto reclasificados por el Auditor como erróneos (etiqueta comercial en vez de naturaleza económica) | ≤ 5 % | HA | Trimestral | Auditor |

### 3.4 · Selección de candidatos (RQ-B04)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-32 | Universo explícito | Tipos aplicables con universo (tamaño, fuentes, fecha, artefacto) y exclusiones motivadas | 100 % | G3B-SEL-01 | Por petición | HT-09 |
| OBJ-B-33 | Puertas del candidato respetadas | Candidatos del top-N o alternativas que no superan PC1–PC4 | 0 | G3B-SEL-02 | Por petición | HT-09 |
| OBJ-B-34 | Ranking reconstruible | S no reproducible por HT-03 | 0 | G3B-SEL-03 | Por petición | HT-09 |
| OBJ-B-35 | Incertidumbre declarada | Finalistas con IC 90 % de S y de rango; prioritarios con extremo inferior ≥ 55 y no FRONTERA | 100 % | G3B-SEL-04 | Por petición | HT-09 |
| OBJ-B-36 | Menos es legítimo | Top-N rellenados con candidatos que no superan las puertas; tipos con menos de N sin motivo | 0; 0 | G3B-SEL-06 | Por petición | HT-09 |
| OBJ-B-37 | Diversidad y no duplicación | Incumplimientos de 9.7 sin sustitución registrada; apuestas independientes mal contadas | 0 | G3B-SEL-07, -08 | Por petición | HT-09 |
| OBJ-B-38 | Encargos C.x útiles | Candidatos PRIORITARIO o SECUNDARIO del top-N con encargo completo y coherente | 100 % | G3B-EST-09, G3B-SEL-13 | Por petición | HT-09 |
| OBJ-B-39 | Sin sesgo de supervivencia | Universos con la comprobación de supervivencia superada (o limitación declarada) | ≥ 95 % en análisis; 100 % en evaluación y backtesting | F2 (DAT-B); F5 (MET-B) | Mensual | Evaluador |
| OBJ-B-40 | El ranking añade valor | Exceso medio del top-N frente a la media equiponderada del universo cribado, por playbook × horizonte (≥ 15 rankings resueltos) | > 0, con IC 90 % publicado | F5 (MET-B) | Trimestral | Evaluador |
| OBJ-B-41 | El orden es informativo | IC de rango medio (Spearman entre S y rentabilidad relativa posterior) | > 0, con IC 90 % publicado; certificado de ranking en ≥ 1 playbook × horizonte el segundo año | F5 | Trimestral | Evaluador |
| OBJ-B-42 | Selección validada por los Bloques C.x | Prioritarios valorados favorablemente por su Bloque C.x (cuando el Broker lo comunica; n ≥ 20) | ≥ 60 % | F5 (`seleccion_vs_C`) | Semestral | Evaluador |
| OBJ-B-43 | Doce playbooks operativos | Playbooks con prueba SEL-19 aprobada y, para pasar a validado, backtesting de rankings con datos reales | 12 de 12 (prueba); progresivo (backtesting) | Plan de pruebas, sección 5 | Trimestral | Orquestador |

### 3.5 · Tiempo, coste y autorización (RQ-B05)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-44 | Estimar siempre antes de empezar | Peticiones admitidas con p50 y p80 de tiempo y UC en el acuse | 100 % | F1 | Mensual | Coordinador |
| OBJ-B-45 | Estimación calibrada | Cobertura del p80 (fracción de peticiones con tiempo real ≤ p80) | Entre 75 % y 90 % | F1; F5 (MOD-B) | Mensual | Evaluador |
| OBJ-B-46 | Estimación precisa | Error absoluto mediano del p50 frente al real | ≤ 20 % | F1; F5 | Mensual | Evaluador |
| OBJ-B-47 | La puerta nunca se salta | Análisis con p80 > 30 min o que superan el tiempo autorizado más el margen sin AUT-B | 0 | G3B-TMP-02; F1 | Continua | Orquestador |
| OBJ-B-48 | Justificar siempre | AUT-B con justificación completa (qué aporta, incertidumbres que reduce y su efecto, qué se perdería), también automáticas y N3 expresos | 100 % | F1 | Mensual | Coordinador |
| OBJ-B-49 | Justificaciones específicas | Justificaciones concretas (dimensiones, candidatos o validaciones nombrados y efecto posible) en la muestra auditada | ≥ 95 % | Auditor (muestreo) | Trimestral | Auditor |
| OBJ-B-50 | Notificar la autorización automática | Autorizaciones por política notificadas al Broker | 100 % | F1 | Mensual | Coordinador |
| OBJ-B-51 | Detener con seguridad | Detenciones en punto de control seguro (nunca a mitad de un cálculo o escritura) | 100 % | HA (AVT-B); F1 (CKP-) | Continua | Orquestador |
| OBJ-B-52 | Reanudar sin repetir | Cálculos y evidencias reutilizados desde caché al reanudar | ≥ 95 % | RC; F2 | Mensual | Orquestador |
| OBJ-B-53 | Recortar alcance, nunca controles | Versiones ≤ 30 min o fases con alguna comprobación G3 omitida, o sin alcance reducido declarado | 0 | G3B-TMP-03 | Por petición | HT-09 |
| OBJ-B-54 | Cumplir el objetivo de tiempo del nivel | N1 terminados en ≤ 10 min; N2 estimados ≤ 30 min terminados en ≤ 30 min más el margen | ≥ 90 %; ≥ 90 % | F1 | Mensual | Orquestador |
| OBJ-B-55 | Consumo transparente | Entregas con tiempo y UC por fase y agente, estimado frente a real | 100 % | F1; G3B-TMP-01 | Por petición | Coordinador |
| OBJ-B-56 | Autorizaciones atendidas | Pendientes con recordatorio a las 24 h; caducadas registradas a los 7 días | 100 % | F1; HT-05 | Mensual | Coordinador |
| OBJ-B-57 | Rendición de cuentas de la puerta | Informe trimestral con frecuencia de PT30 y PTA, decisiones del Broker, uso de la política y desviaciones | 4 al año | HA (TRI-B) | Trimestral | Orquestador |

### 3.6 · Autocrítica y control previo a la salida (RQ-B06)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-58 | Refutar tesis y finalistas | Análisis N2/N3 con CT-B-17 sobre la tesis y sobre todos los finalistas | 100 % | G3B-CON-06, G3B-SEL-11 | Por petición | HT-09 |
| OBJ-B-59 | Ninguna objeción fuerte abierta en lo que se recomienda | INVERTIR, INVERTIR_ESCALONADO o PRIORITARIO_PARA_C con objeción fuerte sin resolver | 0 | G3B-CON-06, G3B-SEL-11 | Por petición | HT-09 |
| OBJ-B-60 | Pre-mortem, steelman y protocolo anti-sesgo | Entregas con los tres registrados | 100 % | F3 (REC-B) | Por petición | Auditor |
| OBJ-B-61 | Auditoría previa donde toca | N2 y N3 auditados antes de salir; muestreo de N1 dentro de la banda binomial del 30 % | 100 %; dentro de banda | HA (AUD-B, AUTC-B, AUTS-B) | Mensual | Orquestador |
| OBJ-B-62 | Sin errores graves que escapen | Hallazgos Críticos o Materiales detectados después de la entrega (re-auditoría muestral) | 0 Críticos; ≤ 2 % Materiales | HA | Trimestral | Auditor |
| OBJ-B-63 | Bucle eficaz | Auditorías cerradas en ≤ 2 vueltas; entregas con reserva de auditoría | ≥ 90 %; ≤ 10 % | HA | Trimestral | Orquestador |
| OBJ-B-64 | Fidelidad de los entregables | Entregas con cifras o afirmaciones ausentes del paquete autorizado | 0 | G3B-ENT-02 | Por petición | HT-09 |
| OBJ-B-65 | Detectar sobreconfianza | Revisión mensual de C declarada frente a acierto observado | 12 al año | F5 (MET-B) | Mensual | Evaluador |
| OBJ-B-66 | Publicar cómo nos fue | Entregas con historial de aciertos (ámbitos y rankings) con tamaño muestral y certificación | 100 % | G3B-CON-17 | Por petición | HT-09 |
| OBJ-B-67 | Hallazgos que mejoran | Hallazgos Materiales convertidos en guía o propuesta en ≤ 30 días | ≥ 90 % | HA (GUI-B, P3-B) | Trimestral | Orquestador |

### 3.7 · Aprendizaje, horizontes y honestidad predictiva (RQ-B07, RQ-B14)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-68 | Resolver todo lo vencido | PRG-B y rankings resueltos en ≤ 2 días tras su fecha | ≥ 98 % | F4; F5 (RES-B) | Mensual | Evaluador |
| OBJ-B-69 | Batir a la referencia ingenua | BSS o error frente a la ingenua > 0 por celda con ≥ 30 resueltos | ≥ 50 % de las celdas el primer año; ≥ 70 % el segundo | F5 (MET-B) | Trimestral | Evaluador |
| OBJ-B-70 | Calibración | ECE agregado con ≥ 200 pronósticos | < 0,10 | F5 | Trimestral | Evaluador |
| OBJ-B-71 | Veredictos con valor | Rentabilidad relativa media de los ámbitos con INVERTIR frente a su referencia; falsos positivos y negativos publicados | > 0 con IC; publicados | F5; F3 | Trimestral | Evaluador |
| OBJ-B-72 | Honestidad predictiva | Probabilidades publicadas sin certificado; rankings sin certificado sin su etiqueta | 0; 0 | G3B-CON-08, -09 | Por petición | HT-09 |
| OBJ-B-73 | Horizontes aplicables | Pronósticos con horizonte «No» para su tipo; cambios hacia o desde «No» sin tipo 3 | 0; 0 | G3B-CON-10; F10 | Por petición | HT-09; Orquestador |
| OBJ-B-74 | Lecciones que nacen | Lecciones LEC-B nuevas o actualizadas | ≥ 4 al mes | F5 | Mensual | Evaluador |
| OBJ-B-75 | Lecciones que se aplican | Encargos que cargan las lecciones vigentes de su ámbito (≤ 10) | 100 % | Auditor (muestreo) | Trimestral | Auditor |
| OBJ-B-76 | Recalibrar con disciplina | Ajustes automáticos fuera de bandas, sin muestra suficiente o sin sombra | 0 | F5 (AJU-B); F10 | Trimestral | Orquestador |
| OBJ-B-77 | Mejorar con el tiempo | Tendencia trimestral del BSS agregado y del exceso del top-N | No negativa | F5 | Trimestral | Evaluador |
| OBJ-B-78 | Medir también lo no seguido | Pronósticos de candidatos descartados o de ámbitos no seguidos por el Broker resueltos | 100 % | F4 | Mensual | Evaluador |
| OBJ-B-79 | Aprender del uso | Preguntas repetidas convertidas en mejora del entregable por defecto | 100 % de las detectadas | F5 (PRO-B) | Trimestral | Evaluador |
| OBJ-B-80 | Modelo de tiempos al día | Reestimación mensual cuando hay ≥ 20 peticiones nuevas | 100 % | F5 (MOD-B) | Mensual | Evaluador |

### 3.8 · Eficiencia y fluidez (RQ-B08)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-81 | Reutilizar la Biblioteca | Dimensiones vigentes y sin cambio material reutilizadas (GC0); reutilizaciones sin re-verificación de primer uso | ≥ 90 %; 0 | F6 (`usos`); PLAN-B | Mensual | Orquestador |
| OBJ-B-82 | No recalcular lo idéntico | Cálculos idénticos servidos desde caché | 100 % | RC | Mensual | Motor |
| OBJ-B-83 | Embudo efectivo | Finalistas ≤ 2 × top-N; proporción universo / finalistas / top-N registrada | 100 % | F3; G3B-MET-16 | Por petición | Orquestador |
| OBJ-B-84 | Gastar solo lo que aporta | Búsquedas, cálculos y encargos sin valor informativo declarado | 0 | Contratos CT-B-09…13 (HT-06) | Mensual | Orquestador |
| OBJ-B-85 | Sin cuellos de botella | Encargos con tiempo en cola > 2 × el objetivo del agente | < 5 % | HA (CAR-B) | Mensual | Orquestador |
| OBJ-B-86 | Escalar a tiempo | Colas por encima del umbral sin instancia adicional en agentes sin estado | 0 | HA (ORD-B) | Continua | Orquestador |
| OBJ-B-87 | Validación rápida | Mediana del tiempo de dictamen G3 | < 5 min | HA (G3V-B) | Mensual | Orquestador |
| OBJ-B-88 | Fondo sin interferir | Tareas de fondo dentro de su presupuesto y sin retrasar peticiones en curso | 100 % | HA; F1 | Mensual | Orquestador |
| OBJ-B-89 | Paralelismo efectivo | Nodos del grafo que bloquearon a otros sin necesidad (RND-B) | Decreciente trimestre a trimestre | F5 (RND-B) | Trimestral | Evaluador |

### 3.9 · Conocimiento verificado y vivo (RQ-B09)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-90 | Cobertura mínima | Áreas de F7 (22), F8 (14) y F9 (18) con ≥ 20 referencias verificadas | 100 % de las áreas | HA (MAN-B) | Mensual | Documentadores, Buscador |
| OBJ-B-91 | Alimentación continua | Altas verificadas al mes en F7, F8 y F9 | ≥ 10, ≥ 5 y ≥ 10 | HA (MAN-B) | Mensual | Orquestador |
| OBJ-B-92 | Enlaces sanos | Referencias en OK (o REDIRIGIDO resuelto) tras el barrido semanal | ≥ 95 % | HT-02 | Semanal | Documentadores, Buscador |
| OBJ-B-93 | Reacción a lo roto | Referencias rotas sin acción tras dos barridos; bajas sin línea en el Registro de bajas; bajas que sustentaban EVD-B sin aviso al Curador | 0; 0; 0 | HT-02; F7–F9; F2 | Mensual | Orquestador |
| OBJ-B-94 | Orden por temática y calidad | Referencias sin temática válida, Q o nivel; inversiones del orden por Q | 0 | Script de verificación | Mensual | Orquestador |
| OBJ-B-95 | Fondo metodológico aplicado | Estrategias de búsqueda que citan sus criterios | 100 % | Auditor (muestreo) | Trimestral | Auditor |
| OBJ-B-96 | Veracidad revisada | Revisiones trimestrales de retractaciones y refutaciones | 4 al año | HA (MAN-B) | Trimestral | Documentadores, Buscador |
| OBJ-B-97 | Fiabilidad medida de fuentes | Fuentes de F9 con pronósticos explícitos medidas por el Evaluador | Creciente; ≥ 50 % al año | F5 (FUE-B) | Trimestral | Evaluador |
| OBJ-B-98 | Biblioteca fiable | Fichas actualizadas con contenido no entregado; caducidades sin marcar a su fecha | 0; 0 | F6 | Mensual | Orquestador |
| OBJ-B-99 | Datos gratuitos | Conectores de pago activos sin aprobación del operador | 0 | F10 (P-B-50) | Continua | Orquestador |

### 3.10 · Entregables (RQ-B10)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-100 | Seis entregables completos | Entregas con los seis entregables y el informe técnico con sus dieciséis secciones | 100 % | ENT; G3B-ENT-05; G3B-ENT-11 | Por petición | HT-09 |
| OBJ-B-101 | Legibilidad para el usuario novato | Fernández-Huerta corregido del informe visual; frases de más de 20 palabras | ≥ 70; ≤ 5 % | HT-07; G3B-ENT-01 | Por petición | HT-07 |
| OBJ-B-102 | Comprensión real | Lectura del informe visual y respuestas correctas en prueba con usuarios sin formación financiera | Mediana < 3 min; ≥ 80 % | Prueba PB-B-ENT-02 | Semestral | Operador |
| OBJ-B-103 | Coherencia entre entregables | Discrepancias de veredicto, cifras, candidatos o fecha de corte | 0 | G3B-ENT-03, G3B-DAT-08 | Por petición | HT-09 |
| OBJ-B-104 | Reproducibilidad del anexo | Cifras y rankings reconstruidos por un tercero desde el anexo de datos (muestra) | ≥ 98 % | Prueba PB-B-ENT-05 | Semestral | Auditor |
| OBJ-B-105 | Informe visual sin listas de compra | Informes visuales con listas de valores para comprar | 0 | G3B-ENT-04 | Por petición | HT-09 |
| OBJ-B-106 | Limitaciones visibles | Reservas de auditoría, alcance reducido y estados degradados en la portada y en el memorando | 100 % | G3B-ENT-09 | Por petición | HT-09 |
| OBJ-B-107 | Memorando breve | Memorandos de una o dos páginas con los contenidos de 14.4 | 100 % | G3B-ENT-06 | Por petición | HT-09 |

### 3.11 · Seguridad y gobernanza (RQ-B11)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-108 | Claves solo en la bóveda | Claves encontradas fuera de la bóveda (mensajes, archivos, registros, RC, ENT); incidencias tratadas con aviso al Broker en ≤ 1 día | 0; 100 % | Barrido mensual; HA (INC-B) | Mensual | Orquestador |
| OBJ-B-109 | Solicitudes de credencial completas | CRED-B con proveedor, finalidad, alcance, duración, alternativa y degradación | 100 % | F1 | Mensual | Coordinador |
| OBJ-B-110 | Sin datos personales | Mensajes o archivos con datos personales, cartera o perfil procesados | 0 | G3B-EST-05; HA | Continua | Orquestador |
| OBJ-B-111 | Inmunidad al contenido externo | Instrucciones incrustadas ejecutadas | 0 | HA; G3B-EST-06 | Continua | Auditor |
| OBJ-B-112 | Canales y matriz cerrados | Mensajes por canales no previstos ejecutados; escrituras fuera de matriz con efecto | 0; 0 | HA | Continua | Orquestador |
| OBJ-B-113 | Cambios gobernados | Cambios de tipo 3 aplicados sin aprobación; ajustes automáticos sobre reglas, canales, seguridad o el umbral de 30 min | 0; 0 | HA; F10 | Trimestral | Orquestador |
| OBJ-B-114 | Madurez honesta | Componentes presentados como validados sin pruebas aprobadas | 0 | G3B-MET-13; Plan de pruebas | Por petición | HT-09; Auditor |
| OBJ-B-115 | Degradar declarando | Usos de credencial ausente, conector caído o herramienta caída sin limitación declarada | 0 | G3B-TMP-04 | Por petición | HT-09 |
| OBJ-B-116 | Frescura declarada, sin tiempo real simulado | Datos críticos sin antigüedad declarada; datos fuera de frescura sin justificación | 0; 0 | G3B-DAT-06 | Por petición | HT-09 |

### 3.12 · Seguimiento de lo entregado (RQ-B12)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-117 | Vigilar a tiempo | Rondas del Vigía ejecutadas en la frecuencia de su horizonte y en cada catalizador fechado | ≥ 98 % | F3 (`rondas`); HT-05 | Mensual | Evaluador |
| OBJ-B-118 | Avisar rápido | Alertas transmitidas al Broker: REVISION en ≤ 1 día hábil; INVALIDACION en el mismo día | 100 % | F1 (ALR-B) | Mensual | Coordinador |
| OBJ-B-119 | Avisar sin reanalizar | Alertas con la nota de que no se inició análisis; análisis abiertos o veredictos modificados por el Vigía | 100 %; 0 | F1; F3 | Continua | Orquestador |
| OBJ-B-120 | Detectar invalidaciones antes del daño | REC-B invalidadas avisadas antes de una pérdida > 2 desviaciones típicas del horizonte | ≥ 80 % | F3; F5 | Trimestral | Evaluador |
| OBJ-B-121 | Pocas falsas alarmas | Alertas REVISION que no derivaron en invalidación ni en petición nueva | Medida y decreciente | F1; F3 | Trimestral | Evaluador |
| OBJ-B-122 | Vigía dimensionado | Criterio de separación (> 150 REC-B o > 40 % del tiempo de AG-B23 dos meses seguidos) vigilado y, si se cumple, propuesta de tipo 3 | 12 lecturas al año | HA (CAR-B) | Mensual | Orquestador |

### 3.13 · Historial (RQ-B13)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-123 | Historial completo | PET-B, RUN-B, AUT-B, CRED-B, QRY-B, ALR-B y RET-B registrados; desde la V2.1 también CNS-B, puertas de viabilidad, paradas, continuaciones forzadas (F1) y SEG-B y CIC-B (F11) | 100 % | F1, F11 | Mensual | Orquestador |
| OBJ-B-124 | Integridad | Reescrituras sustantivas de F1–F6, F11, RC o HA (fuera de bajas de referencias y retención) | 0 | Instantáneas con hash | Mensual | Orquestador |
| OBJ-B-125 | Peticiones reconstruibles | Peticiones de una muestra reconstruidas íntegramente solo con los registros | 100 % | F1–F6, RC, HA | Trimestral | Auditor |

### 3.14 · Conocimiento experto en los prompts (RQ-B15)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-126 | Estructura común | Prompts con las doce secciones del Anexo G y base de conocimientos completa (métodos con autor, fórmulas, umbrales, fuentes TFB, errores típicos, ejemplos, salida JSON) | 100 % | Prueba PB-B-CON-09 | Trimestral | Operador |
| OBJ-B-127 | Exactitud técnica | Afirmaciones técnicas correctas en un muestreo de 10 por prompt | ≥ 95 % | Prueba PB-B-CON-09 | Trimestral | Auditor |
| OBJ-B-128 | Sin residuos de otros bloques | Identificadores de otros bloques no intencionados en prompts, funciones y archivos | 0 | Prueba PB-B-CON-11 | Por versión | Orquestador |

### 3.15 · Valor por eslabón y emergentes (RQ-B16, V2.1)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-129 | Desglose completo y conciliado | Análisis con `mapa_cadena_valor` válido (B.16), profundidad del nivel y omisiones motivadas; hijos que concilian con el padre | 100 %; ≥ 95 % | G3B-EST-11; G3B-MET-20 | Por petición | HT-09 |
| OBJ-B-130 | Cuellos y atractivo reproducibles | PCB y AE reconstruidos por HT-03 desde los indicadores y componentes | 100 % | G3B-MET-19; anexo de datos | Por petición | HT-09 |
| OBJ-B-131 | Todo candidato con su eslabón | Candidatos con `eslabon_id` válido | 100 % | G3B-SEL-16 | Por petición | HT-09 |
| OBJ-B-132 | Mejores opciones por eslabón sin relleno | Eslabones cualificados con tabla de opciones (≤ 5) o motivo; opciones con S < 50 o duplicadas | 100 %; 0 | G3B-SEL-17 | Por petición | HT-09 |
| OBJ-B-133 | Radar de emergentes útil | Análisis SECTOR, TEMATICA o CADENA_DE_VALOR con radar; emergentes con vía de exposición y PEM; emergentes invertibles que pasan al universo | 100 %; 100 %; 100 % | G3B-SEL-18; F3 (EMG-B) | Por petición | HT-09 |
| OBJ-B-134 | Emergentes que se confirman | Emergentes en vigilancia que alcanzan su hito de tracción o salida a bolsa en dos años | Medida y creciente | F3; F6 (radar) | Semestral | Evaluador |
| OBJ-B-135 | Lista profesional completa | Ítems de 8.10 con estado y referencia válida (N2/N3) | 100 % | G3B-MET-21 | Por petición | HT-09 |
| OBJ-B-136 | Entregable 6 útil | Valoración del Broker del mapa por eslabón | ≥ 4/5 | F1 (RET-B) | Trimestral | Evaluador |

### 3.16 · Capas y puertas de viabilidad (RQ-B17, V2.1)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-137 | Puertas evaluadas y coherentes | Análisis con PV1–PV3 registradas, con insumos y resultado conforme a los umbrales | 100 % | F1; G3B-MET-18 | Por petición | HT-09 |
| OBJ-B-138 | Parar barato | Mediana del tiempo hasta un informe de parada en PV1 | ≤ 8 min (N2) | F1 | Mensual | Coordinador |
| OBJ-B-139 | Informe de parada claro | Informes de parada con 3–6 motivos con evidencia, «qué lo cambiaría» observable y sugerencia coherente | 100 % | G3B-CON-19; G3B-EST-12 | Por petición | HT-09 |
| OBJ-B-140 | Pocas paradas erróneas | Falsos negativos de las puertas (ámbitos parados cuyo indicador batió a su referencia en el horizonte) | Medida; ≤ 20 % tras 30 resueltos | F5 (MET-B) | Trimestral | Evaluador |
| OBJ-B-141 | Forzar sin rebajar | Continuaciones forzadas declaradas en los entregables y sin umbral rebajado | 100 %; 0 | G3B-CON-20 | Por petición | HT-09 |
| OBJ-B-142 | Tiempo por capa bajo control | Desviación real frente a p80 por capa | Cobertura del p80 ≥ 80 % | F1; F5 (MOD-B) | Mensual | Evaluador |

### 3.17 · Consultas al Broker (RQ-B18, V2.1)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-143 | Un solo cauce | Consultas enviadas al Broker fuera del Coordinador o sin filtro del Director | 0 | F1; HA | Continua | Orquestador |
| OBJ-B-144 | Preguntar poco y bien | Consultas por petición dentro de los límites del nivel; consultas que el Director podía resolver con la memoria | 100 %; decreciente | F1; G3B-EST-14 | Mensual | Orquestador |
| OBJ-B-145 | Supuestos visibles | Supuestos aplicados que figuran en todos los entregables y en la entrega | 100 % | G3B-CON-21 | Por petición | HT-09 |
| OBJ-B-146 | Pausas cortas | Mediana del tiempo en `EN_PAUSA_CONSULTA` | ≤ 4 h (plazo) | F1 | Mensual | Coordinador |
| OBJ-B-147 | Aprender de las dudas | Consultas recurrentes convertidas en lección de producto | 100 % | F5 (PRO-B, LEC-B) | Trimestral | Evaluador |

### 3.18 · Seguimientos encargados (RQ-B19, V2.1)

| ID | Objetivo | Indicador | Meta inicial | Fuente | Frecuencia | Mide |
|---|---|---|---|---|---|---|
| OBJ-B-148 | Solo por encargo | Ciclos sin SEG-B activo; análisis profundos iniciados por un ciclo | 0; 0 | F11; F1; G3B-TMP-06 | Continua | Orquestador |
| OBJ-B-149 | Ciclos puntuales y ligeros | Ciclos ejecutados en su fecha; mediana del tiempo por ciclo | ≥ 98 %; < 10 min | F11; F1 | Mensual | Coordinador |
| OBJ-B-150 | Informe de seguimiento correcto | Informes con semáforo, recomendación, próximo ciclo y nota de no inicio de análisis | 100 % | G3B-EST-13 | Por ciclo | HT-09 |
| OBJ-B-151 | Semáforo que anticipa | Ciclos ÁMBAR o ROJO confirmados después por el Vigía o por un análisis | Medida y creciente | F5 (MET-B) | Trimestral | Evaluador |
| OBJ-B-152 | Cancelar al instante | Cancelaciones aplicadas sin ciclo posterior | 100 % | F11 | Continua | Coordinador |

---

## 4. Correspondencia requisito → objetivos

| Requisito | Objetivos |
|---|---|
| RQ-B01 | OBJ-B-01 a OBJ-B-06, OBJ-B-11 |
| RQ-B02 | OBJ-B-12 a OBJ-B-25 |
| RQ-B03 | OBJ-B-26 a OBJ-B-31 |
| RQ-B04 | OBJ-B-32 a OBJ-B-43 |
| RQ-B05 | OBJ-B-44 a OBJ-B-57 |
| RQ-B06 | OBJ-B-58 a OBJ-B-67 |
| RQ-B07 | OBJ-B-68 a OBJ-B-71, OBJ-B-74 a OBJ-B-80 |
| RQ-B08 | OBJ-B-81 a OBJ-B-89 |
| RQ-B09 | OBJ-B-90 a OBJ-B-99 |
| RQ-B10 | OBJ-B-100 a OBJ-B-107 |
| RQ-B11 | OBJ-B-108 a OBJ-B-116 |
| RQ-B12 | OBJ-B-07 a OBJ-B-10, OBJ-B-117 a OBJ-B-122 |
| RQ-B13 | OBJ-B-123 a OBJ-B-125 |
| RQ-B14 | OBJ-B-69, OBJ-B-70, OBJ-B-72, OBJ-B-73 |
| RQ-B15 | OBJ-B-126 a OBJ-B-128 |
| RQ-B16 | OBJ-B-129 a OBJ-B-136 |
| RQ-B17 | OBJ-B-137 a OBJ-B-142 |
| RQ-B18 | OBJ-B-143 a OBJ-B-147 |
| RQ-B19 | OBJ-B-148 a OBJ-B-152 |

## 5. Herencia de los objetivos anteriores

### 5.1 De los once objetivos de la V1.3

Los once objetivos de la V1.3 (histórico en `99_Historico_V1.3/04_Objetivos`) se conservan en su intención y se convierten en indicadores medibles:

| Objetivo V1.3 | Dónde vive ahora | Cambio principal |
|---|---|---|
| O1 Análisis profundo bajo demanda | 3.1 (OBJ-B-01 a -06) y 3.5 | «Un ciclo a la vez» pasa a peticiones independientes en paralelo con niveles N0–N3 y PERS, estimación y puerta de 30 minutos |
| O2 Comprensión estructural del mercado | 3.2 (OBJ-B-12 a -14, -22) y 3.3 | Las doce dimensiones depuradas, la matriz de estrategia y los especialistas sustituyen a las fichas de familia y los módulos internos |
| O3 Tesis falsables y escenarios honestos | 3.2 (OBJ-B-16, -19, -20, -21) | Etiquetado epistémico y hipótesis competidoras verificadas por HT-09 y por el Auditor |
| O4 Proyecciones trazables y reproducibles | 3.2 (OBJ-B-15, -18, -21, -25) | Motor propio con artefacto reproducible y re-ejecución CT-B-14 |
| O5 Filtro de invertibilidad explícito | 3.4 (OBJ-B-32 a -43) | El filtro de la recomendación pasa a la **selección cuantitativa de candidatos** con PC1–PC8, S, IC y encargos C.x |
| O6 Calidad antes de la salida | 3.6 (OBJ-B-58 a -64) | Se conserva la auditoría previa; G3 determinista con catálogo numerado; reserva o bloqueo tras tres vueltas |
| O7 Trazabilidad con custodia | 3.2, 3.13 | Un propietario por archivo (F1–F10, RC, HA) en lugar de custodia centralizada |
| O8 Convivencia con el ecosistema | 3.1 (OBJ-B-04 a -06) | Frontera explícita con A (entrada por el Broker) y con C.x (encargos, no valoración individual) |
| O9 Seguridad y límites | 3.11 | Credenciales vía Broker y bóveda; datos gratuitos; frescura declarada |
| O10 Gobernanza viva | 3.6 (OBJ-B-67), 3.11 (OBJ-B-113), 3.5 (OBJ-B-57) | Cuadro trimestral centrado en calibración, rankings, tiempos y carga |
| O11 Evaluación posterior y aprendizaje | 3.7 | Certificados de probabilidad **y de ranking**, modelo de tiempos, recalibración en sombra |

### 5.2 De los objetivos del Bloque A V5.0

Se adoptan su forma (indicador con meta inicial y responsable) y sus familias de servicio, legibilidad, rendimiento predictivo, automejora, eficiencia, autocrítica, historial, conocimiento y seguridad, con los umbrales comunes del ecosistema (Fernández-Huerta ≥ 70; N0 < 2 min; BSS > 0 en el 50 % y el 70 % de las celdas; ECE < 0,10; enlaces OK ≥ 95 %). Se añaden las familias propias del Bloque B: **selección de candidatos y rankings** (3.4), **tiempo y autorización** (3.5) y **seguimiento sin análisis** (3.12).

## 6. Cuadro de mando trimestral

En la revisión programada (18.2), el Orquestador presenta al operador, sin compensar unas familias con otras: (1) integridad (OBJ-B-15, -16, -47, -53, -59, -108, -112); (2) rigor (OBJ-B-12, -19, -22, -24); (3) selección (OBJ-B-36, -39, -40, -41, -42); (4) predicción (OBJ-B-69, -70, -71, -72); (5) tiempo (OBJ-B-45, -46, -54, -57); (6) eficiencia (OBJ-B-81, -85, -87); (7) conocimiento (OBJ-B-90, -92, -93); (8) utilidad (OBJ-B-10, -102, -136); y, desde la V2.1, (9) puertas y consultas (OBJ-B-137, -140, -141, -145) y (10) seguimientos (OBJ-B-148, -149, -151). Cada familia se informa con su tamaño muestral; un objetivo sin muestra suficiente se marca «en construcción».

## 7. Lo que expresamente no es objetivo del bloque

- **Decidir, aconsejar al usuario o dimensionar posiciones** (R4): el bloque analiza y selecciona; el Broker decide.
- **Analizar por iniciativa propia o de forma periódica** (R5): ni siquiera ante una alerta del Vigía (R32). Los únicos ciclos periódicos son los seguimientos que el Broker encarga (CT-B-29) y nunca abren un análisis profundo (R35).
- **Seguir gastando tiempo en un ámbito que no supera sus puertas de viabilidad** sin que el Broker fuerce la continuación (R33).
- **Recomendar emergentes**: el PEM ordena el radar; no es una recomendación ni sustituye a S.
- **Buscar oportunidades en amplitud** (función del Bloque A) ni **valorar en profundidad un activo individual** (función de los Bloques C.x; R7).
- **Llenar el top-N** cuando no hay candidatos que superen las puertas (R21).
- **Minimizar el coste a toda costa**: no hay techo de coste; hay registro, puerta de tiempo y valor de la información (7.2; R22).
- **Usar datos de pago o en tiempo real** sin autorización del operador, o simular su disponibilidad (R30).
- **Publicar probabilidades o rankings «con ventaja»** sin certificado del Evaluador (R13).

## 8. Revisión

Trimestral, en la revisión programada del Documento 0 (18.2). Un cambio de meta es un cambio de tipo 1 si la hace más exigente y de tipo 3 si la relaja. Las pruebas que miden cada objetivo están en el «Plan de pruebas del Bloque B - V2.0» (actualizado V2.1; familias PV, CNS, SEG, ESL y H5 para los objetivos OBJ-B-129 a OBJ-B-152).
