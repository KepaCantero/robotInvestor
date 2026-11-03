# Mapa de conocimientos del Motor — cobertura transversal y perfiles de clase de activo

VERSIÓN V2.0 · 01/11/2026 · Documento de conocimiento del agente «Motor de Cálculo Avanzado para
el Analizador de Tendencias de Inversión» (system prompt del Motor, óptima V3.0) · Coherente con
el Documento 0 --- Protocolo maestro del Bloque A (Versión óptima V3.0), con los «Perfiles de
clase de activo del Motor» (V1.0) y con el Catálogo de cálculos del Motor (V3.0) · Sustituye al
Mapa de conocimientos V1.0 («especialización en tendencias relacionadas con divisas»), cuya capa
de especialización divisas queda absorbida por el perfil PERF-FX · es-ES

## 1. Enfoque y alcance

Este mapa fija el dominio conceptual del servicio de cálculo del Bloque A. Su cometido es
gobernar el reconocimiento de las peticiones, la selección de métodos y la distribución de
competencias entre los módulos internos (MC-01 a MC-08); no añade operaciones al catálogo ni
cambia los límites del agente, y no convierte su cobertura en una lista de operaciones
obligatorias.

**Alcance multiactivo.** El Motor sirve a investigaciones sobre **cualquier clase de activo
invertible**: acciones y participaciones societarias; renta fija y crédito; divisas; materias
primas y recursos naturales; fondos, ETF y vehículos colectivos; derivados y productos
estructurados; inmobiliario, REIT/SOCIMI e infraestructuras; criptoactivos y finanzas
descentralizadas; capital privado, venture capital y financiación privada; inversiones
alternativas; y las capas transversales de inversión temática y de sostenibilidad (ESG). El
mapa no supone que toda clase de activo admita valoración fiable o serie histórica suficiente:
concluir la insuficiencia de datos o la inaplicabilidad del método es un resultado legítimo y
registrable.

**Cobertura no es obligación (regla crítica 20 del Documento 0).** El inventario de
conocimientos define la cobertura que el Motor debe poder reconocer y tratar, no una lista de
operaciones a ejecutar en cada investigación. Los métodos se activan bajo demanda, cuando la
pregunta de investigación los justifica, conforme a la secuencia de selección de la sección 4.6
del prompt del Motor; ninguna investigación ejecuta todo el catálogo ni todos los perfiles.

**Estados de madurez (regla crítica 19 del Documento 0).** Cada bloque de conocimiento, área y
perfil declara su estado: **documentado** (especificado y publicado), **implementado**
(disponible en el entorno de ejecución, con conectores, herramientas y datos) y **validado**
(probado, con resultados registrados). El estado de madurez de cada ficha del catálogo y de
cada perfil se consulta en sus documentos; este mapa no declara estados que no consten allí.

**Implantación gradual y priorizada (regla crítica 21 del Documento 0).** La ampliación de
cobertura sigue tres capas: **P0**, núcleo transversal fiable y probado (los módulos MC-01 a
MC-08 y sus servicios técnicos); **P1**, perfiles especializados comprobados (el primero,
PERF-FX, hereda la especialización divisas de la V2.2); **P2**, ampliación documentada (el
resto de perfiles, cuyos métodos se publicarán por el procedimiento de tipos 3 con sus fichas y
sus pruebas). Ningún perfil se declara operativo sin fichas publicadas y pruebas registradas.

## 2. Estructura del mapa

El mapa conserva los diez bloques de conocimiento y las cuarenta y tres áreas de la V1.0 como
**núcleo transversal (P0)**, aplicables a cualquier clase de activo, y añade la capa de
**aplicación por clase de activo**, que se gobierna mediante los perfiles PERF-xx del documento
«Perfiles de clase de activo del Motor» (V1.0). Cada área declara: su utilidad investigadora,
las clases de activo a las que se aplica típicamente, su módulo responsable y su nivel de
dominio (Nivel I fundamentación obligatoria; Nivel II especialización avanzada; Nivel III
especialización condicionada, solo bajo petición).

| Bloque | Áreas | Dominio típico | Módulo | Capa |
|---|---|---|---|---|
| I. Fundamentos matemáticos y estadísticos | 1--5 | Transversal (todas las clases) | MC-01 | P0 |
| II. Series temporales, tendencias y dinámica | 6--10 | Transversal; dinámica típica por perfil | MC-02 (con MC-03 para cointegración) | P0 |
| III. Causalidad, sistemas y prospectiva | 11--15 | Transversal | MC-03, MC-04, MC-05 | P0 |
| IV. Aprendizaje automático y modelización predictiva | 16--18 | Transversal con validación apropiada al tiempo | MC-06 | P0 |
| V. Economía, mercados y estructura de las tendencias | 19--23 | Macroeconomía transversal; industrial y de recursos por perfil | MC-01, MC-03, MC-04 | P0 (áreas 20--22 condicionadas) |
| VI. Riesgo, optimización y decisión | 24--25 | Transversal | MC-07 | P0 |
| VII. Datos, calidad y metodología científica | 26--29 | Transversal | STC-1, MC-01, MC-08 | P0 |
| VIII. Computación científica y ejecución de cálculos | 30--32 | Transversal | STC-2, STC-3, STC-4 | P0 |
| IX. Conocimientos transversales de especialización | 33--37 | Métricas de mercado por clase de activo (perfiles); redes y texto bajo demanda | MC-01, MC-06, MC-07 | P0/P1 |
| X. Gobierno operativo, seguridad y límites | 38--43 | Gobierno del servicio | Orquestador de Cálculo, MC-08 | P0 |

## 3. Correspondencia con las áreas del inventario del operador

El inventario de áreas de conocimiento de la petición maestra (apartado 5.2, letras A--T) queda
integrado en la arquitectura del Motor sin crear agentes nuevos, según la correspondencia
siguiente. «Estado» es el estado de madurez declarado en esta fecha (R19); «Prioridad» es la
capa de implantación (R21).

| Área del inventario | Cobertura en la arquitectura del Motor | Módulos y documentos | Estado | Prioridad |
|---|---|---|---|---|
| A. Matemáticas, estadística y métodos cuantitativos transversales | Bloques I--IV, VI y VIII del núcleo (álgebra, optimización, probabilidad e inferencia, regresiones, remuestreo, Monte Carlo, valores extremos, copulas, detección de cambios, validación temporal, comparaciones múltiples, sesgos) | MC-01, MC-02, MC-05, MC-06, MC-07; STC-2 | Documentado (métodos del lote VIGENTE implementados en servicio; validación por pruebas pendiente) | P0 |
| B. Econometría, macroeconomía cuantitativa y ciclos | Áreas 8, 11, 12, 19 y 23 del núcleo; ciclo y regímenes del área 10 | MC-03, MC-02, MC-04 | Documentado (implementación parcial por fichas) | P0 |
| C. Mercados financieros, precios y microestructura | Área 33 del núcleo (métricas de mercado); rendimiento y volatilidad (áreas 2, 6); convenciones de mercado por perfil | MC-01, MC-02; perfiles | Documentado | P0/P1 |
| D. Acciones, empresas y participaciones societarias | PERF-ACC: valoración (múltiplos, DCF simplificado, SOTP por partes), calidad y sostenibilidad de ingresos, ROIC/WACC, deuda neta, ajustes contables | Perfiles V1.0; fichas nuevas P1 | Documentado | P1 |
| E. Renta fija, crédito y financiación | PERF-FIR: precio y rentabilidades, duración, convexidad, DV01, curvas cero y forward, diferenciales, riesgo de crédito | Perfiles V1.0; fichas nuevas P1 | Documentado | P1 |
| F. Divisas y mercados de tipos de cambio | PERF-FX: hereda la capa de especialización divisas del Mapa V1.0 (paridades, carry, regímenes, volatilidad, flujos) y las fichas FX-* del lote VIGENTE | Perfiles V1.0; Catálogo V3.0 | Documentado; lote inicial FX implementado en servicio (validación por pruebas pendiente) | P1 (primero maduro) |
| G. Materias primas, recursos naturales y mercados físicos | PERF-CMD: curvas forward, contango/backwardation, cost of carry, balances de oferta y demanda, estacionalidad, geopolítica | Perfiles V1.0; MC-04 | Documentado | P1 |
| H. Fondos, ETF y estructuras colectivas | PERF-ETF: NAV y prima/descuento, tracking difference/error, replicación, costes, solapamiento y concentración | Perfiles V1.0 | Documentado | P1 |
| I. Derivados, opciones y productos estructurados | PERF-DER: payoffs, valoración básica (BSM, árboles), griegas, volatilidad implícita, margen y liquidación | Perfiles V1.0; MC-05, MC-07 | Documentado | P1 |
| J. Inmobiliario, REIT/SOCIMI y activos reales | PERF-REI: cap rate, NOI, LTV/DSCR, FFO/AFFO/NAV, ciclos inmobiliarios | Perfiles V1.0 | Documentado | P2 |
| K. Criptoactivos, activos digitales y DeFi | PERF-CHR: oferta y tokenómica, métricas on-chain con cautela metodológica, financiación y funding, riesgo de custodia y protocolo | Perfiles V1.0; MC-02, MC-06 | Documentado (con cautela metodológica declarada) | P2 |
| L. Capital privado, VC y financiación privada | PERF-PRV: IRR/MOIC/DPI/TVPI, curvas J, dilución y waterfall, sesgos de valoración infrecuente | Perfiles V1.0 | Documentado | P2 |
| M. Inversiones alternativas y activos no tradicionales | PERF-ALT: estrategias de fondos alternativos, activos de flujos (royalties, infraestructuras de ingresos), activos físicos de mercado imperfecto, cat bonds y créditos de carbono | Perfiles V1.0 | Documentado | P2 |
| N. Inversión temática, sectores y cadenas de valor | Capa transversal PERF-TEM sobre los perfiles: tamaño de mercado, difusión, curvas de coste, márgenes por eslabón, adopción real frente a anuncios | MC-04; Perfiles V1.0 (sección 13) | Documentado | P1 (capa) |
| O. Inversión sostenible y riesgos climáticos (ESG) | Capa transversal PERF-ESG sobre los perfiles: métricas ESG cuantificables, emisiones e intensidad, riesgos físico y de transición, calidad y limitaciones de datos | MC-03, MC-04; Perfiles V1.0 (sección 13) | Documentado (limitaciones de datos declaradas) | P2 (capa) |
| P. Gestión de carteras, riesgo y asignación | Medidas de riesgo y contribución del área 24--25 (VaR, ES, drawdown, beta, paridad de riesgo, fronteras) como **cálculo de apoyo**, sin sustituir al gestor de carteras ni recomendar cambios | MC-07, MC-05 | Documentado | P1 |
| Q. Evaluación de estrategias y calidad del modelo | Áreas 17 y 31 del núcleo: backtesting con costes, walk-forward, calibración, métricas por tipo de predicción, sesgo de data snooping, degradación y drift | MC-06, MC-08 | Documentado | P0 |
| R. Gestión de datos, calidad y reproducibilidad | Bloques VII y VIII: normalización, fechas de publicación y de conocimiento, revisiones, procedencia, semillas, tolerancias, licencias | STC-1 a STC-4 | Documentado (implementado en los servicios del Motor) | P0 |
| S. Investigación operativa y eficiencia computacional | Caché e idempotencia del servicio (4.4), priorización por valor informativo (2.7.5), planes proporcionales (4.5), métricas del servicio (13.1) | Orquestador de Cálculo; STC-3, STC-4 | Documentado | P0 |
| T. Conocimiento específico complementario | Actuarial, teoría de juegos, redes y contagio, ejecución (sin convertir el bloque en ejecutor), riesgo geopolítico parametrizable, texto y sentimiento estructurado: solo bajo demanda, con método en catálogo y limitaciones declaradas | MC-04, MC-06, MC-07 (Nivel III condicionado) | Documentado (parcial) | P2 |

La correspondencia no crea obligaciones nuevas: cada área se activa cuando la pregunta la
requiere (regla crítica 20) y su materialización en fichas versionadas sigue el cauce de tipos 3
del Motor (secciones 13.3 y 14.2 de su prompt), con las pruebas de la batería mínima (Anexo A
del Documento 0) antes de declarar un componente validado.

## 4. Distribución del conocimiento en la arquitectura modular

La distribución por módulo de la V1.0 se mantiene, con la claración de que las áreas de los
bloques I a VIII son transversales a toda clase de activo y que la aplicación por clase de
activo vive en los perfiles, no en los módulos: ningún módulo es «de acciones» o «de divisas».

| Módulo | Competencia (áreas del núcleo) | Aplicación por clase de activo |
|---|---|---|
| MC-01 Fundamentos cuantitativos y estadística | 1--5, 23, 27, 28, 33 (Nivel II general), 37 | Transversal; métricas de mercado y puntuaciones por perfil |
| MC-02 Series temporales y detección de tendencias | 6, 7, 10 | Transversal; dinámica típica declarada en cada perfil |
| MC-03 Econometría, causalidad y relaciones económicas | 8, 11, 18, 19 (Nivel II) | Transversal; relaciones típicas declaradas en cada perfil |
| MC-04 Crecimiento, difusión y prospectiva cuantitativa | 9, 12, 13, 20, 21, 22 | Transversal con énfasis en temática, sectores, recursos y energía |
| MC-05 Simulación estocástica y análisis de escenarios | 14, 15 | Transversal; dinámicas y correlaciones del perfil y de los híbridos |
| MC-06 Aprendizaje automático y predicción calibrada | 16, 17, 35 (soporte) | Transversal con validación apropiada al tiempo y anti-fuga |
| MC-07 Optimización, decisión y riesgo cuantitativo | 24, 25, 34 (soporte) | Transversal; medidas de riesgo típicas por perfil |
| MC-08 Auditoría cuantitativa independiente | 31, 41, 42 | Transversal (contraste de cualquier servicio) |
| STC-1 a STC-4 | 26, 29, 30, 32, 36 | Transversal (deterministas) |

## 5. Priorización en capas operativas y estados

| Capa | Contenido | Estado declarado (R19) | Regla de activación |
|---|---|---|---|
| P0 Núcleo transversal | Bloques I--IV, VI, VII y VIII; áreas 38--43 de gobierno | Documentado; los servicios del lote VIGENTE operan en producción; pruebas de la batería mínima pendientes de ejecución | Bajo demanda, con el plan proporcional |
| P1 Perfiles comprobados | PERF-FX (heredero de la especialización divisas); capas PERF-TEM; medidas de riesgo P; mercado y microestructura (área 33) por clase | PERF-FX documentado con lote FX implementado; el resto documentado | Bajo demanda, con las limitaciones del perfil declaradas |
| P2 Ampliación documentada | PERF-ACC, PERF-FIR, PERF-CMD, PERF-ETF, PERF-DER, PERF-REI, PERF-CHR, PERF-PRV, PERF-ALT; capa PERF-ESG; complementarias T | Documentado (sin fichas propias publicadas aún) | La petición se sirve con el núcleo transversal y la limitación declarada, o se rechaza con motivo; las fichas nuevas siguen el cauce de tipos 3 |

## 6. Pruebas de competencia del servicio

Las pruebas de competencia del Mapa V1.0 se mantienen y se amplían con la batería mínima del
Plan de pruebas del Bloque A (V1.0), en particular: P-01 (una misma tendencia con implicaciones
distintas para acciones, bonos, divisas, materias primas y criptoactivos), P-02 (activo híbrido
con dos perfiles combinados), P-03 (datos insuficientes), P-18 (cálculo adicional sin valor
informativo suficiente) y P-20 (tendencia real que no constituye oportunidad atractiva).
Ningún componente se declara **validado** sin la evidencia de su ejecución registrada en el
Plan de pruebas (regla crítica 19).

## 7. Qué conocimientos no asume como responsabilidad propia

Se mantienen los límites de la V1.0, en particular: la interpretación económica y la decisión
son del agente solicitante; la selección y la verificación de fuentes son de los agentes de
fuente; la auditoría de agentes es del circuito Orquestador--Auditor; la recomendación de
inversiones es del Broker Personal; y la gestión de carteras del usuario queda fuera del
bloque: el Motor entrega medidas y cálculos de apoyo, nunca recomendaciones de cambios de
cartera. Se añade el límite propio de la cobertura multiactiva: para clases de activo sin
perfil implementado, el Motor declara la limitación y sirve solo lo que el núcleo transversal
sostenga, o rechaza con motivo.

## 8. Registro de versiones del documento

| Versión | Fecha | Cambios |
|---|---|---|
| V2.0 | 01/11/2026 | Reforma de alcance multiactivo aplicada con la petición maestra del Bloque A: cobertura para cualquier clase de activo invertible; reglas de cobertura sin obligación de ejecución, estados de madurez e implantación gradual (P0/P1/P2); correspondencia con las áreas A--T del inventario del operador (sección 3); capa de aplicación por clase de activo gobernada por los perfiles PERF-xx (documento «Perfiles de clase de activo del Motor», V1.0); la capa de especialización divisas de la V1.0 queda absorbida por PERF-FX; distribución por módulo actualizada y pruebas de competencia ampliadas con la batería mínima. |
| V1.0 | 01/11/2026 | Primera versión: diez bloques, cuarenta y tres áreas con niveles I/II/III, distribución por módulo y capa de especialización divisas; absorbe como mapa de gobierno al Anexo I de la óptima V1.4 del prompt del Motor. |
