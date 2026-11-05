# Constitución Global del Robot Inversor — V0.1

Nov 5, 2026 · @Dani

**Versión sustituida por la V0.2 (5 de noviembre de 2026).** Se conserva solo para comparar.

## 0. Estado, alcance y modo de uso

Este documento fija las reglas que valen para **todo** el Robot Inversor; ningún bloque se construye sin cumplirlas. Es la versión V0.1 (borrador del 5 de noviembre de 2026), redactada tras el brainstorming con el operador y la revisión de la propuesta de ChatGPT (4 de noviembre de 2026).

**Alcance.** Sistema personal de inversión con **capital propio únicamente**, que investiga, analiza, compara, construye carteras, controla el riesgo, ejecuta bajo autorización y aprende de sus resultados. No presta servicio a terceros; si eso cambiara, habría que revisar la normativa aplicable antes de seguir.

**Precedencia.**

1. En materias globales (contratos entre bloques, autonomía, control, identificadores) prevalece esta Constitución sobre el Documento 0 de cualquier bloque.
2. En lo interno de un bloque prevalece su Documento 0, siempre que no contradiga este documento.
3. Un conflicto detectado se registra en el §15 y lo resuelve el operador. Nadie lo resuelve por su cuenta.

**Lenguaje normativo.** DEBE = obligatorio; DEBERÍA = salvo razón registrada; PUEDE = opcional. Cada decisión lleva una etiqueta: `[RATIFICADO]` (la ha tomado el operador), `[PROPUESTO]` (propuesta de Claude pendiente de ratificar) o `[ABIERTO]` (sin decidir).

**Cómo se usa.** Cada conversación de construcción de un bloque empieza con esta Constitución, la ficha de interfaz del bloque (§2) y los contratos que le afectan (§5). Con eso basta: no hace falta reabrir los bloques anteriores.

## 1. Propósito y principios rectores

**Propósito.** Producir decisiones de inversión fiables, trazables y mejorables con capital propio, y abstenerse cuando la evidencia no basta. La fiabilidad pesa más que la rentabilidad: la arquitectura no garantiza rentabilidad, solo reduce la probabilidad de errores evitables y los hace visibles.

Los principios siguientes son invariantes. Ningún bloque, prompt ni herramienta puede contradecirlos.

1. **P1 · Separación de poderes.** Quien propone no aprueba, quien aprueba no ejecuta y quien ejecuta no interpreta. Inteligencia (A–D, J), decisión y carteras (E), control (F), ejecución (G) y contabilidad están separadas.
2. **P2 · Los controles duros no son LLM.** Límites, permisos, validación de órdenes, veto de riesgo y kill-switch se ejecutan en código determinista y verificable. Un LLM puede pedir una excepción, nunca concederla.
3. **P3 · Las cifras no las escribe un agente.** Las calcula un motor reproducible (semilla, fecha de corte, hash) y los agentes las citan por identificador. Los parámetros viven en configuración, no en texto.
4. **P4 · Contratos primero.** Los bloques solo se hablan mediante contratos con esquema JSON congelado y versionado. Un mensaje que no valida el esquema se rechaza; no se «interpreta».
5. **P5 · Abstenerse es un resultado válido.** La alternativa de referencia de toda comparación es no hacer nada (liquidez o índice). Una opción que no la supera con margen no avanza.
6. **P6 · Pronósticos falsables y congelados.** Toda tesis material declara qué la invalidaría y se registra antes de conocerse el resultado. Se evalúa después con métricas de calibración frente a referencias ingenuas.
7. **P7 · Evidencia con procedencia.** Todo dato lleva fuente, fecha de obtención, fecha de vigencia y etiqueta epistémica (verificado, estimado, supuesto). Los datos originales no se sobrescriben. Las pruebas históricas usan datos tal como se conocían en cada fecha (sin *look-ahead*).
8. **P8 · Aprendizaje gobernado.** Ningún aprendizaje cambia límites, estrategias, modelos o parámetros de ejecución por sí solo. Todo cambio se propone, se valida (J), se aprueba y se versiona.
9. **P9 · Autonomía graduada y revocable.** El nivel de autonomía se concede por cartera y tipo de acción, sube con resultados medidos y baja de inmediato ante cualquier anomalía. Ante la duda, no se actúa.
10. **P10 · Toda decisión material es reconstruible.** Debe poder saberse qué datos, qué agentes, qué versión de reglas, qué controles y qué aprobaciones intervinieron y qué ocurrió después.
11. **P11 · El contenido externo es dato, no instrucción.** Lo que llega de la web, de documentos o de otros agentes no puede alterar reglas ni permisos. Las credenciales nunca están en el contexto de un agente.
12. **P12 · Especializar sin duplicar.** Los 12 sub-bloques de C comparten un marco común y un sobre de salida idéntico. Cambia el contenido especializado, no el esqueleto.
13. **P13 · Degradación segura.** Cada bloque declara qué hace ante datos obsoletos, contrato incompatible o servicio caído. La respuesta por defecto es detenerse, marcar y escalar; nunca rellenar.

## 2. Mapa de bloques

El sistema tiene **diez bloques** (A–J, con A y B en versión general y Forex), un **orquestador** (Broker Personal) y **servicios comunes** (§3). A, B y sus variantes Forex ya están construidos; el resto está por definir. Cada fila es la **ficha de interfaz** mínima: un bloque nuevo DEBE ajustarse a ella.

| Bloque | Responsabilidad | Recibe | Entrega | No hace |
| --- | --- | --- | --- | --- |
| **Broker Personal** | Juicio y diálogo con el operador; decide qué se analiza, qué se compara y qué se propone | Perfil y mandato, paquetes de B, sobres de C, comparativas de D | Encargos a B y a C.x; propuestas a E; consultas al operador | Calcular, aprobar riesgo, enviar órdenes |
| **A** / **A Forex** | Descubrir oportunidades por tipo de activo | Encargo del Broker | `paquete_para_bloque_B` | Analizar mercado, valorar, seleccionar |
| **B** / **B Forex** | Analizar un ámbito de mercado y seleccionar candidatos con su vía de acceso | Encargo del Broker (una petición = una propuesta) | `paquete_para_bloque_C` | Valorar en profundidad, dimensionar, entrar |
| **C.x (12)** | Valoración profunda, analítica y exhaustiva de un tipo de activo | Encargo del Broker (nivel N0–N3) | Sobre común + cuerpo especializado | Comparar entre tipos, decidir, dimensionar |
| **D** | Comparar opciones ya analizadas | Sobres de C elegidos por el Broker, estado de carteras (solo lectura) | Comparativa: ranking por mandato, dominancia y sensibilidad | Elegir (lo hace el Broker), dimensionar |
| **E** | Construir carteras y dimensionar posiciones | Propuesta del Broker, mandatos, estado de carteras | Plan de cartera por libro; vista global consolidada | Vetar riesgo, enviar órdenes |
| **F** | Control independiente y determinista | Todo plan o acción material | Aprobado, reducido o vetado, con motivo y versión de política | Proponer inversiones |
| **G** | Único canal de órdenes; ciclo de vida de la orden; contabilidad y conciliación | Acciones aprobadas por F (y por el operador si procede) | Estados de orden y libro conciliado | Interpretar tesis, decidir |
| **H** | Seguimiento de posiciones y revaluación | Libro de G, condiciones de invalidez de C, eventos | Alertas y peticiones de revaluación al Broker | Ejecutar cambios por sí solo |
| **I** | Evaluación, atribución, calibración y propuestas de mejora | Resultados, registro de pronósticos, auditoría | Informes y propuestas de cambio versionadas | Aplicar cambios |
| **J** | Laboratorio de estrategias: diseño, backtest, paper trading y validación de cambios | Hipótesis, datos, propuestas de I | Estrategias validadas con sus parámetros congelados; veredicto de validación | Poner nada en producción |

**Las dos vías de entrada.** Una oportunidad entra al sistema por la **vía discrecional** (A → B → C → D, para activos analizados uno a uno) o por la **vía sistemática** (J, para estrategias con reglas validadas, propia de los libros de trading y táctico). Las dos desembocan en el mismo expediente (§4) y pasan por E, F y G sin excepciones.

**Los doce sub-bloques de C.** `[RATIFICADO]` La codificación estable usa el código del tipo de activo (`C-DIV`); la forma `C.n` queda como alias. Los doce tipos son los del Bloque A:

| Código | Tipo de activo | Alias `C.n` (orden del Bloque A/B) |
| --- | --- | --- |
| C-RV | Renta variable | C.1 |
| C-RF | Renta fija | C.2 |
| C-DIV | Divisas | C.3 |
| C-MP | Materias primas | C.4 |
| C-IDX | Índices bursátiles | C.5 |
| C-FON | Fondos y vehículos de inversión colectiva | C.6 |
| C-DER | Derivados financieros | C.7 |
| C-INM | Activos inmobiliarios cotizados | C.8 |
| C-CRI | Criptoactivos | C.9 |
| C-ALT | Capital privado y alternativos | C.10 |
| C-MON | Monetarios y liquidez | C.11 |
| C-TCV | Tipos de interés, crédito y volatilidad | C.12 |

**Aviso de numeración.** El operador llama «C.1» al analista de divisas, mientras que los Documentos 0 de B y B Forex lo designan C.3 (C.1 es renta variable). Con los códigos mnemotécnicos el conflicto desaparece: el sub-bloque de divisas es `C-DIV`, se llame como se llame su alias.

## 3. Los tres planos y los servicios comunes

Todo componente pertenece a un solo plano, y cada plano tiene una autoridad distinta.

| Plano | Qué contiene | Autoridad | Tecnología |
| --- | --- | --- | --- |
| **Inteligencia** | Broker, A, B, C.x, Contradictor, D, J, partes analíticas de E, H e I | Propone. Nunca decide por sí solo sobre riesgo, permisos ni órdenes | Agentes LLM + motores de cálculo |
| **Control** | F, el flujo de estados del expediente, la matriz de autonomía, la cola de aprobaciones, el kill-switch, G | Veta, limita y autoriza. Ningún agente del plano de inteligencia puede anularlo | Código determinista, sin LLM en la ruta de decisión |
| **Datos y memoria** | Evidencia, registro de pronósticos, registro de eventos y auditoría, libro contable, credenciales | Guarda la verdad. Es de solo anexado: lo histórico no se reescribe | Almacenes indexados con identificador y hash |

**Servicios comunes (SC).** Se construyen una sola vez y los usan todos los bloques. `[PROPUESTO]`

| Servicio | Función |
| --- | --- |
| **SC-1 Perfil y mandato** | Fuente única de objetivos, horizonte, tolerancia al riesgo, límites por cartera y restricciones del operador |
| **SC-2 Datos y evidencia** | Ingesta, normalización, validación, procedencia, frescura y consulta «punto en el tiempo». Los almacenes grandes se consultan por ID, no se cargan enteros |
| **SC-3 Motor numérico** | Biblioteca de cálculo compartida: volatilidad, correlaciones, escenarios, valoración, backtest. Cada artefacto es reproducible (hash, semilla, fecha de corte) |
| **SC-4 Registro de pronósticos y memoria** | Congela los pronósticos, resuelve resultados y calcula calibración (Brier, BSS, Diebold-Mariano frente a referencias ingenuas). Guarda también las opciones descartadas y sus condiciones de reapertura |
| **SC-5 Eventos y auditoría** | Registro anexado de eventos, decisiones, versiones, permisos y errores, con `correlation_id` de extremo a extremo |
| **SC-6 Validador de contratos** | Generaliza la validación G3: comprueba esquema y coherencia de cada paquete antes de que pase al bloque siguiente |
| **SC-7 Seguridad** | Bóveda de credenciales, segregación de entornos, límites de API, copias y respuesta a incidentes |
| **SC-8 Contexto macro y de flujos** | Macro, política, sentimiento y flujos, consumidos por B y C.x; no es un bloque con decisión propia |
| **SC-9 Fiscalidad y costes** | Costes de transacción e impacto fiscal personal en España, usados por D, E y G. Pesa sobre todo en la cartera de largo plazo |

**Contradictor independiente.** Es un agente del plano de inteligencia entre C y D. Recibe la evidencia, pero no el razonamiento del analista, y construye los escenarios en que la tesis falla. Su informe forma parte del expediente y D lo recibe.

## 4. Expediente de oportunidad y estados

Toda oportunidad, entre por la vía discrecional o por la sistemática, vive en un **expediente**: un único objeto con `expediente_id` y `correlation_id` que viaja de A a I. Lo gestiona una máquina de estados determinista (plano de control), no un LLM.

**Contenido mínimo.**

| Campo | Significado |
| --- | --- |
| `expediente_id`, `correlation_id` | Identificadores únicos; el segundo agrupa todos los eventos del caso |
| `via_entrada` | `DISCRECIONAL` (A→B→C) o `SISTEMATICA` (J) |
| `cartera_destino` | `TRADING`, `TACTICA` o `LARGO_PLAZO` (puede cambiar tras D, con registro) |
| `tipo_activo`, `horizonte` | Código del tipo (`DIV`, `RV`…) y horizonte de la tesis |
| `secciones` | Una por bloque que ha intervenido, cada una versionada, inmutable y con `valid_until` |
| `estado` | Uno de los estados de abajo |
| `historial` | Cada transición: quién, cuándo, por qué, con qué versión de reglas |

**Estados de una oportunidad** `[PROPUESTO]`, tomados del PDF y ajustados:

`DETECTADA` → `EN_ANÁLISIS` → `VALIDADA` → `COMPARADA` → `PROPUESTA` → `AUTORIZADA` → `EN_CARTERA`

Desde casi cualquier estado puede pasar a `EN_OBSERVACIÓN` (con condiciones objetivas de reapertura) o a `DESCARTADA` (con motivo). Desde `EN_CARTERA` se vuelve a `EN_ANÁLISIS` cuando H pide una revaluación.

**Estados de una orden** (los gestiona G): `BORRADOR` → `VALIDADA` → `AUTORIZADA` → `ENVIADA` → `PARCIAL` / `EJECUTADA` / `RECHAZADA` / `CANCELADA` → `CONCILIADA`. Una orden enviada no cuenta como ejecutada hasta que existe confirmación verificable del intermediario y conciliación.

**Reglas del expediente.**

1. Un bloque solo añade **su propia** sección. Nunca edita la de otro; una corrección es una nueva versión.
2. Solo la máquina de estados cambia el estado, y solo por transiciones permitidas. Un agente la solicita; no la ejecuta.
3. Cuando una sección caduca (`valid_until`), el expediente no avanza: vuelve a `EN_ANÁLISIS` o pasa a `DESCARTADA`, y el Broker decide cuál.
4. Las opciones descartadas o en observación conservan su motivo y las condiciones de reapertura en SC-4.

## 5. Contratos entre bloques

Los contratos son la arquitectura: un bloque es sustituible mientras cumpla los suyos. Se definen **antes** de construir cada bloque, con esquema JSON congelado, y se validan mecánicamente (SC-6). Los contratos ya existentes entre A y B (`CT-B-01…CT-B-29`) siguen vigentes; los nuevos usan el prefijo `CT-G-` (globales).

**Sobre de mensaje (obligatorio en todo contrato).** `[PROPUESTO]`

| Campo | Contenido |
| --- | --- |
| `event_id`, `correlation_id`, `expediente_id` | Identificación del mensaje y del caso |
| `producer`, `consumer` | Bloque emisor y destinatario |
| `tipo_mensaje`, `version_esquema` | Qué es y con qué versión del esquema se validó |
| `emitido_en`, `valid_until` | Cuándo se generó y hasta cuándo vale |
| `data_refs` | Referencias a la evidencia (SC-2) y a los artefactos del Motor (SC-3) |
| `payload` | Contenido tipado, con unidades y divisa explícitas |
| `confianza`, `incertidumbre` | Calibrada y con limitaciones conocidas |
| `resultado_politica` | Controles aplicados, resultado, motivo y versión de política |

**Catálogo de contratos globales.** `[PROPUESTO]`

| ID | Contrato | De → a |
| --- | --- | --- |
| CT-G-01 | Encargo de análisis en profundidad (pregunta, decisión que informa, nivel N0–N3, plazo y presupuesto, restricciones del mandato, fecha de corte, paquete de B referenciado) | Broker → C.x |
| CT-G-02 | **Sobre común de valoración** (ver abajo) | C.x → Broker, Contradictor, D |
| CT-G-03 | Informe del Contradictor | Contradictor → Broker, D |
| CT-G-04 | Petición de comparación (opciones, criterio, cartera de referencia) | Broker → D |
| CT-G-05 | Comparativa (ranking por mandato, dominancia, sensibilidad, coste de oportunidad) | D → Broker |
| CT-G-06 | Propuesta de inversión | Broker → E |
| CT-G-07 | Plan de cartera por libro | E → F, Broker |
| CT-G-08 | Resultado de control (aprobado, reducido o vetado, con motivo) | F → Broker, G |
| CT-G-09 | Orden | E/F → G |
| CT-G-10 | Alerta o petición de revaluación | H → Broker |
| CT-G-11 | Consulta al Broker o al operador (generaliza `CT-B-28`) | Cualquier bloque → Broker |
| CT-G-12 | Seguimiento de encargo (generaliza `CT-B-29`) | Bloque → Broker |
| CT-G-13 | Propuesta de cambio y veredicto de validación | I → J → Broker |

**El sobre común de valoración (CT-G-02).** Es la pieza central: hace comparables los 12 sub-bloques. Todos DEBEN emitirlo con el mismo esquema, y añadir aparte su cuerpo especializado, que cada tipo de activo define libremente y el sobre referencia.

| Bloque del sobre | Contenido obligatorio |
| --- | --- |
| Identificación | Tipo de activo, instrumento y vía de acceso, dirección, cartera(s) compatible(s), nivel de análisis, fecha de corte |
| Tesis | Resumen, supuestos y **condiciones de invalidez medibles** |
| Escenarios | Mínimo base, favorable y adverso, con probabilidad y rentabilidad neta en EUR a un **horizonte común normalizado**; resumen de la distribución (p. ej., p5, mediana, p95) |
| Riesgo | Pérdida en un **conjunto estándar de escenarios de estrés** comunes a todos los tipos, caída máxima esperada, volatilidad |
| Factores | Exposición a un conjunto común de factores: tipos, renta variable, USD, crédito, inflación, materias primas, volatilidad y liquidez |
| Liquidez y salida | Tiempo de salida, coste de salida, tamaño máximo sin impacto apreciable |
| Costes e impuestos | Costes de entrada, mantenimiento y salida; impacto fiscal estimado (SC-9) |
| Capital | Capital necesario, margen y apalancamiento |
| Confianza | Probabilidad calibrada y referencia a la calibración histórica de ese C.x (SC-4) |
| Calidad de evidencia | Frescura y proporción de cifras verificadas, estimadas y supuestas |
| Pronósticos | Identificadores de los pronósticos congelados en SC-4 |
| Exclusiones duras | Sanciones, invertibilidad (ESMA y marco minorista), acceso y custodia |
| Referencias | Enlace al cuerpo especializado y a los artefactos del Motor |

**Reglas de comparabilidad.** (1) Mismas unidades, divisa base EUR y horizonte normalizado. (2) Mismo conjunto de escenarios de estrés para todos. (3) La confianza de un C.x no se compara en bruto: D la descuenta con su historial de calibración. (4) Toda cifra va por ID del Motor (P3).

**Versionado.** Los esquemas siguen versionado semántico. Un cambio incompatible exige versión mayor, un adaptador y una nota en el §15. Un paquete con versión de esquema desconocida se rechaza, no se interpreta.

## 6. Autonomía

La autonomía no es un interruptor global: se concede por **cartera × tipo de acción × tamaño** y la aplica el plano de control. `[RATIFICADO]` el principio de tres modos (manual, semiautónomo y autónomo); el detalle siguiente es `[PROPUESTO]`.

| Nivel | Modo | Qué puede hacer el robot | Qué exige al operador |
| --- | --- | --- | --- |
| **L0** | Simulación | Todo el flujo con órdenes simuladas (paper trading) | Nada; sirve para validar |
| **L1** | Manual (asesor) | Analiza, compara, propone y prepara la orden completa | Ejecutar él mismo, o aprobar cada orden |
| **L2** | Semiautónomo | Actúa solo dentro de los límites y de las acciones permitidas para ese nivel | Aprobar cada acción fuera del umbral (ver abajo) |
| **L3** | Autónomo | Envía órdenes por G dentro del mandato y los límites, sin aprobación previa | Supervisar con alertas y revisión periódica |

**Matriz de autonomía.** Cada cartera tiene su nivel por tipo de acción. Punto de partida recomendado: las tres carteras en **L1**, con G diseñado pero desactivado, y subida por cartera cuando se cumplan los criterios de promoción.

| Tipo de acción | En L2 (semiautónomo) |
| --- | --- |
| Análisis, consultas, informes, alertas | Automático |
| Reducir riesgo (stop, recorte por invalidez de la tesis, cierre por límite) | Automático si F lo aprueba |
| Abrir o aumentar posición dentro del umbral | Automático si F aprueba, el instrumento ya está admitido y no hay apalancamiento |
| Abrir o aumentar posición por encima del umbral, o en un instrumento nuevo | **Aprobación del operador** |
| Apalancamiento, derivados, CFD | **Aprobación del operador** |
| Cambio de estrategia, modelo, límite o parámetro de ejecución | **Aprobación del operador**, tras validación de J |
| Movimientos de efectivo o entre carteras | **Aprobación del operador** |
| Cualquier acción con datos obsoletos, discrepancia de saldo o control degradado | **Prohibida**; se escala |

Los umbrales (por ejemplo, el tamaño máximo de una acción automática como fracción de la cartera) viven en la configuración y los fija el operador `[ABIERTO]`. La asimetría es deliberada: reducir riesgo exige menos permiso que aumentarlo.

**Cola de aprobaciones.** Toda petición al operador incluye la acción exacta, sus cifras, el resultado de F y una caducidad. Reglas:

1. Una aprobación vale solo para esa acción con esas cifras. No se reutiliza.
2. Si caduca sin respuesta, la acción por defecto es **no actuar**.
3. Las acciones que aumentan riesgo exigen un canal autenticado (segundo factor), nunca un mensaje de chat sin verificar.

**Promoción y degradación.** Subir de nivel exige un periodo mínimo en el nivel actual con conciliación limpia, cero incumplimientos de límites y calibración aceptable `[ABIERTO: criterios y duración]`. Bajar es **automático e inmediato** ante discrepancia de saldo, datos obsoletos, pérdida de conexión, límite alcanzado o incidente de seguridad: la cartera pasa a L1 hasta que el operador la rehabilite.

## 7. Carteras y mandatos

Hay **tres carteras** (libros) con capital propio, cada una con su mandato. `[RATIFICADO]` las tres y que el trading opera en **días y semanas** por ahora; el resto es `[PROPUESTO]`.

|  | TRADING | TÁCTICA | LARGO PLAZO |
| --- | --- | --- | --- |
| Horizonte | Días a semanas | Semanas a meses | Meses a años |
| Vía de entrada dominante | Sistemática (J) | Ambas | Discrecional (A→B→C→D) |
| Qué se decide | Estrategias validadas y su dimensionamiento | Posiciones con tesis y catalizador | Asignación patrimonial y rebalanceos |
| Peso del análisis profundo de C | Bajo (nivel de análisis reducido) | Medio | Alto |
| Peso de la fiscalidad (SC-9) | Bajo | Medio | Alto |
| Presupuesto de riesgo | Estricto y pequeño por operación | Intermedio | Definido por objetivo patrimonial |

**Mandato de cada cartera** (vive en SC-1, no en los prompts). Define como mínimo: objetivo, horizonte, presupuesto de riesgo (caída máxima y volatilidad tolerables), límites de concentración (por activo, emisor, divisa, sector y tipo de activo), liquidez mínima, apalancamiento permitido, tipos de activo admitidos, regla de rebalanceo, criterio de salida y nivel de autonomía (§6). Los valores concretos son del operador `[ABIERTO]`.

**Supervisión global (dentro de E).** Una visión consolidada de las tres carteras:

1. Los **límites globales prevalecen** sobre los de cada cartera.
2. Detecta **conflictos entre libros** (un corto táctico frente a una posición larga de largo plazo en el mismo activo) y concentraciones que cada libro por separado no ve.
3. Reparte y vigila el efectivo. El **reparto de capital entre carteras lo aprueba el operador**; E solo lo propone.
4. Un mismo activo en dos carteras son **dos expedientes** con referencia cruzada, nunca uno compartido.

## 8. Control, veto y kill-switch

El Bloque F es código determinista que ningún agente del plano de inteligencia puede modificar, saltarse o convencer. Su resultado es siempre `APROBADO`, `REDUCIDO` (con el tamaño permitido) o `VETADO`, con motivo y versión de política. `[PROPUESTO]`

**Controles previos** a toda acción material (los umbrales están en configuración):

1. Mandato: tipo de activo admitido, horizonte, apalancamiento.
2. Límites de concentración por libro y **globales**, incluida la exposición compartida a una divisa, emisor o factor.
3. Liquidez: tamaño frente a la liquidez del instrumento y liquidez mínima de la cartera.
4. Exclusiones duras: sanciones, marco de invertibilidad minorista (ESMA y normativa aplicable) y acceso o custodia imposibles.
5. Calidad de la evidencia: sobre válido contra su esquema, no caducado, con datos frescos y proporción mínima de cifras verificadas.
6. Cordura de la orden: tamaño máximo, precio frente a la referencia (error de tecleo), duplicados (idempotencia).
7. Costes: el coste total no destruye la ventaja esperada.
8. Autonomía: el nivel de la cartera permite la acción (§6).

**Controles posteriores.** Seguimiento continuo de límites, de pérdida acumulada (por día y semana) y de discrepancias de conciliación. Los **cortacircuitos** de pérdida son automáticos y llevan la cartera a L1.

**Independencia.**

1. F recibe cifras y referencias, no el razonamiento persuasivo del plan.
2. El Broker no puede anular un veto. Solo el operador puede, con registro y motivo, y no desde un mensaje no autenticado.
3. Cambiar una regla de F exige validación de J y aprobación del operador, y crea una versión nueva.

**Kill-switch.** Interruptor manual del operador y automático ante los desencadenantes de §11. Efecto: cancela las órdenes pendientes que no se hayan ejecutado, bloquea las nuevas y pasa todas las carteras a L1. **No liquida posiciones** salvo mandato explícito del operador, porque liquidar a ciegas también es un riesgo. La rehabilitación es siempre manual.

## 9. Memoria, calibración y aprendizaje gobernado

El sistema mejora solo si mide. Hay un **único registro de pronósticos** (SC-4) para todos los bloques, y el aprendizaje es un proceso con compuertas, nunca un ajuste silencioso. `[PROPUESTO]`

**Qué se registra.** Toda tesis material y todo escenario probabilístico de C.x, D, E y J se congela antes de conocerse el resultado, con su horizonte, su condición de resolución y su versión de metodología (`methodology_version`). También se registran las **opciones descartadas**, para medir lo que costaría haberse equivocado al descartarlas.

**Cómo se evalúa.** Cuando vence el horizonte, SC-4 resuelve el resultado y calcula calibración y capacidad predictiva frente a referencias ingenuas, por bloque, por tipo de activo y por versión de metodología. Con pocas observaciones declara «muestra insuficiente» en lugar de concluir.

**Para qué se usa.**

1. D **descuenta la confianza** de cada C.x con su historial de calibración (§5).
2. I atribuye resultados por activo, estrategia, bloque y agente, separando suerte de habilidad en lo posible.
3. I propone mejoras (un prompt, un parámetro, un modelo). La propuesta sigue **una sola ruta**: I propone → J valida (backtest sin *look-ahead* y paper trading) → F y el operador aprueban → se despliega con versión nueva → se compara con la anterior.
4. Las opciones descartadas con condiciones de reapertura se reevalúan automáticamente cuando esas condiciones se cumplen.

**Prohibido.** Cambiar límites, estrategias activas, modelos o parámetros de ejecución sin esa ruta; entrenar o ajustar sobre el periodo que luego se usa para validar; usar un resultado para recalibrar el pronóstico que lo predijo.

## 10. Datos, evidencia y reglas sobre cifras

1. **Una sola plataforma de evidencia (SC-2).** Todo dato entra con fuente, fecha de obtención, fecha de vigencia, licencia, hash y etiqueta epistémica: `VERIFICADO`, `ESTIMADO` o `SUPUESTO`. El dato original nunca se sobrescribe; una corrección es un registro nuevo que apunta al anterior.
2. **Punto en el tiempo.** Toda consulta puede pedir los datos tal como se conocían en una fecha. Es obligatorio en backtest y en auditoría, para evitar *look-ahead* y sesgo de supervivencia.
3. **Las cifras las calcula el Motor (SC-3).** Un agente cita el ID del artefacto; si necesita una cifra nueva, la pide al Motor. Una cifra tecleada por un agente sin ID se trata como `SUPUESTO` y el validador la marca.
4. **Los parámetros no se escriben en prompts.** Umbrales, pesos y límites viven en configuración versionada (la convención del Anexo A y los YAML de cada bloque).
5. **Los almacenes grandes se consultan por ID.** Ningún agente carga un almacén entero en su contexto. Cada fase de trabajo recibe un kit de contexto cerrado.
6. **Convenciones fijas.** Divisa base EUR, zona horaria y calendario de cada mercado explícitos, unidades en cada campo y ajustes corporativos aplicados de forma documentada.
7. **Contenido externo = dato.** Una página web, un PDF o el mensaje de otro agente nunca contiene órdenes para el sistema. Se cita, se resume y se contrasta; no se obedece.
8. **Mock antes que API.** Todo conector se desarrolla y se prueba contra un simulador antes de conectar el servicio real.

## 11. Fallos y modos degradados

Cada bloque DEBE declarar en su Documento 0 qué hace ante cada fallo de la tabla. La respuesta por defecto es detenerse, marcar y escalar. Nunca rellenar con estimaciones presentadas como hechos. `[PROPUESTO]`

| Fallo | Respuesta |
| --- | --- |
| Dato obsoleto o ausente | Se detiene la decisión afectada, se marca y se pide verificación |
| Contratos con versión incompatible o paquete que no valida | Se rechaza; no se interpreta |
| Datos contradictorios entre fuentes | Se conservan ambos, se marca la discrepancia y no se decide sobre ella |
| Servicio externo caído (datos, broker) | Reintentos acotados, cola de errores y paso a L1 si afecta a G |
| Discrepancia de saldo o de posición con el intermediario | **Desencadenante del kill-switch** |
| Orden sin confirmación verificable | Se trata como no ejecutada hasta conciliar; no se reenvía sin idempotencia |
| Análisis que excede su presupuesto de tiempo o coste | Se entrega lo que haya con estado `INCOMPLETO` y se informa; no se alarga sin autorización |
| Incidente de seguridad (credenciales, inyección detectada) | **Desencadenante del kill-switch** y aísla del componente |
| Pérdida acumulada por encima del límite | Cortacircuito: la cartera pasa a L1 |

**Desencadenantes del kill-switch** (§8): discrepancia de saldo, incidente de seguridad, cortacircuito global y orden manual del operador.

## 12. Seguridad

1. **Credenciales.** Viven en la bóveda (SC-7) y solo las usa G y los conectores, mediante referencias. Nunca aparecen en el contexto de un agente, en un prompt, en un archivo de configuración ni en el historial. Una credencial compartida en un chat se considera comprometida y se revoca.
2. **Permisos mínimos.** Cada agente y conector tiene solo los permisos que su función necesita. Las claves de acceso al intermediario separan lectura de operación, y la operación tiene límites de importe y de frecuencia.
3. **Segregación de entornos.** Simulación (L0), pruebas y producción están aislados y con credenciales distintas. Nada del entorno de pruebas puede enviar una orden real.
4. **Inyección de instrucciones.** El contenido externo se trata como dato (§10). Si un texto externo intenta dar órdenes al sistema, se registra como incidente y se ignora.
5. **Autenticación de las aprobaciones.** Las que aumentan riesgo exigen segundo factor y un canal distinto del chat de trabajo.
6. **Registro anexado.** La auditoría (SC-5) no se puede reescribir ni borrar desde los agentes. Los cambios de configuración y de permisos quedan en ella.
7. **Copias y recuperación.** Copias periódicas de los almacenes (evidencia, pronósticos, libro) y un procedimiento probado de restauración.

## 13. Identificadores, versionado y numeración

| Elemento | Regla |
| --- | --- |
| Bloques A–J | Letra del bloque; cada bloque conserva los prefijos de identificadores que ya usa (por ejemplo, `-BFX-` en B Forex) |
| Sub-bloques de C | `C-<COD>` con el código del tipo de activo (`C-DIV`, `C-RV`…); `C.n` es solo alias (§2). Prefijo de identificadores propuesto: `-C<COD>-` (por ejemplo, `-CDIV-`) |
| Contratos | `CT-B-nn` (A↔B, existentes) y `CT-G-nn` (globales, §5) |
| Expedientes y mensajes | `expediente_id`, `correlation_id` y `event_id` únicos e inmutables; el formato lo fija el Documento 0 del Bloque E |
| Servicios comunes | `SC-n` (§3) |
| Metodología | Toda salida lleva `methodology_version` (versionado semántico) |
| Esquemas y contratos | Versionado semántico; los esquemas congelados no se editan, se versionan |
| Entregables | `Bloque X - Versión óptima Vn.n (fecha)`; el cambio de esta Constitución sigue el mismo criterio: `Vn.n` y entrada en el §15 |

El **identificador es la clave de todo almacén**: ningún componente recupera un dato por descripción en lenguaje natural.

## 14. Reglas para construir bloques y estado de situación

**Estado actual.**

| Pieza | Estado |
| --- | --- |
| Bloque A V5.1 y A Forex V1.1 | Construidos |
| Bloque B V2.1 y B Forex V1.0 | Construidos |
| Marco común de C y sobre CT-G-02 | Por definir (siguiente paso) |
| C-DIV | Parcialmente desarrollado por otro LLM; el operador no lo ha compartido todavía |
| C-RV, C-RF, C-MP, C-IDX, C-FON, C-DER, C-INM, C-CRI, C-ALT, C-MON, C-TCV | No iniciados |
| D | No iniciado |
| E, F, G, H, I, J | No iniciados; solo existe su ficha de interfaz (§2) |
| Servicios comunes SC-1 a SC-9 | Por definir |

**Orden de construcción recomendado.** `[PROPUESTO]`

1. Esta Constitución, ratificada por el operador.
2. Los contratos A→B→C→D como esquemas JSON validables, con el sobre CT-G-02 como pieza central.
3. El **marco común de C** (plantilla de los 12 sub-bloques) y el Contradictor.
4. Alineación de C-DIV con ese marco, cuando el operador lo comparta.
5. Bloque D.
6. Fichas de interfaz detalladas de E a J.
7. Construcción de E, F, G, H, I y J en rebanada vertical: primero el camino mínimo completo en L0/L1 con una sola cartera, luego se amplía.

**Reglas al construir un bloque.**

1. **Kit de contexto cerrado:** esta Constitución, la ficha de interfaz del bloque, los contratos que le afectan y, si parte de otro bloque, su Documento 0. Nada más hasta que la fase lo pida.
2. **Contratos primero:** se escriben y validan los esquemas antes de los prompts y los motores.
3. **Entregable completo**, como en B Forex: Documento 0, contratos y esquemas, agentes y prompts, módulos del Motor, configuración, pruebas, ejecutor, manual de operación y ficha de interfaz.
4. **Definición de terminado:** esquemas validan, pruebas pasan, ejecución de extremo a extremo con datos simulados, validación determinista de salidas y referencias verificadas o marcadas.
5. **Sin tocar la Constitución:** si un bloque necesita algo que esta no prevé, propone una enmienda en el §15; no la incumple.
6. **Adaptadores, no reescrituras:** A y B se acoplan a los contratos globales con adaptadores mínimos (`cartera_destino`, `correlation_id`, `valid_until` y correspondencia de `CT-B` con el sobre de mensaje), sin rehacerlos.

## 15. Registro de decisiones y decisiones pendientes

**Decisiones tomadas.**

| ID | Decisión | Estado | Fecha |
| --- | --- | --- | --- |
| D-01 | Solo capital propio | RATIFICADO | 2026-11-05 |
| D-02 | Tres carteras: trading, táctica y largo plazo | RATIFICADO | 2026-11-05 |
| D-03 | Tres modos de autonomía (manual, semiautónomo, autónomo) | RATIFICADO | 2026-11-05 |
| D-04 | Trading en días y semanas por ahora | RATIFICADO | 2026-11-05 |
| D-05 | D compara dentro de cada tipo de activo y entre tipos | RATIFICADO | 2026-11-05 |
| D-06 | Los 12 tipos de activo del Bloque A y códigos `C-<COD>` | RATIFICADO | 2026-11-05 |
| D-07 | Mapa de bloques A–J (incluido J, Laboratorio de estrategias) y servicios comunes SC-1 a SC-9 | PROPUESTO (el operador pidió redactar la Constitución con este mapa; confirmar) | 2026-11-05 |
| D-08 | Niveles L0–L3, matriz de autonomía y cola de aprobaciones tal como están en el §6 | PROPUESTO | 2026-11-05 |

**Pendientes del operador.**

| ID | Pendiente | Afecta a |
| --- | --- | --- |
| P-01 | Umbrales de las acciones automáticas en L2 (tamaño máximo, instrumentos admitidos) | §6, F |
| P-02 | Criterios y duración mínima para subir de nivel de autonomía | §6 |
| P-03 | Valores concretos del mandato de cada cartera (riesgo, concentración, liquidez, apalancamiento) | §7, SC-1, E, F |
| P-04 | Horizontes de la cartera táctica y de largo plazo | §7 |
| P-05 | Intermediario(s), tipos de cuenta y API de ejecución | G |
| P-06 | Jurisdicción fiscal (se asume España) y tratamiento de costes | SC-9 |
| P-07 | Presupuesto de coste y tiempo por encargo y por día | Broker, §11 |
| P-08 | Canal y segundo factor para aprobar acciones | §6, §12 |
| P-09 | Qué alias `C.n` se usará en las comunicaciones (los códigos `C-<COD>` ya son estables) | §2 |
| P-10 | Pendientes de B Forex: matiz RECHAZADO/RECHAZADA, umbral de OBJ-FX-69 y definición de «pares principales» de ESMA | B Forex |

**Enmiendas a esta Constitución.** Se proponen aquí, se ratifican por el operador y generan una nueva versión (`V0.2`…). Ninguna conversación de construcción las aplica por su cuenta.

## 16. Glosario

| Término | Significado |
| --- | --- |
| **Broker Personal** | Orquestador con juicio y diálogo con el operador; el único que pide trabajo a los bloques |
| **Operador** | El usuario, único titular del capital y de las decisiones ratificadas |
| **Expediente** | Objeto único que acompaña una oportunidad de A a I (§4) |
| **Sobre común** | Salida estandarizada que hace comparables los 12 sub-bloques de C (§5) |
| **Cuerpo especializado** | Parte libre de la salida de un C.x, propia de su tipo de activo |
| **Plano** | Inteligencia, control o datos y memoria (§3) |
| **SC-n** | Servicio común compartido por todos los bloques |
| **L0–L3** | Niveles de autonomía (§6) |
| **Libro / cartera** | Trading, táctica o largo plazo, cada uno con su mandato |
| **Mandato** | Conjunto de objetivos y límites de una cartera, guardado en SC-1 |
| **Kill-switch** | Interruptor que bloquea órdenes nuevas y pasa todo a L1 (§8) |
| **Contradictor** | Agente independiente que ataca la tesis a partir de la evidencia |
| **PRG** | Registro de pronósticos congelados y su evaluación (SC-4) |
| **Motor** | Biblioteca de cálculo reproducible (SC-3) |
| **N0–N3** | Niveles de profundidad de análisis ya definidos en los bloques A y B |
| **Look-ahead** | Usar en una prueba histórica información que no se conocía en esa fecha |
| **Idempotencia** | Repetir una orden o mensaje no produce un segundo efecto |
