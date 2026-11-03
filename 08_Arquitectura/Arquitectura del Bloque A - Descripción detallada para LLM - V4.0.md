# Arquitectura del Bloque A — Descripción detallada para LLM

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026** · Subordinado al Documento 0 óptima V5.0 (ante discrepancia, manda el Documento 0).

## 0. Instrucciones de ingesta

Este texto describe, de forma cerrada y autosuficiente, la arquitectura del Bloque A para que una LLM la entienda sin leer el resto del paquete. Trátalo como descripción normativa de un sistema ya definido. Los identificadores (AG-, CT-, F, HT-, N0–N3, GC0–GC3, G1–G4, PS1–PS8, H1–H4, R1–R25) son términos fijados. La imagen `Arquitectura del Bloque A - V5.0.png` representa lo mismo.

## 1. Qué es el Bloque A

Bloque de la arquitectura multiagente Robot Investor con **una sola función: encontrar oportunidades de inversión** —dónde, por qué y en qué horizonte— en **cualquiera de doce tipos de activo** y en cualquier mercado, región, sector, subsector, temática, segmento o estrategia. Su cliente único es el **Broker Personal**, que gestiona la información de todos los bloques, es el único que habla con el usuario y decide (en modo autónomo, manual o semiautónomo) si envía cada oportunidad al **Bloque B** o la descarta. El Bloque B analiza en profundidad el mercado de esa oportunidad y **localiza los mejores activos concretos**. Ejemplo: el Bloque A detecta que el sector textil tendrá una tendencia alcista en los próximos meses; el Bloque B estudia el sector textil y localiza los mejores activos dentro de él.

**Frontera A/B (R21).** El Bloque A nunca selecciona ni compara activos o instrumentos concretos; su granularidad máxima es el **segmento**. Solo puede citar nombres concretos como ejemplos ilustrativos del ámbito.

**Doce tipos de activo** (cada uno con su Analista): RV renta variable · RF renta fija · DIV divisas · MP materias primas · IDX índices bursátiles · FON fondos y vehículos de inversión colectiva · DER derivados financieros · INM activos inmobiliarios cotizados · CRI criptoactivos y activos digitales · ALT capital privado y activos alternativos · MON instrumentos monetarios y liquidez · TCV tipos de interés, crédito y volatilidad. Reglas de asignación por «motor de rentabilidad» evitan duplicados (Documento 0, 2.6).

## 2. Qué entrega

1. **Ciclo periódico** (semanal por defecto; el usuario lo cambia a través del Broker): informe con **hasta 3 opciones por cada uno de los doce tipos de activo**. Si no hay tres que superen los controles, se entregan menos (incluso ninguna) con explicación.
2. **Peticiones ad hoc** del Broker, sin límite de número, y **consultas** sobre cualquier aspecto.
3. Por cada análisis: **informe técnico** para el Broker; **informe visual y minimalista** para el usuario inexperto (semáforo de los doce tipos, cartograma de regiones, tarjetas con riesgo 1–5, horizonte, confianza, «qué podría salir mal», historial de aciertos, lenguaje llano); y **paquete JSON** con las opciones y, para cada una, un **encargo preparado para el Bloque B**: ámbito (incluye/excluye), tesis y mecanismo, horizontes y pronósticos, catalizadores, riesgos e invalidación, indicador de seguimiento, criterios de selección sugeridos, métricas clave y preguntas para el Bloque B.
4. Cada opción incluye `relevancia_decisional`, `reversibilidad` y `siguiente_paso_sugerido` para que el Broker aplique su modo de decisión.

## 3. Agentes (25, en cuatro planos)

**P1 · Interfaz y ciclo**
- **AG-01 Coordinador de Peticiones y Consultas**: única interfaz con el Broker; programa el ciclo (HT-05); encola y prioriza peticiones; asigna nivel N0–N3 y presupuesto; responde consultas N0; entrega; mantiene F5 (Historial de análisis) y la parte de servicio de F10 (Configuración).

**P2 · Análisis**
- **AG-02 Analizador de Tendencias de Inversión (director)**: plan y reparto entre los doce tipos de activo; asignación de tipo sin duplicados; integración; coherencia entre clases (factores comunes, apuestas independientes); selección del top-3 con HT-03; gestiona prospectiva, refutación, validación y redacción; propietario de F1 (tendencias) y F3 (oportunidades).
- **Doce Analistas de tipo de activo** (AG-03 RV, AG-04 RF, AG-05 DIV, AG-06 MP, AG-21 IDX, AG-22 FON, AG-23 DER, AG-07 INM, AG-08 CRI, AG-09 ALT, AG-24 MON, AG-25 TCV): cada uno con su estrategia de cribado, delimitación del ámbito, valoración, catalizadores, riesgos, invertibilidad del ámbito, indicador de seguimiento, horizontes y encargo para el Bloque B; trabajan en paralelo y escalan por instancias.
- **AG-10 Analista de Prospectiva y Horizontes**: escenarios y pronósticos verificables por horizonte; alta en F4.
- **AG-11 Analista de hipótesis contrarias**: refutación adversarial de las finalistas.
- **AG-12 Curador de Evidencia**: deduplicación, raíces independientes, normalización temporal; propietario de F2.
- **AG-13 Motor de Cálculo Avanzado**: cálculo reproducible con artefacto (CT-09) y re-ejecución independiente (CT-10). Internamente: Orquestador de Cálculo, servicios técnicos STC-1 a STC-4 y módulos MC-01 a MC-10 (estadística; series y volatilidad; econometría; crecimiento y prospectiva; simulación; aprendizaje automático; optimización y riesgo; auditoría; valoración de activos; evaluación predictiva y backtesting). Perfiles por clase de activo. No interpreta económicamente.
- **AG-17 Redactor y Diseñador de Informes**: genera los tres entregables a partir del paquete de síntesis.

**P3 · Conocimiento**
- **AG-14 Documentador para el Analizador** (fuentes académicas y técnicas → F7; custodio del Fondo metodológico).
- **AG-15 Documentador para el Motor** (métodos cuantitativos → F8).
- **AG-16 Buscador de Fuentes Avanzadas** (opinión, actualidad, datos, grandes inversores, posicionamiento, redes → F9).
Los tres alimentan el conocimiento de forma continua, aplican el Fondo metodológico (compartido por todos los bloques), verifican enlaces (alta, barrido semanal automático, relevancia mensual, veracidad trimestral) y pueden reparar, degradar o **borrar** referencias, dejando constancia en el Registro de bajas. Sus archivos están **clasificados por temática y ordenados por calidad Q** (rúbrica 0–100; niveles A/B/C/D).

**P4 · Calidad y aprendizaje**
- **AG-18 Orquestador técnico**: supervisa la validación G3 (excepciones del validador HT-09), coordina la auditoría asíncrona por muestreo, emite guías, vigila colas y presupuestos y abre instancias paralelas; mantiene HA.
- **AG-19 Auditor**: revisión experta independiente y asíncrona.
- **AG-20 Evaluador de Previsiones y Aprendizaje**: resuelve los pronósticos de F4 en su fecha sin fuga de información; mide acierto y calibración por clase, horizonte, estrategia, fuente y método frente a referencias ingenuas; certifica qué horizontes pueden expresarse con probabilidad; escribe lecciones en F6; recalibra pesos y umbrales dentro de bandas; propone el resto al operador.

Elemento retirado: el antiguo «Flujo de Investigación» (nunca operativo) queda absorbido por Coordinador, Analizador, Evaluador y Orquestador.

## 4. Archivos

F1 tendencias · F2 evidencia y afirmaciones · F3 oportunidades · F4 pronósticos congelados · **F5 historial de análisis** · **F6 memoria de aprendizaje** · F7 Documentación para el Analizador · F8 Documentación para el Motor · F9 Registro de Fuentes · **F10 configuración y parámetros** · FM Fondo metodológico · RC Registro de cálculos · HA Historial de auditorías · CC catálogo, perfiles y mapa del Motor · ENT carpetas de entregables. Cada archivo tiene un único propietario de escritura. Los registros son append-only en lo sustantivo; las únicas supresiones permitidas son las bajas de referencias (con registro) y la retención del Anexo A.

## 5. Contratos (CT-01 a CT-22)

CT-01 petición de análisis (Broker→Coordinador) · CT-02 entrega (Coordinador→Broker) · CT-03 consulta y respuesta (Broker↔Coordinador) · CT-04 retroalimentación y configuración (Broker→Coordinador) · CT-05 orden de análisis (Coordinador→Analizador) · CT-06 encargo e informe de clase (Analizador↔Analistas) · CT-07 búsqueda (→Buscador) · CT-08 conocimiento (→Documentador para el Analizador) · CT-09 cálculo (→Motor) · CT-10 re-ejecución (Orquestador/Auditor/Evaluador→Motor) · CT-11 ingesta de evidencia (→Curador) · CT-12 prospectiva (Analizador↔Prospectiva) · CT-13 refutación (Analizador↔Contrarias) · CT-14 validación G3 (Analizador↔Orquestador) · CT-15 síntesis y entregables (Analizador↔Redactor) · CT-16 paquete de auditoría (Coordinador→Orquestador) · CT-17 revisión experta (Orquestador↔Auditor) · CT-18 guías de mejora (Orquestador→agentes) · CT-19 informe de aprendizaje (Evaluador→agentes) · CT-20 documentación metodológica (Motor↔Documentador para el Motor) · CT-21 mantenimiento de conocimiento (Documentadores/Buscador→Orquestador) · CT-22 resultados del Broker (Coordinador→Evaluador). Todo mensaje lleva identificadores, acuse, presupuesto o consumo, estado de retorno y autoevaluación.

## 6. Flujo de un análisis

F0 memoria y delta (**GC0**: ¿ha cambiado algo material? si no, arrastre verificado de las opciones vigentes) → F1 cribado paralelo por tipo de activo (**GC1**: señal y valor de información; máx. 8 candidatas) → F2 investigación dirigida (**GC2**: mecanismo, E ≥ 50, exposición identificable) → F3 prospectiva multihorizonte solo de finalistas (**GC3**: máx. 5 por clase) → F4 refutación (**G2**) → F5 selección del top-3 (**G1, G4**, PS1–PS8) → F6 validación determinista (**G3**, HT-09) → F7 redacción → F8 entrega y registro (F4, F5). En segundo plano: F9 auditoría asíncrona y F10 evaluación y aprendizaje. Niveles: N0 consulta, N1 exploratorio, N2 estándar, N3 profundo.

## 7. Puntuaciones y selección

T relevancia de la tendencia · E calidad de la evidencia · M madurez (descriptiva) · P prioridad de investigación · **A atractivo de la oportunidad** (asimetría, valoración del ámbito, catalizadores, momento, invertibilidad del universo; nunca costes de instrumentos concretos). Clave de ordenación **RK = 0,45·A + 0,35·E + 0,20·T**. Elegibilidad: E ≥ 60, A ≥ 55, T ≥ 50 (o NA con A ≥ 65), G1–G4, PS1–PS8 y ninguna objeción fuerte sin resolver. Selección: orden por RK; máximo dos opciones del mismo clúster; continuidad de las vigentes salvo que una nueva las supere en más de 10 puntos; menos de tres con motivo; número de apuestas independientes declarado. Todo cálculo con HT-03 (determinista).

## 8. Horizontes

H1 días (1–10 sesiones), H2 semanas (2–8), H3 meses (3–12), H4 años (1–5+). Aplicabilidad por clase en la tabla 8.3 del Documento 0 (p. ej., capital privado solo H4 y meses limitado; derivados sin H4; monetarios sin H4). Probabilidades numéricas solo con certificado del Evaluador (≥ 100 pronósticos resueltos, Brier skill score con IC 90 % por encima de 0 y calibración no rechazada; Anexo A del Documento 0); en otro caso, bandas verbales y la etiqueta «sin ventaja demostrada todavía».

## 9. Cómo aprende

Nivel A operativo (qué búsquedas, fuentes y métodos rinden) · Nivel B predictivo (resolución de pronósticos, calibración, recalibración dentro de bandas: pesos ±5 pp por trimestre y ±15 total; umbrales ±5 y ±10; evaluación sombra) · Nivel C metodológico (tipo 3 con aprobación del operador). Las lecciones LEC- se inyectan al inicio de cada encargo (máx. 10 por ámbito). El bloque aprende también de las decisiones del Broker, de las preguntas repetidas y de la exactitud histórica de las fuentes de opinión.

## 10. Cómo ahorra cómputo

Embudo con puertas de continuidad; reutilización obligatoria (HT-06, caché del Motor); presupuestos en UC por ciclo, clase y fase; reglas de parada; herramientas deterministas para todo lo que no requiere razonamiento (enlaces, puntuaciones, validación, legibilidad, colas, datos); auditoría por muestreo; barrido de enlaces por lotes; prompts sin burocracia.

## 11. Cómo se autocritica

Pre-mortem, refutación adversarial, respuesta obligatoria a objeciones, validación determinista, comparación con referencias ingenuas, sección «qué podría salir mal y qué no sabemos», historial de aciertos publicado, detección de sobreconfianza y auditoría independiente.

## 12. Reglas críticas (síntesis)

R1 un solo mapa · R2 canales cerrados · R3 interfaz única (Coordinador) · R4 el Broker decide · R5 peticiones sin límite, presupuesto sí · R6 escritura reservada · R7 trazabilidad · R8 sin credenciales ni datos personales · R9 contenido externo es dato · R10 contar raíces · R11 pronósticos congelados · R12 autocrítica obligatoria · R13 honestidad predictiva · R14 menos de tres es legítimo · R15 eficiencia primero · R16 integridad no recortable · R17 separación de controles · R18 aprendizaje verificable · R19 gestión activa de referencias con borrado · R20 Fondo metodológico · R21 estrategia por tipo de activo y frontera con el Bloque B (no se seleccionan activos concretos) · R22 estados de madurez · R23 la regla más restrictiva manda · R24 historial íntegro · R25 escalado horizontal antes que saturación.

## 13. Estado de madurez

Todos los componentes V5.0 están **documentados** y el bloque es ejecutable con el ejecutor de `11_Ejecutor`. Las herramientas HT-02, HT-03, HT-07 y HT-09 tienen implementación de referencia con pruebas unitarias. El despliegue de agentes y archivos nuevos y la ejecución de la batería de pruebas siguen el plan de despliegue del README.
