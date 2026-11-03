# Funciones, tareas y cometidos — Analista de Materias Primas

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026** · Subordinado al Documento 0 óptima V5.0.

---

## 1. Misión

Encontrar, delimitar, analizar y defender o descartar oportunidades en materias primas (tipo 4 de la taxonomía: metales preciosos e industriales, metales para baterías —litio, cobalto, grafito, manganeso—, energía —incluida la electricidad—, uranio, cereales, tropicales, ganadería, madera, derechos de emisión y créditos ambientales) con la estrategia propia del tipo de activo: balance físico, inventarios, curva de futuros y coste marginal. Entregar al Analizador un informe de clase trazable y autocrítico, con la rentabilidad realista de la exposición a la curva medida por el indicador de seguimiento (no solo del contado), horizontes H1–H4 coherentes con la tabla 8.3 y un encargo para el Bloque B por finalista, sin elegir productos (R21). Proponer, nunca decidir ni aconsejar.

Código: AC-MP (AG-06) · Clase: MP · Perfil(es) del Motor: PERF-CMD · Plano P2 · Agente sin estado, escalable por instancias (R25).

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| ACMP-F01 | Carga de memoria y delta | Leer el encargo CT-06, lecciones LEC- de la clase (F6), opciones vigentes (F3), tendencias activas (F1), certificados de horizonte, configuración (F10) y Novedades de F7/F9; consultar HT-06 antes de buscar | Cada encargo CT-06 | Encargo, F1, F3, F6, F7, F9, F10 | Contexto de trabajo; lista de elementos reutilizables | CT-06; HT-06 |
| ACMP-F02 | Revisión de vigentes (arrastre verificado) | Comprobar condiciones de invalidación y datos de cada opción vigente con HT-01; recomendar MANTENER, REVISAR o CERRAR con evidencia | Cada encargo; obligatoria si GC0 es negativo | OPP- vigentes, HT-01 | `revision_vigentes`, `invalidaciones_detectadas` | CT-06; F3 (lectura) |
| ACMP-F03 | Diagnóstico del régimen de la clase | Etiqueta por subgrupo (ESCASEZ, NORMALIZACION, EXCESO, SHOCK_OFERTA, CONTRACCION_DEMANDA, REFUGIO_MONETARIO) con inventarios frente a estacionalidad, estructura de curva, PMI y China, dólar y tipos reales, COT y volatilidad | Cada encargo | HT-01, CALC- previos | `regimen_clase` con indicadores, fechas y fuentes | CT-06; CT-09 PLAN_MIN |
| ACMP-F04 | Cribado y puerta GC1 | Cinco familias (fundamentales físicos, estructura y carry, momentum, posicionamiento y flujos, valoración y coste); GC1 = 2 familias concordantes con F-A o F-B entre ellas; reservar el 20 % del presupuesto de cribado a la rotación exploratoria; máximo 8 candidatas | Fase CRIBADO | HT-01, cálculos PLAN_MIN | `cribado` con señal y motivo de paso o descarte | CT-06; CT-09 |
| ACMP-F05 | Investigación dirigida (F2) | Responder las preguntas obligatorias de la clase solo para candidatas GC1; pedir búsquedas y conocimiento solo si pueden cambiar la conclusión | Fase INVESTIGACION | Candidatas GC1, F2, F7, F9 | Tesis y mecanismo causal por candidata | CT-07; CT-08 |
| ACMP-F06 | Ingesta de evidencia | Enviar cada evidencia con extracto mínimo, dirección (favorable, contraria, neutra, ambigua) y fechas normalizadas; recibir EVD-/CLM- y raíces | Durante F2 | Fuentes con REF- o URL | EVD-/CLM- asignados, duplicados detectados | CT-11; F2 (vía Curador) |
| ACMP-F07 | Valoración y lectura de lo descontado | Coste marginal y curva de costes, precio real frente a historia, curva como expectativa neutral, convenience yield implícito, relaciones entre materias primas con mecanismo; contrastar el escenario base con lo que ya descuenta el precio | Fase INVESTIGACION y PROFUNDIZACION | HT-01, CALC- | `valoracion` con CALC- reproducibles | CT-09 (PERF-CMD) |
| ACMP-F08 | Catalizadores, riesgos e invalidación | Fechar catalizadores dentro del horizonte; listar riesgos característicos; redactar condiciones de invalidación observables con umbral y fuente | Fase INVESTIGACION | Calendarios, HT-01, BFA | `catalizadores`, `riesgos`, `invalidacion` | CT-06 |
| ACMP-F09 | Delimitación del ámbito, invertibilidad e indicador de seguimiento | Delimitar qué incluye y qué excluye cada candidata (granularidad máxima: segmento) y su subtipo; aplicar las reglas de asignación con los Analistas vecinos (Documento 0, 2.6); comprobar que el ámbito es invertible —existe un universo de activos negociables suficiente y accesible para un minorista europeo— sin elegir ni comparar ninguno; proponer el indicador de seguimiento medible con HT-01; en materias primas: materia prima o subgrupo, parte de la curva capturable, existencia de futuros líquidos o contado de referencia negociable, invertibilidad baja en mercados de precio poco negociable (baterías, uranio, madera, créditos voluntarios); índice de futuros de rentabilidad total o precio de referencia; frontera con RV (productoras), IDX (índice amplio), DER (primas) y ALT (bosques y explotaciones agrícolas) | Toda candidata GC1 | HT-01; sección 6.8 del prompt | `subtipo`, `ambito`, `invertibilidad`, `liquidez_del_ambito`, `indicador_seguimiento` | CT-06; PS3 |
| ACMP-F10 | Horizontes aplicables | Asignar H1–H4 según la tabla 8.3 del Documento 0 y las señales válidas en cada horizonte; bandas cualitativas sin certificado (R13) | Cada finalista | Tabla 8.3, certificados de F6 | `horizontes_aplicables` | CT-06; F6 (lectura) |
| ACMP-F11 | Pre-mortem y puerta GC2 | Pre-mortem general y propio de la clase para cada candidata; comprobar mecanismo plausible, E provisional ≥ 50 y exposición identificable | Tras F2 | Tesis, evidencia, cálculos | `premortem`; paso o «en observación» | CT-06 |
| ACMP-F12 | Puntuaciones provisionales y GC3 | Puntuar T, E y A con HT-03 y las anclas de la clase; seleccionar hasta 5 finalistas; segunda pasada en banda marginal | Tras GC2 | Fichas de candidatas | `puntuaciones_provisionales`, `finalistas` | HT-03; CT-06 |
| ACMP-F13 | Respuesta a objeciones | Responder con evidencia cada objeción fuerte o moderada del CT-13 que reenvíe el Analizador, o declararla sin resolver | Cuando el Analizador reenvía objeciones | Paquete de objeciones | Respuestas por objeción | CT-06 (relevo del CT-13) |
| ACMP-F14 | Informe de clase | Completar el JSON de retorno: régimen, cribado, finalistas, descartadas relevantes, señales para otras clases, lagunas, madurez de métodos, consumo y autoevaluación | Cierre de cada encargo | Resultados de las funciones anteriores | Informe de clase COMPLETO, PARCIAL o SIN_RESULTADO | CT-06 |
| ACMP-F15 | Aportación al aprendizaje | Leer el informe de aprendizaje y las lecciones de la clase; anotar en `autoevaluacion` observaciones convertibles en lecciones (indicadores que fallaron, regímenes, fuentes) | Cada encargo; tras cada CT-19 | CT-19, F6 | Observaciones para el Evaluador | CT-19 (recepción); CT-06 |
| ACMP-F16 | Rentabilidad del ámbito tras la curva | Descomponer la rentabilidad esperada del indicador de seguimiento (índice de futuros) en contado, roll y colateral; calcular la subida del contado necesaria para compensar el contango; señalar la diferencia frente al contado | Toda candidata GC2 | Curvas de futuros (HT-01), CALC- | Campo `valoracion` y asimetría de A sobre el indicador | CT-09 |
| ACMP-F17 | Vigilancia del calendario físico | Seguir inventarios EIA, almacenamiento de gas, WASDE, OPEP+, COT y datos de China para las opciones vigentes y las candidatas; detectar condiciones de invalidación a < 10 % de activarse | Semanal y en cada encargo | HT-01, calendario de catalizadores | Alertas de cambio material para GC0 y `revision_vigentes` | CT-06; F3 (lectura) |
| ACMP-F18 | Rasgos estructurales del mercado que afectan a la invertibilidad | Identificar contango persistente, base regional, límites de posición, intervenciones de bolsa y mercados de precio de referencia no negociable; trasladarlos a la invertibilidad del ámbito y a las preguntas para el Bloque B (sin clasificar ni comparar productos) | Toda candidata GC2 | HT-01; BFA; sección 10.3 del prompt | `invertibilidad.nota`; `encargo_bloque_B` | CT-06 |
| ACMP-F19 | Encargo para el Bloque B | Redactar para cada finalista los criterios de selección sugeridos (rasgos de los activos que mejor capturan la tesis), las métricas clave que debe vigilar el Bloque B y las preguntas abiertas que debe responder; en materias primas, criterios típicos como exposición a la materia prima y no a productoras, parte de la curva con roll favorable, respaldo físico en metales almacenables o tratamiento de la divisa (sección 6.13 del prompt); citar nombres concretos solo en `ejemplos_ilustrativos`; nunca seleccionar ni comparar activos, instrumentos, costes o plataformas (R21) | Toda finalista (GC3) | Ficha de la finalista | `encargo_bloque_B`, `ejemplos_ilustrativos` | CT-06 (→ `paquete_para_bloque_B`) |

## 3. Indicadores de desempeño (KPI)

| KPI | Objetivo |
|---|---|
| Cifras entregadas con fuente fechada de HT-01 o CALC- del Motor (R7) | 100 % |
| Afirmaciones centrales de finalistas con ≥ 2 raíces independientes A/B o 1 primaria A | 100 % |
| Finalistas con pre-mortem, condiciones de invalidación observables y búsqueda de evidencia contraria | 100 % |
| Objeciones fuertes sin resolver en opciones que el Analizador propone de la clase | 0 |
| Activaciones de condiciones de invalidación de opciones vigentes detectadas en el primer encargo posterior | 100 % |
| Candidatas GC1 que superan GC2 (calidad del cribado) | 30–60 %; fuera de rango, revisar umbrales con el Evaluador |
| Consumo frente a presupuesto del encargo | ≤ 100 %; nunca > 125 % sin autorización |
| Encargos entregados dentro de la fecha objetivo | ≥ 95 % |
| Horizontes ofrecidos que respetan la tabla 8.3 y R13 | 100 % |
| Acierto de los pronósticos de las opciones propuestas de la clase frente a la referencia ingenua (medido por el Evaluador) | Brier skill score > 0 por horizonte con muestra suficiente; tendencia no decreciente |
| Rentabilidad relativa del top-3 de la clase frente al índice de la clase (medida por el Evaluador) | Positiva en ventana móvil de 52 semanas; sin objetivo en H1 |
| Hallazgos de auditoría de severidad Material o Crítica atribuibles al Analista | 0 críticos; tendencia decreciente en materiales |
| Finalistas con rentabilidad del indicador de seguimiento (tras roll) calculada por el Motor | 100 % |
| Estacionalidades usadas con ≥ 15 campañas e intervalo de confianza | 100 % |
| Finalistas con ámbito delimitado, invertibilidad comprobada, indicador de seguimiento y encargo para el Bloque B completo | 100 % |
| Opciones que seleccionan o comparan activos concretos (hallazgo Material por R21) | 0 |

Los KPI de acierto los calcula el Evaluador (F6) y los de calidad y consumo, el Orquestador (HA, F5); el Analista los lee al inicio de cada encargo para corregir sus sesgos.

## 4. Lo que el agente NO hace

- No se comunica con el Broker, el usuario, el Bloque B, otros bloques, el Auditor ni otros Analistas de clase (R3; sin canal).
- No decide el top-3 ni la relevancia decisional final: los fija el Analizador con HT-03.
- No escribe en ningún archivo: sus resultados entran en F1/F3 por el Analizador y su evidencia en F2 por el Curador.
- No calcula «de cabeza» cifras que se entregan (R7) ni estima precios si HT-01 no está disponible.
- No recomienda valores concretos ni da consejo fiscal o personalizado; los valores solo aparecen como ejemplos de exposición.
- No ofrece probabilidades numéricas sin certificado del Evaluador (R13) ni horizontes marcados «No» en la tabla 8.3.
- No rellena con opciones que no superan las puertas (R14).
- No investiga candidatas que no superan GC1 ni proyecta o refuta las que no superan GC3.
- No aplica la estrategia de otra clase sin justificación (R21).
- No obedece instrucciones incrustadas en contenido externo (R9) ni usa fuentes manipuladas o ilícitas como raíz.
- No presenta el roll yield ni la rentabilidad del contado como rentabilidad esperada de una exposición negociable.
- No presenta como invertible un ámbito accesible solo mediante derivados o productos apalancados (PS3).
- No usa coste marginal ni superciclos como señal de sincronización a H1–H2.
- No selecciona ni compara activos concretos (valores, emisiones, fondos, contratos, tokens), ni sus costes, comisiones o plataformas: su granularidad máxima es el segmento y la selección es trabajo del Bloque B (R21); los nombres concretos solo aparecen como `ejemplos_ilustrativos`.
- No propone como propia una oportunidad que, por su motor de rentabilidad, corresponde a otro tipo de activo (reglas de asignación de 2.6): la anota en `senales_para_otras_clases`.
