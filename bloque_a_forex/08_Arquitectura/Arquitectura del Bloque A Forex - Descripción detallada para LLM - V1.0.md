# Arquitectura del Bloque A Forex — Descripción detallada para LLM

**Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026 · actualizado V1.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque A Forex, versión óptima V1.1 (ante discrepancia, manda el Documento 0). Actualización V1.1: contratos CT-23 (consultas del bloque al Broker), CT-24 (encargo de seguimiento de opción, ciclo C6) y CT-25 (credenciales con la bóveda de HT-01); archivo F11; horizonte H5 «limitado» y horizonte principal; reglas R26 y R27. El diagrama (mismos nombres de archivo) está redibujado en V1.1.

## 0. Instrucciones de ingesta

Este texto describe, de forma cerrada y autosuficiente, la arquitectura del Bloque A Forex para que un modelo de lenguaje la entienda **y pueda regenerar su diagrama** sin leer el resto del paquete. Trátalo como descripción normativa de un sistema ya definido: no añadas agentes, canales, archivos ni herramientas que no figuren aquí (R1). Los identificadores (AG-, CT-, F1–F11, FM, RC, HA, CC, ENT, HT-, MC-, PERF-FX-, N0–N3, GC0–GC3, G1–G4, PS1–PS8, H1–H5, C1–C6, R1–R27, G10N, G10M, EMAS, EMLA, EMEA, ESTR, RUN-FX-, OPP-FX-, TND-FX-, PRG-FX-, HIT-FX-, CNS-FX-, SEG-FX-, CRD-FX-) son términos fijados y no se parafrasean. La imagen `Arquitectura del Bloque A Forex - V1.1.png` (y su SVG) representa lo mismo; la sección 14 da la especificación de maquetación para redibujarla.

## 1. Qué es el Bloque A Forex

Bloque de la arquitectura multiagente Robot Investor **especializado exclusivamente en divisas**, con **una sola función: encontrar oportunidades de inversión en el mercado de divisas** y responder a tres preguntas: **dónde** (un par, un cruce, una cesta, un bloque regional o temático, una estrategia cambiaria o un cambio de régimen), **por qué** (divergencia de política monetaria, diferencial de tipos y carry, desequilibrio frente al valor de equilibrio, flujos y posicionamiento, términos de intercambio, riesgo político, intervención) y **en qué horizonte** (días, semanas, meses o años).

- **Cliente único**: el **Broker Personal**, que gestiona la información de todos los bloques, es el único que habla con el usuario y decide (modo autónomo, manual o semiautónomo) si envía cada oportunidad al **Bloque B** o la descarta.
- **Frontera con el Bloque B (R21)**: el Bloque A Forex **no elige el instrumento** (contado, forward, futuro, opción, ETF/ETC, CFD), ni su proveedor, coste, apalancamiento, tamaño, cobertura o nivel de entrada; eso lo decide el Bloque B. Su granularidad máxima es el par, el cruce, la cesta o la estrategia. Puede citar la existencia de mercados (p. ej., «hay futuros y opciones líquidos sobre el par») solo para justificar la invertibilidad.
- **Relación con el Bloque A general**: el Bloque A general (doce tipos de activo, con un único Analista de divisas) sigue existiendo; el Bloque A Forex es su especialización profunda. **No se comunican**: el Broker decide a cuál dirige cada petición (por defecto, las de divisas al Bloque A Forex).
- **Notación**: pares en convención de mercado `BASE/COTIZADA` (EUR/USD = dólares por euro); la dirección se refiere siempre a la base (`ALCISTA_BASE` o `BAJISTA_BASE`); las cestas declaran composición, pesos y divisa de financiación.
- **Tipos de opción**: `PAR` (par principal con dirección), `CRUCE` (par sin USD), `CESTA`, `BLOQUE`, `ESTRATEGIA` (carry, valor, momentum, dólar amplio, refugio), `VOLATILIDAD` (nivel o estructura de la volatilidad cambiaria) y `REGIMEN` (ruptura o ajuste de un tipo fijo, una banda o un control de capitales).
- **Humildad frente al paseo aleatorio**: los tipos de cambio son difíciles de predecir (Meese y Rogoff, 1983); todo pronóstico se compara con el paseo aleatorio y, cuando procede, con el forward como predictor.

### 1.1 Los seis segmentos

| Código | Segmento | Universo | Analista | Perfil del Motor |
|---|---|---|---|---|
| G10N | G10 núcleo | USD, EUR, JPY, GBP, CHF: pares principales y cruces | AG-03 | PERF-FX-G10 |
| G10M | G10 de materias primas y escandinavas | AUD, NZD, CAD, NOK, SEK | AG-04 | PERF-FX-G10 |
| EMAS | Emergentes de Asia | CNY/CNH, INR, KRW, TWD, IDR, SGD, THB, MYR, PHP, VND; HKD (tipo fijo) | AG-05 | PERF-FX-EM |
| EMLA | Emergentes de Latinoamérica | BRL, MXN, CLP, COP, PEN; ARS y otras con controles como ámbitos de régimen | AG-06 | PERF-FX-EM |
| EMEA | Emergentes de Europa, Oriente Medio y África | PLN, HUF, CZK, RON, TRY, ZAR, ILS, EGP, NGN, KES, MAD; divisas del Golfo con tipo fijo | AG-07 | PERF-FX-EM |
| ESTR | Estrategias y cestas cambiarias | Carry, valor (PPA/BEER), momentum, dólar amplio, refugio, volatilidad, cestas regionales y temáticas | AG-08 | PERF-FX-FACT |

**Reglas de asignación** (sin duplicados): (1) un par entre divisas de segmentos distintos pertenece al de la divisa **menos líquida** (USD/MXN → EMLA; EUR/PLN → EMEA; AUD/JPY → G10M); (2) tres o más divisas o una regla sistemática → ESTR; (3) la volatilidad de un par pertenece al segmento del par, la de varias divisas a ESTR; (4) ante duda decide el Analizador y registra el motivo; **una oportunidad no puede estar en dos top-3**.

**Capas transversales**: política monetaria y macro (AG-09), posicionamiento, flujos y volatilidad (AG-21), geopolítica, sanciones y controles de capitales, y materias primas como determinante de los términos de intercambio.

## 2. Qué entrega

1. **Ciclo periódico** (semanal por defecto: ejecución el sábado tras el cierre de Nueva York, entrega el lunes a las 07:00 en la zona del usuario; configurable por el Broker): informe con **hasta 3 opciones por cada uno de los seis segmentos** (≤ 18). Si no hay tres que superen las puertas, se entregan las que haya (incluso cero) con explicación (R14).
2. **Peticiones ad hoc** del Broker, sin límite de número, y **consultas** sobre cualquier aspecto.
3. Por cada análisis, tres entregables (sección 10): **informe técnico** para el Broker; **informe visual y minimalista** para el usuario sin conocimientos financieros; **paquete JSON** de oportunidades con un **encargo preparado para el Bloque B** por opción.
4. Cada opción incluye `relevancia_decisional`, `reversibilidad`, `siguiente_paso_sugerido` y `que_cambiaria_la_conclusion` para que el Broker aplique su modo de decisión, y su `naturaleza_inversion` con el `horizonte_principal` coherente (V1.1).
5. **Seguimiento encargado de opción** (V1.1, CT-24, ciclo C6): si el Broker lo encarga, revisión ligera periódica de una opción que no envió al Bloque B, con un **informe de seguimiento de opción** breve + JSON (semáforo y recomendación: mantener vigilancia, proponer enviar a B, cerrar o proponer la cancelación). Nunca por iniciativa del bloque (R27).
6. **Consultas del bloque al Broker** (V1.1, CT-23) cuando una duda puede cambiar una conclusión, con supuesto declarado si no hay respuesta, y **solicitudes de credenciales** (CT-25) que el Broker deposita en la bóveda de HT-01.

## 3. Actores externos

| Actor | Relación con el bloque |
|---|---|
| **Usuario** | Nunca habla con el bloque; solo con el Broker |
| **Broker Personal** | Único interlocutor externo; habla solo con AG-01 (CT-01 a CT-04); decide enviar oportunidades al Bloque B |
| **Bloque B** | Recibe del Broker las oportunidades que este decida; elige instrumento, coste y cobertura; no habla con el Bloque A Forex |
| **Bloque A general** | Bloque hermano independiente; sin canal con el Bloque A Forex |
| **Operador humano** | Configura, aprueba cambios de tipo 3, recibe informes de gobernanza (vía AG-18) |
| **Fondo metodológico (FM)** | Archivo del ecosistema compartido por todos los bloques; lo custodia AG-14 en este bloque |

## 4. Agentes (21, en cuatro planos)

Columnas: código · nombre exacto (siglas) · cometido · escribe · contratos principales · estado (con o sin estado; las instancias paralelas solo se abren en agentes sin estado, R25).

### P1 · Interfaz y ciclo

| Código | Agente | Cometido | Escribe | Contratos | Estado |
|---|---|---|---|---|---|
| AG-01 | **Coordinador de Peticiones y Consultas** (COORD) | Única interfaz con el Broker; programa el ciclo (HT-05); clasifica, encola y prioriza peticiones; asigna nivel N0–N3 y presupuesto; responde consultas N0 desde la memoria; entrega; envía el paquete de auditoría; avisa al Evaluador de las decisiones del Broker; **V1.1**: envía las consultas del bloque (CT-23), solicita credenciales (CT-25) y gestiona los encargos de seguimiento (CT-24, F11, ciclos C6) | F5; F10 (parámetros de servicio y limitaciones por credenciales); F11 | CT-01, CT-02, CT-03, CT-04, CT-23, CT-24, CT-25 (con el Broker); CT-05 (→ AG-02); CT-16 (→ AG-18); CT-22 (→ AG-20) | Con estado (instancia única) |

### P2 · Análisis

| Código | Agente | Cometido | Escribe | Contratos | Estado |
|---|---|---|---|---|---|
| AG-02 | **Analizador de Oportunidades en Divisas** (ANZ, director) | Plan y reparto por segmentos; encarga primero las capas transversales y reparte sus informes; coordina a los seis Analistas de segmento; asigna segmento sin duplicados; integra y resuelve conflictos entre segmentos (exposición común al dólar, al yen o al riesgo global; contradicciones); calcula la **exposición agregada por divisa** y las apuestas independientes; selecciona el top-3 por segmento con HT-03; gestiona prospectiva, refutación, G3 y redacción | F1, F3 | CT-05 (← AG-01); CT-06 (↔ AG-03…AG-08); CT-06T (↔ AG-09, AG-21); CT-07, CT-08, CT-09; CT-12 (↔ AG-10); CT-13 (↔ AG-11); CT-14 (↔ AG-18); CT-15 (↔ AG-17). V1.1: filtra y agrupa las dudas para el Broker (CT-23) y eleva las solicitudes de credenciales (CT-25) en el retorno parcial del CT-05; confirma naturaleza y horizonte principal; dirige los ciclos C6 | Con estado |
| AG-03 | **Analista de G10 núcleo** (AS-G10N) | Segmento G10N: divergencia Fed/BCE/BoJ/BoE/BNS, diferencial a 2 años, tipos reales, *dollar smile*, refugio, flujos de cobertura | — | CT-06; CT-07, CT-08, CT-09, CT-11 | Sin estado |
| AG-04 | **Analista de G10 de materias primas y escandinavas** (AS-G10M) | Segmento G10M: términos de intercambio, demanda china, carry, RBA/RBNZ/BoC/Norges Bank/Riksbank, liquidez de las coronas | — | Ídem | Sin estado |
| AG-05 | **Analista de Divisas Emergentes de Asia** (AS-EMAS) | Segmento EMAS: gestión y fijación diaria del CNY, diferencial CNH–CNY, semiconductores, flujos e índices de bonos, intervención, NDF | — | Ídem | Sin estado |
| AG-06 | **Analista de Divisas Emergentes de Latinoamérica** (AS-EMLA) | Segmento EMLA: carry alto y sensibilidad al riesgo, cobre y petróleo, riesgo fiscal y político, remesas y nearshoring, controles (ARS) | — | Ídem | Sin estado |
| AG-07 | **Analista de Divisas Emergentes de EMEA** (AS-EMEA) | Segmento EMEA: convergencia con el euro, ortodoxia monetaria (TRY), minería (ZAR), tipos fijos del Golfo, rupturas de tipos fijos (EGP, NGN) | — | Ídem | Sin estado |
| AG-08 | **Analista de Estrategias y Cestas Cambiarias** (AS-ESTR) | Segmento ESTR: primas de carry, valor, momentum y dólar; régimen de volatilidad; *crowding*; cestas regionales y de refugio | — | Ídem | Sin estado |
| AG-09 | **Analista de Bancos Centrales y Macro Cambiaria** (TR-BCM, transversal) | Informe transversal de política monetaria y macro por ciclo: senda descontada de cada banco central, sorpresas y cambios de tono, diferenciales nominales y reales, calendario, régimen global, balanza de pagos, riesgos de intervención. **No propone opciones** | — | CT-06T (↔ AG-02); CT-07, CT-08, CT-09, CT-11 | Sin estado |
| AG-21 | **Analista de Posicionamiento, Flujos y Volatilidad Cambiaria** (TR-PFV, transversal) | Informe transversal de posicionamiento (CFTC/COT, encuestas), flujos de cartera, cobertura, estacionales y de fin de mes, *crowding*, volatilidad implícita y realizada, *risk reversals*, estructura de plazos y base cruzada. **No propone opciones** | — | Ídem | Sin estado |
| AG-10 | **Analista de Prospectiva y Horizontes** (PROS) | Escenarios y pronósticos por horizonte (H1–H5; H5 «limitado», cualitativo y con hitos HIT-FX-) de las finalistas, siempre frente al paseo aleatorio y al forward; formula los PRG-FX- y los da de alta en F4 tras G3 | F4 (altas) | CT-12 (↔ AG-02); CT-07, CT-08, CT-09, CT-11 | Varias instancias |
| AG-11 | **Analista de hipótesis contrarias** (CONTRA) | Refutación adversarial con objeciones graduadas; examina lo que ya descuentan el forward y el posicionamiento, el riesgo de intervención y la fragilidad del carry | — | CT-13 (↔ AG-02); CT-08; CT-11 | Varias instancias |
| AG-12 | **Curador de Evidencia** (CUR) | Deduplica, identifica raíces independientes, normaliza fechas (conocibilidad), convenciones de cotización y unidades; publica alertas de procedencia | F2 | CT-11 (← Analistas, Buscador, Documentadores, Prospectiva, Contrarias) | Sin estado (escritura serializada) |
| AG-13 | **Motor de Cálculo Avanzado (Forex)** (MOTOR) | Cálculo reproducible con artefacto (CT-09) y re-ejecución independiente (CT-10); núcleo transversal, perfiles PERF-FX-G10, PERF-FX-EM y PERF-FX-FACT y módulos MC-01 a MC-10 (sección 5). No interpreta económicamente | RC | CT-09 (←), CT-10 (←), CT-20 (↔ AG-15) | Sin estado |
| AG-17 | **Redactor y Diseñador de Informes** (RED) | Genera los tres entregables a partir del paquete de síntesis y, en cada ciclo C6, el informe de seguimiento de opción; controla la legibilidad (HT-07) y los gráficos (HT-04) | ENT (genera) | CT-15 (↔ AG-02) | Sin estado |

### P3 · Conocimiento

| Código | Agente | Cometido | Escribe | Contratos | Estado |
|---|---|---|---|---|---|
| AG-14 | **Documentador para el Analizador** (DOC-A) | Literatura académica y técnica sobre divisas (áreas TX-01 a TX-14); custodio del Fondo metodológico en el bloque | F7; FM (custodio) | CT-08 (←), CT-11 (→), CT-21 (→ AG-18) | Sin estado |
| AG-15 | **Documentador para el Motor de Cálculo Avanzado** (DOC-M) | Métodos cuantitativos para divisas (áreas TMX-01 a TMX-09) | F8 | CT-20 (↔ AG-13), CT-11, CT-21 | Sin estado |
| AG-16 | **Buscador de Fuentes Avanzadas** (BFA) | Fuentes cambiarias (áreas TFX-01 a TFX-10): bancos centrales, COFER, encuesta trienal del BPI, balanza de pagos y reservas, CFTC, tipos de referencia, volatilidad, prensa y análisis de divisas, calendarios y fijaciones; mide la fiabilidad de las fuentes de opinión; V1.1: envía al Coordinador las solicitudes de credenciales de fuentes de pago o API (CT-25 en origen) | F9 | CT-07 (←), CT-11, CT-21, CT-25 (→ AG-01) | Sin estado |

Los tres alimentan el conocimiento de forma continua (ciclo C4), aplican el Fondo metodológico (R20), verifican enlaces (alta, barrido semanal automático con HT-02, relevancia mensual, veracidad trimestral) y pueden **reparar, degradar o borrar** referencias, dejando una línea en el «Registro de bajas» (R19). Sus archivos están clasificados por área temática y ordenados por calidad Q (0–100; niveles A/B/C/D). Publican cada semana una sección «Novedades» que los demás leen vía HT-06 (difusión sin canal nuevo).

### P4 · Calidad y aprendizaje

| Código | Agente | Cometido | Escribe | Contratos | Estado |
|---|---|---|---|---|---|
| AG-18 | **Orquestador técnico** (ORQ) | Dictamina las excepciones de G3 (CT-14 + HT-09); coordina la auditoría asíncrona por muestreo; emite guías (CT-18); vigila colas, consumo y presupuestos; abre y cierra instancias (R25); gestiona la cola de tipo 3 y el informe al operador | HA | CT-14, CT-16, CT-17, CT-18, CT-21 (←), CT-10 (→ Motor) | Con estado |
| AG-19 | **Auditor** (AUD) | Revisión experta independiente y asíncrona por muestreo de riesgo (sesgos, R1–R27, estrategia por segmento, frontera con el Bloque B, honestidad frente al paseo aleatorio) | — | CT-17 (↔ AG-18), CT-10 | Con estado |
| AG-20 | **Evaluador de Previsiones y Aprendizaje** (EVAL) | Resuelve F4 en su fecha sin fuga (con la fijación pactada); mide acierto y calibración por segmento, horizonte, estrategia y fuente frente al paseo aleatorio y al forward; certifica horizontes (R13); evalúa los pronósticos H5 por sus hitos; escribe lecciones; recalibra dentro de bandas; propone el resto al operador | F6; F4 (solo resolución); F10 (parámetros calibrables) | CT-19 (→ COORD, ANZ, Analistas, PROS, BFA, ORQ); CT-22 (←); CT-09, CT-10 | Con estado |

## 5. Motor: perfiles y módulos internos (no son agentes)

**Perfiles**: PERF-FX-G10 (G10N y G10M), PERF-FX-EM (EMAS, EMLA y EMEA), PERF-FX-FACT (ESTR); el núcleo TRANSVERSAL sirve también a AG-09 y AG-21.

| Módulo | Dominio (con énfasis cambiario) |
|---|---|
| MC-01 | Fundamentos cuantitativos y cálculo financiero cambiario: convenciones de cotización, puntos forward, rentabilidad total con carry, cruces sintéticos |
| MC-02 | Series temporales, tendencias, regímenes y volatilidad de tipos de cambio (GARCH, cambios de régimen, volatilidad realizada) |
| MC-03 | Econometría, causalidad y macro cuantitativa: CIP/UIP, PPA, BEER, FEER, reglas de Taylor, sorpresas |
| MC-04 | Prospectiva cuantitativa: escenarios de política monetaria y su traslación al tipo de cambio |
| MC-05 | Simulación estocástica y escenarios, incluidos saltos y rupturas de tipos fijos |
| MC-06 | Aprendizaje automático y predicción calibrada para divisas |
| MC-07 | Optimización, decisión y riesgo: carteras de factores cambiarios y riesgo de cola del carry |
| MC-08 | Auditoría cuantitativa independiente (CT-10) |
| MC-09 | Valoración cambiaria y precios de opciones: PPA, BEER, REER, factores, Garman-Kohlhagen, superficie de volatilidad, *risk reversals*, base cruzada |
| MC-10 | Evaluación predictiva y backtesting: Brier, log-score, calibración, Diebold-Mariano y Clark-West frente al **paseo aleatorio**, backtesting sin sesgos |

## 6. Archivos

| Código | Archivo | Escribe | Leen |
|---|---|---|---|
| F1 | Registro maestro de tendencias (TND-FX-) | AG-02 | Plano P2, AG-14, AG-15, AG-16, ORQ, AUD, EVAL, COORD |
| F2 | Registro de evidencia y afirmaciones (EVD-, CLM-) | AG-12 | Plano P2, COORD, ORQ, AUD, EVAL |
| F3 | Registro de oportunidades (OPP-FX-) | AG-02 | P2, AG-14, AG-15, AG-16, COORD, ORQ, AUD, EVAL |
| F4 | Registro de pronósticos congelados (PRG-FX-) | AG-10 (altas); AG-20 (resolución) | Todos |
| F5 | Historial de análisis (RUN-FX-, QRY-, RET-; incluye los informes transversales de cada ciclo; V1.1: CNS-FX- consultas al Broker, CRD-FX- solicitudes de credenciales sin valores, RUN-FX- de tipo SEGUIMIENTO) | AG-01 | Todos |
| F6 | Memoria de aprendizaje (LEC-, MET-, CERT-, AJU-, HAC-) | AG-20 | Todos (extracto por ámbito) |
| F7 | Documentación para el Analizador de Oportunidades en Divisas (TX-) | AG-14 | P2, AG-16, ORQ, AUD |
| F8 | Documentación para el Motor de Cálculo Avanzado (Forex) (TMX-) | AG-15 | AG-13, AG-14, AG-12, ORQ, AUD, EVAL |
| F9 | Registro de Fuentes para el Analizador de Oportunidades en Divisas (TFX-) | AG-16 | P2, AG-14, ORQ, AUD, EVAL |
| F10 | Configuración y parámetros del bloque (segmentos activos, divisa base del usuario, umbrales, pesos A FX, `methodology_version` FX-1.1; limitaciones de servicio por credenciales denegadas) | AG-01 (servicio y limitaciones); AG-20 (calibrables); operador (resto) | Todos |
| F11 | **Registro de seguimientos encargados** (V1.1; SEG-FX-: OPP-FX- objeto, frecuencia, señales de interés, fecha de fin, estado ACTIVO·PAUSADO·CANCELADO·FINALIZADO, historial; por ciclo C6: RUN-FX-, semáforo, recomendación, informe y respuesta del Broker) | AG-01 | AG-02, Analistas de segmento, AG-17, ORQ, AUD, EVAL; HT-05 |
| FM | Fondo metodológico bibliográfico (ecosistema) | AG-14 (custodio) | AG-14, AG-15, AG-16 y los Documentadores y Buscadores de todos los bloques |
| RC | Registro de cálculos del Motor (CALC-) | AG-13 | ORQ, AUD, EVAL, AG-15, COORD, AG-11, solicitantes |
| HA | Historial de auditorías (G3V-, AUD-, HAL-, GUI-, ORD-, P3-, INC-) | AG-18 | AG-18, AG-19, AG-20, AG-02 (extractos) |
| CC | Catálogo de cálculos, Perfiles cambiarios y Mapa de conocimientos del Motor | Operador (tipo 3); AG-13 propone | AG-13, AG-15, Analistas, ORQ |
| ENT | Carpetas de entregables (`AAAA-MM-DD_tipo_RUN-id`) | AG-17 (genera); AG-01 (publica) | Broker; ORQ y AUD |

Reglas: un único propietario de escritura por archivo (R6); F1–F6, F11, RC y HA son append-only en lo sustantivo; F7–F9 son bases vivas con borrado registrado; cualquier acceso fuera de matriz es una incidencia.

## 7. Herramientas deterministas (no son agentes)

| Código | Herramienta | Usuarios | Función |
|---|---|---|---|
| HT-01 | Servicio de datos de mercado y bóveda de credenciales | Analizador, Analistas, Motor, Evaluador, Prospectiva; Coordinador y BFA (solo estado de la bóveda) | Contado con fijación (BCE, Fed H.10, WM/Reuters), puntos forward, curvas, volatilidades implícitas, tipos efectivos (BPI), CFTC, reservas, macro; con fecha del dato y de recuperación. V1.1: custodia la **bóveda de credenciales** (el Broker deposita las claves por CT-25; los agentes solo ven alias y estado) |
| HT-02 | Verificador de enlaces y contenido | DOC-A, DOC-M, BFA, Curador | HTTP, DOI, muro de pago, hash, archivado, retractaciones |
| HT-03 | Calculadora de puntuaciones y ranking | Analizador, Analistas, Orquestador | T, E, M, P, A (pesos FX) y RK; top-3 por segmento |
| HT-04 | Generador de gráficos | Redactor | Gráficos de pares, mapa de divisas, semáforos e iconos; paleta accesible |
| HT-05 | Planificador | Coordinador | Ciclo periódico, ciclos C6 de cada encargo de F11, calendario de bancos centrales, vencimientos de las consultas CT-23, recordatorios de resolución, de hitos H5 y de credenciales |
| HT-06 | Índice y caché | Todos | Reutilización de evidencia, cálculos y respuestas; lectura de «Novedades» |
| HT-07 | Medidor de legibilidad | Redactor, Orquestador | Fernández-Huerta corregido, longitud de frases, jerga |
| HT-08 | Monitor de colas y consumo | Orquestador | Colas, tiempos, consumo e instancias |
| HT-09 | Validador determinista G3 | Analizador, Orquestador | Trazabilidad, artefactos, puntuaciones, puertas, horizontes por segmento, horizonte principal coherente con la naturaleza de la inversión, hitos de los pronósticos H5, supuestos declarados, ausencia de valores de credenciales, notación de pares, campos obligatorios y legibilidad; valida también el informe de seguimiento de opción |

## 8. Contratos (CT-01 a CT-25 y CT-06T)

| Código | Emisor → receptor | Objeto | Tipo |
|---|---|---|---|
| CT-01 | Broker → Coordinador | Petición de análisis (segmentos, divisas, pares, temáticas, horizontes, prioridad, profundidad) | Servicio |
| CT-02 | Coordinador → Broker | Entrega: informe técnico, informe visual y paquete JSON (con `paquete_para_bloque_B`) | Servicio |
| CT-03 | Broker ↔ Coordinador | Consulta y respuesta | Servicio |
| CT-04 | Broker → Coordinador | Retroalimentación y configuración: decisiones sobre opciones, utilidad, periodicidad, segmentos activos, divisa base, horizontes | Servicio |
| CT-05 | Coordinador → Analizador | Orden de análisis con nivel por segmento, presupuesto por segmento y presupuesto transversal; retorno: síntesis y estado | Servicio |
| CT-06 | Analizador ↔ Analistas de segmento (AG-03…AG-08) | Encargo por segmento (con los identificadores de los informes transversales del ciclo) e informe de segmento | Servicio |
| **CT-06T** | Analizador ↔ Analistas transversales (AG-09, AG-21) | Variante del CT-06: encargo transversal (`capa` BCM o PFV, nivel, presupuesto, segmentos destino, foco) e informe transversal BCM o PFV | Servicio |
| CT-07 | Analizador, Analistas, Prospectiva → Buscador | Petición de búsqueda de fuentes | Servicio |
| CT-08 | Analizador, Analistas, Prospectiva, Contrarias → Documentador para el Analizador | Petición de conocimiento académico o técnico | Servicio |
| CT-09 | Analizador, Analistas, Prospectiva, Evaluador, Orquestador, Auditor, Documentadores y Buscador → Motor | Servicio de cálculo (SYNC_CALC o ASYNC_CALC); `perfil` PERF-FX-G10, PERF-FX-EM o PERF-FX-FACT | Servicio |
| CT-10 | Orquestador, Auditor, Evaluador → Motor | Re-ejecución independiente (MC-08) | Auditoría |
| CT-11 | Analistas, Buscador, Documentadores, Prospectiva, Contrarias → Curador | Ingesta de evidencia (incluido `fuente_retirada`) | Servicio |
| CT-12 | Analizador ↔ Prospectiva | Encargo prospectivo y pronósticos PRG-FX- | Servicio |
| CT-13 | Analizador ↔ Contrarias | Refutación y objeciones graduadas | Servicio |
| CT-14 | Analizador ↔ Orquestador | Validación síncrona G3 (excepciones de HT-09) | Control síncrono |
| CT-15 | Analizador ↔ Redactor | Paquete de síntesis y devolución de los tres entregables | Servicio |
| CT-16 | Coordinador → Orquestador | Paquete de auditoría asíncrono tras cada entrega | Auditoría |
| CT-17 | Orquestador ↔ Auditor | Revisión experta y calibración de severidades | Auditoría |
| CT-18 | Orquestador → cualquier agente | Guías de mejora (tipos 1 y 2) y órdenes de escalado | Gobierno |
| CT-19 | Evaluador → Coordinador, Analizador, Analistas, Prospectiva, Buscador, Orquestador | Informe de aprendizaje | Aprendizaje |
| CT-20 | Motor ↔ Documentador para el Motor | Documentación metodológica | Servicio |
| CT-21 | Documentadores, Buscador → Orquestador | Paquete mensual de mantenimiento de conocimiento | Auditoría |
| CT-22 | Coordinador → Evaluador | Decisiones y resultados comunicados por el Broker; preguntas repetidas; V1.1: consultas recurrentes (`CONSULTA_RECURRENTE`) y decisiones sobre las recomendaciones de seguimiento (`DECISION_SEGUIMIENTO`) | Aprendizaje |
| **CT-23** | Coordinador ↔ Broker (en origen: cualquier agente → Analizador, que filtra y agrupa) | **Consulta al Broker** (V1.1): tipos ACLARACION_ALCANCE, DATO_O_DOCUMENTO, PREFERENCIA_O_CRITERIO, CONFIRMACION_SUPUESTO, OTRA; modo BLOQUEANTE (pausa la parte afectada en su punto de control) o NO_BLOQUEANTE (supuesto declarado); plazo; en sentido entrante, aclaraciones del Broker en cualquier momento | Servicio |
| **CT-24** | Broker → Coordinador; retorno por el mismo contrato | **Encargo de seguimiento de opción** (V1.1): alta, modificación, pausa, reanudación y cancelación en cualquier momento; retorno: acuse con `seg_id` y, en cada ciclo C6, el informe de seguimiento de opción | Servicio |
| **CT-25** | Coordinador ↔ Broker (en origen: Analizador, o el Buscador directamente) | **Solicitud y provisión de credenciales** (V1.1): el Broker deposita la clave en la bóveda de HT-01 y responde solo con estado y alias; la clave nunca viaja en un mensaje | Servicio |

Todo mensaje lleva `msg_id`, `contrato`, `version_contrato` ("FX-1.1"), emisor, receptor, `run_id` o `query_id`, marca temporal, presupuesto o consumo, estado de retorno (`COMPLETO`, `PARCIAL`, `SIN_RESULTADO`, `RECHAZADO`), limitaciones y autoevaluación.

**Pares sin canal** (no se dibujan ni existen): cualquier agente distinto del Coordinador ↔ Broker; cualquier agente ↔ usuario, Bloque B, Bloque A general u otros bloques; Analistas de segmento y transversales entre sí (el Analizador reparte los informes transversales); Contrarias con cualquiera distinto del Analizador (salvo lectura de archivos y CT-08); Auditor ↔ Analizador.

## 9. Flujo de un análisis y ciclos

### 9.1 Fases F0–F8 (síncronas) y F9–F10 (asíncronas)

| Fase | Nombre | Dueño | Contenido | Puerta |
|---|---|---|---|---|
| F0 | Activación y memoria | Coordinador, Analizador | Alcance, nivel y presupuesto; carga de memoria (opciones vigentes, tendencias, lecciones, certificados, F10); delta desde el último ciclo | **GC0** (¿cambio material?: movimiento > 1,5 σ semanales, reunión de banco central con cambio, sorpresa > 1 σ, intervención, invalidación a < 10 %) |
| **F0b** | Capas transversales | AG-09 y AG-21, en paralelo (CT-06T) | Informe de bancos centrales y macro cambiaria; informe de posicionamiento, flujos y volatilidad. En N1 solo se actualizan si GC0 detecta cambio | — |
| F1 | Cribado por segmento | Seis Analistas de segmento, en paralelo (CT-06) | Seis lentes cambiarias (política monetaria y diferencial, carry, valor, momentum, flujos y posicionamiento, riesgo y régimen) con PLAN_MIN del Motor; rotación exploratoria; revisión de invalidaciones; máx. 8 candidatas por segmento | **GC1** |
| F2 | Investigación dirigida | Analistas + BFA + DOC-A + Curador + Motor | Delimitación (par o cesta, dirección, divisa de financiación), tesis, mecanismo, valoración, carry, catalizadores, riesgos, convertibilidad, indicador de seguimiento, encargo para el Bloque B; PLAN_STD | **GC2** (E ≥ 50, mecanismo, exposición identificable) |
| F3 | Prospectiva multihorizonte | Prospectiva + Motor (CT-12) | Solo finalistas (máx. 5 por segmento): escenarios, hitos, PRG-FX- frente al paseo aleatorio y al forward | **GC3** (entre las 5 mejores por RK) |
| F4 | Refutación | Contrarias (CT-13) | Objeciones graduadas; respuesta del Analista | **G2** |
| F5 | Selección e integración | Analizador (HT-03) | Puntuaciones, PS1–PS8, top-3 por segmento, diversidad (clúster y divisa), coherencia entre segmentos, exposición agregada, apuestas independientes | **G1, G4** |
| F6 | Validación determinista | Analizador (HT-09) / Orquestador (CT-14) | Comprobaciones automáticas | **G3** (puede bloquear) |
| F7 | Redacción | Redactor (CT-15) | Tres entregables | Legibilidad (HT-07) y segunda pasada de HT-09 |
| F8 | Entrega y registro | Coordinador, Analizador, Prospectiva | CT-02; F5; F1/F3; congelación en F4 | — |
| F9 | Auditoría asíncrona | Orquestador + Auditor (CT-16, CT-17) | Muestreo por riesgo; hallazgos; guías | Nunca bloquea |
| F10 | Evaluación y aprendizaje | Evaluador | Resolución de pronósticos vencidos, métricas, lecciones, recalibración | Nunca bloquea |

### 9.2 Secuencia de mensajes de un ciclo semanal

1. HT-05 dispara C1 → AG-01 registra RUN-FX- en F5 y emite CT-05 a AG-02 con nivel y presupuesto por segmento y presupuesto transversal.
2. AG-02 ejecuta F0 (GC0 por segmento) y emite **CT-06T** a AG-09 y AG-21 (F0b, en paralelo); recibe los dos informes transversales.
3. AG-02 emite **CT-06** a AG-03…AG-08 con los identificadores de los informes transversales; los Analistas usan CT-07, CT-08, CT-09 y CT-11 y devuelven sus informes de segmento.
4. AG-02 encarga CT-12 a AG-10 y CT-13 a AG-11 para las finalistas.
5. AG-02 selecciona (HT-03), ejecuta HT-09 y, si no es «apto», CT-14 con AG-18.
6. AG-02 envía CT-15 a AG-17 y recibe los tres entregables; ordena a AG-10 congelar los PRG-FX- en F4.
7. AG-02 devuelve el CT-05 a AG-01 (con los informes transversales adjuntos para F5); AG-01 entrega por CT-02 al Broker y envía CT-16 a AG-18.
8. En segundo plano: AG-18 y AG-19 auditan (CT-16, CT-17, CT-18); AG-20 resuelve, mide y aprende (CT-19, CT-22); AG-14, AG-15 y AG-16 mantienen F7–F9 (CT-21).

### 9.3 Ciclos y niveles

**Ciclos**: C1 periódico (semanal por defecto) · C2 petición ad hoc · C3 consulta (N0 o escalado) · C4 mantenimiento continuo de conocimiento · C5 evaluación y aprendizaje · **C6 seguimiento encargado de opción** (V1.1: según la frecuencia de cada encargo de F11; revisión ligera «N1 de seguimiento», 2 UC, ≤ 0,5 UC sin novedad; prioridad inferior a C1–C3; se omite si la opción vuelve a ser vigente en C1). C4, C5 y C6 nunca bloquean ni retrasan C1–C3.

**Niveles**: N0 consulta (memoria; presupuesto relativo 0,05) · N1 exploratorio o «arrastre verificado» (0,3) · N2 estándar (1) · N3 profundo (2,5). El ciclo semanal se ejecuta por segmento (seis), precedido de los dos informes transversales; cada segmento recibe N1 si GC0 es negativo y N2 si es positivo. Presupuesto del ciclo semanal completo: ≤ 170 UC (transversales: 6 UC cada uno).

## 10. Entregables

1. **Informe técnico para el Broker** (Markdown/PDF): resumen ejecutivo (qué cambió, top-3 por segmento, apuestas independientes); alcance, nivel, presupuesto y consumo; régimen macro y cambiario (resumen de los informes de AG-09 y AG-21) y **exposición agregada por divisa**; por segmento: régimen, cribado, top-3 con ficha completa, alternativas descartadas y cambios; seguimiento de opciones y pronósticos abiertos; objeciones y respuestas; limitaciones y qué no sabemos; historial de aciertos frente al paseo aleatorio; anexos (CLM/EVD, cálculos, metodología y versión).
2. **Informe visual para el usuario** (HTML autocontenido y PDF; comprensible en < 3 minutos): «la semana en 30 segundos»; **mapa del mundo con las divisas** (verde gana valor, rojo pierde) y **termómetro del euro**; **semáforo de los seis segmentos** («Grandes monedas», «Monedas de materias primas», «Asia emergente», «Latinoamérica», «Europa del este, Oriente Medio y África», «Estrategias»); tarjetas (máx. 3 por segmento) con banderas o icono de cesta, nombre llano que dice qué divisa sube y cuál baja, por qué, riesgo 1–5, horizonte, confianza y qué podría salir mal; un gráfico sencillo por opción; «Cómo nos fue»; mini-glosario y aviso de no asesoramiento. Fernández-Huerta ≥ 70; frases ≤ 20 palabras.
3. **Paquete JSON** (`paquete_oportunidades`): metadatos, régimen cambiario (dólar, riesgo, volatilidad), `apuestas_independientes`, `exposicion_agregada`, opciones por segmento con todos sus campos (tipo de opción, par o composición, dirección, divisa de financiación, tesis, puntuaciones, horizontes, valoración, carry, catalizadores, riesgos, invalidación, indicador de seguimiento, convertibilidad, campos de decisión, objeciones), seguimiento de vigentes, historial de aciertos, **`paquete_para_bloque_B`** (par o composición, dirección, divisa de financiación, segmento, ámbito, tesis y mecanismo, horizontes y pronósticos, catalizadores, riesgos e invalidación, indicador de seguimiento, carry esperado, **consideraciones de implementación** —liquidez, NDF, riesgo de evento, horario de liquidez—, métricas clave, preguntas para el Bloque B, evidencias y cálculos) y `preguntas_sugeridas`.

4. **Informe de seguimiento de opción** (V1.1, ciclo C6, por CT-24): una pantalla (≤ 300 palabras) + JSON `informe_seguimiento_opcion`: qué ha cambiado, semáforo, señales de interés, invalidación, catalizadores, puntuaciones con HT-03, pronósticos abiertos e hitos, recomendación (con encargo B actualizado si propone el envío).

Ruta: `ENT/Informes técnicos Broker/`, `ENT/Informes visuales Usuario/`, `ENT/Paquetes JSON/`, `ENT/Informes de seguimiento/`, con nombre `AAAA-MM-DD_tipo_RUN-id`.

## 11. Puntuaciones, puertas y selección

- **T** relevancia de la tendencia · **E** calidad de la evidencia · **M** madurez (descriptiva) · **P** prioridad de investigación · **A** atractivo de la oportunidad cambiaria: asimetría 30 · valoración y desviación del equilibrio 20 · carry 15 · catalizadores 15 · momento y posicionamiento 10 · convertibilidad y profundidad 10 (nunca costes de instrumentos).
- **RK = 0,45·A + 0,35·E + 0,20·T** (calibrable). Elegibilidad: E ≥ 60, A ≥ 55, T ≥ 50 (o T NA con A ≥ 65), G1–G4, PS1–PS8 y ninguna objeción fuerte sin resolver.
- **PS1** evidencia · **PS2** datos de mercado frescos (H1 1 día, H2 2, H3 5, H4 30) · **PS3 convertibilidad e invertibilidad** · **PS4** exposición cuantificada (pesos y divisa de financiación) · **PS5** refutación · **PS6** discrepancias · **PS7** críticos (manipulación de la fijación, sanciones, ruptura del régimen) · **PS8** cálculo.
- **Selección**: orden por RK (empate ±2: mayor E y menor riesgo de cola); máximo dos opciones del mismo clúster (dólar, yen y refugio, carry y riesgo global, materias primas, una divisa); **una divisa no puede tener la misma dirección en más de dos opciones del segmento**; continuidad de las vigentes; menos de tres con motivo; coherencia entre segmentos (sin duplicados, exposiciones comunes, apuestas independientes, contradicciones justificadas o resueltas).
- Tope de 40 en la valoración con narrativa saturada (posicionamiento en el decil extremo a favor y forward que ya descuenta la senda esperada).

## 12. Horizontes y referencias

H1 días (1–10 sesiones), H2 semanas (2–8), H3 meses (3–12), H4 años (1–5), H5 décadas (5–30; V1.1, «limitado»).

| Segmento | H1 | H2 | H3 | H4 | H5 |
|---|---|---|---|---|---|
| G10N | Sí | Sí | Sí | Sí | Limitado |
| G10M | Sí | Sí | Sí | Sí | Limitado |
| EMAS | Limitado | Sí | Sí | Limitado | Limitado |
| EMLA | Limitado | Sí | Sí | Limitado | Limitado |
| EMEA | Limitado | Sí | Sí | Limitado | Limitado |
| ESTR | No | Sí | Sí | Sí | Limitado |

**H5** solo para naturaleza `ESTRUCTURAL` en tres ámbitos (equilibrio a muy largo plazo, regímenes cambiarios, sistema monetario internacional); probabilidad siempre cualitativa; ≥ 3 hitos HIT-FX- evaluados en su fecha. **Regla de adecuación** (V1.1): cada opción declara su naturaleza y su horizonte principal dentro de su rango (TACTICA H1–H2 · CICLICA y PRIMA_RIESGO H2–H4 · VALORACION H3–H4 · ESTRUCTURAL H4–H5); HT-09 lo valida.

Referencias obligatorias: **paseo aleatorio** (sin cambio) y **forward como predictor**; en rentabilidad total, rentabilidad en exceso nula (G10N, G10M), cesta equiponderada del segmento frente al USD con carry (EMAS, EMLA, EMEA) e índice de la estrategia o rentabilidad nula (ESTR). Probabilidades numéricas solo con certificado del Evaluador (≥ 100 pronósticos resueltos, IC 90 % del Brier skill score frente al paseo aleatorio por encima de 0 y calibración no rechazada); en otro caso, bandas verbales y la etiqueta «sin ventaja demostrada frente al paseo aleatorio».

## 13. Cómo aprende, ahorra y se autocritica

- **Aprende**: nivel A operativo (búsquedas, fuentes, métodos), nivel B predictivo (resolución sin fuga, calibración, recalibración dentro de bandas: pesos ±5 pp por trimestre y ±15 en total; umbrales ±5 y ±10; evaluación sombra; versiones FX-1.0 → FX-1.1) y nivel C metodológico (tipo 3 con aprobación del operador). Lecciones LEC- inyectadas al inicio de cada encargo (máx. 10 por ámbito). Aprende también de las decisiones del Broker, de las preguntas repetidas y de la exactitud histórica de las fuentes de opinión frente al paseo aleatorio.
- **Ahorra**: embudo con puertas de continuidad; capas transversales analizadas una sola vez y repartidas a los seis segmentos; reutilización obligatoria (HT-06, caché del Motor); presupuestos en UC; reglas de parada; herramientas deterministas; auditoría por muestreo; barrido de enlaces por lotes.
- **Se autocritica**: pre-mortem, refutación adversarial, respuesta obligatoria a objeciones, validación determinista, comparación con el paseo aleatorio y el forward, sección «qué podría salir mal y qué no sabemos», historial de aciertos publicado, detección de sobreconfianza y auditoría independiente.

## 14. Especificación para regenerar el diagrama

**Lienzo**: horizontal, fondo claro; título superior «Bloque A Forex — Buscador de Oportunidades en Divisas · Arquitectura óptima V1.1» y subtítulo «Robot Investor · 03/11/2026 · 21 agentes en 4 planos · 6 segmentos de divisas · contratos CT-01…CT-25 + CT-06T · archivos F1…F11 · herramientas HT-01…HT-09». (Generador de referencia: `diagrama_fx11.py`, copia adaptada del de V1.0.)

**Bandas de arriba abajo**:

1. **Exterior del bloque** (gris): cajas «Usuario» (solo habla con el Broker), «Broker Personal» (decide en modo autónomo · manual · semiautónomo; peticiones y consultas sin límite) y «Bloque B» (analiza la oportunidad y elige instrumento, coste y cobertura). Flecha Usuario ↔ Broker; flecha discontinua Broker → Bloque B «decide enviar». Nota opcional: «Bloque A general: sin canal».
2. **P1 · Interfaz y ciclo** (azul): caja AG-01 con «Interfaz única · ciclo semanal configurable · colas y niveles N0–N3 · consultas N0 desde la memoria · Historial de análisis (F5) · Configuración (F10)». Flechas Broker → AG-01 «CT-01 petición · CT-03 consulta · CT-04 decisiones» y AG-01 → Broker «CT-02 entrega · CT-03 respuesta»; **V1.1**: flecha bidireccional roja AG-01 ↔ Broker con las etiquetas «CT-23 consultas al Broker», «CT-24 encargos de seguimiento» y «CT-25 credenciales», y en la caja AG-01 la línea «CT-23 dudas del bloque · CT-25 credenciales (bóveda HT-01) · CT-24 seguimientos → F11 y ciclo C6».
3. **P2 · Análisis** (verde, banda principal): arriba, caja ancha AG-02 «Analizador de Oportunidades en Divisas — director» (DÓNDE, POR QUÉ y CUÁNDO en divisas · top-3 por segmento con HT-03 · exposición agregada · encargo B · propietario de F1 y F3); flecha AG-01 → AG-02 «CT-05 orden de análisis». Debajo, una fila con las dos cajas transversales (AG-09 TR-BCM «sendas descontadas · diferenciales · calendario · intervención»; AG-21 TR-PFV «CFTC · flujos · volatilidad implícita · *risk reversals* · base»), unidas a AG-02 por flechas bidireccionales «CT-06T». Debajo, una fila con las seis cajas de segmento (AG-03 G10N, AG-04 G10M, AG-05 EMAS, AG-06 EMLA, AG-07 EMEA, AG-08 ESTR), unidas a AG-02 por flechas «CT-06»; leyenda de la fila: «Dos Analistas transversales (CT-06T) alimentan a seis Analistas de segmento (CT-06) · pares, cruces, cestas y estrategias; nunca instrumentos». **No hay flechas** entre transversales y segmentos ni entre segmentos. A la derecha o debajo, cuatro cajas de servicio enlazadas con AG-02: AG-10 Prospectiva (CT-12, → F4), AG-11 Contrarias (CT-13), AG-12 Curador (CT-11, → F2), AG-17 Redactor (CT-15). Caja ancha AG-13 Motor (perfiles PERF-FX-G10 · PERF-FX-EM · PERF-FX-FACT; MC-01…MC-10; «MC-10 evaluación frente al paseo aleatorio y al forward»; CT-09; CT-10 desde P4). A la derecha, columna «Entregables al Broker (CT-02)» con tres cajas: Informe técnico, Informe visual (mapa · lenguaje llano), Paquete JSON (hasta 3 opciones por segmento + encargo Bloque B), con flecha AG-17 → entregables → AG-01.
4. **P3 · Conocimiento** (morado): AG-14 (TX- → F7 · CT-08 · custodio del Fondo metodológico), AG-15 (TMX- → F8 · CT-20 con el Motor), AG-16 (bancos centrales · COT · COFER · prensa FX → F9 · TFX- · CT-07 · fiabilidad medida). Flecha de banda P2 ↔ P3 «CT-07 · CT-08 · CT-20». Título de banda: «alimentación continua, verificación de enlaces y borrado de referencias».
5. **P4 · Calidad y aprendizaje** (naranja; «segundo plano, nunca bloquea salvo G3»): AG-18 (G3 con CT-14 + HT-09 · auditoría · guías CT-18 · colas, presupuestos e instancias · HA), AG-19 (revisión experta por muestreo · CT-17 · R1–R27), AG-20 (resuelve F4 frente al paseo aleatorio · certifica horizontes · lecciones F6 · CT-19). Flechas: AG-02 ↔ AG-18 «CT-14»; AG-01 → AG-18 «CT-16»; AG-18 ↔ AG-19 «CT-17»; AG-01 → AG-20 «CT-22»; AG-20 → agentes «CT-19»; P3 → AG-18 «CT-21».
6. **Archivos del bloque** (amarillo): columna de 14 fichas F1…F11, FM, RC, HA (V1.1: F11 «Seguimientos encargados (CT-24, C6)», escribe Coordinador), cada una con nombre corto y «escribe: …» (F1 Analizador; F2 Curador; F3 Analizador; F4 Prospectiva / Evaluador; F5 Coordinador; F6 Evaluador; F7 Doc. Analizador (TX-); F8 Doc. Motor (TMX-); F9 Buscador (TFX-); F10 Coord. / Evaluador; FM Doc. Analizador (todos los bloques); RC Motor; HA Orquestador). Nota: «Append-only salvo bajas de referencias (R19)».
7. **Herramientas deterministas compartidas** (gris claro): nueve fichas HT-01 Datos y bóveda de credenciales · HT-02 Verificador de enlaces · HT-03 Puntuaciones y ranking · HT-04 Gráficos y mapas · HT-05 Planificador (C1, C6) · HT-06 Índice y caché · HT-07 Legibilidad · HT-08 Colas y consumo · HT-09 Validador G3. Nota: «sin modelo de lenguaje: ahorro de cómputo».
8. **Flujo de un análisis** (franja inferior): nueve cajas encadenadas con su puerta debajo: «F0 · Memoria + F0b» (GC0) → «F1 · Cribado por segmento» (GC1) → «F2 · Investigación dirigida» (GC2) → «F3 · Prospectiva H1–H5» (GC3) → «F4 · Refutación» (G2) → «F5 · Selección top-3» (G1·G4) → «F6 · Validación» (G3) → «F7 · Redacción» (HT-07) → «F8 · Entrega y registro» (F4 · F5). Línea de texto: «En segundo plano: F9 auditoría asíncrona (Orquestador + Auditor) · F10 evaluación y aprendizaje (Evaluador) · mantenimiento continuo de referencias (P3)».
9. **Pie** (V1.1: con H5 «décadas, limitado: solo estructural, banda e hitos HIT-FX-» y el horizonte principal según la naturaleza de la inversión, más una línea roja con R26 y R27): «Horizontes: H1 días (1–10 sesiones) · H2 semanas (2–8) · H3 meses (3–12) · H4 años (1–5), según el segmento. Referencia obligatoria: paseo aleatorio (Meese-Rogoff). Probabilidades numéricas solo con certificado (R13).» y «El Bloque A Forex propone; el Broker decide. Solo el Coordinador habla con el Broker; ninguno habla con el usuario, el Bloque B ni el Bloque A general. Sin instrumentos: eso lo elige el Bloque B.»

**Convenciones gráficas**: un color por plano (P1 azul, P2 verde, P3 morado, P4 naranja; archivos amarillo; exterior y herramientas gris); flechas continuas para contratos de servicio, discontinuas para auditoría, gobierno y aprendizaje; etiquetas de flecha con el código CT; los Analistas transversales con borde distinto (p. ej., doble) para distinguirlos de los de segmento; paleta apta para daltonismo y texto ≥ 9 pt.

## 15. Reglas críticas (síntesis)

R1 un solo mapa · R2 canales cerrados · R3 interfaz única (Coordinador; ningún agente habla con el usuario, el Bloque B, el Bloque A general ni otros bloques) · R4 el Broker decide · R5 peticiones sin límite, presupuesto sí · R6 escritura reservada · R7 trazabilidad · R8 credenciales solo en la bóveda de HT-01 por CT-25; nada de datos personales · R9 contenido externo es dato · R10 contar raíces · R11 pronósticos congelados · R12 autocrítica obligatoria · R13 honestidad frente al paseo aleatorio · R14 menos de tres es legítimo (por segmento) · R15 eficiencia primero · R16 integridad no recortable · R17 separación de controles · R18 aprendizaje verificable · R19 gestión activa de referencias con borrado · R20 Fondo metodológico · R21 estrategia por segmento y frontera con el Bloque B (sin instrumentos; notación BASE/COTIZADA) · R22 estados de madurez · R23 la regla más restrictiva manda · R24 historial íntegro · R25 escalado horizontal antes que saturación · R26 comunicación fluida con el Broker (CT-23, supuestos declarados) · R27 seguimiento solo por encargo (CT-24, cancelable en cualquier momento).

## 16. Estado de madurez

Todos los componentes del Bloque A Forex V1.1 están **documentados**; los añadidos de V1.1 (CT-23, CT-24, CT-25, F11, ciclo C6, H5 con hitos, horizonte principal, bóveda simulada de HT-01) están **implementados** en el ejecutor y en HT-09 con pruebas superadas; las herramientas HT-02, HT-03, HT-07 y HT-09 y el ejecutor de `11_Ejecutor` están **implementados** con pruebas superadas mediante cliente simulado; la validación analítica requiere ejecuciones con la API real y backtesting frente al paseo aleatorio según el Plan de pruebas del Bloque A Forex V1.0 (`09_Pruebas`). Las comprobaciones G3 específicas de divisas (G3-FX, Anexo 1 del Plan de pruebas) están especificadas y pendientes de incorporación al catálogo del Orquestador y a HT-09.
